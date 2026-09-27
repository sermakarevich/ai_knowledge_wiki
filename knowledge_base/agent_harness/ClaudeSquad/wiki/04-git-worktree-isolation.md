> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Git Worktree Isolation and Review
**In one sentence:** Each agent instance gets its own git worktree on its own branch so parallel agents never conflict, and the `gh` CLI pushes branches for review.

## Key points
- Each instance provisions a dedicated worktree under `<configDir>/worktrees/<sanitized-branch>_<hex-nanotime>` via `resolveWorktreePaths` (`worktree.go:49-70`), created by `Setup` which ensures the directory exists then dispatches to new- or existing-branch setup (`worktree_ops.go:13-36`).
- Branch names default to `<BranchPrefix><sessionName>` then pass through `sanitizeBranchName`, which lowercases, replaces spaces with dashes, strips everything outside `[a-z0-9-_/.]`, collapses dashes, and trims edge dashes/slashes (`worktree.go:73-78`, `util.go:13-33`); pre-existing-branch sessions skip prefixing and set `isExistingBranch=true` so the branch survives cleanup (`worktree.go:95-108`).
- Isolation holds because a new worktree is created from the recorded `HEAD` commit with `git worktree add -b <branch> <path> <headCommit>`, giving each agent a clean, independent working tree instead of sharing the user's checkout (`worktree_ops.go:101-112`); reusing an existing branch checks out that branch into a fresh path rather than the repo root (`worktree_ops.go:39-68`).
- The TUI review tab reads `Diff()` (`diff.go:26-52`), which runs `git add -N .` so untracked files appear, then `git --no-pager diff <baseCommitSHA>` and counts `+`/`-` lines excluding `+++`/`---` headers; `DiffNumstat()` (`diff.go:57-75`) runs `diff --numstat` and sums columns via `parseNumstat`, skipping binary `-/-` rows (`diff.go:80-98`).
- Local-only commits go through `CommitChanges` (`worktree_git.go:128-151`: `IsDirty` gate, `git add .`, `git commit -m --no-verify`); remote publish goes through `PushChanges` (`worktree_git.go:71-126`: same commit step, then `gh repo sync --source -b <branch>` with fallback to `git push -u origin <branch>`, then `gh repo sync -b <branch>`, optional `gh browse --branch` via `OpenBranchURL` in `worktree_git.go:190-203`), and every `gh` path is gated by `checkGHCLI` which requires the binary plus `gh auth status` (`util.go:36-49`).
- Teardown is `Cleanup` (remove worktree with `git worktree remove -f`, force-delete the branch unless `isExistingBranch`, then `git worktree prune`, aggregating errors via `combineErrors`) (`worktree_ops.go:116-150`, `worktree_branch.go:8-21`); `Remove` drops only the worktree and keeps the branch (`worktree_ops.go:152-160`); the global `CleanupWorktrees` scans the worktrees directory, maps `git worktree list --porcelain` output to branches, force-deletes matching branches, removes directories, and prunes (`worktree_ops.go:170-236`).
- Repo guards are `IsGitRepo` (`git -C <path> rev-parse --show-toplevel`, boolean) and `findGitRepoRoot` (same command, returns trimmed toplevel or error) (`util.go:52-64`), called by `resolveWorktreePaths` so non-repo paths fail before any worktree is created (`worktree.go:56-60`); runtime health uses `IsValidWorktree` (path plus `.git` entry must exist) (`worktree_git.go:162-179`) and `IsBranchCheckedOut` (`git branch --show-current` compared to the instance branch) (`worktree_git.go:181-188`).
- Failure modes are explicit: empty repos abort with "please create an initial commit" when `rev-parse HEAD` reports an ambiguous/invalid object (`worktree_ops.go:92-99`); unknown branches abort with "not found locally or on remote" (`worktree_ops.go:49-54`); orphaned directories are force-removed before `worktree add` so stale paths do not block setup (`worktree_ops.go:42-45`, `worktree_ops.go:83-87`, verified by `worktree_ops_test.go:11-70`); a missing `baseCommitSHA` surfaces as a `DiffStats.Error` instead of crashing the TUI loop (`diff.go:26-40`, `worktree_ops.go:70-80`); `IsDirty` errors abort commit/push before staging (`worktree_git.go:76-80`, `worktree_git.go:153-160`); failed pushes return the combined git output wrapped with context (`worktree_git.go:99-107`).

---
## Worktree layout and naming
All worktrees live outside the user's checkout under the app config directory (`worktree.go:11-18`), with one subdirectory per instance (`worktree.go:61-68`). The hex-suffixed timestamp guarantees uniqueness even when two sessions share a sanitized branch name (`worktree.go:66-68`).

```go
// session/git/worktree.go:49-70
func resolveWorktreePaths(repoPath string, branchName string) (resolvedRepo string, worktreePath string, err error) {
	absPath, err := filepath.Abs(repoPath)
	if err != nil {
		log.ErrorLog.Printf("git worktree path abs error, falling back to repoPath %s: %s", repoPath, err)
		absPath = repoPath
	}

	resolvedRepo, err = findGitRepoRoot(absPath)
	if err != nil {
		return "", "", err
	}

	worktreeDir, err := getWorktreeDirectory()
	if err != nil {
		return "", "", err
	}

	worktreePath = filepath.Join(worktreeDir, sanitizeBranchName(branchName))
	worktreePath = worktreePath + "_" + fmt.Sprintf("%x", time.Now().UnixNano())

	return resolvedRepo, worktreePath, nil
}
```

Branch construction prepends the configured prefix to the session name and sanitizes the result, which also neutralizes inputs such as Windows `DOMAIN\user` backslashes (`worktree.go:73-78`). Sanitization itself is a fixed pipeline: lowercase, space-to-dash, regex strip, dash collapse, edge trim (`util.go:13-33`).

```go
// session/git/worktree.go:73-91
func NewGitWorktree(repoPath string, sessionName string) (tree *GitWorktree, branchname string, err error) {
	cfg := config.LoadConfig()
	branchName := fmt.Sprintf("%s%s", cfg.BranchPrefix, sessionName)
	// Sanitize the final branch name to handle invalid characters from any source
	// (e.g., backslashes from Windows domain usernames like DOMAIN\user)
	branchName = sanitizeBranchName(branchName)

	repoPath, worktreePath, err := resolveWorktreePaths(repoPath, branchName)
	if err != nil {
		return nil, "", err
	}

	return &GitWorktree{
		repoPath:     repoPath,
		sessionName:  sessionName,
		branchName:   branchName,
		worktreePath: worktreePath,
	}, branchName, nil
}
```

```go
// session/git/util.go:13-33
func sanitizeBranchName(s string) string {
	// Convert to lower-case
	s = strings.ToLower(s)

	// Replace spaces with a dash
	s = strings.ReplaceAll(s, " ", "-")

	// Remove any characters not allowed in our safe subset.
	// Here we allow: letters, digits, dash, underscore, slash, and dot.
	re := regexp.MustCompile(`[^a-z0-9\-_/.]+`)
	s = re.ReplaceAllString(s, "")

	// Replace multiple dashes with a single dash (optional cleanup)
	reDash := regexp.MustCompile(`-+`)
	s = reDash.ReplaceAllString(s, "-")

	// Trim leading and trailing dashes or slashes to avoid issues
	s = strings.Trim(s, "-/")

	return s
}
```

Behavior evidence for sanitization lives in `util_test.go:7-73` (spaces, mixed case, special characters, dash collapsing, edge trims).

## Branch management
`Setup` is the single entry point: it creates the worktrees directory, short-circuits to `setupFromExistingBranch` when `isExistingBranch` is set, otherwise probes `refs/heads/<branch>` with `show-ref --verify` to decide between reuse and fresh creation (`worktree_ops.go:13-36`).

```go
// session/git/worktree_ops.go:13-36
func (g *GitWorktree) Setup() error {
	// Ensure worktrees directory exists early (can be done in parallel with branch check)
	worktreesDir, err := getWorktreeDirectory()
	if err != nil {
		return fmt.Errorf("failed to get worktree directory: %w", err)
	}

	if err := os.MkdirAll(worktreesDir, 0755); err != nil {
		return err
	}

	// If this worktree uses a pre-existing branch, always set up from that branch
	// (it may exist locally or only on the remote).
	if g.isExistingBranch {
		return g.setupFromExistingBranch()
	}

	// Check if branch exists using git CLI (much faster than go-git PlainOpen)
	_, err = g.runGitCommand(g.repoPath, "show-ref", "--verify", fmt.Sprintf("refs/heads/%s", g.branchName))
	if err == nil {
		return g.setupFromExistingBranch()
	}
	return g.setupNewWorktree()
}
```

Existing-branch setup prefers the local branch (`git worktree add <path> <branch>`), falls back to creating a tracking branch from `origin/<branch>` via `git worktree add -b`, and errors if neither exists; both paths end with `recordBaseCommit` (`worktree_ops.go:39-68`). Fresh setup deletes any stale branch, pins `baseCommitSHA` to current `HEAD`, and creates the worktree from that commit hash (`worktree_ops.go:83-113`). Every setup path records the base commit with `rev-parse HEAD` in the new worktree so later diffs have a fixed reference (`worktree_ops.go:73-80`).

```go
// session/git/worktree_ops.go:83-107
func (g *GitWorktree) setupNewWorktree() error {
	// Clean up any existing worktree first
	_, _ = g.runGitCommand(g.repoPath, "worktree", "remove", "-f", g.worktreePath) // Ignore error if worktree doesn't exist
	// If the directory is still there (orphaned, not registered with git), drop it so `git worktree add` won't fail.
	_ = os.RemoveAll(g.worktreePath)

	// Clean up any existing branch using git CLI (much faster than go-git PlainOpen)
	_, _ = g.runGitCommand(g.repoPath, "branch", "-D", g.branchName) // Ignore error if branch doesn't exist

	output, err := g.runGitCommand(g.repoPath, "rev-parse", "HEAD")
	if err != nil {
		if strings.Contains(err.Error(), "fatal: ambiguous argument 'HEAD'") ||
			strings.Contains(err.Error(), "fatal: not a valid object name") ||
			strings.Contains(err.Error(), "fatal: HEAD: not a valid object name") {
			return fmt.Errorf("this appears to be a brand new repository: please create an initial commit before creating an instance")
		}
		return fmt.Errorf("failed to get HEAD commit hash: %w", err)
	}
	headCommit := strings.TrimSpace(string(output))
	g.baseCommitSHA = headCommit
```

Branch search for the attach-to-existing-branch UI lists all branches sorted by committer date, strips the `origin/` prefix, deduplicates local/remote pairs, filters case-insensitively, and caps at 50 results (`worktree_git.go:12-55`).

## Isolation argument — why no conflicts
Git worktrees allow one repository to have multiple checked-out branches at distinct paths; because each instance writes only inside its own worktree path and commits only to its own branch, two agents never share a working tree, index, or `HEAD` (`worktree_ops.go:101-112`, `worktree_ops.go:62-68`). Fresh sessions additionally start from the pinned commit hash rather than inheriting uncommitted changes from another worktree (`worktree_ops.go:104-107`). The only shared mutable state is the branch namespace, which is partitioned by the per-session branch name plus timestamp-suffixed directory (`worktree.go:66-78`).

## Diff pipeline
`DiffStats` carries full content, added/removed counts, and a non-fatal `Error` field so setup problems propagate without breaking the caller (`diff.go:8-23`). `Diff` stages intent-to-add for untracked files, diffs against `GetBaseCommitSHA()`, and counts lines while skipping `+++`/`---` file headers (`diff.go:26-52`).

```go
// session/git/diff.go:26-52
func (g *GitWorktree) Diff() *DiffStats {
	stats := &DiffStats{}

	// -N stages untracked files (intent to add), including them in the diff
	_, err := g.runGitCommand(g.worktreePath, "add", "-N", ".")
	if err != nil {
		stats.Error = err
		return stats
	}

	content, err := g.runGitCommand(g.worktreePath, "--no-pager", "diff", g.GetBaseCommitSHA())
	if err != nil {
		stats.Error = err
		return stats
	}
	lines := strings.Split(content, "\n")
	for _, line := range lines {
		if strings.HasPrefix(line, "+") && !strings.HasPrefix(line, "+++") {
			stats.Added++
		} else if strings.HasPrefix(line, "-") && !strings.HasPrefix(line, "---") {
			stats.Removed++
		}
	}
	stats.Content = content

	return stats
}
```

`DiffNumstat` follows the same preamble but runs `diff --numstat` and delegates summation to `parseNumstat`, which splits on the first two tabs (preserving tabs in paths), parses integers, and ignores binary `-/-` rows (`diff.go:57-98`). Parsing behavior is pinned by table tests covering empty output, multi-file sums, binary skips, tabbed paths, and trailing newlines (`diff_test.go:5-59`).

## Commit/checkout/push and gh usage
All git invocations funnel through `runGitCommand`, which runs `git -C <path> <args>` and wraps combined output in the returned error (`worktree_git.go:57-68`). `IsDirty` shells `git status --porcelain` and treats any output as dirty (`worktree_git.go:153-160`).

```go
// session/git/worktree_git.go:71-95
func (g *GitWorktree) PushChanges(commitMessage string, open bool) error {
	if err := checkGHCLI(); err != nil {
		return err
	}

	// Check if there are any changes to commit
	isDirty, err := g.IsDirty()
	if err != nil {
		return fmt.Errorf("failed to check for changes: %w", err)
	}

	if isDirty {
		// Stage all changes
		if _, err := g.runGitCommand(g.worktreePath, "add", "."); err != nil {
			log.ErrorLog.Print(err)
			return fmt.Errorf("failed to stage changes: %w", err)
		}

		// Create commit
		if _, err := g.runGitCommand(g.worktreePath, "commit", "-m", commitMessage, "--no-verify"); err != nil {
			log.ErrorLog.Print(err)
			return fmt.Errorf("failed to commit changes: %w", err)
		}
	}
```

The push sequence first runs `gh repo sync --source -b <branch>` with working directory set to the worktree, falls back to `git push -u origin <branch>` if sync fails, then runs `gh repo sync -b <branch>`; the optional `open` flag calls `OpenBranchURL` (`gh browse --branch <branch>`) with failures logged but not returned (`worktree_git.go:96-126`, `worktree_git.go:190-203`). `CommitChanges` performs only the dirty-gated `add` plus `commit --no-verify` and never touches the network (`worktree_git.go:128-151`). The `gh` gate checks binary presence via `exec.LookPath` and auth via `gh auth status` (`util.go:36-49`).

```go
// session/git/util.go:36-55
func checkGHCLI() error {
	// Check if gh is installed
	if _, err := exec.LookPath("gh"); err != nil {
		return fmt.Errorf("GitHub CLI (gh) is not installed. Please install it first")
	}

	// Check if gh is authenticated
	cmd := exec.Command("gh", "auth", "status")
	if err := cmd.Run(); err != nil {
		return fmt.Errorf("GitHub CLI is not configured. Please run 'gh auth login' first")
	}

	return nil
}
```

## Cleanup
`Cleanup` stats the path first (skipping removal when absent, erroring on non-NotExist stat failures), runs `git worktree remove -f`, force-deletes the branch unless the session was marked pre-existing, prunes administrative files, and combines all failures into one multi-line error (`worktree_ops.go:116-150`). Error combination returns nil for zero, the single error unwrapped for one, and a `multiple errors occurred:` list otherwise (`worktree_branch.go:8-21`).

```go
// session/git/worktree_ops.go:116-140
func (g *GitWorktree) Cleanup() error {
	var errs []error

	// Check if worktree path exists before attempting removal
	if _, err := os.Stat(g.worktreePath); err == nil {
		// Remove the worktree using git command
		if _, err := g.runGitCommand(g.repoPath, "worktree", "remove", "-f", g.worktreePath); err != nil {
			errs = append(errs, err)
		}
	} else if !os.IsNotExist(err) {
		// Only append error if it's not a "not exists" error
		errs = append(errs, fmt.Errorf("failed to check worktree path: %w", err))
	}

	// Delete the branch using git CLI, but skip if this is a pre-existing branch
	if !g.isExistingBranch {
		if _, err := g.runGitCommand(g.repoPath, "branch", "-D", g.branchName); err != nil {
			// Only log if it's not a "branch not found" error
			if !strings.Contains(err.Error(), "not found") {
				errs = append(errs, fmt.Errorf("failed to remove branch %s: %w", g.branchName, err))
			}
		}
	}
```

`CleanupWorktrees` is the coarse recovery path: it lists the worktrees directory, parses `git worktree list --porcelain` into a path-to-branch map, force-deletes each matching branch (logging and continuing on failure), removes each directory with `os.RemoveAll`, and finishes with `git worktree prune` (`worktree_ops.go:170-236`). Note it runs `git` in the process working directory rather than a `-C` repo path, so it assumes repository context (`worktree_ops.go:182-187`).

## Failure modes
Empty repositories fail fast with an actionable message instead of a raw git error (`worktree_ops.go:92-99`); attaching to a branch that exists neither locally nor on `origin` returns a not-found error before any filesystem mutation beyond the idempotent pre-cleanup (`worktree_ops.go:49-54`). Orphaned worktree directories (path exists but unregistered with git, so `worktree remove -f` is a no-op) are handled by unconditional `os.RemoveAll` before `worktree add`, a path covered by the orphan test (`worktree_ops.go:42-45`, `worktree_ops.go:83-87`, `worktree_ops_test.go:11-70`). Base-commit recording is tested separately to guarantee diffs have a valid reference (`worktree_ops_test.go:72-111`). Worktree-lock contention has no dedicated handler; the mitigation is force removal (`-f`) plus prune on both setup and teardown paths (`worktree_ops.go:43-68`, `worktree_ops.go:116-168`). Push failures preserve the remote command's combined output in the error string (`worktree_git.go:99-107`), while `gh browse` failures during `open` are deliberately non-fatal (`worktree_git.go:117-123`).
**Covers:** session/git/worktree.go, session/git/worktree_ops.go, session/git/worktree_git.go, session/git/worktree_branch.go, session/git/diff.go, session/git/util.go (+ tests)
