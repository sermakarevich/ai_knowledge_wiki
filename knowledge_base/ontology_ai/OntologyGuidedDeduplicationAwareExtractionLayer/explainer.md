> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# An Ontology-Guided, Deduplication-Aware Extraction Layer for Knowledge Graph Construction from Heterogeneous Documents — In Plain Language

## What is this about?

This paper describes a working software layer that reads a live stream of messy, mixed documents — PDFs, spreadsheets, slides, Word files, scanned images — and turns them into a clean, searchable knowledge graph: a network of people, organisations, places, equipment, and how they relate.

The core problem it tackles: large language models (LLMs) are good at pulling facts out of text, but they do it inconsistently. The same person shows up under five different spellings. Relationship names vary wildly ("commands" vs "has subordinate formation"). Two different people with the same name risk being silently merged into one. Type labels fracture across documents.

The answer here is not a new AI model. It is an architecture that constrains and repairs an ordinary model's output: guide it with the relevant slice of a formal schema (ontology), handle each file format properly, then clean, merge, and deduplicate everything through a five-stage pipeline.

The headline result on intelligence-style test documents: search recall rose from about 70% to 95%, with zero false merges — and on one tricky scanned naval document, hallucinated entities fell from 174 to nearly zero.

A concrete sense of scale: a single 45-page report yielded 579 entities and 540 relationships before cleaning, shrinking to roughly 400 entities with zero self-loops and zero broken references after the pipeline's fixes.
On scanned image-only documents, wall-clock time fell about 30% while vessel-class recall nearly doubled when chunk sizes were tuned.

## Why does it matter?

Anyone who has tried to build a knowledge base from real documents knows the pain: the extraction looks fluent, but the graph underneath is a mess. Duplicates inflate counts (one report went from ~224 real people to 315 entries because "Colonel Mario Chavez" and "Mario Chavez" counted twice). Relationships duplicate or point the wrong way. A single mis-merge can attribute one person's actions to another.

Three ideas in this paper matter beyond its original setting:

- Guiding the model with just the schema slice it needs cuts prompt cost by roughly 94% versus dumping a whole domain catalogue into every prompt — about 11,200 tokens down to ~700 on a representative document.
- Deterministic, no-extra-AI-cost cleanup rules (alias expansion, spelling-variant mining, name scoring) do most of the deduplication work for free, before any expensive embedding comparison.
- A "never merge on names alone" safety rule — if hard facts like role, organisation, or ID conflict, the pair stays separate no matter how similar the names look — prevents the worst errors.
- The running example the paper uses: two similar names scoring 0.85 alike stay separate because their roles conflict — exactly the case a naive similarity threshold would get wrong.
- Cleaning is cheap insurance: relationship-name variants (INFILTRATED vs infiltrated vs INfiltrated) collapse to one edge, and qualifier details from duplicate edges are unioned rather than lost.

## How does it work?

Think of it as an assembly line with five stations, fed by a live document stream (Kafka) and powered by a locally hosted, schema-tuned 9B-parameter model:

1. **Read every format correctly.** A per-page PDF classifier looks at six structural signals (extractable text, image coverage, hidden images, drawing shapes, and so on) and sends each page to text extraction, OCR/vision, or skip. A 45-page file with 30 digital pages and 15 scans gets each page handled optimally instead of one blunt choice for the whole file. Spreadsheets get a plan-then-execute treatment.

2. **Guide the model with the right schema slice.** Instead of pasting a giant static catalogue into the prompt, the system embeds chunks of the document, searches a live graph database of the schema for the nearest classes and relationships, and injects only those (~700 tokens). Refinements help it find the specific terms: a compact proper-noun query ("12th Battalion | Operation Vijay") matches terse schema labels better than flowing prose; a high-confidence general match also pulls in its more specific children (e.g. Organisation → SecurityForce); and predicted relationship names are snapped to the official vocabulary, with unknown ones flagged for human review.

3. **Extract in two passes.** Pass one pulls out entities plus a first draft of relationships. Pass two re-reads the text with the full entity list and focuses purely on relationships, including qualifiers like dates and context. A quality gate watches for suspicious output (e.g. one relationship type dominating the document) and can force a re-run.

4. **Clean and merge across chunks.** Long documents are processed in overlapping chunks, so the pipeline normalises relationship names to a controlled vocabulary (fixing typos like "surveiled"), deletes self-loops where source equals target, fixes mis-typed entities by name clues ("Leviathan Submarine" is equipment, not a person), strips titles to form canonical keys, and unifies chaotic IDs (per1, per1_2, per_087) into one scheme (per_001…).

5. **Deduplicate carefully, in layers.** Six rule-based algorithms expand aliases ("Elena Petrov" → "E. Petrov", "E.P."), mine the source text for spelling variants, and score name similarity on five signals (spelling, sound, tokens, and more). A merge is valid only if names are similar AND all shared context agrees; any conflict blocks the merge. An optional embedding layer then compares remaining candidates by meaning, with a hard-conflict guard on IDs and key attributes that no similarity score can override. Borderline cases go to a human with full provenance, never silently merged.

Behind the scenes, candidate pairs are found efficiently — by combining vector-similarity search with phonetic blocking — so the system avoids comparing every entity against every other one.
Relationship duplicates fold together too: three extractions of the same employment link collapse into one edge, keeping every qualifier from each copy.
The whole pipeline degrades gracefully: if the schema database is unreachable for 60 seconds, extraction continues un-guided rather than stalling, and any brand-new types the model emits are flagged for human schema review.

## Where can this be used?

The paper's testbed is intelligence analysis — turning piles of reports into a queryable graph of who commands what, who funds whom, where units deployed. But the authors explicitly generalise:

- **Compliance monitoring** — linking people, companies, and transactions across filings and leaks without conflating same-named individuals.
- **Investigative journalism** — assembling person/organisation networks from mixed document dumps.
- **Enterprise knowledge management** — unifying contracts, spreadsheets, slides, and scans under one governed schema.

Each component is designed to be adoptable independently: schema-slice retrieval, the per-page OCR router, or the deduplication rules can bolt onto an existing pipeline.

Concretely: a compliance team could adopt just the conflict-guarded deduplication without changing its models; a newsroom could adopt just the format handlers and schema grounding; an enterprise team could start with the cleaning stages that fix titles, IDs, and self-loops.

## Conclusions & takeaways

- Fluency is not consistency: raw LLM extraction needs a constraining schema, format-aware reading, and a repair pipeline before it is graph-ready.
- Small, targeted schema guidance beats giant static prompts: ~94% fewer catalogue tokens, and more accurate types and relationships.
- Most deduplication is cheap: deterministic alias, spelling, and scoring rules with zero extra model calls lift recall from ~70% to ~95%.
- Safety must be structural, not a threshold tweak: a non-overridable conflict guard plus human review of borderline pairs is what holds false merges at zero.
- Quiet bugs dominate real pipelines: seven silent defect classes were fixed here, from a one-character text truncation that zeroed all per-chunk relationships, to title-prefix duplication inflating person counts ~30%, to 114 self-loop relationships (21% of one report's edges).
- Dual-use risk is real and named: better person search means misidentification and surveillance harms, contained here by conservative merge policy, provenance on every decision, fictional/synthetic evaluation data, and a governance prescription (authorised analysts, logged queries, legal frameworks).

## Jargon decoder

| Term | Plain definition |
|---|---|
| Ontology | The official catalogue of allowed types and relationships — e.g. what counts as a Person, what "commands" means. |
| Knowledge graph | A database of entities (people, places, orgs) linked by typed relationships, built for searching and querying. |
| Extraction layer | The software stage that reads raw documents and outputs structured entities and relationships. |
| Deduplication / entity resolution | Deciding which mentions refer to the same real thing ("E. Petrov" = "Elena Petrov") and merging them without merging two different people who share a name. |
| Alias expansion | Automatically generating plausible name variants (initials, short forms) so mentions can be matched. |
| Embedding | A numeric fingerprint of a word or passage's meaning, used to find similar items by distance. |
| Retrieval-augmented generation (RAG) | Looking up relevant reference material first, then handing it to the model inside the prompt so its answer stays grounded. |
| Schema / type vocabulary | The controlled list of labels the model is allowed to emit, as opposed to whatever free-form words it invents. |
| Hallucination | Model output that reads plausibly but invents entities or facts not in the source (e.g. 174 phantom "people" read from ship hull numbers). |
| Hard-conflict guard | A safety rule that forbids merging two entities when key facts disagree, regardless of how similar their names are. |
| Provenance | The recorded trail of where each fact or merge decision came from, so it can be audited later. |
| Chunking | Splitting a long document into overlapping pieces the model can process, then stitching results back together. |
