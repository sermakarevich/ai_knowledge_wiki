---
type: index
title: OpenBMB/VoxCPM
description: Folder index for the VoxCPM2 tokenizer-free multilingual TTS repo — summary, digest, wiki pages, explainer, critical analysis, and retrieval questions.
generated:
  by: claude/muse-spark-1.3-contributor
  at: '2026-09-22T17:47:49Z'
sources:
  - id: original
    resource: https://github.com/OpenBMB/VoxCPM
  - id: local-copy
    resource: source/source.md
tags: [text-to-speech, voice-cloning, multilingual, diffusion]
---

# OpenBMB/VoxCPM

This folder distills the OpenBMB/VoxCPM repository into a guided reading path for VoxCPM2, a 2B-parameter tokenizer-free multilingual text-to-speech system. It covers Voice Design from text descriptions, Controllable and Ultimate voice cloning from short clips, and 48 kHz output via AudioVAE V2. Start with the summary, deepen with the digest, then go file-by-file in the wiki.

## How to work through this

1. Read `summary.md` (~2 min) for the big picture: problem, architecture, modes, and serving paths.
2. Read `digest.md` (~10 min) for verbatim per-page key points plus the system in five moves.
3. Read the wiki pages in order for full evidence: repo overview first, then top-level files.

## Read This Folder

- [Summary](summary.md) — technical TL;DR: problem, architecture, request model, pipeline, files, and gotchas.
- [Digest](digest.md) — verbatim per-page key points plus the system in five moves.
- [Explainer](explainer.md) — plain-language guide: what VoxCPM2 is, why it matters, how it works, where to use it.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, new vs. repackaged, weaknesses, applicability, verdict.
- [Questions](questions.md) — 7 retrieval prompts with answers covering both wiki pages.

## Wiki

| Page | Covers |
|---|---|
| [01-overview](wiki/01-overview.md) | Tokenizer-free diffusion-AR architecture, VoxCPM2 scale (2B, MiniCPM-4, 2M+ hours), Voice Design / Controllable / Ultimate cloning, 30 languages + 9 Chinese dialects, 48 kHz AudioVAE V2, install + Python API + CLI + streaming + web demo + Nano-vLLM serving |
| [02-top-level-files](wiki/02-top-level-files.md) | Current VoxCPM2 Gradio demo (app.py), legacy VoxCPM1.5 demo (app_old.py), LoRA fine-tune/inference WebUI (lora_ft_webui.py), Chinese README (install, API, CLI, deployment), .dockerignore / .gitignore rules |

## Original Source

- Upstream: [https://github.com/OpenBMB/VoxCPM](https://github.com/OpenBMB/VoxCPM)
- Local copy: [source/source.md](source/source.md)
