> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Rule-Based Deduplication Algorithms
**In one sentence:** The layer replaces a single-alias / bare-fingerprint schema with an AliasOccurrence-backed, provenance-carrying disambiguation schema and implements six deterministic zero-LLM-cost deduplication algorithms, starting with alias expansion, source-text mining, and five-signal name scoring.
## Key points
- Enhanced schema expands aliases to five-plus variants with per-alias provenance via AliasOccurrence (alias, discovery source, count, confidence) on each entity's `name_variants` list.
- Disambiguation now threads contextual evidence and duplicate flags (context_attributes, context_snippets, possible_duplicates, dedup_status) plus fingerprint, key_attributes, confidence, and source; every ExtractionResult exports `dedup_candidates`.
- Three new record types carry deduplication evidence: which context distinguishes same-named entities, where each alias was discovered, and why a pair is a merge candidate; Relationship and Provenance are unchanged.
- Six deduplication algorithms operate deterministically with zero additional LLM inference cost and no labeled training data, unlike deep-learning entity matching [21, 22].
- Algorithmic alias expansion applies transformation set F = {w1[0]. wk, w1 wk[0]., w1[0]wk[0], w1[0].wk[0].} to Person names with k ≥ 2, with zero false positives and zero LLM cost.
- Source-text mining uses Ratcliff/Obershelp similarity S = 2·M/T with threshold τ = 0.85 over consecutive word pairs, discovering 85–90% of spelling variations present in source text.
- Name similarity is a five-signal weighted composite Sim = Σ wk·σk with w = (0.30, 0.25, 0.20, 0.15, 0.10) plus a strong-signal boost, exemplified by "John Doe" vs "Jon Doe" scoring 0.924 (`phonetic_strong`).
---
## Schema evolution
**Covers:** Fig. 6 and refactored models in `schemas/extraction.py` / `schemas/disambiguation.py`

> "The legacy schema (left) carried one alias per entity and a bare disambiguation fingerprint. The enhanced schema (centre) expands aliases to five-plus variants with per-alias provenance, threads contextual evidence and duplicate flags through Disambiguation, and exports dedup_candidates on every result."

- Legacy: one alias per entity, bare disambiguation fingerprint.
- Enhanced (centre):
  - Disambiguation: alias, count fingerprint; fingerprint, key_attributes; confidence, source; context_attributes[]; context_snippets[]; possible_duplicates[]; dedup_status.
  - ExtractionResult: object_id; entities[], relationships[]; dedup_candidates[].
- New record types (right, green):
  - AliasOccurrence: disambiguation alias, count fingerprint.
  - PossibleDuplicate: entity_id, similarity_score; similarity_reason; context_match, suggested_action.
- Implementation notes:
  - Models live in `schemas/extraction.py` and `schemas/disambiguation.py` rather than a single `str_op_schema.py` file.
  - `properties` and `qualifiers` fields given explicit dictionary type aliases.
  - Per-alias provenance captured by AliasOccurrence record (alias, discovery source, count, and confidence) on each entity's `name_variants` list.
- Relationship and Provenance are unchanged.

## Core deduplication algorithms
**Covers:** Section 6.2

> "This section details the six novel algorithms constituting the entity deduplication pipeline. Each is designed to address specific classes of name variation without necessitating further LLM inference calls."

- Six novel algorithms; each addresses specific classes of name variation.
- Deterministic with zero additional inference cost; operate without labeled training data, unlike deep learning approaches to entity matching [21, 22].

## Algorithmic alias expansion
**Covers:** Section 6.2.1, Eq. (3), Fig. 7

- Problem: entity extracted as "John Doe" limits retrievability for "J. Doe" or "JD"; personal name abbreviation patterns are a leading cause of missed matches (Christen [23]).
- Formulation: person name N as ordered tokens W = (w1, w2, ..., wk), applied only when T = Person and k ≥ 2:
  - `A = {N} ∪ { f(W) | f ∈ F }, F = { w1[0]. wk, w1 wk[0]., w1[0]wk[0], w1[0].wk[0]. } (3)`
- Properties: every transformation deterministic, hence repeatable, auditable, zero LLM cost.
- Fig. 7: single extracted name radiates to abbreviative variants; each spoke annotated with producing transformation; green spokes = deterministic F transformations, dashed spoke = variants recovered later from source text (e.g. "Jon Doe" via text mining §6.2).
- Impact: "Expands search coverage deterministically with zero false positives and zero LLM cost."

## PDF text mining with fuzzy matching
**Covers:** Section 6.2.2, Eqs. (4)–(5), Table 9, Fig. 8

- Problem: source documents contain unextracted spelling variations (e.g. "Jon Doe" when "John Doe" was extracted) or shorthand references.
- Metric: Ratcliff/Obershelp similarity [9] via Python `difflib.SequenceMatcher`:
  - `S(x,y) = 2·M / T (4)` where M = matching characters, T = total characters in both strings; selected based on comparative evaluations of string distance functions for name matching [24].
- Threshold: word w from document D is a spelling variant of entity token v if `S(w,v) ≥ τ, where τ = 0.85 (5)`.
- Procedure: miner slides over consecutive word pairs (word_i, word_{i+1}) and tests each pair against extracted name's first and last tokens (w_first, w_last); two acceptance rules fire (Table 9); every accepted pair joins variant dictionary V[e.id].

| Variant class | Acceptance condition | Example hit |
|---|---|---|
| Initial reference | word_i "." = w_first[0] ∧ word_{i+1} ⊒ w_last[:3] | "J. Doe" |
| Spelling variant | S(word_i, w_first) ≥ τ ∧ word_{i+1} ⊒ w_last[:3] | "Jon Doe" |

- Fig. 8 example passage: ". . . the shipment was authorised by J. Doe on 14 June. Customs records list Jon Doe as the consignee of record . . ."; `V[per_001] = {J. Doe initial reference, Jon Doe S = 0.86 ≥ τ}` for extracted entity John Doe (w_first, w_last).
- Impact: "Discovers 85–90% of spelling variations present in the source text, balancing precision (via the 0.85 threshold) with recall."

## Linguistic-aware name similarity scoring
**Covers:** Section 6.2.3, Eq. (6), Fig. 9

- Problem: standard string similarity fails on (1) Slavic gender suffixes ("Petrov"/"Petrova"), (2) spelling and transliteration variants ("John"/"Jon"/"Jhon"), (3) genuine abbreviations vs coincidental first-letter matches; approximate string matching is language-agnostic without morphological augmentation (Navarro [25]); morphological normalisation improves recall for inflected forms [10, 28].
- Formulation: five-signal weighted composite over independent similarity dimensions (not a priority-ordered tier model):
  - `Sim(n1,n2) = Σ_k w_k · σ_k(n1,n2), w = (0.30, 0.25, 0.20, 0.15, 0.10), (6)`
  - 1. Jaro–Winkler (w=0.30): prefix-weighted edit distance for short-string typos/transpositions ("Petrov"/"Petref").
  - 2. Double Metaphone (w=0.25): phonetic code agreement; "John", "Jon", "Jhon" share code JN and score 1.0.
  - 3. Token overlap (w=0.20): word-level Jaccard |T1∩T2|/|T1∪T2|, robust to reordered tokens and honorific prefixes.
  - 4. Abbreviation confidence (w=0.15): confidence one name is a genuine abbreviation of the other (|p|=1 ∧ p=q1 for at least one part-pair); the corrected single-letter test of Section 7.3.7.
  - 5. Cultural-variant score (w=0.10): Slavic gender suffixes ("-ov"/"-ova", "-ev"/"-eva") and hard-coded transliteration families.
- Strong-signal boost: if max_k σ_k ≥ 0.90 and composite < 80% of that maximum, composite is lifted to 0.8 max_k σ_k.
- Auditable output: returns score plus primary reason and full per-signal breakdown; signal weights are configuration constants, leaving a path to learned weights once labelled match data are available.
- Fig. 9 worked example "John Doe" vs. "Jon Doe": Jaro-Winkler 0.956, Double Metaphone 1.000, Token overlap 0.800, Abbreviation 0.000, Cultural 1.000; composite 0.924, reason `phonetic_strong`; "max_k σ_k = 1.0 ≥ 0.90, composite 0.87 ≥ 0.80, no boost needed"; exported as `NameMatchResult(0.924, "phonetic_strong", signals)`.
