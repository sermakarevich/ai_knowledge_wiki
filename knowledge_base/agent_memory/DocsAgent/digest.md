> [[index|Wiki]] | [[summary|Summary]]
# docsagent/docsagent — Digest
## 1. [[wiki/01-overview|Overview]]
**In one sentence:** DocsAgent MCP gives any MCP-capable AI agent private, local, millisecond access to a personal Zotero library through a resident C++ BM25 search engine fronted by TypeScript and Python MCP shells.
## Key points
- DocsAgent is a spec-driven MCP (Model Context Protocol) server with Zotero as the first supported source, usable from Claude Desktop, Cursor, Cline, Qwen Code, or any MCP client (01-overview.md:10-12).
- A resident C++ engine reads `~/Zotero/zotero.sqlite` + `storage/` directly and serves BM25 full-text search with query-ranked passage retrieval over 1,000+ PDFs at ~15 ms, fully local (01-overview.md:12-14, 01-overview.md:43-45).
- The native C++ core uses an inverted-index BM25 + passage ranking with a low memory footprint of 160–227 MB for a 1,500-paper library (01-overview.md:18-19, 01-overview.md:188-189).
- The external API is 8 MCP tools — 5 read + 3 write — with JSON-schema validated arguments, token budgets, result dedup, and a three-layer write safety gate (01-overview.md:20-21, 01-overview.md:113-115).
- Two transports are supported: stdio for local MCP clients and Streamable HTTP for remote deployment with origin checks, API-key / OAuth 2.0 token introspection, per-request RBAC, and a `/health` probe (01-overview.md:22-23, 01-overview.md:34-35).
- Two shells share one core and one JSON-RPC contract: the TypeScript package `@docsagent/mcp-zotero` and a feature-equal Python wrapper in `python/` (01-overview.md:24-25, 01-overview.md:235-236).
- The MCP shell never spawns the core during tool calls and never touches Zotero files; the core runs as a background service across MCP client restarts, and the shell fails fast with startup instructions if the core is not running (01-overview.md:48-49, 01-overview.md:104-105).
## 2. [[wiki/02-top-level-files|Top-level-files]]
**In one sentence:** The repository root defines packaging, build, distribution, and agent-integration metadata for the `@docsagent/mcp-zotero` 4.0.0 package rather than runtime logic.
## Key points
- The root package is named `@docsagent/mcp-zotero` at version `4.0.0` with license `Apache-2.0` and `lockfileVersion: 3` (`package-lock.json:21-30`).
- The published CLI entry is the `docsagent` bin mapped to `dist/cli.js`, requiring Node `>=18` (`package-lock.json:35-44`).
- Runtime dependencies are only `@modelcontextprotocol/sdk@^1.29.0` and `ajv@^8.17.0`, with `tsup@^8.0.0` and `typescript@^5.0.0` as devDependencies (`package-lock.json:31-41`).
- TypeScript compiles `src/**/*` to `dist/` with `strict: true`, `target/module/lib` set to `ESNext`/`NodeNext`, and `skipLibCheck: true` (`tsconfig.json:1-17`).
- Build output, dependencies, temp files, and tarballs are excluded from version control via `dist/`, `node_modules/`, `tmp/`, `.qwen/`, `*.tgz`, `.DS_Store` (`.gitignore:1-6`).
- Distribution spans four channels — npm tarball, PyPI wheel/sdist, MCP Registry payload `mcp-registry/server.json`, and Smithery via `smithery.yaml` — plus web-form directory submissions (`PUBLISH.md:1-56`).
- The agent skill contract (`SKILL.md:1-87`) exposes local-first `add` / `search` / `list` / `status` / `stop` CLI workflows over private PDF, PPTX, and DOCX files with no web dependency.
- Smithery launches the server over stdio with `npx -y @docsagent/mcp-zotero` and optional `zoteroDataDir` / `enableWrites` config (`smithery.yaml:1-23`).
## The system in five moves
1. The root packages the system as `@docsagent/mcp-zotero` 4.0.0 (Node >=18, minimal runtime deps, strict TS build to `dist/`) rather than implementing runtime logic there.
2. A resident C++ core reads the local Zotero library directly and serves BM25 full-text search with passage ranking at ~15 ms, fully local and private.
3. TypeScript and Python MCP shells front that one core over a single JSON-RPC contract, never touching Zotero files or spawning the core during tool calls.
4. Agents reach the library through 8 spec-driven MCP tools (5 read + 3 gated writes) with validation, token budgets, dedup, and a three-layer write safety gate, over stdio locally or Streamable HTTP remotely.
5. The same binaries and contract ship everywhere — npm tarball, PyPI wheel, MCP Registry, and Smithery — with the `SKILL.md` add/search/list/status/stop workflow as the agent-facing entry point.
