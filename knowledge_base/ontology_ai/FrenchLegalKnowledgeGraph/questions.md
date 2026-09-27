---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: LLM-Assisted Ontology Engineering and Construction of a French Legal Knowledge Graph

### Q1. What are the two stages of the paper's workflow, and what does each stage produce?

> [!tip]- Answer
> Stage 1 enriches a SEMLEG-based core ontology via open class-guided extraction, embedding-based fusion, and property induction on a stratified sample of 1,389 articles. Stage 2 runs closed ontology-grounded triple extraction over the full 6,370-article corpus to build the French legal knowledge graph. See [[wiki/01-llm-assisted-ontology-engineering|LLM-Assisted Ontology Engineering for a French Legal Knowledge Graph]].

### Q2. What corpus and semantic scope ground the ontology, and which SEMLEG classes are retained?

> [!tip]- Answer
> The focused corpus holds 6,370 Légifrance regulatory articles across 20 topics, filtered via Apave regulatory-guide references, with ontology engineering done on a stratified sample of 1,389 articles (~10% per domain–document title pair). Competency questions target maintenance obligations — actors, artifacts, conditions, and legal sources — and the core retains SEMLEG classes Actor, Action, Artifact, Condition, Source, Location, Reason, Situation, and Time. See [[wiki/01-llm-assisted-ontology-engineering|LLM-Assisted Ontology Engineering for a French Legal Knowledge Graph]].

### Q3. How does open class-guided triple extraction process each sampled article?

> [!tip]- Answer
> Each article passes through three prompts: entity extraction typed with retained SEMLEG classes (declarations injected as compact Turtle Light), open-vocabulary triple generation where relation labels are inferred from context within subject–object class constraints, and topic assignment to maintenanceActivity, anotherLegalActivity, or legalCrossReference. Only maintenanceActivity triples are kept for property induction. See [[wiki/01-llm-assisted-ontology-engineering|LLM-Assisted Ontology Engineering for a French Legal Knowledge Graph]].

### Q4. How do embedding-based fusion and property induction turn raw triples into the SemLegM ontology, and how do the OpenAI and Mistral variants differ?

> [!tip]- Answer
> Fusion embeds entity and property labels and merges variants above cosine similarity 0.7 (properties grouped by subject–object class pair), keeping the most frequent label and excluding legal references and numeric values. Induction then samples 5% of fused triples per property across 15 batches, prompting for label, domain, range, evidence, definition, aligned question, and confidence, formalized as OWL axioms. The OpenAI variant yields 75 properties with 105 signatures versus 44 with 59 for Mistral (21 properties and 18 signatures shared); OpenAI is more fine-grained and expressive while Mistral stays conservative and normative. See [[wiki/01-llm-assisted-ontology-engineering|LLM-Assisted Ontology Engineering for a French Legal Knowledge Graph]].

### Q5. What does Table 2 show about the effect of fusion on the constructed knowledge graphs?

> [!tip]- Answer
> Fusion preserves every rdf:Statement instance exactly (75,870 Mistral, 51,657 OpenAI) while sharply cutting duplicates: Mistral entities fall from 74,035 to 20,827, object properties from 2,643 to 500, and annotations from 119,063 to 39,055, with smaller but consistent reductions for OpenAI. The effect is strongest for the Mistral graph, showing normalization is central to turning raw LLM triples into a compact usable KG. See [[wiki/02-knowledge-graph-construction-evaluation|Knowledge Graph Construction and Evaluation Statistics]].

### Q6. What do the quantitative metrics R_JSON, R_class, R_prop, and R_sig reveal after fusion?

> [!tip]- Answer
> JSON validity is 100% everywhere and class coverage is ~99.98% (99.97% Mistral, 99.99% OpenAI), so typing against ontology classes is nearly perfect. R_prop rises to 96.42% for Mistral and 85.11% for OpenAI after fusion, meaning fewer than 20% of triples introduce unseen properties — yet R_sig only reaches 72.61% and 61.03%, so the gap comes from reusing known predicates with novel domain–range combinations rather than missing vocabulary. See [[wiki/02-knowledge-graph-construction-evaluation|Knowledge Graph Construction and Evaluation Statistics]].

### Q7. Given the qualitative errors and future work, should a maintenance team deploy this KG directly into a CMMS, and what should come first?

> [!tip]- Answer
> No — the 39–52 inconsistent signatures per fused graph stem mostly from entity typing errors (e.g., legal sources typed as Artifact) plus modality baked into predicates and occasional French predicates, so direct deployment risks wrong obligations and actors. The team should first run iterative ontology refinement with SHACL validation over newly observed signatures, then pilot GraphRAG consultation with KG updates as law evolves. See [[wiki/02-knowledge-graph-construction-evaluation|Knowledge Graph Construction and Evaluation Statistics]].
