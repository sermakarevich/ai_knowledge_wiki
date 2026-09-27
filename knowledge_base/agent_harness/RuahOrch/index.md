---
type: Codebase
title: ruah-orch — file-claim orchestration for parallel coding agents
description: Zero-dependency TypeScript orchestrator that isolates parallel AI coding agents with declared file-claim locks, durable artifacts, DAG workflows, and harness-agnostic executors.
generated: { by: claude/opencode-go/muse-spark-1.3-contributor, at: 2026-09-09T00:00:00Z }
sources:
  - id: original
    resource: https://github.com/ruah-dev/ruah-orch
  - id: local-copy
    resource: source/source.md
tags: [agents, orchestration, worktree, claims, multi-agent]
---

# ruah-orch — file-claim orchestration for parallel coding agents

ruah-orch (`@ruah-dev/orch-core`, v1.1.1) runs several AI coding agents against one repo in parallel without merge chaos: each task declares which files it owns, shares append-only, or only reads, and the orchestrator enforces that contract before, during, and after execution — with zero runtime dependencies.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every component's headline and key points.
3. **Wiki pages below** (~N min each) — one component, deep. Each opens with its headline and key points, so you can stop early.

_New to the field? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

## Read This Folder

- [[summary|Summary]] — rung 1: the whole source, shallow
- [[digest|Digest]] — rung 2: the whole source at medium depth; the file to re-read on review
- [[explainer|Plain-Language Explainer]] — no-jargon explanation, applications, conclusions
- [[critical_thinking|Critical Analysis]] — claims vs. evidence, applicability, what it changes, verdict
- [[questions|Retrieval Practice]] — self-test questions; **answer these from memory before re-reading anything**
- [[connections|Connections]] — related entries in this knowledge base

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-claims-and-artifacts\|Claims, Artifacts, and Contract Enforcement]] | Three-bucket claim locks, artifact capture, post-execution contract validation |
| [[wiki/02-state-and-restart-safety\|State, Persistence, and Restart Safety]] | Single JSON state file, atomic locked writes, revision guards, migration, restart reconciliation |
| [[wiki/03-planner-and-workflows\|Planner, DAG Workflows, and Claim-Aware Scheduling]] | Markdown task graphs, DAG validation, claim-aware parallel/serial planning, merge order |
| [[wiki/04-executors-and-workspaces\|Executors, Workspace Providers, and Task Lifecycle]] | Seven harness adapters, worktree isolation, task lifecycle, RUAH_* env vars |
| [[wiki/targeted\|Ruah File-Claim Orchestration: Answers to Fleet's Targeted Questions]] | Fleet's six questions: principles, restarts, conflicts, workflows, harnesses, borrowable ideas |

## Original Source

- [source/source.md](source/source.md) — provenance pin (repo + commit SHA), retrieved 2026-09-09
