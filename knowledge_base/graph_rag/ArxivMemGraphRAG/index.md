---
type: Paper
title: MemGraphRAG: Memory-based Multi-Agent System for Graph Retrieval-Augmented Generation
description: A memory-based multi-agent framework that fixes GraphRAG's isolated-chunk extraction problem with a three-layer Global Memory (Ontology/Fact/Passage) and dedicated conflict-detection/resolution agents, achieving the best generation accuracy, densest/most-clustered index graphs, and lowest retrieval latency among compared GraphRAG baselines.
generated: { by: claude/claude-sonnet-5, at: 2026-08-21T09:37:00Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2606.00610
  - id: local-copy
    resource: source/paper.pdf
tags: [graph-rag, knowledge-graph, multi-agent, memory, retrieval-augmented-generation]
---

# MemGraphRAG: Memory-based Multi-Agent System for Graph Retrieval-Augmented Generation

Naive GraphRAG builds its knowledge graph from isolated, per-chunk extractions with no global view of the corpus, producing graphs that are thematically noisy, logically inconsistent, and structurally fragmented — sometimes performing worse than vanilla RAG. MemGraphRAG (Wu et al., 2026, KDD 2026) fixes this by giving a multi-agent extraction pipeline a persistent, shared **Three-Layer Global Memory** (Ontology / Fact / Passage) that lets agents filter noise, resolve conflicts against evidence, and bridge fragmented subgraphs as the graph is built — then reuses that same memory to seed a Personalized-PageRank retrieval pass at query time. It was worth ingesting as a concrete, mechanistic answer to "why does GraphRAG sometimes underperform plain RAG" and a design worth comparing against other memory-centric and agentic GraphRAG systems already in this KB.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~10-15 min each) — one topic, deep. Each opens with its headline and key points, so you can stop early.

_New to GraphRAG? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

## Read This Folder

- [[summary|Summary]] — rung 1: the whole source, shallow
- [[digest|Digest]] — rung 2: the whole source at medium depth; the file to re-read on review
- [[explainer|Plain-Language Explainer]] — no-jargon explanation, applications, conclusions
- [[critical_thinking|Critical Analysis]] — claims vs. evidence, applicability, what it changes
- [[questions|Retrieval Practice]] — self-test questions; **answer these from memory before re-reading anything**
- [[connections|Connections]] — related entries in this knowledge base

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-motivation-and-problem\|Motivation, Problem Statement, and Preliminary Study]] | Why naive GraphRAG underperforms vanilla RAG: thematic irrelevance, logical inconsistency, structural fragmentation, and the preliminary study diagnosing these failure modes |
| [[wiki/02-memgraphrag-framework\|The MemGraphRAG Framework and Experimental Results]] | The Three-Layer Global Memory, Multi-Agent Group (Extract/Detect/Resolve), memory-guided PPR retrieval, and the main experiments (generation accuracy, retrieval quality, adaptability, ablations) |
| [[wiki/03-conclusion-and-additional-experiments\|Conclusion and Additional Experiments]] | The paper's conclusion and stated multimodal limitation, plus backbone-robustness, graph-topology, and qualitative case-study experiments from Appendix A |
| [[wiki/04-related-work-and-appendix\|Related Work and Appendix Details]] | Positioning against relation-extraction and clustering-based GraphRAG, the conflict-detection/resolution agent prompts, retrieval-initialization math, and full dataset/baseline/implementation details |

## Original Source

- [source/paper.pdf](source/paper.pdf) — arXiv PDF (2606.00610), retrieved 2026-08-21
