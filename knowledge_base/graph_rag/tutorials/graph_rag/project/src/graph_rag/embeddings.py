"""Embeddings and vector/full-text search (chapter 07).

Chapters 02-06 built a lexical graph (`Document`/`Chunk`) and a resolved
domain graph (`Entity`). Neither is searchable by a natural-language
question yet -- a Cypher `MATCH` needs an exact string, not "how does X
work?". This module:

  1. `embed_chunks` / `embed_entities` -- embed `Chunk.text` and
     `Entity.name + ": " + description` with `llm.embed`, writing vectors
     back with `db.create.setNodeVectorProperty` (see why below).
  2. `ensure_indexes` -- create two Neo4j vector indexes (`chunk_embedding`,
     `entity_embedding`) and two full-text indexes (`chunk_text`,
     `entity_names`), and wait until `SHOW INDEXES` reports them ONLINE.
  3. `search_chunks` / `search_entities` / `search_fulltext` -- single-mode
     retrieval.
  4. `hybrid_search_entities` -- Reciprocal Rank Fusion (RRF) of the vector
     and full-text entity lists, used by chapter 08's retrieval pipeline.

Run with: python -m graph_rag.embeddings run|search "<question>" [--mode chunks|entities|fulltext|hybrid]
"""

import typer
from rich.console import Console
from rich.table import Table

from graph_rag.db import run as run_query
from graph_rag.llm import embed

app = typer.Typer(add_completion=False)
console = Console()

_EMBED_BATCH_SIZE = 32
_RRF_K = 60  # standard RRF damping constant: rank 1 in either list scores 1/61, not 1/1


# --- embedding ----------------------------------------------------------


def embed_chunks(batch: int = _EMBED_BATCH_SIZE, only_missing: bool = True) -> int:
    """Embed `Chunk.text` for chunks missing `Chunk.embedding` (or every
    chunk if `only_missing=False`), writing vectors back in batches so a
    re-run only pays for what's still missing -- the same "cache as you go"
    pattern chapter 06 uses for `Entity.embedding`.
    """
    where = "WHERE c.embedding IS NULL" if only_missing else ""
    rows = run_query(f"MATCH (c:Chunk) {where} RETURN c.id AS id, c.text AS text ORDER BY c.id")
    return _embed_and_set(rows, label="Chunk", key_prop="id", batch=batch)


def embed_entities(batch: int = _EMBED_BATCH_SIZE, only_missing: bool = True) -> int:
    """Embed `name + ': ' + description` for entities missing
    `Entity.embedding`. Chapter 06 already embedded most entities this same
    way during resolution (stage 2), so a normal run here finds almost
    nothing left to do -- only entities created or renamed since then.
    """
    where = "WHERE e.embedding IS NULL" if only_missing else ""
    rows = run_query(
        f"MATCH (e:Entity) {where} "
        "RETURN e.normalized_name AS id, (e.name + ': ' + coalesce(e.description, '')) AS text "
        "ORDER BY e.normalized_name"
    )
    return _embed_and_set(rows, label="Entity", key_prop="normalized_name", batch=batch)


def _embed_and_set(rows: list[dict], label: str, key_prop: str, batch: int) -> int:
    if not rows:
        return 0
    for i in range(0, len(rows), batch):
        chunk = rows[i : i + batch]
        vectors = embed([r["text"] for r in chunk])
        # `db.create.setNodeVectorProperty` (not plain `SET n.embedding = $vec`)
        # converts the incoming list to Neo4j's native FLOAT[] vector encoding
        # and validates it is a flat numeric array. A plain `SET` stores
        # whatever Cypher type the driver sent (Python floats can arrive as a
        # mix of int/float, or as a Python list the driver encodes as
        # LIST<ANY>), which the vector index silently refuses to use at query
        # time. The procedure is also the only supported way to update a
        # vector-indexed property incrementally without a full index rebuild.
        run_query(
            f"""
            UNWIND $rows AS row
            MATCH (n:{label} {{{key_prop}: row.key}})
            CALL db.create.setNodeVectorProperty(n, 'embedding', row.vec)
            """,
            rows=[{"key": r["id"], "vec": v} for r, v in zip(chunk, vectors)],
        )
    return len(rows)


# --- indexes --------------------------------------------------------------

_VECTOR_INDEXES = {
    "chunk_embedding": "Chunk",
    "entity_embedding": "Entity",
}
_FULLTEXT_INDEXES = {
    "chunk_text": ("Chunk", ["text"]),
    "entity_names": ("Entity", ["name", "aliases", "description"]),
}


def ensure_indexes(embed_dim: int = 768, timeout_s: float = 60.0) -> None:
    """Create the vector and full-text indexes used by search, then block
    until `SHOW INDEXES` reports every one of them ONLINE. Index creation
    returns immediately; the actual population (reading every existing
    node's vector/text into the index structure) happens in the background,
    so a query issued right after `CREATE INDEX` can silently miss rows or
    fail outright until the index is ONLINE.
    """
    for name, label in _VECTOR_INDEXES.items():
        run_query(
            f"""
            CREATE VECTOR INDEX {name} IF NOT EXISTS
            FOR (n:{label}) ON (n.embedding)
            OPTIONS {{indexConfig: {{
                `vector.dimensions`: $dim,
                `vector.similarity_function`: 'cosine'
            }}}}
            """,
            dim=embed_dim,
        )
    for name, (label, props) in _FULLTEXT_INDEXES.items():
        prop_list = ", ".join(f"n.{p}" for p in props)
        run_query(f"CREATE FULLTEXT INDEX {name} IF NOT EXISTS FOR (n:{label}) ON EACH [{prop_list}]")

    all_names = list(_VECTOR_INDEXES) + list(_FULLTEXT_INDEXES)
    import time

    deadline = time.monotonic() + timeout_s
    while True:
        rows = run_query(
            "SHOW INDEXES YIELD name, state WHERE name IN $names RETURN name, state", names=all_names
        )
        states = {r["name"]: r["state"] for r in rows}
        if len(states) == len(all_names) and all(s == "ONLINE" for s in states.values()):
            return
        if time.monotonic() > deadline:
            raise TimeoutError(f"indexes not ONLINE after {timeout_s}s: {states}")
        time.sleep(0.5)


# --- search ---------------------------------------------------------------


def search_chunks(question: str, k: int = 5) -> list[dict]:
    """Vector search over `Chunk.embedding`. Embeds `question` once, then
    `db.index.vector.queryNodes` does an approximate nearest-neighbour scan
    over the `chunk_embedding` index and returns the top-`k` chunks with a
    cosine-similarity `score` in [0, 1] (higher is more similar).
    """
    vector = embed([question])[0]
    return run_query(
        """
        CALL db.index.vector.queryNodes('chunk_embedding', $k, $vector)
        YIELD node, score
        RETURN node.id AS id, node.text AS text, score
        ORDER BY score DESC
        """,
        k=k, vector=vector,
    )


def search_entities(question: str, k: int = 10) -> list[dict]:
    """Vector search over `Entity.embedding`, same mechanics as `search_chunks`."""
    vector = embed([question])[0]
    return run_query(
        """
        CALL db.index.vector.queryNodes('entity_embedding', $k, $vector)
        YIELD node, score
        RETURN node.normalized_name AS normalized_name, node.name AS name, node.type AS type, score
        ORDER BY score DESC
        """,
        k=k, vector=vector,
    )


def search_fulltext(question: str, k: int = 10) -> list[dict]:
    """Lucene full-text search over `entity_names` (`name`, `aliases`,
    `description`). Unlike vector search this needs no embedding call, and
    it is the only mode that finds a match via an *alias* string chapter 06
    carried through a merge (e.g. "G-Indexing") even when the question's
    wording never appears in `description`.
    """
    return run_query(
        """
        CALL db.index.fulltext.queryNodes('entity_names', $question) YIELD node, score
        RETURN node.normalized_name AS normalized_name, node.name AS name, node.type AS type, score
        ORDER BY score DESC LIMIT $k
        """,
        question=question, k=k,
    )


def hybrid_search_entities(question: str, k: int = 10) -> list[dict]:
    """Reciprocal Rank Fusion (RRF) of `search_entities` (vector) and
    `search_fulltext` (Lucene) over entities. RRF combines two ranked lists
    without needing their scores to be on the same scale -- a cosine
    similarity and a Lucene TF-IDF score are not comparable numbers, but
    their *ranks* are -- by scoring each item `sum(1 / (RRF_K + rank))`
    across every list it appears in (`RRF_K=60` is the standard damping
    constant from the original RRF paper: it flattens the difference
    between rank 1 and rank 2 so one list's top hit cannot dominate).
    """
    vector_hits = search_entities(question, k=max(k, 10))
    fulltext_hits = search_fulltext(question, k=max(k, 10))

    scores: dict[str, float] = {}
    info: dict[str, dict] = {}
    for hits in (vector_hits, fulltext_hits):
        for rank, hit in enumerate(hits, start=1):
            key = hit["normalized_name"]
            scores[key] = scores.get(key, 0.0) + 1.0 / (_RRF_K + rank)
            info[key] = hit

    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:k]
    return [{**info[key], "rrf_score": round(score, 5)} for key, score in ranked]


# --- CLI ---------------------------------------------------------------------


@app.command()
def run(
    batch: int = typer.Option(_EMBED_BATCH_SIZE, "--batch"),
    embed_dim: int = typer.Option(768, "--embed-dim"),
) -> None:
    """Embed every Chunk/Entity missing `embedding`, then create and wait for the indexes."""
    n_chunks = embed_chunks(batch=batch)
    n_entities = embed_entities(batch=batch)
    console.print(f"embedded {n_chunks} chunk(s), {n_entities} entity(ies)")
    ensure_indexes(embed_dim=embed_dim)
    console.print("[green]indexes ONLINE: chunk_embedding, entity_embedding, chunk_text, entity_names[/green]")


@app.command()
def search(
    question: str,
    mode: str = typer.Option("hybrid", "--mode", help="chunks|entities|fulltext|hybrid"),
    k: int = typer.Option(5, "--k"),
) -> None:
    """Run one search mode against `question` and print a results table."""
    if mode == "chunks":
        rows = search_chunks(question, k=k)
        columns = ["id", "score", "text"]
    elif mode == "entities":
        rows = search_entities(question, k=k)
        columns = ["name", "type", "score"]
    elif mode == "fulltext":
        rows = search_fulltext(question, k=k)
        columns = ["name", "type", "score"]
    elif mode == "hybrid":
        rows = hybrid_search_entities(question, k=k)
        columns = ["name", "type", "rrf_score"]
    else:
        raise typer.BadParameter(f"unknown mode: {mode}")

    table = Table(title=f"{mode} search: {question!r}")
    for col in columns:
        table.add_column(col)
    for row in rows:
        table.add_row(*[str(row.get(c, ""))[:100] for c in columns])
    console.print(table)


if __name__ == "__main__":
    app()
