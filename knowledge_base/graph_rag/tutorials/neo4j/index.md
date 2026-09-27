# Neo4j tutorial

A from-zero, hands-on tutorial for **Neo4j**, a *graph database*: instead of tables and rows it stores **nodes** (things) connected by **relationships** (how the things relate). Everything runs locally with Docker, `uv` (fast Python package manager), plain Python and a `justfile` (a command runner like `make`).

Retrieve chapters with `ai show research_topics/graph_rag/tutorials/neo4j/<chapter>`.

## Chapters (read in order)
- [00_setup.md](00_setup.md) — run Neo4j 5 in Docker, create the `uv` project, `justfile` recipes, first connection from Python and from the browser UI.
- [001_explore_database.md](001_explore_database.md) — exploring an unknown database: labels, relationship types, which labels connect via which relationships, properties and their types, counts, indexes/constraints, APOC meta procedures.
- [01_concepts.md](01_concepts.md) — the property-graph model (nodes, labels, relationships, properties), Cypher basics, indexes and constraints, transactions, when a graph beats a relational database.
- [02_insert_data.md](02_insert_data.md) — inserting data: `CREATE` vs `MERGE`, constraints first, batch loading with `UNWIND` + parameters, `LOAD CSV`, idempotent loaders from Python.
- [03_basic_queries.md](03_basic_queries.md) — reading data: `MATCH`, `WHERE`, `RETURN`, ordering/paging, aggregation, `OPTIONAL MATCH`, `WITH`.
- [04_advanced_queries.md](04_advanced_queries.md) — paths of variable length, shortest paths, list/map functions, `CASE`, subqueries (`EXISTS`, `COUNT`, `CALL {}`), updating and deleting, full-text index, `EXPLAIN`/`PROFILE`, APOC.
- [05_python_patterns.md](05_python_patterns.md) — Python driver in practice: `execute_query` vs sessions, managed read/write transactions, batching, results to pandas, tests against the Docker database.

## Runnable project
`project/` — `docker-compose.yml`, `justfile`, `pyproject.toml`, `data/*.csv`, `src/neo4j_tutorial/` (loader and query modules), `tests/`. Start with `cd project && just up && just check`.

## Local settings (shared by all chapters)
| setting | value |
|---|---|
| Docker image | `neo4j:5` with APOC plugin |
| container name | `neo4j-tutorial` |
| browser UI | http://localhost:7476 (host port **7476** → container 7474; 7474 is taken by another local Neo4j) |
| Bolt (driver) URI | `bolt://localhost:7689` (host port **7689** → container 7687) |
| user / password | `neo4j` / `tutorial123` |

## Dataset (shared by all chapters)
A small "tech people" graph, loaded from `project/data/*.csv`:

Nodes
- `Person {name, age}` — ~12 people
- `Company {name, industry, founded}` — 4 companies
- `Skill {name}` — ~8 skills (Python, Cypher, Docker, SQL, Kubernetes, Rust, Statistics, Go)
- `City {name, country}` — 4 cities

Relationships
- `(Person)-[:WORKS_AT {since, role}]->(Company)`
- `(Person)-[:KNOWS {since}]->(Person)`
- `(Person)-[:HAS_SKILL {level}]->(Skill)` — level is `beginner`/`intermediate`/`expert`
- `(Person)-[:LIVES_IN]->(City)`
- `(Company)-[:LOCATED_IN]->(City)`

Verified on: Neo4j Kernel 5.26.29, Python driver `neo4j` 6.3.0, 2026-08-28.
