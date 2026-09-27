---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

# ByoCodingAgent — Retrieval Practice

## 1. Agent loop: what caps the `Send` → `loop` cycle, and what happens at the cap?

<details>
<summary>Answer</summary>

The loop iterates up to `MaxTurns` (root agent overrides it to **50** in `main.go`) until the model stops requesting tools. It exits when `StopReason != StopToolUse`, and errors with `max turns (%d) reached` if the cap is hit. Each turn compacts history, calls `Provider.Send`, appends the assistant message, executes `BlockToolUse` blocks, and feeds results back as a user message. Slash lines route via `runCommand`; everything else goes through `rootAgent.Send`.

</details>

## 2. Provider seam: what is the 3-method interface, and what does cost tracking return for unknown models?

<details>
<summary>Answer</summary>

The harness talks to LLMs only through `Send`, `Model`, `SetModel`. `AnthropicProvider` (reference implementation, sole Anthropic SDK importer) and `OpenAIProvider` (Chat Completions; e.g. gpt-4o, gpt-5, o3-mini) both accumulate `api.Usage` under a mutex, expose `TotalUsage()` and `EstimatedCostUSD()` — which returns **-1** for unknown models — and share subagent totals. OpenAI splits tool-result blocks into separate `role:"tool"` messages and wraps `InputSchema` properties into a full `{"type":"object",...}` envelope. `MockProvider` returns canned `Responses` in order with `RepeatLast`/`Err` controls for tests.

</details>

## 3. Compaction: why must a truncation boundary be "tool-pair-safe", and what breaks if it isn't?

<details>
<summary>Answer</summary>

Because a `tool_use` block is meaningless (and un-executable) without its matching `tool_result`, and vice versa. `SafeSplitPoint` walks backward from the desired index to the nearest plain-text user message, returning **0** ("do nothing") when no safe boundary exists, so truncation never splits a pair. Below-threshold input passes through unchanged; above it, `SlidingWindow{KeepLast}` keeps only the newest N messages while `Summarize{Threshold, KeepRecent}` replaces the dropped prefix with one synthetic `[earlier conversation summary]` user message from a single provider call.

</details>

## 4. Tool surface: how is a `write_file` call previewed, and what do the new-file and no-change cases look like?

<details>
<summary>Answer</summary>

`buildWriteDiff` renders it as a unified diff with **3** lines of context for the approval modal: a new file is synthesized as a `/dev/null` diff, and identical content gets a `(no changes...)` marker. The shared contract is `api.ToolDef` (`Name`, `Description`, `InputSchema`, `Required`). Each MCP server is bridged by one `mcp.Client` (stdio or Streamable HTTP), each remote tool adapted by `MCPTool` as `<server>_<name>` while calling the server with the original name; `Register` skips failed servers with a stderr warning instead of aborting. Multi-block MCP results flatten via `joinContent`, with `[non-text content block: %T]` for image/audio. MCP config is opt-in JSON (missing file returns `(nil, nil)`) with `${VAR}` expansion.

</details>

## 5. TUI: what breaks if approval defaults to "allow" on Enter/Esc instead of deny?

<details>
<summary>Answer</summary>

A stray keypress could authorize a destructive tool call (e.g. file write) the user never reviewed. Hence `Confirm(prompt string) bool` defaults Enter/Esc/Ctrl-C to **deny**, and the alt-screen approval modal (`ApprovalRequest{Prompt, Detail, Reply chan bool}`) approves only on `y` — everything else denies. A non-empty `Detail` opens the yellow full-screen diff modal with scrollable viewport. The `harness` model has three states (`stateIdle`, `stateRunning`, `stateAwaitingApproval`); the debug panel is **12** rows, toggled with `Tab`, with list/detail modes, arrow-key navigation, and mouse selection.

</details>

## 6. Transfer: a teammate wants to add a new permission policy to the harness — which track and recipe do you point them to, and what is the fastest orientation tour?

<details>
<summary>Answer</summary>

Point them to `how-to/` — it holds exactly three copy-paste recipes (add a tool, add a provider, add a permission policy), each bilingual (`en/` + `es/`). For orientation, send them on the fastest tour: `follow_along/` chapters **00, 01, 09, 11** (the three core abstractions: agent loop, tools, subagents, 5–10 min each; 14 core chapters 00–13 plus 6 extras 14–19 total). If they want to practice rather than copy, use `exercises/` (six graded tasks in difficulty order, each with goal, recap, file paths, acceptance criteria, stretch goals).

</details>

## 7. Evaluation: is human-approval-only sufficient safety, or is that a real gap?

<details>
<summary>Answer</summary>

See [[critical_thinking|Critical Analysis]] § "Weaknesses and blind spots." ByoCodingAgent's only safety mechanism is a human reading a unified diff before approving a destructive tool call (`buildWriteDiff`, deny-by-default `Confirm`) — there is no automated verification that the agent's output actually works (no test-execution loop, no self-critique pass). For a ~7k-line teaching harness this is a defensible simplification, since the reader is expected to watch every step; it would be an unacceptable gap in any unattended or production deployment, where a verification loop (run the tests, check the diff against acceptance criteria) would need to replace or supplement the human-in-the-loop gate.

</details>
