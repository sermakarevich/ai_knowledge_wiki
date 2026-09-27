> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Runtime Supervision: Daemon, Scheduler, Sessions, Restarts

**In one sentence:** A single Go daemon runs a fixed 3-minute recovery heartbeat plus dedicated per-dog tickers, discovers agent liveness from tmux (not from stored state), and restarts dead sessions with exponential backoff while capacity-gated dispatch and sentinel files (ESTOP, pressure, quota) decide what may spawn.

## Key points
- The daemon main loop (`Daemon.Run`) fires an immediate heartbeat then a fixed recovery heartbeat (default 3 minutes, config `operational.daemon.recovery_heartbeat_interval`) plus independent tickers per dog (quota 5m, doctor 5m, checkpoint 10m, compactor 24h, wisp reaper 1h, dolt backup 15m), so crash detection never waits on the slow tick (`internal/daemon/daemon.go:513`, `internal/daemon/daemon.go:842`, `internal/config/operational.go:48`).
- Stuck/crashed agents are detected four ways: GUPP violations (live session + hooked work + no bead update for 30m), orphaned work (dead session + hooked work left behind), Deacon heartbeat staleness with grace-period logic, and dog-lifecycle sweeps (dead-session working dogs, stale-working dogs idle 2h, idle dogs reaped after 1h) plus the `stuck-agent-dog` plugin scoped to polecats and Deacon only (`internal/daemon/lifecycle.go:1068`, `internal/daemon/lifecycle.go:1185`, `internal/daemon/daemon.go:1525`, `internal/daemon/handler.go:84`, `plugins/stuck-agent-dog/run.sh:2`).
- Every restart goes through a `RestartTracker` with exponential backoff (30s initial, x2 multiplier, 10m max, crash-loop at 5 restarts in 15m, reset after 30m stable, state in `daemon/restart_state.json`), and rate-limit pauses use a separate fixed 60s `RecordPause` that does not count toward the crash-loop budget (`internal/daemon/restart_tracker.go:44`, `internal/daemon/restart_tracker.go:169`, `internal/daemon/restart_tracker.go:217`).
- Worker restart is kill-then-recreate: `KillSessionWithProcesses` (disarm respawn hook, SIGTERM descendants, 2s grace, SIGKILL, kill session) followed by `EnsureSessionFreshWithCommandAndEnv` (skip if agent still alive, else fresh `tmux new-session` + `respawn-pane -k` with `-e` env flags); beads/Dolt state and git worktrees survive, the tmux pane process and in-memory agent context do not (`internal/tmux/tmux.go:637`, `internal/tmux/tmux.go:583`, `internal/daemon/lifecycle.go:415`).
- tmux sessions are per-town-socket (`basename-hash6`, e.g. `gt-a1b2c3`) with names `hq-mayor`, `hq-deacon`, `<prefix>-witness`, `<prefix>-refinery`, `<prefix>-crew-<name>`, `<prefix>-<polecat>`, `hq-dog-<name>`; health is a 3-level check (session exists, agent process alive via `GT_PROCESS_NAMES`, optional inactivity) and a `pane-died` hook auto-respawns crashed panes after a 3s debounce unless the daemon disarmed it for an intentional kill (`internal/session/registry.go:160`, `internal/session/names.go:16`, `internal/tmux/tmux.go:2421`, `internal/tmux/tmux.go:4385`).
- Capacity scheduling is pure functions in `internal/scheduler/capacity`: `PlanDispatch(capacity, batchSize, ready)` returns `ToDispatch/Skipped/Reason` (`capacity|batch|ready|none`), `DispatchCycle` runs query-plan-validate-execute with `OnSuccess` retried twice, cross-rig prefix mismatches are refused, and `max_polecats <= 0` means direct dispatch while `N > 0` means daemon-deferred dispatch (`internal/scheduler/capacity/pipeline.go:135`, `internal/scheduler/capacity/dispatch.go:50`, `internal/scheduler/capacity/config.go:16`).
- E-stop is a sentinel file (`$TOWN/ESTOP` with `trigger\ttimestamp\treason`, plus per-rig `ESTOP.<rig>`); when active the heartbeat returns early so the daemon stays alive for Dolt/maintenance but spawns or restarts nothing, and only the Mayor is exempt by convention (`internal/estop/estop.go:21`, `internal/estop/estop.go:42`, `internal/daemon/daemon.go:866`).
- Quota rotation is mechanical: the quota dog shells out to `gt quota rotate --json` (2m timeout), the scanner matches case-insensitive rate-limit regexes against the bottom 20 of 30 captured pane lines, the planner assigns one fresh account per `CLAUDE_CONFIG_DIR` round-robin, and the rotator swaps keychain tokens under a quota-file lock then restarts affected sessions (`internal/daemon/quota_dog.go:43`, `internal/quota/scan.go:88`, `internal/quota/rotate.go:63`, `internal/quota/executor.go:87`).

---
## Tick loop walkthrough

`Daemon.Run` (`internal/daemon/daemon.go:446`) acquires a file lock (`daemon/daemon.lock`), writes the PID file, starts the feed curator, convoy manager, and KRC pruner, then creates one `time.Ticker` per enabled patrol before running the first heartbeat synchronously (`internal/daemon/daemon.go:513`, `internal/daemon/daemon.go:587`, `internal/daemon/daemon.go:725`):

```go
timer := time.NewTimer(d.recoveryHeartbeatInterval())
// ...
d.heartbeat(state)
for {
    select {
    case <-d.ctx.Done():
        return d.shutdown(state)
    case sig := <-sigChan:
        // lifecycle / reload-restart / shutdown
    case <-doltHealthChan:
        d.ensureDoltServerRunning()
    case <-quotaDogChan:
        d.runQuotaDog()
    // ... one case per dog ticker ...
    case <-timer.C:
        d.heartbeat(state)
        timer.Reset(d.recoveryHeartbeatInterval())
    }
}
```

The recovery interval resolves through `loadOperationalConfig().GetDaemonConfig().RecoveryHeartbeatIntervalD()` with a 3-minute default (`internal/daemon/daemon.go:842`, `internal/config/operational.go:48`). Normal wake is event-driven (`bd activity --follow` via the feed curator); the daemon is the recovery safety net (`internal/daemon/daemon.go:50`).

Each `heartbeat` (`internal/daemon/daemon.go:853`) runs ordered phases and persists `daemon/state.json` with `LastHeartbeat`/`HeartbeatCount` at the end (`internal/daemon/daemon.go:1007`):

1. Early exits: shutdown-in-progress skip, E-stop skip (`internal/daemon/daemon.go:857`, `internal/daemon/daemon.go:866`).
2. Per-tick cache invalidation + prefix registry reload + ghost-session kill (`internal/daemon/daemon.go:878`, `internal/daemon/daemon.go:883`, `internal/daemon/daemon.go:1998`).
3. `ensureDoltServerRunning` before any beads operation (`internal/daemon/daemon.go:892`, `internal/daemon/daemon.go:1033`).
4. `ensureDeaconRunning` / `ensureBootRunning` / `checkDeaconHeartbeat` when the deacon patrol is active (`internal/daemon/daemon.go:897`, `internal/daemon/daemon.go:910`, `internal/daemon/daemon.go:917`).
5. `ensureWitnessesRunning`, `ensureRefineriesRunning` (pressure-gated), `ensureMayorRunning` (`internal/daemon/daemon.go:1723`, `internal/daemon/daemon.go:1800`, `internal/daemon/daemon.go:1900`).
6. `handleDogs` (or cleanup-only under pressure), `processLifecycleRequests` (`internal/daemon/handler.go:42`, `internal/daemon/daemon.go:2263`).
7. `checkGUPPViolations`, `checkOrphanedWork`, `checkPolecatSessionHealth`, `reapIdlePolecats` (`internal/daemon/lifecycle.go:1068`, `internal/daemon/lifecycle.go:1185`, `internal/daemon/daemon.go:2593`, `internal/daemon/daemon.go:2876`).
8. `cleanupOrphanedProcesses`, `pruneStaleBranches`, pressure-gated `dispatchQueuedWork` (shells out to `gt scheduler run`), `rotateOversizedLogs` (`internal/daemon/daemon.go:3017`, `internal/daemon/daemon.go:3038`, `internal/daemon/daemon.go:996`, `internal/daemon/daemon.go:1019`).

Per-rig heartbeat work runs through a bounded `RigWorkerPool` (default 10 workers, 30s per-rig timeout) so one slow rig cannot stall the tick (`internal/daemon/worker.go:21`, `internal/daemon/worker.go:29`). Patrols can also be disabled via `settings/config.json` `disabled_patrols`, checked by `isPatrolActive` alongside `mayor/daemon.json` (`internal/daemon/types.go:381`).

## Detection to restart sequence

Detection never trusts stored liveness; observable state is derived from tmux ("discover, don't track", `internal/daemon/lifecycle.go:946`):

1. **GUPP violation.** For each operational rig, list agent beads (`bd list --label=gt:agent` + `bd mol wisp list` merged in `internal/daemon/lifecycle.go:987`), match `<prefix>-<rig>-polecat-<name>`, and flag beads with non-empty `hook_bead` whose session `IsAgentAlive` but whose `updated_at` is older than `GUPPViolationTimeout` (30m default). The daemon mails `<rig>/witness` with subject `GUPP_VIOLATION:` and does not kill anything itself (`internal/daemon/lifecycle.go:1090`, `internal/constants/constants.go:101`, `internal/daemon/lifecycle.go:1159`).
2. **Orphaned work.** Same bead listing, but the session is dead (`!IsAgentAlive`). A TOCTOU guard re-checks liveness and re-reads `hook_bead` from the DB before notifying the witness with `ORPHANED_WORK:` (`internal/daemon/lifecycle.go:1207`, `internal/daemon/lifecycle.go:1255`, `internal/daemon/lifecycle.go:1287`). Nuked agents are skipped in both checks (`internal/daemon/lifecycle.go:1129`, `internal/daemon/lifecycle.go:1242`).
3. **Polecat crash.** `checkPolecatSessionHealth` validates sessions for polecats with work-on-hook and notifies the witness of crashed polecats; `reapIdlePolecats` kills sessions idle past the configured threshold (`internal/daemon/daemon.go:2593`, `internal/daemon/daemon.go:2853`, `internal/daemon/daemon.go:2876`).
4. **Deacon stuck.** `checkDeaconHeartbeat` reads the Deacon heartbeat file every tick. If the daemon recently started Deacon (`deaconLastStarted`, guarding issue #567) only pre-start heartbeats get a grace period (default 5m); a post-start stale heartbeat means stuck, triggering `restartStuckDeacon`; crash-loop state suppresses the kill (`internal/daemon/daemon.go:74`, `internal/daemon/daemon.go:1525`).
5. **Dog lifecycle.** `cleanupStuckDogs` clears work for `state=working` dogs with dead sessions (compare-and-swap via `ClearWorkIfMatches` so changed assignments are not clobbered); `detectStaleWorkingDogs` kills sessions stuck in `working` past `stale_working_timeout` (2h); `reapIdleDogs` kills sessions idle past 1h and removes dogs idle past 4h only when the pool exceeds `max_dog_pool_size` (4); `dispatchPlugins` assigns cooldown-gated (never manual-gate) plugins to dispatchable idle dogs and records the run immediately to satisfy the cooldown (`internal/daemon/handler.go:84`, `internal/daemon/handler.go:139`, `internal/daemon/handler.go:182`, `internal/daemon/handler.go:240`, `internal/daemon/handler.go:365`).
6. **Plugin detection (`stuck-agent-dog`).** Runs as a dispatched dog plugin, scoped to polecats and Deacon, never crew/mayor/witness/refinery. It checks heartbeat freshness and mass death (>= 3 deaths in the window), escalates with stable fingerprints (`stuck-agent-dog:mass-death`, `stuck-agent-dog:deacon:stuck-heartbeat`), and records its run via `gt plugin record-run` (`plugins/stuck-agent-dog/run.sh:2`, `plugins/stuck-agent-dog/run.sh:363`, `plugins/stuck-agent-dog/run.sh:407`, `plugins/stuck-agent-dog/plugin.md:2`).
7. **Quota detection.** `runQuotaDog` shells out to `gt quota rotate --json` with a 2-minute context timeout; failures are logged non-fatally (`internal/daemon/quota_dog.go:43`, `internal/daemon/quota_dog.go:13`, `internal/daemon/quota_dog.go:53`).
8. **Restart gating.** `ensureDeaconRunning` consults the tracker first: crash-loop means skip with a `gt daemon clear-backoff` hint, active backoff means skip with remaining time; `ErrAlreadyRunning` records success to decay the backoff (`internal/daemon/daemon.go:1463`).
9. **Restart execution.** Lifecycle `cycle`/`restart` requests (claimed from the Deacon mail inbox, stale ones older than 6h deleted) kill via `KillSessionWithProcesses`, sleep `ShutdownNotifyDelay`, then `restartSession` rebuilds the session from role config with fresh env, git pre-sync, theme, readiness wait, and dialog acceptance (`internal/daemon/lifecycle.go:43`, `internal/daemon/lifecycle.go:92`, `internal/daemon/lifecycle.go:198`, `internal/daemon/lifecycle.go:343`, `internal/daemon/lifecycle.go:430`).

## tmux and session management

Session creation avoids the old create-then-SendKeys race by passing the command as the initial pane process (`internal/tmux/tmux.go:324`):

```go
// Replace the initial shell with the actual command.
respawnArgs := []string{"respawn-pane", "-k", "-t", name}
if workDir != "" {
    respawnArgs = append(respawnArgs, "-c", workDir)
}
respawnArgs = append(respawnArgs, command)
```

Env is seeded via `tmux new-session -e` flags (`NewSessionWithCommandAndEnv`) so the first shell and the agent's `bd` subprocesses inherit identity vars instead of stale tmux-global ones like `BD_ACTOR=daemon`; startup commands additionally inline `export K=V ... && exec ...` via `PrependEnv` for `WaitForCommand` detection (`internal/tmux/tmux.go:402`, `internal/daemon/lifecycle.go:500`, `internal/daemon/lifecycle.go:569`). `EnsureSessionFreshWithCommandAndEnv` returns `ErrSessionRunning` when the agent is still alive and only kills zombies (`internal/tmux/tmux.go:583`).

Kills use `KillSessionWithProcesses`: disarm `remain-on-exit` and the `pane-died` hook first, snapshot descendants, SIGTERM, 2s grace (`processKillGracePeriod`), SIGKILL stragglers and the pane PID, then `kill-session` (`internal/tmux/tmux.go:615`, `internal/tmux/tmux.go:637`). Attach is a plain `tmux attach-session -t` wrapper; respawn of a dead pane reuses the original command (`internal/tmux/tmux.go:2638`, `internal/tmux/tmux.go:4385`).

Health and naming:

```go
func (t *Tmux) CheckSessionHealth(session string, maxInactivity time.Duration) ZombieStatus {
    alive, err := t.HasSession(session)
    if err != nil || !alive {
        return SessionDead
    }
    if !t.IsAgentAlive(session) {
        return AgentDead
    }
    // ... optional inactivity -> AgentHung ...
    return SessionHealthy
}
```

(`internal/tmux/tmux.go:2421`). `IsAgentAlive` resolves process names from the session env `GT_PROCESS_NAMES` (set at startup, handles custom agents) with fallback to `GT_AGENT` preset lookup, then checks the pane process tree up to depth 10 (`internal/tmux/tmux.go:3134`, `internal/tmux/tmux.go:3157`, `internal/tmux/tmux.go:2484`). Names come from `internal/session/names.go` (`hq-mayor`, `hq-deacon`, `hq-boot`, `<prefix>-witness`, `<prefix>-refinery`, `<prefix>-crew-<name>`, `<prefix>-<polecat>`, `hq-dog-<name>`) with per-town socket isolation (`internal/session/names.go:16`, `internal/session/registry.go:160`). The unified `session.StartSession` runs a 14-step lifecycle (resolve agent config, ensure settings, build command, create with env, theme, wait, auto-respawn hook, dialogs, ready delay, verify survived, record `GT_PANE_ID`, track PID, optional agent-log watcher, telemetry) and `StopSession` supports graceful Ctrl-C shutdown (`internal/session/lifecycle.go:144`, `internal/session/lifecycle.go:355`). Stale-message detection compares mail timestamps against `SessionCreatedAt` from tmux (`internal/session/stale.go:12`, `internal/session/stale.go:32`).

## Capacity and scheduling

`SchedulerConfig` (`internal/scheduler/capacity/config.go:16`) is town-wide because API/CPU/memory are host-shared: `max_polecats` nil/absent = -1 direct dispatch, 0 = direct, N > 0 = deferred daemon dispatch; `batch_size` default 1 caps spawns per heartbeat; `spawn_delay` default `0s` separates spawns to avoid Dolt lock contention (`internal/scheduler/capacity/config.go:46`, `internal/scheduler/capacity/config.go:53`, `internal/scheduler/capacity/config.go:71`).

The pure core is `PlanDispatch` (`internal/scheduler/capacity/pipeline.go:135`): defensively filter messaging beads (`gt:message`/`gt:handoff`/`gt:merge-request`, `internal/scheduler/capacity/pipeline.go:58`), return `none` when nothing is ready, `capacity` when slots <= 0, otherwise dispatch `min(capacity, batch, len(ready))` with reason `batch`/`capacity`/`ready` (plus `+messaging-filtered`). Failure policy is a circuit breaker (`CircuitBreakerPolicy`, quarantine after N failures, `FilterCircuitBroken`) and context is rebuilt from sling beads via `ReconstructFromContext` (`internal/scheduler/capacity/pipeline.go:190`, `internal/scheduler/capacity/pipeline.go:201`, `internal/scheduler/capacity/pipeline.go:234`).

`DispatchCycle` (`internal/scheduler/capacity/dispatch.go:50`) wires the impure edges: `AvailableCapacity`, `QueryPending`, optional `Validate` (cross-rig prefix guard returning `ErrCrossRigPrefix`, `internal/scheduler/capacity/dispatch.go:24`), `Execute`, `OnSuccess` (retried twice with 500ms backoff because an unclosed sling context would re-dispatch, `internal/scheduler/capacity/dispatch.go:106`), `OnFailure`, `BatchSize`, `SpawnDelay`. Runtime pause state lives in `.runtime/scheduler-state.json` (`internal/scheduler/capacity/state.go:13`, `internal/scheduler/capacity/state.go:23`). The daemon triggers dispatch pressure-gated each heartbeat; polecats, refineries, and dogs are gated while deacon/witness/mayor are not (`internal/daemon/daemon.go:996`, `internal/daemon/pressure.go:34`).

## E-stop, pressure, keepalive, nudges, connections

E-stop (`internal/estop/estop.go:1`): `Activate` writes `manual|auto\ttimestamp\treason` to `$TOWN/ESTOP`; `IsActive` is a single `os.Stat`; `Deactivate(townRoot, onlyAuto=true)` refuses to clear manual stops (must use `gt thaw`); per-rig `ESTOP.<rig>` files compose via `IsAnyActive` (`internal/estop/estop.go:57`, `internal/estop/estop.go:42`, `internal/estop/estop.go:65`, `internal/estop/estop.go:79`, `internal/estop/estop.go:121`).

Pressure (`internal/daemon/pressure.go:43`) checks load-per-core, available memory GB, and active-session caps from operational config; all-disabled (defaults) short-circuits to `OK` without subprocess calls (`internal/daemon/pressure.go:48`). Keepalive is best-effort JSON (`last_command`, `timestamp`) in `.runtime/keepalive.json`; `Read` returns nil on any failure and `Age()` on nil returns 365 days so missing signals read as maximally stale (`internal/keepalive/keepalive.go:53`, `internal/keepalive/keepalive.go:103`, `internal/keepalive/keepalive.go:132`).

Nudges avoid destructive `send-keys` (which cancels in-flight tool calls) by writing JSON files to `.runtime/nudge_queue/<session>/` with 30m normal / 2h urgent TTL and max depth 50; `Drain` uses rename-to-`.claimed` for exactly-once delivery across concurrent drainers, sweeps orphaned claims older than 5m, discards expired, defers `DeliverAfter`, and formats output as `<system-reminder>` blocks for the `UserPromptSubmit` hook (`internal/nudge/queue.go:75`, `internal/nudge/queue.go:40`, `internal/nudge/queue.go:164`, `internal/nudge/queue.go:370`). The `Connection` interface abstracts the same file/exec/tmux surface for local vs SSH rigs (`internal/connection/connection.go:13`). Mass-death protection complements per-agent backoff: the daemon tracks recent session deaths in a 30s window and alerts at 3 deaths instead of restarting blindly into a systemic failure (`internal/daemon/daemon.go:147`). Oversized Dolt server logs are rotated copytruncate-style each heartbeat since child-held file descriptors rule out rename rotation, while `daemon.log` itself uses lumberjack (100MB, 3 backups, 7 days, compressed) (`internal/daemon/daemon.go:1019`, `internal/daemon/daemon.go:226`).

## What survives a restart vs what is re-provisioned

A restart kills only the tmux pane tree; everything persisted outside the pane survives. Beads/Dolt state needs no sync (writes are immediate), while git worktrees for roles with persistent clones (refinery, crew) get `git fetch` + `git pull --rebase` with auto-stash/pop around dirty trees, and consecutive pull failures escalate from WARN to ERROR after the configured threshold (`internal/daemon/lifecycle.go:636`, `internal/daemon/lifecycle.go:681`, `internal/daemon/lifecycle.go:715`). Re-provisioned on every restart: the tmux session itself, the startup command rebuilt from role config plus agent resolution (Claude vs non-Claude agents get different commands), the full `AgentEnv` identity set (`GT_ROLE`, `GT_RIG`, `BEADS_DOLT_PORT`, `CLAUDE_CONFIG_DIR` resolution), tmux theme, `GT_PANE_ID`, PID tracking file, and the `pane-died` auto-respawn hook (`internal/daemon/lifecycle.go:500`, `internal/daemon/lifecycle.go:574`, `internal/daemon/lifecycle.go:430`, `internal/session/pidtrack.go:45`). Restarted polecats also resume their session link where the rotator records one: quota rotation reports `resumed_session` (empty when the session started fresh) and whether a keychain swap occurred (`internal/quota/rotate.go:10`). Lost on restart: the agent's in-flight conversation context, uncommitted shell state, and any un-checkpointed worktree edits (which is why the checkpoint dog auto-commits dirty polecat worktrees every 10m, `internal/daemon/checkpoint_dog.go:50`).

## Shutdown and single-flight guarantees

Only one daemon runs per town: `Run` takes an exclusive `daemon/daemon.lock` (non-blocking `TryLock`) before the PID-file check, closing the TOCTOU race of concurrent starts (`internal/daemon/daemon.go:465`).
Shutdown is cooperative: `shutdown.lock` makes in-flight heartbeats skip work so the daemon does not fight `gt down` by re-spawning killed agents, and lifecycle `shutdown` requests kill without restart (`internal/daemon/daemon.go:857`, `internal/daemon/lifecycle.go:187`).
Lifecycle mail uses claim-then-execute (delete the request before acting) so a crashed daemon never replays a stale cycle on the next tick (`internal/daemon/lifecycle.go:92`).

## Config knobs

| Knob | Location | Default | Effect |
|---|---|---|---|
| `operational.daemon.recovery_heartbeat_interval` | `internal/config/types.go:349` | `3m` (`internal/config/operational.go:48`) | Fixed daemon tick; Dolt fast path stays on its own ticker |
| `operational.daemon.boot_spawn_cooldown` | `internal/config/types.go:352` | `2m` (`internal/config/operational.go:49`) | Minimum gap between Boot triage spawns (`internal/daemon/daemon.go:1316`) |
| `operational.daemon.boot_idle_suppression` | `internal/config/types.go:355` | `15m` (`internal/config/operational.go:50`) | Suppress Boot after a `nothing` (healthy) report |
| `operational.daemon.gupp_violation_timeout` | `internal/config/types.go:265` | `30m` (`internal/config/operational.go:19`) | Hooked-work staleness before witness mail |
| `operational.daemon.max_lifecycle_message_age` | `internal/daemon/lifecycle.go:40` | `6h` (`internal/config/operational.go:45`) | Lifecycle mail older than this is deleted unprocessed |
| `operational.daemon.dog_idle_session_timeout` | `internal/config/types.go:313` | `1h` (`internal/config/operational.go:40`) | Kill sessions of idle dogs (`internal/daemon/handler.go:182`) |
| `operational.daemon.dog_idle_remove_timeout` | `internal/config/types.go:332` | `4h` (`internal/config/operational.go:42`) | Remove long-idle dogs when pool oversized |
| `operational.daemon.stale_working_timeout` | `internal/config/types.go:334` | `2h` (`internal/config/operational.go:43`) | `working` with no activity counts as stuck |
| `operational.daemon.max_dog_pool_size` | `internal/config/types.go:336` | `4` (`internal/config/operational.go:44`) | Target kennel size for phase-2 removal |
| `patrols.restart_tracker.*` | `internal/daemon/restart_tracker.go:14` | 30s / 10m / x2 / 5-in-15m / 30m stable / 60s pause (`internal/daemon/restart_tracker.go:44`) | Backoff and crash-loop budget |
| `patrols.quota_dog.interval` | `internal/daemon/quota_dog.go:16` | `5m` (`internal/daemon/quota_dog.go:11`) | Rate-limit scan + rotation cadence |
| `patrols.{doctor,checkpoint,compactor,wisp_reaper,dolt_backup,jsonl_git_backup,main_branch_test}.*` | `internal/daemon/types.go:116` | 5m / 10m / 24h / 1h / 15m / 15m / 30m (`internal/daemon/lifecycle_defaults.go:15`) | Per-dog ticker cadences; missing entries backfilled by `EnsureLifecycleDefaults` (`internal/daemon/lifecycle_defaults.go:73`) |
| `scheduler.max_polecats / batch_size / spawn_delay` | `internal/scheduler/capacity/config.go:16` | -1 (direct) / 1 / `0s` (`internal/scheduler/capacity/config.go:35`) | Deferred dispatch switch and per-tick spawn cap |
| `GT_STUCK_AGENT_DOG_*` env | `plugins/stuck-agent-dog/run.sh:30` | deacon stale 1200s, mass-death 3 | Plugin-side thresholds for the dog plugin |
| `settings.disabled_patrols` | `internal/daemon/types.go:358` | none | Town-level patrol kill switch evaluated each tick |

**Covers:** `internal/daemon` (daemon.go, types.go, lifecycle.go, handler.go, worker.go, quota_dog.go, restart_tracker.go, lifecycle_defaults.go, pressure.go, dog_molecule.go, checkpoint_dog.go, doctor_dog.go), `internal/scheduler/capacity` (config.go, pipeline.go, dispatch.go, state.go), `internal/session` (lifecycle.go, registry.go, names.go, stale.go, town.go, startup.go, pidtrack.go), `internal/tmux` (tmux.go: session creation, health, respawn hook, attach), `internal/keepalive`, `internal/estop`, `internal/quota` (scan.go, rotate.go, executor.go, state.go), `internal/nudge`, `internal/connection`, `plugins/stuck-agent-dog`
