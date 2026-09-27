> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# NLKGQ paper body — controlled semantics, wrappers, and benchmarks
**In one sentence:** NLKGQ generates SPARQL zero-shot in a single LLM call whose context carries the complete domain OWL ontology plus a domain rider, and wrapper ontologies with a deterministic rewriter extend this to uncontrolled vocabularies, scoring 89.9% Match on DBLP-QuAD 3.1, 98/100 on SemOpenAlex, and 100% on neuroimaging metadata.
## Key points
- Single-call zero-shot mechanism: system prompt with SPARQL instructions + complete domain OWL ontology + domain-specific rider + user query; model output is stripped of fences/reasoning traces before execution.
- Controlled semantics claim: formally typed ontology tokens (declared domain/range, class hierarchy, ObjectProperty vs DatatypeProperty) map directly to query patterns, outperforming informal schema dumps, fine-tuning, agentic exploration, and retrieval pipelines.
- Wrapper ontologies: clean namespace with readable typed terms (e.g. `dblpx:venueName` range `xsd:string` vs `dblpx:venue` range `Venue`; `signatureAuthor`, `signaturePosition`) deterministically rewritten to native forms (e.g. `dblp:publishedInStream`, `dblp:yearOfPublication`); `dblpx` federates DBLP + OpenCitations, `oax` flattens SemOpenAlex intermediaries (Authorship/OpenAccess/Geo).
- Headline results: DBLP-QuAD 2.0 57.6% Match under deterministic re-scoring (QuAD 2.1 protocol); DBLP-QuAD 3.1 89.9% Match / 81.3% Exact on 1,000 questions (Qwen3.6-27B); SemOpenAlex 98/100 vs published baseline 86/100; neuroimaging metadata 100% on 21 competency questions.
- Wrapper ablation: +25.3 Exact-match points on 1,000 DBLP questions (56.0% native → 81.3% wrapper, Table 2); +15.0 Match on QuAD 3.1; ten-model sweep (Qwen, Gemma, Mistral, Llama) converges near 90% Match for the two strongest dense models (Gemma-4-31B 90.3%, Qwen3.6-27B-FP8 90.0%).
- QuAD 2.0 defects → QuAD 3.1 fix: 998/1,000 references have LIMIT (992 LIMIT 10), 723 without ORDER BY, causing 52.1–52.9% run-to-run Match variation and ~61.5-point SPINACH F1 gap (17.5% on 2.0 vs 79.0% on 3.1); 122 VALUES-only echo queries, 211 cases needing undocumented OpenCitations data (only 71% of DBLP publications carry an OpenCitations identifier), plus ambiguous machine-generated questions.
- Hierarchy claim: formal concept transfer > model architecture > model scale > prompt engineering; rider is reserved for stable query conventions because prose repair is "whack-a-mole" (concept smearing: natural-language tokens are semantically "wide" vs formal tokens "narrow").
---
## Introduction: informal transfer vs controlled semantics
**Covers:** Abstract through Introduction (2024; Doulaverakis et al. 2025 references onward)

LLM applications transfer domain concepts informally via prompt prose, schema dumps, and examples. For database queries, the paper argues concepts pass more effectively through representations whose terms carry "declared, machine-readable semantics (controlled semantics)."

> "controlled semantics: schema tokens in the context window carry declared, machine-readable meaning."

> "Complete declared semantics for the vocabulary in the context window avoid leaving the model to invent domain concepts and relationships."

Native DBLP vocabulary illustrates opacity: `dblp:publishedIn` yields a venue name as plain string while `dblp:publishedInStream` yields the venue as URI, "and nothing in either name says so."

Prior compensation strategies listed: fine-tuning (Pan, de Boer, and van Ossenbruggen 2025; Mecharnia and d'Aquin 2025), multi-call agentic exploration (Walter and Bast 2025; Dobriy et al. 2026), retrieval-augmented pipelines (Smeros et al. 2025).

Original NLKGQ result on neuroimaging metadata (purpose-built ontology): 100% on 21 competency questions vs 43% for SQL from auto-generated schema, rising only to 57% with ontology annotations in column comments.

## Related work: schema injection, systems, benchmarks
**Covers:** Related Work section

- Schema injection matters: GPT-4o without schema 0.08 F1 on bioinformatics SPARQL vs 0.91 with retrieved schema + examples + validation (Emonet et al. 2024); medical SPARQL 11/11 with KG structure from an example vs 4/11 without (Doulaverakis et al. 2025).
- Memorization confound: LLMs reproduce real Wikidata URIs even when masked (Gashkov et al. 2025), so less-memorized KGs such as DBLP are a stricter generalization test; on unfamiliar vocabularies "the context window is the model's only source of schema knowledge."
- Systems: GRASP ReAct-style exploration, feedback variant 51.0% F1 on 50 samples of original DBLP-QuAD with GPT-4.1 multi-call; GRISP fine-tunes skeleton properties; FIRESPARQL fine-tunes LLaMA-8B (85% on SciQA but 0% zero-shot); SPARQL-LLM retrieval-augmented with revision loop, finding 11 defective reference queries.
- Benchmarks: QuAD 2.0 authors' own few-shot + entity-linking system reports 57.74% F1 (Taffa et al. 2025); SemOpenAlex 100-question test set best baseline 123B few-shot with entity mappings scores 86/100 (Bartels et al. 2025).
- Schema formalism: SPARQL outperforms SQL 3× overall, SQL falling to zero on hardest quadrants (Sequeda, Allemang, and Jacob 2024); NLKGQ tightened comparison on same ontology/data/models: SPARQL 100%, SQL 57%; fine-tuning works on readable DBpedia (61%) but fails on opaque Wikidata (13%) (Mecharnia and d'Aquin 2025).

## What OWL provides; prior controlled-domain results
**Covers:** "Formal Ontologies as Concept Transfer" + "Prior Results on a Controlled Domain"

Five formally grounded token categories informal descriptions lack:

1. Explicit domain and range (e.g. `dblpx:signatureAuthor` links Signature to Person).
2. Class hierarchy (`rdfs:subClassOf`; "publications" covers Article, Inproceedings, Book without enumeration).
3. Property typing (`owl:ObjectProperty` vs `owl:DatatypeProperty`: URI join vs literal filter).
4. Human-readable annotations (`rdfs:label`, `rdfs:comment` in the processed vocabulary).
5. Semantic naming (`hasAuthor`, `publishedInStream`, `yearOfPublication` vs `auth_id`, `pub_yr`).

Ablation on neuroimaging (same data, model, prompt; only vocabulary varied): full OWL 100% → 81% without `rdfs:comment` → 5% as bare graph structure. Three system-prompt variants tied once vocabulary was right; 35B MoE variants peaked at 57% vs dense 27B's 100%. Six design principles stated: full English words, descriptive property names, consistent has-prefixed naming, recognizable class names, explicit domain and range, no opaque identifiers.

## Wrapper ontologies, worked example, domain rider
**Covers:** "Wrapper Ontologies" + "A Worked Example" + "The Role of the Domain Rider"

Wrapper = clean namespace + deterministic SPARQL-to-SPARQL rewriter to native predicates/patterns before execution on unchanged endpoint; one wrapper term may expand to several triples. Lineage: ontology-based data access (Xiao et al. 2018), but designed for LLM consumption with deterministic rewrite.

- DBLP: native uses `dblp:Signature` for authorship reification, 19 external namespaces, no `rdfs:comment`; `dblpx` gives self-documenting names, domain/range for every property, single namespace; combined DBLP + OpenCitations dump (Peroni and Shotton 2020) under one vocabulary.
- SemOpenAlex: `oax` flattens Authorship/OpenAccess/Geo intermediaries into direct properties.

Worked QuAD 3.1 example — question: "What are the author signatures for publications in venue <https://dblp.org/streams/conf/pods> from 2024? Return signature URI and publication URI, sorted by publication." Model generates in `dblpx`:

```sparql
SELECT DISTINCT ?signature ?pub WHERE {
  ?pub a dblpx:Publication ;
    dblpx:venue <https://dblp.org/streams/conf/pods> ;
    dblpx:year "2024"^^xsd:gYear ;
    dblpx:hasSignature ?signature .
} ORDER BY ?pub
```

Rewriter restores native `dblp:Publication`, `dblp:publishedInStream`, `dblp:yearOfPublication`, `dblp:hasSignature`. "The model never sees publishedInStream or yearOfPublication."

Rider division of labor: vocabulary belongs in the ontology; rider holds small stable query conventions. "Rider additions approach zero sum as the rider matures" — rider failed as incremental concept-repair channel (see Discussion).

## Benchmark critique: DBLP-QuAD 2.0 defects
**Covers:** "Benchmark Critique: DBLP-QuAD 2.0"

QuAD 2.0: 5,000 log-derived question–SPARQL pairs; evaluation on 1,000-question test set.

| Defect | Detail in chunk |
|---|---|
| Non-deterministic evaluation | 998/1,000 refs impose LIMIT (992 LIMIT 10), 723 without ORDER BY; re-executing refs gives 52.1–52.9% Match over five runs; SPINACH F1 ~17.5% either way |
| LLM-generated questions | LLaMA-3.1-8B SPARQL-to-text paraphrases: unnatural, ambiguous where multiple SPARQL forms exist |
| Ambiguous entities | Prose names vs specific URIs; many DBLP authors share names; referent unrecoverable |
| Defective refs | 122 `SELECT * WHERE { VALUES ?x { <uri> } }` echoes; wrong predicates (e.g. `dblp:createdBy` incl. editors for authorship); missing GROUP BY; malformed projections |
| Misdocumented data | 211 cases need OpenCitations data; docs point to plain DBLP dump with no citation triples; required combined dump at sparql.dblp.org unreferenced; 71% citation coverage bound |
| Reproducibility | Endpoint software unspecified, dump not archived, generation on closed service |

> "Match remains informative under this defect while row-wise F1 does not."

## DBLP-QuAD 3.1: deterministic revision
**Covers:** "DBLP-QuAD 3.1" section

Preserves 2.0 intent/provenance; every modification logged per case; repairs against reference intent, not NLKGQ outputs; wrapper advantage predates repairs (+9.9 Match on unmodified 2.0).

- Deterministic evaluation: LIMIT removed in 954 cases (699 no ORDER BY + 255 ties at LIMIT boundary); 305 under-constrained queries scoped with year/venue/affiliation filters; LIMIT survives in 44 ranked top-k queries with deterministic ORDER BY (24 received ORDER BY matching ranking intent; 699 + 24 = 723).
- Reference repair: corrected predicates, missing GROUP BY, broken aggregations verified by execution; 122 VALUES-only echoes replaced with real lookups.
- Questions: frontier-model (Claude) rewrite for natural phrasing/intent; per-case pass amended 547 questions omitting columns/ordering/scope.
- Entities: 266 rewritten questions include bracketed URIs (query-generation scope, not entity resolution); NLKGQ web interface accepts same bracketed URIs.
- Data docs: combined DBLP+OpenCitations requirement stated with 71% bound; 28 SERVICE-federated cases kept with third-party-availability caveat.
- Release: self-contained GitHub benchmark + scripts recreating snapshot from DBLP 2025-07-02 RDF release + OpenCitations Index subset, with QLever instance.

## Evaluation setup, metrics, 2.0 → 3.1 progression
**Covers:** "Evaluation" + "From QuAD 2.0 to QuAD 3.1" + Table 1 + Table 2

Setup: single LLM call, temperature 0.0, no fine-tuning/few-shot/entity linking; QLever (Bast and Buchhold 2017); single fixed DBLP snapshot; open-weight models served locally on AMD APU nodes; repeated runs reproduce within 0.1 points except QuAD 2.0 re-executed refs.

Table 1 — metrics:

| Metric | Scoring | Criterion |
|---|---|---|
| Match | binary | generated results contain the reference results, equal or superset |
| Exact | binary | generated results exactly match reference results |
| QuAD F1 | graded | set-of-values F1 over all result cells, flattened (Taffa et al. 2025 code) |
| SPINACH F1 | graded | row-assignment F1 (Liu et al. 2024), via GRASP code (Walter and Bast 2025) |

Table 2 — DBLP progression (Qwen3.6-27B, procedural prompt, t=0.0, 1,000 cases, %):

| QuAD | Ontology | Match | Exact | QuAD F1 | SPINACH F1 |
|---|---|---|---|---|---|
| 2.0 | native | 43.0 | 10.7 | 23.2 | 23.0 |
| 2.0 | wrapper | 52.9 | 11.3 | 17.6 | 17.5 |
| 2.1 | wrapper | 57.6 | 20.1 | 16.7 | 17.3 |
| 3.1 | native | 74.9 | 56.0 | 63.8 | 62.3 |
| 3.1 | wrapper | 89.9 | 81.3 | 80.7 | 79.0 |

Readings stated: 2.0-wrapper row varies 52.1–52.9 Match over five runs; QuAD 2.1 (same questions/queries, refs computed once) is the reported 2.0 result (57.6% Match); F1 inversion (better system scores worse: 23.2→17.6) is "first evidence that on QuAD 2.0 the F1 columns measure the references, not the system"; on 3.1 wrapper adds +15.0 Match / +25.3 Exact; 2.0→3.1 SPINACH swing 17.5→79.0 attributed mostly to deterministic references; remaining 89.9 vs 79.0 spread is partial-credit granularity.

## Cross-domain generality; model comparison
**Covers:** "Cross-Domain Generality" (Table 3) + "Model Comparison" (Table 4)

Table 3 — cross-domain (Qwen3.6-27B, t=0.0):

| Domain | Cases | Match% | Exact% | F1S | Baseline |
|---|---|---|---|---|---|
| DBLP (QuAD 3.1) | 1,000 | 89.9 | 81.3 | 79.0 | 51.0 F1 |
| SemOpenAlex | 100 | 98.0 | 98.0 | — | 86/100 |
| Neuroimaging | 21 | 100.0 | 100.0 | — | — |

SemOpenAlex audit: one duplicate question retained to preserve denominator; seven "papers that X and Y published" UNION refs read as either-author vs natural co-authorship reading — the two misses use conjunctive reading. DBLP baseline caveat: GRASP 51.0% measured on original template-generated DBLP-QuAD (Banerjee et al. 2023), not same benchmark; "we expect GRASP and other systems also to score higher on QuAD 3.1."

Table 4 — ten models on QuAD 3.1 + wrapper (t=0.0, procedural prompt, %; *partial runs over completed cases):

| Model | Type | Match | Exact | F1Q | F1S | Fail |
|---|---|---|---|---|---|---|
| Gemma-4-31B | dense | 90.3 | 75.1 | 79.4 | 76.9 | 3.5 |
| Qwen3.6-27B-FP8 | dense/q | 90.0 | 81.4 | 81.3 | 79.4 | 2.5 |
| Qwen3.6-27B | dense | 89.9 | 81.4 | 80.8 | 79.1 | 3.4 |
| Qwen3-Coder-30B | MoE/code | 81.1 | 62.3 | 69.6 | 67.9 | 4.0 |
| Mistral-Small-24B | dense | 80.6 | 65.2 | 68.0 | 64.3 | 4.7 |
| Llama3.3-70B | dense | 74.3 | 59.4 | 63.6 | 61.7 | 5.0 |
| Qwen3-8B | dense | 66.2 | 50.6 | 53.5 | 51.3 | 13.2 |
| Qwen3.6-35B-FP8 | MoE/q | 64.9 | 52.6 | 55.1 | 52.7 | 25.3 |
| Qwen3.6-35B* | MoE | 50.4 | 40.3 | 42.4 | 40.3 | 41.5 |
| Qwen3-14B* | dense | 24.8 | 19.1 | 19.3 | 18.4 | 68.6 |

Stated readings: Gemma leads Match only; Qwen3.6-27B ahead on Exact/both F1s; Mistral-Small-24B beats Llama3.3-70B with ~1/3 parameters; Qwen 8B→27B gains 30.8 Exact points (3.4× params) vs 8.8 cross-family for 9× params; wrapper swap on 27B gains 25.3 Exact points atop scale; FP8 matches full precision; general MoE high Fail% (25.3/41.5%) vs code-MoE 4.0%, so sparsity alone does not explain failures.

## Error analysis, discussion, conclusion
**Covers:** "Error Analysis" through "Conclusion" + GenAI disclosure

Error analysis on progression run (899 Match; 101 non-matches; 30 failed cases): 24 citation queries (OMID-side entities vs wrapper's DBLP URIs; 71% mapping coverage); 22 federated SERVICE calls to DBpedia/Wikidata/FactGrid outside `dblpx` (other 6 federated match via FOAF etc.); 18 aggregation-structured differently; 5 aggregation timeouts/failures; 3 ontology-introspection queries; 29 heterogeneous individual errors. Failed-case split: 10 federated, 11 heterogeneous, 5 aggregation, 3 citation, 1 introspection.

Discussion claims:

- Hierarchy: "formal concept transfer > model architecture > model scale > prompt engineering"; scale + wrapper additive (native 56.0% → wrapper 81.3% Exact on tested model).
- Fine-tuning "ranks no higher": exploratory 8B ontology-training unpromising; tuning injects facts slowly with hallucination and erodes out-of-distribution skills (Gekhman et al. 2024; Ovadia et al. 2024; Kandpal et al. 2023; Kotha, Springer, and Raghunathan 2024).
- Beyond SPARQL: SQL/API/code generation face same mapping problem; measured SQL case 43%→57% via column comments.
- Concept smearing: at t=0.0 generation is near-deterministic yet any prompt-token change shifts untargeted queries; "match names exactly" fixes targets but breaks unrelated queries.
- Limitations: wrapper-vs-native ablation on single model (Qwen3.6-27B); sweep only in wrapper config; no proprietary models; full ontology per call (context-window scaling unaddressed); Match allows supersets (Exact 81.3% stricter); repairs and system share authorship (logs + pre-repair margin as checks); manual wrapper design; entity resolution out of scope; 71% citation coverage; DBLP "BibTeX-inherited classification might no longer be a best fit."
- Benchmark moral: "61.5-point SPINACH F1 gap between QuAD 2.0 and QuAD 3.1 (17.5% vs. 79.0%) demonstrates that benchmark defects drive measured performance."
- Conclusion restatement: "Concepts are more effectively passed to LLMs through formal mechanisms than through informal description"; "The system prompt tunes query generation; the ontology and rider tune the concepts."
- GenAI disclosure: tools assisted editing, LaTeX, coding, data analysis; frontier model rewrote QuAD 3.1 questions; evaluated system uses only locally deployed LLMs.

**Covers:** arXiv:2609.14652v1 header through Conclusion/GenAI disclosure and References (chunk 02: main paper body).
