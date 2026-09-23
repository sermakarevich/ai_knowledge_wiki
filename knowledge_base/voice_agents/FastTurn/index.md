---
type: index
title: "FastTurn: Unifying Acoustic and Streaming Semantic Cues for Low-Latency and Robust Turn Detection"
description: "Folder index for FastTurn (arXiv:2604.01897) — acoustic-semantic fusion for low-latency robust turn detection in full-duplex spoken dialogue."
generated:
  by: claude/muse-spark-1.3-contributor
  at: "2026-09-22T11:55:27Z"
sources:
  - id: original
    resource: https://arxiv.org/abs/2604.01897
  - id: local-copy
    resource: source/source.md
tags: [turn-detection, full-duplex-dialogue, acoustic-semantic-fusion, low-latency-asr]
---

# FastTurn: Unifying Acoustic and Streaming Semantic Cues for Low-Latency and Robust Turn Detection

FastTurn is a turn-detection framework for full-duplex spoken dialogue that pairs fast streaming CTC transcription with Conformer acoustic cues fused into an LLM-backed decision. Its headline result is that FastTurn-Unified beats semantic-only baselines across Complete, Incomplete, Backchannel, and Wait states at lower latency (~120 ms). This folder holds a short summary, a verbatim digest, five wiki pages, plus plain-language, critical, and retrieval-practice companions.

## How to work through this

1. Start with `summary.md` (~2 min) for the TL;DR, problem, ideas, findings, and future directions.
2. Move to `digest.md` (~10 min) for the section-by-section digest with verbatim key points and the argument in five moves.
3. Go deeper with the wiki pages, then `explainer.md` for plain-language intuition, `critical_thinking.md` for claims-vs-evidence analysis, and `questions.md` for retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem and motivation, ideas, findings, future directions.
- [Digest](digest.md) — section digest with verbatim key points and five-move argument.
- [Explainer](explainer.md) — plain-language walkthrough: what it is, why it matters, how it works, where it applies.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, applicability, verdict.
- [Questions](questions.md) — nine retrieval-practice questions with answers linking back to the wiki.

## Wiki table

| Page | Covers |
|---|---|
| [FastTurn: Unifying Acoustic and Streaming Semantic](wiki/01-overview-and-problem.md) | Paper framing: full-duplex turn-taking problem, VAD vs ASR baselines, FastTurn contribution summary (chunk 01-fastturn-unifying-acoustic-and-streaming-semanti; source text truncated as noted above) |
| [FastTurn Architecture Variants: Cascaded, Semantic, Unified](wiki/02-architecture-variants.md) | Section 2 (2.1 Architecture: Cascaded / Semantic / Unified; 2.2 training pipeline overview) plus Figure 1 architecture diagram |
| [Training and Test Set: ASR Data, Turn-Detection Data, Setup, Metrics](wiki/03-training-and-test-set.md) | Sections 3–3.4 (Figure 2 training strategy; Table 1 FastTurn test-set splits; 3.1 ASR and turn-detection datasets; 3.2 setup and training schedule; 3.3 metrics; 3.4 main results with Tables 2–3) |
| [Main Results and Latency: Capabilities Across Smart Turn, Easy Turn, and FastTurn Test Sets](wiki/04-main-results-and-latency.md) | Sections 3.4–3.6 (Table 3 capabilities across Smart Turn / Easy Turn / FastTurn test sets, latency comparison, English subset note; ASR decoding adapter note; 3.6 ablation of Semantic vs Cascaded and Unified fusion) |
| [ASR Results and Conclusion](wiki/05-asr-ablation-and-conclusion.md) | Section 3.5 (ASR results, Table 4) through Section 4 (Conclusion) |

## Original Source

- arXiv: [https://arxiv.org/abs/2604.01897](https://arxiv.org/abs/2604.01897)
- Local copy: [source/source.md](source/source.md)
