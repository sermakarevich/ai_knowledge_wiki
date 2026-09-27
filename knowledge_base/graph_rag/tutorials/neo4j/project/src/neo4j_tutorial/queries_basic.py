"""Every read query from chapter 03_basic_queries.md, in one place.

Run one query, or all of them, and see the results as a pandas DataFrame:

    python -m neo4j_tutorial.queries_basic                      # run every query
    python -m neo4j_tutorial.queries_basic people_per_company   # run one query
"""

import argparse
import sys

import pandas as pd

from neo4j_tutorial.db import get_driver

# name -> Cypher text. Every query is read-only (MATCH/OPTIONAL MATCH/UNWIND/RETURN).
QUERIES: dict[str, str] = {
    "return_star": "MATCH (p:Person) RETURN * LIMIT 3",
    "aliases": "MATCH (p:Person) RETURN p.name AS name, p.age AS age ORDER BY name LIMIT 5",
    "distinct_industries": "MATCH (c:Company) RETURN DISTINCT c.industry AS industry",
    "filter_inline_property": "MATCH (p:Person {name: 'Anna Schmidt'}) RETURN p.name AS name, p.age AS age",
    "filter_where": "MATCH (p:Person) WHERE p.age > 35 RETURN p.name AS name, p.age AS age ORDER BY p.age",
    "filter_and_not": (
        "MATCH (p:Person) WHERE p.age > 30 AND NOT p.name STARTS WITH 'A' "
        "RETURN p.name AS name, p.age AS age ORDER BY p.name"
    ),
    "filter_in": "MATCH (c:Company) WHERE c.industry IN ['Software', 'AI Research'] RETURN c.name AS name, c.industry AS industry",
    "filter_string_predicates": (
        "MATCH (p:Person) WHERE p.name CONTAINS 'll' OR p.name ENDS WITH 'ski' "
        "RETURN p.name AS name ORDER BY name"
    ),
    "filter_regex": "MATCH (p:Person) WHERE p.name =~ 'A.*' RETURN p.name AS name ORDER BY name",
    "filter_label_predicate": "MATCH (n) WHERE n:Person RETURN count(n) AS people",
    "rel_type_alternatives": (
        "MATCH (p:Person)-[r:KNOWS|WORKS_AT]->(x) "
        "RETURN p.name AS person, type(r) AS rel_type, coalesce(x.name) AS other ORDER BY person, rel_type LIMIT 8"
    ),
    "relationship_direction": "MATCH (p:Person)-[:WORKS_AT]->(c:Company) RETURN p.name AS person, c.name AS company ORDER BY person LIMIT 5",
    "relationship_variable_props": (
        "MATCH (p:Person)-[w:WORKS_AT]->(c:Company) "
        "RETURN p.name AS person, w.role AS role, type(w) AS rel_type ORDER BY person LIMIT 5"
    ),
    "labels_id_properties": (
        "MATCH (p:Person {name: 'Anna Schmidt'}) "
        "RETURN labels(p) AS labels, elementId(p) AS element_id, properties(p) AS props"
    ),
    "order_skip_limit": "MATCH (p:Person) RETURN p.name AS name, p.age AS age ORDER BY p.age DESC SKIP 2 LIMIT 3",
    "count_star_vs_count_x": (
        "MATCH (p:Person) OPTIONAL MATCH (p)-[:LIVES_IN]->(ci:City {name: 'Austin'}) "
        "RETURN count(p) as p, count(*) AS rows, count(ci) AS non_null_cities"
    ),
    "collect_skills_per_person": (
        "MATCH (p:Person)-[:HAS_SKILL]->(s:Skill) "
        "RETURN p.name AS person, collect(s.name) AS skills ORDER BY person"
    ),
    "age_aggregates": "MATCH (p:Person) RETURN avg(p.age) AS avg_age, min(p.age) AS min_age, max(p.age) AS max_age, sum(p.age) AS total_age",
    "people_per_company": (
        "MATCH (p:Person)-[:WORKS_AT]->(c:Company) "
        "RETURN c.name AS company, count(p) AS people ORDER BY people DESC"
    ),
    "people_per_company2": (
        "MATCH (p:Person)-[:WORKS_AT]->(c:Company) "
        "RETURN c.name AS company, collect(p.name) AS people ORDER BY people DESC"
    ),
    "avg_age_per_city": (
        "MATCH (p:Person)-[:LIVES_IN]->(ci:City) "
        "RETURN ci.name AS city, avg(p.age) AS avg_age ORDER BY city"
    ),
    "with_filter_after_agg": (
        "MATCH (p:Person)-[:HAS_SKILL]->(s:Skill) "
        "WITH s, count(p) AS n WHERE n > 2 "
        "RETURN s.name AS skill, n AS people ORDER BY n DESC"
    ),
    "with_filter_after_agg2": (
        "MATCH (p:Person)-[:HAS_SKILL]->(s:Skill) "
        "WITH s, count(p) AS n WHERE n > 2 "
        "WITH * WHERE n > 3 "
        "RETURN s.name AS skill, n AS people ORDER BY n DESC"
    ),
    "with_top_skill": (
        "MATCH (p:Person)-[:HAS_SKILL]->(s:Skill) "
        "WITH s, count(p) AS n ORDER BY n DESC LIMIT 2 "
        "RETURN s.name AS skill, n AS people"
    ),
    "with_top_skill2": (
        "MATCH (p:Person)-[:HAS_SKILL]->(s:Skill) "
        "RETURN s.name AS skill, count(p) AS people ORDER BY people DESC LIMIT 2"
    ),
    "optional_match_city": (
        "MATCH (p:Person) OPTIONAL MATCH (p)-[:LIVES_IN]->(ci:City) "
        "RETURN p.name AS person, ci.name AS city ORDER BY person"
    ),
    "match_city": (
        "MATCH (p:Person) MATCH (p)-[:LIVES_IN]->(ci:City) "
        "RETURN p.name AS person, ci.name AS city ORDER BY person"
    ),
    "person_with_no_knows": (
        "MATCH (p:Person) OPTIONAL MATCH (p)-[k:KNOWS]-() "
        "WITH p, count(k) AS n WHERE n = 0 "
        "RETURN p.name AS person, n"
    ),
    "unwind_expand_list": (
        "WITH ['Python', 'Docker'] AS wanted UNWIND wanted AS skill "
        "MATCH (p:Person)-[:HAS_SKILL]->(s:Skill {name: skill}) "
        "RETURN skill, p.name AS person ORDER BY skill, person"
    ),
    "unwind_expand_list2": (
        "MATCH (p:Person)-[:HAS_SKILL]->(s:Skill) "
        "WHERE s.name in ['Python', 'Docker'] "
        "RETURN s.name as skill, p.name AS person ORDER BY s.name, p.name"
    ),
    "case_preview": (
        "MATCH (p:Person) RETURN p.name AS name, p.age AS age, "
        "CASE WHEN p.age < 30 THEN 'junior' WHEN p.age < 45 THEN 'mid' ELSE 'senior' END AS band "
        "ORDER BY p.age"
    ),
    "parameterized_lookup": "MATCH (p:Person {name: $name}) RETURN p.name AS name, p.age AS age",
}

# Default parameter values used when a query needs them and none are given on the CLI.
DEFAULT_PARAMS: dict[str, dict] = {
    "parameterized_lookup": {"name": "Anna Schmidt"},
}


def run_query(name: str) -> pd.DataFrame:
    """Run one named query against Neo4j and return the results as a DataFrame."""
    query = QUERIES[name]
    params = DEFAULT_PARAMS.get(name, {})
    with get_driver() as driver:
        result = driver.execute_query(query, params, database_="neo4j")
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
