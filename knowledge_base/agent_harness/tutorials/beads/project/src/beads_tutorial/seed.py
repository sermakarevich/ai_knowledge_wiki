"""Idempotent loader for the shared tutorial graph (epic + 5 tasks).

Mirrors ``../neo4j/load_data.py``: run it any number of times, the database
always ends up with the same 6 beads and the same 5 dependencies. Beads with
the same titles are reused instead of duplicated (check-then-create).

Usage::

    python -m beads_tutorial.seed --cwd <dir>   # prints the 6 ids
"""

import argparse
import sys

from beads_tutorial import db

ITEMS = [
    ("Build website", "epic", 1, "tutorial epic: a tiny website"),
    ("Design homepage", "task", 1, "draft layout"),
    ("Implement homepage", "task", 1, "build it"),
    ("Write tests", "task", 2, "test it"),
    ("Write docs", "task", 2, "document it"),
    ("Deploy website", "task", 1, "ship it"),
]

DEPS = [
    ("Implement homepage", "Design homepage"),
    ("Write tests", "Implement homepage"),
    ("Write docs", "Implement homepage"),
    ("Deploy website", "Write tests"),
    ("Deploy website", "Write docs"),
]


def seed(cwd: str) -> list[str]:
    """Create the tutorial graph in ``cwd`` and return the 6 ids in order."""
    existing = {i["title"]: i["id"] for i in db.bd_json("list", "--all", cwd=cwd)}
    ids: dict = {}
    for title, kind, prio, desc in ITEMS:
        if title in existing:
            ids[title] = existing[title]
        else:
            ids[title] = existing[title] = db.bd_create(
                title, cwd=cwd, type=kind, priority=prio, description=desc)
    for blocked, blocker in DEPS:
        try:
            db.run_bd("dep", "add", ids[blocked], ids[blocker], cwd=cwd)
        except RuntimeError as exc:
            if "already" not in str(exc).lower():
                raise
    return [ids[title] for title, _, _, _ in ITEMS]


def main(argv: list | None = None) -> int:
    parser = argparse.ArgumentParser(description="Seed the tutorial graph.")
    parser.add_argument("--cwd", default=".", help="project folder with .beads/")
    args = parser.parse_args(argv)
    for bead_id in seed(args.cwd):
        print(bead_id)
    return 0


if __name__ == "__main__":
    sys.exit(main())
