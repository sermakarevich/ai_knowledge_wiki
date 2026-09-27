> [[index|Wiki]] | [[summary|Summary]]
# xcc-zach/xtalk — Digest

## 1. [[wiki/01-overview|Overview]]

**In one sentence:** X-Talk is an open-source, full-duplex, cascaded spoken dialogue system framework for low-latency, interruptible speech interaction (01-overview.md:20).

## Key points

- X-Talk is an open-source full-duplex cascaded spoken dialogue system framework (01-overview.md:20).
- Speech flow is optimized for low latency, supports natural user interruption during interaction, and encodes paralinguistic information (e.g. environment noise, emotion) in parallel (01-overview.md:21-24).
- New models and relevant logic can be added within one Python script and integrated with the default pipeline (01-overview.md:25-26).
- The framework backend is pure Python with nothing to build and install beyond `pip install` (01-overview.md:27-28).
- Concurrency is provided through an asynchronous backend and websocket-based implementation for deployment from web browsers to edge devices (01-overview.md:29-31).
- The documented quickstart path uses AliCloud APIs, a JSON model config, and the `examples/sample_app/configurable_server.py` startup script serving the demo at `http://localhost:7635` (01-overview.md:114-161).
- The project is in active prototyping with interfaces subject to change, and points to a live demo, demo videos, and readthedocs docs (01-overview.md:18, 01-overview.md:47-50, 01-overview.md:166-168).

## 2. [[wiki/02-top-level-files|top-level-files]]

**In one sentence:** The top-level files define repo hygiene, toolchain pins, documentation publishing, contribution rules, and docs-site structure — not runtime code.

## Key points

- `.gitattributes` routes only `pysc/**` through Git LFS (`filter=lfs diff=lfs merge=lfs -text`) (`.gitattributes:1`).
- `.gitignore` is a standard Python gitignore (bytecode, packaging, test/coverage, envs, editors) plus X-Talk-specific entries `asset/`, `.gradio/`, `.vscode`, `examples/sample_server/node_modules/`, `/logs/`, `server_configs/`, `/data/` (`.gitignore:1-4`, `.gitignore:177-188`).
- `.pre-commit-config.yaml` pins three hooks: `psf/black` rev `24.3.0` (`id: black`), `charliermarsh/ruff-pre-commit` rev `v0.3.2` (`id: ruff`), `pre-commit/mirrors-mypy` rev `v1.9.0` (`id: mypy`) (`.pre-commit-config.yaml:1-14`).
- `.readthedocs.yaml` (version 2) builds docs with Ubuntu 24.04 + Python 3.13, uses `mkdocs.yml` as configuration, and installs `docs/requirements.txt` (`.readthedocs.yaml:1-13`).
- `AGENTS.md` forbids self-directed commits, requires `feature:`/`docs:`/`refactor:`/`fix:`/`chore:` prefixes, requires Chinese `*.zh.md` doc updates, and states frontend/backend design rules (platform isolation, NumPy vs. JSDoc styles, direct attribute access, sparing try/catch) (`AGENTS.md:1-25`).
- `mkdocs.yml` defines a Material-themed bilingual (en default + zh) docs site named `xtalk` with search/i18n plugins, `pymdownx` markdown extensions, and nav trees for Home, Quickstart, Tutorial, App Tutorial, Technical Reference, and API (`mkdocs.yml:1-5`, `mkdocs.yml:30-42`, `mkdocs.yml:105-141`).
- No source files in this chunk were truncated; all six files are shown in full.

## The system in five moves

1. X-Talk positions itself as an open-source, full-duplex, cascaded spoken dialogue framework for low-latency, interruptible speech interaction.
2. It differentiates on interaction quality: optimized speech flow plus parallel paralinguistic encoding of noise and emotion, with natural user interruption.
3. It lowers adoption cost: pure-Python backend with pip-only install, one-script model integration, and async websocket deployment from browsers to edge devices.
4. It makes the promise runnable: an AliCloud-backed quickstart with JSON model config served via `configurable_server.py` on port 7635, backed by a live demo and docs.
5. It scaffolds the prototyping project around that core: LFS/gitignore hygiene, pinned black/ruff/mypy hooks, and readthedocs/mkdocs bilingual docs publishing.
6. It governs contributions accordingly: no self-directed commits, prefixed messages, Chinese doc parity, and frontend/backend design rules — matching the active-prototyping status.
