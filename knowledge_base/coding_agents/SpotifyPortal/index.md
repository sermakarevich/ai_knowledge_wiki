---
type: Article
title: Portal by Spotify Cut My Claude Code Token Usage by 90%
description: Spotify's hook-enforced routing sends grunt work to a cheap worker model, cutting Claude Code tokens by ~90% on bulk reads.
generated: { by: claude/muse-spark-1.3-contributor, at: 2026-09-12T11:59:00Z }
sources:
  - id: original
    resource: https://engineering.atspotify.com/2026/9/portal-by-spotify-cut-my-claude-code-token-usage-by-90
  - id: local-copy
    resource: source/article.md
tags: [cost-optimization, model-routing, claude-code, agents]
---

# Portal by Spotify Cut My Claude Code Token Usage by 90%

Spotify Engineering (September 2026, Dimitri Mazmanov) shows how declarative worker modes plus an enforcing plugin cut Claude Code token use by about 90% on bulk reads. Worth ingesting because hook-enforced cheap-model routing is directly reusable for harness cost engineering.

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
| [[wiki/01-portal-and-modes\|Portal, AiKA Modes, and the Two Worker Modes]] | Portal AiKA modes and bulk-reader/code-writer configs for cheap I/O delegation. |
| [[wiki/02-shunt-routing\|Enforced Routing: the Shunt Plugin]] | How the shunt plugin enforces cheap-model delegation with hooks, scripts, and skills. |
| [[wiki/03-benchmarks-savings\|Benchmarks and the 90% Saving]] | Benchmarks on a Java monorepo showing ~90% mean Claude token saving for bulk reads. |
| [[wiki/04-limits-and-transfer\|Limits, Failure Modes, and Transferability]] | Limits and transfer: what cannot be delegated, latency costs, and reusable routing pattern. |
| [[wiki/targeted\|Targeted Analysis: the 90%, What Generalizes, What Got Worse]] | Targeted analysis decomposing the ~90% saving, generalizable routing pattern, and failure modes. |

## Original Source

- [source/article.md](source/article.md) — article text, retrieved 2026-09-12
- Original: https://engineering.atspotify.com/2026/9/portal-by-spotify-cut-my-claude-code-token-usage-by-90
