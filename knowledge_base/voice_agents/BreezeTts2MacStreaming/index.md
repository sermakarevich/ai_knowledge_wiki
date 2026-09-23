---
type: index
title: breezetts2_mac_fast.py
description: Index to the summary, digest, explainer, critical analysis, retrieval questions, and wiki page for the breezetts2_mac_fast.py Mac streaming rewrite.
generated:
  by: claude/muse-spark-1.3-contributor
  at: '2026-09-22T14:27:48Z'
sources:
  - id: original
    resource: https://github.com/xzf-thu/BreezeTTS2_Mac_Streaming
  - id: local-copy
    resource: source/source.md
tags: [text-to-speech, apple-silicon, mlx, streaming-inference]
---

# breezetts2_mac_fast.py

This folder distills the `breezetts2_mac_fast.py` rewrite that fixes stuttering Breeze-TTS-2 streaming playback on Apple Silicon. The root cause is redundant depth-decoder recomputation in mlx-audio 0.5.1, not model size, and the fix pairs intra-frame KV cache reuse with RTF/underflow diagnostics. Start with the summary for the verdict, then the digest and wiki page for the mechanism, commands, and decision rules.

## How to work through this

1. Start with `summary.md` (~2 min) for the TL;DR, root cause, fixes, and findings.
2. Then read `digest.md` (~10 min) for the five-move argument and verbatim key points.
3. Then go deep on the wiki page for quick start, options, cause/fix detail, and result interpretation, using `explainer.md`, `critical_thinking.md`, and `questions.md` to check understanding.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem and motivation, fixes, findings, future directions.
- [Digest](digest.md) — compressed verbatim key points and five-move argument.
- [Explainer](explainer.md) — plain-language walkthrough with analogies and jargon decoder.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, blind spots, verdict.
- [Questions](questions.md) — 7 retrieval prompts covering RTF, root cause, fixes, and diagnostics.

## Wiki

| Page | Covers |
|------|--------|
| [01-breezetts2-mac-fast-py](wiki/01-breezetts2-mac-fast-py.md) | Rewritten streaming loop: quick start (default run, compiled fallback, emotion example, options table) and fix detail (stutter cause, code changes, validation status, RTF/result reading rules). |

## Original Source

- Upstream: https://github.com/xzf-thu/BreezeTTS2_Mac_Streaming
- Local copy: [source/source.md](source/source.md)
