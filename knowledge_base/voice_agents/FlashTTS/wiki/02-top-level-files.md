> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-level-files
**In one sentence:** The repo's top-level footprint captured here is its Python/ML hygiene (.gitignore) and its pinned CUDA-12.1 inference-and-training dependency set (requirements.txt).
## Key points
- `.gitignore` excludes Python build and cache artifacts (`__pycache__/`, `*.py[cod]`, `build/`, `dist/`, `*.egg-info/`) so generated packaging output is never committed (`.gitignore:1`, `.gitignore:9`).
- `.gitignore` excludes virtual environments (`.venv/`, `venv/`, `ENV/`, `env/`) and IDE state (`.idea/`, `.vscode/`, `*.swp`, `*.swo`), keeping local dev setup out of version control (`.gitignore:23`, `.gitignore:29`).
- `.gitignore` excludes large binary weights and checkpoint dirs (`*.pt`, `*.pth`, `*.ckpt`, `ckpts/`, `checkpoints/`, `pretrained_models/`), so model files are fetched rather than stored in git (`.gitignore:35`).
- `.gitignore` excludes runtime outputs (`*.log`, `inference_output/`, `outputs/`), OS files (`.DS_Store`, `Thumbs.db`), notebook checkpoints, and local secrets (`.env`, `*.local`) (`.gitignore:43`, `.gitignore:48`, `.gitignore:53`).
- `requirements.txt` pulls PyTorch wheels from the CUDA 12.1 index and pins `torch==2.3.1` with `torchaudio==2.3.1` as the compute base (requirements.txt:1, requirements.txt:35).
- `requirements.txt` splits platform-conditional packages: `deepspeed`, `onnxruntime-gpu`, and `tensorrt-cu12*` install only on Linux, while plain `onnxruntime` installs on macOS/Windows (requirements.txt:4, requirements.txt:22, requirements.txt:32).
- `requirements.txt` pins the serving and training stack together: `fastapi`/`uvicorn`/`gradio`/`grpcio` for APIs and demos, plus `lightning`, `hydra-core`, `omegaconf`, `diffusers`, `transformers`, and `conformer` for model code (requirements.txt:6, requirements.txt:16, requirements.txt:3).
- `requirements.txt` pins the speech/audio toolchain (`librosa`, `soundfile`, `pyworld`, `openai-whisper`, `wetext`, `inflect`, `modelscope`, `gdown`, `wget`) used for audio I/O, vocoding features, text normalization, and weight fetching (requirements.txt:15, requirements.txt:24, requirements.txt:28).
---
## .gitignore
Python cache/build exclusions (verbatim):
```
__pycache__/
*.py[cod]
*$py.class
*.so
build/
dist/
*.egg-info/
```
Environment, IDE, and weight exclusions (verbatim names):
```
.venv/
venv/
ENV/
env/
.idea/
.vscode/
*.swp
*.swo
*.pt
*.pth
*.ckpt
ckpts/
checkpoints/
pretrained_models/
```
Log, output, OS, and secret exclusions (verbatim names):
```
*.log
inference_output/
outputs/
.DS_Store
Thumbs.db
.ipynb_checkpoints/
.env
*.local
```
## requirements.txt
Install sources (exact lines):
```
--extra-index-url https://download.pytorch.org/whl/cu121
--extra-index-url https://aiinfra.pkgs.visualstudio.com/PublicPackages/_packaging/onnxruntime-cuda-12/pypi/simple/
```
Platform-conditional pins (exact):
| Package | Marker |
|---|---|
| `deepspeed==0.15.1` | `sys_platform == 'linux'` |
| `onnxruntime-gpu==1.18.0` | `sys_platform == 'linux'` |
| `onnxruntime==1.18.0` | `sys_platform == 'darwin' or sys_platform == 'win32'` |
| `tensorrt-cu12==10.0.1`, `tensorrt-cu12-bindings==10.0.1`, `tensorrt-cu12-libs==10.0.1` | `sys_platform == 'linux'` |
Core compute pins (exact): `torch==2.3.1`, `torchaudio==2.3.1`, `onnx==1.16.0`, `protobuf==4.25`, `pyarrow==18.1.0`, `pydantic==2.7.0`, `networkx==3.1`, `rich==13.7.1`, `matplotlib==3.7.5`, `tensorboard==2.14.0`.
**Covers:** `.gitignore`, `requirements.txt`
