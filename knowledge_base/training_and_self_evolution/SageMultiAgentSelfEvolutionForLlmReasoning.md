# SAGE: Multi-Agent Self-Evolution for LLM Reasoning

**Paper:** [SAGE: Multi-Agent Self-Evolution for LLM Reasoning (Peng et al., 2025)](https://arxiv.org/abs/2603.15255)

## Human Readable TL;DR

Imagine a study group where one student invents tough practice problems, another makes a step-by-step game plan, a third solves them, and a fourth grades both the problems and the plans -- then they all swap notes and get better together. SAGE does exactly this with AI models: four specialized "agents" living inside a single language model teach each other to reason better at math and coding, starting from just 500 example problems and needing almost no human help after that.

## TL;DR

SAGE is a closed-loop, multi-agent self-evolution framework for improving LLM reasoning in verifiable domains (math, code). It instantiates four specialized agents -- Challenger, Planner, Solver, and Critic -- from a shared LLM backbone, trained jointly via Task-Relative REINFORCE++. Starting from only 500 seed examples, SAGE achieves consistent improvements across Qwen 3B/4B/7B models, with strong out-of-distribution generalization on competition-level math benchmarks and LiveCodeBench.

---

## Problem & Motivation

Current RL-based methods for improving LLM reasoning depend heavily on large human-curated datasets for verifiable rewards -- a scalability bottleneck. Self-play alternatives (SPIRAL, Absolute Zero) reduce this dependency but suffer from instability and curriculum drift due to lack of explicit planning and quality control. Existing multi-agent frameworks (MetaGPT, CAMEL, MARS) struggle in open-ended domains and lack structured planning for sequential multi-step reasoning. SAGE addresses all three gaps: minimal human data dependence, stable training via quality filtering, and structured multi-step planning.

---

## Main Original Ideas

1. **Four-Agent Closed-Loop Architecture** -- A Challenger generates hard problems, a Planner decomposes them into steps, a Solver executes the plan, and a Critic gates quality at two points (task quality and plan quality). All four share a single LLM backbone and co-evolve through joint training.

2. **Dual-Role Critic Gating** -- The Critic serves as both a task filter (rejecting ill-formed Challenger outputs) and a plan gate (suppressing low-quality plans so the Solver falls back to direct answering). This prevents curriculum drift and stabilizes self-training.

3. **Task-Relative REINFORCE++** -- A critic-free policy gradient method with per-role advantage normalization that coordinates agents with heterogeneous reward objectives within a single parameter update, avoiding the instability of separate training loops.

4. **Difficulty-Aware Challenger Reward** -- The Challenger is rewarded for producing problems the Solver finds hard (low average pass rate) but that pass the Critic's quality threshold, creating an adaptive curriculum that scales with model capability.

5. **Minimal Seed Bootstrap** -- The entire system bootstraps from just 500 seed problems (sampled from MATH, GSM8K, HumanEval, MBPP), expanding the dataset 18x autonomously during training.

---

## Key Findings

| Model | Math Avg (ID) | Math Avg (OOD) | Code Avg | Overall Avg | Delta vs Base |
|---|---|---|---|---|---|
| **Qwen-2.5-3B + SAGE** | 75.9 | 19.0 | 50.8 | 42.0 | **+1.6** |
| **Qwen-2.5-7B + SAGE** | 79.2 | 28.8 | 53.4 | 50.1 | **+2.5** |
| **Qwen-3-4B + SAGE** | 77.7 | 36.0 | 56.2 | 55.9 | +0.2 |

- SAGE achieves the best or near-best OOD average across all three backbones, with up to +4.2% OOD gain on Qwen-2.5-7B
- LiveCodeBench performance consistently best across all backbones (e.g., +9.1% on Qwen-3-4B, from 21.5% to 30.6%)
- OlympiadBench improved by +10.7% on Qwen-2.5-7B (28.0% to 38.7%)
- Baselines AZR and MAE show inconsistent or negative gains (AZR drops Math Avg by -9.6% on Qwen-3-4B); SAGE remains balanced
- Ablation confirms all agents contribute: removing Solver causes the largest drop (Overall Avg 42.0% to 38.2%); removing Challenger collapses LiveCodeBench (16.9% to 9.0%); removing Critic degrades code benchmarks
- Self-generated dataset expands 18x (1,136 to 20,532 valid questions) over 250 training steps
- Validation accuracy peaks around steps 100--140, then gradually declines, suggesting over-specialization on the self-generated curriculum

---

## Suggestions & Future Directions

1. **Extension to non-verifiable domains** -- Developing learned reward models or human-in-the-loop validation to apply SAGE beyond math/code where objective verification is unavailable.

2. **Reducing seed requirements further** -- Exploring near-zero-seed settings to broaden applicability to extremely low-resource scenarios.

3. **Other reasoning domains** -- Applying SAGE to logical reasoning, scientific problem-solving, and knowledge graph completion to test generalizability.

4. **Mitigating over-specialization** -- Investigating dynamic curriculum strategies, early stopping, or diversity-promoting rewards to prevent the observed late-training accuracy decline.

5. **Scaling to larger models** -- Evaluating SAGE on 70B+ parameter models to assess whether the co-evolutionary benefits compound at scale.

---

## Authors & Institutions

Yulin Peng, Xinxin Zhu, Chenxing Wei, Nianbo Zeng, Leilei Wang, Ying Tiffany He (Shenzhen University & Guangdong Laboratory of AI and Digital Economy, China), F. Richard Yu (Carleton University, Canada)
