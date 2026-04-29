# Technical Analysis: code-review-graph

**Repository:** https://github.com/tirth8205/code-review-graph  
**Version analyzed:** 2.3.2  
**Date:** 2026-04-23

---

## 1. Overview / What Problem It Solves

Code review in large codebases is expensive, not because reviewers lack skill, but because assembling the relevant context is slow and token-hungry. A reviewer needs to know: what exactly changed, which functions are affected, what calls those functions, are there tests covering them, and do those tests cross community boundaries? Answering that typically means a series of manual searches, file reads, and grep calls that together cost hundreds of LLM tokens and are error-prone.

`code-review-graph` is a Python MCP server that pre-computes and persists a structural knowledge graph of your codebase — stored in a local SQLite file — and exposes it as a set of 28+ MCP tools that AI coding assistants (Claude Code, Cursor, Windsurf, Zed, Codex, OpenCode, and others) can call during a review session. Instead of asking an LLM to re-read the whole codebase, the server answers precise queries — "what calls this function?", "which execution flows pass through this module?", "what is the blast radius of these three changed files?" — directly from the pre-built graph. The primary user is an AI coding agent, not a human typing commands, though a human-facing CLI is also fully functional.

---

## 2. High-Level Architecture

```
User / AI agent
      │
      ▼
 MCP Protocol (stdio or HTTP/SSE)
      │
      ▼
 FastMCP server  ─────────── code_review_graph/main.py
  28 tools + 5 prompts
      │
      ├──► code_review_graph/tools/      (tool implementations)
      │         build.py        ── build_or_update_graph
      │         review.py       ── get_review_context, detect_changes
      │         context.py      ── get_minimal_context
      │         analysis_tools  ── hub/bridge/surprise/gaps
      │         flows_tools     ── list/get/affected flows
      │         community_tools ── list/get communities
      │         query.py        ── callers_of, callees_of, imports_of ...
      │         refactor_tools  ── rename preview, dead code
      │
      ├──► code_review_graph/graph.py    (GraphStore — SQLite backend)
      │
      ├──► code_review_graph/parser.py   (Tree-sitter parse → NodeInfo/EdgeInfo)
      │
      ├──► code_review_graph/incremental.py  (full_build / incremental_update)
      │
      ├──► code_review_graph/postprocessing.py  (signatures, FTS, flows, communities)
      │
      ├──► code_review_graph/flows.py    (entry-point detection + flow tracing)
      ├──► code_review_graph/communities.py  (Leiden algorithm / file-based)
      ├──► code_review_graph/changes.py  (git/svn diff → risk-scored nodes)
      ├──► code_review_graph/embeddings.py  (vector search, optional)
      └──► code_review_graph/visualization.py  (D3.js HTML export)
```

**Data flow from "user runs tool" to "user sees review":**

1. `code-review-graph build` (CLI or `build_or_update_graph_tool` MCP call) triggers `incremental.py::full_build`, which walks the repo, calls `parser.py::CodeParser.parse_file` per file in a `ProcessPoolExecutor`, and batch-writes `NodeInfo` / `EdgeInfo` records into SQLite.
2. Post-processing (`postprocessing.py`) runs four sequential steps: compute node signatures, rebuild FTS5 search index, trace execution flows (`flows.py`), detect code communities (`communities.py`).
3. At review time the AI agent calls `detect_changes_tool` or `get_review_context_tool`. This reads `git diff`, maps changed line ranges to graph nodes (`changes.py::map_changes_to_nodes`), computes per-node risk scores, resolves affected flows and test coverage gaps, and returns a structured JSON dict.
4. The agent receives roughly 100–500 tokens of targeted context rather than re-reading source files.

The SQLite database is stored at `.code-review-graph/graph.db` inside the repo directory. The file is added to `.gitignore` by the `install` command, so it is never committed.

---

## 3. The Code Graph

**Representation:** A directed property graph backed by a single SQLite database. It is not an AST; the AST is used only during parsing to extract entities. The persisted graph is a flat table of nodes and a flat table of edges with typed relationships.

**Node kinds:**
- `File` — each source file
- `Class` — classes, structs, interfaces, enums, contracts
- `Function` — functions, methods, constructors, arrow functions
- `Type` — type aliases, type definitions
- `Test` — test functions/methods (detected by name pattern or test file path)

**Edge kinds** (defined in `parser.py:57-67` `EdgeInfo.kind` docstring and `graph.py:2-5`):
- `CALLS` — function invocation
- `IMPORTS_FROM` — import/require/use/include
- `INHERITS` — class inheritance
- `IMPLEMENTS` — interface implementation
- `CONTAINS` — parent→child structural nesting
- `TESTED_BY` — test function covers this symbol
- `DEPENDS_ON` — general dependency
- `REFERENCES` — any other reference

Edge records carry a `confidence` float (0.0–1.0) and a `confidence_tier` (`EXTRACTED`, `INFERRED`, etc.), allowing downstream tools to filter or weight by parse certainty.

**Parser:** Tree-sitter, via the `tree-sitter-language-pack` PyPI package. This provides pre-compiled grammars for ~35 languages in a single wheel with no system-level build step required. The parser does not use `libcst`, `ast`, or `tree-sitter` directly; instead it uses the pack:

```python
# parser.py:17
import tree_sitter_language_pack as tslp
```

Language detection is file-extension-based (`EXTENSION_TO_LANGUAGE` dict, `parser.py:74-128`). Each language has explicit mappings for which Tree-sitter node types map to classes, functions, imports, and calls (`_CLASS_TYPES`, `_FUNCTION_TYPES`, `_IMPORT_TYPES`, defined at `parser.py:132-280`).

**Traversal during review:** The impact-radius query in `graph.py::get_impact_radius_sql` uses a SQLite recursive CTE:

```sql
-- graph.py:680-698
WITH RECURSIVE impacted(node_qn, depth) AS (
    SELECT qn, 0 FROM _impact_seeds
    UNION
    SELECT e.target_qualified, i.depth + 1
    FROM impacted i
    JOIN edges e ON e.source_qualified = i.node_qn
    WHERE i.depth < ?
    UNION
    SELECT e.source_qualified, i.depth + 1
    FROM impacted i
    JOIN edges e ON e.target_qualified = i.node_qn
    WHERE i.depth < ?
)
SELECT DISTINCT node_qn, MIN(depth) AS min_depth FROM impacted GROUP BY node_qn LIMIT ?
```

This BFS traverses both forward (target) and backward (source) edges up to `MAX_IMPACT_DEPTH` (default: 2, overridden via `CRG_MAX_IMPACT_DEPTH`). A legacy NetworkX BFS path is also kept and activated by setting `CRG_BFS_ENGINE=networkx`.

---

## 4. LLM Integration

`code-review-graph` does **not** call any LLM itself in its default configuration. It is a pure MCP server: it exposes tools and prompts that AI agents call. The LLM is the client, not the server. This is a critical design choice: no OpenAI or Anthropic API keys are required to build or query the graph.

**Where LLMs do appear (optional only):**

1. **Wiki generation (`wiki.py`):** When the optional `[wiki]` extra is installed (`pip install code-review-graph[wiki]`), community summary pages can be LLM-generated via `ollama`. No API keys needed; requires a running Ollama instance.

2. **Embeddings (`embeddings.py`):** Optional semantic search (`embed_graph_tool`) supports four providers:
   - `local`: `sentence-transformers`, default model `all-MiniLM-L6-v2` (offline, 384-dim)
   - `openai`: any OpenAI-compatible endpoint (`CRG_OPENAI_BASE_URL` + `CRG_OPENAI_API_KEY` + `CRG_OPENAI_MODEL` env vars)
   - `google`: Gemini embeddings (`google-generativeai`, `CRG_GEMINI_API_KEY`)
   - `minimax`: MiniMax embo-01 (`MINIMAX_API_KEY`)

Embeddings are stored as binary blobs in a separate SQLite table alongside the main graph database. Vectors are stored once per node; the model name + provider are recorded so a model switch triggers a full re-embed.

**FastMCP** (`fastmcp>=3.2.4`) is the MCP server framework. It handles JSON-RPC framing over stdio or HTTP. There is no LangChain, LangGraph, or similar agent framework in the codebase.

**Prompt structure:** Five workflow prompts are defined in `prompts.py`. They follow a token-efficiency-first strategy:

```python
# prompts.py:15-28  — _TOKEN_EFFICIENCY_PREAMBLE
"1. ALWAYS call `get_minimal_context` first with a task description.
 2. Use `detail_level="minimal"` on all tool calls unless the minimal output is insufficient.
 3. Only escalate to `detail_level="standard"` or "verbose" for specific entities.
 ..."
```

Prompts are returned as `[{"role": "user", "content": "..."}]` lists. They do not include graph data; they are workflow instructions telling the AI agent which sequence of tools to call. Token limits are managed at the tool level via `detail_level` parameters and compact response helpers (`tools/_common.py::compact_response`).

---

## 5. Review Pipeline

When `detect_changes_tool` (the primary review tool) is called:

1. **Change detection** (`changes.py::parse_diff_ranges`): Dispatches to `git diff --unified=0` (or `svn diff`) to extract changed line ranges per file. Git refs are validated against `_SAFE_GIT_REF = re.compile(r'^[A-Za-z0-9_.~^/@{}\-]+$')` to prevent injection.

2. **Node mapping** (`changes.py::map_changes_to_nodes`): Iterates over changed line ranges, fetches all graph nodes for each file, and keeps nodes whose `[line_start, line_end]` overlaps any changed hunk. This links textual changes to semantic graph entities.

3. **Risk scoring** (`changes.py::compute_risk_score`): For each changed function/class, a 0.0–1.0 score is computed from five factors:
   - Flow participation (0–0.25): sum of flow criticality scores, capped
   - Community crossing (0–0.15): 0.05 per caller from a different community
   - Test coverage (0.05–0.30): 0.30 if untested, decreasing as test count grows
   - Security sensitivity (0.20): name matches keywords like `auth`, `token`, `sql`, `encrypt` (`constants.py:7-12`)
   - Caller count (0–0.10): `callers / 20`, capped

4. **Affected flows** (`flows.py::get_affected_flows`): Finds execution flows that contain any of the changed nodes. Flows are pre-computed during post-processing; this step is a lookup, not a re-trace.

5. **Test coverage gap detection**: Uses `graph.py::get_transitive_tests` to find direct and indirect test coverage. Functions with zero transitive test coverage are flagged as test gaps.

6. **Output assembly**: A structured dict is built with `summary`, `risk_score`, `changed_functions`, `affected_flows`, `test_gaps`, and `review_priorities`, with results ordered by risk score descending.

The tool supports both `detail_level="standard"` (full data) and `detail_level="minimal"` (summary + top 5 items, ~60% fewer tokens).

---

## 6. Key Files

| File | Lines | What It Does |
|------|-------|-------------|
| `code_review_graph/graph.py:1-1359` | 1359 | `GraphStore`: SQLite schema, all read/write operations, recursive CTE BFS, FTS5 search, transitive test resolution, batch queries. Central data access layer. |
| `code_review_graph/parser.py:1-~1800` | ~1800 | `CodeParser`: Tree-sitter parsing for 35+ languages. Defines all node/edge extraction logic, language-to-extension mapping, and per-language AST node type mappings. Largest file. |
| `code_review_graph/main.py:1-999` | 999 | `FastMCP` server: declares all 28 MCP tools and 5 prompts, wraps sync tool implementations in `asyncio.to_thread`, implements tool allow-list filter (`CRG_TOOLS`). |
| `code_review_graph/cli.py:1-989` | 989 | CLI entry point: argparse for all commands (`build`, `update`, `watch`, `serve`, `visualize`, `wiki`, `detect-changes`, `daemon`, `eval`, etc.). |
| `code_review_graph/changes.py:1-~400` | ~400 | Change impact analysis: `parse_git_diff_ranges`, `parse_svn_diff_ranges`, `map_changes_to_nodes`, `compute_risk_score`, `analyze_changes`. |
| `code_review_graph/flows.py:1-~450` | ~450 | Execution flow detection: entry-point discovery (framework decorators, name patterns), forward BFS from entry points, criticality scoring, persistence. |
| `code_review_graph/communities.py:1-~350` | ~350 | Community detection: Leiden algorithm via optional `igraph`, weighted edge types, community naming from member node names. Falls back to file-based grouping. |
| `code_review_graph/incremental.py:1-~500` | ~500 | `full_build` and `incremental_update`: parallel file parsing via `ProcessPoolExecutor`, `.gitignore`-aware file filtering, file hash change detection, git/SVN VCS detection. |
| `code_review_graph/postprocessing.py:1-~200` | ~200 | Four-step post-build pipeline: signatures, FTS5 rebuild, flow tracing, community detection. Used identically by CLI, MCP tool, and watch mode. |
| `code_review_graph/embeddings.py:1-~400` | ~400 | Provider abstraction for local (sentence-transformers), OpenAI-compatible, Google Gemini, and MiniMax embeddings. Binary vector storage in SQLite. |
| `code_review_graph/prompts.py:1-171` | 171 | Five MCP prompt templates: `review_changes`, `architecture_map`, `debug_issue`, `onboard_developer`, `pre_merge_check`. Pure workflow instructions, no graph data. |
| `code_review_graph/skills.py:1-~500` | ~500 | Multi-platform MCP config installer: detects Claude Code, Cursor, Windsurf, Zed, Codex, Kiro, OpenCode, etc. and writes `.mcp.json` / `settings.json` entries. |
| `code_review_graph/visualization.py:1-~600` | ~600 | Self-contained D3.js HTML export with force-directed layout. Supports `full`, `community`, `file`, and `auto` rendering modes for large graphs. |
| `code_review_graph/tools/review.py:1-~400` | ~400 | `get_review_context` and `detect_changes_func`: composes impact radius, source snippets, and review guidance for MCP responses. |
| `code_review_graph/tools/_common.py:1-116` | 116 | Shared utilities: `_get_store`, `compact_response`, `_validate_repo_root`, JS/TS builtin call name filter list. |

---

## 7. Dependencies

| Package | Version constraint | Purpose |
|---------|-------------------|---------|
| `fastmcp` | `>=3.2.4` | MCP server framework. Handles JSON-RPC over stdio and HTTP. Version 2.14+ required for CVE-2025-62800/62801/66416 fixes. |
| `tree-sitter` | `>=0.23.0,<1` | AST parsing C library Python bindings. |
| `tree-sitter-language-pack` | `>=0.3.0,<1` | Pre-compiled grammars for 35+ languages. Eliminates per-language `tree-sitter-*` installs. |
| `networkx` | `>=3.2,<4` | Graph algorithms (betweenness centrality, BFS fallback). Also used for the cached in-memory `DiGraph` for the legacy BFS path. |
| `watchdog` | `>=4.0.0,<6` | File system event watcher for `watch` mode. |
| `mcp` | `>=1.0.0,<2` | MCP protocol types (fastmcp depends on this). |
| `sentence-transformers` | optional `[embeddings]` | Local embedding model inference. Default: `all-MiniLM-L6-v2`. |
| `numpy` | optional `[embeddings]` | Vector arithmetic for cosine similarity. |
| `igraph` | optional `[communities]` | Leiden community detection algorithm. Fallback to file-based grouping when absent. |
| `google-generativeai` | optional `[google-embeddings]` | Gemini embedding API. |
| `jedi` | optional `[enrichment]` | Static analysis for type resolution and cross-file call enrichment. |
| `ollama` | optional `[wiki]` | LLM inference for community wiki page summaries. |
| `tomli` | Python < 3.11 | TOML parsing for daemon config (stdlib `tomllib` used on 3.11+). |
| `matplotlib`, `pyyaml` | optional `[eval]` | Evaluation benchmark visualization. |

---

## 8. CLI / Usage Surface

**Entry points** (defined in `pyproject.toml:47-49`):
- `code-review-graph` → `code_review_graph.cli:main`
- `crg-daemon` → `code_review_graph.daemon_cli:main`

**Commands:**
```
code-review-graph install   [--repo DIR] [--platform PLATFORM] [--dry-run] [-y]
code-review-graph build     [--repo DIR] [--skip-flows] [--skip-postprocess]
code-review-graph update    [--base REF] [--repo DIR]
code-review-graph watch     [--repo DIR]
code-review-graph status    [--repo DIR]
code-review-graph serve     [--http] [--host ADDR] [--port PORT] [--tools LIST]
code-review-graph visualize [--mode auto|full|community|file] [--format html|graphml|cypher|obsidian|svg] [--serve]
code-review-graph wiki      [--force]
code-review-graph detect-changes [--base REF] [--brief]
code-review-graph register  <path> [--alias name]
code-review-graph postprocess [--no-flows] [--no-communities] [--no-fts]
code-review-graph eval      [--benchmark LIST] [--all] [--report]
code-review-graph daemon    start|stop|restart|status|logs|add|remove
```

**Environment variables:**
| Variable | Default | Purpose |
|----------|---------|---------|
| `CRG_MAX_IMPACT_NODES` | `500` | BFS result cap |
| `CRG_MAX_IMPACT_DEPTH` | `2` | BFS hop limit |
| `CRG_MAX_BFS_DEPTH` | `15` | Flow tracing hop limit |
| `CRG_BFS_ENGINE` | `sql` | `sql` or `networkx` for impact BFS |
| `CRG_PARSE_WORKERS` | `min(cpu_count, 8)` | Parallel parse worker count |
| `CRG_GIT_TIMEOUT` | `30` | `git diff` subprocess timeout (seconds) |
| `CRG_TOOLS` | (all) | Comma-separated MCP tool allowlist |
| `CRG_EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Local embedding model |
| `CRG_OPENAI_BASE_URL` | — | OpenAI-compatible endpoint URL |
| `CRG_OPENAI_API_KEY` | — | API key for OpenAI-compatible endpoint |
| `CRG_OPENAI_MODEL` | — | Model name for OpenAI-compatible embeddings |
| `CRG_GEMINI_API_KEY` | — | Google Gemini API key |
| `MINIMAX_API_KEY` | — | MiniMax embedding API key |
| `CRG_RECURSE_SUBMODULES` | — | Include git submodule files in build |
| `NO_COLOR` | — | Disable ANSI color output |

**Configuration files:**
- `.mcp.json` (repo root): MCP server entry generated by `install`
- `.code-review-graph/graph.db`: SQLite graph database (gitignored)
- `~/.code-review-graph/registry.json`: Multi-repo registry
- `~/.code-review-graph/watch.toml`: Daemon watch config

---

## 9. Extensibility Points

**New language support:** Add the file extension to `EXTENSION_TO_LANGUAGE` in `parser.py:74`, then add entries to `_CLASS_TYPES`, `_FUNCTION_TYPES`, `_IMPORT_TYPES`, and `_CALL_TYPES` for the new language key. If the language requires special handling not expressible via simple node type lists (e.g. Elixir's `defmodule` pattern), add a dispatch to `_extract_<language>_constructs(node, source, file_path, ...)` within the main visitor in `parser.py`.

**New edge kind or node kind:** Add the new kind string to `EdgeInfo.kind` docstring and `graph.py`'s `_SCHEMA_SQL` comments. The schema itself uses free-text `kind` columns, so no migration is strictly required, but adding to `EDGE_WEIGHTS` in `communities.py:34-42` ensures it participates in community detection with appropriate weight.

**New MCP tool:** Add a function to the appropriate file in `code_review_graph/tools/`, import it in `code_review_graph/tools/__init__.py`, import the function in `main.py`, then decorate it with `@mcp.tool()`. The tool filter mechanism (`CRG_TOOLS`) picks it up automatically.

**New output format:** Add a branch to the `visualize` command in `cli.py` (~line 897) and implement an exporter function in `code_review_graph/exports.py`. For a new community-aware format, follow the existing `export_graphml` / `export_neo4j_cypher` patterns.

**New model provider for embeddings:** Subclass `EmbeddingProvider` in `embeddings.py:34-47`, implement `embed()`, `embed_query()`, `dimension`, and `name`, then add an `elif provider == "yourprovider":` branch in the factory function at the bottom of that file.

**New MCP prompt:** Add a function returning `list[dict]` to `prompts.py`, import it in `main.py`, and register it with `@mcp.prompt()`.

---

## 10. Limitations and Gotchas

**Python-only for most analysis.** While parsing supports 35+ languages, the risk scoring, flow tracing, and community detection are entirely graph-structural. The tool knows nothing about language-specific patterns beyond what Tree-sitter can capture as AST nodes and edges.

**Parser accuracy varies widely by language.** Python, TypeScript, Go, and Java have the most test coverage (`tests/test_multilang.py`, `tests/test_parser.py`). Languages like ReScript, GDScript, Luau, and Zig have regex-based or minimally tested parsers with explicit `FIXME`/`TODO` comments in the code. Dynamic dispatch patterns (Python `getattr(obj, method_name)()`, JS dictionary-of-functions) are silently missed.

**Tree-sitter does not execute code.** Call edges are syntactic, not semantic. Python's dynamic nature means many real call sites go unrecorded. The `jedi` enrichment pass (optional `[enrichment]`) partially addresses this for Python but is not enabled by default.

**Risk score is heuristic, not verified.** The `compute_risk_score` function in `changes.py:217-267` uses five fixed-weight factors tuned for general cases. Security keyword matching is a simple substring check on function names (`constants.py:7-12`) — it will both miss functions and flag false positives. The score correlates with structural coupling, not with actual defect probability.

**No LLM-generated code review comments.** Despite being called "code-review-graph," the tool does not produce "line 42: this assignment might throw a NullPointerException" style findings. It is purely a context provider. The AI agent calling the MCP tools is responsible for the actual code analysis.

**SQLite WAL mode with concurrent writes.** The graph store uses `isolation_level=None` (autocommit) and WAL mode (`graph.py:153`). Watch mode and the daemon run concurrent `incremental_update` calls. The `store_file_nodes_edges` method uses `BEGIN IMMEDIATE` transactions to prevent write conflicts, but multiple processes watching the same repo simultaneously could still hit lock contention with busy_timeout set to only 5 seconds.

**The `crg-daemon` is process-based, not async.** The daemon (`daemon.py`) manages child processes via `subprocess.Popen` and a polling thread. If the parent process is killed with SIGKILL, child processes are orphaned. There is no cgroup or process group management.

**Tool description token cost.** With 28 tools registered, each MCP tool definition sent to the LLM on every turn adds ~8k description tokens. The `CRG_TOOLS` allowlist is the only mitigation, and it requires the user to know in advance which tools they need.

**No execution of user code.** The parser reads files as text and does not exec/import them. This is the correct behavior, but it means framework-level behaviors (routing, middleware chains, dependency injection containers) are only partially recoverable from static analysis.

**Duplicate files with spaces in names.** The repo itself contains files like `code_review_graph/analysis 2.py`, `enrich 2.py`, `memory 2.py`, etc., which appear to be artifact copies left in version control. This is clearly a maintenance issue — these duplicate files have no tests and are not imported anywhere.

---

## 11. How It Compares to Alternatives

`code-review-graph` occupies a narrow but real niche: a persistent, pre-computed, offline-first structural context provider designed specifically for MCP-connected AI agents. It does not send your code to a cloud service and costs nothing per review.

**CodeRabbit and GitHub Copilot PR review** are cloud SaaS products that call a hosted LLM with a rolling window of diff + file context. They produce line-level comments automatically, which `code-review-graph` does not. However, they re-pay the context assembly cost on every PR and cannot answer structural queries like "how many execution flows pass through this function" without rereading the whole codebase.

**Sourcery** is a Python-focused static analyzer that applies a rule library to produce refactoring suggestions. It is deterministic and fast but language-limited and does not build a queryable graph.

**Semgrep + LLM patterns** provide rule-based pattern matching that can be extended with LLM-assisted rule generation. The rules are precise and auditable but require authoring per-language per-pattern. `code-review-graph` produces broader structural signals that Semgrep cannot easily encode as rules.

**Tree-sitter query languages** (used directly in editors) can answer "find all function calls to X" efficiently, but have no persistent storage, no cross-file impact analysis, no flow/community concepts, and no MCP interface.

`code-review-graph` is best understood as a complement to these tools: it reduces the structural context overhead so the LLM can spend more of its context budget on actual reasoning, rather than reconstructing what the codebase looks like.

---

## Appendix: Selected Code Snippets

**Risk score formula (changes.py:217-267):**
```python
def compute_risk_score(store: GraphStore, node: GraphNode) -> float:
    score = 0.0
    # Flow participation (cap 0.25)
    flow_criticalities = store.get_flow_criticalities_for_node(node.id)
    if flow_criticalities:
        score += min(sum(flow_criticalities), 0.25)
    # Community crossing (cap 0.15)
    cross_community = 0
    node_cid = store.get_node_community_id(node.id)
    if node_cid is not None and caller_edges:
        ...
        for cid in cid_map.values():
            if cid is not None and cid != node_cid:
                cross_community += 1
    score += min(cross_community * 0.05, 0.15)
    # Test coverage (0.05–0.30)
    test_count = len(store.get_transitive_tests(node.qualified_name))
    score += 0.30 - (min(test_count / 5.0, 1.0) * 0.25)
    # Security sensitivity (+0.20)
    if any(kw in node.name.lower() for kw in _SECURITY_KEYWORDS):
        score += 0.20
    # Caller count (cap 0.10)
    score += min(len(caller_edges) / 20.0, 0.10)
    return round(min(max(score, 0.0), 1.0), 4)
```

**Qualified name format (graph.py:1281-1286):**
```python
def _make_qualified(self, node: NodeInfo) -> str:
    if node.kind == "File":
        return node.file_path                          # e.g. "src/api/routes.py"
    if node.parent_name:
        return f"{node.file_path}::{node.parent_name}.{node.name}"  # e.g. "src/api/routes.py::Router.get_user"
    return f"{node.file_path}::{node.name}"            # e.g. "src/api/routes.py::get_user"
```

**Prompt injection defense (graph.py:1323-1337):**
```python
def _sanitize_name(s: str, max_len: int = 256) -> str:
    """Strip ASCII control characters and truncate to prevent prompt injection.
    Node names extracted from source code could contain adversarial strings
    (e.g. ``IGNORE_ALL_PREVIOUS_INSTRUCTIONS``). ..."""
    cleaned = "".join(
        ch for ch in s
        if ch in ("\t", "\n") or ord(ch) >= 0x20
    )
    return cleaned[:max_len]
```
