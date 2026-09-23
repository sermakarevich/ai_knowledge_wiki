---
type: index
title: Ankur2606/Low-latency-AI-Voice-Assistant
description: Folder index for the Low-latency-AI-Voice-Assistant repo snapshot — VAD-gated faster-whisper STT, concise Hugging Face LLM replies, and tunable Edge-TTS with terminal and Streamlit run modes.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T16:54:14Z
sources:
  - id: original
    resource: https://github.com/Ankur2606/Low-latency-AI-Voice-Assistant
  - id: local-copy
    resource: source/source.md
tags: [voice-assistant, speech-to-text, text-to-speech, low-latency]
filed_via: "ask_human (jev choose: agent_harness @ 0.56, below 0.7 floor)"
---

# Ankur2606/Low-latency-AI-Voice-Assistant

This folder documents an end-to-end voice assistant that chains faster-whisper speech-to-text, a concise Hugging Face LLM reply capped at 60 tokens / 2 sentences, and tunable Edge-TTS speech output. It covers a VAD-gated pipeline with terminal (`python main.py`) and Streamlit (`streamlit run app.py`) run modes and a sub-500 ms latency design goal. Start with the summary for the two-minute picture, use the digest for verbatim key facts, then go deep in the wiki pages.

## How to work through this

1. Start with the summary (~2 min) for the TL;DR, problem and motivation, main ideas, and key findings.
2. Move to the digest (~10 min) for the verbatim key points per wiki page plus the system in five moves.
3. Go deep in the wiki pages for full configuration, entry-point behavior, and setup detail, then use the explainer, critical thinking, and questions pages to check understanding.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem and motivation, architecture, pipeline, files, dependencies, usage, and limitations.
- [Digest](digest.md) — verbatim key points per wiki page and the system in five moves.
- [Explainer](explainer.md) — plain-language walkthrough of what it is, why it matters, and how it works.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, applicability, verdict.
- [Questions](questions.md) — retrieval practice Q1–Q7 with answers linked to the wiki pages.

## Wiki

| Page | Covers |
| --- | --- |
| [01-overview](wiki/01-overview.md) | Pipeline stages, entry points, model configuration (STT/LLM/TTS), latency, setup, and operations |
| [02-top-level-files](wiki/02-top-level-files.md) | `app.py`, `main.py`, `.env.example`, `.gitignore`, `packages.txt`, `requirements.txt` |

## Original Source

- Upstream: [Ankur2606/Low-latency-AI-Voice-Assistant](https://github.com/Ankur2606/Low-latency-AI-Voice-Assistant)
- Local copy: [source/source.md](source/source.md)
