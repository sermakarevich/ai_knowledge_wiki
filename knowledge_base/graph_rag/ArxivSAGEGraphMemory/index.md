---
type: Paper
title: "SAGE: A Self-Evolving Agentic Graph-Memory Engine for Structure-Aware Associative Memory"
description: A policy-based memory writer and a Graph-Foundation-Model memory reader trained in alternating rounds so the memory graph itself, not just the retrieval trajectory, self-evolves.
generated: { by: claude/claude-sonnet-5, at: 2026-08-21T12:26:00Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2605.12061
  - id: local-copy
    resource: source/full_text.md
tags: [graph-memory, graphrag, agent-memory, reinforcement-learning, graph-foundation-model]
---

# SAGE: A Self-Evolving Agentic Graph-Memory Engine for Structure-Aware Associative Memory

SAGE (Wang et al., 2026) reframes long-term agent memory as a coupled write–read–evolve problem: a policy-based writer builds a graph memory, a Graph-Foundation-Model reader retrieves from it via structure-aware propagation, and the two are trained in alternating rounds so the graph and the retriever co-adapt. It is a 62-page paper with roughly two-thirds of its length in appendices — theoretical bounds (SNR, retrieval budget, stability under graph drift) and exhaustive ablations backing up the method described in the main body.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every wiki page's headline and key points.
3. **Wiki pages below** (~10-20 min each) — one source chunk, deep. Each opens with its headline and key points, so you can stop early.

_New to graph memory or GraphRAG? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

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
| [[wiki/01-challenges-and-related-work\|Challenges and Related Work]] | Intro, Related Work (RAG/GraphRAG, agent memory, graph foundation models), Preliminary formalization of the memory sample, writer, and reader |
| [[wiki/02-method-writer-and-reader\|Method: Memory Writer + Memory Reader]] | Section 4 — the RL-trained writer, the GFM reader (query planning, soft addressing, structural gating, context–schema split), and the self-evolution loop |
| [[wiki/03-experiments-and-conclusion\|Experiments and Conclusion]] | Section 5 — four research questions, multi-hop/open-domain QA results, long-term memory benchmarks, retrieval efficiency, and the conclusion |
| [[wiki/04-appendix-writer-analysis-snr\|Appendix A & B — Writer Analysis and SNR / Retrieval-Budget Theory]] | Reward-design ablations, cross-domain transfer, writing-protocol sweeps, and the theoretical SNR and retrieval-budget bounds behind the GFM reader |
| [[wiki/05-appendix-calibration-stability-theory\|Appendix C–F — Calibration, Stability, and the Writer–Reader Loop Theory]] | Context–schema decomposition optimality, writer-induced distribution shift, reader stability under graph drift, and the coordinate-improvement theory of self-evolution |
| [[wiki/06-appendix-ablations-and-implementation\|Appendix G–O — Ablations and Implementation]] | Reader ablations (structural gating vs. uniform propagation vs. vanilla GNN), selector design, complexity analysis, pretraining/fine-tuning objectives, and the writer's MDP formulation |
| [[wiki/07-appendix-additional-results-case-studies\|Appendix P–R — Additional Results and Case Studies]] | Full result tables (multi-hop QA, AmazonQA, HaluMem), a HotpotQA path-interpretation case study, dataset/baseline details, limitations, broader impact, compute, licenses, and the NeurIPS checklist |

## Original Source

- [source/full_text.md](source/full_text.md) — pymupdf4llm extraction of the original PDF, retrieved 2026-08-21. The original PDF (downloaded to `/tmp/sage.pdf`, 62 pages) was **not** retained in this repo per the size-guard policy against committing PDFs to `.kb`; this markdown extraction is the local copy of record. Canonical source: [arxiv.org/abs/2605.12061](https://arxiv.org/abs/2605.12061).
