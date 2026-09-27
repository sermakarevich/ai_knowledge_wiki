---
type: Paper
title: "Toolformer: Language Models Can Teach Themselves to Use Tools"
description: Self-supervised recipe teaching a 6.7B GPT-J model to call five external tools (QA, search, calculator, translation, calendar), filtering candidate API calls by whether their result reduces future-token loss, so it beats OPT-66B/GPT-3-175B zero-shot on factual, math, and temporal tasks without hurting base perplexity.
generated: { by: claude/claude-sonnet-5, at: 2026-09-12T07:00:00Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2302.04761
  - id: local-copy
    resource: source/full.md
tags: [llm-agents, tool-use, self-supervised-learning, retrieval-augmentation, finetuning]
---

# Toolformer: Language Models Can Teach Themselves to Use Tools

Toolformer (Schick et al., Meta AI) teaches a frozen-architecture 6.7B GPT-J model to call external tools — a factoid-QA system, Wikipedia search, a calculator, a translator, and a calendar — by sampling candidate API calls from a handful of demonstrations, keeping only calls whose result lowers future-token loss past a threshold, and finetuning on the resulting augmented corpus. The model then decides zero-shot when, which, and how to call each tool, beating same-size baselines and often OPT-66B/GPT-3-175B on LAMA, math word problems, and temporal reasoning, with no perplexity cost when tools are disabled — but only one call per input is supported, so chained or interactive tool use remains unsolved.

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
| [[wiki/01-approach-tools\|Approach and tool set]] | Motivation, sampling/filtering formalism, markers, five tools, inference procedure |
| [[wiki/02-experiments-analysis\|Experiments, analysis, limits]] | LAMA, math, open QA, MLQA, temporal results; scale and decoding-threshold analysis; hard limits |
| [[wiki/03-conclusion-appendices\|Conclusion and training appendices]] | Exact thresholds, per-tool implementations, training setup, evaluation prompts, Dateset construction |

## Original Source

- [source/full.md](source/full.md) — full paper text, retrieved from arXiv:2302.04761
