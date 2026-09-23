---
type: index
title: alphaparkinc/genpark-voice-turn-taking-endpointing-detector-skill
description: Zero-dependency Python voice turn-taking skill — energy-gated VAD, silence endpointing, and barge-in arbitration emitting a three-way listen/interrupt/dispatch decision.
generated:
  by: claude/opencode-go/muse-spark-1.3-contributor
  at: 2026-09-22T14:58:52Z
sources:
  - id: original
    resource: https://github.com/alphaparkinc/genpark-voice-turn-taking-endpointing-detector-skill
  - id: local-copy
    resource: source/source.md
tags: [voice-activity-detection, turn-taking, endpointing, barge-in, mcp]
---

# alphaparkinc/genpark-voice-turn-taking-endpointing-detector-skill

A zero-dependency Python skill that classifies each audio frame by energy against a dB threshold and emits one of three turn-taking decisions: keep listening, cut agent audio on barge-in, or dispatch the completed turn to LLM synthesis. This folder holds a shallow summary, a medium-depth digest, and per-slice wiki pages covering the repo overview and the detector, demo, MCP wrapper, and manifest files.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole repo snapshot, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole snapshot at medium depth: the headline and key points of every section.
3. **Wiki pages below** (~5 min each) — one slice, deep. Each opens with its headline and key points, so you can stop early.

_New to the topic? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

## Read This Folder

- [[summary|Summary]] — rung 1: the whole snapshot, shallow
- [[digest|Digest]] — rung 2: the whole snapshot at medium depth; the file to re-read on review
- [[explainer|Plain-Language Explainer]] — no-jargon explanation, applications, conclusions
- [[critical_thinking|Critical Analysis]] — claims vs. evidence, applicability, what it changes, verdict
- [[questions|Retrieval Practice]] — self-test questions; **answer these from memory before re-reading anything**

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-overview\|01-overview]] | README.md (repo overview, architecture diagram, features) |
| [[wiki/02-top-level-files\|02-top-level-files]] | client.py, example_usage.py, mcp_server.py, skill.json, requirements.txt, .gitignore |

## Original Source

- Original: https://github.com/alphaparkinc/genpark-voice-turn-taking-endpointing-detector-skill
- Local copy: [source/source.md](source/source.md) — scraped repo page snapshot
