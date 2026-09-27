---
type: index
title: smixs/agent-second-brain
description: Always-on Telegram-fronted second brain filing voice and text into a private Obsidian vault via one persistent Claude Code session.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-26T14:06:53Z
sources:
  - id: original
    resource: https://github.com/smixs/agent-second-brain
  - id: local-copy
    resource: source/source.md
tags: [second-brain, obsidian, telegram-bot, claude-code, memory-graph]
---
# smixs/agent-second-brain

Always-on Telegram second brain that turns voice and text into typed, linked knowledge in a self-hosted Obsidian vault. One long-lived interactive Claude Code session in tmux does the filing at a flat ~$25/mo, with the autograph graph providing typed cards, Ebbinghaus decay, and self-maintenance.

## How to work through this

Start with [summary](summary.md) (~2 min) for the full technical analysis, then read [digest](digest.md) (~10 min) for verbatim key points per wiki page plus the five-move system view, then go deep into the wiki pages in table order.

## Read This Folder

- [summary](summary.md) — full technical analysis (overview, architecture, autograph, pipeline, files, deps, CLI, extensibility, limits).
- [digest](digest.md) — per-page one-sentence verdicts plus verbatim key points and five-move synthesis.
- [explainer](explainer.md) — plain-language version: what it is, why it matters, how it works, where to use it.
- [critical_thinking](critical_thinking.md) — claims vs. evidence, new vs. repackaged, blind spots, applicability, verdict.
- [questions](questions.md) — retrieval practice (Q1–Q7) covering both wiki pages.

## Wiki

| Page | Covers |
|---|---|
| [01-overview](wiki/01-overview.md) | Product overview: motivation, interaction examples, philosophy, capabilities, autograph engine, architecture, cost, install/upgrade, vault layout |
| [02-top-level-files](wiki/02-top-level-files.md) | Repo root installer: `.env.example`, `.gitignore`, `bootstrap.sh`, `README.ru.md`, `setup.sh`, `upgrade.sh` |

## Original Source

- Upstream: [smixs/agent-second-brain](https://github.com/smixs/agent-second-brain)
- Local copy: [source/source.md](source/source.md)
