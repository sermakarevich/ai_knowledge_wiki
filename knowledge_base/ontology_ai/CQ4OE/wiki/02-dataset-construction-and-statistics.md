> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Dataset construction and statistics
**In one sentence:** From 255 published CQs across six source ontologies, a four-phase CQ-aligned workflow retains 110 CQs, adds 8 new CQs (118 total), and builds CQ2Term (99 CQs) and CQ2Onto (118 CQs) gold standards under triple-review adjudication.
## Key points
- Six source ontologies (Wine, AWO, ODRL, SAREF4WATR, VGO, SWO) contribute 255 published CQs, of which 110 are retained after filtering out CQs requiring external knowledge, unanswerable from the source, or instance-level rather than TBox-level.
- Only 8 new CQs (3.1% of the original 255) are manually authored to cover uncovered core terms, yielding 118 CQs in total.
- CQ2Term keeps only CQs with at least one explicit class or property term (Ei ≠ ∅), excluding 19 inference-heavy CQs from SAREF4WATR, VGO, and SWO, leaving 99 CQs.
- CQ2Onto covers all 118 CQs, linking each CQ to a sufficient TBox axiom set where an axiom is retained only if its removal would make the CQ unanswerable.
- Core terms (Tcore) are selected by ranking named classes/properties by in- and out-degree plus manual verification with owl2diagram and official published requirements.
- Each CQ is annotated with explicit (Ei, surface matches), implicit (Ii, synonyms/equivalents), and derived (Ri, unmentioned but required) term sets, e.g. AWO "Which plants eat animals?" gives Plant, Animal, eats (explicit) plus CarnivorousPlant (derived) with axioms CarnivorousPlant ⊑ Plant and CarnivorousPlant ⊑ ∃eats.Animal.
- Triple-review adjudication finalizes every item only on full agreement of one annotator plus two expert reviewers; 101 of 118 CQs (85.6%) accepted without change, with 17 revisions concentrated in SWO (10), VGO (3), ODRL (2), SAREF4WATR (2).
---
## Table 1a: CQ counts and source ontology statistics
**Covers:** Six source ontologies, 4-phase CQ annotation workflow, and CQ2Term/CQ2Onto gold-standard statistics.

Src., Ret., and New⋆ are original, retained, and added CQs. CQ2O and CQ2T are CQs in each gold standard. C, OP, DP, and Ax are classes, object properties, data properties, and OWL axioms. Depth is the longest SubClassOf or SubPropertyOf chain and Width is the maximum number of terms at any hierarchy level. Source counts include imports.

| Ontology | Src. | Ret. | New⋆ | CQ2O | CQ2T | C | OP | DP | Ax | Depth | Width |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Wine | 7 | 4 | 1 | 5 | 5 | 77 | 13 | 1 | 744 | 3 | 7 |
| AWO | 14 | 7 | 0 | 7 | 7 | 31 | 5 | 0 | 93 | 2 | 21 |
| ODRL | 35 | 13 | 6 | 19 | 19 | 30 | 49 | 4 | 416 | 1 | 22 |
| SAREF4WATR | 43 | 21 | 0 | 21 | 20 | 72 | 40 | 22 | 445 | 5 | 19 |
| VGO | 68 | 30 | 1 | 31 | 22 | 37 | 33 | 6 | 189 | 2 | 20 |
| SWO | 88 | 35 | 0 | 35 | 26 | 1971 | 161 | 5 | 8087 | 15 | 679 |
| Total | 255 | 110 | 8 | 118 | 99 | — | — | — | — | — | — |

## Table 1b: CQ2Term and CQ2Onto gold standard statistics
**Covers:** CQ2Term and CQ2Onto gold-standard statistics.

CQ2Onto counts refer to CQ-aligned sub-ontologies. In CQ2Term, P combines OP and DP.

| Ontology | CQ2Term C | CQ2Term P | CQ2Onto C | CQ2Onto OP | CQ2Onto DP | CQ2Onto Ax | CQ2Onto Depth | CQ2Onto Width |
|---|---|---|---|---|---|---|---|---|
| Wine | 11 | 5 | 17 | 8 | 1 | 68 | 2 | 4 |
| AWO | 7 | 1 | 9 | 5 | 0 | 25 | 1 | 5 |
| ODRL | 13 | 26 | 15 | 28 | 0 | 60 | 1 | 9 |
| SAREF4WATR | 15 | 20 | 20 | 14 | 11 | 43 | 3 | 8 |
| VGO | 7 | 14 | 25 | 33 | 5 | 77 | 1 | 12 |
| SWO | 20 | 18 | 31 | 18 | 5 | 80 | 1 | 7 |

## Four-phase annotation workflow (Fig. 1)
**Covers:** Six source ontologies, 4-phase CQ annotation workflow, and CQ2Term/CQ2Onto gold-standard statistics.

- "To ensure a fair evaluation, the benchmark must assess the knowledge required by the CQs, not the broader domain content of full reference ontologies."
- "Without CQ alignment, a generated ontology could be penalized for omitting out-of-scope content or rewarded for reproducing domain knowledge beyond the stated CQ requirements."
- Phase 1 — Core term selection: rank named classes and properties by in- and out-degree, validate with owl2diagram and official published requirements; retained terms define Tcore.
- Phase 2 — CQ filtering and term annotation: from 255 published CQs remove those requiring external knowledge, unanswerable from source, or instance-level; leaves 110 retained CQs, each annotated with Ei / Ii / Ri.
- Phase 3 — CQ augmentation: manually author CQs for uncovered core terms (marked ⋆); "Only 8 CQs (3.1% of the original 255) are added across all domains, yielding 118 CQs in total."
- Phase 4 — Gold standard construction: "CQ2Term records CQ-to-term provenance over explicit class and property terms"; "the annotated terms (Ei ∪ Ii ∪ Ri) are used to extract CQ-relevant TBox fragments"; "The resulting gold standards cover 99 CQs for CQ2Term and 118 CQs for CQ2Onto."
