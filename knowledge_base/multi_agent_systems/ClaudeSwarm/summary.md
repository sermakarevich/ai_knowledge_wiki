# Technical Analysis: claude-swarm

**Repository:** https://github.com/affaan-m/claude-swarm
**Version analyzed:** 0.2.0
**Date:** 2026-05-03

---

## 1. Overview / What Problem It Solves

Complex software engineering tasks — refactoring a module, adding authentication, building an API — are typically too large for a single Claude Code agent to complete in one turn without losing context or making conflicting decisions. A human developer would decompose such a task mentally, then execute parts in parallel. Claude Swarm automates that decomposition and parallelism: a user describes a high-level goal, and the tool produces a dependency-graph of subtasks, runs them as independent Claude Code subprocesses concurrently, and synthesizes the results.

The primary user is a developer who wants to delegate a multi-step coding task to an automated agent team rather than orchestrate it manually. Secondary users include hackathon judges and presenters — the `--demo` flag simulates an entire swarm run with animated terminal output and no API key required.

The tool was built for the Cerebral Valley x Anthropic Claude Code Hackathon (February 2026) and is openly positioned as a demonstration of strategic model selection: Opus 4.6 handles the reasoning-heavy tasks (decomposition and quality review) while Haiku handles the repetitive execution tasks, targeting a cost/capability tradeoff.

---

## 2. High-Level Architecture

```
 User CLI invocation
        │
        ▼
 ┌─────────────────┐
 │   cli.py:main   │  Click group, resolves config, wires phases
 └────────┬────────┘
          │
  Phase 1 ▼
 ┌─────────────────────────┐
 │  decomposer.py          │  Opus 4.6 via claude-agent-sdk
 │  decompose_task()       │  Produces SwarmPlan (dependency DAG)
 └────────┬────────────────┘
          │ SwarmPlan
  Phase 2 ▼
 ┌─────────────────────────┐     ┌──────────────────┐
 │  orchestrator.py        │────►│  ui.py           │
 │  SwarmOrchestrator.run()│     │  Rich Live panel │
 │  anyio task group       │     └──────────────────┘
 │  Haiku agents (parallel)│     ┌──────────────────┐
 │  file locks, budget     │────►│  session.py      │
 └────────┬────────────────┘     │  JSONL recorder  │
          │ SwarmResult          └──────────────────┘
  Phase 2.5 ▼
 ┌─────────────────────────┐
 │  quality_gate.py        │  Opus 4.6, reads task text outputs
 │  run_quality_gate()     │  Returns QualityReport
 └────────┬────────────────┘
          │
  Phase 3 ▼
 ┌─────────────────────────┐
 │  ui.py                  │  Prints result table + quality report
 │  session.py             │  Writes metadata.json + events.jsonl
 └─────────────────────────┘
```

**Data flow for a `claude-swarm "Refactor auth"` invocation:**

1. `cli.py:_run_swarm()` resolves the working directory, loads any `swarm.yaml`, and initializes `SessionRecorder`.
2. `decomposer.py:decompose_task()` sends a structured system prompt + user task to Opus 4.6 via `claude_agent_sdk.query()`. Opus explores the codebase (up to 3 turns) and returns a JSON block listing tasks with `id`, `dependencies`, `files_to_modify`, and `prompt`.
3. `orchestrator.py:SwarmOrchestrator.run()` opens an `anyio` task group. Each iteration of the scheduling loop calls `_get_ready_tasks()` (tasks whose dependencies are all in `completed_task_ids`) and spawns `_run_agent()` coroutines up to `max_concurrent`.
4. Each `_run_agent()` call creates a `ClaudeAgentOptions(model="haiku", permission_mode="acceptEdits")` and streams messages from `claude_agent_sdk.query()`. Tool use events update `SwarmAgent.current_tool` and trigger dashboard refresh via `on_update` callback.
5. After all agents complete, `quality_gate.py:run_quality_gate()` sends task summaries (text output, file lists, costs) to Opus 4.6 for a structured JSON review.
6. `session.py:SessionRecorder.finish()` writes `~/.claude-swarm/sessions/<id>/metadata.json` and `events.jsonl`.

**Persistent state** lives in `~/.claude-swarm/sessions/` as JSONL event logs and JSON metadata files. No database is used; there is no in-process shared state across sessions.

---

## 3. The SwarmPlan and Task Graph

The central domain abstraction is a directed acyclic graph of `SwarmTask` nodes encoded in a `SwarmPlan`. Each `SwarmTask` carries: a string `id`, a natural-language `description`, an `agent_type` label, a `dependencies: list[str]` of task IDs, a `files_to_modify: list[str]` for conflict detection, and a `prompt: str` that is sent verbatim to the worker agent.

**Core types in `types.py`:**

| Type | Kind | Purpose |
|------|------|---------|
| `TaskStatus` | `StrEnum` | `pending \| blocked \| running \| completed \| failed \| cancelled` |
| `AgentStatus` | `StrEnum` | `idle \| working \| blocked \| completed \| failed` |
| `SwarmTask` | `@dataclass` | One node in the dependency DAG |
| `SwarmAgent` | `@dataclass` | Runtime state of a running subprocess |
| `FileConflict` | `@dataclass` | Detected collision between two tasks on the same file |
| `SwarmPlan` | `@dataclass` | Full DAG: `original_prompt`, `tasks: list[SwarmTask]` |
| `SwarmResult` | `@dataclass` | Terminal output: completed/failed tasks, conflicts, cost |

The topological ordering is computed in `types.py:SwarmPlan.parallel_groups` using a manual Kahn's-algorithm-style loop — not NetworkX (see §10). Tasks are grouped into "waves" of tasks that share no inter-wave dependencies, enabling the orchestrator to launch each wave in parallel:

```python
# types.py:83-100
remaining = {t.id: set(t.dependencies) for t in self.tasks}
groups: list[list[str]] = []
while remaining:
    ready = [tid for tid, deps in remaining.items() if len(deps) == 0]
    if not ready:
        ready = list(remaining.keys())[:1]  # cycle escape hatch
    groups.append(ready)
    for tid in ready:
        del remaining[tid]
    for deps in remaining.values():
        deps -= set(ready)
```

The orchestrator does not use `parallel_groups` directly — it uses `_get_ready_tasks()` in a polling loop instead, which re-evaluates dependency satisfaction after every agent completion. `parallel_groups` is only used by `ui.py:SwarmUI.print_plan()` to display the planned execution waves to the user before execution begins.

---

## 4. LLM / External Service Integration

Claude Swarm calls the Claude API for three purposes, all mediated through the `claude_agent_sdk` package (required, `>=0.1.35`):

| Call site | File | Model | Turns | Purpose |
|-----------|------|-------|-------|---------|
| `decompose_task()` | `decomposer.py:42-73` | `opus` (configurable) | 3 | Codebase exploration + task decomposition |
| `_run_agent()` | `orchestrator.py:152-177` | `haiku` (hardcoded) | 20 max | Execute a single coding subtask |
| `run_quality_gate()` | `quality_gate.py:85-107` | `opus` (configurable) | 2 | Review combined agent outputs |

All three calls use `claude_agent_sdk.query()` with `ClaudeAgentOptions`. The SDK abstracts the actual Claude Code subprocess invocation; the tool does not call the Anthropic HTTP API directly.

The `ANTHROPIC_API_KEY` environment variable is required for all three (checked in `cli.py:75`). No other external services are used. The `--demo` flag bypasses all API calls entirely via `demo.py:run_demo()`.

**Cost control mechanisms:**
- `max_budget_usd=0.50` per worker agent (hardcoded in `orchestrator.py:162`)
- `max_budget_usd` total swarm budget enforced in `SwarmOrchestrator.run()` (default $5.00, configurable via `--budget`)
- Quality gate cost is added to `result.total_cost_usd` after the fact (`cli.py:240`)

---

## 5. The Swarm Execution Pipeline

**Phase 1: Decomposition** (`decomposer.py`)

`decompose_task()` (line 35) constructs `ClaudeAgentOptions(model=model, cwd=cwd, permission_mode="default", max_turns=3)` and passes `DECOMPOSE_SYSTEM_PROMPT` (a strict JSON schema instruction) plus the user task. Opus explores the codebase tree using its available tools, then emits a JSON block. `_parse_decomposition()` (line 77) extracts the JSON via `_extract_json_block()` and constructs a `list[SwarmTask]`. On JSON parse failure, it falls back to a single monolithic task.

**Phase 2: Parallel Execution** (`orchestrator.py`)

`SwarmOrchestrator.run()` (line 72) opens an `anyio.create_task_group()` and enters a scheduling loop with a 500ms sleep between iterations. Each iteration:
1. Checks budget: if `total_cost >= max_budget_usd`, calls `_cancel_pending_tasks()` and waits for running agents to finish.
2. Calls `_get_ready_tasks()` (line 218): returns tasks in PENDING state with all dependency IDs in `completed_task_ids`.
3. For each ready task (up to `max_concurrent` active agents), calls `_check_file_conflict()` (line 234): if a file in `task.files_to_modify` is locked by another working agent, the task is set to BLOCKED. Otherwise, `_lock_files()` is called and `_run_agent()` is spawned in the task group.

`_run_agent()` (line 104) creates a `SwarmAgent` record, streams from `query()`, accumulates `TextBlock` text and fires `on_update` on each `ToolUseBlock`. On completion, it calls `_unlock_files()` (line 213) and `_update_blocked_tasks()` (line 219) to unblock tasks waiting on the now-completed task.

**Retry logic** (`orchestrator.py:190-202`): on exception, if `attempt < max_retries`, the task status is reset to PENDING and the agent is marked FAILED. On the next scheduling loop iteration, the task becomes eligible again.

**Phase 2.5: Quality Gate** (`quality_gate.py`)

`run_quality_gate()` (line 68) calls `_build_task_summaries()` (line 114) which formats each task's text output (truncated to 2000 chars), agent type, files, and cost into a structured string. This is embedded in `QUALITY_GATE_PROMPT` and sent to Opus with `max_turns=2`. `_parse_quality_report()` (line 144) extracts a JSON object containing `overall_score`, `verdict`, `task_reviews[]`, `integration_issues[]`, and `missing_items[]`.

**Phase 3: Session Recording** (`session.py`)

`SessionRecorder` accumulates `SessionEvent` objects throughout execution. `finish()` (line 103) writes two files:
- `~/.claude-swarm/sessions/<id>/metadata.json` — prompt, plan, config, result statistics
- `~/.claude-swarm/sessions/<id>/events.jsonl` — one JSON object per line, streamed by `replay`

---

## 6. Key Files

| File | Lines | What It Does |
|------|-------|--------------|
| `src/claude_swarm/cli.py` | 350 | Click command group; wires all phases; `_run_swarm()` async entry point; `sessions` and `replay` subcommands |
| `src/claude_swarm/orchestrator.py` | 328 | `SwarmOrchestrator`: anyio scheduling loop, file locking, budget enforcement, retry logic, agent hooks |
| `src/claude_swarm/ui.py` | 287 | `SwarmUI`: Rich Live dashboard (tasks panel + agents panel), plan printer, quality report printer, results table |
| `src/claude_swarm/demo.py` | 262 | Animated demo simulation with hardcoded scenarios; uses `SwarmUI` and `SwarmPlan` directly; no API calls |
| `src/claude_swarm/quality_gate.py` | 218 | Opus quality review: prompt construction, JSON parse, `QualityReport` dataclass |
| `src/claude_swarm/session.py` | 207 | JSONL event recorder; `list_sessions()` and `load_session_events()` for replay |
| `src/claude_swarm/decomposer.py` | 179 | Opus task decomposer; `DECOMPOSE_SYSTEM_PROMPT`, JSON extraction, `SwarmTask` construction |
| `src/claude_swarm/config.py` | 166 | YAML swarm topology config; `SwarmConfig`, `AgentConfig`, `ConnectionConfig`; `find_config()` auto-detection |
| `src/claude_swarm/types.py` | 134 | All core dataclasses: `SwarmTask`, `SwarmPlan`, `SwarmAgent`, `FileConflict`, `SwarmResult`; topological sort |
| `src/claude_swarm/__init__.py` | 3 | Package version (`__version__ = "0.2.0"`) |
| `examples/swarm.yaml` | ~60 | Reference YAML topology with coder/security-reviewer/tester/reviewer agents and connection graph |

---

## 7. Dependencies

| Package | Version constraint | Purpose |
|---------|--------------------|---------|
| `claude-agent-sdk` | `>=0.1.35` | Claude Code subprocess control; `query()`, `ClaudeAgentOptions`, message types |
| `rich` | `>=13.0.0` | Terminal UI: `Live`, `Layout`, `Panel`, `Table`, `Console` |
| `anyio` | `>=4.0` | Structured async concurrency; `create_task_group()` for parallel agents |
| `click` | `>=8.0` | CLI framework; `@click.group`, `@click.command`, option parsing |
| `networkx` | `>=3.0` | Listed as required; **not imported in any source file** (see §10) |
| `textual` | `>=1.0.0` | Listed as required; **not imported in any source file** (see §10) |
| `pydantic` | `>=2.0` | Listed as required; **not imported in any source file** (see §10) |

**Dev extras:**

| Package | Version constraint | Purpose |
|---------|--------------------|---------|
| `pytest` | `>=8.0` | Test runner |
| `pytest-anyio` | `>=0.0.0` | Async test support |
| `ruff` | `>=0.8.0` | Linter |
| `mypy` | `>=1.0` | Static type checker |

**Missing from manifest:**

| Package | Where needed |
|---------|-------------|
| `pyyaml` | `config.py:36` — imported as `yaml` with try/except; not in `pyproject.toml` |

---

## 8. CLI / Usage Surface

**Entry point** (declared in `pyproject.toml:31-32`):
```
claude-swarm = "claude_swarm.cli:main"
```

**Commands:**

```bash
# Run a swarm
claude-swarm [OPTIONS] TASK

Options:
  -d, --cwd TEXT            Working directory (default: .)
  -n, --max-agents INTEGER  Max concurrent agents (default: 4)
  -m, --model TEXT          Decomposition model (default: opus)
  -b, --budget FLOAT        Max budget USD (default: 5.0)
  -r, --retry INTEGER       Max retries per failed task (default: 1)
  -c, --config PATH         Path to swarm.yaml
  --demo                    Animated demo, no API key needed
  --dry-run                 Show plan, skip execution
  --quality-gate/--no-quality-gate  Toggle Opus review (default: on)
  --no-ui                   Disable Rich Live dashboard
  -v, --version             Print version

# List past sessions
claude-swarm sessions [--limit N]

# Replay a session's event log
claude-swarm replay <session-id>
```

**Environment variables:**

| Variable | Default | Purpose |
|----------|---------|---------|
| `ANTHROPIC_API_KEY` | (required) | Anthropic API key; validated at startup |

**Configuration files:**

| Path | Purpose |
|------|---------|
| `<cwd>/swarm.yaml` | Custom agent topology; overrides max_concurrent, budget, model |
| `<cwd>/swarm.yml` | Same, alternative extension |
| `<cwd>/.claude/swarm.yaml` | Same, project-local Claude config location |
| `<cwd>/.claude/swarm.yml` | Same, alternative extension |
| `~/.claude-swarm/sessions/` | Session storage directory (auto-created) |

---

## 9. Extensibility Points

- **New agent types in YAML config:** Define a new key under `agents:` in `swarm.yaml` with `description`, `model`, `tools`, and `prompt`. The orchestrator's `_run_agent()` uses `task.tools` and `task.prompt` directly from the decomposed `SwarmTask`; YAML agent definitions are used by `config.py:SwarmConfig.get_agent_prompt/tools/model()` and would need to be wired into the decomposer prompt or a custom `SwarmPlan` builder.

- **New decomposition strategy:** Replace or wrap `decomposer.py:decompose_task()`. The function's contract is `(prompt: str, cwd: str, model: str) -> SwarmPlan`. Any alternative decomposer (e.g., static analysis-based, or using a different model) that returns a valid `SwarmPlan` can be substituted at the call site in `cli.py:_run_swarm()`.

- **Custom quality gate:** Replace `quality_gate.py:run_quality_gate()`. Its contract is `(result: SwarmResult, cwd: str, model: str) -> QualityReport`. The `QualityReport` dataclass fields (`overall_score`, `verdict`, `summary`, `task_reviews`, `integration_issues`, `missing_items`) are consumed only by `ui.py:print_quality_report()` and the session recorder.

- **Agent event hooks:** `SwarmOrchestrator.__init__` accepts `on_agent_event: Callable[[str, str, Any], None]` for external event consumption (e.g., sending to a webhook, external monitoring). The signature is `(agent_id, event_type, data)`. Add custom logic without touching the orchestrator core.

- **New session storage backend:** `session.py:SessionRecorder` writes to `~/.claude-swarm/sessions/`. To change the backend (e.g., SQLite, S3), subclass `SessionRecorder` and override `start()`, `_record_event()`, and `finish()`. The orchestrator only calls the public methods (`start`, `record_*`, `finish`) via the `recorder: SessionRecorder | None` parameter.

---

## 10. Limitations and Gotchas

- **Three unused required dependencies:** `pyproject.toml` lists `textual>=1.0.0`, `networkx>=3.0`, and `pydantic>=2.0` as required dependencies. None of these are imported anywhere in the source. `textual` was likely replaced by `rich`; `networkx` was likely replaced by the manual topological sort in `types.py:SwarmPlan.parallel_groups`; `pydantic` was likely replaced by dataclasses. Users pay install size and version-conflict cost for dead packages.

- **`pyyaml` not in dependencies:** `config.py` handles the missing `yaml` import gracefully with `HAS_YAML = True/False`, but `pyyaml` is absent from `pyproject.toml`. A user who installs `claude-swarm` and uses `--config swarm.yaml` gets an `ImportError` at runtime rather than an install-time resolution.

- **File conflict detection is declaration-based, not actual:** `_check_file_conflict()` (`orchestrator.py:234`) checks `task.files_to_modify`, which comes from the Opus decomposition — a prediction, not a guarantee. An agent editing a file it did not declare goes undetected. This is a fundamental limitation of pessimistic locking based on LLM-declared intent.

- **Budget enforcement does not stop running agents:** `_cancel_pending_tasks()` (`orchestrator.py:265`) only cancels PENDING and BLOCKED tasks. Agents already spawned when the budget is hit continue running and accumulate cost until they complete or fail. The actual overrun can be up to `n_running_agents × 0.50` above the declared budget limit.

- **Quality gate cannot read modified files:** `run_quality_gate()` sets `permission_mode="default"` and `max_turns=2`. The quality gate agent has no tools to read the actual modified source files; it only sees the text output that worker agents printed to stdout. Code changes that succeeded silently are reviewed blind.

- **`on_update` is set as an attribute post-construction in `cli.py`:** `cli.py:_run_swarm()` (line 219) sets `orchestrator.on_update = update_dashboard` after constructing the orchestrator with the default no-op lambda. This overrides the constructor parameter, which works but bypasses the public constructor interface and makes the update callback invisible from the constructor signature.

- **`parallel_groups` property is not used by the orchestrator:** `SwarmPlan.parallel_groups` (`types.py:78`) is only called by `ui.py:print_plan()` for display. The orchestrator's actual scheduling in `_get_ready_tasks()` re-evaluates dependency satisfaction dynamically. The two mechanisms can produce different execution orderings in practice.

- **Demo mode bypasses `swarm.yaml`:** `cli.py:69-72` returns early if `--demo` is set, before config loading. A user with a `swarm.yaml` in their project root who invokes `--demo` will not see their config applied — they always get the hardcoded `demo.py` scenarios.

---

## 11. How It Compares to Alternatives

**crewAI** defines role-based agents with built-in memory and backstory, using an agent-task assignment model. Claude Swarm differs by grounding task decomposition in actual codebase exploration (Opus reads the project tree), using Claude Code's native tool set (Read, Write, Edit, Bash), and targeting terminal UX rather than a Python-embedded orchestration API. crewAI is more portable across LLM providers; Claude Swarm is tightly coupled to Anthropic's SDK.

**Microsoft AutoGen** provides a multi-agent conversational framework with configurable human-in-the-loop interrupts and built-in group-chat patterns. It handles general task types and is model-agnostic. Claude Swarm is narrower in scope (coding only, Claude only) but requires no agent "conversation" scaffolding — the dependency graph structure replaces turn-based dialogue as the coordination mechanism.

**OpenAI Swarm** (lightweight reference implementation) demonstrates agent handoff patterns where a "triage" agent routes to specialist agents. It is intentionally minimal with no built-in scheduling or parallel execution. Claude Swarm adds dependency-aware parallel execution, budget enforcement, file conflict detection, and a full session-replay system on top of a similar routing concept.

**LangGraph** provides stateful DAG-based agent workflows with checkpointing, streaming, and human-in-loop support. It handles complex long-running workflows but requires significant graph definition code. Claude Swarm generates the DAG dynamically from a natural-language task description, trading explicit control for ease of invocation — the user writes a sentence, not a graph definition.

Claude Swarm's positioning: the lowest-friction entry point for running parallelized Claude Code agents on a codebase, with session replay and live terminal visibility, at the cost of being Anthropic-SDK-exclusive and lacking persistence/checkpointing.

---

## Appendix: Selected Code Snippets

**`SwarmPlan.parallel_groups` — manual topological sort for execution wave planning**
(`src/claude_swarm/types.py:78-100`)

```python
@property
def parallel_groups(self) -> list[list[str]]:
    """Group tasks by dependency level for parallel execution."""
    # Tasks with no dependencies can run first
    remaining = {t.id: set(t.dependencies) for t in self.tasks}
    groups: list[list[str]] = []

    while remaining:
        # Find all tasks whose dependencies are satisfied
        ready = [tid for tid, deps in remaining.items() if len(deps) == 0]
        if not ready:
            # Circular dependency — shouldn't happen with good decomposition
            ready = list(remaining.keys())[:1]
        groups.append(ready)
        for tid in ready:
            del remaining[tid]
        # Remove completed tasks from dependency lists
        for deps in remaining.values():
            deps -= set(ready)

    return groups
```

**`SwarmOrchestrator.run` — anyio scheduling loop with budget enforcement**
(`src/claude_swarm/orchestrator.py:72-117`)

```python
async def run(self) -> SwarmResult:
    self.start_time = time.monotonic()

    async with anyio.create_task_group() as tg:
        while not self._all_done():
            if self.total_cost >= self.max_budget_usd and not self._budget_exceeded:
                self._budget_exceeded = True
                self._cancel_pending_tasks(
                    reason=(
                        f"Budget exceeded: ${self.total_cost:.4f}"
                        f" >= ${self.max_budget_usd:.2f}"
                    )
                )
                self.on_update()
                if self.active_agent_count == 0:
                    break
                await anyio.sleep(0.5)
                continue

            ready_tasks = self._get_ready_tasks()

            for task in ready_tasks:
                if self.active_agent_count >= self.max_concurrent:
                    break
                conflict = self._check_file_conflict(task)
                if conflict:
                    self.conflicts.append(conflict)
                    task.status = TaskStatus.BLOCKED
                    self.on_update()
                    continue

                task.status = TaskStatus.RUNNING
                self._lock_files(task)
                tg.start_soon(self._run_agent, task)
                self.on_update()

            await anyio.sleep(0.5)

    elapsed = int((time.monotonic() - self.start_time) * 1000)
    return SwarmResult(...)
```

**`decompose_task` — Opus 4.6 invocation with 3-turn codebase exploration**
(`src/claude_swarm/decomposer.py:35-73`)

```python
async def decompose_task(
    prompt: str,
    cwd: str,
    model: str = "opus",
) -> SwarmPlan:
    options = ClaudeAgentOptions(
        model=model,
        cwd=cwd,
        permission_mode="default",
        max_turns=3,
    )

    decompose_prompt = f"""{DECOMPOSE_SYSTEM_PROMPT}

PROJECT DIRECTORY: {cwd}

TASK TO DECOMPOSE:
{prompt}

First, explore the codebase to understand the structure. \
Then output your decomposition as a JSON code block.
"""

    collected_text = ""
    total_cost = 0.0

    async for message in query(prompt=decompose_prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    collected_text += block.text
        elif isinstance(message, ResultMessage):
            total_cost = message.total_cost_usd or 0.0

    tasks = _parse_decomposition(collected_text)

    return SwarmPlan(
        original_prompt=prompt,
        tasks=tasks,
        estimated_total_cost=total_cost * len(tasks),
        model_used=model,
    )
```

**`SwarmConfig.from_dict` — declarative YAML topology parsing**
(`src/claude_swarm/config.py:86-122`)

```python
@classmethod
def from_dict(cls, data: dict[str, Any]) -> SwarmConfig:
    swarm_data = data.get("swarm", {})
    config = cls(
        name=swarm_data.get("name", "default"),
        max_concurrent=swarm_data.get("max_concurrent", 4),
        budget_usd=swarm_data.get("budget_usd", 5.0),
        model=swarm_data.get("model", "opus"),
    )

    for name, agent_data in data.get("agents", {}).items():
        config.agents[name] = AgentConfig(
            name=name,
            description=agent_data.get("description", f"Agent: {name}"),
            model=agent_data.get("model", "haiku"),
            tools=agent_data.get("tools", ["Read", "Write", "Edit", "Bash", "Grep", "Glob"]),
            prompt=agent_data.get("prompt", ""),
        )

    for conn_data in data.get("connections", []):
        from_val = conn_data.get("from", [])
        if isinstance(from_val, str):
            from_val = [from_val]
        config.connections.append(
            ConnectionConfig(
                from_agents=from_val,
                to_agent=conn_data.get("to", ""),
            )
        )

    return config
```
