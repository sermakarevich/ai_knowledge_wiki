> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Natural Language Access to Domain-Specific Metadata: A Reusable Framework for LLM Query Generation — In Plain Language

## What is this about?

Researchers sit on huge archives of domain metadata — in this paper, an MRI
neuroimaging archive with 80 studies, 2,000 experiments, and 180 TB of data.
Answering everyday questions ("which experiments ran in study 101?",
"which subjects are over 42?") normally means writing SPARQL or SQL,
which requires both query-language skill and insider vocabulary.

The authors propose an ontology-first shortcut. First, write down the
domain's vocabulary and meanings once, in a formal OWL ontology with
readable names and plain-English descriptions. Then run a pipeline
that copies archive metadata (scanner headers, registries, participant
records) into a knowledge graph shaped by that ontology.

On top sits NLKGQ, a reusable, domain-agnostic harness: it pastes the
whole ontology plus short instructions into an LLM prompt, the LLM writes
a SPARQL query from the user's plain-English question, and the harness
runs it against the graph. No fine-tuning, no retrieval augmentation,
no multi-agent orchestration — just zero-shot generation. A web app shows
the generated query, explains it, and lets users download results.

On a 21-question test set built with domain experts, the best setup
answered every question correctly (21/21, 100%).

## Why does it matter?

On simple demo schemas LLMs already score above 90%, but on real
enterprise schemas with hundreds of tables, GPT-4o has been reported
at 0%. How knowledge is structured matters as much as which model you use.

This work shows the structure can be engineered deliberately — and cheaply.
Readable names and comments cost nothing extra when you must design the
vocabulary anyway, yet they dominate accuracy: more than model choice,
more than prompt tricks. Stripping comments alone cut accuracy from
100% to 81%; replacing readable names with generic codes collapsed it
to 5–19%.

It also matters for privacy. Because the demo involves human-subject
data under GDPR, everything must run on local institutional hardware,
not a cloud API. The paper shows a quantized 27B model on several-
generations-old GPUs still hits 100%, so modest local setups suffice.

Finally, both the framework and the process are meant to be reused:
swap in a new ontology and extraction pipeline, and the same harness,
web app, and test driver work for a different archive.

## How does it work?

1. Capture the vocabulary. Domain experts formalize entities, properties,
   and relationships in OWL, following six naming principles: full English
   words, consistent `has...` patterns, descriptive relationship names,
   explicit domain and range, natural-language annotations, and no opaque
   codes or auto-generated identifiers.
2. Build the knowledge graph. A Python pipeline maps each metadata source
   to ontology terms and materializes about 10 million triples, loaded
   into an Apache Jena Fuseki SPARQL server.
3. Ask in plain language. The NLKGQ server builds a system prompt from
   generic SPARQL instructions, the full ontology in Turtle format
   (about 80 KB / 18K tokens), and a short domain-specific "rider"
   fixing recurring mistakes. Small harness fixes clean up the output:
   strip thinking blocks, extract code from markdown, repair prefixes,
   and optionally retry once or twice on syntax errors.
4. Iterate like testing software. Ontology, test questions, and prompt
   rider co-evolve: each test run exposes a confusing name or recurring
   LLM mistake, the team renames the property or adds a rider rule,
   and re-runs the suite. No ML, database, or SPARQL expertise required —
   just domain knowledge and comfort with iterative testing.
5. Measure rigorously. A test driver sweeps combinations of model,
   temperature, prompt, ontology representation, and backend (over
   16,000 runs), comparing generated-query results against reference
   answers. An automatic OWL-to-SQL converter builds an equivalent
   relational schema so SPARQL and SQL can be compared on identical
   questions, data, and models.

The headline numbers: 8 local Qwen3 variants (8B–35B) tested; dense 27B
at temperature 0.0 reaches 100% on SPARQL. The auto-generated SQL version
of the same data peaks at only 57% (12/21).

## Where can this be used?

- Any research facility, hospital, company, or agency with a large
  metadata archive whose users cannot or will not learn query languages.
- Privacy-constrained settings (hospitals, human-subject studies) where
  models must run locally on modest, older, or low-power hardware.
- Teams practicing FAIR data: the ontology doubles as reusable,
  machine-readable documentation of the domain.
- Groups that want transparent AI: the web app displays each generated
  query, offers a plain-English explanation, and exports CSV or Python,
  so users learn which phrasings work and can audit answers.
- Future domains beyond neuroimaging: the pattern is the same each time —
  model the vocabulary, write extraction code, iterate on test questions.

The caveat: the comparison favors SPARQL only for SQL schemas generated
mechanically from the ontology. A hand-designed relational schema with
expert views and documented joins would likely narrow the gap.

## Conclusions & takeaways

- Design the vocabulary for the LLM, not just for the machine: readable
  names plus comments and synonyms are the biggest lever on accuracy.
- Keep one source of truth: ontology, extraction logic, and prompt rider
  designed together beat any one of them optimized alone.
- Prefer structure the LLM can traverse: class grouping, domain/range
  declarations, and two-way (inverse) relationships explain much of the
  100%-vs-57% SPARQL-over-SQL gap on auto-generated schemas.
- Small and simple can win: the plainest prompt, temperature 0.0, dense
  27B over 35B mixture-of-experts, and Q8 quantization with no accuracy
  loss all held up on old local GPUs.
- Limits to remember: one MRI domain, 21 co-evolved test questions,
  Qwen3-family models only, and auto-generated (not expert-designed)
  SQL baselines — so cross-domain and broader model follow-ups are needed.

## Jargon decoder

| Term | Plain definition |
|------|------------------|
| Ontology (OWL) | A formal, machine-readable dictionary of a domain: what things exist, how they relate, and what each term means. |
| Knowledge graph (KG) | A database of facts stored as subject–predicate–object triples (e.g., "experiment-5 belongs-to study-101"). |
| SPARQL | The standard query language for knowledge graphs; you describe a pattern and it returns matching facts. |
| SQL / DDL | The standard query language for relational tables (SQL); DDL is the part that defines tables and columns. |
| NLKGQ | The paper's reusable harness: turns a plain-English question into a query via an LLM and runs it. |
| Zero-shot | The LLM sees the ontology and instructions but no worked examples for the specific question. |
| ETL pipeline | Extraction code that pulls metadata from raw sources, translates it into ontology terms, and loads it. |
| Competency questions | A test set of realistic questions with known-correct answers, used to grade the system. |
| Prompt rider | A short list of domain-specific extra instructions appended to the prompt to fix recurring errors. |
| Inverse property | A relationship stored so it reads naturally both ways (study-has-experiment / experiment-of-study). |
| Quantization (Q8/FP8) | Compression of a model so it runs on smaller hardware, with little or no accuracy loss here. |
| EAV schema | An alternative table layout storing one fact per row (entity, attribute, value); compact but harder for LLMs here. |
