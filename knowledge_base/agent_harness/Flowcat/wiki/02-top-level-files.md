[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-Level Files
**In one sentence:** The repo root files define Flowcat as a self-contained Cargo workspace with its frozen pipeline API, trait seams, feature-flag matrix, provider taxonomy, and credential-free build/test/demo rules.
## Key points
- Flowcat is a Cargo workspace of framework plus sibling crates (`flowcat-core`, `flowcat-services`, `flowcat-transports`, `flowcat-telephony`, `flowcat-agent`, `flowcat-cli`) plus `bench/`/`bench-rs/` benchmark kit (AGENTS.md:13-25).
- The default build pulls no provider/network deps and tests are hermetic/offline, with CI gating on `cargo fmt --all --check` and `cargo clippy --workspace --all-targets -- -D warnings` (AGENTS.md:27-34).
- `DESIGN.md` is the architecture-and-trait-seam spec (call lifecycle, `MediaTransport`/`AgentBrain`/`SessionSource`/`RealtimeLlm` seams), while `PROCESSOR-DESIGN.md` is the frozen `Frame`/`FrameProcessor`/`Pipeline` API and `README`/`FEATURES.md` are authoritative for current surface (AGENTS.md:7-11, DESIGN.md:20-43).
- Every provider/transport/exporter is one `dep:`-gated Cargo feature with `flowcat-services`/`flowcat-transports` defaulting to `[]`, so `cargo tree` on the default build must not grow (AGENTS.md:36-40, FEATURES.md:1-7).
- Providers are triaged as (D) distinct wire-protocol clients versus (W) thin wrappers (~30-line `base_url`/auth/model structs delegating to a family (D) client), each with a pure encode/decode seam plus fixture tests (AGENTS.md:62-79, PROVIDERS.md:25-31).
- The repo is embedder-independent (no host crate import, no path-dep outside `flowcat/`, builds standalone) with `flowcat-core` knowing nothing about embedder routing/SQL/wire contracts (AGENTS.md:55-57, SPINOUT.md:1-29).
- New source files must start with the SPDX header and provider status must not be overclaimed ("fixture-tested" ≠ "live-verified") (AGENTS.md:35-36, AGENTS.md:60-61).
---
## Workspace layout and ignored outputs
`AGENTS.md:14-25` lists the crates verbatim:

- `flowcat-core/` — framework: `Frame`, `FrameProcessor`, `Pipeline`/`Task`/`Runner`, audio codec/resample/recorder, native SIP/RTP/SDP, Gemini Live, all trait seams.
- `flowcat-services/` — STT/TTS/LLM/realtime providers + observability exporters + MCP, one Cargo feature each.
- `flowcat-transports/` — WebRTC (`str0m`) / WebSocket / Daily / LiveKit / local.
- `flowcat-telephony/` — carrier serializers (Twilio/Telnyx/Plivo/…) + DTMF.
- `flowcat-agent/` — declarative graph agent: config-driven `AgentBrain` (`DeclarativeBrain`) over a node/edge graph spec; default-on `brain` feature, or pure engine with `default-features = false`.
- `flowcat-cli/` — the `flowcat` demo binary.
- `bench/`, `bench-rs/` — the reproducible pipecat-vs-flowcat benchmark kit.

Ignored build outputs (`.gitignore:1-11`):

```
/target
/website/book
/pipecat
/bench/vm-results.txt
```

`CLAUDE.md:1-84` is a byte-identical duplicate of `AGENTS.md` (same title, workspace list, build commands, golden rules, provider steps).

## Build, test, and golden rules
Verbatim (AGENTS.md:27-34):

```bash
cargo build -p flowcat-cli     # default features — pulls NO provider/network deps
cargo test                     # full suite: hermetic, no network, no credentials
cargo fmt --all                # CI gates on `cargo fmt --all --check`
cargo clippy --workspace --all-targets -- -D warnings   # CI denies warnings
```

Credential-free demos are `cargo run -p flowcat-cli -- pipeline` and `... ws-echo --loopback`; live provider tests are `#[ignore]`d and read `PROVIDER_API_KEY`-convention keys from the environment (AGENTS.md:33-34).

Golden rules (AGENTS.md:35-61):

| # | Rule |
| --- | --- |
| 1 | Every new source file starts with `// SPDX-License-Identifier: Apache-2.0` (`<!-- … -->` in markdown) |
| 2 | Default build stays dependency-free; every provider/transport/exporter is one `dep:`-gated feature; `flowcat-services`/`flowcat-transports` default to `[]` |
| 3 | Tests are offline: pure encode/decode fixtures on exact bytes/JSON, never a live socket; new auth/signing (e.g. SigV4) needs a known-answer test |
| 4 | Don't break the frozen API (`PROCESSOR-DESIGN.md` §2.1–§2.3): lifecycle/system frames (`Start`/`Stop`/`Cancel`/`Interruption`) bypass `process_frame` — use `start`/`stop`; `process_frame` must not block; push via `Link`, never call another processor directly; hot frame is `Arc<AudioFrame>` |
| 5 | Keep `flowcat-core` contract-agnostic; embedder knowledge lives behind `AgentBrain` / `SessionSource` / `MediaTransport` seams |
| 6 | Comments/docs are public; no internal tickets or work-stream labels |
| 7 | Be honest about provider status — "fixture-tested" ≠ "live-verified" |

Add-a-provider triage (AGENTS.md:62-79, PROVIDERS.md:25-31): (D) distinct client (own wire protocol → real client + pure encode/decode seam + fixtures) or (W) thin wrapper (OpenAI-compatible → ~30-line struct with different `base_url`/auth delegating to the (D) family client); impl the category service trait (`SttService`/`TtsService`/`LlmService`/`RealtimeLlmService` in `flowcat-core::service`) in `flowcat-services/src/<cat>/<name>.rs`, add a `dep:`-gated feature (a (W) just enables its (D) family feature, e.g. `llm-groq = ["llm-openai"]`), register `mod` + `pub use`, add to `*-all` umbrella, keep `FEATURES.md` in sync; unwired stub returns `FlowcatError::Other("<provider>: not yet wired")`.

## Design docs (DESIGN, PROCESSOR-DESIGN, SIP-DESIGN)
`DESIGN.md:1-19` defines Flowcat as a native-Rust real-time voice-agent runtime carrying phone/WebRTC audio through a speech-to-speech model with a pluggable "brain" as one self-contained binary in your own VPC, with no hosted control plane and no Python/FreeSWITCH sidecar, designed to be embedded by a host application.

Scope note (DESIGN.md:20-43): seams are unchanged but runtime broadened to two pipeline shapes (`build_s2s_task` / `build_cascaded_task` for single `RealtimeLlm` like Gemini Live or cascaded STT → LLM → TTS), ~80 providers, 5 transports, 9 telephony serializers in sibling crates, fully local/air-gapped connectors, and the `RemoteBrain` HTTP adapter for Python; `README`/`FEATURES.md`/`PROCESSOR-DESIGN.md` are authoritative for current surface, `DESIGN.md` for trait seams and call lifecycle.

Milestone goal (DESIGN.md:45-63): end-to-end telephony for WebSocket-media carriers (e.g. Plivo, pure-Rust path) and SIP/RTP-only carriers via native in-process `SipAgent` + `SipTransport` through the same `MediaTransport` seam; first brain is native Rust Gemini Live, alternative is cascaded STT → LLM → TTS, logic behind `AgentBrain` (linked rlib or `RemoteBrain` HTTP adapter).

Two-plane fit (DESIGN.md:64-89): PSTN SIP/RTP → in-embedder `SipAgent`, Plivo `<Stream>` WS → host WS → `WsCarrierTransport`, both into the embedder (HTTP `/telephony/ws/{provider}/{run}`, `SipAgent`, control plane, `AgentBrain`/`SessionSource` impls) using `flowcat-core` (`MediaTransport`, call pipeline, codec, recorder, `sip/`, `AgentBrain`·`SessionSource`·`MediaTransport`·`RealtimeLlm` traits); `flowcat-core` knows nothing about embedder, web routing, SQL, or wire contract (DESIGN.md:87-89).

Core trait seams excerpt (DESIGN.md:330-393):

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

`PROCESSOR-DESIGN.md:1-13` is marked **FROZEN**: the keystone API for the pipecat-parity program (`Frame`, `FrameProcessor`, `Pipeline`/`ParallelPipeline`, `PipelineTask`/`PipelineRunner`, `Observer`, metrics frames, service-processor trait signatures), landing alongside `Call::run`, never as a rewrite-in-place. Design decision excerpt (PROCESSOR-DESIGN.md:90-116): closed `enum Frame` for every pipecat frame plus one `Custom(Arc<dyn CustomFrame>)` escape hatch, so core processors `match` exhaustively while OSS extensions downcast only where understood.

`SIP-DESIGN.md:1-16` records the decision that SIP is native Rust inside flowcat and FreeSWITCH is removed (single binary, no softswitch), generalizing the pipeline over `MediaTransport` (`recv` → `MediaIn::{StreamStart, Audio, Stop}`, `send_audio`, `send_clear`, `carrier_rate`; `Call<Tr: MediaTransport, R: RealtimeLlm, B: AgentBrain, S: SessionSource>`), with `SipAgent` (REGISTER/INVITE/ACK/BYE, G.711 PCMU/PCMA, 8 kHz, 20 ms ptime) and per-dialog `SipTransport` (RTP decode → 20 ms `Audio @ 8000`, BYE/timeout → `Stop`, jitter buffer) plus host/control-plane rewire and removals of `deploy/freeswitch/` and the gateway serializer (SIP-DESIGN.md:17-55).

## Feature-flag matrix (FEATURES)
`FEATURES.md:1-11` states every provider, transport, and exporter is a single `dep:`-gated Cargo feature so the default build pulls none of their client dependencies, with (D)/(W) tags per `CONTRIBUTING.md`.

| Crate | Defaults | Notes (FEATURES.md:15-53) |
| --- | --- | --- |
| `flowcat-core` | `default = ["sip", "recorder"]` | `sip` = native SIP UA; `recorder` = WAV via `hound`; optional `vad-ort` (`ort`, `ndarray`), `filter-rnnoise` (`nnnoiseless`); seams, Gemini Live client, codec/resample, SIP/RTP/SDP always present |
| `flowcat-services` | `default = []` | Umbrellas `stt-all`, `tts-all`, `llm-all`, `realtime-all`, `obs-all`; 6 realtime + core Gemini, 20 STT, 31 TTS, 23 LLM, `obs-otel`/`obs-sentry`/`obs-langfuse`/`mcp`, `brain-http` (`reqwest`, `tokio/rt-multi-thread`) |
| `flowcat-transports` | `default = []` | `webrtc-str0m` (`str0m`, `audiopus`, `tokio`, `tokio-util`), `ws` (`tokio-tungstenite`, `tokio`, `tokio-util`), `daily` (`reqwest`), `livekit` (stub), `local` (`audiopus`, `tokio`) |
| `flowcat-telephony` | `default = ["plivo"]` | Dependency-free pure-framing flags: `plivo` on; `twilio`, `telnyx`, `exotel`, `vonage`, `genesys`, `asterisk`, `cloudonix`, `vobiz`, `dtmf-inband` (Goertzel; RFC2833 always available) |
| `flowcat-agent` | `default = ["brain"]` | `DeclarativeBrain` `AgentBrain` adapter over node/edge `graph_spec`; `default-features = false` gives pure graph engine (parse/validate/`{{var}}` interpolation) with no `flowcat-core` dep |

Toolchain caveats (FEATURES.md:46-54): gRPC features (`stt-google`/`stt-nvidia`/`tts-google`/`tts-nvidia`) need `protoc` via `tonic-build`; `stt-whisper-local` bundles whisper.cpp needing `cmake` + C/C++ toolchain; everything else is rustls-only `reqwest`/`tokio-tungstenite` with hand-rolled SigV4 over `hmac`/`sha2` (no AWS SDK, no OpenSSL).

## Provider map, quickstart, roadmap, security, spinout, notice
`PROVIDERS.md:1-12` is the STT/TTS/LLM provider breadth map for ~70 remaining providers landing in isolated worktrees; pre-creating every module home + feature + dep + compiling stub keeps merges conflict-free on `flowcat-services/Cargo.toml` and `src/{stt,tts,llm}/mod.rs`. LLM headline (PROVIDERS.md:39-45): overwhelmingly OpenAI-compatible — 15 pipecat LLM services subclass `OpenAILLMService`, so 5 (D) (`openai`✓, `openai_responses`, `anthropic`, `google/gemini`, `aws_bedrock`) and 18 (W) over `OpenAiLlm` (differing only in `base_url` + auth + default model). STT families (PROVIDERS.md:88-132): streaming-WS (mostly (D)), one (D) Whisper-HTTP client with (W)s (`groq`/`fal`/`speaches`/`xai`), gRPC Google/NVIDIA-Riva (D), local `whisper-rs` (D); ~16 (D) + ~4 (W). TTS (PROVIDERS.md:136-186): streaming-WS Cartesia-family (D each) plus HTTP-POST-audio long tail (mostly (D), `groq`/`xai` (W) over OpenAI-TTS-HTTP); ~28 (D) + ~2 (W), reusing `WsTtsClient`/`HttpTtsClient` plumbing helpers.

`QUICKSTART.md:1-15` goes from `git clone` to watching the runtime move real audio and drive a conversation in ~5 minutes with no credentials: `cargo build -p flowcat-cli`, `cargo run -p flowcat-cli -- pipeline` (440 Hz sine through `Source → Echo → Tap → Sink`, `in == out == sourced`), `cargo run -p flowcat-cli -- ws-echo` (byte-for-byte WebSocket loopback), and the stdlib-only `examples/python-remote-brain/brain_server.py` with the `/session` + `/tool-call` (`transition`/`stay`/`end`) `RemoteBrain` contract; one provider key (`GOOGLE_API_KEY`) then runs `flowcat-server --config deploy/agent.example.yaml` for a browser call at `http://localhost:6210/` (QUICKSTART.md:33-60).

`ROADMAP.md:1-13` is directional-only (shipped capabilities live in `README`/`FEATURES.md`): recently landed composable `FrameProcessor` pipeline (frozen in `PROCESSOR-DESIGN.md`), native SIP/RTP/SDP, ~80 connectors, `flowcat-cli` `pipeline`/`ws-echo` demos, out-of-process Python via `RemoteBrain` (`brain-http`) + `mcp`; planned: in-process PyO3 bindings (Python at turn granularity, GIL released, not started), complete `str0m` WebRTC + Opus transport, feature-gated local device backend (current `local` is a stub), broader live-verified provider coverage (currently fixture/wire-tested), and real LiveKit signaling (ROADMAP.md:14-45).

`SECURITY.md:1-19` supports only latest `main` (pre-1.0); report privately via GitHub Security → Report a vulnerability or `security@areev.ai` with crates/version, feature flags, repro, and impact (no public issues); aims to acknowledge in 3 business days with coordinated disclosure; in-scope examples are SIP/RTP/SDP parsing, SigV4 signing, WebSocket framing, and audio codec handling (SECURITY.md:20-43).

`SPINOUT.md:1-21` asserts a self-contained workspace with zero embedder dependency (no `use <embedder>_*`, no embedder crate in any `Cargo.toml`, no path-dep outside `flowcat/`, `cargo build` standalone), verified by the `grep -rnE 'path\s*=\s*"(\.\./)+' --include='Cargo.toml' .` leak scan plus `cargo build && cargo test`; `flowcat-core` exposes only media-pipeline framework + four seams, providers/transports sit behind one feature each, embedder-supplied SIP credentials and URLs arrive via `SipConfig`/`SipAgent` and seams (only `FLOWCAT_*` keys like `FLOWCAT_VOICE`, `FLOWCAT_VAD_*` are read by flowcat itself); `flowcat-cli` (`bin: flowcat`) ships the `pipeline` and `ws-echo` demos (SPINOUT.md:22-55).

`NOTICE:1-6` licenses Flowcat under Apache-2.0 (© 2026 MindGryd Software Private Limited) and attributes pipecat (BSD-2-Clause, © 2024-2026 Daily, architecture/API reference for FrameProcessor taxonomy, interruption model, service seams, serializers, catalogue), AWS SigV4 published test vectors, third-party vendor wire protocols/trademarks (independent client, user credentials required), and third-party Rust crates (`tokio`, `str0m`, `rsipstack`, `reqwest`, `tonic`, `rubato`, `ort`, others; MIT/Apache-2.0) (NOTICE:13-81).

Truncated in this chunk (contents beyond the excerpt not summarized): `DESIGN.md` (truncated after trait contracts, 7900 more characters), `PROCESSOR-DESIGN.md` (truncated after frame taxonomy opening, 50028 more characters), `PROVIDERS.md` (truncated after fan-out grouping header, 4026 more characters).
**Covers:** `.gitignore`, `AGENTS.md`, `CLAUDE.md`, `DESIGN.md`, `FEATURES.md`, `NOTICE`, `PROCESSOR-DESIGN.md`, `PROVIDERS.md`, `QUICKSTART.md`, `ROADMAP.md`, `SECURITY.md`, `SIP-DESIGN.md`, `SPINOUT.md`
