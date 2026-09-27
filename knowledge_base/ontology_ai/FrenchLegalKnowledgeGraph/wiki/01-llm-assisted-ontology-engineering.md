[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# LLM-Assisted Ontology Engineering for a French Legal Knowledge Graph
**In one sentence:** The paper presents a two-stage LLM-assisted workflow that enriches a SEMLEG-based core ontology via open extraction, embedding-based fusion, and property induction on a stratified sample, then uses that ontology to guide closed triple extraction over the full corpus.
## Key points
- Maintenance regulations are hard to exploit in specific cases and to integrate into operational systems such as Computerized Maintenance Management Systems (CMMS).
- The workflow has two stages: (1) ontology engineering from a SEMLEG-based core ontology, and (2) construction of an ontology-grounded French legal knowledge graph via closed extraction over the full corpus.
- The focused corpus contains 6,370 regulatory articles covering 20 topics, built from Légifrance texts filtered via Apave regulatory-guide references; ontology engineering uses a stratified sample of 1,389 articles (~10% of each domain–document title pair).
- Open extraction processes each sampled article with three prompts: entity extraction typed with retained SEMLEG classes (Turtle Light serialization), open-vocabulary triple generation, and topic assignment to maintenanceActivity, anotherLegalActivity, or legalCrossReference.
- Normalization embeds entity and property labels and merges variants with cosine similarity > θE = 0.7 (entities) and θP = 0.7 (properties, grouped by subject–object class pair), keeping the most frequent variant and excluding legal references and numeric labels.
- Property induction samples 5% of fused maintenance triples per property (at least one per signature), splits the sample into 15 batches, and prompts for label, domain, range, evidence, definition, aligned question, and confidence score, formalized into OWL axioms.
- The OpenAI variant induces 75 maintenance-specific properties with 105 signatures versus 44 properties with 59 signatures for Mistral; they share 21 properties and 18 signatures, including appliesTo, composedOf, performedAtLocation, and responsibleFor.
---
## Abstract and problem statement
The paper targets French maintenance regulations, described as "complex legal texts that are difficult to exploit when addressing a specific case and challenging to integrate into operational systems." Most existing LLM legal extraction work is described as "dataset-driven" without "an end-to-end pipeline for moving from legal text to an ontology-grounded knowledge graph." The contribution is "a compact workflow combining LLM flexibility with ontology-based structural constraints, together with a preliminary evaluation of the resulting ontology and KG."

**Covers:** Abstract; 1. Introduction

## Semantic scope and corpus
Competency questions target maintenance obligations: involved actors, affected artifacts, contextual conditions, and legal sources. The starting point retains SEMLEG classes Actor, Action, Artifact, Condition, Source, Location, Reason, Situation, and Time, plus object properties whose domain and range correspond to these classes. References from the Apave regulatory guide are parsed and normalized before retrieving corresponding legal articles and metadata from Légifrance.

| Corpus | Size |
|---|---|
| Full focused corpus | 6,370 regulatory articles, 20 topics |
| Ontology-engineering stratified sample (~10% per domain–document title pair) | 1,389 articles |
| KG construction (population) | complete corpus |

**Covers:** 2. LLM-Assisted Ontology Engineering — Semantic Scope and Corpus

## Open class-guided triple extraction
Each sampled article 𝑎𝑖 with text 𝑥𝑖 is processed with three prompts: 𝜋𝑖𝑒𝑛𝑡 extracts entities typed with retained SEMLEG classes, with "class declarations … injected into the prompt as a compact Turtle Light serialization"; 𝜋𝑖𝑟𝑒𝑙 receives text, entities, and classes and generates triples 𝑇𝑖 "without a predefined predicate vocabulary" where "relation labels are inferred from context, while subject and object classes restrict the plausible domain–range patterns"; 𝜋𝑖𝑡𝑜𝑝𝑖𝑐 assigns each triple to maintenanceActivity, anotherLegalActivity, or legalCrossReference. Prompt templates are linked in the chunk (LegiMaintLex repository).

**Covers:** 2. LLM-Assisted Ontology Engineering — Open Class-Guided Triple Extraction

## Embedding-based fusion
Only triples classified as maintenanceActivity are retained for induction (𝑇maint); other topics are discarded at this stage. Entities are grouped per ontology class as they occur as subject or object; labels are embedded and merged when cosine similarity > θE = 0.7, with the most frequent variant as canonical. Properties are grouped by subject–object class pairs (𝑐𝑒𝑠, 𝑐𝑒𝑜) with the same threshold θP = 0.7, keeping the most frequent variant. The result is the fused set 𝑇maint fused. Legal references and numeric labels are excluded as "unique or context-dependent values."

**Covers:** 2. LLM-Assisted Ontology Engineering — Embedding-Based Fusion of Entity and Property Labels

## Object property induction and resulting ontology
The induction sample takes 5% of triples per property from the fused maintenance set with at least one triple per signature, split into 15 batches; each batch prompt 𝜋𝑘rel_disc receives triples, core ontology, and competency questions and outputs properties with "label, domain, range, textual evidence, definition, aligned question, and confidence score," formalized into OWL axioms. Two variants reuse the same SEMLEG-based core; differences come only from newly induced properties.

| SemLegM ontology variant | OpenAI | Mistral |
|---|---|---|
| # Maintenance-specific properties | 75 | 44 |
| # Maintenance-specific signatures | 105 | 59 |

Shared: 21 maintenance-related properties and 18 signatures, "including appliesTo, composedOf, performedAtLocation, and responsibleFor, which capture recurring relations for applicability, composition, location, and responsibility." Qualitative contrast from the chunk: "OpenAI tends to induce more fine-grained and expressive predicates, including relations for purpose, sequencing, and interaction (e.g., aimsToAction, precededBy, transmittedTo)" while "Mistral tends to produce a more conservative vocabulary oriented toward normative and compliance relations (e.g., hasModality, verifiedBy, performedUnderCondition)." Variants are kept separate "to compare how different ontologies affect downstream Knowledge Graph construction."

**Covers:** 2. LLM-Assisted Ontology Engineering — Object Property Induction from Triples; Resulting Ontology (Table 1)
