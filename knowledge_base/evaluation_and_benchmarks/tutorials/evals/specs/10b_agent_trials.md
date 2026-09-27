# Task: chapter 10b — agent trials: 20 tasks × 3 trials, pass@k / pass^k, trajectory metrics, transcript judge, simulated user, findings (runs, NO chapter writing)

Read ONLY `specs/COMMON.md`, `specs/10_agent_evals_impl.md` (full design — this task is its SECOND HALF:
`run --trials 3`, `grade` aggregates and experiments, the transcript grader, `simulate`),
`project/runs/10a_findings.md`, `--help` and `grep -n "^def \|^@app"` of `evals_tutorial.agent`,
`head -2 project/data/agent_tasks.jsonl`. (cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`)

## Your part
1. `run --version v1 --trials 3 --temperature 0.7` (60 episodes, ≤ ~500 calls; gpu-check first, background
   + log; if over 3 h cut to 2 trials and record) → `runs/10_agent_v1/trajectories/`.
2. `grade` aggregates → experiments `10_agent_v1_pass_at_k` (primary `pass@3`), `10_agent_v1_pass_pow_k`
   (primary `pass^3`), n = 20 tasks, CIs via `stats` over tasks; trajectory metrics and per-task-type table
   in details.
3. Transcript grader `prompts/agent_transcript_judge_v1.txt` on the 60 episodes (60 calls) →
   `10_agent_transcript_judge` (primary `kappa` vs the state-based grade).
4. `simulate` with `prompts/sim_user_v1.txt`: 6 tasks × 3 trials, ≤ 4 user turns (≤ 200 calls) →
   `10_agent_v1_multiturn` (primary `pass@3`, n = 6). `just results`.
5. Tests: aggregate metrics on a synthetic trial matrix; simulated-user turn loop with `FakeLLM`.
6. `project/runs/10_findings.md` (REQUIRED; merge 10a): everything in the original spec's findings list.

Files to commit: `project/src/evals_tutorial/agent.py`, `project/src/evals_tutorial/prompts/{agent_transcript_judge_v1,sim_user_v1}.txt`,
`project/runs/10_*/**`, `project/runs/results.md`, `project/data/cache/**`, `project/justfile`,
`project/tests/test_10_agent.py`, `project/runs/10_findings.md`.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit only the files listed above by explicit path.
Verify: `git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/project/runs/results.md | grep -c "10_agent_v1_pass_pow_k"` ≥ 1.

## Scope & constraints
Do ONLY the part named above; the other half belongs to the sibling task. Context budget ≈ 45k tokens:
read the original spec once, never `cat` data files (use `head`/`wc -l`), keep tool output short.
LLM budget: ≤ 800 calls (cut trials to 2 if needed). Do not run `fleet serve restart` or `fleet run`.
