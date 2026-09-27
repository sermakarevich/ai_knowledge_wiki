"""Smoke test: init a scratch beads repo, create an issue, find it ready.

Everything happens inside ``tmp_path`` (a temporary folder pytest creates
just for this test), so the real tutorial folder and the fleet database
are never touched.
"""

import subprocess

from beads_tutorial import db


def test_bd_init_create_ready(tmp_path, monkeypatch):
    # Make `bd` discover the database from cwd instead of a fixed location.
    monkeypatch.delenv("BEADS_DIR", raising=False)
    repo = str(tmp_path)

    proc = subprocess.run(
        ["bd", "init", "--prefix", "probe", "--non-interactive"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr

    created = db.bd_create("Probe task", cwd=repo)
    assert created.startswith("probe-")

    ready = db.bd_ready(cwd=repo)
    assert created in [issue["id"] for issue in ready]
