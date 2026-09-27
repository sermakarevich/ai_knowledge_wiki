"""Tests for chapter 05: writing cached extractions into the running Neo4j.

These tests wipe the domain layer (`Entity` nodes only, keeps Document/Chunk)
and rewrite it from `data/extracted/chunks/*.json`, so they need Docker Neo4j
up (`just up`) but never call the LLM.
"""

from graph_rag.db import run as run_query
from graph_rag.graph_writer import ensure_schema, wipe_domain, write_all


def _counts() -> tuple[int, int]:
    nodes = run_query("MATCH (n:Entity) RETURN count(n) AS n")[0]["n"]
    rels = run_query("MATCH ()-[r]->() RETURN count(r) AS n")[0]["n"]
    return nodes, rels


def setup_module() -> None:
    ensure_schema()
    wipe_domain()
    write_all()


def test_every_entity_has_at_least_two_labels():
    rows = run_query("MATCH (n:Entity) RETURN labels(n) AS labels LIMIT 2000")
    assert rows, "expected Entity nodes after write_all()"
    assert all(len(row["labels"]) >= 2 for row in rows)


def test_mentions_count_is_at_least_entity_count():
    n_entities = run_query("MATCH (n:Entity) RETURN count(n) AS n")[0]["n"]
    n_mentions = run_query("MATCH (:Chunk)-[m:MENTIONS]->(:Entity) RETURN count(m) AS n")[0]["n"]
    assert n_mentions >= n_entities


def test_no_relationship_without_chunk_ids():
    rows = run_query(
        "MATCH (:Entity)-[r]->(:Entity) WHERE r.chunk_ids IS NULL RETURN count(r) AS n"
    )
    assert rows[0]["n"] == 0


def test_writing_twice_leaves_counts_unchanged():
    before = _counts()
    write_all()
    after = _counts()
    assert before == after
