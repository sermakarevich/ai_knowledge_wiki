> [[index|Wiki]] | [[summary|Summary]]
# api-evangelist/pipecat-ai — Digest

## 1. [[wiki/01-overview|Overview]]
**In one sentence:** Pipecat is an open-source Python framework for building realtime voice and multimodal AI agents, plus a hosted Pipecat Cloud REST API for deploying agents and managing agent sessions at scale (README.md:73).
## Key points
- Pipecat is an open-source Python framework created by Daily for building realtime voice and multimodal AI agents (README.md:73).
- The framework orchestrates pipelines of frames through pluggable services including STT, LLM, TTS, and vision, with transports such as Daily WebRTC, WebSocket, SmallWebRTC, and telephony (README.md:73).
- The Pipecat Framework interface is the `pipecat-ai` Python library, not a REST API: applications wire `FrameProcessor`s into a `Pipeline` where `Frame`s carry audio, text, images, and control signals (README.md:95).
- Pipecat Cloud is a hosted, Bearer-token authenticated REST control API for deploying and operating agents — create/list/update/delete agents, start and stop sessions, and manage builds, secrets, and organization properties (README.md:115).
- The Pipecat Cloud REST API is served from base URL `https://api.pipecat.daily.co/v1` (README.md:118).
- The realtime transport layer (Daily WebRTC, SmallWebRTC, LiveKit, FastAPI WebSocket server, telephony serializers for Twilio/Telnyx/Plivo/Exotel) consists of SDK transport classes, not a hosted public REST/WebSocket control API (README.md:138).
- The profile is a third-party API Evangelist listing built only from publicly reachable material with no credentials, and it contains no software, builds, or binaries (README.md:17, README.md:57).

## 2. [[wiki/02-top-level-files|Top-Level Files]]
**In one sentence:** The repository root declares Pipecat as an open-source Python voice/multimodal framework plus a hosted Pipecat Cloud REST control API, and tracks artifact authorship and API-review findings in `apis.yml`, `provenance.yml`, and `review.yml`.
## Key points
- `apis.yml` defines the profile as `aid: pipecat-ai` / `name: Pipecat`, describing an open-source Python framework for realtime voice and multimodal agents orchestrated through pluggable STT/LLM/TTS/vision services and transports (apis.yml:9-17).
- `apis.yml` splits the surface into the `pipecat-ai` library framework interface, SDK transport classes, and five Pipecat Cloud REST sub-APIs (agents, builds, organization, secrets, sessions) sharing baseURL `https://api.pipecat.daily.co/v1` (apis.yml:63-180).
- `apis.yml` declares delivery as SaaS/hosted-service with `open_source: false`, `commercial: true`, `callable_host: true` derived from openapi and pricing sources (apis.yml:18-29).
- `apis.yml` declares freemium self-serve access with `try_now: true`, `public: false`, grounded in plans, authentication, and security sources (apis.yml:30-43).
- `provenance.yml` records authorship per artifact as `generated`, `derived`, or `unknown`, noting it was built by `build-provenance-manifest.py` with drift checked by `check-provenance-manifest.py` (provenance.yml:213-216).
- `review.yml` answers `false` to whether Pipecat exposes a documented public WebSocket control API, creating no AsyncAPI document because WebSocket exists only as an SDK media transport class (review.yml:444-459).
- `review.yml` confirms the only Pipecat-owned hosted HTTP surface is the Pipecat Cloud REST control API at `https://api.pipecat.daily.co/v1`, enumerating agents, sessions, builds, secrets, properties, and regions endpoints (review.yml:471-523).

## The system in five moves
1. Pipecat starts as an open-source Python framework where `FrameProcessor`s wired into a `Pipeline` pass audio, text, images, and control signals between pluggable STT/LLM/TTS/vision services and client transports.
2. Realtime media flows over SDK transport classes — Daily WebRTC, SmallWebRTC, LiveKit, FastAPI WebSocket server, and telephony serializers — which are not a hosted public control API.
3. Pipecat Cloud adds the hosted operational layer: a Bearer-token REST control API at `https://api.pipecat.daily.co/v1` for deploying and running agents at scale.
4. The profile catalogs that surface in `apis.yml` as the library interface plus transport classes plus five Cloud REST sub-APIs (agents, builds, organization, secrets, sessions) with SaaS freemium self-serve delivery.
5. `provenance.yml` tracks authorship of each artifact as generated, derived, or unknown, and `review.yml` verifies the only hosted HTTP surface is the Cloud REST API with no public WebSocket control API to model.
