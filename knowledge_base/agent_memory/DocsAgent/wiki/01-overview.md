> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** DocsAgent MCP gives any MCP-capable AI agent private, local, millisecond access to a personal Zotero library through a resident C++ BM25 search engine fronted by TypeScript and Python MCP shells.
## Key points
- DocsAgent is a spec-driven MCP (Model Context Protocol) server with Zotero as the first supported source, usable from Claude Desktop, Cursor, Cline, Qwen Code, or any MCP client (01-overview.md:10-12).
- A resident C++ engine reads `~/Zotero/zotero.sqlite` + `storage/` directly and serves BM25 full-text search with query-ranked passage retrieval over 1,000+ PDFs at ~15 ms, fully local (01-overview.md:12-14, 01-overview.md:43-45).
- The native C++ core uses an inverted-index BM25 + passage ranking with a low memory footprint of 160–227 MB for a 1,500-paper library (01-overview.md:18-19, 01-overview.md:188-189).
- The external API is 8 MCP tools — 5 read + 3 write — with JSON-schema validated arguments, token budgets, result dedup, and a three-layer write safety gate (01-overview.md:20-21, 01-overview.md:113-115).
- Two transports are supported: stdio for local MCP clients and Streamable HTTP for remote deployment with origin checks, API-key / OAuth 2.0 token introspection, per-request RBAC, and a `/health` probe (01-overview.md:22-23, 01-overview.md:34-35).
- Two shells share one core and one JSON-RPC contract: the TypeScript package `@docsagent/mcp-zotero` and a feature-equal Python wrapper in `python/` (01-overview.md:24-25, 01-overview.md:235-236).
- The MCP shell never spawns the core during tool calls and never touches Zotero files; the core runs as a background service across MCP client restarts, and the shell fails fast with startup instructions if the core is not running (01-overview.md:48-49, 01-overview.md:104-105).
---
## Architecture
MCP client connects over stdio (local) or Streamable HTTP `/mcp` (remote) to the MCP shell, which dials the resident C++ core over JSON-RPC 2.0 (01-overview.md:34-46):

```
MCP Client (Claude Desktop / Cursor / Cline / Qwen Code / any MCP host)
        │  stdio (local)   or   Streamable HTTP  /mcp  (remote)
        ▼
MCP shell  ← this package (@docsagent/mcp-zotero / docsagent-mcp-zotero)
   · tool schemas (spec-driven), argument validation, token budget, dedup
   · write orchestration via the Zotero local API, write safety gate, RBAC
   · group-library sync via the Zotero Web API
        │  JSON-RPC 2.0 over HTTP ({coreHost}:{httpPort}/rpc, cpp-httplib)
        ▼
DocsAgent Core (resident C++ engine, papersgpt-agent)
   · reads ~/Zotero/zotero.sqlite + storage/ directly on your machine
   · builds & serves the full-text index (BM25 + passage ranking)
```

Tool schemas and error codes are the single-sourced contract in `spec/` (01-overview.md:50).

## Startup and client configuration
Start the core, then point the MCP client at the shell; the shell connects to the core, loads sources, and checks index status on startup (01-overview.md:56-71, 01-overview.md:104-105).

```bash
npx @docsagent/mcp-zotero start           # spawn the bundled core for your platform
npx @docsagent/mcp-zotero status          # pid / endpoint / version
```

Python shell (same verbs, under the `core` subcommand) (01-overview.md:63-68):

```bash
pip install ./python                      # build the wheel locally (PyPI upload pending)
docsagent-mcp-zotero core start
```

`core stop` / `core restart` also available. The core reads the Zotero data directory, builds the full-text index, and serves JSON-RPC on `http://0.0.0.0:23120/rpc` (01-overview.md:70-71).

Claude Desktop / Cursor / Cline / Qwen Code (`mcpServers`) (01-overview.md:77-88):

```json
{
  "mcpServers": {
    "docsagent-zotero": {
      "command": "npx",
      "args": ["-y", "@docsagent/mcp-zotero"]
    }
  }
}
```

Python shell `mcpServers` (install the Python package first so `docsagent-mcp-zotero` is on `PATH`) (01-overview.md:90-102):

```json
{
  "mcpServers": {
    "docsagent-zotero-py": {
      "command": "docsagent-mcp-zotero"
    }
  }
}
```

## MCP tools (external API)
8 tools, 5 read + 3 write. Schemas are the single-sourced contract in `spec/tools/*.json` (mirrored into both packages); arguments are validated before handlers run and failures map to typed docsagent error codes (01-overview.md:113-115).

### `list_sources`
Every searchable source with capabilities, supported targets/includes/browse modes, filters, and document counts. **Call this first.** (01-overview.md:119-121)

### `search`
Cross-entry search over the whole library (01-overview.md:125-138):

| Parameter | Type | Notes |
|---|---|---|
| `query` | string, required | plain keywords or phrases |
| `target` | `"items" \| "annotations" \| "notes"` or array | default `items` |
| `depth` | `ids` \| `snippets` \| `full` | snippets by default (BM25-ranked passages) |
| `filters` | object | `tags`, `yearFrom`/`yearTo`, `itemType`, `authors`, `colors`, `containerId`, `titleContains` |
| `k`, `snippetsPerResult`, `max_tokens` | numbers | ranking depth and token budget |

Returns `results[]` with global ids (`zotero:KEY`), titles, relevance, snippets; multi-target searches group by target. Results are deduped (id, then normalized title + year) and packed under a token budget (01-overview.md:136-138).

### `get_content`
Read one entry. `mode=passages` (query-ranked passages, `k`) or `mode=fulltext` (offset pagination with `nextOffset`). Notes return their body with tags and metadata (01-overview.md:142-144).

### `get_metadata`
`include`: `metadata`, `abstract`, `annotations`, `notes`, `citation` (bibtex / csljson / formatted via `citationFormat`/`citationStyle`). Notes are packed under the token budget (01-overview.md:148-150).

### `list_library`
Browse modes: `collections` (drill-down via `parentId`), `items` (by `containerId`), `tags`, `saved_searches`, `standalone_notes` (01-overview.md:154-156).

### Write tools (three-layer safety gate)
| Tool | What it does | Key arguments |
|---|---|---|
| `import_item` | Import local PDFs or resolve DOI / ISBN / arXiv IDs (via the Zotero translation server); optional `autoClassify` suggests collections | `paths` \| `identifiers`, `containerId`, `autoClassify`, `confirmed` |
| `add_note` | Add a Markdown child note to an item (converted to Zotero note HTML), with orphan verification and rollback | `id`, `content`, `tags`, `confirmed` |
| `batch_modify` | Bulk `add_to_collection` / `remove_from_collection` / `add_tags` / `remove_tags` on up to 200 items in batches of 50 | `action`, `ids`, `containerId`, `tags`, `confirmed` |

Write safety gate (`spec/algorithms/write-gate.md`): **layer 1** write tools are not registered unless `enableWrites=true`; **layer 2** `confirmed=false` returns a preview and consumes no rate-limit quota; **layer 3** confirmed writes consume a per-hour rate limit (default 30/h). Anything above 20 items in `batch_modify` additionally reports `requiresConfirmation` in the preview (01-overview.md:168-172).

## Engine performance
The C++ engine powers PapersGPT — the same index and retrieval stack ships in this MCP server (01-overview.md:180-182):

| Metric | Mac (Intel i9) | Windows VM (4C8G) |
|---|---|---|
| Library size | 1,506 PDFs (4.5 GB on disk) | 500+ PDFs |
| **Index build time** | **141 s** | a few seconds |
| **Memory (agent process)** | **227 MB** | **160 MB** |
| **Average retrieval latency** | **~15 ms** | **~15 ms** |

Indexing cost scales roughly **linearly** with library size; retrieval latency stays **constant** — a 10,000-paper library (~30 GB) indexes in about 15–20 minutes, and everyday search stays at **~15 ms** (01-overview.md:191-193). For comparison: a typical web page load takes 1,000–3,000 ms; a blink of an eye is 100–150 ms (01-overview.md:194-195). Privacy: the library never leaves the machine (01-overview.md:196).

## Configuration
Config lives at `~/.docsagent/config.json` (or `$DOCSAGENT_CONFIG`) — one file shared by the JS shell, the Python wrapper, and the C++ core. Validated against `spec/config.json` (01-overview.md:202-204):

| Key | Default | Description |
|---|---|---|
| `coreHost` | `0.0.0.0` | Address the core binds and the shell dials |
| `httpPort` | `23120` | Core HTTP port (`POST /rpc`) |
| `coreBinary` | `""` | Optional explicit path to the core binary |
| `zoteroDataDir` | `~/Zotero` | Zotero data directory |
| `zoteroApiUrl` | `http://localhost:23119/api` | Zotero local API (write orchestration) |
| `zoteroGroups` | `[]` | Group libraries to sync from zotero.org |
| `enableWrites` | `false` | Register the three write tools |
| `writeRateLimitPerHour` | `30` | Confirmed-write rate limit |
| `maxTokensPerTool` | `4000` | Token budget per tool result |
| `defaultSource` | `zotero` | Source used when an id omits the prefix |
| `transport` | `stdio` | `stdio` or `streamable-http` |
| `httpListenAddr` | `0.0.0.0:8080` | Listen address for streamable-http (`/mcp`) |
| `authMode` / `authConfig` | `none` | `api-key` or `oauth2` (RFC 7662) + `allowedOrigins` |
| `rbacRoles` | `{}` | role → allowed tool names (per-request RBAC on HTTP) |
| `logLevel` | `info` | `debug` / `info` / `warn` / `error` |

## Distribution
| Channel | Package | Bundled core | Size |
|---|---|---|---|
| npm (JS/TS shell) | `@docsagent/mcp-zotero` | all platforms in `bin/` | ~70 MB tarball |
| PyPI (Python shell) | `docsagent-mcp-zotero` (`pip install ./python`) | same binaries in the wheel | ~65 MB wheel |

Both shells read the same config and talk to the same core — pick either (or both) as the MCP distribution channel. Core lifecycle (`start` / `stop` / `restart` / `status`) is available from both CLIs (01-overview.md:235-237). Contract source: `spec/` — 8 tool schemas, 23 JSON-RPC methods, error codes + suggested calls, config schema (01-overview.md:243-244). No truncated files were noted in this chunk.

**Covers:** README (purpose, transports, shells, tools, performance, config, distribution), Architecture diagram (MCP shell + resident C++ core), `spec/` contract, `python/` wrapper, `bin/` bundled core
