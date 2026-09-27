---
type: Article
---

> [[summary|Summary]] | [[wiki/targeted|Targeted comparison]]

# Ralph loop + Conductor + orchestrator landscape

One-entry landscape: the Ralph re-run loop, Conductor's worktree review cockpit, and the awesome-list / 9-OSS-orchestrators meta-lists — compared against fleet, with borrow/do-not-copy lists. Primary source: Stephane Busso, "From Conductor to Orchestrator" (htdocs.dev, 2026-04-04).

## How to work through this

1. **2 min** — read [[summary]] (rung 1: the whole entry, shallow).
2. **10 min** — read [[wiki/targeted|Targeted comparison]] (rung 3: the six fleet-comparison questions answered in depth).
3. **Provenance** — [[source/sources]] lists every consulted URL.

## Read This Folder

- [[summary]] — TL;DRs, ideas, findings table, borrow list summary
- [[wiki/targeted|wiki/targeted]] — Ralph mechanics vs fleet retry, Conductor design, workflow abstractions, multi-harness, conflict/restart handling, 7 borrows + 5 do-not-copies
- [[source/sources]] — primary + 10 supplements with URLs and retrieval date

## Wiki pages

| Page | What it covers |
|---|---|
| [[wiki/01-ralph-loop-mechanics\|Ralph loop mechanics]] | Prompt file, shell loop, completion check, one-item rule, fit criteria, token cost |
| [[wiki/02-conductor-worktrees-review\|Conductor: worktrees + review dashboard]] | Four pillars, three-Conductor disambiguation, worktree limits, fleet parallel |
| [[wiki/03-micro-patterns\|Micro-patterns: ralphy, subtask, swarm-protocol, wit]] | Multi-harness loop, worktree fan-out, MCP leases, function locks, granularity ladder |
| [[wiki/04-fleet-comparison\|Fleet comparison]] | Retry-table vs loop, workflow ranking, 7 borrows, 5 do-not-copies |
| [[wiki/targeted\|Targeted comparison]] | All six task questions: Ralph vs fleet retry/re-queue, Conductor worktrees + review UI, workflow abstractions, multi-harness support, conflict/restart handling, borrow/do-not-copy lists; covers ralphy, subtask, swarm-protocol, wit |

## Original Source

- Primary: https://htdocs.dev/posts/from-conductor-to-orchestrator-a-practical-guide-to-multi-agent-coding-in-2026/
- Full URL list: [[source/sources]]
