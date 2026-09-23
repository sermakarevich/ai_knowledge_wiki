---
type: index
title: priamjain/pipecat-livekit-turn
description: LiveKit Turn Detector v1 as a drop-in Pipecat turn analyzer for multilingual end-of-utterance detection.
generated:
  by: claude/opencode-go/muse-spark-1.3-contributor
  at: "2026-09-22T17:15:37Z"
sources:
  - id: original
    resource: https://github.com/priamjain/pipecat-livekit-turn
  - id: local-copy
    resource: source/source.md
tags: [turn-detection, pipecat, livekit, voice-agents]
filed_via: jev choose + ask_human fallback, category: agent_harness, confidence: 0.47
---

# priamjain/pipecat-livekit-turn

`pipecat-livekit-turn` wraps LiveKit Turn Detector v1 as `LiveKitTurnAnalyzerV1`, a drop-in Pipecat `BaseTurnAnalyzer` over LiveKit's cloud end-of-utterance gateway. Its headline claim is much higher end-of-turn accuracy than Pipecat's shipped SmartTurn analyzer outside English, at the cost of a cloud dependency. This folder holds a 2-minute summary, a 10-minute digest, plain-language and critical readings, retrieval questions, and per-topic wiki pages.

## How to work through this

1. Start with `summary.md` (~2 min) for the problem, architecture, and headline results.
2. Then read `digest.md` (~10 min) for verbatim per-page key points and the five-move argument.
3. Then go deep in the `wiki/` pages in order, using `explainer.md` for intuition, `critical_thinking.md` for scrutiny, and `questions.md` for retrieval practice.

## Read This Folder

- [Summary](summary.md)
- [Digest](digest.md)
- [Explainer](explainer.md)
- [Critical thinking](critical_thinking.md)
- [Questions](questions.md)

## Wiki

| Page | Covers |
| ---- | ------ |
| [01-overview](wiki/01-overview.md) | `README.md`, `examples/bot.py` (referenced runnable bot) |
| [02-top-level-files](wiki/02-top-level-files.md) | `.gitignore` |

## Original Source

- Upstream: [https://github.com/priamjain/pipecat-livekit-turn](https://github.com/priamjain/pipecat-livekit-turn)
- Local copy: [source/source.md](source/source.md)
