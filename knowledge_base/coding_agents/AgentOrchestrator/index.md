---
type: Article
title: Agent Orchestrator (AO) — Run Coding Agents in Parallel
description: Local-first fleet runner for AI coding agents — isolated worktrees, one PR per session, derived status, built-in CI/review lifecycle.
generated: { by: claude/muse-spark-1.3-contributor, at: 2026-09-09T18:54:13Z }
sources:
  - id: original
    resource: https://useao.dev
  - id: local-copy
    resource: source/article.md
tags: [agents, orchestration, worktrees, pull-requests, control-plane]
---

# Agent Orchestrator (AO)

Product docs for AO (Untrivial-ai, useao.dev): a local-first desktop control plane that runs fleets of coding agents in isolated git worktrees with one pull request per session and daemon-driven CI/review/merge lifecycle. Ingested for the fleet orchestrator comparison track.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every wiki page's headline and key points.
3. **Wiki pages below** (~5 min each) — one topic, deep. Each opens with its headline and key points, so you can stop early.
4. **[[wiki/targeted|Targeted analysis]]** — the six fleet questions answered directly.

_New to the field? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

## Read This Folder

- [[summary|Summary]] — rung 1: the whole source, shallow
- [[digest|Digest]] — rung 2: the whole source at medium depth; the file to re-read on review
- [[explainer|Plain-Language Explainer]] — no-jargon explanation, applications, conclusions
- [[critical_thinking|Critical Analysis]] — claims vs. evidence, applicability, what it changes, verdict
- [[questions|Retrieval Practice]] — self-test questions; **answer these from memory before re-reading anything**
- [[connections|Connections]] — related entries in this knowledge base
- [[wiki/targeted|Targeted Analysis]] — fleet comparison answers (six questions)
- [[source/article|Source notes]] — provenance + abridged extraction

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-worktree-isolation\|Worktree Isolation]] | One worktree + branch per session, Scratch dirs, conservative cleanup, restore, one live interface |
| [[wiki/02-one-pr-per-agent-flow\|One PR per Agent]] | PR claiming + takeover guard, SCM observer, ownership routing, reviewer agents, explicit merge |
| [[wiki/03-control-surface\|Control Surface]] | Go daemon + thin clients, durable facts / derived status, SQLite + CDC/SSE, loopback networking, 8 rules |
| [[wiki/04-ci-review-feedback-routing\|CI, Review, and Feedback Routing]] | Observer facts, lifecycle reaction table, signature dedup, mode-aware delivery, reviewer loop, explicit merge |
| [[wiki/05-harness-support-and-fleet-lessons\|Harness Support and Fleet Lessons]] | 27 compiled-in harnesses, Chat gating, session roles vs DSL, 7 borrowable ideas + limits |
| [[wiki/targeted\|Targeted Analysis]] | Design principles, restart handling, worktree/PR/merge conflict resolution, workflow abstraction, multi-harness adapters, 7 borrowable ideas |

## Original Source

- [source/article.md](source/article.md) — abridged article text + provenance, retrieved 2026-09-09
- Canonical: https://useao.dev + https://useao.dev/docs/architecture/
