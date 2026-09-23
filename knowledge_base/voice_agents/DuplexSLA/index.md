---
type: index
title: hyzhang24/DuplexSLA
description: Folder index for the DuplexSLA repo snapshot — a full-duplex speech-language-action model on a shared 160 ms clock, with technical report released and code, checkpoints, and bench still pending.
generated:
  by: claude/opencode-go/muse-spark-1.3-contributor
  at: 2026-09-22T14:37:17Z
sources:
  - id: original
    resource: https://github.com/hyzhang24/DuplexSLA
  - id: local-copy
    resource: source/source.md
tags: [full-duplex, spoken-language-model, turn-taking, tool-calling]
---
# hyzhang24/DuplexSLA

DuplexSLA is a native full-duplex Speech–Language–Action model that jointly decodes assistant audio and a rate-limited action stream on a shared 160 ms chunk timeline. The snapshot analyzed here is a release stub: the technical report is out, while inference code, checkpoints, and DuplexSLA-Bench are still pending. Start with the summary, then the digest, then the wiki pages for verbatim detail.

## How to work through this

1. Start with the summary (~2 min) for the TL;DR, problem, key ideas, and release status.
2. Move to the digest (~10 min) for the sourced key points and the argument in five moves.
3. Go deep with the wiki pages for verbatim claims, snapshot detail, and citation, plus the explainer, critical thinking, and questions.

## Read This Folder

- [[summary|Summary]] — TL;DR, problem and motivation, main ideas, findings, and future directions.
- [[digest|Digest]] — sourced key points per wiki page and the argument in five moves.
- [[explainer|Explainer]] — plain-language walkthrough: what it is, why it matters, how it works, and where it applies.
- [[critical_thinking|Critical Thinking]] — claims vs. evidence, novelty, weaknesses, applicability, and verdict.
- [[questions|Questions]] — retrieval practice with seven questions covering the wiki pages.

## Wiki

| Page | Covers |
| --- | --- |
| [[wiki/01-overview\|Overview]] | `README.md`, `DuplexSLA.pdf`, `LICENSE`, `assets/architecture.png` — dual-stream three-channel formulation, highlights, open-source plan, citation |
| [[wiki/02-top-level-files\|Top-level-files]] | `.gitignore` (58 lines) — OS, Python, environment, IDE, log, weight, and cache exclusions |

## Original Source

- Upstream: https://github.com/hyzhang24/DuplexSLA
- Local copy: [source/source.md](source/source.md)
