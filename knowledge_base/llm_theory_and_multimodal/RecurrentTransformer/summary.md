# The Recurrent Transformer: Greater Effective Depth and Efficient Decoding

**Paper:** [The Recurrent Transformer: Greater Effective Depth and Efficient Decoding (Oncescu et al., 2026)](https://arxiv.org/abs/2604.21215)

## Human Readable TL;DR

Imagine a skyscraper where each floor can only talk to the floor directly below it -- that's how regular AI language models work, with information passing up one floor at a time. This paper builds a smarter skyscraper where each floor also has a "memory wall" that holds notes written by everyone who passed through before, letting the floor see patterns it would otherwise miss. The result is a building that works just as well with fewer floors, saving space and running faster when answering questions. The key engineering trick is a clever scheduling system that makes building this memory wall no more expensive than the old design.

## TL;DR

The Recurrent Transformer (RT) modifies each Transformer layer so that key-value pairs are computed from the layer's own output activations rather than only its inputs, creating layerwise recurrent memory within each layer. This increases effective temporal depth -- the number of iterative computation steps information can undergo -- without unbounded state or RNN-style gradient instability. RT matches or outperforms parameter-matched Transformer baselines on C4 language modeling (300M params: 2.860 vs. 2.892 CE loss) using fewer layers, shrinking the KV cache footprint at inference. A tiling algorithm reduces training HBM traffic from O(N²) to O(N log N).

---

## Problem & Motivation

Standard Transformers are **temporally shallow**: at layer ℓ, token *i* attends only to KV pairs derived from layer ℓ-1 outputs. This bounds effective depth to the number of stacked layers. Recurrent models offer unbounded temporal depth but suffer from vanishing/exploding gradients and sequential computation that underutilizes modern accelerators. The gap motivates an architecture that captures iterative, recurrent computation within layers while retaining Transformer-style parallel training and stable gradients.

---

## Main Original Ideas

1. **Layerwise Recurrent Memory** -- Each Transformer layer maintains *persistent* KV pairs computed from its own output activations *z_i*, which accumulate across positions within the layer. Later tokens in the same layer can attend to these pairs, enabling within-layer iterative computation. A separate set of *temporary* KV pairs (from the layer input) resolves the circular dependency at the current position.

2. **Parameter-Free Recurrence** -- The same Q/K/V projection matrices are reused for both temporary and persistent KV computation, so RT adds no extra parameters over a standard Transformer of the same width and depth.

3. **O(N log N) Tiling Algorithm** -- A Flash-Inference-inspired tiling strategy reorders computation: once persistent KV pair *(k_t, v_t)* is available, its contribution is immediately aggregated across a block of future queries using online softmax statistics, reducing HBM traffic from O(N²) to O(N log N) and raising arithmetic intensity from Θ(1) to Θ(N/log N).

4. **Depth--Width Trade-off Shift** -- Because each layer is more computationally expressive, RT achieves competitive quality with fewer layers for a fixed parameter budget (width scales up to compensate). Fewer layers → smaller KV cache at inference → lower memory traffic → higher autoregressive throughput.

5. **Stability via RMSNorm + Residual Scaling** -- Applying RMSNorm before computing persistent KV pairs, combined with standard 1/√L residual scaling, prevents exploding gradients while retaining long-range access through direct one-hop attention paths.

---

## Key Findings

| Model | Layers | Params | Val CE (C4, 300M) |
|---|---|---|---|
| Transformer | 24 | 300M | 2.892 |
| Transformer | 12 | 300M | 2.896 |
| RT | 12 | 300M | 2.867 |
| **RT** | **6** | **300M** | **2.860** |

- RT 6-layer (wider) outperforms 24-layer Transformer baseline at equal parameter count.
- Same trend at 150M parameters: RT 6-layer achieves 3.049 CE vs. Transformer 6-layer 3.097.
- RT consistently outperforms standard Transformers on synthetic tasks: In Context Recall, Fuzzy/Noisy In Context Recall, Selective Copying, and Copy.
- The exact tiling algorithm achieves near-linear forward-pass latency scaling vs. approximately quadratic for naive recurrent implementation.
- CUDA Graphs reduce per-layer forward latency by ~7x at batch size 32 (277ms → 38.85ms).
- Ablation: removing RMSNorm before persistent KV computation causes significant loss degradation and instability at higher learning rates.
- KV cache size reduction scales as √α when layers are reduced by factor α (width compensated), directly improving inference memory efficiency.

---

## Suggestions & Future Directions

1. **Scaling law exploration** -- Investigate how layerwise recurrence interacts with existing Transformer scaling laws and whether the favorable depth-width trade-off persists at larger scales.
2. **Inference throughput benchmarks** -- Empirically measure autoregressive decoding throughput gains from reduced KV cache, especially in bandwidth-limited deployment scenarios.
3. **Hybrid architectures** -- Explore mixing RT layers with standard Transformer layers to balance parallelism and recurrent depth.
4. **Sparse or bounded recurrence** -- Study whether restricting the recurrent attention window (e.g., attending to only recent persistent KV pairs) can further improve efficiency without sacrificing quality.
5. **Alternative stability mechanisms** -- The current stability analysis is simplified; deeper theoretical work on gradient dynamics in layerwise recurrent attention could guide more principled design choices.

---

## Authors & Institutions

Costin-Andrei Oncescu, Depen Morwani, Samy Jelassi, Alexandru Meterez, Mujin Kwun, Sham Kakade -- Harvard University
