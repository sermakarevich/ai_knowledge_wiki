> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-Level Files
**In one sentence:** The repo root pins the pnpm workspace, toolchain configs, plugin/registry metadata, multilingual READMEs, and the scale/stability contracts that bound everything under `packages/`.
## Key points
- The root is a `pnpm` monorepo whose only workspace glob is `packages/*` (`pnpm-workspace.yaml:1-2`), with `link-workspace-packages=true` and `prefer-workspace-packages=true` forcing workspace-local resolution (`.npmrc:1-2`).
- Docker and git exclusion keep build context and version control free of outputs and local vault state: `.dockerignore` excludes `node_modules`, `**/dist`, `.git`, logs, `coverage`, `tmp`, `state`, `wiki`, `raw`, `worked`, `inbox`, `smoke`, `validation`, and `templates` (`.dockerignore:1-20`), while `.gitignore` additionally excludes `spec.md`, `.turbo/`, `.env`/`.env.*`, `agent/`, `docs/superpowers/`, `packages/viewer/dist/`, and artifact dirs (`.gitignore:1-20`).
- Formatting and linting are enforced by Biome 2.4.10 with recommended rules plus `noForEach: off` and `noNonNullAssertion: off`, space indent width 2, line width 140, double quotes, trailing commas none, semicolons always (`biome.json:1-55`), and a pre-commit lefthook `lint` command runs `pnpm biome check --no-errors-on-unmatched --files-ignore-unknown=true {staged_files}` on `*.{ts,tsx,js,jsx,json}` with `stage_fixed: true` (`lefthook.yml:1-7`).
- The distributable identity is an Obsidian desktop-only plugin `swarmvault` / `SwarmVault` version `3.21.0` requiring app `>=1.5.0`, whose description promises palette commands for ingest/compile/query/review plus status-bar compile freshness (`manifest.json:1-11`), alongside a Glama MCP registry stub declaring schema `https://glama.ai/mcp/schemas/server.json` and maintainer `swarmclawai` (`glama.json:1-5`).
- Dependency resolution is locked by `pnpm-lock.yaml` (`lockfileVersion: '9.0'`) covering root dev tools (biome, lefthook, playwright, typescript) and importers `packages/cli`, `packages/engine`, `packages/obsidian-plugin`, `packages/viewer` (`pnpm-lock.yaml:1-50`); only the importer header and package-index head were visible in the chunk, remainder truncated.
- The shared TypeScript baseline targets `ES2022` with `ESNext` modules, `Bundler` resolution, `strict`, `declaration`, `sourceMap`, `resolveJsonModule`, `esModuleInterop`, `skipLibCheck`, consistent casing, and `types: ["node"]` (`tsconfig.base.json:1-16`).
- Human entry points are the Japanese (`README.ja.md`) and Simplified Chinese (`README.zh-CN.md`) localizations of the English README (both state `README.md` is authoritative on divergence), documenting `quickstart`/`scan`/`demo`/`next`/`query`/`graph serve` flows, `raw/`-`wiki/`-`state/` disk layout, provider setup, and gist-to-production comparison tables; both files were truncated in the chunk so only the head sections were summarized.
- Operating limits and API promises live outside code: `SCALE.md` defines Small/Medium/Large tiers with compile budgets and degradation notes plus `swarmvault.config.json` tuning knobs (`SCALE.md:1-62`), while `STABILITY.md` defines the semver/deprecation contract and Stable tables for CLI subcommands, config keys, MCP tools, frontmatter, graph artifact, and state files (`STABILITY.md:1-177`).
---
## Ignore and container exclusion
`.dockerignore:1-20` (verbatim):
```text
node_modules
**/node_modules
**/dist
.git
.github
.vscode
.idea
*.log
coverage
tmp
state
wiki
raw
worked
inbox
docs/**/*.png
smoke
validation
templates
```
`.gitignore:1-20` (verbatim):
```text
spec.md
node_modules/
dist/
coverage/
.turbo/
.DS_Store
*.log
.env
.env.*
raw/
wiki/
state/
agent/
tmp/
docs/superpowers/
packages/viewer/dist/
.live-smoke-artifacts/
.oss-corpus-artifacts/
.release-preflight/
```
Both exclude generated/local state (`raw/`, `wiki/`, `state/`, `tmp/`, `*.log`, `coverage`) (`.dockerignore:8-15`, `.gitignore:7-15`); only `.gitignore` excludes secrets and agent/output dirs (`.env`, `.env.*`, `agent/`) (`.gitignore:8-14`).
## Package management and workspace
`pnpm-workspace.yaml:1-3` (verbatim):
```yaml
packages:
  - packages/*
```
`.npmrc:1-2` (verbatim):
```text
link-workspace-packages=true
prefer-workspace-packages=true
```
`pnpm-lock.yaml:1-9` declares `lockfileVersion: '9.0'` with `autoInstallPeers: true` and `excludeLinksFromLockfile: false`. Importers pinned in the visible head (`pnpm-lock.yaml:14-50`):
| Importer | Notable pins |
|---|---|
| `.` (root) | `@biomejs/biome ^2.4.10`, `@evilmartians/lefthook ^2.1.5`, `playwright ^1.59.1`, `typescript ^5.9.3` |
| `packages/cli` | `@swarmvaultai/engine 3.21.0` via `link:../engine`, `commander ^14.0.1`, `tsup`, `vitest` |
| `packages/engine` | `@modelcontextprotocol/sdk`, `graphology`, `neo4j-driver`, `pdfjs-dist`, `xlsx`, `zod`, `yaml`, plus parsers (bibtex, xml, csv, toml, ical, mbox) |
| `packages/obsidian-plugin` | `esbuild`, `obsidian`, `tslib`, `typescript`, `vitest` (dev-only) |
| `packages/viewer` | `cytoscape`, `react`/`react-dom ^19.1.1`, `react-markdown`, `highlight.js`, `vite`, `@vitejs/plugin-react` |
The bulk package index (`pnpm-lock.yaml:439+`, e.g. `@acemir/cssom`, `@babel/*`, `@asciidoctor/core`) was truncated in the chunk (206794 further characters cut), so dependency hashes below the importer block are not covered here.
## Lint, format, and hooks
`biome.json:64-90` sets linter `enabled: true`, `recommended: true`, `complexity.noForEach: off`, `style.noNonNullAssertion: off`; formatter `enabled: true`, `indentStyle: space`, `indentWidth: 2`, `lineWidth: 140`; JS formatter `quoteStyle: double`, `trailingCommas: none`, `semicolons: always`; `assist.enabled: true`. `biome.json:94-116` scopes `files.includes` to `**/*.ts`, `**/*.tsx`, `**/*.js`, `**/*.jsx`, `**/*.json` while excluding `**/dist`, `.live-smoke-artifacts`, `.oss-corpus-artifacts`, `node_modules`, `.next`, `out`, `pnpm-lock.yaml`, `**/raw`, `**/wiki`, `**/state`, `**/agent`, `**/inbox`, `**/.claude`, `**/.cursor`.
`lefthook.yml:1-7` (verbatim):
```yaml
pre-commit:
  commands:
    lint:
      glob: "*.{ts,tsx,js,jsx,json}"
      run: pnpm biome check --no-errors-on-unmatched --files-ignore-unknown=true {staged_files}
      stage_fixed: true
```
## Plugin manifest and registry metadata
`manifest.json:1-11` (verbatim excerpt):
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
`glama.json:1-5` (verbatim):
```json
{
  "$schema": "https://glama.ai/mcp/schemas/server.json",
  "maintainers": ["swarmclawai"]
}
```
## TypeScript baseline
`tsconfig.base.json:1-16` (verbatim):
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
## READMEs (localizations)
`README.ja.md:550-562` and `README.zh-CN.md:836-848` are the Japanese and Simplified Chinese mirrors of the English README (each carries a `readme-language-nav` block linking `README.md` / `README.zh-CN.md` / `README.ja.md` plus npm/downloads/stars/license/node badges). Both state docs are English-first and `README.md` is authoritative on divergence (`README.ja.md:564`, `README.zh-CN.md:850`). Visible heads document the 30-second `npm install -g @swarmvaultai/cli` + `swarmvault quickstart ./your-repo` path (alias of `swarmvault scan`), `swarmvault demo` fallback, post-compile `next` / `query` / `graph serve` / `doctor` / `candidate list` loop, no-API-key heuristic provider, and disk outputs `raw/`, `wiki/`, `state/graph.json`, `state/retrieval/`, `wiki/graph/share-card.*`/`share-kit/` (`README.ja.md:566-604`, `README.zh-CN.md:852-890`); the three-layer `raw/`-`wiki/`-`swarmvault.schema.md` architecture, offline/provider options (Ollama `gemma4`, `nomic-embed-text`, cloud `openai`/`gpt-4o` examples), and gist-vs-SwarmVault comparison table are partially visible but both files were truncated in the chunk (`README.ja.md` cut after ~645-line head, 26944 chars omitted; `README.zh-CN.md` cut after ~643-line head, 22061 chars omitted), so sections below provider setup are not covered here.
## Scale and stability contracts
`SCALE.md:1160-1172` records the tested envelope (verbatim table):
| Tier | Sources | Pages | Graph nodes | Graph edges | Compile budget (warm) | Recommended backend |
|---|---|---|---|---|---|---|
| Small | up to 500 | up to 2,000 | up to 5,000 | up to 25,000 | < 30 s | heuristic or any provider |
| Medium | up to 5,000 | up to 20,000 | up to 50,000 | up to 200,000 | < 3 min | cached embedding provider recommended |
| Large | up to 50,000 | up to 150,000 | up to 400,000 | up to 1,500,000 | < 15 min | embedding + audio providers with local caching; Neo4j sink useful |
Warm budgets assume incremental compile; cold full re-analysis runs 3x-6x slower (`SCALE.md:1172`). Degradation notes cover `state/retrieval/` SQLite FTS5 shard limits, Louvain/god-node memory (`node --max-old-space-size=8192`), `graph.similarityEdgeCap` / `graph.similarityIdfFloor` density caps, Cytoscape ~10k-node viewer limit, and per-source audio cost (`SCALE.md:1176-1180`). All tuning knobs live in `swarmvault.config.json`: `graph.similarityIdfFloor`, `graph.similarityEdgeCap`, `graph.godNodeLimit`, `graph.foldCommunitiesBelow`, `repoAnalysis.classifyGlobs`/`extractClasses`, `benchmark.enabled`, `consolidation.enabled`, `freshness.defaultHalfLifeDays` (`SCALE.md:1182-1193`); `swarmvault benchmark` artifact `state/benchmark.json` tracks `contextTokensNaive` vs `contextTokensGraphGuided` (`SCALE.md:1195-1201`); `pnpm check:perf` budgets live in `scripts/perf-budgets.json` (`SCALE.md:1212-1220`).
`STABILITY.md:1226-1246` declares semver 2.0.0 with Stable (major-bump protection), Experimental (any-minor change), and Internal tiers, plus a 5-step Stable deprecation window (announce, >=2 minor grace, `swarmvault lint` warning, `swarmvault migrate` transition, major-bump exception). Stable surfaces enumerated: CLI subcommands table (`init`, `demo`, `scan`, `ingest`, `add`, `source`, `inbox import`, `compile`, `query`, `context`, `task`/`memory`, `retrieval`, `doctor`, `explore`, `lint`, `review`, `graph`, `candidate`, `watch`, `hook`, `schedule`, `diff`, `benchmark`, `consolidate`, `migrate`, `install --agent`, `mcp`, `--json`, `--version`) (`STABILITY.md:1250-1285`); config keys (`workspace.*`, `providers.*`, `tasks.*`, `graph.*`, `retrieval.*`, `redaction.*`, `freshness.*`, `consolidation.*`, etc., with `search.*` -> `retrieval.*` alias migrated by `migrate --target 3.0.0`) (`STABILITY.md:1287-1316`); MCP tools (`ingest`, `compile`, `query`, `explore`, `lint`, `search`, `page`, candidate/approval/context/task/memory/retrieval/doctor/graph/consolidate/migrate verbs) (`STABILITY.md:1318-1322`); page frontmatter (`page_id`, `kind`, `tags`, `source_ids`, `freshness`, `decay_score`, `tier`, `task_id`, etc.) (`STABILITY.md:1324-1350`); `state/graph.json` fields (`generatedBy`, `nodes[]`, `edges[]`, `hyperedges[]`, `communities[]`, `pages[]`, `sources[]`, `benchmark?`) (`STABILITY.md:1352-1367`); and `state/` files (`graph.json`, `retrieval/`, `context-packs/`, `memory/tasks/`, `approvals/`, `candidates/`, `ingest-runs/`, `benchmark.json`, `embeddings.json`, `vault-version.json`) (`STABILITY.md:1369-1382`). Experimental: custom provider/search modules, orchestration executors, `local-whisper` provider, `provider setup` (`STABILITY.md:1384-1393`).
**Covers:** `.dockerignore`, `.gitignore`, `.npmrc`, `biome.json`, `glama.json`, `lefthook.yml`, `manifest.json`, `pnpm-lock.yaml` (importer head only; package index truncated), `pnpm-workspace.yaml`, `README.ja.md` (head only; truncated), `README.zh-CN.md` (head only; truncated), `SCALE.md`, `STABILITY.md`, `tsconfig.base.json`
