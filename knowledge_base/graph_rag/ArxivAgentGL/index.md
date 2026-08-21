---
type: Paper
title: AgentGL: Towards Agentic Graph Learning with LLMs via Reinforcement Learning
description: An RL-trained LLM agent that treats graph learning as topology-aware navigation with graph-native search tools, beating GraphLLM and GraphRAG baselines by up to 17.5% (node classification) and 28.4% (link prediction).
generated: { by: claude/claude-sonnet-5, at: 2026-08-21T06:07:54Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2604.05846
  - id: local-copy
    resource: source/paper.pdf
tags: [graph-learning, llm-agents, reinforcement-learning, graphrag, text-attributed-graphs]
---

# AgentGL: Towards Agentic Graph Learning with LLMs via Reinforcement Learning

AgentGL (Sun, Li, Fan, Liu, Tan; NYU Shanghai / NYU / Tsinghua, 2026) reformulates graph learning as an agentic, RL-optimized navigation process over Text-Attributed Graphs (TAGs), rather than treating graph context as flat text stuffed into a prompt (as GraphLLMs and GraphRAG do). An LLM agent is equipped with four graph-native search tools, trained with a two-stage RL curriculum to first learn to navigate and then to stop over-searching, and it outperforms GNN, GraphLLM, GraphRAG, and standard agentic-search baselines across 7 datasets and two Qwen backbones. Worth ingesting because it is a clean, RL-native answer to "why treat a graph as text at all" in the current agentic-GraphRAG landscape.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every chapter's headline and key points.
3. **Wiki pages below** (~10 min each) — one chapter, deep. Each opens with its headline and key points, so you can stop early.

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
| [[wiki/01-motivation-and-related-work\|Motivation and Related Work]] | Why agentic reasoning ignores graph topology, the AGL paradigm, and the contrast with GraphLLMs/GraphRAG (source pages 1-3) |
| [[wiki/02-agentgl-method\|The AgentGL Method]] | The four GNS tools, search-constrained thinking, GCCL curriculum, and the two-stage RL objective (source pages 3-6) |
| [[wiki/03-experiments-results-and-conclusion\|Experiments, Results, and Conclusion]] | Datasets, baselines, main results table, ablations, conclusion and limitations (source pages 6-9) |
| [[wiki/04-appendix-datasets-and-implementation\|Appendix: Datasets, Implementation, and Case Study]] | Dataset details, AGL-vs-GraphRAG framing, full hyperparameters/reward engineering, K-sensitivity, case studies (source pages 12-15) |

## Original Source

- [source/paper.pdf](source/paper.pdf) — PDF, retrieved 2026-08-21
