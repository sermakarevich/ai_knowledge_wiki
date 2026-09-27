# Technical Analysis: streamcoreai/streamcore-server

**Repository:** https://github.com/streamcoreai/streamcore-server
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Realtime voice AI requires a latency-sensitive media path — WebRTC transport, NAT traversal, voice activity detection, turn-taking, barge-in, streaming speech-to-text / language-model / text-to-speech, session supervision, and per-turn latency events — kept separate from agent intelligence (prompts, tools, models, business logic). Most application teams do not want to build this path from WebRTC, RTP, and provider streaming APIs.

The repo addresses it with a single Go binary that owns the media path and exposes it over WHIP (RFC 9725) plus DataChannel events, while the agent stays outside via plugin/tool call, HTTP agent endpoint, Ollama-compatible models, a Go interface, or an optional built-in runtime (01-overview.md:38,40,01-overview.md:112-122). Transport is one HTTP POST to `/whip` with Opus/RTP both ways and no signaling socket; connectivity uses built-in Pion STUN/TURN on UDP and TCP 3478 (01-overview.md:81-82). Turn-taking uses adaptive per-call VAD plus debounce; barge-in ducks agent audio, filters backchannels, and cancels in-flight LLM/TTS (01-overview.md:83-84). Streaming runs STT → LLM → chunk-streaming TTS so playout starts before synthesis finishes, with server-generated session IDs, multi-peer sessions, and transcript/response/state/latency events (01-overview.md:85-86).

The primary user is an application developer adding voice to an existing agent or backend across browser, mobile, backend, CLI, SIP telephony, and ESP32 endpoints (01-overview.md:46,87).

## 2. High-Level Architecture

```
Clients (browser / mobile / CLI / SIP / ESP32)
  │  WHIP POST http://localhost:8080/whip, Opus/RTP
  ▼
Public mux :8080 ── /whip, /whip/, /health ("ok"), /token (if jwt_secret set)
  │  JWT HMAC-SHA256 Bearer (optional) + CORS; pprof on separate debug mux
  ▼
Session Manager (in-process sessions, reaper, max_sessions cap, resume tokens)
  │  ┌───────────┴────────────┐
  ▼  ▼                        ▼
STT ─► LLM ─► TTS (chunk streaming)   Built-in Pion STUN/TURN (UDP+TCP 3478)
  │                                    ▲
  ▼                                    │
DataChannel events ◄───────────────────┘
(transcript / response / state / per-turn latency)
  │
  ▼
BYO-agent + plugins + RAG client (outside media path)
```

Data flow:

1. Client POSTs SDP to `/whip` on `:8080`; optional JWT `sub` becomes caller identity; server creates a server-generated session ID and attaches the peer (02-top-level-files.md:559-562,02-top-level-files.md:780-813,01-overview.md:64,86).
2. Audio flows as Opus/RTP both ways; built-in TURN relays where direct NAT traversal fails; ICE restart on the same session survives handovers and NAT rebinds (01-overview.md:81-82,01-overview.md:95).
3. Inbound audio passes adaptive VAD and debounce into one turn; confirmed barge-in ducks agent audio and cancels in-flight LLM/TTS (01-overview.md:83-84).
4. The turn streams STT → streaming LLM → chunk-streaming TTS so audio starts before synthesis completes; transcript, response, state, and per-turn STT/LLM/TTS latency are emitted on the DataChannel (01-overview.md:85-86,01-overview.md:46).
5. Session manager supervises lifetime: reaper, panic isolation per call, `server.max_sessions` cap (`503` + `Retry-After` past cap, resumes exempt), single-use resume tokens for redial reattach (01-overview.md:95-99).
6. Shutdown is ordered: plugins first, then `sm.CloseAll()`, then HTTP and debug shutdowns under a 5 s context with a 5 s force-exit watchdog (02-top-level-files.md:596-620).

Persistent state lives in-process only: live session objects supervised by the session manager. There is no database, no horizontal session store, and no persistent memory in the built-in runtime (01-overview.md:101-106). Durable local inputs are `config.toml` (gitignored; `config.toml.example` is the tracked schema) and the `./plugins` directory; secrets can come from the environment instead of the file (01-overview.md:100,02-top-level-files.md:21-79).

## 3. Sessions and the Media Path — The Core Abstraction

The central concept is the **session**: a server-owned, single-node conversation object binding one or more WebRTC peers, the STT → LLM → TTS pipeline instance, TURN/ICE state, and the event stream for that call.

Representation: server-generated session IDs; multi-peer sessions; per-call VAD noise-floor state; resume via single-use token redial; global bound via `server.max_sessions` (01-overview.md:85-86,01-overview.md:99,01-overview.md:97).

Named kinds and behaviors with sources:

- `session.NewManager(cfg, pluginMgr, ragClient)` — constructed in `main.go` after config, plugins, and RAG client (02-top-level-files.md:510-588).
- `signaling.NewWHIPHandler(sm)` — WHIP endpoint bound to the manager; routes `/whip` and `/whip/` (02-top-level-files.md:510-588,02-top-level-files.md:623-635).
- `signaling.WithResourceID` — carries validated JWT `sub` as caller identity into signaling (02-top-level-files.md:780-813).
- `turnserver.Start(publicIP, turnSecret)` — built-in relay, started only when both `server.public_ip` and `server.turn_secret` are set (02-top-level-files.md:548).
- `plugin.NewManager(directory)` + `SetPluginSettings` + `LoadAll` — plugin host attached to sessions (02-top-level-files.md:510-588).
- `rag.NewClient(cfg)` — retrieval client passed into the session manager (02-top-level-files.md:510-588).

Key queries are HTTP/DataChannel operations, not SQL. Verbatim surface:

```go
mux.HandleFunc("/whip", whipHandler)
mux.HandleFunc("/whip/", whipHandler)
mux.HandleFunc("/health", ...) // writes "ok", StatusOK
if issueToken != nil {
    mux.HandleFunc("/token", issueToken)
}
```

Source: `main.go` via (02-top-level-files.md:623-635). Session-relevant config keys: `server.session_grace_ms = 30000`, `server.max_sessions = 0` (unlimited), `server.public_ip`, `server.turn_secret` (02-top-level-files.md:155-172).

## 4. LLM / External Service Integration

The repo calls external AI providers for every pipeline stage; there is no offline default except an explicitly configured fully-local setup.

Providers named in the analyzed pages: Deepgram (STT and TTS), OpenAI (LLM and STT), Cartesia (TTS), ElevenLabs (TTS), Ollama-compatible models, xAI Grok speech-to-speech (`[realtime] provider = "grok"`), local VibeVoice, Telnyx (SIP/STT front), MiniMax, plus a generic HTTP agent endpoint and native Go tools (01-overview.md:112-122,02-top-level-files.md:261-271,02-top-level-files.md:89-148,02-top-level-files.md:137).

Required vs optional calls:

- Required per turn in classic mode: one STT provider, one LLM provider, one TTS provider (defaults in example: `[stt] provider = "deepgram"`, `[llm] provider = "openai"`, `[tts] provider = "cartesia"`) (02-top-level-files.md:261-271).
- Required in realtime mode: one speech-to-speech provider (`grok`, model `grok-voice-latest`, voice `eve`) (02-top-level-files.md:195-243,02-top-level-files.md:89-148).
- Optional: HTTP agent endpoint (`llm.provider = "agent"`), Ollama bridge (`llm.provider = "ollama"`), RAG client, plugin backends, Telnyx transcription engine selection (01-overview.md:114-118,02-top-level-files.md:261-271).
- Known per-provider caveat: Telnyx fronts engines behind `telnyx.transcription_engine` (default `Deepgram`); the in-house `Telnyx` engine is finals-only, so live captions show finals only and barge-in waits the full backchannel window on VAD alone (01-overview.md:126). No OpenAI TTS provider exists; Deepgram covers STT+TTS in the classic pipeline (02-top-level-files.md:89-148).

Env vars: every API key and secret can come from the environment instead of `config.toml`, including `OPENAI_API_KEY` and `STREAMCORE_JWT_SECRET` (01-overview.md:100). Exact parameter names cited: `llm.provider = "agent"`, `llm.provider = "ollama"`, `openai.stt_model` (`whisper-1`, `gpt-4o-transcribe`, `gpt-4o-mini-transcribe`), `telnyx.transcription_engine`, `server.max_sessions`, `OPENAI_API_KEY`, `STREAMCORE_JWT_SECRET` (01-overview.md:99-100,115-116,124,126).

## 5. Streaming Voice Pipeline (STT → LLM → TTS with Barge-In) — The Main Pipeline

Primary workflow is the per-turn streaming voice loop plus the process boot that hosts it. Available pages describe boot exactly and pipeline behavior at overview level; per-stage function bodies are not in the two analyzed wiki pages.

1. `config.Load("")` — load `config.toml` / environment into `cfg` (`main.go` via 02-top-level-files.md:510-588).
2. `startDebugServer(cfg.Debug)` — start separate pprof mux when `debug.bind` is set; apply block/mutex profile rates; never on the public mux (`main.go` via 02-top-level-files.md:647-700,02-top-level-files.md:623-645).
3. `plugin.NewManager(cfg.Plugins.Directory)` → `SetPluginSettings(pluginSettings(cfg))` → `LoadAll(context.Background())` — discover plugins with merged `[plugins.config.*]` plus legacy `[display]`/`[github]`/`[codex]` settings (`main.go` via 02-top-level-files.md:510-588,02-top-level-files.md:822-849).
4. `rag.NewClient(cfg)` — build retrieval client passed to sessions (`main.go` via 02-top-level-files.md:510-588).
5. `turnserver.Start(cfg.Server.PublicIP, cfg.Server.TurnSecret)` — start built-in STUN/TURN only under `if cfg.Server.PublicIP != "" && cfg.Server.TurnSecret != ""` (`main.go` via 02-top-level-files.md:548).
6. `session.NewManager(cfg, pluginMgr, ragClient)` → `signaling.NewWHIPHandler(sm)` — create session supervisor and bind WHIP handler (`main.go` via 02-top-level-files.md:510-588).
7. Serve public mux (`/whip`, `/whip/`, `/health`, conditional `/token`) with optional `jwtMiddleware` and CORS; run session reaper; on shutdown close plugins first, then `sm.CloseAll()`, then HTTP/debug servers (`main.go` via 02-top-level-files.md:559-562,02-top-level-files.md:623-635,02-top-level-files.md:702-717,02-top-level-files.md:596-620).
8. Per-turn media loop (overview-level): adaptive VAD segments caller speech → streaming STT emits partials/finals → streaming LLM generates tokens → chunk-streaming TTS synthesizes and plays before synthesis finishes → DataChannel emits transcript, response, state, per-turn latency (01-overview.md:83-86).
9. Interruption path: barge-in ducks agent audio, filters backchannels such as `"mm-hm"`, cancels in-flight LLM and TTS; on paths without echo cancellation (e.g. telephony) the threshold is send-bounded so the agent never interrupts itself (01-overview.md:84).

Pipeline timing defaults from the example: `pipeline.barge_in = true`, `user_speech_quiet_ms = 600`, `turn_merge_ms = 350`; Deepgram `endpointing = "300"`, `utterance_end_ms = "1000"` (02-top-level-files.md:195-243,02-top-level-files.md:276-338).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `main.go` | boot + handlers (see 02-top-level-files.md:510-621) | Loads config, starts debug server, plugin manager, RAG, TURN, session manager, WHIP mux, reaper, graceful shutdown |
| `main_test.go` | 434 | Tests `/token` minting, JWT middleware identity, debug mux isolation, legacy config mapping (02-top-level-files.md:875-921,02-top-level-files.md:986-1179) |
| `config.toml.example` | 311 | Annotated schema: `[server]`, `[debug]`, `[plugins]`, `[pipeline]`, `[realtime]`/`[stt]`/`[llm]`/`[tts]`, per-provider credentials (02-top-level-files.md:150-232) |
| `go.sum` | 129 | Pinned module hashes for media/auth/config stack (02-top-level-files.md:347-478) |
| `AGENTS.md` | 57 | Contributor/agent rules: read order, module path, `:8080` + `/whip`, speech-to-speech default, JWT and session notes (02-top-level-files.md:89-148) |
| `README.zh-CN.md` | 193 | Chinese mirror of README: positioning, quickstart, capabilities, gaps, BYO-agent, docs/SDK index (02-top-level-files.md:1225-1420) |
| `SECURITY.md` | 103 | Private-report policy, timelines, in/out of scope, deploy rules (02-top-level-files.md:1422-1527) |
| `docs/quickstart.md` | indexed | Docker, TURN ports, client connection, backend wiring, fully-local setup (01-overview.md:132) |
| `docs/capabilities.md` | indexed | Runtime capabilities, endpoints, AI integrations (01-overview.md:133) |
| `docs/bring-your-own-agent.md` | indexed | Five agent-integration paths incl. HTTP endpoint and `llm.Client` (01-overview.md:134) |
| `docs/agent-runtime.md` | indexed | Built-in runtime: plugins, skills, RAG, ingestion (01-overview.md:135) |
| `docs/providers.md` | indexed | Grok speech-to-speech, MiniMax, VibeVoice, per-provider caveats (01-overview.md:137) |
| `docs/configuration.md` | indexed | Full annotated `config.toml` reference (01-overview.md:138) |
| `docs/protocol.md` | indexed | WHIP signaling, DataChannel events, auth (01-overview.md:139) |
| `docs/architecture.md` | indexed | Media flow, language choice, package layout (01-overview.md:140) |
| `docs/developer-agent.md` | indexed | Optional GitHub App and Codex integrations (01-overview.md:136) |

Only the first seven files have line counts in the analyzed pages; docs rows are index entries without counts. `go.mod`, package sources, and chunk-truncated config sections after `[ollama]` are not covered by the two analyzed pages (02-top-level-files.md:344).

## 7. Dependencies

| Package | Version constraint | Purpose |
|---|---|---|
| `github.com/pion/webrtc/v4` | `v4.2.18` | WebRTC transport, RTP, ICE (02-top-level-files.md:435) |
| `github.com/golang-jwt/jwt/v5` | `v5.3.1` | HS256 Bearer auth on `/whip`, `/token` minting (02-top-level-files.md:369) |
| `github.com/BurntSushi/toml` | `v1.6.0` | `config.toml` parsing (02-top-level-files.md:350) |
| `github.com/ollama/ollama` | `v0.20.3` | Ollama-compatible model bridge (02-top-level-files.md:401) |
| `github.com/sashabaranov/go-openai` | `v1.36.1` | OpenAI LLM/STT client (02-top-level-files.md:441) |
| `github.com/tetratelabs/wazero` | `v1.9.0` | Plugin sandbox runtime (02-top-level-files.md:448) |
| `golang.org/x/crypto` | `v0.48.0` | Crypto primitives (02-top-level-files.md:454) |

All rows are required pins from `go.sum` as reported in the analyzed pages; transitive provider SDKs, Pion subpackages, and remaining `go.mod` constraints are not enumerated in the two analyzed pages. Hygiene keeps `config.toml`, `.env*`, build output, and `node_modules/` out of git; `.gitmodules` mounts only the `examples` submodule (02-top-level-files.md:21-87).

## 8. CLI / Usage Surface

Entry points: `cp config.toml.example config.toml`, then `go run .` (or Docker); server listens on `:8080`; clients connect to `http://localhost:8080/whip`; example browser client via `examples/typescript` on `:3000` (01-overview.md:57,64,73,75,02-top-level-files.md:89-148). Go 1.25+ plus STT/LLM/TTS keys required; fully-local alternative is Ollama + VibeVoice (01-overview.md:57).

Commands:

| Command | Effect |
|---|---|
| `cp config.toml.example config.toml` | Create local config for credentials (01-overview.md:51) |
| `go run .` | Start server on `:8080` (01-overview.md:52) |
| `git clone https://github.com/streamcoreai/examples.git; cd examples/typescript && npm install && npm run dev` | Run browser client on `:3000` (01-overview.md:59-62) |

HTTP surface:

| Endpoint | Behavior |
|---|---|
| `POST /whip`, `POST /whip/` | WHIP offer; `503` + `Retry-After` past `max_sessions`; JWT-gated only when `server.jwt_secret` set (01-overview.md:64,99,02-top-level-files.md:623-635) |
| `GET /health` | Returns `ok`, `200` (02-top-level-files.md:623-635) |
| `POST /token` | Mints 1 h HS256 JWT; only registered when `server.jwt_secret` set; `405` unless POST (02-top-level-files.md:623-635,02-top-level-files.md:727-772) |

Env vars (secrets may come from environment instead of `config.toml`):

| Variable | Purpose |
|---|---|
| `OPENAI_API_KEY` | OpenAI credential (01-overview.md:100) |
| `STREAMCORE_JWT_SECRET` | JWT HMAC secret (01-overview.md:100) |

Selected config keys:

| Key | Default / meaning |
|---|---|
| `server.port` | `"8080"` (02-top-level-files.md:156) |
| `server.public_ip` / `server.turn_secret` | `""` / `""`; TURN starts only when both set (02-top-level-files.md:157-158,548) |
| `server.jwt_secret` / `server.api_key` | `""` / `""`; JWT off by default (02-top-level-files.md:159-160) |
| `server.session_grace_ms` | `30000` (02-top-level-files.md:161) |
| `server.max_sessions` | `0` = unlimited (02-top-level-files.md:162) |
| `debug.bind` / `debug.allow_public` | `""` / `false` (02-top-level-files.md:165-166) |
| `plugins.directory` | `"./plugins"` (02-top-level-files.md:171) |
| `[realtime].provider` | `""` = classic pipeline; `grok` supported (02-top-level-files.md:261-262) |
| `[stt].provider` | `"deepgram"` (02-top-level-files.md:264-265) |
| `[llm].provider` | `"openai"` (`agent` and `ollama` also supported) (02-top-level-files.md:267-268,01-overview.md:114-118) |
| `[tts].provider` | `"cartesia"` (02-top-level-files.md:270-271) |

SDK note: TypeScript, React Native, Go, and Rust SDKs recover via ICE-restart-then-resume; `@streamcore/react-native-sdk` was built but unpublished; plugin SDKs `@streamcore/plugin` and `streamcore-plugin` live in `plugin-sdk` (01-overview.md:96,01-overview.md:144,153).

## 9. Extensibility Points

- **External agent over HTTP:** set `llm.provider = "agent"`; each turn is POSTed to a self-hosted endpoint in any language (01-overview.md:114-118).
- **Ollama-compatible models:** set `llm.provider = "ollama"` against a self-run URL (default `http://localhost:11434`) (01-overview.md:114-118,02-top-level-files.md:195-243).
- **Native Go agent:** implement the small `llm.Client` interface documented in `docs/bring-your-own-agent.md`; media path works unchanged (01-overview.md:114-118,01-overview.md:134).
- **Tool/plugin calls:** Python/TS/JS plugins via `plugin-sdk` (`@streamcore/plugin`, `streamcore-plugin`) or native Go tools calling into an existing backend; discovered from `plugins.directory` via `plugin.NewManager` + `LoadAll`; per-plugin settings under `[plugins.config.<name>]`, with legacy `[display]`/`[github]`/`[codex]` folded in (01-overview.md:114-118,02-top-level-files.md:510-588,02-top-level-files.md:822-849).
- **Built-in agent runtime:** optional tools, skills, RAG, document ingestion, and history per `docs/agent-runtime.md` (01-overview.md:114-118,01-overview.md:135).
- **Realtime provider switch:** `[realtime] provider = "grok"` selects speech-to-speech instead of the classic pipeline (02-top-level-files.md:261-262,02-top-level-files.md:89-148).
- **Client stacks and bridges:** WHIP + DataChannel protocol shared by all SDKs; SIP bridge, examples, and ESP32 firmware accept changes in their own repos under `streamcoreai` (01-overview.md:144,01-overview.md:167,169).

## 10. Limitations and Gotchas

- **No metrics export:** `/health` and DataChannel timing events exist, but there is no Prometheus/OpenTelemetry output; per-turn latency is visible on screen, not scrapable (01-overview.md:101-106).
- **Text-only unstructured logs:** `log.Printf` output with no JSON or `session_id` correlation, complicating per-call diagnosis (01-overview.md:101-106).
- **Single-node sessions with no horizontal scaling:** sessions are in-process; `server.max_sessions` bounds one host and there is no shared session store (01-overview.md:99,101-106).
- **No version in binary or tagged standalone binaries:** provenance and rollback depend on container or checkout rather than `version` output (01-overview.md:101-106).
- **No persistent memory in the built-in runtime:** history does not survive beyond the running session without an external agent store (01-overview.md:101-106).
- **Telnyx in-house engine is finals-only:** live captions show finals only and barge-in falls back to the full backchannel window on VAD alone; set `telnyx.transcription_engine` to `Deepgram` (the default) for partials (01-overview.md:126).
- **Restart after adding plugins and JWT-off-by-default:** newly added plugins require a restart to be discovered, and `/whip` is unauthenticated until `server.jwt_secret` is set (02-top-level-files.md:89-148,02-top-level-files.md:559-562).

## 11. How It Compares to Alternatives

- **LiveKit (Agents + WebRTC SFU):** full SFU with rooms, forwarding, and recording plus an agents framework; StreamCore is narrower — one binary owning a single-call WHIP voice path with built-in TURN and no room primitive in the analyzed pages.
- **Daily (Bots / Pipecat Cloud):** hosted realtime voice platform with managed transport and integrations; StreamCore is self-hosted Go with bring-your-own agent and keys.
- **Twilio Voice / Media Streams + SIP:** carrier telephony with media forking and a large compliance footprint; StreamCore reaches SIP/ESP32 but centers on WebRTC WHIP with optional Telnyx bridging rather than a carrier network.
- **Pipecat (open-source voice pipeline framework):** composable pipeline blocks the developer wires together; StreamCore ships the opinionated STT → LLM → TTS loop, VAD/debounce/barge-in, and session supervision as a running server.

Positioning: StreamCore competes as a self-hosted, single-binary WebRTC voice-path server for teams that already own an agent and want transport, turn-taking, streaming synthesis, and session hardening without adopting an SFU, a carrier, or a pipeline framework.

## Appendix: Selected Code Snippets

1. Boot sequence, `main.go` (via 02-top-level-files.md:510-588):

```go
cfg, err := config.Load("")
debugSrv, err := startDebugServer(cfg.Debug)
pluginMgr := plugin.NewManager(cfg.Plugins.Directory)
pluginMgr.SetPluginSettings(pluginSettings(cfg))
pluginMgr.LoadAll(context.Background())
ragClient, err := rag.NewClient(cfg)
turnSrv, err := turnserver.Start(cfg.Server.PublicIP, cfg.Server.TurnSecret) // only when both set
sm := session.NewManager(cfg, pluginMgr, ragClient)
whipHandler := signaling.NewWHIPHandler(sm)
```

2. Public mux routes, `main.go` (via 02-top-level-files.md:623-635):

```go
mux.HandleFunc("/whip", whipHandler)
mux.HandleFunc("/whip/", whipHandler)
mux.HandleFunc("/health", ...) // writes "ok", StatusOK
if issueToken != nil {
    mux.HandleFunc("/token", issueToken)
}
```

3. Minimal run, shell (via 01-overview.md:51-56):

```bash
cp config.toml.example config.toml   # add your provider credentials
go run .
```

Server listens on `:8080`; clients connect to `http://localhost:8080/whip`.
