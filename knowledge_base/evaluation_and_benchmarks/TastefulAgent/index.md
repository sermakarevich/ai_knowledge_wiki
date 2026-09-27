---
type: index
title: "The Tasteful Agent: Measuring and Improving Taste in Long-Horizon Tasks"
description: "Folder index for the Tasteful Agent paper: taste as long-horizon fork choice, Taste-Bench construction and results, and distilling taste into end-to-end gains."
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-26T04:45:46Z
sources:
  - id: original
    resource: https://arxiv.org/pdf/2609.25804
  - id: local-copy
    resource: source/source.md
tags: [ai-agents, taste-bench, long-horizon-reasoning, judgment-distillation]
---

# The Tasteful Agent: Measuring and Improving Taste in Long-Horizon Tasks

This folder summarises the paper that defines agent "taste" as good long-horizon direction choice and builds Taste-Bench, 502 outcome-labeled decision forks mined from engineering and research trajectories. Frontier models peak near 60% on binary choices with far-horizon errors resisting extra reasoning, yet taste distills into a small student and lifts end-to-end task success. Start with the summary, deepen with the digest, then use the wiki pages and retrieval questions.

## How to work through this (summary ~2 min → digest ~10 min → wiki pages)

1. Read [summary](summary.md) (~2 min) for the TL;DR, problem, ideas, findings, and future directions.
2. Read [digest](digest.md) (~10 min) for the per-chunk argument in thirteen verbatim-mirrored sections plus the five-move arc.
3. Go deep via the wiki pages in order, then test yourself with [questions](questions.md); check assumptions in [critical thinking](critical_thinking.md) and intuition in [explainer](explainer.md).

## Read This Folder

- [Summary](summary.md) — TL;DR, problem and motivation, original ideas, key findings, future directions.
- [Digest](digest.md) — thirteen chunk summaries with key points plus the five-move argument.
- [Explainer](explainer.md) — plain-language walkthrough of taste, forks, results, and distillation.
- [Critical thinking](critical_thinking.md) — claims-vs-evidence check, limits, and open questions.
- [Questions](questions.md) — seventeen retrieval-practice questions covering every wiki page.

## Wiki

| Page | Covers |
| ---- | ------ |
| [01](wiki/01-introduction-and-taste-definition.md) | Taste definition and Taste-Bench overview (502 forks, best model 59.7%) |
| [02](wiki/02-measuring-taste-via-hindsight.md) | Fork formalism, parallel vs detour mining, filters, human review, scoring |
| [03](wiki/03-model-accuracy-results.md) | Frontier accuracy, subset splits, horizon gradient, reasoning-budget null |
| [04](wiki/04-taste-bench-vs-end-to-end-benchmarks.md) | Correlation with SWE-bench Verified plus Qwen3.6-27B distillation transfer |
| [05](wiki/05-related-work.md) | Positioning vs long-horizon, pre-outcome, process, and distillation work |
| [06](wiki/06-references-and-appendix-opening.md) | Trajectory pools, fork statistics, validation rules, generator prompts |
| [07](wiki/07-appendix-goal-spec.md) | Goal-spec acceptance and rejection filters plus detour-generator prompts |
| [08](wiki/08-appendix-required-json-format.md) | Miner JSON schema, judge panel, filter prompts, filtering yield |
| [09](wiki/09-filtering-undecidable-examples.md) | Removed undecidable fork, per-cell examples, evaluation prompt |
| [10](wiki/10-evaluation-prefix-rendering.md) | Prefix rendering, truncation, answer parsing, both-orders scoring |
| [11](wiki/11-time-horizon-annotation-levels.md) | Horizon accuracies, budget interaction, judge/human agreement, distillation recipe |
| [12](wiki/12-distillation-fold-splits.md) | Task-disjoint folds, transfer scores, end-to-end advice experiment |
| [13](wiki/13-trailing-fragment.md) | Placeholder for empty trailing chunk 33 |

## Original Source

- ArXiv PDF: [2609.25804](https://arxiv.org/pdf/2609.25804)
- Local copy: [source](source/source.md)
