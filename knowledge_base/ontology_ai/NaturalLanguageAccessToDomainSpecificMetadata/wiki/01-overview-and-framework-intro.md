> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview and Framework Intro
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
---
## Title, authors, and abstract
**Covers:** chunk sections: paper title/author block, Abstract, Keywords

Paper: "Natural Language Access to Domain-Specific Metadata: A Reusable Framework for LLM Query Generation" by Blake G. Fitch (blake.fitch@tuebingen.mpg.de, Max Planck Institute for Biological Cybernetics, Tübingen, Germany) and Cato Elia Kurtz (Max Planck Institute for Biological Cybernetics, Tübingen, Germany). Identifiers in chunk: "arXiv:2607.18029v2 [cs.DB] 10 Sep 2026".

Verbatim abstract claims:
- "Researchers need to answer ad-hoc questions about the contents of domain-specific archives but often lack the expertise to write structured queries on the metadata."
- "We show that when domain vocabulary and semantics are captured in a well-designed Web Ontology Language (OWL) ontology, Large Language Models (LLMs) can generate accurate structured queries zero-shot, that is, without task-specific fine-tuning examples, retrieval augmentation, or multi-agent orchestration."
- "We present the Natural Language Knowledge Graph Query (NLKGQ) system, a framework and development process that enables natural language access to metadata in such archives."
- "The framework includes a web interface that helps researchers pose natural language questions, which a domain-agnostic harness translates to SPARQL via an LLM and executes against a knowledge graph."
- "The development process begins with capturing domain vocabulary and semantics in a formal OWL ontology. Domain-specific code then extracts metadata from archive sources and imports it into a knowledge graph defined by the ontology."
- "Both the framework and process are designed to support reuse across multiple domains."
- "In this work, we demonstrate the system for metadata derived from a large-scale neuroimaging research archive, evaluating performance across multiple LLMs and ontology representations."
- "The best configurations achieve 100% accuracy on a 21-question competency and regression test set developed with domain experts."
- "An ablation study across eight ontology representations reveals that readable entity names and semantic annotations are the dominant factors in accuracy, more significant than model choice or prompt engineering."
- "We also compare SPARQL to an auto-generated SQL database as query backends, showing that OWL's structural features provide a substantial advantage over SQL DDL for LLM-driven query generation."
- "A notable consideration for our demonstration domain is a requirement to run local LLMs on modest institutional hardware in support of privacy concerns for human subject data."

Keywords (verbatim): "Knowledge Graph, Natural Language Interface, Metadata Search, SPARQL, SQL, OWL, RDF, Large Language Model, Ontology Design, Neuroimaging, DICOM, BIDS, MRI".

## Motivation and approach
**Covers:** chunk sections: Introduction (opening, prior-accuracy context, process summary, demo archive), truncated mid-sentence

- Problem setting: research facilities, enterprises, and government agencies accumulate large archives with rich metadata (e.g., subject demographics, acquisition parameters, experimental configurations, provenance records); ad-hoc querying requires writing SQL or SPARQL, which demands both query-language and domain-vocabulary knowledge that many researchers lack.
- Prior-accuracy context cited in chunk: on simple schemas like Spider [31], top models exceed 90% accuracy, but on real enterprise schemas with hundreds of tables, GPT-4o drops to 0% [3]; Sequeda et al. [21] find reformulating the same enterprise questions over a knowledge graph raises accuracy from 16% to 54%. Chunk's gloss: "How domain knowledge is structured matters as much as which LLM model is used."
- Ontology-first process (verbatim sequence): capture domain vocabulary and semantics in a formal OWL ontology [26] "using readable entity names and semantic annotations"; a domain-specific ETL pipeline maps archive metadata to the ontology, producing a KG; the KG stored in RDF Turtle format loads both a SPARQL database and, via automatic transformation, an SQL database, enabling systematic comparison with equivalent data and NL questions; an LLM generates queries against either backend, zero-shot, with the full ontology or derived schema in the system prompt.
- Co-evolution loop: "The domain-specific ontology, competency and regression test cases, and a domain-specific prompt rider evolve together through iterative testing," progressively refining vocabulary/semantics and "eliminating confusion and inaccuracies that plague even expert human communication."
- Demo archive: an MRI neuroimaging research archive [5] with metadata for 80 active studies and 2,000 MRI experiments; GDPR requires all processing remain on institutional infrastructure rather than external LLM services; practical objective is the smallest model with acceptable accuracy to keep hardware costs manageable for modest GPU resources.
- Evaluation headline in chunk: 8 locally deployed LLM variants (8B to 35B parameters, including quantized and mixture-of-experts variants); best model achieves 100% accuracy on SPARQL and 57% on auto-generated SQL, "with no fine-tuning, no retrieval augmentation, and no multi-agent orchestration [28, 33–35]"; stripping ontology annotations degrades SPARQL accuracy by 19 percentage points.
- Note: the chunk text truncates mid-sentence at "requires both knowledge of the query …" (page break into "Blake G. Fitch and Cato Elia Kurtz"); no further introduction content is present in this chunk.

**Covers:** Paper title/author block, Abstract, Keywords, and Introduction opening through the truncated sentence (archive context: 80 studies / 2,000 MRI experiments; accuracy figures: Spider >90%, GPT-4o on enterprise 0%, KG reformulation 16%→54%, 21-question set at 100%, 8 models 8B–35B, SPARQL 100% vs SQL 57%, −19pp without annotations).
