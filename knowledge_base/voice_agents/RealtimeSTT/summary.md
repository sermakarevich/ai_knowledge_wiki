# Technical Analysis: KoljaB/RealtimeSTT

**Repository:** https://github.com/KoljaB/RealtimeSTT
**Version analyzed:** 1.1.2 (latest entry `1.1.2 - 2026-08-30` in `RELEASE_NOTES.md:276-438`)
**Date:** 2026-09-22
**Wiki:** [[index]]

Scope note: the wiki at analysis time contains two component pages — a README-derived overview (`01-overview.md`) and a root-file inventory (`02-top-level-files.md`). All claims below are grounded in those pages and their `file:line` citations. Package internals (`RealtimeSTT/`, `RealtimeSTT_server/` source lines), per-engine adapters, and server request handlers beyond what the README exposes are not covered in the wiki and are not asserted here.

## 1. Overview / What Problem It Solves

Problem space: application developers need microphone or stream-fed speech-to-text with bounded latency, without assembling VAD, chunking, model inference, wake-word gating, and server transport themselves. Raw engine libraries (Whisper-family, ONNX streaming models) expose inference, not turn detection, realtime partials, callbacks, or deployment contracts.

How the repo addresses it: RealtimeSTT is a Python speech-to-text library that turns microphone or application-fed audio into final plus optional realtime transcripts using voice activity detection, selectable engines, wake words, and an optional production server (`01-overview.md:3`). One class, `AudioToTextRecorder`, covers direct microphone input and application-fed PCM (`use_microphone=False` plus `feed_audio()` for 16-bit mono PCM at 16 kHz or resampled input) (README.md:110-116, README.md:143-158). VAD uses WebRTC VAD and Silero VAD; wake-word activation optionally uses Porcupine or OpenWakeWord (README.md:172-174). Event callbacks cover recording, VAD, realtime text, transcription, and wake-word state (README.md:176-177). A packaged production FastAPI server adds versioned HTTP/WebSocket contracts, session isolation, bounded shared inference resources, authentication, and readiness/capabilities endpoints (README.md:178-180, README.md:225-230).

Primary user: a Python application developer building an assistant, dictation tool, browser streaming server, or prototype that needs speech-to-text in a few lines of code (README.md:11-13).

## 2. High-Level Architecture

```text
Microphone ─► AudioToTextRecorder ─► VAD (WebRTC │ Silero) ─► Transcription engines ─► Callbacks / text()
     │                  │                        │                         │                        │
     │                  ▼                        ▼                         ▼                        ▼
App-fed PCM ─► feed_audio() ─► Wake-word gate (Porcupine │ OpenWakeWord) ─► Realtime partials + Final transcript
     │                                                                               │
     └─────────────────────────── Production FastAPI server (HTTP/WebSocket, auth, sessions) ◄─ Browser clients
```

Data-flow narrative:

1. **Capture.** Either the microphone path (`AudioToTextRecorder()` + `text()`) or the external-audio path (`AudioToTextRecorder(use_microphone=False)` + `feed_audio(chunk, original_sample_rate=...)`) ingests 16-bit mono PCM at 16 kHz (README.md:106-116, README.md:143-158).
2. **Gate.** VAD (WebRTC, Silero) segments speech from silence; an optional wake-word stage (Porcupine or OpenWakeWord) holds transcription until activation (README.md:172-174).
3. **Transcribe.** The general-purpose default path uses `faster_whisper`; other engines require install extras with optional dependencies and models (README.md:15-17). The recommended CPU streaming profile splits duties: `sherpa-onnx-nemotron-3.5-asr-streaming-0.6b-560ms-int8` emits fast replaceable realtime text over new frames only, while `sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8` refines the complete turn once at finalization (README.md:23-31).
4. **Deliver.** Final transcripts return via `text()` (blocking single utterance or callback-driven continuous dictation, README.md:106-139); realtime partials, recording/VAD/transcription/wake-word events fire through callbacks (README.md:176-177).
5. **Serve (optional).** The packaged production server exposes versioned health, readiness, capabilities, raw-PCM final transcription, and ordered streaming WebSocket endpoints, binds loopback by default, and requires bearer-token plus Uvicorn TLS files for direct non-loopback binds (README.md:225-230). The versioned production WebSocket path owns its turn state and does not derive finalization from recorder VAD (README.md:242-245).
6. **Release.** CI covers Python 3.11 and 3.12; packaging ships `requirements.txt`, `README.md`, `RELEASE_NOTES.md`, `LICENSE` in the sdist while pruning dev/private/diagnostic trees (`MANIFEST.in:1-13`).

Persistent state lives in three places per the wiki: pinned Sherpa model bundles under a persistent directory (e.g. `./models/sherpa-onnx`, README.md:35-38, README.md:247-249), the production server's per-session turn state and bounded shared inference resources (README.md:178-180, README.md:242-245), and the release history itself (`RELEASE_NOTES.md:1-313`, releases `1.0.3`–`1.1.2`). No database or durable transcript store is described in the covered pages.

## 3. The AudioToTextRecorder Abstraction

Central concept: `AudioToTextRecorder` is the single user-facing recorder object. Representation per the wiki is constructor configuration plus a small method/callback surface, not a transcript data structure: constructor parameters (model/engine selection, realtime transcription, VAD timing, wake words, callbacks, external audio, logging, executor injection) are documented in `docs/configuration.md` (README.md:165-168); exact surfaced parameter/method names are `use_microphone`, `feed_audio`, `original_sample_rate`, `text`, `shutdown` (README.md:143-158).

Named kinds/types (all cited to README lines via the wiki):

- **Input modes:** microphone capture vs. application-fed audio with `use_microphone=False` (README.md:110-116, README.md:143-145).
- **Transcription engines:** `faster_whisper` default (README.md:15-17, README.md:21-22); CPU streaming pair `sherpa-onnx-nemotron-3.5-asr-streaming-0.6b-560ms-int8` (realtime) + `sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8` (final) (README.md:23-27); `kroko_onnx` native streaming engine (README.md:58-62); engine-specific references for `whisper.cpp`, OpenAI Whisper, Moonshine, `sherpa-onnx`, Kroko-ONNX, Parakeet NeMo, Meta Omnilingual ASR, Granite/Qwen Transformers engines, Cohere Transcribe, FunASR (README.md:209-221).
- **VAD backends:** WebRTC VAD and Silero VAD (README.md:172-174); recorder smoke tests use the `silero-onnx-cpu` extra for a local VAD backend (README.md:72-73).
- **Wake-word backends:** Porcupine or OpenWakeWord, optional (README.md:172-174).
- **Delivery modes:** blocking single utterance (`recorder.text()`), continuous dictation with `text(callback)`, external-audio feed plus `text()` plus `shutdown()` (README.md:106-158).

Key query (verbatim, README.md:147-158): feed external PCM and finalize:

```python
from RealtimeSTT import AudioToTextRecorder

if __name__ == "__main__":
    recorder = AudioToTextRecorder(use_microphone=False)

    with open("audio_chunk.pcm", "rb") as audio_file:
        recorder.feed_audio(audio_file.read(), original_sample_rate=16000)

    print(recorder.text())
    recorder.shutdown()
```

## 4. LLM / External Service Integration

No hosted LLM/chat API is on the default path. Transcription is local-model inference (`faster_whisper` default; `sherpa-onnx`, `kroko_onnx`, and other engines via extras), not a remote LLM call (README.md:15-17, README.md:21-31, README.md:58-77). One engine reference is a remote transcription API: Cohere Transcribe, listed among engine-specific references in `docs/engines/cohere.md` (README.md:209-221); the wiki excerpt gives no endpoint, key, or call-shape details, so authentication and required-vs-optional call semantics for that engine are not asserted here.

External-service-adjacent behavior documented in the wiki: the production server is a self-hosted FastAPI surface (versioned HTTP/WebSocket, bearer-token auth), not a third-party SaaS dependency (README.md:225-230); the `server` extra includes the local Silero ONNX VAD runtime used by legacy recorder-backed server paths, and the versioned production WebSocket path needs no interactive Torch Hub download at startup (README.md:242-245). Kroko commercial options exist for production licensing and higher-end models, with public Community models for local testing (README.md:64-65).

Environment variables surfaced in the wiki:

| Variable | Required? | Purpose |
|---|---|---|
| `REALTIMESTT_SERVER_BEARER_TOKEN` | Required for direct non-loopback binds and for authenticated deployments; replaces removed bearer-token CLI flags (`RELEASE_NOTES.md:385-413`) | Bearer token for the production server (README.md:228-230) |

No other env vars (e.g. engine API keys) are enumerated in the covered pages; engine setup links live in `docs/transcription-engines.md` and per-engine docs (README.md:191-192, README.md:209-221).

## 5. The Record-Detect-Transcribe Pipeline

Primary workflow: single-utterance capture → VAD segmentation → engine transcription → final text, with optional realtime partials, wake-word gating, and remote serving. Every function below is cited to the README lines given in the wiki; internal module/function line numbers are not in the covered pages and are omitted rather than guessed.

1. **Construct recorder** — `AudioToTextRecorder(...)` (README.md:106-116); all constructor parameters documented in `docs/configuration.md` (README.md:165-168). External-audio variant: `AudioToTextRecorder(use_microphone=False)` (README.md:147-158).
2. **Feed audio (external mode only)** — `feed_audio(bytes, original_sample_rate=...)` with 16-bit mono PCM at 16 kHz or an original rate for resampling (README.md:143-158).
3. **Detect speech** — WebRTC/Silero VAD segments the utterance; optional Porcupine/OpenWakeWord gate precedes transcription (README.md:172-174). Multiprocessing guard `if __name__ == "__main__":` is recommended, especially on Windows, because model work uses multiprocessing (README.md:118-119).
4. **Emit realtime partials (optional)** — streaming engines (e.g. Nemotron) process only new frames during the turn for replaceable live text (README.md:28-31); realtime behavior is configured via the parameters in `docs/configuration.md` (README.md:165-168) with callbacks for realtime text (README.md:176-177).
5. **Finalize transcript** — `text()` blocks for one utterance (README.md:106-116); `text(process_text)` runs transcription asynchronously while the loop keeps listening (README.md:122-139); the CPU profile refines the complete turn once with Parakeet at finalization (README.md:28-31); `shutdown()` tears down the external-audio recorder (README.md:147-158).
6. **Serve remotely (optional)** — install `RealtimeSTT[server,...]`, install model bundles (`stt-install-sherpa-models --root ./models/sherpa-onnx --model all`, README.md:247-249), start with `stt-server-production --host 127.0.0.1 --port 8010` (README.md:232-235), full recipe in `RealtimeSTT_server/PRODUCTION_SERVER.md` (README.md:251-252).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `README.md` | cited ranges :9-269 | Library purpose, engine profiles, install, usage patterns, features, docs map, server recipe, license/author |
| `RELEASE_NOTES.md` | 313 (`RELEASE_NOTES.md:1-313`) | Release history `1.0.3`–`1.1.2`; Preview contracts, turn-state-machine change, auth change (excerpt truncated inside `1.0.3`) |
| `requirements.txt` | 15 (`requirements.txt:1-15`) | Default CPU dependency pins (faster-whisper, VAD, audio, websocket) |
| `requirements-gpu.txt` | 15 (`requirements-gpu.txt:1-15`) | GPU-variant pins; notes Silero VAD stays CPU ONNX even with GPU ASR (`requirements-gpu.txt:12-13`) |
| `requirements-gpu-torch.txt` | 4 (`requirements-gpu-torch.txt:1-4`) | CUDA torch/torchaudio pins from the `cu128` index |
| `MANIFEST.in` | 19 (`MANIFEST.in:1-19`) | sdist include/prune rules |
| `.gitignore` | 221 | Excludes local/dev, packaging, test, diagnostic, secret, IDE artifacts |
| `.dockerignore` | 5 (`.dockerignore:1-5`) | Docker build-context exclusions |
| `install_with_gpu_support.bat` | 2 (`install_with_gpu_support.bat:1-2`) | Windows GPU stack install sequence |
| `win_installgpu_virtual_env.bat` | 14 (`win_installgpu_virtual_env.bat:1-14`) | Windows venv create/activate + GPU install chain |
| `docs/configuration.md` | pointer (README.md:165-168, README.md:189-190) | Complete `AudioToTextRecorder` parameter reference |
| `docs/custom-transcription-engines.md` | pointer (README.md:193-194) | Public engine base class, executor integration, streaming sessions |
| `docs/engines/kroko-onnx.md` | pointer (README.md:75-77) | Kroko-ONNX engine guide |
| `RealtimeSTT_server/PRODUCTION_SERVER.md` | pointer (README.md:40-42, README.md:202-203, README.md:251-252) | Authenticated HTTP/WebSocket deployment recipe and limits |
| `docs/fastapi-server.md` | pointer (README.md:200-201, README.md:254-256) | Browser/reference-server protocol, metrics, engine recipes |
| `docs/quick-start.md`, `docs/external-audio.md` | pointers (README.md:160-161, README.md:185-186, README.md:196) | Short demos, recording patterns, microphone-less feeding |
| `docs/installation.md`, `docs/testing.md`, `docs/test-scripts.md`, `docs/troubleshooting.md`, `docs/licenses.md`, `docs/wake-words.md`, `docs/transcription-engines.md` | pointers (README.md:187-208) | Platform/CUDA setup, unit vs. golden tests, demos/regressions, error catalog, license notes, wake-word and engine setup |
| `example_fastapi_server/` | pointer (README.md:254-256) | Interactive browser reference app for source checkouts (not the packaged production server) |
| `tests/realtimestt_test.py` | pointer (README.md:54) | CLI demo reproducing the demo video |

## 7. Dependencies

Required-first order follows the default CPU install (`requirements.txt:1-15`), then GPU-variant deltas. Constraint strings are exact as reported in the wiki.

| Package | Version constraint | Purpose |
|---|---|---|
| `PyAudio` | `==0.2.14` | Microphone/audio I/O |
| `faster-whisper` | `==1.2.1` (CPU) / `==1.1.1` (GPU file) | Default general-purpose transcription engine |
| `pvporcupine` | `==1.9.5` | Porcupine wake-word backend |
| `webrtcvad-wheels` | `==2.0.14` | WebRTC VAD |
| `halo` | `==0.0.31` | CLI spinner/status output |
| `colorama` | `==0.4.6` (CPU file only) | Terminal color output |
| `torch` | unpinned (CPU) / `==2.7.1+cu128` via `--index-url https://download.pytorch.org/whl/cu128` (GPU) | Model runtime |
| `torchaudio` | unpinned (CPU) / `==2.7.1+cu128` (GPU) | Audio tensor utilities |
| `scipy` | `==1.17.1` (CPU) / `==1.15.2` (GPU) | Signal processing / resampling support |
| `openwakeword` | `>=0.6.0` (CPU) / `>=0.4.0` (GPU) | OpenWakeWord wake-word backend |
| `websockets` | `==16.0` (CPU) / `==14.1` (GPU) | Server/streaming transport |
| `websocket-client` | `==1.9.0` (CPU) / `==1.8.0` (GPU) | Client-side websocket support |
| `soundfile` | `==0.13.1` | Audio file decoding |
| `silero-vad[onnx-cpu]` | `>=6.2.1; python_version >= "3.8"` | Silero VAD via CPU ONNX Runtime, including GPU installs |
| `numpy` | `<2.0.0` (GPU file only) | Numeric array compatibility pin |
| Optional extras (names only in wiki) | `server`, `sherpa-onnx`, `faster-whisper`, `kroko-builder`, `silero-onnx-cpu` (README.md:35-38, README.md:67-73, README.md:84-86, README.md:232-241) | Production server, Sherpa-ONNX CPU streaming stack, faster-whisper engine, Kroko builder, local Silero VAD backend |

## 8. CLI / Usage Surface

Entry points (commands verbatim from the wiki):

| Command | Install prerequisite | Effect |
|---|---|---|
| `pip install "RealtimeSTT[faster-whisper]"` (README.md:84-86) | PortAudio headers: `sudo apt-get install python3-dev portaudio19-dev` on Linux (README.md:88-93); `brew install portaudio` on macOS (README.md:95-99) | Base install |
| `python -m pip install "RealtimeSTT[server,sherpa-onnx]"` + `stt-install-sherpa-models --root ./models/sherpa-onnx --model all` (README.md:35-38, README.md:247-249) | Persistent storage for model bundles | CPU INT8 server stack install (Nemotron-live + Parakeet-final) |
| `pip install "RealtimeSTT[kroko-builder,silero-onnx-cpu]"` + `stt-install-kroko --build` (README.md:67-70) | — | Kroko-ONNX engine build plus local VAD backend for recorder smoke tests |
| `stt-server-production --host 127.0.0.1 --port 8010` (README.md:232-235) | `python -m pip install "RealtimeSTT[server,faster-whisper]"` (README.md:232-235) | Start packaged production server on loopback |
| `tests/realtimestt_test.py` (README.md:54) | — | CLI demo reproducing the demo video |

Python surface: `from RealtimeSTT import AudioToTextRecorder`; `AudioToTextRecorder()` / `AudioToTextRecorder(use_microphone=False)`; `recorder.text()` / `recorder.text(callback)`; `recorder.feed_audio(bytes, original_sample_rate=...)`; `recorder.shutdown()`; context-manager use (`with AudioToTextRecorder() as recorder:`) (README.md:106-158).

Environment variables:

| Variable | Values / default | Purpose |
|---|---|---|
| `REALTIMESTT_SERVER_BEARER_TOKEN` | secret string; no default in wiki | Production-server bearer token; required with Uvicorn TLS cert/key for direct non-loopback binds; reverse-proxy deployments keep the server on loopback and terminate TLS at the proxy (README.md:228-230; flag-to-env migration in `RELEASE_NOTES.md:385-413`) |

Configuration: every `AudioToTextRecorder` constructor parameter is documented in `docs/configuration.md` (model/engine selection, realtime transcription, VAD timing, wake words, callbacks, external audio, logging, executor injection) (README.md:165-168). No config-file format is described in the covered pages.

## 9. Extensibility Points

- **Custom transcription engines** — implement the public engine base class and follow the executor-integration, streaming-session, and contribution guide in `docs/custom-transcription-engines.md` (README.md:193-194). Engine selection and setup links live in `docs/transcription-engines.md` plus per-engine docs (`docs/engines/*`, e.g. `docs/engines/kroko-onnx.md`) (README.md:191-192, README.md:209-221, README.md:75-77).
- **Executor injection** — pass a custom executor through the `AudioToTextRecorder` constructor parameters documented in `docs/configuration.md` (README.md:165-168); wiki gives no class/function line numbers.
- **Realtime vs. final engine pairing** — configure the realtime/live model separately from the final model (Nemotron-streaming + Parakeet-final is the documented CPU production pairing, README.md:23-31).
- **VAD / wake-word backends** — choose WebRTC vs. Silero VAD and Porcupine vs. OpenWakeWord; setup in `docs/wake-words.md` (README.md:195); recorder smoke tests use the `silero-onnx-cpu` extra (README.md:72-73).
- **Server and protocol** — extend or embed via the packaged production server recipe (`RealtimeSTT_server/PRODUCTION_SERVER.md`, README.md:40-42, README.md:251-252) or the interactive reference app (`example_fastapi_server`, `docs/fastapi-server.md`, README.md:254-256).
- **External audio sources** — build file/stream/websocket/foreign-process feeders on `use_microphone=False` + `feed_audio()` per `docs/external-audio.md` (README.md:143-161, README.md:196).

## 10. Limitations and Gotchas

- **Python version ceiling.** CI covers 3.11 and 3.12; Python 3.13+ is explicitly not a release target until dependency and CI gates exist (README.md:81-82). Running on newer interpreters is unsupported per the covered pages.
- **Native audio prerequisite.** Linux requires PortAudio headers (`sudo apt-get install python3-dev portaudio19-dev`, README.md:88-93) and macOS requires `brew install portaudio` (README.md:95-99) before the package installs/uses the microphone path.
- **Windows multiprocessing guard.** The `if __name__ == "__main__":` guard is recommended especially on Windows because model work uses multiprocessing (README.md:118-119); omitting it risks spawn-loop failures.
- **Non-loopback serving requires token plus TLS files.** Direct non-loopback binds need both a bearer token (`REALTIMESTT_SERVER_BEARER_TOKEN`) and Uvicorn TLS certificate/key files; the documented alternative is loopback bind behind a TLS-terminating reverse proxy (README.md:228-230).
- **Engine extras are not automatic.** Non-default engines require install extras with their optional dependencies and models (README.md:15-17); CPU streaming needs both pinned Sherpa bundles installed to persistent storage before following the server recipe (README.md:237-249); Kroko needs `stt-install-kroko --build` (README.md:67-70).
- **Coverage truncation.** `RELEASE_NOTES.md` content past the `1.0.3` notes was cut in the chunk (`... (truncated, 4302 more characters)`), so late `1.0.3` details are not covered in the wiki excerpt.

## 11. How It Compares to Alternatives

The wiki names the underlying engines RealtimeSTT wraps rather than end-to-end competitors; the fair comparison is therefore RealtimeSTT (integration + VAD + realtime/final split + server) versus using each engine directly:

- **openai-whisper / faster-whisper** (engine refs, README.md:209-221; `faster-whisper==1.2.1` default in `requirements.txt:1-15`): raw Whisper inference without recorder VAD, wake words, realtime partials, or the production server; RealtimeSTT keeps `faster_whisper` as its general-purpose GPU path (README.md:21-22) and adds those layers.
- **whisper.cpp / transcribe-cpp** (engine refs, README.md:209-221): portable low-dependency inference, but no `AudioToTextRecorder` callback/event model or versioned HTTP/WebSocket deployment contract (README.md:176-180).
- **sherpa-onnx (+ Parakeet NeMo)** (engine refs, README.md:209-221; recommended CPU pair README.md:23-31): streaming-capable runtimes RealtimeSTT composes as Nemotron-live plus Parakeet-final with new-frames-only streaming and single finalization pass; used standalone they leave turn ownership, session isolation, and auth to the integrator.
- **FunASR / Moonshine / Meta Omnilingual ASR / Granite-Qwen Transformers / Cohere Transcribe** (engine refs, README.md:209-221): additional selectable engines inside RealtimeSTT's abstraction rather than replacements for it; Cohere Transcribe is the remote-API option among otherwise local engines.

Positioning: RealtimeSTT competes as a batteries-included Python recorder-to-server integration over swappable ASR engines, not as a new acoustic model; choose it when VAD-gated turns, realtime-plus-final transcripts, wake words, and a deployable server matter more than direct control of a single inference runtime.

## Appendix: Selected Code Snippets

1. Microphone single utterance (README.md:106-116):

```python
from RealtimeSTT import AudioToTextRecorder

if __name__ == "__main__":
    with AudioToTextRecorder() as recorder:
        print("Speak now")
        print(recorder.text())
```

2. Continuous dictation with callback (README.md:122-139):

```python
from RealtimeSTT import AudioToTextRecorder


def process_text(text):
    print(text)


if __name__ == "__main__":
    recorder = AudioToTextRecorder()

    while True:
        recorder.text(process_text)
```

3. External-audio feed (README.md:147-158):

```python
from RealtimeSTT import AudioToTextRecorder

if __name__ == "__main__":
    recorder = AudioToTextRecorder(use_microphone=False)

    with open("audio_chunk.pcm", "rb") as audio_file:
        recorder.feed_audio(audio_file.read(), original_sample_rate=16000)

    print(recorder.text())
    recorder.shutdown()
```

4. CPU server-stack install and start (README.md:35-38, README.md:232-235, README.md:247-249):

```bash
python -m pip install "RealtimeSTT[server,sherpa-onnx]"
stt-install-sherpa-models --root ./models/sherpa-onnx --model all
stt-server-production --host 127.0.0.1 --port 8010
```
