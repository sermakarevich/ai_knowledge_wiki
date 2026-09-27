# Task: chapter 03 — The model from scratch: instantiate, inspect, forward pass, loss, sanity checks, kernel check

Read `specs/COMMON.md`, `index.md`, chapters 00–02 first (cwd `/Users/sergii/.ai/knowledge/research_topics/training_and_self_evolution/tutorials/llm_training`).

## Problem
Chapter 01 built the model on the `meta` device to count parameters. Now we need a real,
randomly-initialised `tiny-qwen35-110m`, understand what one forward pass computes, verify the
loss at initialisation, prove the model can learn (overfit one batch), and decide — with a real
GPU benchmark — whether the hybrid architecture's fast kernels (`flash-linear-attention`) work on
the 4090 or whether we fall back to the dense `Qwen3Config` variant.

## Fix

### Extend `project/src/llm_tutorial/model.py`
- `build_model(model_section, device, dtype=torch.float32, tokenizer_dir=None)`: if a tokenizer dir is given, assert `vocab_size` matches `len(tokenizer)` (pad the config vocab up to a multiple of 64 if needed and explain why in the chapter). Set `pad_token_id`, `eos_token_id`, `bos_token_id` from the tokenizer.
- `init_weights_report(model)`: mean/std of embedding and a few linear layers (shows `initializer_range` 0.02).
- `count_params(model) -> dict(total, embedding, non_embedding)`.
- `expected_init_loss(vocab_size) = ln(vocab_size)`.
- `@torch.no_grad() generate_samples(model, tokenizer, prompts, max_new_tokens=40, temperature=0.8, top_p=0.95) -> list[str]` using `model.generate` (works for both archs; note Gated DeltaNet keeps a recurrent state instead of a KV cache).
- `save_checkpoint(model, tokenizer, run_dir/step) / load_checkpoint(path)` with `save_pretrained` (safetensors) — used by every later chapter.

### New `project/src/llm_tutorial/sanity.py` (Typer CLI)
- `init-loss config tokenizer_dir`: one forward pass on a batch of real tokens from `runs/data/tinystories/val.bin`, print loss vs `ln(V)` (expect 10.4–10.6 for V=32000).
- `overfit config tokenizer_dir --steps 200 --batch 4 --block 256`: AdamW lr 1e-3 on ONE fixed batch until loss < 0.1; print loss every 20 steps and the greedy re-generation of the memorised text. This is the classic "can it learn at all" test.
- `bench config --batch 16 --block 2048 --steps 8 [--compile]`: bf16 training steps on random tokens; print tokens/s, peak memory, and whether `fla` kernels were used (import `fla`; check `transformers.models.qwen3_5.modeling_qwen3_5` for its availability flag or catch the warning about the slow path). Run it for **four** variants and put the table in the chapter: hybrid eager, hybrid `torch.compile`, dense eager, dense compiled. If the hybrid model without `fla` is > 3× slower than dense, or `fla` fails to import, document it and set `configs/pretrain_fineweb.yaml`'s `model_config` (chapter 04 will read it) to the dense YAML; otherwise keep the hybrid. Write the decision and the numbers to `runs/bench_110m/metrics.json`.
  Reference numbers from a 2026-08-30 CPU check on the Mac: 41.9M test config init loss 10.48 vs ln(32000)=10.37, backward OK, no `fla` on macOS (slow path). On `rtx`, `uv pip install flash-linear-attention` succeeded with torch 2.13+cu130 in a scratch venv (`~/projects/_llm_check`, you may delete it) — the GPU numbers still have to be measured by you.
- All GPU commands go through `just gpu-free` first, then `just remote "python -m llm_tutorial.sanity …"` (each is < 5 minutes; foreground is OK).

### `project/tests/test_03_model.py`
Tiny config (2 layers, hidden 64, heads 4/2, head_dim 16, linear heads 4/2 dims 16, vocab 512, `full_attention_interval` 2): forward on random tokens gives finite loss within ±0.5 of ln(512); one AdamW step on a fixed batch decreases the loss; `generate_samples` returns strings of the right count; `save_checkpoint`/`load_checkpoint` round-trip (tmp_path) with identical logits; `count_params` keys. Same for the dense arch (parametrize).

### `justfile`
`sanity-init`, `sanity-overfit`, `bench config=…` (all remote, with `gpu-free` first).

### `03_model_from_scratch.md` (chapter)
What "random initialisation" means and the 0.02 std; module tree walkthrough of the 110M model (annotated real printout, ~60 lines); shapes through one forward pass (batch 2 × 256 tokens → embeddings [2,256,768] → … → logits [2,256,32000]) with a mermaid diagram; cross-entropy loss and why ln(V) is the starting point; the overfit-one-batch test with the real loss trajectory and the regurgitated text; the benchmark table and the kernel decision (explain what a fused kernel is and why linear attention needs a custom one); memory at batch 16×2048 vs the 24 GB; checkpoints in safetensors; Troubleshooting (`fla` import errors, CUDA OOM → smaller batch, `torch.compile` recompiles, vocab mismatch); Exercises.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/llm_tutorial/{model,sanity}.py`, `project/tests/test_03_model.py`, `project/justfile`, `project/runs/bench_110m/metrics.json`, `project/runs/sanity_*/…` (json/md), `project/configs/pretrain_fineweb.yaml` (only the `model_config:` key pointing to the chosen YAML plus a `# filled in chapter 04` comment), `03_model_from_scratch.md`. Verify token `"What you will learn"`.

## Scope & constraints
No full training loop yet (chapter 04). Do not change `index.md`. Respect the GPU rules; if the GPU is busy for hours, do the CPU parts, then wait (`gpu-free` retries) — do not skip the benchmark.
