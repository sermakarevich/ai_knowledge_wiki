# Drop the Hierarchy and Roles: How Self-Organizing LLM Agents Outperform Designed Structures

**Paper:** [Drop the Hierarchy and Roles: How Self-Organizing LLM Agents Outperform Designed Structures (Dochkina, 2026)](https://arxiv.org/abs/2603.28990)

## Human Readable TL;DR

Imagine you're assembling a team to solve a problem. The usual approach is to assign everyone a specific job title and have a boss coordinate them. This study ran 25,000 experiments with AI agents and found something surprising: the best approach is neither a strict boss-controlled team nor a free-for-all. Instead, a simple "take turns and decide your own role" system -- like a sports draft where each pick sees all previous picks -- beat both extremes. The AI agents spontaneously invented over 5,000 unique job titles, voluntarily sat out tasks they weren't suited for, and even formed their own shallow management layers -- all without being told to.

## TL;DR

A 25,000-task experiment across 8 LLMs, 4--256 agents, and 8 coordination protocols reveals an "endogeneity paradox": a hybrid Sequential protocol (fixed agent ordering, autonomous role selection) outperforms centralized coordination by +14% and fully autonomous coordination by +44%. Effective self-organization requires both a capable model and the right protocol; below a capability threshold, rigid structure outperforms autonomy. The system scales sub-linearly to 256 agents with emergent properties including dynamic role invention (5,006 unique roles from 8 agents), voluntary self-abstention, and spontaneous hierarchy formation.

---

## Problem & Motivation

Multi-agent LLM systems (ChatDev, MetaGPT, AutoGen) replicate human organizational patterns: fixed roles, centralized task allocation, and rigid hierarchies. But LLM agents are fundamentally different from human workers -- they can instantly switch specializations, process full organizational context, and contribute zero marginal cost when idle. Pre-assigning fixed roles may unnecessarily constrain them.

The core question had not been systematically studied: how does the degree of agent autonomy in coordination -- from centralized to fully self-organized -- affect collective performance at scale? Prior work tested at most ~12 agents, 1--2 models, and 1--3 protocols.

---

## Main Original Ideas

1. **Exogenous-to-endogenous coordination spectrum.** A formal framework classifying 8 protocols from fully externally controlled (Coordinator) to fully self-organized (Shared), with systematic empirical comparison across all of them.

2. **The endogeneity paradox.** Neither maximal control nor maximal autonomy is optimal. The hybrid Sequential protocol -- where agent ordering is fixed but role selection is autonomous -- outperforms both extremes. Each agent observes completed predecessor outputs (facts, not intentions or history), naturally filling complementary roles like a sports draft.

3. **Capability threshold for self-organization.** Self-organization is a privilege of strong models. Below a capability threshold (lacking self-reflection, deep reasoning, or instruction following), autonomy hurts and rigid structure helps -- a reversal effect.

4. **Three-ring constitutional framework.** A governance model for autonomous multi-agent organizations: Ring 1 (immutable core -- mission/values, human-only), Ring 2 (standards -- human + system), Ring 3 (protocols -- full system autonomy with A/B testing). The closer to "why," the more human control; the closer to "how," the more system autonomy.

---

## Key Findings

### Protocol Comparison (Pilot: N=8, GPT-4.1-mini; Final: N=16, Claude Sonnet 4.6)

| Protocol | Type | Q (pilot) | Q (L3 final) | Balance | Resilience |
|---|---|---|---|---|---|
| Coordinator | Centralized | 0.640 | 0.767 | 0.478 | 0.774 |
| **Sequential** | **Hybrid** | **0.724** | **0.875** | **0.510** | **0.829** |
| Broadcast | Signal-based | 0.510 | -- | 0.363 | 0.580 |
| Shared | Fully autonomous | 0.503 | -- | 0.369 | 0.589 |

- Sequential vs. Shared: +44%, Cohen's d = 1.86, p < 0.0001
- Sequential vs. Coordinator: +14%, p < 0.001 (replicated across Claude, DeepSeek, GLM-5)

### Scaling (4 to 256 agents)

| N | Quality | Cost (tokens) |
|---|---|---|
| 8 | 0.954 | 3,164 |
| 64 | 0.949 | 3,537 |
| 256 | 0.967 | -- |

- No significant quality degradation from 64 to 256 agents (p = 0.61)
- Cost grows only 11.8% for an 8x increase in agents (series 2)
- ~45% of agents self-abstain at N=256 -- an endogenous cost-optimization mechanism

### Open-Source vs. Closed-Source (N=16, Sequential, L3 tasks)

| Model | Quality | Cost (tokens) | Efficiency (Q/1K tok) |
|---|---|---|---|
| Claude Sonnet 4.6 | 0.875 | 37K | 0.0236 |
| DeepSeek v3.2 | 0.829 | 47K | 0.0177 |
| GLM-5 | 0.800 | 57K | 0.0140 |

- DeepSeek achieves 95% of Claude's quality at 24x lower cost
- Protocol choice (44% quality variation) exceeds model choice (~14%) among strong models

### Emergent Properties

- **Dynamic role invention:** 5,006 unique roles from 8 agents; Role Stability Index converges to 0 (agents reinvent roles per task)
- **Voluntary self-abstention:** 38/60 non-contributing agents withdrew voluntarily (Sequential) vs. 60/60 excluded by coordinator directive
- **Spontaneous hierarchy:** Hierarchy depth grows from 1.0 to only 2.0 when scaling from 4 to 64 agents -- consistently flat structures
- **Shock resilience:** Quality recovers within 1 iteration from agent removal or model substitution

---

## Suggestions & Future Directions

1. **Validation on real-world tasks.** Current tasks are synthetic; deploying Sequential self-organization on authentic business workflows (regulatory analysis, incident response) would test production viability.
2. **Batched Sequential for reduced latency.** The O(N) sequential latency can be mitigated by groups of K agents working in parallel, achieving O(N/K) latency while preserving informational advantage.
3. **Bio-inspired protocols.** Preliminary results on Morphogenetic, Clonal, Stigmergic, and Ripple protocols suggest Ripple (wave-based propagation) matches Sequential quality with greater parallelism; companion paper forthcoming.
4. **Combining vertical and horizontal intelligence.** Deploying self-improving agents (e.g., DGM-Hyperagents) within Sequential coordination to test whether gains compound multiplicatively.
5. **Constitutional governance in practice.** Live testing of the three-ring framework where Ring 3 protocols are autonomously optimized via A/B testing.
6. **LLM-as-judge limitation.** All evaluations use LLM judges (GPT-4o, GPT-5.4); human evaluation on a representative subset is planned for validation.

---

## Authors & Institutions

Victoria Dochkina (Moscow Institute of Physics and Technology -- MIPT, Moscow, Russia)
