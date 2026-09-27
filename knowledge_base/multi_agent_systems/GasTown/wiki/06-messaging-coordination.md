> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Messaging and Coordination: Mail, Events, Handoffs

**In one sentence:** Agents communicate through durable mail beads stored in Dolt (a version-controlled SQL database) plus file-based events and protocol mail, with handoffs as self-addressed mail for session continuity.

## Key points
- Mail is durable beads issues with label `gt:message`: send runs `bd create --assignee`, receive queries by assignee and CC labels, read closes the bead or adds a `read` label (`internal/mail/router.go:1138`, `internal/mail/mailbox.go:146`).
- Every message routes to exactly one of direct address, queue, or channel, enforced by validation (`internal/mail/types.go:243`).
- Two-phase delivery tracks `delivery:pending` at send and `delivery:acked` plus acker identity and timestamp after the recipient reads (`internal/mail/delivery.go:12`).
- `mq` is not transport: it only generates merge-request identifiers (`<prefix>-mr-<10-hex>` from branch plus timestamp plus randomness) while `mail` carries the actual coordination traffic (`internal/mq/id.go:22`, `internal/mail/router.go:863`).
- Witness-Refinery coordination uses subject-prefixed protocol mail (`MERGE_READY`, `MERGED`, `FIX_NEEDED`, `REWORK_REQUEST`, `CONVOY_NEEDS_FEEDING`) with line-based `Key: value` bodies parsed by strict field parsers (`internal/protocol/types.go:60`, `internal/protocol/messages.go:517`).
- Handoffs are high-priority self-mail set to status `hooked` so the successor session auto-loads them, with stale hooked beads closed before each new handoff (`internal/cmd/handoff.go:1343`, `internal/beads/handoff.go:193`).
- Raw audit events (`~/gt/.events.jsonl`), curated user feed (`~/gt/.feed.jsonl`), human-readable town lifecycle log (`town/logs/town.log`), per-agent conversation telemetry (`agentlog`), and dashboard staleness colors (`activity`) are five separate record systems (`internal/events/events.go:110`, `internal/feed/curator.go:356`, `internal/townlog/logger.go:68`, `internal/agentlog/event.go:16`, `internal/activity/activity.go:37`).
- Shared-file conflicts are never auto-merged: the refinery rehearsal aborts on conflict, preserves the branch and merge-request bead, and files a conflict-resolution task or requests a polecat rebase (`internal/formula/formulas/mol-refinery-patrol.formula.toml:379`).

---
## Message schema

The in-memory message (`internal/mail/types.go:64`) is:

```go
type Message struct {
    ID string `json:"id"`
    From string `json:"from"`
    To string `json:"to"`
    Subject string `json:"subject"`
    Body string `json:"body"`
    Timestamp time.Time `json:"timestamp"`
    Read bool `json:"read"`
    Priority Priority `json:"priority"`
    Type MessageType `json:"type"`
    Delivery Delivery `json:"delivery,omitempty"`
    ThreadID string `json:"thread_id,omitempty"`
    ReplyTo string `json:"reply_to,omitempty"`
    Pinned bool `json:"pinned,omitempty"`
    Wisp bool `json:"wisp,omitempty"`
    CC []string `json:"cc,omitempty"`
    Queue string `json:"queue,omitempty"`
    Channel string `json:"channel,omitempty"`
    ClaimedBy string `json:"claimed_by,omitempty"`
    ClaimedAt *time.Time `json:"claimed_at,omitempty"`
    DeliveryState string `json:"delivery_state,omitempty"`
    DeliveryAckedBy string `json:"delivery_acked_by,omitempty"`
    DeliveryAckedAt *time.Time `json:"delivery_acked_at,omitempty"`
    SuppressNotify bool `json:"-"`
}
```

Priorities are `low`, `normal`, `high`, `urgent` (`internal/mail/types.go:15`). Types are `task`, `escalation`, `scavenge`, `notification`, `reply` (`internal/mail/types.go:32`). Delivery modes are `queue` (agent polls with `gt mail check`) and `interrupt` (inject a system reminder into the live session) (`internal/mail/types.go:52`). Constructors cover direct mail, replies inheriting `ThreadID`, queue tasks defaulting to `TypeTask`, and channel broadcasts (`internal/mail/types.go:143`, `internal/mail/types.go:159`, `internal/mail/types.go:177`, `internal/mail/types.go:194`). Validation requires a non-empty ID, From, Subject, and exactly one routing target among To, Queue, Channel (`internal/mail/types.go:243`).

On disk the message is a beads issue (`internal/mail/types.go:299`): title holds the subject, description holds the body, assignee holds the recipient identity, integer priority maps 0 to urgent, 1 to high, 2 to normal, 3 to low, status `open` means unread and `closed` means read, and labels carry `from:`, `thread:`, `reply-to:`, `msg-type:`, `cc:`, `queue:`, `channel:`, `claimed-by:`, `claimed-at:` plus delivery labels (`internal/mail/types.go:329`, `internal/mail/types.go:387`, `internal/mail/types.go:491`). Address conversion normalizes crew and polecat path segments, town singletons `mayor/` and `deacon/`, and the human operator `overseer` (`internal/mail/types.go:554`, `internal/mail/types.go:604`).

## Mailbox storage and operations

A `Mailbox` binds one beads identity plus working directory and optional beads directory, with an optional in-process store that bypasses the `bd` subprocess (`internal/mail/mailbox.go:37`, `internal/mail/store.go:24`). Legacy crew-worker mode uses local JSON Lines (JSONL, one JSON object per line) `inbox.jsonl` with file locking (flock, an OS-level file lock); beads mode is the current path (`internal/mail/mailbox.go:52`, `internal/mail/mailbox.go:60`).

List queries beads in three parallel fetches: by assignee, by `cc:<identity>`, and a SQL query against the ephemeral `wisps` table, then deduplicates and sorts by priority then newest first (`internal/mail/mailbox.go:146`, `internal/mail/mailbox.go:205`, `internal/mail/mailbox.go:230`, `internal/mail/mailbox.go:312`). The in-process fast path instead calls `SearchIssues` filtered by `gt:message` label and assignee (`internal/mail/store.go:60`). Both `open` and `hooked` statuses are returned; `hooked` means auto-assigned handoff or work-assignment mail (`internal/mail/mailbox.go:141`). Conversion from storage issues to messages always goes through label parsing (`internal/mail/store.go:233`).

Read operations are: `Get` by bead ID via `bd show` with cross-database fallback for cross-rig prefixes (`internal/mail/mailbox.go:502`); `MarkRead` closes the bead via `bd close` (`internal/mail/mailbox.go:570`); `MarkReadOnly` adds a `read` label without closing (`internal/mail/mailbox.go:654`); `MarkUnreadOnly` removes that label (`internal/mail/mailbox.go:726`); `MarkUnread` reopens (`internal/mail/mailbox.go:776`); `Delete` in beads mode is close, not erase (`internal/mail/mailbox.go:845`); `Archive` appends the JSON message to `archive.jsonl` then closes (`internal/mail/mailbox.go:888`); `Search` scans inbox plus archive with literal case-insensitive matching (`internal/mail/mailbox.go:1123`); `Count` and `ListUnread` derive unread state from the `Read` flag including the `read` label (`internal/mail/mailbox.go:1190`, `internal/mail/mailbox.go:487`); `ListByThread` filters by thread label (`internal/mail/mailbox.go:1341`). All subprocess calls run `bd` with 60-second read and write timeouts (`internal/mail/bd.go:15`).

Two-phase delivery writes `delivery:pending` at send (`internal/mail/delivery.go:27`, `internal/mail/router.go:235`). On read, the recipient writes `delivery-acked-by:<identity>`, `delivery-acked-at:<RFC3339-timestamp>`, and `delivery:acked`, then removes `pending` once `acked` is durable; retries reuse the same timestamp for the same recipient to stay idempotent (`internal/mail/delivery.go:48`, `internal/mail/delivery.go:84`, `internal/mail/delivery.go:151`). Parsing is order-independent with last-wins for acker fields, and `acked` wins over `pending` (`internal/mail/delivery.go:218`). Bulk reads ack concurrently bounded to 8 workers (`internal/mail/mailbox.go:1212`).

## Send-to-receive walkthrough

Send entry `Router.Send` dispatches on address prefix: `list:` fans out per member, `queue:` single-copy claimable, `announce:` single-copy bulletin board, `channel:` broadcast plus per-subscriber fan-out, `@group` resolves then fans out, otherwise single direct send (`internal/mail/router.go:863`). The router object holds working directory, town root, and tmux handle (`internal/mail/router.go:41`). All mail lands in town-level beads (`{townRoot}/.beads`); rig-level beads hold project issues only (`internal/mail/router.go:218`).

Direct send validates the message, normalizes addresses, expands crew shorthand, validates the recipient against agent beads and workspace directories, builds labels, then runs `bd create --assignee <identity> -d <body> --priority <0-3> --labels <csv> --actor <sender> -- <subject>` with `--` guarding subjects that look like flags (`internal/mail/router.go:1113`). Lifecycle subjects such as polecat start and done, nudges, and merge notices are auto-marked ephemeral (wisp: stored in the same database but not synced to git); handoff mail is explicitly not ephemeral so hooks can find it (`internal/mail/router.go:830`, `internal/cmd/handoff.go:1313`). After the durable write, notification is asynchronous: self-mail is skipped, otherwise a goroutine notifies and the caller can block with `WaitPendingNotifications` (`internal/mail/router.go:1200`).

Notification is idle-aware against tmux sessions (`internal/mail/router.go:1592`): if the session shows an idle prompt within the timeout (default 3 seconds, `internal/mail/router.go:35`), the router types a nudge directly; if busy, it enqueues a queued nudge for cooperative delivery at the next turn boundary; the human `overseer` gets a banner instead of typed input (`internal/mail/router.go:1655`, `internal/mail/router.go:1644`). A deferred reply-reminder nudge is also queued (`internal/mail/router.go:1600`).

Queue send creates one bead with assignee `queue:<name>` and `queue:<name>` label after validating the queue exists in messaging config; workers claim it and no notification is sent (`internal/mail/router.go:1256`). Announce send creates one bead with assignee `announce:<name>`, prunes oldest entries to the configured retain count before insert, and omits delivery tracking because broadcasts have no single acker (`internal/mail/router.go:1329`, `internal/mail/router.go:1524`). Channel send validates the channel bead, rejects closed channels, writes one origin copy with `channel:<name>` label, enforces retention, then fans out per-subscriber copies prefixed `[channel:<name>]` through the normal single-send path which re-adds delivery tracking (`internal/mail/router.go:1414`, `internal/mail/router.go:1495`).

Address resolution order is: explicit `group:`/`queue:`/`channel:` prefix, legacy `list:`/`announce:` passthrough, `@` patterns, slash-containing agent addresses, then bare-name lookup in group, queue, channel order with ambiguity errors requiring an explicit prefix (`internal/mail/resolve.go:58`, `internal/mail/resolve.go:281`). Slash addresses support wildcards such as `*/witness` expanded against agent beads (`internal/mail/resolve.go:216`). Group members recurse with cycle detection and deduplication (`internal/mail/resolve.go:401`). Built-in `@` groups include `@town`, `@witnesses`, `@dogs`, `@refineries`, `@rig/<name>`, `@crew/<rig>`, `@polecats/<rig>`, `@overseer` (`internal/mail/router.go:299`).

## mq versus mail

`mq` (merge queue) is only identifier generation: `GenerateMRID(prefix, branch)` hashes branch plus nanosecond timestamp plus 8 random bytes with SHA-256 (Secure Hash Algorithm) and formats `<prefix>-mr-<10-hex-chars>` (`internal/mq/id.go:22`, `internal/mq/id.go:45`). Mail is the transport: durable beads, routing, fan-out, queues, channels, delivery tracking, and tmux nudges described above (`internal/mail/router.go:863`). The merge pipeline itself (refinery picking up merge-request beads) is driven by protocol mail and beads queries, not by the `mq` package (`internal/protocol/refinery_handlers.go:52`).

## Events, channel events, and feed

Raw activity events are JSONL rows `{ts, source, type, actor, payload, visibility}` appended under a cross-process file lock to `{townRoot}/.events.jsonl` (`internal/events/events.go:19`, `internal/events/events.go:110`, `internal/events/events.go:80`). Visibility is `audit` (raw log only), `feed` (curated feed), or `both` (`internal/events/events.go:30`). Types include sling, hook, unhook, handoff, done, mail, spawn, kill, nudge, boot, halt, session start and end, session death and mass death, witness patrol and escalation transitions, merge started/merged/failed/skipped, and scheduler enqueue/dispatch/failure (`internal/events/events.go:36`). Helpers build payloads such as sling bead plus target, mail recipient plus subject, and merge-request plus worker plus branch plus reason (`internal/events/events.go:154`, `internal/events/events.go:188`, `internal/events/events.go:216`).

Channel events are a separate mechanism for named pub-sub signals (publish-subscribe: one writer, many watchers): JSON files `{type, channel, timestamp, payload}` written to `events/<channel>/<nanotime>-<seq>-<pid>.event`, consumed by waiters such as the refinery watching `MERGE_READY` (`internal/channelevents/channelevents.go:1`, `internal/channelevents/channelevents.go:64`). Channel names are restricted to letters, digits, dash, underscore to block path traversal (`internal/channelevents/channelevents.go:23`). Explicit-town-root and cwd-resolved emit variants exist (`internal/channelevents/channelevents.go:31`, `internal/channelevents/channelevents.go:51`).

The feed curator tails the raw events file, drops audit-only rows, dedupes, aggregates, and appends human summaries to `{townRoot}/.feed.jsonl` (`internal/feed/curator.go:1`, `internal/feed/curator.go:156`). Feed rows are `{ts, source, type, actor, summary, payload, count}` (`internal/feed/curator.go:32`). Repeat `done` events from one actor inside the dedupe window are dropped; sling bursts above the aggregate threshold collapse into one `dispatching work to N agents` entry (`internal/feed/curator.go:183`, `internal/feed/curator.go:340`). State is derived from the files, not memory, and reads are tail-bounded to 1 MB; the feed file truncates to its newest half past 10 MB (`internal/feed/curator.go:216`, `internal/feed/curator.go:205`).

## Handoffs between agents

Two handoff mechanisms coexist. Session-cycle handoff mail is self-addressed durable mail whose subject contains `HANDOFF:` and whose body carries freeform context, status, and next steps plus optional attached molecule (a work-unit bead) metadata (`docs/design/mail-protocol.md:204`, `internal/templates/messages/handoff.md.tmpl:1`). Creation uses `bd create --assignee <self> --priority 1 --labels from:<self>,gt:message`, then `bd update <id> --status=hooked --assignee=<self>` so the successor auto-loads it; stale hooked beads from prior cycles are closed first to avoid accumulation (`internal/cmd/handoff.go:1306`, `internal/cmd/handoff.go:1343`, `internal/beads/handoff.go:193`). Default subject is session cycling when none is given (`internal/cmd/handoff.go:1262`). Because handoff must survive in the issues table for hook queries, it is never ephemeral (`internal/cmd/handoff.go:1313`).

Role handoff beads are a second, pinned-bead mechanism: one pinned bead titled `<role> Handoff` per role, created on demand and updated in place (`internal/beads/handoff.go:26`, `internal/beads/handoff.go:70`, `internal/beads/handoff.go:106`). Reads treat `hooked` mail as inbox-visible, which is how successor sessions discover both handoff mail and hooked work (`internal/mail/mailbox.go:141`). Signal-stop handling filters self-handoff mail out of blocking checks to avoid restart loops (`internal/cmd/signal_stop.go:123`).

Polecat completion uses a related but distinct chain:
- `gt done` emits `POLECAT_DONE <name>` with `Exit/Issue/MR/Branch` fields (`docs/design/mail-protocol.md:12`);
- the witness verifies and emits `MERGE_READY` (`docs/design/mail-protocol.md:32`);
- the refinery merges and emits `MERGED` (`internal/protocol/witness_handlers.go:103`);
- failures emit `FIX_NEEDED` or `REWORK_REQUEST` instead (`internal/protocol/messages.go:138`, `internal/protocol/messages.go:229`).
Recovery paths use `RECOVERED_BEAD` for abandoned work reset to open and `RECOVERY_NEEDED` for dirty work needing manual rescue (`docs/design/mail-protocol.md:131`, `docs/design/mail-protocol.md:161`).

## Protocol messages: format and handlers

Protocol detection parses the subject prefix before the first space (`MERGE_READY`, `MERGED`, `MERGE_FAILED`, `FIX_NEEDED`, `REWORK_REQUEST`, `CONVOY_NEEDS_FEEDING`) (`internal/protocol/types.go:60`). Bodies are line-based `Key: value` pairs parsed by a shared prefix scanner (`internal/protocol/messages.go:517`). Payload structs require Branch, Polecat, Rig (plus ConvoyID and Rig for convoy feeding); missing fields are errors except best-effort `POLECAT_DONE` parsing (`internal/protocol/types.go:85`, `internal/protocol/messages.go:186`, `internal/protocol/messages.go:324`, `internal/protocol/messages.go:496`).

Directions are fixed: witness to refinery `MERGE_READY <polecat>` as high-priority task with branch, issue, polecat, rig, verified notes (`internal/protocol/messages.go:13`); refinery to witness `MERGED <polecat>` as notification with target branch, merge time, and commit SHA (SHA: commit hash) (`internal/protocol/messages.go:52`); legacy refinery to witness `MERGE_FAILED <polecat>` for test and build failures (`internal/protocol/messages.go:94`); replacement refinery directly to polecat `FIX_NEEDED <polecat>` with failure type, error text, merge-request bead, and attempt number so the worker fixes in place (`internal/protocol/messages.go:138`); refinery to witness `REWORK_REQUEST <polecat>` with conflict file list and fetch plus rebase plus force-push instructions (`internal/protocol/messages.go:229`, `internal/protocol/messages.go:276`); refinery to deacon `CONVOY_NEEDS_FEEDING <convoy>` with convoy ID, source issue, rig, merge time (`internal/protocol/messages.go:290`). `POLECAT_DONE` additionally carries exit type, merge-request ID, convoy ID, owned flag, and merge strategy, with owned plus direct convoys skipping the merge pipeline (`internal/protocol/types.go:224`, `internal/protocol/types.go:255`).

Handlers dispatch by parsed subject through a registry returning handled versus not-protocol versus no-handler states (`internal/protocol/handlers.go:38`, `internal/protocol/handlers.go:134`). The witness implementation notifies the polecat and auto-nukes clean worktrees on `MERGED`, forwards failures and rebase instructions on failure and rework, and skips merge registration for owned plus direct convoys (`internal/protocol/witness_handlers.go:48`, `internal/protocol/witness_handlers.go:85`, `internal/protocol/witness_handlers.go:103`, `internal/protocol/witness_handlers.go:151`). The refinery implementation acknowledges `MERGE_READY` and relies on direct beads queries for merge-request beads rather than a separate queue file (`internal/protocol/refinery_handlers.go:52`).

## agentlog, townlog, activity, feed: what each records

`agentlog` tails per-agent model conversation logs and emits normalized telemetry events `{agentType, sessionID, nativeSessionID, eventType, role, content, timestamp}` plus token counts on `usage` turns; event kinds are text, tool use, tool result, thinking, usage (`internal/agentlog/event.go:16`). The Claude Code adapter watches `~/.claude/projects/<dir-hash>/<session-uuid>.jsonl`, picks the newest file after session start, and auto-switches when a new session file appears (`internal/agentlog/claudecode.go:27`, `internal/agentlog/claudecode.go:52`). The OpenCode adapter is a stub returning not-implemented (`internal/agentlog/opencode.go:18`).

`townlog` records agent lifecycle in human-readable lines `YYYY-MM-DD HH:MM:SS [type] agent detail` at `{townRoot}/logs/town.log` (`internal/townlog/logger.go:117`, `internal/townlog/logger.go:68`). Event types are spawn, wake, nudge, handoff, done, crash, kill, handoff-no-persist, callback, patrol started plus checked plus nudged, escalation sent, patrol complete, session death, mass death (`internal/townlog/logger.go:15`). Readers support full read, tail-N, and filter by type, agent prefix, and time (`internal/townlog/logger.go:235`, `internal/townlog/logger.go:343`, `internal/townlog/logger.go:363`).

`activity` computes dashboard staleness only: green under 5 minutes, yellow 5 to 10 minutes, red over 10 minutes, unknown for zero time, with short age strings such as `<1m`, `5m`, `2h`, `1d` (`internal/activity/activity.go:18`, `internal/activity/activity.go:37`, `internal/activity/activity.go:68`).
Helpers report `IsActive`, `IsStale`, and `IsStuck` from the same color class (`internal/activity/activity.go:126`).
Future timestamps from clock skew are clamped to zero duration (`internal/activity/activity.go:53`).

The raw events log, curated feed, town lifecycle log, agent conversation telemetry, and activity colors therefore answer different questions:
- audit trail: what happened for every command (`internal/events/events.go:85`);
- human feed: what should an operator read (`internal/feed/curator.go:356`);
- lifecycle: how each agent spawned, nudged, handed off, crashed (`internal/townlog/logger.go:80`);
- model telemetry: what each model session said and spent (`internal/agentlog/event.go:35`);
- health: which agents look stuck right now (`internal/activity/activity.go:126`).

## Delivery addresses, copies, and retention

Direct addresses look like `rig/name`, `rig/crew/name`, `rig/polecats/name`, `rig/witness`, `rig/refinery`, `mayor/`, `deacon/`, `deacon/dogs/<name>`, and `overseer` (`internal/mail/types.go:591`, `internal/mail/dog_address.go:12`). Canonicalization strips the crew and polecat path segments so `gastown/crew/max` and `gastown/max` match the same inbox (`internal/mail/types.go:584`). Town singletons `mayor` and `deacon` accept forms with and without trailing slash; rig witness and refinery inboxes are always valid even without an active session so mail queues for the next run (`internal/mail/router.go:939`, `internal/mail/router.go:950`).

Carbon copy (CC, extra recipients who get a copy without being the main assignee) is stored as repeated `cc:<identity>` labels and returned by inbox queries alongside direct assignee matches (`internal/mail/types.go:353`, `internal/mail/mailbox.go:230`). Queue mode stores one bead addressed to `queue:<name>` with a `queue:<name>` label for claiming; announce mode stores one bead addressed to `announce:<name>` with an `announce:<name>` label and no claiming (`internal/mail/router.go:1256`, `internal/mail/router.go:1329`). Channel mode stores one origin copy plus one fan-out copy per subscriber; closed channels reject sends and retention runs on every write (`internal/mail/router.go:1414`, `internal/mail/router.go:1491`).

Ephemeral wisps share the same database but carry the ephemeral flag and skip git sync; they auto-clean on patrol squash (`internal/mail/types.go:105`, `internal/mail/router.go:1164`). Protocol and lifecycle subjects are auto-detected as wisps by lowercase prefix match (`internal/mail/router.go:830`). Pinned mail is excluded from auto-archive (`internal/mail/types.go:102`).

## Edge cases in receive and notify

Recipient validation checks town singletons, rig witness and refinery, dog addresses, agent beads across town and rig databases via routing tables, and finally workspace directories as fallback when the database was reset (`internal/mail/router.go:932`, `internal/mail/router.go:1012`). Unknown slash addresses fail instead of delivering to a dead inbox (`internal/mail/resolve.go:112`). Crew shorthand such as `crew/bob` is expanded by scanning rig directories, but only when exactly one rig matches (`internal/mail/router.go:1065`).

Inbox sorting is priority first then newest first; thread views sort oldest first (`internal/mail/mailbox.go:128`, `internal/mail/mailbox.go:1371`). Cross-rig bead IDs resolve their database by ID prefix, with fallback to town beads for router-created mail (`internal/mail/mailbox.go:511`, `internal/mail/mailbox.go:584`). Mailbox reads resolve mayor and deacon identity variants with and without trailing slash for backward compatibility (`internal/mail/mailbox.go:430`). Suppressed-notify sends skip tmux nudges entirely (`internal/mail/router.go:1200`).

Channel name validation, per-subscriber skip for self-mail, reply-reminder cleanup by thread, muted-session checks, and multi-session fan-out for canonical aliases all prevent loops and lost copies (`internal/channelevents/channelevents.go:23`, `internal/mail/router.go:1498`, `internal/mail/router.go:1870`, `internal/mail/router.go:1623`).

## Merge and conflict strategy for shared files

There is no three-way auto-merge of conflicting edits. The refinery rehearses each polecat branch merge; on conflict it aborts immediately so the repository never stays conflicted, records target and branch SHAs, files a `Resolve merge conflicts` task bead with merge-without-rewriting-history instructions, leaves the branch and merge-request bead open, and moves to the next branch (`internal/formula/formulas/mol-refinery-patrol.formula.toml:377`, `internal/formula/formulas/mol-refinery-patrol.formula.toml:418`).
Conflicted branches are never deleted (`internal/formula/formulas/mol-refinery-patrol.formula.toml:418`).
Conflict detection checks for `.git/MERGE_HEAD` after a failed rehearsal (`internal/formula/formulas/mol-refinery-patrol.formula.toml:366`).
The polecat path is rebase onto the target then force-push and resubmit via `gt done`, delivered as `REWORK_REQUEST` mail through the witness (`internal/protocol/witness_handlers.go:223`, `internal/protocol/messages.go:276`).
Bead-level races use per-bead advisory file locks for read-modify-write attach and detach (`internal/beads/handoff.go:233`).

**Covers:** internal/mail, internal/mq, internal/events, internal/channelevents, internal/feed, internal/activity, internal/agentlog, internal/townlog, internal/protocol
