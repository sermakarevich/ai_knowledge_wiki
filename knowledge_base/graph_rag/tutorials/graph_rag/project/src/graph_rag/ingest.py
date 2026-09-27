"""Ingest documents into the lexical graph: `Document`, `Chunk`, `HAS_CHUNK`, `NEXT_CHUNK`.

Run with: python -m graph_rag.ingest <path-or-dir> [--max-tokens N] [--overlap N]

Idempotent: re-running on the same files does not create duplicate nodes or
relationships (see `_ensure_constraints` and the `MERGE` queries below). If a
document's content changed (different `sha256` at the same `id`), its old
chunks are deleted first and re-created — chapter 10 refines this into a
proper incremental update that preserves domain-graph provenance.
"""

from pathlib import Path

import typer

from graph_rag.chunking import Chunk, attach_page_numbers, chunk_text
from graph_rag.db import run
from graph_rag.documents import Document, load_document

app = typer.Typer(add_completion=False)

_SUPPORTED_SUFFIXES = {".pdf", ".md", ".txt"}


def _ensure_constraints() -> None:
    run("CREATE CONSTRAINT document_id IF NOT EXISTS FOR (d:Document) REQUIRE d.id IS UNIQUE")
    run("CREATE CONSTRAINT chunk_id IF NOT EXISTS FOR (c:Chunk) REQUIRE c.id IS UNIQUE")


def _existing_sha256(doc_id: str) -> str | None:
    rows = run("MATCH (d:Document {id: $id}) RETURN d.sha256 AS sha256", id=doc_id)
    return rows[0]["sha256"] if rows else None


def _delete_old_chunks(doc_id: str) -> None:
    run(
        "MATCH (d:Document {id: $id})-[:HAS_CHUNK]->(c:Chunk) DETACH DELETE c",
        id=doc_id,
    )


def _write_document(doc: Document) -> None:
    run(
        """
        MERGE (d:Document {id: $id})
        SET d.path = $path, d.title = $title, d.sha256 = $sha256,
            d.ingested_at = datetime()
        """,
        id=doc.id,
        path=doc.path,
        title=doc.title,
        sha256=doc.sha256,
    )


def _write_chunks(doc_id: str, chunks: list[Chunk]) -> None:
    """Write all chunks for one document in a single `UNWIND` batch, then chain
    them with `NEXT_CHUNK` in a second `UNWIND` over consecutive pairs.

    `UNWIND` turns a list parameter into one row per element inside a single
    Cypher query, so one round-trip to Neo4j writes every chunk instead of one
    round-trip per chunk — the difference between ~1 query and ~150 queries
    for this tutorial's PDF.
    """
    rows = [
        {
            "id": c.id,
            "index": c.index,
            "text": c.text,
            "n_tokens": c.n_tokens,
            "page_start": c.page_start,
            "page_end": c.page_end,
        }
        for c in chunks
    ]
    run(
        """
        MATCH (d:Document {id: $doc_id})
        UNWIND $rows AS row
        MERGE (c:Chunk {id: row.id})
        SET c.index = row.index, c.text = row.text, c.n_tokens = row.n_tokens,
            c.page_start = row.page_start, c.page_end = row.page_end
        MERGE (d)-[:HAS_CHUNK]->(c)
        """,
        doc_id=doc_id,
        rows=rows,
    )

    pairs = [{"prev": chunks[i].id, "next": chunks[i + 1].id} for i in range(len(chunks) - 1)]
    if pairs:
        run(
            """
            UNWIND $pairs AS pair
            MATCH (a:Chunk {id: pair.prev}), (b:Chunk {id: pair.next})
            MERGE (a)-[:NEXT_CHUNK]->(b)
            """,
            pairs=pairs,
        )


def ingest_file(path: Path, max_tokens: int = 400, overlap: int = 60) -> tuple[Document, list[Chunk]]:
    doc = load_document(path)
    previous_sha256 = _existing_sha256(doc.id)
    if previous_sha256 is not None and previous_sha256 != doc.sha256:
        _delete_old_chunks(doc.id)

    chunks = chunk_text(doc.id, doc.text, max_tokens=max_tokens, overlap=overlap)
    attach_page_numbers(chunks, doc.text, doc.pages)

    _write_document(doc)
    _write_chunks(doc.id, chunks)
    return doc, chunks


def ingest_path(path: Path, max_tokens: int = 400, overlap: int = 60) -> None:
    _ensure_constraints()
    files = (
        sorted(p for p in path.rglob("*") if p.suffix.lower() in _SUPPORTED_SUFFIXES)
        if path.is_dir()
        else [path]
    )
    for file in files:
        doc, chunks = ingest_file(file, max_tokens=max_tokens, overlap=overlap)
        print(f"{file}: document {doc.id[:8]}… '{doc.title}' -> {len(chunks)} chunks")


@app.command()
def main(
    path: Path = typer.Argument(..., help="A file or a directory of .pdf/.md/.txt files"),
    max_tokens: int = typer.Option(400, help="Max tokens per chunk"),
    overlap: int = typer.Option(60, help="Token overlap between consecutive chunks"),
) -> None:
    ingest_path(path, max_tokens=max_tokens, overlap=overlap)


if __name__ == "__main__":
    app()
