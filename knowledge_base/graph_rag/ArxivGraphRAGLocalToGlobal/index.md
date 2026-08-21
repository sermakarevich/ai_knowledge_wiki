---
type: Paper
title: From Local to Global: A Graph RAG Approach to Query-Focused Summarization
description: Microsoft Research's GraphRAG paper — builds an LLM-derived knowledge graph, partitions it into Leiden communities, summarizes them bottom-up, and answers global sensemaking queries by map-reduce over community summaries, beating vector RAG on comprehensiveness and diversity.
generated: { by: claude/sonnet, at: 2026-08-20T18:50:00Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2404.16130
  - id: local-copy
    resource: source/graphrag_2404.16130.pdf
tags: [graphrag, rag, knowledge-graphs, query-focused-summarization, sensemaking]
---

# From Local to Global: A Graph RAG Approach to Query-Focused Summarization

Microsoft Research's paper (Edge et al., 2024) that coined "GraphRAG." It identifies a class of queries — global sensemaking questions like "what are the main themes across this dataset?" — that conventional vector-similarity RAG structurally cannot answer, because it only ever retrieves a handful of chunks. GraphRAG's answer is to have an LLM build a knowledge graph from the corpus, cluster it into a hierarchy of topical communities, pre-summarize each community, and answer global queries with a map-reduce pass over those summaries. Worth ingesting as the canonical reference architecture every later GraphRAG paper and framework (LightRAG, HippoRAG, etc.) positions itself against.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~5-10 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

_New to the field? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

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
| [[wiki/01-introduction-and-background\|Introduction and Background]] | The sensemaking problem, GraphRAG's pipeline overview, Figure 1, and related work on RAG / knowledge-graph-based RAG / RAG evaluation |
| [[wiki/02-graphrag-methodology\|GraphRAG Methodology]] | The six-step indexing pipeline (chunking → entity/relationship extraction → graph → Leiden communities → community summaries → map-reduce query answering), question-generation method, evaluation criteria |
| [[wiki/03-experimental-setup-and-results\|Experimental Setup and Results]] | Datasets, six experimental conditions (C0-C3, TS, SS), win-rate results (Figure 2) and claim-based validation |
| [[wiki/04-discussion-and-conclusion\|Discussion and Conclusion]] | Limitations (two corpora only, no fabrication-rate measurement), future work, broader-impact risks, conclusion |
| [[wiki/05-appendix-prompts-and-additional-experiments\|Appendix: Prompts and Additional Experiments]] | Exact prompts (extraction, community summary, evaluation), chunk-size trade-off experiment (Figure 3), community-detection example (Figure 4), context-window sizing, full statistics |

## Original Source

- [source/graphrag_2404.16130.pdf](source/graphrag_2404.16130.pdf) — arXiv PDF, retrieved 2026-08-20
