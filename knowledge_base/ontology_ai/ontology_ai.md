# Ontology AI

Research on **ontology engineering, semantic modeling, and knowledge graph construction** — building formal vocabularies and structured graphs from documents, especially with LLM assistance.

## Papers

- [[FrenchLegalKnowledgeGraph/summary]] — Builds a smart index for French maintenance law, turning 6,370 scattered legal articles into a searchable knowledge graph of obligations, actors, and sources.
- [[NaturalLanguageKnowledgeGraphQueryExecution/summary]] — Puts the full domain ontology in the LLM context so terms carry exact meanings, enabling reliable one-shot NL-to-SPARQL with ~90% on a 1,000-question benchmark.
- [[OpenOntologies/summary]] — Rust MCP toolbox validates LLM-built ontologies; strict one-to-one matching kills false alignments, and structured tool access more than doubles axiom accuracy.
- [[CQ4OE/summary]] — Standardized exam for AI turning competency questions into OWL ontologies. Models list terms well but struggle with relations, hierarchies, and full coverage.
- [[OntoExtend/summary]] — LLM assistant drafts ontology extensions from plain-English questions, reusing existing terms; answered all test questions with minimal junk, needing only quick proofreading.
- [[OntologyGuidedDeduplicationAwareExtractionLayer/summary]] — Strict ontology-guided extraction layer with live schema retrieval and deterministic dedup that lifts search recall from ~70% to ~95% with zero false merges.
- [[NaturalLanguageAccessToDomainSpecificMetadata/summary]] — Relabeling domain metadata with clear names and descriptions lets LLMs translate plain questions into exact SPARQL queries zero-shot, reaching 100% on an MRI archive benchmark.
- [[LargeLanguageModelsForOntologyEngineering/summary]] — Survey of 30 papers finds LLMs can draft, enrich, and check ontologies, but fragmented methods block comparison; shared benchmarks and human-AI workflows are needed.

## Research

- [[research/ontology-ai/index|ontology-ai]] — multi-source research: what ontology in AI is, how ontologies are built, represented in OWL/RDF/SPARQL and evaluated, and how they combine with LLMs and knowledge graphs (overview, digests, disagreements, open questions, lenses).
