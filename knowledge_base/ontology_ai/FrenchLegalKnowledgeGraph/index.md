---
type: index
title: LLM-Assisted Ontology Engineering and Construction of a French Legal Knowledge Graph
description: Folder index for the LLM-assisted French maintenance-law ontology and knowledge graph paper, linking summary, digest, explainer, critical analysis, questions, and wiki pages.
generated:
  by: claude/opencode-go/muse-spark-1.3-contributor
  at: 2026-09-23T13:09:56Z
sources:
  - id: original
    resource: https://arxiv.org/abs/2607.24551v1
  - id: local-copy
    resource: source/source.md
tags: [legal-knowledge-graph, ontology-engineering, llm-extraction, french-law, semantic-web]
---

# LLM-Assisted Ontology Engineering and Construction of a French Legal Knowledge Graph

This folder distils a paper that builds a two-stage LLM-plus-ontology pipeline turning 6,370 French maintenance-law articles into a queryable knowledge graph. Start with the short summary for the big picture, then use the digest and wiki pages for the workflow details, evaluation numbers, and critical analysis.

## How to work through this

1. Read `summary.md` (~2 min) for the TL;DR, main ideas, and key findings.
2. Read `digest.md` (~10 min) for the argument in five moves plus verbatim key points per wiki page.
3. Go deeper with the wiki pages, `explainer.md` for plain-language background, `critical_thinking.md` for claims-versus-evidence analysis, and `questions.md` for retrieval practice.

## Read This Folder

- [Summary](summary.md) — human-readable and technical TL;DR, problem, ideas, findings, future directions.
- [Digest](digest.md) — per-page key points plus the argument in five moves.
- [Explainer](explainer.md) — plain-language walkthrough with jargon decoder.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, weaknesses, applicability, verdict.
- [Questions](questions.md) — retrieval-practice questions covering every wiki page.

## Wiki

| Page | Covers |
| ---- | ------ |
| [01 LLM-Assisted Ontology Engineering](wiki/01-llm-assisted-ontology-engineering.md) | Two-stage workflow, SEMLEG scope, 6,370-article corpus, open extraction, embedding fusion, property induction (OpenAI vs Mistral variants) |
| [02 Knowledge Graph Construction and Evaluation](wiki/02-knowledge-graph-construction-evaluation.md) | Closed extraction over full corpus, fusion statistics, R_JSON/R_class/R_prop/R_sig metrics, qualitative errors, SPARQL competency questions, future work |

## Original Source

- arXiv: [LLM-Assisted Ontology Engineering and Construction of a French Legal Knowledge Graph](https://arxiv.org/abs/2607.24551v1)
- Local copy: [source/source.md](source/source.md)
