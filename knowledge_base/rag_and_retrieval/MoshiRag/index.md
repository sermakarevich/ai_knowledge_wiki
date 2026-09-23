---
type: index
title: kyutai-labs/moshi-rag
description: Folder index for the kyutai-labs/moshi-rag snapshot — MoshiRAG async retrieval for full-duplex speech, Moshika weights, and PyTorch plus Rust runtimes.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T16:57:45Z
sources:
  - id: original
    resource: https://github.com/kyutai-labs/moshi-rag
  - id: local-copy
    resource: source/source.md
tags: [full-duplex-speech, retrieval-augmented-generation, moshi, real-time-dialogue]
filed_via: jev choose, category: rag_and_retrieval, confidence: 0.97
---
# kyutai-labs/moshi-rag

This folder captures the `kyutai-labs/moshi-rag` repository snapshot: a compact full-duplex Moshi speech model that keeps talking while an asynchronous back end retrieves facts in the background. Start with the summary for the big picture, use the digest for verbatim key points, then go deep in the two wiki pages for commands, configs, and deployment details.

## How to work through this

1. Read `summary.md` (~2 min) for the TL;DR, problem, ideas, and findings.
2. Read `digest.md` (~10 min) for verbatim per-page key points plus the system in five moves.
3. Go deep in the wiki pages for full quotes, commands, and runtime details, then use `explainer.md`, `critical_thinking.md`, and `questions.md` to check understanding.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem and motivation, ideas, findings, future directions.
- [Digest](digest.md) — verbatim key points per wiki page plus the argument in five moves.
- [Explainer](explainer.md) — plain-language walkthrough of the duplex RAG design.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, verdict.
- [Questions](questions.md) — retrieval practice with answers linked to wiki pages.

## Wiki

| Page | Covers |
|---|---|
| [01-overview](wiki/01-overview.md) | README.md (overview, organisation, system design, models, requirements, PyTorch and Rust run instructions); `moshi/`; `rust/`; `client/`; `front_back_end.png`; `streams.png` |
| [02-top-level-files](wiki/02-top-level-files.md) | `.gitignore`, `.pre-commit-config.yaml`, `deploy.sh`, `LICENSE-APACHE`, `LICENSE-MIT`, `requirements-dev.txt`, `swarm-config.yaml` |

## Original Source

- Original: https://github.com/kyutai-labs/moshi-rag
- Local copy: [source/source.md](source/source.md)
