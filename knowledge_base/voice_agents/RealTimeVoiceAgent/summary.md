# Technical Analysis: vishnu97770/Real-Time-Voice-Agent

**Repository:** https://github.com/vishnu97770/Real-Time-Voice-Agent
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview

Problem space: organizations in regulated verticals (banking, healthcare, telecom, insurance, admissions) need real-time voice agents that answer caller questions from live data and execute guarded actions (freeze a card, schedule an appointment, file a claim) without hallucinating facts or bypassing consent and audit requirements (01-overview.md:38, 01-overview.md:41, 01-overview.md:47-53).

How the repo addresses it: it defines one fixed real-time voice runtime — audio capture, VAD, streaming ASR, tool-grounded LLM reasoning, streaming TTS, barge-in, consent gating, audit logging — and loads per-call Agent Profiles that specify identity, visible data, allowed actions, and prohibitions, so the same engine serves multiple verticals without core rewrites (01-overview.md:20-25, 01-overview.md:76). A single-page browser prototype (`voice-agent-console.html`) demonstrates the loop with live microphone input, live speech recognition, tool-calling against a live LLM, streaming speech output, and five interchangeable profiles; design documents specify the production backend and outbound-calling contracts (01-overview.md:55, 01-overview.md:59-63).

Primary user: a vertical-team developer or operator configuring and running a grounded voice agent for customer-care, follow-up, renewal, or status-call workloads.

## 2. High-Level Architecture

```
Browser / Telephony client
  │ audio packets (mic / SIP)
  ▼
VAD ──► Streaming ASR ──► LLM (tool-grounded) ──► Streaming TTS
  │         │                      │                      │
  │         │ ► scoped tool calls ─┘                      │
  │         │   (account / policy / application data)     │
  │         └─► barge-in: caller speech cuts playback ────┘
  ▼
Consent gate ──► Guarded action ──► Audit log + Call result
```

Data-flow narrative:

1. Client streams audio packets; VAD separates speech from silence and triggers barge-in, cutting agent playback when the caller speaks over it (01-overview.md:36-41).
2. Streaming ASR emits incremental transcripts so reasoning starts before the caller finishes the utterance (01-overview.md:36-41).
3. The LLM drafts replies only through scoped tool calls for account, policy, or application facts; it never states unfetched facts (01-overview.md:38).
4. Streaming TTS speaks the first reply sentence without waiting for the full response, yielding perceived end-to-end latency of ~200–700 ms (01-overview.md:36-41, 01-overview.md:31-34).
5. State-changing actions pause for explicit caller confirmation, then execute and are logged; outbound calls follow a call-job / call-result contract where the business supplies who, why, and which profile, and the platform returns outcome, transcript reference, and audit trail (01-overview.md:38, 01-overview.md:41, 01-overview.md:43).

Persistent state lives: no persistent store is implemented in the analyzed prototype. The design specifies per-customer data, saved call history, call jobs/results, and audit trails as backend responsibilities (outbound contract, operator sign-in, rate limits), with persistent storage listed as specified-but-unimplemented alongside Twilio/LiveKit + SIP telephony, OCR extraction, and the ML risk model (01-overview.md:43, 01-overview.md:72, 01-overview.md:96-103).

## 3. The Runtime–Profile Split

Representation: the split is configuration, not code forking. The runtime is built once (capture, VAD, streaming transcription, tool-grounded reasoning, streaming synthesis, barge-in, consent gating, audit logging); the profile (agent identity, visible data, allowed/forbidden actions) is loaded per call (01-overview.md:20-25). In the prototype each profile carries mock grounded data and one consent-gated action (01-overview.md:55).

Named kinds/types with locations:

- Runtime stages: VAD, Streaming ASR, LLM (tool-grounded), Streaming TTS, consent gate, audit log (01-overview.md:20-25, 01-overview.md:31-34).
- Agent Profiles (5): Credit Underwriting, Bank, Insurance, Telecom, Admissions (01-overview.md:55).
- Vertical task/action pairs: Hospital / schedule an appointment; Bank / freeze a card; Telecom / upgrade a plan; Insurance / file a claim; Admissions / schedule a counselor call (01-overview.md:47-53).
- Outbound contracts: `call job` (who to call, why, which profile) and `call result` (outcome, transcript reference, audit trail) (01-overview.md:43).
- Non-negotiable guardrails: disclose AI identity at call start; never request password, PIN, OTP, or full card number (01-overview.md:55).

Key queries, verbatim (01-overview.md:20-25):

```
The runtime — audio capture, voice-activity detection, streaming transcription,
tool-grounded reasoning, streaming speech synthesis, barge-in handling, consent
gating, and audit logging — is built once and never changes per deployment.
The profile — who the agent is, what data it can see, what it's allowed to do,
and what it must never do — is configuration, loaded per call.
```

## 4. LLM / External Service Integration

Providers: Gemini via Google ADK / `google-genai` for backend reasoning with tool-calling; a live LLM with tool use from the browser prototype; streaming ASR candidates Deepgram / Whisper and Web Speech API (prototype); TTS candidates ElevenLabs / PlayHT and Web Speech API (prototype); real-time transport via Pipecat / LiveKit Agents (`livekit-agents[google]`, `livekit-plugins-ai-coustics`); outbound telephony via Twilio + SIP (specified, not implemented) (01-overview.md:59-72, 01-overview.md:83-91, 02-top-level-files.md:8).

Required vs optional calls: required — LLM tool-grounded reasoning call per turn (prototype calls a live LLM; backend streams Gemini tool-calling replies starting on the first sentence) (01-overview.md:55, 01-overview.md:96-103). Required in production design — streaming ASR and streaming TTS on every turn (01-overview.md:31-34). Optional / specified-but-unimplemented — Twilio/LiveKit + SIP telephony, OCR document extraction, ML risk model (01-overview.md:72).

Env vars and config:

| Variable / file | Required | Purpose |
|---|---|---|
| `GEMINI_API_KEY` in `backend/.env` | Yes (backend path) | Authenticates Gemini tool-calling backend (01-overview.md:96-103) |
| `backend/.env` | Yes (backend path) | Holds backend secrets/config (01-overview.md:96-103) |
| Browser prototype | No backend key described | Runs client-side Web Speech API + live LLM with tool use as a self-contained page (01-overview.md:59-60) |

## 5. The Real-Time Voice Loop

Primary workflow: one inbound or outbound call turn through VAD → streaming ASR → tool-grounded LLM → streaming TTS with barge-in and consent gating. The wiki exposes stage-level behavior, not function symbols; locations below are the finest granularity attested.

1. Capture audio packets — browser microphone in the prototype; SIP/telephone packets in the production design (`voice-agent-console.html` prototype; 01-overview.md:31-34, 01-overview.md:55).
2. Voice-activity detection and barge-in — VAD classifies speech vs silence; overlapping caller speech cuts playback and switches the turn (01-overview.md:36-41).
3. Incremental transcription — streaming ASR emits live transcript fragments so downstream reasoning starts early (01-overview.md:31-34, 01-overview.md:36-41).
4. Tool-grounded reasoning — LLM resolves facts exclusively via scoped tool calls against profile-visible mock data (prototype) or per-customer backend data (backend path); drafts reply incrementally (01-overview.md:38, 01-overview.md:55, 01-overview.md:96-103).
5. Incremental synthesis and playback — streaming TTS speaks the first sentence as packets streamed back to the client rather than waiting for completion (01-overview.md:31-34, 01-overview.md:36-41).
6. Consent-gated action and logging — state-changing actions (freeze card, file claim, reschedule, upgrade plan, schedule call) require explicit confirmation and are always logged; outbound turns close with a call result (outcome, transcript reference, audit trail) (01-overview.md:38, 01-overview.md:41, 01-overview.md:43, 01-overview.md:47-53).

## 6. Key Files

Wiki chunk coverage is limited to the manifest plus design/prototype pointers; the table lists every file attested in the component pages.

| File | Lines | What It Does |
|---|---|---|
| `voice-agent-console.html` | Single self-contained page (line count not in wiki) | Browser prototype: mic input, live speech recognition, tool-calling against live LLM, streaming speech output, 5 profiles with mock data and consent-gated action (01-overview.md:55) |
| `Real-Time-Voice-Agent-PRD.pdf` | Spec document | Product requirements: scope, workflow, state machines, delivery plan (01-overview.md:59-63) |
| `Architecture-Appendix-Voice-Agent.docx` | Spec document | Outbound architecture: schematic, end-to-end workflow, call-job / call-result contracts, compliance notes (01-overview.md:59-63) |
| `requirements.txt` | 1 line manifest | Pins entire backend runtime in one install line (02-top-level-files.md:5-16) |
| `frontend/` | Directory (incoming side) | Standalone UI with built-in rule-based brain; voice needs Chrome/Edge, typing works anywhere (01-overview.md:96-103) |
| `backend/` | Directory (incoming side) | FastAPI service: Gemini tool-calling, streamed replies, operator sign-in, rate limits, call jobs with signed callbacks, history, per-customer data (01-overview.md:96-103) |
| `backend/.env` | Config file | Holds `GEMINI_API_KEY` and backend secrets (01-overview.md:96-103) |
| `backend/README.md` | Doc | Backend setup and run reference (01-overview.md:96-103) |
| `backend/app/cli` (`python -m app.cli create-user`) | CLI module (lines not in wiki) | Creates operator user for backend sign-in (01-overview.md:96-103) |
| `README` (root, HEAD side) | Pitch + Core Idea + How It Works + verticals + stack + status | Defines runtime/profile split, loop, verticals table, tech stack, prototype status (01-overview.md:107-109) |

## 7. Dependencies

All entries come from the single-line manifest (02-top-level-files.md:13-23). Only one entry carries a version constraint; the remainder are unpinned bare names in the analyzed chunk.

| Package | Version constraint | Purpose |
|---|---|---|
| `fastapi` | (none) | Web/API service framework |
| `uvicorn[standard]` | (none) | ASGI server |
| `pydantic` | (none) | Data validation |
| `pydantic-settings` | (none) | Settings / env config |
| `python-multipart` | (none) | Form/multipart parsing |
| `python-dotenv` | (none) | `.env` loading |
| `httpx` | (none) | HTTP client |
| `sqlalchemy` | (none) | ORM / database access |
| `psycopg[binary]` | (none) | Postgres driver |
| `alembic` | (none) | DB migrations |
| `livekit-agents[google]` | `~=1.5` | Real-time voice pipeline, Google integration |
| `livekit-plugins-ai-coustics` | (none) | Audio processing plugin |
| `google-adk` | (none) | Gemini agent framework |
| `google-genai` | (none) | Gemini API client |
| `twilio` | (none) | Outbound telephony (specified) |
| `apscheduler` | (none) | Scheduling (call jobs) |
| `pymupdf` | (none) | PDF text extraction |
| `pypdf` | (none) | PDF handling |
| `pandas` | (none) | Tabular data |
| `openpyxl` | (none) | Excel I/O |
| `pytesseract` | (none) | OCR extraction |
| `Pillow` | (none) | Image handling for OCR |
| `numpy` | (none) | Numerics |
| `scikit-learn` | (none) | ML risk model (specified) |
| `joblib` | (none) | Model persistence |
| `structlog` | (none) | Structured logging |
| `opentelemetry-api` | (none) | Observability API |
| `opentelemetry-sdk` | (none) | Observability SDK |
| `pytest` | (none) | Testing |
| `pytest-asyncio` | (none) | Async tests |

Grouping per component page: Web/API/config, HTTP/DB/migrations, Voice/AI/scheduling, Documents/tables/OCR, Numeric/ML/observability/tests (02-top-level-files.md:17-23).

## 8. CLI / Usage Surface

Entry points: `voice-agent-console.html` opened in a browser (prototype path); `frontend/` dev server and `backend/` FastAPI service (incoming-side path) (01-overview.md:55, 01-overview.md:96-103).

Commands:

| Command | Where | Effect |
|---|---|---|
| Open `voice-agent-console.html` in browser, grant mic | Prototype | Starts mic → recognition → tool-calling LLM → speech output demo with profile switcher (01-overview.md:55) |
| `npm install && npm run dev` in `frontend/` | `frontend/` | Runs standalone UI with rule-based brain; voice requires Chrome or Edge (01-overview.md:96-103) |
| Set `GEMINI_API_KEY` in `backend/.env` | `backend/` | Enables Gemini tool-calling backend (01-overview.md:96-103) |
| `python -m app.cli create-user` | `backend/` | Creates operator sign-in user; browser uses backend automatically when reachable (01-overview.md:96-103) |
| `pip install <requirements.txt line>` | Repo root | Installs full backend stack (02-top-level-files.md:13-16) |

Env-var and config tables:

| Env var | Required for | Source |
|---|---|---|
| `GEMINI_API_KEY` | Backend Gemini calls | `backend/.env` (01-overview.md:96-103) |

| Config | Format | Content |
|---|---|---|
| Agent Profile | Per-call configuration (prototype: in-page; backend: per-customer data) | Identity, visible data, allowed/forbidden actions (01-overview.md:20-25) |
| Call job | Business → platform handoff | Who to call, why, which profile (01-overview.md:43) |
| Call result | Platform → business return | Outcome, transcript reference, audit trail (01-overview.md:43) |

## 9. Extensibility Points

- New vertical / Agent Profile: add a profile definition (identity, data scope, allowed/forbidden actions, consent-gated action, mock grounded data) alongside the five existing profiles in `voice-agent-console.html` (prototype) or the backend per-customer/profile store (01-overview.md:20-25, 01-overview.md:47-55).
- New grounded fact source: add a scoped tool the LLM must call before stating facts, following the tool-grounded pattern; wire it into the ASR → LLM → TTS turn (01-overview.md:38).
- New guarded action: add the action plus its explicit-confirmation prompt and audit-log write, reusing the consent gate that guards freeze-card / file-claim / schedule-class actions (01-overview.md:38, 01-overview.md:41, 01-overview.md:47-53).
- ASR/TTS swap: replace the Web Speech API path with Deepgram/Whisper (ASR) or ElevenLabs/PlayHT (TTS) behind the Pipecat / LiveKit Agents pipeline stages (`livekit-agents[google]`, `livekit-plugins-ai-coustics`) (01-overview.md:59-72, 02-top-level-files.md:8).
- Outbound/telephony integration: implement the specified Twilio/LiveKit + SIP plug-in behind the call-job / call-result contract defined in `Architecture-Appendix-Voice-Agent.docx` (01-overview.md:59-63, 01-overview.md:72).
- Document/ML plug-ins: implement OCR extraction (`pymupdf`, `pypdf`, `pytesseract`, `Pillow`) and the `scikit-learn`/`joblib` risk model behind the PRD delivery-plan interfaces (01-overview.md:72, 02-top-level-files.md:9-10).

## 10. Limitations and Gotchas

- **Unresolved merge conflict in the analyzed chunk:** HEAD describes the runtime/profile split with a browser prototype; incoming side (`1ec24ea`) describes a `frontend/` + `backend/` Python stack with different run instructions — the two halves disagree on what the code is (01-overview.md:17, 01-overview.md:81, 01-overview.md:94-105).
- **Prototype, not a deployed system:** Twilio/LiveKit + SIP telephony, OCR extraction, ML risk model, and persistent storage are specified in the PRD/appendix but unimplemented; only the loop and profile framework are demonstrated (01-overview.md:72).
- **Prototype depends on browser Web Speech API:** ASR/TTS quality, language coverage, latency, and autoplay/mic-permission behavior inherit browser limitations; production streaming behavior (Deepgram/Whisper, ElevenLabs/PlayHT) is design-only in the wiki coverage (01-overview.md:59-60, 01-overview.md:83-91).
- **Single-line unpinned manifest:** all backend dependencies except `livekit-agents[google]~=1.5` are bare names with no version pins, so reproducible installs are not guaranteed from the analyzed line (02-top-level-files.md:13-16).
- **Guardrail burden stays on profile authors:** the LLM-never-states-unfetched-facts rule, AI-identity disclosure, credential-request ban, and per-action confirmation only hold if every new profile and tool is scoped correctly; one over-permissioned profile breaks the guarantee (01-overview.md:38, 01-overview.md:41, 01-overview.md:55).

## 11. How It Compares to Alternatives

- Pipecat (Daily): open-source real-time voice pipeline framework orchestrating ASR → LLM → TTS with transport/VAD building blocks; this repo targets Pipecat as its production pipeline layer rather than reimplementing transport (01-overview.md:59-72).
- LiveKit Agents: real-time session/agent runtime for low-latency voice with pluggable STT/LLM/TTS; this repo pins `livekit-agents[google]` for the same role and adds a profile/consent/audit framing on top (01-overview.md:59-72, 02-top-level-files.md:8).
- Vapi / Retell AI: hosted voice-agent platforms with telephony, tool use, and compliance features out of the box; this repo is a self-hosted design-plus-prototype with telephony still specified-not-implemented, trading managed convenience for profile-level control and audit ownership (01-overview.md:72).
- Generic Gemini + FastAPI voice starter: a minimal single-vertical demo with direct LLM calls; this repo differs by enforcing tool-grounded facts, per-vertical profiles, consent gates, and a call-job / call-result outbound contract as first-class concepts (01-overview.md:38, 01-overview.md:43, 01-overview.md:47-53).

Positioning: a profile-driven, audit-conscious voice-agent scaffold for regulated verticals that reuses commodity streaming voice infrastructure instead of competing with it.

## Appendix: Selected Code Snippets

1. Real-time loop, verbatim (01-overview.md:31-34):

```
Client audio  →  VAD  →  Streaming ASR  →  LLM (tool-grounded)  →  Streaming TTS  →  Client audio
   (packets)                (live transcript)      (drafts reply)      (packets, streamed back)
```

2. Backend manifest, verbatim single line (requirements.txt:1; via 02-top-level-files.md:13-16):

```
pip install fastapi "uvicorn[standard]" pydantic pydantic-settings python-multipart python-dotenv httpx sqlalchemy "psycopg[binary]" alembic "livekit-agents[google]~=1.5" livekit-plugins-ai-coustics google-adk google-genai twilio apscheduler pymupdf pypdf pandas openpyxl pytesseract Pillow numpy scikit-learn joblib structlog opentelemetry-api opentelemetry-sdk pytest pytest-asyncio
```

3. Incoming-side run instructions, verbatim (01-overview.md:96-103):

```
Frontend (frontend/): npm install && npm run dev. Works on its own with a built-in
rule-based brain (Chrome or Edge for voice; typing works anywhere).
Backend (backend/): FastAPI service running the call with Gemini tool-calling, streaming
the reply so speech starts on the first sentence; provides operator sign-in, rate limits,
outbound call jobs with signed result callbacks, saved call history, per-customer data.
Set GEMINI_API_KEY in backend/.env, create a user with python -m app.cli create-user;
browser uses it automatically when reachable. See backend/README.md.
```

4. Vertical reuse table, verbatim (01-overview.md:47-53):

```
| Vertical | Example reason for the call | Example guarded action |
| Hospital | Post-discharge follow-up, medication check | Schedule an appointment |
| Bank | Unusual activity alert, statement query | Freeze a card |
| Telecom | Plan renewal, usage alert | Upgrade a plan |
| Insurance | Renewal reminder, claim update | File a claim |
| Admissions | Application status, program details | Schedule a counselor call |
```
