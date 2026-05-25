# Memory in the Age of AI Agents: A Survey

**Paper:** [Memory in the Age of AI Agents: A Survey (Hu et al., 2025)](https://arxiv.org/abs/2512.13564)

## Human Readable TL;DR

Imagine you hire an assistant, but every day they wake up with complete amnesia -- they can't remember your name, your preferences, or anything you worked on together. That's the current problem with many AI agents. This survey is like a comprehensive textbook that organizes all the different ways researchers have tried to give AI assistants a "memory" -- from sticky notes (text files) to muscle memory (built-in skills) to short-term focus (what they're paying attention to right now). It maps out what memory looks like, what jobs it does, and how it changes over time, giving the field a shared vocabulary to talk about the same things.

## TL;DR

This survey proposes a unified "Forms--Functions--Dynamics" (FFD) taxonomy for agent memory, addressing fragmentation and conceptual ambiguity in a rapidly growing field. It distinguishes agent memory from related concepts (LLM memory, RAG, context engineering) and classifies memory by three representational forms (token-level, parametric, latent), three functional roles (factual, experiential, working), and three lifecycle processes (formation, evolution, retrieval). The paper compiles benchmarks, open-source frameworks, and identifies eight frontier research directions.

---

## Problem & Motivation

LLM-based agents require persistent, adaptive memory to support long-horizon reasoning and continual learning, yet the research field has fragmented into inconsistent terminologies and incompatible taxonomies. The classic long-term/short-term dichotomy is insufficient -- dozens of systems define "episodic," "semantic," or "parametric" memory in conflicting ways. This survey directly addresses this by providing a principled, comprehensive taxonomy that reconciles existing definitions and bridges emerging trends.

---

## Main Original Ideas

1. **Forms--Functions--Dynamics (FFD) Taxonomy** -- A unified three-axis framework for classifying any agent memory system. "Forms" addresses where/how memory is stored, "Functions" addresses why it exists, and "Dynamics" addresses how it operates and evolves across time.

2. **Three Memory Forms** -- Token-level memory (explicit, human-readable text organized flat/planar/hierarchically), parametric memory (encoded into model weights, internal or via adapters), and latent memory (implicit KV-cache/hidden-state representations, generated/reused/transformed).

3. **Three Functional Roles** -- Factual memory (declarative knowledge about users and environments), experiential memory (procedural knowledge: cases, strategies, skills), and working memory (capacity-limited, dynamically managed scratchpad for active context).

4. **Three Dynamic Processes** -- Memory formation (encoding raw experience into compact knowledge via summarization, distillation, graph construction, latent encoding, or parametric internalization), memory evolution (consolidation, updating, forgetting), and memory retrieval (timing, query construction, search strategies, post-retrieval processing).

5. **Conceptual Delineation** -- Rigorous separation of agent memory from LLM memory (KV-cache/architecture), RAG (static external retrieval for single inference), and context engineering (optimizing the context window payload), establishing clean definitional boundaries.

---

## Key Findings

| Dimension | Subcategory | Representative Systems |
|-----------|-------------|----------------------|
| **Token-level (Flat)** | Dialogue logs, preference lists | MemGPT, Memento |
| **Token-level (Planar)** | Knowledge graphs, trees | A-Mem, MemTree |
| **Token-level (Hierarchical)** | Multi-layer pyramid structures | HiAgent, HippoRAG |
| **Parametric (Internal)** | Fine-tuning, model editing | ROME, MEND, Character-LM |
| **Parametric (External)** | LoRA adapters | K-Adapter, WISE |
| **Latent (Generate)** | Gist tokens, summary vectors | AutoCompressor, MemGen |
| **Latent (Reuse)** | KV-cache reuse | Memorizing Transformers, SirLLM |
| **Latent (Transform)** | KV compression/selection | SnapKV, Scissorhands |
| **Factual (User)** | User preferences, commitments | MemoryBank, RMM |
| **Factual (Env)** | Documents, tool states | MetaGPT, Generative Agent |
| **Experiential (Case)** | Raw trajectory replay | Expel, Memento |
| **Experiential (Strategy)** | Reasoning patterns, workflows | Reflexion, AWM |
| **Experiential (Skill)** | Code/API libraries | Voyager, ToolLLM, Alita |
| **Working (Single-turn)** | Input compression | LLMLingua, VideoAgent |
| **Working (Multi-turn)** | State across sessions | MemAgent, KARMA |

- Token-level flat memory dominates current systems due to ease of implementation and scalability, but sacrifices relational reasoning.
- Parametric memory offers zero-latency access but suffers from catastrophic forgetting and high update costs.
- Latent memory is underexplored despite its efficiency advantages for multimodal fusion.
- Working memory is the most actively engineered function, driven by practical context-window limitations.

---

## Suggestions & Future Directions

1. **Memory Generation vs. Retrieval** -- Shift from static retrieval to actively synthesizing context-adaptive memory representations.
2. **Automated Memory Management** -- Replace manually designed rules with self-optimizing, autonomously managed architectures capable of dynamic environments.
3. **RL Meets Agent Memory** -- Use reinforcement learning to internalize memory selection, design, and evolution for genuinely continual learning.
4. **Multimodal Memory** -- Develop omnimodal memory that integrates visual, audio, and text inputs for embodied agent settings.
5. **Shared Memory in Multi-Agent Systems** -- Evolve shared repositories from passive stores to actively managed, learning-driven collective representations.
6. **Memory for World Models** -- Advance memory beyond data caching to interactive internal simulations of the world.
7. **Trustworthy Memory** -- Address privacy (granular permissions, verifiable forgetting), explainability (auditable updates), and hallucination robustness (causal tracing).
8. **Human-Cognitive Connections** -- Draw from biological memory (constructive memory, sleep-like offline consolidation) to build more efficient and robust learning mechanisms.

---

## Authors & Institutions

Yuyang Hu, Shichun Liu, Yanwei Yue, Guibin Zhang (core contributors, project organizer) + 41 co-authors from National University of Singapore, Renmin University of China, Fudan University, Peking University, Nanyang Technological University, Tongji University, UC San Diego, HKUST (Guangzhou), Griffith University, Georgia Institute of Technology, OPPO, Oxford University.
