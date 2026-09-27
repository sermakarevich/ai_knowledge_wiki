---
type: Paper
title: Auto-RecSys
description: Meta's autonomous research harness for industry-scale recommender systems — distributed async execution, centralized cross-server memory, and cognitive-procedural separation drive a dual-loop self-evolving architecture that cut operational fixes from 4.0 to 0.5 per iteration.
generated: { by: claude/claude-sonnet-5, at: 2026-09-12T15:11:57Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2609.10922
  - id: local-copy
    resource: source/full.md
tags: [agent-harness, autonomous-research, recommender-systems, self-evolution, long-horizon-agents]
---

# Auto-RecSys

Auto-RecSys is an autonomous research system Meta built for long-horizon experimentation on industry-scale recommendation models, where a single training run takes days and infrastructure is fragile. It was worth ingesting because it's a rare production (not benchmark) account of what an auto-research harness looks like when feedback loops are measured in days rather than minutes, and because its dual self-evolving loops (execution playbooks + idea portfolio) give a concrete pattern for turning recurring operational failures into durable, natural-language institutional knowledge.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every chapter's headline and key points.
3. **Wiki pages below** (~5 min each) — one topic, deep. Each opens with its headline and key points, so you can stop early.

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
| [[wiki/01-overview-state-machine\|Overview and experiment state machine]] | Why serial auto-research breaks at industry scale, the three harness designs, and the per-idea state machine |
| [[wiki/02-evolution-loops\|Execution and idea evolution loops + persistence]] | Per-model playbooks, dead-end self-healing, ideation grounding, and the centralized persistence layer |
| [[wiki/03-evaluation\|Evaluation, related work, outlook]] | The 31-iteration fix-rate result, categorical errors, positioning against other auto-research systems, and future work |

## Original Source

- [source/full.md](source/full.md) — article text, retrieved 2026-09-12
