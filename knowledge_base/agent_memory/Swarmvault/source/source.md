# swarmclawai/swarmvault
Source: https://github.com/swarmclawai/swarmvault
Kind: repo
Fetched: 2026-09-26T13:40:51.878781+00:00
Tool: git-clone
Research-Target: /Users/sergii/.ai/knowledge/research_topics/agent_memory/research/AgentBrain
Topic: agent_memory

# swarmclawai/swarmvault

Commit: 815412d24298e59e5073ded1ddd6c0e6aee9b91b

## README

# SwarmVault

<!-- readme-language-nav:start -->
**Languages:** [English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)
<!-- readme-language-nav:end -->

[![npm](https://img.shields.io/npm/v/@swarmvaultai/cli)](https://www.npmjs.com/package/@swarmvaultai/cli)
[![npm downloads](https://img.shields.io/npm/dw/@swarmvaultai/cli)](https://www.npmjs.com/package/@swarmvaultai/cli)
[![GitHub stars](https://img.shields.io/github/stars/swarmclawai/swarmvault)](https://github.com/swarmclawai/swarmvault)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![node](https://img.shields.io/badge/node-%3E%3D24-brightgreen)]()

**The local-first LLM Wiki, knowledge graph builder, and RAG knowledge base for AI agents.** SwarmVault turns docs, code, transcripts, notes, and URLs into a durable markdown wiki plus a local graph you can inspect, query, and hand to agents. Start with one command, then learn the deeper graph, review, context-pack, and automation workflows when you need them.

Documentation on the website is currently English-first. If wording drifts between translations, [README.md](README.md) is the canonical source.

<!-- readme-section:try-it -->


## Try It in 30 Seconds

```bash
npm install -g @swarmvaultai/cli
swarmvault quickstart ./your-repo
```

`quickstart` initializes a vault in the current directory, ingests a local file, directory, or public GitHub repo, compiles the wiki and graph, writes share artifacts, and opens the local graph viewer. It is the beginner-friendly alias for `swarmvault scan`.

No repo handy?

```bash
swarmvault demo
```

After your first compile, the most useful next commands are:

```bash
swarmvault next
swarmvault query "What are the key concepts?"
swarmvault graph serve
swarmvault doctor
swarmvault candidate list
```

Not sure what state the vault is in? `swarmvault next` is read-only and tells you whether to initialize, ingest, compile, query, review, or refresh.

![SwarmVault graph workspace](https://www.swarmvault.ai/images/screenshots/graph-workspace.png)

No API keys are required for the first run. The built-in heuristic provider runs locally and offline.

**What you get on disk:**

- `raw/` - immutable copies of ingested material
- `wiki/` - generated markdown pages, saved outputs, graph reports, context packs, and task notes
- `state/graph.json` - the machine-readable knowledge graph
- `state/retrieval/` - local search index
- `wiki/graph/share-card.md`, `wiki/graph/share-card.svg`, and `wiki/graph/share-kit/` - copyable and visual first-run summaries



### Three-Layer Architecture

SwarmVault uses three layers, following the pattern described by Andrej Karpathy:

1. **Raw sources** (`raw/`) — your curated collection of source documents. Books, articles, papers, transcripts, code, images, datasets. These are immutable: SwarmVault reads from them but never modifies them.
2. **The wiki** (`wiki/`) — LLM-generated and human-authored markdown. Source summaries, entity pages, concept pages, cross-references, dashboards, and outputs. The wiki is the persistent, compounding artifact.
3. **The schema** (`swarmvault.schema.md`) — defines how the wiki is structured, what conventions to follow, and what matters in your domain. You and the LLM co-evolve this over time.

> In the tradition of Vannevar Bush's Memex (1945) — a personal, curated knowledge store with associative trails between documents — SwarmVault treats the connections between sources as valuable as the sources themselves. The part Bush couldn't solve was who does the maintenance. The LLM handles that.

Turn books, articles, notes, transcripts, mail exports, calendars, datasets, slide decks, screenshots, URLs, and code into a persistent knowledge vault with a knowledge graph, local search, dashboards, and reviewable artifacts that stay on disk. Use it for **personal knowledge management**, **research deep-dives**, **book companions**, **code documentation**, **business intelligence**, or any domain where you accumulate knowledge over time and want it organized rather than scattered.

SwarmVault turns the LLM Wiki pattern into a local toolchain with graph navigation, search, review, automation, and optional model-backed synthesis. You can also start with just the [standalone schema template](templates/llm-wiki-schema.md) — zero install, any LLM agent — and graduate to the full CLI when you outgrow it.

<!-- readme-section:why -->


## Why SwarmVault

If you liked Karpathy's [LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), SwarmVault is the production-grade version. Here's how it addresses the most common concerns from the community:

**"Won't hallucinations compound?"** — Every edge is tagged `extracted`, `inferred`, or `ambiguous`. Contradiction detection flags conflicting claims. `compile --approve` stages all changes into reviewable approval bundles. New concepts land in `wiki/candidates/` first. `lint --conflicts` audits for contradictions on demand.

**"Does it scale past 100 pages?"** — Yes. Hybrid search merges SQLite full-text with semantic embeddings, so queries work without fitting every page into context. `compile --max-tokens` trims output to fit bounded windows. Graph navigation (`graph query`, `graph path`, `graph explain`, `graph callers`) lets you traverse rather than search.

**"Is it just for personal use?"** — Git-backed workflows (`--commit`), watch mode with git hooks, scheduled automation, and an MCP server make it usable for teams. Agent integrations cover direct-rule targets plus the extended skill-bundle roster.

**"Do I need API keys?"** — No. The built-in `heuristic` provider is fully offline. For sharper extraction, pair with a free local LLM via [Ollama](https://ollama.com). Cloud providers are optional.

<!-- readme-section:comparison -->


## From Gist to Production

| | Karpathy's Gist | **SwarmVault** |
|---|:---:|:---:|
| Three-layer architecture | described | **implemented** |
| Ingest / query / lint | manual | **CLI commands** |
| One-command setup | — | **`swarmvault quickstart`** |
| Typed knowledge graph | — | **yes** |
| Interactive graph viewer | — | **yes** |
| Visual + post-ready share kit | — | **yes** |
| Agent-ready context packs | — | **yes** |
| Agent task ledger | — | **yes** |
| Vault doctor + workbench | — | **yes** |
| 30+ input formats | — | **yes** |
| Code-aware (tree-sitter AST) | — | **yes** |
| Offline / no API keys | — | **yes** |
| Contradiction detection | mentioned | **automatic** |
| Approval queues | — | **yes** |
| Agent integrations | — | **yes** |
| Neo4j / graph export | — | **yes** |
| MCP server | — | **yes** |
| Watch mode + git hooks | — | **yes** |
| Hybrid search + rerank | index.md | **SQLite FTS + embeddings** |

<!-- readme-section:install -->


### Desktop App (no Node.js required)

Download the desktop app for macOS, Windows, or Linux — bundles its own runtime:

**[Download Desktop App](https://www.swarmvault.ai/download)** | [GitHub Releases](https://github.com/swarmclawai/swarmvault-desktop/releases)



### CLI

SwarmVault requires Node `>=24`.

```bash
npm install -g @swarmvaultai/cli
```

Verify the install:

```bash
swarmvault --version
```

Update to the latest published release:

```bash
npm install -g @swarmvaultai/cli@latest
```

The global CLI already includes the graph viewer workflow and MCP server flow. End users do not need to install `@swarmvaultai/viewer` separately.

<!-- readme-section:quickstart -->


### Fast Path

Run this from an empty folder or a scratch folder where you want the vault artifacts to live:

```bash
mkdir my-vault
cd my-vault
swarmvault quickstart ../your-repo
swarmvault next
```

That is the easiest path for a new user. It does the same work as `swarmvault scan`: initialize the vault, ingest a local file, directory, or public GitHub repo, compile the wiki and graph, write share artifacts, and open the graph viewer unless you pass `--no-serve` or `--no-viz`. Interactive runs show bounded ingest progress on stderr, including the active file, so large PDFs and document folders do not look silent while extraction runs.

```text
my-vault/
├── swarmvault.schema.md       user-editable vault instructions
├── raw/                       immutable source files and localized assets
├── wiki/                      compiled wiki: sources, concepts, entities, code, outputs, graph
├── state/                     graph.json, retrieval/, embeddings, sessions, approvals
├── .obsidian/                 optional Obsidian workspace config
└── agent/                     generated agent-facing helpers
```

If you want to keep generated artifacts outside the source tree, run with `SWARMVAULT_OUT=.swarmvault-out`. `swarmvault.config.json` and `swarmvault.schema.md` stay in the project root; `raw/`, `wiki/`, `state/`, `agent/`, and `inbox/` resolve under the output directory.



### Learn The Main Loop

Once the fast path makes sense, the same workflow can be run step by step:

```bash
swarmvault init --obsidian --profile personal-research
swarmvault ingest ./src --repo-root .
swarmvault ingest ./meeting.srt --guide
swarmvault add https://arxiv.org/abs/2401.12345
swarmvault compile
swarmvault next
swarmvault query "What is the auth flow?"
swarmvault graph serve
```

Use `swarmvault source add https://github.com/karpathy/micrograd`, `swarmvault source add https://example.com/docs/getting-started`, `swarmvault source list`, `swarmvault source reload --all`, and `swarmvault source session transcript-or-session-id` when the same repo, folder, or docs hub should stay registered and refreshable. For public GitHub repos, `swarmvault clone https://github.com/owner/repo --no-viz` and `swarmvault source add https://github.com/owner/repo --branch main --checkout-dir .swarmvault-checkouts/repo` are the reusable checkout paths.



### Common Next Commands

| Goal | Command |
| --- | --- |
| See the best next command for this folder | `swarmvault next` |
| Run the beginner path without opening the viewer | `swarmvault quickstart ./path --no-serve` |
| Use the older concise alias | `swarmvault scan ./path --no-viz` |
| Inspect graph freshness | `swarmvault graph status ./src` or `swarmvault check-update ./src` |
| Refresh code-derived graph artifacts | `swarmvault update ./src` |
| Recompute graph communities | `swarmvault graph cluster` or `swarmvault cluster-only` |
| Print graph counts and validate exports | `swarmvault graph stats` and `swarmvault graph validate --strict` |
| Share the first-run summary | `swarmvault graph share --post`, `swarmvault graph share --svg ./share-card.svg`, or `swarmvault graph share --bundle ./share-kit` |
| Export for agents or other tools | `swarmvault export ai --out ./exports/ai` |
| Build bounded agent context | `swarmvault context build "Implement the auth refactor" --target ./src --budget 8000` |
| Record task history | `swarmvault task start "Implement the auth refactor" --target ./src --agent codex` |
| Keep a conversation over the vault | `swarmvault chat "How should the next agent use this vault?"` |
| Open health and repair guidance | `swarmvault doctor --repair` |
| Build graph exports | `swarmvault graph export --report ./exports/report.html`, `swarmvault graph export --callflow ./exports/callflow.html`, `swarmvault graph export --obsidian ./exports/graph-vault`, or `swarmvault graph export --neo4j ./exports/graph.cypher` |
| Merge or inspect source/module trees | `swarmvault tree --output ./exports/tree.html` and `swarmvault merge-graphs ./exports/graph.json ./other-graph.json --out ./exports/merged-graph.json` |
| Push graph data to Neo4j | `swarmvault graph push neo4j --dry-run` |

Want the minimal LLM-Wiki starter instead? `swarmvault init --lite` creates just `raw/`, `wiki/`, `wiki/index.md`, `wiki/log.md`, and `swarmvault.schema.md` - no config, no state, no agent installs. Normal `init`, `quickstart`, `scan`, and `clone` also avoid writing agent rule files by default; run `swarmvault 

... (truncated, 36521 more characters)

## package.json

```
{
  "name": "swarmvault-opensource",
  "private": true,
  "version": "3.21.0",
  "type": "module",
  "packageManager": "pnpm@10.32.1",
  "scripts": {
    "build": "pnpm --filter @swarmvaultai/viewer build && pnpm --filter @swarmvaultai/engine build && pnpm --filter @swarmvaultai/cli build",
    "test": "node ./scripts/check-published-manifests.mjs && node --test ./scripts/release-preflight-summary.test.mjs && pnpm -r test",
    "lint": "biome check .",
    "lint:fix": "biome check --write .",
    "format": "biome format --write .",
    "typecheck": "pnpm -r typecheck",
    "check": "biome check . && pnpm -r typecheck && node ./scripts/check-release-sync.mjs && node ./scripts/check-published-manifests.mjs && node ./scripts/check-readme-parity.mjs && node ./scripts/check-clawhub-skill.mjs",
    "check:release-sync": "node ./scripts/check-release-sync.mjs",
    "check:published-manifests": "node ./scripts/check-published-manifests.mjs",
    "check:readme-parity": "node ./scripts/check-readme-parity.mjs",
    "check:clawhub-skill": "node ./scripts/check-clawhub-skill.mjs",
    "check:perf": "node ./scripts/check-perf-budget.mjs",
    "docs:screenshots": "node ./scripts/sync-docs-screenshots.mjs",
    "live:smoke:heuristic": "node ./scripts/live-smoke.mjs --lane heuristic",
    "live:smoke:heuristic:browser": "node ./scripts/live-smoke.mjs --lane heuristic --browser-check",
    "live:smoke:neo4j": "node ./scripts/live-smoke.mjs --lane neo4j",
    "live:smoke:ollama": "node ./scripts/live-smoke.mjs --lane ollama",
    "live:smoke:openai": "node ./scripts/live-smoke.mjs --lane openai",
    "live:smoke:anthropic": "node ./scripts/live-smoke.mjs --lane anthropic",
    "live:oss:corpus": "node ./scripts/live-oss-corpus.mjs",
    "live:cli-surface": "node ./scripts/cli-surface-smoke.mjs",
    "release:preflight": "node ./scripts/release-preflight.mjs",
    "release:publish": "node ./scripts/release-publish.mjs",
    "skill:publish": "node ./scripts/publish-clawhub-skill.mjs",
    "skill:inspect": "clawhub inspect swarmvault --files",
    "prepare": "lefthook install"
  },
  "devDependencies": {
    "@biomejs/biome": "^2.4.10",
    "@evilmartians/lefthook": "^2.1.5",
    "playwright": "^1.59.1",
    "typescript": "^5.9.3"
  }
}

```

## Top-level layout

- .dockerignore (~19 lines)
- .github/ (dir, 2 files, ~301 lines)
- .gitignore (~19 lines)
- .npmrc (~2 lines)
- biome.json (~54 lines)
- CHANGELOG.md (~764 lines)
- CONTRIBUTING.md (~66 lines)
- Dockerfile (~46 lines)
- docs/ (dir, 2 files, ~290 lines)
- glama.json (~4 lines)
- lefthook.yml (~6 lines)
- LICENSE (~21 lines)
- manifest.json (~10 lines)
- package.json (~41 lines)
- packages/ (dir, 232 files, ~89300 lines)
- pnpm-lock.yaml (~6801 lines)
- pnpm-workspace.yaml (~2 lines)
- README.ja.md (~644 lines)
- README.md (~642 lines)
- README.zh-CN.md (~642 lines)
- SCALE.md (~61 lines)
- scripts/ (dir, 16 files, ~6197 lines)
- skills/ (dir, 10 files, ~1297 lines)
- smoke/ (dir, 52 files, ~380 lines)
- STABILITY.md (~176 lines)
- templates/ (dir, 1 files, ~119 lines)
- tsconfig.base.json (~15 lines)
- validation/ (dir, 1 files, ~105 lines)
- worked/ (dir, 16 files, ~554 lines)

