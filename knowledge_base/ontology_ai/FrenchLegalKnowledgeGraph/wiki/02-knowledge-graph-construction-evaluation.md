> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Knowledge Graph Construction and Evaluation Statistics
**In one sentence:** Fusion preserves all extracted relation statements while sharply reducing duplicated entities, predicates, signatures, and annotations — especially for Mistral — turning raw LLM triples into a compact ontology-grounded KG that scores 100% JSON validity and ~99.98% class coverage but only 50–73% signature compliance.
## Key points
- Mistral NF produced 2,119,485 RDF triples vs 1,131,066 after fusion (F); OpenAI NF produced 1,507,755 vs 1,311,916 after fusion.
- Fusion preserved all rdf:Statement instances exactly (75,870 for Mistral, 51,657 for OpenAI) while cutting entities from 74,035 to 20,827 (Mistral) and 53,804 to 38,339 (OpenAI).
- Object properties fell from 2,643 to 500 for Mistral and 2,649 to 2,031 for OpenAI; signatures fell from 4,694 to 1,636 (Mistral) and 4,374 to 3,398 (OpenAI).
- Annotations fell from 119,063 to 39,055 (Mistral) and 83,879 to 70,930 (OpenAI); classes fell from 18 to 15 (Mistral) and 15 to 12 (OpenAI).
- Quantitative metrics: R_JSON 100.00% in all four settings; R_class 99.97% (Mistral) and 99.99% (OpenAI); R_prop rises 82.51% to 96.42% for Mistral and 81.52% to 85.11% for OpenAI after fusion.
- R_sig rises 49.86% to 72.61% for Mistral and 56.94% to 61.03% for OpenAI, so fewer than 20% of triples introduce unseen properties but many reuse existing predicates with new domain–range combinations.
- Qualitative check: 39 inconsistent signatures for Mistral fusion vs 52 for OpenAI fusion, mostly from entity typing errors (e.g., legal sources typed as Artifact) or wrong expected object types; modality/polarity baked into predicates (e.g., cannotApplyFor, mustNotExceed) and occasional French predicates despite English-only prompts.
---
## Table 2 — Graph variants with and without fusion
**Covers:** Table 2 Statistics of the knowledge graph variants

| Measure | Mistral NF | Mistral F | OpenAI NF | OpenAI F |
|---|---|---|---|---|
| # RDF triples | 2,119,485 | 1,131,066 | 1,507,755 | 1,311,916 |
| # Classes | 18 | 15 | 15 | 12 |
| # Entities | 74,035 | 20,827 | 53,804 | 38,339 |
| # Object properties | 2,643 | 500 | 2,649 | 2,031 |
| # Signatures | 4,694 | 1,636 | 4,374 | 3,398 |
| # rdf:Statement instances | 75,870 | 75,870 | 51,657 | 51,657 |
| # Annotations | 119,063 | 39,055 | 83,879 | 70,930 |

> "Table 2 summarizes the size and variability of the generated graphs. The fusion clearly preserves the extracted relation statements while substantially reducing duplicated entities, predicates, signatures, and annotations, especially for the Mistral-based graph. This shows that normalization is a central step for turning raw LLM triple generation into a more compact and usable ontology-grounded KG."

## Experimental setup (as reported in chunk)
**Covers:** Section 4 Evaluation — Experimental Setup

- Python pipeline using OpenAI (GPT-4.1 and text-embedding-3-large) and Mistral (mistral-large-2512 and mistral-embed-2312) under the same prompting protocol.
- Temperature 0 for deterministic generation; fixed context window 4k tokens for class-guided entity extraction and 10k for relation discovery.
- Vocabulary URLs: ELI, DCTERMS, CNT, SKOS, PROV, Web Annotation (oa#).

## Quantitative analysis — Table 3
**Covers:** Section 4 Quantitative Analysis + Table 3

| Metric | Mistral NF | Mistral F | OpenAI NF | OpenAI F |
|---|---|---|---|---|
| R_JSON | 100.00% | 100.00% | 100.00% | 100.00% |
| R_class | 99.97% | 99.97% | 99.99% | 99.99% |
| R_sig | 49.86% | 72.61% | 56.94% | 61.03% |
| R_prop | 82.51% | 96.42% | 81.52% | 85.11% |

- R_prop measures whether a triple uses a property already present in the ontology; R_sig additionally requires an expected domain–range combination.
- Fewer than 20% of triples introduce previously unseen properties in all settings, and much less after fusion; lower R_sig therefore points to new or unexpected class combinations for existing predicates rather than missing predicate vocabulary.

## Qualitative analysis and conclusion
**Covers:** Section 4 Qualitative Analysis through Section 5 Conclusion

- Inconsistent signatures whose predicate suggests an expected target class (e.g., hasTime should point to Time): 39 for Mistral fusion, 52 for OpenAI fusion.
- Most true errors come from entity typing mistakes propagated to relations or predicates encoding an incorrect expected object type.
- Competency-question tests as SPARQL queries confirm the graph can retrieve actor roles and legal justifications for maintenance actions.
- Future work stated in chunk: iterative ontology refinement by validating and integrating newly observed domain–range signatures, improved entity/predicate fusion, formal validation (e.g., SHACL), GraphRAG-based consultation, and KG updates as legal provisions evolve.
