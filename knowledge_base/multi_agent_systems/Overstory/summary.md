# Technical Analysis: overstory

**Repository:** https://github.com/Marmalade118/overstory
**Version analyzed:** 0.8.7 (commit a961ee5206d85e9d9a37a65ed985de70580f6192, 2026-03-10)
**Date:** 2026-09-09

---

## 1. Overview / What Problem It Solves

Overstory is a multi-agent coding orchestrator: it runs many single-purpose AI agents in parallel without them clobbering each other's files, talking past each other, or merging broken code. Package `@os-eco/overstory-cli` v0.8.7, MIT license, Bun runtime, binaries `overstory` / `ov` both mapping to `src/index.ts`.

The problem it addresses: naive parallel agents share one checkout, one conversation, and one merge path, so concurrent writes conflict, stalled workers go unnoticed, and integration becomes manual. Overstory answers with isolation plus typed coordination: one agent maps to one git worktree plus one branch (`src/worktree/manager.ts:55`, `src/worktree/manager.ts:56`), one role with exactly one job (9 roles; only builder, merger, and lead-for-small-tasks write code per `src/agents/guard-rules.ts:34`), typed mail in SQLite (`src/mail/store.ts:46`), a 3-tier watchdog (T0 daemon, T1 triage, T2 monitor per `src/watchdog/daemon.ts:397`, `src/watchdog/triage.ts:29`, `src/commands/monitor.ts:169`), and a FIFO merge queue with 4-tier conflict escalation (`src/merge/queue.ts:135`, `src/merge/resolver.ts:4`). See [[wiki/targeted|Targeted Brief for Fleet]] for the condensed mapping and [[wiki/01-agent-roles-and-overlays|Agent Roles and Overlays]] for the role catalog.

## 2. High-Level Architecture

Components: role hierarchy with generated overlays and guards; pluggable harness runtime (`AgentRuntime` + registry); git-worktree isolation with tmux/headless process management; SQLite mail (`mail.db`) plus event log (`events.db`); tracker abstraction (seeds `sd` / beads `bd`); SQLite merge queue with 4-tier resolver; 3-tier watchdog with session store; metrics store with pricing.

```
human objective
  │
  ▼
coordinator (depth 0, project root, no overlay) ─► tracker issues (sd / bd)
  │
  ▼
ov sling ─► lead (depth 1, worktree + overlay) ─► scout / builder / reviewer (depth 2, leaf)
  │
  ▼
SQLite mail (mail.db) + events (events.db) ─► watchdog T0 / T1 / T2 supervision
  │
  ▼
FIFO merge queue (merge-queue.db) ─► 4-tier resolver ─► canonical branch
  │
  ▼
metrics store (metrics.db) + transcripts ─► ov costs / ov metrics
```

Data flow in 6 steps. (1) Coordinator decomposes the objective into tracker issues and dispatches leads via `ov sling`, which validates depth/hierarchy, creates the worktree and overlay, claims the issue, and spawns the tmux or headless session (`src/commands/sling.ts:561`, `src/commands/sling.ts:750`, `src/commands/sling.ts:818`). (2) Leads decompose further into specs (`.overstory/specs/<task-id>.md` via `src/commands/spec.ts:40`) and spawn leaf workers at depth+1 (`agents/lead.md:101`). (3) Workers coordinate only through typed mail (`worker_done`, `merge_ready`, `escalation`) with destructive-read `check` semantics and file-based priority nudges (`src/mail/client.ts:156`, `src/commands/mail.ts:27`). (4) The T0 daemon polls tmux/PID liveness plus staleness timers, escalates warn → nudge → AI triage → terminate, and nudges the coordinator once per completed run (`src/watchdog/daemon.ts:569`, `src/watchdog/daemon.ts:190`). (5) Leads verify branches and signal `merge_ready`; integration is serialized through the SQLite FIFO queue with clean-merge → auto-resolve → AI-resolve → reimagine escalation (`src/merge/resolver.ts:235`, `src/merge/resolver.ts:256`, `src/merge/resolver.ts:340`, `src/merge/resolver.ts:415`). (6) Token usage from harness transcripts plus per-model pricing lands in `metrics.db` and surfaces via `ov costs` / `ov metrics` (`src/metrics/transcript.ts:34`, `src/metrics/pricing.ts:123`, `src/commands/costs.ts:248`).

Persistent state: everything durable lives in files under `.overstory/` — `mail.db`, `events.db`, `sessions.db`, `merge-queue.db`, `metrics.db`, `specs/`, `checkpoint.json` / `handoffs.json` per agent, `agent-manifest.json`, `groups.json`, `config.yaml`, `current-run.txt` — never in conversation history, so workers are restartable after compaction or crash. See [[wiki/05-watchdog-and-supervision|Watchdog and Supervision]], [[wiki/03-sqlite-mail-messaging|SQLite Mail Messaging]], [[wiki/06-worktrees-and-isolation|Worktrees and Isolation]].

## 3. The Core Abstraction: Single-Purpose Agents with Overlays and Guards

The core abstraction is the role-shaped agent: hierarchy depth plus a generated per-task overlay plus code-enforced guards. Hierarchy is 3 levels — coordinator (depth 0, spawns only leads) → lead (depth 1, spawns scouts/builders/reviewers at depth 2) → leaf workers that cannot spawn, with supervisor kept only as deprecated alias (`agents/coordinator.md:144`, `agents/coordinator.md:153`, `agents/lead.md:100`, `agents/supervisor.md:1`). Only 3 roles write code (builder, merger, lead for small tasks); scout, reviewer, coordinator, monitor, orchestrator are read-only and blocked from Write/Edit and destructive bash (`src/agents/guard-rules.ts:34`, `src/agents/guard-rules.ts:40`). The manifest (`.overstory/agent-manifest.json`) declares 7 active roles with file, model, tools, capabilities, and `canSpawn`, plus a capability index; task batches live separately in `groups.json` as `{id, name, memberIssueIds, status}` records that auto-close when all member issues close (`src/agents/manifest.ts:145`, `.overstory/agent-manifest.json:2`, `agents/coordinator.md:259`). Complexity triage (simple → lead does it; moderate → one builder; complex → Scout → Build → Verify) is explicit at `agents/lead.md:126`.

Each worker boots from a generated overlay: `generateOverlay()` renders `templates/overlay.md.tmpl` plus role definition, file scope, branch, parent, depth, quality gates, and dispatch overrides (`src/agents/overlay.ts:274`, `src/agents/overlay.ts:299`), written to `{worktreePath}/.claude/CLAUDE.md` with a resolved-path guard refusing writes when the worktree equals the canonical root (`src/agents/overlay.ts:369`, `src/agents/overlay.ts:380`). Read-only roles get a lightweight completion section; writable agents get numbered quality gates plus commit/record/`worker_done`/close steps (`src/agents/overlay.ts:58`, `src/agents/overlay.ts:177`). Dispatch overrides render SKIP REVIEW and MAX AGENTS directives for leads (`src/agents/overlay.ts:80`).

Guards are two layers: shared data constants (10 native team tools, 3 interactive tools, 3 write tools, ~37 dangerous bash patterns, 11 safe prefixes at `src/agents/guard-rules.ts:13`, `src/agents/guard-rules.ts:31`, `src/agents/guard-rules.ts:34`, `src/agents/guard-rules.ts:40`, `src/agents/guard-rules.ts:85`) and deployed hooks in `.overstory/hooks.json` that block `git push` and log every tool call (`.overstory/hooks.json:31`). Lifecycle state (`checkpoint.json` per agent, `handoffs.json` with pending `toSessionId: null` records) and identity CVs (`identity.yaml` with capability, session count, domains, last 20 tasks) complete the abstraction (`src/agents/checkpoint.ts:14`, `src/agents/lifecycle.ts:72`, `src/agents/identity.ts:253`). See [[wiki/01-agent-roles-and-overlays|Agent Roles and Overlays]].

## 4. LLM/External Service Integration

There is no direct LLM (large language model) SDK dependency. All model access goes through harness CLIs (command-line interfaces) behind the `AgentRuntime` interface (`src/runtimes/types.ts:148`): `buildSpawnCommand` (interactive tmux), `buildPrintCommand` (headless one-shot for merge/triage), `buildDirectSpawn`/`parseEvents` (headless streaming, Sapling only), `deployConfig`, `detectReady`, `parseTranscript`, `getTranscriptDir`, `buildEnv`. Eight adapters are registered in `src/runtimes/registry.ts:16` (`claude`, `codex`, `pi`, `copilot`, `cursor`, `gemini`, `sapling`, `opencode`); only Claude (`src/runtimes/claude.ts:35`) and Sapling (`src/runtimes/sapling.ts:349`) are `stable`, the rest `experimental`, and only Sapling is headless (`src/runtimes/sapling.ts:358`). Guard deployment differs per harness: Claude writes hooks via `deployHooks` (`src/runtimes/claude.ts:129`), Pi generates a TypeScript extension (`src/runtimes/pi-guards.ts:128`), Sapling writes `.sapling/guards.json` (`src/runtimes/sapling.ts:98`); the other five deploy no guards. Readiness is per-harness screen scraping (Claude prompt marker plus bypass-permissions dialogs at `src/runtimes/claude.ts:153`; Pi header plus status-bar regex at `src/runtimes/pi.ts:174`; Codex/Sapling always ready; OpenCode always loading stub at `src/runtimes/opencode.ts:138`). RPC (remote procedure call) is defined by `RuntimeConnection` (`src/runtimes/types.ts:102`) but only Sapling implements `connect()` (`src/runtimes/sapling.ts:662`); no adapter implements session resume. AI-assisted internals reuse the same abstraction: merge AI-resolve and watchdog triage both resolve a print-command runtime and call `buildPrintCommand` (`src/merge/resolver.ts:367`, `src/watchdog/triage.ts:144`). Token accounting normalizes per-harness transcripts to one `TranscriptSummary` shape (`src/runtimes/types.ts:66`); Claude Code JSONL (JSON Lines) parsing sums `message.usage` across assistant turns (`src/metrics/transcript.ts:34`), other harnesses parse their own formats (Codex turn usage, Pi v3 message events, Gemini `result.stats`), and Cursor exposes no usage so tokens stay zero (`src/runtimes/cursor.ts:156`).

External services are all local-subprocess CLIs, not network APIs: issue trackers `bd` (beads) or `sd` (seeds) via `Bun.spawn` (`src/beads/client.ts:53`, `src/tracker/seeds.ts:19`); expertise store `mulch`/`ml` (`ml prime`, `ml record`); `git` and `tmux` for isolation. Provider auth flows through environment: gateway providers use the env var named in `authTokenEnv`, spawned agents get `ANTHROPIC_BASE_URL` / blanked `ANTHROPIC_API_KEY` mapping, direct Anthropic calls still need `ANTHROPIC_API_KEY`, and per-agent scoping uses `OVERSTORY_AGENT_NAME` / `OVERSTORY_WORKTREE_PATH` / `OVERSTORY_TASK_ID` (`src/commands/sling.ts:897`, `README.md:321`). Model names resolve as config override → manifest default → fallback with `sonnet/opus/haiku` alias expansion (`src/agents/manifest.ts:348`). See [[wiki/02-multi-harness-runtime|Multi-Harness Runtime]] and [[wiki/07-tracker-workflows-metrics|Tracker, Workflows, Metrics]].

## 5. The Main Pipeline: Sling → Work → Verify → Merge

The main pipeline is the 14-step `ov sling` spawn followed by mail-coordinated work, review, and queued merge, with `file:line` refs below.

Spawn (`src/commands/sling.ts:1` header lists the 14 steps): (1) `loadConfig` then `resolveBackend` (`src/commands/sling.ts:561`); depth reject when `depth > maxDepth`, default ceiling 2 (`src/commands/sling.ts:568`); hierarchy check — parentless coordinator may spawn only lead/scout/builder, others need a lead parent or `--force-hierarchy` (`src/commands/sling.ts:397`, `src/commands/sling.ts:386`); manifest capability must exist (`src/commands/sling.ts:579`); run-ID inherit from parent → `current-run.txt` → new `run-<timestamp>` (`src/commands/sling.ts:603`); concurrency/name/task/lead-child ceilings plus stagger sleep (`src/commands/sling.ts:637`, `src/commands/sling.ts:653`, `src/commands/sling.ts:675`, `src/commands/sling.ts:691`, `src/commands/sling.ts:685`); task must be `open`/`in_progress` unless `--skip-task-check` (`src/commands/sling.ts:728`); worktree under `config.worktrees.baseDir` via `git worktree add -b overstory/{agent}/{task}` (`src/commands/sling.ts:750`, `src/worktree/manager.ts:58`); overlay written by `writeOverlay()` with file-scoped mulch expertise (`src/commands/sling.ts:774`, `src/commands/sling.ts:818`); dispatch mail sent before boot so SessionStart sees it (`src/commands/sling.ts:831`); issue claimed non-fatally plus identity created (`src/commands/sling.ts:857`, `src/commands/sling.ts:866`); tmux path (beacon `[OVERSTORY] name (capability) timestamp task:id` with Enter retries at `src/commands/sling.ts:982`) or headless path with file-redirected stdout/stderr (`src/commands/sling.ts:896`); any post-worktree failure rolls back the worktree (`src/commands/sling.ts:1143`); root execution refused (`src/commands/sling.ts:498`).

Work and verify: builders implement within FILE_SCOPE, pass quality gates, commit to their branch, `ml record`, send `worker_done`, close the issue (`agents/builder.md:52`); reviewers diff, run gates, report `PASS:`/`FAIL:` by mail without editing (`agents/reviewer.md:109`); leads verify commits/issue/exit code then send `merge_ready` (`agents/supervisor.md:223`); coordinator merges only on typed `merge_ready` and closes the issue only after merge success (`agents/coordinator.md:224`, `agents/coordinator.md:291`). Mail fan-out for `@all`/`@capability` inserts N independent rows (`src/commands/mail.ts:327`, `src/mail/broadcast.ts:51`); urgent/high or 5 protocol types write `.overstory/pending-nudges/{agent}.json`, with immediate tmux poke only for `dispatch` (`src/commands/mail.ts:27`, `src/commands/mail.ts:479`).

Merge (`src/commands/merge.ts:140`): target resolves `--into` → `session-branch.txt` → canonical branch (`src/commands/merge.ts:149`); queue at `.overstory/merge-queue.db` ordered by autoincrement id (`src/merge/queue.ts:135`); ad-hoc branches verified via `git rev-parse` and enqueued with `git diff --name-only canonical...branch` (`src/commands/merge.ts:200`); Tier 1 `git merge --no-edit` (`src/merge/resolver.ts:235`) → Tier 2 keep-incoming auto-resolve with canonical-content guard and `merge=union` concatenation (`src/merge/resolver.ts:142`, `src/merge/resolver.ts:273`, `src/merge/resolver.ts:173`) → Tier 3 per-file model resolve with `looksLikeProse()` rejection (`src/merge/resolver.ts:340`, `src/merge/resolver.ts:314`) → Tier 4 abort plus reimplement from `git show canonical:file` vs `git show branch:file` (`src/merge/resolver.ts:415`); outcomes recorded to mulch with 2-failures-0-successes tier skipping (`src/merge/resolver.ts:626`, `src/merge/resolver.ts:576`); cleanup via `ov worktree clean` is merge-gated by `git merge-base --is-ancestor` unless `--force` (`src/commands/worktree.ts:117`). See [[wiki/04-merge-queue-and-conflicts|Merge Queue and Conflicts]], [[wiki/06-worktrees-and-isolation|Worktrees and Isolation]].

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `src/index.ts` | 473 | CLI entry; both `overstory`/`ov` bins; 35 commands; global flags; Levenshtein suggestions |
| `src/commands/sling.ts` | 1150 | 14-step spawn pipeline: config, depth/hierarchy, locks, worktree, overlay, mail, tmux/headless |
| `src/agents/overlay.ts` | 408 | `generateOverlay()` template rendering; read-only vs writable sections; root-write guard |
| `src/agents/guard-rules.ts` | 97 | Shared blocklists/allowlists: team/interactive/write tools, bash patterns, safe prefixes |
| `src/runtimes/types.ts` | 249 | `AgentRuntime` interface: 8 required + 4 optional members; spawn/print/deploy/ready/transcript/env |
| `src/runtimes/registry.ts` | 90 | Name→factory map for 8 harnesses; name → capability → default → `claude` resolution |
| `src/mail/store.ts` | 387 | `messages` table DDL (11 cols, 2 indexes); WAL mode; migration; unread/list/purge queries |
| `src/mail/client.ts` | 223 | `send`/`sendProtocol`/`check`/`checkInject`/`list`/`markRead`/`reply`; destructive-read + inject format |
| `src/merge/queue.ts` | 246 | SQLite FIFO `merge_queue` table; `enqueue`/`dequeue`/`peek`/`list`/`updateStatus` |
| `src/merge/resolver.ts` | 932 | 4-tier resolver (clean/auto/AI/reimagine); pre-merge guards; mulch learning loop |
| `src/commands/merge.ts` | 325 | `ov merge --branch/--all` surface; target resolution; ad-hoc enqueue; status writeback |
| `src/watchdog/daemon.ts` | 805 | T0 daemon ticks; L0–L3 escalation; headless tailers; run-completion nudge |
| `src/watchdog/triage.ts` | 189 | T1 one-word classifier (`retry`/`terminate`/`extend`) over last-50-log-lines prompt |
| `src/worktree/manager.ts` | 350 | `git worktree add -b`; rollback; porcelain parse; merge detection; `.seeds/` preservation |
| `src/worktree/tmux.ts` | 685 | tmux lifecycle: sessions, pane PID, readiness wait, sendKeys, SIGTERM→SIGKILL tree kill |
| `src/config.ts` | 979 | `DEFAULT_CONFIG`; worktree-aware root resolution; YAML merge; validation; migrations |
| `src/metrics/store.ts` | 501 | `sessions` + `token_snapshots` tables; reads by agent/run/task; snapshot latest-view |
| `src/tracker/factory.ts` | 64 | `beads`/`seeds` switch; `auto` probing (`.seeds/` first); `sd`/`bd` CLI name map |
| `src/sessions/store.ts` | 574 | `sessions` + `runs` tables; `upsert`; escalation columns; run lifecycle |
| `src/commands/mail.ts` | ~720 | `ov mail send/check/list/read/reply/purge`; broadcast fan-out; nudge markers; debounce |

## 7. Dependencies

Required (runtime, `package.json:46`):

| Package | Version constraint | Purpose |
|---|---|---|
| `@os-eco/mulch-cli` | `^0.6.2` | Expertise API (`ml prime` / `ml record`); pattern search for merge history and overlays |
| `chalk` | `^5.6.2` | ESM-only terminal color output; respects `NO_COLOR` / `FORCE_COLOR` |
| `commander` | `^14.0.3` | CLI framework: subcommands, typed options, help rendering |

Required runtime environment (not npm): `bun >= 1.0` (`package.json:36`); `git` (worktrees, branches, merges); `tmux` (TUI agent sessions); one harness CLI (`claude`, `pi`, `codex`, `copilot`, `agent`, `gemini`, `opencode`, `sp`); one tracker CLI (`sd` or `bd`).

Optional / development (`package.json:51`):

| Package | Version constraint | Purpose |
|---|---|---|
| `@biomejs/biome` | `^2.3.15` | Formatter plus linter (`bun run lint`) |
| `@types/bun` | `latest` | Bun type definitions |
| `@types/js-yaml` | `^4.0.9` | YAML typing support |
| `typescript` | `^5.9.0` | Strict typechecking (`tsc --noEmit`) |

## 8. CLI/Usage Surface

Main commands (registered in `src/index.ts:70`; `program.name("ov")` at `src/index.ts:144`):

| Command | Purpose |
|---|---|
| `ov init [--force] [--tools]` | Scaffold `.overstory/`, `agents/`, `config.yaml`, manifest, hooks, `.gitignore`; onboard mulch/seeds/canopy |
| `ov sling <task-id>` | Spawn agent: `--capability`, `--name`, `--spec`, `--files`, `--parent`, `--depth`, `--skip-scout`, `--skip-review`, `--max-agents`, `--runtime`, `--base-branch` |
| `ov spec write <task-id>` | Persist spec to `.overstory/specs/<task-id>.md` via `--body` or stdin, optional `--agent` |
| `ov mail send/check/list/read/reply/purge` | Typed agent messaging; `--inject` for hook format; `--debounce <ms>`; `@all`/`@capability` fan-out |
| `ov merge --branch/--all` | Integrate branches; `--into`, `--dry-run`, `--json`; `--all` processes FIFO pending queue |
| `ov watch [--interval] [--background]` | Run T0 daemon foreground or detached via `watchdog.pid` |
| `ov monitor/coordinator/supervisor start/stop/status` | Lifecycle for persistent roles (supervisor deprecated, use lead) |
| `ov worktree list/clean` | Inspect and merge-gated cleanup (`--completed`, `--all`, `--force`, `--json`) |
| `ov stop <agent>` / `ov run` | Kill one agent (optionally `--clean-worktree`); manage run groupings, not processes |
| `ov prime [--agent] [--compact]` | SessionStart context injection: identity, task, checkpoint recovery, capability list |
| `ov costs [--live/--self/--agent/--run/--bead/--by-capability/--last]` | Token spend from transcripts/snapshots with pricing |
| `ov metrics` | Session totals, durations, merge-tier distribution, per-capability averages |
| `ov group / ov status / ov log` | Batch tracking, fleet status, event log inspection |

Environment variables:

| Variable | Purpose |
|---|---|
| `ANTHROPIC_API_KEY` | Direct Anthropic auth for orchestrator-side calls |
| `ANTHROPIC_BASE_URL` / `ANTHROPIC_AUTH_TOKEN` | Gateway routing for spawned agents (base URL plus token source) |
| `ANTHROPIC_DEFAULT_*_MODEL` | `opus`/`sonnet`/`haiku` alias expansion for gateways and Sapling direct spawn |
| `OVERSTORY_AGENT_NAME` / `OVERSTORY_WORKTREE_PATH` / `OVERSTORY_TASK_ID` | Per-agent scoping consumed by hooks (file writes, issue close rights) |
| `NO_COLOR` / `FORCE_COLOR` / `TERM` | Color output control via chalk (`src/logging/color.ts:4`) |
| `HOME` | Transcript discovery root (`~/.claude/projects/`, `~/.pi/agent/sessions/`) |
| `TMUX` | Detect whether inside tmux (`getCurrentSessionName`) |

Config files:

| File | Purpose |
|---|---|
| `.overstory/config.yaml` | Project overrides: canonical branch, gates, tracker backend, merge tiers, watchdog, runtime default |
| `.overstory/config.local.yaml` | Git-ignored machine-specific overrides, merged last (`src/config.ts:806`) |
| `.overstory/agent-manifest.json` | 7 roles with file/model/tools/capabilities/`canSpawn` plus capability index |
| `.overstory/hooks.json` | SessionStart/prompt/PreToolUse/PostToolUse/Stop/PreCompact hooks incl. `git push` block |
| `.overstory/groups.json` | Task-group `{id, name, memberIssueIds, status}` batch records |
| `.overstory/mail-check-state.json` | Per-agent debounce timestamps for `mail check --debounce` |
| `.overstory/current-run.txt` / `run-complete-notified.txt` | Active run ID plus once-per-run completion-dedup marker |
| `.seeds/config.yaml` / `.beads/` | Tracker backend presence probes for `auto` resolution |

## 9. Extensibility Points

Add a harness by creating `src/runtimes/<name>.ts` implementing `AgentRuntime`, registering the factory in `src/runtimes/registry.ts:16`, adding config types under `OverstoryConfig.runtime` if needed, colocating `src/runtimes/<name>.test.ts` with real temp-directory I/O, then using `ov sling --runtime <name>` or setting `runtime.default` (`docs/runtime-adapters.md:516`). If construction needs config like Pi, add a special case beside the Pi branch (`src/runtimes/registry.ts:79`). Guard policy extends in two places that must stay in sync: `src/agents/guard-rules.ts` (Claude hooks) and `src/runtimes/pi-guards.ts` plus `src/runtimes/sapling.ts:98` (Pi extension, Sapling JSON) — the file-modifying bash list is currently duplicated because the source list is not exported (`src/runtimes/pi-guards.ts:38`). Tracker backends extend via the 7-method `TrackerClient` (`ready/show/create/claim/close/list/sync` at `src/tracker/types.ts:25`) plus a factory case (`src/tracker/factory.ts:18`); beads-only molecules (`bd mol create/step/pour/list/status` at `src/beads/molecules.ts:98`) show how workflow prototypes layer on top. Merge tiers toggle via `aiResolveEnabled`/`reimagineEnabled` config flags (`src/commands/merge.ts:162`); watchdog tiers toggle via `tier1Enabled`/`tier2Enabled` with thresholds (`src/config.ts:82`). New CLIs follow the factory-or-inline pattern in `src/index.ts:234` with `OverstoryError` funneling and `--json` envelopes (`src/index.ts:433`). Doctor checks (`src/doctor/merge-queue.ts:40`) and `ov init` scaffolding (`src/commands/init.ts:697`) are the extension points for new health rules and project templates.

## 10. Limitations and Gotchas

Stale-code hazard: the daemon header still describes an old Phase-4 tier numbering ("Tier 2 = Monitor not yet implemented") while `ov monitor` plus `agents/monitor.md` implement the current T2 patrol — trust the commands, not the comment (`src/watchdog/daemon.ts:13`). Five of eight harness adapters deploy no guards (Codex, Copilot, Cursor, Gemini, OpenCode), so role-shaped constraints are prompt-only there. OpenCode is an acknowledged stub (`detectReady` always loading, `parseTranscript` always null at `src/runtimes/opencode.ts:138`, `src/runtimes/opencode.ts:155`); Cursor reports zero tokens because its stream JSON exposes no usage (`src/runtimes/cursor.ts:156`). No adapter implements session resume; resume exists only in design docs (`docs/runtime-abstraction.md:756`). Mail is at-most-once per `check` with crash-between-SELECT-and-UPDATE redelivery risk, and broadcast fan-out can deliver to a recipient prefix on partial failure (`src/mail/client.ts:156`, `src/commands/mail.ts:327`). Priority never reorders storage, only display plus nudge (`src/mail/client.ts:104`). Cleanup defaults to completed/zombie only and refuses unmerged branches without `--force` (`src/commands/worktree.ts:109`, `src/commands/worktree.ts:117`); lead branches are never merged so only their `.seeds/` diff is preserved (`src/worktree/manager.ts:249`). Coordinator merge requires an explicit typed `merge_ready` mail — `ov status` showing done builders is insufficient (`agents/coordinator.md:224`); issue close must follow merge, never precede it (`agents/coordinator.md:291`). Monitor must not poll faster than every 2 minutes (`agents/monitor.md:112`); `ov sling` refuses root execution (UID 0) because the Claude CLI rejects permission bypass (`src/commands/sling.ts:498`). Config YAML parser handles nesting and `- item` arrays but not flow syntax, multiline strings, or anchors (`src/config.ts:121`). Event recording is fire-and-forget everywhere, so observability loss is silent by design (`src/commands/mail.ts:442`, `src/events/tailer.ts:162`).

## 11. How It Compares to Alternatives

- **Claude Code Task/TeamCreate subagents (native).** In-session spawning with no persistent worktree isolation, SQLite mail, or merge queue; Overstory is the durable multi-shell alternative with file-backed state and serialized integration.
- **Aider with `--restore-chat-history` / multi-chat.** Strong single-agent editing with history resume but no role hierarchy, guard plane, or watchdog supervision; Overstory adds the fleet layer (overlays, nudges, triage, monitor patrol) at the cost of heavier scaffolding.
- **Muse / Copilot agent mode (GitHub).** Managed TUI/IDE agent with sandbox but single-threaded task focus and no FIFO merge queue or per-role tool guards; Overstory targets parallel workstreams with explicit conflict-escalation tiers instead.
- **MetaGPT / ChatDev role pipelines.** Fixed SOP (standard operating procedure) role chains with in-memory handoff; Overstory replaces the fixed chain with a depth-capped spawn tree, file-scoped worktrees, and SQLite-backed mail/checkpoints that survive restarts.

Positioning in one sentence: Overstory is the isolation-first, SQLite-state-first orchestrator for parallel coding agents where other tools offer single-agent assistance or ephemeral subagents.

---

## Appendix: Selected Code Snippets

### A1. Guard blocklists as data — `src/agents/guard-rules.ts:13-40`

```typescript
export const NATIVE_TEAM_TOOLS = [
	"Task",
	"TeamCreate",
	"TeamDelete",
	"SendMessage",
	"TaskCreate",
	"TaskUpdate",
	"TaskList",
	"TaskGet",
	"TaskOutput",
	"TaskStop",
];

/**
 * Tools that require human interaction and block indefinitely in non-interactive
 * tmux sessions. Agents run non-interactively and must never call these tools.
 * Use overstory mail (--type question) to escalate to the orchestrator instead.
 */
export const INTERACTIVE_TOOLS = ["AskUserQuestion", "EnterPlanMode", "EnterWorktree"];

/** Tools that non-implementation agents must not use. */
export const WRITE_TOOLS = ["Write", "Edit", "NotebookEdit"];
```

### A2. Merge queue schema and FIFO selector — `src/merge/queue.ts:45-62`, `src/merge/queue.ts:135-137`

```sql
CREATE TABLE IF NOT EXISTS merge_queue (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  branch_name TEXT NOT NULL,
  task_id TEXT NOT NULL,
  agent_name TEXT NOT NULL,
  files_modified TEXT NOT NULL DEFAULT '[]',
  enqueued_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%f','now')),
  status TEXT NOT NULL DEFAULT 'pending'
    CHECK(status IN ('pending','merging','merged','conflict','failed')),
  resolved_tier TEXT
    CHECK(resolved_tier IS NULL OR resolved_tier IN ('clean-merge','auto-resolve','ai-resolve','reimagine'))
)
```

```sql
SELECT * FROM merge_queue WHERE status = 'pending' ORDER BY id ASC LIMIT 1
```

### A3. AgentRuntime contract header — `src/runtimes/types.ts:141-170`

```typescript
// The orchestration engine calls only these methods, never the runtime CLI directly.
export interface AgentRuntime {
	/** Unique runtime identifier (e.g. "claude", "codex", "pi"). */
	id: string;

	/** Stability level of this runtime adapter. */
	readonly stability: "stable" | "beta" | "experimental";

	/** Relative path to the instruction file within a worktree (e.g. ".claude/CLAUDE.md"). */
	readonly instructionPath: string;

	/** Build the shell command string to spawn an interactive agent in a tmux pane. */
	buildSpawnCommand(opts: SpawnOpts): string;

	/**
	 * Build the argv array for a headless one-shot AI call.
	 * Used by merge/resolver.ts and watchdog/triage.ts for AI-assisted operations.
	 */
	buildPrintCommand(prompt: string, model?: string): string[];

	/**
	 * Deploy per-agent instructions and guards to a worktree.
	 * Claude Code writes .claude/CLAUDE.md + settings.local.json hooks.
	 * Codex writes AGENTS.md (no hook deployment needed).
	 * Pi writes .claude/CLAUDE.md + a guard extension in .pi/extensions/.
	 * When overlay is undefined, only hooks are deployed (no instruction file written).
	 */
	deployConfig(
		worktreePath: string,
		overlay: OverlayContent | undefined,
		hooks: HooksDef,
	): Promise<void>;
```
