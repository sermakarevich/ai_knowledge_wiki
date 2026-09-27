> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# OntoExtend: A Framework for Requirement-driven and Scalable Ontology Extension with LLMs — In Plain Language

## What is this about?

An ontology is a shared map of what things exist in a domain and how they relate — for example, what counts as a material, a component, or a manufacturing step.

As needs change, that map must grow: new questions come up that the old map cannot answer. Doing this growth by hand is slow and error-prone.

OntoExtend is a helper that grows an existing ontology automatically. You give it a new requirement written as a plain question (a "competency question", such as "what was this material component meant to represent?"), plus the ontology you already have. It drafts the missing piece in a standard machine-readable format so it can be plugged back into the map.

It was tested on 39 such questions from two real settings: the public Onto-DESIDE project about circular-economy data, and an internal Bosch manufacturing ontology.

In short: instead of asking an LLM to "write an ontology from scratch", OntoExtend asks it to "fill in this one blank, using these existing pieces, so this question becomes answerable".

The headline result: drafts answered every test question, added almost no junk, and engineers judged the best ones nearly ready to merge.

## Why does it matter?

Large language models (LLMs) are good at drafting structured knowledge, but they have two practical problems here.

First, real ontologies are big — one test module ran to about 75,000 tokens, far more than you want to paste into a prompt. That is slow and expensive.

Second, dumping everything in confuses the model: irrelevant details push it toward off-target or inconsistent answers, including invented terms and broken links.

Earlier tools mostly grew simple taxonomies (lists of parent-child terms), needed a human in the loop, and were rarely checked rigorously.

OntoExtend matters because it only shows the model the small slice of the ontology that is relevant to the current question, keeps new drafts anchored in existing terms, and checks the result with structural tests, functional tests, and engineer review.

## How does it work?

Think of it as three stations on an assembly line, handling one question at a time.

**1. Retriever — find the relevant slice.** Every class, property, and shape in your ontology is turned into a short text card (name, description, domain, range, parent/child links, original code) and stored in a fast search index. When a new question arrives, the system finds the top 20 most similar cards. This compact slice becomes the model's context.

**2. Extender — draft the missing piece.** The LLM receives the question plus those retrieved snippets as read-only background, with strict instructions: reuse existing terms, do not redefine them, follow the required style. A two-stage checker then screens the draft: is the code syntactically valid, and does it obey the project's conventions (for example, every new term needs a label and description, or must use a particular shape format)? Bad drafts are retried or flagged.

**3. Integrator — plug it in.** The accepted draft is cleaned up (duplicates and repeated prefixes removed) and merged into the ontology. Optionally it can be added to the search index so later questions build on earlier drafts — though this was switched off during testing so each question could be judged fairly.

The test setup itself was clever: researchers deleted a real class plus its connected properties, wrote a question asking what the deleted part was for, and checked whether the tool could reconstruct something equivalent.

## Where can this be used?

Any team that maintains a living knowledge map and faces a steady stream of new requirements.

- **Manufacturing and engineering:** extend a factory ontology when new materials, parts, or process steps appear, without rewriting the whole model.
- **Circular economy and sustainability:** grow interoperability ontologies (like Onto-DESIDE) as new reuse, recycling, or reporting questions arise.
- **Biomedical and enterprise knowledge graphs:** add new concepts while staying consistent with existing naming and modelling patterns.
- **Requirements triage:** because vague questions produce visibly weaker drafts, the tool's struggles can flag unclear requirements that need rewriting before engineers invest effort.
- **Onboarding aid:** newcomers can propose an extension from a question and learn the project's naming and modelling style from the retrieved examples.

The main condition: it works best when the starting ontology is tidy and the question is precise. Open-ended questions ("model something about sustainability") need much more human cleanup than focused ones ("add this sensor type with these properties").

A good rule of thumb from the study: if the draft comes back clean and tightly linked to existing terms, the requirement was probably well written; if it comes back with loose, unconnected, or oddly named pieces, rewrite the question first.

## Conclusions & takeaways

- Extensions were nearly always syntactically valid, introduced no serious new modelling pitfalls, answered all 39 test questions correctly, and added under 2% unnecessary elements — far less clutter than the ~30% reported for a prior approach.
- Human judges told a split story: Bosch industry drafts (tightly written questions) scored about 4.9/5 for correctness and 4.5/5 for completeness — minor or no edits needed. Onto-DESIDE drafts (broader questions) scored about 3.7/5 and 3.0/5 — moderate revision needed.
- The authors blame question quality, not the tool: open questions force the model to guess modelling decisions, while precise questions let it simply render correct axioms.
- Practical win: sending only a compact retrieved slice cuts waiting time and API cost versus sending tens of thousands of tokens.
- Limits: only two domains tested, only two OpenAI models tried, and public ontologies might partly overlap with LLM training data. Treat OntoExtend as a drafting assistant — shifting work from writing axioms by hand to quick review and targeted fixes — not as a fully autonomous modeller.

## Jargon decoder

| Term | Plain definition |
|---|---|
| Ontology | A shared, machine-readable map of concepts in a domain and how they relate. |
| Ontology extension | Growing an existing map to cover new requirements instead of starting over. |
| Competency question (CQ) | A plain-language question the ontology should be able to answer; used here as the requirement. |
| Fragment | A small self-contained bundle of new statements drafted to answer one question. |
| Retrieval-augmented generation (RAG) | Looking up relevant background documents first, then letting the LLM write using only that slice. |
| Class / Property | A category of things (e.g. Material) and a named relationship or attribute (e.g. has part). |
| Axiom | A single formal statement in the ontology, such as "every sensor has a location". |
| Turtle | A compact text format for writing such statements so tools can read them. |
| SHACL shape | A rule template that says what data for a given type must look like. |
| OOPS! pitfalls | A scanner that flags common modelling mistakes, ranked from minor to critical. |
| Superfluous element | An extra class or property the draft added but nothing actually needs. |
| Domain / Range | Declarations saying which kind of thing a relationship starts from and points to. |
