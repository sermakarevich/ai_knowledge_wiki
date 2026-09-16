---
type: Paper
title: The Anatomy of an Agent Harness
description: LangChain's derivation of the agent harness — Agent = Model + Harness — covering filesystems, bash execution, sandboxes, memory/search, context-rot defenses, Ralph Loops for long-horizon autonomy, and why task-optimized harnesses beat post-training harnesses.
generated: { by: claude/muse-spark-1.3-contributor, at: 2026-09-16T05:42:00Z }
sources:
  - id: original
    resource: https://www.langchain.com/blog/the-anatomy-of-an-agent-harness
  - id: local-copy
    resource: source/source.md
tags: [agent-harness, llm-agents, context-engineering, coding-agents, long-horizon-autonomy]
---

# The Anatomy of an Agent Harness

LangChain's Vivek Trivedy (March 10, 2026) defines the agent as model plus harness and derives each harness component — filesystem, code execution, sandboxes, memory, context-rot defenses, long-horizon loops — by working backwards from model limits. The payoff is empirical: a harness-only change lifted the authors' coding agent from Top 30 to Top 5 on Terminal Bench 2.0. This folder holds a 2-minute summary, a 10-minute digest, and deep wiki pages per article section.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~5 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

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
| [[wiki/01-the-anatomy-of-an-agent-harness\|The Anatomy of an Agent Harness]] | Harness definition, model limits, filesystem, bash/ReAct, sandboxes, memory/search, context rot, long-horizon autonomy (Ralph Loops, planning, verification) |
| [[wiki/02-the-coupling-of-model-training-and-harness-design\|The Coupling of Model Training and Harness Design]] | Post-training in the loop, overfitting to home harness, Terminal Bench 2.0 evidence, enduring value of task-optimized harnesses |

## Original Source

- [The Anatomy of an Agent Harness](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness) — LangChain Blog, Vivek Trivedy, March 10, 2026
- [source/source.md](source/source.md) — local copy of the article text
