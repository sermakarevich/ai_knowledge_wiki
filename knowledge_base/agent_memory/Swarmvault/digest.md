> [[index|Wiki]] | [[summary|Summary]]
# swarmclawai/swarmvault — Digest

## 1. [[wiki/01-overview|Overview]]
**In one sentence:** SwarmVault is a local-first LLM Wiki, knowledge graph builder, and RAG knowledge base for AI agents that turns docs, code, transcripts, notes, and URLs into a durable markdown wiki plus a local graph (README.md:19).
## Key points
- SwarmVault is a local-first LLM Wiki, knowledge graph builder, and RAG knowledge base that ingests docs, code, transcripts, notes, and URLs into a markdown wiki plus inspectable, queryable local graph (README.md:19).
- `quickstart` is the beginner-friendly alias for `scan`: it initializes a vault, ingests a local file/directory or public GitHub repo, compiles wiki and graph, writes share artifacts, and opens the graph viewer (README.md:33).
- No API keys are required for the first run because the built-in heuristic provider runs locally and offline (README.md:55).
- The three-layer architecture is raw immutable sources in `raw/`, generated/authored markdown in `wiki/`, and co-evolved conventions in `swarmvault.schema.md` (README.md:71-73).
- Quality controls tag every edge `extracted`, `inferred`, or `ambiguous`, flag contradictions, stage changes into approval bundles via `compile --approve`, land new concepts in `wiki/candidates/` first, and audit via `lint --conflicts` (README.md:88).
- Scale comes from hybrid SQLite full-text plus semantic-embedding search, bounded `compile --max-tokens` output, and graph traversal commands `graph query`, `graph path`, `graph explain`, `graph callers` (README.md:90).
- Team use is via git-backed `--commit` workflows, watch mode with git hooks, scheduled automation, an MCP server, and direct-rule plus skill-bundle agent integrations (README.md:92).
- The CLI requires Node `>=24`, installs via `npm install -g @swarmvaultai/cli`, and already includes the graph viewer and MCP server flow with no separate `@swarmvaultai/viewer` install (README.md:136-154).

## 2. [[wiki/02-top-level-files|Top-Level Files]]
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

## The system in five moves
1. SwarmVault starts as a local-first, offline-capable LLM wiki that turns arbitrary sources into a durable markdown wiki plus a queryable local graph.
2. A beginner-friendly `quickstart`/`scan` flow initializes the vault, ingests files or repos, compiles artifacts, and opens the graph viewer with no API keys.
3. The three-layer `raw/`-`wiki/`-schema architecture keeps sources immutable while the wiki and conventions compound over time.
4. Trust and scale are enforced by typed edges, contradiction detection, approval bundles, hybrid search, bounded compile output, and graph traversal commands.
5. Team and agent use ride on git workflows, watch mode, scheduling, the MCP server, and generated agent helpers.
6. The repo root pins all of this in place with a pnpm workspace, Biome/lefthook toolchain, TypeScript baseline, plugin/registry metadata, and the SCALE/STABILITY contracts.
