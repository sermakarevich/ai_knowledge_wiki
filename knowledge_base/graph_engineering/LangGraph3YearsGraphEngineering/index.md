---
type: Article
title: 3 Years of Graph Engineering with LangGraph
description: LangChain's founders argue that graphs are the right way to encode an agent's predictable structure while leaving room for model judgment, and that after three years of production use, agent graphs are usually cyclic, loops are just a simple case of graphs, and dynamic fan-out (Send) is essential — while insisting "graph engineering" itself is not a new idea.
generated: { by: claude/claude-sonnet-5, at: 2026-08-18T06:20:00Z }
sources:
  - id: original
    resource: https://www.langchain.com/blog/3-years-of-graph-engineering-with-langgraph
  - id: local-copy
    resource: source/article.md
tags: [graph-engineering, langgraph, agent-architecture, loop-engineering, multi-agent]
---

# 3 Years of Graph Engineering with LangGraph

LangChain's Sydney Runkle and Harrison Chase use three years of building LangGraph to make a practical case for representing agents as graphs: nodes do work (code, an LLM call, or a full agent run), edges decide what happens next, and the graph fixes the parts of a workflow that are predictable while leaving the model free to reason where it actually adds value. They temper this with a boundary (some tasks are too open-ended for a graph and need an agent harness instead), three hard-won lessons from production (graphs are usually cyclic, loops are a simple case of graphs, and dynamic transitions like `Send` are essential), and a closing claim that "graph engineering" is not a new trend but the latest name for a decades-old discipline of putting model reasoning in the right place.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~5 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

_New to agent architecture? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

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
| [[wiki/01-modeling-agents-as-graphs\|Modeling Agents as Graphs]] | Why a graph is a useful state-machine representation of an agent, and when real-world workflow structure should be encoded that way |
| [[wiki/02-when-not-to-use-graphs\|When Not to Use Graphs]] | The boundary case — open-ended tasks like deep research that resist a predefined graph and are better served by an agent harness (Deep Agents) |
| [[wiki/03-lessons-from-three-years\|Lessons from Three Years]] | Three production lessons: agent graphs are usually cyclic, loops are a simple form of graph, and dynamic transitions (`Send`) are essential |
| [[wiki/04-whats-new-and-the-bigger-idea\|What's Actually New, and the Bigger Idea]] | What genuinely changed (nodes can now be full agents) versus the claim that graph engineering itself is just the latest name for an old idea |

## Original Source

- [source/article.md](source/article.md) — article text, retrieved 2026-08-18
