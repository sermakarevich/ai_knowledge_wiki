---
type: index
title: An Empirical Study on the Code Refactoring Capability of Large Language Models
description: Folder index for the StarCoder2-vs-developers Java refactoring study — orientation, reading order, and links to summary, digest, explainer, and all wiki pages.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-23T21:24:31Z
sources:
  - id: original
    resource: https://arxiv.org/abs/2411.02320v1
  - id: local-copy
    resource: source/source.md
tags: [code-refactoring, large-language-models, code-smells, empirical-study]
---

# An Empirical Study on the Code Refactoring Capability of Large Language Models

This folder summarises the arXiv study comparing StarCoder2-generated Java refactorings against developer refactorings on 30 leak-free open-source projects. The headline result is complementarity: StarCoder2 removes more surface-level smells while developers win on architecture-sensitive design, and one-shot prompting with multi-generation is the recommended recipe. Use the reading path below to go from a 2-minute overview to the full per-RQ evidence.

## How to work through this (summary ~2 min → digest ~10 min → wiki pages)

1. Start with the [summary](summary.md) (~2 min) for the TL;DR, headline numbers, and takeaways.
2. Read the [digest](digest.md) (~10 min) for the verbatim per-chunk condensations of every wiki page plus the five-move argument.
3. Deep-dive into the [wiki pages](wiki/01-empirical-study-overview.md) in order for full evidence, then test yourself with [questions](questions.md), check the plain-language [explainer](explainer.md), and read the adversarial [critical analysis](critical_thinking.md).

## Read This Folder

- [Summary](summary.md) — 2-minute TL;DR, findings, and future directions.
- [Digest](digest.md) — 10-minute verbatim condensations of all 12 wiki chunks plus the argument in five moves.
- [Explainer](explainer.md) — plain-language guide: what the study does, why it matters, and where to use it.
- [Critical thinking](critical_thinking.md) — claims-vs-evidence audit, weaknesses, applicability, and verdict.
- [Questions](questions.md) — 13 retrieval-practice questions with answers covering every wiki page.

## Wiki

| Page | Covers |
|---|---|
| [01](wiki/01-empirical-study-overview.md) | Study overview: goals, StarCoder2 choice, 30-project corpus, and headline results |
| [02](wiki/02-rq1-llm-vs-developers.md) | RQ1 setup: leakage-controlled design, pure-refactoring commits, smell/metric/test harness |
| [03](wiki/03-experiment-setup-metrics.md) | Code metrics: complexity, cohesion, coupling, modularity via Understand (Table 1) |
| [04](wiki/04-refactoring-generation-method.md) | Generation method: zero-shot prompt, chunking, Pass@1/3/5 judging, IR and statistics |
| [05](wiki/05-rq1-findings-smell-reduction.md) | RQ1 findings: 44.36% vs 24.27% smell reduction, metric wins, 57.15% Pass@5 |
| [06](wiki/06-rq2-code-smell-types.md) | RQ2 smell types: LLM sweeps 7/8 implementation smells, developers win design smells |
| [07](wiki/07-rq3-refactoring-types.md) | RQ3 Figure 6 chunk: garbled frequency figure, labels only, no recoverable numbers |
| [08](wiki/08-rq3-findings-preferences.md) | RQ3 preferences: syntactic vs structural refactoring payoffs and complementarity |
| [09](wiki/09-rq4-prompt-engineering.md) | RQ4 prompting: one-shot and chain-of-thought beat zero-shot (Scott-Knott Rank 1) |
| [10](wiki/10-rq4-results-validity.md) | RQ4 context and validity: identical-server setup, internal/external/construct limits |
| [11](wiki/11-threats-related-work.md) | Bibliography [1]–[33]: LLM foundations, refactoring literature, statistics |
| [12](wiki/12-references-appendix.md) | Bibliography [34]–[54] tail: smells, tooling, LLM-for-code evaluation |

## Original Source

- arXiv: [An Empirical Study on the Code Refactoring Capability of Large Language Models](https://arxiv.org/abs/2411.02320v1)
- Local copy: [source/source.md](source/source.md)
