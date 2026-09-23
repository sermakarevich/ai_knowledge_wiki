> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Critical Analysis: soniqo/speech-core
## Claims vs. evidence
- Claim: on-device C++17 speech infrastructure (VAD, batch/streaming STT, diarization, TTS, voice-agent pipeline) for Linux, Windows, Android, running on CPU with no cloud, no Python at inference, no audio leaving the machine.
- Evidence: strong structural support — zero-ML-dependency core (`AGENTS.md:5-7`), three static-library targets splitting core from ONNX/LiteRT backends, and a portable C++/C API surface for JNI/FFI/embedded hosts.
- Claim: small model-agnostic orchestration core (turn detection, interruption, audio utils, conversation state, tool calls) where the app chooses the models and a backend swap is a construction/link choice, not a pipeline rewrite.
- Evidence: unusually specific — abstract interfaces (`STTInterface`, `TTSInterface`, `VADInterface`, `TurnCompletionInterface`, plus diarization trio) named in one header, and the orchestration target never depending on a concrete model.
- Claim: real live-agent behavior — VAD-driven turns, eager STT, partial transcripts, barge-in, streaming TTS, tool calling; streaming ASR on cache-aware RNN-T with end-of-utterance detection, beam search, phrase biasing.
- Evidence: mechanism names are concrete (fixed 80 ms Pocket TTS frames with bounded decoder cache, 64-sample Silero v5 left context), but no latency, RTF, or accuracy numbers accompany them in this material.
- Claim: full offline voice agent in 1.2 GB on Android; releases ship `.deb`/`.tar.gz` (amd64/arm64) and a Windows x64 ZIP bundling runtimes but never models.
- Evidence: packaging story is detailed (bundled ONNX Runtime MIT + `libLiteRt.so` Apache-2.0 per third-party notices, CI smoke-tests the ZIP), but the 1.2 GB figure has no weights-vs-runtime breakdown and no device/latency figures.
- Claim: tested across targets — Linux/Windows/macOS/Android-oriented arm64 plus sanitizers and model-backed nightly lanes.
- Evidence: 9 named test executables and a documented `ctest` workflow lend credibility; counter-signal: `test_pipeline_e2e` is admitted intermittently flaky (SIGTRAP under load).
- Claim: the portable surface (native C++ plus C APIs for Kotlin/JNI, Swift/FFI, embedded Linux) makes the stack hostable anywhere.
- Evidence: the API-shape claim is consistent with the zero-platform-code-in-core guideline (accelerator gating lives in `models/`), but no binding, sample app, or ABI-stability note is in evidence here.
- Net: architecture and packaging claims are well-evidenced at the file level; all performance and quality claims remain unevidenced here.
## Genuinely new vs. repackaged
- The model roster is explicitly upstream: Silero, Smart Turn, Parakeet, Whisper, Canary, Nemotron, MOSS, Pyannote, WeSpeaker, ReDimNet2, VoxCPM, Kokoro, Chatterbox, DeepFilterNet3, and more — no novel acoustic or language modeling is claimed.
- The genuine contribution is systems design: a pure-C++17 orchestration core decoupled from inference via abstract interfaces, with backend selection reduced to CMake targets and link decisions.
- Second candidate contribution: streaming discipline done natively in C++ (RNN-T decoder caches, EOU detection, bounded TTS frame emission, DSP-parity fixes like DeepFilterNet3 STFT scaling and delay compensation).
- Third: distribution engineering — multi-OS builds, runtime-bundling releases without models, native model downloader, multilingual READMEs, agent instruction files (`AGENTS.md`/`CLAUDE.md`/`CODEX.md`).
- The OpenAI-compatible local TTS endpoint (`POST /v1/audio/speech`) is a compatibility shim: sound adoption tactic, not research.
- Repackaging risk follows directly — quality ceilings, license terms, and model supply chains are inherited from upstream weights; PersonaPlex listed as "structural" and CosyVoice3 as "staged" confirm coverage is uneven.
- The same process polish (13 README mirrors, identical agent files, shell LF guards) signals docs-and-agent care, but can also mean marketing surface ahead of hardened internals; code review must decide.
- Differentiation, if real, lives in turn-taking latency, memory budget, and build robustness — the least-measured parts of the current evidence.
## Weaknesses and blind spots
- No accuracy numbers anywhere in evidence: no WER (batch or streaming), no DER for diarization, no MOS/intelligibility for TTS, no VAD false-accept/reject rates.
- No performance numbers: no RTF, no p50/p99 turn or first-audio latency, no thread/SIMD/delegation breakdown; LiteRT path is CPU-only via its C API, and ONNX acceleration (NNAPI, QNN, app-supplied EP hook) has no measured story.
- Coverage truncation is a hard limit: `CMakeLists.txt` only evidenced through ~239 of 1378 lines, README mirror tails truncated, and no `src/`/`include/`/`tests/`/`docs/` internals digested beyond the root — only 2 wiki pages exist so far.
- The admitted flaky e2e pipeline test under load is exactly the test that should certify live-agent claims; sanitizer and nightly model-backed lanes are cited but their results are not in evidence.
- Coupling quirks: HF download support requires LiteRT, the HTTP server requires ONNX — reasonable but a constraint on minimal builds; the amd64 VoxCPM2 voice-cloning bundle (~13 GB, explicitly downloaded) undercuts the slim-offline narrative for that path.
- Operational gaps: model provenance, checksums, versioning, update story, and offline-install path are unstated; privacy posture beyond "no audio leaves the machine" (mic handling, retention, telemetry) is absent.
- Community blind spot: no releases, dependents, contributors, or bus-factor signal in evidence; version strings (`0.1.0` project vs `v0.0.11` highlights) already disagree enough to warrant a tagging-hygiene check.
- Failure-mode blindness: no stated behavior in noise, reverb, overlapping speech, or accented/low-resource input — the conditions where VAD, EOU, and diarization claims live or die.
- Legal homework remains: third-party notices summarized but not audited here, and each upstream weight family carries its own commercial-use constraints to check before shipping.
## Applicability
- Credible fit where offline CPU-only voice I/O is a hard requirement: kiosks, field devices, regulated sites, and Android companions that cannot stream raw audio to the cloud.
- The local OpenAI-compatible TTS endpoint lowers swap-in cost for existing agent scaffolds; C++17 with no Python at inference suits embedding in native apps or edge services.
- Not yet fittable for anything needing quantified accuracy or latency SLAs, certified privacy guarantees, or diarization at scale — none are evidenced.
- A spike should scope to one backend and one device first: core-only build, then ONNX or LiteRT Parakeet transcription against a standard set, before touching TTS or diarization.
- **Relevance to my work**
  - AI/ML engineering: candidate pattern for one CPU-local C++ runtime fronting heterogeneous speech models behind stable abstract interfaces.
  - AI/ML engineering: streaming conventions (decoder caches, EOU detection, fixed-frame TTS emission, DSP-parity discipline) worth mining if the code checks out.
  - Agentic systems: VAD-gated STT loop plus local streaming TTS and structured tool calls (FunctionGemma via LiteRT-LM) as a reusable full-duplex voice-agent template.
  - Agentic systems: adopt turn-taking/barge-in handling only after measured endpointing latency; reproduce the flaky-e2e conditions first.
  - Elisity data platform: on-device VAD/STT as a PII-minimizing pre-filter — ship text, not audio — contingent on measured WER and resource cost.
  - Elisity data platform: speaker-attributed transcripts via the diarization pipeline only with measured DER plus a defined retention policy.
## What this changes
- If substantiated, it lowers the integration tax for offline voice agents: one repo, one toolchain, three-plus OS targets, backend swap without pipeline rewrite.
- It reinforces the template of agent-oriented infra repos: `AGENTS.md`-style contributor contracts plus OpenAI-compatible local endpoints as table stakes.
- It does not move the model-quality frontier — STT/TTS/diarization ceilings stay with upstream weights; the burden shifts to the adopter to reproduce the Android demo and measure everything.
- The evaluation checklist is standard and still entirely open: WER/DER/MOS, p50/p99 latency, memory, battery, accelerator behavior, and a weight-license audit.
- For the digest series itself, the next wiki layers should cover `include/` interfaces, `src/pipeline`, and the test inventory — the root-only view is now the binding constraint on deeper judgment.
## Verdict
- Stronger than a landing-page pitch: the orchestration/backend split, interface list, build guards, test inventory, and runtime-bundling releases form a coherent, reviewable systems bet.
- Still a measurement-free zone on every dimension that matters for production (accuracy, latency, memory, stability), with one self-reported flaky e2e test at the center.
- The strongest reason to trial rather than watch: the interface-segregated design means a spike can falsify the claims cheaply, one backend at a time.
- Responsible next step is a time-boxed build-and-measure spike — core plus one backend on a target device — not a dependency commitment.
- Include the third-party-notices and weight-license review inside that spike, before any prototype ships to users.
- **trial** — earn it with reproduced builds and standard evals before any adoption decision.
