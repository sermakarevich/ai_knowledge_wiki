> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Messaging Gateway and Bot Mode
**In one sentence:** Hermes runs one gateway process that connects 20+ messaging platforms at once, while Bot Mode provides a roster of named specialist Bots with their own model, memory, skills, routines, and group-chat collaboration.
## Key points
- Hermes messaging gateway connects 20+ platforms from one background process, including Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Mattermost, Email, SMS, DingTalk, Feishu, WeCom, Weixin, QQ Bot, Yuanbao, BlueBubbles, Home Assistant, Teams, Google Chat, LINE, ntfy, SimpleX, IRC, and webhooks.
- Setup starts with `hermes gateway setup` for interactive configuration, then `hermes gateway`, `hermes gateway install`, `hermes gateway start`, `hermes gateway stop`, and `hermes gateway status` for running and service management.
- Bot Mode turns Hermes profiles into a roster of named Bots, where each Bot has its own chat, role, model pin, memory, skills, toolsets, SOUL.md persona, and avatar.
- Bots run recurring routines as namespaced cron jobs in the form `[bot:<name>] <routine>`, visible in both the Routines pane and `hermes cron list`.
- Group chats hold 2--6 Bots that coordinate in serial rounds, pull each other in with @mentions, escalate with @user, and show a needs-you badge when human judgment is required.
- Bot-to-bot messaging uses @mentions resolved against the live roster plus direct `message_agent` calls with automatic sender attribution, and cross-machine delivery works through Desktop relay or `hermes peer` links.
- For always-on service setup, Linux uses systemd user service plus `sudo loginctl enable-linger $USER` or a boot-time system service, while macOS uses a launchd agent, and `platforms.<name>.enabled: false` in config always wins over leftover credentials.
---
## Gateway architecture and setup
The gateway is a single background process that hosts one adapter per platform. Each adapter receives messages, routes them through a per-chat session store, dispatches to the agent for processing, and runs a cron scheduler ticking every 60 seconds.
Quick setup:
- Run `hermes gateway setup` to configure platforms interactively with token prompts and allowlists.
- Run `hermes gateway` for foreground testing, then install as a service for normal use.
- Manage one adapter without full restart via `/platform list`, `/platform pause <name>`, and `/platform resume <name>`.
- Sessions persist across messages and restarts, with `/new`, `/model`, `/sessions`, `/resume`, `/bg`, `/voice`, `/sethome`, and `/help` available inside chats.
- Security defaults to deny: only allowlisted or DM-paired users can reach the bot, configured via `TELEGRAM_ALLOWED_USERS`, `DISCORD_ALLOWED_USERS`, `GATEWAY_ALLOWED_USERS`, or `hermes pairing approve <platform> <code>`.
- Admin versus regular-user tiers gate slash-command access per DM and group scope, inspectable with `/whoami`.
- Delivery is durable via a ledger in `state.db` with bounded at-least-once redelivery, restart auto-resume for interrupted sessions, optional restart notifications per platform, typing indicators, and a circuit breaker that auto-pauses failing adapters until manual resume.
- Per-channel overrides allow different models and system prompts per chat or thread via `channel_overrides`, with session `/model` still taking priority.
## Platform list grouped by family
Popular Western chat:
- Telegram -- full voice, images, files, threads, typing, streaming.
- Discord -- full voice, images, files, threads, reactions, typing, streaming.
- Slack -- full voice, images, files, threads, reactions, typing, streaming.
- WhatsApp and WhatsApp Cloud API -- images, files, typing, with voice support on Cloud API.
- Signal and SMS via Twilio -- Signal supports images, files, typing; SMS is text-only.
- Email -- images, files, threads.
- Matrix and Mattermost -- rich support including voice, images, files, threads, typing, streaming on Matrix.
- Google Chat, Microsoft Teams, LINE, ntfy, SimpleX, IRC, Buzz, Raft.
China and regional platforms:
- DingTalk -- images, files, reactions, streaming.
- Feishu/Lark -- full voice, images, files, threads, reactions, typing, streaming.
- WeCom and WeCom Callback -- files and images on standard WeCom.
- Weixin/WeChat -- voice, images, files, typing.
- QQ Bot and Yuanbao -- voice, images, files, typing, with streaming on Yuanbao.
Apple and automation surfaces:
- BlueBubbles and Photon for iMessage -- images, files, reactions, typing, with voice on Photon.
- Home Assistant -- text plus native device tools such as `ha_list_entities`, `ha_get_state`, `ha_call_service`, and `ha_list_services`.
- Webhooks, API server, and Relay connectors for programmatic and proxied access.
## Telegram/Discord/Slack setup sketch
Telegram example:
- Create bot with [[BotFather]] via `/newbot`, save API token, optionally set description, about text, avatar, and command menu.
- Find numeric user ID via user-info bot, then run `hermes gateway setup` or set `TELEGRAM_BOT_TOKEN` and `TELEGRAM_ALLOWED_USERS` in env.
- Start with `hermes gateway` and set home channel with `/sethome` for cron deliveries.
- For groups: disable BotFather Group Privacy or make bot admin, remove and re-add bot after privacy change, then use `require_mention: true`, `exclusive_bot_mentions: true`, `mention_patterns`, and `ignored_threads` to control triggers.
- For cloud idle: set webhook URL plus secret instead of default long polling; for restricted networks: set Telegram-specific proxy.
Discord and Slack sketch:
- Same gateway pattern: interactive setup stores tokens, allowlists gate access, `/sethome` designates cron delivery channel.
- Use per-channel model overrides for specialist rooms, typing-indicator flags where noisy, and unique tokens per profile when running multiple Hermes bots in one group.
## Bot Mode -- named bots
A Bot is a Hermes profile under `~/.hermes/profiles/<name>/`, rendered as a roster row with avatar, preview, timestamp, search, hide/unhide, sections, and an Active-now presence strip. Creation via New Agent needs only Name, Title, and Description; Advanced adds clone-from-profile, empty profile, model and provider pin, custom SOUL.md, per-skill and per-toolset and per-MCP enablement, and shared credential pool. Editing, duplicating, renaming, and deleting reuse the same profile surface, with CLI parity via `hermes -p <bot> chat`, `hermes profile list`, and `hermes profile create`. Bot Mode ships built into Desktop and is on by default, with a Bots tab, docked Routines pane, persistent canonical Bot Chat per Bot, and blob, geometric, uploaded, generated, or pet avatars.
Per-Bot model, memory, and skills:
- Each Bot can pin a different provider/model pair or inherit the launch profile default.
- Memory, chat history, credentials scope, SOUL.md, skills, toolsets, and MCP servers are isolated per profile.
- Title and description define the teammate roster entry so other Bots know each specialist role.
Routines:
- Routines attach recurring tasks to the responsible Bot through a schedule picker plus raw schedule string.
- Runs land in that Bot chat history for direct follow-up.
Group chats and @mentions:
- Groups are roster rows with member count, preview, and needs-you state; membership syncs through backend profile metadata and rooms mirror across connected gateways.
- Open chat triggers up to three serial rounds with caps at 10 messages per send; mentioned Bots respond or pass, unmentioned Bots stay quiet unless nobody was mentioned.
- Each member keeps a persistent `Group: <name>` session; rooms can span machines with device-badged members and `@name-device` handles.
- In any chat, `@botname` resolves against the live roster and the active Bot composes its own forwarded message; direct Bot-to-Bot calls use `message_agent(target="researcher", message="...")` with fire-and-forget delivery and background reply notification.
- Cross-connection Bots are reachable the same way while Desktop runs; `hermes peer add`, `hermes peer dm`, `hermes peer run`, `hermes peer status`, and `hermes peer stop` provide Desktop-free machine-to-machine links.
- Failed deliveries retry at most once for transient, timeout, rate-limit, server-error, or context-overflow cases, carry typed `reason` codes, and never auto-retry auth, quota, or config errors.
## Media delivery notes
- Agent replies embed `MEDIA:/path/to/file` tags that the gateway ships as native attachments where supported, including Telegram, Discord, Slack, Signal, WhatsApp, Feishu, and Matrix.
- Supported classes include images, audio, video, documents, office files, archives, and books/packages; unsupported surfaces fall back to link or text indicator.
- For Docker-backed terminals, write outputs to a host-mounted path such as `/home/user/.hermes/cache/documents/report.txt` so the gateway process can read the emitted `MEDIA:` path.
- Incoming Telegram voice is auto-transcribed by configured STT provider, or passed as a cached audio path when `stt.enabled: false` for custom diarization or archiving.
- Outgoing TTS arrives as native Telegram voice bubbles, with Opus-native providers needing no setup and Edge TTS requiring ffmpeg for bubble format.
- Public Telegram Bot API caps downloads at 20 MB; a local Bot API server in local mode raises the ceiling to 2 GB when Hermes points at custom `base_url` and `base_file_url` with `local_mode: true`.
- Document delivery detail such as [[as_document]] forcing file-versus-inline rendering was not confirmed in the fetched overview pages; use native `MEDIA:` attachments and platform defaults unless a platform page documents an explicit override.
**Covers:** user-guide/messaging, user-guide/bot-mode, user-guide/messaging/telegram (docs site, retrieved 2026-09-08)
