> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Safety, Workflow Abstraction, and Extensibility

**In one sentence:** GasTown isolates workers with file locks plus git worktrees, encodes repeatable work as versioned TOML formulas, and extends itself through Deacon-dispatched `plugin.md` patrol plugins — with merging done by git in the Refinery, not by any file-level merge logic.

## Key points
- Agent identity locking is a JSON lockfile at `<worker>/.runtime/agent.lock` serialized by an adjacent `flock()` sidecar, with stale locks reaped only when the PID is dead *and* the tmux session is gone (`internal/lock/lock.go:54`, `internal/lock/lock.go:73`, `internal/lock/lock.go:264`).
- Formula *is* a workflow abstraction: four TOML types (convoy, workflow, expansion, aspect) with validation, cycle detection, topological sort, and ready-step queries, embedded in the binary and provisioned to `.beads/formulas/` (`internal/formula/types.go:16`, `internal/formula/parser.go:275`, `internal/formula/embed.go:16`).
- Formula resolution is three-tier — rig overrides town overrides embedded — with checksummed safe-update that never overwrites user edits (`internal/formula/embed.go:47`, `internal/formula/embed.go:308`).
- A plugin is a directory with `plugin.md` (`+++` TOML frontmatter + markdown) plus an optional `run.sh`; discovery is town-first then rig-override, execution is agent, script, or exec-wrapper, and dispatch goes through dogs during Deacon patrol (`internal/plugin/scanner.go:26`, `internal/plugin/types.go:112`).
- Deacon is a long-running Claude patrol agent (heartbeat-guarded); Refinery is the merge-queue Engineer with GitHub and Bitbucket PR providers behind one interface (`internal/deacon/heartbeat.go:1`, `internal/refinery/pr_provider.go:5`).
- Refinery merges with `MergeNoFF` locally or the VCS merge API when `merge_strategy="pr"`, serializes default-branch pushes through a merge slot, and sends conflicts back to the worker — there is no operational-transform or shared-file three-way merge in code (`internal/refinery/engineer.go:653`, `internal/refinery/engineer.go:1030`, `internal/git/git.go:1481`).
- Doctor runs 100+ registered checks (workspace, rig, binaries, git, hooks, patrol, beads, tmux, Dolt) with `--fix` support; `internal/health` holds the reusable TCP/SQL/zombie/backup probes shared with `gt health` (`internal/doctor/workspace_check.go:384`, `internal/health/health.go:25`).
- Gas City is a design-only declarative role/capability layer (one doc, no runtime package); Wasteland is DoltHub-based federation of towns, currently in unenforced "wild-west" Phase 1 (`docs/gas-city/crew-specialization-design.md:19`, `docs/WASTELAND.md:16`).

---
## File locking (flock)

Flock usage is confined to `internal/lock`. Each worker directory owns a JSON lockfile (`internal/lock/lock.go:54`):

```go
lockPath: filepath.Join(workerDir, ".runtime", "agent.lock"),
```

`LockInfo` records PID, timestamp, tmux session, and hostname (`internal/lock/lock.go:31`). `Acquire()` serializes concurrent claimants with an OS advisory lock on a *sidecar* file, not the lockfile itself (`internal/lock/lock.go:71`):

```go
unlock, err := flockAcquire(l.lockPath + ".flock")
```

The Unix implementation is `syscall.Flock` with `LOCK_EX` (`internal/lock/flock_unix.go:22`):

```go
f, err := os.OpenFile(path, os.O_CREATE|os.O_RDWR, 0644)
if err := syscall.Flock(int(f.Fd()), syscall.LOCK_EX); err != nil {
```

A non-blocking variant exists for try-lock callers (`internal/lock/flock_unix.go:44`): `FlockTryAcquire` uses `LOCK_EX|LOCK_NB` and returns `(nil, false, nil)` on `EWOULDBLOCK`. Windows has mirrored files (`internal/lock/flock_windows.go:1`, `internal/lock/process_windows.go:1`; Unix liveness via `internal/lock/process_unix.go:1`).

Writes are crash-safe: temp file plus atomic rename (`internal/lock/lock.go:207`):

```go
tmpPath := l.lockPath + ".tmp"
os.WriteFile(tmpPath, data, 0644)
os.Rename(tmpPath, l.lockPath)
```

Staleness is PID-liveness (`internal/lock/lock.go:39`). But bulk cleanup is stricter — a lock is reaped only when the PID is dead *and* no tmux session matches, because the spawner normally exits while Claude keeps running inside tmux (`internal/lock/lock.go:259`):

```go
// A lock is only truly stale if BOTH the PID is dead AND the tmux session
// doesn't exist.
```

`CleanStaleLocks` queries the town tmux socket (`internal/lock/lock.go:296`) and skips locks whose session still exists. `DetectCollisions` reports stale and orphaned locks by comparing lockfiles against active sessions (`internal/lock/lock.go:398`).

## Formula: the workflow abstraction

Verdict: **yes, formula is the workflow abstraction** — a TOML definition language plus planning library (parse, validate, sort, ready-steps), executed by agents rather than by its own runner.

Four types (`internal/formula/types.go:16`): `convoy` (parallel legs plus synthesis), `workflow` (sequential steps with `needs`), `expansion` (template-generated steps), `aspect` (parallel analysis). The `Formula` struct carries per-type fields plus cross-cutting `pour`, `agent`, `review_only`, `extends`/`compose` inheritance (`internal/formula/types.go:28`). Steps add `target`, `parallel`, `interactive`, and `acceptance` for Ralph-loop mode (`internal/formula/types.go:121`).

Planning API (`internal/formula/parser.go:23`, `internal/formula/parser.go:275`, `internal/formula/parser.go:365`): `Parse`/`ParseFile`, `Validate` (required fields, unique IDs, known refs), DFS cycle detection (`internal/formula/parser.go:213`), Kahn topological sort, `ReadySteps(completed)` / `ParallelReadySteps`, and `GetStep`/`GetLeg`/`GetTemplate`/`GetAspect` lookups. Overlays patch descriptions per rig or town with `replace`/`append`/`skip` modes, rig winning outright (`internal/formula/overlay.go:8`, `internal/formula/overlay.go:31`).

Embedded distribution (`internal/formula/embed.go:16`):

```go
//go:embed formulas/*.formula.toml
var formulasFS embed.FS
```

About 45 formulas ship in `internal/formula/formulas/`, including `mol-polecat-work`, `gastown-release`, `security-audit`, `rule-of-five`, `shiny`, `tdd-cycle`, and `towers-of-hanoi*`. Resolution is rig > town > embedded (`internal/formula/embed.go:47`): `<town>/<rig>/.beads/formulas/`, then `<town>/.beads/formulas/`, then the binary (full design in `docs/design/formula-resolution.md:24`). `ProvisionFormulas` copies embedded files into `.beads/formulas/` without overwriting, tracking SHA-256 in `.installed.json` (`internal/formula/embed.go:173`); `CheckFormulaHealth` reports ok/outdated/modified/missing/new/untracked and `UpdateFormulas` only refreshes safe entries (`internal/formula/embed.go:235`, `internal/formula/embed.go:308`).

Example — release workflow (`internal/formula/formulas/gastown-release.formula.toml:29`):

```toml
formula = "gastown-release"
type = "workflow"
version = 1

[vars.version]
description = "The semantic version to release (e.g., 0.3.0)"
required = true

[[steps]]
id = "preflight-workspaces"
title = "Preflight workspace checks"
```

The polecat lifecycle formula is the canonical long example: self-cleaning contract (`gt done` = push, submit to merge queue, nuke sandbox), load-bearing branch names `polecat/<name>/<bead>+<suffix>`, mandatory rebase plus pre-verified gate run so the Refinery can fast-path the merge (`internal/formula/formulas/mol-polecat-work.formula.toml:1`). Note: `security-audit.formula.toml` uses `[[advice]]`/`[[pointcuts]]` keys with no matching fields on the `Aspect` struct, evidence the format has experimental extensions beyond `internal/formula/types.go:79`.

## Deacon and Refinery

Deacon is agent infrastructure, not a scheduler library: "a Claude agent that monitors Mayor and Witnesses, handles lifecycle requests, and keeps Gas Town running" (`internal/deacon/heartbeat.go:1`). The Go side manages its tmux session lifecycle (`internal/deacon/manager.go:44`), seeds patrol with "I am Deacon. Start patrol…" (`internal/deacon/manager.go:137`), and tracks liveness through `deacon/heartbeat.json` with 5-minute stale and 20-minute very-stale thresholds (`internal/deacon/heartbeat.go:16`, `internal/deacon/heartbeat.go:51`). Supporting files handle stuck agents, redispatch, pause, stale hooks, and stranded feed items (`internal/deacon/stuck.go:1`, `internal/deacon/redispatch.go:1`, `internal/deacon/pause.go:1`, `internal/deacon/stale_hooks.go:1`, `internal/deacon/feed_stranded.go:1`).

Refinery is the merge-queue Engineer (`internal/refinery/types.go:1`). `MergeRequest` tracks branch, worker, issue, target branch, commit SHA, and optional PR identity (`internal/refinery/types.go:13`); status is `open`/`in_progress`/`closed` with validated transitions, extended by a `ready → claimed → preparing → prepared → merging → merged` phase machine (`internal/refinery/types.go:59`, `internal/refinery/types.go:77`). PR operations are vendor-neutral (`internal/refinery/pr_provider.go:5`):

```go
type PRProvider interface {
    FindPullRequest(branch, prURL string, prNumber int, headSHA string) (*git.PullRequestInfo, error)
    IsPRApproved(pr *git.PullRequestInfo) (bool, error)
    MergePR(pr *git.PullRequestInfo, method string) (string, error)
}
```

Concrete providers use the `gh` CLI for GitHub and the Bitbucket Cloud REST API (workspace plus repo slug parsed from the origin remote) (`internal/refinery/pr_provider_github.go:8`, `internal/refinery/pr_provider_bitbucket.go:8`). Quality gates run pre-merge or post-squash, failures reset the merge (`internal/refinery/engineer.go:58`); conflict policy is `assign_back` or `auto_rebase` (`internal/refinery/engineer.go:107`); a durable `safety_stop:*` bead label blocks startup until an operator clears it (`internal/refinery/safety_stop.go:11`).

## Merge strategy: what the code actually shows

There is **worktree-per-agent isolation plus git merging — no shared-file merge logic**. Rigs are created with a bare `.repo.git` plus per-role worktrees; rig setup explicitly creates "refinery as worktree from bare repo on default branch" (`internal/rig/manager.go:746`). Polecats work on fresh per-bead branches and must never push to main — the formula contract states "You do NOT: push directly to main (Refinery merges from MQ)" (`internal/formula/formulas/mol-polecat-work.formula.toml:31`).

The Engineer path (`internal/refinery/engineer.go:504` `doMerge`): verify the submitted branch head, checkout target, `Pull("origin", target)`, `CheckConflicts`, push submodule commits first, run gates, then either delegate to the PR provider (`internal/refinery/engineer.go:636` when `MergeStrategy == "pr"`, via `internal/refinery/engineer.go:775` `doMergePR`) or land locally with `MergeNoFF` preserving the polecat commit message (`internal/refinery/engineer.go:653`, `internal/git/git.go:1481`), run post-squash gates, then push through the serialized main push slot (`internal/refinery/engineer.go:1030`). Conflicts return a conflict result and spawn a rework task (`internal/refinery/engineer.go:1769`); failure labels map to `needs-rebase` / `needs-fix` / `needs-retry` (`internal/refinery/types.go:292`). Git helpers expose `Merge`, `MergeNoFF`, `MergeFFOnly`, `MergeSquash`, `GhPrMerge`, `BitbucketPRMerge`, `AbortMerge` (`internal/git/git.go:1475`, `internal/git/git.go:1481`, `internal/git/git.go:1489`, `internal/git/git.go:1494`, `internal/git/git.go:1596`, `internal/git/git.go:1736`, `internal/git/git.go:1865`). A mutation guard blocks dangerous town-root operations (`internal/git/git.go:218` `guardUnsafeTownRootMutation`, `internal/git/git.go:266` `EnsureSafeMutationWorkDir`).

## Plugin system and how to add one

Anatomy: `plugin.md` with `+++` TOML frontmatter (name, description, version, gate, tracking, execution) followed by markdown instructions, plus an optional `run.sh` that switches execution from agent-interpreted to script (`internal/plugin/types.go:17`, `internal/plugin/scanner.go:138`, `internal/plugin/scanner.go:147`). Gates are `cooldown` (duration), `cron` (schedule), `condition` (check command), `event` (on), or `manual` (`internal/plugin/types.go:83`); execution is `agent`, `script`, or `exec-wrapper` session-startup wrapping (`internal/plugin/types.go:112`). Each run is recorded as a wisp receipt via `gt plugin record-run`, which gates query instead of state files (`docs/design/plugin-system.md:94`). Invocation formats the dog mail body, ending in `gt dog done` (`internal/plugin/types.go:213`).

All 13 repo plugins live as siblings with `plugin.md`: `compactor-dog`, `dolt-archive`, `dolt-backup`, `dolt-log-rotate`, `dolt-snapshots`, `git-hygiene`, `github-sheriff`, `gitignore-reconcile`, `quality-review`, `rebuild-gt`, `stuck-agent-dog`, `submodule-commit`, `tool-updater` (`plugins/compactor-dog/plugin.md:1`, `plugins/github-sheriff/plugin.md:1`, `plugins/quality-review/plugin.md:1`). Examples: compactor-dog polls Dolt commit growth on a 30-minute cooldown with judgment-based escalation (`plugins/compactor-dog/plugin.md:6`); github-sheriff polls `gh pr list` GraphQL output on a 2-hour cooldown and files `ci-failure` beads (`plugins/github-sheriff/plugin.md:6`).

To add one:

1. Create `<town>/plugins/<name>/plugin.md` for universal or `<town>/<rig>/plugins/<name>/plugin.md` for project-scoped behavior (rig overrides town on name clash; `internal/plugin/scanner.go:29`).
2. Write frontmatter between `+++` lines plus markdown steps; add executable `run.sh` beside it for script mode.
3. Check discovery with `gt plugin list` and `gt plugin show <name>`, trigger manually with `gt plugin run <name>`, sync into runtime dirs with `gt plugin sync` (drift via `DetectDrift`), and record receipts with `gt plugin record-run --plugin <name> --result <outcome>` (`internal/cmd/plugin.go:65`, `internal/plugin/sync.go:23`, `internal/plugin/sync.go:274`).

## Doctor, health, and remaining ops primitives

Doctor is a registry plus streaming runner with panic-safe `--fix` (`internal/doctor/doctor.go:12`, `internal/doctor/doctor.go:52`, `internal/doctor/doctor.go:110`). Workspace checks cover town config, rigs registry, and Mayor existence (`internal/doctor/workspace_check.go:384`); per-rig checks cover git repo state, hooks path, bare repo plus refspec, default branch, witness/refinery/mayor clones, polecat clones, beads config and symlinks (`internal/doctor/rig_check.go:2051`). The CLI registers roughly one hundred checks spanning binaries (bd, dolt, Claude, Groq), town git and branch, remotes, hooks sync, tmux sessions and sockets, daemons, disk, patrol molecules and plugin drift, beads and agent beads, Dolt metadata, sparse checkout, worktree gitdirs, zombies, orphans, and stalled polecats (`internal/cmd/doctor.go:187`, `internal/doctor/formula_check.go:1`, `internal/doctor/overlay_health_check.go:1`, `internal/doctor/hooks_sync_check.go:1`).

`internal/health` is the shared probe library used by both the Doctor Dog and `gt health` (`internal/health/health.go:1`): TCP dial (`internal/health/health.go:25`), Dolt `SELECT 1` latency (`internal/health/health.go:36`), database census (`internal/health/health.go:56`), lsof-based zombie-server scan (`internal/health/health.go:96`), backup freshness by newest file (`internal/health/health.go:122`), JSONL archive freshness by latest git commit (`internal/health/health.go:140`), and recursive directory size (`internal/health/health.go:166`).

Supporting primitives: OpenTelemetry recording of `bd` calls, session start/stop, prompt sends, and agent instantiation (`internal/telemetry/telemetry.go:92`, `internal/telemetry/recorder.go:296`); fuzzy "did you mean" matching with prefix/contain/Levenshtein scoring (`internal/suggest/suggest.go:10`, `internal/suggest/suggest.go:54`); Key Record Chronicle TTL pruning of Level-0 ephemeral events — 7-day default, 1-day patrol events, 30–90-day deaths (`internal/krc/krc.go:30`, `internal/krc/krc.go:50`); shell hook install/remove in rc files (`internal/shell/integration.go:25`); Wasteland trust tiers and escalation evaluation over Dolt queries (`internal/wasteland/trust.go:29`, `internal/wasteland/trust.go:147`).

## Git safety rails

`internal/git` wraps every mutation in a town-root guard. `guardUnsafeTownRootMutation` rejects bare `checkout/merge/rebase/pull/reset/clean/rm/mv/cherry-pick/revert/am/apply` and sensitive `worktree/branch/symbolic-ref/stash/submodule` forms when the effective workdir resolves to the town root (`internal/git/git.go:218`, `internal/git/git.go:328`, `internal/git/git.go:438`). `EnsureSafeMutationWorkDir` fails when a caller passes a directory whose git top-level is the town root (`internal/git/git.go:266`). Clone helpers standardize shared-repo setup: bare and partial clones, branch-scoped clones, reference clones, refspec configuration so worktrees see `origin/*`, and hooks-path wiring (`internal/git/git.go:690`, `internal/git/git.go:789`, `internal/git/git.go:775`). Status parsing explicitly filters `skip-worktree` sparse-checkout deletions so polecat sparse worktrees do not read as dirty (`internal/git/git.go:1219`, `internal/git/git.go:1305`).

## Refinery runtime and Deacon patrol in more depth

The Engineer loads per-rig merge-queue config (enabled flag, `on_conflict`, test command, gates, `merge_strategy`, VCS provider) and selects the PR provider at startup (`internal/refinery/engineer.go:183`, `internal/refinery/engineer.go:319`, `internal/refinery/engineer.go:461`). Claim handling uses a 30-minute default stale-claim timeout before an MR becomes re-claimable (`internal/refinery/engineer.go:37`). Queue listing separates ready, blocked, and anomalous MRs for the TUI and CLI (`internal/refinery/engineer.go:2073`, `internal/refinery/engineer.go:2144`, `internal/refinery/engineer.go:2234`). Post-merge it runs a convoy check and closes superseded conflict artifacts so a landed MR retires its rework tasks (`internal/refinery/engineer.go:1909`, `internal/refinery/engineer.go:2346`).

Deacon patrol is formula-driven: the seeded prompt tells the agent to run `gt deacon heartbeat`, then check hooks, then sling `mol-deacon-patrol` and execute the created hook (`internal/deacon/manager.go:137`). Heartbeat read/write helpers back the daemon poke-or-restart decision (`internal/deacon/heartbeat.go:51`). Pause support freezes all patrol actions while set (`internal/deacon/pause.go:1`); redispatch, stuck detection, stale-hook reaping, and stranded-feed recovery keep patrol moving without operator input (`internal/deacon/redispatch.go:1`, `internal/deacon/stuck.go:1`, `internal/deacon/stale_hooks.go:1`, `internal/deacon/feed_stranded.go:1`).

## Templates, scripts, and telemetry details

`templates/` holds agent model presets (`templates/agents/opencode.json.tmpl:1`, `templates/agents/opencode-models.json:1`) plus `polecat-CLAUDE.md` and `witness-CLAUDE.md` role prompts (`templates/polecat-CLAUDE.md:1`, `templates/witness-CLAUDE.md:1`). `scripts/` holds rig bootstrap (`scripts/bootstrap-local-rig.sh:1`), version bumping, install-path tests, migration launchers and harnesses, proxy smoke/manual tests, hardener and flake updaters, and a `guards/` plus `lib/` helper set. Telemetry initializes an OTel provider per service with content limits and run-ID propagation (`internal/telemetry/telemetry.go:112`, `internal/telemetry/recorder.go:25`), emitting structured records for subprocess output with truncation (`internal/telemetry/recorder.go:276`). KRC auto-prunes on daemon startup and on an hourly interval while keeping a minimum retained count for debugging (`internal/krc/krc.go:50`). Shell integration detects the login shell, resolves the rc file, and inserts or removes the hook source line idempotently (`internal/shell/integration.go:56`, `internal/shell/integration.go:67`, `internal/shell/integration.go:87`).

## Gas City and Wasteland

Gas City is not a runtime package: `docs/gas-city/` contains only `crew-specialization-design.md`, which frames Gas City as the planned declarative role format (`w-gc-001`, `w-gc-002`) and capability-based dispatch layer where tasks declare requirements, agents advertise capabilities, and delegation replaces cognition (`docs/gas-city/crew-specialization-design.md:19`, `docs/gas-city/crew-specialization-design.md:310`).

Wasteland federates towns through DoltHub: each rig holds a sovereign fork of a shared commons database, registers in the `rigs` table, and exchanges wanted items plus completions through fork/PR/merge primitives (`internal/wasteland/wasteland.go:1`). Config lives at `mayor/wasteland.json` with upstream, fork org/db, local dir, and rig handle (`internal/wasteland/wasteland.go:30`, `internal/wasteland/wasteland.go:50`); CLI surface is `gt wl join/browse/claim/done/post/sync` (`docs/WASTELAND.md:22`). Current status is explicitly Phase 1 wild-west with no trust enforcement (`docs/WASTELAND.md:16`); the trust-tier scaffolding exists but is not yet gating (`internal/wasteland/trust.go:60`). Repo extras in scope: `templates/` (agent JSON templates plus polecat/witness prompts), `scripts/` (bootstrap, migration, proxy, install, and guard helpers), and the enterprise-rationale essays (`docs/why-these-features.md:1`).

**Covers:** internal/lock, internal/git, internal/formula (+formulas, docs/design/formula-resolution.md), internal/deacon, internal/refinery, internal/plugin (+plugins, docs/design/plugin-system.md, templates, scripts), internal/doctor, internal/health, internal/telemetry, internal/suggest, internal/krc, internal/wasteland (+docs/WASTELAND.md), internal/shell, docs/gas-city, docs/why-these-features.md
