# RAG tutorial — reader Q&A

Short answers to questions readers actually ask, each pointing to the chapter with the full story.

## Which framework should I start with?

Start with no framework: chapter [03_baseline_rag.md](03_baseline_rag.md) builds naive RAG in ~150 lines, and it scores 0.435 correctness — the baseline everything else is measured against. Of the real frameworks, Haystack's hybrid pipeline (0.696, chapter [10_haystack_and_dspy.md](10_haystack_and_dspy.md)) and LlamaIndex query fusion + rerank (0.652, chapter [09_llamaindex.md](09_llamaindex.md)) beat LangChain's equivalents on our scoreboard, but the differences are mostly configuration, not destiny — pick the one whose API style you like and copy the winning config (hybrid retrieval, k≈20 pool, cross-encoder rerank to 5).

## Why is my hybrid search worse than dense?

Almost always a fusion or pool-size trap, not a verdict on hybrid. In chapter [05_retrieval_hybrid_search.md](05_retrieval_hybrid_search.md) plain hybrid-RRF at k=5 (0.565) barely beats dense (0.500), but widening the pool to k=10 jumps to 0.696 — and the LangChain ensemble in chapter [08_langchain_langgraph.md](08_langchain_langgraph.md) lost purely because its pool was too small. Check that both branches (dense + BM25 (Best Matching 25 — a classic keyword scorer)) return enough candidates before fusion, and use RRF (Reciprocal Rank Fusion — a simple formula that merges ranked lists) or a weighted blend rather than trusting one branch.

## How do I add my own documents?

Parse them to Markdown (chapter [02_corpus_and_golden_set.md](02_corpus_and_golden_set.md) found `pymupdf4llm` the best of three parsers), chunk with the chapter-04 winner for your budget (sentence-window or parent–child, see [04_chunking.md](04_chunking.md)), embed, and index — then write one `evaluate_run` experiment (chapter [02_corpus_and_golden_set.md](02_corpus_and_golden_set.md)) with 10–20 of your own questions so the new corpus gets its own scoreboard rows. Keep chunk ids deterministic (hash of document + offsets) so retrieval metrics stay comparable across strategies.

## How much does it cost to re-run everything from scratch without the cache?

One full test-split evaluation costs ≈ 27 generations + ≈ 60–90 judge calls ≈ 10–15 minutes of shared-GPU (Graphics Processing Unit) time (see `specs/COMMON.md` via [00_setup.md](00_setup.md)). The committed disk cache under `project/data/cache/` (41,630 entries) makes re-runs of `just scoreboard` cost zero LLM (Large Language Model) calls and ~4 seconds — so a cold rerun of all 65 experiments is hours, while a cached rerun is seconds. Never run an uncached batch of 100+ calls without `just gpu-check` first; the RTX 4090 box is shared.

## Which single trick helped the most?

Cross-encoder reranking over a wide hybrid pool: `bge-reranker-v2-m3` over a k=20 hybrid pool reaches 0.674 correctness in 0.155 s/q (chapter [07_reranking_and_query_transforms.md](07_reranking_and_query_transforms.md)) — the best quality-per-second on the Pareto frontier. DSPy zero-shot prompting reaches the outright best (0.739) with no retrieval change at all (chapter [10_haystack_and_dspy.md](10_haystack_and_dspy.md)). Both beat every chunking, query-rewriting, and agentic-loop trick we measured.

## Do I need a reranker, or is hybrid retrieval enough?

Hybrid-RRF at k=10 alone gets you to 0.696 correctness (chapter [05_retrieval_hybrid_search.md](05_retrieval_hybrid_search.md)), so if you can only afford one upgrade over naive RAG, do hybrid first. A CPU (Central Processing Unit) cross-encoder reranker on top adds roughly +0.01–0.11 depending on the pool and costs milliseconds per question (chapter [07_reranking_and_query_transforms.md](07_reranking_and_query_transforms.md)) — add it second, and skip LLM-based listwise reranking unless single/multi-hop accuracy is worth ~18 s/q to you.

## When is graph RAG worth it?

Not for factoid-heavy corpora like ours: all five LightRAG modes scored 0.065–0.130 correctness, below answering from memory (0.174), while costing 1–3 hours of graph indexing (chapter [11_graph_rag_systems.md](11_graph_rag_systems.md)). Collapsed-tree RAPTOR at k=10 (0.522) only tied the best global-question score. Consider graph RAG when your questions are genuinely global ("what are the themes across everything") and you can afford the indexing bill — otherwise hybrid + rerank wins for less.

## How do I know my judge scores mean anything?

Calibrate the judge the way chapter [13_evaluation_and_production.md](13_evaluation_and_production.md) does: a 25-item human spot-check for agreement, a seed-stability rerun, and a synthetic-question leak check, plus RAGAS (Retrieval-Augmented Generation Assessment Suite — an open-source library of RAG metrics) computed with the same local judge for a second opinion. Note the ceiling effect we measured: even handed the gold evidence (the oracle anchor), the judge only awards 0.543 correctness, so judge scores are comparative (run A vs run B) rather than absolute grades.

## Should I just use a long context window instead of RAG?

Chapter [13_evaluation_and_production.md](13_evaluation_and_production.md) runs that exact experiment, and the Lost-in-the-Middle effect (models ignoring the middle of long inputs) shows up: stuffing everything into context is slower, pricier per question, and weaker on multi-hop questions than retrieving 5 good chunks. Use long context for small corpora where everything fits cheaply; use RAG once retrieval + rerank demonstrably beats the long-context row on your own golden set.

## What should I do before putting RAG into production?

Follow the production checklist in chapter [13_evaluation_and_production.md](13_evaluation_and_production.md): incremental ingestion updates (never full re-indexes), caching at every layer, latency/cost monitoring with the scoreboard columns (hit@5, correctness, faithfulness, s/q, LLM calls/q), guardrails including a prompt-injection demo with verbatim transcripts, access control and PII (Personally Identifiable Information — names, emails, and other data that identifies someone) handling, and a cost model per question. Then re-run the golden set on a schedule — the `evaluate_run` contract in `project/src/rag_tutorial/evaluate.py` makes every new config one comparable scoreboard row.
