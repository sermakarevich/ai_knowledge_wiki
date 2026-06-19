# Graph-based Agent Memory: Taxonomy, Techniques, and Applications

**Paper:** [Graph-based Agent Memory: Taxonomy, Techniques, and Applications (Yang et al., 2026)](https://arxiv.org/abs/2602.05665)

## Human Readable TL;DR

Imagine your AI assistant has a notebook where it writes down everything it learns -- but instead of a flat list of notes, the notebook is organized like a web of connected ideas, similar to how Wikipedia links articles together. This survey maps out all the different ways researchers are building these "web-notebook" memory systems for AI agents. It explains how you can store memories (as nodes and links in a graph), find the right memory when you need it, and how the memory can reorganize itself over time as the agent learns more -- ultimately making AI assistants smarter, more personalized, and less forgetful without needing to retrain them from scratch.

## TL;DR

This survey provides the first comprehensive taxonomy and lifecycle-based analysis of graph-based memory systems for LLM agents. It categorizes memory along temporal (short/long-term), cognitive (semantic, episodic, procedural, etc.), and functional (knowledge vs. experience) dimensions, then systematically reviews techniques for memory extraction, storage (knowledge graphs, hierarchical, temporal, hypergraph, hybrid), retrieval (six operator classes plus enhancement strategies), and evolution (internal self-evolving and external self-exploration). The paper also surveys open-source tools, benchmarks, and applications across eight domains, and closes with seven critical research challenges.

---

## Problem & Motivation

LLM-based agents face three fundamental limitations that prevent them from succeeding at long-horizon, complex tasks:

1. **Knowledge cutoff** -- LLMs are trained on static data and cannot incorporate real-time or domain-specific information after training.
2. **Tool incompetence** -- Agents struggle to efficiently learn and apply novel tools encountered post-deployment.
3. **Performance saturation** -- Agents repeatedly fail in iterative tasks because they cannot accumulate task-specific insights or learn from past errors across sessions.

Memory is the key remedy: it enables personalization, long-term reasoning beyond context windows, self-improvement without retraining, and hallucination mitigation via grounded retrieval. However, traditional memory implementations (linear buffers, vector databases, log-based storage) lack relational modeling and hierarchical organization. Graph-based memory addresses this gap, yet no unified survey existed before this paper. The work positions graph memory as "a frontier for 2025-2026 research" and provides the field's first structured reference.

---

## Main Original Ideas

1. **Unified Graph-Centric Taxonomy** -- The paper argues that all traditional memory types (lists, vectors, key-value stores) are degenerate special cases of graphs, making graph-based memory a general, unifying framework rather than just one option among many.

2. **Multi-Dimensional Memory Classification** -- Memory is categorized along three orthogonal axes: (a) temporal scope (short-term vs. long-term), (b) cognitive structure mirroring human memory (semantic, procedural, associative, working, episodic, sentiment), and (c) functional role (Knowledge Memory -- static/objective vs. Experience Memory -- dynamic/personalized/situated).

3. **Lifecycle-Based Analysis Framework** -- The survey introduces a four-stage memory lifecycle as the organizing principle: Extraction (raw data to structured memory units), Storage (graph structure selection and construction), Retrieval (finding relevant memory content), and Evolution (updating and refining memory over time). This lifecycle framing is the paper's core methodological contribution.

4. **Graph Storage Typology** -- Five graph structure families are systematically compared for memory storage: Knowledge Graphs (entity-relation triples), Hierarchical Structures (tree-like for multi-level organization), Temporal Graphs (time-stamped nodes/edges for recency and sequence), Hypergraph Structures (hyperedges for n-ary relations), and Hybrid Architectures (combining multiple types).

5. **Retrieval Operator Taxonomy** -- Six base retrieval operators are identified: Similarity-based, Rule-based, Temporal-based, Graph-based (traversal/path), Reinforcement Learning-based, and Agent-based. These are combined with three enhancement strategies: Multi-round retrieval, Post-retrieval processing, and Hybrid-source integration.

6. **Self-Evolving Memory Paradigm** -- The paper introduces a two-axis evolution framework: (a) Internal Self-Evolving (Memory Consolidation, Graph Reasoning, Graph Reorganization -- maintaining consistency and efficiency within the graph) and (b) External Self-Exploration (Feedback-driven Adaptation and Active Inquiry -- grounding memory in real-world feedback and proactively seeking new knowledge).

7. **Benchmark Taxonomy** -- Benchmarks are classified by scenario type: Interaction, Personalization, Web, LongContext, Continual, Environments, and Tool/Generation -- with each evaluated against modality, environment realism, and memory type coverage.

---

## Key Findings

### Storage Structure Comparison

| Graph Type | Best For | Key Strength | Key Weakness |
|---|---|---|---|
| Knowledge Graph | Semantic/factual memory | Relational reasoning, structured retrieval | Static schema, sparse relations |
| Hierarchical Graph | Multi-level organization | Efficient abstraction, summarization | Rigid hierarchy, hard to update |
| Temporal Graph | Sequential/episodic memory | Recency modeling, event ordering | High storage overhead |
| Hypergraph | Complex n-ary relations | Rich relational modeling | Computational complexity |
| Hybrid Architecture | Mixed memory types | Flexibility, coverage | Integration complexity |

### Retrieval Operator Summary

| Operator Type | Mechanism | Suited For |
|---|---|---|
| Similarity-based | Embedding cosine/vector search | Semantic memory lookup |
| Rule-based | Logic rules, SPARQL-like queries | Structured knowledge retrieval |
| Temporal-based | Recency weighting, time-window filtering | Episodic memory |
| Graph-based | Path traversal, graph algorithms | Multi-hop relational reasoning |
| RL-based | Policy-driven adaptive search | Dynamic, reward-shaped retrieval |
| Agent-based | LLM-driven iterative retrieval | Complex, open-ended queries |

### Application Domains Covered

- Conversational agents (multi-turn dialogue, personalization)
- Code agents (workflow memory, tool learning)
- Recommender systems (user preference graphs)
- Financial agents (market knowledge graphs)
- Game agents (open-world exploration, strategy memory)
- Robotics (embodied experience memory)
- Medical agents (clinical knowledge and patient history)
- Science agents (literature and experimental knowledge)

---

## Suggestions & Future Directions

1. **Memory Graph Quality** -- Ensuring accuracy, consistency, and completeness of extracted graph memory; noise and hallucinations in LLM-extracted triples remain a critical open problem.

2. **Scalability and Efficiency** -- Managing exponentially growing graphs in long-running agents; need for more efficient indexing, pruning, and compression strategies.

3. **Privacy and Security** -- Graph memory can leak sensitive user information; differential privacy, access control, and adversarial robustness of memory graphs need dedicated research.

4. **Dynamic Schema Learning** -- Current graph schemas are largely hand-designed; agents should be able to discover and adapt ontological structures autonomously from experience.

5. **Interpretability and Trustworthiness** -- Graph memory should provide transparent, auditable reasoning traces; bridging graph structure with explainable AI techniques.

6. **Theoretical Foundations** -- Formal guarantees on memory capacity, retrieval completeness, and evolution convergence are largely absent; grounding graph memory in information-theoretic and computational frameworks.

7. **Multi-Agent Memory Coordination** -- Shared and distributed graph memory across agent collectives introduces consistency, synchronization, and conflict resolution challenges that current work does not adequately address.

---

## Authors & Institutions

Chang Yang, Chuang Zhou, Yilin Xiao, Su Dong, Luyao Zhuang, Yujing Zhang, Zhu Wang, Zijin Hong, Zheng Yuan, Shengyuan Chen, Huachi Zhou, Qinggang Zhang, Ninghao Liu, Xiao Huang -- The Hong Kong Polytechnic University, Hong Kong SAR, China; Jinsong Su, Zhishang Xiang -- School of Information, Xiamen University, China; Xinrun Wang -- Singapore Management University, Singapore; Yi Chang -- Jilin University, China.

**GitHub resource list:** https://github.com/DEEP-PolyU/Awesome-GraphMemory
