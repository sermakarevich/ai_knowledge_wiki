> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Agent loop and entrypoint

**In one sentence:** The root `Agent` runs a `Send` → `loop` tool-use cycle capped by `MaxTurns`, wired in `main.go` to a Bubble Tea runner that routes `/`-commands inline and everything else into the loop.

## Key points

- `Agent` owns one conversation — provider, tool registry, compactor, and message slice — and serves both the root REPL and subagents (`internal/agent/agent.go:23`).
- `Send` appends a user message then calls `loop`, which iterates up to `MaxTurns` until the model stops requesting tools (`internal/agent/agent.go:63`).
- Each turn compacts history, calls `Provider.Send`, appends the assistant message, executes any `BlockToolUse` blocks, and feeds results back as a user message (`internal/agent/agent.go:74`).
- The loop exits when `StopReason != StopToolUse` and errors with `max turns (%d) reached` if the cap is hit (`internal/agent/agent.go:133`).
- `main.go` constructs the root agent with `agent.New(llm, activeSysPrompt, tool.Default)` and overrides `MaxTurns = 50` (`main.go:161`).
- The `runner` closure routes slash lines via `runCommand` and all other input via `rootAgent.Send` (`main.go:167`).
- `DelegateTool` exposes each subagent as a `delegate_<name>` tool with a single required `task` parameter (`delegate.go:26`).

---

## Agent struct and construction

The conversation owner is defined verbatim (`internal/agent/agent.go:23`):

```go
type Agent struct {
	Name      string                     // shown in the spinner label; "" for root
	Provider  provider.Provider          //
	Tools     *tool.Registry             // curated registry for this agent
	Compactor compact.CompactionStrategy //
	System    string                     // system prompt
	MaxTurns  int                        // hard cap on tool-use iterations
	Verbose   bool                       // print compaction before/after
	LogPrefix string                     // prefix for tool-call log lines
	Quiet     bool                       // suppress assistant-text printing (set for subagents)
	Confirm   func(prompt, detail string) bool // nil = auto-approve every tool call. detail is optional long-form (e.g. a diff)

	messages []api.Message
}
```

The constructor sets defaults verbatim (`internal/agent/agent.go:38`):

```go
func New(p provider.Provider, system string, tools *tool.Registry) *Agent {
	return &Agent{
		Provider:  p,
		Tools:     tools,
		System:    system,
		Compactor: compact.NoCompaction{},
		MaxTurns:  20,
	}
}
```

History accessors are `Messages`, `SetMessages`, and `ClearMessages` (`internal/agent/agent.go:50`); `/clear` calls `rootAgent.ClearMessages()` (`commands.go:215`).

## Send and loop

Entry signature verbatim (`internal/agent/agent.go:63`):

```go
func (a *Agent) Send(ctx context.Context, prompt string) (string, error) {
	a.messages = append(a.messages, api.Message{
		Role:    api.RoleUser,
		Content: []api.Block{{Type: api.BlockText, Text: prompt}},
	})
	return a.loop(ctx)
}
```

Loop header verbatim (`internal/agent/agent.go:71`):

```go
func (a *Agent) loop(ctx context.Context) (string, error) {
	var finalText strings.Builder

	for turn := 0; turn < a.MaxTurns; turn++ {
```

Per-turn sequence (`internal/agent/agent.go:75`):

1. Compaction: `a.Compactor.Compact(ctx, before)` runs first; on error it prints and records a debug event and continues (`internal/agent/agent.go:76`).
2. Provider call: `a.Provider.Send(ctx, a.messages, a.Tools.Definitions())` (`internal/agent/agent.go:100`).
3. Append: the response is appended as `api.Message{Role: api.RoleAssistant, Content: resp.Content}` (`internal/agent/agent.go:105`).
4. Content scan: `BlockText` is printed unless `Quiet` and accumulated into `finalText`; `BlockToolUse` is dispatched via `executeTool` and collected as `BlockToolResult` blocks (`internal/agent/agent.go:110`).
5. Stop check verbatim (`internal/agent/agent.go:133`):

```go
	if resp.StopReason != api.StopToolUse || !hasToolCall {
		return strings.TrimSpace(finalText.String()), nil
	}

	a.messages = append(a.messages, api.Message{Role: api.RoleUser, Content: toolResults})
```

6. Cap error verbatim (`internal/agent/agent.go:139`):

```go
	return strings.TrimSpace(finalText.String()), fmt.Errorf("max turns (%d) reached", a.MaxTurns)
```

Tool dispatch prints `[tool] <name> <input>`, records a debug event, builds an approval prompt (with diff detail for `write_file`), and honors `Confirm` denial with `"user denied this tool call"` (`internal/agent/agent.go:144`).

## Entrypoint wiring in main

Package comment states the harness wiring intent (`main.go:1`): `// Package main wires the harness together.` Construction happens after provider selection and `registerSubagents(llm)` (`main.go:159`), verbatim (`main.go:161`):

```go
	rootAgent = agent.New(llm, activeSysPrompt, tool.Default)
	rootAgent.Compactor = compact.NoCompaction{}
	rootAgent.MaxTurns = 50
```

System prompt composition is `systemPrompt + loadAgentsContext()` plus the memory preamble (`main.go:100`); the provider is built by `newProvider(activeSysPrompt)` (`main.go:112`).

The input router is verbatim (`main.go:167`):

```go
	runner := func(ctx context.Context, input string) error {
		if runCommand(input) {
			return nil
		}
		_, err := rootAgent.Send(ctx, input)
		return err
	}
```

Slash dispatch returns true when handled and false to fall through to the model (`commands.go:96`); unknown commands print `unknown command: /%s (try /help)` yet still return handled (`commands.go:107`).

Approval flow is a `Confirm` closure that posts `ui.ApprovalRequest` and blocks on the reply channel (`main.go:230`):

```go
	rootAgent.Confirm = func(prompt, detail string) bool {
		reply := make(chan bool, 1)
		program.Send(ui.ApprovalRequest{Prompt: prompt, Detail: detail, Reply: reply})
		return <-reply
	}
```

The TUI program is built with `ui.NewProgram(runner, usageFunc)` where `usageFunc` reads totals from `rootAgent.Provider` so `/provider` swaps propagate (`main.go:181`); stdout is piped into `ui.AppendMsg` and the program runs via `program.Run()` (`main.go:240`).

## Delegate tool as a second loop entry

`DelegateTool` wraps one subagent (`delegate.go:22`) with definition verbatim (`delegate.go:26`):

```go
func (d *DelegateTool) Definition() api.ToolDef {
	return api.ToolDef{
		Name:        "delegate_" + d.Subagent.Name(),
		Description: d.Subagent.Description(),
		InputSchema: map[string]any{
			"task": map[string]any{
				"type":        "string",
				"description": "Concrete description of what the subagent should do.",
			},
		},
		Required: []string{"task"},
	}
}
```

Execution unmarshals `{task}`, prints `↳ delegating to %s subagent`, calls `Subagent.Run(ctx, in.Task)`, prints `← %s subagent done (%s)`, and returns the subagent's final answer as the tool result (`delegate.go:40`); subagents are registered in `registerSubagents` with a `read_file`-only subset plus one `DelegateTool` per subagent (`main.go:422`).

**Covers:** component 01
