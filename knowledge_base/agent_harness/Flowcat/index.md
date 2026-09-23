---
type: index
title: AreevAI/flowcat
description: Folder index for AreevAI/flowcat — self-hosted native-Rust voice-agent runtime with pipecat-compatible pipeline, ContextRelay memory, and single-process call density.
generated:
  by: claude/muse-spark-1.3-contributor
  at: '2026-09-22T14:49:57Z'
sources:
  - id: original
    resource: https://github.com/AreevAI/flowcat
  - id: local-copy
    resource: source/source.md
tags: [voice-agents, rust, self-hosted, realtime-audio]
---

# AreevAI/flowcat

Flowcat is a self-hosted, native-Rust runtime for real-time voice agents, shipped as one static binary you run in your own VPC or fully air-gapped. It mirrors pipecat's `FrameProcessor` pipeline model with cascaded STT → LLM → TTS or single speech-to-speech shapes, ContextRelay text-reseed memory, and flat sub-millisecond framework overhead to 2,000 concurrent calls. This folder holds a TL;DR summary, a verbatim digest of the wiki pages, a plain-language explainer, a critical analysis, retrieval questions, and two wiki detail pages.

## How to work through this

1. **Summary (~2 min)** — read `summary.md` for the TL;DR: problem, architecture, pipeline, providers, call path, and gotchas.
2. **Digest (~10 min)** — read `digest.md` for per-wiki-page key points (verbatim copies) plus the argument in five moves.
3. **Wiki pages** — read the two pages in `wiki/` in order for full detail, then use `explainer.md`, `critical_thinking.md`, and `questions.md` to check understanding.

## Read This Folder

- [Summary](summary.md) — human-readable TL;DR, problem and motivation, architecture, findings, directions.
- [Digest](digest.md) — per-wiki-page key points plus the argument in five moves.
- [Explainer](explainer.md) — plain-language walkthrough: what it is, why it matters, how it works, where to use it.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, applicability, verdict.
- [Questions](questions.md) — retrieval practice with answers (Q1–Q7).

## Wiki

| Page | Covers |
|---|---|
| [01-overview](wiki/01-overview.md) | README overview, why-Flowcat, benchmark/capacity, and usage/demos; referenced bench/, deploy/, flowcat-server config, FEATURES, PROCESSOR-DESIGN |
| [02-top-level-files](wiki/02-top-level-files.md) | Repo root files: workspace layout, build/test rules, DESIGN/PROCESSOR-DESIGN/SIP-DESIGN, feature-flag matrix, provider map, quickstart/roadmap/security/spinout/notice |

## Original Source

- Upstream: [https://github.com/AreevAI/flowcat](https://github.com/AreevAI/flowcat)
- Local copy: [source/source.md](source/source.md)
