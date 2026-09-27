---
type: index
title: "RRSI: Regularized Recursive Self-Improvement of Agent Harnesses"
description: "Folder index for the RRSI paper — regularized harness-level recursive self-improvement that trades evolve-set score for out-of-distribution transfer."
generated:
  by: claude/muse-spark-1.3-contributor
  at: "2026-09-24T02:44:08Z"
sources:
  - id: original
    resource: https://arxiv.org/pdf/2609.24972
  - id: local-copy
    resource: source/source.md
tags: [agent-harnesses, recursive-self-improvement, regularization, generalization]
---

# RRSI: Regularized Recursive Self-Improvement of Agent Harnesses

This folder collects notes on the RRSI paper, which frames iterative agent-harness evolution as adaptive optimization over a fully open edit space and regularizes the search trajectory instead. The headline result is smaller evolve-set gains than prior methods but robust transfer to held-out benchmarks at lower token cost. Start with the summary, then the digest, then the wiki pages for method and appendix details.

## How to work through this

1. Read [summary](summary.md) (~2 min) for the TL;DR, problem, ideas, findings, and future directions.
2. Read [digest](digest.md) (~10 min) for the full argument in nine verbatim section summaries plus the five-move arc.
3. Deep-dive the wiki pages in order ([01](wiki/01-rrsi-regularized-recursive-self-improvement.md) → [09](wiki/09-final-round-selection.md)), then test yourself with [questions](questions.md) and the [critical analysis](critical_thinking.md).

## Read This Folder

- [Summary](summary.md) — TL;DR, problem and motivation, original ideas, key findings, future directions.
- [Digest](digest.md) — section-by-section key points plus the five-move argument.
- [Explainer](explainer.md) — plain-language walkthrough of harness, overfitting, and RRSI regularizers.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, limits, and open questions.
- [Questions](questions.md) — retrieval-practice questions covering every wiki page.

## Wiki

| Page | Covers |
|------|--------|
| [01](wiki/01-rrsi-regularized-recursive-self-improvement.md) | Framing and proposal-side regularization: harness RSI, evolve-set overfitting, annealed budgets and history-aware proposer |
| [02](wiki/02-test-time-computation-vs-reusable-mechanisms.md) | Test-time compute vs. reusable mechanisms: generalization definition, three overfitting behaviors, adaptive optimization framing |
| [03](wiki/03-regularization-view-of-harness-evolution.md) | Regularization view: open reachable set, proposal capacity control, selection survival criteria and L0/L1/L2 analogies |
| [04](wiki/04-environments-and-experimental-setup.md) | Environments and setup: three evolve domains, held-out/OOD splits, frozen-policy protocol and headline results |
| [05](wiki/05-ablation-proposal-vs-acceptance-regularizers.md) | Ablation and transfer: proposal vs. acceptance regularizers, cross-policy transfer, cost and conclusions |
| [06](wiki/06-references.md) | References segment: model releases, harness-evolution methods, benchmarks, memory/reasoning and theory background |
| [07](wiki/07-references-continued.md) | References continued and appendix opening: paired-window evaluation protocol, four baselines, round-level formulation |
| [08](wiki/08-selection-rule-and-appendix-details.md) | Selection rule and appendix bookkeeping: retention, edit budget, history, novelty, stability and cost branches, domain guards |
| [09](wiki/09-final-round-selection.md) | Final-round selection: admissibility, hyperparameters, case-study accept/reject trajectories |

## Original Source

- ArXiv PDF: [RRSI: Regularized Recursive Self-Improvement of Agent Harnesses](https://arxiv.org/pdf/2609.24972)
- Local copy: [source/source.md](source/source.md)
