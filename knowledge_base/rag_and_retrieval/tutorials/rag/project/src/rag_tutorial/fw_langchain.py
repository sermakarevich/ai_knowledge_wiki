"""Chapter 08 — the same RAG toolkit, now expressed through a framework.

Everything expensive and validated (chunking, embeddings, Chroma, golden set,
judges) stays in `rag_tutorial`; this file adds the framework *glue*:

- LangChain models (`ChatOllama`, `OllamaEmbeddings`) pointed at the same
  Ollama server as `rag_tutorial.llm.ollama`
- LangChain vectorstore (Chroma, same on-disk collection as chapter 03)
- Four `langchain_classic` retriever patterns, compared side by side:
    lc_naive            — direct vector similarity search (`as_retriever`)
    lc_parent           — ParentDocumentRetriever (child search → parent fetch)
    lc_multiquery       — MultiQueryRetriever (LLM rewrites, parallel search,
                          reciprocal-rank union handled by the retriever)
    lc_ensemble         — EnsembleRetriever (dense + BM25, weighted RRF)
    lc_ensemble_rerank  — lc_ensemble + a cross-encoder reranker
- One LangGraph workflow:
    lg_crag             — agentic Corrective-RAG loop:
                          retrieve → LLM grades sufficiency → if not, rewrite +
                          re-retrieve → answer (2-hop graph, not a straight line)

Run:
    uv run python -m rag_tutorial.fw_langchain index
    uv run python -m rag_tutorial.fw_langchain ask "..." --pipeline lc_ensemble
    uv run python -m rag_tutorial.fw_langchain eval --pipeline lc_naive --k 5
    uv run python -m rag_tutorial.fw_langchain eval --pipeline lg_crag
"""

from __future__ import annotations

import json
import logging
import time
from collections.abc import Callable
from functools import lru_cache
from typing import TypedDict

import typer
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated

from rag_tutorial.baseline import COLLECTION_NAME, _short_names
from rag_tutorial.config import settings
from rag_tutorial.corpus import load_papers
from rag_tutorial.evaluate import evaluate_run
from rag_tutorial.golden import load_documents
from rag_tutorial.llm import ollama
from rag_tutorial.prompts import build_messages
from rag_tutorial.rerankers import CrossEncoderReranker
from rag_tutorial.schema import Chunk
from rag_tutorial.stores import ChromaStore

app = typer.Typer(add_completion=False)
console = Console()

# ---------------------------------------------------------------------------
# LangChain model + vectorstore singletons
# ---------------------------------------------------------------------------

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.documents import Document as LCDocument
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import Runnable
from langchain_core.vectorstores import VectorStore
from langchain_ollama import ChatOllama, OllamaEmbeddings


class CallCounter(BaseCallbackHandler):
    """LangChain callback that counts every LLM invocation (chat or completion).

    Attached to `ChatOllama` so multi-step pipelines (multiquery rewrite calls,
    CRAG grade calls) report an honest `llm_calls_per_q` on the scoreboard.
    The *judge* calls in `evaluate_run` go through the raw `ollama` client and
    are excluded — same convention as chapters 03-07.
    """

    def __init__(self) -> None:
        self.count = 0

    def on_chat_model_start(self, *_, **__):
        self.count += 1

    def on_llm_start(self, *_, **__):
        self.count += 1


_counter = CallCounter()


@lru_cache(maxsize=1)
def chat_model() -> BaseChatModel:
    """`ChatOllama` over the same server/model as `rag_tutorial.llm.ollama`
    (temperature 0, seed 42 for reproducibility, big context window)."""
    m: BaseChatModel = ChatOllama(
        base_url=ollama.base_url,
        model=settings.chat_model,
        temperature=0.0,
        seed=42,
        num_ctx=16384,
    )
    m.callbacks = [_counter]
    return m


@lru_cache(maxsize=1)
def embed_model() -> OllamaEmbeddings:
    """`OllamaEmbeddings` for the same `nomic-embed-text` model (server-side
    weights, no HF download)."""
    return OllamaEmbeddings(base_url=ollama.base_url, model=settings.embed_model)


@lru_cache(maxsize=1)
def chroma_store() -> ChromaStore:
    """The same Chroma collection chapter 03 built (`baseline_fixed_512`)."""
    return ChromaStore(COLLECTION_NAME)


class _StoreAdapter(VectorStore):
    """Minimal LangChain `VectorStore` over `rag_tutorial.stores.ChromaStore`, so
    the framework's retrievers work against the one source of truth on disk."""

    def __init__(self, store: ChromaStore):
        self._store = store
        self.embedding = embed_model()

    @classmethod
    def from_texts(cls, texts: list[str], embeddings: list[list[float]], **_kw):
        raise NotImplementedError(
            "_StoreAdapter wraps a fixed Chroma collection; it is read-only and "
            "cannot be built from in-memory texts."
        )

    def similarity_search(self, query: str, k: int = 4, **_kw) -> list[LCDocument]:
        emb = self.embedding.embed_query(query)
        out = []
        for chunk, score in self._store.query(emb, k=k):
            out.append(
                LCDocument(
                    page_content=chunk.text,
                    metadata={
                        "id": chunk.id,
                        "paper": chunk.paper,
                        "section": chunk.section,
                        "start": chunk.start,
                        "end": chunk.end,
                        "score": score,
                    },
                )
            )
        return out


def _to_chunk(doc: LCDocument) -> Chunk:
    m = doc.metadata
    return Chunk(
        id=m["id"],
        paper=m["paper"],
        section=m.get("section", ""),
        text=doc.page_content,
        start=int(m.get("start", 0)),
        end=int(m.get("end", 0)),
        meta={},
    )


# ---------------------------------------------------------------------------
# Shared pieces
# ---------------------------------------------------------------------------

_KW = Annotated[int, typer.Option("--k", help="number of chunks to retrieve")]


def _as_contexts(chunks: list[Chunk]) -> list[str]:
    """The exact `[short_name] text` strings the shared prompt uses (and the
    faithfulness judge receives) — identical to `baseline.answer`."""
    short_names = _short_names()
    return [f"[{short_names.get(c.paper, c.paper)}] {c.text}" for c in chunks]


def make_answer() -> Callable[[str, list[Chunk]], tuple[str, list[str], int]]:
    """Answer via `ChatOllama` + the SHARED prompt (same as every other chapter).
    Returns `(answer, contexts, n_llm_calls)` where n counts generator calls
    only — judge calls are the evaluator's business."""
    model = chat_model()

    def answer(question: str, chunks: list[Chunk]) -> tuple[str, list[str], int]:
        triples = [(_short_names().get(c.paper, c.paper), c.section, c.text) for c in chunks]
        messages = build_messages(question, triples)
        before = _counter.count
        reply: str = model.invoke([{"role": m["role"], "content": m["content"]} for m in messages]).content
        return reply, _as_contexts(chunks), max(0, _counter.count - before)

    return answer


# ---------------------------------------------------------------------------
# Pipeline 1 — naive (direct vector search as a LangChain retriever)
# ---------------------------------------------------------------------------


def pipeline_naive():
    store = chroma_store()
    adapter = _StoreAdapter(store)
    retriever = adapter.as_retriever(search_kwargs={"k": 5})
    answer = make_answer()

    def retrieve_fn(item: dict) -> list[Chunk]:
        return [_to_chunk(d) for d in retriever.invoke(item["question"])][: _k_global]

    def answer_fn(item: dict, retrieved: list[Chunk]) -> tuple[str, list[str], int]:
        return answer(item["question"], retrieved)

    return retrieve_fn, answer_fn


_k_global = 5


# ---------------------------------------------------------------------------
# Pipeline 2 — parent (ParentDocumentRetriever: child search + parent fetch)
# ---------------------------------------------------------------------------


def pipeline_parent():
    """Parent-document retrieval (child search → fetch the parent context by id).

    In langchain 1.x the two-collection retriever is `MultiVectorRetriever`
    (`vectorstore` = child search, `docstore` = parent lookup by id). Our chunks
    are self-contained, so the *parent* fetched for a child is the full passage;
    the `docstore` is therefore just an id->text map over the whole corpus.
    Structurally identical to the standard two-collection setup: child_search →
    collect ids → parent fetch by id.
    """
    from langchain_classic.retrievers import MultiVectorRetriever
    from langchain_core.stores import InMemoryStore

    store = chroma_store()
    adapter = _StoreAdapter(store)
    by_id = _corpus_chunk_ids()
    text_to_chunk = {c.text: c for c in by_id.values()}
    docstore = InMemoryStore()
    if by_id:
        docstore.mset([(cid, c.text) for cid, c in by_id.items()])
    retriever = MultiVectorRetriever(
        vectorstore=adapter,
        docstore=docstore,
        id_key="id",
        search_kwargs={"k": _k_global * 2},
    )
    answer = make_answer()

    def retrieve_fn(item: dict) -> list[Chunk]:
        out: list[Chunk] = []
        seen: set[str] = set()
        for text in retriever.invoke(item["question"]):
            c = text_to_chunk.get(text)
            if c is None or c.id in seen:
                continue
            seen.add(c.id)
            out.append(c)
        return out[:_k_global]

    def answer_fn(item: dict, retrieved: list[Chunk]) -> tuple[str, list[str], int]:
        return answer(item["question"], retrieved)

    return retrieve_fn, answer_fn


# ---------------------------------------------------------------------------
# Pipeline 3 — multiquery (LLM rewrites; parallel searches unioned)
# ---------------------------------------------------------------------------


def pipeline_multiquery():
    from langchain_classic.retrievers import MultiQueryRetriever

    store = chroma_store()
    adapter = _StoreAdapter(store)
    retriever = MultiQueryRetriever.from_llm(
        adapter.as_retriever(search_kwargs={"k": _k_global}),
        chat_model(),
        include_original=False,
    )
    answer = make_answer()

    def retrieve_fn(item: dict) -> list[Chunk]:
        seen: set[str] = set()
        out: list[Chunk] = []
        for d in retriever.invoke(item["question"]):
            c = _to_chunk(d)
            if c.id not in seen:
                seen.add(c.id)
                out.append(c)
        return out[: _k_global]

    def answer_fn(item: dict, retrieved: list[Chunk]) -> tuple[str, list[str], int]:
        return answer(item["question"], retrieved)

    return retrieve_fn, answer_fn


# ---------------------------------------------------------------------------
# Pipeline 4 — ensemble (dense + BM25 via EnsembleRetriever, weighted RRF)
# ---------------------------------------------------------------------------


def _bm25_retriever(corpus: list[Chunk], k: int):
    """`BM25Retriever` over our chunks (langchain_community). The documents use
    `metadata["id"]` equal to the corpus chunk id so an id hit maps straight
    back onto a `Chunk`. `k` is set as a model field (this class's `from_texts`
    accepts `k` via `**kwargs`, not as `search_kwargs`)."""
    from langchain_community.retrievers import BM25Retriever

    return BM25Retriever.from_texts(
        [c.text for c in corpus],
        metadatas=[{"id": c.id, "paper": c.paper} for c in corpus],
        ids=[c.id for c in corpus],
        k=k,
    )


def _corpus_chunk_ids() -> dict[str, Chunk]:
    client = chroma_store().client
    col = client.get_collection(COLLECTION_NAME)
    data = col.get(include=["metadatas", "documents"])
    out: dict[str, Chunk] = {}
    for cid, text, meta in zip(data["ids"], data["documents"], data["metadatas"]):
        out[cid] = Chunk(
            id=cid,
            paper=meta["paper"],
            section=meta["section"],
            text=text,
            start=int(meta["start"]),
            end=int(meta["end"]),
            meta={},
        )
    return out


def pipeline_ensemble():
    from langchain_classic.retrievers import EnsembleRetriever

    store = chroma_store()
    adapter = _StoreAdapter(store)
    corpus = list(_corpus_chunk_ids().values())
    dense = adapter.as_retriever(search_kwargs={"k": _k_global * 2})
    bm25 = _bm25_retriever(corpus, k=_k_global * 2)
    retriever = EnsembleRetriever(retrievers=[dense, bm25], weights=(0.7, 0.3), id_key="id")
    by_id = {c.id: c for c in corpus}
    answer = make_answer()

    def retrieve_fn(item: dict) -> list[Chunk]:
        seen: set[str] = set()
        out: list[Chunk] = []
        for d in retriever.invoke(item["question"]):
            cid = d.metadata.get("id")
            if cid is None or cid in seen:
                continue
            seen.add(cid)
            src = by_id.get(cid)
            out.append(src or _to_chunk(d))
        return out[: _k_global]

    def answer_fn(item: dict, retrieved: list[Chunk]) -> tuple[str, list[str], int]:
        return answer(item["question"], retrieved)

    return retrieve_fn, answer_fn


# ---------------------------------------------------------------------------
# Pipeline 5 — ensemble + cross-encoder reranker
# ---------------------------------------------------------------------------

_RERANK_MODEL = "BAAI/bge-reranker-v2-m3"


def pipeline_ensemble_rerank():
    corpus = list(_corpus_chunk_ids().values())
    by_id = {c.id: c for c in corpus}
    reranker = CrossEncoderReranker(model=_RERANK_MODEL)
    retriever_fn, _ = pipeline_ensemble()
    answer = make_answer()

    def retrieve_fn(item: dict) -> list[Chunk]:
        candidates = retriever_fn({"question": item["question"], "evidence": []})
        return reranker.rerank(item["question"], candidates, k=_k_global)

    def answer_fn(item: dict, retrieved: list[Chunk]) -> tuple[str, list[str], int]:
        reply, contexts, n = answer(item["question"], retrieved)
        return reply, contexts, n  # reranker calls are model calls, not chat calls

    return retrieve_fn, answer_fn


# ---------------------------------------------------------------------------
# Pipeline 6 — LangGraph CRAG (agentic: retrieve → grade → rewrite? → re-retrieve)
# ---------------------------------------------------------------------------


class _CragState(TypedDict, total=False):
    """Shared mutable state flowing through the CRAG graph (retrieval loop)."""

    question: str
    attempt: int
    query: str
    contexts: list[str]
    chunks: list[Chunk]
    _sufficient: bool


def pipeline_crag():
    """A 3-node LangGraph instead of one straight line: after retrieval, an LLM
    grades whether the passages can answer the question; if not, it rewrites the
    query and we retrieve once more. `START → retrieve → grade → (rewrite →
    retrieve →) END`. Grading/rewriting are plain text (SUFFICIENT / `QUERY:`)
    so they run identically against test fakes (whose structured-output path
    raises). The final answer is produced by `answer_fn` (not a graph node) so
    it is computed and LLM-counted exactly once, matching the harness contract."""
    from langchain_core.prompts import ChatPromptTemplate
    from langgraph.graph import END, START, StateGraph

    model = chat_model()
    embed = embed_model()

    grade_prompt = ChatPromptTemplate.from_messages([
        ("system", "Decide if the passages can answer the question. Reply with SUFFICIENT or INSUFFICIENT on the first line."),
        ("human", "Question: {question}\n\nPassages:\n{contexts}"),
    ])
    rewrite_prompt = ChatPromptTemplate.from_messages([
        ("system", "Rewrite the question as a better search phrase. Reply with QUERY: <query> on the first line."),
        ("human", "Question: {question}\n\nPassages (not enough):\n{contexts}"),
    ])

    def _grade(question: str, contexts: list[str]) -> bool:
        """Text grading (no structured output) so it also works against test
        fakes, whose `with_structured_output` raises. SUFFICIENT/INSUFFICIENT
        on the first line; default to sufficient if the call fails."""
        if not contexts:
            return True
        try:
            out = str(model.invoke(grade_prompt.invoke({"question": question, "contexts": "\n\n".join(contexts[:3])})).content)
        except Exception:
            return True
        head = " ".join(out.upper().split())
        if "INSUFFICIENT" in head:
            return False
        if "SUFFICIENT" in head:
            return True
        return True

    def _rewrite(question: str, contexts: list[str]) -> str:
        """Ask the LLM for a rephrased search phrase; parse `QUERY: ...` from
        the first line. Falls back to the original question on any failure."""
        try:
            out = str(model.invoke(rewrite_prompt.invoke({"question": question, "contexts": "\n\n".join(contexts[:2])})).content)
        except Exception:
            return question
        for line in out.splitlines():
            if line.strip().upper().startswith("QUERY:"):
                new_q = line.split(":", 1)[1].strip()
                if new_q:
                    return new_q
        return question

    def do_retrieve(state: _CragState) -> dict:
        q = state["query"]
        emb = embed.embed_query(q)
        chunks = [c for c, _ in chroma_store().query(emb, k=_k_global * 2)]
        return {"chunks": chunks, "contexts": _as_contexts(chunks[:_k_global])}

    def do_grade(state: _CragState) -> dict:
        # After one rewrite we already committed to "proceed to answer with
        # whatever we got" in `route_after_grade`; grading a second time would be
        # a wasted LLM call, so short-circuit.
        if state.get("attempt", 0) >= 1:
            return {"_sufficient": True}
        return {"_sufficient": _grade(state["question"], state.get("contexts", []))}

    def do_rewrite(state: _CragState) -> dict:
        new_q = _rewrite(state["question"], state.get("contexts", []))
        return {"query": new_q or state["question"], "attempt": state.get("attempt", 0) + 1}

    def route_after_grade(state: _CragState) -> str:
        if state.get("_sufficient") or state.get("attempt", 0) >= 1:  # at most one re-retrieval
            return END
        return "rewrite"

    builder = StateGraph(_CragState)
    builder.add_node("retrieve", do_retrieve)
    builder.add_node("grade", do_grade)
    builder.add_node("rewrite", do_rewrite)
    builder.add_edge(START, "retrieve")
    builder.add_edge("retrieve", "grade")
    builder.add_conditional_edges("grade", route_after_grade, {
        "rewrite": "rewrite",
        END: END,
    })
    builder.add_edge("rewrite", "retrieve")
    graph = builder.compile()

    answer = make_answer()

    def retrieve_fn(item: dict) -> list[Chunk]:
        # Agentic loop runs here (retrieve → grade → maybe rewrite → re-retrieve);
        # the *answer* is deferred to `answer_fn` so it is computed exactly once
        # and counted exactly once on the scoreboard (the harness contract below
        # calls retrieve_fn then answer_fn and expects the LLM answer to come
        # from the latter).
        state: dict = graph.invoke({"question": item["question"], "query": item["question"], "attempt": 0})
        return list(state.get("chunks", []))[:_k_global]

    def answer_fn(item: dict, retrieved: list[Chunk]) -> tuple[str, list[str], int]:
        return answer(item["question"], retrieved)

    return retrieve_fn, answer_fn


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

PIPELINES = {
    "lc_naive": pipeline_naive,
    "lc_parent": pipeline_parent,
    "lc_multiquery": pipeline_multiquery,
    "lc_ensemble": pipeline_ensemble,
    "lc_ensemble_rerank": pipeline_ensemble_rerank,
    "lg_crag": pipeline_crag,
}


@app.command()
def index() -> None:
    """(De)build the Chroma collection chapter 03 built — this chapter just reuses it.
    If it's missing, build it via the baseline pipeline."""
    store = chroma_store()
    if store.count() > 0:
        console.print(f"[green]collection[/green] {COLLECTION_NAME!r} already has {store.count()} chunks — reusing")
        return
    console.print(f"[yellow]collection[/yellow] {COLLECTION_NAME!r} is empty — building from baseline...")
    from rag_tutorial.baseline import index as baseline_index

    baseline_index(size=512, overlap=64)


@app.command()
def ask(
    question: str,
    pipeline: str = typer.Option("lc_naive", "--pipeline", help=f"one of {list(PIPELINES)}"),
    k: int = typer.Option(5, "--k"),
) -> None:
    """Run one question through a pipeline; print the retrieved chunks and answer."""
    name = "08_" + pipeline
    with open("data/ch08_config.json", "w") as f:
        json.dump(name, f)
    global _k_global
    _k_global = k
    retrieve_fn, answer_fn = PIPELINES[pipeline]()
    item = {"question": question, "evidence": []}
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
    console.print(f"\n[bold]Answer[/bold] (generator LLM calls: {n}):\n{reply}")


@app.command()
def eval(
    pipeline: str = typer.Option("lc_naive", "--pipeline", help=f"one of {list(PIPELINES)}"),
    k: int = typer.Option(5, "--k"),
    name: str = typer.Option("", "--name", help="runs/ dir name (default 08_<pipeline>)"),
) -> None:
    """Run the shared evaluator (`evaluate_run`) on the test split through a pipeline."""
    global _k_global
    _k_global = k
    retrieve_fn, answer_fn = PIPELINES[pipeline]()
    run_name = name or f"08_{pipeline}_k{k}"
    evaluate_run(run_name, chapter="08", answer_fn=answer_fn, retrieve_fn=retrieve_fn, split="test")
    with open("data/ch08_config.json", "w") as f:
        json.dump(run_name, f)
    console.print(f"[green]wrote[/green] runs/{run_name}/metrics.json")


if __name__ == "__main__":
    app()
