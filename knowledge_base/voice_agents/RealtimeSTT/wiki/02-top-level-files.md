[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-Level Files
**In one sentence:** The repo root's loose files define build/docker ignores, sdist packaging rules, CPU/GPU dependency pins, Windows GPU install scripts, and the versioned release history.
## Key points
- `.dockerignore` (5 lines) excludes `__pycache__`, `.cache`, `.dockerignore`, `docker-compose.yml`, and `Dockerfile` from the Docker build context (`.dockerignore:1-5`).
- `.gitignore` (221 lines) keeps local/dev, packaging, test, diagnostic, secret, and IDE artifacts out of version control, including `examples/`, `batch/`, `test_env/`, `tests_private/`, `docs_private/`, `server/`, and `*.pem`/`*.key`/`*.p12`/`*.pfx` (`.gitignore:18-67`).
- `MANIFEST.in` (19 lines) ships `requirements.txt`, `README.md`, `RELEASE_NOTES.md`, and `LICENSE` in the sdist while pruning `docs/development`, `dev-log`, `roadmap`, `test-model-cache`, `test-results`, `docs_private`, `docs/handoffs`, and `tests_private` (`MANIFEST.in:1-13`).
- `requirements.txt` (15 lines) pins the default CPU install, e.g. `faster-whisper==1.2.1`, `scipy==1.17.1`, `websockets==16.0`, `websocket-client==1.9.0`, plus unpinned `torch`/`torchaudio` (`requirements.txt:1-15`).
- `requirements-gpu.txt` (15 lines) plus `requirements-gpu-torch.txt` (4 lines) define the GPU variant: `torch==2.7.1+cu128` / `torchaudio==2.7.1+cu128` from the `cu128` index plus `faster-whisper==1.1.1` and `scipy==1.15.2` (`requirements-gpu-torch.txt:1-4`, `requirements-gpu.txt:1-15`).
- `install_with_gpu_support.bat` (2 lines) installs the GPU stack via `pip install -r requirements-gpu-torch.txt` then `pip install -r requirements-gpu.txt`, and `win_installgpu_virtual_env.bat` (14 lines) creates/activates `test_env` and chains into it (`install_with_gpu_support.bat:1-2`, `win_installgpu_virtual_env.bat:1-14`).
- `RELEASE_NOTES.md` (313 lines) records releases `1.0.3` through `1.1.2` with Added/Changed/Fixed sections and explicit release boundaries; the chunk excerpt is truncated after the `1.0.3` notes, so content past that point was cut instead of guessed (`RELEASE_NOTES.md:1-313`).
---
## Ignore rules
`.dockerignore` is the full 5-line file, verbatim:
```
__pycache__
.cache
.dockerignore
docker-compose.yml
Dockerfile
```
(`.dockerignore:1-5`)

`.gitignore` (221 lines) groups, verbatim excerpts:
```
examples/
batch/
test_env/
tests_private/
docs_private/
docs/development/
dev/
dev-log/
dev-logs/
roadmap/
```
(`.gitignore:18-29`)
```
# Local secrets and credentials
.env.*
!.env.example
*.pem
*.key
*.p12
*.pfx
```
(`.gitignore:61-67`)
```
# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
```
(`.gitignore:78-96`)
```
# Local diagnostic outputs
test_outputs/
audio-recorder-refactoring-map.md
audio-recorder-refactoring-plan.md
ARCHITECTURE.md
REFACTORING.md
```
(`.gitignore:212-217`)

## Packaging manifest
`MANIFEST.in` (19 lines), verbatim:
```
include requirements.txt
include README.md
include RELEASE_NOTES.md
include LICENSE
prune docs/development
prune dev-log
prune dev-logs
prune roadmap
prune test-model-cache
prune test-results
prune docs_private
prune docs/handoffs
prune tests_private
global-exclude *Kopie*.py
global-exclude *.bak
global-exclude *.tmp
global-exclude *.log
global-exclude *.jsonl
```
(`MANIFEST.in:1-19`)

## Dependency pins
| File | Key pins |
|---|---|
| `requirements.txt` (`requirements.txt:1-15`) | `PyAudio==0.2.14`, `faster-whisper==1.2.1`, `pvporcupine==1.9.5`, `webrtcvad-wheels==2.0.14`, `halo==0.0.31`, `colorama==0.4.6`, `torch` (unpinned), `torchaudio` (unpinned), `scipy==1.17.1`, `openwakeword>=0.6.0`, `websockets==16.0`, `websocket-client==1.9.0`, `soundfile==0.13.1`, `silero-vad[onnx-cpu]>=6.2.1; python_version >= "3.8"` |
| `requirements-gpu.txt` (`requirements-gpu.txt:1-15`) | `PyAudio==0.2.14`, `faster-whisper==1.1.1`, `pvporcupine==1.9.5`, `webrtcvad-wheels==2.0.14`, `halo==0.0.31`, `scipy==1.15.2`, `websockets==14.1`, `websocket-client==1.8.0`, `openwakeword>=0.4.0`, `numpy<2.0.0`, `soundfile==0.13.1`, `silero-vad[onnx-cpu]>=6.2.1; python_version >= "3.8"` (torch/torchaudio live in the companion file) |
| `requirements-gpu-torch.txt` (`requirements-gpu-torch.txt:1-4`) | `--index-url https://download.pytorch.org/whl/cu128`, `torch==2.7.1+cu128`, `torchaudio==2.7.1+cu128` |

GPU note, verbatim (`requirements-gpu.txt:12-13`):
```
# RealtimeSTT's default Silero VAD path is CPU ONNX Runtime even when ASR runs on GPU.
silero-vad[onnx-cpu]>=6.2.1; python_version >= "3.8"
```

## Windows GPU install scripts
`install_with_gpu_support.bat` (2 lines), verbatim (`install_with_gpu_support.bat:1-2`):
```
pip install -r requirements-gpu-torch.txt
pip install -r requirements-gpu.txt
```
`win_installgpu_virtual_env.bat` (14 lines), verbatim (`win_installgpu_virtual_env.bat:1-14`):
```
@echo off
cd /d %~dp0

REM Check if the venv directory exists
if not exist test_env\Scripts\python.exe (
    echo Creating VENV
    python -m venv test_env
) else (
    echo VENV already exists
)

echo Activating VENV
start cmd /k "call test_env\Scripts\activate.bat && install_with_gpu_support.bat"
```

## Release history
`RELEASE_NOTES.md` (313 lines) covers `1.1.2 - 2026-08-30`, `1.1.1 - 2026-08-28`, `1.1.0 - 2026-08-27`, `1.0.4 - 2026-08-21`, and `1.0.3 - 2026-08-20` (`RELEASE_NOTES.md:276-438`). Documented highlights in the visible excerpt:
- `1.1.2` advertises the exact `preview.earlyRms` contract (25 ms first-attempt decoder flush, one-attempt limit, no advisory empty-result retry) and keeps the conditional 500 ms empty-result retry for authoritative/missing/unknown/malformed preview modes (`RELEASE_NOTES.md:283-297`).
- `1.1.1` fixes stale Preview ASR work delaying newer full-turn snapshots, with cancellable shared-engine jobs and bounded/coalesced Preview admission (`RELEASE_NOTES.md:312-325`).
- `1.1.0` promotes the `1.1.0rc1` candidate with correlated Preview `resume`, opt-in authenticated late full-turn correction, and recorder Preview/tail support (`RELEASE_NOTES.md:340-348`).
- `1.0.4` replaces the production WebSocket recorder/VAD-derived final path with a turn-owned state machine and canonical PCM buffer, and removes bearer-token CLI flags in favor of `REALTIMESTT_SERVER_BEARER_TOKEN` (`RELEASE_NOTES.md:385-413`).
- Truncation note: the chunk states `... (truncated, 4302 more characters)` inside the `1.0.3` section, so the tail of `RELEASE_NOTES.md` (late `1.0.3` notes and anything after) was cut and is not covered here.

**Covers:** `.dockerignore`, `.gitignore`, `install_with_gpu_support.bat`, `MANIFEST.in`, `RELEASE_NOTES.md`, `requirements-gpu-torch.txt`, `requirements-gpu.txt`, `requirements.txt`, `win_installgpu_virtual_env.bat`
