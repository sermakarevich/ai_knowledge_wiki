---
type: Article
title: Honcho — Memory That Reasons (Plastic Labs)
description: Deep-dive on Honcho, the continual-learning memory layer for stateful agents powered by Neuromancer reasoning models.
generated: { by: claude/opencode-muse-spark, at: 2026-09-10T17:30:00Z }
sources:
  - id: original
    resource: https://honcho.dev/
  - id: local-copy
    resource: source/homepage.html
tags: [agent-memory, neuromancer, rag, evaluations]
---

# Honcho — Memory That Reasons (Plastic Labs)

Honcho (by Plastic Labs) is a continual-learning memory layer that lets AI agents stay consistent across sessions: instead of just storing facts, its custom Neuromancer models reason over every message with formal logic and maintain a living profile of each user or agent. Worth ingesting because it claims vendor-reported SOTA (State Of The Art) scores on the LongMemEval, LoCoMo, and BEAM memory benchmarks — and ships an open test harness so anyone can check.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every wiki page's headline and key points.
3. **Wiki pages below** (~5-15 min each) — one aspect, deep. Each opens with its headline and key points, so you can stop early.

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
| [[wiki/01-concepts\|Concepts]] | Core data-model primitives, representations, observation, scopes, config cascade |
| [[wiki/02-quickstart-integration\|Quickstart & Integration]] | SDK install, workspace/peer/session setup, chat, context, ecosystem |
| [[wiki/03-reasoning-architecture\|Reasoning Architecture]] | Neuromancer, Deriver/Dreamer/Dialectic, write/query paths, price tiers |
| [[wiki/04-evals\|Evaluations]] | LongMemEval-S, LoCoMo, BEAM scores with ablation and third-party tables |
| [[wiki/05-pricing-limits\|Pricing & Limits]] | Pricing tiers, operational limits, unit-economics example |
| [[wiki/06-comparisons\|Comparisons]] | mem0 vs Honcho API/migration, RAG, pgvector DIY, graph stores, decision guide |
| [[wiki/targeted\|Targeted Answers]] | The four deep questions: vs mem0/RAG, Neuromancer cost, eval baselines, build-vs-buy |

## Original Source

- [source/homepage.html](source/homepage.html) — homepage snapshot, retrieved 2026-09-10
- [source/reasoning.md](source/reasoning.md) — reasoning docs page, retrieved 2026-09-10
- [source/architecture.md](source/architecture.md) — architecture docs page, retrieved 2026-09-10
- [source/get-context.md](source/get-context.md) — get-context docs page, retrieved 2026-09-10
- [source/chat.md](source/chat.md) — chat endpoint docs page, retrieved 2026-09-10
- [source/quickstart.md](source/quickstart.md) — quickstart docs page, retrieved 2026-09-10
- [source/dreaming.md](source/dreaming.md) — dreaming docs page, retrieved 2026-09-10
- [source/representation.md](source/representation.md) — peer representation docs page, retrieved 2026-09-10
- [source/mem0-migration.md](source/mem0-migration.md) — mem0 migration guide, retrieved 2026-09-10
- GitHub org https://github.com/plastic-labs treated as provenance only (no repo-track analysis); docs.honcho.dev redirects to honcho.dev/docs (verified 2026-09-10). No eval figures were extracted: the docs diagrams are illustrative architecture sketches, described in words on the wiki pages instead.
