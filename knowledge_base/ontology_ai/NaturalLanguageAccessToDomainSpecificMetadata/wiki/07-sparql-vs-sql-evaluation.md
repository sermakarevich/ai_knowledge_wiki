> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# SPARQL vs SQL Evaluation

**In one sentence:** On 21 natural-language questions the ontology-driven SPARQL path scores 21/21 (100%) versus 12/21 (57%) for mechanically derived SQL, a gap the authors attribute to structural OWL advantages — annotations, domain/range grouping, inverse properties — plus an EAV control at 11/21, all achieved on older local hardware.

## Key points

- Per-question totals are SPARQL 21/21 (100%) versus SQL 12/21 (57%) on the same 21-question set.
- Stripping `rdfs:comment` drops SPARQL accuracy from 100% to 81%, while stripping equivalent SQL column comments drops SQL from 57% to 43%, showing annotations are critical for both backends.
- `rdfs:range` determines SQL column types and `rdfs:domain` determines table placement, but the explicit class-level grouping visible in Turtle is flattened into a column list the LLM must parse without the same semantic scaffolding.
- `owl:inverseOf` lets the LLM traverse a relationship in either direction (e.g. `mro:aStudyHasExperiment` or `mro:isExperimentOfStudy` interchangeably), whereas SQL has one foreign key and the LLM must know which table owns it and JOIN from the correct side.
- An Entity-Attribute-Value alternative (narrow three-column `entity_id, attribute, value` per class, one fact per row, auto-derived from the same ontology) reaches only 11/21 (52%) with comments and 2/21 (10%) without.
- EAV's key difficulty is that relationship attributes store prefixed entity identifiers (e.g. `study_101`) rather than clean values (`101`); SPARQL operates on variables and property patterns and never exposes internal identifiers, while wide-table SQL foreign keys reference clean primary keys.
- The Q8-quantized model (Q36.27B.Q) on 4× Quadro RTX 5000 GPUs — a machine several generations old — achieves the 100% SPARQL accuracy and the highest SQL accuracy (57%), so the approach does not require recent-generation GPUs.

---

## Per-question SPARQL vs SQL results

| Q# | Query | SPARQL OK | s | SQL OK | s |
|---|---|---|---|---|---|
| 1 | Experiments in a study | ✓ | 4 | ✓ | 4 |
| 2 | Experiments for a subject | ✓ | 5 | ✓ | 5 |
| 3 | All experiments for a subject | ✓ | 5 | ✓ | 4 |
| 4 | Same as Q3, rephrased | ✓ | 6 | ✓ | 8 |
| 5 | Two protocol name patterns | ✓ | 9 | ✓ | 8 |
| 6 | Experiment details with demographics | ✓ | 10 | ✓ | 9 |
| 7 | Dataset name, acq date and time | ✓ | 7 | × | 6 |
| 8 | All properties on a dataset | ✓ | 5 | × | 113 |
| 9 | Acquisition dates sorted | ✓ | 7 | × | 7 |
| 10 | Age filter with date range | ✓ | 9 | ✓ | 8 |
| 11 | Subject demographics for a study | ✓ | 10 | × | 8 |
| 12 | Datasets matching coil substring | ✓ | 9 | ✓ | 12 |
| 13 | Datasets matching exact coil | ✓ | 8 | ✓ | 9 |
| 14 | Experiments after 4pm, sorted | ✓ | 9 | × | 10 |
| 15 | Experiments in duration range | ✓ | 12 | ✓ | 13 |
| 16 | Experiments for a coil with date | ✓ | 9 | × | 8 |
| 17 | Studies with scanner hours | ✓ | 11 | × | 12 |
| 18 | Ontology classes and properties | ✓ | 15 | × | 8 |
| 19 | Coils used in a date range | ✓ | 10 | ✓ | 12 |
| 20 | Top N coils by experiment count | ✓ | 9 | × | 10 |
| 21 | Datasets on experiment, sorted | ✓ | 6 | ✓ | 7 |
| | Total | 21/21 | | 12/21 | |

**Covers:** per-question result table (Q1–Q21, SPARQL vs SQL OK/s columns).

## 6.2 SPARQL vs SQL: What the Ontology Provides

> "The gap between SPARQL and SQL accuracy (100% vs 57%) shows that while readable naming helps both, OWL provides structural advantages that SQL DDL lacks:"

- **Annotations.** "Stripping rdfs:comment from the SPARQL ontology drops accuracy from 100% to 81%. Stripping the equivalent SQL column comments drops accuracy from 57% to 43%. Annotations are critical for both backends, consistent with Wretblad et al. [30]."
- **Domain and range declarations.** "In our conversion, rdfs:range determines SQL column types and rdfs:domain determines table placement. These are preserved in the DDL, but the explicit class-level grouping visible in the Turtle ontology is flattened into a column list that the LLM must parse without the same semantic scaffolding."
- **Inverse properties.** "In SPARQL, owl:inverseOf allows the LLM to traverse any relationship in either direction. A query can use mro:aStudyHasExperiment or mro:isExperimentOfStudy interchangeably. In SQL, there is one foreign key, and the LLM must know which table owns it and JOIN from the correct side. The SQL system prompt must explicitly encode join directions, while the SPARQL ontology encodes them structurally."
- **Entity-Attribute-Value schema.** "As an alternative to the wide-table SQL schema (one column per property, NULLs where properties are absent), we also evaluated an Entity-Attribute-Value (EAV) representation: a narrow three-column table (entity_id, attribute, value) per class, where each row stores a single fact. This schema was automatically derived from the same ontology. EAV accuracy reached only 11/21 (52%) with the best model and comments, dropping to 2/21 (10%) without comments."
- **EAV identifier problem.** "A key difficulty is that relationship attributes in EAV store prefixed entity identifiers (e.g., study_101) rather than clean values (101) that the LLM can reason about directly. In SPARQL, the LLM never sees internal identifiers because it operates on variables and property patterns. In wide-table SQL, foreign keys reference clean primary keys. EAV exposes internal naming conventions to the query generator, requiring a domain-specific prompt rider to teach the convention. This represents a structural disadvantage that readable naming alone cannot overcome."
- **Scope of the comparison.** "This result does not show that SPARQL is generally easier for LLMs to generate than SQL. Vejvar and Fujimoto [24] report the opposite ordering under terse schema linearizations, and Sequeda et al. [21] report a KG advantage on an enterprise schema; the ordering depends on how much semantic structure each representation carries. Both relational schemas here were derived mechanically from the ontology. A relational schema designed by hand for these questions, with denormalized views, natural keys, and documented join paths, would likely narrow the gap."

**Covers:** §6.2 (annotation ablation, domain/range, inverses, EAV experiment, scope caveat).

## Local hardware result

- "The Q8-quantized model (Q36.27B.Q) running on 4× Quadro RTX 5000 GPUs (a machine several generations old) achieves 100% SPARQL accuracy and the highest SQL accuracy (57%), demonstrating that the approach does not require recent-generation GPUs."
- "This matters for institutions with privacy constraints (e.g., GDPR for human subject data) that must deploy LLMs locally."
- "Published benchmark estimates [12] indicate that Apple Silicon workstations with 128GB unified memory can run quantized 27B to 35B models at roughly 25–50 tokens per second via MLX or llama.cpp."
- "The low idle power consumption of these systems makes them practical for always-on deployment, and the large unified memory leaves headroom for growing ontologies requiring larger context windows."

**Covers:** quantized-model / local-deployment paragraph preceding §6.

## 6 Discussion — 6.1 The Ontology as Single Source of Truth

- "The central finding is that co-designing an LLM-friendly domain ontology along with the ETL logic building the KG and the domain-specific system prompt rider yields far better results than designing any one of these components independently, or worse, accepting existing components as a given."
- "A related finding is that ontology-driven SPARQL queries are easier for an LLM to generate accurately than an equivalent SQL query on a relational model."
- "Experience with a neuroimaging demonstration domain shows that end users can create well-formed natural language queries where they would not take the time to learn and write SPARQL or SQL queries."
- "Finally, we have found that we can run this service on local LLMs using older or less expensive hardware. It is likely that for domains without privacy constraints, cloud-based frontier LLMs with larger context windows would be faster and more capable."

**Covers:** §6–6.1 discussion paragraphs present in the chunk.
