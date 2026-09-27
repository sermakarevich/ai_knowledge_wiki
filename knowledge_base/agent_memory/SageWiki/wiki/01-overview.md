> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** sage-wiki is a graph memory and knowledge base where an LLM compiler turns dropped-in documents into an interlinked markdown wiki with a knowledge graph that agents query via MCP and humans browse directly.
## Key points
- sage-wiki compiles dropped-in documents into an interlinked wiki with a knowledge graph, queryable by agents through MCP and browsable by humans as plain markdown (README.md:13).
- With opt-in graph passes it becomes an evidenced graph with typed entities, provenance-bearing relations, resolved aliases, and per-fact citations on answers (README.md:13).
- It ships as one Go binary scaling from personal vault to team hub to company knowledge graph (README.md:13).
- Relational answers via `wiki_graph_query` are grounded only in serialized graph edges, each citation carrying source document and confidence when the evidenced graph is on (README.md:19).
- Agents get 19 MCP tools plus generated skill files (search/capture/compile), while humans get Obsidian-native markdown, a TUI, and a web UI over the same data (README.md:20).
- Query outputs are quarantined until verified, and every evidenced relation records which document asserted it (README.md:21).
- The compile pipeline ingests papers, notes, code, and email — summarizing, extracting concepts, writing interconnected articles — so every new source enriches existing articles (README.md:22).
- Retrieval fuses lexical (BM25), vector, and graph-proximity channels at `search.hybrid_weight_graph`, with hybrid chunk search plus LLM query expansion, re-ranking, and graph-aware context assembly (README.md:23, README.md:70).
---
## Purpose and primitives
`sage-wiki` is "a graph memory and knowledge base that AI agents and humans build and query together" (README.md:13). Grown from Andrej Karpathy's idea of an LLM-compiled personal knowledge base and built with the Sage Framework (README.md:17). Feature surface (README.md:19-24):
- Graph memory with citations (`wiki_graph_query`)
- 19 MCP tools + skill files for agents; Obsidian markdown + TUI + web UI for humans
- Trust/provenance quarantine for query outputs
- Compile pipeline: sources in, wiki out
- Cited hybrid-search Q&A
- Tiered compilation scaling to 100K+ documents
## Deployment tiers
From personal vault to company knowledge graph (README.md:32-36):
- **Personal** — overlay an existing Obsidian vault (`init --vault`), run on local models (`docs/guides/local-models.md`), opt into `ontology.triples` + `ontology.resolve` for the evidenced graph.
- **Team** — share one wiki via git or self-hosted server (`docs/guides/self-hosted-server.md`), review entity-resolution proposals and output trust (`docs/guides/output-trust.md`) together, federate with the hub (`docs/guides/team-setup.md`).
- **Company** — PostgreSQL/pgvector storage (`docs/guides/storage-backends.md`), metrics (`docs/guides/metrics.md`), auth-fronted server, tiered compilation (`docs/guides/large-vault-performance.md`).
## Knowledge graph and graph memory
Vector search retrieves look-alike passages; the graph records how things relate so multi-hop questions are answered by traversal, built as a compile output rather than a synced second database (README.md:44-48).
- **Entities and typed relations** — per-compile extraction of concepts, sources, artifacts with user-definable relation vocabulary (`docs/guides/configurable-relations.md`) (README.md:50-53).
- **Evidenced edges** — relations carry `evidence` (supporting span), `confidence` (0–1), `source_doc` (README.md:54-56).
- **Triples** — optional structured-output pass, subject → relation → object, opt-in via `ontology.triples`, one extra LLM call per document (README.md:57-59).
- **Entity resolution** — e.g. "K8s" and "Kubernetes" merge into one node; proposals are review-gated, not silently merged (README.md:60-61).
- **Concept curation** — one opt-in pass (`dedup_strategy: "llm"`), the only stage with global view, judging keep/fold/drop; semantic restatements fold (aliases+sources merge), enumerated entities never fold (`mw-3` is not `mw-2`), drops stay logged proposals until `llm_dedup.allow_drop`; prompt overridable at `prompts/curate-concepts.md` (README.md:62-68).
- **Retrieval fusion** — query terms seed entities, bounded traversal ranks the neighborhood, three channels fuse at `search.hybrid_weight_graph`; empty ontology leaves results byte-identical (README.md:70-74).
- **Direct queries:**
```bash
sage-wiki ontology query --entity kubernetes --depth 3 --direction both
sage-wiki provenance "service mesh"    # which sources produced this concept
```
- **Bi-temporal edges** — contradicting a fact invalidates the old edge; default answers are contradiction-free; `as_of` queries answer "what did we believe in January?"; ambiguous contradictions surface via output-trust review (README.md:83-86). Corpus-wide questions use opt-in community detection (`ontology.communities.enabled`) with cached community summaries answered via `wiki_graph_query` `mode: "global"` (README.md:86-90).
## Guides index
| Guide | Description |
|-------|-------------|
| Agent Memory Layer (`docs/guides/agent-memory-layer.md`) | MCP setup, skill files, capture workflows, read-capture-evolve loop |
| HTTP API (`docs/guides/http-api.md`) | The /v1 REST surface: auth, error model, idempotency, async jobs |
| Graph Memory (`docs/guides/graph-memory.md`) | Evidenced relations, triple extraction, entity resolution, graph QA |
| Configuration (`docs/guides/configuration.md`) | Full annotated config.yaml, multi-provider setup, serve worker |
| Team Setup (`docs/guides/team-setup.md`) | Git-synced, shared server, hub federation patterns |
| Search Quality (`docs/guides/search-quality.md`) | Chunk indexing, query expansion, re-ranking, graph expansion, ANN |
| Large Vault Performance (`docs/guides/large-vault-performance.md`) | Tiered compilation, backpressure, code parsers, 100K+ scaling |
| Output Trust (`docs/guides/output-trust.md`) | Grounding verification, consensus, promotion/demotion lifecycle |
| Subscription Auth (`docs/guides/subscription-auth.md`) | OAuth login, token import, credential management |
| Self-Hosted Server (`docs/guides/self-hosted-server.md`) | Docker Compose, Syncthing, reverse proxy, VPS deployment |
| Storage Backends (`docs/guides/storage-backends.md`) | SQLite vs PostgreSQL/pgvector setup, switching, pool sizing |
| Configurable Relations (`docs/guides/configurable-relations.md`) | Custom ontology types, multilingual synonyms, type restrictions |
| Customizing Prompts (`docs/guides/customizing-prompts.md`) | Prompt scaffolding, per-type overrides, custom frontmatter fields |
| Local Models (`docs/guides/local-models.md`) | Ollama setup, GPU/CPU routing, per-pass model config |
| Metrics (`docs/guides/metrics.md`) | Log snapshots, /metrics endpoint, cardinality controls |
| Webhooks (`docs/webhooks.md`) | HMAC-signed event delivery, signature recipe, retry/dead-letter |
| Security (`docs/security.md`) | Threat model, limits table, prompt boundary, residual risks |
| Contribution Packs (`CONTRIBUTING.md`) | Creating packs, parser authoring, registry submission |
(Table grounded in README.md:96-116.)
## Install and quickstart
```bash
# CLI only (no web UI)
go install github.com/xoai/sage-wiki/cmd/sage-wiki@latest

# With web UI (requires Node.js for building frontend assets)
git clone https://github.com/xoai/sage-wiki.git && cd sage-wiki
cd web && npm install && npm run build && cd ..
go build -tags webui -o sage-wiki ./cmd/sage-wiki/
```
(README.md:121-133.)
Greenfield (README.md:137-157):
```bash
sage-wiki init my-wiki && cd my-wiki
cp ~/papers/*.pdf raw/
# Edit config.yaml to add api key, and pick LLMs
sage-wiki compile                                  # first compile
sage-wiki compile                                  # second: zero LLM calls — unchanged docs are skipped
sage-wiki compile --explain raw/paper.pdf          # why a doc compiles or skips
sage-wiki compile --force                          # recompile everything regardless
sage-wiki search "attention mechanism"             # hybrid search
sage-wiki query "How does flash attention work?"   # cited Q&A
sage-wiki tui                                      # terminal dashboard
sage-wiki serve --ui                               # browser (webui build)
sage-wiki compile --watch                          # watch folder
```
Project layout from `init` (selected entries, illustrative not exhaustive) (README.md:161-176):
```
my-wiki/
├── config.yaml           # providers, models, compiler, search, ontology
├── raw/                  # drop sources here (articles, papers, code, images)
├── wiki/                 # compiled output — Obsidian-compatible markdown
│   ├── summaries/        # per-source LLM summaries
│   ├── concepts/         # concept articles (the knowledge graph)
│   ├── images/           # vision-captioned image descriptions
│   ├── outputs/          # filed query answers (trust.include_outputs: "true")
│   ├── under_review/     # filed answers awaiting trust review (default)
│   └── archive/          # pruned articles
├── .sage/wiki.db         # one SQLite file: FTS index, vectors, ontology, queue
└── .manifest.json        # source↔article mapping + compile state
```
Vault overlay (README.md:180-189):
```bash
cd ~/Documents/MyVault
sage-wiki init --vault
# Edit config.yaml to set source/ignore folders, add api key, pick LLMs
sage-wiki compile --watch
```
Containers (multi-arch Docker images, compose files) are covered in the self-hosted server guide (README.md:191-192).
## Supported source formats
Truncated in chunk: the table lists Markdown (`.md`), PDF (`.pdf`, pure-Go extraction), Word (`.docx`), Excel (`.xlsx`), PowerPoint (`.pptx`), CSV (`.csv`, headers + rows up to 1000 rows) (README.md:198-206), then cuts off mid-table at "`| E`" (README.md:207) — further formats not visible, contents not guessed.
## Truncation note
The chunk's Supported Source Formats table is cut off at line 207 (`| E`) and the `## Macro components` section lists only `top-level-files/` (README.md:208-210); no further module detail was present to summarize.
**Covers:** README.md (project purpose, graph memory, guides index, install/quickstart, source-format table truncated at CSV row); `docs/translations/` (README language links); `docs/guides/` + `docs/webhooks.md`, `docs/security.md`, `CONTRIBUTING.md` (as referenced, not their contents)
