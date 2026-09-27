---
type: Codebase
title: Claude-Orchestrator Skill + Orchestration-Playbook Core
description: Harness-agnostic multi-agent orchestration discipline (evidence levels, dispatch contract, acceptance iron rules, ORC-01-18) and its Claude Code adapter, with fleet-borrowable ideas.
generated: { by: claude/opencode-go/muse-spark-1.3-contributor, at: 2026-09-09T19:00:33Z }
sources:
  - id: original
    resource: https://github.com/indiekitai/claude-orchestrator
  - id: supplement
    resource: https://github.com/indiekitai/orchestration-playbook
  - id: local-copy
    resource: source/source.md
tags: [orchestration, multi-agent, code-review, worktree, evidence]
---

# Claude-Orchestrator Skill + Orchestration-Playbook Core

A failure-case library and orchestration discipline distilled from production-scale agent runs, plus its Claude Code adapter: synchronous worktree batches, bounded dispatch contracts, and mandatory cross-model review. Ingested as a targeted analysis for fleet comparison — task contracts, worktree agents, quality gates, merges.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~10 min each) — one topic, deep. Each opens with its headline and key points, so you can stop early.
4. **[[wiki/targeted|Targeted deep dive]]** (~15 min) — six fleet questions answered in depth.

_New to the field? The targeted page opens with a one-sentence headline and key-points block — read that first. Coming back after a break? Re-read the key points, not the whole page._

## Read This Folder

- [[summary|Summary]] — rung 1: the whole source, shallow
- [[digest|Digest]] — rung 2: the whole source at medium depth; the file to re-read on review
- [[explainer|Plain-Language Explainer]] — no-jargon explanation, applications, conclusions
- [[critical_thinking|Critical Analysis]] — claims vs. evidence, applicability, what it changes, verdict
- [[questions|Retrieval Practice]] — self-test questions; **answer these from memory before re-reading anything**
- [[connections|Connections]] — related entries in this knowledge base
- [[wiki/targeted|Targeted Deep Dive]] — design principles, restart/ledger, conflicts, workflow abstraction, adapters, 7 fleet-borrowable ideas, playbook-vs-adapter deltas, caveats

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-task-contracts-dispatch\|Task Contracts and Dispatch]] | Ten-field contract, adapter template, design-first gate |
| [[wiki/02-worktree-agents-batch-loop\|Worktree Agents and the Batch Loop]] | Sync batches, worktree isolation, concurrency policy, rescue |
| [[wiki/03-evidence-discipline-acceptance-rules\|Evidence Discipline and Acceptance Iron Rules]] | Four evidence levels, no-upgrade rule, acceptance checklist |
| [[wiki/04-orc-antipatterns\|ORC Anti-Patterns]] | ORC-01–18 rejection vocabulary + prune rule |
| [[wiki/05-cross-model-review-fleet-lessons\|Cross-Model Review and Fleet Lessons]] | Different-family review, enforcement gate, 7 borrowable ideas |
| [[wiki/targeted\|Targeted Deep Dive]] | All six fleet questions + deltas + borrowable ideas + caveats, with file:line citations |

## Original Source

- [source/source.md](source/source.md) — provenance pin: claude-orchestrator @ `7a81c78`, orchestration-playbook @ `76d6857`, retrieved 2026-09-09
