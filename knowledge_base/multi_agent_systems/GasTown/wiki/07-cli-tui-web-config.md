> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# User Surface: CLI, TUI, Web UI, and Configuration

**In one sentence:** GasTown is driven by a single `gt` Cobra CLI (command registry in `internal/cmd`, theme/env handling in `internal/cli`, `internal/ui`, `internal/style`), with Bubble Tea TUIs for convoy/feed views and an htmx web dashboard, all configured through versioned JSON files under `mayor/`, `settings/`, and per-rig directories.

## Key points
- The only user entry point is `cmd/gt/main.go:10`, which calls `cmd.Execute()`; `internal/cmd/root.go:25` owns the shared `rootCmd`, and every `gt <verb>` is a Cobra subcommand registered via `rootCmd.AddCommand` in an `init()` function (e.g. `internal/cmd/sling.go:172`).
- Help output is grouped by seven command groups declared in `internal/cmd/root.go:356`, wired into help order in `internal/cmd/root.go:371`; parent commands with subcommands reject bare/unknown invocations through `requireSubcommand` (`internal/cmd/root.go:402`).
- The binary name defaults to `gt` but is overridable with the `GT_COMMAND` environment variable (Environment Variable, a named setting a user can change to control program behavior) resolved in `internal/cli/name.go:17`.
- Work dispatch centers on `gt sling` (`internal/cmd/sling.go:25`), which resolves a rig target, spawns or reuses a polecat via `SpawnPolecatForSling` (`internal/cmd/polecat_spawn.go:102`), and tracks batches with convoys (`internal/cmd/convoy.go:176`).
- Supervision is split across role commands (`mayor`, `deacon`, `polecat`, `crew`, `witness`, `refinery`) that mostly manage tmux sessions (terminal multiplexer sessions, persistent background shells) per role, e.g. `internal/cmd/mayor.go:22` and `internal/cmd/polecat.go:31`.
- Interactive views are Bubble Tea (a Go framework for building terminal user interfaces) programs under `internal/tui/convoy/model.go:1` and `internal/tui/feed/model.go:1`, reached via flags such as `gt convoy --interactive` (`internal/cmd/convoy.go:407`) and `gt rig menu` (`internal/cmd/rig.go:865`).
- The web dashboard (`internal/web/handler.go:46`) is a read-mostly htmx view served by `gt dashboard` on port 8080 by default (`internal/cmd/dashboard.go:48`), with a JSON API under `/api/` (`internal/cmd/dashboard.go:151`).
- All durable settings are versioned JSON configs with explicit schema constants (e.g. town v2 in `internal/config/types.go:637`, daemon-patrol v1 in `internal/config/types.go:568`), loaded/saved by helpers in `internal/config/loader.go:527` and resolved per-agent through `AgentEnv` (`internal/config/env.go:94`).

---
## Entry points and binaries

`cmd/gt/main.go:10` is the whole `gt` binary: it calls `cmd.Execute()`, which initializes telemetry then runs `rootCmd` (`internal/cmd/root.go:320`). The root command's name and help text are set from `cli.Name()` in `internal/cmd/root.go:35`, so `GT_COMMAND` renames the CLI (`internal/cli/name.go:19`).

Two additional binaries support sandboxed execution:

| Binary | File | What it does |
|---|---|---|
| `gt-proxy-client` | `cmd/gt-proxy-client/main.go:1` | Pass-through shim installed as `gt`/`bd` inside containers; forwards argv to the proxy over mTLS (Mutual Transport Layer Security, both sides prove identity with certificates) when proxy env vars are set, otherwise execs the real binary (`cmd/gt-proxy-client/main.go:47`). |
| `gt-proxy-server` | `cmd/gt-proxy-server/main.go:1` | Host-side mTLS proxy that runs allowed `gt`/`bd` subcommands for sandboxes; default allowlist in `cmd/gt-proxy-server/main.go:24`, config defaults to `~/gt/.runtime/proxy/config.json` (`cmd/gt-proxy-server/main.go:50`). |

## Command registration: how a new `gt <verb>` is added

1. Create `internal/cmd/<verb>.go` with `var <verb>Cmd = &cobra.Command{Use: ..., GroupID: ..., Short: ..., Long: ..., RunE: ...}` following `internal/cmd/sling.go:25`.
2. Declare flags on that variable in `init()` (e.g. `internal/cmd/sling.go:142`), add any subcommands with `<verb>Cmd.AddCommand(...)` (e.g. `internal/cmd/convoy.go:426`), then attach to the root with `rootCmd.AddCommand(<verb>Cmd)` (e.g. `internal/cmd/sling.go:172`, `internal/cmd/convoy.go:437`, `internal/cmd/mayor.go:136`, `internal/cmd/polecat.go:381`).
3. Pick one of the seven `GroupID` constants (`GroupWork`, `GroupAgents`, `GroupComm`, `GroupServices`, `GroupWorkspace`, `GroupConfig`, `GroupDiag`) defined in `internal/cmd/root.go:356` so help stays organized.
4. If the command is a parent with subcommands, set `RunE: requireSubcommand` like `internal/cmd/mayor.go:23` so typos fail loudly instead of printing help with exit 0 (`internal/cmd/root.go:402`).
5. If the command must work without the `bd` issue tracker or off-main-branch warnings, add its name to `beadsExemptCommands` or `branchCheckExemptCommands` in `internal/cmd/root.go:45`; the check walks parent commands (`internal/cmd/root.go:171`) and every command runs `persistentPreRun` (`internal/cmd/root.go:99`) for telemetry, theme init (`internal/cmd/root.go:202`), and heartbeat touch (`internal/cmd/root.go:225`).

## Command table (grouped by workflow)

Setup and workspace:

| Command | File | What it does |
|---|---|---|
| `gt install [path]` | `internal/cmd/install.go:52` | Create a new GasTown HQ workspace (town root). |
| `gt init` | `internal/cmd/init.go:22` | Initialize current directory as a rig (Initialize, register a code repository as a managed work area). |
| `gt rig ...` | `internal/cmd/rig.go:38` | Manage rigs: `add` (`internal/cmd/rig.go:54`), `list` (`internal/cmd/rig.go:93`), `remove` (`internal/cmd/rig.go:110`), `boot`/`start`/`shutdown` (`internal/cmd/rig.go:148`, `internal/cmd/rig.go:166`, `internal/cmd/rig.go:202`), `status` (`internal/cmd/rig.go:228`), `menu` (`internal/cmd/rig.go:865`). |
| `gt up` / `gt down` | `internal/cmd/up.go:122` | Bring up / tear down all town services (daemon plus Dolt SQL server). |
| `gt doctor` | `internal/cmd/doctor.go:24` | Run health checks on the workspace. |
| `gt town next/prev` | `internal/cmd/town_cycle.go:41` | Switch between town-level tmux sessions (mayor/deacon). |

Spawn and dispatch work:

| Command | File | What it does |
|---|---|---|
| `gt sling <bead> [target]` | `internal/cmd/sling.go:25` | Unified dispatch: attach work to an agent hook and start it now; auto-spawns a polecat for rig targets (`internal/cmd/polecat_spawn.go:102`), auto-creates a convoy unless `--no-convoy`, validates rig names via `IsRigName` (`internal/cmd/polecat_spawn.go:488`). |
| `gt unsling` | `internal/cmd/unsling.go:20` | Remove work from an agent's hook. |
| `gt hook [bead] [target]` | `internal/cmd/hook.go:24` | Show or attach work on a hook without starting it (vs `sling` = attach+start, `handoff` = attach+restart). |
| `gt handoff <bead>` | `internal/cmd/handoff.go:32` | Hand off to a fresh session; work continues from the hook. |
| `gt done` | `internal/cmd/done.go:32` | Signal work ready for the merge queue (push branch, submit MR (Merge Request, a proposal to merge a branch)). |
| `gt prime` | `internal/cmd/prime.go:68` | Output role context for the current directory (what the agent should work on). |

Track and coordinate:

| Command | File | What it does |
|---|---|---|
| `gt convoy ...` | `internal/cmd/convoy.go:176` | Track batches of work: `create`/`add`/`status`/`list`/`check`/`stranded`/`close`/`land`, all registered in `internal/cmd/convoy.go:386`. |
| `gt mail ...` | `internal/cmd/mail.go:57` | Agent messaging: `send`/`inbox`/`reply`/`claim`/`search` and queue/channel helpers. |
| `gt mq ...` | `internal/cmd/mq.go:65` | Merge queue operations: submit, retry, status, reject (`internal/cmd/mq.go:66`). |
| `gt config ...` | `internal/cmd/config.go:22` | View/modify town and agent configuration (agents, default agent, cost tier). |

Supervise agents and services:

| Command | File | What it does |
|---|---|---|
| `gt mayor start/stop/attach/status/restart/acp` | `internal/cmd/mayor.go:22` | Manage the Mayor tmux session; `acp` runs headless for IDE integration. |
| `gt deacon ...` | `internal/cmd/deacon.go:36` | Manage the town watchdog: start/stop/attach/status, health ping, force-kill, feed stranded convoys. |
| `gt polecat list/status/nuke/...` | `internal/cmd/polecat.go:31` | Polecat lifecycle: list (`internal/cmd/polecat.go:62`), remove, status, git-state, check-recovery, gc, nuke, stale, prune, pool-init (flags wired in `internal/cmd/polecat.go:327`). |
| `gt crew ...` | `internal/cmd/crew.go:31` | Manage crew workers inside a rig. |
| `gt daemon ...` | `internal/cmd/daemon.go:23` | Manage the background patrol daemon. |
| `gt status` | `internal/cmd/status.go:43` | Show overall town status. |
| `gt dashboard` | `internal/cmd/dashboard.go:29` | Start the web dashboard (default port 8080, `/api/` JSON endpoints). |

## TUI vs CLI vs web UI roles

- CLI (`internal/cmd`, Cobra): the primary and complete interface; every automation path (hooks, daemon patrols, proxy allowlist in `cmd/gt-proxy-server/main.go:24`) shells out to `gt` subcommands. Rendering uses `internal/style` and `internal/ui`, with theme selection (`dark`/`light`/`auto`) applied on every invocation (`internal/cmd/root.go:202`).
- TUI (Terminal User Interface, interactive full-screen terminal app via Bubble Tea): used for live operational views only. `internal/tui/convoy/model.go:1` renders the convoy tree (entered with `gt convoy --interactive`, flag in `internal/cmd/convoy.go:407`); `internal/tui/feed/model.go:1` renders the activity feed with multi-source event aggregation; `gt rig menu` (`internal/cmd/rig.go:865`) gives an interactive tmux session picker.
- Web (`internal/web/handler.go:46`): the convoy dashboard is a read-mostly htmx page with a 10s response cache (`internal/web/handler.go:69`) served by `ServeHTTP` (`internal/web/handler.go:93`); `gt dashboard` prints the URL and API prefix (`internal/cmd/dashboard.go:151`). It shells out to `bd`/`gt` subprocesses for data, so it mirrors CLI state rather than owning any.
- Scaffolding text for agents and town layout lives in `internal/templates` (role instruction files, town-root skeleton via `internal/templates/townroot.go`) and the top-level `templates/` directory (fry commands, launchd/systemd units, message templates).

## Configuration files

| Path (relative to town root unless noted) | Purpose |
|---|---|
| `mayor/town.json` | Town identity (`internal/config/types.go:17`); path helper `internal/constants/constants.go:374`; schema v2 (`internal/config/types.go:637`). |
| `mayor/rigs.json` | Rig registry (`internal/config/types.go:613`); path helper `internal/constants/constants.go:369`; schema v1 (`internal/config/types.go:640`). |
| `mayor/config.json` | Town behavioral config (`internal/config/types.go:28`); path helper `internal/constants/constants.go:399`; schema v1 (`internal/config/types.go:608`). |
| `mayor/daemon.json` | Daemon patrol schedule (`internal/config/types.go:546`, defaults in `internal/config/types.go:574`); path helper `internal/config/loader.go:527`; schema v1 (`internal/config/types.go:568`). |
| `settings/config.json` | Town settings: default agent, role agents, timeouts, scheduler (`internal/config/types.go:42`); path helper `internal/config/loader.go:1063`; schema v1 (`internal/config/types.go:38`). |
| `<rig>/settings/config.json` | Per-rig overrides: merge queue, theme, agents, role effort (`internal/config/types.go:669`); path helper `internal/config/loader.go:1068`; schema v1 (`internal/config/types.go:646`). |
| `<rig>/config.json` | Per-rig identity: name, git URLs, beads prefix (`internal/config/types.go:648`); schema v1 (`internal/config/types.go:643`). |
| `config/messaging.json` | Mail lists, queues, announces, nudge channels; path helper `internal/config/loader.go:1047`. |
| `mayor/accounts.json` | Claude account handles to config dirs; path helper `internal/constants/constants.go:418`; `GT_ACCOUNT` resolution in `internal/config/loader.go:900`. |
| `<repo>/.gastown/settings.json` | Repo-committed rig defaults that survive re-scaffolding; constant `internal/config/loader.go:302`. |
| `~/.runtime/proxy/config.json` (default `~/gt/.runtime/...`) | Proxy server listen addresses, CA dir, allowlists (`cmd/gt-proxy-server/main.go:50`). |

Key settings knobs inside town/rig settings: `default_agent`, `agents{}`, `role_agents{}` (mayor/deacon/witness/refinery/polecat/crew/dog), `role_effort{}`, `scheduler{}` (capacity-gated dispatch), `operational{}` (timeouts now config instead of constants), `disabled_patrols[]`, merge-queue commands, and `cli_theme` (`internal/config/types.go:42`).

## Environment variables

| Variable | Default | Purpose |
|---|---|---|
| `GT_COMMAND` | `gt` | Renames the CLI binary/usage string (`internal/cli/name.go:19`). |
| `GT_ROOT` / `GT_TOWN_ROOT` / `GT_TOWN` | cwd-detected | Town root discovery; `GT_TOWN_ROOT` is read for ACP startup (`internal/cmd/mayor.go:469`); every command touches registry/heartbeat from the detected root (`internal/cmd/root.go:225`). |
| `GT_ROLE` | — | Agent identity in compound form (`rig/polecats/name`, `mayor`, `dog`); set by `AgentEnv` (`internal/config/env.go:94`); never inherited across boundaries (`internal/config/env.go:21`). |
| `GT_RIG` | — | Rig scope override, e.g. ACP `--rig` vs env (`internal/cmd/mayor.go:481`). |
| `GT_SESSION` | — | tmux session name for heartbeat/cost correlation (`internal/cmd/root.go:225`). |
| `GT_POLECAT` / `GT_CREW` / `GT_DOG_NAME` | — | Legacy/specific identity vars; `GT_POLECAT` blocks `sling` for workers (`internal/cmd/sling.go:225`); all are scrubbed on boundary crossing (`internal/config/env.go:21`). |
| `GT_ACCOUNT` | default account | Selects a Claude account config dir (`internal/config/loader.go:900`). |
| `GT_AGENT` | — | Per-invocation agent/runtime override (e.g. `--agent codex`). |
| `GT_DOLT_PORT` / `GT_DOLT_HOST` | 3307 / localhost | Central Dolt SQL endpoint; resolution order env → `config.yaml` → `daemon.json` (`internal/config/env.go:444`, `internal/config/env.go:636`); re-injected into every agent env (`internal/config/env.go:94`). |
| `GT_DOLT_IGNORE_CONFIG` | — | Ignore managed `config.yaml` when resolving the Dolt endpoint (`internal/config/env.go:583`). |
| `GT_COST_TIER` | — | Ephemeral cost-tier override for per-role model/effort selection (`internal/config/loader.go:1438`). |
| `GT_THEME` | `auto` | CLI color scheme override for `cli_theme` (`internal/config/types.go:46`). |
| `GT_PROXY_URL` / `GT_PROXY_CERT` / `GT_PROXY_KEY` / `GT_PROXY_CA` | — | Enable proxy-client forwarding mode (`cmd/gt-proxy-client/main.go:39`); `GT_REAL_BIN` sets the fallback binary (`cmd/gt-proxy-client/main.go:129`). |
| `GT_STALE_WARNED` | — | Suppress repeat stale-binary warnings per shell (`internal/cmd/root.go:282`). |
| `BD_DOLT_AUTO_COMMIT` | `off` in sling/polecats | Disabled during dispatch to avoid manifest contention (`internal/cmd/sling.go:262`); `BEADS_DIR` is stripped for town-level `bd` calls (`internal/cmd/convoy.go:451`). |

## TUI programs in detail

- The convoy TUI (`internal/tui/convoy/model.go:1`) is a Bubble Tea model over `IssueItem` rows (id/title/status); it shells out to `bd` for convoy data and validates IDs against the `hq-*` pattern in the same file. Key bindings live in `internal/tui/convoy/keys.go` and rendering in `internal/tui/convoy/view.go`.
- The feed TUI (`internal/tui/feed/model.go:1`) is a multi-panel event viewer (panels, viewport, help bindings) fed by `bd`/tmux subprocess sources; per-source logic is split into `internal/tui/feed/convoy.go`, `internal/tui/feed/mq_source.go`, `internal/tui/feed/multi_source.go`, with stuck-work detection in `internal/tui/feed/stuck.go` and key bindings in `internal/tui/feed/keys.go`.
- Both TUIs are read/write-light overlays: they display state and shell out to the same `gt`/`bd` commands the CLI uses, so nothing in the TUI owns durable state.
- `gt rig menu` (`internal/cmd/rig.go:865`) is a third interactive surface: a tmux session picker rather than a Bubble Tea program.

## Web dashboard and API in detail

- `gt dashboard` starts an HTTP server on `--port 8080` (`internal/cmd/dashboard.go:48`) with `--bind` defaulting to localhost (usage in `internal/cmd/dashboard.go:40`); the listen address is built in `internal/cmd/dashboard.go:100` and the startup line advertises the `/api/` prefix (`internal/cmd/dashboard.go:151`).
- Data comes through the `ConvoyFetcher` interface — convoys, merge queue, workers, mail, rigs, dogs, escalations, health, queues, sessions, hooks, mayor, issues, activity (`internal/web/handler.go:23`) — implemented with subprocess calls that have configurable timeouts (`WebTimeoutsConfig` in `internal/config/types.go:141`).
- Overload protection is built in: a 10s response cache (`internal/web/handler.go:69`) with a fast-path cache serve (`internal/web/handler.go:99`) plus a per-panel expanded-view cache, serializing concurrent fetches so multiple tabs or htmx auto-refresh cannot start a `bd` process storm.
- Static assets are embedded from `internal/web/static` (`internal/web/handler.go:19`) and HTML templates from `internal/web/templates` (loaded via `internal/web/templates.go`).

## Config resolution, versions, and agent startup

- Every agent process starts with environment built by `AgentEnv` (`internal/config/env.go:94`): role/rig/name determine `GT_ROLE`, `GT_RIG`, `BD_ACTOR`, `GIT_AUTHOR_NAME`, plus `GT_ROOT`, `GT_SESSION`, `GT_AGENT`, Dolt endpoint injection, and `BD_BACKUP_ENABLED=false`.
- Model selection resolves per role through town `settings/config.json` → rig `settings/config.json` → built-in presets, with per-worker overrides (`WorkerAgents`, town `CrewAgents`) and an ephemeral `GT_COST_TIER` tier (`internal/config/loader.go:1438`); effort level resolves the same way and lands in `CLAUDE_CODE_EFFORT_LEVEL` (`internal/config/env.go:228`).
- Schema versions are enforced as "max supported" checks in the loader, so newer files fail loudly: town v2 (`internal/config/types.go:637`), rigs v1 (`internal/config/types.go:640`), rig v1 (`internal/config/types.go:643`), rig-settings v1 (`internal/config/types.go:646`), mayor-config v1 (`internal/config/types.go:608`), town-settings v1 (`internal/config/types.go:38`), daemon-patrol v1 (`internal/config/types.go:568`).
- The daemon reads `mayor/daemon.json` env (e.g. `GT_DOLT_PORT`) into its own process before starting dependencies (`internal/cmd/mayor.go:410`), and rig add/remove keeps witness/refinery patrol rig lists in sync (`internal/config/loader.go:597`, `internal/config/loader.go:695`).
- CLI theme comes from town `cli_theme` with `GT_THEME` override, applied via `ui.InitTheme`/`ApplyThemeMode` on every invocation (`internal/cmd/root.go:202`); `BEADS_DIR`-style selector vars are cleared from agent env to prevent stale DB routing (`internal/config/env.go:26).

- `gt proxy-subcmds` (`internal/cmd/proxy_subcmds.go`) prints the machine-readable subcommand allowlist the proxy server auto-discovers at startup (`cmd/gt-proxy-server/main.go:158`).
**Covers:** `cmd/gt/main.go`, `cmd/gt-proxy-client/main.go`, `cmd/gt-proxy-server/main.go`, `internal/cmd` (root, sling, convoy, polecat, polecat_spawn, mayor, deacon, rig, town_cycle, init, install, status, hook, handoff, done, unsling, prime, mail, mq, daemon, up, doctor, dashboard, config, crew), `internal/cli/name.go`, `internal/tui/convoy/model.go`, `internal/tui/feed/model.go`, `internal/ui`, `internal/style`, `internal/web/handler.go`, `internal/templates`, `templates/`, `internal/config/types.go`, `internal/config/loader.go`, `internal/config/env.go`, `internal/constants/constants.go`
