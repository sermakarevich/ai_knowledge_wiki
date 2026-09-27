---
type: Paper
title: What Does Context Compression Cost an Agent? Interaction Costs Unrevealed by Task-Completion Metrics
description: A controlled study showing task completion is a non-identifying projection of context compression's true cost — compression can substantially raise an agent's tool-call reacquisition cost while completion stays statistically unchanged.
generated: { by: claude/claude-sonnet-5, at: 2026-08-26T00:00:00Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2608.16370
  - id: local-copy
    resource: source/2608.16370.pdf
tags: [context-compression, agent-evaluation, interaction-cost, tool-use, benchmarking]
---

# What Does Context Compression Cost an Agent? Interaction Costs Unrevealed by Task-Completion Metrics

This is a controlled empirical study, not a compression benchmark: it asks a fifth question about context compression that prior work misses — not "does completion survive compression" but "what does the agent have to do, and what does that cost, when execution-relevant state is actually gone." Using a deterministic tool-using environment with a fixed interaction horizon, the single author (Shuyu Liu) shows that compression can triple an agent's retrieval tool calls (state reacquisition) while its task-completion rate stays statistically unchanged — a gap formalized as a non-identifiability result and then demonstrated causally through oracle state-restoration and retention-content interventions. It was worth ingesting because it directly targets a blind spot in how agentic systems (including harness and memory-management design) are evaluated: passing a completion benchmark does not certify that a compression strategy is cheap to run.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~10-15 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

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
| [[wiki/01-introduction-and-related-work\|Introduction & Related Work]] | The gap between retention and reacquisition; the paper's three contributions; four-category map of prior compression evaluation work |
| [[wiki/02-method\|Method]] | The Y = (Q, C_R, C_E) evaluation triple, Proposition 1, IRBench environment, context conditions (Sliding/Summary/Oracle), retention-intervention design |
| [[wiki/03-experiments-and-results\|Experiments & Results]] | Severity sweep, operator contrast, oracle intervention, three-model replication, retention-content interventions, ALFWorld boundary probe |
| [[wiki/04-discussion-and-limitations\|Discussion & Limitations]] | Mechanism synthesis (D vs. R recoverability), runtime-design implications, model/regime/environment boundary conditions, 11 stated limitations |

## Original Source

- [source/2608.16370.pdf](source/2608.16370.pdf) — arXiv PDF, retrieved 2026-08-26.
