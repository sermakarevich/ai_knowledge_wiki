# Discovering Multiagent Learning Algorithms with Large Language Models

**Paper:** [Discovering Multiagent Learning Algorithms with Large Language Models (Zun Li, John Schultz, Daniel Hennes, Marc Lanctot, 2025)](https://arxiv.org/abs/2602.16928)

## Human Readable TL;DR

Designing algorithms for AI agents that play games against each other has traditionally been done by human experts through years of trial-and-error. This paper automates that process: an AI (powered by a large language model) writes and rewrites code for game-playing algorithms, tests them in simulated games, and keeps the best versions -- like breeding better and better strategies. The result is two new algorithms that are better than anything humans had previously designed, and they contain tricks that no human thought to try.

## TL;DR

This paper introduces an LLM-driven evolutionary framework (AlphaEvolve) to automatically discover multi-agent reinforcement learning algorithms for imperfect-information games. By treating algorithm source code as the evolutionary genome and using Gemini 2.5 Pro as a semantic mutation operator, the system discovers two novel algorithms -- VAD-CFR and SHOR-PSRO -- that outperform state-of-the-art baselines on 10/11 and 8/11 benchmark games respectively, featuring non-intuitive mechanisms like volatility-adaptive discounting and dynamic annealing meta-solvers.

---

## Problem & Motivation

Designing effective multi-agent learning algorithms (e.g., CFR variants, PSRO meta-solvers) for imperfect-information games has historically required deep human expertise and laborious manual iteration. The combinatorial design space of update rules, weighting schemes, and structural choices is too vast for human search alone, and existing approaches like hyperparameter optimization or genetic programming either fix the algorithm structure or rely on syntactic mutations that lack semantic meaning. The authors ask: can LLMs act as intelligent algorithm designers, generating semantically meaningful code mutations that discover mechanisms humans wouldn't conceive?

---

## Main Original Ideas

1. **LLM as Semantic Evolutionary Operator** -- AlphaEvolve uses an LLM (Gemini 2.5 Pro) to propose meaningful modifications to algorithm source code rather than random syntactic mutations. The LLM reads the current algorithm, understands its logic, and rewrites components to improve exploitability on proxy games -- enabling discovery of novel control flows and symbolic operations.

2. **Code as Genome** -- The algorithm's Python source code is the evolvable entity. Candidate algorithms are auto-executed on training games, scored by exploitability (distance from Nash Equilibrium), and fed into an evolutionary selection loop. Valid, better-performing candidates propagate.

3. **Structured Search Space via Evolvable Classes** -- For CFR, three Python classes are made evolvable: `RegretAccumulator`, `PolicyFromRegretAccumulator`, and `PolicyAccumulator`. For PSRO, two meta-solver classes are evolved: `TrainMetaStrategySolver` and `EvalMetaStrategySolver`. This decomposition is expressive enough to reproduce all known variants while leaving room for novelty.

4. **VAD-CFR: Volatility-Adaptive Discounting** -- The discovered CFR variant dynamically adjusts discount factors based on an EWMA of instantaneous regret magnitude (volatility). High volatility triggers stronger discounting (faster forgetting); low volatility retains more history. It also applies asymmetric boosting (1.1x) to positive instantaneous regrets and delays policy averaging with a hard warm-start at iteration 500, weighting accumulated policies by regret magnitude.

5. **SHOR-PSRO: Hybrid Meta-Solver with Dynamic Annealing** -- The discovered PSRO meta-solver blends Optimistic Regret Matching (ORM) with a Boltzmann distribution over pure strategies, with a blending factor that anneals from 0.3 to 0.05 over training iterations. A diversity bonus also decays (0.05 to 0.001), encouraging early exploration and late refinement. Training and evaluation solvers are asymmetrically configured: training uses dynamic schedules and average strategies; evaluation uses fixed low-noise params and last-iterate strategies.

---

## Key Findings

| Algorithm | Games Matching/Beating SOTA | Notable Example |
|-----------|----------------------------|-----------------|
| VAD-CFR | 10 / 11 | 3-player Leduc Poker: exploitability < 10^-3 while baselines plateau higher |
| SHOR-PSRO | 8 / 11 | 3-player Leduc Poker & 6-sided Liar's Dice: consistently matches or beats best baselines |

- **Generalization without re-tuning:** Both algorithms are discovered on 4 training games and evaluated on 4 distinct (larger/harder) test games and 11 total, confirming generalization.
- **Non-intuitive mechanisms validated empirically:** VAD-CFR's hard warm-start and regret-magnitude weighting -- mechanisms unlikely to be manually conceived -- proved critical to its performance.
- **Asymmetric training/evaluation solvers:** The evolutionary search independently discovered that the training-time and evaluation-time meta-solvers in PSRO benefit from fundamentally different configurations, a nuance absent from all prior hand-designed baselines.
- **Interpretable output:** Unlike neural meta-learners, all discovered algorithms are symbolic Python code that can be read, analyzed, and built upon.

---

## Suggestions & Future Directions

1. **Apply to deep RL agents** -- Extend the framework to evolve algorithms that govern neural network updates in fully deep multi-agent RL settings, where the current work is limited to tabular/exact game-theoretic algorithms.

2. **General-sum and cooperative games** -- The current benchmarks are zero-sum; applying the framework to cooperative or mixed-motive settings is a natural and important extension.

3. **Larger and more complex games** -- The training proxy games are relatively small. Scaling the evaluation infrastructure to support larger state spaces would allow discovery of algorithms optimized for real-world-scale problems.

4. **Multi-objective evolution** -- The system supports multi-objective fitness but was primarily optimized for exploitability. Future work could jointly optimize for convergence speed, computational cost, and robustness.

5. **Cross-domain applicability** -- The authors suggest the AlphaEvolve framework may generalize to algorithm discovery in other scientific and engineering domains beyond MARL.

---

## Authors & Institutions

Zun Li (Google DeepMind), John Schultz (Google DeepMind), Daniel Hennes (Google DeepMind), Marc Lanctot (Google DeepMind)
