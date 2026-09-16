---
type: Article
title: "Agent Harness Engineering"
description: Addy Osmani synthesizes harness engineering — agent = model + harness, the ratchet (every failure becomes a permanent rule), context-rot defences, Ralph Loops, generator/evaluator splits, and the shift to Harness-as-a-Service SDKs.
generated: { by: claude, at: 2026-09-12T06:50:00Z }
sources:
  - id: original
    resource: https://addyosmani.com/blog/agent-harness-engineering/
  - id: local-copy
    resource: source/full.md
tags: [agent-harness, coding-agents, context-management, verification, harness-as-a-service]
---

# Agent Harness Engineering

Addy Osmani's synthesis of "harness engineering" (Viv Trivedy's term): a coding agent is the model plus everything built around it, and most of what makes an agent good or bad is that scaffolding, not the model. Covers the ratchet discipline, working backwards from behaviour, filesystem/bash/sandbox primitives, context-rot defences, long-horizon execution (Ralph Loops, generator/evaluator splits), hooks, and the shift toward Harness-as-a-Service SDKs.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~5 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

_New to the topic? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

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
| [[wiki/01-foundations-behaviour\|Foundations: what a harness is, ratchet, behaviour-first]] | Agent = model + harness, layers of a harness, the "skill issue" reframe, the ratchet, working backwards from behaviour |
| [[wiki/02-primitives-production\|Primitives and production: filesystem to HaaS]] | Filesystem/Git, bash/ReAct loop, sandboxes, memory, context-rot defences, Ralph Loops, hooks, AGENTS.md/tool-count discipline, Claude Code production proof, Harness-as-a-Service |

## Original Source

- [source/full.md](source/full.md) — full article text, retrieved from https://addyosmani.com/blog/agent-harness-engineering/
