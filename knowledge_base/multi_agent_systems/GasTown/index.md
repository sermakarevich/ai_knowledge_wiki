---
type: Codebase
title: GasTown
description: Multi-agent orchestration system (Go) coordinating coding-agent harnesses in git worktrees with beads-backed work tracking.
generated: { by: claude/muse-spark-1.3-contributor, at: 2026-09-09T00:00:00Z }
sources:
  - id: original
    resource: https://github.com/gastownhall/gastown
  - id: local-copy
    resource: source/source.md
tags: [multi-agent, orchestration, coding-agents, worktrees, beads]
---

# GasTown

GasTown (`gastownhall/gastown`, Go, v1.2.1, ~475K LOC) is a multi-agent orchestration system that coordinates AI coding agents (Claude Code, Copilot, Codex, Gemini) working in git-worktree-backed Hooks, with work state persisted in a beads (Dolt/SQL) ledger. Ingested as fleet's closest relative: same beads-DB foundation, with a targeted fleet-comparison page.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every component's headline and key points.
3. **Wiki pages below** (~10 min each) — one component, deep. Each opens with its headline and key points, so you can stop early.

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
| [[wiki/01-orchestrator-town-rig-polecat\|Orchestrator Core]] | Town/Rig/Crew/Polecat/Mayor definitions, provisioning, identity-vs-session lifecycle, on-disk layout |
| [[wiki/02-worktrees-hooks-persistence\|Worktrees & Persistence]] | Worktree lifecycle, checkpoint crash recovery, atomic writes, locking |
| [[wiki/03-beads-ledger-convoy\|Beads Ledger & Convoys]] | Bead schema, convoy feeding lifecycle, Mountain stall-skip, Dolt backend, Reaper cleanup |
| [[wiki/04-harness-adapters\|Harness Adapters]] | Multi-harness registry, per-CLI launch, ACP, wrappers, add-a-harness recipe |
| [[wiki/05-daemon-scheduler-sessions\|Daemon & Sessions]] | Tick loop, stuck/crash detection, restarts, tmux sessions, capacity scheduling, estop, quota |
| [[wiki/06-messaging-coordination\|Messaging & Coordination]] | Inter-agent mail, events, handoffs, protocol flows, log distinctions |
| [[wiki/07-cli-tui-web-config\|CLI, TUI, Web, Config]] | Command registration, command table, TUI/web roles, config files, env vars |
| [[wiki/08-safety-workflow-plugins\|Safety, Workflow, Plugins]] | Locks, formulas, plugin system, refinery/deacon, merge-strategy verdict |
| [[wiki/targeted\|Targeted: What Fleet Can Learn]] | 6 fleet questions — principles, restarts, conflicts, workflows, harnesses, 8 borrowable ideas |

## Original Source

- [source/source.md](source/source.md) — provenance pin (repo URL + commit SHA 649b832b), retrieved 2026-09-09
