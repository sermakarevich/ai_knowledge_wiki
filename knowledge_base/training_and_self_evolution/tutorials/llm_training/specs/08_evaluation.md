# Task: chapter 08 — Evaluation: lm-evaluation-harness general suite, Ollama endpoint eval, the CyberMetric domain harness, LLM-as-judge, `metrics.json`

Read `specs/COMMON.md`, `index.md`, chapters 00–07 first (cwd `/Users/sergii/.ai/knowledge/research_topics/training_and_self_evolution/tutorials/llm_training`).

## Problem
Chapters 09–10 fine-tune real models to a domain and must answer two questions with numbers:
"how good is it on the topic?" and "how much general ability did it lose?". This chapter builds
the measuring instruments once: (1) a general-capability suite with EleutherAI's
`lm-evaluation-harness` (`lm_eval` 0.4.12, installed via the `gpu` extra on rtx), for HF checkpoints
and for Ollama models via their OpenAI-compatible API; (2) a domain harness on CyberMetric
(4-option multiple choice, exact match); (3) an LLM-as-judge for open answers using the local
`qwen3.8:27b`; and (4) a fixed `metrics.json` schema. Baselines are measured for our 110M models and
for `Qwen/Qwen3.5-4B` (the model chapter 09 fine-tunes), so 09 can compare against them.

## Fix

### `project/src/llm_tutorial/eval_general.py` (Typer CLI, rtx)
Config `configs/eval_general.yaml`: `tasks: [mmlu, arc_challenge, hellaswag, winogrande, truthfulqa_mc2, gsm8k, ifeval]`, `limit: {mmlu: 20 per subject (use lm_eval's --limit semantics; document that limit applies per task/subtask), arc_challenge: 300, hellaswag: 300, winogrande: 300, truthfulqa_mc2: 200, gsm8k: 200, ifeval: 200}`, `num_fewshot: {mmlu: 5, gsm8k: 5, others: 0}`, `batch_size: auto`, `seed: 1234`.
- `run_hf(model_dir, out_dir, tasks=None, limit_scale=1.0)` → builds and runs `lm_eval --model hf --model_args pretrained=<dir>,dtype=bfloat16,trust_remote_code=False --tasks … --num_fewshot … --limit … --output_path <out_dir> --log_samples` per task group (subprocess; `lm_eval` CLI is the stable interface), then parses `results.json` into `{task: {metric: value, stderr}}`. For LoRA adapters: `peft=<adapter_dir>` model arg.
- `run_ollama(model_name, out_dir, base_url="http://127.0.0.1:11434/v1")` → `--model local-chat-completions --model_args model=<name>,base_url=…,num_concurrent=1,max_retries=3 --apply_chat_template` for generative tasks (gsm8k, ifeval) and `local-completions` for loglikelihood tasks only if the endpoint supports logprobs (Ollama's OpenAI `/v1/completions` does not return logprobs for scoring → document: with Ollama only generative tasks are possible; loglikelihood tasks need the HF path). Explain this clearly.
- `summarize(results) -> DataFrame` with one row per task and a `general_mean` (mean of the task primary metrics) → `runs/<run>/metrics.json` under key `general`.
- Wall-clock: measure and report. Keep the whole suite ≤ 45 min for a 4B model; if longer, reduce limits in the YAML and say so.

### `project/src/llm_tutorial/eval_domain.py` (Typer CLI)
- CyberMetric loader: download `CyberMetric-2000-v1.json`, `-500-v1.json`, `-10000-v1.json` from `https://huggingface.co/datasets/tihanyin/CyberMetric/resolve/main/…` (cache in `runs/data/cybermetric/`); inspect the JSON structure (`questions: [{question, answers: {A,B,C,D}, solution}]` — verify and adapt); `dedup_train(train10000, eval2000) -> list` removes any question whose normalised text appears in the eval set (report the count; tests cover it).
- `format_mcq(item, style="letter") -> str` prompt: question, four options `A) … D) …`, instruction "Answer with the letter only."; `parse_letter(text) -> str|None` (first standalone A–D, also handles "Answer: B" and "(C)").
- `evaluate_hf(model_dir, split="2000", batch_size=16, adapter=None, chat=True)`: greedy generation, `max_new_tokens 8`, with the chat template if the model is a chat model (Qwen3.5-4B: disable thinking via `enable_thinking=False` in `apply_chat_template`; document); accuracy, per-category accuracy if the JSON has categories, and a `loglik` mode option that scores the 4 letters by log-probability (more robust for small models — implement, it is ~20 lines) → `metrics.json` key `domain`.
- `evaluate_ollama(model_name, split)` same via `/api/chat` (`think: false`, `temperature 0`).
- Bootstrap 95 % confidence interval for accuracy (`ci95(correct: list[bool]) -> (lo, hi)`, pure, tested) — the chapter must explain why differences of 1–2 points on 500 questions are noise.

### `project/src/llm_tutorial/judge.py`
`judge(question, reference, candidate, model="qwen3.8:27b", url=OLLAMA_URL) -> {score 1-5, verdict, reason}` using `/api/chat` with `format` = JSON schema (as in the graph_rag tutorial: `think: false`, `temperature 0`); `judge_pairs(items)`; a small `configs/judge_set.yaml` of 20 open cybersecurity questions with reference answers (write them from CyberMetric-500 items rewritten as open questions; reference = the correct option text). Position-bias note: judge sees one candidate at a time, not pairs. Tests: prompt builder and JSON parsing with canned responses only (no network).

### `metrics.json` schema (document in the chapter, enforce with a Pydantic model `RunMetrics` in `config.py`): `{run_name, model, base, stage, created_at, train: {...}, general: {task: {metric, value, stderr}}, general_mean, domain: {dataset, split, n, accuracy, ci95, per_category}, judge: {n, mean_score}, cost: {wall_seconds, peak_gb}}`.

### Run for real (rtx; `just gpu-free` first for the 4B; the 110M runs and the Ollama-side judge need little memory)
Baselines table for the chapter: `tiny-qwen35-110m-{base,sft,dpo}` (general suite with the small limits — expect near-chance ≈ 25 % MMLU, ~30 % ARC; say so), `Qwen/Qwen3.5-4B` (HF, bf16, general suite + CyberMetric-2000 + judge set) and `qwen3.8:27b` via Ollama (generative tasks gsm8k/ifeval + CyberMetric-2000 + judge on its own answers is circular → skip judge for it). Record wall-clock for each. Save under `runs/eval_baselines/<model>/`.

### `project/tests/test_08_eval.py`
`parse_letter` on 8 strings; `format_mcq` contains all four options; `dedup_train` removes exact and whitespace/case-variant duplicates; `ci95` on 0/100 and 50/100; `RunMetrics` validation; lm_eval results parsing on a canned `results.json` (write a fixture); judge prompt/JSON parsing. No network.

### `justfile`: `eval-general model=…`, `eval-general-ollama name=…`, `eval-domain model=… split=…`, `eval-domain-ollama name=…`, `judge model=…`, `eval-baselines`.

### `08_evaluation.md` (chapter)
Why evaluation comes before fine-tuning; loglikelihood vs generative tasks (a diagram of how MMLU is scored by comparing 4 log-probs); each benchmark in one plain sentence (what MMLU/ARC/HellaSwag/WinoGrande/TruthfulQA/GSM8K/IFEval measure); `--limit` and confidence intervals (stderr from lm_eval, our bootstrap); running against an HF folder vs against Ollama and the logprobs limitation; the CyberMetric harness (a real item, the prompt, letter parsing, loglik mode, dedup count); LLM-as-judge (prompt, JSON schema, biases: position, verbosity, self-preference); the baselines table (real numbers, minutes per run); the `metrics.json` schema; Troubleshooting (`lm_eval` task names / `--tasks list`; never point `--model hf` at a GGUF file without `tokenizer=<hf id>` — HF tries to rebuild the tokenizer from the GGUF and can hang for hours (we evaluate GGUFs only through Ollama); OOM → `batch_size auto:4`; Ollama timeouts; thinking mode producing long outputs → `enable_thinking=False`/`think:false`; letter parsing failures); Exercises.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/llm_tutorial/{eval_general,eval_domain,judge}.py`, `project/src/llm_tutorial/config.py` (RunMetrics), `project/configs/{eval_general,judge_set}.yaml`, `project/tests/test_08_eval.py` (+ fixture), `project/justfile`, `project/runs/eval_baselines/**/metrics.json`, `08_evaluation.md`. Verify token `"What you will learn"`.

## Scope & constraints
No fine-tuning here. Do not change `index.md`. `Qwen/Qwen3.5-4B` (~8 GB) downloads to the HF cache on rtx only. Respect `gpu-free`.
