---
type: index
title: remsky/Kokoro-FastAPI
description: Folder index for the Kokoro-FastAPI repo analysis — Dockerized FastAPI wrapper for Kokoro-82M with an OpenAI-compatible speech endpoint, voice mixing, streaming, and multiplatform CPU/GPU serving.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T16:46:55Z
sources:
  - id: original
    resource: https://github.com/remsky/Kokoro-FastAPI
  - id: local-copy
    resource: source/source.md
tags: [text-to-speech, openai-compatible-api, docker-deployment, voice-mixing]
filed_via: ask_human (jev choose top: models, confidence: 0.57; human confirmed: models)
---

# remsky/Kokoro-FastAPI

This folder distills the `remsky/Kokoro-FastAPI` repository — a Dockerized FastAPI wrapper around the Kokoro-82M text-to-speech model exposing an OpenAI-compatible speech endpoint. It covers multi-language synthesis, voice mixing and aliasing, streaming audio with captions, and multiplatform serving across CPU, NVIDIA GPU, experimental ROCm, and Apple Silicon.

## How to work through this

1. Start with the **summary (~2 min)** for the TL;DR: problem, architecture, voice model, pipeline, and key files.
2. Move to the **digest (~10 min)** for per-page one-sentence takeaways, verbatim key points, and the system in five moves.
3. Go deeper with the **wiki pages** in order (overview → top-level files), then the **explainer** for plain-language background, **critical_thinking** for claims-vs-evidence analysis, and **questions** for retrieval practice.

## Read This Folder

- [Summary](summary.md) — technical analysis: overview, architecture, voicepack, pipeline, key files, dependencies, usage, extensibility, gotchas.
- [Digest](digest.md) — per-wiki-page one-sentence summaries, verbatim key points, and the system in five moves.
- [Explainer](explainer.md) — plain-language guide: what it is, why it matters, how it works, where to use it.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, applicability, verdict.
- [Questions](questions.md) — retrieval-practice Q&A covering both wiki pages plus a scenario question.

## Wiki

| Page | Covers |
|---|---|
| [01-overview](wiki/01-overview.md) | README.md (project purpose, feature list, docker run / compose / uv run paths, OpenAI-compatible usage, streaming, output formats) as given in `chunks/01-overview.md` |
| [02-top-level-files](wiki/02-top-level-files.md) | `.codeql-config.yml`, `.coveragerc`, `.dockerignore`, `.gitattributes`, `.gitignore`, `.python-version`, `.ruff.toml`, `AGENTS.md`, `codecov.yml`, `debug.http`, `docker-bake.hcl`, `package-lock.json`, `playwright.config.mjs`, `pytest.ini`, `start-cpu.ps1`, `start-cpu.sh`, `start-gpu.ps1`, `start-gpu.sh`, `start-gpu_mac.sh`, `VERSION` |

## Original Source

- Upstream: <https://github.com/remsky/Kokoro-FastAPI>
- Local copy: [source/source.md](source/source.md)
