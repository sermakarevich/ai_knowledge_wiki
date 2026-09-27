> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Targeted Analysis: What Fleet Can Learn from GasTown

**In one sentence:** GasTown is a tmux plus git-worktree plus beads-on-Dolt orchestrator
that isolates each worker, supervises sessions with backoff-governed restart, merges
through a refinery instead of auto-merging, drives every harness from one data registry,
and encodes repeatable work as TOML formulas — all patterns fleet can adopt directly.

## Key points
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
---
## 1. Design principles of the orchestrator?
- Town, Rig, worker form the hierarchy. A Town is a workspace root detected by walking up to the
  outermost `mayor/town.json`, with `GT_TOWN_ROOT` fallback when the cwd was deleted (`internal/workspace/find.go:20`, `internal/workspace/find.go:90`). See [[01-orchestrator-town-rig-polecat|Orchestrator Core]].
- A Rig is one managed git repository plus its agents: the `Rig` struct (`internal/rig/types.go:9`)
  created by `Manager.AddRig`, which clones a shared bare repo, a mayor clone, and a refinery worktree
  before scaffolding crew, witness, and polecat directories (`internal/rig/manager.go:318`, `internal/rig/manager.go:424`). See [[01-orchestrator-town-rig-polecat|Orchestrator Core]].
- Beads database is the source of truth. Polecat state derives at query time from beads assignee
  fields cross-checked against tmux liveness, with no per-polecat `state.json` (`internal/polecat/manager.go:2731`); crew workers are the deliberate exception with atomic `state.json` writes (`internal/crew/manager.go:521`). See [[01-orchestrator-town-rig-polecat|Orchestrator Core]].
- Discover liveness, never trust stored flags. The daemon derives observable state from tmux each
  tick (`internal/daemon/lifecycle.go:946`); stuck agents surface via GUPP violations, orphaned work,
  heartbeat staleness, and dog-lifecycle sweeps (`internal/daemon/lifecycle.go:1068`). See [[05-daemon-scheduler-sessions|Runtime Supervision]].
- Isolate each worker in its own worktree on its own branch (`polecats/<name>/<rig>/` on
  `polecat/<name>/<issue>+<suffix>`), the documented persistent-storage unit surviving crashes and
  restarts (`internal/polecat/manager.go:733`, `internal/polecat/branch_name.go:22`, `README.md:68`). See [[02-worktrees-hooks-persistence|Worktrees and Persistence]].
- Coordinate across processes with file locks, not mutexes: per-polecat plus pool-wide locks under
  `<rig>/.runtime/locks/` (`internal/polecat/manager.go:218`), plus a JSON `agent.lock` with flock
  sidecar reaped only when PID is dead and the tmux session is gone (`internal/lock/lock.go:54`, `internal/lock/lock.go:259`). See [[08-safety-workflow-plugins|Safety and Workflow]].
- Run the daemon as recovery safety net, not primary scheduler: event-driven wake via
  `bd activity --follow` plus a fixed 3-minute recovery heartbeat with ordered phases
  (`internal/daemon/daemon.go:50`, `internal/daemon/daemon.go:853`, `internal/config/operational.go:48`), fanned out per rig through a bounded pool (`internal/daemon/worker.go:21`). See [[05-daemon-scheduler-sessions|Runtime Supervision]].
- Gate every spawn on capacity and sentinels: `PlanDispatch` computes `ToDispatch/Skipped/Reason`
  from capacity, batch, and ready counts (`internal/scheduler/capacity/pipeline.go:135`); E-stop files
  freeze spawns and restarts while the daemon stays alive (`internal/estop/estop.go:21`, `internal/daemon/daemon.go:866`); load, memory, and session caps form a pressure gate (`internal/daemon/pressure.go:43`). See [[05-daemon-scheduler-sessions|Runtime Supervision]].
- Merge through a queue, never direct to main: workers must not push to main since the refinery
  merges from the merge queue (`internal/formula/formulas/mol-polecat-work.formula.toml:31`), landing
  locally with `MergeNoFF` or via the VCS API under `merge_strategy="pr"` (`internal/refinery/engineer.go:653`). See [[08-safety-workflow-plugins|Safety and Workflow]].
- Fleet relevance: fleet already mirrors Town/Rig/worker with its Python orchestrator plus isolated
  worktrees, so the transferable half is beads-as-truth, discover-don't-track supervision, and the capacity plus E-stop gates around spawn.

## 2. How are worker restarts handled (crash recovery, context persistence)?
- The daemon runs a fixed recovery heartbeat plus per-dog tickers: `Daemon.Run` takes a per-town file
  lock, fires an immediate heartbeat, then multiplexes quota, doctor, checkpoint, compactor, reaper, and
  backup tickers in one select loop (`internal/daemon/daemon.go:446`, `internal/daemon/daemon.go:513`). See [[05-daemon-scheduler-sessions|Runtime Supervision]].
- Detection lists agent beads then probes tmux for ground truth, merging `bd list --label=gt:agent`
  with wisp listings before matching `<prefix>-<rig>-polecat-<name>` identities
  (`internal/daemon/lifecycle.go:987`), with a TOCTOU guard re-reading `hook_bead` before any
  orphaned-work notification (`internal/daemon/lifecycle.go:1207`). See [[05-daemon-scheduler-sessions|Runtime Supervision]].
- GUPP violations (live session plus hooked work plus no bead update for 30m) mail the witness without
  killing anything (`internal/daemon/lifecycle.go:1090`); orphaned work (dead session plus hooked work)
  notifies only after liveness re-verification (`internal/daemon/lifecycle.go:1255`). See [[05-daemon-scheduler-sessions|Runtime Supervision]].
- `checkPolecatSessionHealth` reports crashed polecats with work on hook while idle reaping kills timed-out
  sessions (`internal/daemon/daemon.go:2593`); Deacon heartbeat staleness triggers `restartStuckDeacon`
  unless crash-loop state suppresses it (`internal/daemon/daemon.go:1525`). See [[05-daemon-scheduler-sessions|Runtime Supervision]].
- Every restart passes through one backoff tracker: 30s initial, 10m max, x2 multiplier, crash-loop at
  5 restarts in 15m, reset after 30m stable (`internal/daemon/restart_tracker.go:44`); rate-limit pauses
  use a separate fixed 60s `RecordPause` outside the crash-loop budget (`internal/daemon/restart_tracker.go:217`). See [[05-daemon-scheduler-sessions|Runtime Supervision]].
- Gating consults the tracker first: `ensureDeaconRunning` skips with remaining-time hints in backoff and
  points at `gt daemon clear-backoff` in crash-loop (`internal/daemon/daemon.go:1463`); a 30s mass-death
  window alerts at 3 deaths instead of restarting into systemic failure (`internal/daemon/daemon.go:147`). See [[05-daemon-scheduler-sessions|Runtime Supervision]].
- Restart is kill-then-recreate of the tmux pane: `KillSessionWithProcesses` disarms the respawn hook,
  SIGTERMs descendants, waits 2s, SIGKILLs stragglers, then kills the session (`internal/tmux/tmux.go:637`);
  `EnsureSessionFreshWithCommandAndEnv` skips the kill when the agent is alive, else builds a fresh session
  with env via `tmux new-session -e` (`internal/tmux/tmux.go:583`, `internal/tmux/tmux.go:402`). See [[05-daemon-scheduler-sessions|Runtime Supervision]].
- Lifecycle requests are claim-then-execute (deleted before acting) so a mid-restart daemon crash never
  replays them, and requests older than 6h are discarded (`internal/daemon/lifecycle.go:92`, `internal/daemon/lifecycle.go:40`). See [[05-daemon-scheduler-sessions|Runtime Supervision]].
- What survives is everything outside the pane: beads/Dolt writes are immediate so no sync is needed,
  and persistent-clone roles get `git fetch` plus `git pull --rebase` with auto-stash around dirty trees
  (`internal/daemon/lifecycle.go:636`); re-provisioned are session, startup command, `AgentEnv` identity set,
  theme, pane ID, PID file, and the `pane-died` hook (`internal/daemon/lifecycle.go:500`, `internal/session/pidtrack.go:45`). See [[05-daemon-scheduler-sessions|Runtime Supervision]].
- What is lost is in-memory context plus un-checkpointed edits (conversation, tool history, shell state,
  unwritten worktree changes), which is why the checkpoint dog auto-commits dirty polecat worktrees every
  10m (`internal/daemon/checkpoint_dog.go:50`). See [[05-daemon-scheduler-sessions|Runtime Supervision]].
- The checkpoint file captures the git-observable half: `<worktree>/.polecat-checkpoint.json` stores
  molecule, step, hooked bead, modified files, branch, commit, timestamp, session ID
  (`internal/checkpoint/checkpoint.go:23`), filled from `git status` plus `rev-parse` (`internal/checkpoint/checkpoint.go:119`). See [[02-worktrees-hooks-persistence|Worktrees and Persistence]].
- The writer is fragile in a known way: direct `os.WriteFile` at `0600` without the atomic helper
  (`internal/checkpoint/checkpoint.go:96`), so a mid-write crash leaves a corrupt file that `Read`
  surfaces as a parse error (`internal/checkpoint/checkpoint.go:62`). See [[02-worktrees-hooks-persistence|Worktrees and Persistence]].
- Recovery is lazy at the next session start: the `SessionStart` hook runs `gt prime --hook`, reporting
  `crash-recovery` for polecat/crew roles when a parseable checkpoint under 24h exists
  (`internal/cmd/prime_session.go:298`); `outputCheckpointContext` prints it as advisory context that is
  never auto-applied, and deletes checkpoints over 24h (`internal/cmd/prime_output.go:770`). See [[02-worktrees-hooks-persistence|Worktrees and Persistence]].
- Durable companions harden the snapshot: `WIP: checkpoint (auto)` commits counted over
  `merge-base..HEAD` and collapsed by soft reset preserving non-WIP subjects (`internal/checkpoint/squash.go:12`,
  `internal/checkpoint/squash.go:47`); handoffs add continuity as self-mail flipped to `hooked` status for
  auto-load, with prior stale hooked beads closed first (`internal/cmd/handoff.go:1343`, `internal/beads/handoff.go:193`). See [[02-worktrees-hooks-persistence|Worktrees and Persistence]] and [[06-messaging-coordination|Messaging]].
- Fleet relevance: no crash-detector process is needed — a session-probing heartbeat, a backoff tracker
  with crash-loop budget, and a checkpoint file re-read at worker start reproduce the whole restart story.

## 3. How are worker conflicts resolved (shared files, merge strategy, locking)?
- Isolation removes the shared-file problem first: each polecat works on a fresh per-bead branch in its
  own worktree, so two workers never edit one checkout (`internal/polecat/manager.go:733`); pushing
  directly to main is contractually forbidden (`internal/formula/formulas/mol-polecat-work.formula.toml:31`). See [[08-safety-workflow-plugins|Safety and Workflow]].
- Nothing auto-merges conflicting edits: the refinery rehearses each branch merge and aborts immediately
  so the repo never stays conflicted (`internal/formula/formulas/mol-refinery-patrol.formula.toml:377`),
  recording SHAs, filing a `Resolve merge conflicts` task, leaving branch and merge-request bead open, and
  moving on (`internal/formula/formulas/mol-refinery-patrol.formula.toml:418`). See [[06-messaging-coordination|Messaging]].
- Conflicted branches are never deleted by automation (detection keys off leftover `.git/MERGE_HEAD`),
  so the worker can rebase, force-push, and resubmit via `gt done`
  (`internal/formula/formulas/mol-refinery-patrol.formula.toml:418`, `internal/formula/formulas/mol-refinery-patrol.formula.toml:366`). See [[06-messaging-coordination|Messaging]].
- Rework returns through typed protocol mail: `REWORK_REQUEST` carries conflict files plus fetch, rebase,
  and force-push instructions via the witness (`internal/protocol/messages.go:229`,
  `internal/protocol/witness_handlers.go:223`); test/build failures take the parallel `FIX_NEEDED` path with
  attempt counting so the worker fixes in place (`internal/protocol/messages.go:138`). See [[06-messaging-coordination|Messaging]].
- One engineer merges with two landing modes: verify branch head, checkout target, pull origin, run
  `CheckConflicts`, push submodule commits first, run gates (`internal/refinery/engineer.go:504`,
  `internal/git/git.go:1876`), then delegate to the PR provider under `MergeStrategy == "pr"` or land
  locally with `MergeNoFF` preserving the worker message (`internal/refinery/engineer.go:653`, `internal/git/git.go:1481`). See [[08-safety-workflow-plugins|Safety and Workflow]].
- Default-branch pushes serialize through a merge slot with post-squash gates; failures reset the merge
  with labels mapping to `needs-rebase`, `needs-fix`, or `needs-retry` (`internal/refinery/engineer.go:1030`,
  `internal/refinery/types.go:292`); helpers expose `Merge`, `MergeNoFF`, `MergeFFOnly`, `MergeSquash`, and
  `AbortMerge` (`internal/git/git.go:1475`, `internal/git/git.go:1865`). See [[08-safety-workflow-plugins|Safety and Workflow]].
- PR operations stay vendor-neutral behind `PRProvider` (find, approval-check, merge) with `gh` CLI and
  Bitbucket REST implementations (`internal/refinery/pr_provider.go:7`, `internal/refinery/pr_provider_github.go:8`, `internal/refinery/pr_provider_bitbucket.go:8`). See [[08-safety-workflow-plugins|Safety and Workflow]].
- Spawn locking nests worker lock inside pool lock: `AllocateAndAdd` holds the pool flock across allocation
  plus directory creation, acquires the per-polecat flock inside that window, then releases the pool lock
  (`internal/polecat/manager.go:662`); a `.pending` reservation marker covers the residual gap (`internal/polecat/manager.go:489`). See [[01-orchestrator-town-rig-polecat|Orchestrator Core]].
- Removal locking orders destructive gates: `RemoveWithOptions` takes the per-polecat lock, then runs
  uncommitted-work, merge-request, bead-reset, shell-safety, and best-effort-push gates in fixed order
  (`internal/polecat/manager.go:1126`, `internal/polecat/manager.go:1231`), falling back from
  `git worktree remove` to `RemoveAll` plus prune only when the repo base is unusable (`internal/git/git.go:2409`). See [[02-worktrees-hooks-persistence|Worktrees and Persistence]].
- The git layer guards what locks cannot: `guardUnsafeTownRootMutation` refuses worktree-mutating commands
  resolving to the town root or touching `mayor/`, `.dolt-data/`, `.runtime/`, `.beads/`, `daemon/`
  (`internal/git/git.go:218`); bead attach/detach uses per-bead advisory locks (`internal/beads/handoff.go:233`). See [[02-worktrees-hooks-persistence|Worktrees and Persistence]].
- Shared settings survive concurrent spawns via `atomicfile.WriteFile` (unique temp file plus rename),
  the fix for truncated JSON under parallel spawns (`internal/atomicfile/atomicfile.go:56`,
  `internal/hooks/installer.go:146`); the checkpoint writer remains the known direct-write exception (`internal/checkpoint/checkpoint.go:101`). See [[02-worktrees-hooks-persistence|Worktrees and Persistence]].
- Fleet relevance: keep one worktree per worker, rehearse merges with abort-on-conflict, return rework as
  structured messages, and serialize slot allocation with nested file locks.

## 4. Is there a workflow abstraction? How is it implemented (files, classes, DSL/YAML)?
- Yes: Formula is a TOML definition language plus a planning library (parse, validate, sort, ready-step
  queries) that agents execute; no central runner steps through it (`internal/formula/parser.go:23`). See [[08-safety-workflow-plugins|Safety and Workflow]].
- One struct covers four types: `convoy` (parallel legs plus synthesis), `workflow` (sequential steps with
  `needs`), `expansion` (template-generated steps), `aspect` (parallel analysis), with `pour`, `agent`,
  `review_only`, and `extends`/`compose` inheritance (`internal/formula/types.go:16`, `internal/formula/types.go:28`); steps add `target`, `parallel`, `interactive`, and Ralph-loop `acceptance` (`internal/formula/types.go:121`). See [[08-safety-workflow-plugins|Safety and Workflow]].
- The planning API answers what can run next: `Validate` checks required fields, unique IDs, and known refs;
  DFS detects cycles and Kahn's algorithm sorts (`internal/formula/parser.go:23`, `internal/formula/parser.go:213`);
  `ReadySteps` and `ParallelReadySteps` project a completed set onto runnable steps (`internal/formula/parser.go:365`, `internal/formula/parser.go:435`). See [[08-safety-workflow-plugins|Safety and Workflow]].
- Overlays specialize formulas per rig or town without forking: patches apply with `replace`, `append`, or
  `skip` modes and the rig overlay wins outright (`internal/formula/overlay.go:8`, `internal/formula/overlay.go:31`). See [[08-safety-workflow-plugins|Safety and Workflow]].
- Distribution is embedded files with three-tier resolution: about 45 formulas ship in the binary via
  `//go:embed formulas/*.formula.toml` (`internal/formula/embed.go:16`); resolution prefers rig, then town,
  then embedded (`internal/formula/embed.go:47`); provisioning copies without overwriting while tracking
  SHA-256 in `.installed.json`, and updates refresh only safe entries (`internal/formula/embed.go:173`, `internal/formula/embed.go:308`). See [[08-safety-workflow-plugins|Safety and Workflow]].
- Worked examples span both ends: `gastown-release.formula.toml` is a `workflow` with required version vars
  and sequential `[[steps]]` from preflight checks (`internal/formula/formulas/gastown-release.formula.toml:29`);
  `mol-polecat-work.formula.toml` is the long worker contract with self-cleaning `gt done`, load-bearing
  branch names, and mandatory rebase plus pre-verified gates (`internal/formula/formulas/mol-polecat-work.formula.toml:1`). See [[08-safety-workflow-plugins|Safety and Workflow]].
- Convoy is the batch-workflow object on beads relations: a bead of type `convoy` whose membership edges
  are `tracks` dependencies (`internal/convoy/operations.go:94`, `internal/convoy/operations.go:356`), with
  owner, notify, molecule, merge, base branch, and watcher fields as `key: value` description lines (`internal/beads/fields.go:261`). See [[03-beads-ledger-convoy|Beads and Convoys]].
- The feed loop dispatches exactly one ready issue per close event: sort by priority then ID, keep open plus
  unassigned plus slingable leaf types (`task`, `bug`, `feature`, `chore`), reject blocked, skip parked rigs,
  dispatch via `gt sling --no-boot` (`internal/convoy/operations.go:285`, `internal/convoy/operations.go:612`); staged convoys stay inert until launch (`internal/convoy/operations.go:124`). See [[03-beads-ledger-convoy|Beads and Convoys]].
- Mountains add stall handling in the same shape: a convoy bead with the `mountain` label
  (`internal/witness/mountain.go:107`); each worker failure bumps `mountain:failures:N`, and at
  `MountainMaxFailures = 3` the issue flips to `blocked` with `mountain:skipped` so feeding grinds around
  it (`internal/witness/mountain.go:131`, `internal/witness/mountain.go:22`, `internal/witness/mountain.go:231`). See [[03-beads-ledger-convoy|Beads and Convoys]].
- Plugins are the second extensibility axis: a directory with `plugin.md` frontmatter plus markdown and
  optional `run.sh` switching agent-interpreted to script execution (`internal/plugin/scanner.go:26`,
  `internal/plugin/types.go:112`); gates are `cooldown`, `cron`, `condition`, `event`, or `manual`, dispatched
  through dogs during Deacon patrol (`internal/plugin/types.go:83`). See [[08-safety-workflow-plugins|Safety and Workflow]].
- Fleet relevance: a TOML workflow file with typed steps, a `ReadySteps` equivalent over beads
  dependencies, and a one-ready-issue convoy feeder give fleet repeatable batches without a workflow engine.

## 5. Can it support different harnesses/coders (Claude Code, Codex, Gemini, Copilot)? How is that implemented (adapter/registry/plugin)?
- Yes via a data registry, not adapter classes: thirteen presets compile in (`claude`, `gemini`, `codex`,
  `kiro`, `cursor`, `auggie`, `amp`, `opencode`, `copilot`, `pi`, `omp`, `vibe`, `groq-compound`)
  (`internal/config/agents.go:23`); no `Harness` interface and no per-harness package exist. See [[04-harness-adapters|Harness Adapters]].
- The harness contract is the `AgentPresetInfo` struct (binary, args, env, process names, resume flag and
  style, hooks provider and paths, prompt mode, ready delay, instructions file, optional ACP config)
  (`internal/config/agents.go:61`); compiled-in `builtinPresets` merge with town/rig JSON where same-name
  keys override (`internal/config/agents.go:230`, `internal/config/agents.go:572`). See [[04-harness-adapters|Harness Adapters]].
- Lookup resolves presets into the spawnable shape: `GetAgentPreset` / `GetAgentPresetByName` /
  `ListAgentPresets` read the merged registry (`internal/config/agents.go:678`, `internal/config/agents.go:695`);
  `RuntimeConfigFromPreset` converts to the `RuntimeConfig` that tmux creation executes (`internal/config/agents.go:722`). See [[04-harness-adapters|Harness Adapters]].
- Launch is argv construction: `BuildCommand` joins command plus quoted args for tmux paths
  (`internal/config/types.go:845`); `BuildCommandWithPrompt` appends the startup beacon positionally except
  `opencode --prompt`, `copilot -i`, `gemini -i` (`internal/config/types.go:866`). See [[04-harness-adapters|Harness Adapters]].
- Exact autonomous argv is pinned per harness: `claude --dangerously-skip-permissions` with flag resume
  (`internal/config/agents.go:231`), `codex` bypass-approvals flags with `resume` subcommand
  (`internal/config/agents.go:281`), `gemini --approval-mode yolo` (`internal/config/agents.go:257`),
  `copilot --yolo` (`internal/config/agents.go:406`); `groq-compound` reuses the Claude binary redirected
  purely by env (`internal/config/agents.go:510`). See [[04-harness-adapters|Harness Adapters]].
- Resume covers both CLI conventions via `BuildResumeCommand` (`<flag> <sessionID>` versus
  `codex resume <id>`) (`internal/config/agents.go:759`); headless shapes live in `NonInteractiveConfig`
  such as codex `exec --json` (`internal/config/agents.go:203`). See [[04-harness-adapters|Harness Adapters]].
- Selection resolves per role through layered overrides: role override, rig `agent`, town `default_agent`,
  then `"claude"` fallback, each looked up rig-custom, town-custom, built-in (`internal/config/loader.go:1314`);
  settings expose `default_agent`, `agents`, `role_agents`, `crew_agents` for this (`internal/config/types.go:42`). See [[04-harness-adapters|Harness Adapters]] and [[07-cli-tui-web-config|CLI and Config]].
- Liveness stays harness-aware without special cases: health reads `pane_current_command` against preset
  `ProcessNames` with wrapper-aware resolution (`internal/config/agents.go:932`); startup env seeds
  `GT_PROCESS_NAMES` so custom agents detect from the first shell (`internal/tmux/tmux.go:402`). See [[04-harness-adapters|Harness Adapters]].
- ACP is the structured alternative to keystrokes: `Proxy` spawns the agent binary and bridges UI and agent
  over newline-delimited JSON-RPC, injecting the startup prompt as `session/prompt` after the handshake
  (`internal/acp/proxy.go:42`, `internal/acp/proxy.go:786`); only `opencode` ships ACP config today as
  `opencode acp` (`internal/config/agents.go:402`). See [[04-harness-adapters|Harness Adapters]].
- Wrappers cover weak-hooks harnesses: `gt-codex` / `gt-gemini` / `gt-opencode` print context via `gt prime`
  then `exec` the real CLI preserving argv (`internal/wrappers/scripts/gt-codex:1`, `internal/wrappers/wrappers.go:16`); default `codex` sets `SupportsHooks: false`, hence stays on the wrapper path (`internal/config/agents.go:289`). See [[04-harness-adapters|Harness Adapters]].
- Hooks install from one generic installer reading preset metadata (`internal/runtime/runtime.go:25`,
  `internal/hooks/installer.go:48`) with embedded templates per provider under `internal/hooks/templates/`
  (`internal/hooks/installer.go:213`); missing-hooks harnesses fall back to beacon-plus-delayed-nudge delivery
  (`internal/runtime/runtime.go:232`, `internal/runtime/runtime.go:219`). See [[04-harness-adapters|Harness Adapters]].
- Fleet relevance: copy the three-layer shape of registry row, wrapper script, and hook template per coder
  to support new harnesses without harness-specific orchestration code.

## 6. What concrete features/ideas can fleet borrow?
1. Data-driven harness registry instead of per-coder adapters. Mirror the `AgentPresetInfo` table
  (command, args, env, process names, resume flag/style, hooks provider, prompt mode) with built-ins merged
  under JSON overrides (`internal/config/agents.go:61`, `internal/config/agents.go:230`). Why for fleet: one
  Python dict plus a `build_command` equivalent spawns Claude Code, Codex, Gemini, and Copilot with no harness-specific code.
2. Checkpoint file plus lazy `prime --hook` recovery. Persist molecule, step, hooked bead, modified files,
  branch, commit, timestamp per worktree on a timer, then re-display as advisory context at next worker start
  (`internal/checkpoint/checkpoint.go:23`, `internal/cmd/prime_session.go:298`, `internal/cmd/prime_output.go:770`). Why
  for fleet: beads plus git already survive death; this closes the context gap in under a hundred lines of Python.
3. RestartTracker backoff with crash-loop budget and separate pause path. Adopt 30s initial, x2, 10m cap,
  5-in-15m circuit open, 30m stable reset, plus fixed 60s non-budget pause for rate limits
  (`internal/daemon/restart_tracker.go:44`, `internal/daemon/restart_tracker.go:217`). Why for fleet: stops restart
  storms on broken worktrees or credentials and separates quota waits from true crashes.
4. Worktree-per-worker plus rehearsal-abort merge rule. Keep one branch per worker, rehearse each merge,
  abort on conflict, preserve branch and merge-request bead, return structured rebase instructions
  (`internal/git/git.go:2281`, `internal/formula/formulas/mol-refinery-patrol.formula.toml:377`, `internal/protocol/messages.go:229`). Why
  for fleet: fleet already isolates coders in worktrees; this adds the merge-side policy keeping shared branches green.
5. Pool-plus-per-worker flock allocation protocol. Hold the pool lock across name allocation and directory
  creation, nest the worker lock inside, plant a `.pending` reservation for reconcile visibility
  (`internal/polecat/manager.go:662`, `internal/polecat/manager.go:489`). Why for fleet: concurrent spawns otherwise
  double-allocate one worktree slot between registry save and directory creation.
6. Atomic temp-plus-rename writes for every shared JSON file. Write unique temp names in the target directory
  then rename so readers always see one complete writer (`internal/atomicfile/atomicfile.go:56`); pin with a
  concurrent-spawn regression test as upstream did (`internal/hooks/installer_concurrent_test.go:13`). Why for fleet:
  centralized beads state plus per-worktree settings hit the same truncation race under parallel spawns.
7. Convoy `tracks`-edge feeder for batch orchestration without a scheduler. Group beads under one convoy bead;
  per close event dispatch exactly one ready issue (open, unassigned, slingable, unblocked) ordered by priority
  then ID (`internal/convoy/operations.go:285`, `internal/convoy/operations.go:612`); add failure-count labels with
  auto-skip at 3 (`internal/witness/mountain.go:131`). Why for fleet: one query plus one spawn per completion event
  gives batch throughput with no daemon rewrite.
8. File-based nudge queue instead of keystroke injection. Drop JSON reminders into
  `.runtime/nudge_queue/<session>/` with TTL and depth caps, claim via rename for exactly-once delivery, render
  as `<system-reminder>` at the next turn boundary (`internal/nudge/queue.go:75`, `internal/nudge/queue.go:164`). Why
  for fleet: typing into a live coder session cancels in-flight tool calls, while the queue cooperates with any harness loop.

**Covers:** wiki/01-08 plus repo files consulted: internal/workspace/find.go, internal/rig/manager.go,
internal/polecat/manager.go, internal/crew/manager.go, internal/daemon/daemon.go, internal/daemon/lifecycle.go,
internal/daemon/restart_tracker.go, internal/daemon/checkpoint_dog.go, internal/daemon/worker.go, internal/tmux/tmux.go,
internal/session/pidtrack.go, internal/git/git.go, internal/checkpoint/checkpoint.go, internal/checkpoint/squash.go,
internal/cmd/prime_session.go, internal/cmd/prime_output.go, internal/cmd/handoff.go, internal/beads/handoff.go,
internal/config/agents.go, internal/config/types.go, internal/config/loader.go, internal/config/operational.go,
internal/scheduler/capacity/pipeline.go, internal/estop/estop.go, internal/daemon/pressure.go, internal/atomicfile/atomicfile.go,
internal/lock/lock.go, internal/lock/flock_unix.go, internal/convoy/operations.go, internal/beads/fields.go,
internal/witness/mountain.go, internal/formula/types.go, internal/formula/parser.go, internal/formula/embed.go,
internal/formula/overlay.go, internal/plugin/scanner.go, internal/plugin/types.go, internal/refinery/engineer.go,
internal/refinery/pr_provider.go, internal/protocol/messages.go, internal/protocol/witness_handlers.go, internal/acp/proxy.go,
internal/wrappers/wrappers.go, internal/hooks/installer.go, internal/runtime/runtime.go, internal/nudge/queue.go,
internal/mayor/manager.go, internal/quota/rotate.go, README.md
