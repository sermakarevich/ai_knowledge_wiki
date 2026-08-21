---
type: Paper
title: "LightRAG: Simple and Fast Retrieval-Augmented Generation"
description: An LLM-built knowledge graph with dual-level (specific + thematic) retrieval and cheap incremental updates, beating chunk-based RAG baselines and out-costing GraphRAG on update overhead.
generated: {by: claude/sonnet, at: 2026-08-20T18:20:00Z}
sources:
  - id: original
    resource: https://arxiv.org/abs/2410.05779
  - id: local-copy
    resource: source/2410.05779.pdf
tags: [rag, graph-rag, knowledge-graph, retrieval, llm]
---

# LightRAG: Simple and Fast Retrieval-Augmented Generation

LightRAG (Guo et al., 2024, EMNLP 2025) replaces flat, chunk-based retrieval-augmented generation with an LLM-constructed knowledge graph and a dual-level (specific-entity / broad-theme) retrieval scheme, combined with an incremental update mechanism that merges new documents into the existing graph instead of rebuilding it. It was worth ingesting because it is one of the clearest, cheapest graph-RAG designs benchmarked directly against GraphRAG (Edge et al., 2024) — same evaluation protocol, orders-of-magnitude cost difference, and an honest reporting of the one dataset where it loses.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~5-10 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

_New to RAG or knowledge graphs? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

## Read This Folder

- [[summary|Summary]] — rung 1: the whole paper, shallow
- [[digest|Digest]] — rung 2: the whole paper at medium depth; the file to re-read on review
- [[explainer|Plain-Language Explainer]] — no-jargon explanation, applications, conclusions
- [[critical_thinking|Critical Analysis]] — claims vs. evidence, applicability, what it changes, verdict
- [[questions|Retrieval Practice]] — self-test questions; **answer these from memory before re-reading anything**
- [[connections|Connections]] — related entries in this knowledge base

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-introduction-and-motivation\|Introduction and Motivation]] | Why flat chunk-based RAG fails on multi-hop questions, and LightRAG's proposed graph-based fix |
| [[wiki/02-lightrag-architecture\|The LightRAG Architecture]] | Graph-based text indexing, dual-level retrieval, answer generation, and complexity analysis |
| [[wiki/03-evaluation-setup-and-main-results\|Evaluation Setup and Main Results (RQ1)]] | UltraDomain benchmark datasets, baselines, and head-to-head win rates vs. NaiveRAG/RQ-RAG/HyDE/GraphRAG |
| [[wiki/04-ablation-case-study-cost-analysis\|Ablation Studies, Case Study, and Cost/Adaptability Analysis (RQ2-RQ4)]] | What each retrieval level contributes, a worked case study, and token/API-call cost vs. GraphRAG |
| [[wiki/05-related-work-conclusion-appendix\|Related Work, Conclusion, and Appendix]] | Positioning vs. prior RAG/GraphRAG/LLM-for-graphs work, conclusion, dataset stats, and all four prompt templates |

## Original Source

- [source/2410.05779.pdf](source/2410.05779.pdf) — PDF, retrieved 2026-08-20
