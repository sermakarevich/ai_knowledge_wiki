---
type: index
title: QuentinFuxa/WhisperLiveKit
description: Folder index for the WhisperLiveKit knowledge pack: self-hosted real-time streaming transcription and translation with a multi-backend server, wlk CLI, and WebSocket plus OpenAI-compatible API.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T17:55:47Z
sources:
  - id: original
    resource: https://github.com/QuentinFuxa/WhisperLiveKit
  - id: local-copy
    resource: source/source.md
tags: [streaming-asr, simultaneous-translation, speaker-diarization, self-hosted]
---

# QuentinFuxa/WhisperLiveKit

WhisperLiveKit is a self-hosted real-time speech-transcription/translation kit that wraps Whisper-family and alternative backends in simultaneous-speech commit policies. This folder holds a 2-minute summary, a 10-minute digest of verbatim key points, a plain-language explainer, a critical analysis, retrieval questions, and two wiki deep-dives. Start with the summary, then use the digest and wiki pages for backend, deployment, and configuration detail.

## How to work through this (summary ~2 min → digest ~10 min → wiki pages)

1. Read `summary.md` (~2 min) for the TL;DR, architecture, pipeline, and usage surface.
2. Read `digest.md` (~10 min) for the verbatim key points per wiki page plus the five-move argument.
3. Skim `explainer.md` for the plain-language version and `critical_thinking.md` for claims-vs-evidence scrutiny.
4. Deep-dive the `wiki/` pages in order, then self-test with `questions.md`.

## Read This Folder

- [Summary](summary.md) — TL;DR, architecture, pipeline, key files, dependencies, CLI surface.
- [Digest](digest.md) — verbatim key points per wiki page + five-move argument.
- [Explainer](explainer.md) — plain-language walkthrough.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, new vs. repackaged, limits.
- [Questions](questions.md) — retrieval practice (Q1–Q7 covering all wiki pages).

## Wiki

| Page | Covers |
|---|---|
| [01-overview](wiki/01-overview.md) | Repo overview grounded in README-level install/usage/architecture material and the files it names: `pyproject.toml` (`[tool.uv].conflicts`, extras), `docs/API.md`, `docs/troubleshooting.md`, `whisperlivekit/whisper/tokenizer.py`, `diff_protocol.py`, `BENCHMARK.md`, `benchmarks/h100_scatter/`, `scripts/run_scatter_benchmark.py`, `macos/WhisperLiveKitMac`, `chrome-extension/` |
| [02-top-level-files](wiki/02-top-level-files.md) | `.dockerignore`, `.gitignore`, `.gitmodules`, `CHANGES.md`, `CITATION.cff`, `CLAUDE.md`, `compose.yml`, `DEV_NOTES.md`, `Dockerfile.cpu`, `JARVISLAB_AGENTS.md`, `MANIFEST.in`, `SECURITY.md` |

## Original Source

- Upstream: [https://github.com/QuentinFuxa/WhisperLiveKit](https://github.com/QuentinFuxa/WhisperLiveKit)
- Local copy: [source/source.md](source/source.md)
