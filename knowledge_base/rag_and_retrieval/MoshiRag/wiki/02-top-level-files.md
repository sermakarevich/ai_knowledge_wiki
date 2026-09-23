> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-level files
**In one sentence:** The repo root defines hygiene, lint, licensing, dev tooling, and Swarm deployment for the Moshi-RAG system.
## Key points
- `.gitignore` (199 lines) excludes Python, packaging, test, IDE, and ML/media artifacts plus local secrets and outputs (`.gitignore:1-4`, `.gitignore:168-179`, `.gitignore:186-187`).
- `.pre-commit-config.yaml` (14 lines) wires `ruff-check`/`ruff-format` at `rev: v0.15.8` and a local `cargo fmt --all --manifest-path rust/Cargo.toml` hook (`.pre-commit-config.yaml:1-5`, `.pre-commit-config.yaml:9-12`).
- `deploy.sh` (8 lines) cleans `./moshi/.venv ./moshi/dist ./rust/target`, rebuilds/pushes via `swarm-config.yaml`, and redeploys the `moshi-rag` stack over SSH (`deploy.sh:1`, `deploy.sh:3-4`, `deploy.sh:7`).
- Dual licensing is vendored as `LICENSE-APACHE` (202 lines, Version 2.0) and `LICENSE-MIT` (24 lines, AS-IS) (`LICENSE-APACHE:1`, `LICENSE-MIT:1`).
- `requirements-dev.txt` pins only three dev tools: `pre-commit>=3.8`, `pyright>=1.1`, `flake8>=7.1` (`requirements-dev.txt:1-3`).
- `swarm-config.yaml` (148 lines) orchestrates `traefik`, `frontend` (from `client/`), `backend` (from `moshi/`), `arc_encoder` (via `Dockerfile.arc_encoder`), plus `agent`/`portainer` monitoring (`swarm-config.yaml:1`, `swarm-config.yaml:35-37`, `swarm-config.yaml:49-51`, `swarm-config.yaml:85-88`, `swarm-config.yaml:108-118`).
- Routing exposes `frontend` on `PathPrefix("/")` (priority 10) and `backend` on `PathPrefix("/api")` (priority 100) behind TLS with Let's Encrypt, while `backend` and `arc_encoder` each reserve one `gpu` (`swarm-config.yaml:41-46`, `swarm-config.yaml:71-82`, `swarm-config.yaml:19`).
---
## Ignore rules (.gitignore)
Standard Python gitignore plus ML/project-specific entries (`.gitignore:1-4`, `.gitignore:168-198`):

```gitignore
__pycache__/
*.py[cod]
*$py.class
*.so
```

```gitignore
*.safetensors
*.wav
trace*.json
*.flac
*.sqlite
*.mp3
*.ogg
/moshi-demo/config.sh
uv.lock
!rust/moshi-server/uv.lock
```

Project outputs and local state excluded (`.gitignore:186-198`):

```gitignore
results*
log
plots
/moshi/export_dir
/.qwen/
.claude
.worktrees/
```

## Lint hooks (.pre-commit-config.yaml)
Full 14-line file (`.pre-commit-config.yaml:1-12`):

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.15.8
    hooks:
      - id: ruff-check
      - id: ruff-format
  - repo: local
    hooks:
      - id: cargo-fmt
        name: cargo fmt
        entry: cargo fmt --all --manifest-path rust/Cargo.toml
        language: system
        types: [rust]
        pass_filenames: false
```

## Deploy script (deploy.sh)
Full script, `set -ex` (`deploy.sh:1-7`):

```sh
set -ex

rm -rf ./moshi/.venv ./moshi/dist ./rust/target
docker compose -f ./swarm-config.yaml build  --push --progress=plain

#docker -H ssh://root@moshi-rag.kyutai.org service update --with-registry-auth  --image rg.fr-par.scw.cloud/namespace-unruffled-tereshkova/moshi-rag-backend:tmp moshi-rag_backend
docker -H ssh://root@moshi-rag.kyutai.org stack deploy -c ./swarm-config.yaml --with-registry-auth --prune moshi-rag
```

## Licenses (LICENSE-APACHE, LICENSE-MIT)
- `LICENSE-APACHE` (202 lines) is the standard Apache-2.0 text: copyright/patent grants, redistribution conditions (a)-(d), contribution, trademark, AS-IS warranty, liability limits (`LICENSE-APACHE:1`, `LICENSE-APACHE:66-77`).
- `LICENSE-MIT` (24 lines) is the standard MIT grant plus AS-IS disclaimer (`LICENSE-MIT:1-10`, `LICENSE-MIT:15-23`):

```text
Permission is hereby granted, free of charge, to any
person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the
Software without restriction, including without
limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following
conditions:
```

No truncation noted in the chunk for either license file.

## Dev dependencies (requirements-dev.txt)
Exact contents (`requirements-dev.txt:1-3`):

```text
pre-commit>=3.8
pyright>=1.1
flake8>=7.1
```

## Swarm orchestration (swarm-config.yaml)
Services table (`swarm-config.yaml:1-136`):

| Service | Image | Build context | Notes |
|---|---|---|---|
| `traefik` | `traefik:v3.6.7` | — | Swarm provider, `:80`/`:443` entrypoints, HTTP→HTTPS redirect, Let's Encrypt (`swarm-config.yaml:3-28`) |
| `frontend` | `rg.fr-par.scw.cloud/namespace-unruffled-tereshkova/moshi-rag-frontend:tmp` | `client/` | `Host("moshi-rag.kyutai.org") && PathPrefix("/")`, port 80, priority 10 (`swarm-config.yaml:35-46`) |
| `backend` | `rg.fr-par.scw.cloud/namespace-unruffled-tereshkova/moshi-rag-backend:tmp` | `moshi/` | `PathPrefix("/api")`, port 80, priority 100, 1× `gpu` (`swarm-config.yaml:49-82`) |
| `arc_encoder` | `rg.fr-par.scw.cloud/namespace-unruffled-tereshkova/moshi-rag-arc-encoder:tmp` | `moshi/` + `Dockerfile.arc_encoder` | 1× `gpu` (`swarm-config.yaml:85-102`) |
| `agent` | `portainer/agent:lts` | — | Global mode, docker socket/volumes (`swarm-config.yaml:108-113`) |
| `portainer` | `portainer/portainer-ce:lts` | — | `9443:9443`, manager-only (`swarm-config.yaml:118-127`) |

Traefik flags verbatim (`swarm-config.yaml:6-21`):

```yaml
command:
  - "--providers.swarm.endpoint=unix:///var/run/docker.sock"
  - "--providers.swarm.exposedByDefault=false"
  - "--entrypoints.web.address=:80"
  - "--entrypoints.websecure.address=:443"
  - "--entrypoints.web.http.redirections.entryPoint.to=websecure"
  - "--entrypoints.web.http.redirections.entryPoint.scheme=https"
  - "--certificatesResolvers.letsencrypt.acme.httpChallenge.entryPoint=web"
  - "--certificatesResolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
  - "--certificatesResolvers.letsencrypt.acme.email=gabriel@kyutai.org"
  - "--certificatesResolvers.letsencrypt.acme.httpChallenge=true"
  - "--log.level=TRACE"
```

Backend environment verbatim (`swarm-config.yaml:53-60`):

```yaml
environment:
  - "PORT=80"
  - "HF_TOKEN=${HUGGING_FACE_HUB_TOKEN}"
  - "HUGGING_FACE_HUB_TOKEN=${HUGGING_FACE_HUB_TOKEN}"
  - "LLM_BASE_URL=${LLM_BASE_URL}"
  - "LLM_API_KEY=${LLM_API_KEY}"
  - "LLM_MODEL_NAME=${LLM_MODEL_NAME}"
  - "ARC_ENCODER_URL=http://arc_encoder:80"
  - "STT_URL=wss://eu.api.gradium.ai/api/speech/asr"
  - "STT_API_KEY=${STT_API_KEY}"
```

GPU reservations verbatim (`swarm-config.yaml:78-82`):

```yaml
resources:
  reservations:
    generic_resources:
      - discrete_resource_spec:
          kind: gpu
          value: 1
```

Volumes (`swarm-config.yaml:63-67`, `swarm-config.yaml:130-136`): backend mounts `/scratch/models:/models`, `uv-cache`, `huggingface-cache`, `target-cache`, `registry-cache`; named volumes are `letsencrypt`, `portainer_data`, `uv-cache`, `huggingface-cache`, `target-cache`, `registry-cache`. Networks (`swarm-config.yaml:138-148`): `agent_network` and `default`, both `overlay`, `attachable: true`, `encrypted: "true"`.

**Covers:** `.gitignore`, `.pre-commit-config.yaml`, `deploy.sh`, `LICENSE-APACHE`, `LICENSE-MIT`, `requirements-dev.txt`, `swarm-config.yaml`
