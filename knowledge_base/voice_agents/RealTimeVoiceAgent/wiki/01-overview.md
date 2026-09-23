> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** Real-Time-Voice-Agent is one reusable real-time voice runtime (VAD → streaming ASR → tool-grounded LLM → streaming TTS) worn by swappable per-vertical Agent Profiles so the same engine serves banks, hospitals, telecom, insurance, and admissions without rewriting the core (01-overview.md:11, 01-overview.md:20-25, 01-overview.md:76).
## Key points
- The project separates a fixed runtime (audio capture, VAD, streaming transcription, tool-grounded reasoning, streaming TTS, barge-in, consent gating, audit logging) from per-call configuration profiles (who the agent is, what data it sees, allowed/forbidden actions) (01-overview.md:22-23).
- The real-time loop streams `Client audio → VAD → Streaming ASR → LLM (tool-grounded) → Streaming TTS → Client audio`, with perceived end-to-end latency ~200–700 ms (01-overview.md:31-34, 01-overview.md:40).
- The LLM never states unfetched facts — every account, policy, or application detail is pulled through a scoped tool call — and any state-changing action pauses for explicit caller confirmation and is logged (01-overview.md:38, 01-overview.md:41).
- Outbound calling reuses the same loop under a call-job / call-result contract: the business sends who to call, why, and which profile; the platform conducts the call and returns outcome, transcript reference, and audit trail (01-overview.md:43).
- Every profile inherits non-negotiables: disclose AI identity at call start and never ask for password, PIN, OTP, or full card number (01-overview.md:55).
- The repo currently holds design plus a functional prototype, not a deployed system; outbound telephony (Twilio/LiveKit + SIP), OCR extraction, ML risk model, and persistent storage are specified but not implemented (01-overview.md:72).
- The chunk contains an unresolved merge conflict: HEAD side describes the runtime/profile split and browser prototype, incoming side (`1ec24ea`) describes a Python/frontend-backend stack with `frontend/` and `backend/` run instructions (01-overview.md:17, 01-overview.md:81, 01-overview.md:94-105).
---
## Core idea: runtime vs profile
Separation stated verbatim (01-overview.md:20-25):
- **The runtime** — audio capture, voice-activity detection, streaming transcription, tool-grounded reasoning, streaming speech synthesis, barge-in handling, consent gating, and audit logging — is built once and never changes per deployment.
- **The profile** — who the agent is, what data it can see, what it's allowed to do, and what it must never do — is configuration, loaded per call.
- Started as a credit-underwriting copilot; giving a hospital the platform makes it a patient-follow-up caller, giving a bank the same platform makes it a fraud-alert or customer-care agent (01-overview.md:13, 01-overview.md:25).

## How it works: real-time loop
Verbatim loop (01-overview.md:31-34):
```
Client audio  →  VAD  →  Streaming ASR  →  LLM (tool-grounded)  →  Streaming TTS  →  Client audio
   (packets)                (live transcript)      (drafts reply)      (packets, streamed back)
```
Behavior notes (01-overview.md:36-41):
- **VAD** separates speech from silence and enables barge-in — caller speech over agent playback cuts playback instantly and switches the turn.
- **Streaming ASR** emits incremental transcripts so reasoning starts before the caller finishes.
- **Streaming TTS** speaks on the first reply sentence instead of waiting for the full response.
- Perceived latency ~200–700 ms.
- State-changing actions (freezing a card, filing a claim, rescheduling an appointment) require explicit confirmation, never assumed, always logged.

## Outbound calling contract
Business workflow sends a **call job** (who to call, why, which profile); platform conducts the call and returns a **call result** (outcome, transcript reference, audit trail); the business owns who gets called and result handling, the platform owns only the call (01-overview.md:43).

## Reusable across verticals
Verbatim table (01-overview.md:47-53):

| Vertical | Example reason for the call | Example guarded action |
|---|---|---|
| Hospital | Post-discharge follow-up, medication check | Schedule an appointment |
| Bank | Unusual activity alert, statement query | Freeze a card |
| Telecom | Plan renewal, usage alert | Upgrade a plan |
| Insurance | Renewal reminder, claim update | File a claim |
| Admissions | Application status, program details | Schedule a counselor call |

Guardrails apply to all verticals regardless of industry (01-overview.md:55).

## What's in this repo
Verbatim table (01-overview.md:59-63):

| File | What it is |
|---|---|
| `Real-Time-Voice-Agent-PRD.pdf` | Original product requirements — scope, workflow, state machines, delivery plan |
| `Architecture-Appendix-Voice-Agent.docx` | Outbound-calling architecture: schematic, end-to-end workflow, `call job` / `call result` data contracts, compliance notes |
| `voice-agent-console.html` | Working browser prototype — real mic input, live speech recognition, tool-calling against a live LLM, streaming speech output, and five interchangeable profiles (Credit Underwriting, Bank, Insurance, Telecom, Admissions), each with mock grounded data and a consent-gated action |

## Tech stack
HEAD side (01-overview.md:67-68):
- **Target production stack:** Python, AsyncIO, Pipecat / LiveKit Agents, streaming ASR & TTS, Gemini / Google ADK, VAD, Docker
- **This prototype:** browser-native Web Speech API (ASR + TTS) driving a live LLM with tool use, entirely client-side as a single self-contained page

Incoming (`1ec24ea`) side technology table (01-overview.md:83-91):

| Technology | Type | What we use it for? | How it helps our project |
|---|---|---|---|
| Python | Programming Language | Backend, agent logic, APIs, processing | Acts as the core development language |
| Pipecat | Voice AI Framework | Builds the real-time voice pipeline | Connects and orchestrates ASR → LLM → TTS |
| LiveKit Agents | Voice/Realtime Framework | Real-time communication and agent execution | Enables low-latency, real-time voice interaction |
| Deepgram / Whisper | ASR | Speech → Text | Allows the agent to understand what the user says |
| ElevenLabs / PlayHT | TTS | Text → Speech | Allows the agent to respond naturally using voice |
| LLM | AI Model | Reasoning and response generation | Acts as the brain of the voice agent |

## Running it (incoming side only)
Verbatim instructions (01-overview.md:96-103):
- **Frontend** (`frontend/`): `npm install && npm run dev`. Works on its own with a built-in rule-based brain (Chrome or Edge for voice; typing works anywhere).
- **Backend** (`backend/`): FastAPI service running the call with Gemini tool-calling, streaming the reply so speech starts on the first sentence; provides operator sign-in, rate limits, outbound call jobs with signed result callbacks, saved call history, per-customer data. Set `GEMINI_API_KEY` in `backend/.env`, create a user with `python -m app.cli create-user`; browser uses it automatically when reachable. See `backend/README.md`.

Exact parameter/command names: `npm install`, `npm run dev`, `GEMINI_API_KEY`, `backend/.env`, `python -m app.cli create-user`, `backend/README.md` (01-overview.md:96-103).

## Status and conclusion
Status (01-overview.md:72): design plus functional prototype of the loop and profile framework — not deployed; Twilio/LiveKit + SIP telephony, OCR document extraction, ML risk model, persistent storage specified in PRD delivery plan but unimplemented; architecture appendix defines their plug-in interfaces. Academic project — Kirit Ranjan, V. Vishnu (PST-25-0051, PST-25-0106), 2025, 3rd Semester (01-overview.md:80). Conclusion restates the split: VAD, streaming ASR, grounded reasoning, streaming TTS handle the *how* identically; the profile handles the *who* and *why* (01-overview.md:76). No truncated files were noted in the chunk.

**Covers:** README (project pitch, Core Idea, How It Works loop, verticals table, repo-contents table, tech stack, status, conclusion); incoming-side technology table and `frontend/` + `backend/` run notes; macro-component pointer `top-level-files/` (01-overview.md:107-109)
