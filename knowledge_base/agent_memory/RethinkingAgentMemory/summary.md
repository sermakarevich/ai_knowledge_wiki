# Rethinking Memory Mechanisms of Foundation Agents in the Second Half: A Survey

**Paper:** [Rethinking Memory Mechanisms of Foundation Agents in the Second Half: A Survey (Huang, Zhang, Liang et al., 2026)](https://arxiv.org/abs/2602.06052)

## Human Readable TL;DR

Imagine hiring a personal assistant who forgets everything after each shift -- no notes from yesterday, no idea who you are, no record of what worked before. That's what current AI agents are like. This paper is a comprehensive handbook for giving AI agents a proper memory system: remembering who they're helping, what they've learned, and how to get better over time. It maps out all the different types of memory an AI agent needs (like short-term focus, long-term facts, learned skills), where to store it, and how to teach the agent to manage it well.

## TL;DR

This survey proposes a unified three-dimensional taxonomy for foundation agent memory along axes of substrate (internal vs. external), cognitive mechanism (sensory, working, episodic, semantic, procedural), and subject (user-centric vs. agent-centric). It argues that the "second half" of AI shifts from benchmark performance to real-world utility, where memory is the critical enabler for agents operating in long-horizon, dynamic, and personalized environments. The paper synthesizes 218 papers (2023--2025), analyzes memory operations, learning policies, scaling challenges, and outlines six open research directions.

---

## Problem & Motivation

Current foundation models achieve impressive benchmark scores but fail in real-world deployment due to **context explosion** -- the inability to handle the volume and dynamism of information in long-horizon, multi-session, and user-dependent settings. Agents forget prior interactions, cannot personalize to users, and cannot accumulate expertise over time. Memory is identified as the natural and critical solution to bridge this "utility gap" between benchmark performance and practical deployment.

---

## Main Original Ideas

1. **"Second Half" Framing** -- The paper reframes the next era of AI development around problem definition and real-world utility rather than scaling and benchmark optimization. Memory is the foundational infrastructure for this shift.

2. **Three-Dimensional Memory Taxonomy** -- A novel orthogonal taxonomy classifying memory along three independent axes:
   - *Substrate*: how memory is physically stored (internal: weights, latent states, KV cache; external: vector index, text-record, structural store, hierarchical store)
   - *Cognitive Mechanism*: functional role (sensory, working, episodic, semantic, procedural)
   - *Subject*: whose needs are served (user-centric for personalization; agent-centric for skill/knowledge accumulation)

3. **Memory Operation Framework** -- Systematic decomposition of memory management into five core operations: storage & indexing, loading & retrieval, updates & refresh, compression & summarization, and forgetting & retention.

4. **Multi-Agent Memory Architecture Taxonomy** -- Classification of memory sharing models in multi-agent systems: private-only, shared-workspace, hybrid, and orchestrated -- plus memory routing and conflict resolution mechanisms.

5. **Memory Learning Policies** -- Categorization of how agents learn to manage memory: prompt-based (static rules or dynamic reflection), fine-tuning (parameterized policies), and reinforcement learning (step-level, trajectory-level, cross-episode).

---

## Key Findings

| Memory Substrate | Strengths | Weaknesses |
|---|---|---|
| External (vector/text/structural) | Scalable, explicitly updatable, human-readable | Retrieval latency, management overhead, reliability |
| Internal (weights/latent/KV cache) | Speed, tight model integration | Costly updates, catastrophic forgetting, transient |
| Hybrid | Balances speed & persistence | Architectural complexity |

| Cognitive Type | Function | Key Challenge |
|---|---|---|
| Working memory | Active task context, multi-step reasoning | Capacity constraints |
| Episodic memory | Cross-session continuity from past experiences | Retrieval relevance |
| Semantic memory | Stable factual/conceptual knowledge | Keeping up-to-date |
| Procedural memory | Reusable skills and action routines | Generalization vs. overfitting |
| Sensory memory | Raw perceptual input retention | Mostly implicit in multimodal agents |

- Effective real-world systems consistently adopt **hybrid internal+external** architectures.
- Memory management is increasingly **learned** (via RL or fine-tuning) rather than hard-coded.
- Existing benchmarks (WebArena, SWE-Bench, MemoryBank) are insufficient -- they lack long-horizon, preference drift, and memory integrity evaluation.

---

## Suggestions & Future Directions

1. **Memory for Continual Learning and Self-Evolving Agents** -- Agents that improve autonomously from accumulated experience without catastrophic forgetting.
2. **Multi-Human-Agent Memory Organization** -- Shared memory architectures that handle information asymmetry, conflict resolution, and privacy boundaries across multiple users and agents.
3. **Memory Infrastructure and Efficiency** -- Scalable, low-latency retrieval and storage systems for production-grade agent deployments.
4. **Life-Long Personalization and Trustworthy Memory** -- Privacy-preserving, auditable, and manipulation-resistant memory for sensitive domains (healthcare, legal, finance).
5. **Memory for Multimodal, Embodied, and World-Model Agents** -- Extending memory taxonomies to handle vision, audio, and physical-world state.
6. **Real-World Benchmarking and Evaluations** -- New benchmarks that assess sustained adaptation, preference drift, and memory integrity under realistic long-horizon constraints.

---

## Authors & Institutions

Wei-Chieh Huang, Weizhi Zhang, Yueqing Liang (co-first authors); Yuanchen Bei, Yankai Chen, Tao Feng, Xinyu Pan, Zhen Tan, Yu Wang, Tianxin Wei, Shanglin Wu, Ruiyao Xu, Liangwei Yang, Rui Yang, Wooseong Yang, Chin-Yuan Yeh, Hanrong Zhang, Haozhen Zhang, Siqi Zhu, Henry Peng Zou (core contributors); Philip S. Yu, Kai Shu, Julian McAuley, James Zou, Jiawei Han, Xue Steve Liu, Yizhou Sun, Wei Wang (senior supervisors).

**Institutions:** UIC, IIT, UIUC, UW-Madison, ASU, Emory, Northwestern, NTU, UCF, Rutgers, Cambridge, Harvard, UTokyo, UCSD, UCSC, TAMU, UCSB, MBZUAI, McGill, UCLA, Stanford; Salesforce, Google, Meta, Roblox, Cisco, Capital One.
