# Technical Analysis: VoiceBlender/voiceblender

**Repository:** https://github.com/VoiceBlender/voiceblender
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview

VoiceBlender is a Go service that bridges SIP and WebRTC voice calls with multi-party audio mixing, a REST API, and real-time webhooks (01-overview.md:9). The problem space is programmable telephony: unifying heterogeneous voice transports (carrier SIP, browser WebRTC, WhatsApp Business Calling, raw WebSocket PCM, experimental Media-over-QUIC) under one call-control and media-mixing model, plus AI-voice primitives (TTS, real-time STT, AI agents, answering-machine detection, recording, playback) and event delivery.

It addresses this by modeling every call endpoint as a leg attached to a room mixer, exposing synchronous room/media control and asynchronous SIP-triggering endpoints over REST on `:8080` (SIP on `127.0.0.1:5060` by default) (01-overview.md:52), streaming the same events over a WebSocket event interface (VSI at `GET /v1/vsi`) and outbound webhooks with HMAC-SHA256 signing, `event_id`/`X-Event-Id` dedup keys, and Prometheus metrics at `GET /metrics` (01-overview.md:29-39). Leg types include SIP inbound/outbound with codec negotiation (PCMU, PCMA, G.722, Opus, AMR-WB, AMR-NB), digest auth, RFC 4028 session timers, optional TLS on a second port, 183 early media, and hold via re-INVITE sendonly/sendrecv (01-overview.md:15-18); WebRTC via SDP offer/answer with trickle ICE; WhatsApp Business Calling over SIP-TLS + ICE/DTLS-SRTP + Opus; WebSocket legs with binary or `json_base64` framing at 8/16/24/48 kHz; and experimental MoQ legs disabled by default behind `MOQ_ENABLED=true` + `MOQ_TLS_CERT_FILE`/`MOQ_TLS_KEY_FILE` (01-overview.md:19-22). Rooms mix N participants with mixed-minus-self audio at 8/16/48 kHz (default 16 kHz), support bridging two same-rate mixers with configurable direction, and per-room role-based audio routing applied atomically at leg-join time (01-overview.md:23-25). The primary user is a backend/telephony developer building AI voice applications (call centers, agents, recording pipelines) who drives calls from server-side code rather than from a softphone UI.

## 2. High-Level Architecture

```
                    ┌─ SIP phones / trunks / WhatsApp (SIP-TLS+ICE/DTLS-SRTP) ─┐
                    │  WebRTC browsers (SDP + trickle ICE) / WS PCM / MoQ (exp) │
                    ▼                                                          │
            ┌───────────────┐   RTP/SRTP/WS/MoQ audio    ┌──────────────────┐
            │  Transport /  │ ─────────────────────────► │  Room mixers     │
            │  Leg adapters │ ◄───────────────────────── │  (mixed-minus-   │
            └───────│───────┘   mixed-minus-self @       │   self, 8/16/    │
                    │           8/16/48 kHz              │   48 kHz)        │
                    │                                    └────────┬─────────┘
                    │  control (REST :8080, VSI /v1/vsi)          │ bridge / routing matrix
                    ▼                                             ▼
            ┌───────────────┐   events                    ┌──────────────────┐
            │  REST + VSI + │ ──────────────────────────► │ Media / AI       │
            │  webhooks     │  leg.*, stt.*, HMAC-SHA256  │ TTS/STT/agents/  │
            └───────────────┘                             │ AMD/play/record  │
                    │                                     └──────────────────┘
                    ▼
            ┌───────────────┐
            │ Observability │  GET /metrics (Prometheus), pprof with -tags pprof
            └───────────────┘
```

Data-flow narrative:

1. A call enters or is originated through a transport adapter: inbound SIP/WhatsApp/WebRTC/WebSocket/MoQ offer, or `POST /v1/legs` originating an outbound leg (`sip`/`whatsapp`/`websocket`/`livekit_room`) with `to`/`uri`, `codecs`, `room_id`, `webhook_url`, `custom_data` (02-top-level-files.md:59). SIP-triggering endpoints validate synchronously (4xx on bad input) then queue SIP work (INVITE, BYE, re-INVITE, REFER, 100/180/183/200) on a goroutine and return `202 Accepted` with progressive-form status (`holding`, `ringing`, `answering`, …); completion or failure arrives later as `leg.connected`/`leg.hold`/`leg.disconnected`/`leg.command_failed` and stream events (02-top-level-files.md:23-37).
2. The leg's media (RTP/SRTP PCM, WS frames, MoQ Opus objects) joins a room mixer, which produces per-participant mixed-minus-self audio at the room rate; two same-rate mixers can be bridged with live-configurable direction, and a role-based who-hears-whom matrix is applied atomically at leg-join time (01-overview.md:23-25).
3. In-pipeline services operate on legs or room mixes: RFC 4733 DTMF, T.140 RTT over RTP per RFC 4103 with RFC 2198 redundancy, WAV/MP3 playback, TTS with preflight stage/commit, real-time STT with partials, AI agents with mid-session injection, AMD classification, stereo/multi-channel WAV recording with pause/resume and S3/GCS upload (01-overview.md:29-39).
4. Every state change emits typed events identically to webhooks (HMAC-SHA256, stable `event_id` / `X-Event-Id`, CDR-style `leg.disconnected`) and to the VSI WebSocket stream (`connected` frame, then event frames; commands return `<command>.result`/`error` echoing `request_id`), sourced from `internal/api/vsi_meta.go` (02-top-level-files.md:75-82).
5. Operators observe via `GET /metrics` (legs/rooms, durations, disconnect reasons, event-egress counters, Go runtime) and pprof when built with `-tags pprof` (01-overview.md:44).
6. A two-container cluster (`dialer` on host 8080, `peer` on 8081, shared `voiceblender.env`) exercises multi-instance behavior via `docker/docker-compose.cluster.yml` (01-overview.md:56-57, 01-overview.md:63-67).

Persistent state lives in memory (legs, rooms, bridges, staged TTS preflights bounded by `TTS_PREFLIGHT_TTL`/`TTS_PREFLIGHT_MAX_PER_LEG`/`TTS_PREFLIGHT_MAX_BYTES`), on disk (`RECORDING_DIR` default `/tmp/recordings`, `TTS_CACHE_DIR` default `/tmp/tts_cache` when `TTS_CACHE_ENABLED`), and externally in S3/GCS buckets on upload; `custom_data` lives only for the leg lifetime including the final `leg.disconnected` (02-top-level-files.md:61, 02-top-level-files.md:192).

## 3. The Leg-and-Room Call Model

The central abstraction is the leg (one call endpoint) composed into rooms (mixing contexts), with streams, roles, bridges, and per-leg `custom_data` as refinements.

Representation: a leg object carries `id`, `type` (`sip_inbound`, `sip_outbound`, `webrtc`, `whatsapp_in`, `whatsapp_out`, `websocket_in`, `websocket_out`, `moq_in`, `livekit_publish`, `livekit_participant`), `state`, `room_id`, `muted`, `deaf`, `held`, `role`, `headers`/`sip_headers`, and `custom_data` (02-top-level-files.md:7). Verbatim shape (02-top-level-files.md:44-57):

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "type": "sip_inbound",
  "state": "connected",
  "room_id": "room-123",
  "muted": false,
  "deaf": false,
  "held": false,
  "role": "agent"
}
```

Named kinds/types with file:line: leg types `sip_inbound`, `sip_outbound`, `webrtc`, `whatsapp_in`, `whatsapp_out`, `websocket_in`, `websocket_out`, `moq_in`, `livekit_publish`, `livekit_participant` (02-top-level-files.md:7); originate types `sip`/`whatsapp`/`websocket`/`livekit_room` on `POST /v1/legs` (02-top-level-files.md:59); codecs `PCMU`, `PCMA`, `G722`, `opus`, `AMR-WB`, `AMR-NB` (02-top-level-files.md:59); WS framing binary vs `json_base64` at 8/16/24/48 kHz (01-overview.md:21); room rates 8/16/48 kHz, default 16 kHz (01-overview.md:23); bridge directions bidirectional / one-way each way / parked (01-overview.md:24); SIPREC server/client roles gated by `SIPREC_ENABLED` (+`SIP_TCP_ENABLED`) and `SIPREC_SRC_ENABLED` (01-overview.md:27).

Key queries: `GET /v1/legs` (list), `GET /v1/legs/{id}` (detail), `GET /v1/legs/{id}/siprec` (`warnings` on `a=label` mismatch), `GET /v1/rooms`, `GET /v1/rooms/{id}`, `GET /v1/rooms/{id}/bridges`, `GET /v1/rooms/{id}/bridges/{bridgeID}` (01-overview.md:88-143); VSI mirrors: `list_legs`, `get_leg`, `list_rooms`, `get_room`, `leg_stream_list`/`leg_stream_get`, `bridge_list`/`bridge_get`, `room_routing_get`, `siprec_get` (02-top-level-files.md:82). Verbatim async rule governing leg commands (02-top-level-files.md:23-27):

```text
Every endpoint that triggers a SIP request or response (e.g. INVITE, BYE, re-INVITE for hold/unhold, REFER for transfer, 100/180/183/200 for inbound calls) is **asynchronous**. The HTTP handler validates inputs synchronously (returning 4xx if anything fails up front) then queues the SIP work on a goroutine and returns **`202 Accepted`** with a progressive-form status string (e.g. `holding`, `unholding`, `hanging_up`, `early_media`, `ringing`, `answering`).
```

## 4. LLM / External Service Integration

Providers (named in wiki): TTS from ElevenLabs, Google Cloud, AWS Polly, Deepgram, Azure; STT from ElevenLabs, Deepgram, Deepgram Flux (adds `stt.turn` turn detection), Azure, Speechmatics; AI agents from ElevenLabs, VAPI, Pipecat, Deepgram (01-overview.md:33-35). Media upload targets S3 or Google Cloud Storage; STUN/TURN via `ICE_SERVERS` (default `stun:stun.l.google.com:19302`) (02-top-level-files.md:118-132).

Required vs optional calls: no provider call is required for basic SIP/WebRTC call control, mixing, DTMF/RTT, playback of local files/tones, local WAV recording, webhooks/VSI, or metrics — media and signaling paths work without keys. TTS/STT/agent endpoints require the corresponding provider key; S3/GCS upload requires bucket configuration; WhatsApp calling requires the SIP-TLS listener (`SIP_TLS_PORT` + `SIP_TLS_CERT` + `SIP_TLS_KEY`; Meta rejects self-signed) (02-top-level-files.md:121-124). SIPREC server additionally needs `SIP_TCP_ENABLED=true` alongside `SIPREC_ENABLED=true` (01-overview.md:27).

Env vars: `ELEVENLABS_API_KEY`, `VAPI_API_KEY`, `DEEPGRAM_API_KEY`, `AZURE_SPEECH_KEY`/`AZURE_SPEECH_REGION` (default `eastus`), `SPEECHMATICS_API_KEY`/`SPEECHMATICS_URL` (default `wss://eu2.rt.speechmatics.com/v2`), `S3_BUCKET`, `S3_REGION` (default `us-east-1`), `S3_ENDPOINT`, `S3_PREFIX`, `S3_ALLOW_INSECURE_ENDPOINT`, `S3_PREFLIGHT_TIMEOUT` (default `10s`), `S3_REQUEST_PREFLIGHT_TIMEOUT` (default `2s`), `GCS_BUCKET`, `GCS_OBJECT_NAME_PREFIX`, plus AWS chain; TTS cache/preflight `TTS_CACHE_ENABLED` (default `false`), `TTS_CACHE_DIR`, `TTS_CACHE_INCLUDE_API_KEY`, `TTS_PREFLIGHT_TTL` (default `30s`), `TTS_PREFLIGHT_MAX_PER_LEG` (default `3`), `TTS_PREFLIGHT_MAX_BYTES` (02-top-level-files.md:132, 02-top-level-files.md:192).

## 5. The Outbound-Leg-to-Room Pipeline

Primary workflow: originate a leg, attach it to a room mixer, drive media/AI services on it, and observe outcomes via events.

1. `POST /v1/legs` — originate outbound leg (`sip`/`whatsapp`/`websocket`/`livekit_room`) with `to`/`uri`, `from`, `outbound_proxy`, `privacy`, `ring_timeout`, `max_duration`, `codecs`, `headers`, `auth`, `room_id`, `webhook_url`, `webhook_secret`, `custom_data`, `amd`, `speech_detection`, `rtt`, `streams` (02-top-level-files.md:59). Handler validates synchronously, queues SIP work, returns `202` with progressive status; success/failure surfaces as `leg.connected` vs `leg.command_failed` (`{leg_id, command, error}`, command in `ring`, `early_media`, `hold`, `unhold`, `add_to_room`, …) (02-top-level-files.md:23-37).
2. `POST /v1/legs/{id}/answer` / `POST /v1/legs/{id}/early-media` (183 with SDP) — accept inbound ringing legs or open pre-answer audio; same async `202` discipline (01-overview.md:93-94, 02-top-level-files.md:23-27).
3. `POST /v1/rooms` + `POST /v1/rooms/{id}/legs` — create room (rate 8/16/48 kHz) and add/move leg; role routing matrix applied atomically at join; multi-`m=audio` sections (RFC 3264, SIPREC RFC 7866 wire profile) each bind RTP port/direction/language/mixer room; outcomes via `leg.stream_added`/`removed`/`rejected`/`failed`, `leg.stream_room_changed`/`leg.stream_role_changed` (01-overview.md:25-26, 01-overview.md:132-138, 02-top-level-files.md:30-36).
4. In-call media control (synchronous, per 02-top-level-files.md:38-42): `POST /v1/legs/{id}/mute` + `DELETE /v1/legs/{id}/mute`, deaf equivalents, `POST /v1/legs/{id}/dtmf` (RTP, not SIP), `POST /v1/legs/{id}/rtt`, `POST /v1/legs/{id}/play` / `DELETE /v1/legs/{id}/play/{pbID}`, room-level `POST /v1/rooms/{id}/play` (01-overview.md:96-111, 01-overview.md:145-146).
5. Intelligence layer: `POST /v1/legs/{id}/tts` (or `/tts/preflight` → `/tts/{ttsID}/commit` vs `DELETE /v1/legs/{id}/tts/{ttsID}` speculative staging), `POST /v1/legs/{id}/stt` → `/stt/finalize` → `DELETE /v1/legs/{id}/stt`, `POST /v1/legs/{id}/amd`, `POST /v1/legs/{id}/agent` → `/agent/message` → `DELETE /v1/legs/{id}/agent`, with room-scoped TTS/STT/record parallels (`POST /v1/rooms/{id}/tts|stt|record`) (01-overview.md:113-128, 01-overview.md:147-154).
6. Capture and interconnect: `POST /v1/legs/{id}/record` → `/record/pause` → `/record/resume` → `DELETE /v1/legs/{id}/record` (pause writes silence), room-record parallels, `POST /v1/rooms/{id}/siprec` client fork vs SIPREC server multipart INVITEs, `POST /v1/rooms/{id}/bridges` → `PATCH` direction → `DELETE` teardown (01-overview.md:117-120, 01-overview.md:139-143, 01-overview.md:148-151).
7. Teardown and audit: `DELETE /v1/legs/{id}` (hangup, async `hanging_up`), `DELETE /v1/rooms/{id}` (hangs up all legs), terminal `leg.disconnected` CDR with lifetime `custom_data` echo; per-event webhook retry and VSI replay (01-overview.md:95, 01-overview.md:136, 02-top-level-files.md:61).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `API.md` | 5101 | REST reference: base URL, sync/async contract, leg/room schemas, events (02-top-level-files.md:15-62) |
| `openapi.yaml` | 6746 | Generated OpenAPI 3.1.0 REST spec + `x-config-vars` table; do not hand-edit (02-top-level-files.md:146-157) |
| `asyncapi.yaml` | 7206 | Generated AsyncAPI 3.0.0 VSI spec for `/v1/vsi`; do not hand-edit (02-top-level-files.md:63-82) |
| `CONFIGURATION.md` | 145 | Env-var reference (single source of truth beside `internal/config/config.go`) (02-top-level-files.md:102-132) |
| `voiceblender.env.example` | 277 | Ready-to-edit env template; `cp` to `voiceblender.env` (untracked) (02-top-level-files.md:181-192) |
| `internal/config/config.go` | — | Env-var reader; every var must appear in example + `CONFIGURATION.md` (02-top-level-files.md:10-12) |
| `internal/api/server.go` | — | chi route wiring; generator does not discover routes from here (02-top-level-files.md:89) |
| `internal/api/openapi_meta.go` | — | `RoutesMetadata()` registry backing OpenAPI generation (02-top-level-files.md:89) |
| `internal/api/vsi_meta.go` | — | `VSICommandsMetadata`, `EventsMetadata`, `VSILifecycleFramesMetadata`; every command/event must be registered (02-top-level-files.md:75-90) |
| `cmd/voiceblender` | — | Service entrypoint (`go build -o voiceblender ./cmd/voiceblender`) (01-overview.md:49-56) |
| `cmd/openapi-gen/main.go` | — | OpenAPI generator; `tagDescriptions()` for new tags (02-top-level-files.md:89) |
| `cmd/asyncapi-gen` | — | AsyncAPI generator (`make asyncapi` / `go generate ./internal/api/`) (02-top-level-files.md:66-72) |
| `docker/docker-compose.cluster.yml` | — | Two-instance (`dialer`/`peer`) cluster for manual e2e (01-overview.md:63-67) |
| `TESTING.md` | 726 | Unit + `tests/integration/` + benchmark test guide (02-top-level-files.md:159-179) |
| `tests/integration/` | — | Loopback-SIP integration tests (`-tags integration`) incl. `TestConcurrentRoomsScale` (02-top-level-files.md:160-179) |
| `go.mod` / `go.sum` | 404 (`go.sum`) | Module + dependency pins incl. `goamr-nb`/`goamr-wb` (02-top-level-files.md:134-144) |
| `CLAUDE.md` | 42 | Contributor workflow: gofmt, spec regen, docs, tests, no API churn, never commit (02-top-level-files.md:84-100) |

## 7. Dependencies

Required first (exact constraint strings as captured in wiki; full pins live in `go.sum`):

| Package | Version constraint | Purpose |
|---|---|---|
| `github.com/VoiceBlender/goamr-nb` | `v1.0.0` | AMR-NB codec (02-top-level-files.md:141) |
| `github.com/VoiceBlender/goamr-wb` | `v1.1.1` | AMR-WB codec (02-top-level-files.md:142) |
| `github.com/aws/aws-sdk-go-v2` | `v1.41.3` | S3 upload path (hash line; 02-top-level-files.md:143) |
| `cloud.google.com/go` | `v0.121.4` | GCS upload path (hash line; 02-top-level-files.md:140) |
| `cel.dev/expr` | `v0.25.1` | Expression dependency (transitive; 02-top-level-files.md:139) |
| `buf.build/gen/go/bufbuild/protovalidate/protocolbuffers/go` | `v1.36.6-20250625184727-c923a0c2a132.1` | Protobuf validation (transitive; 02-top-level-files.md:138) |

Standard toolchain: Go (`go build`, `go run`, `go test`, `gofmt`; unit `go test ./internal/...`, integration `go test -tags integration -timeout 60s ./tests/integration/`) (01-overview.md:49-56, 02-top-level-files.md:160-179). External services are optional (provider keys, S3/GCS, STUN/TURN) — see section 4. No further exact constraint strings are visible in the two wiki pages; the complete pin list is in `go.sum` (404 lines, truncated in chunk) (02-top-level-files.md:134-144).

## 8. CLI / Usage Surface

Entry points: `go build -o voiceblender ./cmd/voiceblender && ./voiceblender`, or `go run ./cmd/voiceblender`; cluster via `docker compose -f docker/docker-compose.cluster.yml up --build` (01-overview.md:49-67, 02-top-level-files.md:160-176).

| Command | Effect |
|---|---|
| `go build -o voiceblender ./cmd/voiceblender` | Build server binary (01-overview.md:49-56) |
| `go run ./cmd/voiceblender` | Run without separate build (01-overview.md:49-56) |
| `docker compose -f docker/docker-compose.cluster.yml up --build` | Two-instance (`dialer` :8080, `peer` :8081) cluster (01-overview.md:63-67) |
| `go test ./internal/...` | Fast unit tests (02-top-level-files.md:160-164) |
| `go test -tags integration -timeout 60s ./tests/integration/` | Loopback-SIP integration tests (02-top-level-files.md:160-168) |
| `go test -tags integration -v -timeout 300s -run TestConcurrentRoomsScale ./tests/integration/` | Scaling/audio-latency benchmark (02-top-level-files.md:170-173) |
| `make openapi` / `make asyncapi` / `make specs` | Regenerate specs (never hand-edit `openapi.yaml`/`asyncapi.yaml`) (02-top-level-files.md:87-90) |
| `go generate ./internal/api/` | Underlying spec generation (02-top-level-files.md:66-72) |
| `go test ./internal/api/ -count=1` | Verify route-metadata/spec consistency after route changes (02-top-level-files.md:89) |
| `cp voiceblender.env.example voiceblender.env` | Create local (untracked) env file (02-top-level-files.md:184-190) |

Representative REST commands (full lists in 01-overview.md:88-154): `POST /v1/legs`, `GET /v1/legs`, `GET /v1/legs/websocket`, `GET /v1/legs/{id}`, `POST /v1/legs/{id}/answer|early-media|mute|hold|transfer|dtmf|rtt|play|tts|record|stt|amd|agent`, `DELETE /v1/legs/{id}`; `POST|GET|DELETE /v1/rooms`, `POST /v1/rooms/{id}/legs`, bridges CRUD, `GET /v1/rooms/{id}/ws`, room play/tts/record/stt; `GET /v1/vsi`, `GET /metrics`.

| Env var | Default | Effect |
|---|---|---|
| `HTTP_ADDR` | `:8080` | REST listen address (02-top-level-files.md:114-118) |
| `SIP_BIND_IP` / `SIP_PORT` | `127.0.0.1` / `5060` | SIP UDP bind (loopback default; must expose for real trunks) (02-top-level-files.md:120-123, 02-top-level-files.md:192) |
| `ALLOWED_IPS` | empty = allow all | Sole gate for all HTTP endpoints incl. VSI/WS/MoQ/metrics/pprof (01-overview.md:80, 02-top-level-files.md:118) |
| `TRUST_PROXY_HEADERS` | `false` | Honor leftmost `X-Forwarded-For`; only behind trusted proxy (02-top-level-files.md:119) |
| `WEBHOOK_URL` / `WEBHOOK_SECRET` | empty | Default webhook target + HMAC secret (distinct from HTTP auth) (01-overview.md:81, 02-top-level-files.md:129) |
| `INSTANCE_ID` | auto UUID | Instance id in API responses and webhooks (02-top-level-files.md:116) |
| `SIP_CODECS` | `PCMU,PCMA` | Default negotiated codecs (02-top-level-files.md:192) |
| `RTP_PORT_MIN` / `RTP_PORT_MAX` | `10000` / `20000` | RTP port range (02-top-level-files.md:192) |
| `DEFAULT_SAMPLE_RATE` | `16000` | Default room/mixer rate (02-top-level-files.md:192) |
| `RECORDING_DIR` | `/tmp/recordings` | Recording output dir (02-top-level-files.md:127) |
| `CUSTOM_DATA_MAX_BYTES` | `1024` | Leg `custom_data` cap; `0` = unlimited; 400 on exceed (02-top-level-files.md:61, 02-top-level-files.md:130) |
| `LOG_LEVEL` | `info` | `debug`/`info`/`warn`/`error`; payloads/transcripts only at `debug` (02-top-level-files.md:128) |
| `SIPREC_ENABLED` (+`SIP_TCP_ENABLED`) / `SIPREC_SRC_ENABLED` | `false` / `false` | SIPREC server / recording-client fork (01-overview.md:27) |
| `MOQ_ENABLED` (+`MOQ_TLS_CERT_FILE`/`MOQ_TLS_KEY_FILE`) | `false` | Experimental MoQ legs (01-overview.md:22) |

## 9. Extensibility Points

- New REST endpoint: add chi wiring in `internal/api/server.go`, register in `RoutesMetadata()` in `internal/api/openapi_meta.go`, add tag in `tagDescriptions()` in `cmd/openapi-gen/main.go` if new, run `make specs`, grep path in `openapi.yaml`, run `go test ./internal/api/ -count=1`, update `API.md` with examples; observability (`/metrics`/health via `addObservabilityPaths()`) excepted from metadata (02-top-level-files.md:89).
- New VSI command/event: extend `VSICommandsMetadata`, `EventsMetadata`, `VSILifecycleFramesMetadata` in `internal/api/vsi_meta.go`, run `make asyncapi` (or `make specs` for both); every event in `internal/events` must be registered or the spec is incomplete (02-top-level-files.md:75-90).
- New configuration: add reader in `internal/config/config.go`, then update `CONFIGURATION.md` table, `README.md` (feature note, no env tables), and `voiceblender.env.example` with the real default (02-top-level-files.md:91-100).
- New codec/media path: SIP codecs negotiated per leg (`PCMU`, `PCMA`, `G722`, `opus`, `AMR-WB`, `AMR-NB`); AMR handled via the pinned `goamr-nb`/`goamr-wb` modules; jitter/comfort-noise knobs (`SIP_JITTER_BUFFER_MS`, `WS_JITTER_BUFFER_MS`, `COMFORT_NOISE_ENABLED`) bound the media pipeline (02-top-level-files.md:59, 02-top-level-files.md:132, 02-top-level-files.md:141-142).
- New TTS/STT/agent provider: add provider behind the existing leg/room `tts`/`stt`/`agent` endpoints and VSI `leg_*` media commands; wire its `*_API_KEY` env var alongside the current provider set (01-overview.md:33-35, 02-top-level-files.md:132).
- New tests: unit tests per new package/feature plus `tests/integration/` coverage and a `TESTING.md` update (02-top-level-files.md:95-99).

## 10. Limitations and Gotchas

- **HTTP surface has no credential auth — `ALLOWED_IPS` is the only gate.** REST, VSI, WS/MoQ leg endpoints, `/metrics`, and pprof share one IP allowlist (empty = allow all); only `X-Forwarded-For` is consulted and only when `TRUST_PROXY_HEADERS=true`. Front with a reverse proxy for per-caller credentials; do not expose `:8080` directly (01-overview.md:11, 01-overview.md:82-90, 02-top-level-files.md:118-119).
- **SIP-triggering calls are async: `202` is not success.** `202 Accepted` with `holding`/`ringing`/`answering` only means validation passed and work was queued; real outcomes arrive as `leg.*` events or `leg.command_failed` with `{leg_id, command, error}`. Polling GET state instead of consuming events/webhooks/VSI misses failures (02-top-level-files.md:23-37).
- **Defaults bind to loopback and disable key features.** SIP defaults to `127.0.0.1:5060`, so trunks/peers fail until bind/advertised IP, ports, and RTP range are set; SIPREC server/client and MoQ are all `false`/disabled by default and SIPREC server additionally requires `SIP_TCP_ENABLED=true`; WhatsApp needs the TLS listener with a non-self-signed cert (01-overview.md:22, 01-overview.md:27, 02-top-level-files.md:120-124, 02-top-level-files.md:192).
- **Room mixing constraints are strict.** Bridges only join same-sample-rate mixers, and the role routing matrix applies atomically at leg-join time — mid-call role changes go through stream update paths (`leg.stream_role_changed`), not silent mutation (01-overview.md:23-25, 02-top-level-files.md:30-36).
- **Spec and docs are generated — hand edits get clobbered.** `openapi.yaml`/`asyncapi.yaml` regenerate from `internal/api/*_meta.go` via `make specs`; `CONFIGURATION.md`/`voiceblender.env.example`/`API.md`/`README.md`/`TESTING.md` must be updated alongside code, routes registered in `RoutesMetadata()`, and `git commit` is forbidden by contributor rules (stage only) (02-top-level-files.md:84-100).

## 11. How It Compares to Alternatives

- **FreeSWITCH / Asterisk:** full PBX/softswitch stacks with dialplans, registrations, and media servers, far broader telephony features but heavier to embed as a programmable Go microservice; VoiceBlender instead exposes legs/rooms over REST/VSI with generated OpenAPI/AsyncAPI contracts (01-overview.md:88-154, 02-top-level-files.md:146-157).
- **LiveKit:** WebRTC-first SFU/mixing rooms with client SDKs; VoiceBlender covers the SIP-carrier/WhatsApp/PSTN edge (digest auth, session timers, REFER transfer, SIPREC, AMR codecs) plus telephony events (DTMF/RTT/AMD/CDR) that a pure SFU does not model (01-overview.md:15-27, 01-overview.md:29-39).
- **Twilio Voice / Vonage / Plivo (CPaaS):** hosted call-control APIs with per-minute pricing and vendor lock-in; VoiceBlender is a self-hosted Go binary configured entirely by env vars with IP-allowlist gating, suited to teams that want the control surface in-cluster (01-overview.md:11, 01-overview.md:64-69).
- **Jambonz / SignalWire:** closer open-source/CPaaS analogues for webhook-driven call control with TTS/STT/agent hooks; VoiceBlender differentiates on the leg/room mixer model (mixed-minus-self, bridging, role routing), multi-`m=audio`/SIPREC handling, and the triple surface of REST + HMAC webhooks + bidirectional VSI command stream (01-overview.md:23-39, 02-top-level-files.md:63-82).
- Positioning: VoiceBlender is the self-hosted, SIP-centric programmable voice-mixing layer for AI call flows — strongest where carrier interop, room mixing/bridging, and provider-pluggable TTS/STT/agents matter more than a full PBX or a browser-only SFU.

## Appendix: Selected Code Snippets

Build and run, verbatim (01-overview.md:49-56):

```bash
# Build and run
go build -o voiceblender ./cmd/voiceblender
./voiceblender

# Or run directly
go run ./cmd/voiceblender
```

Cluster, verbatim (01-overview.md:63-67):

```bash
docker compose -f docker/docker-compose.cluster.yml up --build
```

Async SIP rule, verbatim (02-top-level-files.md:23-27):

```text
Every endpoint that triggers a SIP request or response (e.g. INVITE, BYE, re-INVITE for hold/unhold, REFER for transfer, 100/180/183/200 for inbound calls) is **asynchronous**. The HTTP handler validates inputs synchronously (returning 4xx if anything fails up front) then queues the SIP work on a goroutine and returns **`202 Accepted`** with a progressive-form status string (e.g. `holding`, `unholding`, `hanging_up`, `early_media`, `ringing`, `answering`).
```

Test quick reference, verbatim (02-top-level-files.md:160-176):

```bash
# Unit tests only (fast, no external dependencies)
go test ./internal/...

# Integration tests (requires no external services, uses loopback SIP)
go test -tags integration -timeout 60s ./tests/integration/

# Everything
go test ./internal/... && go test -tags integration -timeout 60s ./tests/integration/

# Benchmark (scaling + audio latency)
go test -tags integration -v -timeout 300s -run TestConcurrentRoomsScale ./tests/integration/

# Two-instance cluster (for manual end-to-end / peer-to-peer scenarios)
docker compose -f docker/docker-compose.cluster.yml up --build
```
