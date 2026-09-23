> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-level-files
**In one sentence:** The repository root defines only project hygiene, legal attribution, and the Python runtime — a standard Python `.gitignore`, a `NOTICE` file crediting five third-party projects, and a 14-package `requirements.txt`.
## Key points
- The chunk grounds this page in exactly 3 source files: `.gitignore` (217 lines), `NOTICE` (40 lines), and `requirements.txt` (18 lines) (`02-top-level-files.md:5`).
- `.gitignore` is the stock Python template excluding bytecode (`__pycache__/`, `*.py[codz]`), C extensions (`*.so`), and packaging outputs (`build/`, `dist/`, `*.egg-info/`, `wheels/`) (`.gitignore:1-35`).
- `.gitignore` excludes environments and secrets including `.env`, `.envrc`, `.venv`, `venv/`, plus `.streamlit/secrets.toml` and `.abstra/` credentials (`.gitignore:158-166`, `.gitignore:199-201`, `.gitignore:223-224`).
- `.gitignore` excludes test/coverage, lint/typecheck, and IDE artefacts such as `.coverage`, `htmlcov/`, `.pytest_cache/`, `.ruff_cache/`, `.mypy_cache/`, and `.pytype/` (`.gitignore:47-60`, `.gitignore:178-187`, `.gitignore:212-213`).
- `NOTICE` copyrights the project as "RAON / Copyright 2026 The RAON Authors" and attributes five third-party codebases, all but PyTorch under Apache-2.0 (`NOTICE:1-8`).
- `NOTICE` explicitly names HuggingFace Transformers (2018–), Qwen3/Qwen3OmniMoe (Alibaba Cloud 2026), Mimi Audio Codec (Kyutai 2024), SpeechBrain ECAPA-TDNN speaker encoder (2021), and PyTorch (BSD 3-Clause, Facebook 2016–) (`NOTICE:9-40`).
- `requirements.txt` installs with `pip install -r requirements.txt` and pins only five packages (`accelerate>=1.10.1`, `pydantic>=2.11.10`, `soundfile>=0.13.1`, `transformers>=4.57.1,<5.0`, `datasets>=3.0.0`), leaving `torch`, `torchaudio`, `speechbrain`, and six others unpinned (`requirements.txt:1-17`).
---
## .gitignore
Standard GitHub Python template (217 lines). Verbatim excerpts:
```
__pycache__/
*.py[codz]
*$py.class
*.so
```
```
build/
dist/
*.egg-info/
.installed.cfg
*.egg
```
Environment/secret exclusions use exact names `[".env", ".envrc", ".venv", "env/", "venv/", "ENV/", "env.bak/", "venv.bak/"]` (`.gitignore:158-166`) plus `.streamlit/secrets.toml` (`.gitignore:223-224`) and `.abstra/` (`.gitignore:199-201`). No repo-specific model, data, or checkpoint patterns appear in the file.
## NOTICE
Full verbatim body (40 lines):
```
RAON
Copyright 2026 The RAON Authors

This product includes software developed by third parties.
```
followed by five attribution blocks with exact names and licenses:
| Block | Copyright holder | License | Upstream |
|---|---|---|---|
| HuggingFace Transformers | The Hugging Face team, 2018– | Apache-2.0 | https://github.com/huggingface/transformers |
| Qwen3 Models (Qwen3, Qwen3OmniMoe) | Alibaba Cloud, 2026 | Apache-2.0 | https://github.com/QwenLM/Qwen3 |
| Mimi Audio Codec | Kyutai Labs, 2024 | Apache-2.0 | https://huggingface.co/kyutai/mimi |
| SpeechBrain (ECAPA-TDNN Speaker Encoder) | SpeechBrain Authors, 2021 | Apache-2.0 | https://github.com/speechbrain/speechbrain |
| PyTorch | Facebook, Inc. (Adam Paszke), 2016– | BSD 3-Clause | https://github.com/pytorch/pytorch |
## requirements.txt
Verbatim header:
```
# RAON - Environment Requirements
# Install with: pip install -r requirements.txt
```
Full dependency table (exact specifiers as written):
| Package | Specifier |
|---|---|
| accelerate | >=1.10.1 |
| einops | (unpinned) |
| kernels | (unpinned) |
| numpy | (unpinned) |
| pydantic | >=2.11.10 |
| requests | (unpinned) |
| soundfile | >=0.13.1 |
| speechbrain | (unpinned) |
| tensorboard | (unpinned) |
| torch | (unpinned) |
| torchaudio | (unpinned) |
| tqdm | (unpinned) |
| transformers | >=4.57.1,<5.0 |
| datasets | >=3.0.0 |
**Covers:** `.gitignore`, `NOTICE`, `requirements.txt`
