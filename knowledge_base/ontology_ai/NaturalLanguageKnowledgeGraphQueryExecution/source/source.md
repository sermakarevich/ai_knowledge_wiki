# Natural Language Knowledge Graph Query Execution: Leveraging Controlled Semantics in the LLM Context Window
Source: https://arxiv.org/abs/2609.14652v1
Kind: pdf
Fetched: 2026-09-23T12:57:35.395640+00:00
Tool: pdftotext
Research-Target: /Users/sergii/.ai/knowledge/research_topics/ontology_ai/research/ontology-ai
Topic: ontology_ai

                                                            Natural Language Knowledge Graph Query Execution:
                                                         Leveraging Controlled Semantics in the LLM Context Window
                                                                                                      Blake G. Fitch
                                                                         Max Planck Institute for Biological Cybernetics, Tübingen, Germany
                                                                                           blake.fitch@tuebingen.mpg.de



                                                                     Abstract                                  of these design choices (Gashkov et al. 2025; Emonet et al.




arXiv:2609.14652v1 [cs.DB] 13 Sep 2026
                                                                                                               2024; Doulaverakis et al. 2025).
                                           Large Language Model (LLM) applications often transfer do-             This paper shows that careful design of the schema in-
                                           main concepts into the model’s context informally, through
                                           prompt prose, schema dumps, and examples. We show that
                                                                                                               formation in the context window, together with the runtime
                                           for database queries, data model concepts pass to LLMs more         support, delivers more accuracy than published fine-tuned,
                                           effectively through representations whose vocabulary terms          agentic, and retrieval systems report. Formal OWL ontolo-
                                           carry declared, machine-readable semantics (controlled se-          gies transfer data model concepts as semantically precise
                                           mantics). NLKGQ is a working system and reusable frame-             tokens that map directly to correct query patterns. Informal
                                           work that does this for data modeled in a knowledge graph.          descriptions (column names, natural language instructions,
                                           A formal OWL ontology serves as the transfer mechanism,             schema comments) transfer ambiguous tokens the LLM must
                                           concentrating the meaning of the data into semantically pre-        interpret probabilistically. Complete declared semantics for
                                           cise tokens the model can use directly. In a single LLM call,       the vocabulary in the context window avoid leaving the model
                                           NLKGQ places in the context a system prompt instructing on          to invent domain concepts and relationships. We call this con-
                                           SPARQL, the complete domain OWL ontology, and a domain-
                                           specific prompt addition, together with the user’s natural lan-
                                                                                                               trolled semantics: schema tokens in the context window carry
                                           guage query. The model then generates the SPARQL query              declared, machine-readable meaning. The original NLKGQ
                                           directly, zero-shot. Where the native vocabulary of an existing     paper introduced the system for natural language knowledge
                                           database or federation of databases is opaque, a wrapper on-        graph querying and established this on a single domain: the
                                           tology substitutes clean terms and a runtime rewriter restores      representation of the ontology, not the model or the prompt,
                                           the native forms. Evaluating on DBLP-QuAD 2.0 showed                determined accuracy (Fitch and Kurtz 2026). Here we test
                                           that its scores depend on the graph snapshot, the endpoint          the principle on public knowledge graphs whose vocabular-
                                           used, and the wording of its machine-generated questions,           ies we do not control, and on larger benchmarks.
                                           so we propose DBLP-QuAD 3.1, which maintains the intent
                                                                                                                  The NLKGQ execution mechanism is a single LLM call.
                                           of 2.0 while making reference results deterministic, revising
                                           reference SPARQL where needed, and rewriting the natural            This OpenAI-compatible API call (OpenAI 2026) comprises
                                           language questions, with a frontier model, to state each refer-     a user prompt carrying the user’s natural language query
                                           ence query’s intent clearly and completely. We evaluate on the      and a system prompt containing a generic set of instructions
                                           DBLP-QuAD 2.0 benchmark (57.6% Match under determin-                for SPARQL generation, the complete domain OWL ontol-
                                           istic re-scoring), DBLP-QuAD 3.1 (89.9% Match on 1,000              ogy, and a domain-specific set of instructions (the domain
                                           questions), SemOpenAlex (98% Match against a published              rider). The model generates the SPARQL query zero-shot.
                                           baseline’s 86% on the identical test set), and neuroimaging         The system strips any non-SPARQL text (code fences, rea-
                                           metadata (100%).                                                    soning traces, commentary) from the response before execu-
                                                                                                               tion. Where the native vocabulary of an existing database or
                                                                                                               federation is opaque, a wrapper ontology substitutes clean,
                                                                 Introduction                                  formally typed terms and a deterministic runtime rewriter re-
                                         Natural language query execution on knowledge graphs re-              stores the native forms before endpoint execution. The native
                                         quires the LLM to know the data model: what classes exist,            vocabulary of DBLP, the computer science bibliography’s
                                         how they connect, what types their properties carry. Prior            knowledge graph (Ackermann et al. 2024), illustrates the
                                         work transfers this knowledge informally (schema dumps,               problem: dblp:publishedIn yields a venue name as
                                         few-shot examples, prompt instructions) and then compen-              a plain string while dblp:publishedInStream yields
                                         sates with engineering complexity: fine-tuning (Pan, de Boer,         the venue as a URI, and nothing in either name says so. Our
                                         and van Ossenbruggen 2025; Mecharnia and d’Aquin 2025),               dblpx wrapper ontology declares dblpx:venueName
                                         multi-call agentic exploration (Walter and Bast 2025; Dobriy          with range xsd:string and dblpx:venue with range
                                         et al. 2026), or retrieval-augmented pipelines (Smeros et al.         Venue, so the distinction the model needs is well defined.
                                         2025). A consistent finding across this literature is that pro-          This insight originates in our original NLKGQ results
                                         viding schema information in context matters more than any            on a purpose-built domain: a neuroimaging metadata KG
whose ontology was designed end-to-end for natural lan-          generation with runtime IRI retrieval, stating that “zero-shot
guage querying reached 100% accuracy on 21 competency            agentic methods take the upper hand” in low-data regimes.
questions, against 43% for the same questions over a SQL         FIRESPARQL (Pan, de Boer, and van Ossenbruggen 2025)
schema auto-generated from that ontology, rising only to         fine-tunes LLaMA-8B for scholarly KGs, achieving 85%
57% with the ontology’s annotations carried into column          on SciQA but 0% zero-shot. SPARQL-LLM (Smeros et al.
comments. This paper extends the approach to three domains       2025) validates retrieval-augmented generation with schema
and establishes three contributions:                             and example injection plus a revision loop, and in doing so
1. A demonstration that controlled semantics can de-             finds 11 defective reference queries in the challenge set it
   liver high accuracy without fine-tuning, agentic explo-       evaluated on, precedent that benchmark auditing is part of
   ration, or very large models. On the SemOpenAlex (Fär-        sound evaluation. Our approach is single-call and zero-shot,
   ber et al. 2023) benchmark the architecture scores 98/100     relying entirely on formal ontology vocabulary rather than
   against the published baseline’s 86/100 on the same test      examples or exploration.
   set. The DBLP wrapper ontology adds +25.3 exact-match            Benchmarks. QuAD 2.0 (Taffa et al. 2025) is a large
   points on 1,000 DBLP questions. The same single-call          log-derived scholarly benchmark but has systematic quality
   architecture reaches 89.9% Match on DBLP (Qwen3.6-            issues we document below. Its authors’ own few-shot system
   27B). A ten-model sweep across four families (Qwen,           with entity linking reports 57.74% F1 on it (Taffa et al. 2025).
   Gemma, Mistral, Llama) shows the two strongest mod-           High F1 there requires reproducing each reference’s arbitrary
   els converging near 90%. On neuroimaging metadata it          10-row slice, which few-shot prompting in the benchmark’s
   reaches 100%.                                                 own query style encourages. A system returning the full an-
                                                                 swer set is penalized for every extra row (see the critique
2. Wrapper ontologies and a runtime rewriter. These              below). Our QuAD 3.1 revision is likely to improve all sys-
   bring controlled semantics to databases and federations       tems’ results. For SemOpenAlex, Bartels et al. (2025) re-
   whose vocabularies we do not control: the LLM sees            lease a 100-question test set with reference queries. Their
   clean, typed terms, and a deterministic rewriter restores     best baseline, a 123B model prompted few-shot with entity
   the native forms for execution on an unchanged endpoint       mappings, scores 86/100. We evaluate on the same test set.
   such as the public DBLP KG (Ackermann et al. 2024).              Schema representation and query generation. Sequeda,
3. A refined benchmark. We identify systematic quality           Allemang, and Jacob (2024) show SPARQL outperforms
   issues in DBLP-QuAD 2.0 (Taffa et al. 2025) and propose       SQL 3× overall, with SQL falling to zero on the hardest
   DBLP-QuAD 3.1 (hereafter QuAD 2.0 and QuAD 3.1)               schema quadrants, suggesting that the richer semantics of
   with deterministic evaluation, revised reference queries,     RDF/OWL schemas benefit query generation. The original
   and questions that state each reference query’s intent.       NLKGQ paper tightened this comparison by deriving both
                                                                 backends from the same ontology with the same data and
                     Related Work                                models: SPARQL 100%, SQL 57% (Fitch and Kurtz 2026).
Schema injection for SPARQL generation. Emonet et al.            Mecharnia and d’Aquin (2025) find that fine-tuning works
(2024) show that GPT-4o without schema context scores 0.08       on KGs with readable names (DBpedia, 61%) but fails on
F1 on bioinformatics SPARQL; with retrieved schema and           opaque identifiers (Wikidata, 13%): direct evidence that vo-
example context plus query validation it reaches 0.91. Medi-     cabulary readability determines accuracy independently of
cal SPARQL generation reaches 11/11 with KG structure ex-        model capability. The same principle is surfacing in the
tracted from an example entry vs. 4/11 without (Doulaverakis     relational world: Zhang, Miao, and Wang (2026) propose
et al. 2025). Gashkov et al. (2025) demonstrate that LLMs        semantics-preserving schema renaming and view-based ab-
memorize popular KG schemas: models reproduce real Wiki-         straction to make SQL schemas legible to LLMs. Wrap-
data URIs even when URIs are masked in the prompt, so            per ontologies share a lineage with ontology-based data ac-
scores on widely used public KGs partly measure memoriza-        cess (Xiao et al. 2018), which maps a clean conceptual vo-
tion rather than generalization. This makes less-memorized       cabulary onto native schemas. Ours differs in being designed
KGs such as DBLP a stricter test of generalization, and it im-   for LLM consumption following the NLKGQ design princi-
plies that on unfamiliar vocabularies the context window is      ples, and applied by a deterministic SPARQL-to-SPARQL
the model’s only source of schema knowledge. These results       rewrite to the native vocabulary before submission.
establish that schema information matters, but which formal
properties of the schema matter, and how to optimize them             Formal Ontologies as Concept Transfer
for LLM consumption, remains largely unexamined.                 NLKGQ generates SPARQL in a single LLM call. The
   SPARQL generation systems. GRASP (Walter and Bast             prompt contains a system prompt with SPARQL rules, the
2025) uses ReAct-style runtime exploration. Its feedback         full ontology in Turtle, an optional domain rider, and the
variant achieves 51.0% F1 on 50 samples of the original          user’s question. Architectural details are in the original
DBLP-QuAD (Banerjee et al. 2023) with GPT-4.1 across             NLKGQ paper (Fitch and Kurtz 2026). Here we focus on
multiple LLM calls. Its error analysis notes failures on cita-   why the ontology representation matters. Pretraining has ex-
tion queries where the OMID (OpenCitations Meta Identi-          posed LLMs to SPARQL and to the principles of querying
fier) indirection chain is too complex to discover at runtime,   knowledge graphs. Models write competent SPARQL over
a case the dblpx wrapper handles by stating the relationship     generic concepts without assistance. What a model lacks for
upfront. GRISP (Walter and Bast 2026) fine-tunes skeleton        a specific graph is the domain vocabulary: which classes and
properties exist, how they connect, and what types they carry.    NLKGQ. This paper reports on two wrapper implementa-
The ontology in the context window supplies exactly this, so      tions, dblpx for DBLP and oax for SemOpenAlex.
query generation reduces to concept transfer.                        For     DBLP,       the     native     vocabulary    uses
                                                                  dblp:Signature for authorship reification, a name
What OWL Provides That SQL Does Not                               that suggests cryptography rather than authorship, has 19
                                                                  external namespaces, and lacks rdfs:comment. The
An OWL ontology in context gives the LLM five categories
                                                                  dblpx wrapper provides self-documenting property names
of formally grounded tokens that informal schema descrip-
                                                                  (signatureAuthor, signaturePosition), explicit
tions lack:
                                                                  domain/range for every property, and a single namespace.
1. Explicit domain and range. Every property declares             The dblpx wrapper also spans a federation: our DBLP
   what class it connects and what type it expects. The           index loads the DBLP and OpenCitations (Peroni and
   LLM knows that dblpx:signatureAuthor links a                   Shotton 2020) dumps together, and the single dblpx
   Signature to a Person without inferring from data.             vocabulary covers entities and citations from both sources.
2. Class hierarchy. rdfs:subClassOf relation-                     For SemOpenAlex, the oax wrapper flattens indirect re-
   ships let the LLM reason about generalization. A               lationships (the Authorship/OpenAccess/Geo intermediary
   query about “publications” can include Article,                classes) into direct properties on the queried classes.
   Inproceedings, and Book without enumeration.
                                                                  A Worked Example
3. Property typing. owl:ObjectProperty vs.                        The following case from the QuAD 3.1 benchmark
   owl:DatatypeProperty tells the LLM whether to                  runs shows the mechanism end to end. The question:
   expect a URI join or a literal filter. SQL has foreign keys,   “What are the author signatures for publications in venue
   but the semantics are implicit.                                <https://dblp.org/streams/conf/pods> from 2024? Return
4. Human-readable annotations. rdfs:label and                     signature URI and publication URI, sorted by publication.”
   rdfs:comment attach natural language meaning to for-           The model, seeing only the dblpx wrapper vocabulary, gen-
   mal terms, directly in the vocabulary the LLM processes.       erates (PREFIX declarations omitted):
5. Semantic naming. Property names like hasAuthor,                SELECT DISTINCT ?signature ?pub WHERE {
   publishedInStream, yearOfPublication en-                         ?pub a dblpx:Publication ;
   code directional relationships in readable English. SQL           dblpx:venue <https://dblp.org/streams/
   column names (auth_id, pub_yr) are opaque.                            conf/pods> ;
                                                                     dblpx:year "2024"^^xsd:gYear ;
                                                                     dblpx:hasSignature ?signature .
Prior Results on a Controlled Domain                              } ORDER BY ?pub
The original NLKGQ paper introduced the system on neu-               The rewriter deterministically restores the native vocabu-
roimaging metadata with a purpose-built ontology (Fitch and       lary before execution:
Kurtz 2026). We summarize the findings this paper builds
on. With the full OWL ontology in context, SPARQL gen-            SELECT DISTINCT ?signature ?pub WHERE {
eration reached 100% on 21 competency questions; auto-              ?pub a dblp:Publication ;
                                                                     dblp:publishedInStream
generated SQL against the same data reached 57%. Strip-                <https://dblp.org/streams/conf/pods> ;
ping rdfs:comment annotations dropped SPARQL from                    dblp:yearOfPublication "2024"^^xsd:gYear
100% to 81%; reducing the ontology to bare graph struc-                  ;
ture dropped it to 5%. Same data, model, and prompt; only            dblp:hasSignature ?signature .
the formal richness of the vocabulary varied. Three system-       } ORDER BY ?pub
prompt variants tied once the vocabulary was right, and 35B         The model never sees publishedInStream or
MoE variants peaked at 57% against the dense 27B’s 100%.          yearOfPublication. It works in a vocabulary where
That work also established six ontology design principles         every term was chosen for semantic precision, and the map-
(full English words, descriptive property names, consistent       ping back to the endpoint’s terms is mechanical.
has-prefixed naming, recognizable class names, explicit do-
main and range, no opaque identifiers); here we apply them        The Role of the Domain Rider
to vocabularies we do not control.
                                                                  NLKGQ’s prompt contains natural language alongside the
                                                                  formal ontology: a system prompt establishing SPARQL dis-
Wrapper Ontologies                                                cipline (the procedural prompt cited in the table captions)
When a KG’s native OWL vocabulary is itself problematic           and a short domain rider. With the ontology they form the
(opaque identifiers, namespace collisions, overloaded terms,      concept layer, the context tokens that carry out concept trans-
missing annotations), we introduce a wrapper ontology: a          fer. Our best configurations use both. The practical division
clean namespace with readable, unambiguous terms that we          of labor: domain knowledge that can be stated as vocabu-
deterministically map to the native vocabulary. A SPARQL          lary belongs in the ontology, where it accumulates safely.
rewriter translates generated queries to native predicates and    The rider is reserved for a small, stable set of query con-
patterns before execution. One wrapper term may expand            ventions. In our experiments the rider failed as a channel for
to several triples. The wrapper is an architectural feature of    incremental concept repair; the Discussion shows why.
     Benchmark Critique: DBLP-QuAD 2.0                                                DBLP-QuAD 3.1
QuAD 2.0 (Taffa et al. 2025) comprises 5,000 question-            We update QuAD 2.0 rather than build a new benchmark be-
SPARQL pairs derived from SPARQL query logs over DBLP.            cause its assets are worth preserving. It is a scholarly KGQA
We evaluate against its 1,000-question test set and identify      benchmark derived from real SPARQL query logs, and pub-
systematic issues that affect all systems evaluated on it.        lished systems have reported against it. As published, how-
   Non-deterministic evaluation. 998 of 1,000 reference           ever, its scores conflate reference artifacts with system qual-
queries impose a LIMIT (992 of them LIMIT 10), 723                ity: the same system scores 17.5% SPINACH F1 on 2.0 and
without ORDER BY. Semantically equivalent queries with            79.0% on 3.1, a gap we attribute mainly to the references, not
different triple pattern orderings return different row slices    the system. An unreleased QuAD 2.1 measurement protocol
from the same engine. Under the benchmark’s own proto-            isolates the cause by keeping questions and reference queries
col, re-executing the references at evaluation time, the share    unchanged. Reference results are computed once against the
of cases our system matches varies run to run (52.1–52.9%         evaluation snapshot instead of re-executed on every run. Un-
across five runs) as the reference slices change; with refer-     der it, Match rises from 52.9% to 57.6% and Exact from
ence results computed once against the evaluation snapshot,       11.3% to 20.1%, while SPINACH F1 does not move (17.5%
the same system scores a stable 57.6% (the QuAD 2.1 pro-          to 17.3%). We report 57.6% as our QuAD 2.0 result. Con-
tocol). Either way, SPINACH F1 (Liu et al. 2024) stays near       sistent reference results repair individual cases, but the F1
17.5%, while on our updated QuAD 3.1 (deterministic or-           metrics still score answer rows against an arbitrary slice of the
dering) the same system scores 79.0%. We attribute most           reference result; only the deterministic references of 3.1 re-
of the 61.5-point F1 gap to the non-deterministic references.     cover them (79.0%). We therefore propose DBLP-QuAD 3.1,
Match remains informative under this defect while row-wise        updating QuAD 2.0’s 1,000 test cases while preserving their
F1 does not: the reference rows are an arbitrary slice of the     provenance. Every modification is logged per case. The re-
true answer, and a correct generated query returns the full an-   pairs were made against the reference queries’ intent, case by
swer set, which contains whichever slice the engine produced      case, not against NLKGQ’s outputs. The wrapper’s advan-
for the reference. F1 counts every valid row outside that slice   tage predates them (+9.9 Match on unmodified 2.0, Table 2
as a precision error, scoring correct queries down for the ref-   native vs. wrapper). The corrections:
erence’s arbitrariness. GRASP’s error analysis notes unfairly        Deterministic evaluation. Non-deterministic LIMIT
low F1 from LIMIT differences (Walter and Bast 2025).             clauses were removed (954 cases: 699 with no ORDER BY
   LLM-generated questions. Natural language questions            and 255 where ties on the ordering key at the LIMIT bound-
are generated by LLaMA-3.1-8B from SPARQL, producing              ary make the slice unstable), and under-constrained queries
unnatural phrasings and ambiguous intent where multiple           were scoped with year, venue, or affiliation filters so the nat-
SPARQL forms exist.                                               ural result set is bounded (305 cases: 296 among the 954, 9
   Ambiguous entity references. Questions name entities in        among the 44). LIMIT survives in 44 ranked top-k queries
prose while the reference query resolves them to a specific       whose ORDER BY key is deterministic. Of these, 24 lacked
URI. With many DBLP authors sharing identical names, the          ORDER BY in 2.0 and received one matching the question’s
intended referent is often unrecoverable from the question        ranking intent (699 + 24 = 723). Reference results are now
text alone: systems with or without entity linking cannot         unique for semantically equivalent queries, up to ties on the
reliably reproduce the reference result.                          ordering key in ranked cases.
   Defective reference queries. 122 reference queries                Reference query repair. Corrected predicates, missing
are trivial echoes of the form SELECT * WHERE {                   GROUP BY, and broken aggregations, verified by execution
VALUES ?x { <uri> } }: they return the URI or string              against the documented endpoint. The 122 VALUES-only
from the question unchanged, testing nothing. Others use          echo queries were replaced with real lookups on the refer-
the wrong predicate for the stated intent (for example            enced entity, preserving each question’s intent.
dblp:createdBy, which includes editors, where the                    Higher-quality natural language. Each machine-
question asks about authorship), omit GROUP BY under ag-          generated question was rewritten for natural phrasing and
gregation, or carry malformed projections.                        unambiguous intent using a frontier model (Claude), re-
   Misdocumented data dependencies. 211 cases require             placing the 8B-model paraphrases of QuAD 2.0. The 8B
OpenCitations citation data. The benchmark’s instruc-             paraphrases were systematically more ambiguous, admitting
tions point to the plain DBLP dump (dblp.org/rdf/),               multiple valid query forms; a per-case pass then amended 547
which contains no citation triples. The required combined         questions that omitted columns, ordering, or scope present
DBLP+OpenCitations dump exists at sparql.dblp.org                 in the reference.
but is not referenced (Ackermann et al. 2024). A system fol-         Explicit entity references. 266 rewritten questions in-
lowing the documentation cannot answer these cases. The           clude bracketed entity URIs that the originals lacked. This is
statistics of Ackermann et al. (2024) imply that only 71%         a deliberate scope decision: QuAD 3.1 evaluates query gen-
of DBLP publications carry an OpenCitations identifier, so        eration, not entity resolution. Where the original question
citation questions have an implicit completeness dependency       named an entity ambiguously (common with author names),
no system can overcome.                                           the URI pins the intended referent so that reference results
   Reproducibility. The endpoint software is unspecified,         are well defined. Systems with entity linking can ignore the
the dump is not archived, and question generation ran on a        brackets; systems without can still be evaluated on query con-
closed institutional service.                                     struction. The convention is not benchmark-only: NLKGQ’s
web interface accepts the same bracketed URIs, giving users           Table 1: Evaluation metrics, reported in this order.
a direct way to pin the intended entity, and an entity linker
could supply them automatically. We report this openly so         Metric           Scoring   Criterion
3.1 scores are not read as directly comparable to 2.0.            Match            binary    generated results contain the refer-
   Documented data dependencies. The combined                                                ence results, equal or superset
DBLP+OpenCitations dump requirement is stated explicitly,         Exact            binary    generated results have an exact match
along with the 71% citation coverage bound. The 28 feder-                                    to reference results
ated cases, whose reference queries issue SERVICE calls to        QuAD F1          graded    set-of-values F1 over all result cells,
live public endpoints, are kept for continuity with QuAD 2.0.                                flattened as in QuAD 2.0’s evaluation
We note that their reference results depend on the availability                              code (Taffa et al. 2025)
and state of third-party SPARQL endpoints.                        SPINACH F1       graded    row-assignment F1 of Liu et al.
                                                                                             (2024), implemented following the
   Release. QuAD 3.1 will be released on GitHub as a self-                                   published code of GRASP (Walter
contained benchmark, independent of NLKGQ: the test cases                                    and Bast 2025)
together with scripts that recreate the evaluation snapshot of
the combined DBLP+OpenCitations graph from persistent
archives (DBLP’s 2025-07-02 RDF release and the DBLP
subset of the OpenCitations Index) and stand up a QLever             The 2.1 row is QuAD 2.0 measured consistently: identi-
instance on which its reference queries execute as published.     cal questions and reference queries, with reference results
                                                                  computed once against the evaluation snapshot rather than
                                                                  re-executed per run. (2.1 is a measurement protocol over the
                        Evaluation                                unchanged 2.0 artifact.) Match and Exact rise, and this row
All experiments: single LLM call, temperature 0.0, no fine-       is our reported QuAD 2.0 result (57.6% Match). Neither F1
tuning, no few-shot examples, no entity linking. SPARQL           column improves (QuAD F1 17.6 to 16.7, SPINACH 17.5 to
queries are executed on QLever (Bast and Buchhold 2017).          17.3): consistent reference results repair some cases outright,
All DBLP results in this paper run against the single fixed       yet the F1 metrics still score answer rows against an arbitrary
snapshot described above. The results are reproducible: mod-      slice of the reference result.
els are open-weight and served locally on AMD APU nodes,             QuAD 3.1 (the two 3.1 rows) replaces the non-
generation at temperature 0.0 is near-deterministic, and re-      deterministic references with deterministic ones, repairs the
peated full-benchmark runs reproduced scores within 0.1           defective queries, and rewrites the questions for unambigu-
points on every deterministic configuration; only QuAD 2.0        ous intent. All four metrics now rise together and largely
with re-executed references varies more (the 52.1–52.9%           agree. The remaining spread between 89.9 Match and 79.0
range above).                                                     SPINACH F1 is partial-credit granularity, not case-level dis-
   Table 1 defines the four metrics we report. Given deter-       agreement.
ministic reference results, Match and Exact are strict and           The progression supports two comparisons. Ontology: on
intuitive: a case either delivers the reference answer or it      QuAD 3.1, the dblpx wrapper adds +15.0 Match and +25.3
does not, which is what a user of the system experiences. We      Exact over the native vocabulary (native vs. wrapper), with
report the two F1 measures for comparability with published       the same model, prompt, and data. The wrapper margin
work, not as quality measures: both award partial credit when     widens on the repaired benchmark (+9.9 to +15.0 Match):
generated and reference results partially overlap, even when      with question ambiguity removed, correct parses that pre-
the question was not answered, and deduct for correct results     viously mismatched the reference are scored as matches.
that include extra rows or columns. QuAD F1 pools all re-         Exact, which forbids supersets, rises more (+25.3 vs. +15.0),
sult cells into one set per side; SPINACH F1 matches row          so Match’s superset tolerance does not drive the gain. With
to row. All reported values are means over the full case set,     the native ontology the model receives a fixed snapshot of
with failed cases (no executable query, or query error) scor-     the DBLP ontology and the rewriter is inactive. Benchmark:
ing zero. To our knowledge, no published system on these          with the dblpx wrapper fixed, the update from 2.0 to 3.1
benchmarks reports stricter than result containment.              moves SPINACH F1 from 17.5 to 79.0. We attribute most
                                                                  of the swing to the deterministic references, with question
From QuAD 2.0 to QuAD 3.1                                         rewriting and URI pinning contributing the rest. The repair
Table 2 traces the path from the benchmark as published to        stages were not separately ablated.
our final configuration. The top row is the reproduction con-
dition: QuAD 2.0 as released, with DBLP’s native ontology.        Cross-Domain Generality
   Adding the dblpx wrapper (2.0-wrapper row) raises              Table 3 shows results across three domains of different evi-
Match and Exact but lowers both F1 measures. The better           dential weight: 1,000 cases on DBLP, 100 on SemOpenAlex,
system scores worse. With non-deterministic references, a         and 21 on neuroimaging metadata, the last inherited from the
correct query returning the full answer set is penalized row      original NLKGQ paper’s purpose-built ontology. The same
for row against an arbitrary 10-row slice, and the dblpx          architecture scores 89.9% Match (reference containment) on
wrapper’s fuller, better-formed results widen that penalty.       the largest and is exact or near-exact on the two smaller
This inversion is the first evidence that on QuAD 2.0 the F1      sets. Where published baselines exist, we compare on the
columns measure the references, not the system.                   baseline’s own metric: on SemOpenAlex our 98/100 com-
Table 2: DBLP progression from QuAD 2.0 with the native          Table 4: Model comparison on QuAD 3.1 + wrapper (t=0.0,
ontology to QuAD 3.1 with the dblpx wrapper. Qwen3.6-            procedural prompt, 1,000 cases). F1Q is QuAD set-of-values
27B, procedural prompt, t=0.0, 1,000 cases, all values %.        F1. F1S is SPINACH row-assignment F1 as used by GRASP.
The 2.0-wrapper row varies run to run under re-executed          All metrics in percent. Fail is the share of cases with no ex-
references (52.1–52.9 Match over five runs; one shown).          ecutable query or query error. *partial runs: Qwen3-14B
                                                                 completed 593 and Qwen3.6-35B 730 of 1,000 cases. Their
  QuAD Ontology Match Exact QuAD F1 SPINACH F1                   percentages are over completed cases. Frequent query time-
                                                                 outs drive their Fail%. Type suffixes: /q FP8-quantized, /code
  2.0     native      43.0   10.7       23.2           23.0
  2.0     wrapper     52.9   11.3       17.6           17.5
                                                                 code-specialized.
  2.1     wrapper     57.6   20.1       16.7           17.3
  3.1     native      74.9   56.0       63.8           62.3        Model              Type       Match Exact F1Q F1S Fail
  3.1     wrapper     89.9   81.3       80.7           79.0        Gemma-4-31B       dense         90.3   75.1 79.4 76.9 3.5
                                                                   Qwen3.6-27B-FP8 dense/q         90.0   81.4 81.3 79.4 2.5
Table 3: Cross-domain results (Qwen3.6-27B, t=0.0; DBLP            Qwen3.6-27B       dense         89.9   81.4 80.8 79.1 3.4
row is the progression run, Table 2). DBLP uses the dblpx          Qwen3-Coder-30B MoE/code        81.1   62.3 69.6 67.9 4.0
wrapper, SemOpenAlex the oax wrapper. The neuroimag-               Mistral-Small-24B dense         80.6   65.2 68.0 64.3 4.7
ing result is the purpose-built-ontology configuration of the      Llama3.3-70B      dense         74.3   59.4 63.6 61.7 5.0
                                                                   Qwen3-8B          dense         66.2   50.6 53.5 51.3 13.2
original NLKGQ paper (Fitch and Kurtz 2026), also with             Qwen3.6-35B-FP8 MoE/q           64.9   52.6 55.1 52.7 25.3
Qwen3.6-27B. Baseline comparisons use the baseline’s own           Qwen3.6-35B*      MoE           50.4   40.3 42.4 40.3 41.5
metric. The DBLP baseline (GRASP) was measured on                  Qwen3-14B*        dense         24.8   19.1 19.3 18.4 68.6
50 samples of the original DBLP-QuAD (see text). F1S is
SPINACH F1, the DBLP baseline’s metric.
                                                                 Gemma-4-31B (90.3%) and Qwen3.6-27B-FP8 (90.0%).
 Domain             Cases Match% Exact% F1S Baseline             Gemma leads on Match only; Qwen3.6-27B is ahead on
 DBLP (QuAD 3.1) 1,000         89.9     81.3 79.0 51.0 F1        Exact (81.4% vs. 75.1%) and both F1 metrics, so Gemma an-
 SemOpenAlex       100         98.0     98.0  — 86/100           swers more questions correctly but more often with a super-
 Neuroimaging       21        100.0    100.0   — —               set of the reference rows rather than the exact result set. That
                                                                 independent LLM families converge at matched size shows
                                                                 the semantics in the context window matter more than the
pares against Bartels et al.’s 86/100 (123B model, few-shot      choice of model family. Mistral-Small-24B, a third family,
with entity mappings) (Bartels, Banerjee, and Usbeck 2025)       reaches 80.6% and beats Llama3.3-70B (74.3%) with a third
on the identical test set. On DBLP our SPINACH F1 of             of the parameters. Scaling from Qwen3-8B (50.6% Exact) to
79.0% compares against GRASP’s 51.0% (GPT-4.1, multi-            Llama3.3-70B (59.4%), a 9× cross-family increase in param-
call exploration), with a caveat: GRASP was measured on the      eters, gains 8.8 Exact points; within the Qwen family, 8B to
original, template-generated DBLP-QuAD (Banerjee et al.          27B gains 30.8 Exact points with 3.4× parameters, confirm-
2023), while our number is on QuAD 3.1, which removes            ing that both scale and training matter. Swapping the native
the entity-resolution and reference-quality confounds doc-       vocabulary for the dblpx wrapper on the 27B model gains
umented above. On 2.0 itself our SPINACH F1 is 17.5              25.3 Exact points (56.0→81.3, Table 2) on top of what scale
(Table 2). The comparison shows what query generation            already provides. The progression run and this sweep differ
achieves once the confounds are removed, not a same-             by 0.1 on Exact and both F1 metrics (81.3 vs. 81.4 Exact),
benchmark ranking; we expect GRASP and other systems             within run-to-run variation. FP8 quantization matches full
also to score higher on QuAD 3.1, which the released bench-      precision. The two general-purpose MoE models show high
mark makes testable.                                             failure rates (25.3% and 41.5%), but the code-specialized
   Auditing the SemOpenAlex test set surfaced two issues.        MoE (Qwen3-Coder-30B) fails only 4.0% of cases, so sparse
One question appears twice (identical ID, text, and query); we   activation alone does not explain the failures. Code-focused
retain the duplicate to preserve the denominator. Seven ques-    training appears to compensate. The neuroimaging results
tions use “papers that X and Y published” with a UNION ref-      follow the general-purpose pattern (35B MoE 57% vs. dense
erence query (meaning: all papers by either author), although    27B 100%, summarized above).
the natural reading is co-authorship. Our two misses gener-
ate the conjunctive reading; disambiguated variants pass.        Error Analysis
Benchmark ambiguity, not system error, sets the ceiling.         All error analysis uses the progression run (899 Match, Ta-
                                                                 ble 2 last row). The main failure modes are data coverage
Model Comparison: The Concept Layer Outweighs                    and federation scope, not vocabulary confusion. Of the 101
Scale                                                            non-matching cases: 24 involve citation queries, where the
Table 4 compares ten models under identical conditions           reference queries return OMID-side entities directly while
(same prompt, ontology, temperature). The most conse-            the wrapper resolves citation endpoints to DBLP publica-
quential result is convergence at the top: two size-matched      tion URIs, so rows diverge wherever the OMID-to-DBLP
dense models from independent families reach 90% Match,          mapping is incomplete (the 71% coverage bound); 22 re-
quire federated SERVICE calls to DBpedia, Wikidata, or            LLM now applies exact matching to DOIs, venue names, and
FactGrid, which the dblpx wrapper does not cover (the             diacritics. In our experiments, rider additions approach zero
other 6 federated cases match: their SERVICE blocks need          sum as the rider matures: once the easy corrections are in,
only well-known vocabularies such as FOAF). Of the rest,          remaining errors can only be reached by prose that disturbs
18 structure an aggregation differently from the reference; 5     cases already correct. Refinement asymptotically approaches
are aggregation queries that failed to execute or timed out;      whack-a-mole. Our interpretation: natural language tokens
3 are ontology introspection queries (“what classes exist”);      are semantically “wide,” activating associations across the
and the remaining 29 are heterogeneous individual errors          LLM’s full vocabulary and shifting generation probabilities
(venue information dumps, type and label listings, and simi-      globally. Formal vocabulary tokens are “narrow”: they par-
lar) with no shared mechanism. The run’s 30 failed cases (no      ticipate in specific patterns without broad activation. This is
executable query, or query error) all lie within these buckets:   why encoding domain knowledge in formal ontology struc-
10 federated, 11 heterogeneous, 5 aggregation, 3 citation,        ture outperforms encoding it in English instructions, and
1 introspection. The sweep run of the same configuration          why the rider is reserved for stable conventions rather than
(Table 4) fails 34, within run-to-run variation.                  incremental repair.
                                                                      Benchmark quality. The 61.5-point SPINACH F1 gap be-
                        Discussion                                tween QuAD 2.0 and QuAD 3.1 (17.5% vs. 79.0%) demon-
The concept layer as the dominant factor. Our results sug-        strates that benchmark defects drive measured performance.
gest a hierarchy for LLM query generation: formal concept             Limitations. The wrapper-vs-native ablation runs on a
transfer > model architecture > model scale > prompt en-          single model (Qwen3.6-27B). The ten-model sweep covers
gineering. The dblpx wrapper’s +25.3 points is additive           four families but only in the dblpx wrapper configuration.
to model scale on the tested model: the 27B model with            We have not tested proprietary models. Every call carries
the native ontology scores 56.0%, so scale and wrapper to-        the complete domain ontology in context. Vocabularies that
gether deliver 81.3%. Prompt wording sits at the bottom:          outgrow the context window would need selection or reduc-
three system prompt variants tied once the vocabulary was         tion, which we do not address. Match accepts supersets of the
right (summarized in the prior-results subsection), and the       reference rows (Exact, 81.3%, is the stricter figure), and the
concept smearing results below show why prose additions           QuAD 3.1 repairs and the evaluated system come from the
cannot be engineered incrementally. Fine-tuning ranks no          same authors. The per-case logs and pre-repair margin above
higher. An exploratory attempt to train the ontology into an      are the available checks. Wrapper ontology design is manual.
8B model was not promising: the model lacks the domain vo-        Entity resolution is deliberately out of scope: 266 QuAD 3.1
cabulary, which the context window supplies, whereas fine-        questions carry bracketed URIs their originals lacked, and
tuning injects new facts slowly and with more hallucination,      unbracketed entity mentions remain unsolved. Inherited data
and erodes skills outside the tuning distribution (Gekhman        limits: only 71% of DBLP publications carry citation iden-
et al. 2024; Ovadia et al. 2024; Kandpal et al. 2023; Kotha,      tifiers, and DBLP’s maintainers note its “BibTeX-inherited
Springer, and Raghunathan 2024). Mecharnia and d’Aquin            classification might no longer be a best fit” (Ackermann et al.
(2025) find that fine-tuning succeeds on readable KGs (DB-        2024), making some publication-type questions ill-posed.
pedia, 61%) but fails on opaque ones (Wikidata, 13%). Fine-
tuning effort is better spent on general SPARQL-writing skill                            Conclusion
than on any one domain’s vocabulary.                              Concepts are more effectively passed to LLMs through for-
   Implications beyond SPARQL. The principle of maxi-             mal mechanisms than through informal description: OWL
mizing the formal semantic precision of the tokens in the         ontologies transfer a database schema’s concepts as seman-
LLM’s context should apply to LLM-based applications that         tically precise tokens that map directly to correct query pat-
generate structured output against a data schema. SQL gener-      terns. Where a native vocabulary is suboptimal, wrapper on-
ation, API call generation, and code generation against typed     tologies substitute precise tokens and a runtime rewriter pre-
interfaces all face the same challenge: the LLM must map          serves compatibility, extending the reusable NLKGQ frame-
natural language intent to formal constructs, and the quality     work from purpose-built domains to existing databases and
of the formal vocabulary it sees determines how well it can       federations. This layer of controlled semantics contributes
do so. The SQL case is measured, not speculative: the neu-        more to accuracy than model scaling or prompt revision,
roimaging experiments of the original NLKGQ paper gener-          tested across three domains and four model families: 89.9%
ated the relational schema from the same ontology, and car-       Match on 1,000 DBLP questions, 98% on SemOpenAlex,
rying the ontology’s annotations into SQL column comments         100% on neuroimaging metadata. The system prompt tunes
lifted SQL accuracy from 43% to 57%. The concept-transfer         query generation; the ontology and rider tune the concepts.
levers act across query formalisms; wrapper ontologies are
one implementation.
   Concept smearing: why prompt refinement becomes                               GenAI Usage Disclosure
whack-a-mole. At temperature 0.0, LLM SPARQL genera-              Generative AI tools assisted with editing, LATEX format-
tion is nearly deterministic, yet any change in prompt tokens     ting, coding, and data analysis. A frontier model rewrote
shifts many queries it did not target. Large case sets expose     the QuAD 3.1 questions; the system under study uses only
this rather than cause it: a “match names exactly” instruction    locally deployed LLMs. All scientific content, experimental
fixes its target cases but breaks unrelated queries where the     design, analysis, and conclusions are the work of the author.
                       References                               Kandpal, N.; Deng, H.; Roberts, A.; Wallace, E.; and Raffel,
Ackermann, M. R.; Bast, H.; Beckermann, B. M.; Kalmbach,        C. 2023. Large Language Models Struggle to Learn Long-
J.; Neises, P.; and Ollinger, S. 2024. The dblp Knowledge       Tail Knowledge. In Proceedings of the 40th International
Graph and SPARQL Endpoint. Transactions on Graph Data           Conference on Machine Learning (ICML), 15696–15707.
and Knowledge, 2(2): 3:1–3:23.                                  Kotha, S.; Springer, J. M.; and Raghunathan, A. 2024. Un-
Banerjee, D.; Awale, S.; Usbeck, R.; and Biemann, C.            derstanding Catastrophic Forgetting in Language Models via
2023. DBLP-QuAD: A Question Answering Dataset over              Implicit Inference. In The Twelfth International Conference
the DBLP Scholarly Knowledge Graph. In Proceedings of           on Learning Representations (ICLR). ArXiv:2309.10105.
the 13th International Workshop on Bibliometric-enhanced        Liu, S.; Semnani, S. J.; Triedman, H.; Xu, J.; Zhao, I. D.;
Information Retrieval (BIR 2023) co-located with ECIR           and Lam, M. S. 2024. SPINACH: SPARQL-Based Informa-
2023, volume 3617 of CEUR Workshop Proceedings, 37–             tion Navigation for Challenging Real-World Questions. In
51. ArXiv:2303.13351.                                           Findings of the Association for Computational Linguistics:
Bartels, M. C.; Banerjee, D.; and Usbeck, R. 2025. Au-          EMNLP 2024, 15977–16001.
tomating SPARQL Query Translations between DBpedia and          Mecharnia, T.; and d’Aquin, M. 2025. Performance and
Wikidata. In Linking Meaning: Semantic Technologies Shap-       Limitations of Fine-Tuned LLMs in SPARQL Query Gener-
ing the Future of AI. Proceedings of the 21st International     ation. In Proceedings of the Workshop on Generative AI and
Conference on Semantic Systems (SEMANTiCS 2025), vol-           Knowledge Graphs (GenAIK) at COLING 2025, 69–77.
ume 62 of Studies on the Semantic Web, 176–193. IOS Press.      OpenAI. 2026. OpenAI API Reference: Chat Comple-
ArXiv:2507.10045.                                               tions. https://platform.openai.com/docs/api-reference/chat.
Bast, H.; and Buchhold, B. 2017. QLever: A Query Engine         Accessed 2026-09-13.
for Efficient SPARQL+Text Search. In Proceedings of the         Ovadia, O.; Brief, M.; Mishaeli, M.; and Elisha, O. 2024.
2017 ACM on Conference on Information and Knowledge             Fine-Tuning or Retrieval? Comparing Knowledge Injection
Management (CIKM), 647–656.                                     in LLMs. In Proceedings of the 2024 Conference on Em-
Dobriy, D.; Bauer, F.; Azzam, A.; Banerjee, D.; and Polleres,   pirical Methods in Natural Language Processing (EMNLP),
A. 2026. Agentic SPARQL: Evaluating SPARQL-MCP-                 237–250.
powered Intelligent Agents on the Federated KGQA Bench-         Pan, X.; de Boer, V.; and van Ossenbruggen, J. 2025. FIRES-
mark. arXiv preprint arXiv:2603.06582.                          PARQL: A LLM-based Framework for SPARQL Query Gen-
Doulaverakis, C.; Vassiliou, G.; Batsakis, S.; Papadakis, N.;   eration over Scholarly Knowledge Graphs. In Proceedings
Trouli, G. E.; and Antoniou, G. 2025. SPARQL Query Gen-         of the 17th International Joint Conference on Knowledge
eration Using LLMs for Medical Information Retrieval. In        Discovery, Knowledge Engineering and Knowledge Man-
The Semantic Web: ESWC 2025 Satellite Events, Lecture           agement (IC3K), Volume 1: KDIR, 123–134. SCITEPRESS.
Notes in Computer Science, 40–44. Springer.                     ArXiv:2508.10467.
Emonet, V.; Bolleman, J.; Duvaud, S.; Mendes de Farias, T.;     Peroni, S.; and Shotton, D. 2020. OpenCitations, an in-
and Sima, A.-C. 2024. LLM-based SPARQL Query Gen-               frastructure organization for open scholarship. Quantitative
eration from Natural Language over Federated Knowledge          Science Studies, 1(1): 428–444.
Graphs. In Proceedings of the Special Session on Harmonis-      Sequeda, J.; Allemang, D.; and Jacob, B. 2024. A Bench-
ing Generative AI and Semantic Web Technologies (HGAIS          mark to Understand the Role of Knowledge Graphs on Large
2024), co-located with ISWC 2024, volume 3953 of CEUR           Language Model’s Accuracy for Question Answering on En-
Workshop Proceedings. Paper 355. arXiv:2410.06062.              terprise SQL Databases. In Proceedings of the 7th Joint
Färber, M.; Lamprecht, D.; Krause, J.; Aung, L.; and Haase,     Workshop on Graph Data Management Experiences & Sys-
P. 2023. SemOpenAlex: The Scientific Landscape in 26            tems (GRADES) and Network Data Analytics (NDA), 1–12.
Billion RDF Triples. In The Semantic Web – ISWC 2023,           ACM. ArXiv:2311.07509.
Lecture Notes in Computer Science, 94–112. Springer.            Smeros, P.; Emonet, V.; Wang, R.; Sima, A.-C.; and
Fitch, B. G.; and Kurtz, C. E. 2026. Natural Language Access    Mendes de Farias, T. 2025. SPARQL-LLM: Real-Time
to Domain-Specific Metadata: A Reusable Framework for           SPARQL Query Generation from Natural Language Ques-
LLM Query Generation. arXiv preprint arXiv:2607.18029.          tions. arXiv preprint arXiv:2512.14277. Under review.
Gashkov, A.; Perevalov, A.; Eltsova, M.; and Both, A. 2025.     Taffa, T. A.; Neises, P.; Ollinger, S.; Westphal, P.; Ackermann,
SPARQL Query Generation with LLMs: Measuring the Im-            M. R.; Banerjee, D.; and Usbeck, R. 2025. DBLP QuAD 2.0:
pact of Training Data Memorization and Knowledge Injec-         Scholarly Natural Questions from SPARQL. In Proceedings
tion. In Web Engineering (ICWE 2025), Lecture Notes in          of the Knowledge Capture Conference (K-CAP ’25), 236–
Computer Science, 177–192. Springer. ArXiv:2507.13859.          240. ACM.
Gekhman, Z.; Yona, G.; Aharoni, R.; Eyal, M.; Feder, A.;        Walter, S.; and Bast, H. 2025. GRASP: Generic Reason-
Reichart, R.; and Herzig, J. 2024. Does Fine-Tuning LLMs on     ing And SPARQL Generation across Knowledge Graphs.
New Knowledge Encourage Hallucinations? In Proceedings          In The Semantic Web – ISWC 2025, volume 16140 of
of the 2024 Conference on Empirical Methods in Natural          Lecture Notes in Computer Science, 271–289. Springer.
Language Processing (EMNLP), 7765–7784.                         ArXiv:2507.08107.
Walter, S.; and Bast, H. 2026. GRISP: Guided Recur-
rent IRI Selection over SPARQL Skeletons. arXiv preprint
arXiv:2604.21133.
Xiao, G.; Calvanese, D.; Kontchakov, R.; Lembo, D.; Poggi,
A.; Rosati, R.; and Zakharyaschev, M. 2018. Ontology-Based
Data Access: A Survey. In Proceedings of the 27th Interna-
tional Joint Conference on Artificial Intelligence (IJCAI),
5511–5519.
Zhang, S. H.; Miao, Z.; and Wang, J. 2026. The Case for Text-
to-SQL Friendly Logical Database Design. arXiv preprint
arXiv:2606.03145.

