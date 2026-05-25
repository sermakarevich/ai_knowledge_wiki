# A Survey on the Memory Mechanism of Large Language Model based Agents

**Paper:** [A Survey on the Memory Mechanism of Large Language Model based Agents (Zhang et al., 2024)](https://arxiv.org/abs/2404.13501)

## Human Readable TL;DR

Think of an AI assistant that can only remember what you said in the last 5 minutes. A useful assistant needs to remember your preferences from last week, look up relevant information on demand, and learn from past mistakes. This paper is a map of all the research on how to give AI agents better memory -- cataloguing what types of memory exist, how they're stored and retrieved, and what challenges remain unsolved. It's like reviewing every possible approach to giving someone (or something) a better filing system for their experiences.

## TL;DR

This is the first comprehensive survey specifically focused on memory mechanisms for LLM-based agents, covering memory sources (inside-trial, cross-trial, external knowledge), forms (textual vs. parametric), and operations (writing, management, reading). The authors propose a unified taxonomy and evaluation framework, survey applications across six domains, and identify open research challenges including multi-agent memory coordination and parametric memory underexploration.

---

## Problem & Motivation

Standard LLMs process only what fits in their current context window -- they have no persistent memory across sessions, no ability to accumulate experience, and no mechanism to retrieve relevant past information. LLM-based agents need all three to be practically useful. Despite growing research on agent memory, no systematic survey existed before this work to unify the fragmented landscape of approaches, evaluation methods, and applications.

---

## Main Original Ideas

1. **Unified Memory Taxonomy** -- Classifies memory along three orthogonal axes: *source* (where information comes from), *form* (how it is stored), and *operations* (how it is written, managed, and read). This cross-cutting framework captures all existing approaches under one coherent structure.

2. **Three Memory Sources** -- Inside-trial (dialogue history, reasoning traces from the current session), cross-trial (knowledge accumulated across prior sessions enabling self-evolution), and external knowledge (databases, APIs, documents extending beyond training data).

3. **Two Memory Forms** -- Textual memory (explicit text storage with retrieval-augmented generation) vs. parametric memory (implicit storage via fine-tuning or knowledge editing). The survey highlights that parametric memory is severely underexplored relative to textual memory.

4. **Three Memory Operations** -- Writing (selective ingestion of new information), management (merging, reflecting, summarizing, and forgetting), and reading (retrieval of relevant stored information to inform the next action). The formal agent interaction equation captures how memory integrates into the action-generation loop.

5. **Dual Evaluation Framework** -- Direct evaluation (subjective: coherence/rationality; objective: correctness, reference accuracy, compute cost) and indirect evaluation through downstream task performance (conversation, multi-source QA, long-context tasks).

---

## Key Findings

| Memory Form | Prevalence | Key Challenge |
|---|---|---|
| Textual (full history) | High | Context window overflow |
| Textual (retrieved) | High | Retrieval quality/latency |
| Textual (summarized) | Medium | Information loss in compression |
| Parametric (fine-tuning) | Low | Catastrophic forgetting |
| Parametric (knowledge editing) | Low | Scalability, precision |

- The majority of agent memory research relies on textual memory + RAG-style retrieval; parametric approaches remain a niche area.
- Cross-trial memory (multi-session accumulation) is what enables agent self-evolution -- agents that improve over time -- yet it is more complex to evaluate than single-session memory.
- Multi-agent systems face unsolved coordination problems: how agents share memory, avoid conflicts, and maintain consistency across distributed memory stores.
- Privacy and security are identified as critical gaps: persistent memory of user data creates attack surfaces and compliance risks with no mature solutions.

---

## Suggestions & Future Directions

1. **Advanced parametric memory** -- Develop efficient, targeted methods to update model weights from agent experiences without catastrophic forgetting.
2. **Multi-agent memory coordination** -- Design frameworks for shared memory, conflict resolution, and synchronization across agent collectives.
3. **Memory-based lifelong learning** -- Build agents that continuously improve across an open-ended stream of experiences, not just within a fixed task horizon.
4. **Human-aligned memory architectures** -- Draw more explicitly from cognitive science models (episodic, semantic, procedural memory) to design more robust agent memory systems.
5. **Privacy-preserving memory** -- Investigate differential privacy, federated memory, and access control mechanisms for agents storing sensitive user data.
6. **Standardized benchmarks** -- The field lacks unified benchmarks for comparing memory mechanisms; the authors call for community-wide evaluation standards.

---

## Authors & Institutions

Zeyu Zhang, Xiaohe Bo, Chen Ma, Rui Li, Xu Chen, Quanyu Dai, Jieming Zhu, Zhenhua Dong, Ji-Rong Wen -- Renmin University of China, Huawei Noah's Ark Lab
