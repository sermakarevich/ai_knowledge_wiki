"""Chapter 12 (part 2): kotaemon — an open-source RAG QA web UI.

kotaemon (Cinnamon, Apache-2.0) is aimed at both end users and RAG-pipeline
developers: hybrid full-text + vector retrieval with re-ranking, advanced
citations, and pluggable GraphRAG backends. It is the only app in our survey
with official ``linux/arm64`` Docker images, i.e. native Apple Silicon
support. Image ``ghcr.io/cinnamon/kotaemon:main-lite`` (tag verified at run
time; the ``main-lite`` stream tracks the default branch), container
``rag-kotaemon``, host port 7870 -> container 7860 (``docker-compose.yml``
profile ``kotaemon``), volume ``./data/kotaemon:/app/ktem_app_data``.

kotaemon is a Gradio app, so ``upload``/``ask``/``eval`` drive it with
``gradio_client`` (endpoint names are discovered live via
``client.view_api()`` — Gradio endpoint indices shift between releases, so
the code resolves them by name at runtime and records the resolved map in
the run's ``config.json``).

LIVE PROBE RESULT (2026-09-09, image main-lite, 368 named endpoints): there
is NO stateless chat/upload endpoint. ``/chat_fn`` takes no message argument
(chat history + UI dropdown state only); the message enters through
``/submit_msg(chat_input, chat_history, conv_name, first_selector_choices)``,
which requires a ``conv_name`` row in the app's server-side SQL session DB
(``/new_conv`` creates it inside browser session state, invisible to the API
client) plus the file-selector choices JSON built by the UI. Two probes
failed server-side (``TypeError`` on ``None`` selector choices, then
``NoResultFound`` on the conversation lookup — see findings note). So the
Gradio API is NOT usable for scripted eval; the fallback is Playwright
driving the UI (not attempted this task — no playwright installed, and a
27-question UI-driven eval exceeds the remaining budget). The rows
``12_kotaemon_default`` / ``12_kotaemon_rerank`` are SKIPPED for now.

Ollama wiring (verified against ``flowsettings.py`` on main, 2026-09-09):
``KH_OLLAMA_URL=http://host.docker.internal:11435/v1/`` (default
``http://localhost:11434/v1/``), chat model ``LOCAL_MODEL=qwen3.8:27b``,
embeddings ``LOCAL_MODEL_EMBEDDINGS=nomic-embed-text``.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

import typer
from rich.console import Console

from rag_tutorial.config import settings
from rag_tutorial.evaluate import evaluate_run
from rag_tutorial.golden import load_documents
from rag_tutorial.retrieval_eval import build_parent_child_index
from rag_tutorial.schema import Chunk
from rag_tutorial.sys_lightrag import map_context_to_chunks, mapping_quality

app = typer.Typer(add_completion=False)
console = Console()

RUNS_DIR = settings.path("runs")
BASE_URL = os.environ.get("KOTAEMON_URL", "http://localhost:7870")
CORPUS_MD_DIR = settings.path("data/corpus/md")

N_LLM_CALLS_PER_Q = 1


# -- pure helpers (no network): response parsers ----------------------------


def parse_kotaemon_response(payload) -> tuple[str, list[str]]:
    """Return ``(answer, cited_chunk_texts)`` from a Gradio chat result.

    kotaemon's chat endpoint returns either a dict like
    ``{"output": ..., "references": [...]}`` / ``{"answer": ..., "citations":
    [...]}`` or a plain string (no citations surfaced). Reference entries may
    be strings or ``{"content"/"text"/"chunk", ...}`` dicts. Never raises on
    shape drift — unknown shapes yield ``(str(payload), [])`` so a UI change
    degrades to "answer without sources" instead of crashing an eval.
    """
    if isinstance(payload, str):
        return payload, []
    if not isinstance(payload, dict):
        return str(payload), []
    answer = ""
    for key in ("output", "answer", "response", "text"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            answer = value
            break
    if not answer:
        answer = json.dumps(payload)[:2000]
    raw_refs: list = []
    for key in ("references", "citations", "sources", "contexts"):
        block = payload.get(key)
        if isinstance(block, list):
            raw_refs.extend(block)
    chunks: list[str] = []
    for entry in raw_refs:
        if isinstance(entry, str):
            if entry.strip():
                chunks.append(entry)
        elif isinstance(entry, dict):
            for key in ("content", "text", "chunk", "page_content", "document"):
                value = entry.get(key)
                if isinstance(value, str) and value.strip():
                    chunks.append(value)
                    break
    return answer, chunks


def resolve_endpoint(api_map: dict, candidates: list[str]) -> str:
    """Pick the first candidate endpoint name present in a Gradio API map.

    ``api_map`` maps endpoint path (e.g. ``"/chat"``) to its spec; candidate
    names are matched with or without a leading slash. Raises ``KeyError``
    listing the available endpoints when nothing matches.
    """
    normalised = {path.lstrip("/"): path for path in api_map}
    for name in candidates:
        if name.lstrip("/") in normalised:
            return normalised[name.lstrip("/")]
    raise KeyError(f"none of {candidates} in Gradio API; available: {sorted(api_map)}")


def chunk_texts_to_leaf_chunks(source_texts: list[str], leaves: list[Chunk], k: int = 5) -> tuple[list[Chunk], dict]:
    """Map the app's cited chunks back to our leaf chunk ids (ch11 mapping)."""
    context = "\n\n".join(source_texts)
    ranked = map_context_to_chunks(context, leaves)
    quality = mapping_quality(context, ranked)
    return [chunk for chunk, _score in ranked[:k]], quality


# -- live Gradio driver (network only past this point) ------------------------


def get_client():
    """Build a ``gradio_client.Client`` (lazy import: optional dependency)."""
    from gradio_client import Client

    return Client(BASE_URL)


def upload_files(client, paths: list[Path]) -> dict:
    """Upload files through the resolved Gradio upload endpoint."""
    api_map = {endpoint: True for endpoint in client.view_api(return_format="dict").get("named_endpoints", {})}
    endpoint = resolve_endpoint(api_map, ["upload", "file_upload", "add_files", "ingest"])
    return client.predict([str(p) for p in paths], api_name=endpoint)


CHAT_ENDPOINT_CANDIDATES = ["submit_msg", "chat_fn", "chat", "ask", "query", "predict"]


def ask_question(client, question: str, chat_endpoint: str) -> tuple[str, list[str]]:
    """Ask one question through the resolved Gradio chat endpoint."""
    raw = client.predict(question, api_name=chat_endpoint)
    return parse_kotaemon_response(raw)


# -- CLI ---------------------------------------------------------------------


@app.command()
def upload() -> None:
    """Upload the 12 Markdown files to the running kotaemon instance."""
    client = get_client()
    md_files = sorted(CORPUS_MD_DIR.glob("*.md"))
    if len(md_files) != 12:
        console.print(f"[yellow]warning[/yellow] expected 12 Markdown files, found {len(md_files)}")
    result = upload_files(client, md_files)
    console.print(f"[green]uploaded[/green] {len(md_files)} files: {str(result)[:300]}")


@app.command()
def ask(question: str, k: int = 5) -> None:
    """Ask one question; print the answer plus mapped chunk ids."""
    client = get_client()
    api_map = {endpoint: True for endpoint in client.view_api(return_format="dict").get("named_endpoints", {})}
    endpoint = resolve_endpoint(api_map, CHAT_ENDPOINT_CANDIDATES)
    answer, cited = ask_question(client, question, endpoint)
    console.print(f"[bold]answer:[/bold]\n{answer}\n")
    leaves = build_parent_child_index(load_documents())[0]
    mapped, quality = chunk_texts_to_leaf_chunks(cited, leaves, k=k)
    console.print(f"mapped chunks: {[c.id for c in mapped]} quality={quality}")


@app.command(name="eval")
def eval_cmd(
    mode: str = "default",
    limit: int | None = None,
) -> None:
    """Evaluate kotaemon on the test split (row ``12_kotaemon_<mode>``).

    ``mode`` is ``default`` or ``rerank`` — the retrieval flavour is switched
    in the kotaemon UI/settings before the run and recorded verbatim in the
    run's ``config.json`` (kotaemon has no stable settings API, so the switch
    is manual; see the findings note).
    """
    if mode not in ("default", "rerank"):
        raise typer.BadParameter("mode must be 'default' or 'rerank'")
    client = get_client()
    api_map = {endpoint: True for endpoint in client.view_api(return_format="dict").get("named_endpoints", {})}
    endpoint = resolve_endpoint(api_map, CHAT_ENDPOINT_CANDIDATES)
    leaves = build_parent_child_index(load_documents())[0]
    cache: dict[str, tuple[str, list[str]]] = {}
    qualities: list[dict] = []

    def retrieve_fn(item: dict, _cache=cache, _quals=qualities) -> list[Chunk]:
        answer_text, cited = ask_question(client, item["question"], endpoint)
        _cache[item["id"]] = (answer_text, cited)
        mapped, quality = chunk_texts_to_leaf_chunks(cited, leaves)
        _quals.append({"id": item["id"], **quality})
        return mapped

    def answer_fn(item: dict, retrieved: list[Chunk], _cache=cache) -> tuple[str, list[str], int]:
        answer_text, cited = _cache[item["id"]]
        return answer_text, cited, N_LLM_CALLS_PER_Q

    name = f"12_kotaemon_{mode}"
    console.print(f"[bold]evaluating[/bold] {name}")
    started = time.monotonic()
    evaluate_run(name, chapter="12", answer_fn=answer_fn, retrieve_fn=retrieve_fn, split="test", limit=limit)
    run_dir = RUNS_DIR / name
    (run_dir / "mapping.json").write_text(json.dumps(qualities, indent=2))
    config_record = {
        "app": "kotaemon",
        "mode": mode,
        "chat_endpoint": endpoint,
        "base_url": BASE_URL,
        "note": "retrieval flavour switched manually in UI; no stable settings API",
        "eval_seconds": round(time.monotonic() - started, 1),
    }
    (run_dir / "config.json").write_text(json.dumps({**json.loads((run_dir / "config.json").read_text()), **config_record}, indent=2))


if __name__ == "__main__":
    app()
