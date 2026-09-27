# Task: chapter 13b — the CI regression gate, GitHub workflow, online monitoring on a sample, tool landscape, findings (code, ZERO LLM calls, NO chapter writing)

Read ONLY `specs/COMMON.md`, `specs/13_production_impl.md` (full design — this task is its SECOND HALF:
`ci`, `monitor`, the workflow file, the landscape table), `project/runs/13a_findings.md`, `--help` and
`grep -n "^def \|^@app"` of `evals_tutorial.prod`, `evals_tutorial.stats`, `evals_tutorial.halluc`,
`research/SOURCES_tools.md` (landscape rows: promptfoo, Opik, Phoenix, LangSmith, Braintrust, MLflow, Weave, Langfuse).
(cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`)

## Your part
1. `ci` / `just eval-ci version=v2 baseline=v1`: the gate rule from the original spec (fail if the CI upper
   bound of the pass-rate delta < −0.05 or `all_checks_pass` drops > 0.10), Markdown summary, exit code,
   `runs/13_ci_gate/metrics.json` (experiment `13_ci_gate_v2_vs_v1`). `project/.github/workflows/evals-ci.yml`
   example (not executed).
2. `monitor --sample 0.2`: 7 seeded "days", HHEM + one cheap code check on the sample, rolling table +
   PNG → `runs/13_monitor/`, one alert rule; push scores to Langfuse only if it is up (start it with
   `just langfuse-up` if needed, stop it after).
3. Landscape table → `runs/13_landscape.md` (from SOURCES_tools only). `just results`.
4. Tests: gate decision logic on synthetic prediction pairs; monitor sampler deterministic and covering all
   traces over 7 days. No network.
5. `project/runs/13_findings.md` (REQUIRED; merge 13a): the actual gate summary and decision, the monitor
   table, the landscape table, everything else in the original spec's findings list.

Files to commit: `project/src/evals_tutorial/prod.py`, `project/.github/workflows/evals-ci.yml`, `project/runs/13_*/**`,
`project/runs/13_landscape.md`, `project/runs/results.md`, `project/justfile`, `project/tests/test_13_prod.py`,
`project/runs/13_findings.md`.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit only the files listed above by explicit path.
Verify: `git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/project/runs/13_landscape.md | grep -c "Langfuse"` ≥ 1.

## Scope & constraints
Do ONLY the part named above; the other half belongs to the sibling task. Context budget ≈ 45k tokens:
read the original spec once, never `cat` data files (use `head`/`wc -l`), keep tool output short.
LLM budget: 0 calls. Do not run `fleet serve restart` or `fleet run`.
