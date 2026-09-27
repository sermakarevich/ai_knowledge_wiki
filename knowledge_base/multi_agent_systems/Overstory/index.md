---
type: Codebase
title: Overstory
description: Overstory is a multi-agent coding orchestrator that runs single-purpose agents in isolated git worktrees coordinated through typed SQLite mail, with watchdog supervision and a tiered merge queue.
generated: { by: claude/opencode-worker, at: 2026-09-09T19:12:53Z }
sources:
  - id: original
    resource: https://github.com/Marmalade118/overstory
  - id: local-copy
    resource: source/source.md
tags: [multi-agent, orchestration, worktrees, sqlite, code-review]
---

# Overstory

This entry covers the Overstory codebase: a strict coordinator-lead-leaf multi-agent runtime for parallel coding work. Its central idea is isolation plus typed coordination — one-purpose agents in separate git worktrees, talking through SQLite mail, guarded by watchdogs and merged through a tiered conflict queue. It was worth ingesting as a concrete reference design for Fleet-style orchestration.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every chapter's headline and key points.
3. **Wiki pages below** (~N min each) — one chapter, deep. Each opens with its headline and key points, so you can stop early.

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
| [[wiki/01-agent-roles-and-overlays\|Agent Roles and Overlays]] | Coordinator, lead, leaf roles plus per-task overlays and tool guards |
| [[wiki/02-multi-harness-runtime\|Multi-Harness Runtime]] | AgentRuntime interface and registry for pluggable harness backends |
| [[wiki/03-sqlite-mail-messaging\|SQLite Mail Messaging]] | Typed agent mail stored and queried in SQLite |
| [[wiki/04-merge-queue-and-conflicts\|Merge Queue and Conflicts]] | FIFO merge queue with 4-tier conflict resolution and learning loop |
| [[wiki/05-watchdog-and-supervision\|Watchdog and Supervision]] | Tiered watchdog escalation, checkpoints, handoffs, and session resume |
| [[wiki/06-worktrees-and-isolation\|Worktrees and Isolation]] | Isolated git worktrees, branch ownership, and file scoping |
| [[wiki/07-tracker-workflows-metrics\|Tracker, Workflows, Metrics]] | Issue tracking, CLI workflows, and run metrics |
| [[wiki/targeted\|Targeted Brief for Fleet]] | Condensed brief mapping Overstory patterns onto Fleet |

## Original Source

- [source/source.md](source/source.md) — provenance pin (commit a961ee5206d85e9d9a37a65ed985de70580f6192, 2026-03-10), retrieved 2026-09-09
