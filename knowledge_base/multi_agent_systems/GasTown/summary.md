# Technical Analysis: gastown

**Repository:** https://github.com/gastownhall/gastown
**Version analyzed:** 1.2.1
**Date:** 2026-09-09

---
## 1. Overview / What Problem It Solves

GasTown is a Go orchestrator (~475K LOC, 1231 .go files, per wiki [[index|index]]) for running many AI coder CLIs in parallel against one or more git repositories without them clobbering each other. It solves three coordination problems: isolation (each worker gets its own git worktree on its own branch), work tracking (all tasks are beads — issue records — in per-rig Dolt SQL databases, fed to workers one at a time via convoys), and supervision (a daemon watches tmux session liveness, restarts dead workers with backoff, and merges finished branches through a refinery merge queue instead of letting workers push to main directly). GasTown never calls an LLM (Large Language Model) API itself; it spawns external coder CLIs (Claude Code, Codex, Gemini, Copilot, etc.) inside tmux sessions and feeds them context via `gt prime` hooks and startup prompts (see [[wiki/04-harness-adapters|harness adapters]]). Persistent state lives in Dolt databases plus git branches plus JSON config files; tmux panes and in-memory agent context are explicitly ephemeral and lost on restart.

## 2. High-Level Architecture (ASCII diagram with │ ▼ ─ ► connectors + 4-6 step data-flow narrative + persistent-state statement)

```
operator / Mayor
│  gt sling <bead> / gt convoy launch / gt mail send
▼
beads ledger (per-rig Dolt DB, port 3307) ──► convoy feeder ──► scheduler capacity gate
│  Issue rows (internal/beads/beads.go:176)      │ tracks edges           │ PlanDispatch (capacity|batch|ready|none)
▼                                                ▼                        ▼
polecat spawner (AllocateAndAdd) ──► git worktree (polecats/<name>/<rig>) ──► tmux session (<prefix>-<name>)
│  pool + per-polecat flock                       │ branch polecat/<name>/<issue>+<suffix>
▼                                                ▼                        ▼
harness CLI (claude/codex/gemini/...) ◄── gt prime --hook context ◄── SessionStart hook
│  works, commits, pushes branch
▼
gt done ──► protocol mail (MERGE_READY) ──► refinery engineer ──► MergeNoFF / PR API ──► main
│                                              │ rehearsal aborts on conflict, never auto-merges
▼                                              ▼
daemon heartbeat (3m) + dogs ──► witness (stuck/zombie patrol) ──► deacon (town watchdog) ──► mayor (coordinator)
```

Data-flow narrative (5 steps):

1. Work enters as beads: issues are created in the town (`hq`) or rig Dolt database; batches are grouped under a convoy bead via `tracks` dependency edges (`internal/convoy/operations.go:94`). On each close event, `feedNextReadyIssue` (`internal/convoy/operations.go:285`) picks exactly one ready issue (open, unassigned, slingable leaf type, unblocked) and dispatches it with `gt sling --no-boot` (`internal/convoy/operations.go:612`).
2. Dispatch spawns an isolated worker: `AllocateAndAdd` (`internal/polecat/manager.go:662`) holds the pool flock across name allocation plus directory creation (closing the GH#2215 race), creates a git worktree on branch `polecat/<name>/<issue>+<suffix>` (`internal/polecat/branch_name.go:22`), hooks the bead to the agent, and starts a tmux session named `<prefix>-<name>` (`internal/session/names.go:46`) running the configured harness binary.
3. The worker runs autonomously: the `SessionStart` hook executes `gt prime --hook`, which replays a `<24h` checkpoint file as advisory context or reports `crash-recovery` state (`internal/cmd/prime_session.go:298`); coordination with other agents happens through durable mail beads (label `gt:message`) plus file-based nudge queue entries rendered as `<system-reminder>` at turn boundaries (`internal/nudge/queue.go:75`), never through keystroke injection into a busy session.
4. Completion goes through the merge queue: `gt done` pushes the branch, submits a merge-request bead, clears the hook, marks agent state `done`, and kills its own session (`docs/concepts/polecat-lifecycle.md:51`); the refinery engineer verifies the branch head, rehearses the merge, aborts on conflict (filing a `Resolve merge conflicts` task instead), and lands via local `MergeNoFF` (`internal/git/git.go:1481`) or the VCS merge API when `merge_strategy="pr"` (`internal/refinery/engineer.go:653`).
5. Supervision runs continuously underneath: the daemon's fixed 3-minute recovery heartbeat plus per-dog tickers (quota 5m, doctor 5m, checkpoint 10m, compactor 24h, reaper 1h) detect GUPP violations (live session + hooked work + no update for 30m), orphaned work (dead session + hooked work), and heartbeat staleness, restarting through a `RestartTracker` (30s initial, x2, 10m max, crash-loop at 5 in 15m) while E-stop sentinels and pressure gates decide what may spawn (`internal/daemon/daemon.go:853`, `internal/daemon/restart_tracker.go:44`, `internal/estop/estop.go:21`).

Persistent-state statement: beads/Dolt rows, git branches/commits (including `WIP: checkpoint (auto)` commits), mail beads, `.polecat-checkpoint.json` files, and JSON configs survive restarts; tmux panes, in-memory conversation context, and un-checkpointed shell state do not — every restart is kill-then-recreate of the pane with `AgentEnv` identity re-injected (`internal/daemon/lifecycle.go:500`, `internal/tmux/tmux.go:637`).

## 3. The Town / Rig / Polecat Model

Town is the workspace root (`~/gt/`) detected by walking up to the outermost `mayor/town.json` marker (`internal/workspace/find.go:33`), with identity in `TownConfig` (`internal/config/types.go:17`) and behavior in `TownSettings` (`internal/config/types.go:42`); see [[wiki/01-orchestrator-town-rig-polecat|orchestrator core]]. Rig is one managed git repository plus its agents, provisioned by `Manager.AddRig` (`internal/rig/manager.go:318`) which clones a shared bare repo (`.repo.git`), a mayor clone (`mayor/rig`), a refinery worktree (`refinery/rig`), and scaffolds `crew/`, `witness/`, `polecats/`; per-rig identity is `rig/config.json` (`internal/config/types.go:650`). Polecat is the Witness-managed ephemeral worker: the `Polecat` struct (`internal/polecat/types.go:87`) carries seven states (`working`, `idle`, `done`, `review-needed`, `stuck`, `stalled`, `zombie` at `internal/polecat/types.go:31`), identity lives in beads (assignee `<rig>/polecats/<name>` at `internal/polecat/manager.go:394`, agent bead `<prefix>-<rig>-polecat-<name>` at `internal/polecat/manager.go:403`), and state is derived at query time by `loadFromBeads` cross-checking hooked beads against tmux liveness — there is no per-polecat `state.json` (`internal/polecat/manager.go:2731`). Crew workers are the persistent counterpart: user-managed full clones with atomic `state.json` (`internal/crew/manager.go:521`), never auto-collected, pushing to main directly instead of the refinery queue. Mayor is the singleton coordinator (tmux `hq-mayor` at `internal/session/names.go:16`, `CombinedStatus` merging tmux + ACP liveness at `internal/mayor/manager.go:53`); Boot is the ephemeral triage watchdog serialized by a flock on `.boot-running` (`internal/boot/boot.go:89`); Deacon is the long-running patrol agent guarded by `deacon/heartbeat.json` (5m stale / 20m very-stale at `internal/deacon/heartbeat.go:51`); Witness and Refinery are per-rig patrol/merge roles. Names come from a themed `NamePool` (default 50 slots, `mad-max` theme, `internal/polecat/namepool.go:23`) with `Allocate`/`Release`/`Reconcile-from-disk` semantics (`internal/polecat/namepool.go:270`). Concurrency is file locking, not mutexes: per-polecat `polecat-<name>.lock`, pool `polecat-pool.lock`, per-crew `crew-<name>.lock`, plus Dolt optimistic-lock retry with backoff (`internal/polecat/manager.go:218`, `internal/polecat/manager.go:55`).

## 4. LLM / External Service Integration (GasTown does NOT call LLMs itself — it launches agent harnesses; describe that design + the harness matrix explicitly)

GasTown contains no LLM client code and no model API keys: every model call happens inside an external coder CLI process that GasTown spawns in tmux. The entire harness contract is data, not Go interfaces — the `AgentPresetInfo` struct plus the `AgentRegistry` map and accessors in `internal/config/agents.go:61-174` and `internal/config/agents.go:217-223`; see [[wiki/04-harness-adapters|harness adapters]]. There is no `Harness` interface and no per-harness package; adding a coder means adding one `builtinPresets` row (`internal/config/agents.go:230`) or one JSON entry in `settings/agents.json`, never a new Go adapter. Launch is argv construction: `RuntimeConfig.BuildCommand()` (`internal/config/types.go:845-860`) concatenates `Command + Args`, and `BuildCommandWithPrompt()` (`internal/config/types.go:866-909`) appends the startup prompt positionally except `opencode --prompt`, `copilot -i`, `gemini -i`. Liveness reads `pane_current_command` against the preset's `ProcessNames` with wrapper-aware resolution (`internal/config/agents.go:932-1001`).

Harness matrix (13 built-in presets, exact autonomous argv per wiki):

| Preset | Command + Args | Resume style | Hooks |
|---|---|---|---|
| `claude` | `claude --dangerously-skip-permissions` | `--resume`/`--continue`, flag | claude templates |
| `gemini` | `gemini --approval-mode yolo` | `--resume`, flag | gemini templates |
| `codex` | `codex -c check_for_update_on_startup=false --dangerously-bypass-approvals-and-sandbox` | `resume` subcommand | none built-in (`SupportsHooks: false`), wrapper path |
| `kiro` | `kiro-cli chat --trust-all-tools` | `--resume-id`/`--resume`, flag | none |
| `cursor` | `cursor-agent -f` | `--resume`, flag | cursor `hooks.json` |
| `auggie` | `auggie --allow-indexing` | `--resume`, flag | none |
| `amp` | `amp --dangerously-allow-all --no-ide` | `threads continue` subcommand | none |
| `opencode` | `opencode` (YOLO via `OPENCODE_PERMISSION` env) | none | `gastown.js` plugin; only preset with ACP (`opencode acp`) |
| `copilot` | `copilot --yolo` | `--resume`/`--continue`, flag | copilot hooks dir |
| `pi` | `pi -e .pi/extensions/gastown-hooks.js` | none | pi extension |
| `omp` | `omp --hook .omp/hooks/gastown-hook.ts` | none | omp hook file |
| `vibe` (Mistral) | `vibe --agent auto-approve` | `--resume`/`--continue`, flag | vibe `config.toml` |
| `groq-compound` | `claude` binary + `ANTHROPIC_BASE_URL`/`ANTHROPIC_API_KEY=$GROQ_API_KEY` env redirect | flag | claude templates |

(Sources: `internal/config/agents.go:231-539`; ACP block at `internal/config/agents.go:402-404`; modes at `internal/config/agents.go:197-201`.) ACP (Agent Client Protocol, JSON-RPC over stdio) is a second execution path where `Proxy` (`internal/acp/proxy.go:42-83`) spawns the agent binary and bridges UI↔agent messages, injecting the startup prompt as `session/prompt` after the handshake (`internal/acp/proxy.go:786-823`); only `opencode` ships ACP config today. Harnesses without executable hooks fall back to `gt prime`-then-`exec` wrapper scripts (`internal/wrappers/scripts/gt-codex:1-18`, installed to `~/bin` by `internal/wrappers/wrappers.go:16-40`) plus beacon-plus-delayed-nudge delivery (`DefaultPrimeWaitMs = 2000`, `internal/runtime/runtime.go:219`). Selection resolves per role: role override → rig `agent` → town `default_agent` → `"claude"` fallback (`internal/config/loader.go:1314-1383`).

## 5. The Spawn-to-Merge Pipeline

Spawn: `gt sling <bead> <rig>` (`internal/cmd/sling.go:25`) resolves the rig, calls `SpawnPolecatForSling` (`internal/cmd/polecat_spawn.go:102`), and auto-creates a convoy unless `--no-convoy` (`internal/cmd/convoy.go:176`); see [[wiki/02-worktrees-hooks-persistence|worktrees]] and [[wiki/03-beads-ledger-convoy|convoys]]. `AllocateAndAdd` (`internal/polecat/manager.go:662`) serializes allocation, builds the worktree via `WorktreeAddFromRef` or `WorktreeAddExistingForce` for `--resume` (`internal/git/git.go:2281`, `internal/git/git.go:2317`), provisions `CLAUDE.md`/beads/`PRIME.md`/overlays/settings in fixed order, and rolls back fully (worktree removal, directory removal, name release) on any error (`internal/polecat/manager.go:741`). Work: the agent reads `gt prime` context, tracks its bead-Hook (the pinned work-queue bead per `docs/glossary.md:69`), checkpoints periodically (`<worktree>/.polecat-checkpoint.json` at `internal/checkpoint/checkpoint.go:20`, plus `WIP: checkpoint (auto)` commits squashed later at `internal/checkpoint/squash.go:47`), and coordinates via mail and protocol messages. Done: `gt done` (`internal/cmd/done.go:32`) pushes the branch, submits the merge-request bead, emits `POLECAT_DONE`, and kills its own session; the witness verifies and emits `MERGE_READY`, the refinery merges and emits `MERGED`, failures emit `FIX_NEEDED`/`REWORK_REQUEST` (`internal/protocol/messages.go:13`, `internal/protocol/messages.go:138`, `internal/protocol/messages.go:229`); see [[wiki/06-messaging-coordination|messaging]]. Merge: the engineer (`internal/refinery/engineer.go:504`) verifies head, pulls target, runs `CheckConflicts`, pushes submodule commits first, runs gates, then lands locally with `MergeNoFF` or delegates to the PR provider (`internal/refinery/engineer.go:636`), pushing through a serialized main-push slot (`internal/refinery/engineer.go:1030`); conflicts abort immediately, preserve branch + MR bead, and file a rework task (`internal/formula/formulas/mol-refinery-patrol.formula.toml:377`). Cleanup: refinery/cleanup owns the branch/worktree after merge; idle slots are reused only when `DecideWorkstate` says `SAFE_TO_NUKE` (`internal/polecat/workstate.go:59`) and `DecideSlotReuse` agrees (`internal/polecat/reuse.go:43`); otherwise `RemoveWithOptions` enforces uncommitted-work, pending-MR, and shell-safety gates (`internal/polecat/manager.go:1126`).

## 6. Key Files (table File | Lines | What It Does, 10-20 rows, most important first)

| File | Lines | What It Does |
|---|---|---|
| `internal/polecat/manager.go` | spawn (`:662`), remove (`:1126`), `loadFromBeads` (`:2731`) | Polecat lifecycle: allocation, worktree provisioning, query-time state derivation, gated removal |
| `internal/daemon/daemon.go` | `Run` (`:446`), `heartbeat` (`:853`) | Daemon main loop, 3m recovery tick, ordered per-tick phases, ESTOP/pressure gating |
| `internal/refinery/engineer.go` | `doMerge` (`:504`), land (`:653`), push slot (`:1030`) | Merge-queue engineer: verify, rehearse, gate, land via MergeNoFF or PR API |
| `internal/config/agents.go` | registry (`:61-174`), presets (`:230-539`) | Harness registry: 13 coder presets, resume styles, hooks providers, ACP configs |
| `internal/convoy/operations.go` | feeder (`:38`), `feedNextReadyIssue` (`:285`), dispatch (`:612`) | Convoy batch feeding: one ready issue per close event via `gt sling --no-boot` |
| `internal/mail/router.go` | send (`:863`, `:1113`), notify (`:1592`) | Mail transport: direct/queue/channel/announce routing, delivery labels, tmux nudges |
| `internal/tmux/tmux.go` | create (`:324`), kill (`:637`), health (`:2421`) | tmux substrate: session creation, kill-then-recreate restart, 3-level health check |
| `internal/git/git.go` | worktree add (`:2281`), merge set (`:1475-1494`), town-root guard (`:218`) | Git wrapper: worktree ops, merge variants, mutation guard, clone helpers |
| `internal/rig/manager.go` | `AddRig` (`:318`), `RegisterRig` (`:1632`) | Rig provisioning and adoption: bare repo, mayor clone, refinery worktree, beads init |
| `internal/beads/beads.go` | `Issue` (`:176`), wrapper (`:543`), `bd` shell-out (`:758`) | Bead schema (status/priority/type/assignee/labels/graph) and ledger access paths |
| `internal/daemon/lifecycle.go` | GUPP (`:1068`), orphans (`:1185`), restart exec (`:343`) | Detection-to-restart: violation scans, TOCTOU-guarded notify, kill-then-recreate |
| `internal/formula/parser.go` + `types.go` | types (`:16`), parse/validate/sort (`:23-365`) | Formula workflow language: 4 TOML types, cycle detection, topological sort, ready-steps |
| `internal/hooks/config.go` + `installer.go` | events (`:31`), merge (`:506`), install (`:48-72`) | Lifecycle-hook system: 8 event types, base/role/rig merge, atomic settings install |
| `internal/checkpoint/checkpoint.go` | struct (`:23`), write (`:96`), capture (`:119`) | Crash snapshot: git-observable state per worktree, re-displayed at next session start |
| `internal/cmd/sling.go` + `internal/cmd/polecat_spawn.go` | sling (`:25`), spawn (`:102`) | Dispatch entry: rig resolution, polecat spawn/reuse, convoy tracking |
| `internal/protocol/messages.go` | builders (`:13-290`), parser (`:517`) | Witness↔refinery protocol mail: MERGE_READY/MERGED/FIX_NEEDED/REWORK_REQUEST bodies |

## 7. Dependencies (table Package | Version constraint | Purpose from go.mod — read /var/folders/53/2mc9jwn935nfj9c8gtl12bhc0000gn/T/opencode/gastown/go.mod ONLY for this table; that one file read is allowed)

| Package | Version constraint | Purpose from go.mod |
|---|---|---|
| `github.com/spf13/cobra` | v1.10.2 | CLI command tree for the `gt` binary |
| `github.com/steveyegge/beads` | v1.0.5 | Issue-ledger library behind the beads work tracker |
| `github.com/charmbracelet/bubbletea` | v1.3.10 | Terminal UI runtime for convoy/feed interactive views |
| `github.com/charmbracelet/bubbles` | v1.0.0 | Reusable TUI widgets used with bubbletea |
| `github.com/charmbracelet/lipgloss` | v1.1.1-0.20250404203927 | Terminal styling for CLI/TUI output |
| `github.com/charmbracelet/glamour` | v0.10.0 | Markdown rendering in terminal views |
| `github.com/go-sql-driver/mysql` | v1.9.3 | MySQL driver for talking to the Dolt SQL server |
| `github.com/gofrs/flock` | v0.13.0 | File-lock primitive for pool/per-worker exclusion |
| `github.com/BurntSushi/toml` | v1.6.0 | TOML parsing for formula and config files |
| `gopkg.in/yaml.v3` | v3.0.1 | YAML handling for configs and templates |
| `github.com/fsnotify/fsnotify` | v1.9.0 | Filesystem watch events for daemon/curator loops |
| `github.com/google/uuid` | v1.6.0 | Unique IDs for sessions, messages, merge requests |
| `go.opentelemetry.io/otel` (+ sdk/metric/log, OTLP exporters) | v1.43.0 / v0.19.0 | Telemetry traces, metrics, and logs |
| `gopkg.in/natefinch/lumberjack.v2` | v2.2.1 | Rotating file logs for the daemon |
| `github.com/go-rod/rod` | v0.116.2 | Headless browser automation dependency |
| `github.com/testcontainers/testcontainers-go` (+ `modules/dolt`) | v0.42.0 | Containerized test fixtures including Dolt |
| `golang.org/x/sys` / `term` / `text` / `time` | v0.45.0 / v0.43.0 / v0.37.0 / v0.15.0 | OS, terminal, text, and time utilities |
| `github.com/muesli/termenv` | v0.16.0 | Terminal environment and color detection |
| `github.com/stretchr/testify` | v1.11.1 | Test assertions and mocks |

## 8. CLI / Usage Surface (entry points, commands block, env vars table, config files table)

Entry points: `cmd/gt/main.go:10` calls `cmd.Execute()`; `internal/cmd/root.go:25` owns the shared `rootCmd`; every `gt <verb>` is a Cobra subcommand registered via `rootCmd.AddCommand` in `init()` (e.g. `internal/cmd/sling.go:172`). Help is grouped by seven `GroupID` constants (`internal/cmd/root.go:356`); parents with subcommands use `requireSubcommand` (`internal/cmd/root.go:402`). Two support binaries exist: `gt-proxy-client` (container shim forwarding argv over mTLS, `cmd/gt-proxy-client/main.go:1`) and `gt-proxy-server` (host-side allowlisted proxy, `cmd/gt-proxy-server/main.go:1`); see [[wiki/07-cli-tui-web-config|CLI and config]].

Commands (grouped):

```
# setup / workspace
gt install [path] | gt init | gt rig add|list|remove|boot|start|shutdown|status|menu
gt up | gt down | gt doctor | gt town next|prev
# dispatch work
gt sling <bead> [target] | gt unsling | gt hook [bead] [target] | gt handoff <bead> | gt done | gt prime
# track / coordinate
gt convoy create|add|status|list|check|stranded|close|land [--interactive]
gt mail send|inbox|reply|claim|search | gt mq submit|retry|status|reject | gt config
# supervise
gt mayor start|stop|attach|status|restart|acp | gt deacon ... | gt polecat list|status|nuke|...
gt crew ... | gt daemon ... | gt status | gt dashboard [--port 8080]
```

Interactive views are Bubble Tea programs (`internal/tui/convoy/model.go:1`, `internal/tui/feed/model.go:1`) plus `gt rig menu` (`internal/cmd/rig.go:865`); the web dashboard (`internal/web/handler.go:46`, 10s cache at `:69`) is read-mostly htmx mirroring CLI state.

Env vars (selected):

| Variable | Purpose |
|---|---|
| `GT_TOWN_ROOT` / `GT_ROOT` / `GT_TOWN` | Town-root discovery fallback (`internal/workspace/find.go:90`) |
| `GT_ROLE` / `GT_RIG` / `GT_SESSION` | Agent identity + scope + session name, set by `AgentEnv` (`internal/config/env.go:94`) |
| `GT_AGENT` | Per-invocation harness override |
| `GT_DOLT_PORT` / `GT_DOLT_HOST` | Dolt endpoint (default 3307/localhost; env → config.yaml → daemon.json) |
| `GT_ACCOUNT` | Claude account config-dir selector (`internal/config/loader.go:900`) |
| `GT_COMMAND` | Rename the CLI binary/usage string (`internal/cli/name.go:19`) |
| `GT_THEME` / `GT_COST_TIER` | Color-scheme override / ephemeral model-effort tier |
| `GT_PROXY_URL` / `GT_PROXY_CERT` / `GT_PROXY_KEY` / `GT_PROXY_CA` | Proxy-client forwarding mode |

Config files:

| Path | Purpose |
|---|---|
| `mayor/town.json` | Town identity, schema v2 (`internal/config/types.go:17`) |
| `mayor/rigs.json` | Rig registry, schema v1 (`internal/config/types.go:613`) |
| `mayor/config.json` | Town behavior, schema v1 (`internal/config/types.go:28`) |
| `mayor/daemon.json` | Daemon patrol schedule, schema v1 (`internal/config/types.go:546`) |
| `settings/config.json` | Town settings: agents, timeouts, scheduler (`internal/config/types.go:42`) |
| `<rig>/settings/config.json` | Per-rig overrides: merge queue, agents, effort (`internal/config/types.go:669`) |
| `<rig>/config.json` | Per-rig identity: URLs, beads prefix (`internal/config/types.go:648`) |
| `config/messaging.json` | Mail lists, queues, announces, nudge channels |
| `mayor/accounts.json` | Claude account handles → config dirs |
| `settings/agents.json` (town or `<rig>/`) | Custom harness presets merged over built-ins |

## 9. Extensibility Points

New harness without Go changes: add a JSON preset (`name`, `command`, `args`, `process_names`, `prompt_mode`, `ready_delay_ms`, `instructions_file`) to `settings/agents.json`, set `resume_flag`/`resume_style` and `non_interactive` shapes as needed, point a rig at it via `agent`/`default_agent`/`role_agents`, then optionally add a hooks template under `internal/hooks/templates/<provider>/` plus preset `hooks_provider`/`hooks_dir` fields; built-in status requires one `builtinPresets` row plus optional `ACP` block (`internal/config/agents.go:177-194`); see [[wiki/04-harness-adapters|harness adapters]]. New repeatable workflow: author a TOML formula (type `convoy`/`workflow`/`expansion`/`aspect` at `internal/formula/types.go:16`) with `[[steps]]`/`needs`, validate with `Validate`, order with topological sort, query with `ReadySteps` (`internal/formula/parser.go:23`); specialize per rig/town with overlays (`replace`/`append`/`skip` at `internal/formula/overlay.go:8`); distribute via rig → town → embedded resolution with checksummed safe-update (`internal/formula/embed.go:47`, `:308`); ~45 formulas ship embedded (e.g. `gastown-release`, `mol-polecat-work`). New patrol behavior: create `<town>/plugins/<name>/plugin.md` (`+++` TOML frontmatter: name, description, version, gate, tracking, execution + markdown) with optional `run.sh` for script mode; gates are `cooldown`/`cron`/`condition`/`event`/`manual` (`internal/plugin/types.go:83`); discovery is town-first then rig-override (`internal/plugin/scanner.go:29`); dispatch runs through dogs during Deacon patrol with receipts via `gt plugin record-run`; 13 plugins ship (compactor-dog, dolt-backup, github-sheriff, stuck-agent-dog, etc.). New lifecycle event handling: extend the 8-event `HooksConfig` (`SessionStart`, `Stop`, `PreCompact`, `UserPromptSubmit`, `WorktreeCreate`, … at `internal/hooks/config.go:31`) with base → role → rig/role merge (`internal/hooks/config.go:506`). New merge provider: implement `PRProvider` (`FindPullRequest`/`IsPRApproved`/`MergePR` at `internal/refinery/pr_provider.go:5`) alongside the `gh`-CLI GitHub and Bitbucket-REST providers. New CLI verb: add `internal/cmd/<verb>.go` with a `cobra.Command`, flags in `init()`, one of seven `GroupID`s, `rootCmd.AddCommand`, and optional exemption lists (`internal/cmd/root.go:45`). New health check: register in the doctor registry (`internal/doctor/doctor.go:12`) reusing `internal/health` probes (TCP/SQL/zombie/backup at `internal/health/health.go:1`).

## 10. Limitations and Gotchas (at least 3 real ones)

1. Checkpoint writes are not atomic: `checkpoint.Write` uses plain `os.WriteFile` at `0600` (`internal/checkpoint/checkpoint.go:96`) instead of `atomicfile.WriteFile` (temp-plus-rename at `internal/atomicfile/atomicfile.go:56`), so a crash mid-write leaves a corrupt `.polecat-checkpoint.json` that `Read` surfaces as a parse error (`internal/checkpoint/checkpoint.go:62`) — the successor session then loses the advisory context it was counting on; per wiki [[wiki/02-worktrees-hooks-persistence|worktrees]] this is a known fragile writer.
2. No eager crash detection and no in-memory recovery: nothing watches for crashes between ticks — detection is lazy at the next `SessionStart` via `gt prime --hook` (`internal/cmd/prime_session.go:298`), checkpoints older than 24h are deleted rather than shown (`internal/cmd/prime_output.go:789`), and `ModifiedFiles`/`LastCommit`/`Notes` are hints only — predecessor reasoning and tool-call history are permanently lost, so work that was never committed or written to disk is gone.
3. Rig names are tightly constrained and harnesses are uneven: names containing `-`, `.`, space, or path separators are rejected because agent IDs use hyphens as delimiters (`internal/rig/manager.go:325`), plus reserved names like `hq` (`internal/rig/manager.go:334`); on the harness side most presets have `SupportsHooks: false` with no templates (`kiro`, `auggie`, `amp`, default `codex`), so those coders run on the weaker wrapper-plus-nudge path instead of true event hooks.
4. Single-machine tmux substrate with a central Dolt server: session names assume one town socket per host (`internal/session/registry.go:160`), `AddRig` fails fast when the Dolt server is down (`internal/rig/manager.go:342`), and stale `.boot-status.json`/PID files plus `GASTOWN_DISABLED`/`GASTOWN_ENABLED` env overrides can silently suppress supervision (`internal/boot/boot.go:29`, `internal/state/state.go:65`) — multi-host or server-down operation is outside the design.
5. Merge conflicts always bounce to humans/workers: the refinery never auto-merges — any rehearsal conflict aborts, preserves branch + MR bead, and files rework (`internal/formula/formulas/mol-refinery-patrol.formula.toml:377`), and bead attach/detach races rely on per-bead advisory locks (`internal/beads/handoff.go:233`) plus fail-open snapshot trust without a `StoreResolver` (`internal/convoy/operations.go:248`) — high-conflict monorepos will accumulate rework tasks rather than converge automatically.

## 11. How It Compares to Alternatives (3-4 REAL named alternatives: e.g. Claude Code subagents/TMUX orchestration scripts, MetaGPT/AutoGen multi-agent frameworks, Hatchet/Temporal workflow engines, git-worktree-based harnesses like Beads/fleet itself — conclude with 1-sentence positioning)

Claude Code subagents + hand-rolled tmux scripts: zero new infrastructure and full prompt control, but no persistent ledger, no capacity/backoff supervision, no merge queue, and every isolation/locking/recovery rule must be reinvented per project — GasTown is that script collection hardened into a daemon with a beads database. MetaGPT / AutoGen (multi-agent conversation frameworks): richer in-process role dialogue and tool-use loops, but agents share one filesystem checkout and coordinate through message passing rather than worktree isolation plus git-branch merging — GasTown inverts the priority, treating the branch merge as the coordination primitive and mail as notification. Hatchet / Temporal (durable workflow engines): stronger exactly-once step execution, retries, and visibility for deterministic pipelines, but they orchestrate functions, not autonomous coder CLIs in tmux panes — GasTown's formula system is deliberately agent-interpreted TOML with `ReadySteps` queries rather than a central step runner. Beads / fleet (git-worktree + beads-ledger harnesses): closest cousins — same worktree-per-worker plus issue-ledger shape — but fleet's Python orchestrator lacks GasTown's Dolt-backed multi-DB routing, convoy `tracks`-edge feeder with mountain auto-skip, refinery rehearsal-abort merge policy, and data-driven 13-harness registry. Positioning in one sentence: GasTown is the option to pick when the bottleneck is parallel coder isolation with auditable merges across many harnesses, not single-agent quality or deterministic step retries.

## Appendix: Selected Code Snippets (2-4 verbatim snippets referenced from wiki pages, each with file:line)

1. Pool-lock discipline at spawn (`internal/polecat/manager.go:662`, via [[wiki/02-worktrees-hooks-persistence|worktrees]]):

```go
// Hold pool lock across allocation + directory creation to close the
// race window where a concurrent AllocateName could miss the pending
// marker and reallocate the same name.
poolLock, err := m.lockPool()
```

2. Checkpoint struct (`internal/checkpoint/checkpoint.go:23`, via [[wiki/02-worktrees-hooks-persistence|worktrees]]):

```go
type Checkpoint struct {
	MoleculeID    string    `json:"molecule_id,omitempty"`
	CurrentStep   string    `json:"current_step,omitempty"`
	StepTitle     string    `json:"step_title,omitempty"`
	ModifiedFiles []string  `json:"modified_files,omitempty"`
	LastCommit    string    `json:"last_commit,omitempty"`
	Branch        string    `json:"branch,omitempty"`
	HookedBead    string    `json:"hooked_bead,omitempty"`
	Timestamp     time.Time `json:"timestamp"`
	SessionID     string    `json:"session_id,omitempty"`
	Notes         string    `json:"notes,omitempty"`
}
```

3. ACP provider contract (`internal/agent/provider/provider.go:31-40`, via [[wiki/04-harness-adapters|harness adapters]]):

```go
type ACPProvider interface {
	Initialize(ctx context.Context, clientName, clientVersion string) (*InitializeResult, error)
	ListTools(ctx context.Context) ([]Tool, error)
	CallTool(ctx context.Context, name string, args map[string]any) (*CallToolResult, error)
	CreateMessage(ctx context.Context, params CreateMessageParams) (*CreateMessageResult, error)
	GetStatus() AgentStatus
	OnToolCall(callback ToolCallback)
	OnSessionStart(callback SessionStartCallback)
	Close() error
}
```

4. Agent lockfile path (`internal/lock/lock.go:54`, via [[wiki/08-safety-workflow-plugins|safety]]):

```go
lockPath: filepath.Join(workerDir, ".runtime", "agent.lock"),
```
