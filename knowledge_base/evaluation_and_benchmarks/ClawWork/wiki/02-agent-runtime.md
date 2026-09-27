> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Live agent runtime and economic tracking

**In one sentence:** The live agent runtime runs one `LiveAgent` per configured signature over weekdays in a date range, charging every LLM and API call against a dollar balance via `EconomicTracker` and paying work income only when the evaluation score clears 0.6.

## Key points
- Entry point `main.py` loads `config["livebench"]`, resolves dates, pricing, task source, and enabled agents, then constructs one `LiveAgent` per agent and runs it (`livebench/main.py:49`, `livebench/main.py:116`, `livebench/main.py:161`).
- `LiveAgent` owns `EconomicTracker`, `TaskManager`, `WorkEvaluator`, direct tools, and a tool-bound `ChatOpenAI` model, with per-day state (`current_date`, `current_task`, `daily_activity`) (`livebench/agent/live_agent.py:50`, `livebench/agent/live_agent.py:131`, `livebench/agent/live_agent.py:687`).
- The daily loop `run_daily_session(date)` selects one task, starts cost tracking, builds the economic system prompt, runs up to 15 tool-calling iterations, then saves end-of-day state (`livebench/agent/live_agent.py:546`, `livebench/agent/live_agent.py:584`, `livebench/agent/live_agent.py:698`, `livebench/agent/live_agent.py:924`).
- `EconomicTracker` deducts token/API costs in real time, writes `balance.jsonl` / `token_costs.jsonl` / `task_completions.jsonl`, and gates pay on `min_evaluation_threshold=0.6` (`livebench/agent/economic_tracker.py:52`, `livebench/agent/economic_tracker.py:158`, `livebench/agent/economic_tracker.py:358`).
- Survival status is derived from balance: bankrupt `<= 0`, struggling `< 100`, stable `< 500`, else thriving (`livebench/agent/economic_tracker.py:524`).
- The system prompt injects balance, token-cost warnings, work-vs-learn choice, and the full work task plus reference-file paths (`livebench/prompts/live_agent_prompt.py:12`, `livebench/prompts/live_agent_prompt.py:115`, `livebench/prompts/live_agent_prompt.py:157`).
- On iteration-limit timeout without submission, a LangGraph `WrapUpWorkflow` lists sandbox artifacts, asks the LLM to pick deliverables, downloads, and submits them (`livebench/agent/wrapup_workflow.py:41`, `livebench/agent/wrapup_workflow.py:64`, `livebench/agent/live_agent.py:849`).

---

## Entry point and run modes

`livebench/main.py:33` defines the per-agent runner verbatim:

```python
async def run_agent(agent: LiveAgent, init_date: str, end_date: str, exhaust: bool = False):
```

`livebench/main.py:49` defines the top-level verbatim:

```python
async def main(config_path: str, exhaust: bool = False):
```

Behavior (`livebench/main.py:55`, `livebench/main.py:59`, `livebench/main.py:116`, `livebench/main.py:161`):
- Loads JSON config and reads `config["livebench"]`.
- Resolves `init_date`/`end_date` from `INIT_DATE`/`END_DATE` env overrides or `lb_config["date_range"]`.
- Prints starting balance (`livebench/main.py:66`), token pricing (`livebench/main.py:76`), and task-source config supporting new `task_source` format plus legacy `gdpval_path` (`livebench/main.py:81`, `livebench/main.py:94`).
- Filters `lb_config["agents"]` by `enabled` (`livebench/main.py:116`), constructs `LiveAgent(...)` with economic, task-source, filter/assignment, evaluation, `tasks_per_day`, and `supports_multimodal` arguments (`livebench/main.py:161`), then awaits `run_agent` (`livebench/main.py:194`).
- CLI (`livebench/main.py:210`) defaults config to `livebench/configs/default_config.json` (`livebench/main.py:217`) and adds `--exhaust` mode that runs every GDPVal task past `end_date` with up to 10 retries per task (`livebench/main.py:219`, `livebench/agent/live_agent.py:1050`).

## LiveAgent construction

`livebench/agent/live_agent.py:50` defines verbatim:

```python
def __init__(
    self,
    signature: str,
    basemodel: str,
    initial_balance: float = 1000.0,
    input_token_price: float = 0.01,
    output_token_price: float = 0.03,
    max_work_payment: float = 50.0,
```

Full constructor continues with `mcp_config`, `data_path`, `max_steps=20`, `max_retries=5`, `base_delay=1.0`, `api_timeout=60.0`, task-source/filter/assignment, `task_values_path`, evaluation, `tasks_per_day=1`, `supports_multimodal=True` (`livebench/agent/live_agent.py:58`, `livebench/agent/live_agent.py:66`, `livebench/agent/live_agent.py:75`, `livebench/agent/live_agent.py:78`).
- Data path defaults to `./livebench/data/agent_data/{signature}` (`livebench/agent/live_agent.py:120`).
- Components wired here: `EconomicTracker` rooted at `<data_path>/economic` (`livebench/agent/live_agent.py:131`), `TaskManager` with task-source/filters/values (`livebench/agent/live_agent.py:140`), `WorkEvaluator` with `use_llm_evaluation` and `meta_prompts_dir` (`livebench/agent/live_agent.py:151`).
- Default MCP config points at `http://localhost:{LIVEBENCH_HTTP_PORT:-8010}/mcp` with trading disabled (`livebench/agent/live_agent.py:181`, `livebench/agent/live_agent.py:189`).
- `initialize()` loads tasks, loads direct tools via `get_all_tools()`, sets global tool state, and builds `ChatOpenAI(model=basemodel)` with proxy-bypassing httpx clients (`livebench/agent/live_agent.py:192`, `livebench/agent/live_agent.py:200`, `livebench/agent/live_agent.py:205`, `livebench/agent/live_agent.py:231`).

## Daily session loop

`livebench/agent/live_agent.py:546` defines verbatim:

```python
async def run_daily_session(self, date: str) -> Optional[str]:
```

Stages (`livebench/agent/live_agent.py:558`, `livebench/agent/live_agent.py:573`, `livebench/agent/live_agent.py:584`, `livebench/agent/live_agent.py:634`):
- Sets up `activity_logs/<date>/log.jsonl` and terminal log (`livebench/agent/live_agent.py:377`, `livebench/agent/live_agent.py:558`).
- Resets `daily_work_income`, `last_evaluation_score`, `last_work_submitted` (`livebench/agent/live_agent.py:566`).
- Returns early if `is_bankrupt()` (`livebench/agent/live_agent.py:573`).
- Selects task via `task_manager.select_daily_task(date, signature)`; returns `"NO_TASKS_AVAILABLE"` or `"ERROR"` markers (`livebench/agent/live_agent.py:584`).
- Starts cost tracking with `economic_tracker.start_task(task_id, date=date)` (`livebench/agent/live_agent.py:596`) and copies reference files to `<data_path>/sandbox/<date>/reference_files/` plus uploads to the code sandbox (`livebench/agent/live_agent.py:242`, `livebench/agent/live_agent.py:610`).
- Builds economic summary and system prompt via `get_live_agent_system_prompt(...)` (`livebench/agent/live_agent.py:677`), binds tools with `model.bind_tools(tools)` (`livebench/agent/live_agent.py:687`).
- Reasoning loop is hardcoded `max_iterations = 15` (`livebench/agent/live_agent.py:698`); each turn calls `_ainvoke_with_retry(messages, timeout=api_timeout)` with `max_retries` and linear backoff `base_delay * attempt` (`livebench/agent/live_agent.py:393`, `livebench/agent/live_agent.py:467`).
- Tool dispatch goes through `_execute_tool`, resolving alias `execute_code_sandbox -> execute_code` (`livebench/agent/live_agent.py:487`, `livebench/agent/live_agent.py:491`).
- `submit_work` ends task tracking, records `actual_payment`/`evaluation_score` into daily income, and marks completion; `learn` success also ends the day (`livebench/agent/live_agent.py:765`, `livebench/agent/live_agent.py:793`).
- Text-only turns without tool calls get a nudge forcing `execute_code_sandbox` then `submit_work` (`livebench/agent/live_agent.py:812`).
- End of day: cleanup sandbox (`livebench/agent/live_agent.py:898`), record `record_task_completion` only when work was submitted without API error (`livebench/agent/live_agent.py:911`), then `save_daily_state` (`livebench/agent/live_agent.py:924`); returns `"API_ERROR"` on provider failure (`livebench/agent/live_agent.py:951`).

## Date-range and exhaust drivers

- `run_date_range(init_date, end_date)` iterates weekdays only, skips dates already in `task_completions.jsonl`, stops on `NO_TASKS_AVAILABLE` or bankruptcy (`livebench/agent/live_agent.py:993`, `livebench/agent/live_agent.py:1021`, `livebench/agent/live_agent.py:1033`, `livebench/agent/live_agent.py:1040`).
- Resume state comes from `_load_already_done()`, which repopulates `task_manager.used_tasks` and `daily_tasks` from `economic/task_completions.jsonl` (`livebench/agent/live_agent.py:954`, `livebench/agent/live_agent.py:968`).
- `run_exhaust_mode(init_date, max_task_failures=10)` force-assigns each task ID to successive weekdays, retries only `API_ERROR` outcomes, abandons after 10 failures, and advances the date past the last recorded date on resume (`livebench/agent/live_agent.py:1050`, `livebench/agent/live_agent.py:1114`, `livebench/agent/live_agent.py:1158`, `livebench/agent/live_agent.py:1171`).

## EconomicTracker: costs, income, persistence

`livebench/agent/economic_tracker.py:24` defines verbatim:

```python
def __init__(
    self,
    signature: str,
    initial_balance: float = 1000.0,
    input_token_price: float = 2.5,  # per 1M tokens
    output_token_price: float = 10.0,  # per 1M tokens
    data_path: Optional[str] = None,
    min_evaluation_threshold: float = 0.6  # Minimum score to receive payment
):
```

- Files: `balance.jsonl`, `token_costs.jsonl`, `task_completions.jsonl` under the agent economic dir (`livebench/agent/economic_tracker.py:52`).
- `start_task(task_id, date)` opens channel buckets `llm_tokens/search_api/ocr_api/other_api` plus detailed `llm_calls`/`api_calls` lists and day wall-clock markers (`livebench/agent/economic_tracker.py:117`, `livebench/agent/economic_tracker.py:133`, `livebench/agent/economic_tracker.py:141`); `end_task()` writes one consolidated record (`livebench/agent/economic_tracker.py:146`, `livebench/agent/economic_tracker.py:288`).
- `track_tokens(input_tokens, output_tokens, api_name="agent", cost=None)` uses the verbatim formula or a precomputed OpenRouter cost, then decrements balance (`livebench/agent/economic_tracker.py:158`, `livebench/agent/economic_tracker.py:172`):

```python
cost = (
    (input_tokens / 1_000_000.0) * self.input_token_price +
    (output_tokens / 1_000_000.0) * self.output_token_price
)
```

- `track_api_call(tokens, price_per_1m, api_name)` and `track_flat_api_call(cost, api_name)` route search/OCR/other channels by name match and decrement balance (`livebench/agent/economic_tracker.py:203`, `livebench/agent/economic_tracker.py:246`, `livebench/agent/economic_tracker.py:223`).
- `add_work_income(amount, task_id, evaluation_score, description="")` pays zero when `evaluation_score < 0.6`, else credits balance and `total_work_income` (`livebench/agent/economic_tracker.py:358`, `livebench/agent/economic_tracker.py:381`).
- `save_daily_state(date, ...)` appends a balance record with token delta, income, completed tasks, wall-clock seconds, and `api_error`, then resets daily/session counters (`livebench/agent/economic_tracker.py:438`, `livebench/agent/economic_tracker.py:476`).
- Status mapping in `get_survival_status()` is verbatim thresholds on `current_balance` (`livebench/agent/economic_tracker.py:524`):

```python
if self.current_balance <= 0:
    return "bankrupt"
elif self.current_balance < 100:
    return "struggling"
elif self.current_balance < 500:
    return "stable"
else:
    return "thriving"
```

- `track_response_tokens(response, economic_tracker, logger, is_openrouter, api_name="agent")` prefers `response_metadata["token_usage"]` raw counts, falls back to `usage_metadata`, and passes OpenRouter dollar cost through directly (`livebench/agent/economic_tracker.py:842`, `livebench/agent/economic_tracker.py:857`, `livebench/agent/economic_tracker.py:868`).

## Prompts and cost surfacing

`livebench/prompts/live_agent_prompt.py:9` defines verbatim:

```python
STOP_SIGNAL = "<FINISH_SIGNAL>"
```

`livebench/prompts/live_agent_prompt.py:12` defines verbatim:

```python
def get_live_agent_system_prompt(
    date: str,
    signature: str,
    economic_state: Dict,
    work_task: Optional[Dict] = None,
    max_steps: int = 15
) -> str:
```

Prompt content (`livebench/prompts/live_agent_prompt.py:157`, `livebench/prompts/live_agent_prompt.py:178`, `livebench/prompts/live_agent_prompt.py:199`, `livebench/prompts/live_agent_prompt.py:254`):
- Injects `balance`, `net_worth`, `total_token_cost`, `session_cost`, `daily_cost`, `survival_status` with emoji and status-specific guidance (`livebench/prompts/live_agent_prompt.py:35`, `livebench/prompts/live_agent_prompt.py:47`, `livebench/prompts/live_agent_prompt.py:133`).
- Work section shows full task prompt, task ID/sector/occupation/max payment, iteration budget with `submit_by_iteration = max(max_steps - 3, int(max_steps * 0.7))`, and reference-file plus sandbox paths (`livebench/prompts/live_agent_prompt.py:54`, `livebench/prompts/live_agent_prompt.py:76`, `livebench/prompts/live_agent_prompt.py:112`, `livebench/prompts/live_agent_prompt.py:115`).
- Daily workflow is fixed: skip `get_status`, call `decide_activity`, then `submit_work` or `learn`, then stop with no finish signal (`livebench/prompts/live_agent_prompt.py:254`, `livebench/prompts/live_agent_prompt.py:369`).
- `format_cost_update(session_cost, daily_cost, balance)` renders the `COST UPDATE` block injected per interaction (`livebench/prompts/live_agent_prompt.py:542`, `livebench/prompts/live_agent_prompt.py:554`).
- `get_work_task_prompt`, `get_learning_prompt`, and deprecated `get_trading_prompt` (returns trading-disabled string) are helpers kept for compatibility (`livebench/prompts/live_agent_prompt.py:407`, `livebench/prompts/live_agent_prompt.py:482`, `livebench/prompts/live_agent_prompt.py:492`).

## Message formatting and wrap-up recovery

- `format_tool_result_message(tool_name, tool_result, tool_args, activity_completed)` routes PDF/PPTX image dicts and single-image dicts to multimodal messages, else plain text (`livebench/agent/message_formatter.py:35`); PDF/PPTX images are base64-encoded as `image_url` content blocks (`livebench/agent/message_formatter.py:53`, `livebench/agent/message_formatter.py:77`).
- `format_result_for_logging` omits binary payloads and truncates long strings at 1000 chars (`livebench/agent/message_formatter.py:9`, `livebench/agent/message_formatter.py:30`).
- `WrapUpState` holds `date`, `task_id`, `task_prompt`, `sandbox_dir`, `conversation_history`, `available_artifacts`, `chosen_artifacts`, `downloaded_paths`, `submission_result`, `error`, `llm_decision` (`livebench/agent/wrapup_workflow.py:26`).
- Graph is `list_artifacts -> decide_submission -> (download_artifacts -> submit_work | END)` with conditional `_should_download` (`livebench/agent/wrapup_workflow.py:64`, `livebench/agent/wrapup_workflow.py:77`, `livebench/agent/wrapup_workflow.py:95`).
- Artifact scan covers `/tmp`, `/home/user`, `/home/user/artifacts` for office/doc/image extensions via `SessionSandbox.list_artifacts` (`livebench/agent/wrapup_workflow.py:118`, `livebench/agent/wrapup_workflow.py:122`, `livebench/agent/wrapup_workflow.py:127`).
- LLM picker returns a 1-indexed JSON array of artifact numbers, falling back to all artifacts on parse failure (`livebench/agent/wrapup_workflow.py:175`, `livebench/agent/wrapup_workflow.py:226`); downloads use `SessionSandbox.download_artifact` and submission calls `submit_work.invoke({"work_output": ..., "artifact_file_paths": ...})` (`livebench/agent/wrapup_workflow.py:250`, `livebench/agent/wrapup_workflow.py:284`, `livebench/agent/wrapup_workflow.py:302`).
- Factory verbatim (`livebench/agent/wrapup_workflow.py:431`):

```python
def create_wrapup_workflow(llm: Optional[ChatOpenAI] = None, logger=None, economic_tracker=None, is_openrouter: bool = False) -> WrapUpWorkflow:
```

**Covers:** component 02
