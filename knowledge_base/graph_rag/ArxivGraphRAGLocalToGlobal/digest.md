> [[index|Wiki]] | [[summary|Summary]]

# From Local to Global: A Graph RAG Approach to Query-Focused Summarization — Digest

The whole paper at medium depth: every wiki page's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-introduction-and-background|Introduction and Background]]

**In one sentence:** Vector RAG answers only local fact-retrieval queries because it fetches a small set of semantically similar records, so it cannot handle global sensemaking questions (e.g. "What are the main themes in the dataset?") — GraphRAG solves this by using an LLM to build an entity knowledge graph, partitioning it into a hierarchy of communities, and summarizing those communities in a map-reduce fashion to produce a global answer.

- RAG (Lewis et al., 2020) exists because data is too large for the LLM's context window (the maximum number of tokens processed at once); in canonical ("vector") RAG, records semantically similar to the query are retrieved, and an answer is generated from the query plus those records alone.
- Vector RAG fails on sensemaking queries — queries requiring global understanding of the entire dataset, e.g. "What are the key trends in how scientific discoveries are influenced by interdisciplinary research over the past decade?" — because sensemaking (Klein et al., 2006) requires reasoning over connections among people, places, and events, and the corpus is too large to put in one prompt.
- GraphRAG's pipeline: (1) an LLM derives an entity knowledge graph (nodes = key entities, edges = relationships); (2) the graph is partitioned into a hierarchy of communities of closely related entities; (3) LLM-generated community summaries are produced bottom-up, higher levels recursively incorporating lower-level summaries; (4) queries are answered by map-reduce — each community summary yields a partial answer in parallel (map), then partial answers are combined into a final global answer (reduce).
- Results: for global sensemaking questions over datasets in the 1 million token range, GraphRAG substantially outperforms a conventional vector RAG baseline in both comprehensiveness and diversity of answers, when using GPT-4 as the LLM.
- Evaluation novelty: an LLM-as-a-judge technique (Zheng et al., 2024) adapted for broad-issue questions with no ground-truth answer — one LLM generates diverse sensemaking questions from corpus-specific use cases, a second LLM judges the two systems' answers against predefined criteria (Section 3.3).
- Background 2.1: RAG = any system where a user query retrieves external information that is incorporated into generation; it's ideal when the data source exceeds the LLM's context window. Embedding-based vector similarity retrieval (Gao et al., 2023) defines the "vector RAG" family GraphRAG contrasts with.
- Background 2.2: GraphRAG belongs to recent LLM-based knowledge-graph extraction work and adds to RAG approaches that use a knowledge graph as an index (Gao et al., 2023); its novel ingredient is the graph's inherent modularity (Newman, 2006) — partitioning into nested modular communities (e.g. Louvain, Blondel et al. 2008; Leiden, Traag et al. 2019) and building globally recursive summaries over that hierarchy.
- Background 2.3/2.4 (RAG evaluation): existing QA benchmarks (HotPotQA, MultiHop-RAG, MT-Bench) target explicit fact retrieval, not global sensemaking; GraphRAG instead uses adaptive benchmarking — LLM-generated persona-based, corpus-specific sensemaking queries — and LLM-as-a-judge comparative evaluation with criteria like "fluency", avoiding corpus-specific vector RAG criteria ("context relevance", "faithfulness", "answer relevance", RAGAS) that don't apply to global sensemaking.

## 2. [[wiki/02-graphrag-methodology|GraphRAG Methodology]]

**In one sentence:** GraphRAG converts a corpus into a hierarchically summarized knowledge graph — extracting entities, relationships, and claims from text chunks, clustering them into Leiden communities at multiple levels, and writing community summaries bottom-up — then answers global sensemaking queries by a map-reduce process that scores and aggregates parallel community-level answers.

- The indexing pipeline has six steps (3.1.1–3.1.6): source documents → text chunks → entities & relationships → knowledge graph → graph communities → community summaries → community answers → global answer.
- Chunk size is a fundamental design decision: longer chunks need fewer LLM extraction calls (lower cost) but suffer degraded recall of information appearing early in the chunk (a recall–precision trade-off).
- Entity/relationship/claim extraction is abstractive summarization: LLMs generate short descriptions, including relationships and claims that may not be explicitly stated; duplicates of the same element are aggregated into nodes/edges with the number of duplicates becoming edge weights.
- Graph communities are found with Leiden community detection, applied hierarchically and recursively until leaf communities can no longer be partitioned; each level yields a partition that is mutually exclusive and collectively exhaustive, enabling divide-and-conquer global summarization.
- Community summaries are generated bottom-up: leaf-level element summaries are prioritized and iteratively added to the LLM context window until the token limit is reached (prioritized by combined source+target node degree in decreasing order); higher-level communities substitute shorter sub-community summaries for longer element summaries until they fit the context window.
- Global query answering is map-reduce: community summaries at a chosen level are shuffled and chunked (distributing relevant information across chunks), each chunk produces a parallel intermediate answer with a 0–100 helpfulness score (score-0 answers filtered out), then answers are sorted by helpfulness and iteratively added into a new context window until the token limit, from which the final global answer is generated.
- Evaluation question generation uses the formula K × N × M: an LLM describes K user personas, N tasks per user, and M high-level questions per (user, task) pair; in this work K = M = N = 5, giving 125 test questions per dataset.
- Evaluation uses an LLM head-to-head judge with three target criteria — Comprehensiveness, Diversity, Empowerment — plus a control criterion, Directness; no method is expected to win across all four, since Directness opposes Comprehensiveness and Diversity.

## 3. [[wiki/03-experimental-setup-and-results|Experimental Setup and Results]]

**In one sentence:** GraphRAG's global approaches (C0–C3) win over vector RAG on comprehensiveness and diversity, validated two ways — LLM pairwise win rates and claim-based measures.

- Podcast transcript dataset: 1669 × 600-token chunks with 100-token overlap (∼1M tokens); news articles dataset: 3197 × 600-token chunks with 100-token overlap (∼1.7M tokens).
- Six conditions compared: C0–C3 (GraphRAG community summaries at four hierarchy levels), TS (map-reduce text summarization without a graph), and SS (vector RAG semantic search).
- Global approaches beat vector RAG (SS) on comprehensiveness with 72–83% win rates (p<.001) on Podcast and 72–80% (p<.001) on News; diversity win rates were 75–82% (p<.001) and 62–71% (p<.01) respectively.
- Directness (validity check): SS produced the most direct responses across all comparisons; the C-conditions are weaker on directness.
- Empowerment: mixed results — no consistent advantage for global approaches over SS or for GraphRAG over TS.
- Graph sizes: Podcast 8,564 nodes / 20,691 edges; News 15,754 nodes / 19,520 edges.
- Experiment 2: 47,075 unique claims extracted (avg 31 per answer); C0–C3 and TS all significantly outperformed SS on claim-based comprehensiveness (p<.05) in both datasets; diversity advantage held only for C0 across all distance thresholds in News.
- Indexing took 281 minutes for the Podcast dataset (600-token window) on a VM (16GB RAM, Intel Xeon Platinum 8171M, 2.60GHz) using a public OpenAI endpoint (gpt-4-turbo, 2M TPM, 10k RPM).

## 4. [[wiki/04-discussion-and-conclusion|Discussion and Conclusion]]

**In one sentence:** The paper's overall takeaway is that combining knowledge graph generation with query-focused summarization (QFS) supports sensemaking over entire corpora and outperforms vector RAG on answer comprehensiveness and diversity at a fraction of the token cost, while honestly acknowledging that evaluation covered only two sensemaking corpora of ~1M tokens each and that fabrication rates were not measured.

- Evaluation so far focused on sensemaking questions over just two corpora (news articles and podcast transcripts), each with approximately 1 million tokens; generalization to other domains and use cases is untested.
- Fabrication rates were not measured; the authors note that comparing them, e.g. with SelfCheckGPT (Manakul et al., 2023), would strengthen the analysis.
- Future work includes embedding-based, more local RAG matching against graph annotations, hybrid schemes with just-in-time community report generation before map-reduce summarization, multi-level "roll-up," and an exploratory "drill down" that follows the information scent in higher-level community summaries.
- The authors flag broader-impact risks: if generated answers do not accurately represent source data, downstream sensemaking and decision-making can be harmed, so use should be accompanied by clear disclosures of AI use and potential errors.
- They argue that, compared to vector RAG, GraphRAG mitigates such risks for global questions that might otherwise be answered by samples of retrieved facts falsely presented as global summaries.
- Conclusion: summaries of root-level communities in the entity-based graph index make a data index superior to vector RAG and competitive with other global methods at a fraction of the token cost, for workloads with many global queries over the same dataset.

## 5. [[wiki/05-appendix-prompts-and-additional-experiments|Appendix: Prompts and Additional Experiments]]

**In one sentence:** These appendices supply the implementation details — exact prompt templates for graph construction and global search, the four evaluation criteria and their wording, and the full statistical methodology — plus supplementary experiments (chunk-size/self-reflection trade-offs, a community-detection example, context-window sizing, and a worked assessment example) that back up the main paper's claims.

- **Chunk size vs. recall (Figure 3):** With a generic entity-extraction prompt and gpt-4-turbo on HotPotQA, smaller chunks (600 tokens) initially detect more entity references than larger ones (2400 tokens), but self-reflection iterations close the gap — by iteration 3, all chunk sizes converge to ≈20k–28k detected references, with 600 tokens still slightly ahead.
- **Hierarchical communities (Figure 4):** Leiden clustering (Traag et al., 2019) over the MultiHop-RAG entity graph yields a clean two-level hierarchy — level 0 gives the maximum-modularity root communities, level 1 splits them into sub-communities revealing internal structure.
- **Context window (Appendix C):** The authors tested 8k, 16k, 32k, and 64k-token context windows for query-time LLM use and found the smallest (8k) universally best for comprehensiveness (average win rate 58.1%), while performing comparably on diversity (52.4%) and empowerment (51.3%) — likely due to "lost in the middle" effects in long contexts.
- **Grounding discipline in prompts:** Generation prompts enforce strict grounding — data references in `[Data: Reports (1, 3, ...)]` format, max 5 record ids per reference with "+more" appended, and an explicit "do not include information where the supporting evidence is not provided."
- **Helpfulness scoring (Appendix E.4):** The global answer generation prompt requires the model to prepend an integer 0–100 self-assessed helpfulness score in `<ANSWER HELPFULNESS>...</ANSWER HELPFULNESS>` tags before the answer.
- **Evaluation rubric (Appendix F):** Pairwise assessments judge answers on four criteria — comprehensiveness, diversity, directness, empowerment — each with a detailed textual definition and example, returning a JSON `{"winner": 1|2|0, "reasoning": "..."}`.
- **Statistics (Appendix G):** Win/lose scoring (winner=100, loser=0, tie=50 per question and metric), averaged over five evaluation runs; Shapiro-Wilk rejected normality, so Wilcoxon signed-rank tests with Holm-Bonferroni correction were used for pairwise significance (125 questions × 2 datasets × 4 metrics).
- **Condition naming in the stats:** C0–C3 are the graph-RAG (local-to-global) conditions, TS = text summarization, SS = semantic search baselines; C0–C3 and TS decisively beat SS on comprehensiveness and diversity in nearly every pairwise comparison, but SS won back the lead on directness.

## The argument in five moves

1. Vector RAG only ever retrieves a small set of records, so it structurally cannot answer questions that require understanding an entire corpus (sensemaking queries).
2. GraphRAG fixes this by having an LLM build a knowledge graph of entities and relationships from the corpus, then partitioning that graph into a hierarchy of Leiden communities.
3. An LLM writes a summary for every community, bottom-up, so the corpus is compressed into a small set of pre-computed, thematic summaries at multiple levels of granularity.
4. A global query is answered by map-reduce over those community summaries: each summary independently produces a scored partial answer (map), and the best-scoring partial answers are merged into one final answer (reduce).
5. On two ~1M-token corpora, this beats vector RAG on comprehensiveness and diversity by wide margins (p<.001), loses only on directness/conciseness, and root-level summaries alone deliver most of the benefit at 9–43x lower token cost — making GraphRAG a practical choice specifically for workloads with many repeated global queries over the same dataset, not a universal RAG replacement.
