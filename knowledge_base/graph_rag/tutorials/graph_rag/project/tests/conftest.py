"""Shared pytest setup for the graph_rag test suite.

The suite talks to the `neo4j-graphrag` Docker container (see
`docker-compose.yml`, on port 7690 Bolt / 7477 browser). Start it first
with `just up`. Here we only probe the database once, before any test
runs: if it is not reachable — or answers with different credentials,
which happens when another Neo4j (e.g. the sibling `neo4j` tutorial's
`neo4j-tutorial` container) is listening on the same port — then every
neo4j-dependent test is skipped with a clear message instead of blowing
up with a long list of connection/auth errors.
"""

import pytest
from neo4j.exceptions import DriverError, Neo4jError

from graph_rag.config import settings
from graph_rag.db import get_driver

_down = False
_reason = "unknown"


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: pytest.Config) -> None:
    """Probe the database once, before any test runs.

    `get_driver()` already calls `verify_connectivity()`; we then run one
    trivial query to also catch auth problems. Any server error
    (`Neo4jError`: `AuthError`, rate-limit `ClientError`, ...) or transport
    error (`NeoDriverError`: `ServiceUnavailable` for a dead port) marks the
    suite as down for the rest of the run.
    """
    global _down, _reason
    try:
        with get_driver() as probe:
            probe.execute_query("RETURN 1 AS ok", database_="neo4j")
    except (Neo4jError, DriverError) as exc:
        _down = True
        _reason = type(exc).__name__


def pytest_runtest_setup(item: pytest.Item) -> None:
    if _down:
        pytest.skip(
            f"Neo4j not reachable/accessible on {settings.neo4j_uri} "
            f"({_reason}); run `just up` first"
        )
