# Task: chapter 05 — normalization and the residual stream

Read `specs/COMMON.md`, `index.md`, `00_setup.md`, `01_*.md` (cwd `/Users/sergii/.ai/knowledge/research_topics/llm_theory_and_multimodal/tutorials/llm_blocks`).

## Code — `src/llm_blocks/ch05_norm_residual.py`
- `LayerNorm` and `RMSNorm` from scratch (RMSNorm: `x / sqrt(mean(x²) + eps) * weight`; Qwen variant uses `(1 + weight)`? — check `Qwen3_5RMSNorm` in transformers 5.16 and implement both `weight` and `1 + weight` conventions; document which Qwen3 vs Qwen3.5 uses). Tests vs `torch.nn.LayerNorm`, `torch.nn.RMSNorm`, and `Qwen3RMSNorm` / `Qwen3_5RMSNorm` with copied weights.
- `Block(pre_norm: bool)`: `x + f(norm(x))` vs `norm(x + f(x))`, where `f` is a tiny MLP; `stack_stats(depth, pre_norm, use_norm)`: run random input through 32 stacked blocks and record per-layer activation std, residual-stream norm and gradient norm at the input (backprop of a dummy loss).
- `plots`: `05_layernorm_vs_rmsnorm.png` (a 16-dim vector before/after each), `05_residual_highway.png` (schematic: the residual stream as a horizontal highway with attention/MLP "on-ramps" adding to it — matplotlib patches), `05_depth_stats.png` (3 panels vs layer index: activation std, residual norm, gradient norm — lines for pre-norm, post-norm, no-norm; log-y), `05_no_norm_training.png` (train a 12-layer toy MLP stack on the moons data from ch. 01 with and without RMSNorm, lr 0.1: loss curves; show the no-norm run diverging or stalling — pick an lr where it does), `05_residual_contributions.png` (for the pre-norm stack: how much each layer adds to the residual norm, bar chart).
- `demo`: prints the numbers quoted.

## Chapter — `05_normalization_and_residuals.md`
Why deep nets are hard to train (signals shrink/explode across layers — the depth-stats figure); normalization as "re-centre and re-scale before each block" (LayerNorm vs RMSNorm: RMSNorm drops the mean, cheaper, used by Llama/Qwen; the vector figure; the learnable scale); pre-norm vs post-norm and why modern LLMs are pre-norm (stability; the figure); the residual stream as a highway/shared whiteboard that every block reads from and writes to (schematic + contributions figure) — this is *the* mental model for the rest of the tutorial; where norms sit in a Qwen3.5 layer (input norm → attention/DeltaNet → residual add → post-attention norm → MLP → residual add; final norm before the LM head; plus the QK-norm inside attention from ch. 03 and the norm inside Gated DeltaNet's output — verify in the source and draw a small Mermaid diagram); eps and dtype details (norm computed in fp32 even in bf16 models — check the transformers code); the no-norm training demo; Troubleshooting; Exercises.

## Scope limits
No `index.md` edits.
