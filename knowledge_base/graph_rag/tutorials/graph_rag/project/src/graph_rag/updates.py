"""Add, update and remove a document without rebuilding the whole graph (chapter 10).

Chapters 02-09 always processed the *whole* corpus: ingest everything, extract
every chunk, write every chunk, resolve everything, embed everything, detect
communities over the whole graph. That is fine once, but a real corpus grows
document by document, and re-running the full pipeline for one new PDF would
mean re-paying every LLM (Large Language Model) call already cached for the
other documents just to add one more. This module does the minimum work for
one document instead:

  - `add_document(path)` -- ingest -> extract (cache) -> write -> resolve
    (only entities the new chunks touched) -> embed what's missing -> mark
    the communities those entities belong to `stale`.
  - `remove_document(doc_id_or_path)` -- delete the document's chunks, strip
    their ids out of every relationship's `chunk_ids` provenance list, drop
    relationships that provenance now empties out, and delete entities left
    with no remaining `MENTIONS`. This is only possible *because* chapter 05
    stamped every relationship and every entity mention with the chunk id(s)
    that produced it -- without that provenance there would be no way to know
    which piece of the graph came from which document, and "remove a
    document" would mean "rebuild everything except it".
  - `update_document(path)` -- sha256 differs from what's stored -> remove +
    add; identical -> no-op.

Run with: python -m graph_rag.updates add|remove|update <path-or-doc-id>
"""

import time
from datetime import datetime, timezone
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from graph_rag.db import run as run_query
from graph_rag.documents import _doc_id, load_document
from graph_rag.embeddings import embed_chunks, embed_entities
from graph_rag.extraction import cache_path, extract_chunk, load_cached, load_schema, save_cached
from graph_rag.graph_writer import ensure_schema, write_extraction
from graph_rag.ingest import ingest_file
from graph_rag.resolution import _DEFAULT_THRESHOLD, fetch_entities, find_candidates, judge_pairs, merge

app = typer.Typer(add_completion=False)
console = Console()


# --- add -------------------------------------------------------------------


def touched_entities(doc_id: str) -> set[str]:
    """Every `normalized_name` mentioned by at least one chunk of `doc_id`."""
    rows = run_query(
        """
        MATCH (d:Document {id: $doc_id})-[:HAS_CHUNK]->(:Chunk)-[:MENTIONS]->(e:Entity)
        RETURN DISTINCT e.normalized_name AS normalized_name
        """,
        doc_id=doc_id,
    )
    return {r["normalized_name"] for r in rows}


def resolve_touched(touched: set[str], threshold: float = _DEFAULT_THRESHOLD) -> int:
    """Run chapter 06's three-stage candidate search over the whole graph (it
    is cheap, pure Python + one embedding call per un-embedded entity), but
    only judge/merge the pairs that involve at least one of the entities the
    new document actually touched -- a brand new document cannot possibly be
    a duplicate of an existing entity it never mentioned, so there is no
    reason to re-judge the untouched majority of the graph again.
    """
    entities = fetch_entities()
    entity_lookup = {e["normalized_name"]: e for e in entities}
    pairs = [
        p for p in find_candidates(entities, threshold)
        if p.a_norm in touched or p.b_norm in touched
    ]
    if not pairs:
        return 0

    merges_done = 0
    for pair, judgement in judge_pairs(pairs, entity_lookup):
        if judgement.same_entity:
            result = merge(pair.a_norm, pair.b_norm, judgement.canonical_name, pair.method)
            if result is not None:
                merges_done += 1
    return merges_done


def mark_communities_stale(touched: set[str]) -> int:
    """Flag every `Community` a touched entity belongs to as `stale=true`.

    `detect()`/`summarize_communities()` (chapter 09) never look at this flag
    themselves -- it is a signal for a human (or a scheduled job) deciding
    *when* a full community rebuild is worth its cost, not something the
    pipeline enforces automatically. See chapter 10 for the rebuild policy.
    """
    if not touched:
        return 0
    rows = run_query(
        """
        UNWIND $names AS name
        MATCH (:Entity {normalized_name: name})-[:IN_COMMUNITY]->(k:Community)
        SET k.stale = true
        RETURN count(DISTINCT k) AS n
        """,
        names=list(touched),
    )
    return rows[0]["n"]


def add_document(
    path: str | Path, max_tokens: int = 400, overlap: int = 60, threshold: float = _DEFAULT_THRESHOLD
) -> dict:
    """Ingest one file and bring it fully into the graph: lexical layer,
    domain layer, resolution against existing entities, embeddings, and a
    stale marker on any community it touches.
    """
    schema = load_schema()
    doc, chunks = ingest_file(Path(path), max_tokens=max_tokens, overlap=overlap)
    ensure_schema()

    n_extracted = 0
    for chunk in chunks:
        cached = load_cached(chunk.id)
        if cached is None:
            cached = extract_chunk({"id": chunk.id, "text": chunk.text}, schema)
            save_cached(cached)
            n_extracted += 1
        write_extraction(cached)

    n_chunks_embedded = embed_chunks()
    n_entities_embedded = embed_entities()

    touched = touched_entities(doc.id)
    n_merged = resolve_touched(touched, threshold=threshold)
    n_stale_communities = mark_communities_stale(touched)

    return {
        "doc_id": doc.id,
        "title": doc.title,
        "chunks": len(chunks),
        "chunks_extracted": n_extracted,
        "chunk_embeddings_written": n_chunks_embedded,
        "entity_embeddings_written": n_entities_embedded,
        "entities_touched": len(touched),
        "entities_merged": n_merged,
        "communities_marked_stale": n_stale_communities,
    }


# --- remove ------------------------------------------------------------------


def _resolve_doc_id(doc_id_or_path: str) -> str:
    path = Path(doc_id_or_path)
    return _doc_id(path) if path.exists() else doc_id_or_path


def remove_document(doc_id_or_path: str) -> dict:
    """Remove one document and everything that existed only because of it.

    Provenance is what makes this safe: every domain relationship carries
    `chunk_ids` (chapter 05) naming which chunk(s) support it, and every
    entity is reachable from at least one `Chunk` via `MENTIONS`. So instead
    of guessing what a document "contributed", we can compute it exactly:
    strip this document's chunk ids out of every relationship's provenance
    list, drop relationships that provenance now empties out (nothing else
    supports them any more), delete the chunks themselves, then delete any
    entity with no remaining `MENTIONS` at all.
    """
    doc_id = _resolve_doc_id(doc_id_or_path)
    chunk_rows = run_query(
        "MATCH (d:Document {id: $id})-[:HAS_CHUNK]->(c:Chunk) RETURN c.id AS id",
        id=doc_id,
    )
    chunk_ids = [r["id"] for r in chunk_rows]
    if not chunk_ids:
        return {"doc_id": doc_id, "found": False}

    run_query(
        """
        MATCH (:Entity)-[r]->(:Entity)
        WHERE any(cid IN r.chunk_ids WHERE cid IN $chunk_ids)
        SET r.chunk_ids = [cid IN r.chunk_ids WHERE NOT cid IN $chunk_ids]
        """,
        chunk_ids=chunk_ids,
    )

    n_rels_deleted = run_query(
        "MATCH (:Entity)-[r]->(:Entity) WHERE size(r.chunk_ids) = 0 RETURN count(r) AS n"
    )[0]["n"]
    run_query("MATCH (:Entity)-[r]->(:Entity) WHERE size(r.chunk_ids) = 0 DELETE r")

    run_query("MATCH (d:Document {id: $id})-[:HAS_CHUNK]->(c:Chunk) DETACH DELETE c", id=doc_id)
    run_query("MATCH (d:Document {id: $id}) DETACH DELETE d", id=doc_id)

    n_entities_deleted = run_query(
        "MATCH (e:Entity) WHERE NOT (:Chunk)-[:MENTIONS]->(e) RETURN count(e) AS n"
    )[0]["n"]
    run_query("MATCH (e:Entity) WHERE NOT (:Chunk)-[:MENTIONS]->(e) DETACH DELETE e")

    for cid in chunk_ids:
        p = cache_path(cid)
        if p.exists():
            p.unlink()

    return {
        "doc_id": doc_id,
        "found": True,
        "chunks_deleted": len(chunk_ids),
        "relationships_deleted": n_rels_deleted,
        "entities_deleted": n_entities_deleted,
    }


# --- update ------------------------------------------------------------------


def update_document(path: str | Path, threshold: float = _DEFAULT_THRESHOLD) -> dict:
    """sha256 differs from what's stored at this document's id -> remove then
    add; identical -> no-op (the common case: `just pipeline` re-run against
    an unchanged corpus should not redo any work).
    """
    path = Path(path)
    doc = load_document(path)
    existing = run_query("MATCH (d:Document {id: $id}) RETURN d.sha256 AS sha256", id=doc.id)
    if not existing:
        return {"action": "add", **add_document(path, threshold=threshold)}
    if existing[0]["sha256"] == doc.sha256:
        return {"action": "noop", "doc_id": doc.id, "title": doc.title}
    remove_document(doc.id)
    return {"action": "update", **add_document(path, threshold=threshold)}


# --- CLI ---------------------------------------------------------------------


def _print_result(title: str, result: dict) -> None:
    table = Table(title=title)
    table.add_column("metric")
    table.add_column("value")
    for key, value in result.items():
        table.add_row(key, str(value))
    console.print(table)


@app.command()
def add(path: Path, max_tokens: int = 400, overlap: int = 60, threshold: float = _DEFAULT_THRESHOLD) -> None:
    """Ingest, extract, write, resolve and embed one new document."""
    start = time.monotonic()
    result = add_document(path, max_tokens=max_tokens, overlap=overlap, threshold=threshold)
    result["elapsed_s"] = round(time.monotonic() - start, 1)
    _print_result(f"add_document({path})", result)


@app.command()
def remove(doc_id_or_path: str) -> None:
    """Remove a document (by path or by stored doc id) and its orphaned entities."""
    start = time.monotonic()
    result = remove_document(doc_id_or_path)
    result["elapsed_s"] = round(time.monotonic() - start, 1)
    _print_result(f"remove_document({doc_id_or_path})", result)


@app.command()
def update(path: Path, threshold: float = _DEFAULT_THRESHOLD) -> None:
    """Re-sync one document: no-op if unchanged, else remove + add."""
    start = time.monotonic()
    result = update_document(path, threshold=threshold)
    result["elapsed_s"] = round(time.monotonic() - start, 1)
    _print_result(f"update_document({path})", result)


if __name__ == "__main__":
    app()
