# Position: Agentic AI System Is a Foreseeable Pathway to AGI

**Paper:** [Position: Agentic AI System Is a Foreseeable Pathway to AGI (Liao, Li, Wen, Wang, Zhang, 2026)](https://arxiv.org/abs/2605.12966)

## Human Readable TL;DR

Imagine trying to hire one person who can do every job -- doctor, lawyer, plumber, chef -- all equally well. That person would be mediocre at each because the skills pull in different directions. This paper argues the same thing happens when you just keep making AI bigger and bigger: it gets stuck averaging across too many different types of tasks and hits a ceiling. Instead, the authors argue you should build a team of specialized AI agents -- each great at one thing -- coordinated by a manager. They prove mathematically that this "agent team" approach learns exponentially faster and more efficiently than the "one giant AI" approach, and they say this coordinated team structure is the realistic path to building truly general artificial intelligence.

## TL;DR

This ICML'26 position paper provides theoretical justification for why monolithic scaling is insufficient for AGI and why agentic AI systems are necessary. The authors prove that real-world data lives on a union of low-dimensional task manifolds, causing monolithic models to suffer an irreducible "Average Trap" penalty from conflicting task gradients. They show routing-based agentic decomposition achieves error that decays exponentially faster (error ratio ≈ K·N^(1/D − 1/dmax)) and extends this to general DAG topologies with topological weight/edge weight analysis. The central claim is that AGI requires shifting from brute-force scaling to stable, well-designed agentic ecosystems.

---

## Problem & Motivation

The dominant paradigm for AI progress has been monolithic scaling -- train one larger model on more data. While effective, scaling laws show diminishing returns (Kaplan et al. 2020, Hoffmann et al. 2022), and no single monolithic model dominates all benchmarks (SWE-bench, GAIA, BFCL). The core question: **is there a fundamental reason why a single model cannot achieve AGI, regardless of scale?**

The paper argues yes -- because real-world tasks are heterogeneous by nature, forming distinct optimization landscapes. Any single parameter set is forced into a compromise that cannot be globally optimal for all tasks simultaneously.

---

## Main Original Ideas

1. **Structured Real-World Distribution (Definition 2.1).** Real-world data concentrates on a union of K compact Riemannian manifolds {ℳk}, each with intrinsic dimension dk ≪ D (ambient dimension). Each task k has its own optimal function fk: ℳk → 𝒴. This formalizes *why* tasks are fundamentally incompatible for a single model.

2. **The Average Trap (Proposition 3.3).** A monolithic model's optimal parameters θmono* cannot coincide with any individual task optimum θk*. The total loss contains an irreducible penalty:
   `ℒtotal(θmono*) ≈ Σk αkℒk(θk*) + Σk (αk/2)‖θmono*−θk*‖²Hk`
   The second term -- a Mahalanobis distance from conflicting Hessians -- is strictly positive and cannot be eliminated by scaling alone.

3. **Exponential Agentic Advantage via Routing (Section 3.2).** Routing to K specialized agents, each operating on manifold ℳk with intrinsic dimension dk, gives error:
   `ℰR-Agentic(N) ≈ O(K·N^(-1/dmax))`
   vs. monolithic `ℰmono(N) ≈ O(N^(-1/D))`.
   The ratio `K·N^(1/D − 1/dmax)` vanishes exponentially since dmax ≪ D. Sample complexity drops from ϵ^(-D) to K^dmax·ϵ^(-dmax).

4. **Optimal Agent Granularity.** The joint error bound `ℰ(K,N) ≤ [KC/N^(1/dmax)] + [Δmax(K)·ϵπ(K)]` is U-shaped in K. Too few agents = insufficient specialization; too many = routing overhead dominates. Tree-based routing scales polylogarithmically (√(log K/N)), making larger K viable; neural routing scales √(K/N), restricting optimal K.

5. **General DAG Topology Framework (Section 4).** Extends routing to arbitrary DAG compositions Ψ = (𝒢, ℱ, Λ). Introduces two key measures:
   - **Topological Weight** ωu: loss sensitivity to agent u, aggregated across all paths to sink nodes via Neumann series on the adjacency Jacobian.
   - **Topological Edge Weight** 𝒲(e*): product of upstream history × local Jacobian ‖Je*‖ × downstream criticality. Design principle: edges after long chains must be contractive (‖Je*‖ < 1) to filter noise.
   Overall DAG generalization error: `ℰAgentic ≈ C(𝒢)·(N/K)^(-1/deff)` where C(𝒢) = Σu ωu is the topology factor.

6. **Reinterpretation of MoE and Multi-Agent Failures.** MoE is shown to be the special case of the routing regime (Section 3.2) with C(𝒢) ≈ ΣLu (inherently stable). Current multi-agent LLM failures are attributed to *organizational entropy* and poor topological design -- not fundamental limitations -- with Lemmas 4.2/4.4 providing diagnostic tools.

---

## Key Findings

| Comparison | Monolithic | Agentic |
|---|---|---|
| Error convergence | O(N^(-1/D)) | O(K·N^(-1/dmax)), dmax ≪ D |
| Sample complexity for ε accuracy | ε^(-D) | K^dmax · ε^(-dmax) |
| Routing error (tree-based) | -- | O(√(poly(log K)/N)) |
| Routing error (neural) | -- | O(√(K/N)) |
| Irreducible loss term | Σ(αk/2)‖θmono*−θk*‖²Hk > 0 | 0 (each agent optimizes locally) |

- The advantage exponent (1/D − 1/dmax) is negative, so the error ratio vanishes as N grows -- agentic systems become exponentially more efficient at scale.
- Mismatch penalty from misrouting: Δmax(K) ≈ Lmax(1−1/√K), decreasing with more agents.
- AGI claim is supported empirically: Anthropic's 2025 multi-agent research system shows significant gains from topology-aware design; sparse MoE systems (Switch Transformers, GShard) consistently outperform dense monoliths.
- No single monolithic model tops all major benchmarks simultaneously (SWE-bench, GAIA, BFCLv2, Humanity's Exam).

---

## Suggestions & Future Directions

1. **Mitigating organizational entropy** -- address inter-agent misalignment and task verification failures that cause current LLM multi-agent systems to degrade.
2. **DAG/tree/forest evolution methods** -- automated topology discovery for finding optimal agent graph structures rather than hand-designing pipelines.
3. **Spectral stability guarantees** -- methods to ensure C(𝒢) < ∞ in practice (topological weight bounded), preventing gradient explosion through deep agent chains.
4. **Transition from static to dynamic topologies** -- topologically-stable ecosystems that can adapt their graph structure during deployment.
5. **Routing mechanisms scaling with agent count** -- especially beyond the √K neural routing barrier.
6. **Topology-aware evaluation** -- benchmarks that attribute failures to specific graph components using the edge weight framework rather than treating the system as a black box.
7. **Theory of Mind for coordination** -- current LLMs underperform RL methods on multi-agent coordination; dedicated coordination training is needed (Agashe et al. 2025).

---

## Authors & Institutions

Junwei Liao, Shuai Li, Muning Wen, Jun Wang, Weinan Zhang

*(Accepted at ICML 2026 Position Track)*
