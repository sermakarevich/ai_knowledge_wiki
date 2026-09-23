---
type: index
title: kyutai-labs/moshi
description: Folder index for kyutai-labs/moshi — full-duplex speech-text dialogue on the Mimi streaming codec, with PyTorch, MLX, and Rust inference stacks.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T16:56:58Z
sources:
  - id: original
    resource: https://github.com/kyutai-labs/moshi
  - id: local-copy
    resource: source/source.md
tags: [speech-dialogue, full-duplex, neural-audio-codec, streaming-inference]
filed_via: "jev choose, category: models, confidence: 0.88"
---

# kyutai-labs/moshi

Moshi is a full-duplex speech-text foundation model built on the Mimi streaming neural audio codec, modeling two live audio streams plus a text inner monologue at ~160 ms theoretical / ~200 ms practical latency. The repo ships three inference stacks — PyTorch for research, MLX for on-device Mac/iPhone, Rust for production — plus a web UI client and Moshiko/Moshika voice checkpoints. These notes distill the repo snapshot into a summary, digest, two wiki pages, and retrieval aids.

## How to work through this

1. Read `summary.md` (~2 min) for the TL;DR of the problem, architecture, and stacks.
2. Read `digest.md` (~10 min) for verbatim key points per section plus the system in five moves.
3. Deep-dive the wiki pages in order for full detail, then test yourself with `questions.md` and check `critical_thinking.md` for claims-vs-evidence gaps.

## Read This Folder

- [Summary](summary.md) — overview, architecture, pipeline, files, dependencies, usage, and limits.
- [Digest](digest.md) — compressed key points per section plus the system in five moves.
- [Explainer](explainer.md) — plain-language walkthrough of Moshi, Mimi, and the three inference stacks.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, applicability, verdict.
- [Questions](questions.md) — retrieval practice (Q1–Q7) covering both wiki pages.

## Wiki

| Page | Covers |
|---|---|
| [01-overview](wiki/01-overview.md) | Repo organisation, Moshi dual-stream + Depth/Temporal architecture, Mimi codec, Moshiko/Moshika checkpoints, requirements, PyTorch/MLX/Rust inference, clients |
| [02-top-level-files](wiki/02-top-level-files.md) | Top-level hygiene and ops: .dockerignore, .gitignore, .pre-commit-config.yaml, deploy.sh, FAQ.md, licenses, requirements-dev.txt, swarm-config.yml |

## Original Source

- Upstream: [https://github.com/kyutai-labs/moshi](https://github.com/kyutai-labs/moshi)
- Local copy: [source/source.md](source/source.md)
