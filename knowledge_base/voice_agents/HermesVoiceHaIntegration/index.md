---
type: index
title: rusty4444/hermes-voice-ha-integration
description: Folder index for the hermes-voice-ha-integration bundle (v0.0.14): HA custom integration plus Hermes HA and voice-stack plugins with a guarded bidirectional bridge.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T15:04:19Z
sources:
  - id: original
    resource: https://github.com/rusty4444/hermes-voice-ha-integration
  - id: local-copy
    resource: source/source.md
tags: [home-assistant, hermes-agent, voice-stack, local-llm]
---

# rusty4444/hermes-voice-ha-integration

This folder documents the `hermes-voice-ha-integration` bundle (v0.0.14) that connects Hermes Agent to Home Assistant for natural-language state queries, guarded service calls, and an optional wake-word → STT → LLM → TTS voice loop. It is a safety-gated glue project — read-only verification first, guarded writes second — where fully local operation requires deliberately choosing local models and engines. Start with the summary, then the digest, then the wiki pages in order.

## How to work through this (summary ~2 min → digest ~10 min → wiki pages)

1. Read `summary.md` (~2 min) for the TL;DR, problem, architecture, and limits.
2. Read `digest.md` (~10 min) for the verbatim per-page key points plus the system in five moves.
3. Read the wiki pages in order (`01` → `02`) for full detail, then `explainer.md` for plain language, `critical_thinking.md` for claims-vs-evidence, and `questions.md` for retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem, architecture, tool tables, setup, and limits.
- [Digest](digest.md) — verbatim per-page condensations plus the system in five moves.
- [Explainer](explainer.md) — plain-language walkthrough: what it is, why it matters, how it works.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, verdict.
- [Questions](questions.md) — 7 retrieval prompts with answers covering all wiki pages.

## Wiki

| Page | Covers |
|---|---|
| [01-overview](wiki/01-overview.md) | README repo overview: bundle pieces, install matrix, v0.0.14 note, capabilities, architecture and HA/voice tools, prerequisites and Steps 1–4 |
| [02-top-level-files](wiki/02-top-level-files.md) | Top-level packaging files: `.gitignore`, `hacs.json`, `MANIFEST.in` |

## Original Source

- Upstream: [rusty4444/hermes-voice-ha-integration](https://github.com/rusty4444/hermes-voice-ha-integration)
- Local copy: [source/source.md](source/source.md)
