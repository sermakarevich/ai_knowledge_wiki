# Task: chapter 10 — Catastrophic forgetting: measure it, then reduce it (replay, lr/rank/epochs, self-distillation, model merging); final export to Ollama; production checklist

Read `specs/COMMON.md`, `index.md`, chapters 00–09 first (cwd `/Users/sergii/.ai/knowledge/research_topics/training_and_self_evolution/tutorials/llm_training`). Read `runs/ablation_4b/summary.json` — this chapter starts from what 09 measured.

## Problem
Chapter 09 showed the trade-off: domain accuracy up, some general benchmarks down (how much is in
`runs/ft_qwen35_4b_lora/metrics.json`). "Catastrophic forgetting" is the name for that loss. This
chapter turns the research of 2024–26 into recipes the reader can run on the 4B model, measures
each with the same instruments (08), picks the best, applies it to the 27B, exports the final
domain model to Ollama and ends with a production checklist. Every claim gets a number.

## Fix

### Recipes to implement and run on `Qwen/Qwen3.5-4B` (all via `finetune.py` configs; one GPU job at a time; domain eval on CyberMetric-2000, general suite from 08; results in `runs/forget/<variant>/metrics.json`)
1. **Reference points**: base (from 08) and 09's default LoRA run (aggressive variant from the ablation if it forgot the most — pick the run with the largest `general_mean` drop as the "forgetting baseline" and say why).
2. **Replay / data mixing**: `data.replay = {dataset: HuggingFaceTB/smoltalk, n: 2500|10000}` (≈ 25 % and ≈ 100 % of the domain set) — general instruction data mixed into training so the model keeps practising general behaviour.
3. **Gentler optimisation**: lr 2e-5, 1 epoch, r 8 (the "LoRA learns less and forgets less" regime — Biderman et al. 2024; and Thinking Machines' "LoRA Without Regret" 2025 finding that LoRA matches full fine-tuning when capacity is not the bottleneck and that lr should be ~10× full-FT lr).
4. **Attention-only targets** vs `all-linear` (from 09's ablation, reuse numbers).
5. **Self-distillation / on-policy data**: generate the *assistant answers* for the domain questions with the base model itself under a helpful prompt that includes the correct option ("the answer is B because …") → train on the model's own phrasing (`data.format: mcq_self_distill`; add a `distill(config)` command that writes `runs/data/cybermetric/train_selfdistill.json` with the base model's explanations, `max_new_tokens 160`, greedy, `enable_thinking=False`). Explain the intuition: staying close to the model's own distribution reduces forgetting (cite the 2025–26 self-distillation fine-tuning line of work in plain words; no exact numbers from papers unless verified).
6. **Model merging** with `mergekit` (install into the rtx venv: `uv pip install mergekit`; if it conflicts with transformers 5.16, implement TIES/linear merging of the *LoRA delta* directly with torch: `W = W_base + λ·ΔW` with λ ∈ {0.5, 0.75, 1.0} — "adapter scaling" — and document; also try merging two adapters (domain + a replay-trained one) with TIES via `peft`'s `add_weighted_adapter(combination_type="ties")` which needs no extra package). Evaluate each merged model.
7. Also record **domain perplexity** (mean NLL on the held-out CyberMetric-500 correct answers) and **general perplexity** on 200 SmolTalk eval conversations for base/each variant — a cheap continuous signal to complement accuracy (add `eval_domain.perplexity(model, texts)`).

Budget: ≤ 10 GPU-hours for the 4B variants (each ≈ 30 min train + ≈ 45 min eval; run general eval with 08's limits). Then one **27B** run with the winning recipe (QLoRA as in 09 + best mitigation), evaluated the same way (several hours).

### `project/src/llm_tutorial/forget.py` (Typer CLI)
`run_all(configs/forget_variants.yaml)` loops the variants (skips those with an existing `metrics.json`), `report()` builds `runs/forget/summary.json` and two plots: `tradeoff.png` (x = `general_mean` change vs base in points, y = domain accuracy change; one dot per variant, labelled) and `per_task.png` (grouped bars per general task for base / naive / best). `scale_adapter(adapter_dir, lam, out_dir)` and `ties_merge(...)` helpers (pure tensor maths, tested on tiny tensors).

### Final export
Take the best 4B variant (merged bf16 folder) → chapter 07's pipeline: GGUF bf16 → Q4_K_M and Q8_0 → `ollama create cyber-qwen35-4b` → CyberMetric-500 accuracy through Ollama (`eval_domain.evaluate_ollama`) vs the HF bf16 number (quantisation cost on a real task) → a chat transcript. For the 27B: if merging succeeded (09), export Q4_K_M as `cyber-qwen38-27b` and evaluate on -500 through Ollama; if not, explain the adapter-serving limitation (Ollama `ADAPTER` whitelist) and stop there. Note `ollama create` of a 27B GGUF needs ~60 GB disk for intermediates — check `df -h` first (555 GB free at the time of writing).

### `project/tests/test_10_forget.py`
`scale_adapter` maths on tiny tensors (λ=0.5 halves the delta), `ties_merge` on two hand-made deltas (sign election, trimming), `report()` on 3 fake metrics.json files (tmp_path) produces summary rows with the right deltas, self-distill example builder shape. No network.

### `justfile`: `forget-run`, `forget-report`, `distill`, `export-final`.

### `10_forgetting_and_merging.md` (chapter)
What forgetting is and why it happens (one intuitive paragraph + one about parameter interference); how to measure it properly (paired evaluation, same limits/seeds, CIs — refer to 08); the variants table (rows = variants, columns = domain acc, Δ general_mean, per-task deltas, train minutes) and `tradeoff.png`; a discussion of *what the data shows* for each recipe (be honest when a recipe did not help); the 27B result; the final exported Ollama model with its numbers; a decision guide ("if you need X, do Y") in ≤ 10 lines; a production checklist (data dedup vs eval, hold-out sets, eval before/after, versioning adapters, reproducibility: seeds/configs/`metrics.json`, quantisation check on the real task, template check, monitoring drift); Troubleshooting; Exercises (text2cypher as second domain; try replay ratio 50 %; try DPO on domain preferences).

Also append to `index.md` a final line under "Verified on" with the date and the two Ollama model names created (this is the one allowed `index.md` edit).

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/llm_tutorial/forget.py`, `project/configs/forget_variants.yaml`, `project/tests/test_10_forget.py`, `project/justfile`, `project/runs/forget/**/{metrics.json,summary.json,*.png,samples.md}`, `project/runs/export/**`, `10_forgetting_and_merging.md`, `index.md`. Verify token `"What you will learn"`.

## Scope & constraints
Do not rewrite `finetune.py`; extend via new config keys/functions only. Never delete other runs. Never touch Ollama's existing models. One GPU job at a time; poll every 20 minutes, do not spin.
