---
type: index
title: wavekat/wavekat-turn
description: Folder index for the wavekat-turn knowledge pack: offline Rust turn detection over Pipecat audio and LiveKit text backends with TurnController orchestration.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T17:54:09Z
sources:
  - id: original
    resource: https://github.com/wavekat/wavekat-turn
  - id: local-copy
    resource: source/source.md
tags: [rust, voice-ai, turn-detection, onnx]
---
# wavekat/wavekat-turn

`wavekat-turn` is an offline Rust turn-detection library for WaveKat voice pipelines that answers "are they done speaking?" It wraps Pipecat Smart Turn v3 audio, WaveKat language fine-tunes, and the LiveKit text backend behind unified traits with `TurnController` orchestration. Use this folder's summary, digest, and wiki pages for progressively deeper, source-cited detail.

## How to work through this

- Summary (~2 min): read `summary.md` for the problem, architecture, backends, and gotchas.
- Digest (~10 min): read `digest.md` for verbatim key points per wiki page plus the system in five moves.
- Wiki pages: read `wiki/01-overview.md` then `wiki/02-top-level-files.md` for full cited detail.
- Go deeper: `explainer.md` for plain-language background, `critical_thinking.md` for claims-vs-evidence review, `questions.md` for retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR, architecture, turn abstraction, pipeline, files, usage, and limitations.
- [Digest](digest.md) — verbatim key points per wiki page plus the five-move argument.
- [Explainer](explainer.md) — plain-language walkthrough: what turn detection is, how audio/text paths and TurnController work, where it is used.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, new vs. repackaged, weaknesses, applicability, verdict (trial).
- [Questions](questions.md) — retrieval prompts Q1–Q7 covering traits, controller, backends, flags, validation, and backend choice.

## Wiki

| Page | Covers |
| --- | --- |
| [Overview](wiki/01-overview.md) | README.md, examples/controller.rs, scripts/README.md |
| [Top-Level Files](wiki/02-top-level-files.md) | .gitignore, release-plz.toml |

## Original Source

- Upstream: [https://github.com/wavekat/wavekat-turn](https://github.com/wavekat/wavekat-turn)
- Local copy: [source/source.md](source/source.md)
