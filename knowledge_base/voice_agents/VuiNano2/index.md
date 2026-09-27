---
type: index
title: fluxions-ai/vui
description: Folder index for the fluxions-ai/vui snapshot — dialogue-conditioned Vui Nano TTS plus the real-time streaming voice assistant.
generated:
  by: claude/muse-spark-1.3-contributor
  at: "2026-09-22T17:53:23Z"
sources:
  - id: original
    resource: https://github.com/fluxions-ai/vui
  - id: local-copy
    resource: source/source.md
tags: [text-to-speech, conversational-ai, voice-assistant, real-time-audio]
---

# fluxions-ai/vui

Vui is a real-time streaming voice assistant built around Vui Nano, a 219M-active (305M total) dialogue-conditioned TTS model that generates each reply inside the conversation's audio and text context. The repo ships the model with a single-Python-server voice loop (ASR → LLM → TTS) over WebRTC/WebSocket, plus installer, Docker, pip, Gradio, and CPU build paths. This folder holds the summary, digest, plain-language explainer, critical analysis, practice questions, and wiki pages.

## How to work through this (summary ~2 min → digest ~10 min → wiki pages)

1. Read `summary.md` (~2 min) for the overview, architecture, model, loop, and gotchas.
2. Read `digest.md` (~10 min) for the five-move argument with verbatim key points per wiki page.
3. Skim `explainer.md` for the plain-language version, then `critical_thinking.md` for claims vs. evidence.
4. Deep-dive the `wiki/` pages in order, using `questions.md` for retrieval practice.

## Read This Folder

- [Summary](summary.md) — overview, architecture, Vui Nano model, streaming loop, key files, dependencies, usage, extensibility, limitations.
- [Digest](digest.md) — five-move argument with verbatim key points per wiki page.
- [Explainer](explainer.md) — plain-language walkthrough.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, weaknesses, verdict.
- [Questions](questions.md) — retrieval-practice Q&As covering every wiki page.

## Wiki

| Page | Covers |
|---|---|
| [01-overview](wiki/01-overview.md) | README project description, Vui Nano model, voice loop and assistant capabilities, install and distribution, docker-compose and native quick start |
| [02-top-level-files](wiki/02-top-level-files.md) | .gitignore, AGENTS.md, bootstrap.sh, demo.py, install.sh, sample_texts.json |

## Original Source

- Upstream: [https://github.com/fluxions-ai/vui](https://github.com/fluxions-ai/vui)
- Local copy: [source/source.md](source/source.md)
