# Technical Analysis: xoai/sage-wiki

**Repository:** https://github.com/xoai/sage-wiki
**Version analyzed:** unknown
**Date:** 2026-09-26
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

The problem space is shared human/agent knowledge management: documents (papers, notes, code, email) accumulate as disconnected files, vector search retrieves look-alike passages but not how things relate, and multi-hop questions require traversal rather than similarity (01-overview.md:11, 01-overview.md:28). The primary user is dual: AI agents and humans building and querying one knowledge base together (01-overview.md:15).

The repo addresses it with `sage-wiki`, a graph memory and knowledge base where an LLM compiler turns dropped-in documents into an interlinked markdown wiki plus a knowledge graph (01-overview.md:3). Sources dropped in `raw/` are summarized, concept-extracted, and written as interconnected articles so every new source enriches existing articles (01-overview.md:11). Agents query via 19 MCP tools plus generated skill files (search/capture/compile); humans browse the same data as Obsidian-native markdown, via a TUI and a web UI (01-overview.md:9). With opt-in graph passes it becomes an evidenced graph with typed entities, provenance-bearing relations, resolved aliases, and per-fact citations on answers (01-overview.md:6). It ships as one Go binary scaling from personal vault to team hub to company knowledge graph (01-overview.md:7). Deployment tiers are Personal (overlay an existing Obsidian vault via `init --vault`, local models), Team (git- or server-shared wiki with joint review of entity-resolution proposals and output trust, hub federation), and Company (PostgreSQL/pgvector storage, metrics, auth-fronted server, tiered compilation) (01-overview.md:23-26).

## 2. High-Level Architecture

```
raw/ sources ──► compile pipeline (summarize ► extract ► write articles) ──► wiki/ markdown
       │                                                                   │
       │                                                          ┌────────▼────────┐
       │                                                          │ .sage/wiki.db   │
       │                                                          │ FTS + vectors + │
       │                                                          │ ontology + queue│
       └──────────────────────────────────────────────────────────│ .manifest.json  │
                                                                  └────────┬────────┘
                                                        ┌──────────────────┼──────────────────┐
                                                        ▼                  ▼                  ▼
                                                  MCP server         TUI / web UI        CLI (search/query)
                                                  (19 tools)         (same data)         (hybrid + graph QA)
```

Data-flow narrative:

1. **Ingest.** Sources (Markdown, PDF via pure-Go extraction, `.docx`, `.xlsx`, `.pptx`, CSV up to 1000 rows; further formats truncated in source) are dropped in `raw/` (01-overview.md:77, 01-overview.md:112-113).
2. **Compile.** The LLM compiler summarizes each source, extracts concepts, and writes/updates interlinked articles under `wiki/` (`summaries/`, `concepts/`, `images/`, `outputs/`, `under_review/`, `archive/`) (01-overview.md:11, 01-overview.md:89-103).
3. **Index.** Chunk index (BM25/FTS), vectors, and optional ontology (typed triples, resolved entities) are stored in one SQLite file `.sage/wiki.db`; source↔article mapping and compile state live in `.manifest.json`, enabling zero-LLM-call recompiles when docs are unchanged (01-overview.md:89-103, 01-overview.md:80).
4. **Retrieve.** Retrieval fuses lexical (BM25), vector, and graph-proximity channels at `search.hybrid_weight_graph`, with hybrid chunk search plus LLM query expansion, re-ranking, and graph-aware context assembly (01-overview.md:12).
5. **Serve/verify.** Agents query through the MCP server (19 tools) and humans through Obsidian/TUI/web UI/CLI; relational answers via `wiki_graph_query` are grounded only in serialized graph edges, outputs are quarantined until verified, and every evidenced relation records its asserting document (01-overview.md:8-10).

Persistent state lives in `.sage/wiki.db` (FTS index, vectors, ontology, queue) and `.manifest.json` (source↔article mapping + compile state); the compiled wiki itself is plain markdown under `wiki/` (01-overview.md:89-103). Company tier swaps SQLite for PostgreSQL/pgvector (01-overview.md:26).

## 3. The Evidenced Graph (Core Abstraction)

Representation: the graph is a compile output, not a synced second database (01-overview.md:28). Nodes are extracted concepts, sources, and artifacts; edges are user-definable typed relations carrying provenance (01-overview.md:29-30).

Named kinds/types with citations:

- **Entities and typed relations** — per-compile extraction with user-definable relation vocabulary (`docs/guides/configurable-relations.md`), e.g. test relations `implements`, `optimizes` (01-overview.md:29; 02-top-level-files.md:93).
- **Evidenced edges** — each relation carries `evidence` (supporting span), `confidence` (0–1), `source_doc` (01-overview.md:30).
- **Triples** — optional structured-output pass, subject → relation → object, opt-in via `ontology.triples`, one extra LLM call per document (01-overview.md:31).
- **Aliases / entity resolution** — e.g. "K8s" and "Kubernetes" merge into one node; proposals are review-gated, not silently merged (01-overview.md:32).
- **Concepts under curation** — one opt-in pass (`dedup_strategy: "llm"`), the only stage with global view, judging keep/fold/drop; semantic restatements fold (aliases+sources merge), enumerated entities never fold, drops stay logged proposals until `llm_dedup.allow_drop`; prompt overridable at `prompts/curate-concepts.md` (01-overview.md:33).
- **Bi-temporal edges** — contradicting a fact invalidates the old edge; default answers are contradiction-free; `as_of` queries answer point-in-time belief (01-overview.md:40).
- **Communities** — opt-in corpus-wide community detection (`ontology.communities.enabled`) with cached summaries answered via `wiki_graph_query` `mode: "global"` (01-overview.md:40).

Key queries (verbatim):

```bash
sage-wiki ontology query --entity kubernetes --depth 3 --direction both
sage-wiki provenance "service mesh"    # which sources produced this concept
```
(01-overview.md:36-39.)

Retrieval fusion detail: query terms seed entities, bounded traversal ranks the neighborhood, three channels fuse at `search.hybrid_weight_graph`; an empty ontology leaves results byte-identical (01-overview.md:34).

## 4. LLM / External Service Integration

Providers: the wiki pages name no specific commercial provider; configuration holds providers/models/compiler settings and the quickstart instructs editing `config.yaml` to add an API key and pick LLMs (01-overview.md:77-78). The integration test defaults to `"gemini-2.5-flash"` (02-top-level-files.md:91). Local-model deployment via Ollama with GPU/CPU routing and per-pass model config is a documented guide (`docs/guides/local-models.md`) (01-overview.md:24, 01-overview.md:57).

Required vs optional calls: a second `compile` with unchanged docs performs zero LLM calls (docs are skipped) (01-overview.md:80). Optional extra-cost passes: triples (`ontology.triples`, one extra LLM call per document), entity resolution proposals, and concept curation (`dedup_strategy: "llm"`) (01-overview.md:31-33). Cited hybrid-search Q&A uses LLM query expansion and re-ranking (01-overview.md:12).

Env vars: no environment-variable names are stated in the available component pages. Config surface is `config.yaml` (providers, models, compiler, search, ontology) plus per-type prompt overrides (01-overview.md:89-103, 01-overview.md:33).

## 5. The Compile Pipeline (Main Pipeline)

Primary workflow: sources in, wiki out (01-overview.md:19).

1. `sage-wiki init my-wiki` — creates greenfield layout (`raw`, `wiki/concepts`, `.sage`, `config.yaml`, `.manifest.json`); asserted in `TestIntegrationM1` via `wiki.InitGreenfield(dir, "integration-test", "gemini-2.5-flash")` (02-top-level-files.md:91; 01-overview.md:76).
2. Drop sources in `raw/` (`cp ~/papers/*.pdf raw/`), or overlay an existing vault via `sage-wiki init --vault` with configured source/ignore folders (01-overview.md:77, 01-overview.md:104-110).
3. `sage-wiki compile` — summarizes each source, extracts concepts, writes interconnected articles; unchanged docs are skipped (zero LLM calls); `--explain <doc>` reports why a doc compiles or skips; `--force` recompiles everything; `--watch` compiles on folder change (01-overview.md:79-87).
4. Optional evidenced-graph passes — triples extraction (`ontology.triples`), entity-resolution proposal/review, concept curation (`dedup_strategy: "llm"`, prompt at `prompts/curate-concepts.md`), community detection (`ontology.communities.enabled`) (01-overview.md:31-33, 01-overview.md:40).
5. Query/serve — `sage-wiki search "<terms>"` (hybrid search), `sage-wiki query "<question>"` (cited Q&A), `sage-wiki ontology query --entity <name> --depth 3 --direction both`, `sage-wiki provenance "<concept>"`, `sage-wiki tui`, `sage-wiki serve --ui` (01-overview.md:83-86, 01-overview.md:36-39).

Per-function `file.py:line` detail for the pipeline implementation is not present in the available component pages (which cover only README-level behavior and top-level files); the end-to-end order `init → populate → search → ontology query → status → MCP read tools` is verified by `TestIntegrationM1` (`integration_test.go:267-269`) (02-top-level-files.md:10, 02-top-level-files.md:88-104).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `README.md` | cited to :210 | Project purpose, graph memory, guides index, install/quickstart, source formats, macro components (01-overview.md:3-116) |
| `integration_test.go` | :530 | End-to-end Milestone 1 test `TestIntegrationM1`: init, populate, BM25/tag search, article read, ontology query, status, vectors, lint, learn (02-top-level-files.md:88-104) |
| `go.sum` | 225 lines | Pinned transitive Go dependency hashes (partially visible; truncated in chunk) (02-top-level-files.md:9, 02-top-level-files.md:73-85) |
| `.golangci.yml` | :108 | Lint gate: golangci-lint v2, standard + bodyclose/misspell/rowserrcheck/sqlclosecheck, test-file relaxations (02-top-level-files.md:8, 02-top-level-files.md:50-71) |
| `.gitignore` | :71 | Excludes agent configs, Sage state dirs, built binaries, benchmark/Python/Node artifacts (02-top-level-files.md:7, 02-top-level-files.md:37-48) |
| `.dockerignore` | :20 | Lean Docker build context; excludes VCS, state, docs, outputs; re-includes `go.md` (02-top-level-files.md:5, 02-top-level-files.md:12-28) |
| `.gitattributes` | :26 | Line-ending normalization (`* text=auto eol=lf`) (02-top-level-files.md:6, 02-top-level-files.md:30-35) |
| `config.yaml` (generated) | n/a | Providers, models, compiler, search, ontology settings (01-overview.md:89-103) |
| `.manifest.json` (generated) | n/a | Source↔article mapping + compile state (01-overview.md:89-103) |
| `.sage/wiki.db` (generated) | n/a | SQLite file: FTS index, vectors, ontology, queue (01-overview.md:89-103) |
| `docs/guides/` (14 guides) | n/a | Agent memory, HTTP API, graph memory, configuration, team setup, search quality, large-vault performance, output trust, subscription auth, self-hosted server, storage backends, configurable relations, customizing prompts, local models (01-overview.md:42-61) |
| `docs/webhooks.md`, `docs/security.md`, `CONTRIBUTING.md` | n/a | Webhook delivery, threat model, contribution/pack authoring (01-overview.md:59-61) |

Structural-importance note: only top-level files plus README-level behavior are covered by the available component pages; internal package layout (`Macro components` beyond `top-level-files/`) was not present to summarize (01-overview.md:114-115).

## 7. Dependencies

| Package | Version constraint | Purpose |
|---|---|---|
| `github.com/charmbracelet/bubbletea` | `v1.3.10` | TUI framework (02-top-level-files.md:73-84) |
| `github.com/charmbracelet/lipgloss` | `v1.1.1-0.20250404203927-76690c660834` | TUI styling (02-top-level-files.md:73-84) |
| `github.com/mark3labs/mcp-go` | `v0.46.0` | MCP server/tools (02-top-level-files.md:73-84) |
| `github.com/jackc/pgx/v5` | `v5.10.0` | PostgreSQL driver, company-tier pgvector storage (02-top-level-files.md:73-84) |
| `github.com/pgvector/pgvector-go` | `v0.4.0` | pgvector client for vector storage (02-top-level-files.md:73-84) |
| `github.com/google/uuid` | `v1.6.0` | UUID generation (02-top-level-files.md:73-84) |
| `github.com/fsnotify/fsnotify` | `v1.9.0` | Filesystem watching (`compile --watch`) (02-top-level-files.md:73-84) |

Required-first note: the available pages do not distinguish direct vs transitive requirements; all rows above are pinned versions from `go.sum` (partial view, truncated mid-entry at `remyoudompheng/bigfft`; remaining pins not covered) (02-top-level-files.md:9, 02-top-level-files.md:84). Build tooling noted: Go 1.26 toolchain, golangci-lint v2, Node.js for web-UI asset builds (02-top-level-files.md:50-71; 01-overview.md:64-72).

## 8. CLI / Usage Surface

Entry points:

| Entry point | Form |
|---|---|
| CLI-only install | `go install github.com/xoai/sage-wiki/cmd/sage-wiki@latest` (01-overview.md:64-72) |
| Web-UI build | `git clone … && cd web && npm install && npm run build && cd .. && go build -tags webui -o sage-wiki ./cmd/sage-wiki/` (01-overview.md:64-72) |
| MCP server (in tests) | `mcppkg.NewServer(dir)` opens DB and registers tools (02-top-level-files.md:92) |

Commands:

| Command | Effect |
|---|---|
| `sage-wiki init my-wiki` | Greenfield wiki layout (01-overview.md:76) |
| `sage-wiki init --vault` | Overlay existing Obsidian vault (01-overview.md:104-110) |
| `sage-wiki compile` | Compile; second run is no-op on unchanged docs (01-overview.md:79-80) |
| `sage-wiki compile --explain <doc>` | Why a doc compiles or skips (01-overview.md:81) |
| `sage-wiki compile --force` | Recompile everything (01-overview.md:82) |
| `sage-wiki compile --watch` | Watch-folder compilation (01-overview.md:87) |
| `sage-wiki search "<terms>"` | Hybrid search (01-overview.md:83) |
| `sage-wiki query "<question>"` | Cited Q&A (01-overview.md:84) |
| `sage-wiki ontology query --entity <n> --depth <d> --direction both` | Graph neighborhood query (01-overview.md:36-39) |
| `sage-wiki provenance "<concept>"` | Sources behind a concept (01-overview.md:38) |
| `sage-wiki tui` | Terminal dashboard (01-overview.md:85) |
| `sage-wiki serve --ui` | Browser UI (webui build) (01-overview.md:86) |
| MCP tools `wiki_search`, `wiki_read`, `wiki_ontology_query`, `wiki_status`, `wiki_list`, `wiki_graph_query` | Agent read/graph interface; `wiki_graph_query` relational answers grounded in serialized edges, `mode: "global"` for community summaries (01-overview.md:8, 01-overview.md:40; 02-top-level-files.md:93-103) |

Env-var and config tables:

| Key | Scope | Notes (from available pages) |
|---|---|---|
| `config.yaml` providers/models | compile, query | API key + LLM selection edited by hand (01-overview.md:77-78) |
| `search.hybrid_weight_graph` | retrieval | Fusion weight across lexical/vector/graph channels (01-overview.md:12, 01-overview.md:34) |
| `ontology.triples` | compile | Opt-in triple pass (01-overview.md:31) |
| `ontology.resolve` | compile | Opt-in entity resolution (01-overview.md:24) |
| `ontology.communities.enabled` | compile/query | Opt-in community detection + `mode: "global"` QA (01-overview.md:40) |
| `dedup_strategy: "llm"` / `llm_dedup.allow_drop` | curation | Global keep/fold/drop pass; drop gating (01-overview.md:33) |
| `prompts/curate-concepts.md` | curation | Overridable curation prompt (01-overview.md:33) |
| `trust.include_outputs` | outputs | `"true"` files query answers under `wiki/outputs/` else `under_review/` (01-overview.md:89-103) |

No environment-variable names are stated in the available component pages.

## 9. Extensibility Points

- **Relation ontology** — define custom relation types, multilingual synonyms, and type restrictions via `docs/guides/configurable-relations.md` (01-overview.md:29, 01-overview.md:54).
- **Prompts** — scaffold and override per-type prompts and custom frontmatter fields via `docs/guides/customizing-prompts.md`; curation prompt overridable at `prompts/curate-concepts.md` (01-overview.md:33, 01-overview.md:56).
- **Contribution packs / parsers** — create packs and author source parsers, submit via registry per `CONTRIBUTING.md` (01-overview.md:61).
- **Storage backends** — SQLite vs PostgreSQL/pgvector setup, switching, pool sizing via `docs/guides/storage-backends.md` (01-overview.md:52).
- **Deployments** — self-hosted server (Docker Compose, Syncthing, reverse proxy, VPS), team hub federation, subscription auth, webhooks (HMAC-signed delivery with retry/dead-letter), metrics endpoint per respective guides (01-overview.md:42-61).
- **Lint/learn loop** — `linter.NewRunner().Run()` with `ValidRelations` and `linter.StoreLearning(...)` extension verified in `TestIntegrationM1` without API access (02-top-level-files.md:101-102).

## 10. Limitations and Gotchas

- **Truncated source coverage in available pages.** The Supported Source Formats table cuts off mid-table at `| E` (after CSV/1000-row row), and the `Macro components` section lists only `top-level-files/` — module internals beyond the top level are not covered (01-overview.md:112-115).
- **Truncated dependency manifest in available pages.** The `go.sum` excerpt ends mid-entry at `remyoudompheng/bigfft` with 8006 further characters unseen; the full transitive pin set cannot be enumerated from these pages (02-top-level-files.md:9, 02-top-level-files.md:84).
- **Evidenced-graph features are opt-in, not default.** Triples (`ontology.triples`), entity resolution (`ontology.resolve`), concept curation (`dedup_strategy: "llm"`), and communities (`ontology.communities.enabled`) each require explicit enablement (and extra LLM calls); an empty ontology leaves hybrid results byte-identical, so graph benefits are absent unless configured (01-overview.md:31-34, 01-overview.md:40).
- **Resolution and curation are gated, not automatic.** Entity merges are review-gated proposals rather than silent merges, enumerated entities never fold (`mw-3` is not `mw-2`), and drops stay logged proposals until `llm_dedup.allow_drop` — teams must budget review effort (joint review of resolution proposals and output trust is part of the Team tier) (01-overview.md:32-33, 01-overview.md:25).
- **Web UI requires a separate frontend build.** CLI-only install is one `go install`; browser UI needs Node.js, `npm install && npm run build` in `web/`, and a `-tags webui` Go build (01-overview.md:64-72).

## 11. How It Compares to Alternatives

The available component pages name no alternative projects, so no grounded comparison can be drawn from them alone. Positioning from stated design (without inventing competitors): sage-wiki is a single-Go-binary, markdown-native (Obsidian-compatible) compiler of documents into a wiki plus an opt-in evidenced knowledge graph with quarantined, citation-carrying answers, serving both MCP agents (19 tools + skill files) and human browsers (TUI/web UI) from the same data and persistent state (01-overview.md:3-12, 01-overview.md:89-103). Omitted: named-alternative comparison, which would require sources beyond the two component pages permitted for this summary.

## Appendix: Selected Code Snippets

1. Quickstart compile loop (`README.md` behavior via 01-overview.md:74-88):

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

2. Graph queries (01-overview.md:36-39):

```bash
sage-wiki ontology query --entity kubernetes --depth 3 --direction both
sage-wiki provenance "service mesh"    # which sources produced this concept
```

3. Lint gate (`.golangci.yml:77-108` via 02-top-level-files.md:50-71):

```yaml
version: "2"
linters:
  default: standard  # errcheck, govet, ineffassign, staticcheck, unused
  enable:
    - bodyclose      # HTTP response bodies must be closed
    - misspell       # common spelling mistakes in comments/strings
    - rowserrcheck   # sql.Rows.Err() checked after iteration
    - sqlclosecheck  # sql.Rows/Stmt closed
  exclusions:
    generated: lax
    presets:
      - std-error-handling
    rules:
      - path: _test\.go
        linters:
          - errcheck
          - bodyclose
```

4. Generated project layout (`README.md:161-176` via 01-overview.md:89-103):

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
