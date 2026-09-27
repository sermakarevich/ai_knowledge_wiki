---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

# ClawWork — Retrieval Practice

## 1. Concept: AI-coworker economic benchmark

### Q1 (core recall): What are the starting balance, task scale, payment formula, judge, and end-to-end loop of ClawWork?

<details>
<summary>Answer</summary>

- Each agent starts with just $10 and pays for every token generated, so waste can wipe the balance.
- 220 GDPVal tasks spanning 44 occupations / economic sectors.
- Payment follows real economic value: `quality_score × (estimated_hours × BLS_hourly_wage)`.
- Work quality is scored by an LLM judge (GPT-5.2) with category-specific rubrics for each of the 44 sectors.
- End-to-end loop: Task Assignment → Execution → Artifact Creation → LLM Evaluation → Payment.

</details>

## 2. Live agent runtime and economic tracking

### Q2 (core recall): How does the live runtime run agents, cap work, track money, and classify survival — with exact numbers?

<details>
<summary>Answer</summary>

- `main.py` constructs one `LiveAgent` per configured agent signature and runs it over weekdays in the date range.
- Each `LiveAgent` owns `EconomicTracker`, `TaskManager`, `WorkEvaluator`, direct tools, and a tool-bound `ChatOpenAI` model.
- Daily loop `run_daily_session(date)`: selects one task, starts cost tracking, runs up to 15 tool-calling iterations, then saves end-of-day state.
- `EconomicTracker` deducts token/API costs in real time, writes `balance.jsonl` / `token_costs.jsonl` / `task_completions.jsonl`, and pays work income only when the evaluation score clears `min_evaluation_threshold=0.6`.
- Survival status from balance: bankrupt `<= 0`, struggling `< 100`, stable `< 500`, else thriving.
- On iteration-limit timeout without submission, a LangGraph `WrapUpWorkflow` lists sandbox artifacts, asks the LLM to pick deliverables, downloads, and submits them.

</details>

## 3. ClawMode integration: loop, tools, classifier

### Q3 (core recall): What are ClawMode's loop subclass, six tools, shared state, classifier settings, cost tracking, and config location?

<details>
<summary>Answer</summary>

- `ClawWorkAgentLoop` subclasses nanobot's `AgentLoop` and wraps every message with `start_task` / `end_task` plus a cost footer.
- Six tools on top of nanobot built-ins: `decide_activity`, `submit_work`, `learn`, `get_status`, `create_artifact`, and conditionally `read_artifact`.
- All tools share one `ClawWorkState` dataclass: economic tracker, task manager, evaluator, signature, current task/date, data path, feature flags.
- `/clawwork <instruction>` classifies the instruction into an occupation, prices it as `hours × hourly_wage`, builds a synthetic task dict, and rewrites the message with a forced submit workflow.
- `TaskClassifier` prompts the agent's own LLM provider (temperature 0.3, 256 max tokens), clamps hours to 0.25–40, and fuzzy-matches occupation names with a fixed fallback.
- `TrackedProvider` wraps `chat()` and feeds `prompt_tokens` / `completion_tokens` plus OpenRouter's direct `cost` into `EconomicTracker.track_tokens`.
- Configuration lives in `agents.clawwork` inside `~/.nanobot/config.json`: `enabled`, `signature`, `initialBalance`, token pricing, data/meta-prompt paths, `enableFileReading`.

</details>

## 4. Scheduler, API server, run configs

### Q4 (elaboration): Why can LiveBench run with an empty `scheduler/` package — and what breaks if the API served from the wrong source or skipped the WebSocket?

<details>
<summary>Answer</summary>

- Scheduling lives in config, not code: `scheduler/__init__.py` is 0 lines (empty placeholder), while `configs/default_config.json` sets the real run — `init_date: 2025-01-20` through `end_date: 2025-01-31`, economics, agents, and data paths.
- The API server (`app = FastAPI(title="LiveBench API", version="1.0.0")` in `api/server.py:23`) is the read layer: agent task data is served authoritatively from per-agent `task_completions.jsonl`, merged with `tasks.jsonl` metadata and `evaluations.jsonl` scores.
- Real-time updates flow through `/ws` WebSocket + `ConnectionManager.broadcast()` + `watch_agent_files()` polling loop.
- What breaks: serving from `tasks.jsonl` alone would show assigned work without completion/payment truth; skipping the merge with `evaluations.jsonl` loses the quality-gated pay signal; dropping the WebSocket/polling loop leaves the frontend stale, forcing manual refresh to see balance and survival changes.

</details>

## 5. Economics pipeline scripts

### Q5 (elaboration): Why is payment an all-or-nothing cliff at 0.6 with a rescale formula — what breaks if you pay proportionally or skip validation?

<details>
<summary>Answer</summary>

- Gating is all-or-nothing at `min_evaluation_threshold=0.6`: scores below 0.6 pay $0, scores at or above pay the full amount (verified across nine boundary cases).
- The cliff forces economic discipline: mediocre work earns nothing while still burning token/API costs across four channels (`llm_tokens`, `search_api`, `ocr_api`, `other_api`), so churning low-quality submissions bankrupts the agent.
- `recalculate_agent_economics.py` rescales old uniform-$50 payments with `new_payment = old_payment × (real_task_value / 50)` so the 0.6 cliff is preserved while values become real (`hours_estimate × hourly_wage` via GPT-5.2 + BLS matching).
- What breaks: proportional pay (e.g. 0.5 score → half pay) would subsidize mediocre work and hide the solvency signal; skipping `validate_economic_system.py` (six required tracker methods, per-channel cost separation, threshold/date/task queries) risks double-counting costs or paying below-threshold tasks.

</details>

## 6. Dashboard: static data + web UI

### Q6 (transfer): You must ship a live leaderboard plus a frozen demo on GitHub Pages from the same codebase. How do you apply the ClawWork dashboard pattern?

<details>
<summary>Answer</summary>

- Mirror the server API as pre-built JSON: port `scripts/generate_static_data.py` functions (`gen_agents`, `gen_leaderboard`, `gen_agent_detail`, `gen_agent_tasks`, `gen_agent_learning`, `gen_agent_economic`, `gen_artifacts`, `gen_settings`) to emit one JSON file per view under `frontend/public/data/`.
- Switch sources with one flag: `VITE_STATIC_DATA` (read in `api.js:9`) with `staticUrl` / `liveUrl` helpers — live mode polls the API (e.g. `fetchAgentsData` every 5 seconds) and opens the `useWebSocket` hook with 3-second reconnect; static mode disables the socket (status `github-pages`) and reads the JSON files.
- Reuse the view split: sidebar with 5 navigation links + survival-status dots + visibility settings, Dashboard page with metric cards, balance chart, domain-earnings chart split by `QUALITY_CLIFF = 0.6`, and recent decisions; map work/learning/leaderboard/artifact pages each to one JSON file per agent with shared `renderFilePreview` for PDF/XLSX/DOCX/PPTX.
- Result: the same React app runs live against FastAPI + WebSocket in production and as a static site with no server for the frozen demo.

</details>

## 7. Critical thinking: is the "real economic value" claim earned?

### Q7 (evaluation, see [[critical_thinking|Critical Analysis]]): ClawWork prices tasks as `estimated_hours × BLS_hourly_wage` and grades them with an LLM judge against an LLM-generated rubric. Why does this weaken the claim that agents earn "genuine economic value," and what would you need to add to strengthen it?

<details>
<summary>Answer</summary>

- Every number in the payment formula is model-estimated: `scripts/estimate_task_hours.py` has GPT-5.2 guess professional hours from prompt text alone (no ground-truth timing study); `scripts/calculate_task_values.py` has GPT-5.2 match each GDPVal occupation to a BLS wage title; and `eval/generate_meta_prompts.py` has GPT-5.2 write the grading rubric that GPT-5.2 (as judge) later scores against.
- Judge and rubric-author share the same model family, so a systematic leniency or strictness bias in GPT-5.2 propagates into both pricing and grading with no independent cross-check — the benchmark measures agent performance relative to one model's opinion, not relative to an external economic ground truth.
- The 0.6 quality cliff makes this worse at the margin: a 0.59 vs. 0.61 score (both judged by the same model) is the difference between $0 and full payment, so judge-score noise near the threshold dominates outcomes as much as actual task quality does.
- To strengthen the "real economic value" claim: replace at least one LLM-estimated leg with ground truth (human-timed task completion for hours, audited BLS matching, or human-graded quality on a sample) and report agent rankings under both LLM-judged and human-audited scoring to show whether conclusions are judge-family-dependent.

</details>
