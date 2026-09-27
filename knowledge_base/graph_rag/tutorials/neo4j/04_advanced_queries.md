# 04 — Advanced queries: paths, subqueries, updates, indexes, performance

**What you will learn**
- Variable-length and shortest-path patterns, and how to read a `path` value (`length`, `nodes`, `relationships`)
- List and map functions (`reduce`, comprehensions, map projection) that let you shape data inside Cypher
- `CASE`, `UNION`, and the modern subquery clauses `EXISTS {}`, `COUNT {}`, `COLLECT {}`, `CALL {}`
- How to write safely: `SET`/`REMOVE`, `DELETE` vs `DETACH DELETE`, `MERGE` on a relationship, `FOREACH` — every example paired with its undo
- Indexes (range and full-text), and how to read `EXPLAIN`/`PROFILE` output to see whether an index is actually used

All read-only queries below live in `project/src/neo4j_tutorial/queries_advanced.py` as a dict named `QUERIES`. Run any one of them, or all of them:

```bash
just query-advanced                          # run every read-only query
just query-advanced shortest_path_knows       # run just one, by name
```

Write examples (`SET`, `DELETE`, `MERGE`, `FOREACH`, index creation) are **not** in that module — they mutate the database, so they only appear here in the chapter text, each one immediately followed by the statement that undoes it. At the very end we run `just load` to restore the dataset to its original state, so the DoD checks in `index.md` still hold.

Every result below is the *real* output of running that query against our loaded dataset (12 `Person`, 4 `Company`, 8 `Skill`, 4 `City` nodes — see `index.md`). The Neo4j server is version 5.26.29 community edition (checked with `CALL dbms.components()`), which supports both the classic `shortestPath()`/`allShortestPaths()` functions and the newer GQL-style quantified path patterns (`-[:TYPE]-{1,5}`, `SHORTEST k`).

## Variable-length paths

A relationship pattern can repeat: `-[:KNOWS*1..3]->` means "follow one to three `KNOWS` relationships in a row". This is how you express "friend of a friend" or "reachable within N hops" without writing N separate `MATCH` clauses.

Our `KNOWS` edges form two chains (see `data/knows.csv`):
`Anna → Marek → Lucia → Tom` and `Anna → Nina → Piotr`, plus two unconnected pairs.

```cypher
MATCH p = (a:Person {name: 'Anna Schmidt'})-[:KNOWS*1..3]->(b:Person)
RETURN b.name AS name, length(p) AS len
ORDER BY len, name
```
```
             name  len
0     Marek Nowak    1
1     Nina Wagner    1
2  Lucia Ferreira    2
3 Piotr Zielinski    2
4      Tom Becker    3
```

`p = (pattern)` binds the whole match as a **path value** — a value that carries all the nodes and relationships it walked through, in order. Three functions read it apart:

- **`length(p)`** — the number of relationships in the path (an `int`). Only works on a path, not on a list.
- **`nodes(p)`** — a list of every node the path visited, start to end.
- **`relationships(p)`** — a list of every relationship the path walked, start to end. Use `size(relationships(p))` for a count — `length()` only accepts a path, not a list, so `length(relationships(p))` is a type error.

```cypher
MATCH p = (a:Person {name: 'Anna Schmidt'})-[:KNOWS*1..3]->(b:Person)
WHERE b.name = 'Tom Becker'
RETURN [x IN nodes(p) | x.name] AS names, size(relationships(p)) AS nrels
```
```
                                            names  nrels
0  [Anna Schmidt, Marek Nowak, Lucia Ferreira, Tom Becker]      3
```

`[x IN nodes(p) | x.name]` is a **list comprehension**: for each node `x` in the path's node list, keep `x.name`. It's covered in full in the next section.

### The unbounded `*` warning

`-[:KNOWS*]->` (no bounds) means "any number of hops, including very many". On a small tutorial graph like ours it's harmless, but on a real graph it can explore an enormous number of paths — the number of possible paths grows exponentially with each extra hop, especially in a densely connected graph, and an unbounded variable-length match can make a query scan far more of the graph than you intended, or never return. Always give it an upper bound, e.g. `*1..5`, unless you specifically want a shortest-path search (see below), which is a different, cheaper algorithm.

### Friends-of-friends who are not direct friends

A classic "people you may know" query: find everyone two `KNOWS` hops away from Anna, in either direction, but exclude Anna herself and anyone already directly connected to her.

```cypher
MATCH (a:Person {name: 'Anna Schmidt'})-[:KNOWS]-()-[:KNOWS]-(fof:Person)
WHERE fof <> a AND NOT (a)-[:KNOWS]-(fof)
RETURN DISTINCT fof.name AS friend_of_friend
ORDER BY friend_of_friend
```
```
  friend_of_friend
0   Lucia Ferreira
1  Piotr Zielinski
```

`(a)-[:KNOWS]-()-[:KNOWS]-(fof)` is two fixed-length hops through an anonymous middle node `()` — that's a plain pattern, not `*`, so it only ever explores exactly two hops. `NOT (a)-[:KNOWS]-(fof)` is a pattern used as a boolean inside `WHERE`: "there is no direct `KNOWS` edge between `a` and `fof`". `DISTINCT` is needed because the same `fof` can be reached through more than one middle person.

## Shortest paths

`shortestPath()` and `allShortestPaths()` are special functions that only work wrapped around a variable-length pattern — Neo4j uses a dedicated breadth-first search instead of enumerating every path, which is why they scale far better than `*` alone for "what's the shortest route" questions.

```cypher
MATCH (a:Person {name: 'Anna Schmidt'}), (b:Person {name: 'Tom Becker'}),
      p = shortestPath((a)-[:KNOWS*]-(b))
RETURN [x IN nodes(p) | x.name] AS path, size(relationships(p)) AS hops
```
```
                                       path  hops
0  [Anna Schmidt, Marek Nowak, Lucia Ferreira, Tom Becker]     3
```

`shortestPath` returns **one** shortest path (if several exist, one is picked arbitrarily). `allShortestPaths` returns **every** path that ties for shortest:

```cypher
MATCH (a:Person {name: 'Anna Schmidt'}), (b:Person {name: 'Nina Wagner'}),
      p = allShortestPaths((a)-[:KNOWS*]-(b))
RETURN [x IN nodes(p) | x.name] AS path, size(relationships(p)) AS hops
```
```
                          path  hops
0  [Anna Schmidt, Nina Wagner]     1
```

Anna and Nina have a direct `KNOWS` edge, so the shortest path is a single hop and there is only one of them.

### Cypher 5 quantified path patterns and `SHORTEST k`

Neo4j 5.26 (confirmed via `CALL dbms.components()` — see below) also supports the newer GQL-style syntax, which folds the repetition bound directly into the relationship arrow: `-[:TYPE]-{min,max}-` instead of `-[:TYPE*min..max]-`. Combined with `SHORTEST k`, it reads almost like English: "the shortest path, using 1 to 5 `KNOWS` hops, between these two people":

```cypher
CALL dbms.components() YIELD name, versions, edition
RETURN name, versions, edition
```
```
           name    versions     edition
0  Neo4j Kernel  [5.26.29]  community
```

```cypher
MATCH p = SHORTEST 1 (a:Person {name: 'Anna Schmidt'})-[:KNOWS]-{1,5}(b:Person {name: 'Tom Becker'})
RETURN [x IN nodes(p) | x.name] AS path
```
```
                                                path
0  [Anna Schmidt, Marek Nowak, Lucia Ferreira, Tom Becker]
```

Same result as `shortestPath()` above. `SHORTEST 1` asks for exactly one shortest path (use a plain `SHORTEST` or a bigger number, e.g. `SHORTEST 3`, to get several). This syntax is newer and less widely documented than `shortestPath()`/`allShortestPaths()`; for compatibility with older Neo4j versions and existing examples online, `shortestPath()` is still the more common choice, but the quantified form is worth knowing since it's now the direction Cypher (and the related GQL standard) is heading.

## Lists and maps

Cypher treats lists and maps as first-class values, with functions to build, filter, and reshape them inline — this is often faster and clearer than pulling raw rows into Python and looping there.

**List comprehension** — `[x IN list WHERE condition | expression]`, same shape as a Python list comprehension: filter, then transform.

```cypher
RETURN [x IN range(1, 10) WHERE x % 2 = 0 | x * x] AS squares
```
```
              squares
0  [4, 16, 36, 64, 100]
```

**`reduce()`** — fold a list down to a single value, carrying an accumulator through each element (like Python's `functools.reduce`):

```cypher
MATCH (p:Person)-[:HAS_SKILL]->(s:Skill)
WITH p, collect(s.name) AS skills
RETURN p.name AS person, reduce(acc = '', name IN skills | acc + name + ',') AS joined
ORDER BY person LIMIT 3
```
```
          person          joined
0   Anna Schmidt  Python,Cypher,
1  Chris Johnson  Kubernetes,Go,
2    David Klein         SQL,Go,
```

**`size()`, `range()`, `head`/`last`/`tail`**:

```cypher
RETURN size(range(0, 20, 5)) AS n, range(0, 20, 5) AS r
```
```
   n                   r
0  5  [0, 5, 10, 15, 20]
```

`range(start, end, step)` is inclusive of `end` when it lands exactly on a step, like above. `size()` works on any list (or string), not just the output of `range()`.

```cypher
WITH [1, 2, 3, 4, 5] AS xs
RETURN head(xs) AS h, last(xs) AS l, tail(xs) AS t
```
```
   h  l             t
0  1  5  [2, 3, 4, 5]
```

`head`/`last` return the first/last element; `tail` returns everything *except* the first element, as a new list.

**`coalesce()`** — return the first non-`NULL` argument, useful for defaults:

```cypher
MATCH (p:Person) RETURN p.name AS name, coalesce(p.nickname, p.name) AS display LIMIT 3
```
```
             name         display
0    Anna Schmidt    Anna Schmidt
1     Marek Nowak     Marek Nowak
2  Lucia Ferreira  Lucia Ferreira
```

No `Person` in our dataset has a `nickname` property, so `coalesce` always falls through to `p.name` — that's the point of the function: build one "display" field from an optional value plus a required fallback.

**Map projection** — `node {.prop1, .prop2, alias: other.prop}` builds a plain map from a node (or a mix of a node and related data), instead of returning the whole node object:

```cypher
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
RETURN p {.name, .age, company: c.name} AS person
LIMIT 3
```
```
                                                       person
0  {'name': 'Marek Nowak', 'age': 34, 'company': 'GraphWorks'}
1  {'name': 'Anna Schmidt', 'age': 29, 'company': 'GraphWorks'}
2  {'name': 'Piotr Zielinski', 'age': 27, 'company': 'GraphWorks'}
```

`.name` and `.age` copy those properties straight from `p`; `company: c.name` adds a new key pulled from a different, related node — handy for shaping a query's output into exactly the JSON-like structure an API caller wants.

**Pattern comprehension** — `[(pattern) | expression]`, a compact way to pull related data into a list without a separate `MATCH`/`WITH`:

```cypher
MATCH (p:Person)
RETURN p.name AS name, [(p)-[:HAS_SKILL]->(s) | s.name] AS skills
ORDER BY name LIMIT 3
```
```
            name            skills
0   Anna Schmidt  [Cypher, Python]
1  Chris Johnson  [Go, Kubernetes]
2    David Klein         [SQL, Go]
```

This is equivalent to the `OPTIONAL MATCH ... collect()` pattern from chapter 03, but inline — if `p` has no matching relationship, the comprehension evaluates to an empty list `[]` rather than dropping the row or needing `OPTIONAL MATCH`.

## `CASE`

**Simple `CASE`** compares one expression against a list of exact values, like a Python `match`:

```cypher
MATCH (p:Person)
RETURN p.name AS name,
       CASE p.age WHEN 24 THEN 'youngest' WHEN 50 THEN 'oldest' ELSE 'other' END AS tag
ORDER BY name LIMIT 4
```
```
             name     tag
0    Anna Schmidt   other
1   Chris Johnson   other
2     David Klein  oldest
3  Elena Kowalski   other
```

**Generic `CASE`** evaluates a list of independent boolean conditions in order and takes the first match — this is the more commonly used form, since most bucketing logic needs ranges or comparisons, not exact values:

```cypher
MATCH (p:Person)
RETURN p.name AS name, p.age AS age,
       CASE WHEN p.age < 30 THEN 'junior'
            WHEN p.age < 45 THEN 'mid'
            ELSE 'senior' END AS band
ORDER BY p.age
```
```
               name  age    band
0    Marta Kaminska   24  junior
1        Tom Becker   26  junior
2   Piotr Zielinski   27  junior
3      Anna Schmidt   29  junior
4       Nina Wagner   31     mid
5       Sofia Alves   33     mid
6       Marek Nowak   34     mid
7     Chris Johnson   37     mid
8    Elena Kowalski   38     mid
9    Lucia Ferreira   41     mid
10      James Silva   45  senior
11      David Klein   50  senior
```

## `UNION` / `UNION ALL`

`UNION` combines the results of two (or more) queries that return the same column names, and — just like SQL — removes duplicate rows. `UNION ALL` keeps duplicates.

```cypher
MATCH (p:Person) WHERE p.age < 27 RETURN p.name AS name
UNION
MATCH (p:Person) WHERE p.age > 45 RETURN p.name AS name
```
```
             name
0  Marta Kaminska
1      Tom Becker
2     David Klein
```

```cypher
MATCH (p:Person)-[:WORKS_AT]->(c:Company {name: 'GraphWorks'}) RETURN c.name AS org
UNION ALL
MATCH (c:Company {name: 'GraphWorks'}) RETURN c.name AS org
```
```
          org
0  GraphWorks
1  GraphWorks
2  GraphWorks
3  GraphWorks
```

The first branch returns `'GraphWorks'` once per person who works there (3 people), the second returns it once for the company node itself — `UNION ALL` keeps all 4 rows instead of collapsing them to 1.

## Subqueries

### `EXISTS {}` and `COUNT {}` — boolean and counting subqueries

`EXISTS { pattern }` is `true` if the pattern (or a full sub-query) matches at least once — clearer than the older `WHERE (p)-->()` pattern-as-boolean trick, and it can hold a full `MATCH`/`WHERE`/`RETURN`, not just a single pattern.

```cypher
MATCH (p:Person)
WHERE EXISTS { (p)-[:HAS_SKILL]->(:Skill {name: 'Python'}) }
RETURN p.name AS name ORDER BY name
```
```
             name
0    Anna Schmidt
1     James Silva
2  Lucia Ferreira
3     Marek Nowak
4     Sofia Alves
```

`COUNT { pattern }` counts matches of a pattern and can be used anywhere a number can — in `WHERE`, or directly in `RETURN`:

```cypher
MATCH (p:Person)
WHERE COUNT { (p)-[:HAS_SKILL]->() } >= 2
RETURN p.name AS name, COUNT { (p)-[:HAS_SKILL]->() } AS n_skills
ORDER BY name
```
```
              name  n_skills
0     Anna Schmidt         2
1    Chris Johnson         2
2      David Klein         2
3      James Silva         2
4   Lucia Ferreira         2
5      Marek Nowak         2
6      Nina Wagner         2
7  Piotr Zielinski         2
8      Sofia Alves         2
9       Tom Becker         2
```

Everyone in our dataset has exactly 2 skills, so this filters out only the people with fewer (Elena Kowalski and Marta Kaminska, who each have 1).

### `COLLECT {}` — a subquery that returns a list

`COLLECT { MATCH ... RETURN expr }` runs a full subquery and gathers its single returned column into a list — equivalent to the pattern-comprehension example above, but able to hold a multi-clause subquery (its own `WHERE`, `ORDER BY`, `LIMIT`) instead of just one pattern:

```cypher
MATCH (p:Person)
RETURN p.name AS name, COLLECT { MATCH (p)-[:HAS_SKILL]->(s) RETURN s.name } AS skills
ORDER BY name LIMIT 3
```
```
            name            skills
0   Anna Schmidt  [Cypher, Python]
1  Chris Johnson  [Go, Kubernetes]
2    David Klein         [SQL, Go]
```

### `CALL {}` — per-row subqueries (top-2 skills per person)

`CALL (variables) { ... }` runs a subquery **once per incoming row**, importing whichever outer variables you list in parentheses. This is the tool for "for each X, compute something with its own `ORDER BY`/`LIMIT`" — something a plain `WITH` can't do per-row, because `ORDER BY ... LIMIT` after a `WITH` applies to the whole result set, not to each group separately.

```cypher
MATCH (p:Person)
CALL (p) {
  MATCH (p)-[h:HAS_SKILL]->(s:Skill)
  RETURN s.name AS skill ORDER BY h.level DESC, s.name LIMIT 2
}
RETURN p.name AS person, collect(skill) AS top_skills
ORDER BY person
```
```
             person            top_skills
0      Anna Schmidt      [Cypher, Python]
1     Chris Johnson      [Kubernetes, Go]
2       David Klein             [Go, SQL]
3    Elena Kowalski                 [SQL]
4       James Silva  [Python, Statistics]
5    Lucia Ferreira  [Python, Statistics]
6       Marek Nowak         [Python, SQL]
7    Marta Kaminska              [Docker]
8       Nina Wagner  [Docker, Kubernetes]
9   Piotr Zielinski          [Go, Cypher]
10      Sofia Alves        [Rust, Python]
11       Tom Becker  [Docker, Kubernetes]
```

Each person in our dataset has at most 2 skills, so "top 2" happens to return everything here — the pattern still matters, because on a graph where people had 10 skills each, `LIMIT 2` inside the `CALL {}` would cap it per person, not overall.

### `CALL { ... } IN TRANSACTIONS OF n ROWS` — batching big writes

For read queries like the ones above, plain `CALL {}` is enough. For a **write** that touches a huge number of rows — e.g. updating every node matched by a `MATCH` over millions of rows — a single transaction has to hold all the changes in memory at once, which can exhaust memory or hold locks for a long time. `CALL { ... } IN TRANSACTIONS OF n ROWS` splits the work into many smaller transactions, committing every `n` rows:

```cypher
MATCH (p:Person)
CALL (p) { SET p.last_seen = date() } IN TRANSACTIONS OF 500 ROWS
```

We don't run this against the tutorial dataset (12 people fits in one transaction with room to spare, and `SET p.last_seen` isn't something we want to leave behind), but the shape is the one to reach for once a write touches enough rows that "500" (or 1000, 10000 — tune it to your data) meaningfully reduces memory pressure and lock contention. It cannot run inside an already-open transaction — from `cypher-shell` or the driver's `execute_query`, run it as its own top-level statement.

## Writing: `SET`, `REMOVE`, `DELETE`, `MERGE`, `FOREACH`

Every example below is immediately followed by the query that undoes it, and the chapter ends with `just load` to fully restore the dataset. Run these from `just shell` (an interactive `cypher-shell` session) or `just cypher "..."` if you want to follow along.

### `SET` — single property, `+=` map merge, replace with `=`

```cypher
MATCH (p:Person {name: 'Anna Schmidt'}) SET p.nickname = 'Ann'
RETURN p.name, p.nickname
```
```
p.name, p.nickname
"Anna Schmidt", "Ann"
```
Undo:
```cypher
MATCH (p:Person {name: 'Anna Schmidt'}) REMOVE p.nickname
RETURN p.name, p.nickname
```
```
p.name, p.nickname
"Anna Schmidt", NULL
```

`SET n += {map}` merges a map into a node's existing properties — keys in the map overwrite, keys not in the map are left alone (unlike plain `SET n = {map}`, which **replaces every property**, deleting any not in the map):

```cypher
MATCH (p:Person {name: 'Anna Schmidt'}) SET p += {nickname: 'Ann', age: 30}
RETURN p.name, p.age, p.nickname
```
```
p.name, p.age, p.nickname
"Anna Schmidt", 30, "Ann"
```
Undo (restore the original age, drop the nickname):
```cypher
MATCH (p:Person {name: 'Anna Schmidt'}) SET p.age = 29 REMOVE p.nickname
RETURN p.name, p.age, p.nickname
```
```
p.name, p.age, p.nickname
"Anna Schmidt", 29, NULL
```

### `REMOVE` a property or a label; `SET` to add a label

`REMOVE n.prop` deletes a single property (shown above). Labels use the same two verbs: `SET n:Label` adds a label, `REMOVE n:Label` removes it — a node can carry several labels at once.

```cypher
MATCH (p:Person {name: 'Anna Schmidt'}) SET p:Mentor RETURN labels(p)
```
```
labels(p)
["Person", "Mentor"]
```
Undo:
```cypher
MATCH (p:Person {name: 'Anna Schmidt'}) REMOVE p:Mentor RETURN labels(p)
```
```
labels(p)
["Person"]
```

### `DELETE` vs `DETACH DELETE`

`DELETE` removes a node only if it has **no relationships**; Neo4j refuses to silently orphan relationships (a relationship without both its endpoints existing would violate the graph model). To prove it, we tried deleting Anna, who has `WORKS_AT`, `KNOWS`, `HAS_SKILL`, and `LIVES_IN` edges:

```cypher
MATCH (p:Person {name: 'Anna Schmidt'}) DELETE p
```
```
Cannot delete node<0>, because it still has relationships. To delete this node, you must first delete its relationships.
```

`DETACH DELETE` deletes the node **and** every relationship attached to it in one statement. We did not run this on any real dataset node (it would break the fixed dataset counts) — instead we created two throwaway nodes just to demonstrate it safely:

```cypher
CREATE (t:Person {name: 'Temp2'})-[:KNOWS]->(:Person {name: 'Temp3'})
```
```cypher
MATCH (p:Person {name: 'Temp2'}) DETACH DELETE p
```
No error, and `Temp2` plus its `KNOWS` relationship are gone. `Temp3` (with no relationships left) can then be removed with a plain `DELETE`:
```cypher
MATCH (p:Person {name: 'Temp3'}) DETACH DELETE p
```
(Nothing to undo — these nodes never belonged to the dataset.)

### `MERGE` on a relationship, with `ON CREATE SET`

`MERGE` matches a pattern if it already exists, or creates it if it doesn't — the read-or-write behaviour we used for idempotent loading in chapter 02. `ON CREATE SET` runs only on the branch where `MERGE` actually created something (there's a matching `ON MATCH SET` for the other branch):

```cypher
MATCH (a:Person {name: 'Anna Schmidt'}), (b:Person {name: 'Sofia Alves'})
MERGE (a)-[r:KNOWS]->(b)
ON CREATE SET r.since = 2024
RETURN a.name, b.name, r.since
```
```
a.name, b.name, r.since
"Anna Schmidt", "Sofia Alves", 2024
```
Undo (this `KNOWS` edge did not exist in the original dataset, so we simply delete it):
```cypher
MATCH (a:Person {name: 'Anna Schmidt'})-[r:KNOWS]->(b:Person {name: 'Sofia Alves'}) DELETE r
```

### `FOREACH` — apply a write to every element of a list

`FOREACH (x IN list | update)` runs an update clause once per list element — commonly a list built by `collect()` earlier in the same query. Cypher has no plain `IF`, so `FOREACH` over a 0-or-1-element list is also the standard trick for a **conditional write**.

```cypher
MATCH (p:Person) WHERE p.age > 45
WITH collect(p) AS olds
FOREACH (x IN olds | SET x.senior = true)
```
```cypher
MATCH (p:Person) WHERE p.senior = true RETURN p.name, p.senior
```
```
p.name, p.senior
"David Klein", TRUE
```
Undo:
```cypher
MATCH (p:Person) WHERE p.senior = true REMOVE p.senior
```

### Restore the dataset

After running (and undoing) the write examples above, reload from the CSVs to guarantee a clean, known state for the next chapter:

```bash
just load
```
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

Matches the original counts from chapter 02 — every write above was cleanly undone.

## Indexes

An index lets Neo4j jump straight to matching nodes instead of scanning every node with a label. Chapter 02 already created uniqueness constraints (which imply an index) on each entity's name; here we add a plain index on a non-unique property, and a full-text index for fuzzy text search.

```cypher
CREATE INDEX person_age IF NOT EXISTS FOR (p:Person) ON (p.age)
```

**Full-text index** — tokenizes a string property for fuzzy/partial search (`CALL db.index.fulltext.queryNodes`), unlike a range index which only supports exact/range lookups:

```cypher
CREATE FULLTEXT INDEX person_names IF NOT EXISTS FOR (p:Person) ON EACH [p.name]
```

```cypher
CALL db.index.fulltext.queryNodes('person_names', 'ann~') YIELD node, score
RETURN node.name AS name, score ORDER BY score DESC
```
```
           name     score
0  Anna Schmidt  0.654389
```

`ann~` is a fuzzy search term (the `~` allows small typos/edit-distance matches) — it matched "Anna Schmidt" even though the query string was truncated to 3 letters.

`SHOW INDEXES` lists everything currently on the database, including the constraint-backed ones from chapter 02:

```cypher
SHOW INDEXES YIELD name, type, entityType, labelsOrTypes, properties
RETURN name, type, entityType, labelsOrTypes, properties ORDER BY name
```
```
             name      type    entityType labelsOrTypes properties
0       city_name     RANGE          NODE        [City]     [name]
1    company_name     RANGE          NODE     [Company]     [name]
2  index_343aff4e    LOOKUP          NODE          None       None
3  index_f7700477    LOOKUP  RELATIONSHIP          None       None
4      person_age     RANGE          NODE      [Person]      [age]
5     person_name     RANGE          NODE      [Person]     [name]
6    person_names  FULLTEXT          NODE      [Person]     [name]
7      skill_name     RANGE          NODE       [Skill]     [name]
```

The two `LOOKUP` indexes (`index_343aff4e` for nodes, `index_f7700477` for relationships) are built-in — Neo4j creates them automatically on every database so that "find anything with this label" or "find anything with this relationship type" is never a full scan, even before you add your own indexes.

## Performance: `EXPLAIN` vs `PROFILE`

- **`EXPLAIN`** shows the query plan Neo4j *would* use, without running the query.
- **`PROFILE`** actually runs the query and adds real row counts and `db hits` (roughly: one storage-engine operation) to each step of the plan — use `PROFILE` when you want to know what a query really costs, `EXPLAIN` when you just want to sanity-check the plan without touching data.

We ran the same query — `MATCH (p:Person) WHERE p.age > 35 RETURN p.name` — with `PROFILE`, once **before** the `person_age` index existed and once **after**, using `cypher-shell --format verbose` to print the full plan tree (`just cypher` prints only the summary row; the verbose plan requires running `cypher-shell` directly).

**Before the index** — `NodeByLabelScan` walks every `Person` node, then a `Filter` checks the age condition on each one:

```
+------------------+----+--------------------+----------------+------+---------+
| Operator         | Id | Details            | Estimated Rows | Rows | DB Hits |
+------------------+----+--------------------+----------------+------+---------+
| +ProduceResults  |  0 | `p.name`           |              4 |    5 |       0 |
| +Projection      |  1 | p.name AS `p.name`|              4 |    5 |       5 |
| +Filter          |  2 | p.age > $autoint_0 |              4 |    5 |      12 |
| +NodeByLabelScan |  3 | p:Person           |             12 |   12 |      13 |
+------------------+----+--------------------+----------------+------+---------+
Total database accesses: 30
```

**After the index** — `NodeIndexSeekByRange` uses the `person_age` range index to go straight to the 5 matching nodes; no separate `Filter` step and roughly a third of the `db hits`:

```
+-----------------------+----+----------------------------------------------------+----------------+------+---------+
| Operator              | Id | Details                                             | Estimated Rows | Rows | DB Hits |
+-----------------------+----+----------------------------------------------------+----------------+------+---------+
| +ProduceResults       |  0 | `p.name`                                            |              1 |    5 |       0 |
| +Projection           |  1 | p.name AS `p.name`                                 |              1 |    5 |       5 |
| +NodeIndexSeekByRange |  2 | RANGE INDEX p:Person(age) WHERE age > $autoint_0    |              1 |    5 |       6 |
+-----------------------+----+----------------------------------------------------+----------------+------+---------+
Total database accesses: 11
```

12 `Person` nodes is far too small to see a real time difference, but `db hits` already drops from 30 to 11 — on a graph with millions of `Person` nodes, `NodeByLabelScan` would touch every one of them while `NodeIndexSeekByRange` touches only the matching rows, and that gap only grows with data size. This is the concrete thing to look for when tuning a slow query: **scan** operators (`NodeByLabelScan`, `AllNodesScan`, `Filter` after a scan) usually mean a missing index; **seek** operators (`NodeIndexSeek`, `NodeIndexSeekByRange`, `NodeUniqueIndexSeek`) mean an index is being used.

## APOC — when plain Cypher isn't enough

APOC ("Awesome Procedures On Cypher") is a plugin library of extra procedures and functions — it's already installed in our Docker image (see `index.md`). Reach for APOC when something is awkward or impossible in plain Cypher: graph-wide statistics, meta-programming (calling a procedure by name at runtime), or algorithms like weighted subgraph extraction that would take many lines of hand-written Cypher. For everyday filtering, aggregation, and pattern matching, plain Cypher is faster to write, easier to read, and doesn't add a dependency — use APOC as the exception, not the default.

**`apoc.meta.stats()`** — instant graph-wide counts without a `MATCH`/`count()` scan over everything:

```cypher
CALL apoc.meta.stats() YIELD nodeCount, relCount, labels
RETURN nodeCount, relCount, labels
```
```
   nodeCount  relCount                                  labels
0         28        58  {Company: 4, Skill: 8, City: 4, Person: 12}
```

**`apoc.path.subgraphNodes`** — collect every node reachable from a starting node within a given depth and relationship filter, in one call, instead of a variable-length `MATCH` plus `DISTINCT`:

```cypher
MATCH (a:Person {name: 'Anna Schmidt'})
CALL apoc.path.subgraphNodes(a, {relationshipFilter: 'KNOWS', maxLevel: 2}) YIELD node
RETURN node.name AS name ORDER BY name
```
```
              name
0     Anna Schmidt
1   Lucia Ferreira
2      Marek Nowak
3      Nina Wagner
4  Piotr Zielinski
```

Same 5 people as the friends-of-friends query earlier in this chapter, but with `relationshipFilter`/`maxLevel` as plain configuration instead of a hand-written pattern — worth it once the traversal rules get more complex than "N hops of one relationship type".

**`apoc.help()`** — search APOC's own procedure catalog from inside Cypher, handy when you vaguely remember a procedure name:

```cypher
CALL apoc.help('path.subgraphNodes') YIELD name, text RETURN name, text LIMIT 1
```
```
                      name                                          text
0  apoc.path.subgraphNodes  Returns the NODE values in the sub-graph reachable from the start NODE following the given RELATIONSHIP types to max-depth.
```

## Key takeaways

- A variable-length pattern (`-[:TYPE*1..3]->`) explores multiple hops; always bound it — an unbounded `*` can explode combinatorially on a real graph.
- `shortestPath()`/`allShortestPaths()` (and the newer `SHORTEST k` quantified path syntax) use a dedicated search algorithm, far cheaper than a bounded `*` pattern when you only want the shortest route.
- List/map tools — comprehensions, `reduce`, map projection (`n {.a, .b}`), pattern comprehension (`[(n)-->(m) | m.x]`) — reshape query output without a round-trip to Python.
- `EXISTS {}`, `COUNT {}`, `COLLECT {}` are subqueries usable as a boolean, a number, or a list respectively; `CALL (vars) {}` runs a subquery per row (top-N per group), and `CALL {} IN TRANSACTIONS OF n ROWS` batches large writes.
- Every write (`SET`, `REMOVE`, `DELETE`, `MERGE`, `FOREACH`) has a natural undo — practice writing both together, and finish any experimentation with `just load` to restore the dataset.
- `DELETE` refuses to orphan relationships; `DETACH DELETE` removes the node and its relationships together.
- `SHOW INDEXES` lists what exists; `EXPLAIN`/`PROFILE` show whether a query actually uses one — a `NodeByLabelScan`/`Filter` pair usually means a missing index, a `NodeIndexSeek*` means one is being used.
- Reach for APOC for graph-wide stats or traversal algorithms that would be verbose in plain Cypher; keep everyday queries in plain Cypher.

Next: [05_python_patterns.md](05_python_patterns.md) — the Python driver in practice: `execute_query` vs sessions, managed read/write transactions, batching, results to pandas, and tests against the Docker database.
