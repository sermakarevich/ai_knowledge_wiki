---
type: index
title: 'NAVIR: Neuromorphic Audio-Visual Speech Recognition for Robust Human-Robot Interaction on Edge Hardware'
description: Folder index for the NAVIR paper — an Akida-compatible audio-visual speech recognizer fusing lip video with noisy audio for low-power edge robot control.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T12:20:09Z
sources:
  - id: original
    resource: http://arxiv.org/abs/2609.24391v1
  - id: local-copy
    resource: source/source.md
tags: [neuromorphic-computing, audio-visual-speech-recognition, edge-AI, human-robot-interaction]
---

# NAVIR: Neuromorphic Audio-Visual Speech Recognition for Robust Human-Robot Interaction on Edge Hardware

NAVIR is an end-to-end audio-visual speech recognizer rebuilt to run on the BrainChip AKD1000 neuromorphic chip using only sequential 2D convolutions. It fuses lip-motion video with noise-augmented audio to hold 98.6% command accuracy under industrial noise, and was validated in a closed-loop Raspberry Pi + AKD1000 + xArm 6 robot demo. This folder holds a 2-minute summary, a 10-minute digest, plain-language and critical companions, and 12 wiki pages covering the full pipeline.

## How to work through this

1. Start with `summary.md` (~2 min) for the TL;DR, problem, ideas, and key numbers.
2. Read `digest.md` (~10 min) for the 12-section verbatim distillation of every wiki page plus the five-move argument.
3. Go deep in `wiki/` pages in order (01 → 12) for methods, results, energy measurements, and references.
4. Use `explainer.md` for plain-language intuition, `critical_thinking.md` for claims-vs-evidence scrutiny, and `questions.md` (Q1–Q15) for retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem, original ideas, findings, future directions.
- [Digest](digest.md) — 12-section condensed map of the whole paper.
- [Explainer](explainer.md) — plain-language walkthrough with jargon decoder.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, applicability, verdict.
- [Questions](questions.md) — 15 retrieval-practice Q&A covering every wiki page.

## Wiki table

| Page | Covers |
|---|---|
| [01-introduction-and-contributions](wiki/01-introduction-and-contributions.md) | Motivation, AVSR robustness, AKD1000 constraint, contributions and headline results |
| [02-neuromorphic-background](wiki/02-neuromorphic-background.md) | SNN energy principle, surrogate-gradient/residual/spiking-transformer lineage, AKD1000 regime and prior deployments |
| [03-related-work-akida-and-grid-sota](wiki/03-related-work-akida-and-grid-sota.md) | AKD1000 applications and limits, GRID and related corpora, lip-reading SOTA and noisy-fusion gap |
| [04-architecture-and-decoding](wiki/04-architecture-and-decoding.md) | Factorised per-frame/temporal/MFCC encoders, MLP fusion, CTC training, grammar-constrained beam search, hybrid quantization + QAT |
| [05-datasets-and-experimental-setup](wiki/05-datasets-and-experimental-setup.md) | NAVIR command corpus, UrbanSound8K noise protocol, GRID splits, augmentation and QAT schedules |
| [06-grid-recognition-results](wiki/06-grid-recognition-results.md) | GRID fusion-under-noise results, quantization effects, constrained vs. unconstrained SOTA gap |
| [07-navir-results-and-energy-method](wiki/07-navir-results-and-energy-method.md) | NAVIR Table 8 quantized results, operation-count energy model, 13.17x SNN-over-ANN gain |
| [08-power-measurements-and-pareto](wiki/08-power-measurements-and-pareto.md) | Table 11 on-board power, 5 vs. 22-pass mappings, Pi-CPU and GPU baselines |
| [09-robot-demonstration](wiki/09-robot-demonstration.md) | Pi + AKD1000 + xArm 6 closed-loop demo, real-time claim, first-system claim |
| [10-limitations-future-work-appendices](wiki/10-limitations-future-work-appendices.md) | Threshold/l1 sparsity fix, AKD1000 toolchain note, Appendix B encoder/head specs |
| [11-references-part-1](wiki/11-references-part-1.md) | Bibliography [2]–[30]: energy, SNN training, hardware, speech datasets |
| [12-references-part-2](wiki/12-references-part-2.md) | Bibliography [31]–[40], author biographies, closing footers |

## Original Source

- arXiv: [http://arxiv.org/abs/2609.24391v1](http://arxiv.org/abs/2609.24391v1)
- Local copy: [source/source.md](source/source.md)
