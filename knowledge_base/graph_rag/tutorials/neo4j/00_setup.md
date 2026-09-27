# 00 — Setup: running Neo4j and connecting to it

**What you will learn**
- What Docker, `uv` and `just` are, and why this tutorial uses them
- What each file in `project/` does
- How to start Neo4j and open its browser UI
- How to run your first Cypher (Neo4j's query language) query, in the browser and from the command line
- How the Python code in `db.py` finds the database's address and password

## The tools we use

- **Docker** runs Neo4j inside an isolated container, a lightweight, self-contained box that has its own filesystem and network. You don't install Neo4j directly on your machine — you just start and stop a container. This keeps your computer clean and makes the setup identical for everyone who runs this tutorial.
- **uv** is a fast Python package manager. It creates a virtual environment (an isolated folder with its own Python packages, so this tutorial's dependencies never clash with other projects) and installs exactly the packages listed in `pyproject.toml`.
- **just** is a command runner, similar to `make`. Instead of typing long Docker or Python commands, you type short recipes like `just up` or `just check`.

## The dataset and shared settings

Before writing any file we read `index.md` (the parent folder's overview page). It fixes the settings every chapter must use and must never change:

| setting | value |
|---|---|
| browser UI | http://localhost:7476 |
| Bolt (Neo4j's binary network protocol used by drivers) URI | `bolt://localhost:7689` |
| user / password | `neo4j` / `tutorial123` |
| container name | `neo4j-tutorial` |

The ports are shifted from Neo4j's normal `7474`/`7687` because another Neo4j instance on this machine (Neo4j Desktop) occupies the defaults **and** 7475/7688. We never touch that other instance.

## The files in `project/`

```
project/
├── docker-compose.yml       # defines the neo4j-tutorial container
├── .gitignore                # keeps secrets and local data out of git
├── .env.template              # documents which environment variables are needed
├── .env                       # your actual local settings (gitignored, not committed)
├── pyproject.toml             # Python project + dependency list, read by uv
├── justfile                   # short commands: up, down, check, cypher, ...
├── data/                      # CSV files with the tutorial dataset
└── src/neo4j_tutorial/
    ├── __init__.py
    ├── db.py                  # connect to Neo4j, run queries
    └── check.py                # a small script that proves the connection works
```

### `docker-compose.yml`

[Docker Compose](https://docs.docker.com/compose/) is a tool that starts one or more containers from a single YAML file. Ours defines one service, `neo4j`, using the official `neo4j:5` image (Neo4j version 5). Key parts:

```yaml
services:
  neo4j:
    image: neo4j:5
    container_name: neo4j-tutorial
    ports:
      - "7476:7474"   # browser UI: host 7476 -> container 7474
      - "7689:7687"   # Bolt driver: host 7689 -> container 7687
    environment:
      NEO4J_AUTH: neo4j/tutorial123
      NEO4J_PLUGINS: '["apoc"]'   # APOC = Awesome Procedures On Cypher, an extension library
    volumes:
      - ./data/neo4j:/data       # the actual graph database files
      - ./data:/import           # lets Cypher's LOAD CSV read our CSV files
    healthcheck:
      test: ["CMD-SHELL", "wget --no-verbose --tries=1 --spider http://localhost:7474 || exit 1"]
```

The **healthcheck** repeatedly pings the browser port so Docker (and our `justfile`) can tell when Neo4j has actually finished starting, not just that the container process exists. Startup takes 15-30 seconds because Neo4j has to initialize its storage engine and install the APOC plugin.

The `./data:/import` volume mount matters for a later chapter: Cypher's `LOAD CSV FROM 'file:///people.csv' ...` looks for files under `/import` inside the container, which is our local `data/` folder.

### `.env`, `.env.template` and secrets

`.env.template` lists the environment variables the Python code needs, with example (in this case, real tutorial) values:

```bash
NEO4J_URI=bolt://localhost:7689
NEO4J_USER=neo4j
NEO4J_PASSWORD=tutorial123
```

`.env` has the same content but is listed in `.gitignore` so it is never committed — that's the standard pattern for keeping credentials out of git history, even when (as here) the password is just a tutorial placeholder. If you ever delete `.env`, the code still works: `db.py` falls back to the same default values.

### `pyproject.toml`

This file tells `uv` what the project needs:

```toml
[project]
name = "neo4j-tutorial"
requires-python = ">=3.11"
dependencies = [
    "neo4j>=5.20",        # the official Neo4j Python driver
    "pandas>=2.2",        # used from chapter 05 onward
    "python-dotenv>=1.0", # loads variables from .env into the environment
]

[dependency-groups]
dev = ["pytest>=8"]        # testing framework, used by later chapters
```

Running `uv sync` reads this file, creates `.venv/` (also gitignored), and installs everything — including the `dev` group, which holds tools only needed while developing (like `pytest`), not to run the tutorial code itself.

### `src/neo4j_tutorial/db.py`

```python
from neo4j import Driver, GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

def get_driver() -> Driver:
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7689")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "tutorial123")
    driver = GraphDatabase.driver(uri, auth=(user, password))
    driver.verify_connectivity()
    return driver
```

`load_dotenv()` reads `.env` (if it exists) and copies its variables into the process's environment. `os.getenv("NEO4J_URI", "bolt://localhost:7689")` reads the `NEO4J_URI` variable, or uses the default if it isn't set — so the code works with or without a `.env` file. `driver.verify_connectivity()` immediately tries to reach the database and raises an error if it can't, so problems show up right away instead of on the first query.

The file also defines a `run()` helper that runs one query and returns the results as a list of plain Python dictionaries, using the driver's `execute_query()` method (the simplest way to run a single query without managing sessions manually — later chapters cover sessions and transactions).

### `src/neo4j_tutorial/check.py`

A small script for exactly one purpose: prove the whole setup works. It connects, runs `RETURN 1 AS ok`, asks Neo4j for its own version with `CALL dbms.components()` (a built-in procedure that reports server metadata), and counts how many nodes exist in the database.

### `justfile`

```just
up:      # start Docker, wait until healthy
down:    # stop the container (keeps data)
reset:   # stop, delete volumes AND the local data/neo4j folder
logs:    # follow container logs
shell:   # open an interactive cypher-shell session
cypher query:  # run one Cypher query non-interactively
check:   # run check.py
sync:    # uv sync
```

`cypher-shell` is Neo4j's command-line client, built into the Docker image — no separate install needed.

## Starting Neo4j

From `project/`:

```bash
just up
```

Real output from this machine:

```
docker compose up -d
 Container neo4j-tutorial Running
waiting for neo4j-tutorial to become healthy...
neo4j-tutorial is healthy
```

The `up` recipe calls `docker compose up -d` (start in the background) and then loops, calling `docker inspect` every second to read the container's health status, until it becomes `healthy`.

## The browser UI

Open **http://localhost:7476** in a browser. Neo4j Browser asks for:
- Connection URL: `bolt://localhost:7689` (it's usually pre-filled)
- Username: `neo4j`
- Password: `tutorial123`

Once logged in, type this into the query box and run it:

```cypher
RETURN "hello" AS greeting
```

Output:

| greeting |
|---|
| "hello" |

This is Cypher's simplest possible query: `RETURN` just produces a value without reading any data, `AS greeting` names the output column.

## Checking the connection from Python

```bash
uv sync
just check
```

Real output:

```
uv run python -m neo4j_tutorial.check
ok=1
Neo4j Kernel version: 5.26.29
node count: 0
```

`ok=1` confirms `RETURN 1 AS ok` came back correctly. The version line comes from `CALL dbms.components()`. `node count: 0` is expected — we haven't loaded any data yet; that's chapter 02.

## Running one Cypher query from the terminal

`just cypher` wraps `cypher-shell` so you don't need to open an interactive session for a single query:

```bash
just cypher "RETURN 1 AS one"
```

Real output:

```
docker exec -i neo4j-tutorial cypher-shell -u neo4j -p tutorial123 "RETURN 1 AS one"
one
1
```

## Troubleshooting

- **"port is already allocated"** — something else is using 7476 or 7689. Our setup deliberately avoids Neo4j's normal ports (7474/7687) **and** 7475/7688, because the local Neo4j Desktop instance on this machine takes all four of those; make sure nothing else grabbed 7476/7689 either (`lsof -nP -iTCP:7689 -sTCP:LISTEN` shows whoever owns a port, `docker ps` lists running containers).
- **`AuthError ... scheme 'basic' is not supported`** — another program (not our container) is answering on the Bolt port with a different authentication setup. Check `lsof -nP -iTCP:7689 -sTCP:LISTEN`; if it's not the `neo4j-tutorial` container, either that other program must move, or our ports here must.
- **Tests all error with `AuthError` but the container looks fine** — the tutorial's old ports 7475/7688 were hidden by Neo4j Desktop, which listens on 7474, 7687 **and** 7688. The tutorial now lives on **7476** (browser) / **7689** (Bolt). If you ever see this again, run `lsof -nP -i :7689` and confirm the listener is the `neo4j-tutorial` container before anything else.
- **Tests all skipped with "Neo4j not reachable"** — the test suite is skipped by design when the container isn't running (`tests/conftest.py`). Run `just up` first, then `just test`.
- **"password rules" / password rejected** — Neo4j requires passwords to be at least 8 characters. `tutorial123` (11 characters) already satisfies this; if you change it, keep it at 8+ characters and update `.env` to match.
- **Need a clean slate?** — `just reset` stops the container, deletes its Docker volumes, and removes the local `data/neo4j/` folder, so the next `just up` starts completely empty. Use this if the database gets into a state you don't want (e.g. after experimenting with chapter 02's data loading).
- **`just check` can't connect** — make sure `just up` reported `healthy` first; Neo4j refuses Bolt connections for the first several seconds while it's still starting even though the container itself is already running.
- **Prerequisite for the test suite** — `cd project && just up` must report `neo4j-tutorial is healthy` **before** `just test` (or `uv run pytest tests -q`). `tests/conftest.py` skips the whole module otherwise, so "all skipped" means the container isn't running.

## Key takeaways

- Docker runs Neo4j in an isolated container so nothing is installed system-wide; `docker-compose.yml` defines that container and its ports/volumes.
- `uv` manages the Python virtual environment and dependencies declared in `pyproject.toml`; `just` gives short commands (`up`, `check`, `cypher`, ...) instead of long Docker/Python invocations.
- Our Neo4j lives on browser port **7476** and Bolt port **7689**, deliberately different from the defaults (7474/7687) — and from 7475/7688 too — to avoid clashing with the local Neo4j Desktop instance.
- `db.py` reads connection details from `.env` (falling back to tutorial defaults if it's missing) and exposes `get_driver()` and `run()` helpers used throughout the rest of the tutorial.
- `just check` and `just cypher "..."` are quick ways to confirm the database is reachable, from Python and from the command line respectively.

Next: [001_explore_database.md](001_explore_database.md) — exploring an unknown database: labels, relationship types, properties, counts, indexes and constraints.
