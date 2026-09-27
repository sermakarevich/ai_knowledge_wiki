"""Tests for chapter 02: ingesting data/docs into the lexical graph."""

from pathlib import Path

from graph_rag.db import run
from graph_rag.ingest import ingest_path

_DOCS_DIR = Path(__file__).resolve().parents[1] / "data" / "docs"


def _counts() -> dict:
    return {
        "documents": run("MATCH (d:Document) RETURN count(d) AS n")[0]["n"],
        "chunks": run("MATCH (c:Chunk) RETURN count(c) AS n")[0]["n"],
        "has_chunk": run("MATCH (:Document)-[r:HAS_CHUNK]->() RETURN count(r) AS n")[0]["n"],
        "next_chunk": run("MATCH ()-[r:NEXT_CHUNK]->() RETURN count(r) AS n")[0]["n"],
    }


def test_ingest_creates_lexical_graph():
    ingest_path(_DOCS_DIR)

    documents = run("MATCH (d:Document) RETURN d.id AS id, d.title AS title")
    assert len(documents) == 1
    assert "Survey" in documents[0]["title"]

    chunk_count = run("MATCH (c:Chunk) RETURN count(c) AS n")[0]["n"]
    assert chunk_count > 0

    # Every chunk belongs to exactly one document.
    has_chunk_per_chunk = run(
        """
        MATCH (c:Chunk)
        OPTIONAL MATCH (:Document)-[r:HAS_CHUNK]->(c)
        RETURN c.id AS id, count(r) AS n
        """
    )
    assert all(row["n"] == 1 for row in has_chunk_per_chunk)

    # NEXT_CHUNK forms one chain per document of length chunks - 1.
    next_chunk_count = run("MATCH ()-[r:NEXT_CHUNK]->() RETURN count(r) AS n")[0]["n"]
    assert next_chunk_count == chunk_count - 1


def test_ingest_is_idempotent():
    ingest_path(_DOCS_DIR)
    first = _counts()

    ingest_path(_DOCS_DIR)
    second = _counts()

    assert first == second
