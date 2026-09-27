"""Test seed.py: double run creates nothing new, total stays 6.

Everything happens inside ``tmp_path`` (a temporary folder pytest creates
just for this test), so the real tutorial folder and the fleet database
are never touched.
"""

import subprocess

from beads_tutorial import db
from beads_tutorial import seed as seed_mod


def _init(repo: str) -> None:
    proc = subprocess.run(
        ["bd", "init", "--prefix", "tut", "--non-interactive"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr


def test_seed_twice_creates_nothing_new(tmp_path, monkeypatch):
    # Make `bd` discover the database from cwd instead of a fixed location.
    monkeypatch.delenv("BEADS_DIR", raising=False)
    repo = str(tmp_path)
    _init(repo)

    first = seed_mod.seed(repo)
    assert len(first) == 6

    before = len(db.bd_json("list", "--all", cwd=repo))
    second = seed_mod.seed(repo)
    after = len(db.bd_json("list", "--all", cwd=repo))

    assert second == first, "second run must reuse the same beads"
    assert after == before == 6, "second run must create 0 new beads"
