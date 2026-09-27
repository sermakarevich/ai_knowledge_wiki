# FlashLib: Bringing Flash Magic to Classical Machine Learning Operators

**Paper:** [FlashLib: Bringing Flash Magic to Classical Machine Learning Operators (Yang et al., 2025)](https://flashml-org.github.io/)

## Human Readable TL;DR

Imagine your car's GPS and navigation tools were designed for leisurely road trips, but now you need them to react in milliseconds for a self-driving car. That's the problem FlashLib solves for AI systems. Old-school data analysis tools (like clustering and search) were built for slow, bulk processing -- but modern AI agents need these same tools to run near-instantly. FlashLib rebuilds these tools from scratch for modern graphics cards, making them up to 208x faster, so AI agents can use them as real-time building blocks rather than slow batch jobs.

## TL;DR

FlashLib is a GPU-accelerated library that rewrites classical ML operators (KMeans, KNN, PCA, t-SNE, HDBSCAN, etc.) as low-latency online primitives for agentic AI pipelines. It achieves massive speedups over NVIDIA's cuML through algorithmic reformulation into GPU-friendly forms, hardware-aware kernel variants, tolerance-driven dispatch, and CPU-side cost prediction. Benchmarked across 194 workload configurations on H200 GPUs, 193/194 show equivalent or superior performance, with 126 achieving 5x+ speedups.

---

## Problem & Motivation

Classical ML operators (clustering, retrieval, dimensionality reduction, linear algebra) were designed for offline, batch-latency workloads measured in minutes to hours. The rise of agentic AI systems -- where LLM controllers orchestrate these primitives in real-time feedback loops -- has compressed latency requirements to milliseconds. NVIDIA's cuML and similar libraries were not designed for this regime: they lack low-latency dispatch paths, transparent cost modeling, or precision-performance tradeoff controls needed for agent-in-the-loop execution. FlashLib addresses this gap by treating these operators as first-class online primitives.

---

## Main Original Ideas

1. **Algorithmic Reformulation for GPU Friendliness** -- Operators are rewritten to avoid materializing large intermediate structures. For example, Flash-KMeans computes cluster assignments via running minima maintained in registers, never writing full N×K distance matrices to HBM -- the key insight that unlocks the 26x speedup.

2. **Hardware-Aware Kernel Variants with Adaptive Dispatch** -- Multiple kernel implementations exist per operator, tuned to different hardware generations and workload shapes. KNN, for instance, uses distinct strategies for large-batch queries vs. single queries against massive corpora. The dispatcher selects automatically.

3. **Tolerance-Driven Precision Routing** -- Users declare a `tol` precision budget; the dispatcher routes through precision-emulation techniques (e.g., bf16, ozaki2_int8) or algorithmic shortcuts that satisfy accuracy requirements while maximizing throughput. This makes precision-performance tradeoffs explicit and controllable.

4. **Transparent CPU-Side Cost Prediction** -- A pure-Python cost estimator (~5 µs, no GPU required) lets agents predict operator costs before submission, enabling pipeline-level budgeting and scheduling without GPU round-trips.

5. **Triton/CuteDSL Implementation with No Binary Blobs** -- All kernels are written in Triton and CuteDSL, fully inspectable and modifiable by researchers and AI agents. No opaque binary components.

---

## Key Findings

### Benchmark vs. cuML 25.10 on H200 GPUs (194 workload configurations)

| Primitive    | Peak Speedup | Geometric Mean | Hardware Efficiency |
|--------------|-------------|----------------|---------------------|
| **TruncatedSVD** | **208x**   | --             | --                  |
| t-SNE (exact)| **147x**    | --             | --                  |
| **PCA**      | **47x**     | --             | --                  |
| HDBSCAN      | 40x         | --             | --                  |
| KMeans       | 26x         | ~4.2x          | 61% peak FLOPs      |
| KNN          | 19x         | ~3.8x          | 85.2% peak HBM BW   |

- 193/194 cells: equivalent or superior to cuML
- 126/194 cells: 5x+ speedup
- 11/194 cells: 50x+ speedup

### Agent Loop Integration (Claude Code Opus 4.7, GPU vector-search backend)

| Scenario              | FlashLib   | Baseline   | Speedup |
|-----------------------|------------|------------|---------|
| Offline batch         | 310k QPS   | 50k QPS    | **6.2x** |
| Online single-query   | ~1x        | --         | 1x (launch overhead dominates) |
| Streaming w/ tie-break| 5.0k QPS   | 1.0k QPS   | **5.2x** |

- GEMM at 4096³ shows Pareto-optimal variants across precision levels -- certain compressed-precision approaches are "tighter AND faster than fp32"

---

## Suggestions & Future Directions

1. **Expand primitive coverage** -- Gaussian mixtures, kernel methods, and graph-based algorithms are targeted for future releases.
2. **Sparse input support** -- Current release focuses on dense primitives; sparse inputs are a planned extension.
3. **Broader hardware portability** -- Coverage is currently concentrated on H200; testing and optimization for other GPU generations is pending.
4. **Agent integration patterns** -- The agent-loop benchmark points to the need for better launch-overhead amortization strategies for single-query online regimes where speedups currently collapse to ~1x.

---

## Authors & Institutions

Shuo Yang, Haocheng Xi, Yilong Zhao, Qiuyang Mang (UC Berkeley); Zhe Wang, Shanlin Sun (UC Irvine); Song Han (MIT); Chenfeng Xu (UT Austin); Kurt Keutzer, Joseph E. Gonzalez, Ion Stoica (UC Berkeley)
