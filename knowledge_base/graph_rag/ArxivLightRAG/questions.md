---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: LightRAG

Answer from memory before opening any answer. Run sessions with `kb show summary/quiz`.

### Q1. What are the two structural limitations of existing RAG systems that LightRAG's introduction identifies, and why does chunk-based retrieval make them worse?

> [!tip]- Answer
> (1) Flat data representations — chunking discards the relationships between entities described across chunks; (2) lack of contextual awareness — the system can retrieve individually relevant chunks but cannot synthesize how they causally interact (e.g., EVs → air quality → transit planning), producing a fragmented answer. See [[wiki/01-introduction-and-motivation|Introduction and Motivation]].

### Q2. Walk through LightRAG's three-step graph-based indexing pipeline (R, P, D) and state what each step produces.

> [!tip]- Answer
> R(·) extracts entities and relationships from each document chunk via an LLM prompt; P(·) generates a text key-value profile for every node and edge (index key + descriptive summary); D(·) deduplicates identical entities/relations found across different chunks, merging them into one graph. The output is the deduplicated knowledge graph D̂ = Dedupe ⊗ Prof(V, E). See [[wiki/02-lightrag-architecture|The LightRAG Architecture]].

### Q3. A query like "Who wrote 'Pride and Prejudice'?" and a query like "How does AI influence modern education?" are handled by two different retrieval paths in LightRAG. Name each path and explain why the split exists.

> [!tip]- Answer
> The first is a low-level (specific) query, handled by low-level retrieval, which matches local keywords against candidate entities and their direct attributes/relationships. The second is a high-level (abstract) query, handled by high-level retrieval, which matches global keywords against relations tied to broad themes across many entities. The split exists because a single retrieval strategy cannot serve both detail-oriented and broad, thematic questions well. See [[wiki/02-lightrag-architecture|The LightRAG Architecture]].

### Q4. On the Legal dataset, why does GraphRAG's retrieval phase cost roughly 610,000 tokens and hundreds of API calls, while LightRAG's costs fewer than 100 tokens and one API call?

> [!tip]- Answer
> GraphRAG must traverse and read summaries for the 610 level-2 communities actively used in retrieval (each averaging 1,000 tokens), requiring many sequential API calls. LightRAG instead extracts local/global keywords from the query with a single LLM call and does direct vector search over graph entities/relations plus a one-hop neighbor expansion — no community traversal. See [[wiki/04-ablation-case-study-cost-analysis|Ablation Studies, Case Study, and Cost/Adaptability Analysis (RQ2-RQ4)]].

### Q5. The ablation study found that removing the original source text from the generation context (the -Origin variant) did not hurt performance, and sometimes improved it. Why would dropping the raw text help rather than hurt?

> [!tip]- Answer
> The graph-based indexing step already extracts and summarizes the key information relevant to entities and relations into their profiles, so that signal survives without the raw text. Meanwhile the original text often contains irrelevant or noisy content that can distract the generator LLM, so removing it can slightly improve focus. See [[wiki/04-ablation-case-study-cost-analysis|Ablation Studies, Case Study, and Cost/Adaptability Analysis (RQ2-RQ4)]].

### Q6. LightRAG loses to GraphRAG on the Mix dataset's Overall and Empowerment metrics, even though it wins on the other three datasets. What is the Mix dataset, and what does the paper say caused this loss?

> [!tip]- Answer
> Mix is a corpus of literary, biographical, and philosophical texts (61 documents, 619,009 tokens) — the smallest of the four and stylistically the most different from the other three (Agriculture/CS/Legal are technical/domain corpora). The paper does not explain the loss; it is an acknowledged-but-unexplained gap rather than a diagnosed cause. See [[wiki/03-evaluation-setup-and-main-results|Evaluation Setup and Main Results (RQ1)]] and [[critical_thinking|Critical Analysis]].

### Q7. Suppose you had a customer-support knowledge base that receives ~500 new support articles every week. How would LightRAG's incremental update mechanism change your system design compared to using GraphRAG?

> [!tip]- Answer
> With LightRAG, each week's new articles are indexed once (entity/relation extraction) and merged into the existing graph by simple set union of nodes and edges — the update cost scales only with the new documents' extraction cost. With GraphRAG, adding new documents would require dismantling and fully regenerating the affected community structure across the whole corpus, an expense that grows with total corpus size, not just the new batch — making frequent updates impractical at scale. See [[wiki/04-ablation-case-study-cost-analysis|Ablation Studies, Case Study, and Cost/Adaptability Analysis (RQ2-RQ4)]].

### Q8. The paper's evaluation relies entirely on LLM-as-judge (GPT-4o-mini) win rates rather than human judges or a ground-truth answer set. What is the strongest reason to be skeptical of the reported win-rate numbers, and does that undermine the paper's core architectural claims?

> [!tip]- Answer
> The strongest reason for skepticism: the same model family judging the comparison may share systematic biases with the models generating the compared answers (e.g., preferring longer, more structured, or more "comprehensive-sounding" answers regardless of actual correctness), and there's no ground-truth check on factual accuracy. This weakens confidence in the exact win-rate magnitudes, but it does not fully undermine the architectural claims, since the cost analysis (token counts, API calls) is measured directly and independently of the judge, and the ablation's internal comparisons (LightRAge variants against each other) are more robust to judge bias than absolute cross-method rankings. See [[critical_thinking|Critical Analysis]].
