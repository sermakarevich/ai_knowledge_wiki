"""Driver patterns: claim work, close it, loop until nothing is ready.

Mirrors the neo4j ``05_python_patterns.md`` idea: small reusable functions
on top of :mod:`beads_tutorial.db` plus a batch loop that is safe to run
more than once (closing an already-closed bead is skipped, claiming an
empty ready list returns ``None``).

Usage::

    python -m beads_tutorial.patterns --cwd <dir>
    python -m beads_tutorial.patterns --cwd <dir> --limit 2
"""

import argparse
import sys

from beads_tutorial import db


def claim_next(cwd: str) -> str | None:
    """Claim the first ready bead and return its id, or ``None``.

    ``bd ready --json`` lists open beads with no blockers. We take the
    first one and run ``bd update <id> --claim`` (sets assignee to you,
    status to ``in_progress``). Empty ready list means ``None``.
    """
    ready = db.bd_ready(cwd=cwd)
    if not ready:
        return None
    bead_id = ready[0]["id"]
    db.run_bd("update", bead_id, "--claim", cwd=cwd)
    return bead_id


def close_with_reason(bead_id: str, cwd: str, reason: str) -> None:
    """Close one bead with a short note (``bd close <id> --reason``)."""
    db.bd_close([bead_id], cwd=cwd, reason=reason)


def ready_loop(cwd: str, limit: int = 5) -> list[str]:
    """Claim and close up to ``limit`` beads, return the closed ids.

    Each round claims the first ready bead, closes it with
    ``"done via ready_loop"``, and repeats. Stops early when nothing is
    ready. Closing unblocks dependents, so later rounds see new beads.
    """
    closed: list[str] = []
    for _ in range(limit):
        bead_id = claim_next(cwd)
        if bead_id is None:
            break
        close_with_reason(bead_id, cwd, "done via ready_loop")
        closed.append(bead_id)
    return closed


def main(argv: list | None = None) -> int:
    parser = argparse.ArgumentParser(description="Claim+close demo loop.")
    parser.add_argument("--cwd", default=".", help="project folder with .beads/")
    parser.add_argument("--limit", type=int, default=5, help="max beads to close")
    args = parser.parse_args(argv)
    for bead_id in ready_loop(args.cwd, args.limit):
        print(bead_id)
    return 0


if __name__ == "__main__":
    sys.exit(main())
