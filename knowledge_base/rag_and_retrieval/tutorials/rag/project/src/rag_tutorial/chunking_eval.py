"""Chapter 04: index the corpus with every chunking strategy, evaluate each with
the same dense top-5 retriever and the same frozen baseline prompt
(`prompts.build_messages`) chapter 03 used — so a scoreboard difference is
attributable to chunking alone, not to a different retriever or prompt.

`just chunking-eval` runs every experiment named in `04_chunking.md`:
`04_fixed_256`, `04_fixed_1024`, `04_fixed_512_ov128`, `04_recursive_512`,
`04_sentence_5`, `04_markdown_512`, `04_semantic`, `04_parent_child`,
`04_sentence_window`, `04_contextual_512`. `04_fixed_512` is *not* re-run here
— it is identical to chapter 03's `03_naive_fixed_512_k5` baseline, so that
run's numbers are reused directly on the scoreboard.
"""

from __future__ import annotations

import json
import statistics
import time
from functools import lru_cache

import typer
from rich.console import Console

from rag_tutorial.chunkers import (
    contextual_chunks,
    fixed_token_chunks,
    markdown_chunks,
    parent_child_chunks,
    parent_chunks,
    recursive_chunks,
    semantic_chunks,
    sentence_chunks,
    sentence_window_chunks,
)
from rag_tutorial.config import settings
from rag_tutorial.corpus import load_papers
from rag_tutorial.evaluate import evaluate_run
from rag_tutorial.golden import _first_abstract, load_documents
from rag_tutorial.gpu import wait_for_gpu
from rag_tutorial.llm import count_tokens, ollama
from rag_tutorial.prompts import build_messages
from rag_tutorial.retrievers import DenseRetriever, ParentChildRetriever, SentenceWindowRetriever
from rag_tutorial.schema import Chunk, Document
from rag_tutorial.stores import ChromaStore

app = typer.Typer(add_completion=False)
console = Console()

K = 5
CHUNK_STATS_PATH = settings.path("runs/04_chunk_stats.json")


@lru_cache(maxsize=1)
def _short_names() -> dict[str, str]:
    return {paper["id"]: paper["short_name"] for paper in load_papers()}


def _as_triples(chunks: list[Chunk]) -> list[tuple[str, str, str]]:
    short_names = _short_names()
    return [(short_names.get(c.paper, c.paper), c.section, c.text) for c in chunks]


def answer(question: str, retrieved: list[Chunk]) -> tuple[str, list[str]]:
    """Identical to `baseline.answer` — same prompt, same triples shape — so a
    scoreboard difference between chapters 03 and 04 is only ever the chunker."""
    triples = _as_triples(retrieved)
    messages = build_messages(question, triples)
    reply = ollama.chat(messages, max_tokens=384)
    contexts = [f"[{short_name}] {text}" for short_name, _section, text in triples]
    return reply, contexts


def _answer_fn(item: dict, retrieved: list[Chunk]) -> tuple[str, list[str], int]:
    reply, contexts = answer(item["question"], retrieved)
    return reply, contexts, 1


def _chunk_stats(name: str, chunks: list[Chunk], seconds: float) -> dict:
    token_counts = [count_tokens(c.text) for c in chunks]
    return {
        "experiment": name,
        "n_chunks": len(chunks),
        "mean_tokens": round(statistics.fmean(token_counts), 1) if token_counts else 0,
        "median_tokens": statistics.median(token_counts) if token_counts else 0,
        "index_seconds": round(seconds, 1),
    }


def _index_and_eval(name: str, chunks: list[Chunk], retriever_factory, seconds_so_far: float) -> dict:
    """Embed+store `chunks`, build the retriever via `retriever_factory(store)`, run
    `evaluate_run`, and return this experiment's `04_chunk_stats.json` row."""
    store = ChromaStore(f"ch04_{name}")
    store.reset()
    embeddings = ollama.embed_documents([c.text for c in chunks])
    store.add(chunks, embeddings)
    elapsed = time.monotonic() - seconds_so_far

    retriever = retriever_factory(store)
    evaluate_run(name, chapter="04", answer_fn=_answer_fn, retrieve_fn=lambda item: retriever.retrieve(item["question"]))
    console.print(f"[green]done[/green] {name}: {len(chunks)} chunks, {elapsed:.1f}s indexing")
    return _chunk_stats(name, chunks, elapsed)


# -- one builder per experiment --------------------------------------------------------


def run_fixed(name: str, docs: dict[str, Document], size: int, overlap: int) -> dict:
    start = time.monotonic()
    chunks = [c for doc in docs.values() for c in fixed_token_chunks(doc, size=size, overlap=overlap)]
    return _index_and_eval(name, chunks, lambda store: DenseRetriever(store, k=K), start)


def run_recursive(name: str, docs: dict[str, Document], size: int, overlap: int) -> dict:
    start = time.monotonic()
    chunks = [c for doc in docs.values() for c in recursive_chunks(doc, size=size, overlap=overlap)]
    return _index_and_eval(name, chunks, lambda store: DenseRetriever(store, k=K), start)


def run_sentence(name: str, docs: dict[str, Document], n_sentences: int, overlap: int) -> dict:
    start = time.monotonic()
    chunks = [c for doc in docs.values() for c in sentence_chunks(doc, n_sentences=n_sentences, overlap=overlap)]
    return _index_and_eval(name, chunks, lambda store: DenseRetriever(store, k=K), start)


def run_markdown(name: str, docs: dict[str, Document], size: int, overlap: int) -> dict:
    start = time.monotonic()
    chunks = [c for doc in docs.values() for c in markdown_chunks(doc, size=size, overlap=overlap)]
    return _index_and_eval(name, chunks, lambda store: DenseRetriever(store, k=K), start)


def run_semantic(name: str, docs: dict[str, Document], percentile: float) -> dict:
    start = time.monotonic()
    chunks = [c for doc in docs.values() for c in semantic_chunks(doc, ollama, percentile=percentile)]
    return _index_and_eval(name, chunks, lambda store: DenseRetriever(store, k=K), start)


def run_parent_child(
    name: str,
    docs: dict[str, Document],
    parent_size: int,
    parent_overlap: int,
    child_size: int,
    child_overlap: int,
) -> dict:
    start = time.monotonic()
    parents: dict[str, Chunk] = {}
    children: list[Chunk] = []
    child_to_parent: dict[str, str] = {}
    for doc in docs.values():
        for parent in parent_chunks(doc, size=parent_size, overlap=parent_overlap):
            parents[parent.id] = parent
        doc_children = parent_child_chunks(
            doc, parent_size=parent_size, parent_overlap=parent_overlap, child_size=child_size, child_overlap=child_overlap
        )
        children.extend(doc_children)
        for child in doc_children:
            child_to_parent[child.id] = child.meta["parent_id"]

    def _factory(store: ChromaStore) -> ParentChildRetriever:
        return ParentChildRetriever(store, child_to_parent, parents, k=K)

    return _index_and_eval(name, children, _factory, start)


def run_sentence_window(name: str, docs: dict[str, Document], window: int) -> dict:
    start = time.monotonic()
    chunks = [c for doc in docs.values() for c in sentence_window_chunks(doc, window=window)]
    return _index_and_eval(name, chunks, lambda store: SentenceWindowRetriever(store, docs, k=K, window=window), start)


def run_contextual(name: str, docs: dict[str, Document], size: int, overlap: int) -> dict:
    """~600-900 LLM calls (one per markdown chunk) — cached, so a second run of
    this experiment costs zero calls. Politeness-checks the shared GPU first."""
    wait_for_gpu()
    abstracts = {paper_id: _first_abstract(doc.text) for paper_id, doc in docs.items()}
    start = time.monotonic()
    chunks: list[Chunk] = []
    for paper_id, doc in docs.items():
        chunks.extend(contextual_chunks(doc, ollama, abstracts[paper_id], size=size, overlap=overlap))
    return _index_and_eval(name, chunks, lambda store: DenseRetriever(store, k=K), start)


EXPERIMENTS = {
    "04_fixed_256": lambda docs: run_fixed("04_fixed_256", docs, size=256, overlap=64),
    "04_fixed_1024": lambda docs: run_fixed("04_fixed_1024", docs, size=1024, overlap=64),
    "04_fixed_512_ov128": lambda docs: run_fixed("04_fixed_512_ov128", docs, size=512, overlap=128),
    "04_recursive_512": lambda docs: run_recursive("04_recursive_512", docs, size=512, overlap=64),
    "04_sentence_5": lambda docs: run_sentence("04_sentence_5", docs, n_sentences=5, overlap=1),
    "04_markdown_512": lambda docs: run_markdown("04_markdown_512", docs, size=512, overlap=64),
    "04_semantic": lambda docs: run_semantic("04_semantic", docs, percentile=20),
    "04_parent_child": lambda docs: run_parent_child(
        "04_parent_child", docs, parent_size=800, parent_overlap=100, child_size=160, child_overlap=32
    ),
    "04_sentence_window": lambda docs: run_sentence_window("04_sentence_window", docs, window=3),
    "04_contextual_512": lambda docs: run_contextual("04_contextual_512", docs, size=512, overlap=64),
}

# 04_fixed_512 is identical to chapter 03's baseline (size=512, overlap=64, dense
# top-5, same prompt) — reused rather than re-run; see 04_chunking.md.
REUSED_FROM_CHAPTER_03 = {"04_fixed_512": "03_naive_fixed_512_k5"}


@app.command(name="run-all")
def run_all(only: list[str] = typer.Option(None, help="run only these experiment names (default: all)")) -> None:
    """Run every chapter-04 chunking experiment and write `runs/04_chunk_stats.json`."""
    docs = load_documents()
    names = only or list(EXPERIMENTS)
    stats = []
    existing = json.loads(CHUNK_STATS_PATH.read_text()) if CHUNK_STATS_PATH.exists() else []
    stats_by_name = {row["experiment"]: row for row in existing}

    for name in names:
        if name not in EXPERIMENTS:
            raise typer.BadParameter(f"unknown experiment {name!r}, choose from {list(EXPERIMENTS)}")
        console.print(f"[bold]running[/bold] {name}")
        stats_by_name[name] = EXPERIMENTS[name](docs)
        stats = list(stats_by_name.values())
        CHUNK_STATS_PATH.parent.mkdir(parents=True, exist_ok=True)
        CHUNK_STATS_PATH.write_text(json.dumps(stats, indent=2))

    console.print(f"[green]wrote[/green] {CHUNK_STATS_PATH} ({len(stats)} rows)")


if __name__ == "__main__":
    app()
