---
type: index
title: vectorize-io/hindsight
description: Folder index for the Hindsight agent-memory research set — summary, digest, explainer, critique, questions, and wiki pages.
generated:
  by: claude/opencode-go/muse-spark-1.3-contributor
  at: 2026-09-26T14:32:36Z
sources:
  - id: original
    resource: https://github.com/vectorize-io/hindsight
  - id: local-copy
    resource: source/source.md
tags: [agent-memory, long-term-memory, retrieval, llm-infrastructure, postgres-pgvector]
---
# vectorize-io/hindsight

Hindsight is an agent memory system that helps agents learn over time — storing world facts, experience facts, and mental models — rather than just replaying conversation history. It is delivered as a memory server (API on port 8888, UI on port 9999) with retain / recall / reflect operations scoped to a `bank_id`, plus an LLM wrapper and 60+ framework integrations. This folder holds the distilled research set: start with the summary, go deeper with the digest, then use the wiki pages and practice questions.

## How to work through this

1. Read [summary.md](summary.md) (~2 min) for the full technical picture: architecture, memory model, operations, config, and limits.
2. Read [digest.md](digest.md) (~10 min) for verbatim key points per wiki page plus the five-move narrative.
3. Read the wiki pages ([01](wiki/01-overview.md), [02](wiki/02-top-level-files.md)) for sourced detail, then [explainer.md](explainer.md) for the plain-language version.
4. Read [critical_thinking.md](critical_thinking.md) for claims-vs-evidence analysis, then test yourself with [questions.md](questions.md).

## Read This Folder

- [Summary](summary.md) — full technical analysis (overview, architecture, memory model, integrations, retain/recall/reflect loop, files, dependencies, CLI, extensibility, limits).
- [Digest](digest.md) — verbatim key points per wiki page plus the system in five moves.
- [Explainer](explainer.md) — plain-language guide: what Hindsight is, why it matters, how it works, where to use it.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, blind spots, applicability, verdict (trial).
- [Questions](questions.md) — seven retrieval-practice questions with answers covering both wiki pages plus an evaluation prompt.

## Wiki

| Page | Covers |
|---|---|
| [01](wiki/01-overview.md) | Positioning (learn vs. recall), LongMemEval accuracy claim and reproduction, server deployments and ports, clients and retain/recall/reflect, LLM wrapper, 60+ integrations |
| [02](wiki/02-top-level-files.md) | `.env.example` LLM/API config surface, `CLAUDE.md`/`AGENTS.md` contributor contract and monorepo map, ignores, lint/format pins, lockfile scope, `SECURITY.md` policy |

## Original Source

- Upstream repository: [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight)
- Local copy: [source/source.md](source/source.md)
