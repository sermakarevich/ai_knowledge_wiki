> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Tmux Backend and Autoyes Daemon
**In one sentence:** All agent execution happens inside named tmux sessions driven via tmux CLI (Command-Line Interface); an optional background daemon polls those sessions and injects accept-keys for autoyes mode.

## Key points
- Each instance maps 1:1 to a tmux session whose name is `claudesquad_` + sanitized instance title (whitespace stripped, `.` replaced with `_`), stored as `sanitizedName` on `TmuxSession` (`session/tmux/tmux.go:60`, `session/tmux/tmux.go:68-72`, `session/tmux/tmux.go:84-91`).
- Lifecycle primitives shell out to the tmux binary: `tmux new-session -d -s <name> -c <workdir> <program>` to create (`session/tmux/tmux.go:102`), `tmux attach-session -t <name>` over a PTY (pseudo-terminal) to connect (`session/tmux/tmux.go:195`), `tmux has-session -t=<name>` for exact-match existence checks (`session/tmux/tmux.go:469-473`), and `tmux kill-session -t <name>` to destroy (`session/tmux/tmux.go:434`).
- Output capture for previews, polling, and trust-prompt detection is `tmux capture-pane -p -e -J -t <name>`, with an `-S <start> -E <end>` variant for ranged scrollback (`session/tmux/tmux.go:476-484`, `session/tmux/tmux.go:488-496`); prompt detection hashes content with SHA-256 (Secure Hash Algorithm) and matches per-program strings (`session/tmux/tmux.go:204-267`).
- PTY handling is abstracted behind a `PtyFactory` interface backed by `creack/pty` (`session/tmux/pty.go:10-26`); resize handling is platform-split with build tags — Unix uses debounced `SIGWINCH` signals (`session/tmux/tmux_unix.go:1`, `session/tmux/tmux_unix.go:16-64`), Windows polls terminal size every 250 ms (`session/tmux/tmux_windows.go:1`, `session/tmux/tmux_windows.go:30-56`).
- `CleanupSessions` lists via `tmux ls`, treats exit code 1 as "no server, nothing to do", regex-matches `claudesquad_.*:` session names, and kills each match (`session/tmux/tmux.go:499-526`); it is invoked by the `reset` command (`main.go:97-99`).
- The autoyes daemon (`daemon/daemon.go:19-88`) loads all stored instances, forces `AutoYes=true`, and on each `DaemonPollInterval` tick calls `HasUpdated()` and `TapEnter()` on started, unpaused instances showing a prompt; `main.go` runs it as `--daemon` (`main.go:35-40`), stops any running daemon before the TUI (terminal user interface) starts (`main.go:72-74`), launches a new detached copy on exit when autoyes is on (`main.go:64-69`), and stops it on `reset` (`main.go:108-110`); detach uses `Setsid` on Unix (`daemon/daemon_unix.go:10-13`) vs `CREATE_NEW_PROCESS_GROUP | DETACHED_PROCESS` on Windows (`daemon/daemon_windows.go:11-14`), coordinated through a `daemon.pid` file (`daemon/daemon.go:115-167`).
- Hard requirements are the `tmux` binary on `PATH` (no `LookPath` guard; every primitive `exec.Command("tmux", ...)` fails if absent) plus per-agent CLIs (Command-Line Interfaces) such as `claude`/`aider`/`gemini` (`session/tmux/tmux.go:22-25`, `session/tmux/tmux.go:102`); `install.sh` installs tmux via brew/apt/dnf/yum (`install.sh:181-214`); `keys/keys.go` only defines TUI list-navigation bindings and plays no role in tmux key injection (`keys/keys.go:38-58`, `keys/keys.go:61-134`).

---
## Session model and naming
`TmuxSession` (`session/tmux/tmux.go:28-58`) holds the sanitized tmux name, the agent program string, injectable `ptyFactory` and `cmdExec` dependencies, a persistent `ptmx` handle to an attached PTY, a `statusMonitor` hash cache, and attach-scoped state (`attachCh`, `ctx`/`cancel`, `wg`). Naming is deterministic: `TmuxPrefix = "claudesquad_"` (`session/tmux/tmux.go:60`) plus `toClaudeSquadTmuxName`, which strips all whitespace, maps `.` to `_` (mirroring tmux behavior), and prepends the prefix (`session/tmux/tmux.go:68-72`). Constructors `NewTmuxSession` / `NewTmuxSessionWithDeps` / `newTmuxSession` only fill name, program, and dependencies; the PTY is created later by `Start` or `Restore` (`session/tmux/tmux.go:75-91`). Sanitization is pinned by `TestSanitizeName` (`session/tmux/tmux_test.go:44-50`).

```go
// session/tmux/tmux.go:60-72
const TmuxPrefix = "claudesquad_"
// ...
var whiteSpaceRegex = regexp.MustCompile(`\s+`)

func toClaudeSquadTmuxName(str string) string {
	str = whiteSpaceRegex.ReplaceAllString(str, "")
	str = strings.ReplaceAll(str, ".", "_") // tmux replaces all . with _
	return fmt.Sprintf("%s%s", TmuxPrefix, str)
}
```

## Create/attach/kill
`Start(workDir)` (`session/tmux/tmux.go:95-157`) rejects already-existing sessions (`session/tmux/tmux.go:97-99`), runs `tmux new-session -d -s <name> -c <workDir> <program>` inside a fresh PTY (`session/tmux/tmux.go:102-104`), polls `DoesSessionExist()` with exponential backoff (5 ms doubling to 50 ms cap) against a 2 s timeout (`session/tmux/tmux.go:117-133`), closes the throwaway PTY, sets `history-limit 10000` and `mouse on` with warnings-only failure (`session/tmux/tmux.go:137-146`), then calls `Restore` (`session/tmux/tmux.go:148-154`). `Restore` (`session/tmux/tmux.go:187-202`) first checks existence so a dead tmux server surfaces as `ErrSessionNotFound` instead of a phantom attach (`session/tmux/tmux.go:191-193`, error defined at `session/tmux/tmux.go:62-64`), then starts `tmux attach-session -t <name>` in a PTY and allocates a fresh `statusMonitor` (`session/tmux/tmux.go:195-201`). `Close` (`session/tmux/tmux.go:424-451`) closes the PTY and runs `tmux kill-session -t <name>`, aggregating both errors (`session/tmux/tmux.go:427-450`). `DoesSessionExist` uses `tmux has-session -t=<name>`; the `=` forces exact match because bare `-t` prefix-matches (`session/tmux/tmux.go:469-473`).

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

```go
// session/tmux/tmux.go:187-202
func (t *TmuxSession) Restore() error {
	// attach-session against a missing session still forks a process successfully, so the
	// PTY start below would report no error while leaving us attached to nothing. Check
	// first so callers can tell "session is gone" apart from "PTY failed".
	if !t.DoesSessionExist() {
		return ErrSessionNotFound
	}

	ptmx, err := t.ptyFactory.Start(exec.Command("tmux", "attach-session", "-t", t.sanitizedName))
	if err != nil {
		return fmt.Errorf("error opening PTY: %w", err)
	}
	t.ptmx = ptmx
	t.monitor = newStatusMonitor()
	return nil
}
```

Interactive `Attach` (`session/tmux/tmux.go:269-344`) wires `ptmx` to stdout via `io.Copy` (`session/tmux/tmux.go:283`), forwards stdin to the PTY except for the first ~50 ms of bytes (nuked as terminal reply-sequence garbage, `session/tmux/tmux.go:316-328`), and treats single-byte `0x11` (Ctrl-Q) as detach (`session/tmux/tmux.go:331-334`). Abnormal PTY EOF (e.g. Ctrl-D) prints a red warning telling the user to use Ctrl-Q (`session/tmux/tmux.go:287-294`). `Detach` (`session/tmux/tmux.go:389-421`) closes the PTY, re-`Restore`s a background PTY to preserve the always-valid-`ptmx` invariant, then cancels goroutines; both close and re-attach failures `panic` (`session/tmux/tmux.go:401-416`). `DetachSafely` (`session/tmux/tmux.go:347-385`) is the non-panicking variant returning aggregated errors.

## Output capture
`CapturePaneContent` runs `tmux capture-pane -p -e -J -t <name>` where `-p` prints to stdout, `-e` preserves ANSI (American National Standards Institute) escape sequences, `-J` joins wrapped lines (`session/tmux/tmux.go:476-484`). `CapturePaneContentWithOptions(start, end)` adds `-S <start> -E <end>` for scrollback windows (`session/tmux/tmux.go:488-496`). Consumers: preview panes, `HasUpdated` polling, and `CheckAndHandleTrustPrompt` (`session/tmux/tmux.go:161-184`), which auto-accepts Claude "Do you trust the files in this folder?"/"new MCP server" prompts with Enter and other agents' "Open documentation url" prompt with `D`+Enter. `HasUpdated` (`session/tmux/tmux.go:246-267`) captures content, sets `hasPrompt` by program-specific substring (`"No, and tell Claude what to do differently"` for claude at `session/tmux/tmux.go:255`, `"(Y)es/(N)o/(D)on't ask again"` for aider at `session/tmux/tmux.go:257`, `"Yes, allow once"` for gemini at `session/tmux/tmux.go:259`), then compares SHA-256 hashes of full content to detect changes (`session/tmux/tmux.go:262-266`, hasher at `session/tmux/tmux.go:214-219`).

```go
// session/tmux/tmux.go:475-496
func (t *TmuxSession) CapturePaneContent() (string, error) {
	// Add -e flag to preserve escape sequences (ANSI color codes)
	cmd := exec.Command("tmux", "capture-pane", "-p", "-e", "-J", "-t", t.sanitizedName)
	output, err := t.cmdExec.Output(cmd)
	if err != nil {
		return "", fmt.Errorf("error capturing pane content: %v", err)
	}
	return string(output), nil
}

// CapturePaneContentWithOptions captures the pane content with additional options
// start and end specify the starting and ending line numbers (use "-" for the start/end of history)
func (t *TmuxSession) CapturePaneContentWithOptions(start, end string) (string, error) {
	// Add -e flag to preserve escape sequences (ANSI color codes)
	cmd := exec.Command("tmux", "capture-pane", "-p", "-e", "-J", "-S", start, "-E", end, "-t", t.sanitizedName)
	output, err := t.cmdExec.Output(cmd)
	if err != nil {
		return "", fmt.Errorf("failed to capture tmux pane content with options: %v", err)
	}
	return string(output), nil
}
```

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

## PTY and platform split
All PTY creation goes through the `PtyFactory` interface (`Start`, `Close`) so tests can substitute file-backed fakes (`session/tmux/pty.go:10-13`, mock at `session/tmux/tmux_test.go:18-42`); production `Pty.Start` delegates to `creack/pty.pty.Start` (`session/tmux/pty.go:18-20`). Resize propagation writes the terminal size into the attached PTY via `pty.Setsize` (`session/tmux/tmux.go:460-467`), exposed as `SetDetachedSize` for detached preview shaping (`session/tmux/tmux.go:453-457`). The watcher `monitorWindowSize` has two build-tagged implementations: Unix (`//go:build !windows`, `session/tmux/tmux_unix.go:1`) subscribes to `SIGWINCH`, fires an initial synthetic `SIGWINCH`, debounces at 50 ms, and throttles error logs to one per 60 s (`session/tmux/tmux_unix.go:16-78`); Windows (`//go:build windows`, `session/tmux/tmux_windows.go:1`) sizes once up front then polls `term.GetSize` on a 250 ms ticker and pushes only on change (`session/tmux/tmux_windows.go:14-57`). `TestStartTmuxSession` pins the exact CLI strings for create and attach (`session/tmux/tmux_test.go:52-88`).

## CleanupSessions
`CleanupSessions(cmdExec)` (`session/tmux/tmux.go:499-526`) runs `tmux ls` (`session/tmux/tmux.go:501`); an `*exec.ExitError` with code 1 means no tmux server and returns nil (`session/tmux/tmux.go:507-508`); any other error is wrapped (`session/tmux/tmux.go:510`). It regex-extracts `claudesquad_.*:` tokens and trims the trailing colon (`session/tmux/tmux.go:513-517`), then `tmux kill-session -t <match>` per session, aborting with an error on first kill failure (`session/tmux/tmux.go:519-524`). Note the stale comment at `session/tmux/tmux.go:498` says `session-` while the code matches `claudesquad_`. Entry point is the `reset` command alongside storage and worktree cleanup (`main.go:97-110`).

## The autoyes daemon
`RunDaemon` (`daemon/daemon.go:19-88`) is the `--daemon` submode of the same binary (`main.go:35-40`): it loads persisted state, opens `session.Storage`, loads instances, and unconditionally sets `instance.AutoYes = true` (`daemon/daemon.go:21-34`). It then ticks every `cfg.DaemonPollInterval` milliseconds (`daemon/daemon.go:36-46`); each tick iterates the snapshot instance list and for every `Started()` and un-`Paused()` instance calls `HasUpdated()` and, if `hasPrompt`, `TapEnter()` plus `UpdateDiffStats()` with 60 s-throttled warning logs (`daemon/daemon.go:48-60`). Shutdown waits on `SIGINT`/`SIGTERM`, stops the ticker goroutine via `stopCh`, then persists instances (`daemon/daemon.go:74-87`). Lifecycle from the foreground process: kill any inherited daemon before the TUI starts (`main.go:72-74`); if autoyes is enabled, `defer LaunchDaemon()` so a fresh daemon spawns after the TUI exits (`main.go:64-69`); `reset` stops the daemon (`main.go:108-110`).

```go
// daemon/daemon.go:44-72
	go func() {
		defer wg.Done()
		ticker := time.NewTimer(pollInterval)
		for {
			for _, instance := range instances {
				// We only store started instances, but check anyway.
				if instance.Started() && !instance.Paused() {
					if _, hasPrompt := instance.HasUpdated(); hasPrompt {
						instance.TapEnter()
						if err := instance.UpdateDiffStats(); err != nil {
							if everyN.ShouldLog() {
								log.WarningLog.Printf("could not update diff stats for %s: %v", instance.Title, err)
							}
						}
					}
				}
			}

			// Handle stop before ticker.
			select {
			case <-stopCh:
				return
			default:
			}

			<-ticker.C
			ticker.Reset(pollInterval)
		}
	}()
```

`LaunchDaemon` (`daemon/daemon.go:91-127`) re-execs the current binary as `<self> --daemon` (`daemon/daemon.go:93-98`), nulls stdio, applies `getSysProcAttr()` detachment (`daemon/daemon.go:101-106`), starts without waiting, and records the PID in `<configDir>/daemon.pid` (`daemon/daemon.go:108-126`). `StopDaemon` (`daemon/daemon.go:131-167`) reads that PID file (missing file = success no-op, `daemon/daemon.go:140-142`), parses the PID, `FindProcess`+`Kill`, and removes the PID file (`daemon/daemon.go:146-166`). Detachment attributes are platform-split: Unix `Setsid: true` (`daemon/daemon_unix.go:10-13`) vs Windows `CREATE_NEW_PROCESS_GROUP | DETACHED_PROCESS` (`daemon/daemon_windows.go:11-14`).

```go
// daemon/daemon.go:91-112
func LaunchDaemon() error {
	// Find the claude squad binary.
	execPath, err := os.Executable()
	if err != nil {
		return fmt.Errorf("failed to get executable path: %w", err)
	}

	cmd := exec.Command(execPath, "--daemon")

	// Detach the process from the parent
	cmd.Stdin = nil
	cmd.Stdout = nil
	cmd.Stderr = nil

	// Set process group to prevent signals from propagating
	cmd.SysProcAttr = getSysProcAttr()

	if err := cmd.Start(); err != nil {
		return fmt.Errorf("failed to start child process: %w", err)
	}
```

## Key injection
Foreground key injection writes raw bytes into the attached PTY: `TapEnter` writes `0x0D` (`session/tmux/tmux.go:222-228`), `TapDAndEnter` writes `0x44, 0x0D` (`session/tmux/tmux.go:231-237`), `SendKeys` writes an arbitrary string (`session/tmux/tmux.go:239-242`). The daemon path delegates through the instance object (`instance.TapEnter()` at `daemon/daemon.go:52`), which forwards to the session PTY. `keys/keys.go` is unrelated to this wire path: it defines the Bubble Tea TUI's `KeyName` enum (`keys/keys.go:9-35`), the string-to-action map for list navigation (`keys/keys.go:38-58`), and the help-text bindings (`keys/keys.go:61-134`); the tmux-context Ctrl-Q detach key is hardcoded in `Attach`, not registered there (`session/tmux/tmux.go:331-334`).

## Failure modes incl. "timed out waiting for tmux session" FAQ
- `timed out waiting for tmux session <name>` (`session/tmux/tmux.go:125`) means `new-session` did not materialize within 2 s; `Start` then calls `Close` (killing the half-created session) and wraps both errors (`session/tmux/tmux.go:122-125`). Causes: missing/slow tmux server, bad `workDir`, or unknown `program` binary.
- `tmux session already exists` (`session/tmux/tmux.go:98`) means a stale session with the same sanitized name survived a crash; fix with `reset` (`CleanupSessions`, `session/tmux/tmux.go:499-526`) or manual `tmux kill-session`.
- `ErrSessionNotFound` (`session/tmux/tmux.go:62-64`) surfaces when the tmux server died (reboot, crash, `tmux kill-server`) between existence check and attach; `Restore` pre-checks explicitly because `attach-session` forks successfully even against a missing session (`session/tmux/tmux.go:188-193`, regression test at `session/tmux/tmux_test.go:93-109`).
- Partial-start cleanup failures are chained as `(cleanup error: %v)` (`session/tmux/tmux.go:109-111`, `session/tmux/tmux.go:150-152`); detached history/mouse option failures only log warnings (`session/tmux/tmux.go:138-146`).
- `Detach` panics if PTY close or re-`Restore` fails (`session/tmux/tmux.go:401-416`); use `DetachSafely` for the error-returning path (`session/tmux/tmux.go:347-385`).
- Exit code 1 from `tmux ls` inside `CleanupSessions` is normal (no server running), not an error (`session/tmux/tmux.go:507-508`).

**Covers:** session/tmux/tmux.go, session/tmux/pty.go, session/tmux/tmux_unix.go, session/tmux/tmux_windows.go, daemon/daemon.go, daemon/daemon_unix.go, daemon/daemon_windows.go, keys/keys.go