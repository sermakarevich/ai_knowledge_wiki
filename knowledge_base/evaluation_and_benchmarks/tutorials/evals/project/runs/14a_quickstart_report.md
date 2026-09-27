# 14a — quickstart verification report

Run 2026-09-05 on a scratch clone (`/tmp/evals_quickstart`, `project/` copied, `.venv` removed).
Goal: prove a fresh reader can `just sync && just check && just test` and rebuild **every** result
from the committed caches with **zero LLM calls**.

## Verdict
PASS. All safe recipes rebuilt from cache with **0 cache misses** (cache stayed at 2720 files the
whole time), and `just results` is now **byte-identical** to the committed file (the determinism fix
above). One bug found and fixed in code; no experiment numbers were touched.

## Recipe table (all from scratch clone, Ollama up on the `rtx` box)
| step | command | ok | cache misses | ~s |
|---|---|---|---|---|
| 1 | `just sync` | ok | n/a | 2 |
| 2 | `just check` | ok (Ollama 0.32.12, chat OK, embed 768, 4 data files ok, cache 2720) | 3 live probes (expected) | 4 |
| 3 | `uv run pytest tests/ -q -m "not slow"` | **219 passed**, 8 deselected (`@pytest.mark.slow`) | 0 | 33 |
| 4 | `just results` | ok | **0** | <1 |
| 5 | `just code-evals` | ok | 0 | 1 |
| 6 | `just judge-scorecard` | ok | 0 | 1 |
| 7 | `just stats-retrofit` | ok (retrofitted 18) | 0 | 1 |
| 8 | `just labels-stats answer_v1` | ok | 0 | 1 |
| 9 | `just rag-retrieval answer_v1` | ok | 0 | 1 |
| 10 | `just rag-agreement answer_v1 30` | ok | 0 | 1 |

Skipped by design (would make real LLM calls with no cache in front / need a GPU batch, per the
"no LLM calls" constraint): `rag-ragas`, `rag-deepeval` (RAGAS/DeepEval call the model directly),
`bench-run`, `bench-sensitivity`, `bench-all` (lm-evaluation-harness). These still run — they are
the GPU-heavy recipes that need `just gpu-check` first and are out of scope for a no-LLM check.

## What was fixed
1. **`runs/results.md` was non-deterministic.** `results.py:build()` stamped `_generated
   {datetime.now(utc)}` into the header, so a clean rebuild (spec step 2) could never match the
   committed file and `just results && git diff --quiet` failed. Fix: dropped the moving clock —
   the header is now just `58 experiment(s)`. Fully content-derived, so rebuilding from unchanged
   data is byte-identical. (Verified: scratch rebuild == canonical, `diff` empty.)
2. **`justfile`: `inspect-collect`** (ch-12) had no doc line. Added one. (All other recipes already
   carried a doc comment.)
3. **`00_setup.md` "Verified on" table** refreshed: date 2026-09-05, and two packages that had
   moved since the last update — `numpy` 2.5.2 → **2.4.6**, `rich` 15.0.0 → **14.3.4**. (uv
   0.11.22, just 1.53.0, Python 3.14.6, Ollama 0.32.12 unchanged.)
4. **Wrote `project/README.md`** (76 lines) — prerequisites, the 5-command quickstart, caching,
   module → chapter table, one chapter's run, the Docker profile, and add-a-new-experiment
   (`write_metrics` → `just results`).

## Checked and fine (no change needed)
- **`.env` / `.env.template`** — every field in `config.py` is present with a sane default; nothing
  missing. (`.env` is gitignored; defaults in `config.py` match the template, so a fresh clone runs
  without it.)
- **cwd-dependent tests** — none. Data and cache paths resolve via `PROJECT_ROOT` / `__file__`, and
  the whole suite passed from the scratch clone (not its original location).
- **Byte-identity of the results table** — the only diff vs committed was the timestamp header (now
  fixed); all data rows were already identical.

## Remaining known issues
- The Langfuse span-exporter retries to `localhost:3030` during `pytest` (ch-13 `@observe`
  wrappers) and prints a "failed to export span batch" warning. Harmless when the stack is down —
  tracing is a no-op without keys — but it adds a few seconds and noise to the test run. Worth a
  "quiet Langfuse when unreachable" follow-up, not a blocker.
- `rag-ragas` / `rag-deepeval` / `bench-*` were not exercised (would make live LLM calls / a GPU
  batch). They are the only recipes whose output is not rebuildable from a committed cache in this
  setup; re-running them needs `just gpu-check` and a free 4090, as documented in the justfile.
- `just check` always makes its 3 live probes (chat, chat_json, embed) because they are seeded
  lazily — by design; it is the one command that is not cache-replayable.

## Test suite
`uv run pytest tests/ -q -m "not slow"` → **219 passed, 8 deselected, 33 s** (under the 2-minute
gate). 8 deselected are `@pytest.mark.slow` (live-LLM) tests, excluded by design.
