# Voxray-AI/Voxray
Source: https://github.com/Voxray-AI/Voxray
Kind: repo
Fetched: 2026-09-22T14:53:52.356874+00:00
Tool: git-clone
PDF: https://github.com/Voxray-AI/Voxray

# Voxray-AI/Voxray

Commit: 4747b666177a0ae9f05fe276ba6671202628e270

## README

# Voxray

<div align="center">

[![Go](https://img.shields.io/badge/Go-1.25+-00ADD8?logo=go&logoColor=white)](https://go.dev/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Go Reference](https://pkg.go.dev/badge/github.com/Voxray-AI/Voxray.svg)](https://pkg.go.dev/github.com/Voxray-AI/Voxray)
[![Go Report Card](https://goreportcard.com/badge/github.com/Voxray-AI/Voxray)](https://goreportcard.com/report/github.com/Voxray-AI/Voxray)
[![codecov](https://codecov.io/gh/Voxray-AI/Voxray/branch/main/graph/badge.svg)](https://codecov.io/gh/Voxray-AI/Voxray)
[![Docs](https://img.shields.io/badge/docs-online-blue)](https://voxray-cac3ed72.mintlify.app/get-started/introduction)
[![Version](https://img.shields.io/badge/version-v0.2.0-green)](https://github.com/Voxray-AI/Voxray/releases)

**Real-time voice agent platform. Build and deploy speech-to-speech AI in minutes.**

[Quick Start](#quick-start) · [Features](#features) · [Docs](https://voxray-cac3ed72.mintlify.app/get-started/introduction) · [Roadmap](#roadmap) · [Contributing](#contributing)

</div>

---



## What is Voxray?

Voxray is a **config-driven Go server** for building production-ready **real-time voice AI agents**. It wires together **STT → LLM → TTS** providers into a single low-latency streaming pipeline delivered over **WebSocket** or **WebRTC** — no audio plumbing required.

Define your pipeline in a single JSON file, point it at any combination of speech and language providers, and ship a voice agent to production in under 5 minutes.

---



## Demo

> The Voxray web console shows a live pipeline visualization with real-time audio waveform, transport toggle (WebRTC / WebSocket), and stage-by-stage status indicators.

![Voxray Console — real-time voice pipeline](docs/assets/console-demo.png)

*Pipeline shown: MIC (48 kHz · Opus) → VAD (Energy) → STT (Sarvam · saarika:v2.5) → LLM (Groq · llama-3.1-8b-instant) → TTS (Sarvam · bulbul:v2) → OUT (WebRTC peer)*

---



## Features

- **End-to-end voice pipeline** — MIC → VAD → STT → LLM → TTS → speaker, fully streamed and low-latency
- **Dual transport** — WebSocket (`/ws`) and WebRTC via SmallWebRTC (`/webrtc/offer`); switchable at runtime
- **Telephony support** — Twilio, Telnyx, Plivo, Exotel, and Daily.co (rooms + optional PSTN dial-in)
- **Wide provider coverage** — 10+ STT, 20+ LLM, and 15+ TTS providers out of the box (see [Supported Providers](#supported-providers))
- **MCP tool integration** — LLM can call external tools via a configurable MCP server
- **Barge-in / interruption** — configurable interruption strategy so users can cut the agent mid-sentence
- **Conversation recording** — mixed-audio WAV per session, uploaded asynchronously to S3
- **Transcript logging** — per-message text persisted to Postgres or MySQL
- **Observability** — Prometheus metrics at `/metrics`, structured JSON logs, configurable log level
- **Plugin system** — extend the pipeline with custom processors and aggregators
- **Config-driven** — one JSON file to define providers, models, voices, turn detection, recording, and more
- **Self-hostable** — no vendor lock-in; deploy to your own infra or VPC

---



## Architecture

Audio enters from a browser, native client, or telephony provider, passes through a configurable processing chain, and streams back to the caller — all within a single low-latency pipeline.

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

Each stage is independently pluggable. Swap any provider by changing a single field in `config.json`.

For detailed design docs, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) and [docs/SYSTEM_ARCHITECTURE.md](docs/SYSTEM_ARCHITECTURE.md).

---



## Supported Providers

| Stage   | Provider        | Notes                                           |
| :------ | :-------------- | :---------------------------------------------- |
| **STT** | OpenAI          | Whisper (`gpt-4o-mini-transcribe`, etc.)        |
|         | Groq            |                                                 |
|         | Sarvam          | Indian languages (`saarika:v2.5`)               |
|         | ElevenLabs      |                                                 |
|         | AWS             | Amazon Transcribe                               |
|         | Google          | Cloud Speech-to-Text                            |
|         | Whisper         | Direct Whisper integration                      |
|         | Camb / Gradium / Soniox |                                         |
| **LLM** | OpenAI          | GPT-4.1, GPT-4o, etc.                          |
|         | Anthropic       | Claude (Sonnet, Haiku, Opus)                    |
|         | Groq            | llama-3.1-8b-instant, etc.                     |
|         | Google          | Gemini (+ Vertex AI with ADC auth)              |
|         | AWS             | Amazon Bedrock                                  |
|         | Mistral / DeepSeek / Cerebras / Grok / Ollama / Qwen | |
|         | AsyncAI / Fish / Inworld / Minimax / Moondream / OpenPipe | |
| **TTS** | OpenAI          | `alloy`, `nova`, `shimmer`, etc.                |
|         | ElevenLabs      |                                                 |
|         | Sarvam          | Indian languages (`bulbul:v2`)                  |
|         | Google          | Cloud Text-to-Speech                            |
|         | AWS             | Amazon Polly                                    |
|         | Groq / Hume / Inworld / Minimax / Neuphonic / XTTS | |

Full capability matrix: [pkg/services/README.md](pkg/services/README.md)

---



## Requirements

**Go 1.25+** is the only hard dependency for the default WebSocket build.

```bash
go version   # 1.25+ required
```

For **WebRTC + Opus TTS audio**, CGO and `gcc` must be on your PATH:

```bash
gcc --version
```



### Installing gcc on Windows

**Option A — WinLibs (winget):**
```powershell
winget install BrechtSanders.WinLibs.POSIX.UCRT --accept-package-agreements


# Restart terminal, then verify:
gcc --version
```

**Option B — MSYS2:**
Install [MSYS2](https://www.msys2.org/), open MSYS2 UCRT64, then:
```bash
pacman -S mingw-w64-ucrt-x86_64-toolchain
```
Add `C:\msys64\ucrt64\bin` to PATH and verify with `gcc --version`.

> Without CGO, WebRTC TTS reports *opus encoder unavailable (build without cgo)* and the server returns **503** on WebRTC offers.


---



### 1. Clone

```bash
git clone https://github.com/Voxray-AI/Voxray.git
cd Voxray
```



### 2. Build

**WebSocket only (no CGO required):**
```bash
go build -o voxray ./cmd/voxray


# or:
make build
```

**With WebRTC + Opus TTS (CGO required):**

Linux / macOS:
```bash
make build-voice
```

Windows (PowerShell):
```powershell
.\scripts\build-voice.ps1
```

Manual (any OS):
```bash
CGO_ENABLED=1 go build -o voxray ./cmd/voxray
```



### 3. Configure

```bash
cp config.example.json config.json


# Edit config.json — fill in your API keys and choose providers
```

Or use `-init` to scaffold the config and required directories:
```bash
./voxray -init


# Windows:
.\voxray.exe -init
```



### 4. Run

```bash
./voxray -config config.json


# Windows:
.\voxray.exe -config config.json
```

One-step build and run with voice:
```bash


# Linux / macOS:
make run-voice ARGS="-config config.json"



# Windows:
.\scripts\run-voice.ps1 -config config.json
```

---



## Configuration

Set the config path with `-config` or the `VOXRAY_CONFIG` environment variable.



### Minimal config

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



### Key config options

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



### Swapping providers (example)

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



### Recording (S3)

```json
"recording": {
  "enable": true,
  "bucket": "your-recordings-bucket",
  "base_path": "recordings/",
  "format": "wav",
  "worker_count": 4
}
```



### Transcript logging (Postgres / MySQL)

```json
"transcripts": {
  "enable": true,
  "driver": "postgres",
  "dsn": "postgres://user:pass@localhost:5432/voxray?sslmode=disable",
  "table_name": "call_transcripts"
}
```

See [config.example.json](config.example.json) and [examples/voice/README.md](examples/voice/README.md) for all options.

---



## Environment Variables

All config values can be overridden via environment variables.

| Variable | Description |
| :------- | :---------- |
| `VOXRAY_CONFIG` | Path to config file |
| `VOXRAY_HOST` / `VOXRAY_PORT` | Bind host / port |
| `VOXRAY_LOG_LEVEL` | `debug`, `info`, `warn`, `error` |
| `VOXRAY_JSON_LOGS` | `true` for structured JSON logs |
| `VOXRAY_CORS_ORIGINS` | Comma-separated allowed CORS origins |
| `VOXRAY_SERVER_API_KEY` | Enable server-level API key auth |
| `VOXRAY_RECORDING_ENABLE` | `true` to enable S3 recording |
| `VOXRAY_RECORDING_BUCKET` | S3 bucket name |
| `VOXRAY_TRANSCRIPTS_ENABLE` | `true` to enable transcript logging |
| `VOXRAY_TRANSCRIPTS_DRIVER` | `postgres` or `mysql` |
| `VOXRAY_TRANSCRIPTS_DSN` | Database connec

... (truncated, 6566 more characters)

## go.mod

```
module github.com/Voxray-AI/Voxray

go 1.25.0

require (
	cloud.google.com/go/speech v1.30.0
	cloud.google.com/go/texttospeech v1.16.0
	github.com/aws/aws-sdk-go-v2 v1.41.2
	github.com/aws/aws-sdk-go-v2/config v1.32.10
	github.com/aws/aws-sdk-go-v2/service/bedrockruntime v1.50.0
	github.com/aws/aws-sdk-go-v2/service/polly v1.54.11
	github.com/aws/aws-sdk-go-v2/service/s3 v1.71.0
	github.com/aws/aws-sdk-go-v2/service/transcribestreaming v1.33.7
	github.com/go-sql-driver/mysql v1.9.3
	github.com/godeps/opus v1.0.3
	github.com/google/uuid v1.6.0
	github.com/gorilla/websocket v1.5.3
	github.com/lib/pq v1.11.2
	github.com/livekit/protocol v1.38.0
	github.com/modelcontextprotocol/go-sdk v1.4.0
	github.com/pion/opus v0.0.0-20260219180131-abe26becac00
	github.com/pion/webrtc/v3 v3.3.6
	github.com/prometheus/client_golang v1.20.5
	github.com/redis/go-redis/v9 v9.18.0
	github.com/sashabaranov/go-openai v1.41.2
	github.com/swaggo/http-swagger v1.3.4
	github.com/swaggo/swag v1.16.3
	google.golang.org/genai v1.48.0
	layeh.com/gopus v0.0.0-20210501142526-1ee02d434e32
)

require (
	buf.build/gen/go/bufbuild/protovalidate/protocolbuffers/go v1.36.6-20250625184727-c923a0c2a132.1 // indirect
	buf.build/go/protovalidate v0.13.1 // indirect
	buf.build/go/protoyaml v0.6.0 // indirect
	cel.dev/expr v0.24.0 // indirect
	cloud.google.com/go v0.123.0 // indirect
	cloud.google.com/go/auth v0.18.1 // indirect
	cloud.google.com/go/auth/oauth2adapt v0.2.8 // indirect
	cloud.google.com/go/compute/metadata v0.9.0 // indirect
	cloud.google.com/go/longrunning v0.8.0 // indirect
	filippo.io/edwards25519 v1.1.0 // indirect
	github.com/KyleBanks/depth v1.2.1 // indirect
	github.com/antlr4-go/antlr/v4 v4.13.1 // indirect
	github.com/aws/aws-sdk-go-v2/aws/protocol/eventstream v1.7.5 // indirect
	github.com/aws/aws-sdk-go-v2/credentials v1.19.10 // indirect
	github.com/aws/aws-sdk-go-v2/feature/ec2/imds v1.18.18 // indirect
	github.com/aws/aws-sdk-go-v2/internal/configsources v1.4.18 // indirect
	github.com/aws/aws-sdk-go-v2/internal/endpoints/v2 v2.7.18 // indirect
	github.com/aws/aws-sdk-go-v2/internal/ini v1.8.4 // indirect
	github.com/aws/aws-sdk-go-v2/internal/v4a v1.3.25 // indirect
	github.com/aws/aws-sdk-go-v2/service/internal/accept-encoding v1.13.5 // indirect
	github.com/aws/aws-sdk-go-v2/service/internal/checksum v1.4.6 // indirect
	github.com/aws/aws-sdk-go-v2/service/internal/presigned-url v1.13.18 // indirect
	github.com/aws/aws-sdk-go-v2/service/internal/s3shared v1.18.6 // indirect
	github.com/aws/aws-sdk-go-v2/service/signin v1.0.6 // indirect
	github.com/aws/aws-sdk-go-v2/service/sso v1.30.11 // indirect
	github.com/aws/aws-sdk-go-v2/service/ssooidc v1.35.15 // indirect
	github.com/aws/aws-sdk-go-v2/service/sts v1.41.7 // indirect
	github.com/aws/smithy-go v1.24.1 // indirect
	github.com/benbjohnson/clock v1.3.5 // indirect
	github.com/beorn7/perks v1.0.1 // indirect
	github.com/cespare/xxhash/v2 v2.3.0 // indirect
	github.com/davecgh/go-spew v1.1.1 // indirect
	github.com/dennwc/iters v1.1.0 // indirect
	github.com/dgryski/go-rendezvous v0.0.0-20200823014737-9f7001d12a5f // indirect
	github.com/felixge/httpsnoop v1.0.4 // indirect
	github.com/frostbyte73/core v0.1.1 // indirect
	github.com/fsnotify/fsnotify v1.9.0 // indirect
	github.com/gammazero/deque v1.1.0 // indirect
	github.com/go-jose/go-jose/v3 v3.0.4 // indirect
	github.com/go-logr/logr v1.4.3 // indirect
	github.com/go-logr/stdr v1.2.2 // indirect
	github.com/go-openapi/jsonpointer v0.19.5 // indirect
	github.com/go-openapi/jsonreference v0.20.0 // indirect
	github.com/go-openapi/spec v0.20.6 // indirect
	github.com/go-openapi/swag v0.19.15 // indirect
	github.com/google/cel-go v0.25.0 // indirect
	github.com/google/go-cmp v0.7.0 // indirect
	github.com/google/jsonschema-go v0.4.2 // indirect
	github.com/google/s2a-go v0.1.9 // indirect
	github.com/googleapis/enterprise-certificate-proxy v0.3.11 // indirect
	github.com/googleapis/gax-go/v2 v2.17.0 // indirect
	github.com/josharian/intern v1.0.0 // indirect
	github.com/jxskiss/base62 v1.1.0 // indirect
	github.com/klauspost/compress v1.18.0 // indirect
	github.com/klauspost/cpuid/v2 v2.2.11 // indirect
	github.com/lithammer/shortuuid/v4 v4.2.0 // indirect
	github.com/livekit/mageutil v0.0.0-20250511045019-0f1ff63f7731 // indirect
	github.com/livekit/psrpc v0.7.1 // indirect
	github.com/mailru/easyjson v0.7.6 // indirect
	github.com/munnerz/goautoneg v0.0.0-20191010083416-a7dc8b61c822 // indirect
	github.com/nats-io/nats.go v1.43.0 // indirect
	github.com/nats-io/nkeys v0.4.11 // indirect
	github.com/nats-io/nuid v1.0.1 // indirect
	github.com/pion/datachannel v1.5.10 // indirect
	github.com/pion/dtls/v2 v2.2.12 // indirect
	github.com/pion/dtls/v3 v3.0.6 // indirect
	github.com/pion/ice/v2 v2.3.38 // indirect
	github.com/pion/ice/v4 v4.0.10 // indirect
	github.com/pion/interceptor v0.1.40 // indirect
	github.com/pion/logging v0.2.4 // indirect
	github.com/pion/mdns v0.0.12 // indirect
	github.com/pion/mdns/v2 v2.0.7 // indirect
	github.com/pion/randutil v0.1.0 // indirect
	github.com/pion/rtcp v1.2.15 // indirect
	github.com/pion/rtp v1.8.19 // indirect
	github.com/pion/sctp v1.8.39 // indirect
	github.com/pion/sdp/v3 v3.0.14 // indirect
	github.com/pion/srtp/v2 v2.0.20 // indirect
	github.com/pion/srtp/v3 v3.0.6 // indirect
	github.com/pion/stun v0.6.1 // indirect
	github.com/pion/stun/v3 v3.0.0 // indirect
	github.com/pion/transport/v2 v2.2.10 // indirect
	github.com/pion/transport/v3 v3.0.7 // indirect
	github.com/pion/turn/v2 v2.1.6 // indirect
	github.com/pion/turn/v4 v4.0.2 // indirect
	github.com/pion/webrtc/v4 v4.1.2 // indirect
	github.com/pmezard/go-difflib v1.0.0 // indirect
	github.com/prometheus/client_model v0.6.1 // indirect
	github.com/prometheus/common v0.55.0 // indirect
	github.com/prometheus/procfs v0.15.1 // indirect
	github.com/puzpuzpuz/xsync/v3 v3.5.1 // indirect
	github.com/segmentio/asm v1.1.3 // indirect
	github.com/segmentio/encoding v0.5.3 // indirect
	github.com/stoewer/go-strcase v1.3.1 // indirect
	github.com/stretchr/testify v1.11.1 // indirect
	github.com/swaggo/files v0.0.0-20220610200504-28940afbdbfe // indirect
	github.com/tetratelabs/wazero v1.9.0 // indirect
	github.com/twitchtv/twirp v8.1.3+incompatible // indirect
	github.com/wlynxg/anet v0.0.5 // indirect
	github.com/yosida95/uritemplate/v3 v3.0.2 // indirect
	github.com/zeebo/xxh3 v1.0.2 // indirect
	go.opentelemetry.io/auto/sdk v1.2.1 // indirect
	go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc v0.61.0 // indirect
	go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp v0.61.0 // indirect
	go.opentelemetry.io/otel v1.39.0 // indirect
	go.opentelemetry.io/otel/metric v1.39.0 // indirect
	go.opentelemetry.io/otel/trace v1.39.0 // indirect
	go.uber.org/atomic v1.11.0 // indirect
	go.uber.org/multierr v1.11.0 // indirect
	go.uber.org/zap v1.27.0 // indirect
	go.uber.org/zap/exp v0.3.0 // indirect
	golang.org/x/crypto v0.47.0 // indirect
	golang.org/x/exp v0.0.0-20250620022241-b7579e27df2b // indirect
	golang.org/x/net v0.49.0 // indirect
	golang.org/x/oauth2 v0.34.0 // indirect
	golang.org/x/sync v0.19.0 // indirect
	golang.org/x/sys v0.40.0 // indirect
	golang.org/x/text v0.33.0 // indirect
	golang.org/x/time v0.14.0 // indirect
	golang.org/x/tools v0.41.0 // indirect
	google.golang.org/api v0.265.0 // indirect
	google.golang.org/genproto v0.0.0-20260128011058-8636f8732409 // indirect
	google.golang.org/genproto/googleapis/api v0.0.0-20260203192932-546029d2fa20 // indirect
	google.golang.org/genproto/googleapis/rpc v0.0.0-20260203192932-546029d2fa20 // indirect
	google.golang.org/grpc v1.78.0 // indirect
	google.golang.org/protobuf v1.36.11 // indirect
	gopkg.in/yaml.v2 v2.4.0 // indirect
	gopkg.in/yaml.v3 v3.0.1 // indirect
)

```

## Top-level layout

- .github/ (dir, 1 files, ~43 lines)
- .gitignore (~42 lines)
- API_SERVER.md (~468 lines)
- build/ (dir, 17 files, ~1049 lines)
- cmd/ (dir, 5 files, ~750 lines)
- config.example.json (~85 lines)
- contributing/ (dir, 3 files, ~286 lines)
- CONTRIBUTING.md (~515 lines)
- core-concepts/ (dir, 6 files, ~753 lines)
- deploy/ (dir, 7 files, ~809 lines)
- docker-compose.yml (~32 lines)
- Dockerfile (~27 lines)
- docs/ (dir, 49 files, ~11214 lines)
- examples/ (dir, 5 files, ~253 lines)
- get-started/ (dir, 5 files, ~631 lines)
- go.mod (~161 lines)
- go.sum (~489 lines)
- hello.wav (~0 lines)
- LICENSE (~201 lines)
- Makefile (~49 lines)
- NOTICE (~10 lines)
- pkg/ (dir, 229 files, ~25180 lines)
- plugins/ (dir, 1 files, ~0 lines)
- README.md (~510 lines)
- reference/ (dir, 5 files, ~601 lines)
- scripts/ (dir, 16 files, ~332 lines)
- sdk/ (dir, 1 files, ~5 lines)
- TESTING.md (~81 lines)
- tests/ (dir, 84 files, ~6964 lines)
- voila (~0 lines)
- web/ (dir, 3 files, ~1433 lines)

