---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: xoai/sage-wiki
### Q1. What is sage-wiki and who are its two audiences?
> [!tip]- Answer
> sage-wiki is a graph memory and knowledge base where an LLM compiler turns dropped-in documents into an interlinked markdown wiki with a knowledge graph. Agents query it through 19 MCP tools plus generated skill files, while humans browse the same data as Obsidian-native markdown via a TUI and web UI. It ships as one Go binary scaling from personal vault to company knowledge graph. See [[wiki/01-overview|Overview]].
### Q2. How does the evidenced knowledge graph keep relational answers trustworthy?
> [!tip]- Answer
> Opt-in graph passes add typed entities, provenance-bearing relations, resolved aliases, and per-fact citations. Relational answers via `wiki_graph_query` are grounded only in serialized graph edges, each citation carrying source document and confidence. Query outputs are quarantined until verified, and every evidenced relation records which document asserted it. See [[wiki/01-overview|Overview]].
### Q3. How do the compile pipeline and retrieval fusion work together?
> [!tip]- Answer
> The compile pipeline ingests papers, notes, code, and email — summarizing, extracting concepts, and writing interconnected articles so every new source enriches existing articles. Retrieval fuses lexical (BM25), vector, and graph-proximity channels at `search.hybrid_weight_graph`, with hybrid chunk search plus LLM query expansion, re-ranking, and graph-aware context assembly. Tiered compilation scales this to 100K+ documents. See [[wiki/01-overview|Overview]].
### Q4. What are the three deployment tiers and how do they differ?
> [!tip]- Answer
> Personal overlays an existing Obsidian vault with local models and opt-in `ontology.triples` + `ontology.resolve` for the evidenced graph. Team shares one wiki via git or a self-hosted server, reviewing entity-resolution proposals and output trust together with hub federation. Company adds PostgreSQL/pgvector storage, metrics, auth-fronted serving, and tiered compilation for large vaults. See [[wiki/01-overview|Overview]].
### Q5. What do the top-level hygiene files (`.dockerignore`, `.gitattributes`, `.gitignore`) exclude and enforce?
> [!tip]- Answer
> `.dockerignore` keeps the Docker build context lean by excluding VCS, state, docs, and build outputs while re-including `go.md`. `.gitattributes` forces consistent line endings with `* text=auto eol=lf`. `.gitignore` excludes agent configs, Sage state directories, built binaries, and benchmark/Python/Node artifacts. See [[wiki/02-top-level-files|Top-Level Files]].
### Q6. What does the lint gate pin and what does `TestIntegrationM1` verify?
> [!tip]- Answer
> `.golangci.yml` pins `version: "2"` for the go1.26 toolchain with standard linters plus `bodyclose`, `misspell`, `rowserrcheck`, and `sqlclosecheck`, relaxing `errcheck`/`bodyclose` for `_test.go` files. `TestIntegrationM1` runs end to end on a temp dir covering `init → populate → search → ontology query → status → MCP read tools`, asserting greenfield layout, BM25/tag-filtered search, article read, ontology traversal, status, and vector counts. See [[wiki/02-top-level-files|Top-Level Files]].
### Q7. Should a small team adopt sage-wiki as its shared knowledge base?
> [!tip]- Answer
> Yes, if the team already keeps notes in markdown and wants agents and humans reading the same evidenced store, since git-synced sharing, review-gated entity resolution, and per-fact citations fit a small collaborative vault. Prefer a simpler wiki or plain vector search if the team will not run the compile pipeline or review trust proposals, because the graph value depends on that upkeep. Start on the Team tier and add PostgreSQL only when scale demands it. See [[wiki/01-overview|Overview]].
