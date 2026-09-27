> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# SQLite Mail Messaging and Event Observation
**In one sentence:** Overstory agents exchange mail through a SQLite (lightweight file-based relational database)-backed `messages` table with destructive-read `check` semantics, group-address fan-out, file-based priority nudges, and a parallel `events.db` observability log fed by a polling NDJSON (Newline-Delimited JSON, one JSON object per line) tailer with tool-argument filtering.
## Key points
- Mail persistence is one `messages` table with 11 columns (`id`, `from_agent`, `to_agent`, `subject`, `body`, `type`, `priority`, `thread_id`, `payload`, `read`, `created_at`) plus 2 indexes (`idx_inbox` on `(to_agent, read)`, `idx_thread` on `thread_id`) (`src/mail/store.ts:46`, `src/mail/store.ts:135`).
- Message identity is `msg-` plus 12 random lowercase alphanumeric characters generated with `crypto.getRandomValues`, and `createdAt` is an ISO (International Organization for Standardization, here an ISO-8601 timestamp) string assigned at insert time, not by SQLite defaults (`src/mail/store.ts:140`, `src/mail/store.ts:274`).
- Reads are destructive: both `check()` and `checkInject()` fetch unread rows and immediately set `read = 1`, so each message is delivered once per agent unless re-queried via `list` (`src/mail/client.ts:156`, `src/mail/client.ts:164`).
- Broadcast is fan-out, not multicast: a `@group` send resolves to N agent names and inserts N independent rows, each with its own `mail_sent` event row and nudge marker (`src/commands/mail.ts:327`, `src/mail/broadcast.ts:51`).
- Urgent delivery avoids direct interruption: `high`/`urgent` priority or 5 protocol types (`worker_done`, `merge_ready`, `error`, `escalation`, `merge_failed`) write a JSON marker to `.overstory/pending-nudges/{agent}.json` consumed on the next `mail check --inject`; only `dispatch` additionally forces an immediate tmux (terminal multiplexer, used here to poke an idle agent pane) `sendKeys` after a 3-second delay (`src/commands/mail.ts:27`, `src/commands/mail.ts:479`).
- Events are a separate SQLite database with an auto-increment `events` table (run/agent/session attribution, tool name, arguments, duration, level, timestamp) and 5 indexes including a partial index on `level = 'error'` (`src/events/store.ts:34`, `src/events/store.ts:49`).
- Live progress comes from polling, not streaming: `startEventTailer()` polls a headless agent's `stdout.log` every 500 ms (milliseconds), tracks a byte offset, parses only new NDJSON (Newline-Delimited JSON) lines, and inserts them into `events.db`; all failures are swallowed (`src/events/tailer.ts:90`, `src/events/tailer.ts:116`).
- Tool-call volume is reduced at write time by per-tool filters (e.g. `Read` keeps only `file_path`/`offset`/`limit`, `Bash` keeps `command`/`description` truncated to 80 chars), shrinking payloads from ~20 KB (kilobytes) to ~200 bytes (`src/events/tool-filter.ts:21`, `src/events/tool-filter.ts:53`).
---
## Mail store schema
The low-level store owns DDL (Data Definition Language, the `CREATE TABLE` statements) and prepared statements; the client never touches SQL (Structured Query Language, the database query language) directly (`src/mail/store.ts:177`).
```sql
CREATE TABLE IF NOT EXISTS messages (
  id TEXT PRIMARY KEY,
  from_agent TEXT NOT NULL,
  to_agent TEXT NOT NULL,
  subject TEXT NOT NULL,
  body TEXT NOT NULL,
  type TEXT NOT NULL DEFAULT 'status' CHECK(type IN (...12 types...)),
  priority TEXT NOT NULL DEFAULT 'normal' CHECK(priority IN ('low','normal','high','urgent')),
  thread_id TEXT,
  payload TEXT,
  read INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
)
```
(`src/mail/store.ts:46`)
Row mapping is snake_case columns to camelCase objects with integer-to-boolean conversion (`read === 1`) (`src/mail/store.ts:29`, `src/mail/store.ts:155`). The `type` CHECK (constraint that rejects values outside a fixed list) is generated from the runtime `MAIL_MESSAGE_TYPES` constant, which holds 4 semantic types (`status`, `question`, `result`, `error`) and 8 protocol types (`worker_done`, `merge_ready`, `merged`, `merge_failed`, `escalation`, `health_check`, `dispatch`, `assign`) (`src/mail/store.ts:44`, `src/types.ts:233`).
Concurrency uses WAL (Write-Ahead Logging, a SQLite mode allowing concurrent readers with one writer) mode, `synchronous = NORMAL`, and a 5-second busy timeout; `close()` issues a passive WAL (Write-Ahead Logging) checkpoint before disconnecting (`src/mail/store.ts:184`, `src/mail/store.ts:376`). Schema migration handles three paths (missing CHECK constraints, missing `payload` column, old type list missing `worker_done`) by either `ALTER TABLE ... ADD COLUMN` or full table recreation with `CASE`-mapped type/priority fallback to `status`/`normal` (`src/mail/store.ts:72`, `src/mail/store.ts:98`).
Unread lookup is ordered oldest-first; filtered listing is ordered newest-first with optional `LIMIT` (`src/mail/store.ts:222`, `src/mail/store.ts:262`). `purge()` requires at least one filter at the CLI (Command-Line Interface) layer and counts rows before deleting so it can report the number removed (`src/commands/mail.ts:668`, `src/mail/store.ts:336`).
## Client API: send, read, ack
The client wraps the store with 7 operations: `send`, `sendProtocol`, `check`, `checkInject`, `list`, `markRead`, `reply` (`src/mail/client.ts:13`).
- `send()` defaults `type` to `status`, `priority` to `normal`, `threadId` and `payload` to null, and passes an empty `id` so the store generates one (`src/mail/client.ts:126`).
- `sendProtocol()` takes a typed `MailProtocolType` plus a structured object and `JSON.stringify`s it into the `payload` TEXT column; `parsePayload()` reverses this and returns null on missing payload or parse failure (`src/mail/client.ts:141`, `src/mail/client.ts:61`).
- `check(agentName)` returns unread messages and marks each read in a loop; `checkInject(agentName)` does the same then renders a hook-injection block (`src/mail/client.ts:156`, `src/mail/client.ts:164`).
- `markRead(id)` throws `MailError` on unknown ID and otherwise returns `{ alreadyRead: boolean }` (`src/mail/client.ts:176`).
- `reply(messageId, body, from)` inherits the original `type`/`priority`, sets `threadId` to the original thread or the original ID if root, prefixes `Re:`, and routes to the other side (if the replier equals the original sender the reply goes to the original recipient, else to the original sender) (`src/mail/client.ts:190`, `src/mail/client.ts:198`, `src/mail/client.ts:203`).
Injection format is one block per message with sender, priority tag, type, subject, body, conditional payload line (only for 8 protocol types in `PROTOCOL_TYPES`), and a reply hint (`src/mail/client.ts:93`, `src/mail/client.ts:76`):
```
You have 1 new message:

--- From: builder-1 [URGENT] (worker_done) ---
Subject: build finished
<body>
Payload: {"taskId":"..."}
[Reply with: ov mail reply msg-xxx --body "..."]
```
Human-readable CLI (Command-Line Interface) rendering instead uses `*`/space read markers and `From → To` lines (`src/commands/mail.ts:53`).
## Broadcast mechanism
Group addresses are strings starting with `@` (`src/mail/broadcast.ts:15`). Resolution is pure (no I/O): `@all` maps to all active session agent names minus the sender; 8 capability stems (`builder`, `scout`, `reviewer`, `lead`, `merger`, `supervisor`, `coordinator`, `monitor`) each accept singular and plural forms (`src/mail/broadcast.ts:59`, `src/mail/broadcast.ts:23`). Unknown groups and zero-recipient resolutions throw (`src/mail/broadcast.ts:62`, `src/mail/broadcast.ts:89`).
The CLI detects `isGroupAddress(to)`, loads active sessions, resolves recipients, then loops: one `client.send()` per recipient, one `mail_sent` event row per recipient with `broadcast: true`, one nudge marker per recipient if the auto-nudge predicate holds (`src/commands/mail.ts:314`, `src/commands/mail.ts:327`, `src/commands/mail.ts:332`).
## Mail CLI commands
Six subcommands under `ov mail`, all resolving the project root first (handles git worktrees) and opening `.overstory/mail.db` (`src/commands/mail.ts:707`, `src/commands/mail.ts:711`, `src/commands/mail.ts:72`).
- `send --to --subject --body [--from | --agent] [--type] [--priority] [--payload] [--json]`: validates type against `MAIL_MESSAGE_TYPES` and priority against the 4-level list, validates `--payload` is JSON (JavaScript Object Notation, a text encoding for structured data), defaults sender to `orchestrator` (`src/commands/mail.ts:274`, `src/commands/mail.ts:283`, `src/commands/mail.ts:301`).
- `check [--agent] [--inject] [--json] [--debounce <ms>]`: `--inject` reads and clears the pending-nudge marker, prepends a `PRIORITY:` banner, then writes hook-formatted output; `--debounce` silently skips when the last check timestamp in `mail-check-state.json` is within the window (`src/commands/mail.ts:528`, `src/commands/mail.ts:558`, `src/commands/mail.ts:548`).
- `list [--from] [--to] [--agent] [--unread] [--json]`: `--to` takes precedence over `--agent` alias; `--unread` maps to `read = 0` (`src/commands/mail.ts:599`).
- `read <message-id>`, `reply <message-id> --body`, `purge (--all | --days N | --agent name)`: `purge --days` converts days to milliseconds (`days * 24 * 60 * 60 * 1000`) (`src/commands/mail.ts:628`, `src/commands/mail.ts:643`, `src/commands/mail.ts:662`, `src/commands/mail.ts:684`).
Side effects on send: a `mail_sent` info-level event row (with optional `runId` from `current-run.txt`), a pending-nudge marker when `shouldAutoNudge()` holds, an immediate tmux nudge only for `dispatch`, and an advisory reviewer-coverage warning for `merge_ready` when builders outnumber reviewers (`src/commands/mail.ts:428`, `src/commands/mail.ts:458`, `src/commands/mail.ts:479`, `src/commands/mail.ts:492`). The nudge predicate is `priority === urgent|high` OR type in the 5-member `AUTO_NUDGE_TYPES` set (`src/commands/mail.ts:27`, `src/commands/mail.ts:39`).
Debounce state is a flat JSON map of agent name to epoch-millisecond timestamp, e.g. `{"coordinator": 1773152940230, ...}` (`.overstory/mail-check-state.json:1`); the path helper points at `<root>/.overstory/mail-check-state.json` and corrupt state is treated as no-debounce (`src/commands/mail.ts:163`, `src/commands/mail.ts:175`).
## Event store and tailer
The event store is a second SQLite database with one `events` table: integer auto-increment `id`, nullable `run_id`/`session_id`, `agent_name`, `event_type`, nullable tool columns (`tool_name`, `tool_args`, `tool_duration_ms`), `level` CHECK (`debug`, `info`, `warn`, `error`), nullable `data`, millisecond-precision timestamp (`src/events/store.ts:34`). Query API covers `getByAgent`, `getByRun`, `getErrors` (newest-first), `getTimeline` (requires `since`), `getToolStats` (count/avg/max duration grouped by tool for `tool_start` rows), and `purge` (`src/events/store.ts:215`, `src/events/store.ts:237`, `src/events/store.ts:258`, `src/events/store.ts:265`, `src/events/store.ts:272`, `src/events/store.ts:317`). `correlateToolEnd()` finds the newest unmatched `tool_start` for an agent+tool pair and backfills its duration (`src/events/tailer.ts:141` is tool-name extraction; correlation at `src/events/store.ts:190`).
The tailer bridges headless agents (which write NDJSON to `stdout.log`) into `events.db` because after `ov sling` exits nobody reads that stream (`src/events/tailer.ts:1`). Mechanics: open a dedicated `EventStore` connection, schedule the first poll after `pollIntervalMs` (default 500), on each tick compare `file.size` against `byteOffset`, slice only new bytes, split on `\n`, skip blank and malformed lines, map the `type` string (unknown maps to `custom`), extract tool name from `tool`/`tool_name`/`toolName`, set level `error` only for `type === "error"`, and insert with the full raw event as JSON in `data` (`src/events/tailer.ts:89`, `src/events/tailer.ts:116`, `src/events/tailer.ts:34`, `src/events/tailer.ts:139`, `src/events/tailer.ts:151`). `stop()` clears the timer and closes only tailer-owned connections (`src/events/tailer.ts:182`). Log discovery scans `.overstory/logs/{agentName}/` timestamped directories, sorts lexicographically (ISO timestamps with `-` separators sort correctly), and returns the latest `stdout.log` if it exists (`src/events/tailer.ts:214`).
## Tool-call filtering
`filterToolArgs(toolName, toolInput)` dispatches to a per-tool filter or returns `{ args: {}, summary: toolName }` for unknown tools (`src/events/tool-filter.ts:21`). Each filter uses `pickDefined` to keep only named keys and `truncate` for fixed-length summaries (`src/events/tool-filter.ts:34`, `src/events/tool-filter.ts:44`). Covered tools: `Bash` (keeps `command`, `description`), `Read` (`file_path`, `offset`, `limit` with line-range summaries), `Write`/`Edit` (`file_path` only, dropping file bodies), `Glob` (`pattern`, `path`), `Grep` (`pattern`, `path`, `glob`, `output_mode`), `WebFetch` (`url`), `WebSearch` (`query`), `Task` (`description`, `subagent_type`) (`src/events/tool-filter.ts:52`).
## Files on disk
- `<project-root>/.overstory/mail.db` — mail messages (`src/commands/mail.ts:73`).
- `<project-root>/.overstory/events.db` — observability events, opened separately on every send and by each tailer (`src/commands/mail.ts:415`, `src/events/tailer.ts:89`).
- `<project-root>/.overstory/pending-nudges/{agent}.json` — one JSON marker per agent (`from`, `reason`, `subject`, `messageId`, `createdAt`), overwritten per nudge, deleted on read (`src/commands/mail.ts:84`, `src/commands/mail.ts:104`, `src/commands/mail.ts:127`).
- `<project-root>/.overstory/mail-check-state.json` — debounce timestamps (`src/commands/mail.ts:163`).
- `<project-root>/.overstory/current-run.txt` — optional run ID attached to `mail_sent` events (`src/commands/mail.ts:419`).
- `<project-root>/.overstory/logs/{agentName}/{timestamp}/stdout.log` — tailed headless-agent output (`src/events/tailer.ts:214`).
## Message flow
```
sender CLI (ov mail send)
  ├─ validate type/priority/payload ──→ src/commands/mail.ts:283
  ├─ group? resolve @all/@capability ─→ src/mail/broadcast.ts:51
  ├─ 1× INSERT INTO messages per recipient (WAL) → src/mail/store.ts:212
  ├─ 1× INSERT INTO events (mail_sent) per msg  → src/commands/mail.ts:428
  └─ nudge? write pending-nudges/{to}.json ────→ src/commands/mail.ts:104
       (dispatch only: + tmux sendKeys, 3 s delay) → src/commands/mail.ts:479
recipient hook (mail check --inject)
  ├─ read+clear pending nudge → banner ─────────→ src/commands/mail.ts:560
  ├─ SELECT unread → format → UPDATE read=1 ────→ src/mail/client.ts:164
  └─ next --debounce window skips silently ─────→ src/commands/mail.ts:548
background (headless agents)
  stdout.log (NDJSON) ──poll 500 ms, byte cursor──→ events.db → src/events/tailer.ts:109
```
## Delivery semantics
At-most-once per `check`: unread fetch followed by per-row `markRead` means a crash between SELECT and UPDATE can redeliver, but a successful check never returns the same row twice (`src/mail/client.ts:156`). Broadcast multiplies this: N recipients means N independent rows with distinct IDs, so partial fan-out failure can deliver to a prefix of the recipient list (`src/commands/mail.ts:327`). Ordering is creation-time ascending for `check`/`getByThread` and descending for `list` (`src/mail/store.ts:222`, `src/mail/store.ts:226`, `src/mail/store.ts:262`). Priority never reorders storage; it only adds a display tag and triggers the nudge path (`src/mail/client.ts:104`, `src/commands/mail.ts:39`). Event recording is fire-and-forget throughout (send, broadcast, tailer insert all swallow DB failures) so observability loss never blocks messaging (`src/commands/mail.ts:442`, `src/events/tailer.ts:162`).
**Covers:** src/mail/store.ts, src/mail/client.ts, src/mail/broadcast.ts, src/commands/mail.ts, src/events/store.ts, src/events/tailer.ts, src/events/tool-filter.ts, .overstory/mail-check-state.json
