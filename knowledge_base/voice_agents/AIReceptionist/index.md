---
type: Index
title: AI Receptionist -- Open Source, Self-Hosted, No Compromises
description: Index to the AIReceptionist folder — open-source, self-hosted AI phone receptionist on OpenAI Realtime speech-to-speech via LiveKit/SIP, per-business YAML configs, and metered per-minute cost.
generated:
  by: claude/opencode-go/muse-spark-1.3-contributor
  at: 2026-09-22T14:06:52Z
sources:
  - id: original
    resource: https://github.com/kirklandsig/AIReceptionist
  - id: local-copy
    resource: source/source.md
tags: [openai-realtime, self-hosted-voice-agent, livekit-sip, ai-receptionist]
---

# AI Receptionist -- Open Source, Self-Hosted, No Compromises

AIReceptionist is an open-source, self-hosted AI phone receptionist that answers business calls with direct speech-to-speech voice (OpenAI Realtime API `gpt-realtime-2.1`) over LiveKit plus a SIP trunk, instead of a cascaded STT-LLM-TTS pipeline. One agent process serves many businesses via per-number YAML configs covering greeting, hours, FAQs, routing, and voice, with message taking, recording/transcripts, multi-language auto-detect, and Google Calendar booking at metered per-minute cost. Start with the summary for the pitch, then the digest and wiki pages for setup and operational detail — noting the 2026-06-03 Realtime Beta sunset that forces `api_key` auth.

## How to work through this

1. **Summary (~2 min)** — the TL;DR, problem and motivation, main ideas, key findings, and future directions.
2. **Digest (~10 min)** — condensed briefs of each wiki page (one-sentence plus key points, verbatim) plus the argument in five moves.
3. **Wiki pages** — full detail per topic with verbatim quotes and covers markers; use the explainer for plain language, critical thinking for claims vs. evidence, and questions for retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem and motivation, main ideas, key findings.
- [Digest](digest.md) — condensed briefs of each wiki page plus the five-move argument.
- [Explainer](explainer.md) — plain-language walkthrough with jargon decoder.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, weaknesses, applicability, verdict.
- [Questions](questions.md) — retrieval practice (Q1–Q7 with answers).

## Wiki

| Page | Covers |
|---|---|
| [01-ai-receptionist-open-source-self-hosted-no-compr](wiki/01-ai-receptionist-open-source-self-hosted-no-compr.md) | Project overview, 2026-06-03 Realtime Beta sunset notice, Why This Exists, SaaS comparison table, features, prerequisites, quick start, per-business YAML configuration, Realtime auth, message delivery channels, call recording and transcripts |
| [02-email-delivery](wiki/02-email-delivery.md) | Email delivery config (SMTP/Resend, on_message/on_call_end triggers), multi-language auto-detect, retention sweeps, multi-business setup, metered cost model, Google Calendar appointment booking (with on_booking trigger), Asterisk SIP transfer-URI override, alternatives, AGPL-3.0 license |

## Original Source

- GitHub: [kirklandsig/AIReceptionist](https://github.com/kirklandsig/AIReceptionist)
- Local copy: [source/source.md](source/source.md)
