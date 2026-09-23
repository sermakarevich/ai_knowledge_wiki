---
type: index
title: vishnu97770/Real-Time-Voice-Agent
description: Folder index for the Real-Time-Voice-Agent knowledge pack: summary, digest, explainer, critical analysis, retrieval questions, and wiki pages.
generated:
  by: claude/opencode-go/muse-spark-1.3-contributor
  at: 2026-09-22T17:28:32Z
sources:
  - id: original
    resource: https://github.com/vishnu97770/Real-Time-Voice-Agent
  - id: local-copy
    resource: source/source.md
tags: [real-time-voice, llm-agents, speech-recognition, guardrails]
---

# vishnu97770/Real-Time-Voice-Agent

This folder holds a knowledge pack for a profile-driven real-time voice agent: one fixed streaming runtime (VAD → streaming ASR → tool-grounded LLM → streaming TTS) configured per call by swappable Agent Profiles. It covers the real-time loop, grounding and consent guardrails, the outbound call-job / call-result contract, and the design-plus-prototype status with its backend dependency manifest.

## How to work through this

1. Read `summary.md` (~2 min) for the TL;DR, architecture, and findings.
2. Read `digest.md` (~10 min) for the verbatim key points and the system in five moves.
3. Go deep with the wiki pages in order, then `explainer.md`, `critical_thinking.md`, and `questions.md` for self-testing.

## Read This Folder

- [Summary](summary.md) — TL;DR, architecture, runtime–profile split, findings.
- [Digest](digest.md) — verbatim key points and five-move argument.
- [Explainer](explainer.md) — plain-language walkthrough.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, strengths, blind spots.
- [Questions](questions.md) — retrieval practice (Q1–Q7).

## Wiki

| Page | Covers |
|------|--------|
| [01-overview](wiki/01-overview.md) | README pitch, Core Idea, How It Works loop, verticals table, repo-contents table, tech stack, status, conclusion; incoming-side technology table and frontend/backend run notes |
| [02-top-level-files](wiki/02-top-level-files.md) | requirements.txt |

## Original Source

- GitHub: [vishnu97770/Real-Time-Voice-Agent](https://github.com/vishnu97770/Real-Time-Voice-Agent)
- Local copy: [source/source.md](source/source.md)
