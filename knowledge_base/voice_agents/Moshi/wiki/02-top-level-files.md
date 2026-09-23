[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-level-files
**In one sentence:** The top-level files define repo hygiene (ignores), licensing, dev/test hooks, the Docker Swarm deployment topology, and the user-facing FAQ.
## Key points
- `.dockerignore` excludes only `moshi/.venv/*` from Docker build contexts (`.dockerignore:1`).
- `.gitignore` is a standard Python template plus Moshi-specific entries for model audio/artifacts (`*.safetensors` at `.gitignore:182`, `*.wav` at `.gitignore:183`, `*.mp3` at `.gitignore:191`), traces (`trace*.json` at `.gitignore:184`, `timings.json` at `.gitignore:197`, `mlx-trace.json` at `.gitignore:198`), and secrets/config (`*.pem` at `.gitignore:189`, `/moshi-demo/config.sh` at `.gitignore:193`, `/scripts/token.txt` at `.gitignore:199`).
- `.pre-commit-config.yaml` defines five local hooks: `flake8-moshi`, `tests-moshi`, `ruff-moshi_mlx`, `ruff-format-moshi_mlx`, `pyright-moshi_mlx` (`.pre-commit-config.yaml:7-39`).
- `deploy.sh` builds/pushes the Swarm stack and deploys it over SSH to `root@moshi-chat.kyutai.org` using short `COMMIT_SHA` as the image tag (`deploy.sh:3-7`).
- `FAQ.md` states Moshi is English-only, training data will not be released, finetuning lives in `moshi-finetune`, quantized PyTorch is unsupported, and MLX/Rust stop after ~5 min due to a fixed buffer (`FAQ.md:5-7`, `FAQ.md:11-13`, `FAQ.md:24-30`, `FAQ.md:33-36`).
- `swarm-config.yml` deploys `traefik` (80/443, Let's Encrypt), `frontend` (port 5173, path `/`), and `backend` (port 8998, path `/api`, 1 GPU reservation, `NO_TORCH_COMPILE=1`) plus Portainer monitoring (`swarm-config.yml:1-65`).
- Licensing is dual Apache-2.0 (`LICENSE-APACHE:1-202`) and MIT (`LICENSE-MIT:1-24`); dev tooling pins are `pre-commit>=3.8`, `pyright>=1.1`, `flake8>=7.1` (`requirements-dev.txt:1-3`).
---
## Ignore files
`.dockerignore` is one line:
```
moshi/.venv/*
```
(`.dockerignore:1`).

`.gitignore` (188 lines) combines the Python `gitignore` template with Moshi additions. Moshi-specific tail entries (`.gitignore:181-202`):
```
*~
*.safetensors
*.wav
trace*.json
*.flac
pkg
*.nsys-rep
*.sqlite
*.pem
*.tgz
*.mp3
*.ogg
/moshi-demo/config.sh
log.*
laurent/cuda-test/check
client/node_modules
timings.json
mlx-trace.json
/scripts/token.txt
uv.lock
tts-outputs
```
Standard sections retained verbatim include `__pycache__/`, `*.py[cod]` (`.gitignore:2-3`), `build/`, `dist/`, `*.egg-info/` (`.gitignore:8-24`), `.tox/`, `.coverage*`, `.pytest_cache/` (`.gitignore:39-50`), `.env`, `.venv`, `env/`, `venv/` (`.gitignore:124-131`), `.mypy_cache/` (`.gitignore:142-144`), and `.vscode/` (`.gitignore:163-164`).

## Pre-commit hooks and dev requirements
`.pre-commit-config.yaml:6-39` declares `repos: [{repo: local}]` with five hooks:

| Hook id | Entry | Purpose |
|---|---|---|
| `flake8-moshi` | `bash -c 'cd moshi && flake8'` | lint `moshi` package |
| `tests-moshi` | `scripts/run_ci_when_installed.sh moshi 'cd moshi && pytest tests'` | run `moshi` tests |
| `ruff-moshi_mlx` | `bash -c 'cd moshi_mlx && uvx ruff check'` | lint `moshi_mlx` |
| `ruff-format-moshi_mlx` | `bash -c 'cd moshi_mlx && uvx ruff format --check'` | format check `moshi_mlx` |
| `pyright-moshi_mlx` | `scripts/run_ci_when_installed.sh moshi_mlx 'cd moshi_mlx && pyright'` | typecheck `moshi_mlx` |

All hooks set `pass_filenames: false, always_run: true` (`.pre-commit-config.yaml:11-39`). `requirements-dev.txt:1-3` pins:
```
pre-commit>=3.8
pyright>=1.1
flake8>=7.1
```

## Deploy script and Swarm topology
`deploy.sh:1-7` verbatim:
```
set -ex

export COMMIT_SHA=$(git rev-parse --short HEAD)

docker compose -f swarm-config.yml build --push

docker -H ssh://root@moshi-chat.kyutai.org stack deploy -c swarm-config.yml --with-registry-auth moshi
```

`swarm-config.yml` services:

| Service | Image / build | Ports / routing |
|---|---|---|
| `traefik` | `traefik:v3.6.7`, Swarm provider, entrypoints `web:80` / `websecure:443`, HTTP→HTTPS redirect, Let's Encrypt `acme.email=gabriel@kyutai.org` | `80:80`, `443:443` (`swarm-config.yml:1-33`) |
| `frontend` | `.../moshi-chat-frontend:${COMMIT_SHA}`, `context: client/` | router `Host(moshi-chat.kyutai.org) && PathPrefix(/)`, port 5173, priority 10 (`swarm-config.yml:34-46`) |
| `backend` | `.../moshi-chat-backend:${COMMIT_SHA}`, `context: moshi/`, `NO_TORCH_COMPILE=1`, 1 GPU reservation | router `Host(moshi-chat.kyutai.org) && PathPrefix(/api)`, port 8998, priority 100 (`swarm-config.yml:47-70`) |
| `agent` / `portainer` | `portainer/agent:lts` (global), `portainer/portainer-ce:lts` on `9443` | `agent_network` overlay, encrypted (`swarm-config.yml:74-96`) |

Volumes `letsencrypt`, `portainer_data`, `hf-cache`, `uv-cache`; both `agent_network` and `default` are encrypted overlay networks (`swarm-config.yml:98-116`).

## FAQ
`FAQ.md:1-65` answers, verbatim claims:
- Training code: "Some finetuning code can be found in the [kyutai-labs/moshi-finetune repo](https://github.com/kyutai-labs/moshi-finetune)." (`FAQ.md:5-7`).
- Dataset: "We will not release the pre-training dataset." (`FAQ.md:9-11`).
- Multilingual: "Moshi only speaks English." (`FAQ.md:11-13`).
- Voice/personality change requires fine tuning, "not currently supported" (`FAQ.md:15-17`).
- M1/smaller GPUs: quantizing beyond 4 bits gives "dramatic decrease in quality" (`FAQ.md:19-22`); quantized PyTorch is unsupported, "possible to use the Rust backend, which should run in int8 with CUDA" (`FAQ.md:24-26`).
- "Moshi stopped talking after 5 min. This is expected on the MLX and Rust implementation. We only use a fixed buffer" (`FAQ.md:28-32`); PyTorch "should work for unlimited times" but quality degrades with no attention sink (`FAQ.md:31-33`).
- Blank server on connect: check browser console; `Cannot read properties of undefined (reading 'addModule')` means remote-http audio block — SSH-tunnel port 8998 to localhost (`FAQ.md:35-44`).
- HTTPS certs: `openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=localhost"` (`FAQ.md:46-48`).
- 12 GB GPUs possible per issue #54; 8 GB "not possible at the moment" (`FAQ.md:50-52`).

## Licenses
- `LICENSE-APACHE` is the full Apache License 2.0 text with appendix boilerplate (`LICENSE-APACHE:1-202`).
- `LICENSE-MIT` is the standard MIT grant plus "AS IS" disclaimer (`LICENSE-MIT:1-24`).

**Covers:** `.dockerignore`, `.gitignore`, `.pre-commit-config.yaml`, `deploy.sh`, `FAQ.md`, `LICENSE-APACHE`, `LICENSE-MIT`, `requirements-dev.txt`, `swarm-config.yml`
