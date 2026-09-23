---
type: index
title: 'Fix AI Voice Interruptions with Semantic Turn Detection'
description: Folder index for the video lesson fixing VAD-only voice agents that interrupt at every pause with a ~20 ms semantic turn detector wired into the agent session.
generated:
  by: claude/opencode-go/muse-spark-1.3-contributor
  at: 2026-09-22T08:00:00Z
sources:
  - id: original
    resource: https://www.youtube.com/watch?v=XbrlOY4Z-Ow
  - id: local-copy
    resource: source/source.md
tags: [voice-ai, turn-detection, vad, livekit, conversational-agents]
---

# Fix AI Voice Interruptions with Semantic Turn Detection

This folder distills a video lesson on fixing voice agents that interrupt users at every mid-sentence pause. VAD-only endpointing mistakes any silence for the end of a turn, so the fix adds a lightweight multilingual semantic turn detector that waits for a complete thought at a cost of only ~20 ms. The result is a patient, natural agent that handles hesitations, interruptions, and topic switches gracefully.

## How to work through this

Start with the summary (~2 min) for the TL;DR, problem, and key findings, then read the digest (~10 min) for the one-sentence thesis, key points, and the argument in five moves. Go deeper with the wiki pages for the full component detail, then use the explainer for plain-language intuition, critical_thinking for claims-vs-evidence scrutiny, and questions for retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem and motivation, main ideas, key findings, and future directions.
- [Digest](digest.md) — one-sentence thesis, key points, and the argument in five moves.
- [Explainer](explainer.md) — plain-language walkthrough with jargon decoder and use cases.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, blind spots, and verdict.
- [Questions](questions.md) — seven retrieval-practice questions with answers.

## Wiki

| Page | Covers |
| ---- | ------ |
| [Semantic Turn Detection](wiki/01-semantic-turn-detection.md) | VAD pause-interruption problem and semantic turn detection fix with LiveKit multilingual model, best practices, and test scenarios |

## Original Source

- Video: [Fix AI Voice Interruptions with Semantic Turn Detection](https://www.youtube.com/watch?v=XbrlOY4Z-Ow)
- Local copy: [source/source.md](source/source.md)
