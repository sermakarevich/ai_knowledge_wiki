"""Small helpers to connect to the tutorial Neo4j database."""

import os

from dotenv import load_dotenv
from neo4j import Driver, GraphDatabase

load_dotenv()

DEFAULT_URI = "bolt://localhost:7689"
DEFAULT_USER = "neo4j"
DEFAULT_PASSWORD = "tutorial123"


def get_driver() -> Driver:
    """Create a Neo4j driver using .env settings, falling back to tutorial defaults."""
    uri = os.getenv("NEO4J_URI", DEFAULT_URI)
    user = os.getenv("NEO4J_USER", DEFAULT_USER)
    password = os.getenv("NEO4J_PASSWORD", DEFAULT_PASSWORD)
    driver = GraphDatabase.driver(uri, auth=(user, password))
    driver.verify_connectivity()
    return driver


def run(query: str, **params) -> list[dict]:
    """Run a Cypher query and return the results as a list of plain dicts."""
    with get_driver() as driver:
        result = driver.execute_query(query, params, database_="neo4j")
        return [record.data() for record in result.records]
