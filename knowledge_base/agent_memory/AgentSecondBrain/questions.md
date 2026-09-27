---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: smixs/agent-second-brain

### Q1. What is Agent Second Brain in one sentence, and what problem does it solve?
> [!tip]- Answer
> Agent Second Brain is an always-on Telegram-fronted second brain that files voice and text into a personal Obsidian vault via one long-lived interactive Claude Code session, with zero per-token API billing. It exists because productivity systems die when maintaining them costs more than the work — un-relistened voice memos, ideas drowning in chat history, unnavigable vaults — so the fix is removing the organizing step entirely: you talk, the agent files. See [[wiki/01-overview|Overview]].

### Q2. Why does v3.0 use one persistent interactive Claude Code session, and what enforces that rule?
> [!tip]- Answer
> Since 2026-06-15 headless `claude -p` runs bill a separate Agent SDK credit, so v3.0 keeps one long-lived interactive session alive in a tmux pane and types prompts into it instead of spawning `claude` per message. A CI guard bans headless calls in the hot path, which is what keeps 24/7 operation inside a flat Pro/Max subscription. See [[wiki/01-overview|Overview]].

### Q3. What are the five stated principles, and how does the vault-as-source-of-truth principle protect the user?
> [!tip]- Answer
> The principles are voice-first capture, the vault as source of truth, memory that forgets like yours, interactive session by the rules, and small enough to read in an evening. Because everything lives as plain markdown in the user's Obsidian vault on the user's own server, deleting the agent keeps everything readable forever with no third-party SaaS holding private notes. See [[wiki/01-overview|Overview]].

### Q4. How does the autograph memory engine work, and what are its five tiers?
> [!tip]- Answer
> Autograph is a typed memory layer where every card carries a type, retrieval description, tags, and status under one `schema.json`, with Ebbinghaus decay (`1 + ln(access_count)`) so each touch slows forgetting. Cards fade through core (always in context), active, warm, cold, and archive tiers, touching promotes back up, archived cards randomly resurface, and self-maintenance handles orphans, link repair, dedup, MOCs, and a 100-point health score. See [[wiki/01-overview|Overview]].

### Q5. How do the runtime pieces fit together, and what does the flat ~$25/mo buy?
> [!tip]- Answer
> Telegram flows through an aiogram bot into the persistent tmux session, which writes the vault and autograph graph, while a cron ticker fires scheduled jobs in a second isolated session so reminders never block chat, serialized by a cross-process lock with watchdog and daily doctor self-healing. The ~$25/mo covers Claude Pro $20 plus a ~$5 VPS with Deepgram on its free tier, and only voice audio leaves for Deepgram and text for Anthropic while the vault stays on the server. See [[wiki/01-overview|Overview]].

### Q6. What do `.env.example`, `setup.sh`'s env writer, and `.gitignore` each contribute to secret and vault-data hygiene?
> [!tip]- Answer
> `.env.example` declares all runtime configuration — bot token, Deepgram key, vault path, allow-list, timezone, model, and cron toggles — with safe defaults, and `setup.sh` writes only the non-advanced subset to a `chmod 600` `.env`. `.gitignore` keeps secrets and personal vault data (`.env*`, `vault/daily/`, `contacts/`, `finances/`, `business/`, `projects/`, `thoughts/`, and more) out of git while noting `vault/.claude/` IS the product. See [[wiki/02-top-level-files|Top-level-files]].

### Q7. (Evaluation) Should you self-host Agent Second Brain for personal voice-first capture, and what must you accept first?
> [!tip]- Answer
> Recommend it when you want Telegram voice notes filed into an ownable Obsidian vault at a flat ~$25/mo with no per-token meter, and you accept running a 24/7 VPS plus a Claude subscription with a private fork and two keys. Before installing, verify you are comfortable with the persistent interactive-session model, the Ubuntu/Debian systemd deployment, and voice audio going to Deepgram for transcription. See [[wiki/02-top-level-files|Top-level-files]].
