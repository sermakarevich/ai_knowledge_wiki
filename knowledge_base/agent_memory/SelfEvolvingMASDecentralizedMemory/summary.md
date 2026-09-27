# Self-Evolving Multi-Agent Systems via Decentralized Memory

**Paper:** [Self-Evolving Multi-Agent Systems via Decentralized Memory (Hao, Long, Zhao, 2026)](https://arxiv.org/abs/2605.22721)

## Human Readable TL;DR

Imagine a team of specialists -- a doctor, a lawyer, an engineer -- who share the same notes folder. Over time, they all start solving problems the same way because they keep reading each other's playbooks, and the diversity that made the team useful in the first place gradually disappears. This paper argues that AI agent teams have exactly the same problem: when all agents share one memory bank, they start behaving identically. The fix is simple: give each agent their own private memory with two compartments -- one for "things that worked before" and one for "try something new" -- and let a judge AI figure out which compartment each agent should draw from at each step. The result is a team that stays diverse, learns faster, and uses far fewer resources than teams with shared memory.

## TL;DR

DECENTMEM introduces a decentralized memory framework for LLM-based multi-agent systems (MAS) in which each agent maintains a private dual-pool memory: an exploitation pool (E-pool) of consolidated past trajectories and an exploration pool (X-pool) of LLM-generated candidates for novel contexts. An online router, guided by an LLM-as-a-judge evaluating stage-wise feedback, dynamically reweights the two pools so each agent learns its own exploitation--exploration balance. The paper proves global reachability of each agent's solution subspace and O(log T) cumulative regret (order-optimal vs. the bandit lower bound). Across 3 MAS frameworks, 5 LLM backbones, and 5 benchmarks, DECENTMEM improves average accuracy by up to 23.8% over the strongest centralized baseline and reduces token usage by up to 49%.

---

## Problem & Motivation

The dominant memory design in LLM-based MAS is a centralized shared repository -- a pattern inherited directly from single-agent architectures (MetaGPT's global message pool, G-Memory's hierarchical graph). This design is fundamentally incompatible with self-evolution in multi-agent settings: when all agents retrieve from the same pool, their behaviors homogenize over time and converge to a single dominant strategy regardless of their initial distinct roles. The diversity that motivates using multiple agents is gradually lost. Centralization also imposes high communication overhead, synchronization costs, and privacy risks. Despite these well-known limitations, decentralized memory architectures for MAS remain underexplored.

---

## Main Original Ideas

1. **Decentralized Dual-Pool Memory** -- Each agent independently maintains an E-pool (consolidated trajectories from past tasks, encoding action taken + cooperation trajectory passed to subsequent agents + self-commentary on rationale) and an X-pool (temporary buffer for the current task, generates novel LLM candidates for unseen contexts). Memory never leaves the agent that earned it, preserving role-complementary specialization.

2. **Online Pool Router via LLM-as-a-Judge** -- At each stage, the router selects between E-pool (probability proportional to its weight vs. fixed X-pool weight 1.0) and retrieves top-K similar memories above a similarity threshold τ, falling back to X-pool if no match. After task completion, an LLM judge evaluates every stage (correctness, allocation quality, coherence, integration); E-pool weight increases on successful exploitation and decays on successful exploration, preventing over-commitment in either direction.

3. **Graph-Walk-with-Teleportation Formulation** -- The paper models MAS self-evolution as a random walk over a graph-structured solution space G. The E-pool implements a local walk (exploiting similarity-based transitions) while the X-pool implements heuristic teleportation (injecting nonzero probability mass into every region via the LLM prior). This mixed process is provably irreducible and aperiodic, guaranteeing global reachability -- no agent can be permanently trapped in a local optimum.

4. **Stochastic Bandit Routing with Optimal Regret** -- Online pool routing is cast as a stochastic bandit problem. Under a strictly concave reward function assumption with a unique optimal mixing ratio α*, the adaptive weight update achieves O(log T) cumulative regret, matching the Ω(log T) lower bound. Fixed routing policies incur Θ(T) regret and are asymptotically dominated.

5. **Plug-in Design Agnostic to MAS Framework** -- DECENTMEM integrates as a drop-in module into any MAS framework (pre-designed workflows, dynamic, or opportunistic coordination), and the performance advantage grows monotonically as coordination becomes more stochastic -- indicating that decentralized memory matters most precisely when centralized memory homogenizes behavior most aggressively.

---

## Key Findings

| Metric | Value |
|--------|-------|
| **Best avg. accuracy configurations** | 14 of 15 (backbone, framework) cells |
| **Avg. relative gain vs. G-Memory (strongest centralized)** | +8.6% |
| **Avg. relative gain vs. no-memory baseline** | +26.1% |
| **Peak gain vs. no-memory** | +52.5% (Qwen3-4B + AgentNet) |
| **Token reduction vs. G-Memory on BBH** | 32% / 49% / 47% (AgentNet/DyLAN/AutoGen); 43% avg. |
| **Learning speed advantage** | ~2.5× faster convergence on DyLAN + MBPP-Plus |

- Gain over centralized baselines widens monotonically with coordination stochasticity: Qwen3 margins are 2.7% (AutoGen) → 9.2% (DyLAN) → 23.1% (AgentNet); Gemma4: 1.7% → 3.9% → 6.8%.
- Ablation confirms online routing is critical: replacing it with pure Exploitation Only drops accuracy 6.93% / 3.51% / 3.38% on AgentNet / DyLAN / AutoGen. Pure Exploration Only collapses on experience-dependent tasks (BBH) but remains competitive on fresh reasoning (AIME).
- Fixed equal-weight routing (α=0.5) incurs Θ(T) regret and is asymptotically dominated -- confirmed both theoretically and empirically.
- DECENTMEM achieves best accuracy in AgentNet configurations at significantly lower token cost than even the no-memory baseline in some cases (localized retrieval avoids centralized read/write overhead).

---

## Suggestions & Future Directions

1. **Broader task domains** -- Validate DECENTMEM on high-stakes, long-horizon tasks such as legal and medical reasoning, where accumulated specialized expertise is critical and homogenization risk is highest.
2. **Selective cross-agent memory sharing** -- Explore controlled mechanisms for agents to optionally share high-quality memories without full centralization (collaborative memory with dynamic access control).
3. **Adaptive similarity threshold τ** -- The current fixed threshold for E-pool retrieval fallback could be made adaptive to task distribution drift over time.
4. **Larger-scale model backbones** -- The current evaluation uses models up to 14B parameters; validating with frontier-scale models would test whether gains persist at higher baseline capability.
5. **Multi-agent scaling laws** -- Study how DECENTMEM's gains scale with the number of agents M, particularly in opportunistic coordination regimes.

---

## Authors & Institutions

Guangya Hao (University of Cambridge), Yunbo Long (University of Cambridge), Zhuokai Zhao (University of Chicago)
