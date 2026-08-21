---
type: Paper
title: Graph Retrieval-Augmented Generation: A Survey
description: A systematic survey formalizing GraphRAG as a three-stage pipeline (indexing, retrieval, generation) that grounds LLM answers in graph-structured relational knowledge instead of raw text.
generated: { by: claude/sonnet-5, at: 2026-08-20T19:00:00Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2408.08921
  - id: local-copy
    resource: source/2408.08921.pdf
tags: [graphrag, retrieval-augmented-generation, knowledge-graphs, graph-neural-networks, llm-survey]
---

# Graph Retrieval-Augmented Generation: A Survey

This paper is the first systematic survey of GraphRAG — retrieval-augmented generation that pulls structured graph elements (nodes, triples, paths, subgraphs) from a graph database instead of raw text chunks, so relational knowledge between entities is preserved rather than lost in flat text retrieval. Its central contribution is a formal three-stage framework — Graph-Based Indexing, Graph-Guided Retrieval, and Graph-Enhanced Generation — under which it categorizes methods, training strategies, downstream tasks, benchmarks, and industrial systems. It's worth reading because it gives a shared vocabulary and taxonomy for a fast-moving area, useful for anyone deciding how to add a knowledge graph to an LLM pipeline.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every chapter's headline and key points.
3. **Wiki pages below** (~N min each) — one chapter, deep. Each opens with its headline and key points, so you can stop early.

_New to the field? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

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
| [[wiki/01-introduction-and-related-work|Introduction & Related Work]] | Why RAG falls short on relational knowledge, and how GraphRAG differs from RAG, LLMs-on-graphs, and KBQA |
| [[wiki/02-preliminaries-and-framework|Preliminaries & Framework]] | Text-attributed graphs, GNNs, LMs, and the formal G-Indexing/G-Retrieval/G-Generation definition |
| [[wiki/03-graph-based-indexing|Graph-Based Indexing]] | Open vs. self-constructed graph data, and graph/text/vector/hybrid indexing schemes |
| [[wiki/04-graph-guided-retrieval|Graph-Guided Retrieval]] | Retriever types, retrieval paradigms, granularity, and query/knowledge enhancement |
| [[wiki/05-graph-enhanced-generation|Graph-Enhanced Generation]] | Generator choice (GNN/LM/hybrid), graph-to-text/embedding formats, and pre/mid/post-generation enhancement |
| [[wiki/06-training-applications-evaluation|Training, Applications & Evaluation]] | Training-free vs. training-based strategies, downstream tasks, benchmarks, and industrial GraphRAG systems |
| [[wiki/07-future-directions-and-conclusion|Future Directions & Conclusion]] | Open challenges (dynamic graphs, multi-modality, scale, compression, benchmarks) and closing summary |

## Original Source

- [source/2408.08921.pdf](source/2408.08921.pdf) — PDF, retrieved 2026-08-20
