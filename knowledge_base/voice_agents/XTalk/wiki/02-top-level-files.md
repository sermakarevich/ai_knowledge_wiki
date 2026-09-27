> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# top-level-files
**In one sentence:** The top-level files define repo hygiene, toolchain pins, documentation publishing, contribution rules, and docs-site structure — not runtime code.
## Key points
- `.gitattributes` routes only `pysc/**` through Git LFS (`filter=lfs diff=lfs merge=lfs -text`) (`.gitattributes:1`).
- `.gitignore` is a standard Python gitignore (bytecode, packaging, test/coverage, envs, editors) plus X-Talk-specific entries `asset/`, `.gradio/`, `.vscode`, `examples/sample_server/node_modules/`, `/logs/`, `server_configs/`, `/data/` (`.gitignore:1-4`, `.gitignore:177-188`).
- `.pre-commit-config.yaml` pins three hooks: `psf/black` rev `24.3.0` (`id: black`), `charliermarsh/ruff-pre-commit` rev `v0.3.2` (`id: ruff`), `pre-commit/mirrors-mypy` rev `v1.9.0` (`id: mypy`) (`.pre-commit-config.yaml:1-14`).
- `.readthedocs.yaml` (version 2) builds docs with Ubuntu 24.04 + Python 3.13, uses `mkdocs.yml` as configuration, and installs `docs/requirements.txt` (`.readthedocs.yaml:1-13`).
- `AGENTS.md` forbids self-directed commits, requires `feature:`/`docs:`/`refactor:`/`fix:`/`chore:` prefixes, requires Chinese `*.zh.md` doc updates, and states frontend/backend design rules (platform isolation, NumPy vs. JSDoc styles, direct attribute access, sparing try/catch) (`AGENTS.md:1-25`).
- `mkdocs.yml` defines a Material-themed bilingual (en default + zh) docs site named `xtalk` with search/i18n plugins, `pymdownx` markdown extensions, and nav trees for Home, Quickstart, Tutorial, App Tutorial, Technical Reference, and API (`mkdocs.yml:1-5`, `mkdocs.yml:30-42`, `mkdocs.yml:105-141`).
- No source files in this chunk were truncated; all six files are shown in full.
---
## .gitattributes
Single-line LFS rule (`.gitattributes:1`):

```
pysc/** filter=lfs diff=lfs merge=lfs -text
```

Everything outside `pysc/**` follows default git handling.
## .gitignore
188-line Python gitignore (`.gitignore:1-188`). Standard sections include bytecode (`__pycache__/`, `*.py[cod]`, `*$py.class`) (`.gitignore:1-4`), C extensions (`*.so`) (`.gitignore:7`), packaging (`build/`, `dist/`, `*.egg-info/`, `*.egg`) (`.gitignore:10-27`), test/coverage (`.tox/`, `.coverage*`, `.pytest_cache/`) (`.gitignore:40-52`), envs (`.venv`, `venv/`, `env/`) (`.gitignore:130-138`), and editor/type-checker caches (`.mypy_cache/`, `.pyre/`, `.ruff_cache/`) (`.gitignore:149-171`).

X-Talk-specific tail entries (`.gitignore:177-188`):

```
asset/
.gradio/
.vscode
# Node.js dependencies
examples/sample_server/node_modules/
# User defined
/logs/
server_configs/
/data/
```

| Entry | What it excludes |
|---|---|
| `asset/` | Project asset directory |
| `.gradio/` | Gradio cache |
| `.vscode` | VS Code settings |
| `examples/sample_server/node_modules/` | Sample-server Node dependencies |
| `/logs/` | Root logs directory |
| `server_configs/` | Server configs directory |
| `/data/` | Root data directory |
## .pre-commit-config.yaml
Three pinned repos (`.pre-commit-config.yaml:1-14`):

```
repos:
  - repo: https://github.com/psf/black
    rev: 24.3.0
    hooks:
      - id: black

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.3.2
    hooks:
      - id: ruff

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.9.0
    hooks:
      - id: mypy
```

| Repo | rev | hook id |
|---|---|---|
| `https://github.com/psf/black` | `24.3.0` | `black` |
| `https://github.com/charliermarsh/ruff-pre-commit` | `v0.3.2` | `ruff` |
| `https://github.com/pre-commit/mirrors-mypy` | `v1.9.0` | `mypy` |
## .readthedocs.yaml
Full content (`.readthedocs.yaml:1-13`):

```
version: 2

build:
  os: ubuntu-24.04
  tools:
    python: "3.13"

mkdocs:
   configuration: mkdocs.yml

python:
   install:
   - requirements: docs/requirements.txt
```

| Key | Value |
|---|---|
| `version` | `2` |
| `build.os` | `ubuntu-24.04` |
| `build.tools.python` | `"3.13"` |
| `mkdocs.configuration` | `mkdocs.yml` |
| `python.install` | `requirements: docs/requirements.txt` |
## AGENTS.md
Contribution and design rules, verbatim excerpts (`AGENTS.md:1-25`):

```
# Commit Guideline

DO NOT commit by yourself. Commit changes only on my request.
```

```
commit messages should start with `feature:`, `docs:`, `refactor:`, `fix:` or `chore:`.
```

```
Documents are under `docs`; when updating the documents, always update their Chinese version `*.zh.md` if necessary.
```

Design concerns (`AGENTS.md:20-28`):

- Frontend platform-specific implementations must not leak outside `frontend/src/platforms` (`AGENTS.md:22`).
- Code in other frontend folders must depend on platform abstractions only; public frontend APIs may use Web-first types (`AGENTS.md:22-23`).
- Backend: prefer direct attribute access over `getattr` when the type is explicit (`AGENTS.md:24`).
- Docstrings required on all externally exposed backend/frontend APIs; backend uses NumPy style, frontend uses TypeDoc-compatible JSDoc/TSDoc `/** ... */` (`AGENTS.md:25-27`).
- Avoid `try catch` except when urgently necessary (`AGENTS.md:28`).
## mkdocs.yml
Site identity and repo links (`mkdocs.yml:1-4`):

```
site_name: xtalk
docs_dir: docs
repo_url: https://github.com/xcc-zach/xtalk
repo_name: xcc-zach/xtalk
```

Theme: `material` with light/dark palettes (primary white/black, accent teal), `navigation.tabs`, `navigation.sections`, `content.code.copy`, `content.code.annotate` (`mkdocs.yml:5-26`). Search separator `'[\s\u200b\-]'` and `i18n` plugin with `docs_structure: suffix`, English default (`site_name: X-Talk Documentation`) plus Chinese (`site_name: X-Talk文档`, `link: /zh/`) and per-tab `nav_translations` (Home→首页, Tutorial→教程, etc.) (`mkdocs.yml:30-95`).

Markdown extensions (`mkdocs.yml:96-104`): `md_in_html`, `pymdownx.highlight` (`anchor_linenums: true`, `line_spans: __span`, `pygments_lang_class: true`), `pymdownx.inlinehilite`, `pymdownx.snippets`, `pymdownx.superfences`.

Nav tree (`mkdocs.yml:105-141`): `Home: index.md`, `Quickstart: quickstart.md`, `Tutorial/Basic Usage` (`tutorial/start_the_service.md`, `tutorial/config_the_service.md`, `tutorial/introduce_a_new_model.md`, `tutorial/customize_the_service.md`), `Tutorial/Other` (LLM agent, tools, text input, local-deployment sample, service config, logging, testing, bot2bot), `App Tutorial` (model configuration, add tools, web search, voice wake), `Technical Reference` (system design, supported models, ASR/TTS/enhancer/VAD/turn-detector/forced-aligner designs, `model_clone_reset.md`, `developer/recipe.md`), `API` (`api/client/globals.md`, `api/server/index.md`).
**Covers:** `.gitattributes`, `.gitignore`, `.pre-commit-config.yaml`, `.readthedocs.yaml`, `AGENTS.md`, `mkdocs.yml`
