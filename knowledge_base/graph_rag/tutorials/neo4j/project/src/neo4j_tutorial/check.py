"""Sanity check: connect to Neo4j and print basic facts about it.

Run with: python -m neo4j_tutorial.check
"""

from neo4j_tutorial.db import get_driver


def main() -> None:
    with get_driver() as driver:
        ok = driver.execute_query("RETURN 1 AS ok", database_="neo4j").records[0]["ok"]
        print(f"ok={ok}")

        components = driver.execute_query(
            "CALL dbms.components() YIELD name, versions RETURN name, versions",
            database_="neo4j",
        ).records
        for record in components:
            print(f"{record['name']} version: {record['versions'][0]}")

        count = driver.execute_query(
            "MATCH (n) RETURN count(n) AS count", database_="neo4j"
        ).records[0]["count"]
        print(f"node count: {count}")


if __name__ == "__main__":
    main()
