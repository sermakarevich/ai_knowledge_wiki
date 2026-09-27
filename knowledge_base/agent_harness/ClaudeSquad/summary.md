# Technical Analysis: claude-squad

**Repository:** https://github.com/smtg-ai/claude-squad
**Version analyzed:** v1.0.20 (ce1ffb4, 2026-08-20)
**Date:** 2026-09-09

---

## 1. Overview / What Problem It Solves
Claude Squad is a terminal app for a human developer who wants to run several AI coding agents at the same time. In plain terms: instead of one agent working in your code folder, you get a list of workers on the left and a live preview on the right, and you switch between them with single keys.

The problem it solves is conflict and loss of context. Parallel agents sharing one checkout overwrite each other, and background terminal sessions are hard to observe, pause, and review. Claude Squad gives each agent its own git worktree on its own branch for filesystem isolation (`README.md:150-154`), its own tmux session for terminal isolation, and a Bubble Tea TUI (terminal user interface) for management (`README.md:150-154`).

There is no scheduler, no task graph, no agent-to-agent messaging. The whole lifecycle is create, pause, resume, push, kill, capped at 10 instances (`app/app.go:24`, `app/app.go:613-615`, `app/app.go:642-644`). Push goes through `gh` with a `git push` fallback behind a confirmation modal (`session/git/worktree_git.go:71-126`, `app/app.go:716-738`).

## 2. High-Level Architecture
```
cobra rootCmd (main.go:27-78)
│
▼
app.Run(ctx, program, autoYes) ─ Bubble Tea home model (app/app.go:27-35)
│
▼
session.Storage + session.Instance (restored in app/app.go:106-152)
│
├─ ─ ► tmux session (isolated PTY per agent)
└─ ─ ► git worktree + branch (isolated filesystem per session)
         │
         ▼
     agent CLI process (claude / codex / aider / gemini)
```

New-session end-to-end path:
1. User runs `cs [-p <program>] [-y]` inside a git repo; `rootCmd` validates repo and resolves `program`/`autoYes` (`main.go:42-63`).
2. `app.Run` starts the `home` model; `newHome` restores existing instances from storage (`app/app.go:106-152`).
3. `n`/`N` key creates a `session.Instance` bound to a new git worktree/branch for filesystem isolation (`README.md:150-154`).
4. The instance starts inside its own tmux session running the selected agent CLI (`README.md:81-87`).
5. TUI polls previews and metadata via `previewTickMsg` and background `instanceStartCmd`/`metadataUpdate` commands (`app/app.go:183-194`).
6. Quit/persist leaves tmux and worktrees intact; `cs reset` tears down storage, tmux sessions, worktrees, and daemon (`main.go:80-115`).

Persistent state lives under `~/.claude-squad/`: `config.json` for user intent (`config/config.go:15-27`), `state.json` for runtime rows (`config/state.go:12`, `config/state.go:41`), `worktrees/` for isolation directories (`session/git/worktree.go:11-18`), `daemon.pid` for daemon coordination (`daemon/daemon.go:115-167`). `home` holds `storage`, `appConfig`, `appState`, `list`, `menu`, `tabbedWindow`, `errBox`, and overlays (`app/app.go:51-104`).

## 3. The Instance-Worktree-Session Triad
The core abstraction is one `Instance` row plus one git worktree plus one tmux session. `Instance` is the unit of work: identity fields (`Title`, `Path`, `Branch`, `Program`), dimensions, timestamps, plus unexported live handles (`started`, `tmuxSession`, `gitWorktree`) that are never serialized (`session/instance.go:32`).

`Status` is a four-value enum — `Running`, `Ready`, `Loading`, `Paused` — where `Paused` explicitly means "worktree removed but branch preserved" (`session/instance.go:18`). `Title` is immutable once started because it keys the tmux session (`session/instance.go:403`). `started` gates almost every method: `RepoName`, `Attach`, `GetGitWorktree`, `Pause`, `Resume` all error on unstarted instances (`session/instance.go:186`, `session/instance.go:368`, `session/instance.go:423`, `session/instance.go:510`).

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
`ToInstanceData` stamps `UpdatedAt` at save time and includes worktree/diff blocks only when non-nil (`session/instance.go:71`). `FromInstanceData` rebuilds the worktree handle from stored paths/SHA and always synthesizes a `diffStats` value, even an empty one (`session/instance.go:110`). `Storage.SaveInstances` skips unstarted instances (`session/storage.go:57`); `LoadInstances` unmarshals and calls `FromInstanceData` per row, returning on the first error (`session/storage.go:76`). `DeleteInstance` and `UpdateInstance` both load-all, match by `Title`, and rewrite the whole file (`session/storage.go:97`, `session/storage.go:122`).

## 4. LLM / External Service Integration
Design statement: it does NOT call LLMs itself. There is no API client, no model endpoint, no token handling, no prompt pipeline in code. Agent CLIs are subprocesses launched verbatim as the trailing command of `tmux new-session` (`session/tmux/tmux.go:93-102`).

External dependencies are binaries on `PATH`, not Go libraries. Hard requirements are the `tmux` binary on `PATH` plus per-agent CLIs such as `claude`/`aider`/`gemini` (`session/tmux/tmux.go:22-25`, `session/tmux/tmux.go:102`); `install.sh` installs tmux via brew/apt/dnf/yum (`install.sh:181-214`). Push/review requires `gh` (GitHub CLI), gated by `checkGHCLI` which requires the binary plus `gh auth status` (`session/git/util.go:36-49`). `keys/keys.go` only defines TUI list-navigation bindings and plays no role in tmux key injection (`keys/keys.go:38-58`, `keys/keys.go:61-134`).

Multi-harness support is one string field, not code — the only harness-aware branches are three suffix/prefix string checks for prompt and trust-screen detection (`ProgramClaude`/`ProgramAider`/`ProgramGemini` at `session/tmux/tmux.go:22-25`), which gains trivial extensibility at the cost of no capability model and prompt detection that silently misses unknown harnesses (`session/tmux/tmux.go:22-25`, `session/tmux/tmux.go:161-184`, `session/tmux/tmux.go:253-260`, `session/instance.go:344-356`).

## 5. The Session Pipeline
Create: `NewInstance` normalizes the repo path to absolute, sets `Status: Ready`, and records the requested branch in unexported `selectedBranch` without touching git or tmux (`session/instance.go:163`). The TUI creates this shell record on `KeyNew`/`KeyPrompt` (capped at 10 instances), holds a finalizer from `list.AddInstance`, and only finalizes it into the visible list after naming (`app/app.go:641`, `app/app.go:612`, `app/app.go:634`, `app/app.go:431`). The expensive `Start(true)` runs in a background `tea.Cmd` so the event loop stays responsive (`app/app.go:923`).

Run: `Start(true)` branches on `selectedBranch`: existing branch via `NewGitWorktreeFromBranch`, else fresh branch via `NewGitWorktree` (`session/instance.go:218`). It then runs worktree `Setup()` followed by `tmuxSession.Start(worktreePath)`, cleaning up the worktree if tmux fails and calling `Kill()` on any other setup error via a deferred handler (`session/instance.go:264`, `session/instance.go:237`). `Start` shells `tmux new-session -d -s <name> -c <workDir> <program>` inside a fresh PTY (`session/tmux/tmux.go:102-104`), polls `DoesSessionExist()` with exponential backoff against a 2 s timeout (`session/tmux/tmux.go:117-133`), then calls `Restore` (`session/tmux/tmux.go:148-154`).

Observe: output capture for previews, polling, and trust-prompt detection is `tmux capture-pane -p -e -J -t <name>`, with an `-S <start> -E <end>` variant for ranged scrollback (`session/tmux/tmux.go:476-484`, `session/tmux/tmux.go:488-496`). `HasUpdated` captures content, sets `hasPrompt` by program-specific substring, then compares SHA-256 hashes of full content to detect changes (`session/tmux/tmux.go:246-267`). Preview and diff are separate tabs inside `TabbedWindow` (`ui/tabbed_window.go:46`); only the active tab updates (`ui/tabbed_window.go:107,114,122`).

Review: the TUI review tab reads `Diff()` (`session/git/diff.go:26-52`), which runs `git add -N .` so untracked files appear, then `git --no-pager diff <baseCommitSHA>` and counts `+`/`-` lines excluding `+++`/`---` headers. `DiffNumstat()` (`session/git/diff.go:57-75`) runs `diff --numstat` and sums columns via `parseNumstat`, skipping binary `-/-` rows (`session/git/diff.go:80-98`).

Push / checkout / kill: `KeySubmit` (push) builds a timestamped `[claudesquad] update from '<title>'` commit message and calls `worktree.PushChanges(commitMsg, true)` — commit plus push for PR creation — without pausing or changing status (`app/app.go:716`). `KeyCheckout` shows the checkout help screen, then calls `selected.Pause()` and cleans up the terminal pane (`app/app.go:739`). `Kill()` always attempts both tmux `Close()` and worktree `Cleanup()`, collecting errors from both rather than short-circuiting, and is a no-op on never-started instances (`session/instance.go:288`).

## 6. Key Files
| File | Lines | What It Does |
|---|---|---|
| `main.go` | `main.go:27-78`, `main.go:80-115` | Cobra entry; git-repo guard, flag overrides, daemon branch, `reset` teardown |
| `app/app.go` | `app/app.go:27-35`, `app/app.go:51-104`, `app/app.go:106-152` | Bubble Tea `home` model, `Run`, `newHome` restore, key dispatch, View |
| `session/instance.go` | `session/instance.go:18-69`, `session/instance.go:163-282` | `Instance` struct, `Status` enum, `NewInstance`, `Start`, `Kill`/`Pause`/`Resume` |
| `session/storage.go` | `session/storage.go:11-42`, `session/storage.go:57-122` | `InstanceData` schema, save/load/delete whole-file JSON |
| `session/tmux/tmux.go` | `session/tmux/tmux.go:28-157`, `session/tmux/tmux.go:187-267` | Tmux session model, `Start`/`Restore`/`Close`, capture, prompt detection |
| `session/tmux/pty.go` | `session/tmux/pty.go:10-26` | `PtyFactory` interface; production impl over `creack/pty` |
| `session/git/worktree.go` | `session/git/worktree.go:49-78` | Worktree path resolution, branch construction and sanitization |
| `session/git/worktree_ops.go` | `session/git/worktree_ops.go:13-150`, `session/git/worktree_ops.go:170-236` | `Setup`, new/existing branch setup, `Cleanup`, `CleanupWorktrees` |
| `session/git/worktree_git.go` | `session/git/worktree_git.go:12-151`, `session/git/worktree_git.go:190-203` | Branch search, `IsDirty`, `CommitChanges`, `PushChanges`, `OpenBranchURL` |
| `session/git/diff.go` | `session/git/diff.go:8-98` | `Diff`, `DiffNumstat`, `parseNumstat` against pinned base SHA |
| `session/git/util.go` | `session/git/util.go:13-64` | Branch sanitization, `checkGHCLI`, `IsGitRepo` guards |
| `config/config.go` | `config/config.go:15-105`, `config/config.go:155-205` | Config dir/file, defaults, `GetProgram`/`GetProfiles`, load/save |
| `config/state.go` | `config/state.go:41-107`, `config/state.go:111-139` | `state.json` store, help bitmask, instance blob get/set/clear |
| `daemon/daemon.go` | `daemon/daemon.go:19-88`, `daemon/daemon.go:91-167` | Autoyes poll loop, `LaunchDaemon`/`StopDaemon`, pid file |
| `keys/keys.go` | `keys/keys.go:9-58`, `keys/keys.go:61-134` | `KeyName` enum, `GlobalKeyStringsMap`, help-text bindings |
| `ui/list.go` + `ui/tabbed_window.go` | `ui/list.go:56-172`, `ui/tabbed_window.go:33-127` | Session list rendering/selection; Preview/Diff/Terminal tabs |

## 7. Dependencies
| Package | Version constraint | Purpose from go.mod verbatim |
|---|---|---|
| `github.com/charmbracelet/bubbletea` | `v1.3.4` (`go.mod:9-11`) | TUI rendering and interaction |
| `github.com/charmbracelet/bubbles` | `v0.20.0` (`go.mod:9-11`) | TUI rendering and interaction |
| `github.com/charmbracelet/lipgloss` | `v1.0.0` (`go.mod:9-11`) | TUI rendering and interaction |
| `github.com/creack/pty` | `v1.1.24` (`go.mod:12-20`) | Terminal isolation (PTY) |
| `golang.org/x/term` | `v0.30.0` (`go.mod:12-20`) | Terminal isolation |
| `github.com/spf13/cobra` | `v1.9.1` (`go.mod:17`) | CLI parsing |
| `golang.org/x/sys` | pinned in `go.mod:12-20` | Terminal isolation support |
| indirect (Charm transitive, cobra transitive) | pinned in `go.mod:7-21` | Transitive deps of TUI/CLI stack (versions in go.mod lock, not enumerated in wiki) |

Module and toolchain pins are `module claude-squad`, `go 1.23.0`, `toolchain go1.25.8` (`go.mod:1-5`). Prerequisites outside Go modules are `tmux` and `gh` (`README.md:47-50`).

## 8. CLI / Usage Surface
Entry points: `app.Run(ctx, program, autoYes)` in `app/app.go:27-35` constructs a Bubble Tea program around `newHome` with alt-screen and mouse-cell-motion; `newHome` in `app/app.go:106-152` loads config, state, storage, and restores persisted instances. `daemon.RunDaemon(cfg)` in `main.go:35-40` is the hidden `--daemon` submode. All `os/exec` invocation passes through the `Executor` interface in `cmd/cmd.go:8-11`, with production implementation `Exec` in `cmd/cmd.go:13-21`.

Commands:
```
cs [-p <program>] [-y]        # root TUI; must run inside git repo
cs reset                      # delete storage rows + kill tmux + remove worktrees + stop daemon
cs debug                      # print resolved config path + indented JSON config
cs version                    # print binName + version 1.0.20 + release URL
cs completion                 # cobra shell completion (listed in README.md:54-70)
cs --daemon                   # hidden internal flag; runs daemon instead of TUI
```

| Env var | Used as |
|---|---|
| `HOME` | Resolves `~/.claude-squad/` config dir (`config/config.go:15-27`) |
| `SHELL` | Fallback shell for terminal pane (`/bin/sh` if unset) (`ui/terminal.go:146-152`) |
| `TMPDIR` / temp dir | `os.TempDir()/claudesquad.log` log file (`log/log.go:17`) |
| (no dedicated `CLAUDESQUAD_*` vars) | Configured via flags + `config.json`, not environment |

| Config file | Path | What it holds |
|---|---|---|
| `config.json` | `~/.claude-squad/config.json` (`config/config.go:15-27`) | `default_program`, `auto_yes`, `daemon_poll_interval`, `branch_prefix`, `profiles` |
| `state.json` | `<configDir>/state.json` (`config/state.go:41`) | `help_screens_seen` bitmask + raw `instances` JSON blob |
| `daemon.pid` | `<configDir>/daemon.pid` (`daemon/daemon.go:115-167`) | Running daemon PID for stop/launch coordination |
| `worktrees/` | `<configDir>/worktrees/` (`session/git/worktree.go:11-18`) | One subdirectory per instance |

## 9. Extensibility Points
- **New harness:** no code change needed for launch — add `{name, program}` to `profiles` in `config.json` (`config/config.go:29-33`, `config/config.go:61-82`, `README.md:117-141`). Only add Go constants if prompt/trust detection is needed, following `ProgramClaude`/`ProgramAider`/`ProgramGemini` in `session/tmux/tmux.go:22-25` and branches in `session/tmux/tmux.go:161-184`, `session/tmux/tmux.go:253-260`.
- **New keybinding:** add entry to `GlobalKeyStringsMap` in `keys/keys.go:38-58`, add dispatch arm in `handleKeyPress` switch in `app/app.go:609-814`, update help in `app/help.go:36-60` and menu in `ui/menu.go:78-154`.
- **New overlay:** add model under `ui/overlay/` following `TextInputOverlay` (`ui/overlay/textInput.go:35`), `BranchPicker` (`ui/overlay/branchPicker.go:15`), or `ConfirmationOverlay` (`ui/overlay/confirmationOverlay.go:9`); render through `PlaceOverlay` (`ui/overlay/overlay.go:47`); wire state in `app/app.go:51-104` and `View` (`app/app.go:1045-1072`).
- **New session op:** add method on `Instance` in `session/instance.go:32` (follow `Pause` at `session/instance.go:423` / `Resume` at `session/instance.go:510` / `Kill` at `session/instance.go:288`), add TUI handler in `app/app.go:677-791`, gate with `confirmAction` as push/kill do (`app/app.go:737`, `app/app.go:714`).
- **New preview/tab:** extend `TabbedWindow` in `ui/tabbed_window.go:46-70`, add tab id alongside `PreviewTab`/`DiffTab`/`TerminalTab` (`ui/tabbed_window.go:33-37`), gate updates like `UpdatePreview`/`UpdateDiff` (`ui/tabbed_window.go:107-127`).

## 10. Limitations and Gotchas
- **Load aborts on first bad row:** `LoadInstances` returns on the first `FromInstanceData` error and `newHome` exits (`session/storage.go:83`, `app/app.go:136`) — one corrupt row hides all instances.
- **Corrupt state file is fatal:** missing/unparseable `state.json` defaults to `[]` at the store layer (`config/state.go:57`, `config/state.go:90`), but a bad instance row at load time triggers `os.Exit(1)` (`app/app.go:136`).
- **No LookPath guard on tmux:** every primitive runs `exec.Command("tmux", ...)` with no preflight check (`session/tmux/tmux.go:22-25`, `session/tmux/tmux.go:102`); missing tmux surfaces as spawn timeout or exec error, not a clear prerequisite message.
- **Unstarted rows never persisted:** `Storage.SaveInstances` skips unstarted instances (`session/storage.go:57`); Esc or prompt-cancel on an unstarted row kills it without persisting (`app/app.go:468`, `app/app.go:1003`).
- **Hard cap of 10 instances:** `GlobalInstanceLimit = 10` (`app/app.go:24`), enforced at both creation sites (`app/app.go:613-615`, `app/app.go:642-644`); no queue or overflow handling.
- **Detach panics on failure:** `Detach` closes the PTY then re-`Restore`s, and both close and re-attach failures `panic` (`session/tmux/tmux.go:401-416`); use `DetachSafely` for the error-returning path (`session/tmux/tmux.go:347-385`).
- **Windows support is degraded:** resize uses 250 ms polling instead of `SIGWINCH` (`session/tmux/tmux_windows.go:30-56` vs `session/tmux/tmux_unix.go:16-64`); daemon detach uses `CREATE_NEW_PROCESS_GROUP | DETACHED_PROCESS` vs Unix `Setsid` (`daemon/daemon_windows.go:11-14`, `daemon/daemon_unix.go:10-13`).
- **Must run inside git repo:** startup is rejected outside a git repository by `filepath.Abs(".")` plus `git.IsGitRepo` (`main.go:42-50`); empty repos abort with "please create an initial commit" (`session/git/worktree_ops.go:92-99`).

## 11. How It Compares to Alternatives
- **Plain git worktree CLI workflows** (`git worktree add -b`, manual branches, manual `gh` push) give the same filesystem isolation with zero dependencies and full control. They lack process isolation, live previews, diff tabs, and single-key pause/resume/push, so every session is manual terminal management. Position: use raw worktrees when you need one branch, use Claude Squad when you need ten agents visible at once.
- **Tmux session managers (tmuxp, tmuxinator, raw tmux)** give stronger terminal multiplexing, layouts, and scripting than Claude Squad's one-session-per-agent model. They know nothing about git worktrees, branch-per-agent isolation, diff review, or agent prompt detection, so the operator wires isolation by hand. Position: use tmuxp for reproducible terminal layouts, use Claude Squad for agent-to-branch binding.
- **Fleet (multi-agent orchestrator with bead DB and coder workers)** adds what Claude Squad deliberately omits: task decomposition, phased pipelines, worker registry, and orchestration above the execution floor. Claude Squad's lesson for Fleet is that the floor needs almost no abstraction — one tmux session plus one worktree per worker, JSON reconciled against live tmux, single-key ops. Position: use Claude Squad as the interactive single-operator console, use Fleet when runs must span workers with dependencies.
- **Claude Code subagents / IDE multi-agent panels** keep orchestration inside one agent runtime with structured handoffs and shared context. They avoid tmux/worktree plumbing entirely but couple you to one harness and one checkout, with weaker process-level isolation and no harness-agnostic CLI slot. Position: use subagents for single-harness decomposed tasks, use Claude Squad for harness-agnostic parallel CLIs with hard filesystem isolation.

## Appendix: Selected Code Snippets
### Tmux session spawn with existence guard
```go
// session/tmux/tmux.go:101-125
	// Create a new detached tmux session and start claude in it
	cmd := exec.Command("tmux", "new-session", "-d", "-s", t.sanitizedName, "-c", workDir, t.program)

	ptmx, err := t.ptyFactory.Start(cmd)
	if err != nil {
		// Cleanup any partially created session if any exists.
		if t.DoesSessionExist() {
			cleanupCmd := exec.Command("tmux", "kill-session", "-t", t.sanitizedName)
			if cleanupErr := t.cmdExec.Run(cleanupCmd); cleanupErr != nil {
				err = fmt.Errorf("%v (cleanup error: %v)", err, cleanupErr)
			}
		}
		return fmt.Errorf("error starting tmux session: %w", err)
	}

	// Poll for session existence with exponential backoff
	timeout := time.After(2 * time.Second)
	sleepDuration := 5 * time.Millisecond
	for !t.DoesSessionExist() {
		select {
		case <-timeout:
```

### Prompt-aware change polling via capture-pane hash
```go
// session/tmux/tmux.go:246-267
func (t *TmuxSession) HasUpdated() (updated bool, hasPrompt bool) {
	content, err := t.CapturePaneContent()
	if err != nil {
		log.ErrorLog.Printf("error capturing pane content in status monitor: %v", err)
		return false, false
	}

	// Only set hasPrompt for claude and aider. Use these strings to check for a prompt.
	if t.program == ProgramClaude {
		hasPrompt = strings.Contains(content, "No, and tell Claude what to do differently")
	} else if strings.HasPrefix(t.program, ProgramAider) {
		hasPrompt = strings.Contains(content, "(Y)es/(N)o/(D)on't ask again")
	} else if strings.HasPrefix(t.program, ProgramGemini) {
		hasPrompt = strings.Contains(content, "Yes, allow once")
	}

	if !bytes.Equal(t.monitor.hash(content), t.monitor.prevOutputHash) {
		t.monitor.prevOutputHash = t.monitor.hash(content)
		return true, hasPrompt
	}
	return false, hasPrompt
}
```

### Diff against pinned base commit with intent-to-add
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
