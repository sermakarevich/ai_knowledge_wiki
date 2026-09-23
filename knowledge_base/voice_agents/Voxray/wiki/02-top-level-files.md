> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-level-files
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
---
## .gitignore
Build, dependency, IDE, and secret exclusions (verbatim):

```
*.exe
*.exe~
*.dll
*.so
*.dylib
/bin/
*.log
*.test
*.out
coverage.html
coverage.txt
vendor/
go.work
```

```
.vscode/
.idea/
*.iml
.cursor/
*.swp
*~
.project
.settings/
.classpath
*.wav
```

Secrets/config exclusion (verbatim):

```
# Config with secrets (use config.example.json as template, set api_keys via env)
/config.json
config_.json
*.local.json
.env
.env.local
```

**Covers:** `.gitignore` (02-top-level-files.md:6-51).

## API_SERVER.md — overview, auth, envelopes
Pipeline and base configuration (verbatim table from chunk):

| Item | Description |
|------|-------------|
| **Base URL** | Configurable via `host` and `port`. Default bind: all interfaces, port `8080`. Example: `http://localhost:8080` or `https://your-host:8080`. |
| **Versioned base path** | `/api/v1`. Versioned routes are under this prefix; legacy paths (e.g. `/start`, `/health`) remain available. |
| **Environment** | Configuration is env-based (no explicit dev/staging/prod). Key overrides: `VOXRAY_HOST`, `VOXRAY_PORT` (or `HOST`, `PORT`), `VOXRAY_TLS_ENABLE`, `VOXRAY_TLS_CERT_FILE`, `VOXRAY_TLS_KEY_FILE`, `VOXRAY_CORS_ORIGINS`, `VOXRAY_SERVER_API_KEY`, `VOXRAY_MAX_BODY_BYTES`, `VOXRAY_LOG_LEVEL`, `VOXRAY_JSON_LOGS`, plus recording/transcripts/session-store vars. |

Auth (verbatim table from chunk):

| Aspect | Detail |
|--------|--------|
| **Method** | Optional **API key**. No JWT, OAuth, or refresh flow. |
| **When required** | Only when `server_api_key` (config) or `VOXRAY_SERVER_API_KEY` (env) is set. When set, required for: `POST /start`, `POST /api/v1/start`, `POST`/`PATCH` `/sessions/{id}/api/offer` and `/api/v1/sessions/{id}/offer`, `POST /webrtc/offer`, `POST /api/v1/webrtc/offer`, and WebSocket `GET /ws`. |
| **How to pass** | `Authorization: Bearer <key>` or `X-API-Key: <key>`. |
| **Expiry / refresh** | None; key is static. |
| **Failure** | `401 Unauthorized` with standard error envelope and code `UNAUTHORIZED`. |

Envelopes (verbatim from chunk):

Success body: `{ "data": <payload>, "meta": { "requestId": "<uuid>" } }`.
Error body: `{ "error": { "code": "<code>", "message": "<message>", "requestId": "<id>", "details": [ { "field": "<name>", "message": "<msg>" } ] } }`.
Body cap: `max_request_body_bytes` (config) or `VOXRAY_MAX_BODY_BYTES`; when unset or zero, default 256 KB.

Error codes documented: `BAD_REQUEST` (also used for 405), `CONFLICT` (reserved), `FORBIDDEN` (reserved), `INTERNAL_ERROR`, `NOT_FOUND`, `RATE_LIMIT_EXCEEDED` (reserved, rate limiting not implemented), `SERVICE_UNAVAILABLE`, `UNAUTHORIZED`, `UNPROCESSABLE_ENTITY` (reserved), `VALIDATION_ERROR` (API_SERVER.md:118-151).

Endpoints visible before truncation:
- `GET /health` / `GET /api/v1/health` — liveness, `200 { "data": { "status": "ok" } }`, no auth (API_SERVER.md:159-182).
- `GET /ready` / `GET /api/v1/ready` — readiness, `503 SERVICE_UNAVAILABLE` when Redis session store ping fails (API_SERVER.md:186-209).
- `GET /metrics` — Prometheus text when enabled, `204 No Content` when disabled (API_SERVER.md:215-225).
- `GET /swagger/` / `GET /swagger/doc.json` — Swagger UI and OpenAPI doc with base path `/api/v1` (API_SERVER.md:229-237).
- `POST /webrtc/offer` / `POST /api/v1/webrtc/offer` — body `{ "offer": "<sdp string>" }`, returns `{ "data": { "answer": "<sdp>" } }`, available when `transport` is `smallwebrtc` or `both` (API_SERVER.md:240-274).
- `POST /start` / `POST /api/v1/start` — body `{ "createDailyRoom": boolean?, "enableDefaultIceServers": boolean?, "body": object? }`, returns `201` with `sessionId` plus optional `iceConfig` or `dailyRoom`/`dailyToken`, supports `Idempotency-Key` with 24h TTL (API_SERVER.md:278-317).
- `POST /sessions/{id}/api/offer` / `POST /api/v1/sessions/{id}/offer` — body `{ "sdp": "<string>", "type": string?, "pc_id": string?, "restart_pc": boolean?, "request_data": object?, "requestData": object? }`, returns `{ "data": { "answer": "<sdp>", "type": "answer" } }` (API_SERVER.md:321-353).

Truncated in chunk: `PATCH /sessions/{id}/api/o...` onward was cut (chunk notes `... (truncated, 7309 more characters)` at 02-top-level-files.md:358-359); contents after that point are not summarized here.

**Covers:** `API_SERVER.md` (02-top-level-files.md:53-360).

## config.example.json
Template header (verbatim):

```json
{
  "_comment": "Copy to config.json and set API keys (or use env vars). Unknown keys like _comment are ignored.",
  "_comment_turn_vad": "Use turn_detection silence for full utterance to LLM. If VAD misses speech (e.g. second utterance or quiet mic), lower vad_min_volume (e.g. 0.2) or vad_threshold."
}
```

Core settings (exact names/values from chunk):

| Key | Example value |
|---|---|
| `host` | `"localhost"` |
| `port` | `3042` |
| `model` | `"llama-3.1-8b-instant"` |
| `provider` | `"groq"` |
| `stt_provider` | `"sarvam"` |
| `llm_provider` | `"groq"` |
| `tts_provider` | `"sarvam"` |
| `stt_model` | `"saarika:v2.5"` |
| `stt_language` | `"hi-IN"` |
| `tts_model` | `"bulbul:v2"` |
| `tts_voice` | `"anushka"` |
| `transport` | `"both"` |
| `webrtc_ice_servers` | `["stun:stun.l.google.com:19302", "stun:openrelay.metered.ca:80"]` |
| `rtc_max_duration_secs` | `0` |
| `plugins` | `["echo"]` |
| `allow_interruptions` | `true` |
| `interruption_strategy` | `"keyword"` |
| `min_words` | `3` |
| `turn_detection` | `"silence"` |
| `turn_stop_secs` | `3.0` |
| `turn_pre_speech_ms` | `10` |
| `turn_max_duration_secs` | `2` |
| `vad_start_secs` | `0` |
| `user_turn_stop_timeout_secs` | `4` |
| `user_idle_timeout_secs` | `30` |
| `turn_async` | `false` |
| `vad_threshold` | `0.01` |
| `vad_type` | `"energy"` |
| `vad_confidence` | `0.2` |
| `vad_start_secs_vad` | `0.25` |
| `vad_stop_secs` | `0.16` |
| `vad_min_volume` | `0.25` |
| `cors_allowed_origins` | `[]` |
| `max_request_body_bytes` | `524288` |
| `server_api_key` | `""` |

`plugin_options` keys (exact names from chunk): `frame_filter.allowed_types` (`["TextFrame", "TranscriptionFrame"]`), `wake_check_filter.wake_phrases` (`["hey bot"]`) + `keepalive_secs: 5`, `stt_mute_filter.strategies` (`["first_speech", "always"]`), `audio_filter.filters` (`[{ "type": "gain", "gain": 0.9 }]`), `interruption_controller` (`{ "strategy": "min_words", "min_words": 3 }`), `external_chain` (`{ "url": "http://localhost:8765/chain", "stream": true, "timeout_sec": 45, "transcript_key": "input" }`), `rtvi` (`{ "protocol_version": "1.2.0" }`) (config.example.json:386-418).

`api_keys` placeholders (all empty in example): `openai`, `deepgram`, `cartesia`, `daily_room_url`, `aws`, `google_cloud_project`, `google_cloud_location`, `aws_region` (config.example.json:436-445).

**Covers:** `config.example.json` (02-top-level-files.md:362-450).

## go.sum
Pinned Go dependency hashes (`<module> <version> h1:...` plus `/go.mod h1:...` lines); visible excerpt includes `buf.build/go/protovalidate`, `cel.dev/expr`, `cloud.google.com/go`, `cloud.google.com/go/speech`, `cloud.google.com/go/texttospeech`, `github.com/aws/aws-sdk-go-v2` (+ `bedrockruntime`, `polly`, `s3`, `transcribestreaming`, `config`), `github.com/envoyproxy/go-control-plane`, `github.com/docker/docker`, `github.com/fsnotify/fsnotify` (go.sum:455-577).

Truncated in chunk: entries after `github.com/gammazero/deque v1.1.0` were cut (chunk notes `... (truncated, 32745 more characters)` at 02-top-level-files.md:578-579); remaining pinned modules are not listed here.

**Covers:** `go.sum` (02-top-level-files.md:452-580).

## NOTICE
Verbatim:

```
Voxray-AI
Copyright 2026 Voxray-AI

This product includes software developed by Voxray-AI and contributors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
```

**Covers:** `NOTICE` (02-top-level-files.md:582-595).

## TESTING.md
Commands (verbatim mapping from chunk):

| Command | Runs |
|---|---|
| `make build` | `go build -o voxray ./cmd/voxray` |
| `make run` | `go run ./cmd/voxray` |
| `make test` or `go test ./...` | full test suite (all features) |
| `go test ./tests/pkg/...` | core package/unit tests under `tests/pkg` |
| `go test ./tests/integration/...` | integration tests under `tests/integration` |
| `go test ./tests/e2e/...` | e2e tests under `tests/e2e` (once added) |

Conventions (exact names from chunk): unit tests are `*_test.go` under `tests/pkg/**` mirroring `pkg/**` (e.g. `tests/pkg/pipeline/pipeline_test.go` for `pkg/pipeline`), written as external packages (e.g. `package pipeline_test`) importing `github.com/Voxray-AI/Voxray/pkg/...`; integration under `tests/integration/`, future e2e/CLI under `tests/e2e/`, shared fixtures in `tests/testdata/`; `tests` is part of the module tree so `go test ./...` runs all of them (TESTING.md:625-635). Sarvam tests under `tests/pkg/services` skip unless `SARVAM_API_KEY` is set (TESTING.md:620-623). Suggested future targets `test-unit` → `go test ./pkg/...`, `test-integration` → `go test ./tests/integration/...`, `test-e2e` → `go test ./tests/e2e/...`, with `make test` remaining the aggregate; CI example runs `actions/checkout@v4`, `actions/setup-go@v5` with `go-version-file: go.mod`, `go mod tidy`, `go test ./...` (TESTING.md:637-670).

**Covers:** `TESTING.md` (02-top-level-files.md:597-680).

**Covers:** `.gitignore`, `API_SERVER.md`, `config.example.json`, `go.sum`, `NOTICE`, `TESTING.md` as given in chunk `02-top-level-files` (6 source files; `API_SERVER.md` and `go.sum` partially truncated as noted above)
