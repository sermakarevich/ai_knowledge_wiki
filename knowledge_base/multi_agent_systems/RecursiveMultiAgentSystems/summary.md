# Recursive Multi-Agent Systems

**Paper:** [Recursive Multi-Agent Systems (Yang et al., 2026)](https://arxiv.org/abs/2604.25917)

## Human Readable TL;DR

Imagine a team of experts working on a hard problem -- but instead of passing written notes back and forth, they can directly share their raw thoughts without translating them into words first. This paper builds that kind of "telepathic" teamwork for AI agents. The result is that the team solves problems more accurately and much faster, because they skip the slow and lossy step of converting ideas into text at every handoff. On average, this makes the AI team 8% more accurate while cutting the amount of "talking" needed by up to 75%.

## TL;DR

RecursiveMAS extends recursive language model scaling (like LoopLM) to multi-agent systems by replacing inter-agent text communication with latent-space thought sharing via a lightweight RecursiveLink module. A two-stage inner-outer loop training algorithm enables system-wide co-optimization via gradient-based credit assignment. Across 9 benchmarks (math, science, medicine, code, search), the framework achieves +8.3% average accuracy, 1.2x-2.4x inference speedup, and 34.6%-75.6% token reduction compared to text-based multi-agent baselines.

---

## Problem & Motivation

Multi-agent systems (MAS) typically coordinate through natural language -- each agent reads text output from the previous agent and writes text back. This creates two bottlenecks: (1) vocabulary-space decoding at every inter-agent step is computationally expensive, and (2) information is lost when rich latent representations are compressed into discrete tokens. Prior work on recursive LMs (LoopLM) showed that feeding latent states back into a single model improves scaling, but this has not been extended to heterogeneous multi-agent collaboration. RecursiveMAS fills this gap.

---

## Main Original Ideas

1. **RecursiveLink Module** -- A lightweight two-layer residual projection with GELU activation that transmits latent hidden states between agents without decoding to text. Two variants: an *inner link* for same-architecture agents and an *outer link* (adds a third linear projection W₃) for bridging agents with different hidden dimensions.

2. **System-Level Recursion** -- The entire MAS is treated as a single recursive computation. Agents form a loop: each produces latent "thoughts" (m embedding steps) that flow to the next agent, and the final agent's state feeds back to the first. Text output is only generated at the final round, eliminating per-step vocabulary decoding.

3. **Inner-Outer Loop Training** -- A two-stage optimization algorithm: the *inner loop* warm-starts each agent individually via cosine similarity regression between generated latent thoughts and ground-truth embeddings; the *outer loop* co-trains the full system end-to-end with cross-entropy loss unrolled through n recursion rounds, enabling shared gradient credit assignment.

4. **Theoretical Complexity & Gradient Stability** -- Proposition 3.1 proves RecursiveMAS reduces runtime complexity from Θ(N·|V|·dₕ·...) to Θ(N·(t+m)²·dₕ), eliminating the expensive vocabulary-projection term. Theorem 4.1 proves that text-based recursion causes gradient norms to collapse to O(ε)≪1 while RecursiveMAS maintains Ω(1-√(1/dₕ·log(1/δ))) gradient stability.

---

## Key Findings

### Accuracy vs. Baselines (r=3 recursion rounds, MATH500)

| Method | MATH500 | Notes |
|---|---|---|
| **RecursiveMAS** | **88.0%** | Full system |
| TextGrad | 84.9% | Text-based gradient |
| LoopLM | 84.6% | Single-agent recursion |
| Single agent + LoRA | 83.1% | Finetuned solo agent |
| MoA baseline | 79.8% | Mixture of agents |

### Efficiency at Different Recursion Rounds

| Rounds (r) | Speedup | Token Reduction |
|---|---|---|
| r=1 | 1.2× | 34.6% |
| r=3 | 2.4× | 75.6% |

### Additional Findings

- Works across all four collaboration styles: sequential (planner→critic→solver), mixture (parallel specialists), distillation (expert→learner), and deliberation (tool-integrated reflection).
- Generalizes across model families: Qwen, Llama, Gemma, Mistral (1.5B-10B parameters).
- +6.2% average improvement in mixture-style settings across 9 benchmarks.
- Optimal latent thought length stabilizes at m=80 steps; residual connections contribute +2.1% on GPQA-Diamond.
- Semantic distribution analysis shows progressive alignment of latent thoughts with ground-truth answer distributions across recursion rounds.
- Lowest training GPU memory footprint (15.29GB) among comparable systems, at highest accuracy (74.9%).

---

## Suggestions & Future Directions

1. **Scale to larger models** -- current experiments are limited to 1.5B-10B parameter models; applying RecursiveMAS to frontier-scale LLMs is an open question.
2. **Unfreeze base LLM parameters** -- current setup keeps base model weights frozen; joint fine-tuning could yield further gains.
3. **Dynamic collaboration patterns** -- the topology (sequential, mixture, etc.) is fixed at design time; learning adaptive routing between agents could improve performance on diverse tasks.
4. **Larger-scale deployment** -- practical deployment challenges (latency, memory, heterogeneous hardware) at scale have not been studied.
5. **Broader model compatibility** -- outer link handles different hidden dimensions, but compatibility across vastly different architectures remains to be explored.

---

## Authors & Institutions

Xiyuan Yang, Jiaru Zou, Rui Pan, Ruizhong Qiu, Pan Lu, Shizhe Diao, Jindong Jiang, Hanghang Tong, Tong Zhang, Markus J. Buehler, Jingrui He, James Zou -- University of Illinois Urbana-Champaign, Stanford University, and collaborating institutions.
