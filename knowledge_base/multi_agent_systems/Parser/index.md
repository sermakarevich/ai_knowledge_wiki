---
type: Paper
title: "PARSER: Read in Parallel, Reason in Depth for Long-Context LLM Agents"
description: Parallel chunk-bound subagents plus a Reinforcement Learning trained lead agent that reasons through iterative scatter-gather rounds, holding accuracy flat to 896K tokens.
generated: { by: claude/muse-spark-1.3-contributor, at: 2026-09-11T07:00:00Z }
sources:
  - id: original
    resource: https://arxiv.org/html/2609.06702
  - id: local-copy
    resource: source/2609.06702.pdf
tags: [agents, long-context, multi-hop-qa, reinforcement-learning]
---

# PARSER: Read in Parallel, Reason in Depth for Long-Context LLM Agents

PARSER (Parallel Reading, Sequential Reasoning) is a September 2026 paper from The Chinese University of Hong Kong that splits long-document Question Answering (QA, questions that need combining facts from several places) into parallel reading by frozen chunk-bound subagents and deep reasoning by a Reinforcement Learning (RL, improving behavior from reward signals) trained lead agent. Its central claim: on multi-hop QA from 7K to 896K tokens, accuracy stays nearly flat while sequential-memory and full-context baselines degrade sharply. Worth ingesting as a candidate architecture for agentic reading over very long evidence.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every page's headline and key points.
3. **Wiki pages below** (~5 min each) — one topic, deep. Each opens with its headline and key points, so you can stop early.

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
| [[wiki/01-problem-and-motivation\|Problem and Motivation]] | Motivation for parallel reading: context rot, sequential-memory limits, and prior work. |
| [[wiki/02-scatter-gather-method\|Scatter-Gather Method]] | Scatter-gather loop with parallel frozen chunk readers and question-only lead-agent reasoning. |
| [[wiki/03-training-lead-agent\|Training the Lead Agent]] | Lead-agent Reinforcement Learning setup, data, dynamics, and ablations. |
| [[wiki/04-experiments-results\|Experiments and Results]] | HotpotQA and 2WikiMultiHopQA results with full Table 1 values, baselines, and out-of-distribution stability. |
| [[wiki/05-analysis-limits\|Analysis, Cost, and Limits]] | Controlled evidence-distribution tests, latency, complexity, subagent ablations, and failure case. |
| [[wiki/targeted\|Targeted Analysis]] | Four deep-dive answers: round mechanics, frozen-reader training, 896K wins, subagent-bank costs. |

## Original Source

- [source/2609.06702.pdf](source/2609.06702.pdf) — PDF, retrieved 2026-09-11
- [arXiv HTML](https://arxiv.org/html/2609.06702) — canonical readable version
