---
type: index
title: "Foreground Voice Activity Detection: Learning Speaker Selectivity from Supervision"
description: "Folder index for the enrollment-free Foreground VAD paper: orientation, reading order, and links to summary, digest, explainer, critical thinking, questions, and all wiki pages."
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T09:22:45Z
sources:
  - id: original
    resource: https://arxiv.org/abs/2609.19856
  - id: local-copy
    resource: source/source.md
tags: [voice-activity-detection, foreground-VAD, speaker-selectivity, streaming-inference]
---

# Foreground Voice Activity Detection: Learning Speaker Selectivity from Supervision

This folder distills the paper's enrollment-free Foreground VAD proposal: track only the sustained dominant speaker by supervising competing speech as negative. The headline result is that selectivity comes from the interference-aware data recipe, not the backbone, in a tiny streaming model. Start with the summary for the takeaway, then the digest for the evidence, then the wiki pages for section-by-section detail.

## How to work through this

1. Read `summary.md` (~2 min) for the TL;DR, task formalization, supervision recipe, and key findings.
2. Read `digest.md` (~10 min) for the six chunk summaries plus the five-move argument arc.
3. Deep-dive the `wiki/` pages in order for verbatim-backed section detail, then use `explainer.md` for plain-language intuition, `critical_thinking.md` for claims-vs-evidence scrutiny, and `questions.md` for retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem, original ideas, findings, future directions.
- [Digest](digest.md) — six chunk summaries plus the argument in five moves.
- [Explainer](explainer.md) — plain-language walkthrough with jargon decoder.
- [Critical Thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, applicability, verdict.
- [Questions](questions.md) — eleven retrieval-practice Q&As covering every wiki page.

## Wiki

| Page | Covers |
|------|--------|
| [01-overview](wiki/01-overview.md) | Paper framing, task definition, and abstract-level claims (chunk 01, truncated) |
| [02-background-and-method](wiki/02-background-and-method.md) | Introduction, related work, interference-aware supervision recipe, model, and benchmark creation (Sections I–III) |
| [03-benchmark-and-selectivity-metric](wiki/03-benchmark-and-selectivity-metric.md) | Foreground F1 and BG-FAR definitions plus Mix-Interference and VOiCES selectivity results (Section IV-A) |
| [04-conventional-vad-performance](wiki/04-conventional-vad-performance.md) | Conventional VAD performance and competing-speaker mixing ablation setup and findings (Sections IV-B–IV-C) |
| [05-ablations](wiki/05-ablations.md) | Boundary case, far-field rendering, architecture ablation, selective-attention behavior, and conclusion with limitations (Sections IV-C–V) |
| [06-qualitative-behavior-and-conclusion](wiki/06-qualitative-behavior-and-conclusion.md) | References [1]–[29], Foreground F1 and BG-FAR algorithm appendices, and generative-AI disclosure (chunk 06 body truncated) |

## Original Source

- arXiv: [Foreground Voice Activity Detection: Learning Speaker Selectivity from Supervision](https://arxiv.org/abs/2609.19856)
- Local copy: [source/source.md](source/source.md)
