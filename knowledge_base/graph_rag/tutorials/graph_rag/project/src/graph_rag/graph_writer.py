"""Write cached extractions (chapter 04) into Neo4j: the domain graph.

Chapter 04 produced one JSON file per chunk under `data/extracted/chunks/`,
each holding entities and relationships that fit the frozen schema. This
module is the only place that turns those files into graph nodes and
relationships. It never calls the LLM (Large Language Model) -- everything
here is deterministic Cypher, safe to re-run as many times as we like.

Run with: python -m graph_rag.graph_writer write|stats [--limit N] [--wipe-domain]
"""

from pathlib import Path

import typer
from neo4j import ManagedTransaction
from rich.console import Console
from rich.table import Table

from graph_rag.db import get_driver, run as run_query
from graph_rag.extraction import ChunkExtraction

app = typer.Typer(add_completion=False)
console = Console()

_CHUNKS_DIR = Path("data/extracted/chunks")


# --- schema ------------------------------------------------------------------


def ensure_schema() -> None:
    """Constraints and indexes for the domain graph.

    `Entity.normalized_name` is the one uniqueness constraint: it is the
    single MERGE key every entity write goes through (see `write_extraction`
    below), so exactly one node exists per normalised name, whatever type the
    LLM assigned it this time. We deliberately do NOT use the composite key
    `(type, normalized_name)`: chapter 04 shows the LLM's `type` field is
    noisy chunk-to-chunk (the same real-world thing can come back as `Method`
    in one chunk and `Other` in another), so keying on `(type, name)` would
    silently create two nodes for one entity every time the type flips --
    exactly the duplicate-node bug chapter 02 warned about. Keying on
    `normalized_name` alone means the *first* type seen wins (`ON CREATE`)
    and later chunks only add evidence (description, aliases, properties),
    which is the more common failure to have (a stale/first type) than
    duplicate entities.
    """
    run_query("CREATE CONSTRAINT entity_normalized_name IF NOT EXISTS "
               "FOR (n:Entity) REQUIRE n.normalized_name IS UNIQUE")
    run_query("CREATE INDEX entity_name IF NOT EXISTS FOR (n:Entity) ON (n.name)")
    run_query("CREATE INDEX entity_type IF NOT EXISTS FOR (n:Entity) ON (n.type)")
    # Same constraint name as chapter 02's ingest.py -- IF NOT EXISTS only
    # no-ops when both name AND definition match, so this stays idempotent
    # instead of erroring on "already exists with a different name".
    run_query("CREATE CONSTRAINT chunk_id IF NOT EXISTS FOR (c:Chunk) REQUIRE c.id IS UNIQUE")


# --- Cypher --------------------------------------------------------------
#
# Dynamic labels/types: classic Cypher parses labels and relationship types
# as literal tokens at query-parse time, so `SET n:$type` (a bare parameter
# as a label) has always been a syntax error -- there was no way to compute
# a label at runtime without either string-building the query (a Cypher
# injection risk) or calling an APOC procedure such as
# `apoc.create.addLabels(n, [e.type])` / `apoc.merge.relationship(...)`,
# which take the label/type as an ordinary string argument instead. Neo4j
# 5.26 added dynamic label/type *expressions*: `SET n:$(e.type)` and
# `MERGE (a)-[r:$(r.type)]->(b)` evaluate the parenthesised expression to a
# name at runtime, parameters and all -- no string-building needed. Both
# ways are used on this server (Neo4j 5.26.29); `_ENTITY_LABEL_QUERY_APOC`
# is kept only to show the older idiom in the tutorial text.

_ENTITY_QUERY = """
UNWIND $entities AS e
MERGE (n:Entity {normalized_name: e.normalized_name})
ON CREATE SET n.name = e.name, n.created_at = datetime()
SET n.type = coalesce(n.type, e.type),
    n.description = CASE
        WHEN size(e.description) > size(coalesce(n.description, '')) THEN e.description
        ELSE n.description
    END,
    n.aliases = apoc.coll.toSet(coalesce(n.aliases, []) + e.name),
    n += e.properties
SET n:$(e.type)
"""

# The APOC equivalent of the last line above -- works the same, but the
# label argument is an ordinary string/list, not a parsed expression:
#   CALL apoc.create.addLabels(n, [e.type]) YIELD node RETURN node

_MENTIONS_QUERY = """
UNWIND $entities AS e
MATCH (c:Chunk {id: $chunk_id})
MATCH (n:Entity {normalized_name: e.normalized_name})
MERGE (c)-[m:MENTIONS]->(n)
SET m.description = e.description
"""

_RELATIONSHIPS_QUERY = """
UNWIND $relationships AS r
MATCH (a:Entity {normalized_name: r.source_norm}), (b:Entity {normalized_name: r.target_norm})
MERGE (a)-[rel:$(r.type)]->(b)
ON CREATE SET rel.weight = r.weight, rel.chunk_ids = [$chunk_id]
ON MATCH SET rel.weight = (rel.weight + r.weight) / 2,
             rel.chunk_ids = CASE
                 WHEN $chunk_id IN rel.chunk_ids THEN rel.chunk_ids
                 ELSE rel.chunk_ids + $chunk_id
             END
SET rel.description = coalesce(rel.description, r.description),
    rel += r.properties
"""


def _entity_rows(ext: ChunkExtraction) -> list[dict]:
    return [
        {
            "name": e.name,
            "type": e.type,
            "normalized_name": e.normalized_name,
            "description": e.description,
            "properties": e.properties,
        }
        for e in ext.entities
    ]


def _relationship_rows(ext: ChunkExtraction) -> list[dict]:
    return [
        {
            "source_norm": r.source,  # normalize() already rewrote source/target to normalized_name
            "target_norm": r.target,
            "type": r.type,
            "weight": r.weight,
            "description": r.description,
            "properties": r.properties,
        }
        for r in ext.relationships
    ]


def _write_extraction_tx(tx: ManagedTransaction, ext: ChunkExtraction) -> dict:
    """Everything for one chunk in a single transaction: entities, provenance,
    relationships. One chunk's extraction is one unit of work -- either all
    of it lands, or (on error) none of it does, so a crash mid-chunk never
    leaves a chunk half-written into the graph.
    """
    counters = {"nodes_created": 0, "properties_set": 0, "relationships_created": 0, "labels_added": 0}

    entities = _entity_rows(ext)
    if entities:
        summary = tx.run(_ENTITY_QUERY, entities=entities).consume()
        for key in counters:
            counters[key] += getattr(summary.counters, key, 0)

        summary = tx.run(_MENTIONS_QUERY, entities=entities, chunk_id=ext.chunk_id).consume()
        for key in counters:
            counters[key] += getattr(summary.counters, key, 0)

    relationships = _relationship_rows(ext)
    if relationships:
        summary = tx.run(_RELATIONSHIPS_QUERY, relationships=relationships, chunk_id=ext.chunk_id).consume()
        for key in counters:
            counters[key] += getattr(summary.counters, key, 0)

    return counters


def write_extraction(ext: ChunkExtraction) -> dict:
    with get_driver() as driver:
        with driver.session(database="neo4j") as session:
            return session.execute_write(_write_extraction_tx, ext)


# --- domain wipe ---------------------------------------------------------


def wipe_domain() -> None:
    """Delete only `Entity` nodes (and everything attached to them):
    `MENTIONS` relationships and all domain relationships between entities.
    `Document` and `Chunk` (the lexical layer, chapter 02) are untouched --
    they came from parsing the PDF, not from the LLM, so there is never a
    reason to redo them just because we want to replay the domain graph
    from a fresh extraction or a schema change. The two layers are only
    connected one-way, `Chunk -[:MENTIONS]-> Entity`, so deleting `Entity`
    nodes cannot orphan or corrupt the lexical layer.
    """
    run_query("MATCH (n:Entity) DETACH DELETE n")


# --- write_all / stats -----------------------------------------------------


def load_cached_from_path(path: Path) -> ChunkExtraction:
    return ChunkExtraction.model_validate_json(path.read_text())


def write_all(cache_dir: Path = _CHUNKS_DIR, limit: int | None = None) -> Table:
    ensure_schema()
    paths = sorted(cache_dir.glob("*.json"))
    if limit is not None:
        paths = paths[:limit]
    if not paths:
        raise typer.Exit("No cached extractions found -- run `just extract` first (see chapter 04).")

    totals = {"nodes_created": 0, "properties_set": 0, "relationships_created": 0, "labels_added": 0}
    labels_seen: set[str] = set()
    for path in paths:
        ext = load_cached_from_path(path)
        counters = write_extraction(ext)
        for key in totals:
            totals[key] += counters[key]
        labels_seen.update(e.type for e in ext.entities)

    table = Table(title=f"Graph write summary ({len(paths)} chunk(s))")
    table.add_column("metric")
    table.add_column("value")
    table.add_row("chunks written", str(len(paths)))
    table.add_row("nodes created", str(totals["nodes_created"]))
    table.add_row("relationships created", str(totals["relationships_created"]))
    table.add_row("labels added", str(totals["labels_added"]))
    table.add_row("properties set", str(totals["properties_set"]))
    table.add_row("entity types seen", ", ".join(sorted(labels_seen)))
    return table


_LABEL_COUNTS_QUERY = """
MATCH (n) UNWIND labels(n) AS label
RETURN label, count(*) AS n ORDER BY n DESC
"""

_REL_COUNTS_QUERY = """
MATCH ()-[r]->() RETURN type(r) AS rel_type, count(*) AS n ORDER BY n DESC
"""

_LABEL_REL_LABEL_QUERY = """
MATCH (a)-[r]->(b)
RETURN labels(a) AS from, type(r) AS rel, labels(b) AS to, count(*) AS n
ORDER BY n DESC
"""


def stats() -> tuple[Table, Table, Table]:
    label_table = Table(title="Node counts per label")
    label_table.add_column("label")
    label_table.add_column("count")
    for row in run_query(_LABEL_COUNTS_QUERY):
        label_table.add_row(row["label"], str(row["n"]))

    rel_table = Table(title="Relationship type counts")
    rel_table.add_column("type")
    rel_table.add_column("count")
    for row in run_query(_REL_COUNTS_QUERY):
        rel_table.add_row(row["rel_type"], str(row["n"]))

    shape_table = Table(title="label -[REL]-> label")
    shape_table.add_column("from")
    shape_table.add_column("rel")
    shape_table.add_column("to")
    shape_table.add_column("count")
    for row in run_query(_LABEL_REL_LABEL_QUERY):
        shape_table.add_row(str(row["from"]), row["rel"], str(row["to"]), str(row["n"]))

    return label_table, rel_table, shape_table


# --- CLI ---------------------------------------------------------------------


@app.command()
def write(
    limit: int | None = None,
    wipe_domain_first: bool = typer.Option(False, "--wipe-domain", help="Delete all Entity nodes first"),
) -> None:
    """Write every cached extraction into Neo4j (chapter 05)."""
    if wipe_domain_first:
        console.print("[yellow]--wipe-domain: deleting all Entity nodes first[/yellow]")
        wipe_domain()
    ensure_schema()
    table = write_all(limit=limit)
    console.print(table)


@app.command(name="stats")
def stats_cmd() -> None:
    """Print label counts, relationship type counts and the label->REL->label table."""
    label_table, rel_table, shape_table = stats()
    console.print(label_table)
    console.print(rel_table)
    console.print(shape_table)


if __name__ == "__main__":
    app()
