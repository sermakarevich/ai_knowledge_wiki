---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: api-evangelist/inworld-ai

### Q1. What is the api-evangelist/inworld-ai repository, and what does it explicitly disclaim?

> [!tip]- Answer
> It is an independent third-party API Evangelist profile of Inworld AI's public real-time voice-AI platform, cataloging its TTS, Voice, STT, and Realtime APIs behind one API surface and billing relationship. It contains no software, build, release, or binary — only text and machine-readable API descriptions assembled from browser-reachable public material. Its recorded position is Consuming with 3rd-Party access, tagged AI, Voice, Text To Speech, Speech To Text, Realtime, LLM Routing, Voice Cloning, Conversational AI, and Game AI. See [[wiki/01-overview|Overview]].

### Q2. What models, interfaces, and features does the Inworld TTS API provide?

> [!tip]- Answer
> The TTS API offers Realtime TTS-2 (100+ languages with natural-language steering), TTS 1.5 Max (15 languages), and cost-optimized TTS 1.5 Mini with sub-120 ms first-token latency. It exposes synchronous synthesis, server-streamed synthesis, and a streaming WebSocket interface. Features include instant and professional voice cloning, voice design from text prompts, custom pronunciation, pause controls, word/character/phoneme alignment for lipsync, and zero-data-retention plus on-premise deployment. See [[wiki/01-overview|Overview]].

### Q3. How does the Inworld Voice API manage custom voices?

> [!tip]- Answer
> It supports instant voice cloning from short audio samples as well as voice design from natural-language descriptions plus optional reference audio. Its operations list, get, update, and delete voices, with an additional publish endpoint for sharing voices across a workspace. Spec artifacts include a per-API OpenAPI file plus Postman and OpenCollection collection files. See [[wiki/01-overview|Overview]].

### Q4. What are the key capabilities of the Inworld STT API?

> [!tip]- Answer
> The STT API provides synchronous transcribe alongside a streaming WebSocket endpoint, with multi-provider routing (currently Whisper variants via Groq) covering 99+ languages. It adds word timestamps, voice profiling, prompt biasing for domain-specific vocabulary, and configurable end-of-turn detection. Its machine-readable artifacts include a per-API OpenAPI file, collections, and the shared AsyncAPI description. See [[wiki/01-overview|Overview]].

### Q5. What kind of system is the Inworld Realtime API, and how does it stay compatible with existing clients?

> [!tip]- Answer
> It is an end-to-end speech-to-speech voice pipeline (STT + LLM + TTS) exposed over WebSocket and WebRTC. It uses an OpenAI-Realtime-API-compatible event protocol (`session.update`, `input_audio_buffer.append`, `response.create`, etc.) so existing OpenAI Realtime clients can swap base URLs. It also provides server-side and semantic VAD, function/tool calling, MCP server tunneling, Twilio media-stream integration, and JWT-based session authentication. See [[wiki/01-overview|Overview]].

### Q6. What does `apis.yml` declare, and what shared artifact set backs the catalog entries?

> [!tip]- Answer
> The catalog root declares `aid: inworld-ai` with `name: Inworld AI` and lists five APIs: Realtime (speech-to-speech sessions), Speech To Text (transcribe audio), Text To Speech (synthesize speech), Voices (cloning, design, lifecycle), and Chat Completions (OpenAI-compatible completions through the LLM Router). The voice entries each repeat the same machine-readable property set pointing at a per-API OpenAPI file plus the shared `asyncapi/inworld-ai-asyncapi.yml`, `json-schema/inworld-tts-synthesis-schema.json`, and `json-ld/inworld-ai-context.jsonld`, alongside Documentation and GettingStarted URLs. See [[wiki/02-top-level-files|Top-level Files]].

### Q7. How does `provenance.yml` distinguish how each artifact was produced?

> [!tip]- Answer
> It maps every artifact path to a `method` plus `evidence`: `harvested` means provider-fetched byte-identical sources (the six `openapi/_original/` specs), while `derived` means built from another artifact (the seven path-subset `openapi/inworld-ai-*-openapi.yml` specs and the collections/Postman files generated from them). `generated` covers tool-written files such as agentic-access and Kin score snapshots, and `unknown` means no authorship record, which applies to the AsyncAPI file and TTS JSON Schema. The manifest itself is version `provenance: '0.1'`, produced by `build-provenance-manifest.py` with drift checked by `check-provenance-manifest.py`. See [[wiki/02-top-level-files|Top-level Files]].

### Q8. A team wants one vendor for cloned voices plus an OpenAI-compatible realtime voice pipeline — should they adopt Inworld AI on the strength of this profile alone?

> [!tip]- Answer
> They should treat the profile as a promising discovery lead, not an adoption basis: the independent Tier-1 Consuming review credits a unified base URL and billing surface, drop-in OpenAI Realtime/Chat Completions and Anthropic Messages compatibility, and first-class cloning with phoneme/viseme alignment, but it is still a third-party description with no software and no endorsement. Before committing, they must verify current cloning quality, realtime latency, pricing with rollover, and zero-data-retention/on-prem terms directly in Inworld's own docs and portal, since the review also flags reconstructed OpenAPIs and a narratively documented Realtime protocol. See [[wiki/02-top-level-files|Top-level Files]].
