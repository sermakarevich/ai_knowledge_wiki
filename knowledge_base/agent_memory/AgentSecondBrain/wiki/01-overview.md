> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
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
---
## Purpose and product
What it is: "An always-on second brain you talk to" — voice note in Telegram becomes typed, linked knowledge in the Obsidian vault (README.md:13-15). The motivating failure mode is productivity systems that die because maintaining them costs more than the work: un-relistened voice memos, ideas drowning in chat history, unnavigable markdown vaults (README.md:53). The fix is removing the organizing step entirely: "you talk, the agent files", self-hosted so private notes, clients, and goals never pass through third-party SaaS (README.md:55).
Start-here map (README.md:40-47):
| You want to… | Go to |
|---|---|
| Understand what this thing is | Why I built this |
| Install it on a fresh VPS in one command | Quick start |
| Upgrade an existing v1 / v2 install | Upgrading from v1 / v2 |
| Пошаговая инструкция на русском, для новичков | docs/setup-guide.ru.md |
| Just want the memory engine for your own vault | autograph |
| See how the persistent-session trick works | How it works |
Example interactions, verbatim (README.md:61-85):
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
## Philosophy
Five stated principles (README.md:91-101):
- **Voice-first.** Capture must be cheaper than forgetting; a voice note costs five seconds (README.md:93).
- **The vault is the source of truth.** Everything lives as plain markdown in the user's Obsidian vault on the user's server; deleting the agent keeps everything (README.md:95).
- **Memory that forgets, like yours.** Storage is not memory; knowledge decays on the Ebbinghaus curve, fades through five tiers, and resurfaces when it matters (README.md:97).
- **Interactive session, by the rules.** One persistent Claude Code session in tmux, driven the way a human drives it; no headless `claude -p` in the hot path, enforced by CI guard (README.md:99).
- **Small enough to read.** One Python process, a handful of modules, 220+ tests; auditable in an evening (README.md:101).
## Capabilities
Feature table, verbatim content (README.md:107-114):
| Capability | Behavior |
|---|---|
| 🎙 Total capture | Voice (Deepgram, seconds), text, photos, documents, videos, forwarded posts, whole albums — the agent reads files itself and files takeaways; nothing sent is silently dropped |
| 🧠 Knowledge graph memory | Powered by autograph: typed cards, wiki-links, Ebbinghaus decay across five tiers, automatic MOC indexes, health scoring, link repair, dedup |
| ⏰ Self-managed routines | Plain-language scheduling ("Remind me Friday at 3pm", "every weekday at 18:30 check my inbox folder"); one-shots, intervals, full cron expressions; no external task manager |
| 🌙 Nightly processing | At 21:00 local time classifies the day's entries, writes vault cards, updates goals and long-term memory, rebuilds the graph, sends a daily report |
| 🔌 Claude Code, but for PKM | It IS Claude Code under the hood — MCP servers via `mcp-config.json`, new abilities via skills in `vault/.claude/skills/` |
| 🩺 Self-healing | Watchdog recovers wedged sessions, daily doctor sends a 🟢/🔴 canary report, broken jobs disable themselves and notify |
## Memory engine: autograph
The part that makes this a *brain* rather than a logger is autograph — a typed memory layer for always-on agents, shipped here as a skill and usable standalone on any Obsidian vault (README.md:120). Properties (README.md:122-126):
- **Typed graph** — every card carries a type (`note`, `contact`, `project`, `CRM`), a description for retrieval, tags, status; one `schema.json` rules them all.
- **Ebbinghaus decay** — strength `1 + ln(access_count)`: each touch slows forgetting; contacts fade in ~100 days, dailies in ~25.
- **Five tiers** — `core` → `active` → `warm` → `cold` → `archive`; touching a card promotes it back up.
- **Random recall** — occasionally an archived card resurfaces next to something current.
- **Self-maintenance** — orphan detection, broken-link repair, dedup into `.trash/`, MOC generation, a 100-point health score.
Tier table, verbatim (README.md:128-134):
| Tier | What happens |
|------|-------------|
| **Core** | Always in context: current projects, active clients, key goals |
| **Active** | Checked regularly: recent ideas, ongoing threads |
| **Warm** | Found when you search |
| **Cold** | Surfaces only in deep searches |
| **Archive** | Almost gone — but randomly recalled for creative collisions |
## Architecture
Dataflow, verbatim (README.md:140-147):
```
Telegram ──▶ bot (aiogram) ──▶ persistent Claude Code session (tmux pane)
                 │                       │
                 │                       ├──▶ Obsidian vault (plain markdown)
                 │                       └──▶ autograph: graph · decay · MOC
                 ├──▶ cron ticker ──▶ second isolated session (reminders never block chat)
                 └──▶ watchdog + daily doctor (self-healing, 🟢/🔴 report)
```
Key mechanics (README.md:149): the bot never spawns `claude` per message; it keeps one long-lived interactive session alive in a tmux pane and types prompts into it, which is why 24/7 operation fits a flat Pro/Max subscription. Scheduled jobs fire in a second isolated session so reminders never interrupt conversation. A cross-process lock serializes everything; a watchdog restarts whatever wedges. Privacy split, verbatim claim (README.md:151): **voice audio** goes to Deepgram for transcription, **text** goes to Anthropic through the subscription, **everything else stays on the server**; the vault never leaves the machine.
## Cost model
Flat-price table, verbatim (README.md:157-162):
| Service | Cost |
|---------|------|
| Claude Pro | $20/mo |
| VPS (any cheap one) | ~$5/mo |
| Deepgram | free tier ($200 credit) |
| **Total** | **~$25/mo, flat** |
Because the session is interactive, the price above stays the price with no token meter to run away (README.md:164).
## Install and upgrade
Quick start is three steps in ~15 minutes; full walkthroughs are `docs/setup-guide.ru.md` and `docs/vps-setup.md` (README.md:170). Step 1: fork the repo (make the fork **private**) then fill in `vault/goals/` and the persona in `vault/.claude/skills/dbrain-processor/references/about.md` (README.md:172). Step 2: get two keys — bot token from `@BotFather`, free key from Deepgram, plus the Telegram ID from `@userinfobot` (README.md:174). Step 3, verbatim (README.md:178-180):
```bash
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/agent-second-brain/main/bootstrap.sh | bash
```
The installer interviews for tokens, walks through Claude Code login (browser link), installs systemd services, and finishes with a health check; the bot messages when alive (README.md:182). What the installer does: `bootstrap.sh` clones the fork and hands off to `setup.sh`, which only asks questions (tokens, timezone, git remote) and writes `.env` (chmod 600); all real work happens in idempotent `upgrade.sh`: uv + Python deps, tmux, Claude CLI, `dbrain-*` systemd user units, a `dbrain` CLI (`status` / `logs` / `attach` / `doctor`), permission hardening, and a first doctor run (README.md:187). Upgrade path, verbatim (README.md:196-199):
```bash
ssh your-server
cd agent-second-brain && git pull && bash upgrade.sh
```
The command is idempotent — migrates old units, installs missing pieces, repairs permissions, health-checks itself (README.md:194). If migration fails, run `claude` in the project directory and call the **migrate-doctor** skill, which diagnoses the install layout (v1/v2/v3), backs up, and repairs interactively (README.md:201).
## Vault structure
Layout, verbatim (README.md:207-221):
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
## Skills (source truncated)
The chunk's Skills table is cut mid-entry at `| **[autograph](` (README.md:230) so only one complete row is visible: **dbrain-processor** classifies entries, writes vault cards, and produces daily reports (README.md:229). No further skill rows can be claimed from this chunk. The chunk also ends with an incomplete `## Macro components` list containing only `top-level-files/` (01-overview.md:232-234), so the component map itself is truncated.
**Covers:** README.md (tagline, billing note, start-here map, motivation, interaction examples, philosophy, capabilities, autograph, architecture, privacy, cost, quick start, upgrade, vault layout, skills header); vault/ directory layout; truncated Skills table and Macro components list (cut, not summarized)
