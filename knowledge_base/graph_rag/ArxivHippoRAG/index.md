---
type: Paper
title: HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models
description: An LLM-built knowledge graph indexed and retrieved via Personalized PageRank, modeled on the hippocampal memory indexing theory, enabling single-step multi-hop retrieval that is far cheaper and faster than iterative RAG.
generated: { by: claude/sonnet, at: 2026-08-20T18:16:00Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2405.14831
  - id: local-copy
    resource: source/paper.pdf
tags: [rag, knowledge-graph, multi-hop-qa, long-term-memory, graph-rag]
---

# HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models

HippoRAG (NeurIPS 2024) gives LLMs a retrieval system modeled directly on how the human hippocampus indexes and links memories stored in the neocortex. It replaces isolated-passage retrieval with a schemaless knowledge graph plus Personalized PageRank, letting a single retrieval pass answer multi-hop questions that would otherwise need several rounds of iterative retrieval. It was worth ingesting as a foundational graph-RAG paper: cheap, fast, and unusually explicit about *why* graph-based indexing helps (path-finding vs. path-following questions) rather than just reporting benchmark wins.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every chapter's headline and key points.
3. **Wiki pages below** (~5-10 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

_New to the field? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

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
| [[wiki/01-introduction\|Abstract & Introduction]] | Problem framing, hippocampal indexing theory, HippoRAG at a high level, headline results |
| [[wiki/02-methodology\|Detailed Methodology]] | Offline indexing (OpenIE + synonymy edges), online retrieval (query NER + Personalized PageRank), node specificity |
| [[wiki/03-experiments-results\|Experimental Setup & Retrieval/QA Results]] | Datasets, baselines, single-step and multi-step retrieval results, QA results |
| [[wiki/04-discussions\|Discussions: Ablations, Integration & Efficiency]] | OpenIE and PPR ablations, knowledge-integration advantage, efficiency comparison to IRCoT |
| [[wiki/05-related-work-conclusion\|Related Work & Conclusions]] | Parametric memory, long-context memory, RAG-as-memory, multi-hop QA/graph literature, conclusions & limitations |
| [[wiki/06-appendix-pipeline-errors\|Appendix: Pipeline Walkthrough, Error Analysis & Prompts]] | Full worked pipeline example, path-finding case study, error analysis, implementation details, LLM prompts |

## Original Source

- [source/paper.pdf](source/paper.pdf) — PDF, retrieved 2026-08-20
