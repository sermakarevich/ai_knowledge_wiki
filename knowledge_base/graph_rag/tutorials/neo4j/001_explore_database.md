# 001 — Exploring an unknown database: what is actually inside it?

**What you will learn**
- Three ways to look inside a Neo4j database: the browser UI, `cypher-shell` (Neo4j's command-line query tool), and Python
- The inventory procedures (`db.labels()`, `db.relationshipTypes()`, `db.propertyKeys()`) and what a **procedure** is
- How to count nodes and relationships, and how to see which labels connect to which other labels via which relationship — the "shape" of the graph
- How to inspect properties per label/relationship type, their data types, and sample values, using both built-in and APOC (Awesome Procedures On Cypher, a plugin bundled in our Docker image) tools
- Structure and health checks (orphan nodes, duplicates, self-loops), plus indexes, constraints, and a reusable `describe_database()` recipe

All examples below were run against the tutorial's Docker Neo4j (`just up` first, from `project/`). Every code block under a `cypher` heading shows the real output from `just cypher "..."` against our "tech people" dataset (see [index.md](index.md) for the full schema).

## 0. The scenario

Someone hands you connection details to a Neo4j database. Nobody gave you a schema diagram or documentation. Before you can write a single useful query, you need to answer: what kinds of things (**labels**) are in there, how are they connected (**relationship types**), what data (**properties**) do they carry, and how much of it is there? This chapter is a checklist and toolbox for exactly that situation.

## 1. Three ways to look

| Tool | When to use it |
|---|---|
| **Browser UI** (http://localhost:7476) | First 30 seconds with a new database — the left sidebar shows a live "Database information" panel with labels, relationship types and property keys with no typing required. Good for visually exploring a small result set (click a node to expand its neighbors). |
| **`cypher-shell`** (`just shell` for an interactive session, `just cypher "..."` for one-off queries) | Scripting, quick checks from a terminal, copy-pasting a query you found in documentation. No graphics, but fast and scriptable. |
| **Python** (`just explore` / `just describe`) | Programmatic exploration — looping over results, building a report, feeding results into pandas or another tool. Best when you want to save or reuse the output. |

In the browser (http://localhost:7476, login `neo4j` / `tutorial123`), the left sidebar's "Database information" panel lists labels, relationship types and property keys as clickable pills — clicking one runs a `MATCH` for you. Two special commands typed into the query box are worth knowing:
- `:schema` — lists indexes and constraints (same data as `SHOW INDEXES` / `SHOW CONSTRAINTS`, see §7).
- `:sysinfo` — shows store sizes, IDs in use, and version/edition info for the whole DBMS (Database Management System).

From the terminal:

```bash
just shell                       # interactive cypher-shell session
just cypher "RETURN 1 AS one"    # one-off query, no session needed
```

From Python:

```bash
just explore                     # run every query in this chapter
just explore label_rel_label     # run one query by name
just describe                    # print the compact describe_database() summary
```

## 2. Inventory procedures: what labels, relationship types and property keys exist

A **procedure** is a built-in (or plugin-provided) routine you invoke with `CALL name()`, similar to calling a function in a programming language, but it can return a table of rows instead of a single value. When a procedure returns columns you want to rename or filter, you `YIELD` them first (`CALL proc() YIELD col1, col2 ...`); if you just want everything a procedure returns, plain `CALL proc()` is enough.

```cypher
CALL db.labels()
```

```
label
"Person"
"Company"
"Skill"
"City"
```

```cypher
CALL db.relationshipTypes()
```

```
relationshipType
"KNOWS"
"WORKS_AT"
"HAS_SKILL"
"LIVES_IN"
"LOCATED_IN"
```

```cypher
CALL db.propertyKeys()
```

```
propertyKey
"name", "since", "age", "industry", "founded", "country", "role", "level", "nickname", "senior"
```

Notice `nickname` and `senior` in that list — no node or relationship in our current dataset actually uses them. Property keys (like labels and relationship types) are stored in a small internal **token table** that only ever grows: once Neo4j sees a property name, it keeps the token even after every node using it is deleted. So `db.propertyKeys()` tells you every key ever used, not necessarily every key in use right now — always cross-check against `db.schema.nodeTypeProperties()` (§5) for what is actually present today.

```cypher
SHOW DATABASES
```

```
name, type, aliases, access, address, role, writer, requestedStatus, currentStatus, statusMessage, default, home, constituents
"neo4j", "standard", [], "read-write", "localhost:7687", "primary", TRUE, "online", "online", "", TRUE, TRUE, []
"system", "system", [], "read-write", "localhost:7687", "primary", TRUE, "online", "online", "", FALSE, FALSE, []
```

Every Neo4j instance has a `system` database for internal bookkeeping (users, other databases) alongside your actual data — that's why there are two rows even though we only ever query `neo4j`.

## 3. Counting: how much of everything is there

```cypher
MATCH (n) RETURN labels(n) AS labels, count(*) AS n ORDER BY n DESC
```

```
labels, n
["Person"], 12
["Skill"], 8
["Company"], 4
["City"], 4
```

```cypher
MATCH ()-[r]->() RETURN type(r) AS rel, count(*) AS n ORDER BY n DESC
```

```
rel, n
"HAS_SKILL", 22
"WORKS_AT", 12
"LIVES_IN", 12
"KNOWS", 8
"LOCATED_IN", 4
```

Total counts:

```cypher
MATCH (n) RETURN count(n) AS total_nodes        // 28
MATCH ()-[r]->() RETURN count(r) AS total_rels  // 58
```

`MATCH (n:Person) RETURN count(n)` on a **single label with no filter** is answered from Neo4j's internal count-store (a small set of running totals it keeps up to date automatically) rather than by scanning every node, so it's effectively O(1) — fast even on a huge database. As soon as you add a `WHERE` clause or match a pattern with a relationship, Neo4j has to actually read data, so it gets slower as the database grows.

On a big, unfamiliar database, the fastest way to get an overview is the APOC (Awesome Procedures On Cypher — the plugin bundled in our Docker image) meta-statistics procedure:

```cypher
CALL apoc.meta.stats() YIELD labelCount, relTypeCount, propertyKeyCount, nodeCount, relCount
RETURN labelCount, relTypeCount, propertyKeyCount, nodeCount, relCount
```

```
labelCount, relTypeCount, propertyKeyCount, nodeCount, relCount
4, 5, 10, 28, 58
```

Note `propertyKeyCount` is 10, matching the "ever used" token list from §2, not the 9 properties actually attached to nodes/relationships today.

**A note on labels that don't fit these queries cleanly:** a node can have *several* labels (e.g. a node tagged both `:Person` and `:Employee`) — `labels(n)` returns a list, so `GROUP BY labels(n)` treats `["Person"]` and `["Person", "Employee"]` as different groups; watch for that if counts look off. A node can also have **zero** labels — it will show up as `n` (no label) in `db.labels()`-based queries but still appear under `MATCH (n) RETURN count(n)`. Our dataset has no multi-label or label-less nodes, but real-world databases sometimes do.

## 4. Who connects to whom: the shape of the graph

This is the single most useful query in this chapter — it tells you, for every relationship in the database, which label it starts from, which type it is, and which label it ends at:

```cypher
MATCH (a)-[r]->(b)
RETURN labels(a) AS from, type(r) AS rel, labels(b) AS to, count(*) AS n
ORDER BY n DESC
```

```
from, rel, to, n
["Person"], "HAS_SKILL", ["Skill"], 22
["Person"], "WORKS_AT", ["Company"], 12
["Person"], "LIVES_IN", ["City"], 12
["Person"], "KNOWS", ["Person"], 8
["Company"], "LOCATED_IN", ["City"], 4
```

Read this table like an ER (Entity-Relationship) diagram: `Person -[HAS_SKILL]-> Skill` means a Person node points to a Skill node via a `HAS_SKILL` relationship, and it happens 22 times. If a relationship type showed up with more than one `(from, to)` pair — say `KNOWS` connecting both `Person→Person` and `Person→Company` — that would be a red flag that the same relationship type is being reused for two different meanings, worth asking the data owner about.

Two ways to get the same picture without writing the aggregation yourself:

```cypher
CALL db.schema.visualization()
```

This is exactly what the browser UI's graph view draws when you visit http://localhost:7476: one representative node per label plus the relationship types connecting them, not real data. Useful to eyeball quickly, but the table above is easier to read as text and additionally tells you *how many* relationships of each kind exist.

```cypher
CALL apoc.meta.schema() YIELD value RETURN value
```

This APOC procedure returns one large map keyed by label/relationship-type name. For a node label it includes `count`, `properties` (name → type/indexed/unique), and `relationships` (each connected relationship type with its own `count`, `direction`, and the labels on the other end). For example our result's `Person` entry shows `KNOWS: {count: 4, direction: "out", labels: ["Person"]}` — `apoc.meta.schema()` reports directed relationships once per direction, so a symmetric-looking `KNOWS` count here (4) is half of the `rels_per_type` total (8) because it's counted from the `Person` side only. It's more detail than you usually need for a first look, but useful once you want properties and relationships in a single call.

## 5. Properties: what data does each label/relationship carry, and what type is it?

The quickest built-in answer:

```cypher
CALL db.schema.nodeTypeProperties()
```

```
nodeType, nodeLabels, propertyName, propertyTypes, mandatory
":`Person`", ["Person"], "name", ["String"], TRUE
":`Person`", ["Person"], "age", ["Long"], TRUE
":`Company`", ["Company"], "name", ["String"], TRUE
":`Company`", ["Company"], "industry", ["String"], TRUE
":`Company`", ["Company"], "founded", ["Long"], TRUE
":`Skill`", ["Skill"], "name", ["String"], TRUE
":`City`", ["City"], "name", ["String"], TRUE
":`City`", ["City"], "country", ["String"], TRUE
```

```cypher
CALL db.schema.relTypeProperties()
```

```
relType, propertyName, propertyTypes, mandatory
":`KNOWS`", "since", ["Long"], TRUE
":`WORKS_AT`", "since", ["Long"], TRUE
":`WORKS_AT`", "role", ["String"], TRUE
":`HAS_SKILL`", "level", ["String"], TRUE
":`LIVES_IN`", NULL, NULL, FALSE
":`LOCATED_IN`", NULL, NULL, FALSE
```

Columns that matter: `propertyTypes` is a list because in principle the same property could hold different types on different nodes (Neo4j does not enforce a single type per property the way a SQL column does); `mandatory` means every sampled node/relationship of that type actually had the property, not that it's enforced — Neo4j has no built-in "NOT NULL" for properties (only *existence constraints* in Enterprise edition can enforce that, and our Community edition image doesn't have them). A `NULL propertyName` row (as for `LIVES_IN`/`LOCATED_IN` above) means that relationship type carries no properties at all — a normal, valid outcome, not an error.

**The manual equivalent**, useful when you want to check how *consistently* a property is filled rather than just whether it appears at least once:

```cypher
MATCH (p:Person) UNWIND keys(p) AS key RETURN key, count(*) AS n ORDER BY n DESC
```

```
key, n
"name", 12
"age", 12
```

Both properties appear on all 12 `Person` nodes — fully consistent. On a messier database you might see `email` at 12 and `phone` at only 3, telling you `phone` is optional in practice even if nothing declares it optional.

Other small, useful checks:

```cypher
MATCH (p:Person) RETURN properties(p) AS props LIMIT 1
```

```
props
{name: "Anna Schmidt", age: 29}
```

`properties(n)` dumps every property of one sample node as a map — the fastest way to "just show me one example."

```cypher
MATCH (c:Company) RETURN collect(DISTINCT c.industry)[..5] AS industries
```

```
industries
["Software", "Data Analytics", "Cloud Infrastructure", "AI Research"]
```

`collect(DISTINCT ...)[..5]` samples up to 5 distinct values of a property — handy for a categorical-looking property when you don't want to print all of them.

```cypher
MATCH (p:Person) RETURN min(p.age) AS min_age, max(p.age) AS max_age, avg(p.age) AS avg_age
```

```
min_age, max_age, avg_age
24, 50, 34.58333333333333
```

```cypher
MATCH ()-[r:HAS_SKILL]->() RETURN DISTINCT r.level AS level
```

```
level
"expert"
"intermediate"
"beginner"
```

For type-checking a single value in code or an ad-hoc query, Neo4j 5 has a built-in `valueType()` function (`RETURN valueType(p.age)` → `"INTEGER"`), and APOC has the equivalent `apoc.meta.cypher.type(x)`. Both are mostly useful when you're not sure whether a property is a string, a number, or a list, and want to check without eyeballing raw data.

## 6. Structure and health checks

Degree (how many relationships touch a node, in either direction) using `COUNT { pattern }`, a Neo4j 5 subquery-counting syntax:

```cypher
MATCH (p:Person) RETURN p.name AS name, COUNT { (p)--() } AS degree ORDER BY degree DESC LIMIT 5
```

```
name, degree
"Nina Wagner", 6
"Lucia Ferreira", 6
"Anna Schmidt", 6
"Marek Nowak", 6
"David Klein", 6
```

Orphan nodes (no relationships at all — often leftover test data or a sign of an incomplete import):

```cypher
MATCH (n) WHERE COUNT { (n)--() } = 0 RETURN labels(n) AS labels, count(*) AS n
```

Empty result on our dataset — every node has at least one relationship.

Duplicate-looking nodes (same `name`, different underlying identity — a common data-quality bug from double imports):

```cypher
MATCH (p:Person) WITH p.name AS name, count(*) AS n WHERE n > 1 RETURN name, n
```

Also empty — no duplicate `Person` names. If it weren't empty, `elementId(n)` (Neo4j's internal, string-typed node/relationship identifier, replacing the older integer `id(n)`) would let you tell the duplicates apart:

```cypher
MATCH (p:Person) RETURN elementId(p) AS id LIMIT 2
```

```
id
"4:cbb9fadc-0ac3-4ef3-b113-b227115ff73b:115"
"4:cbb9fadc-0ac3-4ef3-b113-b227115ff73b:116"
```

Self-loops (a relationship from a node back to itself — sometimes a bug, sometimes intentional, e.g. "self-review"):

```cypher
MATCH (n)-[r]->(n) RETURN type(r) AS rel, count(*) AS n
```

Empty — none in our data.

Dangling direction checks — e.g. does any `KNOWS` pair exist in **both** directions (`A KNOWS B` and `B KNOWS A` as two separate relationships), which usually means the data models a symmetric relationship redundantly instead of relying on `MATCH (a)-[:KNOWS]-(b)` (no arrow = either direction):

```cypher
MATCH (a:Person)-[:KNOWS]->(b:Person) WHERE (b)-[:KNOWS]->(a) RETURN a.name AS a, b.name AS b
```

Empty — every `KNOWS` relationship in our dataset is one-directional only.

## 7. Indexes, constraints and metadata

```cypher
SHOW INDEXES
```

```
name            type      entityType  labelsOrTypes  properties
city_name       RANGE     NODE        [City]         [name]
company_name    RANGE     NODE        [Company]      [name]
index_343aff4e  LOOKUP    NODE        (none)         (none)
index_f7700477  LOOKUP    RELATIONSHIP (none)        (none)
person_age      RANGE     NODE        [Person]       [age]
person_name     RANGE     NODE        [Person]       [name]
person_names    FULLTEXT  NODE        [Person]       [name]
skill_name      RANGE     NODE        [Skill]        [name]
```

Columns that matter: `type` (`RANGE` for ordinary equality/range lookups, `LOOKUP` for the automatic "find any node with this label" index every database has by default, `FULLTEXT` for text search), `entityType` (`NODE` or `RELATIONSHIP` — relationships can be indexed too), `labelsOrTypes` + `properties` (what the index actually covers), and `state` (should say `ONLINE`; anything else means the index is still building or broken).

```cypher
SHOW CONSTRAINTS
```

```
name            type        entityType  labelsOrTypes  properties  ownedIndex
city_name       UNIQUENESS  NODE        [City]         [name]      city_name
company_name    UNIQUENESS  NODE        [Company]      [name]      company_name
person_name     UNIQUENESS  NODE        [Person]       [name]      person_name
skill_name      UNIQUENESS  NODE        [Skill]        [name]      skill_name
```

Every uniqueness constraint automatically creates a backing index with the same name (`ownedIndex`) — that's why `person_name` shows up in both `SHOW INDEXES` and `SHOW CONSTRAINTS`.

Which APOC meta-procedures are available (useful when you're not sure if this Neo4j build has APOC, or which version):

```cypher
SHOW PROCEDURES YIELD name WHERE name STARTS WITH 'apoc.meta'
```

```
name
"apoc.meta.data"
"apoc.meta.data.of"
"apoc.meta.graph"
"apoc.meta.graph.of"
"apoc.meta.graphSample"
"apoc.meta.nodeTypeProperties"
"apoc.meta.relTypeProperties"
"apoc.meta.schema"
"apoc.meta.stats"
"apoc.meta.subGraph"
```

`SHOW FUNCTIONS` works the same way but lists Cypher functions instead of procedures — useful for checking whether a function like `valueType()` is available in this Neo4j version.

Server version and edition:

```cypher
CALL dbms.components() YIELD name, versions, edition RETURN name, versions, edition
```

```
name, versions, edition
"Neo4j Kernel", ["5.26.29"], "community"
```

Community edition (free, no clustering, no existence/type constraints) vs. Enterprise (paid, adds clustering and stronger constraints) — good to know before you assume a feature is available.

```cypher
CALL db.info()
```

```
id, name, creationDate
"051FF0E447485F119B15AB078A47FDFBA324B5864D58E591BB9540DADBE7991A", "neo4j", "2026-08-28T13:20:53.056Z"
```

## 8. A reusable recipe

The `explore.py` module (`project/src/neo4j_tutorial/explore.py`) collects every query from this chapter into a `QUERIES` dict, runnable individually or all at once:

```bash
just explore                    # every query in this chapter, one after another
just explore label_rel_label    # just the "who connects to whom" table
```

It also has a `describe_database()` function that prints a compact summary in one shot — this is the real output on our dataset:

```bash
just describe
```

```
=== Node counts per label ===
  ['Person']: 12
  ['Skill']: 8
  ['Company']: 4
  ['City']: 4

=== Relationship counts per type ===
  HAS_SKILL: 22
  WORKS_AT: 12
  LIVES_IN: 12
  KNOWS: 8
  LOCATED_IN: 4

=== Who connects to whom (label -[REL]-> label) ===
  ['Person'] -[HAS_SKILL]-> ['Skill']: 22
  ['Person'] -[WORKS_AT]-> ['Company']: 12
  ['Person'] -[LIVES_IN]-> ['City']: 12
  ['Person'] -[KNOWS]-> ['Person']: 8
  ['Company'] -[LOCATED_IN]-> ['City']: 4

=== Properties per label ===
  Person: name (String), age (Long)
  Company: name (String), industry (String), founded (Long)
  Skill: name (String)
  City: name (String), country (String)

=== Properties per relationship type ===
  :`KNOWS`: since (Long)
  :`WORKS_AT`: since (Long), role (String)
  :`HAS_SKILL`: level (String)

=== Indexes ===
  city_name (RANGE) on ['City'] ['name']
  company_name (RANGE) on ['Company'] ['name']
  index_343aff4e (LOOKUP) on None None
  index_f7700477 (LOOKUP) on None None
  person_age (RANGE) on ['Person'] ['age']
  person_name (RANGE) on ['Person'] ['name']
  person_names (FULLTEXT) on ['Person'] ['name']
  skill_name (RANGE) on ['Skill'] ['name']

=== Constraints ===
  city_name (UNIQUENESS) on ['City'] ['name']
  company_name (UNIQUENESS) on ['Company'] ['name']
  person_name (UNIQUENESS) on ['Person'] ['name']
  skill_name (UNIQUENESS) on ['Skill'] ['name']
```

### First 10 minutes with an unknown Neo4j — checklist

1. Confirm you can connect (`just check` / `CALL db.info()`), and note the version and edition (`CALL dbms.components()`).
2. List labels, relationship types, property keys (`db.labels()`, `db.relationshipTypes()`, `db.propertyKeys()`).
3. Count nodes per label and relationships per type (`MATCH (n) RETURN labels(n), count(*)`, or `apoc.meta.stats()` for a one-shot summary).
4. Run the "who connects to whom" query — this is your mental map of the schema.
5. For each label, list its properties and types (`db.schema.nodeTypeProperties()`); same for relationship types.
6. Sample a few real values per property to sanity-check the types (`properties(n)`, `collect(DISTINCT ...)[..5]`).
7. Check for orphan nodes, duplicate-looking nodes, self-loops — quick data-quality smell tests.
8. List indexes and constraints (`SHOW INDEXES`, `SHOW CONSTRAINTS`) — tells you what queries are expected to be fast, and what uniqueness is guaranteed.
9. Check whether APOC is installed (`SHOW PROCEDURES YIELD name WHERE name STARTS WITH 'apoc'`) — it unlocks much richer exploration if so.
10. Write down what you found (even a short note) — the next person to touch this database will thank you.

## Key takeaways

- The browser UI's sidebar, `cypher-shell`, and Python each answer "what's in here?" — pick browser for a first glance, `cypher-shell` for quick scripted checks, Python when you want to save or process the output.
- `db.labels()`, `db.relationshipTypes()`, `db.propertyKeys()` give you the vocabulary of an unknown database; a **procedure** is called with `CALL name() YIELD col1, col2` when you want specific columns.
- `MATCH (a)-[r]->(b) RETURN labels(a), type(r), labels(b), count(*)` is the single most valuable query for understanding a graph's shape; `apoc.meta.schema()` gives the same information as a nested map with more detail.
- `db.schema.nodeTypeProperties()` / `db.schema.relTypeProperties()` list every property and its type per label/relationship type; always sample real values too, since types and "mandatory" are inferred from the data, not enforced by Neo4j (except via Enterprise-only constraints).
- `SHOW INDEXES` / `SHOW CONSTRAINTS` tell you what's fast and what's guaranteed unique; `CALL dbms.components()` tells you the version and edition you're working with.
- `explore.py`'s `describe_database()` packages this whole checklist into one command (`just describe`) you can reuse on any Neo4j database.

Next: [01_concepts.md](01_concepts.md) — the property-graph model, Cypher basics, indexes, constraints and transactions.
