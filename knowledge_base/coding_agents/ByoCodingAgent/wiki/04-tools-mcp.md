> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Tool surface, diffs, MCP client

**In one sentence:** External MCP (Model Context Protocol — a standard for exposing tools from outside servers) servers are bridged into the agent's local tool registry with per-server clients, and shared types plus a unified-diff preview define the common tool surface.

## Key points

- `api.ToolDef` (`internal/api/types.go:57`) is the shared tool contract with `Name`, `Description`, `InputSchema`, and `Required` fields used by both local and MCP-backed tools.
- `mcp.Client` (`internal/mcp/client.go:17`) wraps one connected MCP server session, with `NewStdioClient` (`internal/mcp/client.go:25`) for subprocess servers and `NewHTTPClient` (`internal/mcp/client.go:33`) for remote Streamable HTTP servers.
- `MCPTool` (`internal/mcp/register.go:18`) adapts one remote tool to the local `Tool` interface, exposing it as `<server>_<name>` while calling the server with the original name (`internal/mcp/register.go:144`).
- `Register` (`internal/mcp/register.go:103`) connects every configured server, lists and registers its tools, skips failed servers with a stderr warning instead of aborting, and returns open clients for the caller to close.
- `buildWriteDiff` (`internal/agent/diff.go:20`) renders a `write_file` call as a unified diff with 3 lines of context for the approval modal, synthesizing a `/dev/null` diff for new files and a `(no changes...)` marker for identical content.
- `joinContent` (`internal/mcp/client.go:95`) flattens multi-block MCP results to one string, rendering text natively and substituting a `[non-text content block: %T]` placeholder for image/audio blocks.
- `ServerConfig`/`Config` plus `LoadConfig` (`internal/mcp/register.go:49`) make MCP opt-in JSON configuration where a missing file returns `(nil, nil)`, and `${VAR}` environment expansion applies to commands, args, URLs, and headers.

---

## Shared tool and message types

Provider-agnostic types in `internal/api/types.go:1` let providers, tools, and the agent loop share one vocabulary (`internal/api/types.go:1`).

Key definitions quoted verbatim:

```go
type Block struct {
	Type BlockType

	Text string // BlockText

	ToolUseID string // BlockToolUse, BlockToolResult
	ToolName  string // BlockToolUse
	ToolInput string // BlockToolUse — raw JSON, pass-through to provider

	ToolResult string // BlockToolResult
	IsError    bool   // BlockToolResult
}
```

```go
type ToolDef struct {
	Name        string
	Description string
	InputSchema map[string]any
	Required    []string
}
```

(`internal/api/types.go:27`, `internal/api/types.go:57`)

Other shared types (`internal/api/types.go:11`):

- `Role` with `RoleUser` / `RoleAssistant` (`internal/api/types.go:13`).
- `BlockType` with `BlockText`, `BlockToolUse`, `BlockToolResult` (`internal/api/types.go:20`).
- `Message` as `Role` plus `[]Block` (`internal/api/types.go:40`).
- `Message.HasToolResult` (`internal/api/types.go:48`) reports tool-result blocks, used by compaction to find safe split points (`internal/api/types.go:48`).
- `Response` with `Content`, `StopReason`, `Usage` (`internal/api/types.go:72`), and `StopReason` values `StopEndTurn`, `StopToolUse`, `StopOther` (`internal/api/types.go:66`).
- `Usage` with input/output plus cache-creation/cache-read counters (`internal/api/types.go:80`), summed by `Usage.Add` (`internal/api/types.go:89`).
- `RenderTranscript` (`internal/api/types.go:100`) serializes messages to `role: ...` lines with `[called <tool> with <input>]` and `[tool result: ...]` markers for summarization and compaction logs (`internal/api/types.go:100`).

## MCP client transports

`Client` wraps one server session (`internal/mcp/client.go:17`):

```go
type Client struct {
	Name    string
	session *sdk.ClientSession
}
```

Constructors quoted verbatim (`internal/mcp/client.go:25`, `internal/mcp/client.go:33`):

```go
func NewStdioClient(ctx context.Context, name, command string, args ...string) (*Client, error) {
	transport := &sdk.CommandTransport{Command: exec.Command(command, args...)}
	return connect(ctx, name, transport)
}
```

```go
func NewHTTPClient(ctx context.Context, name, endpoint string, headers map[string]string) (*Client, error) {
	httpClient := &http.Client{
		Transport: &headerRoundTripper{
			base:    http.DefaultTransport,
			headers: headers,
		},
	}
	transport := &sdk.StreamableClientTransport{
		Endpoint:   endpoint,
		HTTPClient: httpClient,
	}
	return connect(ctx, name, transport)
}
```

Details:

- `connect` (`internal/mcp/client.go:47`) builds an `sdk.Implementation{Name: "bettatech-harness", Version: "0.1"}` client and blocks on the initialize handshake (`internal/mcp/client.go:48`).
- HTTP auth headers ride every request via `headerRoundTripper.RoundTrip` (`internal/mcp/client.go:118`), which calls `req.Header.Set(k, v)` per configured header (`internal/mcp/client.go:118`).
- `ListTools` (`internal/mcp/client.go:59`) returns every tool the server exposes and is called once per server at startup with results cached in the local registry (`internal/mcp/client.go:59`).
- `CallTool` (`internal/mcp/client.go:71`) dispatches `&sdk.CallToolParams{Name: name, Arguments: arguments}` and returns `(joinContent(res.Content), res.IsError, nil)` (`internal/mcp/client.go:71`).
- `Close` (`internal/mcp/client.go:85`) is nil-safe and idempotent: stdio close terminates the subprocess, HTTP close tears down the persistent connection (`internal/mcp/client.go:85`).

## MCPTool bridge and registration

`MCPTool` makes a remote tool look local (`internal/mcp/register.go:17`):

```go
type MCPTool struct {
	Client *Client
	Def    api.ToolDef
	remoteName string
}
```

- `Definition()` returns `t.Def` (`internal/mcp/register.go:27`).
- `Execute(ctx, input)` (`internal/mcp/register.go:29`) unmarshals the Anthropic SDK's raw-JSON input into `map[string]any`, returns `"invalid tool input: ..."` on bad JSON, then delegates to `Client.CallTool(ctx, t.remoteName, args)` (`internal/mcp/register.go:29`).

Configuration quoted verbatim (`internal/mcp/register.go:49`, `internal/mcp/register.go:59`):

```go
type ServerConfig struct {
	Name      string            `json:"name"`
	Transport string            `json:"transport"` // "stdio" or "http"
	Command   string            `json:"command,omitempty"`
	Args      []string          `json:"args,omitempty"`
	URL       string            `json:"url,omitempty"`
	Headers   map[string]string `json:"headers,omitempty"`
}
```

```go
type Config struct {
	Servers []ServerConfig `json:"servers"`
}
```

- `LoadConfig` (`internal/mcp/register.go:65`) returns `(nil, nil)` when the file does not exist, so MCP is opt-in (`internal/mcp/register.go:65`).
- `dial` (`internal/mcp/register.go:159`) switches on `Transport`: `stdio` requires `Command` and expands env vars in command and args; `http` requires `URL` and expands env vars in URL and headers; anything else errors with `unknown transport %q (want stdio or http)` (`internal/mcp/register.go:159`).
- `Register` (`internal/mcp/register.go:103`) emits `ProgressBegin`/`ProgressDone` around the batch and `ProgressConnecting`/`ProgressConnected`/`ProgressFailed` per server via the `ProgressFunc func(server string, status ProgressStatus, total int)` callback (`internal/mcp/register.go:96`).
- Per-server failure handling in `Register` (`internal/mcp/register.go:118`): dial errors print `mcp: skip server %q: %v` and continue; list-tools errors print `mcp: list tools from %q failed`, close the client, and continue (`internal/mcp/register.go:118`).
- Schema adaptation via `splitSchema` (`internal/mcp/register.go:187`) converts the SDK's `any` input schema into `(properties, required)` for `api.ToolDef`; unrecognized schemas are skipped with `mcp: skip %s/%s: unrecognized input schema` (`internal/mcp/register.go:134`). `normalizeSchema` (`internal/mcp/register.go:207`) accepts `nil`, `map[string]any`, or `json.RawMessage`.
- Registered names are `s.Name + "_" + d.Name` to avoid collisions across servers (`internal/mcp/register.go:144`).

## Write diff preview

`buildWriteDiff(rawInput string) string` (`internal/agent/diff.go:20`) parses `{path, content}` JSON and returns a display-ready unified diff; malformed input returns `""` so the caller falls back to the plain approve prompt (`internal/agent/diff.go:20`).

- Existing files use `difflib.UnifiedDiff` with `FromFile: in.Path + " (current)"`, `ToFile: in.Path + " (proposed)"`, `Context: 3` (`internal/agent/diff.go:36`).
- New files go through `synthesizeNewFileDiff` (`internal/agent/diff.go:56`), which emits `--- /dev/null`, `+++ <path> (new file)`, an `@@ -0,0 +1,N @@` hunk header, and `+`-prefixed lines so the chroma diff lexer colors the body green (`internal/agent/diff.go:56`).
- Identical content returns `"(no changes: proposed content is identical to current file)\n"` so the modal still opens with a clear message (`internal/agent/diff.go:47`).
- Trailing-newline edge case: a missing final newline gets one appended to avoid line concatenation (`internal/agent/diff.go:67`).

**Covers:** component 04
