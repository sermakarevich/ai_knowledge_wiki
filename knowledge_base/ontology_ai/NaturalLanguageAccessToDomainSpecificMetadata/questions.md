---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Natural Language Access to Domain-Specific Metadata: A Reusable Framework for LLM Query Generation

### Q1. What is the NLKGQ system and what does it achieve on the demonstration archive?

> [!tip]- Answer
> NLKGQ (Natural Language Knowledge Graph Query) is a domain-agnostic harness that translates natural language questions into SPARQL via an LLM and executes them against a knowledge graph, plus a web interface for posing questions. Demonstrated on a large MRI neuroimaging archive, its best configurations reach 100% accuracy on a 21-question competency and regression test set built with domain experts, with no fine-tuning, retrieval augmentation, or multi-agent orchestration. See [[wiki/01-overview-and-framework-intro|Overview and Framework Intro]].

### Q2. What is the ontology-first development process, and why must the demo run local LLMs?

> [!tip]- Answer
> The process first captures domain vocabulary and semantics in a formal OWL ontology, then a domain-specific ETL pipeline extracts archive metadata into a knowledge graph defined by that ontology for LLM-driven querying. Both framework and process are designed for reuse across domains, with the MRI archive (80 studies, 2,000 experiments, ~10M triples, 180TB) as the demonstration. GDPR privacy for human-subject data forces local-only inference, so a practical goal is the smallest model with acceptable accuracy on modest institutional hardware. See [[wiki/01-overview-and-framework-intro|Overview and Framework Intro]].

### Q3. What are the paper's four claimed contributions?

> [!tip]- Answer
> The paper claims (1) the NLKGQ framework and ontology-first process with design principles, KG-builder pattern, and query server plus web interface; (2) a systematic evaluation over 8 models, 8 ontology representations, and 768 configurations (16,000+ runs) showing ontology design dominates accuracy; (3) a generic OWL KG-to-SQL generator enabling a controlled SPARQL-vs-SQL comparison on identical questions; and (4) an analysis of OWL's structural advantages over SQL DDL for LLM query generation. It assumes a compact, author-controlled domain ontology, unlike work stuck with opaque public KGs. See [[wiki/02-background-and-annotation-impact|Background and Annotation Impact]].

### Q4. What do the related-work accuracy numbers show about annotations and representation?

> [!tip]- Answer
> Enterprise text-to-SQL collapses on real schemas (GPT-4o at 0% on BEAVER via schema-retrieval and column-mapping failures), while reformulating the same questions over a knowledge graph lifts accuracy from 16% to 54%, and adding column descriptions gains 20+ points on uninformative columns. For SPARQL, Giuliani et al.'s 0.08→0.60 gain confounds renaming with added axioms and filtering, whereas this paper's ablation holds model, prompt, and benchmark fixed and isolates a 90-point spread (100% default to 10% abstract-graph) from representation alone. Template-dependent systems like SparqLLM lose most accuracy without their 360 hand-authored templates, while the full annotated ontology in context reverses the terse-linearization ordering to 100% SPARQL vs 57% auto-SQL. See [[wiki/02-background-and-annotation-impact|Background and Annotation Impact]].

### Q5. What are the six OWL design principles for LLM consumption?

> [!tip]- Answer
> The principles are (1) full English words like hasAcquisitionTime, (2) consistent has<Property> naming, (3) descriptive directional relationships like isSubjectOfExperiment, (4) explicit rdfs:domain and rdfs:range, (5) natural-language annotations via rdfs:comment, rdfs:label, and skos:altLabel for context and synonyms, and (6) no opaque codes — meaningful URIs throughout. They cost nothing in formal expressiveness and are framed as engineering decisions, not cosmetics, aligning with FAIR Reusability. The hasHandedness example shows name, label, comment, domain, and range jointly letting the LLM use the property — including correct FILTERs — without prior exposure, unlike Wikidata's opaque wdt:P552. See [[wiki/03-ontology-richness-and-design-principles|Ontology Richness and Design Principles]].

### Q6. How are the knowledge graph built and the NLKGQ server prompt constructed?

> [!tip]- Answer
> A Python rdflib ETL pipeline maps DICOM headers, NIfTI sidecars, Siemens TWIX raw headers, the experiment registry, and the participant system to MRO terms, materializing implied triples (both inverse directions, explicit class memberships) at build time so no OWL reasoner is needed at query time, then loads ~10M triples into Apache Jena Fuseki for SPARQL 1.1. The server's system prompt combines generic SPARQL instructions, the complete domain ontology in Turtle, and a small domain-specific rider, with harness fixes for <think> blocks, markdown extraction, PREFIX correction, and optional error-feedback retry that mainly helps smaller models. The web app displays generated SPARQL for transparency and trust, with CSV download, an Explain button, script export, ontology visualization, and Save Test Case. See [[wiki/03-ontology-richness-and-design-principles|Ontology Richness and Design Principles]].

### Q7. How do the ontology, competency questions, and prompt rider co-evolve, and what infrastructure supports it?

> [!tip]- Answer
> Each test run feeds back into all three artifacts in small steps: confusing names are fixed in the ontology (e.g. skos:altLabel "pseudonym" on hasSubjectId), recurring LLM mistakes become rider directives (e.g. return experiment IDs, not instance URIs), and poorly handled new questions become new competency cases — needing domain knowledge but no ML, database, or SPARQL expertise. The test driver sweeps model, temperature, prompt, ontology representation, backend, repetitions, and fix-retry policy, logging timing and match status to CSV via a parallel walker script. Eight auto-generated ontology representations (default through abstract-graph) form the ablation, a generic converter derives a PostgreSQL 17 schema (6 tables, up to 182 columns) from the same ontology, and eight Qwen3 variants (8B–35B, dense/MoE, FP8/Q8) run on MI300A APUs via vLLM and 4× Quadro RTX 5000s via llama.cpp against an 80KB (~18K-token) ontology. See [[wiki/04-iterative-development-and-methods|Iterative Development and Research Methods]].

### Q8. What is the evaluation protocol and what do the example queries demonstrate?

> [!tip]- Answer
> Evaluation uses 21 expert-built competency and regression questions (lookups, joins, filters, aggregations, sorts, ontology introspection), each with NL text, reference SPARQL, and expected results in SPARQL Results JSON, scored by canonicalized result match; the SPARQL grid spans 8 models × 8 representations × 3 prompts × 4 temperatures (16,000+ runs), with up to two error-feedback retries on syntax errors. Three zero-shot Qwen3.6-27B examples show the progression: a study-101 lookup, a multi-entity join with demographics and acquisition date, and a filtered aggregation using FILTER(xsd:integer(?PatientAge) > 42) with a date cutoff. All three are generated from NL plus ontology alone, correctly using property names, inverse traversal, and type casting. See [[wiki/05-framework-architecture-and-production-system|Framework Architecture and Production System]].

### Q9. Which models reach 100% on SPARQL and how do the rest rank?

> [!tip]- Answer
> Only the two 27B dense variants reach 100% on the default ontology at temperature 0.0 — full-precision Q36.27B.D (8.1s, baseline prompt) and Q8-quantized Q36.27B.Q (14.6s on older hardware, procedural prompt) — with the FP8 variant at 95%. Accuracy falls to 57% for the 30B coder and both 35B MoE variants, 38% for 14B, and 24% for 8B, showing scale matters within architectures but dense 27B beats larger MoE totals. The Q8 model being 1.8× slower yet equally accurate on vintage Quadros is the deployment-relevant finding. See [[wiki/06-model-comparison-results|Model Comparison Results]].

### Q10. How do ontology representation, prompt, and temperature affect accuracy?

> [!tip]- Answer
> Representation dominates: default Turtle hits 100%, no-comments drops to 81%, compact-typed/grouped/compact reach 71%/67%/62%, raw-graph 48%, and abstract forms collapse to 19%/5% — with the compact→abstract-dict cliff proving name semantics matter beyond graph structure. Prompt and temperature effects are modest by comparison: all three prompts reach 100% with 27B dense at temp 0.0, and temperatures 0.0/0.2/0.4/0.6 peak at 100%/95%/90%/90%. At 80KB the full ontology fits comfortably even in 32K windows, so compactness buys little while costing heavily. See [[wiki/06-model-comparison-results|Model Comparison Results]].

### Q11. What is the SPARQL-vs-SQL headline result and which OWL structures explain it?

> [!tip]- Answer
> On the same 21 questions the ontology-driven SPARQL path scores 21/21 (100%) versus 12/21 (57%) for mechanically derived wide-table SQL, with annotations critical to both (SPARQL 100%→81% and SQL 57%→43% when stripped). Three structural advantages explain the gap: rdfs:domain/range class grouping is visible scaffolding in Turtle but flattened into column lists in DDL; owl:inverseOf allows bidirectional traversal (aStudyHasExperiment vs isExperimentOfStudy) while SQL forces the LLM to find the single owning foreign key and join from the correct side; and per-question results show SQL failing exactly on dataset-property, demographic, temporal, aggregation, and introspection queries. The authors stress this ordering depends on representation richness, not language superiority. See [[wiki/07-sparql-vs-sql-evaluation|SPARQL vs SQL Evaluation]].

### Q12. What does the EAV control show, and what does the local-hardware result prove?

> [!tip]- Answer
> The Entity-Attribute-Value alternative (narrow entity_id/attribute/value tables auto-derived from the same ontology) reaches only 11/21 (52%) with comments and 2/21 (10%) without, because relationship attributes expose prefixed identifiers like study_101 instead of clean values — a structural disadvantage readable naming cannot fix, unlike SPARQL variables or wide-table clean foreign keys. Deployment-wise, the Q8 model on 4× Quadro RTX 5000s (several generations old) takes both the 100% SPARQL and the best 57% SQL scores, proving no recent-generation GPUs are needed. That plus Apple-Silicon/MLX estimates make always-on local deployment practical for GDPR-constrained institutions. See [[wiki/07-sparql-vs-sql-evaluation|SPARQL vs SQL Evaluation]].

### Q13. What limits generalization of the 100%-vs-57% result?

> [!tip]- Answer
> The gap is scoped to auto-generated SQL schemas, not expert-designed ones with denormalized views and documented joins, and its magnitude with hand-tuned SQL is explicitly unmeasured. The evaluation covers one MRI domain, 21 competency questions that co-evolved with the ontology and rider (so novel queries may differ), Qwen3-family models only with no cloud-frontier comparison, Fuseki-in-Docker metadata volume, and ontology complexity bounded by context windows. Counterintuitive lessons bound choices too: dense 27B beats 35B MoE for schema-precise generation, the simplest baseline prompt wins, and Q8 quantization preserves 100% while FP8 slips to 95%. See [[wiki/08-limitations-and-unmeasured-gaps|Limitations and Unmeasured Gaps]].

### Q14. (Evaluation) A privacy-constrained institute with older GPUs wants NL access to a new sensitive archive — should it adopt this approach, and with what caveats?

> [!tip]- Answer
> Yes, conditionally: replicate the ontology-first recipe (readable OWL, co-evolving rider and competency suite, dense 27B-class Q8 local model, simplest prompt at low temperature), since that combination hit 100% SPARQL on modest hardware with no fine-tuning or cloud dependency. But budget for the caveats before promising results: validate on the new domain beyond 21 co-evolved questions, treat the SPARQL-over-SQL gap as specific to auto-generated schemas, and confirm non-Qwen models and larger ontologies against local context-window and serving limits. The system-summary page itself warrants this caution — it states only that locally deployed Qwen3-family LLMs generate SPARQL and SQL, with all conclusions the authors' work, offering no independent deployment guarantees. See [[wiki/09-system-summary-and-conclusions|System Summary and Conclusions]].
