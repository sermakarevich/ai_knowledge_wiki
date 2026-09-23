[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-level-files
**In one sentence:** The top-level-files component captured in this chunk is the repository's `.gitignore`, which excludes OS, Python, environment, IDE, log, weight, and cache artefacts from version control.
## Key points
- The component covers exactly one source file, `.gitignore` (58 lines), defining what the repo checkout leaves untracked.
- It excludes macOS artefacts `.DS_Store`, `.AppleDouble`, and `.LSOverride` (`.gitignore:9`, `.gitignore:10`, `.gitignore:11`).
- It excludes Python build artefacts including `__pycache__/`, `*.py[cod]`, `*$py.class`, `*.so`, `build/`, `dist/`, `*.egg-info/`, and `*.egg` (`.gitignore:15`, `.gitignore:16`, `.gitignore:17`, `.gitignore:18`, `.gitignore:20`, `.gitignore:22`, `.gitignore:32`, `.gitignore:34`).
- It excludes virtual environments `.venv/`, `venv/`, `ENV/`, and `env/` (`.gitignore:37`, `.gitignore:38`, `.gitignore:39`, `.gitignore:40`).
- It excludes IDE/editor artefacts `.idea/`, `.vscode/`, `*.swp`, and `*.swo` (`.gitignore:43`, `.gitignore:44`, `.gitignore:45`, `.gitignore:46`).
- It excludes Jupyter checkpoints (`.ipynb_checkpoints/`), logs (`*.log`), and caches (`.cache/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`) (`.gitignore:49`, `.gitignore:52`, `.gitignore:62`, `.gitignore:63`, `.gitignore:64`, `.gitignore:65`).
- It excludes model weights and large artefacts `*.pt`, `*.pth`, `*.bin`, `*.safetensors`, and `*.ckpt`, noted as hosted on Hugging Face (`.gitignore:54`, `.gitignore:55`, `.gitignore:56`, `.gitignore:57`, `.gitignore:58`).
---
## OS artefacts
Verbatim entries (`.gitignore:9`, `.gitignore:10`, `.gitignore:11`):

```
.DS_Store
.AppleDouble
.LSOverride
```

## Python artefacts
Verbatim entries (`.gitignore:15`, `.gitignore:16`, `.gitignore:17`, `.gitignore:18`, `.gitignore:19`, `.gitignore:20`, `.gitignore:21`, `.gitignore:22`, `.gitignore:23`, `.gitignore:24`, `.gitignore:25`, `.gitignore:26`, `.gitignore:27`, `.gitignore:28`, `.gitignore:29`, `.gitignore:30`, `.gitignore:32`, `.gitignore:33`, `.gitignore:34`):

| Pattern | Meaning in file |
|---|---|
| `__pycache__/` | Bytecode cache directory |
| `*.py[cod]` | Compiled Python files |
| `*$py.class` | Jython class files |
| `*.so` | Compiled extensions |
| `.Python`, `build/`, `develop-eggs/`, `dist/`, `downloads/`, `eggs/`, `.eggs/`, `lib/`, `lib64/`, `parts/`, `sdist/`, `var/`, `wheels/` | Build / packaging outputs |
| `*.egg-info/`, `.installed.cfg`, `*.egg` | Egg metadata and packages |

## Environments, IDE, Jupyter, and logs
Verbatim entries (`.gitignore:37`, `.gitignore:38`, `.gitignore:39`, `.gitignore:40`, `.gitignore:43`, `.gitignore:44`, `.gitignore:45`, `.gitignore:46`, `.gitignore:49`, `.gitignore:52`):

| Pattern | Category |
|---|---|
| `.venv/`, `venv/`, `ENV/`, `env/` | Virtual environments |
| `.idea/`, `.vscode/`, `*.swp`, `*.swo` | IDE / editor |
| `.ipynb_checkpoints/` | Jupyter |
| `*.log` | Logs |

## Model weights and caches
Verbatim comment: `# Model weights / large artefacts (will be hosted on Hugging Face)` (`.gitignore:54`):

| Pattern | Category |
|---|---|
| `*.pt`, `*.pth`, `*.bin`, `*.safetensors`, `*.ckpt` | Model weights / large artefacts |
| `.cache/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/` | Cache |

**Covers:** `.gitignore`
