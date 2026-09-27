---
type: Index
title: dreamtheater123/TurnGuide
description: Index for the TurnGuide repo notes — inference demo and Fisher/Candor test splits for coherent full-duplex dialogue via turn-level text-speech interleaving.
generated:
  by: claude/opencode-go/muse-spark-1.3-contributor
  at: 2026-09-22T17:44:06Z
sources:
- id: original
  resource: https://github.com/dreamtheater123/TurnGuide
- id: local-copy
  resource: source/source.md
tags: [full-duplex-dialogue, speech-language-models, text-speech-interleaving, inference-demo]
---

# dreamtheater123/TurnGuide

TurnGuide is an end-to-end full-duplex speech language model that keeps simultaneous dialogue coherent via dynamic turn-level text-speech interleaving. This folder collects notes on its inference-demo release (Interspeech 2026 paper) with Fisher/Candor test splits. Start here to orient yourself, then drill into the summary, digest, and wiki pages for runnable details.

## How to work through this

Read the summary (~2 min) for the TL;DR and motivation, then the digest (~10 min) for the full verbatim fact set and the system in five moves, then the wiki pages for detailed per-file evidence, commands, and environment pins.

## Read This Folder

- [[summary|Summary]] — TL;DR, problem and motivation, architecture, pipeline, files, dependencies, usage, limits.
- [[digest|Digest]] — verbatim fact set plus the system in five moves.
- [[explainer|Explainer]] — background and intuition for the approach.
- [[critical_thinking|Critical thinking]] — strengths, limits, and open questions.
- [[questions|Questions]] — retrieval practice (Q1–Q7) covering all wiki pages.

## Wiki

| Page | Covers |
|---|---|
| [[wiki/01-overview\|01-overview]] | README.md (repo overview, inference demo, checkpoints, environment, inference command, data, license/citation) |
| [[wiki/02-top-level-files\|02-top-level-files]] | `.gitattributes`, `.gitignore`, `environment.yml`, `requirements.txt`, `flow_inference.py`, `turnguide_inference.py` (partial, truncated), `turnguide_inference_reproducible.py` (partial, truncated) |

## Original Source

- Upstream repository: [dreamtheater123/TurnGuide](https://github.com/dreamtheater123/TurnGuide)
- Local copy: [source/source.md](source/source.md)
