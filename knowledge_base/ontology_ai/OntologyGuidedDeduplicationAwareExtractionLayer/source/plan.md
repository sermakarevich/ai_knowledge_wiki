# Extraction plan — An Ontology-Guided, Deduplication-Aware Extraction Layer for Knowledge Graph Construction from Heterogeneous Documents

Source: https://arxiv.org/abs/2607.28662v1 (pdf via pdftotext)
Chunks: 15 (titles/slugs only; bodies belong to later workers)

| Chunk slug | Planned wiki page | Covers |
|---|---|---|
| 01-an-ontology-guided-deduplication-aware-extractio | 01-introduction-and-system-overview.md | Covers paper abstract, contributions, and two-phase extraction pipeline overview |
| 02-2-related-work-llms-for-knowledge | 02-related-work.md | Covers related work on LLM knowledge-graph construction, ontology grounding, and entity resolution |
| 03-coarse-all-or-nothing-granularity-selection-was | 03-static-catalog-slices-to-live-retrieval.md | Covers limits of static domain catalog slices and shift to live Neo4j graph retrieval |
| 04-g1-term-vectors-alongside-content-vectors | 04-retrieval-refinements-term-vectors-and-subclass-expansion.md | Covers refinements G1 (term vectors) and G2 (subclass expansion) with scoring |
| 05-metric-baseline-exact-label-refined-subclass-awa | 05-predicate-recovery-and-prompt-guards.md | Covers refinements G3–G5, predicate retrieval gains, and fan-out/direction prompt guards |
| 06-solution-a-six-signal-per-page-classifier-using | 06-multi-format-handlers.md | Covers per-format handlers (PDF, spreadsheet, Office, image) and six-signal page classifier |
| 07-aliasoccurrence-disambiguation-disambiguation-al | 07-rule-based-deduplication-algorithms.md | Covers six zero-inference deduplication algorithms and alias/disambiguation logic |
| 08-impact-the-weighted-composite-captures-all | 08-embedding-resolution-subsystem.md | Covers embedding-based entity resolution (blocking, scoring, conflict guard, decision) |
| 09-key-contributions-this-implementation-advances-k | 09-pipeline-engineering-and-implementation.md | Covers modular package layout, Kafka consumer, chunking, and robustness/retry design |
| 10-1-relationship-type-normalisation-converts-free | 10-relationship-normalisation-and-finalization.md | Covers relationship-type normalisation, qualifier-preserving dedup, and finalization conformance |
| 11-observation-point-expected-observed-source-chars | 11-evaluation-and-quality-defects.md | Covers evaluation setup, recall gains, and silent quality defects corrected |
| 12-key-insight-the-core-deduplication-algorithms | 12-deduplication-insights.md | Covers key deduplication insights, no-false-merge results, and title-prefix fixes |
| 13-root-cause-intervention-cost-expected-lift | 13-empirical-results-and-ablations.md | Covers root-cause analysis, interventions, costs, and expected lift measurements |
| 14-10-ethics-and-broader-impact-this | 14-ethics-limitations-and-conclusion.md | Covers ethics, broader impact, limitations, and conclusions |
| 15-a-threshold-reference-table-22-consolidates | 15-appendices-and-threshold-reference.md | Covers appendices, threshold reference tables, and operational tuning notes |
