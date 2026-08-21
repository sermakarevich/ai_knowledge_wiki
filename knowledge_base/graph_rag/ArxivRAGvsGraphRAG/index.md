---
type: Paper
title: RAG vs. GraphRAG — A Systematic Evaluation and Key Insights
description: A controlled benchmark of standard RAG against four GraphRAG families on QA and query-based summarization, finding the two paradigms complementary rather than competing, with hybrid Selection/Integration strategies outperforming either alone.
generated: { by: claude/claude-sonnet-5, at: 2026-08-20T20:00:00Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2502.11371
  - id: local-copy
    resource: source/2502.11371.pdf
tags: [rag, graphrag, retrieval, evaluation, benchmark]
---

# RAG vs. GraphRAG — A Systematic Evaluation and Key Insights

This paper (Han et al., 2025) runs the first controlled, unified benchmark of standard RAG against four representative GraphRAG families — KG-based, community-based, text-centric graph-guided, and hierarchical summary-based — on question answering and query-based summarization. Its central claim: RAG and GraphRAG are not competitors with one winner but complementary tools with different strengths, different costs, and — for LLM-as-a-Judge scoring — an evaluation protocol that can itself flip the conclusion.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~10-15 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

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
| [[wiki/01-introduction-and-evaluation-framework\|Introduction and Evaluation Framework]] | Why unified benchmarking is needed; the four GraphRAG families; the fair-comparison protocol (chunking, embeddings, reranking, generation backbones) |
| [[wiki/02-question-answering-results\|Question Answering Results]] | RAG vs. GraphRAG on NQ/HotPotQA/MultiHop-RAG/NovelQA; reranking & iterative retrieval; Selection/Integration hybrids; cost/latency/storage |
| [[wiki/03-summarization-and-conclusion\|Summarization and Conclusion]] | Reference-based summarization results (ROUGE-2/BERTScore); LLM-as-a-Judge position bias; paper's overall conclusion |
| [[wiki/04-appendix-datasets-and-case-studies\|Appendix: Datasets and Case Studies]] | Dataset statistics, extended result tables, Hotpot case studies, retrieval-accuracy analysis, prompt templates |

## Original Source

- [source/2502.11371.pdf](source/2502.11371.pdf) — arXiv PDF, retrieved 2026-08-20
