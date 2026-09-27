> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Session Lifecycle and State
**In one sentence:** The `Instance` struct plus a JSON state file form a durable session record decoupled from live tmux processes, and every lifecycle operation (create, pause, resume, checkout, push, kill) mutates both the git worktree/tmux session and that persisted record.
## Key points
- `Instance` is the unit of work: identity fields (`Title`, `Path`, `Branch`, `Program`), dimensions, timestamps, plus unexported live handles (`started`, `tmuxSession`, `gitWorktree`) that are never serialized (`session/instance.go:32`).
- Persistence is JSON: `Storage` marshals only `Started()` instances to `InstanceData`/`GitWorktreeData`/`DiffStatsData` and delegates to `config.State`, which stores raw JSON in a `state.json` file under the config dir (`session/storage.go:57`, `config/state.go:41`).
- Create is two-phase: `NewInstance` only builds an unstarted record with an absolute path (`session/instance.go:163`), then `Start(true)` creates the git worktree/branch and starts the tmux session, with automatic `Kill()` cleanup on setup failure (`session/instance.go:203`).
- Pause preserves the branch and discards the worktree (committing dirty state first, detaching tmux via `DetachSafely`); kill destroys both tmux session and worktree and removes the storage row; checkout is Pause behind a help screen, and push commits plus pushes without changing lifecycle state (`session/instance.go:423`, `session/instance.go:288`, `app/app.go:739`, `app/app.go:716`).
- Resume rebuilds from the branch: it refuses when the branch is checked out elsewhere, reuses the on-disk worktree if still valid (preserving uncommitted work after a crash) and otherwise re-adds it, then restores or restarts tmux (`session/instance.go:510`).
- Restart reconciliation is loss-tolerant: `newHome` reloads every row via `FromInstanceData`, and `Start(false)` parks instances whose tmux session is gone as `Paused` instead of failing, so one dead session never hides the rest (`app/app.go:106`, `session/instance.go:248`, `session/instance_test.go:41`).
- Failure handling is fail-fast on load but best-effort on teardown: `LoadInstances` aborts on the first bad row (`session/storage.go:76`), while `Kill`/`Pause` attempt both tmux and git cleanup and combine errors (`session/instance.go:288`, `session/instance.go:423`).
---
## The Instance type
`Status` is a four-value enum — `Running`, `Ready`, `Loading`, `Paused` — where `Paused` explicitly means "worktree removed but branch preserved" (`session/instance.go:18`). The struct splits durable fields from live handles (`session/instance.go:32`):
```go
// session/instance.go:32-69
// Instance is a running instance of claude code.
type Instance struct {
	// Title is the title of the instance.
	Title string
	// Path is the path to the workspace.
	Path string
	// Branch is the branch of the instance.
	Branch string
	// Status is the status of the instance.
	Status Status
	// Program is the program to run in the instance.
	Program string
	// Height is the height of the instance.
	Height int
	// Width is the width of the instance.
	Width int
	// CreatedAt is the time the instance was created.
	CreatedAt time.Time
	// UpdatedAt is the time the instance was last updated.
	UpdatedAt time.Time
	// AutoYes is true if the instance should automatically press enter when prompted.
	AutoYes bool
	// Prompt is the initial prompt to pass to the instance on startup
	Prompt string
	// DiffStats stores the current git diff statistics
	diffStats *git.DiffStats
	// selectedBranch is the existing branch to start on (empty = new branch from HEAD)
	selectedBranch string
	// The below fields are initialized upon calling Start().
	started bool
	// tmuxSession is the tmux session for the instance.
	tmuxSession *tmux.TmuxSession
	// gitWorktree is the git worktree for the instance.
	gitWorktree *git.GitWorktree
}
```
`Title` is immutable once started because it keys the tmux session (`session/instance.go:403`). `started` gates almost every method: `RepoName`, `Attach`, `GetGitWorktree`, `Pause`, `Resume` all error on unstarted instances (`session/instance.go:186`, `session/instance.go:368`, `session/instance.go:423`, `session/instance.go:510`). Paused instances additionally refuse preview, resize, key input, and attach (`session/instance.go:330`, `session/instance.go:375`, `session/instance.go:665`, `app/app.go:779`).
## Storage and the state file
Serializable form drops live handles and keeps worktree coordinates plus cached diff stats (`session/storage.go:11`):
```go
// session/storage.go:11-42
// InstanceData represents the serializable data of an Instance
type InstanceData struct {
	Title     string    `json:"title"`
	Path      string    `json:"path"`
	Branch    string    `json:"branch"`
	Status    Status    `json:"status"`
	Height    int       `json:"height"`
	Width     int       `json:"width"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
	AutoYes   bool      `json:"auto_yes"`

	Program   string          `json:"program"`
	Worktree  GitWorktreeData `json:"worktree"`
	DiffStats DiffStatsData   `json:"diff_stats"`
}
```
`ToInstanceData` stamps `UpdatedAt` at save time and includes worktree/diff blocks only when non-nil (`session/instance.go:71`). `FromInstanceData` rebuilds the worktree handle from stored paths/SHA and always synthesizes a `diffStats` value, even an empty one (`session/instance.go:110`). `Storage.SaveInstances` skips unstarted instances, marshals the slice, and delegates to `config.InstanceStorage` (`session/storage.go:57`); `LoadInstances` unmarshals and calls `FromInstanceData` per row, returning on the first error (`session/storage.go:76`). `DeleteInstance` and `UpdateInstance` both load-all, match by `Title`, and rewrite the whole file (`session/storage.go:97`, `session/storage.go:122`).
The backing store is `config.State`: `{help_screens_seen, instances}` serialized with indent to `<configDir>/state.json`, defaulting to `[]` when missing or unparseable (`config/state.go:41`, `config/state.go:57`, `config/state.go:90`). `SaveInstances`/`GetInstances`/`DeleteAllInstances` just set, return, or clear the raw `instances` blob (`config/state.go:111`).
## Create
`NewInstance` normalizes the repo path to absolute, sets `Status: Ready`, and records the requested branch in unexported `selectedBranch` without touching git or tmux (`session/instance.go:163`):
```go
// session/instance.go:163-184
func NewInstance(opts InstanceOptions) (*Instance, error) {
	t := time.Now()

	// Convert path to absolute
	absPath, err := filepath.Abs(opts.Path)
	if err != nil {
		return nil, fmt.Errorf("failed to get absolute path: %w", err)
	}

	return &Instance{
		Title:          opts.Title,
		Title:          opts.Title,
		Status:         Ready,
		Path:           absPath,
		Program:        opts.Program,
		Height:         0,
		Width:          0,
		CreatedAt:      t,
		UpdatedAt:      t,
		AutoYes:        false,
		selectedBranch: opts.Branch,
	}, nil
}
```
(Note: `Title` appears twice in the literal at `session/instance.go:172`; harmless duplicate key assignment.) The TUI creates this shell record on `KeyNew`/`KeyPrompt` (capped at 10 instances), holds a finalizer from `list.AddInstance`, and only finalizes it into the visible list after naming (`app/app.go:641`, `app/app.go:612`, `app/app.go:634`, `app/app.go:431`). The expensive `Start(true)` runs in a background `tea.Cmd` so the event loop stays responsive (`app/app.go:923`). On `instanceStartDoneMsg`/`instanceStartedMsg` failure the row is removed via `list.Kill()`; on success the full list is persisted (`app/app.go:212`, `app/app.go:304`). Esc or prompt-cancel on an unstarted row also kills it without persisting (`app/app.go:468`, `app/app.go:1003`).
`Start(true)` branches on `selectedBranch`: existing branch via `NewGitWorktreeFromBranch`, else fresh branch via `NewGitWorktree` (`session/instance.go:218`). It then runs worktree `Setup()` followed by `tmuxSession.Start(worktreePath)`, cleaning up the worktree if tmux fails and calling `Kill()` on any other setup error via a deferred handler (`session/instance.go:264`, `session/instance.go:237`). Success sets `started=true` and `Status=Running` (`session/instance.go:237`, `session/instance.go:282`).
## Pause/Resume
`Pause` commits dirty work locally with a `[claudesquad] update ... (paused)` message, detaches (not closes) tmux to preserve scrollback, removes and prunes the worktree, copies the branch name to the clipboard, and sets `Paused` (`session/instance.go:423`):
```go
// session/instance.go:423-431
// Pause stops the tmux session and removes the worktree, preserving the branch
func (i *Instance) Pause() error {
	if !i.started {
		return fmt.Errorf("cannot pause instance that has not been started")
	}
	if i.Status == Paused {
		return fmt.Errorf("instance is already paused")
	}
```
Pause refuses unstarted or already-paused instances (`session/instance.go:424`). If the worktree is orphaned (path or `.git` missing), it skips the dirty check, detaches tmux, deletes the leftover directory so a future `git worktree add` will not conflict, prunes metadata, and still transitions to `Paused` (`session/instance.go:436`). A failed commit aborts before touching tmux/worktree; a failed remove/prune aborts with combined errors (`session/instance.go:467`, `session/instance.go:485`).
`Resume` only accepts `Paused` instances and refuses when the branch is checked out elsewhere (`session/instance.go:510`):
```go
// session/instance.go:510-539
// Resume recreates the worktree and restarts the tmux session
func (i *Instance) Resume() error {
	if !i.started {
		return fmt.Errorf("cannot resume instance that has not been started")
	}
	if i.Status != Paused {
		return fmt.Errorf("can only resume paused instances")
	}

	// Check if branch is checked out
	if checked, err := i.gitWorktree.IsBranchCheckedOut(); err != nil {
		log.ErrorLog.Print(err)
		return fmt.Errorf("failed to check if branch is checked out: %w", err)
	} else if checked {
		return fmt.Errorf("cannot resume: branch is checked out, please switch to a different branch")
	}
```
Crucially, `Setup()` (remove + re-add) runs only when the worktree is invalid; a valid on-disk worktree — e.g. after a tmux-server crash — is left untouched so uncommitted work survives (`session/instance.go:526`). Tmux is then restored if the session still exists, else restarted, with worktree cleanup on start failure (`session/instance.go:542`). Success sets `Running` (`session/instance.go:570`). The TUI wires these to `KeyCheckout` (Pause behind a checkout help screen plus terminal cleanup) and `KeyResume` (`app/app.go:739`, `app/app.go:770`).
## Checkout and push
Checkout and push are app-level compositions, not `Instance` methods. `KeyCheckout` shows the checkout help screen, then calls `selected.Pause()` and cleans up the terminal pane (`app/app.go:739`). `KeySubmit` (push) builds a timestamped `[claudesquad] update from '<title>'` commit message and calls `worktree.PushChanges(commitMsg, true)` — commit plus push for PR creation — without pausing or changing status (`app/app.go:716`):
```go
// app/app.go:716-738
	case keys.KeySubmit:
		selected := m.list.GetSelectedInstance()
		if selected == nil || selected.Status == session.Loading {
			return m, nil
		}

		// Create the push action as a tea.Cmd
		pushAction := func() tea.Msg {
			// Default commit message with timestamp
			commitMsg := fmt.Sprintf("[claudesquad] update from '%s' on %s", selected.Title, time.Now().Format(time.RFC822))
			worktree, err := selected.GetGitWorktree()
			if err != nil {
				return err
			}
			if err = worktree.PushChanges(commitMsg, true); err != nil {
				return err
			}
			return nil
		}
```
Both are confirmation-gated (`confirmAction`) for push and kill, while checkout uses a help-screen gate instead (`app/app.go:737`, `app/app.go:714`, `app/app.go:746`).
## Kill/Delete and reset
`Kill()` always attempts both tmux `Close()` and worktree `Cleanup()`, collecting errors from both rather than short-circuiting, and is a no-op on never-started instances (`session/instance.go:288`):
```go
// session/instance.go:288-312
// Kill terminates the instance and cleans up all resources
func (i *Instance) Kill() error {
	if !i.started {
		// If instance was never started, just return success
		return nil
	}

	var errs []error

	// Always try to cleanup both resources, even if one fails
	// Clean up tmux session first since it's using the git worktree
	if i.tmuxSession != nil {
		if err := i.tmuxSession.Close(); err != nil {
			errs = append(errs, fmt.Errorf("failed to close tmux session: %w", err))
		}
	}
```
The TUI `KeyKill` handler guards `Loading` rows, refuses branches checked out elsewhere, cleans the terminal pane, deletes the storage row *before* killing the live instance, then emits `instanceChangedMsg` (`app/app.go:677`). `DeleteInstance`/`DeleteAllInstances` only rewrite JSON; actual tmux/worktree teardown is the caller's job (`session/storage.go:97`, `session/storage.go:146`). Reorder (`MoveUp`/`MoveDown`) also rewrites the whole file, so display order is persisted (`app/app.go:754`, `app/app.go:762`). Multi-error reporting joins messages under `multiple cleanup errors occurred:` (`session/instance.go:314`).
## Restart and reconciliation — how it re-discovers or orphans tmux sessions
On startup `newHome` loads config, loads `State`, builds `Storage`, then calls `LoadInstances()` — which re-attaches every persisted row — and immediately finalizes each into the list (`app/app.go:106`):
```go
// app/app.go:135-150
	// Load saved instances
	instances, err := storage.LoadInstances()
	if err != nil {
		fmt.Printf("Failed to load instances: %v\n", err)
		os.Exit(1)
	}

	// Add loaded instances to the list
	for _, instance := range instances {
		// Call the finalizer immediately.
		h.list.AddInstance(instance)()
		if autoYes {
			instance.AutoYes = true
		}
	}
```
A corrupt file or single bad row is fatal to the whole load (`os.Exit(1)` here, error return in `LoadInstances`) (`app/app.go:136`, `session/storage.go:83`). Per-instance, `FromInstanceData` restores paused rows cheaply (mark `started`, synthesize a tmux handle, no attach) but calls `Start(false)` for anything else, which calls `tmuxSession.Restore()` (`session/instance.go:137`, `session/instance.go:248`):
```go
// session/instance.go:248-263
	if !firstTimeSetup {
		// Reuse existing session. If the tmux server died since we last ran (reboot,
		// crash, `tmux kill-server`), the session is gone but the worktree and branch
		// are still on disk. Park the instance as Paused so Resume can rebuild it.
		// Reporting an error here would be worse than useless: LoadInstances aborts on
		// the first failure, so a single dead session would hide every other instance.
		if err := tmuxSession.Restore(); err != nil {
			if errors.Is(err, tmux.ErrSessionNotFound) {
				log.WarningLog.Printf(
					"tmux session for %q no longer exists; pausing instance so it can be resumed", i.Title)
				i.SetStatus(Paused)
				return nil
			}
```
Surviving sessions come back `Running` with a fresh PTY attach; dead ones park as `Paused` with worktree/branch intact for later `Resume` (`session/instance_test.go:63`, `session/instance_test.go:41`). The metadata ticker only polls started, non-paused instances and skips rows paused mid-computation, so parked sessions cost no I/O (`app/app.go:935`, `app/app.go:238`).
## Failure modes
- Single bad persisted row hides everything: `LoadInstances` returns on the first `FromInstanceData` error and `newHome` exits (`session/storage.go:83`, `app/app.go:136`).
- `tmux kill-server`/reboot orphans worktrees on disk; by design these become resumable `Paused` rows rather than errors, but uncommitted work in a removed-vs-valid worktree depends on which pause path ran (`session/instance.go:254`, `session/instance.go:530`).
- Pause on a dirty worktree whose commit fails aborts before detach/remove, leaving the session live but the error combined and logged (`session/instance.go:467`).
- Pause/Resume/Kill on unstarted rows, double-pause, resume-when-not-paused, and resume onto a checked-out branch are all hard errors (`session/instance.go:424`, `session/instance.go:514`, `session/instance.go:519`).
- `Start(true)` failure triggers deferred `Kill()` plus worktree `Cleanup()`, and the TUI removes the row — a failed create leaves no record (`session/instance.go:237`, `session/instance.go:272`, `app/app.go:217`).
- Kill and push refuse when the branch is checked out in the main repo, preventing worktree corruption (`app/app.go:691`, `session/instance.go:519`).
**Covers:** session/instance.go, session/storage.go, session/instance_test.go, config/state.go, app/app.go (operation handlers)
