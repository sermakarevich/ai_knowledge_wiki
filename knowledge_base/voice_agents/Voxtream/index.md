---
type: index
title: herimor/voxtream
description: Folder index for herimor/voxtream (VoXtream2) — full-stream zero-shot TTS with mid-utterance speaking-rate control, 74 ms first-packet latency, and CLI/Python/demo/server entry points.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T17:53:20Z
sources:
  - id: original
    resource: https://github.com/herimor/voxtream
  - id: local-copy
    resource: source/source.md
tags: [text-to-speech, streaming, voice-cloning, speaking-rate-control]
---
# herimor/voxtream

VoXtream2 is a zero-shot full-stream text-to-speech model that clones an unseen voice from a short prompt while streaming audio at 4x real-time with 74 ms first-packet latency. Its defining feature is dynamic speaking-rate control adjustable mid-utterance, plus translingual acoustic prompting. This folder holds the summary, digest, wiki pages, explainer, critical analysis, and retrieval questions for the repo.

## How to work through this (summary ~2 min → digest ~10 min → wiki pages)

1. Read `summary.md` (~2 min) for the overview, architecture, pipeline, interfaces, and limits.
2. Read `digest.md` (~10 min) for the verbatim key points per wiki page plus the system in five moves.
3. Deep-dive the wiki pages in order, then `explainer.md` for plain language, `critical_thinking.md` for claims-vs-evidence, and `questions.md` for retrieval practice.

## Read This Folder

- [Summary](summary.md) — overview, architecture, generator, pipeline, files, dependencies, CLI, extensibility, limitations.
- [Digest](digest.md) — verbatim key points for each wiki page plus the five-move argument.
- [Explainer](explainer.md) — plain-language walkthrough with jargon decoder.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, applicability, verdict.
- [Questions](questions.md) — retrieval practice Q1–Q7 with answers.

## Wiki

| Page | Covers |
|------|--------|
| [01-overview](wiki/01-overview.md) | README model statement, features, updates, install, CLI/Python API, demo/server/benchmark, training |
| [02-top-level-files](wiki/02-top-level-files.md) | Repo root config: .gitignore, pre-commit hooks, licenses/attribution/NOTICE, packaging and pinned dependencies |

## Original Source

- Upstream: <https://github.com/herimor/voxtream>
- Local copy: [source/source.md](source/source.md)
