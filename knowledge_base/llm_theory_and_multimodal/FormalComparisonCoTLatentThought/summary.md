# A Formal Comparison Between Chain of Thought and Latent Thought

**Paper:** [A Formal Comparison Between Chain of Thought and Latent Thought (Kevin Xu, Issei Sato, 2025)](https://arxiv.org/abs/2509.25239)

## Human Readable TL;DR

Imagine two ways a student solves a hard math problem: one writes every step on paper (chain of thought), and the other works it all out silently in their head (latent thought). This paper proves mathematically that "writing it out" is fundamentally more powerful for certain types of problems -- specifically those where each step depends on the previous one, like following a maze or solving a puzzle with chain-link constraints. The silent approach works well for tasks that can be done all at once in parallel, like recognizing a face. The key insight is that writing things down lets you handle problems that grow far too complex to hold entirely in your head at once.

## TL;DR

This paper provides a formal theoretical analysis comparing Chain of Thought (CoT) and Latent Thought (LT) reasoning via computational complexity theory. The central result is that CoT -- by introducing sequential token positions -- enables polynomial-depth computation equivalent to PSPACE, while single-pass latent models are bounded by NC (logarithmic-depth parallelizable computation). Conversely, CoT enables approximate counting and sampling via stochastic decoding, tasks that are fundamentally hard for latent approaches. The framework gives principled criteria for choosing between the two paradigms based on task computational structure.

---

## Problem & Motivation

Large language models can reason either explicitly (chain of thought: generating visible intermediate steps) or implicitly (latent thought: internal continuous-space computation without discrete tokens). Despite growing empirical evidence that CoT helps on hard tasks, there was no formal account of *why* or *when* each approach is superior. This paper fills that gap by providing the first rigorous complexity-theoretic comparison, enabling principled model and architecture design rather than purely empirical trial-and-error.

---

## Main Original Ideas

1. **Formal Complexity Framework for Reasoning Paradigms.** The paper models CoT and LT through the lens of circuit complexity and parallel computation (NC, PRAM, boolean circuits). This allows precise characterization of which problem classes each paradigm can solve efficiently, going beyond informal intuitions.

2. **Sequential Depth Advantage of CoT.** Transformers compute in parallel across token positions; a single-pass latent model achieves at most NC-depth (logarithmic) reasoning. CoT breaks this ceiling: each explicit reasoning token introduces a new sequential layer, enabling polynomial-depth circuits (PSPACE). This is the paper's central separation result.

3. **Latent Thought Sufficiency for NC Problems.** For tasks that are inherently parallelizable -- those in NC -- latent computation is sufficient and CoT provides no benefit. The paper gives a constructive argument that parallel transformer passes can express NC-depth computations without explicit intermediate tokens.

4. **CoT as a Counting and Sampling Engine.** Via connections to the Jerrum-Sinclair framework, the paper shows CoT can implement approximate counting and rejection sampling by allocating tokens to probabilistic trials. This links CoT expressivity to classical results on #P-complete problems and randomized computation.

5. **Task Classification Principle.** The framework yields a practical decision rule: use latent thought when the task is NC-solvable (parallelizable, shallow dependencies); use CoT when the task has sequential interdependencies, requires witness verification, or involves counting/sampling.

---

## Key Findings

| Result | Claim |
|--------|-------|
| **Theorem 3.12** | CoT solves problems requiring sequential reasoning steps infeasible for single-pass latent models |
| **Theorem 3.13** | Latent thought suffices for NC-class problems; CoT provides no advantage there |
| **Theorem 3.15** | CoT can solve PSPACE problems when intermediate steps are polynomially bounded |
| **Theorems 4.3--4.4** | Counting and sampling problems may require exponentially many CoT steps without special structure; CoT still outperforms latent |

- Problems favoring **CoT**: Boolean SAT (sequential partial-assignment refinement), pathfinding with backtracking, constraint satisfaction with interdependent constraints
- Problems favoring **Latent Thought**: shallow pattern matching, simple feature composition, tasks without sequential dependencies
- The core mechanism: token positions in CoT create a sequential "bottleneck" that enables non-uniform polynomial-size boolean circuits -- equivalent to PSPACE expressivity
- Approximate counting reduces to sampling (via classical reductions); CoT can implement this via stochastic decoding while latent models cannot accumulate sufficient probabilistic evidence in a single pass

---

## Suggestions & Future Directions

1. **Tighter bounds** -- establish exact token-count requirements for specific problem classes rather than asymptotic results only
2. **Hybrid approaches** -- combine latent computation with selective CoT: use latent when the task is NC-parallelizable, switch to CoT only when sequential reasoning is required
3. **Empirical validation** -- test theoretical predictions on realistic language and reasoning benchmarks to bridge the theory-practice gap
4. **Architectural innovations** -- design models that exploit the NC/PSPACE distinction, e.g., with adaptive computation depth
5. **Task characterization tools** -- develop methods to classify new tasks by their computational structure (NC-solvable vs. requiring CoT) before selecting a reasoning strategy

---

## Authors & Institutions

Kevin Xu, Issei Sato -- University of Tokyo (cs.AI, cs.CL, cs.LG)
