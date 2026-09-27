# Task: chapter 09 — Domain fine-tuning of real models: Qwen3.5-4B LoRA and Qwen3.8-27B QLoRA on CyberMetric, domain vs general accuracy, ablations

Read `specs/COMMON.md`, `index.md`, chapters 00–08 first (cwd `/Users/sergii/.ai/knowledge/research_topics/training_and_self_evolution/tutorials/llm_training`).

## Problem
Part B starts here: take a pretrained instruct model and specialise it to a topic (cybersecurity,
CyberMetric multiple-choice knowledge) while measuring *both* domain accuracy and the general
benchmarks from chapter 08. Two models: `Qwen/Qwen3.5-4B` with LoRA (Low-Rank Adaptation) in bf16
— the fast iteration loop and the ablation vehicle — and `Qwen/Qwen3.8-27B` with QLoRA (base
weights quantised to 4-bit NF4 with bitsandbytes, LoRA adapters in bf16) as the capstone that
proves the 27B-class model can be fine-tuned inside 24 GB.

## Fix

### `project/src/llm_tutorial/finetune.py` (Typer CLI, rtx) — one generic LoRA/QLoRA SFT trainer
Config schema (`configs/ft_*.yaml`): `run_name`, `base` (HF id or dir), `quant: none|nf4`,
`lora: {r: 16, alpha: 32, dropout: 0.05, target_modules: all-linear | [q_proj,k_proj,v_proj,o_proj] | [gate_proj,up_proj,down_proj], modules_to_save: []}`,
`data: {train_file: runs/data/cybermetric/train_dedup.json, format: mcq_chat, n_train: null, replay: {dataset: null, n: 0}}` (replay is used in chapter 10 — implement the key now: mix `n` SmolTalk conversations into the training set),
`max_len: 1024`, `epochs: 2`, `lr: 1e-4`, `schedule: cosine`, `warmup_ratio: 0.03`, `per_device_batch: 8`, `grad_accum: 2`, `bf16: true`, `gradient_checkpointing: true`, `eval: {domain_split: "500", general: true|false}`, `seed`.
- `build_train_examples(items, tokenizer, style="mcq_chat")`: each CyberMetric item becomes a chat: user = `format_mcq(item)` (from 08), assistant = the letter + `) ` + option text (train the model to answer with the letter first, consistent with the eval parser). Pure, tested.
- `load_base(cfg)`: `AutoModelForCausalLM.from_pretrained(base, dtype=bfloat16, quantization_config=BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=bfloat16, bnb_4bit_use_double_quant=True) if nf4)`, `prepare_model_for_kbit_training`, `get_peft_model(LoraConfig(...))`; print trainable vs total parameters (chapter quotes it). The Qwen3.5 checkpoints are the multimodal `Qwen3_5ForConditionalGeneration`: load text-only if `AutoModelForCausalLM` supports it (transformers 5.16 maps `qwen3_5` → check), else load the full model and target only the language-model linear layers by regex (`target_modules=r".*language_model.*\.(q_proj|k_proj|v_proj|o_proj|gate_proj|up_proj|down_proj)"`; `all-linear` would also hit the vision tower — explain). Also handle the Gated DeltaNet layers' projections (`in_proj_qkv`, `in_proj_z`, `out_proj`, …): decide and document whether they are LoRA targets (default: yes for `all-linear`, no for the attention-only list).
- `train(config)`: TRL `SFTTrainer` with `assistant_only_loss` and the model's own chat template (`enable_thinking=False` when rendering: we want direct answers; document the trade-off with thinking mode), checkpoint per epoch, save the adapter to `runs/<run>/adapter`, `merge(run)` → `merge_and_unload()` in bf16 (for the 27B: reload base in bf16 on CPU (62 GB RAM is enough for 54 GB? — it is not with overhead; use `low_cpu_mem_usage` + `device_map="cpu"` and, if it fails, skip merging the 27B and keep the adapter; report), save to `runs/models/<run>-merged`), `metrics.json` (train loss curve, wall time, peak GB, trainable params).
- `eval(run)`: domain accuracy on CyberMetric-2000 (and -500) with `eval_domain.evaluate_hf(adapter=…)`, general suite via `eval_general.run_hf(peft=…)` (for the 27B QLoRA: `load_in_4bit=True` model args) — write into the same `metrics.json`. Also always evaluate the untouched base once (already in `runs/eval_baselines` from 08 — reuse, do not rerun).

### Runs (all `just gpu-free` + `remote-bg`, poll every 20 min)
1. `configs/ft_qwen35_4b_lora.yaml` (r 16, all-linear, lr 1e-4, 2 epochs, ~9.8k dedup'd training items). Expect ≈ 20–40 min training + ≈ 40 min eval.
2. Ablation on the 4B (each ≈ 30 min train + domain eval only on -500, plus general suite only for the two extremes): `lr ∈ {2e-5, 1e-4, 5e-4}`, `r ∈ {4, 16, 64}` at lr 1e-4, `epochs ∈ {1, 2, 4}`, `target_modules ∈ {attention-only, mlp-only, all-linear}`. That is ~9 runs; keep the table small and honest; use `configs/ablation_4b.yaml` listing the variants and a `ablate(config)` command that loops them and writes `runs/ablation_4b/summary.json` + `ablation.png` (domain accuracy vs general_mean scatter).
3. `configs/ft_qwen38_27b_qlora.yaml`: `quant: nf4`, r 16, attention + MLP linear layers, `max_len 1024`, `per_device_batch 1`, `grad_accum 8`, `gradient_checkpointing`, lr 1e-4, 1 epoch (Unsloth's 24 GB recipe: bs 1, ga 4, seq 2048, lr 2e-4 — we are slightly more conservative on memory). The 27B download is ~54 GB (bf16) → HF cache; loading in 4-bit takes minutes. Record peak memory; if it OOMs at 1024, go to 512 and document. Expect several hours including eval; that is fine — poll patiently. If Unsloth would be needed to fit, first try plain TRL+bitsandbytes; only if that fails at `max_len 512`, install `unsloth` in the rtx venv (`uv pip install unsloth`) and use `FastLanguageModel` with the same LoRA config, and document the switch.
4. Before/after generations for 6 prompts (3 cybersecurity open questions, 3 general — a poem, a Python function, a history question) for both models → `samples.md`; run the judge set from 08 on 4B base vs 4B fine-tuned.

### `project/tests/test_09_finetune.py`
`build_train_examples` on 3 synthetic items → messages with the letter-first assistant answer; config validation (Pydantic) rejects an unknown `quant`; LoRA on the 2-layer test model with `target_modules=["q_proj","v_proj"]` trains 3 steps on CPU and `merge_and_unload()` gives logits equal to the adapted model (tolerance 1e-4); the target-module regex matches expected names in a synthetic module list. No downloads.

### `justfile`: `ft config=…`, `ft-eval run=…`, `ft-merge run=…`, `ablate`, `ft-samples run=…`.

### `09_domain_finetuning.md` (chapter)
What LoRA is (diagram: W + B·A, r, α; parameters trained vs total — real numbers for 4B and 27B), why it is cheaper and how it changes what the model can learn — cite *LoRA Learns Less and Forgets Less* (Biderman 2024) and *LoRA Without Regret* (Thinking Machines 2025: all linear layers incl. MLP, lr ≈ 10× full-FT lr, moderate batch) as the reasons behind the defaults; QLoRA (NF4, double quantisation, compute dtype; memory table weights/adapters/optimizer/activations for the 27B at 1024 tokens — real peak GB); building the training set from CyberMetric (dedup count), the answer format decision; the 4B result table: base vs fine-tuned — domain accuracy (2000, CI) and each general task + `general_mean`, judge scores, before/after samples; the ablation table and scatter with 2–3 concrete lessons (e.g. higher lr → more domain gain, more general loss; attention-only vs MLP…) — whatever the data actually shows; the 27B QLoRA result table (base numbers from 08 via Ollama/HF vs fine-tuned) with wall time and memory; what "accuracy" did and did not capture; Troubleshooting (OOM at load → `max_len`, `device_map`; bitsandbytes CUDA errors; `all-linear` hitting the vision tower; thinking mode leaking `<think>` into answers; adapter/base version mismatch; merge OOM on CPU); Exercises (text2cypher-2025v1 as the alternative domain, pointer to the neo4j tutorial DB for `EXPLAIN` checks).

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/llm_tutorial/finetune.py`, `project/configs/{ft_qwen35_4b_lora,ft_qwen38_27b_qlora,ablation_4b}.yaml`, `project/tests/test_09_finetune.py`, `project/justfile`, `project/runs/{ft_*,ablation_4b}/**/{metrics.json,summary.json,*.png,samples.md}`, `09_domain_finetuning.md`. Verify token `"What you will learn"`.

## Scope & constraints
Do not change `index.md`, `eval_*.py` (extend only via new optional parameters if unavoidable). Only one GPU job at a time; the 27B run may take most of a day — that is expected, do not shorten it below 1 epoch. Adapters (~100–400 MB) stay on rtx.

Optional memory saver (try once on the 4B, keep if it works, document either way): `liger-kernel` is in the `gpu` extra; call `from liger_kernel.transformers import _apply_liger_kernel_to_instance` (or the model-specific `apply_liger_kernel_to_qwen3_5` if it exists in 0.8.2) before training and compare peak GB and step time with/without. Its fused linear-cross-entropy matters most for the 248k vocabulary. If it errors on the hybrid `qwen3_5` layers, note that and move on.
