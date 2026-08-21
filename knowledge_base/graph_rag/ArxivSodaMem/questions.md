---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: SodaMem

Answer from memory before opening any answer. Run sessions with `kb show summary/quiz`.

### Q1. What are the four failure modes (P1–P4) that SodaMem argues flat RAG and Markdown-log memories leave unresolved?

> [!tip]- Answer
> (P1) Currency/conflict — preferences reverse and it's unclear which stored value is current; (P2) temporal structure — ordering and relative-date questions break without a comparable timeline; (P3) provenance — lossy summaries and vector hits can't be traced back to a source; (P4) association — multi-hop synthesis needs entity/claim links beyond cosine similarity. See [[wiki/01-motivation-and-related-work|Motivation & Related Work]].

### Q2. On LongMemEval-S, what accuracy and mean cost-per-question did SodaMem's store-of-record configuration achieve, and with which model?

> [!tip]- Answer
> 92.8% accuracy (464/500, best of N=3) at a mean of $0.00161 per question (~18.3k tokens; median $0.00111 / ~14.6k), using deepseek-v4-flash as planner, reader, and judge. See [[wiki/03-evaluation-and-results|Evaluation & Results]].

### Q3. What do the SUPERSEDES, CONTRADICTS, and UPDATES edges mean, and when are they created?

> [!tip]- Answer
> They are typed edges between FactEvents created at write time: SUPERSEDES marks that a new fact deterministically replaces an old one on a competing subject–predicate slot (closing the old fact's validity interval); CONTRADICTS and UPDATES capture other detected relationships between competing or evolving facts. Currency is handled structurally at write time, not inferred by the reader at answer time. See [[wiki/02-method-sodamem|Method: SodaMem]].

### Q4. Why does SodaMem use a "soft time bonus" for query time windows instead of a hard temporal filter?

> [!tip]- Answer
> Users often misremember time windows (e.g. saying "two months ago" about a fact that's actually three months old). A hard filter would exclude the correct evidence in that case. Instead, SodaMem parses the query into a window + sort direction and adds a bonus (β, default 0.3) to a candidate's ranking confidence if it falls in the window, rather than excluding out-of-window candidates outright — keeping misdated queries recoverable. See [[wiki/02-method-sodamem|Method: SodaMem]].

### Q5. Why does SodaMem fuse three retrieval "tunnels" (graph/entity, BM25, embedding) by connection density instead of ranking by cosine similarity alone?

> [!tip]- Answer
> Single-channel retrieval is brittle: embeddings can retrieve "episode-wrong" but similar-sounding memories, BM25 can miss paraphrases, and entity-graph expansion alone can explode into irrelevant neighbors. By awarding mass to an evidence ID whenever any tunnel/head hits it and summing that mass into a density score, a fact that's corroborated by multiple independent signals ranks above one that merely looks similar by one channel — reducing the risk of confidently retrieving the wrong (similar-but-outdated) memory. See [[wiki/01-motivation-and-related-work|Motivation & Related Work]] and [[wiki/02-method-sodamem|Method: SodaMem]].

### Q6. What is the "provenance hard constraint" applied during ingest, and what does it reject?

> [!tip]- Answer
> During ingest, an LLM extracts FactEvent candidates from dialogue, but any candidate whose cited source span does not literally occur in the source turn text is rejected outright — it's a hard constraint, not a soft preference for citations. This guarantees every stored fact carries a verifiable quote it can be traced back to. See [[wiki/02-method-sodamem|Method: SodaMem]].

### Q7. Why does SodaMem separate the "planner" from the "reader" instead of having one model both search and answer?

> [!tip]- Answer
> The planner's job is to call memory tools (search, inspect, session-expand, timeline, count, compute) under a step budget to grow the pool of evidence when initial retrieval isn't enough (e.g. explicit enumeration questions). The reader's separate job is to compose the final answer strictly from the selected evidence IDs with mandatory citations. Splitting them keeps citation discipline separate from tool-use policy, so the model deciding what to search for isn't the same model responsible for staying grounded in the results. See [[wiki/02-method-sodamem|Method: SodaMem]].

### Q8. The paper's own critical analysis flags self-grading as a limitation. Given that the same Flash model serves as planner, reader, and judge, what is the strongest reason to treat the 92.8% figure as directional rather than final — and what would most directly test it?

> [!tip]- Answer
> Self-grading lets a model systematically favor its own phrasing and reasoning style, inflating measured accuracy relative to what an independent judge would score — this is a known bias in LLM-as-judge evaluation, not specific to SodaMem. The paper itself notes released hypotheses "support re-evaluation," meaning the most direct test is re-scoring the same released answers with an independent judge model (e.g. GPT-4o) and seeing whether 92.8% holds, rises, or falls. Cost figures are unaffected by this concern since they're judge-independent. See [[critical_thinking|Critical Analysis]].
