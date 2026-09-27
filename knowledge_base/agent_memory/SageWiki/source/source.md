# xoai/sage-wiki
> PDF location (no local source.pdf): https://github.com/xoai/sage-wiki
Source: https://github.com/xoai/sage-wiki
Kind: repo
Fetched: 2026-09-26T13:42:30.545686+00:00
Tool: git-clone
Research-Target: /Users/sergii/.ai/knowledge/research_topics/agent_memory/research/AgentBrain
Topic: agent_memory

# xoai/sage-wiki

Commit: 165100aaa93d94cb361f013d5ef471a7f9b15728

## README

**English** | [中文](docs/translations/README_zh.md) | [日本語](docs/translations/README_ja.md) | [한국어](docs/translations/README_ko.md) | [Tiếng Việt](docs/translations/README_vi.md) | [Français](docs/translations/README_fr.md) | [Русский](docs/translations/README_ru.md)



# sage-wiki

**sage-wiki** is a graph memory and knowledge base that AI agents and humans build and query together. Drop in documents; an LLM compiler turns them into an interlinked wiki with a knowledge graph — agents query it through MCP, humans browse it as plain markdown. Enable the opt-in graph passes and it becomes an *evidenced* graph: typed entities, provenance-bearing relations, resolved aliases, and per-fact citations on answers. One Go binary scales it from a personal vault to a team hub to a company knowledge graph.

**→ Get started: [Install](#install) · [Quickstart](#quickstart)**

Grown from [Andrej Karpathy's idea](https://x.com/karpathy/status/2039805659525644595) of an LLM-compiled personal knowledge base, built with the [Sage Framework](https://github.com/xoai/sage). Some lessons learned along the way [here](https://x.com/xoai/status/2040936964799795503).

- **Graph memory with citations.** Ask relational questions through `wiki_graph_query` — answers are grounded only in serialized graph edges; with the evidenced graph enabled, each citation carries its source document and confidence.
- **Built for agents and humans.** 19 MCP tools plus generated skill files teach agents when to search, capture, and compile; humans get Obsidian-native markdown, a TUI, and a web UI over the same data.
- **Trust and provenance.** Query outputs quarantine until verified; every evidenced relation records which document asserted it.
- **Your sources in, a wiki out.** The compile pipeline reads papers, notes, code, and email; summarizes; extracts concepts; and writes interconnected articles — the ingestion layer for everything above. Every new source enriches existing articles; the wiki compounds as it grows.
- **Ask your wiki questions.** Hybrid chunk-level search with LLM query expansion, re-ranking, and graph-aware context assembly returns cited answers.
- **Scales to 100K+ documents.** Tiered compilation indexes everything fast and spends LLM budget only where it matters.

https://github.com/user-attachments/assets/c35ee202-e9df-4ccd-b520-8f057163ff26

_Dots on the outer boundary represent summaries of all documents in the knowledge base, while dots in the inner circle represent concepts extracted from the knowledge base, with links showing how those concepts connect to one another._



## From personal vault to company knowledge graph

- **Personal** — overlay an existing Obsidian vault (`init --vault`), run on [local models](docs/guides/local-models.md) for zero cost, and opt into the graph passes (`ontology.triples` + `ontology.resolve`) when you want the evidenced graph.
- **Team** — share one wiki via git or a [self-hosted server](docs/guides/self-hosted-server.md), review entity-resolution proposals and [output trust](docs/guides/output-trust.md) together, and federate multiple wikis with the hub. See [Team Setup](docs/guides/team-setup.md).
- **Company** — move storage to [PostgreSQL/pgvector](docs/guides/storage-backends.md), turn on [metrics](docs/guides/metrics.md), front the server with auth, and scale ingestion with [tiered compilation](docs/guides/large-vault-performance.md).



## Knowledge graph & graph memory

![sage-wiki graph engine](assets/sage-wiki-graph-engine.png)

Vector search retrieves passages that *look like* the query. A graph also
records **how things relate**, so a question needing two or three hops is
answered by traversal instead of hoping one chunk happens to contain the whole
chain. sage-wiki builds that graph as a compile output — not a second database
you have to keep in sync.

- **Entities and typed relations.** Each compile extracts entities (concepts,
  sources, artifacts) and links them with typed relations. The relation
  vocabulary is yours to define — see
  [configurable relations](docs/guides/configurable-relations.md).
- **Evidenced edges.** A relation can carry `evidence` (the span that supports
  it), `confidence` (0–1), and `source_doc`, so a conclusion traces to the
  sentence that justified the edge rather than to a whole document.
- **Triples.** An optional structured-output pass extracts
  subject → relation → object directly. Opt-in (`ontology.triples`): it adds
  one LLM call per document, and defaults never spend your key without asking.
- **Entity resolution.** "K8s" and "Kubernetes" become one node. Proposals are
  review-gated by default rather than silently merged.
- **Concept curation.** One opt-in pass (`dedup_strategy: "llm"`) sees the whole
  proposed concept set at once — the only stage with global view — and judges
  keep / fold / drop per concept. Semantic restatements fold (aliases and
  sources merge), enumerated entities never fold (`mw-3` is not `mw-2`, at any
  similarity), and drops stay logged proposals until `llm_dedup.allow_drop`
  opts in. The judgment prompt is workspace-overridable
  (`prompts/curate-concepts.md`).

**The graph is a retrieval channel, not a side view.** Every search fuses three
channels — lexical (BM25), vector, and graph proximity: query terms seed
entities, a bounded traversal ranks their neighborhood, and the three fuse at
`search.hybrid_weight_graph`. An empty ontology costs nothing and leaves
results byte-identical, so the graph earns its place incrementally.

Query it directly, or let an agent do it over MCP:

```bash
sage-wiki ontology query --entity kubernetes --depth 3 --direction both
sage-wiki provenance "service mesh"    # which sources produced this concept
```

Edges are bi-temporal: contradicting a fact invalidates the old edge instead
of colliding, default answers are contradiction-free, and `as_of` queries
answer "what did we believe in January?" Ambiguous contradictions still
surface through [output trust](docs/guides/output-trust.md) review. For
corpus-wide questions ("main themes across everything?"), opt-in community
detection (`ontology.communities.enabled`) generates cached community
summaries and answers via `wiki_graph_query` `mode: "global"`. Depth
and mechanics: [graph memory](docs/guides/graph-memory.md).



## Guides

| Guide | Description |
|-------|-------------|
| [Agent Memory Layer](docs/guides/agent-memory-layer.md) | MCP setup, skill files, capture workflows, read-capture-evolve loop |
| [HTTP API](docs/guides/http-api.md) | The /v1 REST surface: auth, error model, idempotency, async jobs |
| [Graph Memory](docs/guides/graph-memory.md) | Evidenced relations, triple extraction, entity resolution, graph QA |
| [Configuration](docs/guides/configuration.md) | The full annotated config.yaml, multi-provider setup, serve worker |
| [Team Setup](docs/guides/team-setup.md) | Git-synced, shared server, and hub federation deployment patterns |
| [Search Quality](docs/guides/search-quality.md) | Chunk indexing, query expansion, re-ranking, graph expansion, ANN |
| [Large Vault Performance](docs/guides/large-vault-performance.md) | Tiered compilation, backpressure, code parsers, 100K+ scaling |
| [Output Trust](docs/guides/output-trust.md) | Grounding verification, consensus, promotion/demotion lifecycle |
| [Subscription Auth](docs/guides/subscription-auth.md) | OAuth login, token import, credential management |
| [Self-Hosted Server](docs/guides/self-hosted-server.md) | Docker Compose, Syncthing, reverse proxy, VPS deployment |
| [Storage Backends](docs/guides/storage-backends.md) | SQLite vs PostgreSQL/pgvector setup, switching, pool sizing |
| [Configurable Relations](docs/guides/configurable-relations.md) | Custom ontology types, multilingual synonyms, type restrictions |
| [Customizing Prompts](docs/guides/customizing-prompts.md) | Prompt scaffolding, per-type overrides, custom frontmatter fields |
| [Local Models](docs/guides/local-models.md) | Ollama setup, GPU/CPU routing, per-pass model config |
| [Metrics](docs/guides/metrics.md) | Log snapshots, /metrics endpoint, cardinality controls |
| [Webhooks](docs/webhooks.md) | HMAC-signed event delivery, signature recipe, retry/dead-letter |
| [Security](docs/security.md) | Threat model, the limits table, prompt boundary, residual risks |
| [Contribution Packs](CONTRIBUTING.md) | Creating packs, parser authoring, registry submission |



## Install

```bash


# CLI only (no web UI)
go install github.com/xoai/sage-wiki/cmd/sage-wiki@latest



# With web UI (requires Node.js for building frontend assets)
git clone https://github.com/xoai/sage-wiki.git && cd sage-wiki
cd web && npm install && npm run build && cd ..
go build -tags webui -o sage-wiki ./cmd/sage-wiki/
```



### Greenfield (new project)

```bash
sage-wiki init my-wiki && cd my-wiki


# Add sources to raw/
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

Every `config.yaml` key, annotated line by line: [Configuration](docs/guides/configuration.md).

**Project layout** (what `init` creates — selected entries, illustrative not exhaustive):

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



### Vault Overlay (existing Obsidian vault)

```bash
cd ~/Documents/MyVault
sage-wiki init --vault


# Edit config.yaml to set source/ignore folders, add api key, pick LLMs
sage-wiki compile --watch
```

Prefer containers? Prebuilt multi-arch Docker images and compose files are
covered in the [self-hosted server guide](docs/guides/self-hosted-server.md).



## Supported Source Formats

| Format      | Extensions                              | What gets extracted                                         |
| ----------- | --------------------------------------- | ----------------------------------------------------------- |
| Markdown    | `.md`                                   | Body text with frontmatter parsed separately                |
| PDF         | `.pdf`                                  | Full text via pure-Go extraction                            |
| Word        | `.docx`                                 | Document text from XML                                      |
| Excel       | `.xlsx`                                 | Cell values and sheet data                                  |
| PowerPoint  | `.pptx`                                 | Slide text content                                          |
| CSV         | `.csv`                                  | Headers + rows (up to 1000 rows)                            |
| E

... (truncated, 30811 more characters)

## go.mod

```
module github.com/xoai/sage-wiki

go 1.26
toolchain go1.26.6

require (
	github.com/charmbracelet/bubbles v1.0.0
	github.com/charmbracelet/bubbletea v1.3.10
	github.com/charmbracelet/glamour v1.0.0
	github.com/charmbracelet/lipgloss v1.1.1-0.20250404203927-76690c660834
	github.com/fsnotify/fsnotify v1.9.0
	github.com/jackc/pgx/v5 v5.10.0
	github.com/klauspost/compress v1.19.1
	github.com/ledongthuc/pdf v0.0.0-20250511090121-5959a4027728
	github.com/mark3labs/mcp-go v0.46.0
	github.com/pgvector/pgvector-go v0.4.0
	github.com/pgvector/pgvector-go/pgx v0.4.0
	github.com/prometheus/client_model v0.6.2
	github.com/prometheus/common v0.70.1
	github.com/shopspring/decimal v1.4.0
	github.com/spf13/cobra v1.10.2
	github.com/spf13/pflag v1.0.9
	github.com/viterin/vek v0.4.2
	github.com/zalando/go-keyring v0.2.8
	golang.org/x/sys v0.47.0
	golang.org/x/text v0.40.0
	gopkg.in/yaml.v3 v3.0.1
	modernc.org/sqlite v1.48.1
)

require (
	github.com/alecthomas/chroma/v2 v2.20.0 // indirect
	github.com/atotto/clipboard v0.1.4 // indirect
	github.com/aymanbagabas/go-osc52/v2 v2.0.1 // indirect
	github.com/aymerick/douceur v0.2.0 // indirect
	github.com/charmbracelet/colorprofile v0.4.1 // indirect
	github.com/charmbracelet/x/ansi v0.11.6 // indirect
	github.com/charmbracelet/x/cellbuf v0.0.15 // indirect
	github.com/charmbracelet/x/exp/slice v0.0.0-20250327172914-2fdc97757edf // indirect
	github.com/charmbracelet/x/term v0.2.2 // indirect
	github.com/chewxy/math32 v1.10.1 // indirect
	github.com/clipperhouse/displaywidth v0.9.0 // indirect
	github.com/clipperhouse/stringish v0.1.1 // indirect
	github.com/clipperhouse/uax29/v2 v2.5.0 // indirect
	github.com/danieljoos/wincred v1.2.3 // indirect
	github.com/dlclark/regexp2 v1.11.5 // indirect
	github.com/dustin/go-humanize v1.0.1 // indirect
	github.com/erikgeiser/coninput v0.0.0-20211004153227-1c3628e74d0f // indirect
	github.com/godbus/dbus/v5 v5.2.2 // indirect
	github.com/google/jsonschema-go v0.4.2 // indirect
	github.com/google/uuid v1.6.0 // indirect
	github.com/gorilla/css v1.0.1 // indirect
	github.com/inconshreveable/mousetrap v1.1.0 // indirect
	github.com/jackc/pgpassfile v1.0.0 // indirect
	github.com/jackc/pgservicefile v0.0.0-20240606120523-5a60cdf6a761 // indirect
	github.com/jackc/puddle/v2 v2.2.2 // indirect
	github.com/lucasb-eyer/go-colorful v1.3.0 // indirect
	github.com/mattn/go-isatty v0.0.20 // indirect
	github.com/mattn/go-localereader v0.0.1 // indirect
	github.com/mattn/go-runewidth v0.0.19 // indirect
	github.com/microcosm-cc/bluemonday v1.0.27 // indirect
	github.com/muesli/ansi v0.0.0-20230316100256-276c6243b2f6 // indirect
	github.com/muesli/cancelreader v0.2.2 // indirect
	github.com/muesli/reflow v0.3.0 // indirect
	github.com/muesli/termenv v0.16.0 // indirect
	github.com/munnerz/goautoneg v0.0.0-20191010083416-a7dc8b61c822 // indirect
	github.com/ncruces/go-strftime v1.0.0 // indirect
	github.com/remyoudompheng/bigfft v0.0.0-20230129092748-24d4a6f8daec // indirect
	github.com/rivo/uniseg v0.4.7 // indirect
	github.com/spf13/cast v1.7.1 // indirect
	github.com/viterin/partial v1.1.0 // indirect
	github.com/x448/float16 v0.8.4 // indirect
	github.com/xo/terminfo v0.0.0-20220910002029-abceb7e1c41e // indirect
	github.com/yosida95/uritemplate/v3 v3.0.2 // indirect
	github.com/yuin/goldmark v1.7.17 // indirect
	github.com/yuin/goldmark-emoji v1.0.6 // indirect
	golang.org/x/exp v0.0.0-20251023183803-a4bb9ffd2546 // indirect
	golang.org/x/net v0.57.0 // indirect
	golang.org/x/sync v0.22.0 // indirect
	golang.org/x/term v0.45.0 // indirect
	google.golang.org/protobuf v1.36.11 // indirect
	modernc.org/libc v1.70.0 // indirect
	modernc.org/mathutil v1.7.1 // indirect
	modernc.org/memory v1.11.0 // indirect
)

```

## Top-level layout

- .dockerignore (~12 lines)
- .gitattributes (~1 lines)
- .github/ (dir, 12 files, ~2138 lines)
- .gitignore (~40 lines)
- .golangci.yml (~32 lines)
- api/ (dir, 1 files, ~692 lines)
- assets/ (dir, 5 files, ~0 lines)
- CHANGELOG.md (~1901 lines)
- ci/ (dir, 7 files, ~1190 lines)
- clients/ (dir, 29 files, ~3384 lines)
- cmd/ (dir, 49 files, ~10704 lines)
- CONTRIBUTING.md (~322 lines)
- Dockerfile (~38 lines)
- docs/ (dir, 27 files, ~8704 lines)
- eval/ (dir, 48 files, ~82164 lines)
- examples/ (dir, 8 files, ~665 lines)
- go.mod (~85 lines)
- go.sum (~224 lines)
- integration_test.go (~282 lines)
- internal/ (dir, 747 files, ~147707 lines)
- LICENSE (~21 lines)
- Makefile (~176 lines)
- pkg/ (dir, 46 files, ~8416 lines)
- README.md (~775 lines)
- scripts/ (dir, 11 files, ~1101 lines)
- skills/ (dir, 2 files, ~414 lines)
- testdata/ (dir, 230 files, ~12062 lines)
- tests/ (dir, 2 files, ~243 lines)
- tools/ (dir, 21 files, ~5506 lines)
- web/ (dir, 28 files, ~4431 lines)

