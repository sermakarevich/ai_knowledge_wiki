---
type: Paper
title: Seven Failure Points When Engineering a Retrieval Augmented Generation System
description: An experience report from three RAG deployments (research, education, biomedical) cataloguing seven recurring RAG failure points and the engineering lessons they imply.
generated: { by: claude/sonnet, at: 2026-08-20T18:24:01Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2401.05856
  - id: local-copy
    resource: source/paper.pdf
tags: [rag, retrieval, failure-modes, software-engineering, case-study]
---

# Seven Failure Points When Engineering a Retrieval Augmented Generation System

This paper (Barnett et al., Deakin University, CAIN 2024) is a software-engineering experience report on Retrieval Augmented Generation (RAG) systems — not a benchmark study. It builds a catalogue of seven failure points from three real RAG deployments (a research literature-review tool, a university AI tutor, and a large-scale biomedical Q&A experiment), then distills nine engineering lessons and three open research directions. It was worth ingesting because it is one of the earliest practitioner-grounded taxonomies of *where and why* RAG systems go wrong, independent of model or vector-database choice.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every page's headline and key points.
3. **Wiki pages below** (~5-10 min each) — one topic, deep. Each opens with its headline and key points, so you can stop early.

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
| [[wiki/01-background-and-rag-pipeline\|Background & RAG Pipeline]] | Why RAG over fine-tuning, the Index/Query pipeline, Figure 1 |
| [[wiki/02-case-studies\|Case Studies]] | Cognitive Reviewer, AI Tutor, BioASQ — the three systems the failure catalogue is drawn from |
| [[wiki/03-seven-failure-points\|The Seven Failure Points]] | Missing Content, Missed Top Ranked, Not in Context, Not Extracted, Wrong Format, Incorrect Specificity, Incomplete |
| [[wiki/04-lessons-and-future-research\|Lessons & Future Research]] | Nine lessons (Table 2), and three open research directions |

## Original Source

- [source/paper.pdf](source/paper.pdf) — PDF, retrieved 2026-08-20
- [source/full_text.md](source/full_text.md) — extracted full text
