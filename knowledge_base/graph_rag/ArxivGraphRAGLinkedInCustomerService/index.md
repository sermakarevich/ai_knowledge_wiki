---
type: Paper
title: Retrieval-Augmented Generation with Knowledge Graphs for Customer Service Question Answering
description: LinkedIn production case study fusing RAG with a per-ticket knowledge graph (intra-ticket trees plus explicit/implicit inter-ticket edges) to fix structure loss in chunk-based retrieval, gaining 77.6% MRR and 0.32 BLEU offline and cutting median support-ticket resolution time 28.6% in a live A/B.
generated: { by: claude/sonnet, at: 2026-08-20T20:00:00Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2404.17723
  - id: local-copy
    resource: source/2404.17723.pdf
tags: [graph-rag, knowledge-graph, customer-service, retrieval, rag]
---

# Retrieval-Augmented Generation with Knowledge Graphs for Customer Service Question Answering

A 5-page SIGIR '24 short paper from LinkedIn describing a production system that replaces chunk-based RAG over support tickets with a knowledge-graph-informed pipeline: each ticket becomes a typed tree, tickets are linked by clone/similarity edges, and queries are resolved by entity/intent parsing, embedding-ranked ticket retrieval, and LLM-generated Cypher queries against the graph. It was worth ingesting for the concrete production numbers — a real A/B test with a real business-metric win (resolution time), not just an offline benchmark.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~5-10 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

_New to GraphRAG or knowledge graphs? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

## Read This Folder

- [[summary|Summary]] — rung 1: the whole source, shallow
- [[digest|Digest]] — rung 2: the whole source at medium depth; the file to re-read on review
- [[explainer|Plain-Language Explainer]] — no-jargon explanation, applications, conclusions
- [[critical_thinking|Critical Analysis]] — claims vs. evidence, applicability, what it changes, verdict
- [[questions|Retrieval Practice]] — self-test questions; **answer these from memory before re-reading anything**
- [[connections|Connections]] — related entries in this knowledge base

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-introduction-and-related-work\|Introduction and Related Work]] | Motivation, the two structural weaknesses of chunk-based RAG, and the QA-with-KG literature (retrieval/template/semantic-parsing families, LLM+KG integration work) |
| [[wiki/02-knowledge-graph-method\|Knowledge Graph Method]] | The two-level KG (intra-ticket tree + inter-ticket edges), hybrid rule-based/LLM construction, embedding generation, query entity/intent parsing, sub-graph retrieval scoring, Cypher translation, and answer generation with fallback (Figure 1) |
| [[wiki/03-experiments-and-production\|Experiments and Production Results]] | Golden-dataset retrieval and generation metrics (Tables 1-2), the live LinkedIn A/B resolution-time results (Table 3), and the conclusions/future-work directions |

## Original Source

- [source/2404.17723.pdf](source/2404.17723.pdf) — arXiv:2404.17723v2, "Retrieval-Augmented Generation with Knowledge Graphs for Customer Service Question Answering" by Zhentao Xu, Mark Jerome Cruz, Matthew Guevara, Tie Wang, Manasi Deshpande, Xiaofeng Wang, Zheng Li (LinkedIn), SIGIR '24, retrieved 2026-08-20.
