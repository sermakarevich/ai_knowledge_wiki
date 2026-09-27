# Technical Analysis: smixs/agent-second-brain

**Repository:** https://github.com/smixs/agent-second-brain
**Version analyzed:** unknown
**Date:** 2026-09-26
**Wiki:** [[index]]

## 1. Overview

Problem space: personal productivity systems fail because maintenance exceeds value — voice memos are never re-listened, ideas drown in chat history, markdown vaults become unnavigable after a month (README.md:53). A second failure is privacy: routing notes, clients, and goals through third-party SaaS is unacceptable to the author (README.md:55). A third is cost unpredictability after the 2026-06-15 billing change where headless `claude -p` runs bill a separate Agent SDK credit (README.md:34).

How the repo addresses it: an always-on Telegram-fronted second brain where voice and text become typed, linked knowledge in a self-hosted Obsidian vault via one long-lived interactive Claude Code session in tmux, with no per-token API billing in the normal case (README.md:13-15, README.md:34). Capture requires no commands or categories; the agent classifies entries, writes vault cards, manages reminders and nightly consolidation, and maintains the graph itself (README.md:87, README.md:107-114, README.md:229). The vault remains plain markdown on the user's server, readable without the agent (README.md:95).

Primary user: an individual knowledge worker with a Claude Pro/Max subscription and a cheap VPS who wants voice-first capture into a private Obsidian vault without operating a SaaS or paying metered tokens.

## 2. High-Level Architecture

```
Telegram ──► bot (aiogram) ──► persistent Claude Code session (tmux pane)
                 │                         │
                 │                         ├──► Obsidian vault (plain markdown)
                 │                         └──► autograph: graph · decay · MOC
                 ├──► cron ticker ──► second isolated session
                 └──► watchdog + daily doctor
```

Adapted verbatim from README.md:140-147 and README.ru.md:285-292; connectors use ─ ► │ ├── └── per source diagram.

Data-flow narrative:

1. Capture: Telegram delivers voice, text, photos, documents, videos, forwarded posts, or albums to the bot. Voice audio is sent to Deepgram for transcription; nothing sent is silently dropped (README.md:107-114, README.md:151).
2. Dispatch: the aiogram bot process does not spawn `claude` per message. It types prompts into one long-lived interactive Claude Code session held alive in a tmux pane (README.md:149).
3. Filing: the persistent session writes plain-markdown cards into the vault layout (`daily/`, `goals/`, `business/crm/`, `projects/`, `thoughts/`, `MOC/`, `MEMORY.md`) and updates the autograph graph, links, and MOC indexes (README.md:122-126, README.md:207-221).
4. Scheduling: a cron ticker fires one-shots, intervals, and cron expressions in a second isolated session so reminders never block chat; plain-language requests such as "remind me Friday at 3pm" become jobs (README.md:107-114, README.md:140-147).
5. Supervision: a cross-process lock serializes the two sessions; a watchdog restarts wedged sessions and a daily doctor emits a canary report, with broken jobs self-disabling and notifying (README.md:107-114, README.md:149).
6. Retrieval: later questions ("what did I write about the marketing project last week?") are answered from the vault and graph, with quotes, links, and card promotion on access (README.md:61-85, README.md:128-134).

Persistent state lives in: the Obsidian vault directory itself (`VAULT_PATH`, default `./vault` per .env.example:10-31), the runtime directory for session locks/logs and cron state (default `~/.dbrain`, must be a local filesystem per .env.example:10-45), and systemd user units plus `MEMORY.md` long-term memory (README.md:207-221, upgrade.sh:770-835).

## 3. The Autograph Memory Graph

Central concept: the vault is not a log but a typed, decaying knowledge graph managed by the `autograph` engine, shipped as a skill and usable standalone on any vault (README.md:120).

Representation: every card carries a type, a retrieval description, tags, and status, governed by one `schema.json` (README.md:122-126). Storage is markdown with wiki-links; retrieval strength follows `1 + ln(access_count)` so each touch slows forgetting (README.md:122-126). Five tiers control visibility from always-in-context to near-archived with random recall for creative collisions (README.md:128-134).

Named kinds/types with file:line:

- Card types `note`, `contact`, `project`, `CRM` (README.md:122-126).
- Tier `core` — always in context: current projects, active clients, key goals (README.md:128-134).
- Tier `active` — checked regularly: recent ideas, ongoing threads (README.md:128-134).
- Tier `warm` — found when you search (README.md:128-134).
- Tier `cold` — surfaces only in deep searches (README.md:128-134).
- Tier `archive` — almost gone, randomly recalled (README.md:128-134).
- Maintenance outputs: orphan detection, broken-link repair, dedup into `.trash/`, MOC generation, 100-point health score (README.md:122-126).

Key queries (verbatim interaction snippets from README.md:61-85):

```
You:  what did I write about the marketing project last week?
Bot:  *finds the entries, quotes them, links the cards*
You:  turn the second idea into a project note with next steps
Bot:  *creates the note, links it to the client and this week's goals*
```

```
You:  *forwards a post, drops a photo of a whiteboard, sends a PDF*
Bot:  *reads them itself — files the takeaways into the graph, answers what it saved*
```

## 4. LLM / External Service Integration

Providers: Anthropic Claude Code through the user's flat-rate subscription (interactive session, not API tokens); Deepgram for voice transcription; Telegram Bot API via aiogram; VPS host and systemd for runtime (README.md:13-15, README.md:107-114, README.md:140-147).

Required vs optional calls: text understanding and filing go through the persistent interactive Claude session and are required for all operation; voice messages additionally require a Deepgram transcription call; Telegram delivery is required as the sole interface; nightly classification, MOC rebuild, and doctor reports run inside the same session/scheduler split rather than as separate LLM vendors (README.md:149, README.md:151, README.md:107-114).

Env vars (from .env.example:10-45): `TELEGRAM_BOT_TOKEN` (from @BotFather, required), `DEEPGRAM_API_KEY` (required for voice), `VAULT_PATH` (default `./vault`), `ALLOWED_USER_IDS` (JSON array; empty means allow all; first id gets health alerts and daily reports), `TZ` (default `UTC`), `CLAUDE_MODEL` (empty means Claude Code default Opus; `sonnet` reduces weekly-limit pressure), `CRON_ENABLED` (default `true`), plus advanced `RUNTIME_DIR`, `BRAIN_SESSION_NAME`, `ALLOW_ALL_USERS`, `CRON_TICK_SECONDS`, `CRON_JOB_TIMEOUT`, `CRON_MAX_CONSECUTIVE_ERRORS`, `CRON_RETRY_SECONDS`. Token formats are validated in setup.sh:434-444 (Telegram `^[0-9]+:[A-Za-z0-9_-]+$`, numeric Telegram ID, Deepgram key alphanumeric and >= 20 chars).

## 5. The Capture-to-Vault Pipeline

Primary workflow: voice or text in Telegram becomes transcribed input, a typed prompt into the persistent session, a vault card plus graph update, and an acknowledgement plus any scheduled follow-up.

1. Provision entrypoint: user pipes `bootstrap.sh` via curl; the stub refuses root, downloads `setup.sh` from `main` with curl or wget fallback, then `exec`s it so stdin works (bootstrap.sh:122-127, bootstrap.sh:130-160).
2. Interactive collection: `setup.sh` refuses root, warns unless Ubuntu/Debian, installs `git curl wget tmux`, installs `uv`, Node.js 20, and `@anthropic-ai/claude-code`, clones `https://github.com/$GITHUB_USER/agent-second-brain.git`, collects and validates tokens/timezone, writes `chmod 600` `.env`, configures git identity and optional PAT remote, gates on `claude auth status` showing logged-in, then delegates to `upgrade.sh` (setup.sh:450-457, setup.sh:459-470, setup.sh:480-531, setup.sh:537-574, setup.sh:576-619, setup.sh:621-654, setup.sh:656-697, setup.sh:699-727, setup.sh:729-735).
3. Converge: `upgrade.sh` performs eight stages — system deps, `git pull --ff-only`, `uv sync`, runtime-dir pointer, `bin/dbrain` install, migration of `d-brain-*` to `dbrain-*` systemd units with daemon-reload and restarts, privacy repair, `scripts/check-no-claude-p.sh` guard, first doctor check via `uv run python -m d_brain.services.doctor` (upgrade.sh:749-757, upgrade.sh:770-835).
4. Capture and transcribe: Telegram update arrives at the aiogram bot; audio goes to Deepgram, text stays in-session; filed takeaways are produced rather than raw dumps (README.md:107-114, README.md:151).
5. File via persistent session: the bot injects the prompt into the tmux-held interactive session under a cross-process lock; the session writes `daily/` stream entries, typed cards (`business/crm/`, `projects/`, `thoughts/`), links, and `MEMORY.md` updates (README.md:149, README.md:207-221).
6. Schedule and remind: plain-language time expressions become cron one-shots/intervals/expressions executed in the second isolated session; nightly 21:00 local-time job classifies the day, rebuilds the graph, and sends a daily report (README.md:107-114).
7. Supervise: watchdog plus daily doctor monitor liveness; wedged sessions restart; failing jobs auto-disable with notification (README.md:107-114, README.md:149).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `bootstrap.sh` | ~62 | Curl-pipeable entrypoint; refuses root, fetches setup.sh, execs it |
| `setup.sh` | ~430 | Interactive first-time installer; validates secrets, installs deps, writes .env, gates on Claude login, calls upgrade.sh |
| `upgrade.sh` | ~91 | Idempotent migrate-and-converge; syncs code/deps, migrates systemd units, guards headless calls, runs doctor |
| `.env.example` | ~37 | Declares all runtime configuration with defaults and advanced cron tuning |
| `.gitignore` | ~43 | Excludes secrets, runtimes, and personal vault subtrees; marks vault/.claude as product |
| `README.ru.md` | ~231 | Russian storefront, architecture brief, cost table, quick start and upgrade |
| `bin/dbrain` | ~78 | Installed CLI wrapper for status/logs/attach/doctor operations |
| `deploy/dbrain-*.service\|timer` | ~180 across 9 files | Systemd unit templates for bot, watchdog, process and doctor timers |
| `scripts/check-no-claude-p.sh` | part of ~243 across 4 files in scripts/ | CI/install guard banning headless claude -p in hot path |
| `vault/.claude/skills/` | product skills dir | Agent abilities; dbrain-processor classifies entries and writes cards/reports |
| `vault/goals/` | user-filled | Vision to yearly/monthly/weekly goal hierarchy |
| `vault/daily/` | git-ignored stream | Raw daily voice/text/attachment intake |
| `vault/MOC/` | auto-generated | Maps of Content indexes rebuilt by maintenance |
| `vault/MEMORY.md` | long-term memory | Agent persistent memory updated by nightly processing |
| `mcp-config.json` | referenced config | MCP server registrations extending Claude Code abilities |
| `vault/.claude/skills/dbrain-processor/references/about.md` | persona file | User persona filled during setup to steer filing behavior |

Structural importance ordered from installer to runtime to vault; line counts for top-level entries per wiki top-level layout except where wiki gives only functional description.

## 7. Dependencies

| Package | Version constraint | Purpose |
|---|---|---|
| Claude Pro/Max subscription | $20/mo flat (per README.md:157-162) | Interactive Claude Code session; avoids metered tokens |
| VPS | ~$5/mo (per README.md:157-162) | 24/7 host for bot, tmux sessions, vault, systemd units |
| Deepgram | free tier, $200 credit (per README.md:157-162); key via DEEPGRAM_API_KEY | Voice transcription |
| aiogram (bot) | version constraint not stated in wiki excerpts | Telegram interface |
| tmux | version constraint not stated in wiki excerpts; installed by setup.sh:480-488 and upgrade.sh:770-835 | Holds persistent and isolated sessions alive |
| uv + Python deps | version constraint not stated in wiki excerpts | Python packaging and `uv sync` install |
| Node.js 20 | Node >= 18 reused, 20 installed (per setup.sh:506-520) | Runtime for Claude CLI |
| @anthropic-ai/claude-code | version constraint not stated in wiki excerpts; installed via npm (per setup.sh:522-531) | Interactive agent engine driven via tmux |
| git, curl, wget | version constraint not stated in wiki excerpts; installed via apt (per setup.sh:480-488) | Clone, download, update |
| systemd user units | version constraint not stated in wiki excerpts | Runs dbrain-bot, watchdog, process and doctor timers |
| zram-tools | version constraint not stated in wiki excerpts (per upgrade.sh:770-835) | System dependency on small VPS |

Wiki excerpts do not reproduce pyproject.toml constraint strings; only the installer-level packages and flat-cost services above are citable from the two component pages.

## 8. CLI / Usage Surface

Entry points: `curl .../bootstrap.sh | bash` for fresh VPS install (bootstrap.sh:106-107); `bash upgrade.sh` after `git pull` for idempotent upgrade and repair (README.md:196-199); Telegram message to the bot as the sole daily interface with no commands to memorize (README.md:87).

Commands:

| Command | Effect |
|---|---|
| `curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/agent-second-brain/main/bootstrap.sh \| bash` | Fresh install interview, Claude login, systemd install, health check (README.md:178-180, README.md:182) |
| `cd agent-second-brain && git pull && bash upgrade.sh` | Migrate units, install missing pieces, repair permissions, self health-check (README.md:194) |
| `dbrain status` | Show service/session health (per installer description README.md:187) |
| `dbrain logs` | Tail bot and job logs |
| `dbrain attach` | Attach to the persistent tmux session |
| `dbrain doctor` | Run first/canary health check (`uv run python -m d_brain.services.doctor` per upgrade.sh:770-835) |

Env-var and config tables: see Section 4 for `.env` vars. `setup.sh:create_env_file` writes exactly the non-advanced subset (`TELEGRAM_BOT_TOKEN`, `DEEPGRAM_API_KEY`, `VAULT_PATH=./vault`, `ALLOWED_USER_IDS`, `TZ`) with `chmod 600` (setup.sh:634-653). Git remote user is recorded in `.github_user` and PAT remote rewriting hardens `.git/config` to 600 (setup.sh:537-574, setup.sh:656-697). Vault content is configured by filling `vault/goals/` and the persona file before install (README.md:172).

## 9. Extensibility Points

- New agent abilities: add a skill directory under `vault/.claude/skills/`; the running Claude Code session picks it up as PKM capability (README.md:107-114).
- External tool access: register an MCP server in `mcp-config.json`; the persistent session can then call it during filing and retrieval (README.md:107-114).
- Memory-only reuse: extract the `autograph` skill/standalone engine for another Obsidian vault without the Telegram bot (README.md:120).
- Scheduling: express routines in plain language to the bot ("every weekday at 18:30 check my inbox folder"); no external task manager or code change needed (README.md:107-114).
- Install and migration behavior: edit `upgrade.sh` as the single source of truth and `scripts/check-no-claude-p.sh` to extend the headless-call guard; `bootstrap.sh`/`setup.sh` remain thin question-askers by design (setup.sh:371-384, upgrade.sh:749-757).
- Operations: extend `bin/dbrain` and `deploy/dbrain-*.service|timer` templates to add services, timers, or diagnostics (upgrade.sh:770-835).

## 10. Limitations and Gotchas

- **Subscription-coupled, not API-portable.** Continuous operation depends on driving one interactive Claude Code session the way a human would; headless `claude -p` in the hot path is banned by CI guard, so reuse outside a Claude subscription model requires rework (README.md:34, README.md:99).
- **Single-admin trust model.** `ALLOWED_USER_IDS` empty means allow-all, flagged as a security risk; the first listed id alone receives health alerts and daily reports, so multi-user or team use is outside the design (per .env.example:10-45).
- **Local-filesystem and distro assumptions.** `RUNTIME_DIR` must be a local filesystem and setup warns unless Ubuntu/Debian; non-Linux or networked-home installs diverge from installer expectations (per .env.example:10-45, setup.sh:459-470).
- **Private-fork discipline required.** The fork must be made private before filling `vault/goals/` and persona, and `.gitignore` exclusions (`vault/daily/`, `contacts/`, `finances/`, `business/`, `projects/`, `thoughts/`) must hold; misconfiguration leaks personal vault data via git (README.md:172, .gitignore:79-87).
- **Source truncation in available wiki.** The Skills table is cut mid-entry after `dbrain-processor` and macro-component mapping is incomplete, so claims about additional skills beyond classification, card writing, and daily reports cannot be grounded from these two pages (per 01-overview.md:129-131, 02-top-level-files.md:11).

## 11. How It Compares to Alternatives

- Obsidian plus capture plugins (e.g. voice-recorder and templating community plugins): stays local markdown but leaves classification, linking, MOC building, and reminders manual; this repo automates filing and maintenance through the persistent agent.
- Mem0 / Letta-style memory layers: provide API-backed recall and decay abstractions for developers, but require integration work and metered calls; this repo ships a vault-native typed graph with Ebbinghaus tiers as an end-user product on a flat subscription.
- ChatGPT memory / Claude Projects: zero-ops hosted memory inside a chat vendor with export friction; this repo keeps the vault as portable markdown on the user's server with explicit privacy split (audio to Deepgram, text via subscription, rest local).
- Self-hosted Telegram AI bots (generic aiogram + LLM-API polling templates): typically spawn a stateless completion per message with per-token billing; this repo holds one interactive session in tmux with a lock, isolated cron session, and watchdog for flat-cost 24/7 operation.

Positioning: the differentiating choice is persistent interactive session plus vault-native decaying graph for one owner, trading multi-user generality and vendor portability for flat cost, auditability, and data ownership.

## Appendix: Selected Code Snippets

1. Runtime configuration core block (`.env.example:10-31`):

```
TELEGRAM_BOT_TOKEN=
DEEPGRAM_API_KEY=
VAULT_PATH=./vault
ALLOWED_USER_IDS=[123456789]
TZ=UTC
CLAUDE_MODEL=
CRON_ENABLED=true
```

2. Architecture dataflow (`README.md:140-147`):

```
Telegram ──▶ bot (aiogram) ──▶ persistent Claude Code session (tmux pane)
                 │                       │
                 │                       ├──▶ Obsidian vault (plain markdown)
                 │                       └──▶ autograph: graph · decay · MOC
                 ├──▶ cron ticker ──▶ second isolated session (reminders never block chat)
                 └──▶ watchdog + daily doctor (self-healing, 🟢/🔴 report)
```

3. Vault layout (`README.md:207-221`):

```
vault/
├── daily/              # Your raw daily stream (voice, text, attachments)
├── goals/              # Vision → yearly → monthly → weekly
├── business/
│   ├── crm/            # Client cards
│   └── network/        # Professional contacts
├── projects/           # Active work, leads, pipeline
├── thoughts/
│   ├── ideas/          # Ideas and brainstorms
│   ├── learnings/      # Lessons learned
│   └── reflections/    # Personal reflections
├── MOC/                # Maps of Content (auto-generated)
└── MEMORY.md           # The agent's long-term memory
```

4. Fresh-install and upgrade commands (`README.md:178-180`, `README.md:196-199`):

```bash
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/agent-second-brain/main/bootstrap.sh | bash
```

```bash
ssh your-server
cd agent-second-brain && git pull && bash upgrade.sh
```
