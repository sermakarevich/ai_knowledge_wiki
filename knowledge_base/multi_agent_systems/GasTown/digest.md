> [[index|Wiki]] | [[summary|Summary]]

# GasTown — Digest

The whole source at medium depth: every component's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-orchestrator-town-rig-polecat|Orchestrator Core: Town, Rig, Crew, Polecat, Mayor]]
**In one sentence:** A Town (workspace directory identified by `mayor/town.json`) contains Rigs (one managed repository each, provisioned by `rig.Manager.AddRig`), and each rig hosts a persistent Mayor-adjacent identity layer, user-managed Crew clones, and Witness-managed Polecats whose persistent beads identity is kept separate from their ephemeral tmux sessions and per-assignment git worktrees.
- A Town is a workspace root (`~/gt/`) detected by walking up to the outermost `mayor/town.json` marker in `workspace.Find` (`internal/workspace/find.go:33`), with town identity in `TownConfig` (`internal/config/types.go:17`) and behavior in `TownSettings` (`internal/config/types.go:42`).
- A Rig is one managed git repository plus its agents, represented by the `Rig` struct (`internal/rig/types.go:9`) and created by `Manager.AddRig` (`internal/rig/manager.go:318`), which clones a shared bare repo (`.repo.git`), a mayor clone (`mayor/rig`), a refinery worktree (`refinery/rig`), and scaffolds `crew/`, `witness/`, `polecats/` directories.
- A Polecat is a Witness-managed worker with persistent identity but an ephemeral session: the `Polecat` struct (`internal/polecat/types.go:87`) carries seven lifecycle states (`internal/polecat/types.go:31`), while the live tmux session is retired on clean completion and the branch/MR evidence is left for refinery/cleanup (`docs/concepts/polecat-lifecycle.md:51`).
- Polecat identity is stored in the beads database (agent bead ID `<prefix>-<rig>-polecat-<name>` from `agentBeadID`, `internal/polecat/manager.go:403`, plus assignee `rig/polecats/name`, `internal/polecat/manager.go:394`); there is no per-polecat `state.json` — `loadFromBeads` derives state at query time from hooked/assigned beads cross-checked against tmux liveness (`internal/polecat/manager.go:2731`).
- Polecat spawn is `AllocateAndAdd` (`internal/polecat/manager.go:662`), which holds the pool flock across name allocation plus directory creation to close the GH#2215 TOCTOU race, then builds a git worktree on a generated branch `polecat/<name>/<issue>+<suffix>` (`internal/polecat/branch_name.go:22`).
- A Crew worker is a persistent, user-managed clone defined by `CrewWorker` (`internal/crew/types.go:8`) and created by `crew.Manager.Add` via full `git clone` (`internal/crew/manager.go:182`), with its own `state.json` persisted by atomic write (`internal/crew/manager.go:521`).
- The Mayor is a singleton persistent coordinator (one per machine, tmux session `hq-mayor` from `MayorSessionName`, `internal/session/names.go:16`) managed by `mayor.Manager` (`internal/mayor/manager.go:48`), with tmux and ACP modes combined in `CombinedStatus` (`internal/mayor/manager.go:53`).
- Concurrency between agents is file locking, not in-process mutexes: per-polecat `polecat-<name>.lock` and pool-wide `polecat-pool.lock` under `<rig>/.runtime/locks/` (`internal/polecat/manager.go:218`), per-crew `crew-<name>.lock` (`internal/crew/manager.go:168`), Boot's flock on `.boot-running` (`internal/boot/boot.go:89`), and Dolt optimistic-lock retry with backoff (`internal/polecat/manager.go:55`).

## 2. [[wiki/02-worktrees-hooks-persistence|Worktrees, Hooks, and Crash-Recovery Persistence]]
**In one sentence:** GasTown agents live in `git worktree` checkouts whose creation and deletion are serialized with per-polecat `flock` locks, while crash recovery is lazy and file-based: a `.polecat-checkpoint.json` snapshot plus surviving git state is re-displayed by the next session's startup hook, and shared settings files are protected against concurrent-writer corruption with atomic temp-plus-rename writes.
- "Hook" has three distinct meanings that must not be conflated: README-level Hook as git-worktree-backed persistent storage (`README.md:68`), beads-level Hook as an agent's pinned work-queue bead (`docs/glossary.md:69`), and code-level lifecycle hooks as Claude `settings.json` event commands (`internal/hooks/config.go:24`).
- Polecat worktree creation is `git worktree add -b <branch> <polecats/<name>/<rig>> <startPoint>` from the rig's repo base, executed under a pool lock plus a per-polecat `flock`, with full rollback (worktree removal, directory removal, name-pool release) on any failure (`internal/polecat/manager.go:662`, `internal/polecat/manager.go:725`, `internal/git/git.go:2281`).
- Worktree destruction is `git worktree remove [--force]` through the repo base, gated by uncommitted-work checks, pending merge-request blockers, shell-safety checks, and a best-effort push of unpushed commits — falling back to `os.RemoveAll` plus `worktree prune` only when the repo base is unusable (`internal/polecat/manager.go:1126`, `internal/polecat/manager.go:1231`, `internal/git/git.go:2409`).
- Crash state is a single JSON file, `<worktree>/.polecat-checkpoint.json`, capturing molecule, step, hooked bead, modified files, branch, last commit, timestamp, and session ID; it is written with plain `os.WriteFile` (mode `0600`), not with the atomic-write helper, so a crash mid-write can leave a corrupt file that `Read` reports as a parse error (`internal/checkpoint/checkpoint.go:20`, `internal/checkpoint/checkpoint.go:82`).
- Nobody detects crashes eagerly: the successor session's startup path (`gt prime --hook`) calls `checkpoint.Read` and treats a non-stale (<24h) checkpoint as `crash-recovery` state, then prints it as context — nothing is automatically re-applied, so committed history and on-disk files survive while in-memory reasoning is lost (`internal/cmd/prime_session.go:298`, `internal/cmd/prime_output.go:770`).
- `WIP: checkpoint (auto)` commits are the durable companion to the JSON snapshot: `CountWIPCommits`/`SquashWIPCommits` count or collapse them over `merge-base..HEAD` with a soft reset into one commit, preserving non-WIP subjects (`internal/checkpoint/squash.go:12`, `internal/checkpoint/squash.go:47`).
- Shared agent settings are crash-safe against concurrent spawns via `atomicfile.WriteFile` (unique temp file plus `rename`, gh#3500), used by both the Claude merge path and the template path — but the checkpoint writer does not use it (`internal/atomicfile/atomicfile.go:56`, `internal/hooks/config.go:266`, `internal/hooks/installer.go:146`).
- There is no lock inside the git wrapper itself: exclusion comes from polecat/pool `flock` files under `<rig>/.runtime/locks/`, plus a town-root mutation guard that refuses worktree-mutating git commands resolving to the town root (`internal/polecat/manager.go:218`, `internal/git/git.go:218`).

## 3. [[wiki/03-beads-ledger-convoy|Work Tracking: Beads Ledger, Convoys, Dolt Backend]]
**In one sentence:** GasTown tracks all work as beads (issues) in per-rig Dolt (SQL database with version control) databases, groups them into convoys that feed ready items to agents one at a time, and grinds stuck epics with Mountain stall detection plus Reaper cleanup of temporary wisps.
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

## 4. [[wiki/04-harness-adapters|Multi-Harness Support: Agent Adapters and Registry]]
**In one sentence:** GasTown supports many coder CLIs through a single data-driven registry (`AgentPresetInfo` in `internal/config/agents.go`) that declares each harness's launch command, resume style, hooks provider, and ACP mode — there is no per-harness Go adapter class.
- The harness "interface" is the `AgentPresetInfo` struct plus the `AgentRegistry` map and its accessor functions, all in `internal/config/agents.go:61-174` and `internal/config/agents.go:217-223`; a new harness is a new `builtinPresets` entry (`internal/config/agents.go:230`) or a JSON entry in `settings/agents.json`, never a new Go package.
- Thirteen built-in presets are compiled in: `claude`, `gemini`, `codex`, `kiro`, `cursor`, `auggie`, `amp`, `opencode`, `copilot`, `pi`, `omp`, `vibe` (Mistral), `groq-compound` (`internal/config/agents.go:23-55`); each entry fixes the exact CLI binary plus autonomous-mode flags, e.g. `copilot --yolo` (`internal/config/agents.go:406-431`).
- Launch is string/array construction, not a plugin call: `RuntimeConfig.BuildCommand()` (`internal/config/types.go:845-860`) concatenates `Command + Args`, and `BuildCommandWithPrompt()` (`internal/config/types.go:866-909`) appends the startup prompt positionally except for `opencode --prompt`, `copilot -i`, `gemini -i`.
- ACP (Agent Client Protocol, a JSON-RPC stdio protocol) is a second, structured execution path: `internal/acp/proxy.go:42-83` (`Proxy` struct) spawns the agent binary and bridges the UI and the agent over newline-delimited JSON-RPC, injecting the startup prompt as a `session/prompt` request (`internal/acp/proxy.go:786-823`).
- Only `opencode` ships ACP config today (`ACP: &ACPConfig{Command: "acp"}` at `internal/config/agents.go:402-404`, yielding `opencode acp`); three invocation modes (`native`, `subcommand`, `flag`) are defined at `internal/config/agents.go:197-201` and assembled in `internal/mayor/manager.go:271-317`.
- Wrappers are thin `gt prime`-then-`exec` shell scripts (`internal/wrappers/scripts/gt-codex:1-18`, plus `gt-gemini`, `gt-opencode`) installed to `~/bin` by `Install()` (`internal/wrappers/wrappers.go:16-40`); they cover harnesses whose hooks path is weak or absent (notably default `codex`, which has `SupportsHooks: false`).
- Hooks are installed by one generic installer reading preset metadata (`internal/hooks/installer.go:48-72`), with embedded templates per provider under `internal/hooks/templates/` (claude, gemini, codex, cursor, copilot, opencode, pi, omp, vibe); `internal/proxy` plus `cmd/gt-proxy-server` and `cmd/gt-proxy-client` are unrelated to harnesses — they are the mTLS sandbox proxy letting containers call `gt`/`bd` on the host.

## 5. [[wiki/05-daemon-scheduler-sessions|Runtime Supervision: Daemon, Scheduler, Sessions, Restarts]]
**In one sentence:** A single Go daemon runs a fixed 3-minute recovery heartbeat plus dedicated per-dog tickers, discovers agent liveness from tmux (not from stored state), and restarts dead sessions with exponential backoff while capacity-gated dispatch and sentinel files (ESTOP, pressure, quota) decide what may spawn.
- The daemon main loop (`Daemon.Run`) fires an immediate heartbeat then a fixed recovery heartbeat (default 3 minutes, config `operational.daemon.recovery_heartbeat_interval`) plus independent tickers per dog (quota 5m, doctor 5m, checkpoint 10m, compactor 24h, wisp reaper 1h, dolt backup 15m), so crash detection never waits on the slow tick (`internal/daemon/daemon.go:513`, `internal/daemon/daemon.go:842`, `internal/config/operational.go:48`).
- Stuck/crashed agents are detected four ways: GUPP violations (live session + hooked work + no bead update for 30m), orphaned work (dead session + hooked work left behind), Deacon heartbeat staleness with grace-period logic, and dog-lifecycle sweeps (dead-session working dogs, stale-working dogs idle 2h, idle dogs reaped after 1h) plus the `stuck-agent-dog` plugin scoped to polecats and Deacon only (`internal/daemon/lifecycle.go:1068`, `internal/daemon/lifecycle.go:1185`, `internal/daemon/daemon.go:1525`, `internal/daemon/handler.go:84`, `plugins/stuck-agent-dog/run.sh:2`).
- Every restart goes through a `RestartTracker` with exponential backoff (30s initial, x2 multiplier, 10m max, crash-loop at 5 restarts in 15m, reset after 30m stable, state in `daemon/restart_state.json`), and rate-limit pauses use a separate fixed 60s `RecordPause` that does not count toward the crash-loop budget (`internal/daemon/restart_tracker.go:44`, `internal/daemon/restart_tracker.go:169`, `internal/daemon/restart_tracker.go:217`).
- Worker restart is kill-then-recreate: `KillSessionWithProcesses` (disarm respawn hook, SIGTERM descendants, 2s grace, SIGKILL, kill session) followed by `EnsureSessionFreshWithCommandAndEnv` (skip if agent still alive, else fresh `tmux new-session` + `respawn-pane -k` with `-e` env flags); beads/Dolt state and git worktrees survive, the tmux pane process and in-memory agent context do not (`internal/tmux/tmux.go:637`, `internal/tmux/tmux.go:583`, `internal/daemon/lifecycle.go:415`).
- tmux sessions are per-town-socket (`basename-hash6`, e.g. `gt-a1b2c3`) with names `hq-mayor`, `hq-deacon`, `<prefix>-witness`, `<prefix>-refinery`, `<prefix>-crew-<name>`, `<prefix>-<polecat>`, `hq-dog-<name>`; health is a 3-level check (session exists, agent process alive via `GT_PROCESS_NAMES`, optional inactivity) and a `pane-died` hook auto-respawns crashed panes after a 3s debounce unless the daemon disarmed it for an intentional kill (`internal/session/registry.go:160`, `internal/session/names.go:16`, `internal/tmux/tmux.go:2421`, `internal/tmux/tmux.go:4385`).
- Capacity scheduling is pure functions in `internal/scheduler/capacity`: `PlanDispatch(capacity, batchSize, ready)` returns `ToDispatch/Skipped/Reason` (`capacity|batch|ready|none`), `DispatchCycle` runs query-plan-validate-execute with `OnSuccess` retried twice, cross-rig prefix mismatches are refused, and `max_polecats <= 0` means direct dispatch while `N > 0` means daemon-deferred dispatch (`internal/scheduler/capacity/pipeline.go:135`, `internal/scheduler/capacity/dispatch.go:50`, `internal/scheduler/capacity/config.go:16`).
- E-stop is a sentinel file (`$TOWN/ESTOP` with `trigger\ttimestamp\treason`, plus per-rig `ESTOP.<rig>`); when active the heartbeat returns early so the daemon stays alive for Dolt/maintenance but spawns or restarts nothing, and only the Mayor is exempt by convention (`internal/estop/estop.go:21`, `internal/estop/estop.go:42`, `internal/daemon/daemon.go:866`).
- Quota rotation is mechanical: the quota dog shells out to `gt quota rotate --json` (2m timeout), the scanner matches case-insensitive rate-limit regexes against the bottom 20 of 30 captured pane lines, the planner assigns one fresh account per `CLAUDE_CONFIG_DIR` round-robin, and the rotator swaps keychain tokens under a quota-file lock then restarts affected sessions (`internal/daemon/quota_dog.go:43`, `internal/quota/scan.go:88`, `internal/quota/rotate.go:63`, `internal/quota/executor.go:87`).

## 6. [[wiki/06-messaging-coordination|Messaging and Coordination: Mail, Events, Handoffs]]
**In one sentence:** Agents communicate through durable mail beads stored in Dolt (a version-controlled SQL database) plus file-based events and protocol mail, with handoffs as self-addressed mail for session continuity.
- Mail is durable beads issues with label `gt:message`: send runs `bd create --assignee`, receive queries by assignee and CC labels, read closes the bead or adds a `read` label (`internal/mail/router.go:1138`, `internal/mail/mailbox.go:146`).
- Every message routes to exactly one of direct address, queue, or channel, enforced by validation (`internal/mail/types.go:243`).
- Two-phase delivery tracks `delivery:pending` at send and `delivery:acked` plus acker identity and timestamp after the recipient reads (`internal/mail/delivery.go:12`).
- `mq` is not transport: it only generates merge-request identifiers (`<prefix>-mr-<10-hex>` from branch plus timestamp plus randomness) while `mail` carries the actual coordination traffic (`internal/mq/id.go:22`, `internal/mail/router.go:863`).
- Witness-Refinery coordination uses subject-prefixed protocol mail (`MERGE_READY`, `MERGED`, `FIX_NEEDED`, `REWORK_REQUEST`, `CONVOY_NEEDS_FEEDING`) with line-based `Key: value` bodies parsed by strict field parsers (`internal/protocol/types.go:60`, `internal/protocol/messages.go:517`).
- Handoffs are high-priority self-mail set to status `hooked` so the successor session auto-loads them, with stale hooked beads closed before each new handoff (`internal/cmd/handoff.go:1343`, `internal/beads/handoff.go:193`).
- Raw audit events (`~/gt/.events.jsonl`), curated user feed (`~/gt/.feed.jsonl`), human-readable town lifecycle log (`town/logs/town.log`), per-agent conversation telemetry (`agentlog`), and dashboard staleness colors (`activity`) are five separate record systems (`internal/events/events.go:110`, `internal/feed/curator.go:356`, `internal/townlog/logger.go:68`, `internal/agentlog/event.go:16`, `internal/activity/activity.go:37`).
- Shared-file conflicts are never auto-merged: the refinery rehearsal aborts on conflict, preserves the branch and merge-request bead, and files a conflict-resolution task or requests a polecat rebase (`internal/formula/formulas/mol-refinery-patrol.formula.toml:379`).

## 7. [[wiki/07-cli-tui-web-config|User Surface: CLI, TUI, Web UI, and Configuration]]
**In one sentence:** GasTown is driven by a single `gt` Cobra CLI (command registry in `internal/cmd`, theme/env handling in `internal/cli`, `internal/ui`, `internal/style`), with Bubble Tea TUIs for convoy/feed views and an htmx web dashboard, all configured through versioned JSON files under `mayor/`, `settings/`, and per-rig directories.
- The only user entry point is `cmd/gt/main.go:10`, which calls `cmd.Execute()`; `internal/cmd/root.go:25` owns the shared `rootCmd`, and every `gt <verb>` is a Cobra subcommand registered via `rootCmd.AddCommand` in an `init()` function (e.g. `internal/cmd/sling.go:172`).
- Help output is grouped by seven command groups declared in `internal/cmd/root.go:356`, wired into help order in `internal/cmd/root.go:371`; parent commands with subcommands reject bare/unknown invocations through `requireSubcommand` (`internal/cmd/root.go:402`).
- The binary name defaults to `gt` but is overridable with the `GT_COMMAND` environment variable (Environment Variable, a named setting a user can change to control program behavior) resolved in `internal/cli/name.go:17`.
- Work dispatch centers on `gt sling` (`internal/cmd/sling.go:25`), which resolves a rig target, spawns or reuses a polecat via `SpawnPolecatForSling` (`internal/cmd/polecat_spawn.go:102`), and tracks batches with convoys (`internal/cmd/convoy.go:176`).
- Supervision is split across role commands (`mayor`, `deacon`, `polecat`, `crew`, `witness`, `refinery`) that mostly manage tmux sessions (terminal multiplexer sessions, persistent background shells) per role, e.g. `internal/cmd/mayor.go:22` and `internal/cmd/polecat.go:31`.
- Interactive views are Bubble Tea (a Go framework for building terminal user interfaces) programs under `internal/tui/convoy/model.go:1` and `internal/tui/feed/model.go:1`, reached via flags such as `gt convoy --interactive` (`internal/cmd/convoy.go:407`) and `gt rig menu` (`internal/cmd/rig.go:865`).
- The web dashboard (`internal/web/handler.go:46`) is a read-mostly htmx view served by `gt dashboard` on port 8080 by default (`internal/cmd/dashboard.go:48`), with a JSON API under `/api/` (`internal/cmd/dashboard.go:151`).
- All durable settings are versioned JSON configs with explicit schema constants (e.g. town v2 in `internal/config/types.go:637`, daemon-patrol v1 in `internal/config/types.go:568`), loaded/saved by helpers in `internal/config/loader.go:527` and resolved per-agent through `AgentEnv` (`internal/config/env.go:94`).

## 8. [[wiki/08-safety-workflow-plugins|Safety, Workflow Abstraction, and Extensibility]]
**In one sentence:** GasTown isolates workers with file locks plus git worktrees, encodes repeatable work as versioned TOML formulas, and extends itself through Deacon-dispatched `plugin.md` patrol plugins — with merging done by git in the Refinery, not by any file-level merge logic.
- Agent identity locking is a JSON lockfile at `<worker>/.runtime/agent.lock` serialized by an adjacent `flock()` sidecar, with stale locks reaped only when the PID is dead *and* the tmux session is gone (`internal/lock/lock.go:54`, `internal/lock/lock.go:73`, `internal/lock/lock.go:264`).
- Formula *is* a workflow abstraction: four TOML types (convoy, workflow, expansion, aspect) with validation, cycle detection, topological sort, and ready-step queries, embedded in the binary and provisioned to `.beads/formulas/` (`internal/formula/types.go:16`, `internal/formula/parser.go:275`, `internal/formula/embed.go:16`).
- Formula resolution is three-tier — rig overrides town overrides embedded — with checksummed safe-update that never overwrites user edits (`internal/formula/embed.go:47`, `internal/formula/embed.go:308`).
- A plugin is a directory with `plugin.md` (`+++` TOML frontmatter + markdown) plus an optional `run.sh`; discovery is town-first then rig-override, execution is agent, script, or exec-wrapper, and dispatch goes through dogs during Deacon patrol (`internal/plugin/scanner.go:26`, `internal/plugin/types.go:112`).
- Deacon is a long-running Claude patrol agent (heartbeat-guarded); Refinery is the merge-queue Engineer with GitHub and Bitbucket PR providers behind one interface (`internal/deacon/heartbeat.go:1`, `internal/refinery/pr_provider.go:5`).
- Refinery merges with `MergeNoFF` locally or the VCS merge API when `merge_strategy="pr"`, serializes default-branch pushes through a merge slot, and sends conflicts back to the worker — there is no operational-transform or shared-file three-way merge in code (`internal/refinery/engineer.go:653`, `internal/refinery/engineer.go:1030`, `internal/git/git.go:1481`).
- Doctor runs 100+ registered checks (workspace, rig, binaries, git, hooks, patrol, beads, tmux, Dolt) with `--fix` support; `internal/health` holds the reusable TCP/SQL/zombie/backup probes shared with `gt health` (`internal/doctor/workspace_check.go:384`, `internal/health/health.go:25`).
- Gas City is a design-only declarative role/capability layer (one doc, no runtime package); Wasteland is DoltHub-based federation of towns, currently in unenforced "wild-west" Phase 1 (`docs/gas-city/crew-specialization-design.md:19`, `docs/WASTELAND.md:16`).

## 9. [[wiki/targeted|Targeted Analysis: What Fleet Can Learn]]
**In one sentence:** GasTown is a tmux plus git-worktree plus beads-on-Dolt orchestrator that isolates each worker, supervises sessions with backoff-governed restart, merges through a refinery instead of auto-merging, drives every harness from one data registry, and encodes repeatable work as TOML formulas — all patterns fleet can adopt directly.
- Town holds rigs and rigs hold isolated workers: town root resolves via `mayor/town.json`
  (`internal/workspace/find.go:20`); each rig is provisioned with a shared bare repo plus per-worker worktrees (`internal/rig/manager.go:318`).
- Worker restart is kill-then-recreate of the tmux pane under exponential backoff (30s, x2,
  10m cap, crash-loop at 5 in 15m) while beads rows and git branches survive (`internal/daemon/restart_tracker.go:44`, `internal/tmux/tmux.go:637`).
- Conflicts are never auto-merged: the refinery rehearses each branch merge, aborts on conflict,
  keeps branch and merge-request bead open, and mails rework to the worker (`internal/formula/formulas/mol-refinery-patrol.formula.toml:377`, `internal/refinery/engineer.go:653`).
- The workflow abstraction is Formula, a TOML language with four types plus validation, cycle
  detection, and ready-step queries, interpreted by agents rather than a runner (`internal/formula/types.go:16`, `internal/formula/parser.go:23`).
- Each harness is one data row, not one Go class: `AgentPresetInfo` plus `builtinPresets` declare
  binary, flags, resume style, and hooks provider for thirteen coders (`internal/config/agents.go:61`, `internal/config/agents.go:230`).
- Fleet relevance: adopt the harness registry, checkpoint plus lazy-recovery pair, restart backoff
  budget, worktree-per-worker plus rehearsal-abort merge rule, and file-based nudge queue
  (`internal/config/agents.go:230`, `internal/checkpoint/checkpoint.go:23`, `internal/daemon/restart_tracker.go:44`, `internal/nudge/queue.go:75`).

## The system in five moves
1. `gt sling` hooks a bead to an agent and `AllocateAndAdd` spawns a polecat worktree on a generated branch.
2. The polecat works in its tmux session while checkpoints and WIP commits preserve resumable state.
3. `gt done` pushes the branch and submits a merge-request bead that the witness verifies into `MERGE_READY` mail.
4. The refinery rehearses and lands the merge, then the convoy feeder dispatches the next ready issue.
5. The daemon heartbeat supervises liveness throughout and restarts dead sessions under backoff.
