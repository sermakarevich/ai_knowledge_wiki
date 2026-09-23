---
type: index
title: VoiceBlender/voiceblender
description: Folder index for VoiceBlender — Go SIP/WebRTC voice bridge with leg-and-room mixing, REST/VSI control, and TTS/STT/agent media layer.
generated:
  by: claude/muse-spark-1.3-contributor
  at: '2026-09-22T17:44:58Z'
sources:
  - id: original
    resource: https://github.com/VoiceBlender/voiceblender
  - id: local-copy
    resource: source/source.md
tags: [voice-ai, sip-webrtc, telephony, ai-agents]
---

# VoiceBlender/voiceblender

VoiceBlender is a Go service that bridges SIP and WebRTC voice calls with multi-party audio mixing, a REST API, and real-time webhooks. Every call endpoint is modeled as a leg composed into room mixers, with media/AI services (TTS, STT, agents, recording, playback) and event delivery over webhooks and the VSI stream. This folder holds the summary, digest, explainer, critical analysis, retrieval questions, and two wiki pages.

## How to work through this (summary ~2 min → digest ~10 min → wiki pages)

1. Read the [[summary|summary]] (~2 min) for the overview, architecture, call model, and gotchas.
2. Read the [[digest|digest]] (~10 min) for verbatim key points per wiki page plus the system in five moves.
3. Dive into the wiki pages for full endpoint tables, configuration, specs, and contributor workflow.
4. Use the [[explainer|plain-language explainer]] for intuition, [[critical_thinking|critical analysis]] for claims-vs-evidence judgment, and [[questions|retrieval practice]] to test yourself.

## Read This Folder

- [[summary|Summary]] — technical analysis: overview, architecture, leg-and-room model, pipeline, files, deps, CLI, extensibility, limitations.
- [[digest|Digest]] — verbatim key points per wiki page plus the system in five moves.
- [[explainer|Explainer]] — plain-language walkthrough (what/why/how, uses, jargon decoder).
- [[critical_thinking|Critical thinking]] — claims vs. evidence, novelty, weaknesses, applicability, verdict.
- [[questions|Questions]] — retrieval-practice questions with answers covering every wiki page.

## Wiki

| Page | Covers |
|---|---|
| [[wiki/01-overview\|Overview]] | README content (definition, features, quick start, configuration, links), API overview (auth, legs, rooms as captured), `CONFIGURATION.md`, `API.md`, `voiceblender.env.example`, `cmd/voiceblender`, `docker/docker-compose.cluster.yml` |
| [[wiki/02-top-level-files\|Top-level-files]] | `API.md`, `asyncapi.yaml`, `CLAUDE.md`, `CONFIGURATION.md`, `go.sum`, `openapi.yaml`, `TESTING.md`, `voiceblender.env.example` |

## Original Source

- Upstream: https://github.com/VoiceBlender/voiceblender
- Local copy: source/source.md
