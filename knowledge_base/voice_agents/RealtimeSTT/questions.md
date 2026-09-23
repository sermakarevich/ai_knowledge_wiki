---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: KoljaB/RealtimeSTT

### Q1. What is RealtimeSTT and what is its main entry point?
> [!tip]- Answer
> RealtimeSTT is a Python speech-to-text library for assistants, dictation tools, browser streaming servers, and prototypes that need VAD, fast transcription, wake words, and audio-stream access in a few lines of code. The main entry point is `AudioToTextRecorder`, used for example as `with AudioToTextRecorder() as recorder` followed by `recorder.text()` for a single microphone utterance. See [[wiki/01-overview|Overview]].

### Q2. What are the recommended engine profiles for GPU versus CPU streaming?
> [!tip]- Answer
> The recommended general-purpose GPU path keeps the established `faster_whisper` CUDA setup, while Linux x86-64 CPU production streaming pairs `sherpa-onnx-nemotron-3.5-asr-streaming-0.6b-560ms-int8` for realtime text with `sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8` for the authoritative final transcript. Other engines such as Kroko-ONNX are available through install extras with their optional dependencies and models. See [[wiki/01-overview|Overview]].

### Q3. How do microphone, continuous dictation, and external-audio usage differ?
> [!tip]- Answer
> A single microphone utterance blocks on `recorder.text()` until the detected utterance ends, while continuous dictation passes a callback such as `process_text` to `text()` so transcription completes asynchronously inside a listening loop. External-audio mode constructs the recorder with `use_microphone=False`, feeds 16-bit mono PCM chunks at 16 kHz via `feed_audio()`, then calls `text()` and `shutdown()`. See [[wiki/01-overview|Overview]].

### Q4. What VAD, wake-word, callback, and server features does RealtimeSTT provide?
> [!tip]- Answer
> Voice activity detection uses WebRTC VAD and Silero VAD, wake-word activation optionally uses Porcupine or OpenWakeWord, and event callbacks cover recording, VAD, realtime text, transcription, and wake-word state. The packaged production FastAPI server binds loopback by default and exposes versioned health, readiness, capabilities, raw-PCM final transcription, and ordered streaming WebSocket endpoints with bearer-token plus TLS discipline. See [[wiki/01-overview|Overview]].

### Q5. How do the CPU and GPU dependency pins differ?
> [!tip]- Answer
> The default CPU `requirements.txt` pins `faster-whisper==1.2.1`, `scipy==1.17.1`, `websockets==16.0`, and `websocket-client==1.9.0` with unpinned `torch`/`torchaudio`, while `requirements-gpu.txt` uses `faster-whisper==1.1.1`, `scipy==1.15.2`, older websocket pins, and `numpy<2.0.0`. GPU torch comes from the companion `requirements-gpu-torch.txt` via the `cu128` index with `torch==2.7.1+cu128` and `torchaudio==2.7.1+cu128`, and both variants note Silero VAD stays on CPU ONNX Runtime. See [[wiki/02-top-level-files|Top-Level Files]].

### Q6. What do the ignore rules, packaging manifest, install scripts, and release notes define?
> [!tip]- Answer
> `.dockerignore` excludes five build-context entries and `.gitignore` (221 lines) keeps local, packaging, test, diagnostic, secret, and IDE artifacts — including `*.pem`/`*.key`/`*.p12`/`*.pfx` — out of version control. `MANIFEST.in` ships `requirements.txt`, `README.md`, `RELEASE_NOTES.md`, and `LICENSE` while pruning dev and private directories, the two `.bat` files install the GPU stack (optionally inside a `test_env` venv), and `RELEASE_NOTES.md` records releases `1.0.3` through `1.1.2`. See [[wiki/02-top-level-files|Top-Level Files]].

### Q7. For a Linux x86-64 CPU deployment needing low-latency live captions plus high-quality final transcripts behind a reverse proxy, which setup would you recommend and why?
> [!tip]- Answer
> I would recommend the pinned sherpa-onnx pairing — Nemotron streaming for realtime hypotheses with Parakeet for the single final — installed via `RealtimeSTT[server,sherpa-onnx]` with both model bundles in persistent storage behind the loopback-by-default production server. This fits best because Nemotron processes only new frames during the turn instead of retranscribing a growing buffer, Parakeet still yields one authoritative high-quality final, and keeping the server on loopback with TLS terminated at the proxy matches the documented production posture. See [[wiki/01-overview|Overview]].
