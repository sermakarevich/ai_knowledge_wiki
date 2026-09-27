---
type: index
title: swarmclawai/swarmvault
description: Local-first LLM wiki, knowledge graph builder, and RAG knowledge base that compiles docs, code, and transcripts into a markdown wiki plus queryable graph
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-26T13:58:40Z
sources:
  - id: original
    resource: https://github.com/swarmclawai/swarmvault
  - id: local-copy
    resource: source/source.md
tags: [knowledge-graph, rag, llm-wiki, agents]
---
# swarmclawai/swarmvault

SwarmVault is a local-first LLM Wiki, knowledge graph builder, and RAG knowledge base that turns docs, code, transcripts, notes, and URLs into a durable markdown wiki plus a local typed graph. It runs offline by default via `swarmvault quickstart`, with approval-gated compile, hybrid search, and agent integrations. This folder holds a 2-minute summary, a 10-minute digest, plain-language and critical takes, retrieval questions, and two wiki pages.

## How to work through this

1. Start with the [summary](summary.md) (~2 min) for the problem, architecture, pipeline, and CLI surface.
2. Read the [digest](digest.md) (~10 min) for verbatim key points plus the system-in-five-moves narrative.
3. Go deep with the [wiki pages](wiki/01-overview.md) as needed, then check [explainer](explainer.md), [critical thinking](critical_thinking.md), and [questions](questions.md).

## Read This Folder

- [Summary](summary.md) — full technical analysis (overview, architecture, graph, providers, pipeline, files, deps, CLI).
- [Digest](digest.md) — verbatim key points per wiki page plus the system in five moves.
- [Explainer](explainer.md) — plain-language guide: what it is, why it matters, how it works.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, weaknesses, applicability, verdict.
- [Questions](questions.md) — seven retrieval prompts with answers covering both wiki pages.

## Wiki

| Page | Covers |
|---|---|
| [01-overview](wiki/01-overview.md) | README.md (Try It, three-layer architecture, why SwarmVault, gist-to-production table, install, fast path, main loop, common commands) |
| [02-top-level-files](wiki/02-top-level-files.md) | `.dockerignore`, `.gitignore`, `.npmrc`, `biome.json`, `glama.json`, `lefthook.yml`, `manifest.json`, `pnpm-lock.yaml`, `pnpm-workspace.yaml`, `README.ja.md`, `README.zh-CN.md`, `SCALE.md`, `STABILITY.md`, `tsconfig.base.json` |

## Original Source

- Upstream: [https://github.com/swarmclawai/swarmvault](https://github.com/swarmclawai/swarmvault)
- Local copy: [source/source.md](source/source.md)
