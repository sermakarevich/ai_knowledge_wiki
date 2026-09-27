# 03 — Basic queries: MATCH, WHERE, RETURN, aggregation

**What you will learn**
- The anatomy of a read query: `MATCH` (find a pattern) → `WHERE` (filter it) → `RETURN` (project the output)
- How to filter with properties, comparisons, boolean logic, string and regex predicates, and `NULL` checks
- How relationships show up in patterns: direction, relationship variables, and their own properties
- How to sort, page, aggregate (`count`, `collect`, `avg`...), and pipe results between query parts with `WITH`
- `OPTIONAL MATCH` (Neo4j's version of a SQL `LEFT JOIN`) and `UNWIND` for reading

All queries below live in `project/src/neo4j_tutorial/queries_basic.py` as a dict named `QUERIES` (name → Cypher text). Run any one of them, or all of them, and see the output as a **pandas DataFrame** (a table, from the `pandas` Python library):

```bash
just query-basic                       # run every query in QUERIES
just query-basic people_per_company    # run just one, by name
```

Every result table below is the *real* output of running that query against our loaded dataset (see `index.md` for the schema: 12 `Person`, 4 `Company`, 8 `Skill`, 4 `City` nodes).

## Anatomy of a read query

A basic Cypher (Neo4j's query language) read has three parts, always in this order:

1. **`MATCH`** — describe a *pattern* of nodes and relationships to look for, e.g. `(p:Person)`.
2. **`WHERE`** — filter which matches to keep (optional).
3. **`RETURN`** — pick what to output, and optionally rename it with `AS` (an alias).

```cypher
MATCH (p:Person)
RETURN p.name AS name, p.age AS age
ORDER BY name
LIMIT 5
```
```
             name  age
0    Anna Schmidt   29
1   Chris Johnson   37
2     David Klein   50
3  Elena Kowalski   38
4     James Silva   45
```

`RETURN *` returns every variable bound in the `MATCH`, as a single column per variable — each row's cell is the whole node, printed like a dictionary:

```cypher
MATCH (p:Person) RETURN * LIMIT 3
```
```
                                       p
0    {'name': 'Anna Schmidt', 'age': 29}
1     {'name': 'Marek Nowak', 'age': 34}
2  {'name': 'Lucia Ferreira', 'age': 41}
```

`RETURN *` is convenient for exploring in the Browser UI, but in real code always list the exact fields you need — it's clearer to read and cheaper to send over the network.

**`DISTINCT`** removes duplicate rows from the output, same as in SQL:

```cypher
MATCH (c:Company) RETURN DISTINCT c.industry AS industry
```
```
               industry
0              Software
1        Data Analytics
2  Cloud Infrastructure
3           AI Research
```

## Filtering

### Property in the pattern vs. `WHERE`

You can filter directly inside the pattern's curly braces — this only works for **exact equality**:

```cypher
MATCH (p:Person {name: 'Anna Schmidt'}) RETURN p.name AS name, p.age AS age
```
```
           name  age
0  Anna Schmidt   29
```

For anything other than exact equality — ranges, `OR`, functions — use `WHERE`:

```cypher
MATCH (p:Person) WHERE p.age > 35
RETURN p.name AS name, p.age AS age
ORDER BY p.age
```
```
             name  age
0   Chris Johnson   37
1  Elena Kowalski   38
2  Lucia Ferreira   41
3     James Silva   45
4     David Klein   50
```

### Boolean logic: `AND`, `OR`, `NOT`

```cypher
MATCH (p:Person)
WHERE p.age > 30 AND NOT p.name STARTS WITH 'A'
RETURN p.name AS name, p.age AS age
ORDER BY p.name
```
```
             name  age
0   Chris Johnson   37
1     David Klein   50
2  Elena Kowalski   38
3     James Silva   45
4  Lucia Ferreira   41
5     Marek Nowak   34
6     Nina Wagner   31
7     Sofia Alves   33
```

### `IN [...]` — match against a list of values

```cypher
MATCH (c:Company)
WHERE c.industry IN ['Software', 'AI Research']
RETURN c.name AS name, c.industry AS industry
```
```
         name     industry
0  GraphWorks     Software
1    ByteLabs  AI Research
```

### String predicates: `STARTS WITH`, `CONTAINS`, `ENDS WITH`, regex `=~`

```cypher
MATCH (p:Person)
WHERE p.name CONTAINS 'll' OR p.name ENDS WITH 'ski'
RETURN p.name AS name
ORDER BY name
```
```
              name
0   Elena Kowalski
1  Piotr Zielinski
```

`=~` matches a full regular expression (a pattern for matching text) against the whole string:

```cypher
MATCH (p:Person) WHERE p.name =~ 'A.*' RETURN p.name AS name ORDER BY name
```
```
           name
0  Anna Schmidt
```

### `IS NULL` / `IS NOT NULL`

Every `Person` in our dataset has an `age`, so to see `IS NULL` do something you'd normally run it against optional data — for example, `WHERE p.middle_name IS NULL` would match everyone, since no `Person` has that property at all. We come back to this with `OPTIONAL MATCH` below, which is the more common way this pattern shows up in practice.

### Label predicate: `n:Person`

Instead of writing the label inside the pattern, you can test it in `WHERE` — useful when a variable might match more than one label, or when the check is conditional:

```cypher
MATCH (n) WHERE n:Person RETURN count(n) AS people
```
```
   people
0      12
```

### Relationship-type alternatives: `[:KNOWS|WORKS_AT]`

A relationship pattern can list several relationship types separated by `|` — it matches any of them:

```cypher
MATCH (p:Person)-[r:KNOWS|WORKS_AT]->(x)
RETURN p.name AS person, type(r) AS rel_type, coalesce(x.name) AS other
ORDER BY person, rel_type
LIMIT 8
```
```
           person  rel_type           other
0    Anna Schmidt     KNOWS     Marek Nowak
1    Anna Schmidt     KNOWS     Nina Wagner
2    Anna Schmidt  WORKS_AT      GraphWorks
3   Chris Johnson  WORKS_AT        ByteLabs
4     David Klein     KNOWS  Marta Kaminska
5     David Klein  WORKS_AT       DataForge
6  Elena Kowalski     KNOWS     James Silva
7  Elena Kowalski  WORKS_AT       DataForge
```

## Relationships in patterns

### Direction

`-[:TYPE]->` means "from left node to right node". Flip the arrow, `<-[:TYPE]-`, to search the other way, and drop the arrow entirely, `-[:TYPE]-`, to match the relationship in **either** direction:

```cypher
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
RETURN p.name AS person, c.name AS company
ORDER BY person
LIMIT 5
```
```
           person     company
0    Anna Schmidt  GraphWorks
1   Chris Johnson    ByteLabs
2     David Klein   DataForge
3  Elena Kowalski   DataForge
4     James Silva    ByteLabs
```

### Relationship variables and their own properties

Just like nodes, relationships can have a variable (`w` below) so you can read the properties stored **on the edge itself** (here, `WORKS_AT.role`):

```cypher
MATCH (p:Person)-[w:WORKS_AT]->(c:Company)
RETURN p.name AS person, w.role AS role, type(w) AS rel_type
ORDER BY person
LIMIT 5
```
```
           person                 role  rel_type
0    Anna Schmidt     Backend Engineer  WORKS_AT
1   Chris Johnson    Platform Engineer  WORKS_AT
2     David Klein   Principal Engineer  WORKS_AT
3  Elena Kowalski  Engineering Manager  WORKS_AT
4     James Silva        ML Researcher  WORKS_AT
```

- **`type(r)`** — the relationship's type as a string (`"WORKS_AT"`), useful when a query matched several alternative types.
- **`labels(n)`** — a node's labels as a list, e.g. `["Person"]`.
- **`elementId(n)`** — the node's internal, database-assigned identity string (replaces the older numeric `id(n)`, which is deprecated). You never set this yourself; it exists for every node and relationship.
- **`properties(n)`** — every property on a node as one map, handy for debugging or generic printing.

```cypher
MATCH (p:Person {name: 'Anna Schmidt'})
RETURN labels(p) AS labels, elementId(p) AS element_id, properties(p) AS props
```
```
labels, element_id, props
["Person"], "4:cbb9fadc-0ac3-4ef3-b113-b227115ff73b:28", {name: "Anna Schmidt", age: 29}
```

(The exact `element_id` string will differ every time you reload the database — it is assigned internally and is not something your queries should hard-code.)

## Ordering and paging

`ORDER BY` sorts, `DESC` reverses it, `SKIP` drops the first N rows, and `LIMIT` caps how many rows come back — together they give you a page of results, the same idea as SQL's `ORDER BY ... OFFSET ... LIMIT`:

```cypher
MATCH (p:Person)
RETURN p.name AS name, p.age AS age
ORDER BY p.age DESC
SKIP 2
LIMIT 3
```
```
             name  age
0  Lucia Ferreira   41
1  Elena Kowalski   38
2   Chris Johnson   37
```

## Aggregation

Aggregating functions (`count`, `avg`, `min`, `max`, `sum`, `collect`) fold many rows into one — same idea as SQL's `GROUP BY` and aggregate functions, but Cypher's grouping is **implicit**: every plain (non-aggregated) item in `RETURN` automatically becomes a grouping key, with no explicit `GROUP BY` clause needed.

### `count(*)` vs `count(x)`

`count(*)` counts **rows**, including rows where a value is missing. `count(x)` counts **non-null values of `x`** only. `OPTIONAL MATCH` (below) is where this difference actually matters — here we force a miss by matching a city that doesn't exist, to show the gap:

```cypher
MATCH (p:Person)
OPTIONAL MATCH (p)-[:LIVES_IN]->(ci:City {name: 'Nowhere'})
RETURN count(*) AS rows, count(ci) AS non_null_cities
```
```
   rows  non_null_cities
0    12                0
```

All 12 people produce a row (`count(*)`), but since no city named `'Nowhere'` exists, `ci` is `NULL` in every row, so `count(ci)` is 0.

### `collect()` — gather values into a list

```cypher
MATCH (p:Person)-[:HAS_SKILL]->(s:Skill)
RETURN p.name AS person, collect(s.name) AS skills
ORDER BY person
```
```
             person                skills
0      Anna Schmidt      [Python, Cypher]
1     Chris Johnson      [Kubernetes, Go]
2       David Klein             [SQL, Go]
3    Elena Kowalski                 [SQL]
4       James Silva  [Python, Statistics]
5    Lucia Ferreira  [Python, Statistics]
6       Marek Nowak         [Python, SQL]
7    Marta Kaminska              [Docker]
8       Nina Wagner  [Docker, Kubernetes]
9   Piotr Zielinski          [Cypher, Go]
10      Sofia Alves        [Python, Rust]
11       Tom Becker  [Docker, Kubernetes]
```

`person` is a plain `RETURN` item, so it's the implicit grouping key — one row per person, each with all their skills collected into a list.

### `avg`, `min`, `max`, `sum`

```cypher
MATCH (p:Person)
RETURN avg(p.age) AS avg_age, min(p.age) AS min_age, max(p.age) AS max_age, sum(p.age) AS total_age
```
```
     avg_age  min_age  max_age  total_age
0  34.583333       24       50        415
```

### Implicit grouping: people per company, average age per city

```cypher
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
RETURN c.name AS company, count(p) AS people
ORDER BY people DESC
```
```
      company  people
0  GraphWorks       3
1   DataForge       3
2   CloudNine       3
3    ByteLabs       3
```

```cypher
MATCH (p:Person)-[:LIVES_IN]->(ci:City)
RETURN ci.name AS city, avg(p.age) AS avg_age
ORDER BY city
```
```
     city    avg_age
0  Austin  31.500000
1  Berlin  36.666667
2  Lisbon  39.666667
3  Warsaw  30.750000
```

In both queries, `company`/`city` is the only non-aggregated `RETURN` item, so Cypher groups by it automatically — there is no `GROUP BY` keyword in Cypher at all.

## `WITH` — pipelining a query in stages

`WITH` passes variables from one part of a query to the next, the same role a subquery or CTE (Common Table Expression) plays in SQL. A common use: **aggregate first, then filter on the aggregate** — you cannot put an aggregate directly in `WHERE`, so you compute it in `WITH` first.

```cypher
MATCH (p:Person)-[:HAS_SKILL]->(s:Skill)
WITH s, count(p) AS n WHERE n > 2
RETURN s.name AS skill, n AS people
ORDER BY n DESC
```
```
        skill  people
0      Python       5
1      Docker       3
2         SQL       3
3  Kubernetes       3
4          Go       3
```

`Cypher` and `Statistics` (2 people each) and `Rust` (1 person) were dropped by the `WHERE n > 2` — they never reach the final `RETURN`.

**Top-N per group** — aggregate, then `ORDER BY` and `LIMIT` in the same `WITH`, before the final `RETURN`:

```cypher
MATCH (p:Person)-[:HAS_SKILL]->(s:Skill)
WITH s, count(p) AS n ORDER BY n DESC LIMIT 1
RETURN s.name AS skill, n AS people
```
```
    skill  people
0  Python       5
```

## `OPTIONAL MATCH` — like a LEFT JOIN

`OPTIONAL MATCH` keeps rows even when the pattern doesn't match — missing values become `NULL`, exactly like a SQL `LEFT JOIN` keeps left-side rows with no matching right-side row.

**People with or without a city** (every person in our dataset does have one, so this returns all 12 with a real city — but the query is written so it would still return people with `NULL` city if the `LIVES_IN` edge were missing):

```cypher
MATCH (p:Person)
OPTIONAL MATCH (p)-[:LIVES_IN]->(ci:City)
RETURN p.name AS person, ci.name AS city
ORDER BY person
```
```
             person    city
0      Anna Schmidt  Berlin
1     Chris Johnson  Austin
2       David Klein  Berlin
3    Elena Kowalski  Warsaw
4       James Silva  Lisbon
5    Lucia Ferreira  Lisbon
6       Marek Nowak  Warsaw
7    Marta Kaminska  Warsaw
8       Nina Wagner  Berlin
9   Piotr Zielinski  Warsaw
10      Sofia Alves  Lisbon
11       Tom Becker  Austin
```

**Find the person with no `KNOWS` relationships at all** — this is the pattern where `OPTIONAL MATCH` really earns its keep: match every person, optionally match their `KNOWS` edges (in either direction with `-[k:KNOWS]-`), then keep only the ones where that count came back zero:

```cypher
MATCH (p:Person)
OPTIONAL MATCH (p)-[k:KNOWS]-()
WITH p, count(k) AS n WHERE n = 0
RETURN p.name AS person
```
```
          person
0  Chris Johnson
```

Chris Johnson is the only person in our 8-row `knows.csv` who never appears as either `person1` or `person2`.

## `UNWIND` for reading

`UNWIND` turns a list into rows. Chapter 02 used it to load many rows in one write; on the read side, it's handy for expanding a small list of values you want to check against the graph:

```cypher
WITH ['Python', 'Docker'] AS wanted UNWIND wanted AS skill
MATCH (p:Person)-[:HAS_SKILL]->(s:Skill {name: skill})
RETURN skill, p.name AS person
ORDER BY skill, person
```
```
    skill          person
0  Docker  Marta Kaminska
1  Docker     Nina Wagner
2  Docker      Tom Becker
3  Python    Anna Schmidt
4  Python     James Silva
5  Python  Lucia Ferreira
6  Python     Marek Nowak
7  Python     Sofia Alves
```

## `CASE` preview

`CASE` maps values to other values inline, like a SQL `CASE WHEN`. It's covered in depth in chapter 04; here's a first taste, bucketing people into age bands:

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

## Parameters from Python

Just like the writes in chapter 02, reads should also use **parameters** (`$name`) rather than pasting values into the query string — same reason: it avoids Cypher injection and lets Neo4j reuse the query plan.

```python
from neo4j_tutorial.db import run

rows = run(
    "MATCH (p:Person {name: $name}) RETURN p.name AS name, p.age AS age",
    name="Anna Schmidt",
)
```
```
           name  age
0  Anna Schmidt   29
```

`db.run` (from chapter 00) forwards `**params` straight into `execute_query`, which sends them to Neo4j as data, never as query text.

## Translating SQL to Cypher

| SQL | Cypher |
|---|---|
| `SELECT name, age FROM person` | `MATCH (p:Person) RETURN p.name AS name, p.age AS age` |
| `SELECT * FROM person WHERE age > 35` | `MATCH (p:Person) WHERE p.age > 35 RETURN p` |
| `SELECT p.name, c.name FROM person p JOIN company c ON p.company_id = c.id` | `MATCH (p:Person)-[:WORKS_AT]->(c:Company) RETURN p.name, c.name` |
| `SELECT company_id, COUNT(*) FROM person GROUP BY company_id` | `MATCH (p:Person)-[:WORKS_AT]->(c:Company) RETURN c.name, count(p)` (grouping is implicit) |
| `SELECT * FROM person ORDER BY age DESC LIMIT 3` | `MATCH (p:Person) RETURN p ORDER BY p.age DESC LIMIT 3` |
| `SELECT p.name, c.name FROM person p LEFT JOIN city c ON p.city_id = c.id` | `MATCH (p:Person) OPTIONAL MATCH (p)-[:LIVES_IN]->(c:City) RETURN p.name, c.name` |

## Key takeaways

- Every read is `MATCH` (pattern) → `WHERE` (filter) → `RETURN` (project); alias output columns with `AS`.
- Filter with exact-match properties `{name: "..."}` in the pattern, or `WHERE` for comparisons, `AND/OR/NOT`, `IN`, string predicates, regex `=~`, and label checks like `n:Person`.
- Relationships have direction (`->`, `<-`, or undirected `-`), can carry their own variable and properties (`[w:WORKS_AT]`, `w.role`), and support type alternatives `[:KNOWS|WORKS_AT]`.
- Cypher has no `GROUP BY` — every non-aggregated `RETURN` item is automatically a grouping key; `count(*)` counts rows, `count(x)` counts non-null values.
- `WITH` pipes an aggregate into a later `WHERE`, `ORDER BY`, or `LIMIT` — the standard way to filter or rank on top of a `count`/`avg`/etc.
- `OPTIONAL MATCH` is Cypher's `LEFT JOIN`: keep the row even when the pattern doesn't match, with missing values as `NULL`.
- Always pass values from Python as parameters (`$name`), never string-formatted into the query.

Next: [04_advanced_queries.md](04_advanced_queries.md) — variable-length paths, shortest paths, list/map functions, `CASE` in depth, subqueries, updating and deleting data, full-text search, `EXPLAIN`/`PROFILE`, and APOC.
