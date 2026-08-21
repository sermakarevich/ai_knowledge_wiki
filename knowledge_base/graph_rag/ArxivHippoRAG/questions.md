---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# HippoRAG — Retrieval Practice

Answer from memory before expanding each answer. See [[wiki/01-introduction|Introduction]] through [[wiki/06-appendix-pipeline-errors|Appendix]] for full detail.

**Q1.** Why can't standard RAG answer "path-finding" multi-hop questions like "Which Stanford professor works on the neuroscience of Alzheimer's?" even with a perfect retriever?

<details><summary>Answer</summary>
Because each passage is encoded and retrieved in isolation — no single passage co-mentions both "Stanford" and "Alzheimer's," so there is nothing for a similarity-based retriever to match against the full query. The answer only emerges by combining two separate passages through a shared entity, which isolated-passage retrieval cannot do. (wiki/01-introduction)
</details>

**Q2.** What is the hippocampal memory indexing theory, and what two brain structures does HippoRAG map onto its own two components?

<details><summary>Answer</summary>
The theory (Teyler & Discenna) holds that the neocortex stores actual memory representations while the C-shaped hippocampus holds an index of interconnected associations pointing to those representations, enabling recall from partial cues. HippoRAG maps the neocortex to the LLM (which processes text into entities/triples) and the hippocampus to its knowledge graph + Personalized PageRank (which stores and traverses associations). (wiki/01-introduction)
</details>

**Q3.** Walk through HippoRAG's offline indexing pipeline: what are the two LLM steps run on each passage, and what do synonymy edges add?

<details><summary>Answer</summary>
First, the LLM extracts named entities from the passage (1-shot prompt); those entities are then fed into an OpenIE prompt to extract final (subject, relation, object) triples, forming noun-phrase nodes and relation edges — this two-step process balances generality against bias toward named entities. Separately, a retrieval encoder adds synonymy edges between any two node representations with cosine similarity above a threshold τ, mimicking parahippocampal regions and improving pattern completion at retrieval time. (wiki/02-methodology)
</details>

**Q4.** How does online retrieval turn a query into a passage ranking, and what role does node specificity play?

<details><summary>Answer</summary>
The LLM extracts named entities from the query; each is matched to its highest-cosine-similarity KG node to form the query nodes. Personalized PageRank runs starting from an equal-probability distribution over just those query nodes (zero elsewhere), producing an updated distribution over all nodes; multiplying that by the node-passage count matrix gives a per-passage ranking score. Node specificity (s_i = |P_i|^-1, inverse to how many passages a node appears in) is multiplied into each query node's starting probability before PPR, so rare/distinctive entities (e.g., "Stanford") get more weight than common ones. (wiki/02-methodology)
</details>

**Q5.** On which benchmark does HippoRAG's single-step retrieval NOT outperform the best baseline, and why?

<details><summary>Answer</summary>
HotpotQA — ColBERTv2 still edges out HippoRAG there (R@2 64.7 vs 60.5, R@5 79.3 vs 77.7). This is attributed to HotpotQA's lower knowledge-integration demands (it's a weaker multi-hop test with many spurious signals) and a concepts-vs-context tradeoff where HippoRAG's entity-centric design underperforms on more context-dependent questions; ensembling with a dense retriever partially closes this gap. (wiki/03-experiments-results)
</details>

**Q6.** What efficiency advantage does single-step HippoRAG have over the multi-step baseline IRCoT, and where does that advantage come from mechanically?

<details><summary>Answer</summary>
HippoRAG's online retrieval is 10–30x cheaper and 6–13x faster than IRCoT while matching or beating its QA performance. Mechanically, IRCoT re-runs the LLM at every reasoning step to decide what to retrieve next, while HippoRAG only calls the LLM once per query (to extract named entities) and then does a cheap graph algorithm (PPR) — all the expensive LLM work happened once, offline, during indexing. (wiki/03-experiments-results, wiki/04-discussions)
</details>

**Q7.** What happens to retrieval quality when GPT-3.5's OpenIE is replaced by REBEL, and what explains the gap?

<details><summary>Answer</summary>
Average recall drops sharply (Avg R@2 46.2 vs HippoRAG's 57.4; MuSiQue R@2 31.7 vs 40.9). GPT-3.5 produces roughly twice as many triples as REBEL, and REBEL is biased against extracting triples involving general concepts (not just named entities), leaving many useful associations out of the graph. Open-weight Llama-3.1-70B, by contrast, is competitive with or beats GPT-3.5 on 2 of 3 datasets. (wiki/04-discussions)
</details>

**Q8.** The paper measures "all-recall" (percentage of queries where ALL supporting passages are retrieved). What does the growing gap between HippoRAG and ColBERTv2 as k increases (R@2 → R@5) actually demonstrate?

<details><summary>Answer</summary>
On 2WikiMultiHopQA the gap grows from 20% (AR@2) to 38% (AR@5), and on MuSiQue from 3% to 6%. This shows HippoRAG's advantage isn't just retrieving more relevant passages spread thinly across more questions — it's specifically retrieving the *complete set* of supporting passages needed to answer multi-hop questions, which is exactly the knowledge-integration capability the paper claims. (wiki/04-discussions)
</details>

**Q9.** How does HippoRAG's approach to incorporating new information differ from RAPTOR, MemWalker, and GraphRAG, all of which also index knowledge offline?

<details><summary>Answer</summary>
RAPTOR, MemWalker, and GraphRAG integrate knowledge by summarizing groups of passages during indexing, so adding new data requires redoing summarization. HippoRAG integrates new knowledge incrementally by simply adding new nodes/edges to its knowledge graph — no re-summarization step is needed. (wiki/05-related-work-conclusion)
</details>

**Q10.** List the paper's own four stated limitations.

<details><summary>Answer</summary>
(1) All components (NER, OpenIE, PPR, the LLM) are used off-the-shelf without any task-specific fine-tuning, despite most errors stemming from NER and OpenIE. (2) Graph search is plain Personalized PageRank, which ignores the semantics of the relation labels themselves. (3) OpenIE consistency (triple-extraction quality) degrades on longer documents. (4) Scalability of the knowledge graph far beyond current benchmark sizes remains empirically unproven, even though Llama-3.1 makes indexing cheaper. (wiki/05-related-work-conclusion)
</details>

**Q11.** In the worked pipeline example (Appendix), why does HippoRAG rank the *Vila Franca de Xira* passage highly even though it never mentions "Alhandra" being born there directly by name?

<details><summary>Answer</summary>
Because PPR seeds probability on the "Alhandra" node (extracted from the query) and that probability spreads through the graph edge "Alhandra → born in → Vila Franca de Xira" created during indexing; "Vila Franca de Xira" then accumulates the largest share of neighboring PPR mass (≈0.05) of any node besides the seed itself, and since that node's passage describes it as being in the Lisbon District, the passage-level score (mass summed via the node–passage matrix) ranks it second overall — surfacing the answer without any passage having to state the full multi-hop fact explicitly. (wiki/06-appendix-pipeline-errors)
</details>

**Q12.** In the qualitative path-finding case study, why does IRCoT fail to identify "Black Hawk Down" as the war film directed by someone known for sci-fi and crime films?

<details><summary>Answer</summary>
IRCoT does retrieve Ridley Scott mostly through the LLM's parametric (pre-trained) knowledge rather than the corpus, and its chain-of-thought reasoning gets split between exploring two candidate directors (Ridley Scott and Denis Villeneuve). Combined with a three-step iteration limit on its retrieval loop, it never resolves down to the specific film Black Hawk Down, whereas HippoRAG's graph-based association retrieves it within the first four passages. (wiki/06-appendix-pipeline-errors)
</details>
