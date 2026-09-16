---
type: Article
title: How to Build a Custom Agent Harness
description: LangChain blog post arguing agent = model + harness, presenting create_agent as a deliberately minimal harness primitive with composable middleware (four levers, ~8 capability groups) as the customization surface, and task-harness fit as the design goal over adopting a fixed pre-assembled harness.
generated: { by: claude, at: 2026-09-13T12:19:00Z }
sources:
  - id: original
    resource: https://www.langchain.com/blog/how-to-build-a-custom-agent-harness
  - id: local-copy
    resource: source/full.md
tags: [agent-harness, middleware, langchain, create_agent, task-harness-fit]
---

# How to Build a Custom Agent Harness

An agent is a model plus a task-fitted harness, and the harness's job is delivering the right context at every step. LangChain's `create_agent` implements only the minimal core loop (model, tools, system prompt), exposing composable middleware — hooking in before/after model and tool calls, at startup and teardown — as the single primitive for all customization. Middleware works through four levers (deterministic logic, tool lifecycle, custom state, stream handlers), and production agents stack capability groups (context management, memory, action/delegation, reliability, policy/steering, cost control) chosen by how long-lived, complex, and sensitive the task is. The article's thesis is task-harness fit: start minimal, add only what the specific task demands.

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
| [[wiki/01-base-middleware|create_agent base and middleware customization]] | base harness + middleware |
| [[wiki/02-capabilities-fit|Harness capabilities and task-harness fit]] | capabilities + fit |

## Source

- [[source/full|Local copy of the full article]]
