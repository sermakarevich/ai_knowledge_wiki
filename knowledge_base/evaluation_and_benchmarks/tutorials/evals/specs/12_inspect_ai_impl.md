# Task: chapter 12 impl — the helpdesk eval as an Inspect AI Task, scorers, log viewer, GSM8K in Inspect reconciled with chapter 11 (code + runs, NO chapter writing)

Read ONLY `specs/COMMON.md`, `index.md`, `project/src/evals_tutorial/{helpdesk,judge,results,stats}.py`
(signatures: `retrieve`, `answer`, the judge prompt loader, `write_metrics`, `bootstrap_ci`),
`project/runs/results.md` (rows `05_judge_overall`, `11_gsm8k_qwen*`), and `research/SOURCES_tools.md`
(Inspect AI entry: version, Ollama/OpenAI-compatible provider, `inspect eval`, `inspect view`). Do not
read chapter markdown (cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`).

## Problem
Everything so far is a hand-rolled harness. Inspect AI (UK AI Security Institute) is the leading open
framework with the dataset → solver → scorer model, a log viewer and many built-in scorers. Rebuild the
helpdesk eval in it, reuse our aligned judge as a model-graded scorer, run GSM8K through Inspect, and see
whether it reproduces chapter 11 and chapter 05.

## Fix

### `project/src/evals_tutorial/inspect_tasks.py` (+ Typer wrapper `inspect_run.py`: `helpdesk`, `gsm8k`, `collect`)
- Install `inspect-ai` (check version and the provider syntax; the model string is
  `openai/qwen3.8:27b` with `OPENAI_BASE_URL=http://127.0.0.1:11435/v1`, `OPENAI_API_KEY=ollama`, or
  Inspect's native `ollama/` provider if present — use whichever works and record it).
- `@task helpdesk_answer(split="test", version="v1")`: dataset = the 60 test tickets as `Sample(input=
  ticket text, target=gold answer points, metadata=gold+id)`; solver chain = a custom `@solver` that runs
  **our** retrieval (`helpdesk.retrieve`, cached embeddings) and injects the sections into the system
  prompt from `prompts/answer_<version>.txt`, then `generate()`; scorers: (a) `model_graded_qa` with our
  chapter-05 overall-judge wording as the template (frozen text, copied from the prompt file, grader
  model = same qwen), (b) a custom `@scorer` `code_checks` reusing `code_evals` check functions, (c)
  `includes()` on the answer-point keywords. `--limit 60`, temperature 0, `--log-dir runs/12_inspect/logs`.
  ≈ 60 gen + 60 grader calls.
- `@task gsm8k_inspect(limit=50)`: use Inspect's built-in GSM8K recipe if available in `inspect_evals`
  (add the package; else a 30-line task with `match(numeric=True)` on the same 50 questions in the same
  order as chapter 11 — read them from the harness samples file `runs/11_lmeval/.../samples_*.jsonl`).
  50 calls.
- `collect`: read Inspect's `.eval` logs via its Python API (`read_eval_log`) → `metrics.json` experiments
  `12_inspect_helpdesk_v1` (primary `pass_rate` from the model-graded scorer, n = 60, CI) and
  `12_inspect_gsm8k_qwen` (primary `accuracy`, n = 50, CI). **Reconciliation**: per-item agreement of the
  Inspect model-graded verdict with the chapter-05 `05_judge_overall` predictions (same tickets), and of
  Inspect's GSM8K per-item correctness with the harness's per-item correctness → both as kappa / % agree
  in `details`, plus a list of the disagreeing items with a one-line cause each (extraction, template,
  sampling) in `runs/12_reconcile.md`.
- Capture 1–2 screenshots of `inspect view` (Playwright MCP or the browser tool is NOT available to you
  — instead export the log as JSON with `inspect log dump` and save a trimmed 40-line excerpt to
  `runs/12_inspect/log_excerpt.json`; note in findings that the viewer runs at `inspect view --port 7575`).

### `project/justfile`
`inspect-helpdesk`, `inspect-gsm8k`, `inspect-view` (port 7575), `inspect-collect`.

### Tests `project/tests/test_12_inspect.py`
The dataset builder yields 60 samples with the metadata fields; the custom scorer over a fake state
object returns CORRECT/INCORRECT as expected; `collect` on a tiny hand-written log-like dict produces the
metrics schema. Import-guard `inspect_ai`; real runs are `@pytest.mark.slow`. No network.

### Findings note `project/runs/12_findings.md` (REQUIRED)
Both experiments' numbers with CIs; the reconciliation (kappa/% agree with chapter 05 and 11, number of
disagreements and the causes); Inspect version and provider used; how long each run took; what was
pleasant and what hurt (concretely — errors hit, docs gaps); log sizes; what was skipped.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/evals_tutorial/{inspect_tasks,inspect_run}.py`, `project/pyproject.toml`,
`project/uv.lock`, `project/runs/12_*/**` (Inspect `.eval` logs only if ≤ 5 MB total, else keep the JSON excerpt only),
`project/runs/12_reconcile.md`, `project/runs/results.md`, `project/data/cache/**`, `project/justfile`,
`project/tests/test_12_inspect.py`, `project/runs/12_findings.md`.
Verify: `git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/project/runs/results.md | grep -c "12_inspect_helpdesk_v1"` ≥ 1.

## Scope & constraints
Do not change chapter-05 prompts or chapter-11 outputs. ≤ ~200 LLM calls. No Langfuse (13). Context
budget ≈ 55k tokens. Do not run `fleet serve restart` or `fleet run`.
