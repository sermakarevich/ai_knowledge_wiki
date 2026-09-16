---
type: Codebase
title: superharness
description: Superharness is a SQLite-backed coordination layer with queue-based delegation and harness adapters for supervising coding-agent CLIs, ingested as the closest missed framework to fleet's queue plus persistent-state model.
generated: { by: claude/opencode-go-muse-spark-1.3-contributor, at: 2026-09-09T19:11:04Z }
sources:
  - id: original
    resource: https://github.com/artificemachine/superharness
  - id: local-copy
    resource: source/source.md
tags: [multi-agent, orchestration, sqlite, harness]
---

# superharness

Superharness is a coordination layer (not another agent) for running several coding-agent CLIs against one project without collisions. Its central design is one per-project SQLite `state.db` as the sole runtime authority, queue-based delegation (`inbox` rows fed by enqueue, claimed atomically by dispatch, supervised by watch), a Harness adapter registry for five agent runtimes, lifecycle status gates plus a dual event-driven watchdog. It was ingested for fleet comparison as the closest missed framework to fleet's queue plus persistent-state model.

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
| [[wiki/01-shared-contract-sqlite-state\|Shared Contract and SQLite State]] | One per-project SQLite `state.db` (39 migrations, Pydantic-validated contract model) is the sole runtime authority, with all task/inbox/handoff writes funneled through typed DAO boundaries and canonical `state_reader` / `state_writer` paths while YAML survives only as export/backfill material. |
| [[wiki/02-queue-delegation-lifecycle\|Queue-Based Delegation and Lifecycle Rules]] | Delegation is a SQLite-backed queue (`inbox` rows) fed by `inbox_enqueue`, claimed atomically by `inbox_dispatch`, supervised by `inbox_watch`, while task progress follows a strict status graph (`next_action.py`) plus a timeout reconciler (`lifecycle_rules.py`). |
| [[wiki/03-worker-restart-crash-recovery\|Worker Restart and Crash Recovery]] | Crashed or timed-out workers are detected via heartbeats and stale inbox rows, their partial state survives in append-only handoffs plus ledger plus git-stash checkpoints plus auto-flush YAML, and the next dispatch respawns with that full context while durable counters cap retry loops. |
| [[wiki/04-conflict-resolution-gates\|Conflict Resolution and Lifecycle Gates]] | Superharness prevents agent conflicts with per-agent git worktrees plus hook-layer write/push guards, and prevents premature progress with dispatch-time gates (status, preflight, policy, plan quality) and close-time gates (status, subtask resolution, verification, ownership). |
| [[wiki/05-workflow-abstraction\|Workflow Abstraction]] | The workflow layer is a verb surface (`enqueue`/`dispatch`/`watch`/`talk`/`delegate`/`discuss`) over a SQLite-backed task state machine with per-workflow dispatch gates, orchestrator routing, three fanout executors, quorum-gated discussions, classifier-driven auto-dispatch, and YAML module hooks. |
| [[wiki/06-multi-harness-adapters\|Multi-Harness Support]] | Superharness dispatches work to five coding-agent runtimes (Claude Code, Codex CLI, Gemini CLI, opencode, Pi) through one `Harness` protocol plus a Python adapter registry and per-harness launcher scripts, with golden parity tests proving adapter argv is byte-identical to the legacy path. |
| [[wiki/07-watchdog-telemetry-benchmark\|Watchdog, Telemetry, Skills, and Benchmarks]] | Stuck work is killed by a dual event-driven watchdog (`idle-timeout` + `absolute-ceiling`), liveness is decided from DB heartbeats, all activity lands in typed telemetry events with opt-in Langfuse export, and completed work feeds a skill library plus a cost leaderboard. |
| [[wiki/targeted\|Targeted Analysis]] | Fleet-targeted Q&A: design principles, crash recovery, conflict resolution, workflow abstraction, multi-harness adapters, and what fleet can borrow (Q1–Q6). |

## Original Source

- [source/source.md](source/source.md) — provenance pin (commit 9c2166dccac6717b8b4056a8eae87c44052d77d5, 2026-08-28), retrieved 2026-09-09
