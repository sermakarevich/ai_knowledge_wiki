> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** This repository is a third-party API Evangelist profile of Inworld AI's real-time voice-AI platform, cataloging its TTS, Voice, STT, and Realtime APIs behind one API surface and billing relationship.
## Key points
- The profile covers Inworld AI as a real-time voice AI infrastructure provider delivering TTS, STT, speech-to-speech Realtime API, and an OpenAI/Anthropic-compatible LLM Router (01-overview.md:73).
- The repository contains no software, build, release, or binary — only text and machine-readable API descriptions (01-overview.md:57-60).
- The repo position is Consuming with 3rd-Party access, tagged AI, Voice, Text To Speech, Speech To Text, Realtime, LLM Routing, Voice Cloning, Conversational AI, and Game AI (01-overview.md:79-93).
- The Inworld TTS API provides Realtime TTS-2 (100+ languages), TTS 1.5 Max (15 languages), and TTS 1.5 Mini (sub-120 ms first-token) with sync, server-streamed, and WebSocket synthesis (01-overview.md:104).
- The Inworld Voice API manages custom voices via instant cloning from audio samples and natural-language voice design, with list/get/update/delete plus a workspace publish endpoint (01-overview.md:135).
- The Inworld STT API offers synchronous transcribe and streaming WebSocket transcription with multi-provider routing (Whisper variants via Groq), 99+ languages, word timestamps, voice profiling, and prompt biasing (01-overview.md:161).
- The Inworld Realtime API is an end-to-end STT+LLM+TTS pipeline over WebSocket and WebRTC using an OpenAI-Realtime-API-compatible event protocol with VAD, tool calling, MCP tunneling, and Twilio integration (01-overview.md:187).
---
## Provenance and scope
> **This is not our API.** This repository is an independent, third-party profile of a company's **publicly available** API surface, maintained by API Evangelist (01-overview.md:12-13).
> **Where the information came from.** Everything here is assembled from material a member of the public can reach with a browser and no credentials (01-overview.md:17-18).
> **The rating is an independent assessment.** The Kin Score and Agent Readiness rating are independently calculated scores of a company's *public* API artifacts (01-overview.md:24-25).

| Field | Value |
|---|---|
| Position | Consuming (01-overview.md:79) |
| Access | 3rd-Party (01-overview.md:80) |
| Created | 2026-05-25T00:00:00.000Z (01-overview.md:97) |
| Modified | 2026-05-25 (01-overview.md:98) |
| APIs.json | `apis.yml` raw GitHub URL (01-overview.md:75) |

Tags: `AI`, `Artificial Intelligence`, `Voice`, `Text To Speech`, `Speech To Text`, `Realtime`, `LLM Routing`, `Voice Cloning`, `Conversational AI`, `Game AI` (01-overview.md:84-93).
## Inworld TTS API
> Inworld TTS — real-time text-to-speech API with the #1-ranked voice models on the Artificial Analysis Speech Arena (01-overview.md:104).

- Models: `Realtime TTS-2` (100+ languages, natural-language steering), `Realtime TTS 1.5 Max` (15 languages), `Realtime TTS 1.5 Mini` (cost-optimized, sub-120 ms first-token) (01-overview.md:104).
- Interfaces: synchronous synthesis, server-streamed synthesis, streaming WebSocket interface (01-overview.md:104).
- Features: instant + professional voice cloning, voice design from text prompts, custom pronunciation, pause controls, word/character/phoneme alignment for lipsync, zero-data-retention plus on-premise deployment (01-overview.md:104).
- Human URL: `https://docs.inworld.ai/tts/tts` (01-overview.md:106).
- Spec artifacts: `openapi/inworld-tts-api-openapi.yml`, `collections/inworld-tts-api.postman_collection.json`, `collections/inworld-tts-api.opencollection.json`, `asyncapi/inworld-ai-asyncapi.yml`, `json-schema/inworld-tts-synthesis-schema.json`, `json-ld/inworld-ai-context.jsonld` (01-overview.md:126-131).
## Inworld Voice API
> Clone voices from short audio samples (instant voice cloning) or design voices from natural-language descriptions plus optional reference audio (01-overview.md:135).

- Operations: lists, gets, updates, and deletes voices, plus a publish endpoint for sharing voices across a workspace (01-overview.md:135).
- Human URL: `https://docs.inworld.ai/api-reference/voiceAPI/voiceservice/list-voices` (01-overview.md:137).
- Spec artifacts: `openapi/inworld-voice-api-openapi.yml`, `collections/inworld-voice-api.postman_collection.json`, `collections/inworld-voice-api.opencollection.json` (01-overview.md:155-157).
## Inworld STT API
> Inworld STT — speech-to-text transcription API with synchronous transcribe and a streaming WebSocket endpoint (01-overview.md:161).

- Routing: multi-provider routing (currently Whisper variants via Groq) with 99+ language support (01-overview.md:161).
- Features: word timestamps, voice profiling, prompt biasing for domain-specific vocabulary, configurable end-of-turn detection (01-overview.md:161).
- Human URL: `https://docs.inworld.ai/stt/overview` (01-overview.md:163).
- Spec artifacts: `openapi/inworld-stt-api-openapi.yml`, `collections/inworld-stt-api.postman_collection.json`, `collections/inworld-stt-api.opencollection.json`, `asyncapi/inworld-ai-asyncapi.yml` (01-overview.md:180-183).
## Inworld Realtime API
> Inworld Realtime — end-to-end speech-to-speech voice pipeline (STT + LLM + TTS) exposed over WebSocket and WebRTC (01-overview.md:187).

- Protocol: OpenAI-Realtime-API-compatible event protocol (`session.update`, `input_audio_buffer.append`, `response.create`, etc.) so existing OpenAI Realtime clients can swap base URLs (01-overview.md:187).
- Features: server-side and semantic VAD, function/tool calling, MCP server tunneling, Twilio media-stream integration, JWT-based session authentication (01-overview.md:187).
- Human URL: `https://docs.inworld.ai/realtime/overview` (01-overview.md:189).
- Note: the chunk's Realtime Properties list is cut off mid-entry at `https://docs.inworld.ai/realtime` (01-overview.md:208); contents after that point were not provided, so Router/Models APIs listed in the plan cover line are not described here.

**Covers:** repo overview (README scope, tags, timestamps, TTS / Voice / STT / Realtime API entries) as given in `chunks/01-overview.md`
