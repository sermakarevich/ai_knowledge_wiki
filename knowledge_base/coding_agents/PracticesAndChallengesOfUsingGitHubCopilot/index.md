---
type: index
title: "Practices and Challenges of Using GitHub Copilot:"
description: Empirical study of GitHub Copilot practice mining 169 Stack Overflow posts and 655 GitHub Discussions — languages, IDEs, technologies, implemented functions, benefits led by useful code generation (49.0%), and limitations around quality, privacy, and integration.
generated: { by: claude/muse-spark-1.3-contributor, at: 2026-09-23T21:27:04Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2303.08733v3
  - id: local-copy
    resource: source/source.md
tags: [github-copilot, empirical-study, developer-productivity, ai-pair-programming]
---

# Practices and Challenges of Using GitHub Copilot:

This folder summarises an empirical study of how developers really use GitHub Copilot, mined from Stack Overflow and GitHub Discussions. The headline is that Copilot speeds up routine work in mainstream setups but brings quality, privacy, and integration trade-offs. Use the summary for the gist, the digest for the numbers, and the wiki pages for section-by-section depth.

## How to work through this

Three depths — stop at whichever answers your question:

1. [Summary](summary.md) (~2 min) — the whole paper, shallow.
2. [Digest](digest.md) (~10 min) — the whole paper at medium depth: every section's headline and key points.
3. Wiki pages below (~5 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

New to the topic? Start with [the plain-language explainer](explainer.md) instead. Coming back after a break? Read [the digest](digest.md), then [self-test](questions.md) — do not re-read the wiki.

## Read This Folder

- [Summary](summary.md) — rung 1: the whole source, shallow
- [Digest](digest.md) — rung 2: the whole source at medium depth; the file to re-read on review
- [Plain-Language Explainer](explainer.md) — no-jargon explanation, applications, conclusions
- [Critical Analysis](critical_thinking.md) — claims vs. evidence, applicability, what it changes, verdict
- [Retrieval Practice](questions.md) — self-test questions; answer these from memory before re-reading anything

## Wiki

| Page | Covers |
|------|--------|
| [01-overview](wiki/01-overview.md) | Paper title, authors, affiliations, and truncated abstract fragment; no findings citable from this chunk |
| [02-research-design](wiki/02-research-design.md) | Related work, RQ1–RQ6, and data method: 169 SO posts + 655 GitHub Discussions with descriptive statistics and constant comparison |
| [03-languages-ides-technologies-functions](wiki/03-languages-ides-technologies-functions.md) | RQ1–RQ4 figure fragments: languages, IDEs, technologies, implemented functions, plus full Table III benefits |
| [04-benefits](wiki/04-benefits.md) | RQ5 benefits: useful code generation, faster development, code quality, style adaptation, user experience |
| [05-limitations-and-challenges](wiki/05-limitations-and-challenges.md) | RQ6 limitations plus implications: generation limits, quality, privacy, IDE integration, double-edged-sword verdict |

## Original Source

- [Original paper on arXiv](https://arxiv.org/abs/2303.08733v3) — Practices and Challenges of Using GitHub Copilot
- [Local copy](source/source.md) — full source text stored with this folder
