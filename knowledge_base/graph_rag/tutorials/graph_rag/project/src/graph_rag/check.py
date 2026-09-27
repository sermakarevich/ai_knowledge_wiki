"""Sanity check: Neo4j + APOC/GDS + Ollama chat + embeddings.

Run with: python -m graph_rag.check
"""

from graph_rag.db import get_driver
from graph_rag.llm import chat, embed


def main() -> None:
    with get_driver() as driver:
        components = driver.execute_query(
            "CALL dbms.components() YIELD name, versions RETURN name, versions",
            database_="neo4j",
        ).records
        for record in components:
            print(f"{record['name']} version: {record['versions'][0]}")

        apoc_version = driver.execute_query(
            "RETURN apoc.version() AS v", database_="neo4j"
        ).records[0]["v"]
        print(f"apoc.version() = {apoc_version}")

        gds_version = driver.execute_query(
            "RETURN gds.version() AS v", database_="neo4j"
        ).records[0]["v"]
        print(f"gds.version() = {gds_version}")

    reply = chat([{"role": "user", "content": "Reply with the single word: pong"}])
    print(f"chat reply: {reply!r}")

    vectors = embed(["hello graph rag"])
    print(f"embedding length: {len(vectors[0])}")


if __name__ == "__main__":
    main()
