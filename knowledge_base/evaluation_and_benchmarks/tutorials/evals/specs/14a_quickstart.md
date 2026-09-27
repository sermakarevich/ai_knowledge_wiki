# Task: 14a — end-to-end quickstart check of the runnable project (verification + fixes, NO chapter writing)

Read ONLY `specs/COMMON.md`, `index.md`, `project/justfile`, `project/README.md` (if it exists) and
`00_setup.md` ("Verified on" table). (cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`)

## Problem
Thirteen chapters were built by different workers over days. Before the wrap-up we need proof that a
fresh reader can follow `index.md` → "Start with `cd project && just sync && just check`" and rebuild
every result **from the committed caches without a single LLM call**.

## Fix
1. In a scratch clone of only the project folder (`cp -r project /tmp/evals_quickstart && cd …`, remove
   `.venv`), run `just sync`, `just check` (Ollama may be reachable or not — `check` must degrade
   gracefully and say which services are up), `uv run pytest tests/ -q -m "not slow"` (time it; must be
   < 2 min), then every non-slow, non-Docker recipe that rebuilds results from cache: `just results`,
   `just code-evals`, `just judge-scorecard`, `just stats-retrofit`, `just labels-stats`, `just rag-retrieval`
   … (read the justfile; anything that would make LLM calls must hit the cache — watch
   `evals_tutorial.llm`'s usage log / cache-miss counter; **0 misses** expected). Record every recipe:
   ok / failed / cache misses / seconds.
2. Confirm `runs/results.md` after the rebuild is byte-identical to the committed one (`git diff --stat`);
   if not, find out why (unseeded randomness, timestamp in the table body, missing cache) and fix the
   cause in code — minimal changes — never by editing the numbers.
3. Fix broken recipes, missing `just` comments, missing dependencies, tests depending on a specific
   working directory, and `.env.template` gaps. Fill/refresh the "Verified on" table in `00_setup.md`
   with the exact installed versions (`uv pip list` for the libraries named there) and the date.
4. Write `project/README.md` (≤ 80 lines): what the project is, prerequisites, the 5-command quickstart,
   the module ↔ chapter table, how caching works, how to run one chapter's experiment, how to run the
   Docker profile, how to add a new experiment (write_metrics → just results).
5. Write `runs/14a_quickstart_report.md`: the recipe table from step 1, what was fixed, remaining known
   issues (be explicit), test suite time.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"` (< 2 min, green) and `just results && git diff --quiet project/runs/results.md`.

## DoD
As in COMMON.md. Commit: `project/README.md`, `00_setup.md`, `project/runs/14a_quickstart_report.md`, plus
every file you had to fix (explicit paths). Verify:
`git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/project/README.md | grep -c "just sync"` ≥ 1.

## Scope & constraints
No new experiments, no LLM calls (a cache miss is a finding to fix, not something to run), no chapter
prose beyond the "Verified on" table. Do not start Docker unless a recipe you are fixing needs it, and
stop it after. Context budget ≈ 50k tokens. Do not run `fleet serve restart` or `fleet run`.
