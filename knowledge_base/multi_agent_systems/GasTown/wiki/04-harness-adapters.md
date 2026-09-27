> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Multi-Harness Support: Agent Adapters and Registry

**In one sentence:** GasTown supports many coder CLIs through a single data-driven registry (`AgentPresetInfo` in `internal/config/agents.go`) that declares each harness's launch command, resume style, hooks provider, and ACP mode — there is no per-harness Go adapter class.

## Key points
- The harness "interface" is the `AgentPresetInfo` struct plus the `AgentRegistry` map and its accessor functions, all in `internal/config/agents.go:61-174` and `internal/config/agents.go:217-223`; a new harness is a new `builtinPresets` entry (`internal/config/agents.go:230`) or a JSON entry in `settings/agents.json`, never a new Go package.
- Thirteen built-in presets are compiled in: `claude`, `gemini`, `codex`, `kiro`, `cursor`, `auggie`, `amp`, `opencode`, `copilot`, `pi`, `omp`, `vibe` (Mistral), `groq-compound` (`internal/config/agents.go:23-55`); each entry fixes the exact CLI binary plus autonomous-mode flags, e.g. `copilot --yolo` (`internal/config/agents.go:406-431`).
- Launch is string/array construction, not a plugin call: `RuntimeConfig.BuildCommand()` (`internal/config/types.go:845-860`) concatenates `Command + Args`, and `BuildCommandWithPrompt()` (`internal/config/types.go:866-909`) appends the startup prompt positionally except for `opencode --prompt`, `copilot -i`, `gemini -i`.
- ACP (Agent Client Protocol, a JSON-RPC stdio protocol) is a second, structured execution path: `internal/acp/proxy.go:42-83` (`Proxy` struct) spawns the agent binary and bridges the UI and the agent over newline-delimited JSON-RPC, injecting the startup prompt as a `session/prompt` request (`internal/acp/proxy.go:786-823`).
- Only `opencode` ships ACP config today (`ACP: &ACPConfig{Command: "acp"}` at `internal/config/agents.go:402-404`, yielding `opencode acp`); three invocation modes (`native`, `subcommand`, `flag`) are defined at `internal/config/agents.go:197-201` and assembled in `internal/mayor/manager.go:271-317`.
- Wrappers are thin `gt prime`-then-`exec` shell scripts (`internal/wrappers/scripts/gt-codex:1-18`, plus `gt-gemini`, `gt-opencode`) installed to `~/bin` by `Install()` (`internal/wrappers/wrappers.go:16-40`); they cover harnesses whose hooks path is weak or absent (notably default `codex`, which has `SupportsHooks: false`).
- Hooks are installed by one generic installer reading preset metadata (`internal/hooks/installer.go:48-72`), with embedded templates per provider under `internal/hooks/templates/` (claude, gemini, codex, cursor, copilot, opencode, pi, omp, vibe); `internal/proxy` plus `cmd/gt-proxy-server` and `cmd/gt-proxy-client` are unrelated to harnesses — they are the mTLS sandbox proxy letting containers call `gt`/`bd` on the host.

---
## 1. The registry is the adapter interface

There is no `Harness` interface, no factory, and no per-harness package under `internal/agent` (that directory holds only the ACP `provider` package and session state). The extension point is data:

```go
// internal/config/agents.go:20,23-55
type AgentPreset string
const (
	AgentClaude   AgentPreset = "claude"
	AgentGemini   AgentPreset = "gemini"
	AgentCodex    AgentPreset = "codex"
	AgentKiro     AgentPreset = "kiro"
	AgentCursor   AgentPreset = "cursor"
	AgentAuggie   AgentPreset = "auggie"
	AgentAmp      AgentPreset = "amp"
	AgentOpenCode AgentPreset = "opencode"
	AgentCopilot  AgentPreset = "copilot"
	AgentPi       AgentPreset = "pi"
	AgentOmp      AgentPreset = "omp"
	AgentMistral  AgentPreset = "vibe"
	AgentGroqCompound AgentPreset = "groq-compound"
)
```

```go
// internal/config/agents.go:61-74 (struct continues to line 174)
type AgentPresetInfo struct {
	Name AgentPreset `json:"name"`
	// Command is the CLI binary to invoke.
	Command string `json:"command"`
	// Args are the default command-line arguments for autonomous mode.
	Args []string `json:"args"`
	// Env are environment variables to set when starting the agent.
	Env map[string]string `json:"env,omitempty"`
	// ProcessNames are the process names to look for when detecting if the agent is running.
	ProcessNames []string `json:"process_names,omitempty"`
	// ... SessionIDEnv, ResumeFlag/ContinueFlag, ResumeStyle ("flag"|"subcommand"),
	// SupportsHooks, SupportsForkSession, NonInteractive, PromptMode ("arg"|"none"),
	// ConfigDirEnv/ConfigDir, HooksProvider/HooksDir/HooksSettingsFile,
	// HooksInformational, HooksUseSettingsDir, ReadyPromptPrefix, ReadyDelayMs,
	// InstructionsFile, EmitsPermissionWarning, HasTurnBoundaryDrain,
	// EscapeCancelsRequest, ACP *ACPConfig
}
```

```go
// internal/config/agents.go:177-194
type ACPConfig struct {
	Mode    string   `json:"mode,omitempty"`
	Command string   `json:"command,omitempty"`
	Args    []string `json:"args,omitempty"`
}
```

Registration and lookup mechanics (`internal/config/agents.go:542-551`, `678-704`):

- `builtinPresets` (`internal/config/agents.go:230`) is the compiled-in map; `globalRegistry` guarded by `registryMu` (`internal/config/agents.go:542-551`) is the merged view of built-ins plus user JSON.
- User presets in `~/gt/settings/agents.json` (town) or `<rig>/settings/agents.json` (rig) are merged over built-ins by `loadAgentRegistryFromPathLocked` (`internal/config/agents.go:572-608`); same-name keys override.
- Lookup: `GetAgentPreset` (`internal/config/agents.go:678-683`), `GetAgentPresetByName` (`internal/config/agents.go:687-692`), `ListAgentPresets` (`internal/config/agents.go:695-704`), `IsKnownPreset` (`internal/config/agents.go:1034-1040`).
- `RuntimeConfigFromPreset` (`internal/config/agents.go:722-725`) converts a preset to the resolved `RuntimeConfig` (`internal/config/types.go:729-786`) that tmux spawn actually consumes.

Note on stale docs: `docs/agent-provider-integration.md:321-342` describes a `HookInstallerFunc` registered via `config.RegisterHookInstaller` in `internal/runtime/runtime.go`. That function does not exist in the code — hooks went to a single generic installer (`internal/hooks/installer.go:48-72`) driven by preset metadata. Treat the doc's Tier 2 registration snippet as aspirational; the JSON preset fields are authoritative.

## 2. Supported harnesses and launch construction

Built-in preset entries with exact autonomous-mode argv (binary + flags):

| Preset | `Command` + `Args` | Resume | Source |
|---|---|---|---|
| `claude` | `claude --dangerously-skip-permissions` | `--resume` / `--continue`, style `flag` | `internal/config/agents.go:231-256` |
| `gemini` | `gemini --approval-mode yolo` | `--resume`, `flag` | `internal/config/agents.go:257-280` |
| `codex` | `codex -c check_for_update_on_startup=false --dangerously-bypass-approvals-and-sandbox` | `resume` subcommand | `internal/config/agents.go:281-300` |
| `kiro` | `kiro-cli chat --trust-all-tools` | `--resume-id` / `--resume`, `flag` | `internal/config/agents.go:301-318` |
| `cursor` | `cursor-agent -f` | `--resume`, `flag` | `internal/config/agents.go:319-345` |
| `auggie` | `auggie --allow-indexing` | `--resume`, `flag` | `internal/config/agents.go:346-359` |
| `amp` | `amp --dangerously-allow-all --no-ide` | `threads continue` subcommand | `internal/config/agents.go:360-373` |
| `opencode` | `opencode` (no flags; YOLO via `OPENCODE_PERMISSION` env) | none | `internal/config/agents.go:374-405` |
| `copilot` | `copilot --yolo` | `--resume` / `--continue`, `flag` | `internal/config/agents.go:406-431` |
| `pi` | `pi -e .pi/extensions/gastown-hooks.js` | none | `internal/config/agents.go:432-454` |
| `omp` | `omp --hook .omp/hooks/gastown-hook.ts` | none | `internal/config/agents.go:455-469` |
| `vibe` | `vibe --agent auto-approve` | `--resume` / `--continue`, `flag` | `internal/config/agents.go:470-493` |
| `groq-compound` | `claude --dangerously-skip-permissions` + `ANTHROPIC_BASE_URL`/`ANTHROPIC_API_KEY=$GROQ_API_KEY` env override | `--resume` / `--continue`, `flag` | `internal/config/agents.go:510-539` |

How the argv becomes a process:

1. `defaultRuntimeCommand` / `defaultRuntimeArgs` (`internal/config/types.go:1069-1114`) pull `Command`/`Args` from the preset (Claude's binary is path-resolved via `resolveClaudePath`, `internal/config/types.go:1087-1107`).
2. Codex argv is force-amended with `-c check_for_update_on_startup=false` unless already present (`internal/config/types.go:1046-1054`).
3. `BuildCommand()` (`internal/config/types.go:845-860`) joins command + shell-quoted args for tmux `send-keys` / respawn-pane.
4. `BuildCommandWithPrompt()` (`internal/config/types.go:866-909`) appends the startup beacon: positional quoted arg by default, but `--prompt <p>` for opencode, `-i <p>` for copilot and gemini (`internal/config/types.go:891-905`). `PromptMode "none"` drops the prompt with a stderr warning (`internal/config/types.go:876-886`).
5. Resume is rendered by `BuildResumeCommand` (`internal/config/agents.go:759-784`): `flag` style appends `<flag> <sessionID>`; `subcommand` style yields `codex resume <id> <args>` or `amp threads continue <id>`.
6. Liveness detection reads `pane_current_command` against the preset's `ProcessNames`, with wrapper-aware resolution (`ResolveProcessNames`, `internal/config/agents.go:932-1001`).

Special cases: `groq-compound` reuses the Claude binary as an SDK proxy and redirects it to Groq's OpenAI-compatible endpoint purely through env (`internal/config/agents.go:494-519`); non-interactive (headless) shapes per harness live in `NonInteractiveConfig` (`internal/config/agents.go:203-213`), e.g. codex `exec --json`, gemini `-p --output-format json`, cursor `-p --output-format json`, opencode `run --format json`.

## 3. ACP role: structured alternative to tmux keystrokes

ACP (Agent Client Protocol) is a JSON-RPC-over-stdio protocol for driving an agent with messages instead of terminal keystrokes. GasTown implements both sides of the plumbing:

- Message vocabulary (`internal/agent/provider/acp.go`): `JSONRPCRequest`/`JSONRPCResponse` (`internal/agent/provider/acp.go:38-56`), `ContentBlock` with `text`/`tool_use`/`tool_result`/`thinking` variants (`internal/agent/provider/acp.go:58-82`), `Tool`, `InitializeParams/Result`, `CallToolParams/Result`, `CreateMessageParams/Result` (`internal/agent/provider/acp.go:195-338`), plus constructors such as `NewInitializeRequest` (`internal/agent/provider/acp.go:501-519`).
- Provider interface, verbatim (`internal/agent/provider/provider.go:31-40`):

```go
type ACPProvider interface {
	Initialize(ctx context.Context, clientName, clientVersion string) (*InitializeResult, error)
	ListTools(ctx context.Context) ([]Tool, error)
	CallTool(ctx context.Context, name string, args map[string]any) (*CallToolResult, error)
	CreateMessage(ctx context.Context, params CreateMessageParams) (*CreateMessageResult, error)
	GetStatus() AgentStatus
	OnToolCall(callback ToolCallback)
	OnSessionStart(callback SessionStartCallback)
	Close() error
}
```

`BaseProvider` (`internal/agent/provider/provider.go:49-56`) holds state/tools/callbacks; `LocalProvider` (`internal/agent/provider/provider.go:118-128`) is the in-process implementation.

- `Proxy` (`internal/acp/proxy.go:42-83`) is the stdio bridge: `Start` (`internal/acp/proxy.go:181-242`) spawns `exec.CommandContext(agentPath, agentArgs...)` with piped stdin/stdout/stderr; `forwardToAgent` (`internal/acp/proxy.go:365-421`) relays UI→agent JSON-RPC; `forwardFromAgent` (`internal/acp/proxy.go:437-548`) relays agent→UI, extracts `sessionId` (`internal/acp/proxy.go:825-850`), tracks the `initialize → session/new` handshake (`internal/acp/proxy.go:765-784`), and injects the startup prompt as `session/prompt` once the handshake completes (`internal/acp/proxy.go:786-823`). Keep-alive heartbeats (`runKeepAlive`, `internal/acp/proxy.go:626-727`) and propulsion-trigger suppression (`internal/acp/proxy.go:1180-1213`) ride on the same loop.
- ACP argv assembly for the mayor path (`internal/mayor/manager.go:271-317`): `native` mode passes only extra args; `subcommand` mode prepends `acpConfig.Command` (hence `opencode acp`); `flag` mode appends `acpConfig.Args` (e.g. `gemini --experimental-acp`). Empty result falls back to `rc.Args`.
- Registry helpers: `ResolveACPConfig` (`internal/config/agents.go:1100-1121`), `SupportsACP`/`GetACPConfig` (`internal/config/agents.go:1125-1145`), `RuntimeConfigSupportsACP`/`GetACPConfigFromRuntime` (`internal/config/agents.go:1179-1241`).

## 4. Wrappers: `gt prime` before `exec`

`internal/wrappers/wrappers.go:16-40` embeds `scripts/*` and installs three scripts to `~/bin`:

```bash
# internal/wrappers/scripts/gt-codex:7-18 (gt-gemini and gt-opencode are identical modulo binary name)
gastown_enabled() {
    [[ -n "$GASTOWN_DISABLED" ]] && return 1
    [[ -n "$GASTOWN_ENABLED" ]] && return 0
    local state_file="$HOME/.local/state/gastown/state.json"
    [[ -f "$state_file" ]] && grep -q '"enabled":\s*true' "$state_file" 2>/dev/null
}
if gastown_enabled && command -v gt &>/dev/null; then
    gt prime 2>/dev/null || true
fi
exec codex "$@"
```

Semantics: print role context to the terminal (`gt prime` output is inherited, not piped), then replace the process with the real CLI preserving argv. This is the context path for harnesses without working executable hooks — the default `codex` preset has `SupportsHooks: false` (`internal/config/agents.go:289`) and its doc section still points at the wrapper (`docs/agent-provider-integration.md:458-477`). An experimental opt-in Codex hooks profile (`.codex/hooks.json` via a custom preset) is documented at `docs/agent-provider-integration.md:480-513` but is not the built-in default.

## 5. Hooks and startup fallback per harness

`EnsureSettingsForRole` (`internal/runtime/runtime.go:25-66`) reads the preset's `HooksProvider/HooksDir/HooksSettingsFile/HooksUseSettingsDir` and calls the generic `hooks.InstallForRole` (`internal/hooks/installer.go:48-72`), which resolves an embedded template (`resolveTemplate`, `internal/hooks/installer.go:213-241`) and writes it atomically. Template inventory (`internal/hooks/templates/`):

| Provider | Templates | Preset fields |
|---|---|---|
| `claude` | `settings-autonomous.json`, `settings-interactive.json` | `HooksDir .claude`, `HooksUseSettingsDir true` (`internal/config/agents.go:246-250`) |
| `gemini` | `settings-autonomous.json`, `settings-interactive.json` | `HooksDir .gemini` (`internal/config/agents.go:273-277`) |
| `cursor` | `hooks-autonomous.json`, `hooks-interactive.json` | `HooksDir .cursor`, file `hooks.json` (`internal/config/agents.go:337-341`); onboarding in `.cursor/README.md:1-49` |
| `copilot` | `gastown-autonomous.json`, `gastown-interactive.json` (+ legacy `copilot-instructions.md`) | `HooksDir .github/hooks`, file `gastown.json` (`internal/config/agents.go:423-426`) |
| `opencode` | `gastown.js` plugin | `HooksDir .opencode/plugins` (`internal/config/agents.go:394-398`) |
| `pi` | `gastown-hooks.js` extension | `HooksDir .pi/extensions` (`internal/config/agents.go:441-443`) |
| `omp` | `gastown-hook.ts` | `HooksDir .omp/hooks` (`internal/config/agents.go:462-464`) |
| `vibe` | `config.toml` | `HooksDir .vibe` (`internal/config/agents.go:486-489`) |
| `codex` | `hooks-autonomous.json`, `hooks-interactive.json` exist but are only used by opt-in custom profiles | built-in `SupportsHooks: false` (`internal/config/agents.go:289`) |
| `kiro`, `auggie`, `amp` | no templates | `SupportsHooks: false` |

Harnesses without executable hooks (or with `PromptMode "none"`) fall back to tmux-nudge delivery per the matrix in `GetStartupFallbackInfo` (`internal/runtime/runtime.go:232-293`): hooks+prompt needs nothing; no-hooks adds "Run `gt prime`" to the beacon plus a delayed nudge (`DefaultPrimeWaitMs = 2000`, `internal/runtime/runtime.go:219`).

## 6. Adding a new harness: exact recipe

Tier 1 (no Go changes; `docs/agent-provider-integration.md:65-264`):

1. Create/extend `~/gt/settings/agents.json` (town-wide) or `<rig>/settings/agents.json` with `{"version": 1, "agents": {"<name>": {...}}}` using the `AgentPresetInfo` field names (`internal/config/agents.go:61-174`); minimal viable keys are `name`, `command`, `args`, `process_names`, `prompt_mode`, `ready_delay_ms`, `instructions_file` (example at `docs/agent-provider-integration.md:682-701`).
2. Add `resume_flag` + `resume_style` if the CLI can resume (`internal/config/agents.go:759-784` consumes them); add `non_interactive` (`internal/config/agents.go:203-213`) to enable formula/dog headless execution.
3. Point a rig at it via `agent` / `default_agent` / `role_agents` (`docs/agent-provider-integration.md:211-264`); resolution order is role override → rig `agent` → town `default_agent` → `"claude"` fallback, each looked up rig-custom → town-custom → built-in (`docs/agent-provider-integration.md:249-264`, implemented in `internal/config/loader.go:1314-1383`).

Tier 2 (hooks; requires a template plus preset fields):

4. Add `templates/<provider>/` files under `internal/hooks/templates/` following the `settings-autonomous.json` / `settings-interactive.json` (or `hooks-*.json`, or single `<hooksFile>`) convention resolved at `internal/hooks/installer.go:213-241`; role classification comes from `hookutil.IsAutonomousRole` (`internal/hooks/installer.go:216`).
5. Set `hooks_provider`, `hooks_dir`, `hooks_settings_file` (and `hooks_use_settings_dir` if the CLI accepts a `--settings`-style flag) in the preset; if hooks are instructions-only, also set `hooks_informational: true` so `StartupFallbackCommands` (`internal/runtime/runtime.go:189-204`) nudges `gt prime` instead.
6. To ship it built-in, add one `builtinPresets` entry in `internal/config/agents.go:230-539` and, if ACP-capable, an `ACP` block (`internal/config/agents.go:177-194`) plus verification via `SupportsACP` (`internal/config/agents.go:1125-1135`).

Explicitly out of scope: `docs/contrib-harnesses/README.md:1-20` ("harness" there means role directives/formula overlays, not coder CLIs); `docs/runtimes/NOS_TOWN.md:1-36` (Groq runtime fork strategy, not a harness adapter); `internal/proxy/server.go:25-60`, `cmd/gt-proxy-server/main.go:1-38`, `cmd/gt-proxy-client/main.go:1-51` (sandbox mTLS proxy, not agent protocol); `docs/cursor-runtime-beads-tasks.md:1-21` (Cursor parity task tracker).

**Covers:** `internal/config/agents.go`, `internal/config/types.go`, `internal/agent/provider/`, `internal/acp/proxy.go`, `internal/wrappers/`, `internal/hooks/installer.go`, `internal/hooks/templates/`, `internal/runtime/runtime.go`, `internal/mayor/manager.go`, `internal/proxy/`, `cmd/gt-proxy-server`, `cmd/gt-proxy-client`, `docs/agent-provider-integration.md`, `docs/contrib-harnesses/README.md`, `docs/runtimes/NOS_TOWN.md`, `docs/cursor-runtime-beads-tasks.md`, `.cursor/README.md`
