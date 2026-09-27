# Task: chapter 04 — positional encoding: sinusoidal, RoPE, partial RoPE, context extension

Read `specs/COMMON.md`, `index.md`, `00_setup.md`, `03_attention.md` (cwd `/Users/sergii/.ai/knowledge/research_topics/llm_theory_and_multimodal/tutorials/llm_blocks`).

## Code — `src/llm_blocks/ch04_positional_encoding.py`
- `sinusoidal_pe(seq, d)` (Vaswani 2017) from scratch.
- `rope_cos_sin(seq, head_dim, theta=10000.0)` and `apply_rope(x, cos, sin)` from scratch using the rotate-half convention used by transformers — test against `transformers.models.qwen3.modeling_qwen3.Qwen3RotaryEmbedding` + `apply_rotary_pos_emb` (find the exact 5.16 import paths; document them).
- `partial_rope(x, cos, sin, rotary_frac=0.25)` — rotate only the first `rotary_frac` of head dim (Qwen3.5/3.8: `partial_rotary_factor 0.25` — verify in `Qwen3_5TextConfig`; quote the real attribute name).
- `permutation_test(model_fn)`: show attention output without positions is permutation-equivariant (shuffle tokens → shuffled output) and with RoPE it is not.
- `plots`: `04_sinusoidal.png` (heat-map of the sinusoidal table 64 positions × 64 dims + two dimension curves), `04_rope_rotation.png` (a 2-D pair rotated by position angle for 3 frequencies — show the same vector at positions 0…7 as arrows on unit circles), `04_rope_relative.png` (dot product of q at position 0 with k at positions 0…512 after RoPE, averaged over random vectors, showing decay with relative distance; plus the same for two absolute offsets to show it depends only on the difference), `04_frequencies.png` (wavelength per dimension pair for theta 10k vs 1M — Qwen uses a large theta; read `rope_theta` from the 0.8B config and annotate), `04_partial_rope.png` (which dims are rotated for head dim 256 with factor 0.25), `04_context_extension.png` (attention score vs distance for a model "trained to 4k" evaluated at 16k, with and without a YaRN/NTK-style frequency rescale — a toy illustration; label as illustration).
- `demo`: prints the permutation test result and config values.

## Chapter — `04_positional_encoding.md`
Why attention is blind to order (bag of words; the permutation demo numbers); option 1: add a position vector (sinusoidal figure, why sines: smooth, unique, generalise); option 2: RoPE (rotary position embedding) = rotate q and k by an angle proportional to position, so the dot product depends only on the *distance* between tokens (rotation figure → relative figure; the complex-number view in two sentences); frequencies: low dims turn fast (local), high dims slowly (global); `rope_theta` and long context; partial RoPE in Qwen3.5/3.8 (only a quarter of each head is rotated — the rest is position-free; intuition: keep some "pure content" channels; verify the config); extending context after training (YaRN = "yet another RoPE extension"; the interpolation figure; Qwen3.8 262k native, 1M with YaRN — from the model card); Gated DeltaNet layers do not use RoPE (they carry position through recurrence — preview of ch. 07); Troubleshooting (rotate-half vs interleaved convention mismatch; cos/sin dtype; position ids offset in KV-cached decoding); Exercises.

## Scope limits
No `index.md` edits. Keep the YaRN part as intuition + one toy figure; do not implement YaRN exactly.
