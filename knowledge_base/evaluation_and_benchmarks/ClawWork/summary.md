> [[index|Wiki]] | [[digest|Digest]]

# Technical Analysis: ClawWork

**Repository:** https://github.com/HKUDS/ClawWork @ 9c73ac0

---

## 1. Overview / What Problem It Solves

ClawWork turns an AI assistant into an economically accountable "AI coworker": it must complete real professional tasks drawn from the GDPVal dataset, pay for its own token/API usage out of a starting balance, and only earn income when an LLM judge scores its deliverable above a fixed threshold (`README.md:36-43`, `README.md:64`). The benchmark spans 220 GDPVal tasks across 44 occupations/sectors (`README.md:62`), and the same economic engine is repackaged three ways in this repo: a standalone `livebench/` daily-agent runtime, a `clawmode/` plugin that bolts the economy onto the `nanobot` chat harness, and an offline `scripts/` pipeline that prices tasks and validates the accounting. A React dashboard (live or statically exported) visualizes balances, earnings, and artifacts.

## 2. Architecture / Layering

```text
configs/default_config.json ──► livebench/main.py ──► LiveAgent (per signature)
                                                          │  ├─► EconomicTracker (balance, cost channels)
                                                          │  ├─► TaskManager / WorkEvaluator
                                                          │  └─► ChatOpenAI + direct tools + WrapUpWorkflow
api/server.py (FastAPI + WebSocket) ──reads jsonl──► frontend/ (React, live or static via VITE_STATIC_DATA)
scripts/*.py (offline) ──► task_hours.jsonl → task_values.jsonl → economic_real_value/ (validated by validate_economic_system.py)
clawmode/agent_loop.py (ClawWorkAgentLoop subclasses nanobot AgentLoop) ──► tools.py / artifact_tools.py / task_classifier.py / provider_wrapper.py
```

Four largely independent stacks share one accounting primitive, `EconomicTracker`, but are otherwise not layered on top of each other: (1) `livebench/` is the self-contained daily-simulation runtime; (2) `api/` + `frontend/` is a read-only observability layer over `livebench/`'s JSONL output; (3) `scripts/` is an offline batch pipeline that produces the pricing tables `livebench/` consumes and separately audits `EconomicTracker`'s behavior; (4) `clawmode/` is a parallel integration that re-implements the same economic loop as tools bolted onto a different host agent (`nanobot`) rather than reusing `livebench/agent/live_agent.py` directly. The `scheduler/` package (`scheduler/__init__.py:1`) is an empty placeholder — no code lives there; run cadence is entirely config-driven (`configs/default_config.json:3-6`).

## 3. Macro Components

| Component | Location | Responsibility | Key file:line |
|---|---|---|---|
| Live agent runtime | `livebench/agent/live_agent.py` | Per-signature daily loop: select task, run ≤15 tool iterations, submit, settle economics | `livebench/agent/live_agent.py:50`, `:546`, `:698` |
| Economic tracker | `livebench/agent/economic_tracker.py` | Deducts token/API costs live, gates pay at `min_evaluation_threshold=0.6`, computes survival status | `livebench/agent/economic_tracker.py:24`, `:158`, `:358`, `:524` |
| Wrap-up recovery | `livebench/agent/wrapup_workflow.py` | LangGraph fallback that scans sandbox artifacts and force-submits on iteration timeout | `livebench/agent/wrapup_workflow.py:41`, `:64` |
| ClawMode integration | `clawmode/agent_loop.py`, `tools.py`, `task_classifier.py`, `provider_wrapper.py` | Subclasses nanobot's `AgentLoop`, registers 6 economic/artifact tools, classifies `/clawwork` instructions into priced tasks | `agent_loop.py:46`, `tools.py:29`, `task_classifier.py:90` |
| API server | `api/server.py` | FastAPI REST + `/ws` WebSocket serving agent JSONL data to the frontend | `api/server.py:23`, `:713` |
| Scheduler (empty) | `scheduler/__init__.py` | Placeholder package, 0 lines | `scheduler/__init__.py:1` |
| Economics scripts | `scripts/estimate_task_hours.py`, `calculate_task_values.py`, `recalculate_agent_economics.py`, `validate_economic_system.py` | Offline hour estimation, BLS wage pricing, historical rescaling, tracker validation | `scripts/estimate_task_hours.py:23`, `scripts/calculate_task_values.py:26`, `scripts/recalculate_agent_economics.py:120`, `scripts/validate_economic_system.py:237` |
| Frontend dashboard | `frontend/src/` | React app (live or static via `VITE_STATIC_DATA`) rendering leaderboard, dashboard, work/learning/artifact views | `frontend/src/App.jsx:14`, `frontend/src/api.js:9` |

## 4. Data Flow

A run starts from `livebench/main.py:49`, which reads `configs/default_config.json`, builds one `LiveAgent` per enabled signature (`livebench/main.py:161`), and iterates weekdays (`livebench/agent/live_agent.py:993`). Each day, `run_daily_session` (`livebench/agent/live_agent.py:546`) selects a task, calls `economic_tracker.start_task` (`:596`), builds a cost-aware system prompt (`livebench/prompts/live_agent_prompt.py:12`), and runs up to 15 tool-calling iterations (`:698`) where every LLM call and paid tool call is deducted live via `EconomicTracker.track_tokens`/`track_api_call` (`economic_tracker.py:158`, `:203`). `submit_work` triggers `WorkEvaluator` scoring and `add_work_income`, which pays $0 below the 0.6 threshold and the full `quality_score × estimated_hours × BLS_wage` amount at or above it (`economic_tracker.py:358`, `README.md:276-278`). Results land in per-agent `balance.jsonl` / `token_costs.jsonl` / `task_completions.jsonl` (`economic_tracker.py:52`), which `api/server.py:311` merges with `tasks.jsonl` and `evaluations.jsonl` for the REST/WebSocket layer, or which `scripts/generate_static_data.py:424` flattens into `frontend/public/data/*.json` for the static build. The `clawmode/` path runs a structurally identical cost-then-pay cycle per chat message instead of per simulated day (`agent_loop.py:108-135`).

## 5. Economic Model

Payment formula: `quality_score × (estimated_hours × BLS_hourly_wage)` (`README.md:276-278`), with hours and wages pre-computed offline by `scripts/estimate_task_hours.py` (GPT-5.2 estimation, `MODEL = "gpt-5.2"` at line 23) and `scripts/calculate_task_values.py` (BLS occupation matching, `:142`). Task values quoted range $82.78–$5,004.00, average $259.45 across 220 tasks (`README.md:280-285`). Costs are metered per call: token cost `(input/1e6 × input_price) + (output/1e6 × output_price)` (`economic_tracker.py:108-111`), plus flat/per-token charges for search (Tavily $0.0008/call) and OCR (Jina $0.05/1M tokens) (`README.md:338-342`). Payment gating is a hard cliff at `min_evaluation_threshold=0.6` — verified across nine boundary score cases in `scripts/validate_economic_system.py:322-332` — not a proportional payout. `recalculate_agent_economics.py:120` retroactively rescales historical flat-$50 payments to real task values with `new_payment = old_payment × (real_task_value / 50)`, preserving the pass/fail pattern rather than recomputing evaluation outcomes.

## 6. Tool Surface

`livebench/` agents get direct-bound LangChain tools plus `decide_activity`/`submit_work` (`README.md:375-376`). `clawmode/` registers six tools on top of nanobot's built-ins, sharing one `ClawWorkState` dataclass (`tools.py:29`): `decide_activity` (enum `work`/`learn`, `tools.py:48`), `submit_work` (`tools.py:112`), `learn` (200-char minimum knowledge entry, `tools.py:252`), `get_status` (`tools.py:326`), `create_artifact` (writes txt/md/csv/json/xlsx/docx/pdf, `artifact_tools.py:26`), and conditionally `read_artifact` (multimodal PDF or OCR fallback, `artifact_tools.py:181`). `TaskClassifier` (`task_classifier.py:90`) turns a free-form `/clawwork <instruction>` into a priced synthetic task by prompting the host LLM (temperature 0.3, 256 max tokens) for an occupation + hour estimate, clamped to 0.25–40h (`task_classifier.py:133`).

## 7. Eval Story

Work quality is judged entirely by a single LLM (GPT-5.2), scored 0–10 against per-occupation rubrics generated by `eval/generate_meta_prompts.py` (`:26-29`, `:80-81`) and weighted completeness 40% / correctness 30% / quality 20% / domain standards 10% (`:123-147`). There is no human-in-the-loop scoring and no held-out reference answer comparison visible in this clone — the rubric is itself LLM-generated per occupation, not hand-authored. Missing/incomplete deliverables are contractually forced to 0-2 (`generate_meta_prompts.py:80-81`), and the 0-10 score is mapped to a binary pay/no-pay outcome at 0.6 (normalized) with no partial-credit payout (`economic_tracker.py:358`).

## 8. Error Handling

Error handling favors graceful degradation over hard failure: `_ainvoke_with_retry` retries LLM calls with linear backoff (`live_agent.py:393`, `:467`); a text-only turn without a tool call gets a forced nudge toward `execute_code_sandbox` then `submit_work` rather than looping forever (`live_agent.py:812`); provider failures return an `"API_ERROR"` sentinel string rather than raising (`live_agent.py:951`); `WrapUpWorkflow` is the safety net for iteration-limit timeouts — it lists sandbox artifacts, asks the LLM to pick deliverables, and force-submits them so a day never ends with zero output (`wrapup_workflow.py:64-95`). Occupation/task classification similarly degrades to fixed fallbacks (`_FALLBACK_OCCUPATION`, `_FALLBACK_WAGE = 64.0`, `task_classifier.py:18`) rather than erroring. `generate_static_data.py`'s `read_jsonl` silently tolerates missing files and malformed lines (`:36-48`).

## 9. Testing

No `_test.py`/`test_*.py` unit-test files are referenced anywhere across the six extracted wiki pages; the closest thing to a test suite is `scripts/validate_economic_system.py`, which is a demo-plus-assertions script run from `__main__` (`:588`, `:597`) rather than a pytest suite — it builds a temp-dir `EconomicTracker`, runs three scripted tasks, and asserts six required tracker methods exist, nine score/threshold boundary cases pay correctly, and cost-channel totals reconcile within `1e-6` (`:237`, `:322`, `:425`). This is manual-run correctness auditing of one module (the economic core), not automated regression coverage of `livebench/`, `clawmode/`, `api/`, or `frontend/`.

## 10. How to Extend

Add an agent: append a signature to `configs/default_config.json`'s `agents` list (`configs/default_config.json:198-205`) or `livebench/configs/`. Add a tool to the `clawmode/` integration: subclass nanobot's `Tool` ABC and register it in `ClawWorkAgentLoop._register_default_tools` (`agent_loop.py:76-59`), taking the shared `ClawWorkState`. Re-price tasks: rerun the `scripts/` pipeline (`estimate_task_hours.py` → `calculate_task_values.py`) and point `task_values_path` at the new output. Add a dashboard view: add a `gen_*` function to `generate_static_data.py` mirroring an `api/server.py` endpoint, then a matching React page reading via `frontend/src/api.js`'s `staticUrl`/`liveUrl` split. The `scheduler/` package is the obvious empty extension point for anyone wanting cron-style multi-run orchestration instead of the current single-invocation `main.py` date-range loop.

## 11. Verdict

ClawWork is a coherent, narrowly-scoped economic-accountability benchmark layered three different ways (standalone runtime, chat-plugin, dashboard) over one shared accounting primitive (`EconomicTracker`) and one shared pay cliff (0.6 quality threshold). Its central design choice — binary pay/no-pay gated on a single LLM judge's rubric score, applied to dollar values themselves estimated by an LLM (hours) and matched by an LLM (BLS occupation) — means the "economic value" numbers are model-estimated end to end, not independently priced; see `critical_thinking.md` for how far that stretches the claim of a "real economic value" benchmark. Engineering quality is uneven: the core economic loop has an actual validation script and a documented backward-compatibility contract (`validate_economic_system.py:568-575`), but there is no automated test suite for the agent runtime, chat integration, API, or frontend, and the `scheduler/` package is entirely unimplemented.
