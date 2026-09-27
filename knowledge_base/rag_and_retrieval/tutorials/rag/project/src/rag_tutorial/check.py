"""Sanity check for chapter 00: Ollama, Qdrant, corpus, and cache.

Run with: uv run python -m rag_tutorial.check
Exits non-zero if Ollama is unreachable or the chat model fails to answer;
Qdrant-not-started and an empty corpus are reported but do not fail the check
(they are expected before `just up qdrant` / `just corpus`).
"""

from __future__ import annotations

import sys

import httpx
import typer
from rich.console import Console
from rich.table import Table

from rag_tutorial.config import settings
from rag_tutorial.corpus import MD_DIR, load_papers
from rag_tutorial.llm import Ollama, cache_stats

app = typer.Typer(add_completion=False)
console = Console()


@app.command()
def main() -> None:
    rows: list[tuple[str, str]] = []
    hard_failure = False

    try:
        version = httpx.get(f"{settings.ollama_url}/api/version", timeout=10).json()["version"]
        rows.append(("Ollama reachable", f"yes (version {version})"))
    except Exception as exc:  # noqa: BLE001
        rows.append(("Ollama reachable", f"[red]NO[/red] ({exc}) — try `just tunnel`"))
        hard_failure = True

    client = Ollama()
    if not hard_failure:
        try:
            reply = client.chat([{"role": "user", "content": "Reply with the single word OK"}], max_tokens=8)
            rows.append((f"chat model {settings.chat_model} answers", repr(reply.strip())))
        except Exception as exc:  # noqa: BLE001
            rows.append(("chat model answers", f"[red]FAILED[/red] ({exc})"))
            hard_failure = True

        try:
            vector = client.embed_documents(["retrieval-augmented generation"])[0]
            rows.append((f"embedding dim ({settings.embed_model})", str(len(vector))))
        except Exception as exc:  # noqa: BLE001
            rows.append(("embedding dim", f"[red]FAILED[/red] ({exc})"))

    try:
        httpx.get(f"{settings.qdrant_url}/readyz", timeout=5).raise_for_status()
        rows.append(("Qdrant /readyz", "ok"))
    except Exception:  # noqa: BLE001
        rows.append(("Qdrant /readyz", "not started — `just up qdrant`"))

    papers = load_papers()
    n_parsed = sum(1 for p in papers if (MD_DIR / f"{p['id']}.md").exists())
    rows.append(("corpus present", f"{n_parsed}/{len(papers)} papers parsed"))

    cache = cache_stats()
    total_entries = sum(v["entries"] for v in cache.values())
    total_bytes = sum(v["bytes"] for v in cache.values())
    rows.append(("cache size", f"{total_entries} entries, {total_bytes / 1024:.1f} KB"))

    table = Table(title="rag_tutorial check")
    table.add_column("check")
    table.add_column("result")
    for name, value in rows:
        table.add_row(name, value)
    console.print(table)

    if hard_failure:
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
