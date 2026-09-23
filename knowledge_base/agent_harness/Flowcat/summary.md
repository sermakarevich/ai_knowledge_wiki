# Technical Analysis: AreevAI/flowcat

**Repository:** https://github.com/AreevAI/flowcat
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

The problem space is self-hosted real-time voice-agent infrastructure: carrying phone/WebRTC audio through speech-to-text, language-model reasoning, and text-to-speech (or a single speech-to-speech model) with bounded tail latency at high concurrent-call counts, inside infrastructure the operator controls (README.md:14-21, README.md:44-59). The reference pain point is the Python-process model, where per-frame routing cost, GIL-limited multi-core scaling, and per-session memory footprint cause throughput collapse past a few hundred concurrent calls (README.md:131-148).

The repo addresses it with Flowcat, a native-Rust runtime that carries a call through a composable media pipeline as one self-contained static binary in the operator's own VPC, with no hosted control plane or phone-home (README.md:14-21, README.md:44-59). The framework core (`flowcat-core`) holds the `Frame` / `FrameProcessor` / `Pipeline` / `Task` / `Runner` graph plus trait seams; sibling crates hold providers (`flowcat-services`), transports (`flowcat-transports`), carrier serializers (`flowcat-telephony`), a declarative graph agent (`flowcat-agent`), and a demo binary (`flowcat-cli`) (AGENTS.md:13-25). Two pipeline shapes are supported: cascaded STT → LLM → TTS and single-`RealtimeLlm` speech-to-speech (DESIGN.md:20-43). Long-call memory is handled by ContextRelay, which reseeds accumulated audio context as compact text (~7x smaller, ~4x cheaper per token), off by default and provider-agnostic (README.md:61-72). The primary user is the platform engineer or team deploying regulated or high-volume call traffic who must own the full stack, including air-gapped operation with local STT/TTS/LLM (README.md:44-59, README.md:52-59).

## 2. High-Level Architecture

```
  PSTN SIP/RTP ──► SipAgent / SipTransport (flowcat-core sip) ──┐
  Plivo/Twilio/Telnyx WS ──► host WS ──► WsCarrierTransport      │
                              + MediaSerializer (flowcat-telephony)
                                                                ▼
                                         ┌─────────────────────────────────┐
                                         │ MediaTransport seam: recv /     │
                                         │ send_audio / send_clear         │
                                         │ (DESIGN.md:330-393)             │
                                         └─────────────────────────────────┘
                                                                │
                                                                ▼
                                    transport.input() ──► vad ──► stt ──► llm ──► tts
                                                                │
                                        or single RealtimeLlm (e.g. Gemini Live)
                                                                │
                                                                ▼
                                                      transport.output()
                                                                │
                       ┌──────────────────┼──────────────────┐
                       ▼                  ▼                  ▼
              AgentBrain seam    SessionSource seam    Observer / metrics frames
         (DeclarativeBrain /     (call bootstrap +     (PROCESSOR-DESIGN.md:1-13)
          RemoteBrain HTTP)       finalize)
         (README.md:218-227)
```

Data flow, cascaded shape (README.md:218-227, DESIGN.md:45-63):

1. Ingress: carrier audio enters through a `MediaTransport` implementation. SIP/RTP-only carriers go through in-process `SipAgent` plus per-dialog `SipTransport` (RTP decode to 20 ms audio at 8 kHz, BYE/timeout to `Stop`); WebSocket-media carriers (e.g. Plivo `<Stream>`) go through the host WebSocket into `WsCarrierTransport` plus a `flowcat-telephony` serializer (DESIGN.md:45-63, DESIGN.md:64-89, SIP-DESIGN.md:1-16, SIP-DESIGN.md:17-55).
2. Frame routing: the `MediaTransport` yields `MediaIn::{StreamStart, Audio, Stop}` into the `FrameProcessor` graph, where each processor runs in its own tokio task behind a bounded channel and system frames (`Start`/`Stop`/`Cancel`/`Interruption`) bypass `process_frame` with priority/interruption semantics (DESIGN.md:330-393, AGENTS.md:35-61, README.md:74-82).
3. Inference: audio frames pass VAD/turn-taking, then either the cascaded chain (STT service, LLM service, TTS service selected by name from config via the `flowcat-services` factory) or a single `RealtimeLlm` such as Gemini Live; conversation logic sits behind the `AgentBrain` seam (native `DeclarativeBrain` or `RemoteBrain` HTTP adapter for Python) (README.md:208-227, README.md:96-104, DESIGN.md:20-43).
4. Egress: synthesized audio returns through `send_audio`, conversation teardown and bearer clearing through `send_clear` / `Stop`; `SessionSource` handles call bootstrap and finalize (DESIGN.md:330-393, README.md:218-227).
5. Observation: `Observer` and metrics frames record the pass without participating in media flow; observability exporters (`obs-otel`/`obs-sentry`/`obs-langfuse`) are opt-in features (PROCESSOR-DESIGN.md:1-13, FEATURES.md:15-53).
6. Memory: when enabled, ContextRelay converts accumulated audio context to a compact text transcript and reseeds the session so the model re-attends text; the live voice path itself is unchanged (README.md:61-72).

Persistent state: the runtime keeps no database and no control plane; `flowcat-server` runs a YAML/JSON node/edge graph from config with no control plane or database (README.md:195-200). In-memory per-session state is ~19.6 KB RAM per idle session across 7 tokio tasks per session (README.md:140-148). Durable artifacts are limited to WAV recording via the `recorder` feature (`hound`) and optional observability exports (FEATURES.md:15-53).

## 3. The FrameProcessor Pipeline

The central concept is the `FrameProcessor` pipeline, a pipecat-parity graph model defined as frozen API in `PROCESSOR-DESIGN.md` (PROCESSOR-DESIGN.md:1-13, AGENTS.md:35-61). Representation: a closed `enum Frame` covering every pipecat frame plus one `Custom(Arc<dyn CustomFrame>)` escape hatch, so core processors match exhaustively while extensions downcast only where understood (PROCESSOR-DESIGN.md:90-116). Composition is `transport.input() → vad → stt → llm → tts → transport.output()` (or a single realtime speech-to-speech model) assembled into a `Pipeline` (with a `ParallelPipeline` variant) driven by `PipelineTask` / `PipelineRunner`, each processor in its own tokio task behind a bounded channel (README.md:218-227). The hot frame is `Arc<AudioFrame>`; `process_frame` must not block, lifecycle/system frames (`Start`/`Stop`/`Cancel`/`Interruption`) are handled via `start`/`stop` rather than `process_frame`, frames are pushed via `Link`, and processors never call each other directly (AGENTS.md:35-61).

Named kinds and types with citations: `Frame` (closed enum + `Custom`) (PROCESSOR-DESIGN.md:90-116); `FrameProcessor` (AGENTS.md:13-25, README.md:218-227); `Pipeline` / `ParallelPipeline` / `PipelineTask` / `PipelineRunner` (README.md:218-227, PROCESSOR-DESIGN.md:1-13); `Observer` and metrics frames (PROCESSOR-DESIGN.md:1-13); `AudioChunk { pcm: Vec<i16>, sample_rate: u32 }` and `MediaIn::{StreamStart, Audio, Stop}` (DESIGN.md:330-393); seams `MediaTransport` / `MediaSocket` / `MediaSerializer` / `AgentBrain` / `SessionSource` / `RealtimeLlm` (DESIGN.md:20-43, DESIGN.md:330-393); service traits `SttService` / `TtsService` / `LlmService` / `RealtimeLlmService` in `flowcat-core::service` (AGENTS.md:62-79).

Key query: the embedder contract for the media seam (DESIGN.md:330-393):

```rust
pub struct AudioChunk { pub pcm: Vec<i16>, pub sample_rate: u32 }
#[async_trait] pub trait MediaTransport: Send {
    async fn recv(&mut self) -> Option<MediaIn>;
    async fn send_audio(&mut self, chunk: AudioChunk) -> Result<(), FlowcatError>;
    async fn send_clear(&mut self) -> Result<(), FlowcatError>;
    fn carrier_rate(&self) -> u32;
}
pub enum MediaIn { StreamStart { call_id: String }, Audio(AudioChunk), Stop }
```

A second structural query is the consumer composition seam (README.md:218-227): `transport.input() → vad → stt → llm → tts → transport.output()` into a `Pipeline` driven by `PipelineTask` / `PipelineRunner`, with `AgentBrain` for decision-making and `SessionSource` for bootstrap/finalize.

## 4. LLM / External Service Integration

The repo calls external LLM, STT, TTS, and realtime speech-to-speech providers, all opt-in behind per-provider Cargo features; the default build has nothing networked (README.md:175-178, FEATURES.md:1-11). Provider breadth is approximately 80 connectors across sibling crates: 6 realtime plus core Gemini, 20 STT, 31 TTS, 23 LLM, enumerated in `FEATURES.md` with umbrella features `stt-all`, `tts-all`, `llm-all`, `realtime-all`, `obs-all` for CLI/CI (README.md:175-178, FEATURES.md:15-53, DESIGN.md:20-43).

Provider structure follows a (D)/(W) triage (AGENTS.md:62-79, PROVIDERS.md:25-31): (D) distinct wire-protocol clients with their own client plus a pure encode/decode seam and fixture tests, versus (W) thin wrappers (~30-line `base_url`/auth/model structs delegating to a family (D) client). LLM families are overwhelmingly OpenAI-compatible: 5 (D) (`openai`, `openai_responses`, `anthropic`, `google/gemini`, `aws_bedrock`) and 18 (W) over `OpenAiLlm` differing only in `base_url`, auth, and default model (PROVIDERS.md:39-45). STT is roughly 16 (D) plus 4 (W): streaming WebSocket clients (mostly (D)), one (D) Whisper-HTTP client with (W)s (`groq`/`fal`/`speaches`/`xai`), gRPC Google/NVIDIA-Riva (D), local `whisper-rs` (D) (PROVIDERS.md:88-132). TTS is roughly 28 (D) plus 2 (W): streaming-WebSocket Cartesia-family (D each) plus an HTTP-POST-audio long tail (mostly (D), `groq`/`xai` (W) over OpenAI-TTS-HTTP), reusing `WsTtsClient`/`HttpTtsClient` helpers (PROVIDERS.md:136-186).

Required versus optional calls: no provider call is required by the framework; the runtime reads only its own `FLOWCAT_*` config and talks only to user-configured providers with user credentials, so fully air-gapped local STT/TTS/LLM operation is possible (README.md:52-59, SPINOUT.md:22-55). Selection is by provider name from config via the `flowcat-services` factory, with keys from the environment (README.md:208-211). The first native brain is Gemini Live; the alternative is any cascaded STT → LLM → TTS combination; Python-side reasoning goes through the `RemoteBrain` HTTP adapter (`brain-http` feature) plus MCP-exposed Python tools, with in-process PyO3 bindings roadmap-only (DESIGN.md:45-63, README.md:96-104, ROADMAP.md:14-45).

Environment variables and secrets: provider keys follow the `PROVIDER_API_KEY` convention read from the environment, with live provider tests `#[ignore]`d (AGENTS.md:33-34). Documented instances are `GOOGLE_API_KEY` for the `flowcat-server` browser-call example (README.md:195-200, QUICKSTART.md:33-60) and `FLOWCAT_VOICE` / `FLOWCAT_VAD_*` as the only `FLOWCAT_*` keys the framework itself reads (SPINOUT.md:22-55). Transports Daily (`daily`) use `reqwest`; AWS-family auth is hand-rolled SigV4 over `hmac`/`sha2` with known-answer tests, no AWS SDK and no OpenSSL (AGENTS.md:35-61, FEATURES.md:46-54).

## 5. The Voice-Agent Call Path

Primary workflow: config-driven call setup through inference to teardown, in the two shapes `build_s2s_task` (single `RealtimeLlm`) and `build_cascaded_task` (STT → LLM → TTS) (DESIGN.md:20-43).

1. Build config graph — operator writes a YAML/JSON node/edge graph plus provider topology; schema lives in `flowcat-server/src/config.rs`, sample config and env template in `deploy/` (README.md:195-211). Providers resolve by name through the `flowcat-services` factory with environment keys (README.md:208-211).
2. Bootstrap session — `SessionSource` performs call bootstrap; `MediaTransport::recv` yields `MediaIn::StreamStart { call_id }` for telephony ingress (SIP `SipAgent` REGISTER/INVITE/ACK/BYE path or Plivo-style WebSocket `<Stream>` through `WsCarrierTransport` plus serializer) (DESIGN.md:45-89, DESIGN.md:330-393, SIP-DESIGN.md:17-55).
3. Stream media frames — `SipTransport` decodes RTP to 20 ms audio at 8 kHz (PCMU/PCMA, G.711, 20 ms ptime, jitter buffer); carrier serializers in `flowcat-telephony` (Twilio/Telnyx/Plivo and others, plus DTMF via RFC2833 or Goertzel `dtmf-inband`) frame WebSocket audio (SIP-DESIGN.md:17-55, FEATURES.md:15-53, DESIGN.md:330-393).
4. Run the processor graph — `transport.input() → vad → stt → llm → tts → transport.output()` (or single realtime model) executes as a `Pipeline` under `PipelineTask` / `PipelineRunner`, with `AgentBrain` (`DeclarativeBrain` over the node/edge spec, or `RemoteBrain` HTTP adapter exposing `/session` + `/tool-call` with `transition`/`stay`/`end`) making conversation decisions (README.md:218-227, FEATURES.md:15-53, QUICKSTART.md:33-60).
5. Emit audio and handle interruption — `MediaTransport::send_audio` returns synthesized `AudioChunk`; system frames (`Interruption`/`Cancel`/`Stop`) preempt via the priority path and `send_clear` clears bearers (DESIGN.md:330-393, AGENTS.md:35-61, README.md:74-82).
6. Finalize — `MediaIn::Stop` (BYE/timeout or WebSocket close) ends the stream; `SessionSource` finalizes; optional WAV recording (`recorder`) and observability exporters (`obs-otel`/`obs-sentry`/`obs-langfuse`) close out the call (DESIGN.md:330-393, FEATURES.md:15-53).

Credential-free verification of the path uses the two demo commands `cargo run -p flowcat-cli -- pipeline` (440 Hz sine through `Source → Echo → Tap → Sink`) and `cargo run -p flowcat-cli -- ws-echo --loopback` (real WebSocket PCM echo round-trip), plus the stdlib-only `examples/python-remote-brain/brain_server.py` for the `RemoteBrain` contract (README.md:179-193, AGENTS.md:33-34, QUICKSTART.md:33-60).

## 6. Key Files

| File | Lines | What It Does |
| --- | --- | --- |
| README.md | overview, why-Flowcat, benchmark, usage (cited README.md:14-239) | Authoritative surface: embedding seams, feature flags, demos, benchmark setup |
| PROCESSOR-DESIGN.md | frozen spec, §2.1–§2.3 lifecycle rules; taxonomy at PROCESSOR-DESIGN.md:90-116 | Frozen `Frame`/`FrameProcessor`/`Pipeline` API and frame taxonomy |
| DESIGN.md | seams and call lifecycle; contracts at DESIGN.md:330-393; scope at DESIGN.md:20-89 | Architecture and trait-seam spec (`MediaTransport`/`AgentBrain`/`SessionSource`/`RealtimeLlm`) |
| FEATURES.md | matrix at FEATURES.md:1-53 | Per-provider/transport/exporter feature flags, defaults, umbrellas, toolchain caveats |
| AGENTS.md (= CLAUDE.md:1-84) | workspace at AGENTS.md:13-25; rules at AGENTS.md:35-79 | Contributor contract: workspace layout, hermetic tests, frozen-API rules, provider triage |
| PROVIDERS.md | breadth map at PROVIDERS.md:1-45; families at PROVIDERS.md:88-186 | STT/TTS/LLM provider catalogue and (D)/(W) fan-out plan |
| SIP-DESIGN.md | decision at SIP-DESIGN.md:1-16; design at SIP-DESIGN.md:17-55 | Native SIP/RTP/SDP removal of FreeSWITCH, `SipAgent`/`SipTransport` design |
| flowcat-server/src/config.rs | config schema (README.md:208-211) | YAML/JSON node/edge graph plus provider topology schema |
| QUICKSTART.md | flow at QUICKSTART.md:1-60 | Clone-to-conversation path: demos, `RemoteBrain` contract, first provider key |
| ROADMAP.md | status at ROADMAP.md:1-45 | Landed capabilities versus planned work (PyO3, WebRTC/Opus, LiveKit, live-verified coverage) |
| SECURITY.md | policy at SECURITY.md:1-43 | Supported versions, private reporting, in-scope parsing/signing/framing surface |
| SPINOUT.md | isolation at SPINOUT.md:1-55 | Embedder-independence claim, leak scan, seam-only configuration |
| NOTICE | attribution at NOTICE:13-81 | Apache-2.0 license, pipecat/SigV4/vendor/crate attributions |
| bench/RESULTS.md, bench/README.md | methodology (README.md:150-169) | Full benchmark distributions, harness, and SKU notes |
| deploy/agent.example.yaml, deploy/ | sample deployment (README.md:195-211) | Sample agent config, Dockerfile, compose file, env template |
| examples/python-remote-brain/brain_server.py | contract (QUICKSTART.md:33-60) | Stdlib-only `RemoteBrain` `/session` + `/tool-call` reference server |

## 7. Dependencies

The wiki component pages record dependency names but no version constraint strings; exact constraints are therefore listed as not stated in the wiki sources rather than inferred. Required entries (always present) come first, then optional per-feature entries.

| Package | Version constraint | Purpose |
| --- | --- | --- |
| tokio | not stated in wiki pages | Async runtime; 7 tokio tasks per session, bounded inter-processor channels (README.md:140-148, README.md:218-227) |
| hound | not stated in wiki pages | WAV recording behind `recorder` default in `flowcat-core` (FEATURES.md:15-53) |
| rsipstack | not stated in wiki pages | Native SIP UA parsing/stack (NOTICE:13-81) |
| str0m | not stated in wiki pages | WebRTC transport behind `webrtc-str0m` (FEATURES.md:15-53, NOTICE:13-81) |
| audiopus | not stated in wiki pages | Opus codec for WebRTC/local transports (FEATURES.md:15-53) |
| tokio-tungstenite, tokio-util | not stated in wiki pages | WebSocket transports (`ws`, `webrtc-str0m`) (FEATURES.md:15-53) |
| reqwest (rustls-only) | not stated in wiki pages | HTTP provider clients; `daily` transport; `brain-http` `RemoteBrain` adapter (FEATURES.md:15-53, FEATURES.md:46-54) |
| tonic, tonic-build, protoc | not stated in wiki pages | gRPC STT/TTS (`stt-google`/`stt-nvidia`/`tts-google`/`tts-nvidia`); `protoc` required at build time (FEATURES.md:46-54) |
| whisper-rs / whisper.cpp, cmake, C/C++ toolchain | not stated in wiki pages | Local STT behind `stt-whisper-local` (FEATURES.md:46-54) |
| ort, ndarray | not stated in wiki pages | VAD behind `vad-ort` (FEATURES.md:15-53) |
| nnnoiseless | not stated in wiki pages | Denoising filter behind `filter-rnnoise` (FEATURES.md:15-53) |
| rubato | not stated in wiki pages | Audio resampling (NOTICE:13-81) |
| hmac, sha2 | not stated in wiki pages | Hand-rolled AWS SigV4, no AWS SDK / no OpenSSL (FEATURES.md:46-54) |

Default-feature posture: `flowcat-core` defaults to `["sip", "recorder"]`; `flowcat-services` and `flowcat-transports` default to `[]`; `flowcat-telephony` defaults to `["plivo"]`; `flowcat-agent` defaults to `["brain"]` (FEATURES.md:15-53).

## 8. CLI / Usage Surface

Entry points: `flowcat-cli` ships the `flowcat` demo binary with `pipeline` and `ws-echo` demos (SPINOUT.md:22-55); `flowcat-server` runs a config-driven agent over HTTP with a browser talk page and telephony WebSocket bridges (README.md:195-200).

| Command | Effect |
| --- | --- |
| `cargo build` | Build workspace with default features (no provider client deps) (README.md:179-193) |
| `cargo test` | Full fixture/wire suite, no network, no credentials (README.md:179-193, AGENTS.md:27-34) |
| `cargo build -p flowcat-services --features stt-all,tts-all,llm-all,realtime-all,obs-all` | Fat build pulling in every provider client (README.md:179-193) |
| `cargo run -p flowcat-cli -- pipeline` | In-process `FrameProcessor` pipeline demo, no credentials (README.md:179-193) |
| `cargo run -p flowcat-cli -- ws-echo --loopback` | Real WebSocket PCM echo round-trip demo (README.md:179-193) |
| `cargo build --release -p flowcat-server --features webrtc` then `./target/release/flowcat-server --config deploy/agent.example.yaml` | Run agent from config; talk at `http://localhost:6210/`, bridge Plivo numbers to `/telephony/ws/plivo/{run_id}` (README.md:195-200) |
| `cargo fmt --all --check` / `cargo clippy --workspace --all-targets -- -D warnings` | CI gates: formatting check, clippy with warnings denied (AGENTS.md:27-34) |

| Env var | Required? | Used for |
| --- | --- | --- |
| `GOOGLE_API_KEY` | Only for the Gemini-backed server example | First provider key to run `flowcat-server --config deploy/agent.example.yaml` (QUICKSTART.md:33-60) |
| `PROVIDER_API_KEY`-convention keys | Only for live/ignored tests and configured providers | Live provider tests (`#[ignore]`d) and provider auth selected by name from config (AGENTS.md:33-34, README.md:208-211) |
| `FLOWCAT_VOICE`, `FLOWCAT_VAD_*` | Optional runtime tuning | Only `FLOWCAT_*` keys the framework itself reads (SPINOUT.md:22-55) |

| Config surface | Format / location | Content |
| --- | --- | --- |
| Agent graph | YAML/JSON, e.g. `deploy/agent.example.yaml`, schema in `flowcat-server/src/config.rs` | Node/edge graph plus realtime or cascaded provider topology; no control plane or database (README.md:195-211) |
| Cargo features | `FEATURES.md`, `flowcat-services`/`flowcat-transports` `Cargo.toml` | One `dep:`-gated flag per provider/transport/exporter; umbrellas `stt-all`/`tts-all`/`llm-all`/`realtime-all`/`obs-all` (README.md:175-178, FEATURES.md:1-11) |
| `RemoteBrain` contract | `examples/python-remote-brain/brain_server.py` | `/session` + `/tool-call` with `transition`/`stay`/`end` verbs (QUICKSTART.md:33-60) |

## 9. Extensibility Points

- New STT/TTS/LLM/realtime provider: implement `SttService` / `TtsService` / `LlmService` / `RealtimeLlmService` (in `flowcat-core::service`) in `flowcat-services/src/<cat>/<name>.rs`; triage (D) distinct client versus (W) thin wrapper over a family (D) client; add one `dep:`-gated feature (a (W) enables its family feature, e.g. `llm-groq = ["llm-openai"]`); register `mod` + `pub use`; add to the matching `*-all` umbrella; keep `FEATURES.md` in sync; unwired stubs return `FlowcatError::Other("<provider>: not yet wired")` (AGENTS.md:62-79, PROVIDERS.md:25-31, FEATURES.md:1-11).
- New processor in the media graph: follow `PROCESSOR-DESIGN.md` §2.1–§2.3 and `CONTRIBUTING.md`; handle lifecycle via `start`/`stop`, keep `process_frame` non-blocking, push via `Link`, never call another processor directly, use `Arc<AudioFrame>` for hot audio; use `Custom(Arc<dyn CustomFrame>)` for extension frames outside the closed `Frame` enum (AGENTS.md:35-61, PROCESSOR-DESIGN.md:90-116).
- New transport: implement behind the `MediaTransport` / `MediaSocket` / `MediaSerializer` seams (`recv`, `send_audio`, `send_clear`, `carrier_rate`; `on_message`, `encode_audio`, `encode_clear`) as one `dep:`-gated feature in `flowcat-transports` (DESIGN.md:330-393, AGENTS.md:36-40).
- New carrier framing: add a dependency-free pure-framing flag in `flowcat-telephony` alongside `plivo` / `twilio` / `telnyx` / `exotel` / `vonage` / `genesys` / `asterisk` / `cloudonix` / `vobiz`, plus DTMF via RFC2833 or `dtmf-inband` Goertzel (FEATURES.md:15-53).
- New conversation logic: implement `AgentBrain` (native Rust, e.g. extend `DeclarativeBrain` graph evaluation in `flowcat-agent` with `default-features = false` for the pure engine) or run out-of-process Python through the `RemoteBrain` HTTP adapter (`brain-http`) plus MCP tools (README.md:218-227, README.md:96-104, FEATURES.md:15-53).
- New call bootstrap/finalize behavior: implement `SessionSource` (DESIGN.md:20-43, README.md:218-227).
- New observability export: add behind one `dep:`-gated feature next to `obs-otel` / `obs-sentry` / `obs-langfuse` / `mcp` (FEATURES.md:15-53).

## 10. Limitations and Gotchas

- **Benchmark numbers measure framework overhead, not conversational latency.** Sub-millisecond p99 figures are per-frame routing/transport overhead on a 16-vCPU Azure `Standard_FX16mds_v2` box with a Rust WebSocket μ-law echo load generator; end-to-end voice latency remains provider-dominated in the hundreds of milliseconds, and results are hardware/config-dependent (README.md:110-121, README.md:150-169).
- **Most providers are fixture-tested, not live-verified.** New-provider rules require honest status labeling because the suite is hermetic/offline on exact bytes/JSON with no live sockets; broader live-verified coverage is explicitly roadmap work (AGENTS.md:35-61, AGENTS.md:60-61, ROADMAP.md:14-45).
- **Python integration is out-of-process only.** The `RemoteBrain` HTTP adapter plus MCP tools is the available path (per-frame path untouched); in-process PyO3 bindings are roadmap-only and not started, and the `local` device backend is currently a stub (README.md:96-104, ROADMAP.md:14-45).
- **WebRTC and LiveKit paths are incomplete.** Complete `str0m` WebRTC + Opus transport and real LiveKit signaling are planned, not landed; gRPC providers additionally require `protoc` via `tonic-build` and local Whisper requires `cmake` plus a C/C++ toolchain (ROADMAP.md:14-45, FEATURES.md:46-54).
- **Default build is intentionally non-functional for networked calls.** Nothing networked ships by default; every provider/transport/exporter must be explicitly enabled via `dep:`-gated features or umbrellas, and `cargo tree` on the default build must not grow (README.md:175-178, AGENTS.md:36-40).
- **Only latest `main` is supported, pre-1.0.** Vulnerability reports go privately via GitHub Security or `security@areev.ai` with crates/version, feature flags, repro, and impact; no public issues (SECURITY.md:1-43).

## 11. How It Compares to Alternatives

- **pipecat (Daily, BSD-2-Clause):** the declared architecture/API reference for the `FrameProcessor` taxonomy, interruption model, service seams, serializers, and catalogue; Flowcat is a clean-room native-Rust counterpart with no pipecat code vendored, trading the Python process tree for a single static binary with ~0.20 µs per-frame routing, ~19.6 KB per idle session, and flat p99 to 2,000 calls on one box in the reported echo benchmark (README.md:23-27, README.md:74-82, README.md:131-148, NOTICE:13-81).
- **FreeSWITCH-based softswitch stacks:** the removed alternative; `SIP-DESIGN.md` records the decision to drop FreeSWITCH for native in-process `SipAgent` + `SipTransport`, keeping one binary with no softswitch sidecar (SIP-DESIGN.md:1-55).
- **Hosted voice-agent clouds / control planes:** the rejected deployment model; Flowcat runs fully in the operator's VPC or air-gapped with only user-configured providers and user credentials, no Flowcat cloud and no phone-home (README.md:44-59, README.md:52-59).
- **Python remote-brain services:** the complementary extension path rather than a competitor; `RemoteBrain` (`brain-http`) plus MCP tools lets Python own turn-granularity decisions over `/session` + `/tool-call` while the per-frame media path stays in Rust (README.md:96-104, QUICKSTART.md:33-60).

Positioning: Flowcat occupies the own-your-stack, single-Rust-binary slot for regulated or high-concurrency call traffic where per-call overhead and dependency closure matter more than the breadth of a hosted platform, accepting fixture-level provider coverage and out-of-process Python as current trade-offs (README.md:44-59, README.md:84-94, ROADMAP.md:14-45).

## Appendix: Selected Code Snippets

1. Media transport seam, `DESIGN.md:330-393`:

```rust
pub struct AudioChunk { pub pcm: Vec<i16>, pub sample_rate: u32 }
#[async_trait] pub trait MediaTransport: Send {
    async fn recv(&mut self) -> Option<MediaIn>;
    async fn send_audio(&mut self, chunk: AudioChunk) -> Result<(), FlowcatError>;
    async fn send_clear(&mut self) -> Result<(), FlowcatError>;
    fn carrier_rate(&self) -> u32;
}
pub enum MediaIn { StreamStart { call_id: String }, Audio(AudioChunk), Stop }
#[async_trait] pub trait MediaSocket: Send {
    async fn recv(&mut self) -> Option<WsIn>;
    async fn send_text(&mut self, s: String) -> Result<(), FlowcatError>;
    async fn send_binary(&mut self, b: Vec<u8>) -> Result<(), FlowcatError>;
}
pub trait MediaSerializer: Send {
    fn on_message(&mut self, msg: &WsIn) -> SerIn;
    fn encode_audio(&self, chunk: &AudioChunk) -> WsOut;
    fn encode_clear(&self) -> Option<WsOut>;
    fn carrier_rate(&self) -> u32;
}
```

2. Credential-free build, test, and demo surface, `AGENTS.md:27-34` and `README.md:179-193`:

```bash
cargo build -p flowcat-cli     # default features — pulls NO provider/network deps
cargo test                     # full suite: hermetic, no network, no credentials
cargo fmt --all                # CI gates on `cargo fmt --all --check`
cargo clippy --workspace --all-targets -- -D warnings   # CI denies warnings
```

```bash
# Build the whole workspace (default features only → no provider client deps).
cargo build

# Run the full fixture/wire test suite (no network, no credentials).
cargo test

# Build a "fat" binary that pulls in every provider client:
cargo build -p flowcat-services \
  --features stt-all,tts-all,llm-all,realtime-all,obs-all

# The demo binary — two runnable, credential-free demos:
cargo run -p flowcat-cli -- pipeline           # in-process FrameProcessor pipeline
cargo run -p flowcat-cli -- ws-echo --loopback # real WebSocket PCM echo round-trip
```

3. Config-driven server run, `README.md:195-200`:

```bash
cargo build --release -p flowcat-server --features webrtc
GOOGLE_API_KEY=… ./target/release/flowcat-server --config deploy/agent.example.yaml
# open http://localhost:6210/ to talk to it (mic + live transcript), or bridge a
# Plivo number to the server's /telephony/ws/plivo/{run_id}
```

4. Benchmark harness invocation, `README.md:117-121`:

```bash
docker compose -f bench/compose.yml up --build   # on a 16-vCPU VM
```
