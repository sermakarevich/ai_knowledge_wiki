> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Key Insight: The Core Deduplication Algorithms
**In one sentence:** The core deduplication algorithms (Figs. 7–10) were designed for entity-level refinement but needed clean upstream input, so the data-cleaning fixes (Stages 2–3) and the core algorithms (Stage 5) work as complementary defense-in-depth layers evaluated through retrieval gains and an adversarial OCR stress test.
## Key points
- Core algorithms (Figs. 7–10) target entity-level refinement, but their effectiveness was undermined by upstream raw LLM output and chunk-merging data quality issues.
- Data-cleaning fixes (Stages 2–3) and core algorithms (Stage 5) are complementary: the former ensures clean input data while the latter enriches it, and neither layer alone would be sufficient.
- Entity deduplication enhancement raised aliases per entity from 1.0 to 5.0 (+400%), discovered ~6 name variants per entity, auto-flagged dedup candidates, and held false positives at 0.
- Search recall rose from ~70% to ~95% (+25–30%) with <250 ms processing overhead (<0.5% latency), preventing 4–8 graph false merges per document.
- On the 10-page image-only Joint Fleet Summary (JFS) naval document, the fixed pipeline cut wall-clock time 294.6 s to 204.9 s (−30%) and hallucination rate 80.9% (174 entities) to 1.2% (1 entity).
- Legacy OCR failure mode emitted 174 "Dong You 576/598/649…" entities typed as Person from mis-read hull-number columns; the fixed run emits 71 Ship + 12 ShipClass and corrects typing to Ship/ShipClass.
- Reducing OCR_TEXT_CHUNK_PAGES from 5 to 2 doubled ground-truth vessel-class recall from 5/17 (29.4%) to 10/17 (58.8%) and tripled relationships 64 → 206, at a 2:30 latency cost (3:25 → 5:55).
---
## Key insight: refinement vs. input quality
> "The core deduplication algorithms (Figs. 7–10) were correctly designed for entity-level refinement, but their effectiveness was undermined by upstream data quality issues in the raw LLM output and the chunk merging infrastructure."
- "The data cleaning fixes (Stages 2–3) and the core algorithms (Stage 5) are complementary: the former ensures clean input data, while the latter enriches it."
- "Together, they form a defense-in-depth approach where neither layer alone would be sufficient."
## 8 Evaluation — two axes
- Axis 1: impact of deduplication and grounding enhancements on retrieval quality (Section 8.1).
- Axis 2: end-to-end stress test of the OCR pipeline on an adversarial image-only document (Section 8.2).
## 8.1 Deduplication and retrieval impact
Table 17: Performance Metrics Before and After Entity Deduplication Enhancement

| Metric | Before Phase 3 | After Phase 3 | Improvement |
|---|---|---|---|
| Aliases per entity | 1.0 | 5.0 | +400% |
| Name variants discovered | 0 | ~6 per entity | +6 |
| Dedup candidates detected | 0 | Auto-flagged | N/A |
| False positives | 0 | 0 | Maintained |
| Processing overhead | N/A | <250 ms | <0.5% latency |
| Search recall | ~70% | ~95% | +25–30% |
| Graph false merges prevented | 0 | 4–8 per document | High impact |

Fig. 23 glance: "+400% aliases / entity, 95% search recall, 0 false merges, 94% catalog size drop, <250 ms added latency, 7 quality fixes."
## 8.2 OCR pipeline on naval intelligence documents
### 8.2.1 Evaluation corpus and setup
- 10-page Joint Fleet Summary (JFS) naval intelligence report listing PLAN vessel classes by identifier, hull number, and role.
- Image-only: zero extractable characters, Signal 4 = 0 throughout; dense structured layout with multi-column tables, abbreviated headings, and long-tail transliterated ship-class names (Zhongyu, Hutao, Shuoshi, Dalang, Jiangwei, Zhaochang, Dayun, …).
- All 17 distinct vessel-class names serve as ground-truth labels; processed exclusively through the OCR path (100% image pages, text-page ratio = 0).
- Two configurations: legacy (un-guided extraction, binary PDF routing, no deduplication) vs. fixed (ontology-guided extraction, per-page OCR classification, deduplication, type correction); chunk-size ablation varies OCR_TEXT_CHUNK_PAGES ∈ {5, 2}.
### 8.2.2 Headline results: legacy versus fixed pipeline
Table 18 (chunk size = 5 pages for both):

| Metric | Legacy | Fixed | Δ |
|---|---|---|---|
| Wall-clock time | 294.6 s (4:55) | 204.9 s (3:25) | −30% |
| Total entities extracted | 215 | 83 | −61% (fakes removed) |
| Total relationships | 98 | 64 | −35% (fakes removed) |
| Ground-truth class names | 0/17 (0%) | 5/17 (29.4%) | +29.4 pp |
| Hallucinated entities | 174 | 1 | −173 |
| Hallucination rate | 80.9% | 1.2% | −79.7 pp |
| Entity typing | Person/Org (wrong) | Ship/ShipClass (correct) | semantic fix |
| Distinct relationship types | 5 | 8 | +60% |

Hallucination pattern (verbatim): legacy produced "174 entities of the form 'Dong You 576', 'Dong You 598', 'Dong You 649', … (and similar sequential-suffix variants), all typed as Person" from "a systematic OCR mis-read of hull-number columns: the model transcribed table row numbers as given names and appended them to a partial transliteration of the column header."
- Fixed pipeline suppresses this via (1) ontology-guided extraction constraining types to Ship and ShipClass (71 Ship + 12 ShipClass vs. legacy 174 Person + 41 Organization), and (2) alias-expansion and context-aware deduplication consolidating surviving near-identical variants into a single candidate for review.
- Fig. 24: "eliminates the hallucinations, corrects entity types to Ship/Ship Class via ontology-guided extraction, and captures 29.4% of ground-truth class names at 30% lower wall-clock cost."
### 8.2.3 Chunk-size ablation study
Table 19: Reducing OCR_TEXT_CHUNK_PAGES from 5 to 2 doubles ground-truth recall at the cost of a 2:30 latency increase.

| Metric | Legacy | Fixed (chunk=5) | Fixed (chunk=2) |
|---|---|---|---|
| Wall-clock | 4:55 | 3:25 | 5:55 |
| Ground-truth class names | 0/17 | 5/17 (29.4%) | 10/17 (58.8%) |
| Hallucinated entities | 174 | 1 | 0 |
| Distinct entity types | 2 (wrong) | 2 | 4 |
| Distinct relationship types | 5 (fake) | 8 | 18 |
| Total relationships | 98 (fake) | 64 | 206 |

Analysis: halving chunk size 5 → 2 pages gives "+29.4 percentage-point improvement in ground-truth recall (29.4% → 58.8%) and eliminates the last hallucinated entity"; five additional vessel classes captured (Zhongyu, Hutao, Shuoshi, Dalang, Jiangwei, Zhaochang) while one class (Dayun) is displaced at a chunk boundary; relationship count triples (64 → 206) as smaller windows surface intra-table cross-references; trade-off is 2:30 wall-clock increase (3:25 → 5:55) from more LLM calls (Fig. 25).
### 8.2.4 Residual errors and improvement roadmap
- Even with chunk=2, 7 of 17 ground-truth vessel classes are missed, falling into four structural categories each with a targeted intervention (Table 20).
- "The multi-pass union and the directive-prompt interventions require no infrastructure changes and are the natural next step."
- "The dense-layout crop-and-re-OCR addresses the structural root cause for multi-column tables, which accounts for the majority of missed vessel-class names in the JFS corpus."
- Note: Table 20 body beyond its title/ordering line ("ordered by implementation complexity; expected lift is qualitative") is not present in this chunk.
**Covers:** key deduplication insights, no-false-merge results, and title-prefix fixes (chunk Sections 8–8.2.4)
