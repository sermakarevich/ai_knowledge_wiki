---
type: Paper
title: Why Neighborhoods Matter — Traversal Context and Provenance in Agentic GraphRAG
description: A controlled ablation study showing that final citations in agentic GraphRAG are necessary but not sufficient — visited-but-uncited entities and graph structure also shape the answer.
generated: { by: claude/sonnet, at: 2026-08-21T06:15:00Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2605.15109
  - id: local-copy
    resource: source/full.txt
  - id: provenance-pin
    resource: source/source.md
tags: [graphrag, agentic-rag, provenance, citation-faithfulness, knowledge-graphs]
---

# Why Neighborhoods Matter — Traversal Context and Provenance in Agentic GraphRAG

This short paper (Terrenzi, von Zastrow, Ayvaz, 2026) asks whether the entities an agentic GraphRAG system cites at the end of its answer actually account for everything that shaped that answer. Using a 30-question multi-hop QA benchmark and a series of graph-ablation experiments (removing cited entities, removing random entities, isolating only cited entities, masking visited-but-uncited entities), the authors show that cited evidence is *necessary* but not *sufficient*: the graph structure and the entities an agent visits but never cites still measurably affect accuracy. It was worth ingesting because it directly challenges the common assumption — used across most GraphRAG citation/provenance designs — that "cited sources = full evidence basis."

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~5 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

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
| [[wiki/01-introduction-and-motivation\|Introduction and Motivation]] | Hallucination/RAG/GraphRAG background, the gap in prior citation-faithfulness work, and the paper's hypothesis and contributions |
| [[wiki/02-experimental-design-and-studies\|Experimental Design and Studies]] | The 30-question 2WikiMultiHopQA-derived benchmark, six evaluated systems, and the three graph-ablation study designs |
| [[wiki/03-results-and-discussion\|Results and Discussion]] | Table 1/Table 2 numbers — baseline accuracy, cited vs. random ablation, isolation, and visited-but-uncited ablation results |
| [[wiki/04-conclusion-and-limitations\|Conclusion and Limitations]] | The trajectory-level provenance argument, and the authors' acknowledged scale/benchmark limitations |

## Original Source

- [source/source.md](source/source.md) — provenance pin: the original PDF (3.1 MB) exceeded this repo's 2 MB size guard and was not committed. Full text was extracted locally into `source/full.txt` / `source/chunks/`; both figures were rendered and cropped into `wiki/images/`. Retrieved 2026-08-21.
