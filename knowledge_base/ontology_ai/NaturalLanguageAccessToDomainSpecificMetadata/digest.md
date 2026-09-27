> [[index|Wiki]] | [[summary|Summary]]

# Natural Language Access to Domain-Specific Metadata: A Reusable Framework for LLM Query Generation — Digest

## 1. [[wiki/01-overview-and-framework-intro|Overview and Framework Intro]]

**In one sentence:** When domain vocabulary and semantics are captured in a well-designed OWL ontology, LLMs can generate accurate structured queries zero-shot — without fine-tuning, retrieval augmentation, or multi-agent orchestration — via the NLKGQ framework demonstrated on a large MRI archive with 100% accuracy on a 21-question test set.

## Key points
- The NLKGQ (Natural Language Knowledge Graph Query) system provides a domain-agnostic harness that translates natural language questions to SPARQL via an LLM and executes them against a knowledge graph, plus a web interface for posing questions.
- The development process starts by capturing domain vocabulary and semantics in a formal OWL ontology, then a domain-specific ETL pipeline extracts archive metadata into a KG defined by that ontology.
- Both the framework and the process are designed for reuse across multiple domains; the demonstration domain is metadata from a large-scale neuroimaging (MRI) research archive.
- Best configurations reach 100% accuracy on a 21-question competency and regression test set developed with domain experts.
- An ablation across eight ontology representations shows readable entity names and semantic annotations are the dominant accuracy factors, more significant than model choice or prompt engineering.
- Comparing SPARQL against an auto-generated SQL database with equivalent data shows OWL's structural features give a substantial advantage over SQL DDL for LLM-driven query generation.
- The demonstration evaluates 8 locally deployed LLM variants (8B to 35B parameters, including quantized and mixture-of-experts variants), with the best model at 100% on SPARQL and 57% on auto-generated SQL; stripping ontology annotations degrades SPARQL accuracy by 19 percentage points.
- The demonstration constraint is privacy-driven: human-subject data under GDPR must stay on institutional infrastructure, so the goal includes finding the smallest locally runnable model on modest hardware.

## 2. [[wiki/02-background-and-annotation-impact|SQL by 14, revealing the importance]]

**In one sentence:** Related work shows LLM query accuracy hinges on semantic annotations and schema representation — not query language alone — with enterprise SQL failing at 0–16%, knowledge-graph/SPARQL variants reaching 54–100%, and ontology representation alone causing a 90-point accuracy spread.

## Key points
- The paper claims four contributions: the NLKGQ framework and ontology-first process for NL access to domain-specific metadata demonstrated on neuroimaging data; evaluation over 8 models, 8 ontology representations, and 768 configurations (over 16,000 runs) showing ontology design dominates accuracy; a generic OWL KG-to-SQL generator enabling SPARQL vs SQL comparison on identical NL questions; and analysis of OWL's structural advantages over SQL DDL for LLM query generation.
- Traditional KGQA (entity linking plus relation prediction) has been extended by LLMs via fine-tuning (SGPT; Zhang et al. GAIL for low-resource KGQA), multi-agent/pipeline orchestration (AGENTiGraph with 95% classification accuracy on a 3,500-query benchmark; CyberBOT with RAG plus ontology-based post-hoc verification), in-context learning with retrieved examples (D'Abramo et al.), query-time graph exploration (GRASP, state-of-the-art on Wikidata zero-shot), and exploratory interfaces (Rhizomer-LLM on BESDUI).
- Rhizomer-LLM's BESDUI evaluation is complementary rather than comparable because it measures task completion, not answer correctness, since, in the authors' words, "semantic correctness cannot be automatically verified", whereas this paper reports execution-level correctness against a reference query for every competency question.
- In text-to-SQL, GPT-4o achieves 0% execution accuracy on real enterprise schemas with hundreds of tables (BEAVER), failures traced to schema retrieval and column mapping; adding column descriptions improves accuracy by over 20% on uninformative columns (Wretblad et al.), and schema presentation directly affects accuracy (Rajkumar et al.).
- Knowledge graphs provide a structural advantage on the same enterprise questions, raising accuracy from 16% (SQL) to 54% (SPARQL) (Sequeda et al.); the authors' controlled ontology is smaller in vocabulary than public KGs like Wikidata or DBpedia but describes large data volumes with compact classes and properties, unlike approaches that cope with unchangeable public ontologies with opaque identifiers.
- For text-to-SPARQL, Giuliani et al.'s heuristic advice (prefer expressive labels over cryptic identifiers) rests on a confounded GPT-3.5 improvement from 0.08 to 0.60 combining renaming, added axioms, and query filtering, whereas this paper's ablation (Table 4) holds model, prompt, and benchmark fixed and isolates a 90-point spread from ontology representation alone, from 100% (default) to 10% (abstract-graph).
- SparqLLM's accuracy depends mostly on its 360 hand-authored query templates rather than zero-shot capability (relaxed-match drops from 66.7% to 55.3% without template retrieval), while this approach needs no per-question templates because the ontology supplied once in the system prompt provides the semantic scaffolding; against Vejvar and Fujimoto's terse-linearization result where SPARQL trails SQL (17.2% vs 29.7% with fine-tuned uT5), the full annotated OWL ontology in context reverses this to 100% SPARQL vs 57% auto-generated SQL.

## 3. [[wiki/03-ontology-richness-and-design-principles|Ontology Richness and Design Principles]]

**In one sentence:** Schema and ontology richness — not the query language itself — determines which backend an LLM can query more reliably, so the authors design finite-size OWL ontologies for LLM consumption with six expressive-naming principles and compare SPARQL and SQL backends derived from the same ontology, data, and models.

## Key points
- Central claim: schema and ontology richness, not the query language itself, determines which backend an LLM can query more reliably.
- Rasheed and Aguado [18] test reduced/condensed ontology prompt formats but take the KG ontology as given to fit it into the prompt, rather than designing the ontology for LLM consumption from the start.
- The work targets finite-size domain-specific ontologies that fit in the LLM context window, and measurements show departing from expressive naming of ontological elements hurts accuracy.
- No prior work addresses the end-to-end reusable process — capture domain vocabulary in a formal ontology, build a KG from domain metadata via ETL, and enable LLM-driven NL querying — while prior work treats the ontology/schema as given and focuses on query generation.
- Controlled comparison: unlike Sequeda et al. [21], who compare SQL vs SPARQL across different schemas and datasets, the authors auto-generate a relational schema from the same authoritative ontology and evaluate both backends on the same competency questions with the same readable naming, data, and LLM models.
- Contribution has two parts: a development process — (1) capture vocabulary in OWL, (2) build a KG via ETL, (3) iterate ontology, competency questions, and prompt rider together until accuracy is acceptable — and a domain-agnostic reusable framework (NLKGQ query server, web application, combinatorial test driver) that also supports production deployment.
- ETL/KG facts: Python pipeline with rdflib [19] maps DICOM headers, NIfTI sidecars [7, 11], Siemens TWIX raw headers, experiment registry, and participant management system [13] to MRO terms, producing ~10 million triples from a 180TB MRI archive loaded into Apache Jena Fuseki [2] for SPARQL 1.1 [27] querying.
- NLKGQ server builds a system prompt of (1) generic SPARQL instructions, (2) the complete domain ontology in OWL Turtle, and (3) a small domain-specific rider, then applies harness fixes (strip `<think>` blocks, extract SPARQL from markdown, fix PREFIX declarations from ontology ground truth, optional error-feedback retry that mainly helps smaller models with syntax errors).

## 4. [[wiki/04-iterative-development-and-methods|Iterative Development and Research Methods]]

**In one sentence:** Ontology, competency questions, and the domain-specific prompt rider co-evolve through lightweight test-driven iterations, supported by a test-driver framework with combinatorial sweeps, eight virtual ontology representations, an automatic OWL-to-SQL converter, and eight Qwen3 model variants on two GPU systems.

## Key points
- Ontology, competency questions, and the domain-specific prompt rider co-evolve: test runs reveal gaps that feed back into all three artifacts, and each iteration is a small change followed by re-running the test suite.
- Confusing property names are fixed in the ontology (e.g., adding skos:altLabel "pseudonym" to hasSubjectId), recurring LLM mistakes are fixed with new prompt-rider directives (e.g., "return experiment IDs, not instance URIs"), and poorly handled new questions become new competency test cases.
- The iteration cycle requires domain knowledge and comfort with iterative testing but no machine learning, database, or SPARQL expertise.
- The test driver evaluates each competency question (NL, reference SPARQL, expected results) by calling the LLM, extracting and executing the generated query, and comparing results, with combinatorial sweeps over model, temperature (e.g., 0.0, 0.2), system prompt, ontology representation, query backend, repetitions, and fix-retry policy.
- Results are logged to CSV with per-query timing, match status, and fix-retry outcomes, orchestrated by a walker script with parallel execution; the SQL driver uses tolerant comparison (column name normalization, order-independent row matching, URI prefix stripping).
- Eight virtual ontology representations auto-generated from full OWL Turtle (default, no-comments, compact, compact-typed, compact-grouped, raw-graph, abstract-dict, abstract-graph) form an ablation study that progressively strips semantic information.
- A generic OWL-to-SQL converter derives a PostgreSQL 17 schema (each OWL class becomes a table, datatype properties become columns typed from rdfs:range, object properties become foreign keys with direction from owl:inverseOf, annotations become column comments), loading the same KG data into 6 tables with 182 columns in the largest table.
- Eight Qwen3 variants (8B to 35B parameters, dense and MoE, including FP8/Q8_0 quantized variants) are served locally on AMD MI300A APUs (128GB HBM3 per APU) via vLLM and a 4× Quadro RTX 5000 system (64GB total VRAM) via llama.cpp, with context windows of 32K–64K tokens against an 80KB (~18K-token) ontology.

## 5. [[wiki/05-framework-architecture-and-production-system|Figure 3: Framework Architecture Showing Production]]

**In one sentence:** Although titled for Figure 3 (production solid vs research dashed components), the chunk body actually details the evaluation protocol, three generated SPARQL examples, the 21-question competency set, and SPARQL accuracy results by model and ontology representation.

## Key points
- Only architecture fact present is the caption: "Figure 3: Framework architecture showing production components (solid) and research infrastructure (dashed)."
- Evaluation uses 21 competency and regression questions with NL question, reference SPARQL, and expected results in SPARQL Results JSON format; primary metric is result match after canonicalization (row order ignored, variable names normalized), with accuracy as fraction matched.
- SPARQL evaluation grid is 8 models × 8 ontology representations × 3 prompts × 4 temperatures, yielding over 16,000 runs; SQL evaluation is 8 models × 2 schema variants (with/without column comments) × 4 temperatures.
- On syntax error, the harness sends query plus error back to the LLM for up to two correction attempts, rarely used with production-chosen LLMs; even the smallest 32K (Q8 model) context window had ample headroom with no overflow errors.
- Three zero-shot Qwen3.6-27B examples (default ontology) are shown: simple lookup for study 101, multi-entity join with subject demographics and acquisition date, and filtered aggregation for study 42 (age > 42, date before June 2025) using FILTER(xsd:integer(?PatientAge) > 42) and FILTER(?date < "2025-06-01"^^xsd:date).
- SPARQL model results: both 27B dense variants (full-precision and Q8) reach 100% on full Turtle ontology, Q8 on older hardware (N) is 1.8× slower but equally accurate as full-precision on HPC (A); 35B MoE peaks at 57%, and accuracy rises 24% (8B) through 38% (14B) to 100% (27B dense).
- Ontology representation results: only default full OWL Turtle reaches 100%; stripping rdfs:comment and rdfs:label drops to 81%; compact name-retaining forms reach 62–71% (compact 62%, compact-typed 71%); abstract generic-identifier forms collapse to 5–19% (abstract-dict 19%); prompt sizes range 1.7K (compact) to 17.6K (default) tokens against an 80KB ontology.

## 6. [[wiki/06-model-comparison-results|Model Comparison Results]]

**In one sentence:** The best SPARQL setup reaches 100% accuracy (21 questions) with the default ontology at temperature 0.0, while the best auto-SQL setup reaches only 57%, and accuracy falls sharply with weaker models or impoverished ontology representations.

## Key points
- Best SPARQL per model: Q36.27B.D (Qwen3.6-27B) and Q36.27B.Q (Qwen3.6-27B-Q8_0) both reach 100% on the default ontology at temp 0.0, with 8.1s/17.6K tokens (baseline) and 14.6s/17.7K tokens (procedural) respectively.
- The FP8 variant Q36.27B.F reaches 95% (default ontology, temp 0.0, guardrails, 7.9s, 17.8K tokens), while smaller/weaker models drop to 57% (Q30.30B.C, Q36.35B.F, Q36.35B.M), 38% (Q30.14B.D), and 24% (Q30.08B.D).
- Across ontology representations (Table 4), default hits 100%, then no-comments 81%, compact-typed 71%, compact-grouped 67%, compact 62%, raw-graph 48%, abstract-dict 19%, and abstract-graph 5%.
- With the default ontology, all three prompts reach 100% (baseline 8.1s, guardrails 8.3s, procedural 8.5s, all Q36.27B.D at temp 0.0), plus procedural with Q36.27B.Q at 14.6s.
- Across temperatures (Table 6, default ontology), temp 0.0 gives 100% (four configurations), temp 0.2 gives 95%, temp 0.4 gives 90%, and temp 0.6 gives 90%.
- Best auto-SQL accuracy (Table 7, wide-table schema) is 12/21 (57%) with comments vs 9/21 (43%) without, achieved by Q36.27B.Q; all other models score 52% or lower with comments.
- Ontology-derived column comments add 3 correct cases for the best SQL model (43% without to 57% with), described as "a considerably larger effect than stripping annotations from the SPARQL ontology (100% to 81%)".

## 7. [[wiki/07-sparql-vs-sql-evaluation|SPARQL vs SQL Evaluation]]

**In one sentence:** On 21 natural-language questions the ontology-driven SPARQL path scores 21/21 (100%) versus 12/21 (57%) for mechanically derived SQL, a gap the authors attribute to structural OWL advantages — annotations, domain/range grouping, inverse properties — plus an EAV control at 11/21, all achieved on older local hardware.

## Key points
- Per-question totals are SPARQL 21/21 (100%) versus SQL 12/21 (57%) on the same 21-question set.
- Stripping `rdfs:comment` drops SPARQL accuracy from 100% to 81%, while stripping equivalent SQL column comments drops SQL from 57% to 43%, showing annotations are critical for both backends.
- `rdfs:range` determines SQL column types and `rdfs:domain` determines table placement, but the explicit class-level grouping visible in Turtle is flattened into a column list the LLM must parse without the same semantic scaffolding.
- `owl:inverseOf` lets the LLM traverse a relationship in either direction (e.g. `mro:aStudyHasExperiment` or `mro:isExperimentOfStudy` interchangeably), whereas SQL has one foreign key and the LLM must know which table owns it and JOIN from the correct side.
- An Entity-Attribute-Value alternative (narrow three-column `entity_id, attribute, value` per class, one fact per row, auto-derived from the same ontology) reaches only 11/21 (52%) with comments and 2/21 (10%) without.
- EAV's key difficulty is that relationship attributes store prefixed entity identifiers (e.g. `study_101`) rather than clean values (`101`); SPARQL operates on variables and property patterns and never exposes internal identifiers, while wide-table SQL foreign keys reference clean primary keys.
- The Q8-quantized model (Q36.27B.Q) on 4× Quadro RTX 5000 GPUs — a machine several generations old — achieves the 100% SPARQL accuracy and the highest SQL accuracy (57%), so the approach does not require recent-generation GPUs.

## 8. [[wiki/08-limitations-and-unmeasured-gaps|Limitations and Unmeasured Gaps]]

**In one sentence:** The SPARQL-over-SQL advantage comes from OWL representation scaffolding lost in mechanical OWL-to-DDL translation, but the size of that gap is explicitly unmeasured, and the single-domain, 21-question, Qwen3-only evaluation with auto-generated SQL baselines limits generalization.

## Key points
- The representation comparison holds data, naming, annotations, questions, and models constant, isolating the effect of representation: OWL carries domain/range declarations, inverse properties, and class-level grouping as first-class structure that mechanical translation to DDL partly loses.
- The reported SPARQL advantage is specific to SQL schemas auto-generated from the ontology, not schemas designed by a database expert, and the gap magnitude is explicitly unmeasured.
- Qwen3 35B MoE variants peaked at 57% while 27B dense models reached 100% despite fewer total parameters, indicating dense models are the better choice at a given compute budget for structured generation requiring precise schema adherence.
- The simplest baseline prompt with the fewest instructions achieved the highest peak accuracy, with more elaborate guardrail and procedural prompts performing comparably but not better.
- Q8 GGUF quantization preserved accuracy completely at 100% matching full precision, while FP8 quantization showed a small drop to 95%.
- The evaluation is limited to one MRI metadata domain, 21 expert-developed competency questions co-evolved with the ontology and prompt rider, Qwen3-family models only, Jena Fuseki in Docker for metadata volume, and LLM context-window bounds on ontology complexity.

## 9. [[wiki/09-system-summary-and-conclusions|System Summary and Conclusions]]

**In one sentence:** This chunk contains almost no summary or conclusion prose — only the statement that the paper's system uses locally deployed Qwen3-family LLMs for SPARQL and SQL query generation, followed by the paper's reference list ([1]–[35]).

## Key points
- The chunk states the paper's system uses locally deployed LLMs for query generation.
- The LLM family named in the chunk is the Qwen3 family.
- The chunk states the system generates both SPARQL and SQL queries.
- The chunk states this system is the subject of the research described in the paper.
- The chunk attributes all scientific content, experimental design, analysis, and conclusions to the authors.
- Apart from those two sentences, the chunk consists entirely of the reference list, entries [1] through [35].
- The chunk provides no metrics, mechanisms, takeaways, or conclusion claims beyond the sentences quoted below.

## The argument in five moves

1. Researchers cannot easily query rich domain archives, so the work proposes an ontology-first path: capture vocabulary in OWL, build a KG via ETL, and let an LLM generate zero-shot queries through the reusable NLKGQ harness (pages 1, 3).
2. Prior work treats schemas as given and accuracy hinges on annotations and representation — enterprise SQL at 0–16%, KG/SPARQL at 54–100% — motivating design of the ontology for LLM consumption with six expressive-naming principles (pages 2, 3).
3. Ontology, competency questions, and prompt rider co-evolve through a combinatorial test driver (8 models × 8 ontology representations × prompts × temperatures, 16,000+ runs; auto OWL-to-SQL; local Qwen3 8B–35B hardware) over 21 expert questions (pages 4, 5).
4. Results isolate representation as dominant: default Turtle hits 100% SPARQL (27B dense, temp 0.0, any prompt) while stripping comments costs 19 points, compact/abstract forms collapse to 5–71%, and auto-SQL peaks at only 57% (12/21), with OWL inverses, domain/range grouping, and annotations explaining the gap plus an EAV control at 52% (pages 5, 6, 7).
5. The gap is scoped to auto-generated SQL baselines (hand-designed schemas unmeasured), dense 27B beats 35B MoE, simple prompts and Q8 quantization suffice on old local GPUs for GDPR privacy, but single-domain, 21-question, Qwen3-only limits demand cross-domain and model-diversity follow-ups (pages 7, 8, 9).
