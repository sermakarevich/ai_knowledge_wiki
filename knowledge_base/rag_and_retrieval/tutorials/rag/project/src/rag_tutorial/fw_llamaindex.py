"""Chapter 09 — the same RAG toolkit, now expressed through LlamaIndex.

LlamaIndex (LI) is the RAG-first framework: documents become nodes via
*node parsers*, nodes live in indexes, and *retrievers* / *query engines* /
*postprocessors* compose the pipeline. Everything expensive and validated
(chunk text, the golden set, judges, the shared answer prompt) stays in
`rag_tutorial`; this file adds the LI *glue*:

- LI models: `Ollama` (chat) + `OllamaEmbedding` on `Settings` (the global
  config object that replaced the old `ServiceContext`), pointed at the same
  Ollama server as `rag_tutorial.llm.ollama`.
- LI documents: `SimpleDirectoryReader` over `data/corpus/md` (12 papers).
- LI node sets via `IngestionPipeline` (local node cache under
  `data/indexes/`): naive (`MarkdownNodeParser` + `SentenceSplitter`),
  sentence-window (`SentenceWindowNodeParser`), hierarchical
  (`HierarchicalNodeParser`, the parent/child pyramid behind auto-merging).
- Ten `09_li_*` pipelines, compared side by side on the same scoreboard:
    li_naive            — VectorStoreIndex + top-k vector retriever
    li_sentence_window  — sentence nodes retrieved, window swapped back in
                          (`MetadataReplacementPostProcessor`)
    li_auto_merging     — HierarchicalNodeParser + AutoMergingRetriever
    li_fusion           — QueryFusionRetriever (vector + BM25, reciprocal
                          rerank, num_queries=3)
    li_fusion_rerank    — fusion + SentenceTransformerRerank (bge-reranker-v2-m3)
    li_subquestion      — SubQuestionQueryEngine (one tool per 3 papers)
    li_router           — RouterQueryEngine (vector tool vs SummaryIndex tool)
    li_mode_compact / li_mode_refine / li_mode_tree_summarize — same vector
                          retriever, three response-synthesis modes
- LI built-in evaluators (`FaithfulnessEvaluator`, `RelevancyEvaluator`,
  `CorrectnessEvaluator`) run over the `li_fusion_rerank` predictions and
  compared against our own judge (agreement %).

Node -> chunk mapping: every LI node carries `start_char_idx`/`end_char_idx`
offsets into its source document, so `node_to_chunk` rebuilds our
deterministic chunk id with `chunk_id(paper, start, end)` (hierarchical
parents without offsets fall back to a hash of paper+text).

Run:
    uv run python -m rag_tutorial.fw_llamaindex index
    uv run python -m rag_tutorial.fw_llamaindex ask "..." --pipeline li_fusion
    uv run python -m rag_tutorial.fw_llamaindex eval --pipeline li_naive
    uv run python -m rag_tutorial.fw_llamaindex eval-all
    uv run python -m rag_tutorial.fw_llamaindex li-eval
"""

from __future__ import annotations

import hashlib
import json
import time
from functools import lru_cache
from pathlib import Path
from typing import ClassVar

import typer
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated

from rag_tutorial.baseline import _short_names
from rag_tutorial.config import settings
from rag_tutorial.corpus import MD_DIR
from rag_tutorial.evaluate import (
    RUNS_DIR,
    evaluate_run,
    judge_abstain,
    judge_correctness,
    judge_faithfulness,
    retrieval_metrics,
)
from rag_tutorial.llm import ollama
from rag_tutorial.prompts import build_messages
from rag_tutorial.schema import Chunk, chunk_id

app = typer.Typer(add_completion=False)
console = Console()

# ---------------------------------------------------------------------------
# LlamaIndex model singletons (Settings.llm / Settings.embed_model)
# ---------------------------------------------------------------------------

# Imported at module level like fw_langchain does with langchain: the
# `llamaindex` uv group is installed in this project, and unit tests use the
# MockLLM/MockEmbedding from the same package (no network on import).
from llama_index.core import Settings, SimpleDirectoryReader, StorageContext, VectorStoreIndex
from llama_index.core.ingestion import IngestionCache, IngestionPipeline
from llama_index.core.node_parser import (
    HierarchicalNodeParser,
    MarkdownNodeParser,
    SentenceSplitter,
    SentenceWindowNodeParser,
)
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama


class CountingOllama(Ollama):
    """`Ollama` LLM that counts every completion/chat call at class level.

    Retrieval-side LLM calls (fusion query generation, sub-question
    decomposition, routing, tree summarisation) go through `Settings.llm`,
    i.e. through this class, while the *answer* for retriever pipelines uses
    the shared cached prompt (counted separately as one generator call) and
    judge calls go through the raw `ollama` client. Reset with
    `CountingOllama.calls = 0` and read the delta — the honest
    `llm_calls_per_q` for the scoreboard.

    NOTE: `calls` must be `ClassVar` — a bare `calls: int = 0` annotation
    becomes a pydantic model *field* (not a real class attribute), so the
    first `type(self).calls` read in a fresh process (e.g. `li-eval`, which
    never resets the counter before `achat`) raises
    `AttributeError: calls` via the model metaclass `__getattr__`.
    """

    calls: ClassVar[int] = 0

    def _count(self) -> None:
        type(self).calls += 1

    def chat(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        self._count()
        return super().chat(*args, **kwargs)

    def complete(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        self._count()
        return super().complete(*args, **kwargs)

    async def achat(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        self._count()
        return await super().achat(*args, **kwargs)

    async def acomplete(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        self._count()
        return await super().acomplete(*args, **kwargs)


_configured = False


def _configure() -> None:
    """Point the `Settings` singleton at our Ollama server (idempotent).

    Kept out of module import so unit tests can install `MockLLM` /
    `MockEmbedding` on `Settings` without ever touching the network.
    """
    global _configured
    if _configured:
        return
    Settings.llm = CountingOllama(
        model=settings.chat_model,
        base_url=ollama.base_url,
        temperature=0.0,
        # RouterQueryEngine + tree_summarize routes issue single LLM calls
        # well above 300s (other global questions took 140-250s for 2 calls);
        # 900s lets slow summary calls finish instead of ReadTimeout-crashing.
        request_timeout=900.0,
    )
    Settings.embed_model = OllamaEmbedding(
        model_name=settings.embed_model,
        base_url=ollama.base_url,
    )
    _configured = True


# ---------------------------------------------------------------------------
# Documents + node sets (IngestionPipeline with a local cache)
# ---------------------------------------------------------------------------


def load_li_documents():
    """`SimpleDirectoryReader` over the 12 parsed papers; `paper` = file stem."""
    _configure()
    # NOTE (installed version wins over the research note): this repo lives
    # under `~/.ai`, and 0.14.x `is_hidden` flags any path with a dot-part
    # (`.ai`) as hidden — so every file would be skipped with the default
    # `exclude_hidden=True`. Our corpus has no dot-files; disable the filter.
    docs = SimpleDirectoryReader(
        input_dir=str(MD_DIR),
        required_exts=[".md"],
        filename_as_id=True,
        exclude_hidden=False,
    ).load_data()
    for doc in docs:
        paper = Path(doc.metadata.get("file_name", doc.doc_id or "")).stem or doc.doc_id
        doc.metadata["paper"] = paper
        doc.id_ = paper
    return docs


def _pipeline(transformations) -> IngestionPipeline:
    # `IngestionCache` (persisted under data/indexes/) skips re-parsing
    # documents whose hash is unchanged; the docstore dedups re-runs.
    from llama_index.core.storage.docstore import SimpleDocumentStore

    return IngestionPipeline(
        transformations=list(transformations),
        cache=IngestionCache(),
        docstore=SimpleDocumentStore(),
    )


def build_naive_nodes(docs):
    """Spec §1: `MarkdownNodeParser` (header-aware split) then `SentenceSplitter`."""
    return _pipeline([MarkdownNodeParser(), SentenceSplitter(chunk_size=512, chunk_overlap=64)]).run(documents=docs)


def build_window_nodes(docs):
    """Spec §2: one node per sentence, ±3-sentence window kept in metadata."""
    return _pipeline([SentenceWindowNodeParser(window_size=3)]).run(documents=docs)


def build_hier_nodes(docs):
    """Spec §3: coarse-to-fine pyramid (512 -> 128 -> 64 chars) for auto-merging."""
    return _pipeline([HierarchicalNodeParser.from_defaults(chunk_sizes=[512, 128, 64])]).run(documents=docs)


# ---------------------------------------------------------------------------
# Index persistence (data/indexes/ is gitignored; embeddings are one-time)
# ---------------------------------------------------------------------------


def _index_dir(name: str) -> Path:
    return settings.path(f"data/indexes/li_09_{name}")


def build_or_load_index(name: str, nodes):
    """Load the persisted `VectorStoreIndex` if present, else embed + persist."""
    from llama_index.core import load_index_from_storage

    _configure()
    persist_dir = _index_dir(name)
    if (persist_dir / "docstore.json").exists():
        return load_index_from_storage(StorageContext.from_defaults(persist_dir=str(persist_dir)))
    index = VectorStoreIndex(nodes, show_progress=True)
    persist_dir.mkdir(parents=True, exist_ok=True)
    index.storage_context.persist(persist_dir=str(persist_dir))
    return index


@lru_cache(maxsize=8)
def _naive_index():
    return build_or_load_index("naive", build_naive_nodes(load_li_documents()))


@lru_cache(maxsize=8)
def _window_index():
    return build_or_load_index("window", build_window_nodes(load_li_documents()))


@lru_cache(maxsize=8)
def _hier_index():
    return build_or_load_index("hier", build_hier_nodes(load_li_documents()))


# ---------------------------------------------------------------------------
# Node -> Chunk mapping (via start_char_idx / end_char_idx)
# ---------------------------------------------------------------------------


def node_chunk_id(paper: str, start: int | None, end: int | None, text: str) -> str:
    """Deterministic chunk id for a node: `chunk_id(paper, start, end)` when the
    parser recorded offsets, else a hash of paper+text (hierarchical parents)."""
    if start is not None and end is not None:
        return chunk_id(paper, int(start), int(end))
    return hashlib.sha1(f"{paper}:{text}".encode("utf-8")).hexdigest()[:16]


def node_to_chunk(node) -> Chunk:
    """Map an LI node (or NodeWithScore) back onto our `Chunk` schema."""
    inner = getattr(node, "node", node)  # unwrap NodeWithScore
    get_text = getattr(inner, "get_content", None)
    text = get_text() if callable(get_text) else getattr(inner, "text", "")
    meta = dict(getattr(inner, "metadata", None) or {})
    paper = str(meta.get("paper", meta.get("file_name", "unknown")))
    if paper.endswith(".md"):
        paper = paper[: -len(".md")]
    start = getattr(inner, "start_char_idx", None)
    end = getattr(inner, "end_char_idx", None)
    return Chunk(
        id=node_chunk_id(paper, start, end, text or ""),
        paper=paper,
        section=str(meta.get("section", meta.get("header", ""))),
        text=text or "",
        start=int(start or 0),
        end=int(end or 0),
        meta={},
    )


def _as_contexts(chunks: list[Chunk]) -> list[str]:
    short_names = _short_names()
    return [f"[{short_names.get(c.paper, c.paper)}] {c.text}" for c in chunks]


def _shared_answer(question: str, chunks: list[Chunk]) -> tuple[str, list[str]]:
    """The shared ch03 prompt through the cached `ollama` client (1 generator call)."""
    triples = [(_short_names().get(c.paper, c.paper), c.section, c.text) for c in chunks]
    reply = ollama.chat(build_messages(question, triples), max_tokens=384)
    return reply, _as_contexts(chunks)


_k_global = 5


# ---------------------------------------------------------------------------
# Retriever builders (spec §1-5)
# ---------------------------------------------------------------------------


def _naive_retriever(k: int):
    return _naive_index().as_retriever(similarity_top_k=k)


def _window_retriever(k: int):
    """Sentence nodes retrieved, then `MetadataReplacementPostProcessor`
    swaps each sentence back for its ±3-sentence window before scoring."""
    from llama_index.core.postprocessor import MetadataReplacementPostProcessor

    base = _window_index().as_retriever(similarity_top_k=k)
    post = MetadataReplacementPostProcessor(target_metadata_key="window")

    class _WindowRetriever:
        def retrieve(self, query: str):
            nodes = base.retrieve(query)
            return post.postprocess_nodes(nodes, query_str=query)

    return _WindowRetriever()


def _automerge_retriever(k: int):
    """Leaf-level search over the hierarchical pyramid; `AutoMergingRetriever`
    merges children back into the parent when enough of them hit."""
    from llama_index.core.retrievers.auto_merging_retriever import AutoMergingRetriever

    index = _hier_index()
    base = index.as_retriever(similarity_top_k=k * 4)
    return AutoMergingRetriever(base, index.storage_context, verbose=False)


def _bm25_retriever(nodes, k: int):
    from llama_index.retrievers.bm25 import BM25Retriever

    return BM25Retriever.from_defaults(nodes=list(nodes), similarity_top_k=k)


def _fusion_retriever(k: int, num_queries: int = 3):
    """`QueryFusionRetriever`: vector + BM25 fused with reciprocal rerank;
    the LLM writes `num_queries` query variants (counted via CountingOllama)."""
    from llama_index.core.retrievers import QueryFusionRetriever

    _configure()
    vector = _naive_index().as_retriever(similarity_top_k=k * 2)
    docs = load_li_documents()
    bm25 = _bm25_retriever(build_naive_nodes(docs), k * 2)
    return QueryFusionRetriever(
        [vector, bm25],
        llm=Settings.llm,
        mode="reciprocal_rerank",
        similarity_top_k=k,
        num_queries=num_queries,
        use_async=False,
        verbose=False,
    )


def _fusion_rerank_retriever(k: int):
    """Fusion retrieval, then `SentenceTransformerRerank` (local cross-encoder)."""
    from llama_index.core.postprocessor import SentenceTransformerRerank

    base = _fusion_retriever(k * 2)
    post = SentenceTransformerRerank(model="BAAI/bge-reranker-v2-m3", top_n=k)

    class _RerankRetriever:
        def retrieve(self, query: str):
            nodes = base.retrieve(query)
            return post.postprocess_nodes(nodes, query_str=query)

    return _RerankRetriever()


def _retrieve_chunks(retriever, question: str, k: int) -> list[Chunk]:
    seen: set[str] = set()
    out: list[Chunk] = []
    for scored in retriever.retrieve(question):
        chunk = node_to_chunk(scored)
        if chunk.id in seen:
            continue
        seen.add(chunk.id)
        out.append(chunk)
        if len(out) >= k:
            break
    return out


def _retriever_pipeline(retriever_fn, k_opt: str = "k_global"):
    """Shared harness adapter: LI retriever -> Chunks, answer via shared prompt.

    `n_llm_calls` = retrieval-side LLM calls (fusion query-gen, counted by
    `CountingOllama`) + 1 for the generator.
    """

    def retrieve_fn(item: dict) -> list[Chunk]:
        CountingOllama.calls = 0
        k = _k_global
        chunks = _retrieve_chunks(retriever_fn(k), item["question"], k)
        item["_li_calls"] = CountingOllama.calls
        return chunks

    def answer_fn(item: dict, retrieved: list[Chunk]) -> tuple[str, list[str], int]:
        reply, contexts = _shared_answer(item["question"], retrieved)
        return reply, contexts, int(item.get("_li_calls", 0)) + 1

    return retrieve_fn, answer_fn


def pipeline_naive():
    return _retriever_pipeline(lambda k: _naive_retriever(k))


def pipeline_sentence_window():
    return _retriever_pipeline(lambda k: _window_retriever(k))


def pipeline_auto_merging():
    return _retriever_pipeline(lambda k: _automerge_retriever(k))


def pipeline_fusion():
    return _retriever_pipeline(lambda k: _fusion_retriever(k))


def pipeline_fusion_rerank():
    return _retriever_pipeline(lambda k: _fusion_rerank_retriever(k))


# ---------------------------------------------------------------------------
# Engine pipelines (spec §6-7): sub-question, router, response modes.
# These run end-to-end (their synthesis IS the experiment); retrieve_fn runs
# the engine once and stashes the response for answer_fn.
# ---------------------------------------------------------------------------


def _stash_answer(item: dict, response, calls: int) -> list[Chunk]:
    item["_li_response"] = response
    item["_li_calls"] = calls
    seen: set[str] = set()
    out: list[Chunk] = []
    for scored in getattr(response, "source_nodes", []) or []:
        chunk = node_to_chunk(scored)
        if chunk.id in seen:
            continue
        seen.add(chunk.id)
        out.append(chunk)
    return out[: _k_global]


def _stashed_answer(item: dict) -> tuple[str, list[str], int]:
    response = item.get("_li_response")
    if response is None:  # pragma: no cover - defensive; harness always retrieves first
        raise RuntimeError("answer_fn called before retrieve_fn")
    return str(response.response), _as_contexts(_stash_chunks(item)), int(item.get("_li_calls", 0))


def _stash_chunks(item: dict) -> list[Chunk]:
    seen: set[str] = set()
    out: list[Chunk] = []
    for scored in getattr(item.get("_li_response"), "source_nodes", []) or []:
        chunk = node_to_chunk(scored)
        if chunk.id in seen:
            continue
        seen.add(chunk.id)
        out.append(chunk)
    return out[: _k_global]


def _engine_pipeline(engine_fn):
    def retrieve_fn(item: dict) -> list[Chunk]:
        CountingOllama.calls = 0
        response = engine_fn().query(item["question"])
        return _stash_answer(item, response, CountingOllama.calls)

    def answer_fn(item: dict, retrieved: list[Chunk]) -> tuple[str, list[str], int]:
        return _stashed_answer(item)

    return retrieve_fn, answer_fn


_SUBQ_GROUPS = [0, 1, 2, 3]  # 4 tools, one per 3 papers (12 papers total)


@lru_cache(maxsize=1)
def _subquestion_engine():
    """`SubQuestionQueryEngine`: decomposes the question, one vector tool per
    group of 3 papers, synthesises the final answer."""
    from llama_index.core.query_engine import SubQuestionQueryEngine
    from llama_index.core.question_gen import LLMQuestionGenerator
    from llama_index.core.tools import QueryEngineTool, ToolMetadata

    _configure()
    docs = load_li_documents()
    papers = sorted({str(d.metadata["paper"]) for d in docs})
    tools = []
    for gi in _SUBQ_GROUPS:
        group = papers[gi * 3 : gi * 3 + 3]
        sub_docs = [d for d in docs if d.metadata["paper"] in group]
        nodes = build_naive_nodes(sub_docs)
        engine = VectorStoreIndex(nodes, show_progress=False).as_query_engine(similarity_top_k=3)
        tools.append(
            QueryEngineTool(
                query_engine=engine,
                metadata=ToolMetadata(
                    name=f"papers_group_{gi}",
                    description=f"Answers questions about papers: {', '.join(group)}.",
                ),
            )
        )
    # NOTE: pass LLMQuestionGenerator explicitly. from_defaults() without it
    # tries OpenAIQuestionGenerator first and hard-fails with ImportError when
    # `llama-index-question-gen-openai` is not installed; with a local Ollama
    # LLM it would fall back to LLMQuestionGenerator anyway (ValueError path),
    # so pin the local generator and skip the hosted dependency entirely.
    question_gen = LLMQuestionGenerator.from_defaults(llm=Settings.llm)
    return SubQuestionQueryEngine.from_defaults(tools, llm=Settings.llm, question_gen=question_gen, use_async=False)


@lru_cache(maxsize=1)
def _router_engine():
    """`RouterQueryEngine`: an LLM selector picks the vector tool (facts) or
    the `SummaryIndex` tool with `tree_summarize` (global questions)."""
    from llama_index.core import SummaryIndex
    from llama_index.core.query_engine import RouterQueryEngine
    from llama_index.core.selectors import LLMSingleSelector
    from llama_index.core.tools import QueryEngineTool, ToolMetadata

    _configure()
    docs = load_li_documents()
    vector_tool = QueryEngineTool(
        query_engine=_naive_index().as_query_engine(similarity_top_k=_k_global),
        metadata=ToolMetadata(name="vector", description="Dense vector search over paper chunks; best for specific factual questions."),
    )
    summary_tool = QueryEngineTool(
        query_engine=SummaryIndex(docs).as_query_engine(response_mode="tree_summarize", llm=Settings.llm),
        metadata=ToolMetadata(name="summary", description="Whole-corpus summary; best for broad global or thematic questions."),
    )
    return RouterQueryEngine.from_defaults(
        [vector_tool, summary_tool], llm=Settings.llm, selector=LLMSingleSelector.from_defaults(llm=Settings.llm)
    )


def pipeline_subquestion():
    return _engine_pipeline(_subquestion_engine)


def pipeline_router():
    return _engine_pipeline(_router_engine)


@lru_cache(maxsize=4)
def _mode_engine(response_mode: str):
    """Same naive vector retriever, three LI response-synthesis modes:
    `compact` (default: stuff chunks to fill context, few calls), `refine`
    (iterative, one call per node), `tree_summarize` (recursive bottom-up)."""
    from llama_index.core.query_engine import RetrieverQueryEngine
    from llama_index.core.response_synthesizers import get_response_synthesizer

    _configure()
    synth = get_response_synthesizer(llm=Settings.llm, response_mode=response_mode, use_async=False)  # type: ignore[arg-type]
    return RetrieverQueryEngine(_naive_index().as_retriever(similarity_top_k=_k_global), response_synthesizer=synth)


def pipeline_mode_compact():
    return _engine_pipeline(lambda: _mode_engine("compact"))


def pipeline_mode_refine():
    return _engine_pipeline(lambda: _mode_engine("refine"))


def pipeline_mode_tree_summarize():
    return _engine_pipeline(lambda: _mode_engine("tree_summarize"))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

PIPELINES = {
    "li_naive": pipeline_naive,
    "li_sentence_window": pipeline_sentence_window,
    "li_auto_merging": pipeline_auto_merging,
    "li_fusion": pipeline_fusion,
    "li_fusion_rerank": pipeline_fusion_rerank,
    "li_subquestion": pipeline_subquestion,
    "li_router": pipeline_router,
    "li_mode_compact": pipeline_mode_compact,
    "li_mode_refine": pipeline_mode_refine,
    "li_mode_tree_summarize": pipeline_mode_tree_summarize,
}

_KW = Annotated[int, typer.Option("--k", help="number of chunks to retrieve")]


@app.command()
def index() -> None:
    """Parse the corpus into LI node sets and persist the vector indexes.

    Embeddings run once (Ollama, uncached); later processes reload
    `data/indexes/li_09_*` from disk. Rebuilds from scratch if deleted.
    """
    _configure()
    docs = load_li_documents()
    console.print(f"[green]documents[/green] {len(docs)} papers from {MD_DIR}")
    t0 = time.monotonic()
    naive_nodes = build_naive_nodes(docs)
    _naive_index()
    console.print(f"[green]naive[/green] {len(naive_nodes)} nodes")
    window_nodes = build_window_nodes(docs)
    _window_index()
    console.print(f"[green]sentence-window[/green] {len(window_nodes)} nodes")
    hier_nodes = build_hier_nodes(docs)
    _hier_index()
    console.print(f"[green]hierarchical[/green] {len(hier_nodes)} nodes")
    console.print(f"[green]done[/green] in {time.monotonic() - t0:.1f}s")


@app.command()
def ask(
    question: str,
    pipeline: str = typer.Option("li_naive", "--pipeline", help=f"one of {list(PIPELINES)}"),
    k: int = typer.Option(5, "--k"),
) -> None:
    """Run one question through a pipeline; print retrieved chunks and answer."""
    global _k_global
    _k_global = k
    retrieve_fn, answer_fn = PIPELINES[pipeline]()
    item: dict = {"question": question, "evidence": []}
    retrieved = retrieve_fn(item)
    table = Table(title=f"retrieved via {pipeline} (k={k})")
    table.add_column("rank", justify="right")
    table.add_column("chunk id")
    table.add_column("paper")
    table.add_column("section", max_width=48)
    for rank, chunk in enumerate(retrieved, start=1):
        table.add_row(str(rank), chunk.id, chunk.paper, chunk.section)
    console.print(table)
    reply, _contexts, n = answer_fn(item, retrieved)
    console.print(f"\n[bold]Answer[/bold] (LLM calls: {n}):\n{reply}")


@app.command()
def eval(
    pipeline: str = typer.Option("li_naive", "--pipeline", help=f"one of {list(PIPELINES)}"),
    k: int = typer.Option(5, "--k"),
    name: str = typer.Option("", "--name", help="runs/ dir name (default 09_<pipeline>)"),
) -> None:
    """Run the shared evaluator (`evaluate_run`) on the test split through a pipeline."""
    global _k_global
    _k_global = k
    retrieve_fn, answer_fn = PIPELINES[pipeline]()
    run_name = name or f"09_{pipeline}"
    evaluate_run(run_name, chapter="09", answer_fn=answer_fn, retrieve_fn=retrieve_fn, split="test")
    console.print(f"[green]wrote[/green] runs/{run_name}/metrics.json")


@app.command(name="eval-all")
def eval_all(k: int = typer.Option(5, "--k")) -> None:
    """Evaluate every `09_li_*` pipeline (writes one runs/ dir per pipeline)."""
    global _k_global
    _k_global = k
    for pipeline in PIPELINES:
        run_name = f"09_{pipeline}"
        if (RUNS_DIR / run_name / "metrics.json").exists():
            console.print(f"[yellow]skipping[/yellow] {run_name} (metrics.json exists)")
            continue
        retrieve_fn, answer_fn = PIPELINES[pipeline]()
        console.print(f"[bold]evaluating[/bold] {run_name} ...")
        t0 = time.monotonic()
        evaluate_run(run_name, chapter="09", answer_fn=answer_fn, retrieve_fn=retrieve_fn, split="test")
        console.print(f"[green]wrote[/green] runs/{run_name}/metrics.json ({time.monotonic() - t0:.1f}s)")


@app.command(name="eval-resume")
def eval_resume(
    pipeline: str = typer.Option(..., "--pipeline", help=f"one of {list(PIPELINES)}"),
    k: int = typer.Option(5, "--k"),
) -> None:
    """Resume-safe per-question eval: same rows/metrics as `evaluate_run`.

    Appends one row to `runs/09_<pipeline>/predictions.jsonl` per question
    (flushed immediately, so a killed worker loses at most one question) and
    skips ids already on disk. Writes `metrics.json`/`config.json` in the
    exact `evaluate_run` format once all test questions are done. Safe to
    re-run across attempts; run one pipeline per worker to avoid Ollama
    contention.
    """
    from rag_tutorial.golden import QA_PATH, load_qa

    global _k_global
    _k_global = k
    retrieve_fn, answer_fn = PIPELINES[pipeline]()
    run_name = f"09_{pipeline}"
    run_dir = RUNS_DIR / run_name
    run_dir.mkdir(parents=True, exist_ok=True)
    pred_path = run_dir / "predictions.jsonl"

    done: dict[str, dict] = {}
    if pred_path.exists():
        for line in pred_path.read_text().splitlines():
            if line.strip():
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                done[row.get("id", "")] = row

    items = [item for item in load_qa(QA_PATH) if item["split"] == "test"]
    todo = [it for it in items if it["id"] not in done]
    console.print(f"[bold]{run_name}[/bold]: {len(done)}/{len(items)} done, {len(todo)} to go")
    if not todo:
        console.print("[green]already complete[/green]")
        return

    with pred_path.open("a") as f:
        for item in todo:
            start = time.monotonic()
            try:
                retrieved = retrieve_fn(item)
                answer, contexts, n_llm_calls = answer_fn(item, retrieved)
            except Exception as exc:  # one killer question (e.g. global_005
                # tree_summarize runaway exceeding request_timeout) must not
                # crash the whole run: record an explicit error row and move on.
                elapsed = time.monotonic() - start
                row = {
                    "id": item["id"],
                    "type": item["type"],
                    "question": item["question"],
                    "answer": "",
                    "error": f"{type(exc).__name__}: {exc}",
                    "retrieved_chunk_ids": [],
                    "retrieval_metrics": retrieval_metrics([], item["evidence"] or []),
                    "correctness": None
                    if item["type"] == "unanswerable"
                    else {"score": 0.0, "reason": f"query failed: {type(exc).__name__}"},
                    "faithfulness": {
                        "score": 0.0,
                        "supported": 0,
                        "total": 0,
                        "unsupported_claims": [],
                    },
                    "abstain": {"abstain": 0.0, "reason": "query failed"}
                    if item["type"] == "unanswerable"
                    else None,
                    "n_llm_calls": 0,
                    "seconds": round(elapsed, 3),
                }
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
                f.flush()
                done[item["id"]] = row
                console.print(f"[red]{item['id']}[/red] FAILED ({elapsed:.1f}s): {type(exc).__name__}")
                continue
            elapsed = time.monotonic() - start
            r_metrics = retrieval_metrics(retrieved, item["evidence"])
            faithfulness = (
                judge_faithfulness(answer, contexts)
                if contexts
                else {"score": 1.0, "supported": 0, "total": 0, "unsupported_claims": []}
            )
            if item["type"] == "unanswerable":
                abstain = judge_abstain(item["question"], answer)
                correctness = None
            else:
                correctness = judge_correctness(item["question"], item["answer"], answer)
                abstain = None
            row = {
                "id": item["id"],
                "type": item["type"],
                "question": item["question"],
                "answer": answer,
                "retrieved_chunk_ids": [c.id for c in retrieved],
                "retrieval_metrics": r_metrics,
                "correctness": correctness,
                "faithfulness": faithfulness,
                "abstain": abstain,
                "n_llm_calls": n_llm_calls,
                "seconds": round(elapsed, 3),
            }
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            f.flush()
            done[item["id"]] = row
            console.print(f"[green]{item['id']}[/green] done ({len(done)}/{len(items)}, {elapsed:.1f}s)")

    if len(done) < len(items):
        return  # more questions remain; next attempt resumes

    rows = [done[it["id"]] for it in items]
    evidence_by_id = {it["id"]: it["evidence"] for it in items}

    def _mean(xs: list[float]) -> float | None:
        return sum(xs) / len(xs) if xs else None

    retrieval_rows = [r["retrieval_metrics"] for r in rows if evidence_by_id[r["id"]]]
    correctness_scores = [r["correctness"]["score"] for r in rows if r["correctness"] is not None]
    faithfulness_scores = [r["faithfulness"]["score"] for r in rows]
    abstain_scores = [r["abstain"]["abstain"] for r in rows if r["abstain"] is not None]
    metrics = {
        "experiment": run_name,
        "chapter": "09",
        "split": "test",
        "n_questions": len(items),
        "hit@5": _mean([r["hit@5"] for r in retrieval_rows]),
        "recall@5": _mean([r["recall@5"] for r in retrieval_rows]),
        "hit@10": _mean([r["hit@10"] for r in retrieval_rows]),
        "recall@10": _mean([r["recall@10"] for r in retrieval_rows]),
        "mrr": _mean([r["mrr"] for r in retrieval_rows]),
        "ndcg@10": _mean([r["ndcg@10"] for r in retrieval_rows]),
        "correctness": _mean(correctness_scores),
        "faithfulness": _mean(faithfulness_scores),
        "unanswerable_abstain": _mean(abstain_scores),
        "llm_calls_per_q": _mean([r["n_llm_calls"] for r in rows]),
        "seconds_per_q": _mean([r["seconds"] for r in rows]),
        "details": {"cache_stats": ollama.stats.as_dict()},
    }
    (run_dir / "metrics.json").write_text(json.dumps(metrics, indent=2))
    with pred_path.open("w") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    (run_dir / "config.json").write_text(
        json.dumps({"name": run_name, "chapter": "09", "split": "test", "limit": None, "chat_model": settings.chat_model, "embed_model": settings.embed_model}, indent=2)
    )
    console.print(f"[green]wrote[/green] {run_dir}/metrics.json ({len(items)} questions)")
@app.command(name="li-eval")
def li_eval() -> None:
    """Run LI's built-in evaluators over the `li_fusion_rerank` predictions and
    compare their verdicts with our judge (agreement %).

    Writes `runs/09_li_evaluators/li_eval.json`. Costs ~3 LLM calls/question
    through `Settings.llm` (uncached); reuse the predictions already on disk.
    """
    from llama_index.core.evaluation import CorrectnessEvaluator, FaithfulnessEvaluator, RelevancyEvaluator

    _configure()
    pred_path = settings.path("runs/09_li_fusion_rerank/predictions.jsonl")
    rows = [json.loads(line) for line in pred_path.read_text().splitlines() if line.strip()]
    qa_by_id = {}
    from rag_tutorial.golden import QA_PATH, load_qa

    for item in load_qa(QA_PATH):
        qa_by_id[item["id"]] = item

    fe = FaithfulnessEvaluator(llm=Settings.llm)
    re_ = RelevancyEvaluator(llm=Settings.llm)
    ce = CorrectnessEvaluator(llm=Settings.llm)
    # Contexts are not stored in predictions.jsonl (only chunk ids), so rebuild
    # the id->Chunk map from the deterministic naive node set (local parse, no
    # LLM/embedding calls). Fusion(-rerank) retrieves from these same nodes.
    by_id: dict[str, Chunk] = {}
    for _node in build_naive_nodes(load_li_documents()):
        _chunk = node_to_chunk(_node)
        by_id.setdefault(_chunk.id, _chunk)
    run_dir = settings.path("runs/09_li_evaluators")
    run_dir.mkdir(parents=True, exist_ok=True)
    partial_path = run_dir / "li_eval.jsonl"
    done: dict[str, dict] = {}
    if partial_path.exists():
        for line in partial_path.read_text().splitlines():
            if line.strip():
                try:
                    _r = json.loads(line)
                    done[_r.get("id", "")] = _r
                except json.JSONDecodeError:
                    continue
    if done:
        console.print(f"[yellow]resuming[/yellow] li-eval: {len(done)} rows already done")

    async def _eval_one(question: str, answer: str, contexts: list, reference: str | None):  # type: ignore[no-untyped-def]
        # NOTE: use the async `aevaluate` entry points under ONE event loop.
        # The sync `.evaluate()` wrapper goes through llama_index `asyncio_run`,
        # which breaks on its 2nd+ call in the same process on Python 3.14
        # (every call after the first raises a bogus "Detected nested async").
        li_f = await fe.aevaluate(query=question, response=answer, contexts=contexts)
        li_r = await re_.aevaluate(query=question, response=answer, contexts=contexts)
        li_c = await ce.aevaluate(query=question, response=answer, contexts=contexts, reference=reference or None)
        return li_f, li_r, li_c

    async def _eval_all(jobs):  # type: ignore[no-untyped-def]
        results = []
        for job in jobs:
            qid = job["id"]
            if qid in done:
                results.append(done[qid])
                continue
            try:
                li_f, li_r, li_c = await _eval_one(job["question"], job["answer"], job["contexts"], job["reference"])
                row_out = {
                    "id": qid,
                    "li_faithfulness": {"passing": bool(li_f.passing), "score": li_f.score, "feedback": li_f.feedback},
                    "li_relevancy": {"passing": bool(li_r.passing), "score": li_r.score, "feedback": li_r.feedback},
                    "li_correctness": {"passing": bool(li_c.passing), "score": li_c.score, "feedback": li_c.feedback},
                    "ours_correctness": job["ours_c"],
                    "ours_faithfulness": job["ours_f"],
                }
            except Exception as exc:  # noqa: BLE001 — record and continue
                row_out = {"id": qid, "error": f"{type(exc).__name__}: {exc}", "ours_correctness": job["ours_c"], "ours_faithfulness": job["ours_f"]}
            with partial_path.open("a") as f:
                f.write(json.dumps(row_out, ensure_ascii=False) + "\n")
            results.append(row_out)
            console.print(f"[green]{qid}[/green] done ({len(results)}/{len(jobs)})")
        return results

    jobs = []
    for row in rows:
        qid = row.get("id") or row.get("question_id") or ""
        item = qa_by_id.get(qid, {})
        question = row.get("question", item.get("question", ""))
        answer = row.get("answer", "")
        chunks = [by_id[cid] for cid in (row.get("retrieved_chunk_ids") or []) if cid in by_id]
        jobs.append({
            "id": qid,
            "question": question,
            "answer": answer,
            "contexts": _as_contexts(chunks),
            "reference": item.get("answer", ""),
            "ours_c": (row.get("correctness") or {}).get("score"),
            "ours_f": (row.get("faithfulness") or {}).get("score"),
        })
    import asyncio

    out = asyncio.run(_eval_all(jobs))
    out = [r for r in out if "error" not in r]

    def agreement(li_key: str, ours_key: str, thresh: float = 0.5) -> float:
        pairs = [(r[li_key]["passing"], r[ours_key]) for r in out if r[ours_key] is not None]
        agree = sum(1 for passing, ours in pairs if passing == (ours >= thresh))
        return agree / len(pairs) if pairs else 0.0

    table = {
        "n": len(out),
        "agreement_li_faithfulness_vs_ours_faithfulness": agreement("li_faithfulness", "ours_faithfulness"),
        "agreement_li_correctness_vs_ours_correctness": agreement("li_correctness", "ours_correctness"),
        "agreement_li_relevancy_vs_ours_correctness": agreement("li_relevancy", "ours_correctness"),
    }
    run_dir = settings.path("runs/09_li_evaluators")
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "li_eval.json").write_text(json.dumps({"rows": out, "agreement": table}, indent=2))
    console.print(f"[green]wrote[/green] runs/09_li_evaluators/li_eval.json")
    console.print(json.dumps(table, indent=2))


if __name__ == "__main__":
    app()
