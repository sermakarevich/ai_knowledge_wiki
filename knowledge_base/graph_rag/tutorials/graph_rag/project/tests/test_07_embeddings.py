"""Tests for chapter 07: embeddings and vector/full-text indexes.

Integration only, needs Docker Neo4j up (`just up`). `test_05_graph_writer`'s
`setup_module` wipes and rewrites `Entity` nodes from the on-disk extraction
cache (no embeddings) every time the full suite runs, and file order in a
pytest session follows this file's name (`test_05_...` before
`test_07_...`), so this module cannot assume chapter 06/07's `just
resolve`/`just embed` state survived -- it re-runs `embed_chunks` /
`embed_entities` / `ensure_indexes` itself in `setup_module`, the same
"ensure my own precondition" pattern `test_05_graph_writer.py` uses.
"""

from graph_rag.db import run as run_query
from graph_rag.embeddings import embed_chunks, embed_entities, ensure_indexes, search_chunks


def setup_module() -> None:
    embed_chunks()
    embed_entities()
    ensure_indexes()


def test_no_chunk_missing_embedding():
    rows = run_query("MATCH (c:Chunk) WHERE c.embedding IS NULL RETURN count(c) AS n")
    assert rows[0]["n"] == 0


def test_no_entity_missing_embedding():
    rows = run_query("MATCH (e:Entity) WHERE e.embedding IS NULL RETURN count(e) AS n")
    assert rows[0]["n"] == 0


def test_vector_indexes_are_online():
    rows = run_query(
        "SHOW INDEXES YIELD name, state, type WHERE name IN ['chunk_embedding', 'entity_embedding'] "
        "RETURN name, state, type"
    )
    states = {r["name"]: r for r in rows}
    assert set(states) == {"chunk_embedding", "entity_embedding"}
    for row in states.values():
        assert row["state"] == "ONLINE"
        assert row["type"] == "VECTOR"


def test_fulltext_indexes_are_online():
    rows = run_query(
        "SHOW INDEXES YIELD name, state, type WHERE name IN ['chunk_text', 'entity_names'] "
        "RETURN name, state, type"
    )
    states = {r["name"]: r for r in rows}
    assert set(states) == {"chunk_text", "entity_names"}
    for row in states.values():
        assert row["state"] == "ONLINE"
        assert row["type"] == "FULLTEXT"


def test_search_chunks_returns_relevant_results():
    rows = search_chunks("Leiden community detection", 3)
    assert len(rows) == 3
    for row in rows:
        assert row["score"] > 0.5
