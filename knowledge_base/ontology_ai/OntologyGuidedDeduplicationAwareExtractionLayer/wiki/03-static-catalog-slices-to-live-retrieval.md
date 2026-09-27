> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Static Catalog Slices to Live Graph Retrieval
**In one sentence:** Static domain-level catalog slices wasted context (~17.7K tokens worst case), misrouted on filenames, and drifted from the live schema, so the pipeline replaced them with live content-conditioned Neo4j graph retrieval that injects only the ~700 relevant tokens (~94% / 16× reduction) under a PageRank-penalised, thresholded token budget.
## Key points
- Static selection was coarse and all-or-nothing at the domain level: the whole `catalog_<domain>.txt` was injected even when a document touched only a handful of its classes.
- Static routing was brittle keyword matching on filenames plus a ~2 KB content sample against a hand-curated vocabulary, misrouting opaque hashed filenames, multilingual content, and unanticipated synonyms.
- Static slices suffered maintenance drift: materialised text snapshots required rerunning `build_ontology_catalog.py` after every ontology edit and silently diverged between rebuilds.
- Static injection created budget pressure: whole domains cost ~17.7K tokens worst case (~11,200 tokens on the representative document), crowding document content in a 32K-token window.
- Live retrieval uses multi-span windowing (~1,500 chars, 300-char overlap, up to four windows) because a single vector over a multi-entity chunk collapses to a blended centroid.
- Each window queries a Neo4j vector index (`db.index.vector.queryNodes`) over class/predicate definition embeddings, scored as `score(c) = cos(q,c) × (1 − λ·pr(c))` with λ = 0.4 PageRank penalty, keeping classes with cosine ≥ 0.72 within a ~5,000-token budget (70% classes / 30% predicates).
- Retrieval is cached under content-hash + ontology-version hash (refreshed every ten minutes) with a 60-second circuit breaker that degrades to un-guided extraction, plus post-extraction `flag_novel_types()` marking for human-reviewed schema growth.
- Measured result on a representative document: ~11,200 → ~700 catalog tokens (~94% reduction, ~16× smaller, ~10,500 tokens reclaimed), where the retained tokens are content-nearest classes rather than a truncation of the slice.
---
## Limits of the static approach
**Covers:** pp. 7–8, static-slice limits leading into §4

- "• Coarse, all-or-nothing granularity. Selection was at the domain level: the entire slice was injected even when a document touched only a handful of its classes, spending context budget on irrelevant types."
- "• Brittle routing. Keyword matching depends on filename conventions and a hand-curated vocabulary; opaque hashed filenames, multilingual content, or unanticipated synonyms misroute the file and inject the wrong (or default) slice."
- "• Maintenance drift. The slice text files are a materialised snapshot. Every ontology edit requires rerunning build_ontology_catalog.py; between rebuilds the injected catalog silently diverges from the live schema."
- "• Budget pressure. Injecting whole domains (∼17.7 K tokens in the worst case) crowds out document content in a 32 K-token window."

## The current approach: live graph retrieval
**Covers:** pp. 7–8, §4 mechanism (ontology/graph_retriever.py, catalog_injection.py, context_composer.py)

> "We replace the static slice with live, content-conditioned retrieval of the ontology, in the spirit of retrieval-augmented generation [6] but targeting a formal class hierarchy rather than free text."

A curated ontology is materialised as a Neo4j graph in which every class and predicate carries a natural-language definition and a pre-computed embedding. At extraction time the relevant slice is fetched on demand and injected into the system prompt. Five elements:

1. Multi-span windowing — content sample split into overlapping windows (∼1,500 characters, 300-character overlap, up to four windows); per-window embeddings preserve local topicality.
2. Vector retrieval over class definitions — each window embedded and queried via Neo4j vector index (`db.index.vector.queryNodes`), returning candidate classes with cosine score, definition, alternative labels, and graph centrality.
3. PageRank-penalised scoring — down-weights high-centrality ancestors (Entity, Organization, Location):

   `score(c) = cos(q,c) × (1 − λ·pr(c)), λ = 0.4`

4. Dynamic cut-off under a token budget — every class above floor `min_score = 0.72` taken, then trimmed to ∼5,000 tokens (70% classes, 30% predicates); a 0.5 floor "admitted too many 'vaguely related' classes."
5. Version-keyed caching and circuit breaker — cache key combines content hash and ontology-version hash refreshed every ten minutes; if the graph is unreachable the circuit opens for sixty seconds and "extraction proceeds un-guided rather than blocking."

## Novel-type flagging
**Covers:** p. 7, grounding-as-steering

Grounding is steering, not a hard constraint: the prompt instructs the model to use a catalogue type where one fits and otherwise mark the emission as novel. After extraction, `flag_novel_types()` compares every emitted entity and relationship type against the full ontology vocabulary (after stripping pluralisation and wrapper suffixes such as `(records)`, `(entities)`) and sets `_novel_type` / `_novel_predicate` markers, surfacing candidates for human-reviewed ontology extension.

## Engineering note: dedicated event loop
**Covers:** p. 7

Because the Neo4j async driver and the embedding HTTP client bind to the event loop on which they are first used, the retriever runs coroutines on a single dedicated daemon event loop (`_run_coro` with a 15-second timeout) rather than `asyncio.run()` per extraction, avoiding "future attached to a different loop" errors from cached singletons.

## Impact and measured injection size
**Covers:** pp. 7–8, Fig. 2, Tables 1–2

Content-conditioned retrieval "injects only the handful of classes a document actually needs," the "grounding at extraction" stage for the rest of the pipeline. Fig. 2 flow: multi-span windowing + embedding → vector query → PageRank-penalised scoring → dynamic cut-off (≥ 0.72, ∼5k budget) → catalog block injected into extraction prompt → LLM extraction → novel-type flagging; Neo4j graph sits between columns with version cache + circuit breaker.

| Metric | Static slices | Graph retrieval | Change |
|---|---|---|---|
| Catalog tokens injected | ∼11,200 | ∼700 | −94% (∼16×) |
| Selection unit | whole domains + bridge | matched classes only | class-level |
| Irrelevant classes carried | many (domain padding) | none (thresholded) | eliminated |
| Context freed for content | — | ∼10,500 tokens | reclaimed |

Three reasons the reduction matters: (1) reclaimed ∼10,500 tokens let more source document share each call in the 32K window, reducing chunking and cross-chunk fragmentation; (2) a tighter catalog steers better, avoiding plausible-but-wrong neighbouring types; (3) cost per call drops with tokens removed. "Crucially, the smaller block is not a truncation of the larger one: the ∼700 retained tokens are precisely the classes the content embeds closest to."

| Dimension | Static catalog slices (earlier) | Live graph retrieval (current) |
|---|---|---|
| Granularity | Domain-level: whole `catalog_<domain>.txt` injected | Class/predicate-level: only matched classes |
| Selection signal | Filename + ∼2 KB content keyword match | Per-window embedding similarity over class definitions |
| Relevance ranking | None (all-or-nothing) | Cosine, PageRank-penalised, thresholded at 0.72 |
| Freshness | Requires rebuilding slice files; drifts | Always current; cached by ontology-version hash |
| Token cost | Whole domain(s); worst case ∼17.7K tokens | Bounded budget of relevant classes (∼5K) |
| Failure mode | Misroutes opaque filenames/synonyms; over-injection | Degrades to un-guided extraction via circuit breaker |

Leads into §4.1: the Fig. 2 mechanism retrieves the right neighbourhood, but evaluation on intelligence-domain documents exposed systematic precision gaps (classes that should have been injected fell out, or injected classes were insufficiently specific), each traced to one baseline design decision with a targeted refinement.
