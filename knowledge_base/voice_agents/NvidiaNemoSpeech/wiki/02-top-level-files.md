> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-Level Files
**In one sentence:** The repo root holds no model code itself but the guardrails around it — lint/format/test configs, ignore lists, agent guidance, a dependency-analysis helper, and legal/attribution files.
## Key points
- The component is 20 root-level files only: no `nemo/`, `examples/`, `scripts/`, `tests/`, or `docs/` sources, just repo-level config, guidance, and legal files (02-top-level-files.md:5).
- Coverage is scoped to speech work: `.coveragerc` enables `thread,multiprocessing` concurrency and omits `nemo/collections/{asr,speechlm,tts}` plus `nemo/core` and `nemo/collections/common` among others (.coveragerc:2, .coveragerc:13-24, .coveragerc:32-33), while `codecov.yml` disables project status and requires 80% patch coverage excluding the same speech/core paths (codecov.yml:3-12).
- Lint/format agree on `max-line-length = 119` across flake8, pylint, and the AGENTS.md/CLAUDE.md guidance (.flake8:2, .pylintrc:3, AGENTS.md:17).
- `AGENTS.md` and `CLAUDE.md` are identical 147-line agent guides declaring active collections `asr`, `tts`, `audio`, `speechlm2`, `common` (AGENTS.md:7, CLAUDE.md:7).
- `nemo_dependencies.py` (206 lines) builds a reverse dependency graph by AST-parsing `nemo.*` imports across `nemo/`, `scripts/`, `examples/`, `tests/` (nemo_dependencies.py:125-127, nemo_dependencies.py:134-141).
- Docs build on Read the Docs with Ubuntu 22.04 / Python 3.10, Sphinx config at `docs/source/conf.py`, and docs requirements from `requirements/requirements_docs.txt` (.readthedocs.yml:7-19).
- Two chunk files are truncated so their full contents are not covered here: `.secrets.baseline` (2083 lines) and `THIRD-PARTY-NOTICES` (321 lines) (02-top-level-files.md:460, 02-top-level-files.md:1463).
---
## Coverage and test config
`.coveragerc` (41 lines) verbatim head (`.coveragerc:1-3`):
```ini
[run]
concurrency = thread,multiprocessing
omit =
```
Omitted speech/core paths include (`.coveragerc:13-24`, `.coveragerc:32-33`):
```ini
    nemo/collections/asr/*
    nemo/collections/speechlm/*
    nemo/collections/tts/*
    nemo/core/*
    nemo/collections/common/*
```
`codecov.yml` (24 lines) disables comment and project status, enforces patch coverage (codecov.yml:1-12):
```yaml
comment: false
coverage:
  status:
    project: false
    patch:
      default:
        target: 80%
```
The patch-status path exclusions mirror the coveragerc omits (`!nemo/collections/asr`, `!nemo/collections/audio`, `!nemo/collections/speechlm`, `!nemo/collections/tts`, `!nemo/core`, `!nemo/collections/common`, plus multimodal/diffusion/nlp) (codecov.yml:8-12).
## Ignore files
`.dockerignore` (20 lines) excludes caches, logs, and artifacts (`.dockerignore:1-20`):
```
__pycache__
*.pyc
.coverage
*.log
.git
**/*.nemo
**/*.ckpt
```
`.gitignore` (198 lines) additionally excludes model/data outputs (`*.model`, `*.pkl`, `*.pt`, `output`, `runs`, `wandb`), test data (`tests/.data`, `tests/data`), example experiment dirs (`examples/*/outputs`, `examples/*/nemo_experiments`, `examples/*/wandb`), checkpoints from tutorials, `slurm*.out`, and `node_modules/` / `.vite/` voice-agent artifacts (.gitignore:1-11, .gitignore:286-320).
## Lint, format, and pre-commit
All three flake8 configs share the same select list (`.flake8:2-9`):
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
| File | Difference vs base `.flake8` |
| --- | --- |
| `.flake8.other` (13 lines) | Adds `per-file-ignores = __init__.py: F401` with comment "Package initializers intentionally re-export public APIs" (.flake8.other:11-13) |
| `.flake8.speech` (13 lines) | Same `__init__.py: F401` ignore as `.other` (.flake8.speech:11-13) |
Pylint configs (`.pylintrc:1-5`, `.pylintrc.other:1-14`, `.pylintrc.speech:1-10`):
| File | Config |
| --- | --- |
| `.pylintrc` (6 lines) | `ignore-paths=tests`, `max-line-length=119`, `ignore-patterns=.*\.ipynb$`, `recursive=y` |
| `.pylintrc.other` (14 lines) | `disable=all`, `enable=C0115,C0116,W0611,C0301` (missing docstrings, unused-import, line-too-long) |
| `.pylintrc.speech` (10 lines) | `disable=all`, `enable=W0611` (unused-import only) |
`.pre-commit-config.yaml` (46 lines) wires three hook repos (`.pre-commit-config.yaml:23-37`): `pre-commit-hooks` (check-yaml, check-case-conflict, detect-private-key, check-added-large-files `--maxkb=1000`, requirements-txt-fixer), `isort` 5.13.2 excluding `docs/`, and `black` 24.10.0 via the mypyc mirror; `default_language_version: python: python3` with quarterly autoupdate (`.pre-commit-config.yaml:15-21`).
## Agent guidance (AGENTS.md / CLAUDE.md)
Both files are byte-identical 147-line guides ("This file provides guidance when working with code in this repository") (AGENTS.md:3, CLAUDE.md:3). Project scope verbatim (AGENTS.md:7):
```
NeMo Speech — toolkit for training/deploying speech models (ASR, TTS, Speech LLM). Active collections: `asr`, `tts`, `audio`, `speechlm2`, `common`.
```
Exact parameter names and commands stated in the chunk:
| Topic | Value |
| --- | --- |
| Line length | `119`, consistent across black, isort, flake8 (AGENTS.md:17) |
| Black | `skip_string_normalization = true` (AGENTS.md:18) |
| isort | `profile = black` (AGENTS.md:19) |
| Dev install | `uv sync --locked --python 3.13 --extra all --extra cu13 --group test` (AGENTS.md:13) |
| Test markers | `unit`, `integration`, `system`, `pleasefixme` (broken — skip), `skipduringci` (AGENTS.md:48) |
| CI | GitHub Actions in `.github/workflows/` (AGENTS.md:57) |
| Docs build | `uv run make -C docs clean html`, output `docs/build/html/index.html` (AGENTS.md:98-102) |
| Hydra pattern | `@hydra_runner(config_path="conf", config_name="fast-conformer_transducer_bpe")` with CLI overrides like `model.optim.lr=1e-4 trainer.max_epochs=50` (AGENTS.md:110-121) |
Forbidden operations verbatim list (AGENTS.md:142-146): never push directly to `main`; never modify `.github/workflows/` without explicit instruction; never delete test files without explicit instruction.
## Dependency helper (nemo_dependencies.py)
206-line script defining the NeMo dependency structure via AST analysis (nemo_dependencies.py:1-5). Key functions and exact names:
- `find_python_files(directory: str) -> List[str]` scans `relevant_dirs = ['nemo', 'scripts', 'examples', 'tests']` for `*.py` (nemo_dependencies.py:7-21).
- `analyze_imports(file_path: str) -> Set[str]` parses `ast.ImportFrom` nodes starting with `nemo.`, mapping `nemo.collections.<x>` and `nemo.{core,utils,export,deploy,lightning,automodel}` (nemo_dependencies.py:24-50).
- `find_top_level_packages(nemo_root: str)` / `find_collection_modules(nemo_root: str)` enumerate `nemo/` dirs and per-collection modules (nemo_dependencies.py:53-92).
- `build_dependency_graph(nemo_root: str)` does two passes — collect packages, then record each file's package as a reverse dependency of every `nemo.*` package it imports — grouping `nemo.collections.*` under a `nemo.collections` key (nemo_dependencies.py:95-168).
- `main()` uses `nemo_root = os.path.dirname(os.path.abspath(__file__))` and prints the graph as indented JSON (nemo_dependencies.py:171-184).
## Docs, packaging, citation
`.readthedocs.yml` (37 lines, version 2): `build.os: ubuntu-22.04`, `build.tools.python: "3.10"`, `sphinx.configuration: docs/source/conf.py`, `python.install.requirements: requirements/requirements_docs.txt` (.readthedocs.yml:7-19). `MANIFEST.in` (2 lines) is a single directive verbatim (MANIFEST.in:1): `include requirements/*`. `CITATION.cff` (42 lines, `cff-version: 1.2.0`) cites "NeMo: a toolkit for Conversational AI and Large Language Models" at `https://github.com/NVIDIA-NeMo/Speech` (CITATION.cff:2-5).
## Security and third-party notices (truncated sources)
`SECURITY.md` (26 lines) directs reporters away from GitHub to the web submission form and `psirt@nvidia.com`, requesting product/driver name and version, vulnerability type, reproduction instructions, PoC, and impact (SECURITY.md:6-19). `THIRD-PARTY-NOTICES` (321 lines) inventories adapted third-party material with paths, copyright, license, and source per component — e.g. Daily/Pipecat client code (BSD-2-Clause), warp-transducer RNN-T loss (Apache-2.0), ESPnet transducer code (Apache-2.0), fairseq wav2vec/Adafactor (MIT), HiFi-GAN (MIT), CMU Pronouncing Dictionary (BSD-2-Clause) (THIRD-PARTY-NOTICES:12-30). `.secrets.baseline` (2083 lines, `version: 1.5.0`) configures detectors (Artifactory, AWS, Base64/hex high-entropy, private-key, etc.) with allowlist/heuristic filters and a `results` map of hashed findings (`.secrets.baseline:1-50`). Truncation note: the chunk truncates `.secrets.baseline` after ~line 838 of its content ("... (truncated, 62031 more characters)") and `THIRD-PARTY-NOTICES` at its final DPO entry ("... (truncated, 1008 more characters)"), so detector-by-detector results and the tail attribution entries are not covered here (02-top-level-files.md:839, 02-top-level-files.md:1762).
**Covers:** .coveragerc, .dockerignore, .flake8, .flake8.other, .flake8.speech, .gitignore, .pre-commit-config.yaml, .pylintrc, .pylintrc.other, .pylintrc.speech, .readthedocs.yml, .secrets.baseline (truncated), AGENTS.md, CITATION.cff, CLAUDE.md, codecov.yml, MANIFEST.in, nemo_dependencies.py, SECURITY.md, THIRD-PARTY-NOTICES (truncated)
