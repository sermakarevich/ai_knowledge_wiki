"""Tests for chapter 08: local search retrieval.

Integration only, needs Docker Neo4j up (`just up`). Runs after chapter 07's
embeddings exist (test file order follows the numeric prefix, so
`test_07_embeddings.py` has already re-embedded everything missing by the
time this file runs) -- `setup_module` re-runs the same idempotent
`embed_chunks`/`embed_entities`/`ensure_indexes` anyway, so this file does
not depend on that ordering surviving.

`retrieve_context` itself never calls the LLM (Large Language Model) --
only `hybrid_search_entities`/`search_chunks` (embedding calls). `answer()`
does call the chat model, so only one smoke test exercises it.
"""

import json
from pathlib import Path

from graph_rag.embeddings import embed_chunks, embed_entities, ensure_indexes
from graph_rag.retrieval import answer, build_context, format_context, retrieve_context

_QUESTIONS = json.loads(Path("data/questions.json").read_text())


def setup_module() -> None:
    embed_chunks()
    embed_entities()
    ensure_indexes()


def _question(qid: str) -> str:
    return next(q["question"] for q in _QUESTIONS if q["id"] == qid)


def test_retrieve_context_has_entities_triples_and_chunks_within_budget():
    max_tokens = 3000
    for qid in ("q6", "q8"):
        ctx = retrieve_context(_question(qid), max_tokens=max_tokens)
        assert len(ctx.entities) >= 1, qid
        assert len(ctx.triples) >= 1, qid
        assert len(ctx.chunks) >= 1, qid
        assert ctx.budget_used <= max_tokens, qid


def test_format_context_includes_all_three_sections():
    ctx = retrieve_context(_question("q8"))
    text = format_context(ctx)
    assert "## Entities" in text
    assert "## Relationships" in text
    assert "## Source passages" in text


def test_answer_graph_mode_cites_only_known_chunk_ids():
    question = _question("q8")
    ctx = build_context(question, "graph", k_chunks=4, max_tokens=1500)
    known_ids = {c["id"] for c in ctx.chunks}

    ans = answer(question, mode="graph", k_chunks=4, max_tokens=1500)
    assert ans.text
    assert ans.context_stats["mode"] == "graph"
    assert set(ans.citations) <= known_ids
