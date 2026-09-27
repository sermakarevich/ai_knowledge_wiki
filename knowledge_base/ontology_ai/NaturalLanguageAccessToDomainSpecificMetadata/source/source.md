# Natural Language Access to Domain-Specific Metadata: A Reusable Framework for LLM Query Generation
Source: https://arxiv.org/abs/2607.18029v2
Kind: pdf
Fetched: 2026-09-23T12:59:48.596313+00:00
Tool: pdftotext
Research-Target: /Users/sergii/.ai/knowledge/research_topics/ontology_ai/research/ontology-ai
Topic: ontology_ai

                                                   Natural Language Access to Domain-Specific Metadata:
                                                    A Reusable Framework for LLM Query Generation
                                                                   Blake G. Fitch                                                  Cato Elia Kurtz
                                                         blake.fitch@tuebingen.mpg.de                              Max Planck Institute for Biological Cybernetics
                                                  Max Planck Institute for Biological Cybernetics                              Tübingen, Germany
                                                              Tübingen, Germany

                                         Abstract                                                              language and the domain vocabulary. Many researchers lack the
                                         Researchers need to answer ad-hoc questions about the contents        expertise to effectively access the information they need without
                                         of domain-specific archives but often lack the expertise to write     assistance.




arXiv:2607.18029v2 [cs.DB] 10 Sep 2026
                                         structured queries on the metadata. We show that when domain             Large language models (LLMs) can generate structured queries
                                         vocabulary and semantics are captured in a well-designed Web          from natural language (NL), but their accuracy depends on how
                                         Ontology Language (OWL) ontology, Large Language Models               the underlying data schema is presented. On simple schemas like
                                         (LLMs) can generate accurate structured queries zero-shot, that is,   Spider [31], top models exceed 90% accuracy, but on real enterprise
                                         without task-specific fine-tuning examples, retrieval augmentation,   schemas with hundreds of tables, GPT-4o drops to 0% [3]. Sequeda
                                         or multi-agent orchestration. We present the Natural Language         et al. [21] find that reformulating the same enterprise questions
                                         Knowledge Graph Query (NLKGQ) system, a framework and                 over a knowledge graph raises accuracy from 16% to 54%. How
                                         development process that enables natural language access to meta-     domain knowledge is structured matters as much as which LLM
                                         data in such archives. The framework includes a web interface         model is used.
                                         that helps researchers pose natural language questions, which a          In this paper, we present an ontology-first process for enabling
                                         domain-agnostic harness translates to SPARQL via an LLM and           NL access to domain-specific metadata, a generic framework of tools
                                         executes against a knowledge graph. The development process           to facilitate deployment, and measured results searching metadata
                                         begins with capturing domain vocabulary and semantics in a            on a large MRI image archive. The process begins with capturing the
                                         formal OWL ontology. Domain-specific code then extracts meta-         domain vocabulary and semantics in a formal OWL ontology [26]
                                         data from archive sources and imports it into a knowledge graph       using readable entity names and semantic annotations. A domain-
                                         defined by the ontology. Both the framework and process are           specific Extract-Transform-Load (ETL) pipeline maps archive meta-
                                         designed to support reuse across multiple domains. In this work,      data to the ontology, producing a knowledge graph (KG). Using
                                         we demonstrate the system for metadata derived from a large-scale     the KG stored in RDF Turtle format, we load both a SPARQL data-
                                         neuroimaging research archive, evaluating performance across          base and, via automatic transformation, an SQL database, enabling a
                                         multiple LLMs and ontology representations. The best configu-         systematic comparison of both as targets for LLM-generated queries
                                         rations achieve 100% accuracy on a 21-question competency and         with equivalent data and NL questions. An LLM generates correct
                                         regression test set developed with domain experts. An ablation        queries against either backend, zero-shot, with the full ontology or
                                         study across eight ontology representations reveals that readable     derived schema provided in full, in the system prompt.
                                         entity names and semantic annotations are the dominant factors           The domain-specific ontology, competency and regression test
                                         in accuracy, more significant than model choice or prompt engi-       cases, and a domain-specific prompt rider evolve together through
                                         neering. We also compare SPARQL to an auto-generated SQL data-        iterative testing. During this process, the vocabulary and semantics
                                         base as query backends, showing that OWL’s structural features        of the domain are refined in increasing detail, progressively elimi-
                                         provide a substantial advantage over SQL DDL for LLM-driven           nating confusion and inaccuracies that plague even expert human
                                         query generation. A notable consideration for our demonstration       communication.
                                         domain is a requirement to run local LLMs on modest institutional        We demonstrate this process on an MRI neuroimaging research
                                         hardware in support of privacy concerns for human subject data.       archive [5] containing metadata for 80 active studies with 2,000
                                                                                                               MRI experiments. Since this archive contains human subject data,
                                         Keywords                                                              privacy regulations (GDPR) require that all processing remain on
                                                                                                               institutional infrastructure rather than external LLM services. A
                                         Knowledge Graph, Natural Language Interface, Metadata Search,
                                                                                                               practical objective is therefore to find the smallest model that
                                         SPARQL, SQL, OWL, RDF, Large Language Model, Ontology Design,
                                                                                                               achieves acceptable accuracy, keeping hardware costs manageable
                                         Neuroimaging, DICOM, BIDS, MRI
                                                                                                               for institutions that may have modest GPU resources. We eval-
                                                                                                               uate across 8 locally deployed LLM variants (8B to 35B parameters,
                                         1   Introduction
                                                                                                               including quantized and mixture-of-experts variants), showing that
                                         Research facilities, enterprises, and government agencies accumu-     the best model achieves 100% accuracy on SPARQL and 57% on auto-
                                         late large archives of domain-specific data with rich metadata,       generated SQL, with no fine-tuning, no retrieval augmentation, and
                                         for example subject demographics, acquisition parameters, exper-      no multi-agent orchestration [28, 33–35]. Stripping ontology anno-
                                         imental configurations, and provenance records. Querying this         tations degrades SPARQL accuracy by 19 percentage points and
                                         metadata ad-hoc can require writing structured queries in SQL
                                         or SPARQL, which in turn requires both knowledge of the query
                                                                                                                 Blake G. Fitch and Cato Elia Kurtz


SQL by 14, revealing the importance of semantic annotations for           DBpedia, where opaque identifiers provide few semantic hints to
LLM-driven query generation.                                              the LLM. Our approach differs in assuming the ontology is under
  Contributions:                                                          our control. Domain-specific ontologies are typically smaller in
    (1) The NLKGQ framework and ontology-first development                vocabulary than public KGs, but may describe large volumes of
        process for enabling NL access to domain-specific meta-           data with a compact set of classes and properties.
        data, including ontology design principles, a KG builder
        pattern, and a reusable query server with web interface,
                                                                          2.2   Text-to-SQL and Schema Representation
        demonstrated on neuroimaging research data
    (2) A systematic evaluation of LLM-driven SPARQL genera-              Text-to-SQL has seen rapid progress on benchmarks like Spider [31],
        tion across 8 models, 8 ontology representations, and 768         but performance depends on schema simplicity. BEAVER [3] shows
        configurations (over 16,000 runs), showing that ontology          that GPT-4o achieves 0% execution accuracy on real enterprise
        design is a dominant factor in accuracy                           schemas with hundreds of tables, with failures traced to schema
    (3) A generic OWL KG-to-SQL schema generator and data                 retrieval and column mapping. Sequeda et al. [21] show that knowl-
        transformer enabling a systematic comparison of text-to-          edge graphs provide a structural advantage, raising accuracy from
        SPARQL vs text-to-SQL for the same NL questions                   16% (SQL) to 54% (SPARQL) on the same enterprise questions.
    (4) Analysis of the structural advantages OWL provides over           Rajkumar et al. [17] show that schema representation, how table
        SQL Data Definition Language (DDL) for LLM-based query            and column names are presented, directly affects LLM accuracy
        generation                                                        for SQL generation, paralleling our findings for SPARQL. Wretblad
                                                                          et al. [30] show that adding column descriptions to SQL schemas
2 Related Work                                                            improves text-to-SQL accuracy by over 20% on columns with unin-
                                                                          formative names, validating the importance of annotations.
2.1 Knowledge Graph Question Answering
Traditional Knowledge Graph Question Answering (KGQA)
systems combine entity linking with relation prediction, mapping          2.3   Text-to-SPARQL
NL to structured queries through classification [8, 23]. Recent work      LLM-based approaches to SPARQL generation began with sequence-
applies LLMs to this problem through several strategies.                  to-sequence models [22]. Chain-of-thought prompting [32] and
    Fine-tuning approaches train models on SPARQL examples.               complex benchmarks like Spider4SPARQL [9] have advanced the
SGPT [20] applied a pre-trained generative model, combined with           field, but most work targets public KGs with opaque identifiers.
knowledge graph embeddings, to SPARQL generation. Zhang et                   Giuliani et al. [6] propose heuristics for designing LLM-friendly
al. [33] use GAIL (Generative Adversarial Imitation Learning) to          ontologies, such as preferring semantically expressive labels over
fine-tune LLMs for low-resource KGQA, where the LLM acts as a             cryptic identifiers, drawn from experience refining evaluation
generator producing SPARQL that a discriminator evaluates against         ontologies for two zero-shot SPARQL benchmarks. Their appendix
expert demonstrations.                                                    states our controlled-semantics thesis as design advice, without an
    Multi-agent and pipeline approaches add orchestration layers.         ablation isolating naming from other confounded changes: their
AGENTiGraph [35] deploys intent classification, task planning,            one supporting data point, GPT-3.5 improving from 0.08 to 0.60,
and automatic knowledge integration across multiple agents,               combines renaming, added axioms, and query filtering in a single
achieving 95% classification accuracy on a 3,500-query benchmark.         step. Our ablation (Table 4) provides the controlled measurement
CyberBOT [34] combines RAG with an ontology-based verification            behind such guidance: holding model, prompt, and benchmark
layer that constrains LLM outputs post-hoc.                               fixed, ontology representation alone accounts for a 90-point spread
    In-context learning approaches provide examples at inference          in SPARQL accuracy, from 100% (default) to 10% (abstract-graph).
time. D’Abramo et al. [4] show that ICL with retrieved SPARQL                SparqLLM [1] retrieves from 360 hand-authored query templates
examples can match fine-tuned models on KGQA benchmarks,                  to construct SPARQL via retrieval-augmented generation; removing
though their approach requires example retrieval infrastructure.          the template retrieval drops their reported relaxed-match accuracy
GRASP [28] uses the LLM to explore the knowledge graph at query           from 66.7% to 55.3%, indicating that curated templates, not the
time, searching for relevant IRIs and literals, achieving state-of-the-   LLM’s zero-shot capability, account for most of their accuracy. Our
art results on Wikidata in a zero-shot setting.                           approach requires no per-question template curation: the ontology
    Rhizomer-LLM [16] lowers the barrier to SPARQL for non-               alone, supplied once in the system prompt, provides the semantic
expert users with an LLM-assisted exploratory interface over              scaffolding an LLM needs to generate correct queries for a fixed
cloud APIs (Gemini, DeepSeek, Llama), evaluated on the BESDUI             domain.
task-completion benchmark. Because BESDUI measures whether                   Vejvar and Fujimoto [24] compare SPARQL, SQL, and Cypher
a task was completed rather than whether the returned answer is           generation on a shared benchmark and find SPARQL trails SQL
correct, since, in the authors’ words, semantic correctness cannot        under terse, token-dense schema linearizations (17.2% vs 29.7%
be automatically verified, it is complementary to our evaluation,         execution accuracy with fine-tuned uT5 models, including for a
which reports execution-level result correctness against a reference      pretrained model tested in their appendix); they identify richer
query for every competency question.                                      schema representations as future work. We test that condition
    All of these approaches build complexity to cope with ontologies      directly: with the full annotated OWL ontology in context, SPARQL
they cannot change, typically public KGs like Wikidata [25] or            accuracy exceeds auto-generated SQL (100% vs 57%), suggesting
Natural Language Access to Domain-Specific Metadata:
A Reusable Framework for LLM Query Generation


that schema and ontology richness, not the query language itself,           (5) Natural language annotations: rdfs:comment, rdfs:label,
determines which backend an LLM can query more reliably.                        and skos:altLabel provide context, readable names, and
   Closest to our work, Rasheed and Aguado [18] investigate                     synonyms beyond the property URI
prompt augmentation formats for domain-specific KGs, testing                (6) No opaque codes: Meaningful URIs throughout; no arbi-
reduced and condensed ontology representations. However, they                   trary or auto-generated identifiers
take the existing KG ontology as given and focus on fitting it           These are not cosmetic choices. They are engineering deci-
into the prompt, rather than designing the ontology for LLM           sions made during ontology development. When building a new
consumption from the start. Our work focuses on domain-specific       domain knowledge graph, readability costs little: the ontology
ontologies of finite size that fit in the LLM context window. Our     must be designed regardless, and readable names are no harder to
measurements show that departing from expressive naming of            define than opaque ones. These principles also align with the FAIR
ontological elements hurts accuracy.                                  (Findable, Accessible, Interoperable, Reusable) data guidelines [29],
                                                                      particularly Reusable: the ontology provides rich, domain-relevant
2.4     Our Focus                                                     metadata described with formal semantics, making both the data
Prior work treats the ontology or database schema as a given and      and the NL access layer reusable across tools and communities.
focuses on improving query generation. To our knowledge, no prior        Consider a concrete example from our demonstration domain
work addresses the end-to-end process: how to capture domain          ontology (MRI Research Ontology, MRO):
vocabulary in a formal ontology, build a knowledge graph from
domain metadata via ETL, and enable LLM-driven NL querying, all       mro:hasHandedness a owl:DatatypeProperty ;
as a reusable technique for domain practitioners.                         rdfs:label "Handedness"@en ;
   Furthermore, while Sequeda et al. [21] compare LLM accuracy            rdfs:comment "Subject handedness: Right, Left,
on SQL vs SPARQL across different schemas and datasets, no prior              Ambidextrous, or Unknown. (MRO)"@en ;
work compares SPARQL and SQL as query backends when both                  rdfs:domain mro:Subject ;
are derived from the same authoritative ontology, with the same           rdfs:range xsd:string .
readable naming, the same data, and the same LLM models. We
                                                                         The property name, label, comment, domain, and range together
provide this controlled comparison by automatically generating a
                                                                      allow the LLM to use this property correctly without any prior
relational schema from the domain ontology and evaluating both
                                                                      exposure to our ontology. The comment tells the LLM what values
backends on the same competency questions.
                                                                      to expect, enabling it to generate correct FILTER clauses. Contrast
                                                                      this with Wikidata’s wdt:P552 (handedness): the identifier P552
3     Production Framework with Demonstration                         carries no semantic information, so the mapping must be learned
      Domain                                                          through fine-tuning, few-shot examples, or graph exploration.
Our contribution has two main areas: a development process               Frontier LLMs can assist domain experts in formalizing their
and a reusable framework. The development process is what a           vocabulary into OWL, lowering the barrier to ontology creation
domain practitioner follows to enable NL access for a new domain:     for practitioners without semantic web expertise.
(1) capture domain vocabulary in an OWL ontology, (2) build a            Figure 1 shows the class and property structure of our demon-
knowledge graph via ETL from domain data sources, and (3) iterate     stration domain ontology (MRO).
the ontology, competency questions, and prompt rider together
until accuracy is acceptable. The reusable framework is the domain-   3.2     ETL and Knowledge Graph Construction
agnostic infrastructure that supports this process: the NLKGQ queryWith the domain ontology defined, a domain-specific ETL pipeline
server, web application, and combinatorial test driver. The frame- collects metadata and populates a KG. In our demonstration domain,
work also supports production deployment. Both are described       metadata is extracted from DICOM headers, NIfTI sidecar files [7,
below, illustrated with our neuroimaging demonstration domain.     11], Siemens TWIX raw data headers, an experiment registry, and
                                                                   a participant management system [13]. Our Python pipeline uses
3.1 Capturing Domain Vocabulary                                    rdflib [19] to map extracted fields to MRO classes and properties,
The first step is formalizing what domain experts already know:    producing RDF triples. The resulting KG contains approximately
the entities, their properties, their relationships, and what they 10 million triples derived from a 180TB MRI archive.
mean. We capture this in an OWL ontology [15, 26] following six       Each new domain requires its own ETL logic, but the pattern is
design principles that cost nothing in formal expressiveness but   the same: identify metadata sources, write extraction code, map
measurably improve LLM accuracy:                                   fields to ontology terms, generate RDF. The ETL pipeline can
    (1) Full English words: hasAcquisitionTime rather than         also anonymize sensitive fields and compute aggregate properties
        acqT or AT                                                 (e.g., experiment duration from individual acquisition timestamps)
    (2) Consistent naming pattern: Properties follow has<Property> during the transformation step. Rather than relying on an OWL
        (e.g., hasSubjectId, hasRepetitionTime)                    reasoner at query time, the ETL pipeline materializes all implied
    (3) Descriptive relationships: isSubjectOfExperiment           relationships as concrete RDF triples (e.g., generating both direc-
        clearly indicates direction                                tions of inverse properties and explicit class memberships) during
    (4) Explicit domain and range: Property definitions specify    KG construction; this is sufficient for the OWL constructs we use.
        which classes they connect                                 The ontology guides what to extract and how to name it.
                                                                                                                Blake G. Fitch and Cato Elia Kurtz


                                                                        and the rider captures the conventions that naming alone cannot
                                                                        express.

                                                                        3.4    NLKGQ Query Server and Web Application
                                                                        The NLKGQ server receives an NL question and constructs a system
                                                                        prompt containing: (1) generic SPARQL generation instructions
                                                                        (output format, error handling, query patterns to prefer or avoid),
                                                                        (2) the complete domain ontology in OWL Turtle format, and
                                                                        (3) a small domain-specific rider with conventions particular to
                                                                        the knowledge graph (e.g., preferred identifier patterns, directives
                                                                        addressing recurring LLM mistakes). The user’s NL question is
                                                                        appended as the user message, and the LLM generates SPARQL.
                                                                           Logic in the harness handles practical issues of the LLM response:
                                                                        stripping chain-of-thought <think> blocks, extracting SPARQL
                                                                        from markdown, fixing PREFIX declarations using the ontology as
                                                                        ground truth, and optionally retrying failed queries by sending the
                                                                        error back to the LLM. Retrying failed queries is technically not
                                                                        zero-shot; however, it primarily helps smaller models recover from
                                                                        syntax errors, while the best-performing models rarely trigger it.
                                                                           The web application provides an interface where end users
                                                                        type NL questions and receive query results, with the generated
                                                                        SPARQL shown for transparency. Features include prefix compres-
                                                                        sion that strips verbose RDF URIs from query results, displaying
                                                                        data with readable prefixed names instead (with a toggle for full
                                                                        URIs when needed), CSV download of results, an LLM-powered
                                                                        “Explain” button that describes what the generated SPARQL does in
                                                                        plain language, Python script export for rerunning queries outside
Figure 1: MRI Research Ontology (MRO) class diagram.                    the web interface, an interactive ontology graph visualization, and
Classes are connected by object properties (arrows).                    a “Save Test Case” function that packages a query with its results
                                                                        for use in the evaluation framework. Displaying the generated
                                                                        query builds user trust and helps researchers learn which phrasings
   The resulting KG is loaded into a SPARQL server, in our case         produce useful results. The system is deployed at a neuroimaging
Apache Jena Fuseki [2], where it can be queried using SPARQL            research facility where neuroscience researchers with varying levels
1.1 [27] via the web interface or HTTP API. This keeps the SPARQL       of query expertise can search their metadata directly. Figure 2 shows
server lightweight and query latency predictable.                       the web interface processing a natural language query.

3.3    Iterative Development                                            4     Research Methods and Experimental Setup
Ontology development is not a one-time design step. The ontology,       To rigorously evaluate our design decisions, we developed addi-
competency questions, and domain-specific prompt rider co-evolve        tional research infrastructure beyond the production system. Some
through testing. Running test cases against the system reveals gaps     of this infrastructure also supports the iterative development
that feed back into all three:                                          process (Section 3.3), serving both production and research needs.
      • A property name that confuses the LLM gets renamed in
        the ontology (e.g., adding skos:altLabel “pseudonym” to         4.1    Test Driver Framework
        hasSubjectId when users say “pseudonym” instead of              The test driver is the foundation of both domain development and
        “subject ID”)                                                   research evaluation. Given a competency question (NL), a refer-
      • A recurring LLM mistake gets addressed by a new directive       ence SPARQL query, and expected results, the driver calls the LLM,
        in the domain-specific prompt rider (e.g., “return experi-      extracts the generated query, executes it against the appropriate
        ment IDs, not instance URIs”)                                   backend, and compares results. The driver supports combinato-
      • A new user question that the system handles poorly              rial sweeps across the following parameters for each competency
        becomes a new competency test case                              question:
   This cycle is lightweight: each iteration is a small change to             • LLM model: different model families, sizes, and quantiza-
one of the three artifacts, followed by re-running the test suite. It           tion variants
requires domain knowledge and comfort with iterative testing, but             • Temperature: controls generation randomness (e.g., 0.0,
no machine learning, database, or SPARQL expertise. The result                  0.2)
is a progressively refined system where the ontology captures                 • System prompt: different prompt formulations and
the domain vocabulary, the test cases capture the query patterns,               domain-specific riders
Natural Language Access to Domain-Specific Metadata:
A Reusable Framework for LLM Query Generation


                                                                            • compact-typed: Compact with datatype annotations
                                                                               retained
                                                                            • compact-grouped: Properties grouped by domain class
                                                                            • raw-graph: RDF triples in N-Triples format
                                                                            • abstract-dict: Dictionary mapping generic keys to values
                                                                            • abstract-graph: Graph with anonymized node/edge labels
                                                                          These form an ablation study: moving from default to abstract-
                                                                       graph progressively strips semantic information, revealing which
                                                                       features the LLM relies on.

                                                                       4.3   Automatic Generation of SQL Database
                                                                       We developed a generic OWL-to-SQL converter that reads the
                                                                       domain ontology and automatically derives a PostgreSQL 17
                                                                       schema: each OWL class becomes a table, each datatype property
                                                                       becomes a column (typed from rdfs:range), and object proper-
                                                                       ties become foreign keys (direction inferred from owl:inverseOf).
                                                                       Ontology annotations (rdfs:comment, rdfs:label, skos:altLabel)
                                                                       are converted to SQL column comments. The same KG data is loaded
                                                                       into the relational schema (6 tables, 182 columns for the largest
                                                                       table).
Figure 2: The NLKGQ web interface. The user types a natural               A system prompt analogous to the SPARQL prompt provides
language question (top), the system generates and displays             the Data Definition Language (DDL) schema (with or without
the SPARQL query (left), and shows the result table with               comments) and instructs the LLM to generate SQL instead of
prefix-compressed URIs (right).                                        SPARQL. A SQL test driver evaluates the same competency ques-
                                                                       tions against PostgreSQL using tolerant comparison to match SQL
                                                                       results against SPARQL reference data.
      • Ontology representation: full Turtle, no-comments,
                                                                       4.4   Models and Hardware
        compact, abstract, etc.
      • Query backend: SPARQL or auto-generated SQL (with or           We evaluate eight model variants from the Qwen3 family, span-
        without column comments)                                       ning 8B to 35B parameters, including dense and mixture-of-experts
      • Repetitions: multiple runs per configuration to assess vari-   (MoE) architectures, and quantized variants for production deploy-
        ability                                                        ment:
      • Fix-retry policy: number of LLM correction attempts on
                                                                       Table 1: Models evaluated. All served locally. HW: A=AMD
        syntax errors
                                                                       MI300A APU (HPC), N=4×NVIDIA RTX5000 (institutional).
   Results are logged to CSV with per-query timing, match status,
and fix-retry outcomes.
                                                                        Model                   Params   Type        Ctx   Server      HW
   A walker script orchestrates the driver across all test cases
and configurations, with parallel execution across models. For          Qwen3-8B                    8B   Dense       41K   vLLM        A
the SQL evaluation, a separate test driver executes against Post-       Qwen3-14B                  14B   Dense       41K   vLLM        A
                                                                        Qwen3-Coder-30B-A3B     30B/3B   MoE         64K   vLLM        A
greSQL with tolerant comparison (column name normalization,
                                                                        Qwen3.6-27B                27B   Dense       64K   vLLM        A
order-independent row matching, and URI prefix stripping) to
                                                                        Qwen3.6-27B-FP8            27B   Dense/FP8   64K   vLLM        A
handle differences between SQL output and SPARQL reference              Qwen3.6-27B-Q8_0           27B   Dense/Q8    32K   llama.cpp   N
data.                                                                   Qwen3.6-35B-A3B         35B/3B   MoE         64K   vLLM        A
   The test driver is used both for iterative domain development        Qwen3.6-35B-A3B-FP8     35B/3B   MoE/FP8     64K   vLLM        A
(Section 3.3) and for the research evaluations described below.

4.2     Virtual Ontology Representations                                  Models are served on two GPU systems: AMD Instinct MI300A
                                                                       APUs (128GB HBM3 per APU) at a shared HPC facility [14] via
To measure which ontology features different LLMs rely on, we          vLLM [10], and an institutional 4× Quadro RTX 5000 system (64GB
evaluate eight representations of the same ontology, generated         total VRAM) via llama.cpp for the Q8 variant. The Quadro RTX
automatically from the full OWL Turtle:                                5000 based system (AMD CPU, 256GB main memory, 4×16GB GPU
      • default: Full OWL Turtle with domain, range, comments,         VRAM) is vintage 2020 hardware and serves as our production
        labels                                                         deployment target. Context windows range from 32K to 64K tokens
      • no-comments: Turtle with rdfs:comment and rdfs:label           (Table 1). The full OWL Turtle ontology (80KB, approximately 18K
        stripped                                                       tokens) and the SQL schema with comments are each provided in
      • compact: One-line-per-property listing class memberships       the system prompt, requiring models that can handle substantial
                                                                                                                  Blake G. Fitch and Cato Elia Kurtz




      Domain       Domain Specific Code and Artifacts              Domain Agnostic Framework                    End-users
      Experts
                                             Prompt                                        NLKGQ
                        Domain                                      SPARQL
                                              Rider                                        WebApp
                        Specific                                      LLM
                                                                                            Server
      Vocabulary         OWL                                        Prompt
         and            Ontology                                                            LLM API              NLKGQ
      Semantics                                                                                                  Web GUI

                                                                                           SPARQL
    Archive                                                         SPARQL                   Test                 NL
                           ETL                KG RDF                                        Driver            Competence
   Metadata                                                        KG Server
                         Pipeline              Turtle                                                         & Regression
   Sources                                                          (Fuseki)               LLM API
                                                                                                               Questions
  KEY :     Informs
            Data feed
                                            KG->SQL                   SQL                 SQL Test
            Interface
                                            DB : Data               RDBMS                  Driver
  Human Interaction                         Schema                 (Postgres)               LLM API
  Domain Specific
                                           Exploratory SPARQL/KG to SQL RDBMS Infrastructure
  Reusable Framework
  SQL Comparison Inf.


        Figure 3: Framework architecture showing production components (solid) and research infrastructure (dashed).


context alongside the generation task. Even the smallest context            SQL evaluation. The same test cases are evaluated across 8
window (32K for the Q8 model) provides ample headroom, and               models × 2 schema variants (with and without column comments)
no context overflow errors were observed in any run. The same            × 4 temperatures.
models are used for both SPARQL and SQL evaluation.                         For both backends, when a generated query produces a syntax
                                                                         error, the harness sends the query and error message back to the
                                                                         LLM for up to two correction attempts. As discussed in Section 3.4,
                                                                         this is technically not zero-shot, but it is rarely used with the LLMs
4.5     Evaluation Protocol                                              chosen for production deployment. LLM generation time is recorded
                                                                         for each run.
Twenty-one competency and regression questions were developed
with domain experts, covering filtered queries (“Subjects over age       4.6    Example Queries and Generated SPARQL
42 in study 42”), multi-entity joins (“Experiments with subject from
study EPEQ-7ITX”), and aggregations with sorting (“All datasets          To illustrate what the system produces, we show three competency
for a study, sorted by acquisition time”). Each test case comprises      questions of increasing complexity with the SPARQL generated by
an NL question, a reference SPARQL query, and expected results           Qwen3.6-27B (default ontology, zero-shot).
in SPARQL Results JSON format. The web application’s “Save Test             Simple lookup. NL: “Show all the experiments by ID in study
Case” function generates these artifacts directly from a successful      101.”
query, enabling domain experts to create new test cases without          SELECT DISTINCT ?ExperimentId WHERE {
manual JSON editing. The primary metric is result match: a gener-          ?study mro:hasStudyId "101" .
ated query is counted as correct when its result set equals the            ?experiment mro:isExperimentOfStudy ?study .
reference result set after canonicalization (row order ignored, vari-      ?experiment mro:hasExperimentId ?ExperimentId .
able names normalized). Accuracy is the fraction of the 21 questions     }
matched; reported times are mean LLM generation time over the
                                                                           Multi-entity join. NL: “List all experiment IDs for study 101.
questions whose generated query executed.
                                                                         Show the subject ID, handedness, age, and acquisition date for each.”
   SPARQL evaluation. Each test case is evaluated across all
combinations of model, ontology representation, system prompt            SELECT DISTINCT ?ExperimentId ?SubjectId
variant, and temperature setting: 8 models × 8 ontology represen-              ?Handedness ?PatientAge ?AcquisitionDate
tations × 3 prompts × 4 temperatures, yielding over 16,000 runs.         WHERE {
Natural Language Access to Domain-Specific Metadata:
A Reusable Framework for LLM Query Generation


    ?exp mro:isExperimentOfStudy ?study .                              Table 2: Competency questions by category. L=lookup, J=join,
    ?study mro:hasStudyId "101" .                                      F=filter, A=aggregation, S=sort, O=ontology.
    ?exp mro:hasExperimentId ?ExperimentId .
    ?exp mro:aExperimentHasSubject ?subj .                                   #     Description                                              Type
    ?subj mro:hasSubjectId ?SubjectId .
                                                                             1     List experiments in a study                              L
    ?subj mro:hasHandedness ?Handedness .                                    2     Find experiments for a subject by pseudonym              L
    ?exp mro:hasPatientAge ?PatientAge .                                     3     Find all experiments for the subject in a given exper-   J
    ?exp mro:hasExperimentBeginDate ?AcquisitionDate .                             iment
}                                                                            4     Same as 3, rephrased as two-part question                J
                                                                             5     Experiments matching two protocol name patterns          J,F
   Filtered aggregation. NL: “For study 42, find experiments
                                                                             6     Experiment details with subject demographics and         J
where the subject is older than 42. List only experiments before                   date
June 2025.”                                                                  7     Dataset names with acquisition date and time             L,S
SELECT DISTINCT ?ExperimentId ?PatientAge WHERE {                            8     All properties and values on a specific dataset          O
  ?exp mro:isExperimentOfStudy ?study .                                            instance
  ?study mro:hasStudyId "42" .                                               9     Acquisition dates for all experiments in a study,        L,S
                                                                                   sorted
  ?exp mro:hasExperimentId ?ExperimentId .
                                                                             10    Experiments filtered by subject age and date range       F
  ?exp mro:hasPatientAge ?PatientAge .
                                                                             11    Subject demographics (language, degree, handed-          J
  ?exp mro:hasExperimentBeginDate ?date .                                          ness, etc.)
  FILTER(xsd:integer(?PatientAge) > 42)                                      12    Sequence datasets matching coil name substring           F
  FILTER(?date < "2025-06-01"^^xsd:date)                                     13    Same as 12, exact coil name match                        F
}                                                                            14    Experiments after a time of day, sorted by duration      F,S
                                                                             15    Experiments in a date and duration range with            F,J,S
  All three queries are generated zero-shot from the NL question
                                                                                   study info
and the ontology alone. The LLM correctly uses ontology property             16    Experiments using a specific coil with study and         J,F
names, traverses relationships via inverse properties, and applies                 date
appropriate type casting in filters. PREFIX declarations are omitted         17    Studies with scanner types and total experiment          A,J,S
above for brevity.                                                                 hours
  Table 2 lists all competency questions used in the evaluation.             18    Ontology introspection: classes, properties, and         O
                                                                                   types
5 Results                                                                    19    Coils used in a date range with experiment counts        A,F
                                                                             20    Top N coils by usage count in a year                     A,F,S
5.1 SPARQL: Model Comparison                                                 21    Datasets on a specific experiment, sorted by time        L,S
Table 3 shows the best SPARQL configuration for each model,
reporting the full configuration (ontology representation, temper-
ature, system prompt) that achieved the highest accuracy. Short        factor in accuracy. The Tokens column shows the prompt size for
model identifiers (ID column) are used in subsequent tables.           each representation, ranging from 1.7K (compact) to 17.6K (default).
   Both 27B dense variants (full-precision and Q8 quantized)              Property names are essential: the jump from compact (62%) to
achieve 100% accuracy on the full Turtle ontology. The Q8 model        abstract-dict (19%) shows the LLM uses name semantics, not just
on older institutional hardware (N) is 1.8× slower but equally         graph structure. Annotations matter: stripping comments costs 19
accurate as the full-precision model on HPC hardware (A). The          percentage points for SPARQL, and as we show below, comments
35B MoE models peak at 57%, well below the 27B dense models            are even more critical for SQL. Domain and range declarations
despite having more parameters, suggesting that MoE architectures      help: compact-typed (71%) outperforms compact (62%), suggesting
may be less effective for structured generation tasks requiring        type information reduces cross-class property confusion.
precise schema adherence. Model scale matters within architec-            At our ontology’s scale (80KB), the full Turtle fits comfortably
tures: accuracy improves from 24% (8B) through 38% (14B) to 100%       within 32K-token context windows, so there is no practical reason to
(27B dense).                                                           sacrifice accuracy for compactness. Looking forward, many smaller
                                                                       models now support substantially larger context windows (64K
5.2     SPARQL: Ontology Representation Impact                         to 256K tokens), suggesting these methods will scale to domains
Table 4 shows the best configuration for each ontology represen-       requiring more complex ontologies.
tation, reporting the full configuration that achieved the highest
accuracy.                                                              5.3        SPARQL: System Prompt and Temperature
   Only default (the complete OWL Turtle ontology with all anno-       Tables 5 and 6 show the best configurations for each system prompt
tations, no ablation) reaches 100%. Stripping rdfs:comment and         variant and temperature setting.
rdfs:label annotations drops accuracy to 81%. Compact repre-              Temperature and system prompt have modest effects compared
sentations that retain property names achieve 62–71%. Abstract         to model choice and ontology representation. All three prompts
representations that replace readable entity names with generic        reach 100% with the 27B dense model at 𝑡=0.0, and all four temper-
identifiers collapse to 5–19%, confirming naming as a dominant         atures reach at least 90% when paired with the right model and
                                                                                                                                     Blake G. Fitch and Cato Elia Kurtz


Table 3: Best SPARQL configuration per model (21 competency questions). The ID column provides short identifiers used in
subsequent tables: Q30/Q36=Qwen generation, xxB=parameters, D=dense, M=MoE, F=FP8, Q=Q8, C=Coder. HW from Table 1.

                 Model ID        Model Name                   Acc%     Ontology            Temp        Prompt        Avg Time    Tokens       HW
                 Q36.27B.D       Qwen3.6-27B                   100     default                0.0      baseline           8.1s    17.6K       A
                 Q36.27B.Q       Qwen3.6-27B-Q8_0              100     default                0.0      procedural        14.6s    17.7K       N
                 Q36.27B.F       Qwen3.6-27B-FP8                95     default                0.0      guardrails         7.9s    17.8K       A
                 Q30.30B.C       Qwen3-Coder-30B-A3B            57     compact-grouped        0.2      procedural         1.0s     1.9K       A
                 Q36.35B.F       Qwen3.6-35B-A3B-FP8            57     default                0.6      guardrails        25.8s    17.8K       A
                 Q36.35B.M       Qwen3.6-35B-A3B                57     default                0.2      procedural        24.2s    17.7K       A
                 Q30.14B.D       Qwen3-14B                      38     default                0.0      procedural         1.8s    16.8K       A
                 Q30.08B.D       Qwen3-8B                       24     default                0.6      procedural         0.9s    16.8K       A


              Table 4: Best SPARQL configuration per ontology representation (21 questions). Model IDs from Table 3.

                                   Ontology             Acc%         Temp   Prompt         Avg Time      Tokens     Model ID
                                   default                100         0.0   baseline            8.1s       17.6K    Q36.27B.D
                                   no-comments             81         0.0   procedural         14.7s        7.6K    Q36.27B.Q
                                   compact-typed           71         0.0   procedural          3.0s        1.9K    Q36.27B.D
                                   compact-grouped         67         0.2   procedural          2.9s        1.9K    Q36.27B.D
                                   compact                 62         0.0   procedural          3.1s        1.7K    Q36.27B.D
                                   raw-graph               48         0.4   guardrails          3.5s        4.1K    Q36.27B.D
                                   abstract-dict           19         0.6   baseline           20.8s        5.7K    Q36.35B.M
                                   abstract-graph           5         0.0   guardrails         31.8s        3.8K    Q36.35B.F


the default ontology. The baseline prompt (the simplest of the                       5.4     Auto-SQL Results
three) achieves 100%, suggesting that with a well-designed ontology,                 Table 7 shows auto-SQL accuracy with and without ontology-
elaborate prompting is unnecessary.                                                  derived column comments.
                                                                                     Table 7: Best auto-SQL accuracy per model (21 questions,
                                                                                     wide-table schema). Model IDs from Table 3.
Table 5: Best SPARQL configurations per system prompt (21
questions). All use default ontology.                                                               Model ID        With comments       No comments
                                                                                                    Q36.27B.Q          12/21 (57%)          9/21 (43%)
        Prompt         Acc%      Model ID     Temp     Avg Time                                     Q36.27B.D          11/21 (52%)          7/21 (33%)
                                                                                                    Q36.27B.F          11/21 (52%)          8/21 (38%)
        baseline           100   Q36.27B.D       0.0   8.1s                                         Q36.35B.M          11/21 (52%)          6/21 (29%)
        guardrails         100   Q36.27B.D       0.0   8.3s                                         Q36.35B.F          11/21 (52%)          7/21 (33%)
                                                                                                    Q30.14B.D           9/21 (43%)          7/21 (33%)
        procedural         100   Q36.27B.D       0.0   8.5s                                         Q30.08B.D           8/21 (38%)          6/21 (29%)
        procedural         100   Q36.27B.Q       0.0   14.6s                                        Q30.30B.C           8/21 (38%)          7/21 (33%)


                                                                                        The best model achieves 57% on auto-SQL compared to 100% on
Table 6: Best SPARQL configurations per temperature (21                              SPARQL. Ontology-derived column comments add 3 cases for the
questions). All use default ontology.                                                best model (43% without, 57% with), a considerably larger effect
                                                                                     than stripping annotations from the SPARQL ontology (100% to
                                                                                     81%). The Q8 model (Q36.27B.Q) on institutional hardware achieves
        Temp       Acc%     Model ID    Prompt         Avg Time                      the highest SQL accuracy, suggesting that the chain-of-thought
        0.0          100    Q36.27B.D   baseline               8.1s                  reasoning enabled in llama.cpp benefits the more complex SQL
        0.0          100    Q36.27B.D   guardrails             8.3s                  generation task.
        0.0          100    Q36.27B.D   procedural             8.5s
        0.0          100    Q36.27B.Q   procedural            14.6s                  5.5     Practical Deployment on Modest Hardware
        0.2           95    Q36.27B.Q   baseline              14.2s                  For SPARQL with the default ontology, both 27B dense vari-
        0.4           90    Q36.27B.F   guardrails             7.8s                  ants (Q36.27B.D and Q36.27B.Q) achieve 100% accuracy at 𝑡=0.0,
                                                                                     Q36.27B.D with all three prompts, while the FP8 variant (Q36.27B.F)
        0.6           90    Q36.27B.F   procedural             8.0s
                                                                                     reaches 95%.
Natural Language Access to Domain-Specific Metadata:
A Reusable Framework for LLM Query Generation


Table 8: Per-query comparison using each backend’s best                            The complex pipelines in prior work [28, 33–35] exist for a
configuration. SPARQL: Q36.27B.D, default ontology, 𝑡=0.0,                      reason: they cope with ontologies not designed for LLM consump-
baseline. Auto-SQL: Q36.27B.Q, with comments, 𝑡=0.0. Q#                         tion. When the ontology can be designed, which is the case for
from Table 2. Time is LLM generation in seconds.                                every new domain metadata project, the simpler path is available.

                                                SPARQL              SQL
Q#      Query                                  OK      s    OK             s
 1      Experiments in a study                  ✓       4    ✓             4
 2
 3
        Experiments for a subject
        All experiments for a subject
                                                ✓
                                                ✓
                                                       5
                                                        5
                                                             ✓
                                                             ✓             5
                                                                            4
                                                                                6.2    SPARQL vs SQL: What the Ontology
 4
 5
        Same as Q3, rephrased
        Two protocol name patterns
                                                ✓
                                                ✓
                                                        6
                                                        9
                                                             ✓
                                                             ✓
                                                                           8
                                                                           8
                                                                                       Provides
 6      Experiment details with demographics    ✓      10    ✓             9    The gap between SPARQL and SQL accuracy (100% vs 57%) shows
 7      Dataset name, acq date and time         ✓       7    ×             6
 8      All properties on a dataset             ✓       5    ×            113   that while readable naming helps both, OWL provides structural
 9      Acquisition dates sorted                        7    ×             7
10      Age filter with date range
                                                ✓
                                                ✓       9    ✓             8
                                                                                advantages that SQL DDL lacks:
11      Subject demographics for a study        ✓      10    ×             8        Annotations. Stripping rdfs:comment from the SPARQL
12      Datasets matching coil substring        ✓       9    ✓            12
13      Datasets matching exact coil            ✓       8    ✓             9    ontology drops accuracy from 100% to 81%. Stripping the equivalent
14      Experiments after 4pm, sorted           ✓       9    ×             10   SQL column comments drops accuracy from 57% to 43%. Annota-
15      Experiments in duration range           ✓      12    ✓            13
16      Experiments for a coil with date        ✓       9    ×             8    tions are critical for both backends, consistent with Wretblad et
17      Studies with scanner hours              ✓      11    ×            12    al. [30].
18      Ontology classes and properties         ✓      15    ×             8
19      Coils used in a date range              ✓      10    ✓            12        Domain and range declarations. In our conversion, rdfs:range
20      Top N coils by experiment count                 9    ×            10
21      Datasets on experiment, sorted
                                                ✓
                                                ✓       6    ✓              7
                                                                                determines SQL column types and rdfs:domain determines table
        Total                                  21/21        12/21
                                                                                placement. These are preserved in the DDL, but the explicit class-
                                                                                level grouping visible in the Turtle ontology is flattened into a
                                                                                column list that the LLM must parse without the same semantic
                                                                                scaffolding.
                                                                                    Inverse properties. In SPARQL, owl:inverseOf allows the
   The Q8-quantized model (Q36.27B.Q) running on 4× Quadro                      LLM to traverse any relationship in either direction. A query can use
RTX 5000 GPUs (a machine several generations old) achieves 100%                 mro:aStudyHasExperiment or mro:isExperimentOfStudy inter-
SPARQL accuracy and the highest SQL accuracy (57%), demon-                      changeably. In SQL, there is one foreign key, and the LLM must
strating that the approach does not require recent-generation GPUs.             know which table owns it and JOIN from the correct side. The SQL
This matters for institutions with privacy constraints (e.g., GDPR              system prompt must explicitly encode join directions, while the
for human subject data) that must deploy LLMs locally. Published                SPARQL ontology encodes them structurally.
benchmark estimates [12] indicate that Apple Silicon workstations                   Entity-Attribute-Value schema. As an alternative to the wide-
with 128GB unified memory can run quantized 27B to 35B models                   table SQL schema (one column per property, NULLs where proper-
at roughly 25–50 tokens per second via MLX or llama.cpp. The low                ties are absent), we also evaluated an Entity-Attribute-Value (EAV)
idle power consumption of these systems makes them practical for                representation: a narrow three-column table (entity_id, attribute,
always-on deployment, and the large unified memory leaves head-                 value) per class, where each row stores a single fact. This schema
room for growing ontologies requiring larger context windows.                   was automatically derived from the same ontology. EAV accuracy
                                                                                reached only 11/21 (52%) with the best model and comments, drop-
6 Discussion                                                                    ping to 2/21 (10%) without comments. A key difficulty is that rela-
                                                                                tionship attributes in EAV store prefixed entity identifiers (e.g.,
6.1 The Ontology as Single Source of Truth                                      study_101) rather than clean values (101) that the LLM can reason
The central finding is that co-designing an LLM-friendly domain                 about directly. In SPARQL, the LLM never sees internal identifiers
ontology along with the ETL logic building the KG and the domain-               because it operates on variables and property patterns. In wide-
specific system prompt rider yields far better results than designing           table SQL, foreign keys reference clean primary keys. EAV exposes
any one of these components independently, or worse, accepting                  internal naming conventions to the query generator, requiring a
existing components as a given.                                                 domain-specific prompt rider to teach the convention. This repre-
   A related finding is that ontology-driven SPARQL queries are                 sents a structural disadvantage that readable naming alone cannot
easier for an LLM to generate accurately than an equivalent SQL                 overcome.
query on a relational model.                                                        Scope of the comparison. This result does not show that
   Experience with a neuroimaging demonstration domain shows                    SPARQL is generally easier for LLMs to generate than SQL. Vejvar
that end users can create well-formed natural language queries                  and Fujimoto [24] report the opposite ordering under terse schema
where they would not take the time to learn and write SPARQL or                 linearizations, and Sequeda et al. [21] report a KG advantage on an
SQL queries.                                                                    enterprise schema; the ordering depends on how much semantic
   Finally, we have found that we can run this service on local LLMs            structure each representation carries. Both relational schemas here
using older or less expensive hardware. It is likely that for domains           were derived mechanically from the ontology. A relational schema
without privacy constraints, cloud-based frontier LLMs with larger              designed by hand for these questions, with denormalized views,
context windows would be faster and more capable.                               natural keys, and documented join paths, would likely narrow the
                                                                                                                   Blake G. Fitch and Cato Elia Kurtz


gap, and we have not measured by how much. What the compar-                from the ontology, not designed by a database expert; the SPARQL
ison isolates is the effect of representation with data, naming, anno-     advantage we report is specific to that setting.
tations, questions, and models held constant: the OWL ontology
carries domain and range declarations, inverse properties, and class-      6.5    Future Work
level grouping as first-class structure, and a mechanical translation            • Cross-domain validation: Applying the development
to DDL loses part of that scaffolding.                                             process and framework to additional domains. Here we
                                                                                   are open to discussing collaboration.
                                                                                 • Expanded MRI archive use: The MRO ontology builds
6.3    Lessons Learned
                                                                                   on DICOM and BIDS standards shared across MRI research
Two findings were counterintuitive:                                                sites. With site-specific ETL adaptation, the same ontology
   Qwen3 MoE variants underperformed Qwen3 dense vari-                             and framework could serve other neuroimaging archives.
ants. The 35B MoE variants peaked at 57%, well below the 27B                     • Expanded test cases: Growing the competency question
dense models at 100%, despite having more total parameters. For                    set, including more complex query patterns.
structured generation tasks requiring precise schema adherence,                  • Multi-turn refinement: Supporting follow-up questions
dense models appear to be the better choice at a given compute                     where the LLM refines a previous query based on user
budget.                                                                            feedback, making the web application more conversational.
   The simplest prompt won. The baseline prompt, with the                        • LLM Model diversity: Evaluating non-Qwen model
fewest instructions, achieved the highest peak accuracy. More elab-                families and cloud-hosted models where domain privacy
orate prompts (guardrails, procedural) performed comparably but                    constraints permit.
not better, suggesting that with a well-designed ontology, the LLM
needs minimal additional guidance.
                                                                           7     Conclusion
   Additional findings: Full ontology in context consistently
produced the best results across all models and configurations.            We have presented a reusable framework and development process
Readable naming had the largest measurable effect on accuracy.             for natural language access to domain-specific metadata. A key
Q8 GGUF quantization preserved accuracy completely (100%,                  insight is that capturing domain vocabulary and semantics in a
matching full precision); FP8 quantization showed a small drop             well-designed OWL ontology enables LLM-driven query generation
(95%). Automatic OWL-to-SQL conversion derived a working                   against both SPARQL and SQL backends, with no fine-tuning, no
relational schema directly from the ontology with no manual                retrieval augmentation, and no multi-agent orchestration.
tuning.                                                                       The ontology serves as the single source of truth: it defines the
   The test driver is essential infrastructure. The combinatorial          domain vocabulary, informs the ETL pipeline, and provides the LLM
test driver (Section 4.1) is not only research tooling; it is the engine   with schema context for SPARQL queries. To explore SPARQL vs
that drives ontology evolution. The ontology, prompt rider, and            SQL for this work, we automatically generate a relational schema,
competency questions co-evolve: each iteration of any of these three       transform and load the KG into a PostgreSQL database, and eval-
artifacts is validated by re-running the full suite, making regressions    uate the competency questions via SQL, enabling a direct compar-
immediately visible. Without this tight feedback loop, the co-design       ison. On our MRI neuroimaging metadata benchmark, NL text-to-
process described in Section 3.3 would be more difficult. In our           SPARQL achieves 100% accuracy on our competency/regression
experience, ontology evolution slows over time but does not halt           question set while the analogous NL text-to-SQL achieves 57%.
as the vocabulary and semantics are better resolved.                       An ablation study across eight ontology representations confirms
                                                                           that ontology design, particularly readable naming and semantic
                                                                           annotations, is the dominant factor in accuracy.
6.4    Limitations                                                            The framework and development process are intended to be
Our evaluation covers a single metadata domain. While the ontology         reusable. The framework is designed to avoid domain-specific
design principles are domain-agnostic, generalization to other             components. The iterative development process outlined here
domains needs validation. The test set of 21 competency ques-              (ontology, competency questions, and prompt rider evolving
tions, while developed with domain experts, is small; expansion is         together) requires domain expertise but no machine learning, data-
ongoing. Because the competency questions co-evolved with the              base, or programming skills. We have demonstrated the process
ontology and prompt rider, accuracy on novel end-user queries may          and deployed the framework at a major neuroscience institute
differ from test set performance. The complexity of the ontology is        enabling end-user natural language search of MRI metadata on a
bounded by the available LLM context window, with some promise             growing image archive.
shown for token-dense encodings. The volume of metadata under                 We intend to open source this work including the MRI metadata
management is bounded by the capabilities of the SPARQL server.            domain and the framework, and we welcome collaboration on
We use Jena Fuseki in a Docker container, but for larger archives a        application to new domains.
heavy-duty commercial solution could be used without changing
the architecture. All models are from the Qwen3 family and results         GenAI Usage Disclosure
may differ with other model families. We have not compared                 Generative AI tools were used to assist with manuscript editing and
against cloud-hosted models (GPT-4, Claude) due to institutional           LATEX formatting. Generative AI was also used to assist with coding,
data privacy constraints. The SQL baselines are auto-generated             particularly the web server where we have little expertise available.
Natural Language Access to Domain-Specific Metadata:
A Reusable Framework for LLM Query Generation


The system described in this paper uses locally deployed LLMs                               [21] Juan F. Sequeda, Dean Allemang, and Bryon Jacob. 2023. A Benchmark to
(Qwen3 family) for SPARQL and SQL query generation, which is                                     Understand the Role of Knowledge Graphs on Large Language Model’s Accu-
                                                                                                 racy for Question Answering on Enterprise SQL Databases. arXiv preprint
the subject of this research. All scientific content, experimental                               arXiv:2311.07509 (2023).
design, analysis, and conclusions are the work of the authors.                              [22] Tommaso Soru, Edgard Marx, Diego Moussallem, Gustavo Publio, André Valdes-
                                                                                                 tilhas, Diego Esteves, and Ciro Baron Neto. 2017. SPARQL as a Foreign Language.
                                                                                                 In SEMANTiCS 2017 Posters & Demos.
                                                                                            [23] Ricardo Usbeck, Ria Hari Gusmita, Axel-Cyrille Ngonga Ngomo, and Muhammad
References                                                                                       Saleem. 2018. 9th Challenge on Question Answering over Linked Data (QALD-9).
 [1] Marco Arazzi, Davide Ligari, Serena Nicolazzo, and Antonino Nocera. 2025.                   In Joint Proceedings of SemDeep-4 and NLIWoD-4 and QALD-9, co-located with
     Augmented Knowledge Graph Querying leveraging LLMs. arXiv preprint                          ISWC 2018 (CEUR Workshop Proceedings, Vol. 2241). 58–64.
     arXiv:2502.01298.                                                                      [24] Martin Vejvar and Yasutaka Fujimoto. 2026. Are we too focused on single query
 [2] Jeremy J. Carroll, Ian Dickinson, Chris Dollin, Dave Reynolds, Andy Seaborne,               language? Investigating text-to-SQL/SPARQL/Cypher task complexity via fine-
     and Kevin Wilkinson. 2004. Jena: Implementing the Semantic Web Recommenda-                  tuning unbiased T5 models. Neurocomputing 697 (2026), 134202. doi:10.1016/j.
     tions. In Proceedings of the 13th International World Wide Web Conference (WWW).            neucom.2026.134202
     ACM, 74–83. doi:10.1145/1013367.1013381                                                [25] Denny Vrandečić and Markus Krötzsch. 2014. Wikidata: A Free Collaborative
 [3] Peter Baile Chen, Fabian Wenz, Yi Zhang, Devin Yang, Justin Choi, Nesime Tatbul,            Knowledgebase. Commun. ACM 57, 10 (2014), 78–85. doi:10.1145/2629489
     Michael Cafarella, Çağatay Demiralp, and Michael Stonebraker. 2025. BEAVER:            [26] W3C. 2012. OWL 2 Web Ontology Language Primer (Second Edition). https:
     An Enterprise Benchmark for Text-to-SQL. arXiv preprint arXiv:2409.02038v2                  //www.w3.org/TR/owl2-primer/.
     (2025).                                                                                [27] W3C. 2013. SPARQL 1.1 Query Language. https://www.w3.org/TR/sparql11-
 [4] Jacopo D’Abramo, Andrea Zugarini, and Paolo Torroni. 2025. Investigating Large              query/.
     Language Models for Text-to-SPARQL Generation. In Proceedings of the 4th Inter-        [28] Sebastian Walter and Hannah Bast. 2025. GRASP: Generic Reasoning And
     national Workshop on Knowledge-Augmented Methods for NLP (KnowledgeNLP).                    SPARQL Generation across Knowledge Graphs. In The Semantic Web – ISWC
     Association for Computational Linguistics, 66–80.                                           2025 (Lecture Notes in Computer Science, Vol. 16140). Springer. doi:10.1007/978-3-
 [5] Blake G. Fitch, Sebastian Müller, and Dario Bosch. 2022. MrData: An iRODS                   032-09527-5_15
     Based Human Research Data Management System. In Proceedings of the iRODS               [29] Mark D Wilkinson et al. 2016. The FAIR Guiding Principles for scientific data
     User Group Meeting. Leuven, Belgium.                                                        management and stewardship. Scientific Data 3 (2016), 160018.
 [6] Alessandro Giuliani, Marco Manolo Manca, Leonardo Piano, Alessandro Sebas-             [30] Niklas Wretblad, Oskar Holmström, Erik Larsson, Axel Wiksäter, Oscar Söder-
     tian Podda, Livio Pompianu, and Sandro Gabriele Tiddia. 2026. Are LLMs                      lund, Hjalmar Öhman, Ture Pontén, Martin Forsberg, Martin Sörme, and Fredrik
     adequate SPARQL query generators? Investigating zero-shot NL-to-SPARQL                      Heintz. 2024. Synthetic SQL Column Descriptions and Their Impact on Text-to-
     translation. Neural Computing and Applications 38, Article 33 (feb 2026), 38 pages.         SQL Performance. arXiv preprint arXiv:2408.04691 (2024).
     doi:10.1007/s00521-025-11799-x                                                         [31] Tao Yu, Rui Zhang, Kai Yang, Michihiro Yasunaga, Dongxu Wang, Zifan Li, James
 [7] Krzysztof J Gorgolewski et al. 2016. The brain imaging data structure, a format             Ma, Irene Li, Qingning Yao, Shanelle Roman, et al. 2018. Spider: A Large-Scale
     for organizing and describing outputs of neuroimaging experiments. Scientific               Human-Labeled Dataset for Complex and Cross-Domain Semantic Parsing and
     Data 3 (2016), 160044. doi:10.1038/sdata.2016.44                                            Text-to-SQL Task. In Proceedings of EMNLP.
 [8] Aidan Hogan, Eva Blomqvist, Michael Cochez, Claudia d’Amato, Gerard de Melo,           [32] Hamada M. Zahera, Manzoor Ali, Mohamed Ahmed Sherif, Diego Moussallem,
     Claudio Gutierrez, Sabrina Kirrane, Jose Emilio Labra Gayo, Roberto Navigli,                and Axel-Cyrille Ngonga Ngomo. 2024. Generating SPARQL from Natural
     Sebastian Neumaier, et al. 2021. Knowledge Graphs. Comput. Surveys 54, 4 (2021),            Language Using Chain-of-Thoughts Prompting. In Knowledge Graphs in the Age
     1–37. doi:10.1145/3447772                                                                   of Language Models and Neuro-Symbolic AI (SEMANTiCS 2024). Studies on the
 [9] Catherine Kosten, Philippe Cudré-Mauroux, and Kurt Stockinger. 2023.                        Semantic Web, Vol. 60. IOS Press, 353–368. doi:10.3233/SSW240028
     Spider4SPARQL: A Complex Benchmark for Evaluating Knowledge Graph Ques-                [33] Zhiqiang Zhang, Liqiang Wen, and Wen Zhao. 2024. A GAIL Fine-Tuned LLM
     tion Answering Systems. In 2023 IEEE International Conference on Big Data                   Enhanced Framework for Low-Resource Knowledge Graph Question Answering.
     (BigData). IEEE, 5272–5281.                                                                 In Proceedings of the 33rd ACM International Conference on Information and
[10] Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng,                          Knowledge Management (CIKM). ACM, 3300–3309. doi:10.1145/3627673.3679753
     Cody Hao Yu, Joseph E Gonzalez, Hao Zhang, and Ion Stoica. 2023. Efficient             [34] Chengshuai Zhao, Riccardo De Maria, Tharindu Kumarage, Kumar Satvik Chaud-
     Memory Management for Large Language Model Serving with PagedAttention.                     hary, Garima Agrawal, Yiwen Li, Jongchan Park, Yuli Deng, Ying-Chih Chen,
     In Proceedings of SOSP. doi:10.1145/3600006.3613165                                         and Huan Liu. 2025. CyberBOT: Ontology-Grounded Retrieval Augmented
[11] Xiangrui Li, Paul S Morgan, John Ashburner, Jolinda Smith, and Christopher                  Generation for Reliable Cybersecurity Education. In Proceedings of the 34th ACM
     Rorden. 2016. The first step for neuroimaging data analysis: DICOM to NIfTI                 International Conference on Information and Knowledge Management (CIKM).
     conversion. Journal of Neuroscience Methods 264 (2016), 47–56. doi:10.1016/j.               ACM. doi:10.1145/3746252.3761478
     jneumeth.2016.03.001                                                                   [35] Xinjie Zhao, Moritz Blum, Fan Gao, Yingjian Chen, Boming Yang, Luis Marquez-
[12] LLM Check. 2026. Apple Silicon LLM Benchmarks: Real tok/s by Model, Chip                    Carpintero, Mónica Pina-Navarro, Yanran Fu, So Morikawa, Yusuke Iwasawa,
     and Quantization. https://llmcheck.net/benchmarks.                                          Yutaka Matsuo, Chanjun Park, and Irene Li. 2025. AGENTiGraph: A Multi-Agent
[13] Karolina Mader and Maike Kleemeyer. 2023. Castellum: A Data Protection-                     Knowledge Graph Framework for Interactive, Domain-Specific LLM Chatbots.
     Compliant Web Application for the Subject Management of Human Science                       In Proceedings of the 34th ACM International Conference on Information and
     Studies. In Proceedings of the Conference on Research Data Infrastructure (CoRDI),          Knowledge Management (CIKM). ACM. doi:10.1145/3746252.3761459
     Vol. 1. doi:10.52825/cordi.v1i.325
[14] Max Planck Computing and Data Facility. 2025. Viper-GPU User Guide. https:
     //docs.mpcdf.mpg.de/doc/computing/viper-gpu-user-guide.html. 228 nodes, 2 ×
     AMD Instinct MI300A APUs per node, 128 GB HBM3 per APU.
[15] Natalya F. Noy and Deborah L. McGuinness. 2001. Ontology Development 101:
     A Guide to Creating Your First Ontology. Technical Report. Stanford University.
     Stanford Knowledge Systems Laboratory Technical Report KSL-01-05.
[16] D. Paslavska, J.M. López-Gil, J. Pereira, R. Gil, and R. García. 2026. Rhizomer-LLM:
     Natural language interface for semantic data exploration. SoftwareX 35 (2026),
     102834. doi:10.1016/j.softx.2026.102834
[17] Nitarshan Rajkumar, Raymond Li, and Dzmitry Bahdanau. 2022. Evalu-
     ating the Text-to-SQL Capabilities of Large Language Models. arXiv preprint
     arXiv:2204.00498 (2022).
[18] Mohammed H. Rasheed and Marina Aguado. 2025. LLM-Based Natural Language
     to SPARQL Translation over Domain-Specific Knowledge Graph. Knowledge
     Organization 52, 8 (2025), 42705. doi:10.31083/KO42705
[19] RDFLib Team. 2024. rdflib: A Python library for working with RDF. https:
     //github.com/RDFLib/rdflib.
[20] Md Rashad Al Hasan Rony, Uttam Kumar, Roman Teucher, Liubov Kovriguina,
     and Jens Lehmann. 2022. SGPT: A Generative Approach for SPARQL Query
     Generation From Natural Language Questions. IEEE Access 10 (2022), 70712–
     70723. doi:10.1109/ACCESS.2022.3188714

