---
type: index
title: KoljaB/RealtimeSTT
description: Folder index for the KoljaB/RealtimeSTT knowledge pack: summary, digest, wiki pages, and study aids.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T17:29:36Z
sources:
  - id: original
    resource: https://github.com/KoljaB/RealtimeSTT
  - id: local-copy
    resource: source/source.md
tags: [speech-to-text, realtime-asr, voice-activity-detection, wake-word]
---

# KoljaB/RealtimeSTT

RealtimeSTT is a Python speech-to-text library built around `AudioToTextRecorder`, pairing voice activity detection and wake-word gating with fast realtime hypotheses plus one authoritative final transcript. This folder holds a layered reading pack: a quick summary, a verbatim digest, two detailed wiki pages, and study aids. Start with the summary, then go deeper only where you need engine profiles, install recipes, or the production server contract.

## How to work through this

- Summary (~2 min): read [[summary|Summary]] for the TL;DR, problem, main ideas, and findings.
- Digest (~10 min): read [[digest|Digest]] for the one-sentence take plus verbatim key points and the system in five moves.
- Wiki pages (deep dives): open the pages in the Wiki table below in order for full detail with `file:line` citations.

## Read This Folder

- [[summary|Summary]] — human-readable TL;DR, problem and motivation, main ideas, key findings.
- [[digest|Digest]] — one-sentence take, verbatim key points, system in five moves.
- [[explainer|In Plain Language]] — plain-language explainer with jargon decoder.
- [[critical_thinking|Critical Analysis]] — claims vs. evidence, weaknesses, applicability, verdict.
- [[questions|Retrieval Practice]] — Q&A prompts with answers linked to wiki pages.

## Wiki table

| Page | Covers |
|---|---|
| [[wiki/01-overview\|Overview]] | README.md (library purpose, engine profiles, install, microphone/continuous/external-audio examples, configuration pointer, features, documentation map, production server, contributing/license/author) |
| [[wiki/02-top-level-files\|Top-Level Files]] | `.dockerignore`, `.gitignore`, `install_with_gpu_support.bat`, `MANIFEST.in`, `RELEASE_NOTES.md`, `requirements-gpu-torch.txt`, `requirements-gpu.txt`, `requirements.txt`, `win_installgpu_virtual_env.bat` |

## Original Source

- Upstream: [KoljaB/RealtimeSTT](https://github.com/KoljaB/RealtimeSTT) — GitHub
- Local copy: [source/source.md](source/source.md)
