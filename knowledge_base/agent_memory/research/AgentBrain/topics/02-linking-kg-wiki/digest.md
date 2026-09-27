> [[../../index|Research]] | [[../../overview|Overview]] | [[../../digest|Digest]]

# linking and knowledge graphs

**In one sentence:** The four sources jointly establish that durable agent memory comes from compiling sources into interlinked markdown plus an explicit graph/provenance layer, with retrieval fusing lexical, vector, and graph signals and every new link gated by review or verdict.

## Key points
- All four keep the human-readable layer as ordinary interlinked Markdown (Obsidian-compatible), with the graph as a companion machine layer rather than a replacement for files [[research_topics/agent_memory/ClaudeObsidian/summary|ClaudeObsidian]] [[research_topics/agent_memory/Swarmvault/summary|Swarmvault]] [[research_topics/agent_memory/SageWiki/summary|SageWiki]] [[research_topics/agent_memory/VaultCurate/summary|VaultCurate]].
- Provenance is first-class: source/claim ledgers record authority, support, contradiction, and confidence [[research_topics/agent_memory/ClaudeObsidian/summary|ClaudeObsidian]], edges carry `extracted`/`inferred`/`ambiguous` tags plus contradiction flags [[research_topics/agent_memory/Swarmvault/summary|Swarmvault]], and evidenced edges carry span, confidence, and asserting document [[research_topics/agent_memory/SageWiki/summary|SageWiki]].
- Retrieval is hybrid everywhere: deterministic BM25 with optional cosine rerank [[research_topics/agent_memory/ClaudeObsidian/summary|ClaudeObsidian]], SQLite FTS plus semantic embeddings with bounded traversal (`graph query`/`path`/`explain`/`callers`) [[research_topics/agent_memory/Swarmvault/summary|Swarmvault]], three-channel lexical/vector/graph-proximity fusion at `search.hybrid_weight_graph` [[research_topics/agent_memory/SageWiki/summary|SageWiki]], and fused keyword/semantic/fuzzy-title ranking (RRF k=60) [[research_topics/agent_memory/VaultCurate/summary|VaultCurate]].
- New links never land silently: one inspected transaction bundle applied by a single orchestrator [[research_topics/agent_memory/ClaudeObsidian/summary|ClaudeObsidian]], `compile --approve` with `wiki/candidates/` staging and `lint --conflicts` [[research_topics/agent_memory/Swarmvault/summary|Swarmvault]], review-gated entity-resolution proposals and quarantined outputs [[research_topics/agent_memory/SageWiki/summary|SageWiki]], and suggestion-only Canvas links requiring an accept/dismiss verdict [[research_topics/agent_memory/VaultCurate/summary|VaultCurate]].
- Navigation structures are generated, not hand-drawn: Maps of Content, indexes, and Canvas/bases views [[research_topics/agent_memory/ClaudeObsidian/summary|ClaudeObsidian]], community detection with cluster queries [[research_topics/agent_memory/Swarmvault/summary|Swarmvault]] [[research_topics/agent_memory/SageWiki/summary|SageWiki]], and relation graphs, semantic paths, and MOC exports from Discover results [[research_topics/agent_memory/VaultCurate/summary|VaultCurate]].
- Time and staleness are modelled explicitly: freshness/review state in ledgers and `lint` for dead links, orphans, and stale indexes [[research_topics/agent_memory/ClaudeObsidian/summary|ClaudeObsidian]], freshness decay scoring with `freshness.defaultHalfLifeDays` [[research_topics/agent_memory/Swarmvault/summary|Swarmvault]], bi-temporal edges with contradiction invalidation and `as_of` point-in-time answers [[research_topics/agent_memory/SageWiki/summary|SageWiki]], and live Hot/Cold tiering from links plus recency [[research_topics/agent_memory/VaultCurate/summary|VaultCurate]].
- Aliasing and dedup are configurable, not automatic: plural-key frontmatter with aliases [[research_topics/agent_memory/ClaudeObsidian/summary|ClaudeObsidian]], user-definable relation vocabularies with review-gated merges and an opt-in LLM keep/fold/drop curation pass [[research_topics/agent_memory/SageWiki/summary|SageWiki]], and query-time synonym lists [[research_topics/agent_memory/VaultCurate/summary|VaultCurate]].

---
## What the sources agree on
- The vault is plain Markdown files first; the graph (ledgers, `graph.json`, ontology, index) is a derived companion layer, with raw sources kept immutable/content-addressed before synthesis.
- Links without provenance are untrustworthy: every source keeps unsupported, inferred, or contradictory claims visibly tagged rather than hiding them.
- Retrieval must combine similarity with structure: BM25/FTS plus embeddings plus graph traversal/proximity, with a deterministic fallback when models are unavailable.
- Graph writes are gated: staging areas, approval bundles, review queues, or explicit user verdicts stand between a proposed link and a canonical one.
- Local-first by default: core indexing, search, and linking run on-device with no API key; model/cloud calls are optional, explicit, and egress-consented.

## Where they differ
- Graph weight: Swarmvault and SageWiki build a persistent typed graph artifact (`state/graph.json`, `.sage/wiki.db` ontology) with traversal queries; ClaudeObsidian leans on ledgers plus file links/MOCs/Canvas; VaultCurate keeps no persistent graph at all — only ephemeral Canvas suggestions promoted to plain wikilinks.
- Automation posture: ClaudeObsidian serialises all shared mutation through one inspected transaction; Swarmvault/SageWiki use compile-pipeline staging and approval bundles; VaultCurate is suggestion-only and never edits notes automatically.
- Curation of identity: SageWiki makes entity resolution and concept dedup opt-in passes with explicit no-fold rules for enumerated entities; VaultCurate handles identity lightly via synonym lists; ClaudeObsidian via frontmatter aliases and filing-mode routing.
- Freshness model: SageWiki uses bi-temporal invalidation with `as_of` queries; Swarmvault uses decay scores and half-life config; VaultCurate derives Hot/Cold live from links plus recency; ClaudeObsidian reports staleness via lint against a declared UTC date.

## Evidence quality
- All claims are grounded in the per-source `summary.md`/`digest.md` pair only, which themselves cite file:line evidence from README-level pages and root-file manifests — no raw source or implementation code was read.
- Coverage is uneven: Swarmvault, SageWiki, and VaultCurate summaries each flag truncated chunks or missing `src/` internals pages, so CLI/behavior-level claims are stronger than engine-internals claims.
- No contradictions on the linking model itself; differences above are design choices (graph weight, gating mechanism, freshness math), not factual disputes.

## Sources in this sub-topic
| source | kind | what it contributes |
|---|---|---|
| ClaudeObsidian | fresh (summarise run) | Ledgers, filing modes, MOC/Canvas views, transaction-guarded linking, BM25 lint loop |
| Swarmvault | fresh (summarise run) | Typed `graph.json` with tagged edges, candidates/approvals, hybrid search plus traversal queries, Obsidian/Neo4j export |
| SageWiki | fresh (summarise run) | Opt-in evidenced graph (typed relations, triples, aliases, bi-temporal edges, communities), hybrid fusion, provenance queries, quarantined answers |
| VaultCurate | fresh (summarise run) | Suggestion-only discovery: fused search, Canvas relation graphs/semantic paths, verdict lifecycle, Hot/Cold rediscovery, synonym aliases |
