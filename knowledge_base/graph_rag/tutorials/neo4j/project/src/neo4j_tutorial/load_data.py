"""Load the tutorial CSV dataset into Neo4j.

Run with: python -m neo4j_tutorial.load_data [--reset]

Safe to run more than once: every write uses MERGE (find-or-create), so
re-running never creates duplicate nodes or relationships.
"""

import argparse
import csv
from itertools import islice
from pathlib import Path
from typing import Iterable, Iterator

from neo4j_tutorial.db import get_driver

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

CONSTRAINTS = [
    "CREATE CONSTRAINT person_name IF NOT EXISTS FOR (p:Person) REQUIRE p.name IS UNIQUE",
    "CREATE CONSTRAINT company_name IF NOT EXISTS FOR (c:Company) REQUIRE c.name IS UNIQUE",
    "CREATE CONSTRAINT skill_name IF NOT EXISTS FOR (s:Skill) REQUIRE s.name IS UNIQUE",
    "CREATE CONSTRAINT city_name IF NOT EXISTS FOR (ci:City) REQUIRE ci.name IS UNIQUE",
]

INT_FIELDS = {"age", "founded", "since"}


def batched(rows: list[dict], size: int = 500) -> Iterator[list[dict]]:
    """Split a list of rows into chunks of at most `size` rows each."""
    it = iter(rows)
    while chunk := list(islice(it, size)):
        yield chunk


def read_csv(name: str) -> list[dict]:
    """Read a CSV file from data/ and cast known integer fields."""
    with open(DATA_DIR / name, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        for field in INT_FIELDS:
            if field in row:
                row[field] = int(row[field])
    return rows


NODE_QUERIES = {
    "people.csv": (
        "UNWIND $rows AS row "
        "MERGE (p:Person {name: row.name}) "
        "SET p.age = row.age"
    ),
    "companies.csv": (
        "UNWIND $rows AS row "
        "MERGE (c:Company {name: row.name}) "
        "SET c.industry = row.industry, c.founded = row.founded"
    ),
    "skills.csv": (
        "UNWIND $rows AS row "
        "MERGE (s:Skill {name: row.name})"
    ),
    "cities.csv": (
        "UNWIND $rows AS row "
        "MERGE (ci:City {name: row.name}) "
        "SET ci.country = row.country"
    ),
}

REL_QUERIES = {
    "works_at.csv": (
        "UNWIND $rows AS row "
        "MATCH (p:Person {name: row.person}) "
        "MATCH (c:Company {name: row.company}) "
        "MERGE (p)-[w:WORKS_AT]->(c) "
        "SET w.since = row.since, w.role = row.role"
    ),
    "knows.csv": (
        "UNWIND $rows AS row "
        "MATCH (p1:Person {name: row.person1}) "
        "MATCH (p2:Person {name: row.person2}) "
        "MERGE (p1)-[k:KNOWS]->(p2) "
        "SET k.since = row.since"
    ),
    "has_skill.csv": (
        "UNWIND $rows AS row "
        "MATCH (p:Person {name: row.person}) "
        "MATCH (s:Skill {name: row.skill}) "
        "MERGE (p)-[h:HAS_SKILL]->(s) "
        "SET h.level = row.level"
    ),
    "lives_in.csv": (
        "UNWIND $rows AS row "
        "MATCH (p:Person {name: row.person}) "
        "MATCH (ci:City {name: row.city}) "
        "MERGE (p)-[l:LIVES_IN]->(ci)"
    ),
    "located_in.csv": (
        "UNWIND $rows AS row "
        "MATCH (c:Company {name: row.company}) "
        "MATCH (ci:City {name: row.city}) "
        "MERGE (c)-[l:LOCATED_IN]->(ci)"
    ),
}


def load_file(driver, csv_name: str, query: str) -> int:
    rows = read_csv(csv_name)
    for chunk in batched(rows):
        driver.execute_query(query, rows=chunk, database_="neo4j")
    return len(rows)


def print_counts(driver) -> None:
    print("\nNode counts:")
    for row in driver.execute_query(
        "MATCH (n) RETURN labels(n)[0] AS label, count(*) AS count ORDER BY label",
        database_="neo4j",
    ).records:
        print(f"  {row['label']}: {row['count']}")

    print("\nRelationship counts:")
    for row in driver.execute_query(
        "MATCH ()-[r]->() RETURN type(r) AS rel_type, count(*) AS count ORDER BY rel_type",
        database_="neo4j",
    ).records:
        print(f"  {row['rel_type']}: {row['count']}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="delete all nodes/relationships first")
    args = parser.parse_args()

    with get_driver() as driver:
        if args.reset:
            driver.execute_query("MATCH (n) DETACH DELETE n", database_="neo4j")
            print("reset: all nodes and relationships deleted")

        for constraint in CONSTRAINTS:
            driver.execute_query(constraint, database_="neo4j")
        print(f"ensured {len(CONSTRAINTS)} uniqueness constraints")

        for csv_name, query in NODE_QUERIES.items():
            n = load_file(driver, csv_name, query)
            print(f"loaded {n} rows from {csv_name}")

        for csv_name, query in REL_QUERIES.items():
            n = load_file(driver, csv_name, query)
            print(f"loaded {n} rows from {csv_name}")

        print_counts(driver)


if __name__ == "__main__":
    main()
