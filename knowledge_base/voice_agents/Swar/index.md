---
type: index
title: vivekananda-2201/Swar
description: Folder index for vivekananda-2201/Swar — offline CPU-first full-duplex voice runtime orchestrating Silero VAD, Parakeet TDT STT, and Kokoro TTS with barge-in, wake-word gating, and benchmark harness.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T17:40:57Z
sources:
  - id: original
    resource: https://github.com/vivekananda-2201/Swar
  - id: local-copy
    resource: source/source.md
tags: [voice-ai, full-duplex, cpu-inference, turn-taking, speech-pipeline]
---

# vivekananda-2201/Swar

Swar is a 100% offline, CPU-first full-duplex conversational audio runtime that orchestrates Silero VAD, NVIDIA Parakeet TDT STT, and Kokoro TTS into an interruptible voice loop with wake-word gating, reasoning-model filtering, and a speaker echo guard. This folder holds a 2-minute summary, a 10-minute digest, plain-language and critical companions, retrieval questions, and two wiki pages covering the runtime architecture and the repository root wiring. Start with the summary, then go deeper only where needed.

## How to work through this (summary ~2 min → digest ~10 min → wiki pages)

1. Read `summary.md` (~2 min) for the TL;DR, problem/motivation, architecture, dependencies, CLI surface, and limitations.
2. Read `digest.md` (~10 min) for the one-sentence takeaways, verbatim key points, and the system in five moves.
3. Deep-dive the wiki pages in order, then `explainer.md` for plain language, `critical_thinking.md` for claims-vs-evidence, and `questions.md` for retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem/motivation, architecture, loop, files, dependencies, CLI, limitations.
- [Digest](digest.md) — one-sentence takeaways, verbatim key points, system in five moves.
- [Explainer](explainer.md) — plain-language walkthrough of what Swar is and how it works.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, verdict.
- [Questions](questions.md) — retrieval practice Q1–Q7 with answers linked to wiki pages.

## Wiki

| Page | Covers |
|------|--------|
| [Overview](wiki/01-overview.md) | Swar runtime: full-duplex pipeline, highlights vs traditional pipelines, benchmarks, speaker echo guard |
| [top-level-files](wiki/02-top-level-files.md) | Repository root: run.py CLI, swar.py facade, config.yaml, requirements.txt, .gitignore |

## Original Source

- Upstream: <https://github.com/vivekananda-2201/Swar>
- Local copy: [source/source.md](source/source.md)
