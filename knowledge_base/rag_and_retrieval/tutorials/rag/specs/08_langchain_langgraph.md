# Task: chapter 08 — LangChain and LangGraph: the same pipeline in the most popular framework, plus agentic RAG

Read `specs/COMMON.md`, `index.md`, chapters 00–07 first (cwd `/Users/sergii/.ai/knowledge/research_topics/rag_and_retrieval/tutorials/rag`).
Research: `specs/research/frameworks.md` (LangChain section — package names and the *current* API; the
installed version wins over the note).

## Problem
Most RAG code in the wild is LangChain. The reader should see how our hand-built pieces map onto
LangChain's abstractions, what LangChain adds for free (retriever classes, loaders, LCEL composition,
LangGraph control flow), what it costs (abstraction, churn), and how it scores on the same golden set.

## Fix

### `project/src/rag_tutorial/fw_langchain.py` (Typer CLI: `index`, `ask`, `eval`) — new dependency group `langchain`
Install the packages named in the research note (`langchain`, `langchain-core`, `langchain-community`
or `langchain-classic` as required by the installed major version, `langchain-ollama`,
`langchain-chroma`, `langchain-text-splitters`, `langgraph`, `rank_bm25` if `BM25Retriever` needs it).
Point `ChatOllama`/`OllamaEmbeddings` at `settings.ollama_url`; `temperature=0`, `seed=42`,
`num_ctx=16384`. **Caching**: use LangChain's `set_llm_cache(SQLiteCache("data/cache/langchain.sqlite"))`
for chat and `CacheBackedEmbeddings` with a `LocalFileStore("data/cache/langchain_embed")` — commit
both so re-runs are free. Count LLM calls with a callback handler.
1. **Plain RAG in LCEL**: `TextLoader`/our Markdown → `MarkdownHeaderTextSplitter` +
   `RecursiveCharacterTextSplitter` (≈ our `markdown` chunker; map metadata so our chunk ids can be
   recomputed from `paper,start,end` — if positions are not available, compute ids by hashing the
   text and note the consequence for metrics) → `Chroma` → `retriever` → prompt → `ChatOllama` →
   `StrOutputParser`. Experiment `08_lc_naive`.
2. **Retriever classes**: `ParentDocumentRetriever` (`08_lc_parent`), `MultiQueryRetriever`
   (`08_lc_multiquery`), `EnsembleRetriever` (BM25 + dense = hybrid; `08_lc_ensemble`),
   `ContextualCompressionRetriever` with `CrossEncoderReranker` (`langchain_community`'s
   `HuggingFaceCrossEncoder`, `bge-reranker-v2-m3`; `08_lc_ensemble_rerank`). Optionally
   `SelfQueryRetriever` for metadata filters if it works with Ollama structured output.
3. **LangGraph agentic RAG** (`08_lg_crag`): a graph following the Corrective-RAG / Adaptive-RAG
   templates: route (answer directly for unanswerable-looking / retrieve) → retrieve → grade each
   document (LLM yes/no) → if too few relevant: rewrite the query and retry once (max 2 loops) →
   generate → check hallucination/groundedness (LLM) → if ungrounded regenerate once. Draw the graph
   (mermaid; LangGraph can also emit one). Count calls per question (it will be 8–15).
   Show the `unanswerable` abstain rate — the grader should help here.
4. `ask` prints the retrieved docs and answer like chapter 03.

### Experiments
`08_lc_naive`, `08_lc_parent`, `08_lc_multiquery`, `08_lc_ensemble`, `08_lc_ensemble_rerank`, `08_lg_crag`.
Compare `08_lc_ensemble_rerank` with our own `07_hybrid_k20_ce_bge_k5` — same idea, two
implementations; explain any gap (splitter differences, BM25 tokenisation, prompt).

### Tests `project/tests/test_08_langchain.py`
Build the LCEL chain with `FakeListChatModel` and `FakeEmbeddings` (LangChain's own fakes) on a
3-document in-memory store and assert the output contains the canned answer; the LangGraph graph
compiles and runs one path with fakes; the id-mapping helper. No network.

### `08_langchain_langgraph.md` (chapter)
What LangChain is (Runnables, LCEL `|`, the ecosystem of integrations), a side-by-side of our 03 code
vs the LCEL version; the retriever zoo with one-paragraph explanations and which chapter of ours each
corresponds to; LangGraph: state, nodes, edges, why an agentic loop is a graph, the real trace of one
question (which nodes fired, how many calls); "What changed on the scoreboard" (all six rows next to
our best from 07 and the anchors); "Advantages and disadvantages" table (breadth of integrations,
speed of prototyping, docs churn / deprecations you hit, debugging opacity, dependency weight — quote
the number of packages `uv` installed); when to use LangChain vs writing it yourself; Troubleshooting
(deprecation warnings; `langchain-classic` split; Ollama JSON mode in `with_structured_output`);
Exercises.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/rag_tutorial/fw_langchain.py`, `project/pyproject.toml`,
`project/uv.lock`, `project/justfile`, `project/data/cache/**` (incl. the LangChain sqlite/file caches),
`project/runs/08_*/**`, `project/runs/scoreboard.md`, `project/tests/test_08_langchain.py`,
`08_langchain_langgraph.md`. Verify token `"What you will learn"`.

## Scope & constraints
Do not use LangSmith or any hosted service. Do not rewrite earlier modules to use LangChain.
