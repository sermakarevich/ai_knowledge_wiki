> [[index|Wiki]] | [[summary|Summary]]
# KoljaB/RealtimeSTT — Digest

## 1. [[wiki/01-overview|Overview]]
**In one sentence:** RealtimeSTT is a Python speech-to-text library that turns microphone or application-fed audio into final plus optional realtime transcripts using voice activity detection, selectable engines, wake words, and an optional production server.
## Key points
- RealtimeSTT targets assistants, dictation tools, browser streaming servers, and prototypes that need speech-to-text in a few lines of code, with voice activity detection, fast transcription, optional realtime text updates, wake words, and direct audio-stream access (README.md:9-13).
- The general-purpose default transcription path uses `faster_whisper`, with other engines available through install extras when optional dependencies and models are present (README.md:15-17).
- The recommended GPU profile keeps the established `faster_whisper` CUDA setup as the general-purpose path, while the recommended CPU streaming profile pairs `sherpa-onnx-nemotron-3.5-asr-streaming-0.6b-560ms-int8` for realtime text with `sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8` for the authoritative final transcript (README.md:21-31).
- The library supports direct microphone input via `AudioToTextRecorder` as well as application-fed audio with `use_microphone=False` plus `feed_audio()` for 16-bit mono PCM at 16 kHz or resampled from an original rate (README.md:110-116, README.md:143-158).
- Voice activity detection uses WebRTC VAD and Silero VAD, and wake-word activation optionally uses Porcupine or OpenWakeWord (README.md:172-174).
- Event callbacks cover recording, VAD, realtime text, transcription, and wake-word state (README.md:176-177).
- The packaged production FastAPI server provides versioned HTTP/WebSocket contracts, session isolation, bounded shared inference resources, authentication, and readiness/capabilities endpoints, binds loopback by default, and requires a bearer token plus Uvicorn TLS files for direct non-loopback binds (README.md:178-180, README.md:225-230).
- CI covers Python 3.11 and 3.12, with Python 3.13+ explicitly not a release target until dependency and CI gates exist (README.md:81-82).

## 2. [[wiki/02-top-level-files|Top-Level Files]]
**In one sentence:** The repo root's loose files define build/docker ignores, sdist packaging rules, CPU/GPU dependency pins, Windows GPU install scripts, and the versioned release history.
## Key points
- `.dockerignore` (5 lines) excludes `__pycache__`, `.cache`, `.dockerignore`, `docker-compose.yml`, and `Dockerfile` from the Docker build context (`.dockerignore:1-5`).
- `.gitignore` (221 lines) keeps local/dev, packaging, test, diagnostic, secret, and IDE artifacts out of version control, including `examples/`, `batch/`, `test_env/`, `tests_private/`, `docs_private/`, `server/`, and `*.pem`/`*.key`/`*.p12`/`*.pfx` (`.gitignore:18-67`).
- `MANIFEST.in` (19 lines) ships `requirements.txt`, `README.md`, `RELEASE_NOTES.md`, and `LICENSE` in the sdist while pruning `docs/development`, `dev-log`, `roadmap`, `test-model-cache`, `test-results`, `docs_private`, `docs/handoffs`, and `tests_private` (`MANIFEST.in:1-13`).
- `requirements.txt` (15 lines) pins the default CPU install, e.g. `faster-whisper==1.2.1`, `scipy==1.17.1`, `websockets==16.0`, `websocket-client==1.9.0`, plus unpinned `torch`/`torchaudio` (`requirements.txt:1-15`).
- `requirements-gpu.txt` (15 lines) plus `requirements-gpu-torch.txt` (4 lines) define the GPU variant: `torch==2.7.1+cu128` / `torchaudio==2.7.1+cu128` from the `cu128` index plus `faster-whisper==1.1.1` and `scipy==1.15.2` (`requirements-gpu-torch.txt:1-4`, `requirements-gpu.txt:1-15`).
- `install_with_gpu_support.bat` (2 lines) installs the GPU stack via `pip install -r requirements-gpu-torch.txt` then `pip install -r requirements-gpu.txt`, and `win_installgpu_virtual_env.bat` (14 lines) creates/activates `test_env` and chains into it (`install_with_gpu_support.bat:1-2`, `win_installgpu_virtual_env.bat:1-14`).
- `RELEASE_NOTES.md` (313 lines) records releases `1.0.3` through `1.1.2` with Added/Changed/Fixed sections and explicit release boundaries; the chunk excerpt is truncated after the `1.0.3` notes, so content past that point was cut instead of guessed (`RELEASE_NOTES.md:1-313`).

## The system in five moves
1. RealtimeSTT presents a few-lines-of-code Python API (`AudioToTextRecorder`) that converts microphone or fed-in PCM audio into final plus optional realtime transcripts.
2. Voice activity detection (WebRTC/Silero) segments speech while selectable engines — `faster_whisper` by default, Nemotron-live plus Parakeet-final on CPU, Kroko and others via extras — produce realtime and authoritative text with wake-word gating.
3. Event callbacks, external-audio feeding, and documented engine/configuration guides wire the library into assistants, dictation tools, and browser streaming servers.
4. A packaged production FastAPI server hardens this into versioned HTTP/WebSocket contracts with session isolation, bounded inference resources, auth, and loopback-by-default TLS discipline.
5. The repo root pins the whole stack for reproduction: ignore rules and sdist manifest for clean builds, CPU/GPU requirement files plus Windows GPU scripts for installs, and a versioned release history from 1.0.3 to 1.1.2.
