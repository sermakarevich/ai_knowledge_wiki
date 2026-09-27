[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-Level Files
**In one sentence:** The top-level files define repo hygiene and build layout, the lint gate, pinned Go dependencies, and the end-to-end Milestone 1 verification test.
## Key points
- `.dockerignore` keeps the Docker build context lean by excluding VCS, state, docs, and build outputs while re-including `go.md` via `!go.md` (`.dockerignore:9-20`).
- `.gitattributes` forces consistent line endings with `* text=auto eol=lf` (`.gitattributes:26`).
- `.gitignore` excludes agent configs (`.claude/`, `.opencode/`, `CLAUDE.md`, `AGENTS.md`), Sage state (`.sage/`, `.sage-memory/`, `.sage-wiki/`, `sage/`), built binaries (`/sage-wiki`, `/civalidate`, `/ciobserve`, `/ciproof`, `/testsummary`, `bin/`), and benchmark/Python/Node artifacts (`.gitignore:32-71`).
- `.golangci.yml` pins `version: "2"` for the go1.26 toolchain, uses `default: standard` linters plus `bodyclose`, `misspell`, `rowserrcheck`, `sqlclosecheck`, and relaxes `errcheck`/`bodyclose` for `_test.go` files (`.golangci.yml:86-108`).
- `go.sum` (225 lines) pins the full transitive dependency set, including `charmbracelet/*`, `mark3labs/mcp-go v0.46.0`, `jackc/pgx/v5 v5.10.0`, and `pgvector/pgvector-go v0.4.0`; the chunk excerpt is truncated after `remyoudompheng/bigfft`, so the remaining pins are not covered here (`go.sum:114-243`).
- `integration_test.go` provides `TestIntegrationM1`, an end-to-end test for Milestone 1 covering `init → populate → search → ontology query → status → MCP read tools` (`integration_test.go:267-269`), asserting greenfield layout, BM25/tag-filtered search, article read, ontology traversal, status, and vector counts (`integration_test.go:273-443`).
---
## Dockerignore
Build-context exclusions (`.dockerignore:9-20`):
```
.git
.github
.sage
.sage-memory
*.db
*.md
!go.md
docs
sage
web/node_modules
Dockerfile
.dockerignore
```
**Covers:** `.dockerignore`

## Gitattributes
Line-ending normalization (`.gitattributes:26`):
```
* text=auto eol=lf
```
**Covers:** `.gitattributes`

## Gitignore
Grouped exclusions (`.gitignore:32-71`):
| Group | Entries |
|---|---|
| Claude / agent | `.claude/`, `.opencode/`, `CLAUDE.md`, `AGENTS.md`, `.mcp.json`, `opencode.json` |
| Sage state | `.sage/`, `.sage-memory/`, `.sage-wiki/`, `sage/` |
| macOS | `.DS_Store` |
| Build | `/sage-wiki`, `/civalidate`, `/ciobserve`, `/ciproof`, `/testsummary`, `bin/` |
| Benchmark data | `eval/benchmarks/runs/` |
| Python | `__pycache__/`, `*.pyc` |
| Client/example | `node_modules/`, `.venv/`, `dist/`, `dist-test/`, `*.egg-info/`, `.pytest_cache/`, `examples/langgraph/__pycache__/`, `skillgen` |
**Covers:** `.gitignore`

## Golangci Lint Gate
Config (`.golangci.yml:77-108`): requires golangci-lint v2 because prebuilt v1 binaries refuse to analyze the go1.26 module and CI installs via `go install` with the same toolchain; CI gates only `--new-from-merge-base` issues so pre-existing findings are grandfathered.
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
**Covers:** `.golangci.yml`

## Pinned Dependencies
`go.sum` records 225 pinned module hashes (`go.sum:113-243`), including:
| Module | Pinned version (`go.sum`) |
|---|---|
| `github.com/charmbracelet/bubbletea` | `v1.3.10` |
| `github.com/charmbracelet/lipgloss` | `v1.1.1-0.20250404203927-76690c660834` |
| `github.com/mark3labs/mcp-go` | `v0.46.0` |
| `github.com/jackc/pgx/v5` | `v5.10.0` |
| `github.com/pgvector/pgvector-go` | `v0.4.0` |
| `github.com/google/uuid` | `v1.6.0` |
| `github.com/fsnotify/fsnotify` | `v1.9.0` |
Truncated in chunk: the excerpt ends mid-entry at `github.com/remyoudompheng/bigfft v0.0.0-20230129092748-24d4a6f8daec/go.` with `... (truncated, 8006 more characters)` (`go.sum:242-243`); contents beyond that point are not covered here.
**Covers:** `go.sum` (partially — truncated in source chunk)

## Integration Test (Milestone 1)
`TestIntegrationM1` (`integration_test.go:269`) runs against `t.TempDir()` (`integration_test.go:270`) in this order:
| Step | Subtest | What it asserts |
|---|---|---|
| 1 | `init` | `wiki.InitGreenfield(dir, "integration-test", "gemini-2.5-flash")` creates `raw`, `wiki/concepts`, `.sage`, `config.yaml`, `.manifest.json` (`integration_test.go:273-284`) |
| 2 | server | `mcppkg.NewServer(dir)` opens DB and registers tools (`integration_test.go:287-291`) |
| 3 | `populate` | Adds 3 FTS5 entries (`self-attention`, `flash-attention`, `kv-cache`), 3 vectors, 3 ontology entities, 2 relations (`implements`, `optimizes`), plus a test article file (`integration_test.go:294-332`) |
| 4 | `search_bm25` | `wiki_search` for `"attention optimization"` returns `flash-attention` (`integration_test.go:335-359`) |
| 5 | `search_tag_filter` | `wiki_search` for `"attention"` with `tags: "optimization"` returns exactly 1 result (`integration_test.go:362-378`) |
| 6 | `read_article` | `wiki_read` of `wiki/concepts/self-attention.md` contains `Self-Attention` (`integration_test.go:381-391`) |
| 7 | `ontology_query` | `wiki_ontology_query` for `self-attention`, `inbound`, depth 1 returns 2 entities (`integration_test.go:394-406`) |
| 8 | `status` | `wiki_status` contains `integration-test` and `Entries: 3` (`integration_test.go:409-417`) |
| 9 | `list_concepts` | `wiki_list` with `type: concept` returns 2 entities (`integration_test.go:420-431`) |
| 10 | `vectors` | `VecStore().Count()==3`, `Dimensions()==4` (`integration_test.go:434-443`) |
| 11 | `lint` | `linter.NewRunner().Run()` with `ValidRelations: ["implements", "optimizes"]`, no API needed (`integration_test.go:446-459`) |
| 12 | `learn` | `linter.StoreLearning(db, "gotcha", "integration test learning", "test", "integration")` (`integration_test.go:462-472`) |
| 13–14 | ontology lists | `ListEntities("concept")` returns 2; `ListRelations("", 100)` returns 2 (`integration_test.go:475-494`) |
Helper `callTool` builds `mcp.CallToolRequest` with `Name`/`Arguments`, calls `srv.CallTool`, fails on nil or `IsError`, and returns `TextContent.Text` (`integration_test.go:498-521`); helper `contains` is a manual substring scan (`integration_test.go:523-530`).
**Covers:** `integration_test.go`

**Covers:** `.dockerignore`, `.gitattributes`, `.gitignore`, `.golangci.yml`, `go.sum` (truncated in chunk), `integration_test.go`
