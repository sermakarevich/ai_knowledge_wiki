> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-level files
**In one sentence:** The repo root is a single Go binary (`main.go`) that loads `config.toml`, starts an optional pprof debug server, discovers plugins, opens the public `/whip` + `/token` + `/health` surface with JWT/CORS, and supervises sessions, RAG, TURN, and shutdown — surrounded by config example, agent guide, ignore rules, pinned `go.sum`, tests, a Chinese README mirror, and a security policy (02-top-level-files.md:510-621).
## Key points
- `main()` boots in one order: `config.Load("")`, `startDebugServer`, provider log line, plugin manager with settings before discovery, RAG client, built-in STUN/TURN only when `public_ip` + `turn_secret` are set, session manager, WHIP handler with optional JWT, CORS mux, `:port` listener, reaper, then graceful shutdown with plugins-first ordering and a 5 s force-exit net (02-top-level-files.md:510-621).
- The public surface is exactly `/whip`, `/whip/`, `/health` returning `ok`, and `/token` only when `server.jwt_secret` is set; pprof is never on the public mux (proven by a 404 test) and lives on a separate debug mux (02-top-level-files.md:623-645,02-top-level-files.md:986-996).
- Auth is JWT HMAC-SHA256 Bearer on `/whip` with CORS preflight exempted and the `sub` claim forwarded as caller identity via `signaling.WithResourceID`, while `POST /token` mints 1-hour tokens with optional `{"resource_id": "..."}` → `sub`, optional `Authorization: Bearer <apiKey>` gate, and bodies capped at 4096 bytes with missing/unparseable bodies accepted (02-top-level-files.md:727-813).
- The optional debug server is off when `debug.bind` is empty (profiling rates then only warn), rejects negative rates and non-loopback binds without `allow_public`, applies `runtime.SetBlockProfileRate` / `SetMutexProfileFraction`, uses a 5 s `ReadHeaderTimeout`, and a dead pprof listener only logs and continues instead of `log.Fatalf`-ing the media pipeline (02-top-level-files.md:647-700).
- `config.toml.example` (311 lines) is the full annotated schema: `[server]` ports/secrets/caps, `[debug]`, `[plugins]`, legacy `[display]`/`[github]`/`[codex]`, `[pipeline]` timing, `[realtime]`/`[stt]`/`[llm]`/`[tts]` provider switch, and per-provider credential sections — and `pluginSettings` folds legacy `[display]`/`[github]`/`[codex]` into plugin settings with explicit `[plugins.config.<name>]` always winning (02-top-level-files.md:150-232,02-top-level-files.md:822-830).
- `AGENTS.md` forbids writing StreamCore code/config from memory, pins the module path `github.com/streamcoreai/streamcore-server`, defaults simplest setup to speech-to-speech (`[realtime] provider = "grok"`), and records easy-to-miss facts: `:8080` + `/whip`, `events` DataChannel before the SDP offer, 30 sessions/min/IP `429`, JWT-off-by-default with `POST /token`, restart-after-adding-plugins (02-top-level-files.md:89-148).
- `go.sum` (129 lines) pins the media/auth/config stack including `pion/webrtc/v4 v4.2.18`, `golang-jwt/jwt/v5 v5.3.1`, `BurntSushi/toml v1.6.0`, `ollama v0.20.3`, and `wazero v1.9.0`; hygiene files keep secrets/build output out of git and Docker (`config.toml`, `.env*`, `*.tfstate`, `node_modules/`, Go artifacts) and `.gitmodules` mounts only the `examples` submodule (02-top-level-files.md:347-478,02-top-level-files.md:21-87).
---
## Entrypoint and HTTP surface (`main.go`)
Boot sequence, verbatim (02-top-level-files.md:510-588):

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

TURN starts only under `if cfg.Server.PublicIP != "" && cfg.Server.TurnSecret != ""` (02-top-level-files.md:548). Realtime mode logs `speech-to-speech: %s (model: %s, voice: %s)`; classic mode logs `STT: %s, LLM: %s, TTS: %s` (02-top-level-files.md:520-527). Shutdown order is plugins first, then `sm.CloseAll()`, then HTTP + debug shutdowns under a 5 s context with a parallel 5 s force-exit watchdog (02-top-level-files.md:596-620).

Public mux, verbatim routes (02-top-level-files.md:623-635):

```go
mux.HandleFunc("/whip", whipHandler)
mux.HandleFunc("/whip/", whipHandler)
mux.HandleFunc("/health", ...) // writes "ok", StatusOK
if issueToken != nil {
    mux.HandleFunc("/token", issueToken)
}
```

CORS sets `Access-Control-Allow-Origin: *`, methods `GET, POST, PATCH, DELETE, OPTIONS`, headers `Content-Type, Authorization, If-Match`, exposes `Location, ETag, Accept-Patch, X-Resume-Token, X-Resume-Status`, and answers `OPTIONS` with `204` (02-top-level-files.md:702-717).

## Auth: JWT middleware and `/token` (`main.go`)
`tokenHandler(secret, apiKey)` issues HS256 JWTs with `iat` and `exp = now + 1h`; a trimmed non-empty `resource_id` from a ≤4096-byte body becomes `sub`, otherwise no identity claim; an empty/missing/unparseable body is not an error; a configured `apiKey` requires `Authorization: Bearer <apiKey>` or `401` (02-top-level-files.md:727-772). `jwtMiddleware(secret, next)` lets `OPTIONS` through, demands `Authorization: Bearer …`, rejects wrong-signature tokens with `401` before reading claims, and forwards a valid `sub` via `signaling.WithResourceID` (02-top-level-files.md:780-813).

| Handler | Exact behavior |
|---|---|
| `POST /token` | `405` unless POST; `401` on bad API key; `200` `{"token": "<jwt>"}` (02-top-level-files.md:727-772) |
| `/whip` wrapper | Applied only when `server.jwt_secret != ""`; preflight exempt; `401` on missing/malformed/invalid token (02-top-level-files.md:559-562,02-top-level-files.md:780-813) |

## Debug / pprof server (`main.go`)
`startDebugServer(cfg config.DebugConfig)`: empty `Bind` returns `(nil, nil)` plus a `debug.bind is empty` warning when profiling rates are set; negative `block_profile_rate` / `mutex_profile_fraction` error; binds via `net.Listen("tcp", cfg.Bind)`; non-loopback bind without `allow_public` errors with `set debug.allow_public = true` guidance; then sets `runtime` profile rates and serves `newDebugMux()` with `ReadHeaderTimeout: 5s` (02-top-level-files.md:647-683). `newDebugMux()` registers `/debug/pprof/`, `/debug/pprof/cmdline`, `/debug/pprof/profile`, `/debug/pprof/symbol`, `/debug/pprof/trace` (02-top-level-files.md:637-645). `serveDebug` only logs `debug server error: %v; continuing without pprof` so a dead profiling socket never drops live WebRTC calls (02-top-level-files.md:695-700).

## Configuration reference (`config.toml.example`, 311 lines)
Core `[server]` / `[debug]` / `[plugins]` values, verbatim names (02-top-level-files.md:155-172):

| Key | Default in example |
|---|---|
| `server.port` | `"8080"` (02-top-level-files.md:156) |
| `server.public_ip` / `server.turn_secret` | `""` / `""` (02-top-level-files.md:157-158) |
| `server.jwt_secret` / `server.api_key` | `""` / `""` (02-top-level-files.md:159-160) |
| `server.session_grace_ms` | `30000` (02-top-level-files.md:161) |
| `server.max_sessions` | `0` = unlimited; past cap `POST /whip` → `503` + `Retry-After` (02-top-level-files.md:162) |
| `debug.bind` / `debug.allow_public` | `""` / `false` (02-top-level-files.md:165-166) |
| `debug.block_profile_rate` / `debug.mutex_profile_fraction` | `0` / `0` (02-top-level-files.md:167-168) |
| `plugins.directory` | `"./plugins"` (02-top-level-files.md:171) |

Provider switch, verbatim (02-top-level-files.md:261-271):

| Section | Key | Example value |
|---|---|---|
| `[realtime]` | `provider` | `""` (empty = classic pipeline; supported: `grok`) (02-top-level-files.md:261-262) |
| `[stt]` | `provider` | `"deepgram"` (02-top-level-files.md:264-265) |
| `[llm]` | `provider` | `"openai"` (02-top-level-files.md:267-268) |
| `[tts]` | `provider` | `"cartesia"` (02-top-level-files.md:270-271) |

Notable pinned defaults: `grok` model `grok-voice-latest`, voice `eve`, `reasoning_effort = "high"`, `transcription = true`; `deepgram` STT `nova-3`, TTS `aura-2-thalia-en`, `endpointing = "300"`, `utterance_end_ms = "1000"`; `openai` LLM `gpt-4o-mini`, `stt_model = "whisper-1"`; `ollama` `base_url = "http://localhost:11434"`, model `gemma4:e4b`; `codex` binary `codex`, `model = "gpt-5.6-terra"`, `workspace_root = "/var/lib/streamcore/codex"`, `turn_timeout_ms = 600000`, `network_access = false`; pipeline `barge_in = true`, `user_speech_quiet_ms = 600`, `turn_merge_ms = 350`; display off (`enabled = false`, `plugin = "display-projector"`, `timeout_ms = 3000`, `fast_path_max_chars = 80`); `[github]`/`[codex]` both `enabled = false` (02-top-level-files.md:195-243,02-top-level-files.md:276-338).

Legacy bridge: `pluginSettings` copies every `[plugins.config.<name>]` table, then `withLegacyDisplaySettings` maps `[display]` onto the plugin named by `display.plugin` (default `display-projector`) unless explicitly set, and `withLegacyDeveloperSettings` folds `[github]`/`[codex]` the same way, so pre-move deployments keep working unedited (02-top-level-files.md:822-849).

## Tests (`main_test.go`, 434 lines)
Helpers `mintToken(t, secret, apiKey, body)` drives `tokenHandler` and returns the JWT; `resourceSeenBy(t, secret, token)` runs it through `jwtMiddleware` and reports the handler-side identity (02-top-level-files.md:875-921). Cases: requested `resource_id` round-trips (`user_8891`); empty/`{}`/non-JSON bodies yield no identity; whitespace-only `resource_id` mints no claim; forged token (wrong secret) never reaches the handler with `401`; API-key-gated minting rejects keyless callers with `401` (02-top-level-files.md:923-984). Debug cases: public mux answers `/debug/pprof/` with `404`; loopback bind serves pprof `200`; empty bind with rates warns `debug.bind is empty`; mux pattern table covers all five pprof routes; default-mux handlers leak-test `404`; public bind without acknowledgement errors with `debug.allow_public = true` guidance; `serveDebug` returns on a permanent Accept error and the public mux still serves `/health` after the debug listener dies (02-top-level-files.md:986-1179). Legacy-config cases: `[display]` reaches `display-projector` (`enabled`/`timeout_ms`/`fast_path_max_chars`), stays `enabled = false` when never configured, and explicit `[plugins.config."display-projector"]` wins (02-top-level-files.md:1181-1221).

## Repo hygiene: ignores, submodule, agent guide
`.dockerignore` (11 lines) excludes `.env`, `**/.env`, `**/.env.*`, `**/token.json`, `**/node_modules` (host symlinks crash npm in the image), `*.log`, `.git`, `.gitignore` (02-top-level-files.md:6-19). `.gitignore` (55 lines) excludes `node_modules/`, `.env`/`.env.*` (keeping `!.env.example`), Terraform state/vars (`*.tfstate*`, `*.tfvars` except `*.tfvars.example`), plugin secrets/venvs, `config.toml` (examples tracked), Go artifacts/coverage/vendor/`go.work*`, logs, IDE/OS files (02-top-level-files.md:21-79). `.gitmodules` declares one submodule: `examples` at `https://github.com/streamcoreai/examples.git` (02-top-level-files.md:81-87). `AGENTS.md` (57 lines) requires reading `README.md` + `config.toml.example` (+ `llms-full.txt` for client code) before generating code, states the Go media runtime scope and module path, gives the `cp config.toml.example config.toml` / `go run .` (`:8080`, `/whip`) flow, and mandates the speech-to-speech default (`[realtime] provider = "grok"`, one xAI key) noting Deepgram covers STT+TTS in the classic pipeline and that no OpenAI TTS provider exists (02-top-level-files.md:89-148).

## Dependency pins (`go.sum`, 129 lines)
Selected pins, verbatim (02-top-level-files.md:350-477):

| Module | Version |
|---|---|
| `github.com/BurntSushi/toml` | `v1.6.0` (02-top-level-files.md:350) |
| `github.com/golang-jwt/jwt/v5` | `v5.3.1` (02-top-level-files.md:369) |
| `github.com/ollama/ollama` | `v0.20.3` (02-top-level-files.md:401) |
| `github.com/pion/webrtc/v4` | `v4.2.18` (02-top-level-files.md:435) |
| `github.com/sashabaranov/go-openai` | `v1.36.1` (02-top-level-files.md:441) |
| `github.com/tetratelabs/wazero` | `v1.9.0` (02-top-level-files.md:448) |
| `golang.org/x/crypto` | `v0.48.0` (02-top-level-files.md:454) |

## Chinese README mirror and security policy
`README.zh-CN.md` (193 lines) mirrors the English README in Chinese: Go binary + bring-your-own-agent positioning, live demo at `streamcore.ai` with per-turn STT/LLM/TTS latency, two-terminal quickstart (`cp config.toml.example config.toml`, `go run .`, `:8080`, `http://localhost:8080/whip`, `examples/typescript` client), the 7-row capability table (WHIP/RFC 9725 transport, Pion STUN/TURN UDP+TCP 3478, adaptive VAD + debounce, barge-in with backchannel filter and echo-bounded threshold, streaming STT→LLM→TTS, sessions/events, browser-to-ESP32 reach), the honest-gaps checklist (shipped: reconnection, resume, panic recovery, `server.max_sessions`, env secrets, HTTP agent endpoint; missing: metrics, structured logs, versioned binaries, horizontal scaling, persistent memory), five BYO-agent ways, 10-row docs table, SDK/plugin/examples links, and Apache 2.0 license (02-top-level-files.md:1225-1420). `SECURITY.md` (103 lines) requires private reports via the Security tab (never public issues), asks for commit/version, redacted `config.toml` shape, minimal SDP/RTP/client repro, and attacker gain; promises acknowledgement in 3 business days, assessment in 10, coordinated advisory within 90 days with opt-out credit and no bounty; fixes land on `main` only (pre-1.0, no backports); in-scope covers `/whip`/token auth bypass, peer-reachable crash/exhaustion, TURN open-relay abuse, session isolation, key disclosure via logs/errors/DataChannel/`/health`, plugin overreach, and prompt-injection-to-tool-execution; out-of-scope keeps trusted-plugin behavior, documented misconfiguration, single-process DoS limits, upstream provider bugs, sample code, and header/scanner-only findings; deploy rules are JWT on public `/whip`, secrets out of the repo (gitignored `config.toml`), front TLS, key rotation, pinned/reviewed plugins, and spend-as-signal (02-top-level-files.md:1422-1527).

Truncated in chunk, not described: `config.toml.example` is cut at chunk line 344 (`... (truncated, 7464 more characters)`), so sections after `[ollama]` (agent bridge, remaining providers, RAG, SIP, etc.) are not covered here; `main.go` is cut at chunk lines 849-850 (`... (truncated, 1313 more characters)`), so the tail of `withLegacyDisplaySettings` and `withLegacyDeveloperSettings` bodies is not covered; `main_test.go` is cut at chunk lines 1221-1222 (`... (truncated, 2250 more characters)`), so tests after the display-override case are not covered (02-top-level-files.md:344,02-top-level-files.md:849-851,02-top-level-files.md:1217-1223).

**Covers:** `.dockerignore`, `.gitignore`, `.gitmodules`, `AGENTS.md`, `config.toml.example`, `go.sum`, `main.go`, `main_test.go`, `README.zh-CN.md`, `SECURITY.md` as given in chunks/02-top-level-files.md
