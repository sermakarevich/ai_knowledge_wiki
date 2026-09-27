---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Natural Language Knowledge Graph Query Execution: Leveraging Controlled Semantics in the LLM Context Window

### Q1. What does the paper's opening front-matter chunk contain, and what is its limitation?

> [!tip]- Answer
> > It contains only bibliographic front-matter: the title, subtitle, author Blake G. Fitch, Max Planck Institute affiliation, and a truncated abstract fragment ending mid-citation. It states no complete claims, numbers, or mechanisms, so substantive questions must draw on the companion paper-body page. See [[wiki/01-natural-language-knowledge-graph-query-execution|Natural Language Knowledge Graph Query Execution]].

### Q2. How does the NLKGQ system generate SPARQL from a natural-language question?

> [!tip]- Answer
> > It uses a single zero-shot LLM call whose context carries SPARQL instructions, the complete domain OWL ontology, and a small domain rider plus the user query. The model writes SPARQL in the given vocabulary, and fences or reasoning traces are stripped before execution with no fine-tuning, few-shot examples, or agentic exploration. See [[wiki/02-paper-body|NLKGQ paper body]].

### Q3. What does the paper mean by controlled semantics, and which OWL features carry it?

> [!tip]- Answer
> > Controlled semantics means context-window schema tokens carry declared, machine-readable meaning so the model maps types directly to query patterns instead of inventing relations. The five carriers are explicit domain and range, class hierarchy via rdfs:subClassOf, ObjectProperty versus DatatypeProperty typing, rdfs:label/comment annotations, and descriptive semantic names. See [[wiki/02-paper-body|NLKGQ paper body]].

### Q4. How do wrapper ontologies extend NLKGQ to opaque native vocabularies such as DBLP and SemOpenAlex?

> [!tip]- Answer
> > A wrapper defines a clean readable namespace with declared types (for example dblpx:venueName as string versus dblpx:venue as Venue, plus signatureAuthor and signaturePosition) and a deterministic SPARQL-to-SPARQL rewriter restores native predicates before execution on the unchanged endpoint. The dblpx wrapper federates DBLP with OpenCitations while oax flattens SemOpenAlex intermediaries such as Authorship, OpenAccess, and Geo into direct properties. See [[wiki/02-paper-body|NLKGQ paper body]].

### Q5. What defects made DBLP-QuAD 2.0 non-deterministic, and how did QuAD 3.1 repair them?

> [!tip]- Answer
> > In QuAD 2.0, 998 of 1,000 references impose LIMIT (992 LIMIT 10) with 723 lacking ORDER BY, so re-executing references swings Match by 52.1–52.9%, alongside 122 VALUES-only echo queries and 211 cases needing undocumented OpenCitations data with only 71% citation coverage. QuAD 3.1 removed LIMIT in 954 cases, kept it in 44 ranked top-k queries with deterministic ORDER BY, repaired predicates and aggregations, replaced echoes with real lookups, rewrote 547 ambiguous questions, and documented the combined dump. See [[wiki/02-paper-body|NLKGQ paper body]].

### Q6. What are the headline evaluation results, and how are Match and Exact defined?

> [!tip]- Answer
> > With Qwen3.6-27B the system scores 89.9% Match and 81.3% Exact on 1,000 QuAD 3.1 questions, 98/100 on SemOpenAlex versus an 86/100 baseline, and 100% on 21 neuroimaging competency questions, with wrappers adding 25.3 Exact points over native vocabulary. Match is binary containment where generated results equal or supersede the reference, while Exact requires the result sets to be identical. See [[wiki/02-paper-body|NLKGQ paper body]].

### Q7. Should a team building NL-to-SPARQL over a new opaque knowledge graph invest in a manual wrapper ontology first?

> [!tip]- Answer
> > Yes, when the native vocabulary is opaque and the domain is stable, because the wrapper plus deterministic rewrite outranked model scale and prompt engineering, adding 15.0 Match and 25.3 Exact points on DBLP with convergence near 90% Match for the strongest dense models. The recommendation is bounded by manual wrapper cost, single-model ablation, 71% citation-coverage limits, and out-of-scope entity resolution, so treat the wrapper as the first lever but budget for those residual errors. See [[wiki/02-paper-body|NLKGQ paper body]].
