# Technical Analysis: docsagent/docsagent

**Repository:** https://github.com/docsagent/docsagent
**Version analyzed:** 4.0.0 (from `package-lock.json:21-30`)
**Date:** 2026-09-26
**Wiki:** [[index]]

## 1. Overview

Problem space: researchers keep large personal PDF libraries in Zotero (1,000+ papers, multiple GB) and want an AI agent to search, read, cite, and curate that library with millisecond latency and without exfiltrating private documents to a cloud service. Zotero's built-in search is not agent-addressable, and naive RAG wrappers re-parse files per query, spawn an indexer per call, or send content to hosted embeddings.

What the repo does: DocsAgent MCP splits the system into a resident native search engine plus thin MCP shells. A background C++ core (`papersgpt-agent`) reads `~/Zotero/zotero.sqlite` + `storage/` directly and serves BM25 full-text search with query-ranked passage retrieval (~15 ms, 160–227 MB for 500–1,500 PDFs) (01-overview.md:12-14, 01-overview.md:18-19, 01-overview.md:113-121). Two feature-equal shells — TypeScript package `@docsagent/mcp-zotero` and a Python wrapper in `python/` — expose 8 MCP tools (5 read + 3 write) with JSON-schema validation, token budgets, dedup, and a three-layer write safety gate, over stdio (local) or Streamable HTTP `/mcp` (remote) (01-overview.md:20-25). The primary user is an MCP-capable agent (via Claude Desktop, Cursor, Cline, Qwen Code, or any MCP host) acting on behalf of a researcher who owns a local Zotero library (01-overview.md:10-12).

## 2. High-Level Architecture

```
MCP Client (Claude Desktop / Cursor / Cline / Qwen Code / any MCP host)
        │  stdio (local) ── or ── Streamable HTTP /mcp (remote)
        ▼
MCP shell (@docsagent/mcp-zotero / docsagent-mcp-zotero in python/)
  · tool schemas, arg validation, token budget, result dedup
  · write orchestration via Zotero local API + write safety gate + RBAC
  · group-library sync via Zotero Web API
        │  JSON-RPC 2.0 over HTTP ({coreHost}:{httpPort}/rpc, cpp-httplib)
        ▼
DocsAgent Core (resident C++ engine, papersgpt-agent)
  · reads ~/Zotero/zotero.sqlite + storage/ directly
  · builds + serves full-text index (BM25 + passage ranking)
        │
        ▼
Zotero data dir (sqlite + PDFs) + ~/.docsagent/config.json (shared config)
```

Derived from the architecture diagram and transport description (01-overview.md:14-29, 01-overview.md:34-46).

Data-flow narrative (5 steps):

1. **Configure and start.** Operator starts the core (`npx @docsagent/mcp-zotero start` or `docsagent-mcp-zotero core start`), which reads the Zotero data directory, builds the full-text index, and serves JSON-RPC on `http://0.0.0.0:23120/rpc` (01-overview.md:36-39, 01-overview.md:48-49). Shared config lives at `~/.docsagent/config.json` (or `$DOCSAGENT_CONFIG`), validated against `spec/config.json` (01-overview.md:125-126).
2. **Attach the shell.** The MCP client launches the shell over stdio or Streamable HTTP `/mcp`; the shell dials the already-running core, loads sources, and checks index status on startup, failing fast with startup instructions if the core is absent (01-overview.md:33-34, 01-overview.md:48-49, 01-overview.md:104-105).
3. **Discover then search.** The agent calls `list_sources` first, then `search` (cross-entry BM25 retrieval with `target`/`depth`/`filters`/`k`/`snippetsPerResult`/`max_tokens`), and the shell packs deduped results under the token budget (01-overview.md:78-80, 01-overview.md:81-92).
4. **Read.** `get_content` (passages vs. paginated fulltext via `nextOffset`) and `get_metadata` (metadata/abstract/annotations/notes/citation in bibtex/csljson/formatted) fetch single entries; notes are packed under the token budget (01-overview.md:94-100).
5. **Write (opt-in).** `import_item` / `add_note` / `batch_modify` execute only when `enableWrites=true`, with a preview-then-confirm gate and a per-hour rate limit; writes go through the Zotero local API (with orphan verification/rollback on notes) while group content arrives via the Zotero Web API sync (01-overview.md:20-22, 01-overview.md:103-110).

Persistent state lives in three places: the Zotero data directory (`zotero.sqlite` + `storage/` PDFs, the source of truth the core indexes), the core's built index (resident process memory/rebuilt at startup; build cost scales roughly linearly with library size), and `~/.docsagent/config.json` (shell + core settings).

## 3. The Resident Index and Entry Model

The central abstraction is the **resident full-text index over Zotero entries**, fronted by a fixed 8-tool contract. The core owns retrieval (inverted-index BM25 + passage ranking); the shell owns the MCP contract (schemas single-sourced in `spec/`, argument validation before handlers run, typed error codes on failure) (01-overview.md:31-32, 01-overview.md:75-76). Entries are addressed by global ids (`zotero:KEY`, with `defaultSource: zotero` when the prefix is omitted), and the shell never spawns the core per call and never touches Zotero files itself — the core is a background service across MCP client restarts (01-overview.md:11-12, 01-overview.md:136-137).

Named kinds/types (tool-level surface; the wiki does not document core C++ classes):

- **Sources** — enumerated by `list_sources` with capabilities, supported targets/includes/browse modes, filters, and document counts; the designated first call (01-overview.md:78-80).
- **Targets** — `items` (default) vs. `annotations` vs. `notes`, singly or as an array; multi-target searches group by target (01-overview.md:85-87, 01-overview.md:92-93).
- **Depths** — `ids` vs. `snippets` (default, BM25-ranked passages) vs. `full` (01-overview.md:88-89).
- **Browse modes** (`list_library`) — `collections` (drill-down via `parentId`), `items` (by `containerId`), `tags`, `saved_searches`, `standalone_notes` (01-overview.md:100-101).
- **Content modes** (`get_content`) — `passages` (query-ranked, `k`) vs. `fulltext` (offset pagination with `nextOffset`) (01-overview.md:94-95).
- **Metadata includes** (`get_metadata`) — `metadata`, `abstract`, `annotations`, `notes`, `citation` with `citationFormat`/`citationStyle` (bibtex / csljson / formatted) (01-overview.md:98-99).

Key queries (verbatim contract excerpts from the wiki):

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

(01-overview.md:52-61; the shell's attach contract — the agent's entry query is `list_sources` first, then `search` with `query` + `target`/`depth`/`filters` per 01-overview.md:78-92.)

## 4. LLM / External Service Integration

The repository calls **no LLM or embedding API itself**. Retrieval is lexical (BM25 + passage ranking, fully local, ~15 ms), and the wiki claims zero data leakage with the library never leaving the machine (01-overview.md:12-14, 01-overview.md:122-123, 02-top-level-files.md:105). The "intelligence" is supplied by the calling MCP host (Claude Desktop, Cursor, Cline, Qwen Code); this repo is the tool server, not the model caller. There are therefore no LLM provider keys, model names, or prompt templates documented in the wiki pages analyzed.

External (non-LLM) services the shell/core touch, with required vs. optional status:

- **Resident C++ core JSON-RPC (`{coreHost}:{httpPort}/rpc`, default `http://0.0.0.0:23120/rpc`) — required.** The shell dials it on startup and per tool call; missing core = fail-fast with startup instructions (01-overview.md:24-25, 01-overview.md:48-49, 01-overview.md:104-105).
- **Zotero data dir (`~/Zotero`: `zotero.sqlite` + `storage/`) — required.** Read directly by the core (01-overview.md:26-27).
- **Zotero local API (`http://localhost:23119/api`) — required only for writes.** Write orchestration path; irrelevant when `enableWrites=false` (01-overview.md:20-22, 01-overview.md:131-132).
- **Zotero translation server — optional, write-path only.** Used by `import_item` to resolve DOI / ISBN / arXiv IDs or import local PDFs (01-overview.md:106-107).
- **Zotero Web API (zotero.org) — optional.** Group-library sync for entries in `zoteroGroups` (01-overview.md:22-23, 01-overview.md:133-134).
- **Streamable-HTTP auth infrastructure — optional, remote transport only.** `api-key` or OAuth 2.0 token introspection (RFC 7662), `allowedOrigins`, per-request RBAC, `/health` probe (01-overview.md:22-23, 01-overview.md:34-35, 01-overview.md:140-142).

Environment variables and config keys documented: `$DOCSAGENT_CONFIG` (config file override), `DOCSAGENT_ZOTERO_DATA_DIR` (Smithery-mapped `zoteroDataDir` override) (01-overview.md:125-126, 02-top-level-files.md:141-143); full key table in §8.

## 5. The Search-Read-Write Pipeline

Primary workflow: discover → ranked search → passage/fulltext read → metadata/citation → opt-in write. Each step cites the wiki location of the tool/function contract; the two analyzed wiki pages do not expose `src/*.ts` function-level line numbers, so steps are grounded at the tool-schema/spec level rather than invented line references.

1. **Start the core** — `start` (JS: `npx @docsagent/mcp-zotero start`, 01-overview.md:36-39; Python: `docsagent-mcp-zotero core start`, 01-overview.md:43-46) with `core stop` / `core restart` / `status` lifecycle verbs on both CLIs (01-overview.md:151-152). Effect: index build + JSON-RPC serve on `{coreHost}:{httpPort}/rpc` (01-overview.md:48-49).
2. **Attach and validate** — shell connects to core, loads sources, checks index status (01-overview.md:33-34); contract source is `spec/` (8 tool schemas, 23 JSON-RPC methods, error codes, config schema) (01-overview.md:151-152).
3. **Enumerate sources** — `list_sources` with no required args; returns capabilities/targets/filters/counts (01-overview.md:78-80).
4. **Ranked search** — `search` with `query` (required string), `target`, `depth`, `filters` (`tags`, `yearFrom`/`yearTo`, `itemType`, `authors`, `colors`, `containerId`, `titleContains`), `k`, `snippetsPerResult`, `max_tokens`; returns `results[]` (`zotero:KEY`, titles, relevance, snippets), deduped by id then normalized title+year, packed under token budget (01-overview.md:81-92).
5. **Read content** — `get_content` with `mode=passages` (`k`) or `mode=fulltext` (`nextOffset` pagination); notes return body + tags + metadata (01-overview.md:94-95).
6. **Read metadata/citation** — `get_metadata` with `include` set and `citationFormat`/`citationStyle` for bibtex/csljson/formatted output (01-overview.md:98-99).
7. **Browse** — `list_library` with `collections`/`items`/`tags`/`saved_searches`/`standalone_notes` modes, `parentId`/`containerId` drill-down (01-overview.md:100-101).
8. **Write with safety gate** — `import_item` (`paths` | `identifiers`, `containerId`, `autoClassify`, `confirmed`), `add_note` (`id`, `content`, `tags`, `confirmed`, Markdown→Zotero-HTML, orphan verification + rollback), `batch_modify` (`action`, `ids`, `containerId`, `tags`, `confirmed`, ≤200 items in batches of 50) (01-overview.md:103-108); gate per `spec/algorithms/write-gate.md`: layer 1 (registration requires `enableWrites=true`), layer 2 (`confirmed=false` preview, no quota), layer 3 (confirmed writes consume 30/h quota; >20-item `batch_modify` previews report `requiresConfirmation`) (01-overview.md:110-111).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `spec/` (dir: `tools/*.json`, config schema, error codes) | contract source; 8 tool schemas + 23 JSON-RPC methods | Single-sourced MCP/JSON-RPC contract both shells validate against (01-overview.md:31-32, 01-overview.md:75-76, 01-overview.md:151-152) |
| `spec/algorithms/write-gate.md` | 3-layer gate spec | Defines write registration / preview / rate-limit semantics (01-overview.md:110-111) |
| `spec/config.json` | config schema | Validates `~/.docsagent/config.json` (01-overview.md:125-126) |
| `src/**` → `dist/` (`dist/cli.js`) | TS sources compile to `dist/`; bin entry `dist/cli.js` | Runtime MCP shell; `strict:true`, ESNext/NodeNext per `tsconfig.json:1-17` (02-top-level-files.md:4-8, 02-top-level-files.md:58-77) |
| `package-lock.json` | identity block at `package-lock.json:21-45` (+ esbuild pins to :440) | Package identity (`@docsagent/mcp-zotero@4.0.0`, Apache-2.0, Node ≥18) and dependency pins (02-top-level-files.md:5-7, 02-top-level-files.md:26-56) |
| `python/` (wheel `docsagent_mcp_zotero-4.0.0`) | wrapper, same verbs under `core` subcommand | Feature-equal Python shell sharing config + JSON-RPC contract (01-overview.md:24-25, 01-overview.md:41-46, 01-overview.md:235-237) |
| `bin/` (bundled core binaries) | per-platform natives, ~70 MB tarball / ~65 MB wheel | Ships the resident C++ engine with both distributions (01-overview.md:146-150) |
| `~/.docsagent/config.json` (`$DOCSAGENT_CONFIG`) | 16 documented keys | One file shared by JS shell, Python wrapper, C++ core (01-overview.md:125-144) |
| `SKILL.md` | `SKILL.md:1-91` | Agent-facing skill contract (`add`/`search`/`list`/`status`/`stop` over PDF/PPTX/DOCX) (02-top-level-files.md:11-13, 02-top-level-files.md:99-113) |
| `smithery.yaml` | `smithery.yaml:1-23` | Smithery stdio launch config (`zoteroDataDir`, `enableWrites`) (02-top-level-files.md:12-13, 02-top-level-files.md:114-144) |
| `mcp-registry/server.json` | registry payload | Official MCP Registry submission (`io.github.docsagent/zotero`) (02-top-level-files.md:85-98) |
| `PUBLISH.md` | `PUBLISH.md:1-56` | 4-channel release runbook (npm, PyPI, MCP Registry, Smithery + directory forms) (02-top-level-files.md:10-12, 02-top-level-files.md:85-98) |
| `tsconfig.json` | `tsconfig.json:1-17` | Compiler contract (ESNext/NodeNext, `strict`, `src/**/*`→`dist/`) (02-top-level-files.md:8-9, 02-top-level-files.md:58-84) |
| `.gitignore` | `.gitignore:1-6` | Excludes `dist/`, `node_modules/`, `tmp/`, `.qwen/`, `*.tgz`, `.DS_Store` (02-top-level-files.md:9-10, 02-top-level-files.md:14-24) |

14 files/dirs; line ranges beyond those quoted are not exposed by the two analyzed wiki pages.

## 7. Dependencies

| Package | Version constraint | Purpose |
|---|---|---|
| `@modelcontextprotocol/sdk` | `^1.29.0` | MCP transport + tool protocol (required runtime) |
| `ajv` | `^8.17.0` | JSON-schema validation of tool args / config (required runtime) |
| `node` (engine) | `>=18` | Minimum runtime for the TS shell / CLI |
| `tsup` | `^8.0.0` | Build bundler (dev) |
| `typescript` | `^5.0.0` | Type-check + compile `src/**/*`→`dist/` (dev) |

All constraint strings verbatim from `package-lock.json:31-44` via (02-top-level-files.md:6-8, 02-top-level-files.md:26-56). Platform-scoped optional `@esbuild/*` pins (e.g. `:0.27.7` entries at `package-lock.json:46-440`) exist but were truncated in the wiki chunk and are not enumerated here (02-top-level-files.md:57). Python wheel dependencies are not itemized in the analyzed pages.

## 8. CLI / Usage Surface

Entry points: `docsagent` bin → `dist/cli.js` (JS) and `docsagent-mcp-zotero` (Python, requires installing `./python` first so it is on `PATH`) (02-top-level-files.md:5-7, 01-overview.md:63-72).

| Command | Purpose |
|---|---|
| `npx @docsagent/mcp-zotero start` | Spawn the bundled core for the platform |
| `npx @docsagent/mcp-zotero status` | Show pid / endpoint / version |
| `core stop` / `core restart` | Stop / restart the core (both CLIs; Python verbs nested under `core`) |
| `docsagent-mcp-zotero core start` | Python-shell equivalent of `start` (after `pip install ./python`) |
| `docsagent add <paths…>` | Index folders/files (skill contract; multi-path allowed) |
| `docsagent search "<query>"` | Hybrid/local search returning snippets with paths + scores |
| `docsagent list` | List indexed/monitored files |
| `docsagent status` | Indexing progress + service health |
| `docsagent stop` | Stop the indexing service |

First four rows from (01-overview.md:36-49, 01-overview.md:151-152); last five from the skill contract (02-top-level-files.md:106-113).

Env vars:

| Variable | Effect |
|---|---|
| `DOCSAGENT_CONFIG` | Override config file path (default `~/.docsagent/config.json`) |
| `DOCSAGENT_ZOTERO_DATA_DIR` | Override `zoteroDataDir` (set by Smithery when configured) |

Config (`~/.docsagent/config.json`, validated against `spec/config.json`):

| Key | Default | Description |
|---|---|---|
| `coreHost` | `0.0.0.0` | Address the core binds / shell dials |
| `httpPort` | `23120` | Core HTTP port (`POST /rpc`) |
| `coreBinary` | `""` | Explicit core binary path |
| `zoteroDataDir` | `~/Zotero` | Zotero data directory |
| `zoteroApiUrl` | `http://localhost:23119/api` | Zotero local API (writes) |
| `zoteroGroups` | `[]` | Group libraries to sync from zotero.org |
| `enableWrites` | `false` | Register `import_item`, `add_note`, `batch_modify` |
| `writeRateLimitPerHour` | `30` | Confirmed-write quota |
| `maxTokensPerTool` | `4000` | Token budget per tool result |
| `defaultSource` | `zotero` | Source when an id omits the prefix |
| `transport` | `stdio` | `stdio` or `streamable-http` |
| `httpListenAddr` | `0.0.0.0:8080` | Listen address for `/mcp` |
| `authMode` / `authConfig` | `none` | `api-key` or `oauth2` (RFC 7662) + `allowedOrigins` |
| `rbacRoles` | `{}` | Role → allowed tool names (HTTP per-request RBAC) |
| `logLevel` | `info` | `debug` / `info` / `warn` / `error` |

Config table from (01-overview.md:125-144).

## 9. Extensibility Points

- **New read tool / argument** — add its JSON schema under `spec/tools/*.json` (the single-sourced contract mirrored into both packages), then implement the handler in the TS shell (`src/`) and mirror it in `python/`; arguments validate before handlers run and failures map to typed error codes (01-overview.md:31-32, 01-overview.md:75-76).
- **New write operation** — same as above plus the safety gate: gate the registration on `enableWrites`, implement `confirmed=false` preview, and consume `writeRateLimitPerHour` quota on confirmed writes per `spec/algorithms/write-gate.md` (01-overview.md:103-111).
- **New document source (beyond Zotero)** — extend `list_sources` capabilities/targets/includes/browse modes and add a core reader + shell sync path analogous to the Zotero sqlite/`storage/` reader and `zoteroGroups` Web API sync (01-overview.md:20-27, 01-overview.md:78-80).
- **New transport / auth scheme** — extend the shell's transport layer (`stdio` vs. `streamable-http` + `authMode`/`authConfig`/`allowedOrigins`/`rbacRoles`/`httpListenAddr`); remote deployments add origin checks, token introspection, per-request RBAC, and `/health` (01-overview.md:22-23, 01-overview.md:34-35, 01-overview.md:138-142).
- **New distribution channel** — replicate the `PUBLISH.md` / registry pattern: npm tarball with `bin/` natives, PyPI wheel, `mcp-registry/server.json` payload, `smithery.yaml` launch config (02-top-level-files.md:10-12, 02-top-level-files.md:85-98, 02-top-level-files.md:114-144).
- **New agent workflow** — extend `SKILL.md` command/verb table (`add`/`search`/`list`/`status`/`stop`) and its check-index → search → synthesize → cite-path-and-page workflow (02-top-level-files.md:99-113).

## 10. Limitations and Gotchas

- **Core must be running or nothing works.** The shell never spawns the core per call; if the background service is down the shell fails fast and the agent must run `start` first — a two-process deployment the caller has to manage across MCP client restarts (01-overview.md:11-12, 01-overview.md:48-49, 01-overview.md:104-105).
- **Writes are off by default and throttled.** `enableWrites=false` unregisters all three write tools, previews consume no quota but confirmed writes are capped at 30/h, and `batch_modify` over 20 items forces an extra confirmation round-trip (01-overview.md:103-111).
- **Lexical retrieval only in the documented path.** The analyzed pages describe BM25 + passage ranking with filters (`tags`, years, `itemType`, `authors`, `colors`, `containerId`, `titleContains`); there is no documented semantic/vector or cross-library-join behavior in the tool contract, so synonym-heavy or cross-source questions depend on keyword overlap (01-overview.md:81-92). (The skill page mentions "hybrid (text + semantic)" claims at `SKILL.md:7-24` without a corresponding engine spec in the analyzed pages — treat as unverified from these sources.)
- **Heavyweight distribution.** The npm tarball (~70 MB) and wheel (~65 MB) bundle all-platform core binaries in `bin/`; install size and the `pip install ./python` local-build step (PyPI upload pending) are costs of the native-core design (01-overview.md:41-46, 01-overview.md:146-150).
- **Thin wiki coverage bounds this analysis.** Only two component pages were in scope; `src/` handler internals, core C++ files, the 23 JSON-RPC methods, and error-code taxonomy are referenced but not line-documented here, so §5–§6 cite tool/spec level rather than per-function lines (01-overview.md:151-153, 02-top-level-files.md:57).

## 11. How It Compares to Alternatives

- **PapersGPT (same team/stack)** — the wiki states the C++ engine powers PapersGPT and the same index/retrieval stack ships in this MCP server; PapersGPT is the standalone product, DocsAgent MCP is its agent-addressable (MCP tool) packaging (01-overview.md:113-114).
- **Zotero's built-in desktop search** — human-facing, single-app full-text search over the same `zotero.sqlite` + `storage/`; DocsAgent adds a resident agent protocol (8 tools, token-budgeted passages, citations, browse modes) that Zotero itself does not expose to MCP hosts.
- **Generic hosted-MCP / directory servers (e.g. entries discoverable via the MCP Registry, PulseMCP, Glama, mcp.so submissions in `PUBLISH.md`)** — typically remote or per-call spawned; DocsAgent's differentiator is the local resident core (~15 ms retrieval, 160–227 MB, no document exfiltration) at the cost of a ~65–70 MB native bundle and a separately managed background process (01-overview.md:113-123, 02-top-level-files.md:85-98).
- **Agent skill / CLI indexers over loose files (the `SKILL.md` `add`/`search`/`list`/`status` pattern over PDF/PPTX/DOCX)** — lighter for ad-hoc folders without Zotero metadata (collections, tags, saved searches, annotations, citations); weaker where Zotero structure (global ids, browse modes, citation formats, group sync, write gate) matters (01-overview.md:94-101, 02-top-level-files.md:99-113).

Positioning: DocsAgent is the local-first, Zotero-native MCP server choice — pick it when a private Zotero library must be agent-searchable offline with ranked passages and governed writes; pick a generic file indexer or hosted MCP server when there is no Zotero library or no tolerance for a resident native binary.

## Appendix: Selected Code Snippets

1. Root package identity and dependency pin (`package-lock.json:21-45`):

```json
{
  "name": "@docsagent/mcp-zotero",
  "version": "4.0.0",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "": {
      "name": "@docsagent/mcp-zotero",
      "version": "4.0.0",
      "hasInstallScript": true,
      "license": "Apache-2.0",
      "dependencies": {
        "@modelcontextprotocol/sdk": "^1.29.0",
        "ajv": "^8.17.0"
      },
      "bin": {
        "docsagent": "dist/cli.js"
      },
      "devDependencies": {
        "tsup": "^8.0.0",
        "typescript": "^5.0.0"
      },
      "engines": {
        "node": ">=18"
      }
    }
  }
}
```

2. Compiler contract (`tsconfig.json:1-17`):

```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "lib": ["ESNext"],
    "outDir": "dist",
    "strict": true,
    "declaration": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"]
}
```

3. MCP client attach config (`mcpServers`, cf. 01-overview.md:52-61):

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

4. Smithery launch config core (`smithery.yaml:1-23`):

```yaml
startCommand:
  type: stdio
  configSchema:
    type: object
    title: DocsAgent Zotero MCP Server
    description: Search, read, and write a local Zotero library through a resident C++ search engine. The core must be running (docsagent-mcp-zotero core start or the JS CLI equivalent).
    properties:
      zoteroDataDir:
        type: string
        title: Zotero data directory
        description: Path to the Zotero data directory the engine indexes.
        default: ~/Zotero
      enableWrites:
        type: boolean
        title: Enable write tools
        description: Register the write tools (import_item, add_note, batch_modify).
        default: false
  commandFunction: |-
    (config) => ({
      "command": "npx",
      "args": ["-y", "@docsagent/mcp-zotero"],
      "env": config.zoteroDataDir ? { "DOCSAGENT_ZOTERO_DATA_DIR": config.zoteroDataDir } : {}
    })
```
