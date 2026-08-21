---
type: Paper
title: Schema-Agnostic Graph Reasoning Agent for Hybrid Knowledge Graphs
description: An agent with seven generic unix-style tools navigates a hybrid text+relational knowledge graph it has never seen, beating a full-context SQL baseline by 5.1pp on an industrial benchmark while reading under a third of the tokens.
generated: { by: claude/sonnet-5, at: 2026-08-21T05:30:00Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2608.15834
  - id: local-copy
    resource: source/paper.pdf
tags: [graph-rag, llm-agents, knowledge-graphs, tool-use, benchmarks]
---

# Schema-Agnostic Graph Reasoning Agent for Hybrid Knowledge Graphs

GRA (Graph Reasoning Agent) treats a hybrid knowledge graph — part text, part relational tables — the way a coding agent treats an unfamiliar repository: it explores with a handful of generic tools (`ls`, `cat`, `grep`, `sems`, `query`, `think`, `answer`) rather than being handed a schema up front. On UFK-M, a 258-question industrial benchmark, GRA beats a full-context baseline that serializes everything into the prompt by 5.1 percentage points (88.4% vs. 83.3%) while reading under a third of its input tokens. The paper also traces the gain to selective agentic access rather than graph structure itself, and shows GRA deployed inside a real factory rule-feasibility loop.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~5-10 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

_New to the field? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

## Read This Folder

- [[summary|Summary]] — rung 1: the whole paper, shallow
- [[digest|Digest]] — rung 2: the whole paper at medium depth; the file to re-read on review
- [[explainer|Plain-Language Explainer]] — no-jargon explanation, applications, conclusions
- [[critical_thinking|Critical Analysis]] — claims vs. evidence, applicability, what it changes, verdict
- [[questions|Retrieval Practice]] — self-test questions; **answer these from memory before re-reading anything**
- [[connections|Connections]] — related entries in this knowledge base

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-gra-agent-design\|GRA Agent Design]] | The code-agent-to-graph-agent analogy, related work, and the three agents (GRA/RSA/SQA) compared on one substrate |
| [[wiki/02-ufkm-benchmark\|UFK-M Benchmark]] | The synthetic factory benchmark, answer-first question generation, deterministic scoring, experimental setup |
| [[wiki/03-results\|Results]] | Accuracy across seven backbone models, tool reliability vs. reasoning, token usage, and the tool-call budget |
| [[wiki/04-industrial-deployment\|Industrial Deployment]] | GRA inside a factory rule-feasibility loop, two worked examples (refusal and acceptance), and the conclusion |

## Original Source

- [source/paper.pdf](source/paper.pdf) — PDF, retrieved 2026-08-21
