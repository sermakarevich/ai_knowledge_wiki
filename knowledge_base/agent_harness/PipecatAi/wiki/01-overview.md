> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** Pipecat is an open-source Python framework for building realtime voice and multimodal AI agents, plus a hosted Pipecat Cloud REST API for deploying agents and managing agent sessions at scale (README.md:73).
## Key points
- Pipecat is an open-source Python framework created by Daily for building realtime voice and multimodal AI agents (README.md:73).
- The framework orchestrates pipelines of frames through pluggable services including STT, LLM, TTS, and vision, with transports such as Daily WebRTC, WebSocket, SmallWebRTC, and telephony (README.md:73).
- The Pipecat Framework interface is the `pipecat-ai` Python library, not a REST API: applications wire `FrameProcessor`s into a `Pipeline` where `Frame`s carry audio, text, images, and control signals (README.md:95).
- Pipecat Cloud is a hosted, Bearer-token authenticated REST control API for deploying and operating agents — create/list/update/delete agents, start and stop sessions, and manage builds, secrets, and organization properties (README.md:115).
- The Pipecat Cloud REST API is served from base URL `https://api.pipecat.daily.co/v1` (README.md:118).
- The realtime transport layer (Daily WebRTC, SmallWebRTC, LiveKit, FastAPI WebSocket server, telephony serializers for Twilio/Telnyx/Plivo/Exotel) consists of SDK transport classes, not a hosted public REST/WebSocket control API (README.md:138).
- The profile is a third-party API Evangelist listing built only from publicly reachable material with no credentials, and it contains no software, builds, or binaries (README.md:17, README.md:57).
---
## Repository identity
This repository is an independent, third-party profile of Pipecat's publicly available API surface, maintained by API Evangelist — not an API operated, hosted, resold, or supported by API Evangelist (README.md:12).
> "Pipecat is an open-source Python framework (created by Daily) for building realtime voice and multimodal AI agents. It orchestrates pipelines of frames through pluggable services (STT, LLM, TTS, vision) and transports (Daily WebRTC, WebSocket, SmallWebRTC, telephony). Pipecat Cloud adds a hosted platform with a REST control API for deploying agents and starting/stopping agent sessions at scale." (README.md:73)
- **APIs.json:** `https://raw.githubusercontent.com/api-evangelist/pipecat-ai/refs/heads/main/apis.yml` (README.md:75)
- **Tags:** AI, Voice, Multimodal, Agents, Realtime, Framework (README.md:79)
- **Timestamps:** Created 2026-06-21; Modified 2026-06-21 (README.md:88)
## Pipecat Framework (Python SDK)
Open-source (BSD 2-Clause) Python framework whose interface is the `pipecat-ai` library, not a REST API (README.md:95).
> "Applications wire FrameProcessors into a Pipeline, where Frames carry audio, text, images, and control signals between pluggable AI Services (STT, LLM, TTS, vision) and client Transports." (README.md:95)
| Property | Value |
|---|---|
| Human URL | `https://docs.pipecat.ai/overview/introduction` (README.md:97) |
| Documentation | `https://docs.pipecat.ai/overview/introduction` (README.md:109) |
| API Reference | `https://docs.pipecat.ai/server/introduction` (README.md:110) |
| GitHub | `https://github.com/pipecat-ai/pipecat` (README.md:111) |
| Tags | Framework, Python, SDK, Pipelines, Frames (README.md:101) |
## Pipecat Cloud (Agents/Sessions API)
Hosted REST control API (Bearer-token authenticated) for deploying and operating Pipecat agents on Pipecat Cloud (README.md:115).
> "create/list/update/delete agents, start and stop agent sessions, manage builds, secrets, and organization properties." (README.md:115)
| Property | Value |
|---|---|
| Human URL | `https://docs.pipecat.ai/api-reference/pipecat-cloud/rest-reference` (README.md:117) |
| Base URL | `https://api.pipecat.daily.co/v1` (README.md:118) |
| Documentation | `https://docs.pipecat.ai/overview/cloud` (README.md:130) |
| API Reference | `https://docs.pipecat.ai/api-reference/pipecat-cloud/rest-reference` (README.md:131) |
| OpenAPI | `openapi/pipecat-ai-openapi.yml` (README.md:132) |
| Postman Collection | `collections/pipecat-ai.postman_collection.json` (README.md:133) |
| Open Collection | `collections/pipecat-ai.opencollection.json` (README.md:134) |
| Tags | Cloud, Agents, Sessions, REST, Deployment (README.md:123) |
## Transports (WebRTC/WebSocket)
Realtime media transport layer of the framework; bidirectional audio, video, and data flow over Daily WebRTC, SmallWebRTC, LiveKit, FastAPI WebSocket server, and telephony serializers (Twilio, Telnyx, Plivo, Exotel) (README.md:138).
> "These are SDK transport classes, not a hosted public REST/WebSocket control API." (README.md:138)
| Property | Value |
|---|---|
| Human URL | `https://docs.pipecat.ai/server/services/supported-services` (README.md:140) |
| Documentation | `https://docs.pipecat.ai/server/services/supported-services` (README.md:152) |
| GitHub | `https://github.com/pipecat-ai/pipecat` (README.md:153) |
| Tags | Transports, WebRTC, WebSocket, Telephony, Realtime (README.md:144) |
## Common properties and maintainers
| Property | Value |
|---|---|
| GitHub Organization | `https://github.com/pipecat-ai` (README.md:157) |
| LinkedIn | `https://www.linkedin.com/company/daily-co` (README.md:158) |
| Website | `https://www.pipecat.ai` (README.md:159) |
| Documentation | `https://docs.pipecat.ai` (README.md:160) |
| Plans | `plans/pipecat-ai-plans-pricing.yml` (README.md:161) |
| Rate Limits | `rate-limits/pipecat-ai-rate-limits.yml` (README.md:162) |
| Fin Ops | `finops/pipecat-ai-finops.yml` (README.md:163) |
- **Maintainer:** Kin Lane, `kin@apievangelist.com` (README.md:167)
- **Macro components listed on this page:** `top-level-files/` (README.md:172)
- No truncated files were noted in the chunk; all claims above come from the full chunk text.
**Covers:** `README.md` (repository identity, tags, timestamps, framework / cloud / transports API entries, common properties, maintainer, macro-component list)
