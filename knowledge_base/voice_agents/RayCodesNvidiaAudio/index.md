---
type: index
title: 47thtechcorner/RayCodes_Nvidia_Audio
description: Folder index for the RayCodes_Nvidia_Audio demo snapshot — NVIDIA NemotronLabs VoiceChat 11B full-duplex speech wrapper with native in-stream tool calling.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T17:28:24Z
sources:
  - id: original
    resource: https://github.com/47thtechcorner/RayCodes_Nvidia_Audio
  - id: local-copy
    resource: source/source.md
tags: [full-duplex-speech, voice-ai, nvidia-nemotron, tool-calling]
---

# 47thtechcorner/RayCodes_Nvidia_Audio

This folder captures the `47thtechcorner/RayCodes_Nvidia_Audio` repo as a minimal runnable demo over NVIDIA's NemotronLabs VoiceChat 11B end-to-end full-duplex speech model. The core is a two-turn speech-to-speech pipeline (`main.py` + `voicechat_agent.py`) with a strict `<TOOLCALL>` tag protocol for live tool use. Start with the summary for headline claims, then the digest and wiki pages for verbatim metrics, protocol detail, and file-level behavior.

## How to work through this (summary ~2 min → digest ~10 min → wiki pages)

1. Read `summary.md` (~2 min) for the TL;DR, problem space, architecture, demo pipeline, and limitations.
2. Read `digest.md` (~10 min) for the verbatim key points per wiki page plus the system in five moves.
3. Deep-dive the wiki pages in table order, then `explainer.md` for plain language, `critical_thinking.md` for claims-vs-evidence, and `questions.md` for retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR, architecture, spoken-turn protocol, demo pipeline, dependencies, limitations.
- [Digest](digest.md) — verbatim key points per wiki page plus the system in five moves.
- [Explainer](explainer.md) — plain-language walkthrough with jargon decoder.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, weaknesses, verdict.
- [Questions](questions.md) — retrieval practice Q1–Q7 with answers.

## Wiki

| Page | Covers |
|------|--------|
| [01-overview](wiki/01-overview.md) | README.md (project overview, metrics, architecture, infrastructure, tool-call protocol, code layout, quick start, use cases, roadmap, resources) |
| [02-top-level-files](wiki/02-top-level-files.md) | `.gitignore`, `main.py`, `voicechat_agent.py` |

## Original Source

- Upstream: <https://github.com/47thtechcorner/RayCodes_Nvidia_Audio>
- Local copy: [source/source.md](source/source.md)
