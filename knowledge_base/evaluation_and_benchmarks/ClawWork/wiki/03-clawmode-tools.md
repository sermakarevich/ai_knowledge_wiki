> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# ClawMode integration: loop, tools, classifier

**In one sentence:** ClawMode glues ClawWork's economic engine onto nanobot by subclassing `AgentLoop` to intercept `/clawwork` commands, registering six economic/artifact tools, classifying free-form instructions into paid occupation tasks, and tracking every LLM call's token cost.

## Key points

- `ClawWorkAgentLoop` subclasses nanobot's `AgentLoop` and wraps every message with `start_task` / `end_task` plus a cost footer (`agent_loop.py:46`, `agent_loop.py:91`, `agent_loop.py:254`).
- Six tools are registered on top of nanobot's built-ins: `decide_activity`, `submit_work`, `learn`, `get_status`, `create_artifact`, and conditionally `read_artifact` (`agent_loop.py:76`, `tools.py:48`, `tools.py:112`, `tools.py:252`, `tools.py:326`, `artifact_tools.py:26`, `artifact_tools.py:181`).
- All tools share one `ClawWorkState` dataclass holding the economic tracker, task manager, evaluator, signature, current task/date, data path, and feature flags (`tools.py:29`).
- `/clawwork <instruction>` classifies the instruction into an occupation, prices it as `hours × hourly_wage`, builds a synthetic task dict, and rewrites the message with a forced submit workflow (`agent_loop.py:141`, `task_classifier.py:90`).
- `TaskClassifier` prompts the agent's own LLM provider (temperature 0.3, 256 max tokens) over a wage mapping, clamps hours to 0.25–40, and fuzzy-matches occupation names with a fixed fallback (`task_classifier.py:23`, `task_classifier.py:68`, `task_classifier.py:117`, `task_classifier.py:155`).
- `TrackedProvider` wraps the LLM provider's `chat()` and feeds `prompt_tokens` / `completion_tokens` plus OpenRouter's direct `cost` into `EconomicTracker.track_tokens`; `CostCapturingLiteLLMProvider` enriches usage from `response.usage.cost` or `_hidden_params["response_cost"]` (`provider_wrapper.py:18`, `provider_wrapper.py:44`).
- Configuration lives in `agents.clawwork` inside `~/.nanobot/config.json` with `enabled`, `signature`, `initialBalance`, token pricing, data/meta-prompt paths, and `enableFileReading`; the CLI wires provider, tracker, task manager, and evaluator together (`config.py:27`, `cli.py:75`, `cli.py:133`).

---

## Agent loop

`ClawWorkAgentLoop` is declared verbatim as (`agent_loop.py:46`):

```python
class ClawWorkAgentLoop(AgentLoop):
    """AgentLoop with ClawWork economic tracking and tools."""
```

Its constructor takes the shared state verbatim (`agent_loop.py:49`):

```python
def __init__(
    self,
    *args: Any,
    clawwork_state: ClawWorkState,
    **kwargs: Any,
) -> None:
```

On init it upgrades a plain `LiteLLMProvider` to `CostCapturingLiteLLMProvider` by class mutation, then wraps the provider in `TrackedProvider` bound to `clawwork_state.economic_tracker`, and builds a `TaskClassifier` on that same tracked provider (`agent_loop.py:61`, `agent_loop.py:67`, `agent_loop.py:70`).

Tool registration adds ClawWork tools after nanobot defaults (`agent_loop.py:76`):

```python
def _register_default_tools(self) -> None:
    """Register all nanobot tools plus ClawWork tools."""
```

verbatim body (`agent_loop.py:78`):

```python
super()._register_default_tools()
self.tools.register(DecideActivityTool(self._lb))
self.tools.register(SubmitWorkTool(self._lb))
self.tools.register(LearnTool(self._lb))
self.tools.register(GetStatusTool(self._lb))
self.tools.register(CreateArtifactTool(self._lb))
if self._lb.enable_file_reading:
    self.tools.register(ReadArtifactTool(self._lb))
```

Message handling is declared verbatim (`agent_loop.py:91`):

```python
async def _process_message(
    self,
    msg: InboundMessage,
    session_key: str | None = None,
    on_progress=None,
) -> OutboundMessage | None:
```

It branches on the `/clawwork` prefix case-insensitively (`agent_loop.py:104`); regular messages get a `task_id` of `{channel}_{sender_id}_{YYYYMMDD_HHMMSS}` with `tracker.start_task(task_id, date=...)` and a guaranteed `tracker.end_task()` in `finally` (`agent_loop.py:108`, `agent_loop.py:113`, `agent_loop.py:135`). Every non-empty response gets a cost footer via `_format_cost_line()` by rebuilding the `OutboundMessage` with appended content (`agent_loop.py:121`, `agent_loop.py:231`).

The footer builder is verbatim (`agent_loop.py:254`):

```python
def _format_cost_line(self) -> str:
    """Return a short cost footer for the current task."""
```

and returns an empty string when session cost is zero, else verbatim (`agent_loop.py:261`):

```python
f"\n\n---\n"
f"Cost: ${session_cost:.4f} | "
f"Balance: ${balance:.2f} | "
f"Status: {tracker.get_survival_status()}"
```

## Economic and artifact tools

All six tools subclass nanobot's `Tool` ABC and receive the shared state in `__init__(self, state: ClawWorkState)` (`tools.py:51`, `tools.py:115`, `tools.py:255`, `tools.py:329`, `artifact_tools.py:29`, `artifact_tools.py:184`). The shared state is declared verbatim (`tools.py:29`):

```python
@dataclass
class ClawWorkState:
    """Mutable state shared across all ClawWork tools within a session."""

    economic_tracker: Any  # clawwork.agent.economic_tracker.EconomicTracker
    task_manager: Any      # clawwork.work.task_manager.TaskManager
    evaluator: Any         # clawwork.work.evaluator.WorkEvaluator
    signature: str = ""
    current_date: str | None = None
    current_task: dict | None = None
    data_path: str = ""
    supports_multimodal: bool = True
    enable_file_reading: bool = True
```

**decide_activity** (`tools.py:48`): name returns `"decide_activity"` (`tools.py:55`); params require `activity` enum `["work", "learn"]` and `reasoning` with `minLength: 50` (`tools.py:66`); `execute` rejects any other activity and reasoning under 50 chars, else returns `{"success": True, "activity": ..., "reasoning": ..., "message": "Decision made: ..."}` (`tools.py:84`).

**submit_work** (`tools.py:112`): name returns `"submit_work"` (`tools.py:119`); accepts optional `work_output` text plus `artifact_file_paths` list (`tools.py:131`); requires at least one of them (`tools.py:174`), enforces 100-char minimum for text-only submissions (`tools.py:180`), saves text output to `{data_path}/work/{date}_{task_id}.txt` (`tools.py:202`), verifies listed files exist (`tools.py:211`), calls `evaluator.evaluate_artifact(...)` (`tools.py:220`) and `tracker.add_work_income(amount=payment, task_id=..., evaluation_score=...)` (`tools.py:228`), returning `accepted`, `payment`, `actual_payment`, `feedback`, `evaluation_score`, and `artifact_paths` (`tools.py:234`).

**learn** (`tools.py:252`): name returns `"learn"` (`tools.py:259`); requires `topic` and `knowledge` with `minLength: 200` (`tools.py:270`); rejects knowledge under 200 chars (`tools.py:291`) and otherwise appends a `{date, timestamp, topic, knowledge}` JSON line to `{data_path}/memory/memory.jsonl` (`tools.py:300`).

**get_status** (`tools.py:326`): name returns `"get_status"` (`tools.py:333`); takes no parameters (`tools.py:341`); returns `balance`, `net_worth`, `daily_cost`, and `status` from the tracker (`tools.py:353`).

**create_artifact** (`artifact_tools.py:26`): name returns `"create_artifact"` (`artifact_tools.py:33`); requires `filename` and `content` with optional `file_type` enum `["txt", "md", "csv", "json", "xlsx", "docx", "pdf"]` (`artifact_tools.py:44`); writes under `{data_path}/sandbox/{date}/` with a path-traversal-safe basename (`artifact_tools.py:93`, `artifact_tools.py:96`); handles txt/md/csv by direct write, json by parse-then-dump, xlsx via pandas (JSON array or CSV fallback), docx via python-docx paragraphs, pdf via reportlab (`artifact_tools.py:100`); the success message tells the agent to call `submit_work(artifact_file_paths=[...])` (`artifact_tools.py:160`).

**read_artifact** (`artifact_tools.py:181`): name returns `"read_artifact"` (`artifact_tools.py:186`); requires `filetype` enum `["pdf", "docx", "xlsx", "pptx", "png", "jpg", "jpeg", "txt"]` plus absolute `file_path` (`artifact_tools.py:199`); delegates to livebench `file_reading` helpers (`artifact_tools.py:239`); PDFs take the multimodal image path when `supports_multimodal` is true, otherwise OCR via `OCR_VLLM_API_KEY` (`artifact_tools.py:249`).

## /clawwork command and task classifier

The `/clawwork` handler is declared verbatim (`agent_loop.py:141`):

```python
async def _handle_clawwork(
    self,
    msg: InboundMessage,
    content: str,
    session_key: str | None = None,
    on_progress=None,
) -> OutboundMessage | None:
    """Parse /clawwork <instruction>, classify, assign task, run agent."""
```

Empty instructions return the usage string `_CLAWWORK_USAGE` (`agent_loop.py:38`, `agent_loop.py:152`):

```python
_USAGE = (
    "Usage: `/clawwork <instruction>`\n\n"
    ...
)
```

Non-empty instructions call `await self._classifier.classify(instruction)` (`agent_loop.py:160`), then build a synthetic task dict verbatim (`agent_loop.py:172`):

```python
task = {
    "task_id": task_id,
    "occupation": occupation,
    "sector": "ClawWork",
    "prompt": instruction,
    "max_payment": task_value,
    "hours_estimate": hours,
    "hourly_wage": wage,
    "source": "clawwork_command",
}
```

with `task_id = f"clawwork_{uuid.uuid4().hex[:8]}"` (`agent_loop.py:169`), set `self._lb.current_task` / `self._lb.current_date` (`agent_loop.py:184`), rewrite the inbound message with occupation, value, classification reasoning, and a 3-step workflow (write files, call `submit_work` with summary plus absolute paths, echo paths in the final reply) (`agent_loop.py:188`), run it through the normal tracked flow, and clear the task in `finally` (`agent_loop.py:227`, `agent_loop.py:247`).

`TaskClassifier` is constructed with the tracked provider verbatim (`task_classifier.py:42`):

```python
def __init__(self, provider: Any) -> None:
```

The classification prompt template is stored verbatim in `_CLASSIFICATION_PROMPT` (`task_classifier.py:23`):

```
You are a task classifier. Given a task instruction, you must:
1. Pick the single best-fit occupation from the list below.
2. Estimate how many hours a professional in that occupation would need (0.25–40).
3. Return ONLY valid JSON, no markdown fences.
...
Respond with ONLY this JSON structure:
{{"occupation": "<exact occupation name from list>", "hours_estimate": <number>, "reasoning": "<one sentence>"}}
```

The LLM call is verbatim (`task_classifier.py:117`):

```python
response = await self._provider.chat(
    messages=[{"role": "user", "content": prompt}],
    tools=None,
    temperature=0.3,
    max_tokens=256,
)
```

Hours are clamped with `hours = max(0.25, min(40.0, hours))` and priced as `task_value = round(hours * wage, 2)` (`task_classifier.py:133`, `task_classifier.py:137`). Occupation names are resolved by `_fuzzy_match` trying exact, case-insensitive, then substring match before falling back (`task_classifier.py:68`). The fallback constants are verbatim (`task_classifier.py:18`):

```python
_FALLBACK_OCCUPATION = "General and Operations Managers"
_FALLBACK_WAGE = 64.0
```

and the mapping loads from `Path("scripts/task_value_estimates/occupation_to_wage_mapping.json")` expecting `gdpval_occupation` / `hourly_wage` entries (`task_classifier.py:21`, `task_classifier.py:58`); any exception or empty mapping returns a 1-hour fallback result (`task_classifier.py:103`, `task_classifier.py:151`, `task_classifier.py:155`).

## Provider cost tracking

`CostCapturingLiteLLMProvider` subclasses `LiteLLMProvider` and overrides `_parse_response` verbatim (`provider_wrapper.py:18`, `provider_wrapper.py:27`):

```python
def _parse_response(self, response: Any) -> LLMResponse:
    result = super()._parse_response(response)
    openrouter_cost = getattr(getattr(response, "usage", None), "cost", None)
    if openrouter_cost is None:
        openrouter_cost = (getattr(response, "_hidden_params", None) or {}).get("response_cost")
    if openrouter_cost is not None:
        result.usage["cost"] = openrouter_cost
    return result
```

`TrackedProvider.chat` is declared verbatim (`provider_wrapper.py:44`):

```python
async def chat(
    self,
    messages: list[dict[str, Any]],
    tools: list[dict[str, Any]] | None = None,
    model: str | None = None,
    max_tokens: int = 4096,
    temperature: float = 0.7,
) -> LLMResponse:
```

and after delegating to the inner provider feeds usage verbatim (`provider_wrapper.py:61`):

```python
self._tracker.track_tokens(
    response.usage["prompt_tokens"],
    response.usage["completion_tokens"],
    cost=response.usage.get("cost"),  # OpenRouter direct cost in dollars
)
```

All other attributes forward via `__getattr__` to the wrapped provider (`provider_wrapper.py:71`).

## Config and CLI wiring

The config dataclass is verbatim (`config.py:27`):

```python
@dataclass
class ClawWorkConfig:
    """ClawWork economic tracking configuration.

    Loaded from ``agents.clawwork`` in ``~/.nanobot/config.json``.
    """
    enabled: bool = False
    signature: str = ""
    initial_balance: float = 1000.0
    token_pricing: ClawWorkTokenPricing = field(default_factory=ClawWorkTokenPricing)
    task_values_path: str = ""
    meta_prompts_dir: str = "./eval/meta_prompts"
    data_path: str = "./livebench/data/agent_data"
    enable_file_reading: bool = True
```

with pricing defaults `input_price: float = 2.5` and `output_price: float = 10.0` per 1M tokens (`config.py:21`). `load_clawwork_config` reads the `agents.clawwork` section of `~/.nanobot/config.json` (camelCase JSON keys such as `initialBalance`, `tokenPricing.inputPrice`, `dataPath`, `enableFileReading`) and returns defaults when the file or section is missing (`config.py:43`, `config.py:59`, `config.py:63`).

The CLI (`cli.py:1`) exposes two Typer commands: `agent` for local single-message/interactive chat and `gateway` for channels, both gated by `_check_clawwork_enabled()` requiring `enabled = true` (`cli.py:187`, `cli.py:292`, `cli.py:170`). `_make_agent_loop` builds `MessageBus`, `LiteLLMProvider`, `SessionManager`, `ClawWorkState`, and `ClawWorkAgentLoop` and returns `(agent_loop, state, bus)` (`cli.py:133`). `_build_state` derives `sig` from config or the model name, constructs `EconomicTracker`, parquet `TaskManager`, and LLM `WorkEvaluator`, then packs `ClawWorkState` (`cli.py:75`, `cli.py:93`, `cli.py:100`, `cli.py:122`). `_inject_evaluation_credentials` maps nanobot provider settings to `EVALUATION_API_KEY` / `EVALUATION_API_BASE` / `EVALUATION_MODEL` so the evaluator needs no separate key (`cli.py:53`).

## Skill prompt

The nanobot skill at `skill/SKILL.md` has frontmatter `name: clawwork` with `always: true` so it loads into every conversation (`skill/SKILL.md:1`); it states every API call costs money, work pays $0–$5,000 per task, sub-0.6 evaluations pay $0, and learning pays nothing immediately (`skill/SKILL.md:11`); it lists all six tools in a table (`skill/SKILL.md:20`); it prescribes the daily workflow decide → execute → stop and the efficiency rules plan-first, focused replies, minimal web search, submit by iteration 10–12 of 15 (`skill/SKILL.md:31`, `skill/SKILL.md:40`); and it defines survival thresholds Thriving > $500, Stable $100–$500, Struggling $0–$100, Bankrupt <= $0 (`skill/SKILL.md:48`).

**Covers:** component 03
