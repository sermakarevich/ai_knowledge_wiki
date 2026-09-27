> [[index|Wiki]] | [[summary|Summary]]

# ByoCodingAgent — Digest

The whole source at medium depth: every chapter's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-agent-loop|Agent loop and entrypoint]]

**In one sentence:** The root `Agent` runs a `Send` → `loop` tool-use cycle capped by `MaxTurns`, wired in `main.go` to a Bubble Tea runner that routes `/`-commands inline and everything else into the loop.

- `Agent` owns one conversation — provider, tool registry, compactor, and message slice — and serves both the root REPL and subagents (`internal/agent/agent.go:23`).
- `Send` appends a user message then calls `loop`, which iterates up to `MaxTurns` until the model stops requesting tools (`internal/agent/agent.go:63`).
- Each turn compacts history, calls `Provider.Send`, appends the assistant message, executes any `BlockToolUse` blocks, and feeds results back as a user message (`internal/agent/agent.go:74`).
- The loop exits when `StopReason != StopToolUse` and errors with `max turns (%d) reached` if the cap is hit (`internal/agent/agent.go:133`).
- `main.go` constructs the root agent with `agent.New(llm, activeSysPrompt, tool.Default)` and overrides `MaxTurns = 50` (`main.go:161`).
- The `runner` closure routes slash lines via `runCommand` and all other input via `rootAgent.Send` (`main.go:167`).
- `DelegateTool` exposes each subagent as a `delegate_<name>` tool with a single required `task` parameter (`delegate.go:26`).

## 2. [[wiki/02-provider|Provider seam: Anthropic/OpenAI/mock]]

**In one sentence:** The `Provider` interface (`Send`/`Model`/`SetModel`) decouples the agent loop from LLM backends, with `AnthropicProvider` and `OpenAIProvider` translating generic messages/tools to vendor SDK calls plus per-model cost tracking, and `MockProvider` serving canned responses for tests.

- The harness only talks to LLMs through the 3-method `Provider` interface — `Send`, `Model`, `SetModel` — so swapping models or SDKs means swapping implementations (`provider.go:12`).
- `AnthropicProvider` is the reference implementation and the only file importing the Anthropic SDK; it holds client, model, maxTokens, system prompt, and cumulative usage (`anthropic.go:18`).
- `OpenAIProvider` implements the same interface on Chat Completions and works for any chat-capable model such as gpt-4o, gpt-5, or o3-mini (`openai.go:18`).
- Both live providers accumulate `api.Usage` under a mutex, expose `TotalUsage()` and `EstimatedCostUSD()` (returning -1 for unknown models), and share subagent totals (`anthropic.go:47`, `openai.go:55`).
- Anthropic maps generic blocks to SDK params, enables adaptive thinking, maps stop reasons, and logs each call via the debug recorder (`anthropic.go:86`).
- OpenAI splits Anthropic-style tool-result blocks into separate `role:"tool"` messages and wraps `InputSchema` properties into a full `{"type":"object",...}` envelope (`openai.go:134`, `openai.go:195`).
- `MockProvider` returns canned `Responses` in order with `RepeatLast`/`Err` controls and records every `Send` input for test assertions (`mock.go:22`).
- Debug payload helpers render requests (tool names+descriptions, schemas elided) and responses (elapsed, usage, content) as pretty JSON for `/debug show` (`payloads.go:15`, `payloads.go:41`).

## 3. [[wiki/03-compaction-memory|Compaction strategies and session memory]]

**In one sentence:** Short-term context is truncated per-turn by a `CompactionStrategy` snapped to tool-pair-safe boundaries, while long-term context persists across sessions through a `memory.Store` whose default file-backed implementation writes one markdown file per session plus a JSON index.

- Every strategy implements `Compact(ctx, messages)` and is invoked at the top of each agent-loop turn, returning input unchanged below its threshold (`internal/compact/strategy.go:14`).
- `SafeSplitPoint` walks backward from the desired index to the nearest plain-text user message, returning 0 ("do nothing") when no safe boundary exists so a `tool_use` is never split from its `tool_result` (`internal/compact/strategy.go:23`).
- `SlidingWindow{KeepLast}` keeps only the newest N messages and `Summarize{Threshold, KeepRecent}` replaces the dropped prefix with a single synthetic `[earlier conversation summary]` user message produced by one provider call (`internal/compact/slidingwindow.go:12`, `internal/compact/summarize.go:14`).
- `LoggingStrategy{Inner, FilePath}` wraps any strategy and appends a before/after transcript only when the message count changed, via `WithLogging(inner, path)` (`internal/compact/logging.go:15`, `internal/compact/logging.go:21`).
- `memory.Store` is a three-method interface — `Save`, `Recall`, `Preamble` — with a package-level `Default` that falls back to no-op `NoMemory` (`internal/memory/store.go:40`, `internal/memory/store.go:49`).
- `SessionFiles` is the default `Store`: `<root>/sessions/*.md` per session plus `<root>/index.json` as the lookup layer, with missing files pruned silently at open (`internal/memory/sessionfiles.go:24`, `internal/memory/sessionfiles.go:45`).
- `Save` only buffers into an in-memory draft (flushed by `Close`), `Recall` is a case-insensitive substring scan over summary/tags ordered most-recent-first, and `Preamble` injects at most the last 5 session summaries into the system prompt (`internal/memory/sessionfiles.go:100`, `internal/memory/sessionfiles.go:114`, `internal/memory/sessionfiles.go:162`).

## 4. [[wiki/04-tools-mcp|Tool surface, diffs, MCP client]]

**In one sentence:** External MCP (Model Context Protocol — a standard for exposing tools from outside servers) servers are bridged into the agent's local tool registry with per-server clients, and shared types plus a unified-diff preview define the common tool surface.

- `api.ToolDef` (`internal/api/types.go:57`) is the shared tool contract with `Name`, `Description`, `InputSchema`, and `Required` fields used by both local and MCP-backed tools.
- `mcp.Client` (`internal/mcp/client.go:17`) wraps one connected MCP server session, with `NewStdioClient` (`internal/mcp/client.go:25`) for subprocess servers and `NewHTTPClient` (`internal/mcp/client.go:33`) for remote Streamable HTTP servers.
- `MCPTool` (`internal/mcp/register.go:18`) adapts one remote tool to the local `Tool` interface, exposing it as `<server>_<name>` while calling the server with the original name (`internal/mcp/register.go:144`).
- `Register` (`internal/mcp/register.go:103`) connects every configured server, lists and registers its tools, skips failed servers with a stderr warning instead of aborting, and returns open clients for the caller to close.
- `buildWriteDiff` (`internal/agent/diff.go:20`) renders a `write_file` call as a unified diff with 3 lines of context for the approval modal, synthesizing a `/dev/null` diff for new files and a `(no changes...)` marker for identical content.
- `joinContent` (`internal/mcp/client.go:95`) flattens multi-block MCP results to one string, rendering text natively and substituting a `[non-text content block: %T]` placeholder for image/audio blocks.
- `ServerConfig`/`Config` plus `LoadConfig` (`internal/mcp/register.go:49`) make MCP opt-in JSON configuration where a missing file returns `(nil, nil)`, and `${VAR}` environment expansion applies to commands, args, URLs, and headers.

## 5. [[wiki/05-ui|TUI: program, input, styles, compaction view]]

**In one sentence:** The `internal/ui` package implements the Bubble Tea terminal UI — a `harness` model with conversation viewport, input box, debug panel, approval modals, banner animation, and stdout helpers for spinner, highlight, and compaction views.

- The main TUI is a `harness` struct holding conversation `viewport`, bottom debug `viewport`, `textinput`, and `spinner` models plus window size, state, approval, focus, shine, MCP, and scrollback fields (`internal/ui/program.go:95`).
- Three model states drive interaction — `stateIdle`, `stateRunning`, `stateAwaitingApproval` — declared as a `modelState` enum (`internal/ui/program.go:87`).
- `NewProgram` captures terminal width before stdout redirection, builds the banner, and runs with alt-screen plus full mouse motion (`internal/ui/program.go:194`).
- User input echoes into scrollback with a timestamped turn divider, then dispatches via `AgentRunner` and flips to `stateRunning` with spinner tick (`internal/ui/program.go:426`).
- Approval uses `ApprovalRequest{Prompt, Detail, Reply chan bool}`; a non-empty `Detail` opens a yellow full-screen diff modal with scrollable viewport, `y` approves and everything else denies (`internal/ui/program.go:55`, `internal/ui/program.go:466`).
- The debug panel occupies `debugPanelHeight = 12` rows, toggles with `Tab`, supports list/detail modes with `↑/↓` navigation, `Enter` drill-in, `←/→` pair jumps, and mouse selection (`internal/ui/program.go:28`, `internal/ui/program.go:650`).
- Standalone (non-alt-screen) prompts live in `input.go`: `ReadChatInput() (string, bool)` with `↑↓` history from `~/.bettatech_harness_history`, and `Confirm(prompt string) bool` defaulting Enter/Esc/Ctrl-C to deny (`internal/ui/input.go:119`, `internal/ui/input.go:168`).

## 6. [[wiki/06-course-map|Course structure: lessons, exercises, how-tos]]

**In one sentence:** The repo teaches harness engineering through three parallel tracks — a 20-chapter narrative (`follow_along/`), three copy-paste recipes (`how-to/`), and six graded extension exercises (`exercises/`), all bilingual in English and Spanish.

- Three doc flavors serve three reader intents: narrative why, recipe how, and extension practice (`README.md:237-243`).
- `follow_along/` has 14 core chapters (00–13) plus 6 standalone extras (14–19), read in order at 5–10 min each (`follow_along/en/README.md:5-24`).
- The fastest tour is chapters 00, 01, 09, 11 — the three core abstractions: agent loop, tools, subagents (`follow_along/en/README.md:41-41`).
- `how-to/` holds exactly three recipes: add a tool, add a provider, add a permission policy (`how-to/en/README.md:7-9`).
- `exercises/` holds six tasks in rough difficulty order, each tied to one extension point (`exercises/en/README.md:3-14`).
- Every track is bilingual: `en/` and `es/` directories exist under `follow_along/`, `how-to/`, and `exercises/`.
- Exercises ship goal, recap, suggested steps with file paths, acceptance criteria, and stretch goals (`exercises/en/README.md:16-16`).

<!-- FIVE_MOVES_START -->
## The argument in five moves

1. A single Agent loop drives Send → tool-use cycles capped by MaxTurns.
2. A narrow Provider seam decouples that loop from Anthropic, OpenAI, or mock backends.
3. Per-turn compaction plus file-backed session memory keep context bounded yet persistent.
4. Local tools and remote MCP servers share one registry with diff-gated writes.
5. A Bubble Tea TUI wraps the loop with viewports, approvals, and debug inspection.
6. Three bilingual doc tracks turn the harness into a teachable build-your-own course.
<!-- FIVE_MOVES_END -->
