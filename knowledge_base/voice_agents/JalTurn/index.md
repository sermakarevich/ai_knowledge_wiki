---
type: index
title: 'JAL-Turn: Joint Acoustic-Linguistic Modeling for Real-Time and Robust Turn-Taking Detection in Full-Duplex Spoken Dialog'
description: Folder index for the JAL-Turn paper notes — a lightweight dual-encoder turn-taking detector fusing SenseVoice and CPC cues with shared-encoder ASR inference at 12–38 ms latency.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T11:59:09Z
sources:
  - id: original
    resource: https://arxiv.org/abs/2603.26515
  - id: local-copy
    resource: source/source.md
tags: [turn-taking, full-duplex, spoken-dialogue, low-latency]
---

# JAL-Turn: Joint Acoustic-Linguistic Modeling for Real-Time and Robust Turn-Taking Detection in Full-Duplex Spoken Dialog

JAL-Turn is a lightweight speech-only turn-taking detector that fuses linguistic cues from a frozen SenseVoice encoder with acoustic cues from a frozen CPC encoder to predict Hold vs. Shift in real time. Its SenseVoice encoder is shared with ASR for single-pass parallel inference at 12–38 ms, trained on automatically labeled stereo conversation via a VAD future-window pipeline. Start with the summary, then the digest, then the six wiki pages for pipeline, architecture, experiments, and ablations.

## How to work through this

1. Read `summary.md` (~2 min) for the TL;DR, problem, ideas, findings, and future directions.
2. Read `digest.md` (~10 min) for the compressed key points per section plus the argument in five moves.
3. Deep-dive the wiki pages in order for full detail, then test yourself with `questions.md` and check `critical_thinking.md` for claims-vs-evidence gaps.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem, original ideas, findings, future directions.
- [Digest](digest.md) — compressed key points per section plus the argument in five moves.
- [Explainer](explainer.md) — plain-language walkthrough of the Hold/Shift problem, data pipeline, model, and results.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, applicability, verdict (trial).
- [Questions](questions.md) — retrieval practice (Q1–Q9) covering all six wiki pages.

## Wiki

| Page | Covers |
|---|---|
| [01-overview-and-problem](wiki/01-overview-and-problem.md) | Title block + abstract opening fragment (up to "while still maintaining") |
| [02-background-and-data-pipeline](wiki/02-background-and-data-pipeline.md) | Motivation, prior limits, VAD 50 Hz future-window labeling with 3-scheme agreement, 10-s context, dataset generation |
| [03-architecture-dual-encoder-and-fusion](wiki/03-architecture-dual-encoder-and-fusion.md) | Dual frozen encoders, cross-attention fusion, ALiBi Transformer, temporal pooling, sigmoid classification head |
| [04-experiments-slm-and-audio-baselines](wiki/04-experiments-slm-and-audio-baselines.md) | Experimental setups, Mandarin Easy-Turn SLM comparison (Table 1), audio-only Tables 2–3 spillover |
| [05-llm-comparison-and-ablations](wiki/05-llm-comparison-and-ablations.md) | LLM comparison on in-house benchmark (Table 4) and component ablations (Sense, CPC, CrossATT, ATTPooling) |
| [06-analysis-and-conclusion](wiki/06-analysis-and-conclusion.md) | Abstract-tail claims, references [1]–[25], no new methods or numbers |

## Original Source

- Upstream: [https://arxiv.org/abs/2603.26515](https://arxiv.org/abs/2603.26515)
- Local copy: [source/source.md](source/source.md)
