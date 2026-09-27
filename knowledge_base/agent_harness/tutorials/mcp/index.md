# MCP tutorial

MCP (Model Context Protocol) is an open standard that lets LLM apps — like Claude Desktop or Claude Code — call external tools, read external data, and use prompt templates, all through one common protocol instead of a bespoke integration per app. This project has two halves: a small **MCP server** (`weather/`) that exposes weather tools, and a generic **MCP client** (`mcp-client/`) that connects to any MCP server and lets Claude use its tools in a chat loop.

## What this project does

- `weather/weather.py` is an MCP server built with `FastMCP("weather")` from the `mcp` Python SDK. It talks to the US National Weather Service API (`https://api.weather.gov`, no API key required) and exposes:
  - `get_alerts(state: str) -> str` — active weather alerts for a two-letter US state code (e.g. `CA`).
  - `get_forecast(latitude: float, longitude: float) -> str` — next 5 forecast periods for a lat/lon point.
  - `formatted_summary(question: str) -> str` — an `@mcp.prompt` template (a reusable prompt, not a tool) with a "Claudia" persona.
  - `content_weather(file: str)` — an `@mcp.resource` that reads a local file by name.
  - `get_models()` — a resource returning a hardcoded fake model list (demo only).
  - `greeting://{name}` / `greeting://` — trivial "Hello, {name}!" resources.
  The server runs over **stdio transport** (`mcp.run(transport='stdio')`) — it's launched as a subprocess and talks to its client over stdin/stdout, not HTTP.
- `weather/resources.py` is a separate, standalone example of a lower-level MCP server (using the raw `Server` class instead of `FastMCP`) that lists and reads files in its working directory as resources. It is **not** wired into `weather.py` — it's a second reference snippet, not part of the running server.
- `mcp-client/client.py` implements `MCPClient`, a generic client that:
  1. Spawns any MCP server script (Python or Node) as a subprocess via `stdio_client(StdioServerParameters(...))`.
  2. Opens an `mcp.ClientSession` and lists the server's available tools.
  3. Sends a user query plus the tool list to a Claude model (`claude-3-5-sonnet-20241022`), executes any `tool_use` calls the model makes via `session.call_tool(...)`, and feeds results back for a follow-up answer.
  4. Runs an interactive `chat_loop()` REPL.

In short: `weather/` is a tool provider, `mcp-client/` is a tool consumer — run them together to see an LLM answer weather questions using live NWS data.

## Prerequisites

- [`uv`](https://docs.astral.sh/uv/) — Python package/dependency manager used by both projects (`pyproject.toml` + `uv.lock`).
- Python `>=3.10`.
- An `ANTHROPIC_API_KEY` environment variable (for `mcp-client/` only — it calls the Anthropic API directly). Put it in a `.env` file inside `mcp-client/` (loaded via `python-dotenv`); never commit `.env`.
- No key needed for the weather server itself — the NWS API is open.

## Run it

Start from two terminals.

**1. Run the weather MCP server standalone** (mostly for sanity-checking; normally it's spawned by the client):
```bash
cd knowledge/research_topics/agent_harness/tutorials/mcp/weather
uv sync
uv run weather.py
```
`weather/justfile` also defines `just format` (ruff format), `just lint` (ruff check), and `just test` (pytest — note: no tests actually exist yet). Its `just run` recipe calls `uvicorn weather:mcp --reload`, which is stale/incorrect — the server uses stdio transport, not an ASGI app, so prefer `uv run weather.py` directly.

**2. Run the client against the weather server:**
```bash
cd knowledge/research_topics/agent_harness/tutorials/mcp/mcp-client
uv sync
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env   # your own key, do not commit
uv run client.py ../weather/weather.py
```
The client connects to the server (spawning it as a subprocess), lists its tools, and drops you into a chat prompt. Ask something like "what's the weather forecast for Seattle?" and Claude will call `get_forecast` under the hood.

## Walkthrough

**Server side — declaring a tool** (`weather/weather.py`):
```python
mcp = FastMCP("weather")

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    ...
```
`FastMCP` turns a decorated async function into an MCP tool automatically — the function's name, type hints, and docstring become the tool's schema that the client (and the LLM) sees. `@mcp.resource(uri=...)` works the same way for read-only data, and `@mcp.prompt(...)` for reusable prompt templates.

**Client side — connecting and looping** (`mcp-client/client.py`):
```python
async def connect_to_server(self, server_script_path: str):
    params = StdioServerParameters(command=command, args=[server_script_path])
    stdio_transport = await self.exit_stack.enter_async_context(stdio_client(params))
    self.session = await self.exit_stack.enter_async_context(ClientSession(*stdio_transport))
    await self.session.initialize()
```
This spawns the server script as a child process and wraps its stdin/stdout as an MCP transport — this is the essence of the **stdio transport**: no network sockets, just a pipe to a local subprocess.

```python
async def process_query(self, query: str) -> str:
    response = self.anthropic.messages.create(..., tools=available_tools)
    # if the model responds with a tool_use block:
    result = await self.session.call_tool(tool_name, tool_args)
```
The client hands Claude the tool list on every turn; if Claude decides to call a tool, the client executes it through the MCP session and sends the result back to Claude for a final natural-language answer.

**Registering the weather server with Claude Desktop / Claude Code**

Add an entry to `claude_desktop_config.json` (macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`) or the equivalent Claude Code MCP config:
```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/knowledge/tutorials/mcp/weather", "run", "weather.py"]
    }
  }
}
```
Restart the app; the weather tools then appear alongside built-in tools in any conversation.

## Key concepts

- **MCP (Model Context Protocol)** — a standard way for an LLM application to discover and call external tools/resources/prompts, regardless of who wrote the server.
- **MCP server** — a process that exposes tools/resources/prompts; here, `weather.py`.
- **MCP client** — code that connects to a server, lists its capabilities, and lets an LLM use them; here, `client.py`.
- **Transport (stdio)** — the server and client communicate over the child process's stdin/stdout, not HTTP; simplest transport for local tools.
- **Tool** — a callable function the LLM can invoke with structured arguments (`@mcp.tool()`).
- **Resource** — read-only data the client can fetch by URI (`@mcp.resource(uri=...)`), like a GET endpoint.
- **Prompt template** — a reusable, parameterized prompt exposed by the server (`@mcp.prompt()`).
- **`ClientSession`** — the MCP SDK object representing an active client↔server connection, used to call tools and list capabilities.

## Gotchas / notes

- Both `weather/README.md` and `mcp-client/README.md` were empty before this doc — see the pointer lines added to each.
- `weather/resources.py` is a standalone example, not used by the running server — don't expect its resources to show up when you run `weather.py`.
- `weather/justfile`'s `run` recipe (`uvicorn weather:mcp --reload`) is stale and inconsistent with the actual stdio transport; use `uv run weather.py` instead.
- `content_weather`'s file resource does an unsanitized path join — fine for a local tutorial, but don't copy that pattern into anything exposed beyond localhost.
- No `ANTHROPIC_API_KEY` is committed anywhere (correctly) — you must supply your own via `.env` in `mcp-client/`.
- `get_models()` returns a hardcoded, fake model list — it's a resource demo, not real data.

## Further reading

- [Model Context Protocol docs](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Anthropic: Build an MCP server/client quickstart](https://docs.claude.com/en/docs/agents-and-tools/mcp)
- [NWS API documentation](https://www.weather.gov/documentation/services-web-api)
