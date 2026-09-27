# Task: chapter 00 — Setup (two machines, uv project, justfile, GPU sharing, `just check`)

Read `specs/COMMON.md` and `index.md` first (cwd `/Users/sergii/.ai/knowledge/research_topics/training_and_self_evolution/tutorials/llm_training`).

## Problem
The tutorial folder has only `index.md` and `specs/`. We need the runnable project skeleton
(`project/`), the Mac ↔ `rtx` workflow (push code, run remotely, pull results), the GPU-sharing
helper, a connectivity/speed check, and the chapter `00_setup.md` that explains all of it.

## Fix — create these files

### `project/pyproject.toml`
```toml
[project]
name = "llm-tutorial"
version = "0.1.0"
requires-python = ">=3.12,<3.13"
dependencies = [
  "torch>=2.13", "transformers>=5.16", "datasets>=5.0", "tokenizers>=0.23",
  "trl>=1.12", "peft>=0.20", "accelerate>=1.14",
  "pydantic>=2", "pyyaml>=6", "typer>=0.12", "rich>=13", "python-dotenv>=1.0",
  "httpx>=0.27", "matplotlib>=3.9", "numpy>=2",
]
[project.optional-dependencies]
gpu = [                       # Linux/CUDA only — installed on rtx with `uv sync --extra gpu`
  "bitsandbytes>=0.50; sys_platform == 'linux'",
  "flash-linear-attention>=0.5; sys_platform == 'linux'",
  "lm_eval>=0.4.12; sys_platform == 'linux'",
]
[dependency-groups]
dev = ["pytest>=8"]
[tool.uv]
package = true
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
[tool.hatch.build.targets.wheel]
packages = ["src/llm_tutorial"]
[tool.pytest.ini_options]
markers = ["slow: needs the GPU box or the network; excluded from the DoD run"]
```
Run `uv sync` on the Mac (CPU torch) and `uv lock`; commit `uv.lock`.

### `project/.env.template` (copy to `.env`, which is gitignored)
```bash
RTX_HOST=rtx                              # ssh alias from ~/.ssh/config
RTX_PROJECT_DIR=/home/sergii/projects/llm_training
RTX_UV=/home/sergii/.local/bin/uv
OLLAMA_URL=http://127.0.0.1:11435         # tunnel to rtx (fallback http://localhost:11434)
OLLAMA_MODEL=qwen3.8:27b
HF_HOME=/home/sergii/.cache/huggingface   # on rtx
```
`project/.gitignore`: `.venv/`, `.env`, `__pycache__/`, `runs/*` but keep `!runs/**/*.json`, `!runs/**/*.png`, `!runs/**/*.md`, `!runs/**/*.log` (use the `runs/**` negation pattern so pulled results are committed but checkpoints never are), `data/`.

### `project/justfile` (`set dotenv-load := true`) — recipes, each with a one-line comment:
- `sync` → `uv sync`; `test` → `uv run pytest tests/ -q -m "not slow"`.
- `push` → `rsync -az --delete --exclude .venv --exclude runs --exclude data --exclude .git --exclude __pycache__ --exclude .pytest_cache ./ $RTX_HOST:$RTX_PROJECT_DIR/`.
- `pull` → `rsync -az --prune-empty-dirs --include '*/' --include '*.json' --include '*.png' --include '*.md' --include '*.log' --exclude '*' $RTX_HOST:$RTX_PROJECT_DIR/runs/ runs/`.
- `remote cmd` → `ssh -o ClearAllForwardings=yes $RTX_HOST "cd $RTX_PROJECT_DIR && . .venv/bin/activate && {{cmd}}"`.
- `remote-sync` → push, then remote `$RTX_UV sync --extra gpu` (creates `.venv` on rtx; first run downloads ~3 GB, several minutes).
- `remote-bg name cmd` → `ssh … "mkdir -p $RTX_PROJECT_DIR/runs/logs && tmux new-session -d -s {{name}} \"cd $RTX_PROJECT_DIR && . .venv/bin/activate && ({{cmd}}) 2>&1 | tee runs/logs/{{name}}.log\""`.
- `remote-log name` → `tail -n 60 runs/logs/{{name}}.log` on rtx; `remote-wait name` → loop `while tmux has-session -t {{name}} 2>/dev/null; do sleep 30; done` on rtx then `tail -n 20` of the log; `remote-kill name` → `tmux kill-session -t {{name}}`.
- `gpu-status` → `ssh … "nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv; ollama ps"`.
- `gpu-free` → remote `python -m llm_tutorial.gpu free` (see below).
- `check` → remote `python -m llm_tutorial.check` (GPU present, bf16 matmul TFLOPS, `fla` importable) AND locally `uv run python -m llm_tutorial.check --cpu` (prints versions, confirms no GPU).
Note: `just` recipes with `{{cmd}}` containing quotes — use the `remote` recipe pattern from `../graph_rag2/project/justfile` (`trim_start_match`) if arguments need `name=` handling.

### `project/src/llm_tutorial/__init__.py`, `config.py`, `gpu.py`, `check.py`
- `config.py`: `load_yaml(path) -> dict` and a `RunPaths` helper (`runs/<run_name>/` with `metrics.json`, `samples.md`, `loss.png`, `checkpoints/`), plus `write_metrics(run_dir, dict)` that merges into `metrics.json` (`json.dump(indent=2, sort_keys=True)`). Every later chapter uses these.
- `gpu.py` (Typer app, runs on rtx): `status()` prints `nvidia-smi` numbers + `ollama ps` via `subprocess`. `free(min_free_gb: float = 20, idle_seconds: int = 60, max_wait_minutes: int = 360)`: loop — read GPU 0 utilisation every 5 s via `nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader,nounits`; if a model is loaded (`ollama ps` has rows) and utilisation stayed < 10 % for `idle_seconds`, run `ollama stop <model>` for each loaded model; once free memory ≥ `min_free_gb`, print it and exit 0; if utilisation was ≥ 10 % (someone generating), print "GPU busy (Ollama serving another client), waiting…" and keep polling until `max_wait_minutes`, then exit 1. Never kill anything. Pure functions (`parse_nvidia_smi(text) -> list[dict]`, `parse_ollama_ps(text) -> list[str]`) so tests can cover parsing with canned strings.
- `check.py`: `--cpu` mode prints Python/torch/transformers/trl/peft versions and `torch.cuda.is_available()`; GPU mode additionally prints GPU name, total/free memory, a 4096×4096 bf16 matmul benchmark in TFLOP/s (≈150–165 TFLOP/s expected on a 4090), and whether `import fla` works. Exit non-zero if CUDA is missing in GPU mode.

### On `rtx`
Run `just remote-sync` for real (uv is already installed at `~/.local/bin/uv`; do not reinstall). Then `just check` and `just gpu-status`; paste the real output into the chapter. If `qwen3.8:27b` is loaded and busy, do NOT stop it — `just check` needs < 1 GB, run it anyway and note the shared state in the chapter. Install `just` on rtx too (`curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to ~/.local/bin`) so the same recipes work when logged in there; mention it.

### `project/tests/test_00_setup.py`
Tests for `gpu.parse_nvidia_smi`, `gpu.parse_ollama_ps` (canned strings incl. the empty "no models" case), `config.write_metrics` merge behaviour (tmp_path), and `check` in `--cpu` mode via `typer.testing.CliRunner` (asserts exit 0 and that the output mentions "torch").

### `00_setup.md` (chapter)
Sections: the tools (uv, just, ssh/rsync/tmux — one paragraph each, plain language); why two machines and what lives where (the table from `index.md`); the files in `project/` (tree with one-line comments, like `../neo4j/00_setup.md`); `.env`; the push/remote/pull loop (mermaid sequence diagram Mac → rtx → Mac); GPU sharing with Ollama and what `just gpu-free` does and refuses to do; running `just check` on both machines with real output; a "first `just remote-bg` job" example (`nvidia-smi -l 5` for 30 s is enough); Troubleshooting (ssh port-forward errors → `ClearAllForwardings`, `uv: command not found` on rtx → full path, `just gpu-free` waiting forever → another client is generating, tmux session vanished → check the log); Exercises.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Files to commit: `project/pyproject.toml`, `project/uv.lock`, `project/.env.template`,
`project/.gitignore`, `project/justfile`, `project/src/llm_tutorial/{__init__,config,gpu,check}.py`,
`project/tests/test_00_setup.py`, `project/runs/.gitkeep`, `00_setup.md`. Verify token: `"What you will learn"` in `00_setup.md`.

## Scope & constraints
Do not write other chapters or modules. Do not change `index.md`. Do not stop Ollama's model unless
`gpu-free`'s idle rule says it is idle (and chapter 00 does not need the GPU memory anyway).
