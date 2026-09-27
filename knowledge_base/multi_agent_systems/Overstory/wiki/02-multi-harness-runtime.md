> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Multi-Harness AgentRuntime Abstraction
**In one sentence:** Overstory isolates all harness-specific logic (CLI = command-line interface) behind an `AgentRuntime` interface with per-harness adapters resolved through a central registry, plus guard generators, a connection store, and headless (NDJSON = newline-delimited JSON) event paths.
## Key points
- The `AgentRuntime` contract in `src/runtimes/types.ts:148` declares 8 required members (`id`, `stability`, `instructionPath`, `buildSpawnCommand`, `buildPrintCommand`, `deployConfig`, `detectReady`, `parseTranscript`, `getTranscriptDir`, `buildEnv`) plus 4 optional members (`requiresBeaconVerification`, `connect`, `headless`, `buildDirectSpawn`/`parseEvents`).
- The registry in `src/runtimes/registry.ts:16` maps 8 names (`claude`, `codex`, `pi`, `copilot`, `cursor`, `gemini`, `sapling`, `opencode`) to factories, resolves by explicit name → per-capability routing → config default → `"claude"` fallback (`src/runtimes/registry.ts:72`), and special-cases Pi config injection (`src/runtimes/registry.ts:79`).
- Only 2 of 8 adapters are `stable` (Claude in `src/runtimes/claude.ts:35`, Sapling in `src/runtimes/sapling.ts:349`); the other 6 are `experimental`, and only Sapling sets `headless = true` (`src/runtimes/sapling.ts:358`) with `buildDirectSpawn` (`src/runtimes/sapling.ts:429`) and `parseEvents` (`src/runtimes/sapling.ts:593`).
- Guard enforcement splits three ways: Claude writes hooks via `deployHooks` (`src/runtimes/claude.ts:129`), Pi generates a TypeScript (TS) extension via `generatePiGuardExtension` (`src/runtimes/pi-guards.ts:128`), Sapling writes `.sapling/guards.json` via `buildGuardsConfig` (`src/runtimes/sapling.ts:98`); Codex, Copilot, Cursor, Gemini, and OpenCode deploy no guards.
- Pi readiness requires header plus status-bar regex (`src/runtimes/pi.ts:174`), Claude requires prompt marker plus `bypass permissions` with two dialog phases (`src/runtimes/claude.ts:153`), Codex and Sapling always return ready (`src/runtimes/codex.ts:163`, `src/runtimes/sapling.ts:506`), and OpenCode always returns loading as an acknowledged stub (`src/runtimes/opencode.ts:138`).
- RPC (remote procedure call) is defined by `RuntimeConnection` (`src/runtimes/types.ts:102`) over `RpcProcessHandle` (`src/runtimes/types.ts:89`), tracked per-agent in `src/runtimes/connections.ts:12`, but only Sapling implements `connect()` (`src/runtimes/sapling.ts:662`); none of the read source files implement session resume.
- Adding a runtime means creating `src/runtimes/<name>.ts` implementing `AgentRuntime`, registering a factory in `src/runtimes/registry.ts:16`, optionally adding config types, and testing spawn plus `deployConfig` (`docs/runtime-adapters.md:516`).
---
## 1. Interface: `AgentRuntime`
Defined in `src/runtimes/types.ts:148`. The header comment states the design rule: the orchestration engine calls only these methods, never the runtime CLI (command-line interface) directly (`src/runtimes/types.ts:141`).

Verbatim definition (`src/runtimes/types.ts:148`–`src/runtimes/types.ts:249`):
```typescript
export interface AgentRuntime {
	/** Unique runtime identifier (e.g. "claude", "codex", "pi"). */
	id: string;

	/** Stability level of this runtime adapter. */
	readonly stability: "stable" | "beta" | "experimental";

	/** Relative path to the instruction file within a worktree (e.g. ".claude/CLAUDE.md"). */
	readonly instructionPath: string;

	/** Build the shell command string to spawn an interactive agent in a tmux pane. */
	buildSpawnCommand(opts: SpawnOpts): string;

	/**
	 * Build the argv array for a headless one-shot AI call.
	 * Used by merge/resolver.ts and watchdog/triage.ts for AI-assisted operations.
	 */
	buildPrintCommand(prompt: string, model?: string): string[];

	/**
	 * Deploy per-agent instructions and guards to a worktree.
	 * Claude Code writes .claude/CLAUDE.md + settings.local.json hooks.
	 * Codex writes AGENTS.md (no hook deployment needed).
	 * Pi writes .claude/CLAUDE.md + a guard extension in .pi/extensions/.
	 * When overlay is undefined, only hooks are deployed (no instruction file written).
	 */
	deployConfig(
		worktreePath: string,
		overlay: OverlayContent | undefined,
		hooks: HooksDef,
	): Promise<void>;

	/**
	 * Detect agent readiness from tmux pane content.
	 * Headless runtimes that exit when done should return { phase: "ready" } unconditionally.
	 */
	detectReady(paneContent: string): ReadyState;

	/**
	 * Parse a session transcript file into normalized token usage.
	 * Returns null if the transcript does not exist or cannot be parsed.
	 */
	parseTranscript(path: string): Promise<TranscriptSummary | null>;

	/**
	 * Return the directory containing session transcript files for this runtime,
	 * or null if transcript discovery is not supported.
	 *
	 * @param projectRoot - Absolute path to the project root
	 * @returns Absolute path to the transcript directory, or null
	 */
	getTranscriptDir(projectRoot: string): string | null;

	/**
	 * Build runtime-specific environment variables for model/provider routing.
	 * Claude Code uses ANTHROPIC_API_KEY; Codex uses OPENAI_API_KEY; Pi passes
	 * the provider's authTokenEnv directly.
	 */
	buildEnv(model: ResolvedModel): Record<string, string>;

	/**
	 * Whether this runtime requires the beacon verification/resend loop after initial send.
	 *
	 * Claude Code's TUI sometimes swallows Enter during late initialization, so the
	 * orchestrator resends the beacon if the pane still appears idle (overstory-3271).
	 * Pi's TUI does not exhibit this behavior AND its idle/processing states are
	 * indistinguishable via detectReady (both show the header and status bar), so
	 * the resend loop would spam Pi with duplicate startup messages.
	 *
	 * Runtimes that omit this method (or return true) get the resend loop.
	 * Pi returns false to skip it.
	 */
	requiresBeaconVerification?(): boolean;

	/**
	 * Establish direct RPC connection to running agent process.
	 * Runtimes without RPC (Claude, Codex) omit this method.
	 * Orchestrator checks `if (runtime.connect)` before calling, falls back to tmux when absent.
	 */
	connect?(process: RpcProcessHandle): RuntimeConnection;

	/**
	 * Whether this runtime is headless (no tmux, direct subprocess).
	 * Headless runtimes bypass all tmux session management and use Bun.spawn directly.
	 * Default: false (absent means interactive/tmux-based).
	 */
	readonly headless?: boolean;

	/**
	 * Build the argv array for Bun.spawn() to launch a headless agent subprocess.
	 * Only headless runtimes implement this method.
	 * The returned array is passed directly to Bun.spawn() — no shell interpolation.
	 */
	buildDirectSpawn?(opts: DirectSpawnOpts): string[];

	/**
	 * Parse NDJSON stdout from a headless agent subprocess into typed AgentEvent objects.
	 * Only headless runtimes implement this method.
	 * The caller provides the raw stdout ReadableStream from Bun.spawn().
	 */
	parseEvents?(stream: ReadableStream<Uint8Array>): AsyncIterable<AgentEvent>;
}
```

Supporting types:
- `SpawnOpts` (`src/runtimes/types.ts:9`): `model`, `permissionMode` (`bypass`|`ask`), `systemPrompt`, `appendSystemPrompt`, `appendSystemPromptFile` (`src/runtimes/types.ts:19`), `cwd`, `sharedWritableDirs`, `env`.
- `ReadyState` (`src/runtimes/types.ts:34`): `loading` | `dialog` + `action` | `ready`; headless runtimes always return ready (`src/runtimes/types.ts:30`).
- `OverlayContent` (`src/runtimes/types.ts:42`): single `content` markdown string.
- `HooksDef` (`src/runtimes/types.ts:52`): `agentName`, `capability`, `worktreePath`, optional `qualityGates`.
- `TranscriptSummary` (`src/runtimes/types.ts:66`): `inputTokens`, `outputTokens`, `model`.
- `ConnectionState` (`src/runtimes/types.ts:79`): `idle`|`working`|`error` plus optional `currentTool`.
- `RpcProcessHandle` (`src/runtimes/types.ts:89`): `stdin.write` plus `stdout` stream, compatible with `Bun.spawn` output (`src/runtimes/types.ts:85`).
- `RuntimeConnection` (`src/runtimes/types.ts:102`): `sendPrompt`, `followUp`, `abort`, `getState`, `close` (`src/runtimes/types.ts:104`–`src/runtimes/types.ts:112`).
- `DirectSpawnOpts` (`src/runtimes/types.ts:118`): `cwd`, `env`, optional `model`, `instructionPath`.
- `AgentEvent` (`src/runtimes/types.ts:130`): `type`, `timestamp` (ISO 8601 = International Organization for Standardization date format), plus open payload.

## 2. Wiring: registry, orchestrator, connections
ASCII (American Standard Code for Information Interchange) diagram:
```
orchestrator (sling/coordinator/monitor)
  |
  | getRuntime(name?, config?, capability?)  [src/runtimes/registry.ts:67]
  v
registry Map<string, factory>  [src/runtimes/registry.ts:16]
  |-- claude   -> ClaudeRuntime    [src/runtimes/registry.ts:17]
  |-- codex    -> CodexRuntime     [src/runtimes/registry.ts:18]
  |-- pi       -> PiRuntime (+config) [src/runtimes/registry.ts:79]
  |-- copilot  -> CopilotRuntime   [src/runtimes/registry.ts:20]
  |-- cursor   -> CursorRuntime    [src/runtimes/registry.ts:21]
  |-- gemini   -> GeminiRuntime    [src/runtimes/registry.ts:22]
  |-- sapling  -> SaplingRuntime   [src/runtimes/registry.ts:23]
  |-- opencode -> OpenCodeRuntime  [src/runtimes/registry.ts:24]
  v
AgentRuntime methods only:
buildSpawnCommand / deployConfig / detectReady /
parseTranscript / getTranscriptDir / buildEnv /
[requiresBeaconVerification?] / [connect? -> RuntimeConnection]
  |
  +-- tmux path (7 runtimes): spawn string -> pane -> detectReady
  +-- headless path (sapling): buildDirectSpawn -> Bun.spawn ->
      parseEvents -> connect -> connections Map  [src/runtimes/connections.ts:12]
```

Registry semantics:
- `runtimes` is the only place importing concrete adapters (`src/runtimes/registry.ts:1`).
- `getAllRuntimes()` constructs one fresh instance per runtime for enumeration, e.g. instruction-path discovery (`src/runtimes/registry.ts:36`).
- Resolution order is explicit name, then `config.runtime.capabilities[capability]`, then `config.runtime.default`, then `"claude"` (`src/runtimes/registry.ts:72`–`src/runtimes/registry.ts:76`).
- Pi bypasses the generic factory to receive `config?.runtime?.pi` for alias expansion (`src/runtimes/registry.ts:79`–`src/runtimes/registry.ts:81`).
- Unknown names throw with the available list (`src/runtimes/registry.ts:84`–`src/runtimes/registry.ts:87`).
- Connection store is a module-level `Map<string, RuntimeConnection>` keyed by agent name (`src/runtimes/connections.ts:12`), with `getConnection` (`src/runtimes/connections.ts:15`), `setConnection` overwrite (`src/runtimes/connections.ts:20`), and `removeConnection` that calls `close()` first and is a no-op when absent (`src/runtimes/connections.ts:28`).

## 3. Adapters
### 3.1 Claude (`src/runtimes/claude.ts`)
Reference TUI (terminal user interface) runtime: `id = "claude"` (`src/runtimes/claude.ts:32`), `stability = "stable"` (`src/runtimes/claude.ts:35`), `instructionPath = ".claude/CLAUDE.md"` (`src/runtimes/claude.ts:38`).
- Spawn maps `bypass` to `--permission-mode bypassPermissions` and `ask` to `default` (`src/runtimes/claude.ts:57`); file-based prompt uses `$(cat ...)` shell expansion to avoid tmux IPC (inter-process communication) size limits (`src/runtimes/claude.ts:61`), inline prompt uses POSIX (Portable Operating System Interface) single-quote escaping (`src/runtimes/claude.ts:68`).
- Print uses `["claude", "--print", "-p", prompt]` plus optional `--model` (`src/runtimes/claude.ts:92`).
- `deployConfig` writes `CLAUDE.md` only when overlay is defined, then always calls `deployHooks` (`src/runtimes/claude.ts:116`–`src/runtimes/claude.ts:129`).
- `detectReady` handles three phases: bypass-confirmation screen returns `dialog/type:2` (`src/runtimes/claude.ts:153`), `trust this folder` returns `dialog/Enter` (`src/runtimes/claude.ts:163`), prompt marker (`❯` or `Try "`) plus `bypass permissions` returns ready (`src/runtimes/claude.ts:169`–`src/runtimes/claude.ts:174`); `shift+tab` is deliberately excluded as a ready signal (`src/runtimes/claude.ts:172`).
- `parseTranscript` delegates to `parseTranscriptUsage` and validates via `estimateCost`, returning null on missing/unparsable files (`src/runtimes/claude.ts:198`–`src/runtimes/claude.ts:218`).
- `buildEnv` returns `model.env ?? {}` (`src/runtimes/claude.ts:235`).
- `getTranscriptDir` maps project root to `~/.claude/projects/<path-with-/-as-->` and returns null when `HOME` is empty (`src/runtimes/claude.ts:248`–`src/runtimes/claude.ts:252`).
- Omits `requiresBeaconVerification`, so it gets the resend loop by default (`docs/runtime-adapters.md:326`).

### 3.2 Pi (`src/runtimes/pi.ts`)
TUI runtime with alias expansion and extension guards: `id = "pi"` (`src/runtimes/pi.ts:36`), `experimental` (`src/runtimes/pi.ts:39`), same instruction path as Claude (`src/runtimes/pi.ts:42`).
- Default config maps `opus/sonnet/haiku` to `anthropic/claude-*-4-6/4-5` with provider `anthropic` (`src/runtimes/pi.ts:18`); `expandModel` passes through `/`-qualified models, uses `modelMap`, else prefixes provider (`src/runtimes/pi.ts:57`–`src/runtimes/pi.ts:62`).
- Spawn ignores `permissionMode`; security comes from guard extensions (`src/runtimes/pi.ts:64`); prompt-file and inline escaping mirror Claude (`src/runtimes/pi.ts:81`–`src/runtimes/pi.ts:89`).
- Print uses `["pi", "--print", ..., prompt]` with prompt as last positional argument (`src/runtimes/pi.ts:105`–`src/runtimes/pi.ts:112`).
- `deployConfig` writes `CLAUDE.md` conditionally, then always writes `.pi/extensions/overstory-guard.ts` and `.pi/settings.json` with `extensions: ["./extensions"]` (`src/runtimes/pi.ts:126`–`src/runtimes/pi.ts:146`).
- Returns `requiresBeaconVerification() = false` to avoid duplicate prompts (`src/runtimes/pi.ts:157`).
- `detectReady` requires `pi v` header plus `/\d+\.\d+%\/\d+k/` token counter (`src/runtimes/pi.ts:170`–`src/runtimes/pi.ts:180`); no dialog phase.
- `parseTranscript` reads Pi v3 `message` events with `message.usage.input/output` plus `cacheRead` folded into input, falls back to legacy `message_end.inputTokens/outputTokens`, and takes model from `model_change.modelId` or `message.model` (`src/runtimes/pi.ts:197`–`src/runtimes/pi.ts:270`).
- `buildEnv` returns `model.env ?? {}` (`src/runtimes/pi.ts:281`).
- `getTranscriptDir` encodes project path as `--<dashes>--` under `~/.pi/agent/sessions/` (`src/runtimes/pi.ts:297`–`src/runtimes/pi.ts:304`).

### 3.3 Codex (`src/runtimes/codex.ts`)
Interactive-but-sandboxed runtime: `id = "codex"` (`src/runtimes/codex.ts:38`), `experimental` (`src/runtimes/codex.ts:41`), `instructionPath = "AGENTS.md"` (`src/runtimes/codex.ts:44`).
- Omits `--model` for manifest aliases `sonnet/opus/haiku` (`src/runtimes/codex.ts:50`); otherwise `codex --full-auto [--model X]` plus `--add-dir` for `sharedWritableDirs` (`src/runtimes/codex.ts:77`–`src/runtimes/codex.ts:86`); system prompt is prepended to the exec prompt because there is no `--append-system-prompt` flag (`src/runtimes/codex.ts:68`–`src/runtimes/codex.ts:100`).
- Print uses `codex exec --full-auto --ephemeral` (`src/runtimes/codex.ts:119`–`src/runtimes/codex.ts:126`).
- `deployConfig` is a no-op when overlay is undefined; otherwise writes `AGENTS.md` only, no hooks (`src/runtimes/codex.ts:143`–`src/runtimes/codex.ts:155`).
- `detectReady` always returns ready (`src/runtimes/codex.ts:163`); `requiresBeaconVerification` returns false (`src/runtimes/codex.ts:172`).
- `parseTranscript` sums `turn.completed.usage.input_tokens/output_tokens` and captures top-level `model` (`src/runtimes/codex.ts:189`–`src/runtimes/codex.ts:234`).
- `buildEnv` returns `model.env ?? {}` (`src/runtimes/codex.ts:246`); `getTranscriptDir` returns null (`src/runtimes/codex.ts:251`).

### 3.4 Copilot (`src/runtimes/copilot.ts`)
GitHub Copilot TUI: `id = "copilot"` (`src/runtimes/copilot.ts:29`), `experimental` (`src/runtimes/copilot.ts:32`), `instructionPath = ".github/copilot-instructions.md"` (`src/runtimes/copilot.ts:35`).
- Spawn maps `bypass` to `--allow-all-tools`, `ask` to no flag, and silently ignores both append-prompt fields (`src/runtimes/copilot.ts:53`–`src/runtimes/copilot.ts:64`).
- Print uses `["copilot", "-p", prompt, "--allow-all-tools"]` plus optional `--model` (`src/runtimes/copilot.ts:79`–`src/runtimes/copilot.ts:85`).
- `deployConfig` writes only the instruction file; hooks unused (`src/runtimes/copilot.ts:101`–`src/runtimes/copilot.ts:113`).
- `detectReady` requires prompt (`❯` or `copilot`, case-insensitive) plus status bar (`shift+tab` or `esc`); never dialog (`src/runtimes/copilot.ts:127`–`src/runtimes/copilot.ts:141`).
- `parseTranscript` handles dual formats: Claude-style `assistant/message.usage.input_tokens` and Pi-style `message_end/inputTokens`, plus top-level and nested `model` (`src/runtimes/copilot.ts:158`–`src/runtimes/copilot.ts:215`).
- `buildEnv` returns `model.env ?? {}` (`src/runtimes/copilot.ts:226`); `getTranscriptDir` returns null (`src/runtimes/copilot.ts:231`).

### 3.5 Gemini (`src/runtimes/gemini.ts`)
Google Gemini CLI (CLI = command-line interface): `id = "gemini"` (`src/runtimes/gemini.ts:40`), `experimental` (`src/runtimes/gemini.ts:43`), `instructionPath = "GEMINI.md"` (`src/runtimes/gemini.ts:46`).
- Spawn maps `bypass` to `--approval-mode yolo` and ignores append-prompt fields; roles go via `GEMINI.md` (`src/runtimes/gemini.ts:62`–`src/runtimes/gemini.ts:74`).
- Print uses `["gemini", "-p", prompt, "--yolo"]` plus optional `-m` (`src/runtimes/gemini.ts:90`–`src/runtimes/gemini.ts:96`).
- `deployConfig` writes only `GEMINI.md`; hooks unused (`src/runtimes/gemini.ts:113`–`src/runtimes/gemini.ts:123`).
- `detectReady` requires prompt (`type your message`, `^> `, or `❯`) plus `gemini` branding; never dialog (`src/runtimes/gemini.ts:139`–`src/runtimes/gemini.ts:156`).
- `parseTranscript` takes model from `init.model` and tokens from `result.stats.input_tokens/output_tokens` (`src/runtimes/gemini.ts:172`–`src/runtimes/gemini.ts:223`).
- `buildEnv` returns `model.env ?? {}` (`src/runtimes/gemini.ts:235`); `getTranscriptDir` returns null (`src/runtimes/gemini.ts:240`).

### 3.6 OpenCode (`src/runtimes/opencode.ts`)
Stub adapter: `id = "opencode"` (`src/runtimes/opencode.ts:42`), `experimental` (`src/runtimes/opencode.ts:45`), `instructionPath = "AGENTS.md"` marked unverified (`src/runtimes/opencode.ts:54`).
- Spawn ignores permission and prompt fields: `opencode --model X` (`src/runtimes/opencode.ts:70`–`src/runtimes/opencode.ts:74`).
- Print uses `["opencode", "--prompt", prompt, "--format", "json"]` plus optional `--model`, both flags unverified (`src/runtimes/opencode.ts:91`–`src/runtimes/opencode.ts:97`).
- `deployConfig` writes only `AGENTS.md`; no hooks (`src/runtimes/opencode.ts:113`–`src/runtimes/opencode.ts:124`).
- `detectReady` always returns `loading` until real TUI (terminal user interface) strings are observed (`src/runtimes/opencode.ts:138`–`src/runtimes/opencode.ts:142`); `parseTranscript` always returns null (`src/runtimes/opencode.ts:155`–`src/runtimes/opencode.ts:159`); `getTranscriptDir` always returns null (`src/runtimes/opencode.ts:171`–`src/runtimes/opencode.ts:174`).
- `buildEnv` returns `model.env ?? {}` (`src/runtimes/opencode.ts:185`).

### 3.7 Cursor (`src/runtimes/cursor.ts`)
Cursor CLI (binary `agent`, not `cursor`): `id = "cursor"` (`src/runtimes/cursor.ts:38`), `experimental` (`src/runtimes/cursor.ts:41`), `instructionPath = ".cursor/rules/overstory.md"` (`src/runtimes/cursor.ts:44`).
- Spawn maps `bypass` to `--yolo` and ignores append-prompt fields (`src/runtimes/cursor.ts:62`–`src/runtimes/cursor.ts:70`).
- Print uses `["agent", "-p", prompt, "--yolo"]` plus optional `--model` (`src/runtimes/cursor.ts:83`–`src/runtimes/cursor.ts:89`).
- `deployConfig` writes only the rules file, creating `.cursor/rules/` (`src/runtimes/cursor.ts:105`–`src/runtimes/cursor.ts:115`).
- `detectReady` requires prompt (`❯` or `^> `) plus status (`shift+tab`, `esc`, or `agent`); never dialog (`src/runtimes/cursor.ts:131`–`src/runtimes/cursor.ts:144`).
- `parseTranscript` extracts model from `system/init` events only; tokens are always zero because Cursor stream-JSON (JavaScript Object Notation) exposes no usage (`src/runtimes/cursor.ts:156`–`src/runtimes/cursor.ts:189`).
- `buildEnv` returns `model.env ?? {}` (`src/runtimes/cursor.ts:197`); `getTranscriptDir` returns null (`src/runtimes/cursor.ts:202`).

### 3.8 Sapling (`src/runtimes/sapling.ts`)
Primary headless runtime (`sp` CLI): `id = "sapling"` (`src/runtimes/sapling.ts:346`), `stable` (`src/runtimes/sapling.ts:349`), `instructionPath = "SAPLING.md"` (`src/runtimes/sapling.ts:352`), `headless = true` (`src/runtimes/sapling.ts:358`).
- Tmux fallback spawn uses `sp run --model X --json` plus `SAPLING.md` prompt (`src/runtimes/sapling.ts:377`–`src/runtimes/sapling.ts:395`); print uses `["sp", "print"]` (`src/runtimes/sapling.ts:410`–`src/runtimes/sapling.ts:417`).
- `buildDirectSpawn` emits `sp run --json --cwd X --system-prompt-file Y` and resolves gateway aliases via `ANTHROPIC_DEFAULT_<ALIAS>_MODEL` with bare-alias fallbacks for `haiku/sonnet/opus` (`src/runtimes/sapling.ts:429`–`src/runtimes/sapling.ts:463`, fallbacks at `src/runtimes/sapling.ts:40`).
- `deployConfig` writes `SAPLING.md` conditionally and always writes `.sapling/guards.json` from `buildGuardsConfig` (`src/runtimes/sapling.ts:477`–`src/runtimes/sapling.ts:494`).
- Always ready (`src/runtimes/sapling.ts:506`) and no beacon verification (`src/runtimes/sapling.ts:517`).
- `parseTranscript` sums any `usage.input_tokens/output_tokens` and captures first `model` (`src/runtimes/sapling.ts:534`–`src/runtimes/sapling.ts:578`); `parseEvents` yields typed `AgentEvent` per NDJSON (newline-delimited JSON) line with buffered partial-line handling (`src/runtimes/sapling.ts:593`–`src/runtimes/sapling.ts:636`).
- Only adapter implementing `connect()`, returning `SaplingConnection` (`src/runtimes/sapling.ts:662`); connection maps `sendPrompt` to `steer`, `followUp` to `followUp`, `abort` to `abort`, and `getState` to JSON-RPC (JSON remote procedure call) 2.0 with timeout and background stdout draining (`src/runtimes/sapling.ts:280`–`src/runtimes/sapling.ts:316`).
- `buildEnv` clears `CLAUDECODE`, `CLAUDE_CODE_SSE_PORT`, `CLAUDE_CODE_ENTRYPOINT`, and `ANTHROPIC_API_KEY`, then maps `ANTHROPIC_AUTH_TOKEN` to `ANTHROPIC_API_KEY`, passes through `ANTHROPIC_BASE_URL`, forces `SAPLING_BACKEND=sdk` for gateways, and forwards `ANTHROPIC_DEFAULT_*_MODEL` (`src/runtimes/sapling.ts:666`–`src/runtimes/sapling.ts:703`).
- `getTranscriptDir` returns null because Sapling uses event streaming (`src/runtimes/sapling.ts:706`–`src/runtimes/sapling.ts:708`).

## 4. Guards: pi-guards and Sapling guards
Pi guard generator `generatePiGuardExtension(hooks)` (`src/runtimes/pi-guards.ts:128`) emits `.pi/extensions/overstory-guard.ts` in Pi ExtensionAPI (application programming interface) factory style (`src/runtimes/pi-guards.ts:93`). Guard order is fixed (`src/runtimes/pi-guards.ts:96`–`src/runtimes/pi-guards.ts:111`): block native team tools, block interactive tools, block write tools for non-implementation capabilities, enforce path boundary on write/edit, apply universal Bash (Bourne Again Shell) danger guards, then capability-specific Bash handling, then default allow.
- Non-implementation set covers `scout/reviewer/lead/coordinator/supervisor/monitor` (`src/runtimes/pi-guards.ts:26`); coordination subset adds `git add/commit` (`src/runtimes/pi-guards.ts:36`).
- Pi uses lowercase tool names (`write`, `edit`, `bash`) plus mixed-case compat, `event.toolName` (not `name`), and `event.input.path` (not `file_path`) (`src/runtimes/pi-guards.ts:143`, `src/runtimes/pi-guards.ts:241`, `src/runtimes/pi-guards.ts:279`).
- File-modifying Bash patterns are duplicated from hooks-deployer because the source list is not exported (`src/runtimes/pi-guards.ts:38`–`src/runtimes/pi-guards.ts:60`).
- Activity tracking prevents watchdog zombie-classification: fire-and-forget `ov log tool-start/tool-end` on `tool_call`/`tool_execution_end`, awaited `ov log session-end` on `agent_end` and `session_shutdown` fallback (`src/runtimes/pi-guards.ts:113`–`src/runtimes/pi-guards.ts:120`, emitted at `src/runtimes/pi-guards.ts:248`, `src/runtimes/pi-guards.ts:333`, `src/runtimes/pi-guards.ts:346`, `src/runtimes/pi-guards.ts:358`).
- Sapling mirrors the same policy as JSON (JavaScript Object Notation): `buildGuardsConfig` sets `pathBoundary`, `readOnly` for non-implementation roles, `blockedTools`, `writeToolsBlocked`, `writeToolNames`, `bashGuards` (`safePrefixes`, `dangerousPatterns`, `fileModifyingPatterns`), `qualityGates`, and `eventConfig` argv for `ov log` (`src/runtimes/sapling.ts:98`–`src/runtimes/sapling.ts:162`).

## 5. Session resume
None of the source files under review implement resume: `AgentRuntime` has no `resume`/`continue` method (`src/runtimes/types.ts:148`), and no adapter in `claude.ts`, `pi.ts`, `codex.ts`, `copilot.ts`, `gemini.ts`, `opencode.ts`, `cursor.ts`, or `sapling.ts` references resume. Resume appears only in design docs as a comparison row: transcript-based resume for Claude, `codex resume`, `--continue`/`--session` for Pi and OpenCode, history-based for Cline, `--restore-chat-history` for Aider (`docs/runtime-abstraction.md:756`).

## 6. Extensibility: adding a runtime
Per `docs/runtime-adapters.md:516`: create `src/runtimes/<name>.ts` as a class implementing `AgentRuntime` (`docs/runtime-adapters.md:520`), register `["name", () => new XRuntime()]` in `src/runtimes/registry.ts:16` (`docs/runtime-adapters.md:606`), add config types under `OverstoryConfig.runtime` if needed (`docs/runtime-adapters.md:623`), colocate tests as `src/runtimes/<name>.test.ts` with real temp-directory I/O (`docs/runtime-adapters.md:648`), then use `ov sling --runtime <name>` or set `runtime.default` (`docs/runtime-adapters.md:691`). If construction needs config like Pi, add a special case beside the Pi branch (`src/runtimes/registry.ts:79`, `docs/runtime-adapters.md:622`). Package metadata is `@os-eco/overstory-cli` (`package.json:2`) requiring Bun (JavaScript runtime) >= 1.0 (`package.json:36`).
**Covers:** src/runtimes/types.ts, src/runtimes/registry.ts, src/runtimes/claude.ts, src/runtimes/pi.ts, src/runtimes/copilot.ts, src/runtimes/codex.ts, src/runtimes/gemini.ts, src/runtimes/opencode.ts, src/runtimes/cursor.ts, src/runtimes/sapling.ts, src/runtimes/connections.ts, src/runtimes/pi-guards.ts, docs/runtime-abstraction.md, docs/runtime-adapters.md, package.json
