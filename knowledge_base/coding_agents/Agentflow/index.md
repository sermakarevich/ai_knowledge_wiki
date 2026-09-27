---
type: Codebase
title: Agentflow
description: Programmatic Python graph orchestration for codex/claude/kimi agents — fanout, merge, LGTM cycles, SSH/EC2/ECS execution — contrasted with fleet's queue model.
generated: { by: claude/opencode, at: 2026-09-09T21:10:00Z }
sources:
  - id: original
    resource: https://github.com/abt0y/agentflow
  - id: local-copy
    resource: source/source.md
tags: [agents, orchestration, graphs, fanout, remote-execution]
---

# Agentflow

Agentflow (`abt0y/agentflow`, v0.1.0) is a programmatic Python framework for running AI coding agents as dependency graphs: fan out dozens of parallel workers, merge their outputs with reducers, loop write→review until LGTM, and run nodes remotely on SSH/EC2/ECS. Its DAG (Directed Acyclic Graph — a workflow with no loops, plus explicit cycle edges) paradigm contrasts with fleet's queue model, and the comparison yields concrete borrowable ideas.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every component's headline and key points.
3. **Wiki pages below** (~5 min each) — one component, deep. Each opens with its headline and key points, so you can stop early.

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
| [[wiki/01-graph-dsl\|Graph DSL]] | Graph context manager, fanout/merge primitives, Jinja templating, 94-node pipeline |
| [[wiki/02-orchestration-engine\|Orchestration engine]] | Scheduling, concurrency, success checks, retries/cycles, state persistence |
| [[wiki/03-agent-harness\|Agent harnesses]] | codex/claude/kimi node constructors, tools knob, context isolation, skills |
| [[wiki/04-remote-execution\|Remote execution]] | SSH/EC2/ECS runners, shared-instance reuse, auto-discovery, AWS prerequisites |
| [[wiki/05-merge-and-cli\|Merge reducers and CLI]] | Batch vs group reducers, branch isolation, run/inspect/doctor surface |
| [[wiki/targeted\|Targeted: graph vs fleet queue]] | Fleet comparison — six questions plus 5-8 borrowable workflow ideas |

## Original Source

- [source/source.md](source/source.md) — provenance pin (commit 1afc32ce70a4bbbe3058d51a9743b8b13302478c, 2026-03-31), retrieved 2026-09-09
- [wiki/images/graph-94-node-pipeline.png](wiki/images/graph-94-node-pipeline.png) — 94-node pipeline figure from the repo docs
