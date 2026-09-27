> [[index|Wiki]] | [[digest|Digest]]

# Technical Analysis: ByoCodingAgent (byo-coding-agent)

**Repository:** https://github.com/betta-tech/byo-coding-agent @ 77aa4db

---

## 1. Overview / What Problem It Solves

ByoCodingAgent ("build your own coding agent") is a small, teachable Go harness that wires a chat-style LLM to real tools, a terminal UI, session memory, and an external MCP (Model Context Protocol) bridge — plus a bilingual (English/Spanish) course (`follow_along/`, `how-to/`, `exercises/`) that teaches how each piece works by having the reader extend it. It is not aimed at production coding-agent users; it is a reference implementation sized to be read end to end, then rebuilt piece by piece. The whole non-course codebase is ~7.3k lines of Go (`wc -l` on `*.go` excluding `exercises/`).

## 2. Architecture / Layering

```text
main.go ──► agent.Agent (loop) ──► provider.Provider (Anthropic/OpenAI/Mock)
   │             │  │                        ▲
   │             │  └─► tool.Registry ◄── internal/mcp (remote tool bridge)
   │             └─► compact.CompactionStrategy
   │             └─► memory.Store (session persistence)
   └─► internal/ui (Bubble Tea TUI) ── ApprovalRequest channel ──► agent.Confirm
```

Four layers, cleanly seamed by interfaces: (1) `agent.Agent` (`internal/agent/agent.go:23`) is the conversation owner and the only thing that knows about turns; (2) `provider.Provider` (`internal/provider/provider.go:12`) is the LLM seam — a 3-method interface (`Send`, `Model`, `SetModel`) so the loop never imports a vendor SDK directly, only `anthropic.go`/`openai.go` do; (3) `tool.Registry` plus `internal/mcp` is the capability seam — local Go tools and remote MCP-server tools implement the same `Tool` interface; (4) `internal/ui` is presentation-only, driven by an `AgentRunner` callback and an `ApprovalRequest{Prompt, Detail, Reply chan bool}` channel (`internal/ui/program.go:55`), so the agent package has zero dependency on Bubble Tea. `main.go` is the composition root: it builds the provider, the root `Agent`, registers subagents and MCP tools, and wires the `Confirm` closure that bridges loop-side tool approval to UI-side modal (`main.go:161`, `main.go:230`).

## 3. Macro Components

| Component | Package | Responsibility | Key file:line |
|---|---|---|---|
| Agent loop | `internal/agent` | Send→loop tool-use cycle, MaxTurns cap, tool dispatch, diff-gated approval | `internal/agent/agent.go:23`, `internal/agent/agent.go:71` |
| Provider seam | `internal/provider` | LLM-agnostic interface + Anthropic/OpenAI/Mock implementations, cost tracking | `internal/provider/provider.go:12`, `anthropic.go:18`, `openai.go:18`, `mock.go:22` |
| Compaction | `internal/compact` | Per-turn context truncation at tool-pair-safe boundaries | `internal/compact/strategy.go:14,23` |
| Session memory | `internal/memory` | Cross-session persistence: `Save`/`Recall`/`Preamble` over markdown+JSON index | `internal/memory/store.go:40`, `internal/memory/sessionfiles.go:24` |
| Tool surface + MCP | `internal/tool`, `internal/mcp`, `internal/api` | Shared `ToolDef` contract, local tools (bash/read/write/remember/recall), remote MCP bridge | `internal/api/types.go:57`, `internal/mcp/register.go:103` |
| Subagents | `internal/subagent`, `delegate.go` | Delegated sub-conversations exposed as `delegate_<name>` tools | `delegate.go:26` |
| TUI | `internal/ui` | Bubble Tea `harness` model: viewport, input, debug panel, approval modal | `internal/ui/program.go:95` |
| Debug recorder | `internal/debug` | Structured request/response logging surfaced via `/debug show` | `payloads.go:15,41` |
| Entrypoint/wiring | `main.go`, `commands.go` | Composition root, slash-command router, provider/MCP/subagent bootstrap | `main.go:94`, `commands.go:96` |
| Course | `follow_along/`, `how-to/`, `exercises/` | 20-chapter narrative, 3 recipes, 6 graded exercises, bilingual | `follow_along/en/README.md:5-24` |

## 4. Data Flow

A user line goes through `runner` (`main.go:167`): slash lines are handled by `runCommand` (`commands.go:96`) and consumed; everything else calls `rootAgent.Send(ctx, input)`. `Send` appends a user `api.Message` and calls `loop` (`internal/agent/agent.go:63`). Each turn: (a) `Compactor.Compact` trims history if needed (`internal/agent/agent.go:76`); (b) `Provider.Send(ctx, messages, tools)` calls the live model (`internal/agent/agent.go:100`); (c) the response is appended as an assistant message (`internal/agent/agent.go:105`); (d) `BlockText` streams to stdout/finalText, `BlockToolUse` blocks are dispatched via `executeTool`, gated by `Confirm` for destructive calls with a diff preview built by `buildWriteDiff` (`internal/agent/diff.go:20`), and results are appended as a new user message (`internal/agent/agent.go:110-133`). The loop exits when `StopReason != StopToolUse`, or errors with `max turns (%d) reached` at the `MaxTurns` cap — 50 for the root agent (`main.go:161`), 20 by default (`internal/agent/agent.go:38`). Tool calls to a `delegate_<name>` tool re-enter this same loop inside a subagent with its own (usually smaller) tool registry (`delegate.go:40`).

## 5. State Management

In-process state is a single `[]api.Message` slice owned by `Agent` (`internal/agent/agent.go:23`, accessors at `internal/agent/agent.go:50`), reset by `/clear` → `rootAgent.ClearMessages()` (`commands.go:215`). Across turns, size is bounded by `CompactionStrategy` (`SlidingWindow` or `Summarize`, never splitting a `tool_use`/`tool_result` pair — `internal/compact/strategy.go:23`). Across process restarts, state is persisted by `memory.Store`: the default `SessionFiles` implementation writes one markdown file per session under `<root>/sessions/*.md` plus a `<root>/index.json` lookup index, prunes missing files silently on open, buffers `Save` in memory until `Close` flushes it, and injects at most the last 5 session summaries into the next system prompt via `Preamble` (`internal/memory/sessionfiles.go:24,45,100,114,162`). Provider-side state is per-provider cumulative `api.Usage` guarded by a mutex, shared with subagent totals (`anthropic.go:47`, `openai.go:55`). UI-side state is the `harness` struct's `modelState` enum (`stateIdle`/`stateRunning`/`stateAwaitingApproval`, `internal/ui/program.go:87,95`).

## 6. Tool Surface

Shared contract: `api.ToolDef{Name, Description, InputSchema, Required}` (`internal/api/types.go:57`) is implemented uniformly by local tools (`internal/tool`: `bash.go`, `readfile.go`, `writefile.go`, `remember.go`, `recall.go`) and by MCP-backed tools. `MCPTool` (`internal/mcp/register.go:18`) adapts one remote tool as `<server>_<name>`, calling the server with its original name (`internal/mcp/register.go:144`); `Register` (`internal/mcp/register.go:103`) connects every configured server, skips failures with a stderr warning rather than aborting the whole registry, and `LoadConfig` treats a missing MCP config file as a no-op (`(nil, nil)`) with `${VAR}` environment expansion for commands/args/URLs/headers (`internal/mcp/register.go:49`). `mcp.Client` supports both stdio subprocess servers and remote Streamable HTTP servers (`internal/mcp/client.go:17,25,33`). Writes are diff-gated: `buildWriteDiff` renders a unified diff with 3 lines of context, synthesizing a `/dev/null` diff for new files and a `(no changes...)` marker for identical content (`internal/agent/diff.go:20`).

## 7. Verification Story

There is no runtime type/schema verification beyond what Go's compiler and the provider SDKs enforce; correctness is established mostly by unit tests (see §9) plus human-in-the-loop approval gates. The one built-in safety mechanism is the diff-gated approval flow: destructive tool calls (e.g., `write_file`) surface a human-readable diff through `ApprovalRequest{Prompt, Detail, Reply chan bool}` (`internal/ui/program.go:55`), and `Confirm(prompt string) bool` defaults `Enter`/`Esc`/`Ctrl-C` to **deny** — only `y` approves (`internal/ui/input.go:168`, `internal/ui/program.go:466`). There is no automated "did the agent's output actually work" check (no test-execution loop, no self-critique pass) — verification is entirely the human operator reading the diff before approving.

## 8. Error Handling

Errors are handled locally and non-fatally at almost every seam rather than propagated as panics: a failed MCP server is skipped with a stderr warning, not aborting `Register` (`internal/mcp/register.go:103`); a missing MCP config file returns `(nil, nil)` instead of an error (`internal/mcp/register.go:49`); unknown slash commands print `unknown command: /%s (try /help)` but still count as handled (`commands.go:107`); `EstimatedCostUSD()` returns `-1` rather than erroring for unrecognized models (`anthropic.go:47`); a denied tool call returns the string `"user denied this tool call"` as a tool result, letting the model react instead of crashing the loop (`internal/agent/agent.go:144`); non-text MCP content becomes a `[non-text content block: %T]` placeholder instead of failing `joinContent` (`internal/mcp/client.go:95`). The one hard failure mode is `MaxTurns` exhaustion, which returns `fmt.Errorf("max turns (%d) reached", a.MaxTurns)` (`internal/agent/agent.go:139`) — a fail-loud cap rather than an infinite loop.

## 9. Testing

Seven `_test.go` files cover the core seams directly: `internal/compact/strategy_test.go` (safe-split-point logic), `internal/memory/sessionfiles_test.go` (save/recall/preamble), `internal/agent/agent_test.go` and `internal/agent/diff_test.go` (loop behavior and diff rendering), `internal/api/types_test.go`, `internal/tool/registry_test.go`, and `internal/debug/debug_test.go`. `MockProvider` (`mock.go:22`) — canned `Responses` played back in order with `RepeatLast`/`Err` controls, recording every `Send` input — is the seam that makes `agent_test.go` possible without a live LLM call. There is no end-to-end test that drives the TUI or a real MCP server; those paths are exercised manually per the README/course, not by CI-visible tests in this clone.

## 10. How to Extend

The course encodes exactly three sanctioned extension points via `how-to/{en,es}`: add a tool, add a provider, add a permission policy (`how-to/en/README.md:7-9`). Concretely: a new provider implements `Send`/`Model`/`SetModel` (`provider.go:12`) and is wired in `newProviderByName` (`main.go:287`); a new tool implements the `Tool` interface and is registered into `tool.Default`/a subagent's registry; a new MCP server is added to the JSON config consumed by `LoadConfig` (`internal/mcp/register.go:49`) with no code change required. `exercises/{en,es}` ships six graded tasks, each tied to one such extension point with goal, recap, file paths, acceptance criteria, and stretch goals (`exercises/en/README.md:3-14,16`). The fastest orientation path for a new contributor is `follow_along/` chapters 00, 01, 09, 11 — the three core abstractions: agent loop, tools, subagents (`follow_along/en/README.md:41`).

## 11. Verdict

This is a well-seamed teaching artifact, not a production coding agent: every axis that matters for extension (LLM backend, tool set, compaction policy, memory backend, UI) sits behind a narrow interface with one reference implementation, and the accompanying course turns the codebase itself into the documentation. Its intentional limits — a fixed `MaxTurns` cap, substring-scan session recall, last-5-summaries-only memory injection, human-only approval as the sole safety net, no automated agent-output verification — are appropriate for a ~7k-line teaching repo and would need to be revisited (real semantic recall, output verification loop, configurable safety policy) before treating it as anything beyond a build-your-own-harness reference.
