"""Every read-only query from chapter 04_advanced_queries.md, in one place.

Write examples (SET, DELETE, MERGE, FOREACH, index creation, ...) are NOT
here on purpose -- they live only in the chapter text, each followed by the
statement that undoes it. This module only holds queries that are safe to
run any number of times without changing the database.

Run one query, or all of them, and see the results as a pandas DataFrame:

    python -m neo4j_tutorial.queries_advanced                      # run every query
    python -m neo4j_tutorial.queries_advanced shortest_path_knows  # run one query
"""

import argparse
import sys

import pandas as pd

from neo4j_tutorial.db import get_driver

# name -> Cypher text. Every query here is read-only.
QUERIES: dict[str, str] = {
    "variable_length_1_3": (
        "MATCH p = (a:Person {name: 'Anna Schmidt'})-[:KNOWS*1..3]->(b:Person) "
        "RETURN b.name AS name, length(p) AS len ORDER BY len, name"
    ),
    "path_nodes_and_relationships": (
        "MATCH p = (a:Person {name: 'Anna Schmidt'})-[:KNOWS*1..3]->(b:Person) "
        "WHERE b.name = 'Tom Becker' "
        "RETURN [x IN nodes(p) | x.name] AS names, size(relationships(p)) AS nrels"
    ),
    "path_nodes_and_relationships2": (
        "MATCH p = (a:Person {name: 'Anna Schmidt'})-[:KNOWS*1..3]->(b:Person {name: 'Tom Becker'}) "
        "RETURN [x IN nodes(p) | x.name] AS names, size(relationships(p)) AS nrels"
    ),
    "path_nodes_and_relationships3": (
        "MATCH p = (a:Person {name: 'Anna Schmidt'})-[:KNOWS*1..3]->(b:Person {name: 'Tom Becker'}) "
        "WITH nodes(p) as z, size(relationships(p)) AS nrels "
        "UNWIND (z) as x "
        "RETURN collect(x.name), nrels"
    ),
    "friends_of_friends_not_direct": (
        "MATCH (a:Person {name: 'Anna Schmidt'})-[:KNOWS]-()-[:KNOWS]-(fof:Person) "
        "WHERE fof <> a AND NOT (a)-[:KNOWS]-(fof) "
        "RETURN DISTINCT fof.name AS friend_of_friend ORDER BY friend_of_friend"
    ),
    "friends_of_friends_not_direct2": (
        "MATCH (a:Person)-[:KNOWS]->()-[:KNOWS]->(fof:Person) "
        "WHERE fof <> a AND NOT (a)-[:KNOWS]-(fof) "
        "RETURN DISTINCT a.name, fof.name AS friend_of_friend ORDER BY friend_of_friend"
    ),
    "shortest_path_knows": (
        "MATCH (a:Person {name: 'Anna Schmidt'}), (b:Person {name: 'Tom Becker'}), "
        "p = shortestPath((a)-[:KNOWS*]-(b)) "
        "RETURN [x IN nodes(p) | x.name] AS path, size(relationships(p)) AS hops"
    ),
    "all_shortest_paths_knows": (
        "MATCH (a:Person {name: 'Anna Schmidt'}), (b:Person {name: 'Nina Wagner'}), "
        "p = allShortestPaths((a)-[:KNOWS*]-(b)) "
        "RETURN [x IN nodes(p) | x.name] AS path, size(relationships(p)) AS hops"
    ),
    "shortest_quantified_path_pattern": (
        "MATCH p = SHORTEST 1 (a:Person {name: 'Anna Schmidt'})-[:KNOWS]-{1,5}(b:Person {name: 'Tom Becker'}) "
        "RETURN [x IN nodes(p) | x.name] AS path"
    ),
    "list_comprehension_filter_map": "RETURN [x IN range(1, 10) WHERE x % 2 = 0 | x * x] AS squares",
    "reduce_join_skills": (
        "MATCH (p:Person)-[:HAS_SKILL]->(s:Skill) WITH p, collect(s.name) AS skills "
        "RETURN p.name AS person, reduce(acc = '', name IN skills | acc + name + ',') AS joined "
        "ORDER BY person LIMIT 3"
    ),
    "reduce_join_skills2": (
        "MATCH (p:Person)-[:HAS_SKILL]->(s:Skill) WITH p, collect(s.name) AS skills "
        "RETURN p.name AS person, reduce(acc = '', name IN skills | CASE WHEN acc = '' THEN name ELSE acc + ', ' + name END) AS joined "
        "ORDER BY person LIMIT 3"
    ),
    "size_and_range": "RETURN size(range(0, 20, 5)) AS n, range(0, 20, 5) AS r",
    "head_last_tail": "WITH [1, 2, 3, 4, 5] AS xs RETURN head(xs) AS h, last(xs) AS l, tail(xs) AS t",
    "coalesce_missing_property": "MATCH (p:Person) RETURN p.name AS name, coalesce(p.nickname, p.name) AS display LIMIT 3",
    "map_projection": "MATCH (p:Person)-[:WORKS_AT]->(c:Company) RETURN p {.name, .age, company: c.name} AS person LIMIT 3",
    "pattern_comprehension_skills": (
        "MATCH (p:Person) RETURN p.name AS name, [(p)-[:HAS_SKILL]->(s) | s.name] AS skills "
        "ORDER BY name LIMIT 30"
    ),
    "case_simple": (
        "MATCH (p:Person) RETURN p.name AS name, "
        "CASE p.age WHEN 24 THEN 'youngest' WHEN 50 THEN 'oldest' ELSE 'other' END AS tag "
        "ORDER BY name LIMIT 4"
    ),
    "case_generic_age_band": (
        "MATCH (p:Person) RETURN p.name AS name, p.age AS age, "
        "CASE WHEN p.age < 30 THEN 'junior' WHEN p.age < 45 THEN 'mid' ELSE 'senior' END AS band "
        "ORDER BY p.age"
    ),
    "union_young_or_old": (
        "MATCH (p:Person) WHERE p.age < 27 RETURN p.name AS name, 'young' as type "
        "UNION "
        "MATCH (p:Person) WHERE p.age > 45 RETURN p.name AS name, 'old' as type "
    ),
    "union_all_duplicates_allowed": (
        "MATCH (p:Person)-[:WORKS_AT]->(c:Company {name: 'GraphWorks'}) RETURN c.name AS org "
        "UNION ALL "
        "MATCH (c:Company {name: 'GraphWorks'}) RETURN c.name AS org"
    ),
    "exists_subquery": (
        "MATCH (p:Person) WHERE EXISTS { (p)-[:HAS_SKILL]->(:Skill {name: 'Python'}) } "
        "RETURN p.name AS name, [(p) - [] -> (s: Skill) | s.name] ORDER BY name"
    ),
    "count_subquery": (
        "MATCH (p:Person) WHERE COUNT { (p)-[:HAS_SKILL]->() } >= 2 "
        "RETURN p.name AS name, COUNT { (p)-[:HAS_SKILL]->() } AS n_skills ORDER BY name"
    ),
    "collect_subquery": (
        "MATCH (p:Person) RETURN p.name AS name, "
        "COLLECT { MATCH (p)-[:HAS_SKILL]->(s) RETURN s.name } AS skills "
        "ORDER BY name LIMIT 3"
    ),
    "call_subquery_top_skills_per_person": (
        "MATCH (p:Person) CALL (p) { "
        "MATCH (p)-[h:HAS_SKILL]->(s:Skill) RETURN s.name AS skill ORDER BY h.level DESC, s.name LIMIT 2 "
        "} RETURN p.name AS person, collect(skill) AS top_skills ORDER BY person"
    ),
    "apoc_meta_stats": "CALL apoc.meta.stats() YIELD nodeCount, relCount, labels RETURN nodeCount, relCount, labels",
    "apoc_subgraph_nodes": (
        "MATCH (a:Person {name: 'Anna Schmidt'}) "
        "CALL apoc.path.subgraphNodes(a, {relationshipFilter: 'KNOWS', maxLevel: 2}) YIELD node "
        "RETURN node.name AS name ORDER BY name"
    ),
    "apoc_help_lookup": "CALL apoc.help('path.subgraphNodes') YIELD name, text RETURN name, text LIMIT 1",
    "fulltext_search_names": (
        "CALL db.index.fulltext.queryNodes('person_names', 'ann~') YIELD node, score "
        "RETURN node.name AS name, score ORDER BY score DESC"
    ),
    "show_indexes": "SHOW INDEXES YIELD name, type, entityType, labelsOrTypes, properties RETURN name, type, entityType, labelsOrTypes, properties ORDER BY name",
}


def run_query(name: str) -> pd.DataFrame:
    """Run one named query against Neo4j and return the results as a DataFrame."""
    query = QUERIES[name]
    with get_driver() as driver:
        result = driver.execute_query(query, database_="neo4j")
        return pd.DataFrame([record.data() for record in result.records])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("name", nargs="?", default=None, help="query name to run; omit to run all")
    args = parser.parse_args()

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
