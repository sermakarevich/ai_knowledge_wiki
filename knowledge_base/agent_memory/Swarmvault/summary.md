# Technical Analysis: swarmclawai/swarmvault

**Repository:** https://github.com/swarmclawai/swarmvault
**Version analyzed:** 3.21.0
**Date:** 2026-09-26
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

The problem space is durable, queryable personal and team knowledge built from heterogeneous sources (docs, code, transcripts, notes, URLs, mail, calendars, datasets, slide decks, screenshots) without losing provenance or accumulating hallucinated links. Ad-hoc LLM summarization produces flat markdown that does not scale past ~100 pages, drifts from sources, and cannot answer graph questions (callers, paths, contradictions).

SwarmVault addresses this as a local-first LLM Wiki, knowledge graph builder, and RAG knowledge base (README.md:19). It ingests sources into immutable `raw/`, compiles a markdown `wiki/` plus a machine-readable typed graph in `state/graph.json` with retrieval index in `state/retrieval/`, and co-evolves conventions in `swarmvault.schema.md` (README.md:71-73). Quality controls tag edges `extracted`/`inferred`/`ambiguous`, detect contradictions, stage changes via `compile --approve` and `wiki/candidates/`, and audit via `lint --conflicts` (README.md:88). Scale uses hybrid SQLite FTS plus semantic embeddings, bounded `compile --max-tokens`, and `graph query` / `graph path` / `graph explain` / `graph callers` traversal (README.md:90). Team use is git-backed `--commit` workflows, watch mode with git hooks, scheduled automation, an MCP server, and direct-rule plus skill-bundle agent integrations (README.md:92). The primary user is a developer or researcher operating an AI-agent-assisted codebase or research vault locally, with teams as secondary via git and MCP.

## 2. High-Level Architecture

```text
Sources (files, dirs, URLs, GitHub repos, transcripts)
  │
  ▼
Ingest ─► raw/ (immutable) ─► Compile (heuristic/Ollama/cloud extraction)
  │                                    │
  │                                    ▼
  │              wiki/ (pages, candidates/, graph reports, context packs) ◄─► swarmvault.schema.md (conventions)
  │                                    │
  │                                    ▼
  │              state/graph.json + state/retrieval/ (SQLite FTS + embeddings)
  │                                    │
  ▼                                    ▼
agent/ (helpers, rules, skills)    Query surface (CLI query/graph/context/task/chat, MCP server, viewer, Neo4j/Obsidian export)
```

Data-flow narrative:

1. **Ingest:** `ingest`, `add`, `source add`, `clone`, or `quickstart`/`scan` copy or localize sources into `raw/` without modification (README.md:71-73, README.md:170). `SWARMVAULT_OUT=.swarmvault-out` redirects `raw/`, `wiki/`, `state/`, `agent/`, `inbox/` under one output dir while config and schema stay at root (README.md:182).
2. **Compile:** `compile` extracts entities, concepts, edges (tagged `extracted`/`inferred`/`ambiguous`), detects contradictions, stages uncertain concepts in `wiki/candidates/`, and writes `wiki/` pages plus `state/graph.json` and `state/retrieval/` (README.md:88, README.md:57-63).
3. **Review:** `compile --approve` approval bundles, `candidate list`, and `lint --conflicts` gate what lands in the wiki (README.md:88).
4. **Retrieve and traverse:** hybrid SQLite FTS plus embeddings with `query`, `graph query`/`path`/`explain`/`callers`, `graph cluster`, `context build --budget`, bounded by `compile --max-tokens` (README.md:90).
5. **Share and act:** `graph serve` viewer, `graph share`/`graph export` (HTML, Obsidian, Neo4j Cypher), `export ai`, `task start`, `chat`, MCP server, `--commit` git workflow, watch mode with hooks, scheduled automation (README.md:92, README.md:207-224).
6. **Govern:** `doctor --repair`, `graph stats`/`graph validate --strict`, `graph status`/`check-update`/`update`, SCALE.md budgets and STABILITY.md semver contract bound evolution (README.md:207-224, SCALE.md:1-62, STABILITY.md:1-177).

Persistent state lives in the vault working directory: `raw/` (immutable sources), `wiki/` (compounding artifact including `candidates/`, `graph/`, outputs, context packs, task notes), `state/` (`graph.json`, `retrieval/`, embeddings, sessions, approvals, `benchmark.json`, `vault-version.json`), plus `swarmvault.schema.md` and `swarmvault.config.json` at root (README.md:57-63, README.md:172-180, STABILITY.md:1369-1382). Generated `raw/`/`wiki/`/`state/`/`agent/`/`inbox/` are excluded from version control and containers (`.gitignore:1-20`, `.dockerignore:1-20).

## 3. The Vault Graph and Wiki Pages

Representation is dual: human-readable markdown pages in `wiki/` (sources, concepts, entities, code, outputs, graph reports, context packs, task notes) and a machine-readable typed graph in `state/graph.json` with a local retrieval index in `state/retrieval/` (README.md:57-63). The third layer, `swarmvault.schema.md`, defines wiki structure, conventions, and domain priorities and is co-evolved by user and LLM (README.md:71-73). A zero-install standalone template at `templates/llm-wiki-schema.md` precedes CLI adoption (README.md:79).

Named kinds/types grounded in the component pages:

- Edge provenance tags `extracted` / `inferred` / `ambiguous` (README.md:88).
- Staging kind `wiki/candidates/` for new concepts before promotion (README.md:88).
- Graph artifact fields `generatedBy`, `nodes[]`, `edges[]`, `hyperedges[]`, `communities[]`, `pages[]`, `sources[]`, `benchmark?` (STABILITY.md:1352-1367).
- Page frontmatter keys `page_id`, `kind`, `tags`, `source_ids`, `freshness`, `decay_score`, `tier`, `task_id` (STABILITY.md:1324-1350).
- State file kinds `graph.json`, `retrieval/`, `context-packs/`, `memory/tasks/`, `approvals/`, `candidates/`, `ingest-runs/`, `benchmark.json`, `embeddings.json`, `vault-version.json` (STABILITY.md:1369-1382).
- Scale tiers Small / Medium / Large with node/edge/page/source bounds (SCALE.md:1160-1172).

Key queries (all CLI-traversal, README.md:90, README.md:207-224):

```bash
swarmvault query "What is the auth flow?"
swarmvault graph query <pattern>
swarmvault graph path <a> <b>
swarmvault graph explain <edge>
swarmvault graph callers <node>
```

## 4. LLM / External Service Integration

No API keys are required for the first run: the built-in `heuristic` provider runs locally and offline (README.md:55, README.md:94). Sharper extraction uses a free local LLM through Ollama; cloud providers are optional (README.md:94). The localized README heads cite Ollama `gemma4` and `nomic-embed-text` and cloud `openai` / `gpt-4o` examples (README.zh-CN.md:852-890, README.ja.md:566-604).

Required vs optional: `heuristic` is the default required-nothing path; Ollama embedding/audio providers with local caching are recommended for Medium tier and above (SCALE.md:1160-1172); cloud LLM providers are optional upgrades. Neo4j is an optional sink (`graph push neo4j`, `graph export --neo4j`), useful at Large tier (SCALE.md:1160-1172, README.md:207-224). No other external API is required by the documented fast path (`quickstart`, `demo`, `next`, `query`, `graph serve`, `doctor`).

Environment variables and secrets handling: `SWARMVAULT_OUT=.swarmvault-out` relocates generated dirs (README.md:182). `.env` and `.env.*` are git-excluded for secrets (`.gitignore:8-14`); provider credentials therefore live outside version control, consistent with `.gitignore:1-20`. The wiki chunk set analyzed here does not enumerate per-provider variable names (e.g. `OPENAI_API_KEY`); those live in engine/provider code not covered by the two available component pages. Experimental surfaces include custom provider/search modules, orchestration executors, the `local-whisper` provider, and `provider setup` (STABILITY.md:1384-1393).

## 5. The Quickstart-to-Compile Pipeline

Primary workflow is `quickstart` (beginner alias of `scan`): initialize, ingest, compile, share, serve (README.md:33, README.md:170). Each step cites the CLI surface documented in the wiki pages:

1. **Install and enter vault dir** (`README.md:136-154`, `README.md:161-168`): `npm install -g @swarmvaultai/cli`; run from an empty/scratch folder. Requires Node `>=24` (README.md:136-154).
2. **Quickstart/scan** (`README.md:170`): `swarmvault quickstart ../your-repo` (or `swarmvault scan ./path --no-viz`); ingests local file/directory or public GitHub repo, compiles wiki and graph, writes share artifacts (`wiki/graph/share-card.md`, `share-card.svg`, `share-kit/`), opens graph viewer unless `--no-serve`/`--no-viz`. Interactive runs emit bounded ingest progress on stderr (README.md:170). Fallback without a repo: `swarmvault demo` (README.md:37-39).
3. **Incremental build** (`README.md:190-199`, `README.md:201`): `swarmvault init --obsidian --profile personal-research`; `swarmvault ingest ./src --repo-root .`; `swarmvault ingest ./meeting.srt --guide`; `swarmvault add https://arxiv.org/abs/2401.12345`; `swarmvault compile`; registered sources via `source add` / `source list` / `source reload --all` / `source session`; public repos via `clone ... --no-viz` and `source add https://github.com/owner/repo --branch main`.
4. **Orient** (`README.md:51`, `README.md:207-224`): `swarmvault next` (read-only; reports initialize/ingest/compile/query/review/refresh); `graph status` / `check-update`; `update ./src` refreshes code-derived artifacts; `graph cluster` / `cluster-only` recomputes communities.
5. **Query and build context** (`README.md:43-49`, `README.md:207-224`): `query`, `graph serve`, `context build "..." --target ./src --budget 8000`, `export ai --out ./exports/ai`, `chat`, `task start "..." --target ./src --agent codex`.
6. **Review, validate, share** (`README.md:88`, `README.md:207-224`): `candidate list`, `compile --approve`, `lint --conflicts`, `doctor --repair`, `graph stats` + `graph validate --strict`, `graph share --post` / `--svg` / `--bundle`, `graph export --report` / `--callflow` / `--obsidian` / `--neo4j`, `graph push neo4j --dry-run`, `merge-graphs`, `tree --output`.

Note: the available wiki chunks truncate mid-sentence at `swarmvault init --lite` details (01-overview.md:136), so lite-mode behavior is not characterized here. Internal function-level call chains (engine `packages/`) were not in the analyzed chunk set; steps above are grounded at CLI-command granularity with `README.md:line` citations.

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `README.md` | Try It, architecture, install, fast path, main loop, command table | Canonical product contract: quickstart/scan, three-layer model, quality/scale/team rationale |
| `manifest.json` | 1-11 | Obsidian desktop-only plugin identity `swarmvault` 3.21.0, app `>=1.5.0`, palette commands + freshness status bar |
| `pnpm-workspace.yaml` | 1-3 | Monorepo glob `packages/*`, single workspace root |
| `.npmrc` | 1-2 | Forces workspace-local resolution (`link-workspace-packages`, `prefer-workspace-packages`) |
| `pnpm-lock.yaml` | 1-50 visible head; bulk index truncated | Lockfile v9; importer pins for root, cli, engine, obsidian-plugin, viewer |
| `biome.json` | 1-55, 64-116 | Biome 2.4.10 lint/format policy: line width 140, double quotes, TS/JS/JSON scope, generated-dir exclusions |
| `lefthook.yml` | 1-7 | Pre-commit `biome check` on staged TS/JS/JSON with `stage_fixed` |
| `tsconfig.base.json` | 1-16 | Shared TS baseline: ES2022/ESNext, Bundler resolution, strict, node types |
| `SCALE.md` | 1-62, 1160-1220 | Small/Medium/Large tiers, compile budgets, degradation notes, `swarmvault.config.json` knobs, perf budgets |
| `STABILITY.md` | 1-177, 1226-1393 | Semver 2.0.0 contract: Stable/Experimental/Internal tiers, deprecation window, Stable CLI/config/MCP/frontmatter/graph/state tables |
| `swarmvault.schema.md` | schema layer (README.md:71-73) | User-editable vault instructions co-evolved with the LLM |
| `swarmvault.config.json` | knobs (SCALE.md:1182-1193) | Tuning: `graph.*`, `repoAnalysis.*`, `benchmark`, `consolidation`, `freshness`, `retrieval`/`search` alias |
| `templates/llm-wiki-schema.md` | template (README.md:79) | Zero-install schema for any LLM agent before CLI adoption |
| `.gitignore` | 1-20 | Excludes generated vault state, secrets, agent/output dirs, viewer dist |
| `.dockerignore` | 1-20 | Keeps build context free of `node_modules`, `dist`, vault outputs, logs, coverage |
| `README.ja.md` | head ~566-604, truncated | Japanese localization; `README.md` authoritative on divergence |
| `README.zh-CN.md` | head ~852-890, truncated | Simplified Chinese localization; `README.md` authoritative on divergence |
| `glama.json` | 1-5 | Glama MCP registry stub, maintainer `swarmclawai` |

## 7. Dependencies

Required toolchain first, then workspace runtime pins. All constraint strings are verbatim from the analyzed pages; the lockfile package index body was truncated in the chunk set, so transitive hashes are not listed.

| Package | Version constraint | Purpose |
|---|---|---|
| node | `>=24` | CLI runtime requirement (README.md:136-154) |
| pnpm | workspace (`pnpm-workspace.yaml:1-2`, `pnpm-lock.yaml:1-9` `lockfileVersion: '9.0'`) | Monorepo install/link manager |
| typescript | `^5.9.3` | Shared compile baseline (root importer, `tsconfig.base.json:1-16`) |
| `@biomejs/biome` | `^2.4.10` | Lint + format enforcement |
| `@evilmartians/lefthook` | `^2.1.5` | Pre-commit hook runner |
| `@swarmvaultai/engine` | `3.21.0` via `link:../engine` | CLI-to-engine workspace link (`packages/cli` importer) |
| commander | `^14.0.1` | CLI argument parsing (`packages/cli` importer) |
| `@modelcontextprotocol/sdk` | pinned in lockfile (engine importer) | MCP server implementation |
| graphology | pinned in lockfile (engine importer) | In-memory graph algorithms (cluster/community/traversal) |
| neo4j-driver | pinned in lockfile (engine importer) | Optional Neo4j sink (`graph push neo4j`) |
| zod | pinned in lockfile (engine importer) | Schema validation (config, frontmatter, graph artifact) |
| yaml | pinned in lockfile (engine importer) | Frontmatter/config YAML parsing |
| pdfjs-dist / xlsx / bibtex / xml / csv / toml / ical / mbox parsers | pinned in lockfile (engine importer) | 30+ input-format ingestion |
| cytoscape | pinned in lockfile (viewer importer) | Graph viewer rendering |
| react / react-dom | `^19.1.1` | Viewer UI framework |
| react-markdown / highlight.js | pinned in lockfile (viewer importer) | Markdown + code rendering in viewer |
| vite / `@vitejs/plugin-react` | pinned in lockfile (viewer importer) | Viewer build/dev |
| obsidian | dev pin (obsidian-plugin importer) | Obsidian plugin API |
| esbuild / tslib | dev pins (obsidian-plugin importer) | Plugin bundling/runtime helpers |
| vitest / tsup | dev pins (cli importer) | Test runner / bundler |
| playwright | `^1.59.1` | E2E/smoke testing (root importer) |

## 8. CLI / Usage Surface

Entry points: `npm install -g @swarmvaultai/cli` then `swarmvault` (README.md:136-154); Desktop app bundles its own runtime via `swarmvault-desktop` releases, no Node required (README.md:126-130); Obsidian palette via `swarmvault` plugin 3.21.0 desktop-only (manifest.json:1-11).

| Goal | Command |
|---|---|
| Beginner path | `swarmvault quickstart ./your-repo` (alias `scan`) |
| No repo handy | `swarmvault demo` |
| Best next action (read-only) | `swarmvault next` |
| Suppress viewer | `quickstart ./path --no-serve` / `scan ./path --no-viz` |
| Init / ingest / compile loop | `init --obsidian --profile personal-research`, `ingest ./src --repo-root .`, `ingest ./meeting.srt --guide`, `add <url>`, `compile` |
| Registered sources | `source add` / `source list` / `source reload --all` / `source session <id>`; `clone <github-url> --no-viz` |
| Freshness / refresh | `graph status ./src`, `check-update ./src`, `update ./src`, `graph cluster` / `cluster-only` |
| Validate / stats | `graph stats`, `graph validate --strict` |
| Query / context / tasks | `query "<q>"`, `context build "<task>" --target ./src --budget 8000`, `task start "<task>" --target ./src --agent codex`, `chat "<q>"`, `export ai --out ./exports/ai` |
| Share / export | `graph share --post` / `--svg` / `--bundle`, `graph export --report` / `--callflow` / `--obsidian` / `--neo4j`, `graph push neo4j --dry-run`, `merge-graphs`, `tree --output` |
| Health | `doctor`, `doctor --repair` |
| Stable extended set (STABILITY.md) | `retrieval`, `explore`, `lint`, `review`, `candidate`, `watch`, `hook`, `schedule`, `diff`, `benchmark`, `consolidate`, `migrate`, `install --agent`, `mcp`, `--json`, `--version` |

Env-var and config tables:

| Variable | Effect |
|---|---|
| `SWARMVAULT_OUT` | Relocates generated `raw/`, `wiki/`, `state/`, `agent/`, `inbox/` under output dir; config + schema stay at root (README.md:182) |
| `.env` / `.env.*` | Git-excluded secret carrier (`.gitignore:8-14`); provider keys live here, not in repo |

| Config key group (`swarmvault.config.json`) | Controls |
|---|---|
| `graph.similarityIdfFloor`, `graph.similarityEdgeCap`, `graph.godNodeLimit`, `graph.foldCommunitiesBelow` | Edge density, hub capping, community folding (SCALE.md:1182-1193) |
| `repoAnalysis.classifyGlobs`, `repoAnalysis.extractClasses` | Code classification/extraction scope |
| `benchmark.enabled` | `state/benchmark.json` `contextTokensNaive` vs `contextTokensGraphGuided` tracking |
| `consolidation.enabled` | Vault consolidation behavior |
| `freshness.defaultHalfLifeDays` | Freshness decay scoring |
| `workspace.*`, `providers.*`, `tasks.*`, `retrieval.*` (`search.*` alias), `redaction.*` | Stable config surface; `search.*` to `retrieval.*` migrated by `migrate --target 3.0.0` (STABILITY.md:1287-1316) |

## 9. Extensibility Points

- **Custom providers and search:** implement a custom provider/search module; Experimental tier, may change any minor (STABILITY.md:1384-1393). Start from the engine provider interface and `swarmvault.config.json` `providers.*` / `retrieval.*` keys (SCALE.md:1182-1193, STABILITY.md:1287-1316).
- **Orchestration executors:** pluggable executors for watch/schedule automation; Experimental (STABILITY.md:1384-1393). Wire via `watch`, `hook`, `schedule` CLI and git hooks (README.md:92).
- **Vault conventions:** edit `swarmvault.schema.md` or fork `templates/llm-wiki-schema.md` to change page structure, domain priorities, and extraction conventions without touching code (README.md:71-79).
- **Retrieval tuning:** adjust `graph.*`, `repoAnalysis.*`, `freshness.*`, `consolidation.*` in `swarmvault.config.json`; migrate renames with `migrate --target 3.0.0` (SCALE.md:1182-1193, STABILITY.md:1287-1316).
- **Agent integration:** `install --agent` writes direct rules vs extended skill bundles; `agent/` helpers are generated per vault; MCP tools (`ingest`, `compile`, `query`, `explore`, `lint`, `search`, `page`, candidate/approval/context/task/memory/retrieval/doctor/graph/consolidate/migrate verbs) expose the vault to agents (README.md:92, STABILITY.md:1318-1322).
- **Graph sinks:** add export/push targets beside HTML/callflow/Obsidian/Neo4j-Cypher and `graph push neo4j` (README.md:207-224); graph artifact fields are Stable (`generatedBy`, `nodes[]`, `edges[]`, `hyperedges[]`, `communities[]`, `pages[]`, `sources[]`), so new sinks should read those (STABILITY.md:1352-1367).
- **Viewer and Obsidian plugin:** extend `packages/viewer` (Cytoscape + React 19) or the desktop-only Obsidian plugin (`manifest.json:1-11`, palette commands + status-bar freshness).

## 10. Limitations and Gotchas

- **Only two wiki component pages were available for this summary.** The analyzed chunk set covers `README.md` behavior and root-level files only; engine internals (`packages/cli`, `packages/engine`, viewer code, provider implementations) are characterized solely through CLI/config/lockfile headers, and the lockfile package index plus both localized READMEs were truncated in the chunks.
- **Cold compiles cost 3x-6x a warm incremental budget.** Tested warm envelopes are Small (<30 s, 500 sources / 2k pages / 5k nodes / 25k edges), Medium (<3 min), Large (<15 min); cold full re-analysis multiplies those (SCALE.md:1160-1172). Cached embedding providers are recommended from Medium up; Large wants embedding + audio providers with local caching plus Neo4j sink.
- **Viewer and retrieval degrade at scale without tuning.** Cytoscape viewer caps around ~10k nodes; SQLite FTS5 sharding, Louvain/god-node memory (documented escape hatch `node --max-old-space-size=8192`), and `graph.similarityEdgeCap` / `graph.similarityIdfFloor` density caps require active `swarmvault.config.json` tuning (SCALE.md:1176-1193).
- **Generated vault dirs are invisible to git and containers by default.** `raw/`, `wiki/`, `state/` (plus `tmp/`, logs, coverage) are excluded by both `.dockerignore:8-15` and `.gitignore:7-15`; `agent/` and `.env*` are git-excluded only. Teams must use explicit `--commit` workflows and exports (`graph export`, `export ai`, share-kit) or artifacts will not travel.
- **Platform and doc-freshness constraints are narrow.** The Obsidian plugin is desktop-only (`isDesktopOnly: true`, app `>=1.5.0`, manifest.json:1-11); CLI needs Node `>=24` (or the Desktop bundle); docs are English-first with `README.md` authoritative over `README.ja.md` / `README.zh-CN.md` on divergence; `init --lite` behavior was cut mid-sentence in the chunk set and cannot be relied on from this summary.

## 11. How It Compares to Alternatives

- **Karpathy's LLM Wiki gist:** the explicit ancestor. The gist describes the three-layer raw/wiki/schema pattern manually; SwarmVault implements it as CLI commands with typed graph, viewer, share kit, context packs, task ledger, doctor/workbench, 30+ formats, tree-sitter code awareness, offline mode, contradiction detection, approvals, Neo4j export, MCP server, watch mode, and hybrid search (README.md:86, README.md:101-121).
- **Obsidian:** local markdown knowledge base with palette-driven PKM. SwarmVault complements it: it can emit an Obsidian workspace (`init --obsidian`, `graph export --obsidian`) and ships a desktop-only Obsidian plugin (manifest.json:1-11) that runs ingest/compile/query/review from the palette, but the vault itself remains a compiled CLI artifact rather than a hand-authored note graph.
- **Neo4j:** production graph database and Cypher ecosystem. SwarmVault keeps the working graph local (`state/graph.json` + graphology) and treats Neo4j as an optional sink (`graph export --neo4j`, `graph push neo4j`), recommended at Large tier (SCALE.md:1160-1172) rather than as the default store.
- **Local RAG stacks (Ollama embeddings + SQLite FTS):** the standard offline retrieval recipe. SwarmVault productizes it: heuristic-by-default with Ollama `gemma4`/`nomic-embed-text` sharpening, SQLite FTS5 + semantic embeddings with rerank, bounded token budgets, graph-guided context packs (`benchmark.json` tracks naive vs graph-guided tokens), and Stable MCP/config/frontmatter contracts (README.md:90-94, SCALE.md:1195-1201, STABILITY.md:1226-1393).

Positioning: SwarmVault is the production CLI around the LLM-Wiki pattern — local-first and offline-capable by default, graph-typed and agent-addressable (MCP, context packs, task ledger) where note apps are manual and where graph databases or bare RAG kits require assembly.

## Appendix: Selected Code Snippets

`pnpm-workspace.yaml:1-3` — monorepo scope:

```yaml
packages:
  - packages/*
```

`.npmrc:1-2` — workspace-local resolution:

```text
link-workspace-packages=true
prefer-workspace-packages=true
```

`manifest.json:1-11` — Obsidian plugin identity:

```json
{
  "id": "swarmvault",
  "name": "SwarmVault",
  "version": "3.21.0",
  "minAppVersion": "1.5.0",
  "description": "Runs SwarmVault ingest, compile, query, and review commands from the command palette and surfaces compile freshness in your status bar.",
  "author": "SwarmVault",
  "authorUrl": "https://www.swarmvault.ai",
  "isDesktopOnly": true
}
```

`tsconfig.base.json:1-16` — shared TypeScript baseline:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "strict": true,
    "declaration": true,
    "sourceMap": true,
    "resolveJsonModule": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "types": ["node"]
  }
}
```
