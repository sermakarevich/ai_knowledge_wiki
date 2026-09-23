---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: AreevAI/flowcat

### Q1. What is Flowcat in one sentence and what voice path does it run?

> [!tip]- Answer
> > Flowcat is a native-Rust, self-hosted runtime for real-time voice agents shipped as one self-contained binary in your own VPC. It carries a call through transport in → VAD / turn-taking → STT · LLM · TTS (or a single speech-to-speech model) → transport out with no hosted control plane or phone-home. See [[wiki/01-overview|Overview]].

### Q2. How is Flowcat related to pipecat, and how do you embed or drive it?

> [!tip]- Answer
> > Flowcat is a clean-room native-Rust counterpart to pipecat's `FrameProcessor` pipeline model and provider breadth, with no pipecat code vendored. You compose `transport.input() → vad → stt → llm → tts → transport.output()` into a `Pipeline` driven by `PipelineTask` / `PipelineRunner`, with `AgentBrain` and `SessionSource` seams for decisions and call bootstrap. Python teams drive it at turn granularity via the `RemoteBrain` HTTP adapter, since in-process PyO3 bindings are roadmap-only. See [[wiki/01-overview|Overview]].

### Q3. What is ContextRelay and what does it cost you?

> [!tip]- Answer
> > ContextRelay preserves long-call memory by reseeding accumulated audio context as compact text (~7× smaller, ~4× cheaper per token) so the model re-attends cheap text instead of rebilled audio. It is off by default and provider-agnostic, and the live voice path is unchanged. The trade-off is that converted turns carry words, not prosody. See [[wiki/01-overview|Overview]].

### Q4. What does the benchmark actually prove, and what is its key caveat?

> [!tip]- Answer
> > On one 16-vCPU box, a single Flowcat process holds flat p99 framework/transport overhead (≤0.61 ms) from 10 to 2,000 concurrent calls with 100% throughput, while a 12-worker pipecat deployment tails to 843 ms at 500 calls and collapses past ~250. The caveat is that these are runtime-overhead numbers, not end-to-end conversational latency, which stays provider-dominated in the hundreds of milliseconds. See [[wiki/01-overview|Overview]].

### Q5. What is the workspace layout and what are the build, test, and doc-authority rules?

> [!tip]- Answer
> > Flowcat is a Cargo workspace of `flowcat-core`, `flowcat-services`, `flowcat-transports`, `flowcat-telephony`, `flowcat-agent`, and `flowcat-cli`, plus the `bench/`/`bench-rs/` benchmark kit. The default build pulls no provider or network deps, tests are hermetic and offline, and CI gates on `cargo fmt --all --check` and `cargo clippy --workspace --all-targets -- -D warnings`. `DESIGN.md` specifies trait seams and call lifecycle, `PROCESSOR-DESIGN.md` freezes the `Frame`/`FrameProcessor`/`Pipeline` API, and `README`/`FEATURES.md` are authoritative for current surface. See [[wiki/02-top-level-files|Top-Level Files]].

### Q6. How does the feature-flag matrix work and how do you add a provider?

> [!tip]- Answer
> > Every provider, transport, and exporter is one `dep:`-gated Cargo feature, with `flowcat-services`/`flowcat-transports` defaulting to `[]` and umbrella features `stt-all, tts-all, llm-all, realtime-all, obs-all` for CLI/CI. New providers are triaged as (D) distinct wire-protocol clients with a pure encode/decode seam plus fixture tests, or (W) thin wrappers (~30-line `base_url`/auth/model structs delegating to a family (D) client). Golden rules require the SPDX header on new files and honest status claims where "fixture-tested" is never called "live-verified". See [[wiki/02-top-level-files|Top-Level Files]].

### Q7. Your team runs regulated in-VPC voice traffic with long calls and high concurrency but no Rust expertise — should you adopt Flowcat?

> [!tip]- Answer
> > Yes, recommend Flowcat: its single air-gappable binary keeps audio in your VPC, ContextRelay preserves whole conversations at a fraction of the token cost, and one process absorbs spikes that would force a Python worker fleet. Start credential-free with the `pipeline` and `ws-echo` demos, then serve a YAML agent via `flowcat-server` with local STT/TTS/LLM and drive policy from Python through `RemoteBrain`. Decline only if you need a managed control plane or guaranteed sub-hundred-millisecond end-to-end latency, since provider inference still dominates and the project is pre-1.0. See [[wiki/01-overview|Overview]].
