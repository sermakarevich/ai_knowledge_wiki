# smixs/agent-second-brain
Source: https://github.com/smixs/agent-second-brain
Kind: repo
Fetched: 2026-09-26T13:42:49.482645+00:00
Tool: git-clone
Research-Target: /Users/sergii/.ai/knowledge/research_topics/agent_memory/research/AgentBrain
Topic: agent_memory

# smixs/agent-second-brain

Commit: 7828ed62cf76aae87bee7f2660468ab88495cf3d

## README

<p align="center">
  <img alt="Agent Second Brain" src="assets/hero.webp" />
</p>

<h1 align="center">Agent Second Brain</h1>

<p align="center"><b>An always-on second brain you talk to.</b><br/>
Voice note in Telegram → typed, linked knowledge in your Obsidian vault.<br/>
Runs 24/7 on a $5 VPS and the Claude subscription you already pay for — zero per-token API bills.</p>

<p align="center">
  <a href="README.ru.md">🇷🇺 Русский</a> •
  <a href="docs/setup-guide.ru.md">Полная инструкция</a> •
  <a href="docs/vps-setup.md">VPS guide</a> •
  <a href="https://github.com/smixs/autograph">autograph engine</a>
</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-blue.svg"></a>
  <img alt="Python 3.12+" src="https://img.shields.io/badge/python-3.12+-blue.svg">
  <a href="https://github.com/smixs/agent-second-brain/stargazers"><img alt="Stars" src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.github.com%2Frepos%2Fsmixs%2Fagent-second-brain&query=%24.stargazers_count&label=stars&logo=github&color=blue"></a>
  <a href="https://github.com/smixs/agent-second-brain/forks"><img alt="Forks" src="https://img.shields.io/github/forks/smixs/agent-second-brain?style=flat&logo=github"></a>
</p>

---

> [!IMPORTANT]
> **Since June 15, 2026, headless `claude -p` runs bill against a separate paid Agent SDK credit.** v3.0 sidesteps that completely: it drives one long-lived *interactive* Claude Code session — the same thing you run in a terminal, used exactly the way the subscription is meant to be used. No headless calls in the hot path (enforced by a CI guard), no per-request billing, no surprise invoice.



## Start here

| You want to… | Go to |
|---|---|
| Understand what this thing is | [Why I built this](#why-i-built-this) |
| Install it on a fresh VPS in one command | [Quick start](#quick-start) |
| Upgrade an existing v1 / v2 install | [Upgrading](#upgrading-from-v1--v2) |
| Пошаговая инструкция на русском, для новичков | [docs/setup-guide.ru.md](docs/setup-guide.ru.md) |
| Just want the memory engine for your own vault | [autograph →](https://github.com/smixs/autograph) |
| See how the persistent-session trick works | [How it works](#how-it-works) |



## Why I built this

Every productivity system dies the same way. You set it up on a Sunday, use it for two weeks, then slowly stop — because maintaining the system is more work than the work itself. Voice memos you never re-listen to. Ideas that drown in chat history. A vault of markdown files that nobody, including you, can navigate a month later.

The fix isn't another app. It's removing the organizing step entirely: **you talk, the agent files**. And it has to be *yours* — I wasn't going to pipe my private notes, clients, and goals through somebody's SaaS. Everything here runs on your own server, lands in your own Obsidian vault as plain markdown, and is small enough to actually read before you trust it with your life.



## What talking to it looks like

```
You   (voice, 40s, while walking): "Call with Alisher — they're in for the
      pilot, but want to push the start to July. I need to update the
      proposal, and remind me Friday to send the contract."

Bot:  💾 Saved: Alisher's CRM card updated (pilot, July start), linked
      to [[pilot-project]]. Reminder set: Friday 10:00 — send the contract.

      — Friday, 10:00 —

Bot:  🔔 Reminder: send Alisher the contract. Context: pilot, July start,
      proposal updated on Tuesday.
```

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

No commands to memorize, no categories to pick, no app to open. Telegram is the whole interface.



## Philosophy

**Voice-first.** Capture has to be cheaper than forgetting, or the system dies. A voice note costs five seconds.

**The vault is the source of truth.** Everything lives as plain markdown in *your* Obsidian vault on *your* server. Delete the agent tomorrow — you keep everything, readable forever. No lock-in, no export button needed.

**Memory that forgets, like yours.** Storage is not memory. Knowledge decays on the Ebbinghaus curve, fades through five tiers, and resurfaces when it matters — so the graph stays sharp instead of becoming a landfill.

**Interactive session, by the rules.** One persistent Claude Code session in tmux, driven the way a human drives it. No headless `claude -p` anywhere in the hot path — a CI guard fails the build if anyone tries.

**Small enough to read.** One Python process, a handful of modules, 220+ tests. You can audit the thing that reads your private notes in an evening.



## What it does

<table>
<tr><td><b>🎙 Total capture</b></td><td>Voice (Deepgram, seconds), text, photos, documents, videos, forwarded posts, whole albums — the agent reads files itself and files the takeaways. Nothing you send is ever silently dropped.</td></tr>
<tr><td><b>🧠 Knowledge graph memory</b></td><td>Powered by <a href="https://github.com/smixs/autograph">autograph</a>: typed cards, wiki-links, Ebbinghaus decay across five tiers, automatic MOC indexes, health scoring, link repair, dedup. The most thorough open-source memory layer you can drop on a vault.</td></tr>
<tr><td><b>⏰ Self-managed routines</b></td><td>"Remind me Friday at 3pm", "every weekday at 18:30 check my inbox folder" — the agent schedules its own cron jobs from plain language. One-shots, intervals, full cron expressions. No external task manager.</td></tr>
<tr><td><b>🌙 Nightly processing</b></td><td>At 21:00 your time it classifies the day's entries, writes vault cards, updates goals and long-term memory, rebuilds the graph — and sends you a daily report.</td></tr>
<tr><td><b>🔌 Claude Code, but for PKM</b></td><td>It IS Claude Code under the hood — so drop any MCP server into <code>mcp-config.json</code>, add any skill into <code>vault/.claude/skills/</code>, and your second brain grows new abilities. Like Claude Code through Telegram — for knowledge, not code.</td></tr>
<tr><td><b>🩺 Self-healing</b></td><td>A watchdog recovers a wedged session, a daily doctor sends a 🟢/🔴 canary report, broken jobs disable themselves and tell you. It just stays up.</td></tr>
</table>



## The memory engine: autograph

The part that makes this a *brain* rather than a logger is [**autograph**](https://github.com/smixs/autograph) — a typed memory layer for always-on agents, shipped here as a skill and also usable standalone on any Obsidian vault.

- **Typed graph** — every card carries a type (note, contact, project, CRM), a description for retrieval, tags, status; one `schema.json` rules them all
- **Ebbinghaus decay** — strength `1 + ln(access_count)`: each touch slows forgetting; contacts fade in ~100 days, dailies in ~25
- **Five tiers** — core → active → warm → cold → archive; touching a card promotes it back up
- **Random recall** — occasionally an archived card resurfaces next to something current. Sometimes noise. Sometimes the best idea you forgot you had.
- **Self-maintenance** — orphan detection, broken-link repair, dedup into `.trash/`, MOC generation, a 100-point health score. You never run vault chores again.

| Tier | What happens |
|------|-------------|
| **Core** | Always in context: current projects, active clients, key goals |
| **Active** | Checked regularly: recent ideas, ongoing threads |
| **Warm** | Found when you search |
| **Cold** | Surfaces only in deep searches |
| **Archive** | Almost gone — but randomly recalled for creative collisions |



## How it works

```
Telegram ──▶ bot (aiogram) ──▶ persistent Claude Code session (tmux pane)
                 │                       │
                 │                       ├──▶ Obsidian vault (plain markdown)
                 │                       └──▶ autograph: graph · decay · MOC
                 ├──▶ cron ticker ──▶ second isolated session (reminders never block chat)
                 └──▶ watchdog + daily doctor (self-healing, 🟢/🔴 report)
```

The bot never spawns `claude` per message. It keeps **one long-lived interactive Claude Code session** alive in a tmux pane and types prompts into it — which is why a 24/7 agent runs on a flat Pro/Max subscription instead of metered API tokens. Scheduled jobs fire in a second, isolated session, so a reminder going off never interrupts your conversation. A cross-process lock serializes everything; a watchdog restarts whatever wedges.

Privacy is explicit: **voice audio** goes to Deepgram for transcription, **text** goes to Anthropic through your subscription, **everything else stays on your server**. The vault never leaves the machine.



## What it costs

| Service | Cost |
|---------|------|
| Claude Pro | $20/mo |
| VPS (any cheap one) | ~$5/mo |
| Deepgram | free tier ($200 credit) |
| **Total** | **~$25/mo, flat** |

A personal assistant that organizes your life, never sleeps, and gets better the more you use it — for the price of two coffees. And because the session is interactive, the price above *stays* the price: there is no token meter to run away from you.



## Quick start

Three steps, ~15 minutes of work (full beginner walkthrough: [🇷🇺 setup-guide](docs/setup-guide.ru.md) / [🇬🇧 vps-setup](docs/vps-setup.md)).

**1. Fork this repo** (make the fork **private** — it will contain your life), then fill in `vault/goals/` and the persona in `vault/.claude/skills/dbrain-processor/references/about.md`.

**2. Get two keys**: a bot token from [@BotFather](https://t.me/BotFather), a free key from [Deepgram](https://console.deepgram.com/), plus your Telegram ID from [@userinfobot](https://t.me/userinfobot).

**3. On a fresh Ubuntu VPS:**

```bash
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/agent-second-brain/main/bootstrap.sh | bash
```

The installer interviews you for the tokens, walks you through Claude Code login (browser link), installs systemd services, and finishes with a health check. The bot messages you when it's alive. That's it — start talking.

<details>
<summary>What the installer actually does (inspect before you trust)</summary>

`bootstrap.sh` clones your fork and hands off to `setup.sh`, which only asks questions (tokens, timezone, git remote) and writes `.env` (chmod 600). All real work happens in idempotent `upgrade.sh`: uv + Python deps, tmux, Claude CLI, `dbrain-*` systemd user units, a `dbrain` CLI (`status` / `logs` / `attach` / `doctor`), permission hardening, and a first doctor run. Every script is short enough to read first.
</details>



## Upgrading from v1 / v2

One idempotent command — it migrates old units, installs what's missing, repairs permissions, and health-checks itself:

```bash
ssh your-server
cd agent-second-brain && git pull && bash upgrade.sh
```

If a migration ever goes sideways, run `claude` in the project directory and call the **migrate-doctor** skill — it diagnoses the install layout (v1/v2/v3), backs up, and repairs interactively.



## Vault structure

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



## Skills

| Skill | What it does |
|-------|-------------|
| **dbrain-processor** | Classifies entries, writes vault cards, daily reports |
| **[autograph](

... (truncated, 2646 more characters)

## pyproject.toml

```
[project]
name = "agent-second-brain"
version = "3.0.3"
description = "Voice-first personal assistant for Telegram with an Obsidian second brain"
readme = "README.md"
authors = [
    { name = "smixs", email = "mixshima@gmail.com" }
]
requires-python = ">=3.12"
dependencies = [
    "aiogram>=3.0,<4",
    "croniter>=2.0,<7",
    "deepgram-sdk>=5.3,<6",
    "httpx>=0.28,<1",
    "pydantic>=2.0,<3",
    "pydantic-settings>=2.0,<3",
]

[build-system]
requires = ["uv_build>=0.9.7,<0.10.0"]
build-backend = "uv_build"

[tool.uv.build-backend]
module-name = "d_brain"

[tool.ruff]
line-length = 88
target-version = "py312"
# vault/ is the agent's workspace — skills there keep their own style;
# the bot's lint gate covers src/ and tests/ only.
extend-exclude = ["vault"]

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]

[tool.pytest.ini_options]
asyncio_mode = "auto"

[dependency-groups]
dev = [
    "pytest>=9.0.2",
    "pytest-asyncio>=1.3.0",
    "ruff>=0.9",
]

```

## Top-level layout

- .claude/ (dir, 1 files, ~8 lines)
- .env.example (~37 lines)
- .github/ (dir, 1 files, ~28 lines)
- .gitignore (~43 lines)
- assets/ (dir, 1 files, ~0 lines)
- bin/ (dir, 1 files, ~78 lines)
- bootstrap.sh (~62 lines)
- deploy/ (dir, 9 files, ~180 lines)
- docs/ (dir, 2 files, ~1631 lines)
- LICENSE (~21 lines)
- pyproject.toml (~44 lines)
- README.md (~239 lines)
- README.ru.md (~231 lines)
- scripts/ (dir, 4 files, ~243 lines)
- setup.sh (~430 lines)
- src/ (dir, 29 files, ~3735 lines)
- tests/ (dir, 20 files, ~3126 lines)
- upgrade.sh (~91 lines)
- uv.lock (~958 lines)
- vault/ (dir, 70 files, ~11933 lines)

