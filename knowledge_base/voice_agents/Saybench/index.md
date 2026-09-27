---
type: index
title: renan-martini/saybench
description: Folder index for the saybench voice-AI pipeline benchmark notes: summary, digest, explainer, critical analysis, questions, and wiki pages.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T17:31:35Z
sources:
  - id: original
    resource: https://github.com/renan-martini/saybench
  - id: local-copy
    resource: source/source.md
tags: [voice-AI, benchmarking, speech-recognition, latency]
---

# renan-martini/saybench

Saybench is a single-static-binary Go harness that benchmarks the full voice-AI pipeline on your own audio across batch STT, streaming STT, LLM turns, speech-to-speech, and TTS. This folder holds a 2-minute summary, a 10-minute digest of verbatim key points, a plain-language explainer, a critical analysis, retrieval questions, and two wiki pages with full runnable detail. Start with the summary, then use the digest and wiki pages for verbatim findings and the measure-compare-gate workflow.

## How to work through this

- Summary (~2 min): read `summary.md` for the problem, the five benchmark modes, the measure-compare-gate pipeline, and golden-set findings.
- Digest (~10 min): read `digest.md` for the verbatim key points per wiki page plus the argument in five moves.
- Wiki pages: read `wiki/01-overview.md` then `wiki/02-top-level-files.md` for the full tables, verbatim quickstart sequence, documentation map, guardrails, and shipped history.
- Then use `explainer.md` for plain-language background, `critical_thinking.md` for claims-vs-evidence scrutiny, and `questions.md` for retrieval practice.

## Read This Folder

- [Summary](summary.md) — technical analysis: problem space, architecture, modes, providers, workflow, and limitations.
- [Digest](digest.md) — verbatim key points per wiki page and the system in five moves.
- [Explainer](explainer.md) — plain-language guide: what saybench is, why per-failure-mode and live-call numbers matter, how the workflow runs.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, blind spots, applicability, verdict.
- [Questions](questions.md) — seven retrieval questions covering modes, scoring, findings, quickstart, guardrails, roadmap, and adoption.

## Wiki

| Page | Covers |
|---|---|
| [01-overview](wiki/01-overview.md) | Five benchmark modes, cross-mode capabilities, golden-set findings, install and quickstart, documentation map, design principles |
| [02-top-level-files](wiki/02-top-level-files.md) | Repo-root guardrails and history: CLAUDE.md rules, SECURITY.md posture, .gitignore, go.sum pin, ROADMAP.md shipped log |

## Original Source

- Upstream: [renan-martini/saybench](https://github.com/renan-martini/saybench)
- Local copy: [source/source.md](source/source.md)
