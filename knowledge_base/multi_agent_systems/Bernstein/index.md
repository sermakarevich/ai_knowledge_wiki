---
type: Codebase
title: Bernstein
description: Open-source Python orchestrator for AI coding agents — deterministic scheduler, per-task git worktrees, 40+ coder adapters, signed lineage receipts.
generated: { by: claude/opencode-go-muse-spark, at: 2026-09-09T00:00:00Z }
sources:
  - id: original
    resource: https://github.com/sipyourdrink-ltd/bernstein
  - id: local-copy
    resource: source/source.md
tags: [orchestration, ai-agents, deterministic-scheduler, git-worktrees, adapters]
---

# Bernstein

Bernstein (v3.19.1, beta, solo-maintained) is the open-source governance layer for AI agents: a deterministic Python scheduler with no model in the coordination loop, per-task git worktrees behind merge gates, 40+ CLI coder adapters, and signed lineage receipts verifiable offline. Ingested as a deep dive for fleet (beads-DB + Python orchestrator + worktree coders) — see [[wiki/targeted|the targeted fleet comparison]] for the 8 borrowable ideas.

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
| [[wiki/01-deterministic-scheduler\|Deterministic Scheduler]] | Tick loop, DAG scheduling, strict LLM replay, Merkle journal, .sdd state |
| [[wiki/02-task-lifecycle-retries\|Task Lifecycle and Retries]] | Task states, atomic claims, restarts, janitor, checkpoint retries, DLQ, model escalation |
| [[wiki/03-worktrees-merge-gates\|Worktrees and Merge Gates]] | Per-task worktrees, merge queue, quality gates, artifact workspaces |
| [[wiki/04-adapter-registry\|Adapter Registry]] | Adapter registry, CLIAdapter contract, multi-harness support |
| [[wiki/05-workflow-abstraction\|Workflow Abstraction]] | Task graphs, phases, roles, artifact contracts |
| [[wiki/06-lineage-receipts-audit\|Lineage, Receipts and Audit]] | Lineage spine, replay journal, signed receipts, evidence bundles, offline verification |
| [[wiki/07-policy-quality-gates\|Policy and Quality Gates]] | Policy as code, gates, approvals, admission, credential scoping, cost routing |
| [[wiki/targeted\|Targeted: Bernstein for Fleet]] | Fleet comparison — design principles, retries, conflicts, workflows, adapters, 8 borrow ideas |

## Original Source

- [source/source.md](source/source.md) — provenance pin (commit 36326d75427e663b6d1da05dbd6d8de582d361a4, 2026-09-09), retrieved 2026-09-09
