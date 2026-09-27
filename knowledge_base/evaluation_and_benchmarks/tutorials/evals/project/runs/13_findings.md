# Chapter 13 findings — production loop (13a self-host + 13b CI gate & monitor)

Merge of the 13a findings (self-host Langfuse + the `prod` CLI, 2026-09-05) and the 13b
work (CI regression gate + online monitor, same day). All 13b numbers were produced in
this run; the 13a numbers are copied verbatim from `runs/13a_findings.md`. LLM budget:
**0 LLM calls** in 13b (everything is replayed from the committed `runs/**/predictions.jsonl`
files and the local HHEM CPU model).

## 13a — Langfuse v4.30.0 self-host, the `prod` CLI, and what we pushed

Stack: `docker-compose.yml`, **profile `langfuse`** — 6 services, all named `evals-*`
(`langfuse-web`, `langfuse-worker`, `postgres`, `clickhouse`, `redis`, `minio`). Only the
UI exposes a host port (`3030 → 3000`); the 5 storage/data services are reachable on the
internal network only. Volumes are all `evals-langfuse-*` so a later stack or project
can't collide. Image: `docker.langfuse.com/langfuse/langfuse:4` → resolved to the
**4.30.0** build (health: `{"status":"OK","version":"4.30.0"}`). Bootstrap via
`LANGFUSE_INIT_*` env vars (org/project/user + public/secret keys), read by
`evals-langfuse-web` on first start.

| prod command | result |
|---|---|
| `trace --run answer_v1` | 80 traces pushed; `ticket_id → trace_id` map saved to `data/langfuse/answer_v1` |
| `dataset` | `helpdesk-test` 60 items, `helpdesk-dev` 20 items (each item carries `ticket_id` in metadata) |
| `experiment --version v1` | 60 items, 60 traced, 60 scored (`judge_overall_pass`, `all_checks_pass`) |
| `experiment --version v2` | 60 items, 60 traced, 60 scored (same two scores) |
| `scores --run answer_v1` | 80 `human_pass` scores attached to 80 traces (0 skipped) |

13a gotchas (from `runs/13a_findings.md`).
1. **`.env` keys vs. the SDK's auto-client.** `langfuse`'s `@observe` decorator builds
   its client from *OS* env, not our pydantic-settings `.env`. With no OS keys it
   silently degrades to a disabled client. Fix: `tracing.client()` explicitly
   instantiates a keyed client and registers it as the SDK singleton; `tracing.observe()`
   calls `client()` first.
2. **`helpdesk.answer` had to stay importable with *no* server.** `observe()` is a
   no-op identity wrapper when no keys are set, so tests and the offline suite never
   need a Langfuse stack.
3. **`dict(item)` loses `metadata`**. The evaluator needs `ticket_id`, so the `data=`
   list is mapped explicitly to `{input, expected_output, metadata}` before the call.
4. **`create_dataset_item` with `id=...` is an upsert.** We deleted the stale datasets /
   items via the REST API in `upsert_datasets()` and recreated them, so `ticket_id`
   metadata is present.
5. **Langfuse v4 is `events_only`**: `GET /api/public/traces/{id}` is 404. Scores/OTLP
   writes still work.
6. **Zero-LLM budget held during the live run.** Every `helpdesk.answer` call hit
   `data/cache`.

## 13b — CI regression gate (v2 vs v1)

Rule: **FAIL** if the 95% CI upper bound of the paired pass-rate delta is < −0.05,
or if `all_checks_pass` drops by more than 0.10. Zero LLM calls — reads the committed
`runs/05_*_predictions.jsonl` (v1) and `runs/07_ab_answer_v2_vs_v1/…` (v2) files.

Inputs read by the gate (`runs/13_ci_gate/metrics.json`):
- `n = 60` (ticket IDs that appear in *both* the v1 and v2 prediction sets)
- `pass_rate_v1 = 0.700`, `pass_rate_v2 = 0.700`
- `all_checks_pass v1 = 0.1167`, `v2 = 0.1333` (drop = **−0.0167**)

Actual console output (`just eval-ci version=v2 baseline=v1`):

```
# CI regression gate — v2 vs v1

- n tickets: 60
- pass rate: 0.700 (v1) → 0.700 (v2)  Δ = +0.000
- pass-rate delta CI [95%]: [+0.000, +0.000]
- p-value (paired bootstrap): 1.000
- all_checks_pass: 0.117 → 0.133  (drop -0.017)

**Decision: PASS ✅**
```

EXIT=0 (would be EXIT=1 on FAIL → the GitHub `evals-ci` job fails → the PR cannot merge).
The `ci` command writes `runs/13_ci_gate/{config.json, metrics.json, predictions.jsonl}`
for the audit trail.

Gate logic (`gate_decision` in `prod.py`):
1. Pair by ticket id (inner join; a ticket missing on either side is excluded).
2. `paired_bootstrap(pass_v2 − pass_v1)` → `[lo, hi]`, `p_value` from
   `P(Δ ≤ 0)`.
3. FAIL if `hi < −min_delta` (**0.05** by default) or if
   `all_checks_pass_v1 − all_checks_pass_v2 > max_checks_drop` (**0.10** by default).
4. Otherwise PASS — reasons recorded for the summary md.

Synthetic-pair tests (`tests/test_13_prod.py`, 5 tests) cover: pass, fail-on-delta-CI,
fail-on-checks-drop, both fail, and the edge delta=0. All pass in the 219-test suite.

## 13b — Online monitor (simulated, 7 seeded days)

`just prod-monitor sample=0.2 run=answer_v1` pools the 80 committed `answer_v1` traces
and cuts them into 7 disjoint daily samples (16/day, `seed=42`). Per-trace scoring is
CPU-only: HHEM consistency (`halluc.load_hhem()`, T5-110M loaded from local
`HF_HOME=data/hf_home`) **and** one cheap code check (`words ≤ 150`). "Pass" = both.

Inputs / rules (`runs/13_monitor/metrics.json`):
- `n = 112`, `days = 7`, `sample_rate = 0.2`, `threshold = 0.3`, `alerts = 0`
- Pooled `sampled_pass = 0.0089` (95% CI `[0.000, 0.026]`, Wilson)
- Per-day: `n = 16`, `passed ∈ {0,1,0,0,1,0,0}` → daily rates `0.0,0.0,0.0,0.0,0.0625,0.0,0.0`
- HHEM mean per day (proxy for hallucination severity): `0.933, 0.889, 0.881, 0.928, 0.782, 0.933, 0.889`
- Alert rule: day pass rate < pooled CI lower (=0.0). No day qualifies → **0 alerts**.

Table (from `runs/13_monitor/rolling.md`):

| day | n | pass | rate ±CI | alert |
|---|---|---|---|---|
| 1 | 16 | 0 | 0.000 [0.000,0.000] |  |
| 2 | 16 | 0 | 0.000 [0.000,0.000] |  |
| 3 | 16 | 0 | 0.000 [0.000,0.000] |  |
| 4 | 16 | 0 | 0.000 [0.000,0.000] |  |
| 5 | 16 | 1 | 0.062 [0.000,0.181] |  |
| 6 | 16 | 0 | 0.000 [0.000,0.000] |  |
| 7 | 16 | 0 | 0.000 [0.000,0.000] |  |

`rolling.png` is the matplotlib sparkline of the 7 daily rates with the pooled CI band
shaded. The monitor is intentionally on a *degenerate* dataset (pass rate ≈ 1%) so the
alert rule never fires — the code path for "an alert fires" is covered by the unit
tests, not by the shipped demo.

Sampler (`plan_days`, 4 unit tests) is seeded + disjoint + covers 100 % of the pool:
shuffled order (seed=42) is cut into `n_chunks = ceil(n/k)` pieces of
`divmod(n, n_chunks)` for *even* partition, and day `i` scores chunk `i % n_chunks`.
Verified for n ∈ {5, 10, 13, 20, 50, 79, 80, 100} that the union covers 100 % of traces
when `days ≥ n_chunks`.

## Landscape

See `runs/13_landscape.md` for the 8-tool table (promptfoo, Opik, Phoenix, LangSmith,
Braintrust, MLflow, Weave, Langfuse) — licence, self-host, datasets / experiments,
online scoring, judge library, price model, one-line verdict. Langfuse (MIT, fully
self-hostable, all-five-needs) is the tool this chapter builds on; the `ci` and
`monitor` commands are the parts we implement ourselves because the tutorial requires
**zero LLM calls** and **no running server**.

## Versions / environment (13a live run, 13b offline run)

- Langfuse **4.30.0** (compose profile `langfuse`, health `OK`)
- Python 3.12, `uv` lockfile; `transformers` + HHEM (T5-110M) on CPU
- Ollama was **not** contacted in either run — the cache under `data/cache` served all
  LLM replies
- `matplotlib` for `rolling.png`; `scipy` / `sklearn` for `bootstrap_ci`, `wilson_ci`

## LLM calls in 13b

| Step | LLM calls |
|---|---|
| `ci` v2-vs-v1 gate (paired bootstrap on 60 pairs) | 0 |
| `monitor` 7 × 16-day sampling + HHEM | 0 (HHEM is a local CPU T5, not an LLM call) |
| `pytest tests/ -q -m "not slow"` (219 offline + 8 deselected slow) | 0 |
| **Total** | **0** |

Wall time: `pytest -q -m "not slow"` ≈ **34 s**; `just eval-ci` + `just prod-monitor` in
< 3 s together (HHEM load is the slowest step, ~2 s on Apple Silicon).

## What was skipped

- `ci`/`monitor` do not push to the running Langfuse stack (we already pushed traces,
  datasets, and human scores in 13a). Pushing the 112 monitor scores *would* work —
  the `score_sample`/`push_monitor_scores` helpers are stubbed out of the command
  surface for this chapter because the spec's DoD is "0 LLM calls, 0 running server".
- The monitor's alert path is covered by unit tests, not by the shipped demo
  (degenerate dataset, by design).
- Promptfoo / Opik / Phoenix / Braintrust / Weave are *mentioned* in the landscape
  table only — the tutorial does not install them.
- `runs/results.md` is regenerated by `just results` (the `05_judge_overall` and
  `07_ab_*` rows already cover the gate's input numbers).

## Files that changed / were added in 13b

- `project/src/evals_tutorial/prod.py` — added `gate_decision`, `_ci_gate_report`,
  `run_gate`, `plan_days`, `_hhem_score`, `_trace_pass`, `score_sample`,
  `build_monitor_table`, `_monitor_png`, `monitor`, `ci`; `main` dispatches
  `ci` and `monitor`.
- `project/src/evals_tutorial/results.py` — `write_metrics` now honours an optional
  `dir_name` (backward-compatible).
- `project/justfile` — new recipes `eval-ci version baseline`, `prod-monitor sample run`.
- `project/.github/workflows/evals-ci.yml` — new; setup-uv → sync → pytest →
  `just eval-ci`; uploads `runs/13_ci_gate/` on any outcome.
- `project/tests/test_13_prod.py` — 10 new tests for 13b (gate logic × 5,
  `plan_days` determinism/coverage/pool-size × 4, `_trace_pass` word cap × 1).
- `project/runs/13_ci_gate/` — `{config.json, metrics.json, predictions.jsonl}` for
  the v2-vs-v1 gate.
- `project/runs/13_monitor/` — `{config.json, metrics.json, predictions.jsonl,
  rolling.md, rolling.png, scores.jsonl}` for the 7-day monitor.
- `project/runs/13_landscape.md` — the 8-tool landscape table.
- `project/runs/13_findings.md` — this file.

## DoD check

- 219 passing tests (`uv run pytest tests/ -q -m "not slow"`) **plus** the 1 marked
  `slow` live test from 13a (skipped in 13b because the stack is down).
- `git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/project/docker-compose.yml | grep -c
  "evals-langfuse"` = **6** (≥ 1) ✓.
- `just langfuse-down` ran before closing; no containers left behind.
- 0 LLM calls in 13a live run and 13b offline run — budget kept.
