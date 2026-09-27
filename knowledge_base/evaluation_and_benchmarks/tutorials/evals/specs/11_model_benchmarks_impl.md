# Task: chapter 11 impl — model benchmarks with lm-evaluation-harness against Ollama: GSM8K and IFEval, three models, prompt sensitivity, error bars (code + runs, NO chapter writing)

Read ONLY `specs/COMMON.md`, `index.md`, `project/src/evals_tutorial/{results,stats}.py` (signatures),
`research/SOURCES_tools.md` (lm-evaluation-harness entry: version, `local-chat-completions`, flags) and
`research/SOURCES_papers.md` (benchmark methodology: GSM8K, IFEval, GSM1k contamination, saturation,
Miller 2024). Do not read chapter markdown (cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`).

## Problem
Public benchmarks are how models are compared, and how they are misread. Run two standard ones locally
through the de-facto standard harness against Ollama, on three very different models, and show what
moves the score: sample size (error bars), prompt template / few-shot count, answer extraction, and
model size.

## Fix

### `project/src/evals_tutorial/bench.py` (Typer: `run`, `collect`, `sensitivity`, `all`)
- Install `lm_eval` (`lm-evaluation-harness`, add to pyproject with the `api` extra if needed; check the
  installed version and `lm_eval --help`). Model spec:
  `--model local-chat-completions --model_args model=<name>,base_url=http://127.0.0.1:11435/v1/chat/completions,num_concurrent=1,max_retries=3,tokenized_requests=False`
  with `OPENAI_API_KEY=ollama`, `--apply_chat_template`, `--gen_kwargs temperature=0`, `--limit 50`,
  `--seed 0`, `--output_path runs/11_lmeval/<model>/<task>/`, `--log_samples`.
- `run`: tasks `gsm8k` (default 5-shot, exact-match on the extracted answer) and `ifeval`
  (`prompt_level_strict_acc`, `inst_level_strict_acc`) for models `qwen3.8:27b`, `gemma4:latest`,
  `tiny-qwen35-110m-sft:latest` (expect ≈ 0 — that is the point). 50 items × 2 tasks × 3 models = 300
  calls (+ retries); gpu-check first, background with a log. If `qwen3.8:27b` emits thinking tokens
  that break extraction, add a `--gen_kwargs` / system-prompt fix and **record both scores**.
- `collect`: parse the harness result JSON (`results.json` + `samples_*.jsonl`) into our `metrics.json`
  per (model, task): experiment `11_<task>_<model>` (primary = the task's main metric, n = 50, `ci` via
  bootstrap over the per-sample correctness from the samples file, `llm_calls` = 50, `seconds` from the
  log). Compare the harness's own stderr with our bootstrap CI in `details`.
- `sensitivity` (qwen only, gsm8k, 50 items): (a) `--num_fewshot 0` vs 5; (b) the harness's `gsm8k_cot`
  variant (different template and extraction); (c) our own minimal re-implementation
  `prompts/gsm8k_plain_v1.txt` with a lenient regex extractor on the same 50 questions through
  `evals_tutorial.llm` (50 calls, cached) — three more scores for the same model and items; paired
  bootstrap of the differences via `stats.paired_bootstrap`. Experiment `11_gsm8k_prompt_sensitivity`
  (primary `score_range` = max − min across variants; details: the four scores with CIs and per-item
  agreement). Also report per-item: how many questions flip between variants.
- Contamination/saturation are literature points only — do NOT run GSM1k; just save a short table of
  reported numbers with citations into `runs/11_notes.md` from `research/SOURCES_papers.md`.

### `project/justfile`
`bench-run model=… task=…`, `bench-collect`, `bench-sensitivity`.

### Tests `project/tests/test_11_bench.py`
Parsing a saved miniature harness `results.json` + samples file (write a 5-line fixture in the test)
into `metrics.json`; the lenient GSM8K extractor on 8 tricky strings ("#### 42", "$1,234", "The answer
is 7."); model-arg string builder. No network; harness invocation is `@pytest.mark.slow`.

### Findings note `project/runs/11_findings.md` (REQUIRED)
Score table (3 models × 2 tasks with CIs and the harness stderr), seconds per model; the sensitivity
table (0-shot, 5-shot, cot, plain — with CIs and the paired deltas) and the count of flipping items with
one example question that flips; anything about thinking tokens / extraction failures; installed
lm_eval version; what was skipped.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/evals_tutorial/bench.py`, `project/src/evals_tutorial/prompts/gsm8k_plain_v1.txt`,
`project/pyproject.toml`, `project/uv.lock`, `project/runs/11_*/**` (harness outputs: results.json and samples only, ≤ 5 MB
total — delete anything larger), `project/runs/11_notes.md`, `project/runs/results.md`, `project/data/cache/**`,
`project/justfile`, `project/tests/test_11_bench.py`, `project/runs/11_findings.md`.
Verify: `git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/project/runs/results.md | grep -c "11_gsm8k_qwen"` ≥ 1.

## Scope & constraints
`--limit 50` is fixed; no other tasks or models. ≤ ~550 LLM calls. No Inspect (12). Context budget
≈ 55k tokens. Do not run `fleet serve restart` or `fleet run`.
