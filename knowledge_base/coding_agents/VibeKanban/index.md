---
type: Codebase
title: Vibe Kanban
description: Local-first kanban board running parallel AI coding agents in isolated workspaces, with an adapter trait for 10+ harnesses and diff-first review.
generated: { by: claude/muse-spark-1.3-contributor, at: 2026-09-09T21:10:00Z }
sources:
  - id: original
    resource: https://github.com/BloopAI/vibe-kanban
  - id: local-copy
    resource: source/source.md
tags: [agents, orchestration, kanban, code-review, multi-harness]
---

# Vibe Kanban

Vibe Kanban (BloopAI) is a local-first kanban board for running parallel AI coding agents: plan as issues on a board, execute each in an isolated workspace (branch + terminal + dev server), review the diff in the UI, merge via PR. The company shut down in April 2026; the repo is community-maintained. Worth ingesting as fleet's closest worked example of board-driven multi-agent orchestration.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every component's headline and key points.
3. **Wiki pages below** (~N min each) — one component, deep. Each opens with its headline and key points, so you can stop early.

_New to the field? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki. Evaluating for fleet? Go straight to [[wiki/targeted|the targeted fleet analysis]]._

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
| [[wiki/01-overview-architecture\|Architecture Overview]] | Rust backend + TypeScript frontend split, local-first storage, relay/cloud track |
| [[wiki/02-executor-adapter-layer\|Executor Adapter Layer]] | One trait, 10-agent mapping, spawn/discovery/approvals/logs/MCP |
| [[wiki/03-workspaces-and-worktrees\|Workspaces and Worktrees]] | Data model, branch mechanics, terminal, dev servers, restart recovery |
| [[wiki/04-kanban-issues-and-workflow\|Kanban Issues and Workflow]] | Emergent workflow: status rows, issue-workspace link, 3 automations vs manual moves |
| [[wiki/05-diff-review-and-pr-flow\|Diff Review and PR Flow]] | Diff computation, comment-to-agent loop, PR create/monitor/merge, conflicts |
| [[wiki/06-preview-browser-and-dev-server\|Preview Browser and Dev Server]] | Proxy request paths, dev-server lifecycle, inspect/Eruda, security bounds |
| [[wiki/07-persistence-config-and-ops\|Persistence, Config, and Ops]] | SQLite schema, services, CLI/env, MCP tools, operational gotchas |
| [[wiki/targeted\|Targeted: Vibe Kanban for Fleet]] | Six fleet questions + 7 borrowable features with file anchors |

## Original Source

- [source/source.md](source/source.md) — provenance pin, retrieved 2026-09-09
