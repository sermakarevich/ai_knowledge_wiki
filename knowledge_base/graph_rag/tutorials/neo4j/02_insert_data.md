# 02 — Inserting data: CREATE, MERGE, constraints and batch loading

**What you will learn**
- The difference between `CREATE` (always makes a new node) and `MERGE` (find it, or create it if missing)
- Why you create uniqueness constraints *before* loading any data, not after
- How to pass values safely into Cypher with parameters (`$name`), instead of building query strings by hand
- How to load many rows at once with `UNWIND`, and why that is faster and safer than one query per row
- How `LOAD CSV` reads files directly from disk, and how our Python loader (`load_data.py`) does the same job in a way you can re-run any time

## CREATE vs MERGE

**`CREATE`** always adds a brand new node or relationship, even if an identical one already exists. Watch what happens if we `CREATE` the same person twice:

```cypher
CREATE (p:Person {name:'Test Dup', age:99}) RETURN p;
```
```
p
(:Person {name: "Test Dup", age: 99})
```

Run it again with a different age:

```cypher
CREATE (p:Person {name:'Test Dup', age:100}) RETURN p;
```

Because our database already has a **uniqueness constraint** on `Person.name` (more on that below), Neo4j refuses:

```
Node(0) already exists with label `Person` and property `name` = 'Test Dup'
```

Without that constraint, this second `CREATE` would have succeeded silently, and now the graph would contain **two different "Test Dup" nodes** with two different `age` values — the classic duplicate-node mistake. Any later query matching `{name:'Test Dup'}` could return either one, or both, and your counts would be wrong. This is the single most common bug when people start loading data into Neo4j.

**`MERGE`** is the fix: it means "match this whole pattern; if it exists, use it; if it doesn't, create it." It checks the *entire pattern* you give it (labels + properties in the curly braces), not just part of it:

```cypher
MERGE (p:Person {name:'Test Dup'})
  ON CREATE SET p.age = 1, p.created = true
  ON MATCH  SET p.age = p.age + 1
RETURN p.name, p.age, p.created;
```

First run (the node from the failed `CREATE` above still exists with `age: 99`, so this is a **match**, not a create):
```
p.name, p.age, p.created
"Test Dup", 100, NULL
```

Run the exact same query again:
```
p.name, p.age, p.created
"Test Dup", 101, NULL
```

- `ON CREATE SET` only runs the first time, when `MERGE` had to build a new node.
- `ON MATCH SET` only runs when `MERGE` found an existing node.
- Every re-run above only ever touched **one** node — no duplicates, no matter how many times we run it. That is what "idempotent" means: running an operation twice has the same effect as running it once.

(We clean up this `Test Dup` node afterwards — it was only there to demonstrate the mistake.)

## Constraints: create them before you load anything

A **constraint** is a rule the database enforces on every write. A **uniqueness constraint** says "no two nodes with this label may share this property value" — and Neo4j automatically builds an index to check that rule fast.

Two reasons to create constraints *first*, before loading data:

1. **Correctness.** Without the constraint, nothing stops `CREATE` (or a badly written `MERGE` on the wrong property) from producing duplicates, as shown above.
2. **Speed.** `MERGE (p:Person {name: row.name})` has to search for a matching node before deciding whether to create one. Without an index on `Person.name`, that search scans every `Person` node — slow once you have more than a few hundred. With the constraint's index, it's a direct lookup, no matter how many people you have.

We create four constraints, one per node label that has a natural unique key:

```cypher
CREATE CONSTRAINT person_name  IF NOT EXISTS FOR (p:Person)  REQUIRE p.name IS UNIQUE;
CREATE CONSTRAINT company_name IF NOT EXISTS FOR (c:Company) REQUIRE c.name IS UNIQUE;
CREATE CONSTRAINT skill_name   IF NOT EXISTS FOR (s:Skill)   REQUIRE s.name IS UNIQUE;
CREATE CONSTRAINT city_name    IF NOT EXISTS FOR (ci:City)   REQUIRE ci.name IS UNIQUE;
```

`IF NOT EXISTS` makes this safe to run every time you start the loader — it does nothing if the constraint is already there. Verified after running our loader:

```bash
just cypher "SHOW CONSTRAINTS YIELD name RETURN count(*) AS c"
```
```
c
4
```

## Parameters: never paste values into a query string

If you build Cypher text by string-formatting user data into it (e.g. Python f-strings), you risk **Cypher injection** — a user-supplied value containing quotes or Cypher keywords could change what the query does. It's the exact same class of bug as SQL injection. The fix is **parameters**: placeholders like `$name` in the query text, with the actual value passed separately, never mixed into the query string.

From `cypher-shell` (Neo4j's command-line client), you set a parameter with `:param` and then reference it with `$`:

```cypher
:param name => "Anna Schmidt"
MATCH (p:Person {name: $name}) RETURN p.name, p.age;
```
```
p.name, p.age
"Anna Schmidt", 29
```

From Python, the driver takes parameters as a plain dictionary — the driver sends them to Neo4j as data, never as text glued into the query:

```python
driver.execute_query(
    "MATCH (p:Person {name: $name}) RETURN p.name, p.age",
    name="Anna Schmidt",   # becomes the $name parameter
    database_="neo4j",
)
```

Our `db.py` (from chapter 00) already works this way: `run(query, **params)` forwards keyword arguments straight to `execute_query` as parameters.

## Batch loading with UNWIND

Loading data one row at a time (one query per person) means one network round-trip per row — for a few rows that's fine, for thousands it's slow. **`UNWIND`** turns a list into rows *inside* Cypher, so you can send many rows in a single query:

```cypher
UNWIND $rows AS row
MERGE (p:Person {name: row.name})
SET p.age = row.age
```

Here `$rows` is a parameter holding a list of small dictionaries (one per CSV row), e.g. `[{"name": "Anna Schmidt", "age": 29}, ...]`. `UNWIND $rows AS row` turns that list into one "row" per list item, and the rest of the query runs once per row, all inside one transaction.

Why not put *all* rows — even a million — into one `UNWIND`? A single transaction that touches too much data holds locks and memory for a long time and risks running out of memory. The common pattern is **batches of a few hundred to a few thousand rows per transaction** — big enough to amortize the network round-trip, small enough to keep each transaction quick and safe to retry. Our loader uses batches of 500 rows via a small helper:

```python
def batched(rows: list[dict], size: int = 500) -> Iterator[list[dict]]:
    """Split a list of rows into chunks of at most `size` rows each."""
    it = iter(rows)
    while chunk := list(islice(it, size)):
        yield chunk
```

Our dataset is small (a few dozen rows per file), so every file fits in one batch — but the loader would behave identically on a file with 50,000 rows.

## LOAD CSV: reading files directly in Cypher

Cypher can also read a CSV file itself, without any Python in between, using `LOAD CSV WITH HEADERS FROM ...`. This works here because `docker-compose.yml` mounts our local `data/` folder to `/import` inside the container (see chapter 00), and Neo4j resolves `file:///name.csv` against that `/import` folder.

```cypher
LOAD CSV WITH HEADERS FROM 'file:///cities.csv' AS row
MERGE (c:City {name: row.name})
SET c.country = row.country
RETURN count(*) AS rows_processed;
```
```
rows_processed
4
```
```cypher
MATCH (c:City) RETURN count(c) AS cities;
```
```
cities
4
```

Every value coming from `LOAD CSV` is a **string**, even things that look like numbers — CSV files have no types. That's why the *people* loader needs `toInteger(row.age)` if you did this in pure Cypher, to turn the text `"29"` into the number `29`. (You'll see the same conversion done in Python below.)

**`LOAD CSV` vs the Python loader** — both use `MERGE`, both are idempotent, both process the file in one pass. The difference is where the casting and batching logic lives:

| | `LOAD CSV` | `load_data.py` |
|---|---|---|
| Runs entirely inside | Neo4j (via cypher-shell or the Browser) | Python, calling Neo4j over Bolt |
| Type casting | Manual `toInteger()` per field in Cypher | Python's `int()` in `read_csv()` |
| Batching | You add `CALL { ... } IN TRANSACTIONS OF n ROWS` yourself | Built in via `batched()` |
| Reusable across files | One query per file, copy-pasted | One shared loop, works for any CSV with the same shape |
| Good for | Quick one-off loads, debugging in the Browser | Repeatable project setup, used by every later chapter |

## Relationship creation pattern

Relationships need both endpoint nodes to already exist, so the pattern is always: `MATCH` both nodes, then `MERGE` the relationship between them, then `SET` its properties:

```cypher
UNWIND $rows AS row
MATCH (p:Person {name: row.person})
MATCH (c:Company {name: row.company})
MERGE (p)-[w:WORKS_AT]->(c)
SET w.since = row.since, w.role = row.role
```

`MERGE` on a relationship checks the whole pattern — start node, relationship type, end node — so re-running this never creates a second `WORKS_AT` edge between the same person and company; it just updates `since`/`role` on the one that's already there.

## `load_data.py`: a reusable, idempotent loader

The full file lives at `project/src/neo4j_tutorial/load_data.py`. Run it with:

```bash
python -m neo4j_tutorial.load_data [--reset]
```

Key pieces, in the order they run:

**1. `--reset` wipes the graph clean**, useful when you want to start from nothing:
```python
if args.reset:
    driver.execute_query("MATCH (n) DETACH DELETE n", database_="neo4j")
```
`DETACH DELETE` removes a node *and* any relationships attached to it in one step — plain `DELETE` would refuse to delete a node that still has relationships.

**2. Constraints are created first**, before any data is loaded (as explained above):
```python
CONSTRAINTS = [
    "CREATE CONSTRAINT person_name IF NOT EXISTS FOR (p:Person) REQUIRE p.name IS UNIQUE",
    ...
]
for constraint in CONSTRAINTS:
    driver.execute_query(constraint, database_="neo4j")
```

**3. CSVs are read with `csv.DictReader`, and known numeric fields are cast to `int`:**
```python
INT_FIELDS = {"age", "founded", "since"}

def read_csv(name: str) -> list[dict]:
    with open(DATA_DIR / name, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        for field in INT_FIELDS:
            if field in row:
                row[field] = int(row[field])
    return rows
```
This is the Python-side equivalent of `toInteger()` in Cypher — `csv.DictReader` gives you strings for every column, so anything meant to be a number needs an explicit cast.

**4. Nodes load before relationships**, each with an `UNWIND ... MERGE` query and our `batched()` helper:
```python
for csv_name, query in NODE_QUERIES.items():
    n = load_file(driver, csv_name, query)
    print(f"loaded {n} rows from {csv_name}")

for csv_name, query in REL_QUERIES.items():
    n = load_file(driver, csv_name, query)
    print(f"loaded {n} rows from {csv_name}")
```
Nodes must exist before a relationship query's `MATCH` can find them, so the four node files (`people.csv`, `companies.csv`, `skills.csv`, `cities.csv`) always run before the five relationship files (`works_at.csv`, `knows.csv`, `has_skill.csv`, `lives_in.csv`, `located_in.csv`).

**5. Counts are printed at the end**, one line per label and per relationship type:
```python
def print_counts(driver) -> None:
    for row in driver.execute_query(
        "MATCH (n) RETURN labels(n)[0] AS label, count(*) AS count ORDER BY label",
        database_="neo4j",
    ).records:
        print(f"  {row['label']}: {row['count']}")
    for row in driver.execute_query(
        "MATCH ()-[r]->() RETURN type(r) AS rel_type, count(*) AS count ORDER BY rel_type",
        database_="neo4j",
    ).records:
        print(f"  {row['rel_type']}: {row['count']}")
```

The `justfile` wraps the whole thing in a `load` recipe:
```just
load:
    uv run python -m neo4j_tutorial.load_data --reset
```

## Proving it works, and proving it's idempotent

First run, `just load` (starts from an empty database):

```bash
just load
```
```
reset: all nodes and relationships deleted
ensured 4 uniqueness constraints
loaded 12 rows from people.csv
loaded 4 rows from companies.csv
loaded 8 rows from skills.csv
loaded 4 rows from cities.csv
loaded 12 rows from works_at.csv
loaded 8 rows from knows.csv
loaded 22 rows from has_skill.csv
loaded 12 rows from lives_in.csv
loaded 4 rows from located_in.csv

Node counts:
  City: 4
  Company: 4
  Person: 12
  Skill: 8

Relationship counts:
  HAS_SKILL: 22
  KNOWS: 8
  LIVES_IN: 12
  LOCATED_IN: 4
  WORKS_AT: 12
```

Second run, `just load` again (this time it resets first, then reloads from a clean state again — the counts must be identical):

```bash
just load
```
```
reset: all nodes and relationships deleted
ensured 4 uniqueness constraints
loaded 12 rows from people.csv
loaded 4 rows from companies.csv
loaded 8 rows from skills.csv
loaded 4 rows from cities.csv
loaded 12 rows from works_at.csv
loaded 8 rows from knows.csv
loaded 22 rows from has_skill.csv
loaded 12 rows from lives_in.csv
loaded 4 rows from located_in.csv

Node counts:
  City: 4
  Company: 4
  Person: 12
  Skill: 8

Relationship counts:
  HAS_SKILL: 22
  KNOWS: 8
  LIVES_IN: 12
  LOCATED_IN: 4
  WORKS_AT: 12
```

Identical counts. Even more telling: running the loader **without** `--reset`, twice in a row, on top of already-loaded data, gives the exact same counts both times — nothing is duplicated, because every query is a `MERGE`:

```bash
uv run python -m neo4j_tutorial.load_data   # first, on top of existing data
uv run python -m neo4j_tutorial.load_data   # second, right after
```
Both print the same final block:
```
Node counts:
  City: 4
  Company: 4
  Person: 12
  Skill: 8

Relationship counts:
  HAS_SKILL: 22
  KNOWS: 8
  LIVES_IN: 12
  LOCATED_IN: 4
  WORKS_AT: 12
```

## Quick verification queries

Count a specific label or relationship type:
```bash
just cypher "MATCH (p:Person) RETURN count(p) AS people"
```
```
people
12
```
```bash
just cypher "MATCH ()-[r:WORKS_AT]->() RETURN count(r) AS works_at"
```
```
works_at
12
```

See the graph's *shape* — which labels connect to which via which relationship types — without listing every node:
```bash
just cypher "CALL db.schema.visualization() YIELD nodes, relationships RETURN [n IN nodes | labels(n)] AS node_labels, [r IN relationships | type(r)] AS rel_types"
```
```
node_labels, rel_types
[["Company"], ["Skill"], ["City"], ["Person"]], ["LOCATED_IN", "WORKS_AT", "LIVES_IN", "KNOWS", "HAS_SKILL"]
```

In the Browser UI (http://localhost:7476), running `MATCH (n) RETURN n LIMIT 50` after loading shows the same shape visually: four `Person` nodes' worth of clusters radiating `WORKS_AT` edges to 4 `Company` nodes, `LIVES_IN` edges to 4 `City` nodes (which the companies also connect to via `LOCATED_IN`), `HAS_SKILL` edges fanning out to 8 `Skill` nodes, and a handful of `KNOWS` edges directly between `Person` nodes — a small, densely connected social-and-work graph rather than rows in separate tables.

## Key takeaways

- `CREATE` always adds a new node; `MERGE` finds-or-creates by matching the whole pattern. Use `MERGE` for anything you might load more than once.
- Create uniqueness constraints *before* loading data — they stop duplicates and make `MERGE` fast via an index.
- Never build Cypher by pasting values into the query string — use parameters (`$name`), from `:param` in `cypher-shell` or as keyword arguments from the Python driver.
- `UNWIND $rows AS row` loads many rows in one query; batch a few hundred to a few thousand rows per transaction, not one row and not a million.
- `LOAD CSV WITH HEADERS FROM 'file:///...'` reads files from the `/import`-mounted `data/` folder directly in Cypher; every value comes in as a string, so cast numbers with `toInteger()`.
- `load_data.py` (`just load`) is the reusable, idempotent loader every later chapter relies on to (re)build the dataset.

Next: [03_basic_queries.md](03_basic_queries.md) — reading data with `MATCH`, `WHERE`, `RETURN`, ordering, paging and aggregation.
