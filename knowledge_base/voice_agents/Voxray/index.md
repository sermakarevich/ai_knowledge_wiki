---
type: index
title: Voxray-AI/Voxray
description: Folder index for Voxray-AI/Voxray, a config-driven Go server wiring STT → LLM → TTS into a low-latency voice pipeline over WebSocket/WebRTC.
generated:
  by: claude/muse-spark-1.3-contributor
  at: "2026-09-22T17:54:36Z"
sources:
  - id: original
    resource: https://github.com/Voxray-AI/Voxray
  - id: local-copy
    resource: source/source.md
tags: [voice-ai, go, webrtc, speech-to-text]
---

# Voxray-AI/Voxray

Voxray is a self-hostable, config-driven Go server that wires STT → LLM → TTS providers into a single low-latency streaming voice pipeline delivered over WebSocket or WebRTC, defined by one JSON file. This folder holds a 2-minute summary, a 10-minute digest of verbatim key points, plain-language and critical companions, and two wiki pages covering the project overview and the top-level runnable/API surface.

## How to work through this

1. Start with `summary.md` (~2 min) for the TL;DR, problem, main ideas, and findings.
2. Read `digest.md` (~10 min) for verbatim per-page key points plus the system in five moves.
3. Go deep in the `wiki/` pages for architecture, providers, configuration, API, and build/test details; use `explainer.md` for plain language, `critical_thinking.md` for claims-vs-evidence, and `questions.md` for retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR, motivation, ideas, findings, future directions.
- [Digest](digest.md) — verbatim key points per wiki page plus the system in five moves.
- [Explainer](explainer.md) — plain-language walkthrough with jargon decoder.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, blind spots, verdict.
- [Questions](questions.md) — retrieval practice with answers per wiki page.

## Wiki

| Page | Covers |
|------|--------|
| [01-overview](wiki/01-overview.md) | README.md (project overview, pipeline, features, architecture, providers, requirements/build, configuration, environment variables) |
| [02-top-level-files](wiki/02-top-level-files.md) | .gitignore, API_SERVER.md, config.example.json, go.sum, NOTICE, TESTING.md (runnable/documented surface; API_SERVER.md and go.sum partially truncated) |

## Original Source

- Upstream: [https://github.com/Voxray-AI/Voxray](https://github.com/Voxray-AI/Voxray)
- Local copy: [source/source.md](source/source.md)
