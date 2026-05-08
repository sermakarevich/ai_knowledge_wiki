# Nemotron 3 Super: Open, Efficient Mixture-of-Experts Hybrid Mamba-Transformer Model for Agentic Reasoning

**Paper:** [Nemotron 3 Super (NVIDIA, 2025)](https://arxiv.org/abs/2604.12374)

## Human Readable TL;DR

Imagine you have a very smart assistant that can handle complex, multi-step tasks -- like fixing bugs in a real codebase or navigating a computer terminal -- but it also runs 7x faster and costs far less than comparable assistants. Nemotron 3 Super is NVIDIA's open-source AI model that achieves this by cleverly combining two efficiency tricks: routing each question only to the most relevant "specialist" brain cells (rather than using all of them), and replacing the expensive memory required to track long conversations with a more efficient rolling-summary approach. The result is a model that matches the best in the world on reasoning tasks while being dramatically cheaper to run.

## TL;DR

Nemotron 3 Super is a 120B total / 12B active parameter hybrid Mamba-Attention Mixture-of-Experts (MoE) LLM that achieves competitive accuracy with GPT-OSS-120B and Qwen3.5-122B while delivering up to 7.5x higher inference throughput. Key innovations include LatentMoE (hardware-aware expert routing in a reduced latent dimension), Multi-Token Prediction (MTP) for native speculative decoding, and NVFP4 pre-training on 25T tokens -- the first model at this scale trained end-to-end in 4-bit floating point. Post-training emphasizes agentic reasoning via multi-environment RLVR, SWE-RL, and PivotRL across 21 diverse environments.

---

## Problem & Motivation

Deploying frontier-scale LLMs (100B+ parameters) in real-world agentic applications faces two compounding problems: (1) the computational cost of inference is prohibitive at high throughput, driven by the quadratic complexity of self-attention's KV cache and dense expert utilization; (2) existing MoE architectures optimize for accuracy in isolation, ignoring hardware constraints like memory bandwidth and inter-chip communication latency. Additionally, the field lacked open models with strong multi-step tool-use, software engineering, and terminal-use capabilities trained with verifiable-reward RL at scale.

---

## Main Original Ideas

1. **LatentMoE** -- A hardware-aware MoE design that projects tokens from the full hidden dimension *d* into a smaller latent dimension *ℓ* before routing and expert computation. This reduces per-expert weight loads and communication payloads by *d/ℓ*, and the savings are reinvested to increase both the total number of experts (512) and active experts per token (top-22), achieving better accuracy per FLOP and per parameter simultaneously.

2. **Multi-Token Prediction (MTP) with Shared Weights** -- The model is trained to predict multiple future tokens at each position, with parameters shared across MTP heads. This simultaneously improves modeling quality (capturing multi-step dependencies) and enables native speculative decoding using the auxiliary heads as an internal draft model. Shared weights stabilize acceptance rates when the draft model conditions on its own generated states.

3. **NVFP4 Pre-training at Scale** -- First model pre-trained end-to-end in NVIDIA's NVFP4 (E2M1 element format, 16-element micro-blocks, E4M3 scaling factors) on 25 trillion tokens. Sensitive layers (final 15% of network, attention projections, embeddings) are kept in BF16/MXFP8. Demonstrates stable, accurate training at low precision, enabling reduced energy and hardware cost.

4. **Hybrid Mamba-Attention Architecture** -- 88 transformer layers with Mamba-2 blocks interleaved with sparse global self-attention "anchor" layers. Mamba handles linear-time sequence modeling (avoiding quadratic KV cache growth) while attention layers provide full-token interaction for long-range routing. Supports up to 1M token context with no positional embeddings.

5. **Multi-Stage Agentic Post-Training** -- A four-stage post-training pipeline: (1) SFT with expanded agentic datasets (SWE-Gym, terminal-use, tool-use, search, SQL, CUDA); (2) multi-environment RLVR across 21 tasks with a difficulty curriculum; (3) end-to-end SWE-RL using OpenHands agent loops and real GitHub tests; (4) PivotRL, an assistant-turn-level RL method that reuses offline SFT expert trajectories and focuses training only on "pivot" turns with policy uncertainty.

---

## Key Findings

### Inference Throughput vs. Accuracy (B200 GPUs, 8k input / 64k output)

| Model | Throughput vs. Nemotron 3 Super | Active Params |
|---|---|---|
| **Nemotron 3 Super** | **1.0x (baseline)** | **12B** |
| GPT-OSS-120B | 0.45x (2.2x slower) | ~120B |
| Qwen3.5-122B | 0.13x (7.5x slower) | ~122B |

### Base Model Benchmarks (selected)

| Benchmark | Nemotron 3 Super | Ling-flash-Base-2.0 | GLM-4.5-Air-Base |
|---|---|---|---|
| MMLU | **86.01** | 81.00 | -- |
| MATH | **84.84** | 63.80 | 50.36 |
| HumanEval | **79.40** | 70.10 | 76.30 |
| RULER @ 1M | **71.00** | N/A | N/A |

### MTP Speculative Decoding (SPEED-Bench, draft length 7)

| Model | Avg Acceptance Length |
|---|---|
| **Nemotron 3 Super** | **3.45** |
| Qwen3-Next | 3.33 |
| DeepSeek-R1 | 2.70 |

### Quantization Accuracy Retention

| Format | Median Accuracy vs. BF16 |
|---|---|
| FP8 (W8A8) | ~99.9% |
| NVFP4 (W4A4) | **99.8%** |

- Checkpoint merging during stable pre-training phase consistently yielded 2--4 point average improvement across 12 benchmarks.
- Training across 21 RLVR environments simultaneously prevented benchmark regressions while achieving stable gains.
- Mamba state cache quantization using FP16 + stochastic rounding (Philox pseudorandom) matched FP32 baseline quality.

---

## Suggestions & Future Directions

1. **Broader low-precision adoption** -- The NVFP4 pre-training recipe should generalize to other architectures; further exploration of ultra-low-precision training across diverse model families is warranted.
2. **Scaling agentic RL environments** -- The 21-environment RLVR setup showed strong results; expanding to more diverse real-world agentic domains (scientific, financial, robotic) is a natural next step.
3. **MTP depth scaling** -- Increasing draft depth continued to shift the throughput-latency Pareto frontier positively; exploring optimal MTP depth and head sharing strategies is ongoing.
4. **Mamba state quantization robustness** -- Stochastic rounding provided a practical fix for recurrent state quantization drift; more principled approaches to managing error accumulation in SSM states deserve further study.
5. **Long-context RL** -- The model supports 1M context, but RL training for tasks requiring very long-horizon context remains computationally challenging and underexplored.
6. **Open-source community leverage** -- The authors release base, post-trained, and quantized checkpoints with full training recipes, encouraging the community to build on and extend the approach.

---

## Authors & Institutions

Large collaborative team at **NVIDIA** (full author list in paper). Key areas: model architecture, pre-training infrastructure, post-training/RL, quantization, and safety.
