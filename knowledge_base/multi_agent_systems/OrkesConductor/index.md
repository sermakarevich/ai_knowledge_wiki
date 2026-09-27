---
type: Article
title: Orkes Conductor Documentation Hub
description: Durable workflow orchestration engine (Netflix Conductor lineage) — principles, core abstractions, operators, events, design patterns, and AI-agent orchestration.
generated: { by: opencode/muse-spark, at: 2026-09-08T12:45:00Z }
sources:
  - id: original
    resource: https://www.orkes.io/content/
  - id: local-copy
    resource: source/sources.md
tags: [orchestration, durable-execution, agents, microservices]
---

# Orkes Conductor Documentation Hub

The technical docs behind the "Agentic Workflow Engine": how Conductor runs microservice processes and AI-agent work as persisted, event-driven task graphs — and why that single substrate covers retries, sagas, human approvals, LLM calls, and tool use with identical semantics.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every page's headline and key points.
3. **Wiki pages below** (~10 min each) — one topic, deep. Each opens with its headline and key points, so you can stop early.

_New to the field? Start with [[explainer|the plain-language explainer]] instead. Asked for the framework's principles, patterns, and abstractions specifically? Read [[wiki/targeted|the targeted brief]] — it answers that question directly. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

## Read This Folder

- [[summary|Summary]] — rung 1: the whole source, shallow
- [[digest|Digest]] — rung 2: the whole source at medium depth; the file to re-read on review
- [[explainer|Plain-Language Explainer]] — no-jargon explanation, applications, conclusions
- [[wiki/targeted|Targeted Brief]] — the user's question answered directly: framework, principles, design patterns, abstractions
- [[critical_thinking|Critical Analysis]] — claims vs. evidence, applicability, what it changes, verdict
- [[questions|Retrieval Practice]] — self-test questions; **answer these from memory before re-reading anything**
- [[connections|Connections]] — related entries in this knowledge base

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-overview-and-principles\|Overview and Principles]] | What Conductor is, OSS vs Orkes editions, architecture split, guiding principles |
| [[wiki/02-core-abstractions\|Core Abstractions]] | Workflow definition vs execution, task types, workers, data wiring, versioning |
| [[wiki/03-operators-and-system-tasks\|Operators and System Tasks]] | Flow-control operators and server-executed system tasks with semantics |
| [[wiki/04-event-driven-and-integrations\|Event-Driven and Integrations]] | Event handlers, brokers, webhooks, schedules, signals, gateways |
| [[wiki/05-design-patterns\|Design Patterns]] | Microservice orchestration, saga, parallelism, polling, timeouts/retries |
| [[wiki/06-agents-and-ai-orchestration\|Agents and AI Orchestration]] | AI tasks, Conductor Agents, A2A, guardrails, evals, human-in-the-loop |
| [[wiki/targeted\|Targeted Brief]] | Framework + principles + patterns + abstractions in one place |

## Original Source

- [source/sources.md](source/sources.md) — provenance pin (docs-hub URL, retrieval date, page inventory), retrieved 2026-09-08
