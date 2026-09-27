> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Provider seam: Anthropic/OpenAI/mock

**In one sentence:** The `Provider` interface (`Send`/`Model`/`SetModel`) decouples the agent loop from LLM backends, with `AnthropicProvider` and `OpenAIProvider` translating generic messages/tools to vendor SDK calls plus per-model cost tracking, and `MockProvider` serving canned responses for tests.

## Key points

- The harness only talks to LLMs through the 3-method `Provider` interface — `Send`, `Model`, `SetModel` — so swapping models or SDKs means swapping implementations (`provider.go:12`).
- `AnthropicProvider` is the reference implementation and the only file importing the Anthropic SDK; it holds client, model, maxTokens, system prompt, and cumulative usage (`anthropic.go:18`).
- `OpenAIProvider` implements the same interface on Chat Completions and works for any chat-capable model such as gpt-4o, gpt-5, or o3-mini (`openai.go:18`).
- Both live providers accumulate `api.Usage` under a mutex, expose `TotalUsage()` and `EstimatedCostUSD()` (returning -1 for unknown models), and share subagent totals (`anthropic.go:47`, `openai.go:55`).
- Anthropic maps generic blocks to SDK params, enables adaptive thinking, maps stop reasons, and logs each call via the debug recorder (`anthropic.go:86`).
- OpenAI splits Anthropic-style tool-result blocks into separate `role:"tool"` messages and wraps `InputSchema` properties into a full `{"type":"object",...}` envelope (`openai.go:134`, `openai.go:195`).
- `MockProvider` returns canned `Responses` in order with `RepeatLast`/`Err` controls and records every `Send` input for test assertions (`mock.go:22`).
- Debug payload helpers render requests (tool names+descriptions, schemas elided) and responses (elapsed, usage, content) as pretty JSON for `/debug show` (`payloads.go:15`, `payloads.go:41`).

---

## Interface

The seam is defined verbatim (`provider.go:12`):

```go
type Provider interface {
	Send(ctx context.Context, messages []api.Message, tools []api.ToolDef) (api.Response, error)
	Model() string
	SetModel(name string)
}
```

Package doc verbatim (`provider.go:1`):

```go
// Package provider defines the LLM-backend interface and houses each
// concrete implementation. The harness only talks to providers through
// the Provider interface — swap implementations to swap models or SDKs.
```

## AnthropicProvider

Struct verbatim (`anthropic.go:18`):

```go
type AnthropicProvider struct {
	client    anthropic.Client
	model     anthropic.Model
	maxTokens int64
	system    string

	mu    sync.Mutex
	total api.Usage // cumulative across every Send call on this provider
}
```

Constructor verbatim (`anthropic.go:28`):

```go
func NewAnthropicProvider(model anthropic.Model, maxTokens int64, system string) *AnthropicProvider {
	return &AnthropicProvider{
		client:    anthropic.NewClient(),
		model:     model,
		maxTokens: maxTokens,
		system:    system,
	}
}
```

`Model`/`SetModel` verbatim (`anthropic.go:37`):

```go
func (p *AnthropicProvider) Model() string { return string(p.model) }
func (p *AnthropicProvider) SetModel(name string) {
	p.mu.Lock()
	p.model = anthropic.Model(name)
	p.mu.Unlock()
}
```

`Send` builds `anthropic.MessageNewParams` with model, max tokens, system text block, converted messages/tools, and adaptive thinking enabled (`anthropic.go:86`):

```go
resp, err := p.client.Messages.New(ctx, anthropic.MessageNewParams{
	Model:     p.model,
	MaxTokens: p.maxTokens,
	System:    []anthropic.TextBlockParam{{Text: p.system}},
	Messages:  p.toMessages(messages),
	Tools:     p.toTools(tools),
	Thinking: anthropic.ThinkingConfigParamUnion{
		OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
	},
})
```

Response mapping keeps only text and tool_use blocks, converting to `api.Block{Type: api.BlockText}` and `api.Block{Type: api.BlockToolUse, ToolUseID, ToolName, ToolInput}` (`anthropic.go:106`); usage maps `InputTokens`, `OutputTokens`, `CacheCreationInputTokens`, `CacheReadInputTokens` into `api.Usage` and adds to the cumulative total under lock (`anthropic.go:121`). Every call is wrapped in debug recording: `debug.Recordp` before send and `Recordfc`/`Recordpc` after (`anthropic.go:88`).

Usage and cost verbatim (`anthropic.go:47`):

```go
func (p *AnthropicProvider) TotalUsage() api.Usage {
	p.mu.Lock()
	defer p.mu.Unlock()
	return p.total
}
```

```go
func (p *AnthropicProvider) EstimatedCostUSD() float64 {
	p.mu.Lock()
	u := p.total
	model := string(p.model)
	p.mu.Unlock()
	rates, ok := modelPricing[model]
	if !ok {
		return -1
	}
	return float64(u.InputTokens)*rates.InputPerMillion/1_000_000 +
		float64(u.OutputTokens)*rates.OutputPerMillion/1_000_000 +
		float64(u.CacheCreationTokens)*rates.CacheCreationPerMillion/1_000_000 +
		float64(u.CacheReadTokens)*rates.CacheReadPerMillion/1_000_000
}
```

Pricing table verbatim (`anthropic.go:79`):

```go
var modelPricing = map[string]pricing{
	"claude-opus-4-7":   {InputPerMillion: 15.00, OutputPerMillion: 75.00, CacheCreationPerMillion: 18.75, CacheReadPerMillion: 1.50},
	"claude-opus-4-6":   {InputPerMillion: 15.00, OutputPerMillion: 75.00, CacheCreationPerMillion: 18.75, CacheReadPerMillion: 1.50},
	"claude-sonnet-4-6": {InputPerMillion: 3.00, OutputPerMillion: 15.00, CacheCreationPerMillion: 3.75, CacheReadPerMillion: 0.30},
	"claude-haiku-4-5":  {InputPerMillion: 1.00, OutputPerMillion: 5.00, CacheCreationPerMillion: 1.25, CacheReadPerMillion: 0.10},
}
```

Message conversion maps `BlockText` via `anthropic.NewTextBlock`, `BlockToolUse` via `ToolUseBlockParam{ID, Name, Input}`, `BlockToolResult` via `NewToolResultBlock`, then wraps in user/assistant messages (`anthropic.go:137`). Tool conversion maps `ToolDef{Name, Description, InputSchema, Required}` to `ToolParam{Name, Description, InputSchema{Properties, Required}}` (`anthropic.go:167`). Stop-reason mapping verbatim (`anthropic.go:184`):

```go
func fromStopReason(s anthropic.StopReason) api.StopReason {
	switch s {
	case anthropic.StopReasonEndTurn:
		return api.StopEndTurn
	case anthropic.StopReasonToolUse:
		return api.StopToolUse
	default:
		return api.StopOther
	}
}
```

## OpenAIProvider

Struct verbatim (`openai.go:21`):

```go
type OpenAIProvider struct {
	client    openai.Client
	model     string
	system    string
	maxTokens int64

	mu    sync.Mutex
	total api.Usage
}
```

Constructor verbatim (`openai.go:34`):

```go
func NewOpenAIProvider(model, system string, maxTokens int64) *OpenAIProvider {
	return &OpenAIProvider{
		client:    openai.NewClient(),
		model:     model,
		system:    system,
		maxTokens: maxTokens,
	}
}
```

`Send` calls Chat Completions verbatim (`openai.go:83`):

```go
resp, err := p.client.Chat.Completions.New(ctx, openai.ChatCompletionNewParams{
	Model:               shared.ChatModel(model),
	Messages:            p.toMessages(messages),
	Tools:               p.toTools(tools),
	MaxCompletionTokens: param.NewOpt(p.maxTokens),
})
```

Empty-choices guard verbatim (`openai.go:94`):

```go
if len(resp.Choices) == 0 {
	return api.Response{StopReason: api.StopOther}, nil
}
```

Usage maps `PromptTokens`/`CompletionTokens`/`PromptTokensDetails.CachedTokens`; cache-creation is not tracked because OpenAI only returns cached (read) tokens (`openai.go:112`). Cost uses only input/output/cache-read rates and returns -1 for unknown models (`openai.go:61`).

Pricing verbatim (`openai.go:239`):

```go
var openaiPricing = map[string]openaiRates{
	"gpt-4o":      {InputPerMillion: 2.50, OutputPerMillion: 10.00, CacheReadPerMillion: 1.25},
	"gpt-4o-mini": {InputPerMillion: 0.15, OutputPerMillion: 0.60, CacheReadPerMillion: 0.075},
	"gpt-5":       {InputPerMillion: 1.25, OutputPerMillion: 10.00, CacheReadPerMillion: 0.125},
	"gpt-5-codex": {InputPerMillion: 1.25, OutputPerMillion: 10.00, CacheReadPerMillion: 0.125},
	"gpt-5-mini":  {InputPerMillion: 0.25, OutputPerMillion: 2.00, CacheReadPerMillion: 0.025},
	"o1":          {InputPerMillion: 15.00, OutputPerMillion: 60.00, CacheReadPerMillion: 7.50},
	"o3-mini":     {InputPerMillion: 1.10, OutputPerMillion: 4.40, CacheReadPerMillion: 0.55},
}
```

Message translation has two notable splits documented in code (`openai.go:128`): user messages gather text parts joined by newline and emit each tool_result as its own `openai.ToolMessage(b.ToolResult, b.ToolUseID)` (`openai.go:141`); assistant turns merge text and tool calls into one message with `.Content` and `.ToolCalls` populated (`openai.go:159`). The system prompt is prepended as `openai.SystemMessage(p.system)` when non-empty (`openai.go:136`). Tool translation wraps the inner properties map into a full envelope (`openai.go:195`):

```go
parameters := map[string]any{
	"type":       "object",
	"properties": t.InputSchema,
}
```

Finish-reason mapping verbatim (`openai.go:219`):

```go
func fromFinishReason(r string) api.StopReason {
	switch r {
	case "stop":
		return api.StopEndTurn
	case "tool_calls":
		return api.StopToolUse
	default:
		return api.StopOther
	}
}
```

## MockProvider

Struct verbatim (`mock.go:22`):

```go
type MockProvider struct {
	// Responses is consumed front-to-back. The i-th Send returns
	// Responses[i] (or a fall-through depending on RepeatLast — see below).
	Responses []api.Response

	// RepeatLast, when true, causes the final element of Responses to be
	// returned for every Send after the slice is exhausted. Useful for
	// tests that need a "loops forever" provider (e.g. asserting that
	// Agent.MaxTurns kicks in). When false (the default) Send returns a
	// plain end_turn response once Responses is empty.
	RepeatLast bool

	// Err, if non-nil, is returned from every Send call instead of a
	// response. Lets tests exercise error-handling paths in the agent
	// loop. Responses is ignored while Err is set.
	Err error

	// ModelName backs Model() / SetModel(). Defaults to "mock" when zero.
	ModelName string

	mu    sync.Mutex
	sent  [][]api.Message
	tools [][]api.ToolDef
	calls int
}
```

Constructor verbatim (`mock.go:55`):

```go
func NewMockProvider(responses ...api.Response) *MockProvider {
	return &MockProvider{Responses: responses}
}
```

`Send` returns `Err` if set, otherwise the next canned response (repeat-last or default `api.Response{StopReason: api.StopEndTurn}`), recording defensive copies of messages/tools (`mock.go:61`). Introspection helpers are `Calls()`, `SentAt(i)`, and `LastSent()` (`mock.go:104`, `mock.go:114`, `mock.go:124`); all methods are mutex-guarded for concurrent subagent use (`mock.go:20`).

## Debug payload helpers

Request helper signature verbatim (`payloads.go:15`):

```go
func marshalRequestPayload(model, system string, maxTokens int64, messages []api.Message, tools []api.ToolDef) string {
```

It emits `{model, max_tokens, system, tools, messages}` where tools are briefs of name+description with schemas elided (`payloads.go:24`). Response helper signature verbatim (`payloads.go:41`):

```go
func marshalResponsePayload(resp api.Response, elapsed time.Duration) string {
```

It emits `{elapsed, stop_reason, usage, content}` so expensive calls are visible at a glance (`payloads.go:42`).

**Covers:** component 02
