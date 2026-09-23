[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
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
---
## Purpose and default engine
RealtimeSTT is described as a Python speech-to-text library for applications needing voice activity detection, fast transcription, optional realtime text updates, wake words, and direct access to audio streams (README.md:9-11). Intended uses are assistants, dictation tools, browser streaming servers, and prototypes needing speech-to-text with only a few lines of code (README.md:11-13). The general-purpose default path uses `faster_whisper`; other engines require install extras with their optional dependencies and models (README.md:15-17).
## Recommended engine profiles
- **CUDA / GPU:** keep the established `faster_whisper` CUDA setup as the recommended general-purpose GPU path (README.md:21-22).
- **CPU:** production streaming on Linux x86-64 strongly recommends `sherpa-onnx-nemotron-3.5-asr-streaming-0.6b-560ms-int8` for fast replaceable realtime text together with `sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8` for the single authoritative final transcript (README.md:23-27). Nemotron processes only new audio frames during the turn; Parakeet refines the complete turn once at finalization, avoiding repeated retranscription of a growing buffer while preserving final quality (README.md:28-31).

| Profile | Realtime / live model | Final model | Notes |
|---|---|---|---|
| CUDA / GPU | `faster_whisper` | `faster_whisper` | Established general-purpose GPU path (README.md:21-22) |
| CPU Linux x86-64 | `sherpa-onnx-nemotron-3.5-asr-streaming-0.6b-560ms-int8` | `sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8` | New-frames-only streaming + single finalization pass (README.md:23-31) |

CPU server stack install (verbatim, README.md:35-38):
```bash
python -m pip install "RealtimeSTT[server,sherpa-onnx]"
stt-install-sherpa-models --root ./models/sherpa-onnx --model all
```
The authenticated HTTP/WebSocket deployment recipe and pinned model directories are in `RealtimeSTT_server/PRODUCTION_SERVER.md` (README.md:40-42).
## Kroko/Banafo integration
RealtimeSTT includes native support for `kroko_onnx`, the local streaming ASR engine from the Kroko/Banafo team, positioned as fast accurate local speech recognition (README.md:58-62). Start with public Community models for local testing; commercial options exist for production licensing and higher-end models (README.md:64-65). Verbatim install (README.md:67-70):
```bash
pip install "RealtimeSTT[kroko-builder,silero-onnx-cpu]"
stt-install-kroko --build
```
The `silero-onnx-cpu` extra gives `AudioToTextRecorder` a local VAD backend for recorder-based smoke tests and live microphone use (README.md:72-73). Guides: `docs/engines/kroko-onnx.md`, Kroko ASR docs, and `kroko-onnx` on GitHub (README.md:75-77).
## Install
Base install (verbatim, README.md:84-86):
```bash
pip install "RealtimeSTT[faster-whisper]"
```
Platform prerequisites: CI matrix covers Python 3.11 and 3.12; Python 3.13 and newer are not release targets until dependency and CI gates are available (README.md:81-82). On Linux install PortAudio headers before the package (README.md:88-93):
```bash
sudo apt-get update
sudo apt-get install python3-dev portaudio19-dev
```
On macOS (README.md:95-99):
```bash
brew install portaudio
```
CUDA, platform notes, and optional engine stacks are in `docs/installation.md` (README.md:101-102).
## Usage examples
Microphone single-utterance example — waits for speech, stops after the detected utterance, prints the final transcript (README.md:106-116):
```python
from RealtimeSTT import AudioToTextRecorder

if __name__ == "__main__":
    with AudioToTextRecorder() as recorder:
        print("Speak now")
        print(recorder.text())
```
Continuous dictation passes a callback to `text()` so transcription completes asynchronously while the loop keeps listening (README.md:122-139):
```python
from RealtimeSTT import AudioToTextRecorder


def process_text(text):
    print(text)


if __name__ == "__main__":
    recorder = AudioToTextRecorder()

    while True:
        recorder.text(process_text)
```
External-audio mode sets `use_microphone=False` when audio comes from a file, stream, websocket, or another process; feed 16-bit mono PCM chunks at 16 kHz or pass the original sample rate for resampling (README.md:143-145). Verbatim pattern (README.md:147-158):
```python
from RealtimeSTT import AudioToTextRecorder

if __name__ == "__main__":
    recorder = AudioToTextRecorder(use_microphone=False)

    with open("audio_chunk.pcm", "rb") as audio_file:
        recorder.feed_audio(audio_file.read(), original_sample_rate=16000)

    print(recorder.text())
    recorder.shutdown()
```
Exact parameter names surfaced here: `use_microphone`, `feed_audio`, `original_sample_rate`, `text`, `shutdown` (README.md:143-158). The `if __name__ == "__main__":` guard is recommended especially on Windows because RealtimeSTT uses multiprocessing for model work (README.md:118-119). More examples are in `docs/quick-start.md` and `docs/external-audio.md` (README.md:160-161). Every `AudioToTextRecorder` constructor parameter is documented in `docs/configuration.md`, covering model/engine selection, realtime transcription, VAD timing, wake words, callbacks, external audio, logging, and executor injection (README.md:165-168).
## Features
Verbatim feature list (README.md:172-181):
- Voice activity detection with WebRTC VAD and Silero VAD.
- Final and realtime transcription with selectable engines.
- Optional wake word activation through Porcupine or OpenWakeWord.
- Direct microphone input or application-fed audio chunks.
- Event callbacks for recording, VAD, realtime text, transcription, and wake word state.
- A packaged production FastAPI server with versioned HTTP/WebSocket contracts, session isolation, bounded shared inference resources, authentication, and readiness/capabilities endpoints.
- A browser streaming reference app for source checkouts.
## Documentation map
The chunk lists these entry points (README.md:185-221):

| Doc | Covers |
|---|---|
| `docs/quick-start.md` | Shortest demos and common recording patterns (README.md:185-186) |
| `docs/installation.md` | Platform setup, CUDA notes, optional dependencies (README.md:187-188) |
| `docs/configuration.md` | Complete `AudioToTextRecorder` parameter reference (README.md:189-190) |
| `docs/transcription-engines.md` | Engine selection and setup links (README.md:191-192) |
| `docs/custom-transcription-engines.md` | Public base class, executor integration, streaming sessions, contribution guide (README.md:193-194) |
| `docs/wake-words.md` | Porcupine and OpenWakeWord setup (README.md:195) |
| `docs/external-audio.md` | Feeding audio without a microphone (README.md:196) |
| `docs/testing.md` | Maintained unit and opt-in golden test workflow (README.md:197) |
| `docs/test-scripts.md` | Demos, manual tests, regressions, legacy experiments under `tests/` (README.md:198-199) |
| `docs/fastapi-server.md` | Browser server configuration, protocol, metrics, deployment notes (README.md:200-201) |
| `RealtimeSTT_server/PRODUCTION_SERVER.md` | Packaged remote HTTP/WebSocket API, authentication, limits, deployment recipe (README.md:202-203) |
| `docs/troubleshooting.md` | Install, audio, CUDA, model, dependency, runtime errors (README.md:204-205) |
| `docs/licenses.md` | License notes for optional engine runtimes and model families (README.md:206-207) |

Engine-specific references: `faster-whisper`, `whisper.cpp`, OpenAI Whisper, Moonshine, `sherpa-onnx`, Kroko-ONNX, Parakeet NeMo, Meta Omnilingual ASR, Granite/Qwen Transformers engines, Cohere Transcribe, FunASR (README.md:209-221).
## Production server
The supported remote server is an optional install, binds loopback by default, and exposes versioned health, readiness, capabilities, raw-PCM final transcription, and ordered streaming WebSocket endpoints (README.md:225-227). Direct non-loopback binds require both a bearer token and Uvicorn TLS certificate/key files; reverse-proxy deployments keep the server on loopback and terminate TLS at the proxy (README.md:228-230). Verbatim start (README.md:232-235):
```bash
python -m pip install "RealtimeSTT[server,faster-whisper]"
stt-server-production --host 127.0.0.1 --port 8010
```
CPU INT8 deployment repeats the Nemotron-live plus Parakeet-final pairing; install `RealtimeSTT[server,sherpa-onnx]` and both pinned model bundles into persistent storage before following the server recipe (README.md:237-241). The `server` extra includes the local Silero ONNX VAD runtime used by legacy recorder-backed server paths; the versioned production WebSocket path owns its turn state and does not derive finalization from recorder VAD, so production startup needs no interactive Torch Hub download (README.md:242-245). Model install verbatim (README.md:247-249):
```bash
stt-install-sherpa-models --root ./models/sherpa-onnx --model all
```
Full recipe: `RealtimeSTT_server/PRODUCTION_SERVER.md` (README.md:251-252). The interactive browser reference app remains in `example_fastapi_server` for source checkouts; its UI, engine recipes, protocol, and metrics are in `docs/fastapi-server.md` (README.md:254-256).
## Contributing, license, author
Focused tests and small changes are easiest to review; fast unit tests are kept separate from opt-in real-model tests per `docs/testing.md` (README.md:260-261). License: MIT (README.md:263-265). Author: Kolja Beigel (README.md:267-269). The CLI demo reproducing the demo video is `tests/realtimestt_test.py` (README.md:54).
**Covers:** README.md (library purpose, engine profiles, install, microphone/automatic/external-audio examples, configuration pointer, features, documentation map, production server, contributing/license/author)
