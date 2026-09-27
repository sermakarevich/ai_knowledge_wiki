# An Ontology-Guided, Deduplication-Aware Extraction Layer for Knowledge Graph Construction from Heterogeneous Documents
Source: https://arxiv.org/abs/2607.28662v1
Kind: pdf
Fetched: 2026-09-23T12:59:12.922523+00:00
Tool: pdftotext
Research-Target: /Users/sergii/.ai/knowledge/research_topics/ontology_ai/research/ontology-ai
Topic: ontology_ai

                                         An Ontology-Guided, Deduplication-Aware Extraction
                                            Layer for Knowledge Graph Construction from
                                                      Heterogeneous Documents



                                               Vaibhav Dangaich                   Kevin Lewis             Kundeshwar Pundalik
                                             vaibhavdangaich@gmail.com       kevin.lewis@konectu.in         kundeshwar@konectu.in




arXiv:2607.28662v1 [cs.AI] 22 Jul 2026
                                                                                    Abstract

                                              Large language models extract entities and relationships from unstructured documents
                                              fluently but inconsistently: type vocabularies fracture across documents, the same person
                                              surfaces under several name variants, relationships duplicate, and distinct individuals
                                              who share a name risk silent conflation. This paper presents the design, implementation,
                                              and empirical refinement of a production extraction layer that converts a live document
                                              stream into a validated knowledge graph aligned to a formal ontology. The system
                                              consumes document metadata from Kafka, routes PDF, spreadsheet, Office, and image
                                              content through handlers built for each format, and extracts entities and relationships
                                              in two passes using a locally hosted Qwen3.5-9B model tuned on the ontology. Its
                                              distinguishing component is ontology-guided extraction: the relevant slice of a curated
                                              ontology is retrieved live from a graph database by embedding similarity and injected
                                              into the extraction prompt, reducing catalog overhead by about 94 percent relative
                                              to static domain slices. Extracted results then pass through a refinement pipeline
                                              of five stages: deterministic cleaning, merging across chunks, a second pass for
                                              relationships, six deduplication algorithms that require no model inference, and an
                                              embedding resolution subsystem whose conflict guard no similarity score can override.
                                              Evaluation on intelligence corpora improved search recall from roughly 70 to 95 percent
                                              with no false merges, and corrected seven classes of silent quality defect, ranging from
                                              a bug that truncated source text by a single character to the systematic duplication of
                                              entities that carried title prefixes.


                                         Keywords: ontology-guided extraction, knowledge graph construction, entity resolution,
                                         retrieval-augmented generation, large language models
1   Introduction
This paper presents an extraction system that transforms a real-time stream of heterogeneous
documents into a validated, ontology-aligned knowledge graph. It operates as a real-time Kafka
consumer [1] that ingests document metadata from an upstream ingestion service, retrieves the
corresponding raw files from disk, and employs a locally hosted Large Language Model (LLM),
deployed on a GCP virtual machine via vLLM [2] with an OpenAI-compatible API, to extract
structured entities and relationships from unstructured text, PDF, and image content. The extraction
model is Konect-U/Qwen3.5-9B-AWQ-4bit-Ontology, a 4-bit AWQ-quantised, ontology-tuned
Qwen3.5-9B model, and ontology retrieval (Section 4) and embedding-based resolution (Section 6.5)
use the companion embedding model Konect-U/Qwen3-Embedding-0.6B-Ontology. This
approach builds upon the growing body of work demonstrating the efficacy of LLMs for knowledge
graph construction [3, 4]. The system supports provider switching between these local self-hosted
models and cloud-hosted models through environment configuration, enabling seamless fallback
without code changes. The output is a validated JSON knowledge graph conforming to a strict
Pydantic-enforced schema [5], enriched with entity deduplication metadata. This output is persisted
both to the terminal for operator visibility and to a designated output directory as individual JSON
files for downstream graph database ingestion.
The system is implemented in Python. An earlier iteration was organised as three monolithic
files (consumer.py, a ∼1,860-line model.py, and str_op_schema.py); that design became
difficult to extend as new document formats and an ontology-grounding stage were added, and
the single model.py entangled prompting, chunking, multi-phase extraction, retry logic, and
deduplication in one namespace. The current system is therefore refactored into a modular package
(src/extraction/) of roughly fifty focused modules grouped by responsibility:

    • consumer/ (kafka.py, record_processor.py, output.py): Kafka consumption, message
      normalisation, MIME/extension-based routing, bounded-concurrency worker pool, and
      sequence-ordered output buffering.
    • core/ (entity_extractor.py, relationship_extractor.py, media_extractor.py,
      plain_text.py, prompts.py): the two-phase LLM extraction pipeline, prompt
      construction, and relationship second-pass quality guards.
    • ontology/ (catalog_injection.py, graph_retriever.py, context_composer.py):
      ontology-guided extraction: live retrieval of the relevant ontology slice from a Neo4j ontology
      graph and its injection into the extraction prompt (Section 4).
    • pdf/, xlsx/, docx/, pptx/, vision/: per-format extraction handlers for born-digital and scanned
      PDF, spreadsheets, Word, PowerPoint, and images (Section 5).
    • dedup/ (alias_resolver.py, name_similarity.py, phonetic.py, candidates.py,
      merger.py): the rule-based deduplication algorithms, now augmented with phonetic
      matching (Double Metaphone, Soundex, Jaro–Winkler).
    • resolution/ (engine.py, blocking.py, scorer.py, embedder.py, decision.py,
      store.py): an embedding-based entity-resolution subsystem with FAISS blocking,
      multi-signal scoring, and a thresholded decision engine (Section 6.5).
    • parsing/ (retry.py, json_parser.py, result_finalizer.py, entity_type.py,
      relationship_normalizer.py) and schemas/ (extraction.py, disambiguation.py):
      strict-retry parsing, result finalisation, and the Pydantic data models that enforce structural
      guarantees on every extraction result.
    • providers/ (local.py, gemini.py, base.py):              pluggable LLM backends with
      environment-driven provider switching, per-request timeouts, and retry budgets.




                                                 2
                                                  Neo4j ontology graph
                                                     live vector retrieval




                                                                    five-stage extraction pipeline
      Kafka stream          Format                                                                                   Validated JSON
  ingested-objects          router                                                                                   knowledge graph
                                                 S1 extract       S2 clean    S3 merge     S4 2nd pass   S5 enrich




                                              Qwen3.5-9B (vLLM) / Gemini
                                                     provider-switchable



Fig. 1: High-level architecture of the extraction layer. The Kafka consumer routes each document by MIME
type into the five-stage extraction pipeline (detailed in Fig. 15); the ontology graph steers the type vocabulary
at Stage 1; the LLM provider is switchable between the local vLLM endpoint and Gemini; the final output is a
validated JSON knowledge graph.


1.1      Contributions

This paper makes four contributions. First, ontology-guided extraction (Section 4) retrieves the
relevant slice of a curated ontology live from a graph database, using vector search over class
definitions, and injects it into the extraction prompt, so the model emits types drawn from the formal
schema rather than free-form labels, in the spirit of retrieval-augmented generation [6]. Second,
multi-format handling (Section 5) extends extraction beyond PDF and plain text to spreadsheets,
Word, PowerPoint, and images, with a deterministic plan-then-execute strategy for tabular data and
a six-signal per-page classifier that routes individual PDF pages to text, OCR, or skip paths. Third,
a layered deduplication subsystem (Section 6) pairs six zero-inference rule-based algorithms with
an embedding-based resolution stage whose hard-conflict guard no similarity score can override.
Fourth, an empirical evaluation (Sections 8.1–8.2) on intelligence-domain corpora quantifies the
impact of these mechanisms and documents the upstream quality defects they expose and correct.
The entity deduplication system addresses a critical gap in knowledge graph construction: the
handling of name variations and the prevention of false entity merges. This challenge has been
extensively studied in the entity resolution literature [7, 8], yet existing approaches typically
require dedicated training data or pre-linked knowledge bases. Our contribution is a zero-overhead,
rule-based deduplication pipeline that operates as a post-processing layer over LLM-extracted entities.


The Initial Challenge.       Prior to this enhancement, the system exhibited several limitations:

       • Extracted entities possessed only a single alias (the base name as it appeared in the text).
       • Spelling variations (e.g., “John Doe” vs. “Jon Doe”) were instantiated as entirely distinct
         entities.
       • The system lacked the capability to detect similarly named entities that might represent
         duplicates.
       • Consequently, graph searches missed roughly a quarter of valid entity matches due to these
         name variations.
       • Conversely, identical names appearing in disparate contexts were at risk of being incorrectly
         merged into a single entity (e.g., “Elena Petrov,” a combustion scientist at Khamsin Institute,
         and “Elena Petrova,” a malware analyst at Vektor Signal, could be falsely consolidated despite
         representing different individuals).


The Applied Solution. A six-stage post-extraction enhancement pipeline (detailed in Section 6.2)
addresses these limitations: algorithmic alias expansion to five-plus variants per entity, fuzzy
source-text mining for spelling variations [9], linguistically aware similarity scoring [10],
context-validated duplicate detection that matches roles, organisations, and locations before

                                                              3
any merge, qualifier-preserving relationship deduplication, and sequence-ordered parallel output
buffering.


Results. This methodology improved search recall from approximately 70% to 95% while
maintaining a zero false-positive rate.

2     Related work
LLMs for knowledge graph construction. Since the introduction of the Transformer architecture
[11] and the emergence of few-shot prompting in large models [12], a growing body of work
demonstrates that large language models can populate knowledge graphs directly from text [3, 4],
whether through zero-shot prompting [13], NER-style prompting [14], generative end-to-end relation
extraction [15], or revisited relation extraction [16]. These studies consistently report the failure
modes our system confronts in production: fragmented type vocabularies, hallucinated relations,
and a bias toward entity description over relation extraction. Our contribution is not a new extraction
model but an architecture that constrains and repairs a stock model’s output at every stage.


Ontology grounding and retrieval augmentation. An ontology is a formal specification of a
shared conceptualisation [17]; grounding extraction in such a schema is what keeps the emitted type
vocabulary coherent. Retrieval-augmented generation [6] conditions generation on retrieved free
text; we apply the same principle to a formal class hierarchy, retrieving the relevant ontology slice
by embedding similarity and injecting it into the extraction prompt. The centrality penalty we apply
to generic classes adapts PageRank [18] to schema retrieval. To our knowledge the combination of
live graph retrieval, subclass expansion, and predicate full-text search for extraction-time grounding
has not been described before.


Entity resolution and name matching. Entity resolution traces to the probabilistic record-linkage
theory of Fellegi and Sunter [19] and has since matured into a broad field [20, 7], with blocking
surveys [8] and learned matchers from Magellan [21] to transformer-based matchers [22]. Classical
name-matching work covers personal-name abbreviation [23], string-metric comparisons [24, 25],
the Jaro–Winkler measure our scorer relies on [26], phonetic codes [27], and cross-lingual matching
[10, 28]; entity linking and disambiguation supply the contextual-evidence principle [29, 30]. The
embedding-based layer follows the modern practice of dense sentence representations for semantic
similarity [31]. Unlike learned matchers, our six rule-based algorithms require no training data and
run at zero inference cost, while the embedding-based layer adopts the canonical blocking–matching
pipeline with a hard-conflict guard that no similarity score can override.

3     System overview
The extraction layer runs as a real-time Kafka consumer that receives document metadata from the
upstream ingestion phase, resolves either file-based records (metadata pointers to files on disk) or
database-embedded records (full text inline), and normalises both into a single internal representation
before extraction. Consumer configuration, session-timeout tuning, and parallelism settings are
operational rather than scientific concerns and are collected in Appendix B. The subsections below
describe the extraction strategy itself: the two-phase prompt design, the quality gate that protects the
relationship pass, the chunking scheme, and the error-recovery behaviour.

3.1   Two-phase extraction pipeline

LLMs tend to prioritise entity descriptions over relationships [16], so extraction is split into two
calls: Phase 1 extracts entities and preliminary relationships in the zero-shot paradigm [13, 14];
Phase 2 re-reads the text alongside the extracted entity catalog and focuses solely on relationships,
including temporal and contextual qualifiers. The outputs are consolidated by qualifier-preserving
deduplication (Fig. 11), after which Phase 3 (post-extraction enhancement, Figs. 7–10) refines the
entity data.


                                                   4
3.2    Quality-gated relationship second pass

Ratio-based skip logic (“if |𝜌| ≥ 50, skip the second pass”) can false-trigger on documents where
the existing relationships are disproportionately concentrated on one type or where entire relation
families are structurally absent. To protect against these under-extraction cases, a quality-gate
evaluation precedes the skip decision, implementing four domain-informed checks:

   1. Financial connectivity. If financial entities are present alongside non-financial ones but zero
      cross-type relationships exist, the second pass is forced. This is a structurally common pattern
      where financial nodes appear as sources of funding but the LLM failed to connect them.
   2. Financial relation types. Even when the cross-type edges exist, if no relationship label
      matches FUND|BUDGET|APPROV (case-insensitive), the second pass is forced. This catches
      cases where financial relationships were extracted under non-standard labels that evade the
      cross-type edge check.
   3. Person relation diversity. When the entity set contains ≥ 8 persons, fewer than 4
      non-REPORTED_TO person relationships triggers forcing. This prevents the known “all roads
      lead to REPORTED_TO” LLM failure mode, where the model collapses all inter-person links
      into a single structural type.
   4. Relationship type concentration. If more than 30% of relationships share a single type and
      fewer than 6 distinct types are present, the document likely received a shallow extraction that
      over-indexed on the most frequent signal in the text; the second pass is forced to surface the
      other families.

The gate returns a (should_force, reasons) pair; when forcing, the reasons list is logged so the
forcing decision is auditable. Crucially, the gate complements the ratio threshold: a document with
60 relationships of type REPORTED_TO only still triggers check 3 and check 4, even though it clears
the raw count. This heuristic-driven quality gate bridges the gap between shallow “good enough”
metrics and domain-specific extraction completeness.

3.3    Chunk-based extraction and merging

For extensive documents, content is partitioned to respect LLM context limits. The chunking strategy
differs by content type:


PDF and OCR text. Pages are grouped into fixed-size windows (default chunk_pages=5,
one-page neighbor overlap on each side).


Plain text and database records. Character-range chunking is used with configurable overlap
(default: 8,000-char chunks, 1,000-char overlap). Each chunk is prefixed with an explicit
overlap annotation, “Primary target chars: 𝑠–𝑒. Overlap chars: 1000.”, which tells
the model it is looking at partially replicated context from the previous call, reducing relationship
hallucination at chunk boundaries. This overlap-awareness matters: without the annotation, the
model treats the overlap region as a novel document section and tends to re-extract entities and
re-invent edges rather than recognising the continuation.
Following chunk-level extraction across all formats:

      • Entities are merged based on a canonical key.
      • Relationship references are remapped to these canonical IDs.
      • Phase 3 enhancements are applied to the consolidated entity set, ensuring that name variations
        discovered in any specific chunk propagate throughout the document’s extracted data.




                                                   5
3.4   Robustness and error recovery

The pipeline includes retry mechanisms and automated JSON repair functions to handle malformed
LLM outputs. The JSON parser handles both closed markdown fences (‘‘‘json ... ‘‘‘)
and unclosed fences (output truncated mid-stream), applying a three-stage recovery: closed-fence
extraction → open-fence extraction → raw JSON search, so truncated LLM responses yield the
maximum recoverable structure rather than a hard failure. When the main relationship extraction call
fails due to entity count exceeding the model’s capacity, a simplified fallback retries with the top-20
entities and a capped 30,000-character evidence window, recovering partial relationship coverage
rather than returning an empty result.


Failure tracking for re-runs. Chunks that hit unrecoverable errors (e.g. context-window overflow
on the local vLLM endpoint) are appended as self-contained JSONL records to a persistent failure
log (extraction_failures.jsonl), keyed by file path, object ID, stage, and the specific failed
chunk or page indices. The log is written under a module-level mutex so concurrent workers never
interleave partial records. Failed documents can be re-run as a batch from the log without re-scanning
the full corpus, a critical operational property in production pipelines where transient GPU memory
pressure may temporarily fail a document that would extract correctly on a retry.
Furthermore, the Phase 3 enhancement algorithms are designed to degrade gracefully; for instance,
if properties are missing, duplicate detection proceeds with adjusted confidence levels, ensuring
continued operation.

4     Ontology-guided extraction via live graph retrieval
The Problem with Un-Guided Extraction. A general-purpose LLM, asked to extract entities and
relationships, invents its own type vocabulary on a per-document and even per-chunk basis. The
same real-world class surfaces as GovBody, Government Organization, Govt. Agency, and
Ministry across documents; relationship labels proliferate similarly. The downstream knowledge
graph then carries a fractured, unaligned schema that frustrates ontology-conformant querying and
analytics. To make extraction more solid and predictable, we constrain the model by injecting a
description of the relevant ontology classes and predicates into the extraction prompt. The question
is which part of the ontology to inject, and how to choose it; this is where the design evolved from
static slices to live graph retrieval.


The First Approach: Static Catalog Slices. The initial design pre-compiled the ontology into a set
of domain slices. An offline build step (build_ontology_catalog.py) walked the ontology and
emitted one prompt-ready text file per domain: catalog_cdr.txt, catalog_south_asia.txt,
a cross-domain catalog_bridge.txt carrying shared predicates (HAS_PHONE, LOCATED_IN,
. . . ), and a full catalog_full.txt for inspection. At extraction time a read-side loader
(catalog_loader.py) memoised each slice and estimated its size with a chars/4 token heuristic
against a soft budget (∼20,000 tokens; the worst routed case of three domains plus the bridge slice
came to ∼17,700 tokens).
The selection of slices per file was performed by a deterministic router (file_router.py)
implementing a three-tier keyword decision tree, comparing the file against a curated, domain-unique
keyword vocabulary:

    1. Strong filename match (a domain keyword present in the filename, e.g. 07_cdr_data.csv
       → cdr): trust the filename and skip the content scan.
    2. Weak filename match (an ambiguous single hit): read a ∼2 KB content sample and combine
       filename and content signals.
    3. No filename match: scan content only; if that too is inconclusive, fall back to the bridge plus
       a broad regional slice for default coverage.

The chosen slices were then concatenated into the system prompt, and a FORCE_CATALOG_SLICES
override allowed pinning specific slices for testing. This was a clear improvement over un-guided

                                                  6
extraction, since it bounded the type vocabulary and made outputs far more predictable, but it carried
structural limitations:

    • Coarse, all-or-nothing granularity. Selection was at the domain level: the entire slice was
      injected even when a document touched only a handful of its classes, spending context budget
      on irrelevant types.
    • Brittle routing. Keyword matching depends on filename conventions and a hand-curated
      vocabulary; opaque hashed filenames, multilingual content, or unanticipated synonyms
      misroute the file and inject the wrong (or default) slice.
    • Maintenance drift. The slice text files are a materialised snapshot. Every ontology edit
      requires rerunning build_ontology_catalog.py; between rebuilds the injected catalog
      silently diverges from the live schema.
    • Budget pressure. Injecting whole domains (∼17.7 K tokens in the worst case) crowds out
      document content in a 32 K-token window.


The Current Approach: Live Graph Retrieval. We replace the static slice with live,
content-conditioned retrieval of the ontology, in the spirit of retrieval-augmented generation [6]
but targeting a formal class hierarchy rather than free text. A curated ontology is materialised
as a Neo4j graph in which every class and predicate carries a natural-language definition and a
pre-computed embedding. At extraction time, the relevant slice of that ontology is fetched on
demand and injected into the system prompt, so the model is steered to emit types drawn from the
formal schema. The mechanism (ontology/graph_retriever.py, catalog_injection.py,
context_composer.py) comprises five elements:

   1. Multi-span windowing. The content sample is split into overlapping windows (∼1,500
      characters, 300-character overlap, up to four windows) rather than embedded as one vector. A
      single vector over a multi-entity chunk collapses to a blended centroid that retrieves nothing
      specifically; per-window embeddings preserve local topicality.
   2. Vector retrieval over class definitions. Each window is embedded and used to query a
      Neo4j vector index (db.index.vector.queryNodes) over the ontology’s class/predicate
      embeddings, returning candidate classes with their cosine score, definition, alternative labels,
      and graph centrality.
   3. PageRank-penalised scoring. High-centrality ancestor classes (Entity, Organization,
      Location) match almost everything and would dominate every retrieval. We down-weight
      them using a PageRank [18] penalty,
                                                          
                          score(𝑐) = cos(𝑞, 𝑐) 1 − 𝜆 pr(𝑐) ,    𝜆 = 0.4,
      so that a generic class must clear a higher cosine bar than a specific one to be injected.
   4. Dynamic cut-off under a token budget. Rather than a fixed top-𝑘, every class above an
      empirically motivated floor (min_score = 0.72) is taken, then trimmed to a token budget
      (∼5,000 tokens, apportioned 70% to classes and 30% to predicates). A 0.5 cosine floor
      admitted too many “vaguely related” classes; 0.72 retains genuinely relevant ones.
   5. Version-keyed caching and a circuit breaker. Retrievals are cached under a key combining
      the content hash and an ontology-version hash refreshed every ten minutes, so editing the
      ontology transparently invalidates stale entries. If the graph is unreachable the circuit opens
      for sixty seconds and extraction proceeds un-guided rather than blocking; ontology grounding
      is an enhancement, never a hard dependency.




                                                  7
Novel-Type Flagging. Grounding is steering, not a hard constraint: the prompt instructs the model
to use a catalogue type where one fits and otherwise to mark the emission as novel. After extraction,
flag_novel_types() compares every emitted entity and relationship type against the full ontology
vocabulary (after stripping pluralisation and wrapper suffixes such as (records), (entities)) and
sets _novel_type/_novel_predicate markers on those absent from the schema. These surface
downstream as candidate ontology extensions for human review, so the schema can grow from real
data without the model silently fragmenting the existing vocabulary.


Engineering Note. Because the Neo4j async driver and the embedding HTTP client bind to the
event loop on which they are first used, the retriever runs its coroutines on a single dedicated daemon
event loop (_run_coro with a 15-second timeout) rather than calling asyncio.run() per extraction,
which would create a fresh loop each time and trigger “future attached to a different loop” errors
from the cached singletons.


Impact. Content-conditioned retrieval injects only the handful of classes a document actually
needs, aligning emitted types with the formal ontology while keeping prompt overhead bounded.
This is the “grounding at extraction” stage that lets the rest of the pipeline reason over a coherent
schema rather than a bag of ad-hoc labels. Fig. 2 summarises the mechanism end-to-end.

        Document chunk (content sample)                                  Ontology-aligned entities & relationships


                                                    version cache
        Multi-span windowing + embedding           + circuit breaker
                                                                                     Novel-type flagging
        ∼4 overlapping windows, 300-char overlap                                → proposed ontology extensions


                                                       Neo4j
    Vector query over class/predicate embeddings      ontology                Injected into extraction prompt
            db.index.vector.queryNodes                 graph                           → LLM extraction



            PageRank-penalised scoring
                                                                                  Ontology catalog block
     score(𝑐) = cos(𝑞, 𝑐) 1 − 𝜆 pr(𝑐) , 𝜆 = 0.4                               only the relevant classes + predicates



                   Dynamic cut-off
        keep ≥ 0.72, trim to token budget (∼5k)




Fig. 2: Ontology-guided extraction via live graph retrieval, read as a U-shaped flow: the left column retrieves
(window, embed, query, score, threshold), the bottom arrow hands the surviving classes across, and the right
column injects (catalog block, prompt, novel-type flagging, aligned output). The Neo4j ontology graph sits
between the columns; retrieval is cached by ontology version and protected by a circuit breaker, so a graph
outage degrades to un-guided extraction rather than blocking.



Measured Impact on Injection Size. The shift from domain slices to class-level retrieval produces
a large, directly measurable reduction in the catalog prompt overhead. On a representative document,
the static router selected multiple domain slices (the matched domains plus the cross-domain bridge
slice), injecting roughly 11,200 tokens of catalog text into the system prompt, most of it classes the
document never used, carried only because they belonged to a selected domain. Live graph retrieval,
by contrast, injected only the handful of classes and predicates the document’s own content actually
retrieved: approximately 700 tokens for the same document. That is a ∼94% reduction (about a
16× smaller catalog block), summarised in Table 2.
This reduction matters on three fronts. First, in a 32 K-token window, reclaiming ∼10,500 tokens
lets substantially more of the source document share each extraction call, reducing chunking and
the cross-chunk fragmentation it causes. Second, a tighter catalog is a stronger steer: the model is
shown only classes that are genuinely relevant, so it is less likely to reach for a plausible-but-wrong
neighbouring type that a broad domain slice would have placed in front of it, so extraction becomes
both more predictable and more accurate. Third, the cost per call drops in proportion to the tokens

                                                          8
Table 1: Ontology injection: static catalog slices versus live graph retrieval.

      Dimension                 Static catalog slices (earlier)           Live graph retrieval (current)
      Granularity               Domain-level: the whole                   Class/predicate-level: only the
                                catalog_<domain>.txt is                   matched classes
                                injected
      Selection signal          Filename + ∼2 KB content                  Per-window embedding
                                keyword match against a curated           similarity over class definitions
                                vocabulary
      Relevance ranking         None within a slice                       Cosine score,
                                (all-or-nothing)                          PageRank-penalised,
                                                                          thresholded at 0.72
      Freshness                 Requires rebuilding slice files;          Always current; cached by
                                drifts from the live schema               ontology-version hash
      Token cost                Whole domain(s); worst case               Bounded budget of only relevant
                                ∼17.7 K tokens                            classes (∼5 K)
      Failure mode              Misroutes opaque                          Degrades to un-guided
                                filenames/synonyms; coarse                extraction via the circuit breaker
                                over-injection

Table 2: Catalog injection size for a representative document: domain slices versus graph retrieval.

         Metric                             Static slices             Graph retrieval        Change
         Catalog tokens injected             ∼11,200                        ∼700           −94% (∼16×)
         Selection unit               whole domains + bridge        matched classes only    class-level
         Irrelevant classes carried   many (domain padding)          none (thresholded)     eliminated
         Context freed for content             —                      ∼10,500 tokens        reclaimed


removed. Crucially, the smaller block is not a truncation of the larger one: the ∼700 retained
tokens are precisely the classes the content embeds closest to, whereas the ∼11,200-token slice was
dominated by domain-mates that happened to be bundled together.

4.1     Retrieval refinements: closing four precision gaps

The mechanism of Fig. 2 retrieves the right neighbourhood of the ontology, but operational evaluation
on intelligence-domain documents exposed five systematic precision gaps: cases where a class or
predicate that should have been injected fell out of the catalog, or where the injected classes were
correct but insufficiently specific. Each gap traces to one design decision in the baseline retriever,
and each admits a targeted refinement (Table 3). Fig. 3 shows the refined pipeline with the five
refinements marked in place.


G1: Term vectors alongside content vectors. A 1,500-character window such as “The SSP
directed the 12th Battalion along the LoC during Operation Vijay . . . ” embeds into an average
over narrative prose, while the ontology label Military Formation (definition: “a body of troops
organised for military purposes”) has a clean, focused vector. The two are about the same things, yet
the prose centroid sits measurably farther from the label than it should, and borderline classes slip
under the cosine floor. The refinement extracts the window’s proper-noun phrases, abbreviations,
and domain-adjacent terms into a compact pipe-delimited string (“12th Battalion | Operation
Vijay | SSP | LoC”), embeds that string as a second query vector, and scores every candidate
class against both vectors, retaining the maximum:
                                                                             
                      score(𝑐) =            max         cos(𝑞, 𝑐) 1 − 𝜆 pr(𝑐) .
                                       𝑞 ∈ {𝑒 (𝑤), 𝑒(terms(𝑤) ) }

Term vectors match the terse register of ontology labels far more tightly than running prose does.

                                                          9
Table 3: Five precision gaps in the baseline retriever and their refinements.

            Gap in the baseline                      Refinement
   G1       Raw window text embeds to a              Extract proper nouns, abbreviations, and domain
            blurred centroid; cosine distance        terms from each window and embed them as a
            to a sharply defined ontology            second term vector; query with both vectors and
            label is inflated, dropping              keep the best match per class.
            relevant classes below the 0.72
            floor.
   G2       Hierarchy traversal looks only           For every class with adjusted score ≥ 0.80,
            upward (parent fetch); a                 traverse subClassOf one hop downward and
            high-confidence generic parent is        inject the children at score 0.78 (one additional
            injected without its more specific       Cypher call).
            children, so the model emits
            Organization where
            SecurityForce was available.
   G3       Predicates reach the catalog only        Full-text search over ObjectProperty labels and
            through domain/range edges to            definitions (a dedicated Lucene index) using the
            retrieved classes; predicates            key terms extracted in G1, independent of
            lacking those annotations are            domain/range connectivity.
            structurally invisible no matter
            how relevant.
   G4       Windows are cut at fixed                 Split on paragraph boundaries, score each
            character offsets; a cut can split       window by proper-noun density, and embed the
            mid-paragraph, and entity-dense          top windows by density rather than by position.
            sections receive no priority over
            boilerplate.
   G5       The relational route matches a           Walk each retrieved class up its subClassOf
            predicate only against the exact         chain and match predicates whose domain or
            retrieved class labels, but              range is the class or any ancestor, ordered by
            predicates are anchored on               hop distance so the closest-anchored predicates
            generic parents (subordinate to          win the token budget.
            on Military Formation) while
            retrieval returns specific
            subclasses (Northern Light
            Infantry), so the relevant
            predicate never matches.


G2: Subclass expansion. Vector retrieval rewards the classes whose definitions resemble the
content, which systematically favours well-described general classes. If Organization retrieves
at 0.85, the baseline injects it, and only it, so the model, steered by the catalog, dutifully emits
Organization even when SecurityForce or TerroristGroup is the correct, more informative
type. The refinement treats a high-confidence match as evidence that its children are worth showing:
for every class with adjusted score ≥ 0.80, one Cypher hop down the subClassOf hierarchy injects
the direct children at a score of 0.78 (just above the floor, below their parent). The model now sees
the specific options alongside the general one and can choose the tighter fit.


G3: Predicate full-text search. The baseline reaches predicates only relationally: a predicate
enters the catalog if its declared domain or range points at a retrieved class. Predicates
without domain/range annotations (common among upper-ontology imports) can never be retrieved,
regardless of how plainly the content calls for them. The refinement adds a second, content-driven
route: a full-text index over ObjectProperty labels and definitions is queried with the key terms
from G1, so a document about command relationships surfaces controls, mediates-access-to,
and operates even when their schema annotations are absent. The route is additive and non-fatal:


                                                       10
if the index is missing, retrieval proceeds on the relational route alone.


G4: Density-ranked windows. Fixed offsets at characters 0, 1200, 2400, 3600 ignore both
paragraph structure and information density: a window boundary can bisect a sentence, and the
four windows selected may be summary boilerplate while the entity-rich passage at character 5,000
is never embedded. The refinement splits on paragraph boundaries, packs paragraphs greedily up to
the window size, and scores each window by proper-noun density
                                    |propnoun chars(𝑤)| + 6 · |domain hits(𝑤)|
                        𝑑 (𝑤) =                                                ,
                                                       |𝑤|
embedding the top windows by density instead of by position. Entity-dense sections, the ones that
actually determine which ontology classes matter, always enter the embedding queue first.


G5: Subclass-aware predicate matching. G3 opens a content-driven route to predicates, but
the original relational route stays brittle for a subtler reason: it matches a predicate only when
its declared domain or range is one of the exact retrieved class labels. Predicates, however, are
almost always anchored on a generic parent (subordinate to declares its domain and range as
Military Formation), whereas retrieval (sharpened by G1, G2, G4) returns the specific subclasses
the document names, such as Force Command Northern Areas and Northern Light Infantry.
The exact-label test never intersects, so the single most relevant predicate for a military command
document silently falls out, and the model, handed no canonical hierarchy predicate, fabricates its
own (SUPERIOR_COMMANDER_OF, COMMANDED_SECTOR). The refinement walks each retrieved class
up its subClassOf chain and matches predicates whose domain or range is the class or any ancestor,
ordering candidates by hop distance so the closest-anchored (most specific) predicates win the token
budget. It is the predicate-side analogue of G2: where G2 expands classes one hop downward, G5
matches predicates against the retrieved class’s upward ancestor chain.


Measured Effect. The refinements change which classes reach the prompt, and the change is visible
immediately on real documents. On a document describing intelligence-service support to a militant
organisation, the baseline’s strongest retrieval was the generic Organization at 0.74; the refined
retriever surfaces the named, specific classes the document is actually about (Table 4), and the
predicate route recovers relationship vocabulary (controls, mediates-access-to, operates)
that the domain/range route alone never produced. The specific classes matter downstream: an
extraction steered by Inter-Services Intelligence and Military Formation emits those types,
where the baseline catalog would have flattened both to Organization.
The predicate side shows the sharpest gain. On a passage describing the Force Command Northern
Areas (FCNA) command of Northern Light Infantry battalions, the baseline retrieved only three
predicates, all tangential (assigned to command, has joint operational area); the subclass-aware
route (G5) lifts this to 68, surfacing the entire hierarchy family the document actually needs
(subordinate to, commands, part of, reports to, under command), as Table 5 reports. With
those predicates in the catalog the extractor emits canonical relationship types instead of fabricating
labels such as SUPERIOR_COMMANDER_OF or COMMANDED_SECTOR, recovering canonical relationship
vocabulary at the source rather than repairing it downstream.

Table 4: Top retrieved classes for a representative intelligence document, before and after the refinements.

                        Baseline retriever                 Refined retriever
                     Class              Score     Class                             Score
                     Organization       0.74      Inter-Services Intelligence       0.806
                     Location           0.73      Operation Badr                    0.801
                     Person             0.72      12 Northern Light Infantry        0.782
                     —                   —        Military Formation                0.780
                     —                   —        Security Force (via G2)           0.78



                                                      11
                                 Document chunk (content sample)



        G4
                     Paragraph-aware windows, ranked by proper-noun density
                             top windows by 𝑑 (𝑤) , not by character position



                       Window vector                                Term vector             G1
                    𝑒 (𝑤) : prose embedding              𝑒( 12th Bn | Op Vijay | SSP )



                                                                                                    Neo4j
                          Vector query: both vectors, best match per class                         ontology
                     PageRank penalty + 0.72 floor + token budget (baseline, retained)              graph



        G2
                  Subclass expansion: children of classes ≥ 0.80 injected at 0.78
                                       one subClassOf hop downward



        G3
                Predicate recovery: subclass-aware domain/range + full-text search          G5
                 anchors on ancestors of retrieved classes (G5) ∪ key terms → Lucene (G3)



                 Refined ontology catalog (specific classes + recovered predicates)



                  Injected into extraction prompt → ontology-aligned extraction


Fig. 3: The refined retrieval pipeline. The five refinements (red badges) slot into the baseline of Fig. 2 without
altering its architecture: G4 re-orders what gets embedded, G1 adds a second query vector per window, G2
widens class coverage downward from high-confidence matches, and G3 and G5 widen the two predicate
routes: G3 opens a content-driven full-text route, while G5 makes the relational route subclass-aware so
predicates anchored on generic ancestors still reach the catalog. All five are additive: disabling any refinement
degrades precision, never availability.




Table 5: Predicate retrieval on a military command passage (Force Command Northern Areas commanding
the Northern Light Infantry), before and after the subclass-aware route (G5). The baseline’s exact-label match
returns three tangential predicates; G5 surfaces the canonical hierarchy family the document needs.

    Metric                         Baseline (exact-label)                       Refined (subclass-aware, G5)
    Predicates retrieved           3                                            68
    What surfaced                  assigned to command,                         subordinate to, commands, part
                                   assigned to air force                        of, reports to, under command,
                                   command, has joint                           has subordinate formation,
                                   operational area (all                        commanded by, deployed under
                                   tangential)                                  command of, . . .
    Hierarchy family               none                                         complete
    present




                                                               12
4.2     From retrieval to canonical relationships: prompt guards and finalization conformance

The retrieval refinements of Section 4.1 put the right ontology classes and predicates in front of the
model, but a 9B local model is not bound by what it is shown: it still over-emits relationships,
mislabels predicates, and mis-orients them. Three deterministic, ontology-grounded guards
downstream of retrieval close that gap (one at the prompt, two at finalization), so emitted relationships
conform to the schema regardless of the model’s discipline. They are the relationship-side analogue
of the entity canonical_iri mapping (which the tagger applies to entity types but not to predicates),
and they compose as defense in depth: retrieval steers, the prompt restrains, finalization enforces.


Over-extraction: the fan-out guard. Asked to “find ALL relationships,” the model templates a
pattern across every plausible entity pair. On an intelligence document about disputed territory it
emitted a perfect 2 × 58 Cartesian grid (each of two armies “claiming” every one of 58 places),
116 edges (45% of the document) from only two distinct sources, all sharing a single predicate
and pointing in the inverted direction. The driver was the prompt itself: a licence to extract
“ANY . . . strongly implied connection” together with a fan-out guard scoped only to reporting verbs.
Two minimal edits (replacing “strongly implied” with “explicitly stated in the text” and generalising
the fan-out guard to any relation type with an explicit no-grid clause) collapsed it (Table 6). This
is a prompt-level guard: cheap, but probabilistic. On a small model it sharply reduces rather than
provably eliminates the pattern, which is why the finalization guards below do not depend on it.

Table 6: Relationship over-extraction on a disputed-territory document, before and after the prompt fan-out
guard.

                         Metric                                    Before     After
                         CLAIMED_BY edges (a 2 × 58 grid)              116        1
                         Total relationships                           258      112
                         Most-concentrated predicate share            45%      16%
                         Distinct predicate types                       63       29



Direction: rank-guarded orientation. Asymmetric hierarchy predicates (subordinate to, part
of, commands) carry a fixed semantic direction, but the model orders source/target inconsistently:
the same corpus yielded both “NLI subordinate to FCNA” (correct) and “FCNA subordinate
to NLI” (inverted), plus the inverse predicate has subordinate formation pointing the wrong
way. Because no pipeline stage ever swaps endpoints, a reversed edge is the model’s error, faithfully
preserved into the graph and then narrated back by the chatbot as a contradiction. The guard
canonicalises the predicate label (folding inverse forms such as has subordinate formation and
commands into the upward subordinate to with endpoints swapped) and then re-orients by ontology
rank: for an upward predicate the source must be the junior formation, where rank is a coarse tier read
from the entity name (Command/Corps > Division > Brigade > Battalion/Regiment). Whatever order
the model emits (flipped, inverse, or correct), the edge converges to one canonical form (Table 7).
The guard fires only on organisation↔organisation edges, so person-role edges (commander of)
are left untouched.
Table 7: Rank-guarded direction normalization: every phrasing of the FCNA/NLI command hierarchy
converges to one canonical edge.

      Model emits                                           After conformance
      FCNA -[subordinate to]-> NLI (flipped)                NLI -[subordinate to]-> FCNA
      NLI -[has subordinate formation]->                    NLI -[subordinate to]-> FCNA
      FCNA (inverse)
      FCNA -[commands]-> NLI (downward)                     NLI -[subordinate to]-> FCNA
      NLI -[subordinate to]-> FCNA (already right)          NLI -[subordinate to]-> FCNA


                                                     13
Vocabulary: ontology-grounded canonicalization with novel flagging. The tagger maps entity
types to ontology classes but leaves relationship predicates untouched (it only validates their
domain/range), so morphological and lexical variants of one relation proliferate: a single document
carried CAPTURED_LOCATIONS (×14) and CAPTURED_LOCATION (×9) as two distinct edge types,
neither of which the tagger would merge (its label match fails on the plural). The guard
snaps each emitted predicate to the ontology object-property vocabulary (954 label/alt-label
keys loaded once from the ontology graph) by a tiered, meaning-preserving match: exact, then
de-pluralised (CAPTURED_LOCATIONS→CAPTURED_LOCATION), then an embedding cosine against
the ontology’s predicate embeddings. The embedding tier is deliberately conservative: a calibration
showed that below ≈ 0.80 cosine, generic upper-ontology predicates (may-be-detected-by,
attack-may-be-countered-by) act as semantic magnets and produce confident-but-wrong matches,
so the floor is set at 0.80: only near-certain synonyms (observed by→observed-by-at-some-time)
snap, and everything else is left verbatim. Critically, an unmatched predicate is not forced: it is
marked _novel_predicate and the post-ingest validator flags it unknown_predicate for review
in the admin panel, where it can be promoted into the ontology, so the schema grows from real data
instead of the model silently fragmenting it. Running this at extraction, before ingest, means the
relationship-deduplication key (source, target, type) sees canonical types, so the 14 and 9
variants collapse into a single qualifier-merged edge rather than entering the graph as duplicates.

5   Multi-format document handling
The earlier system handled plain text and PDF. The current consumer routes by MIME type and file
extension to format-specific handlers, unifying every format onto the same two-phase extraction and
finalisation backend.


Spreadsheets (XLSX): Plan-Then-Execute. Per-row LLM extraction over a spreadsheet is both
wasteful and inconsistent. Instead, the spreadsheet handler uses a deterministic plan-then-execute
strategy: (1) inspect the workbook to build a bounded sample (header tokens, merged-cell ranges,
∼10 sample rows per sheet); (2) issue a single LLM call that returns a typed ExtractionPlan
listing, per sheet, the entity type, the name-bearing column, a list of ColumnMaps (each with a
value_type ∈ {string, int, float, date}), relationship definitions, and drop-row filters; (3) execute
the plan deterministically over all rows, with numeric coercion, merged-cell propagation, multi-value
splitting, and conditional skipping; and (4) map the resulting records onto Entity/Relationship
objects. A date value_type triggers date parsing and emits coverage warnings for cells that fail to
parse, so silent data loss in date columns becomes a visible, reviewable signal rather than a dropped
field. This yields one LLM call per workbook template instead of one per row, with reproducible
execution.


Office Documents (DOCX, PPTX): Virtual Pages. Word and PowerPoint files are converted into
“virtual pages” so they can reuse the PDF text pipeline unchanged. the Word handler prefers Docling
for layout-aware Markdown (falling back to python-docx), flattens tables to pipe-delimited rows,
and groups content into ∼3,600-character virtual pages. the PowerPoint handler emits one virtual
page per slide: title as a heading, body shapes in spatial reading order, hyperlinks inlined, tables as
pipe-rows, and speaker notes as a separate page. For both, if the extracted text falls below a floor
(∼200 characters, indicating an image-only document) the handler extracts and OCRs embedded
images before chunking. The virtual pages then flow through the same chunked text pipeline as a
born-digital PDF.


PDF and Images. The PDF path (Section 5.1) classifies each page and routes born-digital pages
through layout-aware text extraction and scanned pages through the vision/OCR pipeline; standalone
images go directly to vision. All paths converge on the same finalisation stage, so deduplication, type
normalisation, and ontology grounding apply uniformly regardless of source format. Fig. 4 shows
the routing topology.




                                                  14
                                          Kafka record (MIME type + file extension)




                                                Format router (process_record)




                PDF                            XLSX                       DOCX / PPTX                 Image




         per-page classifier:              plan-then-execute                virtual pages           vision VLM
         text / OCR / mixed              1 LLM call / template           reuse PDF pipeline         transcription




                                 Unified two-phase extraction + ontology grounding + finalisation




                                                Validated JSON knowledge graph


Fig. 4: Multi-format routing. The consumer dispatches each record by MIME type and extension to a
format-specific handler (per-page-classified PDF, plan-then-execute spreadsheets, virtual-page Office
documents, or vision-transcribed images), and every path converges on the same two-phase extraction,
ontology grounding, and finalisation backend, so downstream processing is format-agnostic.


5.1     Per-page OCR classification and PDF routing

A critical limitation of the initial PDF handling strategy was its binary treatment of documents: a
PDF was either routed entirely through text extraction or entirely through OCR/vision processing.
In practice, many real-world PDFs are mixed, containing both born-digital text pages and scanned
or image-heavy pages within the same document. To address this, we implemented a per-page OCR
classification system using PyMuPDF [32] that analyses six structural signals for each page and
routes individual pages to the optimal extraction path.

5.1.1    Per-page OCR classification
Problem. Treating an entire PDF as either text or OCR causes information loss: routing a mixed
PDF entirely through text extraction silently drops scanned pages, while routing it entirely through
OCR wastes compute on born-digital pages and may degrade text extraction quality.


Solution. A six-signal per-page classifier using PyMuPDF’s low-level page analysis API determines
whether each page should be processed via text extraction, OCR/vision, or skipped entirely.
Six structural signals are measured per page (Table 8), and the classification is a priority-ordered
cascade over them: image dominance is checked first, then extractable text, then the vector-text edge
case, with skip as the final default:
                                               
                                               
                                                skip            if 𝐴 𝑝 = 0,
                                               
                                               
                                               
                                                ocr             if 𝐼block > 0.15 ∨ 𝐼xref > 0.15,
                                               
                                                text
                                               
                                                                if 𝐶 > 50,
                                classify( 𝑝) =                                                                      (1)
                                               
                                                ocr             if 𝐷 > 200,
                                               
                                               
                                               
                                               
                                                text            if 𝐶 > 0,
                                                skip
                                               
                                                                 otherwise.
                                               
                                                                   15
Table 8: The six per-page signals and their roles in the cascade of Eq. (1).

        #      Signal      Definition                       Detects                                         Threshold
        1      𝐴𝑝          page area                        degenerate pages                                 =0
        2      𝐼block      image-block area / 𝐴 𝑝           scanned pages                                   > 0.15
        3      𝐼xref       xref-image area / 𝐴 𝑝            images hidden from block analysis               > 0.15
        4      𝐶           extractable characters           born-digital text                            > 50 (or > 0)
        5      𝐷           drawing/path primitives          text drawn as vectors                           > 200
        6      𝑋           xref image count                 gates signal 3’s computation                     >0


            A mixed 10-page PDF under per-page classification:


             text        text       ocr         ocr        text          ocr     text      ocr        skip       text
            𝐶=2840      𝐶=3105    𝐼blk =.91   𝐼blk =.88   𝐶=1990        𝐷=412   𝐶=2470   𝐼xref =.67   𝐶=0       𝐶=3320


              p1          p2         p3          p4         p5           p6       p7        p8         p9         p10


            6 text / 9 usable = 0.67 ⇒ mixed route: text pages → text extraction, ocr pages → vision; merged downstream


Fig. 5: Per-page classification on a mixed document. Each page carries the signal that decided it: born-digital
pages pass on character count, scanned pages trip the image-coverage thresholds, page 6 is the
vector-drawn-text edge case (zero characters, 412 drawing primitives), and the empty page 9 is skipped. The
text-page ratio then routes the document as a whole (ratio rule below), here into the mixed path, where neither
the scanned appendix nor the digital body is lost.



Signal Design Rationale. The six signals were chosen to cover distinct categories of page content:

    • Image block coverage (Signal 2) detects pages dominated by raster images embedded as
      block-level elements, the most common indicator of scanned pages.
    • Xref image coverage (Signal 3) catches images that are referenced via PDF cross-reference
      tables but may not appear as blocks in the structured page dictionary, providing a secondary
      detection mechanism.
    • Character count (Signal 4) identifies born-digital pages with extractable text, using a threshold
      of 50 characters to distinguish meaningful content from stray artefacts.
    • Drawing count (Signal 5) addresses an edge case where text is rendered as vector paths
      rather than font glyphs. Such pages report zero characters but contain hundreds of drawing
      primitives, requiring OCR to recover the text.
    • The 15% coverage threshold for Signals 2 and 3 was empirically determined: pages with small
      logos or decorative images below this threshold still contain predominantly extractable text.

5.1.2   PDF routing logic
After classifying every page, the system computes the ratio of text pages to usable (non-skip) pages
and routes the entire document through one of three extraction paths:

                                             
                                             
                                             
                                              Text  if || {{ 𝑝𝑝 || 𝑝≠skip}
                                                                    𝑝=text} |
                                                                            | ≥ 0.80
                                             
                                             
                                             
                                   Route(𝑃) = OCR    if || {{ 𝑝𝑝 || 𝑝≠skip}
                                                                    𝑝=text} |
                                                                            | ≤ 0.20
                                                                                                                          (2)
                                             
                                             
                                             
                                             
                                              Mixed otherwise
                                             

    • Text path (≥80% text pages): Extracts text from all pages using pypdf and processes via the
      existing chunked text extraction pipeline.

                                                                   16
      • OCR path (≤20% text pages): Routes the entire PDF through vision-based extraction. When
        LLM_PROVIDER=local, pages are rendered as images and sent to the local VLM; when using
        Gemini, the Gemini File API handles native PDF processing.
      • Mixed path (20–80% text pages): Routes text pages and OCR pages through their respective
        extraction pipelines independently, then merges results using the existing cross-chunk merge
        infrastructure (Stage 3).

5.1.3    Mixed PDF extraction
The mixed PDF extraction function partitions pages by their classification and processes each group
through the appropriate pipeline:

    1. Text pages: Non-text page slots are blanked out in the page text array, and the remaining text
       is processed through the standard chunked text extraction pipeline.
    2. OCR pages: Only the OCR-classified page indices are sent to the vision extraction pipeline,
       avoiding unnecessary processing of born-digital pages.
    3. Skip pages: Ignored entirely; no extraction is attempted on empty or zero-area pages.
    4. Merge: Partial results from both paths are merged using _merge_chunk_results(),
       followed by a relationship second pass and consistent ID reassignment (Stages 3–4).

When all extraction paths fail (e.g., due to corrupted pages), the system returns an empty but valid
ExtractionResult rather than raising an exception, ensuring downstream pipeline stability.


Impact. Mixed PDF support eliminates the information loss caused by binary routing. For a
45-page document with 30 text pages and 15 scanned pages, the previous approach would either
miss all scanned content (text path) or wastefully OCR all 30 born-digital pages (OCR path). The
per-page classifier processes each page optimally.

6     Deduplication and entity resolution
This section presents the deduplication subsystem: the output schema that carries deduplication
evidence, six zero-inference rule-based algorithms, their orchestration as a guarded composition,
and the complementary embedding-based resolution layer.

6.1     Deduplication-aware output schema

The output schema evolved from a minimal entity–relationship container into a deduplication-aware
data model. The legacy schema carried a single alias per entity and a bare disambiguation fingerprint;
it had no way to record where an alias came from, which contextual evidence distinguishes two
same-named people, or why two entities might be the same. The revised schema introduces three
dedicated record types (ContextAttribute, AliasOccurrence, and PossibleDuplicate) and
threads them through the existing classes, drawing on entity-resolution design patterns described
in [7]. Fig. 6 contrasts the two generations; shaded fields and cards mark what the deduplication
upgrade added.


Schema Improvements. Fig. 6 carries most of the story: entities now hold five-plus
aliases with per-alias provenance (AliasOccurrence: discovery source, occurrence count,
confidence), disambiguation records track contextual attributes (role, organisation, location [29])
and scored duplicate flags with actionable merge recommendations, and every result exports
dedup_candidates for automated processing or human review. One addition is not visible in
the figure: a coverage_warnings list records soft quality signals raised during extraction, such as a
document yielding many entities but disproportionately few relationships (Section 7.3) or spreadsheet


                                                 17
           Legacy schema                                     Enhanced schema
                                                                                                      New record types
                                                   Entity
 Entity
                                                   id, type, name                            ContextAttribute
 id, type, name
                                                   aliases                    5+ variants    type                  role/org/location
 aliases                       1 entry
                                                   name_variants[]    provenance per alias   value, confidence
 disambiguation, properties               dedup    disambiguation, properties                source_text
 confidence, provenance                  upgrade   confidence, provenance

                                                                                             AliasOccurrence
 Disambiguation
                                                   Disambiguation                            alias, count
 fingerprint
                                                   fingerprint, key_attributes               confidence, source
 key_attributes
                                                   context_attributes[]                      context_snippets[]
                                                   possible_duplicates[]
                                                   dedup_status
 ExtractionResult
                                                                                             PossibleDuplicate
 object_id
                                                                                             entity_id, similarity_score
 entities[], relationships[]                       ExtractionResult                          similarity_reason
                                                   object_id                                 context_match, suggested_action
                                                   entities[], relationships[]
                                                   dedup_candidates[]



Fig. 6: Schema evolution. The legacy schema (left) carried one alias per entity and a bare disambiguation
fingerprint. The enhanced schema (centre) expands aliases to five-plus variants with per-alias provenance,
threads contextual evidence and duplicate flags through Disambiguation, and exports dedup_candidates on
every result. Three new record types (right, green) carry the deduplication evidence: which context
distinguishes same-named entities, where each alias was discovered, and why a pair is a merge candidate.
Relationship and Provenance are unchanged.


date cells that failed to parse (Section 5), so downstream consumers see where extraction may be
incomplete rather than discovering it silently.
In the refactored codebase these models live in schemas/extraction.py and
schemas/disambiguation.py rather than in a single str_op_schema.py file; the properties
and qualifiers fields are given explicit dictionary type aliases, and per-alias provenance is
captured by an AliasOccurrence record (alias, discovery source, count, and confidence) on each
entity’s name_variants list.

6.2     Core deduplication algorithms

This section details the six novel algorithms constituting the entity deduplication pipeline. Each is
designed to address specific classes of name variation without necessitating further LLM inference
calls. Unlike deep learning approaches to entity matching [21, 22] which require labeled training
data, our algorithms operate deterministically with zero additional inference cost.

6.2.1    Algorithmic alias expansion
Problem. An entity extracted as “John Doe” limits search retrievability if users query variants
like “J. Doe” or “JD.” As demonstrated by Christen [23], personal name abbreviation patterns are a
leading cause of missed matches in record linkage.


Formulation. Let a person’s name 𝑁 be an ordered sequence of tokens 𝑊 = (𝑤 1 , 𝑤 2 , . . . , 𝑤 𝑘 ).
We define a transformation set F of abbreviative permutations, applied only when 𝑇 = Person and
𝑘 ≥ 2; the expanded alias set is
 𝐴 = {𝑁 } ∪ { 𝑓 (𝑊) | 𝑓 ∈ F },              F = { 𝑤 1 [0]. 𝑤 𝑘 , 𝑤 1 𝑤 𝑘 [0]., 𝑤 1 [0]𝑤 𝑘 [0], 𝑤 1 [0].𝑤 𝑘 [0]. }. (3)

Every transformation is deterministic, so the expansion is repeatable, auditable, and incurs zero LLM
cost. Fig. 7 shows the full expansion radiating from a single extracted name; each spoke is annotated
with the transformation that produced it.


Impact.       Expands search coverage deterministically with zero false positives and zero LLM cost.




                                                               18
                                                           Jon Doe

              J. Doe                                                 text mining (§6.2)                       John D.
                                      𝑤1 [                                                     0].
                                                                                          𝑤𝑘 [
                                             0].
                                                   𝑤𝑘
                                                                                     𝑤1


                                                               John
                                                               Doe
                                                                                     𝑤1 [
                                              [0]                                           0 ] .𝑤
                                      0] 𝑤𝑘                                                      𝑘 [0
                               𝑤1 [                                                                     ].


                 JD                                                                                             J.D.


               green spokes: deterministic F transformations    dashed: variants recovered later from the source text


Fig. 7: Algorithmic alias expansion. A single extracted name deterministically radiates to its abbreviative
variants; each spoke carries the transformation that generated it. The dashed spoke shows where source-text
mining (Fig. 8) later adds genuine spelling variants the transformations cannot predict.


6.2.2   PDF text mining with fuzzy matching
Problem. Source documents often contain unextracted spelling variations (e.g., “Jon Doe” when
“John Doe” was extracted) or shorthand references.


Mathematical Formulation. We employ the Ratcliff/Obershelp similarity metric [9], as
implemented by Python’s difflib.SequenceMatcher:
                                                                      2·𝑀
                                                        𝑆(𝑥, 𝑦) =                                                          (4)
                                                                       𝑇
where 𝑀 is the number of matching characters and 𝑇 is the total number of characters in both strings.
This metric was selected based on comparative evaluations of string distance functions for name
matching tasks [24]. A word 𝑤 from the document text 𝐷 is considered a spelling variant of entity
token 𝑣 if:
                                𝑆(𝑤, 𝑣) ≥ 𝜏, where 𝜏 = 0.85                                       (5)

The miner slides over consecutive word pairs (word𝑖 , word𝑖+1 ) of the document and tests each pair
against the extracted name’s first and last tokens (𝑤 first , 𝑤 last ). Two acceptance rules fire (Table 9);
every accepted pair joins the variant dictionary 𝑉 [𝑒.id]. Fig. 8 shows both rules firing on a real
passage.

Table 9: Acceptance rules of the source-text variant miner (𝜏 = 0.85).

           Variant class              Acceptance condition                                                   Example hit
           Initial reference          word𝑖 \“.” = 𝑤 first [0] ∧ word𝑖+1 ⊒ 𝑤 last [:3]                       “J. Doe”
           Spelling variant           𝑆(word𝑖 , 𝑤 first ) ≥ 𝜏 ∧ word𝑖+1 ⊒ 𝑤 last [:3]                        “Jon Doe”



Impact. Discovers 85–90% of spelling variations present in the source text, balancing precision
(via the 0.85 threshold) with recall.

6.2.3   Linguistic-aware name similarity scoring
Problem. Standard string similarity metrics fail on three categories of name variation common
in intelligence documents: (1) Slavic gender suffixes (“Petrov” / “Petrova”), (2) spelling and

                                                                19
   Document text 𝐷
   . . . the shipment was authorised by J. Doe on 14 June. Customs records list Jon Doe as the
   consignee of record, while internal memos refer only to the procurement office. . .

                                   pairwise scan (word𝑖 , word𝑖+1 ) against (𝑤first , 𝑤last )

             𝑉 [per_001] = {                                                 extracted entity
                J. Doeinitial reference                                   John Doe (𝑤first , 𝑤last )
                Jon Doe𝑆 = 0.86 ≥ 𝜏 }

Fig. 8: Source-text variant mining in action. The miner scans the raw document for word pairs matching the
extracted name under the two rules of Table 9: an initial-style reference (blue) and a fuzzy spelling variant
(orange, Ratcliff/Obershelp 𝑆 = 0.86). Both land in the entity’s variant dictionary with their provenance.


transliteration variants (“John” / “Jon” / “Jhon”), and (3) genuine abbreviations versus coincidental
first-letter matches. As noted by Navarro [25], approximate string matching algorithms are inherently
language-agnostic without explicit morphological augmentation. Cross-lingual name matching
research [10, 28] has demonstrated that morphological normalisation significantly improves recall
for inflected name forms.


Mathematical Formulation. Rather than a priority-ordered tier model, the implementation uses
a five-signal weighted composite over independent similarity dimensions, each capturing a distinct
aspect of name variation:
                              ∑︁
           Sim(𝑛1 , 𝑛2 ) =          𝑤 𝑘 · 𝜎𝑘 (𝑛1 , 𝑛2 ),           w = (0.30, 0.25, 0.20, 0.15, 0.10),      (6)
                               𝑘

where the five signals 𝜎𝑘 are:

   1. Jaro–Winkler (𝑤 = 0.30): prefix-weighted edit distance, excelling at short-string typos and
      transpositions (“Petrov” / “Petref”).
   2. Double Metaphone (𝑤 = 0.25): phonetic code agreement, covering transliteration families:
      “John”, “Jon”, and “Jhon” all share the phonetic code JN and score 1.0.
   3. Token overlap (𝑤 = 0.20): word-level Jaccard similarity |𝑇1 ∩𝑇2 |/|𝑇1 ∪𝑇2 |, robust to reordered
      tokens and honorific prefixes.
   4. Abbreviation confidence (𝑤 = 0.15): confidence that one name is a genuine abbreviation of
      the other (| 𝑝| = 1 ∧ 𝑝 = 𝑞 1 for at least one part-pair); this is the corrected single-letter test of
      Section 7.3.7.
   5. Cultural-variant score (𝑤 = 0.10): matches Slavic gender suffixes (“-ov”/“-ova”,
      “-ev”/“-eva”) and hard-coded transliteration families.

A strong-signal boost prevents weak signals from dragging down a confident match: if max 𝑘 𝜎𝑘 ≥
0.90 and the composite falls below 80% of that maximum, the composite is lifted to 0.8 max 𝑘 𝜎𝑘 .
The scorer returns not only a score but the primary reason and the full per-signal breakdown, so every
match is auditable: a hit can be attributed to a strong phonetic signal with moderate edit-distance
support rather than reported as a single opaque number. The signal weights are configuration
constants, leaving a path to learned weights once labelled match data are available. Fig. 9 illustrates
the signal computation and composite for a representative pair.




                                                              20
                            Per-signal breakdown: “John Doe” vs. “Jon Doe”


Jaro-Winkler (𝑤 =0.30)   Double Metaphone (𝑤 =0.25)    Token overlap (𝑤 =0.20)   Abbreviation (𝑤 =0.15)       Cultural (𝑤 =0.10)
        0.956                      1.000                       0.800                    0.000                      1.000


                                      Composite score: 0.924      reason: phonetic_strong


                         strong-signal boost: max 𝑘 𝜎𝑘 = 1.0 ≥ 0.90, composite 0.87 ≥ 0.80, no boost needed
                                   exported as NameMatchResult(0.924, "phonetic_strong", signals)


Fig. 9: Five-signal composite scoring for “John Doe” vs. “Jon Doe”. The Double Metaphone and
cultural-variant signals both score 1.0 (same phonetic code, same transliteration family); Jaro-Winkler scores
0.956; token overlap 0.80 (partial word match on first token). The weighted composite is 0.924, labelled
phonetic_strong. The per-signal breakdown travels with the result, making every match auditable
downstream.


Impact. The weighted composite captures all three categories of name variation simultaneously
rather than committing to a single signal. The per-signal breakdown enables interpretable matching:
analysts can see why two names were linked (transliteration family, phonetic code, token overlap)
rather than trusting an opaque score. The corrected abbreviation signal (Section 7.3.7) ensures
coincidental initial matches score near-zero on that signal, so they cannot boost the composite above
the merge threshold. The configurable weights leave an upgrade path to ML-learned values once
labelled match data are available.

6.2.4    Context-aware duplicate detection
Problem. Entities with high name similarity (e.g., “Elena Petrov” and “Elena Petrova”) may
represent different individuals if their contextual attributes (roles, organizations, locations) diverge.
Relying solely on name similarity leads to false merges. This challenge is well-documented in the
entity disambiguation literature [29, 30], where contextual features are essential for distinguishing
co-referent from non-co-referent mentions.


Mathematical Formulation. Let an entity 𝑒 be associated with a contextual attribute set 𝐶𝑒 =
{role, org, loc}. We define a contextual agreement function:
                                       
                                         1 if all non-null shared attributes match
                       Δ(𝑒 1 , 𝑒 2 ) =                                                    (7)
                                         0 if any non-null attribute conflicts

A merge candidate is valid if and only if:

                               Sim(𝑒 1 .name, 𝑒 2 .name) ≥ 0.75 ∧ Δ(𝑒 1 , 𝑒 2 ) = 1                                           (8)

Candidate pairs (same type, Sim ≥ 0.75) are placed on two axes, name similarity and contextual
agreement Δ, and the cell they land in is the decision. Fig. 10 shows the decision surface with the
canonical false-merge example pinned where context vetoes a high name score.


Impact. Essential for preventing false positives. Context validation ensures that entities with
similar names but disparate contexts are accurately identified as distinct entities.

6.2.5    Relationship deduplication
Problem. Multi-phase extraction can yield duplicate relationships with varying levels of detail
(e.g., one extraction includes a date qualifier, another does not), artificially inflating edge counts and
fragmenting contextual data.


                                                             21
                             context agrees Δ = 1                         context conflicts Δ = 0


                                 auto_merge                                 different_contexts
         Sim > 0.95
                                 confidence: high                                 kept distinct



                               manual_review                                different_contexts
  0.90 < Sim ≤ 0.95
                                confidence: medium                                kept distinct



                              different_contexts                            different_contexts
  0.75 ≤ Sim ≤ 0.90
                                  low similarity                                  kept distinct




                                                    Pinned example:   Elena Petrov (combustion scientist, Khamsin Institute)
                                                                      Elena Petrova (malware analyst, Vektor Signal)
                                                    Sim = 0.85 (gender suffix), but role conflict ⇒ Δ = 0 ⇒ kept distinct


Fig. 10: The context-validated decision surface. Name similarity alone never merges: only the top-left cell
(very high similarity and full contextual agreement on role/organisation/location) auto-merges, the band below
it goes to human review, and any contextual conflict forces the pair into the distinct column regardless of how
alike the names are. The pinned pair shows the false merge this design prevents.


Mathematical Formulation. Let a relationship be a tuple 𝑟 = (𝑢, 𝑣, 𝑡, 𝑄), where 𝑢, 𝑣 are nodes,
𝑡 is the edge type, and 𝑄 is a dictionary of qualifiers. If two relationships 𝑟 1 and 𝑟 2 share the same
identity key 𝐾 = (𝑢, 𝑣, 𝑡), we merge them to maximize the qualifier set:

                                                   𝑄 merged = 𝑄 1 ∪ 𝑄 2                                                        (9)

Operationally, relationships sharing a key collapse under a richness-preserving fold: the retained
record is the one with the larger qualifier set, and ties merge their qualifiers,
                      
                      
                       𝑟                                                          if |𝑄 𝑟 | > |𝑄 Seen[𝐾 ] |,
                      
                      
            Seen[𝐾] ← Seen[𝐾] with 𝑄 ← 𝑄 Seen[𝐾 ] ∪ 𝑄 𝑟                            if |𝑄 𝑟 | = |𝑄 Seen[𝐾 ] | > 0,
                      
                      
                       Seen[𝐾]                                                    otherwise.
                      
Fig. 11 traces three extractions of the same real-world edge collapsing into one fully qualified record.

      (per_001, org_001, EMPLOYED_BY)                                                 same key 𝐾 = (𝑢, 𝑣, 𝑡 )
      Q = {}                         chunk 2                                         ⇒ qualifier-preserving fold


                                                                       (per_001, org_001, EMPLOYED_BY)
      (per_001, org_001, EMPLOYED_BY)
                                                                       Q = {date: 2024-06-15,
      Q = {date: 2024-06-15}         chunk 4
                                                                            location: London HQ}


      (per_001, org_001, EMPLOYED_BY)                                                1 edge out, 0 qualifiers lost
      Q = {location: London HQ}     2nd pass


Fig. 11: Qualifier-preserving relationship deduplication. Three extractions of the same edge (bare, dated, and
located) share the identity key (𝑢, 𝑣, 𝑡) and fold into a single record carrying the union of their qualifiers. Naive
key-based deduplication would have kept whichever arrived first and silently discarded the date or the location.



Impact. Treats temporal and contextual metadata as primary attributes, preventing information
loss during the deduplication process.


                                                              22
6.2.6      Sequence-ordered parallel processing with mutex-protected output
Problem. Parallel document processing can lead to interleaved and garbled JSON output in the
terminal if a worker completes a shorter document while another worker is mid-output on a larger
document.


Solution. Employs a mutex lock to ensure atomic printing and a sequence-ordered buffering
mechanism to emit outputs strictly in their original submission order.
Each submitted document carries a sequence number; completions land in a hash-map buffer, and a
single drain loop releases result 𝑛+1 only after result 𝑛 has been printed (under a mutex, so no two
workers interleave bytes). The invariant is simple: output order = submission order, regardless of
completion order. Fig. 12 shows the mechanism on a real out-of-order completion pattern.

                                                                                                              𝑡

      W1                   doc #1 (45 pp)


      W2          doc #2             doc #4


      W3               doc #3



buffer                     2          3       4        results 2–4 wait: next_seq = 1 not yet complete


                                                                                drain loop releases 1→2→3→4
stdout                                             1        2   3      4
                                                                                under one mutex


Fig. 12: Sequence-ordered output under parallel processing. Three workers finish out of order: the short
documents #2–#4 complete while the 45-page document #1 is still extracting, but their results park in the
sequence-keyed buffer. The moment #1 lands, the drain loop emits 1→2→3→4 atomically. Operators see
coherent, submission-ordered output; throughput keeps the full benefit of parallelism.



Impact. Enables significant performance gains via parallel processing while maintaining the
operational requirement of coherent, sequential terminal output.

6.3     Post-extraction enhancement pipeline

The aforementioned algorithms are integrated into a Phase 3 pipeline that executes automatically
following relationship extraction.      Formally, the enhancement is a composition of three
transformations applied to the extraction result 𝑅 = (𝐸, 𝜌) with entity set 𝐸 and relationship set 𝜌,
given the raw source text 𝑆:
                                     𝑅 ′ = D ◦ M 𝑆 ◦ A (𝑅),
                                                          

where A (alias expansion) replaces each person entity’s alias set 𝑎(𝑒) by 𝑎(𝑒) ∪ expand(name(𝑒));
M 𝑆 (text mining) further unions in the spelling variants mine𝑆 (𝑒) recovered from 𝑆 by fuzzy
matching; and D (duplicate detection) leaves entities unchanged but populates the result’s candidate
list with scored pairs {(𝑒 𝑖 , 𝑒 𝑗 , 𝑠𝑖 𝑗 , action𝑖 𝑗 )}. Each stage is guarded: A applies only to Person
entities, M 𝑆 is skipped when no source text accompanies the record, and the whole composition is
the identity on an empty entity set, so the pipeline degrades gracefully rather than failing. Fig. 13
shows the orchestration.




                                                       23
                                 ExtractionResult 𝑅 = (𝐸, 𝜌) + source text 𝑆


                                                                             no       return 𝑅
                                                            𝐸 ≠ ∅?
                                                                                     unchanged
                                                            yes

                                       A: Algorithmic alias expansion Fig. 7
                                Person entities only: 𝑎 (𝑒) ← 𝑎 (𝑒) ∪ expand(name(𝑒) )



                                        M 𝑆 : Source-text variant mining Fig. 8
                                      skipped if 𝑆 = ∅: 𝑎 (𝑒) ← 𝑎 (𝑒) ∪ mine𝑆 (𝑒)



                                  D: Context-aware duplicate detection Figs. 9, 10
                                scored pairs (𝑒𝑖 , 𝑒 𝑗 , 𝑠𝑖 𝑗 , action𝑖 𝑗 ) with context validation




                                    𝑅 ′ : enriched aliases + dedup_candidates


Fig. 13: Phase 3 orchestration as a guarded composition D ◦ M 𝑆 ◦ A. Alias expansion and text mining enrich
entity aliases in place; duplicate detection appends scored merge candidates. Every stage is conditional, so
missing inputs degrade the pipeline to a no-op rather than an error.


6.4   Algorithm summary

Table 10: Summary of Core Procedures

          #   Algorithm                                   Innovation                                  Value
          1   Algorithmic Alias Expansion                 Deterministic abbreviation generation       Coverage
          2   PDF Text Mining (Fuzzy Matching)            SequenceMatcher + word pairing              Discovery
          3   Linguistic-Aware Similarity Scoring         5-signal composite, cultural variants       Highly novel
          4   Context-Aware Duplicate Detection           Role/org/location conflict validation       Precision
          5   Relationship Deduplication                  Qualifier-aware merging                     Data integrity
          6   Sequence-Ordered Parallel Output            Mutex + buffering for consistency           Operational
          7   Per-Page OCR Classification                 6-signal PyMuPDF page classifier            Routing



Key Contributions. This implementation advances knowledge graph extraction through the
integration of domain-specific linguistic pattern recognition (e.g., Slavic suffixes), multi-source alias
discovery, robust context-aware deduplication, and intelligent per-page PDF routing via a six-signal
OCR classifier (Fig. 5). By prioritizing relationship metadata and executing these enhancements
without incurring additional LLM inference costs, the system raises search recall from roughly 70%
to 95% while preventing false merges. The per-page OCR classification eliminates information loss
from binary PDF routing, and the configurable LLM provider switching enables seamless transitions
between local and cloud models. The empirical quality analysis (Section 7.3) and issues catalogue
(Section C) further demonstrate the necessity of a defense-in-depth approach combining upstream
data cleaning, intelligent document routing, and downstream entity enrichment.

6.5   Embedding-based entity resolution

Motivation. The six rule-based algorithms of Section 6.2 resolve name variation deterministically
and at zero LLM cost, but they reason primarily over surface strings and a few context fields.
They do not capture semantic similarity between mentions whose surface forms diverge yet whose
surrounding descriptions agree, and their pairwise comparison is quadratic in the number of entities.
We therefore add a complementary embedding-based resolution subsystem (resolution/) that
follows the canonical blocking–matching pipeline of the entity-resolution literature [7, 8] and the

                                                               24
learned-matching tradition of Magellan/DeepMatcher and transformer-based matchers [21, 22]. It
runs as an optional post-extraction stage and is disabled by a single configuration flag when not
required.


Pipeline.   The resolution engine executes five stages (embed, block, score, decide, collect):

   1. Embed. Each entity is rendered to a short descriptive string (name, type, salient
      properties, aliases) and embedded.       For within-document resolution a deterministic
      hash-seeded pseudo-embedder is used (no API calls); for cross-document resolution the
      ontology-tuned embedding model Konect-U/Qwen3-Embedding-0.6B-Ontology, served
      behind a swappable provider interface (vLLM, a text-embedding-inference server, or Gemini),
      supplies real semantic vectors.
   2. Block. To avoid the 𝑂 (𝑛2 ) all-pairs comparison, candidate pairs are generated by the union
      of two blocking strategies [8]: a FAISS [33] inner-product index over ℓ2 -normalised vectors
      (cosine top-𝑘, 𝑘 = 20), and a phonetic block that groups entities sharing a Double Metaphone
      [27] fingerprint. The union recovers both semantically and orthographically near pairs.
   3. Score. Each candidate pair receives a weighted multi-signal score combining name similarity
      (0.25), embedding cosine (0.20), property overlap (0.15), phonetic match (0.10), type
      compatibility (0.10), alias cross-match (0.10), and source proximity (0.10). Property conflicts
      are penalised at twice the weight of property agreements, and type compatibility recognises
      synonym families (person/individual/officer, organization/agency, location/place).
   4. Decide. A decision engine maps the score to an action under tunable thresholds: ≥
      0.85 ⇒ auto-merge; 0.60–0.85 ⇒ manual-review; ≥ 0.50 with a codename pattern ⇒
      codename-candidate; otherwise distinct. Crucially, a hard-conflict guard overrides any
      score: if two entities carry differing values on a discriminator key (date of birth, nationality,
      gender, passport or employee number) they are never merged, however similar their names,
      which directly prevents the “Elena Petrov vs. Elena Petrova” class of false merge.
   5. Collect. The stage returns merged entities, a canonical-ID mapping, per-decision provenance
      records, and the items flagged for human review; a file-backed store persists this metadata
      alongside the extraction output for audit and for cross-document resolution on subsequent
      runs.


Relationship to the Rule-Based Layer. The two layers are complementary rather than redundant:
the rule-based algorithms run first and cheaply collapse obvious surface variants and expand aliases,
while the embedding layer catches semantically equivalent mentions that survive string matching
and does so under blocking to remain tractable at scale. Both feed the same review queue, and
the hard-conflict guard ensures the more aggressive embedding layer cannot override discriminating
evidence. Fig. 14 depicts the pipeline.




                                                  25
       Extracted                                Embed                                      Blocking                                      Candidate
        entities                             hash / semantic                      FAISS top- 𝑘 ∪ Metaphone                                 pairs

                            Auto-merge
                            score ≥ 0.85


                           Manual review                                           Decision                                       Multi-signal scorer
                             0.60–0.85                                              engine                                            7 weighted features



                              Distinct
                            score < 0.60                                               Hard-conflict guard
                                                                          differing DOB / nationality / ID ⇒ never merge


Fig. 14: Embedding-based entity resolution. Entities are embedded and blocked by the union of a FAISS
cosine index and a Double Metaphone phonetic block; each candidate pair is scored by a weighted
combination of seven signals; a decision engine routes the pair to auto-merge, manual review, or distinct under
tunable thresholds. A hard-conflict guard on discriminator attributes overrides the score and forbids merging
regardless of name similarity.


7      Pipeline architecture and quality refinement
7.1      Five-stage pipeline architecture

Fig. 15 illustrates the complete five-stage extraction pipeline, showing the flow from raw document
input through LLM extraction, data cleaning, cross-chunk merging, relationship enrichment, and
post-extraction entity enhancement. Stages 2 and 3 (highlighted in orange and purple) represent
the data cleaning fixes introduced after empirical evaluation (Section 7.3), while Stage 5 (red)
encompasses the six core deduplication algorithms detailed in Section 6.2.

                       1                        2                     3                       4                     5

          Raw                   LLM                  Per-Chunk              Cross-Chunk             Relationship         Post-Extr.                Knowledge
                              Extraction             Finalization             Merging                 2nd Pass            Enhance
        Document                                      normalise,             title-aware                                   aliases,                  Graph
      (PDF/text/img)         chunk, entity                                                             batched                                      (+ dedup)
                              & relation            de-loop, retype          dedup, IDs           cross-chunk LLM       mining, dedup


                                Fig. 16                  Fig. 17               Fig. 18                 Fig. 19              Fig. 20




Fig. 15: High-level overview of the five-stage extraction pipeline. A document enters at the left and flows
strictly left to right through chunked LLM extraction, deterministic per-chunk cleaning, cross-chunk merging,
a relationship second pass, and post-extraction enhancements, emerging as a validated knowledge graph.
Numbered badges key each stage to its detail figure (Figs. 16–20).

The extraction pipeline transforms raw documents into a validated JSON knowledge graph through
five sequential stages. Each stage addresses a distinct class of data-quality concern, from initial
LLM extraction through normalisation, deduplication, cross-chunk relationship discovery, and
post-extraction enrichment. The following subsections present the internal structure of each stage.


Stage 1: LLM Extraction. The pipeline begins by splitting the input document into overlapping
chunks of five pages each, with one page of overlap on each side to preserve cross-page context. For
each chunk, two sequential LLM calls are issued:

    1. Entity Extraction: the LLM identifies named entities (persons, organisations, locations,
       equipment) together with their properties and provisional aliases.
    2. Relationship Extraction: a second, dedicated LLM call receives the full entity catalog
       extracted so far plus the raw chunk text, and returns typed relationships with qualifiers and
       evidence spans.

A critical infrastructure bug was discovered during evaluation: the helper function _env_int()

                                                                               26
                          Raw Document Input
                               PDF / Text / Image




                 Stage 1 LLM Extraction (Per Chunk)

                           Document Chunking
                     chunk_pages=5, overlap neighbor=1



                        Phase 1: Entity Extraction
                   LLM extracts typed entities from chunk text


                                                                                          Infrastructure Fix
                    Phase 2: Relationship Extraction                                       _env_int() bug:
               Dedicated LLM call with entity catalog + source text                    max(1, 0) truncated source
                                                                                           text to 1 character



Fig. 16: Stage 1: LLM Extraction. The document is split into overlapping chunks; two sequential LLM calls
extract entities and relationships per chunk. The dashed annotation marks a critical infrastructure bug where
_env_int() defaulted the context window to one character, suppressing all per-chunk relationships.


used max(1, 0) instead of the configured context-window size, truncating the source text fed to the
relationship prompt to a single character and producing zero per-chunk relationships.

                                      Stage 2 Per-Chunk Finalization (Data Cleaning)

                                                    Normalize Relationship Types
                                       UPPER_SNAKE_CASE conversion + typo correction
                                   infiltrated → INFILTRATED, surveiled → SURVEILLED



                                            Remove Self-Referencing Relationships
                                                      Filter source == target loops
                                                          per_001 → per_001 ×



                                               Correct Entity Type Misassignment
                                                 Name-pattern-based type inference
                                          ‘Leviathan Submarine’ Person → Equipment



Fig. 17: Stage 2: Per-Chunk Finalization. Three deterministic cleaning passes normalise relationship types,
remove self-loops, and correct entity type misassignments before cross-chunk merging.



Stage 2: Per-Chunk Finalization. Before merging results across chunks, three deterministic
cleaning passes are applied to each chunk’s output:

   1. Relationship-type normalisation converts free-form LLM relationship labels into a controlled
      UPPER_SNAKE_CASE vocabulary and corrects common misspellings (e.g. surveiled →
      SURVEILLED).
   2. Self-loop removal filters out relationships where the source and target entity are identical, an
      artefact of LLM hallucination.
   3. Entity-type correction uses name-pattern heuristics to fix misclassified entities. For example,
      an entity named “Leviathan Submarine” initially typed as Person is reassigned to Equipment
      based on the suffix keyword “Submarine”.



                                                                      27
                             Stage 3 Cross-Chunk Merging (Entity Deduplication)

                                        Title-Aware Name Normalization
                                       Dynamic prefix stripping for canonical key
                                   ‘Colonel Mario Chavez’ → ‘Mario Chavez’



                                               Merge Chunk Results
                         Canonical-key dedup, property & alias merging, relationship ID remapping



                                           Consistent ID Reassignment
                              Uniform scheme: per_001, org_001, loc_001, eqp_001
                             per1, per1_2, per_087 → per_001, per_002, per_003



Fig. 18: Stage 3: Cross-Chunk Merging. Title-aware normalisation produces canonical keys; entities sharing
the same key are merged with property and alias unification; finally, all IDs are reassigned to a consistent
scheme.


Stage 3: Cross-Chunk Merging.                    This stage unifies entity records that were extracted
independently from different chunks:

   1. Title-aware name normalisation strips honorifics and titles (“Colonel”, “Dr.”, “Agent”) to
      produce a canonical key. This prevents the same person from appearing under both “Colonel
      Mario Chavez” and “Mario Chavez”.
   2. Chunk-result merging groups entities by canonical key and merges their properties, aliases,
      and associated relationships. Relationship source/target IDs are remapped to the merged entity.
   3. Consistent ID reassignment replaces the heterogeneous IDs produced by per-chunk extraction
      (per1, per1_2, per_087) with a uniform <type>_<seq> scheme.

                                       Stage 4 Relationship Second Pass

                                                Batch Entity Catalog
                                            batch_size=80, max_batches=8



                                  Cross-Chunk LLM Relationship Extraction
                                   Evidence-based discovery of inter-chunk relationships



                                            Relationship Deduplication
                                 Qualifier-aware merging by (source, target, type)
                                                         Fig. 11



Fig. 19: Stage 4: Relationship Second Pass. The merged entity catalog is batched and sent to the LLM for
cross-chunk relationship discovery; duplicate relationships are then merged using qualifier-aware
deduplication (Fig. 11).



Stage 4: Relationship Second Pass. Per-chunk extraction can only discover relationships whose
participants co-occur within a single chunk. Stage 4 performs a second LLM pass over the merged
entity catalog to discover cross-chunk relationships:

   1. Batching: the full entity catalog is partitioned into batches of up to 80 entities (at most
      8 batches) to stay within context-window limits.

                                                           28
   2. Cross-chunk LLM extraction: each batch is sent to the LLM alongside the source text,
      requesting evidence-grounded relationships between entities that may have originated from
      different chunks.
   3. Relationship deduplication: newly discovered and previously existing relationships are
      deduplicated by the composite key (source, target, type), with qualifier fields merged
      using Fig. 11.


        Stage 5 Post-Extraction Enhancements (Data Enrichment)

                          Alias Expansion (Fig. 7)
                      Deterministic abbreviation generation
         ‘Elena Petrov’ → ‘E. Petrov’, ‘Elena P.’, ‘EP’, ‘E.P.’



                         PDF Text Mining (Fig. 8)
                 Fuzzy matching for spelling variants in source text
                   Discovers ‘Jon’ when ‘John’ was extracted


                                                                                              Similarity-scorer Bug Fix
                         Similarity Scoring (Fig. 9)
            Multi-tier: exact → Slavic suffix → abbreviation → sequence                       Abbreviation check required
                                                                                                only first-letter match
           ‘Petrov’ vs ‘Petrova’ → 0.85 slavic_gender_suffix                                     → 79 false positives


                      Context-Aware Dedup (Fig. 10)
                       Role/org/location conflict validation
                Same name + different org → ‘different_people’




Fig. 20: Stage 5: Post-Extraction Enhancements. Four algorithms enrich the knowledge graph with expanded
aliases, text-mined spelling variants, similarity scores, and context-aware deduplication decisions. The dashed
annotation marks a bug in the similarity scorer (Fig. 9) where an overly permissive abbreviation check
produced 79 false-positive merge candidates.



Stage 5: Post-Extraction Enhancements. The final stage enriches the knowledge graph with alias
information and deduplication candidates through four algorithms:

   1. Alias Expansion (Fig. 7) deterministically generates abbreviations and name variants (e.g.
      “Elena Petrov” → “E. Petrov”, “EP”) to increase recall during downstream entity linking.
   2. PDF Text Mining (Fig. 8) performs fuzzy matching against the raw source text to discover
      spelling variants that the LLM normalised away (e.g. “Jon” vs. “John”).
   3. Similarity Scoring (Fig. 9) computes a multi-tier similarity score between all entity-name
      pairs using exact matching, Slavic gender-suffix handling, abbreviation detection, and sequence
      alignment. A bug in the abbreviation check, which required only a first-letter match, produced
      79 false positives before correction.
   4. Context-Aware Dedup Detection (Fig. 10) validates high-similarity pairs against contextual
      evidence (role, organisation, location) to distinguish true duplicates from distinct entities who
      share a name.


                                               Validated JSON Knowledge Graph
                                                Entities + Relationships + Dedup Candidates



Fig. 21: Pipeline output: a validated JSON knowledge graph containing typed entities, evidence-linked
relationships, and scored deduplication candidates ready for downstream analysis.

After all five stages complete, the pipeline emits a single JSON knowledge graph containing:

                                                                       29
      • Entities with normalised names, consistent IDs, merged properties, and expanded alias sets.
      • Relationships with typed labels, qualifier metadata, and evidence spans linking back to the
        source document.
      • Deduplication candidates scored by similarity and annotated with context-aware verdicts
        (same_person, different_people, uncertain).

7.2    Example extraction output

The output payload captures, for every entity, its full alias family with provenance (which discovery
method found each variant, and how often), the contextual attributes that anchor its identity, and
any scored duplicate candidates with a recommended action. Fig. 22 renders one representative
record as the graph fragment it becomes: the person per_001 carries six aliases discovered by three
different mechanisms, is linked to his employer by a qualified relationship, and is connected to the
similarly named per_002 only by a dashed dedup edge: the 0.929 name similarity was overridden
by conflicting context (different roles, different organisations), so the two remain distinct people.

                        J Doe       JD       John D.

      John Doe (LLM, × 3)       Jon Doe (text mining, × 2)    J. Doe (alias expansion)




                                         John                                 EMPLOYED_BY                                 Vector Glass
                                         Doe                                                                               Industries
                                                                 {date: 2024-06-15, location: London HQ}
                                         per_001                                                                               org_001



                                                             similarity 0.929 (spelling variant)
                                                             context conflict ⇒ kept distinct



 Context attributes
                                                                     John                          Context attributes
 role: Procurement Engineer
                                                                     Doe                           role: Logistics Clerk
 org: Vector Glass Industries
                                                                    per_002                        org: Khamsin Institute
 dedup_status: confirmed_unique


                                                                                                      LLM-extracted        algorithmic
                                                                                                      text-mined   - - dedup candidate


Fig. 22: A single output record rendered as the graph fragment it becomes. The entity carries six aliases
colour-coded by discovery mechanism (LLM extraction, algorithmic expansion, source-text mining, each with
occurrence counts), a qualified Employed_By relationship, and contextual attributes. The dashed edge is the
system’s restraint on display: despite a 0.929 name similarity to per_002, conflicting role and organisation
evidence keeps the two people distinct; the pair is exported in dedup_candidates for audit rather than
silently merged.


7.3    Empirical quality analysis and post-extraction data cleaning

While the six core deduplication algorithms (Section 6.2) address entity-level name variation
and relationship deduplication, empirical evaluation on a 45-page intelligence report (IR-001.pdf,
yielding 579 entities and 540 relationships) revealed a critical infrastructure bug together with six
data-quality issues originating from LLM output inconsistencies. These issues persisted despite the
existing algorithms because they occur upstream, in the raw LLM output, the chunk merging logic,
or the utility infrastructure, before the deduplication algorithms execute. This section documents
each issue, analyzes why the existing algorithms failed to catch it, and describes the applied fix. The
architectural placement of these fixes within the pipeline is illustrated in Fig. 15 (Stages 2–3).

                                                                      30
7.3.1   Critical infrastructure bug: source text truncation
Issue. All per-chunk relationship extractions (Phase 2) returned zero relationships despite the LLM
receiving 23–134 entities per chunk. Tracing the data through the call boundary exposed a striking
discontinuity (Table 11): the caller handed over the full chunk text, yet the relationship prompt saw
a single character.

Table 11: Observed evidence of the source-truncation bug on a representative chunk.

                      Observation point                        Expected       Observed
                      Source chars passed by caller              37,542         37,542
                      Source chars seen inside extraction        37,542           1
                      Entities provided to the LLM                 23             23
                      Relationships returned                     22–38             0



Root Cause. The configuration reader applied a well-intentioned safety guard to every integer
environment variable:
                                   𝑔(𝑣) = max(1, 𝑣),
intended to prevent division-by-zero in unrelated callers.                       But the variable
REL_EXTRACTION_MAX_SOURCE_CHARS uses the sentinel 𝑣 = 0 to mean unlimited; the
guard silently rewrote the sentinel, 𝑔(0) = 1, and the downstream slice 𝑆[ : 𝑔(0)] = 𝑆[ : 1] reduced
thirty-seven thousand characters of evidence to the single letter “P”. The relationship model, asked
to find relations in a one-character document, correctly returned none, which made the failure look
like a model deficiency rather than an infrastructure bug.


Fix. The guard was removed, restoring the sentinel semantics 𝑔(𝑣) = 𝑣 (with non-numeric values
falling back to the default). No other caller was affected, as every other integer default in the codebase
is ≥ 1.


Impact. Per-chunk relationship extraction immediately recovered, producing 22–38+ relationships
per chunk.

7.3.2   Fix 1: cross-chunk title-based entity duplication
Issue. The same real-world entity appeared as multiple distinct entities when the LLM extracted it
with different title prefixes across chunks. Table 12 shows representative examples.

Table 12: Title-Based Entity Duplication Examples from IR-001.pdf

        Chunk A Entity               Chunk B Entity                    Chunk C Entity
        per_087: “Mario Chavez”      per85_3: “Colonel Mario Chavez”   —
        per48_2: “Nicole Trujillo”   per47: “Dr. Nicole Trujillo”      per80: “Agent Dr. Nicole Trujillo”
        per5: “Bianca Knapp”         per2_2: “General Bianca Knapp”    —


Scale: 91 duplicate pairs detected, inflating the Person entity count from ∼224 to 315 (∼30%
inflation).


Why Fig. 10 Did Not Catch It. The context-aware duplicate detection algorithm did flag 66 of these
91 pairs but systematically classified every one as "different_people_different_contexts"
with low confidence. This occurred because: (1) the SequenceMatcher similarity between “Mario
Chavez” and “Colonel Mario Chavez” is only 0.75, falling below the 0.95 auto-merge threshold;
(2) the algorithm compared full strings without recognizing that one is a title-prefixed variant of the
other; (3) 25 pairs fell below the 0.75 detection threshold entirely.


                                                      31
Why the Chunk Merging Did Not Catch It. The canonical entity key used for
cross-chunk deduplication compared names verbatim: ("person", "colonel mario chavez")
≠ ("person", "mario chavez").

Fix. Introduced a dynamic name normalisation that strips leading prefix tokens until a two-word
core name remains, without a hardcoded title list. Writing a name as the token sequence 𝑤 1 𝑤 2 · · · 𝑤 𝑛 ,
the normal form is computed by the recurrence
                                     (
                                       norm(𝑤 2 · · · 𝑤 𝑛 ) if 𝑛 > 2 ∧ prefixlike(𝑤 1 ),
              norm(𝑤 1 · · · 𝑤 𝑛 ) =
                                       𝑤1 · · · 𝑤 𝑛         otherwise,
where prefixlike(𝑤) holds when 𝑤 ends in a period ( “Dr.” ) or is a short alphabetic token (|𝑤| ≤ 12,
covering “Colonel”, “General”, “Agent”). Because the rule is structural rather than lexical, unseen
titles normalise correctly: “Agent Dr. Nicole Trujillo” → “Dr. Nicole Trujillo” → “Nicole Trujillo”,
terminating at the two-word core. The merge logic preserves the titled variant as an alias while
promoting the base name to primary: “Mario Chavez” with alias “Colonel Mario Chavez”.

7.3.3   Fix 2: relationship type inconsistency
Issue. The same relationship type appeared in multiple casings and formats across chunks,
preventing proper deduplication by Fig. 11.

Table 13: Relationship Type Variants from IR-001.pdf

                  Variant 1               Variant 2               Variant 3
                  INFILTRATED (7)         INfiltrated (15)        infiltrated (4)
                  REPORTED_TO (22)        reported to (5)         —
                  SURVEILLED (64)         surveilled (1)          surveiled (1, typo)


Root Cause. Fig. 11 deduplicates by the key (𝑢, 𝑣, 𝑡) but compared type 𝑡 as a raw string without
normalization.

Fix.    Every relationship type is canonicalised during finalisation by the mapping
                                      𝑡 ′ = 𝜏 Upper(Snake(𝑡)) ,
                                                                 

where Snake collapses whitespace and hyphen runs to underscores, Upper uppercases, and
𝜏 is a small typo-correction table accumulated from observed LLM output (𝜏(SURVEILED) =
SURVEILLED, 𝜏(TRANSFERED) = TRANSFERRED). After canonicalisation the three INFILTRATED
variants of Table 13 collapse to one key and deduplicate correctly.

7.3.4   Fix 3: self-referencing relationships
Issue. 114 relationships (21% of all 540) had source == target, meaning an entity was related
to itself. One entity (“Dr. Nicole Trujillo”) had nine self-loops including SURVEILLED, FUNDED,
MONITORED, and DEPLOYED_TO pointing to herself.

Root Cause. When the LLM cannot resolve the correct target entity for a relationship, it defaults
to reusing the source entity ID, a known hallucination pattern observed more frequently with smaller
local models than with the cloud-hosted alternative.

Fix.    Self-loops are removed by a single set filter during finalisation:
                                    𝜌 ′ = { (𝑢, 𝑣, 𝑡) ∈ 𝜌 : 𝑢 ≠ 𝑣 },
which on IR-001.pdf discarded all 114 self-referencing relationships while leaving every legitimate
edge untouched.

                                                    32
7.3.5   Fix 4: entity type misassignment
Issue. 42 entities with clearly non-person names were assigned the type “Person” by the LLM.
Table 14 shows representative examples.

Table 14: Entity Type Misassignment Examples

         Entity Name                       Assigned Type     Correct Type    Indicator Word
         “Bank”                            Person            Organization    —
         “Leviathan Submarine LS-6720”     Person            Equipment       submarine
         “Christopherchester Camp”         Person            Location        camp
         “Agency”                          Person            Organization    agency



Root Cause. In later chunks of long documents, the LLM’s entity typing accuracy degrades,
consistent with reported positional degradation in long contexts [34]. The model occasionally
assigns “Person” as a default type.

Fix. A post-extraction type inference function checks entity names for indicator words (e.g., camp,
laboratory → Location; agency, institute → Organization; submarine, drone → Equipment). This
runs only on entities typed as “Person” and only reclassifies when a strong indicator word is present,
minimizing false corrections.

7.3.6   Fix 5: inconsistent entity ID scheme
Issue. Entity IDs used at least seven different format patterns across chunks: per1, per1_2,
per_001, org_020, e_local_5, etc. This inconsistency arose because each chunk’s LLM
call independently generated entity IDs, and the merge function added collision suffixes without
normalizing the base format.

Fix. A final-stage ID reassignment function converts all entity IDs to a uniform
{prefix}_{number} format (e.g., per_001, org_001, loc_001, eqp_001) and remaps all
relationship references accordingly. Additionally, relationships referencing entity IDs that do not
exist in the final entity list (9 dangling references in IR-001.pdf) are filtered out.

7.3.7   Fix 6: false positive abbreviation similarity matches
Issue. The abbreviation signal of Fig. 9 produced 79 nonsensical matches with a hardcoded
0.92 similarity score. For example, “Michael Cruz” and “Mario Chavez” were flagged as
abbreviation_variant because both names have two words starting with ‘M’ and ‘C’ respectively.

Root Cause.    For two name parts 𝑝 and 𝑞, the buggy check accepted the pair whenever
                             matchbuggy ( 𝑝, 𝑞) ⇐⇒ 𝑝 = 𝑞 ∨ 𝑝 1 = 𝑞 1 ,
i.e. identical parts or merely identical first letters. Under this predicate “Michael”/“Mario” match
on ‘M’ and “Cruz”/“Chavez” match on ‘C’, so two entirely different people clear the abbreviation
check and receive its hardcoded 0.92 score.

Fix. A genuine abbreviation requires one side to actually be a single-letter token. The corrected
predicate is
                                                                                  
             match( 𝑝, 𝑞) ⇐⇒ 𝑝 = 𝑞 ∨ | 𝑝| = 1 ∧ 𝑝 = 𝑞 1 ∨ |𝑞| = 1 ∧ 𝑞 = 𝑝 1 ,
and the pair as a whole is accepted only if at least one part-pair matched through the single-letter
clause, i.e. an abbreviation was genuinely present. After the fix, “E. Petrov” vs. “Elena Petrov” still
matches (|E| = 1 ∧ E = Elena1 ), while “Michael Cruz” vs. “Mario Chavez” is correctly rejected: no
part is a single letter, so first-letter coincidence no longer suffices.

                                                    33
7.3.8      Summary of quality fixes
Table 15 summarizes the six data cleaning fixes and the infrastructure bug. These fixes operate at
Stages 2–3 of the pipeline (Fig. 15), cleaning the raw LLM output before the core deduplication
algorithms (Stage 5) execute.

Table 15: Summary of Post-Extraction Data Cleaning Fixes

      #    Fix                      Root Cause                                 Entities            Rels
      0    _env_int() bug           max(1,0) truncated source text               0              All (0→500+)
      1    Title normalization      Verbatim name comparison                91 merged          Refs remapped
      2    Rel type normalization   No case normalization                        0              ∼30 deduped
      3    Self-loop filtering      LLM hallucination                            0              114 removed
      4    Entity type correction   LLM accuracy degradation              42 reclassified             0
      5    ID reassignment          Independent per-chunk IDs             All renumbered     9 dangling removed
      6    Abbreviation fix         First-letter-only match                      0             0 (dedup fixed)


Table 16: Net Quality Impact on IR-001.pdf (45 pages)

           Metric                                 Before Fixes       After Fixes            Change
           Total entities                              579              ∼400           −31% (dedup)
           True Person count                      315 (inflated)        ∼224          −29% (accurate)
           Per-chunk relationships                       0              500+             Restored
           Self-loop relationships                 114 (21%)              0               −100%
           Broken entity references                      9                0               −100%
           Relationship type variants                   39              ∼28          −28% (normalized)
           False positive dedup candidates              79               ∼0               −100%
           Entity ID format patterns                     7                1              Uniform


Key Insight. The core deduplication algorithms (Figs. 7–10) were correctly designed for
entity-level refinement, but their effectiveness was undermined by upstream data quality issues
in the raw LLM output and the chunk merging infrastructure. The data cleaning fixes (Stages 2–3)
and the core algorithms (Stage 5) are complementary: the former ensures clean input data, while the
latter enriches it. Together, they form a defense-in-depth approach where neither layer alone would
be sufficient.

8     Evaluation
We evaluate the system on two axes: the impact of the deduplication and grounding enhancements
on retrieval quality (Section 8.1), and an end-to-end stress test of the OCR pipeline on an adversarial
image-only document (Section 8.2).

8.1       Deduplication and retrieval impact

Table 17: Performance Metrics Before and After Entity Deduplication Enhancement

          Metric                               Before Phase 3         After Phase 3         Improvement
          Aliases per entity                         1.0                    5.0                +400%
          Name variants discovered                    0                ∼6 per entity             +6
          Dedup candidates detected                   0                Auto-flagged             N/A
          False positives                             0                      0               Maintained
          Processing overhead                        N/A                 <250 ms            <0.5% latency
          Search recall                             ∼70%                  ∼95%                +25–30%
          Graph false merges prevented                0              4–8 per document        High impact


                                                          34
                                              Deduplication Enhancement: Key Results at a Glance


       +400%                    95%                         0                   94%                     <250 ms                  7
      aliases / entity        search recall            false merges         catalog size drop           added latency       quality fixes



Fig. 23: Summary of the principal quantitative results from the deduplication and ontology-grounding
enhancements described in Sections 6.2–7.3.


8.2       OCR pipeline on naval intelligence documents

8.2.1        Evaluation corpus and setup
To stress-test the extraction layer under adversarial OCR conditions, we evaluate on a 10-page
Joint Fleet Summary (JFS) document, a naval intelligence report listing PLAN (People’s Liberation
Army Navy) vessel classes by identifier, hull number, and role. The document is image-only (zero
extractable characters, Signal 4 = 0 throughout) and contains a dense, structured layout: multi-column
tables, abbreviated headings, and a long-tail vocabulary of Chinese transliterated ship-class names
(Zhongyu, Hutao, Shuoshi, Dalang, Jiangwei, Zhaochang, Dayun, . . . ) that fall far outside
general-purpose LLM training corpora. All 17 distinct vessel-class names serve as ground-truth
labels for recall measurement. The document is processed exclusively through the OCR path (100%
image pages, text-page ratio = 0); no born-digital text is available at any stage.
Two configurations are compared: the legacy system (un-guided extraction, binary PDF
routing, no deduplication) and the fixed system (full pipeline: ontology-guided extraction,
per-page OCR classification, deduplication, type correction). A chunk-size ablation then varies
OCR_TEXT_CHUNK_PAGES ∈ {5, 2} to quantify the recall–latency trade-off introduced by smaller
windows on OCR-derived text.

8.2.2        Headline results: legacy versus fixed pipeline
Table 18 summarises the principal metrics; Fig. 24 renders the most dramatic contrasts visually.

Table 18: Headline extraction metrics on the 10-page JFS document: legacy (un-guided) versus fixed (full)
pipeline. Chunk size = 5 pages for both.

              Metric                                         Legacy                             Fixed       Δ
              Wall-clock time                         294.6 s (4:55)              204.9 s (3:25)            −30%
              Total entities extracted                          215                           83            −61% (fakes removed)
              Total relationships                                 98                          64            −35% (fakes removed)
              Ground-truth class names                   0/17 (0%)                5/17 (29.4%)              +29.4 pp
              Hallucinated entities                             174                            1            −173
              Hallucination rate                             80.9%                         1.2%             −79.7 pp
              Entity typing                     Person/Org (wrong)      Ship/ShipClass (correct)            semantic fix
              Distinct relationship types                          5                           8            +60%




Hallucination Pattern. The legacy pipeline produced 174 entities of the form “Dong You 576”,
“Dong You 598”, “Dong You 649”, . . . (and similar sequential-suffix variants), all typed as Person.
These arise from a systematic OCR mis-read of hull-number columns: the model transcribed table
row numbers as given names and appended them to a partial transliteration of the column header.
Because the legacy system had no ontology constraint, the LLM accepted these as plausible human
names and emitted them confidently. The fixed pipeline suppresses this class of hallucination through
two complementary mechanisms: (1) ontology-guided extraction constrains the type vocabulary to
Ship and ShipClass for naval documents (the fixed run emits 71 Ship and 12 ShipClass entities,
against the legacy run’s 174 Person and 41 Organization), making “Dong You 576: Person” a
schema violation the model avoids; (2) the alias-expansion and context-aware deduplication stage
consolidates the surviving 174 near-identical variants into a single candidate for review.



                                                                       35
                               Legacy vs. Fixed Pipeline: Four Key Dimensions


        Wall-clock               Hallucination rate                Ground-truth recall            Entity types

         4:55                       80.9%                               0/17                      Person / Org
         3:25                        1.2%                               5/17                    Ship / Ship Class
           − 30%                      − 79.7 pp                         +29.4 pp                   semantic fix
         legacy / fixed               legacy / fixed                    legacy / fixed              legacy / fixed



Fig. 24: Four headline dimensions on the JFS document. The legacy pipeline misclassifies all naval vessels as
Persons or Organisations and produces 174 hallucinated “Dong You 576/598/649 . . . ” variants. The fixed
pipeline eliminates the hallucinations, corrects entity types to Ship/Ship Class via ontology-guided extraction,
and captures 29.4% of ground-truth class names at 30% lower wall-clock cost.


8.2.3   Chunk-size ablation study
For OCR-derived text, smaller chunks present a richer slice of the document’s long-tail vocabulary
to each LLM call at the cost of more calls and higher latency. Table 19 presents results for
OCR_TEXT_CHUNK_PAGES ∈ {5, 2}.

Table 19: Chunk-size ablation on the JFS document. Reducing OCR_TEXT_CHUNK_PAGES from 5 to 2 doubles
ground-truth recall at the cost of a 2:30 latency increase.

            Metric                                     Legacy    Fixed (chunk=5)         Fixed (chunk=2)
            Wall-clock                                 4:55                  3:25                    5:55
            Ground-truth class names                   0/17         5/17 (29.4%)           10/17 (58.8%)
            Hallucinated entities                       174                     1                       0
            Distinct entity types                2 (wrong)                      2                       4
            Distinct relationship types            5 (fake)                     8                      18
            Total relationships                   98 (fake)                    64                     206



Analysis. Halving the chunk size from 5 to 2 pages delivers a +29.4 percentage-point improvement
in ground-truth recall (29.4% → 58.8%) and eliminates the last hallucinated entity. Five additional
vessel classes are captured (Zhongyu, Hutao, Shuoshi, Dalang, Jiangwei, Zhaochang), while
one class (Dayun) is displaced because it falls at a chunk boundary that no longer favours its context.
The relationship count triples (64 → 206) as smaller windows surface intra-table cross-references that
were folded into a single long chunk before. The trade-off is a 2:30 wall-clock increase (3:25 → 5:55),
driven by the larger number of LLM calls. The recall-curve as a function of chunk pages is visualised
in Fig. 25.

8.2.4   Residual errors and improvement roadmap
Even with chunk=2, 7 of 17 ground-truth vessel classes are missed. The residual errors fall into four
structural categories, each with a targeted intervention (Table 20).
The multi-pass union and the directive-prompt interventions require no infrastructure changes and
are the natural next step. The dense-layout crop-and-re-OCR addresses the structural root cause for
multi-column tables, which accounts for the majority of missed vessel-class names in the JFS corpus.




                                                            36
               recall (%)

                                                     latency: chunk=2 → 5:55, chunk=5 → 3:25


                                             58.8%
             58.8%




                                                                             29.4%
             29.4%




                      legacy: 0%
               0%                                                                              chunk pages
                                         2                               5

Fig. 25: Ground-truth vessel-class recall vs. chunk size (pages per LLM call) on the 10-page JFS document.
The dashed red line shows the legacy baseline (0%). Smaller chunks surface more of the long-tail vocabulary
at the cost of higher latency.




Table 20: OCR residual-error taxonomy and improvement roadmap. Interventions are ordered by
implementation complexity; expected lift is qualitative.

 Root cause                        Intervention                 Cost                       Expected lift
 OCR non-determinism:              Multi-pass OCR +             2–3× OCR time              Medium–high
 different runs recover            transcript union:
 different names                   re-transcribe each page
                                   2–3×, union outputs
 Image quality below               Higher DPI (200 →            +file size                 Low–medium
 model’s reading floor             300 dpi), contrast
                                   enhancement,
                                   sharpening
 Under-specified                   Directive prompt:            Free                       Low–medium
 transcription prompt              “preserve every all-caps
                                   heading, numeric
                                   prefix, and bold word”
 Long-tail vocabulary              Dedicated OCR model          Infrastructure             High
 OOV to vision model               (e.g. Tesseract with
                                   custom dictionary) run
                                   alongside VLM; union
                                   outputs
 Dense layout regions              Crop-and-re-OCR:             Engineering                High
 (multi-column, tight              detect dense regions,
 tables)                           re-render at 400 dpi,
                                   OCR independently




                                                       37
8.3            Benchmark campaign: local model versus cloud ceiling

The case studies above use the production extraction model. To establish whether a locally hosted
model is good enough for deployment, or whether a cloud model is required, we ran a controlled
campaign comparing the local model (Konect-U/Qwen3.5-9B-AWQ-4bit-Ontology, served via
vLLM) against a strong cloud model (Gemini 2.5 Flash) used purely as an upper-bound calibration
reference, not a production candidate. The decision lens throughout is: is the local model good
enough, and where are the gaps? The campaign spans four phases (entity/relation extraction, OCR,
and two ontology-conformance settings) on public benchmarks with fixed seeds; samples are small
(𝑛 = 8–50), so results are directional rather than statistically significant.


Phase 1: extraction quality. On CoNLL04 (𝑛 = 50) and Re-DocRED (𝑛 = 20) the local model
trails the cloud model by roughly six points on entity spans and is at parity on relations (Table 21).
Absolute F1 is low for both providers because open-schema ontology extraction is scored here against
closed academic label sets with strict surface matching; we therefore report span-only and pair-only
F1 and read the numbers as directional calibration, not capability ceilings.

Table 21: Phase 1 extraction quality (micro-F1, span-only / pair-only) on closed-label academic sets. Absolute
values are deflated by the closed-label scoring; the local-vs-cloud gap is the signal.

                                  Dataset       Metric                             Local   Cloud       Δ
                                  CoNLL04       Entity (span-only)                59.6%    65.3%   +5.7
                                  CoNLL04       Relation (pair-only)              16.3%    19.9%   +3.6
                                  Re-DocRED     Entity (span-only)                60.8%    66.6%   +5.8
                                  Re-DocRED     Relation (pair-only)              21.2%    20.6%   −0.6



Phase 2: OCR. Across three OCR datasets the local model matches the cloud model on
clean English (FUNSD forms, CORD receipts) and beats it on multilingual scans (XFUND,
German/Spanish), while a classical OCR engine (Paddle) trails everywhere (Fig. 26). The local
model was also the only engine with no runaway or empty-output failures; the cloud model loops
on dense forms because its API rejects the repetition penalty that would suppress the behaviour.
Token-F1 of 0.86–0.95 shows recognition is strong even where order-sensitive WER is inflated
by ground-truth layout noise. The verdict is that local OCR is production-viable with no cloud
dependency.

                                                Local (Qwen)        Cloud (Gemini)            Paddle

                1
                                                                    0.95   0.95                                0.95

                                                                                                                      0.92
                                                                                                                             0.9




  Token-F1 ↑
               0.9         0.87   0.87                                            0.86




                                         0.78
               0.8


               0.7
                       FUNSD (EN)                              CORD (EN)                                   XFUND (DE/ES)

Fig. 26: OCR token-F1 across three datasets and three engines. The local model matches the cloud model on
English and overtakes it on multilingual XFUND scans; the classical Paddle engine trails on every dataset.



Phases 3–4: ontology conformance versus recall. With the target ontology force-injected as
a catalog, both providers reach high schema conformance (68–70% on Text2KGBench, ≈89%


                                                               38
on OSKGC) with near-zero hallucination, but under-extract: triple-level F1 stays low (22–26% /
35–40%), and on OSKGC the fine-grained type-mapping accuracy is only 42–50% (the model emits
a generic Location where the schema expects City). Fig. 27 contrasts the strong conformance
against the weak triple recall and mapping. This high-conformance / low-recall signature is exactly
the gap that richer ontology retrieval (Section 4) is designed to close without regressing conformance
or hallucination.

                                                        Text2KGBench           OSKGC

       100                            89.1

        80
                               68.1

        60
  %                                                                                 41.7
                                                              40
        40
                                                       22.3
        20
                                                                                0                     1.9   0
          0
                        Conformance               Triple F1 (norm)         Mapping acc.         Hallucination

Fig. 27: Ontology results (local model). High conformance and near-zero hallucination coexist with low
triple-level recall and low fine-grained mapping accuracy. Mapping accuracy is not defined for Text2KGBench
(no schema-type triples), shown as zero. The recall and mapping gaps motivate retrieval-based grounding.



Takeaways. The local model is production-viable for OCR (at or above the cloud ceiling, especially
multilingual) and within ∼6 points on academic extraction, while matching the cloud model on
ontology conformance with zero hallucination. The measured weak spots, triple-level recall and
fine-grained type mapping, are precisely the targets of the ontology-guided retrieval mechanism
rather than reasons to move to a cloud model.

8.4    End-to-end accuracy against a ground-truth document

Finally, we measure end-to-end accuracy on a synthetic intelligence report with a hand-built
ground-truth key (entities, properties, and relationships across nine document sections). This
complements the benchmark campaign with a whole-document view of the production pipeline
rather than per-phase scores. Fig. 28 summarises six accuracy dimensions; the overall accuracy is
≈93%.

       Entity completeness                                                                                                 100

           Entity properties                                                                                               100

              Entity typing                                                                                      90

Relationship completeness                                                                                             95

      Relationship accuracy                                                                                      90

         Qualifier accuracy                                                                                      90

                               0             10   20    30          40    50        60     70    80             90     100
                                                                         accuracy (%)

Fig. 28: End-to-end accuracy on a ground-truth intelligence document across six dimensions (overall ≈93%).
All 16 persons were extracted with exact role/organisation attribution; every entity class (organisations,
locations, operations, technologies, vehicles, events, financials) was captured, and relationships covered all
nine document sections with correct date/time/location qualifiers. The residual gaps are cosmetic: redundant
generic “Item” typing alongside the specific technology/vehicle types, and a few over-verbose relationship
labels lifted verbatim from prose.


                                                                   39
Entity completeness and property attribution were exact: all persons were recovered with correct
roles, and every organisation, location, operation, technology, vehicle, event, and financial entity
in the key was captured. The two sub-100% entity dimensions are cosmetic, a generic Item type
emitted redundantly alongside the specific Technology/Vehicle types, and one document-title
string over-extracted as an organisation. Relationship coverage spanned all nine sections with correct
source/target pairs and qualifier attribution (dates, times, locations), the residual loss coming from
a few over-verbose relationship labels copied verbatim from strategic-assessment prose. These
are exactly the upstream artifacts the Stage 2–3 cleaning fixes (Section 7.3) target, and they are
addressable by post-processing without changing the extraction model.

9    Limitations
Several limitations qualify the results. Evaluation breadth: the case studies derive from single
representative documents per condition (a 45-page intelligence report for the deduplication analysis;
a 10-page naval summary for the OCR ablation), and the benchmark campaign (Section 8.3) uses
small public-dataset samples (𝑛 = 8–50) with fixed seeds; none of the results carry significance
testing or inter-annotator agreement on the ground-truth labels, so they should be read as directional
engineering evidence rather than statistically validated effect sizes. The cloud-model comparison is
an upper-bound calibration, not a controlled provider study. OCR recall ceiling: even at the best
chunk size, ground-truth vessel-class recall reaches only 58.8%, and the roadmap interventions of
Table 20 remain unimplemented. Hand-tuned components: the similarity-scorer weights, retrieval
thresholds (0.72 floor, 0.80 expansion trigger), and indicator-word lists are heuristics tuned on
the development corpus; they have not been learned from labelled data and may not transfer across
domains without re-tuning. Attribution of causes: explanations offered for observed model behaviour
(for example, attention dilution as the cause of late-chunk type degradation [34]) are plausible
readings of the evidence, not controlled findings. Infrastructure dependence: throughput numbers
reflect one specific local deployment and do not generalise across hardware.

10    Ethics and broader impact
This system extracts and resolves identities of people from intelligence-domain documents, a
capability with inherent dual-use risk. Two harms deserve explicit treatment. Misidentification: an
erroneous entity merge can attribute one person’s actions to another. The architecture is deliberately
conservative here: context-validated deduplication never auto-merges on name similarity alone, a
hard-conflict guard forbids merging entities with contradictory discriminator attributes regardless of
score, and borderline pairs are exported for human review rather than resolved silently. Every merge
decision carries provenance, so downstream consumers can audit why two mentions were linked.
Surveillance: alias expansion and cross-document resolution increase the recall of person-centric
search, which is precisely the property that makes the system useful and the property that demands
governance. Deployments should restrict access to authorised analysts, log queries, and operate
within applicable legal frameworks for the jurisdiction of use. All person and organisation names
appearing in this paper’s examples are fictional placeholders; no real individuals’ data are reproduced.
The evaluation corpora are synthetic intelligence-style documents created for system development.

11    Conclusion
This paper presented a production extraction layer that converts a heterogeneous, real-time document
stream into a validated, ontology-aligned knowledge graph. Its principal advantages are threefold.
First, ontology-guided extraction with live graph retrieval aligns emitted types with a formal schema
while cutting catalog prompt overhead by roughly 94 percent relative to static domain slices, and
the four retrieval refinements (term vectors, subclass expansion, predicate full-text search, and
density-ranked windowing) recover the specific classes and predicates that embedding similarity
alone misses. Second, the layered deduplication design, six zero-inference rule-based algorithms
followed by embedding-based resolution with a hard-conflict guard, raised search recall from roughly
70 to 95 percent without a single false merge. Third, the per-page OCR classifier and the quality-gated
relationship second pass make the pipeline robust to mixed documents and to silent under-extraction,
and the empirical evaluation on naval intelligence documents showed the full pipeline cutting


                                                  40
hallucinated entities from 174 to zero while tripling relationship coverage.
The architecture generalises beyond intelligence analysis to any setting that must turn unstructured
documents into a queryable graph under a governed schema, including compliance monitoring,
investigative journalism, and enterprise knowledge management. Because ontology grounding,
deduplication, and graceful degradation are architectural concerns rather than afterthoughts, each
component can be adopted independently by existing extraction pipelines.

12    Reproducibility statement
The pipeline is implemented in Python against an OpenAI-compatible inference endpoint;
all thresholds, weights, and configuration knobs referenced in the paper are reported
in the text and in Appendix B. Extraction uses the locally hosted, ontology-tuned
model Konect-U/Qwen3.5-9B-AWQ-4bit-Ontology (a 4-bit AWQ quantisation of
Qwen3.5-9B [35]) served via vLLM [2], with the companion embedding model
Konect-U/Qwen3-Embedding-0.6B-Ontology for retrieval and resolution; the spreadsheet
plan-then-execute stage and all deduplication algorithms are deterministic given a fixed extraction
output. The evaluation documents are synthetic intelligence-style corpora created for development
and cannot be redistributed in full; the ground-truth label lists and per-run metric tables are
reproduced in the paper. Code and prompts are proprietary to the production deployment at the time
of writing; an open reference implementation is under consideration.

References
 [1] Kreps, J., Narkhede, N., & Rao, J. (2011). Kafka: A distributed messaging system for log
     processing. In Proceedings of the NetDB (Vol. 11, pp. 1–7).
 [2] Kwon, W., Li, Z., Zhuang, S., Sheng, Y., Zheng, L., Yu, C. H., Gonzalez, J., Zhang, H., & Stoica,
     I. (2023). Efficient memory management for large language model serving with PagedAttention.
     In Proceedings of the 29th Symposium on Operating Systems Principles (SOSP) (pp. 611–626).
 [3] Pan, S., Luo, L., Wang, Y., Chen, C., Wang, J., & Wu, X. (2024). Unifying large language models
     and knowledge graphs: A roadmap. IEEE Transactions on Knowledge and Data Engineering,
     36(7), 3580–3599.
 [4] Zhu, Y., Wang, X., Chen, J., Qiao, S., Ou, Y., Yao, Y., Deng, S., Chen, H., & Zhang, N.
     (2024). LLMs for knowledge graph construction and reasoning: Recent capabilities and future
     opportunities. World Wide Web, 27(5), 58.
 [5] Colvin, S. (2024). Pydantic (Version 2) [Computer software]. https://github.com/
     pydantic/pydantic
 [6] Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M.,
     Yih, W., Rocktäschel, T., Riedel, S., & Kiela, D. (2020). Retrieval-augmented generation for
     knowledge-intensive NLP tasks. In Advances in Neural Information Processing Systems (Vol.
     33, pp. 9459–9474).
 [7] Christophides, V., Efthymiou, V., Palpanas, T., Papadakis, G., & Stefanidis, K. (2020). An
     overview of end-to-end entity resolution for big data. ACM Computing Surveys, 53(6), 1–42.
 [8] Papadakis, G., Skoutas, D., Thanos, E., & Palpanas, T. (2020). Blocking and filtering techniques
     for entity resolution: A survey. ACM Computing Surveys, 53(2), 1–42.
 [9] Ratcliff, J. W., & Metzener, D. E. (1988). Pattern matching: The gestalt approach. Dr. Dobb’s
     Journal, 13(7), 46–51.
[10] Knight, K., & Graehl, J. (1998). Machine transliteration. Computational Linguistics, 24(4),
     599–612.
[11] Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., &
     Polosukhin, I. (2017). Attention is all you need. In Advances in Neural Information Processing
     Systems (Vol. 30).

                                                 41
[12] Brown, T. B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., Neelakantan, A.,
     Shyam, P., Sastry, G., Askell, A., et al. (2020). Language models are few-shot learners. In
     Advances in Neural Information Processing Systems (Vol. 33, pp. 1877–1901).
[13] Wei, X., Cui, X., Cheng, N., Wang, X., Zhang, X., Huang, S., Xie, P., Xu, J., Chen, Y., Zhang,
     M., Jiang, Y., & Han, W. (2023). ChatIE: Zero-shot information extraction via chatting with
     ChatGPT. arXiv. https://arxiv.org/abs/2302.10205
[14] Wang, S., Sun, X., Li, X., Ouyang, R., Wu, F., Zhang, T., Li, J., & Wang, G. (2025).
     GPT-NER: Named entity recognition via large language models. In Findings of the Association
     for Computational Linguistics: NAACL 2025 (pp. 4257–4275).
[15] Huguet Cabot, P.-L., & Navigli, R. (2021). REBEL: Relation extraction by end-to-end language
     generation. In Findings of the Association for Computational Linguistics: EMNLP 2021 (pp.
     2370–2381).
[16] Wadhwa, S., Amir, S., & Wallace, B. (2023). Revisiting relation extraction in the era of
     large language models. In Proceedings of the 61st Annual Meeting of the Association for
     Computational Linguistics (ACL) (pp. 15566–15589).
[17] Gruber, T. R. (1993). A translation approach to portable ontology specifications. Knowledge
     Acquisition, 5(2), 199–220.
[18] Page, L. (1998). The PageRank citation ranking: Bringing order to the web (Technical Report).
     Stanford Digital Library Technologies Project.
[19] Fellegi, I. P., & Sunter, A. B. (1969). A theory for record linkage. Journal of the American
     Statistical Association, 64(328), 1183–1210.
[20] Elmagarmid, A. K., Ipeirotis, P. G., & Verykios, V. S. (2007). Duplicate record detection: A
     survey. IEEE Transactions on Knowledge and Data Engineering, 19(1), 1–16.
[21] Mudgal, S., Li, H., Rekatsinas, T., Doan, A., Park, Y., Krishnan, G., Deep, R., Arcaute, E.,
     & Raghavendra, V. (2018). Deep learning for entity matching: A design space exploration. In
     Proceedings of the 2018 International Conference on Management of Data (SIGMOD) (pp.
     19–34).
[22] Brunner, U., & Stockinger, K. (2020). Entity matching with transformer architectures: A step
     forward in data integration. In Proceedings of the 23rd International Conference on Extending
     Database Technology (EDBT) (pp. 463–473).
[23] Christen, P. (2006). A comparison of personal name matching: Techniques and practical issues.
     In Sixth IEEE International Conference on Data Mining Workshops (ICDM) (pp. 290–294).
[24] Cohen, W., Ravikumar, P., & Fienberg, S. (2003). A comparison of string distance metrics for
     name-matching tasks. In Proceedings of the IJCAI-2003 Workshop on Information Integration
     on the Web (IIWeb) (pp. 73–78).
[25] Navarro, G. (2001). A guided tour to approximate string matching. ACM Computing Surveys,
     33(1), 31–88.
[26] Winkler, W. E. (1990). String comparator metrics and enhanced decision rules in the
     Fellegi–Sunter model of record linkage. In Proceedings of the Section on Survey Research
     Methods, American Statistical Association (pp. 354–359).
[27] Philips, L. (2000). The double metaphone search algorithm. C/C++ Users Journal, 18(6),
     38–43.
[28] Freeman, A. T., Condon, S. L., & Ackerman, C. M. (2006). Cross linguistic name matching
     in English and Arabic. In Proceedings of the Human Language Technology Conference of the
     NAACL (pp. 471–478).
[29] Shen, W., Wang, J., & Han, J. (2015). Entity linking with a knowledge base: Issues, techniques,
     and solutions. IEEE Transactions on Knowledge and Data Engineering, 27(2), 443–460.

                                                42
[30] Cucerzan, S. (2007). Large-scale named entity disambiguation based on Wikipedia data.
     In Proceedings of the 2007 Joint Conference on Empirical Methods in Natural Language
     Processing and Computational Natural Language Learning (EMNLP-CoNLL) (pp. 708–716).
[31] Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence embeddings using Siamese
     BERT-networks. In Proceedings of the 2019 Conference on Empirical Methods in Natural
     Language Processing and the 9th International Joint Conference on Natural Language
     Processing (EMNLP-IJCNLP) (pp. 3982–3992).
[32] Artifex Software. (2024). PyMuPDF documentation. https://pymupdf.readthedocs.io/
[33] Johnson, J., Douze, M., & Jégou, H. (2019). Billion-scale similarity search with GPUs. IEEE
     Transactions on Big Data, 7(3), 535–547.
[34] Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P. (2024).
     Lost in the middle: How language models use long contexts. Transactions of the Association
     for Computational Linguistics, 12, 157–173.
[35] Yang, A., Li, A., Yang, B., Zhang, B., Hui, B., Zheng, B., . . . & Qiu, Z. (2025). Qwen3 technical
     report. arXiv. https://arxiv.org/abs/2505.09388
[36] Wang, G., Koshy, J., Subramanian, S., Paramasivam, K., Zadeh, M., Narkhede, N., Rao,
     J., Kreps, J., & Stein, J. (2015). Building a replicated logging system with Apache Kafka.
     Proceedings of the VLDB Endowment, 8(12), 1654–1655.


A      Threshold reference
Table 22 consolidates every tunable threshold in the extraction and resolution pipeline, the
subsystem it governs, and the decision it drives. These are deployment defaults tuned on the
development corpus; we do not claim universality. The class/predicate retrieval floor is overridable
via the ONTOLOGY_RETRIEVAL_MIN_SCORE environment variable. Independently of any score, a
hard-conflict guard on discriminator keys (date of birth, nationality, passport or employee number)
forbids merging two entities, however similar their names (the embedding-based resolution engine).

B     Operational configuration
This appendix collects deployment-level configuration detail referenced from the main text: Kafka
consumption and session management, the evolution from sequential to parallel processing, output
persistence, and concurrency tuning.

B.1    Kafka consumption and record normalisation

The consumer subscribes to the ingested-objects Kafka topic and processes two distinct
categories of messages:

      • File-based Records: These contain metadata pointers (an object_id, filename, and
        mime.type) that the consumer uses to locate the raw file on the local filesystem. Files are
        organized by MIME type into corresponding subdirectories (text/, pdf/, image/, audio/)
        under a configurable base path.
      • Database-embedded Records: These carry the full document text inline within the Kafka
        message itself (in fields such as report_text, content, or text), alongside metadata
        including title, classification, and timestamps. These records bypass filesystem resolution
        entirely.

A normalization layer (normalize_record) unifies these heterogeneous message formats into a
stable internal representation before passing the record to the extraction pipeline. This handles
discrepancies such as MongoDB-style _id objects with nested $oid fields, varying timestamp
conventions (camelCase versus snake_case), and differing content field names.

                                                  43
 Value          Subsystem (section)              Role / decision
 0.50           Class retrieval (§4)             Initial cosine floor; admitted too many “vaguely related” classes, superseded
                                                 by 0.72.
 0.72           Class/predicate retrieval (§4)   Retrieval floor (min_score) after the PageRank penalty; classes/predicates
                                                 scoring above it are injected. Env: ONTOLOGY_RETRIEVAL_MIN_SCORE.
 0.80           Subclass expansion (§4)          Trigger: for any class scoring ≥ 0.80, traverse subClassOf one hop
                                                 downward.
 0.78           Subclass expansion (§4)          Score assigned to injected child classes (just above the 0.72 floor, below the
                                                 parent).
 0.80           Predicate vocabulary guard       Embedding snap floor: only predicate synonyms ≥ 0.80 snap to the ontology
                (§4)                             object-property vocabulary; below it the predicate is left verbatim and flagged
                                                 _novel_predicate.
 0.85           Source-text variant miner (§6)   Acceptance threshold 𝜏 for a mined spelling variant.
 0.75           Context-aware        duplicate   Candidate threshold: name similarity ≥ 0.75 (with full context agreement)
                detection (§6)                   to consider a pair at all.
 0.95           Context-aware        duplicate   Auto-merge cell of the decision surface: name similarity > 0.95 and full
                detection (§6)                   contextual agreement on role/organisation/location.
 0.90–0.95      Context-aware        duplicate   Human-review band (high name similarity, partial context).
                detection (§6)
 0.85           Embedding-based resolution       Composite-score auto-merge.
                engine (§6)
 0.60–0.85      Embedding-based resolution       Manual-review band.
                engine (§6)
 0.50           Embedding-based resolution       Codename-candidate (with codename pattern); otherwise distinct.
                engine (§6)

Table 22: Master threshold reference for the extraction and resolution pipeline. The two “0.80” rows and the
two “0.85”/“0.75”/“0.95” rows govern distinct subsystems and are not interchangeable.


B.1.1    Kafka consumer session management and rebalancing tradeoffs
The Kafka consumer is configured with extended timeout values (max.poll.interval.ms of
1,800,000 ms and session.timeout.ms of 300,000 ms) to accommodate the latency inherent in
LLM inference on large documents without triggering disruptive consumer group rebalances. This
configuration reflects the unique demands of LLM-backed streaming architectures, where individual
message processing times can exceed typical Kafka consumer expectations by orders of magnitude
[1, 36].
The session.timeout.ms parameter governs how long the Kafka broker waits before declaring
a consumer dead and triggering a partition rebalance. This value represents a critical tradeoff in
LLM-backed consumer architectures:
Table 23: Kafka Session Timeout Tradeoff Analysis

Config             Advantages                                          Disadvantages
300 s              Long-running LLM inference calls                    Stale consumer sessions block new
(current)          complete without triggering                         consumers from acquiring partitions
                   rebalances; essential for large                     for up to 5 minutes after an unclean
                   multi-chunk PDF extractions                         shutdown
45 s (Kafka        Fast recovery after consumer crashes;               LLM calls exceeding 45 seconds cause
default)           new instances acquire partitions within             the broker to evict the consumer
                   seconds                                             mid-processing, resulting in rebalance
                                                                       storms and duplicate processing
60–90 s            Reasonable recovery time (∼1–1.5                    May still trigger rebalances on very
(balanced)         minutes) while accommodating most                   large documents requiring extended
                   single-chunk LLM calls                              multi-phase extraction

The cost of the long timeout is visible on unclean shutdown: the broker keeps the stale session alive

                                                        44
until it expires, so a replacement consumer was observed waiting ∼6.5 minutes (the 300-second
timeout plus rebalancing overhead) before receiving its first message. The practical guidance follows
the inference-latency profile: 60–90 s suffices for fast local models with small context windows, while
300 s remains necessary for multi-phase extraction of large documents, where a single mid-extraction
eviction costs far more than a slow recovery.

B.2   Evolution from sequential to parallel processing

Sequential processing proved insufficient for large corpora; the redesigned consumer runs a
ThreadPoolExecutor with tuned worker and in-flight limits (Section B.4, Table 24), and the
resulting out-of-order completions are kept operator-readable by the sequence-ordered output buffer
of Fig. 12.

B.3   Extraction output persistence

Extraction results are saved as individual JSON files, enveloped with traceability metadata (e.g.,
source file, MIME type, timestamps). The inclusion of the dedup_candidates array in this
payload facilitates subsequent downstream processing or human review.

B.4   Concurrency and parallelism configuration

Two independent concurrency domains govern throughput: document-level workers in the Kafka
consumer (ThreadPoolExecutor) and asynchronous embedding backfill after graph ingestion.
Table 24 summarises the knobs and their tuned values.
Table 24: Concurrency knobs across the two parallelism domains.

       Domain       Knob                        Default → tuned   Rationale
       Documents    WORKER_COUNT                    10 → 4        LLM saturation, OOM on large PDFs
       Documents    MAX_IN_FLIGHT_TASKS             40 → 16       bounds memory; tracks workers
       Embeddings   EMBED_BATCH_SIZE                   20         texts per batched API call
       Embeddings   EMBED_PARALLEL_BATCHES              5         concurrent calls (semaphore)


Each worker holds one document’s full text plus its extracted entities in memory for the duration of
multi-phase extraction; ten concurrent large PDFs exhausted both system memory and the vLLM
request queue, motivating the reduction to four workers (the in-flight cap followed automatically,
40 → 16). The embedding backfill achieves up to 100 embeddings per round over only five HTTP
connections; items that fail within a batch are retried individually via single-item create() calls to
maximise recovery.

C     Field issue log
Beyond the data-quality fixes of the main text, development surfaced infrastructure and integration
issues catalogued here for practitioners. The source-truncation bug is analysed in the main text and
omitted here.

C.1   Issue 2: parallelism-induced resource exhaustion

Ten concurrent workers saturated the local LLM endpoint (request-queuing timeouts) and exhausted
memory when several >30-page PDFs were in flight simultaneously. The resolution, reducing
WORKER_COUNT to 4 with the in-flight cap following automatically, is detailed in Section B.4
(Table 24).

C.2   Issue 3: binary PDF routing information loss

The original PDF handling used a single heuristic (_should_use_text_pdf_path()) that
examined overall page statistics (non-empty page ratio, average character count) to make a binary
text-or-OCR decision for the entire document. Mixed PDFs, e.g. a 45-page document with 30 text

                                                   45
pages and 15 scanned appendix pages, would be routed entirely through one path, losing either the
scanned content or the text quality.


Resolution. Implemented the per-page OCR classification system (Eq. (1), Section 5.1) that
classifies each page independently and routes text, OCR, and skip pages to their optimal extraction
paths. The legacy heuristic is retained as a fallback only when the new classifier reports zero usable
pages.

C.3   Issue 4: vector-drawn text misclassification

Certain PDF pages render text as vector paths (drawing primitives) rather than font glyphs. These
pages report zero extractable characters via get_text("text") despite containing readable text
content. Without Signal 5 (drawing count > 200), such pages were classified as skip and their
content was lost.


Resolution. Added drawing count as Signal 5 in the per-page classifier. Pages with more than
200 drawing primitives but zero extractable characters are routed to the OCR path, where the vision
model can recover the text from the rendered page image.

C.4   Issue 5: xref images missed by block analysis

Some PDFs embed images via cross-reference tables that do not appear in the structured block
analysis obtained from get_text("dict"). Pages with such images were incorrectly classified as
text despite being dominated by scanned content.


Resolution. Added Signal 3 (xref image coverage via get_image_info()) as a secondary
image detection mechanism.     This signal is evaluated only when xref images exist
(get_images(full=True)) to avoid unnecessary computation on text-only pages.




                                                 46

