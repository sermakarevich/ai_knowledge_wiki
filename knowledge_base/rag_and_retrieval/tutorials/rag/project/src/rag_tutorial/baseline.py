"""Chapter 03: naive RAG from scratch, no framework.

Fixed-size chunks (`chunkers.fixed_token_chunks`) -> `nomic-embed-text`
embeddings (cached, `rag_tutorial.llm`) -> a Chroma collection
(`stores.ChromaStore`) -> top-k retrieval -> one fixed prompt
(`rag_tutorial.prompts`) -> the shared evaluator (`evaluate.evaluate_run`).
This is the reference pipeline every later chapter's experiment is measured
against.
"""

from __future__ import annotations

import time
from functools import lru_cache

import typer
from rich.console import Console
from rich.table import Table

from rag_tutorial.chunkers import CHUNKERS
from rag_tutorial.corpus import load_papers
from rag_tutorial.evaluate import evaluate_run
from rag_tutorial.golden import load_documents
from rag_tutorial.llm import ollama
from rag_tutorial.prompts import build_messages
from rag_tutorial.schema import Chunk
from rag_tutorial.stores import ChromaStore

app = typer.Typer(add_completion=False)
console = Console()

COLLECTION_NAME = "baseline_fixed_512"


@lru_cache(maxsize=1)
def _short_names() -> dict[str, str]:
    return {paper["id"]: paper["short_name"] for paper in load_papers()}


def _as_triples(chunks: list[Chunk]) -> list[tuple[str, str, str]]:
    short_names = _short_names()
    return [(short_names.get(c.paper, c.paper), c.section, c.text) for c in chunks]


@app.command()
def index(chunker: str = "fixed", size: int = 512, overlap: int = 64) -> None:
    """Chunk all 12 papers, embed with `embed_documents` (cached), write to Chroma."""
    if chunker not in CHUNKERS:
        raise typer.BadParameter(f"chunker must be one of {list(CHUNKERS)}")
    chunk_fn = CHUNKERS[chunker]

    docs = load_documents()
    store = ChromaStore(COLLECTION_NAME)
    store.reset()

    start = time.monotonic()
    all_chunks: list[Chunk] = []
    for doc in docs.values():
        all_chunks.extend(chunk_fn(doc, size=size, overlap=overlap))

    embeddings = ollama.embed_documents([c.text for c in all_chunks])
    store.add(all_chunks, embeddings)
    elapsed = time.monotonic() - start

    console.print(
        f"[green]indexed[/green] {len(all_chunks)} chunks from {len(docs)} papers "
        f"in {elapsed:.1f}s ({store.count()} chunks in {COLLECTION_NAME!r})"
    )


def retrieve(question: str, k: int, store: ChromaStore) -> list[Chunk]:
    """Embed `question` and return the top-`k` chunks (no scores)."""
    query_embedding = ollama.embed_query(question)
    return [chunk for chunk, _score in store.query(query_embedding, k=k)]


def answer(question: str, retrieved: list[Chunk]) -> tuple[str, list[str]]:
    """Build the fixed prompt from `retrieved` chunks and get one chat answer."""
    triples = _as_triples(retrieved)
    messages = build_messages(question, triples)
    reply = ollama.chat(messages, max_tokens=384)
    contexts = [f"[{short_name}] {text}" for short_name, _section, text in triples]
    return reply, contexts


@app.command()
def ask(question: str, k: int = 5) -> None:
    """Embed the question, retrieve top-k, print the retrieved chunks and the cited answer."""
    store = ChromaStore(COLLECTION_NAME)
    query_embedding = ollama.embed_query(question)
    scored = store.query(query_embedding, k=k)

    console.print(f"[bold]Question:[/bold] {question}\n")
    table = Table(title=f"retrieved (k={k})")
    table.add_column("rank", justify="right")
    table.add_column("chunk id")
    table.add_column("paper")
    table.add_column("section")
    table.add_column("score", justify="right")
    for rank, (chunk, score) in enumerate(scored, start=1):
        table.add_row(str(rank), chunk.id, chunk.paper, chunk.section[:60], f"{score:.3f}")
    console.print(table)

    retrieved = [chunk for chunk, _score in scored]
    reply, _contexts = answer(question, retrieved)
    console.print(f"\n[bold]Answer:[/bold]\n{reply}")


def _make_retrieve_fn(k: int, store: ChromaStore):
    def retrieve_fn(item: dict) -> list[Chunk]:
        return retrieve(item["question"], k, store)

    return retrieve_fn


def _answer_fn(item: dict, retrieved: list[Chunk]) -> tuple[str, list[str], int]:
    reply, contexts = answer(item["question"], retrieved)
    return reply, contexts, 1


@app.command(name="eval")
def eval_cmd(name: str = "03_naive_fixed_512_k5", k: int = 5) -> None:
    """Run `evaluate_run` at k, plus the k=3 and k=10 variants when `name` is the k=5 default."""
    store = ChromaStore(COLLECTION_NAME)
    evaluate_run(name, chapter="03", answer_fn=_answer_fn, retrieve_fn=_make_retrieve_fn(k, store))

    if name == "03_naive_fixed_512_k5":
        evaluate_run(
            "03_naive_fixed_512_k3", chapter="03", answer_fn=_answer_fn, retrieve_fn=_make_retrieve_fn(3, store)
        )
        evaluate_run(
            "03_naive_fixed_512_k10", chapter="03", answer_fn=_answer_fn, retrieve_fn=_make_retrieve_fn(10, store)
        )


if __name__ == "__main__":
    app()
