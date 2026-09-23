---
type: Video
title: 'TEN Framework: Voice AI That Can Actually Be Interrupted'
description: TEN Framework presented as an open-source graph-of-extensions runtime for real-time voice AI — live tests show mid-sentence interruption works, while answer quality stays rough and setup takes real work.
generated: { by: claude/muse-spark-1.3-contributor, at: 2026-09-22T08:18:13Z }
sources:
  - id: original
    resource: https://www.youtube.com/watch?v=ES3HhoYCtIc
  - id: local-copy
    resource: source/source.md
tags: [voice-ai, real-time, interruption-handling, open-source]
---

# TEN Framework: Voice AI That Can Actually Be Interrupted

TEN Framework rebuilds voice agents as a graph of single-job extensions (STT, LLM, TTS, VAD, turn detection) instead of a linear pipeline, so the agent can stop speaking and yield when you talk over it. A hands-on video test confirms mid-sentence interruption survives in practice, though answers stay imperfect and the multi-key Docker setup only pays off for genuinely live conversations.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole video, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole video, medium: headline and key points.
3. **Wiki pages below** (~5 min each) — one chunk, deep. Each opens with its headline and key points, so you can stop early.

_New to the field? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

## Read This Folder

- [[summary|Summary]] — rung 1: the whole video, shallow
- [[digest|Digest]] — rung 2: the whole video at medium depth; the file to re-read on review
- [[explainer|Plain-Language Explainer]] — no-jargon explanation, applications, conclusions
- [[critical_thinking|Critical Analysis]] — claims vs. evidence, applicability, what it changes, verdict
- [[questions|Retrieval Practice]] — self-test questions; **answer these from memory before re-reading anything**

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-is-this-one-of-the-best\|Is this one of the best]] | TEN framing and interruption test plan; graph-of-extensions vs. STT→LLM→TTS chain; Agora/Deepgram/LLM/ElevenLabs setup and ready-made configs; live barge-in tests; designer tool and when to use TEN |

## Original Source

- [TEN Framework: Voice AI That Can Actually Be Interrupted](https://www.youtube.com/watch?v=ES3HhoYCtIc) — original YouTube video
- [source/source.md](source/source.md) — local transcript copy
