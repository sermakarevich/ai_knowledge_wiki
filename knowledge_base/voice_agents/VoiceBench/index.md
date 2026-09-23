---
type: index
title: MatthewCYM/VoiceBench
description: Folder index for the MatthewCYM/VoiceBench repo notes — 11-subset spoken-instruction benchmark for LLM voice assistants with a three-step generate-judge-score pipeline.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T17:44:56Z
sources:
  - id: original
    resource: https://github.com/MatthewCYM/VoiceBench
  - id: local-copy
    resource: source/source.md
tags: [voice-assistant, speech-benchmark, llm-evaluation, spoken-qa]
---

# MatthewCYM/VoiceBench

VoiceBench is a benchmark harness for LLM-based voice assistants that pairs the 11-subset spoken-instruction suite on Hugging Face (`hlt-lab/voicebench`) with a fixed generate-then-judge-then-score pipeline (`main.py` → `api_judge.py` via `gpt-4o-mini` → `evaluate.py`). Subsets span open-ended, multiple-choice, reference-based, and multi-turn QA plus instruction following, reasoning, and safety, in mixed Google TTS and human audio. Use the summary and digest for the short path, then the two wiki pages for full pipeline and file-level detail.

## How to work through this

1. Read `summary.md` (~2 min) for the overview, architecture, subset table, pipeline, and gotchas.
2. Read `digest.md` (~10 min) for the compressed key points per section plus the system in five moves.
3. Deep-dive the wiki pages in order for full detail, then test yourself with `questions.md` and check `critical_thinking.md` for claims-vs-evidence gaps.

## Read This Folder

- [Summary](summary.md) — overview, architecture, spoken-instruction subsets, pipeline, key files, dependencies, CLI, extensibility, limitations.
- [Digest](digest.md) — compressed key points per wiki section plus the system in five moves.
- [Explainer](explainer.md) — plain-language walkthrough of the benchmark, the three-step pipeline, and reuse.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, applicability, verdict.
- [Questions](questions.md) — retrieval practice (Q1–Q7) covering both wiki pages.

## Wiki

| Page | Covers |
|---|---|
| [01-overview](wiki/01-overview.md) | README.md project header, News, Setup, 11-subset dataset suite, three-step evaluation flow, Awesome Voice Assistants table |
| [02-top-level-files](wiki/02-top-level-files.md) | `main.py`, `api_judge.py`, `evaluate.py`, `requirements.txt`, `.gitignore` (repo root top-level files) |

## Original Source

- Upstream: [https://github.com/MatthewCYM/VoiceBench](https://github.com/MatthewCYM/VoiceBench)
- Local copy: [source/source.md](source/source.md)
