---
type: index
title: TencentCloud/TencentDB-Agent-Memory
description: Folder index for the TencentDB Agent Memory shared team-memory system (Memory Hub + Proxy, L0-L3 memory, Skills, Wiki, CodeGraph).
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-26T14:02:03Z
sources:
  - id: original
    resource: https://github.com/TencentCloud/TencentDB-Agent-Memory
  - id: local-copy
    resource: source/source.md
tags: [agent-memory, team-knowledge, llm-proxy, code-graph]
---

# TencentCloud/TencentDB-Agent-Memory

TencentDB Agent Memory is a shared Memory Hub + Proxy stack that turns past conversations, documents, and code into reusable, versioned, permissioned team memory assets. Start with the summary for the thesis and architecture, use the digest for verbatim key points, then go deep in the two wiki pages for install/deploy details.

## How to work through this

1. Read [summary](summary.md) (~2 min) for the full technical overview: problem, architecture, assets, pipeline, ports, and gotchas.
2. Read [digest](digest.md) (~10 min) for the verbatim key-points distillation of both wiki pages plus the five-move narrative.
3. Go deep in the wiki pages in order ([01](wiki/01-overview.md) → [02](wiki/02-top-level-files.md)), using [explainer](explainer.md) for plain-language background, [critical_thinking](critical_thinking.md) for claims-vs-evidence, and [questions](questions.md) for retrieval practice.

## Read This Folder

- [summary](summary.md) — full technical analysis (overview, architecture, assets, pipeline, files, deps, CLI, extensibility, limitations, comparison).
- [digest](digest.md) — key-points distillation with one-sentence headers per wiki page plus the system-in-five-moves narrative.
- [explainer](explainer.md) — plain-language guide: what it is, why it matters, how it works, where to use it, jargon decoder.
- [critical_thinking](critical_thinking.md) — critical analysis: claims vs. evidence, novelty, weaknesses, applicability, verdict (trial).
- [questions](questions.md) — retrieval practice Q1–Q7 with answers pointing back to the wiki pages.

## Wiki

| Page | Covers |
|------|--------|
| [01-overview](wiki/01-overview.md) | README.md — project purpose, install, agent support, Chat Memory / Skill / Wiki / CodeGraph, Memory Hub panel, cold start, team play, RAG comparison |
| [02-top-level-files](wiki/02-top-level-files.md) | .gitignore, CONTRIBUTING_CN.md, INSTALL.md, INSTALL_CN.md, README.deployment.md, README.docker.md, README_CN.md, ROADMAP.md, ROADMAP_CN.md — install, deploy modes, plugins, contributions, roadmap |

## Original Source

- Upstream repository: [TencentCloud/TencentDB-Agent-Memory](https://github.com/TencentCloud/TencentDB-Agent-Memory)
- Local copy: [source/source.md](source/source.md)
