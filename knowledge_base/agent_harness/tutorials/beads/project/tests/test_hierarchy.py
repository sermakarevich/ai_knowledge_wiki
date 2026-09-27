"""Test hierarchy.py against a scratch database in ``tmp_path``.

``tmp_path`` is a temporary folder pytest creates just for this test, so
the real tutorial folder and the fleet database are never touched.
"""

import subprocess

from beads_tutorial import db
from beads_tutorial import hierarchy as hier_mod


def _init(repo: str) -> None:
    proc = subprocess.run(
        ["bd", "init", "--prefix", "tut", "--non-interactive"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr


def test_epic_children_and_blocks_edge(tmp_path, monkeypatch):
    # Make `bd` discover the database from cwd instead of a fixed location.
    monkeypatch.delenv("BEADS_DIR", raising=False)
    repo = str(tmp_path)
    _init(repo)

    epic_id = hier_mod.make_epic("Website relaunch", cwd=repo)
    kids = [hier_mod.add_child(epic_id, t, cwd=repo) for t in ("A", "B", "C")]
    assert len(set(kids)) == 3, "three distinct child ids"
    hier_mod.link_blocked(kids[1], kids[0], cwd=repo)

    status = hier_mod.epic_status(epic_id, cwd=repo)
    assert status["epic_id"] == epic_id
    assert status["total_children"] == 3
    assert status["closed_children"] == 0
    assert status["eligible_for_close"] is False

    out = db.run_bd("dep", "cycles", cwd=repo)
    assert "No dependency cycles" in out, "demo graph must be cycle-free"

    ready_ids = [i["id"] for i in db.bd_ready(cwd=repo)]
    assert kids[0] in ready_ids, "blocker child is claimable"
    assert kids[1] not in ready_ids, "blocked child waits on its blocker"


def test_closing_children_makes_epic_eligible(tmp_path, monkeypatch):
    monkeypatch.delenv("BEADS_DIR", raising=False)
    repo = str(tmp_path)
    _init(repo)

    epic_id = hier_mod.make_epic("Tiny epic", cwd=repo)
    kid = hier_mod.add_child(epic_id, "Only child", cwd=repo)
    db.bd_close([kid], cwd=repo, reason="test done")

    status = hier_mod.epic_status(epic_id, cwd=repo)
    assert status["closed_children"] == 1
    assert status["eligible_for_close"] is True
