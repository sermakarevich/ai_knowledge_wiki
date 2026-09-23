---
type: index
title: soniqo/speech-core
description: Folder index for the soniqo/speech-core snapshot (v0.0.11): on-device C++17 speech stack with VAD, batch/streaming STT, diarization, TTS, and a voice-agent pipeline.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T17:38:33Z
sources:
  - id: original
    resource: https://github.com/soniqo/speech-core
  - id: local-copy
    resource: source/source.md
tags: [on-device-speech, streaming-stt, voice-agent-pipeline, edge-tts]
---

# soniqo/speech-core

This folder captures the `soniqo/speech-core` repository at v0.0.11: on-device C++17 speech infrastructure covering voice activity detection, batch and streaming speech-to-text, speaker diarization, text-to-speech, and the voice-agent pipeline connecting them. The core is a small model-agnostic orchestration layer (turn detection, interruption, audio utils, conversation state, tool calls) with optional ONNX Runtime and LiteRT backends. Start with the summary for the two-minute picture, use the digest for verbatim evidence, then go deeper with the wiki pages, explainer, critical analysis, and retrieval questions.

## How to work through this (summary ~2 min → digest ~10 min → wiki pages)

1. Read `summary.md` (~2 min) for the TL;DR, motivation, key findings, and future directions.
2. Read `digest.md` (~10 min) for verbatim-copied evidence lines behind each claim, including the five-move argument.
3. Open the wiki pages for full per-section detail, then `explainer.md` for the plain-language walkthrough.
4. Read `critical_thinking.md` for claims-vs-evidence analysis and the verdict, then self-test with `questions.md`.

## Read This Folder

- [Summary](summary.md) — TL;DR, motivation, findings, and future directions.
- [Digest](digest.md) — verbatim evidence lines and the argument in five moves.
- [Explainer](explainer.md) — plain-language walkthrough with jargon decoder.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, weaknesses, verdict.
- [Questions](questions.md) — 7 retrieval-practice questions with answers.

## Wiki

| Page | Covers |
|---|---|
| [01-overview](wiki/01-overview.md) | README.md: repo overview, model/backend tables, quick-start snippets, CLI packages, architecture diagram. |
| [02-top-level-files](wiki/02-top-level-files.md) | Build and contributor contract: CMakeLists.txt targets and option guards, AGENTS.md/CLAUDE.md/CODEX.md, multilingual READMEs, .gitattributes/.gitignore hygiene, THIRD-PARTY-NOTICES.md. |

## Original Source

- Upstream: [https://github.com/soniqo/speech-core](https://github.com/soniqo/speech-core)
- Local copy: [source/source.md](source/source.md)
