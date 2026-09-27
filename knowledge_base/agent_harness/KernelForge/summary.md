# Kernel Forge: An Agent Harness for LLM-based Generation and Optimization of CUDA Kernels

**Paper:** [Kernel Forge: An Agent Harness for LLM-based Generation and Optimization of CUDA Kernels (Brodsky, Kumar, Kashmira, Danatanarayana, Mars, Flautner, Tang, 2026)](https://arxiv.org/abs/2607.24762)

## Human Readable TL;DR

Imagine a mechanic who won't just tune an engine part on a workbench, but insists on testing it while it's actually bolted into the car, driving on the real road it will be used on. Kernel Forge is that mechanic for AI models: it watches a real PyTorch model run, has an LLM (Claude Opus 4.7) write custom low-level GPU code (CUDA) for the specific operations that model actually uses, checks that the new code computes the same answer and is actually faster, and only swaps it in if it's a genuine improvement -- otherwise it quietly keeps using the original, tried-and-true code. It even builds a "family tree" of many candidate versions and explores promising branches, like trying many recipe variations and only keeping the ones that taste better.

## TL;DR

Kernel Forge is an open-source LLM-agent system that generates and optimizes CUDA kernels for real, unmodified PyTorch model executions rather than isolated micro-benchmarks. It captures concrete "operator cards" from a live model run, uses an LLM (Claude Opus 4.7) inside a Monte Carlo Tree Search loop to iteratively generate and refine kernel candidates, validates each candidate for compilation, runtime correctness, and numerical fidelity, and only deploys a generated kernel when it is faster than the observed PyTorch eager baseline -- otherwise falling back automatically. Across ResNet-50, Stable Diffusion 3.5 Medium, Gemma 4 E2B, and Qwen 3.5 35B-A3B, the system achieves per-operator speedups up to 2.83x, but consistently fails to beat mature vendor-backed kernels (cuDNN/cuBLAS, attention, large matmuls) that dominate total runtime.

---

## Problem & Motivation

Existing LLM-based kernel optimization work typically benchmarks generated kernels in isolation with randomly generated tensors, which doesn't reflect how a kernel behaves when embedded in a deployed model with its actual shapes, dtypes, and call patterns -- "a kernel that performs well in isolation may not provide the same benefit when inserted into a deployed ML model." Additionally, prior systems often require manual integration of optimized code back into the model, target only specific model families (mostly LLMs), and lack tooling for a developer to inspect or debug what the optimizer actually did. Kernel Forge is built to close these three gaps at once: workload-grounded evaluation, automatic integration, and a GUI for auditability.

---

## Main Original Ideas

1. **Operator cards from live model execution.** Instead of optimizing abstract operator families, Kernel Forge runs the unmodified PyTorch model on user-provided example inputs and records concrete "variants" -- specific shape/dtype/stride/layout/argument combinations actually observed at runtime. Two convolution calls with different shapes become two distinct optimization targets, letting the search focus exactly on what the deployed workload needs.

2. **Three-stage kernel validator.** Every LLM-generated candidate must pass (a) `nvcc` compilation with a bounded automatic repair loop on errors, (b) runtime execution on captured inputs with repair-on-failure, and (c) numerical correctness against PyTorch eager outputs within tolerance. This is a workload-specific admissibility filter, not a correctness guarantee outside the captured inputs.

3. **MCTS-based optimization controller.** Rather than linear refinement or beam search, a persistent revision tree explores multiple optimization lineages in parallel. Each node tracks source, visit count, measured latency, and parent/child links. Progressive widening lets a node with *x* visits spawn up to ⌊α(R)·√x⌋ children, with α annealing from 0.5 to 0.3 over the first 1000 root visits; a UCT-style score balances exploiting the best-known subtree against exploring under-visited branches. This lets initially-slower candidates survive if they become useful stepping stones later.

4. **Guarded dispatch with automatic fallback.** A generated kernel is only ever dispatched into the live model if it is compatible with the exact captured call pattern, numerically valid on recorded examples, and empirically faster than the measured PyTorch eager latency for that variant. Otherwise the system silently falls back to the original PyTorch path -- eliminating regression risk from bad or merely-not-better generated code. Kernels package as `.cast` files with source, validation status, timing, and an audit label (custom CUDA / wrapper-or-backend / fallback).

---

## Key Findings

### Per-operator speedups at 50 optimization iterations (opt50)

| Workload | Operator | Speedup | Runtime share |
|---|---|---|---|
| ResNet-50 | **Adaptive avg pooling** | **1.515x** | 0.12% |
| ResNet-50 | Tensor add | 1.257x | 13.71% |
| ResNet-50 | Max pooling | 1.212x | 1.63% |
| ResNet-50 | ReLU | 1.004x | 11.90% |
| ResNet-50 | Conv2d | 0.999x (fallback) | 53.35% |
| ResNet-50 | Batch norm | 0.992x (slower) | -- |
| SD 3.5 Medium | **Group norm** | **1.699x** | 5.72% |
| SD 3.5 Medium | SiLU | 1.052x | 0.19% |
| SD 3.5 Medium | Layer norm | 1.049x | 4.76% |
| SD 3.5 Medium | Linear | 0.495x (fallback) | 53.40% |
| SD 3.5 Medium | Scaled-dot-product attention | 0.021x (fallback) | 27.12% |
| Gemma 4 E2B | **Softmax** | **2.827x** | 5.93% |
| Gemma 4 E2B | Linear | 0.246x (fallback) | 90.13% |
| Qwen 3.5 35B-A3B | Softmax | 1.544x | 0.19% |
| Qwen 3.5 35B-A3B | Conv1d | 1.292x | 0.40% |
| Qwen 3.5 35B-A3B | Embedding | 1.138x | ~0.002% |
| Qwen 3.5 35B-A3B | Grouped matmul | 0.616x (fallback) | 93.62% |

- Across all four workloads, open-source/native PyTorch operators improved 13 of 24 times (54%), while proprietary/vendor-backed operators (cuDNN, cuBLAS, fused attention) improved only 1 of 9 times (11%).
- The largest speedups consistently land on operators contributing a small share of total runtime; the dominant, runtime-heavy operators (Conv2d, Linear, attention, grouped matmul) remain slower than PyTorch eager and fall back.
- Evaluated on an NVIDIA DGX Spark (GB10 GPU) across ResNet-50 (fp16, ImageNetV2), Stable Diffusion 3.5 Medium (bf16, T2I-CompBench), Gemma 4 E2B (bf16, MT-Bench/ShareGPT/LongBench), and Qwen 3.5 35B-A3B (bf16, same LLM benchmark mix), with 912-75,544 captured operator calls per workload.
- Search cost (Claude Opus 4.7 at $5/M input, $25/M output tokens) rises sharply at higher iteration budgets (opt50) without a proportional increase in aggregate runtime-weighted benefit, even after filtering to operators consuming ≥1% of operator-region time.

---

## Suggestions & Future Directions

1. Move from fixed, uniform search budgets per operator to **runtime-percentage-aware search policies** that stop early on low-impact operators and allocate more iterations to dominant, runtime-heavy operators with weaker baselines.
2. Extend evaluation from operator-region measurements to **full end-to-end model latency**, since current results only measure captured operator executions rather than whole-model wall-clock time.
3. Investigate why generated CUDA struggles specifically against **mature vendor-backed implementations** (cuDNN, cuBLAS, fused attention) -- these remain the hardest and highest-value targets since they dominate runtime share.
4. Extend beyond CUDA/NVIDIA to **other accelerator targets**, which the authors note would require architectural changes to the current system.

---

## Authors & Institutions

Joshua Brodsky, Dhravid Kumar, Savini Kashmira, Jayanaka Danatanarayana, Jason Mars, Krisztian Flautner, Lingjia Tang -- all University of Michigan.

Code: [github.com/TheJoshBrod/KernelForge](https://github.com/TheJoshBrod/KernelForge) (CC BY 4.0).
