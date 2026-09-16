---
type: Codebase
title: Harness — Rust Control Plane for AI Agent Fleets
description: Technical analysis of majiayu000/harness (v0.6.34) — task/turn lifecycle, Starlark policy engine, multi-agent adapters, workflow runtime, cross-agent review, and what Fleet can borrow.
generated: { by: claude/muse-spark-1.3-contributor, at: 2026-09-09T00:00:00Z }
sources:
  - id: original
    resource: https://github.com/majiayu000/harness
  - id: local-copy
    resource: source/source.md
tags: [agent-orchestration, rust, policy-engine, code-review, observability]
---

# Harness — Rust Control Plane for AI Agent Fleets

Harness (majiayu000/harness, v0.6.34 @ `8b23adb6`) is a Rust control plane that wraps AI coding agents (Claude Code, Codex, Anthropic API, OpenCode) with lifecycle management, Starlark policy enforcement, cross-agent review, and OTLP observability over Postgres + Docker. It was ingested to answer what Fleet — a Python worktree-per-task orchestrator — can borrow from it.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every component's headline and key points.
3. **Wiki pages below** (~5 min each) — one component, deep. Each opens with its headline and key points, so you can stop early.

_New to the field? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

## Read This Folder

- [[summary|Summary]] — rung 1: the whole source, shallow
- [[digest|Digest]] — rung 2: the whole source at medium depth; the file to re-read on review
- [[explainer|Plain-Language Explainer]] — no-jargon explanation, applications, conclusions
- [[critical_thinking|Critical Analysis]] — claims vs. evidence, applicability, what it changes, verdict: trial
- [[questions|Retrieval Practice]] — self-test questions; **answer these from memory before re-reading anything**
- [[connections|Connections]] — related entries in this knowledge base

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-overview-architecture\|Workspace and Control-Plane Architecture]] | 13-crate map, control/data-plane split, Postgres-backed boot flow |
| [[wiki/02-task-turn-lifecycle\|Task, Thread, and Turn Lifecycle]] | leased job claims, worker turns, reconcile, terminal states |
| [[wiki/03-policy-engine\|Starlark Policy Engine and Sandboxing]] | exec-policy rules, enforcement hooks, OS/network sandbox tiers |
| [[wiki/04-agent-adapters\|Multi-Agent Adapters and Registry]] | Claude/Codex/API/OpenCode adapters, registry dispatch, streaming parsers |
| [[wiki/05-workflow-runtime\|Workflow Runtime and Worktree Isolation]] | submissions API, ExecPlan, dispatch permits, worktree isolation |
| [[wiki/06-review-and-gc\|Cross-Agent Review and Garbage Collection]] | no-self-review guards, quality gates, GC signal-to-draft lifecycle |
| [[wiki/07-observability-persistence\|Observability, Persistence, Skills, and Context]] | OTLP export, event store, Postgres schema, skill dedup |
| [[wiki/targeted\|Targeted: What Fleet Can Learn from Harness]] | fleet-comparison answers + 5-8 borrowable features with citations |

## Original Source

- [source/source.md](source/source.md) — provenance pin (repo + commit SHA), retrieved 2026-09-09
