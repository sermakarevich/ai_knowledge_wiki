"""Chapter 08: local search -- turn a question into a graph-grounded answer.

Chapters 02-07 built the lexical graph (`Document`/`Chunk`), the domain graph
(`Entity` + typed relationships), and vector/full-text search over both. This
module is where retrieval finally answers a question:

  1. `retrieve_context` -- hybrid-search entities (chapter 07) as seeds, expand
     one or two hops through the domain graph with Cypher, collect the chunks
     that back up every triple, and trim everything to a token budget.
  2. `format_context` -- render a `Context` into the plain-text block the LLM
     (Large Language Model) prompt is built from.
  3. `answer` -- ask the LLM to answer only from that context, citing
     `[chunk_id]` after every claim; `mode="vector"` is the plain-RAG baseline
     (top-k chunks, no graph), `mode="both"` runs both for comparison.

Run with: python -m graph_rag.retrieval ask "<question>" [--mode graph|vector|both] [--show-context]
"""

from dataclasses import dataclass, field

import typer
from rich.console import Console

from graph_rag.db import run as run_query
from graph_rag.embeddings import hybrid_search_entities, search_chunks
from graph_rag.llm import chat

app = typer.Typer(add_completion=False)
console = Console()

_CHARS_PER_TOKEN = 4  # rough estimate -- no tokenizer dependency for a token budget check
_MAX_HOP2_SEEDS = 5  # cap how many hop-1 neighbours get expanded again
_MAX_TRIPLES = 60  # cap total triples before ranking/trimming


@dataclass
class Context:
    entities: list[dict]
    triples: list[dict]
    chunks: list[dict]
    budget_used: int


@dataclass
class Answer:
    text: str
    citations: list[str]
    context_stats: dict = field(default_factory=dict)


# --- graph expansion ---------------------------------------------------------


def _expand_one_hop(seed_names: list[str], exclude: set[tuple] | None = None) -> list[dict]:
    """One Cypher hop out from `seed_names`: every non-`MENTIONS` relationship
    touching a seed, in either direction. `startNode(r) = e` recovers the
    real direction (Cypher's `(e)-[r]-(n)` matches both ways), so the
    returned `subject`/`object` always read in the relationship's actual
    direction, never flipped by which side happened to match `e`.
    """
    rows = run_query(
        """
        MATCH (e:Entity)-[r]-(n:Entity)
        WHERE e.normalized_name IN $seeds AND type(r) <> 'MENTIONS'
        WITH e, r, n, startNode(r) = e AS e_is_source
        RETURN
            CASE WHEN e_is_source THEN e.name ELSE n.name END AS subject,
            CASE WHEN e_is_source THEN e.normalized_name ELSE n.normalized_name END AS subject_key,
            type(r) AS rel,
            CASE WHEN e_is_source THEN n.name ELSE e.name END AS object,
            CASE WHEN e_is_source THEN n.normalized_name ELSE e.normalized_name END AS object_key,
            r.description AS description,
            coalesce(r.weight, 1.0) AS weight,
            coalesce(r.chunk_ids, []) AS chunk_ids
        """,
        seeds=seed_names,
    )
    if exclude:
        rows = [r for r in rows if (r["subject_key"], r["rel"], r["object_key"]) not in exclude]
    return rows


def _rank_triples(triples: list[dict], seed_set: set[str]) -> list[dict]:
    """Rank by (a) how many of the triple's two endpoints are seeds -- a
    triple connecting two seeds is stronger evidence than one connecting a
    seed to an unrelated neighbour -- then (b) the extraction's own `weight`.
    """
    for t in triples:
        t["seed_touches"] = (t["subject_key"] in seed_set) + (t["object_key"] in seed_set)
    return sorted(triples, key=lambda t: (t["seed_touches"], t["weight"]), reverse=True)


def _dedupe_triples(triples: list[dict]) -> list[dict]:
    seen: set[tuple] = set()
    out = []
    for t in triples:
        key = (t["subject_key"], t["rel"], t["object_key"])
        if key not in seen:
            seen.add(key)
            out.append(t)
    return out


def retrieve_context(
    question: str,
    k_entities: int = 8,
    hops: int = 1,
    k_chunks: int = 6,
    max_tokens: int = 3000,
) -> Context:
    """Seed with hybrid entity search (chapter 07), expand `hops` hops through
    the domain graph, collect provenance chunks, and trim to `max_tokens`.
    """
    seeds = hybrid_search_entities(question, k=k_entities)
    seed_names = [s["normalized_name"] for s in seeds]
    seed_set = set(seed_names)

    triples = _expand_one_hop(seed_names)
    seen_keys = {(t["subject_key"], t["rel"], t["object_key"]) for t in triples}

    if hops >= 2:
        # Only expand further from the strongest hop-1 neighbours, capped,
        # so a densely connected seed can't blow up the neighbourhood.
        hop1_ranked = _rank_triples(list(triples), seed_set)
        hop2_seeds = []
        for t in hop1_ranked:
            for key in (t["subject_key"], t["object_key"]):
                if key not in seed_set and key not in hop2_seeds:
                    hop2_seeds.append(key)
            if len(hop2_seeds) >= _MAX_HOP2_SEEDS:
                break
        if hop2_seeds:
            triples += _expand_one_hop(hop2_seeds, exclude=seen_keys)

    triples = _dedupe_triples(triples)
    triples = _rank_triples(triples, seed_set)[:_MAX_TRIPLES]

    chunks = _collect_chunks(question, seed_names, triples, k_chunks)
    chunks, budget_used = _trim_to_budget(chunks, max_tokens)

    entities = [{"name": s["name"], "normalized_name": s["normalized_name"], "type": s.get("type")} for s in seeds]
    return Context(entities=entities, triples=triples, chunks=chunks, budget_used=budget_used)


def _collect_chunks(question: str, seed_names: list[str], triples: list[dict], k_chunks: int) -> list[dict]:
    """Provenance chunks, ranked: chunks a selected triple/mention actually
    cites outrank chunks that only look topically similar -- if the graph
    found a specific relationship, the chunk that stated it is the best
    evidence, better than a vector hit that merely mentions the same topic.
    """
    triple_chunk_ids = {cid for t in triples for cid in t["chunk_ids"]}

    mention_rows = run_query(
        """
        MATCH (c:Chunk)-[:MENTIONS]->(e:Entity)
        WHERE e.normalized_name IN $seeds
        RETURN DISTINCT c.id AS id, c.text AS text
        """,
        seeds=seed_names,
    )
    mention_ids = {r["id"] for r in mention_rows}

    vector_hits = search_chunks(question, k=k_chunks)

    by_id: dict[str, dict] = {}
    for hit in vector_hits:
        by_id[hit["id"]] = {"id": hit["id"], "text": hit["text"], "score": hit["score"]}
    for row in mention_rows:
        by_id.setdefault(row["id"], {"id": row["id"], "text": row["text"], "score": 0.0})
    if triple_chunk_ids - by_id.keys():
        rows = run_query(
            "MATCH (c:Chunk) WHERE c.id IN $ids RETURN c.id AS id, c.text AS text",
            ids=list(triple_chunk_ids - by_id.keys()),
        )
        for row in rows:
            by_id.setdefault(row["id"], {"id": row["id"], "text": row["text"], "score": 0.0})

    def _rank_key(c: dict) -> tuple:
        return (c["id"] in triple_chunk_ids, c["id"] in mention_ids, c["score"])

    return sorted(by_id.values(), key=_rank_key, reverse=True)


def _trim_to_budget(chunks: list[dict], max_tokens: int) -> tuple[list[dict], int]:
    kept = []
    used = 0
    for c in chunks:
        cost = max(1, len(c["text"]) // _CHARS_PER_TOKEN)
        if used + cost > max_tokens:
            break
        kept.append(c)
        used += cost
    return kept, used


# --- context formatting -------------------------------------------------------


def format_context(ctx: Context) -> str:
    lines = ["## Entities"]
    for e in ctx.entities:
        lines.append(f"- {e['name']} ({e.get('type') or 'Entity'})")

    lines.append("\n## Relationships")
    for t in ctx.triples:
        cids = ",".join(t["chunk_ids"]) if t["chunk_ids"] else "?"
        raw_desc = t.get("description")
        # `graph_writer` merges parallel duplicate relationships (chapter 05),
        # which can turn `description` into a list of the merged strings.
        desc_text = "; ".join(raw_desc) if isinstance(raw_desc, list) else raw_desc
        desc = f" -- {desc_text}" if desc_text else ""
        lines.append(f"- {t['subject']} -> {t['rel']} -> {t['object']}{desc} [source chunk ids: {cids}]")

    lines.append("\n## Source passages")
    for c in ctx.chunks:
        lines.append(f"[{c['id']}] {c['text']}")

    return "\n".join(lines)


# --- answering -----------------------------------------------------------------

_SYSTEM_PROMPT = """You are answering a question using only the context below, taken from a \
research paper's knowledge graph and passages. Answer only from the context. \
Each passage in "Source passages" starts with its own id in square brackets, e.g. "[abc123:4] some text" \
-- after every claim, copy that exact bracketed id from the passage it came from, verbatim, \
do not invent or reformat an id (never write things like [chunk_1] or [chunk_003]). \
If the context does not support an answer, say "not in the documents" instead of guessing."""


def _build_vector_context(question: str, k_chunks: int, max_tokens: int) -> Context:
    chunks = [{"id": h["id"], "text": h["text"], "score": h["score"]} for h in search_chunks(question, k=k_chunks)]
    chunks, budget_used = _trim_to_budget(chunks, max_tokens)
    return Context(entities=[], triples=[], chunks=chunks, budget_used=budget_used)


def build_context(
    question: str,
    mode: str,
    k_entities: int = 8,
    hops: int = 1,
    k_chunks: int = 6,
    max_tokens: int = 3000,
) -> Context:
    if mode == "vector":
        return _build_vector_context(question, k_chunks, max_tokens)
    return retrieve_context(question, k_entities=k_entities, hops=hops, k_chunks=k_chunks, max_tokens=max_tokens)


def answer(
    question: str,
    mode: str = "graph",
    k_entities: int = 8,
    hops: int = 1,
    k_chunks: int = 6,
    max_tokens: int = 3000,
) -> Answer | dict[str, Answer]:
    """Answer `question` from graph context, vector-only context, or both.

    `mode="both"` returns `{"graph": Answer, "vector": Answer}` for a
    side-by-side comparison -- it makes two separate LLM calls, one per mode,
    each grounded only in its own context.
    """
    if mode == "both":
        return {
            "graph": answer(question, "graph", k_entities, hops, k_chunks, max_tokens),
            "vector": answer(question, "vector", k_entities, hops, k_chunks, max_tokens),
        }

    ctx = build_context(question, mode, k_entities, hops, k_chunks, max_tokens)
    prompt = format_context(ctx)
    text = chat(
        [
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{prompt}\n\nQuestion: {question}"},
        ]
    )

    known_ids = {c["id"] for c in ctx.chunks}
    citations = _extract_citations(text, known_ids)
    stats = {
        "mode": mode,
        "n_entities": len(ctx.entities),
        "n_triples": len(ctx.triples),
        "n_chunks": len(ctx.chunks),
        "budget_used": ctx.budget_used,
    }
    return Answer(text=text, citations=citations, context_stats=stats)


def _extract_citations(text: str, known_ids: set[str]) -> list[str]:
    import re

    found = re.findall(r"\[([a-zA-Z0-9_\-:]+)\]", text)
    ordered: list[str] = []
    for cid in found:
        if cid in known_ids and cid not in ordered:
            ordered.append(cid)
    return ordered


# --- CLI -----------------------------------------------------------------------


@app.command()
def ask(
    question: str,
    mode: str = typer.Option("graph", "--mode", help="graph|vector|both"),
    k_entities: int = typer.Option(8, "--k-entities"),
    hops: int = typer.Option(1, "--hops"),
    k_chunks: int = typer.Option(6, "--k-chunks"),
    max_tokens: int = typer.Option(3000, "--max-tokens"),
    show_context: bool = typer.Option(False, "--show-context"),
) -> None:
    """Ask a question, print the answer (and citations), one or both modes."""
    modes = ["graph", "vector"] if mode == "both" else [mode]

    if show_context:
        for m in modes:
            ctx = build_context(question, m, k_entities, hops, k_chunks, max_tokens)
            console.rule(f"context ({m})")
            console.print(format_context(ctx))

    result = answer(question, mode=mode, k_entities=k_entities, hops=hops, k_chunks=k_chunks, max_tokens=max_tokens)
    results = result if isinstance(result, dict) else {mode: result}
    for m, ans in results.items():
        console.rule(f"answer ({m})")
        console.print(ans.text)
        console.print(f"[dim]citations: {ans.citations}[/dim]")
        console.print(f"[dim]context: {ans.context_stats}[/dim]")


@app.command()
def batch(
    mode: str = typer.Option("graph", "--mode", help="graph|vector|both"),
    questions_path: str = typer.Option("data/questions.json", "--questions"),
) -> None:
    """Answer every question in `data/questions.json` (chapter 08/10's shared
    evaluation set) and print a one-line-per-question summary.
    """
    import json
    from pathlib import Path

    questions = json.loads(Path(questions_path).read_text())
    for q in questions:
        result = answer(q["question"], mode=mode)
        results = result if isinstance(result, dict) else {mode: result}
        console.rule(f"{q['id']} ({q['type']}): {q['question']}")
        for m, ans in results.items():
            console.print(f"[bold]{m}[/bold]: {ans.text}")
            console.print(f"[dim]citations: {ans.citations}[/dim]")


if __name__ == "__main__":
    app()
