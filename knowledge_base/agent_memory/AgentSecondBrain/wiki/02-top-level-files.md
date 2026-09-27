> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-level files
**In one sentence:** The repo root is a self-hosted product installer — example env, ignore rules, bootstrap/setup/upgrade shell scripts, and a Russian README storefront — that clones a private fork, collects secrets, and converges any install onto the v3.0 persistent-session systemd deployment.
## Key points
- `.env.example` declares all runtime configuration (bot token, Deepgram key, vault path, allow-list, timezone, model, cron toggles) with safe defaults, and `setup.sh` writes a `chmod 600` `.env` from it (`.env.example:10-31`, `setup.sh:634-653`).
- `.gitignore` keeps secrets and personal vault data out of git (`.env*`, `vault/daily/`, `vault/contacts/`, `vault/finances/`, and other vault subtrees) while explicitly noting `vault/.claude/` IS the product (`.gitignore:51-94`).
- `bootstrap.sh` is a curl-pipeable stub that refuses root, downloads `setup.sh` from `main` to a temp file via curl/wget, and `exec`s it so stdin works normally (`bootstrap.sh:122-127`, `bootstrap.sh:130-160`).
- `setup.sh` is the interactive first-time installer: validates tokens, checks Ubuntu/Debian, installs system deps/uv/Node/Claude CLI, clones the user's fork, writes `.env`, configures git push, gates on Claude login, then delegates to `upgrade.sh` (`setup.sh:371-384`, `setup.sh:434-444`, `setup.sh:729-735`).
- `upgrade.sh` is the idempotent single source of truth for install/migrate: pulls code, `uv sync`s, installs the `dbrain` CLI, migrates `d-brain-*` to `dbrain-*` systemd units, repairs runtime-dir privacy, guards against `claude -p`, and runs the first doctor check (`upgrade.sh:749-757`, `upgrade.sh:797-835`).
- `README.ru.md` is the Russian storefront: voice-in-Telegram to structured Obsidian knowledge, fixed ~$25/mo cost, fork-plus-two-keys-plus-one-curl-command quick start, and the persistent interactive tmux session architecture (`README.ru.md:172-174`, `README.ru.md:300-323`).
- Truncated in this chunk: `README.ru.md` (cut after the skills table, 1676 more characters not shown) and `setup.sh` (cut after the setup-complete banner, 1567 more characters not shown); no claims are made about the hidden tails.
---
## `.env.example` — runtime configuration
Verbatim core block (`.env.example:10-31`):
```
TELEGRAM_BOT_TOKEN=
DEEPGRAM_API_KEY=
VAULT_PATH=./vault
ALLOWED_USER_IDS=[123456789]
TZ=UTC
CLAUDE_MODEL=
CRON_ENABLED=true
```
Config table (`.env.example:10-45`):

| Variable | Meaning / default |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Bot API token from @BotFather |
| `DEEPGRAM_API_KEY` | Key for voice transcription |
| `VAULT_PATH` | Obsidian vault directory (`./vault`) |
| `ALLOWED_USER_IDS` | JSON array of allowed Telegram IDs; empty = allow all; FIRST id gets health alerts / daily reports |
| `TZ` | Timezone for systemd timers and reports (e.g. `Asia/Tashkent`), default `UTC` |
| `CLAUDE_MODEL` | Model for persistent session; empty = Claude Code default (Opus); `"sonnet"` reduces weekly-limit pressure |
| `CRON_ENABLED` | `true` by default; `false` turns the ticker off |
| `RUNTIME_DIR` | Advanced, commented out; session locks/logs and cron state, must be a LOCAL fs (`~/.dbrain`) |
| `BRAIN_SESSION_NAME` | Advanced, commented out; tmux session name, empty = generated per install |
| `ALLOW_ALL_USERS` | Advanced, commented out; `false` — allow-everyone is a security risk |
| `CRON_TICK_SECONDS` / `CRON_JOB_TIMEOUT` / `CRON_MAX_CONSECUTIVE_ERRORS` / `CRON_RETRY_SECONDS` | Advanced cron tuning: ticker interval / per-job timeout / failures before auto-disable / retry delay for a failed one-shot |

`setup.sh:create_env_file` writes exactly the non-advanced subset with `chmod 600` (`setup.sh:634-653`):
```
TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN
DEEPGRAM_API_KEY=$DEEPGRAM_API_KEY
VAULT_PATH=./vault
ALLOWED_USER_IDS=[$TELEGRAM_USER_ID]
TZ=$USER_TZ
```

## `.gitignore` — what never gets committed
Secrets and runtimes (`.gitignore:51-66`): `.env`, `.env.local`, `.env.*.local`, Python (`__pycache__/`, `*.py[cod]`, `.venv/`), `node_modules/`. Personal vault data, verbatim (`.gitignore:79-87`):
```
vault/daily/
vault/contacts/
vault/finances/
vault/attachments/
vault/.session/
vault/.graph/
vault/business/
vault/projects/
vault/thoughts/
```
Local agent-skill installs are anchored to the repo root and excluded — `/.agents/`, `/.claude/`, `/skills-lock.json` — with the explicit comment that `vault/.claude/` IS the product (`.gitignore:89-94`).

## `bootstrap.sh` — curl-pipeable entry point
Usage, verbatim (`.gitignore` no; `bootstrap.sh:106-107`):
```bash
curl -fsSL https://raw.githubusercontent.com/smixs/agent-second-brain/main/bootstrap.sh | bash
```
Behavior: refuses `EUID == 0` with a create-a-user hint (`bootstrap.sh:122-127`); always downloads `SETUP_URL="https://raw.githubusercontent.com/smixs/agent-second-brain/main/setup.sh"` (`bootstrap.sh:130`); prefers `curl`, falls back to `wget`, fails if neither exists or the download is empty (`bootstrap.sh:138-152`); then `chmod +x` and `exec bash "$TEMP_SCRIPT"` so the installer runs properly with working stdin instead of via pipe (`bootstrap.sh:157-160`).

## `README.ru.md` — Russian storefront and architecture brief
Pitch, verbatim (`.env.example` no; `README.ru.md:172-174`): always-on second brain you talk to — voice in Telegram becomes structured, linked knowledge in the Obsidian vault; 24/7 on a $5 VPS plus a normal Claude subscription, zero API-token bills. Billing change callout: since 15 June 2026 headless `claude -p` runs bill a separate Agent SDK credit, so v3.0 keeps one long-lived *interactive* Claude Code session and CI-guards against headless calls in the working loop (`README.ru.md:192`). Start-here router (`README.ru.md:198-203`): what-it-is vs. one-command fresh VPS install vs. v1/v2 upgrade vs. `docs/setup-guide.ru.md` beginner guide vs. standalone `autograph` engine vs. persistent-session explainer. Architecture, verbatim (`README.ru.md:285-292`):
```
Telegram ──▶ бот (aiogram) ──▶ постоянная сессия Claude Code (tmux)
                 │                       │
                 │                       ├──▶ Obsidian vault (обычный markdown)
                 │                       └──▶ autograph: граф · угасание · MOC
                 ├──▶ cron-тикер ──▶ вторая изолированная сессия (напоминания не блокируют чат)
                 └──▶ watchdog + ежедневный doctor (самолечение, 🟢/🔴 отчёт)
```
Cost table (`README.ru.md:300-305`): Claude Pro $20/mo + VPS ~$5/mo + Deepgram free tier ($200 credit) = ~$25/mo fixed. Quick start is three steps — private fork, two keys (BotFather token, Deepgram key) plus Telegram ID, then one curl of `bootstrap.sh` against `YOUR_USERNAME` — after which the installer asks for tokens, walks through Claude Code browser login, installs `dbrain-*` systemd services, and health-checks (`README.ru.md:313-323`). Upgrade from v1/v2 is `git pull && bash upgrade.sh`, with a `migrate-doctor` skill fallback for broken migrations (`README.ru.md:333-340`). Vault layout shown (`README.ru.md:344-358`): `daily/`, `goals/`, `business/crm/`, `business/network/`, `projects/`, `thoughts/ideas|learnings|reflections/`, `MOC/`, `MEMORY.md`. Note: the skills table at the end of the visible excerpt is cut off mid-row (`dbrain-processor` / "Классифицирует запис…"), so its full contents are not summarized here.

## `setup.sh` — interactive first-time installer
Header contract (`setup.sh:371-384`): interactive first-time setup that installs dependencies, clones the fork, asks for tokens, then delegates heavy lifting (systemd units, brain session, health check) to `upgrade.sh` — one source of truth, no drift. Validators (`setup.sh:434-444`): Telegram token must match `^[0-9]+:[A-Za-z0-9_-]+$`; Telegram ID numeric and > 0; Deepgram key alphanumeric and ≥ 20 chars. Steps: refuse root (`setup.sh:450-457`); warn unless Ubuntu/Debian (`setup.sh:459-470`); `apt-get install git curl wget tmux` (`setup.sh:480-488`); install `uv` via `astral.sh` and persist `~/.local/bin` on PATH (`setup.sh:489-504`); Node.js 20 via NodeSource, reusing existing Node ≥ 18 (`setup.sh:506-520`); global `@anthropic-ai/claude-code` via npm (`setup.sh:522-531`); clone `https://github.com/$GITHUB_USER/agent-second-brain.git` into `$HOME/projects/agent-second-brain` and record `.github_user` (`setup.sh:537-574`); interactively collect and validate the three secrets plus timezone defaulting to `UTC` (`setup.sh:576-619`); write `chmod 600` `.env` (`setup.sh:621-654`); set `user.name`/`user.email` for the bot and optionally re-point `origin` to a fine-grained PAT URL after `chmod 600 .git/config` (`setup.sh:656-697`); gate on `claude auth status --json` showing `"loggedIn": true`, with a second-terminal login loop or `skip` (`setup.sh:699-727`); finally `bash "$PROJECT_DIR/upgrade.sh"` (`setup.sh:729-735`). Note: the outro/banner tail after that point is truncated in this chunk and not summarized here.

## `upgrade.sh` — idempotent migrate-and-converge
Contract, verbatim header (`upgrade.sh:749-757`): upgrade an existing install (v1/v2) to v3.0 persistent interactive-session architecture in one `bash upgrade.sh` command; installs tmux+deps, pulls code, migrates systemd units from `d-brain-*` to `dbrain-*`, runs a first health check; idempotent, safe to re-run. Eight numbered stages (`upgrade.sh:770-835`): 1/8 system deps (`tmux`, `zram-tools`); 2/8 `git pull --ff-only`; 3/8 `uv sync`; 4/8 runtime dir plus project pointer (`$RUNTIME_DIR/project.path`, default `$HOME/.dbrain`); 5/8 install `bin/dbrain` to `/usr/local/bin/dbrain` or fallback `~/.local/bin/dbrain`; 6/8 migrate user units — disable/remove legacy `d-brain-*`, retire removed `dbrain-weekly.*`, template `deploy/dbrain-*.service|timer` with the real path, `daemon-reload`, `enable-linger`, enable `dbrain-bot.service dbrain-watchdog.service dbrain-process.timer dbrain-doctor.timer`, restart services (restart, not just `enable --now`, with `KillMode=process` preserving the brain) and start timers; then `chmod 700/600` privacy repair on the runtime dir; 7/8 `scripts/check-no-claude-p.sh` guard; 8/8 first health check via `uv run python -m d_brain.services.doctor`.

**Covers:** `.env.example`, `.gitignore`, `bootstrap.sh`, `README.ru.md` (visible portion only; tail after skills-table head truncated, 1676 more characters), `setup.sh` (visible portion only; tail after setup-complete banner truncated, 1567 more characters), `upgrade.sh`
