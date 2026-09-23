---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: api-evangelist/pipecat-ai

### Q1. What is Pipecat at its core, and who created it?
> [!tip]- Answer
> Pipecat is an open-source Python framework created by Daily for building realtime voice and multimodal AI agents. Its interface is the `pipecat-ai` library, not a REST API. See [[wiki/01-overview|Overview]].

### Q2. How do FrameProcessors, Pipelines, and Frames fit together in the Pipecat framework?
> [!tip]- Answer
> Applications wire `FrameProcessor`s into a `Pipeline`, where `Frame`s carry audio, text, images, and control signals between pluggable AI services such as STT, LLM, TTS, and vision and the client transports. This pipeline model is the core programming abstraction of the framework. See [[wiki/01-overview|Overview]].

### Q3. What is Pipecat Cloud, and what is its base URL and auth model?
> [!tip]- Answer
> Pipecat Cloud is the hosted operational layer: a Bearer-token authenticated REST control API for deploying agents and managing sessions, builds, secrets, and organization properties. It supports agent CRUD, session start/stop, and related operations. It is served from `https://api.pipecat.daily.co/v1`. See [[wiki/01-overview|Overview]].

### Q4. Why are Daily WebRTC, SmallWebRTC, LiveKit, and the FastAPI WebSocket server not counted as a public control API?
> [!tip]- Answer
> They are SDK transport classes for realtime media flow, including telephony serializers for Twilio, Telnyx, Plivo, and Exotel — not a hosted public REST or WebSocket control surface. That is why the review verdict records no documented public WebSocket control API and no AsyncAPI document. See [[wiki/02-top-level-files|Top-Level Files]].

### Q5. What does `apis.yml` catalog, and what are the five Pipecat Cloud REST sub-APIs?
> [!tip]- Answer
> `apis.yml` defines the profile as `aid: pipecat-ai` / `name: Pipecat` and splits the surface into the library framework interface, SDK transport classes, and five Cloud REST sub-APIs sharing one base URL. The five are agents, builds, organization, secrets, and sessions. It also declares SaaS freemium self-serve delivery. See [[wiki/02-top-level-files|Top-Level Files]].

### Q6. What do `provenance.yml` and `review.yml` each establish about this profile?
> [!tip]- Answer
> `provenance.yml` records per-artifact authorship as `generated`, `derived`, or `unknown`, noting it was built by `build-provenance-manifest.py` with drift checked by `check-provenance-manifest.py`. `review.yml` confirms the only Pipecat-owned hosted HTTP surface is the Cloud REST control API and answers `false` on a public WebSocket control API. See [[wiki/02-top-level-files|Top-Level Files]].

### Q7. A team wants realtime voice agents with managed deployment: should they adopt the framework alone, Cloud alone, or both, and why?
> [!tip]- Answer
> They should adopt both together: use the open-source framework for pipeline flexibility with pluggable STT/LLM/TTS and transports, and Cloud for hosted agent deployment, session lifecycle, secrets, and builds at scale. Framework-only fits self-hosted prototypes, while Cloud-only without the pipeline model misses how agents are actually built. The freemium self-serve Cloud model supports starting small before scaling. See [[wiki/01-overview|Overview]].
