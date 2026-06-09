# Mixture-of-Depths Attention

**Paper:** [Mixture-of-Depths Attention (Zhu et al., 2025)](https://arxiv.org/abs/2603.15619)

## Human Readable TL;DR

Imagine a deep building where workers on upper floors have to rely only on messages passed floor-by-floor from below -- by the time the message arrives at the 48th floor, important early details have been garbled or lost. This paper builds an elevator system (MoDA) that lets workers on any floor directly query archives from every previous floor using a smart search mechanism. The elevator is also cleverly engineered so it barely slows down the overall building operation, adding only a tiny cost while dramatically improving the quality of information available at every level.

## TL;DR

MoDA (Mixture-of-Depths Attention) extends standard self-attention to jointly attend over both sequence tokens and depth-stream KV pairs from all preceding layers in a single unified softmax operation. This directly combats information dilution in deep Transformers -- where residual stacking degrades shallow-layer features -- without the quadratic cost of DenseNet-style connections. On 700M–1.5B models, MoDA reduces validation perplexity uniformly across 10 domains and improves downstream task averages by 1.76–2.11%, while a hardware-aware Triton kernel achieves 97.3% of FlashAttention-2 efficiency.

---

## Problem & Motivation

Deep Transformers suffer from **information dilution**: shallower layers produce salient features that are progressively overwritten or attenuated by successive residual updates, making them inaccessible to later layers. Standard residual connections compress the entire depth history into a single hidden state. Dense cross-layer connections (DenseNet-style) preserve depth history but scale as O(T L² D²) -- prohibitively expensive for large LLMs. The paper asks: can we give each layer data-dependent, adaptive read access to all prior depth states, at minimal extra cost?

---

## Main Original Ideas

1. **Depth Stream as Attention Context** -- Frames Transformer block stacking as "read, operate, write" along a depth dimension, unifying depth residual, depth dense, and the new depth attention approaches in a single conceptual taxonomy.

2. **Unified Sequence + Depth Attention (MoDA)** -- Each attention head jointly attends to sequence KV pairs (standard self-attention) and depth KV pairs from *all preceding layers at the same token position*, normalized by a single shared softmax. No separate normalization or routing -- one operation retrieves both.

3. **Tiered Depth KV Projection Strategy** -- Three progressive variants: (a) reuse preceding layers' sequence KV at near-zero overhead; (b) add an Extra FFN KV Projection from the FFN input; (c) add Extra Attn KV Projection dedicated to depth. Ablations show (b) is the sweet spot; (c) saturates.

4. **Chunk- and Group-Aware Hardware Kernel** -- A custom Triton kernel reorganizes depth KV by query chunks (improving utilization from 1/T to 1/C) and by GQA groups (further to G/C), then fuses sequence and depth attention into a single online-softmax accumulator with no HBM intermediate writes. Total speedup over naive PyTorch: ~1458×.

---

## Key Findings

| Model | Config | Avg Downstream | C4 Val PPL | Train PPL |
|-------|--------|---------------|------------|-----------|
| OLMo2 baseline | 700M | -- | 15.61 | -- |
| MoDA (Depth KV only) | 700M | +1.17 pp | 15.50 | -0.41 |
| **MoDA + FFN KV Proj** | **700M** | **+1.94 pp** | **15.46** | **-0.59** |
| OLMo2 baseline | 1.5B | -- | 13.67 | -- |
| **MoDA + FFN KV Proj** | **1.5B** | **+2.11 pp** | **13.47** | -- |

- Gains are consistent across all 10 validation domains (no regression on any domain).
- Tasks improved include commonsense (HellaSwag, WinoGrande), reasoning (ARC-Challenge, SciQ), and broad knowledge (MMLU, BoolQ).
- MoDA outperforms an OLMo2 baseline with two *extra layers* (more params, more FLOPs) using fewer parameters and similar compute.
- Attention heatmaps confirm substantial, persistent probability mass on the Depth KV block in middle and late layers -- the model actively uses depth retrieval.
- MoDA partially breaks "attention sink" behavior (fixed mass on initial tokens), redistributing attention more broadly.

**Hardware efficiency ablation (at seq len 64K):**

| Optimization | Cumulative Speedup |
|---|---|
| Flash-compatible depth-KV layout | 162.5× |
| + Chunk-aware layout | ~316× |
| + Group-aware indexing | ~1458× |
| vs FlashAttention-2 | 97.3% efficiency |

---

## Suggestions & Future Directions

1. **Advanced CUDA engineering** -- Further optimize the MoDA kernel for industrial scale via improved memory scheduling, deeper compute pipelining, and overlap with distributed communication.
2. **Bounded depth-KV caching** -- In extremely deep networks, storing all historical depth-KV states becomes a memory bottleneck; future work should explore dynamic slot caching (utility-based or sliding-window eviction policies).
3. **Multimodal and vision extension** -- The depth-attention principle is architecture-agnostic; applying MoDA to visual, multimodal, and world-model Transformers is a natural next step.
4. **Deeper attention mechanism analysis** -- The observed reduction in attention-sink behavior from MoDA warrants further investigation to understand the mechanistic change in how the model routes information.

---

## Authors & Institutions

Lianghui Zhu (HUST / ByteDance Seed intern), Yuxin Fang (ByteDance Seed, Project Lead), Bencheng Liao (HUST / ByteDance Seed intern), Shijie Wang, Tianheng Cheng, Zilong Huang, Chen Chen, Lai Wei, Yutao Zeng, Ya Wang, Yi Lin, Yu Li (ByteDance Seed), Xinggang Wang (HUST, corresponding author)
