"""Entity resolution: find and merge duplicate `Entity` nodes (chapter 06).

Chapter 05 wrote the domain graph with `normalized_name` as the only MERGE
key, which catches exact-spelling duplicates but nothing else: chunk 04/05
already showed real duplicates like `GraphRAG` / `Graph Retrieval-Augmented
Generation` or `G-Indexing` / `Graph-Based Indexing (G-Indexing)`. This
module finds those duplicates in three stages of increasing cost and
decreasing precision-by-construction, then asks an LLM to judge each
candidate pair before merging anything:

  1. `candidates_by_normalization` -- cheap, deterministic, Python only.
  2. `candidates_by_embedding`     -- one Ollama embedding call per entity,
                                      cosine similarity in Python.
  3. `judge_pairs`                 -- one Ollama chat call per candidate
                                      pair, cached to disk (LLM-as-judge).

Only pairs the judge confirms are `same_entity` are merged, via
`apoc.refactor.mergeNodes` (APOC = Awesome Procedures On Cypher).

Run with: python -m graph_rag.resolution run|report [--dry-run] [--threshold 0.92]
"""

import json
import re
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

import typer
from pydantic import BaseModel, Field
from rich.console import Console
from rich.table import Table

from graph_rag.db import run as run_query
from graph_rag.llm import embed, chat_json

app = typer.Typer(add_completion=False)
console = Console()

_CACHE_DIR = Path("data/extracted/resolution")
_DEFAULT_THRESHOLD = 0.92

_PUNCT_RE = re.compile(r"[^\w\s]", re.UNICODE)
_WHITESPACE_RE = re.compile(r"\s+")
_PAREN_RE = re.compile(r"\(([^)]*)\)")

# "Full Name (ACRONYM)" -- e.g. "Large Language Model (LLM)",
# "Graph-Based Indexing (G-Indexing)". The acronym side is only required to
# start with a capital letter; "G-Indexing" is not a pure letter-acronym but
# is exactly the shorthand this document actually uses for the phrase next
# to it, so a stricter `[A-Z]{2,6}` regex would miss it.
_ACRONYM_RE = re.compile(r"\b([A-Z][\w-]*(?:\s+[A-Z][\w-]*)*)\s*\(([A-Z][\w-]{1,20})\)")


# --- Pydantic models ---------------------------------------------------------


class CandidatePair(BaseModel):
    a_norm: str
    b_norm: str
    a_name: str
    b_name: str
    method: str  # "normalization" | "embedding"
    score: float | None = None  # cosine similarity, only set for "embedding"


class Judgement(BaseModel):
    same_entity: bool = Field(description="True if both names refer to the same real-world thing")
    canonical_name: str = Field(description="The best human-readable name to keep")
    reason: str = Field(description="One sentence explaining the decision")


# --- stage 1: normalization + acronym candidates -----------------------------


def strip_parenthetical(name: str) -> str:
    """Drop any '(...)' content entirely, e.g. 'Graph-Based Indexing (G-Indexing)' -> 'Graph-Based Indexing'."""
    return _WHITESPACE_RE.sub(" ", _PAREN_RE.sub(" ", name)).strip()


def _singularize(word: str) -> str:
    """A simple plural stemmer: 'datasets' -> 'dataset'. Not linguistically
    complete (won't touch irregular plurals), but the corpus here is
    technical English where trailing '-s' plurals dominate.
    """
    if len(word) > 3 and word.endswith("ies"):
        return word[:-3] + "y"
    if len(word) > 3 and word.endswith("es") and word[-3] in "sxz":
        return word[:-2]
    if len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word


def build_acronym_map(names: list[str]) -> dict[str, str]:
    """Scan entity names for 'Full Name (ACRONYM)' patterns and build a map
    from the acronym's resolution key to the full name's resolution key.
    Built fresh from this corpus every run -- no hardcoded acronym list.
    """
    acronym_map: dict[str, str] = {}
    for name in names:
        for match in _ACRONYM_RE.finditer(name):
            phrase, acronym = match.group(1), match.group(2)
            acronym_map[resolution_key(acronym)] = resolution_key(phrase)
    return acronym_map


def resolution_key(name: str, acronym_map: dict[str, str] | None = None) -> str:
    """A looser normalization than `extraction.normalized_name`: also drops
    parenthetical asides, treats hyphens as word separators, and singularizes
    each word. Two entities with the same `resolution_key` are Stage 1
    candidates -- likely the same thing spelled differently.
    """
    text = strip_parenthetical(name).casefold()
    text = _PUNCT_RE.sub(" ", text.replace("-", " "))
    words = [_singularize(w) for w in _WHITESPACE_RE.split(text) if w]
    key = " ".join(words)
    if acronym_map and key in acronym_map:
        key = acronym_map[key]
    return key


def candidates_by_normalization(entities: list[dict]) -> list[CandidatePair]:
    """Group entities whose `resolution_key` collides. `entities` is a list of
    dicts with at least `name` and `normalized_name`.
    """
    acronym_map = build_acronym_map([e["name"] for e in entities])
    groups: dict[str, list[dict]] = {}
    for e in entities:
        key = resolution_key(e["name"], acronym_map)
        groups.setdefault(key, []).append(e)

    pairs: list[CandidatePair] = []
    for members in groups.values():
        distinct = {m["normalized_name"]: m for m in members}
        if len(distinct) < 2:
            continue
        for a, b in combinations(distinct.values(), 2):
            pairs.append(
                CandidatePair(
                    a_norm=a["normalized_name"], b_norm=b["normalized_name"],
                    a_name=a["name"], b_name=b["name"], method="normalization",
                )
            )
    return pairs


# --- stage 2: embedding similarity -------------------------------------------


def _cosine(u: list[float], v: list[float]) -> float:
    dot = sum(x * y for x, y in zip(u, v))
    norm_u = sum(x * x for x in u) ** 0.5
    norm_v = sum(y * y for y in v) ** 0.5
    return dot / (norm_u * norm_v) if norm_u and norm_v else 0.0


def ensure_embeddings(entities: list[dict]) -> None:
    """Embed `name + ': ' + description` for entities missing `Entity.embedding`,
    batching Ollama calls (32 at a time, see `llm.embed`) and writing each
    batch back to Neo4j immediately so a re-run only embeds what's still
    missing -- the same "cache as you go" pattern chapter 04 uses for
    extraction, applied here to embeddings instead of LLM JSON.
    """
    todo = [e for e in entities if e.get("embedding") is None]
    if not todo:
        return
    texts = [f"{e['name']}: {e['description']}" for e in todo]
    batch_size = 32
    for i in range(0, len(todo), batch_size):
        batch = todo[i : i + batch_size]
        vectors = embed(texts[i : i + batch_size])
        run_query(
            "UNWIND $rows AS row MATCH (n:Entity {normalized_name: row.norm}) SET n.embedding = row.vec",
            rows=[{"norm": e["normalized_name"], "vec": v} for e, v in zip(batch, vectors)],
        )
        for e, v in zip(batch, vectors):
            e["embedding"] = v


def candidates_by_embedding(entities: list[dict], threshold: float = _DEFAULT_THRESHOLD) -> list[CandidatePair]:
    """Pairwise cosine similarity over `Entity.embedding`, restricted to pairs
    with the same `type` (or one of them "Other") -- a `Method` and a
    `Dataset` should never merge just because their descriptions are similar
    prose, but an "Other"-typed entity might genuinely be either side of a
    real match the frozen schema mistyped.
    """
    ensure_embeddings(entities)
    pairs: list[CandidatePair] = []
    n = len(entities)
    for i in range(n):
        a = entities[i]
        if a.get("embedding") is None:
            continue
        for j in range(i + 1, n):
            b = entities[j]
            if b.get("embedding") is None:
                continue
            if a["type"] != b["type"] and "Other" not in (a["type"], b["type"]):
                continue
            score = _cosine(a["embedding"], b["embedding"])
            if score >= threshold:
                pairs.append(
                    CandidatePair(
                        a_norm=a["normalized_name"], b_norm=b["normalized_name"],
                        a_name=a["name"], b_name=b["name"], method="embedding", score=round(score, 4),
                    )
                )
    return pairs


# --- stage 3: LLM-as-judge ---------------------------------------------------

_JUDGE_SYSTEM = """You are an entity-resolution judge for a knowledge graph built from a \
technical survey paper. You will be given two candidate entities: their names, types, \
descriptions, and one sentence of text where each was mentioned. Decide whether they refer to \
the SAME real-world thing (a duplicate that should be merged) or two DIFFERENT things that \
happen to look similar. Two entities with the same surface name but different roles (for \
example one is a general concept/component and the other a specific named system or model) are \
DIFFERENT. Output ONLY JSON matching the given schema. If they are the same, `canonical_name` \
should be the clearest, most complete of the two names."""


def _mention_text(norm_name: str) -> str:
    rows = run_query(
        "MATCH (:Chunk)-[m:MENTIONS]->(:Entity {normalized_name: $n}) RETURN m.description AS d LIMIT 1",
        n=norm_name,
    )
    return rows[0]["d"] if rows else ""


def _cache_path(a_norm: str, b_norm: str) -> Path:
    a, b = sorted([a_norm, b_norm])
    safe = lambda s: re.sub(r"[^\w-]", "_", s)[:80]
    return _CACHE_DIR / f"{safe(a)}__{safe(b)}.json"


def judge_pairs(pairs: list[CandidatePair], entity_lookup: dict[str, dict]) -> list[tuple[CandidatePair, Judgement]]:
    """LLM-as-judge over candidate pairs, one Ollama call per pair, cached to
    `data/extracted/resolution/<a>__<b>.json` so re-running `resolution.py`
    never re-pays for a judgement already made.
    """
    _CACHE_DIR.mkdir(parents=True, exist_ok=True)
    results: list[tuple[CandidatePair, Judgement]] = []
    for pair in pairs:
        path = _cache_path(pair.a_norm, pair.b_norm)
        if path.exists():
            judgement = Judgement.model_validate_json(path.read_text())
        else:
            a, b = entity_lookup[pair.a_norm], entity_lookup[pair.b_norm]
            user = (
                f"Entity A: {a['name']} (type: {a['type']})\n"
                f"Description A: {a['description']}\n"
                f"Mention A: {_mention_text(pair.a_norm)}\n\n"
                f"Entity B: {b['name']} (type: {b['type']})\n"
                f"Description B: {b['description']}\n"
                f"Mention B: {_mention_text(pair.b_norm)}"
            )
            messages = [{"role": "system", "content": _JUDGE_SYSTEM}, {"role": "user", "content": user}]
            judgement = chat_json(messages, Judgement)
            path.write_text(judgement.model_dump_json(indent=2) + "\n")
        results.append((pair, judgement))
    return results


# --- merge --------------------------------------------------------------


def merge(a_norm: str, b_norm: str, canonical_name: str, method: str) -> dict | None:
    """Merge the `Entity` node `b_norm` into `a_norm` with `apoc.refactor.mergeNodes`.

    Property policy (the second argument to `mergeNodes`):
    - `name`: 'discard' -- we set the canonical `name` ourselves afterwards,
      so whichever side's `name` APOC happens to keep does not matter.
    - `aliases`: 'combine' -- APOC concatenates both nodes' `aliases` lists;
      we still de-duplicate case-insensitively afterwards since `combine`
      does not dedupe by itself.
    - `description`: 'combine' -- APOC turns two scalar descriptions into a
      list; we keep the longer of the two right after, same "more
      informative wins" rule as chapter 05's write.
    - `` `.*` `` (everything else, e.g. `type`, `created_at`, `embedding`): 'discard'
      -- the surviving node (`keep`) already carries a value for these from
      whichever of the two nodes was created first; there is no principled
      way to combine a `type` string or an embedding vector, so we keep the
      one already on `keep` and drop `b`'s.
    - `mergeRels: true` -- every relationship pointing at or from the
      discarded node (`MENTIONS`, and any domain relationship) is
      redirected onto the kept node instead of being dropped; parallel
      relationships of the same type between the same two nodes afterwards
      are left as-is by APOC (multiple edges can remain), so `chunk_ids` are
      unioned across them in a follow-up query below rather than relying on
      APOC to do it.
    """
    rows = run_query(
        """
        MATCH (a:Entity {normalized_name: $a_norm}), (b:Entity {normalized_name: $b_norm})
        WHERE a <> b
        CALL apoc.refactor.mergeNodes([a, b], {
            properties: {
                name: 'discard',
                aliases: 'combine',
                description: 'combine',
                `.*`: 'discard'
            },
            mergeRels: true
        }) YIELD node
        RETURN node.normalized_name AS normalized_name
        """,
        a_norm=a_norm, b_norm=b_norm,
    )
    if not rows:
        return None
    kept_norm = rows[0]["normalized_name"]

    # `description: 'combine'` turns two scalar descriptions into a list (or,
    # on a second merge into an already-merged node, extends that list
    # further) -- flatten in Python and keep the longest, rather than trust
    # a fixed list length in Cypher.
    current = run_query(
        "MATCH (n:Entity {normalized_name: $norm}) RETURN n.description AS description, n.aliases AS aliases",
        norm=kept_norm,
    )[0]
    descriptions = current["description"] if isinstance(current["description"], list) else [current["description"]]
    descriptions = [d for d in descriptions if d]
    best_description = max(descriptions, key=len) if descriptions else ""
    deduped_aliases = sorted({a.casefold(): a for a in (current["aliases"] or [])}.values())

    run_query(
        """
        MATCH (n:Entity {normalized_name: $norm})
        SET n.name = $canonical_name,
            n.normalized_name = $new_norm,
            n.description = $description,
            n.aliases = $aliases
        """,
        norm=kept_norm, canonical_name=canonical_name, new_norm=_new_normalized_name(canonical_name),
        description=best_description, aliases=deduped_aliases,
    )
    # de-duplicate any parallel relationships APOC left behind (same type,
    # same endpoints) by unioning their chunk_ids and deleting the extras.
    run_query(
        """
        MATCH (n:Entity {normalized_name: $norm})-[r]->(m)
        WITH n, m, type(r) AS rel_type, collect(r) AS rels
        WHERE size(rels) > 1
        WITH rels[0] AS keep_rel, rels[1..] AS extra_rels,
             reduce(ids = [], x IN rels | ids + coalesce(x.chunk_ids, [])) AS all_ids
        SET keep_rel.chunk_ids = apoc.coll.toSet(all_ids)
        WITH extra_rels
        UNWIND extra_rels AS extra
        DELETE extra
        """,
        norm=kept_norm,
    )
    run_query(
        """
        CREATE (:ResolutionLog {
            a: $a_norm, b: $b_norm, canonical: $canonical_name,
            method: $method, at: datetime()
        })
        """,
        a_norm=a_norm, b_norm=b_norm, canonical_name=canonical_name, method=method,
    )
    return {"kept_normalized_name": _new_normalized_name(canonical_name)}


def _new_normalized_name(canonical_name: str) -> str:
    from graph_rag.extraction import normalized_name

    return normalized_name(canonical_name)


# --- run / report -------------------------------------------------------


def fetch_entities() -> list[dict]:
    rows = run_query(
        "MATCH (n:Entity) RETURN n.name AS name, n.normalized_name AS normalized_name, "
        "n.type AS type, n.description AS description, n.embedding AS embedding"
    )
    return rows


def find_candidates(entities: list[dict], threshold: float) -> list[CandidatePair]:
    norm_pairs = candidates_by_normalization(entities)
    embed_pairs = candidates_by_embedding(entities, threshold=threshold)
    seen = {frozenset((p.a_norm, p.b_norm)) for p in norm_pairs}
    combined = list(norm_pairs)
    for p in embed_pairs:
        key = frozenset((p.a_norm, p.b_norm))
        if key not in seen:
            combined.append(p)
            seen.add(key)
    return combined


def run_resolution(dry_run: bool, threshold: float) -> Table:
    entities = fetch_entities()
    entity_lookup = {e["normalized_name"]: e for e in entities}
    pairs = find_candidates(entities, threshold)

    table = Table(title=f"Resolution candidates ({len(pairs)} pair(s), threshold={threshold})")
    table.add_column("a")
    table.add_column("b")
    table.add_column("method")
    table.add_column("score")
    table.add_column("decision")
    table.add_column("canonical")

    if not pairs:
        console.print(table)
        return table

    judged = judge_pairs(pairs, entity_lookup)
    merges_done = 0
    for pair, judgement in judged:
        decision = "MERGE" if judgement.same_entity else "keep separate"
        table.add_row(
            pair.a_name, pair.b_name, pair.method,
            f"{pair.score:.3f}" if pair.score is not None else "-",
            decision, judgement.canonical_name if judgement.same_entity else "-",
        )
        if judgement.same_entity and not dry_run:
            # a pair earlier in the loop may have already merged one of
            # these two normalized_names into a third node; MATCH ... WHERE
            # a <> b in merge() silently no-ops if both sides now resolve
            # to the same node, so re-running is always safe.
            result = merge(pair.a_norm, pair.b_norm, judgement.canonical_name, pair.method)
            if result is not None:
                merges_done += 1
    if not dry_run:
        console.print(f"[green]{merges_done} merge(s) applied[/green]")
    else:
        console.print("[yellow]--dry-run: no merges applied[/yellow]")
    return table


def report() -> Table:
    rows = run_query(
        "MATCH (n:ResolutionLog) RETURN n.a AS a, n.b AS b, n.canonical AS canonical, "
        "n.method AS method, toString(n.at) AS at ORDER BY n.at"
    )
    table = Table(title=f"Resolution log ({len(rows)} merge(s))")
    table.add_column("a")
    table.add_column("b")
    table.add_column("canonical")
    table.add_column("method")
    table.add_column("at")
    for row in rows:
        table.add_row(row["a"], row["b"], row["canonical"], row["method"], row["at"])
    return table


# --- CLI ---------------------------------------------------------------------


@app.command()
def run(  # noqa: A001 - CLI command name matches spec
    dry_run: bool = typer.Option(False, "--dry-run", help="Print candidates and decisions but merge nothing"),
    threshold: float = typer.Option(_DEFAULT_THRESHOLD, "--threshold", help="Embedding cosine-similarity cutoff"),
) -> None:
    """Find and merge duplicate Entity nodes (chapter 06)."""
    table = run_resolution(dry_run=dry_run, threshold=threshold)
    console.print(table)


@app.command(name="report")
def report_cmd() -> None:
    """Print every merge recorded in :ResolutionLog."""
    console.print(report())


if __name__ == "__main__":
    app()
