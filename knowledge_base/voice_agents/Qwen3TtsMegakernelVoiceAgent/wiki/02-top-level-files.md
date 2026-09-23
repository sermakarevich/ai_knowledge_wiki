> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# top-level-files
**In one sentence:** The top-level files define what is excluded from version control and the pinned Python dependency stack for inference, serving, benchmarking, and the voice pipeline.
## Key points
- `.gitignore` excludes the `model/` weights directory, directing users to Git LFS or `setup.sh` download instead (`.gitignore:1-2`).
- `.gitignore` excludes the compiled megakernel cache `~/.cache/torch_extensions/` plus `__pycache__/`, `*.pyc`, and `*.pyo` (`.gitignore:4-8`).
- `.gitignore` excludes Python virtual environments `venv/`, `.venv/`, and `env/` (`.gitignore:10-13`).
- `.gitignore` excludes editor/OS artifacts `.DS_Store`, `.vscode/`, and `*.swp` (`.gitignore:15-18`).
- `.gitignore` excludes assessment/personal docs `*.pdf`, `e3-assessment.txt`, `Technical assessment mail.txt`, `takehome_project.docx`, and `takehome_project.txt` (`.gitignore:20-25`).
- `requirements.txt` pins the core inference stack `torch>=2.3.0` (CUDA-enabled), `transformers>=4.47.0`, `safetensors>=0.4.0`, and `numpy>=1.24.0` (`requirements.txt:1-5`).
- `requirements.txt` pins the model/download layer `qwen-tts>=0.1.1`, `huggingface_hub>=0.23.0`, and optional fast downloader `hf_transfer>=0.1.6`, plus the serving, benchmarking, and voice-pipeline layers `fastapi`/`uvicorn`/`pydantic`, `aiohttp`, `pipecat-ai[silero,local]`, `deepgram-sdk`, and `groq` (`requirements.txt:7-26`).
---
## .gitignore
Verbatim excerpt (26 lines):
```
# Model weights (large binary files – use Git LFS or download via setup.sh)
model/

# Compiled megakernel
~/.cache/torch_extensions/
__pycache__/
*.pyc
*.pyo

# Python venv
venv/
.venv/
env/

# Editor
.DS_Store
.vscode/
*.swp

# Assessment PDFs / personal docs (not needed in source repo)
*.pdf
e3-assessment.txt
Technical assessment mail.txt
takehome_project.docx
takehome_project.txt
```

| Group | Patterns (`.gitignore:1-25`) |
|---|---|
| Model weights | `model/` (`.gitignore:2`) |
| Compiled megakernel | `~/.cache/torch_extensions/`, `__pycache__/`, `*.pyc`, `*.pyo` (`.gitignore:5-8`) |
| Python venv | `venv/`, `.venv/`, `env/` (`.gitignore:11-13`) |
| Editor | `.DS_Store`, `.vscode/`, `*.swp` (`.gitignore:16-18`) |
| Assessment / personal docs | `*.pdf`, `e3-assessment.txt`, `Technical assessment mail.txt`, `takehome_project.docx`, `takehome_project.txt` (`.gitignore:21-25`) |

## requirements.txt
Verbatim excerpt (27 lines):
```
# Core inference
torch>=2.3.0          # must be CUDA-enabled (e.g. pip install torch --index-url https://download.pytorch.org/whl/cu121)
transformers>=4.47.0
safetensors>=0.4.0
numpy>=1.24.0

# Qwen3-TTS model + HuggingFace download
qwen-tts>=0.1.1
huggingface_hub>=0.23.0
hf_transfer>=0.1.6    # optional fast downloader

# TTS server
fastapi>=0.110.0
uvicorn[standard]>=0.29.0
pydantic>=2.0.0

# Benchmarking
aiohttp>=3.9.0

# Pipecat voice pipeline
pipecat-ai[silero,local]>=0.0.36
# pipecat-ai[deepgram,groq] — uncomment if those extras are available separately

# STT / LLM services (pipecat integrations)
deepgram-sdk>=3.0.0
groq>=0.5.0
```

| Layer | Exact spec (`requirements.txt:1-26`) |
|---|---|
| Core inference | `torch>=2.3.0`, `transformers>=4.47.0`, `safetensors>=0.4.0`, `numpy>=1.24.0` (`requirements.txt:2-5`) |
| Qwen3-TTS + HuggingFace download | `qwen-tts>=0.1.1`, `huggingface_hub>=0.23.0`, `hf_transfer>=0.1.6` (`requirements.txt:8-10`) |
| TTS server | `fastapi>=0.110.0`, `uvicorn[standard]>=0.29.0`, `pydantic>=2.0.0` (`requirements.txt:13-15`) |
| Benchmarking | `aiohttp>=3.9.0` (`requirements.txt:18`) |
| Pipecat voice pipeline | `pipecat-ai[silero,local]>=0.0.36`, commented alternative `# pipecat-ai[deepgram,groq]` (`requirements.txt:21-22`) |
| STT / LLM services | `deepgram-sdk>=3.0.0`, `groq>=0.5.0` (`requirements.txt:25-26`) |

No truncated files were noted in the chunk.
**Covers:** `.gitignore`, `requirements.txt`
