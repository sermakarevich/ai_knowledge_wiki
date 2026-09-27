---
type: index
title: "Just-in-Time Memory: Learning to Curate Task-Adaptive Memory for LLM Agents"
description: "Folder index for the JITMEM paper — defer memory curation to read time, train only the curator with GRPO on immediate task reward."
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-27T04:05:41Z
sources:
  - id: original
    resource: https://arxiv.org/pdf/2609.27334
  - id: local-copy
    resource: source/source.md
tags: [llm-agents, episodic-memory, read-time-curation, GRPO]
---

# Just-in-Time Memory: Learning to Curate Task-Adaptive Memory for LLM Agents

JITMEM stores raw agent trajectories losslessly and curates them just in time at read time into a compact task-conditioned briefing. Even the untrained curator beats strong write-time baselines, and GRPO training on immediate same-task reward adds large gains (+16.2 ALFWorld, +16.3 WebShop, +3.9 τ²-bench) with fewer tokens and cross-executor transfer.

## How to work through this

Start with the [Summary](summary.md) (~2 min) for the TL;DR and headline numbers, then read the [Digest](digest.md) (~10 min) for the full argument in nine verbatim chunks. Go deeper with the [wiki pages](wiki/01-introduction-and-problem.md) in order, use the [Explainer](explainer.md) for plain-language intuition, the [Critical Thinking](critical_thinking.md) notes for strengths and blind spots, and the [Questions](questions.md) for retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem, ideas, findings, future directions (~2 min).
- [Digest](digest.md) — nine verbatim chunks, one per wiki page (~10 min).
- [Explainer](explainer.md) — plain-language walkthrough: what, why, how, where used.
- [Critical Thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, verdict.
- [Questions](questions.md) — 16 retrieval-practice Q&A covering every wiki page.

## Wiki

| Page | Covers |
|------|--------|
| [01](wiki/01-introduction-and-problem.md) | Introduction and Problem: write-time vs just-in-time memory curation |
| [02](wiki/02-background-and-related-work.md) | Background and Related Work: read-time vs write-time curation |
| [03](wiki/03-method-retrieve-curate-execute.md) | Method: Retrieve, Curate, Execute, Update loop and GRPO curator training |
| [04](wiki/04-main-results-alfworld-webshop.md) | Main Results on ALFWorld and WebShop across three executors |
| [05](wiki/05-ablations-and-analysis.md) | Ablations and Analysis: write-time distillation, bank dynamics, task-adaptivity |
| [06](wiki/06-references.md) | References (Liu–Zhou block) and Appendix A prompt start |
| [07](wiki/07-appendix-prompts-a.md) | Appendix A: executor, judge, and distillation prompts |
| [08](wiki/08-appendix-training-setup.md) | Appendix: training setup (hyperparameters and optimization) |
| [09](wiki/09-appendix-example-payloads.md) | Appendix: example payloads and GRPO training curves |

## Original Source

- ArXiv PDF: [2609.27334](https://arxiv.org/pdf/2609.27334)
- Local copy: [source/source.md](source/source.md)
