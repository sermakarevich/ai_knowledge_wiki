---
type: Paper
title: "Natural Language Knowledge Graph Query Execution: Leveraging Controlled Semantics in the LLM Context Window"
description: Single-call zero-shot NL-to-SPARQL with the full OWL ontology in the LLM context window plus wrapper ontologies and a deterministic rewriter, reaching 89.9% Match on DBLP-QuAD 3.1, 98/100 on SemOpenAlex, and 100% on neuroimaging metadata.
generated: { by: claude/muse-spark-1.3-contributor, at: 2026-09-23T13:15:24Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2609.14652v1
  - id: local-copy
    resource: source/source.md
tags: [knowledge-graphs, sparql, llm-prompting, ontologies, benchmarking]
---

# Natural Language Knowledge Graph Query Execution: Leveraging Controlled Semantics in the LLM Context Window

This folder summarises Fitch's NLKGQ paper: controlled OWL semantics in the context window for single-call zero-shot SPARQL generation, wrapper ontologies with deterministic rewriting for opaque vocabularies, and the deterministic DBLP-QuAD 3.1 benchmark revision. Start with the summary for the headline results, use the digest and wiki pages for the mechanism, wrappers, and evaluation details.

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

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-natural-language-knowledge-graph-query-execution\|Natural Language Knowledge Graph Query Execution]] | Title/front-matter opener of the paper (short header chunk, no substantive claims) |
| [[wiki/02-paper-body\|NLKGQ paper body — controlled semantics, wrappers, and benchmarks]] | Main paper body: single-call mechanism, controlled semantics, wrapper ontologies, DBLP-QuAD 3.1 revision, cross-domain and model evaluations, error analysis |

## Original Source

- [arXiv:2609.14652v1](https://arxiv.org/abs/2609.14652v1) — original paper
- [source/source.md](source/source.md) — local copy of the source text
