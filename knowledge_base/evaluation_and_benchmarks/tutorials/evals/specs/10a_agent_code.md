# Task: chapter 10a — the order-management agent: mock DB, tools, agent loop, 20 tasks, tests, a 3-task demo (code, NO chapter writing)

Read ONLY `specs/COMMON.md`, `specs/10_agent_evals_impl.md` (full design — this task is its FIRST HALF:
everything under "Mock shop DB", "Tools", "Agent loop", "Tasks", plus the `grade` functions),
`project/data/handbook/order_changes.md`, `project/data/handbook/returns.md`, and `llm.chat`'s signature
(does it accept `tools=`? extend minimally, keep the cache). (cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`)

## Your part
1. `project/src/evals_tutorial/agent.py`: mock DB with `reset()`, the 8 tools with JSON schemas and the
   policy rules, `run_episode(task, prompt_version, seed, temperature)` with `prompts/agent_v1.txt`, max 12
   steps, full trajectory recording; grading functions (`state_ok`, `no_forbidden`, `within_steps`,
   `required_done`, `reply_ok`, `pass`) and `pass_at_k` / `pass_pow_k` helpers. Typer: `demo`, `run`, `grade`
   (`simulate` stub for 10b).
2. `project/data/agent_tasks.jsonl`: the 20 hand-written tasks exactly as specified.
3. `demo`: run 3 tasks once at temperature 0 (≤ 36 calls) and grade them, to prove the loop works; save
   under `runs/10_demo/`.
4. `project/tests/test_10_agent.py` as in the original spec (DB rules, grading a hand-built trajectory,
   pass@k / pass^k on synthetic matrices, the loop with `FakeLLM` emitting one tool call then `reply`). No network.
5. `project/runs/10a_findings.md`: the demo trajectories summarised, tool-calling quirks of the model,
   calls and seconds.

## Not your part (10b)
The 20 × 3 trial run, aggregate metrics/experiments, the transcript judge, the simulated user, `10_findings.md`.

Files to commit: `project/src/evals_tutorial/agent.py`, `project/src/evals_tutorial/llm.py` (if extended),
`project/src/evals_tutorial/prompts/agent_v1.txt`, `project/data/agent_tasks.jsonl`, `project/runs/10_demo/**`,
`project/data/cache/**`, `project/justfile`, `project/tests/test_10_agent.py`, `project/runs/10a_findings.md`.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit only the files listed above by explicit path.
Verify: `git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/project/data/agent_tasks.jsonl | grep -c "expected_state"` ≥ 1.

## Scope & constraints
Do ONLY the part named above; the other half belongs to the sibling task. Context budget ≈ 45k tokens:
read the original spec once, never `cat` data files (use `head`/`wc -l`), keep tool output short.
LLM budget: ≤ 50 calls. Do not run `fleet serve restart` or `fleet run`.
