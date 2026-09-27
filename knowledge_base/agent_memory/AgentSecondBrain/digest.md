> [[index|Wiki]] | [[summary|Summary]]
# smixs/agent-second-brain — Digest

## 1. [[wiki/01-overview|Overview]]
**In one sentence:** Agent Second Brain is an always-on Telegram-fronted second brain that files voice and text into a personal Obsidian vault via one long-lived interactive Claude Code session, with zero per-token API billing.
## Key points
- An always-on second brain you talk to: voice notes in Telegram become typed, linked knowledge in an Obsidian vault (README.md:13-15).
- Runs 24/7 on a cheap VPS plus an existing Claude subscription with no per-token API bills in the normal case (README.md:13-15).
- Since 2026-06-15 headless `claude -p` runs bill separately, so v3.0 drives one long-lived interactive Claude Code session and bans headless calls in the hot path via a CI guard (README.md:34).
- Telegram is the whole interface — no commands, categories, or separate app to open (README.md:87).
- The vault is the source of truth as plain markdown on the user's own server, readable forever without the agent (README.md:95).
- Memory is a typed autograph graph with Ebbinghaus decay across five tiers plus self-maintenance (MOCs, health score, link repair, dedup) (README.md:109, README.md:122-126).
- One persistent Claude Code session in tmux handles chat while scheduled jobs fire in a second isolated session, serialized by a cross-process lock with watchdog recovery (README.md:141-149).
- Flat cost is ~$25/mo (Claude Pro $20 + VPS ~$5 + Deepgram free tier), stable because the session is interactive rather than metered (README.md:157-164).

## 2. [[wiki/02-top-level-files|Top-level files]]
**In one sentence:** The repo root is a self-hosted product installer — example env, ignore rules, bootstrap/setup/upgrade shell scripts, and a Russian README storefront — that clones a private fork, collects secrets, and converges any install onto the v3.0 persistent-session systemd deployment.
## Key points
- `.env.example` declares all runtime configuration (bot token, Deepgram key, vault path, allow-list, timezone, model, cron toggles) with safe defaults, and `setup.sh` writes a `chmod 600` `.env` from it (`.env.example:10-31`, `setup.sh:634-653`).
- `.gitignore` keeps secrets and personal vault data out of git (`.env*`, `vault/daily/`, `vault/contacts/`, `vault/finances/`, and other vault subtrees) while explicitly noting `vault/.claude/` IS the product (`.gitignore:51-94`).
- `bootstrap.sh` is a curl-pipeable stub that refuses root, downloads `setup.sh` from `main` to a temp file via curl/wget, and `exec`s it so stdin works normally (`bootstrap.sh:122-127`, `bootstrap.sh:130-160`).
- `setup.sh` is the interactive first-time installer: validates tokens, checks Ubuntu/Debian, installs system deps/uv/Node/Claude CLI, clones the user's fork, writes `.env`, configures git push, gates on Claude login, then delegates to `upgrade.sh` (`setup.sh:371-384`, `setup.sh:434-444`, `setup.sh:729-735`).
- `upgrade.sh` is the idempotent single source of truth for install/migrate: pulls code, `uv sync`s, installs the `dbrain` CLI, migrates `d-brain-*` to `dbrain-*` systemd units, repairs runtime-dir privacy, guards against `claude -p`, and runs the first doctor check (`upgrade.sh:749-757`, `upgrade.sh:797-835`).
- `README.ru.md` is the Russian storefront: voice-in-Telegram to structured Obsidian knowledge, fixed ~$25/mo cost, fork-plus-two-keys-plus-one-curl-command quick start, and the persistent interactive tmux session architecture (`README.ru.md:172-174`, `README.ru.md:300-323`).
- Truncated in this chunk: `README.ru.md` (cut after the skills table, 1676 more characters not shown) and `setup.sh` (cut after the setup-complete banner, 1567 more characters not shown); no claims are made about the hidden tails.

## The system in five moves
1. Talk in Telegram and the bot captures voice, text, photos, and forwards with nothing silently dropped.
2. One long-lived interactive Claude Code session in tmux files it all into the plain-markdown Obsidian vault, avoiding metered headless calls.
3. The autograph memory layer types, links, decays, and self-maintains the graph across five tiers with MOCs and health scoring.
4. A second isolated session plus cron ticker, cross-process lock, watchdog, and daily doctor keep reminders and nightly processing from blocking chat.
5. Fork, two keys, and one curl command install it via bootstrap/setup/upgrade onto systemd units at a flat ~$25/mo, with secrets and vault data kept out of git.
