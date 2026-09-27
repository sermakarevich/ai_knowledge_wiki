# Memory in the Age of AI Agents: A Survey -- Forms, Functions and Dynamics

**Paper:** [Memory in the Age of AI Agents: A Survey (Hu et al., 2026)](https://arxiv.org/abs/2512.13564)

## Human Readable TL;DR

Imagine you hired an assistant who forgets everything the moment you stop talking to them. Modern AI systems have this problem -- they can answer questions brilliantly, but they don't remember who you are, what you've told them, or what they've learned from past mistakes. This paper is like a comprehensive field guide written by 45 researchers that maps out all the different ways AI agents can build and use memory: where they store things (in text files, in the model itself, in hidden computational states), what they store (facts, skills, temporary notes), and how memory grows and changes over time. The goal is to give everyone building AI agents a shared vocabulary and a clear map of what's possible.

## TL;DR

This survey proposes a unified "Forms--Functions--Dynamics" (FFD) taxonomy for agent memory, distinguishing it from related concepts (LLM memory, RAG, context engineering). Memory *forms* span token-level (flat/planar/hierarchical), parametric (internal/external), and latent (generate/reuse/transform). Memory *functions* are categorized as factual (user + environment), experiential (case/strategy/skill-based), and working (single/multi-turn). Memory *dynamics* cover formation, evolution (consolidation, updating, forgetting), and retrieval. The survey also compiles benchmarks and frameworks and outlines eight frontier research directions.

---

## Problem & Motivation

Agent memory research has exploded in volume but fragmented in vocabulary and methodology. Papers claiming to study "agent memory" differ drastically in implementation, objectives, and assumptions. Traditional taxonomies (long-term/short-term) are too coarse to capture the diversity of modern systems. Simultaneously, loosely defined terminology (declarative, episodic, semantic, parametric) obscures conceptual clarity. Existing surveys predate rapid 2025 advances such as tool-distilling memory frameworks and memory-augmented test-time scaling. The paper addresses this by providing a rigorous definition of agent memory that distinguishes it from LLM memory (KV-cache/architecture concerns), RAG (static external knowledge for single-inference augmentation), and context engineering (optimizing the context window payload), then building a comprehensive taxonomy that unifies the field.

---

## Main Original Ideas

1. **Forms--Functions--Dynamics (FFD) Taxonomy** -- A three-dimensional lens that jointly answers *what carries memory* (form), *why memory is needed* (function), and *how memory operates over time* (dynamics). This replaces the inadequate long/short-term dichotomy.

2. **Token-level Memory with 1D/2D/3D Geometry** -- Token-level memory is classified by structural complexity: flat (1D sequences/bags), planar (2D graphs/trees with single-layer topology), and hierarchical (3D multi-layer structures with inter-layer links). Each level trades flexibility for richer relational reasoning.

3. **Functional Taxonomy: Factual / Experiential / Working** -- Moving beyond temporal labels, the survey proposes three functional roles. Factual memory holds declarative knowledge (user identity, environment state). Experiential memory encodes procedural/strategic knowledge to enable continual self-improvement. Working memory manages capacity-limited, task-scoped context.

4. **Experiential Memory Sub-taxonomy** -- Experiential memory is further split into case-based (raw trajectory replay), strategy-based (distilled reasoning patterns), skill-based (executable code/APIs), and hybrid, capturing the full spectrum from raw experience to generalizable capability.

5. **Memory Dynamics Decomposition** -- The lifecycle of memory is formally decomposed into: *formation* (semantic summarization, knowledge distillation, structured construction, latent representation, parametric internalization), *evolution* (consolidation, updating, forgetting), and *retrieval* (timing/intent, query construction, retrieval strategies, post-retrieval processing).

6. **Conceptual Delineation of Agent Memory** -- The paper rigorously formalizes agent memory as an evolving external cognitive state M_t with three operators (Formation, Evolution, Retrieval) -- distinct from KV-cache manipulation (LLM memory), static knowledge augmentation (RAG), and context-window optimization (context engineering).

---

## Key Findings

| Dimension | Key Insight |
|-----------|-------------|
| Token-level memory | Most prevalent form; flat memory (e.g., MemGPT, Memento) is fastest to update but lacks relational structure |
| Parametric memory | Zero-latency access but high update cost and catastrophic forgetting risk; external parametric (LoRA adapters) offers modular personalization |
| Latent memory | KV-cache reuse preserves fidelity but is resource-intensive; transform strategies (Scissorhands, SnapKV) reduce footprint |
| Factual memory | User factual memory (preferences, identity) critical for personalized agents; environment factual memory enables multi-agent coordination |
| Experiential memory | Strategy-based memory (Reflexion, AWM) most transferable; skill-based memory (Voyager, ToolLLM) most directly executable |
| Working memory | Multi-turn working memory (MemAgent, HiAgent, KARMA) requires temporal state consolidation across sessions |
| Memory formation | Structured construction (knowledge graphs via GraphRAG, Zep, A-MEM) supports richest retrieval but highest build cost |
| Memory evolution | Naive append-only strategies fail due to semantic redundancy and contradiction accumulation; active consolidation is necessary |
| Retrieval | Hybrid strategies (lexical + semantic + graph) outperform any single method; post-retrieval re-ranking and compression are essential |

- The boundary between RAG and agent memory is becoming blurred with "agentic RAG," but the distinction remains meaningful: agent memory is self-evolving and task-persistent, RAG is typically static and inference-scoped.
- Open-source ecosystem has matured rapidly: MemGPT, Mem0, Zep, LangMem are production-grade frameworks already in use.
- Benchmarks such as MemBench, LoCoMo, and WebChoreArena are emerging but evaluation protocols remain fragmented.

---

## Suggestions & Future Directions

1. **Automation-oriented memory design** -- Shift from manually engineered rules to autonomously managed, self-optimizing memory systems using hierarchical and adaptive architectures.
2. **Reinforcement learning meets agent memory** -- Use RL to internalize memory management abilities (component selection, architecture design) for genuinely continual learning.
3. **Multimodal memory** -- Develop omnimodal memory systems that integrate heterogeneous sensory inputs (visual, audio, text) for embodied agents.
4. **Shared memory in multi-agent systems** -- Evolve shared memory from passive repositories to actively managed, agent-aware, learning-driven collective representations for coordination and collective intelligence.
5. **Memory for world models** -- Move memory from data caching to active state simulation, constructing high-fidelity internal simulations of the world.
6. **Trustworthy memory** -- Address privacy (granular permissions, verifiable forgetting), explainability (auditable updates, causal tracing), and hallucination robustness.
7. **Memory generation vs. retrieval** -- Shift from retrieving stored information to actively synthesizing context-adaptive, integrated memory representations.
8. **Human-cognitive connections** -- Draw on biological memory processes (constructive memory, offline consolidation / sleep-like cycles) to build more efficient and robust learning mechanisms.

---

## Authors & Institutions

Yuyang Hu, Shichun Liu, Yanwei Yue, Guibin Zhang (core contributors and project organizer), plus 41 additional contributors and supervisors (Tao Gui, Shirui Pan, Yan Zhang, Philip Torr, Zhicheng Dou, Ji-Rong Wen, Xuanjing Huang, Yu-Gang Jiang, Shuicheng Yan).

**Affiliations:** National University of Singapore, Renmin University of China, Fudan University, Peking University, Nanyang Technological University, Tongji University, UC San Diego, HKUST (Guangzhou), Griffith University, Georgia Institute of Technology, OPPO, Oxford University.
