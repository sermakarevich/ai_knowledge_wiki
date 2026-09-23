> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-Level Files
**In one sentence:** The top-level files define what stays out of version control, how HACS presents the integration, and what ships in the source distribution.
## Key points
- `.gitignore` excludes Python build artifacts (`__pycache__/`, `*.py[cod]`, `*.egg-info/`, `dist/`, `build/`, `.eggs/`, `*.egg`, `*.whl`) from version control (`.gitignore:1-9`).
- `.gitignore` excludes virtual environments (`venv/`, `.venv/`, `env/`, `.env`) from version control (`.gitignore:11-15`).
- `.gitignore` excludes IDE and OS files (`.idea/`, `.vscode/`, `*.swp`, `*.swo`, `*~`, `.DS_Store`, `Thumbs.db`) from version control (`.gitignore:17-26`).
- `.gitignore` excludes test and coverage outputs (`.coverage`, `htmlcov/`, `.pytest_cache/`, `coverage/`) from version control (`.gitignore:28-32`).
- `.gitignore` excludes Hermes-local files (`*.hermes-home`, `local-config.yaml`) and build archives (`*.tar.gz`, `*.zip`) from version control (`.gitignore:34-40`).
- `hacs.json` declares the HACS integration name as `Hermes Voice Assistant`, the minimum Home Assistant version as `2024.8.0`, and enables README rendering via `render_readme` (`hacs.json:2-4`).
- `MANIFEST.in` ships top-level docs and assets (`README.md`, `LICENSE`, `CHANGELOG.md`, `hacs.json`, `logo.png`, `icon.png`) and recursively includes `docs`, `custom_components`, `addon`, `plugins`, `skills`, and `tests` while globally excluding `__pycache__`, `*.py[cod]`, and `.DS_Store` (`MANIFEST.in:1-8`).
---
## .gitignore
Excludes generated, local, and environment-specific files from version control (`.gitignore:1-40`).

Verbatim excerpts:
```
# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.eggs/
*.egg
*.whl
```
```
# Virtual environments
venv/
.venv/
env/
.env
```
```
# Hermes local
*.hermes-home
local-config.yaml
```
```
# Build artifacts
*.tar.gz
*.zip
```

| Group | Patterns |
|---|---|
| Python (`.gitignore:1-9`) | `__pycache__/`, `*.py[cod]`, `*.egg-info/`, `dist/`, `build/`, `.eggs/`, `*.egg`, `*.whl` |
| Virtual environments (`.gitignore:11-15`) | `venv/`, `.venv/`, `env/`, `.env` |
| IDE (`.gitignore:17-22`) | `.idea/`, `.vscode/`, `*.swp`, `*.swo`, `*~` |
| OS (`.gitignore:24-26`) | `.DS_Store`, `Thumbs.db` |
| Testing (`.gitignore:28-32`) | `.coverage`, `htmlcov/`, `.pytest_cache/`, `coverage/` |
| Hermes local (`.gitignore:34-36`) | `*.hermes-home`, `local-config.yaml` |
| Build artifacts (`.gitignore:38-40`) | `*.tar.gz`, `*.zip` |

## hacs.json
HACS metadata for the integration (`hacs.json:1-5`).

Verbatim excerpt:
```
{
  "name": "Hermes Voice Assistant",
  "homeassistant": "2024.8.0",
  "render_readme": true
}
```

| Key | Value |
|---|---|
| `name` (`hacs.json:2`) | `"Hermes Voice Assistant"` |
| `homeassistant` (`hacs.json:3`) | `"2024.8.0"` |
| `render_readme` (`hacs.json:4`) | `true` |

## MANIFEST.in
Source-distribution packaging rules: what to include and what to exclude (`MANIFEST.in:1-8`).

Verbatim excerpt:
```
include README.md LICENSE CHANGELOG.md hacs.json logo.png icon.png
recursive-include docs *.png *.md *.html
recursive-include custom_components *
recursive-include addon *
recursive-include plugins *.py *.yaml *.md
recursive-include skills *
recursive-include tests *.py
global-exclude __pycache__ *.py[cod] .DS_Store
```

| Directive | Arguments |
|---|---|
| `include` (`MANIFEST.in:1`) | `README.md`, `LICENSE`, `CHANGELOG.md`, `hacs.json`, `logo.png`, `icon.png` |
| `recursive-include docs` (`MANIFEST.in:2`) | `*.png`, `*.md`, `*.html` |
| `recursive-include custom_components` (`MANIFEST.in:3`) | `*` |
| `recursive-include addon` (`MANIFEST.in:4`) | `*` |
| `recursive-include plugins` (`MANIFEST.in:5`) | `*.py`, `*.yaml`, `*.md` |
| `recursive-include skills` (`MANIFEST.in:6`) | `*` |
| `recursive-include tests` (`MANIFEST.in:7`) | `*.py` |
| `global-exclude` (`MANIFEST.in:8`) | `__pycache__`, `*.py[cod]`, `.DS_Store` |

**Covers:** `.gitignore`, `hacs.json`, `MANIFEST.in`
