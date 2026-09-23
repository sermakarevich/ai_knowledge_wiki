---
type: index
title: nari-labs/nari-qwen3-tts
description: Folder index for the Nari Qwen3-TTS serving snapshot — single-H100 Qwen3-TTS 1.7B CustomVoice server with sub-50 ms p95 TTFA at 10 RPS, ttfa/balanced/throughput profiles, and OpenAI-shaped HTTP plus WebSocket streaming.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T17:06:19Z
sources:
  - id: original
    resource: https://github.com/nari-labs/nari-qwen3-tts
  - id: local-copy
    resource: source/source.md
tags: [text-to-speech, tts-serving, low-latency, cuda-graphs]
filed_via: jev choose, category: models, confidence: 0.77
---
# nari-labs/nari-qwen3-tts

Nari Qwen3-TTS is a latency-tuned serving stack for Qwen3-TTS 1.7B CustomVoice that claims sub-50 ms p95 time-to-first-audio at 10 RPS on a single NVIDIA H100. This folder holds a summary, a verbatim digest, a plain-language explainer, a critical analysis, retrieval questions, and two wiki pages covering the README serving surface and the top-level runtime files.

## How to work through this

- Summary (~2 min): read `summary.md` for the problem space, architecture, profiles, and operational gotchas.
- Digest (~10 min): read `digest.md` for the verbatim one-sentence theses, key points, and the five-move system narrative.
- Wiki pages: read `wiki/01-overview.md` then `wiki/02-top-level-files.md` for the full evidence tables (performance claims, run targets, profiles/config, API surface, compose runtime).

## Read This Folder

- [Summary](summary.md)
- [Digest](digest.md)
- [Explainer (plain language)](explainer.md)
- [Critical thinking](critical_thinking.md)
- [Retrieval questions](questions.md)

## Wiki

| Page | Covers |
|---|---|
| [01-overview](wiki/01-overview.md) | README.md (project TL;DR, Docker/uv run targets, profiles, API surface) |
| [02-top-level-files](wiki/02-top-level-files.md) | `.dockerignore`, `.gitignore`, `.python-version`, `docker-compose.yaml` |

## Original Source

- Upstream: https://github.com/nari-labs/nari-qwen3-tts
- Local copy: `source/source.md`
