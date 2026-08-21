---
type: Paper
title: "GraphRAG-Bench: Challenging Domain-Specific Reasoning Benchmark for GraphRAG"
description: A 1,018-question, 20-textbook, college-level benchmark that scores GraphRAG methods across graph construction, retrieval, generation, and gold-rationale reasoning, finding that GraphRAG substantially improves reasoning but its accuracy gains are inconsistent across question types and topics.
generated: { by: claude/sonnet, at: 2026-08-20T18:04:08Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2506.02404
  - id: local-copy
    resource: source/paper.pdf
tags: [graphrag, rag, benchmark, multi-hop-reasoning, knowledge-graph, llm-evaluation]
---

# GraphRAG-Bench: Challenging Domain-Specific Reasoning Benchmark for GraphRAG

GraphRAG-Bench is the first benchmark built specifically to test whether graph-structured retrieval-augmented generation (GraphRAG) actually improves an LLM's *reasoning*, not just its factual recall. It replaces prior benchmarks' shallow, single-hop, training-data-adjacent questions with 1,018 college-level questions drawn from 20 computer-science textbooks, each carrying an expert-written rationale, and scores nine GraphRAG methods end-to-end — graph construction, retrieval, generation, and reasoning fidelity — against a shared GPT-4o-mini backend. The central finding is that GraphRAG helps reasoning broadly but helps *accuracy* unevenly: strong on tree/PageRank-style methods (RAPTOR, HippoRAG), harmful on two structure-heavy methods (DALK, G-Retriever), and domain-dependent (hurts Mathematics, barely moves Ethics).

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every chapter's headline and key points.
3. **Wiki pages below** (~10-15 min each) — one chapter, deep. Each opens with its headline and key points, so you can stop early.

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
| [[wiki/01-introduction-and-motivation\|Introduction & Motivation]] | Why flat RAG can't do multi-hop/global reasoning, the three limitations of prior GraphRAG benchmarks, and GraphRAG-Bench's answer: 1,018 questions, 5 types, 16 disciplines. |
| [[wiki/02-benchmark-design\|Benchmark Design & Construction]] | The 5 question types, the 4-stage textbook-to-tree extraction pipeline, and why every question ships with an expert-crafted rationale and two-level topic label. |
| [[wiki/03-evaluation-protocol-and-core-results\|Evaluation Protocol, Metrics & Core Results]] | The 4 metric families (construction, retrieval, generation, reasoning) and Tables 2-5: full numbers for all 9 methods plus RAG baselines. |
| [[wiki/04-topic-analysis-observations-and-conclusion\|Topic Analysis, Observations, Case Study & Conclusion]] | Where GraphRAG helps or hurts by topic and question type, a worked multi-hop case study, and the paper's conclusion. |

## Original Source

- [source/paper.pdf](source/paper.pdf) — arXiv PDF, retrieved 2026-08-20
- [arXiv:2506.02404](https://arxiv.org/abs/2506.02404) — canonical source
