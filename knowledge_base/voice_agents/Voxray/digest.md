> [[index|Wiki]] | [[summary|Summary]]
# Voxray-AI/Voxray — Digest

## 1. [[wiki/01-overview|Overview]]
**In one sentence:** Voxray is a config-driven Go server that wires STT → LLM → TTS providers into a single low-latency streaming voice pipeline delivered over WebSocket or WebRTC.
## Key points
- Voxray is a config-driven Go server for production-ready real-time voice AI agents wiring STT → LLM → TTS into one low-latency streaming pipeline over WebSocket or WebRTC (README.md:31).
- The per-session pipeline runs MIC → VAD → STT → LLM → TTS → Transport Sink inside the Voxray server, fronted by an HTTP server with `/ws`, `/webrtc/offer`, `/start`, `/metrics`, `/swagger/` (README.md:87).
- Transport is dual: WebSocket (`/ws`) and WebRTC via SmallWebRTC (`/webrtc/offer`), switchable at runtime, plus telephony via Twilio, Telnyx, Plivo, Exotel, and Daily.co (README.md:54).
- Provider coverage is wide out of the box: 10+ STT, 20+ LLM, and 15+ TTS providers, swapped by changing a single field in `config.json` (README.md:56).
- The whole agent is defined by one JSON file covering providers, models, voices, turn detection, recording, and more, with env-var overrides for every value (README.md:63).
- Go 1.25+ is the only hard dependency for the default WebSocket build, while WebRTC + Opus TTS audio additionally requires CGO and `gcc` on PATH (README.md:141).
- Barge-in/interruption is a configurable strategy so users can cut the agent mid-sentence, alongside MCP tool calls, S3 WAV recording, Postgres/MySQL transcripts, Prometheus `/metrics`, and a plugin system (README.md:57).

## 2. [[wiki/02-top-level-files|Top-level-files]]
**In one sentence:** Top-level files define the repo's runnable and documented surface — ignored build/secret paths, the server API contract, the example runtime config, pinned Go dependencies, license notice, and build/test workflows.
## Key points
- `.gitignore` excludes build outputs, coverage, dependencies, and secrets so `go build`/`go test` artifacts and local configs never enter the repo (.gitignore:9-51).
- `API_SERVER.md` documents the voice-pipeline HTTP/WebSocket API with versioned `/api/v1` routes, legacy-path compatibility, and env-based host/port configuration (API_SERVER.md:64-71).
- Authentication is an optional static API key passed as `Authorization: Bearer <key>` or `X-API-Key: <key>`, failing with `401 UNAUTHORIZED` only when `server_api_key` is configured (API_SERVER.md:77-83).
- All JSON responses use a `{ "data", "meta" }` success envelope and `{ "error": { "code", "message", "requestId", "details" } }` error envelope, with a 256 KB default body cap and no pagination (API_SERVER.md:91-97).
- `config.example.json` is the copy-to-`config.json` template for host/port, providers/models, transport, VAD/turn-detection, plugins, CORS, body limit, and empty API-key placeholders (config.example.json:365-449).
- `go.sum` pins every Go module hash used by the build, including AWS, Google Cloud, and envoy/protovalidate dependency trees (go.sum:455-578).
- `TESTING.md` defines `make build`/`make run`/`make test` and `go test ./...` scopes, with Sarvam live tests skipped unless `SARVAM_API_KEY` is set (TESTING.md:602-623).
- `NOTICE` attributes copyright to Voxray-AI (2026) and states Apache License 2.0 terms with a link to the license text (NOTICE:585-595).

## The system in five moves
1. Voxray starts from a single JSON config that declares the whole voice agent — STT, LLM, TTS providers, models, voices, turn detection, recording, and transport.
2. Each session runs the streaming chain MIC → VAD → STT → LLM → TTS → Transport Sink inside the Go server, fronted by one HTTP server.
3. Audio reaches clients over dual transports — WebSocket (`/ws`) and WebRTC (`/webrtc/offer`), switchable at runtime — extended by Twilio, Telnyx, Plivo, Exotel, and Daily.co telephony.
4. Breadth comes from 10+ STT, 20+ LLM, and 15+ TTS providers swapped by one config field, plus barge-in, MCP tools, plugins, S3 recording, Postgres/MySQL transcripts, and Prometheus metrics.
5. The runnable surface is pinned down at the top level: `.gitignore` keeps builds/secrets out, `config.example.json` templates runtime, `go.sum` pins dependencies, and `NOTICE` states Apache-2.0 terms.
6. That surface is served through a versioned `/api/v1` HTTP/WebSocket contract with optional static API-key auth, standard success/error envelopes, and a 256 KB body cap.
7. Builds stay minimal — Go 1.25+ for WebSocket, plus CGO/gcc for WebRTC Opus — verified by `make build`/`make run`/`make test` and `go test ./...`, with live Sarvam tests gated on `SARVAM_API_KEY`.
