---
type: Paper
title: "Design Docs Are All You Need: An AI-native Machine-Learning Performance Tool"
description: SMART regenerates a symbolic ML performance-modeling library from scratch from a DAG of worked-example design docs on every version update, reproducing hand-audited references to round-off precision.
generated: { by: claude/muse-spark-1.3, at: 2026-09-08T11:30:00Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2609.05364
  - id: local-copy
    resource: source/2609.05364.pdf
tags: [performance-modeling, ai-coding-agents, design-docs, symbolic-cost-model, tpu]
---

# Design Docs Are All You Need: An AI-native Machine-Learning Performance Tool

A 5-page paper (Kushnir et al., Google DeepMind / MIT / Stanford / Google, arXiv:2609.05364, Sep 2026) arguing that for fast-churn domains like ML performance modeling, natural-language design docs — not code — should be the durable artifact: coding subagents regenerate the whole SMART symbolic cost-modeling library from ~50 worked-example docs on every version update, reproducing hand-audited references (DeepSeekV3 serving on a TPU pod slice) to round-off precision.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~10 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

_New to performance modeling or agentic code regeneration? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

## Read This Folder

- [[summary|Summary]] — rung 1: the whole paper, shallow
- [[digest|Digest]] — rung 2: the whole paper at medium depth; the file to re-read on review
- [[explainer|Plain-Language Explainer]] — no-jargon explanation, applications, conclusions
- [[critical_thinking|Critical Analysis]] — claims vs. evidence, applicability, what it changes
- [[questions|Retrieval Practice]] — self-test questions; **answer these from memory before re-reading anything**
- [[connections|Connections]] — related entries in this knowledge base

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-motivation-and-regeneration-workflow\|Motivation and Regeneration Workflow]] | Churn from both stack directions, incremental generation debt (Eq. 1), context-window myopia, Figure 1 regeneration loop |
| [[wiki/02-design-docs-as-source-of-truth\|Design Docs as Source of Truth]] | Doc DAG with machine-discovered edges, orchestrator + per-doc subagents, log-guided doc refinement, cost/speed, worked-example doctrine, reconciliation anchors |
| [[wiki/03-symbolic-ir-and-builder-dsl\|Symbolic IR and Builder DSL]] | Recursive Op abstraction, TPU leaf ops, tracing DSL, flash-attention Listing 1, sharding-annotated distribution, DeepSeekMoE block |
| [[wiki/04-rollup-modes-validation-conclusion\|Roll-up Modes, Validation, Conclusion]] | Fast roofline-style vs slow modulo-scheduling roll-up, SymPy edge-bound propagation, round-off validation, 50-doc scale, generalization bet |

## Original Source

- [source/2609.05364.pdf](source/2609.05364.pdf) — Paper PDF, retrieved 2026-09-08
