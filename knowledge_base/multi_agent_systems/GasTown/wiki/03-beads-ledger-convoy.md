> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Work Tracking: Beads Ledger, Convoys, Dolt Backend

**In one sentence:** GasTown tracks all work as beads (issues) in per-rig
Dolt (SQL database with version control) databases, groups them into convoys
that feed ready items to agents one at a time, and grinds stuck epics with
Mountain stall detection plus Reaper cleanup of temporary wisps.

## Key points
- A bead is the unit of work: `internal/beads/beads.go:176` defines `Issue`
  with `id, title, description, status, priority, issue_type, assignee,
  labels, parent, dependencies/dependents, metadata`, and IDs are
  `<prefix>-<suffix>` (e.g. `hq-cv-abc`), where the prefix routes to the
  owning rig database via `internal/beads/routes.go:252`.
- GasTown does not reimplement the ledger: `go.mod:18` depends on
  `github.com/steveyegge/beads v1.0.5`, and `internal/beads/store.go:57`
  opens it via `beadsdk.OpenFromConfig`; the local `Beads` wrapper
  (`internal/beads/beads.go:543`) either shells out to the `bd`
  command-line tool or uses in-process `beadsdk.Storage` to skip subprocess
  cost (`internal/beads/store.go:1`).
- GasTown registers its own vocabulary on top of beads: custom types
  `agent,role,rig,convoy,slot,queue,event,message,molecule,gate,merge-request`
  (`internal/constants/constants.go:185`), infra/ephemeral types
  `agent,role,message` (`internal/constants/constants.go:190`), and custom
  statuses `staged_ready,staged_warnings` (`internal/constants/constants.go:212`).
- A convoy is a bead of type `convoy` that links work with `tracks`
  dependencies: `internal/convoy/operations.go:94` finds tracking convoys via
  `GetDependentsWithMetadata` filtered to `tracks`, and
  `internal/convoy/operations.go:356` reads the tracked set via
  `GetDependenciesWithMetadata` filtered to `tracks` plus a fresh
  `GetIssuesByIDs` refresh.
- Convoy feeding is event-driven and guarded: on each close,
  `internal/convoy/operations.go:38` runs `gt convoy check`, skips closed
  (`internal/convoy/operations.go:113`) and staged
  (`internal/convoy/operations.go:124`) convoys, then
  `internal/convoy/operations.go:285` dispatches exactly one ready issue
  (open, unassigned, slingable type, unblocked) via `gt sling --no-boot`
  (`internal/convoy/operations.go:612`).
- A mountain is a convoy with the `mountain` label
  (`internal/witness/mountain.go:107`); each polecat failure on its hooked
  bead increments a `mountain:failures:N` label
  (`internal/witness/mountain.go:131`), and at `MountainMaxFailures = 3`
  (`internal/witness/mountain.go:22`) the issue is set `blocked` with
  `mountain:skipped` so feeding flows around it
  (`internal/witness/mountain.go:231`).
- Dolt is the storage backend: a central SQL server on port 3307
  (`internal/doltserver/doltserver.go:140`) serves one database per rig under
  `.dolt-data/` (`internal/doltserver/doltserver.go:19`), town beads live in
  `hq`, and ephemeral agent/operational rows live in a `wisps` table family
  created by `internal/doltserver/wisps_migrate.go:42`.
- The Reaper is SQL janitoring with no policy brain:
  `internal/reaper/reaper.go:308` scans counts,
  `internal/reaper/reaper.go:411` closes stale open wisps,
  `internal/reaper/reaper.go:566` purges old closed wisps and mail, and
  `internal/reaper/reaper.go:721` auto-closes stale durable issues while
  explicitly excluding `epic` and `convoy` types.
---
## Bead schema and ID format
The canonical struct is `Issue` in `internal/beads/beads.go:176`.
Identity fields are `ID`, `Title`.
Content fields are `Description`, `Design`, `Notes`, `AcceptanceCriteria`.
Workflow fields are `Status`, `Priority`, `Type` (`issue_type`), `Assignee`.
Graph fields are `Parent`, `Children`, `DependsOn`, `Blocks`, `BlockedBy`,
plus detailed `Dependencies` / `Dependents` of type `IssueDep`
(`internal/beads/beads.go:351`).
Extension fields are `Labels`, `Ephemeral`, `Metadata` (JSON blob),
`Comments`; agent slots are `HookBead`, `AgentState`
(`internal/beads/beads.go:176`).
Dependency relation names are normalized in `internal/beads/beads.go:392`:
blocking relations are `blocks, conditional-blocks, waits-for,
merge-blocks`; non-blocking are `tracks, parent-child, related,
discovered-from, thread`.
The `IssueDep` JSON parser accepts both `dependency_type` and `type` keys
for the relation (`internal/beads/beads.go:364`), keeping them distinct from
the bead's own `issue_type`.
ID format is prefix-routed: `internal/beads/routes.go:248` documents
`ExtractPrefix`, e.g. `hq-cv-abc` returns `hq-`, `ap-qtsup.16` returns `ap-`.
The implementation cuts at the first `-` (`internal/beads/routes.go:252`)
and returns empty on missing/leading hyphen.
`internal/beads/routes.go:269` maps a prefix to a rig directory via the
routes table (town-level `path="."` resolves to the town root).
`internal/convoy/multi_store.go:98` maps the same prefix to a store name
(`hq` for town-level, rig name otherwise).
Cross-rig references are wrapped as `external:<prefix>:<id>`
(`internal/beads/beads.go:151`); both `extractIssueID`
(`internal/convoy/operations.go:446`) and `ExtractIssueID` strip the wrapper
before display and store lookup.
Convoy pointers also ride in the description body (see next section).

## GasTown vs upstream beads
Upstream is a library dependency, not a fork: `go.mod:18` pins
`github.com/steveyegge/beads v1.0.5`, and all typed access goes through
`beadsdk.Storage` / `beadsdk.Issue`
(`internal/convoy/operations.go:14`, `internal/beads/store.go:16`).
GasTown adds two access paths around it.
The legacy path shells out to `bd` (`list/show/ready/dep/sql`) through
`internal/beads/beads.go:758`, with a 60s subprocess timeout
(`internal/beads/beads.go:744`), `--allow-stale` probing
(`internal/beads/beads.go:55`), `--flat` injection for JSON list output
(`internal/beads/beads.go:126`), and explicit `BEADS_DIR` pinning to defeat
inherited-env misrouting (`internal/beads/beads.go:935`).
The fast path attaches an in-process store to the wrapper
(`internal/beads/store.go:19`, `internal/beads/store.go:37`,
`internal/beads/beads.go:549`) and implements list/show/create/update/close/
ready/search against SDK calls (`internal/beads/store.go:276`,
`internal/beads/store.go:290`, `internal/beads/store.go:357`,
`internal/beads/store.go:482`), converting SDK types to local types in
`internal/beads/store.go:82` (notably `time.Time` to RFC3339 strings).
`internal/beads/store.go:57` (`OpenStore` via `beadsdk.OpenFromConfig`) is
the short-lived-command constructor; daemons keep persistent stores via
`SetStore` (`internal/beads/store.go:25`).
GasTown owns the vocabulary and routing on top: custom types/statuses are
enforced into each `.beads` dir via `bd config set` with sentinel caching
(`internal/beads/beads_types.go:103`, `internal/beads/beads_types.go:238`),
missing databases are bootstrapped with `bd init --server` plus `bd migrate`
(`internal/beads/beads_types.go:335`), and prefix routing resolves which
database an ID belongs to (`internal/beads/beads_types.go:57`).
Agent beads are special: they live in the town database regardless of ID
prefix, so `ForAgentBead` re-roots the wrapper and disables routing
(`internal/beads/beads.go:595`).

## Convoy data and lifecycle
A convoy is a bead whose type is `convoy` (one of the custom types at
`internal/constants/constants.go:185`) and whose membership edges are
`tracks` dependencies pointing at the tracked beads.
`internal/beads/fields.go:261` defines `ConvoyFields` verbatim:
`Owner`, `Notify`, `Molecule`, `Merge`, `BaseBranch`, `Watchers`,
`NudgeWatchers`, `CompletionNotifiedAt`, stored as `key: value` lines in the
convoy description and parsed by `internal/beads/fields.go:276`, which
accepts aliases (`base-branch`, `nudge-watchers`, `completion-notified-at`).
Notification fan-out reads owner/notify/watchers
(`internal/beads/fields.go:337`).
Lifecycle commands (`docs/skills/convoy/SKILL.md:96`,
`docs/concepts/convoy.md:8`):
`gt convoy create "<name>" <beads...>` makes one convoy tracking N beads;
batch `gt sling` does the same automatically with title
`Batch: N beads to <rig>` and one polecat per bead sharing the convoy
(`docs/skills/convoy/SKILL.md:145`); `gt convoy create --from-epic`
builds a standard `hq-cv-*` convoy over slingable children
(`docs/concepts/convoy.md:189`).
Stage/launch is the validated path: `gt convoy stage <epic|tasks|convoy>`
validates the graph, computes waves, and creates a convoy with status
`staged_ready` or `staged_warnings`
(`docs/skills/convoy/SKILL.md:204`); `gt convoy launch` flips staged to open
and dispatches Wave 1 (`docs/skills/convoy/SKILL.md:282`).
Staged convoys are inert by design: the event feeder skips `staged_*`
(`internal/convoy/operations.go:124`) and the stranded scan only sees open
convoys (`docs/skills/convoy/SKILL.md:294`).
Feed loop: `CheckConvoysForIssue` (`internal/convoy/operations.go:38`)
triggers on a close event, runs `gt convoy check <id>` as a subprocess
(`internal/convoy/operations.go:136`), then `feedNextReadyIssue`
(`internal/convoy/operations.go:285`) sorts tracked issues by priority then
ID (`internal/convoy/operations.go:300`), keeps only `open` plus unassigned
(`internal/convoy/operations.go:309`), keeps only slingable leaf types
`task,bug,feature,chore` (empty defaults to task) via `IsSlingableType`
(`internal/convoy/operations.go:163`), rejects blocked issues via
`isIssueBlocked` (`internal/convoy/operations.go:201`), resolves the target
rig from the ID prefix (`internal/convoy/operations.go:459`), skips parked
rigs, and dispatches one issue with `gt sling <id> <rig> --no-boot`
(`internal/convoy/operations.go:612`). Dispatch failure falls through to the
next candidate; success ends the cycle after exactly one dispatch.
Blocking semantics: `blockingDepTypes` are `blocks, conditional-blocks,
waits-for, merge-blocks`; `parent-child` is deliberately not blocking
(`internal/convoy/operations.go:181`). `merge-blocks` additionally requires
`CloseReason` starting with `Merged in `
(`internal/convoy/operations.go:196`, `internal/beads/beads.go:484`).
With a `StoreResolver`, stale snapshot statuses are re-verified in the home
store (`internal/convoy/operations.go:253`,
`internal/convoy/multi_store.go:73`); without one the snapshot is trusted
fail-open (`internal/convoy/operations.go:248`).
Cross-database reads: convoys usually live in `hq` while tracked beads live
in rigs, so IDs missing from the local store are resolved per-prefix either
by direct store queries (`internal/convoy/multi_store.go:37`) or legacy
`bd show --json` per rig (`internal/convoy/operations.go:471`); cross-rig
unblock events also nudge the owning rig's witness
(`internal/convoy/operations.go:535`).
Close/land: `gt convoy check` auto-closes when all tracked issues are done,
`gt convoy close` forces it, `gt convoy land` also cleans worktrees and
notifies (`docs/CLEANUP.md:109`).

## Mountain stall detection and smart skip
Definition: a mountain is a convoy bead carrying the `mountain` label; the
label alone opts the convoy into Layers 1-2, with no new entity or schema
(`docs/design/convoy/mountain-eater.md:95`,
`internal/witness/mountain.go:104`). Activation is stage, label, launch:
`gt convoy stage`, `bd update <convoy> --add-label mountain`,
`gt convoy launch` (`docs/design/convoy/mountain-eater.md:101`).
Layer 1 — witness failure tracking (implemented):
`trackConvoyFailures` (`internal/witness/mountain.go:39`) runs after
zombie-polecat detection; for each zombie with a non-empty `HookBead` that
implies active failure (`internal/witness/mountain.go:77`, excluding
already-closed/submitted cases), it calls `TrackConvoyFailure`
(`internal/witness/mountain.go:93`).
Lookup is CLI-based: tracking convoys via
`bd dep list <issue> --direction=up --type=tracks --json`
(`internal/witness/mountain.go:157`), convoy and issue labels via
`bd show --json` (`internal/witness/mountain.go:178`), exact match on
`mountain` (`internal/witness/mountain.go:193`).
Non-mountain convoys only get a stderr warning
(`internal/witness/mountain.go:118`). Mountain convoys call
`trackMountainFailure` (`internal/witness/mountain.go:131`): read the count
from `mountain:failures:N` (`internal/witness/mountain.go:206`), replace
`mountain:failures:<old>` with `mountain:failures:<new>` via
`bd update --remove-label/--add-label`
(`internal/witness/mountain.go:219`), and when
`newCount >= MountainMaxFailures` (`internal/witness/mountain.go:144`)
run the skip.
Skip command verbatim: `bd update <issue> --status=blocked --add-label
mountain:skipped --notes "Skipped by Mountain-Eater after N polecat
failures"` (`internal/witness/mountain.go:231`). Blocked status drops the
issue from the ready front so the convoy grinds around it; recovery is
`bd update --status=open --remove-label mountain:skipped`
(`docs/design/convoy/mountain-eater.md:176`). Only the first tracking convoy
is processed per call (`internal/witness/mountain.go:121`).
Layer 2 — deacon Dog audit (design): patrol lists
`bd list --label mountain --status=open --type=convoy`, compares
closed-count against a `mountain:audit:<convoy-id>` mark on the deacon bead,
and slings a short-lived `mountain-dog` formula with task `stall` or
`complete` when there is no progress
(`docs/design/convoy/mountain-eater.md:192`). The Dog investigates skipped
issues, cross-rig blocks, and orphaned work, then mails the Mayor
(`docs/design/convoy/mountain-eater.md:299`). Roadmap status and CLI surface
(`gt mountain`, `mountain status/pause/resume/cancel`) are tracked in
`docs/design/convoy/roadmap.md:270`.

## Dolt backend and sync
Dolt (a MySQL-compatible versioned database) is the durable store behind
`bd`: GasTown runs one SQL server (default port 3307, user `root`) whose
data dir holds one database per rig (`internal/doltserver/doltserver.go:140`,
`internal/doltserver/doltserver.go:288`). This avoids embedded single-writer
limits (`internal/doltserver/doltserver.go:1`). Layout is
`~/gt/.dolt-data/<hq|rig>/` (`internal/doltserver/doltserver.go:19`).
Liveness combines PID file, `sql-server.info`, port probe, and TCP
reachability (`internal/doltserver/doltserver.go:698`); `WaitForReady` gates
agent start on the server (`internal/doltserver/doltserver.go:794`).
`gt dolt start/stop/status/logs/sql/init-rig` manage it
(`internal/doltserver/doltserver.go:19`). Timeouts are tuned for agent load:
30s idle `wait_timeout` (`internal/doltserver/doltserver.go:169`), 5min
read/write timeouts (`internal/doltserver/doltserver.go:147`), UTC timezone
(`internal/doltserver/doltserver.go:179`).
Sync is Dolt push per database with `--force`/dry-run/single-DB filter
(`internal/doltserver/sync.go:15`); remote discovery uses `dolt remote -v`
(`internal/doltserver/sync.go:45`).
Schema split: durable work lives in `issues` plus
`labels/comments/events/dependencies`; ephemeral operational rows (agent
beads, patrol/molecule scratch) live in `wisps` plus
`wisp_labels/wisp_comments/wisp_events/wisp_dependencies`, described as a
`dolt_ignored` copy of the issues schema
(`internal/doltserver/wisps_migrate.go:1`). Migration
(`internal/doltserver/wisps_migrate.go:42`) copies `issue_type='agent'` rows
issues-to-wisps with labels/comments/events/dependencies, then closes the
originals (`internal/doltserver/wisps_migrate.go:284`,
`internal/doltserver/wisps_migrate.go:301`,
`internal/doltserver/wisps_migrate.go:653`), and ensures the tables exist on
both the `bd` database and the `gt` server because the Reaper connects to
the latter (`internal/doltserver/wisps_migrate.go:75`,
`internal/doltserver/wisps_migrate.go:380`).
Representative DDL: `wisps(id, title, description, status, priority,
issue_type, assignee, hook_bead, agent_state, rig, created_at, updated_at,
closed_at, ephemeral, wisp_type, ...)` with status/type indexes
(`internal/doltserver/wisps_migrate.go:512`); dependency tables use split
targets `depends_on_issue_id/depends_on_wisp_id/depends_on_external` with a
one-target check constraint (`internal/doltserver/wisps_migrate.go:581`).
On-disk, the repo's own `.beads/` holds `config.yaml` (with `types.custom`,
`external_projects`, `issue-prefix`, sync remote) plus `backup/*.jsonl`
(`issues, dependencies, labels, comments, events`); `metadata.json` with
`dolt_mode: server` marks server-backed databases
(`internal/beads/beads_types.go:356`).

## Reaper and wisp cleanup
The Reaper (`internal/reaper/reaper.go:1`) is explicitly helper SQL without
eligibility judgment; the Dog/daemon decides, the Reaper executes.
Discovery lists databases via `SHOW DATABASES`, skipping system and test
names (`internal/reaper/reaper.go:54`), falling back to `hq`
(`internal/reaper/reaper.go:29`); names are validated
(`internal/reaper/reaper.go:172`) and connections use MySQL DSNs
(`internal/reaper/reaper.go:181`).
Scan (`internal/reaper/reaper.go:308`) counts disjoint classes, e.g.:
`SELECT COUNT(*) FROM wisps w ... WHERE <open-ish> AND w.created_at < ? AND
w.issue_type != 'agent' AND <no-open-parent>` for reap candidates
(`internal/reaper/reaper.go:331`); `w.status='closed' AND closed_at < ?` for
purge (`internal/reaper/reaper.go:342`); closed `gt:message` mail
(`internal/reaper/reaper.go:350`); stale durable issues excluding
`epic/convoy` and dependency-guarded rows (`internal/reaper/reaper.go:362`).
Open-parent exclusion uses one `LEFT JOIN` anti-join instead of correlated
`EXISTS` subqueries (`internal/reaper/reaper.go:210`).
Reap (`internal/reaper/reaper.go:411`) batch-closes (`DefaultBatchSize =
100`, `internal/reaper/reaper.go:159`) open/hooked/in-progress wisps
(`internal/reaper/reaper.go:222`) whose parent is closed/missing and whose
age exceeds max-age, plus immediate close of steps whose parent molecule
closed (`internal/reaper/reaper.go:226`); agent rows are never reaped
(`internal/reaper/reaper.go:424`). Updates run as
`UPDATE wisps SET status='closed', closed_at=NOW() WHERE id IN (...)`
(`internal/reaper/reaper.go:552`).
Purge (`internal/reaper/reaper.go:566`) batch-deletes closed wisps past
purge-age with aux tables (`internal/reaper/reaper.go:634`) and old closed
mail (`internal/reaper/reaper.go:663`), cleaning reverse dependency refs
(`internal/reaper/reaper.go:888`); every mutation commits via `COMMIT`
then `CALL DOLT_COMMIT` (`internal/reaper/reaper.go:493`).
AutoClose (`internal/reaper/reaper.go:721`) closes `open/in_progress`
durable issues past stale-age with `priority > 1`, excluding `epic/convoy`
(convoy lifecycle is tracked-status driven, never staleness driven),
protected labels (`gt:standing-orders/gt:keep/gt:role/gt:rig`), and both
directions of live dependencies; it writes
`close_reason = 'stale:auto-closed by reaper'`
(`internal/reaper/reaper.go:816`). Extra closers handle `type:plugin-run`
receipts (`internal/reaper/reaper.go:933`) and daemon plugin dispatches
(`gt:message` + `from:daemon`, title `Plugin:`)
(`internal/reaper/reaper.go:1017`). The open-wisp alert threshold is 3000,
set above healthy steady-state to avoid false alarms
(`internal/reaper/reaper.go:155`).

**Covers:** internal/beads (beads.go, beads_types.go, fields.go, routes.go,
store.go), internal/convoy (operations.go, multi_store.go),
internal/doltserver (doltserver.go, sync.go, wisps_migrate.go),
internal/witness (mountain.go), internal/reaper (reaper.go), .beads/config.yaml
+ backup, docs/skills/convoy/SKILL.md, docs/concepts/convoy.md,
docs/design/convoy/mountain-eater.md, docs/design/convoy/roadmap.md,
docs/CLEANUP.md, go.mod
