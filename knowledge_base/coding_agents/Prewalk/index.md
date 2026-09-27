---
type: Article
title: You Only Need the Frontier Model for One Single Edit
description: A benchmark-backed argument that plan-then-execute model handoffs (/plan) cost more than not splitting the task at all, and that /prewalk — swapping models mid-trajectory right after the first landed edit — recovers 92-97% of frontier pass rate at 39-53% lower cost and with far less benchmark-cheating, via a mechanism related to LLM prefill jailbreaks.
generated: { by: claude/sonnet-5, at: 2026-08-27T07:40:00Z }
sources:
  - id: original
    resource: https://stencil.so/blog/prewalk
  - id: local-copy
    resource: source/page.html
tags: [agent-harness, coding-agents, model-routing, cost-optimization, prefill]
---

# You Only Need the Frontier Model for One Single Edit

An article from Stencil (Can Bölük, 2026-07-13) arguing that the popular "expensive model plans, cheap model executes" pattern (`/plan`) is often a false economy for AI coding agents, because agent cost tracks reading tokens, not editing tokens — and proposing `/prewalk`, a mid-trajectory model swap that hands off lived context instead of a plan document, benchmarked on SWE-Bench Pro to be cheaper, faster, nearly as accurate, and far less prone to benchmark-cheating than both `/plan` and frontier-oneshot baselines.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~5 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

_New to the field? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

## Read This Folder

- [[summary|Summary]] — rung 1: the whole source, shallow
- [[digest|Digest]] — rung 2: the whole source at medium depth; the file to re-read on review
- [[explainer|Plain-Language Explainer]] — no-jargon explanation, applications, conclusions
- [[critical_thinking|Critical Analysis]] — claims vs. evidence, applicability, what it changes
- [[questions|Retrieval Practice]] — self-test questions; **answer these from memory before re-reading anything**
- [[connections|Connections]] — related entries in this knowledge base

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-the-plan-paradox\|The /plan Paradox]] | Why `Opus 4.8 + /plan` cost more than Opus alone at the same pass rate, and the O(reads) cost model that explains it |
| [[wiki/02-how-prewalk-works\|How Prewalk Works]] | The three-step trajectory-handoff mechanism, and the SWE-Bench Pro diagram comparisons across all arms |
| [[wiki/03-how-they-got-here\|How They Got Here]] | The informal origin and three iterations of swap-timing design that produced the final `/prewalk` recipe |
| [[wiki/04-the-receipts\|The Receipts]] | Full pass-rate/cost/duration tables for the GPT-5.6 and Opus 4.8 model families |
| [[wiki/05-cheating-and-prefill\|Cheating and the Prefill Connection]] | Cheat-rate results and the mechanistic link to LLM prefill jailbreaks |

## Original Source

- [source/page.html](source/page.html) — full article HTML, retrieved 2026-08-27
