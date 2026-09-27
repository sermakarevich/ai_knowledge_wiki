# Graphify — Open-Source Knowledge Graph Skill for AI Coding Assistants

**Source:** [Graphify](https://graphify.net/) — product/docs site, maintained by Safi Shamsi

## Human Readable TL;DR

Imagine handing a new hire your entire codebase, papers, diagrams and docs on day one, and instead of them reading every file, they get a map showing which pieces matter most, how everything connects, and which connections are surprising. Graphify builds that map automatically for AI coding assistants (Claude Code, Codex, OpenCode) so the assistant can look up "what does this touch and why" without re-reading the whole repo every time.

## TL;DR

Graphify (PyPI package `graphifyy`, CLI `graphify`) is an MIT-licensed, open-source skill that builds a queryable knowledge graph from a repository's code, docs, papers and diagrams. It combines Tree-sitter static analysis (ASTs, call graphs) with LLM-driven semantic extraction and vision-model diagram reading, merges everything into a NetworkX graph, clusters it with the Leiden algorithm (no embeddings/vector store), and surfaces "god nodes" and unexpected cross-file connections. It ships `/graphify`, `/graphify query`, `/graphify path` and `/graphify explain` commands for AI coding assistants, and reports a 71.5× token-cost reduction versus naive full-context retrieval on a mixed code+paper corpus.

---

## Problem & Motivation

AI coding assistants working on large, multi-modal repositories (code + docs + research papers + diagrams) either re-read large portions of the repo on every query (expensive, slow) or rely on vector/RAG retrieval that captures semantic similarity but not structural relationships (who calls whom, what depends on what, why a design choice was made). Graphify's pitch is that a **structural graph beats vector RAG** for code understanding because it preserves call/dependency topology and lets an assistant answer "what" and "why" questions cheaply via targeted graph traversal instead of ingesting large spans of raw text.

---

## Main Original Ideas

1. **Multi-modal extraction pipeline** — a single pipeline parses source code (.py, .js, .go, .java, etc.) via Tree-sitter for ASTs/call graphs/docstrings, Markdown and PDFs via LLM concept extraction, and diagrams via vision models — unifying code, docs, papers and images into one graph instead of siloed tools per modality.
2. **No-embedding clustering** — community detection uses the **Leiden algorithm** directly on graph topology, explicitly avoiding vector embeddings or a vector store, which the site frames as a differentiator vs. embedding-based RAG.
3. **"God nodes" and surprise-edge detection** — the `analyze` stage identifies the highest-degree nodes (structural centers of the system) and flags unexpected cross-file/cross-domain edges worth a human's attention (e.g. `DigestAuth → Response` in the httpx example).
4. **Assistant-native command surface** — rather than being a standalone tool, Graphify ships skill manifests (`skill-*.md`) and slash commands (`/graphify`, `/graphify query`, `/graphify path`, `/graphify explain`) so Claude Code, Codex and OpenCode can invoke it directly as part of their tool-use loop.
5. **Security-by-design ingestion** — the `security.py` module restricts fetched URLs to http/https, enforces size/timeout limits on downloads, path-containment-checks output writes, and HTML-escapes node labels — defending specifically against SSRF, injection and XSS in a tool that ingests arbitrary repo content.

---

## Key Findings

**Pipeline stages:** `detect → extract → build → cluster → analyze → report → export`, each an isolated module; supporting modules: `ingest.py` (URL fetching), `cache.py` (semantic caching), `security.py` (input validation), `watch.py` (live updates), `serve.py` (MCP-protocol service).

**Worked examples reported on the site:**

| Corpus | Size | Result | Notes |
|---|---|---|---|
| httpx (small) | 6 Python files, HTTP transport layer | 144 nodes, 330 edges, 6 communities | God nodes: `Client`, `AsyncClient`, `Response`, `Request`. Surprise edge: `DigestAuth → Response` |
| Karpathy mixed corpus | 3 GPT framework repos + 5 attention papers + 4 diagrams (~52 files, ~92k words) | 285 nodes, 340 edges, 53 communities | Avg. query cost ~1.7k tokens vs. ~123k naive → **71.5× reduction** |
| Large-scale (FAQ claim) | ~500k-word corpus | BFS subgraph queries ~2k tokens vs. ~670k naive | Claimed to preserve compression ratio at scale |

**Outputs:** `graph.html` (interactive visualization), `GRAPH_REPORT.md` (human-readable audit: core nodes, surprises, suggested questions), `graph.json` (persistent, queryable graph), `cache/` (incremental cache).

**Stats badges on the landing page:** 3.7k+ GitHub stars, MIT license, 71.5× token reduction, Python 3.10+ runtime.

**Install:**
```bash
pip install graphifyy && graphify install
/graphify ./raw   # build a knowledge graph for any project folder
```
(Package name on PyPI is `graphifyy`; the CLI command is `graphify`.)

**Privacy/network model:** Graphify does not bundle an LLM — it uses the model API key already configured in the host AI assistant, and only sends semantic descriptions of documents/diagrams upstream, never raw source code. The project performs no telemetry; the only outbound call is the semantic-extraction step.

**Comparison table (from the site):**

| Project | Focus | Strength | Limitation vs. Graphify |
|---|---|---|---|
| Sourcegraph | Cross-repo code search | Enterprise-grade navigation | Not a knowledge graph; limited design semantics |
| Code2Vec | Function-level embeddings | Vector retrieval & classification | No graph structure, no multi-modal input |
| Neo4j | General graph database | Powerful Cypher queries | Does not generate graphs from code itself |

**FAQ (per site):**
- Does it send code to a third party model? — No, only semantic descriptions, never raw source.
- Supported assistants — Claude Code, OpenAI Codex, OpenCode out of the box via `skill-*.md` manifests; any shell-capable assistant can invoke `graphify`.
- Scale — Tree-sitter/NetworkX scale linearly; ~2k-token BFS queries claimed on a ~500k-word corpus.
- Commercial use — MIT-licensed, free for personal and commercial use.

---

## Suggestions & Future Directions

Not explicitly stated by the source as a roadmap — the site is a marketing/docs landing page, not a paper, so there is no authors' "future work" section. Implicit open questions worth flagging: all quantitative claims (token-reduction ratios, star count, corpus results) are self-reported by the maintainer on the project's own site and were **not independently verified** here; treat them as vendor claims pending third-party benchmarking.

---

## Authors & Institutions

Maintained by **Safi Shamsi**. Repository: [github.com/safishamsi/graphify](https://github.com/safishamsi/graphify). Package: [pypi.org/project/graphifyy](https://pypi.org/project/graphifyy/). License: MIT. Built on NetworkX (BSD) and Tree-sitter (MIT).

## Related pages linked from the site

- [Knowledge Graphs for AI Coding Assistants](https://graphify.net/knowledge-graph-for-ai-coding-assistants.html) — why structural graphs beat vector RAG for code understanding.
- [Tree-sitter AST Extraction](https://graphify.net/tree-sitter-ast-extraction.html) — how Graphify parses 19 languages locally, no LLM calls on source.
- [Leiden Community Detection](https://graphify.net/leiden-community-detection.html) — clustering on graph topology alone.
- [Claude Code Integration](https://graphify.net/graphify-claude-code-integration.html) — CLAUDE.md directives and the PreToolUse hook.
- [CLI Command Reference](https://graphify.net/graphify-cli-commands.html) — every `/graphify` and `graphify` command.
- [Graphify vs Alternatives](https://graphify.net/graphify-vs-alternatives.html) — comparison vs Sourcegraph, Code2Vec, Neo4j.
