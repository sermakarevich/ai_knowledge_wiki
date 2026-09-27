> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Tracker Backends, Workflows, CLI Surface, Config, and Metrics

**In one sentence:** Overstory abstracts issue tracking behind a `TrackerClient` interface with `beads` (`bd` command-line interface) and `seeds` (`sd`) backends selected by filesystem probing, drives agent work through `ov sling`/`ov spec write`/`ov prime`/`ov init` commands configured by `.overstory/config.yaml`, and accounts token spend via a SQLite (Structured Query Language database) metrics store fed by transcript parsing plus per-model pricing.

## Key points

- The tracker abstraction is a 7-method `TrackerClient` interface (`ready`, `show`, `create`, `claim`, `close`, `list`, `sync`) over a unified `TrackerIssue` shape, with `createTrackerClient()` switching on `"beads" | "seeds"` and `resolveBackend()` probing `.seeds/` before `.beads/`, defaulting to `seeds` (`src/tracker/types.ts:25`, `src/tracker/factory.ts:18`, `src/tracker/factory.ts:35`).
- Beads and seeds differ in wire protocol, not surface: beads returns raw JSON (JavaScript Object Notation) arrays and maps `issue_type` to `type`, while seeds wraps every response in a `{ success, command, ... }` envelope that must be validated; both `claim` via `update <id> --status in_progress` and both `sync` via their CLI (`src/beads/client.ts:107`, `src/tracker/seeds.ts:50`, `src/tracker/seeds.ts:152`).
- Beads-only molecules (`bd mol create|step add|pour|list|status`) are multi-step workflow prototypes whose "pour" instantiates pre-wired issue chains; seeds has no molecule equivalent in this codebase (`src/beads/molecules.ts:98`, `src/beads/molecules.ts:138`).
- There are no `/orchestrate` or `/plan-worktrees` slash commands in `.claude/commands/` (only `issue-reviews`, `pr-reviews`, `prioritize`, `release`, `triage`); the equivalent workflow is coordinator-dispatches-leads via `ov sling`, lead-owned specs via `ov spec write`, and the Scout → Build → Verify playbook in `agents/lead.md` and `agents/coordinator.md`.
- `ov sling` is a 14-step spawn pipeline (config → depth/hierarchy checks → manifest → run-id → concurrency/name/task locks → worktree → overlay → dispatch mail → claim → identity → tmux (terminal multiplexer) or headless spawn → session record) with hard guards: depth > `maxDepth` rejected, coordinator may only spawn lead/scout/builder directly, one agent per task (`src/commands/sling.ts:1`, `src/commands/sling.ts:568`, `src/commands/sling.ts:386`, `src/commands/sling.ts:675`).
- Configuration merges `DEFAULT_CONFIG` ← `config.yaml` ← `config.local.yaml`, resolves the project root through git worktree detection (`git rev-parse --git-common-dir`), and validates `taskTracker.backend` against `auto|seeds|beads`; shipped defaults are 25 max concurrent agents, 2000 ms stagger, depth 2, 5 agents per lead, `backend: auto` (`src/config.ts:914`, `src/config.ts:857`, `src/config.ts:602`, `.overstory/config.yaml:28`).
- Metrics are two SQLite tables (`sessions` keyed by `(agent_name, task_id)`, `token_snapshots` append-only with per-agent latest view) in WAL (write-ahead logging) mode; costs come from substring-matched per-million-token pricing (e.g. sonnet $3 in / $15 out, opus $15 / $75, haiku $0.80 / $4) applied to Claude Code transcript JSONL (JSON Lines) usage aggregates, surfaced by `ov costs` (`--live`, `--self`, `--agent`, `--run`, `--bead`, `--by-capability`, `--last`) and `ov metrics` (`src/metrics/store.ts:68`, `src/metrics/pricing.ts:30`, `src/metrics/transcript.ts:74`, `src/commands/costs.ts:565`).

---

## 1. Tracker abstraction: types and factory

The unified shape is defined in `src/tracker/types.ts:9`:

```typescript
export interface TrackerIssue {
	id: string;
	title: string;
	status: string;
	priority: number;
	type: string;
	assignee?: string;
	description?: string;
	blocks?: string[];
	blockedBy?: string[];
}
```

The client contract in `src/tracker/types.ts:25` declares seven methods: `ready()` for open unblocked work (`src/tracker/types.ts:27`), `show(id)` (`src/tracker/types.ts:30`), `create(title, options)` returning the new ID (`src/tracker/types.ts:33`), `claim(id)` marking `in_progress` (`src/tracker/types.ts:39`), `close(id, reason?)` (`src/tracker/types.ts:42`), `list(options)` with status/limit filters (`src/tracker/types.ts:45`), and `sync()` for git synchronization (`src/tracker/types.ts:48`). The backend discriminator is `TrackerBackend = "beads" | "seeds"` (`src/tracker/types.ts:52`).

The factory in `src/tracker/factory.ts:18` switches exhaustively (`src/tracker/factory.ts:19`, `src/tracker/factory.ts:20`, `src/tracker/factory.ts:22`, `src/tracker/factory.ts:25`): unknown strings fail at compile time via the `never` guard. Backend resolution in `src/tracker/factory.ts:35` passes explicit `beads`/`seeds` through (`src/tracker/factory.ts:39`, `src/tracker/factory.ts:40`) and for `auto` probes `.seeds/` first, then `.beads/`, with seeds as the preferred default (`src/tracker/factory.ts:50`, `src/tracker/factory.ts:51`, `src/tracker/factory.ts:53`). `trackerCliName()` maps seeds to `sd` and beads to `bd` (`src/tracker/factory.ts:59`); sling injects this name into overlays as `trackerCli`/`trackerName` (`src/commands/sling.ts:813`).

## 2. Beads backend vs seeds backend

Both backends shell out via `Bun.spawn` with zero runtime dependencies (`src/beads/client.ts:53`, `src/tracker/seeds.ts:19`). The beads adapter in `src/tracker/beads.ts:16` is a thin wrapper over `createBeadsClient()` (`src/beads/client.ts:127`), casting `BeadIssue` to `TrackerIssue` (`src/tracker/beads.ts:20`).

Beads wire details (`src/beads/client.ts:1`): issues are `BeadIssue` (`src/beads/client.ts:15`); `ready()` accepts an optional molecule filter `--mol` (`src/beads/client.ts:29`, `src/beads/client.ts:140`); `show` parses a single-element array (`src/beads/client.ts:150`, comment at `src/beads/client.ts:152`, empty-array guard `src/beads/client.ts:154`); `create` is positional-title form `bd create <title> --json` (`src/beads/client.ts:161`); `claim` runs `bd update <id> --status in_progress` (`src/beads/client.ts:177`); `close` appends `--reason` (`src/beads/client.ts:181`); `list` supports `--status/--limit` (`src/beads/client.ts:189`). The key normalization is `issue_type` → `type` (`src/beads/client.ts:90`, implemented `src/beads/client.ts:107`):

```typescript
type: raw.issue_type ?? raw.type ?? "unknown",
```

Beads `sync()` shells `bd sync` and throws `AgentError` on nonzero exit (`src/tracker/beads.ts:47`).

Seeds wire details (`src/tracker/seeds.ts:1`): every call goes through `runSd()` (`src/tracker/seeds.ts:14`), which raises `AgentError` on nonzero exit (`src/tracker/seeds.ts:23`). Output parsing in `src/tracker/seeds.ts:32` strips non-JSON (non-JavaScript-Object-Notation) prefix lines by seeking the first `{` or `[` (`src/tracker/seeds.ts:38`). Envelopes are typed as list, show, and create variants sharing `{ success, command, error? }` (`src/tracker/seeds.ts:50`, `src/tracker/seeds.ts:57`, `src/tracker/seeds.ts:62`, `src/tracker/seeds.ts:67`) and validated by `assertEnvelopeSuccess()` (`src/tracker/seeds.ts:76`). Seeds uses `type` directly with no mapping (`src/tracker/seeds.ts:83`, normalized `src/tracker/seeds.ts:96`). Command shapes: `sd ready --json` (`src/tracker/seeds.ts:117`), `sd show <id> --json` (`src/tracker/seeds.ts:124`), `sd create --title <t> --json` with optional `--type/--priority/--description` and ID read from `envelope.id ?? envelope.issue?.id` (`src/tracker/seeds.ts:131`, `src/tracker/seeds.ts:145`); `claim` is `sd update <id> --status in_progress` (`src/tracker/seeds.ts:152`); `close` appends `--reason` (`src/tracker/seeds.ts:156`); `list` supports `--status/--limit` (`src/tracker/seeds.ts:164`); `sync` is `sd sync` (`src/tracker/seeds.ts:178`).

Storage note: neither adapter owns storage; beads persists via the external `bd` tool and seeds via `sd` plus its git-native files (the clone's `.seeds/config.yaml` is just `project: "overstory", version: "1"` at `.seeds/config.yaml:1`). The tracker layer only normalizes CLI (command-line interface) output into `TrackerIssue`.

## 3. Beads molecules

Molecules are beads-only multi-step workflow prototypes: templates with ordered steps that, when "poured", create real issues with dependencies pre-wired (module docstring `src/beads/molecules.ts:1`). Types are `MoleculeStep { title, type? }` (`src/beads/molecules.ts:15`), `MoleculePrototype { id, name, stepCount }` (`src/beads/molecules.ts:20`), and `ConvoyStatus { total, completed, inProgress, blocked }` (`src/beads/molecules.ts:26`).

Creation in `src/beads/molecules.ts:98` runs `bd mol create --name <n> --json` (`src/beads/molecules.ts:102`) then one `bd mol step add <id> --title <t> --type <ty> --json` per step, defaulting type to `task` (`src/beads/molecules.ts:111`). Pouring in `src/beads/molecules.ts:138` runs `bd mol pour <id> --json` with optional `--prefix` (`src/beads/molecules.ts:142`) and returns `{ ids }` (`src/beads/molecules.ts:147`). Listing (`src/beads/molecules.ts:157`) and convoy status (`src/beads/molecules.ts:180`, returning the four counters at `src/beads/molecules.ts:192`) complete the API (application programming interface). All helpers share the `runBd` + `parseJsonOutput` pattern (`src/beads/molecules.ts:56`, `src/beads/molecules.ts:72`). No seeds-side molecule code exists in the files read.

## 4. Task-spec workflow and the orchestrate / plan-worktrees equivalents

There is no `/orchestrate` or `/plan-worktrees` command in this repo: `.claude/commands/` contains exactly `issue-reviews.md`, `pr-reviews.md`, `prioritize.md`, `release.md`, `triage.md`. The functional equivalents are:

- Dispatch equivalent: `ov sling <task-id>` plus the coordinator/lead playbooks. The coordinator dispatches leads only and never writes specs or code (failure modes `HIERARCHY_BYPASS`, `SPEC_WRITING`, `CODE_MODIFICATION` in `agents/coordinator.md:19`, `agents/coordinator.md:20`, `agents/coordinator.md:21`; hierarchy enforced by `HierarchyError` per `agents/coordinator.md:49` and `src/commands/sling.ts:386`). The required merge sequence is lead `merge_ready` mail → coordinator merges branch → merge succeeds → close issue (`agents/coordinator.md:25`).
- Plan equivalent: lead-owned three-phase Scout → Build → Verify pipeline (`agents/lead.md:79`), with propulsion rule "simple tasks implement immediately, moderate tasks spec-then-builder, complex tasks scouts first" (`agents/lead.md:3`), dispatch overrides `SKIP REVIEW` / `MAX AGENTS` (`agents/lead.md:5`), and named failures including `SPEC_WITHOUT_SCOUT`, `OVERLAPPING_FILE_SCOPE`, `WORKTREE_ISSUE_CREATE` (`agents/lead.md:29`).

The spec artifact mechanism is `ov spec write <task-id> --body <content>` (registered `src/index.ts:294`). `writeSpec()` in `src/commands/spec.ts:40` creates `.overstory/specs/` (`src/commands/spec.ts:46`), prepends an optional `<!-- written-by: agent -->` header (`src/commands/spec.ts:51`), enforces a trailing newline (`src/commands/spec.ts:57`), and writes `.overstory/specs/<task-id>.md` (`src/commands/spec.ts:61`). The entry point `specWriteCommand()` (`src/commands/spec.ts:73`) accepts `--body` or piped stdin (`src/commands/spec.ts:27`, consumed `src/commands/spec.ts:83`), rejects empty task ID (`src/commands/spec.ts:74`) and empty body (`src/commands/spec.ts:90`), resolves the root via `resolveProjectRoot()` (`src/commands/spec.ts:96`), and supports `--json` and `--agent` attribution (`src/commands/spec.ts:17`). Sling consumes specs by path: `--spec` is validated for existence and resolved absolute so worktree agents can read it (`src/commands/sling.ts:540`), then injected into the overlay as `specPath` (`src/commands/sling.ts:793`).

## 5. sling command: 14-step spawn

The header comment in `src/commands/sling.ts:1` lists the 14 steps (load config/manifest, validate, run-id, uniqueness/concurrency, task check, worktree, overlay, hooks, claim, identity, tmux session, session record, return). Options are `SlingOptions` (`src/commands/sling.ts:139`): capability, name, spec, files, parent, depth, skipScout, skipTaskCheck, forceHierarchy, json, maxAgents, skipReview, dispatchMaxAgents, runtime, noScoutCheck, baseBranch. CLI (command-line interface) flags including defaults (`--capability builder`, `--depth 0`) are wired in `src/index.ts:266`.

Mechanism sequence with guards:

1. Config + backend: `loadConfig(cwd)` then `resolveBackend(config.taskTracker.backend, ...)` (`src/commands/sling.ts:561`).
2. Depth: reject `depth > maxDepth` (`src/commands/sling.ts:568`); default `maxDepth` is 2, i.e. orchestrator(0) → lead(1) → specialist(2) (`src/commands/sling.ts:566`, default `src/config.ts:59`).
3. Hierarchy: coordinator (no `--parent`) may spawn only `lead`, `scout`, `builder` (`src/commands/sling.ts:397`); others require a lead parent or `--force-hierarchy` (`src/commands/sling.ts:386`).
4. Manifest capability must exist (`src/commands/sling.ts:579`, unknown-capability error `src/commands/sling.ts:587`).
5. Run ID: inherit from parent session → `current-run.txt` → create `run-<ISO-timestamp>` (`src/commands/sling.ts:603`, `src/commands/sling.ts:613`, `src/commands/sling.ts:619`).
6. Limits: per-run session ceiling (`src/commands/sling.ts:345`, enforced `src/commands/sling.ts:637`), global `maxConcurrent` (`src/commands/sling.ts:653`), name auto-generation `capability-taskId` with `-2..-100` suffixing (`src/commands/sling.ts:88`, applied `src/commands/sling.ts:661`), per-task single lock exempting the parent delegator (`src/commands/sling.ts:308`, enforced `src/commands/sling.ts:675`), per-lead child ceiling (`src/commands/sling.ts:361`, enforced `src/commands/sling.ts:691`), stagger sleep between spawns (`src/commands/sling.ts:66`, enforced `src/commands/sling.ts:685`), non-blocking scout-before-build warning for parent-spawned builders (`src/commands/sling.ts:266`, emitted `src/commands/sling.ts:710`), duplicate-lead check helper (`src/commands/sling.ts:330`).
7. Task check (skippable): `tracker.show(taskId)` must succeed and status must be `open` or `in_progress` (`src/commands/sling.ts:728`, workable list `src/commands/sling.ts:740`).
8. Worktree under `config.worktrees.baseDir` (`src/commands/sling.ts:750`); base branch precedence is `--base-branch` → current HEAD → `canonicalBranch` (`src/commands/sling.ts:754`).
9. Overlay: file-scoped mulch expertise is fetched when enabled (`src/commands/sling.ts:774`); runtime resolved before overlay construction (`src/commands/sling.ts:788`); `OverlayConfig` carries agent name, task, spec, branch, worktree, file scope, domains, parent, depth, spawn rights, gates, tracker CLI/name, instruction path (`src/commands/sling.ts:790`); written by `writeOverlay()` (`src/commands/sling.ts:818`).
10. Dispatch mail is sent before boot so it exists when SessionStart fires (`src/commands/sling.ts:831`, message built `src/commands/sling.ts:174`); tracker issue claimed non-fatally (`src/commands/sling.ts:857`); identity created if absent (`src/commands/sling.ts:866`); mulch record IDs extracted for outcome tracking (`src/commands/sling.ts:413`, saved `src/commands/sling.ts:882`).
11. Spawn branches: headless runtimes bypass tmux with file-redirected stdout/stderr to avoid SIGPIPE (signal-broken-pipe) death (`src/commands/sling.ts:896`, log dir `src/commands/sling.ts:919`); otherwise tmux path verifies tmux, builds the spawn command with shared writable dirs (all agents get `.overstory`; only `lead` gets canonical `.git`, per `src/commands/sling.ts:291`), creates `overstory-<project>-<name>`, records the session before the beacon to close the booting→working race, waits for TUI (text user interface) readiness, sends the `[OVERSTORY] name (capability) timestamp task:id` beacon (`src/commands/sling.ts:226`), retries Enters and re-verifies receipt (`src/commands/sling.ts:982`, `src/commands/sling.ts:1006`, `src/commands/sling.ts:1045`, `src/commands/sling.ts:1073`, `src/commands/sling.ts:1101`). Any post-worktree failure rolls back the worktree (`src/commands/sling.ts:1143`).
12. Root execution is refused because the Claude CLI (command-line interface) rejects permission bypass as UID (user identifier) 0 (`src/commands/sling.ts:113`, enforced `src/commands/sling.ts:498`).

## 6. prime command: context injection

`ov prime` loads context for the orchestrator or one agent for hook injection; it is the SessionStart hook target (`src/commands/prime.ts:1`, hook wiring `src/commands/init.ts:441`, CLI registration `src/index.ts:307`). `primeCommand()` (`src/commands/prime.ts:127`) resolves `--agent/--compact/--json/--instruction-path` (`src/commands/prime.ts:128`), loads config (`src/commands/prime.ts:134`), auto-heals `.overstory/.gitignore` (`src/commands/prime.ts:106`, called `src/commands/prime.ts:138`), fetches mulch expertise unless compact (`src/commands/prime.ts:142`), and either prints sections or wraps captured stdout in a JSON envelope (`src/commands/prime.ts:153`).

Agent context (`src/commands/prime.ts:187`) prints identity (sessions-completed, expertise, recent tasks via formatters at `src/commands/prime.ts:66`, `src/commands/prime.ts:35`), warns on fully unknown agents (`src/commands/prime.ts:228`), injects the bound-task activation block pointing at the overlay (`src/commands/prime.ts:240`), and in compact mode appends checkpoint recovery (progress, files, pending work, branch) (`src/commands/prime.ts:248`, formatter `src/commands/prime.ts:89`). Orchestrator context (`src/commands/prime.ts:268`) registers the orchestrator tmux session (`src/commands/prime.ts:274`), records the session branch for merge targeting (`src/commands/prime.ts:289`), prints project/limits (`src/commands/prime.ts:311`), the manifest capability list (`src/commands/prime.ts:320`, formatter `src/commands/prime.ts:35`), and unless compact the last 5 sessions plus expertise (`src/commands/prime.ts:333`, metrics formatter `src/commands/prime.ts:48`).

## 7. init command: scaffolding

`initCommand()` (`src/commands/init.ts:697`) requires a git repo (`src/commands/init.ts:705`), refuses to overwrite without `--force/--yes` (`src/commands/init.ts:719`), detects name from `git remote get-url origin` or directory basename (`src/commands/init.ts:180`) and canonical branch from `refs/remotes/origin/HEAD` → current branch → `main` (`src/commands/init.ts:207`). It creates `.overstory/`, `agents/`, `agent-defs/`, `worktrees/`, `specs/`, `logs/` (`src/commands/init.ts:738`), deploys `agents/*.md` except deprecated `supervisor.md` (`src/commands/init.ts:753`), writes `config.yaml` serialized from `DEFAULT_CONFIG` (`src/commands/init.ts:766`, serializer `src/commands/init.ts:254`), `agent-manifest.json` with 7 roles (scout haiku read-only, builder sonnet, reviewer sonnet read-only, lead opus spawn-capable, merger sonnet, coordinator opus read-only no-worktree, monitor sonnet) plus a capability index (`src/commands/init.ts:777`, builder `src/commands/init.ts:349`), `hooks.json` with SessionStart/UserPromptSubmit/PreToolUse/PostToolUse/Stop/PreCompact hooks including the git-push block (`src/commands/init.ts:783`, builder `src/commands/init.ts:432`), `.gitignore` wildcard-plus-whitelist (`src/commands/init.ts:789`, content `src/commands/init.ts:604`), and `README.md` (`src/commands/init.ts:792`, content `src/commands/init.ts:620`). On `--force/--yes` it migrates `mail.db`/`metrics.db` schemas in place (`src/commands/init.ts:797`, migrator `src/commands/init.ts:543`).

Ecosystem bootstrap covers three sibling tools — mulch (`ml`/`.mulch`), seeds (`sd`/`.seeds`), canopy (`cn`/`.canopy`) (`src/commands/init.ts:60`) — filtered by `--tools` or `--skip-*` (`src/commands/init.ts:75`), probed via `<cli> --version` and skipped with an install hint when absent (`src/commands/init.ts:88`, `src/commands/init.ts:102`), onboarded via `<cli> onboard` (`src/commands/init.ts:136`), union-merged in `.gitattributes` for `.mulch/expertise/*.jsonl` and `.seeds/issues.jsonl` (`src/commands/init.ts:157`), and auto-committed as `chore: initialize overstory and ecosystem tools` when anything staged (`src/commands/init.ts:840`). CLI flags are registered in `src/index.ts:247`.

## 8. Config files and environment variables

`DEFAULT_CONFIG` (`src/config.ts:47`) sets project (`src/config.ts:48`), agents (`src/config.ts:54`: manifest path `src/config.ts:55`, base dir `src/config.ts:56`, maxConcurrent 25 `src/config.ts:57`, stagger 2000 ms `src/config.ts:58`, maxDepth 2 `src/config.ts:59`, maxSessionsPerRun 0 = unlimited `src/config.ts:60`, maxAgentsPerLead 5 `src/config.ts:61`), worktrees dir (`src/config.ts:63`), taskTracker `{ backend: "auto", enabled: true }` (`src/config.ts:66`), mulch (`src/config.ts:70`), merge (`src/config.ts:75`), providers (`src/config.ts:79`), watchdog tiers/thresholds (`src/config.ts:82`), coordinator exit triggers (`src/config.ts:91`), models (`src/config.ts:98`), logging (`src/config.ts:99`), and runtime (`src/config.ts:103`: default `claude` at `src/config.ts:104`, Pi provider plus opus/sonnet/haiku model map at `src/config.ts:106`). Default quality gates are Tests/Lint/Typecheck (`src/config.ts:41`).

The shipped `.overstory/config.yaml` mirrors defaults with `name: overstory`, `canonicalBranch: main`, the three gates, and `taskTracker: { backend: auto, enabled: true }` (`.overstory/config.yaml:4`, `.overstory/config.yaml:8`, `.overstory/config.yaml:28`, `.overstory/config.yaml:58`):

```yaml
agents:
  manifestPath: .overstory/agent-manifest.json
  baseDir: .overstory/agent-defs
  maxConcurrent: 25
  staggerDelayMs: 2000
  maxDepth: 2
  maxSessionsPerRun: 0
  maxAgentsPerLead: 5
taskTracker:
  backend: auto
  enabled: true
runtime:
  default: claude
```

Loading (`src/config.ts:914`) resolves worktree → main root via `git rev-parse --git-common-dir` (`src/config.ts:857`, logic `src/config.ts:870`), falls back to defaults plus local overrides when no file exists (`src/config.ts:929`), otherwise deep-merges file over defaults (`src/config.ts:965`, merger `src/config.ts:368`), then merges gitignored `config.local.yaml` for machine-specific overrides (`src/config.ts:806`, applied `src/config.ts:971`), pins `project.root` to the resolved root (`src/config.ts:974`), and validates (`src/config.ts:976`, validator `src/config.ts:498`). The internal YAML (YAML Ain't Markup Language) parser handles nested indentation, scalars, `- item` arrays, quotes, and comments but not flow syntax, multiline strings, or anchors (`src/config.ts:121`). Legacy `beads:`/`seeds:` top-level keys migrate to `taskTracker:` and old watchdog tier keys migrate with deprecation warnings (`src/config.ts:468`, `src/config.ts:416`).

Environment variables (inherited process environment, not config keys): provider auth comes from the env var named in `authTokenEnv` for gateway providers (`src/config.ts:638`, reachability/token checks `src/doctor/providers.ts:122`); gateway routing sets `ANTHROPIC_BASE_URL` from `baseUrl`, `ANTHROPIC_AUTH_TOKEN` from that env var, and blanks `ANTHROPIC_API_KEY` per spawned agent, while direct Anthropic calls still need `ANTHROPIC_API_KEY` in the orchestrator environment (`README.md:321`, reminder `src/doctor/providers.ts:236`); spawned agents receive `OVERSTORY_AGENT_NAME`, `OVERSTORY_WORKTREE_PATH`, `OVERSTORY_TASK_ID` (`src/commands/sling.ts:897`, tmux path `src/commands/sling.ts:990`), which hook guards use to scope file writes and restrict issue close/update to the agent's own task (`src/agents/hooks-deployer.ts:77`, `src/agents/hooks-deployer.ts:100`, `src/agents/hooks-deployer.ts:291`); color output respects `NO_COLOR`/`FORCE_COLOR`/`TERM=dumb` via chalk (`src/logging/color.ts:4`); `--project <path>` overrides root detection through `setProjectRootOverride()` (`src/config.ts:22`, enforced `src/index.ts:204`).

## 9. CLI entry: index.ts and binary names

Both binaries map to the same entry: `overstory` and `ov` point at `./src/index.ts` (`package.json:23`). `src/index.ts:1` declares the Bun shebang, `program.name("ov")` (`src/index.ts:144`), version `0.8.7` (`src/index.ts:52`, package `package.json:3`), 35 registered command names (`src/index.ts:70`), global flags `--quiet/--json/--verbose/--timing/--project` (`src/index.ts:149`), and a custom help renderer (`src/index.ts:156`). Commands are either factory-registered (`costs` at `src/index.ts:409`, `metrics` at `src/index.ts:411`, plus agents/doctor/coordinator/supervisor/hooks/monitor/worktree/log/watch/group/completions at `src/index.ts:234`) or inline-registered (`init` at `src/index.ts:247`, `sling` at `src/index.ts:266`, `spec write` at `src/index.ts:294`, `prime` at `src/index.ts:307`). Unknown commands get Levenshtein (edit-distance) `Did you mean` suggestions within distance 2 (`src/index.ts:418`, distance `src/index.ts:107`, threshold `src/index.ts:129`). Errors are funneled through typed `OverstoryError` handling with `--json` envelope support (`src/index.ts:433`). The `--version --json` fast path prints name/version/runtime/platform before Commander (command-line parser) runs (`src/index.ts:57`).

## 10. Metrics store

`createMetricsStore()` (`src/metrics/store.ts:213`) opens `bun:sqlite` in WAL mode with 5 s busy timeout (`src/metrics/store.ts:217`), creates `sessions` (`src/metrics/store.ts:68`) and `token_snapshots` (`src/metrics/store.ts:89`) plus the agent-time index (`src/metrics/store.ts:103`), and runs idempotent migrations: `bead_id` → `task_id` (`src/metrics/store.ts:122`), token columns (`src/metrics/store.ts:158`, list `src/metrics/store.ts:109`), `run_id` on both tables (`src/metrics/store.ts:134`, `src/metrics/store.ts:146`). The `sessions` primary key is `(agent_name, task_id)` (`src/metrics/store.ts:86`); rows carry capability, timestamps, duration, exit code, merge result, parent, four token counters, estimated cost, model, and run ID (`src/metrics/store.ts:35`, camelCased `src/metrics/store.ts:170`).

Reads: recent sessions default limit 20 (`src/metrics/store.ts:365`), by agent/run/task (`src/metrics/store.ts:370`, `src/metrics/store.ts:375`, `src/metrics/store.ts:380`), average duration globally or per capability over completed sessions (`src/metrics/store.ts:385`), unbounded count (`src/metrics/store.ts:394`), purge by all/agent returning deleted-row counts (`src/metrics/store.ts:399`). Snapshots: append via `recordSnapshot()` (`src/metrics/store.ts:425`), latest-one-per-agent globally or per run via the `MAX(created_at)` self-join (`src/metrics/store.ts:312`, `src/metrics/store.ts:322`, accessors `src/metrics/store.ts:439`), latest time per agent (`src/metrics/store.ts:448`), purge by all/agent/age (`src/metrics/store.ts:453`). `generateSummary()` (`src/metrics/summary.ts:34`) caps aggregates at 10 000 recent rows (`src/metrics/summary.ts:38`), groups per-capability counts and completed-only averages (`src/metrics/summary.ts:45`, `src/metrics/summary.ts:61`), sums token/cost totals (`src/metrics/summary.ts:72`), and rounds the average (`src/metrics/summary.ts:93`); formatting covers durations (`src/metrics/summary.ts:160`), token counts (`src/metrics/summary.ts:173`), and cost with `$X.XX` (`src/metrics/summary.ts:136`).

## 11. Pricing: per-model costs

Pricing is runtime-agnostic and keyed by lowercase substring match in priority order (`src/metrics/pricing.ts:1`, matcher `src/metrics/pricing.ts:101`). The table at `src/metrics/pricing.ts:30` (USD per million tokens, columns input/output/cache-read/cache-create):

```typescript
opus:          { inputPerMTok: 15,  outputPerMTok: 75, cacheReadPerMTok: 1.5,   cacheCreationPerMTok: 3.75 }
sonnet:        { inputPerMTok: 3,   outputPerMTok: 15, cacheReadPerMTok: 0.3,   cacheCreationPerMTok: 0.75 }
haiku:         { inputPerMTok: 0.8, outputPerMTok: 4,  cacheReadPerMTok: 0.08,  cacheCreationPerMTok: 0.2  }
"gpt-4o-mini": { inputPerMTok: 0.15, outputPerMTok: 0.6, ... }
"gpt-4o":      { inputPerMTok: 2.5,  outputPerMTok: 10,  ... }
"gpt-5":       { inputPerMTok: 10,   outputPerMTok: 40,  ... }
o1:            { inputPerMTok: 15,   outputPerMTok: 60,  ... }
o3:            { inputPerMTok: 10,   outputPerMTok: 40,  ... }
"gemini-flash":{ inputPerMTok: 0.1,  outputPerMTok: 0.4, ... }
"gemini-pro":  { inputPerMTok: 1.25, outputPerMTok: 5,   ... }
```

Exact rows: opus `src/metrics/pricing.ts:32`, sonnet `src/metrics/pricing.ts:38`, haiku `src/metrics/pricing.ts:44`, GPT family `src/metrics/pricing.ts:51`, Gemini `src/metrics/pricing.ts:82`. Match order matters: `gpt-4o-mini` before `gpt-4o`, `o3` before `o1`, `flash` before `gemini+pro` (`src/metrics/pricing.ts:107`). `estimateCost()` (`src/metrics/pricing.ts:123`) returns null for null/unknown models (`src/metrics/pricing.ts:124`, `src/metrics/pricing.ts:126`) and otherwise sums the four linear terms (`src/metrics/pricing.ts:129`).

## 12. Transcript parsing

The Claude Code JSONL parser (`src/metrics/transcript.ts:1`, runtime-agnostic pricing split noted `src/metrics/transcript.ts:8`) scans transcript files line by line, keeps only `type: "assistant"` entries with a `message.usage` object (`src/metrics/transcript.ts:34`, type gate `src/metrics/transcript.ts:44`), maps `input_tokens`/`output_tokens`/`cache_read_input_tokens`/`cache_creation_input_tokens` with non-number fallback to 0 (`src/metrics/transcript.ts:55`), skips malformed lines (`src/metrics/transcript.ts:94`), sums all turns, and takes the model from the first assistant turn (`src/metrics/transcript.ts:74`, model capture `src/metrics/transcript.ts:108`). The expected entry shape is documented inline (`src/metrics/transcript.ts:12`). Other runtimes implement their own parsing via `AgentRuntime.parseTranscript()` (`src/metrics/transcript.ts:9`).

## 13. costs and metrics commands

`ov costs` (`src/commands/costs.ts:565`, executor `src/commands/costs.ts:248`) reads `metrics.db` via the store and validates `--last` as a positive integer defaulting to 20 (`src/commands/costs.ts:258`, default `src/commands/costs.ts:268`). Three modes: `--self` discovers the newest runtime transcript JSONL by mtime (`src/commands/costs.ts:58`, selection `src/commands/costs.ts:78`), parses usage (`src/commands/costs.ts:290`), estimates cost (`src/commands/costs.ts:291`), and prints model/transcript/input/output/cache/cost or the JSON equivalent (`src/commands/costs.ts:275`); `--live` joins latest snapshots to active sessions, skips inactive agents, and derives burn rate and tokens-per-minute from average elapsed time (`src/commands/costs.ts:324`, join `src/commands/costs.ts:375`, skip `src/commands/costs.ts:402`, rates `src/commands/costs.ts:442`); default mode filters by `--agent/--run/--bead` or recent N (`src/commands/costs.ts:528`) and prints either the per-agent table (`src/commands/costs.ts:147`) or the capability-grouped table sorted by cost descending (`src/commands/costs.ts:191`, grouping/sort `src/commands/costs.ts:123`). Flags registered: `--live --self --agent --run --bead --by-capability --last --json` (`src/commands/costs.ts:568`).

`ov metrics` (`src/commands/metrics.ts:105`, executor `src/commands/metrics.ts:21`) defaults to 20 rows (`src/commands/metrics.ts:22`), prints "No metrics data yet." when the DB (database) is absent (`src/commands/metrics.ts:30`), and otherwise reports totals, completed count, average duration, merge-tier distribution, per-capability averages, and the recent table (`src/commands/metrics.ts:56`, tiers `src/commands/metrics.ts:65`, capabilities `src/commands/metrics.ts:80`, table `src/commands/metrics.ts:92`).

## 14. Dependencies

From `package.json:46` (runtime) and `package.json:51` (development):

| Package | Version | Scope | Role |
|---|---|---|---|
| `@os-eco/mulch-cli` | `^0.6.2` | runtime | Programmatic expertise API (record/search/query); CLI wrapper for the rest (`CLAUDE.md:12`) |
| `chalk` | `^5.6.2` | runtime | ESM (ECMAScript Modules)-only color output (`CLAUDE.md:12`) |
| `commander` | `^14.0.3` | runtime | CLI framework: typed options, subcommands, help (`CLAUDE.md:13`) |
| `@biomejs/biome` | `^2.3.15` | dev | Formatter plus linter (`CLAUDE.md:11`) |
| `@types/bun` | `latest` | dev | Bun type definitions |
| `@types/js-yaml` | `^4.0.9` | dev | YAML typing support |
| `typescript` | `^5.9.0` | dev | Strict typechecking (`tsc --noEmit`, `package.json:44`) |

Runtime requires Bun `>=1.0` (`package.json:36`); scripts are `test` → `bun test`, `lint` → `biome check .`, `typecheck` → `tsc --noEmit`, `version:bump` (`package.json:39`). External CLIs (command-line interfaces) are not npm dependencies but subprocesses: `bd` or `sd` for tracking, `mulch`/`ml` for expertise, plus `git` and `tmux` (`CLAUDE.md:15`, convention `CLAUDE.md:221`). The published file set is `src`, `agents`, `templates` (`package.json:28`).

**Covers:** src/tracker/types.ts, src/tracker/beads.ts, src/tracker/seeds.ts, src/tracker/factory.ts, src/beads/client.ts, src/beads/molecules.ts, src/commands/spec.ts, src/commands/sling.ts, src/commands/prime.ts, src/commands/init.ts, src/config.ts, src/metrics/store.ts, src/metrics/pricing.ts, src/metrics/summary.ts, src/metrics/transcript.ts, src/commands/costs.ts, src/commands/metrics.ts, src/index.ts, .overstory/config.yaml, .seeds/config.yaml, package.json, README.md, CLAUDE.md, .claude/commands/, agents/lead.md, agents/coordinator.md
