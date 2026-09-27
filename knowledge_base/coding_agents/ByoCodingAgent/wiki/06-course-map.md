> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Course structure: lessons, exercises, how-tos

**In one sentence:** The repo teaches harness engineering through three parallel tracks — a 20-chapter narrative (`follow_along/`), three copy-paste recipes (`how-to/`), and six graded extension exercises (`exercises/`), all bilingual in English and Spanish.

## Key points
- Three doc flavors serve three reader intents: narrative why, recipe how, and extension practice (`README.md:237-243`).
- `follow_along/` has 14 core chapters (00–13) plus 6 standalone extras (14–19), read in order at 5–10 min each (`follow_along/en/README.md:5-24`).
- The fastest tour is chapters 00, 01, 09, 11 — the three core abstractions: agent loop, tools, subagents (`follow_along/en/README.md:41-41`).
- `how-to/` holds exactly three recipes: add a tool, add a provider, add a permission policy (`how-to/en/README.md:7-9`).
- `exercises/` holds six tasks in rough difficulty order, each tied to one extension point (`exercises/en/README.md:3-14`).
- Every track is bilingual: `en/` and `es/` directories exist under `follow_along/`, `how-to/`, and `exercises/`.
- Exercises ship goal, recap, suggested steps with file paths, acceptance criteria, and stretch goals (`exercises/en/README.md:16-16`).

---

## The three tracks

The top-level README defines the intended reading order (`README.md:239-243`):

- `follow_along/` — "chapter-length narrative on the *why* of every layer in the harness, in the order it was built. Read in order; about an hour total."
- `how-to/` — "short recipe-style references for the extension tasks people actually do: add a tool, add a provider, add a permission policy."
- `examples/minimal/` is a fourth on-ramp (single-file agent loop) but outside this component's scope; the course map here covers only the three prose tracks.

All three tracks are mirrored in English and Spanish: `follow_along/en/` and `follow_along/es/`, `how-to/en/` and `how-to/es/`, `exercises/en/` and `exercises/es/` each contain the same file set.

## Follow-along: core arc (00–13)

Declared as "a chapter-by-chapter walk through how this harness came together" where "each chapter is short (5–10 min) and focuses on one design decision" (`follow_along/en/README.md:3-5`). Chapter table (`follow_along/en/README.md:11-24`):

| # | File | Title |
|---|---|---|
| 00 | `00-introduction.md` | Introduction |
| 01 | `01-the-agent-loop.md` | The agent loop |
| 02 | `02-the-permission-gate.md` | The permission gate |
| 03 | `03-the-provider-interface.md` | The provider interface |
| 04 | `04-ui-polish.md` | UI polish |
| 05 | `05-slash-commands.md` | Slash commands |
| 06 | `06-conversation-state.md` | Conversation state |
| 07 | `07-compaction-strategies.md` | Compaction strategies |
| 08 | `08-better-input.md` | Better input |
| 09 | `09-plug-and-play-tools.md` | Plug-and-play tools |
| 10 | `10-project-structure.md` | Project structure |
| 11 | `11-subagents.md` | Subagents |
| 12 | `12-full-tui.md` | The full TUI |
| 13 | `13-whats-next.md` | What's next |

The introduction frames three arcs (`follow_along/en/00-introduction.md:52-56`): "01–02, the bare minimum"; "03–08, abstractions earn their keep"; "09–12, the architecture pays off". Its closing chapter states "by the end of chapter 02 you have something that works. By the end of chapter 12 you have something that resembles a small Claude Code" (`follow_along/en/00-introduction.md:58-58`).

## Follow-along: extras (14–19)

Described as "standalone chapters that extend the harness with concrete integrations… aren't part of the core arc — read them when you want the feature" (`follow_along/en/README.md:28-28`). Table (`follow_along/en/README.md:32-37`):

| # | File | Title |
|---|---|---|
| 14 | `14-mcp-support.md` | Adding MCP support |
| 15 | `15-agents-md.md` | Project context with AGENTS.md |
| 16 | `16-token-viewer.md` | The token viewer |
| 17 | `17-prompt-caching.md` | Prompt caching |
| 18 | `18-diff-approval.md` | Diff approval for writes |
| 19 | `19-agent-memory.md` | Agent memory |

Chapter 13 bridges core to extras by listing deliberately skipped layers — streaming, tests, prompt caching, multi-line input, permission policies, MCP, persistence, token counting (`follow_along/en/13-whats-next.md:7-23`).

## How-to recipes

"Recipe-style references for the most common extension tasks… they tell you *how*, not *why*" (`how-to/en/README.md:3-3`). Index (`how-to/en/README.md:7-9`):

| Guide | When you need it |
|---|---|
| `add-a-tool.md` | The model needs a new capability |
| `add-a-provider.md` | Swap Anthropic for OpenAI, Bedrock, Ollama, or a mock |
| `add-a-permission-policy.md` | Something other than "ask every time" |

Add-a-tool recipe: "The tool registry uses `init()` self-registration, so adding a tool means dropping a file in `internal/tool/`. No edits to `main.go`." (`how-to/en/add-a-tool.md:5-5`). Canonical scaffold quoted verbatim (`how-to/en/add-a-tool.md:23-25`):

```go
type WebFetchTool struct{}

func init() { Default.Register(&WebFetchTool{}) }
```

Its conventions: "Return errors as tool results. `(message, true)` means 'this failed, here's why.'" (`how-to/en/add-a-tool.md:77-77`).

Add-a-provider recipe: "The `Provider` interface… is three methods" (`how-to/en/add-a-provider.md:5-5`). Signature quoted verbatim (`how-to/en/add-a-provider.md:39-46`):

```go
func (p *YourProvider) Send(ctx context.Context, messages []api.Message, tools []api.ToolDef) (api.Response, error) {
	req := p.toRequest(messages, tools)        // ↓ adapter
	sdkResp, err := p.client.Chat(ctx, req)
	if err != nil {
		return api.Response{}, err
	}
	return p.fromResponse(sdkResp), nil        // ↓ adapter
}
```

Wiring is one line: `llm := provider.NewYourProvider("gpt-4o", sysPrompt, 8192)` (`how-to/en/add-a-provider.md:77-77`).

Add-a-permission-policy recipe: "The harness ships with one strategy: `Agent.Confirm` is called on every tool call… There's no abstraction yet" (`how-to/en/add-a-permission-policy.md:5-5`). Interface quoted verbatim (`how-to/en/add-a-permission-policy.md:28-30`):

```go
type Policy interface {
	Decide(ctx context.Context, name, input string) (Decision, string)
}
```

Repeatable policies after the one-time refactor: `AlwaysAllow`, `AllowList{Names}`, `AskOnce`, `PathScoped{Inner}` (`how-to/en/add-a-permission-policy.md:92-229`).

## Exercises (01–06)

"Six extension exercises for the harness, in rough order of difficulty. Each one parallels an existing extension point (Provider, Tool, CompactionStrategy, Store, Subagent)" (`exercises/en/README.md:3-3`). Table (`exercises/en/README.md:9-14`):

| # | File | Layer | Difficulty |
|---|---|---|---|
| 1 | `01-tool-retry-on-error.md` | Agent loop | easy |
| 2 | `02-markdown-subagents.md` | Subagents | medium |
| 3 | `03-pluggable-memory.md` | Memory | medium |
| 4 | `04-transcript-renderer.md` | Transcript | medium |
| 5 | `05-streaming-responses.md` | Provider + UI | hard |
| 6 | `06-image-inputs.md` | API types + Provider | medium |

Exercise 1 (retry): "when a tool call fails, give the model one or two structured retries" (`exercises/en/01-tool-retry-on-error.md:3-3`), scaffold quoted verbatim (`exercises/en/01-tool-retry-on-error.md:26-29`):

```go
type RepairPolicy struct {
    MaxRetries int
    Note       func(toolName string, attempt, max int) string // returns the meta-note
}
```

Exercise 2 (markdown subagents): loader scans `.harness/agents/*.md`, "frontmatter configures the wrapper; the body is the system prompt" (`exercises/en/02-markdown-subagents.md:15-34`). Example frontmatter quoted verbatim (`exercises/en/02-markdown-subagents.md:18-23`):

```markdown
---
name: reviewer
description: Review a diff for bugs, unhandled errors, and security issues. Returns a bulleted list.
tools: [read_file, bash]
max_turns: 6
---
```

Exercise 3 (memory): "implement a second `memory.Store` and prove the existing harness doesn't know the difference" (`exercises/en/03-pluggable-memory.md:3-3`); pick `InMemoryRing{Capacity int}`, `SQLite{Path string}`, or `JSONBlob{Path string}` (`exercises/en/03-pluggable-memory.md:17-19`).

Exercise 4 (transcript renderer): "turn the single `RenderTranscript` function into a `Renderer` interface" (`exercises/en/04-transcript-renderer.md:3-3`). Signature quoted verbatim (`exercises/en/04-transcript-renderer.md:18-20`):

```go
type Renderer interface {
    Render(io.Writer, []Message) error
}
```

Exercise 5 (streaming): "render the assistant's reply token by token as it streams" (`exercises/en/05-streaming-responses.md:3-3`); chunk type quoted verbatim (`exercises/en/05-streaming-responses.md:34-39`):

```go
type Chunk struct {
    Kind  ChunkKind // TextDelta, ToolStart, ToolDelta, ToolEnd, Stop, Usage
    Text  string    // for TextDelta
    Block api.Block // for ToolEnd
    Usage *api.Usage
}
```

Exercise 6 (images): "let the user attach images to a turn" (`exercises/en/06-image-inputs.md:3-3`); block extension quoted verbatim (`exercises/en/06-image-inputs.md:22-31`):

```go
const BlockImage BlockType = "image"

type Block struct {
    // ... existing fields ...

    // BlockImage
    ImageSource    string // "base64" or "url"
    ImageMediaType string // "image/png", "image/jpeg", "image/webp", "image/gif"
    ImageData      string // base64 payload OR the URL, depending on Source
}
```

## How to navigate

- Fastest tour: "read chapter 00, then skim chapters 01, 09, 11 (the three core abstractions: agent loop, tools, subagents)" (`follow_along/en/README.md:41-41`).
- Build it yourself: "read in order, write the code for each chapter, then diff your work against the repo at HEAD" (`follow_along/en/README.md:43-43`).
- Extend it: jump to the matching `how-to/` recipe, which "assume you've read the corresponding `follow_along/` chapter" (`how-to/en/README.md:3-3`).
- Practice: "read the relevant `follow_along/` chapter first; these don't re-explain the why" (`exercises/en/README.md:5-5`).

**Covers:** component 06
