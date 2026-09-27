---
type: Paper
title: Agentic ML Exploration (A-MLE) for Ads Ranking
description: Meta's autonomous LLM-agent system that runs the full ML iteration loop across production ads ranking models, with HITL gates and a shared knowledge substrate.
generated: { by: claude/muse-spark-1.3-contributor, at: 2026-09-11T07:00:00Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2609.08248
  - id: local-copy
    resource: source/2609.08248.pdf
tags: [agents, ml-engineering, recommenders, ads-ranking, automl]
---

# Agentic ML Exploration (A-MLE) for Ads Ranking

Meta (Gao et al., Sept 2026) reframes industrial ads-ranking progress as a
throughput problem -- human ML iteration, not model capacity -- and builds a
single agent that walks five gated stages over a shared skill library and
sandbox. Worth ingesting: the tiered L1/L2/L3 evaluation, the cross-LLM
study, and the REA production mapping in the targeted analysis.

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
| [[wiki/01-manual-iteration-bottleneck\|The Manual ML-Iteration Bottleneck]] | Manual-iteration bottleneck: why human cycle throughput across dozens of models limits ads ranking progress. |
| [[wiki/02-five-stage-system\|The Five-Stage A-MLE System]] | Five-stage A-MLE loop: gated hypothesis→strategy→execution→analysis over a shared substrate with HITL checkpoints. |
| [[wiki/03-tiered-evaluation\|Experimental Setup and Tiered Evaluation]] | Setup plus L1/L2/L3 tiered evaluation with Table 1 (+2.56%, +0.42% QPS). |
| [[wiki/04-cross-llm-study\|Cross-LLM Study and Agent-Surfaced Techniques]] | Cross-LLM study (L2/L3 by model and prompt stress) plus agent-surfaced technique families and transfer wins. |
| [[wiki/05-failure-modes-and-outlook\|Failure Modes, Design Lessons, and Outlook]] | Failure modes, harness-over-model lesson, and future outlook for A-MLE. |
| [[wiki/targeted\|Targeted Analysis]] | The five stages as a loop, sandbox+HITL reliability, A-MLE↔REA mapping, failure modes and senior-engineer limits. |

## Original Source

- [source/2609.08248.pdf](source/2609.08248.pdf) — PDF, retrieved 2026-09-11
- Companion: [REA engineering article](https://engineering.fb.com/2026/03/17/developer-tools/ranking-engineer-agent-rea-autonomous-ai-system-accelerating-meta-ads-ranking-innovation/) — Meta Engineering, 2026-03-17
