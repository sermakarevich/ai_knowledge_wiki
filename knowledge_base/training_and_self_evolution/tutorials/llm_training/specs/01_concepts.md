# Task: chapter 01 — Concepts: what an LLM is, the Qwen3.5/3.8 architecture piece by piece, the modern training pipeline, the compute budget

Read `specs/COMMON.md`, `index.md` and `00_setup.md` first (cwd `/Users/sergii/.ai/knowledge/research_topics/training_and_self_evolution/tutorials/llm_training`).

## Problem
Before touching data or training loops the reader must understand (a) what the model computes,
(b) what every component of the Qwen3.5/Qwen3.8 architecture does and how big it is, (c) which
stages modern training consists of and what each stage changes, and (d) why 27B from scratch is
out of reach on one GPU while 110M is fine. This chapter is mostly prose + small verified code.

## Fix

### `project/src/llm_tutorial/anatomy.py` (Typer CLI, CPU only)
- `describe(config_path)`: build a model from a YAML config with `Qwen3_5TextConfig` on the
  `meta` device (`with torch.device("meta")`), print a `rich` table per layer type — module name,
  shape, parameter count — plus totals: embedding vs non-embedding parameters, and the
  `layer_types` pattern. Support `--from-hub Qwen/Qwen3.8-27B` (only downloads `config.json` via
  `AutoConfig.from_pretrained`, no weights; use `.text_config` when the config is the multimodal
  wrapper `Qwen3_5Config`) to print the same table for the real 27B and 4B and 0.8B models.
- `budget(params, tokens, tflops=165, mfu=0.4)`: prints training FLOPs = 6·N·D, and the time on
  one 4090 at the given MFU (Model FLOPs Utilisation = fraction of peak actually achieved), for
  a table of (model, tokens) pairs; used to produce the "why not 27B from scratch" table.
- Verified facts to use (from `Qwen/Qwen3.8-27B/config.json`, fetched 2026-08-30): 64 layers,
  `layer_types` = 3×linear_attention then 1×full_attention repeated (`full_attention_interval` 4),
  hidden 5120, intermediate 17408, `hidden_act` silu (SwiGLU), 24 attention heads / 4 KV heads,
  `head_dim` 256, `partial_rotary_factor` 0.25 (RoPE applied to a quarter of head dims),
  `rope_theta` 1e7, `attn_output_gate` true (the "gated" in Gated Attention), linear-attention
  layers: 48 value heads, 16 key heads, head dims 128, `linear_conv_kernel_dim` 4,
  `output_gate_type` swish, `mtp_num_hidden_layers` 1 (a Multi-Token-Prediction head used in
  training), vocab 248320, `tie_word_embeddings` false, `max_position_embeddings` 262144,
  `rms_norm_eps` 1e-6. Qwen3.5-4B: hidden 2560, 32 layers, 16/4 heads, tied embeddings.
  Qwen3.5-0.8B: hidden 1024, 24 layers, 8/2 heads, tied embeddings.

### `project/configs/tiny_qwen35_110m.yaml`
```yaml
model:
  arch: qwen3_5            # Qwen3_5TextConfig
  vocab_size: 32000
  hidden_size: 768
  intermediate_size: 2048
  num_hidden_layers: 12
  num_attention_heads: 12
  num_key_value_heads: 2
  head_dim: 64
  linear_num_value_heads: 12
  linear_num_key_heads: 6
  linear_key_head_dim: 64
  linear_value_head_dim: 64
  full_attention_interval: 4
  tie_word_embeddings: true
  max_position_embeddings: 2048
  rms_norm_eps: 1.0e-6
```
(verified: 108.6M parameters, 84.0M non-embedding, 24.6M embedding). Also add
`configs/tiny_qwen3_110m_dense.yaml` (same but `arch: qwen3`, plain `Qwen3Config`, no `linear_*`
keys) as the fallback used if the hybrid kernels are unavailable. Add `llm_tutorial.model.build_model(cfg_dict)` → returns `(model, hf_config)` for either arch (this module is extended in chapter 03; keep it minimal here: `build_config(model_section) -> PretrainedConfig`, `build_model(model_section, device="cpu")`).

### `01_concepts.md` (chapter) — sections
1. What an LLM does: next-token prediction, tokens, probabilities, sampling (temperature/top-p) — one short worked example.
2. The Qwen3.5/3.8 architecture, one subsection per component, each with "what it is / why it exists / how many parameters": token embeddings; RMSNorm (Root Mean Square normalisation) and pre-norm; RoPE (Rotary Position Embedding) and partial rotary; **Gated Attention** with GQA (Grouped-Query Attention: 24 query heads share 4 key/value heads → smaller KV cache), QK-norm, the output gate; **Gated DeltaNet** linear attention (a recurrent state instead of a growing KV cache — explain intuitively as "a fixed-size memory updated each token with a delta rule", why 3 of every 4 layers use it: long context at constant memory), the short causal conv; SwiGLU MLP; tied vs untied LM head; the residual stream. Include the module printout of our 110M model from `anatomy.describe` and the parameter table for 27B/4B/0.8B/110M side by side. Mermaid diagram of one decoder block pair (linear-attention block + full-attention block).
3. Thinking mode and the chat template (what `<think>` blocks are, `enable_thinking`, `reasoning_effort`) — two paragraphs, details come in chapter 05.
4. The modern training pipeline as a mermaid flowchart with one paragraph per stage: pre-training (stage 1 general web, stage 2 knowledge-dense STEM/code, stage 3 long-context; Qwen3 used ~36T tokens); mid-training/annealing; SFT (Supervised Fine-Tuning); preference optimisation (DPO — Direct Preference Optimization, and relatives); RL with verifiable rewards (GRPO — Group Relative Policy Optimization; DAPO/GSPO as refinements); distillation of small models from big ones; what Qwen published for Qwen3 (arXiv 2505.09388) vs the qualitative statements for Qwen3.8 ("early fusion multimodal training", "RL across million-agent environments"). Map each stage to the chapter that reproduces it.
5. Compute and memory budget: 6·N·D; the `budget` table (27B×36T, 27B×1T, 4B×1T, 110M×1.5B) with hours/years on one 4090 at 40 % MFU; training memory = weights + gradients + Adam states (≈16 bytes/param in mixed precision) + activations, with numbers for 110M, 4B, 27B; what LoRA (Low-Rank Adaptation: train small added matrices, freeze the base) and QLoRA (base weights in 4-bit) change — the 27B QLoRA ≈ 15–19 GB base fits 24 GB, 16-bit LoRA does not (> 36 GB).
6. Troubleshooting (conceptual FAQ table is fine here), Exercises (e.g. compute the KV-cache size per token for 27B at 4 KV heads × 256 dims × 16 full-attention layers).

Keep every number traceable to a command in this chapter or to the cited config/report. Use simple language; every abbreviation expanded on first use.

### `project/tests/test_01_anatomy.py`
Build the 110M config from the YAML via `build_model` (CPU, real weights) and assert total params
between 108.0M and 109.2M, embedding params == 32000*768, `layer_types` has 12 entries with
`full_attention` at indices 3, 7, 11. Build the dense fallback and assert it is a `Qwen3ForCausalLM`.
Test `budget()` maths for one pair (pure function). No downloads in tests.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/llm_tutorial/{anatomy,model}.py`, `project/configs/tiny_qwen35_110m.yaml`, `project/configs/tiny_qwen3_110m_dense.yaml`, `project/tests/test_01_anatomy.py`, `project/justfile` (new recipes `anatomy config=…`, `budget`), `01_concepts.md`. Verify token `"What you will learn"` in `01_concepts.md`.

## Scope & constraints
Prose-heavy chapter; do not implement data loading or training here. Do not change `index.md`.
`anatomy --from-hub` needs the network (Mac is fine, it is a 10 kB config download) — run it once for real and paste the output; do not put it in tests.
