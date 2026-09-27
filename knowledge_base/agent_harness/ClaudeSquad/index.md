---
type: Codebase
title: Claude Squad
description: Terminal-first parallel agent runner that isolates each coding agent in its own tmux session plus git worktree, with a no-adapter multi-harness design.
generated: { by: claude/opencode-go/muse-spark-1.3-contributor, at: 2026-09-09T00:00:00Z }
sources:
  - id: original
    resource: https://github.com/smtg-ai/claude-squad
  - id: local-copy
    resource: source/source.md
tags: [coding-agents, tmux, git-worktrees, tui, orchestration]
---

# Claude Squad

Claude Squad (`smtg-ai/claude-squad`, analyzed at v1.0.20) is a single-binary terminal app for running multiple AI coding agents in parallel: one tmux session plus one git worktree per worker, managed through a keyboard-driven Bubble Tea TUI (Terminal User Interface). Its central lesson for parallel-agent orchestration is how far near-zero abstraction goes — no workflow engine, no per-harness adapters — and where that floor ends.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every component's headline and key points.
3. **Wiki pages below** (~N min each) — one component, deep. Each opens with its headline and key points, so you can stop early.

_New to the field? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki. Fleet context? Go straight to [[wiki/targeted|Targeted Analysis for Fleet]]._

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
| [[wiki/01-architecture-and-entry\|Architecture and Entry Points]] | Entry via cobra rootCmd into Bubble Tea TUI fanning agent CLIs across tmux sessions and git worktrees. |
| [[wiki/02-session-lifecycle\|Session Lifecycle and State]] | Instance record plus JSON state file driving create/pause/resume/checkout/push/kill and tmux-loss reconciliation. |
| [[wiki/03-tmux-backend\|Tmux Backend and Autoyes Daemon]] | Tmux session lifecycle, PTY/platform split, capture-pane scraping, and autoyes daemon key injection. |
| [[wiki/04-git-worktree-isolation\|Git Worktree Isolation and Review]] | Per-instance git worktree isolation with branch naming, diff pipeline, gh-backed push flows, cleanup, and failure modes. |
| [[wiki/05-tui-and-keybindings\|TUI Views and Keybindings]] | Bubble Tea list/preview/diff/terminal panes with overlay system and full keyboard map. |
| [[wiki/06-config-and-multi-harness\|Config, Profiles, and Multi-Harness]] | Config/profiles as verbatim tmux program strings with no per-harness adapters, covering schema, flags, spawn chain, state split, and logging. |
| [[wiki/targeted\|Targeted Analysis for Fleet]] | Fleet-focused analysis of Claude Squad (tmux+worktree parallelism, restart reconciliation, no-adapter multi-harness) with source-verified citations. |

## Original Source

- [source/source.md](source/source.md) — provenance pin (repo + commit SHA), retrieved 2026-09-09
