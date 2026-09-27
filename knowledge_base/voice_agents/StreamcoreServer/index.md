---
type: index
title: streamcoreai/streamcore-server
description: Folder index for streamcoreai/streamcore-server, a single Go binary owning the realtime voice media path over WHIP with streaming STT/LLM/TTS.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T17:41:15Z
sources:
  - id: original
    resource: https://github.com/streamcoreai/streamcore-server
  - id: local-copy
    resource: source/source.md
tags: [webrtc, voice-ai, go, realtime-audio]
---
# streamcoreai/streamcore-server

StreamCore is a single Go binary that owns the latency-sensitive realtime media path — WebRTC/WHIP transport, adaptive turn-taking, barge-in, and streaming STT → LLM → TTS — while agent intelligence stays outside via bring-your-own-agent options. This folder distills the repo into a quick summary, a verbatim digest, a plain-language explainer, a critical analysis, retrieval questions, and two evidence-grounded wiki pages. Start with the summary, then go deeper as needed.

## How to work through this

- Summary (~2 min): read `summary.md` for the overview, architecture, pipeline, usage surface, and gaps.
- Digest (~10 min): read `digest.md` for the verbatim one-sentence theses, key points, and the system in five moves.
- Wiki pages: read `wiki/01-overview.md` then `wiki/02-top-level-files.md` for full evidence tables, verbatim routes, config keys, and caveats.

## Read This Folder

- [[summary|Summary]]
- [[digest|Digest]]
- [[explainer|Explainer (plain language)]]
- [[critical_thinking|Critical thinking]]
- [[questions|Retrieval questions]]

## Wiki

| Page | Covers |
|---|---|
| [[wiki/01-overview\|01-overview]] | README-level repo overview: positioning, demo, quickstart, transport, turn-taking, streaming sessions, BYO-agent, docs/SDK index |
| [[wiki/02-top-level-files\|02-top-level-files]] | Root files: main.go boot/HTTP/auth/debug, config schema, tests, hygiene, dependency pins, Chinese README mirror, security policy |

## Original Source

- Upstream: https://github.com/streamcoreai/streamcore-server
- Local copy: `source/source.md`
