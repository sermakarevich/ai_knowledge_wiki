---
type: index
title: 'StreamTN: A Low-Latency Streaming Chinese Text Normalization Model for Streaming TTS in Dialogue Systems'
description: Folder index for the StreamTN paper — a lightweight Qwen3-0.6B-based Chinese streaming text normalization model with dual-track architecture and a 14-category dialogue benchmark.
generated:
  by: claude/muse-spark-1.3-contributor
  at: '2026-09-22T09:13:53Z'
sources:
  - id: original
    resource: http://arxiv.org/abs/2609.24267v1
  - id: local-copy
    resource: source/source.md
tags: [text-normalization, streaming-tts, chinese-nlp, spoken-dialogue-systems]
---

# StreamTN: A Low-Latency Streaming Chinese Text Normalization Model for Streaming TTS in Dialogue Systems

StreamTN is a lightweight Qwen3-0.6B-based Chinese streaming text normalization model that converts partial LLM outputs into TTS-readable text with controllable first-packet delay. Its dual-track architecture plus a 95,793/1,262-sample 14-category dialogue benchmark reaches 0.8937 Micro-F1 at 213 ms delay (4-frame setting). Start with the summary for the big picture, then the digest and wiki pages for architecture, training, and results.

## How to work through this

1. **Summary (~2 min)** — the TL;DR, problem, key ideas, and headline numbers.
2. **Digest (~10 min)** — the full argument in four verbatim moves plus the five-move arc.
3. **Wiki pages** — deep dives with verbatim claims, equations, tables, and per-category results; use the explainer for plain-language intuition, critical_thinking for limits, and questions for retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem and motivation, main ideas, key findings.
- [Digest](digest.md) — verbatim per-section key points plus the argument in five moves.
- [Explainer](explainer.md) — plain-language walkthrough with jargon decoder.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, weaknesses, applicability, verdict.
- [Questions](questions.md) — retrieval practice Q1–Q7 covering all wiki pages.

## Wiki

| Page | Covers |
|---|---|
| [01-introduction-and-motivation](wiki/01-introduction-and-motivation.md) | SDS setting (cascaded vs. end-to-end), NSW ambiguity, prior TN work and streaming gap, StreamTN proposal and abstract claims |
| [02-dual-track-streaming-architecture](wiki/02-dual-track-streaming-architecture.md) | Prompt-based TN limits, streaming SDS requirements, 14-category benchmark gap, dual-track proposal and placement, streaming formulation (Eqs. 1–7) |
| [03-training-objective-and-dataset](wiki/03-training-objective-and-dataset.md) | Delay parameter d, masked NLL objective (Eq. 8), KV-cache inference alignment, FPD decomposition (Eq. 9), benchmark construction and experimental setup |
| [04-experiments-results-and-conclusions](wiki/04-experiments-results-and-conclusions.md) | Baseline comparison, per-category results (Table II), LoRA/prompt ablations (Table III), delay trade-off (Table IV), conclusions and future work |

## Original Source

- arXiv: [StreamTN: A Low-Latency Streaming Chinese Text Normalization Model for Streaming TTS in Dialogue Systems](http://arxiv.org/abs/2609.24267v1)
- Local copy: [source/source.md](source/source.md)
