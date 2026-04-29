# Toward Ultra-Long-Horizon Agentic Science: Cognitive Accumulation for Machine Learning Engineering

**Paper:** [Toward Ultra-Long-Horizon Agentic Science: Cognitive Accumulation for Machine Learning Engineering (Zhu et al., 2026)](https://arxiv.org/abs/2601.10402)
**Deep dive:** [[details]]
**Code sandbox:** [[sandbox/README]]

## Human Readable TL;DR

Imagine a researcher who has to solve a hard Kaggle competition over a whole day. A normal AI "researcher" keeps a single messy notebook -- every line of output, every failed attempt -- until the notebook is so full it can't think straight and starts repeating old mistakes. This paper gives the AI three notebooks instead of one: a scratchpad for what it is doing right now, a clean summary book where it writes down lessons learned after each chapter, and a long-term diary where it keeps general tricks that worked on past competitions. With this setup, the AI wins Kaggle medals on 56 out of 100 competitions -- more than any previous system -- and does it using only open-source models instead of the most expensive commercial ones.

## TL;DR

The paper introduces **ML-Master 2.0**, an autonomous agent for ultra-long-horizon machine-learning engineering, built around **Hierarchical Cognitive Caching (HCC)** -- a three-tier memory architecture (Evolving Experience / Refined Knowledge / Prior Wisdom) inspired by CPU cache hierarchies. HCC reframes long-horizon context management as *cognitive accumulation*: raw execution traces are progressively distilled into strategic judgments and cross-task wisdom, controlled by explicit promotion and migration operators. On MLE-Bench's 75 Kaggle tasks with a 24h budget, ML-Master 2.0 achieves a **56.4% medal rate** using open-source Deepseek-V3.2-Speciale, surpassing the prior best (Leeroo on Gemini-3-pro-preview, 50.7%) and nearly doubling its own predecessor (29.3%).

---

## Problem & Motivation

Scientific ML engineering is an **ultra-long-horizon** activity: it unfolds over hundreds of interdependent steps spanning hours to weeks -- hypothesizing, coding, debugging, tuning, reflecting. Existing LLM agents collapse in this regime for two related reasons. First, finite context windows force indiscriminate truncation of execution traces, erasing the strategic continuity needed to avoid repeated dead-ends. Second, current agents treat each new task as a fresh start; hard-won lessons from prior tasks do not transfer. Previous memory-augmented agents (MemGPT, HiAgent, G-Memory) address pieces of this problem -- hierarchical storage *or* experiential abstraction -- but never unify both inside a single evolutionary loop. The paper argues that what is missing is not a bigger context window but a **principled way for an agent to convert experience into durable knowledge** during a run.

---

## Main Original Ideas

1. **Cognitive Accumulation as a Paradigm.** Reframes long-horizon autonomy as an evolution: raw *experience* (execution traces) is distilled into validated *knowledge* (strategic judgments), and finally into task-agnostic *wisdom* (reusable strategies). This is presented as the conceptual foundation of the rest of the system.

2. **Hierarchical Cognitive Caching (HCC).** A three-tier memory architecture directly inspired by CPU cache hierarchies. L1 holds high-fidelity traces for the active exploration phase; L2 holds compressed strategic summaries across completed phases; L3 holds persistent cross-task wisdom indexed by task-embedding similarity. Each tier has different temporal stability and reuse value.

3. **Context Migration Protocol.** The governance layer that moves information between tiers via three operations -- *Context Prefetch* (pull similar wisdom from L3 at task start), *Context Hit* (prefer L1 raw traces, fall back to L2 summaries, discard rest), and *Context Promotion* (operators P1 for phase-level compression, P2 for task-level wisdom distillation). This is the mechanism that keeps peak context near 70k tokens instead of 200k+.

4. **ML-Master 2.0 Reference System.** An end-to-end MLE agent instantiating cognitive accumulation with only open-source LLMs, establishing new state-of-the-art on MLE-Bench and serving as empirical validation of the paradigm.

---

## Key Findings

**MLE-Bench full (75 Kaggle tasks, 24h budget, 3 seeds):**

| Method | Base Model | Avg Medal Rate |
|---|---|---|
| **ML-Master 2.0** | **Deepseek-V3.2-Speciale (open)** | **56.4% +/- 2.5** |
| Leeroo | Gemini-3-pro-preview | 50.7% |
| Thesis | gpt-5-codex | 48.4% |
| MLE-STAR-Pro-1.5 | Gemini-2.5-Pro | 44.0% |
| FM Agent | Gemini-2.5-Pro | 43.6% |
| R&D-Agent | gpt-5 | 35.1% |
| AIRA-dojo | o3 | 31.6% |
| ML-Master v1 | Deepseek-R1 | 29.3% |
| AIDE | o1-preview | 17.1% |

- **Difficulty breakdown (medal rate):** Low 75.8% (v1: 48.5%), Medium 50.9% (v1: 20.2%), High 42.2% (v1: 24.4%) -- gains hold across all difficulty tiers.
- **Secondary metrics:** 95.6% valid-submission rate, 63.1% above-median-human rate (highest of any method), 45.3% silver+, 19.6% gold.
- **Relative gains:** +92.7% over ML-Master v1; +11.2% over the previous best proprietary pipeline (Leeroo).
- **Ablation on MLE-Bench-Lite (any-medal rate):** full HCC 72.7%; no L3 (prior wisdom) 54.5%; no L2 (refined knowledge) 59.1%; no L1 (evolving experience) 22.7%. Removing L1 is catastrophic; L2 and L3 each contribute ~13-18 percentage points.
- **Context economy:** peak context ~70k tokens with HCC vs >200k tokens without, on the representative task *random-acts-of-pizza*.

---

## Suggestions & Future Directions

1. **Beyond MLE.** Authors frame the work as a blueprint for broader agentic science; extending HCC to chemistry, biology, and physics is the main stated direction.
2. **Beyond human precedent.** The paradigm aims at tasks exceeding human-expert complexity, where cross-task wisdom accumulation is the only path forward.
3. **Scaling to longer horizons.** Implicit direction toward multi-week or multi-month cycles with thousands of intermediate steps.
4. **Ablation robustness.** The paper notes ablations used a single seed on MLE-Bench-Lite due to compute cost -- more statistically robust evaluations are an open gap.
5. **Cross-domain transfer of wisdom (L3).** Current L3 is populated by 407 Kaggle competitions; generalizing wisdom across scientific domains is unexplored.

---

## Authors & Institutions

Xinyu Zhu, Yuzhu Cai, Zexi Liu, Bingyang Zheng, Cheng Wang, Rui Ye, Weinan E, Siheng Chen, Yanfeng Wang (Shanghai Jiao Tong University, School of Artificial Intelligence); Yuzhi Zhang, Linfeng Zhang (DP Technology); Yuzhu Cai, Yanfeng Wang (also Shanghai AI Laboratory).
