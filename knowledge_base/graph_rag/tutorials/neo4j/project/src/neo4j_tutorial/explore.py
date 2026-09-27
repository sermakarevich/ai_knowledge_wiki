"""Every query from chapter 001_explore_database.md, in one place.

Use these when you are handed a Neo4j database you did not build, to find
out what is inside it: labels, relationship types, properties, counts,
indexes and constraints.

    python -m neo4j_tutorial.explore                 # run every query
    python -m neo4j_tutorial.explore label_rel_label  # run one query
    python -m neo4j_tutorial.explore --summary        # print describe_database()
"""

import argparse
import logging
import sys

import pandas as pd

from neo4j_tutorial.db import run

# Neo4j 5 warns that `propertyTypes` (from db.schema.*Properties) will change format in a
# future major version. It is harmless here, so keep the output clean.
logging.getLogger("neo4j.notifications").setLevel(logging.ERROR)

# name -> Cypher text. Every query is read-only.
QUERIES: dict[str, str] = {
    "labels": "CALL db.labels()",
    "relationship_types": "CALL db.relationshipTypes()",
    "property_keys": "CALL db.propertyKeys()",
    "show_databases": "SHOW DATABASES",
    "nodes_per_label": "MATCH (n) RETURN labels(n) AS labels, count(*) AS n ORDER BY n DESC",
    "rels_per_type": "MATCH ()-[r]->() RETURN type(r) AS rel, count(*) AS n ORDER BY n DESC",
    "total_nodes": "MATCH (n) RETURN count(n) AS total_nodes",
    "total_rels": "MATCH ()-[r]->() RETURN count(r) AS total_rels",
    "apoc_stats": (
        "CALL apoc.meta.stats() YIELD labelCount, relTypeCount, propertyKeyCount, nodeCount, relCount "
        "RETURN labelCount, relTypeCount, propertyKeyCount, nodeCount, relCount"
    ),
    "label_rel_label": (
        "MATCH (a)-[r]->(b) RETURN labels(a) AS from, type(r) AS rel, labels(b) AS to, count(*) AS n "
        "ORDER BY n DESC"
    ),
    "schema_visualization": "CALL db.schema.visualization()",
    "apoc_meta_schema": "CALL apoc.meta.schema() YIELD value RETURN value",
    "node_type_properties": "CALL db.schema.nodeTypeProperties()",
    "rel_type_properties": "CALL db.schema.relTypeProperties()",
    "person_keys_consistency": "MATCH (p:Person) UNWIND keys(p) AS key RETURN key, count(*) AS n ORDER BY n DESC",
    "sample_person_properties": "MATCH (p:Person) RETURN properties(p) AS props LIMIT 1",
    "distinct_industries": "MATCH (c:Company) RETURN collect(DISTINCT c.industry)[..5] AS industries",
    "age_stats": "MATCH (p:Person) RETURN min(p.age) AS min_age, max(p.age) AS max_age, avg(p.age) AS avg_age",
    "has_skill_levels": "MATCH ()-[r:HAS_SKILL]->() RETURN DISTINCT r.level AS level",
    "degree_top": "MATCH (p:Person) RETURN p.name AS name, COUNT { (p)--() } AS degree ORDER BY degree DESC LIMIT 5",
    "orphan_nodes": "MATCH (n) WHERE COUNT { (n)--() } = 0 RETURN labels(n) AS labels, count(*) AS n",
    "duplicate_names": "MATCH (p:Person) WITH p.name AS name, count(*) AS n WHERE n > 1 RETURN name, n",
    "self_loops": "MATCH (n)-[r]->(n) RETURN type(r) AS rel, count(*) AS n",
    "bidirectional_knows": (
        "MATCH (a:Person)-[:KNOWS]->(b:Person) WHERE (b)-[:KNOWS]->(a) RETURN a.name AS a, b.name AS b"
    ),
    "indexes": "SHOW INDEXES",
    "constraints": "SHOW CONSTRAINTS",
    "apoc_meta_procedures": "SHOW PROCEDURES YIELD name WHERE name STARTS WITH 'apoc.meta'",
    "dbms_components": "CALL dbms.components() YIELD name, versions, edition RETURN name, versions, edition",
}


def run_query(name: str) -> pd.DataFrame:
    """Run one named query against Neo4j and return the results as a DataFrame."""
    return pd.DataFrame(run(QUERIES[name]))


def describe_database() -> str:
    """Build a compact, human-readable summary of what is inside the database."""
    lines: list[str] = []

    lines.append("=== Node counts per label ===")
    for row in run(QUERIES["nodes_per_label"]):
        lines.append(f"  {row['labels']}: {row['n']}")

    lines.append("\n=== Relationship counts per type ===")
    for row in run(QUERIES["rels_per_type"]):
        lines.append(f"  {row['rel']}: {row['n']}")

    lines.append("\n=== Who connects to whom (label -[REL]-> label) ===")
    for row in run(QUERIES["label_rel_label"]):
        lines.append(f"  {row['from']} -[{row['rel']}]-> {row['to']}: {row['n']}")

    lines.append("\n=== Properties per label ===")
    props_by_type: dict[str, list[str]] = {}
    for row in run(QUERIES["node_type_properties"]):
        key = "/".join(row["nodeLabels"])
        props_by_type.setdefault(key, []).append(f"{row['propertyName']} ({', '.join(row['propertyTypes'])})")
    for label, props in props_by_type.items():
        lines.append(f"  {label}: {', '.join(props)}")

    lines.append("\n=== Properties per relationship type ===")
    rel_props_by_type: dict[str, list[str]] = {}
    for row in run(QUERIES["rel_type_properties"]):
        if row["propertyName"] is None:
            continue
        rel_props_by_type.setdefault(row["relType"], []).append(
            f"{row['propertyName']} ({', '.join(row['propertyTypes'])})"
        )
    for rel_type, props in rel_props_by_type.items():
        lines.append(f"  {rel_type}: {', '.join(props)}")

    lines.append("\n=== Indexes ===")
    for row in run(QUERIES["indexes"]):
        lines.append(f"  {row['name']} ({row['type']}) on {row['labelsOrTypes']} {row['properties']}")

    lines.append("\n=== Constraints ===")
    for row in run(QUERIES["constraints"]):
        lines.append(f"  {row['name']} ({row['type']}) on {row['labelsOrTypes']} {row['properties']}")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("name", nargs="?", default=None, help="query name to run; omit to run all")
    parser.add_argument("--summary", action="store_true", help="print describe_database() instead")
    args = parser.parse_args()

    if args.summary:
        print(describe_database())
        return

    names = [args.name] if args.name else list(QUERIES)
    for name in names:
        if name not in QUERIES:
            print(f"unknown query: {name}", file=sys.stderr)
            sys.exit(1)
        print(f"\n=== {name} ===")
        print(f"{QUERIES[name]}\n")
        print(run_query(name))


if __name__ == "__main__":
    main()
