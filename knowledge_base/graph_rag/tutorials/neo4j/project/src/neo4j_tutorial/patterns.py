"""Python driver patterns used in chapter 05_python_patterns.md.

Covers: one-shot execute_query straight to a pandas DataFrame, managed
read/write transaction functions (with automatic retries), an explicit
transaction for a multi-statement unit of work, and batched writes.
"""

from itertools import islice

import neo4j
import pandas as pd

from neo4j_tutorial.db import get_driver


def query_to_df(query: str, **params) -> pd.DataFrame:
    """Run a read-only query in one round trip and get a pandas DataFrame back.

    `routing_="r"` marks the query as a read, so a Neo4j cluster could route
    it to a follower instead of always hitting the leader (on our single
    instance it has no visible effect, but it is good habit). `result_transformer_`
    streams the result straight into a DataFrame instead of first building a
    list of Record objects.
    """
    with get_driver() as driver:
        return driver.execute_query(
            query,
            params,
            database_="neo4j",
            routing_="r",
            result_transformer_=neo4j.Result.to_df,
        )


def _count_people_tx(tx: neo4j.ManagedTransaction) -> int:
    result = tx.run("MATCH (p:Person) RETURN count(p) AS n")
    return result.single()["n"]


def count_people() -> int:
    """Managed read transaction. `session.execute_read` retries the function
    it is given on transient errors (e.g. a leader election in a cluster), so
    the function must be safe to call more than once with no extra effect.
    """
    with get_driver() as driver, driver.session(database="neo4j") as session:
        return session.execute_read(_count_people_tx)


def _add_skill_tx(tx: neo4j.ManagedTransaction, person: str, skill: str, level: str) -> int:
    result = tx.run(
        "MATCH (p:Person {name: $person}) MATCH (s:Skill {name: $skill}) "
        "MERGE (p)-[h:HAS_SKILL]->(s) SET h.level = $level "
        "RETURN count(h) AS n",
        person=person,
        skill=skill,
        level=level,
    )
    return result.single()["n"]


def add_skill(person: str, skill: str, level: str) -> int:
    """Managed write transaction. Just like `execute_read`, `execute_write`
    may call its function again after a transient failure, so the write must
    be idempotent -- here `MERGE` guarantees running it twice never creates a
    duplicate `HAS_SKILL` relationship.
    """
    with get_driver() as driver, driver.session(database="neo4j") as session:
        return session.execute_write(_add_skill_tx, person=person, skill=skill, level=level)


def rename_person_explicit(old_name: str, new_name: str, fail_before_commit: bool = False) -> None:
    """Explicit transaction: one or more statements committed, or rolled
    back, together as a single unit of work. Use this instead of a managed
    transaction function when the logic between statements needs
    application-level decisions that don't fit a retryable function.

    `with session.begin_transaction() as tx:` commits automatically if the
    block exits normally *and* `tx.commit()` was called, or rolls back if an
    exception escapes the block. Set `fail_before_commit=True` to see the
    rollback: the rename runs against the transaction's buffer, then the
    exception fires before `tx.commit()`, so the rename never reaches the
    database.
    """
    with get_driver() as driver, driver.session(database="neo4j") as session:
        with session.begin_transaction() as tx:
            tx.run(
                "MATCH (p:Person {name: $old}) SET p.name = $new",
                old=old_name,
                new=new_name,
            )
            if fail_before_commit:
                raise RuntimeError("simulated failure before commit")
            tx.commit()


def batch_write(rows: list[dict], cypher: str, size: int = 500) -> int:
    """Write many rows in chunks, reusing the `UNWIND $rows AS row` pattern
    from chapter 02. `cypher` must reference the batch as `$rows`. Returns
    the total number of rows written.
    """
    with get_driver() as driver:
        total = 0
        it = iter(rows)
        while chunk := list(islice(it, size)):
            driver.execute_query(cypher, rows=chunk, database_="neo4j")
            total += len(chunk)
        return total
