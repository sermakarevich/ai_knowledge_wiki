> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Worktrees, Hooks, and Crash-Recovery Persistence

**In one sentence:** GasTown agents live in `git worktree` checkouts whose creation and deletion are serialized with per-polecat `flock` locks, while crash recovery is lazy and file-based: a `.polecat-checkpoint.json` snapshot plus surviving git state is re-displayed by the next session's startup hook, and shared settings files are protected against concurrent-writer corruption with atomic temp-plus-rename writes.

## Key points
- "Hook" has three distinct meanings that must not be conflated: README-level Hook as git-worktree-backed persistent storage (`README.md:68`), beads-level Hook as an agent's pinned work-queue bead (`docs/glossary.md:69`), and code-level lifecycle hooks as Claude `settings.json` event commands (`internal/hooks/config.go:24`).
- Polecat worktree creation is `git worktree add -b <branch> <polecats/<name>/<rig>> <startPoint>` from the rig's repo base, executed under a pool lock plus a per-polecat `flock`, with full rollback (worktree removal, directory removal, name-pool release) on any failure (`internal/polecat/manager.go:662`, `internal/polecat/manager.go:725`, `internal/git/git.go:2281`).
- Worktree destruction is `git worktree remove [--force]` through the repo base, gated by uncommitted-work checks, pending merge-request blockers, shell-safety checks, and a best-effort push of unpushed commits — falling back to `os.RemoveAll` plus `worktree prune` only when the repo base is unusable (`internal/polecat/manager.go:1126`, `internal/polecat/manager.go:1231`, `internal/git/git.go:2409`).
- Crash state is a single JSON file, `<worktree>/.polecat-checkpoint.json`, capturing molecule, step, hooked bead, modified files, branch, last commit, timestamp, and session ID; it is written with plain `os.WriteFile` (mode `0600`), not with the atomic-write helper, so a crash mid-write can leave a corrupt file that `Read` reports as a parse error (`internal/checkpoint/checkpoint.go:20`, `internal/checkpoint/checkpoint.go:82`).
- Nobody detects crashes eagerly: the successor session's startup path (`gt prime --hook`) calls `checkpoint.Read` and treats a non-stale (<24h) checkpoint as `crash-recovery` state, then prints it as context — nothing is automatically re-applied, so committed history and on-disk files survive while in-memory reasoning is lost (`internal/cmd/prime_session.go:298`, `internal/cmd/prime_output.go:770`).
- `WIP: checkpoint (auto)` commits are the durable companion to the JSON snapshot: `CountWIPCommits`/`SquashWIPCommits` count or collapse them over `merge-base..HEAD` with a soft reset into one commit, preserving non-WIP subjects (`internal/checkpoint/squash.go:12`, `internal/checkpoint/squash.go:47`).
- Shared agent settings are crash-safe against concurrent spawns via `atomicfile.WriteFile` (unique temp file plus `rename`, gh#3500), used by both the Claude merge path and the template path — but the checkpoint writer does not use it (`internal/atomicfile/atomicfile.go:56`, `internal/hooks/config.go:266`, `internal/hooks/installer.go:146`).
- There is no lock inside the git wrapper itself: exclusion comes from polecat/pool `flock` files under `<rig>/.runtime/locks/`, plus a town-root mutation guard that refuses worktree-mutating git commands resolving to the town root (`internal/polecat/manager.go:218`, `internal/git/git.go:218`).
---
## 1. What "Hook" means here (three layers)

The task wording "Hook (git-worktree-backed storage)" matches the README, not the `internal/hooks` package. All three senses appear in scope:

- Worktree Hook: "Git worktree-based persistent storage for agent work. Survives crashes and restarts." (`README.md:68`); "Each hook is a git worktree with: persistent state, version control, rollback, multi-agent coordination" (`README.md:722`); role table maps Hook to persistent storage via git worktree (`README.md:777`).
- Beads Hook: "A special pinned Bead for each agent. The Hook is an agent's primary work queue" (`docs/glossary.md:69`); slinging puts work "on their Hook" (`docs/glossary.md:77`). The checkpoint records this as `HookedBead` (`internal/checkpoint/checkpoint.go:42`).
- Lifecycle hook: an individual `{type: command, command: ...}` entry inside a matcher group such as `SessionStart` or `PreToolUse` (`internal/hooks/config.go:24`), managed by base-plus-override merging and installed as `settings.json` or agent plugins (`docs/HOOKS.md:7`).

The rest of this page keeps these labels explicit: worktree-Hook, bead-Hook, lifecycle-hook.

**Covers:** `README.md:20`, `README.md:68`, `README.md:720`, `docs/glossary.md:69`, `internal/hooks/config.go:18`

## 2. Worktree creation (polecat spawn path)

On-disk layout for a polecat named `fury` in rig `gastown`:

```
<town>/gastown/
  .repo.git/                    # bare shared object database
  mayor/rig/                    # reference clone (submodule reference source)
  polecats/fury/gastown/        # the worktree-Hook (clonePath = polecatDir + rig name)
  polecats/.claude/settings.json# shared lifecycle-hook settings for all polecats
  .runtime/locks/polecat-fury.lock
  .runtime/locks/polecat-pool.lock
```

The clone path construction is `clonePath := filepath.Join(polecatDir, m.rig.Name)` (`internal/polecat/manager.go:733`). Allocation serializes name choice across processes:

```go
// Hold pool lock across allocation + directory creation to close the
// race window where a concurrent AllocateName could miss the pending
// marker and reallocate the same name.
poolLock, err := m.lockPool()
```

(`internal/polecat/manager.go:662`). `AllocateAndAdd` then takes the per-polecat lock while still holding the pool lock, creates the polecat directory, kills any lingering tmux session for the name, releases the pool lock, and continues under the polecat lock only (`internal/polecat/manager.go:684`, `internal/polecat/manager.go:692`, `internal/polecat/manager.go:715`).

The expensive half runs in `addWithOptionsLocked`: disk-space pre-check, `repoBase()` lookup, `Fetch("origin")` (warning-only on failure), then either resume-branch attach or fresh-branch creation (`internal/polecat/manager.go:725`, `internal/polecat/manager.go:757`, `internal/polecat/manager.go:767`):

- Resume: `FetchBranch("origin", resumeBranch)` then `WorktreeAddExistingForce(clonePath, resumeBranch)`, which tolerates the branch being checked out in another worktree (`internal/polecat/manager.go:771`, `internal/git/git.go:2317`).
- Fresh: verify `origin/<default>` exists, then `WorktreeAddFromRef(clonePath, branchName, startPoint)` with `GIT_LFS_SKIP_SMUDGE=1` and submodule init (`internal/polecat/manager.go:791`, `internal/git/git.go:2281`).

All four `WorktreeAdd*` variants call `InitSubmodules(path, g.submoduleReferencePath())`, where the reference resolves to the sibling `mayor/rig` directory when it has tracked `.gitmodules` and is not shallow (`internal/git/git.go:2266`, `internal/git/git.go:2324`).

Post-worktree provisioning order is fixed: `CLAUDE.md`, shared beads, `PRIME.md` (warning-only), rig overlay files, local git excludes, agent runtime settings, rig setup-hook scripts, rig setup command, and finally the agent bead with `HookBead` set atomically at creation (`internal/polecat/manager.go:812`, `internal/polecat/manager.go:836`, `internal/polecat/manager.go:850`). Any error triggers `cleanupOnError`: reset the agent bead, `WorktreeRemove(clonePath, true)`, `os.RemoveAll(polecatDir)`, release the name, save the pool (`internal/polecat/manager.go:741`).

Cross-rig crew worktrees follow a simpler variant: `gt worktree <rig>` creates `<target-rig>/crew/<source-rig>-<name>/` via `WorktreeAddExistingForce(worktreePath, "main")` after `Fetch("origin")`, then sets per-worktree `user.name` identity and pulls `origin/main` (`internal/cmd/worktree.go:121`, `internal/cmd/worktree.go:157`, `internal/cmd/worktree.go:162`).

**Covers:** `internal/polecat/manager.go:660`, `internal/git/git.go:2263`, `internal/cmd/worktree.go:97`

## 3. Worktree destruction

`Remove` delegates to `RemoveWithOptions(name, force, nuclear, selfNuke)`; the latter takes the per-polecat lock first and defers unlock (`internal/polecat/manager.go:1115`, `internal/polecat/manager.go:1126`). The locked body runs these gates in order (`internal/polecat/manager.go:1138`):

1. Existence check returns `ErrPolecatNotFound` for unknown names.
2. Uncommitted-work gate (skipped only in nuclear mode): prefer the agent bead's self-reported `cleanup_status`; fall back to `CheckUncommittedWork()` on the clone path. Non-force mode fails on any dirt; force mode still blocks on stashes, which represent intentional work in progress (`internal/polecat/manager.go:1148`).
3. Merge-request gate: unless `--force`, a pending refinery merge request blocks removal (`internal/polecat/manager.go:1180`).
4. Agent-bead reset and work-bead unassignment happen before filesystem mutation, so a concurrent sling sees a clean bead rather than having its `hook_bead` cleared mid-creation (`internal/polecat/manager.go:1186`, `internal/polecat/manager.go:1201`).
5. Shell-safety gate refuses removal when the caller's cwd is inside the worktree, unless `selfNuke` (the `gt done` self-delete path) is set (`internal/polecat/manager.go:1211`).
6. Best-effort push: if the polecat branch has unpushed commits, push to `origin` before removal; failures are warnings, not errors (`internal/polecat/manager.go:1231`).
7. Removal proper: `repoGit.WorktreeRemove(clonePath, force)`; on failure fall back to `os.RemoveAll(clonePath)` for old-style clones; if the repo base itself is missing, prune both `.repo.git` and `mayor/rig` entries and `os.RemoveAll(polecatDir)` (`internal/polecat/manager.go:1249`, `internal/polecat/manager.go:1268`, `internal/git/git.go:2408`).

Crew worktree removal mirrors this at smaller scale: refuse dirty worktrees without `--force`, then run `git worktree remove [--force] <path>` with cwd set to the target rig's `mayor/rig`, then close (default) or delete (`--purge`) the crew agent bead and unassign its beads (`internal/cmd/crew_lifecycle.go:78`, `internal/cmd/worktree.go:296`).

**Covers:** `internal/polecat/manager.go:1115`, `internal/cmd/crew_lifecycle.go:60`, `internal/git/git.go:2408`

## 4. Worktree integrity validation and repair

`internal/worktree` contains only validation, not creation. `Validate` walks upward to the nearest `.git` marker bounded by the town root; a `.git` directory must contain `HEAD`, while a `.git` file must read `gitdir: <path>` and resolve to an existing directory that itself contains `HEAD` — anything else is `ErrIntegrityViolation` and command paths fail closed (`internal/worktree/integrity.go:30`, `internal/worktree/integrity.go:50`, `internal/worktree/integrity.go:89`). Missing markers are violations only when `Require` is set, which is the mode for polecat, crew, refinery, and witness roles (`internal/worktree/integrity.go:15`).

Repair lives in the doctor check: `fixOneWorktree` deletes the broken `.git` file, runs `git worktree prune`, resolves the default branch via `symbolic-ref HEAD`, retries `git worktree add --force`, and — when the directory already has content (e.g. deacon dogs after rsync) — manually registers the worktree by writing `.repo.git/worktrees/<name>/{gitdir,commondir,HEAD}` plus the worktree's own `.git` pointer file (`internal/doctor/worktree_gitdir_check.go:342`, `internal/doctor/worktree_gitdir_check.go:379`).

**Covers:** `internal/worktree/integrity.go:1`, `internal/doctor/worktree_gitdir_check.go:341`

## 5. Checkpoint mechanism (what is persisted, where)

The checkpoint file is `<polecat-or-crew-worktree>/.polecat-checkpoint.json`, from `Path(polecatDir)` joining the directory with `Filename` (`internal/checkpoint/checkpoint.go:20`, `internal/checkpoint/checkpoint.go:56`). The struct persisted is:

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

(`internal/checkpoint/checkpoint.go:23`). `Capture` fills only the git-observable half: `git status --porcelain` filenames, `rev-parse HEAD`, and `rev-parse --abbrev-ref HEAD` (`internal/checkpoint/checkpoint.go:119`). The `gt checkpoint write` command layers on molecule context (parsed from `instantiated_from:` lines in assigned in-progress beads), the hooked bead (first `hooked`-status bead for the agent identity), and optional `--notes`, then calls `checkpoint.Write(cwd, cp)` (`internal/cmd/checkpoint_cmd.go:83`, `internal/cmd/checkpoint_cmd.go:119`, `internal/cmd/checkpoint_cmd.go:264`). `SessionID` comes from the runtime environment with a `pid-<n>` fallback, and `Timestamp` defaults to now (`internal/checkpoint/checkpoint.go:84`).

`Write` marshals indented JSON and calls `os.WriteFile(path, data, 0600)` — direct, non-atomic, no temp file (`internal/checkpoint/checkpoint.go:96`). `Read` returns `(nil, nil)` when absent and a parse error when corrupt (`internal/checkpoint/checkpoint.go:62`). `Remove` deletes the file, ignoring not-exist (`internal/checkpoint/checkpoint.go:110`). Freshness helpers are `Age()` (`time.Since`) and `IsStale(threshold)` (`Age() >= threshold`) (`internal/checkpoint/checkpoint.go:183`, `internal/checkpoint/checkpoint.go:189`).

**Covers:** `internal/checkpoint/checkpoint.go:19`, `internal/cmd/checkpoint_cmd.go:15`

## 6. Crash sequence: who detects, who recovers, what replays

There is no crash detector process in scope. Detection is lazy and happens at the next session start:

1. The `SessionStart` lifecycle hook runs `gt prime --hook`, which calls `detectSessionState` with no side effects (`internal/hooks/config.go:1063`, `internal/cmd/prime_session.go:283`).
2. Handoff marker wins first: `<workdir>/.runtime/handoff_to_successor` means `post-handoff` (`internal/cmd/prime_session.go:290`, `internal/constants/constants.go:153`).
3. Otherwise, for polecat and crew roles only, a present, parseable, non-stale (<24h) checkpoint means `crash-recovery` with the checkpoint age attached (`internal/cmd/prime_session.go:298`).
4. Otherwise, hooked-bead lookup (agent bead's `hook_bead` column first, assigned active-work query second, town-level fallback third) means `autonomous`; else `normal` (`internal/cmd/prime_session.go:307`).
5. Separately, `outputCheckpointContext` re-reads the checkpoint, silently ignores read errors, deletes it when stale (>24h), and otherwise prints molecule, step, hooked bead, branch, first five modified files, and notes under a "Previous Session Checkpoint" heading (`internal/cmd/prime_output.go:770`, `internal/cmd/prime_output.go:789`).

Replayed versus lost:

- Replayed (durable): the git branch and all commits including `WIP: checkpoint (auto)` commits; the worktree files on disk, including uncommitted changes the checkpoint dog may not yet have committed; the bead-Hook assignment, which is re-resolved from the beads database rather than trusted blindly from the checkpoint.
- Advisory only: `ModifiedFiles`, `LastCommit`, `Branch`, and `Notes` are hints for the successor agent — nothing checks the files back out or restores the branch pointer.
- Lost: the predecessor's in-memory reasoning, tool-call history, and anything never written to disk or committed; checkpoints older than 24 hours are deleted instead of shown.

**Covers:** `internal/cmd/prime_session.go:272`, `internal/cmd/prime_output.go:755`, `internal/constants/constants.go:132`

## 7. WIP commits and squash

`WIPCommitPrefix = "WIP: checkpoint (auto)"` names the auto-commit subject (`internal/checkpoint/squash.go:12`). `CountWIPCommits(workDir, baseRef)` resolves `merge-base(baseRef, HEAD)` and counts subjects with that prefix in `merge-base..HEAD` (`internal/checkpoint/squash.go:16`). `SquashWIPCommits` soft-resets to the merge base (keeping all changes staged), then creates one commit titled with the first non-WIP subject (remaining non-WIP subjects as bullet lines) or the generic `squashed WIP checkpoint commits` when everything was WIP, returning the squashed WIP count (`internal/checkpoint/squash.go:47`, `internal/checkpoint/squash.go:80`). This is declared safe because the refinery squash-merges polecat branches anyway (`internal/checkpoint/squash.go:45`).

**Covers:** `internal/checkpoint/squash.go:1`

## 8. Atomic file writes

```go
func WriteFile(path string, data []byte, perm os.FileMode) error {
	dir := filepath.Dir(path)
	base := filepath.Base(path)
	// "*" in the pattern is replaced with a random suffix by os.CreateTemp,
	// preventing concurrent writers from colliding on the same temp file.
	f, err := os.CreateTemp(dir, base+".tmp.*")
	...
	if err := os.Chmod(tmpName, perm); err != nil { ... }
	if err := os.Rename(tmpName, path); err != nil { ... }
	return nil
}
```

(`internal/atomicfile/atomicfile.go:56`). The package doc states the contract: write-to-temp in the same directory plus rename, atomic on POSIX, leaf package with no internal dependencies so low-level callers avoid import cycles (`internal/atomicfile/atomicfile.go:1`). `WriteJSON`/`WriteJSONWithPerm` marshal indented JSON then delegate; `EnsureDirAndWriteJSON*` create parents (`0755`) first (`internal/atomicfile/atomicfile.go:13`, `internal/atomicfile/atomicfile.go:34`). Each concurrent writer gets a distinct temp name, so outputs never interleave — the file is always one writer's complete content (`internal/atomicfile/atomicfile.go:52`).

Consumers in scope: `SyncManagedClaudeSettings` writes `settings.json` with mode `0600` via `atomicfile.WriteFile` after merging managed hooks over preserved fields (`internal/hooks/config.go:223`, `internal/hooks/config.go:266`); `SyncForRole` and `writeTemplate` use `0600` for JSON settings and `0644` otherwise, explicitly citing gh#3500 where concurrent polecat spawns left truncated JSON that Claude rejected (`internal/hooks/installer.go:108`, `internal/hooks/installer.go:143`, `internal/hooks/installer_concurrent_test.go:13`). The checkpoint writer is the exception: it uses `os.WriteFile` directly (`internal/checkpoint/checkpoint.go:101`).

**Covers:** `internal/atomicfile/atomicfile.go:1`, `internal/hooks/installer.go:24`, `internal/hooks/installer_concurrent_test.go:28`

## 9. Locking around worktrees

Per-polecat and pool exclusion use `github.com/gofrs/flock` (`internal/polecat/manager.go:19`). Both helpers create `<rig>/.runtime/locks/` and lock `<name>`-scoped or pool-scoped files; callers must `defer Unlock()` (`internal/polecat/manager.go:214`, `internal/polecat/manager.go:231`). Coverage in scope: `AllocateAndAdd` (pool plus polecat), `AddWithOptions` (polecat), `RemoveWithOptions` (polecat), plus repair/rename paths that take the same per-polecat lock (`internal/polecat/manager.go:666`, `internal/polecat/manager.go:878`, `internal/polecat/manager.go:1128`, `internal/polecat/manager.go:1349`). Flocks are advisory and inter-process; the settings-file race needed no flock because atomic rename already guarantees a well-formed file, which is exactly what the concurrent-spawn regression test pins (`internal/hooks/installer_concurrent_test.go:20`).

The git layer adds a safety guard rather than a lock: every mutating worktree subcommand (`add`, `remove`, `move`, `prune`, plus checkout/merge/rebase/reset and friends) is checked by `guardUnsafeTownRootMutation`, which refuses operations whose effective workdir resolves to the town root and refuses worktree targets under `mayor/`, `.dolt-data/`, `.runtime/`, `.beads/`, or `daemon/` (`internal/git/git.go:218`, `internal/git/git.go:328`, `internal/git/git.go:438`, `internal/git/git.go:535`). Clones additionally run isolated in a temp dir with `GIT_CEILING_DIRECTORIES` set, then move the result into place with rename-or-copy fallback (`internal/git/git.go:609`, `internal/git/git.go:48`).

**Covers:** `internal/polecat/manager.go:214`, `internal/git/git.go:98`, `internal/git/git.go:607`

## 10. Lifecycle-hook config system (the other "hooks")

`HooksConfig` covers eight event types, including `SessionStart`, `Stop`, `PreCompact`, `UserPromptSubmit`, and notably `WorktreeCreate`/`WorktreeRemove` (`internal/hooks/config.go:31`, `internal/hooks/config.go:787`). Effective config is `Merge(DefaultBase(), onDiskBase)` as the floor, then role override, then `rig/role` override — more specific wins (`internal/hooks/config.go:506`, `internal/hooks/config.go:1110`). Per-matcher semantics: same matcher replaces, new matcher appends, empty hooks list deletes (`internal/hooks/merge.go:11`, `internal/hooks/merge.go:89`). `LoadBase`/`LoadOverride` cascade `$GT_HOME/.gt` over `~/.gt`, with `gastown/crew` stored as `gastown__crew.json` (`internal/hooks/config.go:875`, `internal/hooks/config.go:906`). `DiscoverTargets` emits one shared `settings.json` per role parent (`crew/`, `polecats/`, `witness/`, `refinery/`, town `mayor`/`deacon`), passed to agents via `--settings` so customer repos stay clean, with `DiscoverWorktrees` handling polecats whose real git root sits one level below the slot directory (`internal/hooks/config.go:555`, `internal/hooks/config.go:717`, `docs/HOOKS.md:22`).

Defaults: `SessionStart`/`PreCompact` run `gt prime --hook`, `UserPromptSubmit` runs `gt mail check --inject`, `Stop` runs `gt costs record`, and `PreToolUse` guards `gh pr create`, branch creation, `rm -rf /`, and force pushes (`internal/hooks/config.go:1015`). Built-in role deltas add polecat `Stop` auto-`gt done` via `polecat-stop-check`, crew `PreCompact` session cycling via `gt handoff --cycle`, and witness/deacon/refinery patrol-formula guards (`internal/hooks/config.go:326`). Role-aware template installers split autonomous (polecat, witness, refinery, deacon, boot) from interactive (mayor, crew) variants (`internal/hookutil/roletype.go:15`, `internal/hooks/installer.go:212`).

**Covers:** `internal/hooks/config.go:1`, `internal/hooks/merge.go:1`, `internal/hooks/installer.go:24`, `internal/hookutil/roletype.go:1`, `docs/HOOKS.md:1`

## 11. `.runtime` directory

The repo-root `.runtime/` holds only `setup-hooks/01-git-config.sh`, which propagates the global git identity into each new polecat worktree via `git -C "$GT_WORKTREE_PATH" config user.name/email` (`.runtime/setup-hooks/01-git-config.sh:1`). At spawn time the manager executes the rig's setup-hook scripts against the fresh `clonePath` (`internal/polecat/manager.go:842`). At runtime, `<rig>/.runtime/` additionally hosts the `locks/` directory used by the polecat/pool flocks and the per-worktree `.runtime/handoff_to_successor` marker consumed by startup recovery (`internal/polecat/manager.go:219`, `internal/cmd/prime_session.go:291`, `internal/constants/constants.go:132`).

**Covers:** `.runtime/setup-hooks/01-git-config.sh:1`, `internal/constants/constants.go:132`

**Covers:** internal/worktree, internal/hooks, internal/hookutil, internal/git (worktree + guard paths), internal/checkpoint, internal/atomicfile, .runtime, docs/HOOKS.md, README Hooks sections
