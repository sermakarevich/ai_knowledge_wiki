---
type: index
title: Akshat21Shah/e3-tts-assessment
description: Real-time streaming voice agent pairing Qwen3-TTS with a fused 28-layer CUDA megakernel; TTFC ~36 ms and RTF ~0.13 on RTX 5090 via a rented-GPU FastAPI server and Pipecat laptop pipeline.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T17:25:53Z
sources:
  - id: original
    resource: https://github.com/Akshat21Shah/e3-tts-assessment
  - id: local-copy
    resource: source/source.md
tags: [text-to-speech, cuda, voice-agent, gpu-optimization]
---

# Akshat21Shah/e3-tts-assessment

A real-time mic-to-speaker voice agent (Deepgram STT → Groq LLaMA-3.3-70B → Qwen3-TTS) whose talker decode is fused into a single CUDA megakernel, cutting per-step cost from ~20 ms to 0.86 ms. Headline result: time-to-first-chunk ~35–38 ms and RTF ~0.12–0.15 on RTX 5090, served from a rented GPU over an SSH tunnel. Start with the summary, use the digest for verbatim numbers, then work the two wiki pages for setup and kernel detail.

## How to work through this

1. **Summary (~2 min):** read `summary.md` for the problem, architecture, key files, and limitations.
2. **Digest (~10 min):** read `digest.md` for the verbatim key points per wiki page plus the system in five moves.
3. **Wiki pages:** read `wiki/01-overview.md` then `wiki/02-top-level-files.md` for full pipeline, kernel adaptations, and dependency detail; use `explainer.md`, `critical_thinking.md`, and `questions.md` to check understanding.

## Read This Folder

- [Summary](summary.md) — technical TL;DR, architecture, pipeline, files, dependencies, limitations.
- [Digest](digest.md) — verbatim key points per wiki page plus the system in five moves.
- [Explainer](explainer.md) — plain-language walkthrough with jargon decoder.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, weaknesses, applicability, verdict.
- [Questions](questions.md) — retrieval practice (Q1–Q8) covering both wiki pages.

## Wiki

| Page | Covers |
|------|--------|
| [Overview](wiki/01-overview.md) | README.md overview: voice-agent pipeline and metrics, architecture decisions, megakernel adaptations, GPU-server and local-Mac setup |
| [top-level-files](wiki/02-top-level-files.md) | `.gitignore`, `requirements.txt` |

## Original Source

- Upstream: [https://github.com/Akshat21Shah/e3-tts-assessment](https://github.com/Akshat21Shah/e3-tts-assessment)
- Local copy: [source/source.md](source/source.md)
