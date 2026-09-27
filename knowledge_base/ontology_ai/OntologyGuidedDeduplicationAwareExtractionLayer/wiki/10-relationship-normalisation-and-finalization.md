> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Relationship normalisation and finalization
**In one sentence:** The pipeline normalises free-form LLM outputs, merges cross-chunk entities under canonical keys and uniform IDs, runs a second LLM pass for cross-chunk relationships, enriches the graph with aliases and scored dedup candidates, and emits a validated JSON knowledge graph.
## Key points
- Relationship-type normalisation converts free-form LLM labels into a controlled UPPER_SNAKE_CASE vocabulary and corrects misspellings such as surveiled → SURVEILLED.
- Self-loop removal deletes relationships where source and target are identical, described as an artefact of LLM hallucination.
- Entity-type correction uses name-pattern heuristics, e.g. reassigning "Leviathan Submarine" from Person to Equipment based on the suffix keyword "Submarine".
- Stage 3 cross-chunk merging strips titles ("Colonel", "Dr.", "Agent") to form canonical keys such as 'Colonel Mario Chavez' → 'Mario Chavez', merges properties/aliases with relationship ID remapping, and reassigns heterogeneous IDs (per1, per1_2, per_087) to a uniform per_001, org_001, loc_001, eqp_001 scheme.
- Stage 4 relationship second pass batches the full entity catalog into batches of up to 80 entities (at most 8 batches), prompts the LLM for evidence-grounded cross-chunk relationships, and deduplicates by the composite key (source, target, type) with qualifier merging per Fig. 11.
- Stage 5 post-extraction enrichment runs alias expansion (e.g. 'Elena Petrov' → 'E. Petrov', 'Elena P.', 'EP', 'E.P.'), PDF text mining for spelling variants ('Jon' when 'John' was extracted), multi-tier similarity scoring, and context-aware dedup; a first-letter-only abbreviation bug produced 79 false positives before correction.
- Final output is a single validated JSON graph with normalised entities, typed evidence-linked relationships, and scored dedup candidates (same_person, different_people, uncertain), exemplified by per_001 with six aliases and a 0.929 similarity to per_002 overridden by conflicting role/org context on a 45-page report yielding 579 entities and 540 relationships.
---
## Output cleanup: normalisation and hallucination filters
> "Relationship-type normalisation converts free-form LLM relationship labels into a controlled UPPER_SNAKE_CASE vocabulary and corrects common misspellings (e.g. surveiled → SURVEILLED)."

1. Relationship-type normalisation as quoted above.
2. "Self-loop removal filters out relationships where the source and target entity are identical, an artefact of LLM hallucination."
3. "Entity-type correction uses name-pattern heuristics to fix misclassified entities. For example, an entity named "Leviathan Submarine" initially typed as Person is reassigned to Equipment based on the suffix keyword "Submarine"."

## Stage 3 — Cross-chunk merging (Fig. 18)
> "Title-aware normalisation produces canonical keys; entities sharing the same key are merged with property and alias unification; finally, all IDs are reassigned to a consistent scheme."

1. Title-aware name normalisation: "strips honorifics and titles ("Colonel", "Dr.", "Agent") to produce a canonical key. This prevents the same person from appearing under both "Colonel Mario Chavez" and "Mario Chavez"."
2. Chunk-result merging: "groups entities by canonical key and merges their properties, aliases, and associated relationships. Relationship source/target IDs are remapped to the merged entity."
3. Consistent ID reassignment: "replaces the heterogeneous IDs produced by per-chunk extraction (per1, per1_2, per_087) with a uniform <type>_<seq> scheme" — "per_001, org_001, loc_001, eqp_001" and "per1, per1_2, per_087 → per_001, per_002, per_003".

## Stage 4 — Relationship second pass (Fig. 19)
> "Per-chunk extraction can only discover relationships whose participants co-occur within a single chunk. Stage 4 performs a second LLM pass over the merged entity catalog to discover cross-chunk relationships."

- Batching: "the full entity catalog is partitioned into batches of up to 80 entities (at most 8 batches) to stay within context-window limits" — diagram labels "batch_size=80, max_batches=8".
- Cross-chunk LLM extraction: "each batch is sent to the LLM alongside the source text, requesting evidence-grounded relationships between entities that may have originated from different chunks."
- Relationship deduplication: "newly discovered and previously existing relationships are deduplicated by the composite key (source, target, type), with qualifier fields merged using Fig. 11" — diagram notes "Qualifier-aware merging by (source, target, type)".

## Stage 5 — Post-extraction enhancements (Fig. 20)
> "The final stage enriches the knowledge graph with alias information and deduplication candidates through four algorithms."

| Algorithm | Mechanism in chunk | Exact example / number |
|---|---|---|
| Alias Expansion (Fig. 7) | "deterministically generates abbreviations and name variants ... to increase recall during downstream entity linking" | "'Elena Petrov' → 'E. Petrov', 'Elena P.', 'EP', 'E.P.'" |
| PDF Text Mining (Fig. 8) | "performs fuzzy matching against the raw source text to discover spelling variants that the LLM normalised away" | "Discovers 'Jon' when 'John' was extracted" / "(e.g. "Jon" vs. "John")" |
| Similarity Scoring (Fig. 9) | "computes a multi-tier similarity score between all entity-name pairs using exact matching, Slavic gender-suffix handling, abbreviation detection, and sequence alignment" | "'Petrov' vs 'Petrova' → 0.85 slavic_gender_suffix"; "A bug in the abbreviation check, which required only a first-letter match, produced 79 false positives before correction" |
| Context-Aware Dedup Detection (Fig. 10) | "validates high-similarity pairs against contextual evidence (role, organisation, location) to distinguish true duplicates from distinct entities who share a name" | "Same name + different org → 'different_people'" |

## Validated output and example record (Figs. 21–22, §7.2)
Pipeline output (Fig. 21): "a validated JSON knowledge graph containing typed entities, evidence-linked relationships, and scored deduplication candidates ready for downstream analysis." After all five stages:

- "Entities with normalised names, consistent IDs, merged properties, and expanded alias sets."
- "Relationships with typed labels, qualifier metadata, and evidence spans linking back to the source document."
- "Deduplication candidates scored by similarity and annotated with context-aware verdicts (same_person, different_people, uncertain)."

Example (§7.2): "the person per_001 carries six aliases discovered by three different mechanisms, is linked to his employer by a qualified relationship, and is connected to the similarly named per_002 only by a dashed dedup edge: the 0.929 name similarity was overridden by conflicting context (different roles, different organisations), so the two remain distinct people."

- Aliases: "John Doe (LLM, × 3)", "Jon Doe (text mining, × 2)", "J. Doe (alias expansion)", plus display variants "J Doe", "JD", "John D."
- Relationship: "John Doe per_001 EMPLOYED_BY Vector Glass Industries org_001 {date: 2024-06-15, location: London HQ}".
- Dedup edge: "similarity 0.929 (spelling variant)" with "context conflict ⇒ kept distinct"; per_001 context "role: Procurement Engineer, org: Vector Glass Industries, dedup_status: confirmed_unique" vs per_002 "John Doe ... role: Logistics Clerk, org: Khamsin Institute".
- Fig. 22 caption note: "the pair is exported in dedup_candidates for audit rather than silently merged."

## Empirical setup and next defect (§7.3–§7.3.1)
> "While the six core deduplication algorithms (Section 6.2) address entity-level name variation and relationship deduplication, empirical evaluation on a 45-page intelligence report (IR-001.pdf, yielding 579 entities and 540 relationships) revealed a critical infrastructure bug together with six data-quality issues originating from LLM output inconsistencies."

- These issues "persisted despite the existing algorithms because they occur upstream, in the raw LLM output, the chunk merging logic, or the utility infrastructure, before the deduplication algorithms execute."
- "The architectural placement of these fixes within the pipeline is illustrated in Fig. 15 (Stages 2–3)."
- §7.3.1 opens: "Issue. All per-chunk relationship extractions (Phase 2) returned zero relationships despite the LLM receiving 23–134 entities per chunk."

**Covers:** Chunk pp. 27–30: output-cleanup rules through Stages 3–5 (Figs. 18–21), §7.2 example record (Fig. 22), §7.3 setup and §7.3.1 opening (Table 11).
