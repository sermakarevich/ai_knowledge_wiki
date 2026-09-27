---
type: index
title: A Generalized Software Architecture for Swarm
description: Folder index for the decentralized swarm architecture paper — summary, digest, wiki pages, and study aids.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-15T06:49:36Z
sources:
  - id: original
    resource: http://127.0.0.1:8765/Agentic_AI1.pdf
  - id: local-copy
    resource: source/source.md
tags: [swarm-intelligence, multi-agent-systems, decentralized-coordination, LLM-agents]
---

# A Generalized Software Architecture for Swarm

This folder indexes a paper proposing a fully decentralized, task-agnostic software architecture for swarms of heterogeneous LLM agents. Instead of a central orchestrator, peer agents coordinate through bidding, gossip-disseminated shared state, and dynamic membership handling. Use the summary for the big picture, the digest for verbatim key claims, and the wiki pages for section-by-section detail.

## How to work through this

1. Start with the **summary (~2 min)** for the plain-language TL;DR, problem, main ideas, and findings.
2. Then read the **digest (~10 min)** for the full argument in five moves plus verbatim one-sentence theses and key points per chunk.
3. Then go deep into the **wiki pages** in order (01 → 02 → 03), using **explainer**, **critical_thinking**, **questions**, and **connections** to test and extend understanding.

## Read This Folder

- [Summary](summary.md) — human-readable TL;DR, problem and motivation, main ideas, findings, future directions.
- [Digest](digest.md) — verbatim one-sentence theses and key points per chunk plus the argument in five moves.
- [Explainer](explainer.md) — plain-language walkthrough of the architecture for non-experts.
- [Critical Thinking](critical_thinking.md) — claims vs. evidence, what's new vs. repackaged, weaknesses and blind spots.
- [Questions](questions.md) — retrieval-practice questions with answers covering every wiki page.
- [Connections](connections.md) — links to related papers and systems in the knowledge base.

## Wiki

| Page | Covers |
|------|--------|
| [01-generalized-swarm-architecture-overview](wiki/01-generalized-swarm-architecture-overview.md) | Abstract through Sec. IV.B: motivation, three requirements, three planes, agent/goal formalization start, five principles |
| [02-system-model-task-representation](wiki/02-system-model-task-representation.md) | Sec. IV.B tail–IV.E plus V.A/V.D start: task tuple, recursive decomposition, bidding and awards, CRDT-gossip state, membership and fault recovery |
| [03-decentralized-state-synchronization](wiki/03-decentralized-state-synchronization.md) | Tail of Sec. IV-D through Sec. VIII: layers 4–5, agent internals, goal lifecycle, scalability/consistency/fault-tolerance analysis, limits and conclusion |

## Original Source

- Original PDF: [A Generalized Software Architecture for Swarm](http://127.0.0.1:8765/Agentic_AI1.pdf)
- Local copy: [source/source.md](source/source.md)
