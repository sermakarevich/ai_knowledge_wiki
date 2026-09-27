"""Read-only inventory of an UNKNOWN beads database.

Mirrors ``../neo4j/001_explore_database.md``: look before you create.
All reads go through :mod:`beads_tutorial.db` (which runs the ``bd`` CLI
(Command-Line Interface) for us) — nothing here writes to the database.

Usage::

    python -m beads_tutorial.explore --summary --cwd <dir>   # compact counts
    python -m beads_tutorial.explore --shape --cwd <dir>     # type->type blocks
    python -m beads_tutorial.explore --orphans --cwd <dir>   # broken dependencies
"""

import argparse
import re
import sys

from beads_tutorial import db


def _all_issues(cwd: str) -> list:
    """Every issue including closed ones (``bd list`` hides closed by default)."""
    return db.bd_json("list", "--all", cwd=cwd)


def summary(cwd: str) -> dict:
    """Counts by status and by type, plus the raw ``bd status`` text.

    Returns ``{"total": int, "by_status": {...}, "by_type": {...},
    "ready": int | None, "status_text": str}``.
    """
    issues = _all_issues(cwd)
    by_status: dict = {}
    by_type: dict = {}
    for issue in issues:
        by_status[issue.get("status", "?")] = by_status.get(issue.get("status", "?"), 0) + 1
        by_type[issue.get("issue_type", "?")] = by_type.get(issue.get("issue_type", "?"), 0) + 1
    try:
        status_text = db.run_bd("status", cwd=cwd)
    except RuntimeError as exc:
        status_text = f"<bd status failed: {exc}>"
    ready = None
    match = re.search(r"Ready to Work:\s+(\d+)", status_text)
    if match:
        ready = int(match.group(1))
    return {"total": len(issues), "by_status": by_status, "by_type": by_type,
            "ready": ready, "status_text": status_text}


def shape(cwd: str) -> dict:
    """Which issue types block which other types, as ``{(from, to): count}``.

    ``from`` is the blocked issue's type, ``to`` the blocker's type.
    Reads the ``dependencies`` embedded in ``bd list --all --json`` and
    falls back to ``bd dep list <id> --json`` per issue when missing.
    """
    issues = _all_issues(cwd)
    id_to_type = {i["id"]: i.get("issue_type", "?") for i in issues}
    edges: dict = {}

    def add(frm: str, to: str) -> None:
        edges[(frm, to)] = edges.get((frm, to), 0) + 1

    for issue in issues:
        deps = issue.get("dependencies")
        if deps is None:  # older bd versions omit it: ask per issue
            try:
                deps = db.bd_json("dep", "list", issue["id"], cwd=cwd)
            except RuntimeError:
                deps = []
        for dep in deps or []:
            target = dep.get("depends_on_id", "?")
            add(issue.get("issue_type", "?"), id_to_type.get(target, "?"))
    return edges


def orphans_check(cwd: str) -> list:
    """Beads with broken dependencies (pointing at missing ids).

    Tries ``bd orphans`` first; when its output is not machine-readable,
    falls back to checking every dependency id against ``bd list --all``.
    Returns a list of ``{"id": ..., "missing": ...}`` dicts (empty = healthy).
    """
    try:
        out = db.run_bd("orphans", cwd=cwd)
        if "No orphan" in out:
            return []
        found = re.findall(r"[A-Za-z0-9_-]+-[A-Za-z0-9]+", out)
        return [{"id": f, "missing": "?"} for f in sorted(set(found))]
    except RuntimeError:
        pass
    issues = _all_issues(cwd)
    known = {i["id"] for i in issues}
    broken = []
    for issue in issues:
        for dep in issue.get("dependencies") or []:
            target = dep.get("depends_on_id", "")
            if target and target not in known:
                broken.append({"id": issue["id"], "missing": target})
    return broken


def _print_summary(cwd: str) -> None:
    info = summary(cwd)
    print(f"Total: {info['total']}")
    print("By status:")
    for key in sorted(info["by_status"]):
        print(f"  {key}: {info['by_status'][key]}")
    print("By type:")
    for key in sorted(info["by_type"]):
        print(f"  {key}: {info['by_type'][key]}")
    if info["ready"] is not None:
        print(f"Ready to work: {info['ready']}")


def main(argv: list | None = None) -> int:
    parser = argparse.ArgumentParser(description="Explore an unknown beads database.")
    parser.add_argument("--cwd", default=".", help="project folder with .beads/")
    parser.add_argument("--summary", action="store_true", help="print compact summary")
    parser.add_argument("--shape", action="store_true", help="print type->type blocks")
    parser.add_argument("--orphans", action="store_true", help="print broken dependencies")
    args = parser.parse_args(argv)
    if args.shape:
        for (frm, to), count in sorted(shape(args.cwd).items()):
            print(f"{frm} -[blocks]-> {to}: {count}")
    elif args.orphans:
        broken = orphans_check(args.cwd)
        print("No orphaned issues found" if not broken else broken)
    else:  # default: compact summary
        _print_summary(args.cwd)
    return 0


if __name__ == "__main__":
    sys.exit(main())
