---
type: index
title: "Coding Agents are Strong Prompt Optimizers"
description: "Folder index for Singh et al. (2026) CASD — single offline coding-agent pass over frozen rollouts that beats iterative prompt search at ~$1.60."
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-26T04:31:41Z
sources:
  - id: original
    resource: https://arxiv.org/pdf/2609.26261
  - id: local-copy
    resource: source/source.md
tags: [prompt-optimization, coding-agents, offline-distillation, agentic-benchmarks]
---

# Coding Agents are Strong Prompt Optimizers

This folder distills Singh et al. (2026): Coding-Agent Skill Distillation (CASD), a single offline pass in which an unmodified coding agent analyzes frozen rollout logs with code and writes a skill file used directly as the optimized prompt. Start with the 2-minute summary, deepen with the 10-minute digest, then use the wiki pages for method, theory, and ablations.

## How to work through this

1. Read [summary.md](summary.md) (~2 min) for the TL;DR, problem, ideas, and headline results.
2. Read [digest.md](digest.md) (~10 min) for the five wiki summaries plus the five-move argument.
3. Deep-dive the wiki pages in order, then [explainer.md](explainer.md) for plain language, [critical_thinking.md](critical_thinking.md) for skepticism, and [questions.md](questions.md) for retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem and motivation, main ideas, key findings.
- [Digest](digest.md) — one-sentence plus key-points per wiki page and the argument in five moves.
- [Explainer](explainer.md) — plain-language handbook analogy, how it works, where to use it.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, applicability, verdict.
- [Questions](questions.md) — ten retrieval-practice Q&A covering every wiki page.

## Wiki

| Page | Covers |
|------|--------|
| [01](wiki/01-casd-overview.md) | CASD overview: single offline distillation recipe, headline results and cost |
| [02](wiki/02-head-to-head-results.md) | Contributions, related work, method setup, distillation pass and workflow |
| [03](wiki/03-method-and-theory.md) | Unified optimization view, bias–variance, operating regimes, setup, matched-data results and cost |
| [04](wiki/04-why-corpus-scope-wins.md) | Why corpus scope wins: statistical rules, duplicates, gateless pass, Figure 4 absences |
| [05](wiki/05-reasoning-gap-ablation.md) | Reasoning-gap ablation, limitations, and conclusion |

## Original Source

- ArXiv PDF: [Coding Agents are Strong Prompt Optimizers](https://arxiv.org/pdf/2609.26261)
- Local copy: [source/source.md](source/source.md)
