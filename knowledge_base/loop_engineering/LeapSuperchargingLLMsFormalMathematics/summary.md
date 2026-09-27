# LEAP: Supercharging LLMs for Formal Mathematics with Agentic Frameworks

**Paper:** [LEAP: Supercharging LLMs for Formal Mathematics with Agentic Frameworks (Kung et al., 2026)](https://arxiv.org/abs/2606.03303)

## Human Readable TL;DR

Imagine trying to write a legal contract so precise that a computer can check every clause for contradictions -- that's what mathematicians do when writing "formal proofs." While AI is already great at solving math problems in plain English, it struggles to write these super-precise computer-checkable proofs. LEAP fixes this by giving the AI a structured workflow: instead of trying to write the whole proof at once, it breaks the problem into smaller pieces, sketches a rough plan first, then fills in the rigorous details -- just like a human mathematician would. The result is an AI that can now solve competition math problems that even top human undergrads struggle with, fully verified by a computer.

## TL;DR

LEAP (LLM-in-Lean Environment Agentic Prover) is an agentic framework enabling general-purpose LLMs to achieve state-of-the-art automated formal theorem proving without specialized fine-tuning. It uses an AND-OR DAG for hierarchical proof decomposition, interleaving informal blueprints with formal Lean code, and applying iterative compiler-feedback refinement. On Putnam 2025, LEAP achieves a perfect 100% solve rate (12/12); on the newly introduced Lean-IMO-Bench, it improves the one-shot solve rate from <10% to 70%, surpassing the specialized gold-medal-level Aristotle system (48%).

---

## Problem & Motivation

General LLMs excel at informal mathematical reasoning but fail at generating mechanically verifiable proofs in formal languages like Lean 4. The bottleneck is not mathematical comprehension -- LLMs can already solve competition problems in natural language -- but the difficulty of producing long, complex, syntactically and semantically correct formal proofs in one shot. Prior work addressed this with specialized fine-tuned prover models (AlphaProof, DeepSeek Prover V2, Goedel Prover V2), but these require large computational resources and assume general LLMs are ineffective for formal tasks without specialization. LEAP challenges this assumption.

---

## Main Original Ideas

1. **Blueprint-Driven Agentic Proving** -- Inspired by the human practice of writing proof roadmaps using the Lean Blueprint tool, LEAP generates high-level informal blueprints before formal code. The informal plan structures the formalization and makes proof construction more robust than direct code generation.

2. **AND-OR DAG for Hierarchical Memoization** -- LEAP maintains proof progress as an AND-OR directed acyclic graph (DAG) rather than a flat tree. OR nodes represent open goals (any valid strategy can resolve them); AND nodes represent decompositions (all subgoals must be proved). Intermediate lemmas are stored as shared nodes and reused across branches, supporting anticipatory lemma planning and avoiding redundant derivation.

3. **Interleaved Informal-Formal Planning** -- Both the direct proof path and the decomposition path pass through an informal sketch. The informal reasoning provides a planning space before formalization, paired with executable Lean code for verification. This makes proof steps interpretable alongside compiler feedback.

4. **Verification-Guided Proof Search with LLM Reviewer** -- Two layers of verification are used: the Lean compiler checks formal correctness, and an LLM reviewer assesses whether a proposed decomposition is semantically useful (i.e., actually simplifies the parent goal). The reviewer filters cyclic or non-simplifying decompositions, triggering backtracking and preserving search budget for productive branches.

5. **Lean-IMO-Bench** -- A new benchmark of 60 IMO-style problems (30 Basic, 30 Advanced) formalized in Lean by expert mathematicians. Problems have elementary statements but require highly non-routine, multi-step proofs, complementing saturated benchmarks like MiniF2F and PutnamBench.

---

## Key Findings

| Method | Putnam 2025 | IMO-Bench Basic (%) | IMO-Bench Advanced (%) |
|---|---|---|---|
| Gemini-3.1-Pro (pass@128) | 0/12 (0%) | 20.0 | 3.3 |
| Goedel-Prover-V2-32B (pass@128) | 0/12 (0%) | 10.0 | 0 |
| Hilbert (rollout=2) | 4/12 (33.3%) | 36.6 | 6.6 |
| Aristotle (rollout=2) | 9/12 (75.0%) | **76.7** | 20.0 |
| **LEAP (rollout=2)** | **12/12 (100%)** | **83.3** | **56.7** |

- **Iterative refinement beats one-shot sampling**: Gemini-3.1-Pro improves from 20.0% (pass@128) to 36.6% (pass@1 with 20 compiler-feedback revision steps) on the Basic set. Goedel-Prover-V2-32B does not benefit from feedback loops, confirming that general LLMs' advantage comes from instruction-following and context maintenance.
- **DAG vs. tree**: Removing global lemma sharing (naive tree) drops performance from 83.3% to 73.3% (Basic) and 56.7% to 40.0% (Advanced). The gain is most pronounced in hard categories (Advanced Algebra, Advanced Number Theory).
- **LLM reviewer is critical**: On Putnam A5 (the hardest problem), removing the LLM reviewer causes failure in 8 rollouts. Without it, the agent enters unproductive loops -- restating equivalent goals -- until search budget is exhausted.
- **Geometry remains unsolved**: All methods score near 0% on IMO-level geometry, reflecting the difficulty of formalizing Olympiad geometry in Lean without domain-specific tooling.
- **Research-level utility**: LEAP formalized a key subproblem in Knuth's Hamiltonian decomposition of even-order Cayley graphs, producing 5000+ lines of verified Lean 4 code from 20 pages of dense informal argument. It also reproduced a verified proof of Erdős Problem 457.

---

## Suggestions & Future Directions

1. **Better branch prioritization** -- As decomposition produces fine-grained subgoals, the search space grows rapidly. Future systems need smarter heuristics for branch selection and compute allocation across large proof searches.

2. **Hybrid architectures** -- Combining a general LLM for high-level structural reasoning (blueprints, decomposition) with a specialized fine-tuned model for local Lean tactic generation could combine the best of both paradigms.

3. **LLM-guided proof search** -- The LLM reviewer already acts as a local heuristic; extending it to guide global search (e.g., replacing DFS with LLM-scored best-first search) could further reduce wasted rollouts.

4. **Geometry formalization** -- Olympiad-level geometry in Lean remains an open challenge. Domain-specific supplementary frameworks are likely needed to reach competitive solve rates.

5. **Scaling to more complex problems** -- Proving more complex open problems (beyond subproblems) requires advances in decomposition strategy, proof length management, and long-horizon planning.

---

## Authors & Institutions

Po-Nien Kung (Google Cloud AI Research), Linfeng Song (Google Cloud), Dawsen Hwang (Google DeepMind), Jinsung Yoon (Google Cloud AI Research), Chun-Liang Li (Google Cloud AI Research), Simone Severini (Google Cloud), Mirek Olšák (Google DeepMind), Edward Lockhart (Google DeepMind), Quoc V Le (Google DeepMind), Burak Gokturk (Google Cloud AI Research), Thang Luong (Google DeepMind), Tomas Pfister (Google Cloud AI Research), Nanyun Peng (Google Cloud AI Research)
