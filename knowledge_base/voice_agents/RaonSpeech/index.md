---
type: index
title: krafton-ai/Raon-Speech
description: "Index for the Raon-Speech repo folder: 9B bilingual SpeechLM family, offline and full-duplex tracks, latency numbers, and top-level runtime files."
generated:
  by: claude/muse-spark-1.3-contributor
  at: "2026-09-22T17:27:24Z"
sources:
  - id: original
    resource: https://github.com/krafton-ai/Raon-Speech
  - id: local-copy
    resource: source/source.md
tags: [speech-ai, text-to-speech, speech-recognition, full-duplex-dialogue]
---
# krafton-ai/Raon-Speech

This folder indexes KRAFTON's open-source Raon-Speech repo: a 9B bilingual (English/Korean) SpeechLM family with an offline track (TTS, STT, SpeechChat, TextQA) and a real-time full-duplex track (Raon-SpeechChat) sharing one backbone under `src/raon/`. Start here to find the 2-minute summary, the 10-minute digest, the plain-language explainer, critical analysis, practice questions, and the two wiki pages.

## How to work through this

1. Read `summary.md` (~2 min) for the TL;DR, problem, architecture, and key findings.
2. Read `digest.md` (~10 min) for the condensed verbatim key points per wiki page plus the system in five moves.
3. Deep-dive the `wiki/` pages in order, then use `explainer.md`, `critical_thinking.md`, and `questions.md` to check understanding.

## Read This Folder

- [Summary](summary.md) — technical analysis: problem, architecture, bilingual core, workflows, files, dependencies, CLI.
- [Digest](digest.md) — verbatim-condensed key points per wiki page plus the system in five moves.
- [Explainer](explainer.md) — plain-language walkthrough: what it is, why it matters, how it works, uses.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, applicability, verdict (watch).
- [Questions](questions.md) — retrieval practice with answers (Q1–Q7 covering both wiki pages).

## Wiki

| Page | Covers |
|---|---|
| [01-overview](wiki/01-overview.md) | README.md repo overview: two tracks, benchmarks/latency table, requirements, model loading, execution modes, layout, architecture, SpeechLLM data format/inference/API/training, duplex format up to `speak_first` truncation |
| [02-top-level-files](wiki/02-top-level-files.md) | `.gitignore`, `NOTICE`, `requirements.txt` |

## Original Source

- Original: https://github.com/krafton-ai/Raon-Speech
- Local copy: [source/source.md](source/source.md)
