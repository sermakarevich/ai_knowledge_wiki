# Task: chapter 13a — Langfuse self-hosted: compose profile, tracing replay, datasets, experiment runs, human scores (code + Docker, ZERO LLM calls, NO chapter writing)

Read ONLY `specs/COMMON.md`, `specs/13_production_impl.md` (full design — this task is its FIRST HALF:
the compose profile and `prod.py` commands `trace`, `dataset`, `experiment`, `scores`), `index.md`
("Local settings" Langfuse row), `research/SOURCES_tools.md` (Langfuse entry only), `--help` of
`evals_tutorial.helpdesk`, `head -3` of `runs/05_judge_overall/predictions.jsonl` and of one trace file.
(cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`)

## Your part
1. `project/docker-compose.yml` profile `langfuse` exactly as specified (names `evals-*`, UI 3030, init
   env vars, volumes not committed), `just langfuse-up|down|logs`, `.env.template` keys.
2. `project/src/evals_tutorial/prod.py`: `trace` (replay 80 traces), the env-guarded `@observe` wrapper on
   `helpdesk.answer`, `dataset` (`helpdesk-test`, `helpdesk-dev`), `experiment --version v1|v2` (cached
   generations; chapter-05 verdicts and chapter-04 checks attached as scores), `scores` (chapter-03 labels
   as human scores). Stubs for `ci`, `monitor`.
3. `project/tests/test_13_prod.py`: compose parses, all service names start with `evals-`, only 3030 is
   published; `@observe` wrapper is a no-op without env vars; Langfuse-live paths `@pytest.mark.slow`.
4. Run it for real once (`just langfuse-up`, health check, trace, dataset, experiment v1 and v2, scores),
   record counts and run names, then `just langfuse-down`.
5. `project/runs/13a_findings.md`: startup time, image sizes, counts pushed, run names/URLs, SDK and server
   versions, pain points.

## Not your part (13b)
The CI gate, the GitHub workflow, the monitor, the landscape table, `13_findings.md`.

Files to commit: `project/docker-compose.yml`, `project/.env.template`, `project/src/evals_tutorial/prod.py`,
`project/src/evals_tutorial/helpdesk.py` (if wrapped), `project/pyproject.toml`, `project/uv.lock`, `project/justfile`,
`project/tests/test_13_prod.py`, `project/runs/13a_findings.md`.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit only the files listed above by explicit path.
Verify: `git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/project/docker-compose.yml | grep -c "evals-langfuse"` ≥ 1.

## Scope & constraints
Do ONLY the part named above; the other half belongs to the sibling task. Context budget ≈ 45k tokens:
read the original spec once, never `cat` data files (use `head`/`wc -l`), keep tool output short.
LLM budget: 0 calls. Do not run `fleet serve restart` or `fleet run`.
