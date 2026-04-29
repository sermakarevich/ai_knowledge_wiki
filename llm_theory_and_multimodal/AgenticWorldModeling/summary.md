# Agentic World Modeling: Foundations, Capabilities, Laws, and Beyond

**Paper:** [Agentic World Modeling: Foundations, Capabilities, Laws, and Beyond (Chu et al., 2026)](https://arxiv.org/pdf/2604.22748)

## Human Readable TL;DR

Imagine teaching a chess computer not just to memorize moves, but to truly understand the rules of the game -- and then extend that to the real world. This paper is a master map for researchers building AI that doesn't just predict what happens next, but can mentally simulate entire futures, test hypotheses, and revise its own understanding when it's wrong. It organizes all existing approaches into three tiers: basic one-step guessers, full-blown "mental simulators" useful for planning, and the most advanced systems that can run experiments to fix their own blind spots. The map covers four "worlds": the physical world of objects and gravity, the digital world of software and APIs, the social world of human norms and intentions, and the scientific world of unknown laws waiting to be discovered.

## TL;DR

This survey introduces a unified "levels × laws" taxonomy for agentic world modeling, organizing over 400 works into three capability levels (L1 Predictor, L2 Simulator, L3 Evolver) cross-referenced against four governing-law regimes (physical, digital, social, scientific). It formalizes precise boundary conditions for each capability transition, proposes decision-centric evaluation metrics (ASR, COD), and identifies ten open research problems -- providing a common language to bridge fragmented communities and a roadmap toward fully autonomous, self-revising world models.

---

## Problem & Motivation

The term "world model" means different things to different research communities: in RL it refers to learned transition functions, in computer vision to video generators, in robotics to dynamics models. This fragmentation produces incompatible definitions, inconsistent evaluation practices, and blocked knowledge transfer across communities. The gap widens as AI shifts from passive content generation to goal-directed agentic behavior, where the ability to simulate future states is a core bottleneck. Existing surveys organize literature by modality or domain rather than by what a system can actually *do*, leaving the capability progression -- from local prediction through multi-step simulation to autonomous self-revision -- unmapped.

---

## Main Original Ideas

1. **L1 Predictor** -- The foundational level: learns local one-step transition operators (state inference, forward dynamics, observation decoding, inverse dynamics). Operates in latent space with a Markovian belief state. Effective for representation learning but prone to compounding errors over long horizons.

2. **L2 Simulator** -- Extends L1 by composing operators into decision-usable multi-step rollouts. Three formal boundary conditions mark the L1→L2 transition: (a) long-horizon coherence, (b) intervention sensitivity (counterfactuals induce stable, directional trajectory changes), and (c) constraint consistency (rollouts obey the regime's governing laws).

3. **L3 Evolver** -- Extends L2 with evidence-driven model revision via a closed loop: design → execute → observe → reflect. Three boundary conditions: (a) evidence-grounded diagnosis, (b) persistent asset update (parameters, architecture, or hypothesis space), (c) governed validation (rollback and canary policies before deployment).

4. **Four Governing-Law Regimes** -- Physical (contact mechanics, gravity), Digital (API contracts, UI state machines), Social (beliefs, norms, institutional rules), Scientific (latent causal mechanisms to be discovered). Each regime defines what "constraint consistency" means and what constitutes a failure.

5. **Decision-Centric Evaluation** -- Replaces generative metrics (FID, PSNR) with metrics that measure planning utility: Action Success Rate (ASR) and Counterfactual Outcome Deviation (COD). Introduces Minimal Reproducible Evaluation Packages (MREPs) to standardize reporting.

6. **Capability as Dynamic Invocation** -- Levels are not static model classes; a single system may invoke L1, L2, or L3 capabilities in different contexts within the same task.

---

## Key Findings

| Regime | L2 Maturity | L3 Maturity | Representative Systems |
|--------|-------------|-------------|------------------------|
| Physical | High (video gen + sim) | Emerging | Sora, GAIA-1, DayDreamer, AdaptSim |
| Digital | High (code/web agents) | Partial | WorldCoder, WebDreamer, FunSearch, AlphaEvolve |
| Social | Moderate (ToM, sandboxes) | Aspirational | CICERO, Generative Agents, Sotopia |
| Scientific | High (neural operators) | Established | GraphCast, Aurora, Robot Scientist, A-Lab |

- Most current systems are L1; compounding error is the universal failure mode.
- Scientific world has the most mature L3 examples because its evidence signal is unambiguous and its experiments are instrumentable.
- Social world L3 remains aspirational due to attribution ambiguity and ethical constraints on experimentation.
- Video generation models (Sora, Genie, Oasis) approach L2 visually but often fail intervention sensitivity and constraint consistency tests.
- Symbolic representations become necessary at L3 for law revision; neural representations alone are insufficient.

**Recurring failure modes across all regimes:** compounding error, state aliasing, controllability failure, exploitability, calibration failure under distribution shift.

---

## Suggestions & Future Directions

1. **Physical faithfulness beyond visual plausibility** -- Video generators need explicit geometry and contact models, not just photorealism.
2. **Partially observable multi-user digital environments** -- Web agents must handle concurrent users and hidden server state.
3. **Social attribution for model revision** -- Detecting which social norm was violated and why is unsolved.
4. **Surrogate-to-reality gap in science** -- Neural surrogates must close the loop to real experimental validation.
5. **Continual L3 learning without catastrophic forgetting** -- Self-revision systems must retain prior knowledge while integrating new evidence.
6. **Benchmark contamination in L3** -- When the model can modify its own training data or evaluation environment, standard benchmarks break.
7. **Governance of self-evolving systems** -- Rollback policies, canary deployments, and misattribution cascades need principled frameworks.
8. **Neuro-symbolic hybrid architectures** -- Neural dynamics for scalability combined with symbolic law representations for inspectable revision.
9. **Cross-regime transfer** -- Skills and representations learned in one regime (e.g., digital) should transfer to others (e.g., physical).
10. **Decision-centric benchmarks** -- Community-wide adoption of ASR/COD-style metrics and MREP reporting standards.

---

## Authors & Institutions

Meng Chu, Xuan Billy Zhang, Jize Zhang, Kevin Qinghong Lin, Lingdong Kong, Teng Tu, Weijian Ma, Haoxuan Che, Long Chen, Qifeng Chen, Wenxuan Zhang, Wenya Wang, Xiaojuan Qi, Yang Deng, Yanwei Li, Mike Zheng Shou, Zhi-Qi Cheng, See-Kiong Ng, Ziwei Liu, Philip Torr, Jiaya Jia -- Hong Kong University of Science and Technology, National University of Singapore, University of Oxford, Nanyang Technological University, Chinese University of Hong Kong, University of Hong Kong, University of Washington, Singapore University of Technology and Design, Singapore Management University
