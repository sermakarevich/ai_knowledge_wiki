> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** A Go service that bridges SIP and WebRTC voice calls with multi-party audio mixing, a REST API, and real-time webhooks (01-overview.md:9).

## Key points
- VoiceBlender bridges SIP and WebRTC voice calls with multi-party mixing, a REST API, and real-time webhooks (01-overview.md:9).
- SIP supports inbound and outbound calls with codec negotiation (PCMU, PCMA, G.722, Opus, AMR-WB, AMR-NB), digest auth, and RFC 4028 session timers, plus optional TLS on a second port, 183 early media, and hold via re-INVITE sendonly/sendrecv (01-overview.md:15-18).
- Leg types include WebRTC via SDP offer/answer with trickle ICE, WhatsApp Business Calling over SIP-TLS + ICE/DTLS-SRTP + Opus, WebSocket legs with binary or `json_base64` framing, and experimental MoQ legs disabled by default (01-overview.md:19-22).
- Rooms mix N participants with mixed-minus-self audio at 8/16/48 kHz (default 16 kHz), support bridging two same-rate mixers with configurable direction, and per-room role-based audio routing applied atomically at leg-join time (01-overview.md:23-25).
- Media and AI surface covers RFC 4733 DTMF, T.140 RTT over RTP per RFC 4103 with RFC 2198 redundancy, stereo WAV recording with pause/resume and S3/GCS upload, WAV/MP3 playback, TTS and real-time STT from named providers, AI agents, AMD, webhooks with HMAC-SHA256 and `event_id`/`X-Event-Id`, VSI event stream at `GET /v1/vsi`, and Prometheus metrics at `GET /metrics` (01-overview.md:29-39).
- REST listens on `:8080` and SIP on `127.0.0.1:5060` by default; the HTTP surface has no credential auth and is gated solely by the `ALLOWED_IPS` allowlist and network placement (01-overview.md:52, 01-overview.md:82-90).
- Configuration is entirely via environment variables with the full reference in `CONFIGURATION.md` and an editable template at `voiceblender.env.example` (01-overview.md:64-69).

---
## Features
SIP, WebRTC, and interop legs (01-overview.md:15-22):

- **SIP inbound & outbound** — codec negotiation (PCMU, PCMA, G.722, Opus, AMR-WB, AMR-NB), digest auth, session timers (RFC 4028) (01-overview.md:15).
- **SIP over TLS** — optional TLS transport on a second port alongside UDP (01-overview.md:16).
- **Early media** — SIP 183 Session Progress with SDP for pre-answer audio (01-overview.md:17).
- **Hold/unhold** — SIP re-INVITE with sendonly/sendrecv direction (01-overview.md:18).
- **WebRTC** — browser-based voice via SDP offer/answer with trickle ICE (01-overview.md:19).
- **WhatsApp Business Calling** — inbound and outbound calls over SIP-TLS + ICE/DTLS-SRTP + Opus (01-overview.md:20).
- **WebSocket legs** — inbound (HTTP upgrade) and outbound (dial) PCM-over-WebSocket with binary or `json_base64` framing, configurable sample rate (8/16/24/48 kHz), bidirectional text, caller-supplied X-/P- headers (01-overview.md:21).
- **MoQ legs (experimental, PoC)** — inbound Media-over-QUIC over WebTransport/HTTP/3 with Opus one frame per MoQ Object; tracks `mengelbart/moqtransport` (IETF draft-11); disabled by default; enable with `MOQ_ENABLED=true` + `MOQ_TLS_CERT_FILE` / `MOQ_TLS_KEY_FILE` (01-overview.md:22).

Rooms, recording, and AI (01-overview.md:23-39):

- **Multi-party rooms** — mix N participants with mixed-minus-self audio at 8 kHz, 16 kHz, or 48 kHz per room; default 16 kHz (01-overview.md:23).
- **Room bridging** — join two rooms' mixers (same sample rate) with live-configurable direction (bidirectional, one-way each way, or parked) (01-overview.md:24).
- **Audio routing matrix** — free-form `role` tags plus a who-hears-whom matrix by role, applied atomically at leg-join time; see `API.md#audio-routing-matrix` (01-overview.md:25).
- **Multi-stream SIP calls** — several `m=audio` sections in one dialog (RFC 3264) with per-section RTP port, direction, language, mixer room; follows SIPREC RFC 7866 wire profile; see `API.md#per-leg-audio-streams-multiple-maudio-lines` (01-overview.md:26).
- **SIPREC recording server/client** — server answers multipart `SDP` + `rs-metadata` INVITEs receive-only, binds sections to named participants, reports `a=label` mismatches in `warnings` on `GET /v1/legs/{id}/siprec`; client forks room participants via `POST /v1/rooms/{id}/siprec`; disabled by default, enable with `SIPREC_ENABLED=true` (needs `SIP_TCP_ENABLED=true`); client needs `SIPREC_SRC_ENABLED=true` (01-overview.md:27).
- **DTMF** — send and receive RFC 4733 telephone-events (01-overview.md:29).
- **Real-Time Text (RTT)** — ITU-T T.140 over RTP per RFC 4103 with RFC 2198 redundancy (01-overview.md:30).
- **Recording** — stereo WAV per-leg or per-room, multi-channel per-participant tracks, pause/resume writing silence, optional S3 or Google Cloud Storage upload (01-overview.md:31).
- **Playback** — WAV/MP3 audio or built-in telephone tones into legs or rooms (01-overview.md:32).
- **TTS** — into legs or rooms (ElevenLabs, Google Cloud, AWS Polly, Deepgram, Azure) with preflight staging: synthesize speculatively, then commit or discard (01-overview.md:33).
- **STT** — real-time with partial transcripts (ElevenLabs, Deepgram, Deepgram Flux, Azure, Speechmatics); Flux adds `stt.turn` turn detection (01-overview.md:34).
- **AI Agent** — attach to leg or room (ElevenLabs, VAPI, Pipecat, Deepgram) with mid-session context injection (01-overview.md:35).
- **AMD** — classify answerer as human, machine, no-speech, or not-sure; optional voicemail beep detection via Goertzel analysis (01-overview.md:36).
- **Webhooks** — HMAC-SHA256 signing and retry; stable per-event `event_id` also sent as `X-Event-Id`; typed data with CDR-style `leg.disconnected` (01-overview.md:37).
- **WebSocket event stream (VSI)** — `GET /v1/vsi` streams all events and accepts commands (mute, hold, DTMF, room management); filter by `app_id` regex (01-overview.md:38).
- **Prometheus metrics** — at `GET /metrics` (active legs/rooms, call durations, disconnect reasons, event-egress counters, Go runtime); pprof at `/debug/pprof/` when built with `-tags pprof` (01-overview.md:39).

## Quick Start and multi-instance cluster
Verbatim build and run (01-overview.md:45-50):

```bash
# Build and run
go build -o voiceblender ./cmd/voiceblender
./voiceblender

# Or run directly
go run ./cmd/voiceblender
```

| Setting | Value (01-overview.md:52) |
|---|---|
| REST API | `:8080` by default |
| SIP | `127.0.0.1:5060` by default |

Multi-instance cluster via `docker/docker-compose.cluster.yml` with two containers (`dialer` on host port 8080, `peer` on 8081) sharing `voiceblender.env` (01-overview.md:56-57):

```bash
docker compose -f docker/docker-compose.cluster.yml up --build
```

## Configuration and links
- All configuration is via environment variables; full reference in `CONFIGURATION.md` including S3 bucket preflight rules (01-overview.md:64-66).
- Ready-to-edit template: `voiceblender.env.example` (01-overview.md:68-69).
- Online documentation: `https://voiceblender.org/docs/` (01-overview.md:71).
- Website `voiceblender.org` and documentation `voiceblender.org/docs` (01-overview.md:75-76).

| Flag / variable | Behaviour in this chunk |
|---|---|
| `MOQ_ENABLED=true` + `MOQ_TLS_CERT_FILE` / `MOQ_TLS_KEY_FILE` | Enables experimental MoQ legs (01-overview.md:22) |
| `SIPREC_ENABLED=true` (needs `SIP_TCP_ENABLED=true`) | Enables SIPREC recording server (01-overview.md:27) |
| `SIPREC_SRC_ENABLED=true` | Enables SIPREC recording client for `POST /v1/rooms/{id}/siprec` (01-overview.md:27) |
| `ALLOWED_IPS` | Sole gate for the HTTP surface; no API key/bearer/session (01-overview.md:82-90) |
| `WEBHOOK_SECRET` | Signs outbound webhooks, distinct from HTTP-surface auth (01-overview.md:88-90) |

## API overview — auth, legs, rooms
API authentication: the HTTP surface — REST, `/v1/vsi`, `/v1/legs/websocket`, `/v1/legs/moq`, `/metrics`, pprof — has no built-in credential authentication; access is gated solely by `ALLOWED_IPS` and network placement; front with a reverse proxy for per-caller credentials; distinct from SIP digest auth and `WEBHOOK_SECRET` webhook signing (01-overview.md:82-90). Full reference: `API.md` (01-overview.md:80).

Legs endpoints verbatim (01-overview.md:94-136):

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
```

Rooms endpoints as captured (01-overview.md:141-162; truncated at `POST /v1/r`):

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
```

Truncation note: the chunk ends mid-line at `POST /v1/r` (01-overview.md:162) and the macro-components list is cut after `top-level-files/` (01-overview.md:164-166); contents beyond those cut points are not described here.

**Covers:** README content (definition, features, quick start, configuration, links), API overview (auth, legs, rooms as captured), `CONFIGURATION.md`, `API.md`, `voiceblender.env.example`, `cmd/voiceblender`, `docker/docker-compose.cluster.yml`
