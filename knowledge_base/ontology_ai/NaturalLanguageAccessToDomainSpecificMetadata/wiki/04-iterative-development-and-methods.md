> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Iterative Development and Research Methods
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
---
## 3.3 Iterative Development
**Covers:** Section 3.3

Ontology development is not a one-time design step: the ontology, competency questions, and domain-specific prompt rider co-evolve through testing, where running test cases reveals gaps feeding back into all three:

- A property name that confuses the LLM gets renamed in the ontology (e.g., adding skos:altLabel "pseudonym" to hasSubjectId when users say "pseudonym" instead of "subject ID").
- A recurring LLM mistake gets addressed by a new directive in the domain-specific prompt rider (e.g., "return experiment IDs, not instance URIs").
- A new user question that the system handles poorly becomes a new competency test case.

> "This cycle is lightweight: each iteration is a small change to one of the three artifacts, followed by re-running the test suite."

It requires domain knowledge and comfort with iterative testing, but no machine learning, database, or SPARQL expertise; the result is a progressively refined system where the ontology captures the domain vocabulary and the test cases capture the query patterns.

## 4.1 Test Driver Framework
**Covers:** Section 4.1

The test driver is the foundation of both domain development and research evaluation. Given a competency question (NL), a reference SPARQL query, and expected results, the driver calls the LLM, extracts the generated query, executes it against the appropriate backend, and compares results.

Combinatorial sweep parameters per competency question:

- LLM model: different model families, sizes, and quantization variants
- Temperature: controls generation randomness (e.g., 0.0, 0.2)
- System prompt: different prompt formulations and domain-specific riders
- Ontology representation: full Turtle, no-comments, compact, abstract, etc.
- Query backend: SPARQL or auto-generated SQL (with or without column comments)
- Repetitions: multiple runs per configuration to assess variability
- Fix-retry policy: number of LLM correction attempts on syntax errors

Results are logged to CSV with per-query timing, match status, and fix-retry outcomes. A walker script orchestrates the driver across all test cases and configurations, with parallel execution across models. The SQL evaluation uses a separate test driver against PostgreSQL with tolerant comparison (column name normalization, order-independent row matching, and URI prefix stripping) to handle differences between SQL output and SPARQL reference data.

## 4.2 Virtual Ontology Representations
**Covers:** Section 4.2

To measure which ontology features different LLMs rely on, eight representations of the same ontology are evaluated, generated automatically from the full OWL Turtle:

| Representation | Definition in chunk |
|---|---|
| default | Full OWL Turtle with domain, range, comments, labels |
| no-comments | Turtle with rdfs:comment and rdfs:label stripped |
| compact | One-line-per-property listing class memberships |
| compact-typed | Compact with datatype annotations retained |
| compact-grouped | Properties grouped by domain class |
| raw-graph | RDF triples in N-Triples format |
| abstract-dict | Dictionary mapping generic keys to values |
| abstract-graph | Graph with anonymized node/edge labels |

These form an ablation study: moving from default to abstract-graph progressively strips semantic information, revealing which features the LLM relies on.

## 4.3 Automatic Generation of SQL Database
**Covers:** Section 4.3

A generic OWL-to-SQL converter reads the domain ontology and automatically derives a PostgreSQL 17 schema:

- Each OWL class becomes a table.
- Each datatype property becomes a column (typed from rdfs:range).
- Object properties become foreign keys (direction inferred from owl:inverseOf).
- Ontology annotations (rdfs:comment, rdfs:label, skos:altLabel) are converted to SQL column comments.

The same KG data is loaded into the relational schema (6 tables, 182 columns for the largest table). A system prompt analogous to the SPARQL prompt provides the Data Definition Language (DDL) schema (with or without comments) and instructs the LLM to generate SQL instead of SPARQL. A SQL test driver evaluates the same competency questions against PostgreSQL using tolerant comparison to match SQL results against SPARQL reference data.

## 4.4 Models and Hardware
**Covers:** Section 4.4

Eight model variants from the Qwen3 family are evaluated, spanning 8B to 35B parameters, including dense and mixture-of-experts (MoE) architectures and quantized variants for production deployment. All served locally. HW: A=AMD MI300A APU (HPC), N=4×NVIDIA RTX5000 (institutional).

| Model | Params | Type | Ctx | Server | HW |
|---|---|---|---|---|---|
| Qwen3-8B | 8B | Dense | 41K | vLLM | A |
| Qwen3-14B | 14B | Dense | 41K | vLLM | A |
| Qwen3-Coder-30B-A3B | 30B/3B | MoE | 64K | vLLM | A |
| Qwen3.6-27B | 27B | Dense | 64K | vLLM | A |
| Qwen3.6-27B-FP8 | 27B | Dense/FP8 | 64K | vLLM | A |
| Qwen3.6-27B-Q8_0 | 27B | Dense/Q8 | 32K | llama.cpp | N |
| Qwen3.6-35B-A3B | 35B/3B | MoE | 64K | vLLM | A |
| Qwen3.6-35B-A3B-FP8 | 35B/3B | MoE/FP8 | 64K | vLLM | A |

Models are served on two GPU systems: AMD Instinct MI300A APUs (128GB HBM3 per APU) at a shared HPC facility via vLLM, and an institutional 4× Quadro RTX 5000 system (64GB total VRAM) via llama.cpp for the Q8 variant. The Quadro RTX 5000 based system (AMD CPU, 256GB main memory, 4×16GB GPU VRAM) is vintage 2020 hardware and serves as the production deployment target. Context windows range from 32K to 64K tokens. The full OWL Turtle ontology (80KB, approximately 18K tokens) and the SQL schema with comments are each provided in the system prompt, requiring models that can handle substantial context.
