> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Impact — Weighted Composite, Context-Aware Detection, and Phase 3 Pipeline
**In one sentence:** The weighted name-similarity composite captures all three name-variation categories with an interpretable per-signal breakdown, and it is gated by context agreement, qualifier-preserving relationship folding, sequence-ordered parallel output, and a guarded Phase 3 composition to prevent false merges and information loss.
## Key points
- The weighted composite captures all three categories of name variation simultaneously rather than committing to a single signal, with a per-signal breakdown showing why two names were linked (transliteration family, phonetic code, token overlap) instead of an opaque score.
- The corrected abbreviation signal (Section 7.3.7) forces coincidental initial matches to score near-zero on that signal so they cannot boost the composite above the merge threshold; configurable weights leave an upgrade path to ML-learned values once labelled match data exist.
- Context-aware duplicate detection makes a merge valid if and only if `Sim(e1.name, e2.name) ≥ 0.75 ∧ Δ(e1, e2) = 1`, where Δ = 1 when all non-null shared attributes (role, org, loc) match and Δ = 0 when any non-null attribute conflicts.
- The Fig. 10 decision surface auto-merges only the top-left cell (Sim > 0.95 with Δ = 1, high confidence), sends 0.90 < Sim ≤ 0.95 with Δ = 1 to manual review (medium confidence), and keeps every Δ = 0 pair distinct regardless of name score — pinned by Elena Petrov vs Elena Petrova at Sim = 0.85 with a role conflict (Δ = 0).
- Relationship deduplication folds edges sharing identity key K = (u, v, t) into `Q_merged = Q1 ∪ Q2`, retaining the record with the larger qualifier set (ties union qualifiers), so three extractions of `(per_001, org_001, EMPLOYED_BY)` collapse to 1 edge with 0 qualifiers lost.
- Sequence-ordered parallel processing uses a mutex plus a sequence-keyed buffer so output order equals submission order regardless of completion order: short docs #2–#4 park in the buffer while 45-page doc #1 extracts, then the drain loop emits 1→2→3→4 atomically.
- The Phase 3 pipeline is the guarded composition `R′ = D ◦ M_S ◦ A(R)` on `R = (E, ρ)` with source text S: A expands Person-only aliases, M_S unions in mined variants (skipped when S is empty), D appends scored pairs `(ei, ej, sij, actionij)`; it is the identity on an empty entity set.
---
## Weighted-composite impact
**Covers:** Impact paragraph preceding Section 6.2.4

> "The weighted composite captures all three categories of name variation simultaneously rather than committing to a single signal."

- Per-signal breakdown enables interpretable matching: analysts see why two names were linked (transliteration family, phonetic code, token overlap) rather than trusting an opaque score.
- Corrected abbreviation signal (Section 7.3.7): coincidental initial matches score near-zero on that signal, so they cannot boost the composite above the merge threshold.
- Configurable weights leave an upgrade path to ML-learned values once labelled match data are available.

## Context-aware duplicate detection
**Covers:** Section 6.2.4, Eqs. (7)–(8), Fig. 10

> "Entities with high name similarity (e.g., "Elena Petrov" and "Elena Petrova") may represent different individuals if their contextual attributes (roles, organizations, locations) diverge."

- Contextual attribute set: `Ce = {role, org, loc}`; agreement function `Δ(e1, e2) = 1` if all non-null shared attributes match, `0` if any non-null attribute conflicts (7).
- Merge validity: `Sim(e1.name, e2.name) ≥ 0.75 ∧ Δ(e1, e2) = 1` (8).
- Decision surface (Fig. 10):

| Name similarity | Context agrees (Δ = 1) | Context conflicts (Δ = 0) |
|---|---|---|
| Sim > 0.95 | auto_merge, confidence: high | different_contexts, kept distinct |
| 0.90 < Sim ≤ 0.95 | manual_review, confidence: medium | different_contexts, kept distinct |
| 0.75 ≤ Sim ≤ 0.90 | different_contexts, low similarity | different_contexts, kept distinct |

- Pinned example: Elena Petrov (combustion scientist, Khamsin Institute) vs Elena Petrova (malware analyst, Vektor Signal); Sim = 0.85 (gender suffix) but role conflict ⇒ Δ = 0 ⇒ kept distinct.
- Impact: "Essential for preventing false positives. Context validation ensures that entities with similar names but disparate contexts are accurately identified as distinct entities."

## Relationship deduplication
**Covers:** Section 6.2.5, Eq. (9), Fig. 11

> "Multi-phase extraction can yield duplicate relationships with varying levels of detail (e.g., one extraction includes a date qualifier, another does not), artificially inflating edge counts and fragmenting contextual data."

- Relationship tuple `r = (u, v, t, Q)` with nodes u, v, edge type t, qualifier dictionary Q; shared identity key `K = (u, v, t)` merges to `Q_merged = Q1 ∪ Q2` (9).
- Richness-preserving fold: retained record is the one with the larger qualifier set; ties merge qualifiers (`Seen[K] ← Seen[K]` with `Q ← Q_Seen[K] ∪ Q_r` when `|Qr| = |Q_Seen[K]| > 0`).
- Fig. 11 trace: `(per_001, org_001, EMPLOYED_BY)` with `Q = {}` (chunk 2), `Q = {date: 2024-06-15}` (chunk 4), `Q = {location: London HQ}` (2nd pass) fold into one record with `Q = {date: 2024-06-15, location: London HQ}` — 1 edge out, 0 qualifiers lost.
- Impact: "Treats temporal and contextual metadata as primary attributes, preventing information loss during the deduplication process."

## Sequence-ordered parallel processing with mutex-protected output
**Covers:** Section 6.2.6, Fig. 12

> "Parallel document processing can lead to interleaved and garbled JSON output in the terminal if a worker completes a shorter document while another worker is mid-output on a larger document."

- Solution: mutex lock for atomic printing plus sequence-ordered buffering emitting outputs strictly in original submission order.
- Mechanism: each document carries a sequence number; completions land in a hash-map buffer; a single drain loop releases result n+1 only after result n has been printed (under mutex); invariant: output order = submission order regardless of completion order.
- Fig. 12 pattern: W1 holds doc #1 (45 pp) while W2/W3 finish docs #2–#4; results 2–4 wait (`next_seq = 1` not yet complete); once #1 lands the drain loop releases 1→2→3→4 under one mutex.
- Impact: "Enables significant performance gains via parallel processing while maintaining the operational requirement of coherent, sequential terminal output."

## Post-extraction enhancement pipeline
**Covers:** Section 6.3, Fig. 13

> "The aforementioned algorithms are integrated into a Phase 3 pipeline that executes automatically following relationship extraction."

- Composition on extraction result `R = (E, ρ)` with raw source text S: `R′ = D ◦ M_S ◦ A(R)`.
- A (alias expansion): replaces each person entity's alias set `a(e)` by `a(e) ∪ expand(name(e))`; Person entities only.
- M_S (text mining): further unions in spelling variants `mine_S(e)` recovered from S by fuzzy matching; skipped when no source text accompanies the record.
- D (duplicate detection): leaves entities unchanged but populates the candidate list with scored pairs `{(ei, ej, sij, actionij)}` with context validation.
- Guards: every stage conditional; whole composition is the identity on an empty entity set, so the pipeline degrades gracefully rather than failing.

## Algorithm summary
**Covers:** Section 6.4, Table 10

| # | Algorithm | Innovation | Value |
|---|---|---|---|
| 1 | Algorithmic Alias Expansion | Deterministic abbreviation generation | Coverage |
| 2 | PDF Text Mining (Fuzzy Matching) | SequenceMatcher + word pairing | Discovery |
| 3 | Linguistic-Aware Similarity Scoring | 5-signal composite, cultural variants | Highly novel |
| 4 | Context-Aware Duplicate Detection | Role/org/location conflict validation | Precision |
| 5 | Relationship Deduplication | Qualifier-aware merging | Data integrity |
| 6 | Sequence-Ordered Parallel Output | Mutex + buffering for consistency | Operational |
| 7 | Per-Page OCR Classification | 6-signal PyMuPDF page classifier | Routing |

**Covers:** Chunk 08-impact-the-weighted-composite-captures-all (weighted-composite impact paragraph; Sections 6.2.4–6.4; Eqs. (7)–(9); Figs. 10–13; Table 10)
