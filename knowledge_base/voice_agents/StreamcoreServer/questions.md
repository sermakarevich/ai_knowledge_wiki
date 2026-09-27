---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: streamcoreai/streamcore-server

### Q1. What is StreamCore's core responsibility, and what stays outside it?
> [!tip]- Answer
> StreamCore owns the latency-sensitive realtime media path: WebRTC transport, adaptive turn-taking, barge-in, streaming STT/LLM/TTS, NAT traversal, sessions, and realtime events. The agent itself — prompts, tools, models, and business logic — stays outside the binary via bring-your-own-agent options. See [[wiki/01-overview|Overview]].

### Q2. How do WebRTC transport, NAT traversal, and connection recovery work in StreamCore?
> [!tip]- Answer
> Clients connect with WebRTC audio over WHIP (RFC 9725) via a single HTTP POST to `:8080/whip` with Opus/RTP both ways and no signaling socket. Built-in Pion STUN/TURN on UDP and TCP 3478 replaces any external coturn. Dropped paths recover by ICE restart on the same session, with single-use resume tokens and SDK redial ladders. See [[wiki/01-overview|Overview]].

### Q3. How do adaptive turn-taking and barge-in handle interruptions and backchannels?
> [!tip]- Answer
> Adaptive VAD tracks each call's noise floor while a debounce merges mid-sentence pauses into one turn. Confirmed barge-in ducks agent audio, filters backchannels like "mm-hm", and cancels in-flight LLM and TTS. On paths without echo cancellation such as telephony, the interrupt threshold is bounded by what the agent just sent so it never interrupts itself. See [[wiki/01-overview|Overview]].

### Q4. What is the boot order and public HTTP surface of the StreamCore binary?
> [!tip]- Answer
> `main()` loads config, starts the optional pprof debug server, sets plugin settings before discovery, builds the RAG client, starts built-in TURN only when `public_ip` plus `turn_secret` are set, then wires the session manager, WHIP handler with optional JWT, and CORS mux before listening and supervising graceful shutdown. The public surface is exactly `/whip`, `/whip/`, `/health` returning `ok`, and `/token` only when `server.jwt_secret` is set, with pprof isolated on a separate debug mux. See [[wiki/02-top-level-files|Top-level files]].

### Q5. How do JWT auth on `/whip` and token minting on `/token` work?
> [!tip]- Answer
> When `server.jwt_secret` is set, `/whip` requires an HMAC-SHA256 Bearer token, exempts CORS preflight, and forwards the `sub` claim as caller identity. `POST /token` mints 1-hour tokens, mapping a trimmed non-empty `resource_id` body field to `sub`, optionally gated by `Authorization: Bearer <apiKey>`, with bodies capped at 4096 bytes. Forged tokens are rejected with 401 before claims are read. See [[wiki/02-top-level-files|Top-level files]].

### Q6. What does the debug server do, and what does `config.toml.example` define?
> [!tip]- Answer
> The debug server is off when `debug.bind` is empty, rejects negative profiling rates and non-loopback binds without `allow_public`, applies block/mutex profile rates, and only logs listener failures so a dead pprof socket never drops live calls. The 311-line `config.toml.example` is the full annotated schema covering server ports/secrets/caps, debug, plugins, pipeline timing, realtime/classic provider switches, and per-provider credentials, with legacy `[display]`/`[github]`/`[codex]` folded into plugin settings. See [[wiki/02-top-level-files|Top-level files]].

### Q7. (Evaluation) Should a team adopt StreamCore for a multi-region voice product needing horizontal scaling and audited metrics?
> [!tip]- Answer
> Not as-is for that target: the wiki lists single-node in-process sessions with no horizontal scaling, no Prometheus/OpenTelemetry metrics export, text-only `log.Printf` logging without structured `session_id` fields, and no versioned standalone binaries. Recommend adopting it for single-node realtime media with a bring-your-own agent, while planning external work for multi-region session distribution, metrics, structured logging, and releases. See [[wiki/01-overview|Overview]].
