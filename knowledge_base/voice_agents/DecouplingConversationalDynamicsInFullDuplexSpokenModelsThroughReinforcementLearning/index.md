---
type: index
title: Decoupling Conversational Dynamics in Full-Duplex Spoken Models through Reinforcement Learning
description: Folder index for DuplexPO, an RL framework that decouples when to speak from what to say to improve full-duplex turn-taking, backchanneling, and barge-in handling without degrading reasoning.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T12:14:13Z
sources:
  - id: original
    resource: https://arxiv.org/abs/2607.07148
  - id: local-copy
    resource: source/source.md
tags: [full-duplex-dialogue, reinforcement-learning, turn-taking, conversational-dynamics]
---
# Decoupling Conversational Dynamics in Full-Duplex Spoken Models through Reinforcement Learning

This folder collects study notes for Li et al. (2026), which proposes DuplexPO — reinforcement learning restricted to short dynamics-critical windows so a full-duplex voice model learns when to speak without relearning what to say. Start with the summary for the argument in two minutes, use the digest for the evidence in ten, then go deep in the wiki pages.

## How to work through this

1. Read `summary.md` (~2 min) for the TL;DR, problem diagnosis, and key findings.
2. Read `digest.md` (~10 min) for the argument in five moves plus one-sentence verdicts and key points per wiki page.
3. Work through the `wiki/` pages in order for equations, data recipe, evaluation, and ablations; use `explainer.md` for plain language, `critical_thinking.md` to stress-test the claims, and `questions.md` for retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem and motivation, main ideas, key findings.
- [Digest](digest.md) — section-by-section one-sentence verdicts with verbatim key points.
- [Explainer](explainer.md) — plain-language walkthrough of the decoupling idea and results.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, limits, and open objections.
- [Questions](questions.md) — retrieval practice covering every wiki page (Q1–Q14).

## Wiki

| Page | Covers |
| ---- | ------ |
| [01 Decoupling Conversational Dynamics](wiki/01-decoupling-conversational-dynamics.md) | Intelligence–dynamics trade-off, decoupling hypothesis, DuplexPO overview |
| [02 DuplexPO Framework](wiki/02-duplexpo-framework.md) | Dynamics-critical window sampling, FCDR setup, Eqs. 1–8, ASPIRin/ORISE contrast |
| [03 Factorized Reward and Optimization](wiki/03-factorized-reward-optimization.md) | Four FCDR components and ranges, GRPO objective Eqs. 9–10, DPO baseline |
| [04 Conversational Dynamics Evaluation](wiki/04-conversational-dynamics-evaluation.md) | Window-level results, mid-turn latency–interruption trade-off, judge wins, intelligence preservation |
| [05 References Opening](wiki/05-model-intelligence-results.md) | Bibliography opening, Acikgoz SpeakRL through Raux & Eskenazi, no results prose |
| [06 References Continued and Data Details](wiki/06-references.md) | Bibliography continued plus Appendix A training-data recipe |
| [07 Data Preprocessing](wiki/07-data-preprocessing.md) | Filtering to 24.6K Fisher / 43.1K Seamless samples, splits, augmentation, training stack, SFT controls, SIR/SRR |
| [08 Evaluation Protocol Appendix](wiki/08-evaluation-protocol-appendix.md) | Attention redistribution, judge calibration, pairwise judging protocol and prompts |
| [09 Judge Evaluation Details](wiki/09-judge-evaluation-details.md) | Reward dynamics, lead-time/buffer ablations, NRM vs FCDR, GRPO vs DPO, broader impacts |

## Original Source

- arXiv: [Decoupling Conversational Dynamics in Full-Duplex Spoken Models through Reinforcement Learning](https://arxiv.org/abs/2607.07148)
- Local copy: [source/source.md](source/source.md)
