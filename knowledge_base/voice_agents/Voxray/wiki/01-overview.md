[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** Voxray is a config-driven Go server that wires STT → LLM → TTS providers into a single low-latency streaming voice pipeline delivered over WebSocket or WebRTC.
## Key points
- Voxray is a config-driven Go server for production-ready real-time voice AI agents wiring STT → LLM → TTS into one low-latency streaming pipeline over WebSocket or WebRTC (README.md:31).
- The per-session pipeline runs MIC → VAD → STT → LLM → TTS → Transport Sink inside the Voxray server, fronted by an HTTP server with `/ws`, `/webrtc/offer`, `/start`, `/metrics`, `/swagger/` (README.md:87).
- Transport is dual: WebSocket (`/ws`) and WebRTC via SmallWebRTC (`/webrtc/offer`), switchable at runtime, plus telephony via Twilio, Telnyx, Plivo, Exotel, and Daily.co (README.md:54).
- Provider coverage is wide out of the box: 10+ STT, 20+ LLM, and 15+ TTS providers, swapped by changing a single field in `config.json` (README.md:56).
- The whole agent is defined by one JSON file covering providers, models, voices, turn detection, recording, and more, with env-var overrides for every value (README.md:63).
- Go 1.25+ is the only hard dependency for the default WebSocket build, while WebRTC + Opus TTS audio additionally requires CGO and `gcc` on PATH (README.md:141).
- Barge-in/interruption is a configurable strategy so users can cut the agent mid-sentence, alongside MCP tool calls, S3 WAV recording, Postgres/MySQL transcripts, Prometheus `/metrics`, and a plugin system (README.md:57).
---
## What is Voxray
Voxray is a **config-driven Go server** for building production-ready **real-time voice AI agents** (README.md:31):
> It wires together **STT → LLM → TTS** providers into a single low-latency streaming pipeline delivered over **WebSocket** or **WebRTC** — no audio plumbing required. (README.md:31)
> Define your pipeline in a single JSON file, point it at any combination of speech and language providers, and ship a voice agent to production in under 5 minutes. (README.md:33)
Demo pipeline shown in the console (README.md:45):
> *Pipeline shown: MIC (48 kHz · Opus) → VAD (Energy) → STT (Sarvam · saarika:v2.5) → LLM (Groq · llama-3.1-8b-instant) → TTS (Sarvam · bulbul:v2) → OUT (WebRTC peer)*
## Architecture
Audio enters from a browser, native client, or telephony provider, passes through a configurable processing chain, and streams back to the caller (README.md:72). Verbatim diagram (README.md:74):
```
┌─────────────────────────────────────────────────────────────────────┐
│                            CLIENT                                   │
│          Browser / Mobile app / Telephony / Daily.co                │
└─────────────┬───────────────────────────────────────┬───────────────┘
               │  WebSocket / WebRTC / Telephony WS     │
               ▼                                         ▲
┌─────────────────────────────────────────────────────────────────────┐
│                         VOXRAY SERVER                               │
│   HTTP server — /ws  /webrtc/offer  /start  /metrics  /swagger/    │
│                                                                     │
│  ┌───────┐    ┌──────────────────────────────────────────────────┐  │
│  │Runner │───▶│           PIPELINE (per session)                 │  │
│  └───────┘    │  MIC → VAD → STT → LLM → TTS → Transport Sink   │  │
│               └──────┬──────────┬──────────┬─────────────────────┘  │
└──────────────────────┼──────────┼──────────┼────────────────────────┘
                        ▼          ▼          ▼
                ┌──────────┐ ┌─────────┐ ┌─────────┐
                │ STT API  │ │ LLM API │ │ TTS API │
                │(Sarvam,  │ │(OpenAI, │ │(ElevenL,│
                │ OpenAI,  │ │ Groq,   │ │ Sarvam, │
                │ Groq...) │ │ Claude…)│ │ Google…)│
                └──────────┘ └─────────┘ └─────────┘
```
Each stage is independently pluggable (README.md:99):
> Swap any provider by changing a single field in `config.json`.
Detailed design docs: `docs/ARCHITECTURE.md` and `docs/SYSTEM_ARCHITECTURE.md` (README.md:101).
## Features
Verbatim feature list (README.md:53):
- **End-to-end voice pipeline** — MIC → VAD → STT → LLM → TTS → speaker, fully streamed and low-latency
- **Dual transport** — WebSocket (`/ws`) and WebRTC via SmallWebRTC (`/webrtc/offer`); switchable at runtime
- **Telephony support** — Twilio, Telnyx, Plivo, Exotel, and Daily.co (rooms + optional PSTN dial-in)
- **Wide provider coverage** — 10+ STT, 20+ LLM, and 15+ TTS providers out of the box
- **MCP tool integration** — LLM can call external tools via a configurable MCP server
- **Barge-in / interruption** — configurable interruption strategy so users can cut the agent mid-sentence
- **Conversation recording** — mixed-audio WAV per session, uploaded asynchronously to S3
- **Transcript logging** — per-message text persisted to Postgres or MySQL
- **Observability** — Prometheus metrics at `/metrics`, structured JSON logs, configurable log level
- **Plugin system** — extend the pipeline with custom processors and aggregators
- **Config-driven** — one JSON file to define providers, models, voices, turn detection, recording, and more
- **Self-hostable** — no vendor lock-in; deploy to your own infra or VPC
## Supported providers
Full capability matrix: `pkg/services/README.md` (README.md:133).
| Stage | Provider | Notes |
| :------ | :-------------- | :---------------------------------------------- |
| **STT** | OpenAI | Whisper (`gpt-4o-mini-transcribe`, etc.) (README.md:111) |
| | Groq | (README.md:112) |
| | Sarvam | Indian languages (`saarika:v2.5`) (README.md:113) |
| | ElevenLabs | (README.md:114) |
| | AWS | Amazon Transcribe (README.md:115) |
| | Google | Cloud Speech-to-Text (README.md:116) |
| | Whisper | Direct Whisper integration (README.md:117) |
| | Camb / Gradium / Soniox | (README.md:118) |
| **LLM** | OpenAI | GPT-4.1, GPT-4o, etc. (README.md:119) |
| | Anthropic | Claude (Sonnet, Haiku, Opus) (README.md:120) |
| | Groq | llama-3.1-8b-instant, etc. (README.md:121) |
| | Google | Gemini (+ Vertex AI with ADC auth) (README.md:122) |
| | AWS | Amazon Bedrock (README.md:123) |
| | Mistral / DeepSeek / Cerebras / Grok / Ollama / Qwen | (README.md:124) |
| | AsyncAI / Fish / Inworld / Minimax / Moondream / OpenPipe | (README.md:125) |
| **TTS** | OpenAI | `alloy`, `nova`, `shimmer`, etc. (README.md:126) |
| | ElevenLabs | (README.md:127) |
| | Sarvam | Indian languages (`bulbul:v2`) (README.md:128) |
| | Google | Cloud Text-to-Speech (README.md:129) |
| | AWS | Amazon Polly (README.md:130) |
| | Groq / Hume / Inworld / Minimax / Neuphonic / XTTS | (README.md:131) |
## Requirements and build
**Go 1.25+** is the only hard dependency for the default WebSocket build (README.md:141):
```bash
go version   # 1.25+ required (README.md:144)
```
For **WebRTC + Opus TTS audio**, CGO and `gcc` must be on PATH (README.md:147):
```bash
gcc --version (README.md:150)
```
Windows gcc options: WinLibs via `winget install BrechtSanders.WinLibs.POSIX.UCRT` (README.md:159) or MSYS2 UCRT64 with `pacman -S mingw-w64-ucrt-x86_64-toolchain` plus `C:\msys64\ucrt64\bin` on PATH (README.md:168). Without CGO, WebRTC TTS reports *opus encoder unavailable (build without cgo)* and the server returns **503** on WebRTC offers (README.md:173).
Build and run steps (README.md:180):
```bash
git clone https://github.com/Voxray-AI/Voxray.git
cd Voxray (README.md:182)
go build -o voxray ./cmd/voxray  # WebSocket only, no CGO (README.md:193)
# or:
make build (README.md:197)
make build-voice  # Linux/macOS, with WebRTC + Opus TTS (README.md:204)
CGO_ENABLED=1 go build -o voxray ./cmd/voxray  # manual, any OS (README.md:214)
cp config.example.json config.json (README.md:222)
./voxray -init  # scaffold config and required directories (README.md:230)
./voxray -config config.json (README.md:242)
make run-voice ARGS="-config config.json"  # Linux/macOS one-step build+run (README.md:254)
```
## Configuration
Config path is set with `-config` or the `VOXRAY_CONFIG` environment variable (README.md:268). Minimal config, verbatim (README.md:274):
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
Key config options (README.md:302):
| Key | Type | Default | Description |
| :-- | :--- | :------ | :---------- |
| `transport` | string | `"websocket"` | `"websocket"`, `"smallwebrtc"`, or `"both"` |
| `host` / `port` | string / int | `"0.0.0.0"` / `8080` | Bind address |
| `stt_provider` | string | — | STT provider (`"openai"`, `"sarvam"`, `"groq"`, …) |
| `stt_model` | string | — | STT model name |
| `llm_provider` | string | — | LLM provider (`"openai"`, `"anthropic"`, `"groq"`, …) |
| `model` | string | — | LLM model name |
| `system_prompt` | string | — | System prompt for the LLM |
| `tts_provider` | string | — | TTS provider (`"openai"`, `"elevenlabs"`, `"sarvam"`, …) |
| `tts_voice` | string | — | Voice name / ID |
| `api_keys` | object | — | Map of `provider → API key` |
| `turn_detection` | string | `"energy"` | VAD mode (`"energy"`, `"silero"`) |
| `allow_interruptions` | bool | `true` | Enable barge-in |
| `metrics_enabled` | bool | `true` | Expose `/metrics` |
| `runner_transport` | string | `""` | `"webrtc"`, `"daily"`, `"twilio"`, `"telnyx"`, `"plivo"`, `"exotel"` |
Swapping providers example, verbatim (README.md:325):
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
Recording (S3), verbatim (README.md:348):
```json
"recording": {
  "enable": true,
  "bucket": "your-recordings-bucket",
  "base_path": "recordings/",
  "format": "wav",
  "worker_count": 4
}
```
Transcript logging (Postgres / MySQL), verbatim (README.md:362):
```json
"transcripts": {
  "enable": true,
  "driver": "postgres",
  "dsn": "postgres://user:pass@localhost:5432/voxray?sslmode=disable",
  "table_name": "call_transcripts"
}
```
See `config.example.json` and `examples/voice/README.md` for all options (README.md:370).
## Environment variables
All config values can be overridden via environment variables (README.md:378).
| Variable | Description |
| :------- | :---------- |
| `VOXRAY_CONFIG` | Path to config file (README.md:382) |
| `VOXRAY_HOST` / `VOXRAY_PORT` | Bind host / port (README.md:383) |
| `VOXRAY_LOG_LEVEL` | `debug`, `info`, `warn`, `error` (README.md:384) |
| `VOXRAY_JSON_LOGS` | `true` for structured JSON logs (README.md:385) |
| `VOXRAY_CORS_ORIGINS` | Comma-separated allowed CORS origins (README.md:386) |
| `VOXRAY_SERVER_API_KEY` | Enable server-level API key auth (README.md:387) |
| `VOXRAY_RECORDING_ENABLE` | `true` to enable S3 recording (README.md:388) |
| `VOXRAY_RECORDING_BUCKET` | S3 bucket name (README.md:389) |
| `VOXRAY_TRANSCRIPTS_ENABLE` | `true` to enable transcript logging (README.md:390) |
| `VOXRAY_TRANSCRIPTS_DRIVER` | `postgres` or `mysql` (README.md:391) |
| `VOXRAY_TRANSCRIPTS_DSN` | Description truncated in chunk at "Database connec" — content beyond this point not present (README.md:392) |
**Covers:** README.md (project overview, pipeline, features, architecture, providers, requirements/build, configuration, environment variables)
