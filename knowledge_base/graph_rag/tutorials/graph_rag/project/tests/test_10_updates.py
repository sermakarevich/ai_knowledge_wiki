"""Tests for chapter 10: incremental updates (add/remove one document).

Integration only, needs Docker Neo4j up (`just up`). The chapter's real `just
add path="data/docs_extra/graphrag_local_to_global_2404.16130.pdf"` run
already populated `data/extracted/chunks/*.json` (extraction) and
`data/extracted/resolution/*.json` (entity-resolution judgements) for this
exact file, so re-running `add_document`/`remove_document` here hits those
caches and makes zero LLM (Large Language Model) calls.
"""

from pathlib import Path

from graph_rag.db import run as run_query
from graph_rag.updates import add_document, remove_document

_EXTRA_PDF = Path("data/docs_extra/graphrag_local_to_global_2404.16130.pdf")


def _counts() -> dict:
    return {
        "documents": run_query("MATCH (d:Document) RETURN count(d) AS n")[0]["n"],
        "chunks": run_query("MATCH (c:Chunk) RETURN count(c) AS n")[0]["n"],
        "entities": run_query("MATCH (e:Entity) RETURN count(e) AS n")[0]["n"],
        "relationships": run_query(
            "MATCH (:Entity)-[r]->(:Entity) WHERE type(r) <> 'MENTIONS' RETURN count(r) AS n"
        )[0]["n"],
    }


def test_add_then_remove_restores_counts():
    before = _counts()

    add_result = add_document(_EXTRA_PDF)
    assert add_result["chunks"] > 0
    after_add = _counts()
    assert after_add["documents"] == before["documents"] + 1
    assert after_add["chunks"] > before["chunks"]
    assert after_add["entities"] >= before["entities"]

    remove_result = remove_document(str(_EXTRA_PDF))
    assert remove_result["found"] is True
    assert remove_result["chunks_deleted"] == add_result["chunks"]

    after_remove = _counts()
    # documents/chunks/entities are provably exact: provenance (chunk_ids on every
    # relationship, MENTIONS on every entity) guarantees nothing the new document didn't
    # add survives its removal.
    assert after_remove["documents"] == before["documents"]
    assert after_remove["chunks"] == before["chunks"]
    assert after_remove["entities"] == before["entities"]
    # relationships is not: entity-resolution's LLM judge can merge two extracted
    # relationships into one (or not) depending on which entity survives a merge, so two
    # otherwise-identical add+remove cycles can restore a slightly different relationship
    # count (see chapter 10's "Cost & latency" section for real, observed drifts of 1-8
    # across repeated runs against ~40 merges) -- assert it stays in the same ballpark
    # (well under the ~41 entities `add_document` merges each run), not byte-identical.
    assert abs(after_remove["relationships"] - before["relationships"]) <= 30


def test_remove_missing_document_reports_not_found():
    result = remove_document("this-path-does-not-exist.pdf")
    assert result["found"] is False
