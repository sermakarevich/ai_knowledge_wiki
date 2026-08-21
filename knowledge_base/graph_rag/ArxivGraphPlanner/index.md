---
type: Paper
title: "GraphPlanner: Graph Memory-Augmented Agentic Routing for Multi-Agent LLMs"
description: A heterogeneous graph memory network (GARNet) plus PPO trains a single lightweight router to jointly pick agent role and LLM backbone at every step of a multi-agent workflow, beating single- and multi-round routers on accuracy, cost, and generalization.
generated: { by: claude/sonnet, at: 2026-08-21T10:41:00Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2604.23626
  - id: local-copy
    resource: source/2604.23626.pdf
tags: [agentic-graphrag, multi-agent-llm, llm-routing, reinforcement-learning, graph-neural-network]
---

# GraphPlanner: Graph Memory-Augmented Agentic Routing for Multi-Agent LLMs

GraphPlanner reframes LLM routing as *agentic workflow generation*: instead of assigning a query to one model once (single-round) or interleaving calls without modeling collaboration (multi-round), it casts routing as a Markov Decision Process in which a policy network — GARNet, a heterogeneous graph neural network fusing a per-query workflow graph with a cross-episode historical-memory graph — jointly selects both an agent role (Planner/Executor/Summarizer) and an LLM backbone at every step, trained end-to-end with PPO. It was worth ingesting because it sits at the intersection of three active KB threads — agentic GraphRAG, LLM routing, and graph-structured agent memory — and reports the strongest generalization numbers (78% zero-shot accuracy on unseen tasks) and lowest training cost (1.04 GiB GPU) of any router surveyed so far.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~10-15 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

_New to agentic routing or graph neural memory? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

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
| [[wiki/01-problem-and-preliminaries\|Problem, Motivation & Preliminaries]] | Why agentic routing needs a new paradigm; single-round vs. multi-round vs. agentic router formalization (Abstract, §1, §2) |
| [[wiki/02-graphplanner-method\|GraphPlanner Method]] | The MDP formulation, GARNet heterogeneous graph policy network, PPO training (§3) |
| [[wiki/03-experiments-and-results\|Experiments, Results & Conclusion]] | 14 tasks / 6 domains, Phase 1/2 results, Pareto frontier, ablations, conclusion (§4, §5) |
| [[wiki/04-related-work-and-implementation\|Related Work & Implementation Details]] | Extended related work, PPO/GARNet hyperparameters, dataset & LLM backbone catalog (App. A–D) |
| [[wiki/05-additional-ablations-and-generalization\|Additional Ablations & Generalization]] | New agentic roles, alternative graph encoders, LLM-based history baselines, unseen AIME dataset, time-cost comparison (App. E–J) |
| [[wiki/06-prompt-templates-and-examples\|Prompt Templates & Worked Examples]] | Verbatim Planner/Executor/Summarizer/Thinker/Verifier prompts and three fully-traced workflow examples (App. K) |

## Original Source

- [source/2604.23626.pdf](source/2604.23626.pdf) — PDF, retrieved 2026-08-21
