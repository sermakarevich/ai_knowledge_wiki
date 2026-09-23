> PDF location: https://github.com/KoljaB/RealtimeSTT (no source.pdf fetched; repo source — see Source field below)

# KoljaB/RealtimeSTT
Source: https://github.com/KoljaB/RealtimeSTT
Kind: repo
Fetched: 2026-09-22T14:39:53.885252+00:00
Tool: git-clone

# KoljaB/RealtimeSTT

Commit: 777727553eedfa19aead15337ce66bab549add3f

## README

# RealtimeSTT

RealtimeSTT is a Python speech-to-text library for applications that need
voice activity detection, fast transcription, optional realtime text updates,
wake words, and direct access to audio streams. It is designed for assistants,
dictation tools, browser streaming servers, and prototypes that need to turn
speech into text with only a few lines of code.

The general-purpose default path uses `faster_whisper`. Other engines are
available through install extras when their optional dependencies and models
are present.

## Recommended Engine Profiles

- **CUDA / GPU:** Keep using the established `faster_whisper` CUDA setup. It
  remains the recommended general-purpose GPU path.
- **CPU:** For production streaming on Linux x86-64, the strongly recommended
  profile is
  `sherpa-onnx-nemotron-3.5-asr-streaming-0.6b-560ms-int8` for fast,
  replaceable realtime text together with
  `sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8` for the single authoritative
  final transcript. Nemotron processes only new audio frames during the turn;
  Parakeet then refines the complete turn once at finalization. This pairing
  provides substantially better CPU streaming behavior than repeatedly
  retranscribing a growing audio buffer while preserving a high-quality final.

Install the CPU server stack and both pinned model bundles with:

```bash
python -m pip install "RealtimeSTT[server,sherpa-onnx]"
stt-install-sherpa-models --root ./models/sherpa-onnx --model all
```

See the [production server guide](RealtimeSTT_server/PRODUCTION_SERVER.md) for
the authenticated HTTP/WebSocket deployment recipe and exact pinned model
directories.

### Support RealtimeSTT

If RealtimeSTT saved you time, one GitHub star is a simple way to help make it more stable.

Stars improve visibility and visibility brings more users, more real-world testing, more bug reports, more fixes, and better releases for everyone.

## Demo

https://github.com/user-attachments/assets/797e6552-27cd-41b1-a7f3-e5cbc72094f5

[CLI demo code (reproduces the video above)](tests/realtimestt_test.py)

## Featured Integration: Kroko/Banafo ASR

RealtimeSTT includes native support for `kroko_onnx`, the local streaming ASR
engine from the Kroko/Banafo team.

This integration has been on my wishlist for a long time. Kroko is a strong fit
for RealtimeSTT's goals: fast, accurate local speech recognition.

Start with the public Community models for local testing, or see Kroko/Banafo's
commercial model options if you need production licensing and higher-end models.

```bash
pip install "RealtimeSTT[kroko-builder,silero-onnx-cpu]"
stt-install-kroko --build
```

The `silero-onnx-cpu` extra gives `AudioToTextRecorder` a local VAD backend for
recorder-based smoke tests and live microphone use.

See the [Kroko-ONNX engine guide](docs/engines/kroko-onnx.md),
[Kroko ASR docs](https://docs.kroko.ai/on-premise/), and
[kroko-onnx on GitHub](https://github.com/kroko-ai/kroko-onnx).

## Install

The current CI matrix covers Python 3.11 and 3.12. Python 3.13 and newer are
not release targets until dependency and CI gates are available.

```bash
pip install "RealtimeSTT[faster-whisper]"
```

On Linux, install PortAudio headers before installing the package:

```bash
sudo apt-get update
sudo apt-get install python3-dev portaudio19-dev
```

On macOS:

```bash
brew install portaudio
```

For CUDA, platform notes, and optional engine stacks, see
[docs/installation.md](docs/installation.md).

## Microphone Example

This waits for speech, stops after the detected utterance, and prints the final
transcript:

```python
from RealtimeSTT import AudioToTextRecorder

if __name__ == "__main__":
    with AudioToTextRecorder() as recorder:
        print("Speak now")
        print(recorder.text())
```

Use the `if __name__ == "__main__":` guard when running scripts, especially on
Windows, because RealtimeSTT uses multiprocessing for model work.

## Automatic Recording Loop

For continuous dictation, pass a callback to `text()` so transcription work can
complete asynchronously while your loop keeps listening:

```python
from RealtimeSTT import AudioToTextRecorder


def process_text(text):
    print(text)


if __name__ == "__main__":
    recorder = AudioToTextRecorder()

    while True:
        recorder.text(process_text)
```

## External Audio

Set `use_microphone=False` when audio comes from a file, stream, websocket, or
another process. Feed 16-bit mono PCM chunks at 16 kHz, or pass the original
sample rate so RealtimeSTT can resample:

```python
from RealtimeSTT import AudioToTextRecorder

if __name__ == "__main__":
    recorder = AudioToTextRecorder(use_microphone=False)

    with open("audio_chunk.pcm", "rb") as audio_file:
        recorder.feed_audio(audio_file.read(), original_sample_rate=16000)

    print(recorder.text())
    recorder.shutdown()
```

More examples are in [docs/quick-start.md](docs/quick-start.md) and
[docs/external-audio.md](docs/external-audio.md).

## Configuration Reference

Every `AudioToTextRecorder` constructor parameter is documented in
[docs/configuration.md](docs/configuration.md), including model/engine
selection, realtime transcription, VAD timing, wake words, callbacks, external
audio, logging, and executor injection.

## Features

- Voice activity detection with WebRTC VAD and Silero VAD.
- Final and realtime transcription with selectable engines.
- Optional wake word activation through Porcupine or OpenWakeWord.
- Direct microphone input or application-fed audio chunks.
- Event callbacks for recording, VAD, realtime text, transcription, and wake
  word state.
- A packaged production FastAPI server with versioned HTTP/WebSocket contracts,
  session isolation, bounded shared inference resources, authentication, and
  readiness/capabilities endpoints.
- A browser streaming reference app for source checkouts.

## Documentation

- [Quick start](docs/quick-start.md): shortest demos and common recording
  patterns.
- [Installation](docs/installation.md): platform setup, CUDA notes, and optional
  dependencies.
- [Configuration](docs/configuration.md): complete `AudioToTextRecorder`
  parameter reference.
- [Transcription engines](docs/transcription-engines.md): engine selection and
  setup links.
- [Custom transcription engines](docs/custom-transcription-engines.md): public
  base class, executor integration, streaming sessions, and contribution guide.
- [Wake words](docs/wake-words.md): Porcupine and OpenWakeWord setup.
- [External audio](docs/external-audio.md): feeding audio without a microphone.
- [Testing](docs/testing.md): maintained unit and opt-in golden test workflow.
- [Test scripts](docs/test-scripts.md): demos, manual tests, regressions, and
  legacy experiments under `tests/`.
- [FastAPI server](docs/fastapi-server.md): browser server configuration,
  protocol, metrics, and deployment notes.
- [Production server](RealtimeSTT_server/PRODUCTION_SERVER.md): packaged remote
  HTTP/WebSocket API, authentication, limits, and deployment recipe.
- [Troubleshooting](docs/troubleshooting.md): common install, audio, CUDA,
  model, dependency, and runtime errors.
- [Engine licenses](docs/licenses.md): license notes for optional engine
  runtimes and model families.

Engine-specific references:

- [faster-whisper](docs/engines/faster-whisper.md)
- [whisper.cpp](docs/engines/whisper-cpp.md)
- [OpenAI Whisper](docs/engines/openai-whisper.md)
- [Moonshine](docs/engines/moonshine.md)
- [sherpa-onnx](docs/engines/sherpa-onnx.md)
- [Kroko-ONNX](docs/engines/kroko-onnx.md)
- [Parakeet NeMo](docs/engines/parakeet-nemo.md)
- [Meta Omnilingual ASR](docs/engines/omnilingual-asr.md)
- [Granite/Qwen Transformers engines](docs/engines/hf-transformers.md)
- [Cohere Transcribe](docs/engines/cohere.md)
- [FunASR](docs/engines/funasr.md)

## Production Server

The supported remote server is packaged as an optional install. It binds to
loopback by default and exposes versioned health, readiness, capabilities,
raw-PCM final transcription, and ordered streaming WebSocket endpoints.
Direct non-loopback binds require both a bearer token and Uvicorn TLS
certificate/key files; for a reverse-proxy deployment, keep the server on
loopback and terminate TLS at the proxy.

```bash
python -m pip install "RealtimeSTT[server,faster-whisper]"
stt-server-production --host 127.0.0.1 --port 8010
```

For CPU INT8 deployment, the recommended pairing is
`sherpa-onnx-nemotron-3.5-asr-streaming-0.6b-560ms-int8` for live hypotheses
and `sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8` for authoritative final
transcription. Install `RealtimeSTT[server,sherpa-onnx]` and both pinned model
bundles into persistent storage before following the server recipe. The
`server` extra includes the local Silero ONNX VAD runtime used by legacy
recorder-backed server paths. The versioned production WebSocket path owns its
turn state and does not derive finalization from recorder VAD, so production
startup does not need an interactive Torch Hub download:

```bash
stt-install-sherpa-models --root ./models/sherpa-onnx --model all
```

See
[PRODUCTION_SERVER.md](RealtimeSTT_server/PRODUCTION_SERVER.md).

The interactive browser reference app remains in `example_fastapi_server` for
source checkouts. See [docs/fastapi-server.md](docs/fastapi-server.md) for its
UI, engine recipes, protocol details, and metrics.

## Contributing

Focused tests and small changes are easiest to review. The project keeps fast
unit tests separate from opt-in real-model tests; see [docs/testing.md](docs/testing.md).

## License

MIT

## Author

Kolja Beigel


## setup.py

```
import os
import re
import shutil

import setuptools
from setuptools.command.build_py import build_py as _build_py


current_version = "1.1.2"


INSTALL_GUIDE = """
RealtimeSTT lets you choose the transcription and wake-word dependencies you
want to install.

Recommended default local Whisper install:

    pip install "realtimestt[recommended]"

Main ASR backend only, without the faster packaged Silero ONNX Runtime VAD:

    pip install "realtimestt[faster-whisper]"

Base recorder/audio runtime, without a transcription engine or wake-word
backend:

    pip install realtimestt

The base install still includes microphone/audio support, WebRTC VAD, recorder
VAD logic, websocket client/server dependencies, and shared audio utilities. It
does not install `faster-whisper`, Porcupine, OpenWakeWord, or another optional
ASR/wake-word backend unless you request the matching extra.

Install multiple extras by separating them with commas:

    pip install "realtimestt[faster-whisper,porcupine]"
    pip install "realtimestt[whisper-cpp,openwakeword]"

Available extras include:

- faster-whisper: default CTranslate2 Whisper backend
- whisper-cpp: whisper.cpp backend through pywhispercpp
- transcribe-cpp: first-party transcribe.cpp Python binding; add the matching CUDA provider separately
- openai-whisper: original OpenAI Whisper Python backend
- sherpa-onnx: sherpa-onnx CPU backends
- server/production-server: versioned FastAPI HTTP and WebSocket ASR server
- silero-vad: packaged Silero model assets and PyTorch wrapper
- silero-onnx/silero-onnx-cpu: fastest Silero VAD CPU ONNX Runtime backend
- silero-onnx-gpu: installs Silero's ONNX GPU runtime extra for experiments
- parakeet: NVIDIA NeMo Parakeet backend
- omnilingual/omnilingual-asr: Meta Omnilingual ASR backend for Linux/WSL2 with Python 3.11.x only; uses omnilingual-asr>=0.2.0 with matching torch/torchaudio builds
- transformers: shared Transformers dependency for Moonshine, Granite, and Cohere
- moonshine, granite, cohere: aliases for the Transformers dependency set
- qwen: Qwen ASR backend
- qwen-vllm: Qwen ASR with vLLM extras
- funasr: experimental FunASR/SenseVoice backend
- kroko-builder: helper command for building/installing Kroko-ONNX plus Hugging Face model downloads
- porcupine: Porcupine wake-word backend
- openwakeword: OpenWakeWord wake-word backend
- wakewords: both wake-word backends
- recommended/default: faster-whisper backend plus fast Silero CPU ONNX VAD
- all: all PyPI-installable optional backends

Install the pinned Nemotron live and Parakeet final model bundles into a
persistent verified cache:

    stt-install-sherpa-models --root ./models/sherpa-onnx --model all

WebRTC VAD is installed with the core package. AudioToTextRecorder also
initializes a Silero VAD path. Install the recommended/default or
silero-onnx-cpu extra for a self-contained local Silero ONNX Runtime backend.

Meta Omnilingual ASR install note: use Linux or WSL2 with Python 3.11.x.
Native Windows cannot run the Omnilingual runtime because fairseq2n has no
Windows wheel, and Python 3.12.x currently cannot resolve omnilingual-asr>=0.2.0
from PyPI because the upstream package metadata excludes normal 3.12 patch
releases.

For live Kroko-ONNX usage, install the builder helper and then build Kroko in
the same Python environment:

    pip install "realtimestt[kroko-builder,silero-onnx-cpu]"
    stt-install-kroko --build

The silero-onnx-cpu extra is not needed to build Kroko-ONNX itself, but
recorder-based Kroko smoke tests and live AudioToTextRecorder use need a local
VAD backend.

On Windows, use Python 3.12 x64 and start Docker Desktop before running the
builder. Check that Docker's Linux engine is available with:

    python --version
    git --version
    docker version

`docker version` must show a Server section. `docker --version` only checks
that the Docker CLI is installed.

If the default builder cache is not writable, use a project-local work
directory:

    stt-install-kroko --build --work-dir .\\kroko-builder-work

The kroko-builder extra includes huggingface_hub. Download a public Community
model after the builder finishes:

    mkdir test-model-cache\\kroko-onnx
    python -c "from huggingface_hub import hf_hub_download; hf_hub_download(repo_id='Banafo/Kroko-ASR', filename='Kroko-EN-Community-64-L-Streaming-001.data', local_dir='test-model-cache/kroko-onnx')"

"""

# Get the absolute path of requirements.txt
req_path = os.path.join(os.path.dirname(__file__), "requirements.txt")

def parse_requirements(filename):
    parsed = {}
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("-"):
                continue
            package = re.split(
                r"\s*(?:===|==|>=|<=|~=|!=|>|<|;)",
                line,
                maxsplit=1,
            )[0].strip()
            parsed[package] = line
    return parsed


def requirement(name, fallback=None):
    return requirements.get(name, fallback or name)


def unique_requirements(items):
    seen = set()
    unique = []
    for item in items:
        normalized = item.lower()
        if normalized not in seen:
            seen.add(normalized)
            unique.append(item)
    return unique


def is_local_backup_file(path):
    filename = os.path.basename(path)
    return " - Kopie" in filename or filename.endswith((".bak", ".tmp"))


class build_py(_build_py):
    def run(self):
        for package_name in ("RealtimeSTT", "RealtimeSTT_server"):
            package_build_dir = os.path.join(
                self.build_lib,
                *package_name.split("."),
            )
            if os.path.isdir(package_build_dir):
                shutil.rmtree(package_build_dir)
        super().run()

    def find_package_modules(self, package, package_dir):
        modules = super().find_package_modules(package, package_dir)
        return [
            (pkg, module, path)
            for pkg, module, path in modules
            if not is_local_backup_file(path)
        ]


requirements = parse_requirements(req_path)

base_requirements = [
    requirement("PyAudio"),
    requirement("webrtcvad-wheels"),
    requirement("halo"),
    requirement("colorama"),
    requirement("torch"),
    requirement("torchaudio"),
    requirement("scipy"),
    requirement("websockets"),
    requirement("websocket-client"),
    requirement("soundfile"),
]

faster_whisper_requirements = [requirement("faster-whisper")]
whisper_cpp_requirements = ["pywhispercpp"]
transcribe_cpp_requirements = ["transcribe-cpp==0.2.1"]
openai_whisper_requirements = ["openai-whisper"]
sherpa_onnx_requirements = ["sherpa-onnx==1.13.4"]
silero_vad_requirements = [
    "silero-vad>=6.2.1; python_version >= '3.8'",
]
silero_onnx_requirements = [
    "silero-vad[onnx-cpu]>=6.2.1; python_version >= '3.8'",
]
silero_onnx_gpu_requirements = [
    "silero-vad[onnx-gpu]>=6.2.1; python_version >= '3.8'",
]
production_server_requirements = [
    "fastapi>=0.115,<1",
    "uvicorn[standard]>=0.30,<1",
    *silero_onnx_requirements,
]
transformers_requirements = ["transformers"]
parakeet_requirements = ["nemo_toolkit[asr]"]
omnilingual_asr_marker = (
    "python_version >= '3.10' and python_version < '3.12' "
    "and platform_system != 'Windows'"
)
omnilingual_asr_requirements = [
    "torch==2.8.0; %s" % omnilingual_asr_marker,
    "torchaudio==2.8.0; %s" % omnilingual_asr_marker,
    "omnilingual-asr>=0.2.0; %s" % omnilingual_asr_marker,
]
qwen_requirements = ["qwen-asr"]
qwen_vllm_requirements = ["qwen-asr[vllm]"]
funasr_requirements = ["funasr"]
kroko_builder_requirements = ["huggingface_hub"]
porcupine_requirements = [requirement("pvporcupine")]
openwakeword_requirements = [requirement("openwakeword")]

all_optional_requirements = unique_requirements(
    faster_whisper_requirements
    + whisper_cpp_requirements
    + transcribe_cpp_requirements
    + openai_whisper_requirements
    +

... (truncated, 4843 more characters)
```

## Top-level layout

- .dockerignore (~5 lines)
- .github/ (dir, 2 files, ~357 lines)
- .gitignore (~220 lines)
- __init__.py (~0 lines)
- docker-compose.yml (~30 lines)
- Dockerfile (~40 lines)
- docs/ (dir, 31 files, ~5491 lines)
- example_app/ (dir, 7 files, ~635 lines)
- example_browserclient/ (dir, 4 files, ~310 lines)
- example_fastapi_server/ (dir, 8 files, ~6894 lines)
- example_webserver/ (dir, 3 files, ~488 lines)
- install_with_gpu_support.bat (~2 lines)
- LICENSE (~21 lines)
- MANIFEST.in (~18 lines)
- README.md (~263 lines)
- RealtimeSTT/ (dir, 57 files, ~20392 lines)
- RealtimeSTT_server/ (dir, 8 files, ~7609 lines)
- RELEASE_NOTES.md (~312 lines)
- requirements-gpu-torch.txt (~3 lines)
- requirements-gpu.txt (~14 lines)
- requirements.txt (~14 lines)
- setup.py (~354 lines)
- tests/ (dir, 114 files, ~40955 lines)
- tools/ (dir, 6 files, ~5103 lines)
- win_installgpu_virtual_env.bat (~13 lines)

