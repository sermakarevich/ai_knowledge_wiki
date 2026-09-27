> [[index|Wiki]] | [[summary|Summary]]

# Natural Language Knowledge Graph Query Execution: Leveraging Controlled Semantics in the LLM Context Window — Digest

## 1. [[wiki/01-natural-language-knowledge-graph-query-execution|Natural Language Knowledge Graph Query Execution: Leveraging Controlled Semantics in the LLM Context Window]]

**In one sentence:** This chunk contains only the paper's title, subtitle, author, and affiliation front-matter, with the abstract truncated mid-phrase, so no substantive argument can be summarised from it.

- The chunk provides no complete claims, numbers, or mechanisms beyond bibliographic front-matter.
- See the companion page [[02-paper-body|02-paper-body]] for the main paper body content.

## 2. [[wiki/02-paper-body|NLKGQ paper body — controlled semantics, wrappers, and benchmarks]]

**In one sentence:** NLKGQ generates SPARQL zero-shot in a single LLM call whose context carries the complete domain OWL ontology plus a domain rider, and wrapper ontologies with a deterministic rewriter extend this to uncontrolled vocabularies, scoring 89.9% Match on DBLP-QuAD 3.1, 98/100 on SemOpenAlex, and 100% on neuroimaging metadata.

- Single-call zero-shot mechanism: system prompt with SPARQL instructions + complete domain OWL ontology + domain-specific rider + user query; model output is stripped of fences/reasoning traces before execution.
- Controlled semantics claim: formally typed ontology tokens (declared domain/range, class hierarchy, ObjectProperty vs DatatypeProperty) map directly to query patterns, outperforming informal schema dumps, fine-tuning, agentic exploration, and retrieval pipelines.
- Wrapper ontologies: clean namespace with readable typed terms (e.g. `dblpx:venueName` range `xsd:string` vs `dblpx:venue` range `Venue`; `signatureAuthor`, `signaturePosition`) deterministically rewritten to native forms (e.g. `dblp:publishedInStream`, `dblp:yearOfPublication`); `dblpx` federates DBLP + OpenCitations, `oax` flattens SemOpenAlex intermediaries (Authorship/OpenAccess/Geo).
- Headline results: DBLP-QuAD 2.0 57.6% Match under deterministic re-scoring (QuAD 2.1 protocol); DBLP-QuAD 3.1 89.9% Match / 81.3% Exact on 1,000 questions (Qwen3.6-27B); SemOpenAlex 98/100 vs published baseline 86/100; neuroimaging metadata 100% on 21 competency questions.
- Wrapper ablation: +25.3 Exact-match points on 1,000 DBLP questions (56.0% native → 81.3% wrapper, Table 2); +15.0 Match on QuAD 3.1; ten-model sweep (Qwen, Gemma, Mistral, Llama) converges near 90% Match for the two strongest dense models (Gemma-4-31B 90.3%, Qwen3.6-27B-FP8 90.0%).
- QuAD 2.0 defects → QuAD 3.1 fix: 998/1,000 references have LIMIT (992 LIMIT 10), 723 without ORDER BY, causing 52.1–52.9% run-to-run Match variation and ~61.5-point SPINACH F1 gap (17.5% on 2.0 vs 79.0% on 3.1); 122 VALUES-only echo queries, 211 cases needing undocumented OpenCitations data (only 71% of DBLP publications carry an OpenCitations identifier), plus ambiguous machine-generated questions.
- Hierarchy claim: formal concept transfer > model architecture > model scale > prompt engineering; rider is reserved for stable query conventions because prose repair is "whack-a-mole" (concept smearing: natural-language tokens are semantically "wide" vs formal tokens "narrow").

## The argument in five moves

1. Informal concept transfer (prompt prose, schema dumps, examples) leaves the model to invent domain relations, so NLKGQ instead puts complete OWL controlled semantics in the context window for single-call zero-shot SPARQL generation.
2. Wrapper ontologies with a deterministic SPARQL-to-SPARQL rewriter extend the method to opaque native vocabularies (DBLP, SemOpenAlex) without changing the endpoint, gaining +25.3 Exact points on DBLP.
3. DBLP-QuAD 2.0's non-deterministic LIMIT-without-ORDER-BY references, echo queries, and undocumented OpenCitations dependency make its scores measure the references, motivating the deterministic repaired QuAD 3.1 revision.
4. On QuAD 3.1, SemOpenAlex, and neuroimaging metadata the system reaches 89.9% Match, 98/100, and 100% respectively, with the model sweep showing formal concept transfer outranking architecture, scale, and prompt engineering.
5. Residual errors (citation coverage, federated calls, aggregation) plus concept-smearing limits bound the claims: Match allows supersets, wrappers are manual, entity resolution is out of scope, and benchmark defects drive measured performance.
