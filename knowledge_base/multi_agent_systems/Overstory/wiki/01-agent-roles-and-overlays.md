> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Agent Roles, Overlays, and Guards

**In one sentence:** Overstory splits work across 9 specialized agent roles coordinated through generated per-task overlays, code-enforced tool-call guards, checkpoint/handoff lifecycle files, per-agent identity records, and a manifest plus task-group registry.

## Key points

- Hierarchy is 3 levels: coordinator (depth 0, spawns only leads) → lead (depth 1, spawns scouts/builders/reviewers at depth 2) → leaf workers that cannot spawn, with supervisor kept only as a deprecated alias of lead (`agents/coordinator.md:144`, `agents/coordinator.md:153`, `agents/lead.md:100`, `agents/supervisor.md:1`).
- Only 3 roles write code: builder, merger, and lead (for small tasks); scout, reviewer, coordinator, monitor, and orchestrator are read-only and blocked from Write/Edit and destructive bash by guard lists (`src/agents/guard-rules.ts:34`, `src/agents/guard-rules.ts:40`, `agents/scout.md:23`, `agents/reviewer.md:23`).
- Each worker gets a generated overlay file (a per-task instruction sheet, by default `.claude/CLAUDE.md` in its worktree) built by `generateOverlay()` from `templates/overlay.md.tmpl` plus the role definition, file scope, branch, parent, depth, quality gates, and dispatch overrides (`src/agents/overlay.ts:274`, `templates/overlay.md.tmpl:12`, `src/agents/overlay.ts:299`).
- Guards work at two layers: shared blocklists/allowlists in `guard-rules.ts` (10 native team tools, 3 interactive tools, 3 write tools, ~37 dangerous bash patterns, 11 safe prefixes) and deployed hooks in `.overstory/hooks.json` that block `git push` and log every tool call (`src/agents/guard-rules.ts:13`, `src/agents/guard-rules.ts:31`, `src/agents/guard-rules.ts:85`, `.overstory/hooks.json:31`).
- Lifecycle state lives outside conversation history in files: `checkpoint.json` per agent plus `handoffs.json` for session replacement, with `save/load/clearCheckpoint` and `initiate/resume/completeHandoff` as the only API (`src/agents/checkpoint.ts:14`, `src/agents/checkpoint.ts:48`, `src/agents/checkpoint.ts:86`, `src/agents/lifecycle.ts:72`, `src/agents/lifecycle.ts:120`, `src/agents/lifecycle.ts:157`).
- Identity is a per-agent CV (curriculum vitae, meaning a work-history record) at `{agentsDir}/{name}/identity.yaml` holding name, capability, creation time, session count, expertise domains, and up to 20 recent tasks with deduplicated domain merge on update (`src/agents/identity.ts:253`, `src/agents/identity.ts:288`, `src/agents/identity.ts:335`, `src/agents/identity.ts:7`).
- The manifest (`.overstory/agent-manifest.json`) declares 7 active roles with file, model, tools, capabilities, `canSpawn` (ability to create sub-agents), and constraints, plus a capability index; task batches are tracked separately in `groups.json` as `{id, name, memberIssueIds, status, createdAt, completedAt}` records that auto-close when all member issues close (`src/agents/manifest.ts:145`, `.overstory/agent-manifest.json:2`, `.overstory/groups.json:3`, `agents/coordinator.md:259`).

---

## Role hierarchy at a glance

Overstory uses a tree of agents. CLAUDE.md here means the instruction file each Claude Code session reads at startup; overlay means the per-task section appended to it.

```
orchestrator (ecosystem root, multi-repo; starts coordinators, never slings)
  └── coordinator (depth 0, project root, no overlay, spawns ONLY leads)
        └── lead (depth 1, worktree, spawns scouts/builders/reviewers at depth 2)
              ├── scout (depth 2, leaf, read-only explorer)
              ├── builder (depth 2, leaf, implements code + tests)
              ├── reviewer (depth 2, leaf, read-only validator)
              └── merger (depth 2, leaf, branch integrator)
monitor (sidecar patrol agent, Tier 2 watchdog brain; observes, never spawns)
supervisor (deprecated alias of lead, kept for compatibility)
```

The coordinator hierarchy is stated explicitly in code and docs: coordinator spawns only leads and this is code-enforced by `sling.ts` raising a `HierarchyError` otherwise (`agents/coordinator.md:144`, `agents/coordinator.md:49`). Depth numbering is fixed: coordinator is depth 0 and its leads are depth 1 (`agents/coordinator.md:153`), with the tree drawn at (`agents/coordinator.md:155`). Leads spawn sub-workers one level deeper via `ov sling` with `--parent` and `--depth current+1` (`agents/lead.md:101`). Leaf nodes (workers that do the actual file work, such as builder/scout) must never spawn sub-workers (`agents/builder.md:31`, `agents/merger.md:30`).

## The 9 roles

### 1. Coordinator — the project brain

The coordinator is the persistent top-level decision-maker for one project: it takes a human objective, creates high-level tracker issues, dispatches leads, monitors mail and status, handles escalations by severity, and merges branches (`agents/coordinator.md:115`, `agents/coordinator.md:119`).

Key mechanics:

- Runs at the project root with full read visibility but no write access and no worktree (`agents/coordinator.md:56`, `agents/coordinator.md:44`).
- Unlike other roles it gets no per-task overlay; objectives arrive via direct human instruction, mail, tracker CLI (`sd`/`bd`, the issue-tracker command), and its checkpoint file (`agents/coordinator.md:33`, `agents/coordinator.md:345`).
- Target shape is 2–5 leads per batch, each managing 2–5 builders, i.e. 4–25 effective workers (`agents/coordinator.md:28`).
- Merge is strictly gated: only a typed `merge_ready` mail from the owning lead authorizes `ov merge`; watchdog nudges and `ov status` showing completed builders are informational only (`agents/coordinator.md:24`, `agents/coordinator.md:224`). Issue close follows merge, never precedes it (`agents/coordinator.md:25`, `agents/coordinator.md:291`).

### 2. Supervisor — deprecated, use lead

The supervisor file opens with an explicit deprecation notice pointing to `lead.md` (`agents/supervisor.md:1`). It describes the same job the lead now does: receive a dispatch, decompose into worker subtasks, spawn builders/scouts/reviewers at depth 2, verify branches, and signal `merge_ready` (`agents/supervisor.md:80`, `agents/supervisor.md:84`). Its overlay fields (agent name, task ID, spec path, depth always 1, parent always `coordinator`, branch) are documented at (`agents/supervisor.md:34`). Nudge escalation after 3 attempts and severity routing (warning/error/critical) live at (`agents/supervisor.md:292`, `agents/supervisor.md:335`).

### 3. Lead — team lead and the only role with flexible scope

The lead is both coordinator and occasional doer: it decomposes work, delegates to specialists, verifies results, and for simple tasks implements directly (`agents/lead.md:73`, `agents/lead.md:77`).

Complexity triage is explicit (`agents/lead.md:126`):

- Simple (all must hold: 1–3 files, well-understood, no cross-cutting concerns, enough context, no architecture calls): lead does it directly, no spawns (`agents/lead.md:130`).
- Moderate (any: 3–6 files focused, clear spec, single builder suffices): skip scouts, spawn one builder, self-verify by reading the diff plus quality gates (`agents/lead.md:140`).
- Complex (any: 6+ files or multi-subsystem, unfamiliar code, cross-cutting/architectural, needs parallel builders): full Scout → Build → Verify pipeline (`agents/lead.md:148`).

Lead pipeline phases are Scout, Build, Review-and-Verify (`agents/lead.md:159`, `agents/lead.md:203`, `agents/lead.md:226`). Dispatch overrides in the overlay can set SKIP REVIEW (self-verify instead of spawning a reviewer) and MAX AGENTS (per-lead spawn ceiling) (`agents/lead.md:5`, `src/agents/overlay.ts:80`). Leads must never create tracker issues inside a worktree; they mail the coordinator to create them on main (`agents/lead.md:59`, `agents/lead.md:42`).

### 4. Scout — read-only explorer

Scouts do reconnaissance: explore, gather information, report findings, never modify anything (`agents/scout.md:63`, `agents/scout.md:69`). Read-only status is non-negotiable with one narrow exception, `ov spec write` for persisting spec files (`agents/scout.md:23`, `agents/scout.md:25`). Allowed tools are Read, Glob, Grep, and read-only Bash plus `ov spec write` and mail (`agents/scout.md:73`). The workflow is overlay → spec → `ml prime` (load domain expertise from mulch, the project knowledge store) → systematic explore → `ov spec write <task-id>` → short result mail → close issue (`agents/scout.md:100`, `agents/scout.md:107`).

### 5. Builder — implementation specialist

Builders implement a spec within an exclusive file scope and commit to their worktree branch only (`agents/builder.md:75`, `agents/builder.md:79`). Constraints: all writes inside the assigned worktree directory, only files in FILE_SCOPE (the exact file list the agent owns), never push to the canonical (main shared) branch, never run `git push`, never spawn sub-workers, and pass quality gates before closing (`agents/builder.md:27`, `agents/builder.md:28`, `agents/builder.md:29`, `agents/builder.md:31`, `agents/builder.md:32`). Completion order is quality gates → commit → `ml record` (required knowledge capture) → `worker_done` mail → tracker close → exit (`agents/builder.md:52`).

### 6. Reviewer — read-only validator

Reviewers validate code for correctness, style, security, coverage, and convention adherence, running tests/linters but never editing (`agents/reviewer.md:63`, `agents/reviewer.md:69`). They share the scout's strict read-only constraints (`agents/reviewer.md:23`). The checklist covers correctness, tests, strict TypeScript types, error handling, style, security (secrets, injection, path traversal), dependencies, and performance (`agents/reviewer.md:125`). Close reason is an explicit `PASS:`/`FAIL:` summary plus a detailed mail report (`agents/reviewer.md:109`, `agents/reviewer.md:115`).

### 7. Merger — tiered branch integrator

Mergers integrate completed worker branches into the target branch through 4 escalating tiers, preserving history (`agents/merger.md:64`, `agents/merger.md:70`):

- Tier 1 Clean Merge: `git merge <branch> --no-edit`; success plus passing tests ends the job (`agents/merger.md:108`).
- Tier 2 Auto-Resolve: hand-fix simple non-overlapping conflict markers, `git add` and commit (`agents/merger.md:114`).
- Tier 3 AI-Resolve: read both versions, understand intent from specs/commits, write a merged version preserving both (`agents/merger.md:120`).
- Tier 4 Reimagine (last resort): fresh checkout of target, reimplement the spec against current state, and report that reimagine was needed (`agents/merger.md:127`).

Failure modes forbid tier-skipping, unverified merges, and scope creep beyond conflict resolution (`agents/merger.md:13`). Non-trivial (Tier 2+) merges must record mulch learnings; clean Tier 1 merges are exempt (`agents/merger.md:18`, `agents/merger.md:52`).

### 8. Orchestrator — multi-repo layer above coordinators

The orchestrator distributes work across sub-repos (examples given: `mulch/`, `seeds/`, `canopy/`, `overstory/`) by starting per-repo coordinators, dispatching objectives, monitoring, and reporting completion (`agents/orchestrator.md:75`, `agents/orchestrator.md:81`, `agents/orchestrator.md:149`). It runs at the ecosystem root, not inside any sub-repo (`agents/orchestrator.md:46`, `agents/orchestrator.md:89`). Structural bans: never Write/Edit, never `ov sling`, never `ov merge`, never run tests/linters itself, one coordinator per sub-repo (`agents/orchestrator.md:38`, `agents/orchestrator.md:42`, `agents/orchestrator.md:47`). All cross-repo mail uses `--project <path>` targeting (`agents/orchestrator.md:121`, `agents/orchestrator.md:97`).

### 9. Monitor — continuous patrol (Tier 2)

The monitor is the watchdog's brain: Tier 0 (a mechanical daemon, meaning a background liveness checker) watches tmux/process liveness on a heartbeat, Tier 1 (ephemeral triage, meaning one-shot classification) classifies, and the monitor keeps continuous fleet awareness, nudges, and summarizes health (`agents/monitor.md:40`, `agents/monitor.md:42`). It patrols in a loop: `ov status --json` → mail → progressive nudging → periodic health summary → wait (`agents/monitor.md:89`). Polling faster than every 2 minutes is a named failure (`agents/monitor.md:18`, `agents/monitor.md:112`). Nudge stages are warning (log only), first nudge after 2 stale cycles, second with `--force` after 4, escalation to coordinator after 6, critical escalation after 8 (`agents/monitor.md:142`). Anomaly patterns watched: repeated stalls (3+), silent completions without `worker_done`, branch divergence (working state but no commits), resource hogging, cascade failures (`agents/monitor.md:180`). It must never spawn agents (`agents/monitor.md:21`, `agents/monitor.md:202`).

## Overlays — per-task instruction sheets

An overlay is the generated task file each agent reads at startup. The template states "DO NOT EDIT — Auto-generated by overstory" and that manual edits are overwritten on next spawn (`templates/overlay.md.tmpl:1`). The template path is resolved as `templates/overlay.md.tmpl` relative to the repo root (`src/agents/overlay.ts:11`).

Template sections and their placeholder variables (`templates/overlay.md.tmpl:10`, `templates/overlay.md.tmpl:26`, `templates/overlay.md.tmpl:35`, `templates/overlay.md.tmpl:45`, `templates/overlay.md.tmpl:53`, `templates/overlay.md.tmpl:77`):

```markdown
## Your Assignment
- **Agent Name:** {{AGENT_NAME}}
- **Task ID:** {{TASK_ID}}
- **Spec:** {{SPEC_PATH}}
- **Branch:** {{BRANCH_NAME}}
- **Worktree:** {{WORKTREE_PATH}}
- **Parent:** {{PARENT_AGENT}}
- **Depth:** {{DEPTH}}
## Working Directory
Your worktree root is: `{{WORKTREE_PATH}}`
## File Scope (exclusive ownership)
{{FILE_SCOPE}}
## Expertise
{{MULCH_DOMAINS}}
{{MULCH_EXPERTISE}}
## Communication
... ov mail check/send/reply examples ...
## Spawning Sub-Workers
{{CAN_SPAWN}}
{{QUALITY_GATES}}
{{CONSTRAINTS}}
```

Generation is pure placeholder replacement in `generateOverlay()` over ~20 keys including `AGENT_NAME`, `TASK_ID`, `FILE_SCOPE`, `MULCH_EXPERTISE`, `SKIP_SCOUT`, `DISPATCH_OVERRIDES`, `BASE_DEFINITION`, quality-gate variants, and tracker names (`src/agents/overlay.ts:274`, `src/agents/overlay.ts:299`, `src/agents/overlay.ts:326`).

Key formatting rules in code:

- File scope renders as a bullet list of backticked paths, or "No file scope restrictions" when empty (`src/agents/overlay.ts:20`).
- Scout and reviewer are the read-only capabilities: they get a lightweight Completion section (record learnings, close issue, send result, no commits or gates) while writable agents get numbered Quality Gates plus commit, record, `worker_done`, and close steps (`src/agents/overlay.ts:58`, `src/agents/overlay.ts:177`).
- Constraints differ the same way: read-only agents get "do NOT modify/create/delete"; writable agents get worktree isolation plus branch and scope limits (`src/agents/overlay.ts:221`).
- Spawn permission renders either "You may NOT spawn sub-workers." or an `ov sling` example at `depth + 1` (`src/agents/overlay.ts:250`).
- Lead-only dispatch overrides render SKIP REVIEW and MAX AGENTS directives when set (`src/agents/overlay.ts:80`).
- A `--skip-scout` flag injects a section telling the lead to skip Phase 1 and go straight to Build (`src/agents/overlay.ts:64`).

Safety guard: `writeOverlay()` writes to `{worktreePath}/.claude/CLAUDE.md` (creating `.claude/` as needed) but refuses when the worktree path equals the canonical project root, to avoid overwriting the operator's own session file; the check uses resolved-path comparison so it still works when dogfooding (running Overstory on its own repo where `.overstory/config.yaml` appears in every worktree) (`src/agents/overlay.ts:369`, `src/agents/overlay.ts:380`, `src/agents/overlay.ts:352`, `src/agents/overlay.ts:388`, `src/agents/overlay.ts:401`).

## Guards — tool-call enforcement

Guards are PreToolUse hooks (checks that run before a tool call and can block it) plus prompt/session hooks defined per agent. The shared constants module is pure data, no logic, and is the single source of truth for hook generation (`src/agents/guard-rules.ts:1`).

Blocked/dangerous sets (`src/agents/guard-rules.ts:13`, `src/agents/guard-rules.ts:31`, `src/agents/guard-rules.ts:34`, `src/agents/guard-rules.ts:40`):

```typescript
export const NATIVE_TEAM_TOOLS = [
  "Task", "TeamCreate", "TeamDelete", "SendMessage",
  "TaskCreate", "TaskUpdate", "TaskList", "TaskGet",
  "TaskOutput", "TaskStop",
];
export const INTERACTIVE_TOOLS = ["AskUserQuestion", "EnterPlanMode", "EnterWorktree"];
export const WRITE_TOOLS = ["Write", "Edit", "NotebookEdit"];
export const DANGEROUS_BASH_PATTERNS = [
  "sed\\s+-i", "echo\\s+.*>", "cat\\s+.*>", "tee\\s",
  "\\bmv\\s", "\\bcp\\s", "\\brm\\s", "\\bmkdir\\s", "\\btouch\\s",
  ">>", "\\bgit\\s+add\\b", "\\bgit\\s+commit\\b", "\\bgit\\s+merge\\b",
  "\\bgit\\s+push\\b", "\\bgit\\s+reset\\b", "\\bgit\\s+checkout\\b",
  "\\bgit\\s+rebase\\b", "\\bnpm\\s+install\\b", "\\bbun\\s+install\\b",
  "\\bbun\\s+-e\\b", "\\bnode\\s+-e\\b", "\\bpython3?\\s+-c\\b", ...
];
```

The eval-flag entries (`bun -e`, `node -e`, `python -c`, `perl -e`, `ruby -e`, `deno eval`) exist because direct language execution bypasses shell-pattern guards (`src/agents/guard-rules.ts:69`).

Allowlist checked before the blocklist (`src/agents/guard-rules.ts:85`):

```typescript
export const SAFE_BASH_PREFIXES = [
  "ov ", "overstory ", "bd ", "sd ",
  "git status", "git log", "git diff", "git show",
  "git blame", "git branch", "mulch ",
];
```

Deployed example (`.overstory/hooks.json`, SessionStart/UserPromptSubmit/PreToolUse/PostToolUse/Stop/PreCompact): session start primes expertise, prompt submit injects pending mail, PreToolUse on Bash blocks `git push` with a JSON block decision, every tool start/end is logged, and PreCompact re-primes before context compaction (`src/agents/guard-rules.ts:1`, `.overstory/hooks.json:9`, `.overstory/hooks.json:20`, `.overstory/hooks.json:31`, `.overstory/hooks.json:40`, `.overstory/hooks.json:51`, `.overstory/hooks.json:71`, `.overstory/hooks.json:86`).

```json
{
  "matcher": "Bash",
  "hooks": [
    { "type": "command", "command": "read -r INPUT; CMD=$(echo \"$INPUT\" | sed 's/.*\"command\": *\"\\([^\"]*\\)\".*/\\1/'); if echo \"$CMD\" | grep -qE '\\bgit\\s+push\\b'; then echo '{\"decision\":\"block\",\"reason\":\"git push is blocked by overstory — merge locally, push manually when ready\"}'; exit 0; fi;" }
  ]
}
```

Role markdown repeats the same bans in human language (no Write/Edit outside specs, no destructive git, no installs, no redirects) so both the model instructions and the machine hooks agree (`agents/supervisor.md:49`, `agents/scout.md:27`, `agents/builder.md:27`).

## Lifecycle — spawn, stop, checkpoint, handoff

Spawn goes through `ov sling` (coordinator spawns leads; leads spawn workers with `--parent` and `--depth`) or, for the multi-repo layer, `ov coordinator start --project <path>` (`agents/coordinator.md:146`, `agents/lead.md:101`, `agents/orchestrator.md:158`). Stop uses `ov stop` / `ov coordinator stop --project` (`agents/coordinator.md:109`, `agents/orchestrator.md:199`). Status and groups use `ov status`, `ov group status`, `ov worktree list/clean` (`agents/coordinator.md:221`, `agents/supervisor.md:204`).

Checkpoints let long-lived agents (agents that persist across batches, especially coordinator/lead/monitor) survive compaction (automatic context compression) or restart: coordinator checkpoints live at `.overstory/agents/coordinator/checkpoint.json` and other agents at `.overstory/agents/$OVERSTORY_AGENT_NAME/checkpoint.json` (`agents/coordinator.md:345`, `agents/supervisor.md:418`). Recovery is always the same pattern: read checkpoint → read overlay → check groups → check `ov status` → check mail → prime expertise → review open issues (`agents/supervisor.md:419`, `agents/monitor.md:209`).

File API (`src/agents/checkpoint.ts:6`, `src/agents/checkpoint.ts:14`, `src/agents/checkpoint.ts:48`, `src/agents/checkpoint.ts:86`):

- `saveCheckpoint(agentsDir, checkpoint)` writes `{agentsDir}/{agentName}/checkpoint.json`, creating the directory (`src/agents/checkpoint.ts:18`).
- `loadCheckpoint(agentsDir, agentName)` returns parsed JSON or null when absent (`src/agents/checkpoint.ts:52`).
- `clearCheckpoint(agentsDir, agentName)` deletes the file, silently ignoring missing-file (`ENOENT`, the system code for "no such file") errors (`src/agents/checkpoint.ts:90`).

Handoffs replace one session with another and append to `handoffs.json` (`src/agents/lifecycle.ts:7`):

- `initiateHandoff()` builds a checkpoint, saves it, appends a `{fromSessionId, toSessionId: null, checkpoint, reason, handoffAt}` record, and returns it (`src/agents/lifecycle.ts:72`, `src/agents/lifecycle.ts:98`).
- `resumeFromHandoff()` scans from the end for the most recent record with `toSessionId === null`, loads its checkpoint, and returns both, or null when none is pending (`src/agents/lifecycle.ts:120`, `src/agents/lifecycle.ts:128`).
- `completeHandoff()` sets that pending record's `toSessionId` to the new session and clears the checkpoint, throwing when no pending handoff exists (`src/agents/lifecycle.ts:157`, `src/agents/lifecycle.ts:169`, `src/agents/lifecycle.ts:182`).

## Identity — agent CVs

Each named agent keeps a small YAML CV at `{baseDir}/{name}/identity.yaml` (`src/agents/identity.ts:253`, `src/agents/identity.ts:288`). Creation writes the directory if needed and serializes with tab-indented `- item` lists for domains and `- taskId/summary/completedAt` objects for tasks (`src/agents/identity.ts:18`, `src/agents/identity.ts:253`). The custom parser handles top-level scalars, scalar arrays, object arrays, empty `[]`, quoted strings, and tab indentation (`src/agents/identity.ts:90`).

Example shape produced by the serializer (`src/agents/identity.ts:21`):

```yaml
name: auth-lead
capability: lead
created: 2026-02-14T03:19:38.077Z
sessionsCompleted: 4
expertiseDomains:
  - auth
  - sessions
recentTasks:
  - taskId: overstory-2zg1
    summary: Migrated session store
    completedAt: 2026-02-14T05:48:16.020Z
```

Updates are additive/merge-only: session count increments, domains merge with deduplication (removing duplicates), completed tasks append with a fresh timestamp and the list is capped at 20 entries by dropping the oldest (`src/agents/identity.ts:335`, `src/agents/identity.ts:351`, `src/agents/identity.ts:356`, `src/agents/identity.ts:365`, `src/agents/identity.ts:7`, `src/agents/identity.ts:373`). Updating a missing identity throws (`src/agents/identity.ts:344`).

## Manifest and groups

The manifest loader validates `agent-manifest.json` structurally before use: version must be a non-empty string, `agents` must be an object, each definition must have non-empty `file`/`model` strings, `tools`/`capabilities`/`constraints` arrays of strings, and boolean `canSpawn` (`src/agents/manifest.ts:145`, `src/agents/manifest.ts:176`, `src/agents/manifest.ts:62`). Referenced `.md` files must exist under the agent base directory, and the capability index is rebuilt from declarations (`src/agents/manifest.ts:205`, `src/agents/manifest.ts:219`). Query API is `getAgent(name)`, `findByCapability(cap)`, and `validate()` which rechecks definitions plus both directions of index consistency (`src/agents/manifest.ts:230`, `src/agents/manifest.ts:237`, `src/agents/manifest.ts:257`). Model choice resolves as config override → manifest default → fallback, with `sonnet/opus/haiku` aliases expanded via `ANTHROPIC_DEFAULT_*_MODEL` environment variables and gateway providers returning routing env vars (`src/agents/manifest.ts:348`, `src/agents/manifest.ts:48`, `src/agents/manifest.ts:311`).

The checked-in manifest declares version `1.0` with 7 agents — supervisor and orchestrator are absent because supervisor is deprecated and orchestrator lives outside the per-project manifest (`src/agents/manifest.ts:62`, `.overstory/agent-manifest.json:2`, `agents/supervisor.md:1`, `agents/orchestrator.md:89`):

| Agent | Model | Can spawn | Tools | Capabilities (`capabilityIndex`) |
|---|---|---|---|---|
| scout | haiku | no | Read, Glob, Grep, Bash | explore, research (` .overstory/agent-manifest.json:4`, `.overstory/agent-manifest.json:137`) |
| builder | sonnet | no | +Write, Edit | implement, refactor, fix (` .overstory/agent-manifest.json:22`, `.overstory/agent-manifest.json:144`) |
| reviewer | sonnet | no | Read, Glob, Grep, Bash | review, validate (` .overstory/agent-manifest.json:41`, `.overstory/agent-manifest.json:154`) |
| lead | opus | yes (+Task tool) | full + Write/Edit | coordinate, implement, review (` .overstory/agent-manifest.json:59`, `.overstory/agent-manifest.json:144`) |
| merger | sonnet | no | full + Write/Edit | merge, resolve-conflicts (` .overstory/agent-manifest.json:79`, `.overstory/agent-manifest.json:165`) |
| coordinator | opus | yes | Read, Glob, Grep, Bash (no Write) | coordinate, dispatch, escalate (` .overstory/agent-manifest.json:97`, `.overstory/agent-manifest.json:161`) |
| monitor | sonnet | no | Read, Glob, Grep, Bash | monitor, patrol (` .overstory/agent-manifest.json:117`, `.overstory/agent-manifest.json:177`) |

Read-only plus no-worktree constraints mark coordinator and monitor; scout and reviewer are read-only only (` .overstory/agent-manifest.json:112`, ` .overstory/agent-manifest.json:131`).

Groups track batches of tracker issues, not agents: each record has `id`, `name`, `memberIssueIds`, `status` (`active`/`completed`), and timestamps (` .overstory/groups.json:3`). Example: the first entry `phase1-session-migration` groups `overstory-2zg1` + `overstory-xhg8` as completed, while the last entry `bugfix-batch-2026-03-10` is still `active` with null `completedAt` (` .overstory/groups.json:2`, ` .overstory/groups.json:880`). Groups auto-close when every member issue reaches `closed`, which the coordinator treats as batch-done (`agents/coordinator.md:259`).

**Covers:** agents/coordinator.md, agents/supervisor.md, agents/scout.md, agents/builder.md, agents/reviewer.md, agents/merger.md, agents/orchestrator.md, agents/lead.md, agents/monitor.md, src/agents/overlay.ts, src/agents/guard-rules.ts, src/agents/lifecycle.ts, src/agents/manifest.ts, src/agents/identity.ts, src/agents/checkpoint.ts, templates/overlay.md.tmpl, .overstory/agent-manifest.json, .overstory/groups.json, .overstory/hooks.json
