# Technical Analysis: QuentinFuxa/WhisperLiveKit

**Repository:** https://github.com/QuentinFuxa/WhisperLiveKit
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Problem space: offline Whisper run on successive audio chunks loses cross-chunk context and truncates words mid-syllable, producing high latency and boundary errors in live use. Naive per-batch transcription also wastes compute on silence and cannot serve concurrent sessions with per-session language, translation target, or terminology conditioning (01-overview.md:9-17, 01-overview.md:24-26, 01-overview.md:95-103).

How the repo addresses it: WhisperLiveKit applies simultaneous-speech research policies instead of chunked offline decoding — Simul-Whisper/Streaming with AlignAtt, NLLB-based NLLW, WhisperStreaming with LocalAgreement, Streaming Sortformer diarization, Qwen3-ASR-causal single-encode streaming, AlignAtt4LLM for decoder-only simultaneous translation — fronted by Voice Activity Detection to skip silent frames and a multi-backend server that serves multiple concurrent users (01-overview.md:9-17, 01-overview.md:26). Distribution is `pip install whisperlivekit` with a `wlk` CLI (server, offline file transcription, subtitle generation, model management, benchmarking), a bundled web UI at `http://localhost:8000`, an OpenAI-compatible REST endpoint plus native WebSocket `ws://localhost:8000/asr`, and optional backends installed as extras (01-overview.md:32-72, 01-overview.md:76-103, 01-overview.md:117-132).

Primary user: developer/integrator deploying self-hosted real-time transcription/translation (live meeting, capture, or API-compatible service) who needs low-latency incremental output, not batch transcription.

## 2. High-Level Architecture

```
Browser / SwiftUI / chrome-extension / OpenAI SDK client
  │ audio (PCM/file) + session params (language, target_language, context, mode, token)
  ▼
Web + protocol layer ── http://localhost:8000 (UI, full snapshots)
  │                    ── ws://localhost:8000/asr (native streaming; ?mode=diff experimental)
  │                    ── POST /v1/audio/transcriptions (OpenAI-compatible REST)
  ▼
Session layer ── AudioInput (PCM buffering/decoding, per session)
  │             ── AudioProcessor (per session) ► run_translation() consumes translation events
  │             ── SessionASRProxy / backend session wrapper (language/context overrides)
  ▼
Shared engine ── TranscriptionEngine (models loaded at startup, shared per process)
  │               backends: simul_whisper/, local_agreement/, voxtral-mlx, voxtral-hf,
  │               funasr (SenseVoiceSmall), qwen3-streaming/vllm, canary, mlx-whisper
  │               policies: AlignAtt, LocalAgreement, Voxtral own policy, append-only causal
  ▼
Post-processing ── tokens_alignment.py, translation_processor.py, diarization (Sortformer/Diart)
  │                 NLLB translation, sentence tokenizer, AlignAtt4LLM (separate server)
  ▼
Sinks ── WebSocket JSON (FrontData.to_dict()), SRT/file output, benchmark harnesses
```

Data-flow narrative (5 steps):

1. Ingest: client opens WebSocket session with query parameters (`language`, `target_language`, `context`, `mode`, `token`) or posts a file to the REST endpoint; `AudioInput` owns PCM buffering/decoding per session (01-overview.md:95-103, 02-top-level-files.md:217-224).
2. Gating: Voice Activity Detection suppresses processing when no voice is detected, reducing overhead under multi-user load (01-overview.md:24-26).
3. Inference: the shared per-process `TranscriptionEngine` decodes via the selected backend/policy (`online_factory()` selects the session processor; SimulStreaming AlignAtt, LocalAgreement, Voxtral own policy, Qwen3 causal single-encode); one engine serves mixed-language sessions (02-top-level-files.md:217-224, 02-top-level-files.md:228-236, 01-overview.md:65-68, 01-overview.md:202).
4. Enrichment: `run_translation()` consumes translation events; `tokens_alignment.py` / `translation_processor.py` align and translate (NLLB or external AlignAtt4LLM server via `translation_alignatt.py`); diarization and sentence tokenization are optional extras (02-top-level-files.md:217-224, 02-top-level-files.md:228-236).
5. Emit: `FrontData.to_dict()` defines native WebSocket JSON; browser uses full snapshots, `diff` mode is opt-in experimental (`diff_protocol.py`); offline path writes transcripts/SRT without a server (02-top-level-files.md:217-224, 01-overview.md:65-69, 01-overview.md:36-44).

Persistent state: model weights and Hugging Face hub cache (shared `hf-cache:/root/.cache/huggingface/hub` volume in `compose.yml`); downloaded-model artifacts (`*.pt`, `nllb-200-distilled-600M-ctranslate2/`); no database — session state is ephemeral per-`AudioProcessor`, engine state is in-process shared (02-top-level-files.md:243-298, 02-top-level-files.md:142-167, 02-top-level-files.md:217-224).

## 3. Simultaneous Streaming Session

Representation: a session is a per-connection `AudioProcessor` + owned `AudioInput` (PCM buffer/decoder) bound to one shared `TranscriptionEngine`; configuration is a `WhisperLiveKitConfig` dataclass produced by `parse_args()` (`engine.args` kept as compatibility namespace); wire form is `FrontData.to_dict()` JSON, full-snapshot by default (02-top-level-files.md:217-224).

Named kinds/types with file:line (as cited in wiki pages):

- `TranscriptionEngine` — shared per process, models loaded at startup; `reset()` for tests/backend comparison (02-top-level-files.md:217-224).
- `AudioProcessor` — per session; `run_translation()` consumes translation events; always call `cleanup()` (02-top-level-files.md:217-224).
- `AudioInput` — per session PCM buffering/decoding; does not import orchestrator (02-top-level-files.md:217-224).
- `WhisperLiveKitConfig` / `parse_args()` / `engine.args` — config dataclass, constructor, compat namespace (02-top-level-files.md:217-224).
- `SessionASRProxy` / backend session wrapper — language/context overrides per session (02-top-level-files.md:217-224).
- `FrontData.to_dict()` — native WebSocket JSON contract; browser `full`, `diff` opt-in (02-top-level-files.md:217-224).
- Session query kinds: `language`, `target_language`, `context`, `mode`, `token` (01-overview.md:95-103).
- Policy kinds: AlignAtt (Simul-Whisper/Streaming), LocalAgreement (WhisperStreaming/FunASR), Voxtral own streaming policy, Qwen3 causal append-only, AlignAtt4LLM attention-gated commits (01-overview.md:9-17, 01-overview.md:202, 01-overview.md:224-227).

Key queries (verbatim session-parameter contract, 01-overview.md:95-103):

```
| `language` | `?language=fr` | transcription language for this session (one shared engine serves mixed-language sessions) |
| `target_language` | `?target_language=de` | translation target for this session (server must run with `--target-language`) |
| `context` | `?context=WhisperLiveKit%2C+Qwen3-ASR` | terminology, names, or phrase-list text used to condition this session; supported by Whisper-family and SimulStreaming backends |
| `mode` | `?mode=diff` | incremental snapshot/diff protocol instead of resending the full state (experimental, for integrators building their own client, see `diff_protocol.py`); the bundled web UI uses `full` |
| `token` | `?token=...` | API token when the server runs with `--api-token` (also accepted as an `Authorization: Bearer` header) |
```

## 4. LLM / External Service Integration

Providers and call pattern: the repo calls no hosted LLM/API by default. All inference is local backends selected by extras: Whisper-family (incl. `mlx-whisper`), Voxtral Mini 4B (Mistral AI speech model, MLX or HF Transformers), FunASR SenseVoiceSmall, Qwen3-ASR (HF streaming or vLLM), Canary-1b-v2 (NeMo), NLLB-200-distilled-600M translation (Transformers preferred over CTranslate2 on tested Apple hardware per dev notes) (01-overview.md:117-132, 01-overview.md:183-200, 01-overview.md:209-231, 02-top-level-files.md:302-342). One external-service exception: `translation_alignatt.py` is a client of a separate AlignAtt4LLM translation server, not an in-process module (02-top-level-files.md:217-224). The OpenAI-compatible surface (`POST /v1/audio/transcriptions`, `OpenAI(base_url="http://localhost:8000/v1", api_key="unused")`) is inbound compatibility for existing clients, not an outbound OpenAI call (01-overview.md:76-93).

Required vs optional calls: no required external call; local model loads are required per selected backend. Optional: translation stack (`translation` extra), sentence tokenizer, diarization (Sortformer recommended; Diart not recommended), HF-hub downloads at `pull`/first run (01-overview.md:117-132, 01-overview.md:224-231).

Env vars: `HF_TOKEN` passed through to GPU/CPU compose services for gated hub models; `token`/`--api-token` (or `Authorization: Bearer`) gates sessions when enabled; no LLM API keys documented in analyzed pages (02-top-level-files.md:243-298, 01-overview.md:95-103).

## 5. Real-Time Transcription Pipeline

Step by step (function-level file:line for every function is not present in the analyzed wiki pages; the pages expose module/entry-point granularity, cited below):

1. Configure: `parse_args()` returns `WhisperLiveKitConfig`; `engine.args` compat namespace; CLI selects model/language/backend (`whisperlivekit/cli.py`, `whisperlivekit/parse_args.py`, `whisperlivekit/config.py`) (02-top-level-files.md:228-236, 02-top-level-files.md:217-224).
2. Construct engine: shared `TranscriptionEngine` loads models at startup; backend construction in `whisperlivekit/core.py`, `whisperlivekit/simul_whisper/`, `whisperlivekit/local_agreement/` (02-top-level-files.md:228-236, 02-top-level-files.md:217-224).
3. Accept session: protocol adapters (`whisperlivekit/basic_server.py`, `whisperlivekit/deepgram_compat.py`) open per-session pipeline; `online_factory()` selects session processor; `SessionASRProxy`/wrapper applies `language`/`context` overrides (02-top-level-files.md:228-236, 02-top-level-files.md:217-224).
4. Buffer audio: `whisperlivekit/audio_input.py` (`AudioInput`) buffers/decodes PCM; VAD/VAC gates silent frames before inference (02-top-level-files.md:228-236, 01-overview.md:24-26, 01-overview.md:209-211).
5. Decode streaming: `whisperlivekit/audio_processor.py` (`AudioProcessor`) runs backend policy — AlignAtt commits (SimulStreaming), LocalAgreement commits (WhisperStreaming/FunASR path), Voxtral own policy, or Qwen3 causal append-only encode (02-top-level-files.md:228-236, 01-overview.md:9-17, 01-overview.md:202).
6. Align and translate: `whisperlivekit/tokens_alignment.py`, `whisperlivekit/translation_processor.py`, `run_translation()` event consumer; NLLB or separate AlignAtt4LLM server via `translation_alignatt.py`; optional diarization/sentence split (02-top-level-files.md:228-236, 02-top-level-files.md:217-224).
7. Serialize: `FrontData.to_dict()` emits WebSocket JSON (`full` default, `diff` experimental via `diff_protocol.py`); offline `wlk transcribe` writes text/SRT; `wlk bench` and `scripts/run_scatter_benchmark.py` measure speed/accuracy (02-top-level-files.md:217-224, 01-overview.md:36-48, 01-overview.md:159-167).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `whisperlivekit/audio_processor.py` | n/a in pages | Per-session streaming inference (`AudioProcessor`, `run_translation()`, `cleanup()`) (02-top-level-files.md:228-236) |
| `whisperlivekit/audio_input.py` | n/a in pages | Per-session PCM buffering/decoding (`AudioInput`) (02-top-level-files.md:228-236) |
| `whisperlivekit/core.py` | n/a in pages | Backend construction, shared `TranscriptionEngine` (02-top-level-files.md:228-236) |
| `whisperlivekit/simul_whisper/simul_whisper.py` | l.397 cited | SimulStreaming encoder/policy implementation; M4 timings reference point (02-top-level-files.md:303-321) |
| `whisperlivekit/cli.py`, `whisperlivekit/parse_args.py`, `whisperlivekit/config.py` | n/a in pages | CLI and `WhisperLiveKitConfig` / `parse_args()` (02-top-level-files.md:228-236) |
| `whisperlivekit/basic_server.py`, `whisperlivekit/deepgram_compat.py` | n/a in pages | Server and protocol adapters (REST, WebSocket, compat) (02-top-level-files.md:228-236) |
| `whisperlivekit/translation_processor.py`, `whisperlivekit/tokens_alignment.py` | n/a in pages | Translation events and token alignment (02-top-level-files.md:228-236) |
| `whisperlivekit/whisper/tokenizer.py` | n/a in pages | Available-language list referenced by docs (01-overview.md:108) |
| `pyproject.toml` | `[tool.uv].conflicts`, extras | Extras matrix and conflicting heavy-env declarations (01-overview.md:134-155) |
| `docs/API.md`, `docs/backends.md`, `docs/translation-alignatt.md`, `docs/troubleshooting.md` | n/a in pages | API reference, backend setup, AlignAtt translation, GPU/env fixes (01-overview.md:105-110, 02-top-level-files.md:228-236) |
| `diff_protocol.py` | n/a in pages | Experimental incremental snapshot/diff protocol (01-overview.md:65-69) |
| `compose.yml`, `Dockerfile`, `Dockerfile.cpu` | cpu file traced ll.398-479 | Deployment profiles (Sortformer GPU, Voxtral GPU, CPU) and two-stage CPU image (02-top-level-files.md:243-298, 02-top-level-files.md:398-479) |
| `scripts/run_scatter_benchmark.py`, `benchmarks/h100_scatter/`, `benchmarks/README.md`, `BENCHMARK.md` | n/a in pages | Reproducible scatter benchmarks and Voxtral numbers (01-overview.md:159-167, 01-overview.md:203) |
| `tests/test_harness.py` (`whisperlivekit/test_harness.py`), `tests/test_pipeline.py`, `tests/test_asr_coalescing_pipeline.py` | n/a in pages | Real-audio regression testing entry points (02-top-level-files.md:228-236) |
| `third_party/qwen3-asr-causal` (+ `.gitmodules`) | 5 lines cited | Qwen3 causal-streaming submodule pointer (02-top-level-files.md:169-175) |
| `macos/WhisperLiveKitMac`, `chrome-extension/` | n/a in pages | Native SwiftUI client and web-capture demo (01-overview.md:106, 01-overview.md:170-176) |
| `CLAUDE.md` | navigation ll.228-236 cited | Agent runtime boundaries and area-to-entrypoint map (02-top-level-files.md:210-241) |
| `CITATION.cff`, `CHANGES.md`, `SECURITY.md`, `MANIFEST.in` | cff 1.2.0; others short | Citation (incl. AlignAtt4LLM paper), release-pointer, disclosure policy, fixture packaging (02-top-level-files.md:177-208, 02-top-level-files.md:674-694) |

## 7. Dependencies

Exact version pins are not stated in the analyzed wiki pages; the pages document extras/install expressions, not constraint strings. Required-first ordering below follows core vs optional split implied by the extras matrix.

| Package | Version constraint | Purpose |
|---|---|---|
| (core install) `whisperlivekit` via `pip install whisperlivekit` | unpinned in analyzed pages | Base server, `wlk` CLI, WebSocket + OpenAI-compatible API (01-overview.md:32-33) |
| `mlx-whisper` extra (`".[mlx-whisper]"`) | unpinned in analyzed pages | Apple Silicon MLX Whisper backend (01-overview.md:117-132) |
| `funasr` extra (`".[funasr]"`) | unpinned in analyzed pages | SenseVoiceSmall backend through LocalAgreement/VAD pipeline (01-overview.md:117-132, 01-overview.md:209-211) |
| `voxtral-mlx` / `voxtral-hf` extras | unpinned in analyzed pages | Voxtral Mini backends (MLX Apple Silicon / HF Linux-GPU) (01-overview.md:117-132, 01-overview.md:188-200) |
| `cpu` / `cu129` extras | unpinned in analyzed pages | CPU and CUDA 12.9 PyTorch stacks; GPU profiles A/B (01-overview.md:117-132, 01-overview.md:134-155) |
| `translation` extra | unpinned in analyzed pages | NLLB-based translation stack (01-overview.md:117-132) |
| `sentence_tokenizer` extra | unpinned in analyzed pages | Sentence segmentation for translation/output (01-overview.md:117-132) |
| `qwen3-vllm` / `qwen3-streaming` / `qwen3-vllm-metal` extras | unpinned in analyzed pages; `qwen3-vllm` must be isolated from `cu129` per `[tool.uv].conflicts` | Qwen3-ASR CUDA vLLM, HF streaming, Metal vLLM (01-overview.md:117-132, 01-overview.md:134-155) |
| `diarization-sortformer` / `diarization-diart` extras | unpinned; Diart limited to Python 3.11/3.12 (NumPy<2 via Diart 0.9.2) | Speaker diarization; Sortformer is the Python 3.13 path (01-overview.md:117-132, 01-overview.md:134-155) |
| `canary` extra | unpinned; conflicts with `voxtral-hf`, `qwen3-vllm-metal`, compatible with `diarization-sortformer` | Canary-1b-v2 NeMo backend (01-overview.md:117-132, 01-overview.md:155) |
| `ffmpeg`, `ca-certificates` (runtime image) | unpinned in analyzed pages | Audio decoding and TLS in `Dockerfile.cpu` runtime stage (02-top-level-files.md:424-466) |
| `transformers`, `torch` (named for Voxtral Linux/GPU path) | unpinned in analyzed pages | HF backend requirement (`pip install transformers torch`) (01-overview.md:188-200) |

## 8. CLI / Usage Surface

Entry points: `wlk` CLI (installed by package); Docker entrypoint `["wlk", "--host", "0.0.0.0"]` with default `CMD ["--model", "tiny"]`; compose services; `http://localhost:8000` web UI; `ws://localhost:8000/asr`; `POST /v1/audio/transcriptions` (01-overview.md:32-72, 02-top-level-files.md:398-479, 01-overview.md:76-93).

Commands:

```bash
wlk --model base --language en
wlk run whisper:tiny
wlk transcribe meeting.wav
wlk transcribe --format srt podcast.mp3 -o podcast.srt
wlk models
wlk pull large-v3
wlk rm large-v3
wlk bench
wlk --backend voxtral-mlx
wlk --backend voxtral
wlk --backend funasr --language auto
wlk --backend funasr --model_dir /path/to/SenseVoiceSmall --language yue
python scripts/run_scatter_benchmark.py
```
(01-overview.md:39-72, 01-overview.md:188-200, 01-overview.md:213-222, 01-overview.md:166-167).

| Env var | Effect |
|---|---|
| `HF_TOKEN` | Passed to compose services for hub model access (02-top-level-files.md:243-298) |
| `token` query / `Authorization: Bearer` | Session auth when server runs with `--api-token` (01-overview.md:95-103) |

| Config knob | Effect |
|---|---|
| `--model` / `wlk run <id>` / `pull` / `rm` / `models` | Model select, auto-pull, delete, inventory (01-overview.md:39-72) |
| `--language`, `?language=` | Session transcription language; one engine serves mixed-language sessions (01-overview.md:39-72, 01-overview.md:95-103) |
| `--target-language`, `?target_language=` | Translation target; server flag required (01-overview.md:95-103) |
| `?context=` | Terminology/phrase-list conditioning; Whisper-family and SimulStreaming only (01-overview.md:95-103) |
| `?mode=diff\|full` | Incremental diff (experimental, `diff_protocol.py`) vs full snapshots (bundled UI uses `full`) (01-overview.md:95-103) |
| `--backend` (`voxtral-mlx`, `voxtral`, `funasr`, qwen3/canary families) | Backend/policy selection (01-overview.md:188-231) |
| `--diarization`, `--pcm-input`, `--host`, `--api-token`, SSL/HTTPS options | Deployment features; SSL details in Parameters section (02-top-level-files.md:243-298, 01-overview.md:110) |
| `ARG EXTRAS=cpu` (image build) | Bakes dependency profile into Docker image (02-top-level-files.md:398-479) |

## 9. Extensibility Points

- New streaming backend/policy: add module under `whisperlivekit/simul_whisper/` or `whisperlivekit/local_agreement/`, wire construction in `whisperlivekit/core.py` and selection in `online_factory()`; FunASR precedent reuses LocalAgreement + VAC/VAD pipeline rather than forking it (02-top-level-files.md:228-236, 01-overview.md:209-211).
- New session behavior (language/context override, custom processor): extend `SessionASRProxy` or backend session wrapper selected by `online_factory()`; per-session conditioning precedent is `?context=` for Whisper-family/SimulStreaming (02-top-level-files.md:217-224, 01-overview.md:95-103).
- New wire protocol/client: extend `FrontData.to_dict()` for JSON shape and `diff_protocol.py` for incremental mode; bundled UI is the `full`-snapshot reference (02-top-level-files.md:217-224, 01-overview.md:65-69).
- New protocol adapter: extend `whisperlivekit/basic_server.py` / `whisperlivekit/deepgram_compat.py`; API contract documented in `docs/API.md` (02-top-level-files.md:228-236).
- New translation path: extend `whisperlivekit/translation_processor.py` or add a client like `translation_alignatt.py` pointing at an external server; translation extras and AlignAtt docs are the setup reference (`docs/translation-alignatt.md`) (02-top-level-files.md:217-236).
- New deployment profile: add a `compose.yml` service (image, `EXTRAS`, command, ports, `hf-cache` mount) or a new `Dockerfile.*` variant following the `Dockerfile.cpu` builder/runtime split (02-top-level-files.md:243-298, 02-top-level-files.md:398-479).
- New regression coverage: extend `tests/test_pipeline.py` / `tests/test_asr_coalescing_pipeline.py` via `test_harness.py` with real audio on affected backends before adding scaffolding (02-top-level-files.md:228-240).

## 10. Limitations and Gotchas

- **Heavy extras conflict and need isolated environments.** `qwen3-vllm` must live in a separate environment from `cu129`; `voxtral-hf`/`qwen3-vllm-metal`/vLLM stacks conflict with one another; `canary` conflicts with `voxtral-hf` and `qwen3-vllm-metal`. Declarations live in `[tool.uv].conflicts` in `pyproject.toml` (01-overview.md:134-155).
- **Diart diarization is version-boxed and not recommended.** Diart profile works only on Python 3.11/3.12 because Diart 0.9.2 requires NumPy below 2; Sortformer is the diarization path on Python 3.13 (01-overview.md:134-155).
- **FunASR backend is narrowly scoped.** No `--direct-english-translation`; WLK retains voice-activity control instead of FunASR internal VAD; only SenseVoiceSmall is covered (arbitrary FunASR models are out of contract); SenseVoiceSmall carries its own model license; transcription limited to `zh`/`yue`/`en`/`ja`/`ko`/auto (01-overview.md:224-231).
- **Diff protocol is experimental.** `?mode=diff` is for integrators building their own client; the bundled web UI uses `full`; behavior may change (01-overview.md:95-103).
- **Benchmark scope is bounded.** Scatter claims rest on 6 minutes of LibriVox/Project Gutenberg audiobook audio per language on H100; Qwen3 causal tower is English-only and appears only on the English chart; other hardware relies on contributed reproductions (01-overview.md:159-167).
- **Source-page truncation bounds Qwen3-streaming claims.** The analyzed Qwen3-ASR streaming section is cut mid-sentence at "the pretrained audio to"; no further claims from that section are usable (01-overview.md:235-239).

## 11. How It Compares to Alternatives

- OpenAI Whisper (batch/offline): full-context accuracy on files but no streaming policy; WhisperLiveKit wraps Whisper-family models with AlignAtt/LocalAgreement commit policies plus VAD for incremental low-latency output (01-overview.md:9-17).
- WhisperStreaming (Ufal, LocalAgreement): the 2023 low-latency baseline WhisperLiveKit incorporates as one policy among several, adding multi-backend serving, OpenAI-compatible REST/WebSocket, and translation/diarization stacks (01-overview.md:11).
- Simul-Whisper / Streaming Simul-Whisper (AlignAtt): the 2025 ultra-low-latency transcription research line WhisperLiveKit productizes alongside NLLW translation, Sortformer diarization, and Qwen3 causal streaming (01-overview.md:9-17).
- SYSTRAN faster-whisper / CTranslate2: efficient inference runtime; WhisperLiveKit dev notes measured standard Transformers at 4.1068s vs CTranslate2 at 8.5476s on five NLLB sentences on the tested Apple system and recommend Transformers (ideally MLX) there — runtime choice is hardware-dependent, not universal (02-top-level-files.md:323-342).
- Diart (real-time diarization): usable via extra but version-boxed and not recommended here; Streaming Sortformer is the positioned real-time diarization path (01-overview.md:12, 01-overview.md:134-155).

Positioning: WhisperLiveKit is a self-hosted streaming-transcription/translation server and `wlk` toolkit that composes several simultaneous-speech policies and optional translation/diarization backends behind one session/REST/WebSocket surface, rather than a single model or single-policy research demo.

## Appendix: Selected Code Snippets

1. Quick-start CLI surface (01-overview.md:39-72):

```bash
# Start the server — open http://localhost:8000 and start talking
wlk --model base --language en

# Auto-pull model and start server
wlk run whisper:tiny

# Transcribe a file (no server needed)
wlk transcribe meeting.wav

# Generate subtitles
wlk transcribe --format srt podcast.mp3 -o podcast.srt

# Manage models
wlk models                             # See what's installed
wlk pull large-v3                      # Download a model
wlk rm large-v3                        # Delete a model

# Benchmark speed and accuracy
wlk bench
```

2. API compatibility surface (01-overview.md:76-93):

```bash
# OpenAI-compatible REST API
curl http://localhost:8000/v1/audio/transcriptions -F file=@audio.wav

# Works with the OpenAI Python SDK
client = OpenAI(base_url="http://localhost:8000/v1", api_key="unused")

# Native WebSocket for real-time streaming
ws://localhost:8000/asr
```

3. Deployment defaults, `Dockerfile.cpu` key lines (02-top-level-files.md:398-479):

```
FROM ghcr.io/astral-sh/uv:0.12.10 AS uvbin
FROM debian:bookworm-slim AS builder-cpu
RUN uv python install 3.12
ARG EXTRAS=cpu
HEALTHCHECK --interval=30s --timeout=5s --start-period=120s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')" || exit 1
EXPOSE 8000
ENTRYPOINT ["wlk", "--host", "0.0.0.0"]
CMD ["--model", "tiny"]
```

4. Submodule pointer, `.gitmodules` (02-top-level-files.md:171-175):

```
[submodule "third_party/qwen3-asr-causal"]
	path = third_party/qwen3-asr-causal
	url = https://github.com/QuentinFuxa/Qwen3-ASR-causal.git
```
