---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: From Local to Global (GraphRAG)

Answer from memory before opening any answer. Run sessions with `kb show summary/quiz`.

### Q1. What is a "sensemaking query," and why does it break conventional vector RAG?

> [!tip]- Answer
> A sensemaking query requires reasoning over connections across an entire dataset (e.g. "what are the main themes here?") rather than a fact localized in a few records. Vector RAG retrieves only a small set of chunks semantically similar to the query, so it can never see enough of the corpus to answer a question about the whole thing. See [[wiki/01-introduction-and-background|Introduction and Background]].

### Q2. Walk through GraphRAG's indexing pipeline from raw text to community summaries — what happens at each step?

> [!tip]- Answer
> Source documents are split into text chunks; an LLM extracts entities, relationships, and claims from each chunk (abstractive summarization); duplicate mentions are aggregated into graph nodes/edges (duplicate counts become edge weights); Leiden community detection recursively partitions the graph into a hierarchy of communities; starting from leaf communities, an LLM writes report-like summaries bottom-up, with higher levels substituting shorter sub-community summaries for element summaries once the context window fills up. See [[wiki/02-graphrag-methodology|GraphRAG Methodology]].

### Q3. Why does the paper prioritize community elements by "combined source+target node degree" when building leaf-level summaries, rather than, say, chronological order?

> [!tip]- Answer
> Node degree (how many connections an entity has) is a proxy for how prominent/central that entity is to the community. Since the context window has a token limit and not all element summaries can fit, prioritizing by degree ensures the most structurally important entities and relationships are captured first, rather than whichever happened to be extracted earliest. See [[wiki/02-graphrag-methodology|GraphRAG Methodology]].

### Q4. On the two evaluation datasets, which conditions won on comprehensiveness and diversity, and which won on directness — and why isn't that a contradiction?

> [!tip]- Answer
> The GraphRAG community-summary conditions (C0-C3) and the graph-free map-reduce baseline (TS) beat vector RAG (SS) decisively on comprehensiveness (72-83% win rates) and diversity (62-82%), because they synthesize across many sources. SS wins on directness because it gives short, to-the-point answers rather than broad surveys. This isn't a contradiction — the paper explicitly designed Directness as a control criterion in opposition to Comprehensiveness/Diversity, so no method should win on all four. See [[wiki/03-experimental-setup-and-results|Experimental Setup and Results]].

### Q5. Experiment 2 used claim extraction (Claimify) as an independent validation method — what did it show, and where did it partially disagree with Experiment 1's LLM-judge results?

> [!tip]- Answer
> It confirmed the main direction: C0-C3 and TS all significantly beat SS on claim-based comprehensiveness (p<.05) in both datasets, largely agreeing with Experiment 1. But on diversity in the News dataset, only C0 significantly beat SS by claim clustering, while Experiment 1's LLM judge had found all global conditions significantly beating SS — a partial disagreement between the two validation methods (about 30-31% non-tie rate, with 69-70% agreement where both gave a clear verdict). See [[wiki/03-experimental-setup-and-results|Experimental Setup and Results]].

### Q6. The paper explicitly flags that fabrication rates were never measured. Why does this matter given GraphRAG's own stated motivation, and what would you need to check before trusting a deployed GraphRAG system?

> [!tip]- Answer
> The paper's own broader-impact argument is that GraphRAG *reduces* the risk of a sensemaking answer misrepresenting the source data compared to vector RAG's "unrepresentative sample presented as summary" failure mode — but that claim about hallucination/fabrication was never actually measured (e.g. via SelfCheckGPT), so it remains an assumption rather than a demonstrated result. Before trusting a deployment, you'd want a fabrication/faithfulness audit of both the extraction step (does the graph correctly represent the source) and the final answer generation step. See [[wiki/04-discussion-and-conclusion|Discussion and Conclusion]].

### Q7. Why did the authors settle on an 8k-token context window for query-time answer generation, when the underlying model (gpt-4-turbo) supports up to 128k tokens?

> [!tip]- Answer
> They tested 8k, 16k, 32k, and 64k windows and found the smallest (8k) was universally best for comprehensiveness (58.1% average win rate) and comparable on diversity/empowerment — likely due to the "lost in the middle" effect, where models handle long contexts by underweighting information buried in the middle rather than at the start or end. More context isn't automatically better; it can dilute the model's ability to use the most relevant summaries. See [[wiki/05-appendix-prompts-and-additional-experiments|Appendix: Prompts and Additional Experiments]].

### Q8. The evaluation prompts enforce a strict grounding/citation discipline (e.g. `[Data: Reports (1, 3, ...); +more]`, max 5 record ids, explicit "do not include unsupported information"). What failure mode is this rule specifically designed to prevent, and is it sufficient on its own?

> [!tip]- Answer
> It's designed to prevent the LLM from asserting claims that aren't traceable back to a specific extracted entity/relationship/claim record — i.e., to force answers to cite their evidence and make unsupported statements detectable/rejectable. It is a prompt-level instruction, not a hard technical guarantee: nothing in the pipeline verifies at generation time that a cited record ID actually supports the sentence it's attached to, which is exactly the "unmeasured fabrication rate" gap raised in [[critical_thinking|Critical Analysis]]. See [[wiki/05-appendix-prompts-and-additional-experiments|Appendix: Prompts and Additional Experiments]].
