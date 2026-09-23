---
type: index
title: AI Native Call Center
description: Folder index for the ai-native-callcenter repository digest — AI-first voice answering, flow-steered dialogue, and queue-native human handover.
generated:
  by: claude/opencode-go/muse-spark-1.3-contributor
  at: "2026-09-22T14:11:00Z"
sources:
  - id: original
    resource: https://github.com/rasonyang/ai-native-callcenter
  - id: local-copy
    resource: source/source.md
tags: [voice-ai, ai-call-center, freeswitch, realtime-speech, human-handover]
---

# AI Native Call Center

rasonyang/ai-native-callcenter is an open-source, AI-first call center where a voice model answers every inbound call over a provider-native speech-to-speech connection and escalates to human agents in real FreeSWITCH queues. Dialogue is steered by a flow engine where the model owns the words and the flow owns the phase, and every conversation — bot leg, queue wait, and agent leg — is unified into one call record. This folder holds a layered reading path: a 2-minute summary, a 10-minute digest of verbatim key points, one wiki page covering the repository snapshot, plus explainer, critical-thinking, and retrieval-practice files.

## How to work through this

1. Start with the summary (~2 min) for the TL;DR, problem and motivation, main ideas, and key findings.
2. Move to the digest (~10 min) for verbatim key points plus the argument in five moves.
3. Go deeper with the wiki page(s), then the explainer, critical-thinking notes, and retrieval questions.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem and motivation, main ideas, key findings.
- [Digest](digest.md) — verbatim key points plus the argument in five moves.
- [Explainer](explainer.md) — beginner-friendly walkthrough of the ideas.
- [Critical thinking](critical_thinking.md) — strengths, limits, and open questions.
- [Questions](questions.md) — retrieval-practice prompts with answers.

## Wiki

| Page | Covers |
|------|--------|
| [AI Native Call Center](wiki/01-ai-native-call-center.md) | AI-native call center overview: model-first answering, flow engine, human handover, single Go binary + FreeSWITCH architecture |

## Original Source

- Upstream: <https://github.com/rasonyang/ai-native-callcenter>
- Local copy: [source/source.md](source/source.md)
