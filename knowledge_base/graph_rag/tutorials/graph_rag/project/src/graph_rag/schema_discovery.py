"""Let the LLM propose a graph schema from a sample of chunks, then freeze it.

We do not know, ahead of time, what *kinds* of things a new document talks
about. Rather than hand-writing a schema (which only works for documents we
already understand) or extracting with no schema at all (which produces
inconsistent, unqueryable labels — see the chapter for the comparison), this
module asks the LLM to read a spread sample of chunks and propose entity
types, relationship types and their properties, then lets a human review and
freeze the result to `data/extracted/schema.json`. Chapter 04 extracts
against that frozen schema.

Run with: python -m graph_rag.schema_discovery propose|show|validate
"""

import json
import re
from pathlib import Path
from typing import Literal

import typer
from pydantic import BaseModel, Field
from rich.console import Console
from rich.table import Table

from graph_rag.db import run
from graph_rag.llm import chat_json

app = typer.Typer(add_completion=False)
console = Console()

_DEFAULT_OUT = Path("data/extracted/schema.json")

_PROPERTY_TYPES = ("string", "integer", "float", "date", "boolean", "list[string]")


class PropertySpec(BaseModel):
    name: str
    type: Literal["string", "integer", "float", "date", "boolean", "list[string]"]
    description: str


class EntityType(BaseModel):
    name: str = Field(description="PascalCase, e.g. Method, Dataset")
    description: str
    properties: list[PropertySpec] = Field(default_factory=list)
    examples: list[str] = Field(default_factory=list, description="Real examples seen in the text")


class RelationshipType(BaseModel):
    name: str = Field(description="UPPER_SNAKE_CASE, e.g. EVALUATED_ON")
    description: str
    source_types: list[str]
    target_types: list[str]
    properties: list[PropertySpec] = Field(default_factory=list)


class GraphSchema(BaseModel):
    entity_types: list[EntityType]
    relationship_types: list[RelationshipType]


# --- sampling -----------------------------------------------------------


def sample_chunks(n: int = 12, strategy: str = "spread") -> list[dict]:
    """Pick `n` chunks from the whole document, not just the first `n`.

    `strategy="spread"` takes chunks evenly spaced over the document's index
    range (via Python striding over a full, index-ordered fetch) so the
    sample includes the intro, methods, evaluation and conclusion sections
    instead of only the abstract and introduction a "first N" sample would
    give.
    """
    rows = run("MATCH (c:Chunk) RETURN c.index AS index, c.text AS text ORDER BY c.index")
    if not rows:
        return []
    if strategy != "spread" or len(rows) <= n:
        return rows[:n]
    step = len(rows) / n
    indices = sorted({int(i * step) for i in range(n)})
    return [rows[i] for i in indices]


# --- naming / normalisation ----------------------------------------------

_PASCAL_RE = re.compile(r"^[A-Z][A-Za-z0-9]*$")
_UPPER_SNAKE_RE = re.compile(r"^[A-Z][A-Z0-9]*(_[A-Z0-9]+)*$")


def _to_pascal_case(name: str) -> str:
    parts = re.split(r"[^A-Za-z0-9]+", name)
    return "".join(p[:1].upper() + p[1:] for p in parts if p)


def _to_upper_snake_case(name: str) -> str:
    parts = re.split(r"[^A-Za-z0-9]+", name)
    return "_".join(p.upper() for p in parts if p)


def normalize_schema(schema: GraphSchema) -> GraphSchema:
    """Enforce naming rules in Python instead of trusting the LLM to follow
    them, and drop entity/relationship types that end up as duplicates after
    normalisation (e.g. the LLM proposing both "Paper" and "Research Paper").
    """
    seen_entities: dict[str, EntityType] = {}
    for entity in schema.entity_types:
        name = entity.name if _PASCAL_RE.match(entity.name) else _to_pascal_case(entity.name)
        if name not in seen_entities:
            seen_entities[name] = entity.model_copy(update={"name": name})

    valid_types = set(seen_entities)
    seen_relationships: dict[str, RelationshipType] = {}
    for rel in schema.relationship_types:
        name = rel.name if _UPPER_SNAKE_RE.match(rel.name) else _to_upper_snake_case(rel.name)
        source_types = [t for t in rel.source_types if t in valid_types]
        target_types = [t for t in rel.target_types if t in valid_types]
        if not source_types or not target_types:
            continue
        if name not in seen_relationships:
            seen_relationships[name] = rel.model_copy(
                update={"name": name, "source_types": source_types, "target_types": target_types}
            )

    return GraphSchema(
        entity_types=list(seen_entities.values()),
        relationship_types=list(seen_relationships.values()),
    )


def validate_schema(schema: GraphSchema) -> list[str]:
    """Check naming rules and referential integrity. Returns a list of
    human-readable issues; an empty list means the schema is valid.
    """
    issues: list[str] = []
    entity_names = {e.name for e in schema.entity_types}

    if len(entity_names) != len(schema.entity_types):
        issues.append("duplicate entity type names")
    for entity in schema.entity_types:
        if not _PASCAL_RE.match(entity.name):
            issues.append(f"entity type '{entity.name}' is not PascalCase")
        for prop in entity.properties:
            if prop.type not in _PROPERTY_TYPES:
                issues.append(f"entity type '{entity.name}' property '{prop.name}' has invalid type '{prop.type}'")

    rel_names = [r.name for r in schema.relationship_types]
    if len(set(rel_names)) != len(rel_names):
        issues.append("duplicate relationship type names")
    for rel in schema.relationship_types:
        if not _UPPER_SNAKE_RE.match(rel.name):
            issues.append(f"relationship type '{rel.name}' is not UPPER_SNAKE_CASE")
        for endpoint_kind, types in (("source", rel.source_types), ("target", rel.target_types)):
            if not types:
                issues.append(f"relationship type '{rel.name}' has no {endpoint_kind}_types")
            for t in types:
                if t not in entity_names:
                    issues.append(f"relationship type '{rel.name}' has dangling {endpoint_kind} type '{t}'")

    return issues


# --- LLM prompts ----------------------------------------------------------

_PROPOSE_PROMPT = """You are a knowledge-graph architect. Below are sample passages taken from \
one document, spread evenly across its whole length. Propose a graph schema that would let \
someone answer questions about these texts.

Rules:
- Propose at most 12 entity types and at most 15 relationship types.
- Entity type names must be PascalCase (e.g. Method, Dataset, Organization).
- Relationship type names must be UPPER_SNAKE_CASE (e.g. EVALUATED_ON, PROPOSED_BY).
- Do not propose generic types like "Thing", "Concept", "Entity" or "Item" — every type must \
be specific enough that a reader immediately knows what belongs in it.
- Every relationship type must declare which entity type(s) can be its source and target.
- Give each entity type 2-4 relevant properties (beyond name/description) and 1-3 real \
examples drawn from the passages.
- Only propose types that are actually reflected in the passages below.

Passages:
{passages}
"""

_REFINE_PROMPT = """You proposed the following draft graph schema from a first sample of a \
document. Here is a second, different sample of passages from the same document. Refine the \
schema:
- Merge or rename entity/relationship types that overlap or duplicate each other.
- Drop any type that is not clearly supported by evidence in the samples (first or second).
- Add a type only if the new passages clearly need it and no existing type fits.
- Keep names PascalCase for entity types and UPPER_SNAKE_CASE for relationship types.
- Output the complete, revised schema (not just the changes).

Draft schema (JSON):
{draft}

New passages:
{passages}
"""


def _format_passages(chunks: list[dict]) -> str:
    return "\n\n".join(f"--- passage (chunk {c['index']}) ---\n{c['text']}" for c in chunks)


def propose_schema(chunks: list[dict]) -> GraphSchema:
    prompt = _PROPOSE_PROMPT.format(passages=_format_passages(chunks))
    return chat_json([{"role": "user", "content": prompt}], GraphSchema)


def refine_schema(schema: GraphSchema, more_chunks: list[dict]) -> GraphSchema:
    prompt = _REFINE_PROMPT.format(
        draft=schema.model_dump_json(indent=2),
        passages=_format_passages(more_chunks),
    )
    return chat_json([{"role": "user", "content": prompt}], GraphSchema)


# --- storage ----------------------------------------------------------


def store_schema_in_graph(schema: GraphSchema, version: int = 1) -> None:
    """Write the frozen schema into the graph itself as a `_Schema` node.

    The leading underscore keeps it out of the way of domain labels (no real
    document entity should ever be typed "_Schema"). Storing the schema in
    the same graph it describes means anyone exploring the database with
    plain Cypher (see `knowledge/research_topics/graph_rag/tutorials/neo4j/001_explore_database.md`)
    can discover the labels and relationship types in use without reading a
    separate file, and a future chapter can diff the graph against
    `_Schema.json` to detect drift.
    """
    run(
        "MERGE (s:_Schema {version: $version}) SET s.json = $json, s.updated_at = datetime()",
        version=version,
        json=schema.model_dump_json(),
    )


# --- CLI ----------------------------------------------------------------


@app.command()
def propose(samples: int = 12, out: Path = _DEFAULT_OUT) -> None:
    """Propose a schema from a first sample, refine it against a second sample, freeze it."""
    first_sample = sample_chunks(n=samples, strategy="spread")
    if not first_sample:
        raise typer.Exit("No chunks found — run `just ingest` first (see chapter 02).")
    print(f"Proposing schema from {len(first_sample)} sampled chunks...")
    draft = propose_schema(first_sample)

    second_sample = sample_chunks(n=samples, strategy="spread")
    print(f"Refining schema against {len(second_sample)} more sampled chunks...")
    refined = refine_schema(draft, second_sample)

    schema = normalize_schema(refined)
    issues = validate_schema(schema)
    if issues:
        print("Validation issues after normalisation:")
        for issue in issues:
            print(f"  - {issue}")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(schema.model_dump_json(indent=2) + "\n")
    print(f"Wrote {len(schema.entity_types)} entity types, {len(schema.relationship_types)} "
          f"relationship types -> {out}")

    store_schema_in_graph(schema)
    print("Stored schema as (:_Schema {version: 1}) in the graph.")


@app.command()
def show(path: Path = _DEFAULT_OUT) -> None:
    """Pretty-print the frozen schema as two tables."""
    schema = GraphSchema.model_validate_json(path.read_text())

    entity_table = Table(title="Entity types")
    entity_table.add_column("Name")
    entity_table.add_column("Description")
    entity_table.add_column("Properties")
    entity_table.add_column("Examples")
    for entity in schema.entity_types:
        entity_table.add_row(
            entity.name,
            entity.description,
            ", ".join(p.name for p in entity.properties),
            ", ".join(entity.examples),
        )
    console.print(entity_table)

    rel_table = Table(title="Relationship types")
    rel_table.add_column("Name")
    rel_table.add_column("Description")
    rel_table.add_column("Source -> Target")
    for rel in schema.relationship_types:
        rel_table.add_row(
            rel.name,
            rel.description,
            f"{'/'.join(rel.source_types)} -> {'/'.join(rel.target_types)}",
        )
    console.print(rel_table)


@app.command()
def validate(path: Path = _DEFAULT_OUT) -> None:
    """Validate the frozen schema's naming rules and referential integrity."""
    schema = GraphSchema.model_validate_json(path.read_text())
    issues = validate_schema(schema)
    if issues:
        print(f"{len(issues)} issue(s):")
        for issue in issues:
            print(f"  - {issue}")
        raise typer.Exit(1)
    print(f"OK: {len(schema.entity_types)} entity types, {len(schema.relationship_types)} "
          "relationship types, no issues.")


if __name__ == "__main__":
    app()
