"""Setup check for chapter 00: Ollama, chat, chat_json, embeddings, public data, cache.

Run with: uv run python -m evals_tutorial.check
Exits non-zero if Ollama is unreachable or the chat model fails to answer;
embedding / data problems are reported in the table.
"""

from __future__ import annotations

import json

import httpx
import typer
from rich.console import Console
from rich.table import Table

from evals_tutorial.config import settings
from evals_tutorial.llm import Ollama, cache_stats
from pydantic import BaseModel

app = typer.Typer(add_completion=False)
console = Console()

# Public datasets committed in chapter 00 (README in the same folder says which
# row counts to expect; the test split is fixed and never regenerated).
_PUBLIC_FILES = {
    "mt_bench_answers.jsonl": 480,
    "mt_bench_human_votes.jsonl": 3355,
    "mt_bench_gpt4_votes.jsonl": 2400,
    "ragtruth_test_subset.jsonl": 480,
}


class _CheckReply(BaseModel):
    word: str
    ok: bool


@app.command()
def main() -> None:
    rows: list[tuple[str, str]] = []
    hard_failure = False

    # 1. Ollama reachable + version
    try:
        version = httpx.get(f"{settings.ollama_url}/api/version", timeout=10).json()["version"]
        rows.append(("Ollama reachable", f"yes (version {version})"))
    except Exception as exc:  # noqa: BLE001
        rows.append(("Ollama reachable", f"[red]NO[/red] ({exc}) — try `just tunnel`"))
        hard_failure = True

    client = Ollama()
    if not hard_failure:
        # 2. chat model answers a trivial prompt
        try:
            reply = client.chat([{"role": "user", "content": "Reply with the single word OK"}], max_tokens=8)
            rows.append((f"chat {settings.chat_model} answers", repr(reply.strip())[:120]))
        except Exception as exc:  # noqa: BLE001
            rows.append(("chat answers", f"[red]FAILED[/red] ({exc})"))
            hard_failure = True

        # 3. chat_json returns a valid object for a 2-field schema
        try:
            result = client.chat_json(
                [{"role": "user", "content": 'Reply with {"word": "OK", "ok": true}'}],
                _CheckReply,
                max_tokens=32,
            )
            rows.append(("chat_json 2-field schema", f"model(word={result.word!r}, ok={result.ok}) valid"))
        except Exception as exc:  # noqa: BLE001
            rows.append(("chat_json 2-field schema", f"[red]FAILED[/red] ({exc})"))
            hard_failure = True

        # 4. embedding dimension
        try:
            vector = client.embed_documents(["retrieval-augmented generation"])[0]
            expected_dim = 768  # nomic-embed-text on rtx
            status = "ok" if len(vector) == expected_dim else f"[red]dim {len(vector)} != {expected_dim}[/red]"
            rows.append((f"embedding dim ({settings.embed_model})", f"{len(vector)} {status}"))
        except Exception as exc:  # noqa: BLE001
            rows.append(("embedding dim", f"[red]FAILED[/red] ({exc})"))

    # 5. public data files + row counts
    for name, expected_rows in _PUBLIC_FILES.items():
        path = settings.path("data/public") / name
        try:
            rows_n = sum(1 for line in path.open() if line.strip())
            ok = rows_n == expected_rows
            rows.append((f"data/public/{name}", f"{rows_n} rows {'ok' if ok else f'[red]!= {expected_rows}[/red]'}"))
            if name.endswith(".jsonl"):
                json.loads(path.read_text().splitlines()[0])  # first line parses as JSON
        except Exception as exc:  # noqa: BLE001
            rows.append((f"data/public/{name}", f"[red]MISSING/INVALID[/red] ({exc})"))

    # 6. cache size
    cache = cache_stats()
    total_entries = sum(v["entries"] for v in cache.values())
    total_bytes = sum(v["bytes"] for v in cache.values())
    rows.append(("cache size", f"{total_entries} entries, {total_bytes / 1024:.1f} KB"))

    table = Table(title="evals_tutorial check")
    table.add_column("check")
    table.add_column("result")
    for name, value in rows:
        table.add_row(name, value)
    console.print(table)

    if hard_failure:
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
