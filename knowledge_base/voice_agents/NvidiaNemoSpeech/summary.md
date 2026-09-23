# Technical Analysis: NVIDIA-NeMo/Speech

**Repository:** https://github.com/NVIDIA-NeMo/Speech
**Version analyzed:** v3.0.0 (NGC container 26.07.00; last pre-split release v2.7.3)
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Speech-model work (ASR, TTS, Speech LLMs) requires reproducible training stacks, pre-trained checkpoints, and deployment paths across GPU/CUDA variants. Without a shared toolkit, researchers reimplement data loading, training loops, and inference harnesses per model, and drift between CUDA/PyTorch builds breaks reproducibility.

NeMo Speech addresses this as a PyTorch toolkit for creating, customizing, and deploying ASR, TTS, and Speech-LLM models by reusing existing code and pre-trained checkpoints (README.md:52-54). It fixes the tested stack (Python 3.13, PyTorch 2.11/CUDA 12.9 or PyTorch 2.12/CUDA 13.2, per README.md:67) behind `uv sync` + `uv.lock`, a prebuilt Docker image, and a pip fallback that preserves the user's own PyTorch build (README.md:67, README.md:84, README.md:121-127). Checkpoints and demos are distributed via the HuggingFace Nemotron-Speech collection and build.nvidia.com entries such as MagpieTTS, Parakeet, Canary, and Nemotron-Speech-Streaming/VoiceChat (README.md:16-17, README.md:27-48). The repo pivoted to audio, speech, and multimodal LLMs; other modalities remain at v2.7.3 (README.md:42-43). Primary user: researchers and PyTorch developers working on speech models (README.md:52-54).

## 2. High-Level Architecture

```
  ┌─ Source: git clone Speech ──────────────────────┐
  │  uv.lock + pyproject (pinned stack)              │
  │  docker/Dockerfile (GPU_TARGET=h100plus / a100)  │
  └──────────────────────┬──────────────────────────┘
                         ▼
  ┌─ Environment ───────────────────────────────────┐
  │  .venv/ via `uv sync` │ container 26.07.00       │
  │  or user PyTorch + pip fallback                  │
  └──────────────────────┬──────────────────────────┘
                         ▼
  ┌─ Model code (out of wiki scope) ────────────────┐
  │  nemo/collections: asr │ tts │ audio │ speechlm2 │
  │  nemo/{core,utils,export,deploy,lightning,automodel} │
  └──────────────────────┬──────────────────────────┘
                         ▼
  ┌─ Checkpoints / Demos ───────────────────────────┐
  │  HF Nemotron-Speech collection │ build.nvidia.com│
  │  *.nemo / *.ckpt / *.pt artifacts                │
  └─────────────────────────────────────────────────┘
  Guardrails ─► lint/format/test configs, coverage gates,
  agent guides, dependency-graph helper, legal notices
```

Data-flow narrative (environment-to-artifact, the only flow the wiki covers):

1. Acquire source and select install path: `uv sync` from source (recommended), prebuilt/buildable Docker, or PyPI pip fallback with `asr`/`tts` plus `cu12`/`cu13` extras (README.md:86-94, README.md:100-117, README.md:121-134).
2. Resolve the compute stack: minimum Python 3.12+ and PyTorch 2.7+, NVIDIA GPU + CUDA required for training (README.md:63-65); the tested baseline is Python 3.13 with PyTorch 2.11/CUDA 12.9 or PyTorch 2.12/CUDA 13.2 pinned in `uv.lock` (README.md:67).
3. Train/customize/infer against reusable code and pre-trained checkpoints (README.md:52-54), with Hydra-configured runs (e.g. `@hydra_runner(config_path="conf", ...)`) per agent guidance (AGENTS.md:110-121).
4. Obtain or emit checkpoints: published checkpoints arrive via HuggingFace/build.nvidia.com (README.md:16-17, README.md:27-48); local outputs (`*.nemo`, `*.ckpt`, `*.model`, `*.pkl`, `*.pt`, `output`, `runs`, `wandb`) are git/docker-ignored build artifacts (.dockerignore:1-20, .gitignore:1-11).
5. Guard output quality with repo-level gates: coverage omits speech/core paths but enforces 80% patch coverage elsewhere (.coveragerc:13-24, codecov.yml:3-12); lint/format pinned at line length 119 (.flake8:2, .pylintrc:3, AGENTS.md:17).
6. Ship or attribute: Docker image or `.venv` reproduces the stack; third-party adaptations are inventoried in `THIRD-PARTY-NOTICES` and contributions follow `CONTRIBUTING.md` under Apache-2.0 (THIRD-PARTY-NOTICES:12-30, README.md:136-143).

Persistent state lives outside the repo: model checkpoints (`*.nemo`, `*.ckpt`, `*.pt`), training outputs (`output`, `runs`, `wandb`, `nemo_experiments`), and datasets are explicitly ignored, not versioned (.dockerignore:1-20, .gitignore:1-11, .gitignore:286-320). Versioned state is the stack pin (`uv.lock`), container tag (`26.07.00`), and published checkpoint identities on HuggingFace/build.nvidia.com.

## 3. The Speech Collection and Checkpoint

The repo's central concept is the *collection*: a modality-scoped model family sharing code and checkpoints. Active collections are `asr`, `tts`, `audio`, `speechlm2`, `common` (AGENTS.md:7). Coverage configuration treats `nemo/collections/{asr,speechlm,tts}` plus `nemo/core` and `nemo/collections/common` as the in-scope core, omitting them from coverage measurement (.coveragerc:13-24, .coveragerc:32-33); the patch-status exclusions mirror this with `!nemo/collections/asr`, `!nemo/collections/audio`, `!nemo/collections/speechlm`, `!nemo/collections/tts`, `!nemo/core`, `!nemo/collections/common` (codecov.yml:8-12). The dependency helper generalizes the supporting namespaces as `nemo.collections.<x>` and `nemo.{core,utils,export,deploy,lightning,automodel}` (nemo_dependencies.py:24-50).

Named kinds visible in the wiki:

- `asr` — automatic speech recognition, incl. streaming/offline variants (Parakeet-unified-en-0.6b, Nemotron-3.5-ASR-Streaming-0.6B) (README.md:27-48).
- `tts` — text-to-speech (MagpieTTS v2512/v2602/v2607) (README.md:27-48).
- `speechlm` / `speechlm2` — speech LLMs, incl. voice-chat and streaming checkpoints (Nemotron-Speech-Streaming, VoiceChat Early Access on Nemotron Nano v2) (README.md:27-48, AGENTS.md:7).
- `audio` — audio support collection named in agent scope and coverage exclusions (AGENTS.md:7, codecov.yml:8-12).
- `common` / `core` — shared collection utilities and framework core, excluded from coverage alongside the above (.coveragerc:13-24).
- Checkpoint identities — Canary-Qwen-2.5B, Canary V2, Parakeet V3 (README.md:27-48).

Key query: the helper maps which package depends on which `nemo.*` namespace by AST-parsing imports, grouping `nemo.collections.*` under a `nemo.collections` key (nemo_dependencies.py:95-168). Verbatim scope declaration (AGENTS.md:7):

```
NeMo Speech — toolkit for training/deploying speech models (ASR, TTS, Speech LLM). Active collections: `asr`, `tts`, `audio`, `speechlm2`, `common`.
```

Representation: models are PyTorch modules trained on GPU/CUDA and serialized as `*.nemo` / `*.ckpt` / `*.pt` artifacts; the wiki covers only their distribution (HuggingFace collection, NGC container `26.07.00`) and their exclusion from version control, not tensor or config schemas.

## 4. LLM / External Service Integration

The repo ships and trains speech-LLM checkpoints locally; it calls no external LLM/API at runtime per the wiki. No API providers, keys, or remote inference endpoints appear in either component page. The LLM-adjacent facts are all local artifacts:

- Speech-LLM checkpoints: Nemotron-Speech-Streaming lineage, VoiceChat Early Access on a Nemotron Nano v2 LLM backbone, Canary-Qwen-2.5B (5.63% WER on English Open ASR Leaderboard) (README.md:27-48).
- Optional accelerated local backends for SpeechLM2/Automodel runs: Transformer Engine, FlashAttention, Mamba, grouped-GEMM/MoE, DeepEP, selected via `compiled` (Hopper/Blackwell) or `compiled-a100` (A100) extras built by `docker/Dockerfile` with `GPU_TARGET=h100plus` / `a100` (README.md:96).
- Documentation endpoints are reads, not service calls: versioned docs at `docs.nvidia.com/nemo/speech/3.0.0/` and `/nightly/` (README.md:77-80); checkpoint distribution via HuggingFace collection and build.nvidia.com (README.md:16-17).

Environment variable with external-behavior implications:

| Variable | Required? | Effect |
| --- | --- | --- |
| `TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD=1` | Optional, only when a checkpoint requires `weights_only=False` | Relaxes `torch.load` weights-only restriction; use only with trusted files due to arbitrary-code-execution risk (README.md:69-73) |

## 5. The Reproduce-Environment-to-Checkpoint Pipeline

Primary workflow in wiki scope: reproduce the tested stack, then train/customize/deploy from reusable code and checkpoints. Every function below is from `nemo_dependencies.py`, the only implementation file the wiki describes line-by-line; training-loop functions are not covered by any component page.

1. Enumerate candidate files — `find_python_files(directory: str) -> List[str]` scans `relevant_dirs = ['nemo', 'scripts', 'examples', 'tests']` for `*.py` (nemo_dependencies.py:7-21).
2. Extract intra-repo imports — `analyze_imports(file_path: str) -> Set[str]` parses `ast.ImportFrom` nodes starting with `nemo.`, mapping `nemo.collections.<x>` and `nemo.{core,utils,export,deploy,lightning,automodel}` (nemo_dependencies.py:24-50).
3. Enumerate packages — `find_top_level_packages(nemo_root: str)` lists `nemo/` directories and `find_collection_modules(nemo_root: str)` lists per-collection modules (nemo_dependencies.py:53-92).
4. Build the reverse graph — `build_dependency_graph(nemo_root: str)` makes two passes (collect packages, then record each file's package as a reverse dependency of every `nemo.*` package it imports), grouping `nemo.collections.*` under `nemo.collections` (nemo_dependencies.py:95-168).
5. Emit — `main()` sets `nemo_root = os.path.dirname(os.path.abspath(__file__))` and prints the graph as indented JSON (nemo_dependencies.py:171-184).
6. Run model work (generic, per guidance) — Hydra pattern `@hydra_runner(config_path="conf", config_name="fast-conformer_transducer_bpe")` with CLI overrides such as `model.optim.lr=1e-4 trainer.max_epochs=50` (AGENTS.md:110-121); test selection via markers `unit`, `integration`, `system`, `pleasefixme`, `skipduringci` (AGENTS.md:48).

## 6. Key Files

| File | Lines | What It Does |
| --- | --- | --- |
| `README.md` | cited to :143 | Project definition, release/checkpoint log, requirements, install paths, docs links, license |
| `nemo_dependencies.py` | 206 | AST-based reverse dependency-graph helper over `nemo.*` imports; prints indented JSON |
| `AGENTS.md` / `CLAUDE.md` | 147 each, identical | Agent working guide: scope, line length, install, markers, CI, docs build, Hydra pattern, prohibitions |
| `pyproject.toml` + `uv.lock` | — (sizes not in wiki) | Dependency manifest and tested-stack pin (Python 3.13, PyTorch 2.11/cu12.9 or 2.12/cu13.2) |
| `docker/Dockerfile` | — | Container build; `BASE_IMAGE`, `GPU_TARGET=h100plus`/`a100`; compiled-backend extras |
| `requirements/requirements_docs.txt` | — | Docs-build requirements referenced by Read the Docs config |
| `docs/source/conf.py` | — | Sphinx configuration for the docs build |
| `.coveragerc` | 41 | Coverage concurrency (`thread,multiprocessing`) and speech/core omit list |
| `codecov.yml` | 24 | Disables project status; 80% patch target with speech/core path exclusions |
| `.flake8` / `.flake8.other` / `.flake8.speech` | 13 each (variants) | Flake8 select lists, `max-line-length = 119`; variants add `__init__.py: F401` ignore |
| `.pylintrc` / `.pylintrc.other` / `.pylintrc.speech` | 6 / 14 / 10 | Pylint scoping: full pass vs docstring/import checks vs unused-import only |
| `.pre-commit-config.yaml` | 46 | Hooks: pre-commit-hooks, isort 5.13.2, black 24.10.0; quarterly autoupdate |
| `.readthedocs.yml` | 37 | Docs build: Ubuntu 22.04, Python 3.10, Sphinx conf, docs requirements |
| `.gitignore` | 198 | Ignores checkpoints, outputs, test/example data, voice-agent artifacts |
| `.dockerignore` | 20 | Excludes caches, logs, `.git`, `*.nemo`, `*.ckpt` from image context |
| `CITATION.cff` | 42 | Citation metadata (`cff-version: 1.2.0`) for the toolkit |
| `SECURITY.md` | 26 | Vulnerability reporting route (web form, `psirt@nvidia.com`) and required fields |
| `THIRD-PARTY-NOTICES` | 321 (truncated in chunk) | Per-component third-party attributions (licenses, sources) |
| `.secrets.baseline` | 2083 (truncated in chunk) | Secret-detector configuration and hashed-findings map |

Sizes and roles per 02-top-level-files.md; line counts for manifest/Dockerfile/docs sources are not stated in the wiki and are marked —.

## 7. Dependencies

The wiki gives exact constraint strings only for the language/runtime floor and extras selectors; library pins live in `uv.lock` without per-package versions quoted.

| Package | Version constraint | Purpose |
| --- | --- | --- |
| Python | `3.12 or above` (min); `3.13` (tested baseline) | Runtime (README.md:63-67) |
| PyTorch | `2.7 or above` (min); `2.11 with CUDA 12.9` or `2.12 with CUDA 13.2` (tested) | Training/inference framework (README.md:63-67) |
| NVIDIA GPU + CUDA | required for training; recommended for inference | Compute (README.md:63-65) |
| `nemo-toolkit[asr,tts]` | feature extras `asr`, `tts` | PyPI fallback install selector (README.md:121-134) |
| `nemo-toolkit[asr,tts,cu13]` / `[...,cu12]` | `cu13` (CUDA 13.x) / `cu12` (CUDA 12.x), mutually exclusive on Linux | CUDA wheel variant + `--extra-index-url .../cu132` / `.../cu129` (README.md:129-134) |
| `uv sync --extra all --extra cu13` (or `cu12`) | exactly one of `cu12`/`cu13`, default `cu13` | Full from-source extras set; reproduces container/CI baseline with `--locked --python 3.13` (README.md:94) |
| `--group test` / `--group docs` | optional groups | Test and docs tooling (README.md:94, AGENTS.md:13) |
| `compiled` / `compiled-a100` extras | GPU-gated | Accelerated backends (Transformer Engine, FlashAttention, Mamba, grouped-GEMM/MoE, DeepEP); `compiled` = Hopper/Blackwell, `compiled-a100` = A100 (README.md:96) |
| isort | `5.13.2` (pre-commit) | Import sorting, `profile = black`, excludes `docs/` (.pre-commit-config.yaml:23-37, AGENTS.md:19) |
| black | `24.10.0` via mypyc mirror; `skip_string_normalization = true` | Formatting at line length 119 (.pre-commit-config.yaml:23-37, AGENTS.md:17-18) |

## 8. CLI / Usage Surface

Entry points (all local; no service endpoints in wiki scope):

| Command | Purpose |
| --- | --- |
| `git clone https://github.com/NVIDIA-NeMo/Speech.git && cd Speech` | Acquire source (README.md:88-94) |
| `uv sync --extra all --extra cu13` (or `--extra cu12`) | Recommended from-source install into `.venv/` editable; add `--group test` / `--group docs`; run via `uv run <cmd>` or `source .venv/bin/activate` (README.md:88-94) |
| `uv sync --locked --python 3.13 --extra all --extra cu13 --group test` | Dev install reproducing container/CI baseline (AGENTS.md:13) |
| `uv pip install 'nemo-toolkit[asr,tts]'` / `pip install 'nemo-toolkit[asr,tts]'` | PyPI fallback preserving the user's own PyTorch ≥ 2.7; never `uv sync --locked` here (README.md:121-127) |
| `pip install 'nemo-toolkit[asr,tts,cu13]' --extra-index-url https://download.pytorch.org/whl/cu132` | Pinned-CUDA variant (cu12/cu129 analogously) (README.md:129-134) |
| `docker pull nvcr.io/nvidia/nemo-speech:26.07.00` + `docker run --rm -it --gpus all -v "$PWD:/workspace" ... bash` | Prebuilt container shell (README.md:100-106) |
| `docker buildx build -f docker/Dockerfile -t nemo-speech .` + `docker run ...` | Build from source (CUDA 13/H100+ default; `GPU_TARGET=a100` for A100) (README.md:110-117) |
| `uv run make -C docs clean html` → `docs/build/html/index.html` | Docs build (AGENTS.md:98-102) |
| `python nemo_dependencies.py` (graph printer) | Print reverse `nemo.*` dependency graph as indented JSON (nemo_dependencies.py:171-184) |

Env vars:

| Variable | Effect |
| --- | --- |
| `TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD=1` | Allow `torch.load` with `weights_only=False`; trusted files only (README.md:69-73) |

Test/config surface:

| Item | Values |
| --- | --- |
| Pytest markers | `unit`, `integration`, `system`, `pleasefixme` (broken — skip), `skipduringci` (AGENTS.md:48) |
| Hydra overrides | e.g. `model.optim.lr=1e-4 trainer.max_epochs=50` with `@hydra_runner(config_path="conf", config_name="fast-conformer_transducer_bpe")` (AGENTS.md:110-121) |
| Line length | `119` across black/isort/flake8/pylint (AGENTS.md:17, .flake8:2, .pylintrc:3) |
| CI | GitHub Actions in `.github/workflows/` — do not modify without explicit instruction (AGENTS.md:57, AGENTS.md:142-146) |

## 9. Extensibility Points

- New speech model / collection module — add under the corresponding `nemo/collections/<asr|tts|audio|speechlm2|common>/` tree and verify placement with `find_collection_modules` / `build_dependency_graph` in `nemo_dependencies.py` (nemo_dependencies.py:53-168).
- Shared framework capability — extend `nemo/{core,utils,export,deploy,lightning,automodel}`; the import mapper in `analyze_imports` already recognizes these namespaces (nemo_dependencies.py:24-50).
- New scripts/examples/tests — place under `scripts/`, `examples/`, `tests/`; they are included in `find_python_files` traversal and the dependency graph (nemo_dependencies.py:7-21).
- Training configuration — add Hydra configs under `conf/` and launch via `@hydra_runner(config_path="conf", config_name="<name>")` with CLI overrides (AGENTS.md:110-121).
- Accelerated backend — build the image with the matching extra: `compiled` (`GPU_TARGET=h100plus`, Hopper/Blackwell) or `compiled-a100` (A100) in `docker/Dockerfile` (README.md:96, README.md:117).
- Install surfacing for a new feature/CUDA variant — add a `pyproject.toml` extra consumed via `uv sync --extra <name>` or `nemo-toolkit[<name>]`, respecting the `cu12`/`cu13` mutual exclusion on Linux (README.md:94, README.md:121-134).

## 10. Limitations and Gotchas

- **`weights_only=False` is an arbitrary-code-execution risk.** `TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD=1` exists only for checkpoints that require it; set it solely for trusted files (README.md:69-73). Loading an untrusted checkpoint this way can execute code.
- **`uv sync --locked` destroys a pip-fallback stack.** The PyPI path requires installing your own PyTorch ≥ 2.7 first and using `uv pip`/`pip`; running `uv sync --locked` there replaces the stack instead of layering on it (README.md:121-127).
- **`cu12`/`cu13` are mutually exclusive on Linux.** Exactly one CUDA extra may be selected (default `cu13`); requesting both or omitting the wheel index (`--extra-index-url .../cu132` or `.../cu129`) breaks the pinned install (README.md:94, README.md:129-134).
- **Coverage numbers exclude the speech core.** `.coveragerc` omits `nemo/collections/{asr,speechlm,tts}`, `nemo/core`, and `nemo/collections/common` (plus mirrored `codecov.yml` exclusions), so headline coverage says nothing about model code; only the 80% patch gate on the remainder applies (.coveragerc:13-24, codecov.yml:3-12).
- **GPU is effectively mandatory for training.** CPU PyTorch satisfies the minimum install, but training requires NVIDIA GPU + CUDA (README.md:63-65); SpeechLM2/Automodel accelerated backends further require Hopper/Blackwell (`compiled`) or A100 (`compiled-a100`) images (README.md:96).
- **Speech-only scope; history ends at v2.7.3 for other modalities.** The repo covers audio/speech/multimodal LLMs; non-speech work stays on pre-split v2.7.3 (README.md:42-43). Confusing the two leads to missing collections.
- **Hard agent-workflow prohibitions.** Never push directly to `main`, never modify `.github/workflows/` without explicit instruction, never delete test files without explicit instruction (AGENTS.md:142-146). `pleasefixme`-marked tests are broken and must be skipped (AGENTS.md:48).

## 11. How It Compares to Alternatives

- **ESPnet (espnet/espnet)** — end-to-end speech-processing toolkit covering ASR/TTS/ST with Kaldi-style recipes; NeMo Speech instead pins a PyTorch/CUDA stack with NGC containers and centers distribution on HuggingFace Nemotron checkpoints.
- **SpeechBrain (speechbrain/speechbrain)** — PyTorch speech toolkit emphasizing readable recipes and HuggingFace Hub integration; NeMo Speech differentiates on NVIDIA-accelerated backends (Transformer Engine, FlashAttention, grouped-GEMM/MoE) and GPU-targeted container builds.
- **HuggingFace Transformers (audio/speech models)** — general-purpose model hub with broad speech-model coverage and `pip`-first install; NeMo Speech is narrower (ASR/TTS/Speech-LLM training and customization) with a locked `uv.lock`/container baseline rather than hub-version flexibility.
- **Coqui TTS / fairseq (legacy speech baselines)** — single-family or legacy training codebases; several of their techniques survive inside NeMo only as attributed adaptations (e.g. fairseq wav2vec/Adafactor MIT, HiFi-GAN MIT per THIRD-PARTY-NOTICES:12-30), while NeMo Speech is the actively released (v3.0.0) training-to-deployment surface.

Positioning: NeMo Speech is the NVIDIA-pinned, container-reproducible training/customization surface for ASR, TTS, and speech-LLMs — choose it when the tested CUDA/PyTorch stack and Nemotron-family checkpoints matter more than recipe breadth or hub generality.

## Appendix: Selected Code Snippets

1. From-source install (README.md:88-94):

```bash
git clone https://github.com/NVIDIA-NeMo/Speech.git
cd Speech
uv sync --extra all --extra cu13     # CUDA 13.x (recommended) — use --extra cu12 for CUDA 12.x
```

2. Coverage concurrency head (.coveragerc:1-3) and speech/core omits (.coveragerc:13-24, .coveragerc:32-33):

```ini
[run]
concurrency = thread,multiprocessing
omit =
```

```ini
    nemo/collections/asr/*
    nemo/collections/speechlm/*
    nemo/collections/tts/*
    nemo/core/*
    nemo/collections/common/*
```

3. Patch-coverage gate (codecov.yml:1-12):

```yaml
comment: false
coverage:
  status:
    project: false
    patch:
      default:
        target: 80%
```

4. Flake8 select list shared across configs (.flake8:2-9):

```ini
[flake8]
max-line-length = 119
select =
    F541, # f-string without any placeholders
    F841, # local variable 'x' is assigned to but never used
    F401, # 'x' imported but unused
    E741, # ambiguous variable name 'l'
    F821, # undefined name 'x'
    E266, # too many leading '#' for block comment
```
