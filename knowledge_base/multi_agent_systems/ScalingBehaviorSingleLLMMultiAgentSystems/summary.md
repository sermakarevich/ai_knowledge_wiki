# Scaling Behavior of Single LLM-Driven Multi-Agent Systems

**Paper:** [Scaling Behavior of Single LLM-Driven Multi-Agent Systems (Jialing Li, Zhouhong Gu, Yin Cai, Hongwei Feng, 2026)](https://arxiv.org/abs/2606.00655)

## Human Readable TL;DR

Imagine you're trying to solve a puzzle, and you add more people to help. At first more helpers is better -- they catch each other's mistakes and bring different ideas. But add too many, and they start stepping on each other's toes: too much back-and-forth, contradictions pile up, and the group gets confused. This paper shows the same thing happens with AI agents: adding more AI "workers" to a team starts helping but quickly starts hurting, and the sweet spot is surprisingly small. The takeaway is that a smarter team design matters far more than a bigger team.

## TL;DR

This paper studies how performance of homogeneous LLM-based Multi-Agent Systems (MAS) scales with agent count using SIMAS, a minimalist sequential-communication framework. Performance follows an inverted-U curve: collaborative synergy improves results up to an optimal agent count n*, then coordination overhead causes decline. This pattern is causally driven by coordination overhead (not context length), persists across interaction architectures (AutoGen debate), and critically depends on base model capability and task type. Collective intelligence is an emergent property of architectural design, not a guaranteed outcome of adding agents.

---

## Problem & Motivation

LLM-based Multi-Agent Systems (MAS) have proliferated rapidly, yet fundamental questions about how their performance scales with agent count remain unanswered. Prior work conflates model heterogeneity, tool use, and specialized workflows with collaboration effects, making it impossible to isolate scaling dynamics. The paper asks: when all agents use the same LLM, does adding more agents consistently improve performance -- and if not, why?

---

## Main Original Ideas

1. **SIMAS (Sequential Iterative Multi-Agent System):** A minimalist MAS architecture where n homogeneous agents communicate sequentially over T rounds, each building on the progressively accumulated conversation history. The first agent synthesizes the final answer. This bare-bones design strips away workflow engineering to expose raw scaling dynamics.

2. **Inverted-U Scaling Law:** MAS performance is not monotonically increasing with agent count. It rises due to collaborative synergy (diverse perspectives, mutual error correction) then falls as coordination overhead (information redundancy, conflicting reasoning paths) dominates. This law is architectural and universal, not a quirk of SIMAS.

3. **Sufficiency Threshold:** Only models above a capability threshold (typically 70B+) can effectively power MAS. Small models (7B/8B) exhibit monotonic degradation -- they fail to benefit from collaboration at all, making the inverted-U collapse entirely.

4. **Pseudo-Stability at High Agent Count:** Beyond the performance peak, output stability paradoxically recovers -- not from robust collaboration but from consistently wrong consensus. This "pseudo-stability" is a diagnostic signal for collective failure.

5. **Coordination Overhead Causality:** A controlled token-padding experiment (fixing total context length while varying agent count) confirms that performance degradation is caused by coordination overhead -- the semantic noise from multiple conflicting reasoning paths -- not by long-context failure of the LLM.

6. **Collective Intelligence as Emergent Property:** Minimalist MAS (SIMAS) frequently underperforms a single agent using CoT prompting on reasoning tasks. Structured architectures (AutoGen debate, Multi-Agent Debate) surpass CoT by engineering synthesis and critique loops -- proving that collective intelligence must be designed, not assumed.

---

## Key Findings

| Finding | Description |
|---------|-------------|
| Inverted-U law | Performance peaks at n* then declines; token cost scales quadratically with n |
| Model capability prerequisite | 7B/8B models cannot benefit from MAS; 70B/72B models are needed |
| Task-type modulation | Reasoning tasks (abstract algebra, formal logic) degrade sharply; knowledge tasks (philosophy, global facts) are more tolerant |
| Coordination overhead causality | Inverted-U persists under fixed context length (token-padding experiment) |
| Cross-architecture generality | AutoGen GroupChat debate shows the same inverted-U, though with higher peak and delayed onset |
| CoT vs. SIMAS | CoT matches or outperforms SIMAS on reasoning benchmarks; SIMAS fails catastrophically on AIME 2025 |
| Pseudo-stability | Stability paradoxically increases at very high n due to consistently wrong consensus |

**Architecture comparison on math benchmarks (from Gu et al., 2025):**

| Architecture | Model | GSM8K | AIME 2024 |
|---|---|---|---|
| Naive-CoT | Qwen2.5-72B | 75.13 | 10.0 |
| Naive-CoT | Llama-3.1-70B | 87.33 | 16.7 |
| AutoGen | Qwen2.5-72B | 81.80 | 16.7 |
| AutoGen | Llama-3.1-70B | 85.21 | 20.0 |
| Multi-Agent Debate | Llama-3.1-70B | 90.82 | 20.0 |
| SIMAS | -- | Underperforms CoT on reasoning | -- |

---

## Suggestions & Future Directions

1. **Heterogeneous agents:** Study MAS where agents use different LLMs or have access to different tools -- complementarity may shift scaling dynamics.
2. **Advanced coordination mechanisms:** Explore voting, dynamic workflows, and hierarchical/DAG topologies to understand how architectural safeguards mitigate overhead.
3. **Psycholinguistic analysis:** Deeper analysis of agent dialogues -- semantic diversity, conversational dynamics, belief divergence -- to characterize micro-level mechanisms of collaboration breakdown.
4. **Beyond closed-book QA:** Evaluate on longitudinal, creative, or tool-augmented tasks where collaborative benefits may be more pronounced.
5. **Larger agent collectives:** Scaling beyond 8 agents (e.g., hundreds as in MacNet) to explore novel emergent phenomena in much larger collectives.
6. **Adaptive collaboration protocols:** Design task-aware MAS that dynamically adjusts agent count and interaction structure rather than using fixed configurations.

---

## Authors & Institutions

Jialing Li (Fudan University), Zhouhong Gu (Fudan University), Yin Cai (Fudan University), Hongwei Feng (Fudan University, corresponding author)
