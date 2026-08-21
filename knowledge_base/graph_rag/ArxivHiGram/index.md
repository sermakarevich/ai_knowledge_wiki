---
type: Paper
title: "HiGram: Hierarchical Graph Memory for LLM Agents with Path-level Localization and Rewrite"
description: A hierarchical graph memory for LLM agents that localizes a query- and update-relevant evidence path via MicroGraphs, then coordinately rewrites only that bounded region, cutting token cost while improving long-term QA and conflict resolution.
generated: { by: claude/claude-sonnet-5, at: 2026-08-21T07:14:01Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2608.05095
  - id: local-copy
    resource: source/chunks/
tags: [graph-memory, llm-agents, memory-update, retrieval-localization, conflict-resolution]
---

# HiGram: Hierarchical Graph Memory for LLM Agents with Path-level Localization and Rewrite

HiGram (Yue et al., 2026-08) is a graph memory framework for long-horizon LLM agents that organizes memory into a two-tier hierarchy, localizes the small evidence path relevant to a query and an incoming update via lightweight "MicroGraphs," and then performs coordinated rewriting strictly within that bounded region instead of rewriting memory units independently. The paper argues this closes a granularity mismatch in prior graph-memory systems — retrieval and update act on the whole graph while answers depend on small localized structures — and reports gains in both answer quality and token efficiency on LoCoMo and MemConflict. Worth ingesting because it's a clean, well-ablated design for the "update memory without re-searching the whole graph every time" problem that recurs across agent-memory systems in this KB.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~10-15 min each) — one part of the paper, deep. Each opens with its headline and key points, so you can stop early.

_New to graph-based agent memory? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

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
| [[wiki/01-hierarchical-memory-and-method\|Hierarchical Memory and the HiGram Method]] | The granularity-mismatch problem, the two-tier hierarchical graph (upper-level nodes + MemoryUnits), MicroGraph-based path-level localization, and coordinated intra-/inter-unit rewriting (paper sections 1-3). |
| [[wiki/02-experiments-and-results\|Experiments and Results]] | Setup and baselines on LoCoMo and MemConflict, main results, ablations of MicroGraph organization and the support subgraph, memory-update-strategy comparison, hyperparameter sensitivity, and the conclusion (paper sections 4-5). |

## Original Source

- [source/chunks/](source/chunks/) — extracted markdown text split into 2 chunks (`01.txt`, `02.txt`); no single local PDF copy is kept, retrieved 2026-08-21. See `source/provenance.md` for extraction details.
