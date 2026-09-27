> [[index|Wiki]] | [[summary|Summary]]
# sgl-project/sglang-omni — Digest
## 1. [[wiki/01-overview|Overview]]
**In one sentence:** SGLang-Omni is a multi-stage serving runtime for omni, speech, and TTS models that owns pipeline topology, stage lifecycle, inter-stage transport, and an OpenAI-compatible serving surface while composing with SGLang for autoregressive execution.
## Key points
- SGLang-Omni is a multi-stage serving runtime for omni, speech, and TTS models whose design target is multi-stage decoding split across heterogeneous stages (README.md:47).
- It owns the pipeline topology, stage lifecycle, inter-stage transport, model-family integration layer, and OpenAI-compatible serving surface, while composing with SGLang for high-performance autoregressive scheduling and model execution where applicable (README.md:47).
- It models generation as coordinated stages: preprocessing, encoders, autoregressive engines, talkers, decoders, vocoders, and aggregators (README.md:49).
- Each stage runs behind a scheduler matched to its workload, from SGLang-backed autoregressive scheduling to lightweight preprocessing and streaming vocoder loops (README.md:50).
- A control plane coordinates requests while the relay data plane moves tensor payloads across shared-memory, NCCL, NIXL, and Mooncake backends (README.md:51).
- OpenAI-compatible endpoints expose multimodal chat, speech generation, batch speech, streaming speech, uploaded voices, and transcription (README.md:52).
- Hardware coverage is NVIDIA CUDA as the supported default backend with full model coverage, plus experimental Apple Silicon and Intel GPU (XPU) paths (README.md:66).
## 2. [[wiki/02-top-level-files|top-level-files]]
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
## The system in five moves
1. SGLang-Omni frames generation as multi-stage decoding split across heterogeneous stages with different compute and dependency patterns.
2. It owns pipeline topology, stage lifecycle, transport, and the serving surface while composing with SGLang for autoregressive execution.
3. Each stage runs behind a workload-matched scheduler, coordinated by a control plane with a relay data plane over shared-memory, NCCL, NIXL, and Mooncake.
4. OpenAI-compatible endpoints expose the runtime for omni chat, speech, music, transcription, and diarization behind a multi-worker router.
5. The repository top level supports this with build hygiene, lint gates, a macOS-only installer, and per-accelerator packaging for CUDA, CPU, NPU, ROCm, and XPU.
