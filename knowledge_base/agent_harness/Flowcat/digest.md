> [[index|Wiki]] | [[summary|Summary]]
# AreevAI/flowcat — Digest

## 1. [[wiki/01-overview|Overview]]
**In one sentence:** Flowcat is a native-Rust, self-hosted runtime for real-time voice agents that carries a call through a composable media pipeline as one self-contained binary in your own VPC.
## Key points
- Flowcat runs the full voice path as transport in → VAD / turn-taking → STT · LLM · TTS (or single speech-to-speech model) → transport out in one self-contained binary with no hosted control plane or phone-home (README.md:14-21).
- It is a clean-room native-Rust counterpart to pipecat's `FrameProcessor` pipeline model and provider breadth, with no pipecat code vendored per `NOTICE` (README.md:23-27).
- The runtime reads only its own `FLOWCAT_*` config and talks only to user-configured providers with user credentials, enabling fully air-gapped local STT/TTS/LLM operation (README.md:52-59).
- ContextRelay reseeds accumulated audio context as compact text (~7× smaller, ~4× cheaper per token), preserving the whole conversation; it is off by default and provider-agnostic (README.md:61-72).
- One process holds flat p99 (≤0.61 ms framework/transport overhead) from 10 to 2,000 concurrent calls on a single box, where conversational latency itself remains provider-dominated (README.md:86-94).
- Nothing networked is in the default build: every provider, transport, and exporter is an opt-in Cargo feature, with umbrella features `stt-all, tts-all, llm-all, realtime-all, obs-all` for CLI/CI (README.md:175-178).
- Embedding composes `transport.input() → vad → stt → llm → tts → transport.output()` (or single realtime S2S model) into a `Pipeline` driven by `PipelineTask` / `PipelineRunner`, plus `AgentBrain` and `SessionSource` seams (README.md:218-227).

## 2. [[wiki/02-top-level-files|Top-Level Files]]
**In one sentence:** The repo root files define Flowcat as a self-contained Cargo workspace with its frozen pipeline API, trait seams, feature-flag matrix, provider taxonomy, and credential-free build/test/demo rules.
## Key points
- Flowcat is a Cargo workspace of framework plus sibling crates (`flowcat-core`, `flowcat-services`, `flowcat-transports`, `flowcat-telephony`, `flowcat-agent`, `flowcat-cli`) plus `bench/`/`bench-rs/` benchmark kit (AGENTS.md:13-25).
- The default build pulls no provider/network deps and tests are hermetic/offline, with CI gating on `cargo fmt --all --check` and `cargo clippy --workspace --all-targets -- -D warnings` (AGENTS.md:27-34).
- `DESIGN.md` is the architecture-and-trait-seam spec (call lifecycle, `MediaTransport`/`AgentBrain`/`SessionSource`/`RealtimeLlm` seams), while `PROCESSOR-DESIGN.md` is the frozen `Frame`/`FrameProcessor`/`Pipeline` API and `README`/`FEATURES.md` are authoritative for current surface (AGENTS.md:7-11, DESIGN.md:20-43).
- Every provider/transport/exporter is one `dep:`-gated Cargo feature with `flowcat-services`/`flowcat-transports` defaulting to `[]`, so `cargo tree` on the default build must not grow (AGENTS.md:36-40, FEATURES.md:1-7).
- Providers are triaged as (D) distinct wire-protocol clients versus (W) thin wrappers (~30-line `base_url`/auth/model structs delegating to a family (D) client), each with a pure encode/decode seam plus fixture tests (AGENTS.md:62-79, PROVIDERS.md:25-31).
- The repo is embedder-independent (no host crate import, no path-dep outside `flowcat/`, builds standalone) with `flowcat-core` knowing nothing about embedder routing/SQL/wire contracts (AGENTS.md:55-57, SPINOUT.md:1-29).
- New source files must start with the SPDX header and provider status must not be overclaimed ("fixture-tested" ≠ "live-verified") (AGENTS.md:35-36, AGENTS.md:60-61).

## The system in five moves
1. A call enters as transport audio in your own VPC and travels transport in → VAD/turn-taking → STT · LLM · TTS (or one realtime speech-to-speech model) → transport out in a single self-contained Rust binary with no hosted control plane.
2. That path is composed from a frozen `Frame`/`FrameProcessor`/`Pipeline` API driven by `PipelineTask`/`PipelineRunner`, with `MediaTransport`, `AgentBrain`, `SessionSource`, and `RealtimeLlm` seams keeping `flowcat-core` contract-agnostic and embedder-independent.
3. Long-call memory is preserved by ContextRelay reseeding accumulated audio context as compact text, and capacity is held by one process with flat sub-millisecond framework overhead while conversational latency stays provider-dominated.
4. The workspace stays lean as breadth grows via one `dep:`-gated Cargo feature per provider/transport/exporter, hermetic offline tests, fmt/clippy CI gates, and SPDX plus no-overclaim provider-status rules.
5. Breadth scales through the (D) distinct-client versus (W) thin-wrapper triage with pure encode/decode fixtures, native SIP/RTP/SDP plus carrier serializers, and credential-free `pipeline`/`ws-echo` demos with `flowcat-server` YAML and `RemoteBrain` on-ramps.
