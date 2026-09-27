---
type: index
title: xcc-zach/xtalk
description: Folder index for xcc-zach/xtalk — a full-duplex cascaded spoken-dialogue framework; orientation, reading order, and links to summary, digest, wiki, and sources.
generated:
  by: claude/opencode-go/muse-spark-1.3-contributor
  at: 2026-09-22T17:59:04Z
sources:
  - id: original
    resource: https://github.com/xcc-zach/xtalk
  - id: local-copy
    resource: source/source.md
tags: [spoken-dialogue, full-duplex, speech-to-speech, low-latency]
---

# xcc-zach/xtalk

X-Talk is an open-source, pure-Python cascaded spoken-dialogue framework (ASR → LLM agent → TTS) built for low-latency, interruptible voice conversation. This folder captures its features, AliCloud quickstart path, demo configuration, and repo hygiene/toolchain metadata. Coverage is README-level plus top-level config files; no pipeline internals are covered, so treat latency and interruption claims as unverified.

## How to work through this

1. **Summary (~2 min):** read `summary.md` for the TL;DR, architecture, pipeline, and limitations.
2. **Digest (~10 min):** read `digest.md` for the verbatim key points per wiki page and the system in five moves.
3. **Wiki pages:** read each page in `wiki/` in order for full detail, then use `explainer.md`, `critical_thinking.md`, and `questions.md` to check understanding.

## Read This Folder

- [Summary](summary.md) — technical analysis: overview, architecture, pipeline, files, dependencies, limitations.
- [Digest](digest.md) — verbatim key points per wiki page plus the five-move synthesis.
- [Explainer](explainer.md) — plain-language walkthrough of the framework and its use cases.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, weaknesses, applicability, verdict.
- [Questions](questions.md) — retrieval practice with answers covering every wiki page.

## Wiki

| Page | Covers |
|---|---|
| [01-overview](wiki/01-overview.md) | `README.md`: features, demo matrix, install, AliCloud quickstart (ASR/LLM/TTS config, server launch) |
| [02-top-level-files](wiki/02-top-level-files.md) | Top-level files: `.gitattributes`, `.gitignore`, pre-commit pins, ReadTheDocs build, `AGENTS.md` rules, `mkdocs.yml` docs site |

## Original Source

- Original: [https://github.com/xcc-zach/xtalk](https://github.com/xcc-zach/xtalk)
- Local copy: [source/source.md](source/source.md)
