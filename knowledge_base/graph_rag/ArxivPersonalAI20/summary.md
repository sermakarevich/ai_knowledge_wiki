> [[index|Wiki]] | [[digest|Digest]]

# PersonalAI 2.0 (PAI-2) — Summary

**Paper:** [PersonalAI 2.0: Enhancing knowledge graph traversal/retrieval with planning mechanism for Personalized LLM Agents (Menschikov et al., 2026)](https://arxiv.org/abs/2605.13481)

## What it is

PAI-2 is a GraphRAG (graph-based Retrieval-Augmented Generation) system: it stores knowledge as a graph and lets a large language model (LLM) plan, step by step, how to search that graph to answer a question. The core idea is that a *dynamic, LLM-planned* search — rather than a single flat retrieval pass — handles multi-hop questions (ones that need several linked facts) far better.

## How it works, in brief

A question is preprocessed and split into independent sub-questions. For each sub-question, the LLM writes a natural-language "search plan" (a sequence of steps), extracts entities from each step, matches them to graph vertices, generates "clue-queries" to explore from those vertices, traverses the graph, filters the retrieved facts for relevance, and summarizes what it learned. A decision step checks whether enough is known to answer; if not, the plan is revised and the loop continues (up to a step limit) before all sub-answers are aggregated into a final response.

## Key results

- On six QA benchmarks (Natural Questions, TriviaQA, HotpotQA, 2WikiMultihopQA, MuSiQue, DiaASQ), PAI-2 beats LightRAG, RAPTOR and HippoRAG 2 with an average +4% LLM-as-a-Judge score gain (best on 4 of 6 benchmarks).
- The planning mechanism itself (vs. disabling it) is responsible for +18% of that gain; smarter graph-traversal algorithms add another +6% over a naive flat retriever.
- On the MINE-1 benchmark (measuring how much factual information survives being turned into a graph and back), PAI-2 reaches state-of-the-art with an 89% information-retention score, and its graph-construction process is more stable (fewer parsing errors) than competing methods.

## Limitations

The authors flag four concrete weaknesses in their memory design: timestamps are stored as plain text (risking loss in long contexts), the graph's category structure ("ontology") is too simple for efficient filtering, entities aren't formally disambiguated (causing wasted search on ambiguous terms), and duplicate facts aren't merged except by exact string match.

## Why it matters

It's evidence that *how* an LLM searches a knowledge graph — planning and adapting mid-search — matters more than the graph-traversal algorithm alone, for personalized agents that need to reason over long-term structured memory.

**Read next:** [[digest|Digest]] for a fuller pass, or dive into the [[index|Wiki]] for chapter-by-chapter detail.
