---
type: index
title: Talkio
description: Folder index for Talkio — zero-infrastructure TypeScript voice-AI orchestration with six XState actors, dual-path interruption, sentence-level streaming TTS, and BYO providers.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T14:49:31Z
sources:
  - id: original
    resource: https://github.com/abdufelsayed/talkio
  - id: local-copy
    resource: source/source.md
tags: [voice-ai, orchestration, typescript, turn-taking, xstate]
---

# Talkio

Talkio ("TAWK-yo") is a TypeScript-first, provider- and infrastructure-agnostic voice-AI orchestration library: you bring STT, LLM, and TTS providers, it coordinates turn-taking, interruptions, cancellation, and streaming through six parallel XState actors, and you consume a typed event stream. This folder holds a 2-minute summary, a 10-minute digest, plain-language and critical companions, retrieval questions, and three wiki pages covering the core library, orchestration-library comparisons, and the no-built-in-LLM design. Start with the summary, then go deeper only where needed.

## How to work through this (summary ~2 min → digest ~10 min → wiki pages)

1. Read `summary.md` (~2 min) for the TL;DR, problem/motivation, main ideas, findings, and future directions.
2. Read `digest.md` (~10 min) for the one-sentence takeaways, verbatim key points, and the argument in five moves.
3. Deep-dive the wiki pages in order, then `explainer.md` for plain language, `critical_thinking.md` for claims-vs-evidence, and `questions.md` for retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem/motivation, main ideas, findings, future directions.
- [Digest](digest.md) — one-sentence takeaways, verbatim key points, argument in five moves.
- [Explainer](explainer.md) — plain-language walkthrough of what Talkio is and how it works.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, verdict.
- [Questions](questions.md) — retrieval practice Q1–Q7 with answers linked to wiki pages.

## Wiki

| Page | Covers |
|------|--------|
| [Talkio](wiki/01-talkio.md) | Talkio overview: voice-AI orchestration, architecture, and core features |
| [Orchestration Libraries](wiki/02-orchestration-libraries.md) | Comparison of orchestration libraries and when to use each, plus managed platforms, deployment, design philosophy, and custom providers |
| [Why no built-in LLM](wiki/03-why-no-built-in-llm.md) | Why no built-in LLM (`LLMFunction` interface), why XState, why separate provider packages, streaming example, context API, custom providers |

## Original Source

- Upstream: <https://github.com/abdufelsayed/talkio>
- Local copy: [source/source.md](source/source.md)
