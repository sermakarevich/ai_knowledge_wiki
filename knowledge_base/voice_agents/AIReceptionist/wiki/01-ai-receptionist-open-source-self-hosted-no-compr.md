[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# AI Receptionist -- Open Source, Self-Hosted, No Compromises
**In one sentence:** A production-grade, self-hosted, AGPL-3.0 open-source AI receptionist built on OpenAI's Realtime speech-to-speech API via LiveKit and SIP replaces $200-500/month cascaded-pipeline SaaS products with sub-second, near-human phone answering with no platform fee or vendor lock-in.
## Key points
- Direct speech-to-speech via OpenAI Realtime API (the model behind ChatGPT Advanced Voice) eliminates the STT-to-LLM-to-TTS cascade, giving sub-second responses and model-native turn-taking instead of 1-3 second multi-hop delays.
- Self-hosted on the operator's infrastructure with standard SIP (Twilio/Telnyx trunk, LiveKit server) keeps call flows, prompts, and caller data under operator control with no vendor lock-in.
- Costs only metered OpenAI API-key usage per minute with no $200-500/month subscription, platform markup, per-seat pricing, or per-minute SaaS overages.
- One agent process serves multiple businesses, with each phone number routed to its own YAML config covering hours, FAQs, routing, voice, and personality.
- Requires Python 3.11+, a standard `sk-...` OpenAI API key with Realtime access, a LiveKit server, and a SIP trunk provider with a phone number; ChatGPT/Codex OAuth (`oauth_codex`) no longer authenticates Realtime after the 2026-06-03 Beta sunset.
- Customization is a YAML file per business (`business`, `voice`, `greeting`, `personality`, `hours`, `after_hours_message`, `routing`, `faqs`, `messages`) plus recording/transcript and multi-channel message delivery (file, email, webhook) sections — no code changes or dashboard feature requests.
- Active-development status: core voice conversations, FAQ answering, call transfers, and message taking work, but breaking changes and rough edges are expected.
---
## Overview
A production-grade, open-source AI receptionist that answers business phone calls using OpenAI's Realtime API — "the same speech-to-speech model that powers ChatGPT Advanced Voice. Self-hosted. No vendor lock-in. No monthly SaaS fees bleeding you dry."

> "This is not another cascaded STT-to-LLM-to-TTS hack. This is a direct speech-to-speech AI voice agent built on the highest-fidelity model available today, connected to your phone system via LiveKit and SIP."

> "If you have been paying $200-500/month for a SaaS AI receptionist that sounds robotic, interrupts callers, and takes 2 seconds to respond -- stop. Deploy this instead."

> "**This project is in active development.** Core functionality works (voice conversations, FAQ answering, call transfers, message taking), but expect breaking changes and rough edges. Contributions welcome."

> "⚠️ **2026-06-03 — OpenAI sunset the Realtime *Beta* API.** The GA Realtime API requires a standard OpenAI API key (`sk-...`). **ChatGPT/Codex OAuth (`voice.auth.type: oauth_codex`) no longer authenticates Realtime** — deployments using it will connect the call but the caller hears silence. Set `voice.auth.type: api_key` and `voice.model: gpt-realtime-2.1`."

## Why this exists
SaaS products named in the chunk — Bland AI, Vapi, Retell AI, Smith.ai, Ruby Receptionist — share these problems:
- **High latency:** cascaded transcribe → LLM → TTS pipeline; each hop adds latency.
- **Robotic voices:** cheap TTS sounds "like a GPS navigator reading a script"; callers hang up.
- **Poor turn-taking:** interruptions, talking over callers, awkward silences; no natural rhythm.
- **Expensive subscriptions:** $200-500/month "for what amounts to a wrapper around the same APIs you can call directly."
- **Vendor lock-in:** call flows, prompts, business logic, and caller data live on someone else's servers.
- **No data privacy:** callers' conversations, phone numbers, and messages sit in a third-party database.
- **Limited customization:** changes to transfers or integrations require feature requests.

This project answers each with:
- **OpenAI Realtime API (speech-to-speech):** model hears the caller and speaks back directly; sub-second response, natural turn-taking.
- **Self-hosted:** runs on your infrastructure; data stays on your servers.
- **No monthly SaaS fee:** standard `sk-...` API key; no platform markup, per-seat pricing, or "enterprise tier" upsell.
- **Fully configurable:** business hours, FAQs, call routing, voice selection, personality in one YAML file; redeploy in seconds.
- **Multi-business from a single deployment:** one agent process, each phone number routed to its own config.
- **Open source under AGPL-3.0:** fork, modify, extend; derivatives cannot be locked behind a paywall without releasing changes.

## Comparison: this vs. SaaS AI receptionists
| | **AIReceptionist (this project)** | **Typical SaaS AI Receptionist** |
|---|---|---|
| **Voice fidelity** | OpenAI Realtime speech-to-speech -- near-human quality | Cascaded STT + LLM + TTS -- robotic, high latency |
| **Response latency** | Sub-second (direct speech-to-speech) | 1-3 seconds (multi-hop pipeline) |
| **Turn-taking** | Natural, model-native | Awkward pauses, interruptions |
| **Monthly cost** | OpenAI API-key usage (metered per minute); no platform fee | $200-500/month subscription + per-minute overages |
| **Data privacy** | Your servers, your data | Third-party stores your call data |
| **Customization** | Full source code, modify anything | Limited to what their dashboard exposes |
| **Vendor lock-in** | None -- open source, standard SIP | Proprietary platform, migration is painful |
| **Multi-business** | Built in, single deployment | Usually requires separate accounts/plans |
| **Self-hosted** | Yes | No |
| **Source code access** | Full | None |

## Features
- Natural speech-to-speech conversations via OpenAI Realtime API
- Inbound phone call handling via SIP/Twilio/Telnyx
- FAQ answering from configurable knowledge base
- Call transfers to departments and specific people
- Message taking with file-based or webhook delivery
- Multi-business support from a single running agent
- Built-in noise cancellation optimized for phone audio (LiveKit BVC Telephony)
- YAML-based configuration — no code changes needed to customize
- After-hours detection with configurable messages

## Prerequisites
- Python 3.11+
- OpenAI API key (`sk-...`) with Realtime API access
- LiveKit server ([self-hosted](https://docs.livekit.io/home/self-hosting/local/) or [LiveKit Cloud](https://cloud.livekit.io))
- SIP trunk provider (Twilio or Telnyx) with a phone number

## Quick start
1. Clone and install:
```bash
git clone https://github.com/kirklandsig/AIReceptionist.git
cd AIReceptionist
pip install -e .
```
2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your LiveKit keys:
#   LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET, RECEPTIONIST_AGENT_NAME
# Add OPENAI_API_KEY (a standard sk-... key). ChatGPT/Codex OAuth no longer works for Realtime (2026-06-03 Beta sunset).
```
3. Configure your business:
```bash
cp config/businesses/example-dental.yaml config/businesses/my-business.yaml
# Edit with your business name, FAQs, routing numbers, hours
```
4. Set up telephony (full walkthrough in `documentation/telephony-setup.md`): buy or port a DID to a SIP trunk provider (Twilio Elastic SIP, Telnyx, Signalwire), point its Origination URI at LiveKit's SIP endpoint (`sip:<project-id>.sip.livekit.cloud;transport=tcp`), enable SIP REFER on the trunk for transfers, then create a LiveKit inbound trunk matching the DID plus a dispatch rule routing calls to the `receptionist` agent. RingCentral/RingEX reception groups are covered in `documentation/ringcentral-setup.md`.
5. Run:
```bash
python -m receptionist.agent dev
```
- `RECEPTIONIST_AGENT_NAME` defaults to `receptionist` for production LiveKit dispatch rules; for local Playground sessions use `RECEPTIONIST_AGENT_NAME="" python -m receptionist.agent dev`.
- "Call your phone number -- you should hear your AI receptionist answer with your custom greeting."

## Configuration
Each business is a YAML file in `config/businesses/` (see `example-dental.yaml`). Key sections:
- `business` — name, type, timezone
- `voice` — OpenAI voice selection (coral, alloy, ash, ballad, echo, sage, shimmer, verse)
- `greeting` — what the receptionist says when answering
- `personality` — system prompt personality instructions
- `hours` — business hours per day of week
- `after_hours_message` — what to say when the office is closed
- `routing` — departments/people the receptionist can transfer to
- `faqs` — question/answer pairs the receptionist draws from
- `messages` — how to store messages (file or webhook)

### OpenAI Realtime auth
Default `auth.type` is `api_key`, reading `OPENAI_API_KEY`:
```yaml
voice:
  voice_id: "marin"
  model: "gpt-realtime-2.1"
  auth:
    type: "api_key"   # reads OPENAI_API_KEY by default
```
> "⚠️ **The `oauth_codex` (ChatGPT/Codex OAuth) auth type no longer works for Realtime.** OpenAI's 2026-06-03 Realtime *Beta* sunset disabled OAuth for the GA Realtime API — deployments using it connect the call but the caller hears silence. Use `auth.type: api_key` with a real `sk-...` key."

## Message delivery channels
A business can route messages to multiple destinations simultaneously via `messages.channels`:
```yaml
messages:
  channels:
    - type: "file"
      file_path: "./messages/<business>/"
    - type: "email"
      to: ["owner@example.com"]
      include_transcript: true
      include_recording_link: true
    - type: "webhook"
      url: "https://hooks.slack.com/services/..."
      headers:
        X-Api-Key: ${SLACK_TOKEN}
```
- **file** — writes JSON to disk; most reliable, always awaited synchronously
- **email** — requires the top-level `email` section; supports SMTP or Resend
- **webhook** — POSTs `{"message": ..., "context": ...}` to the URL
- Email and webhook run in the background with 3-attempt exponential backoff; exhausted failures land in `<file_path>/.failures/` and are inspected with `python -m receptionist.messaging list-failures`.

## Call recording and transcripts
Enable in a business YAML:
```yaml
recording:
  enabled: true
  storage:
    type: "local"        # or "s3"
    local:
      path: "./recordings/<business>/"
  consent_preamble:
    enabled: true
    text: "This call may be recorded for quality purposes."

transcripts:
  enabled: true
  storage:
    type: "local"
    path: "./transcripts/<business>/"
  formats: ["json", "markdown"]
```
- Recording uses LiveKit Egress; S3 credentials come from `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`.
- The consent preamble is spoken **before** the greeting — required for two-party consent states (CA, FL, IL, MD, MA, MT, NV, NH, PA, WA).

**Covers:** chunk 01-ai-receptionist-open-source-self-hosted-no-compr (project overview through call recording and transcripts: badges, active-development notice, 2026-06-03 Realtime Beta sunset banner, overview, Why This Exists, SaaS comparison table, Features, Prerequisites, Quick Start, Configuration, Realtime auth, message delivery channels, recording/transcripts)
