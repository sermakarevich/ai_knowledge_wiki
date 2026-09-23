---
type: index
title: "NemotronLabs VoiceChat: An Open Full-duplex Speech-to-Speech Model with Tool Calling Capabilities"
description: "Folder index for the NemotronLabs VoiceChat paper: orientation, reading order, and links to summary, digest, explainer, wiki pages, and original source."
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T11:41:04Z
sources:
  - id: original
    resource: https://arxiv.org/abs/2609.21967
  - id: local-copy
    resource: source/source.md
tags: [full-duplex-speech, speech-to-speech, tool-calling, streaming-tts]
---

# NemotronLabs VoiceChat: An Open Full-duplex Speech-to-Speech Model with Tool Calling Capabilities

This folder collects study notes for the NemotronLabs VoiceChat paper (arXiv:2609.21967), presented as the first fully open unified streaming speech-to-speech model combining full-duplex conversational timing with native tool calling. Start with the summary for the headline claims, use the digest for verbatim key points per section, then go deeper with the wiki pages, explainer, and critical analysis.

## How to work through this

1. Read `summary.md` (~2 min) for the TL;DR, main ideas, and reported results.
2. Read `digest.md` (~10 min) for the section-by-section key points and the five-move argument.
3. Open the `wiki/` pages, `explainer.md`, `critical_thinking.md`, and `questions.md` for detail, plain-language background, critical appraisal, and retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem, ideas, findings, and future directions.
- [Digest](digest.md) — verbatim key points per wiki chunk plus the argument in five moves.
- [Explainer](explainer.md) — plain-language walkthrough: what it is, why it matters, how it works, and where it applies.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, applicability, and verdict.
- [Questions](questions.md) — retrieval-practice questions with answers linked to wiki pages.

## Wiki

| Page | Covers |
|------|--------|
| [01-overview-architecture](wiki/01-overview-architecture.md) | Overview and full-duplex architecture; abstract and introduction |
| [02-speech-to-text](wiki/02-speech-to-text.md) | STT component: streaming encoder, LLM backbone, 80-ms timeline, RNN-T branch |
| [03-training-recipes](wiki/03-training-recipes.md) | Component-wise training, STT loss and optimization, inference-time enhancements |
| [04-backchannel-evaluation](wiki/04-backchannel-evaluation.md) | Backchannel behavior, VoiceBench intelligence, FDB 3.0 tool calling, conclusion and limitations |
| [05-references-background](wiki/05-references-background.md) | Prior work references [4]–[38] and CPT pseudo-dialogue data construction |
| [06-sft-data-construction](wiki/06-sft-data-construction.md) | SFT data mixture, tool-calling pipeline, and conversational augmentation |
| [07-tts-decoder-evaluation](wiki/07-tts-decoder-evaluation.md) | VoiceChat-TTS standalone evaluation, streaming ASR, and inference efficiency |

## Original Source

- arXiv: [NemotronLabs VoiceChat: An Open Full-duplex Speech-to-Speech Model with Tool Calling Capabilities](https://arxiv.org/abs/2609.21967)
- Local copy: [source/source.md](source/source.md)
