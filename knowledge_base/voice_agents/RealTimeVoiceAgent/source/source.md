> PDF location: https://github.com/vishnu97770/Real-Time-Voice-Agent
# vishnu97770/Real-Time-Voice-Agent
Source: https://github.com/vishnu97770/Real-Time-Voice-Agent
Kind: repo
Fetched: 2026-09-22T14:39:26.606834+00:00
Tool: git-clone

# vishnu97770/Real-Time-Voice-Agent

Commit: 6874010ec351243ec0f853c522a5a2bfd89ee710

## README

# Real-Time Voice Agent — One Runtime, Any Vertical

![Status](https://img.shields.io/badge/status-prototype-blue) ![Type](https://img.shields.io/badge/type-academic%20project-lightgrey) ![Core](https://img.shields.io/badge/core-real--time%20voice%20AI-orange)

A production-grade, real-time conversational voice agent that can pick up the phone (or a mic) as a bank's customer-care line, a hospital's follow-up caller, a telecom support desk, or an admissions office — using the **same real-time engine** every time. Only a swappable **Agent Profile** changes between deployments.

It started as a credit-underwriting copilot. It's architected to be much more than that.

---

<<<<<<< HEAD
## Core Idea

Most voice-bot projects hard-code one persona into one pipeline. This project separates the two:

- **The runtime** — audio capture, voice-activity detection, streaming transcription, tool-grounded reasoning, streaming speech synthesis, barge-in handling, consent gating, and audit logging — is built once and never changes per deployment.
- **The profile** — who the agent is, what data it can see, what it's allowed to do, and what it must never do — is configuration, loaded per call.

Give a hospital the platform and it becomes a patient-follow-up caller. Give a bank the same platform and it becomes a fraud-alert or customer-care agent. Nothing about the underlying engine is rewritten.

## How It Works

**Real-time loop** (workspace voice or live on a call):

```
Client audio  →  VAD  →  Streaming ASR  →  LLM (tool-grounded)  →  Streaming TTS  →  Client audio
   (packets)                (live transcript)      (drafts reply)      (packets, streamed back)
```

- **VAD** continuously separates speech from silence and is what makes barge-in possible — if the caller talks over the agent, playback is cut instantly and the turn switches.
- **Streaming ASR** produces a transcript incrementally, so reasoning can start before the caller finishes speaking.
- **The LLM** never states a fact it hasn't fetched — every account, policy, or application detail is pulled through a scoped tool call, not invented.
- **Streaming TTS** starts speaking on the first sentence of a reply instead of waiting for the whole response.
- **Perceived end-to-end latency runs ~200–700 ms**, keeping the exchange close to natural conversation.
- Any action that *changes* something (freezing a card, filing a claim, rescheduling an appointment) pauses for the caller's explicit confirmation before it executes — never assumed, always logged.

**Outbound calling** extends the same loop with a simple contract: a business's own workflow sends the platform a **call job** (who to call, why, and which profile to use), the platform conducts the entire call, and sends back a **call result** (outcome, transcript reference, audit trail). The business decides who gets called and what happens with the result; the platform only owns the call itself.

## Reusable Across Verticals

| Vertical | Example reason for the call | Example guarded action |
|---|---|---|
| Hospital | Post-discharge follow-up, medication check | Schedule an appointment |
| Bank | Unusual activity alert, statement query | Freeze a card |
| Telecom | Plan renewal, usage alert | Upgrade a plan |
| Insurance | Renewal reminder, claim update | File a claim |
| Admissions | Application status, program details | Schedule a counselor call |

Every profile inherits the same non-negotiable behavior regardless of industry: it discloses that it's an AI at the start of the call, and it never asks for a password, PIN, one-time passcode, or full payment card number.

## What's In This Repo

| File | What it is |
|---|---|
| `Real-Time-Voice-Agent-PRD.pdf` | Original product requirements — scope, workflow, state machines, delivery plan |
| `Architecture-Appendix-Voice-Agent.docx` | Outbound-calling architecture: schematic, end-to-end workflow, `call job` / `call result` data contracts, compliance notes |
| `voice-agent-console.html` | Working browser prototype — real mic input, live speech recognition, tool-calling against a live LLM, streaming speech output, and five interchangeable profiles (Credit Underwriting, Bank, Insurance, Telecom, Admissions), each with mock grounded data and a consent-gated action |

## Tech Stack

- **Target production stack:** Python, AsyncIO, Pipecat / LiveKit Agents, streaming ASR & TTS, Gemini / Google ADK, VAD, Docker
- **This prototype:** browser-native Web Speech API (ASR + TTS) driving a live LLM with tool use, running entirely client-side as a single self-contained page

## Status

This repository currently contains the **design and a functional prototype** of the real-time conversational loop and profile framework — not a deployed production system. Outbound telephony (Twilio/LiveKit + SIP), OCR-based document extraction, the ML risk model, and persistent storage are specified in the PRD's delivery plan but not yet implemented; the architecture appendix defines the exact interfaces they'll plug into.

## Conclusion

The point of this project isn't "a voice bot for credit underwriting" — it's a reusable real-time voice runtime where the underwriting agent, the bank agent, and the hospital caller are all the same system wearing a different, tightly-scoped profile. VAD, streaming ASR, grounded reasoning, and streaming TTS handle the *how* of the conversation identically every time; the profile handles the *who* and the *why*. That split is what lets one platform, built once, serve as the calling infrastructure for a bank, a hospital, a telecom provider, or a university admissions desk — without ever touching the real-time core again.

---

*Academic project — Kirit Ranjan, V. Vishnu (PST-25-0051, PST-25-0106), 2025, 3rd Semester.*
=======
_____________________________________________________________________________________________________________________________________________________|___
Technology	        |            Type            |             What we use it for?              |   	      How it helps our project               |
____________________|____________________________|______________________________________________|____________________________________________________|__        
Python	            |   Programming Language	 |  Backend, agent logic, APIs, processing	    |  Acts as the core development language             |
Pipecat	            |   Voice AI Framework	     |  Builds the real-time voice pipeline	        |  Connects and orchestrates ASR → LLM → TTS         |
LiveKit Agents	    |   Voice/Realtime Framework |  Real-time communication and agent execution |  Enables low-latency, real-time voice interaction  |
Deepgram / Whisper	|   ASR	                     |  Speech → Text	                            |  Allows the agent to understand what the user says | 
ElevenLabs / PlayHT |   TTS	                     |  Text → Speech	                            |  Allows the agent to respond naturally using voice |
LLM	                |   AI Model	             |  Reasoning and response generation	        |  Acts as the brain of the voice agent              |
_____________________________________________________________________________________________________________________________________________________|_


## Running it

**Frontend** (`frontend/`): `npm install && npm run dev`. Works on its own with a built-in
rule-based brain (Chrome or Edge for voice; typing works anywhere).

**Backend** (`backend/`): a FastAPI service that runs the call with Gemini tool-calling and
streams the reply so speech starts on the first sentence. It also provides operator sign-in, rate
limits, outbound call jobs with signed result callbacks, saved call history, and per-customer data.
Set `GEMINI_API_KEY` in `backend/.env`, create a user with `python -m app.cli create-user`, and
the browser uses it automatically when it is reachable. See [`backend/README.md`](backend/README.md).

>>>>>>> 1ec24ea (Add voice console: profiles, voice loop, sign-in, call history, callee screen)


## Top-level layout

- backend/ (dir, 46 files, ~8597 lines)
- frontend/ (dir, 59 files, ~12695 lines)
- README.md (~99 lines)
- requirements.txt (~1 lines)

