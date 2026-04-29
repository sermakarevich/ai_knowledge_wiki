# GAAMA: Graph Augmented Associative Memory for Agents

**Paper:** [GAAMA: Graph Augmented Associative Memory for Agents (Paul, Sharma & Sareen, 2026)](https://arxiv.org/abs/2603.27910)

## Human Readable TL;DR

Imagine an AI assistant that talks to you every day but forgets everything between conversations -- like a coworker with amnesia. GAAMA gives the assistant a structured "memory scrapbook" where facts, themes, and insights are connected like a web, so it can trace links between things you mentioned weeks apart. Instead of just searching for similar-sounding notes, it walks along these connections to recall related information -- much like how your own memory works when one thought triggers another. The result is an assistant that remembers your preferences, past issues, and routines across many conversations.

## TL;DR

GAAMA introduces a concept-mediated hierarchical knowledge graph for agent long-term memory, using four node types (episode, fact, reflection, concept) and five edge types to preserve structural relationships across multi-session conversations. A hybrid retrieval mechanism blends edge-type-aware Personalized PageRank with semantic similarity, achieving 78.9% mean reward on the LoCoMo-10 benchmark -- outperforming tuned RAG (75.0%), HippoRAG (69.9%), and other baselines, with especially strong gains on temporal (+12.9 pp) and multi-hop (+4.7 pp) reasoning questions.

---

## Problem & Motivation

AI agents that interact with users across multiple sessions need persistent long-term memory for coherent and personalized behavior. Current approaches fall short in several ways:

- **Flat RAG** retrieves text chunks by embedding similarity but loses structural relationships between entities, events, and facts spread across conversations, making multi-hop reasoning difficult.
- **Memory compression and vector retrieval** treat memories as isolated units, failing to capture the associative links connecting information over time.
- **Entity-centric knowledge graphs** (e.g., HippoRAG) suffer from the "mega-hub problem" -- frequently mentioned entities like "user" accumulate hundreds of edges, diffusing retrieval precision and producing uniform relevance scores.
- **Full-context approaches** that feed entire conversation histories into the LLM context window are computationally expensive and do not scale.

Without effective long-term memory, agents lose context between sessions and provide generic, repetitive responses.

---

## Main Original Ideas

1. **Concept-mediated hierarchical knowledge graph** -- Four node types (episode, fact, reflection, concept) connected by five typed edges. Concept nodes replace entity nodes as cross-cutting connectors, producing ~30x fewer edges than entity-centric designs and eliminating the mega-hub problem while enabling thematic traversal across sessions.

2. **Three-step construction pipeline** -- Separates structural operations from LLM calls: (1) verbatim episode preservation with temporal ordering (no LLM), (2) LLM-based extraction of atomic facts and topic-level concepts, (3) LLM-based synthesis of higher-order reflections from multiple facts. This supports incremental, continuous memory evolution.

3. **Hybrid retrieval with edge-type-aware PPR and hub dampening** -- Combines Personalized PageRank (with per-edge-type transition weights and hub dampening for high-degree nodes) with semantic similarity via additive scoring. A mild PPR weight (0.1) augments embedding-based retrieval without introducing structural noise.

4. **Per-type budget caps for memory packing** -- Retrieved nodes are capped per type (facts, reflections, episodes) before assembly, preventing episodes from dominating the context and ensuring diversity in retrieved memory.

---

## Key Findings

### Main Results on LoCoMo-10 Benchmark

| System       | Overall | Multi-hop (Cat1) | Temporal (Cat2) | Open Domain (Cat3) | Single Hop (Cat4) |
|-------------|---------|-------------------|-----------------|---------------------|--------------------|
| **GAAMA**   | **78.9%** | **72.2%**       | **71.9%**       | **49.3%**           | **87.2%**          |
| RAG (tuned) | 75.0%  | 67.5%             | 59.0%           | 44.6%               | 87.1%              |
| HippoRAG   | 69.9%  | --                | --              | --                  | --                 |
| Nemori      | 52.1%  | --                | --              | --                  | --                 |
| A-Mem       | 47.2%  | --                | --              | --                  | --                 |

- Largest gains over RAG baseline on **temporal reasoning** (+12.9 pp) and **multi-hop** (+4.7 pp) questions
- Single-hop performance nearly identical to RAG, confirming embedding retrieval suffices for direct factual recall
- Mild PPR (w=0.1) consistently outperformed both pure semantic retrieval (+1.0 pp overall) and strong PPR (w=1.0), which introduced noise
- PPR improved 8 out of 10 conversations; open-domain questions showed high variance -- PPR can dramatically help or hurt depending on concept quality
- Removing per-type budget caps degraded multi-hop performance by 3--7% as episodes overwhelmed facts and reflections

### Error Analysis

- Most retrieval failures traced to knowledge graph construction issues: generic concepts (e.g., `personal_growth`), near-duplicate concepts (e.g., `supportive_relationships` vs. `supportive_relationship`), and semantically overlapping concepts that fragment PPR mass

---

## Suggestions & Future Directions

1. **Concept canonicalization** -- Merging near-duplicate and semantically overlapping concept nodes to strengthen PPR paths and reduce graph fragmentation.

2. **Adaptive PPR gating** -- A learned model to predict per-query whether graph traversal is beneficial, especially for open-domain questions where PPR shows high variance.

3. **Edge weight learning** -- Optimizing edge type weights end-to-end via backpropagation through the PPR computation to improve retrieval quality beyond hand-tuned weights.

4. **Scaling evaluation** -- Testing on larger and more diverse multi-session benchmarks beyond LoCoMo-10's 10 conversations and 1,540 questions.

---

## Authors & Institutions

Swarna Kamal Paul (Nagarro), Shubhendu Sharma (Nagarro), Nitin Sareen (Nagarro)
