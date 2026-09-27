> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Critical Analysis: xoai/sage-wiki

## Claims vs. evidence
- Claim: an LLM compiler turns dropped-in docs (papers, notes, code, email) into an interlinked Obsidian wiki where each new source enriches existing articles. Evidence in corpus: feature description only; no compile-quality example, no before/after article, no eval of enrichment vs. duplication.
- Claim: opt-in evidenced graph (typed entities, provenance-bearing relations, resolved aliases, per-fact citations with source doc + confidence). Evidence: schema and pass names described (`ontology.triples`, `ontology.resolve`, `dedup_strategy: "llm"`); no precision/recall numbers for extraction, resolution, or citation faithfulness.
- Claim: `wiki_graph_query` answers are grounded only in serialized graph edges. Evidence: asserted, not demonstrated; the sole test (`TestIntegrationM1`) queries a hand-populated 3-entity fixture, so grounding under real LLM-extracted graphs is unproven.
- Claim: quarantine + trust lifecycle keeps unverified outputs out of answers. Evidence: lifecycle named (under_review/outputs, promotion/demotion, consensus) but no policy detail, no false-positive/negative rates, no toil estimate.
- Claim: hybrid retrieval (BM25 + vector + graph proximity at `search.hybrid_weight_graph`, with expansion, re-rank, graph-aware assembly) improves answers. Evidence: mechanism described; the integration test asserts one BM25 case (`"attention optimization"` -> `flash-attention`) and one tag filter — no ablation, no benchmark.
- Claim: one Go binary scales personal vault -> team hub -> company graph (100K+ docs via tiered compilation, Postgres/pgvector). Evidence: tier names and guide pointers only; test fixture is 3 docs on SQLite with 4-dim vectors — scale claim is entirely unexercised in this corpus.
- Claim: incremental compile costs zero LLM calls on unchanged docs (`--explain`, `--force`, `--watch`, manifest skipping). Evidence: plausible via `.manifest.json` content hashing, but no cost/latency figures for the dirty path (per-doc triples pass + global curation pass).
- Claim: corpus-wide questions work via opt-in community detection with cached summaries answered in `wiki_graph_query` `mode: "global"`. Evidence: architecture named only; no example global answer, no summary-freshness or staleness policy in corpus.
- Claim: the relation vocabulary is user-definable (`configurable-relations`) including multilingual synonyms and type restrictions. Evidence: guide title only; no sample vocabulary, no guard against relation-sprawl degrading traversal precision.
- Claim: local-model operation (Ollama, GPU/CPU routing, per-pass model config) frees the personal tier from API dependence. Evidence: routing surface described; no quality or throughput comparison for extraction/curation passes on small models.

## Genuinely new vs. repackaged
- Genuinely distinctive: markdown-first store where the wiki *is* the database and the graph is a compile output, not a synced sidecar — humans browse the same artifact agents query.
- Distinctive: review-gated entity resolution ("K8s"/"Kubernetes" merge as proposals, never silent) plus enumerated-entity protection (`mw-3` is not `mw-2`) and logged drops behind `llm_dedup.allow_drop`.
- Distinctive: bi-temporal edges (contradiction invalidates old edge, `as_of` historical queries) combined with quarantine-by-default answers.
- Distinctive: generated agent skill files (search/capture/compile) plus a read-capture-evolve loop as a shipped primitive, not an afterthought.
- Repackaged: BM25 + vector hybrid search, LLM query expansion, re-ranking, pgvector storage, TUI/web UI, Docker Compose deployment — standard RAG-system furniture.
- Repackaged: repo hygiene (pinned `go.sum`, golangci-lint v2 gate, `init -> populate -> search -> status` integration test) is competent but conventional Go practice.
- Genuinely useful but unproven at scale: tiered compilation with backpressure and code parsers for 100K+ docs — the right decomposition (tier, throttle, parse), but no throughput or degradation curve in corpus.
- Borrowed lineage, honestly disclosed: grown from Karpathy's LLM-compiled knowledge-base idea and built on the Sage Framework — derivation is stated, not hidden, which raises rather than lowers trust.

## Weaknesses and blind spots
- Corpus ceiling: this analysis sees only README-level overview plus top-level hygiene files; all 17 guides, security limits table, prompts, and storage/metrics internals are referenced by name only — judgments below are about claimed design, not verified implementation.
- No evals anywhere in corpus: no citation precision, no resolution accuracy, no retrieval benchmarks, no hallucination-rate measurement for compiled articles.
- Cost opacity: one extra LLM call per doc for triples plus a global curation pass with whole-vocabulary view; at 100K docs this is the cost and latency bottleneck, yet no figures exist here.
- Global curation bottleneck: the single pass with global view (`keep/fold/drop`) is inherently hard to parallelize; semantic-fold errors at scale could merge or drop load-bearing concepts.
- Conflict toil: ambiguous contradictions "surface via output-trust review" — i.e., routed to humans. Team-scale write contention could turn the trust queue into a second inbox.
- Truncated inputs: source-format table cuts off mid-row after CSV; `go.sum` excerpt truncates mid-hash; macro-components section lists only `top-level-files/` — coverage beyond that is unknown.
- Local-model quality gap: local/Ollama routing is offered, but extraction, curation, and citation quality on small models vs. frontier APIs is unaddressed.
- Frontend friction: web UI build requires Node (`npm install && npm run build`); CLI-only install avoids it but splits the shipped experience.
- HTTP API surface risk: `/v1` REST with auth, idempotency, async jobs, webhooks (HMAC, retry/dead-letter), and subscription OAuth is a large surface for a "one binary" story — each integration (auth-fronting, reverse proxy, Syncthing/VPS) is operator burden documented only by guide titles here.
- Retrieval tuning opacity: fusion weight (`search.hybrid_weight_graph`), chunking, expansion, re-rank, and ANN settings are configurable, but no defaults, sensitivity notes, or failure modes (e.g., graph channel drowning lexical on empty ontology — claimed byte-identical, otherwise uncharacterized).
- Security posture unknown: threat model, limits table, prompt boundary, and residual risks are cited as existing docs but their contents are outside this corpus — prompt-injection via compiled sources is the obvious unexamined attack (malicious raw/ doc -> trusted wiki article -> cited answer).

## Applicability
- Personal research vault: strongest fit — overlay existing Obsidian vault, compile papers/notes, browse markdown directly, no server needed.
- Team knowledge base: plausible second fit — git-synced wiki plus shared server and hub federation match small-team workflows, provided trust-review toil stays low.
- Company knowledge graph: weakest fit on current evidence — Postgres/pgvector, auth-fronted server, metrics, and tiered compilation are claimed but unexercised in this corpus; needs a scale pilot before belief.
- **Relevance to my work**
  - AI/ML engineering: compile-manifest skipping, per-pass model routing, and quarantined outputs are reusable patterns for cost-controlled indexing pipelines and eval-gated promotion.
  - Agentic systems: 19 MCP tools + generated skills + grounded graph-query-with-citations is a concrete template for giving agents browsable, provenance-bearing memory instead of naked vector search.
  - Elisity data platform: evidenced edges (`evidence`, `confidence`, `source_doc`), provenance queries ("which sources produced this concept"), and `as_of` bi-temporal reads map directly onto data-lineage, audit, and point-in-time correctness needs.
- Poor fit where: low-latency serving with strict freshness SLAs (compile-then-query is batch-shaped, not streaming), or adversarial corpora where source poisoning matters — quarantine helps only if reviewers keep up.
- Adoption preconditions: a reviewer willing to own the trust queue, a pinned relation vocabulary before first compile, and a small seed corpus where markdown output can be read end-to-end for quality judgment.

## What this changes
- If the compile quality holds, the unit of knowledge work shifts from "write notes" to "drop sources, review proposals" — curation becomes exception-handling (resolution proposals, trust queue, dedup drops) rather than authoring.
- Markdown-as-database collapses the human/agent tooling split: one artifact serves Obsidian browsing, TUI dashboard, web UI, MCP queries, and git versioning simultaneously.
- Provenance-by-default (every relation carries its asserting document) makes "who says so" a first-class query instead of forensic reconstruction — a prerequisite for trusting agent memory.
- The risk it introduces is silent graph rot: confident-looking compiled articles and resolved entities can entrench extraction errors unless the trust queue is actually worked, so adoption cost is ongoing reviewer attention, not just setup.
- It also reframes eval priorities: for memory systems, extraction fidelity, resolution correctness, and citation faithfulness matter more than raw retrieval recall — yet those are exactly the metrics missing from this corpus, so the first build step in any trial must be instrumentation, not more sources.

## Verdict
- Use it where markdown-native, provenance-bearing agent memory matters and a human will work the review queues; do not bet a company-scale rollout on this corpus alone — the scale, quality, and cost claims are undescribed where it counts.
- Concrete next step: scoped pilot on a real 50–200 doc corpus measuring compile cost per doc, citation precision on multi-hop queries, resolution proposal acceptance rate, and trust-queue hours/week before any team-server commitment.
- Call: **trial**
