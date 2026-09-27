---
type: index
title: google/ax
description: Declarative Kubernetes-like orchestrator for sandboxed autonomous agent workloads at scale
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-24T03:07:29Z
sources:
  - id: original
    resource: https://github.com/google/ax
  - id: local-copy
    resource: source/source.md
tags: [agents, kubernetes, orchestration, sandboxing]
---
# google/ax

AX is a declarative, Kubernetes-like orchestrator for running sandboxed autonomous agent workloads at scale on Agent Substrate. Users declare `Task`, `Workspace`, `Gateway`, and `Model` manifests and operate them with a kubectl-shaped `ax` CLI backed by Redis instead of etcd. This folder holds a 2-minute summary, a 10-minute digest, plain-language and critical takes, retrieval questions, and two wiki pages.

## How to work through this

1. Start with the [summary](summary.md) (~2 min) for the architecture, lifecycle, and CLI surface.
2. Read the [digest](digest.md) (~10 min) for verbatim key points plus the five-move system narrative.
3. Go deep with the [wiki pages](wiki/01-overview.md) as needed, then check [explainer](explainer.md), [critical thinking](critical_thinking.md), and [questions](questions.md).

## Read This Folder

- [Summary](summary.md) — full technical analysis (overview, architecture, lifecycle, files, deps, CLI).
- [Digest](digest.md) — verbatim key points per wiki page plus the system in five moves.
- [Explainer](explainer.md) — plain-language guide: what it is, why it matters, how it works.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, weaknesses, applicability, verdict.
- [Questions](questions.md) — seven retrieval prompts with answers covering both wiki pages.

## Wiki

| Page | Covers |
|---|---|
| [01-overview](wiki/01-overview.md) | README.md (project purpose, primitives, install/deploy/run, docs index, CLI reference) |
| [02-top-level-files](wiki/02-top-level-files.md) | `.dockerignore`, `.gitignore`, `.ko.yaml`, `demo.sh`, `DESIGN.md`, `Dockerfile.task-runner`, `go.sum` |

## Original Source

- Upstream: [https://github.com/google/ax](https://github.com/google/ax)
- Local copy: [source/source.md](source/source.md)
