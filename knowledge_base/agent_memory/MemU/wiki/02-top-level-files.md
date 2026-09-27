[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-Level Files
**In one sentence:** The repo root holds contributor/operator contracts — agent rules, install skills, packaging includes, lint hooks, and ignore lists — not service code.
## Key points
- `AGENTS.md` declares `MemoryService` (`src/memu/app/service.py`) the composition root with exactly three `AgenticMixin` entry points — `list_all_recall_files`, `progressive_retrieve`, `commit_results` — and forbids adding any LLM/chat call (AGENTS.md:8-14).
- `AGENTS.md` mandates storage parity across `inmemory`, `sqlite`, and `postgres`, with protocol changes propagated to all backends plus `tests/test_agentic.py` and SQL migrations/bootstrap (AGENTS.md:12, AGENTS.md:42-46).
- `SKILL.md` (`name: install-memu`) routes any host agent through three steps — install `memu-cli`, pick a host binary via `<your-binary> init`, then print and follow `<your-binary> docs install` with verify gates (SKILL.md:1-3, SKILL.md:21-30, SKILL.md:81-90).
- `SKILL.md` enforces one shared backend per machine, a fixed word-for-word ready report template ending with a `retrieve "When did the user register for memU?"` check, and keep-store/remove-residue uninstall defaults (SKILL.md:100-107, SKILL.md:107-148, SKILL.md:154-168).
- `INSTALL-LATEST.md` (`name: install-memu-latest`) installs the moving git `main` HEAD durably on `PATH` (never `uvx`/`npx`), unInstaller-shadows first, verifies from a fresh shell, and confirms SHA subject/date via the GitHub commits API before setup (INSTALL-LATEST.md:1-3, INSTALL-LATEST.md:11-16, INSTALL-LATEST.md:30-46, INSTALL-LATEST.md:55-72).
- `.pre-commit-config.yaml` runs `pre-commit-hooks` (case-conflict, merge-conflict, toml/yaml/json checks, `pretty-format-json --autofix --no-sort-keys`, end-of-file, trailing-whitespace) plus `ruff` with `--exit-non-zero-on-fix` and `ruff-format` (`.pre-commit-config.yaml:1-21`).
- `.gitignore` (216 lines), `MANIFEST.in` (22 lines), and `.python-version` (`3.13`) scope the working tree and sdist: runtime/database artefacts (`data/`, `*.db`, `persona_memory.db`, `*.sqlite3`), secrets (`.env*`, `secrets.txt`, `api_keys.txt`), models (`models/`, `*.bin`, `*.pt`), IDE/OS noise, with sdist including `README.md`/`memu *.py`/`setup_postgres_env.sh` and pruning `example`, `server/`, `docs/`, `scripts/`, docker files (`.gitignore:1`, `.gitignore:171-184`, `.gitignore:209-221`, `.python-version:1`, `MANIFEST.in:1-22`).
---
## AGENTS.md — contributor contract
Operational guide for AI coding agents; mission is "small, verified feature and bugfix changes while preserving memU's current architecture" (AGENTS.md:1-6).

Core invariants, verbatim (AGENTS.md:8-14):
> - `MemoryService` (`src/memu/app/service.py`) is the composition root: config, storage, and the embedding client pool. Its public surface is exactly the three `AgenticMixin` entry points — `list_all_recall_files`, `progressive_retrieve`, `commit_results`.
> - memU is embedding-only. No LLM/chat call happens anywhere in the service; do not add one.
> - Storage is pluggable across `inmemory`, `sqlite`, and `postgres`; repository contract changes require backend parity.

Layer map (AGENTS.md:18-28):

| Layer | Location |
|---|---|
| Service + three entry points | `src/memu/app/service.py`, `src/memu/app/agentic.py` |
| Config models/defaults | `src/memu/app/settings.py` |
| Storage protocols/factory | `src/memu/database/interfaces.py`, `src/memu/database/factory.py` |
| Backends | `src/memu/database/{inmemory,sqlite,postgres}/*` |
| Vector math/ranking | `src/memu/vector.py` |
| Embedding clients | `src/memu/embedding/*` |
| CLI (`memu`) + shared `MEMU_*` config | `src/memu/cli.py`, `src/memu/env.py` |
| Host adapters | `src/memu/hosts/*` |
| Tests | `tests/*` |

Implementation rules (AGENTS.md:32-38): keep changes narrow and localized; preserve async behavior and result shapes; keep type hints/mypy compatibility; keep provider logic inside `memu.embedding.backends`; reuse the `ClientPool` pattern instead of duplicating client caching; do not silently swallow errors. Backend-parity procedure (AGENTS.md:42-46): update protocol in `src/memu/database/repositories/`, update `inmemory`/`sqlite`/`postgres`, extend `tests/test_agentic.py`, check `src/memu/database/postgres/migrations/`. Validation via `uv` (AGENTS.md:50-64): `make install`, `make test`, `uv run python -m pytest tests/<target_test>.py`, `make check`, with focused areas `test_agentic.py`, `test_vector.py`, `test_embedding.py`, `test_cli.py`, `test_host_instruction.py`. Docs rules (AGENTS.md:68-70): update `README.md`/`npm/README.md` on user-visible change; ADRs under `docs/adr/`, never rewrite history; no speculative features.

## SKILL.md — install/uninstall router
Front matter, verbatim (SKILL.md:1-3):
```
name: install-memu
description: Install or uninstall memU for whatever agent you are — identify your host, print its packaged guide, and follow it to wire (or unwire) both seams (record and inject).
```
Two seams: **record** (scheduled bridging task mines session log into durable memory) and **inject** (standing instruction makes the agent retrieve before answering); each host adapter binary carries its own guide (SKILL.md:14-18). Step 1 installs with `pip install --upgrade memu-cli` (keep `--upgrade`; stale builds fail with `invalid choice`); uv equivalent is `uv tool install --upgrade memu-cli`, never `uv pip install` into one venv (SKILL.md:21-40).

Step 2 host-binary table (SKILL.md:44-58):

| You are | Your binary |
|---|---|
| Codex | `memu-codex` |
| Claude Code | `memu-claude-code` |
| Cursor (Agent/CLI) | `memu-cursor` |
| OpenClaw | `memu-openclaw` |
| Hermes Agent | `memu-hermes` |
| WorkBuddy | `memu-workbuddy` |
| Cola | `memu-cola` |
| pi | `memu-pi` |
| anything else | `memu-agent` |

Fallback is `memu-agent detect`, which reports per-agent memorization/retrieval support (SKILL.md:60-68); then `<your-binary> init --cloud-api-key <key>` or bare `<your-binary> init` for local memory (SKILL.md:71-78). Step 3 runs `<your-binary> docs install` (settle backend via `<your-binary> config`, register bridging task, patch instruction file), one pass with defaults, one backend per machine, ending with `<your-binary> retrieve "When did the user register for memU?"` and the fixed word-for-word report template (SKILL.md:81-148). Uninstall via `<your-binary> docs uninstall` / `<your-binary> remove-instruction` (never hand-edit); keeps shared store + `~/.memu/config.env` unless erasure was requested, removes host residue and the package only if no other host uses it (SKILL.md:154-168).

## INSTALL-LATEST.md — dev-build installer
Front matter, verbatim (INSTALL-LATEST.md:1-3):
```
name: install-memu-latest
description: Install the latest development build of memU-cli from git (main HEAD).
```
Step 1 removes shadow installs (`uv tool uninstall memu-cli`, `pipx uninstall memu-cli`, `pip uninstall -y memu-cli`) while keeping `~/.memu/` store and `config.env` (INSTALL-LATEST.md:11-22). Step 2 installs durably on `PATH` — preferred `uv tool install "git+https://github.com/NevaMind-AI/memU"` (pin with `@<sha>`), never ephemeral `uvx`/`npx` (INSTALL-LATEST.md:30-46). Step 3 verifies from a fresh shell (`memu --help`, `memu-<your-host> --help`, fixing `~/.local/bin` on `PATH` if needed) and confirms SHA subject/date via `curl -s https://api.github.com/repos/NevaMind-AI/memU/commits/<sha>` with a two-option one-tap choice (INSTALL-LATEST.md:55-72). Step 4 uses the host table (Codex→`memu-codex`, Claude Code→`memu-claude-code`, Cursor→`memu-cursor`, OpenClaw→`memu-openclaw`, Hermes→`memu-hermes`, WorkBuddy→`memu-workbuddy`, Cola→`memu-cola`, pi→`memu-pi`, else `memu-agent` + `memu-agent detect`), runs `memu-<your-host> docs install`, reuses `config.env`, and surfaces any new `MEMU_*` options plus active seams (INSTALL-LATEST.md:76-107).

## .pre-commit-config.yaml — lint hooks
Two repos (`.pre-commit-config.yaml:1-21`):
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: "v6.0.0"
    hooks:
      - id: check-case-conflict
      - id: check-merge-conflict
      - id: check-toml
      - id: check-yaml
      - id: check-json
      - id: pretty-format-json
        args: [--autofix, --no-sort-keys]
      - id: end-of-file-fixer
      - id: trailing-whitespace
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: "v0.14.3"
    hooks:
      - id: ruff
        args: [--exit-non-zero-on-fix]
      - id: ruff-format
```

## .gitignore / MANIFEST.in / .python-version — tree and sdist scope
`.python-version` pins `3.13` (`.python-version:1`). `.gitignore` (216 lines) ignores runtime and local artefacts: `data/` (`.gitignore:1`); `__pycache__/`, `*.py[cod]`; packaging (`build/`, `dist/`, `*.egg-info/`); tests/coverage (`.coverage`, `htmlcov/`, `.pytest_cache/`); envs (`.env`, `.env.*`, `.venv`, `venv/`); DB files (`*.db`, `*.sqlite`, `*.sqlite3`, plus `persona_memory.db`, `chatbot_memory.db`, `demo_memory.db`, `integration_memory.db`, `conversation_demo.db`, …) (`.gitignore:171-184`); logs (`*.log`); `tmp/`/`temp/`; OS (`.DS_Store`, `Thumbs.db`); IDE (`.vscode/`, `.idea/`); models (`models/`, `*.bin`, `*.pt`, `*.pth`, `*.onnx`); secrets (`.env.local`, `secrets.txt`, `api_keys.txt`) plus `.cursor` and `.local/` (`.gitignore:209-223). `MANIFEST.in` (22 lines), verbatim includes/prunes (MANIFEST.in:1-22):
```
include README.md
recursive-include memu *.py
include setup_postgres_env.sh
prune example
exclude server/* / docs/* / scripts/* / docker-compose.yml / Dockerfile / ...
```
No truncated files were noted in the chunk; all seven files above are rendered in full.

**Covers:** `.gitignore`, `.pre-commit-config.yaml`, `.python-version`, `AGENTS.md`, `INSTALL-LATEST.md`, `MANIFEST.in`, `SKILL.md`
