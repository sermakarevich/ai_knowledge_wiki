---
type: index
title: "Voice-Light: A Full-Duplex Cascaded Voice Agent with Causal Turn-Taking and Speculative Generation"
description: "Folder index for the Voice-Light paper: a full-duplex cascaded voice agent with a causal turn-taking adapter, reversible hybrid controller, and private speculative generation."
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T11:50:18Z
sources:
  - id: original
    resource: https://arxiv.org/abs/2609.20995
  - id: local-copy
    resource: source/source.md
tags: [voice-agents, full-duplex, turn-taking, cascaded-systems]
---

# Voice-Light: A Full-Duplex Cascaded Voice Agent with Causal Turn-Taking and Speculative Generation

Voice-Light is a full-duplex cascaded (streaming ASR → LLM → TTS) voice agent whose rule is that uncertain work may begin early but becomes audible or durable only after explicit causal checks. Its headline result is negative: the learned turn-completion policy loses to simple timing baselines on locked real-conversation tests, so the deployed system keeps a hybrid controller. This folder holds a layered reading path — a 2-minute summary, a 10-minute digest, plain-language and critical companions, seven deep-dive wiki pages, and retrieval questions.

## How to work through this

1. Start with `summary.md` (~2 min) for the TL;DR, problem, key ideas, findings, and limits.
2. Read `digest.md` (~10 min) for the seven section condensates plus the argument in five moves.
3. Go deep in `wiki/` page by page for evidence, numbers, and caveats; use `explainer.md` for intuition and `critical_thinking.md` for claims-vs-evidence.
4. Test yourself with `questions.md` before citing any number.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem and motivation, main ideas, key findings, future directions.
- [Digest](digest.md) — seven section condensates plus the argument in five moves.
- [Explainer](explainer.md) — the paper in plain language.
- [Critical thinking](critical_thinking.md) — claims vs. evidence and limits.
- [Questions](questions.md) — retrieval practice (Q1–Q10) covering every wiki page.

## Wiki

| Page | Covers |
| ---- | ------ |
| [Voice-Light: A Full-Duplex Cascaded Voice Agent](wiki/01-full-duplex-cascaded-voice-agent.md) | Full-duplex cascade, causal rule, reversible control, private speculation, and the hybrid-controller outcome |
| [Acknowledged Audio and Latency Results](wiki/02-acknowledged-audio-latency-results.md) | Acknowledged-audio durability, system latency scope, streaming components, and the two synthetic-data branches |
| [Synthetic Data and Turn-Taking Corpora](wiki/03-synthetic-data-turn-taking-corpora.md) | Synthetic rendering pipeline, V4/V5 manifests, locked human corpus, and both trained adapters |
| [Model Adaptation and Validation-Loss Tuning](wiki/04-model-adaptation-validation-loss.md) | Step-750 adapter selection, tool-protocol holdout, and the synthetic-to-human transfer gap |
| [Turn-Completion Evaluation — The Detectors Do Not Score](wiki/05-turn-completion-evaluation.md) | Native-gate policy comparison, locked V1 negative result, and the sealed V2 test split |
| [5 Snapshots Failed for the Multi-Process — End-to-End Latency Case Study](wiki/06-streaming-controller-deployment.md) | Scale-to-zero deployment, 36-turn latency case study, speculation association, and observability |
| [Discussion and Limitations: The Negative Result](wiki/07-discussion-limitations.md) | Bounded contribution, evidence limits, and what would justify replacing the hybrid controller |

## Original Source

- arXiv: [Voice-Light: A Full-Duplex Cascaded Voice Agent with Causal Turn-Taking and Speculative Generation](https://arxiv.org/abs/2609.20995)
- Local copy: [source/source.md](source/source.md)
