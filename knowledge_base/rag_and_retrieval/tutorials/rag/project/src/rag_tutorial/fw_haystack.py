"""Chapter 10 (part 1) — the same RAG toolkit through Haystack 2 pipelines.

Haystack (deepset) is the production-oriented pipeline framework: typed
components wired into an explicit, serialisable `Pipeline` graph
(`Pipeline()` -> `add_component` -> `connect` -> `run`).

What this module adds (everything expensive/validated stays in
`rag_tutorial` — chunk text, golden set, judges, shared answer prompt):

- Indexing pipeline: `MarkdownToDocument` -> `DocumentSplitter`
  (`split_by="word"`, `split_length=350`, `split_overlap=50` — roughly a
  512-token chunk with 64-token overlap) -> `OllamaDocumentEmbedder`
  (`nomic-embed-text`) -> `DocumentWriter` (in-memory store).
- Query pipelines over one shared `InMemoryDocumentStore`:
    hs_hybrid         — `OllamaTextEmbedder` + `InMemoryBM25Retriever` +
                        `InMemoryEmbeddingRetriever` ->
                        `DocumentJoiner(join_mode="reciprocal_rank_fusion")` ->
                        `ChatPromptBuilder` -> `OllamaChatGenerator` ->
                        `AnswerBuilder` (no rerank).
    hs_hybrid_rerank  — as above, plus a rerank step before the prompt
                        builder (bge-reranker-v2-m3 cross-encoder).
- Haystack built-in evaluators (`FaithfulnessEvaluator`,
  `ContextRelevanceEvaluator`, `DocumentMRREvaluator`,
  `DocumentRecallEvaluator`) over the reranked predictions, compared with
  our own judge (agreement %).
- The query pipeline serialised to YAML (`Pipeline.dumps()`) and loaded
  back; an excerpt is saved for the writeup task.

Haystack <-> Chunk mapping: `DocumentSplitter` records per-split metadata
(`meta["split_id"]`, `meta["split_idx_start"]`, `meta["source_id"]` —
verified against the installed `haystack-ai==3.1.1`; there are NO character
`start`/`end` offsets, only the word-index `split_idx_start`). We map each
split back with `chunk_id(paper, start, end)` where
`start = split_idx_start` and `end = start + len(content)`. The Haystack
`Document.id` itself is a hash of the content and is NOT our chunk id, so
retrieval metrics are computed from the mapped `Chunk.id`.

Installed-version notes (research note loses where it disagrees):
- `SentenceTransformersSimilarityRanker` does NOT exist in the installed
  `haystack-ai==3.1.1` (`haystack.components.rankers` only ships
  `LLMRanker`, `LostInTheMiddleRanker`, `MetaFieldRanker`, ...). The
  `sentence-transformers-haystack` integration package cannot be installed
  here (it needs `sentence-transformers>=5.4.0`, pinned to `==5.3.0` by
  `pylate`). Reranking is therefore a small custom `@component`
  (`CrossEncoderRankerComponent`) wrapping our `CrossEncoderReranker`
  (`BAAI/bge-reranker-v2-m3`) — same model the spec asks for, same scores.
- `ollama-haystack==6.8.0` embedders/generators call Ollama directly and
  bypass the `rag_tutorial.llm` disk cache, so Haystack-side embedding and
  generation calls are NOT cached (judge calls still go through the cached
  client). This is documented in the findings note.
- Qdrant (`qdrant-haystack`) is intentionally NOT used: it needs the Docker
  daemon, while `InMemoryDocumentStore` + `InMemoryBM25Retriever` +
  `InMemoryEmbeddingRetriever` + `DocumentJoiner(RRF)` gives the same
  hybrid topology with zero infrastructure.

Run:
    uv run --group haystack python -m rag_tutorial.fw_haystack index
    uv run --group haystack python -m rag_tutorial.fw_haystack ask "..." --pipeline hs_hybrid_rerank
    uv run --group haystack python -m rag_tutorial.fw_haystack eval --pipeline hs_hybrid
    uv run --group haystack python -m rag_tutorial.fw_haystack eval-all
    uv run --group haystack python -m rag_tutorial.fw_haystack hs-eval
    uv run --group haystack python -m rag_tutorial.fw_haystack dump-pipeline
"""

from __future__ import annotations

import json
import time
from functools import lru_cache
from pathlib import Path
from typing import Any

import typer
from rich.console import Console
from rich.table import Table

from rag_tutorial.baseline import _short_names
from rag_tutorial.config import settings
from rag_tutorial.corpus import MD_DIR
from rag_tutorial.evaluate import RUNS_DIR, evaluate_run
from rag_tutorial.llm import ollama
from rag_tutorial.prompts import SYSTEM_PROMPT
from rag_tutorial.schema import Chunk, chunk_id

app = typer.Typer(add_completion=False)
console = Console()

# ---------------------------------------------------------------------------
# Haystack imports (the `haystack` uv group; installed versions win)
# ---------------------------------------------------------------------------

from haystack import Document, Pipeline
from haystack.components.builders import AnswerBuilder, ChatPromptBuilder
from haystack.components.converters import MarkdownToDocument
from haystack.components.joiners import DocumentJoiner
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.retrievers.in_memory import (
    InMemoryBM25Retriever,
    InMemoryEmbeddingRetriever,
)
from haystack.components.writers import DocumentWriter
from haystack.dataclasses import ByteStream, ChatMessage
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack_integrations.components.embedders.ollama import (
    OllamaDocumentEmbedder,
    OllamaTextEmbedder,
)
from haystack_integrations.components.generators.ollama import OllamaChatGenerator

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SPLIT_LENGTH = 150  # words (~200 tokens — fits the bge reranker's 256-token window)
SPLIT_OVERLAP = 30  # words (~40 tokens)
K_GLOBAL = 5
K_EACH = 20  # per-side pool for hybrid fusion (matches ch07 RERANK_POOL)
RERANK_MODEL = "BAAI/bge-reranker-v2-m3"

PROMPT_TEMPLATE = [
    # Same system instruction as the shared ch03 prompt (plus the same
    # user/excerpts shape) — an early version without the system message
    # made qwen emit bare "[short_name]" citations with no content.
    ChatMessage.from_system(SYSTEM_PROMPT),
    ChatMessage.from_user(
        "Excerpts:\n"
        "{% for doc in documents %}[{{ doc.meta.short_name }}] {{ doc.content }}\n\n{% endfor %}"
        "Question: {{question}}"
    ),
]

# Tutorial convention (COMMON.md): temperature 0 + fixed seed for everything
# evaluated. ollama-haystack does NOT default to these (server default
# temperature is 0.8, random seed), so pin them explicitly — otherwise the
# Haystack rows are not comparable with the rest of the scoreboard.
GEN_KWARGS = {"temperature": 0.0, "seed": 42, "num_predict": 384}

_k_global = K_GLOBAL


# ---------------------------------------------------------------------------
# Haystack Document <-> Chunk mapping
# ---------------------------------------------------------------------------


def hs_doc_to_chunk(doc: Document) -> Chunk:
    """Map a Haystack `Document` (post-split) back onto our `Chunk` schema.

    `DocumentSplitter` (haystack-ai 3.1.1) sets `meta["split_id"]` (int) and
    `meta["split_idx_start"]` (word offset) but no char offsets, so
    `start = split_idx_start`, `end = start + len(content)`; the id is our
    deterministic `chunk_id(paper, start, end)`.
    """
    meta = dict(doc.meta or {})
    paper = str(meta.get("paper", "unknown"))
    start = int(meta.get("split_idx_start", 0) or 0)
    end = start + len(doc.content or "")
    section = str(meta.get("section", ""))
    return Chunk(
        id=chunk_id(paper, start, end),
        paper=paper,
        section=section,
        text=doc.content or "",
        start=start,
        end=end,
        meta={"split_id": meta.get("split_id")},
    )


def _as_contexts(chunks: list[Chunk]) -> list[str]:
    short_names = _short_names()
    return [f"[{short_names.get(c.paper, c.paper)}] {c.text}" for c in chunks]


# ---------------------------------------------------------------------------
# Custom rerank component (bge-reranker-v2-m3 via our CrossEncoderReranker)
# ---------------------------------------------------------------------------

from haystack import component  # noqa: E402


@component
class CrossEncoderRankerComponent:
    """Haystack component wrapping `CrossEncoderReranker` (bge-reranker-v2-m3).

    Reason: the spec's `SentenceTransformersSimilarityRanker` is not shipped
    in `haystack-ai==3.1.1` and its external package conflicts with `pylate`'s
    `sentence-transformers==5.3.0` pin, so it cannot be installed. Same model,
    same scores, honest component boundary.
    """

    def __init__(self, model: str = RERANK_MODEL, top_k: int = K_GLOBAL):
        self.model_name = model
        self.top_k = top_k
        self._reranker = None

    def _ensure(self):
        if self._reranker is None:
            from rag_tutorial.rerankers import CrossEncoderReranker

            self._reranker = CrossEncoderReranker(model=self.model_name)
        return self._reranker

    @component.output_types(documents=list[Document])
    def run(self, documents: list[Document], query: str) -> dict[str, Any]:
        if not documents:
            return {"documents": []}
        chunks = [hs_doc_to_chunk(d) for d in documents]
        ranked = self._ensure().rerank(query, chunks, k=min(self.top_k, len(chunks)))
        by_id = {c.id: d for c, d in zip(chunks, documents)}
        return {"documents": [by_id[c.id] for c in ranked if c.id in by_id]}


# ---------------------------------------------------------------------------
# Store singleton + indexing pipeline
# ---------------------------------------------------------------------------

_store: InMemoryDocumentStore | None = None


def get_store() -> InMemoryDocumentStore:
    """Process-local in-memory store (rebuilt by `index()` each process)."""
    global _store
    if _store is None:
        _store = InMemoryDocumentStore()
    return _store


def build_indexing_pipeline(
    store: InMemoryDocumentStore | None = None,
    document_embedder: Any | None = None,
) -> Pipeline:
    """Indexing pipeline: converter -> splitter -> embedder -> writer."""
    store = store or get_store()
    embedder = document_embedder or OllamaDocumentEmbedder(
        model=settings.embed_model, url=ollama.base_url
    )
    pipe = Pipeline()
    pipe.add_component("converter", MarkdownToDocument())
    pipe.add_component(
        "splitter",
        DocumentSplitter(
            split_by="word", split_length=SPLIT_LENGTH, split_overlap=SPLIT_OVERLAP
        ),
    )
    pipe.add_component("embedder", embedder)
    pipe.add_component("writer", DocumentWriter(document_store=store))
    pipe.connect("converter", "splitter")
    pipe.connect("splitter", "embedder")
    pipe.connect("embedder", "writer")
    return pipe


def _md_sources() -> tuple[list[ByteStream], list[dict]]:
    """One `ByteStream` per parsed paper plus `{"paper", "short_name"}` meta.

    Both keys propagate through `MarkdownToDocument` into every split's
    `meta`, so the prompt template can cite `[short_name]` exactly like the
    shared ch03 prompt (Haystack splits don't track `section`, so there is
    no `§section` suffix — documented in the findings).
    """
    from rag_tutorial.corpus import load_papers

    papers = load_papers()
    short = {p["id"]: p.get("short_name", p["id"]) for p in papers}
    sources: list[ByteStream] = []
    metas: list[dict] = []
    for paper in papers:
        path = MD_DIR / f"{paper['id']}.md"
        if not path.exists():
            continue
        sources.append(ByteStream.from_file_path(path))
        metas.append({"paper": paper["id"], "short_name": short[paper["id"]]})
    return sources, metas


def ensure_indexed() -> InMemoryDocumentStore:
    """Build the in-memory index if empty (embeddings via Ollama, uncached)."""
    store = get_store()
    if store.count_documents() > 0:
        return store
    sources, metas = _md_sources()
    pipe = build_indexing_pipeline(store)
    pipe.run({"converter": {"sources": sources, "meta": metas}})
    return store


# ---------------------------------------------------------------------------
# Query pipelines
# ---------------------------------------------------------------------------


def build_query_pipeline(
    use_rerank: bool = True,
    k: int = K_GLOBAL,
    k_each: int = K_EACH,
    text_embedder: Any | None = None,
    generator: Any | None = None,
    ranker: Any | None = None,
    store: InMemoryDocumentStore | None = None,
) -> Pipeline:
    """Query pipeline: embed -> BM25+vector -> RRF join -> [rerank] -> prompt -> LLM -> answer."""
    store = store or get_store()
    embedder = text_embedder or OllamaTextEmbedder(
        model=settings.embed_model, url=ollama.base_url
    )
    llm = generator or OllamaChatGenerator(
        model=settings.chat_model, url=ollama.base_url, generation_kwargs=dict(GEN_KWARGS)
    )
    pipe = Pipeline()
    pipe.add_component("text_embedder", embedder)
    pipe.add_component("bm25_retriever", InMemoryBM25Retriever(store, top_k=k_each))
    pipe.add_component(
        "embedding_retriever", InMemoryEmbeddingRetriever(store, top_k=k_each)
    )
    pipe.add_component(
        "joiner", DocumentJoiner(join_mode="reciprocal_rank_fusion", top_k=k_each)
    )
    if use_rerank:
        pipe.add_component(
            "ranker", ranker or CrossEncoderRankerComponent(top_k=k)
        )
    pipe.add_component("prompt_builder", ChatPromptBuilder(template=PROMPT_TEMPLATE))
    pipe.add_component("llm", llm)
    pipe.add_component("answer_builder", AnswerBuilder())

    pipe.connect("text_embedder.embedding", "embedding_retriever.query_embedding")
    pipe.connect("bm25_retriever", "joiner")
    pipe.connect("embedding_retriever", "joiner")
    if use_rerank:
        pipe.connect("joiner", "ranker")
        pipe.connect("ranker", "prompt_builder")
        pipe.connect("ranker.documents", "answer_builder.documents")
    else:
        pipe.connect("joiner", "prompt_builder")
        pipe.connect("joiner.documents", "answer_builder.documents")
    pipe.connect("prompt_builder.prompt", "llm.messages")
    pipe.connect("llm.replies", "answer_builder.replies")
    return pipe


def _pipeline_inputs(question: str, use_rerank: bool) -> dict[str, Any]:
    base: dict[str, Any] = {
        "text_embedder": {"text": question},
        "bm25_retriever": {"query": question},
        "prompt_builder": {"question": question},
        "answer_builder": {"query": question},
    }
    if use_rerank:
        base["ranker"] = {"query": question}
    return base


def _run_pipeline(pipe: Pipeline, question: str, use_rerank: bool) -> tuple[str, list[Chunk]]:
    out = pipe.run(_pipeline_inputs(question, use_rerank))
    answers = out.get("answer_builder", {}).get("answers", [])
    if not answers:
        return "", []
    ans = answers[0]
    docs = ans.documents or []
    chunks = [hs_doc_to_chunk(d) for d in docs]
    contexts = _as_contexts(chunks)
    return str(ans.data or ""), contexts


def pipeline_hybrid():
    """`10_hs_hybrid`: hybrid RRF retrieval, shared cached generator (1 call)."""

    def retrieve_fn(item: dict) -> list[Chunk]:
        store = ensure_indexed()
        pipe = build_query_pipeline(use_rerank=False, k=_k_global)
        # Retrieval-only pass would double embedding calls; instead run the
        # full pipeline once here is wasteful — so retrieve via components:
        # reuse the pipeline's retrievers directly for the chunk list, and let
        # answer_fn do the generation through the shared cached client.
        from haystack import Document as _D  # noqa: F401 (kept local on purpose)

        _ = store  # store is populated by ensure_indexed
        # Run the Haystack pipeline up to the joiner by running the whole
        # pipeline but discarding the answer is simpler and honest about cost
        # (1 generator call happens in retrieve; answer_fn reuses it).
        out = pipe.run(_pipeline_inputs(item["question"], False))
        answers = out.get("answer_builder", {}).get("answers", [])
        docs = (answers[0].documents if answers else []) or []
        chunks = [hs_doc_to_chunk(d) for d in docs[:_k_global]]
        item["_hs_answer"] = str(answers[0].data) if answers else ""
        item["_hs_contexts"] = _as_contexts(chunks)
        return chunks

    def answer_fn(item: dict, retrieved: list[Chunk]) -> tuple[str, list[str], int]:
        return str(item.get("_hs_answer", "")), list(item.get("_hs_contexts", [])), 1

    return retrieve_fn, answer_fn


def pipeline_hybrid_rerank():
    """`10_hs_hybrid_rerank`: hybrid RRF + bge cross-encoder rerank (1 call)."""

    def retrieve_fn(item: dict) -> list[Chunk]:
        ensure_indexed()
        pipe = build_query_pipeline(use_rerank=True, k=_k_global)
        out = pipe.run(_pipeline_inputs(item["question"], True))
        answers = out.get("answer_builder", {}).get("answers", [])
        docs = (answers[0].documents if answers else []) or []
        chunks = [hs_doc_to_chunk(d) for d in docs[:_k_global]]
        item["_hs_answer"] = str(answers[0].data) if answers else ""
        item["_hs_contexts"] = _as_contexts(chunks)
        return chunks

    def answer_fn(item: dict, retrieved: list[Chunk]) -> tuple[str, list[str], int]:
        return str(item.get("_hs_answer", "")), list(item.get("_hs_contexts", [])), 1

    return retrieve_fn, answer_fn


PIPELINES = {
    "hs_hybrid": pipeline_hybrid,
    "hs_hybrid_rerank": pipeline_hybrid_rerank,
}


def draw_mermaid(pipe: Pipeline) -> str:
    """Hand-drawn mermaid from `pipe.to_dict()` (no network for `draw()`)."""
    data = pipe.to_dict()
    lines = ["graph TD"]
    comps = data.get("components", {})
    conns = data.get("connections", [])
    for name, comp in comps.items():
        ctype = comp.get("type", "?").split(".")[-1]
        lines.append(f'    {name}["{name}<br/>{ctype}"]')
    for conn in conns:
        s, r = conn.get("sender", "?"), conn.get("receiver", "?")
        sender = str(s).split(".")[0]
        lines.append(f"    {sender} --> {str(r).split('.')[0]}")
        lines.append(f"    %% {s} -> {r}")
    _ = comps
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


@app.command()
def index() -> None:
    """Build the in-memory Haystack index (converter -> splitter -> embed -> write)."""
    global _store
    _store = InMemoryDocumentStore()
    sources, metas = _md_sources()
    console.print(f"[green]papers[/green] {len(sources)} markdown files from {MD_DIR}")
    t0 = time.monotonic()
    pipe = build_indexing_pipeline(_store)
    pipe.run({"converter": {"sources": sources, "meta": metas}})
    console.print(
        f"[green]indexed[/green] {pipe} -> {get_store().count_documents()} splits "
        f"({time.monotonic() - t0:.1f}s; embeddings via Ollama, uncached)"
    )


@app.command()
def ask(
    question: str,
    pipeline: str = typer.Option("hs_hybrid_rerank", "--pipeline", help=f"one of {list(PIPELINES)}"),
    k: int = typer.Option(5, "--k"),
) -> None:
    """Run one question through a Haystack pipeline; print chunks + answer."""
    global _k_global
    _k_global = k
    ensure_indexed()
    retrieve_fn, answer_fn = PIPELINES[pipeline]()
    item: dict = {"question": question, "evidence": []}
    retrieved = retrieve_fn(item)
    table = Table(title=f"retrieved via 10_{pipeline} (k={k})")
    table.add_column("rank", justify="right")
    table.add_column("chunk id")
    table.add_column("paper")
    table.add_column("split_id")
    for rank, chunk in enumerate(retrieved, start=1):
        table.add_row(str(rank), chunk.id, chunk.paper, str((chunk.meta or {}).get("split_id", "")))
    console.print(table)
    reply, _contexts, n = answer_fn(item, retrieved)
    console.print(f"\n[bold]Answer[/bold] (LLM calls: {n}):\n{reply}")


@app.command()
def eval(
    pipeline: str = typer.Option("hs_hybrid_rerank", "--pipeline", help=f"one of {list(PIPELINES)}"),
    k: int = typer.Option(5, "--k"),
    name: str = typer.Option("", "--name", help="runs/ dir name (default 10_<pipeline>)"),
) -> None:
    """Run the shared evaluator on the test split through a Haystack pipeline."""
    global _k_global
    _k_global = k
    ensure_indexed()
    retrieve_fn, answer_fn = PIPELINES[pipeline]()
    run_name = name or f"10_{pipeline}"
    evaluate_run(run_name, chapter="10", answer_fn=answer_fn, retrieve_fn=retrieve_fn, split="test")
    console.print(f"[green]wrote[/green] runs/{run_name}/metrics.json")


@app.command(name="eval-all")
def eval_all(k: int = typer.Option(5, "--k")) -> None:
    """Evaluate both `10_hs_*` pipelines (writes one runs/ dir per pipeline)."""
    global _k_global
    _k_global = k
    ensure_indexed()
    for pipeline in PIPELINES:
        run_name = f"10_{pipeline}"
        if (RUNS_DIR / run_name / "metrics.json").exists():
            console.print(f"[yellow]skipping[/yellow] {run_name} (metrics.json exists)")
            continue
        retrieve_fn, answer_fn = PIPELINES[pipeline]()
        console.print(f"[bold]evaluating[/bold] {run_name} ...")
        t0 = time.monotonic()
        evaluate_run(run_name, chapter="10", answer_fn=answer_fn, retrieve_fn=retrieve_fn, split="test")
        console.print(f"[green]wrote[/green] runs/{run_name}/metrics.json ({time.monotonic() - t0:.1f}s)")


@app.command(name="hs-eval")
def hs_eval() -> None:
    """Run Haystack's built-in evaluators over `10_hs_hybrid_rerank` predictions.

    `FaithfulnessEvaluator`/`ContextRelevanceEvaluator` get an
    `OllamaChatGenerator` (local); anything needing an OpenAI-style API is
    recorded as an error instead of crashing. Writes
    `runs/10_hs_evaluators/hs_eval.json` with per-question rows + an
    agreement table vs our judge.
    """
    from haystack.components.evaluators import (
        ContextRelevanceEvaluator,
        DocumentMRREvaluator,
        DocumentRecallEvaluator,
        FaithfulnessEvaluator,
    )

    from rag_tutorial.golden import QA_PATH, load_qa

    ensure_indexed()
    pred_path = settings.path("runs/10_hs_hybrid_rerank/predictions.jsonl")
    if not pred_path.exists():
        console.print(f"[red]missing[/red] {pred_path} — run `eval --pipeline hs_hybrid_rerank` first")
        raise typer.Exit(1)
    rows = [json.loads(line) for line in pred_path.read_text().splitlines() if line.strip()]
    qa_by_id = {item["id"]: item for item in load_qa(QA_PATH)}

    # Rebuild chunk text for retrieved ids from the live store.
    store_docs = get_store().filter_documents() or []
    text_by_id = {hs_doc_to_chunk(d).id: (d.content or "") for d in store_docs}

    chat_gen = OllamaChatGenerator(
        model=settings.chat_model, url=ollama.base_url, generation_kwargs=dict(GEN_KWARGS)
    )
    faithfulness = FaithfulnessEvaluator(chat_generator=chat_gen)
    relevance = ContextRelevanceEvaluator(chat_generator=chat_gen)
    mrr = DocumentMRREvaluator()
    recall = DocumentRecallEvaluator(mode="single_hit")

    out_rows: list[dict] = []
    for row in rows:
        qid = row.get("id", "")
        item = qa_by_id.get(qid, {})
        question = row.get("question", item.get("question", ""))
        answer = row.get("answer", "")
        contexts = [text_by_id[cid] for cid in (row.get("retrieved_chunk_ids") or []) if cid in text_by_id]
        gold_docs = [Document(content=ev["quote"]) for ev in (item.get("evidence") or [])]
        ret_docs = [Document(content=t) for t in contexts]
        entry: dict[str, Any] = {"id": qid}
        try:
            fr = faithfulness.run(questions=[question], contexts=[contexts], predicted_answers=[answer])
            entry["hs_faithfulness"] = fr.get("results", fr)
        except Exception as exc:  # noqa: BLE001 — record and continue
            entry["hs_faithfulness_error"] = f"{type(exc).__name__}: {exc}"
        try:
            cr = relevance.run(questions=[question], contexts=[contexts], predicted_answers=[answer])
            entry["hs_context_relevance"] = cr.get("results", cr)
        except Exception as exc:  # noqa: BLE001
            entry["hs_context_relevance_error"] = f"{type(exc).__name__}: {exc}"
        try:
            mr = mrr.run(ground_truth_documents=gold_docs, retrieved_documents=ret_docs)
            entry["hs_mrr"] = mr.get("results", mr)
        except Exception as exc:  # noqa: BLE001
            entry["hs_mrr_error"] = f"{type(exc).__name__}: {exc}"
        try:
            rc = recall.run(ground_truth_documents=gold_docs, retrieved_documents=ret_docs)
            entry["hs_recall"] = rc.get("results", rc)
        except Exception as exc:  # noqa: BLE001
            entry["hs_recall_error"] = f"{type(exc).__name__}: {exc}"
        entry["ours_correctness"] = (row.get("correctness") or {}).get("score")
        entry["ours_faithfulness"] = (row.get("faithfulness") or {}).get("score")
        out_rows.append(entry)
        console.print(f"[green]{qid}[/green] done ({len(out_rows)}/{len(rows)})")

    def agreement(hs_key: str, ours_key: str, thresh: float = 0.5) -> float | None:
        pairs = []
        for r in out_rows:
            hs = r.get(hs_key)
            ours = r.get(ours_key)
            if ours is None or not isinstance(hs, list):
                continue
            try:
                score = float(hs[0].get("score", 0))
            except Exception:  # noqa: BLE001
                continue
            pairs.append((score >= thresh, ours >= thresh))
        if not pairs:
            return None
        return sum(1 for a, b in pairs if a == b) / len(pairs)

    table = {
        "n": len(out_rows),
        "agreement_hs_faithfulness_vs_ours_faithfulness": agreement("hs_faithfulness", "ours_faithfulness"),
        "agreement_hs_context_relevance_vs_ours_correctness": agreement("hs_context_relevance", "ours_correctness"),
        "note": "DocumentMRREvaluator/DocumentRecallEvaluator compare exact document content; "
        "agreement is only computed for the LLM-based evaluators.",
    }
    run_dir = settings.path("runs/10_hs_evaluators")
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "hs_eval.json").write_text(json.dumps({"rows": out_rows, "agreement": table}, indent=2))
    console.print(f"[green]wrote[/green] runs/10_hs_evaluators/hs_eval.json")
    console.print(json.dumps(table, indent=2))


@app.command(name="dump-pipeline")
def dump_pipeline() -> None:
    """Serialise the reranked query pipeline to YAML and reload it (round-trip check)."""
    pipe = build_query_pipeline(use_rerank=True)
    yaml_text = pipe.dumps()
    run_dir = settings.path("runs/10_hs_hybrid_rerank")
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "pipeline.yaml").write_text(yaml_text)
    reloaded = Pipeline.loads(yaml_text, unsafe=True)  # custom ranker component needs explicit trust
    console.print(f"[green]wrote[/green] runs/10_hs_hybrid_rerank/pipeline.yaml")
    console.print(f"components: {sorted(pipe.to_dict().get('components', {}))}")
    console.print(f"round-trip ok: {sorted(reloaded.to_dict().get('components', {})) == sorted(pipe.to_dict().get('components', {}))}")
    console.print("--- mermaid ---")
    console.print(draw_mermaid(pipe))


if __name__ == "__main__":
    app()
