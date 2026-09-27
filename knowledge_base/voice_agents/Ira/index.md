---
type: index
title: vedantnimbarte/IRA
description: Index for the IRA interruptible voice-assistant folder: single-process
  voice loop with barge-in, spoken confirmation-gated tools, and repo hygiene.
generated:
  by: claude/muse-spark-1.3-contributor
  at: '2026-09-22T15:13:07Z'
sources:
- id: original
  resource: https://github.com/vedantnimbarte/IRA
- id: local-copy
  resource: source/source.md
tags:
- voice-assistant
- rust
- turn-taking
- mcp
---
# vedantnimbarte/IRA

IRA is a single-process desktop voice assistant in Rust whose headline feature is interruptible turn-taking: wake word, VAD endpointing, streaming speech-to-text, streaming model replies, and duck-then-cut barge-in. State-changing tool calls pass a spoken yes-only confirmation gate, and the screen and orb render the same live event stream.

## How to work through this (summary ~2 min → digest ~10 min → wiki pages)

1. Start with `summary.md` (~2 min) for the TL;DR, turn state machine, and key findings.
2. Read `digest.md` (~10 min) for the per-wiki-page key points plus the system in five moves.
3. Go deep with the wiki pages in order, then `explainer.md` for plain language, `critical_thinking.md` for claims vs. evidence, and `questions.md` for retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem and motivation, architecture, key findings.
- [Digest](digest.md) — per-wiki-page key points plus the system in five moves.
- [Explainer](explainer.md) — plain-language walkthrough of the voice loop and tooling.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, verdict.
- [Questions](questions.md) — retrieval practice with answers (Q1–Q7).

## Wiki

| Page | Covers |
|---|---|
| [Overview](wiki/01-overview.md) | Interruptible voice loop: install/first start, turn state machine, tool registry with confirmation gate, HTTP surface, Wingman |
| [Top-level files](wiki/02-top-level-files.md) | Repo hygiene and Windows packaging: `.gitattributes`, `.gitignore`, `build.rs` icon embedding |

## Original Source

- Upstream: [https://github.com/vedantnimbarte/IRA](https://github.com/vedantnimbarte/IRA)
- Local copy: [source/source.md](source/source.md)
