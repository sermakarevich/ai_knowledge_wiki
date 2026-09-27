"""Runs on rtx: report GPU/Ollama status, and wait for the GPU to be idle-and-free
before a training job starts. Never kills anything — it only waits and, if Ollama's
model has been idle, asks Ollama itself to unload it (`ollama stop`).
"""

import subprocess
import time

import typer

app = typer.Typer(add_completion=False)


def parse_nvidia_smi(text: str, fields: list[str] | None = None) -> list[dict[str, str]]:
    """Parse `nvidia-smi --query-gpu=... --format=csv[,noheader]` output.

    If `fields` is given, `text` has no header row (the `noheader` format) and
    `fields` supplies the column names in the same order as the query. Otherwise
    the first line of `text` is used as the header.
    """
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    if not lines:
        return []
    if fields is None:
        header = [h.strip() for h in lines[0].split(",")]
        rows = lines[1:]
    else:
        header = fields
        rows = lines
    return [dict(zip(header, (v.strip() for v in row.split(",")))) for row in rows]


def parse_ollama_ps(text: str) -> list[str]:
    """Return the model names currently loaded, from `ollama ps` output (header + rows)."""
    lines = [line for line in text.strip().splitlines() if line.strip()]
    if len(lines) <= 1:
        return []
    return [line.split()[0] for line in lines[1:]]


def _run(cmd: list[str]) -> str:
    return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout


@app.command()
def status() -> None:
    """Print nvidia-smi numbers and which Ollama models are loaded."""
    print(_run(["nvidia-smi", "--query-gpu=index,name,memory.used,memory.total,utilization.gpu", "--format=csv"]))
    print(_run(["ollama", "ps"]))


def _read_gpu(total_mib: float) -> tuple[float, float]:
    rows = parse_nvidia_smi(
        _run(["nvidia-smi", "--query-gpu=utilization.gpu,memory.used", "--format=csv,noheader,nounits"]),
        fields=["utilization.gpu", "memory.used"],
    )
    util = float(rows[0]["utilization.gpu"])
    used_mib = float(rows[0]["memory.used"])
    free_gb = (total_mib - used_mib) / 1024
    return util, free_gb


@app.command()
def free(
    min_free_gb: float = 20,
    idle_seconds: int = 60,
    max_wait_minutes: int = 360,
    confirm_checks: int = 3,
    confirm_interval_seconds: float = 5,
) -> int:
    """Wait until the GPU has >= min_free_gb free, stopping an idle Ollama model if needed.

    Never stops a model that is actively serving a request (utilisation >= 10%) —
    it only waits for someone else's job to finish. Exits 1 if still busy after
    max_wait_minutes.

    A single free reading can be a false positive on a shared GPU where another
    process reclaims memory within seconds (observed: an external Ollama workload
    reappearing ~5-10s after being reported idle). Before declaring the GPU free,
    `confirm_checks` consecutive readings spaced `confirm_interval_seconds` apart
    must all still show >= min_free_gb; any drop below the threshold resets the
    confirmation and falls back to the normal wait loop.
    """
    total_mib = float(
        parse_nvidia_smi(_run(["nvidia-smi", "--query-gpu=memory.total", "--format=csv,noheader,nounits"]), fields=["memory.total"])[0]["memory.total"]
    )
    idle_since: float | None = None
    deadline = time.monotonic() + max_wait_minutes * 60
    while time.monotonic() < deadline:
        util, free_gb = _read_gpu(total_mib)

        if free_gb >= min_free_gb:
            confirmed = True
            for _ in range(confirm_checks - 1):
                time.sleep(confirm_interval_seconds)
                util, free_gb = _read_gpu(total_mib)
                if free_gb < min_free_gb:
                    confirmed = False
                    print(f"GPU freed then reclaimed ({free_gb:.1f} GB < {min_free_gb} GB) — resuming wait")
                    break
            if confirmed:
                print(f"GPU free: {free_gb:.1f} GB >= {min_free_gb} GB (confirmed over {confirm_checks} checks)")
                return 0
            continue

        loaded = parse_ollama_ps(_run(["ollama", "ps"]))
        now = time.monotonic()
        if util >= 10:
            idle_since = None
            print("GPU busy (Ollama serving another client), waiting...")
        else:
            if idle_since is None:
                idle_since = now
            if loaded and now - idle_since >= idle_seconds:
                for model in loaded:
                    print(f"idle for {idle_seconds}s, stopping {model}")
                    subprocess.run(["ollama", "stop", model], check=False)

        time.sleep(5)

    print(f"GPU still busy after {max_wait_minutes} minutes")
    raise typer.Exit(1)


if __name__ == "__main__":
    app()
