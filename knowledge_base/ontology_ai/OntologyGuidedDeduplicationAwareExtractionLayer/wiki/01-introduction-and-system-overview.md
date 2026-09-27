> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Introduction and System Overview
**In one sentence:** The paper presents a production extraction layer that converts a live Kafka stream of heterogeneous documents into a validated, ontology-aligned knowledge graph via format-specific handlers, two-pass extraction with a locally hosted ontology-tuned Qwen3.5-9B model steered by live ontology retrieval, and a five-stage refinement pipeline with rule-based plus embedding-based deduplication, lifting search recall from ~70% to 95% with zero false merges.
## Key points
- LLMs extract fluently but inconsistently: type vocabularies fracture across documents, one person appears under several name variants, relationships duplicate, and distinct same-named individuals risk silent conflation.
- The system is a real-time Kafka consumer that ingests document metadata, retrieves raw files from disk, and extracts with `Konect-U/Qwen3.5-9B-AWQ-4bit-Ontology` (4-bit AWQ-quantised, ontology-tuned Qwen3.5-9B) served on a GCP VM via vLLM with an OpenAI-compatible API, plus companion embedding model `Konect-U/Qwen3-Embedding-0.6B-Ontology`.
- Ontology-guided extraction retrieves the relevant ontology slice live from a Neo4j graph database by embedding similarity and injects it into the prompt, reducing catalog overhead by about 94 percent relative to static domain slices.
- The five-stage pipeline is S1 extract, S2 clean, S3 merge, S4 2nd pass (relationships), S5 enrich, ending in Pydantic-enforced validated JSON persisted both to the terminal and to per-document JSON files for downstream graph ingestion, with switchable local vLLM / Gemini providers.
- Refinement pairs six deduplication algorithms requiring no model inference with an embedding resolution subsystem whose conflict guard no similarity score can override.
- The codebase was refactored from three monoliths (`consumer.py`, ~1,860-line `model.py`, `str_op_schema.py`) into `src/extraction/` of roughly fifty focused modules grouped by responsibility (consumer, core, ontology, pdf/xlsx/docx/pptx/vision, dedup, resolution, parsing/schemas, providers).
- Evaluation on intelligence corpora improved search recall from approximately 70% to 95% with a zero false-positive / no-false-merge rate, and corrected seven classes of silent quality defect, from a single-character source-text truncation bug to systematic duplication of title-prefixed entities.
---
## Abstract
**Covers:** Abstract (arXiv:2607.28662v1 [cs.AI] 22 Jul 2026)

> "Large language models extract entities and relationships from unstructured documents fluently but inconsistently: type vocabularies fracture across documents, the same person surfaces under several name variants, relationships duplicate, and distinct individuals who share a name risk silent conflation."

System summary from the abstract:

| Element | Value in chunk |
|---|---|
| Input | Live document stream; document metadata from Kafka; PDF, spreadsheet, Office, and image content via per-format handlers |
| Extraction | Two passes using locally hosted Qwen3.5-9B tuned on the ontology |
| Distinguishing component | Relevant ontology slice retrieved live from a graph database by embedding similarity and injected into the extraction prompt; ~94% catalog-overhead reduction vs static domain slices |
| Refinement | Five stages: deterministic cleaning, merging across chunks, second pass for relationships, six deduplication algorithms requiring no model inference, embedding resolution subsystem with non-overridable conflict guard |
| Evaluation | Search recall ~70% to 95% with no false merges; seven classes of silent quality defect corrected |

Keywords: ontology-guided extraction, knowledge graph construction, entity resolution, retrieval-augmented generation, large language models.

## 1 Introduction — system design
**Covers:** Section 1 (Introduction)

Real-time Kafka consumer ingests document metadata from an upstream ingestion service, retrieves raw files from disk, and extracts structured entities/relationships from unstructured text, PDF, and image content.

| Model | Role |
|---|---|
| `Konect-U/Qwen3.5-9B-AWQ-4bit-Ontology` (4-bit AWQ-quantised, ontology-tuned Qwen3.5-9B) | Extraction model, deployed on GCP VM via vLLM with OpenAI-compatible API |
| `Konect-U/Qwen3-Embedding-0.6B-Ontology` | Ontology retrieval and embedding-based resolution |

Provider switching between local self-hosted models and cloud-hosted models is done through environment configuration, enabling "seamless fallback without code changes." Output is "a validated JSON knowledge graph conforming to a strict Pydantic-enforced schema, enriched with entity deduplication metadata."

Refactor history:

| Before | After |
|---|---|
| Three monoliths: `consumer.py`, ~1,860-line `model.py`, `str_op_schema.py`, with prompting, chunking, multi-phase extraction, retry logic, and deduplication entangled in one namespace | Modular `src/extraction/` package of roughly fifty focused modules |

Module groups (verbatim):

| Group | Modules / responsibility |
|---|---|
| `consumer/` | `kafka.py`, `record_processor.py`, `output.py`: Kafka consumption, message normalisation, MIME/extension-based routing, bounded-concurrency worker pool, sequence-ordered output buffering |
| `core/` | `entity_extractor.py`, `relationship_extractor.py`, `media_extractor.py`, `plain_text.py`, `prompts.py`: two-phase LLM extraction pipeline, prompt construction, relationship second-pass quality guards |
| `ontology/` | `catalog_injection.py`, `graph_retriever.py`, `context_composer.py`: live retrieval of relevant ontology slice from Neo4j ontology graph and injection into prompt |
| `pdf/`, `xlsx/`, `docx/`, `pptx/`, `vision/` | Per-format handlers for born-digital and scanned PDF, spreadsheets, Word, PowerPoint, images |
| `dedup/` | `alias_resolver.py`, `name_similarity.py`, `phonetic.py`, `candidates.py`, `merger.py`: rule-based deduplication, augmented with phonetic matching (Double Metaphone, Soundex, Jaro–Winkler) |
| `resolution/` | `engine.py`, `blocking.py`, `scorer.py`, `embedder.py`, `decision.py`, `store.py`: embedding-based resolution with FAISS blocking, multi-signal scoring, thresholded decision engine |
| `parsing/`, `schemas/` | `retry.py`, `json_parser.py`, `result_finalizer.py`, `entity_type.py`, `relationship_normalizer.py`; `extraction.py`, `disambiguation.py`: strict-retry parsing, finalisation, Pydantic data models |
| `providers/` | `local.py`, `gemini.py`, `base.py`: pluggable LLM backends with environment-driven switching, per-request timeouts, retry budgets |

Implementation language: Python.

## Architecture — five-stage pipeline (Fig. 1)
**Covers:** Fig. 1 and surrounding description

> "Fig. 1: High-level architecture of the extraction layer. The Kafka consumer routes each document by MIME type into the five-stage extraction pipeline (detailed in Fig. 15); the ontology graph steers the type vocabulary at Stage 1; the LLM provider is switchable between the local vLLM endpoint and Gemini; the final output is a validated JSON knowledge graph."

Flow: Kafka stream (`ingested-objects`) → format router → S1 extract, S2 clean, S3 merge, S4 2nd pass, S5 enrich → validated JSON knowledge graph, with Neo4j ontology graph live vector retrieval steering Stage 1 and Qwen3.5-9B (vLLM) / Gemini as the provider-switchable LLM.

## 1.1 Contributions
**Covers:** Section 1.1 (four contributions plus dedup framing)

1. Ontology-guided extraction: retrieves the relevant slice of a curated ontology live from a graph database using vector search over class definitions and injects it into the prompt, "so the model emits types drawn from the formal schema rather than free-form labels, in the spirit of retrieval-augmented generation."
2. Multi-format handling: extends extraction beyond PDF and plain text to spreadsheets, Word, PowerPoint, and images, with a deterministic plan-then-execute strategy for tabular data and a six-signal per-page classifier routing individual PDF pages to text, OCR, or skip paths.
3. Layered deduplication subsystem: pairs six zero-inference rule-based algorithms with an embedding-based resolution stage "whose hard-conflict guard no similarity score can override."
4. Empirical evaluation on intelligence-domain corpora quantifying mechanism impact and documenting upstream quality defects exposed and corrected.

Dedup framing: "a zero-overhead, rule-based deduplication pipeline that operates as a post-processing layer over LLM-extracted entities," positioned against entity-resolution literature requiring dedicated training data or pre-linked knowledge bases.

## The initial challenge, applied solution, and results
**Covers:** Section 1.1 sub-blocks (Initial Challenge / Applied Solution / Results)

The Initial Challenge (verbatim bullets):

- "Extracted entities possessed only a single alias (the base name as it appeared in the text)."
- Spelling variations (e.g., "John Doe" vs. "Jon Doe") were instantiated as entirely distinct entities.
- "The system lacked the capability to detect similarly named entities that might represent duplicates."
- "Consequently, graph searches missed roughly a quarter of valid entity matches due to these name variations."
- Identical names in disparate contexts risked incorrect merging into one entity (e.g., "Elena Petrov," a combustion scientist at Khamsin Institute, and "Elena Petrova," a malware analyst at Vektor Signal, could be falsely consolidated despite representing different individuals).

The Applied Solution: "A six-stage post-extraction enhancement pipeline" with algorithmic alias expansion to five-plus variants per entity, fuzzy source-text mining for spelling variations, linguistically aware similarity scoring, context-validated duplicate detection matching roles, organisations, and locations before any merge, qualifier-preserving relationship deduplication, and sequence-ordered parallel output buffering.

Results: "This methodology improved search recall from approximately 70% to 95% while maintaining a zero false-positive rate."

**Covers:** Paper abstract, contributions, and two-phase extraction pipeline overview (chunk 01, Sections Abstract–1.1, Fig. 1)
