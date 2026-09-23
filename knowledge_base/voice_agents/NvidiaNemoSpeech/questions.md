---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: NVIDIA-NeMo/Speech

### Q1. What is NVIDIA NeMo Speech, who is it for, and what does it help them do?
> [!tip]- Answer
> NeMo Speech is a PyTorch toolkit for researchers and developers working on ASR, TTS, and Speech LLMs. It helps them efficiently create, customize, and deploy new models by reusing existing code and pre-trained checkpoints. The repo has pivoted to audio, speech, and multimodal LLMs, with v3.0.0 current and v2.7.3 the final pre-split release. See [[wiki/01-overview|Overview]].

### Q2. What are the three supported install paths for NeMo Speech, and how do the uv and pip approaches differ?
> [!tip]- Answer
> The three paths are `uv sync` from source (recommended), prebuilt or buildable Docker images, and the PyPI pip fallback with `asr`/`tts` plus `cu12`/`cu13` extras. `uv sync` reproduces the tested stack from `uv.lock` (Python 3.13, pinned PyTorch/CUDA), while the pip fallback installs on top of the user's existing Python/PyTorch/CUDA stack without replacing it. Docker offers the prebuilt `nvcr.io/nvidia/nemo-speech` image or a source build with `GPU_TARGET` selection. See [[wiki/01-overview|Overview]].

### Q3. What are the minimum versus tested stack requirements, and what is the `torch.load` checkpoint warning?
> [!tip]- Answer
> Minimum versions are Python 3.12+, PyTorch 2.7+, and NVIDIA GPU + CUDA (required for training). The tested baseline is Python 3.13 with PyTorch 2.11/CUDA 12.9 or PyTorch 2.12/CUDA 13.2 pinned in `uv.lock`. Checkpoints needing `weights_only=False` require setting `TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD=1`, used only with trusted files because of arbitrary-code-execution risk. See [[wiki/01-overview|Overview]].

### Q4. What does the repo root contain, and how is test coverage scoped?
> [!tip]- Answer
> The root holds only 20 repo-level files — lint/format/test configs, ignore lists, agent guidance, a dependency-analysis helper, and legal files — with no `nemo/`, `examples/`, `scripts/`, `tests/`, or `docs/` model code. `.coveragerc` enables `thread,multiprocessing` concurrency and omits speech and core paths such as `nemo/collections/{asr,speechlm,tts}`, `nemo/core`, and `nemo/collections/common`. `codecov.yml` disables project status and requires 80% patch coverage with matching path exclusions. See [[wiki/02-top-level-files|Top-Level Files]].

### Q5. What lint and format standards guard the repo, and how do the speech-specific configs differ?
> [!tip]- Answer
> Lint and format agree on `max-line-length = 119` across flake8, pylint, and the AGENTS.md/CLAUDE.md guidance, with black using `skip_string_normalization` and isort using the black profile. The base `.flake8` selects a small rule set (unused imports/variables, undefined names, ambiguous names), while `.flake8.speech` and `.flake8.other` add a `__init__.py: F401` ignore for intentional re-exports. The `.pylintrc.speech` config enables only the unused-import check (`W0611`). See [[wiki/02-top-level-files|Top-Level Files]].

### Q6. What do the agent guides and `nemo_dependencies.py` provide for contributors?
> [!tip]- Answer
> `AGENTS.md` and `CLAUDE.md` are identical 147-line guides declaring active collections `asr`, `tts`, `audio`, `speechlm2`, and `common`, plus dev install, test markers, CI, docs-build, and Hydra commands. They forbid pushing directly to `main`, modifying `.github/workflows/` unasked, and deleting test files unasked. The 206-line `nemo_dependencies.py` builds a reverse dependency graph by AST-parsing `nemo.*` imports across `nemo/`, `scripts/`, `examples/`, and `tests/`, printing it as indented JSON. See [[wiki/02-top-level-files|Top-Level Files]].

### Q7. Which install path would you recommend for a researcher who needs a reproducible baseline versus one who already has a tuned CUDA environment, and why?
> [!tip]- Answer
> Recommend `uv sync` from source for the reproducible baseline because it pins Python 3.13 and the tested PyTorch/CUDA builds from `uv.lock`, matching the official container and CI. Recommend the PyPI pip fallback for the tuned environment because it keeps the user's existing PyTorch/CUDA stack instead of replacing it. Choose Docker when a prebuilt isolated runtime matters more than either source control or stack preservation. See [[wiki/01-overview|Overview]].
