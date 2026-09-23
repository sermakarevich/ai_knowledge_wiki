---
type: index
title: alphaparkinc/genpark-neural-speech-codec-full-duplex-dialogue-engine-skill
description: Folder index for the GenPark neural speech codec full-duplex dialogue engine skill notes (summary, digest, wiki, explainer, critique, questions).
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T15:00:46Z
sources:
  - id: original
    resource: https://github.com/alphaparkinc/genpark-neural-speech-codec-full-duplex-dialogue-engine-skill
  - id: local-copy
    resource: source/source.md
tags:
  - full-duplex-dialogue
  - neural-speech-codec
  - realtime-voice
  - agent-skills
---

# alphaparkinc/genpark-neural-speech-codec-full-duplex-dialogue-engine-skill

This folder collects notes on a GenPark AI Agent Skill that packages a Moshi-style neural speech codec full-duplex dialogue engine behind a JSON-in / structured-out contract with an MCP stub. The snapshot analyzed is a deterministic stub returning fixed telemetry (160 ms latency, 12.5 Hz framing), not a working codec. Start with the summary for the big picture, then use the digest and wiki pages for verifiable details.

## How to work through this

- Start with the summary (~2 min) for the TL;DR, problem space, architecture, and limitations.
- Then read the digest (~10 min) for the verbatim per-section breakdown and the five-move system view.
- Then go into the wiki pages for file-level tables, verbatim snippets, the plain-language explainer, critique, and retrieval practice.

## Read This Folder

- [Summary](summary.md) — overview, architecture, duplex turn, pipeline, key files, limitations, and comparisons.
- [Digest](digest.md) — verbatim per-section digest of the wiki snapshot plus the system in five moves.
- [Explainer](explainer.md) — plain-language walkthrough of full-duplex dialogue, the request flow, and use cases.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, repackaging check, weaknesses, applicability, verdict.
- [Questions](questions.md) — retrieval practice (Q1–Q7) with answers linked to the wiki pages.

## Wiki

| Page | Covers |
|------|--------|
| [01-overview](wiki/01-overview.md) | README-level purpose, quick start, JSON→Skill→Core-Engine diagram, MCP entry point, macro-component list |
| [02-top-level-files](wiki/02-top-level-files.md) | skill.json manifest, client.py duplex-turn payload, example_usage.py demo, mcp_server.py stub, requirements.txt, .gitignore |

## Original Source

- Upstream: https://github.com/alphaparkinc/genpark-neural-speech-codec-full-duplex-dialogue-engine-skill
- Local copy: [source/source.md](source/source.md)
