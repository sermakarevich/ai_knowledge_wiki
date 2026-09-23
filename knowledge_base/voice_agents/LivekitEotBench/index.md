---
type: index
title: "livekit/eot-bench"
description: "Index for the eot-bench open benchmark for end-of-turn detection on real human-to-agent turns in 14 languages."
generated:
  by: claude/opencode-go/muse-spark-1.3-contributor
  at: "2026-09-22T16:47:07Z"
sources:
  - id: original
    resource: https://github.com/livekit/eot-bench
  - id: local-copy
    resource: source/source.md
tags: [end-of-turn-detection, voice-agents, benchmarking, multilingual-evaluation]
filed_via: "jev choose, category: evaluation_and_benchmarks, confidence: 1.0"
---

# livekit/eot-bench

eot-bench is LiveKit's open, reproducible benchmark for end-of-turn detection on real human-to-agent turns in 14 languages. Detectors are scored at every causal silence pause under explicit false-cutoff/latency budgets, where LiveKit Turn Detector v1 leads. This folder holds a 2-minute summary, a 10-minute digest, plain-language and critical readings, retrieval questions, and per-topic wiki pages.

## How to work through this

1. Start with `summary.md` (~2 min) for the TL;DR, problem, ideas, and headline results.
2. Then read `digest.md` (~10 min) for verbatim per-page key points and the five-move argument.
3. Then go deep in `wiki/` pages in order, using `explainer.md` for intuition, `critical_thinking.md` for scrutiny, and `questions.md` for retrieval practice.

## Read This Folder

- [Summary](summary.md)
- [Digest](digest.md)
- [Explainer](explainer.md)
- [Critical thinking](critical_thinking.md)
- [Questions](questions.md)

## Wiki

| Page | Covers |
| ---- | ------ |
| [01-overview](wiki/01-overview.md) | Benchmark purpose, dataset, results leaderboard, tradeoff, quick start, evaluation model, scope |
| [02-top-level-files](wiki/02-top-level-files.md) | `.gitignore`, `requirements.txt` |

## Original Source

- Upstream: [https://github.com/livekit/eot-bench](https://github.com/livekit/eot-bench)
- Local copy: [source/source.md](source/source.md)
