> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Critical Analysis: docsagent/docsagent
## Claims vs. evidence
- **~15 ms retrieval over 1,000+ PDFs, constant latency:**
  plausible for a resident BM25 inverted index, but self-reported only.
  Two cited points (1,506-PDF Mac build, 500-PDF Windows VM) with no
  query mix, concurrency level, or p50/p99 definition.
- **160–227 MB for a 1,500-paper library:**
  believable for C++ BM25 plus passages, but a single data point.
  The 10k-paper / 15–20 min claim is linear extrapolation, not a run.
- **Fully local and private:**
  true for core search, which reads `~/Zotero/zotero.sqlite` + `storage/`
  directly on the machine. Weakened by group sync over the Zotero Web API
  and `import_item` resolving DOI/ISBN/arXiv via a translation server.
- **"Hybrid text + semantic, zero leakage" (SKILL.md):**
  contradicted by the digest, which documents only BM25 + passage ranking.
  Either the skill overclaims or a semantic path is undocumented.
  Treat hybrid as unverified until the core evidences it.
- **Spec-driven contract (`spec/` as single source):**
  the strongest claim and well-evidenced — 8 tool schemas, 23 JSON-RPC
  methods, error codes plus config schema mirrored into both shells.
- **Three-layer write safety gate:**
  concrete and checkable (gated registration unless `enableWrites=true`,
  `confirmed=false` preview consuming no quota, 30/h confirmed-write limit,
  extra confirmation above 20 items in `batch_modify`).
  Credible design; no abuse-test evidence cited.
## Genuinely new vs. repackaged
- **Genuinely useful packaging:**
  a resident C++ core that survives MCP client restarts, with thin shells
  that never touch Zotero files and never spawn the core per tool call.
  This fixes the common cold-start / rebuild-index-per-call antipattern.
- **Dual-shell, one-contract distribution:**
  TypeScript (`@docsagent/mcp-zotero`) plus a feature-equal Python wrapper
  over one JSON-RPC contract, shipped via npm, PyPI, MCP Registry, Smithery.
  Pragmatic reach, not research novelty.
- **Repackaged retrieval:**
  inverted-index BM25, query-ranked passages, token budgets, result dedup
  (id, then normalized title + year) are standard RAG plumbing.
  No evidenced reranker, dense vectors, or hybrid fusion.
- **Repackaged safety:**
  opt-in writes, dry-run previews, per-hour rate limits, per-request RBAC
  on HTTP are conventional guardrails, competently combined rather than
  invented. The combination is worth copying even if no part is new.
## Weaknesses and blind spots
- **Retrieval ceiling:**
  BM25-only means vocabulary mismatch and weak multilingual/semantic recall.
  No cited eval — no recall@k, MRR, or comparison against embedding search.
- **Single-source lock-in:**
  Zotero-first makes `~/Zotero` layout, SQLite schema, and local-API
  assumptions load-bearing. Direct SQLite reads risk breakage on upgrades,
  locked DBs, or concurrent Zotero writes; no incremental-index story shown.
- **Ops weight:**
  ~70 MB npm tarball and ~65 MB wheel bundling all-platform binaries.
  Manual `core start` precedes any shell use; the shell fails fast otherwise.
  One shared `~/.docsagent/config.json` with `0.0.0.0` defaults invites error.
- **Incomplete distribution:**
  Python wheel is build-locally with PyPI upload pending.
  Smithery stdio mapping forwards the data dir but not `enableWrites`.
  Directory listings are web-form submissions, not verification.
- **Security asymmetry:**
  origin checks, API-key/OAuth2 introspection, RBAC, and `/health` exist
  only on Streamable HTTP. Stdio relies on local-process trust with no
  multi-user story.
- **Missing evidence:**
  no failure-mode analysis (corrupt/encrypted PDFs, CJK tokenization),
  no concurrency or multi-client behavior, no freshness/locking analysis,
  no rollback testing beyond the `add_note` orphan check.
## Applicability
- Fits solo researchers and small teams living in Zotero who want fast,
  private, agent-queryable libraries from Claude Desktop, Cursor, Cline,
  or Qwen Code without shipping PDFs to the cloud.
- Does not fit multi-source bases (Drive/Notion/Confluence/code),
  semantic-discovery workloads, hosted multi-tenant deployments,
  or teams needing evaluated recall guarantees.
- **Relevance to my work**
  - *AI/ML engineering:* spec-first MCP design (schemas → validation →
    typed errors), token-budget packing, and resident-index sidecars
    for large local corpora are directly reusable.
  - *Agentic systems:* resident-core plus stateless-shell split,
    fail-fast-when-core-down, preview-before-write, and rate-limited
    gated writes port cleanly to file- and code-editing agents.
  - *Elisity data platform:* local-first private retrieval suits sensitive
    docs, but Zotero-only ingestion, no evidenced semantic search, and
    stdio-only trust make this a reference pattern, not a drop-in —
    adopt the contract and gate ideas, not the binary.
## What this changes
- Shows personal-library RAG needs no vector DB or cloud:
  a small C++ BM25 sidecar at millisecond latency and ~200 MB
  covers keyword-driven agent workflows over thousands of papers.
- Raises the bar for MCP server hygiene:
  single-sourced schemas, shell-never-touches-data, explicit core lifecycle,
  and preview plus rate-limit write gates should be the default template.
- Clarifies the ceiling:
  without dense/hybrid retrieval and evals, this class stays a fast finder,
  not a research synthesizer. The "digest my library" demo still needs
  an agent and a token budget on top.
## Verdict
- Narrow but solid: use where Zotero plus keyword search plus privacy
  coincide, copy the architecture everywhere else, and demand semantic
  evidence before treating it as general document intelligence.
- For now: **trial**.
