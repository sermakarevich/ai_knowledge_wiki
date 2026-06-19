# Technical Analysis: pi-coding-agent

**Repository:** https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent
**Package:** `@mariozechner/pi-coding-agent`
**Version analyzed:** 0.72.1
**Date:** 2026-05-03

---

## 1. Overview / What Problem It Solves

Most AI coding agents accumulate features until they dictate the developer's workflow: fixed plan modes, hardcoded permission gates, MCP as the only extension protocol, mandatory sub-agent designs. `pi-coding-agent` ("pi") takes the opposite position: ship the minimal viable coding agent and let users extend it in TypeScript. The core bets that a good extension API removes the need for most baked-in features.

The primary users are human developers who want a terminal coding agent they can shape to their workflow without forking the repo. Secondary users are developers embedding pi programmatically via its SDK, or integrating it into external processes via RPC mode.

Pi provides four built-in tools (`read`, `bash`, `edit`, `write`) plus three read-only extras (`grep`, `find`, `ls`), session persistence with tree branching, LLM-context compaction, and a TypeScript extension API that can replace or wrap nearly every behavior -- including the editor, footer, compaction logic, and tools themselves.

---

## 2. High-Level Architecture

```
  CLI args / stdin
        │
        ▼
  src/main.ts  ─────────────────────────────────────────┐
  (mode dispatch)                                        │
        │                                                │
        ├─► InteractiveMode (pi-tui TUI)                 │
        ├─► PrintMode / JsonMode                         │
        ├─► RpcMode (JSONL over stdin/stdout)            │
        └─► SDK (createAgentSession)                     │
                                                         │
  All modes share:                                       │
        │                                                │
        ▼                                                │
  AgentSession  ◄──── ExtensionRunner ◄── Extension TSX │
  (agent-session.ts)       │                             │
        │                  └── events, tools, commands   │
        ├─► Agent (pi-agent-core)                        │
        │       └─► pi-ai (LLM providers)                │
        ├─► SessionManager (JSONL on disk)               │
        ├─► ToolRegistry (read/bash/edit/write/...)      │
        ├─► ResourceLoader (skills/prompts/themes)       │
        ├─► SettingsManager (global+project JSON)        │
        └─► PackageManager (npm/git packages)            │
                                                         │
  Persistent state: ~/.pi/agent/sessions/<cwd-hash>/    │
```

**Data flow for one interactive turn:**

1. User types a message in the TUI editor and presses Enter.
2. `InteractiveMode` calls `AgentSession.prompt(text, options)` (`agent-session.ts:965`).
3. `AgentSession` fires `ExtensionRunner` `input` event; extensions can modify or cancel the message.
4. The session builds the system prompt (`buildSystemPrompt`), resolves active tools, calls `Agent.run()` from `pi-agent-core`, which streams to the configured `pi-ai` provider.
5. As the agent emits `tool_call` events, `AgentSession` dispatches them through `ExtensionRunner`, then executes the matching tool (bash, read, edit, write, or an extension tool).
6. Tool results are appended to the in-flight message; `turn_end` is fired when the assistant stops.
7. The full exchange is persisted as JSONL entries in the session file via `SessionManager`.

**Persistent state:** JSONL files at `~/.pi/agent/sessions/<cwd-hash>/`, one file per session. Each line is a `FileEntry` (header or a session entry with `id`/`parentId` forming a tree).

---

## 3. The AgentSession

`AgentSession` (`src/core/agent-session.ts:243`) is the central class shared by all run modes. It is not a state machine in the strict sense -- it is a coordinator that owns:

- **Agent reference** -- the underlying `Agent` from `pi-agent-core` that drives LLM calls and tool dispatch.
- **Tool registry** -- a map from tool name → `ToolDefinition`, populated at construction from built-in tools + extension tools + SDK custom tools. The active set is a subset controlled by `--tools` / `--no-tools` flags and runtime `setToolEnabled()` calls.
- **Session tree** -- delegated to `SessionManager`; `AgentSession` writes entries after each event and reads them to rebuild context for compaction.
- **Extension runner** -- `ExtensionRunner` instance that holds all loaded extensions and routes lifecycle events.
- **Message queue** -- steering messages (interruptive) and follow-up messages (post-turn), managed internally and drained at turn boundaries.

Key methods:

| Method | Location | What it does |
|---|---|---|
| `prompt(text, opts)` | `:965` | Full turn: preflight, queue, LLM call, persistence |
| `compact(instructions?)` | `:1608` | Manual context compaction |
| `cycleModel(direction)` | `:1437` | Switch model forward/backward through scoped list |
| `switchSession(path)` | internal | Replace active session file in-place |
| `fork()` | internal | Copy active branch into a new session file |
| `_rebuildSystemPrompt()` | `:916` | Reconstruct system prompt after tool set changes |

**Session entry types** (defined in `src/core/session-manager.ts`):

| Type | Participates in LLM context? | Purpose |
|---|---|---|
| `message` | Yes | User/assistant messages |
| `compaction` | Yes (as summary) | Replaces older messages with LLM-generated summary |
| `branch_summary` | Yes | Summary injected when switching branches |
| `custom_message` | Yes | Extension-injected user messages |
| `custom` | No | Extension-specific opaque data for state persistence |
| `model_change` | No | Model switch marker |
| `thinking_level_change` | No | Thinking level marker |
| `label` | No | User bookmark on any entry |
| `session_info` | No | Display name metadata |

---

## 4. LLM / External Service Integration

Pi does not call LLMs directly -- it delegates entirely to `@mariozechner/pi-ai`, which provides a unified multi-provider API. The `pi-coding-agent` package is responsible for:

- Resolving the model (via `ModelRegistry`, `model-resolver.ts`) and auth credentials (via `AuthStorage`).
- Constructing the system prompt (`buildSystemPrompt` in `system-prompt.ts`).
- Passing the session context as an `AgentMessage[]` array to `Agent.run()`.

The LLM is never called directly from `coding-agent` source; all streaming and token accounting flows back through `pi-agent-core` events.

**Auth surface:** `AuthStorage` (`auth-storage.ts:14KB`) stores API keys and OAuth tokens in `~/.pi/agent/auth.json`. OAuth credentials (Anthropic, OpenAI, GitHub Copilot) flow through `oauth.ts` in `pi-ai`.

**Startup network calls (two, both optional):**

- Version check: `GET https://pi.dev/api/latest-version` -- disable with `PI_SKIP_VERSION_CHECK=1`.
- Install telemetry: `POST https://pi.dev/api/report-install` -- disable with `PI_TELEMETRY=0` or `enableInstallTelemetry: false` in settings.
- Both: disable with `PI_OFFLINE=1` or `--offline`.

---

## 5. The Prompt Pipeline

One full agentic turn from user input to persisted response:

1. **Input preflight** (`agent-session.ts:965`) -- checks model is set, API key available, no concurrent turn running; errors emit `notify` and return early.
2. **Extension input event** -- `ExtensionRunner.emitInput()` fires; extensions can modify the text, inject images, or cancel the turn.
3. **Skill block injection** -- if the message contains a `<skill name="..." location="...">` block (from `/skill:name` expansion in `skills.ts`), the block is prepended to the system prompt for this turn only.
4. **Prompt template expansion** -- `expandPromptTemplate()` (`prompt-templates.ts`) replaces `/templatename` with the template file content, filling `{{placeholders}}` interactively.
5. **System prompt build** -- `_rebuildSystemPrompt()` assembles: base instructions + active tool descriptions + skill content + context files (AGENTS.md / CLAUDE.md) + extension system prompt contributions.
6. **Agent.run()** -- `pi-agent-core` streams the LLM response. Each streaming chunk fires `turn_start`, `message_update`, and tool events through `AgentSession`'s event listener.
7. **Tool dispatch** -- on `tool_call`, `AgentSession` invokes the registered `ToolDefinition.execute()`, passing result back to the agent. Extensions intercept via `ExtensionRunner.emitToolCall()` and can override results or cancel calls.
8. **Auto-retry** -- on context overflow (`isContextOverflow` from `pi-ai`), compaction is triggered and the turn is retried (up to `MAX_AUTO_RETRIES`). Events `auto_retry_start` / `auto_retry_end` are emitted.
9. **Persistence** -- after `turn_end`, the complete `AgentMessage[]` for the turn is written as `message` entries to the JSONL session file via `SessionManager`.
10. **Queue drain** -- steering / follow-up messages queued during the turn are dispatched in order.

---

## 6. Key Files

| File | Lines (approx.) | What It Does |
|---|---|---|
| `src/core/agent-session.ts` | ~2,500 | Central class: prompt loop, tool registry, compaction, session branching, extension binding |
| `src/modes/interactive/interactive-mode.ts` | ~4,400 | Full TUI: editor, message rendering, commands, keyboard, overlays |
| `src/core/package-manager.ts` | ~1,800 | Install/update/remove packages from npm or git; config enable/disable |
| `src/core/session-manager.ts` | ~1,050 | JSONL read/write, tree traversal, `buildSessionContext()` |
| `src/core/extensions/types.ts` | ~1,350 | Complete `ExtensionAPI`, `ExtensionContext`, `ExtensionUIContext` interfaces |
| `src/core/extensions/runner.ts` | ~800 | Extension lifecycle: load, emit events, collect results, keybinding conflict detection |
| `src/core/extensions/loader.ts` | ~450 | Dynamic TypeScript loading via `@mariozechner/jiti` |
| `src/core/compaction/compaction.ts` | ~650 | Pure compaction logic: summarize context, track file ops, write `CompactionEntry` |
| `src/core/model-registry.ts` | ~800 | Model discovery, API-key resolution, subscription OAuth flow |
| `src/core/settings-manager.ts` | ~830 | Merge global + project settings; drain parse errors |
| `src/core/resource-loader.ts` | ~800 | Discover skills, prompts, themes, context files from global + project dirs |
| `src/core/tools/bash.ts` | ~400 | Bash tool: sandboxed exec, operation hooks, timeout handling |
| `src/core/tools/edit.ts` | ~400 | Edit tool: diff-based patching, conflict detection |
| `src/core/tools/read.ts` | ~390 | Read tool: file content with truncation, image detection |
| `src/core/sdk.ts` | ~340 | `createAgentSession()` public SDK entry point |
| `src/main.ts` | ~590 | CLI entry: arg parsing, mode dispatch, startup sequence |
| `src/cli/args.ts` | ~380 | Argument parsing (all flags, modes, env overrides) |
| `src/core/auth-storage.ts` | ~350 | Credential persistence (API keys + OAuth tokens) |
| `src/modes/rpc/rpc-mode.ts` | ~550 | JSONL-over-stdin/stdout RPC protocol handler |
| `src/core/skills.ts` | ~360 | Skill discovery, SKILL.md parsing, system prompt injection |

---

## 7. Dependencies

| Package | Version | Purpose |
|---|---|---|
| `@mariozechner/pi-agent-core` | `^0.72.1` | Agent runtime: tool calling, AgentMessage types, ThinkingLevel |
| `@mariozechner/pi-ai` | `^0.72.1` | Unified LLM API: providers, streaming, OAuth |
| `@mariozechner/pi-tui` | `^0.72.1` | Terminal UI: differential rendering, editor, overlays |
| `@mariozechner/jiti` | `^2.6.2` | TypeScript runtime for loading extension files at startup |
| `yaml` | `^2.8.2` | AGENTS.md / skill frontmatter parsing |
| `glob` | `^13.0.1` | File discovery for resource loading |
| `ignore` | `^7.0.5` | `.gitignore`-style filtering in file tools |
| `diff` | `^8.0.2` | Diff rendering in edit tool output |
| `marked` | `^15.0.12` | Markdown rendering in TUI messages |
| `chalk` | `^5.5.0` | Terminal color output |
| `proper-lockfile` | `^4.1.2` | File locking for concurrent session writes |
| `extract-zip` | `^2.0.1` | Package install from zip archives |
| `undici` | `^7.19.1` | HTTP client for package downloads and version checks |
| `uuid` | `^14.0.0` | `uuidv7` for session and entry IDs |
| `typebox` | `^1.1.24` | JSON schema / type validation for tool input definitions |
| `file-type` | `^21.1.1` | MIME detection for image attachments |
| `@silvia-odwyer/photon-node` | `^0.3.4` | Image resizing before LLM attachment |
| `hosted-git-info` | `^9.0.2` | Parse git URL formats for package manager |
| `minimatch` | `^10.2.3` | Glob matching in tool path filtering |
| `strip-ansi` | `^7.1.0` | Strip ANSI codes for plain-text export |
| `cli-highlight` | `^2.1.11` | Syntax highlighting in TUI code blocks |
| `@mariozechner/clipboard` | `^0.3.5` (optional) | Native clipboard access for paste |

---

## 8. CLI / Usage Surface

**Entry point:** `dist/cli.js` (Node), `dist/pi` (Bun binary), registered as `pi` in `package.json:bin`.

**Core invocation patterns:**

```bash
pi                                  # Interactive mode
pi -p "summarize this codebase"     # Print mode, exits after response
pi --mode json "list files"         # JSON event stream
pi --mode rpc                       # RPC over stdin/stdout

# Session management
pi -c                               # Continue most recent session
pi -r                               # Browse sessions
pi --session <path|uuid>            # Specific session
pi --fork <path|uuid>               # Fork into new session

# Model selection
pi --provider anthropic --model claude-3-7-sonnet
pi --model openai/gpt-4o
pi --model sonnet:high              # Model + thinking level shorthand
pi --thinking high

# Tool control
pi --tools read,grep,find,ls -p "review"   # Read-only
pi --no-builtin-tools -e ./my-ext.ts       # Extensions only
pi --no-tools                              # No tools

# Package management
pi install npm:@foo/pi-tools
pi install git:github.com/user/repo@v1
pi remove npm:@foo/pi-tools
pi update --extensions
pi list
pi config
```

**Environment variables:**

| Variable | Default | Purpose |
|---|---|---|
| `PI_CODING_AGENT_DIR` | `~/.pi/agent` | Override config directory |
| `PI_CODING_AGENT_SESSION_DIR` | `<agentDir>/sessions` | Override session storage |
| `PI_PACKAGE_DIR` | `<agentDir>/git` | Override git package directory |
| `PI_OFFLINE` | unset | Disable all startup network ops |
| `PI_SKIP_VERSION_CHECK` | unset | Skip version fetch from pi.dev |
| `PI_TELEMETRY` | unset | `0`/`false`/`no` to disable install ping |
| `PI_CACHE_RETENTION` | unset | `long` for extended prompt cache |
| `VISUAL` / `EDITOR` | unset | External editor for Ctrl+G |

**Configuration files:**

| Path | Purpose |
|---|---|
| `~/.pi/agent/settings.json` | Global settings (all projects) |
| `.pi/settings.json` | Project-local settings (overrides global) |
| `~/.pi/agent/auth.json` | Credentials (API keys, OAuth tokens) |
| `~/.pi/agent/AGENTS.md` | Global context file |
| `.pi/SYSTEM.md` / `~/.pi/agent/SYSTEM.md` | System prompt replacement |
| `APPEND_SYSTEM.md` | Appends to system prompt without replacing |
| `~/.pi/agent/keybindings.json` | Keybinding overrides |
| `~/.pi/agent/models.json` | Custom model/provider definitions |

---

## 9. Extensibility Points

- **Custom tools** -- implement `ToolDefinition<TInput, TDetails>` from `src/core/extensions/types.ts` and call `pi.registerTool(def)` in an extension factory. The tool is automatically injected into the LLM's tool list and appears in `/hotkeys` output. Built-in tools can be replaced entirely by registering a tool with the same name.

- **Custom providers / models** -- call `pi.registerProvider(config)` in an async extension factory (factory can be `async` so it awaits remote model discovery before startup continues). `ProviderConfig` is defined in `src/core/extensions/types.ts`. Alternatively, add entries to `~/.pi/agent/models.json` for providers speaking OpenAI/Anthropic/Google APIs without writing code.

- **Commands** -- call `pi.registerCommand("name", handler)` in an extension. Commands appear when the user types `/` and can open custom TUI components via `ctx.ui.custom()`.

- **Keyboard shortcuts** -- call `pi.registerShortcut(keyId, handler)` in an extension. Conflicts with reserved system keybindings (`app.interrupt`, `tui.input.submit`, etc.) are detected at load time and reported as diagnostics. See reserved list at `src/core/extensions/runner.ts:18-36`.

- **Custom compaction** -- handle `ctx.on("session_before_compact", handler)` in an extension. Return `{ handled: true, result }` to replace pi's default LLM-based summarization entirely (e.g., to implement structured/artifact-aware compaction).

- **Custom editor component** -- call `ctx.ui.setEditorComponent(factory)` where factory returns a class extending `CustomEditor` from the public API (`src/modes/interactive/components/custom-editor.ts`). Override `handleInput()` and call `super.handleInput()` for unhandled keys to preserve app-level shortcuts.

- **New skill** -- create `SKILL.md` (Agent Skills standard) in `~/.pi/agent/skills/<name>/` or `.pi/skills/<name>/`. No code required; pi discovers and injects it on startup. Skills can be packaged into Pi Packages and published to npm.

- **Pi Package** -- add a `"pi"` key to `package.json` with `extensions`, `skills`, `prompts`, and `themes` arrays pointing to source directories. Publish to npm with keyword `pi-package`. Users install via `pi install npm:<package>`.

---

## 10. Limitations and Gotchas

- **No MCP built in** -- MCP is explicitly excluded by design. Users who need MCP must build an extension that starts an MCP client and wraps tools, or install a third-party pi package. The README links to the rationale post.

- **No sub-agents or plan mode built in** -- same design philosophy. Both require extensions or third-party packages. The codebase has no native orchestration for parallel agent runs.

- **Compaction is lossy** -- `compact()` summarizes context via an LLM call and discards the original messages from the active window. The JSONL file retains the full history, but the LLM no longer sees it. The summary quality depends on the compaction model used and `keepRecentTokens` setting.

- **Extension execution is fully trusted** -- extensions run as arbitrary TypeScript with full `process` access. The README explicitly warns: "Pi packages run with full system access." There is no sandbox, permission gate, or capability restriction for extension code.

- **Session JSONL lock contention** -- `proper-lockfile` is used for concurrent writes, but two simultaneous `pi` processes on the same session file (e.g., running pi twice in the same directory without `--session`) will contend on the lock. The second process will fail to acquire it.

- **`interactive-mode.ts` is a monolith** -- at ~180KB it handles TUI layout, all command dispatch, component lifecycle, and event wiring. There is no internal component abstraction that cleanly separates concerns.

- **Bun binary is a separate build target** -- `src/bun/cli.ts` wraps the Node entry for Bun compilation. Divergences between Node and Bun runtime behavior (e.g., `restore-sandbox-env.ts`) are handled with bespoke shims rather than a unified abstraction.

- **Extension TypeScript is loaded via `@mariozechner/jiti`** -- a fork of the `jiti` TS runtime. Extensions must be valid TypeScript compatible with jiti's transpilation (no decorators by default, no certain advanced transforms). Type errors in extensions produce runtime load failures, not compile-time warnings.

- **`models.generated.ts` must not be edited directly** -- the file is generated by `packages/ai/scripts/generate-models.ts`. Manual edits are overwritten on the next `npm run build` in the `ai` package (per AGENTS.md).

- **Windows / Termux support is documented but not tested in CI** -- CI runs on Linux only (`.github/workflows/ci.yml`). The README links to separate Windows and Termux docs, flagging known issues.

---

## 11. How It Compares to Alternatives

**Claude Code** -- Anthropic's official coding agent CLI. Provides built-in plan mode, sub-agents via the Agent SDK, MCP support, and permission popups. Pi deliberately omits all of these and offers extension hooks where Claude Code bakes behavior in. Claude Code's extension story (hooks, slash commands) is narrower than pi's full TypeScript extension API. Pi supports many more LLM providers.

**Aider** -- Python-based, Git-first coding assistant. Strong at multi-file diffs and commit-centric workflows. Aider's architecture is opinionated about git usage; pi has no Git integration in the core (extensions can add it). Aider lacks a TUI extension API; pi's is its central feature.

**Cline (VS Code extension)** -- Deep IDE integration, visual diffs, browser tool. Runs inside VS Code only. Pi is terminal-first and IDE-agnostic. Cline has MCP and plan mode built in; pi leaves those to extensions.

**OpenCode** -- Another TypeScript terminal coding agent (one of several appearing in 2025). Also extensible and multi-provider. Pi differentiates with its session tree/branching model, the Pi Package ecosystem, and the explicit "no MCP, no sub-agents by default" philosophy that keeps the core footprint small.

**Positioning:** Pi is the terminal coding agent for developers who want to own their workflow: minimal core, full-replacement extension API, and a package ecosystem for distributing capabilities without forking.

---

## Appendix: Selected Code Snippets

**`AgentSession.prompt()` -- turn entry point** (`src/core/agent-session.ts:965`)

```typescript
async prompt(text: string, options?: PromptOptions): Promise<void> {
    // ... preflight: model check, concurrent-turn guard ...
    const inputResult = await this._extensionRunner.emitInput({ text, images, source });
    if (inputResult?.cancel) return;
    const effectiveText = inputResult?.text ?? text;

    // Skill block injection
    const skillBlock = parseSkillBlock(effectiveText);
    const skillSystemPromptAddition = skillBlock
        ? `\n\n<skill ...>\n${skillBlock.content}\n</skill>`
        : undefined;

    // LLM call via pi-agent-core
    await this._agent.run({
        messages: await this._buildContext(),
        systemPrompt: this._baseSystemPrompt + (skillSystemPromptAddition ?? ""),
        tools: this._resolveActiveTools(),
        onEvent: (event) => this._handleAgentEvent(event),
    });
}
```

**`SessionEntry` union type** (`src/core/session-manager.ts`)

```typescript
export type SessionEntry =
    | SessionMessageEntry       // type: "message"
    | ThinkingLevelChangeEntry  // type: "thinking_level_change"
    | ModelChangeEntry          // type: "model_change"
    | CompactionEntry           // type: "compaction"   -- LLM summary replaces older messages
    | BranchSummaryEntry        // type: "branch_summary"
    | CustomEntry               // type: "custom"       -- extension opaque state
    | CustomMessageEntry        // type: "custom_message" -- extension-injected LLM context
    | LabelEntry                // type: "label"        -- user bookmark
    | SessionInfoEntry;         // type: "session_info" -- display name
```

**Extension tool registration** (`src/core/extensions/types.ts`, simplified)

```typescript
export default function (pi: ExtensionAPI) {
    pi.registerTool({
        name: "deploy",
        description: "Deploy to staging",
        input: Type.Object({ env: Type.String() }),
        execute: async (input, ctx) => {
            const ok = await ctx.ui.confirm("Deploy?", `Target: ${input.env}`);
            if (!ok) return { type: "text", text: "Cancelled." };
            // ... run deploy ...
            return { type: "text", text: "Deployed." };
        },
    });
}
```

**`createAgentSession()` SDK entry** (`src/core/sdk.ts`)

```typescript
export async function createAgentSession(
    opts: CreateAgentSessionOptions = {},
): Promise<CreateAgentSessionResult> {
    const agentDir   = opts.agentDir   ?? getAgentDir();
    const authStorage  = opts.authStorage  ?? AuthStorage.create(agentDir);
    const modelRegistry = opts.modelRegistry ?? ModelRegistry.create(authStorage, agentDir);
    const sessionManager = opts.sessionManager ?? SessionManager.create(opts.cwd ?? process.cwd());
    const settingsManager = opts.settingsManager
        ?? SettingsManager.create(opts.cwd ?? process.cwd(), agentDir);
    // ... resolve model, load extensions, create AgentSession ...
    return { session, extensionsResult, modelFallbackMessage };
}
```
