> [[index|Wiki]] | [[summary|Summary]]
# NVIDIA-NeMo/Speech — Digest
## 1. [[wiki/01-overview|Overview]]
**In one sentence:** NVIDIA NeMo Speech is a PyTorch toolkit for researchers and developers to create, customize, and deploy ASR, TTS, and Speech-LLM models from existing code and pre-trained checkpoints.
## Key points
- NeMo Speech targets researchers and PyTorch developers working on ASR, TTS, and Speech LLMs, reusing existing code and pre-trained checkpoints to create, customize, and deploy models (README.md:52-54).
- The repo has pivoted to audio, speech, and multimodal LLMs; v2.7.3 was the final pre-split release with additional modalities and v3.0.0 is the current NeMo Speech release (README.md:21-25, README.md:42-43).
- Minimum stack is Python 3.12+, PyTorch 2.7+, and NVIDIA GPU + CUDA for training, while the actively tested baseline is Python 3.13 with PyTorch 2.11/CUDA 12.9 or PyTorch 2.12/CUDA 13.2 pinned in `uv.lock` (README.md:63-67).
- NeMo Speech installs on top of an existing Python/PyTorch/CUDA stack without replacing it via the pip fallback, whereas `uv sync` reproduces the tested stack from `uv.lock` (README.md:67, README.md:84, README.md:121-127).
- Three install paths are supported: `uv sync` from source (recommended), prebuilt/buildable Docker images, and PyPI pip fallback with `asr`/`tts` plus `cu12`/`cu13` extras (README.md:86-94, README.md:100-117, README.md:121-134).
- Checkpoints loading with `torch.load` may require `weights_only=False` via env var `TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD=1`, with a warning to use it only with trusted files due to arbitrary-code-execution risk (README.md:69-73).
- Current checkpoints/demos are published via the HuggingFace Nemotron-Speech collection and build.nvidia.com entries, including MagpieTTS, Parakeet, Canary, and Nemotron-Speech-Streaming/VoiceChat updates from 2025-2026 (README.md:16-17, README.md:27-48).
## 2. [[wiki/02-top-level-files|Top-Level Files]]
**In one sentence:** The repo root holds no model code itself but the guardrails around it — lint/format/test configs, ignore lists, agent guidance, a dependency-analysis helper, and legal/attribution files.
## Key points
- The component is 20 root-level files only: no `nemo/`, `examples/`, `scripts/`, `tests/`, or `docs/` sources, just repo-level config, guidance, and legal files (02-top-level-files.md:5).
- Coverage is scoped to speech work: `.coveragerc` enables `thread,multiprocessing` concurrency and omits `nemo/collections/{asr,speechlm,tts}` plus `nemo/core` and `nemo/collections/common` among others (.coveragerc:2, .coveragerc:13-24, .coveragerc:32-33), while `codecov.yml` disables project status and requires 80% patch coverage excluding the same speech/core paths (codecov.yml:3-12).
- Lint/format agree on `max-line-length = 119` across flake8, pylint, and the AGENTS.md/CLAUDE.md guidance (.flake8:2, .pylintrc:3, AGENTS.md:17).
- `AGENTS.md` and `CLAUDE.md` are identical 147-line agent guides declaring active collections `asr`, `tts`, `audio`, `speechlm2`, `common` (AGENTS.md:7, CLAUDE.md:7).
- `nemo_dependencies.py` (206 lines) builds a reverse dependency graph by AST-parsing `nemo.*` imports across `nemo/`, `scripts/`, `examples/`, `tests/` (nemo_dependencies.py:125-127, nemo_dependencies.py:134-141).
- Docs build on Read the Docs with Ubuntu 22.04 / Python 3.10, Sphinx config at `docs/source/conf.py`, and docs requirements from `requirements/requirements_docs.txt` (.readthedocs.yml:7-19).
- Two chunk files are truncated so their full contents are not covered here: `.secrets.baseline` (2083 lines) and `THIRD-PARTY-NOTICES` (321 lines) (02-top-level-files.md:460, 02-top-level-files.md:1463).
## The system in five moves
1. NeMo Speech positions itself as a PyTorch toolkit for researchers and developers to create, customize, and deploy ASR, TTS, and Speech-LLM models from existing code and pre-trained checkpoints.
2. The repo pivots to audio, speech, and multimodal LLMs, closing the pre-split line at v2.7.3 and shipping the current v3.0.0 release with its checkpoint slate of MagpieTTS, Parakeet, Canary, and Nemotron streaming/VoiceChat updates.
3. Users enter through a defined stack — minimum Python 3.12+ and PyTorch 2.7+ with NVIDIA GPU + CUDA for training, tested baseline Python 3.13 with PyTorch 2.11/CUDA 12.9 or 2.12/CUDA 13.2 — via `uv sync`, Docker, or the pip fallback that preserves the existing stack.
4. The repo root wraps that product in guardrails rather than model code: coverage scoped to speech collections with 80% patch targets, lint/format pinned at 119 columns, and identical agent guides declaring the active `asr`, `tts`, `audio`, `speechlm2`, `common` collections.
5. Supporting machinery keeps the tree navigable and shippable: a reverse dependency-graph helper over `nemo.*` imports, Read the Docs builds from `docs/source/conf.py`, and security/attribution files alongside the `torch.load` trusted-checkpoint warning.
