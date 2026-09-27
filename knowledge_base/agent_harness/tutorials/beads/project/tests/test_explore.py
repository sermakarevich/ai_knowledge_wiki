"""Test explore.py against a freshly seeded scratch beads repo.

Seeds 2 tasks + 1 bug with one dependency (bug blocked by a task),
then checks ``summary()`` counts match and ``shape()`` is not empty.
Everything happens inside ``tmp_path`` so real databases are untouched.
"""

import subprocess

from beads_tutorial import db
from beads_tutorial import explore


def _seed(repo: str) -> None:
    proc = subprocess.run(
        ["bd", "init", "--prefix", "tut", "--non-interactive"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr

    first = db.bd_create("First task", cwd=repo, type="task")
    db.bd_create("Second task", cwd=repo, type="task")
    bug = db.bd_create("A bug", cwd=repo, type="bug", priority=0)
    db.run_bd("dep", "add", bug, first, cwd=repo)


def test_summary_counts_match_seed(tmp_path, monkeypatch):
    monkeypatch.delenv("BEADS_DIR", raising=False)
    repo = str(tmp_path)
    _seed(repo)

    info = explore.summary(repo)
    assert info["total"] == 3
    assert info["by_status"] == {"open": 3}
    assert info["by_type"] == {"task": 2, "bug": 1}


def test_shape_not_empty(tmp_path, monkeypatch):
    monkeypatch.delenv("BEADS_DIR", raising=False)
    repo = str(tmp_path)
    _seed(repo)

    edges = explore.shape(repo)
    assert edges, "expected at least one type->type edge"
    assert edges.get(("bug", "task")) == 1
    assert explore.orphans_check(repo) == []
