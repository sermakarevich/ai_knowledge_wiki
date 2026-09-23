[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** Flowcat is a native-Rust, self-hosted runtime for real-time voice agents that carries a call through a composable media pipeline as one self-contained binary in your own VPC.
## Key points
- Flowcat runs the full voice path as transport in → VAD / turn-taking → STT · LLM · TTS (or single speech-to-speech model) → transport out in one self-contained binary with no hosted control plane or phone-home (README.md:14-21).
- It is a clean-room native-Rust counterpart to pipecat's `FrameProcessor` pipeline model and provider breadth, with no pipecat code vendored per `NOTICE` (README.md:23-27).
- The runtime reads only its own `FLOWCAT_*` config and talks only to user-configured providers with user credentials, enabling fully air-gapped local STT/TTS/LLM operation (README.md:52-59).
- ContextRelay reseeds accumulated audio context as compact text (~7× smaller, ~4× cheaper per token), preserving the whole conversation; it is off by default and provider-agnostic (README.md:61-72).
- One process holds flat p99 (≤0.61 ms framework/transport overhead) from 10 to 2,000 concurrent calls on a single box, where conversational latency itself remains provider-dominated (README.md:86-94).
- Nothing networked is in the default build: every provider, transport, and exporter is an opt-in Cargo feature, with umbrella features `stt-all, tts-all, llm-all, realtime-all, obs-all` for CLI/CI (README.md:175-178).
- Embedding composes `transport.input() → vad → stt → llm → tts → transport.output()` (or single realtime S2S model) into a `Pipeline` driven by `PipelineTask` / `PipelineRunner`, plus `AgentBrain` and `SessionSource` seams (README.md:218-227).
---
## Why Flowcat
Own-your-stack runtime for regulated call traffic: a single static Rust binary in your own VPC or air-gapped, no Flowcat cloud, audio/transcripts never leave infrastructure you control (README.md:44-59).

Long-call memory via ContextRelay without the audio tax: converts accumulated audio context to a compact text transcript and reseeds the session so the model re-attends cheap text instead of audio; live voice path unchanged, converted turns carry words not prosody (README.md:61-72).

Pipecat-compatible by design: mirrors the `FrameProcessor` graph, typed `Frame` taxonomy, system-frame priority / interruption model, and STT/TTS/LLM/realtime service seams; same mental model and vendor credentials, single static Rust binary instead of a Python process tree (README.md:74-82).

One process, room to scale: Rust media loop with no GC/GIL uses every core; runtime never becomes the bottleneck or stall source, giving capacity headroom while end-to-end voice latency stays provider-dominated (README.md:84-94).

Driven from Python at turn granularity: run as a service with the `RemoteBrain` adapter (`brain-http` feature) plus MCP-exposed Python tools; per-frame path untouched; in-process PyO3 bindings are roadmap-only (README.md:96-104).

## Benchmark and capacity
What this measures is runtime bottleneck/tail tightness under load, not end-to-end conversational latency, which is provider-dominated (hundreds of ms); sub-millisecond figures are framework/transport overhead (README.md:110-115).

Setup verbatim (README.md:117-121):

```bash
docker compose -f bench/compose.yml up --build   # on a 16-vCPU VM
```

> Single Azure `Standard_FX16mds_v2` box (16 vCPU): one Flowcat process (12 cores) vs pipecat real multiprocess deployment (12 workers, `SO_REUSEPORT`, one per core); identical Rust WebSocket + μ-law load generator, full-duplex echo, 50 frames/s/call, 10 s per data point (README.md:117-121).

p99 round-trip latency vs concurrent calls (README.md:131-136):

| Concurrent calls | Flowcat (1 process) | pipecat (12 workers) |
| --- | --- | --- |
| 250  | **0.59 ms** p99 | 51 ms p99 |
| 500  | **0.51 ms** p99 | 843 ms p99 |
| 1000 | **0.47 ms** p99 | 5,673 ms p99 · 77% throughput |
| 2000 | **0.61 ms** p99 | failing · 41% throughput (982 conns refused) |

Other measured metrics (README.md:140-148):

| Metric | Flowcat (Rust) | pipecat (Python) | Ratio |
| --- | --- | --- | --- |
| Worst-case p99, 10→2,000 calls | **0.61 ms** | 5,673 ms | — |
| Tail at 500 calls (matched load) | **0.51 ms** | 843 ms | **~1,650× lower** |
| Sustained throughput | **100%** to 2,000 calls | collapses past ~250 | — |
| Per-frame routing (framework floor) | **~0.20 µs** | ~106 µs | ~525× |
| RAM per idle session | **~19.6 KB** | ≤ ~1 MB | ~50× tighter |
| Tasks per session | 7 tokio | 22 asyncio | — |
| Multi-core scaling (1→14 cores) | **8.4×** (no GIL) | n/a (1 core/process) | — |

Full distributions and methodology are in `bench/RESULTS.md`; harness and SKU notes in `bench/README.md`; numbers are hardware/config-dependent and pipecat is an unaffiliated baseline reference per `NOTICE` (README.md:150-169).

## How to use it
Cargo workspace of four library crates plus a demo binary; default build has nothing networked (README.md:175-178).

Build and demo verbatim (README.md:179-193):

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

Run an agent from config with no Rust via `flowcat-server`: YAML/JSON node/edge graph plus realtime or cascaded provider topology over HTTP, no control plane or database (README.md:195-200).

```bash
cargo build --release -p flowcat-server --features webrtc
GOOGLE_API_KEY=… ./target/release/flowcat-server --config deploy/agent.example.yaml
# open http://localhost:6210/ to talk to it (mic + live transcript), or bridge a
# Plivo number to the server's /telephony/ws/plivo/{run_id}
```

Providers are selected by name from config via the `flowcat-services` factory with keys from the environment; the graph runs under `flowcat-agent`; Dockerfile, compose file, sample config, and env template are in `deploy/` and schema in `flowcat-server/src/config.rs` (README.md:208-211).

Embed seams for full control (README.md:218-227):

| Seam | Role |
| --- | --- |
| `FrameProcessor` pipeline | compose `transport.input() → vad → stt → llm → tts → transport.output()` (or single realtime S2S) into a `Pipeline`, driven by `PipelineTask` / `PipelineRunner`; each processor in its own tokio task behind a bounded channel |
| `AgentBrain` | conversation decision-making; trait seam, runtime knows nothing of control plane/REST/database; ready-made `RemoteBrain` HTTP adapter for Python |
| `SessionSource` | call bootstrap and finalize |

Feature-flag model (README.md:233-239):

| Item | Value |
| --- | --- |
| `flowcat-core` defaults | `["sip", "recorder"]` (no HTTP/gRPC/ONNX) |
| Provider/transport/exporter gates | `dep:`-gated, default build pays nothing for the 80th provider |
| Umbrella features | `stt-all`, `tts-all`, `llm-all`, `realtime-all`, `obs-all` (CLI and CI) |
| Full enumeration | `FEATURES.md` |
| Processor-author contract | `PROCESSOR-DESIGN.md`, `CONTRIBUTING.md` |

No files were marked truncated in this chunk.
**Covers:** README.md (overview, why-Flowcat, benchmark, usage); referenced `bench/RESULTS.md`, `bench/README.md`, `deploy/`, `flowcat-server/src/config.rs`, `FEATURES.md`, `PROCESSOR-DESIGN.md`, `CONTRIBUTING.md`, `QUICKSTART.md`, `ROADMAP.md`, `NOTICE`
