---
type: index
title: NevaMind-AI/memU
description: Folder index for NevaMind-AI/memU — lightweight agent-driven skill-wiki memory with record/inject sidecar binaries and an embedding-only service.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-26T14:26:42Z
sources:
  - id: original
    resource: https://github.com/NevaMind-AI/memU
  - id: local-copy
    resource: source/source.md
tags: [agent-memory, skills, embeddings, multi-agent]
---

# NevaMind-AI/memU

memU is a lightweight, agent-driven memory system that gives users a shared LLM wiki across sessions, agents, and devices. Each host agent runs memU as a sidecar binary binding a record seam (scheduled bridging task mines session logs into Markdown skills) and an inject seam (standing instruction retrieves skills before answering). Its core memory logic is about 500 lines and embedding-only — no LLM calls in the service.

## How to work through this

1. Start with [summary](summary.md) (~2 min) for the full technical picture: architecture, pipeline, config, and gotchas.
2. Then read [digest](digest.md) (~10 min) for the compressed per-page brief plus the five-move system narrative.
3. Then go deep into the [wiki pages](#wiki) below, the [plain-language explainer](explainer.md), and test yourself with [questions](questions.md); finish with [critical thinking](critical_thinking.md) before trusting headline claims.

## Read This Folder

- [Summary](summary.md) — full technical analysis (overview, architecture, pipeline, files, deps, CLI, extensibility, gotchas).
- [Digest](digest.md) — per-page compressed brief and five-move system narrative.
- [Explainer](explainer.md) — plain-language guide: what it is, why it matters, how it works, where to use it.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, applicability verdict (trial).
- [Questions](questions.md) — 7 retrieval-practice Q&As covering both wiki pages.

## Wiki

| Page | Covers |
|---|---|
| [01](wiki/01-overview.md) | `README.md` (memory-as-wiki model, install routes, agent support matrix, skill-extraction pipeline, host adapters, developer integration, CLI, configuration, storage backends) |
| [02](wiki/02-top-level-files.md) | `.gitignore`, `.pre-commit-config.yaml`, `.python-version`, `AGENTS.md`, `INSTALL-LATEST.md`, `MANIFEST.in`, `SKILL.md` |

## Original Source

- Upstream repository: [NevaMind-AI/memU](https://github.com/NevaMind-AI/memU)
- Local copy: [source/source.md](source/source.md)
