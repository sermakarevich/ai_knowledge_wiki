> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-level-files
**In one sentence:** The repo root defines how VoxForge is configured, built, and deployed via env templates, Docker assets, a production deploy script, and repo/security policy files.
## Key points
- Three env templates separate concerns: `.env.deploy.example` holds only `TOKEN` plus optional Cloudflare DNS keys (`.env.deploy.example:1-5`), `.env.example` holds the full local-dev defaults (`.env.example:1-115`), and `.env.production.example` holds the production template validated by `scripts/validate_production_env.py` (`.env.production.example:1-3`).
- Local development defaults to mock providers (`STT_PROVIDER`/`LLM_PROVIDER`/`TTS_PROVIDER=mock`) with the public demo enabled (`DEMO_ENABLED=true`), while production keeps mocks but switches to invite-only signup and container hostnames (`.env.example:31-36`, `.env.example:117-119`, `.env.production.example:23-30`, `.env.production.example:36-40`).
- `deploy.sh` is the single production entrypoint with subcommands `init|up|down|logs|backup|renew-cert|smoke|status`, enforcing `set -euo pipefail`, env-file loading, NGINX rendering, TLS bootstrap, and optional workers (`deploy.sh:1-12`, `deploy.sh:374`, `deploy.sh:566-579`).
- `docker-compose.prod.yml` defines the production stack (`voxforge-prod`) with `postgres` (pgvector/pg16), `redis`, `app`, `livekit-worker`, `knowledge-worker`, `prometheus`, `grafana`, `nginx`, and `certbot`, with resource limits and healthchecks (`.env.production.example:78-84`, `docker-compose.prod.yml:1-6`, `docker-compose.prod.yml:589-613`, `docker-compose.prod.yml:800-824`).
- `Dockerfile.dev` is a single-stage hot-reload image with dev dependencies while `Dockerfile.prod` is a two-stage builder/runtime image that runs as non-root `appuser` with a single uvicorn worker (`.env.example:1`, `Dockerfile.dev:857-858`, `Dockerfile.dev:878`, `Dockerfile.prod:891-903`, `Dockerfile.prod:913-929`, `Dockerfile.prod:936`).
- `SECURITY.md` declares `1.0.x` supported and `0.1.x` unsupported, requires private vulnerability reporting with 72-hour acknowledgement and 14-day remediation plan, and lists a secure-deployment checklist gated by `APP_ENV=production` (`.env.production.example:4`, `SECURITY.md:1-7`, `SECURITY.md:11-24`, `SECURITY.md:77-86`).
- `alembic.ini` is the generic single-database Alembic config (`script_location = alembic`, placeholder `sqlalchemy.url`), `.gitattributes` forces `text=auto eol=lf` with binary media/font types, and `.gitignore` excludes secrets (`.env`, `.env.production`, `.env.deploy`), venvs, caches, media, and generated deploy/prometheus outputs (`alembic.ini:11-18`, `.gitattributes:1-13`, `.gitignore:25-29`, `.gitignore:49-57`).
---
## Environment templates
Deployment-token template (`.env.deploy.example:1-5`):

```
# Copy to .env.deploy and fill in (never commit .env.deploy)
TOKEN=
# Optional Cloudflare DNS automation:
# CF_API_TOKEN=
# CF_ZONE_ID=
```

Local-dev template highlights (`.env.example:1-115`), verbatim keys:

| Area | Exact keys / values |
|------|---------------------|
| Core | `DATABASE_URL=postgresql+asyncpg://voxforge:voxforge@localhost:5432/voxforge` (`.env.example:1`), `REDIS_URL=redis://localhost:6379/0` (`.env.example:2`), `APP_ENV=development` (`.env.example:8`), `PUBLIC_BASE_URL=http://localhost:8000` (`.env.example:9`) |
| Demo | `DEMO_ENABLED=true`, `DEMO_ORG_ID=a0000000-0000-4000-8000-000000000001`, `DEMO_USER_ID=a0000000-0000-4000-8000-000000000002`, `DEMO_EMAIL=demo@voxforge.io`, `DEMO_PASSWORD_HINT=VoxForgeDemo!` (`.env.example:13-18`) |
| Rate limit | `RATE_LIMIT_ENABLED=true`, `RATE_LIMIT_MULTIPLIER=1.0`, `RATE_LIMIT_FAIL_CLOSED_CATEGORIES=auth,auth_login,demo,sessions_create,voice_ws,livekit,knowledge_upload,knowledge_reindex,knowledge_collections,replay,onboarding_sample,onboarding,api_keys` (`.env.example:20-22`); deprecated `RATE_LIMIT_PER_MINUTE=60`, `RATE_LIMIT_PATHS=/api/v1/auth,/api/v1/demo` (`.env.example:24-25`) |
| Auth | `JWT_SECRET_KEY=change-me-in-production`, `JWT_ALGORITHM=HS256`, `JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60`, `JWT_REFRESH_TOKEN_EXPIRE_DAYS=7`, `API_KEY_PREFIX=vxf_`, `API_KEY_HASH_PEPPER=change-me-in-production`, `AUTH_REQUIRED=true`, `REGISTRATION_ENABLED=true` (`.env.example:30-37`) |
| Memory/tools | `MEMORY_ENABLED=true`, `MEMORY_EMBEDDING_MODEL=text-embedding-3-small`, `MEMORY_EMBEDDING_DIMENSIONS=1536`, `MEMORY_MAX_RECENT_MESSAGES=10`, `MEMORY_SUMMARIZE_AFTER_MESSAGES=20`, `MEMORY_RETRIEVAL_TOP_K=5`, `MEMORY_SIMILARITY_THRESHOLD=0.65`, `TOOLS_ENABLED=true`, `TOOL_TIMEOUT_SECONDS=30`, `MAX_TOOL_ITERATIONS=5` (`.env.example:53-63`) |
| Knowledge/support | `SUPPORT_TOOLS_ENABLED=true`, `KNOWLEDGE_ENABLED=true`, `KNOWLEDGE_BASE_PROVIDER=mock`, `KNOWLEDGE_BLOB_STORE=filesystem`, `KNOWLEDGE_BLOB_PATH=/tmp/voxforge-knowledge`, `KNOWLEDGE_WORKER_ENABLED=false`, `EMBEDDING_PROVIDER=mock`, `TICKETING_PROVIDER=mock` (`.env.example:66-79`) |
| Providers | `STT_PROVIDER=mock`, `LLM_PROVIDER=mock`, `TTS_PROVIDER=mock` (`.env.example:99-101`); defaults `DEFAULT_LLM_MODEL=gpt-4.1-mini`, `DEFAULT_TTS_VOICE_ID=79a125e8-cd45-4c13-8a67-188112f4dd22` (`.env.example:27-28`) |
| Handoff/LiveKit | `HANDOFF_ENABLED=true`, `HANDOFF_AUTO_POLICY=true`, `HANDOFF_MIN_CONFIDENCE=0.55`, `HANDOFF_MAX_TOOL_FAILURES=2`, `HANDOFF_ESCALATE_ON_TOOL_FAILURE=true`, `HANDOFF_SESSION_TTL_SECONDS=14400`, `HANDOFF_ASSIGNMENT_PROVIDER=mock`, `LIVEKIT_AGENT_NAME=voxforge-voice`, `LIVEKIT_DISPATCH_ENABLED=true` (`.env.example:103-114`) |

Production template deltas (`.env.production.example:1-89`):

| Area | Production value |
|------|------------------|
| Env | `APP_ENV=production`, `PUBLIC_BASE_URL=https://your-domain.example`, `CERTBOT_EMAIL=admin@your-domain.example` (`.env.production.example:4-6`) |
| Secrets (empty, must fill) | `JWT_SECRET_KEY=`, `API_KEY_HASH_PEPPER=`, `HANDOFF_REPLAY_SIGNING_SECRET=`, `METRICS_BEARER_TOKEN=` (`.env.production.example:9-12`) |
| Signup/throttle | `REGISTRATION_ENABLED=false` (invite-only), `RATE_LIMIT_PER_MINUTE=30` (`.env.production.example:29-34`) |
| Data | `DATABASE_URL=postgresql+asyncpg://voxforge:CHANGE_ME@postgres:5432/voxforge`, `REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/0`, `KNOWLEDGE_BLOB_PATH=/data/knowledge`, `KNOWLEDGE_WORKER_ENABLED=true` (`.env.production.example:36-50`) |

## Git, ignore, and migration config
`.gitattributes:1` forces `* text=auto eol=lf`; `.gitattributes:3-13` marks `*.png`, `*.jpg`, `*.jpeg`, `*.gif`, `*.webp`, `*.ico`, `*.mp4`, `*.woff`, `*.woff2`, `*.ttf`, `*.eot` as `binary`.

`.gitignore` exclusions (`.gitignore:1-57`):

```
.env
.env.production
.env.deploy
.venv
deploy/backups/*.sql.gz
deploy/.droplet-ip
deploy/nginx/certs-ready
deploy/nginx/staged/
deploy/nginx/conf.d/voxforge.conf
deploy/nginx/conf.d/voxforge-http.conf
deploy/nginx/conf.d/voxforge-https.conf
infra/prometheus/prometheus.prod.yml
/data/knowledge/
```

`alembic.ini:13-18` (verbatim):

```
[alembic]
script_location = alembic
prepend_sys_path = .
version_path_separator = os
sqlalchemy.url = driver://user:pass@localhost/dbname
```

Logging within `alembic.ini:22-44` sets `logger_root` to `WARN`, `logger_sqlalchemy` to `WARN`, `logger_alembic` to `INFO`, with a `StreamHandler` on `sys.stderr` and format `%(levelname)-5.5s [%(name)s] %(message)s`.

## Deploy script (`deploy.sh`)
Usage header (`deploy.sh:3-12`):

```
#   ./deploy.sh init          # First-time: validate env, bootstrap TLS, start stack
#   ./deploy.sh up            # Build and start (after init)
#   ./deploy.sh down          # Stop stack
#   ./deploy.sh logs          # Tail logs
#   ./deploy.sh backup        # PostgreSQL backup to deploy/backups/
#   ./deploy.sh renew-cert    # Force certbot renewal
#   ./deploy.sh status        # Service health summary
```

Key functions and exact behavior:

| Function | What it does |
|----------|--------------|
| `require_env_file` | Generates from `scripts/setup-production-env.sh` when `$ENV_FILE` (default `$ROOT/.env.production`) is missing (`.env.production.example:1`, `deploy.sh:385-391`) |
| `load_env` | Sources `$ENV_FILE` with `set -a`, derives `DOMAIN` from `PUBLIC_BASE_URL`, rejects placeholder `your-domain.example` (`.env.production.example:6`, `deploy.sh:393-404`) |
| `validate_env` | Builds `app` and runs `python /app/scripts/validate_production_env.py` with `APP_ENV=production` in the container (`.env.production.example:3`, `deploy.sh:406-414`) |
| `render_nginx_config` | Renders `voxforge-http.conf.template` / `voxforge-https.conf.template` with `sed s/${DOMAIN}/$DOMAIN/g` into `staged/`; uses bootstrap conf until `deploy/nginx/certs-ready` exists (`.gitignore:52-55`, `deploy.sh:416-436`) |
| `bootstrap_tls` | Starts `postgres redis app nginx`, polls `http://127.0.0.1:8000/api/v1/health` 30x2s, runs `certbot certonly --webroot -w /var/www/certbot`, touches `certs-ready`, re-renders NGINX (`.gitignore:52`, `deploy.sh:471-501`) |
| `start_optional_workers` | Starts `livekit-worker` with `--profile livekit` when `LIVEKIT_URL` is set, `knowledge-worker` unless `KNOWLEDGE_ENABLED=false`, and `prometheus`+`grafana` with `--profile monitoring` when `METRICS_BEARER_TOKEN` is set (`.env.production.example:12`, `.env.production.example:64-73`, `deploy.sh:448-469`) |
| `cmd_status` | Prints `compose ps`, probes `/api/v1/health` and `/api/v1/ready` via the app container, and prints `Landing: https://$DOMAIN/`, `Demo: https://$DOMAIN/demo`, `API docs: https://$DOMAIN/api/v1/docs` (`deploy.sh:551-564`) |

## Compose stacks
Production stack name is `voxforge-prod` (`docker-compose.prod.yml:2`). Service table:

| Service | Image / build | Notes with citations |
|---------|---------------|----------------------|
| `postgres` | `pgvector/pgvector:pg16` | Requires `POSTGRES_PASSWORD`, mounts `postgres_data` + `./deploy/backups:/backups`, `pg_isready` healthcheck, default `0.30` CPU / `512M` (`docker-compose.prod.yml:589-613`) |
| `redis` | `redis:7-alpine` | `--save 60 1 --loglevel warning --requirepass`, `redis-cli ping` healthcheck, default `0.10` CPU / `128M` (`docker-compose.prod.yml:615-639`) |
| `app` | Built from `Dockerfile.prod` | Uses `.env.production`, overrides `DATABASE_URL`/`REDIS_URL` to service hostnames, `KNOWLEDGE_BLOB_PATH=/data/knowledge`, entrypoint `/app/scripts/docker-entrypoint.sh`, `uvicorn voxforge.main:app --host 0.0.0.0 --port 8000 --app-dir /app/src --workers 1`, `/api/v1/ready` healthcheck (`docker-compose.prod.yml:641-691`, `.env.production.example:50`) |
| `livekit-worker` | Built from `Dockerfile.prod`, `profiles: ["livekit"]` | Runs `python -m voxforge.infrastructure.livekit.worker`, waits on healthy `app` (`docker-compose.prod.yml:693-718`) |
| `knowledge-worker` | Built from `Dockerfile.prod` | Runs `python -m voxforge.infrastructure.knowledge.worker`, shares `knowledge_data:/data/knowledge`, waits on healthy `postgres`/`redis`/`app` (`docker-compose.prod.yml:720-751`, `.env.production.example:50`) |
| `prometheus` | `prom/prometheus:v2.54.1`, `profiles: ["monitoring"]` | Mounts generated `infra/prometheus/prometheus.prod.yml` read-only (git-ignored) (`.gitignore:56`, `docker-compose.prod.yml:753-771`) |
| `grafana` | `grafana/grafana:11.2.0`, `profiles: ["monitoring"]` | Binds `127.0.0.1:3000:3000`, `GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_ADMIN_PASSWORD:-voxforge}`, signups disabled (`docker-compose.prod.yml:773-798`, `.env.production.example:68-70`) |
| `nginx` | `nginx:1.27-alpine` | Publishes `80:80` + `443:443`, mounts `nginx.conf`, `conf.d`, certbot webroot/certs read-only, waits on healthy `app` (`docker-compose.prod.yml:800-823`) |
| `certbot` | `certbot/certbot:v2.11.0`, `profiles: ["certbot"]` | Loops `certbot renew --webroot -w /var/www/certbot` every `12h` (`docker-compose.prod.yml:825-834`) |

Smoke overlay (`docker-compose.smoke.yml:1-6`), verbatim:

```
# Smoke-test overlay — publish app port for local prod validation (no nginx/TLS).
services:
  app:
    ports:
      - "127.0.0.1:${SMOKE_APP_PORT:-8000}:8000"
```

## Docker images
`Dockerfile.dev:857-885` — `FROM python:3.12-slim`, installs `gcc libpq-dev curl`, copies `pyproject.toml README.md src alembic alembic.ini dashboard examples public scripts`, installs `.[dev,livekit]`, healthchecks `/api/v1/health`, runs uvicorn without `--workers`:

```
CMD ["uvicorn", "voxforge.main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "/app/src"]
```

`Dockerfile.prod:891-936` — two stages: `builder` installs `gcc libpq-dev` and `.[livekit]`; runtime installs `libpq5 curl`, creates `appuser (uid 10001)`, copies site-packages/bin plus `pyproject.toml README.md src alembic alembic.ini dashboard examples public scripts`, `chown`s to `appuser`, runs as `USER appuser` with `HEALTHCHECK --start-period=40s` and:

```
CMD ["uvicorn", "voxforge.main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "/app/src", "--workers", "1"]
```

## Security policy (`SECURITY.md`)
Supported-versions table (`SECURITY.md:3-7`):

| Version | Supported |
| ------- | ------------------ |
| 1.0.x | :white_check_mark: |
| 0.1.x | :x: |

Reporting (`SECURITY.md:11-24`): do not open public GitHub issues; use GitHub private vulnerability reporting or the owner contact; include description/impact, reproduction steps, affected versions/commits, suggested fix; acknowledgement within **72 hours**, remediation plan within **14 days**.

Practices (`SECURITY.md:26-33`): JWT + scoped API keys for REST and bearer-token WebSocket auth; production startup validation (`validate_production_settings`) blocking weak secrets, open metrics, mock providers when demo is disabled, and missing CORS/hosts; rate limiting on auth/voice/knowledge/replay categories; knowledge-upload size/extension/basename checks; signed handoff-replay links with configurable TTL (`HANDOFF_SESSION_TTL_SECONDS=14400` in `.env.example:112`); bearer/IP-gated metrics endpoint. NGINX TLS/HSTS/body-limit hardening lives in `docs/deployment/security.md` (`SECURITY.md:35`).

Checklist (`SECURITY.md:39-52`): set `APP_ENV=production` (`.env.production.example:4`); generate `JWT_SECRET_KEY`, `API_KEY_HASH_PEPPER`, `HANDOFF_REPLAY_SIGNING_SECRET`; set `TRUSTED_HOSTS`, `CORS_ORIGINS`, `PUBLIC_BASE_URL`; set `METRICS_BEARER_TOKEN`; use real `STT_PROVIDER`/`LLM_PROVIDER`/`TTS_PROVIDER` unless `DEMO_ENABLED=true`; run `./deploy.sh init`; validate with `python scripts/validate_production_env.py`.

**Covers:** `.env.deploy.example`, `.env.example`, `.env.production.example`, `.gitattributes`, `.gitignore`, `alembic.ini`, `deploy.sh`, `docker-compose.prod.yml`, `docker-compose.smoke.yml`, `Dockerfile.dev`, `Dockerfile.prod`, `SECURITY.md`
