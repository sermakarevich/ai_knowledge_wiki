# Task: chapter 09 — LlamaIndex: the RAG-first framework (node parsers, auto-merging, fusion, sub-questions, RAPTOR, evaluators)

Read `specs/COMMON.md`, `index.md`, chapters 00–08 first (cwd `/Users/sergii/.ai/knowledge/research_topics/rag_and_retrieval/tutorials/rag`).
Research: `specs/research/frameworks.md` (LlamaIndex section; installed version wins).

## Problem
LlamaIndex was built for RAG specifically and has the deepest menu of retrieval strategies. The
reader should see the same pipeline in its idioms and measure its advanced pieces on our golden set.

## Fix

### `project/src/rag_tutorial/fw_llamaindex.py` (Typer CLI: `index`, `ask`, `eval`) — dependency group `llamaindex`
Packages from the research note (`llama-index-core`, `llama-index-llms-ollama`,
`llama-index-embeddings-ollama`, `llama-index-vector-stores-chroma` or `-qdrant`,
`llama-index-retrievers-bm25`, `llama-index-postprocessor-sbert-rerank` or the flag-embedding
reranker, `llama-index-packs-raptor` if installable). `Settings.llm = Ollama(base_url=…, model=…,
temperature=0, request_timeout=300, additional_kwargs={"seed": 42, "num_ctx": 16384})`,
`Settings.embed_model = OllamaEmbedding(...)`. Use LlamaIndex's `IngestionCache`/`IngestionPipeline`
with a local cache and `llama_index.core.llms` callback token counting; count calls with a callback.
1. **Plain**: `SimpleDirectoryReader(data/corpus/md)` → `MarkdownNodeParser` + `SentenceSplitter`
   → `VectorStoreIndex` → `as_query_engine(similarity_top_k=5)` → `09_li_naive`. Map nodes to our
   chunk ids (`start_char_idx`/`end_char_idx` are available on nodes — use them).
2. **SentenceWindowNodeParser** + `MetadataReplacementPostProcessor` → `09_li_sentence_window`.
3. **HierarchicalNodeParser** + `AutoMergingRetriever` → `09_li_auto_merging`.
4. **QueryFusionRetriever** (BM25 + vector, `mode="reciprocal_rerank"`, `num_queries=3`) →
   `09_li_fusion`.
5. **SentenceTransformerRerank** (`bge-reranker-v2-m3`) on top of fusion → `09_li_fusion_rerank`.
6. **SubQuestionQueryEngine** (one tool per paper or per 3 papers) → `09_li_subquestion`; and a
   **RouterQueryEngine** choosing between a vector engine and a `SummaryIndex` (tree_summarize) engine
   for `global` questions → `09_li_router`.
7. **Response modes** `compact` vs `refine` vs `tree_summarize` on the same retriever → 3 rows
   (`09_li_mode_*`), with call counts — this is where "modes" cost shows.
8. **RAPTOR pack**: the research note says `llama-index-packs-raptor` is officially deprecated — do
   NOT spend time on it; mention this in one sentence and point to chapter 11, which builds RAPTOR by hand.
9. **Built-in evaluators**: `FaithfulnessEvaluator`, `RelevancyEvaluator`, `CorrectnessEvaluator`
   with our Ollama LLM on the `09_li_fusion_rerank` predictions; compare their verdicts with our
   judge's (agreement %) → table.

### Tests `project/tests/test_09_llamaindex.py`
`MockLLM` + `MockEmbedding` from `llama_index.core`: build a tiny index and query; the node→chunk-id
mapping; the sentence-window postprocessor replaces text with the window. No network.

### `09_llamaindex.md` (chapter)
LlamaIndex's mental model (Documents → Nodes → Index → Retriever → Node postprocessors → Response
synthesizer → Query engine; `Settings`), side-by-side with chapter 03; each technique in a paragraph
with the real output for one golden question; the response-mode cost table; the evaluator-agreement
table; "What changed on the scoreboard" (all rows next to 07/08 and the anchors); "Advantages and
disadvantages" (RAG depth, sensible defaults, docs quality, magic/implicit behaviour, dependency
weight, speed); LangChain vs LlamaIndex in one honest paragraph; Troubleshooting (Ollama
`request_timeout`; `num_ctx`; `chromadb` version pinning conflicts with LangChain group — use separate
uv groups/extras or one resolved lock and say which); Exercises.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/rag_tutorial/fw_llamaindex.py`, `project/pyproject.toml`,
`project/uv.lock`, `project/justfile`, `project/data/cache/**`, `project/runs/09_*/**`,
`project/runs/scoreboard.md`, `project/tests/test_09_llamaindex.py`, `09_llamaindex.md`.
Verify token `"What you will learn"`.

## Scope & constraints
No LlamaCloud/LlamaParse (hosted). Do not touch earlier modules except `pyproject.toml`/lock.
