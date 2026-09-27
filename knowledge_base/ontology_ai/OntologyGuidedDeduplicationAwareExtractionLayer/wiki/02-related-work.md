> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Related Work: LLMs for Knowledge Graph Construction
**In one sentence:** Prior LLM-based knowledge-graph work (zero-shot, NER-style, generative and revisited relation extraction) consistently hits fragmented type vocabularies, hallucinated relations, and description-over-relation bias, so the paper claims its contribution is not a new extraction model but an architecture that constrains and repairs a stock model's output via ontology-slice retrieval, rule-based plus embedding entity resolution, and a two-phase quality-gated chunked pipeline with JSON/error recovery, evolving from static catalog slices toward live graph retrieval.
## Key points
- LLM KG population via zero-shot prompting [13], NER-style prompting [14], generative end-to-end relation extraction [15], and revisited relation extraction [16] — building on Transformer [11] and few-shot prompting [12] — consistently reports fragmented type vocabularies, hallucinated relations, and bias toward entity description over relation extraction.
- Ontology grounding treats an ontology as "a formal specification of a shared conceptualisation" [17] to keep the emitted type vocabulary coherent; the paper retrieves the relevant ontology slice by embedding similarity and injects it into the extraction prompt, applying a centrality penalty to generic classes adapted from PageRank [18].
- Retrieval augmentation follows RAG [6] (conditioning generation on retrieved free text) but applied to a formal class hierarchy, and the claimed-novel combination is live graph retrieval plus subclass expansion plus predicate full-text search for extraction-time grounding.
- Entity resolution spans Fellegi–Sunter probabilistic record linkage [19], the broad field [20, 7], blocking surveys [8], Magellan [21] to transformer matchers [22], plus classical strands: personal-name abbreviation [23], string metrics [24, 25], Jaro–Winkler [26] (used by the paper's scorer), phonetic codes [27], cross-lingual matching [10, 28], entity linking/disambiguation contextual evidence [29, 30], and dense sentence representations [31].
- The paper's resolution design pairs six rule-based algorithms requiring no training data at zero inference cost with an embedding layer using the canonical blocking–matching pipeline guarded by a hard-conflict rule no similarity score can override.
- Extraction is split into two LLM calls because LLMs prioritise entity descriptions over relationships [16]: Phase 1 extracts entities plus preliminary relationships (zero-shot [13, 14]), Phase 2 re-reads text with the entity catalog for relationships including temporal/contextual qualifiers, consolidated by qualifier-preserving deduplication before Phase 3 enhancement.
- The relationship second pass is protected by a ratio skip ("if |ρ| ≥ 50, skip the second pass") plus a four-check quality gate (financial connectivity, FUND|BUDGET|APPROV labels, person-relation diversity, type concentration) with auditable (should_force, reasons) logging, alongside format-specific chunking (PDF pages vs 8,000-char/1,000-overlap text) and three-stage JSON plus fallback recovery.
---
## LLMs for knowledge graph construction
Since the Transformer [11] and few-shot prompting [12], work demonstrates LLMs can populate knowledge graphs directly from text [3, 4] through:

| Approach | Citation |
|---|---|
| Zero-shot prompting | [13] |
| NER-style prompting | [14] |
| Generative end-to-end relation extraction | [15] |
| Revisited relation extraction | [16] |

Reported failure modes the system confronts in production: fragmented type vocabularies, hallucinated relations, and bias toward entity description over relation extraction. Positioning quote: "Our contribution is not a new extraction model but an architecture that constrains and repairs a stock model's output at every stage."

## Ontology grounding and retrieval augmentation
An ontology is "a formal specification of a shared conceptualisation" [17]; grounding extraction in such a schema keeps the emitted type vocabulary coherent. Retrieval-augmented generation [6] conditions generation on retrieved free text; here the same principle is applied to a formal class hierarchy — retrieving the relevant ontology slice by embedding similarity and injecting it into the extraction prompt. The centrality penalty on generic classes adapts PageRank [18]. Novelty claim: "To our knowledge the combination of live graph retrieval, subclass expansion, and predicate full-text search for extraction-time grounding has not been described before."

## Entity resolution and name matching
Lineage and components named in the chunk:

| Strand | References |
|---|---|
| Probabilistic record-linkage theory (Fellegi and Sunter) | [19] |
| Broad field | [20, 7] |
| Blocking surveys | [8] |
| Learned matchers, Magellan to transformer-based | [21], [22] |
| Personal-name abbreviation | [23] |
| String-metric comparisons | [24, 25] |
| Jaro–Winkler measure (used by the paper's scorer) | [26] |
| Phonetic codes | [27] |
| Cross-lingual matching | [10, 28] |
| Entity linking/disambiguation contextual-evidence principle | [29, 30] |
| Dense sentence representations for semantic similarity | [31] |

Design contrast stated in chunk: "Unlike learned matchers, our six rule-based algorithms require no training data and run at zero inference cost, while the embedding-based layer adopts the canonical blocking–matching pipeline with a hard-conflict guard that no similarity score can override."

## System overview (as present in this chunk)
The extraction layer runs as a real-time Kafka consumer receiving document metadata from upstream ingestion, resolving either file-based records (metadata pointers to files on disk) or database-embedded records (full text inline), normalising both into one internal representation. Consumer configuration, session-timeout tuning, and parallelism are noted as operational (Appendix B), not scientific.

### Two-phase extraction pipeline
Because "LLMs tend to prioritise entity descriptions over relationships [16]", extraction is split: Phase 1 extracts entities and preliminary relationships in the zero-shot paradigm [13, 14]; Phase 2 re-reads the text alongside the extracted entity catalog and focuses solely on relationships, including temporal and contextual qualifiers. Outputs are consolidated by qualifier-preserving deduplication (Fig. 11), then Phase 3 post-extraction enhancement (Figs. 7–10) refines entity data.

### Quality-gated relationship second pass
Verbatim skip rule: "if |ρ| ≥ 50, skip the second pass". The chunk notes this ratio logic can false-trigger when relationships concentrate on one type or whole relation families are structurally absent, so a four-check gate precedes the skip decision:

1. **Financial connectivity.** Financial entities present alongside non-financial ones but zero cross-type relationships → force second pass (financial nodes as funding sources the LLM failed to connect).
2. **Financial relation types.** Even with cross-type edges, no label matching `FUND|BUDGET|APPROV` (case-insensitive) → force (catches non-standard labels evading the edge check).
3. **Person relation diversity.** With ≥ 8 persons, fewer than 4 non-`REPORTED_TO` person relationships → force; prevents the "all roads lead to REPORTED_TO" collapse of all inter-person links into one structural type.
4. **Relationship type concentration.** More than 30% of relationships share a single type and fewer than 6 distinct types present → force (shallow extraction over-indexed on the most frequent signal).

The gate returns a `(should_force, reasons)` pair with logged reasons for auditability; it complements the count threshold (e.g. 60 relationships of only `REPORTED_TO` clears the raw count but still triggers checks 3 and 4).

### Chunk-based extraction and merging
Partitioning respects LLM context limits, differing by content type:

| Content type | Chunking (defaults) |
|---|---|
| PDF and OCR text | Pages grouped into fixed-size windows (default `chunk_pages=5`, one-page neighbour overlap each side) |
| Plain text and database records | Character-range chunking (default 8,000-char chunks, 1,000-char overlap) |

Each text chunk carries the verbatim overlap annotation "Primary target chars: 𝑠–𝑒. Overlap chars: 1000.", telling the model it sees partially replicated context so it recognises continuation instead of treating overlap as a novel section and re-extracting entities or re-inventing edges. Merging: entities merged on a canonical key, relationship references remapped to canonical IDs, Phase 3 enhancements applied to the consolidated set so per-chunk name variations propagate document-wide.

### Robustness and error recovery
JSON repair handles closed fences (```json ... ```) and unclosed/truncated fences via three-stage recovery: closed-fence extraction → open-fence extraction → raw JSON search, yielding maximum recoverable structure instead of hard failure. On relationship-call failure from entity-count overflow, a simplified fallback retries with top-20 entities and a capped 30,000-character evidence window for partial coverage. Unrecoverable chunk errors (e.g. context-window overflow on the local vLLM endpoint) append self-contained JSONL records to `extraction_failures.jsonl`, keyed by file path, object ID, stage, and failed chunk/page indices, written under a module-level mutex; documents re-run as a batch without full-corpus rescan. Phase 3 algorithms degrade gracefully (e.g. duplicate detection proceeds at adjusted confidence when properties are missing).

## Ontology-guided extraction via live graph retrieval (opening; chunk cuts off mid-discussion)
The stated problem with un-guided extraction: a general-purpose LLM invents its type vocabulary per document and per chunk — the same class surfacing as `GovBody`, `Government Organization`, `Govt. Agency`, and `Ministry`, with relationship labels proliferating likewise — fracturing the downstream schema for ontology-conformant querying. The fix is constraining the model by injecting relevant ontology classes and predicates into the prompt; the design question is which slice to inject and how, evolving from static slices to live graph retrieval.

First approach — static catalog slices: offline build (`build_ontology_catalog.py`) emitted one prompt-ready file per domain (`catalog_cdr.txt`, `catalog_south_asia.txt`, cross-domain `catalog_bridge.txt` with shared predicates `HAS_PHONE`, `LOCATED_IN`, …; full `catalog_full.txt` for inspection). Read-side loader (`catalog_loader.py`) memoised slices and estimated size with a chars/4 token heuristic against a ~20,000-token soft budget (worst routed case of three domains plus bridge ≈ 17,700 tokens). Selection used a deterministic router (`file_router.py`) with a three-tier keyword decision tree over a curated domain-unique vocabulary:

1. Strong filename match (domain keyword in filename, e.g. `07_cdr_data.csv` → cdr): trust filename, skip content scan.
2. Weak filename match (ambiguous single hit): read a ~2 KB content sample, combine filename and content signals.
3. No filename match: scan content only; if inconclusive, fall back to bridge plus a broad regional slice.

Chosen slices were concatenated into the system prompt, with a `FORCE_CATALOG_SLICES` override for testing. The chunk states this bounded the vocabulary and improved predictability but "carried structural limitations:" — the sentence is cut off at the chunk boundary, so limitations belong to the next chunk's page.

**Covers:** §2 Related work through §4 opening (static catalog slices; chunk ends mid-sentence at "structural limitations:")
