---
type: index
title: volcengine/OpenViking
description: Open-source context database for AI agents unifying knowledge, memory, and skills as a browsable viking:// filesystem
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-26T14:00:35Z
sources:
  - id: original
    resource: https://github.com/volcengine/OpenViking
  - id: local-copy
    resource: source/source.md
tags: [agents, context-database, memory, retrieval]
---
# volcengine/OpenViking

OpenViking is an open-source context database for AI agents that organizes knowledge, memory, and skills as one browsable virtual filesystem under `viking://` with layered summaries and scoped search. Agents navigate it with file operations (`ls`, `tree`, `find`, `grep`) and scan L0 abstracts and L1 overviews before opening full L2 content. This folder holds a 2-minute summary, a 10-minute digest, plain-language and critical takes, retrieval questions, and two wiki pages.

## How to work through this

1. Start with the [summary](summary.md) (~2 min) for the architecture, viking:// model, pipeline, and CLI surface.
2. Read the [digest](digest.md) (~10 min) for verbatim key points plus the system-in-five-moves narrative.
3. Go deep with the [wiki pages](wiki/01-overview.md) as needed, then check [explainer](explainer.md), [critical thinking](critical_thinking.md), and [questions](questions.md).

## Read This Folder

- [Summary](summary.md) — full technical analysis (overview, architecture, filesystem, pipeline, files, deps, CLI).
- [Digest](digest.md) — verbatim key points per wiki page plus the system in five moves.
- [Explainer](explainer.md) — plain-language guide: what it is, why it matters, how it works.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, weaknesses, applicability, verdict.
- [Questions](questions.md) — seven retrieval prompts with answers covering both wiki pages.

## Wiki

| Page | Covers |
|---|---|
| [01-overview](wiki/01-overview.md) | README.md (What is OpenViking, Why OpenViking, `viking://` layout, L0/L1/L2 tiers, benchmarks, quick start, `ov` CLI) |
| [02-top-level-files](wiki/02-top-level-files.md) | `.clang-format`, `.dockerignore`, `.gitattributes`, `.gitignore`, `.pr_agent.toml`, `Caddyfile`, `CONTRIBUTING_CN.md`, `CONTRIBUTING_JA.md`, `MANIFEST.in`, `README_CN.md`, `README_JA.md`, `RELEASE.md`, `RELEASE_CN.md`, `SECURITY.md` |

## Original Source

- Upstream: [https://github.com/volcengine/OpenViking](https://github.com/volcengine/OpenViking)
- Local copy: [source/source.md](source/source.md)
