> [[index|Wiki]] | [[summary|Summary]]
# xoai/sage-wiki — Digest

## 1. [[wiki/01-overview|Overview]]
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

## 2. [[wiki/02-top-level-files|Top-Level Files]]
**In one sentence:** The top-level files define repo hygiene and build layout, the lint gate, pinned Go dependencies, and the end-to-end Milestone 1 verification test.
## Key points
- `.dockerignore` keeps the Docker build context lean by excluding VCS, state, docs, and build outputs while re-including `go.md` via `!go.md` (`.dockerignore:9-20`).
- `.gitattributes` forces consistent line endings with `* text=auto eol=lf` (`.gitattributes:26`).
- `.gitignore` excludes agent configs (`.claude/`, `.opencode/`, `CLAUDE.md`, `AGENTS.md`), Sage state (`.sage/`, `.sage-memory/`, `.sage-wiki/`, `sage/`), built binaries (`/sage-wiki`, `/civalidate`, `/ciobserve`, `/ciproof`, `/testsummary`, `bin/`), and benchmark/Python/Node artifacts (`.gitignore:32-71`).
- `.golangci.yml` pins `version: "2"` for the go1.26 toolchain, uses `default: standard` linters plus `bodyclose`, `misspell`, `rowserrcheck`, `sqlclosecheck`, and relaxes `errcheck`/`bodyclose` for `_test.go` files (`.golangci.yml:86-108`).
- `go.sum` (225 lines) pins the full transitive dependency set, including `charmbracelet/*`, `mark3labs/mcp-go v0.46.0`, `jackc/pgx/v5 v5.10.0`, and `pgvector/pgvector-go v0.4.0`; the chunk excerpt is truncated after `remyoudompheng/bigfft`, so the remaining pins are not covered here (`go.sum:114-243`).
- `integration_test.go` provides `TestIntegrationM1`, an end-to-end test for Milestone 1 covering `init → populate → search → ontology query → status → MCP read tools` (`integration_test.go:267-269`), asserting greenfield layout, BM25/tag-filtered search, article read, ontology traversal, status, and vector counts (`integration_test.go:273-443`).

## The system in five moves
1. Drop heterogeneous sources (papers, notes, code, email) into `raw/` and run the LLM compile pipeline, which summarizes, extracts concepts, and writes interlinked markdown articles.
2. Enrich the wiki into an opt-in evidenced knowledge graph with typed entities, provenance-bearing relations, resolved aliases, and per-fact citations.
3. Serve both audiences over the same data: agents via 19 MCP tools plus skill files with quarantined, grounded answers, and humans via Obsidian markdown, TUI, and web UI.
4. Fuse lexical, vector, and graph-proximity retrieval with query expansion, re-ranking, and graph-aware assembly, scaling one Go binary from personal vault to team hub to company graph.
5. Hold the repo together with lean build hygiene, a pinned golangci-lint v2 gate, and pinned Go dependencies, verified end to end by the Milestone 1 integration test.
