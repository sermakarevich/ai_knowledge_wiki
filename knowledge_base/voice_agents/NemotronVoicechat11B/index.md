---
type: Repo
title: Nikki1404/nemotron_voicechat_11B
description: Dockerized speech-to-speech wrapper around nvidia/NVIDIA-NemotronLabs-VoiceChat-11B exposing a native WebSocket endpoint plus an OpenAI-compatible HTTP namespace, with turn-based push-to-talk file and microphone modes over a PCM16 mono 24 kHz boundary.
generated: { by: claude/muse-spark-1.3-contributor, at: 2026-09-22T17:07:53Z }
sources:
  - id: original
    resource: https://github.com/Nikki1404/nemotron_voicechat_11B
  - id: local-copy
    resource: source/source.md
tags: [speech-to-speech, websocket-serving, fastapi, docker-deployment]
filed_via: ask_human (jev choose confidence 0.39 below 0.7 floor), category: models
---

# Nikki1404/nemotron_voicechat_11B

This folder indexes a deployment wrapper (not a new model) around NVIDIA's 11B end-to-end VoiceChat checkpoint, packaged as a GPU Docker server with WebSocket and OpenAI-compatible endpoints. File mode and microphone mode share the same speech-to-speech core over PCM16 mono 24 kHz audio, but the bundled client is turn-based push-to-talk rather than continuous full-duplex. Start with the summary for the shape of the system, then go deeper only where you need detail.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[summary](summary.md)** (~2 min) — the whole thing, shallow.
2. **[digest](digest.md)** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~5 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

_New to the field? Start with [the plain-language explainer](explainer.md) instead. Coming back after a break? Read [the digest](digest.md), then [self-test](questions.md) — do not re-read the wiki._

## Read This Folder

- [Summary](summary.md) — rung 1: the whole source, shallow
- [Digest](digest.md) — rung 2: the whole source at medium depth; the file to re-read on review
- [Plain-Language Explainer](explainer.md) — no-jargon explanation, applications, conclusions
- [Critical Analysis](critical_thinking.md) — claims vs. evidence, applicability, what it changes, verdict
- [Retrieval Practice](questions.md) — self-test questions; **answer these from memory before re-reading anything**

## Wiki

| Page | Covers |
|------|--------|
| [01-overview](wiki/01-overview.md) | README.md (project purpose, endpoints, mic/file flows, dependency/build/run layout, client and curl tests, audio format) |
| [02-top-level-files](wiki/02-top-level-files.md) | .dockerignore, client-requirements.txt, client.py, requirements.txt, server.py (visible portion only; truncated after health endpoint), update.py |

## Original Source

- [https://github.com/Nikki1404/nemotron_voicechat_11B](https://github.com/Nikki1404/nemotron_voicechat_11B) — original GitHub repository
- [source/source.md](source/source.md) — local copy of the source
