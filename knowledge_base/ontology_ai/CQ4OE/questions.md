---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: CQ4OE: A benchmark for assessing LLM-assisted ontology generation from competency questions

### Q1. What three gaps make current LLM-assisted ontology generation hard to evaluate, according to CQ4OE?
> [!tip]- Answer
> Evaluations use heterogeneous task formulations with incompatible inputs and outputs, reference ontologies rarely specify which classes, properties, or axioms each CQ requires, and metrics based on lexical or coarse structural overlap miss property modeling, logical constraints, and reasoning behavior. Errors like wrong domain/range assignments, missing axioms, or flawed hierarchies therefore go undetected. See [[wiki/01-cq4oe-overview-and-motivation|CQ4OE: Overview and Motivation]].

### Q2. What are the two CQ4OE evaluation tasks and how do they differ?
> [!tip]- Answer
> CQ2Term is the term-level task testing whether a system predicts the explicit classes and properties each CQ requires, over 99 CQs. CQ2Onto is the ontology-level task testing whether a generated ontology captures terms, property characteristics, domain/range triples, TBox axioms, and hierarchies needed to answer 118 CQs. See [[wiki/01-cq4oe-overview-and-motivation|CQ4OE: Overview and Motivation]].

### Q3. How does CQ4OE's four-phase workflow turn 255 published CQs into its two gold standards?
> [!tip]- Answer
> Phase 1 selects core terms by degree ranking plus manual verification, Phase 2 filters 255 published CQs down to 110 retained ones, Phase 3 authors just 8 new CQs for uncovered core terms (118 total), and Phase 4 builds CQ2Term over 99 CQs with explicit terms and CQ2Onto over 118 CQs with required TBox axiom sets. Every item is finalized only on full agreement of one annotator plus two expert reviewers. See [[wiki/02-dataset-construction-and-statistics|Dataset construction and statistics]].

### Q4. What are explicit, implicit, and derived term sets, and what is the AWO example?
> [!tip]- Answer
> Explicit terms (Ei) surface-match the CQ text, implicit terms (Ii) are synonyms or equivalents, and derived terms (Ri) are unmentioned but required to answer the CQ. For AWO's "Which plants eat animals?", Plant, Animal, and eats are explicit while CarnivorousPlant is derived, with axioms CarnivorousPlant ⊑ Plant and CarnivorousPlant ⊑ ∃eats.Animal. See [[wiki/02-dataset-construction-and-statistics|Dataset construction and statistics]].

### Q5. How does CQ4OE align gold and predicted terms that use different labels?
> [!tip]- Answer
> It scores each same-type candidate pair with five methods — hard exact match, difflib sequence matching, Levenshtein, Jaro–Winkler, and embeddinggemma semantic similarity — then takes a hard-match override or the mean of the three highest non-hard scores. One-to-one alignment applies type-specific thresholds (τC = 0.6 for classes, τP = 0.7 for properties) with greedy selection prioritizing hard matches. See [[wiki/03-term-alignment-and-evaluation-metrics|Term Alignment and Evaluation Metrics]].

### Q6. What metrics do CQ2Term and CQ2Onto report over that alignment?
> [!tip]- Answer
> CQ2Term reports global P/R/F1 over pooled term sets plus CQ-conditioned at-least-one, mean, and full coverage, exposing models that recover vocabulary without attaching terms to the right CQ. CQ2Onto evaluates five targets — term recovery, property characteristics, domain/range triples, TBox axioms, HermiT hierarchy closure — with global and alignment-conditioned views, strict equivalence counting, an embedding-cosine diagnostic, and axiom-level plus closure-recovered CQ coverage. See [[wiki/03-term-alignment-and-evaluation-metrics|Term Alignment and Evaluation Metrics]].

### Q7. What is the CQ4OE baseline experimental setup?
> [!tip]- Answer
> Nine LLMs (DeepSeek V4-Pro, V4-Flash, V3.2; Qwen Plus, Flash, 35B-A3B, 27B; Gemma 31B-IT, 26B-A4B-IT) run via OpenRouter at temperature 0 with a 16,384-token limit, reusing MASEO Generation Agent prompts. CQ2Onto compares zero-shot, iterative sequential, and multi-agent repair strategies with RDFLib, HermiT, and OOPS!, totaling 54 runs and 162 ontologies. See [[wiki/04-experimental-setup-and-baselines|Experimental Setup and Baselines]].

### Q8. What do the Fig. 2 CQ2Term results show about conceptualization across domains?
> [!tip]- Answer
> CQ2Term isolates conceptualization — recognizing explicit classes and properties in CQs — and global F1 spans 59.1% to 66.5% with classes (67.1%) beating properties (55.2%) and a precision–recall gap signaling over-generation. CQ-conditioned coverage averages 89.2% at-least-one but only 23.5% full, with Water at 70.6% global F1 yet 0% full coverage, so global scores hide requirement-localization errors. See [[wiki/05-cq2term-results-by-model-and-domain|CQ2Term results by model and domain]].

### Q9. What do the Fig. 3 CQ2Onto results and closure rescue show?
> [!tip]- Answer
> Structure collapses below vocabulary: class F1 averages 59.7% versus property F1 31.8%, Triple-AC 36.4% versus Triple-G 12.4%, and closure F1 only 16.7%, with Axioms-Full near 2%. Closure rescue adds just 1.4 points of mean coverage and leaves full coverage unchanged, confirming reasoning recovers little when SubClassOf/SubPropertyOf chains were never generated. See [[wiki/06-cq2onto-results-and-closure-gains|CQ2Onto Results and Closure Gains]].

### Q10. Which prior tools, methods, and benchmarks does CQ4OE build on or distinguish itself from?
> [!tip]- Answer
> CQ4OE reuses MASEO prompting, scores with the HermiT reasoner and OOPS! pitfall scanner, and grounds similarity in Levenshtein plus Lin/Resnik foundations. It distinguishes itself from OAEI, BioASQ, OntoAxiom, CORAL, and Plu et al. on the grounds that none provides a reusable benchmark with CQ-aligned requirement scope and CQ-to-axiom provenance. See [[wiki/07-discussion-limitations-and-references|Discussion, limitations and references]].

### Q11. Should an ontology team adopt CQ4OE as its evaluation basis for LLM-generated ontologies?
> [!tip]- Answer
> Adopt it when you need requirement-localized, provenance-traceable comparison, since per-run Markdown reports and CSV traces diagnose exactly which terms, axioms, and CQs fail. Hold off as a sole gate if your domain diverges from the six covered ontologies or you need contamination control, given alignment dependence, hierarchy-only closure scope, and public-source leakage — extend with private or post-cutoff ontologies first. See [[wiki/06-cq2onto-results-and-closure-gains|CQ2Onto Results and Closure Gains]].
