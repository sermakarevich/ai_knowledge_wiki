"""Shared pytest fixtures: one driver for the whole test module, loaded once
from the CSV dataset (with a full reset) before any test runs.
"""

import pytest

from neo4j_tutorial import load_data
from neo4j_tutorial.db import get_driver
from neo4j.exceptions import Neo4jError, ServiceUnavailable

_down = False
_reason = "unknown"


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: pytest.Config) -> None:
    """Probe the database once, before any test runs.

    The suite talks to the `neo4j-tutorial` Docker container on port 7689
    (Bolt) / 7476 (browser). Start it first with `just up`. Here we just record
    whether the database is reachable; `pytest_runtest_setup` turns a failed
    probe into a clean skip instead of 70+ connection errors.
    """
    global _down, _reason
    try:
        with get_driver() as probe:
            probe.execute_query("RETURN 1 AS ok", database_="neo4j")
    except (Neo4jError, ServiceUnavailable) as exc:
        _down = True
        _reason = repr(exc)


def pytest_runtest_setup(item: pytest.Item) -> None:
    if _down:
        pytest.skip(
            f"Neo4j not reachable/accessible ({_reason}); run `just up` first"
        )


def load_dataset(driver, reset: bool = True) -> None:
    """Run the same steps as `load_data.main()`, without the CLI/print parts."""
    if reset:
        driver.execute_query("MATCH (n) DETACH DELETE n", database_="neo4j")
    for constraint in load_data.CONSTRAINTS:
        driver.execute_query(constraint, database_="neo4j")
    for csv_name, query in load_data.NODE_QUERIES.items():
        load_data.load_file(driver, csv_name, query)
    for csv_name, query in load_data.REL_QUERIES.items():
        load_data.load_file(driver, csv_name, query)


@pytest.fixture(scope="module")
def driver():
    d = get_driver()
    yield d
    d.close()


@pytest.fixture(scope="module", autouse=True)
def loaded_dataset(driver):
    load_dataset(driver, reset=True)
    yield
    load_dataset(driver, reset=True)
