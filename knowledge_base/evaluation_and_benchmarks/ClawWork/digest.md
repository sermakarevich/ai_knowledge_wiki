> [[index|Wiki]] | [[summary|Summary]]

# ClawWork — Digest

The whole source at medium depth: every chapter's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-concept-economics|Concept: AI-coworker economic benchmark]]

**In one sentence:** ClawWork turns an AI assistant into an economically accountable AI coworker that must earn real income from professional tasks while paying its own token costs from a $10 starting balance.

- ClawWork frames assistants as coworkers that "complete real work tasks and create genuine economic value" (`/tmp/clawwork/README.md:36-37`).
- Agents do professional work from the GDPVal dataset, "pay for their own token usage, and maintain economic solvency" (`/tmp/clawwork/README.md:39-40`).
- The benchmark runs 220 GDPVal tasks spanning 44 occupations/economic sectors (`/tmp/clawwork/README.md:62-62`).
- Each agent starts with just $10 and "pay[s] for every token generated" so waste can wipe the balance (`/tmp/clawwork/README.md:64-64`).
- Payment follows real economic value as `quality_score × (estimated_hours × BLS_hourly_wage)` (`/tmp/clawwork/README.md:276-278`).
- Work quality is scored by an LLM judge (GPT-5.2) with "category-specific rubrics for each of the 44 GDPVal sectors" (`/tmp/clawwork/README.md:76-76`).
- The end-to-end loop is Task Assignment → Execution → Artifact Creation → LLM Evaluation → Payment (`/tmp/clawwork/README.md:72-72`).

## 2. [[wiki/02-agent-runtime|Live agent runtime and economic tracking]]

**In one sentence:** The live agent runtime runs one `LiveAgent` per configured signature over weekdays in a date range, charging every LLM and API call against a dollar balance via `EconomicTracker` and paying work income only when the evaluation score clears 0.6.

- Entry point `main.py` loads `config["livebench"]`, resolves dates, pricing, task source, and enabled agents, then constructs one `LiveAgent` per agent and runs it (`livebench/main.py:49`, `livebench/main.py:116`, `livebench/main.py:161`).
- `LiveAgent` owns `EconomicTracker`, `TaskManager`, `WorkEvaluator`, direct tools, and a tool-bound `ChatOpenAI` model, with per-day state (`current_date`, `current_task`, `daily_activity`) (`livebench/agent/live_agent.py:50`, `livebench/agent/live_agent.py:131`, `livebench/agent/live_agent.py:687`).
- The daily loop `run_daily_session(date)` selects one task, starts cost tracking, builds the economic system prompt, runs up to 15 tool-calling iterations, then saves end-of-day state (`livebench/agent/live_agent.py:546`, `livebench/agent/live_agent.py:584`, `livebench/agent/live_agent.py:698`, `livebench/agent/live_agent.py:924`).
- `EconomicTracker` deducts token/API costs in real time, writes `balance.jsonl` / `token_costs.jsonl` / `task_completions.jsonl`, and gates pay on `min_evaluation_threshold=0.6` (`livebench/agent/economic_tracker.py:52`, `livebench/agent/economic_tracker.py:158`, `livebench/agent/economic_tracker.py:358`).
- Survival status is derived from balance: bankrupt `<= 0`, struggling `< 100`, stable `< 500`, else thriving (`livebench/agent/economic_tracker.py:524`).
- The system prompt injects balance, token-cost warnings, work-vs-learn choice, and the full work task plus reference-file paths (`livebench/prompts/live_agent_prompt.py:12`, `livebench/prompts/live_agent_prompt.py:115`, `livebench/prompts/live_agent_prompt.py:157`).
- On iteration-limit timeout without submission, a LangGraph `WrapUpWorkflow` lists sandbox artifacts, asks the LLM to pick deliverables, downloads, and submits them (`livebench/agent/wrapup_workflow.py:41`, `livebench/agent/wrapup_workflow.py:64`, `livebench/agent/live_agent.py:849`).

## 3. [[wiki/03-clawmode-tools|ClawMode integration: loop, tools, classifier]]

**In one sentence:** ClawMode glues ClawWork's economic engine onto nanobot by subclassing `AgentLoop` to intercept `/clawwork` commands, registering six economic/artifact tools, classifying free-form instructions into paid occupation tasks, and tracking every LLM call's token cost.

- `ClawWorkAgentLoop` subclasses nanobot's `AgentLoop` and wraps every message with `start_task` / `end_task` plus a cost footer (`agent_loop.py:46`, `agent_loop.py:91`, `agent_loop.py:254`).
- Six tools are registered on top of nanobot's built-ins: `decide_activity`, `submit_work`, `learn`, `get_status`, `create_artifact`, and conditionally `read_artifact` (`agent_loop.py:76`, `tools.py:48`, `tools.py:112`, `tools.py:252`, `tools.py:326`, `artifact_tools.py:26`, `artifact_tools.py:181`).
- All tools share one `ClawWorkState` dataclass holding the economic tracker, task manager, evaluator, signature, current task/date, data path, and feature flags (`tools.py:29`).
- `/clawwork <instruction>` classifies the instruction into an occupation, prices it as `hours × hourly_wage`, builds a synthetic task dict, and rewrites the message with a forced submit workflow (`agent_loop.py:141`, `task_classifier.py:90`).
- `TaskClassifier` prompts the agent's own LLM provider (temperature 0.3, 256 max tokens) over a wage mapping, clamps hours to 0.25–40, and fuzzy-matches occupation names with a fixed fallback (`task_classifier.py:23`, `task_classifier.py:68`, `task_classifier.py:117`, `task_classifier.py:155`).
- `TrackedProvider` wraps the LLM provider's `chat()` and feeds `prompt_tokens` / `completion_tokens` plus OpenRouter's direct `cost` into `EconomicTracker.track_tokens`; `CostCapturingLiteLLMProvider` enriches usage from `response.usage.cost` or `_hidden_params["response_cost"]` (`provider_wrapper.py:18`, `provider_wrapper.py:44`).
- Configuration lives in `agents.clawwork` inside `~/.nanobot/config.json` with `enabled`, `signature`, `initialBalance`, token pricing, data/meta-prompt paths, and `enableFileReading`; the CLI wires provider, tracker, task manager, and evaluator together (`config.py:27`, `cli.py:75`, `cli.py:133`).

## 4. [[wiki/04-scheduler-api|Scheduler, API server, run configs]]

**In one sentence:** LiveBench run scheduling is configured by `default_config.json` date/agent/economic settings while `api/server.py` serves all agent data over REST plus WebSocket, and the `scheduler/` package itself is currently an empty placeholder.

- The `scheduler/` package contains only an empty `scheduler/__init__.py` (0 lines), so no scheduling logic lives there yet (`scheduler/__init__.py:1`).
- The API server is a FastAPI app defined as `app = FastAPI(title="LiveBench API", version="1.0.0")` in `api/server.py:23`.
- Run date range, economics, agents, and data paths are all set in `configs/default_config.json`, e.g. `init_date: 2025-01-20` through `end_date: 2025-01-31` (`configs/default_config.json:3-6`).
- Agent task data is served authoritatively from per-agent `task_completions.jsonl`, merged with `tasks.jsonl` metadata and `evaluations.jsonl` scores (`api/server.py:311-316`).
- Real-time frontend updates flow through the `/ws` WebSocket, the `ConnectionManager.broadcast()` fan-out, and the `watch_agent_files()` polling loop (`api/server.py:713-714`, `api/server.py:167-173`, `api/server.py:748-804`).
- Economic/token accounting uses `initial_balance: 1000.0` plus `input_per_1m: 2.5 / output_per_1m: 10.0` pricing from the run config (`configs/default_config.json:8-13`).

## 5. [[wiki/05-economics-scripts|Economics pipeline scripts]]

**In one sentence:** Four offline scripts estimate task labor hours with GPT-5.2, convert hours to dollar values via BLS wages, validate the EconomicTracker payment/threshold system, and retroactively rescale old uniform-$50 agent payments to real task values.

- `estimate_task_hours.py` estimates per-task professional hours with `MODEL = "gpt-5.2"` and streams results to `task_hour_estimates/task_hours.jsonl` (`scripts/estimate_task_hours.py:23`, `scripts/estimate_task_hours.py:25`).
- `calculate_task_values.py` computes `task_value = hours_estimate * hourly_wage` by matching each GDPVal occupation to a BLS `OCC_TITLE` with GPT-5.2 and writes `task_values.jsonl` (`scripts/calculate_task_values.py:26`, `scripts/calculate_task_values.py:261`).
- `recalculate_agent_economics.py` rescales paid entries with `new_payment = old_payment × (real_task_value / 50)` so the 0.6 evaluation cliff is preserved, writing a new `economic_real_value/` directory (`scripts/recalculate_agent_economics.py:120`, `scripts/recalculate_agent_economics.py:210`).
- `validate_economic_system.py` checks six required `EconomicTracker` methods, the `evaluation_score` parameter, per-channel cost separation, and threshold/date/task queries end to end (`scripts/validate_economic_system.py:237`, `scripts/validate_economic_system.py:404`).
- Payment gating is all-or-nothing at `min_evaluation_threshold=0.6`: scores below 0.6 pay $0, scores at or above pay the full amount, verified across nine boundary cases (`scripts/validate_economic_system.py:322`, `scripts/validate_economic_system.py:332`).
- Cost records distinguish four channels — `llm_tokens`, `search_api`, `ocr_api`, `other_api` — with per-task and per-day aggregation via `get_task_costs` and `get_daily_summary` (`scripts/validate_economic_system.py:433`, `scripts/validate_economic_system.py:127`).
- All three data scripts use append/streaming writes plus resume (`load_existing_estimates`, per-mapping saves) and 1-second rate limiting between LLM calls (`scripts/estimate_task_hours.py:195`, `scripts/calculate_task_values.py:227`, `scripts/estimate_task_hours.py:358`).

## 6. [[wiki/06-frontend-dashboard|Dashboard: static data + web UI]]

**In one sentence:** The dashboard is a React web app (a user interface that runs in the browser) plus a Python script that pre-builds JSON data files so the same app can run live against an API server or as a static site on GitHub Pages.

- The static generator `scripts/generate_static_data.py:89` (`gen_agents`), `:112` (`gen_leaderboard`), `:187` (`gen_agent_detail`), `:223` (`gen_agent_tasks`), `:297` (`gen_agent_learning`), `:319` (`gen_agent_economic`), `:346` (`gen_artifacts`), `:406` (`gen_settings`) mirrors the server API as JSON files under `frontend/public/data/` (`scripts/generate_static_data.py:13`).
- The frontend switches between live and static data sources with one flag, `VITE_STATIC_DATA`, read in `frontend/src/api.js:9`, with URL helpers `staticUrl`/`liveUrl` at `frontend/src/api.js:12-13`.
- The app shell `frontend/src/App.jsx:14` holds agent list, selected agent, hidden-agent set, and display names, polls `fetchAgentsData` every 5 seconds (`frontend/src/App.jsx:49`), and routes 6 views (`frontend/src/App.jsx:102-130`).
- Real-time updates use a WebSocket hook (a reusable live-connection function) `frontend/src/hooks/useWebSocket.js:4` that is disabled in static mode with status `github-pages` (`frontend/src/hooks/useWebSocket.js:6`), otherwise reconnects every 3 seconds (`frontend/src/hooks/useWebSocket.js:35`).
- The sidebar `frontend/src/components/Sidebar.jsx:6` provides 5 navigation links (`frontend/src/components/Sidebar.jsx:21-27`), an agent list with survival-status dots (`frontend/src/components/Sidebar.jsx:29-42`), and an agent-visibility settings panel (`frontend/src/components/Sidebar.jsx:123-170`).
- The Dashboard page `frontend/src/pages/Dashboard.jsx:8` shows metric cards, a balance chart, a domain-earnings chart split by a quality cutoff `QUALITY_CLIFF = 0.6` (`frontend/src/pages/Dashboard.jsx:127`), and recent decisions (`frontend/src/pages/Dashboard.jsx:380-396`).
- Work, learning, leaderboard, and artifact pages each map to one pre-generated JSON file per agent, with file previews for PDF/XLSX/DOCX/PPTX shared in `frontend/src/components/FilePreview.jsx:201-217` (`renderFilePreview`).

<!-- FIVE_MOVES_START -->
## The argument in five moves

1. Frame AI assistants as economically accountable coworkers that must earn income while paying token costs from $10.
2. Run live daily agents over 220 GDPVal tasks with real-time cost tracking and payment gated at quality 0.6.
3. Integrate the economy into nanobot via ClawMode tools, task classification, and per-call cost tracking.
4. Configure runs by date and pricing, then serve agent data over REST plus WebSocket.
5. Validate economics offline by estimating hours, pricing via BLS wages, and enforcing the 0.6 pay cliff.
6. Present balances, earnings, and artifacts in a React dashboard that runs live or as a static site.
<!-- FIVE_MOVES_END -->
