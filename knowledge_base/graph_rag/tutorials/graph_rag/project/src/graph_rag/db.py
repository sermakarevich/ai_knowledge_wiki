"""Small helpers to connect to the graph_rag Neo4j database."""

import pandas as pd
from neo4j import Driver, GraphDatabase

from graph_rag.config import settings


def get_driver() -> Driver:
    """Create a Neo4j driver using .env settings."""
    driver = GraphDatabase.driver(
        settings.neo4j_uri, auth=(settings.neo4j_user, settings.neo4j_password)
    )
    driver.verify_connectivity()
    return driver


def run(query: str, **params) -> list[dict]:
    """Run a Cypher query and return the results as a list of plain dicts."""
    with get_driver() as driver:
        result = driver.execute_query(query, params, database_="neo4j")
        return [record.data() for record in result.records]


def run_df(query: str, **params) -> pd.DataFrame:
    """Run a Cypher query and return the results as a pandas DataFrame."""
    return pd.DataFrame(run(query, **params))
