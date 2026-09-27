# Hermes Agent Documentation

**Article:** [Hermes Agent Documentation](https://hermes-agent.nousresearch.com/docs/) — Nous Research docs site (Docusaurus, ~150 pages), retrieved 2026-09-08

## Human Readable TL;DR

Hermes Agent is a smart computer assistant made by Nous Research that lives in your terminal and can also answer you on Telegram, Discord, Slack, WhatsApp, and 15+ other chat apps. Think of it as an apprentice that remembers your preferences in a tiny notebook, writes its own how-to guides when it learns something new, and can do chores on a schedule — like a helper who gets better at helping you every day. You install it with one command, connect it to an AI model (easiest through the Nous Portal login), and then chat, give it computer tasks, or let it run errands automatically.

## TL;DR

Hermes Agent is Nous Research's terminal-native autonomous agent: persistent dual-store memory (MEMORY.md/USER.md) plus session search, self-authored progressive-disclosure skills with a hub ecosystem, 60+ built-in tools across selectable toolsets with 7 terminal backends, a 20+ platform messaging gateway with named Bots and group chats, cron scheduling with subagent delegation and checkpoint rollback, and layered security — configured via `~/.hermes/config.yaml` + `.env`, served by one platform-agnostic `AIAgent` core across CLI, TUI, Desktop, gateway, ACP, batch, and API surfaces.

---

## Problem & Motivation

General-purpose chatbots forget everything between sessions, live only in a browser tab, and cannot act on your computer or reach you where you already chat. Hermes answers that gap with an agent that persists (memory + skills that compound across sessions), acts (terminal, browser, code execution, messaging tools), is reachable (one gateway process on 20+ platforms), and runs unattended (cron, delegation, checkpoints) — while staying governable through approval gates, audit surfaces, and container isolation.

---

## Main Original Ideas

1. **Bounded curated memory plus free recall.** Two tiny agent-managed files (~1,300 tokens total, always in context) for facts that must always be present, paired with FTS5 session search over every past conversation at zero token cost until queried — a two-tier recall design rather than one ever-growing context.
2. **The agent writes its own procedures.** `skill_manage` lets the agent save non-trivial workflows as reusable skills (lessons, not logs), installed from 8 hub sources, security-scanned, background-maintained by a Curator — procedural memory that compounds without human authoring.
3. **A post-turn learning loop with consent controls.** A background review replays each turn and may save memories or patch skills, with cheaper-model routing, local-GPU deferral, notification levels, and `write_approval` staging gates for both memory and skills.
4. **One gateway, every chat app, plus a bot roster.** A single background process hosts one adapter per messaging platform, while Bot Mode turns profiles into named specialists with own model, memory, skills, routines, and serial-round group chats with @mentions and human escalation.
5. **Toolsets and terminal backends as the unit of capability.** 60+ tools grouped into enable/disable toolsets (per run, per platform, per MCP server), with the terminal tool spanning local, Docker, SSH, Singularity, Modal, Daytona, and Vercel sandboxes — capability scoping instead of all-tools-always.
6. **Automation with undo.** Cron jobs in isolated fresh sessions plus subagent delegation and shadow-git checkpoints make unattended work reviewable and revertible; a hardline blocklist of catastrophic commands holds even in auto-approve modes.

---

## Key Findings

- Install is one curl/PowerShell command or a Desktop installer; models need ≥64K context; provider setup is fastest via `hermes setup --portal` (one OAuth login, 300+ models plus managed Tool Gateway).
- Config splits cleanly: secrets in `~/.hermes/.env`, settings in `~/.hermes/config.yaml` (`hermes config set` routes automatically); sessions persist in SQLite with resume, compression, background tasks, and git-worktree isolation.
- Memory limits fail loudly (consolidate-and-retry, no silent drops); `/journey` visualizes and prunes everything learned; 8 external memory providers add graphs/semantic search alongside built-ins.
- Skills load progressively (~3k-token index, full content on demand), stack 5 per message, bundle into YAML aliases, and span project-local → local → external precedence with trust/quarantine for repo-carried skills.
- Gateway setup is `hermes gateway setup` then run/install/start; always-on via systemd linger (Linux) or launchd (macOS); bots run namespaced cron routines and coordinate in 2–6-member group chats.
- MCP servers declare as stdio or HTTP under `mcp_servers`, register as `mcp_<server>_<tool>` with include/exclude glob exposure control; Nous Tool Gateway routes search, extract, image-gen, TTS, cloud browsers, and cloud terminals through managed infra.
- Security is eight layers (approvals, authorization, write guards, containers, credential filtering, injection scanning, hardline blocklist, secret-safe skill setup); batch/trajectory export feeds RL training via Atropos.

---

## Suggestions & Future Directions

1. **Start minimal, add layers in order.** Docs' own learning path: install → chat → provider → gateway → tools/skills/MCP → automation — each layer assumes the previous one works (`hermes doctor` first when stuck).
2. **Gate the learning loop early.** Turn on `memory.write_approval` / `skills.write_approval` while the agent still learns your conventions, then relax once `/journey` shows stable entries.
3. **Scope capabilities per surface.** Use toolsets, MCP include/exclude lists, and per-platform display settings so each chat surface exposes only what it needs.
4. **Treat skills as the compounding asset.** Invest in `/learn` and Curator hygiene: the entry's durable value is the skill library, not any single session.
5. **Open questions the docs leave for operators.** Cost/latency of always-on gateway + background reviews at scale; quality variance of agent-authored skills across model sizes; multi-user authorization boundaries on shared gateways.

---

## Authors & Institutions

Nous Research (docs site authors; no individual authors listed). Source: https://hermes-agent.nousresearch.com/docs/ — see [[connections]] for related KB entries.
