# 05 — The Python driver in practice: patterns, transactions, tests

**What you will learn**
- The driver lifecycle: one `Driver` per application, `close()`/context manager, `verify_connectivity()`
- `execute_query` (one-shot, straight to pandas) vs sessions with managed or explicit transactions — and when to use which
- Why a managed-transaction function must be idempotent (the driver may run it twice)
- How to read a `Record`: `.data()`, `.value()`, and the raw `Node`/`Relationship`/`Path` objects
- Parameters, temporal types, error handling, batching, multi-database, and how the test suite in `project/tests/` proves the whole tutorial works

All the functions shown below live in `project/src/neo4j_tutorial/patterns.py`. Every snippet was run against our Docker Neo4j (server 5.26.29, Python driver `neo4j` 6.3.0, `pandas` 3.0.5) and the output shown is the real output.

## The driver lifecycle

A `Driver` (from `neo4j.GraphDatabase.driver(...)`) is a connection pool, not a single connection — it manages a pool of TCP connections over **Bolt** (Neo4j's binary network protocol) and reuses them across queries. Because of that pooling, an application should create **one `Driver` per target database** and reuse it for the lifetime of the app, not open a new one per request.

`project/src/neo4j_tutorial/db.py` (from chapter 00) wraps this:

```python
def get_driver() -> Driver:
    driver = GraphDatabase.driver(uri, auth=(user, password))
    driver.verify_connectivity()
    return driver
```

`verify_connectivity()` makes one round trip immediately, so a bad URI or wrong password fails fast at startup instead of on the first real query. A `Driver` (and a `Session`, see below) is a context manager, so `with get_driver() as driver: ...` always calls `driver.close()` — releasing every pooled connection — even if the code inside raises.

Our tutorial calls `get_driver()` inside every helper function for simplicity (small scripts, short-lived processes). A long-running application (a web server, say) should instead build the `Driver` once at startup and pass it around, calling `close()` once at shutdown.

## `execute_query` vs sessions

`Driver.execute_query(...)` is the simplest way to run one query: it opens a connection, runs the query in its own transaction, and returns. It's the right tool whenever a piece of work is exactly one Cypher statement — most of what chapters 02–04 used it for.

```python
def query_to_df(query: str, **params) -> pd.DataFrame:
    with get_driver() as driver:
        return driver.execute_query(
            query,
            params,
            database_="neo4j",
            routing_="r",
            result_transformer_=neo4j.Result.to_df,
        )
```

```python
>>> query_to_df("MATCH (p:Person) RETURN p.name AS name, p.age AS age ORDER BY name LIMIT 3")
            name  age
0   Anna Schmidt   29
1  Chris Johnson   37
2    David Klein   50
```

Two keyword arguments make `execute_query` more than "just run a string":
- `routing_="r"` marks the query as a **read**. On a single instance (ours) it has no visible effect, but on a Neo4j cluster it lets the driver route the query to a follower instead of always hitting the leader — cheap to add, and it documents intent even when it doesn't change behaviour.
- `result_transformer_=neo4j.Result.to_df` consumes the result stream directly into a **pandas DataFrame**, instead of first materializing a list of `Record` objects and converting them yourself. It needs no extra dependency — `to_df` ships with the `neo4j` package itself and only requires `pandas` to be installed, which the tutorial already uses.

**When to reach for a session instead:** as soon as a unit of work needs more than one statement to succeed or fail together — e.g. "move a skill from one person to another" (delete one `HAS_SKILL` edge, create another) — a single `execute_query` call can't express that, because each `execute_query` call is its own transaction. That's what sessions and transactions are for.

## Managed transactions: `execute_read` / `execute_write`

A `Session` groups one or more transactions against one database. Inside a session, `session.execute_read(fn, **kw)` and `session.execute_write(fn, **kw)` run a **transaction function** — a plain function that receives a transaction (`tx`) as its first argument and calls `tx.run(...)` on it:

```python
def _count_people_tx(tx: neo4j.ManagedTransaction) -> int:
    result = tx.run("MATCH (p:Person) RETURN count(p) AS n")
    return result.single()["n"]


def count_people() -> int:
    with get_driver() as driver, driver.session(database="neo4j") as session:
        return session.execute_read(_count_people_tx)
```

```python
>>> count_people()
12
```

**Why "managed"?** `execute_read`/`execute_write` wrap the whole call in retry logic: if the transaction fails for a *transient* reason (a dropped connection, a leader election on a cluster, a deadlock with another transaction), the driver transparently **runs your function again** from scratch. This is the reason the function you pass in must be idempotent — safe to execute more than once with the same net effect — because you cannot know in advance whether it will run once or several times.

Our write example follows that rule by using `MERGE`, exactly like the loader in chapter 02:

```python
def _add_skill_tx(tx: neo4j.ManagedTransaction, person: str, skill: str, level: str) -> int:
    result = tx.run(
        "MATCH (p:Person {name: $person}) MATCH (s:Skill {name: $skill}) "
        "MERGE (p)-[h:HAS_SKILL]->(s) SET h.level = $level "
        "RETURN count(h) AS n",
        person=person, skill=skill, level=level,
    )
    return result.single()["n"]


def add_skill(person: str, skill: str, level: str) -> int:
    with get_driver() as driver, driver.session(database="neo4j") as session:
        return session.execute_write(_add_skill_tx, person=person, skill=skill, level=level)
```

```python
>>> add_skill("Anna Schmidt", "Rust", "beginner")
1
>>> add_skill("Anna Schmidt", "Rust", "beginner")   # called again — same result, no duplicate edge
1
```

Running it twice returns `1` both times, and a follow-up count of `HAS_SKILL` edges between Anna and Rust stays at `1` — exactly what a possible driver-side retry needs to be safe.

**Rule of thumb:** default to `execute_read`/`execute_write` for anything that fits in one transaction function. Reach for an explicit transaction (next section) only when you need control the managed API doesn't give you.

## Explicit transactions

An explicit transaction is for a multi-statement unit of work where the decision to commit depends on application logic that doesn't fit cleanly inside a retryable function — for example, running one statement, inspecting its result in Python, and deciding whether to run a second statement or abort:

```python
def rename_person_explicit(old_name: str, new_name: str, fail_before_commit: bool = False) -> None:
    with get_driver() as driver, driver.session(database="neo4j") as session:
        with session.begin_transaction() as tx:
            tx.run(
                "MATCH (p:Person {name: $old}) SET p.name = $new",
                old=old_name, new=new_name,
            )
            if fail_before_commit:
                raise RuntimeError("simulated failure before commit")
            tx.commit()
```

`session.begin_transaction()` returns a `Transaction` used as a context manager: if the `with` block raises, the transaction is **rolled back** automatically when it closes; nothing reaches the database unless `tx.commit()` was called first.

Rollback, proven by actually raising inside the block:

```python
>>> rename_person_explicit("Anna Schmidt", "Not Anna", fail_before_commit=True)
Traceback (most recent call last):
    ...
RuntimeError: simulated failure before commit
>>> query_to_df("MATCH (p:Person {name: 'Anna Schmidt'}) RETURN count(p) AS n")
   n
0  1
```

The rename ran inside the transaction, the exception fired before `tx.commit()`, and "Anna Schmidt" is still there — the write never left the transaction.

Commit, for comparison:

```python
>>> rename_person_explicit("Marta Kaminska", "Marta K.", fail_before_commit=False)
>>> query_to_df("MATCH (p:Person {name: 'Marta K.'}) RETURN count(p) AS n")
   n
0  1
```

(We renamed "Marta K." back to "Marta Kaminska" afterwards with `just load`, to keep the dataset matching `index.md`.)

## Reading a `Record`

A query result is a stream of `Record` objects — one per row. A `Record` behaves like an ordered mapping: index by column name or position, or convert it wholesale.

```python
>>> result = driver.execute_query(
...     "MATCH (p:Person {name: $name})-[w:WORKS_AT]->(c:Company) RETURN p, w, c",
...     name="Anna Schmidt", database_="neo4j",
... )
>>> rec = result.records[0]
>>> rec.data()
{'p': {'name': 'Anna Schmidt', 'age': 29},
 'w': ({'name': 'Anna Schmidt', 'age': 29}, 'WORKS_AT', {'name': 'GraphWorks', 'founded': 2015, 'industry': 'Software'}),
 'c': {'name': 'GraphWorks', 'founded': 2015, 'industry': 'Software'}}
>>> rec.value("p")
<Node element_id='4:...:56' labels=frozenset({'Person'}) properties={'name': 'Anna Schmidt', 'age': 29}>
```

- **`.data()`** converts every column to plain Python (`dict`s for nodes, `(start, type, end)` tuples for relationships) — good for a quick look or `json.dumps`, but it loses type information (a `Node` becomes indistinguishable from a plain map).
- **`.value("p")`** (or `.value(0)`) returns one column, un-converted — for a `Node`/`Relationship` column that keeps the real object.
- Indexing a record directly (`rec["p"]`) does the same as `.value("p")`.

The raw objects carry more than their properties:

```python
>>> node = rec["p"]
>>> type(node)
<class 'neo4j.graph.Node'>
>>> node.labels
frozenset({'Person'})
>>> node.element_id
'4:cbb9fadc-0ac3-4ef3-b113-b227115ff73b:56'
>>> dict(node)          # properties only, as a plain dict — the usual way to serialize a Node
{'name': 'Anna Schmidt', 'age': 29}

>>> rel = rec["w"]
>>> rel.type
'WORKS_AT'
>>> dict(rel)
{'role': 'Backend Engineer', 'since': 2018}
```

`dict(node)` / `dict(relationship)` is the standard way to get a JSON-serializable dict out of a `Node` or `Relationship` — it drops the label/type/id and keeps only the properties, so add those back explicitly (`{"labels": list(node.labels), **dict(node)}`) if you need them downstream. A `Path` value (from a variable-length or `shortestPath()` match, chapter 04) exposes `.nodes` and `.relationships` the same way `nodes(p)`/`relationships(p)` do in Cypher.

`element_id` is a string that uniquely identifies a node or relationship *for the lifetime of the database* — use it to re-fetch or de-duplicate the same entity across queries; don't parse or persist it as a stable external ID, since Neo4j does not guarantee its format across versions.

## Parameters and temporal types

Always pass values as **parameters** (`$name`), never string-format them into Cypher — parameters are the difference between a fast, cached query plan and a slow one recompiled every time, and they close off Cypher injection the same way a parameterized SQL query closes off SQL injection.

Neo4j has native temporal types (`DATE`, `DATETIME`, `TIME`, `DURATION`, ...). The driver maps them to its own `neo4j.time` classes, not directly to `datetime.datetime`, because Neo4j's types support a wider range and different precision than Python's:

```python
>>> result = driver.execute_query("RETURN datetime() AS now, date() AS today", database_="neo4j")
>>> rec = result.records[0]
>>> rec["now"], type(rec["now"])
(2026-08-28T13:44:27.491000000+00:00, <class 'neo4j.time.DateTime'>)
>>> rec["now"].to_native(), type(rec["now"].to_native())
(datetime.datetime(2026, 8, 28, 13, 44, 27, 491000, tzinfo=...), <class 'datetime.datetime'>)
```

`.to_native()` converts to the closest standard-library type (`datetime.datetime`, `datetime.date`, ...) when you need to hand the value to code that expects those. Going the other way, a Python `datetime.datetime` passed as a parameter is accepted directly and comes back as a `neo4j.time.DateTime`:

```python
>>> driver.execute_query("RETURN $dt AS dt", dt=datetime.datetime.now(datetime.timezone.utc), database_="neo4j").records[0]["dt"]
2026-08-28T13:44:27.504258000+00:00
```

## Error handling

`neo4j.exceptions` has specific exception classes worth catching separately rather than a bare `except Exception`:

- **`ConstraintError`** — a write violated a uniqueness constraint (chapter 02). Unlike `MERGE`, a `CREATE` does not check first, so it raises instead of silently doing nothing:

```python
>>> driver.execute_query('CREATE (:Person {name: "Anna Schmidt"})', database_="neo4j")
Traceback (most recent call last):
    ...
neo4j.exceptions.ConstraintError: {neo4j_code: Neo.ClientError.Schema.ConstraintValidationFailed}
{message: Node(56) already exists with label `Person` and property `name` = 'Anna Schmidt'}
```

  A failed query is never partially applied — the person count stayed at `12` afterwards. Catch `ConstraintError` when a duplicate is an expected, recoverable situation (e.g. "this signup email is already taken") rather than a bug.

- **`ServiceUnavailable`** — the driver could not reach any server at all (wrong host/port, Neo4j not running, network partition):

```python
>>> GraphDatabase.driver("bolt://localhost:9999", auth=("neo4j", "tutorial123")).verify_connectivity()
Traceback (most recent call last):
    ...
neo4j.exceptions.ServiceUnavailable: Couldn't connect to localhost:9999 ...
```

  Catch this around startup connectivity checks and retry/backoff logic; catching it around every single query is usually overkill for a tutorial-sized app.

Both are subclasses of `neo4j.exceptions.Neo4jError` / `DriverError`, so a broad `except neo4j.exceptions.Neo4jError:` is a reasonable last-resort fallback that still excludes unrelated Python exceptions.

## Batching large writes

Chapter 02's loader already established the pattern: send many rows in one query with `UNWIND $rows AS row`, in chunks, rather than one `execute_query` call per row (which would pay a network round trip per row) or one call for millions of rows at once (which would build one enormous transaction). `patterns.batch_write` packages it as a one-liner for reuse:

```python
def batch_write(rows: list[dict], cypher: str, size: int = 500) -> int:
    with get_driver() as driver:
        total = 0
        it = iter(rows)
        while chunk := list(islice(it, size)):
            driver.execute_query(cypher, rows=chunk, database_="neo4j")
            total += len(chunk)
        return total
```

```python
>>> batch_write(
...     [{"name": f"BatchSkill{i}"} for i in range(3)],
...     "UNWIND $rows AS row MERGE (s:Skill {name: row.name})",
...     size=2,
... )
3
```

`size=500` is a reasonable starting point for small rows (matches the loader's default from chapter 02); tune it up or down based on row size and how long you're willing to hold a single transaction open. For write volumes so large that even one 500-row transaction is a problem, chapter 04 covered the Cypher-side equivalent: `CALL { ... } IN TRANSACTIONS OF n ROWS`.

## `database_` and multi-database

Every call above passes `database_="neo4j"` — Neo4j (Enterprise edition, and also usable in Community for the single default database) can host multiple named databases on one server, and the driver has no built-in default, so this argument is required to avoid ambiguity. Our Docker image is Community edition with a single database also named `neo4j` (see `index.md`), so `database_="neo4j"` always resolves to "the only database there is" here — but the argument is there so the same code works unchanged on Enterprise, against whichever database you name.

## Async driver, in short

The same API exists in an async flavor: `from neo4j import AsyncGraphDatabase`, with `async def` transaction functions and `await driver.execute_query(...)` / `await session.execute_read(...)`. Reach for it inside an already-async application (e.g. an `asyncio`-based web framework); for scripts and simple services like this tutorial's, the synchronous driver used throughout is simpler and just as capable.

## Testing against the real database

`project/tests/` runs pytest directly against the Docker Neo4j — no mocks — because a graph database's behaviour (constraint errors, path results, transaction semantics) is exactly the kind of thing that's easy to get subtly wrong in a mock. `conftest.py` provides a module-scoped `driver` fixture and an `autouse` fixture that resets and reloads the dataset once before the module's tests run (and once more after, to leave a clean state for the next chapter or task).

```bash
just test
```
```
..............................................................           [100%]
62 passed in 0.48s
```

What the suite proves:
- **`test_connectivity`** — the driver can actually reach the container (catches a wrong port/password/down container immediately).
- **`test_node_counts_match_csv_row_counts` / `test_relationship_counts_match_csv_row_counts`** — the loader from chapter 02 created exactly one node/relationship per CSV row, for every entity and relationship type in `index.md`.
- **`test_loader_is_idempotent`** — running the loader a second time, without a reset, leaves every count unchanged (the `MERGE`-based idempotency chapter 02 promised).
- **`test_basic_query_runs` / `test_advanced_query_runs`** (parametrized over every entry in `queries_basic.QUERIES` and `queries_advanced.QUERIES`) — every read-only query shown in chapters 03 and 04 still parses and runs against the live schema; this is what would catch a chapter's Cypher going stale if the dataset or a query ever changed.
- **`test_query_to_df_returns_dataframe`** — `execute_query(..., result_transformer_=neo4j.Result.to_df)` really returns a `pandas.DataFrame`, not a list of records.
- **`test_execute_read_and_write_transaction_functions`** — `execute_read`/`execute_write` run and, run twice, `add_skill` stays idempotent (no duplicate `HAS_SKILL` edge).
- **`test_explicit_transaction_rollback_leaves_counts_unchanged`** — an explicit transaction that raises before `tx.commit()` truly leaves the database untouched.
- **`test_explicit_transaction_commit_applies_change`** — the same API, committed, really persists.
- **`test_batch_write`** — chunked `UNWIND` writes land the full row count, in more than one chunk.

Every test cleans up after itself (deleting temporary skills, restoring renamed people) so the suite can run any number of times and the dataset always ends up matching `index.md`.

## Key takeaways

- One `Driver` per application; use it as a context manager (or call `close()` explicitly) so pooled connections are released; `verify_connectivity()` fails fast on a bad connection.
- `execute_query` is the right tool for a single Cypher statement, especially with `result_transformer_=neo4j.Result.to_df` for a straight-to-pandas result; reach for a session once a unit of work needs more than one statement.
- `session.execute_read`/`execute_write` may retry your transaction function on transient errors — write it so running it twice is always safe (typically via `MERGE`, not `CREATE`).
- An explicit transaction (`session.begin_transaction()` as a context manager) gives full control over commit/rollback for multi-statement logic that a managed transaction function can't express; an uncaught exception rolls it back automatically.
- `.data()` gives a quick plain-Python view of a row; `dict(node)`/`dict(relationship)` extract just the properties from a `Node`/`Relationship` object, which also expose `.labels`/`.type` and a stable-for-this-database `element_id`.
- Temporal values come back as `neo4j.time` types with a `.to_native()` escape hatch to the standard library; always pass values as `$parameters`, never string-formatted into the query text.
- Catch `neo4j.exceptions.ConstraintError` for expected duplicate-write conflicts and `ServiceUnavailable` for connectivity problems, rather than a bare `except Exception`.
- `database_="..."` is mandatory on every call because Neo4j supports multiple named databases per server, even though our tutorial only ever uses one.
- An async driver (`AsyncGraphDatabase`) mirrors this whole API with `async`/`await`, for use inside an already-async application.
- `just test` runs the full suite against the live Docker database — it is the closest thing this tutorial has to a single command that proves every chapter's code still works.

## Where to go next

- **GDS (Graph Data Science library)** — a separate Neo4j plugin with graph algorithms (PageRank, community detection, node embeddings) that go well beyond what plain Cypher or APOC express concisely.
- **Vector index** — Neo4j can index embedding vectors and run similarity search natively, letting you combine a nearest-neighbour search with a graph traversal in one query.
- **Neo4j Aura** — Neo4j's managed cloud offering; the same driver and Cypher you used here connect to it by changing only the URI and credentials, no code changes.
- **LLM / GraphRAG** — using a graph as retrieval context for a large language model (an LLM, e.g. GPT or Claude): the graph structure (relationships, paths, communities) gives an LLM connected context that plain vector search over isolated text chunks misses.
