# Task: chapter 04 — Pre-training: the training loop, schedules, mixed precision, the real ~hours run, loss curves and samples

Read `specs/COMMON.md`, `index.md`, chapters 00–03 first (cwd `/Users/sergii/.ai/knowledge/research_topics/training_and_self_evolution/tutorials/llm_training`).

## Problem
We have data shards (02) and a model that can overfit one batch (03). Now we pre-train
`tiny-qwen35-110m` for real on FineWeb-Edu on the 4090, with a training loop the reader can read
end to end (no Trainer abstraction here — that comes with TRL in chapter 05), and produce the
loss/perplexity curves and sample generations that the rest of Part A builds on.

## Fix

### `project/src/llm_tutorial/pretrain.py` (Typer CLI, single-GPU, plain PyTorch)
Config `configs/pretrain_fineweb.yaml` (extend the file created in 03) with keys:
`run_name: pretrain_110m_fineweb`, `model_config`, `tokenizer_dir: runs/tokenizer_32k`,
`data_dir: runs/data/fineweb_edu`, `block_size: 2048`, `micro_batch: 16`, `grad_accum: 4`
(→ 131k tokens/step), `train_tokens: 1.5e9`, `lr: 6e-4`, `min_lr_ratio: 0.1`, `warmup_steps: 300`,
`schedule: cosine` (also implement `wsd` = warmup-stable-decay with `decay_fraction: 0.2`),
`weight_decay: 0.1` (no decay on norms/embeddings/biases), `betas: [0.9, 0.95]`, `grad_clip: 1.0`,
`dtype: bf16`, `compile: true`, `eval_every: 500`, `eval_tokens: 2e6`, `sample_every: 2000`,
`ckpt_every: 2000`, `keep_last: 2`, `seed: 1337`, `prompts: ["The capital of France is", "Photosynthesis is the process", "def fibonacci(n):", "Once upon a time"]`.
Also `configs/pretrain_tinystories_smoke.yaml` (same, `train_tokens: 5e7`, `micro_batch 32`, `block 512`, `eval_every 100`) — the 10-minute smoke run.

Loop (`train(config)`): build model + tokenizer (03), `PackedDataset.iter_batches` (02), fused AdamW
with two param groups, LR schedule function `lr_at(step)` (pure, tested), `torch.autocast(bfloat16)`,
gradient accumulation, `clip_grad_norm_`, `torch.compile` when enabled, logging every 10 steps
(step, loss, lr, grad-norm, tokens/s, peak GB, ETA) as one line, eval loss on `val.bin` every
`eval_every` (also report perplexity = exp(loss)), samples via `generate_samples` appended to
`runs/<run>/samples.md` with the step number, checkpoints via `save_checkpoint` into
`runs/<run>/checkpoints/step_XXXXXX` (+ optimizer state in `optim.pt`; keep `keep_last`), **resume**
from the latest checkpoint if `--resume`, and a final `runs/<run>/metrics.json` (config, total steps,
tokens seen, wall time, tokens/s mean, peak memory, final train/val loss and perplexity, MFU using
6·N·D/(time·165 TFLOP/s)). `runs/<run>/log.jsonl` with every logged step; `plot(run)` makes `loss.png`
(train + val loss vs tokens, log-x optional) with matplotlib (Agg backend).
Handle `KeyboardInterrupt`/SIGTERM by saving a checkpoint.

### Run for real on `rtx` (all via `just gpu-free` + `just remote-bg`)
1. Smoke: `just remote-bg smoke "python -m llm_tutorial.pretrain train configs/pretrain_tinystories_smoke.yaml"` → ~10 min; verify loss falls from ~10.4 to < 3 and samples become story-like.
2. Size the real run: from the smoke tokens/s (and 03's bench) compute hours for 1.5B tokens. **Budget rule: the run must finish in ≤ 6 hours.** If 1.5B tokens takes longer, lower `train_tokens` (never below 0.8B) and note the actual value in the chapter and in `index.md`'s dataset table (this is the one allowed `index.md` edit: replace "≈1.5B tokens (≈14 tokens per parameter…" with the real figure).
3. Real run: `just remote-bg pretrain "python -m llm_tutorial.pretrain train configs/pretrain_fineweb.yaml"`; poll with `just remote-log pretrain` every ~20 minutes (`sleep 1200` between polls — do not spin), `just remote-wait pretrain` at the end. If the tmux session died (OOM, ssh), `--resume`. Then `just remote "python -m llm_tutorial.pretrain plot runs/pretrain_110m_fineweb"` and `just pull`.
4. The final checkpoint path `runs/pretrain_110m_fineweb/checkpoints/final` is what chapters 05–08 load. Also copy it to `runs/models/tiny-qwen35-110m-base` on rtx (`save_pretrained` folder).

### `project/tests/test_04_pretrain.py`
`lr_at` (warmup linear to peak, cosine to `min_lr`, WSD plateau then decay — check 4 points each); param-group split (no weight decay on 1-D params); a 30-step CPU training run with the 2-layer test config on a synthetic shard dir (reuse 02's `write_shards`) ending with lower loss than at step 1, a checkpoint written, `metrics.json` and `log.jsonl` present; resume from that checkpoint continues at the right step. Keep the test under 60 s (block 32, batch 2, `compile: false`).

### `justfile`
`pretrain-smoke`, `pretrain`, `pretrain-log`, `pretrain-plot`.

### `04_pretraining.md` (chapter)
The loop in ~12 numbered lines of real code with commentary; AdamW and why β2=0.95 and weight decay 0.1 (and where Muon fits as the 2025–26 alternative — mention only); LR schedules (warmup, cosine vs WSD, with a small plot); why bf16 autocast and what stays in fp32; gradient accumulation = bigger batch for free; gradient clipping; `torch.compile`; checkpoints & resume; what tokens/s, memory and MFU we measured; the smoke-run curve; the real run: loss.png, table of (tokens, train loss, val loss, perplexity) at ~10 checkpoints, wall time, cost in kWh if you like (4090 ≈ 400 W); samples at step 0 / early / mid / final for the four prompts (verbatim); an honest paragraph on what 110M×1.5B tokens can and cannot do (compare to SmolLM-135M at 600B tokens); Troubleshooting (OOM → micro_batch; loss spikes → lower lr/clip; NaN in bf16; tmux died; slow data loading); Exercises (try WSD, change warmup, train the dense variant and compare).

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/llm_tutorial/pretrain.py`, `project/configs/pretrain_*.yaml`, `project/tests/test_04_pretrain.py`, `project/justfile`, `project/runs/pretrain_*/{metrics.json,samples.md,loss.png,log.jsonl}`, `04_pretraining.md`, and `index.md` only if the token budget changed. Verify token `"What you will learn"`.

## Scope & constraints
Single GPU, plain PyTorch — no DDP/FSDP, no Trainer. Do not start the real run while another training or an active Ollama client holds the GPU (`gpu-free` decides). Do not delete anything under `runs/data`.

## Addendum (from watching the real run)
The real run flattens: val loss 3.92 (step 1000) → 3.32 (5000) → 3.23 (7000) → 3.16 (9000) → 3.17 (10000) while lr decays 6e-4 → 8e-5. The chapter must have a short section "Why the curve flattens" that (a) shows the val table above (use the final numbers from `log.jsonl`), (b) explains the power-law/diminishing-returns shape, (c) points at the cosine tail (lr near `min_lr_ratio`) as the reason the last 10% is flat within noise (quote the step-to-step train-loss noise ±0.03), (d) states tokens/parameter for this run (≈14) vs Chinchilla 20 vs modern 100–1000× and that the remedy is more tokens, not more steps, (e) confirms health signals (grad_norm ≈ 0.24 steady, val tracks train, < 1 epoch so no overfitting). Exercises: continue training from the last checkpoint with a fresh WSD schedule on another 1B tokens and compare the final drop; halve `min_lr_ratio`.
