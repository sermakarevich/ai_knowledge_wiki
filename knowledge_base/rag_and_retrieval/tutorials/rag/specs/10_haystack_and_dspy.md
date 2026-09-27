# Task: chapter 10 — Haystack 2 pipelines and DSPy prompt optimisation

Read `specs/COMMON.md`, `index.md`, chapters 00–09 first (cwd `/Users/sergii/.ai/knowledge/research_topics/rag_and_retrieval/tutorials/rag`).
Research: `specs/research/frameworks.md` (Haystack and DSPy sections; installed versions win).

## Problem
Haystack is the production-oriented pipeline framework (explicit typed components, serialisable
pipelines); DSPy replaces hand-written prompts with *programs* whose prompts are optimised against a
metric — a genuinely different trick to improve a RAG system. The reader should try both on our set.

## Fix

### `project/src/rag_tutorial/fw_haystack.py` (Typer CLI: `index`, `ask`, `eval`) — dependency group `haystack`
`haystack-ai`, `ollama-haystack`, `qdrant-haystack` (or the in-memory document store + our Chroma —
pick what installs; Qdrant preferred since we run it), `sentence-transformers` for the ranker.
1. Indexing pipeline: `MarkdownToDocument`/`TextFileToDocument` → `DocumentSplitter`
   (`split_by="word"/"sentence"`, map to our ids via `meta["split_id"]`/offsets — document what is
   available) → `OllamaDocumentEmbedder` → `DocumentWriter` (Qdrant with hybrid enabled).
2. Query pipeline: `OllamaTextEmbedder` → `QdrantHybridRetriever` (or `InMemoryBM25Retriever` +
   `InMemoryEmbeddingRetriever` → `DocumentJoiner(join_mode="reciprocal_rank_fusion")`) →
   `SentenceTransformersSimilarityRanker`/`TransformersSimilarityRanker` (`bge-reranker-v2-m3`) →
   `ChatPromptBuilder` → `OllamaChatGenerator` → `AnswerBuilder`. Rows `10_hs_hybrid`,
   `10_hs_hybrid_rerank`. Draw the pipeline (`pipeline.draw()` needs a network service — use
   `pipeline.show()`'s mermaid text or `to_dict()` → mermaid by hand).
3. Haystack evaluators (`FaithfulnessEvaluator`, `ContextRelevanceEvaluator`, `DocumentMRREvaluator`,
   `DocumentRecallEvaluator`) with Ollama — run on `10_hs_hybrid_rerank`, compare with our judge
   (agreement table), note any that require OpenAI-style APIs (Ollama's OpenAI-compatible endpoint
   `…/v1` may work — try it).
4. Serialise the pipeline to YAML (`dumps`) and load it back — show the YAML excerpt in the chapter.

### `project/src/rag_tutorial/fw_dspy.py` (Typer CLI: `baseline`, `optimize`, `eval`) — dependency group `dspy`
`dspy` with `dspy.LM("ollama_chat/qwen3.8:27b", api_base=settings.ollama_url, temperature=0,
cache=True)` (DSPy has its own disk cache — point it under `data/cache/dspy`).
1. A `RAG(dspy.Module)` with our chapter-07 best retriever (hybrid + rerank, k=5) as a plain Python
   retriever and `dspy.ChainOfThought("context, question -> answer")`. Row `10_dspy_zero_shot`.
2. Metric: our `judge_correctness` (dev split, ~10 questions — small on purpose; discuss the
   overfitting risk) — or a cheaper exact/semantic-match metric if the judge is too slow inside the
   optimiser; say which.
3. Optimise with `dspy.BootstrapFewShot` (cheap) and `dspy.MIPROv2(auto="light")` on the dev split
   → evaluate on the test split → rows `10_dspy_bootstrap`, `10_dspy_mipro`. Save the optimised
   program JSON (`program.save(...)`) and show the *learned prompt/instructions and few-shot demos* in
   the chapter — this is the interesting artefact. Count LLM calls used by optimisation.
4. Optionally `dspy.Refine`/assertions for citation format.

### Tests `project/tests/test_10_haystack_dspy.py`
Haystack pipeline builds and runs with a fake generator component and the in-memory store; DSPy
module runs with `dspy.utils.DummyLM` (verify the current name). No network.

### `10_haystack_and_dspy.md` (chapter)
Haystack's mental model (components with typed sockets, pipelines as graphs, document stores), the
two pipeline diagrams, YAML serialisation, evaluator agreement; DSPy's mental model (signatures,
modules, optimisers, "programming not prompting"), the before/after prompts verbatim, the dev/test
numbers and the optimisation cost; "What changed on the scoreboard"; "Advantages and disadvantages"
tables for both (Haystack: explicitness, production features, smaller ecosystem than LangChain;
DSPy: measurable prompt improvement, needs an eval set, optimisation cost, opacity of learned
prompts); Troubleshooting; Exercises.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/rag_tutorial/{fw_haystack,fw_dspy}.py`, `project/pyproject.toml`,
`project/uv.lock`, `project/justfile`, `project/data/cache/**`, `project/runs/10_*/**`
(incl. the saved DSPy program), `project/runs/scoreboard.md`, `project/tests/test_10_haystack_dspy.py`,
`10_haystack_and_dspy.md`. Verify token `"What you will learn"`.

## Scope & constraints
No hosted services (deepset Cloud, etc.). Keep optimisation budgets small (≤ 400 LLM calls per optimiser run).
