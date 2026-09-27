"""Tests for chapter 06: entity resolution.

Unit tests below exercise only the normalisation/acronym functions -- no LLM,
no Neo4j -- so they run instantly and every time. The integration test needs
Docker Neo4j up (`just up`) and runs against the graph currently in it: it
does not call the LLM either, since chapter 06's `just resolve` was already
run for real and its merges are committed to the graph and to the judge
cache under `data/extracted/resolution/`.
"""

from graph_rag.db import run as run_query
from graph_rag.resolution import (
    build_acronym_map,
    candidates_by_normalization,
    resolution_key,
    strip_parenthetical,
)


def test_strip_parenthetical_drops_paren_content():
    assert strip_parenthetical("Graph-Based Indexing (G-Indexing)") == "Graph-Based Indexing"
    assert strip_parenthetical("Knowledge Graph") == "Knowledge Graph"


def test_resolution_key_ignores_case_hyphens_and_plurals():
    assert resolution_key("Knowledge Graphs") == resolution_key("Knowledge Graph")
    assert resolution_key("G-Indexing") == resolution_key("G Indexing")
    assert resolution_key("Datasets") == resolution_key("Dataset")


def test_resolution_key_collapses_parenthetical_acronym_pair():
    key_full = resolution_key("Graph-Based Indexing")
    key_paren = resolution_key("Graph-Based Indexing (G-Indexing)")
    assert key_full == key_paren


def test_build_acronym_map_expands_acronym_to_phrase_key():
    names = ["Large Language Model (LLM)", "Something else"]
    acronym_map = build_acronym_map(names)
    assert resolution_key("LLM", acronym_map) == resolution_key("Large Language Model")


def test_candidates_by_normalization_groups_acronym_and_full_name():
    entities = [
        {"name": "Graph-Based Indexing (G-Indexing)", "normalized_name": "graph-based indexing g-indexing"},
        {"name": "G-Indexing", "normalized_name": "g-indexing"},
        {"name": "Graph-Based Indexing", "normalized_name": "graph-based indexing"},
        {"name": "Unrelated Entity", "normalized_name": "unrelated entity"},
    ]
    pairs = candidates_by_normalization(entities)
    grouped_norms = {pair.a_norm for pair in pairs} | {pair.b_norm for pair in pairs}
    assert "unrelated entity" not in grouped_norms
    assert {"graph-based indexing g-indexing", "g-indexing", "graph-based indexing"} <= grouped_norms
    # 3 distinct spellings in one group -> 3 pairwise combinations
    assert len(pairs) == 3


def test_candidates_by_normalization_no_false_positive_across_groups():
    entities = [
        {"name": "Method A", "normalized_name": "method a"},
        {"name": "Method B", "normalized_name": "method b"},
    ]
    assert candidates_by_normalization(entities) == []


# --- integration: requires `just up` + `just resolve` already run ------------


def test_no_two_entities_share_an_alias_case_insensitively():
    rows = run_query(
        """
        MATCH (n:Entity) UNWIND coalesce(n.aliases, []) AS alias
        WITH toLower(alias) AS lowered_alias, collect(DISTINCT n.normalized_name) AS owners
        WHERE size(owners) > 1
        RETURN lowered_alias, owners
        """
    )
    assert rows == [], f"aliases shared across distinct entities: {rows}"


def test_no_two_entities_share_a_normalized_name():
    rows = run_query(
        "MATCH (n:Entity) WITH n.normalized_name AS nn, count(*) AS c WHERE c > 1 RETURN nn, c"
    )
    assert rows == []


def test_resolution_log_has_at_least_one_merge():
    rows = run_query("MATCH (n:ResolutionLog) RETURN count(n) AS n")
    assert rows[0]["n"] >= 1
