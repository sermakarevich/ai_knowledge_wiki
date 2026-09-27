> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Predicate Recovery and Prompt Guards — Metric Baseline vs Refined (G5)

**In one sentence:** Subclass-aware refined retrieval (G5) lifts predicate recovery from 3 tangential predicates to 68 with complete hierarchy coverage, and three deterministic ontology-grounded guards — prompt fan-out restraint, rank-guarded orientation, and vocabulary canonicalization with novel flagging — make emitted relationships conform to the schema.

## Key points
- Predicate retrieval jumps from 3 (baseline, exact-label) to 68 (refined, subclass-aware G5): baseline surfaced only tangential predicates while refined surfaces the full command-hierarchy family.
- Hierarchy-family coverage goes from none at baseline to complete under G5, with refined predicates including subordinate to, commands, part of, reports to, under command, has subordinate formation, commanded by, and deployed under command of.
- A 9B local model still over-emits, mislabels, and mis-orients relationships despite good retrieval, so three guards close the gap: one at the prompt and two at finalization, composing as "retrieval steers, the prompt restrains, finalization enforces."
- The prompt fan-out guard collapsed a 2 × 58 Cartesian grid (116 CLAIMED_BY edges, 45% of the document) to 1 edge, cutting total relationships from 258 to 112 and most-concentrated predicate share from 45% to 16%.
- Rank-guarded orientation canonicalizes inverse/downward phrasings (has subordinate formation, commands) into upward subordinate to with endpoints swapped, re-orienting by coarse tier (Command/Corps > Division > Brigade > Battalion/Regiment) on organisation↔organisation edges only.
- Vocabulary canonicalization snaps emitted predicates to 954 ontology object-property label/alt-label keys via exact, de-pluralised, then embedding-cosine tiers with a 0.80 floor, leaving non-matches verbatim as _novel_predicate flagged unknown_predicate for admin-panel review.
- Running canonicalization at extraction before ingest lets the relationship-deduplication key (source, target, type) collapse variants such as CAPTURED_LOCATIONS (×14) and CAPTURED_LOCATION (×9) into a single qualifier-merged edge.

---

## Predicate retrieval: baseline vs refined

| Metric | Baseline (exact-label) | Refined (subclass-aware, G5) |
|---|---|---|
| Predicates retrieved | 3 | 68 |
| What surfaced | assigned to command, assigned to air force command, has joint operational area (all tangential) | subordinate to, commands, part of, reports to, under command, has subordinate formation, commanded by, deployed under command of, … |
| Hierarchy family present | none | complete |

## From retrieval to canonical relationships: prompt guards and finalization conformance

> "The retrieval refinements of Section 4.1 put the right ontology classes and predicates in front of the model, but a 9B local model is not bound by what it is shown: it still over-emits relationships, mislabels predicates, and mis-orients them."

Three deterministic, ontology-grounded guards downstream of retrieval (one at the prompt, two at finalization) make emitted relationships conform to the schema regardless of model discipline. They are the relationship-side analogue of the entity canonical_iri mapping (which the tagger applies to entity types but not to predicates).

## Over-extraction: the fan-out guard

Asked to "find ALL relationships," the model templates a pattern across every plausible entity pair: on an intelligence document about disputed territory it emitted a perfect 2 × 58 Cartesian grid (each of two armies "claiming" every one of 58 places), 116 edges (45% of the document) from only two distinct sources, all sharing a single predicate and pointing in the inverted direction.

The driver was the prompt itself: a licence to extract "ANY … strongly implied connection" plus a fan-out guard scoped only to reporting verbs. Two minimal edits — replacing "strongly implied" with "explicitly stated in the text" and generalising the fan-out guard to any relation type with an explicit no-grid clause — collapsed it. This guard is prompt-level and probabilistic: it sharply reduces rather than provably eliminates the pattern on a small model, so the finalization guards do not depend on it.

Table 6: Relationship over-extraction before and after the prompt fan-out guard:

| Metric | Before | After |
|---|---|---|
| CLAIMED_BY edges (a 2 × 58 grid) | 116 | 1 |
| Total relationships | 258 | 112 |
| Most-concentrated predicate share | 45% | 16% |
| Distinct predicate types | 63 | 29 |

## Direction: rank-guarded orientation

Asymmetric hierarchy predicates (subordinate to, part of, commands) carry fixed semantic direction, but the model orders source/target inconsistently: the same corpus yielded both "NLI subordinate to FCNA" (correct) and "FCNA subordinate to NLI" (inverted), plus the inverse predicate has subordinate formation pointing the wrong way. Because no pipeline stage ever swaps endpoints, a reversed edge is preserved into the graph and narrated back as a contradiction.

The guard canonicalises the predicate label (folding inverse forms such as has subordinate formation and commands into upward subordinate to with endpoints swapped) then re-orients by ontology rank: for an upward predicate the source must be the junior formation, with rank a coarse tier read from the entity name (Command/Corps > Division > Brigade > Battalion/Regiment). It fires only on organisation↔organisation edges, leaving person-role edges (commander of) untouched.

Table 7: every phrasing of the FCNA/NLI hierarchy converges to one canonical edge:

| Model emits | After conformance |
|---|---|
| FCNA -[subordinate to]-> NLI (flipped) | NLI -[subordinate to]-> FCNA |
| NLI -[has subordinate formation]-> FCNA (inverse) | NLI -[subordinate to]-> FCNA |
| FCNA -[commands]-> NLI (downward) | NLI -[subordinate to]-> FCNA |
| NLI -[subordinate to]-> FCNA (already right) | NLI -[subordinate to]-> FCNA |

## Vocabulary: ontology-grounded canonicalization with novel flagging

The tagger maps entity types to ontology classes but leaves relationship predicates untouched (validating only domain/range), so variants proliferate: one document carried CAPTURED_LOCATIONS (×14) and CAPTURED_LOCATION (×9) as two distinct edge types the tagger would not merge.

The guard snaps each emitted predicate to the ontology object-property vocabulary (954 label/alt-label keys loaded once from the ontology graph) by tiered match: exact, then de-pluralised (CAPTURED_LOCATIONS→CAPTURED_LOCATION), then embedding cosine against predicate embeddings. The embedding tier floor is 0.80: below ≈ 0.80, generic upper-ontology predicates (may-be-detected-by, attack-may-be-countered-by) act as "semantic magnets," so only near-certain synonyms (observed by→observed-by-at-some-time) snap and everything else stays verbatim. Unmatched predicates are marked _novel_predicate and flagged unknown_predicate by the post-ingest validator for review in the admin panel, where they can be promoted into the ontology. Running at extraction before ingest means the dedup key (source, target, type) sees canonical types, collapsing the 14 + 9 variants into one qualifier-merged edge.

## Tail: start of multi-format handling (Section 5)

The chunk tail opens Section 5: the consumer routes by MIME type and file extension onto the same two-phase extraction and finalisation backend — XLSX via deterministic plan-then-execute (one LLM call per workbook template: bounded sample, typed ExtractionPlan with ColumnMaps, deterministic execution with coercion and coverage warnings), DOCX/PPTX via ~3,600-character virtual pages (one virtual page per slide for PPTX; ~200-character floor triggers image OCR), and PDF/images via per-page classification with all paths converging on unified finalisation. Full detail belongs to chunk 06.

**Covers:** Sections 4.1 (predicate-retrieval table, G5) – 4.2 (fan-out, direction, vocabulary guards) with tail into Sections 5 – 5.1.1 (multi-format routing)
