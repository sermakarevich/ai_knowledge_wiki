---
type: index
title: KetsuiLabs/MichiAI
description: Folder index for KetsuiLabs/MichiAI, a 530M-parameter full-duplex speech LLM claiming ~80ms time-to-first-audio via continuous embeddings and flow matching.
generated:
  by: claude/muse-spark-1.3-contributor
  at: "2026-09-22T16:56:27Z"
sources:
  - id: original
    resource: https://github.com/KetsuiLabs/MichiAI
  - id: local-copy
    resource: source/source.md
tags: [speech-LLM, full-duplex, low-latency-TTS, voice-cloning]
filed_via: jev choose, category: models, confidence: 0.9
---

# KetsuiLabs/MichiAI

MichiAI is a 530M-parameter multimodal speech LLM for full-duplex voice interaction that listens and speaks simultaneously with a claimed ~80ms time-to-first-audio. It pairs a SmolLM-360m backbone with a Listening Head and a Speaking Head built on continuous audio latents, rectified flow matching, and a causal HiFi-GAN vocoder. This folder holds the summary, digest, wiki pages, explainer, critical analysis, and retrieval questions for the repo snapshot.

## How to work through this

1. **Summary (~2 min):** read `summary.md` for the problem, architecture, spec table, comparison, and roadmap.
2. **Digest (~10 min):** read `digest.md` for the verbatim key points per wiki page plus the system in five moves.
3. **Wiki pages:** read `wiki/` for full detail — specs, features, architecture, comparison table, roadmap, and top-level files.
4. **Going further:** read `explainer.md` for the plain-language version, `critical_thinking.md` for claims-vs-evidence scrutiny, then test yourself with `questions.md`.

## Read This Folder

- [Summary](summary.md) — overview, architecture, pipeline, files, dependencies, limitations, and comparisons.
- [Digest](digest.md) — verbatim key points per wiki page plus the system in five moves.
- [Explainer](explainer.md) — plain-language walkthrough with jargon decoder.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, verdict (watch).
- [Questions](questions.md) — retrieval practice, Q1–Q7 with answers.

## Wiki

| Page | Covers |
|---|---|
| [01-overview](wiki/01-overview.md) | `README.md` (goals, specs, features, Listening/Speaking-head architecture, performance comparison, roadmap) |
| [02-top-level-files](wiki/02-top-level-files.md) | `.gitignore`, `_config.yml` (docs-site theme/title/description, `dist` exclusion) |

## Original Source

- Original: [KetsuiLabs/MichiAI](https://github.com/KetsuiLabs/MichiAI)
- Local copy: [source/source.md](source/source.md)
