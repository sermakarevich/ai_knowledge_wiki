---
type: index
title: StepAudio 3 Realtime Technical Report — Folder Index
description: Orientation index for the StepAudio 3 Realtime paper folder: summary, digest, explainer, critical analysis, questions, and ten wiki pages.
generated:
  by: claude/opencode-go/muse-spark-1.3-contributor
  at: 2026-09-22T11:53:04Z
sources:
  - id: original
    resource: https://arxiv.org/abs/2609.14005
  - id: local-copy
    resource: source/source.md
tags: [realtime-speech, full-duplex-dialogue, audio-language-models, voice-agents]
---

# StepAudio 3 Realtime Technical Report

StepAudio 3 Realtime is an audio-language foundation model for full-duplex spoken interaction, organized around a listen-converse-think-act loop with Think-While-Speaking reasoning and a streaming Voice Agent. This folder holds a layered reading path: a 2-minute summary, a 10-minute digest, ten detailed wiki pages, plus explainer, critical analysis, and retrieval questions.

## How to work through this

1. Start with `summary.md` (~2 min) for the TL;DR, key ideas, findings, and future directions.
2. Read `digest.md` (~10 min) for the one-sentence takeaway plus key points of each wiki page, in order.
3. Go deep in `wiki/` pages 01–10 for evidence, tables, and section-level detail; use `explainer.md` for plain-language intuition, `critical_thinking.md` for claims-vs-evidence scrutiny, and `questions.md` for retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem, original ideas, findings, future directions.
- [Digest](digest.md) — one-sentence + key points per wiki page, plus the argument in five moves.
- [Explainer](explainer.md) — plain-language walkthrough with jargon decoder.
- [Critical Thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, verdict.
- [Questions](questions.md) — 16 retrieval-practice Q&As covering every wiki page.

## Wiki

| Page | Covers |
|---|---|
| [01 Overview: Listen-Converse-Think-Act Loop](wiki/01-overview-listen-converse-think-act-loop.md) | Abstract, Figure 1 headline results, Introduction, realtime loop overview |
| [02 Architecture and Foundation Training](wiki/02-architecture-foundation-training.md) | Conversational context, MoE architecture, 3-stage pretraining, 128K midtraining, ASR SFT divergence |
| [03 Deep Perception: ASR Max and Audio Understanding](wiki/03-deep-perception-asr-max.md) | ASR benchmarks (Table 1), ContextASR-Bench, audio-understanding data pipeline, Table 2, quality ablation |
| [04 Seamless Duplex Floor Management](wiki/04-seamless-duplex-floor-management.md) | Pauses, backchannels, interruptions, background rejection, 10K-hour duplex training, AA bench Table 3, StepAudioChat/data lead-in |
| [05 Conversational Intelligence — Reasoning-Mode Evaluation](wiki/05-conversational-intelligence-stepaudiochat.md) | StepAudioChat Table 4 reasoning results, Think-While-Speaking design, Adaptive Thinking policy and Table 5 |
| [06 Think-While-Speaking, Adaptive Reasoning and MTP Acceleration](wiki/06-think-while-speaking-adaptive-reasoning.md) | MTP3/MTP5 Tables 6–7, teacher merging Table 8, voice-agent routing |
| [07 Voice Agent Tool Execution and Agentic Results](wiki/07-voice-agent-tool-execution.md) | τ-Voice Table 9, clarification/confirmation discipline, async execution, tool-use training |
| [08 Capability Evaluation Benchmarks (Table 10)](wiki/08-capability-evaluation-benchmarks.md) | Table 10 cross-domain comparison, interpretation, conclusion |
| [09 References: Audio Language Models and Streaming Systems](wiki/09-references-audio-language-models.md) | References [4]–[39]: audio LM foundations, Step-Audio lineage, duplex systems, ASR, decoding, agents |
| [10 References: Benchmarks and Evaluation](wiki/10-references-benchmarks-evaluation.md) | References [40]–[56]: speech/dialogue benchmarks, LLM evaluation, industry model docs |

## Original Source

- arXiv: [StepAudio 3 Realtime Technical Report — https://arxiv.org/abs/2609.14005](https://arxiv.org/abs/2609.14005)
- Local copy: [source/source.md](source/source.md)
