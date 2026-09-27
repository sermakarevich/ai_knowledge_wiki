---
type: index
title: sgl-project/sglang-omni
description: Folder index for the SGLang-Omni multi-stage omni/speech/TTS serving runtime snapshot.
generated:
  by: claude/muse-spark-1.3-contributor
  at: "2026-09-22T17:37:10Z"
sources:
  - id: original
    resource: https://github.com/sgl-project/sglang-omni
  - id: local-copy
    resource: source/source.md
tags: [model-serving, text-to-speech, speech-recognition, multimodal]
---

# sgl-project/sglang-omni

SGLang-Omni is a multi-stage serving runtime for omni, speech, and TTS models that owns pipeline topology, stage lifecycle, inter-stage transport, and an OpenAI-compatible serving surface while composing with SGLang for autoregressive execution. This folder holds a summary, a verbatim digest, two wiki pages, a plain-language explainer, a critical analysis, and retrieval questions. Start with the summary for orientation, then go deeper via the digest and wiki pages.

## How to work through this

1. **Summary (~2 min)** — read `summary.md` for the TL;DR, problem/motivation, architecture, and key findings.
2. **Digest (~10 min)** — read `digest.md` for the verbatim condensed snapshot (overview stages/schedulers/transports plus top-level packaging) and the system in five moves.
3. **Wiki pages** — open each page in `wiki/` in order for full detail, then use `explainer.md`, `critical_thinking.md`, and `questions.md` to check understanding.

## Read This Folder

- [Summary](summary.md) — TL;DR and key findings for the SGLang-Omni snapshot.
- [Digest](digest.md) — verbatim condensed snapshot plus the system in five moves.
- [Explainer](explainer.md) — plain-language walkthrough (what it is, why it matters, how the pipeline works).
- [Critical thinking](critical_thinking.md) — claims vs. evidence, weaknesses, applicability, and verdict.
- [Questions](questions.md) — retrieval prompts with answers covering the full snapshot.

## Wiki

| Page | Covers |
|---|---|
| [01-overview](wiki/01-overview.md) | README.md (About, What SGLang-Omni Serves, Hardware Support, Quick Start, Community & Support, Acknowledgments) |
| [02-top-level-files](wiki/02-top-level-files.md) | `.dockerignore`, `.editorconfig`, `.gitignore`, `.isort.cfg`, `.pre-commit-config.yaml`, `AGENTS.md`, `CLAUDE.md`, `install.sh` (tail truncated in chunk), `pyproject_cpu.toml`, `pyproject_npu.toml`, `pyproject_rocm.toml`, `pyproject_xpu.toml` |

## Original Source

- Upstream: [https://github.com/sgl-project/sglang-omni](https://github.com/sgl-project/sglang-omni)
- Local copy: [source/source.md](source/source.md)
