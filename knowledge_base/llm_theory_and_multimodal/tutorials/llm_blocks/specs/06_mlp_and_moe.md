# Task: chapter 06 — the MLP block (SwiGLU) and Mixture of Experts

Read `specs/COMMON.md`, `index.md`, `00_setup.md`, `01_*.md`, `05_*.md` (cwd `/Users/sergii/.ai/knowledge/research_topics/llm_theory_and_multimodal/tutorials/llm_blocks`).

## Code — `src/llm_blocks/ch06_mlp_moe.py`
- `SwiGLUMLP(d_model, d_ff)` from scratch: `down(silu(gate(x)) * up(x))` — test vs `transformers` `Qwen3MLP` (tiny `Qwen3Config`) with copied weights.
- `KeyValueMemoryDemo`: fit a 1-layer MLP on a tiny lookup task (50 "keys" → "values") to show neurons act as key detectors; record which hidden units fire for which inputs.
- `TopKRouter(d_model, n_experts, k)` and `MoELayer(d_model, d_ff, n_experts, k, shared_expert=True)` from scratch (softmax router → top-k → weighted sum of expert MLPs; optional always-on shared expert as in Qwen3-MoE/Qwen3.8-MoE); `load_balancing_loss(router_probs, expert_indices)` (Switch-Transformer style); test `MoELayer` vs a dense `SwiGLUMLP` when `n_experts=1, k=1` (equal) and vs `transformers` `Qwen3MoeSparseMoeBlock` (tiny `Qwen3MoeConfig`, copied weights) if the class is importable in 5.16 — else document.
- `param_breakdown(config)`: parameters per block type for a text config (embeddings, attention layers, DeltaNet layers, MLP, norms, LM head) — use `Qwen3_5TextConfig` defaults for the 27B (verify with `AutoConfig.from_pretrained("Qwen/Qwen3.8-27B")` — config download only, no weights; if network is off, fall back to the 0.8B) and the 0.8B.
- `plots`: `06_swiglu_schematic.png` (gate/up/down with shapes for hidden 5120 → 17408 → 5120), `06_gate_behaviour.png` (silu(gate)·up as a 2-D surface or a set of curves showing the "volume knob"), `06_kv_memory.png` (hidden-unit activation matrix from the memory demo: rows = inputs, cols = neurons, showing sparse selective firing), `06_param_pie.png` (two pies: 27B and 0.8B parameter share per block type — real numbers from `param_breakdown`), `06_moe_schematic.png` (router → top-2 of 8 experts + shared expert), `06_expert_usage.png` (histogram of expert usage over 4096 random tokens with and without the balancing loss after a short toy training — shows collapse vs balance), `06_moe_cost.png` (active vs total parameters for dense 27B vs Qwen3.8-2.4T-A95B (2.4T total / 95B active — from the model card) as a bar chart, log-y).
- `demo`: prints the parameter table.

## Chapter — `06_mlp_and_moe.md`
What the MLP (multi-layer perceptron / feed-forward block) does per token (no mixing between tokens — that was attention's job); the "key–value memory" intuition (Geva et al. 2021, one sentence) with the firing figure; SwiGLU (SiLU-gated linear unit): three matrices, the gate as a volume knob (figure), the 5120→17408 shape and why ~⅔ of a 27B's parameters live in MLPs (pie figure — quote the real share); MoE (Mixture of Experts): many MLPs, a router picks k per token; total vs active parameters (Qwen3.8-2.4T-A95B: 512 experts, 10 routed + 1 shared active — from the model card, mark as reported); load balancing and why it is needed (usage figure); why MoE is cheaper to run but not to store (cost figure; single-GPU relevance: the 27B dense fits, the MoE does not); Troubleshooting (shapes, `top_k` gradient flow through weights only, expert collapse); Exercises.

## Scope limits
No `index.md` edits. Config download only; no MoE weights.
