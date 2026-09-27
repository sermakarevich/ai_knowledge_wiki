---
type: index
title: "Open Ontologies: Tool-Augmented Ontology Engineering with Stable Matching Alignment"
description: "Folder index for the Open Ontologies paper — Rust MCP ontology engineering system with stable 1-to-1 alignment (Anatomy F1 0.832) and structured tool access beating raw OWL reading."
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-23T13:16:10Z
sources:
  - id: original
    resource: https://arxiv.org/abs/2605.09184v1
  - id: local-copy
    resource: source/source.md
tags: [ontology-engineering, ontology-alignment, MCP, OWL-reasoning, LLMs]
---

# Open Ontologies: Tool-Augmented Ontology Engineering with Stable Matching Alignment

This folder summarises the Open Ontologies paper (arXiv:2605.09184v1, 9 May 2026): a Rust single-binary system exposing ontology construction, OWL-RL reasoning, and alignment as MCP tools. Start with the summary for the headline numbers, then the digest and wiki pages for evidence, then the explainer, critical analysis, and retrieval questions to test understanding.

## How to work through this

1. **Summary (~2 min)** — headline results: stable 1-to-1 matching (Anatomy F1 0.832, P 0.963), MCP tools (F1 0.717) vs raw OWL (0.323) vs unaided LLM (0.431).
2. **Digest (~10 min)** — the argument in five moves plus per-section key points, all verbatim from the wiki pages.
3. **Wiki pages** — full evidence: system architecture and Anatomy/Conference results, tool-access ablation and reasoning comparisons, references fragment; then explainer, critical thinking, and questions.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem, ideas, findings, future directions.
- [Digest](digest.md) — section-by-section key points plus the five-move argument.
- [Explainer](explainer.md) — plain-language walkthrough with analogies and jargon decoder.
- [Critical thinking](critical_thinking.md) — claims vs evidence, novelty, weaknesses, applicability, verdict.
- [Questions](questions.md) — 7 retrieval-practice questions covering every wiki page.

## Wiki

| Page | Covers |
|---|---|
| [01 — Tool-Augmented Ontology Engineering](wiki/01-tool-augmented-ontology-engineering.md) | Abstract through §4.3 (Table 3 caption only; table body truncated in chunk) — system overview, MCP tooling, stable matching alignment approach |
| [02 — Condition Input F1: LLM Alone vs Raw File vs MCP Tools](wiki/02-evaluation-results.md) | Conditions B/D/C ablation; Why D < B; per-ontology variance; disentanglement; §4.4 reasoning performance; §4.5 Pizza construction; §5 ablation tables 5–6; §§6–8 discussion, limitations, conclusion |
| [03 — References](wiki/03-references.md) | References 19–23 (bibliography fragment only; no body text in chunk) |

## Original Source

- arXiv: [https://arxiv.org/abs/2605.09184v1](https://arxiv.org/abs/2605.09184v1)
- Local copy: [source/source.md](source/source.md)
