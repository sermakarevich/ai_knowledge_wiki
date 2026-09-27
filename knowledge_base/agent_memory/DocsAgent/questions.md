---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: docsagent/docsagent
### Q1. How does a query flow from an MCP client to the search index in DocsAgent?
> [!tip]- Answer
> The MCP client connects over stdio locally or Streamable HTTP remotely to the MCP shell, which validates arguments and dials the resident C++ core over JSON-RPC 2.0. The core reads `~/Zotero/zotero.sqlite` plus `storage/` directly and serves BM25 full-text search with passage ranking. See [[wiki/01-overview|Overview]].
### Q2. What are the 8 MCP tools and how do the read tools differ?
> [!tip]- Answer
> Five tools read: `list_sources` enumerates searchable sources and must be called first, `search` runs cross-entry queries with depth and token budgets, `get_content` reads one entry as passages or paginated fulltext, `get_metadata` returns metadata plus abstracts and citations, and `list_library` browses collections, items, tags, and saved searches. Three tools write: `import_item`, `add_note`, and `batch_modify`. See [[wiki/01-overview|Overview]].
### Q3. How does the three-layer write safety gate work?
> [!tip]- Answer
> Layer one gates registration: write tools are not registered unless `enableWrites=true`. Layer two makes unconfirmed calls return only a preview without consuming rate-limit quota. Layer three charges confirmed writes against a per-hour limit of 30, with `batch_modify` over 20 items additionally flagging `requiresConfirmation`. See [[wiki/01-overview|Overview]].
### Q4. What performance and privacy guarantees does the C++ engine offer?
> [!tip]- Answer
> The inverted-index BM25 engine holds a 1,500-paper library in roughly 160–227 MB and answers everyday searches in about 15 ms, with indexing cost scaling linearly while retrieval latency stays constant. Everything runs fully locally, so the library never leaves the machine. See [[wiki/01-overview|Overview]].
### Q5. Which configuration keys control transports, auth, and write limits?
> [!tip]- Answer
> The shared config at `~/.docsagent/config.json` defaults to stdio transport, core port 23120, and writes disabled, with HTTP mode listening on `0.0.0.0:8080` under `/mcp`. Remote deployments add origin checks, API-key or OAuth 2.0 token introspection, and per-request RBAC role-to-tool mappings. Token budgets default to 4000 per tool and confirmed writes to 30 per hour. See [[wiki/01-overview|Overview]].
### Q6. What does the repository root define, and what are the package identity and build rules?
> [!tip]- Answer
> The root defines packaging and distribution for `@docsagent/mcp-zotero` 4.0.0 under Apache-2.0 with Node `>=18`, not runtime logic. Runtime dependencies are only the MCP SDK and Ajv, while TypeScript compiles `src/**/*` to `dist/` in strict ESNext/NodeNext mode. Build output, `node_modules/`, temp files, and tarballs are git-ignored. See [[wiki/02-top-level-files|Top-level-files]].
### Q7. Would you recommend DocsAgent to a researcher with a large private PDF library who needs agent access without cloud uploads?
> [!tip]- Answer
> Yes, provided the researcher runs Zotero locally and accepts a resident background core plus local-first setup. The private millisecond BM25 search, spec-driven MCP tools with gated writes, and multi-channel distribution fit offline agent workflows well. The main trade-off is operational overhead versus a hosted search service. See [[wiki/01-overview|Overview]].
