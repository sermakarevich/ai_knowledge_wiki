"""Test patterns.py against a scratch database in ``tmp_path``.

``tmp_path`` is a temporary folder pytest creates just for this test, so
the real tutorial folder and the fleet database are never touched.
"""

import subprocess

from beads_tutorial import db
from beads_tutorial import patterns as pat_mod
from beads_tutorial import seed as seed_mod


def _init(repo: str) -> None:
    proc = subprocess.run(
        ["bd", "init", "--prefix", "tut", "--non-interactive"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr


def test_claim_next_returns_id_and_close_removes_from_ready(tmp_path, monkeypatch):
    # Make `bd` discover the database from cwd instead of a fixed location.
    monkeypatch.delenv("BEADS_DIR", raising=False)
    repo = str(tmp_path)
    _init(repo)
    seed_mod.seed(repo)

    bead_id = pat_mod.claim_next(repo)
    assert bead_id is not None, "seeded graph must have ready work"

    ready_ids = [i["id"] for i in db.bd_ready(cwd=repo)]
    assert bead_id not in ready_ids, "claimed bead leaves the ready list"

    pat_mod.close_with_reason(bead_id, repo, "test done")
    all_ids = [i["id"] for i in db.bd_json("list", "--all", cwd=repo)]
    assert bead_id in all_ids, "closed bead still exists in --all"
    ready_ids = [i["id"] for i in db.bd_ready(cwd=repo)]
    assert bead_id not in ready_ids, "closed bead stays out of ready"


def test_ready_loop_closes_batch(tmp_path, monkeypatch):
    monkeypatch.delenv("BEADS_DIR", raising=False)
    repo = str(tmp_path)
    _init(repo)
    seed_mod.seed(repo)

    closed = pat_mod.ready_loop(repo, limit=2)
    assert len(closed) == 2, "two rounds must close two beads"
    ready_ids = [i["id"] for i in db.bd_ready(cwd=repo)]
    for bead_id in closed:
        assert bead_id not in ready_ids, f"{bead_id} must stay out of ready"

    # Empty database: nothing ready, loop returns [] instead of crashing.
    closed_rest = pat_mod.ready_loop(repo, limit=10)
    assert isinstance(closed_rest, list)
