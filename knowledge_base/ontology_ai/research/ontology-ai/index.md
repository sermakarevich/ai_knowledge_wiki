---
type: Research
title: ontology_ai
description: A working engineer's guide to ontologies in AI — what they are, how they are built, represented in OWL/RDF/SPARQL and evaluated, and how they combine with LLMs and knowledge graphs.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-23T13:58:07Z
focus: What is ontology in AI, how are ontologies built, represented and evaluated, and how do they combine with LLMs and knowledge graphs for a working engineer?
topics:
  - ontology-foundations
  - owl-rdf-sparql
  - ontology-learning-llm-kg
lenses:
  - tech
  - ai
sources:
  processed: 8
  in_kb: 0
  unreachable: 2
runs:
  - { at: 2026-09-23, added: 8 }
tags:
  - ontology
  - llm
  - knowledge-graph
  - sparql
---

# ontology_ai

## How to work through this

1. Start with the three sub-topic digests under `topics/` — they are the only evidence this hub synthesizes: `01-ontology-foundations` maps the lifecycle-wide role of LLMs, `02-owl-rdf-sparql` details the controlled-semantics NL-to-SPARQL mechanism, and `03-ontology-learning-llm-kg` covers constrained generation and the validation stack.
2. Read `digest.md` for the condensed cross-topic synthesis, then `overview.md` for the narrative interpretation.
3. Read `agreements.md` for jointly supported claims with evidence, `disagreements.md` for disputed claims with competing positions, and `open_questions.md` for what remains unresolved.
4. Pick a lens (`lenses/tech.md` for software engineers shipping ontology-backed systems, `lenses/ai.md` for AI engineers combining LLMs with knowledge graphs).
5. Consult `sources.md` for the full source ledger and per-source folders under `research_topics/ontology_ai/<Name>/summary.md` for primary detail.

## Cross-cutting

- LLMs assist across the full ontology-engineering lifecycle (requirements, implementation, publication, maintenance) as drafter, domain expert, and evaluator — but fragmented tasks, datasets, metrics, and thin human evidence block comparison.
- The consistent failure mode is a vocabulary-to-structure collapse: LLMs recover terms far better than relations, hierarchies, domain/range assignments, and full axioms, so unconstrained output is never committable.
- The fix that works everywhere is grounding generation in controlled semantics: retrieved ontology slices in context, readable names with comments/labels, explicit domain/range and class hierarchy, reuse-without-redeclaration, and deterministic normalization/deduplication.
- How the ontology reaches the model matters more than model choice: full OWL in context with a single zero-shot call, structured tool access over raw file dumps, and wrapper ontologies with deterministic rewriting for opaque vocabularies.
- Symbolic validation plus human review close the loop: SHACL/RDFLib gates, OOPS!/Pellet/HermiT consistency checks, CQ-as-SPARQL verification, and engineer ratings turn fluent drafts into merge-safe changes.
- What remains is standardization and scale: shared benchmarks with deterministic references, hybrid LLM-human workflows, and retrieval past context limits.
- [[agreements|Agreements]] — 6 shared findings

## Lenses

| lens | for |
|---|---|
| [[lenses/tech\|tech]] | software engineers building ontology-backed systems |
| [[lenses/ai\|ai]] | AI engineers combining LLMs with knowledge graphs |

## Sub-topics

| sub-topic | in one sentence | sources |
|---|---|---|
| [[topics/01-ontology-foundations/digest\|ontology-foundations]] | A systematic review of 30 papers (41 studies) finds LLMs can assist across the full ontology-engineering lifecycle but the evidence is fragmented by non-standard tasks, datasets, metrics, and workflows. | 1 |
| [[topics/02-owl-rdf-sparql/digest\|owl-rdf-sparql]] | Putting the complete domain OWL ontology directly in the LLM context window enables reliable single-call zero-shot NL-to-SPARQL, with wrapper ontologies extending this to opaque vocabularies. | 1 (+1 skipped) |
| [[topics/03-ontology-learning-llm-kg/digest\|ontology-learning-llm-kg]] | LLMs draft terms and triples fluently but collapse on structure, so every source converges on retrieved slices, controlled vocabularies, deterministic dedup, and symbolic validation plus human review. | 6 (+1 skipped) |

## Sources

| source | kind | folder |
|---|---|---|
| [[../../LargeLanguageModelsForOntologyEngineering/summary\|Large Language Models for Ontology Engineering: A Systematic Literature Review]] | paper | research_topics/ontology_ai/LargeLanguageModelsForOntologyEngineering |
| [[../../NaturalLanguageKnowledgeGraphQueryExecution/summary\|Natural Language Knowledge Graph Query Execution: Leveraging Controlled Semantics in the LLM Context Window]] | paper | research_topics/ontology_ai/NaturalLanguageKnowledgeGraphQueryExecution |
| [[../../CQ4OE/summary\|CQ4OE: A benchmark for assessing LLM-assisted ontology generation from competency questions]] | paper | research_topics/ontology_ai/CQ4OE |
| [[../../OpenOntologies/summary\|Open Ontologies: Tool-Augmented Ontology Engineering with Stable Matching Alignment]] | paper | research_topics/ontology_ai/OpenOntologies |
| [[../../NaturalLanguageAccessToDomainSpecificMetadata/summary\|Natural Language Access to Domain-Specific Metadata: A Reusable Framework for LLM Query Generation]] | paper | research_topics/ontology_ai/NaturalLanguageAccessToDomainSpecificMetadata |
| [[../../FrenchLegalKnowledgeGraph/summary\|LLM-Assisted Ontology Engineering and Construction of a French Legal Knowledge Graph]] | paper | research_topics/ontology_ai/FrenchLegalKnowledgeGraph |
| [[../../OntoExtend/summary\|OntoExtend: A Framework for Requirement-driven and Scalable Ontology Extension with LLMs]] | paper | research_topics/ontology_ai/OntoExtend |
| [[../../OntologyGuidedDeduplicationAwareExtractionLayer/summary\|An Ontology-Guided, Deduplication-Aware Extraction Layer for Knowledge Graph Construction from Heterogeneous Documents]] | paper | research_topics/ontology_ai/OntologyGuidedDeduplicationAwareExtractionLayer |

Two further shortlisted sources were unreachable and are not summarised: "When Do You Really Need RDF/OWL for Agentic AI?" (article, fetch failed HTTP 403) and "Schema-Agnostic Knowledge Graph Construction via Hybrid Ontology Discovery for Cyber Threat Intelligence" (paper, fetch failed). See `sources.md` for the full ledger.
