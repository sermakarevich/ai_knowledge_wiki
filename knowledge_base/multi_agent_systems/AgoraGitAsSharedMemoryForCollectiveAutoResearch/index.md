---
type: Paper
title: "Agora: Git as Shared Memory for Collective AutoResearch"
description: Agora stores multi-agent research as an append-only Git DAG of immutable commits with evidence-weighted quality and diversity-aware attention, and 13 uncoordinated workers used it to drive a frozen 119.6M hybrid from 3.39 to 1.899 bits per byte with no training data.
generated: { by: claude/muse-spark-1.3-contributor, at: 2026-09-17T17:06:18Z }
sources:
  - id: original
    resource: https://arxiv.org/pdf/2609.18094
  - id: local-copy
    resource: source/source.md
tags: [multi-agent-systems, collective-intelligence, git-provenance, exploration-diversity, weight-transfer]
---

# Agora: Git as Shared Memory for Collective AutoResearch

Agora (Zhang et al., NVIDIA — arXiv:2609.18094) proposes Git history as the only shared state for collective autonomous research: every result, insight, hypothesis, verification, and report is an immutable commit linked to what it builds on, quality is set by downstream reproduction and reuse rather than votes, and diversity-aware views keep uncoordinated workers from collapsing onto one leaderboard leader. In its first sustained run, thirteen task-free coding-agent workers published 1,703 contributions over nearly twelve days on a no-training weight-transfer task, closing 62% of the gap to a trained GPT-2 124M — after a single human-supplied diversity map broke a five-day monoculture.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~10 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

_New to shared-memory research infrastructure or weight transfer? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

## Read This Folder

- [[summary|Summary]] — rung 1: the whole paper, shallow
- [[digest|Digest]] — rung 2: the whole paper at medium depth; the file to re-read on review
- [[explainer|Plain-Language Explainer]] — no-jargon explanation, applications, conclusions
- [[critical_thinking|Critical Analysis]] — claims vs. evidence, applicability, what it changes
- [[questions|Retrieval Practice]] — self-test questions; **answer these from memory before re-reading anything**

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-agora-overview\|Overview]] | Git-backed append-only research DAG, evidence-weighted quality, shared-state-only coordination, 13-worker / 1,703-contribution run |
| [[wiki/02-exploration-quality-diversity\|Exploration, open-ended search, and quality diversity]] | Bandits/UCT, novelty search, MAP-Elites, POET as heuristics; DAG node model, evidence score, leaderboard limits, clustering views |
| [[wiki/03-diversity-ucb-attention\|Diversity-aware UCB ranking and attention allocation]] | Diversity-aware UCB formula, exploit / explore-known / explore-novel slots, Go+SQLite+Git prototype, weight-transfer task, evaluator, worker setup |
| [[wiki/04-weight-transfer-recipe\|Algorithm 1 Donor-Behavior Transfer, As Committed]] | Winning transfer(): low-rank bigram operator in embeddings/head plus sparse banded attention/SSM/FFN routes, trajectory, negative results, lineage and reproduction |
| [[wiki/05-conclusion-coordination\|Conclusion — Scaling autonomous researchers without scaling their institution]] | Durable/linked contributions, reproduction-set quality, neglected-branch visibility; monoculture escape and unsettled causality |
| [[wiki/06-references\|References and Reproducibility Appendices]] | Retained-run identity groups, minimal contribution and verification records, matched Isolated / Flat-log / Central-planner / Agora evaluation matrix |

## Original Source

- [https://arxiv.org/pdf/2609.18094](https://arxiv.org/pdf/2609.18094) — Paper source, arXiv:2609.18094
- [source/source.md](source/source.md) — Local copy of the paper source
