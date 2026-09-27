---
type: Article
title: 'Harness Engineering: Leveraging Codex in an Agent-First World'
description: OpenAI's field report on shipping a real product with zero hand-written code via Codex agents, and the harness discipline that made it work.
generated: { by: claude/opencode, at: 2026-09-21T09:30:00Z }
sources:
  - id: original
    resource: https://openai.com/index/harness-engineering/
  - id: local-copy
    resource: source/article.txt
tags: [agents, codex, harness-engineering, developer-productivity]
---

# Harness Engineering: Leveraging Codex in an Agent-First World

OpenAI engineering post (Ryan Lopopolo, Feb 11 2026) reporting a five-month experiment: a small team shipped an internal-beta product with zero manually-written code, all ~1M lines via Codex agents. Worth ingesting as the clearest vendor-side playbook for the harness pattern: environment design, agent-legible knowledge, enforced architecture, and automated quality collection.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every chapter's headline and key points.
3. **Wiki pages below** (~5 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

_New to the field? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

## Read This Folder

- [[summary|Summary]] — rung 1: the whole source, shallow
- [[digest|Digest]] — rung 2: the whole source at medium depth; the file to re-read on review
- [[explainer|Plain-Language Explainer]] — no-jargon explanation, applications, conclusions
- [[critical_thinking|Critical Analysis]] — claims vs. evidence, applicability, what it changes, verdict
- [[questions|Retrieval Practice]] — self-test questions; **answer these from memory before re-reading anything**

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-zero-hand-written-code-experiment\|The Zero-Hand-Written-Code Experiment]] | Experiment setup, headline numbers, and the redefined engineer role |
| [[wiki/02-application-legibility\|Making the Application Legible to Agents]] | Per-worktree instances, CDP browser control, ephemeral observability |
| [[wiki/03-repository-knowledge-system-of-record\|Repository Knowledge as the System of Record]] | AGENTS.md-as-map, docs/ layout, plans, doc-gardening, agent legibility |
| [[wiki/04-architecture-taste-throughput\|Enforcing Architecture and Taste]] | Layered domains, Providers, teaching linters, merge philosophy |
| [[wiki/05-autonomy-entropy-learnings\|Autonomy, Entropy, and What Comes Next]] | Agent-generated surface, autonomy loop, garbage collection, open questions |

## Original Source

- [OpenAI blog post](https://openai.com/index/harness-engineering/) — Engineering, Feb 11 2026, by Ryan Lopopolo
- [source/article.txt](source/article.txt) — article text, local copy
