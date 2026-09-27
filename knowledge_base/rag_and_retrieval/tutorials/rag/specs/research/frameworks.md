# RAG framework research — LangChain/LangGraph, LlamaIndex, Haystack 2.x, DSPy

Research date: 2026-08-30. Target stack: macOS, Python 3.12, `uv`, Ollama (chat `qwen3.8:27b`, embeddings
`nomic-embed-text`) at `http://127.0.0.1:11435`, Chroma (embedded) and Qdrant (Docker) as vector stores.

Every fact below carries the URL of the page it was fetched from. Anything not directly confirmed on a
fetched page is explicitly marked **UNVERIFIED**. Prefer these over blog posts when writing the tutorial.

---

## 1. LangChain + LangGraph

### 1.1 Versions, Python support, license

| Package | Version | Release date | Python | License | Source |
|---|---|---|---|---|---|
| `langchain` | 1.3.18 | 2026-08-27 | >=3.10,<4.0 | MIT | https://pypi.org/project/langchain/ |
| `langchain-core` | 1.6.1 | 2026-08-27 | >=3.10,<4.0 | MIT | https://pypi.org/project/langchain-core/ |
| `langgraph` | 1.2.11 | 2026-08-11 | 3.10–3.13 | MIT | https://pypi.org/project/langgraph/ |
| `langchain-ollama` | 1.1.0 | 2026-04-07 | >=3.10,<4.0 | MIT | https://pypi.org/project/langchain-ollama/ |
| `langchain-chroma` | 1.1.0 | 2025-12-12 | >=3.10,<4.0 | MIT | https://pypi.org/project/langchain-chroma/ |
| `langchain-qdrant` | 1.1.0 | 2025-10-22 | >=3.10,<4.0 | MIT | https://pypi.org/project/langchain-qdrant/ |
| `langchain-classic` | 1.0.8 | 2026-06-10 | >=3.10,<=3.13 | MIT | https://pypi.org/project/langchain-classic/ |

Python 3.12 is supported by every package above. LangGraph describes itself as "a low-level orchestration
framework for building, managing, and deploying long-running, stateful agents" with durable execution,
streaming, human-in-the-loop, and persistence/memory (used in production by Klarna, Replit, Elastic per
https://pypi.org/project/langgraph/).

### 1.2 Exact packages/imports for this tutorial's stack

- **Ollama chat + embeddings**: `pip install langchain-ollama` → `from langchain_ollama import ChatOllama, OllamaEmbeddings`. Both take a `base_url` constructor kwarg — confirmed on the `ChatOllama.base_url` reference page: "specifies the base URL the model is hosted under… supports userinfo auth". So `ChatOllama(model="qwen3.8:27b", base_url="http://127.0.0.1:11435")` and `OllamaEmbeddings(model="nomic-embed-text", base_url="http://127.0.0.1:11435")`. Sources: https://pypi.org/project/langchain-ollama/, https://reference.langchain.com/python/langchain-ollama/chat_models/ChatOllama/base_url
- **Chroma**: `pip install langchain-chroma` → class `Chroma` in `langchain_chroma`. Source: https://pypi.org/project/langchain-chroma/
- **Qdrant**: `pip install langchain-qdrant` (optional `fastembed` extra) → class `QdrantVectorStore` in `langchain_qdrant`. Docker/remote via `url=...`; hybrid dense+sparse via `sparse_embedding=...` + `retrieval_mode=RetrievalMode.HYBRID`. Sources: https://pypi.org/project/langchain-qdrant/, https://docs.langchain.com/oss/python/integrations/vectorstores/qdrant, https://reference.langchain.com/python/langchain-qdrant/qdrant/QdrantVectorStore
- **BM25**: `pip install rank_bm25`, then `from langchain_community.retrievers.bm25 import BM25Retriever` — `.from_documents()`/`.from_texts()`, params `bm25_params`, `preprocess_func`. Source: https://reference.langchain.com/python/langchain-community/retrievers/bm25/BM25Retriever
- **PDF loader**: `pip install pypdf`, `from langchain_community.document_loaders import PyPDFLoader` (one `Document` per page, metadata `source`/`page`). The current official RAG tutorial actually loads PDFs by hand with raw `pypdf.PdfReader` wrapped in `langchain_core.documents.Document` rather than via the loader class — UNVERIFIED whether `PyPDFLoader` was demoted, but it still resolves under `langchain_community`. Source: https://reference.langchain.com/python/langchain-community/document_loaders/pdf/PyPDFLoader
- **Markdown loader**: `UnstructuredMarkdownLoader` (`langchain_community.document_loaders`, needs `unstructured` — exact current extra name UNVERIFIED); header-aware alternative `MarkdownHeaderTextSplitter` from `langchain_text_splitters`.
- **Text splitter**: `from langchain_text_splitters import RecursiveCharacterTextSplitter` — default separators `["\n\n","\n"," ",""]`, recursive paragraph→sentence→word split. Source: https://reference.langchain.com/python/langchain-text-splitters/character/RecursiveCharacterTextSplitter

### 1.3 Minimal current "index PDFs → retrieve → answer" snippet

Adapted from the official knowledge-base tutorial (https://docs.langchain.com/oss/python/langchain/knowledge-base), substituting OpenAI for the local Ollama/Chroma stack:

```python
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
import pypdf

def load_pdf_pages(file_path: str) -> list[Document]:
    reader = pypdf.PdfReader(file_path)
    return [Document(page_content=p.extract_text() or "",
                      metadata={"source": file_path, "page": i})
            for i, p in enumerate(reader.pages)]

docs = load_pdf_pages("mydoc.pdf")
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
all_splits = splitter.split_documents(docs)

embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url="http://127.0.0.1:11435")
vector_store = Chroma(embedding_function=embeddings, collection_name="rag")
vector_store.add_documents(all_splits)

retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
llm = ChatOllama(model="qwen3.8:27b", base_url="http://127.0.0.1:11435", temperature=0)

docs_found = retriever.invoke("your question")
context = "\n\n".join(d.page_content for d in docs_found)
answer = llm.invoke(f"Answer using only this context:\n{context}\n\nQuestion: your question")
```
`VectorStoreRetriever.search_type` accepts `"similarity"` (default), `"mmr"`, `"similarity_score_threshold"`.

### 1.4 Breaking changes in v1 (confirmed)

- `langchain` v1 shrank its top-level namespace to agent-building blocks only (agents, messages, tools, chat-model/embedding init helpers). Legacy chains, `langchain-community` re-exports, the indexing API, `hub`, and evaluation abstractions moved into a **new `langchain-classic` package**. Sources: https://docs.langchain.com/oss/python/migrate/langchain-v1, https://pypi.org/project/langchain-classic/
- **`RetrievalQA` and `ConversationalRetrievalChain` were removed** from `langchain` (not merely deprecated). Migrate to `create_retrieval_chain`/`create_history_aware_retriever`, both now in `langchain_classic`. Sources: https://docs.langchain.com/oss/python/migrate/langchain-v1, https://reference.langchain.com/python/langchain-classic/chains/retrieval/create_retrieval_chain
- `create_react_agent` (previously in `langgraph.prebuilt`) → replaced by **`create_agent`**, now in `langchain.agents`, built directly on LangGraph (durable execution/streaming/checkpointing "for free"). `prompt=` renamed to `system_prompt=` (str only); hooks became "middleware" (`before_model`/`after_model`/`wrap_tool_call`); new `@dynamic_prompt` decorator. Source: https://docs.langchain.com/oss/python/migrate/langchain-v1
- Current official RAG guidance beyond bare retrieval is **agentic**: give `create_agent(...)` a retrieval `@tool` rather than a fixed chain — "The only thing an agent needs to enable RAG behavior is access to one or more tools." Source: https://docs.langchain.com/oss/python/langchain/retrieval
- Practical options for a tutorial: (a) hand-roll the LCEL retrieve→format→prompt→llm pipeline (no deprecated classes, shown above); (b) `pip install langchain-classic` for the tutorial-style `create_retrieval_chain` + `create_stuff_documents_chain`; (c) wrap retrieval as a tool inside `create_agent` for the "current idiomatic v1" agentic-RAG path.

### 1.5 Advanced RAG features (exact names, doc URLs)

Most of these wrappers now live in **`langchain_classic`**, not top-level `langchain`.

- **Hybrid search / RRF**: `EnsembleRetriever` (`langchain_classic.retrievers.ensemble`) — merges retrievers via reciprocal-rank-fusion (`weighted_reciprocal_rank`, constant `c=60`, per-retriever `weights`). Source: https://reference.langchain.com/python/langchain-classic/retrievers/ensemble/EnsembleRetriever
- **Multi-query**: `MultiQueryRetriever` (`langchain_classic.retrievers.multi_query`) — LLM rewrites the query into variants, retrieves each, dedupes via `unique_union()`; built with `.from_llm()`. Source: https://reference.langchain.com/python/langchain-classic/retrievers/multi_query/MultiQueryRetriever
- **HyDE**: no dedicated built-in class confirmed in current docs (older `HypotheticalDocumentEmbedder` in `langchain.chains.hyde` not found in current `langchain_classic` listing). **UNVERIFIED as currently shipped** — plan a small custom LLM-rewrite step instead.
- **Parent-document retriever**: `ParentDocumentRetriever` (`langchain_classic.retrievers.parent_document_retriever`) — stores small chunks, returns larger parent docs on retrieval. Source: https://reference.langchain.com/python/langchain-classic/retrievers/parent_document_retriever/ParentDocumentRetriever
- **Contextual compression / rerank**: `ContextualCompressionRetriever` (`langchain_classic.retrievers.contextual_compression`). Free/local cross-encoder reranker: `FlashrankRerank` document compressor (`langchain_community.document_compressors.flashrank_rerank`, params `client`, `model` e.g. `"ms-marco-MultiBERT-L-12"`, `top_n`, `score_threshold`) — good fit since it needs no API key. Cohere's `CohereRerank` also exists but is a paid API, not relevant here. Sources: https://reference.langchain.com/python/langchain-classic/retrievers/contextual_compression/ContextualCompressionRetriever, https://reference.langchain.com/v0.3/python/community/document_compressors/langchain_community.document_compressors.flashrank_rerank.FlashrankRerank.html (v0.3-pinned URL — confirm current path before shipping)
- **Self-query**: `SelfQueryRetriever` (`langchain_classic.retrievers.self_query.base`) — parses natural-language filters into structured metadata queries. Source: https://reference.langchain.com/python/langchain-classic/retrievers/self_query/base/SelfQueryRetriever
- **Routing**: `RunnableBranch` (`langchain_core.runnables`) is the long-standing LCEL conditional-routing primitive (exact current doc URL not fetched this session). No confirmed single "semantic router" built-in class — typically hand-rolled or done via LangGraph conditional edges.
- **Sub-question decomposition**: no dedicated shipped class found — normally a small LangGraph subgraph or an LLM query-decomposition prompt feeding `MultiQueryRetriever`-style parallel retrieval. **UNVERIFIED** that a first-class class exists.
- **Agentic RAG templates (Self-RAG / CRAG / Adaptive RAG)**: official example notebooks in `langchain-ai/langgraph`:
  - `examples/rag/langgraph_self_rag.ipynb` — self-grades generations for hallucination/answer-quality (Self-RAG paper)
  - `examples/rag/langgraph_crag.ipynb` / `langgraph_crag_local.ipynb` — Corrective RAG: lightweight retrieval evaluator grades docs, falls back to web search when ambiguous, does knowledge-strip refinement
  - `examples/rag/langgraph_adaptive_rag.ipynb` — routes the query across strategies by complexity
  Built with `StateGraph`/`add_node`/`add_edge`/`add_conditional_edges`. GitHub's notebook preview failed to render during this research — **verify these still run against LangGraph 1.2.x** before basing tutorial code on them (some archived notebooks reportedly redirect users to consolidated docs). Overview: https://blog.langchain.com/agentic-rag-with-langgraph/
- **Evaluation, free/local**: `langchain.evaluation` is deprecated (slated for removal in v1); classes (`StringDistanceEvalChain`, criteria/embedding-distance evaluators, `load_evaluator`) moved to `langchain_classic.evaluation`. Sources: https://reference.langchain.com/python/langchain-classic/evaluation/string_distance, https://reference.langchain.com/python/langchain-classic/evaluation/criteria, https://reference.langchain.com/python/langchain-classic/evaluation/embedding_distance. For a genuinely free/local RAG-quality eval, **RAGAS** (`pip install ragas`, https://docs.ragas.io) is the standard: faithfulness, answer/response relevancy, context precision/recall, runs fully against local Ollama models with no LangSmith dependency (https://docs.ragas.io/en/stable/references/integrations/).
- **Caching**: `set_llm_cache()` (`langchain_core.globals`); `InMemoryCache` now lives in `langchain_core.caches` (`lookup()`/`update()`/`clear()`, sync+async, optional `maxsize`). `SQLiteCache`/`RedisCache` remain in `langchain_community.cache` — good for a local persistent LLM-response cache. Sources: https://reference.langchain.com/python/langchain-core/caches/InMemoryCache, https://reference.langchain.com/python/langchain-community/cache
- **Streaming**: `.stream()`/`.astream()` are standard `Runnable` methods implemented by every LCEL component including `ChatOllama` — baseline LCEL behavior.
- **Structured output**: `with_structured_output(schema)` on `BaseChatModel`, including `ChatOllama` (dedicated reference page confirmed). Accepts Pydantic model / TypedDict / JSON-schema dict; `include_raw=True` returns raw+parsed. Source: https://reference.langchain.com/python/langchain-ollama/chat_models/ChatOllama/with_structured_output
- **Citations**: no dedicated citation class found; standard practice is returning `Document.metadata` (`source`, `page`) alongside the answer, or forcing citation fields via structured output. **UNVERIFIED** any first-class citation API in v1.

### 1.6 LangGraph's role

LangGraph is the low-level graph/state-machine layer: explicit `StateGraph` of nodes/edges/conditional-edges giving durable execution, checkpointing, streaming, human-in-the-loop beyond what a flat LCEL chain provides (https://pypi.org/project/langgraph/). In v1, `create_agent` is built directly on top of LangGraph, so "agentic RAG" in current LangChain docs is really LangGraph under a simpler API (https://docs.langchain.com/oss/python/migrate/langchain-v1). LangGraph is what backs Self-RAG/CRAG/Adaptive-RAG patterns that a linear retrieve→generate chain can't express (https://blog.langchain.com/agentic-rag-with-langgraph/).

**Tutorial-writer flags**: `langchain-classic` is a load-bearing dependency for demoing `EnsembleRetriever`, `MultiQueryRetriever`, `ParentDocumentRetriever`, `SelfQueryRetriever`, `ContextualCompressionRetriever`, `create_retrieval_chain`, or the deprecated evaluators — none ship in bare `langchain` 1.3.x. HyDE, sub-question decomposition, semantic routing, citations: plan as small custom code, not "just import X."

---

## 2. LlamaIndex

**Docs-site note**: `docs.llamaindex.ai` now 301-redirects to **`developers.llamaindex.ai`** (e.g. `.../python/examples/llm/ollama/`). Use the new domain in the tutorial; old links still resolve.

### 2.1 Versions, Python support, license

- `llama-index` (meta-package) and `llama-index-core`: both **v0.14.24**, released **2026-08-19**, `Requires-Python >=3.10,<4.0`, **MIT**. Sources: https://pypi.org/project/llama-index/, https://pypi.org/project/llama-index-core/
- Since 0.10, `pip install llama-index`/`uv add llama-index` pulls core + a default integration bundle; Ollama/Chroma/Qdrant are separate versioned packages (below) — a known breaking change from pre-0.10 all-in-one releases.

### 2.2 Exact packages/imports

| Purpose | Package | Version | Release date | Import |
|---|---|---|---|---|
| Ollama LLM | `llama-index-llms-ollama` | 0.10.1 | 2026-03-20 | `from llama_index.llms.ollama import Ollama` |
| Ollama embeddings | `llama-index-embeddings-ollama` | 0.9.0 | 2026-03-12 | `from llama_index.embeddings.ollama import OllamaEmbedding` |
| Chroma store | `llama-index-vector-stores-chroma` | 0.5.5 | 2025-12-30 | `from llama_index.vector_stores.chroma import ChromaVectorStore` (class name by convention — **confirm before use**, not shown on the fetched PyPI page) |
| Qdrant store | `llama-index-vector-stores-qdrant` | 0.10.3 | 2026-08-13 | `from llama_index.vector_stores.qdrant import QdrantVectorStore` (same caveat) |
| BM25 retriever | `llama-index-retrievers-bm25` | 0.7.1 | 2026-03-13 | `from llama_index.retrievers.bm25 import BM25Retriever` (import confirmed via the RRF-fusion doc, §2.4) |
| File loading | `llama-index-readers-file` (auto-pulled by `SimpleDirectoryReader`) | 0.6.0 | 2026-03-12 (**UNVERIFIED-low-confidence**, PyPI fetch failed, taken from search snippet) | `from llama_index.core import SimpleDirectoryReader` (auto-detects `.pdf`/`.md`); explicit: `from llama_index.readers.file import PDFReader, MarkdownReader` |
| Splitters/node parsers | ships in `llama-index-core`, no extra package | — | — | `from llama_index.core.node_parser import SentenceSplitter, MarkdownNodeParser, SentenceWindowNodeParser, HierarchicalNodeParser, TokenTextSplitter` |

Sources: https://pypi.org/project/llama-index-llms-ollama/, https://pypi.org/project/llama-index-embeddings-ollama/, https://pypi.org/project/llama-index-vector-stores-chroma/, https://pypi.org/project/llama-index-vector-stores-qdrant/, https://pypi.org/project/llama-index-retrievers-bm25/, https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/, https://developers.llamaindex.ai/python/framework/module_guides/loading/simpledirectoryreader/

Qdrant integration lists `Python >=3.10,<3.14` and an optional `fastembed` extra (https://pypi.org/project/llama-index-vector-stores-qdrant/) — fine for Python 3.12.

### 2.3 Minimal current snippet (global `Settings`, replaces old `ServiceContext`)

```python
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

Settings.llm = Ollama(
    model="qwen3.8:27b",
    base_url="http://127.0.0.1:11435",
    request_timeout=120.0,     # docs' example default is 30s
)
Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text",
    base_url="http://127.0.0.1:11435",
)

documents = SimpleDirectoryReader("./data").load_data()   # auto-detects .pdf/.md
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("Your question here")
print(response)
```
`Settings` singleton confirmed at https://developers.llamaindex.ai/python/framework/module_guides/supporting_modules/settings/. `OllamaEmbedding(model_name=..., base_url=...)` kwarg shape confirmed at https://developers.llamaindex.ai/python/examples/embeddings/ollama_embedding/. The fetched `Ollama(...)` LLM example (https://developers.llamaindex.ai/python/examples/llm/ollama/) showed `model`/`request_timeout`/`context_window` but not `base_url` explicitly — **confirm the `base_url` kwarg name on the `Ollama` LLM class itself** before shipping. Load→index→query pattern confirmed verbatim at https://developers.llamaindex.ai/python/framework/understanding/rag/.

**Breaking-change note**: LlamaIndex 0.11 introduced **Workflows**, deprecating the older Query Pipelines; 0.14.x continues recommending Workflows for anything beyond a simple query engine (**UNVERIFIED exact version**, sourced from a secondary synthesis, not an official page fetch).

### 2.4 Advanced RAG features

- **Hybrid search / RRF**: `QueryFusionRetriever` (`llama_index.core.retrievers`, `mode="reciprocal_rerank"`) combining a vector retriever + `BM25Retriever`; `num_queries` also drives multi-query/rewriting (`num_queries=1` disables it):
  ```python
  from llama_index.core.retrievers import QueryFusionRetriever
  retriever = QueryFusionRetriever([vector_retriever, bm25_retriever],
                                    similarity_top_k=2, num_queries=4,
                                    mode="reciprocal_rerank", use_async=True)
  ```
  Source: https://developers.llamaindex.ai/python/examples/retrievers/reciprocal_rerank_fusion/
- **HyDE**: `HyDEQueryTransform` + `TransformQueryEngine` — `hyde = HyDEQueryTransform(include_original=True); hyde_query_engine = TransformQueryEngine(query_engine, hyde)`. Source: https://developers.llamaindex.ai/python/examples/query_transformations/hydequerytransformdemo/
- **Parent-document / small-to-big**: `HierarchicalNodeParser` (coarse-to-fine chunk hierarchy) + `AutoMergingRetriever` (merges children back to parent when enough are retrieved). Exact import paths **UNVERIFIED** (conventionally `llama_index.core.node_parser` / `llama_index.core.retrievers`). Source: https://developers.llamaindex.ai/python/examples/retrievers/auto_merging_retriever/
- **Sentence-window**: `SentenceWindowNodeParser` (default window ±5 sentences, stored in node metadata — **secondary-source claim**) + `MetadataReplacementPostProcessor(target_metadata_key="window")` to swap the sentence back for its window at query time. Source: https://developers.llamaindex.ai/python/framework/module_guides/querying/node_postprocessors/node_postprocessors/
- **RAPTOR**: `llama-index-packs-raptor` (`tree_traversal`/`collapsed` modes) — **officially marked deprecated/unmaintained**; flag as historical only. Sources: https://pypi.org/project/llama-index-packs-raptor/, https://developers.llamaindex.ai/python/framework-api-reference/packs/raptor/
- **Rerankers**: `SentenceTransformerRerank` (`llama_index.core.postprocessor`, needs `sentence-transformers`, default `cross-encoder/ms-marco-TinyBERT-L-2-v2` — local, no API key); `LLMRerank` (`llama_index.core.postprocessor`, uses `Settings.llm`, fully local with Ollama); `CohereRerank`/`JinaRerank` (separate paid-API packages). **No official FlashRank postprocessor** — the fetched node-postprocessors doc page explicitly lists rankgpt/rankllm/tei/nvidia/siliconflow/sbert as the "other" integrations, no FlashRank entry. Source: https://developers.llamaindex.ai/python/framework/module_guides/querying/node_postprocessors/node_postprocessors/
- **Metadata filtering / auto-retrieval**: `VectorIndexAutoRetriever` exists per official retriever docs; exact import/usage **UNVERIFIED** this session (page not directly fetched).
- **Routing / sub-question decomposition**: `RouterQueryEngine`, `SubQuestionQueryEngine` (breaks a complex query into per-source sub-questions, synthesizes a final answer). Conventional import `llama_index.core.query_engine` — **import paths UNVERIFIED**, confirm before use. Sources: https://docs.llamaindex.ai/en/stable/module_guides/querying/router/ (redirects), https://developers.llamaindex.ai/python/examples/cookbooks/oreilly_course_cookbooks/module-6/router_and_subquestion_queryengine/
- **Response synthesis modes** (`response_mode` on `as_query_engine`): `refine` (iterative, one call/node), `compact` (**default**, concatenates chunks to fill context first, fewer calls), `tree_summarize` (bottom-up recursive merge, best for whole-corpus summarization). **Search-synthesized, not a direct page fetch** — verify wording. Sources: https://developers.llamaindex.ai/python/framework/module_guides/querying/response_synthesizers/, https://docs.llamaindex.ai/en/stable/module_guides/deploying/query_engine/response_modes/
- **Agentic RAG**: LlamaIndex **Workflows** (event-driven step composition, recommended since 0.11) plus `FunctionAgent` (tool-calling LLMs) and `ReActAgent` (works with any LLM incl. local Ollama models without native tool-calling — relevant here); `CodeActAgent` also exists. **Search-synthesized, UNVERIFIED against a direct official-page fetch** — confirm at `developers.llamaindex.ai/python/framework/module_guides/deploying/agents/` before writing code.
- **Evaluation (free/local, uses `Settings.llm` as judge)**: `FaithfulnessEvaluator` (hallucination check vs. context), `RelevancyEvaluator` (context+answer relevance to query), `CorrectnessEvaluator` (vs. a reference answer) — all runnable fully locally against Ollama. Sources: https://docs.llamaindex.ai/en/stable/examples/evaluation/faithfulness_eval/, https://docs.llamaindex.ai/en/stable/examples/evaluation/relevancy_eval/ (both redirect to developers.llamaindex.ai)
- **Streaming**: `index.as_query_engine(streaming=True)`, then `streaming_response.print_response_stream()` or iterate `streaming_response.response_gen`. Ollama LLM class exposes `stream_complete()`/`stream_chat()` per its PyPI page, so streaming should work with this stack. Sources: https://developers.llamaindex.ai/python/framework/module_guides/deploying/query_engine/streaming/, https://pypi.org/project/llama-index-llms-ollama/
- **Structured output / citations**: `CitationQueryEngine` (`llama_index.core.query_engine`), built via `CitationQueryEngine.from_args(index, ...)`, adds inline citation numbering. **UNVERIFIED** — search-synthesized, confirm `from_args` signature directly.

**Gaps to close before writing final tutorial code**: `ChromaVectorStore`/`QdrantVectorStore` exact constructor kwargs; `VectorIndexAutoRetriever`, `RouterQueryEngine`/`SubQuestionQueryEngine` import paths; `CitationQueryEngine.from_args` signature; Workflows/`FunctionAgent`/`ReActAgent` doc page; `Ollama(...)` LLM's `base_url` kwarg name.

---

## 3. Haystack (deepset) 2.x

### 3.1 Versions, Python support, license

- `haystack-ai`: **3.1.0**, released **2026-08-24**, Python **3.10–3.14**, **Apache-2.0**. Source: https://pypi.org/project/haystack-ai/

### 3.2 Exact package/component names

| Need | Package | Class(es) | Source |
|---|---|---|---|
| Ollama chat generator | **`ollama-haystack`** (separate integration, not bundled in core) | `OllamaChatGenerator`, `OllamaGenerator` (`haystack_integrations.components.generators.ollama`) | https://docs.haystack.deepset.ai/docs/ollamachatgenerator, https://haystack.deepset.ai/integrations/ollama |
| Ollama embedders | `ollama-haystack` | `OllamaTextEmbedder`, `OllamaDocumentEmbedder` (default model `nomic-embed-text`, default url `http://localhost:11434`) (`haystack_integrations.components.embedders.ollama`) | https://docs.haystack.deepset.ai/docs/ollamatextembedder |
| `ollama-haystack` version | **6.3.0** (**UNVERIFIED** exact date — PyPI fetch failed, corroborated only by search snippet/Socket listing) | — | https://pypi.org/project/ollama-haystack/ |
| Chroma store | `chroma-haystack` **4.4.0**, released **2026-07-24** | `ChromaDocumentStore` (`haystack_integrations.document_stores.chroma`) | https://pypi.org/project/chroma-haystack/, https://haystack.deepset.ai/integrations/chroma-documentstore |
| Qdrant store | `qdrant-haystack` **10.5.0**, released **2026-08-03**, Python `>=3.10`, Apache-2.0 | `QdrantDocumentStore` (`haystack_integrations.document_stores.qdrant`) | https://pypi.org/project/qdrant-haystack/, https://haystack.deepset.ai/integrations/qdrant-document-store |
| BM25 | built into `haystack-ai` core, works only with `InMemoryDocumentStore` | `InMemoryBM25Retriever` (`haystack.components.retrievers.in_memory`) | https://docs.haystack.deepset.ai/docs/inmemorybm25retriever |
| PDF converter | core (needs `pypdf`) | `PyPDFToDocument` (`haystack.components.converters`) | https://docs.haystack.deepset.ai/docs/pypdftodocument |
| Markdown converter | core (needs `markdown-it-py`, `mdit_plain`) | `MarkdownToDocument` (`extract_frontmatter=True` supported) | https://docs.haystack.deepset.ai/docs/markdowntodocument |
| Splitter | core | `DocumentSplitter` (`haystack.components.preprocessors`), `split_by` in word/sentence/passage/page/line/period/function, plus `split_length`/`split_overlap`/`split_threshold` | https://docs.haystack.deepset.ai/docs/documentsplitter |

### 3.3 Minimal current pipeline

```python
from haystack import Pipeline, Document
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.builders import ChatPromptBuilder
from haystack.dataclasses import ChatMessage
from haystack_integrations.components.embedders.ollama import OllamaTextEmbedder
from haystack_integrations.components.generators.ollama import OllamaChatGenerator

OLLAMA_URL = "http://127.0.0.1:11435"
document_store = InMemoryDocumentStore()
# ... index Documents first with OllamaDocumentEmbedder(model="nomic-embed-text", url=OLLAMA_URL) ...

template = [ChatMessage.from_user(
    "Context:\n{% for doc in documents %}{{ doc.content }}\n{% endfor %}\nQuestion: {{question}}\nAnswer:"
)]

rag = Pipeline()
rag.add_component("text_embedder", OllamaTextEmbedder(model="nomic-embed-text", url=OLLAMA_URL))
rag.add_component("retriever", InMemoryEmbeddingRetriever(document_store))
rag.add_component("prompt_builder", ChatPromptBuilder(template=template, required_variables="*"))
rag.add_component("llm", OllamaChatGenerator(model="qwen3.8:27b", url=OLLAMA_URL))

rag.connect("text_embedder.embedding", "retriever.query_embedding")
rag.connect("retriever", "prompt_builder")
rag.connect("prompt_builder.prompt", "llm.messages")

result = rag.run({"text_embedder": {"text": q}, "prompt_builder": {"question": q}})
```
Sources: https://haystack.deepset.ai/tutorials/27_first_rag_pipeline, https://docs.haystack.deepset.ai/docs/ollamachatgenerator, https://docs.haystack.deepset.ai/docs/ollamatextembedder, https://docs.haystack.deepset.ai/docs/pipelines (canonical steps: `Pipeline()` → `add_component` → `connect` → `run`).

**Breaking-change note**: the widely-known 1.x→2.x rewrite (old Farm/Reader-based `ExtractiveQAPipeline` API replaced by the component/pipeline model above) was **not** re-confirmed on a page fetched this session — treat as commonly known but UNVERIFIED against an official page in this pass.

### 3.4 Advanced RAG features

- **Hybrid search / RRF**: `DocumentJoiner` (`haystack.components.joiners.document_joiner`), `join_mode="reciprocal_rank_fusion"` (also `concatenate`, `merge`, `distribution_based_rank_fusion`) — wire an `InMemoryBM25Retriever` and an embedding retriever into it. Source: https://docs.haystack.deepset.ai/docs/documentjoiner
- **HyDE**: official cookbook https://haystack.deepset.ai/cookbook/using_hyde_for_improved_retrieval, blog https://haystack.deepset.ai/blog/optimizing-retrieval-with-hyde, doc https://docs.haystack.deepset.ai/docs/hypothetical-document-embeddings-hyde. Pattern: `ChatPromptBuilder` → generator produces N hypothetical docs → `OutputAdapter` → `SentenceTransformersDocumentEmbedder` → averaging component → `InMemoryEmbeddingRetriever`.
- **Rerankers**: `SentenceTransformersSimilarityRanker`, `SentenceTransformersDiversityRanker`, `CohereRanker`, plus `LLMRanker`, `MetaFieldRanker`, `LostInTheMiddleRanker`, `NvidiaRanker`, `JinaRanker`, `FastembedRanker` (note: renamed from the older `TransformersSimilarityRanker`). Source: https://docs.haystack.deepset.ai/docs/rankers
- **Metadata filtering**: native `filters` dict argument on retrievers/document stores (`InMemoryEmbeddingRetriever`, `ChromaDocumentStore`, `QdrantDocumentStore`) — not independently re-verified beyond the package docs already cited.
- **Routing**: `ConditionalRouter` (`haystack.components.routers`) — Jinja2 conditions, multiple named outputs. Source: https://docs.haystack.deepset.ai/docs/conditionalrouter
- **Agentic RAG**: `Agent` component (`haystack.components.agents`) — takes `chat_generator`, `tools` (`Tool`, `ComponentTool`, `PipelineTool`, `AgentTool`, `MCPTool`, `Toolset`, `MCPToolset`, `SearchableToolset`), `system_prompt`; tools via `@tool` decorator (`haystack.tools`). Source: https://docs.haystack.deepset.ai/docs/agent
- **Evaluation**: `FaithfulnessEvaluator`, `ContextRelevanceEvaluator` (`haystack.components.evaluators`) — default to `gpt-5-mini`/`OPENAI_API_KEY` unless you pass your own `chat_generator`; **plausible but UNVERIFIED** that pointing `chat_generator=OllamaChatGenerator(...)` at them makes them fully local. A `RagasEvaluator` is also listed for RAGAS integration. Source: https://docs.haystack.deepset.ai/docs/faithfulnessevaluator
- **Streaming**: `streaming_callback` param confirmed on `OllamaChatGenerator`. Source: https://docs.haystack.deepset.ai/docs/ollamachatgenerator
- **Caching, multi-query, sub-question decomposition, structured output**: not confirmed via a fetched official page this session — **UNVERIFIED**, would need direct doc/cookbook lookups.

---

## 4. DSPy

### 4.1 Version, Python support, license

- `dspy`: **3.3.1**, released **2026-08-21**, `Python <3.15,>=3.10` (3.12 fully supported), **MIT**. Repo: https://github.com/stanfordnlp/dspy, docs: https://dspy.ai/. Source: https://pypi.org/project/dspy/
- Tutorial-relevant installs: `pip install -U dspy`, `pip install datasets`, `pip install dspy[numpy]` (needed for `dspy.Embedder`/`dspy.retrievers.Embeddings`); optional `pip install -U faiss-cpu` (or pass `brute_force_threshold=30_000` to skip FAISS). Source: https://github.com/stanfordnlp/dspy/blob/main/docs/docs/tutorials/rag/index.ipynb

### 4.2 Configuring Ollama

Confirmed exact current syntax (https://github.com/stanfordnlp/dspy/blob/main/docs/docs/learn/programming/language_models.md, served at https://dspy.ai/getting-started/installation/):

```python
import dspy
lm = dspy.LM("ollama_chat/qwen3.8:27b", api_base="http://127.0.0.1:11435", api_key="")
dspy.configure(lm=lm)
```

DSPy uses **LiteLLM** under the hood; `ollama_chat/` is LiteLLM's convention for the Ollama chat endpoint (vs. bare `ollama/` for completion-only). `dspy.configure(lm=lm)` sets a global default; scope-override with `with dspy.context(lm=other_lm): ...`. Extra params on `dspy.LM(...)`: `temperature`, `max_tokens`, `stop`, `cache=False`, `rollout_id=`. Direct raw calls: `lm("prompt")` or `lm(messages=[...])`.

### 4.3 Retrieval story (confirmed from the official RAG tutorial notebook)

Source: https://github.com/stanfordnlp/dspy/blob/main/docs/docs/tutorials/rag/index.ipynb (served at https://dspy.ai/tutorials/rag/)

- The current official tutorial does **not use `dspy.Retrieve`**. It uses **`dspy.retrievers.Embeddings`** + `dspy.Embedder`:
  ```python
  embedder = dspy.Embedder("openai/text-embedding-3-small", dimensions=512)
  search = dspy.retrievers.Embeddings(embedder=embedder, corpus=corpus, k=topk_docs_to_retrieve)
  ```
- Explicit philosophy quote: **"As far as DSPy is concerned, you can plug in any Python code for calling tools or retrievers."** Retrieval is a plain Python callable, not a mandatory DSPy abstraction.
- Whether `dspy.Retrieve` is formally deprecated vs. simply superseded is **UNVERIFIED** (not stated on fetched pages); GitHub issue #250 ("Standardize Vector Search Retrievers") suggests the retriever API has been in flux (https://github.com/stanfordnlp/dspy/issues/250).
- The official tutorial uses local FAISS-backed brute-force search over a JSONL corpus — **no Chroma or Qdrant mention** in it.
- For **Qdrant**, a maintained package **`dspy-qdrant`** exposes `QdrantRM`:
  ```python
  from qdrant_client import QdrantClient
  from dspy_qdrant import QdrantRM
  qdrant_client = QdrantClient()
  retrieve = QdrantRM(qdrant_collection_name="my_collection_name", qdrant_client=qdrant_client, k=5)
  ```
  Params: `qdrant_collection_name` (required), `qdrant_client` (required), `k` (default 3), `document_field` (default `"document"`), `vectorizer` (defaults to FastEmbedVectorizer). Source: https://github.com/qdrant/dspy-qdrant
- For **Chroma**, no official first-party DSPy integration was found (**UNVERIFIED**) — write a plain function wrapping `chromadb`'s query API returning `.passages`/a list of strings and call it inside `forward()`, matching the tutorial's own pattern.

### 4.4 Signatures/modules — minimal current idiomatic RAG example

```python
import dspy

lm = dspy.LM("ollama_chat/qwen3.8:27b", api_base="http://127.0.0.1:11435", api_key="")
dspy.configure(lm=lm)

embedder = dspy.Embedder("openai/text-embedding-3-small", dimensions=512)
search = dspy.retrievers.Embeddings(embedder=embedder, corpus=corpus, k=5)

class RAG(dspy.Module):
    def __init__(self):
        self.respond = dspy.ChainOfThought("context, question -> response")

    def forward(self, question):
        context = search(question).passages
        return self.respond(context=context, question=question)

rag = RAG()
rag(question="what are high memory and low memory on linux?")
```
Source: https://github.com/stanfordnlp/dspy/blob/main/docs/docs/tutorials/rag/index.ipynb

- Signatures use in-line strings, e.g. `"question: str -> response: str"` or shorthand `"context, question -> response"` (default field type `str`).
- `dspy.Predict` is the base module (no reasoning); `dspy.ChainOfThought` wraps it and elicits a `reasoning` field before the requested outputs. Other built-ins: `dspy.ProgramOfThought`, `dspy.ReAct`.
- `dspy.Module` subclasses declare sub-modules in `__init__`, free-form Python control flow in `forward` — this is how retrieval + generation compose into one optimizable program.
- `dspy.inspect_history(n=1)` shows the actual prompt(s) sent to the LM — useful when debugging locally against Ollama.

### 4.5 Optimizers

Source: https://dspy.ai/learn/optimization/optimizers/ and the RAG tutorial notebook.

- General definition: "A DSPy optimizer is an algorithm that can tune the parameters of a DSPy program (i.e., the prompts and/or the LM weights) to maximize the metrics you specify, like accuracy."
- **`dspy.MIPROv2`**: generates instructions *and* few-shot examples per step, data/demonstration-aware, Bayesian-optimization search over generation instructions/demos (3 stages: bootstrapping traces → grounded instruction proposal → discrete search).
  ```python
  tp = dspy.MIPROv2(metric=metric, auto="medium", num_threads=24)
  optimized_rag = tp.compile(RAG(), trainset=trainset, max_bootstrapped_demos=2, max_labeled_demos=2)
  ```
  `auto` accepts presets `"light"`/`"medium"`/etc. (cost/time tradeoff); tutorial notes a `"medium"` run costs "~$1.5" and 20–30 minutes with the original (OpenAI) example.
- **`dspy.BootstrapFewShot`**: uses a `teacher` module (defaults to your program) to generate demonstrations for every stage, plus labeled examples from `trainset`. Params: `max_labeled_demos`, `max_bootstrapped_demos`.
- **`dspy.BootstrapFewShotWithRandomSearch`**: applies `BootstrapFewShot` multiple times with random search over generated demos, picks the best program; extra param `num_candidate_programs`:
  ```python
  config = dict(max_bootstrapped_demos=4, max_labeled_demos=4, num_candidate_programs=10, num_threads=4)
  teleprompter = dspy.BootstrapFewShotWithRandomSearch(metric=YOUR_METRIC_HERE, **config)
  optimized_program = teleprompter.compile(YOUR_PROGRAM_HERE, trainset=YOUR_TRAINSET_HERE)
  ```
- **`dspy.Evaluate`**:
  ```python
  evaluate = dspy.Evaluate(devset=devset, metric=metric, num_threads=24, display_progress=True, display_table=2)
  evaluate(rag)
  ```
- **Metric example**: `dspy.evaluate.SemanticF1` (`from dspy.evaluate import SemanticF1; metric = SemanticF1(decompositional=True)`), called as `metric(example, pred)` → float score; itself a small DSPy module using the configured LM as judge. Source: https://github.com/stanfordnlp/dspy/blob/main/dspy/evaluate/auto_evaluation.py
- Data prep: `dspy.Example(**dict_row).with_inputs("question")`; split into train/dev/test (tutorial suggests 30–300 each); `MIPROv2` auto-splits 20/80 train/val if no `valset` given.
- Save/load: `optimized_rag.save("optimized_rag.json")`, then `RAG().load("optimized_rag.json")`.

**Practical note for a local Ollama eval loop**: `SemanticF1` calls the configured LM as judge, so with `qwen3.8:27b` as both the RAG model and the judge, expect slower/less reliable scoring than the original tutorial's GPT-4o-mini judge — consider a simpler exact-match/custom metric for a fully local, fast eval loop (this is reasoning, not a doc fact).

### 4.6 Philosophy vs. LangChain/LlamaIndex/Haystack

- DSPy README, verbatim: **"DSPy is the framework for programming—rather than prompting—language models."** and **"Instead of brittle prompts, you write compositional Python code and use DSPy to teach your LM to deliver high-quality outputs."** Source: https://github.com/stanfordnlp/dspy/blob/main/README.md
- No explicit head-to-head comparison sentence naming LangChain/LlamaIndex/Haystack was found on fetched pages — the "framework vs. compiler" contrast is **UNVERIFIED against official docs** as a direct quote, though consistent with DSPy's own tutorial design: retrieval is "any Python code you plug in," while the value-add is the optimizer/compile step (`MIPROv2`, `BootstrapFewShot*`) that rewrites instructions and selects few-shot demos to raise a measured metric. DSPy ships no retrieval framework, vector-store abstraction hierarchy, or document-loader ecosystem of its own, unlike the other three.

---

## 5. Comparison table (2026, as commonly reported)

GitHub star counts fetched directly from each repo's page on 2026-08-30: https://github.com/langchain-ai/langchain (145.3k), https://github.com/run-llama/llama_index (51.9k), https://github.com/deepset-ai/haystack (26.4k), https://github.com/stanfordnlp/dspy (37.7k).

Narrative comparison points below are drawn from a web search of 2026 secondary sources (not official docs) — cited inline, treat framing/opinions as **community consensus, not verified fact**: https://www.secondtalent.com/resources/top-rag-frameworks-and-tools-for-enterprise-ai-applications/, https://gigagpu.com/langchain-vs-llamaindex-vs-haystack-2026/, https://alphacorp.ai/blog/rag-frameworks-top-5-picks-in-2026, https://iternal.ai/blockify-rag-frameworks, https://pecollective.com/blog/ai-orchestration-frameworks-2026/

| Dimension | LangChain (+LangGraph) | LlamaIndex | Haystack 2.x | DSPy |
|---|---|---|---|---|
| Philosophy | General-purpose LLM app/agent orchestration framework; RAG is one use case among many (chains → LCEL → agentic, now built on LangGraph) | Retrieval/indexing-first framework — "no framework takes retrieval more seriously" per community sources | Production-first pipeline framework: typed, serializable, testable components wired into explicit `Pipeline` graphs | Not a retrieval framework at all — a *programming/compiler* framework that optimizes prompts and few-shot demos against a metric, agnostic to how you retrieve |
| Learning curve | Moderate–steep: large surface area, frequent breaking changes (v1 namespace split, `langchain-classic`), "complexity tax for simple RAG pipelines" per community sources | Gentle for basic RAG (`Settings` + `VectorStoreIndex` + `as_query_engine` gets you far fast); steeper for Workflows/agents | Moderate: pipeline/component model is explicit and predictable once learned, less "magic" than LangChain | Steep conceptually (signatures, modules, compilation are a different mental model) but the RAG-specific code itself is short |
| RAG feature depth | Very deep via `langchain_classic` retrievers (ensemble/RRF, multi-query, parent-doc, self-query, contextual compression) + LangGraph agentic templates (Self-RAG/CRAG/Adaptive-RAG) | Very deep and RAG-specialized: fusion retrieval, HyDE, auto-merging/sentence-window, response-synthesis modes, citation engine, free local evaluators | Solid core (hybrid via `DocumentJoiner`+RRF, HyDE cookbook, many rerankers, `Agent` component) but fewer named "advanced RAG" retriever classes than the other two | Minimal built-in retrieval machinery by design; RAG quality comes from optimizing the surrounding prompt/program (MIPROv2/BootstrapFewShot), not from retrieval feature breadth |
| Production-readiness | Widely deployed, huge ecosystem (350+ integrations per community sources), but breaking v1 migration is a real cost right now | Strong for retrieval-centric services; increasingly paired with LangGraph for orchestration in production per community sources | "Rebuilt from scratch as Haystack 2.0... cleanest pipeline abstraction for production deployments" per community sources (deepset is enterprise-focused, common in regulated industries) | Newer to production RAG; best fit for teams doing systematic, metric-driven prompt optimization rather than shipping a retrieval stack outright |
| Community size (GitHub stars, 2026-08-30) | 145.3k (langchain-ai/langchain) | 51.9k (run-llama/llama_index) | 26.4k (deepset-ai/haystack) | 37.7k (stanfordnlp/dspy) |
| Pros | Huge ecosystem/integrations; LangGraph gives real agentic/stateful control; `create_agent` unifies agentic RAG | Cleanest DX for pure RAG; deep retrieval-specific features (fusion, HyDE, auto-merge, sentence-window); free local evaluators | Explicit, typed, testable pipelines; strong enterprise/production posture; many rerankers built in | Turns prompt engineering into an optimizable, measurable process; small, composable core; model-agnostic via LiteLLM |
| Cons | Frequent breaking changes; many "advanced" retrievers now live in a second package (`langchain-classic`); some claimed features (HyDE, sub-question decomposition) have no confirmed first-class class currently | Some advanced classes' exact import paths were not directly confirmable this session; RAPTOR pack is deprecated/unmaintained | Fewer named advanced-retrieval abstractions than LangChain/LlamaIndex; smallest community of the three RAG-first frameworks | No built-in vector-store/document-loader ecosystem; retrieval is fully DIY; official RAG tutorial doesn't demo Chroma/Qdrant at all (Qdrant only via a 3rd-party `dspy-qdrant` package) |

**Common 2026 production pattern reported in secondary sources**: LlamaIndex for retrieval + LangChain/LangGraph for orchestration + RAGAS (free/local) or LangSmith (paid) for evaluation, with LlamaIndex retrievers pluggable into LangChain chains and DSPy modules wrapping LangChain components (https://www.secondtalent.com/resources/top-rag-frameworks-and-tools-for-enterprise-ai-applications/, https://pecollective.com/blog/ai-orchestration-frameworks-2026/) — **UNVERIFIED as an official recommendation**, this is community-blog framing, cite with that caveat if used in the tutorial.
