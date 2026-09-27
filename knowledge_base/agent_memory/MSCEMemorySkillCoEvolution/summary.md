# From Memory to Skills: Evidence-Grounded Co-Evolution Governance for Long-Horizon LLM Agents

**Paper:** [From Memory to Skills: Evidence-Grounded Co-Evolution Governance for Long-Horizon LLM Agents (Tang et al., 2026)](https://arxiv.org/abs/2607.16621)

## Human Readable TL;DR

Imagine an intern who, every time they solve a task, jots a diary entry ("I did X, it worked/failed") but never turns those diary entries into an actual habit or checklist -- so tomorrow they're back to reasoning everything out from scratch. This paper builds a system that turns an AI agent's diary of past attempts into three levels of learning: raw notes of what happened, generalized "how-to" recipes it can call on demand, and a running mental map of how the environment behaves. The system is picky about which recipes get promoted to trusted, reusable "skills" -- only ones backed by real evidence of success get in -- and it grades earlier decisions using hindsight, similar to a coach reviewing game tape to figure out which specific plays actually won the match. The result is an agent that keeps getting better the more tasks it does, without anyone retraining the underlying model.

## TL;DR

The paper introduces **MSCE (Memory-Skill Co-Evolution)**, a training-free framework that organizes an LLM agent's experience into three memory tiers -- L1 grounded step traces, L2 reusable procedural policies, and L3 declarative environmental cognition -- and selectively crystallizes only evidence-backed, positive-gain, stable L2 policies into callable "skills." A reflection-weighted value-backfilling mechanism blends sparse terminal rewards with dense LLM-generated self-reflections to assign calibrated credit to each step. On EvoAgentBench (five agentic domains) and LoCoMo (long-context memory QA), MSCE beats the strongest baselines (e.g. SkillFlow-Evolve) by up to +15.4 Pass@1 points in software engineering and by 2.01/1.18 points on LoCoMo's judge score/F1, while ablations show every component (hierarchy, crystallization gate, L3 cognition, reflection weighting) contributes meaningfully.

---

## Problem & Motivation

Long-horizon LLM agents that operate over many episodes (coding tasks, research, multi-turn assistants) accumulate experience, but most existing memory systems just retrieve past trajectories as passive context stuffed back into the prompt. This has two failure modes: (1) raw trajectories are noisy and don't generalize -- the agent re-derives the same reasoning every time instead of reusing a proven procedure, and (2) there is no principled gate deciding *what* from memory deserves to become a trusted, reusable capability versus what was a one-off fluke. The paper frames the real problem as **governance**: not "how do we store memories" but "what becomes a skill, when does it apply, and how is it revised or retired." This distinguishes MSCE from prior memory-as-skill approaches (MemSkill, ProcMEM) that simply recast memory operations as skills without an evidence-gated promotion process.

---

## Main Original Ideas

1. **Three-level memory hierarchy (L1/L2/L3).** L1 is grounded step-trace memory: normalized state-action-observation-reflection-value records per step. L2 is policy memory: recurring procedural patterns with a trigger condition (ϕ), procedure (π), verification criteria (κ), and applicability boundaries (ℬ), linked back to supporting L1 evidence. L3 is declarative environmental cognition: factual knowledge about entities, action regularities, and constraints in the environment, linked to the L2 policies that rely on them.

2. **Evidence-gated skill crystallization.** Rather than treating every discovered policy as a skill, MSCE only promotes an L2 policy to a callable skill when it (a) retains supporting traces (real evidence it worked) and (b) has an estimated gain G(f²) above a threshold θ_G (set to 0, i.e. must be net-positive). Promoted skills inherit trigger/procedure/verification/boundaries from L2 and add evidence anchors (𝒜), decision guidance (𝒟), and a reliability estimate (η) -- making them auditable rather than opaque.

3. **Reflection-weighted value backfilling.** Terminal task rewards are sparse and uninformative about which specific step mattered. MSCE backfills a value to every step using V(f_{i,t}) = α_{i,t}·R_i + (1−α_{i,t})·γ·V(f_{i,t+1}), where α is a reflection weight estimated by having the LLM score how much a given step's self-reflection indicates it contributed to the outcome, and γ = 0.9 discounts future value. This couples the one sparse terminal signal with dense, per-step self-reflection to produce calibrated, step-level credit.

4. **Training-free, fully in-context design.** The entire framework operates without any weight updates -- memory construction, skill promotion, and value backfilling are all orchestrated via LLM calls and structured storage, so it can be layered on top of any base agent/backbone.

---

## Key Findings

**EvoAgentBench (Pass@1 %, MSCE vs. best baseline per domain):**

| Domain | MSCE | Best Baseline | Improvement |
|---|---|---|---|
| Information Retrieval | 26.15 | 21.54 | +4.61 pts |
| Mathematical Reasoning | 47.00 | 43.00 | +4.00 pts |
| **Software Engineering** | **53.85** | 38.46 | **+15.39 pts** |
| Code Implementation | 61.54 | 61.54 | tied |
| Knowledge Work | 53.45 | 48.28 | +5.17 pts |

**LoCoMo (judge-scored QA by question type, selected methods):**

| Method | Single | Multi | Temp. | Open | Overall | F1 |
|---|---|---|---|---|---|---|
| Vanilla Agent | 28.18 | 21.63 | 12.15 | 39.58 | 24.35 | 25.95 |
| SkillFlow-Evolve (strongest baseline) | 74.08 | 46.81 | 41.43 | 25.00 | 59.22 | 48.71 |
| **MSCE** | **75.98** | **47.87** | **44.24** | 28.13 | **61.23** | **49.89** |

MSCE outperforms SkillFlow-Evolve by **+2.01 overall judge score** and **+1.18 F1**, and clearly beats memory-only baselines (EverOS, Memento, MemSkill, OpenSpace) that don't gate skill promotion.

- **Ablations (Table 3):** removing the memory hierarchy entirely ("Flat Memory") costs -15.4 to -19.2 Pass@1 points; removing skill crystallization costs -6.2 to -11.5 points; removing L3 environmental cognition costs -3.0 to -5.9 points; removing reflection weighting costs -4.5 to -7.0 points -- every component matters, and the hierarchy + crystallization gate matter most.
- **Cross-domain transfer:** skills learned in one domain and applied to a different domain still yield an average **+3.93 point** gain across six transfer pairs, indicating the learned structure (not just domain-specific artifacts) generalizes.
- **Lifelong evolution:** Pass@1 improves monotonically as experience accumulates from p0 to p100 (+13.84 to +17.00 points), while normalized cost per task decreases after an initial accumulation phase -- the agent gets both better and cheaper over time.

---

## Suggestions & Future Directions

1. The governance signals used to decide promotion/value are **heuristic**, not causal credit-assignment estimates -- future work could explore more principled causal attribution of which steps truly drove success.
2. The framework depends on **prompted LLM operators** (for reflection scoring, skill extraction, etc.), which introduces latency and noise; more efficient or distilled scoring mechanisms are a natural next step.
3. **Storing normalized traces** raises ongoing privacy considerations even with truncation/redaction controls -- an area for further mitigation work.
4. Implicit open directions include extending skill governance to multi-agent settings and further scaling to longer task horizons than tested here.

---

## Authors & Institutions

Bo Tang, Yang Zhang, Guomian Zhuang, Wenqiang Wei, Gaoyang Zheng, Lindong Xie, Yanchao Tan, Feiyu Xiong, Qingyu Yang, Edward Chung, Zhiyu Li -- affiliated with **MemTensor**, **University of Science and Technology of China**, **Hong Kong Polytechnic University**, **Fuzhou University**, and **Xi'an Jiaotong University** (per-author affiliation mapping not specified in the source).
