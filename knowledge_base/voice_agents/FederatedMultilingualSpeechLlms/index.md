---
type: index
title: "Federated Multilingual Speech-LLMs: Architecture and Aggregation Strategy Benchmarking"
description: "Folder index for the federated multilingual Speech-LLM benchmark: Whisper/WavLM encoder-LLM pairings on speaker-partitioned MLS under FedAvg vs FedProx."
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T11:20:23Z
sources:
  - id: original
    resource: http://arxiv.org/abs/2609.23825v1
  - id: local-copy
    resource: source/source.md
tags: [federated-learning, speech-recognition, multilingual, speech-llm]
---

# Federated Multilingual Speech-LLMs: Architecture and Aggregation Strategy Benchmarking

This folder distills the first systematic benchmark of federated multilingual ASR with Speech-LLMs on speaker-partitioned Multilingual LibriSpeech (8 languages, 316 single-speaker clients). The headline result: ASR-supervised Whisper encoders paired with the multilingual EuroLLM decoder win, per-component learning rates with full three-component adaptation give the lowest errors, and FedProx helps only the strong multilingual backbone. Start with the summary, then the digest, then the wiki pages for evidence.

## How to work through this

1. Read the **summary** (~2 min) for the TL;DR, problem, ideas, and findings.
2. Read the **digest** (~10 min) for the per-chunk sentences, key points, and the five-move argument.
3. Dive into the **wiki pages** in order for tables, verbatim evidence, and section coverage — then test yourself with **questions** and the plain-language **explainer**.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem and motivation, ideas, findings, future directions.
- [Digest](digest.md) — per-chunk sentences and key points plus the argument in five moves.
- [Explainer](explainer.md) — plain-language walkthrough of the setup, loop, and takeaways.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, verdict.
- [Questions](questions.md) — retrieval practice (Q1–Q7) covering every wiki page.

## Wiki

| Page | Covers |
|---|---|
| [01 — Federated Multilingual Speech-LLMs: Architecture and Aggregation](wiki/01-federated-multilingual-speech-llms-architecture.md) | Benchmark scope, research questions (Q1/Q2), FedAvg setup, and headline findings |
| [02 — Speech-LLM architecture: encoder, connector, decoder](wiki/02-speech-llm-architecture-encoder-connector-decoder.md) | Figure 1 pipeline, four Whisper/WavLM × TinyLlama/EuroLLM pairings, FedAvg/FedProx updates |
| [03 — SSL vs ASR Encoder Adaptability](wiki/03-ssl-vs-asr-encoder-adaptability.md) | MLS dataset and IID vs speaker partitions, leakage, training config, centralized ceilings (Table 1–2) |
| [04 — Per-Language WER: FedAvg vs FedProx](wiki/04-per-language-wer-fedavg-vs-fedprox.md) | Per-language Table 3 analysis, macro-averaged WER, FedProx low-resource effects |

## Original Source

- arXiv: [Federated Multilingual Speech-LLMs: Architecture and Aggregation Strategy Benchmarking](http://arxiv.org/abs/2609.23825v1)
- Local copy: [source/source.md](source/source.md)
