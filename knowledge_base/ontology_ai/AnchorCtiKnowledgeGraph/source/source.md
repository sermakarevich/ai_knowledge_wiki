# Schema-Agnostic Knowledge Graph Construction via Hybrid Ontology Discovery for Cyber Threat Intelligence
Source: https://arxiv.org/abs/2606.01208
Kind: pdf
Fetched: 2026-09-23T12:58:42.538960+00:00
Tool: pdftotext
Research-Target: /Users/sergii/.ai/knowledge/research_topics/ontology_ai/research/ontology-ai
Topic: ontology_ai

                                          Schema-Agnostic Knowledge Graph Construction via Hybrid
                                              Ontology Discovery for Cyber Threat Intelligence
                                                   Seonwoo Kim                                          Jinwoo Kim                               Daegyu Kang
                                            Ministry of National Defense                  Incheon International Airport Corporation        Financial Security Institute
                                             Seoul, Republic of Korea                           Incheon, Republic of Korea                 Yongin, Republic of Korea

                                                                               Daeseong Kim                                Insup Lee∗
                                                                        Korean National Police Agency                  Korea University
                                                                          Seoul, Republic of Korea                  Seoul, Republic of Korea




arXiv:2606.01208v1 [cs.CR] 31 May 2026
                                            Abstract—Cyber threat intelligence (CTI) reports now serve as      properties (object and datatype), and structural constraints.
                                         essential resources for capturing adversary tactics, techniques,      Notable efforts include the unified cyber ontology (UCO) [7],
                                         and procedures observed in modern attack campaigns. While             STUCCO [8], and MALOnt [9]. These frameworks are typ-
                                         traditional CTI platforms reduce this intelligence to isolated
                                         indicators through fixed schemas such as STIX, ontology-based         ically formalized in the web ontology language (OWL) for
                                         representations preserve the semantic relationships needed for        class hierarchies and properties, supplemented by optional
                                         structured threat analysis. However, existing approaches for          shapes constraint language (SHACL) constraints for struc-
                                         ontology-aligned CTI extraction face three challenges: (i) schema-    tural validation. However, despite the introduction of many
                                         specific pipelines that require manual reconfiguration whenever       security ontologies over the past decade, no single schema
                                         the schema changes, (ii) prompt-based schema inclusion that
                                         fails to scale on large ontologies such as UCO, and (iii) reliance    has achieved widespread adoption in practice [10]. Recent
                                         on enterprise LLM APIs that conflicts with privacy constraints        studies have therefore explored the automated extraction of
                                         when integrating sensitive internal incident data. In this paper,     ontology-aligned knowledge from unstructured CTI text. Con-
                                         we present A NCHOR, a schema-agnostic CTI knowledge graph             ventional approaches rely on rule-based pipelines [11], [12]
                                         construction system that bridges LLMs and formal ontology             and classification models [13], [14]. Unfortunately, these meth-
                                         schemas. At the core of A NCHOR is hybrid ontology discovery, a
                                         search-and-navigate mechanism that dynamically explores large-        ods depend on hand-crafted rules or fixed type inventories,
                                         scale ontology schemas, combined with SHACL-based validation          requiring a complete redesign whenever the target schema
                                         to enforce schema-compliant type assignments. Experimental            changes. Large language model (LLM)-based methods [15]–
                                         results on the UCO, STIX, and MALOnt schemas show that                [17] are better suited for schema-agnostic extraction because
                                         A NCHOR outperforms existing baselines in ontology typing and         they can interpret ontology class descriptions directly without
                                         schema compliance. In addition, A NCHOR with a local LLM
                                         closely matches enterprise LLM typing performance, enabling           schema-specific engineering. However, existing LLM-based
                                         privacy-preserving CTI analysis with high fidelity.                   approaches have been validated only on small custom schemas
                                            Index Terms—Cyber threat intelligence, ontology, knowledge         and exhibit critical limitations when applied to large-scale,
                                         graph, large language models                                          real-world ontologies [18].
                                                                                                                  We identify three limitations of existing LLM-based au-
                                                                  I. I NTRODUCTION                             tomated ontology extraction approaches. First, conventional
                                            A comprehensive analysis of cyber campaigns requires more          methods [11], [15]–[17] either define their own custom
                                         than isolated indicators of compromise (IoC) [1]. Cyber threat        schemas or hard-code a specific ontology into the extraction
                                         intelligence (CTI) reports record the threat actors, attack se-       pipeline (schema dependency). This rigid design requires a
                                         quences, and technical evidence, explicitly detailing the causal      complete redesign whenever the underlying schema changes.
                                         relationships between attack steps. To facilitate automated           The resolution of schema dependency alone does not solve
                                         sharing of such knowledge, standardized data formats such as          the scalability problem, as the system must still present the
                                         the structured threat information expression (STIX) [2] and the       target ontology to the LLM at inference time. Second, prompt-
                                         malware information sharing platform (MISP) [3] have been             based schema inclusion strategies fail on large-scale ontologies
                                         widely adopted. However, these indicator-oriented formats             such as UCO. Hundreds of hierarchical classes exhaust the
                                         primarily capture low-level, isolated data points such as IP          context window and degrade the model’s ability to distinguish
                                         addresses and file names, discarding the causal dependencies          semantically similar types. Third, an inherent reliance on
                                         between attack steps and the analytical reasoning that links          enterprise LLMs complicates the integration of external CTI
                                         them [4]–[6].                                                         with sensitive internal incident data due to privacy and data-
                                            Ontology-based representations address this semantic gap           sovereignty concerns. In this context, we derive the following
                                         by defining a formal vocabulary of ontology classes, their            three challenges from the existing literature.
                                                                                                                  Challenge 1) How can we extract ontology-aligned
                                           ∗ Corresponding author: Insup Lee (islee94@korea.ac.kr)             knowledge without being tied to a specific schema? To
support diverse and evolving security standards [19], the sys-                                        Unstructured CTI Report
tem must decouple extraction logic from schema definitions.                                 Buckeye APT used Trojan.Bemstour to install
This decoupling allows different OWL/SHACL ontologies to                                    DoublePulsar by exploiting CVE-2019-0703.

be loaded without manually reconfiguring the pipeline.                              Indicator-Oriented               Ontology-Based Knowledge Graph
   Challenge 2) How can we handle large-scale ontolo-
gies that exceed the capacity of prompt-based schema                                                                Adversary
                                                                             File     name=Trojan.Bemstour                         uses
inclusion? Rather than including the entire schema in the                                                           Buckeye APT
                                                                           Vuln.       name=CVE=2019-0703
LLM prompt, the system must dynamically discover and                                                                       Exploit Tool                  Backdoor
                                                                                                                                             delivers
                                                                        Maware          name=DoublePulsar
retrieve only task-relevant ontology fragments. This dynamic                                                             Trojan.Bemstour                DoublePulsar

                                                                                                                                  exploits
retrieval enables schema-aware reasoning within large and               Data extraction without causal context          Vuln.
                                                                        results in isolated attribute-value pairs
hierarchical ontologies while keeping each query within the                                                         CVE-2019-0703
                                                                                                                    Knowledge graph with semantic relationships
context window.                                                                                                     preserves attack logics

   Challenge 3) How can we support privacy-preserving
CTI analysis with local LLMs? External CTI provides                Fig. 1. Comparison of two CTI data formats: indicator-oriented flat data and
greater operational value when integrated with internal alerts,    ontology-based knowledge graph.
logs, and incident reports, but such data is often too sensitive
to expose to enterprise LLMs. The system must therefore            changing threats [20]. Open-source CTI (OSCTI) is collected
enable ontology-grounded reasoning with locally deployed           from security blogs, threat reports, and vulnerability databases,
open-source LLMs while preserving competitive typing per-          providing a critical resource for understanding dynamic threat
formance.                                                          environments. To standardize the exchange of threat informa-
   To this end, we propose A NCHOR (Adaptive Navigation            tion, the security community widely adopts three data formats
for Cybersecurity Hybrid Ontology Reasoning), a schema-            and protocols. STIX [2] defines a set of domain objects (e.g.,
agnostic system that builds a structured threat knowledge          threat actors, malware, vulnerabilities) and their relationships
graph from unstructured CTI reports. The proposed method           in a JSON-based format. MISP [3] provides a collabora-
presents a hybrid ontology discovery mechanism, which en-          tive framework to share IoCs using a predefined attribute
ables LLMs to dynamically explore relevant sub-graphs of           taxonomy. The trusted automated exchange of intelligence
complex ontologies and separates the extraction pipeline from      information (TAXII) [21] acts as the transport protocol to
any specific schema. To ensure accurate and schema-compliant       distribute STIX-formatted data between organizations.
ontology alignment, A NCHOR also considers a SHACL-based
                                                                      While these formats enable efficient indicator sharing, their
validation during ontology typing. The main contributions of
                                                                   structures are limited to flat attribute-value pairs and pre-
this paper are summarized as follows.
                                                                   defined relationship types [4]. Fig. 1 illustrates differences
   • We propose A NCHOR , a schema-agnostic CTI knowl-
                                                                   between this indicator-oriented view and an ontology-based
      edge graph construction framework that decouples the         knowledge graph. In the threat knowledge graph, semantic
      extraction pipeline from any specific ontology schema,       relationships connect security entities into a coherent structure.
      supporting arbitrary OWL/SHACL ontologies at runtime         This connectivity allows analysts to trace the full attack flow
      without manual reconfiguration.                              rather than examine individual indicators in isolation. Ontolo-
   • We introduce hybrid ontology discovery, which combines
                                                                   gies are typically expressed in the web ontology language
      embedding-based semantic search with LLM-guided re-          (OWL), which defines class hierarchies alongside object and
      cursive navigation to retrieve only task-relevant ontolo-    datatype properties. These definitions often include optional
      gies, integrated with closed-loop SHACL validation to        shapes constraint language (SHACL) constraints for structural
      ensure schema-compliant knowledge graphs.                    validation, such as required attributes and cardinality bounds.
   • We demonstrate privacy-preserving CTI knowledge graph
      construction with locally deployed open-source LLMs,            UCO [7] unifies concepts from multiple security standards
      retaining 99.2% (entity) and 97.8% (predicate) of the best   (e.g., CyBOK, NIST, MITRE ATT&CK) into a single hi-
      enterprise LLM’s performance.                                erarchical framework defined in OWL/SHACL, containing
   The source code of A NCHOR will be publicly available in        hundreds of classes and properties. In contrast, MALOnt [9]
the near future to foster further research.                        provides a lightweight malware-focused ontology with only
                                                                   75 classes, 10 relations, and 12 properties. Despite the studies
                      II. BACKGROUND                               on security ontologies, the construction and maintenance of a
   This section reviews the necessary background on CTI data       comprehensive cybersecurity ontology remains an open prob-
formats, ontologies, and LLM-based knowledge extraction.           lem. A recent survey reports inconsistencies and ambiguities in
                                                                   cybersecurity terminology that hinder communication between
A. CTI Data Formats and Ontologies                                 security professionals [10]. Furthermore, no existing ontology
  CTI records adversary tactics, techniques, and procedures        fully aligns with the major security standards required for
(TTPs) and IoCs. This intelligence serves as a shared re-          seamless cross-platform integration. These practical limita-
source for organizations to coordinate defenses against rapidly    tions motivate the scenarios described in Section III.
B. LLM-based Knowledge Extraction                                                            TABLE I
                                                                    C OMPARISON OF CTI K NOWLEDGE G RAPH C ONSTRUCTION S YSTEMS
   LLMs have demonstrated strong performance in natural
language understanding and information extraction tasks [22],       System            Method       Schema dependency     Schema size
[23]. In the CTI domain, LLMs offer a practical alternative         TTPDrill [11]      Rule         Fixed (ATT&CK)            -
to traditional rule-based or keyword-matching systems. While        CTIKG [15]      LLM (prompt)       Open-ended             -
                                                                    CTINexus [16]   LLM (prompt)    Fixed (MALOnt)           60
these traditional systems struggle to capture the intent and        LLM4CTI [17]    LLM (prompt)      Fixed (STIX)           77
contextual nuances of attacker behavior, recent studies [5],         A NCHOR        LLM (hybrid)   Any OWL/SHACL       Up to 997 (UCO)
[15]–[17] show that LLMs can extract key entities and their
semantic relationships from threat reports with high perfor-            – URL: “update-check[.]site”
mance. This automated extraction reduces the need for manual            – IP: “45[.]77[.]23[.]91”
analyst intervention in knowledge graph construction.                   – File: “loader.exe”
   The integration of LLMs with external knowledge sources,           • Objects:
such as databases and ontology schemas, has traditionally
                                                                        – Scheduled Task: “WindowsUpdateCheck”
required separate implementations for each data source. This
                                                                        – Identity: Financial Sector
requirement creates tightly coupled pipelines that are difficult
                                                                      • Relationships:
to maintain. Recent agent frameworks address this fragmenta-
tion by providing standardized interfaces to access external            – Attributed-to APT-X
knowledge dynamically. This interactive approach grounds           Note that this isolation leads to the loss of semantic con-
LLM outputs in verifiable references rather than relying solely    nectivity: indicator-oriented formats log discrete values while
on parametric knowledge. Our design adopts this methodology        omitting the causality and rationale that link them together.
to ensure flexibility and maintainability. A uniform interface     For instance, the passage above includes a causal chain (e.g.,
between the LLM agent and the external ontology, aligned           (i) macro execution downloads the secondary payload and (ii)
with open standards such as the model context protocol             the C2 connection enables remote control) and an attribution
(MCP) [24], successfully decouples the extraction logic from       rationale (TTP overlap with APT-X), yet the STIX output
any specific schema (Section IV).                                  preserves only flat identifiers without any of this contextual
                                                                   reasoning. As a result, the structured output captures a frag-
                III. M OTIVATING E XAMPLES                         mented snapshot of the original report, with no representation
   This section illustrates the practical limitations of current   of the attack logic that connects these indicators. To pre-
automated CTI extraction through two scenarios: (i) informa-       serve these crucial relationships, an ontology-based knowledge
tion loss issues common to all indicator-oriented pipelines and    graph offers a promising alternative that explicitly models
(ii) a scalability limitation caused by prompt-based schema        semantic connectivity between threat entities.
inclusion in LLM.
                                                                   B. Limited Scalability of Prompt-Based Schema Inclusion
A. Information Loss in Indicator-oriented Formats                     Recent LLM-based methods map entities to ontologies
   To illustrate the information loss caused by indicator-         using prompt-based schema inclusion, which embeds the en-
oriented CTI data, consider the following passage from typical     tire class list directly into the input prompt. As shown in
threat analysis reports:                                           Table I, existing systems [11], [15]–[17] either hard-code a
     “In early March 2024, security analysts identified a          specific schema, operate without one, or rely on prompt-based
     spear-phishing campaign targeting Southeast Asian             inclusion at a small scale (60 to 77 elements). While prompt-
     financial institutions. The attacker delivered a Mi-          based inclusion is feasible for small schemas like MALOnt
     crosoft Word document disguised as an invoice via             and STIX, it introduces three severe limitations when applied
     email. When a user opens the document, a macro                to large-scale ontologies such as UCO (419 classes):
     executes to download a secondary payload from                 • Context exhaustion: Massive prompts with hundreds of
     hxxp://update-check[.]site/loader.exe. This payload              class descriptions trigger the “Lost in the Middle” phe-
     maintained access by creating a scheduled task                   nomenon [25], causing the model to miss relevant context.
     named “WindowsUpdateCheck” and afterward com-                 • Precision degradation: An excessive number of candidates
     municated with a command and control (C2) server                 degrades semantic precision, causing the model to confuse
     at 45.77.23.91 via TCP port 443. Analysis revealed               adjacent types (e.g., Process, Action, Event) or hallucinate
     that these techniques align with the activities of APT-          non-existent classes.
     X, known for macro-based initial access and invoice-          • Maintenance burden: A fixed class list requires manual
     themed lures.”                                                   reconfiguration whenever the schema is updated.
   When this scenario is mapped into indicator-oriented for-       Furthermore, none of the existing baselines verify whether
mats such as STIX, most CTI platforms extract only a limited       assigned types satisfy formal structural constraints, allowing
subset of isolated indicators:                                     invalid mappings to enter the knowledge graph undetected.
   • Indicators:                                                   These scalability and validation gaps highlight a critical mis-
alignment between static LLM prompts and complex security         B. Schema-Agnostic Extraction
ontologies. To process large-scale schemas without context           To prepare unstructured CTI data for ontology-aligned
exhaustion, a system requires dynamic exploration that re-        knowledge extraction, A NCHOR processes raw inputs through
trieves only task-relevant fragments on demand. Furthermore,      a sequential pipeline: (i) input preprocessing, (ii) knowledge
to prevent hallucinated mappings from corrupting the output,      extraction, and (iii) post-processing and filtering.
the system must enforce formal constraints before committing         1) Input Preprocessing: Given unstructured CTI text such
the data. Motivated by these exact requirements, Section IV in-   as threat reports, A NCHOR applies a recursive character-
troduces the architectural design of A NCHOR, which replaces      based splitting strategy to handle documents that exceed the
prompt-based full schema inclusion with an effective ontology     LLM context window. The splitter respects natural seman-
discovery and validation mechanism.                               tic boundaries (paragraph breaks, sentence boundaries, word
                                                                  boundaries) and retains a fixed-size overlap window between
                   IV. A NCHOR D ESIGN                            consecutive chunks to preserve cross-boundary context.
   We propose A NCHOR, a schema-agnostic threat knowledge            2) Knowledge Extraction: After preprocessing, A NCHOR
graph construction system that aligns entities and predicates     extracts structured entities and relationships from preprocessed
to large-scale OWL/SHACL ontologies via hybrid ontology           chunks through three phases: entity extraction, coreference
discovery. This section describes the system overview, the        resolution, and triplet extraction.
schema-agnostic extraction pipeline, and the hybrid ontology         Entity extraction. A NCHOR identifies all named entities
discovery procedure.                                              from each chunk through a dedicated LLM extraction call. An
                                                                  entity here refers to any phrase that denotes a concrete object
A. System Overview                                                or referent in the text, in contrast to descriptive expressions
                                                                  (e.g., adjectives, adverbs) or behavioral phrases that do not
   A NCHOR aims to construct threat knowledge graphs from         stand as standalone referents.
fragmented CTI data based on the following three principles:         Rather than restricting the process to predefined entity
(i) the extraction pipeline is decoupled from any specific on-    classes, the system captures a broad spectrum of referents
tology schema, supporting arbitrary OWL/SHACL ontologies          and defers formal ontology type assignment to the subse-
at runtime; (ii) ontology fragments are discovered dynami-        quent discovery stage. Each extracted entity is represented
cally rather than included as a whole in the LLM prompt,          as a tuple (name, type hint, properties), where type hint is a
keeping each query within the context window; (iii) during        short phrase that guides ontology class search, and properties
threat knowledge graph construction, every type assignment is     captures clearly stated literal attributes (e.g., implementation
verified against formal schema constraints before commitment,     language, alias, first-seen date). To maintain consistent ref-
ensuring schema compliance. As shown in Fig. 2, the result-       erencing, the extraction enforces name normalization (e.g.,
ing architecture consists of three core components: schema-       stripping leading articles, lowercasing) and performs cross-
agnostic extraction, hybrid ontology discovery, and knowledge     chunk unification using a normalized key, so that surface
graph construction.                                               variations such as “Fancy Bear Hacking Group” and “Fancy
   Schema-agnostic extraction. This stage extracts entities,      Bear” map to the same canonical entry while non-entity
coreferences, and relation triplets from preprocessed CTI text    behavioral descriptions are filtered out.
without binding the extraction logic to any specific ontology,       Coreference resolution. After entity extraction, A NCHOR
and forwards the structured output to the next stage for type     applies an entity-aware coreference resolution pass to each
assignment. Section IV-B details the full extraction pipeline.    chunk. The LLM replaces anaphoric references (pronouns,
   Hybrid ontology discovery. This stage aligns each ex-          role descriptors, near-demonstratives) with the corresponding
tracted element to a formal ontology class or property URI        canonical entity name from the unified list, reducing misat-
by combining embedding-based semantic search with LLM-            tributed or missing relations caused by unresolved anaphora.
guided hierarchical navigation over the target OWL/SHACL             Triplet extraction. With the extracted entity list in place,
schema. When the search confidence falls below a predefined       the system extracts structured relationships per chunk, pro-
threshold, the system switches to recursive schema traversal,     viding the entity list as an explicit restriction so that only
ensuring that domain-specific or novel terminology is correctly   known, verified entities appear as relation endpoints. This
resolved. Section IV-C details the discovery algorithm.           two-pass design (entities first, relations second) eliminates
   Knowledge graph construction. The validated type as-           subject-bias (over-generating relations for prominent entities
signments are assembled into an ontology-aligned knowledge        while neglecting less salient ones) and dangling references
graph through a SHACL-based closed-loop correction pro-           (relation endpoints absent from the final inventory), both of
cess: each candidate assignment is checked against the target     which frequently arise when entity discovery and relation ex-
schema, and the mapper is re-invoked with the violation report    traction are performed simultaneously. ObjectProperty triplets
until the output is conformant or a retry budget is exhausted.    represent entity-to-entity relations of the form (es , p, eo ) with
The resulting graph is serialized as JSON and, optionally, as     p a concise predicate phrase (e.g., “uses”, “targets”, “exploits”,
a Neo4j-importable Cypher file to support downstream multi-       “attributed to”) and an evidence sentence from the source
hop queries over attack chains.                                   text attached for grounding context during ontology alignment;
              (1) Schema-Agnostic Extraction                       (2) Hybrid Ontology Discovery                       (3) Knowledge Graph Construction
                                                                                Concept Overview
                                                                                                                                          Ontology-Aligned
           Input         Knowledge       Post-processing             LLM                   MCP          Ontology                       Threat Knowledge Graph
       Preprocessing     Extraction         & Filtering             Agent                 Server        Schema            SHACL
                                                                                                                         Validation
                           Entity              IoC                                                                                           Threat Actor
                         Extraction         Detection                       score   YES                 Ontology           Self
                                                                                             Direct
       Threat Reports                                                         ≥                          Typing         Correction
                                                           Embedding                       Alignment
                                                                              τ?
                        Coreference           Noise         Search
                         Resolution          Filtering                                                   Entity to                     Malware       Campaign
                                                                               NO                       Ont. Class       Schema
       Security Blog                                                                                                    Compliance
                                                                                            Scoped
                          Triplet           Duplicate
                                                                                            Search     Predicate to
                         Extraction         Removal
                                                                       Recursive                       Ont. Property
          Vuln. DB                                                                                                                    Indicator   Tool      Vuln.
                                                                       Navigation



Fig. 2. Architecture of the A NCHOR System: (i) Schema-agnostic extraction preprocesses CTI documents and extracts entities, coreferences, and triplets
without binding to a fixed ontology schema; (ii) Hybrid ontology discovery maps each entity and predicate to an ontology class or property URI via
embedding search when confidence meets τ , or recursive navigation otherwise; (iii) Knowledge graph construction applies SHACL validation with closed-loop
self-correction to build an ontology-aligned threat knowledge graph.



DatatypeProperty triplets capture entity-to-literal associations                          Algorithm 1. For this phase, the algorithm is instantiated using
such as language strings, timestamps, or boolean flags. The                               class-specific semantic search, the root class set Uroots , and
LLM is instructed to be exhaustive, evaluating every entity                               owl:Thing as the default fallback.
pair and capturing all stated attributes regardless of salience.                             Unlike predicate ontology typing, entity ontology typing
   3) Post-processing and Filtering: Following knowledge ex-                              executes only Steps 1 and 2 of the discovery process, with
traction, A NCHOR applies three deterministic post-processing                             Algorithm 1 instantiated in E NTITY mode.
steps: IoC detection, noise filtering, and duplicate removal.                                Step 1: Embedding-based search. The system first per-
In IoC detection, A NCHOR matches entity names against                                    forms embedding-based search, which computes a relevance
regular expression patterns and overrides their type hints with                           score for each candidate URI u in the ontology graph G:
a schema-agnostic descriptor (e.g., “IPv4 address”, “SHA-
256 hash”), enabling reliable class resolution in the mapping                                              1                  1
stage regardless of which ontology is active. In noise filter-                               score(u) =      sim(q, ename
                                                                                                                      u    ) + sim(q, edesc
                                                                                                                                          u   ) + δk , (1)
                                                                                                           2                  2
ing, A NCHOR removes non-entity strings such as temporal
                                                                                             where q is the query embedding derived from the query
expressions, short strings, and common descriptors. Finally, in
                                                                                          hint h (e.g., the entity’s type hint), ename
                                                                                                                                     u      and edesc
                                                                                                                                                   u    are
duplicate removal, A NCHOR merges duplicate entities sharing
                                                                                          pre-computed embeddings of the class name and description,
the same normalized key and removes duplicate or dangling
                                                                                          sim(·) denotes cosine similarity, and δk is a fixed keyword
triplets. The filtered output is then forwarded to the subsequent
                                                                                          bonus (set to 0.3 in our experiments) applied when the query
hybrid ontology discovery stage.
                                                                                          string appears verbatim in the class name or description. If the
C. Hybrid Ontology Discovery                                                              top candidate’s score meets or exceeds the entity confidence
   With the schema-agnostic knowledge extraction complete,                                threshold τentity (set to 0.45 in our experiments), the class is
A NCHOR aligns each extracted element to a formal ontology                                selected immediately.
class and property. Hybrid ontology discovery provides this                                  Step 2: Hierarchical recursive navigation. If no can-
alignment through a uniform tool-based interface between the                              didate from Step 1 clears the threshold τentity , the system
LLM agent and any OWL/SHACL ontology. At initialization,                                  activates hierarchical recursive navigation. From the set of
A NCHOR parses the target ontology file, pre-computes embed-                              root classes Uroots , the LLM evaluates semantic definitions
dings for all class names and descriptions, and indexes the type                          of each subclass tier and selects the most logically matching
hierarchy. It exposes six tools covering three targets (classes,                          branch, drilling down iteratively until it reaches a leaf node
attributes, relations), each with two operations: (i) embedding-                          or determines that no sufficiently matching branch remains.
based search that retrieves candidates by semantic similarity,                            This top-down approach compensates for the limitations of
and (ii) hierarchical recursive navigation that the LLM invokes                           embedding models by leveraging LLM reasoning, enabling
when search confidence is below the threshold τ . 1                                       precise classification of domain-specific or novel terminology.
   1) Entity Ontology Typing: A NCHOR determines the appro-                               The LLM bases this decision on the candidate subclasses’
priate formal ontology class for each extracted entity, repre-                            names, textual descriptions, and child counts presented at each
senting it as a uniform resource identifier (URI), by executing                           tier, signaling termination when no candidate aligns with the
                                                                                          target query hint h.
  1 To facilitate broader reuse, the discovery suite is provided as an MCP-                  Fallback. If the recursive navigation fails to identify a suit-
compatible server that includes the six core tools used in this work along with           able class, the entity defaults to owl:Thing, corresponding to
auxiliary functions for general-purpose ontology exploration. The underlying
hybrid ontology discovery architecture, however, is agnostic to any specific              the fallback return in Algorithm 1. This defensive assignment
tool-call protocol.                                                                       ensures the extracted entity and its associated relations remain
  Algorithm 1: Hybrid Ontology Discovery                          property’s declared XML Schema Definition (XSD) range. For
   Input: Query hint h; root URIs Uroots ; confidence threshold entity connections, the relation search targets ObjectProperty
        τ ; discovery mode m ∈ {E NTITY, P REDICATE}.             URIs by utilizing the evidence sentence captured during triplet
   Output: Matched ontology element URI u .       ∗               extraction as additional context. It applies direction-aware
     1: /* Step 1: Embedding-based search */                      score adjustments, adding a bonus (0.10) for direct forward
     2: Ucands ← Search(h)                                        relations and a minor penalty (−0.05) for inverse relations. To
     3: if Ucands ̸= ∅ and score(top(Ucands )) ≥ τ then           ensure completeness, both tools evaluate properties inherited
     4:    return top(Ucands )                                    from the transitive superclass hierarchy, leveraging SHACL
     5: end if                                                    domain annotations back-propagated during schema loading.
     6: /* Step 2: Hierarchical recursive navigation */              Step 2: Hierarchical recursive navigation. If the search
     7: ucurr ← LlmSelect(h, Uroots , RetrieveDesc(Uroots ))      score   falls below the predicate confidence threshold τpredicate
     8: if ucurr = none then                                      (set  to  0.30), the system triggers LLM-guided traversal. The
     9:    return Fallback(m)                                     traversal   starting point depends on the target: data-property
    10: end if                                                    navigation    roots at the bound entity URI, while object-property
    11: uscope ← ∅                                                navigation     roots at the (s, o) URI pair. From these roots,
    12: while true do                                             the   LLM     navigates     a structured property list organized by
    13:    S ← Children(ucurr )                                   inheritance     level    and   domain class. For object properties,
    14:    if S = ∅ then                                          the   LLM     additionally     infers the correct assertion direction
    15:       uscope ← ucurr ; break                              (forward    or  inverse).
    16:    end if                                                    Step 3: Scoped embedding search. Large schemas of-
    17:    ubest ← LlmSelect(h, S, RetrieveDesc(S))               ten  group properties under intermediate classes, making ex-
    18:    if ubest = none then                                   haustive    LLM traversal impractical (e.g., UCO contains 578
    19:       uscope ← ucurr ; break                              properties).     When navigation reveals a collapsed property
    20:    end if                                                 group    anchored     to an intermediate class uscope , A NCHOR re-
    21:    ucurr ← ubest                                          executes    the   embedding      similarity search restricted solely to
    22: end while                                                 the  properties    of that  class. This scoped pass allows the system
    23: if m = E NTITY then                                       to  handle    large     hierarchies   efficiently once anchored to a
    24:    return uscope                                          specific   branch.
    25: end if                                                       Fallback. If all three steps fail to identify a matching
    26: /* Step 3: Scoped embedding search (predicate) */         property,    A NCHOR defaults to rdfs:label for literal attributes
    27: if uscope ̸= ∅ then                                       and  rdfs:seeAlso      for entity relations. Similar to entity ontology
    28:    Ucands ← Search(h, scope = uscope )                    typing,   this  defensive    mapping ensures every extracted triplet
    29:    if Ucands ̸= ∅ and score(top(Ucands )) ≥ τ then        is preserved     in the   output   graph without fabricating incorrect
    30:       return top(Ucands )                                 schema     assignments.
    31:    end if
                                                                  D. Knowledge Graph Construction with SHACL Validation
    32: end if
    33: return Fallback(m)                                           After finalizing the entity and predicate mappings, A NCHOR
                                                                  assembles the typed elements into a unified knowledge graph.
                                                                  To ensure structural integrity, the system applies a SHACL-
in the knowledge graph without introducing an incorrect or based validation mechanism that evaluates every entity against
unverified type.                                                  the node shapes defined in the target ontology. This validation
   2) Predicate Ontology Typing: To assign a formal property targets cardinality constraints, verifying that required prop-
URI to each extracted triplet, A NCHOR extends the search- erties are present and that value counts fall within declared
and-navigate strategy used in entity ontology typing. Depend- bounds. Because LLM-based extraction often omits manda-
ing on the triplet type, it determines either an ObjectProperty tory attributes, missing required properties represent the most
URI for entity-to-entity relations or a DatatypeProperty URI common source of schema violations in this domain.
for entity-to-literal attributes.                                    For example, under the UCO schema, a cardinality violation
   Unlike entity ontology typing, this phase utilizes all three occurs if an extracted malware entity lacks the required
steps of Algorithm 1, with the algorithm instantiated in P RED - hash algorithm attribute, a common omission that renders the
ICATE mode.                                                       indicator unusable for downstream matching. Upon detecting a
   Step 1: Embedding-based search. A NCHOR deploys two violation, the system generates a structured feedback message
distinct search tools to handle attributes and relations. For detailing the violating entity, the failed constraint, and the
literal attributes, the embedding-based search identifies the op- expected correction. The LLM agent receives this feedback
timal DatatypeProperty. It extends Equation 1 with a datatype and re-invokes the appropriate discovery tool to rectify the
inference heuristic, applying a score boost when the inferred omission (e.g., searching for a missing required property).
XSD type (e.g., xsd:dateTime, xsd:integer) aligns with the A NCHOR limits this closed-loop self-correction to three retries
                                                                                                                           TABLE II
            File: buckeye-windows-zero-day-exploit                                                        S TATISTICS OF TARGET O NTOLOGY S CHEMAS
     Beginning in March 2016, Buckeye began using a variant of DoublePulsar
     (Backdoor.Doublepulsar), a backdoor that was subsequently released by                                Schema      Classes   Relations   Properties
     the Shadow Brokers in 2017. DoublePulsar was delivered to victims using
     a custom exploit tool (Trojan.Bemstour) that was specifically designed                               UCO           419        177         578
     to install DoublePulsar. Bemstour exploits two Windows vulnerabilities
     in order to achieve remote kernel code execution on targeted computers.                              STIX 2.1      109         92         311
     One vulnerability is a Windows zero-day vulnerability (CVE-2019-0703)                                MALOnt         75         10          12
     discovered by Symantec. The second Windows vulnerability (CVE-2017-
     0143) was patched in March 2017 after it was discovered to have been
     used by two exploit tools — EternalRomance and EternalSynergy — that
     were also released as part of the Shadow Brokers leak.                                   ences. Datatype properties such as malware types (“backdoor”
                                                                                              and “exploit-tool”) and alias (“Backdoor.DoubleParser”) attach
                                       Symantec                                               literal attributes to the entities. These typed entities, properties,
                                          Identity
                                                                                              and predicates jointly reconstruct the semantic connectivity
                                       investigates                                           discussed in Section III-A, including the causal chain, the
                                                                                              temporal sequence, and the qualitative reasoning that indicator-
                                     CVE-2019-0703
     exploit-tool
                                         Vulnerability                                        oriented formats omit.

                  malware_types          exploits                              Buckeye
                                                                                ThreatActor                           V. E VALUATION
                                                                    uses
                                     Trojan.Bemstour
                                          Malware                                                For reproducibility, we use a benchmark provided by
      Windows                                                                      uses
       Software                                               delivers
                                                                                              CTINexus [16], consisting of 149 CTI reports with manually
                                              backdoor
                                                                                              annotated entities, triplets, and ontology type labels. The orig-
                         exploits
        targets
                                                                                              inal benchmark targets only the small-scale MALOnt schema,
                                                         malware_types
                                                                                              so we additionally reconstruct ground-truth type labels for two
                                                                           DoublePulsar
    CVE-2017-0143                                                              Malware        larger schemas, UCO and STIX 2.1, as summarized in Table II.
         Vulnerability
                                                            alias
                                                                                              Three cybersecurity researchers established the ground truth
                                  Backdoor.DoubleParser                                       through a human-in-the-loop process. An ensemble of three
                                                                             authored-by
         exploits         exploits                                                            LLMs (GPT-5.4, Claude-Sonnet-4-6, and Gemini-3.1-flash)
                                                                                              produced the initial candidates, and the researchers manually
     EternalSynergy                  EternalRomance                        Shadow Brokers
           Malware                        Malware                               Identity      cross-examined and resolved conflicting assignments by con-
                                                                                              sensus.
Fig. 3. Example knowledge graph constructed by A NCHOR from a Buckeye                            For our baselines, we compare the F1 scores of A NCHOR
APT campaign report.
                                                                                              against three systems: TTPDrill [11], CTINexus [16], and
to prevent unbounded execution. If the violation persists after                               LLM4CTI [17]. We exclude CTIKG [15], as it performs
the maximum attempts, the system retains the entity with its                                  only knowledge extraction without ontology typing. Since
assigned class and flags it with a validation warning rather than                             CTINexus originally types only entities, we extend it to
silently discarding it. This approach minimizes unverified type                               predicate typing by reusing its prompt-based entity ontology
assignments while preserving the extracted intelligence.                                      typing method on relation predicates. We deploy A NCHOR
   Beyond constraint checking, these SHACL shapes facil-                                      on a workstation equipped with an NVIDIA GB10 board and
itate facet discovery for ontologies that organize auxiliary                                  128 GB of memory, where we serve Qwen3.5-35B locally
properties into compound structures (e.g., UCO). The sys-                                     via vLLM [26]. For a fair comparison, all baselines also use
tem performs this through a multi-strategy lookup combining                                   Qwen3.5-35B as their underlying model. In the comparison
property domain inspection, inheritance traversal, and SHACL                                  against enterprise LLMs (Section V-D), we additionally use
shape resolution. Finally, A NCHOR serializes the validated                                   GPT-5.4-mini and Claude Haiku-4.5.
type assignments as an ontology-aligned knowledge graph in
JSON format.                                                                                  A. Ontology Typing Performance
   To provide an intuitive understanding of how A NCHOR                                          We examine the ontology typing performance on three
reconstructs semantic connectivity from an unstructured CTI                                   schemas with different scales: UCO (large, 419 classes), STIX
report, as shown in Fig. 3, we visualize an example knowledge                                 (medium, 109 classes), and MALOnt (small, 75 classes). On-
graph constructed from a Buckeye APT campaign report.                                         tology typing measures whether the extracted entities and rela-
The resulting graph contains 10 typed entities of five classes                                tions can be aligned to formal ontology classes and properties.
(ThreatActor, Identity, Malware, Software, and Vulnerabil-                                    Since the UCO schema is deeply nested with multi-level class
ity), connected by typed predicates (e.g., uses, delivers, and                                hierarchies, we adopt a hierarchical F1 score that assigns full
exploits) that trace the attack chain from the exploit tool                                   credit (1.0) for an exact match and partial credit (0.6 for a one-
through the vulnerabilities and the backdoor to the Shadow                                    step parent or child mismatch, 0.3 for a two-step mismatch) to
Brokers leak. The two vulnerabilities (CVE-2019-0703 and                                      capture semantic proximity. We evaluate two complementary
CVE-2017-0143) are typed against the Vulnerability class,                                     tasks: entity ontology typing, where each extracted entity is
demonstrating accurate resolution of numerical CVE refer-                                     mapped to an ontology class uniform resource identifier (URI),
                            TABLE III                                                         TABLE V
   E NTITY O NTOLOGY T YPING P ERFORMANCE ON T HREE S CHEMAS       A BLATION S TUDY ON H YBRID O NTOLOGY D ISCOVERY C OMPONENTS

     System          UCO      STIX     MALOnt    Average
                                                                   Configuration   Entity Ontology Typing   Predicate Ontology Typing
     TTPDrill [11]   0.0652   0.1042   0.2305     0.1333
     CTINexus [16]   0.4439   0.5698   0.6370     0.5502           Search-Only             0.9184                    0.3142
     LLM4CTI [17]    0.4521   0.7886   0.6891     0.6432           Recurse-Only            0.7914                    0.6416
     A NCHOR         0.7347   0.8724   0.6942     0.7371           Hybrid (ours)           0.9364                    0.7843


                           TABLE IV                               performance on STIX and MALOnt, since its template-based
 P REDICATE O NTOLOGY T YPING P ERFORMANCE ON T HREE S CHEMAS     approach cannot produce property URIs outside the predefined
                                                                  ATT&CK vocabulary.
     System          UCO      STIX     MALOnt    Average
                                                                     Predicate ontology typing is more difficult than entity on-
     TTPDrill [11]   0.0033   0.0000   0.0000     0.0011          tology typing for all four systems: A NCHOR drops by 25.6%
     CTINexus [16]   0.1282   0.4289   0.4528     0.3366
     LLM4CTI [17]    0.4000   0.5355   0.5647     0.5001          (from 0.7371 to 0.5484) and LLM4CTI drops by 22.2% (from
     A NCHOR         0.5180   0.5860   0.5412     0.5484          0.6432 to 0.5001). The gap is intuitive since a predicate’s
                                                                  correct property URI depends not only on the surface verb
                                                                  but also on the domain and range of its subject and object
and predicate ontology typing, where each extracted relation
                                                                  entities, and on the direction of the edge (e.g., uses vs.
predicate is mapped to an ontology property URI.
                                                                  used by). Single-word embedding similarity alone is therefore
   Entity ontology typing. For each extracted entity, the         insufficient, and the schema-navigation component of hybrid
system selects the best-matching class URI from the target        ontology discovery becomes the main contributor to predicate
ontology. As shown in Table III, A NCHOR achieves the highest     ontology typing, as analyzed in Section V-B. The marginal un-
performance on every schema, with an average F1 of 0.7371.        derperformance of A NCHOR on MALOnt (0.5412 vs. 0.5647
Specifically, A NCHOR outperforms the second-best baseline        for LLM4CTI) is consistent with our earlier observation that
(LLM4CTI) by 62.5% (from 0.4521 to 0.7347) on the UCO             hybrid ontology discovery offers limited advantage on small
schema. The margin shrinks on smaller schemas: A NCHOR            schemas. The key findings from the ontology typing analysis
outperforms LLM4CTI by 10.6% (from 0.7886 to 0.8724) on           are summarized as follows: (i) A NCHOR generalizes to large
STIX and by 0.7% (from 0.6891 to 0.6942) on MALOnt.               hierarchical schemas where prompt-based schema inclusion
CTINexus, which includes the entire schema in the LLM             baselines collapse, and (ii) predicate typing remains a harder
prompt, suffers a 30.3% performance drop when scaling from        task than entity typing for all four systems, motivating the
MALOnt (0.6370) to UCO (0.4439). TTPDrill never exceeds           ablation study on hybrid ontology discovery in Section V-B.
0.2305 on any schema because it relies on a simple rule-based
pipeline.                                                         B. Ablation Study
   We observe that this performance gap widens as the schema         We isolate two design choices within hybrid ontology dis-
size grows, highlighting the contrast between prompt-based        covery: (i) the combination of embedding search and recursive
schema inclusion and the dynamic hybrid ontology discovery        schema navigation, and (ii) the embedding-similarity threshold
provided by A NCHOR. As the number of candidate classes           τ that controls when the system switches from search to
increases from 75 in MALOnt to 419 in UCO, prompt-based           recursive traversal. For both ablations, we use ground-truth
baselines exhaust the LLM context window and degrade due          entities and triplets as fixed inputs so that the reported scores
to the “lost in the middle” phenomenon [25]. In contrast,         reflect only the typing performance of each configuration,
A NCHOR retrieves only the relevant ontology fragments and        while all other parameters (ontology schema, candidate in-
remains stable on the larger schema. The small performance        ventory, scoring rule) remain unchanged.
difference on MALOnt indicates that hybrid ontology discov-          1) Effect of Hybrid Ontology Discovery: We evaluate
ery offers limited benefit when the schema fits easily within     three configurations on both ontology typing tasks: Hybrid
a single prompt. However, its advantage becomes highly            (A NCHOR), Search-Only, and Recurse-Only. The Hybrid con-
pronounced on large schemas such as UCO, where prompt-            figuration combines embedding-based search with hierarchical
based inclusion fails.                                            recursive navigation, while the others rely solely on one of
   Predicate ontology typing. The system maps each extracted      these strategies.
relation predicate to a formal property URI (either ObjectProp-      As shown in Table V, the Hybrid configuration achieves the
erty or DatatypeProperty). As shown in Table IV, A NCHOR          highest performance on both tasks, scoring 0.9364 on entity
achieves the highest average F1 of 0.5484, outperforming          typing and 0.7843 on predicate typing, while the two single-
the baselines on the UCO and STIX schemas. Specifically,          strategy baselines exhibit asymmetric behavior. On entity
A NCHOR outperforms LLM4CTI by 29.5% (from 0.4000                 ontology typing, Search-Only (0.9184) approaches the Hybrid
to 0.5180) on UCO and by 9.4% (from 0.5355 to 0.5860)             score, whereas Recurse-Only falls to 0.7914. The pattern
on STIX. On MALOnt, A NCHOR scores 0.5412, which is               reverses on predicate ontology typing: Recurse-Only reaches
4.3% below LLM4CTI at 0.5647. TTPDrill records zero               0.6416, while Search-Only collapses to 0.3142. Notably, the
Hybrid configuration improves performance by 22.2% (from                                          
0.6416 to 0.7843) over Recurse-Only and more than doubles
the score of Search-Only.                                                                         

                                                                            $ F F X U D F \
   The contrasting tendency of the two tasks reflects a struc-
tural difference between entity and predicate ontology typing.                                    
Entity ontology typing maps a single named entity to a class,
                                                                                                  
a problem that aligns well with semantic similarity over class
names and descriptions, so embedding search alone suffices                                        
in most cases. In contrast, predicate ontology typing requires                                                                                                                    
                                                                                                                               ( P E H G G L Q J  W K U H V K R O G  entity
reasoning over the subject-object relation, the property hierar-
chy, and directional constraints that distinguish subject from                                                                              (a)
object, all of which are structurally represented in the schema
and accessed through recursive navigation rather than lexical                                     
similarity. We further quantify this contrast in Appendix A:                                      
instrumented measurements show that 91.0% of entity-class                                         

                                                                            $ F F X U D F \
queries are resolved by embedding search alone, while 72.1%                                       
of ObjectProperty queries are routed to recursive navigation.
Ultimately, the hybrid configuration effectively combines these                                   
strengths: embedding-based search provides a fast lexical entry                                   
point for entities, and hierarchical recursive navigation handles                                 
                                                                                                                                                                                  
the structural reasoning needed for predicates.                                                                          ( P E H G G L Q J  W K U H V K R O G  predicate
   2) Effect of Embedding Threshold: To evaluate the effect
of the embedding thresholds, we analyze τentity for class search                                                                           (b)
in entity ontology typing and τpredicate for property search in       Fig. 4. Effect of the embedding thresholds on ontology typing performance:
predicate ontology typing. Each threshold controls when the           (a) entity ontology typing and (b) predicate ontology typing.
system accepts an embedding search result rather than trig-
gering a fallback to recursive navigation. The system accepts                                                      TABLE VI
                                                                                                S CHEMA N ON -C OMPLIANCE R ATE ON UCO S CHEMA
a candidate only if its similarity score reaches or exceeds
the corresponding threshold. We sweep each threshold over               System                                    Total Items                Violations               Non-compliance (%)
{0.20, 0.25, 0.30, . . . , 0.70} while keeping all other parameters     TTPDrill [11]                                3,784                        2,868                                75.8
fixed. We then measure the performance of the corresponding             CTINexus [16]                               10,382                        4,556                                43.9
typing task.                                                            LLM4CTI [17]                                 3,881                        1,950                                50.2
                                                                        A NCHOR                                      3,665                         191                                  5.2
   As shown in Fig. 4, the two tasks exhibit distinct optimal
thresholds and sensitivity patterns. For entity ontology typing,
performance peaks at τentity = 0.45 (0.9423) and remains              Note that optimal values may vary depending on the target
within 0.7% of this peak for τentity ∈ [0.30, 0.55]. This             ontology and downstream task. The key findings from this
performance converges to a constant 0.9353 at τentity ≥ 0.55,         ablation study are summarized as follows: (i) embedding-based
where every query triggers recursive navigation. For predi-           search and hierarchical recursive navigation are fundamentally
cate ontology typing, performance peaks at τpredicate = 0.30          complementary, where embedding search drives entity ontol-
(0.6596) and is more sensitive to the threshold value. This           ogy typing and recursive navigation drives predicate ontol-
task shows moderate fluctuations in the middle range and              ogy typing, and (ii) the asymmetric lexical richness between
experiences a sharper degradation by 6.2% (from 0.6596 to             classes and properties dictates distinct similarity thresholds for
0.6190) at τpredicate = 0.70.                                         optimal performance.
   This difference in optimal thresholds stems from the distinct
embedding similarity distributions of the two search targets.
                                                                      C. Schema Compliance
As detailed in Appendix A, entity-class queries demonstrate
a high median similarity of 0.837, whereas ObjectProperty                To investigate whether the constructed knowledge graph
queries demonstrate a much lower median of 0.244. Class               follows the formal structural rules of the target ontology,
names and descriptions provide rich lexical signals, enabling         we measure the non-compliance rate over the full set of
the system to tolerate a stricter threshold for entity ontology       extracted entities and triplets on UCO. This measurement is
typing. In contrast, property predicates offer weaker lexical         essential because downstream RDF/OWL reasoning systems
signals, requiring a more permissive threshold to prevent             reject malformed inputs at load time. An item fails if it violates
the system from indiscriminately routing every query into             at least one of two checks: (i) URI and namespace confor-
recursive traversal.                                                  mance, and (ii) SHACL constraints declared by the schema.
   Consequently, we adopt τentity = 0.45 and τpredicate = 0.30        These constraints cover required-attribute counts, datatype
as the default configurations for all subsequent experiments.         rules, malformed URIs, and missing required properties.
   As shown in Table VI, A NCHOR achieves the lowest non-                                         TABLE VII
compliance rate of 5.2%. Specifically, A NCHOR improves per-            E FFECT OF A NCHOR ON L OCAL AND E NTERPRISE LLM BACKBONES
formance over the second-best baseline (CTINexus) by 88.2%
                                                                        Backbone                        Discovery     Entity   Predicate
(from 43.9% to 5.2%). CTINexus and LLM4CTI emit class-
                                                                                                        w/o A NCHOR   0.4284    0.1491
like labels that satisfy URI conformance for common entity              Qwen3.5-35B (local)
                                                                                                        w/ A NCHOR    0.9364    0.7843
types. However, they skip schema-level checks, which causes
                                                                                                        w/o A NCHOR   0.3905    0.2849
missing required-attribute violations and datatype violations to        Gemma-4-26B (local)
                                                                                                        w/ A NCHOR    0.9198    0.6657
dominate their failure counts. TTPDrill produces rule-based
                                                                                                        w/o A NCHOR   0.4540    0.1581
templates with identifiers that diverge from the canonical              GPT-5.4-mini (enterprise)
                                                                                                        w/ A NCHOR    0.9410    0.8012
UCO namespaces. This divergence inflates URI conformance
                                                                                                        w/o A NCHOR   0.5412    0.4318
violations in addition to the required-attribute failures observed      Claude Haiku-4.5 (enterprise)
                                                                                                        w/ A NCHOR    0.9439    0.8021
in the LLM-based baselines.
   This performance gap arises from the closed-loop SHACL
validation described in Section IV-D. The baseline sys-               A NCHOR improves entity ontology typing by 118.6% (from
tems [11], [16], [17] do not perform this validation. A NCHOR         0.4284 to 0.9364), 135.5% (from 0.3905 to 0.9198), 107.3%
re-checks each predicted type against the required-attribute          (from 0.4540 to 0.9410), and 74.4% (from 0.5412 to 0.9439),
counts and datatype rules declared by the target schema before        respectively. Predicate ontology typing exhibits the same pat-
commitment. The system re-invokes the discovery tool when it          tern for all four backbones. The largest absolute improve-
detects a violation. We limit this self-correction to three retries   ments appear on local backbones, where the naive prompt-
to prevent unbounded execution. The system records any                based scores are the lowest (Table VII). The strongest enter-
remaining violation as a validation warning rather than silently      prise configuration (Claude Haiku-4.5 with A NCHOR) reaches
dropping it. Most violations in the LLM-based baselines are           0.9439 on entity ontology typing and 0.8021 on predicate
missing-attribute failures, such as a malware entity lacking          ontology typing. Meanwhile, the strongest local configuration
the required hash algorithm attribute. The closed-loop retry          (Qwen3.5-35B with A NCHOR) reaches 0.9364 and 0.7843.
addresses these failures by routing a targeted property search        This local configuration retains 99.2% (= 0.9364
                                                                                                                     0.9439 ) and 97.8%
back through the discovery tool.                                      (= 0.7843
                                                                           0.8021 ) of the performance  of  the best  enterprise model,
   The 5.2% of non-compliant items in A NCHOR represent               respectively.
violations that remain after the three-retry budget. These items         We observe that Qwen3.5-35B with A NCHOR (entity typing
typically correspond to exceptional cases where no candidate          of 0.9364 and predicate typing of 0.7843) outperforms Claude
property satisfies the missing required attribute. A NCHOR            Haiku-4.5 without A NCHOR (entity typing of 0.5412 and
retains these items with their assigned class and a validation        predicate typing of 0.4318) by 1.73× and 1.82×, respec-
marker to preserve the extracted intelligence for downstream          tively. This result indicates that the integration of A NCHOR
review. A graph with 5.2% marked items can be loaded into             into a local backbone delivers a larger gain than upgrading
an RDF triplestore with minimal cleanup. In contrast, the high        the backbone from local to enterprise. The four backbones
violation rates of the baselines require pre-validation of every      converge to a narrow performance band with A NCHOR. This
downstream query or manual cleanup of 40% to 75% of the               convergence occurs because the system offloads the heaviest
items before reasoning is possible.                                   part of the reasoning, such as the navigation of large class and
                                                                      property hierarchies under formal constraints, from the LLM
D. Local LLM Feasibility                                              to the schema itself. Consequently, the LLM is left with a
   A primary design goal of A NCHOR is the integration of             small bounded selection problem. This finding demonstrates
external CTI with sensitive internal incident data without            that for schema-grounded reasoning tasks such as ontology
exposing the data to enterprise LLM APIs. To demonstrate this         typing, the design of the discovery pipeline matters more
capability, we evaluate whether A NCHOR preserves competi-            than the raw capability of the underlying LLM. The key
tive typing performance with locally hosted open-source back-         findings of the feasibility analysis are summarized as follows:
bones. We compare four LLM backbones under two condi-                 (i) A NCHOR offloads structural reasoning from the LLM to the
tions: with A NCHOR and without A NCHOR (i.e., naive prompt-          schema, which reduces the performance gap between local and
based ontology typing). The local backbones are Qwen3.5-              enterprise backbones, and (ii) local deployment with A NCHOR
35B and Gemma-4-26B, served through vLLM on the local                 retains 99.2% (entity) and 97.8% (predicate) of the best enter-
workstation. The enterprise backbones are GPT-5.4-mini and            prise LLM performance. This level of performance supports
Claude Haiku-4.5, accessed through their official APIs. As            privacy-preserving CTI knowledge graph construction without
in Section V-B, we use ground-truth entities and triplets as          a loss of typing fidelity.
fixed inputs so that the measured performance reflects only
the typing stage.                                                                             VI. R ELATED W ORK
   As shown in Table VII, A NCHOR improves typing per-
formance for every backbone. Specifically, for Qwen3.5-                 The automation of structured knowledge extraction from
35B, Gemma-4-26B, GPT-5.4-mini, and Claude Haiku-4.5,                 CTI reports has been an active research topic. We organize
existing studies into three categories: rule-based pipelines,           Practical deployment in security operations. The local-
classification-based approaches, and LLM-based methods.              deployment configuration (Section V-D) directly addresses
   Rule-based pipelines. Husari et al. [11] proposed TTPDrill,       privacy regulations (e.g., GDPR, HIPAA) that restrict sen-
which mapped threat actions to MITRE ATT&CK patterns                 sitive data sharing. Our local backbones achieve nearly the
through natural language processing (NLP) over predefined            same typing quality as enterprise LLMs, making this privacy-
templates. Satvat et al. [12] introduced EXTRACTOR, which            preserving setup a practical default rather than a performance
built attack graphs through dependency parsing and heuristic         compromise. The primary trade-off is increased processing
rules. While these systems demonstrated automated CTI ex-            latency due to multiple LLM calls per entity. However, in
traction, they rely on hand-crafted rules that require manual        threat intelligence operations where reports are processed
updates when new attack patterns appear.                             asynchronously, this latency is a reasonable cost to maintain
   Classification-based approaches. Later studies adopted ma-        complete control over sensitive data.
chine learning models for CTI extraction. Alam et al. [13]              Ontology schema augmentation. Schema-aligned extrac-
presented LADDER, a BERT-based entity classifier for attack          tion is inherently bounded by the target schema’s expressive-
pattern recognition. Peng et al. [14] proposed a retrieval-          ness. For example, when encountering novel entities like newly
augmented named entity recognition (NER) pipeline with               registered CVEs, the schema often lacks a suitable class. In
adaptive instructions. Mouiche and Saad [27] combined Se-            these cases, A NCHOR conservatively defaults to owl:Thing
cureBERT [28] with a BiLSTM joint extractor for entity and           rather than assigning an imprecise or fabricated type. This
relation extraction. Piplai et al. [29] applied NER and fused        fallback mechanism highlights a fundamental limitation of
the results into the UCO knowledge graph. These methods              mapping dynamic text to a static ontology: a system cannot
improved upon rule-based systems, but they remain bound to           assign a concept that the schema does not define. Future
fixed type inventories defined during training. This limitation      work will explore ontology schema augmentation methods,
reduces their applicability when ontology schemas change.            dynamically generating new classes for concepts that repeat-
   LLM-based methods. Recent work has explored LLM-based             edly trigger this fallback to relieve static schema constraints.
pipelines for CTI knowledge extraction. Huang et al. [15]               Confidence-based typing. A NCHOR rejects mappings be-
proposed CTIKG, which used GPT-4 with in-context learning            low specific confidence thresholds (τentity and τpredicate ), de-
(ICL) to extract open-ended knowledge graphs from CTI                faulting unverified items to owl:Thing or generic properties.
reports while deliberately avoiding fixed ontology schemas.          This prevents low-confidence guesses from corrupting the
Cheng et al. [16] proposed CTINexus, which adopted a                 knowledge graph, which is essential to avoid misleading
similar ICL approach but aligned extracted triplets to the           threat attribution in security operations. While we establish
MALOnt ontology through in-context schema inclusion. How-            default thresholds (τentity = 0.45, τpredicate = 0.30) based on
ever, this design does not scale to large ontologies such as         Section V-B, these are empirical baselines. Operators should
UCO. LLM4CTI [17] introduced a chunk-wise dual-context               recalibrate these values depending on the target ontology’s
framework with GNN-based link prediction, but it relies on           complexity and the specific downstream analytical objective.
a fixed, custom-defined schema and does not support formal
ontology alignment. Other LLM-based systems for CTI knowl-                        VIII. E THICAL C ONSIDERATIONS
edge graph construction (TRACE [30], CTI-Thinker [31], At-              A NCHOR is designed as a defensive analysis tool to struc-
tacKG+ [32], LLM-TIKG [33]) and general-purpose sequence-            ture and integrate publicly available cyber threat intelligence.
to-sequence extractors (KnowGL [34], REBEL [35]) remain              All data used in this study originate from open-source threat
bound to fixed schemas or require task-specific fine-tuning.         reports that are freely accessible to the public. The system does
Furthermore, none of these systems addresses cybersecurity-          not discover or exploit new vulnerabilities. Its primary purpose
specific ontology constraints. None of the above systems             is to assist security analysts in organizing threat knowledge
validates type assignments against a formal schema. This             rather than enabling offensive operations.
omission causes hallucinated mappings to enter the down-
                                                                                           IX. C ONCLUSION
stream knowledge graph without verification.
   In summary, prior systems either bind to a fixed ontology            We have presented A NCHOR, a schema-agnostic CTI knowl-
during pipeline design or rely on in-context schema inclusion.       edge graph construction framework. A NCHOR has addressed
Furthermore, none of these systems verifies ontology typing          the limitations of existing LLM-based extraction pipelines,
against formal schema constraints. Therefore, A NCHOR has            such as schema dependency, scalability issues on large on-
addressed both limitations through schema-agnostic hybrid            tologies, and the privacy risks of enterprise LLMs. A NCHOR
ontology discovery with SHACL-based validation.                      introduces a hybrid ontology discovery mechanism that com-
                                                                     bines embedding-based search with LLM-guided hierarchical
                      VII. D ISCUSSION                               recursive navigation. Furthermore, a SHACL-based closed-
                                                                     loop validation enforces schema-compliant ontology typing,
   In this section, we discuss the operational trade-offs of local   reducing hallucinated mappings in the output graph. Exper-
deployment, the structural boundaries of static ontologies, and      imental results on UCO, STIX, and MALOnt demonstrated
the rationale behind our ontology typing mechanism.                  that A NCHOR improves UCO entity and predicate ontology
typing by 62.5% and 29.5%, while decreasing the schema                            [17] L. Huang, M. Zhang, Z. Chen, S. Ma, Z. Liu, Y. Ye, and X. Xiao,
non-compliance rate from 43.9% to 5.2%. When paired with                               “Llm4cti: Uncovering security entities and their interactions from un-
                                                                                       structured cyber threat intelligence.”
a locally deployed open-source LLM, A NCHOR maintains                             [18] M. Büchel, T. Paladini, S. Longari, M. Carminati, S. Zanero,
99.2% (entity) and 97.8% (predicate) of the typing per-                                H. Binyamini, G. Engelberg, D. Klein, G. Guizzardi, M. Caselli et al.,
formance of the best enterprise LLM, supporting privacy-                               “Sok: Automated ttp extraction from cti reports–are we there yet?” in
                                                                                       34th USENIX security symposium (USENIX Security 25), 2025, pp.
preserving CTI analysis without a loss of typing fidelity.                             4621–4641.
In future work, we will explore cross-ontology translation,                       [19] D. Preuveneers and W. Joosen, “An ontology-based cybersecurity frame-
where the schema-agnostic reasoning of A NCHOR maps threat                             work for ai-enabled systems and applications,” Future internet, vol. 16,
                                                                                       no. 3, p. 69, 2024.
knowledge between disparate schemas to facilitate seamless                        [20] T. D. Wagner, K. Mahbub, E. Palomar, and A. E. Abdallah, “Cyber
inter-organization CTI sharing.                                                        threat intelligence sharing: Survey and research directions,” Computers
                                                                                       & Security, vol. 87, p. 101589, 2019.
                              R EFERENCES                                         [21] OASIS Cyber Threat Intelligence Technical Committee, “TAXII version
 [1] N. Sun, M. Ding, J. Jiang, W. Xu, X. Mo, Y. Tai, and J. Zhang, “Cyber             2.1: OASIS standard,” https://docs.oasis-open.org/cti/taxii/v2.1/taxii-v2.
     threat intelligence mining for proactive cybersecurity defense: A survey          1.html, 2021, accessed: 2026-03-31.
     and new perspectives,” IEEE Communications Surveys & Tutorials,              [22] T. Brown, B. Mann, N. Ryder, M. Subbiah, J. D. Kaplan, P. Dhariwal,
     vol. 25, no. 3, pp. 1748–1774, 2023.                                              A. Neelakantan, P. Shyam, G. Sastry, A. Askell et al., “Language mod-
 [2] OASIS Cyber Threat Intelligence Technical Committee, “STIX version                els are few-shot learners,” Advances in neural information processing
     2.1: OASIS standard,” https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.        systems, vol. 33, pp. 1877–1901, 2020.
     html, 2021, accessed: 2026-03-31.                                            [23] J. Achiam, S. Adler, S. Agarwal, L. Ahmad, I. Akkaya, F. L. Aleman,
 [3] C. Wagner, A. Dulaunoy, G. Wagener, and A. Iklody, “Misp: The                     D. Almeida, J. Altenschmidt, S. Altman, S. Anadkat et al., “Gpt-4
     design and implementation of a collaborative threat intelligence sharing          technical report,” arXiv preprint arXiv:2303.08774, 2023.
     platform,” in Proceedings of the 2016 ACM on workshop on information         [24] X. Hou, Y. Zhao, S. Wang, and H. Wang, “Model context protocol
     sharing and collaborative security, 2016, pp. 49–56.                              (mcp): Landscape, security threats, and future research directions,” ACM
 [4] P. Gao, X. Liu, E. Choi, B. Soman, C. Mishra, K. Farris, and D. Song,             Transactions on Software Engineering and Methodology, 2025.
     “A system for automated open-source threat intelligence gathering and        [25] N. F. Liu, K. Lin, J. Hewitt, A. Paranjape, M. Bevilacqua, F. Petroni, and
     management,” in Proceedings of the 2021 International conference on               P. Liang, “Lost in the middle: How language models use long contexts,”
     management of data, 2021, pp. 2716–2720.                                          Transactions of the association for computational linguistics, vol. 12, pp.
 [5] Z. Li, J. Zeng, Y. Chen, and Z. Liang, “Attackg: Constructing technique           157–173, 2024.
     knowledge graph from cyber threat intelligence reports,” in European         [26] W. Kwon, Z. Li, S. Zhuang, Y. Sheng, L. Zheng, C. H. Yu, J. Gonzalez,
     symposium on research in computer security. Springer, 2022, pp. 589–              H. Zhang, and I. Stoica, “Efficient memory management for large
     609.                                                                              language model serving with pagedattention,” in Proceedings of the 29th
 [6] X. Liao, K. Yuan, X. Wang, Z. Li, L. Xing, and R. Beyah, “Acing                   symposium on operating systems principles, 2023, pp. 611–626.
     the ioc game: Toward automatic discovery and analysis of open-source         [27] I. Mouiche and S. Saad, “Entity and relation extractions for threat
     cyber threat intelligence,” in Proceedings of the 2016 ACM SIGSAC                 intelligence knowledge graphs,” Computers & Security, vol. 148, p.
     conference on computer and communications security, 2016, pp. 755–                104120, 2025.
     766.                                                                         [28] E. Aghaei, X. Niu, W. Shadid, and E. Al-Shaer, “Securebert: A domain-
 [7] Z. Syed, A. Padia, M. L. Mathews, T. Finin, A. Joshi et al., “Uco: A              specific language model for cybersecurity,” in international conference
     unified cybersecurity ontology,” in Proceedings of the AAAI Workshop              on security and privacy in communication systems. Springer, 2022, pp.
     on Artificial Intelligence for Cyber Security, 2016, pp. 195–202.                 39–56.
 [8] M. Iannacone, S. Bohn, G. Nakamura, J. Gerth, K. Huffer, R. Bridges,         [29] A. Piplai, S. Mittal, M. Abdelsalam, M. Gupta, A. Joshi, and T. Finin,
     E. Ferragut, and J. Goodall, “Developing an ontology for cyber security           “Knowledge enrichment by fusing representations for malware threat
     knowledge graphs,” in Proceedings of the 10th annual cyber and                    intelligence and behavior,” in 2020 IEEE International Conference on
     information security research conference, 2015, pp. 1–4.                          Intelligence and Security Informatics (ISI). IEEE, 2020, pp. 1–6.
 [9] N. Rastogi, S. Dutta, M. J. Zaki, A. Gittens, and C. Aggarwal, “Malont:      [30] Z. Xu, Z. Ning, T. Hu, J. Zhuge, Y. Wang, J. Cao, and M. Xu,
     An ontology for malware threat intelligence,” in International workshop           “Trace: Timely retrieval and alignment for cybersecurity knowledge
     on deployable machine learning for security defense. Springer, 2020,              graph construction and expansion,” arXiv preprint arXiv:2602.11211,
     pp. 28–44.                                                                        2026.
[10] M. Adach, K. Hänninen, and K. Lundqvist, “Security ontologies: A            [31] X. Yang, R. Zhong, Y. Chen, G. Peng, D. Yao, C. Chen, C. Wang,
     systematic literature review,” in International Conference on Enterprise          D. Zhang, Y. Zhou, and Z. Yang, “Cti-thinker: an llm-driven system for
     Design, Operations, and Computing. Springer, 2022, pp. 36–53.                     cti knowledge graph construction and attack reasoning,” Cybersecurity,
[11] G. Husari, E. Al-Shaer, M. Ahmed, B. Chu, and X. Niu, “Ttpdrill:                  vol. 9, no. 1, p. 106, 2026.
     Automatic and accurate extraction of threat actions from unstructured        [32] Y. Zhang, T. Du, Y. Ma, X. Wang, Y. Xie, G. Yang, Y. Lu, and E.-
     text of cti sources,” in Proceedings of the 33rd annual computer security         C. Chang, “Attackg+: Boosting attack graph construction with large
     applications conference, 2017, pp. 103–115.                                       language models,” Computers & Security, vol. 150, p. 104220, 2025.
[12] K. Satvat, R. Gjomemo, and V. Venkatakrishnan, “Extractor: Extracting        [33] Y. Hu, F. Zou, J. Han, X. Sun, and Y. Wang, “Llm-tikg: Threat intel-
     attack behavior from threat reports,” arXiv preprint arXiv:2104.08618,            ligence knowledge graph construction utilizing large language model,”
     2021.                                                                             Computers & Security, vol. 145, p. 103999, 2024.
[13] M. T. Alam, D. Bhusal, Y. Park, and N. Rastogi, “Looking beyond              [34] G. Rossiello, M. F. M. Chowdhury, N. Mihindukulasooriya, O. Cornec,
     iocs: Automatically extracting attack patterns from external cti,” in             and A. M. Gliozzo, “Knowgl: Knowledge generation and linking from
     Proceedings of the 26th international symposium on research in attacks,           text,” in Proceedings of the AAAI Conference on Artificial Intelligence,
     intrusions and defenses, 2023, pp. 92–108.                                        vol. 37, no. 13, 2023, pp. 16 476–16 478.
[14] J. Peng, H. Sun, X. Tian, C. Huang, Z. Li, and R. Yan, “From retrieval       [35] P.-L. H. Cabot and R. Navigli, “Rebel: Relation extraction by end-to-end
     to reasoning: A framework for cyber threat intelligence ner with explicit         language generation,” in Findings of the association for computational
     and adaptive instructions,” arXiv preprint arXiv:2512.19414, 2025.                linguistics: EMNLP 2021, 2021, pp. 2370–2381.
[15] L. Huang and X. Xiao, “Ctikg: Llm-powered knowledge graph construc-
     tion from cyber threat intelligence,” in First Conference on Language                                A PPENDIX A
     Modeling, 2024.
[16] Y. Cheng, O. Bajaber, S. A. Tsegai, D. Song, and P. Gao, “Ctinexus:                   D ETAILS OF H YBRID O NTOLOGY D ISCOVERY
     Automatic cyber threat intelligence knowledge graph construction using
     large language models,” in 2025 IEEE 10th European Symposium on                The ablation study in Section V-B shows that entity ontol-
     Security and Privacy (EuroS&P). IEEE, 2025, pp. 923–938.                     ogy typing and predicate ontology typing draw on different
components of hybrid ontology discovery. We analyze this            clear the predicate threshold at 60.0%, sitting between the
difference by recording, for each typing query, whether the         two extremes and matching the intermediate 54.4% search-
final answer comes from the embedding-based search step             resolution rate in Table VIII.
or from the hierarchical recursive navigation step. We also            Explanation of the ablation study. Together, Tables VIII
measure the top-1 search similarity to indicate how reliably        and IX explain why the ablation study in Section V-B affects
embedding similarity resolves each phase.                           entity typing and predicate typing so differently. Search-
                                                                    Only performs well on entity ontology typing because 92.9%
                            TABLE VIII                              of entity-class queries already clear τentity by embedding
 T YPING Q UERIES R ESOLVED BY S EARCH VS . R ECURSIVE NAVIGATION   similarity, but it loses most of predicate ontology typing
                                                                    because only 13.2% of ObjectProperty queries clear τpredicate
                Phase              Search   Recurse
                                                                    and the remaining 86.8% have no recursive navigation route
                Entity (class)     91.0%     9.0%                   available. Recurse-Only partially recovers the ObjectProperty
                DatatypeProperty   54.4%    45.6%
                ObjectProperty     27.9%    72.1%                   case because recursive navigation can travel the domain-
                                                                    range structure, but it underperforms on entity ontology typing
                Total              62.3%    37.7%
                                                                    because it discards the median similarity of 0.837 lexical signal
                                                                    in favor of a longer LLM-driven navigation. The full hybrid
   Resolution by phase. Table VIII shows that the two phases        configuration (A NCHOR) combines the two complementary
of hybrid ontology discovery are exercised at very different        signals: search resolves the lexically dominated portion (62.3%
rates depending on the typing target. The search-resolution         of all queries), and recursive navigation handles the schema-
rates for entity class, DatatypeProperty, and ObjectProperty        driven remainder (37.7%).
queries are 91.0%, 54.4%, and 27.9%, respectively, while
the remaining 9.0%, 45.6%, and 72.1% are answered by
recursive navigation. Entity typing and ObjectProperty typing
sit at opposite ends of this routing: the search-resolution rate
drops by 69.3% (from 91.0% to 27.9%) between the two
phases. DatatypeProperty typing sits between the two extremes
at 54.4% search and 45.6% recurse, because literal-valued
properties carry stronger lexical signals than relations but
weaker structural cues than entity classes. Aggregated over the
three phases, 62.3% of typing queries are answered by search
and 37.7% by recursive navigation, confirming that neither
component dominates the workload.

                             TABLE IX
 T OP -1 E MBEDDING S IMILARITY AND T HRESHOLD C LEARANCE R ATES

          Phase               Median    Mean    Above τ
          Entity (class)       0.837    0.856    92.9%
          DatatypeProperty     0.507    0.512    60.0%
          ObjectProperty       0.244    0.300    13.2%
          All                  0.624    0.702    57.9%


   Embedding similarity distribution. As shown in Table IX,
the top-1 similarity statistics align with the routing pattern
in Table VIII. The median top-1 similarities for entity-
class, DatatypeProperty, and ObjectProperty queries are 0.837,
0.507, and 0.244, respectively, and the means follow the same
ordering at 0.856, 0.512, and 0.300. The threshold-clearance
rates differ even more sharply: 92.9% of entity-class queries
exceed τentity = 0.45, whereas only 13.2% of ObjectProperty
queries exceed τpredicate = 0.30. ObjectProperty typing depends
on the domain-range pair of subject and object entities rather
than on the surface verb, so embedding similarity over surface
forms is a weak signal, which is consistent with the drop in
median top-1 similarity from 0.837 for entity-class queries to
0.244 for ObjectProperty queries. DatatypeProperty queries

