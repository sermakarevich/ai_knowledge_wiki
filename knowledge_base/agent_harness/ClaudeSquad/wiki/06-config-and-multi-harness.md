> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Config, Profiles, and Multi-Harness Support
**In one sentence:** Multi-harness support is a plain shell-command string — `default_program` plus an optional named `profiles` array, resolved by `GetProgram()` and launched verbatim as the command argument of `tmux new-session` — with zero per-harness adapter classes or plugin interfaces anywhere in the codebase.

## Key points
- Config lives at `~/.claude-squad/config.json` (`ConfigFileName`, `GetConfigDir`), holding `default_program`, `auto_yes`, `daemon_poll_interval`, `branch_prefix`, and an optional `profiles` array — there is no per-harness section or adapter registry (`config/config.go:16-27`, `config/config.go:36-47`, `config/config.go:155-185`).
- `default_program` is either a literal shell command (`"aider --model ..."`) or a profile name that `GetProgram()` resolves to that profile's `program` string; with no profiles it is passed through as-is (`config/config.go:49-59`, `config/config_test.go:205-231`).
- Named `profiles` (`{name, program}` pairs) feed a profile picker in the session-creation overlay (`GetProfiles()` reorders default first; `README.md:117-141`, `config/config.go:29-33`, `config/config.go:61-82`, `app/app.go:1000`).
- CLI flags override file config at startup: `-p/--program` replaces the resolved program string and `-y/--autoyes` forces `autoYes=true` before `app.Run(ctx, program, autoYes)` (`main.go:52-63`, `main.go:149-154`, `main.go:76`).
- The program string travels untouched through `app.Run → home.program → NewInstance(InstanceOptions{Program}) → Instance.Start → tmux.NewTmuxSession(title, program) → exec tmux new-session ... t.program`, where it becomes the trailing command argument of the tmux invocation (`app/app.go:27-35`, `app/app.go:56`, `app/app.go:625-629`, `session/instance.go:155-156`, `session/instance.go:203-215`, `session/tmux/tmux.go:95-102`).
- Runtime state is a separate file (`state.json`: help-screen bitmask + raw instance JSON) managed by `LoadState`/`SaveState`, never merged with `config.json` despite sharing the same directory (`config/state.go:11-14`, `config/state.go:40-46`, `config/state.go:56-107`).
- Logging is three global `log.Logger`s (`InfoLog`, `WarningLog`, `ErrorLog`) appending to `os.TempDir()/claudesquad.log`, with a `[DAEMON]` prefix variant; config/state load failures degrade to defaults plus a log line rather than crashing (`log/log.go:11-17`, `log/log.go:25-43`, `config/config.go:155-185`).
- Central thesis: Claude/Codex/Gemini/Aider/Amp support is one string field, not code — the only harness-aware branches are three suffix/prefix string checks for prompt and trust-screen detection (`ProgramClaude`/`ProgramAider`/`ProgramGemini`), which gains trivial extensibility (any CLI works) at the cost of no capability model, no argument validation, and prompt detection that silently misses unknown harnesses (`session/tmux/tmux.go:22-25`, `session/tmux/tmux.go:161-184`, `session/tmux/tmux.go:253-260`, `session/instance.go:344-356`).

---
## Config file and schema
Config directory is `$HOME/.claude-squad`, file is `config.json` (`config/config.go:15-27`). Missing file causes a default config to be written and returned; corrupt JSON logs an error and returns defaults (`config/config.go:155-185`). Save path creates the directory and writes indented JSON with mode 0644 (`config/config.go:187-205`).

```go
// config/config.go:36-59
// Config represents the application configuration
type Config struct {
	// DefaultProgram is the default program to run in new instances
	DefaultProgram string `json:"default_program"`
	// AutoYes is a flag to automatically accept all prompts.
	AutoYes bool `json:"auto_yes"`
	// DaemonPollInterval is the interval (ms) at which the daemon polls sessions for autoyes mode.
	DaemonPollInterval int `json:"daemon_poll_interval"`
	// BranchPrefix is the prefix used for git branches created by the application.
	BranchPrefix string `json:"branch_prefix"`
	// Profiles is a list of named program profiles.
	Profiles []Profile `json:"profiles,omitempty"`
}

// GetProgram returns the program to run. If Profiles is non-empty and
// DefaultProgram matches a profile name, that profile's Program is returned.
// Otherwise DefaultProgram is returned as-is.
func (c *Config) GetProgram() string {
	for _, p := range c.Profiles {
		if p.Name == c.DefaultProgram {
			return p.Program
		}
	}
	return c.DefaultProgram
}
```

Defaults are resolved dynamically: `DefaultProgram` via shell/PATH lookup for `claude` (`GetClaudeCommand`, `config/config.go:107-153`), falling back to the literal `"claude"` (`config/config.go:15-18`); `DaemonPollInterval` 1000, `AutoYes` false, `BranchPrefix` `<username>/` (`config/config.go:84-105`). Tests pin these defaults and the missing-file/invalid-JSON fallback behavior (`config/config_test.go:101-113`, `config/config_test.go:128-203`).

## Profiles
Each profile is `{name, program}` (`config/config.go:29-33`). `default_program` doubles as the default profile selector: if it matches a profile name, that profile's command is used (`config/config.go:52-59`). `GetProfiles()` synthesizes a single entry from `DefaultProgram` when no profiles exist, otherwise returns defined profiles with the default first (`config/config.go:61-82`). The documented contract is explicit: `program` is a "shell command used to launch the agent for that profile", and without profiles `default_program` is used "directly as the launch command" (`README.md:134-141`). Example from README (`README.md:123-132`):

```json
{
  "default_program": "claude",
  "profiles": [
    { "name": "claude", "program": "claude" },
    { "name": "codex", "program": "codex" },
    { "name": "aider", "program": "aider --model ollama_chat/gemma3:1b" }
  ]
}
```

The new-session overlay shows a profile picker navigable with arrow keys when more than one profile exists (`README.md:117-119`, `app/app.go:1000`).

## Flag overrides
Flag registration defines `-p/--program` and `-y/--autoyes` (plus hidden `--daemon`) (`main.go:148-160`):

```go
// main.go:52-77
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
```

Precedence is flag > config file > built-in default. `autoYes=true` also launches the background daemon that polls sessions (`main.go:64-70`).

## Program string to tmux spawn — the full call chain
1. `main.go` resolves `program` and calls `app.Run(ctx, program, autoYes)` (`main.go:76`, `app/app.go:27-35`).
2. `app.Run` stores it as `home.program` (`app/app.go:56`, `app/app.go:106`).
3. Session creation passes it verbatim into `session.NewInstance(session.InstanceOptions{Title: "", Path: ".", Program: m.program})` at both creation sites (`app/app.go:625-629`, `app/app.go:646-650`); the field is documented with a multi-harness example (`session/instance.go:149-161`).
4. `NewInstance` copies `opts.Program` onto `Instance.Program` (`session/instance.go:163-184`); the struct field is a bare string (`session/instance.go:41-42`), persisted as `program` in `InstanceData` (`session/storage.go:22`).
5. `Instance.Start` builds `tmux.NewTmuxSession(i.Title, i.Program)` (`session/instance.go:203-215`); the revive-from-storage path does the same (`session/instance.go:137-144`).
6. `newTmuxSession` stores it as unexported `program` (`session/tmux/tmux.go:84-91`); `Start(workDir)` interpolates it as the final argument of the spawn command (`session/tmux/tmux.go:93-102`):

```go
// session/tmux/tmux.go:93-114
// Start creates and starts a new tmux session, then attaches to it. Program is the command to run in
// the session (ex. claude). workdir is the git worktree directory.
func (t *TmuxSession) Start(workDir string) error {
	// Check if the session already exists
	if t.DoesSessionExist() {
		return fmt.Errorf("tmux session already exists: %s", t.sanitizedName)
	}

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
```

No shell parsing, no argument splitting, no per-harness wrapper: whatever string the user configured is the tmux pane's initial command. The tmux session name itself is sanitized (`toClaudeSquadTmuxName`, `session/tmux/tmux.go:70-72`); the program string is not.

## State vs config
`state.json` holds `help_screens_seen` (uint32 bitmask) and `instances` (raw JSON blob), managed through `InstanceStorage`/`AppState` interfaces on `State` (`config/state.go:16-46`, `config/state.go:109-139`). Load/save semantics mirror config (missing file → write and return `DefaultState()` with empty instance list; corrupt JSON → defaults plus error log) (`config/state.go:56-107`). Config is user-edited intent (which program, auto-yes, branch prefix); state is machine-managed runtime memory (which instances exist, which help screens were shown). `reset` wipes state/instances, tmux sessions, and worktrees but never touches `config.json` (`main.go:80-115`).

## Logging
`log.Initialize(daemon bool)` opens `os.TempDir()/claudesquad.log` in append mode and builds the three loggers with date/time/shortfile flags; daemon mode prefixes `[DAEMON]` (`log/log.go:17`, `log/log.go:25-43`). `log.Close()` closes the file and prints its path (`log/log.go:45-49`). `Every` provides rate-limited logging (`log/log.go:51-76`). Every entry point calls `Initialize` first, including tests (`main.go:32`, `config/config_test.go:15-23`).

## The no-adapter design — consequences
Only three constants name harnesses at all (`session/tmux/tmux.go:22-25`): `ProgramClaude = "claude"`, `ProgramAider = "aider"`, `ProgramGemini = "gemini"`. They appear exclusively in string-match branches: trust-prompt dismissal (`HasSuffix` on claude, `HasPrefix` on aider/gemini in `session/tmux/tmux.go:161-184`, gated by `session/instance.go:344-356`) and auto-yes prompt detection (`==`/`HasPrefix` checks against pane content in `session/tmux/tmux.go:253-260`). Anything else — codex, amp, a custom wrapper script — launches fine but gets generic trust handling and no prompt detection. Gains: adding a harness is a one-line JSON edit, no recompile, arbitrary flags supported (`"aider --model ollama_chat/gemma3:1b"`, `session/instance.go:155`). Losses: no validation that the command exists before tmux spawn (failure surfaces as a tmux timeout, `session/tmux/tmux.go:116-133`, `README.md:145-148`), no structured capability differences, and prompt matching is substring-fragile per CLI version.

**Covers:** config/config.go, config/state.go, log/log.go, main.go (flag handling), session spawn call sites
