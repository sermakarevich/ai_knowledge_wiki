---
type: index
title: 'DebugRepair: Enhancing LLM-Based Automated Program Repair via Self-Directed Debugging'
description: Folder index for the DebugRepair paper — orientation, reading order, and links to summary, digest, explainer, critical thinking, questions, and all wiki pages.
generated:
  by: claude/muse-spark-1.3-contributor
  at: '2026-09-23T21:32:03Z'
sources:
  - id: original
    resource: https://arxiv.org/abs/2604.19305v1
  - id: local-copy
    resource: source/source.md
tags:
  - automated-program-repair
  - llm-debugging
  - software-testing
  - runtime-traces
---

# DebugRepair: Enhancing LLM-Based Automated Program Repair via Self-Directed Debugging

DebugRepair replaces outcome-level failure symptoms (e.g. stack traces) with intermediate runtime evidence collected through self-directed simulated debugging. It combines test semantic purification, hybrid LLM plus rule-based instrumentation, and hierarchical conversational repair, fixing 224 Defects4J bugs on GPT-3.5 and 295 on DeepSeek-V3 at the lowest per-bug cost among compared baselines.

## How to work through this

1. Start with [summary](summary.md) (~2 min) for the TL;DR, problem, ideas, and findings.
2. Then read [digest](digest.md) (~10 min) for the section-by-section argument in five moves.
3. Then go deep in any order via the [wiki table](#wiki): each page has **In one sentence:** plus **Key points**, with retrieval practice in [questions](questions.md).

## Read This Folder

- [summary](summary.md) — TL;DR, problem and motivation, main ideas, key findings, future directions.
- [digest](digest.md) — verbatim per-section condensation of all 15 wiki pages plus the five-move argument.
- [explainer](explainer.md) — plain-language version: what it is, why it matters, how it works, where to use it, jargon decoder.
- [critical_thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, applicability, verdict (trial).
- [questions](questions.md) — 16 retrieval questions (Q1–Q15 per wiki page plus Q16 synthesis) with answers.

## Wiki

| Page | Covers |
|---|---|
| [01](wiki/01-framework-overview.md) | Framework overview: three components and headline 224 / 295 Defects4J gains |
| [02](wiki/02-background-and-limitations.md) | Background and limitations: why APR needs debugging augmentation |
| [03](wiki/03-motivation-example.md) | Chart-24 motivation: symptom-only patch vs. runtime-state diagnosis |
| [04](wiki/04-framework-workflow.md) | Fig. 2 workflow illustration with TimeSeries createCopy example |
| [05](wiki/05-test-semantic-purification.md) | Test semantic purification: backward slicing with alias-aware rescans |
| [06](wiki/06-simulated-instrumentation.md) | Simulated instrumentation: LLM prints with consistency check plus AST fallback |
| [07](wiki/07-conversational-repair.md) | Debugging-driven conversational repair: sessions, rounds, augmentation |
| [08](wiki/08-evaluation-setup.md) | Evaluation setup: 15 baselines, metrics, budgets, 224-fix headline |
| [09](wiki/09-main-results.md) | Main results: totals, unique-fix leads, Lang-6 case study |
| [10](wiki/10-results-analysis.md) | Results analysis: single-function / single-hunk scenarios and orthogonality |
| [11](wiki/11-comparison-and-generality.md) | Comparison and generality: complex vs. single-line bugs, 51.3% lift across LLMs |
| [12](wiki/12-ablation-test-purification.md) | Ablation: purification removal 224 to 164 and 18.6% token cut |
| [13](wiki/13-ablation-repair-rounds.md) | Repair rounds and budget: sessions, augmentation, cost, validity threats |
| [14](wiki/14-conclusion-and-references-a.md) | References part A ([1]–[32]): models, APR foundations, benchmarks |
| [15](wiki/15-references-b.md) | References part B ([33]–[51]): debugging-driven work, surveys, decoders |

## Original Source

- arXiv: [DebugRepair: Enhancing LLM-Based Automated Program Repair via Self-Directed Debugging](https://arxiv.org/abs/2604.19305v1)
- Local copy: [source](source/source.md)
