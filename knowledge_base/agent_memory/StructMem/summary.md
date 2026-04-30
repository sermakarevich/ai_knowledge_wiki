# StructMem: Structured Memory for Long-Horizon Behavior in LLMs

**Paper:** [StructMem: Structured Memory for Long-Horizon Behavior in LLMs (Xu et al., 2026)](https://arxiv.org/abs/2604.21748)

## Human Readable TL;DR

Imagine a personal assistant who remembers not just what you said in past meetings, but also *why* things happened and *how* events connect over time -- like a detective's corkboard with threads linking clues. StructMem gives AI chatbots this kind of memory. Instead of storing a flat list of notes or building a complex web of connections that's slow and error-prone, it groups memories into "events" with their full context, then periodically links related events across time. The result is a smarter, faster memory that helps AI assistants answer "what did we agree about last month because of what happened earlier?" without needing a supercomputer to do it.

## TL;DR

StructMem is a hierarchical memory framework for LLM agents that organizes conversational history into two levels: (1) event-level binding via dual-perspective extraction of factual and relational entries with temporal anchoring, and (2) periodic cross-event consolidation that semantically clusters related events across time windows. Evaluated on the LoCoMo benchmark, it achieves 76.82% overall -- the best among all compared systems -- with 81.62% on temporal reasoning, while using ~18x fewer tokens and ~50x fewer API calls than the best-performing graph-based baseline (Mem0g).

---

## Problem & Motivation

LLM agents in long-term dialogues need memory that supports temporal reasoning and multi-hop question answering -- not just simple fact lookup. Existing approaches hit a fundamental trade-off:

- **Flat memory** (vector databases, summaries) is fast but loses relational and temporal context; retrieval returns isolated facts without causal scaffolding.
- **Graph memory** (knowledge graphs) captures structure but requires cascading LLM calls for entity/relation extraction, is slow, and accumulates hallucination errors from noisy triplet extraction.

StructMem targets this gap: structured reasoning at graph-like quality, with flat-memory-like efficiency.

---

## Main Original Ideas

1. **Temporally Grounded Relational Event as Memory Unit** -- Rather than isolated facts or entity-relation triplets, the fundamental unit is an "event": all factual and relational entries from a single utterance, anchored to a precise timestamp. This preserves context without rigid schemas or entity resolution.

2. **Dual-Perspective Extraction** -- Each utterance is processed into two complementary entry types: *factual entries* (what happened, plans, opinions) and *relational entries* (interpersonal dynamics, causal influences, emotional responses). Both are stored as natural language, not triplets.

3. **Temporal Anchoring** -- Every extracted entry is coupled to its originating timestamp, enabling exact event reconstruction at retrieval time by pulling all entries sharing the same timestamp.

4. **Periodic Cross-Event Consolidation** -- When a buffer of unconsolidated events exceeds a time threshold, StructMem generates an aggregated query embedding, retrieves top-K semantically similar historical entries, reconstructs their full event contexts, then synthesizes the cluster into higher-level relational hypotheses using a constrained consolidation prompt (requiring timestamp citations and concrete dependency focus).

5. **Constrained Synthesis for Hallucination Control** -- The consolidation prompt enforces timestamp citations and forbids ungrounded inference. This constraint reduces hallucination rates from 7.45% (unconstrained) to 0.61% in cross-event synthesis.

---

## Key Findings

### Overall Results on LoCoMo Benchmark

| System | Type | Overall | Single-Hop | Multi-Hop | Temporal | Open-Domain |
|--------|------|---------|-----------|-----------|----------|-------------|
| **StructMem** | **Structural** | **76.82** | -- | **68.77** | **81.62** | -- |
| Memobase | Structural | ~74 | -- | -- | ~76 | -- |
| Zep | Structural | ~73 | -- | -- | ~78 | -- |
| Mem0g | Structural (graph) | ~72 | -- | -- | ~75 | -- |
| A-Mem | Flat | ~70 | -- | -- | ~72 | -- |
| LangMem | Flat | ~68 | -- | -- | ~70 | -- |

### Efficiency vs. Mem0g (graph baseline)

| Metric | StructMem | Mem0g | Reduction |
|--------|-----------|-------|-----------|
| Build tokens | 1.937M | 35.825M | **~18x fewer** |
| API calls | 1,056 | 53,514 | **~51x fewer** |
| Runtime (s) | 22,854 | 115,670 | **~5x faster** |

### Ablation Insights

- Event-level structuring alone improves temporal and single-session tasks over flat memory.
- Cross-event consolidation (K > 0 semantic seeds) provides the major multi-hop and causal reasoning gains; K=0 collapses to flat retrieval plateau.
- Increasing flat retrieval beyond ~60 entries yields no further gains -- bottleneck is knowledge synthesis, not data coverage.
- Hallucination rate of dual-perspective extraction: 2.36% mean across conversations.
- Constrained vs. unconstrained consolidation hallucination: 0.61% vs. 7.45%.

---

## Suggestions & Future Directions

1. **Automated prompt optimization** for dual-perspective extraction to improve robustness across diverse dialogue contexts and domains beyond the LoCoMo benchmark.
2. **Conflict resolution and memory update strategies** to handle evolving user facts, contradictions, and preference changes over extended periods.
3. **Memory decay mechanisms** to gracefully downweight or remove stale entries in very long-term interactions.
4. **Broader evaluation** across more datasets and backbone LLMs to validate generalizability beyond gpt-4o-mini.
5. **Real-time deployment investigation** to assess practical performance in streaming, latency-sensitive applications.

---

## Authors & Institutions

Buqiang Xu (Zhejiang University), Yijun Chen (Zhejiang University), Jizhan Fang (Zhejiang University), Ruobin Zhong (Zhejiang University), Yunzhi Yao (Zhejiang University), Yuqi Zhu (Zhejiang University / Zhejiang University-Ant Group Joint Lab of Knowledge Graph), Lun Du (Ant Group / Zhejiang University-Ant Group Joint Lab of Knowledge Graph), Shumin Deng (Zhejiang University)
