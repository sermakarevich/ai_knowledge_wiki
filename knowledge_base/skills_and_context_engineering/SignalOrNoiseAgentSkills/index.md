---
type: Paper
title: "Signal or Noise? A Benchmark Study of Agent Skills in Web Development"
description: A controlled benchmark (WebDev-Skills-Bench) showing injected Agent Skills usually reduce Pass@2 and raise token cost in web-dev coding agents, with gains in only a minority of (Skill, project, model) triples.
generated: { by: claude/claude-sonnet-5, at: 2026-08-26T10:40:34Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2608.23067
  - id: local-copy
    resource: source/2608.23067.pdf
tags: [agent-skills, benchmarking, web-development, llm-agents, prompt-engineering]
---

# Signal or Noise? A Benchmark Study of Agent Skills in Web Development

Yang & Ding (Baidu NLP) build WebDev-Skills-Bench, a controlled study of whether injecting matched Agent Skills into a coding-agent session actually helps. Using four matched conditions — no Skill, target Skill, a length-matched irrelevant Skill, and a component ablation — across 31 public Skills, 50 Web-Bench projects, and four LLMs, the paper finds that target injection is on net harmful: lower Pass@2, lower Task Completion Depth, and 72–394% more tokens, with real gains in only a minority of cases. It's worth ingesting because it turns a widely-assumed-beneficial practice (attaching a Skill/cheat-sheet before every task) into an empirically conditional one, with a concrete mechanism (length distraction vs content misalignment) and a concrete fix (per-model, chain-position-aware routing).

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~10 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

_New to the field? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

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
| [[wiki/01-introduction-and-benchmark-design\|Introduction and Benchmark Design]] | Motivation, four matched conditions (C0-C3), the workspace-aware injection protocol, task/Skill corpus, routing methodology, Tables 1-2 |
| [[wiki/02-results-and-mechanisms\|Results and Mechanisms]] | Headline C1-C0 effects, easy-task retry lock-in, length vs content decomposition, cross-model decorrelation, C3 slice ablation, Figures 3-4 |
| [[wiki/03-implications-and-conclusion\|Implications and Conclusion]] | Injection as an opt-in routing decision, chain-position evaluation, per-model curation, limitations |
| [[wiki/04-appendices-worked-examples\|Appendices: Worked Examples and Protocol Detail]] | Retry-lock-in trace, content-driven-win trace, cross-model sign-reversal trace, C3 protocol detail, released artifacts |

## Original Source

- [source/2608.23067.pdf](source/2608.23067.pdf) — arXiv PDF, retrieved 2026-08-26
