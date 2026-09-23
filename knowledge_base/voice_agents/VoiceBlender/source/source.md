# VoiceBlender/voiceblender
> PDF: https://github.com/VoiceBlender/voiceblender (not copied locally; no source.pdf in workflow run dir)
Source: https://github.com/VoiceBlender/voiceblender
Kind: repo
Fetched: 2026-09-22T14:50:23.029123+00:00
Tool: git-clone

# VoiceBlender/voiceblender

Commit: 9083dcf7afa08a6dcf696c4555d450f30b311491

## README

# VoiceBlender

A Go service that bridges SIP and WebRTC voice calls with multi-party audio mixing, a REST API, and real-time webhooks.

[![Join our Discord](https://img.shields.io/badge/Discord-Join%20our%20community-5865F2?logo=discord&logoColor=white)](https://discord.gg/HE9WDMzavN)

## Features

- **SIP inbound & outbound** -- receive and originate SIP calls with codec negotiation (PCMU, PCMA, G.722, Opus, AMR-WB, AMR-NB), digest auth, session timers (RFC 4028)
- **SIP over TLS** -- optional TLS transport on a second port alongside UDP, reusable by classic SIP trunks and required by WhatsApp
- **Early media** -- SIP 183 Session Progress with SDP for pre-answer audio (custom ringback, IVR)
- **Hold/unhold** -- SIP re-INVITE with sendonly/sendrecv direction
- **WebRTC** -- browser-based voice via SDP offer/answer with trickle ICE
- **WhatsApp Business Calling** -- inbound and outbound calls over SIP-TLS + ICE/DTLS-SRTP + Opus 
- **WebSocket legs** -- inbound (HTTP upgrade) and outbound (dial) PCM-over-WebSocket legs with binary or `json_base64` framing, configurable sample rate (8/16/24/48 kHz), bidirectional text, and caller-supplied X-/P- headers — designed to also back a future generic Agent API
- **MoQ legs (experimental, PoC)** -- inbound Media-over-QUIC legs over WebTransport/HTTP/3 with Opus framed one frame per MoQ Object (LOC-style). Tracks `mengelbart/moqtransport` (IETF draft-11); browser interop with draft-16 clients (moqtail, moq.dev) is not expected to work out of the box. Disabled by default; enable with `MOQ_ENABLED=true` + `MOQ_TLS_CERT_FILE` / `MOQ_TLS_KEY_FILE`
- **Multi-party rooms** -- mix N participants with mixed-minus-self audio at a configurable sample rate (8 kHz, 16 kHz, or 48 kHz per room; default 16 kHz)
- **Room bridging** -- join two rooms' mixers (same sample rate) with live-configurable direction (bidirectional, one-way each way, or parked); echo-free via mixed-minus-self
- **Audio routing matrix** -- per-room role-based routing for asymmetric audio (barge-in / whisper / supervisor monitor). Tag legs with a free-form `role` and declare a matrix of who-hears-whom by role. Applied atomically at leg-join time so a supervisor cannot momentarily bleed into the customer's audio. See [API.md](API.md#audio-routing-matrix).
- **Multi-stream SIP calls** -- several `m=audio` sections in one dialog (RFC 3264), each with its own RTP port, direction, language and mixer room; built for live translation, where the original audio and a translated feed are mixed separately. Follows the SIPREC (RFC 7866) wire profile for interoperability. See [API.md](API.md#per-leg-audio-streams-multiple-maudio-lines).
- **SIPREC session recording server (RFC 7865 / RFC 7866)** -- accept recording sessions forked from an SBC or PBX: multipart `SDP` + `rs-metadata` INVITEs are answered receive-only on every `m=audio` section, and each section is bound to the participant the metadata names. The received audio is an ordinary set of leg streams, so it can be recorded to file *and* attached to rooms for live STT/agents. Disabled by default; enable with `SIPREC_ENABLED=true` (needs `SIP_TCP_ENABLED=true`). The metadata is checked against the SDP it arrived with, so a client that binds a participant to the wrong `a=label` -- a document that is otherwise valid and would silently attribute audio to the wrong party -- is reported in `warnings` on `GET /v1/legs/{id}/siprec` instead of being recorded as if it were correct. VoiceBlender can also act as the **recording client**, forking a room's participants to an external recording server one stream each (`POST /v1/rooms/{id}/siprec`, `SIPREC_SRC_ENABLED=true`). See [API.md](API.md#siprec-session-recording).
- **WebSocket room access** -- join rooms from any client over a WebSocket with base64 PCM frames
- **DTMF** -- send and receive RFC 4733 telephone-events
- **Real-Time Text (RTT)** -- ITU-T T.140 over RTP per RFC 4103 with RFC 2198 redundancy;
- **Recording** -- stereo WAV recording per-leg or per-room, multi-channel per-participant tracks, pause/resume (writes silence to preserve timeline while sensitive data is exchanged), optional S3 or Google Cloud Storage upload
- **Playback** -- stream WAV/MP3 audio or built-in telephone tones into legs or rooms
- **TTS** -- text-to-speech into legs or rooms (ElevenLabs, Google Cloud, AWS Polly, Deepgram, Azure), with optional **preflight staging**: synthesize a speculative reply off the critical path, then commit it for instant playback or discard it
- **STT** -- real-time speech-to-text with partial transcripts (ElevenLabs, Deepgram, Deepgram Flux, Azure, Speechmatics). Deepgram Flux adds conversational turn detection (`stt.turn`), including eager end-of-turn signals for speculative generation; Speechmatics reports end-of-turn from server-side silence detection and supports mid-stream finalize
- **AI Agent** -- attach a conversational AI agent to a leg or room (ElevenLabs, VAPI, Pipecat, Deepgram) with mid-session context injection
- **Answering Machine Detection (AMD)** -- per-call analysis of outbound call audio to classify the answerer as human, machine, no-speech, or not-sure; optional voicemail beep detection via Goertzel frequency analysis
- **Webhooks** -- real-time event delivery with HMAC-SHA256 signing and retry; a stable per-event `event_id` (also sent as `X-Event-Id`) for receiver-side deduplication; typed event data with CDR-style `leg.disconnected` (disposition, timing, quality)
- **WebSocket event stream (VSI)** -- `GET /v1/vsi` streams all events and accepts commands (mute, hold, DTMF, room management) over a single persistent WebSocket; filter by `app_id` regex for multi-tenant isolation
- **Prometheus metrics** -- operational metrics exposed at `GET /metrics` (active legs/rooms, call durations, disconnect reasons, event-egress drop/delivery counters, Go runtime). See [API.md](API.md) for the full metric reference. Profiling via `go tool pprof` is available at `/debug/pprof/` when built with `-tags pprof`.

## Quick Start

```bash
# Build and run
go build -o voiceblender ./cmd/voiceblender
./voiceblender

# Or run directly
go run ./cmd/voiceblender
```

The REST API listens on `:8080` and SIP on `127.0.0.1:5060` by default.

### Multi-instance cluster

`docker/docker-compose.cluster.yml` brings up two VoiceBlender containers (`dialer` on host port 8080, `peer` on 8081) sharing the same `voiceblender.env`. Useful for end-to-end testing of inter-instance calls, REFER transfers, and webhook delivery between peers. Bring it up with:

```bash
docker compose -f docker/docker-compose.cluster.yml up --build
```

## Configuration

All configuration is via environment variables. The full reference — every variable,
its default and behaviour, plus the S3 bucket preflight rules — lives in
**[CONFIGURATION.md](CONFIGURATION.md)**.

A ready-to-edit file with every variable is committed as
[voiceblender.env.example](voiceblender.env.example).

Online documentation: <https://voiceblender.org/docs/>

## Links

- **Website:** [voiceblender.org](https://voiceblender.org/)
- **Documentation:** [voiceblender.org/docs](https://voiceblender.org/docs)

## API Overview

Full reference: [API.md](API.md)

> **API authentication.** The HTTP surface — REST, the `/v1/vsi` event
> WebSocket, `/v1/legs/websocket`, the `/v1/legs/moq` WebTransport endpoint,
> `/metrics`, and pprof — has **no built-in credential authentication** (no API
> key, bearer token, or session). Access is gated **solely** by the `ALLOWED_IPS`
> allowlist and your network placement. Do not expose it to untrusted networks;
> front it with a reverse proxy or gateway that enforces auth if you need
> per-caller credentials. This is distinct from SIP-layer auth (digest challenge
> of inbound INVITE/REGISTER) and outbound webhook signing (`WEBHOOK_SECRET`),
> which are covered separately below.

### Legs

```
POST   /v1/legs                    # Originate outbound leg (sip / whatsapp / websocket / livekit_room)
GET    /v1/legs                    # List all legs
GET    /v1/legs/websocket          # Connect a WebSocket leg (HTTP upgrade)
GET    /v1/legs/{id}               # Get leg details
POST   /v1/legs/{id}/answer        # Answer ringing inbound leg
POST   /v1/legs/{id}/early-media   # Enable early media (183)
DELETE /v1/legs/{id}               # Hang up
POST   /v1/legs/{id}/mute          # Mute
DELETE /v1/legs/{id}/mute          # Unmute
POST   /v1/legs/{id}/hold          # Put on hold
DELETE /v1/legs/{id}/hold          # Resume from hold
POST   /v1/legs/{id}/transfer            # Initiate a SIP REFER (blind or attended)
POST   /v1/legs/{id}/transfer/accept     # Accept a parked inbound REFER (202 + NOTIFY 100)
POST   /v1/legs/{id}/transfer/progress   # Interim sipfrag NOTIFY (e.g. 180 Ringing)
POST   /v1/legs/{id}/transfer/complete   # Terminal NOTIFY (200 OK or failure)
POST   /v1/legs/{id}/transfer/decline    # Reject a parked inbound REFER (603 default)
POST   /v1/legs/{id}/dtmf          # Send DTMF digits
POST   /v1/legs/{id}/dtmf/accept   # Re-enable DTMF reception (default)
POST   /v1/legs/{id}/dtmf/reject   # Stop receiving DTMF broadcast from peers
POST   /v1/legs/{id}/rtt           # Send Real-Time Text chunk (T.140 / RFC 4103)
POST   /v1/legs/{id}/rtt/accept    # Re-enable RTT reception (default)
POST   /v1/legs/{id}/rtt/reject    # Stop emitting rtt.received events
POST   /v1/legs/{id}/play          # Play audio or tone
DELETE /v1/legs/{id}/play/{pbID}   # Stop playback
POST   /v1/legs/{id}/tts           # Text-to-speech
POST   /v1/legs/{id}/tts/preflight # Synthesize and hold for a later commit (speculative reply)
POST   /v1/legs/{id}/tts/{ttsID}/commit # Play a staged utterance
DELETE /v1/legs/{id}/tts/{ttsID}   # Drop a staged utterance without playing it
POST   /v1/legs/{id}/record        # Start recording
DELETE /v1/legs/{id}/record        # Stop recording
POST   /v1/legs/{id}/record/pause  # Pause recording (writes silence)
POST   /v1/legs/{id}/record/resume # Resume recording
POST   /v1/legs/{id}/stt           # Start speech-to-text
POST   /v1/legs/{id}/stt/finalize  # Flush STT and emit a final transcript
DELETE /v1/legs/{id}/stt           # Stop speech-to-text
POST   /v1/legs/{id}/amd            # Start answering machine detection
POST   /v1/legs/{id}/agent         # Attach AI agent
POST   /v1/legs/{id}/agent/message # Inject message into agent
DELETE /v1/legs/{id}/agent         # Detach AI agent
                                   # LiveKit: each remote LK participant becomes its own `livekit_participant` leg in the same VB room.
                                   # Per-LK operations (mute, recording, role, hangup) use the standard /v1/legs/{id}/* endpoints.
```

### Rooms

```
POST   /v1/rooms                   # Create room
GET    /v1/rooms                   # List rooms
GET    /v1/rooms/{id}              # Get room
DELETE /v1/rooms/{id}              # Delete room (hangs up all legs)
POST   /v1/rooms/{id}/legs         # Add or move leg to room
DELETE /v1/rooms/{id}/legs/{legID}      # Remove leg from room
POST   /v1/rooms/{id}/bridges      # Bridge this room's mixer to another room
GET    /v1/rooms/{id}/bridges      # List bridges involving this room
GET    /v1/rooms/{id}/bridges/{bridgeID}    # Get a bridge
PATCH  /v1/rooms/{id}/bridges/{bridgeID}    # Change bridge direction
DELETE /v1/rooms/{id}/bridges/{bridgeID}    # Tear down a bridge
GET    /v1/rooms/{id}/ws           # Join room via WebSocket
POST   /v1/rooms/{id}/play         # Play audio or tone to room
DELETE /v1/rooms/{id}/play/{pbID}  # Stop room playback
POST   /v1/rooms/{id}/tts          # TTS to room
POST   /v1/rooms/{id}/record       # Record room mix
DELETE /v1/rooms/{id}/record       # Stop room recording
POST   /v1/rooms/{id}/record/pause # Pause room recording
POST   /v1/rooms/{id}/record/resume # Resume room recording
POST   /v1/rooms/{id}/stt          # STT on all participants
DELETE /v1/rooms/{id}/stt          # Stop room STT
POST   /v1/r

... (truncated, 20450 more characters)

## go.mod

```
module github.com/VoiceBlender/voiceblender

go 1.26

require (
	cloud.google.com/go/storage v1.56.0
	cloud.google.com/go/texttospeech v1.16.0
	github.com/VoiceBlender/goamr-nb v1.0.0
	github.com/VoiceBlender/goamr-wb v1.1.1
	github.com/aws/aws-sdk-go-v2 v1.41.3
	github.com/aws/aws-sdk-go-v2/config v1.32.11
	github.com/aws/aws-sdk-go-v2/credentials v1.19.11
	github.com/aws/aws-sdk-go-v2/service/polly v1.54.12
	github.com/aws/aws-sdk-go-v2/service/s3 v1.96.3
	github.com/emiago/sipgo v1.4.3
	github.com/go-audio/audio v1.0.0
	github.com/go-audio/wav v1.1.0
	github.com/go-chi/chi/v5 v5.2.5
	github.com/gobwas/ws v1.4.0
	github.com/golang-jwt/jwt/v5 v5.3.1
	github.com/google/uuid v1.6.0
	github.com/hajimehoshi/go-mp3 v0.3.4
	github.com/icholy/digest v1.1.0
	github.com/livekit/protocol v1.46.6
	github.com/mengelbart/moqtransport v0.5.0
	github.com/pion/interceptor v0.1.44
	github.com/pion/logging v0.2.4
	github.com/pion/rtp v1.10.1
	github.com/pion/sdp/v3 v3.0.18
	github.com/pion/stun/v3 v3.1.1
	github.com/pion/webrtc/v4 v4.2.9
	github.com/prometheus/client_golang v1.23.2
	github.com/quic-go/quic-go v0.53.0
	github.com/quic-go/webtransport-go v0.9.0
	github.com/thesyncim/gopus v0.1.1
	github.com/zaf/g711 v1.4.0
	golang.org/x/sync v0.20.0
	google.golang.org/api v0.247.0
	google.golang.org/protobuf v1.36.11
	gopkg.in/yaml.v3 v3.0.1
)

require (
	buf.build/gen/go/bufbuild/protovalidate/protocolbuffers/go v1.36.6-20250625184727-c923a0c2a132.1 // indirect
	buf.build/go/protovalidate v0.13.1 // indirect
	buf.build/go/protoyaml v0.6.0 // indirect
	cel.dev/expr v0.25.1 // indirect
	cloud.google.com/go v0.121.4 // indirect
	cloud.google.com/go/auth v0.16.4 // indirect
	cloud.google.com/go/auth/oauth2adapt v0.2.8 // indirect
	cloud.google.com/go/compute/metadata v0.9.0 // indirect
	cloud.google.com/go/iam v1.5.2 // indirect
	cloud.google.com/go/longrunning v0.6.7 // indirect
	cloud.google.com/go/monitoring v1.24.2 // indirect
	github.com/GoogleCloudPlatform/opentelemetry-operations-go/detectors/gcp v1.31.0 // indirect
	github.com/GoogleCloudPlatform/opentelemetry-operations-go/exporter/metric v0.53.0 // indirect
	github.com/GoogleCloudPlatform/opentelemetry-operations-go/internal/resourcemapping v0.53.0 // indirect
	github.com/antlr4-go/antlr/v4 v4.13.1 // indirect
	github.com/aws/aws-sdk-go-v2/aws/protocol/eventstream v1.7.6 // indirect
	github.com/aws/aws-sdk-go-v2/feature/ec2/imds v1.18.19 // indirect
	github.com/aws/aws-sdk-go-v2/internal/configsources v1.4.19 // indirect
	github.com/aws/aws-sdk-go-v2/internal/endpoints/v2 v2.7.19 // indirect
	github.com/aws/aws-sdk-go-v2/internal/ini v1.8.5 // indirect
	github.com/aws/aws-sdk-go-v2/internal/v4a v1.4.19 // indirect
	github.com/aws/aws-sdk-go-v2/service/internal/accept-encoding v1.13.6 // indirect
	github.com/aws/aws-sdk-go-v2/service/internal/checksum v1.9.11 // indirect
	github.com/aws/aws-sdk-go-v2/service/internal/presigned-url v1.13.19 // indirect
	github.com/aws/aws-sdk-go-v2/service/internal/s3shared v1.19.19 // indirect
	github.com/aws/aws-sdk-go-v2/service/signin v1.0.7 // indirect
	github.com/aws/aws-sdk-go-v2/service/sso v1.30.12 // indirect
	github.com/aws/aws-sdk-go-v2/service/ssooidc v1.35.16 // indirect
	github.com/aws/aws-sdk-go-v2/service/sts v1.41.8 // indirect
	github.com/aws/smithy-go v1.24.2 // indirect
	github.com/beorn7/perks v1.0.1 // indirect
	github.com/cespare/xxhash/v2 v2.3.0 // indirect
	github.com/cncf/xds/go v0.0.0-20251210132809-ee656c7534f5 // indirect
	github.com/dennwc/iters v1.1.0 // indirect
	github.com/dgryski/go-rendezvous v0.0.0-20200823014737-9f7001d12a5f // indirect
	github.com/envoyproxy/go-control-plane/envoy v1.36.0 // indirect
	github.com/envoyproxy/protoc-gen-validate v1.3.0 // indirect
	github.com/felixge/httpsnoop v1.0.4 // indirect
	github.com/gammazero/deque v1.1.0 // indirect
	github.com/go-audio/riff v1.0.0 // indirect
	github.com/go-jose/go-jose/v4 v4.1.3 // indirect
	github.com/go-logr/logr v1.4.3 // indirect
	github.com/go-logr/stdr v1.2.2 // indirect
	github.com/gobwas/httphead v0.1.0 // indirect
	github.com/gobwas/pool v0.2.1 // indirect
	github.com/google/cel-go v0.25.0 // indirect
	github.com/google/s2a-go v0.1.9 // indirect
	github.com/googleapis/enterprise-certificate-proxy v0.3.6 // indirect
	github.com/googleapis/gax-go/v2 v2.15.0 // indirect
	github.com/klauspost/compress v1.18.0 // indirect
	github.com/klauspost/cpuid/v2 v2.2.11 // indirect
	github.com/livekit/mageutil v0.0.0-20250511045019-0f1ff63f7731 // indirect
	github.com/livekit/psrpc v0.7.1 // indirect
	github.com/mengelbart/qlog v0.1.0 // indirect
	github.com/munnerz/goautoneg v0.0.0-20191010083416-a7dc8b61c822 // indirect
	github.com/nats-io/nats.go v1.43.0 // indirect
	github.com/nats-io/nkeys v0.4.11 // indirect
	github.com/nats-io/nuid v1.0.1 // indirect
	github.com/pion/datachannel v1.6.0 // indirect
	github.com/pion/dtls/v3 v3.1.2 // indirect
	github.com/pion/ice/v4 v4.2.1 // indirect
	github.com/pion/mdns/v2 v2.1.0 // indirect
	github.com/pion/randutil v0.1.0 // indirect
	github.com/pion/rtcp v1.2.16 // indirect
	github.com/pion/sctp v1.9.2 // indirect
	github.com/pion/srtp/v3 v3.0.10 // indirect
	github.com/pion/transport/v4 v4.0.1 // indirect
	github.com/pion/turn/v4 v4.1.4 // indirect
	github.com/planetscale/vtprotobuf v0.6.1-0.20240319094008-0393e58bdf10 // indirect
	github.com/prometheus/client_model v0.6.2 // indirect
	github.com/prometheus/common v0.66.1 // indirect
	github.com/prometheus/procfs v0.16.1 // indirect
	github.com/quic-go/qpack v0.5.1 // indirect
	github.com/redis/go-redis/v9 v9.11.0 // indirect
	github.com/spiffe/go-spiffe/v2 v2.6.0 // indirect
	github.com/stoewer/go-strcase v1.3.1 // indirect
	github.com/twitchtv/twirp v8.1.3+incompatible // indirect
	github.com/wlynxg/anet v0.0.5 // indirect
	github.com/zeebo/xxh3 v1.0.2 // indirect
	go.opentelemetry.io/auto/sdk v1.2.1 // indirect
	go.opentelemetry.io/contrib/detectors/gcp v1.39.0 // indirect
	go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc v0.61.0 // indirect
	go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp v0.61.0 // indirect
	go.opentelemetry.io/otel v1.43.0 // indirect
	go.opentelemetry.io/otel/metric v1.43.0 // indirect
	go.opentelemetry.io/otel/sdk v1.43.0 // indirect
	go.opentelemetry.io/otel/sdk/metric v1.43.0 // indirect
	go.opentelemetry.io/otel/trace v1.43.0 // indirect
	go.uber.org/mock v0.5.0 // indirect
	go.uber.org/multierr v1.11.0 // indirect
	go.yaml.in/yaml/v2 v2.4.2 // indirect
	golang.org/x/crypto v0.50.0 // indirect
	golang.org/x/exp v0.0.0-20250620022241-b7579e27df2b // indirect
	golang.org/x/mod v0.34.0 // indirect
	golang.org/x/net v0.53.0 // indirect
	golang.org/x/oauth2 v0.34.0 // indirect
	golang.org/x/sys v0.43.0 // indirect
	golang.org/x/text v0.36.0 // indirect
	golang.org/x/time v0.12.0 // indirect
	golang.org/x/tools v0.43.0 // indirect
	google.golang.org/genproto v0.0.0-20250603155806-513f23925822 // indirect
	google.golang.org/genproto/googleapis/api v0.0.0-20260427160629-7cedc36a6bc4 // indirect
	google.golang.org/genproto/googleapis/rpc v0.0.0-20260427160629-7cedc36a6bc4 // indirect
	google.golang.org/grpc v1.80.0 // indirect
)

```

## Top-level layout

- .github/ (dir, 1 files, ~128 lines)
- API.md (~5100 lines)
- asyncapi.yaml (~7205 lines)
- certs/ (dir, 1 files, ~3 lines)
- CLAUDE.md (~41 lines)
- cmd/ (dir, 5 files, ~2375 lines)
- CONFIGURATION.md (~144 lines)
- docker/ (dir, 1 files, ~77 lines)
- docker-compose.yml (~19 lines)
- Dockerfile (~21 lines)
- examples/ (dir, 13 files, ~2697 lines)
- go.mod (~148 lines)
- go.sum (~403 lines)
- internal/ (dir, 334 files, ~88096 lines)
- LICENSE (~21 lines)
- Makefile (~70 lines)
- openapi.yaml (~6745 lines)
- README.md (~521 lines)
- TESTING.md (~725 lines)
- tests/ (dir, 75 files, ~21613 lines)
- voiceblender.env.example (~276 lines)

