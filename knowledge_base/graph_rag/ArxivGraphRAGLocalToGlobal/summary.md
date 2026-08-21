> [[index|Wiki]] | [[digest|Digest]]

# From Local to Global: A Graph RAG Approach to Query-Focused Summarization

**Paper:** [From Local to Global: A Graph RAG Approach to Query-Focused Summarization (Edge et al., 2024)](https://arxiv.org/abs/2404.16130)

Conventional "vector RAG" retrieves a handful of text chunks similar to a query and answers from those alone — great for fact lookup, useless for questions that require understanding an entire corpus at once (e.g. "what are the main themes here?"). This is the **sensemaking problem**, and it's the reason a chatbot over your company's documents can answer "when did we sign contract X?" but not "what are the recurring risks across all our contracts?"

**GraphRAG's fix:** use an LLM to build a knowledge graph from the corpus (entities as nodes, relationships as edges), partition that graph into a hierarchy of topic **communities** using the Leiden algorithm, have an LLM write a summary of each community bottom-up, and answer global queries with **map-reduce**: every relevant community summary produces a partial answer in parallel (map), and those partial answers are merged into one final answer (reduce).

**Results:** on two ~1M-token corpora (podcast transcripts, news articles), GraphRAG's community-summary conditions beat a vector-RAG baseline 72–83% of the time on *comprehensiveness* and 62–82% on *diversity* (p<.001), while vector RAG keeps the edge on *directness* (shorter, more to-the-point answers) and *empowerment* is a wash. Root-level community summaries alone are competitive with fuller graph-detail levels while using 9–43x fewer tokens per query — the practical sweet spot for repeated global queries over the same dataset.

**Caveats:** evaluated on only two corpora with GPT-4-turbo; no ablation isolating the contribution of community detection itself vs. just having graph-structured summaries; results rely on LLM-as-judge, which the paper itself validates against extracted-claim counts (78%/69–70% agreement) rather than human judgment.

For more:
- [[digest|Digest]] — medium-depth pass, ~10 min
- [[wiki/01-introduction-and-background|Wiki]] — deep dive, chapter by chapter
