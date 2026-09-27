> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Natural Language Knowledge Graph Query Execution: Leveraging Controlled Semantics in the LLM Context Window — In Plain Language

## What is this about?

In plain terms: this paper asks how to get a language model to answer
ordinary questions by writing correct database queries — first try, no examples, no retries.
The setting is a knowledge graph: facts stored as linked triples (e.g. "paper X — has author — person Y").
The query language is SPARQL, powerful but picky about exact names and types.
The proposed system is called NLKGQ. You ask in English, the model writes one SPARQL
query in a single call, and that query runs against the database — no fine-tuning,
no few-shot examples, no multi-step agent loop, no separate entity-linking step.
The key idea is "controlled semantics": instead of loose prose or raw schema names,
the context window gets the complete domain ontology in OWL, where every term
declares exactly what it connects to.
Tested on DBLP, SemOpenAlex, and a neuroimaging metadata store, it reaches 89.9%
Match on 1,000 DBLP questions, 98/100 on SemOpenAlex, and 100% on 21 neuroimaging questions.

## Why does it matter?

Plain-language database questions usually fail for a boring reason: the model
guesses relationships that do not exist, or confuses two similar names.
Example: in DBLP's native vocabulary, one predicate returns a venue name as plain
text and a near-identical one returns the venue as a linkable entity — and nothing
in either name says which is which. A guessing model picks wrong.
Common fixes each cost something: fine-tuning is slow and can degrade other skills,
multi-call exploring agents are expensive and fragile, retrieval pipelines add moving
parts, and informal schema dumps leave the model to invent missing connections.
This work tests a simpler claim: give the model formally typed meanings up front, and
a modest open-weight model beats bigger or more complicated setups. The stated hierarchy:
formal concept transfer > model architecture > model scale > prompt engineering.
It is also a benchmark cautionary tale: the same system scores ~17.5% on one DBLP
benchmark version and 79.0% on the repaired version — a ~61.5-point swing caused
by defects in the test itself, not the system.

## How does it work?

Think of it in four parts: the prompt, the ontology, the rider, and (when needed) the wrapper.
**1. One call, zero examples.** Each question triggers exactly one model call at temperature
0.0. The system prompt holds SPARQL instructions, the full OWL ontology, a short domain
"rider," then the question. The answer is cleaned (fences and reasoning traces stripped)
and executed directly.
**2. The ontology carries the meaning.** OWL terms are "narrow" where English is "wide."
Each property declares domain and range (what it connects), each class sits in a hierarchy
(so "Publication" covers articles, conference papers, books without listing them), and each
term is typed as entity-link (a join) versus literal value (a filter). That typing maps
almost directly onto query structure.
**3. The rider holds stable conventions.** Small durable query habits live in the rider,
not the ontology. The paper warns against prose as incremental repair: patching one
misunderstanding in words tends to break unrelated queries — "whack-a-mole" (concept smearing).
**4. Wrappers tame messy vocabularies.** Where native vocabulary is opaque, the team writes
a clean wrapper ontology with readable typed names (e.g. separate terms for "venue name as
text" vs "venue as entity", explicit author-signature links). The model only sees the wrapper;
a deterministic rewriter translates the query into native predicates before execution, without
changing the endpoint. One wrapper term can expand into several native triples. The DBLP
wrapper federates DBLP + OpenCitations under one vocabulary; the SemOpenAlex wrapper flattens
intermediaries like Authorship and OpenAccess into direct properties.
Worked example: asked for 2024 author signatures in a given venue, the model writes a short
query in clean `dblpx:` terms (venue, year, signature links, sorted by publication); the rewriter
swaps in native `dblp:` predicates. The model never sees the confusing native names.
The effect is large: on 1,000 DBLP questions Exact-match rises 56.0% → 81.3% (+25.3 points)
and Match rises 15 points; a ten-model sweep (Qwen, Gemma, Mistral, Llama) converges near
90% Match for the two strongest dense models.
The team also repaired the benchmark as DBLP-QuAD 3.1: removing non-deterministic
LIMIT-without-ORDER-BY clauses, fixing broken references and predicates, replacing 122
"echo" queries that just repeated an answer URI, rewriting ambiguous machine-generated
questions, and documenting the hidden OpenCitations dependency (~71% coverage). Every repair
was logged per case.

## Where can this be used?

- **Scholarly search.** Ask for papers by venue/year, co-authorship, or citation links across
  DBLP + OpenCitations without learning SPARQL or native schema quirks.
- **Other curated graphs.** Same recipe reached 98/100 on SemOpenAlex (baseline 86/100).
- **Lab and domain metadata.** 100% on 21 neuroimaging competency questions — vs 43% for SQL
  over an auto-generated schema, 57% with ontology notes in column comments.
- **Anywhere the schema is the hard part.** The same mapping problem appears in SQL, API, and
  code generation: a clean typed vocabulary plus deterministic translation beats piling on prose.
Out of scope: resolving ambiguous names to entities (benchmark passes URIs in brackets),
ranking beyond 44 kept top-k queries, federated calls outside the wrapper (DBpedia/Wikidata),
and citation lookups capped by 71% coverage — the largest remaining error sources.

## Conclusions & takeaways

- Formal typed vocabulary beats informal description: full OWL hit 100% on neuroimaging
  metadata vs 5% for bare graph structure and 81% for OWL without comments.
- One careful call beats many clever ones: single-call zero-shot outperformed fine-tuning,
  agentic exploration, and retrieval pipelines on the tested benchmarks.
- Clean vocabulary + mechanical translation is the portability trick (+25.3 Exact points on DBLP).
- Benchmarks can dominate measured progress: fixing references moved SPINACH F1 ~17.5% → 79.0%
  with no system change — distrust headline scores on unexamined benchmarks.
- Honest limits: Match allows supersets (stricter Exact: 81.3%), wrappers are hand-designed,
  full ontology per call strains context windows, prose tweaks stay unreliable for concepts.

## Jargon decoder

| Term | Plain definition |
|---|---|
| Knowledge graph | A database of facts stored as linked subject–relation–object triples. |
| SPARQL | The standard query language for knowledge graphs; precise but unforgiving. |
| Ontology (OWL) | A formal vocabulary file declaring classes, relations, and their allowed types. |
| Controlled semantics | Schema terms whose meaning is declared in machine-readable form, not prose. |
| Domain and range | Declarations of what kinds of things a relation goes from and to. |
| ObjectProperty vs DatatypeProperty | Whether a relation links to another entity (a join) or holds a literal value (a filter). |
| Wrapper ontology | A clean readable vocabulary the model sees, mechanically translated to native terms. |
| Deterministic rewriter | A fixed rule-based translator from wrapper queries to native queries; no guessing. |
| Domain rider | A short appendix of stable query conventions kept separate from the vocabulary. |
| Match vs Exact | Match: answer contains expected rows (supersets allowed); Exact: rows match precisely. |
| Zero-shot, single-call | No examples, one attempt per question — no retries or agents. |
| Concept smearing | Natural-language words are semantically "wide"; formal terms are "narrow" and precise. |
