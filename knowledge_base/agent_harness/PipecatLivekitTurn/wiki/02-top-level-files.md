> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-level-files
**In one sentence:** The top-level-files component captured in this chunk consists solely of the repository's `.gitignore`, which excludes Python bytecode, packaging, virtual-environment, secret, cache, and OS artifacts from version control.
## Key points
- The chunk grounds exactly one top-level file, `.gitignore`, and no source, packaging, example, or test files appear in it (`.gitignore:1-11`).
- It excludes Python bytecode artifacts via `__pycache__/` (`.gitignore:1`) and `*.py[cod]` (`.gitignore:2`), keeping compiled output out of the repo.
- It excludes Python packaging outputs via `*.egg-info/` (`.gitignore:3`), `build/` (`.gitignore:4`), and `dist/` (`.gitignore:5`).
- It excludes local virtual environments via both `.venv/` (`.gitignore:6`) and `venv/` (`.gitignore:7`).
- It excludes local secrets and configuration via `.env` (`.gitignore:8`), so environment-provided credentials are never committed.
- It excludes tool caches (`.pytest_cache/` at `.gitignore:9`, `.ruff_cache/` at `.gitignore:10`) and the macOS `.DS_Store` file (`.gitignore:11`).
---
## `.gitignore`
Verbatim content (12 lines reported in chunk, 11 ignore entries):
```
__pycache__/
*.py[cod]
*.egg-info/
build/
dist/
.venv/
venv/
.env
.pytest_cache/
.ruff_cache/
.DS_Store
```
| Entry | Ignores |
|---|---|
| `__pycache__/` (`.gitignore:1`) | Python bytecode cache directories |
| `*.py[cod]` (`.gitignore:2`) | Compiled Python files |
| `*.egg-info/` (`.gitignore:3`) | Package egg metadata |
| `build/` (`.gitignore:4`) | Build output directory |
| `dist/` (`.gitignore:5`) | Distribution output directory |
| `.venv/` (`.gitignore:6`) | Virtual environment (dotted) |
| `venv/` (`.gitignore:7`) | Virtual environment (plain) |
| `.env` (`.gitignore:8`) | Local environment/secret file |
| `.pytest_cache/` (`.gitignore:9`) | pytest cache |
| `.ruff_cache/` (`.gitignore:10`) | Ruff cache |
| `.DS_Store` (`.gitignore:11`) | macOS Finder metadata |
**Covers:** `.gitignore`
