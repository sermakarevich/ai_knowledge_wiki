---
type: Video
title: Find and Fix Latency Leaks in Real-time Voice Agents (Pipecat)
description: Latency debugging demo on a Pipecat voice-to-video agent — per-module timing isolates local Whisper STT (~2.48 s) and a one-line swap to Deepgram (~0.001 s TTFB) restores real-time feel.
generated: { by: claude/opencode-go/muse-spark-1.3-contributor, at: 2026-09-22T08:05:07Z }
sources:
  - id: original
    resource: https://www.youtube.com/watch?v=GUxNi4qmsYE
  - id: local-copy
    resource: source/source.md
tags: [voice-agents, latency, pipecat, speech-to-text]
---

# Find and Fix Latency Leaks in Real-time Voice Agents (Pipecat)

A live latency hunt on a Pipecat voice-to-video app: voice commands switch videos sluggishly until per-module timing pins the leak on local Whisper STT (~2.48 s), and a one-line plugin swap to remote Deepgram STT (~0.001 s TTFB) makes switching feel instant. Read this folder to learn the instrument-each-stage method and why production voice agents need permanent per-component latency monitoring.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole video, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole video, medium: headline and key points.
3. **Wiki pages below** (~5 min each) — one chunk, deep. Each opens with its headline and key points, so you can stop early.

_New to the field? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

## Read This Folder

- [[summary|Summary]] — rung 1: the whole video, shallow
- [[digest|Digest]] — rung 2: the whole video at medium depth; the file to re-read on review
- [[explainer|Plain-Language Explainer]] — no-jargon explanation, applications, conclusions
- [[critical_thinking|Critical Analysis]] — claims vs. evidence, applicability, what it changes, verdict
- [[questions|Retrieval Practice]] — self-test questions; **answer these from memory before re-reading anything**

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-latency-leaks-in-pipecat-voice-agents\|What Really Makes or Breaks a Voice App]] | Voice-to-video demo delay; Pipecat STT/LLM/video pipeline with per-module timing; local-Whisper (~2.48 s) bottleneck fixed by remote Deepgram STT (~0.001 s TTFB) |

## Original Source

- [Find and Fix Latency Leaks in Real-time Voice Agents (Pipecat)](https://www.youtube.com/watch?v=GUxNi4qmsYE) — original YouTube video
- [source/source.md](source/source.md) — local transcript copy
