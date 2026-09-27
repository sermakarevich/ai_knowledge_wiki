---
type: index
title: Project Aether
description: Folder index for Project Aether — a staged AETHER-1 to AETHER-11 validation of Mimi plus Qwen2.5-1.5B NF4 plus CPU Zipformer plus VAD barge-in plus NLMS AEC full-duplex voice running on a 6 GB RTX 3050 laptop.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T14:27:45Z
sources:
  - id: original
    resource: https://github.com/lucifer5051/Aether
  - id: local-copy
    resource: source/source.md
tags: [full-duplex, voice-AI, low-latency, echo-cancellation, edge-inference]
---

# Project Aether

Project Aether is an independent realtime full-duplex voice AI project that runs a complete streaming conversational stack entirely on a consumer RTX 3050 6 GB laptop GPU. Eleven validated research steps (AETHER-1 through AETHER-11) freeze each layer in turn — memory coexistence, Cooperative Yielding GPU scheduling, CPU Zipformer ASR, acoustic VAD barge-in, and linear NLMS AEC — ending in a Class A production-ready verdict within its operating envelope.

## How to work through this

1. Read `summary.md` (~2 min) for the TL;DR, problem and motivation, original ideas, key findings, and future directions.
2. Read `digest.md` (~10 min) for the compressed key points per section plus the argument in five moves.
3. Deep-dive the wiki pages in order for full detail, then test yourself with `questions.md` and check `critical_thinking.md` for claims-vs-evidence gaps.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem and motivation, original ideas, key findings, future directions.
- [Digest](digest.md) — compressed key points per section plus the argument in five moves.
- [Explainer](explainer.md) — plain-language walkthrough of the full-duplex pipeline, Cooperative Yielding, VAD barge-in, and AEC.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, applicability, verdict (watch).
- [Questions](questions.md) — retrieval practice (Q1–Q7) covering both wiki pages.

## Wiki

| Page | Covers |
|---|---|
| [01-project-aether](wiki/01-project-aether.md) | Project overview, target hardware, validated post-AETHER-11 architecture, AETHER-1 through AETHER-11 research loop, validated stack summary, benchmark scripts and artifacts |
| [02-research-reports](wiki/02-research-reports.md) | Research report index for AETHER-4 through AETHER-11 (ASR feasibility and benchmarks, latency optimization, VAD barge-in, echo analysis, AEC research and integration) |

## Original Source

- Upstream: [https://github.com/lucifer5051/Aether](https://github.com/lucifer5051/Aether)
- Local copy: [source/source.md](source/source.md)
