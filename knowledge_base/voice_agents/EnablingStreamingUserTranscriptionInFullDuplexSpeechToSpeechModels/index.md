---
type: index
title: Enabling Streaming User Transcription in Full-Duplex Speech-to-Speech Models
description: Folder index for the SALM-Duplex streaming user transcription paper — summary, digest, wiki pages, explainer, and critical analysis.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T11:42:37Z
sources:
  - id: original
    resource: https://arxiv.org/abs/2609.15759
  - id: local-copy
    resource: source/source.md
tags: [full-duplex, speech-to-speech, streaming-ASR, turn-taking]
---

# Enabling Streaming User Transcription in Full-Duplex Speech-to-Speech Models

This folder distills the NVIDIA paper that adds a lightweight parallel streaming ASR head to the SALM-Duplex full-duplex S2S model. The integrated system transcribes the user in real time (10.21% average WER) while preserving turn-taking and barge-in, and the same architecture reaches 7.73% WER as a standalone streaming recognizer.

## How to work through this

- Start with the summary (~2 min) for the TL;DR, problem, ideas, and key numbers.
- Then read the digest (~10 min) for the per-page key points plus the five-move argument.
- Then go deep into the wiki pages in order (01 → 04), using the explainer for plain-language background, critical_thinking for claims-vs-evidence scrutiny, and questions for retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem, ideas, findings, future directions.
- [Digest](digest.md) — per-page key points (verbatim from wiki) plus the argument in five moves.
- [Explainer](explainer.md) — plain-language walkthrough with jargon decoder.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, verdict.
- [Questions](questions.md) — retrieval practice with one question per wiki page or more.

## Wiki

| Page | Covers |
|---|---|
| [01 — Enabling Streaming User Transcription in Full-Duplex](wiki/01-enabling-streaming-user-transcription.md) | Paper framing: missing user transcription problem and proposed parallel ASR head (planned scope; source chunk holds title/authors/abstract fragment only) |
| [02 — Model Architecture and Streaming ASR Head](wiki/02-model-architecture-and-streaming-asr-head.md) | Backbone (Parakeet encoder + Nemotron LLM), parallel ASR head, on-the-fly CTC alignment with left word alignment and du/da delays, training data mixture |
| [03 — Experiments: Turn-Taking and ASR Results](wiki/03-experiments-turn-taking-and-asr-results.md) | Duplex results at du = 1.2s / da = 0.16s: 10.21% WER, turn-taking/barge-in (Tables I–II), intelligence (Table III), FDB-v1 (Table IV), standalone numbers (Table V) |
| [04 — Standalone Streaming ASR, Conclusions and References](wiki/04-standalone-asr-conclusions-and-references.md) | Standalone ASR (7.73% WER with YODAS/YTC), conclusions on the lightweight parallel head, AI-use disclosure and references |

## Original Source

- arXiv: [Enabling Streaming User Transcription in Full-Duplex Speech-to-Speech Models](https://arxiv.org/abs/2609.15759)
- Local copy: [source/source.md](source/source.md)
