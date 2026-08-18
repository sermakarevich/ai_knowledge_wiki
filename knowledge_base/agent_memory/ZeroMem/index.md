---
type: Paper
title: "Zero-Mem: Zero-Token Memory Operations for LLM Agents"
description: A provenance-preserving agent-memory system that builds an entity-context graph and temporal hierarchy over raw interaction traces and answers queries via routing, dual-view retrieval, and deterministic calibration -- with zero LLM calls or tokens outside the final answer.
generated: { by: claude/claude-sonnet-5, at: 2026-08-04T09:53:39Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2607.29377
  - id: local-copy
    resource: source/2607.29377.pdf
tags: [agent-memory, retrieval, knowledge-graphs, llm-agents, efficiency]
---

# Zero-Mem: Zero-Token Memory Operations for LLM Agents

Zero-Mem is an agent-memory system that eliminates LLM calls from every memory operation except the final question-answering step. Instead of generating intermediate summaries or abstractions (the common approach in systems like A-Mem, Mem0, and LightMem), it organizes raw interaction traces into an entity-context graph and a temporal hierarchy, then answers queries through deterministic routing, dual-view retrieval, and calibration -- reaching the best average accuracy on LoCoMo and HotpotQA among 9 compared baselines while cutting memory-operation latency by 57.6% and consuming zero memory-operation tokens.

## How to work through this

Three depths -- stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) -- the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) -- the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~5-10 min each) -- one part of the method or results, deep. Each opens with its headline and key points, so you can stop early.

_New to the field? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] -- do not re-read the wiki._

## Read This Folder

- [[summary|Summary]] -- rung 1: the whole source, shallow
- [[digest|Digest]] -- rung 2: the whole source at medium depth; the file to re-read on review
- [[explainer|Plain-Language Explainer]] -- no-jargon explanation, applications, conclusions
- [[critical_thinking|Critical Analysis]] -- claims vs. evidence, applicability, what it changes, verdict
- [[questions|Retrieval Practice]] -- self-test questions; **answer these from memory before re-reading anything**
- [[connections|Connections]] -- related entries in this knowledge base

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-problem-motivation-and-related-work\|Problem, Motivation, and Related Work]] | The agent-memory problem, failure modes of generative-memory and raw-retrieval strategies, and positioning against SimpleMem, LightMem, A-Mem, Mem0, MemoryOS, CompassMem, GAM. |
| [[wiki/02-memory-substrate-and-structures\|The Token-Free Memory Substrate]] | Preliminaries plus the provenance-preserving substrate: Entity-Context Graph construction (edge-weight formula) and Temporal Hierarchy (turn/window/episode/session), plus BM25 + BGE-M3 indexing. |
| [[wiki/03-query-routing-retrieval-and-calibration\|Query-Conditioned Routing, Dual-View Retrieval, and Deterministic Calibration]] | Query-conditioned view weighting (ρ / 1-ρ), dual-view retrieval and evidence closure (graph bridges, local neighbors), and deterministic calibration (Filter/Rank/Extract/Calibrate) around the sole LLM call. |
| [[wiki/04-experiments-results-and-conclusion\|Experiments, Results, and Conclusion]] | Experimental setup (LoCoMo, HotpotQA, 9 baselines, two backbones), main results tables, efficiency comparison (zero tokens, 57.6% latency reduction), ablation study, retrieval-budget analysis, and conclusion. |

## Original Source

- [source/2607.29377.pdf](source/2607.29377.pdf) -- arXiv PDF, retrieved 2026-08-04
