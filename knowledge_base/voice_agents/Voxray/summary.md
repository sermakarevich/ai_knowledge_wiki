# Technical Analysis: Voxray-AI/Voxray

**Repository:** https://github.com/Voxray-AI/Voxray
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Real-time voice agents require wiring audio capture, voice activity detection, speech-to-text, an LLM, text-to-speech, and a delivery transport (browser, mobile, telephony) into a single low-latency streaming loop, plus auth, observability, recording, and transcript persistence. Voxray addresses this by providing a config-driven Go server that wires STT → LLM → TTS providers into one streaming pipeline delivered over WebSocket or WebRTC, defined by a single JSON file (README.md:31, README.md:33). The per-session chain is MIC → VAD → STT → LLM → TTS → Transport Sink, fronted by an HTTP server exposing `/ws`, `/webrtc/offer`, `/start`, `/metrics`, `/swagger/` (README.md:87). Providers are swapped by changing one field in `config.json` (README.md:99), with 10+ STT, 20+ LLM, and 15+ TTS providers out of the box (README.md:56). The primary user is a developer deploying a self-hosted production voice agent on their own infra or VPC without vendor lock-in (README.md:57).

## 2. High-Level Architecture

```
CLIENT (Browser / Mobile / Telephony / Daily.co)
  │  WebSocket / WebRTC / Telephony WS
  ▼                                         ▲
VOXRAY SERVER ──────────────────────────────
  │ HTTP server: /ws ─ /webrtc/offer ─ /start ─ /metrics ─ /swagger/
  ▼
Runner ──► PIPELINE (per session):
  MIC ─► VAD ─► STT ─► LLM ─► TTS ─► Transport Sink
           │      │      │      │
           ▼      ▼      ▼      ▼
        STT API  LLM API TTS API  S3 / DB sinks
        (Sarvam, (OpenAI, (ElevenL,
         OpenAI,  Groq,   Sarvam,
         Groq..)  Claude) Google)
```

(Redrawn from the verbatim README.md:74 diagram summarized in 01-overview.md:20-44.)

Data flow: (1) Audio enters from browser, native client, or a telephony provider over WebSocket, WebRTC via SmallWebRTC, or a provider-specific WebSocket, and is routed by the HTTP server into a per-session Runner-owned pipeline (README.md:72, README.md:87). (2) The pipeline stages audio through VAD/turn detection (`energy` or `silero`, README.md:302), STT transcription, LLM completion (with optional MCP tool calls), and TTS synthesis, each stage calling an external provider API (README.md:53, README.md:57). (3) Synthesized audio streams back to the caller through the session's transport sink; barge-in lets the user interrupt mid-sentence per the configured interruption strategy (README.md:57). (4) Side sinks persist state asynchronously: mixed-audio WAV per session uploaded to S3, and per-message transcripts to Postgres or MySQL (README.md:57, README.md:348, README.md:362). (5) Observability and control run alongside: Prometheus text at `/metrics` (204 when disabled), structured JSON logs, liveness at `/health`, readiness at `/ready` (503 when the Redis session-store ping fails), versioned `/api/v1` routes with legacy-path compatibility, and optional static API-key auth (API_SERVER.md:64-71, API_SERVER.md:159-225).

Persistent state lives outside the server process: session recordings in the configured S3 bucket under `recordings/` (config `recording.bucket`, `recording.base_path`), transcripts in the configured Postgres/MySQL `call_transcripts` table, idempotency keys with 24h TTL for `POST /start`, and an optional Redis session store checked by `/ready` (README.md:348, README.md:362, API_SERVER.md:186-209, API_SERVER.md:278-317). No in-repo database schema or migration beyond the configured DSN and table name is described in the wiki.

## 3. The Config-Driven Voice Pipeline

The central abstraction is the **session pipeline**: a linear, fully streamed MIC → VAD → STT → LLM → TTS → speaker chain instantiated per session from one JSON config file covering providers, models, voices, turn detection, recording, and more, with env-var overrides for every value (README.md:53, README.md:63). Representation is declarative configuration, not code: provider selection is string fields (`stt_provider`, `llm_provider`, `tts_provider`), model selection is string fields (`stt_model`, `model`, `tts_model`, `tts_voice`), and pipeline behavior is scalar fields (`turn_detection`, `turn_stop_secs`, `vad_threshold`, `vad_type`, `allow_interruptions`, `interruption_strategy`, `min_words`) plus a `plugin_options` object (config.example.json:365-449, README.md:302).

Named kinds/types visible in the wiki: transports `"websocket"`, `"smallwebrtc"`, `"both"` (README.md:302) with `runner_transport` values `"webrtc"`, `"daily"`, `"twilio"`, `"telnyx"`, `"plivo"`, `"exotel"` (README.md:302); VAD modes `"energy"`, `"silero"` (README.md:302); interruption strategies including `"keyword"` and `min_words` (config.example.json:365-449); plugin option blocks `frame_filter`, `wake_check_filter`, `stt_mute_filter`, `audio_filter`, `interruption_controller`, `external_chain`, `rtvi` (config.example.json:386-418); error envelope codes `BAD_REQUEST`, `UNAUTHORIZED`, `NOT_FOUND`, `INTERNAL_ERROR`, `SERVICE_UNAVAILABLE`, `VALIDATION_ERROR` plus reserved `CONFLICT`, `FORBIDDEN`, `RATE_LIMIT_EXCEEDED`, `UNPROCESSABLE_ENTITY` (API_SERVER.md:118-151).

Key query — the pipeline is defined, not queried; its canonical "query" is the minimal config (README.md:274):

```json
{
  "transport": "both",
  "host": "0.0.0.0",
  "port": 8080,
  "stt_provider": "openai",
  "stt_model": "gpt-4o-mini-transcribe",
  "llm_provider": "openai",
  "model": "gpt-4.1-mini",
  "system_prompt": "You are a helpful voice assistant. Keep replies brief and conversational.",
  "tts_provider": "openai",
  "tts_voice": "alloy",
  "api_keys": {
    "openai": "YOUR_OPENAI_API_KEY"
  },
  "webrtc_ice_servers": [
    "stun:stun.l.google.com:19302"
  ]
}
```

## 4. LLM / External Service Integration

The repo calls external LLM, STT, TTS, infrastructure, and telephony APIs; no local-model path is described in the wiki. STT providers: OpenAI Whisper (`gpt-4o-mini-transcribe`), Groq, Sarvam (`saarika:v2.5`, Indian languages), ElevenLabs, AWS Transcribe, Google Cloud Speech-to-Text, direct Whisper, Camb, Gradium, Soniox (README.md:111-118). LLM providers: OpenAI (GPT-4.1, GPT-4o), Anthropic Claude (Sonnet, Haiku, Opus), Groq (`llama-3.1-8b-instant`), Google Gemini plus Vertex AI with ADC auth, AWS Bedrock, Mistral, DeepSeek, Cerebras, Grok, Ollama, Qwen, AsyncAI, Fish, Inworld, Minimax, Moondream, OpenPipe (README.md:119-125). TTS providers: OpenAI (`alloy`, `nova`, `shimmer`), ElevenLabs, Sarvam (`bulbul:v2`), Google Cloud TTS, AWS Polly, Groq, Hume, Inworld, Minimax, Neuphonic, XTTS (README.md:126-131). Full capability matrix is in `pkg/services/README.md` (README.md:133).

Required vs optional: at least one STT, one LLM, and one TTS provider key must be set for the configured providers (via `api_keys` map or env); the STT→LLM→TTS calls are required per turn, while MCP tool calls, S3 recording upload, Postgres/MySQL transcript writes, and Daily.co room creation are optional per configuration (README.md:53-60, README.md:348-370, API_SERVER.md:278-317). Telephony (Twilio, Telnyx, Plivo, Exotel, Daily.co rooms plus optional PSTN dial-in) is optional and selected via `runner_transport` (README.md:54, README.md:302).

Env vars (config-file values also settable via env): `VOXRAY_CONFIG` (config path), `VOXRAY_HOST`/`VOXRAY_PORT` (also `HOST`/`PORT`), `VOXRAY_LOG_LEVEL` (`debug|info|warn|error`), `VOXRAY_JSON_LOGS`, `VOXRAY_CORS_ORIGINS`, `VOXRAY_SERVER_API_KEY`, `VOXRAY_MAX_BODY_BYTES`, `VOXRAY_TLS_ENABLE`, `VOXRAY_TLS_CERT_FILE`, `VOXRAY_TLS_KEY_FILE`, `VOXRAY_RECORDING_ENABLE`, `VOXRAY_RECORDING_BUCKET`, `VOXRAY_TRANSCRIPTS_ENABLE`, `VOXRAY_TRANSCRIPTS_DRIVER` (`postgres|mysql`), `VOXRAY_TRANSCRIPTS_DSN`, plus recording/transcripts/session-store vars (README.md:378-392, API_SERVER.md:64-71). The wiki chunk truncates at `VOXRAY_TRANSCRIPTS_DSN` ("Database connec…", README.md:392), so further vars beyond that point are not covered here. `config.example.json` `api_keys` placeholders include `openai`, `deepgram`, `cartesia`, `daily_room_url`, `aws`, `google_cloud_project`, `google_cloud_location`, `aws_region` (config.example.json:436-445). Sarvam live tests additionally require `SARVAM_API_KEY` (TESTING.md:620-623).

## 5. The Session Voice Loop

Primary workflow: establish a session, stream audio through the pipeline, and sink output plus side records. The wiki describes HTTP-level steps; per-function Go signatures are not present in the wiki (only two component pages exist), so each step cites the endpoint/config source instead of a function definition.

1. Configure: copy `config.example.json` to `config.json`, set provider/model/voice fields and `api_keys` (or env equivalents), optionally run `./voxray -init` to scaffold config and directories (README.md:222, README.md:230). Source: `config.example.json` template (config.example.json:365-449).
2. Build and start: `go build -o voxray ./cmd/voxray` (WebSocket only, no CGO) or `make build-voice` / `CGO_ENABLED=1 go build` for WebRTC + Opus TTS; then `./voxray -config config.json` (README.md:193-254). Config path also settable via `VOXRAY_CONFIG` (README.md:268).
3. Create session: `POST /start` or `POST /api/v1/start` with optional `{ createDailyRoom, enableDefaultIceServers, body }`; returns 201 with `sessionId` plus optional `iceConfig` or `dailyRoom`/`dailyToken`; supports `Idempotency-Key` with 24h TTL (API_SERVER.md:278-317). Auth required only when `server_api_key` is set, via `Authorization: Bearer <key>` or `X-API-Key: <key>` (API_SERVER.md:77-83).
4. Attach transport: browser does `POST /webrtc/offer` (or `/api/v1/webrtc/offer`) with `{ offer: <sdp> }` and receives `{ data: { answer: <sdp> } }` when `transport` is `smallwebrtc` or `both`, or opens `GET /ws`; per-session renegotiation uses `POST /sessions/{id}/api/offer` (API_SERVER.md:240-353).
5. Stream turns: each utterance flows MIC → VAD/turn detection (`turn_detection`, `turn_stop_secs`, `vad_*`) → STT (`stt_provider`/`stt_model`) → LLM (`llm_provider`/`model`, `system_prompt`, optional MCP tools) → TTS (`tts_provider`/`tts_voice`) → transport sink, with barge-in governed by `allow_interruptions`/`interruption_strategy` (README.md:53-60, README.md:302, config.example.json:365-449).
6. Persist and observe: WAV uploaded to S3 (`recording.*`), messages written to Postgres/MySQL (`transcripts.*`), metrics scraped at `/metrics`, health checked at `/health`/`/ready` (README.md:348-370, API_SERVER.md:159-225).

## 6. Key Files

| File | Lines | What It Does |
| :--- | :--- | :--- |
| README.md | 392 cited (truncated at env table) | Pipeline definition, architecture diagram, features, provider lists, build/run, config reference |
| API_SERVER.md | 359+ cited (truncated past `PATCH /sessions/{id}/api/o…`) | Versioned `/api/v1` + legacy routes, auth, envelopes, endpoint contracts |
| config.example.json | 365-449 cited | Copy-to-`config.json` runtime template: host/port, providers/models, transport, VAD/turn, plugins, CORS, body limit, key placeholders |
| go.mod | not in wiki | Module identity and Go version (wiki only states Go 1.25+ requirement, README.md:141) |
| go.sum | 455-580 cited (truncated) | Pinned hashes for AWS, Google Cloud, protovalidate/cel/expr, envoy, docker, fsnotify trees |
| cmd/voxray | referenced by build commands | Server entry point built by `go build -o voxray ./cmd/voxray` (README.md:193) |
| pkg/services/README.md | referenced | Full STT/LLM/TTS capability matrix (README.md:133) |
| docs/ARCHITECTURE.md | referenced | Detailed pipeline design doc (README.md:101) |
| docs/SYSTEM_ARCHITECTURE.md | referenced | Detailed system design doc (README.md:101) |
| examples/voice/README.md | referenced | Full config-option examples (README.md:370) |
| Makefile | referenced via targets | `build`, `build-voice`, `run`, `test` workflows (README.md:197-254, TESTING.md:602-623) |
| TESTING.md | 602-680 cited | `go test ./...` scopes, tests/ layout, Sarvam skip rule, CI example |
| .gitignore | 9-51 cited | Excludes binaries, coverage, vendor, IDE files, local configs/secrets |
| NOTICE | 585-595 cited | Voxray-AI 2026 copyright, Apache-2.0 notice |
| config.json | gitignored, scaffolded | Local runtime config (excluded via `/config.json`, `*.local.json`, `.env`, README.md:230) |

Note: only the first three rows plus TESTING/NOTICE/.gitignore content are excerpted in the wiki; the remainder are referenced-but-not-excerpted, and internal `pkg/` source files are not covered by the current two-page wiki.

## 7. Dependencies

The wiki excerpts `go.sum` hashes but not `go.mod` constraint strings, so exact version constraints are not available from the wiki; the table below lists the pinned module trees visible in the excerpt plus the runtime requirements stated elsewhere. All are required for the build except where noted optional.

| Package | Version constraint | Purpose |
| :--- | :--- | :--- |
| Go toolchain | `1.25+` (README.md:141) | Only hard dependency for default WebSocket build |
| gcc + CGO | on PATH (README.md:147) | Required for WebRTC + Opus TTS audio; without it, WebRTC TTS 503s |
| github.com/aws/aws-sdk-go-v2 (+ bedrockruntime, polly, s3, transcribestreaming, config) | pinned in go.sum (hash only, go.sum:455-577) | Bedrock LLM, Polly TTS, Transcribe STT, S3 recording upload |
| cloud.google.com/go (+ speech, texttospeech) | pinned in go.sum (hash only) | Cloud Speech-to-Text, Cloud TTS, Gemini/Vertex LLM |
| buf.build/go/protovalidate, cel.dev/expr | pinned in go.sum (hash only) | Request validation / expression evaluation |
| github.com/envoyproxy/go-control-plane | pinned in go.sum (hash only) | Transitive (envoy/proxy config types) |
| github.com/fsnotify/fsnotify | pinned in go.sum (hash only) | File/config watching |
| github.com/gammazero/deque | pinned in go.sum (hash only; excerpt truncated after this line) | In-memory deque (truncation noted at 02-top-level-files.md:578-579) |
| STT/LLM/TTS provider APIs (OpenAI, Groq, Sarvam, ElevenLabs, Anthropic, Google, AWS, Mistral, DeepSeek, Cerebras, xAI Grok, Ollama, Qwen, Hume, Neuphonic, Minimax, Inworld, Cartesia, Deepgram, Soniox, Camb, Gradium, Whisper, XTTS, Moondream, OpenPipe, AsyncAI, Fish) | API keys via `api_keys`/env (README.md:111-131) | Per-turn transcription, completion, synthesis; at least the configured triple required |
| S3 bucket | `recording.bucket` (README.md:348) | Optional WAV session-recording sink |
| Postgres / MySQL | `transcripts.driver` + `dsn` (README.md:362) | Optional transcript sink |
| Redis session store | checked by `/ready` (API_SERVER.md:186-209) | Optional session state; readiness 503 on ping failure |
| Prometheus | scrape `/metrics` (API_SERVER.md:215-225) | Optional observability (204 when disabled) |

## 8. CLI / Usage Surface

Entry point is the `voxray` binary built from `./cmd/voxray` (README.md:193).

| Command | Effect |
| :--- | :--- |
| `go build -o voxray ./cmd/voxray` / `make build` | WebSocket-only build, no CGO (README.md:193, TESTING.md:602-623) |
| `make build-voice` / `CGO_ENABLED=1 go build -o voxray ./cmd/voxray` | Build with WebRTC + Opus TTS (README.md:204-214) |
| `cp config.example.json config.json` | Create local runtime config (README.md:222) |
| `./voxray -init` | Scaffold config and required directories (README.md:230) |
| `./voxray -config config.json` / `make run-voice ARGS="-config config.json"` | Run server (README.md:242-254) |
| `go run ./cmd/voxray` / `make run` | Dev run (TESTING.md:602-623) |
| `make test` / `go test ./...` | Full suite incl. `tests/` tree (TESTING.md:602-623) |
| `go test ./tests/pkg/...` / `./tests/integration/...` / `./tests/e2e/...` | Scoped suites (TESTING.md:602-623) |

HTTP surface (auth only when `server_api_key` set; `Authorization: Bearer` or `X-API-Key`, else 401 `UNAUTHORIZED`): `GET /health`, `GET /ready`, `GET /metrics`, `GET /swagger/` + `/swagger/doc.json`, `POST /start`, `POST /webrtc/offer`, `POST /sessions/{id}/api/offer`, `PATCH /sessions/{id}/api/o…` (truncated), each with a versioned `/api/v1` twin and legacy-path compatibility; WebSocket `GET /ws` (API_SERVER.md:64-360). Success envelope `{ data, meta: { requestId } }`; error envelope `{ error: { code, message, requestId, details[] } }`; default 256 KB body cap via `max_request_body_bytes` (API_SERVER.md:91-97).

| Env var | Purpose |
| :--- | :--- |
| `VOXRAY_CONFIG` | Config file path (README.md:382) |
| `VOXRAY_HOST` / `VOXRAY_PORT` (or `HOST`/`PORT`) | Bind address (README.md:383, API_SERVER.md:64-71) |
| `VOXRAY_LOG_LEVEL` | `debug|info|warn|error` (README.md:384) |
| `VOXRAY_JSON_LOGS` | Structured JSON logs (README.md:385) |
| `VOXRAY_CORS_ORIGINS` | Allowed CORS origins (README.md:386) |
| `VOXRAY_SERVER_API_KEY` | Static API-key auth gate (README.md:387) |
| `VOXRAY_MAX_BODY_BYTES` | Body cap override, default 256 KB (API_SERVER.md:91-97) |
| `VOXRAY_TLS_ENABLE` / `VOXRAY_TLS_CERT_FILE` / `VOXRAY_TLS_KEY_FILE` | TLS (API_SERVER.md:64-71) |
| `VOXRAY_RECORDING_ENABLE` / `VOXRAY_RECORDING_BUCKET` | S3 recording toggle + bucket (README.md:388-389) |
| `VOXRAY_TRANSCRIPTS_ENABLE` / `VOXRAY_TRANSCRIPTS_DRIVER` / `VOXRAY_TRANSCRIPTS_DSN` | Transcript sink toggle, `postgres|mysql`, DSN (README.md:390-392) |
| `SARVAM_API_KEY` | Enables live Sarvam tests (TESTING.md:620-623) |

Core config keys: `transport`, `host`, `port`, `stt_provider`, `stt_model`, `stt_language`, `llm_provider`/`provider`, `model`, `system_prompt`, `tts_provider`, `tts_model`, `tts_voice`, `api_keys`, `webrtc_ice_servers`, `turn_detection`, `turn_stop_secs`, `turn_*`, `vad_*`, `allow_interruptions`, `interruption_strategy`, `min_words`, `plugins`, `plugin_options`, `cors_allowed_origins`, `max_request_body_bytes`, `server_api_key`, `recording.*`, `transcripts.*`, `rtc_max_duration_secs`, `user_turn_stop_timeout_secs`, `user_idle_timeout_secs` (README.md:302, config.example.json:365-449).

## 9. Extensibility Points

- **New STT/LLM/TTS provider**: change one field in `config.json` for supported providers; for an unsupported one extend the provider registry documented in `pkg/services/README.md` and add its key under `api_keys` (README.md:99, README.md:133, config.example.json:436-445).
- **Custom pipeline processors/aggregators**: use the plugin system — set `plugins` (e.g. `["echo"]`) and the matching `plugin_options` block (`frame_filter`, `wake_check_filter`, `stt_mute_filter`, `audio_filter`, `interruption_controller`, `external_chain`, `rtvi`) in `config.example.json:386-418`; frame filtering composes on `TextFrame`/`TranscriptionFrame` types.
- **Interruption behavior**: tune `allow_interruptions`, `interruption_strategy` (`keyword`, `min_words`), and `interruption_controller.min_words` without code changes (README.md:302, config.example.json:365-449).
- **Turn/VAD tuning**: adjust `turn_detection` (`energy`/`silence`/`silero`), `turn_stop_secs`, `turn_pre_speech_ms`, `turn_max_duration_secs`, `vad_type`, `vad_threshold`, `vad_min_volume`, `vad_confidence`, `vad_start_secs*`, `vad_stop_secs` per microphone conditions (config.example.json:365-449; `_comment_turn_vad` guidance).
- **External chain offload**: point `plugin_options.external_chain` at an HTTP chain (`url`, `stream`, `timeout_sec`, `transcript_key`) to insert custom logic without forking the server (config.example.json:386-418).
- **Transports and telephony**: switch `transport` (`websocket`/`smallwebrtc`/`both`) and `runner_transport` (`webrtc`/`daily`/`twilio`/`telnyx`/`plivo`/`exotel`) plus `webrtc_ice_servers` for new networks (README.md:302).
- **Ops extensions**: add S3 recording targets, Postgres/MySQL transcript tables, Prometheus scrapes, and CORS/TLS settings via config + env (README.md:348-391, API_SERVER.md:64-71).

## 10. Limitations and Gotchas

- **WebRTC build requires CGO and gcc, and fails closed at runtime**: without `CGO_ENABLED=1` and `gcc` on PATH, the binary builds but WebRTC TTS reports *opus encoder unavailable (build without cgo)* and the server returns 503 on WebRTC offers — including a Windows-specific WinLibs/MSYS2 toolchain setup (README.md:147-173).
- **VAD misses quiet or second utterances unless retuned**: the template's own `_comment_turn_vad` warns that when VAD misses speech, the operator must lower `vad_min_volume` (e.g. 0.2) or `vad_threshold`; defaults (`vad_threshold` 0.01, `vad_min_volume` 0.25, `turn_stop_secs` 3.0) are starting points, not universal (config.example.json:365-449).
- **Wiki coverage is partial and truncated**: `API_SERVER.md` cuts off at `PATCH /sessions/{id}/api/o…` (7309 chars missing) and `go.sum` cuts off after `gammazero/deque`, while `README.md` env documentation truncates mid-`VOXRAY_TRANSCRIPTS_DSN`; endpoint, dependency, and env details past those points are unknown from the wiki alone (02-top-level-files.md:358-359, 02-top-level-files.md:578-579, README.md:392).
- **Secrets live next to config with only gitignore as guard**: `config.json`, `*.local.json`, `.env` holding `api_keys` are excluded by `.gitignore` (02-top-level-files.md:6-51), but the documented flow still copies real keys into a local JSON file, so a misconfigured ignore or backup leaks provider keys.
- **Body cap and idempotency defaults are silent**: requests over `max_request_body_bytes` (default 256 KB) are rejected, `POST /start` idempotency keys expire after 24h, and `GET /metrics` returns 204 rather than an error when disabled — all easy to misread as failures (API_SERVER.md:91-97, API_SERVER.md:215-225, API_SERVER.md:278-317).

## 11. How It Compares to Alternatives

The wiki names no alternatives directly; positioning below is inferred from the documented feature set (dual transport, telephony, provider breadth, self-hosting) against well-known voice-agent stacks.

- **LiveKit Agents (Python/Node, LiveKit WebRTC infra)**: full-featured agent framework with managed global SFU transport; Voxray instead embeds SmallWebRTC directly in a single Go binary with no separate media server, trading LiveKit's managed scaling for self-hosted simplicity (cf. README.md:53-57).
- **Pipecat (Daily, Python)**: pipeline-orchestration framework (processors, transports, telephony via Daily) where developers write pipeline code; Voxray instead declares the whole MIC→VAD→STT→LLM→TTS chain in one JSON file with env overrides, trading programmability for zero-code provider swaps (cf. README.md:63, README.md:99).
- **Twilio Voice / native telephony APIs**: carrier-grade PSTN with per-minute pricing and vendor lock-in; Voxray speaks Twilio/Telnyx/Plivo/Exotel as optional `runner_transport` values inside the same server while remaining deployable to a private VPC (cf. README.md:54, README.md:57).
- **Vapi / Retell / managed voice-agent clouds**: hosted STT→LLM→TTS with dashboards and usage billing; Voxray covers the same loop (barge-in, MCP tools, S3 recording, SQL transcripts, Prometheus metrics) as a self-hosted binary with caller-owned API keys, trading a managed console for cost control and data residency (cf. README.md:53-60).

Positioning: Voxray is the self-hosted, config-first Go server for teams that want a single-binary WebSocket/WebRTC voice pipeline with wide provider choice and telephony reach, rather than a code framework or a managed cloud.

## Appendix: Selected Code Snippets

1. Minimal runtime config (README.md:274, via 01-overview.md:112-132):

```json
{
  "transport": "both",
  "host": "0.0.0.0",
  "port": 8080,
  "stt_provider": "openai",
  "stt_model": "gpt-4o-mini-transcribe",
  "llm_provider": "openai",
  "model": "gpt-4.1-mini",
  "system_prompt": "You are a helpful voice assistant. Keep replies brief and conversational.",
  "tts_provider": "openai",
  "tts_voice": "alloy",
  "api_keys": {
    "openai": "YOUR_OPENAI_API_KEY"
  },
  "webrtc_ice_servers": [
    "stun:stun.l.google.com:19302"
  ]
}
```

2. Provider swap to Sarvam + Groq (README.md:325, via 01-overview.md:150-164):

```json
{
  "stt_provider": "sarvam",
  "stt_model": "saarika:v2.5",
  "llm_provider": "groq",
  "model": "llama-3.1-8b-instant",
  "tts_provider": "sarvam",
  "tts_voice": "bulbul:v2",
  "api_keys": {
    "sarvam": "YOUR_SARVAM_KEY",
    "groq": "YOUR_GROQ_KEY"
  }
}
```

3. Build and run (README.md:180-254, via 01-overview.md:97-110):

```bash
git clone https://github.com/Voxray-AI/Voxray.git
cd Voxray
go build -o voxray ./cmd/voxray  # WebSocket only, no CGO
# or:
make build
make build-voice  # Linux/macOS, with WebRTC + Opus TTS
CGO_ENABLED=1 go build -o voxray ./cmd/voxray  # manual, any OS
cp config.example.json config.json
./voxray -init  # scaffold config and required directories
./voxray -config config.json
make run-voice ARGS="-config config.json"  # Linux/macOS one-step build+run
```

4. Recording and transcript sinks (README.md:348-370, via 01-overview.md:165-183):

```json
"recording": {
  "enable": true,
  "bucket": "your-recordings-bucket",
  "base_path": "recordings/",
  "format": "wav",
  "worker_count": 4
}
```

```json
"transcripts": {
  "enable": true,
  "driver": "postgres",
  "dsn": "postgres://user:pass@localhost:5432/voxray?sslmode=disable",
  "table_name": "call_transcripts"
}
```
