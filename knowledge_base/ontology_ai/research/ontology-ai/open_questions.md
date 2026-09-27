# Open questions — ontology_ai

Focus: What is ontology in AI, how are ontologies built, represented and evaluated, and how do they combine with LLMs and knowledge graphs for a working engineer?

> Seed file for the next run: each question below may become a new sub-topic. Derived ONLY from `topics/*/digest.md`. No answers here — questions only.

## 1. What counts as an ontology in AI practice, versus a taxonomy, a schema, or a knowledge graph?
- **Why it matters for the focus:** a working engineer cannot decide what to build — or reuse — without a practical boundary between ontologies (formal, logic-bearing) and lighter structures.
- **Sub-topic:** `01-ontology-foundations`

## 2. What is the standard ontology-engineering lifecycle, and where do LLMs versus humans belong at each stage?
- **Why it matters for the focus:** the digests show LLMs tried at every stage (requirements, implementation, publication, maintenance) in three roles (engineer, domain expert, evaluator), but with thin human-participant evidence — the engineer needs to know which stages to automate and which to keep human-led.
- **Sub-topic:** `01-ontology-foundations`

## 3. What shared benchmarks, task definitions, and metrics would make LLM-for-ontology work comparable and reproducible?
- **Why it matters for the focus:** fragmentation of tasks, datasets, metrics, and workflows plus weak reproducibility is the central finding — without standard evaluation the engineer cannot compare methods or trust reported gains.
- **Sub-topic:** `01-ontology-foundations`

## 4. How should ontology quality be evaluated functionally (competency-question coverage, consistency, signature compliance) rather than by lexical overlap?
- **Why it matters for the focus:** "how are ontologies evaluated" is core to the focus, and the digests point to CQ-as-SPARQL verification and validator gates without a settled, engineer-usable evaluation recipe.
- **Sub-topic:** `01-ontology-foundations`

## 5. When does a working engineer really need RDF/OWL, versus lighter representations (SQL schemas, JSON, SHACL-only shapes)?
- **Why it matters for the focus:** "how are ontologies represented" is core to the focus, and the planned practitioner-guidance comparison could not be made — the build-vs-simplify decision remains open.
- **Sub-topic:** `02-owl-rdf-sparql`

## 6. How can wrapper/mapping ontologies over opaque native vocabularies be built and maintained without manual effort?
- **Why it matters for the focus:** wrappers plus deterministic rewriting are the mechanism that extends controlled-semantics querying to uncontrolled endpoints, but they are currently manual — automation determines whether the pattern is production-viable.
- **Sub-topic:** `02-owl-rdf-sparql`

## 7. How should entity resolution and linking be handled in natural-language-to-SPARQL pipelines?
- **Why it matters for the focus:** entity resolution is explicitly out of scope in the current results, yet no working NL-to-query system ships without it — the gap blocks end-to-end deployment.
- **Sub-topic:** `02-owl-rdf-sparql`

## 8. Why do LLMs recover terms well but collapse on relations, hierarchies, and domain/range discipline — and what fixes it?
- **Why it matters for the focus:** the vocabulary-to-structure collapse (strong term F1, weak property/hierarchy/axiom F1, low signature compliance) is the key obstacle to "how ontologies are built" with LLMs.
- **Sub-topic:** `03-ontology-learning-llm-kg`

## 9. What retrieval-grounding and tool-access pattern scales ontology extension and extraction past context limits?
- **Why it matters for the focus:** per-question slice retrieval, live catalog-conditioned retrieval, and structured tool access all beat dumping raw OWL into context — the engineer needs the settled pattern with token budgets and reuse rules.
- **Sub-topic:** `03-ontology-learning-llm-kg`

## 10. What deterministic normalization, fusion, and deduplication layer is needed to merge LLM-extracted triples safely?
- **Why it matters for the focus:** combining LLMs with knowledge graphs for production requires merge-safe output (no duplicates, no false merges, no hallucinated entities) — the rule-based plus embedding dedup design space is still open.
- **Sub-topic:** `03-ontology-learning-llm-kg`

## 11. What validation gates and human-review loops turn fluent LLM drafts into committable ontology and graph changes?
- **Why it matters for the focus:** syntax gates, consistency checkers, pitfall scanners, and engineer verification ratings appear in every pipeline but as an ad hoc bundle — the engineer needs the minimal reliable gate sequence for "how ontologies combine with LLMs and KGs."
- **Sub-topic:** `03-ontology-learning-llm-kg`

## 12. How do ontology design choices for LLM consumption (naming, labels, comments, explicit types) affect downstream accuracy?
- **Why it matters for the focus:** naming and annotation discipline reportedly dominates model choice and prompting in query accuracy, but the generalizable authoring rules for LLM-consumable ontologies are not settled.
- **Sub-topic:** `03-ontology-learning-llm-kg`
