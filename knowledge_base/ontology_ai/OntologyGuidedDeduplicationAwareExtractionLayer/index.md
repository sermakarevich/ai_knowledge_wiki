---
type: index
title: An Ontology-Guided, Deduplication-Aware Extraction Layer for Knowledge Graph Construction from Heterogeneous Documents
description: Folder index for the extraction-layer paper — orientation, reading order, and links to summary, digest, explainer, critical thinking, questions, and all 15 wiki pages.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-23T13:23:48Z
sources:
  - id: original
    resource: https://arxiv.org/abs/2607.28662v1
  - id: local-copy
    resource: source/source.md
tags: [knowledge-graphs, ontology-grounded-extraction, entity-resolution, RAG]
---

# An Ontology-Guided, Deduplication-Aware Extraction Layer for Knowledge Graph Construction from Heterogeneous Documents

This folder distils a production Kafka-based extraction layer that turns messy mixed documents into a validated, ontology-aligned knowledge graph. Start with the 2-minute summary for the headline results (recall ~70% → 95% with zero false merges), then use the digest and fifteen wiki pages for the retrieval, deduplication, and pipeline details.

## How to work through this

1. Read `summary.md` (~2 min) for the TL;DR, problem, ideas, findings, and roadmap.
2. Read `digest.md` (~10 min) for the fifteen one-sentence section distillations plus the five-move argument.
3. Dive into `wiki/` pages in order for full detail, using `explainer.md` for plain-language background, `critical_thinking.md` for claims-vs-evidence scrutiny, and `questions.md` for retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem and motivation, ideas, findings, roadmap.
- [Digest](digest.md) — fifteen verbatim one-sentence section summaries with key bullets.
- [Explainer](explainer.md) — plain-language walkthrough with jargon decoder.
- [Critical Thinking](critical_thinking.md) — claims vs evidence, novelty, weaknesses, verdict.
- [Questions](questions.md) — eighteen retrieval-practice Q&As covering every wiki page.

## Wiki

| Page | Covers |
|---|---|
| [01 — Introduction and System Overview](wiki/01-introduction-and-system-overview.md) | Kafka stream, ontology-tuned Qwen3.5-9B, five-stage pipeline, recall 70% → 95% |
| [02 — Related Work](wiki/02-related-work.md) | Prior LLM-for-KG work and where the architecture contribution sits |
| [03 — Static Catalog Slices to Live Retrieval](wiki/03-static-catalog-slices-to-live-retrieval.md) | Static-slice costs and live Neo4j content-conditioned retrieval (~94% saving) |
| [04 — Retrieval Refinements](wiki/04-retrieval-refinements-term-vectors-and-subclass-expansion.md) | Term-vector queries and one-hop subclass expansion |
| [05 — Predicate Recovery and Prompt Guards](wiki/05-predicate-recovery-and-prompt-guards.md) | G5 predicate lift (3 → 68) plus fan-out, orientation, vocabulary guards |
| [06 — Multi-Format Handlers](wiki/06-multi-format-handlers.md) | Six-signal per-page PDF classifier with mixed split-and-merge |
| [07 — Rule-Based Deduplication Algorithms](wiki/07-rule-based-deduplication-algorithms.md) | Alias schema, alias expansion, source-text mining, name-similarity scoring |
| [08 — Embedding Resolution Subsystem](wiki/08-embedding-resolution-subsystem.md) | Weighted composite, context gating, relationship folding, Phase 3 pipeline |
| [09 — Pipeline Engineering and Implementation](wiki/09-pipeline-engineering-and-implementation.md) | Embedding resolution layer and five-stage extraction pipeline |
| [10 — Relationship Normalisation and Finalization](wiki/10-relationship-normalisation-and-finalization.md) | Cleaning, cross-chunk merging, relationship second pass, enrichment |
| [11 — Evaluation and Quality Defects](wiki/11-evaluation-and-quality-defects.md) | `_env_int()` truncation bug and six Stage 2–3 cleaning fixes |
| [12 — Deduplication Insights](wiki/12-deduplication-insights.md) | Cleaning vs core algorithms as defense-in-depth plus OCR stress test |
| [13 — Empirical Results and Ablations](wiki/13-empirical-results-and-ablations.md) | OCR roadmap, local-vs-cloud benchmarks, conformance and end-to-end accuracy |
| [14 — Ethics, Limitations and Conclusion](wiki/14-ethics-limitations-and-conclusion.md) | Dual-use risks, mitigations, advantages, generalisation, reproducibility |
| [15 — Appendices and Threshold Reference](wiki/15-appendices-and-threshold-reference.md) | Table 22 thresholds, Kafka/concurrency tuning, field issues |

## Original Source

- arXiv: [An Ontology-Guided, Deduplication-Aware Extraction Layer for Knowledge Graph Construction from Heterogeneous Documents](https://arxiv.org/abs/2607.28662v1)
- Local copy: [source/source.md](source/source.md)
