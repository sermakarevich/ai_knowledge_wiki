> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
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
---
## Try it in 30 seconds
Beginner path (README.md:29-33):
```bash
npm install -g @swarmvaultai/cli
swarmvault quickstart ./your-repo
```
No repo handy (README.md:37-39):
```bash
swarmvault demo
```
Most useful commands after first compile (README.md:43-49):
```bash
swarmvault next
swarmvault query "What are the key concepts?"
swarmvault graph serve
swarmvault doctor
swarmvault candidate list
```
`swarmvault next` is read-only and reports whether to initialize, ingest, compile, query, review, or refresh (README.md:51).
## What you get on disk
(README.md:57-63):
- `raw/` - immutable copies of ingested material
- `wiki/` - generated markdown pages, saved outputs, graph reports, context packs, and task notes
- `state/graph.json` - the machine-readable knowledge graph
- `state/retrieval/` - local search index
- `wiki/graph/share-card.md`, `wiki/graph/share-card.svg`, and `wiki/graph/share-kit/` - copyable and visual first-run summaries
## Three-layer architecture
Follows the Karpathy pattern (README.md:69-73):
1. **Raw sources** (`raw/`) — curated collection of source documents. Books, articles, papers, transcripts, code, images, datasets. Immutable: SwarmVault reads but never modifies them.
2. **The wiki** (`wiki/`) — LLM-generated and human-authored markdown. Source summaries, entity pages, concept pages, cross-references, dashboards, outputs. The persistent, compounding artifact.
3. **The schema** (`swarmvault.schema.md`) — defines wiki structure, conventions, and domain priorities. Co-evolved by user and LLM over time.
Framed as in the tradition of Vannevar Bush's Memex (1945), treating connections between sources as valuable as the sources, with the LLM handling maintenance (README.md:75).
Supported inputs include books, articles, notes, transcripts, mail exports, calendars, datasets, slide decks, screenshots, URLs, and code, for personal knowledge management, research deep-dives, book companions, code documentation, business intelligence, or any accumulating-knowledge domain (README.md:77). A standalone schema template at `templates/llm-wiki-schema.md` works with zero install and any LLM agent before graduating to the full CLI (README.md:79).
## Why SwarmVault
Production-grade version of Karpathy's LLM Wiki gist (README.md:86):
- Hallucinations: edges tagged `extracted`/`inferred`/`ambiguous`, contradiction detection, `compile --approve` approval bundles, `wiki/candidates/` staging, `lint --conflicts` audits (README.md:88).
- Scale past 100 pages: hybrid SQLite FTS plus semantic embeddings, `compile --max-tokens` trimming, `graph query`/`graph path`/`graph explain`/`graph callers` traversal (README.md:90).
- Teams: `--commit` git workflows, watch mode with git hooks, scheduled automation, MCP server, direct-rule plus extended skill-bundle agent integrations (README.md:92).
- No API keys: built-in `heuristic` provider fully offline; sharper extraction via free local LLM through Ollama; cloud providers optional (README.md:94).
## From gist to production
Verbatim comparison table (README.md:101-121):
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
## Install
Desktop app bundles its own runtime, no Node.js required, via Download Desktop App page and `swarmvault-desktop` GitHub Releases (README.md:126-130). CLI path (README.md:136-154):
```bash
npm install -g @swarmvaultai/cli
swarmvault --version
npm install -g @swarmvaultai/cli@latest
```
## Fast path and vault layout
Run from an empty or scratch folder where vault artifacts should live (README.md:161-168):
```bash
mkdir my-vault
cd my-vault
swarmvault quickstart ../your-repo
swarmvault next
```
Same work as `swarmvault scan`: initialize, ingest local file/directory or public GitHub repo, compile wiki and graph, write share artifacts, open graph viewer unless `--no-serve` or `--no-viz` passed (README.md:170). Interactive runs show bounded ingest progress on stderr including the active file (README.md:170).
Resulting layout (README.md:172-180):
```text
my-vault/
├── swarmvault.schema.md       user-editable vault instructions
├── raw/                       immutable source files and localized assets
├── wiki/                      compiled wiki: sources, concepts, entities, code, outputs, graph
├── state/                     graph.json, retrieval/, embeddings, sessions, approvals
├── .obsidian/                 optional Obsidian workspace config
└── agent/                     generated agent-facing helpers
```
With `SWARMVAULT_OUT=.swarmvault-out`, generated `raw/`, `wiki/`, `state/`, `agent/`, `inbox/` resolve under the output directory while `swarmvault.config.json` and `swarmvault.schema.md` stay in the project root (README.md:182).
## Main loop
Step-by-step once the fast path makes sense (README.md:190-199):
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
Registered, refreshable sources use `swarmvault source add`, `swarmvault source list`, `swarmvault source reload --all`, and `swarmvault source session transcript-or-session-id`; public GitHub repos use `swarmvault clone https://github.com/owner/repo --no-viz` and `swarmvault source add https://github.com/owner/repo --branch main --checkout-dir .swarmvault-checkouts/repo` (README.md:201).
## Common next commands
Verbatim command table (README.md:207-224):
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
Note: the chunk truncates mid-sentence at `swarmvault init --lite` details (chunk line 226: "Normal `init`, `quickstart`, `scan`, and `clone` also avoid writing agent rule files by default; run `swarmvault…"), so lite-mode contents and the remainder of that command are not covered here.
**Covers:** README.md (Try It, three-layer architecture, why SwarmVault, gist-to-production table, install, fast path, main loop, common commands); chunk macro-components stub lists `top-level-files/` (chunk lines 228-231) but its file list was cut, so no claims about it are made here.
