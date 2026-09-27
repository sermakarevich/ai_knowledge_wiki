"""Chapter 05: dense vs BM25 vs hybrid (RRF/weighted), MMR, metadata filtering
and Qdrant native hybrid — all on top of chapter 04's best chunking strategy,
`parent_child` (parent 800/100 tokens, child 160/32 tokens), so a scoreboard
difference from here on is attributable to the *retriever* alone.

`just retrieval-eval` runs the 8 named experiments (`05_dense_k5`, `05_bm25_k5`,
`05_hybrid_rrf_k5`, `05_hybrid_weighted_k5`, `05_hybrid_rrf_k10`,
`05_dense_mmr_k5`, `05_hybrid_rrf_filtered_k5`, `05_qdrant_native_hybrid_k5`)
through the same `evaluate_run` chapters 02-04 used, plus a retrieval-only
k-sweep (k in 1/3/5/10/20, no generation, no judge calls — cheap) written to
`runs/05_retrieval_sweep.json` and plotted to `runs/05_retrieval_sweep.png`.
"""

from __future__ import annotations

import json
import statistics
import time

import typer
from rich.console import Console

from rag_tutorial.chunkers import parent_child_chunks, parent_chunks
from rag_tutorial.config import settings
from rag_tutorial.corpus import load_papers
from rag_tutorial.evaluate import evaluate_run, retrieval_metrics
from rag_tutorial.golden import QA_PATH, _first_abstract, load_documents, load_qa
from rag_tutorial.llm import ollama
from rag_tutorial.prompts import build_messages
from rag_tutorial.retrievers import (
    BM25Retriever,
    DenseRetriever,
    HybridRetriever,
    MMRRetriever,
    ParentChildRetriever,
    QdrantHybridRetriever,
)
from rag_tutorial.schema import Chunk, Document
from rag_tutorial.stores import ChromaStore, QdrantStore

app = typer.Typer(add_completion=False)
console = Console()

PARENT_SIZE, PARENT_OVERLAP = 800, 100
CHILD_SIZE, CHILD_OVERLAP = 160, 32

CHROMA_COLLECTION = "ch05_parent_child_children"
BM25_NAME = "05_parent_child_children"
QDRANT_COLLECTION = "ch05_parent_child_children"

SWEEP_KS = (1, 3, 5, 10, 20)
SWEEP_PATH = settings.path("runs/05_retrieval_sweep.json")
SWEEP_PLOT_PATH = settings.path("runs/05_retrieval_sweep.png")


def _short_names() -> dict[str, str]:
    return {paper["id"]: paper["short_name"] for paper in load_papers()}


def build_parent_child_index(docs: dict[str, Document]) -> tuple[list[Chunk], dict[str, Chunk], dict[str, str]]:
    """Build the children (indexed) and parents (returned) for chapter 05's fixed
    chunking. Identical parameters to chapter 04's `04_parent_child`."""
    parents: dict[str, Chunk] = {}
    children: list[Chunk] = []
    child_to_parent: dict[str, str] = {}
    for doc in docs.values():
        for parent in parent_chunks(doc, size=PARENT_SIZE, overlap=PARENT_OVERLAP):
            parents[parent.id] = parent
        doc_children = parent_child_chunks(
            doc, parent_size=PARENT_SIZE, parent_overlap=PARENT_OVERLAP, child_size=CHILD_SIZE, child_overlap=CHILD_OVERLAP
        )
        children.extend(doc_children)
        for child in doc_children:
            child_to_parent[child.id] = child.meta["parent_id"]
    return children, parents, child_to_parent


def answer(question: str, retrieved: list[Chunk]) -> tuple[str, list[str]]:
    """Same prompt, same triples shape as chapters 03/04 — a scoreboard
    difference is only ever the retriever."""
    short_names = _short_names()
    triples = [(short_names.get(c.paper, c.paper), c.section, c.text) for c in retrieved]
    messages = build_messages(question, triples)
    reply = ollama.chat(messages, max_tokens=384)
    contexts = [f"[{short_name}] {text}" for short_name, _section, text in triples]
    return reply, contexts


def _answer_fn(item: dict, retrieved: list[Chunk]) -> tuple[str, list[str], int]:
    reply, contexts = answer(item["question"], retrieved)
    return reply, contexts, 1


class _Indexes:
    """Lazily-built Chroma/BM25/Qdrant indexes over the fixed parent_child
    children, shared by every chapter-05 experiment so we chunk/embed the
    corpus exactly once per run of `run-all`."""

    def __init__(self, rebuild: bool = False):
        self.rebuild = rebuild
        self.docs = load_documents()
        self.children, self.parents, self.child_to_parent = build_parent_child_index(self.docs)
        self.papers = load_papers()

        self.chroma = ChromaStore(CHROMA_COLLECTION)
        if rebuild or self.chroma.count() != len(self.children):
            self.chroma.reset()
            embeddings = ollama.embed_documents([c.text for c in self.children])
            self.chroma.add(self.children, embeddings)

        self._bm25_index = BM25Retriever.from_chunks(BM25_NAME, self.children, rebuild=rebuild)

    def dense(self, k: int = 5, fetch_multiplier: int = 4) -> ParentChildRetriever:
        return ParentChildRetriever(self.chroma, self.child_to_parent, self.parents, k=k, fetch_multiplier=fetch_multiplier)

    def dense_raw(self, k: int = 5) -> DenseRetriever:
        """Dense retriever over the raw child index (no parent swap) — used as
        the `dense` half of `HybridRetriever`/`MMRRetriever`, which do the swap
        themselves after fusing/re-selecting at the child level."""
        return DenseRetriever(self.chroma, k=k)

    def bm25(self, k: int = 5, with_parent_swap: bool = True) -> BM25Retriever:
        return self._bm25_index.clone(k=k, child_to_parent=self.child_to_parent if with_parent_swap else None, parents=self.parents if with_parent_swap else None)

    def qdrant(self, rebuild: bool = False) -> QdrantStore:
        store = QdrantStore(QDRANT_COLLECTION)
        exists = store.client.collection_exists(QDRANT_COLLECTION)
        needs_build = rebuild or not exists or store.client.count(QDRANT_COLLECTION, exact=True).count != len(self.children)
        if needs_build:
            store.reset()
            embeddings = ollama.embed_documents([c.text for c in self.children])
            store.add(self.children, embeddings)
        return store


# -- one builder per experiment --------------------------------------------------------


def run_dense_k(name: str, idx: _Indexes, k: int) -> dict:
    retriever = idx.dense(k=k)
    return evaluate_run(name, chapter="05", answer_fn=_answer_fn, retrieve_fn=lambda item: retriever.retrieve(item["question"]))


def run_bm25_k(name: str, idx: _Indexes, k: int) -> dict:
    retriever = idx.bm25(k=k)
    return evaluate_run(name, chapter="05", answer_fn=_answer_fn, retrieve_fn=lambda item: retriever.retrieve(item["question"]))


def run_hybrid(name: str, idx: _Indexes, k: int, fusion: str, router: bool = False) -> dict:
    dense = idx.dense_raw(k=20)
    sparse = idx.bm25(k=20, with_parent_swap=False)
    retriever = HybridRetriever(
        dense,
        sparse,
        fusion=fusion,
        k=k,
        k_each=20,
        child_to_parent=idx.child_to_parent,
        parents=idx.parents,
        router=router,
        papers=idx.papers,
    )
    metrics = evaluate_run(name, chapter="05", answer_fn=_answer_fn, retrieve_fn=lambda item: retriever.retrieve(item["question"]))
    if router:
        metrics["details"]["router_calls"] = retriever.router_calls
        metrics["details"]["router_fired"] = retriever.router_fired
        (settings.path("runs") / name / "metrics.json").write_text(json.dumps(metrics, indent=2))
    return metrics


def run_mmr(name: str, idx: _Indexes, k: int, lambda_mult: float = 0.7) -> dict:
    dense = idx.dense_raw(k=20)
    retriever = MMRRetriever(dense, k=k, fetch_k=20, lambda_mult=lambda_mult, child_to_parent=idx.child_to_parent, parents=idx.parents)
    return evaluate_run(name, chapter="05", answer_fn=_answer_fn, retrieve_fn=lambda item: retriever.retrieve(item["question"]))


def run_qdrant_native(name: str, idx: _Indexes, k: int) -> dict:
    store = idx.qdrant()
    retriever = QdrantHybridRetriever(store, k=k, k_each=20, child_to_parent=idx.child_to_parent, parents=idx.parents)
    metrics = evaluate_run(name, chapter="05", answer_fn=_answer_fn, retrieve_fn=lambda item: retriever.retrieve(item["question"]))
    metrics["details"]["query_points_seconds"] = retriever.last_seconds
    (settings.path("runs") / name / "metrics.json").write_text(json.dumps(metrics, indent=2))
    return metrics


EXPERIMENTS = {
    "05_dense_k5": lambda idx: run_dense_k("05_dense_k5", idx, k=5),
    "05_bm25_k5": lambda idx: run_bm25_k("05_bm25_k5", idx, k=5),
    "05_hybrid_rrf_k5": lambda idx: run_hybrid("05_hybrid_rrf_k5", idx, k=5, fusion="rrf"),
    "05_hybrid_weighted_k5": lambda idx: run_hybrid("05_hybrid_weighted_k5", idx, k=5, fusion="weighted"),
    "05_hybrid_rrf_k10": lambda idx: run_hybrid("05_hybrid_rrf_k10", idx, k=10, fusion="rrf"),
    "05_dense_mmr_k5": lambda idx: run_mmr("05_dense_mmr_k5", idx, k=5),
    "05_hybrid_rrf_filtered_k5": lambda idx: run_hybrid("05_hybrid_rrf_filtered_k5", idx, k=5, fusion="rrf", router=True),
    "05_qdrant_native_hybrid_k5": lambda idx: run_qdrant_native("05_qdrant_native_hybrid_k5", idx, k=5),
}


@app.command(name="run-all")
def run_all(only: list[str] = typer.Option(None, help="run only these experiment names (default: all)"), rebuild: bool = False) -> None:
    """Run every chapter-05 retrieval experiment (writes runs/<name>/metrics.json each)."""
    idx = _Indexes(rebuild=rebuild)
    names = only or list(EXPERIMENTS)
    for name in names:
        if name not in EXPERIMENTS:
            raise typer.BadParameter(f"unknown experiment {name!r}, choose from {list(EXPERIMENTS)}")
        console.print(f"[bold]running[/bold] {name}")
        EXPERIMENTS[name](idx)
        console.print(f"[green]done[/green] {name}")


# -- retrieval-only k-sweep (cheap: no generation, no judge) ----------------------------


def _retrieval_only(name: str, retrieve_fn, items: list[dict], ks: tuple[int, ...]) -> dict:
    rows = []
    seconds = []
    for item in items:
        if not item["evidence"]:
            continue
        start = time.monotonic()
        retrieved = retrieve_fn(item, max(ks))
        seconds.append(time.monotonic() - start)
        rows.append(retrieval_metrics(retrieved, item["evidence"], ks=ks, ndcg_ks=ks))

    def _mean(key: str) -> float:
        return statistics.fmean(r[key] for r in rows) if rows else 0.0

    result = {"name": name, "n_questions": len(rows), "mean_seconds": round(statistics.fmean(seconds), 4) if seconds else 0.0}
    for k in ks:
        result[f"hit@{k}"] = round(_mean(f"hit@{k}"), 4)
        result[f"recall@{k}"] = round(_mean(f"recall@{k}"), 4)
        result[f"ndcg@{k}"] = round(_mean(f"ndcg@{k}"), 4)
    result["mrr"] = round(_mean("mrr"), 4)
    return result


@app.command()
def sweep(rebuild: bool = False) -> None:
    """Retrieval-only k-sweep (k in 1/3/5/10/20) for dense/bm25/hybrid-rrf: hit,
    recall, MRR, nDCG — no generation, no judge calls. Writes
    `runs/05_retrieval_sweep.json` and a recall@k plot `runs/05_retrieval_sweep.png`.
    """
    idx = _Indexes(rebuild=rebuild)
    items = [item for item in load_qa(QA_PATH) if item["split"] == "test"]

    def _dense_fetch(item: dict, k: int) -> list[Chunk]:
        return idx.dense(k=k).retrieve(item["question"])

    def _bm25_fetch(item: dict, k: int) -> list[Chunk]:
        return idx.bm25(k=k).retrieve(item["question"])

    def _hybrid_fetch(item: dict, k: int) -> list[Chunk]:
        dense = idx.dense_raw(k=20)
        sparse = idx.bm25(k=20, with_parent_swap=False)
        retriever = HybridRetriever(dense, sparse, fusion="rrf", k=k, k_each=20, child_to_parent=idx.child_to_parent, parents=idx.parents)
        return retriever.retrieve(item["question"])

    rows = [
        _retrieval_only("dense", _dense_fetch, items, SWEEP_KS),
        _retrieval_only("bm25", _bm25_fetch, items, SWEEP_KS),
        _retrieval_only("hybrid_rrf", _hybrid_fetch, items, SWEEP_KS),
    ]
    SWEEP_PATH.parent.mkdir(parents=True, exist_ok=True)
    SWEEP_PATH.write_text(json.dumps(rows, indent=2))
    console.print(f"[green]wrote[/green] {SWEEP_PATH}")

    _plot_sweep(rows)
    console.print(f"[green]wrote[/green] {SWEEP_PLOT_PATH}")


def _plot_sweep(rows: list[dict]) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6, 4))
    for row in rows:
        ys = [row[f"recall@{k}"] for k in SWEEP_KS]
        ax.plot(SWEEP_KS, ys, marker="o", label=row["name"])
    ax.set_xlabel("k")
    ax.set_ylabel("recall@k")
    ax.set_title("Chapter 05: recall@k, dense vs BM25 vs hybrid (RRF)")
    ax.set_xticks(list(SWEEP_KS))
    ax.legend()
    fig.tight_layout()
    SWEEP_PLOT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(SWEEP_PLOT_PATH, dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    app()
