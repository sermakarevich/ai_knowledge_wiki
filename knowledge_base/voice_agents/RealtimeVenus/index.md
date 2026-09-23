---
type: index
title: "Realtime-Venus: A full-duplex interaction system with asynchronous delegation"
description: "Folder index for the Realtime-Venus paper: orientation, reading order, folder contents, and wiki page map."
generated:
  by: claude/opencode-go/muse-spark-1.3-contributor
  at: 2026-09-22T11:57:00Z
sources:
  - id: original
    resource: https://arxiv.org/abs/2609.13814
  - id: local-copy
    resource: source/source.md
tags: [full-duplex-interaction, asynchronous-delegation, spoken-dialogue-systems, streaming-multimodal-models]
---

# Realtime-Venus: A full-duplex interaction system with asynchronous delegation

Realtime-Venus pairs two 9B conversational frontends (Omni for audio–visual, Audio for spoken interaction) with a dual-loop runtime where Realtime-Venus-Harness executes delegated tasks asynchronously while live interaction continues. This folder holds a 2-minute summary, a 10-minute digest of verbatim wiki key points, an explainer, a critical analysis, retrieval questions, and 14 wiki pages. Start with the summary, then the digest, then the wiki pages for full detail.

## How to work through this

1. Read `summary.md` (~2 min) for the TL;DR, problem, ideas, findings, and future directions.
2. Read `digest.md` (~10 min) for the verbatim key points of all 14 wiki pages plus the five-move argument.
3. Dive into `wiki/*.md` for per-section detail, then use `explainer.md` for plain-language intuition, `critical_thinking.md` for claims-vs-evidence analysis, and `questions.md` for retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem and motivation, ideas, findings, future directions.
- [Digest](digest.md) — verbatim key points from every wiki page plus the argument in five moves.
- [Explainer](explainer.md) — plain-language walkthrough of the system, why it matters, and how it works.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty judgment, weaknesses, applicability, verdict.
- [Questions](questions.md) — 15 retrieval questions with answers covering every wiki page.

## Wiki

| Page | Covers |
|---|---|
| [01-overview-full-duplex-system](wiki/01-overview-full-duplex-system.md) | System overview: two 9B frontends, dual-loop runtime, post-training recipe, headline video/audio/duplex results |
| [02-benchmark-figures](wiki/02-benchmark-figures.md) | Garbled benchmark-figure OCR: surviving name/label/number fragments only, no recoverable claim |
| [03-offline-benchmarks](wiki/03-offline-benchmarks.md) | Figure 1/2 captions plus Figure 2 full-duplex score tables across four overlap scenarios |
| [04-introduction](wiki/04-introduction.md) | Introduction: timescale mismatch, two frontends, harness with evidence snapshots and playback-aware delivery |
| [05-related-work](wiki/05-related-work.md) | Related work: GPT-Realtime async function calling, VoiceChat tool channel, private delegation interface |
| [06-system-overview-runtime](wiki/06-system-overview-runtime.md) | Unified per-second runtime transition, Thinker–Talker stack, in-stream delegation, Omni long-video memory |
| [07-interaction-control-states](wiki/07-interaction-control-states.md) | Chunk serialization, listen/speak/turn-end control, playback-aware scheduling, role-conditioned overlap handling |
| [08-training-recipe](wiki/08-training-recipe.md) | Unified post-training pass: sparse response-only supervision, per-sample normalization, Thinker-only updates |
| [09-data-pipeline](wiki/09-data-pipeline.md) | Three-stage data construction: scenario planning, acoustic realization, temporal alignment; corpus scale |
| [10-delegation-evaluation](wiki/10-delegation-evaluation.md) | Duplex/delegation target taxonomy, retain/cancel/revise supervision, evaluation settings |
| [11-understanding-evaluation](wiki/11-understanding-evaluation.md) | Video/audio understanding, spoken QA, memory gains, and overlap-handling results |
| [12-full-duplex-evaluation](wiki/12-full-duplex-evaluation.md) | Interruption–continuation trade-off, FDB-v3 tool use, internal delegate-benchmark routing gaps |
| [13-references-a-m](wiki/13-references-a-m.md) | References A–M: omni models, duplex systems, speech foundations, benchmarks, industry systems |
| [14-references-n-z-appendix](wiki/14-references-n-z-appendix.md) | References N–Z, contribution credits, and Appendix B unit-level training examples |

## Original Source

- arXiv: [Realtime-Venus: A full-duplex interaction system with asynchronous delegation](https://arxiv.org/abs/2609.13814)
- Local copy: [source/source.md](source/source.md)
