> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Architecture and Entry Points
**In one sentence:** Claude Squad is a Bubble Tea TUI that fans out agent CLIs into tmux sessions bound to git worktrees, entered via a cobra root command in `main.go`.
## Key points
- The binary enters through cobra `rootCmd.RunE` in `main.go:30-77`, which initializes logging, branches on `--daemon`, enforces a git-repo guard, resolves the agent program, then calls `app.Run`. `main.go:30-77`
- Startup is rejected outside a git repository by `filepath.Abs(".")` plus `git.IsGitRepo` in `main.go:42-50`; the binary name in the error derives from `os.Args[0]` in `main.go:167-175`. `main.go:42-50`
- `--daemon` is a hidden internal flag (`main.go:153-160`) that routes to `daemon.RunDaemon(cfg)` in `main.go:35-40` instead of the TUI; `--autoyes/-y` and `--program/-p` override config in `main.go:52-63`. `main.go:35-40`
- Auto-yes mode side-effects daemon lifecycle: it defers `daemon.LaunchDaemon()` in `main.go:64-70` and unconditionally calls `daemon.StopDaemon()` before `app.Run` in `main.go:71-74`. `main.go:64-74`
- All `os/exec` invocation passes through the `Executor` interface in `cmd/cmd.go:8-11`, with production implementation `Exec` in `cmd/cmd.go:13-21` and constructor `MakeExecutor()` in `cmd/cmd.go:23-25`. `cmd/cmd.go:8-25`
- `app.Run(ctx, program, autoYes)` in `app/app.go:27-35` constructs a Bubble Tea program around `newHome` with alt-screen and mouse-cell-motion; `newHome` in `app/app.go:106-152` loads config, state, storage, and restores persisted instances. `app/app.go:27-35`
- The module is `claude-squad` on `go 1.23.0` / `toolchain go1.25.8` (`go.mod:1-5`); direct dependencies are Charm TUI stack, `spf13/cobra`, `creack/pty`, and `golang.org/x/sys|term` (`go.mod:7-21`). `go.mod:1-21`
---
## Entry flow (main.go)
Root command definition and dispatch live in `main.go:27-78`. Verbatim:
```go
rootCmd     = &cobra.Command{
    Use:   "claude-squad",
    Short: "Claude Squad - Manage multiple AI agents like Claude Code, Aider, Codex, and Amp.",
    RunE: func(cmd *cobra.Command, args []string) error {
        ctx := context.Background()
        log.Initialize(daemonFlag)
        defer log.Close()

        if daemonFlag {
            cfg := config.LoadConfig()
            err := daemon.RunDaemon(cfg)
            log.ErrorLog.Printf("failed to start daemon %v", err)
            return err
        }

        // Check if we're in a git repository
        currentDir, err := filepath.Abs(".")
        if err != nil {
            return fmt.Errorf("failed to get current directory: %w", err)
        }

        if !git.IsGitRepo(currentDir) {
            return fmt.Errorf("error: %s must be run from within a git repository", binName)
        }

        cfg := config.LoadConfig()

        // Program flag overrides config
        program := cfg.GetProgram()
        if programFlag != "" {
            program = programFlag
        }
        // AutoYes flag overrides config
        autoYes := cfg.AutoYes
        if autoYesFlag {
            autoYes = true
        }
        if autoYes {
            defer func() {
                if err := daemon.LaunchDaemon(); err != nil {
                    log.ErrorLog.Printf("failed to launch daemon: %v", err)
                }
            }()
        }
        // Kill any daemon that's running.
        if err := daemon.StopDaemon(); err != nil {
            log.ErrorLog.Printf("failed to stop daemon: %v", err)
        }

        return app.Run(ctx, program, autoYes)
    },
}
```
Flag registration rewrites `rootCmd.Use` from the invoked binary name so `cs` and `claude-squad` share one implementation (`main.go:167-175`). `main.go:167-175` CLI flags are `--program/-p`, `--autoyes/-y`, and hidden `--daemon` (`main.go:148-160`). `main.go:148-160`
## The Executor seam (cmd/cmd.go)
`cmd` isolates process execution behind two methods (`cmd/cmd.go:8-11`). Verbatim:
```go
type Executor interface {
    Run(cmd *exec.Cmd) error
    Output(cmd *exec.Cmd) ([]byte, error)
}
```
```go
func MakeExecutor() Executor {
    return Exec{}
}
```
`Exec.Run` delegates to `cmd.Run` and `Exec.Output` to `cmd.Output` (`cmd/cmd.go:13-21`). `cmd/cmd.go:13-21` `ToString` joins `cmd.Args` for logging, with nil guard (`cmd/cmd.go:27-32`). `cmd/cmd.go:27-32` Callers such as `resetCmd` pass `cmd2.MakeExecutor()` into `tmux.CleanupSessions` (`main.go:97`). `main.go:97`
## Commands: reset / debug / version
`resetCmd` in `main.go:80-115` deletes all stored instances via `session.NewStorage`, then cleans tmux sessions with `MakeExecutor()`, cleans worktrees, and stops the daemon (`main.go:87-111`). `main.go:80-115` `debugCmd` in `main.go:117-136` prints the resolved config path and indented JSON config (`main.go:124-134`). `main.go:117-136` `versionCmd` in `main.go:138-145` prints `binName` plus hardcoded `version = "1.0.20"` (`main.go:21-22`) and a release URL (`main.go:141-144`). `main.go:138-145` Commands are registered in `init()` (`main.go:162-164`). `main.go:162-164` Public usage surface documented in `README.md:54-70` lists `completion|debug|help|reset|version` plus `-y/-p` flags (`README.md:54-70`). `README.md:54-70`
## Dependency stack (go.mod)
Module and toolchain pins are `module claude-squad`, `go 1.23.0`, `toolchain go1.25.8` (`go.mod:1-5`). `go.mod:1-5` TUI rendering and interaction come from `bubbletea v1.3.4`, `bubbles v0.20.0`, `lipgloss v1.0.0` (`go.mod:9-11`). `go.mod:9-11` CLI parsing is `cobra v1.9.1` (`go.mod:17`). `go.mod:17` Terminal isolation uses `creack/pty v1.1.24` plus `golang.org/x/term v0.30.0` (`go.mod:12-20`). `go.mod:12-20` Prerequisites outside Go modules are `tmux` and `gh` (`README.md:47-50`). `README.md:47-50` Default agent program is `claude`, overridable per-invocation (`README.md:72-87`) or per-profile via `default_program`/`profiles` (`README.md:117-141`). `README.md:72-87`
## End-to-end data flow
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
The split is stated as design in `README.md:150-154`: tmux for session isolation, worktrees for codebase isolation, TUI for management (`README.md:150-154`). `README.md:150-154` `home` holds `storage`, `appConfig`, `appState`, `list`, `menu`, `tabbedWindow`, `errBox`, and overlays (`app/app.go:51-104`). `app/app.go:51-104` Event flow uses Bubble Tea messages including `previewTickMsg`, `instanceStartedMsg`, `instanceStartDoneMsg`, `metadataUpdateDoneMsg`, `branchSearchResultMsg` (`app/app.go:853-921`). `app/app.go:853-921` Instance creation is capped by `GlobalInstanceLimit = 10` (`app/app.go:24`), enforced at `app/app.go:613-615` and `app/app.go:642-644`. `app/app.go:24`
### New-session path
1. User runs `cs [-p <program>] [-y]` inside a git repo; `rootCmd` validates repo and resolves `program`/`autoYes` (`main.go:42-63`). `main.go:42-63`
2. `app.Run` starts the `home` model; `newHome` restores existing instances from storage (`app/app.go:106-152`). `app/app.go:106-152`
3. `n`/`N` key creates a `session.Instance` bound to a new git worktree/branch for filesystem isolation (`README.md:150-154`). `README.md:150-154`
4. The instance starts inside its own tmux session running the selected agent CLI (`README.md:81-87`). `README.md:81-87`
5. TUI polls previews and metadata via `previewTickMsg` and background `instanceStartCmd`/`metadataUpdate` commands (`app/app.go:183-194`). `app/app.go:183-194`
6. Quit/persist leaves tmux and worktrees intact; `cs reset` tears down storage, tmux sessions, worktrees, and daemon (`main.go:80-115`). `main.go:80-115`
**Covers:** main.go, cmd/cmd.go, go.mod, README.md, app/app.go (structural surface only)
