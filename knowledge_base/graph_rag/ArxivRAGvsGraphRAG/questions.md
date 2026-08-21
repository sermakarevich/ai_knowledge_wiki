---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# RAG vs. GraphRAG — Retrieval Practice

Answer from memory first. Expand a callout only after you've committed to an answer.

## 1. (Core recall) What is the paper's central complementarity finding, and which task type does each paradigm win?

> [!tip]- Answer
> RAG and GraphRAG show complementary rather than dominant strengths: RAG wins single-hop, detail-oriented factual QA (e.g., Natural Questions), while GraphRAG wins multi-hop, reasoning-intensive QA (e.g., HotPotQA, MultiHop-RAG Comparison/Temporal categories) and produces more corpus-level, diverse summaries. See [[wiki/01-introduction-and-evaluation-framework]] and [[wiki/02-question-answering-results]].

## 2. (Core recall) Why does KG-based GraphRAG underperform on QA, according to the paper's diagnosis?

> [!tip]- Answer
> Its constructed knowledge graph has incomplete entity coverage — only about 65.8% of HotPotQA answer entities and 65.5% of NQ answer entities actually appear in the graph, so many correct answers simply aren't retrievable from the graph at all (Appendix C, Table 16). See [[wiki/02-question-answering-results]] and [[wiki/04-appendix-datasets-and-case-studies]].

## 3. (Elaboration) What is the difference between Community-GraphRAG's "Local" and "Global" search modes, and how does that difference show up in the results?

> [!tip]- Answer
> Local search retrieves fine-grained entity neighborhoods and lower-level community reports; Global search retrieves only high-level, corpus-wide community summaries. Local tracks closer to RAG's detail-oriented performance, while Global sacrifices detail for breadth — it does poorly on detail-oriented QA and NULL/abstention queries but helps on Comparison/Temporal multi-hop QA and broad summarization diversity. See [[wiki/02-question-answering-results]].

## 4. (Core recall) What did the LLM-as-a-Judge position-bias experiment show, and on which criteria?

> [!tip]- Answer
> Running the same pairwise comparison twice — once with RAG shown first, once with GraphRAG shown first — produced substantially different, sometimes opposite, preferences (Figure 4), most pronounced for RAG vs. GraphRAG-Local. On Comprehensiveness, RAG was consistently preferred; on Diversity, GraphRAG-Global was favored. This means judge-based comparisons without order controls can be misleading. See [[wiki/03-summarization-and-conclusion]].

## 5. (Elaboration) On reference-based summarization metrics (ROUGE-2, BERTScore), how did GraphRAG variants compare to RAG, and why?

> [!tip]- Answer
> Vanilla RAG, RaptorRAG, and HippoRAG2 generally matched human-written ground-truth summaries better than most GraphRAG variants, because they retrieve original text chunks that stay close to the reference detail. KG-GraphRAG needed to add raw text alongside triplets to compete; Community-GraphRAG did much better with Local search than Global, since Global's high-level summaries lose the query-specific detail these datasets reward. See [[wiki/03-summarization-and-conclusion]].

## 6. (Transfer) You're building a support-ticket QA system where most questions are simple lookups ("what's our refund policy for X") but a growing minority require connecting a policy change to an older ticket. Based on this paper, what retrieval architecture decision would you make, and why?

> [!tip]- Answer
> Given the finding that RAG wins detail lookups and GraphRAG wins multi-hop reasoning, and that Selection/Integration hybrids consistently beat either alone, a reasonable design is: use plain RAG as the default (cheap, matches most queries), and add a lightweight query classifier that routes the minority of "connect facts across time/policy versions" queries to a GraphRAG-style retrieval path (or runs Integration for just those queries) — avoiding the full construction/latency/storage cost of GraphRAG on every query. See [[wiki/02-question-answering-results]] and [[critical_thinking]].

## 7. (Transfer) The paper reports that Community-GraphRAG retrieves ~2.3× more tokens than RAG for the same query set. What are the practical implications of this for a production system with a fixed LLM context/cost budget?

> [!tip]- Answer
> More retrieved tokens per query means higher per-query generation cost and latency, and less headroom for other context (conversation history, system prompts, few-shot examples). The paper's token-matched control experiments show that giving RAG the same extra token budget closes most (but not all) of the gap on some benchmarks, meaning some of GraphRAG's apparent advantage is architecture-driven (how it organizes evidence) rather than purely "more context helps." A production system should budget for this multiplier before adopting GraphRAG at scale. See [[wiki/04-appendix-datasets-and-case-studies]].

## 8. (Evaluation, critical thinking) Why should you be skeptical of a benchmark result claiming "GraphRAG beats RAG" (or vice versa) if it doesn't report the graph-construction model, the token budget, and the evaluation method used?

> [!tip]- Answer
> This paper shows all three of those variables independently move the outcome: stronger graph-construction LLMs (GPT-4o vs. GPT-4o-mini) measurably improve GraphRAG's scores; token-matching RAG to GraphRAG's retrieval budget partially closes gaps that looked like architectural advantages; and LLM-as-a-Judge scores flip with presentation order. A benchmark claim that omits these levers could be reporting an artifact of its specific setup rather than a durable property of RAG vs. GraphRAG. See [[critical_thinking]] and [[wiki/04-appendix-datasets-and-case-studies]].
