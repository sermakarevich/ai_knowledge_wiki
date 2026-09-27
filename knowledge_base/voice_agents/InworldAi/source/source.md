# api-evangelist/inworld-ai
> PDF location: https://github.com/api-evangelist/inworld-ai (no source.pdf in run work dir; pinned per plan)
Source: https://github.com/api-evangelist/inworld-ai
Kind: repo
Fetched: 2026-09-22T14:12:35.008506+00:00
Tool: git-clone

# api-evangelist/inworld-ai

Commit: 10479fa331005124262e3a61a37399af8c669b55

## README

# Inworld AI (inworld-ai)

<!-- API-EVANGELIST-PROVENANCE:BEGIN -->
> ### About this repository
>
> **This is not our API.** This repository is an independent, third-party profile of a company's
> **publicly available** API surface, maintained by [API Evangelist](https://apievangelist.com).
> API Evangelist does not operate, host, resell, or support this company's APIs, and is not
> affiliated with or endorsed by the company unless stated on the profile.
>
> **Where the information came from.** Everything here is assembled from material a member of the
> public can reach with a browser and no credentials — the company's own website, developer portal
> and documentation, the specifications it publishes for public use (OpenAPI, AsyncAPI, JSON Schema,
> `apis.json`, `llms.txt` and similar), its public repositories, and its public status, pricing and
> changelog pages. **Nothing here is obtained by breaching a system, defeating an access control, or
> using credentials of any kind.**
>
> **The rating is an independent assessment.** The Kin Score and Agent Readiness rating are
> independently calculated scores of a company's *public* API artifacts, produced by API Evangelist
> against a published rubric. They are not certifications, endorsements, security assessments, or
> audits, and they score published artifacts — not the quality, safety, or security of the software.
>
> **Corrections, re-scores, and removal are free.** No partnership, contract, or purchase is
> required, and you do not need to justify the request.
>
> - **Something wrong?** Open an issue on this repository, or email
>   [info@apievangelist.com](mailto:info@apievangelist.com).
> - **Published something new?** Ask for a re-score and we will re-run the rating.
> - **Want the listing taken down?** Say so and we will honor it. The profile is reduced to your
>   company name, a factual description, and a link to your own site, and the company is recorded as
>   **unrated** — never scored zero for having asked.
>
> **Response times.** Acknowledgement within **one business day**; removal or restriction within
> **two business days**; corrections and re-scores within **five business days**.
>
> **Not from the company, and here with a question?** You are welcome here — we would rather be the
> front line and point you the right way than have a good report go nowhere. What this repository
> can answer is narrow, though, so it is worth knowing who you are actually looking for:
>
> - **A question about how the API works, an account, billing, or a bug in the service** — that is
>   the company's own support, not us. We profile this API; we do not operate it and cannot see
>   your account.
> - **A bug in an open-source project we only catalog** — file it on that project's own repository.
>   This has happened with a real and correct bug report that reached us instead of the people who
>   could fix it, which helped nobody.
> - **Anything about this listing itself** — the description, the tags, the rating, a missing or
>   wrong artifact — is ours. Open an issue here.
> - **Not sure, or something general about API Evangelist or APIs.io** — open an issue on the
>   [APIs.io Inbox](https://github.com/api-search/inbox) and we will route it.
>
> **This repository contains no software, and we will never ask you to download anything.** There is
> no build, release, installer, or binary here — only text and machine-readable API descriptions, so
> there is nothing here that can be "corrupt" or need "repairing". Any issue, comment, or email
> claiming otherwise and offering a download link is not from us and is hostile. Do not follow the
> link; it is a lure. Report it to GitHub and, if you like, tell us at
> [info@apievangelist.com](mailto:info@apievangelist.com) so we can take it down.
>
> **On a security or compliance team?** Email
> [info@apievangelist.com](mailto:info@apievangelist.com) with *security* in the subject line and
> you will get a person, not a form. We will tell you exactly which public URLs this profile was
> built from so your team can see the same surface we did, and we will take the listing down on
> request while you work through it.
>
> Full detail: **[Where this data comes from](https://apievangelist.com/about/where-our-data-comes-from)**
<!-- API-EVANGELIST-PROVENANCE:END -->

Inworld AI is a real-time voice AI infrastructure provider. The Inworld platform delivers text-to-speech, speech-to-text, an end-to-end speech-to-speech Realtime API, and an OpenAI- and Anthropic-compatible LLM Router behind one API surface and one billing relationship. Inworld's voice models lead the Artificial Analysis Speech Arena and are used to power voice agents, language-learning apps, AI companions, avatar experiences, game NPCs, and Twilio-backed phone agents. The platform supports instant and professional voice cloning, voice design from natural language, lipsync-grade phoneme alignment, on-premise TTS deployment, and zero-data-retention configurations for regulated workloads.

**APIs.json:** [https://raw.githubusercontent.com/api-evangelist/inworld-ai/refs/heads/main/apis.yml](https://raw.githubusercontent.com/api-evangelist/inworld-ai/refs/heads/main/apis.yml)

## Scope

- **Position:** Consuming
- **Access:** 3rd-Party

## Tags

- AI
- Artificial Intelligence
- Voice
- Text To Speech
- Speech To Text
- Realtime
- LLM Routing
- Voice Cloning
- Conversational AI
- Game AI

## Timestamps

- **Created:** 2026-05-25T00:00:00.000Z
- **Modified:** 2026-05-25

## APIs

### Inworld TTS API

Inworld TTS — real-time text-to-speech API with the #1-ranked voice models on the Artificial Analysis Speech Arena. Supports the Realtime TTS-2 model (100+ languages, natural-language steering), Realtime TTS 1.5 Max (15 languages), and Realtime TTS 1.5 Mini (cost-optimized, sub-120 ms first-token). Provides synchronous synthesis, server-streamed synthesis, and a streaming WebSocket interface with instant + professional voice cloning, voice design from text prompts, custom pronunciation, pause controls, word/character/phoneme alignment for lipsync, and zero-data-retention plus on-premise deployment options.

- **Human URL:** [https://docs.inworld.ai/tts/tts](https://docs.inworld.ai/tts/tts)

#### Tags

- AI
- Artificial Intelligence
- Text To Speech
- Voice
- Audio

#### Properties

- [Documentation](https://docs.inworld.ai/tts/tts)
- [Getting Started](https://docs.inworld.ai/quickstart-tts)
- [Documentation](https://docs.inworld.ai/api-reference/ttsAPI/texttospeech/synthesize-speech)
- [Documentation](https://docs.inworld.ai/api-reference/ttsAPI/texttospeech/synthesize-speech-stream)
- [Documentation](https://docs.inworld.ai/api-reference/ttsAPI/texttospeech/synthesize-speech-websocket)
- [Documentation](https://docs.inworld.ai/tts/voice-cloning)
- [Documentation](https://docs.inworld.ai/tts/voice-design)
- [Documentation](https://docs.inworld.ai/tts/on-premises)
- [OpenAPI](openapi/inworld-tts-api-openapi.yml) — [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [Postman Collection](collections/inworld-tts-api.postman_collection.json) — [Postman Collection 2.1](https://schema.getpostman.com/json/collection/v2.1.0/collection.json)
- [Open Collection](collections/inworld-tts-api.opencollection.json) — [Open Collection 1.0](https://schema.opencollection.com/opencollection/v1.0.0.json)
- [AsyncAPI](asyncapi/inworld-ai-asyncapi.yml) — [AsyncAPI Specification](https://www.asyncapi.com/docs/reference/specification/latest)
- [JSON Schema](json-schema/inworld-tts-synthesis-schema.json) — [JSON Schema](https://json-schema.org/specification)
- [JSON-LD](json-ld/inworld-ai-context.jsonld) — [JSON-LD](https://www.w3.org/TR/json-ld11/)

### Inworld Voice API

Inworld Voice API — manage custom voices used by the TTS and Realtime APIs. Clone voices from short audio samples (instant voice cloning) or design voices from natural-language descriptions plus optional reference audio. Lists, gets, updates, and deletes voices, and exposes a publish endpoint for sharing voices across a workspace.

- **Human URL:** [https://docs.inworld.ai/api-reference/voiceAPI/voiceservice/list-voices](https://docs.inworld.ai/api-reference/voiceAPI/voiceservice/list-voices)

#### Tags

- AI
- Artificial Intelligence
- Voice
- Voice Cloning
- Voice Design

#### Properties

- [Documentation](https://docs.inworld.ai/tts/voice-cloning)
- [Documentation](https://docs.inworld.ai/tts/voice-design)
- [Documentation](https://docs.inworld.ai/api-reference/voiceAPI/voiceservice/clone-voice)
- [Documentation](https://docs.inworld.ai/api-reference/voiceAPI/voiceservice/design-voice)
- [Documentation](https://docs.inworld.ai/api-reference/voiceAPI/voiceservice/publish-voice)
- [Documentation](https://docs.inworld.ai/api-reference/voiceAPI/voiceservice/list-voices)
- [OpenAPI](openapi/inworld-voice-api-openapi.yml) — [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [Postman Collection](collections/inworld-voice-api.postman_collection.json) — [Postman Collection 2.1](https://schema.getpostman.com/json/collection/v2.1.0/collection.json)
- [Open Collection](collections/inworld-voice-api.opencollection.json) — [Open Collection 1.0](https://schema.opencollection.com/opencollection/v1.0.0.json)

### Inworld STT API

Inworld STT — speech-to-text transcription API with synchronous transcribe and a streaming WebSocket endpoint. Multi-provider routing (currently Whisper variants via Groq) with 99+ language support, word timestamps, voice profiling, prompt biasing for domain-specific vocabulary, and configurable end-of-turn detection for low-latency conversational agents.

- **Human URL:** [https://docs.inworld.ai/stt/overview](https://docs.inworld.ai/stt/overview)

#### Tags

- AI
- Artificial Intelligence
- Speech To Text
- Transcription
- Voice

#### Properties

- [Documentation](https://docs.inworld.ai/stt/overview)
- [Getting Started](https://docs.inworld.ai/stt/quickstart)
- [Documentation](https://docs.inworld.ai/api-reference/sttAPI/speechtotext/transcribe)
- [Documentation](https://docs.inworld.ai/api-reference/sttAPI/speechtotext/transcribe-stream-websocket)
- [Documentation](https://docs.inworld.ai/stt/voice-profiles)
- [OpenAPI](openapi/inworld-stt-api-openapi.yml) — [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [Postman Collection](collections/inworld-stt-api.postman_collection.json) — [Postman Collection 2.1](https://schema.getpostman.com/json/collection/v2.1.0/collection.json)
- [Open Collection](collections/inworld-stt-api.opencollection.json) — [Open Collection 1.0](https://schema.opencollection.com/opencollection/v1.0.0.json)
- [AsyncAPI](asyncapi/inworld-ai-asyncapi.yml) — [AsyncAPI Specification](https://www.asyncapi.com/docs/reference/specification/latest)

### Inworld Realtime API

Inworld Realtime — end-to-end speech-to-speech voice pipeline (STT + LLM + TTS) exposed over WebSocket and WebRTC. OpenAI-Realtime-API-compatible event protocol (session.update, input_audio_buffer.append, response.create, etc.) so existing OpenAI Realtime clients can swap base URLs. Includes server-side and semantic VAD, function/tool calling, MCP server tunneling, Twilio media-stream integration, and JWT-based session authentication.

- **Human URL:** [https://docs.inworld.ai/realtime/overview](https://docs.inworld.ai/realtime/overview)

#### Tags

- AI
- Artificial Intelligence
- Realtime
- Voice
- WebSocket
- WebRTC

#### Properties

- [Documentation](https://docs.inworld.ai/realtime/overview)
- [Getting Started](https://docs.inworld.ai/realtime/quickstart-websocket)
- [Getting Started](https://docs.inworld.ai/realtime/quickstart-webrtc)
- [Documentation](https://docs.inworld.ai/api-reference/realtimeAPI/realtime/realtime-websocket)
- [Documentation](https://docs.inworld.ai/api-reference/realtimeAPI/realtime/realtime-webrtc)
- [Documentation](https://docs.inworld.ai/realtime/openai-migration)
- [Documentation](https://docs.inworld.ai/realtime

... (truncated, 7021 more characters)

## Top-level layout

- agentic-access/ (dir, 1 files, ~231 lines)
- apis.yml (~697 lines)
- asyncapi/ (dir, 1 files, ~1086 lines)
- authentication/ (dir, 1 files, ~22 lines)
- collections/ (dir, 25 files, ~6895 lines)
- examples/ (dir, 3 files, ~134 lines)
- finops/ (dir, 1 files, ~129 lines)
- front-door-ai/ (dir, 1 files, ~32 lines)
- json-ld/ (dir, 1 files, ~108 lines)
- json-schema/ (dir, 2 files, ~144 lines)
- kin/ (dir, 60 files, ~2992 lines)
- openapi/ (dir, 13 files, ~2848 lines)
- plans/ (dir, 1 files, ~122 lines)
- postman/ (dir, 5 files, ~2608 lines)
- provenance.yml (~320 lines)
- rate-limits/ (dir, 1 files, ~55 lines)
- README.md (~321 lines)
- review.yml (~36 lines)
- rules/ (dir, 3 files, ~204 lines)
- screenshots/ (dir, 2 files, ~10 lines)
- security/ (dir, 2 files, ~44 lines)
- vocabulary/ (dir, 1 files, ~108 lines)

