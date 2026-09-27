"""End-to-end tests for the Neo4j tutorial: connectivity, loaded data,
every read query in the tutorial modules, and the transaction patterns
from chapter 05_python_patterns.md.

Run with `just test` (from `project/`).
"""

import pandas as pd
import pytest

from neo4j_tutorial import load_data, patterns, queries_advanced, queries_basic

from conftest import load_dataset

NODE_CSV_TO_LABEL = {
    "people.csv": "Person",
    "companies.csv": "Company",
    "skills.csv": "Skill",
    "cities.csv": "City",
}

REL_CSV_TO_TYPE = {
    "works_at.csv": "WORKS_AT",
    "knows.csv": "KNOWS",
    "has_skill.csv": "HAS_SKILL",
    "lives_in.csv": "LIVES_IN",
    "located_in.csv": "LOCATED_IN",
}


def _label_counts(driver) -> dict[str, int]:
    records = driver.execute_query(
        "MATCH (n) RETURN labels(n)[0] AS label, count(*) AS count",
        database_="neo4j",
    ).records
    return {r["label"]: r["count"] for r in records}


def _rel_type_counts(driver) -> dict[str, int]:
    records = driver.execute_query(
        "MATCH ()-[r]->() RETURN type(r) AS rel_type, count(*) AS count",
        database_="neo4j",
    ).records
    return {r["rel_type"]: r["count"] for r in records}


def test_connectivity(driver):
    driver.verify_connectivity()


def test_node_counts_match_csv_row_counts(driver):
    counts = _label_counts(driver)
    for csv_name, label in NODE_CSV_TO_LABEL.items():
        expected = len(load_data.read_csv(csv_name))
        assert counts[label] == expected, f"{label} count mismatch"


def test_relationship_counts_match_csv_row_counts(driver):
    counts = _rel_type_counts(driver)
    for csv_name, rel_type in REL_CSV_TO_TYPE.items():
        expected = len(load_data.read_csv(csv_name))
        assert counts[rel_type] == expected, f"{rel_type} count mismatch"


def test_loader_is_idempotent(driver):
    before_nodes = _label_counts(driver)
    before_rels = _rel_type_counts(driver)

    load_dataset(driver, reset=False)  # run again without wiping first

    assert _label_counts(driver) == before_nodes
    assert _rel_type_counts(driver) == before_rels


@pytest.mark.parametrize("name", list(queries_basic.QUERIES))
def test_basic_query_runs(name):
    df = queries_basic.run_query(name)
    assert isinstance(df, pd.DataFrame)


@pytest.mark.parametrize("name", list(queries_advanced.QUERIES))
def test_advanced_query_runs(name):
    df = queries_advanced.run_query(name)
    assert isinstance(df, pd.DataFrame)


def test_query_to_df_returns_dataframe():
    df = patterns.query_to_df("MATCH (p:Person) RETURN p.name AS name ORDER BY name LIMIT 3")
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["name"]
    assert len(df) == 3


def test_execute_read_and_write_transaction_functions(driver):
    before = patterns.count_people()
    assert before == 12

    n = patterns.add_skill("Anna Schmidt", "Rust", "beginner")
    assert n == 1

    # idempotent: running the same write again must not create a duplicate edge
    n_again = patterns.add_skill("Anna Schmidt", "Rust", "beginner")
    assert n_again == 1

    rel_count = driver.execute_query(
        "MATCH (:Person {name: 'Anna Schmidt'})-[h:HAS_SKILL]->(:Skill {name: 'Rust'}) RETURN count(h) AS n",
        database_="neo4j",
    ).records[0]["n"]
    assert rel_count == 1

    load_dataset(driver, reset=True)  # restore the original dataset


def test_explicit_transaction_rollback_leaves_counts_unchanged(driver):
    before_nodes = _label_counts(driver)

    with pytest.raises(RuntimeError):
        patterns.rename_person_explicit("Anna Schmidt", "Not Anna", fail_before_commit=True)

    still_anna = driver.execute_query(
        "MATCH (p:Person {name: 'Anna Schmidt'}) RETURN count(p) AS n",
        database_="neo4j",
    ).records[0]["n"]
    assert still_anna == 1
    assert _label_counts(driver) == before_nodes


def test_explicit_transaction_commit_applies_change(driver):
    patterns.rename_person_explicit("Marta Kaminska", "Marta K.", fail_before_commit=False)

    renamed = driver.execute_query(
        "MATCH (p:Person {name: 'Marta K.'}) RETURN count(p) AS n",
        database_="neo4j",
    ).records[0]["n"]
    assert renamed == 1

    load_dataset(driver, reset=True)  # restore the original dataset


def test_batch_write():
    rows = [{"name": f"BatchSkill{i}"} for i in range(3)]
    n = patterns.batch_write(
        rows,
        "UNWIND $rows AS row MERGE (s:Skill {name: row.name})",
        size=2,
    )
    assert n == 3

    from neo4j_tutorial.db import get_driver

    with get_driver() as driver:
        count = driver.execute_query(
            "MATCH (s:Skill) WHERE s.name STARTS WITH 'BatchSkill' RETURN count(s) AS n",
            database_="neo4j",
        ).records[0]["n"]
        assert count == 3
        driver.execute_query(
            "MATCH (s:Skill) WHERE s.name STARTS WITH 'BatchSkill' DETACH DELETE s",
            database_="neo4j",
        )
