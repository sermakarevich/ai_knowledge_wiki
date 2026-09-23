---
type: index
title: 'ECHO: A Matched-Contrast Benchmark for Context-Sensitive Turn-Taking in Full-Duplex Dialogue'
description: Folder index for the ECHO paper — a paired Chinese diagnostic benchmark testing context-sensitive YIELD-vs-KEEP turn-taking in full-duplex dialogue.
generated:
  by: claude/muse-spark-1.3-contributor
  at: '2026-09-22T11:51:54Z'
sources:
  - id: original
    resource: https://arxiv.org/abs/2609.17360
  - id: local-copy
    resource: source/source.md
tags:
  - full-duplex-dialogue
  - turn-taking
  - speech-benchmarks
  - context-sensitivity
---

# ECHO: A Matched-Contrast Benchmark for Context-Sensitive Turn-Taking in Full-Duplex Dialogue

ECHO tests whether voice AIs yield the floor or keep talking when the overlapping words are identical and only the earlier conversation differs. Its matched pairs expose a widespread over-yielding bias that interruption-only accuracy hides. This folder holds a 2-minute summary, a 10-minute digest, plain-language and critical companions, and four wiki pages.

## How to work through this

1. Start with the summary (~2 min) for the TL;DR, problem, ideas, and headline numbers.
2. Read the digest (~10 min) for the per-page key points plus the five-move argument.
3. Go deep with the wiki pages in order (01 → 04), then the explainer and critical_thinking for intuition and caveats.
4. Self-test with questions.md — one retrieval prompt per wiki page (two for pages 02–04).

## Read This Folder

- [Summary](summary.md) — TL;DR, problem, ideas, findings, future directions.
- [Digest](digest.md) — per-page key points plus the argument in five moves.
- [Explainer](explainer.md) — plain-language walkthrough with jargon decoder.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, verdict.
- [Questions](questions.md) — retrieval practice covering every wiki page.

## Wiki

| Page | Covers |
|------|--------|
| [01-matched-contrast-benchmark-overview](wiki/01-matched-contrast-benchmark-overview.md) | Paper framing: Yield-vs-KEEP paired benchmark idea and abstract-level claims (source chunk truncated; title/authors/affiliation only) |
| [02-background-roles-contrast-generation](wiki/02-background-roles-contrast-generation.md) | Sec. 1–2.1: YIELD-vs-KEEP framing, prior-benchmark gaps, matched-contrast design, roles, and generation/validation pipeline |
| [03-speech-synthesis-overlap-rendering](wiki/03-speech-synthesis-overlap-rendering.md) | Sec. 2.3 / Fig. 1: IndexTTS2 synthesis pipeline, within-group controls, role-dependent overlap rendering, matched-contrast illustration |
| [04-experiments-pair-metrics-findings](wiki/04-experiments-pair-metrics-findings.md) | Experiments, pair-level metrics (PASR/PASRI, PRSR, PKC), Yield-bias findings, conclusion, and limitations |

## Original Source

- arXiv: [ECHO: A Matched-Contrast Benchmark for Context-Sensitive Turn-Taking in Full-Duplex Dialogue](https://arxiv.org/abs/2609.17360)
- Local copy: [source/source.md](source/source.md)
