---
type: index
title: rohitg00/agentmemory
description: Folder index for rohitg00/agentmemory — persistent local-first memory server for coding agents (iii-engine, MCP/hooks/REST, keyless BM25).
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-26T14:22:59Z
sources:
  - id: original
    resource: https://github.com/rohitg00/agentmemory
  - id: local-copy
    resource: source/source.md
tags: [agent-memory, mcp, coding-assistants, local-first, hybrid-search]
---

# rohitg00/agentmemory

agentmemory is a persistent, local-first memory server that lets coding agents share observations across sessions via hooks, MCP, or REST. It runs keyless by default (BM25 recall, no external databases) on a pinned iii-engine, with opt-in local or provider-backed embeddings and LLM compression.

## How to work through this

1. Start with [summary](summary.md) (~2 min) for the full technical picture: architecture, pipeline, config, and gotchas.
2. Then read [digest](digest.md) (~10 min) for the compressed per-page brief plus the five-move system narrative.
3. Then go deep into the [wiki pages](#wiki) below, the [plain-language explainer](explainer.md), and test yourself with [questions](questions.md); finish with [critical thinking](critical_thinking.md) before trusting headline claims.

## Read This Folder

- [Summary](summary.md) — full technical analysis (overview, architecture, pipeline, files, deps, CLI, extensibility, gotchas).
- [Digest](digest.md) — per-page compressed brief and five-move system narrative.
- [Explainer](explainer.md) — plain-language guide: what it is, why it matters, how it works, where to use it.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, applicability verdict (trial solo-only).
- [Questions](questions.md) — 7 retrieval-practice Q&As covering both wiki pages.

## Wiki

| Page | Covers |
|---|---|
| [01](wiki/01-overview.md) | `README.md` (repo overview, install, runtime ports/state, agent-compatibility table as far as preserved in chunk) |
| [02](wiki/02-top-level-files.md) | `.env.example`, `.gitignore`, `AGENTS.md`, `DESIGN.md`, `GOVERNANCE.md`, `iii-config.docker.yaml`, `iii-config.yaml`, `INSTALL_FOR_AGENTS.md`, `MAINTAINERS.md`, `ROADMAP.md`, `SECURITY.md`, `tsconfig.json`, `tsdown.config.ts`, `vitest.config.ts` |

## Original Source

- Upstream repository: [rohitg00/agentmemory](https://github.com/rohitg00/agentmemory)
- Local copy: [source/source.md](source/source.md)
