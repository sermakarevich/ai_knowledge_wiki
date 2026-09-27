---
type: Article
title: Loops vs. Graphs
description: Prefect's Jeremiah Lowin and Radhika Gulati argue agent engineering is moving from prompts to loops to "directed agentic graphs" — cycles allowed, per-node config — mainly for security via capability segregation, with Prefect positioning itself as the macro-orchestration layer above LangGraph/Pydantic AI.
generated:
  by: claude/sonnet
  at: 2026-08-18T09:10:00Z
sources:
  - id: original
    resource: https://www.prefect.io/blog/loops-vs-graphs
  - id: local-copy
    resource: source/page.html
tags: [agent-engineering, graph-engineering, orchestration, prefect]
---

# Loops vs. Graphs

A company blog post (Prefect, July 2026) arguing that agent engineering is progressing through three stages — prompt engineering, loop engineering, and now graph engineering — and that Prefect's "directed agentic graph" (a graph that, unlike a traditional DAG, permits cycles, with per-node tools/model/access config) is the right structure for businesses that need reproducibility, auditability, and security. The piece is explicitly a response to a viral "loops or graphs?" tweet, and it doubles as a strategy statement tying together Prefect's own agent runtime and its recent Dagster acquisition.

## How to work through this

1. **2 minutes:** read `summary.md` for the whole argument at a glance.
2. **10 minutes:** read `digest.md` for the key points of both chunks plus the article's five-move arc.
3. **As needed:** read the two `wiki/` pages for full detail — page 1 covers the graph/loop conceptual setup, page 2 covers security, human-in-the-loop design, and Prefect's competitive/strategic framing.
4. **Going deeper:** `explainer.md` for plain-language definitions of the jargon, `questions.md` to test retention, `critical_thinking.md` for a skeptical read (this is vendor marketing), `connections.md` for how this fits with other graph-engineering sources already in the KB.

## Read This Folder

- [[summary]] — shallow, whole-article pass
- [[digest]] — medium-depth pass, section-by-section key points
- [[explainer]] — plain-language layer with jargon decoder
- [[questions]] — retrieval-practice questions
- [[critical_thinking]] — skeptical review (claims vs. evidence, vendor bias, blind spots)
- [[connections]] — links to related KB entries

## Wiki Pages

| Page | Covers |
|---|---|
| [[wiki/01-directed-agentic-graphs\|01 — Directed Agentic Graphs]] | Graph fundamentals, the prompt→loop→graph progression, the "Ralph loop," Prefect's definition of a directed agentic graph, why businesses need reproducibility, and the control-vs-autonomy tension. |
| [[wiki/02-security-humans-and-strategy\|02 — Security, Humans, and Strategy]] | Capability segregation as the strongest case for graphs, humans-in-the-loop as ordinary nodes, how this differs from LangGraph/Pydantic AI, the tweet that prompted the piece, and Prefect's Dagster-backed strategic bet. |

## Original Source

[Loops vs. Graphs](https://www.prefect.io/blog/loops-vs-graphs) — Prefect blog, 2026-07-22
