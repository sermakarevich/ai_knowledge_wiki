> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** StreamCore is a single Go binary owning the latency-sensitive realtime media path (WebRTC transport, turn-taking, barge-in, streaming STT/LLM/TTS, NAT traversal, sessions, events) between users and a bring-your-own agent (01-overview.md:15-16,38,40).
## Key points
- StreamCore handles the media path between users and AI — WebRTC transport, adaptive turn-taking, barge-in, streaming STT/LLM/TTS, NAT traversal, session state, and realtime events — while the agent (prompts, tools, models, business logic) stays outside it (01-overview.md:38,40).
- Transport is WebRTC audio over WHIP (RFC 9725) via one HTTP POST with no signaling socket, using Opus/RTP in both directions (01-overview.md:81).
- Connectivity is built-in Pion STUN/TURN on UDP and TCP 3478 with no external coturn, and network handovers/NAT rebinds are recovered by ICE restart on the same session (01-overview.md:82).
- Turn-taking uses adaptive VAD tracking each call's noise floor plus a debounce merging mid-sentence pauses, while barge-in ducks agent audio, filters backchannels such as "mm-hm", and cancels in-flight LLM and TTS, with a send-bounded threshold on paths without echo cancellation such as telephony (01-overview.md:83-84).
- Streaming runs STT → LLM → chunk-streaming TTS so audio starts before synthesis finishes, with server-generated session IDs, multi-peer sessions, and DataChannel events for transcript, response, state, and per-turn latency (01-overview.md:85-86).
- Reach covers browser, mobile, backend, CLI, SIP telephony, and ESP32 endpoints, and the live demo at streamcore.ai runs this repo with on-screen per-turn STT/LLM/TTS latency (01-overview.md:46,87).
- Agent integration stays outside the media path via five options — plugin/tool call, HTTP agent endpoint (`llm.provider = "agent"`), Ollama-compatible models (`llm.provider = "ollama"`), one small Go interface, or the optional built-in runtime with tools/skills/RAG/history — plus a dozen-plus providers including Deepgram, OpenAI, Cartesia, ElevenLabs, and local VibeVoice (01-overview.md:112-122).
- Honest gaps are listed as unticked: no metrics export (`/health` and timing events exist, no Prometheus/OpenTelemetry), `log.Printf` text only with no JSON `session_id` logs, no version in binary or tagged standalone binaries, single-node in-process sessions with no horizontal scaling, and no persistent memory in the built-in runtime (01-overview.md:101-106).
---
## Transport and connectivity
WebRTC audio over WHIP ([RFC 9725](https://www.rfc-editor.org/rfc/rfc9725.html)) — one HTTP POST, no signaling socket, Opus/RTP both ways (01-overview.md:81).

Built-in Pion STUN/TURN on UDP *and* TCP 3478 — no external coturn; ICE restart on the same session survives handovers/rebinds (01-overview.md:82).

| Item | Value (verbatim) |
|---|---|
| Signaling | `http://localhost:8080/whip`, server listens on `:8080` (01-overview.md:64) |
| Media | Opus/RTP both ways (01-overview.md:81) |
| NAT traversal | Built-in Pion STUN/TURN on UDP and TCP 3478 (01-overview.md:82) |
| Recovery | ICE restart on the same session; client ladder is restart-then-resume (01-overview.md:82,97) |

## Turn-taking and interruption
Adaptive VAD tracking each call's noise floor plus debounce merging mid-sentence pauses into one turn (01-overview.md:83).

Barge-in ducks agent audio, filters backchannels (`"mm-hm"`), cancels in-flight LLM and TTS on confirmed interrupt; on no-echo-cancellation paths such as telephony the threshold is bounded by what the agent just sent so it never interrupts itself (01-overview.md:84).

Telnyx STT caveat (verbatim): fronts engines behind `telnyx.transcription_engine` (default `Deepgram`); the in-house `Telnyx` engine is finals-only, so live captions show finals only and barge-in waits out the full backchannel window on VAD alone (01-overview.md:126).

## Streaming, sessions, and events
Streaming STT → streaming LLM → chunk-streaming TTS, so audio starts before synthesis finishes (01-overview.md:85).

Server-generated session IDs, multi-peer sessions, DataChannel events for transcript, response, state, and per-turn latency (01-overview.md:86).

Shipped session hardening (verbatim flags/behaviors):

| Item | Behavior |
|---|---|
| Session reconnection (server) | Dropped connection recovers on same session via ICE restart; pipeline survives (01-overview.md:95) |
| Client-driven reconnection | TypeScript, React Native, Go, Rust SDKs recover automatically: ICE restart first, then resume redial (01-overview.md:96) |
| Session resume | Redial with single-use token reattaches to running conversation; backgrounded phones rejoin same conversation (01-overview.md:97) |
| Panic recovery | Panic in one call's goroutines ends that call alone, logs stack, session reaped like any ended call (01-overview.md:98) |
| Session cap | `server.max_sessions` bounds live sessions globally; past it `POST /whip` returns 503 with `Retry-After`; resumes exempt (01-overview.md:99) |

## Quick start
Needs Go 1.25+ (or Docker) plus STT, LLM, and TTS provider keys; fully-local alternative is Ollama + VibeVoice (01-overview.md:57).

```bash
cp config.toml.example config.toml   # add your provider credentials
go run .
```

Server listens on `:8080`; clients connect to `http://localhost:8080/whip` (01-overview.md:64).

```bash
git clone https://github.com/streamcoreai/examples.git
cd examples/typescript && npm install && npm run dev
```

Browser client at [http://localhost:3000](http://localhost:3000); Docker, TURN ports, and production notes are in `docs/quickstart.md` (01-overview.md:73,75).

## Bring your own agent
Five ways, verbatim (01-overview.md:114-118):

1. **Tool call** — plugins (Python/TS/JS) or native Go tools call into your existing backend
2. **Your agent** — set `llm.provider = "agent"` and each turn is POSTed to an HTTP endpoint you host, in any language
3. **Your models** — point `llm.provider = "ollama"` at any Ollama-compatible URL you run
4. **Your code** — implement one small Go interface; the whole media path works unchanged
5. **Built in** — or use StreamCore's optional agent runtime with tools, skills, RAG, and history

Exact parameter names: `llm.provider = "agent"`, `llm.provider = "ollama"`, `openai.stt_model` (`whisper-1`, `gpt-4o-transcribe`, `gpt-4o-mini-transcribe`), `telnyx.transcription_engine` (default `Deepgram`), `server.max_sessions`, `OPENAI_API_KEY`, `STREAMCORE_JWT_SECRET` (01-overview.md:99-100,115-116,124,126).

Env-var secrets: every API key and secret can come from the environment (`OPENAI_API_KEY`, `STREAMCORE_JWT_SECRET`, …) instead of `config.toml` (01-overview.md:100).

## Docs, SDKs, contributing
| Page | What's in it (verbatim) |
|------|--------------|
| `docs/quickstart.md` | Docker, TURN ports, connecting a client, wiring your backend, fully-local setup (01-overview.md:132) |
| `docs/capabilities.md` | What the runtime does today, endpoints, AI integrations (01-overview.md:133) |
| `docs/bring-your-own-agent.md` | Five ways to own the intelligence, including the HTTP agent endpoint and the `llm.Client` interface (01-overview.md:134) |
| `docs/agent-runtime.md` | Plugins, skills, RAG, document ingestion (01-overview.md:135) |
| `docs/developer-agent.md` | Optional GitHub App and Codex integrations: CI investigation, isolated worktrees, confirmation-gated pull requests (01-overview.md:136) |
| `docs/providers.md` | Grok speech-to-speech, MiniMax, local VibeVoice, per-provider caveats (01-overview.md:137) |
| `docs/configuration.md` | Full annotated `config.toml` reference (01-overview.md:138) |
| `docs/protocol.md` | WHIP signaling, DataChannel events, auth (01-overview.md:139) |
| `docs/architecture.md` | Media flow, why Go, package layout (01-overview.md:140) |

Every SDK speaks the same WHIP + DataChannel protocol; `@streamcore/react-native-sdk` is built but not yet published to npm; plugin SDKs `@streamcore/plugin` and `streamcore-plugin` live in `plugin-sdk`, runnable apps in `examples` (01-overview.md:144,151,153).

Contributing starts at `CONTRIBUTING.md` (local run, four CI checks, care for the timing-sensitive media path); client SDKs, SIP bridge, examples, and ESP32 firmware take changes in their own repos under `streamcoreai` (01-overview.md:167,169).

Truncated in chunk, not described: the `Security` section is cut mid-link at `https://github.com/streamcor` (01-overview.md:173), so its reporting procedure is not covered here; only macro-component stub `top-level-files/` is listed (01-overview.md:177).

**Covers:** README-level repo overview (tagline, demo, quick start, capability table, gaps, BYO-agent, docs/SDK index) as given in chunks/01-overview.md; grounded in `top-level-files/` stub (01-overview.md:177)
