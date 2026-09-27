---
type: index
title: 'Natural Language Access to Domain-Specific Metadata: A Reusable Framework for LLM Query Generation'
description: Folder index for the NLKGQ paper — ontology-first zero-shot SPARQL generation over MRI metadata, 100% SPARQL vs 57% auto-SQL, with summary, digest, and wiki map.
generated:
  by: claude/muse-spark-1.3-contributor
  at: '2026-09-23T13:26:54Z'
sources:
  - id: original
    resource: https://arxiv.org/abs/2607.18029v2
  - id: local-copy
    resource: source/source.md
tags: [text-to-SPARQL, ontology-design, knowledge-graphs, LLM-evaluation]
---

# Natural Language Access to Domain-Specific Metadata: A Reusable Framework for LLM Query Generation

This folder distils the NLKGQ paper: an ontology-first process that lets LLMs turn plain-language questions into SPARQL zero-shot over domain metadata. The demo on a large MRI archive reaches 100% on 21 expert questions, with readable names and annotations dominating accuracy. Start with the summary, then the digest, then the wiki pages for evidence and caveats.

## How to work through this

1. **Summary (~2 min)** — the TL;DR, problem, ideas, findings, and limits.
2. **Digest (~10 min)** — nine verbatim section distillates plus the five-move argument.
3. **Wiki pages** — full per-section evidence, then `explainer.md`, `critical_thinking.md`, and `questions.md` for retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR and key findings in one page.
- [Digest](digest.md) — all nine section distillates plus the argument in five moves.
- [Explainer](explainer.md) — plain-language walkthrough with jargon decoder.
- [Critical thinking](critical_thinking.md) — claims vs evidence, weaknesses, applicability, verdict.
- [Questions](questions.md) — 14 retrieval-practice Q&A covering every wiki page.

## Wiki

| Page | Covers |
|------|--------|
| [01 Overview and Framework Intro](wiki/01-overview-and-framework-intro.md) | NLKGQ framework, ontology-first process, MRI demo, 100% result |
| [02 Background and Annotation Impact](wiki/02-background-and-annotation-impact.md) | Related work, four contributions, annotation/representation effects |
| [03 Ontology Richness and Design Principles](wiki/03-ontology-richness-and-design-principles.md) | Six OWL naming principles, ETL/KG build, NLKGQ server prompt |
| [04 Iterative Development and Methods](wiki/04-iterative-development-and-methods.md) | Co-evolution loop, test driver, 8 ontology representations, OWL-to-SQL converter, Qwen3 hardware |
| [05 Framework Architecture and Production System](wiki/05-framework-architecture-and-production-system.md) | Evaluation protocol, example SPARQL queries, model/representation accuracy |
| [06 Model Comparison Results](wiki/06-model-comparison-results.md) | Per-model, per-representation, per-prompt, per-temperature results; SQL peak 57% |
| [07 SPARQL vs SQL Evaluation](wiki/07-sparql-vs-sql-evaluation.md) | 21/21 vs 12/21 gap, OWL structural advantages, EAV control, local-hardware result |
| [08 Limitations and Unmeasured Gaps](wiki/08-limitations-and-unmeasured-gaps.md) | Auto-SQL scope, dense-vs-MoE, quantization, single-domain/Qwen3-only limits |
| [09 System Summary and Conclusions](wiki/09-system-summary-and-conclusions.md) | Source-chunk note: Qwen3 SPARQL/SQL statement plus reference list [1]–[35] |

## Original Source

- arXiv: [Natural Language Access to Domain-Specific Metadata: A Reusable Framework for LLM Query Generation](https://arxiv.org/abs/2607.18029v2)
- Local copy: [source/source.md](source/source.md)
