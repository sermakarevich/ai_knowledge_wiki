---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: Voxray-AI/Voxray

### Q1. What is Voxray and what pipeline does each session run?
> [!tip]- Answer
> Voxray is a config-driven Go server for real-time voice AI agents that wires STT → LLM → TTS into one low-latency streaming pipeline. Each session runs MIC → VAD → STT → LLM → TTS → Transport Sink inside the Voxray server, fronted by one HTTP server. See [[wiki/01-overview|Overview]].

### Q2. Which transports and telephony integrations does Voxray support?
> [!tip]- Answer
> Voxray supports dual transport — WebSocket at `/ws` and WebRTC via SmallWebRTC at `/webrtc/offer` — switchable at runtime. It also extends to telephony through Twilio, Telnyx, Plivo, Exotel, and Daily.co rooms with optional PSTN dial-in. See [[wiki/01-overview|Overview]].

### Q3. How do you swap providers or models in Voxray, and how broad is the built-in coverage?
> [!tip]- Answer
> Any stage is swapped by changing a single provider/model field in `config.json`, for example switching STT/LLM/TTS to Sarvam saarika:v2.5, Groq llama-3.1-8b-instant, and Sarvam bulbul:v2. Built-in coverage is roughly 10+ STT, 20+ LLM, and 15+ TTS providers, with the full matrix in `pkg/services/README.md`. See [[wiki/01-overview|Overview]].

### Q4. What are Voxray's build requirements, and what happens without CGO for WebRTC?
> [!tip]- Answer
> Go 1.25+ is the only hard dependency for the default WebSocket-only build, while WebRTC plus Opus TTS audio additionally requires CGO with `gcc` on PATH. Without CGO the server reports opus encoder unavailable and returns 503 on WebRTC offers. See [[wiki/01-overview|Overview]].

### Q5. How do authentication and response envelopes work in Voxray's HTTP/WebSocket API?
> [!tip]- Answer
> Auth is an optional static API key sent as `Authorization: Bearer <key>` or `X-API-Key: <key>`, enforced with a `401 UNAUTHORIZED` error only when `server_api_key` is configured. Success bodies use a `{ "data", "meta" }` envelope and errors use `{ "error": { "code", "message", "requestId", "details" } }`, with a 256 KB default body cap and versioned `/api/v1` routes alongside legacy paths. See [[wiki/02-top-level-files|Top-level-files]].

### Q6. What do `config.example.json`, `.gitignore`, and `TESTING.md` establish for running and testing Voxray?
> [!tip]- Answer
> `config.example.json` is the copy-to-`config.json` template covering host/port, providers, transport, VAD/turn-detection, plugins, CORS, body limit, and empty API-key placeholders. `.gitignore` keeps build outputs, coverage, vendor files, and secret configs like `/config.json` and `.env` out of the repo. `TESTING.md` maps `make build`/`make run`/`make test` to `go build`/`go test ./...` scopes, with Sarvam live tests skipped unless `SARVAM_API_KEY` is set. See [[wiki/02-top-level-files|Top-level-files]].

### Q7. When would you recommend Voxray over a managed voice-agent cloud, and when would you avoid it?
> [!tip]- Answer
> Recommend Voxray when you need a self-hostable, config-driven voice stack with broad provider choice, dual WebSocket/WebRTC transport, and telephony plus recording/transcript/observability on your own infra. Avoid it when you want zero-ops managed scaling, lack Go/CGO build capacity for WebRTC, or need richer auth than a static API key. See [[wiki/01-overview|Overview]].
