---
type: index
title: index-tts/index-tts
description: Folder index for IndexTTS zero-shot voice cloning — one-clip multilingual TTS with emotion, speed, and pronunciation control.
generated:
  by: claude/opencode-go/muse-spark-1.3-contributor
  at: "2026-09-22T15:06:55Z"
sources:
  - id: original
    resource: https://github.com/index-tts/index-tts
  - id: local-copy
    resource: source/source.md
tags: [text-to-speech, voice-cloning, multilingual, emotion-control]
---

# index-tts/index-tts

IndexTTS is a zero-shot text-to-speech system that clones a voice from a single reference clip. The current IndexTTS-2.5 line adds five-language synthesis with disentangled timbre–emotion control, speed and pronunciation knobs, and WebUI, Python API, and vLLM serving paths.

## How to work through this

1. Start with `summary.md` (~2 min) for the TL;DR, architecture, conditioning, and gotchas.
2. Read `digest.md` (~10 min) for verbatim per-page key points plus the system in five moves.
3. Go deep in `wiki/` pages for commands, API signatures, and file details; use `explainer.md` for plain language, `critical_thinking.md` for claims-vs-evidence, and `questions.md` for retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR, architecture, conditioning, pipeline, files, usage.
- [Digest](digest.md) — verbatim key points per wiki page plus five-move argument.
- [Explainer](explainer.md) — plain-language walkthrough with jargon decoder.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, blind spots, verdict.
- [Questions](questions.md) — retrieval practice with answers per wiki page.

## Wiki

| Page | Covers |
|------|--------|
| [01-overview](wiki/01-overview.md) | README: model zoo, releases, install, WebUI/vLLM/Python API usage, emotion controls |
| [02-top-level-files](wiki/02-top-level-files.md) | webui.py startup and checkpoint resolution plus root env, packaging, and legal files |

## Original Source

- Upstream: [https://github.com/index-tts/index-tts](https://github.com/index-tts/index-tts)
- Local copy: [source/source.md](source/source.md)
