---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: An Ontology-Guided, Deduplication-Aware Extraction Layer for Knowledge Graph Construction from Heterogeneous Documents

### Q1. What problem does the extraction layer solve, and what is its end-to-end shape?

> [!tip]- Answer
> Unconstrained LLM extraction fractures type vocabularies, duplicates entities and relationships, and risks silently conflating distinct same-named people. The layer is a real-time Kafka consumer that routes heterogeneous documents through a five-stage pipeline (extract, clean, merge, relationship second pass, enrich) using a locally hosted ontology-tuned Qwen3.5-9B model plus live Neo4j ontology retrieval, emitting Pydantic-validated JSON. See [[wiki/01-introduction-and-system-overview|Introduction and System Overview]].

### Q2. What does the paper claim as its contribution relative to prior LLM-for-KG work?

> [!tip]- Answer
> Prior zero-shot, NER-style, generative, and revisited relation-extraction work consistently reports fragmented type vocabularies, hallucinated relations, and description-over-relation bias. The paper claims no new extraction model; instead its contribution is an architecture that constrains and repairs a stock model's output via ontology-slice retrieval, rule-based plus embedding entity resolution, and a two-phase quality-gated chunked pipeline. See [[wiki/02-related-work|Related Work: LLMs for Knowledge Graph Construction]].

### Q3. Why did live Neo4j graph retrieval replace static catalog slices, and what did it save?

> [!tip]- Answer
> Static domain-level slices injected whole catalog files (~11,200 tokens on the representative document, ~17.7K worst case), misrouted on filenames and synonyms, and drifted from the live schema between rebuilds. Live content-conditioned retrieval uses multi-span windowing with PageRank-penalised cosine scoring (floor 0.72, ~5K token budget) and injects only matched classes (~700 tokens), reclaiming ~10,500 tokens (~94%, ~16×) for document content. See [[wiki/03-static-catalog-slices-to-live-retrieval|Static Catalog Slices to Live Graph Retrieval]].

### Q4. What is the G1 term-vector refinement and why does it help?

> [!tip]- Answer
> A ~1,500-character prose window embeds to a blurred narrative centroid that sits too far from terse ontology labels, dropping borderline classes below the 0.72 floor. G1 embeds a compact pipe-delimited term string of proper nouns, abbreviations, and domain terms (e.g. "12th Battalion | Operation Vijay | SSP | LoC") as a second query vector and keeps the best match per class across both vectors. See [[wiki/04-retrieval-refinements-term-vectors-and-subclass-expansion|Retrieval Refinements: Term Vectors and Subclass Expansion]].

### Q5. What is the G2 subclass-expansion refinement and when does it fire?

> [!tip]- Answer
> Baseline vector retrieval favours well-described general classes, so if Organization scores 0.85 only it is injected and the model emits Organization even when SecurityForce is correct. G2 treats any class with adjusted score ≥ 0.80 as evidence its children are worth showing, traversing one subClassOf hop down and injecting direct children at 0.78 so the model can choose the tighter fit. See [[wiki/04-retrieval-refinements-term-vectors-and-subclass-expansion|Retrieval Refinements: Term Vectors and Subclass Expansion]].

### Q6. What did subclass-aware refined retrieval (G5) achieve for predicates?

> [!tip]- Answer
> Baseline exact-label predicate retrieval surfaced only 3 tangential predicates with no command-hierarchy family coverage. Refined subclass-aware G5 retrieval surfaces 68 predicates including subordinate to, commands, part of, reports to, and commanded by, giving complete hierarchy-family coverage for the evaluated command structure. See [[wiki/05-predicate-recovery-and-prompt-guards|Predicate Recovery and Prompt Guards]].

### Q7. What three guards make emitted relationships conform to the schema?

> [!tip]- Answer
> Retrieval steers but a 9B local model still over-emits, mislabels, and mis-orients, so one prompt guard plus two finalization guards enforce conformance. The fan-out guard collapsed a 2 × 58 CLAIMED_BY grid from 116 edges to 1; rank-guarded orientation canonicalizes inverse phrasings into upward subordinate to by coarse tier; vocabulary canonicalization snaps predicates to 954 ontology keys (0.80 floor) and flags the rest _novel_predicate. See [[wiki/05-predicate-recovery-and-prompt-guards|Predicate Recovery and Prompt Guards]].

### Q8. How does the six-signal per-page PDF classifier route pages and documents?

> [!tip]- Answer
> Each page follows a priority cascade: skip if area is zero, OCR if image-block or xref-image coverage exceeds 0.15, text if characters exceed 50, OCR if drawing primitives exceed 200, text if any characters remain, else skip. The document routes by text pages over usable pages: ≥80% text, ≤20% OCR, otherwise a mixed split-and-merge that processes each page optimally instead of losing scanned content or wastefully OCRing born-digital pages. See [[wiki/06-multi-format-handlers|Solution: A Six-Signal Per-Page Classifier for PDF Routing]].

### Q9. How do alias expansion and source-text mining expand recall without LLM calls?

> [!tip]- Answer
> Alias expansion applies the deterministic transformation set F = {w1[0]. wk, w1 wk[0]., w1[0]wk[0], w1[0].wk[0].} to Person names with two or more tokens, generating variants like "J. Doe" with zero false positives and zero inference cost. Source-text mining slides over consecutive word pairs with Ratcliff/Obershelp similarity at τ = 0.85, recovering 85–90% of spelling variants present in the text such as "Jon Doe" or "J. Doe". See [[wiki/07-rule-based-deduplication-algorithms|Rule-Based Deduplication Algorithms]].

### Q10. What are the five signals in the linguistic-aware name-similarity score?

> [!tip]- Answer
> The composite Sim = Σ wk·σk uses weights (0.30, 0.25, 0.20, 0.15, 0.10) over Jaro–Winkler, Double Metaphone phonetic agreement, token-overlap Jaccard, abbreviation confidence, and cultural-variant score (e.g. Slavic -ov/-ova), plus a strong-signal boost and an auditable per-signal breakdown. "John Doe" versus "Jon Doe" scores 0.924 with reason phonetic_strong, showing how transliteration and phonetic agreement survive spelling drift. See [[wiki/07-rule-based-deduplication-algorithms|Rule-Based Deduplication Algorithms]].

### Q11. When is a duplicate merge valid under context-aware detection?

> [!tip]- Answer
> A merge is valid if and only if name similarity ≥ 0.75 and context agreement Δ = 1, where Δ = 1 only when all non-null shared attributes (role, organisation, location) match. Only Sim > 0.95 with Δ = 1 auto-merges; 0.90–0.95 goes to manual review; any Δ = 0 pair stays distinct, as with Elena Petrov versus Elena Petrova at Sim 0.85 but conflicting roles. See [[wiki/08-embedding-resolution-subsystem|Impact — Weighted Composite, Context-Aware Detection, and Phase 3 Pipeline]].

### Q12. How do relationship deduplication and sequence-ordered output prevent information loss?

> [!tip]- Answer
> Edges sharing the identity key K = (u, v, t) fold qualifiers via Q_merged = Q1 ∪ Q2, keeping the record with the larger qualifier set, so three extractions of (per_001, org_001, EMPLOYED_BY) collapse to one edge with zero qualifiers lost. A mutex plus sequence-keyed buffer holds early-finishing short documents until the long document ahead completes, so terminal output order always equals submission order. See [[wiki/08-embedding-resolution-subsystem|Impact — Weighted Composite, Context-Aware Detection, and Phase 3 Pipeline]].

### Q13. How does the optional embedding-based resolution layer score and guard pairs?

> [!tip]- Answer
> The five-stage embed–block–score–decide–collect engine blocks via the union of FAISS cosine top-k (k = 20) and Double Metaphone phonetic grouping to avoid O(n²) comparison, then scores seven signals (0.25 name, 0.20 embedding, 0.15 property overlap, four 0.10 signals) with conflicts penalised at twice agreement weight. Pairs route to auto-merge (≥0.85), manual review (0.60–0.85), or codename-candidate (≥0.50 with pattern), but a hard-conflict guard on discriminator keys forbids merging regardless of score. See [[wiki/09-pipeline-engineering-and-implementation|Pipeline Engineering and Implementation]].

### Q14. What happens in pipeline Stages 2–5 after per-chunk LLM extraction?

> [!tip]- Answer
> Stage 2 normalises relationship types to UPPER_SNAKE_CASE with typo correction, deletes self-loops, and fixes entity types by name-pattern heuristics. Stage 3 merges cross-chunk entities on title-stripped canonical keys with uniform ID reassignment; Stage 4 runs a batched (≤80 entities, ≤8 batches) LLM second pass for cross-chunk relationships with qualifier-aware dedup; Stage 5 enriches aliases and scored dedup candidates into one validated JSON graph. See [[wiki/10-relationship-normalisation-and-finalization|Relationship normalisation and finalization]].

### Q15. What caused the zero per-chunk relationships, and what was the net fix impact on IR-001.pdf?

> [!tip]- Answer
> The _env_int() guard rewrote the REL_EXTRACTION_MAX_SOURCE_CHARS = 0 (unlimited) sentinel via max(1, 0) = 1, so S[:1] truncated 37,542 characters to the single letter "P" and per-chunk relationships fell from 22–38 expected to zero. Removing the guard plus six Stage 2–3 cleaning fixes cut entities 579 → ~400, self-loops 114 → 0, broken references 9 → 0, abbreviation false positives 79 → ~0, and restored 500+ relationships. See [[wiki/11-evaluation-and-quality-defects|Evaluation and Quality Defects]].

### Q16. What do the JFS naval stress test, ablations, and threshold reference imply for deployment?

> [!tip]- Answer
> On the 10-page image-only Joint Fleet Summary, the fixed pipeline cut wall-clock time ~30%, hallucination rate 80.9% → ~1%, and corrected typing to Ship/ShipClass, while shrinking OCR chunks from 5 to 2 pages doubled vessel-class recall (5/17 → 10/17) and tripled relationships at a 2:30 latency cost. Local-vs-cloud benchmarks show the local model production-viable for OCR and within ~6 points on extraction, but Table 22 thresholds are deployment defaults tuned on the development corpus, so adopters must retune floors like 0.72/0.80/0.85 rather than treating them as universal. See [[wiki/12-deduplication-insights|Key Insight: The Core Deduplication Algorithms]], [[wiki/13-empirical-results-and-ablations|Root Cause, Intervention Cost and Expected Lift]] and [[wiki/15-appendices-and-threshold-reference|Appendices and Threshold Reference]].

### Q17. What dual-use risks does person-identity extraction carry, and what mitigations does the paper name?

> [!tip]- Answer
> The two explicit harms are misidentification (an erroneous merge attributing one person's actions to another) and surveillance (higher-recall person-centric search demanding governance). Mitigations are conservative context-validated merging that never auto-merges on name similarity alone, a hard-conflict guard no score can override, human review of borderline pairs with provenance on every decision, restricted access with query logging, and fictional-placeholder names plus synthetic evaluation corpora. See [[wiki/14-ethics-limitations-and-conclusion|Ethics, Broader Impact, Limitations and Conclusion]].

### Q18. Should a compliance-monitoring team adopt this extraction layer for person-centric search?

> [!tip]- Answer
> Yes, conditionally: adopt it where a governed schema exists, because ontology grounding plus layered deduplication lifted search recall ~70% → 95% with zero false merges and cut hallucinations from 174 to near zero on adversarial input. Require authorised-analyst access, query logging, human review of borderline pairs, and local retuning of thresholds first, since weights and floors are dev-corpus heuristics and the dual-use misidentification and surveillance risks demand provenance-audited, conservative merging. See [[wiki/14-ethics-limitations-and-conclusion|Ethics, Broader Impact, Limitations and Conclusion]].
