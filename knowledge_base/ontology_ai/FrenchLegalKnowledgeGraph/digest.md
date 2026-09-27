> [[index|Wiki]] | [[summary|Summary]]
# LLM-Assisted Ontology Engineering and Construction of a French Legal Knowledge Graph — Digest
## 1. [[wiki/01-llm-assisted-ontology-engineering|LLM-Assisted Ontology Engineering for a French Legal Knowledge Graph]]
**In one sentence:** The paper presents a two-stage LLM-assisted workflow that enriches a SEMLEG-based core ontology via open extraction, embedding-based fusion, and property induction on a stratified sample, then uses that ontology to guide closed triple extraction over the full corpus.
## Key points
- Maintenance regulations are hard to exploit in specific cases and to integrate into operational systems such as Computerized Maintenance Management Systems (CMMS).
- The workflow has two stages: (1) ontology engineering from a SEMLEG-based core ontology, and (2) construction of an ontology-grounded French legal knowledge graph via closed extraction over the full corpus.
- The focused corpus contains 6,370 regulatory articles covering 20 topics, built from Légifrance texts filtered via Apave regulatory-guide references; ontology engineering uses a stratified sample of 1,389 articles (~10% of each domain–document title pair).
- Open extraction processes each sampled article with three prompts: entity extraction typed with retained SEMLEG classes (Turtle Light serialization), open-vocabulary triple generation, and topic assignment to maintenanceActivity, anotherLegalActivity, or legalCrossReference.
- Normalization embeds entity and property labels and merges variants with cosine similarity > θE = 0.7 (entities) and θP = 0.7 (properties, grouped by subject–object class pair), keeping the most frequent variant and excluding legal references and numeric labels.
- Property induction samples 5% of fused maintenance triples per property (at least one per signature), splits the sample into 15 batches, and prompts for label, domain, range, evidence, definition, aligned question, and confidence score, formalized into OWL axioms.
- The OpenAI variant induces 75 maintenance-specific properties with 105 signatures versus 44 properties with 59 signatures for Mistral; they share 21 properties and 18 signatures, including appliesTo, composedOf, performedAtLocation, and responsibleFor.
## 2. [[wiki/02-knowledge-graph-construction-evaluation|Knowledge Graph Construction and Evaluation Statistics]]
**In one sentence:** Fusion preserves all extracted relation statements while sharply reducing duplicated entities, predicates, signatures, and annotations — especially for Mistral — turning raw LLM triples into a compact ontology-grounded KG that scores 100% JSON validity and ~99.98% class coverage but only 50–73% signature compliance.
## Key points
- Mistral NF produced 2,119,485 RDF triples vs 1,131,066 after fusion (F); OpenAI NF produced 1,507,755 vs 1,311,916 after fusion.
- Fusion preserved all rdf:Statement instances exactly (75,870 for Mistral, 51,657 for OpenAI) while cutting entities from 74,035 to 20,827 (Mistral) and 53,804 to 38,339 (OpenAI).
- Object properties fell from 2,643 to 500 for Mistral and 2,649 to 2,031 for OpenAI; signatures fell from 4,694 to 1,636 (Mistral) and 4,374 to 3,398 (OpenAI).
- Annotations fell from 119,063 to 39,055 (Mistral) and 83,879 to 70,930 (OpenAI); classes fell from 18 to 15 (Mistral) and 15 to 12 (OpenAI).
- Quantitative metrics: R_JSON 100.00% in all four settings; R_class 99.97% (Mistral) and 99.99% (OpenAI); R_prop rises 82.51% to 96.42% for Mistral and 81.52% to 85.11% for OpenAI after fusion.
- R_sig rises 49.86% to 72.61% for Mistral and 56.94% to 61.03% for OpenAI, so fewer than 20% of triples introduce unseen properties but many reuse existing predicates with new domain–range combinations.
- Qualitative check: 39 inconsistent signatures for Mistral fusion vs 52 for OpenAI fusion, mostly from entity typing errors (e.g., legal sources typed as Artifact) or wrong expected object types; modality/polarity baked into predicates (e.g., cannotApplyFor, mustNotExceed) and occasional French predicates despite English-only prompts.
## The argument in five moves
1. French maintenance regulations are hard to operationalize, so the paper proposes a compact two-stage LLM-plus-ontology workflow from legal text to an ontology-grounded knowledge graph.
2. A SEMLEG-based core ontology and a 6,370-article Légifrance corpus (with a 1,389-article stratified sample) scope the problem to maintenance obligations, actors, artifacts, conditions, and sources.
3. Open class-guided extraction, embedding-based fusion at 0.7 thresholds, and batched property induction produce two SemLegM ontology variants (OpenAI: 75 properties/105 signatures; Mistral: 44/59; 21 properties and 18 signatures shared).
4. Closed extraction over the full corpus plus fusion yields a compact KG that preserves all relation statements while sharply cutting entities, predicates, signatures, and annotations, especially for Mistral.
5. Evaluation shows perfect JSON validity and ~99.98% class coverage with 50–73% signature compliance, where errors stem mainly from entity typing mistakes and novel domain–range reuse, motivating iterative refinement, SHACL validation, GraphRAG consultation, and KG updates as law evolves.
