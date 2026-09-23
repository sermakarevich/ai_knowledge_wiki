---
type: index
title: "CodeVoice: AI-Powered Technical Interview Simulator"
description: "Index for the CodeVoice folder: a real-time voice-to-voice AI interview simulator (LiveKit + Pipecat + Django) with streaming STT-LLM-TTS pipeline."
generated:
  by: claude/muse-spark-1.3-contributor
  at: "2026-09-22T14:32:00Z"
sources:
  - id: original
    resource: https://github.com/Raihan2511/codevoice
  - id: local-copy
    resource: source/source.md
tags: [voice-ai, technical-interviews, livekit, pipecat, django]
---

# CodeVoice: AI-Powered Technical Interview Simulator

CodeVoice is a real-time voice-to-voice AI technical interview simulator that routes browser audio through a LiveKit server into a Pipecat pipeline (Deepgram STT/TTS plus a Krutrim-hosted LLM) backed by a Django control plane. This folder distills the repo into a short summary, a verbatim digest of the two wiki chunks, plain-language and critical readings, and retrieval questions. Start with the summary for the big picture, then use the digest and wiki pages for exact pipeline, orchestration, and data-model details.

## How to work through this

1. Read the **summary** (~2 min) for the TL;DR, problem and motivation, main ideas, and key findings.
2. Read the **digest** (~10 min) for verbatim per-chunk key points plus the argument in five moves.
3. Deep-dive the **wiki pages** in order for full detail, then use the explainer, critical thinking, and questions files to check understanding.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem/motivation, main ideas, key findings, future directions.
- [Digest](digest.md) — verbatim per-chunk condensations plus the argument in five moves.
- [Explainer](explainer.md) — plain-language walkthrough with jargon decoder.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, weaknesses, applicability, verdict.
- [Questions](questions.md) — retrieval practice (Q1–Q7) covering both wiki pages.

## Wiki

| Page | Covers |
|---|---|
| [CodeVoice: AI-Powered Technical Interview Simulator](wiki/01-codevoice-overview.md) | System architecture, interaction flow, turn detection, context management, pipeline, token system |
| [1. Simulation App (`src/apps/simulation/`)](wiki/02-simulation-app.md) | Simulation/interviews/users apps and config, setup steps, usage workflow, troubleshooting, roadmap, tech stack |

## Original Source

- GitHub: https://github.com/Raihan2511/codevoice
- Local copy: [source/source.md](source/source.md)
