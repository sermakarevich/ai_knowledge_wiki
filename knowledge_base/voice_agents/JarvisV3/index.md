---
type: index
title: CarverXx/jarvis-v3
description: Index for the CarverXx/jarvis-v3 local-first dual-brain voice assistant folder.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T15:17:03Z
sources:
  - id: original
    resource: https://github.com/CarverXx/jarvis-v3
  - id: local-copy
    resource: source/source.md
tags: [voice-assistant, local-llm, tool-calling-agent, speech-pipeline]
---

# CarverXx/jarvis-v3

CarverXx/jarvis-v3 is a local-first, always-on voice assistant that pairs a fast conversational Subconscious with a slower Hermes tool-calling executor on a single Linux box. This folder holds a short summary, a verbatim digest, two wiki detail pages, plus plain-language, critical, and retrieval-practice companions.

## How to work through this (summary ~2 min → digest ~10 min → wiki pages)

1. Read the summary (~2 min) for the problem, dual-brain idea, pipeline, and hardware trade-offs.
2. Read the digest (~10 min) for the verbatim per-page key points plus the system in five moves.
3. Work through the wiki pages in order for full detail, using the explainer for plain-language background, critical_thinking for claims-vs-evidence scrutiny, and questions.md for retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem and motivation, architecture, findings, and gotchas.
- [Digest](digest.md) — verbatim per-page key points plus the system in five moves.
- [Explainer](explainer.md) — plain-language walkthrough: what it is, why it matters, how it works, where it fits.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, applicability, verdict.
- [Questions](questions.md) — retrieval practice with answers linked back to wiki pages.

## Wiki

| Page | Covers |
|---|---|
| [01-overview](wiki/01-overview.md) | Dual-brain architecture, wake → ASR → Subconscious → Hermes → TTS pipeline, services, TUI dashboard, install and personalisation |
| [02-top-level-files](wiki/02-top-level-files.md) | Top-level guardrails and defaults: `.gitignore`, env-driven `config.py`, pinned `requirements.txt` |

## Original Source

- Original: https://github.com/CarverXx/jarvis-v3
- Local copy: [source/source.md](source/source.md)
