---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: MemGraphRAG

Answer from memory before opening any answer. Run sessions with `kb show summary/quiz`.

### Q1. Why can adding a knowledge graph to RAG sometimes make answer quality *worse* than plain vanilla RAG, according to the preliminary study?

> [!tip]- Answer
> GraphRAG methods raise retrieval Recall (e.g. GFM-RAG 84.3% vs. vanilla RAG 71.8% on G-Medical) but crash Relevance (38.5% vs. 62.9%) — they pull in more of the needed evidence, but bury it in a much larger amount of irrelevant content, producing noisier context that degrades generation accuracy. See [[wiki/01-motivation-and-problem|Motivation, Problem Statement, and Preliminary Study]].

### Q2. What are the three types of conflicts that independent, chunk-isolated extraction introduces into a knowledge graph, and give a one-line example of each?

> [!tip]- Answer
> Mutually exclusive (e.g. two incompatible birth years for the same person, "1643" vs "1645"), temporal (facts valid at different times stored without timestamps, e.g. conflicting presidents at different years), and granularity (the same entity described at inconsistent levels of detail, e.g. "born in Shanghai" vs "born in China"). See [[wiki/01-motivation-and-problem|Motivation, Problem Statement, and Preliminary Study]] and [[wiki/04-related-work-and-appendix|Related Work and Appendix Details]].

### Q3. Describe the roles of the three agents in MemGraphRAG's Multi-Agent Group and explain why the work is split between them instead of one agent doing everything.

> [!tip]- Answer
> The Extraction Agent (A_ext) writes candidate schemas, facts, and passages into the three memory layers; the Conflict Detection Agent (A_det) purely diagnoses by scanning for conflicts (never modifies the graph); the Conflict Resolution Agent (A_res) is the only one that fixes conflicts, using retrieved provenance passages as evidence. Splitting extraction, diagnosis, and correction keeps each agent's task simple and auditable, and lets resolution be evidence-driven rather than an ad hoc correction bundled into extraction. See [[wiki/02-memgraphrag-framework|The MemGraphRAG Framework and Experimental Results]].

### Q4. Why does a schema need to reach a frequency threshold τ before it becomes "stable," and what would happen to the graph if this threshold were removed?

> [!tip]- Answer
> New schemas start as unverified "candidates"; only once a schema's extraction frequency across the corpus crosses τ is it promoted to "stable," and only facts aligned with stable schemas get activated into the graph. This is how thematic irrelevance is filtered: one-off, off-topic relationship types never accumulate enough frequency to graduate. Removing the threshold (as the ablation shows: "w/o Schema Filter" drops HotpotQA accuracy to 68.10% and G-Medical to 65.92%) lets low-frequency, off-topic schemas flood the graph with noisy triples that weaken semantic focus. See [[wiki/02-memgraphrag-framework|The MemGraphRAG Framework and Experimental Results]].

### Q5. In the retrieval-time node initialization, why do type nodes get a "hub suppression" term (dividing by log(deg(t)+1)) that entity nodes don't need?

> [!tip]- Answer
> Type nodes (like "Person") can be connected to thousands of entities, so without correction their high degree would let them dominate the Personalized PageRank propagation and spread importance too broadly across irrelevant nodes. Entity nodes don't have this problem to the same degree because their importance is already grounded directly in specific retrieved facts (mean similarity over facts containing the entity), not in a generic, corpus-wide category. See [[wiki/02-memgraphrag-framework|The MemGraphRAG Framework and Experimental Results]] and [[wiki/04-related-work-and-appendix|Related Work and Appendix Details]].

### Q6. What does the "adaptability" experiment (Q3, Table 3) demonstrate that the main generation-accuracy experiment (Q1, Table 1) does not, and why does this strengthen the paper's central claim?

> [!tip]- Answer
> It shows that swapping MemGraphRAG's constructed graph into other frameworks' own retrieval/reasoning pipelines (HippoRAG, HippoRAG2, MS-GraphRAG, LazyGraphRAG) improves every one of them on every dataset, proving the *graph itself* is higher quality — independent of MemGraphRAG's own retrieval algorithm. Without this, a skeptic could argue MemGraphRAG's gains came only from its retrieval method (PPR with tuned node initialization) rather than from better graph construction. See [[wiki/02-memgraphrag-framework|The MemGraphRAG Framework and Experimental Results]].

### Q7. Which single ablated component causes the largest accuracy drop on HotpotQA, and what does that ranking imply about which of the paper's two core design goals (thematic denoising vs. consistency maintenance) matters more?

> [!tip]- Answer
> Removing Conflict Resolution (Global Adjudication) causes the largest drop (69.40% → 66.95%), ahead of removing Schema Filter (→68.10%), Hub Suppression (→67.22%), or the Information Density term (→68.67%). This implies consistency maintenance (resolving contradictions) is a slightly larger driver of accuracy than thematic denoising (filtering irrelevant triples) on this dataset, though both — plus the retrieval-side mechanisms — are shown to be jointly necessary. See [[wiki/02-memgraphrag-framework|The MemGraphRAG Framework and Experimental Results]].

### Q8. Where is this paper's evidence weakest, and what claim should be trusted the least as a result?

> [!tip]- Answer
> The graph-topology claim (higher Average Degree and Clustering Coefficient are "better") is asserted without demonstrating that density/clustering causally drives the accuracy gains, rather than simply correlating with a system that also has better conflict resolution; a denser but noisier graph is not obviously superior on its own. See [[critical_thinking|Critical Analysis]] for the full claims-vs-evidence breakdown.
