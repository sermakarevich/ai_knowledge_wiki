[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-Level Files
**In one sentence:** The repository root pins release automation on and excludes all build outputs, lockfiles, local tooling state, and generated training data from version control.
## Key points
- The root excludes Rust build output via `/target` (`.gitignore:1`), so compiled artifacts are never committed.
- The root ignores `Cargo.lock` (`.gitignore:2`), meaning the workspace does not pin exact dependency versions in version control.
- Editor and OS state is excluded via `*.swp`, `*.swo`, and `.DS_Store` (`.gitignore:3-5`), plus `.cargo/config.toml` (`.gitignore:6`).
- Claude Code runtime state is excluded via `.claude/scheduled_tasks.lock` (`.gitignore:9`).
- Python tooling outputs are excluded via `scripts/.venv/`, `scripts/__pycache__/`, `scripts/*.onnx`, `__pycache__/`, and `*.pyc` (`.gitignore:12-16`).
- Generated mel reference tensors are excluded via `*.mel.npy` (`.gitignore:19`), with the pointer to regenerate using `scripts/gen_reference.py` noted in the ignore comment (`.gitignore:18`).
- Training working state is broadly excluded: venvs (`training/**/.venv/`, `.gitignore:25`), wav/JSONL/VAD/ASR/grouped data (`training/smart-turn-zh/data/...`, `.gitignore:28-34`), PDF refs (`training/smart-turn-zh/refs/*.pdf`, `.gitignore:37`), and viewer build output (`training/smart-turn-zh/viewer/node_modules/`, `dist/`, `.gitignore:40-41`).
- Release automation is configured in `release-plz.toml` under `[workspace]` with `git_tag_enable = true` and `git_release_enable = true` (`release-plz.toml:1-3`), so releases create git tags and GitHub releases.
---
## .gitignore
Verbatim content (41 lines):
```
/target
Cargo.lock
*.swp
*.swo
.DS_Store
.cargo/config.toml

# Claude Code runtime state
.claude/scheduled_tasks.lock

# Python tooling (scripts/)
scripts/.venv/
scripts/__pycache__/
scripts/*.onnx
__pycache__/
*.pyc

# Generated mel reference tensors (regenerate with scripts/gen_reference.py)
*.mel.npy

# Jupyter checkpoints
.ipynb_checkpoints/

# Training venvs
training/**/.venv/

# Training data
training/smart-turn-zh/data/wav/*.wav
training/smart-turn-zh/data/**/*.wav
training/smart-turn-zh/data/*.jsonl
training/smart-turn-zh/data/vad_probs/
training/smart-turn-zh/data/asr_results/
training/smart-turn-zh/data/example/
training/smart-turn-zh/data/grouped/

# Training references
training/smart-turn-zh/refs/*.pdf

# Viewer
training/smart-turn-zh/viewer/node_modules/
training/smart-turn-zh/viewer/dist/
```
Grouped by ignore block:

| Block | Patterns |
|---|---|
| Rust build | `/target` (`.gitignore:1`), `Cargo.lock` (`.gitignore:2`) |
| Editor / OS / cargo | `*.swp`, `*.swo`, `.DS_Store` (`.gitignore:3-5`), `.cargo/config.toml` (`.gitignore:6`) |
| Claude Code runtime | `.claude/scheduled_tasks.lock` (`.gitignore:9`) |
| Python tooling | `scripts/.venv/`, `scripts/__pycache__/`, `scripts/*.onnx`, `__pycache__/`, `*.pyc` (`.gitignore:12-16`) |
| Generated tensors | `*.mel.npy` (`.gitignore:19`) |
| Jupyter | `.ipynb_checkpoints/` (`.gitignore:22`) |
| Training venvs | `training/**/.venv/` (`.gitignore:25`) |
| Training data | `training/smart-turn-zh/data/wav/*.wav`, `data/**/*.wav`, `data/*.jsonl`, `data/vad_probs/`, `data/asr_results/`, `data/example/`, `data/grouped/` (`.gitignore:28-34`) |
| Training refs | `training/smart-turn-zh/refs/*.pdf` (`.gitignore:37`) |
| Viewer build | `training/smart-turn-zh/viewer/node_modules/`, `viewer/dist/` (`.gitignore:40-41`) |

## release-plz.toml
Verbatim content (4 lines, 3 non-blank):
```toml
[workspace]
git_tag_enable = true
git_release_enable = true
```
Config flags:

| Key | Value | Location |
|---|---|---|
| `[workspace]` table | — | `release-plz.toml:1` |
| `git_tag_enable` | `true` | `release-plz.toml:2` |
| `git_release_enable` | `true` | `release-plz.toml:3` |

**Covers:** `.gitignore`, `release-plz.toml`
