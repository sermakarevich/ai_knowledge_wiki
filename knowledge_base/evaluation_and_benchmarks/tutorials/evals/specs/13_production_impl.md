# Task: chapter 13 impl — production: Langfuse self-hosted (tracing, datasets, experiment runs, scores), a CI regression gate, online sampling (code + runs, NO chapter writing)

Read ONLY `specs/COMMON.md`, `index.md` ("Local settings" — Langfuse row), `project/src/evals_tutorial/
{helpdesk,judge,halluc,results,stats}.py` (signatures only), `project/runs/results.md`, and
`research/SOURCES_tools.md` (Langfuse entry: version, self-host compose, SDK v3 API, datasets/experiments;
plus the landscape rows for promptfoo, Opik, Phoenix, LangSmith, Braintrust, MLflow, Weave). Do not read
chapter markdown (cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`).

## Problem
Scripts and a results table are not a system. Production needs: every request traced; the eval set
stored as a dataset; each prompt version run as an experiment with scores attached; a CI (continuous
integration) gate that fails a change when the eval drops beyond the noise; and online monitoring on a
sample of live traffic. Langfuse is the leading open-source (MIT) self-hostable option.

## Fix

### `project/docker-compose.yml` — profile `langfuse`
Langfuse v3 stack (langfuse-web, langfuse-worker, postgres, clickhouse, redis, minio) from the official
self-host compose, **all container names prefixed `evals-`**, UI on host port **3030** → 3000, every
other port not published (or shifted, documented in `.env.template`), volumes named `evals-langfuse-*`
(never committed). `just langfuse-up|down|logs`; add the Langfuse keys to `.env.template`
(`LANGFUSE_HOST=http://localhost:3030`, `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`) — set
`LANGFUSE_INIT_*` env vars in compose so a project + keys exist at first start without clicking
(check the current variable names in the Langfuse docs cited in SOURCES_tools). Health check: wait for
`http://localhost:3030/api/public/health`.

### `project/src/evals_tutorial/prod.py` (Typer: `trace`, `dataset`, `experiment`, `scores`, `ci`, `monitor`)
- `trace --run answer_v1`: replay the 80 committed traces into Langfuse as traces/generations via the
  Python SDK (check the installed `langfuse` version; v3 uses `langfuse.start_as_current_observation` /
  `@observe` — use what is installed), including retrieved sections, latency, model, usage and the ticket
  metadata. Zero LLM calls. Also wrap `helpdesk.answer` with `@observe` so **new** calls are traced when
  `LANGFUSE_*` is set (env-guarded, no-op otherwise; tests must still pass without Langfuse).
- `dataset`: create dataset `helpdesk-test` with the 60 test tickets (input + expected = gold) and
  `helpdesk-dev` (20).
- `experiment --version v1|v2`: run the dataset through the traced `answer` (cached → zero LLM calls
  for v1/v2, the cache makes this free), attach the chapter-05 overall-judge verdict (read from the
  committed predictions; no new judge calls) and the chapter-04 checks as **scores** on each run item, so
  the Langfuse UI shows v1 vs v2 side by side. Record the run URLs in the findings.
- `scores`: push the chapter-03 labels as `human`-source scores on the replayed traces (shows how
  human annotation lands next to judge scores).
- `ci`: `just eval-ci version=v2 baseline=v1`: computes pass rate of `version` vs `baseline` from
  committed predictions with `stats.paired_bootstrap`; **fails (exit 1) if the CI upper bound of the
  delta < −0.05 or the check-suite `all_checks_pass` rate drops by more than 0.10**; prints a Markdown
  summary suitable for a PR comment; writes `runs/13_ci_gate/metrics.json` (experiment `13_ci_gate_v2_vs_v1`,
  primary `pass_rate_delta`, `ci`, details: gate decision). Add a `.github/workflows/evals-ci.yml`
  example (not executed here) that runs the offline tests and `just eval-ci` on the cached data.
- `monitor --sample 0.2`: simulate online monitoring — sample 20 % of the replayed traces daily
  (seeded), score them with HHEM (chapter 09, CPU) and a **cheap** code check, and push as scores;
  produce a 7-"day" table of rolling pass rate (days = 7 seeded splits of the 80 traces) →
  `runs/13_monitor/rolling.md` + `rolling.png`. Show one alert rule (rate below the v1 CI lower bound).
- Landscape table (from `research/SOURCES_tools.md`, not from memory): promptfoo, Opik, Phoenix,
  LangSmith, Braintrust, MLflow, Weave, Langfuse — licence, self-host, datasets/experiments, online
  scoring, judge library, price model, one-line verdict → `runs/13_landscape.md`.

### `project/justfile`
`langfuse-up`, `langfuse-down`, `langfuse-logs`, `prod-trace`, `prod-dataset`, `prod-experiment version=…`,
`eval-ci version=v2 baseline=v1`, `prod-monitor`.

### Tests `project/tests/test_13_prod.py`
The CI gate decision logic on synthetic prediction pairs (pass, fail on delta, fail on checks); the
monitor sampler is deterministic and covers all traces over 7 days; `@observe` wrapper is a no-op
without env vars; compose file parses (`yaml.safe_load`) and every service name starts with `evals-`
and no port other than 3030 is published. Langfuse-live paths are `@pytest.mark.slow`. No network.

### Findings note `project/runs/13_findings.md` (REQUIRED)
Compose startup time and image sizes; counts of traces/dataset items/scores pushed and the experiment
run names; the CI gate output (the actual Markdown summary and the decision); the monitor table; the
landscape table; Langfuse SDK and server versions; pain points hit (auth, ClickHouse memory, SDK API
changes); LLM calls (should be 0) and seconds; what was skipped.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/docker-compose.yml`, `project/.env.template`, `project/src/evals_tutorial/prod.py`,
`project/src/evals_tutorial/helpdesk.py` (if wrapped), `project/.github/workflows/evals-ci.yml`, `project/pyproject.toml`,
`project/uv.lock`, `project/runs/13_*/**`, `project/runs/13_landscape.md`, `project/runs/results.md`, `project/justfile`,
`project/tests/test_13_prod.py`, `project/runs/13_findings.md`.
Verify: `git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/project/docker-compose.yml | grep -c "evals-langfuse"` ≥ 1.
Run `just langfuse-down` before closing (leave no containers running).

## Scope & constraints
Zero or near-zero LLM calls (everything is replayed from cache/committed files). Ports and names fixed
by `index.md`. No Langfuse volumes or `.env` in git. Context budget ≈ 55k tokens. Do not run
`fleet serve restart` or `fleet run`.
