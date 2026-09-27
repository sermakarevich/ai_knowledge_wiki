# Task: chapter 10 impl — agent evals: order-management agent with mock DB, tasks with expected final state, pass@k / pass^k, trajectory metrics, simulated user (code + runs, NO chapter writing)

Read ONLY `specs/COMMON.md`, `index.md`, `project/src/evals_tutorial/{llm,results,stats}.py` (signatures;
`llm.chat` must support tool calling via Ollama's OpenAI-compatible `tools=` — check and extend
`llm.py` minimally if it does not, keeping the cache), `project/data/handbook/order_changes.md` and
`returns.md`, and `research/SOURCES_practitioner.md` (Anthropic "Demystifying evals for AI agents" section)
plus `research/SOURCES_papers.md` (agent evaluation: τ-bench, pass^k). Do not read chapter markdown
(cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`).

## Problem
Chapters 02–09 evaluated single replies. Agents act: they call tools, change state, and can succeed by
different paths. The right grade is the **final state** plus constraints on the path (forbidden actions,
step budget), and because agents are stochastic, a task must be run several times: pass@k (any trial
passes — capability) vs pass^k (all trials pass — reliability; Yao et al. 2024, τ-bench).

## Fix

### `project/src/evals_tutorial/agent.py` (Typer: `demo`, `run`, `grade`, `simulate`, `all`)
- Mock shop DB: in-memory dataclasses seeded deterministically — 12 customers, 30 orders (statuses
  `placed, shipped, delivered, returned, cancelled`), items, addresses; `reset()` returns a fresh copy.
- Tools (plain Python functions with JSON schemas): `lookup_order(order_id)`, `list_orders(customer_email)`,
  `cancel_order(order_id)`, `update_address(order_id, address)`, `start_return(order_id, item_id, reason)`,
  `issue_refund(order_id, amount)`, `escalate(reason)`, `reply(text)` (ends the episode). Policy rules
  live in the handbook (`order_changes.md`, `returns.md`): e.g. address can change only while `placed`;
  refunds above 200 need escalation; returns within 30 days of delivery.
- Agent loop `run_episode(task, prompt_version, seed, temperature)`: system prompt
  `prompts/agent_v1.txt` (+ the two handbook sections), tool-calling loop with `qwen3.8:27b`, max 12
  steps, records the full trajectory (`messages`, tool calls with args and results, final DB diff,
  steps, latency).
- Tasks `project/data/agent_tasks.jsonl` — 20 tasks: `id, user_message, customer_email, expected_state
  (assertions on the DB after the episode, e.g. {"orders.O1017.status": "cancelled"}), required_actions[],
  forbidden_actions[], max_steps, expected_reply_keywords[]`. Mix: 8 straightforward, 6 needing a policy
  refusal (correct outcome = no state change + polite reply), 4 needing `escalate`, 2 with a missing
  order id (should ask / look up by email). Write them by hand from the handbook rules.
- `run --version v1 --trials 3 --temperature 0.7`: 20 × 3 = 60 episodes (each ≤ 12 calls → ≤ ~500 calls;
  gpu-check first, background). Trajectories → `runs/10_agent_v1/trajectories/<task>_<trial>.json`.
- `grade`: per episode `state_ok` (all expected_state assertions), `no_forbidden`, `within_steps`,
  `required_done`, `reply_ok` (keywords), `pass` = all. Aggregates: pass rate over episodes, **pass@3**
  and **pass^3** per task then averaged, mean steps, tool-call error rate (invalid args/unknown tool),
  policy-violation rate; per task-type table. Experiments `10_agent_v1_pass_at_k` (primary `pass@3`) and
  `10_agent_v1_pass_pow_k` (primary `pass^3`), n = 20 tasks, CIs via `stats` (bootstrap over tasks).
  Also a **transcript grader**: `prompts/agent_transcript_judge_v1.txt` grades the trajectory text for
  "followed policy and was helpful" (pass/fail + critique) on the 60 episodes (60 calls) → agreement
  with the state-based grade in `details` (experiment `10_agent_transcript_judge`, primary `kappa`).
- `simulate`: multi-turn for the 2 missing-id tasks + 4 others: a **simulated user** (`prompts/
  sim_user_v1.txt`, persona + hidden facts like the order id) answers the agent's questions for up to 4
  turns; 6 tasks × 3 trials (≤ ~200 calls). Experiment `10_agent_v1_multiturn` (primary `pass@3`, n = 6).

### `project/justfile`
`agent-demo`, `agent-run`, `agent-grade`, `agent-simulate`.

### Tests `project/tests/test_10_agent.py`
Mock DB rules (address change refused when shipped; refund > 200 requires escalation); grading of a
hand-built trajectory (pass and each failure kind); pass@k / pass^k on synthetic trial matrices
(k = 3, known answers); the agent loop with `FakeLLM` emitting one scripted tool call then `reply`
finishes and produces a trajectory. No network.

### Findings note `project/runs/10_findings.md` (REQUIRED)
Pass rate, pass@3, pass^3 (with CIs), per task-type table, steps/tool errors/violations, transcript-judge
agreement, multi-turn results; 2 trajectories summarised (one success, one policy violation: task,
tool calls in order, final diff, grade); LLM calls and seconds; what was skipped.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/evals_tutorial/agent.py`, `project/src/evals_tutorial/llm.py` (if extended),
`project/src/evals_tutorial/prompts/{agent_v1,agent_transcript_judge_v1,sim_user_v1}.txt`, `project/data/agent_tasks.jsonl`,
`project/runs/10_*/**`, `project/runs/results.md`, `project/data/cache/**`, `project/justfile`,
`project/tests/test_10_agent.py`, `project/runs/10_findings.md`.
Verify: `git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/project/runs/results.md | grep -c "10_agent_v1_pass_pow_k"` ≥ 1.

## Scope & constraints
No real network tools, no Inspect (12), no Langfuse (13). ≤ ~800 LLM calls total; if the budget runs out,
cut trials to 2 and record. Context budget ≈ 55k tokens. Do not run `fleet serve restart` or `fleet run`.
