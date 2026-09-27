"""Extract entities and relationships from every chunk, against the frozen schema.

Chapter 03 froze a graph schema (`data/extracted/schema.json`): a fixed list of
entity types (e.g. `Method`, `Dataset`) and relationship types (e.g.
`EVALUATED_ON`) with allowed endpoints. This module asks the LLM (Large
Language Model) to read one chunk at a time and return entities and
relationships that fit that schema, as JSON validated against a Pydantic
schema (a Python class that describes the exact shape of the data). We do
NOT write anything to Neo4j here: chapter 05 does that. Keeping extraction
and graph-writing separate means a bad write query or a schema tweak never
forces us to re-run the (slow, 20-60s per chunk) LLM calls -- we just replay
the cached JSON in `data/extracted/chunks/`.

Run with: python -m graph_rag.extraction run|stats|show
"""

import json
import re
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

import typer
from pydantic import BaseModel, Field
from rich.console import Console
from rich.progress import BarColumn, MofNCompleteColumn, Progress, TextColumn, TimeElapsedColumn
from rich.table import Table

from graph_rag.db import run as run_query
from graph_rag.llm import chat_json
from graph_rag.schema_discovery import GraphSchema

app = typer.Typer(add_completion=False)
console = Console()

_SCHEMA_PATH = Path("data/extracted/schema.json")
_CHUNKS_DIR = Path("data/extracted/chunks")
PROMPT_VERSION = "v1"

_ARTICLES = {"a", "an", "the"}
_PUNCT_RE = re.compile(r"[^\w\s-]", re.UNICODE)
_WHITESPACE_RE = re.compile(r"\s+")

PropertyValue = str | int | float | bool | list[str]


# --- Pydantic models ------------------------------------------------------


class ExtractedEntity(BaseModel):
    name: str = Field(description="Exact name as it appears in the text")
    type: str = Field(description="One of the allowed entity types, or 'Other'")
    description: str = Field(description="One sentence, grounded in this chunk")
    properties: dict[str, PropertyValue] = Field(default_factory=dict)
    normalized_name: str = Field(
        default="", description="Filled in by normalize(), not by the LLM"
    )


class ExtractedRelationship(BaseModel):
    source: str = Field(description="Must match an entity name extracted from this chunk")
    target: str = Field(description="Must match an entity name extracted from this chunk")
    type: str = Field(description="One of the allowed relationship types, UPPER_SNAKE_CASE")
    description: str = Field(description="One sentence, grounded in this chunk")
    weight: float = Field(ge=0, le=1, description="How strongly the text supports this relationship")
    properties: dict[str, PropertyValue] = Field(default_factory=dict)


class ChunkExtraction(BaseModel):
    chunk_id: str
    entities: list[ExtractedEntity]
    relationships: list[ExtractedRelationship]
    model: str
    prompt_version: str
    extracted_at: str


class _LLMExtraction(BaseModel):
    """The narrower shape we actually ask the LLM to produce.

    The model should never be asked to invent `chunk_id`, `model`,
    `prompt_version`, `extracted_at` or `normalized_name` -- those are added
    by us afterwards, from things we already know. Passing the wider
    `ChunkExtraction` schema to `chat_json` would tempt a small model into
    hallucinating values for fields it cannot possibly know.
    """

    entities: list[ExtractedEntity]
    relationships: list[ExtractedRelationship]


# --- prompt ----------------------------------------------------------------

_FEW_SHOT_CHUNK = """Graph Retrieval-Augmented Generation: A Survey
BOCI PENG, School of Intelligence Science and Technology, Peking University, China
YUN ZHU, College of Computer Science and Technology, Zhejiang University, China
YONGCHAO LIU, Ant Group, China
Graph-based Retrieval-Augmented Generation (GraphRAG) has emerged to \
effectively address the limitations of large language models (LLMs) by \
leveraging graphs with rich relational knowledge. GNN-RAG combines a \
graph neural network (GNN) with an LLM to answer questions over knowledge \
graphs. We evaluate GNN-RAG on the WebQSP dataset."""

_FEW_SHOT_OUTPUT = _LLMExtraction(
    entities=[
        ExtractedEntity(
            name="Graph Retrieval-Augmented Generation",
            type="Method",
            description="A survey subject: augmenting LLMs with graphs of relational knowledge.",
            properties={"category": "Retrieval"},
        ),
        ExtractedEntity(
            name="Boci Peng",
            type="Person",
            description="An author of this survey, affiliated with Peking University.",
        ),
        ExtractedEntity(
            name="Peking University",
            type="Organization",
            description="University affiliation of author Boci Peng.",
        ),
        ExtractedEntity(
            name="GNN-RAG",
            type="Method",
            description="A method combining a graph neural network with an LLM to answer questions over knowledge graphs.",
            properties={"technique": "GNN"},
        ),
        ExtractedEntity(
            name="WebQSP",
            type="Dataset",
            description="A dataset used to evaluate GNN-RAG.",
        ),
    ],
    relationships=[
        ExtractedRelationship(
            source="Boci Peng",
            target="Peking University",
            type="AFFILIATED_WITH",
            description="Boci Peng is affiliated with Peking University.",
            weight=0.95,
        ),
        ExtractedRelationship(
            source="GNN-RAG",
            target="WebQSP",
            type="EVALUATED_ON",
            description="GNN-RAG is evaluated on the WebQSP dataset.",
            weight=0.9,
        ),
    ],
).model_dump_json(indent=2)

_SYSTEM_TEMPLATE = """You are an information-extraction system building a knowledge graph from a \
technical document. Read the passage below and extract entities and relationships that fit \
this schema. Output ONLY JSON matching the given JSON schema.

Allowed entity types:
{entity_types}

Allowed relationship types (source type -> target type):
{relationship_types}

Rules:
1. Use the exact name for an entity as it appears in the text (do not translate, expand \
abbreviations, or rephrase).
2. Use ONE canonical name per real-world entity: if the same thing is mentioned twice in this \
passage (e.g. once in full, once abbreviated), pick a single name and reuse it for every \
mention, and reflect that in the relationships too.
3. Only create a relationship between two entities you extracted in this same passage. Never \
reference an entity that is not in your `entities` list.
4. Prefer one of the allowed entity types above. If nothing fits, use type "Other" -- we track \
how often "Other" is used as a signal that the schema needs a new type.
5. Relationship `type` must be one of the allowed relationship types above, in UPPER_SNAKE_CASE.
6. `weight` reflects how strongly the passage itself supports the relationship (1.0 = stated \
explicitly, 0.3 = weakly implied). Do not invent relationships the text does not support.
7. If the passage contains no clear entities, return empty lists. Do not pad with guesses.

Example
Passage:
{few_shot_chunk}

Output:
{few_shot_output}
"""


def _format_entity_types(schema: GraphSchema) -> str:
    lines = []
    for entity in schema.entity_types:
        props = ", ".join(p.name for p in entity.properties) or "none"
        lines.append(f"- {entity.name}: {entity.description} (properties: {props})")
    return "\n".join(lines)


def _format_relationship_types(schema: GraphSchema) -> str:
    lines = []
    for rel in schema.relationship_types:
        sources = "/".join(rel.source_types)
        targets = "/".join(rel.target_types)
        lines.append(f"- {rel.name}: {rel.description} ({sources} -> {targets})")
    return "\n".join(lines)


def build_prompt(schema: GraphSchema, chunk_text: str) -> list[dict]:
    """Build the chat messages for one chunk: one system prompt + the chunk as user content."""
    system = _SYSTEM_TEMPLATE.format(
        entity_types=_format_entity_types(schema),
        relationship_types=_format_relationship_types(schema),
        few_shot_chunk=_FEW_SHOT_CHUNK,
        few_shot_output=_FEW_SHOT_OUTPUT,
    )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": f"Passage:\n{chunk_text}"},
    ]


# --- normalisation -----------------------------------------------------------


def normalized_name(name: str) -> str:
    """casefold + drop leading articles + strip punctuation + collapse whitespace.

    This is the key we will MERGE on in chapter 05: "The GNN-RAG Model" and
    "GNN-RAG model" must land on the same node, so the identity we compare on
    has to survive capitalisation, articles and stray punctuation.
    """
    text = unicodedata.normalize("NFKC", name).strip().casefold()
    text = _PUNCT_RE.sub(" ", text)
    words = [w for w in _WHITESPACE_RE.split(text) if w]
    if words and words[0] in _ARTICLES:
        words = words[1:]
    return " ".join(words)


def _to_upper_snake_case(name: str) -> str:
    parts = re.split(r"[^A-Za-z0-9]+", name)
    return "_".join(p.upper() for p in parts if p)


def normalize(extraction: _LLMExtraction, schema: GraphSchema, chunk_id: str) -> ChunkExtraction:
    """Clean up raw LLM output into something safe to write to the graph later.

    - trims/collapses whitespace in free-text fields
    - computes `normalized_name` for every entity
    - coerces relationship types to UPPER_SNAKE_CASE
    - coerces entity types to a known schema type, else "Other"
    - drops relationships whose source/target is not one of this chunk's entities
    """
    schema_types = {e.name.casefold(): e.name for e in schema.entity_types}

    entities: list[ExtractedEntity] = []
    valid_norm_names: set[str] = set()
    for entity in extraction.entities:
        name = _WHITESPACE_RE.sub(" ", entity.name.strip())
        if not name:
            continue
        norm = normalized_name(name)
        entity_type = schema_types.get(entity.type.strip().casefold(), "Other")
        entities.append(
            entity.model_copy(
                update={
                    "name": name,
                    "type": entity_type,
                    "description": _WHITESPACE_RE.sub(" ", entity.description.strip()),
                    "normalized_name": norm,
                }
            )
        )
        valid_norm_names.add(norm)

    relationships: list[ExtractedRelationship] = []
    dropped = 0
    for rel in extraction.relationships:
        source_norm = normalized_name(rel.source)
        target_norm = normalized_name(rel.target)
        if source_norm not in valid_norm_names or target_norm not in valid_norm_names:
            dropped += 1
            continue
        relationships.append(
            rel.model_copy(
                update={
                    "source": source_norm,
                    "target": target_norm,
                    "type": _to_upper_snake_case(rel.type),
                    "description": _WHITESPACE_RE.sub(" ", rel.description.strip()),
                }
            )
        )
    if dropped:
        console.log(f"[yellow]chunk {chunk_id}: dropped {dropped} relationship(s) with unknown endpoints[/yellow]")

    return ChunkExtraction(
        chunk_id=chunk_id,
        entities=entities,
        relationships=relationships,
        model="",  # set by extract_chunk
        prompt_version=PROMPT_VERSION,
        extracted_at=datetime.now(timezone.utc).isoformat(),
    )


# --- extraction --------------------------------------------------------------


def load_schema(path: Path = _SCHEMA_PATH) -> GraphSchema:
    return GraphSchema.model_validate_json(path.read_text())


def extract_chunk(chunk: dict, schema: GraphSchema) -> ChunkExtraction:
    """Extract one chunk (`{"id": ..., "text": ...}`) via `llm.chat_json`, then normalize it."""
    from graph_rag.config import settings

    messages = build_prompt(schema, chunk["text"])
    raw = chat_json(messages, _LLMExtraction)
    result = normalize(raw, schema, chunk["id"])
    return result.model_copy(update={"model": settings.chat_model})


def fetch_chunks(doc_substring: str | None = None) -> list[dict]:
    query = """
    MATCH (d:Document)-[:HAS_CHUNK]->(c:Chunk)
    WHERE $doc IS NULL OR toLower(d.title) CONTAINS toLower($doc)
    RETURN c.id AS id, c.index AS index, c.text AS text
    ORDER BY c.index
    """
    return run_query(query, doc=doc_substring)


def cache_path(chunk_id: str) -> Path:
    safe_id = chunk_id.replace("/", "_")
    return _CHUNKS_DIR / f"{safe_id}.json"


def load_cached(chunk_id: str) -> ChunkExtraction | None:
    path = cache_path(chunk_id)
    if not path.exists():
        return None
    return ChunkExtraction.model_validate_json(path.read_text())


def save_cached(extraction: ChunkExtraction) -> None:
    _CHUNKS_DIR.mkdir(parents=True, exist_ok=True)
    cache_path(extraction.chunk_id).write_text(extraction.model_dump_json(indent=2) + "\n")


def _stats_from(extractions: list[ChunkExtraction], elapsed: float | None = None) -> Table:
    n_entities = sum(len(e.entities) for e in extractions)
    n_relationships = sum(len(e.relationships) for e in extractions)
    n_other = sum(1 for e in extractions for ent in e.entities if ent.type == "Other")

    table = Table(title="Extraction stats")
    table.add_column("metric")
    table.add_column("value")
    table.add_row("chunks", str(len(extractions)))
    table.add_row("entities", str(n_entities))
    table.add_row("relationships", str(n_relationships))
    table.add_row("'Other' entities", f"{n_other} ({n_other / n_entities:.1%})" if n_entities else "0")
    if elapsed is not None:
        table.add_row("elapsed", f"{elapsed:.1f}s")
        table.add_row("sec/chunk", f"{elapsed / len(extractions):.1f}s" if extractions else "n/a")
    return table


# --- CLI ---------------------------------------------------------------------


@app.command()
def run(  # noqa: A001 - CLI command name matches spec
    limit: int | None = None,
    doc: str | None = None,
    force: bool = False,
) -> None:
    """Extract entities/relationships for every chunk, skipping already-cached ones."""
    schema = load_schema()
    chunks = fetch_chunks(doc)
    if limit is not None:
        chunks = chunks[:limit]
    if not chunks:
        raise typer.Exit("No chunks found -- run `just ingest` first (see chapter 02).")

    todo = [c for c in chunks if force or load_cached(c["id"]) is None]
    print(f"{len(chunks)} chunk(s) selected, {len(todo)} need extraction ({len(chunks) - len(todo)} cached).")

    results: list[ChunkExtraction] = []
    start = time.monotonic()
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("extracting", total=len(todo))
        for chunk in todo:
            extraction = extract_chunk(chunk, schema)
            save_cached(extraction)
            progress.advance(task)
    elapsed = time.monotonic() - start

    for chunk in chunks:
        cached = load_cached(chunk["id"])
        if cached is not None:
            results.append(cached)

    console.print(_stats_from(results, elapsed if todo else None))


@app.command()
def stats(doc: str | None = None) -> None:
    """Print the stats table from the on-disk cache, without calling the LLM."""
    chunks = fetch_chunks(doc)
    results = [load_cached(c["id"]) for c in chunks]
    results = [r for r in results if r is not None]
    if not results:
        raise typer.Exit("No cached extractions found -- run `just extract` first.")
    console.print(_stats_from(results))


@app.command()
def show(chunk_id: str) -> None:
    """Print a chunk's text next to its cached extraction, side by side."""
    rows = run_query("MATCH (c:Chunk {id: $id}) RETURN c.text AS text", id=chunk_id)
    if not rows:
        raise typer.Exit(f"No chunk with id {chunk_id!r}")
    cached = load_cached(chunk_id)
    if cached is None:
        raise typer.Exit(f"No cached extraction for {chunk_id!r} -- run `just extract` first.")

    console.rule(f"Chunk {chunk_id}")
    console.print(rows[0]["text"])
    console.rule("Extraction")
    console.print_json(cached.model_dump_json())


if __name__ == "__main__":
    app()
