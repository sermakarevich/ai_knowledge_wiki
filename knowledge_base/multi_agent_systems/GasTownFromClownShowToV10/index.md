---
type: Article
title: "Gas Town: From Clown Show to v1.0"
description: Steve Yegge's Gas Town v1.0 story — how a 20-30-agent coding factory fixed worker-killings, data loss, and Dolt bloat; fleet lessons inside.
generated: { by: claude/muse-spark-1.3-contributor, at: 2026-09-09T00:00:00Z }
sources:
  - id: original
    resource: https://steve-yegge.medium.com/gas-town-from-clown-show-to-v1-0-c239d9a407ec
  - id: supplement
    resource: https://yegge.ai/essays/welcome-to-gas-town/
  - id: local-copy
    resource: source/source.md
tags: [agents, orchestration, beads, dolt, workflows]
---

# Gas Town: From Clown Show to v1.0

Steve Yegge's v1.0 retrospective on Gas Town (a multi-agent coding factory) and Beads (its Git-backed task ledger): what broke at scale and what held. Worth ingesting for fleet's worker-lifecycle, merge-queue, and ledger-bloat decisions.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every page's headline and key points.
3. **Wiki pages below** (~10 min each) — one topic, deep. Each opens with its headline and key points, so you can stop early.
4. **[[wiki/targeted|Targeted deep dive]]** — the fleet-relevant answers: principles, restarts, conflicts, workflows, harnesses, borrow-list, scale dangers.

_New to agents? Start with the Human TL;DR in [[summary|Summary]] or [[explainer|the plain-language explainer]]. Coming back later? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

## Read This Folder

- [[summary|Summary]] — rung 1: the whole source, shallow
- [[digest|Digest]] — rung 2: the whole source at medium depth; the file to re-read on review
- [[explainer|Plain-Language Explainer]] — no-jargon explanation, applications, conclusions
- [[critical_thinking|Critical Analysis]] — claims vs. evidence, applicability, what it changes, verdict
- [[questions|Retrieval Practice]] — self-test questions; **answer these from memory before re-reading anything**
- [[connections|Connections]] — related entries in this knowledge base
- [[wiki/targeted|Targeted: fleet lessons]] — design, Deacon/corpse recovery, Refinery conflicts, Mayor/Crew/Convoy/patrol/molecule mechanics, multi-harness, 7 borrowable ideas, scale dangers
- [[source/source|Source provenance]] — which URL was actually used (Medium 403, yegge.ai fallback)

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-town-mayor-crew-convoys\|Town, Roles, and Convoys]] | Town/rigs/Overseer, 7 worker roles, mail, convoys, GUPP/nudge/seance, tmux loop |
| [[wiki/02-beads-dolt-meow-wisps\|Beads on Dolt: MEOW and Wisps]] | Beads ledger, Embedded Dolt migration, MEOW stack, NDI, wisps/Reaper, patrols/plugins |
| [[wiki/03-clown-show-failures\|The Clown Show: Failures and Fixes]] | Killer watchdog, 22 data-loss noses, corpses, spawn storm #22, Dolt bloat, v1.0 evidence |
| [[wiki/04-scale-lessons-for-fleet\|Scale Lessons for Fleet]] | Stage/cost gates, K8s/Temporal comparisons, 7 borrowable ideas, dangers, Gas City roadmap |
| [[wiki/targeted\|Targeted: GasTown v1.0 Deep Dive]] | All 7 fleet questions + Jan-vs-Apr deltas |

## Original Source

- [Medium: Gas Town from Clown Show to v1.0](https://steve-yegge.medium.com/gas-town-from-clown-show-to-v1-0-c239d9a407ec) — paywalled on fetch (403); excerpts via search/mirrors, retrieved 2026-09-09
- [yegge.ai: Welcome to Gas Town](https://yegge.ai/essays/welcome-to-gas-town/) — read in full, retrieved 2026-09-09
- [yegge.ai: Gas Town hub](https://yegge.ai/gastown.html)
- Code: [gastown](https://github.com/gastownhall/gastown) / [beads](https://github.com/gastownhall/beads)
