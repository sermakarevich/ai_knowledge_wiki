# Qwen3.8 Research Report (2026-08-30, live web research)

## 1. The Qwen3.8 family — exact repos, sizes, license

Qwen3.8 (Alibaba/Qwen team) has **only two members** — no small dense model in this generation:

| Model | HF repo | Type | Params | Released | License |
|---|---|---|---|---|---|
| Qwen3.8-27B | `Qwen/Qwen3.8-27B` (also `-FP8`) | Dense | 27B | 2026-08-13/14 | Apache-2.0 |
| Qwen3.8-2.4T-A95B | `Qwen/Qwen3.8-2.4T-A95B` (also `-FP8`) | MoE | 2.4T total / 95B active | 2026-08-12 | Custom "qwen3.8-max" license |

Community mirrors: `unsloth/Qwen3.8-27B`, `unsloth/Qwen3.8-27B-GGUF`, `unsloth/Qwen3.8-27B-NVFP4`.

No 0.5B–4B dense Qwen3.8 model exists. Small dense siblings:
- Qwen3.5: 0.8B, 2B, 4B, 9B, 27B (dense) + 35B-A3B/122B-A10B/397B-A17B (MoE) — Feb–Mar 2026
- Qwen3 (2025): 0.6B, 1.7B, 4B, 8B, 14B, 32B dense — Apache-2.0 (arXiv 2505.09388)
- Lineage: Qwen3 → Qwen3.5 → Qwen3.6 (35B-A3B MoE + 27B dense, Apr 2026) → Qwen3.8

## 2. Architecture (Qwen3.8-27B)

- **Hybrid attention** (introduced in Qwen3.5, reused in Qwen3.8): `16 × (3 × (Gated DeltaNet → FFN) → 1 × (Gated Attention → FFN))` = 64 layers, 3:1 linear-attention : full-attention.
  - Gated DeltaNet layers: 48 V heads, 16 QK heads, head-dim 128 (linear-recurrent attention).
  - Gated Attention layers: 24 Q heads, 4 KV heads, head-dim 256 (GQA 6:1). RoPE dimension 64.
- Hidden 5120, FFN intermediate 17,408 (SwiGLU — UNVERIFIED for 3.8 specifically, standard in Qwen family).
- Context 262,144 native, 1M via YaRN. Vocab (padded) 248,320. Tied embeddings: UNVERIFIED.
- RMSNorm / QK-norm: used in Qwen3/3.5; UNVERIFIED re-confirmation for 3.8.
- Natively multimodal (image + video).
- Thinking mode on by default; chat-template kwargs `enable_thinking`, `preserve_thinking`, `reasoning_effort` ∈ {low, medium, xhigh}; `/think` `/no_think` inline. Users report over-thinking at default xhigh.
- transformers architecture class: **`qwen3_5`** (per Unsloth docs); no separate `Qwen3_8Config`. Requires transformers v5 (exact pin UNVERIFIED). Comparable to `Qwen3NextConfig` hybrid model.
- Tiny random-init from config should work by transformers convention (`Qwen3_5Config(num_hidden_layers=2, ...)` + `AutoModelForCausalLM.from_config`) — not confirmed in a source.
- MoE sibling: 92 layers, hidden 8192, 512 experts, 11 active (10 routed + 1 shared), MTP in training.

## 3. Inference / export tooling

- llama.cpp `convert_hf_to_gguf.py`: works via recent builds (many community GGUFs incl. `unsloth/Qwen3.8-27B-GGUF`; gist with working llama.cpp config on a 4090). Official upstream support status for the hybrid arch murky; PR #27742 (Unsloth maintainer) added Qwen3.8-Flash-Next. Recommend building recent `master`. Exact release needed: UNVERIFIED.
- Ollama: `qwen3.8:27b` official (27.3B, Q4_K_M, ~18 GB incl. ~931 MB vision projector). Minimum Ollama version UNVERIFIED (recent 2026 build).
- Build Ollama model: Modelfile `FROM ./model.gguf`; `ollama create name -f Modelfile`. Chat template embedded in GGUF metadata by the converter; `TEMPLATE` overrides; `PARAMETER` for stop/num_ctx. `FROM <safetensors dir>` documented for supported archs.
- `ADAPTER` safetensors LoRA import documented only for Llama/Mistral/Mixtral/Gemma — Qwen3.8 hybrid likely unsupported. Safer: merge LoRA (`merge_and_unload()`) → convert to GGUF → `ollama create`.

## 4. Feasibility (24 GB RTX 4090)

- QLoRA (4-bit) on Qwen3.8-27B fits in 24 GB (Unsloth: "QLoRA works with 24GB and LoRA needs >36GB"). 4-bit weights ~14–19 GB; 24 GB is "the realistic floor". Unsloth 24 GB recipe: bs 1, grad-accum 4, max_seq_len 2048, LR 2e-4. Keep ≥75% reasoning-style examples in SFT mix to preserve thinking behaviour.
- 16-bit LoRA on 27B: >36 GB → not feasible. Full FT: out of reach.
- Small dense (Qwen3/3.5 0.6B–2B): full FT in bf16 on 24 GB feasible with grad checkpointing; 4B–9B: LoRA/QLoRA comfortable, full FT infeasible (rule of thumb).
- Mapping: Qwen3(.5)-4B → full FT/LoRA demo; 8B/9B → LoRA/QLoRA; Qwen3.8-27B → QLoRA-only capstone, seq ≤2048–4096.

## 5. Published training pipeline

Qwen3 (arXiv 2505.09388): ~36T tokens, 119 languages. Pretraining S1 general >30T @4K ctx; S2 knowledge-dense STEM/code/reasoning; S3 long-context extension. Post-training: GRPO on verifiable-reward reasoning, then broad RL (instruction following, agentic, preference). Small dense Qwen3 via strong-to-weak distillation.
Qwen3.8 README: "early fusion training on trillions of multimodal tokens", "reinforcement learning scaled across million-agent environments"; no quantified breakdown (UNVERIFIED details).

## Sources
- https://huggingface.co/Qwen/Qwen3.8-27B
- https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B
- https://huggingface.co/Qwen/Qwen3.8-27B-FP8
- https://ollama.com/library/qwen3.8:27b
- https://github.com/QwenLM/Qwen3.8
- https://github.com/ggml-org/llama.cpp/pull/27742
- https://huggingface.co/blog/mlabonne/qwen35
- https://unsloth.ai/docs/models/qwen3.8/train
- https://www.yottalabs.ai/post/how-to-run-qwen-3-8-27b-locally-ollama-gguf-single-gpu-2026
- https://www.yottalabs.ai/post/how-to-fine-tune-qwen-3-8-27b-with-unsloth-2026
- https://www.yottalabs.ai/post/qwen-3-8-27b-specs-hardware-requirements-how-to-run-2026
- https://www.runpod.io/blog/qwen3-8-27b-on-runpod-the-theory-behind-frontier-class-agentic-coding-that-fits-on-a-single-24gb-worker
- https://medium.com/ai-actually/fine-tune-a-27b-model-on-one-gpu-qlora-and-unsloth-explained-927ad5e382ae
- https://gist.github.com/ryan4yin/19db9fa44972c5735c1d181e8888d4fe
- https://docs.ollama.com/import
- https://github.com/ollama/ollama/issues/13314
- https://huggingface.co/docs/transformers/main/en/model_doc/qwen3_next
- arXiv:2505.09388 (Qwen3 Technical Report)
- https://qwenlm.github.io/blog/qwen3/
