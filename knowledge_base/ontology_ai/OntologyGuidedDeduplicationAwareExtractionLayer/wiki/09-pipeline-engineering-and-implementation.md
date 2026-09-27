> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Pipeline Engineering and Implementation
**In one sentence:** The implementation combines zero-extra-LLM-cost linguistic, alias, and deduplication enhancements (lifting search recall from ~70% to 95% without false merges) with an optional five-stage embedding-based resolution layer and a five-stage extraction pipeline whose per-chunk cleaning and relationship second pass were fixed after empirical evaluation.
## Key points
- System integrates domain-specific linguistic patterns (e.g. Slavic suffixes), multi-source alias discovery, context-aware deduplication, and per-page PDF routing via a six-signal OCR classifier (Fig. 5) with zero additional LLM inference cost.
- Search recall rises from roughly 70% to 95% while preventing false merges by prioritising relationship metadata.
- Per-page OCR classification eliminates information loss from binary PDF routing, and configurable LLM provider switching enables seamless local-to-cloud model transitions.
- Embedding resolution (resolution/) runs as an optional post-extraction stage, disabled by a single configuration flag, following the blocking–matching pipeline [7, 8] and Magellan/DeepMatcher learned-matching tradition [21, 22].
- Candidate pairs come from the union of FAISS inner-product cosine top-k (k = 20) over ℓ2-normalised vectors and a Double Metaphone phonetic block, avoiding O(n²) all-pairs comparison.
- Each pair gets a seven-signal weighted score (0.25 name, 0.20 embedding cosine, 0.15 property overlap, 0.10 phonetic, 0.10 type compatibility, 0.10 alias cross-match, 0.10 source proximity), with property conflicts penalised at twice agreement weight.
- Decision thresholds route pairs to auto-merge (≥ 0.85), manual review (0.60–0.85), codename-candidate (≥ 0.50 with codename pattern), or distinct, but a hard-conflict guard on discriminator keys (date of birth, nationality, gender, passport or employee number) forbids merging regardless of score.
- Five-stage pipeline (chunked LLM extraction → per-chunk finalization → cross-chunk merging → relationship second pass → post-extraction enhancement) uses 5-page chunks with 1-page overlap on each side plus two sequential per-chunk LLM calls, after an `_env_int()` bug (`max(1, 0)`) truncated relationship-prompt source text to one character and produced zero per-chunk relationships.
---
## Key contributions
**Covers:** Opening contribution statement; Figs. 5, 14–15; Section 7.3; Section C

> "Key Contributions. This implementation advances knowledge graph extraction through the integration of domain-specific linguistic pattern recognition (e.g., Slavic suffixes), multi-source alias discovery, robust context-aware deduplication, and intelligent per-page PDF routing via a six-signal OCR classifier (Fig. 5)."

- Enhancements execute "without incurring additional LLM inference costs" while "prioritizing relationship metadata".
- Search recall rises "from roughly 70% to 95% while preventing false merges".
- "The per-page OCR classification eliminates information loss from binary PDF routing, and the configurable LLM provider switching enables seamless transitions between local and cloud models."
- "The empirical quality analysis (Section 7.3) and issues catalogue (Section C) further demonstrate the necessity of a defense-in-depth approach combining upstream data cleaning, intelligent document routing, and downstream entity enrichment."

## Embedding-based entity resolution — motivation
**Covers:** Section 6.5, Motivation; Section 6.2; refs [7, 8, 21, 22]

> "The six rule-based algorithms of Section 6.2 resolve name variation deterministically and at zero LLM cost, but they reason primarily over surface strings and a few context fields."

- Gap: rule-based layer "do[es] not capture semantic similarity between mentions whose surface forms diverge yet whose surrounding descriptions agree, and their pairwise comparison is quadratic in the number of entities."
- Answer: "a complementary embedding-based resolution subsystem (resolution/) that follows the canonical blocking–matching pipeline of the entity-resolution literature [7, 8] and the learned-matching tradition of Magellan/DeepMatcher and transformer-based matchers [21, 22]."
- Deployment: "It runs as an optional post-extraction stage and is disabled by a single configuration flag when not required."

## Resolution pipeline — five stages
**Covers:** Section 6.5, Pipeline (embed, block, score, decide, collect); Fig. 14

> "The resolution engine executes five stages (embed, block, score, decide, collect)."

- 1. Embed: "Each entity is rendered to a short descriptive string (name, type, salient properties, aliases) and embedded." Within-document resolution uses "a deterministic hash-seeded pseudo-embedder (no API calls)"; cross-document resolution uses "the ontology-tuned embedding model Konect-U/Qwen3-Embedding-0.6B-Ontology, served behind a swappable provider interface (vLLM, a text-embedding-inference server, or Gemini)".
- 2. Block: "To avoid the O(n²) all-pairs comparison, candidate pairs are generated by the union of two blocking strategies [8]: a FAISS [33] inner-product index over ℓ2-normalised vectors (cosine top-k, k = 20), and a phonetic block that groups entities sharing a Double Metaphone [27] fingerprint." The union "recovers both semantically and orthographically near pairs."
- 3. Score: "a weighted multi-signal score combining name similarity (0.25), embedding cosine (0.20), property overlap (0.15), phonetic match (0.10), type compatibility (0.10), alias cross-match (0.10), and source proximity (0.10)." "Property conflicts are penalised at twice the weight of property agreements, and type compatibility recognises synonym families (person/individual/officer, organization/agency, location/place)."

| Signal | Weight |
|---|---|
| Name similarity | 0.25 |
| Embedding cosine | 0.20 |
| Property overlap | 0.15 |
| Phonetic match | 0.10 |
| Type compatibility | 0.10 |
| Alias cross-match | 0.10 |
| Source proximity | 0.10 |

- 4. Decide: "≥ 0.85 ⇒ auto-merge; 0.60–0.85 ⇒ manual-review; ≥ 0.50 with a codename pattern ⇒ codename-candidate; otherwise distinct."

| Score | Action |
|---|---|
| ≥ 0.85 | Auto-merge |
| 0.60–0.85 | Manual review |
| ≥ 0.50 with codename pattern | Codename-candidate |
| Otherwise | Distinct |

- Hard-conflict guard: "if two entities carry differing values on a discriminator key (date of birth, nationality, gender, passport or employee number) they are never merged, however similar their names, which directly prevents the "Elena Petrov vs. Elena Petrova" class of false merge."
- 5. Collect: "returns merged entities, a canonical-ID mapping, per-decision provenance records, and the items flagged for human review; a file-backed store persists this metadata alongside the extraction output for audit and for cross-document resolution on subsequent runs."
- Fig. 14: "Entities are embedded and blocked by the union of a FAISS cosine index and a Double Metaphone phonetic block; each candidate pair is scored by a weighted combination of seven signals; a decision engine routes the pair to auto-merge, manual review, or distinct under tunable thresholds. A hard-conflict guard on discriminator attributes overrides the score and forbids merging regardless of name similarity."

## Relationship to the rule-based layer
**Covers:** Section 6.5, Relationship to the Rule-Based Layer; Fig. 14

> "The two layers are complementary rather than redundant: the rule-based algorithms run first and cheaply collapse obvious surface variants and expand aliases, while the embedding layer catches semantically equivalent mentions that survive string matching and does so under blocking to remain tractable at scale."

- "Both feed the same review queue, and the hard-conflict guard ensures the more aggressive embedding layer cannot override discriminating evidence."

## Five-stage pipeline architecture
**Covers:** Section 7, Section 7.1; Figs. 15–20

> "Fig. 15 illustrates the complete five-stage extraction pipeline, showing the flow from raw document input through LLM extraction, data cleaning, cross-chunk merging, relationship enrichment, and post-extraction entity enhancement."

- Flow: "raw document input through LLM extraction, data cleaning, cross-chunk merging, relationship enrichment, and post-extraction entity enhancement"; "A document enters at the left and flows strictly left to right through chunked LLM extraction, deterministic per-chunk cleaning, cross-chunk merging, a relationship second pass, and post-extraction enhancements, emerging as a validated knowledge graph."
- Colour coding: "Stages 2 and 3 (highlighted in orange and purple) represent the data cleaning fixes introduced after empirical evaluation (Section 7.3), while Stage 5 (red) encompasses the six core deduplication algorithms detailed in Section 6.2."
- Detail figures: "Numbered badges key each stage to its detail figure (Figs. 16–20)."
- "The extraction pipeline transforms raw documents into a validated JSON knowledge graph through five sequential stages. Each stage addresses a distinct class of data-quality concern, from initial LLM extraction through normalisation, deduplication, cross-chunk relationship discovery, and post-extraction enrichment."

## Stage 1 — LLM extraction
**Covers:** Section 7.1, Stage 1; Fig. 16; chunk_pages=5, overlap 1

> "Stage 1: LLM Extraction. The pipeline begins by splitting the input document into overlapping chunks of five pages each, with one page of overlap on each side to preserve cross-page context."

- Two sequential LLM calls per chunk:
  - 1. Entity Extraction: "the LLM identifies named entities (persons, organisations, locations, equipment) together with their properties and provisional aliases."
  - 2. Relationship Extraction: "a second, dedicated LLM call receives the full entity catalog extracted so far plus the raw chunk text, and returns typed relationships with qualifiers and evidence spans."
- Infrastructure bug: "the helper function _env_int() used max(1, 0) instead of the configured context-window size, truncating the source text fed to the relationship prompt to a single character and producing zero per-chunk relationships."
- Fig. 16: "The document is split into overlapping chunks; two sequential LLM calls extract entities and relationships per chunk. The dashed annotation marks a critical infrastructure bug where _env_int() defaulted the context window to one character, suppressing all per-chunk relationships."
- Parameters: `chunk_pages=5, overlap neighbor=1`.

## Stage 2 — Per-chunk finalization
**Covers:** Section 7.1, Stage 2; Fig. 17

> "Stage 2: Per-Chunk Finalization. Before merging results across chunks, three deterministic cleaning passes are applied to each chunk's output."

| Pass | Mechanism | Example from chunk |
|---|---|---|
| Normalise relationship types | UPPER_SNAKE_CASE conversion + typo correction | infiltrated → INFILTRATED, surveiled → SURVEILLED |
| Remove self-referencing relationships | Filter source == target loops | per_001 → per_001 × |
| Correct entity type misassignment | Name-pattern-based type inference | 'Leviathan Submarine' Person → Equipment |

- Fig. 17: "Three deterministic cleaning passes normalise relationship types, remove self-loops, and correct entity type misassignments before cross-chunk merging."
- Note: chunk text ends mid-Stage-2; Stages 3–5 internals are not in this chunk.
