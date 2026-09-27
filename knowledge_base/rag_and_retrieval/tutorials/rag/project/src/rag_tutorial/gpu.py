"""GPU-politeness check: the RTX 4090 on `rtx` is shared with the `llm_training`
tutorial. Before starting a batch of more than ~100 LLM calls, check that no
non-Ollama process is holding a lot of VRAM; if one is, wait instead of piling on.

Run with: uv run python -m rag_tutorial.gpu
"""

from __future__ import annotations

import subprocess
import time

import typer

app = typer.Typer(add_completion=False)

_SSH_CMD = ["ssh", "-o", "ClearAllForwardings=yes", "rtx"]
_QUERY = ["nvidia-smi", "--query-compute-apps=pid,process_name,used_memory", "--format=csv,noheader"]
_MAX_OTHER_PROCESS_MB = 6 * 1024


def _query_gpu() -> str:
    result = subprocess.run(_SSH_CMD + _QUERY, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        raise RuntimeError(f"nvidia-smi over ssh failed: {result.stderr.strip()}")
    return result.stdout


def parse_compute_apps(text: str) -> list[dict]:
    """Parse `nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader`."""
    rows = []
    for line in text.strip().splitlines():
        if not line.strip():
            continue
        pid, name, mem = (part.strip() for part in line.split(",", 2))
        rows.append({"pid": pid, "process_name": name, "used_memory_mib": int(mem.split()[0])})
    return rows


def is_gpu_free_for_us(rows: list[dict]) -> bool:
    """True unless a non-ollama process holds more than the polite VRAM budget.

    Ollama's actual GPU worker process is not called "ollama" — it shows up as
    a path like `/usr/local/lib/ollama/llama-server` — so we match on
    "ollama" appearing anywhere in the process name/path, not an exact match.
    """
    return not any(
        "ollama" not in row["process_name"].lower() and row["used_memory_mib"] > _MAX_OTHER_PROCESS_MB for row in rows
    )


@app.command()
def check() -> None:
    """Print GPU compute processes; exit 1 if a non-ollama one uses > 6 GB."""
    text = _query_gpu()
    rows = parse_compute_apps(text)
    if not rows:
        print("no compute processes on the GPU")
    for row in rows:
        print(f"pid={row['pid']} process={row['process_name']} used_memory={row['used_memory_mib']} MiB")
    if is_gpu_free_for_us(rows):
        print("GPU is polite to use")
    else:
        print("a non-ollama process is using > 6 GB, back off")
        raise typer.Exit(1)


def wait_for_gpu(max_hours: float = 6, poll_seconds: int = 600) -> None:
    """Block until the GPU is polite to use, polling every `poll_seconds`.

    Used by later chapters before a batch of more than ~100 LLM calls.
    """
    deadline = time.monotonic() + max_hours * 3600
    while time.monotonic() < deadline:
        rows = parse_compute_apps(_query_gpu())
        if is_gpu_free_for_us(rows):
            return
        print(f"GPU busy with a non-ollama job, waiting {poll_seconds}s...")
        time.sleep(poll_seconds)
    raise TimeoutError(f"GPU still busy after {max_hours} hours")


if __name__ == "__main__":
    app()
