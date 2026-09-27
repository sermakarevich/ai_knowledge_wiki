"""Tiny wrapper around the ``bd`` CLI (Command-Line Interface) for beads.

``bd`` is a command-line program, so instead of importing a library we run
it with ``subprocess`` (Python's built-in way of starting other programs)
and read back its output.

Every function takes ``cwd`` (current working directory): the folder of the
project whose ``.beads/`` database you want to talk to. ``bd`` finds the
database automatically by looking at that folder, so we never pass ``--db``
by hand.
"""

import json
import os
import subprocess


def _clean_env() -> dict:
    """Copy of the environment without ``BEADS_DIR``.

    ``BEADS_DIR`` points ``bd`` at one fixed database and overrides the
    automatic discovery from ``cwd``. Removing it makes sure the commands
    below always use the database in ``cwd``.
    """
    return {k: v for k, v in os.environ.items() if k != "BEADS_DIR"}


def run_bd(*args: str, cwd: str) -> str:
    """Run ``bd`` with the given arguments and return its standard output.

    Raises ``RuntimeError`` with the program's error message when ``bd``
    exits with a failure.
    """
    proc = subprocess.run(
        ["bd", *args], cwd=cwd, capture_output=True, text=True, env=_clean_env()
    )
    if proc.returncode != 0:
        message = proc.stderr.strip() or proc.stdout.strip()
        raise RuntimeError(message or f"bd exited with code {proc.returncode}")
    return proc.stdout


def bd_json(*args: str, cwd: str) -> list | dict:
    """Run ``bd`` and parse its output as JSON (JavaScript Object Notation).

    ``--json`` is added automatically when the caller did not pass it.
    Returns a list (for commands like ``bd ready``) or a dict (for
    commands like ``bd create`` that return one object).
    """
    if "--json" not in args:
        args = (*args, "--json")
    return json.loads(run_bd(*args, cwd=cwd))


def bd_create(
    title: str, cwd: str, type: str = "task", priority: int = 2, description: str = ""
) -> str:
    """Create one issue and return its id (for example ``probe-a3f2dd``).

    ``type`` is the kind of issue (``task``, ``bug``, ``feature``, ...).
    ``priority`` is a number from 0 (critical) to 4 (backlog); 2 is medium.
    """
    args = [title, "--type", type, "--priority", str(priority)]
    if description:
        args += ["--description", description]
    data = bd_json("create", *args, cwd=cwd)
    return data["id"]


def bd_ready(cwd: str) -> list:
    """Return open issues that have no blockers, as a list of dicts."""
    return bd_json("ready", cwd=cwd)


def bd_close(ids: list[str], cwd: str, reason: str = "") -> None:
    """Close the issues with the given ids.

    ``reason`` is an optional short note stored with the close action.
    """
    args = ["close", *ids]
    if reason:
        args += ["--reason", reason]
    run_bd(*args, cwd=cwd)
