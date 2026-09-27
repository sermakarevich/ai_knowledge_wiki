"""Epic + parent-child hierarchy helpers on top of :mod:`beads_tutorial.db`.

An **epic** is a big container bead that groups smaller child beads.
A **parent-child** link ties one child to its epic (structure: what belongs
together). A **blocks** link orders two beads (sequence: what waits on what).

Usage::

    python -m beads_tutorial.hierarchy --demo --cwd <dir>
"""

import argparse
import json
import sys

from beads_tutorial import db


def make_epic(title: str, cwd: str) -> str:
    """Create an epic bead and return its id (``bd create --type epic``)."""
    data = db.bd_json("create", title, "--type", "epic", cwd=cwd)
    return data["id"]


def add_child(epic_id: str, title: str, cwd: str) -> str:
    """Create a child under ``epic_id`` and return the child id.

    Uses ``bd create --parent <epic>``, which also stores a
    ``parent-child`` dependency edge from child to epic.
    """
    data = db.bd_json("create", title, "--parent", epic_id, cwd=cwd)
    return data["id"]


def link_blocked(blocked: str, blocker: str, cwd: str, link_type: str = "blocks") -> None:
    """Link two beads (``bd link <blocked> <blocker> --type <link_type>``).

    ``link_type`` is one of ``blocks`` (default), ``related``, ``tracks``,
    ``parent-child``, or ``discovered-from``. For sequencing work use
    ``blocks``: ``blocked`` waits until ``blocker`` is closed.
    """
    db.run_bd("link", blocked, blocker, "--type", link_type, cwd=cwd)


def epic_status(epic_id: str, cwd: str) -> dict:
    """Summarise an epic: child counts plus ``bd epic status`` output.

    Runs ``bd epic status <id> --json`` (one row with ``total_children``,
    ``closed_children``, ``eligible_for_close``) and ``bd children <id>
    --json`` (the full child list), then merges both into one dict.
    """
    status_rows = db.bd_json("epic", "status", epic_id, cwd=cwd)
    row = status_rows[0] if isinstance(status_rows, list) else status_rows
    try:
        children = db.bd_json("children", epic_id, cwd=cwd)
    except RuntimeError:
        children = []
    if not isinstance(children, list):
        children = [children]
    open_children = [c["id"] for c in children if c.get("status") != "closed"]
    closed_children = [c["id"] for c in children if c.get("status") == "closed"]
    return {
        "epic_id": row.get("epic", {}).get("id", epic_id),
        "title": row.get("epic", {}).get("title", ""),
        "total_children": row.get("total_children", len(children)),
        "closed_children": row.get("closed_children", len(closed_children)),
        "open_children": open_children,
        "eligible_for_close": row.get("eligible_for_close", False),
    }


def demo(cwd: str) -> dict:
    """Build epic + 3 children + one blocks edge, print the tree."""
    epic_id = make_epic("Website relaunch", cwd=cwd)
    kids = [
        add_child(epic_id, title, cwd=cwd)
        for title in ("Design homepage", "Implement homepage", "Write docs")
    ]
    link_blocked(kids[1], kids[0], cwd=cwd)
    print(f"epic: {epic_id}")
    for kid in kids:
        print(f"  child: {kid}")
    print(f"  blocks: {kids[1]} waits on {kids[0]}")
    try:
        tree = db.run_bd("children", epic_id, "--pretty", cwd=cwd)
    except RuntimeError:
        tree = db.run_bd("list", "--parent", epic_id, cwd=cwd)
    print(tree)
    return {"epic": epic_id, "children": kids}


def main(argv: list | None = None) -> int:
    parser = argparse.ArgumentParser(description="Epic hierarchy demo.")
    parser.add_argument("--demo", action="store_true", help="build demo graph")
    parser.add_argument("--cwd", default=".", help="project folder with .beads/")
    parser.add_argument("--epic-status", metavar="ID", help="print epic summary")
    args = parser.parse_args(argv)
    if args.epic_status:
        print(json.dumps(epic_status(args.epic_status, args.cwd), indent=2))
        return 0
    if args.demo:
        demo(args.cwd)
        return 0
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
