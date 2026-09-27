# 01 — Concepts: the property-graph model, Cypher basics, schema, transactions

**What you will learn**
- What a graph database is, and the four building blocks of the property-graph model: node, relationship, property, path
- How the property-graph model compares to relational tables and joins
- The shape of Cypher (Neo4j's query language) queries: `CREATE`, `MATCH ... RETURN`, `MATCH ... SET`
- What constraints and indexes are, and how to see them with `SHOW CONSTRAINTS` / `SHOW INDEXES`
- What a transaction is, ACID (Atomicity, Consistency, Isolation, Durability), and the architecture words you'll meet later (Bolt, cypher-shell, APOC)

All examples below were run against the tutorial's Docker Neo4j (`just up` first, from `project/`). Every table under a `cypher` block is the real output from `just cypher "..."`.

## 1. What a graph database is

A **graph database** stores data as things and the connections between them, instead of as tables of rows. Neo4j uses the **property graph** model, which has exactly four building blocks:

- **Node** — a thing (a person, a company, a skill). Like a row, but not tied to one table.
- **Label** — a tag on a node that says what kind of thing it is (`:Person`, `:Company`). A node can have zero, one, or several labels.
- **Relationship** — a named, **directed** connection between exactly two nodes: it always has one start node and one end node, and a **type** (`KNOWS`, `WORKS_AT`). "Directed" just means it points from one node to the other, like an arrow.
- **Property** — a key/value pair attached to a node or a relationship (`{name: "Ann", age: 33}`).
- **Path** — a sequence of nodes connected by relationships, e.g. "Ann knows Bob who works at Acme".

ASCII art of one relationship:

```
 (a:Demo {name: "Ann"}) --- KNOWS {since: 2020} ---> (b:Demo {name: "Bob"})
      node, label                relationship             node, label
      property                     type + property
```

### Compared to a relational database

If you know SQL (Structured Query Language, used by relational databases like Postgres or MySQL), here is the same idea in both worlds:

| SQL term | Neo4j term |
|---|---|
| table | label |
| row | node |
| column | property |
| foreign key / join table | relationship |
| `JOIN` | pattern match, e.g. `(a)-[:KNOWS]->(b)` |

The key difference: in SQL, connecting two tables at query time means a `JOIN`, which gets slower and more complex the more tables you chain. In Neo4j, the relationship is stored once, up front, as a first-class object — following it is a direct pointer lookup, however many hops you chain.

## 2. Cypher: ASCII-art pattern matching

Cypher queries look like little drawings of the graph you're describing or searching for:

- `(a)` — a node, with variable `a` (a name you can reuce later in the query)
- `(a:Person)` — a node with label `Person`
- `(p:Person {name: "Ann"})` — a node with label `Person` and a **property map** (the `{...}` part) requiring `name` to equal `"Ann"`
- `(a)-[r]->(b)` — a relationship from `a` to `b`, stored in variable `r`, pointing right (the arrowhead shows direction)
- `(a)-[:KNOWS]->(b)` — a relationship with type `KNOWS`, no variable needed if you don't use it later
- `()-[]->()`  — **anonymous** nodes/relationships: you can omit the variable, the label, or both, whenever you don't need to refer to them again

### `CREATE` — write two nodes and a relationship

```cypher
CREATE (a:Demo {name: 'Ann'})-[:KNOWS {since: 2020}]->(b:Demo {name: 'Bob'})
```

This creates two throw-away nodes labelled `:Demo` (so they're easy to find and delete later) and one `KNOWS` relationship between them, in a single statement.

### `MATCH ... RETURN` — read it back

```cypher
MATCH (a:Demo)-[r:KNOWS]->(b:Demo)
RETURN a.name AS from_person, type(r) AS rel, r.since AS since, b.name AS to_person
```

Output:

| from_person | rel | since | to_person |
|---|---|---|---|
| "Ann" | "KNOWS" | 2020 | "Bob" |

`MATCH` finds every part of the graph that matches the pattern; `RETURN` picks which values come back. `type(r)` reads a relationship's type as text.

You can also return a whole **path** in one variable:

```cypher
MATCH p=(a:Demo)-[:KNOWS]->(b:Demo)
RETURN p
```

Output:

| p |
|---|
| (:Demo {name: "Ann", age: 33})-[:KNOWS {since: 2020}]->(:Demo {name: "Bob"}) |

(The `age: 33` shows up because we ran the next example first — Cypher prints the path exactly as it exists in the database right now.)

### `MATCH ... SET` — update a property

```cypher
MATCH (a:Demo {name: 'Ann'})
SET a.age = 33
RETURN a.name AS name, a.age AS age
```

Output:

| name | age |
|---|---|
| "Ann" | 33 |

`SET` adds or overwrites a property on whatever `MATCH` found.

## 3. Reading vs writing clauses

Cypher clauses split into two families. Details and more examples come in chapters 02–04; here's the one-line summary of each:

**Reading** (never change the data):
- `MATCH` — find nodes/relationships matching a pattern
- `OPTIONAL MATCH` — like `MATCH`, but keeps the row (with `null`s) even if nothing matches, instead of dropping it
- `WHERE` — filter matched rows by a condition
- `RETURN` — choose what comes back from the query
- `WITH` — pass intermediate results (optionally reshaped) to the next part of the query, like a pipe

**Writing** (change the data):
- `CREATE` — add new nodes/relationships, always, even if similar ones already exist
- `MERGE` — find a node/relationship matching a pattern, or create it if it's missing (avoids duplicates)
- `SET` — add or overwrite properties (or labels)
- `REMOVE` — delete a property or a label from a node
- `DELETE` — remove nodes or relationships (nodes must have their relationships deleted first, or use `DETACH DELETE`)

## 4. Schema: optional, but you can add rules

Neo4j is **schema-optional**: unlike a relational database, you don't have to declare labels or properties before using them — you just start writing data. But you can add two kinds of rules on top, once you know your data's shape.

### Constraints

A **constraint** is a rule Neo4j enforces on every write, rejecting any change that would break it.

- **Uniqueness constraint** — no two nodes with the same label can share the same value for a property. Available in Neo4j Community Edition.
- **Node key constraint** — like uniqueness, but across a *combination* of properties (a composite key). Requires **Neo4j Enterprise Edition**.
- **Property existence constraint** — every node with a label must have a given property. Requires **Neo4j Enterprise Edition**.

Create one, look at it, then drop it:

```cypher
CREATE CONSTRAINT demo_name IF NOT EXISTS
FOR (d:Demo) REQUIRE d.name IS UNIQUE
```

```cypher
SHOW CONSTRAINTS
```

Output:

| id | name | type | entityType | labelsOrTypes | properties | ownedIndex | propertyType |
|---|---|---|---|---|---|---|---|
| 4 | "demo_name" | "UNIQUENESS" | "NODE" | ["Demo"] | ["name"] | "demo_name" | NULL |

Notice Neo4j also created an index for it automatically (uniqueness constraints need one internally to check fast).

```cypher
SHOW INDEXES
```

Output:

| id | name | state | populationPercent | type | entityType | labelsOrTypes | properties | indexProvider |
|---|---|---|---|---|---|---|---|---|
| 3 | "demo_name" | "ONLINE" | 100.0 | "RANGE" | "NODE" | ["Demo"] | ["name"] | "range-1.0" |
| 1 | "index_343aff4e" | "ONLINE" | 100.0 | "LOOKUP" | "NODE" | NULL | NULL | "token-lookup-1.0" |
| 2 | "index_f7700477" | "ONLINE" | 100.0 | "LOOKUP" | "RELATIONSHIP" | NULL | NULL | "token-lookup-1.0" |

The two `LOOKUP` indexes exist by default in every new database — they let Neo4j find nodes/relationships by label or type quickly, even with no constraints defined.

```cypher
DROP CONSTRAINT demo_name
```

### Indexes

An **index** makes lookups on a property fast, without enforcing any rule (unlike a constraint). Neo4j has several kinds:

- **Range index** — the default kind, good for equality and range lookups (`=`, `<`, `>`, `IN`) on numbers, strings, dates, etc.
- **Text index** — optimized for string-specific operations like `CONTAINS` and `STARTS WITH`.
- **Point index** — for spatial (`point()`) properties, e.g. geographic coordinates.
- **Full-text index** — free-text search across one or more properties, similar to a search engine (used in chapter 04).
- **Vector index** — stores embeddings (lists of numbers representing meaning, produced by machine-learning models) for similarity search, e.g. "find nodes semantically similar to this one".

## 5. Transactions and ACID

A **transaction** is a group of writes that either all succeed or all fail together — nothing is left half-done. Every single Cypher statement you run, even a one-line `CREATE`, is automatically wrapped in its own transaction.

Neo4j (like a relational database) guarantees **ACID** properties for transactions:

- **Atomicity** — a transaction's writes all happen, or none do.
- **Consistency** — a transaction can never leave the database violating a constraint you defined.
- **Isolation** — transactions running at the same time don't see each other's half-finished changes.
- **Durability** — once a transaction commits (finishes successfully), the change survives even a crash right afterward.

You can also group several statements into one **explicit transaction**:
- In `cypher-shell`, type `:begin`, run several statements, then `:commit` (or `:rollback` to undo).
- From Python, the driver's session object offers the same thing (`session.begin_transaction()`) — covered in chapter 05.

## 6. Architecture words you will meet

- **Database vs DBMS** — the **DBMS** (Database Management System) is the running Neo4j server process; a **database** is one named set of data inside it. One DBMS can host several databases.
- **`system` and `neo4j` databases** — every DBMS ships with a `system` database (metadata: users, other databases, roles) and a default database, normally named `neo4j` (that's where our tutorial data lives).

```cypher
SHOW DATABASES
```

Output (trimmed to the relevant columns):

| name | type | currentStatus | default |
|---|---|---|---|
| "neo4j" | "standard" | "online" | TRUE |
| "system" | "system" | "online" | FALSE |

- **Bolt** (Neo4j's binary network protocol used by drivers) — normally port 7687; ours is remapped to **7689** because another Neo4j (Neo4j Desktop) already uses 7687 **and** 7688 on this machine (see `index.md`).
- **HTTP + Browser** — Neo4j Browser, the web UI, talks over HTTP; normally port 7474, ours is remapped to **7476**.
- **cypher-shell** — Neo4j's command-line client (used by `just cypher "..."` and `just shell`), talks over Bolt too.
- **APOC** (Awesome Procedures On Cypher) — a plugin library bundled with our Docker image that adds hundreds of extra procedures and functions Cypher doesn't have built in.

```cypher
RETURN apoc.version() AS apoc_version
```

Output:

| apoc_version |
|---|
| "5.26.29" |

- **Procedures vs functions** — a **function** (like `type()`, `apoc.version()`) is called inline inside an expression and returns one value per row. A **procedure** is called with `CALL procedure.name(...)` on its own line, can take multiple rows as input and yield multiple rows/columns as output — used for things like full-text search or algorithms.

## 7. When to reach for a graph database

**Good fit:**
- Many-to-many relationships (people who know people who know people)
- Questions about paths: "how are these two things connected?", "what's the shortest route?"
- Variable-depth traversals: "friends of friends of friends", without knowing in advance how many hops
- Recommendations ("people who bought X also bought Y")
- Knowledge graphs: entities and how they relate, where the relationships matter as much as the entities

**Poor fit:**
- Bulk aggregation over flat, unconnected data (e.g. "sum this column across 50 million rows") — a columnar or relational database is faster and simpler
- Simple key-value lookups with no relationships to traverse — a key-value store is lighter-weight and simpler to run

## 8. Vocabulary cheat-sheet

| term | meaning |
|---|---|
| node | a thing; roughly like a row |
| label | tag naming what kind of thing a node is; roughly like a table name |
| relationship | a directed, typed connection between exactly two nodes |
| property | a key/value pair on a node or relationship |
| path | a chain of nodes connected by relationships |
| Cypher | Neo4j's query language |
| `MATCH` | find nodes/relationships matching a pattern (read) |
| `CREATE` | add new nodes/relationships (write, always inserts) |
| `MERGE` | find-or-create (write, avoids duplicates) |
| constraint | a rule Neo4j enforces on every write (e.g. uniqueness) |
| index | a lookup structure that speeds up queries, enforces nothing |
| transaction | a group of writes that all succeed or all fail together |
| ACID | Atomicity, Consistency, Isolation, Durability — transaction guarantees |
| DBMS | Database Management System — the running Neo4j server |
| Bolt | Neo4j's binary network protocol used by drivers (ours: port 7689) |
| cypher-shell | Neo4j's command-line client |
| APOC | Awesome Procedures On Cypher — a plugin library of extra procedures/functions |
| procedure | called with `CALL`, can take/return multiple rows |
| function | called inline in an expression, returns one value per row |

## Cleanup

```cypher
DROP CONSTRAINT demo_name
```

```cypher
MATCH (n:Demo) DETACH DELETE n
```

`DETACH DELETE` removes a node together with any relationships attached to it — plain `DELETE` would refuse to delete a node that still has relationships.

## Key takeaways

- The property graph model has four parts: nodes (things), labels (types), relationships (directed, typed connections), and properties (key/value data) — plus paths, which chain them together.
- Cypher queries are literal drawings of the pattern you want: `(a)-[r]->(b)`, with labels, variables and `{property: value}` maps.
- Constraints enforce rules (uniqueness, and in Enterprise Edition, node keys and property existence); indexes only speed up lookups. `SHOW CONSTRAINTS` / `SHOW INDEXES` list what's active.
- Every Cypher statement runs inside an ACID transaction automatically; `cypher-shell`'s `:begin`/`:commit` and the Python driver let you group several statements into one explicit transaction.
- Graph databases shine at many-to-many, variable-depth, path-shaped questions; plain aggregation over flat data is often better served by a relational or columnar database.

Next: [02_insert_data.md](02_insert_data.md) — inserting data: `CREATE` vs `MERGE`, constraints first, batch loading with `UNWIND` and parameters, `LOAD CSV`, idempotent loaders from Python.
