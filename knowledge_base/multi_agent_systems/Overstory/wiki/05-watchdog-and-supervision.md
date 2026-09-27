> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Tiered Watchdog and Worker Supervision
**In one sentence:** Overstory supervises workers through a three-tier watchdog — T0 (Tier 0, mechanical daemon) polling tmux (terminal multiplexer) and PID (process identifier) liveness with progressive 4-level escalation, T1 (Tier 1, ephemeral AI triage) classifying stalled agents via log analysis, and T2 (Tier 2, persistent monitor agent) patrolling the fleet — backed by ZFC (Zero Failure Crash: observable state wins over recorded state) health checks, SQLite (structured query language database) session store, and checkpoint/handoff files for resume.
## Key points
- T0 mechanical daemon (`runDaemonTick` / `startDaemon`) polls every `intervalMs` (default 30000ms via `ov watch`), skips `completed` sessions, re-checks zombies every tick, and never crashes on per-tick errors (`src/watchdog/daemon.ts:397-405`, `src/watchdog/daemon.ts:338-357`, `src/commands/watch.ts:127-129`).
- Health evaluation follows ZFC (Zero Failure Crash): tmux/PID liveness outranks `sessions.db` recorded state; tmux-dead means `terminate`, tmux-alive-plus-recorded-zombie means `investigate` (hold, never auto-kill) (`src/watchdog/health.ts:4-31`, `src/watchdog/health.ts:256-285`).
- Escalation is progressive across 4 levels gated by `nudgeIntervalMs` (default 60000ms): L0 warn, L1 tmux nudge, L2 AI triage (only if `tier1Enabled`), L3 terminate; recovery resets `escalationLevel`/`stalledSince` (`src/watchdog/daemon.ts:8-12`, `src/watchdog/daemon.ts:569-608`, `src/watchdog/daemon.ts:703-803`).
- T1 triage reads the last 50 lines of the newest `session.log`, prompts a print-command runtime model for exactly one word (`retry`/`terminate`/`extend`), defaults to `extend` when logs or model are missing, with a 30s subprocess timeout (`src/watchdog/triage.ts:29-58`, `src/watchdog/triage.ts:94-99`, `src/watchdog/triage.ts:127-189`).
- T2 monitor is a persistent agent (`monitor`, depth 0, no task, project root) gated by `watchdog.tier2Enabled`, patrolling no faster than every 2 minutes, with warn → 2 nudges → escalation → critical escalation stages (`src/commands/monitor.ts:80-85`, `src/commands/monitor.ts:169-189`, `agents/monitor.md:140-178`).
- Session truth lives in `sessions.db` (SQLite, WAL — write-ahead logging — mode, 5s busy timeout) keyed by `agent_name`, with `escalation_level`/`stalled_since`/`transcript_path` columns and a `runs` table; legacy `sessions.json` is imported once on first open (`src/sessions/store.ts:73-113`, `src/sessions/store.ts:181-200`, `src/sessions/compat.ts:76-105`).
- Restart/resume uses `checkpoint.json` plus append-only `handoffs.json` per agent: `initiateHandoff` saves checkpoint and appends a pending (`toSessionId: null`) handoff, `resumeFromHandoff` returns the newest pending pair, `completeHandoff` links the new session and clears the checkpoint (`src/agents/lifecycle.ts:72-111`, `src/agents/lifecycle.ts:120-146`, `src/agents/lifecycle.ts:157-183`).
- Coordinator owns run lifecycle: start creates a `runs` row plus `current-run.txt`, T0 nudges the coordinator once per run via a `run-complete-notified.txt` dedup marker (coordinator/monitor capabilities excluded), stop completes the run and kills watchdog plus monitor (`src/commands/coordinator.ts:429-444`, `src/watchdog/daemon.ts:190-262`, `src/commands/coordinator.ts:583-688`).
---
## Tier architecture (T0/T1/T2)

Three tiers with increasing cost and judgment. T0 (Tier 0) is cheap and mechanical, T1 (Tier 1) is an ephemeral AI (artificial intelligence) classifier, T2 (Tier 2) is a persistent AI patrol agent:

```
                        +-------------------------+
                        | T0 mechanical daemon    |
                        | poll tmux/PID + timers  |
                        | L0 warn -> L1 nudge ->  |
                        | L2 triage -> L3 kill    |
                        +------------+------------+
                                     | L2, only if tier1Enabled
                                     v
                        +-------------------------+
                        | T1 ephemeral triage     |
                        | last-50-log-lines + LLM |
                        | retry | terminate       |
                        | | extend                |
                        +------------+------------+
                                     | patterns over time
                                     v
                        +-------------------------+
                        | T2 monitor agent        |
                        | patrol <= every 2 min   |
                        | nudge, health summary,  |
                        | escalate to coordinator |
                        +-------------------------+
```

The daemon header still labels tiers per an older Phase 4 numbering where "Tier 2 = Monitor agent (not yet implemented)" and "Tier 3 = Supervisor monitors" (`src/watchdog/daemon.ts:13-17`). That comment is stale: `ov monitor` plus `agents/monitor.md` implement the Tier 2 patrol agent (`src/commands/monitor.ts:1-14`, `agents/monitor.md:40-44`), and `ov supervisor` is marked `[DEPRECATED]` in favor of `lead` (`src/commands/supervisor.ts:452`, `agents/supervisor.md:1-3`). Effective current mapping is T0 = daemon, T1 = triage, T2 = monitor agent, coordinator = top-level orchestrator.

## T0: mechanical daemon

Entry is `ov watch [--interval <ms>] [--background] [--json]` (`src/commands/watch.ts:229-238`). Foreground mode writes a PID (process identifier) file, calls `startDaemon()` with thresholds from config, prints each `HealthCheck` via `onHealthCheck`, and blocks until SIGINT (interrupt signal) (`src/commands/watch.ts:191-227`). Background mode refuses to double-start when the recorded PID is alive, otherwise spawns a detached `bun run <bin> watch` child, unrefs it, and writes `watchdog.pid` (`src/commands/watch.ts:137-189`). PID helpers are duplicated in the coordinator, which starts/stops the watchdog via `ov watch --background` and SIGTERM (termination signal) to the recorded PID (`src/commands/coordinator.ts:145-213`).

`startDaemon()` runs the first tick immediately, then on `setInterval`, swallowing per-tick errors so the daemon never crashes (`src/watchdog/daemon.ts:338-357`). Each `runDaemonTick()` opens the session store via the compat bridge, opens `events.db` (EventStore, fire-and-forget), and reads `current-run.txt` (`src/watchdog/daemon.ts:417-438`):

```ts
const { store } = openSessionStore(overstoryDir);
// ...
const sessions = store.getAll();
```

Core loop behavior per session (`src/watchdog/daemon.ts:452-609`):
- Skip `completed` sessions; explicitly do not skip `zombie` sessions (ZFC — Zero Failure Crash — requires re-checking observable state).
- Headless agents (`tmuxSession === ""` with non-null PID) get an NDJSON (newline-delimited JSON) event tailer from a module-level registry, cleaned up when the agent leaves the active set (`src/watchdog/daemon.ts:465-480`, `src/watchdog/daemon.ts:611-619`).
- Headless agents with an RPC (remote procedure call) connection get a 5s-timeout `getState()` probe; `idle`/`working` refreshes `lastActivity`. Without RPC, one recent event inside the stale window refreshes activity (`src/watchdog/daemon.ts:490-524`).
- `evaluateHealth()` plus forward-only `transitionState()` persist state; `onHealthCheck` fires for every session (`src/watchdog/daemon.ts:526-538`).
- `terminate` kills via the headless-aware `killAgent()` (PID tree for headless, tmux kill for TUI — terminal user interface — only when alive), records a Tier 0 failure to mulch (expertise store), and resets escalation tracking (`src/watchdog/daemon.ts:540-552`, `src/watchdog/daemon.ts:368-389`).
- `investigate` changes nothing; the operator or a higher tier decides (`src/watchdog/daemon.ts:553-557`).
- `escalate` initializes `stalledSince`, advances `expectedLevel = min(floor(stalledMs / nudgeIntervalMs), 3)`, persists via `updateEscalation`, and dispatches the level action (`src/watchdog/daemon.ts:558-608`).
- `none` with non-null `stalledSince` means recovery: reset escalation to 0/null (`src/watchdog/daemon.ts:603-608`).

`MAX_ESCALATION_LEVEL = 3` caps the ladder (`src/watchdog/daemon.ts:41-42`). Level actions in `executeEscalationAction()` (`src/watchdog/daemon.ts:656-805`):
- Level 0 warns (event only, callback already fired) (`src/watchdog/daemon.ts:704-714`).
- Level 1 sends a forced tmux nudge (`force: true` skips debounce) and records delivery (`src/watchdog/daemon.ts:716-738`).
- Level 2 invokes T1 triage only when `tier1Enabled`; otherwise skips toward level 3. `terminate` verdict records a Tier 1 mulch failure and kills; `retry` sends a recovery nudge; `extend` leaves the session running (`src/watchdog/daemon.ts:740-786`).
- Level 3+ records a Tier 0 terminal failure and kills (`src/watchdog/daemon.ts:788-803`).

All failures are recorded to mulch fire-and-forget with agent, capability, reason, detecting tier, and optional triage suggestion (`src/watchdog/daemon.ts:67-96`). All escalation/nudge/triage steps also emit `events.db` custom events (`src/watchdog/daemon.ts:706-712`, `src/watchdog/daemon.ts:730-736`, `src/watchdog/daemon.ts:753-759`).

## Health checks and ZFC

`src/watchdog/health.ts` documents ZFC (Zero Failure Crash): observable state (tmux alive, PID alive) is the source of truth, because `sessions.db` is updated asynchronously by hooks and can go stale mid-crash (`src/watchdog/health.ts:4-31`). Signal priority is tmux liveness, then PID liveness, then recorded state (`src/watchdog/health.ts:8-12`). PID liveness uses signal 0, which checks existence without killing (`src/watchdog/health.ts:63-71`).

Decision order in `evaluateHealth()` (`src/watchdog/health.ts:188-301`):
1. `completed` skips monitoring (`src/watchdog/health.ts:215-223`).
2. Headless (`tmuxSession === "" && pid !== null`): PID is the primary signal. PID-dead yields zombie/terminate; PID-alive plus recorded-zombie yields investigate; otherwise time-based checks (`src/watchdog/health.ts:79-81`, `src/watchdog/health.ts:226-252`).
3. TUI (terminal user interface): tmux-dead yields zombie/terminate regardless of recorded state (`src/watchdog/health.ts:258-271`); tmux-alive plus recorded-zombie yields investigate (`src/watchdog/health.ts:276-285`); PID-dead plus tmux-alive yields zombie/terminate since the shell survived but the agent exited (`src/watchdog/health.ts:289-297`).
4. Time-based: past `zombieMs` yields zombie/terminate; past `staleMs` yields stalled/escalate; `booting` with fresh activity becomes `working` (`src/watchdog/health.ts:116-147`).

Persistent capabilities `coordinator` and `monitor` are exempt from time-based stale/zombie detection (long idle waits are normal); only tmux/PID liveness applies, and a recorded `stalled` flips back to `working` (`src/watchdog/health.ts:36-43`, `src/watchdog/health.ts:101-114`). The same exemption set exists in the daemon for run-completion accounting (`src/watchdog/daemon.ts:48-48`).

State transitions are forward-only over `booting(0) → working(1) → stalled(2) → zombie(3)` — completed is terminal and separately skipped; `investigate` holds state (`src/watchdog/health.ts:46-52`, `src/watchdog/health.ts:320-335`).

## T1: AI triage

`triageAgent()` takes `agentName`, `root`, `lastActivity`, optional timeout and config (`src/watchdog/triage.ts:29-38`). It reads the newest timestamped session directory's `session.log` tail (last 50 lines), builds a one-word classification prompt, shells to the configured print-command runtime, and classifies the reply (`src/watchdog/triage.ts:42-58`, `src/watchdog/triage.ts:67-100`, `src/watchdog/triage.ts:105-124`):

```ts
"Respond with exactly one word: 'retry' if the error is recoverable,
'terminate' if the error is fatal or the agent has failed,
or 'extend' if this looks like a long-running operation."
```

Missing logs or model failure both fall back to `extend`, the safe no-kill default (`src/watchdog/triage.ts:44-47`, `src/watchdog/triage.ts:54-57`). Default subprocess timeout is 30s with kill-on-expiry; nonzero exit throws `AgentError` with stderr (standard error) text (`src/watchdog/triage.ts:126-168`). `classifyResponse()` matches `retry|recoverable` first, then `terminate|fatal|failed`, else `extend` (`src/watchdog/triage.ts:176-189`).

## T2: monitor agent

The monitor is a persistent agent named `monitor` at depth 0 with no parent, no task assignment, no worktree (project root), and no per-task overlay — context comes from `ov status`, mail, tracker, and mulch (`src/commands/monitor.ts:31-32`, `src/commands/monitor.ts:169-189`, `agents/monitor.md:25-34`). Start is gated on `watchdog.tier2Enabled` (`src/commands/monitor.ts:80-85`). Startup deploys monitor hooks, creates an identity record on first run, spawns a project-namespaced tmux session `overstory-<project>-monitor`, records a `booting` session before sending the beacon (so hooks can transition to `working`), then sends the beacon plus a follow-up Enter (`src/commands/monitor.ts:113-198`). The beacon is (`src/commands/monitor.ts:46-54`):

```ts
`[OVERSTORY] monitor (monitor/tier-2) ${timestamp}` —
"Depth: 0 | Parent: none | Role: continuous fleet patrol" —
"Startup: run mulch prime, check fleet (ov status --json), check mail ..."
```

Stop kills tmux and marks `completed`; status reconciles tmux-dead-but-recorded-active to `zombie` (`src/commands/monitor.ts:234-274`, `src/commands/monitor.ts:281-339`).

Patrol doctrine (`agents/monitor.md:89-115`): check `ov status --json` for transitions, process mail (lifecycle requests, health probes), nudge progressively, send a `status` health summary to the coordinator every ~5 cycles, and never poll faster than every 2 minutes (adaptive 2–5 min cadence). Nudge stages are warning (log only), first nudge after 2+ stale cycles, second forced nudge after 4+, escalation after 6+, critical escalation after 8+ with no coordinator response; any new activity resets the count (`agents/monitor.md:140-178`). Anomaly patterns to flag: repeated stalls (3+), silent completions (tmux died without `worker_done`), branch divergence, resource hogging, cascade failures (`agents/monitor.md:180-188`). Hard constraints: no code writes, no spawning — report the need, do not create agents (`agents/monitor.md:190-203`).

## Worker restart handling

Restart semantics differ by tier. T0 kills directly: headless by PID tree, TUI by tmux kill (`src/watchdog/daemon.ts:368-389`). Every `stop`/`status` command reconciles the same way: tmux-dead plus recorded-active becomes `zombie` (coordinator additionally checks PID-inside-live-tmux to reclaim crashed panes) (`src/commands/monitor.ts:306-313`, `src/commands/supervisor.ts:353-361`, `src/commands/coordinator.ts:334-357`).

Higher-level restart is human/AI-mediated, not automatic respawn: the monitor's lifecycle section handles respawn/restart/cycle requests via mail — verify dead via `ov status`, warn-then-wait for restart, checkpoint-then-confirm for cycle (`agents/monitor.md:117-138`). The deprecated supervisor workflow adds the operator-side protocol: 15-minute nudge spacing, max 3 nudges, then escalate warning→error, with named failure modes `SILENT_WORKER_FAILURE`, `EXCESSIVE_NUDGING`, `ORPHANED_WORKERS` (`agents/supervisor.md:19-30`, `agents/supervisor.md:290-333`).

## Checkpoints and handoffs

Checkpoints are per-agent `checkpoint.json` files under `{agentsDir}/{agentName}/`, written with tab-indented JSON (JavaScript Object Notation) and recursive mkdir (directory creation); load returns null when absent, parse failure throws `LifecycleError`; clear tolerates ENOENT (error: no such file) (`src/agents/checkpoint.ts:6-6`, `src/agents/checkpoint.ts:14-40`, `src/agents/checkpoint.ts:48-78`, `src/agents/checkpoint.ts:86-101`).

Handoffs layer a pending/completed protocol over checkpoints in `{agentsDir}/{agentName}/handoffs.json` (`src/agents/lifecycle.ts:7-7`, `src/agents/lifecycle.ts:13-61`):
- `initiateHandoff()` builds a checkpoint (agent, task, session, timestamp, progress summary, files modified, branch, pending work, mulch domains), saves it, appends a handoff with `toSessionId: null` and a reason, and returns it (`src/agents/lifecycle.ts:72-111`).
- `resumeFromHandoff()` scans from the end for the newest `toSessionId === null` entry, loads the checkpoint, returns both or null (`src/agents/lifecycle.ts:120-146`).
- `completeHandoff()` binds the newest pending handoff to `newSessionId` and clears the checkpoint; throws when none is pending (`src/agents/lifecycle.ts:157-183`).

Supervisor recovery order is checkpoint → overlay → group status → `ov status` → mail → `ml prime` → tracker ready (`agents/supervisor.md:414-427`); monitor recovery is status → mail → `ml prime` → tracker in-progress list (`agents/monitor.md:205-214`).

## Session store and resume

`SessionStore` is SQLite (`bun:sqlite`, synchronous) at `.overstory/sessions.db`, WAL (write-ahead logging) mode, `synchronous = NORMAL`, 5s busy timeout, with `sessions` and `runs` tables plus state/run/coordinator indexes (`src/sessions/store.ts:1-10`, `src/sessions/store.ts:181-200`, `src/sessions/store.ts:73-113`). Sessions key on unique `agent_name`; `upsert` overwrites all fields on conflict; `getActive` returns `booting/working/stalled`; `getByRun` filters by run; `updateEscalation` writes level plus `stalled_since`; `purge` deletes by all/state/agent (`src/sessions/store.ts:203-250`, `src/sessions/store.ts:256-271`, `src/sessions/store.ts:281-292`, `src/sessions/store.ts:380-416`). `RunStore` in the same file tracks run id, timestamps, agent count, coordinator session/name, and `active/completed/failed` status (`src/sessions/store.ts:99-113`, `src/sessions/store.ts:447-574`).

`openSessionStore()` is the compat bridge: DB-with-rows is authoritative; empty-or-missing DB falls through to a one-time `sessions.json` import with field normalization (`runId`, `pid`, `escalationLevel` defaults); neither yields an empty DB (`src/sessions/compat.ts:63-105`, `src/sessions/compat.ts:21-41`).

## Supervisor / monitor / coordinator commands

Supervisor (`ov supervisor start|stop|status`, deprecated): per-project agent at depth 1 under `coordinator`, requires `--task` and `--name`, runs at project root on the canonical branch, deploys supervisor hooks, creates identity on first run, spawns namespaced tmux `overstory-<project>-supervisor-<name>`, waits for TUI (terminal user interface) ready, sends a beacon, and upserts a `booting` session; duplicate-name start is rejected when tmux is alive, else the stale row completes (`src/commands/supervisor.ts:1-13`, `src/commands/supervisor.ts:45-60`, `src/commands/supervisor.ts:75-264`). Stop kills tmux and completes; status lists one or all supervisors with tmux reconciliation (`src/commands/supervisor.ts:273-319`, `src/commands/supervisor.ts:327-446`).

Monitor (`ov monitor start|stop|status`): as above; `--attach/--no-attach` controls tmux attach, defaulting to TTY (teletypewriter/terminal) detection (`src/commands/monitor.ts:341-354`).

Coordinator (`ov coordinator start|stop|status|send|ask|output|check-complete`): persistent depth-0 orchestrator with no task, project root, run ownership, and `--watchdog`/`--monitor` auto-start flags (`src/commands/coordinator.ts:1-13`, `src/commands/coordinator.ts:1248-1350`). Start reclaims zombie panes (tmux alive but PID dead), creates the run row plus `current-run.txt`, records the session before the beacon to avoid the booting-stuck race, waits for TUI with shell-init delay, then sends the hierarchy beacon ("ONLY spawn leads... NEVER spawn non-lead agents directly") (`src/commands/coordinator.ts:293-573`, `src/commands/coordinator.ts:271-281`). Stop kills tmux, stops watchdog and monitor, completes the run, and removes `current-run.txt` (`src/commands/coordinator.ts:583-688`). `check-complete` requires all enabled exit triggers (`allAgentsDone`, `taskTrackerEmpty`, `onShutdownSignal`) to be met, and `allAgentsDone` additionally requires an empty merge queue (`src/commands/coordinator.ts:1105-1243`).

## Watch command and run completion

`ov watch` is the T0 operator surface (see T0 section for foreground/background). Run-level completion detection runs at the end of every daemon tick when `current-run.txt` exists: non-persistent workers (`coordinator`/`monitor` excluded) all `completed` triggers one forced coordinator nudge with a phase-aware message (scout/builder/reviewer/lead/merger single-phase vs mixed breakdown), an `events.db` `run_complete` record, and a `run-complete-notified.txt` dedup marker (`src/watchdog/daemon.ts:154-181`, `src/watchdog/daemon.ts:190-262`, `src/watchdog/daemon.ts:621-632`).

**Covers:** src/watchdog/daemon.ts, src/watchdog/triage.ts, src/watchdog/health.ts, src/agents/checkpoint.ts, src/agents/lifecycle.ts, src/sessions/store.ts, src/sessions/compat.ts, src/commands/supervisor.ts, src/commands/monitor.ts, src/commands/coordinator.ts, src/commands/watch.ts, agents/supervisor.md, agents/monitor.md
