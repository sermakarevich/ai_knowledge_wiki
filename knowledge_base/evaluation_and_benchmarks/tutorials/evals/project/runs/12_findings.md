# Chapter 12 — Findings: the helpdesk eval and GSM8K as Inspect-AI Tasks

Rebuild of chapters 05 and 11 on [Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai)
0.3.263, UK-AISI's eval framework. Same model (Ollama `qwen3.8:27b`), same prompt
files, same cached client — the only variable is the harness. Code:
`src/evals_tutorial/inspect_tasks.py` (tasks, solvers, scorers, `CachedModelAPI`),
`inspect_run.py` (Typer runners + `collect`).

## Results

| experiment | n | primary metric | value | 95% CI (bootstrap) |
|---|---|---|---|---|
| `12_inspect_helpdesk_v1` | 60 | **pass_rate** (mean of the model-graded `judge_grade` scorer) | **0.70** | [0.583, 0.817] |
| `12_inspect_gsm8k_qwen3.8:27b` | 50 | **accuracy** (built-in `match(location="end", numeric=True)`) | **0.96** | [0.90, 1.00] |

Helpdesk secondaries: `accuracy` (agree with ch-03 human labels) = 0.60 [0.483, 0.733] —
identical to ch-05's 0.60; `kappa` (positive=fail) = 0.155 [-0.088, 0.415] — identical to
ch-05's 0.1549; `code_checks_mean` = 0.819; `includes_hit_rate` = 0.0 (replies paraphrase,
verbatim gold-keyword hits expected to be low).

## Reconciliation (per-item, full tables in `runs/12_reconcile.md`)

- **Helpdesk vs ch-05 `05_judge_overall`**: 0 / 60 disagreements in pass/fail verdict and
  in which failure mode failed. Cause: the `judge_grade` scorer runs the *same* four
  tracked-mode judges with the *same* frozen prompts/versions through the *same* cached
  client, so every judge verdict and the generated reply are byte-identical to ch-05's.
  The 8 mismatching verdicts vs human labels that ch-05 had carry over unchanged — same
  tickets, same causes (judge vs human disagreement on borderline answers).
- **GSM8K vs ch-11 `11_gsm8k_plain_*`**: 0 / 50 disagreements (agreement 1.0). Same 50
  questions in the same order, same `gsm8k_plain_v1.txt` prompt, same cached client.
  Scorer equivalence: ch-11's harness extracts the last `#### N` line; Inspect's
  `match(location="end", numeric=True)` pulls the last parseable number — on this
  dataset they agree on all 50 (the 2 misses the model made are identical in both).

## Harness plumbing

- **Model API**: Inspect's native `ollama/` provider was not used. Instead
  `CachedModelAPI` (`inspect_tasks.py`, registered as `cached_ollama`) is a custom
  `ModelAPI` whose `generate()` delegates to `evals_tutorial.llm.ollama` — the same
  disk-cached client every chapter uses. Consequence: **every re-run costs 0 fresh LLM
  calls** (helpdesk full run: 3s wall / 119 cache hits; gsm8k: 1s / 50 hits), and the
  numbers reconcile 1:1 by construction. The spec's `openai/qwen3.8:27b` route was
  considered and rejected for exactly this cache-reuse reason.
- **Scorers**: (a) `judge_grade` — custom `@scorer` that AND-composes the four tracked
  ch-05 failure-mode judges (per-mode verdict+critique in `Score.metadata`, ch-05's rule:
  pass iff no mode fails); (b) `code_checks` — ch-10's six deterministic `code_evals`
  checks scored as pass-rate; (c) built-in `includes()` for verbatim answer-point hits.
  GSM8K: built-in `match(location="end", numeric=True)`, target = the gold number
  extracted from the harness CoT dump (`runs/11_lmeval/.../samples_*.jsonl`).
- **Logs**: 3 `.eval` archives under `runs/12_inspect/logs/` (helpdesk 412K/408K, gsm8k
  176K — zstd-compressed zips, not plain JSON). Trimmed 45-line excerpt:
  `runs/12_inspect/log_excerpt.json`. Viewer: `just inspect-view` →
  `http://127.0.0.1:7575` (screenshot not taken — no browser tool available in this
  session; the `inspect log dump` excerpt stands in per the spec).

## What was pleasant

- Dataset → solver → scorer decomposition meant the ch-05/ch-10 logic dropped into
  `@scorer` functions *unchanged* (the `code_checks` scorer is 15 lines of glue) —
  the scorers grade the same `ticket`/`trace` dictionaries as before.
- `inspect log dump` / `read_eval_log` is a clean, typed read API; `collect` needed
  no hacks to pull per-sample scores + metadata out of the logs.
- `Score.metadata` carries the per-mode verdicts, so the reconciliation tables come
  straight out of the log — no side-channel trace files needed.
- Typer integration is idiomatic (`@app.command` per workload, one `collect`).

## What hurt

- **Provider mismatch forced a custom `ModelAPI`**: Inspect's `openai/` provider
  speaks to a live API, so it can't see our disk cache; the `CachedModelAPI` shim is
  ~40 lines of async glue (`run_in_executor` around the sync cached client) just to
  keep cache reuse. It also means the log's "model" is the raw string, not Inspect's
  provider record.
- **`@scorer` is a factory-wrapped async fn**, not an object: `isinstance(x, Scorer)`
  passes on the decorator yet calling it returns a *coroutine* (`score_fn(state,
  target)`), which cost a test round-trip to pin down; there is no stable documented
  call signature beyond "async, take `TaskState, Target`, return `Score`".
- **`match`'s numeric parsing is permissive** (last parseable number): it silently
  accepts "…42 meters" and "#### 42" the same way, which hides output-format
  regressions the harness's strict `#### N` extractor would have surfaced. Equivalent
  *here* (0/50 split) — not guaranteed elsewhere.
- `.eval` logs are binary zstd-zips; anything ad-hoc (`jq`, grep) needs
  `inspect log dump` first — minor friction in CI/scripts.
- `Sample.metadata` is untyped (`dict`), and `TaskState` construction needs 5 args —
  hand-rolling test states around the scorers was easier with duck-types than real
  `TaskState` objects (see `tests/test_12_inspect.py`).

## What was skipped (per scope)

- No chapter markdown (spec forbids), no Langfuse, no screenshots (no browser tool).
- `model_graded_qa` built-in unused: the spec's "our ch-05 overall-judge template"
  maps 1:1 to our per-mode judge composition, and `model_graded_qa`'s generic
  rubric would drift from the frozen ch-05 prompts — `judge_grade` keeps bit-parity.
- 5-shot variant of ch-11: spec pins the *plain-prompt* re-run (50 questions).
- Log-viewer screenshots replaced by `log_excerpt.json` + the `inspect-view` recipe.

## How to reproduce

```
cd project
just inspect-helpdesk   # 60 test tickets, 0 fresh LLM calls (all cache hits)
just inspect-gsm8k      # 50 questions
just inspect-collect    # metrics.json ×2 + 12_reconcile.md + results.md rows
just inspect-view       # http://127.0.0.1:7575
uv run pytest tests/test_12_inspect.py -q -m "not slow"   # 7 offline tests
```
