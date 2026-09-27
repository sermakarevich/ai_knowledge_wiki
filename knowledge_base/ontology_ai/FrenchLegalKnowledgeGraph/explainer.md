> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# LLM-Assisted Ontology Engineering and Construction of a French Legal Knowledge Graph — In Plain Language

## What is this about?

This paper tackles a practical headache: French maintenance regulations are long,
scattered across legal codes, and hard to apply to one concrete case.

The authors build a bridge from raw legal text to a structured, searchable map
of what the law requires. That map is called a knowledge graph.

The method has two stages. First, teach a computer a vocabulary of maintenance
law — who does what, to which equipment, under which conditions, citing which
legal source. Second, use that vocabulary to read thousands of articles and
extract machine-readable facts.

The starting vocabulary reuses an existing legal model called SEMLEG, with
broad categories such as Actor, Action, Artifact, Condition, and Source.

The corpus is 6,370 regulatory articles from Légifrance, covering 20 topics,
collected by following references in an Apave regulatory guide. A smaller
sample of 1,389 articles is used to design the vocabulary; the full corpus is
used to populate the graph.

Two versions of the pipeline are tested side by side: one built with OpenAI
models, one with Mistral models, using the same prompts.

## Why does it matter?

Maintenance teams and facility managers must prove they follow the law, but
legal texts are not written for day-to-day operations.

Today it is hard to answer simple operational questions — who must inspect
this lift, how often, under which conditions, and which article says so —
without manual legal research.

Existing AI research on legal text is often dataset-driven: it tests extraction
on benchmarks but does not deliver a working pipeline from text to a usable
knowledge base.

This work also matters because it connects legal knowledge to operational
systems such as Computerized Maintenance Management Systems (CMMS), the
software that schedules and tracks maintenance tasks.

A structured graph makes obligations searchable, linkable, and auditable,
instead of buried in paragraphs of legal prose.

The comparison of two model families also shows how much the choice of AI
model shapes the resulting vocabulary — a useful warning for anyone building
such systems.

## How does it work?

Think of the workflow as: draft a dictionary, clean it up, then use it to
read the whole library.

Step 1 — Open extraction on a sample. Each of the 1,389 sampled articles is
processed with three prompts: find the entities (people, equipment, actions)
typed with SEMLEG classes; propose relation triples in the model's own words
(no fixed predicate list); then label each triple as maintenanceActivity,
anotherLegalActivity, or legalCrossReference.

Step 2 — Fusion (deduplication). The raw output contains many spelling and
phrasing variants of the same thing. Labels are turned into embeddings and
merged when their cosine similarity exceeds 0.7, keeping the most frequent
variant. Only maintenance-related triples are kept for the next step.

Step 3 — Property induction. From the cleaned triples, the system samples 5%
of examples per relation (at least one per subject–object class combination),
split into 15 batches. Each batch is shown to the model with the core ontology
and guiding questions, and the model proposes formal properties with a label,
domain, range, definition, evidence, and confidence score, converted into OWL
axioms. This yields the SemLegM ontology: 75 properties with 105 signatures
for OpenAI, 44 properties with 59 signatures for Mistral, with 21 properties
shared (e.g., appliesTo, composedOf, performedAtLocation, responsibleFor).

Step 4 — Closed extraction over everything. The finished ontology becomes a
fixed vocabulary, and the pipeline reads all 6,370 articles to extract
conforming triples, followed by another round of fusion.

Step 5 — Evaluation. Fusion preserves every extracted relation statement
(75,870 for Mistral, 51,657 for OpenAI) while sharply cutting duplicates:
entities fall from 74,035 to 20,827 for Mistral, predicates from about 2,640
to 500. Quality scores show 100% valid JSON output and ~99.98% valid class
usage, but only 50–73% of triples reuse an expected domain–range combination.

## Where can this be used?

Maintenance compliance is the direct use case: look up which actor is
responsible for which check, on which equipment, at which location, and under
which condition, with the legal source attached.

CMMS integration is the operational payoff — feeding legal obligations into
scheduling, checklists, and audit trails instead of keeping law and operations
in separate worlds.

Legal question-answering is another path: the authors test SPARQL queries
behind typical competency questions (actor roles, legal justifications), a
stepping stone toward GraphRAG assistants that answer with citations.

Regulatory monitoring fits naturally too: as legal provisions change, the
pipeline can be re-run to update the graph rather than rewriting a handbook.

The approach transfers beyond maintenance: any domain with dense regulation
(safety, environment, energy) could reuse the two-stage recipe of open
vocabulary discovery followed by ontology-guided extraction.

## Conclusions & takeaways

Large language models are flexible readers, but without a controlled
vocabulary they produce messy, duplicated output. The ontology plus fusion
steps turn that raw output into something compact and usable.

OpenAI produced a richer, more fine-grained vocabulary (purpose, sequencing,
interaction); Mistral produced a smaller, compliance-oriented one (modality,
verification, conditions). Neither is automatically better — the choice
depends on the application.

Remaining errors come mostly from misclassified entities (e.g., a legal source
typed as equipment) and from reusing known predicates with new class
combinations, plus quirks like negations baked into predicate names.

The authors propose next steps: iteratively fold new valid combinations back
into the ontology, add formal validation such as SHACL, build a GraphRAG
consultation layer, and keep the graph in sync as the law evolves.

Bottom line: a compact LLM-plus-ontology workflow can convert thousands of
legal articles into a queryable maintenance knowledge graph — promising, but
still in need of validation and refinement before operational use.

## Jargon decoder

| Term | Plain definition |
|---|---|
| Ontology | A formal dictionary of allowed categories and relations in a domain. |
| Knowledge graph | A network of facts (subject–relation–object) linked to that dictionary. |
| Triple | One fact with three parts, e.g., technician — inspects — lift. |
| SEMLEG | An existing legal ontology the authors reuse as a starting point. |
| CMMS | Maintenance management software that schedules and tracks upkeep tasks. |
| Open extraction | Letting the AI invent relation names freely instead of picking from a list. |
| Closed extraction | Forcing the AI to use only relations from the finished ontology. |
| Fusion | Merging duplicate labels that mean the same thing into one canonical term. |
| Embedding | A numeric representation of a word's meaning used to measure similarity. |
| Domain and range | The allowed subject type and object type of a relation. |
| Signature | One specific domain–range combination for a given relation. |
| SHACL | A standard language for writing validation rules over a knowledge graph. |
