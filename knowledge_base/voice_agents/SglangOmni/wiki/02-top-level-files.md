[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# top-level-files
**In one sentence:** The repository top level defines build hygiene, lint/format gates, and per-accelerator packaging plus a macOS-only Apple Silicon installer, not model or serving logic.
## Key points
- `.dockerignore` excludes VCS, virtualenv, bytecode, and cache/result artifacts from the Docker build context (`.dockerignore:1-10`).
- `.editorconfig` enforces UTF-8, LF endings, space indentation with size 4 (size 2 for JSON/YAML/Markdown), trailing-whitespace trimming, and tab indentation for Makefiles (`.editorconfig:5-13`, `.editorconfig:15-16`, `.editorconfig:46-47`).
- `.gitignore` excludes bytecode, packaging outputs, virtualenvs (`venv/`, `.venv/`, `/omni`), IDE files, test/log/media artifacts (`*.wav`, `output.wav`), result/run directories, and Rust `target/` (`.gitignore:2-6`, `.gitignore:64-67`, `.gitignore:70-74`, `.gitignore:106-107`).
- `.isort.cfg` sets `profile=black`, `known_first_party=sglang-omni`, and `known_third_party=transformers` (`.isort.cfg:2-4`).
- `.pre-commit-config.yaml` wires autoflake, pre-commit-hooks, isort, ruff, black-jupyter, clang-format, nbstripout, plus local `sort-ci-permissions`, `rustfmt-sglang-omni-router`, and `leading-underscore-names` checks (`.pre-commit-config.yaml:8-14`, `.pre-commit-config.yaml:163-176`, `.pre-commit-config.yaml:195-216`).
- `AGENTS.md` and `CLAUDE.md` are identical 5-line pointers requiring readers to follow `.claude/skills/code-review/coding-style.md` before writing, modifying, or reviewing code (`AGENTS.md:1-5`, `CLAUDE.md:1-5`).
- `install.sh` is a macOS arm64-only Apple Silicon installer that creates a Python 3.12 venv, requires native `/opt/homebrew` Homebrew with `ffmpeg@7` and `uv`, pins SGLang to `v0.5.19` via `SGLANG_VERSION`, and installs `sglang-omni` plus the `sgl-omni` CLI (`install.sh:240-246`, `install.sh:249-252`, `install.sh:351-352`, `install.sh:428-429`, `install.sh:443-448`, `install.sh:559-561`).
- `pyproject_cpu.toml`, `pyproject_npu.toml`, `pyproject_rocm.toml`, and `pyproject_xpu.toml` are per-accelerator `sglang-omni` packaging variants that share the `sgl-omni` / `sgl-omni-router-py` console scripts and `sglang.serve_backends` `omni` entry point while pinning device-specific torch stacks (`pyproject_cpu.toml:605-610`, `pyproject_npu.toml:730-739`, `pyproject_rocm.toml:879-880`, `pyproject_xpu.toml:1021-1024`, `pyproject_cpu.toml:656-661`).
---
## Build context and ignores
Verbatim `.dockerignore` (`.dockerignore:1-10`):
```
.git/
.venv/
__pycache__/
*.py[cod]
.pytest_cache/
.ruff_cache/
.mypy_cache/
.cache/
results/
```

Verbatim `.isort.cfg` (`.isort.cfg:1-4`):
```
[settings]
profile=black
known_first_party=sglang-omni
known_third_party=transformers
```

`.gitignore` excerpts (`.gitignore:53-69`, `.gitignore:91-96`, `.gitignore:106-107`):
```
__pycache__/
*.py[cod]
*$py.class
dist/
build/
*.egg-info/
*.egg
venv/
.venv/
env/
/omni
.ruff_cache/
uv.lock
results/
target/
```

## Editor and lint gates
Verbatim `.editorconfig` core (`.editorconfig:5-16`):
```
[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 4
trim_trailing_whitespace = true
insert_final_newline = true

[*.{json,yaml,yml}]
indent_size = 2
```

`.pre-commit-config.yaml` hook inventory (`.pre-commit-config.yaml:8-14`, `.pre-commit-config.yaml:163-176`, `.pre-commit-config.yaml:181-189`, `.pre-commit-config.yaml:195-216`):

| Repo | Hooks |
|------|-------|
| `PyCQA/autoflake@v2.3.1` | `autoflake --remove-all-unused-imports --in-place` |
| `pre-commit/pre-commit-hooks@v5.0.0` | `check-symlinks`, `destroyed-symlinks`, `trailing-whitespace`, `end-of-file-fixer`, `check-yaml`, `check-toml`, `check-ast`, `check-added-large-files`, `check-merge-conflict`, `check-shebang-scripts-are-executable`, `detect-private-key`, `debug-statements`, `no-commit-to-branch` |
| `PyCQA/isort@5.13.2` | `isort` |
| `astral-sh/ruff-pre-commit@v0.11.10` | `ruff --select=F401 --fixable=F401` on `benchmarks/`, `docs/`, `examples/`; `ruff-check` |
| `psf/black@24.10.0` | `black-jupyter` |
| `pre-commit/mirrors-clang-format@v18.1.8` | `clang-format --style=file --verbose` for `c++`, `cuda` |
| `kynan/nbstripout@0.8.1` | `nbstripout --keep-output --extra-keys=metadata.kernelspec metadata.language_info.version` |
| `local` | `sort-ci-permissions` (`python3 .github/update_ci_permission.py --sort-only`), `rustfmt-sglang-omni-router` (`cd sglang_omni_router/rust && cargo fmt --all -- --check`), `leading-underscore-names` (`python3 scripts/check_leading_underscore.py --fix` on `^sglang_omni/`, excluding `^sglang_omni/vendor/`) |

## Agent pointers
Verbatim `AGENTS.md` and `CLAUDE.md` (`AGENTS.md:1-5`, `CLAUDE.md:1-5`):
```
# Coding style guidelines

Before writing, modifying, or reviewing code, read and follow
[.claude/skills/code-review/coding-style.md](.claude/skills/code-review/coding-style.md).
```

## install.sh (Apple Silicon installer)
`install.sh` declares it installs sglang-omni and the Apple Silicon Qwen3-ASR runtime, deliberately does not bootstrap Homebrew, runs `set -Eeuo pipefail`, and defaults `DEFAULT_OMNI_REPO` to `https://github.com/sgl-project/sglang-omni.git`, `DEFAULT_OMNI_REF` to `main`, `DEFAULT_SGLANG_REPO` to `https://github.com/sgl-project/sglang.git`, `DEFAULT_SGLANG_REF` to `v0.5.19` (`install.sh:240-252`).

Options (`install.sh:305-333`):

| Flag | Meaning |
|------|---------|
| `--non-interactive` | Disable Homebrew auto-update (CI use) |
| `-h, --help` | Show help |

Environment knobs (`install.sh:315-327`):

| Variable | Meaning |
|----------|---------|
| `SGLANG_OMNI_VENV` | Virtual environment path |
| `SGLANG_OMNI_CACHE` | Cache root for source checkouts |
| `SGLANG_SOURCE_DIR` | SGLang source checkout path |
| `SGLANG_VERSION` | SGLang git tag/branch (default: `v0.5.19`) |
| `SGLANG_REPO` | SGLang repository URL |
| `SGLANG_OMNI_REPO` / `SGLANG_OMNI_REF` / `SGLANG_OMNI_PROJECT_DIR` | sglang-omni repository URL, branch/tag, checkout path |
| `SGLANG_OMNI_EXTRAS` | Optional extras, comma-separated |
| `NONINTERACTIVE=1` | Same as `--non-interactive` |
| `UV_HTTP_TIMEOUT` / `UV_HTTP_RETRIES` | Per-request timeout in seconds (default: 300) / network retry count (default: 5) |

Hard requirements and behavior (`install.sh:351-352`, `install.sh:408-414`, `install.sh:428-448`, `install.sh:527-537`, `install.sh:558-561`):
- Dies unless `uname -s` is `Darwin` and `uname -m` is `arm64`.
- Requires native Apple Silicon Homebrew at prefix `/opt/homebrew`; errors instead of bootstrapping it.
- Ensures formulas `ffmpeg@7` and `uv` (plus `git` if missing).
- Creates/reuses a Python 3.12 venv (`uv venv --python 3.12`) and asserts `sys.version_info[:2] == (3, 12)`.
- Stages the SGLang checkout, swaps in `python/pyproject_other.toml` as `python/pyproject.toml`, and installs `$SGLANG_STAGE_DIR/python[all_mps]` with `SGLANG_BUILD_RUST_EXTS=none`.
- Installs the local or cloned `sglang-omni` project (editable, with `$EXTRAS`), then verifies with `uv pip check`, `import sglang_omni` version print, and `sgl-omni --help`.

Truncation note: the chunk marks `install.sh` as 345 lines but truncates the tail after the `DYLD_LIBRARY_PATH` line (621 more characters cut), so verification/cleanup lines past that point are not grounded here.

## Per-accelerator packaging
All four variants name the package `sglang-omni` with dynamic version from `sglang_omni.__version__`, `requires-python = ">=3.10,<3.13"`, Apache-2.0 license, and the same console scripts (`pyproject_cpu.toml:581-589`, `pyproject_cpu.toml:656-661`, `pyproject_cpu.toml:680-681`):
```
sgl-omni = "sglang_omni.cli:app"
sgl-omni-router-py = "sglang_omni_router.python.serve:main"
```
plus entry point `omni = "sglang_omni.cli.sglang_backend:create_backend"` under `[project.entry-points."sglang.serve_backends"]` (`pyproject_cpu.toml:663-664`, `pyproject_npu.toml:809-810`, `pyproject_rocm.toml:946-947`).

Torch/device scoping (exact pins from the chunk):

| Variant | Torch stack | Notes |
|---------|-------------|-------|
| `pyproject_cpu.toml` (`pyproject_cpu.toml:605-611`) | `torch==2.12.0`, `torchvision==0.27.0`, `torchaudio==2.11.0`, `torchcodec==0.12.0`, `transformers==5.12.1` | Intel CPU build; drops CUDA-only wheels; sglang verified against `v0.5.19` but unpinned because every published wheel pulls CUDA torch |
| `pyproject_npu.toml` (`pyproject_npu.toml:730-749`, `pyproject_npu.toml:764-765`) | torch / torch_npu / triton-ascend / memfabric intentionally unpinned, installed manually per CANN release; `transformers==5.12.1`, `silero-vad==6.2.1` | Ascend NPU build; NPU metadata in `[tool.sglang-omni.npu]` pins `sglang-version = "0.5.19"` plus `base-image-a3` / `base-image-910b` digests (`pyproject_npu.toml:823-826`) |
| `pyproject_rocm.toml` (`pyproject_rocm.toml:879-880`) | Torch, SGLang, AITER, Triton, FlashInfer, NIXL, ROCm runtime inherited from the SGLang base image; `transformers==5.12.1`, `torchcodec==0.11.1`, `cache-dit==1.3.0` | Adds `dots.tts==0.2.1`, `diffusers==0.37.0`, `gradio>=4.0.0`, `nemo_text_processing==1.2.0`; optional `audar-tts` extra (`llama-cpp-python==0.3.34`, `neucodec==0.0.6`) (`pyproject_rocm.toml:936-940`) |
| `pyproject_xpu.toml` (`pyproject_xpu.toml:1019-1028`) | `torch==2.13.0+xpu`, `torchvision==0.28.0+xpu`, `torchaudio==2.11.0+xpu`, `torchcodec==0.13.0`, `transformers==5.12.1` | Intel XPU build; adds `omegaconf` and `x-transformers` for AuK checkpoints/DiT rotary embeddings (`pyproject_xpu.toml:1053-1055`) |

Shared extras pattern: `eval` (SeedTTS speaker-sim / WER eval + tests: `s3prl>=0.4.18`, `jiwer`, `openai-whisper==20250625`, `pytest>=7.0.0`, `pytest-asyncio>=0.21.0`) with `all` aliasing `eval`; NPU additionally defines `fun-cosyvoice3` (`pyproject_cpu.toml:641-654`, `pyproject_npu.toml:776-803`, `pyproject_xpu.toml:1058-1071`).

**Covers:** `.dockerignore`, `.editorconfig`, `.gitignore`, `.isort.cfg`, `.pre-commit-config.yaml`, `AGENTS.md`, `CLAUDE.md`, `install.sh` (tail truncated in chunk), `pyproject_cpu.toml`, `pyproject_npu.toml`, `pyproject_rocm.toml`, `pyproject_xpu.toml`
