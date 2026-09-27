---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: swarmclawai/swarmvault

### Q1. What is SwarmVault in one sentence, and what does it turn its inputs into?
> [!tip]- Answer
> SwarmVault is a local-first LLM Wiki, knowledge graph builder, and RAG knowledge base for AI agents. It ingests docs, code, transcripts, notes, and URLs into a durable markdown wiki plus an inspectable, queryable local graph. See [[wiki/01-overview|Overview]].

### Q2. What does `swarmvault quickstart` do, and why does the first run need no API keys?
> [!tip]- Answer
> `quickstart` (alias of `scan`) initializes a vault, ingests a local file/directory or public GitHub repo, compiles the wiki and graph, writes share artifacts, and opens the graph viewer. No API keys are needed because the built-in heuristic provider runs locally and offline, with Ollama or cloud providers optional later. See [[wiki/01-overview|Overview]].

### Q3. Describe the three-layer architecture: what lives in `raw/`, `wiki/`, and `swarmvault.schema.md`?
> [!tip]- Answer
> `raw/` holds immutable copies of ingested sources that SwarmVault reads but never modifies. `wiki/` holds LLM-generated and human-authored markdown: entity/concept pages, cross-references, outputs, and the compounding persistent artifact. `swarmvault.schema.md` defines wiki structure and conventions and co-evolves with use. See [[wiki/01-overview|Overview]].

### Q4. How does SwarmVault control hallucinations and scale past ~100 pages?
> [!tip]- Answer
> Every edge is tagged `extracted`, `inferred`, or `ambiguous`, contradictions are flagged, risky changes stage in `wiki/candidates/` via `compile --approve` bundles, and `lint --conflicts` audits the vault. Scale comes from hybrid SQLite full-text plus semantic-embedding search, bounded `compile --max-tokens` output, and traversal commands `graph query`, `graph path`, `graph explain`, and `graph callers`. See [[wiki/01-overview|Overview]].

### Q5. What do the repo-root workspace, toolchain, and TypeScript baseline pin in place?
> [!tip]- Answer
> The root is a pnpm monorepo with the sole workspace glob `packages/*` plus `link-workspace-packages` and `prefer-workspace-packages` forcing local resolution. Biome 2.4.10 enforces format/lint with a lefthook pre-commit `biome check` on staged TS/JS/JSON files. The shared baseline targets ES2022 with ESNext modules, Bundler resolution, strict mode, declarations, and source maps. See [[wiki/02-top-level-files|Top-Level Files]].

### Q6. What contracts do `SCALE.md` and `STABILITY.md` define, and where do their knobs live?
> [!tip]- Answer
> `SCALE.md` defines Small/Medium/Large tiers with compile budgets and degradation notes, tuned via `swarmvault.config.json` keys like similarity caps and community folding. `STABILITY.md` defines the semver/deprecation contract with Stable tables for CLI subcommands, config keys, MCP tools, page frontmatter, graph artifacts, and state files. Both keep operating limits and API promises outside code. See [[wiki/02-top-level-files|Top-Level Files]].

### Q7. (Evaluation) Would you recommend SwarmVault for a solo developer documenting a growing codebase with an AI agent, and why?
> [!tip]- Answer
> Yes, because the offline `quickstart` path, typed graph with approval queues, and bounded agent context packs directly fit an agent-assisted codebase that must stay queryable as it grows. The main caveat is the Node >= 24 CLI plus config/scale tuning overhead, which is heavier than plain markdown notes for tiny vaults. On balance the provenance and traversal payoff justifies it once sources accumulate. See [[wiki/01-overview|Overview]].
