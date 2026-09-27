"""Chapter 09: community detection and global search (map-reduce over the graph).

Chapter 08's local search always starts from a *seed* -- an entity or a
chunk close to the question. That answers "what does X do?" well but has no
way to answer "what are the main themes across all documents?": there is no
single seed for a question about the whole graph. Microsoft's GraphRAG
answers this by first grouping the graph into densely-connected clusters of
entities called *communities*, asking the LLM (Large Language Model) to
summarise each community once, and then answering global questions by
map-reduce over those summaries instead of the raw graph:

  1. `detect()` -- project the `Entity` subgraph into GDS (Graph Data
     Science library, a Neo4j plugin for in-memory graph algorithms),
     run Leiden community detection, write `(:Community {id, level})
     <-[:IN_COMMUNITY]-(:Entity)` back into Neo4j.
  2. `summarize_communities()` -- for every community with enough members,
     ask the LLM for a structured `CommunityReport` (title, summary, key
     findings, importance rating), store it on the `Community` node, embed
     the summary, and cache it to disk.
  3. `global_search()` -- map: ask the LLM for a partial answer + a 0-100
     relevance score from each community's summary; reduce: merge the
     highest-scoring partial answers into one final answer that names which
     communities it used.

Run with: python -m graph_rag.communities detect|summarize|ask "<question>"
"""

import json
from datetime import datetime, timezone
from pathlib import Path

import typer
from pydantic import BaseModel, Field
from rich.console import Console
from rich.table import Table

from graph_rag.db import run as run_query
from graph_rag.llm import chat_json, embed

app = typer.Typer(add_completion=False)
console = Console()

_CACHE_DIR = Path("data/extracted/communities")
_PROJECTION_NAME = "entities"
_DEFAULT_MIN_SIZE = 3
_MAX_MEMBERS_IN_PROMPT = 40  # cap prompt size for very large communities
_MAX_INTERNAL_RELS_IN_PROMPT = 40
_MAX_PASSAGES_IN_PROMPT = 2


# --- Pydantic models ---------------------------------------------------------


class CommunityReport(BaseModel):
    title: str = Field(description="Short, specific name for this cluster of entities")
    summary: str = Field(description="2-4 sentences describing what this community is about")
    key_findings: list[str] = Field(description="3-6 bullet-point findings, grounded in the members/relationships given")
    rating: float = Field(ge=0, le=10, description="How important this community is to the overall document, 0-10")


# --- detection ----------------------------------------------------------------


def detect(random_seed: int = 42) -> dict:
    """Run Leiden community detection over the `Entity` subgraph and write
    `Community` nodes + `IN_COMMUNITY` edges for every level Leiden found.

    Leiden is a graph-clustering algorithm: it repeatedly moves nodes
    between communities to increase *modularity* -- roughly, "are there more
    edges inside these groups than we'd expect if edges were placed at
    random?" -- then merges the resulting communities into super-nodes and
    repeats, which is why it naturally produces a hierarchy of levels (many
    small communities at level 0, fewer/bigger ones at the top level)
    instead of a single flat partition.

    Projecting only the `Entity` label (no `Chunk`) automatically excludes
    `MENTIONS` (`Chunk -> Entity`) from the in-memory graph -- there is
    nothing to filter by relationship type, a plain label projection already
    leaves only Entity-Entity relationships (`PROPOSED_BY`, `EVALUATED_ON`,
    ...). `orientation: UNDIRECTED` matters because Leiden measures
    modularity over undirected edges: "A improves on B" and "B improves on
    A" should count as the same connection for clustering purposes, even
    though the domain graph stores relationships as directed.

    `concurrency: 1` is set deliberately: GDS parallelises Leiden's local
    node-moving phase across threads, and even with a fixed `randomSeed`
    that parallel scheduling can nondeterministically change which node
    "wins" a tie, producing a slightly different partition run to run
    (measured: 241 vs 242 communities with the default concurrency, 0
    entities differ between two `concurrency: 1` runs *against the exact
    same graph*). It is not a full fix, though: re-running the *upstream*
    pipeline (chapter 05's wipe+rewrite, chapter 06's resolution) before
    calling `detect()` again can itself land on very slightly different
    relationship weights -- `graph_writer`'s `ON MATCH SET rel.weight =
    (rel.weight + r.weight) / 2` and `apoc.refactor.mergeNodes`'s own merge
    order are not perfectly order-stable across separate replays -- and
    Leiden clusters by those weights, so a handful of borderline entities
    can still end up in a different community after a full pipeline replay,
    even with `concurrency: 1` here. See `data/extracted/communities/`'s
    note in the chapter text for what this means for the summary cache.

    Every call drops and rebuilds `Community` nodes from scratch: Leiden's
    community ids are arbitrary integers assigned fresh each run, not a
    stable identity, so reusing an old `(id, level)` node for what might now
    be a completely different set of members would silently leave a stale,
    mismatched `summary`/`title` attached to the wrong cluster. Dropping
    first means a `detect()` re-run always starts from a clean slate, and
    `summarize_communities()` has to be re-run afterward (cache hits still
    make that free for any community whose members didn't change enough to
    get a new id).
    """
    run_query("MATCH (k:Community) DETACH DELETE k")
    run_query(f"CALL gds.graph.drop('{_PROJECTION_NAME}', false) YIELD graphName RETURN graphName")

    run_query(
        f"""
        CALL gds.graph.project(
            '{_PROJECTION_NAME}', 'Entity',
            {{ALL: {{type: '*', orientation: 'UNDIRECTED', properties: 'weight'}}}}
        ) YIELD graphName, nodeCount, relationshipCount
        """
    )
    stats = run_query(
        f"""
        CALL gds.leiden.write('{_PROJECTION_NAME}', {{
            writeProperty: 'community',
            relationshipWeightProperty: 'weight',
            includeIntermediateCommunities: true,
            randomSeed: $seed,
            concurrency: 1
        }}) YIELD communityCount, modularity, ranLevels, nodePropertiesWritten
        """,
        seed=random_seed,
    )[0]
    run_query(f"CALL gds.graph.drop('{_PROJECTION_NAME}') YIELD graphName RETURN graphName")

    run_query("CREATE CONSTRAINT community_id_level IF NOT EXISTS "
               "FOR (k:Community) REQUIRE (k.id, k.level) IS UNIQUE")

    rows = run_query("MATCH (e:Entity) RETURN e.normalized_name AS key, e.community AS levels")
    n_levels = len(rows[0]["levels"]) if rows else 0
    for level in range(n_levels):
        memberships = [{"key": r["key"], "id": r["levels"][level]} for r in rows]
        run_query(
            """
            UNWIND $memberships AS m
            MERGE (k:Community {id: m.id, level: $level})
            ON CREATE SET k.created_at = datetime()
            WITH k, m
            MATCH (e:Entity {normalized_name: m.key})
            MERGE (e)-[:IN_COMMUNITY]->(k)
            """,
            memberships=memberships,
            level=level,
        )

    return {
        "community_count": stats["communityCount"],
        "modularity": stats["modularity"],
        "ran_levels": stats["ranLevels"],
        "levels_written": n_levels,
        "top_level": n_levels - 1,
    }


def _top_level() -> int:
    rows = run_query("MATCH (k:Community) RETURN max(k.level) AS top")
    top = rows[0]["top"]
    if top is None:
        raise typer.Exit("No communities found -- run `just communities` (detect) first.")
    return top


def level_sizes(level: int) -> list[dict]:
    return run_query(
        """
        MATCH (e:Entity)-[:IN_COMMUNITY]->(k:Community {level: $level})
        WITH k, count(e) AS size, collect(e.name)[..5] AS sample_members
        RETURN k.id AS id, size, sample_members ORDER BY size DESC
        """,
        level=level,
    )


# --- summarization --------------------------------------------------------------


def _report_input(community_id: int, level: int) -> dict | None:
    members = run_query(
        """
        MATCH (e:Entity)-[:IN_COMMUNITY]->(:Community {id: $id, level: $level})
        RETURN e.normalized_name AS key, e.name AS name, e.type AS type, e.description AS description
        ORDER BY e.name
        LIMIT $limit
        """,
        id=community_id, level=level, limit=_MAX_MEMBERS_IN_PROMPT,
    )
    if not members:
        return None
    keys = [m["key"] for m in members]

    internal_rels = run_query(
        """
        MATCH (a:Entity)-[r]->(b:Entity)
        WHERE a.normalized_name IN $keys AND b.normalized_name IN $keys AND type(r) <> 'MENTIONS'
        RETURN a.name AS subject, type(r) AS rel, b.name AS object, r.description AS description
        ORDER BY coalesce(r.weight, 0) DESC
        LIMIT $limit
        """,
        keys=keys, limit=_MAX_INTERNAL_RELS_IN_PROMPT,
    )

    passages = run_query(
        """
        MATCH (c:Chunk)-[:MENTIONS]->(e:Entity)
        WHERE e.normalized_name IN $keys
        RETURN DISTINCT c.id AS id, c.text AS text
        LIMIT $limit
        """,
        keys=keys, limit=_MAX_PASSAGES_IN_PROMPT,
    )

    return {"members": members, "internal_rels": internal_rels, "passages": passages}


def _report_prompt(report_input: dict) -> list[dict]:
    lines = ["## Members"]
    for m in report_input["members"]:
        lines.append(f"- {m['name']} ({m['type']}): {m['description']}")

    lines.append("\n## Internal relationships")
    for r in report_input["internal_rels"]:
        desc = f" -- {r['description']}" if r.get("description") else ""
        lines.append(f"- {r['subject']} -> {r['rel']} -> {r['object']}{desc}")

    lines.append("\n## Example passages")
    for p in report_input["passages"]:
        lines.append(f"[{p['id']}] {p['text']}")

    user_content = "\n".join(lines)
    system = (
        "You are summarising one community (a densely-connected cluster of entities) from a "
        "knowledge graph built from a technical survey paper. Using only the members, "
        "relationships and passages given, write a short report: a specific title, a 2-4 "
        "sentence summary, 3-6 concrete key findings, and an importance rating from 0 (minor) "
        "to 10 (central to the document). Do not invent members or facts not grounded below."
    )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user_content},
    ]


def _restore_cached_report(community_id: int, level: int, cached: dict) -> None:
    """Write a cached report's fields back onto the `Community` node.

    `detect()` drops and recreates every `Community` node on each run (see
    its docstring), so a node that a previous `summarize_communities()` run
    already set `title`/`summary`/`embedding` on may now be a brand new,
    empty node that merely happens to reuse the same `(id, level)` -- a
    cache *file* hit on disk does not by itself mean the *graph* still has
    the summary. Restoring here, instead of only printing the cached title
    to the table, is what makes a `detect()` + `summarize_communities()`
    replay actually free (no LLM calls) for every community whose id didn't
    change, rather than only free for the on-disk cache but silently blank
    in the graph.
    """
    run_query(
        """
        MATCH (k:Community {id: $id, level: $level})
        SET k.title = $title, k.summary = $summary, k.findings = $findings, k.rating = $rating
        WITH k
        CALL db.create.setNodeVectorProperty(k, 'embedding', $embedding)
        """,
        id=community_id, level=level,
        title=cached["title"], summary=cached["summary"],
        findings=cached["key_findings"], rating=cached["rating"],
        embedding=embed([cached["summary"]])[0],
    )


def summarize_communities(
    min_size: int = _DEFAULT_MIN_SIZE, level: int | None = None, limit: int | None = None,
    restore_only: bool = False,
) -> Table:
    """Summarise every community at `level` (defaults to the coarsest/top
    level Leiden produced -- the fewest, most thematic clusters, which is
    what a "what are the main themes" question needs) with at least
    `min_size` members. Skips communities already cached on disk (after
    restoring the cached report onto the current `Community` node, see
    `_restore_cached_report`).

    `restore_only=True` skips any community that has no cache file instead of
    calling the LLM for it -- used by the test suite to re-attach cached
    reports onto freshly-rebuilt `Community` nodes (after `detect()` reruns
    with a new, arbitrary community-id assignment) without making a single
    LLM call.
    """
    _CACHE_DIR.mkdir(parents=True, exist_ok=True)
    level = _top_level() if level is None else level
    communities = [c for c in level_sizes(level) if c["size"] >= min_size]
    if limit is not None:
        communities = communities[:limit]
    if not communities:
        raise typer.Exit(f"No communities with >= {min_size} members at level {level}.")

    table = Table(title=f"Community summaries (level {level}, min_size={min_size})")
    table.add_column("id")
    table.add_column("size")
    table.add_column("title")
    table.add_column("rating")

    for c in communities:
        cache_path = _CACHE_DIR / f"{c['id']}.json"
        if cache_path.exists():
            cached = json.loads(cache_path.read_text())
            _restore_cached_report(c["id"], level, cached)
            table.add_row(str(c["id"]), str(c["size"]), cached["title"], f"{cached['rating']:.1f}")
            continue

        if restore_only:
            continue

        report_input = _report_input(c["id"], level)
        if report_input is None:
            continue
        messages = _report_prompt(report_input)
        report: CommunityReport = chat_json(messages, CommunityReport)
        summary_embedding = embed([report.summary])[0]

        run_query(
            """
            MATCH (k:Community {id: $id, level: $level})
            SET k.title = $title, k.summary = $summary, k.findings = $findings, k.rating = $rating
            WITH k
            CALL db.create.setNodeVectorProperty(k, 'embedding', $embedding)
            """,
            id=c["id"], level=level,
            title=report.title, summary=report.summary,
            findings=report.key_findings, rating=report.rating,
            embedding=summary_embedding,
        )

        record = {
            "id": c["id"],
            "level": level,
            "size": c["size"],
            "title": report.title,
            "summary": report.summary,
            "key_findings": report.key_findings,
            "rating": report.rating,
            "summarized_at": datetime.now(timezone.utc).isoformat(),
        }
        cache_path.write_text(json.dumps(record, indent=2))
        table.add_row(str(c["id"]), str(c["size"]), report.title, f"{report.rating:.1f}")

    return table


# --- global search (map-reduce) -----------------------------------------------


class _PartialAnswer(BaseModel):
    answer: str = Field(description="Partial answer to the question, from this community's summary only, or empty if irrelevant")
    score: float = Field(ge=0, le=100, description="How relevant/useful this community's summary is to the question, 0-100")


def _candidate_communities(question: str, top_n: int, level: int) -> list[dict]:
    all_communities = run_query(
        """
        MATCH (k:Community {level: $level})
        WHERE k.summary IS NOT NULL
        RETURN k.id AS id, k.title AS title, k.summary AS summary,
               k.findings AS findings, k.rating AS rating, k.embedding AS embedding
        """,
        level=level,
    )
    if len(all_communities) <= top_n:
        return all_communities

    q_vector = embed([question])[0]

    def _cosine(a: list[float], b: list[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(y * y for y in b) ** 0.5
        return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0

    ranked = sorted(all_communities, key=lambda c: _cosine(q_vector, c["embedding"]), reverse=True)
    return ranked[:top_n]


def _map_partial_answer(question: str, community: dict) -> dict:
    findings = "\n".join(f"- {f}" for f in community["findings"] or [])
    user_content = (
        f"Community: {community['title']}\nSummary: {community['summary']}\nKey findings:\n{findings}\n\n"
        f"Question: {question}"
    )
    system = (
        "You are one of many analysts, each given a different community summary from a knowledge "
        "graph. Using ONLY the community summary and findings above, answer the question as far as "
        "this community lets you, and rate how relevant/useful your answer is from 0 (not relevant) "
        "to 100 (directly and fully answers it). If this community says nothing relevant, return an "
        "empty answer and a score of 0."
    )
    partial: _PartialAnswer = chat_json(
        [{"role": "system", "content": system}, {"role": "user", "content": user_content}],
        _PartialAnswer,
    )
    return {"id": community["id"], "title": community["title"], "answer": partial.answer, "score": partial.score}


def _reduce_partial_answers(question: str, partials: list[dict]) -> str:
    from graph_rag.llm import chat

    used = [p for p in partials if p["score"] > 0 and p["answer"].strip()]
    used.sort(key=lambda p: p["score"], reverse=True)
    if not used:
        return "not in the documents"

    blocks = "\n\n".join(f"[Community {p['id']}: {p['title']}, relevance {p['score']:.0f}] {p['answer']}" for p in used)
    system = (
        "You are combining partial answers from several communities of a knowledge graph into one "
        "final answer. Merge them, remove redundancy, prefer higher-relevance answers, and end with "
        "a line 'Communities used: <id: title, ...>' naming every community you actually drew on."
    )
    return chat(
        [
            {"role": "system", "content": system},
            {"role": "user", "content": f"Question: {question}\n\nPartial answers:\n{blocks}"},
        ]
    )


def global_search(question: str, top_n: int = 8, level: int | None = None) -> dict:
    """Map-reduce a global question over community summaries: ask every
    candidate community for a partial answer + relevance score (map), then
    merge the highest-scoring ones into a final answer (reduce). Cost is
    `len(candidates) + 1` LLM calls -- one per community, plus one merge.
    """
    level = _top_level() if level is None else level
    candidates = _candidate_communities(question, top_n, level)
    if not candidates:
        raise typer.Exit(f"No summarized communities at level {level} -- run `just communities` first.")

    partials = [_map_partial_answer(question, c) for c in candidates]
    final = _reduce_partial_answers(question, partials)
    return {"question": question, "final_answer": final, "partials": partials, "n_candidates": len(candidates)}


# --- CLI -----------------------------------------------------------------------


@app.command(name="detect")
def detect_cmd(seed: int = typer.Option(42, "--seed")) -> None:
    """Run Leiden community detection and write Community/IN_COMMUNITY (chapter 09)."""
    stats = detect(random_seed=seed)
    console.print(
        f"[green]detected {stats['community_count']} communities[/green] "
        f"(modularity={stats['modularity']:.3f}, levels={stats['ran_levels']}, top_level={stats['top_level']})"
    )


@app.command()
def summarize(
    min_size: int = typer.Option(_DEFAULT_MIN_SIZE, "--min-size"),
    level: int | None = typer.Option(None, "--level"),
    limit: int | None = typer.Option(None, "--limit"),
) -> None:
    """Summarize every community with >= min_size members (chapter 09)."""
    table = summarize_communities(min_size=min_size, level=level, limit=limit)
    console.print(table)


@app.command(name="community-stats")
def community_stats_cmd() -> None:
    """Print community counts per level and how many are flagged stale (chapter 10)."""
    rows = run_query(
        "MATCH (k:Community) RETURN k.level AS level, count(k) AS n, "
        "sum(CASE WHEN k.stale THEN 1 ELSE 0 END) AS n_stale ORDER BY level"
    )
    if not rows:
        console.print("[yellow]no communities found -- run `just communities`[/yellow]")
        return
    table = Table(title="Community counts per level")
    table.add_column("level")
    table.add_column("count")
    table.add_column("stale")
    for row in rows:
        table.add_row(str(row["level"]), str(row["n"]), str(row["n_stale"]))
    console.print(table)


@app.command()
def ask(
    question: str,
    top_n: int = typer.Option(8, "--top-n"),
    level: int | None = typer.Option(None, "--level"),
) -> None:
    """Answer a global question by map-reduce over community summaries (chapter 09)."""
    result = global_search(question, top_n=top_n, level=level)
    console.rule("partial answers")
    for p in sorted(result["partials"], key=lambda p: p["score"], reverse=True):
        console.print(f"[dim]community {p['id']} ({p['title']}) score={p['score']:.0f}[/dim] {p['answer']}")
    console.rule("final answer")
    console.print(result["final_answer"])


if __name__ == "__main__":
    app()
