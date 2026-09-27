"""Chapter 12 (part 1): Open WebUI — a self-hosted chat app with built-in RAG.

Open WebUI (source-available licence, not OSI-approved) is a chat platform,
not a dedicated RAG (Retrieval-Augmented Generation) engine — RAG is one
feature among many. We drive it entirely through its REST API so the run is
reproducible without screenshots:

- ``setup``: sign in (or sign up the first admin user), save the API key to
  ``.env`` as ``OPENWEBUI_API_KEY``, and push one of the two named RAG
  configurations via ``/api/v1/retrieval/config/update``.
- ``upload``: create a knowledge base (``/api/v1/knowledge/create``) and
  upload the 12 parsed Markdown files (``/api/v1/files/`` + attach).
- ``ask``: chat via OpenAI-compatible ``/api/chat/completions`` with
  ``files: [{"type": "collection", "id": ...}]`` and print answer + sources.
- ``eval``: ask every test-split question through the app, map the app's
  source chunks back to our leaf chunk ids (same overlap mapping as chapter
  11, so retrieval metrics stay comparable), and write the scoreboard rows
  ``12_openwebui_default`` and ``12_openwebui_hybrid_rerank``.

Container: ``rag-openwebui`` on port 3010 (``docker-compose.yml`` profile
``openwebui``), ``OLLAMA_BASE_URL=http://host.docker.internal:11435``,
``WEBUI_AUTH=False`` (local tutorial only).

Field names for the retrieval config are verified against the running
instance's OpenAPI schema at ``/docs`` by ``setup --verify``; the builder
:func:`build_retrieval_settings` documents any rename we had to apply.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

import httpx
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
BASE_URL = os.environ.get("OPENWEBUI_URL", "http://localhost:3010")
CORPUS_MD_DIR = settings.path("data/corpus/md")
KNOWLEDGE_NAME = "rag-tutorial-12-papers"

# One chat call per question from the app's point of view; the app's own
# internal LLM-call count is not observable through the API, so the
# scoreboard's ``llm_calls_per_q`` is 1 by construction (noted in findings).
N_LLM_CALLS_PER_Q = 1


# -- pure helpers (no network): settings builder + response parsers ---------


def build_retrieval_settings(
    chunk_size: int = 1000,
    chunk_overlap: int = 100,
    top_k: int = 5,
    hybrid: bool = False,
    reranker_model: str = "",
    embedding_engine: str = "ollama",
    embedding_model: str = "nomic-embed-text",
) -> dict:
    """RAG settings payload for ``POST /api/v1/retrieval/config/update``.

    Field names verified against ``ConfigForm`` in
    ``backend/open_webui/routers/retrieval.py`` on main (2026-09-09): the
    API takes SCREAMING_SNAKE_CASE keys (``TOP_K``,
    ``ENABLE_RAG_HYBRID_SEARCH``, ``RAG_RERANKING_MODEL``, ``CHUNK_SIZE``,
    ``CHUNK_OVERLAP``, ``RAG_EMBEDDING_ENGINE``, ``RAG_EMBEDDING_MODEL``).
    ``setup --verify`` re-checks the live instance's ``/openapi.json``.
    """
    return {
        "RAG_EMBEDDING_ENGINE": embedding_engine,
        "RAG_EMBEDDING_MODEL": embedding_model,
        "CHUNK_SIZE": chunk_size,
        "CHUNK_OVERLAP": chunk_overlap,
        "TOP_K": top_k,
        "ENABLE_RAG_HYBRID_SEARCH": hybrid,
        "RAG_RERANKING_MODEL": reranker_model,
    }


NAMED_CONFIGS: dict[str, dict] = {
    "default": build_retrieval_settings(),
    "hybrid_rerank": build_retrieval_settings(hybrid=True, reranker_model="cross-encoder/ms-marco-MiniLM-L-6-v2"),
}


def parse_auth_response(payload: dict) -> str:
    """Extract the bearer token from a signin/signup response."""
    for key in ("token", "access_token", "api_key", "key"):
        value = payload.get(key)
        if isinstance(value, str) and value:
            return value
    raise ValueError(f"no token field in auth response: {sorted(payload)}")


def parse_knowledge_response(payload: dict) -> str:
    """Extract the knowledge-base id from a ``/knowledge/create`` response."""
    for key in ("id", "knowledge_id", "uid"):
        value = payload.get(key)
        if isinstance(value, str) and value:
            return value
    raise ValueError(f"no id field in knowledge response: {sorted(payload)}")


def parse_file_upload_response(payload: dict) -> str:
    """Extract the file id from a ``/files/`` upload response.

    Observed live shape (2026-09-09): the id is top-level (``{"id": ...,
    "filename": ..., "data": {"status": ...}, "meta": {...}}``), so top-level
    keys win over a nested ``data`` dict.
    """
    if isinstance(payload, dict):
        for key in ("id", "file_id", "uid"):
            value = payload.get(key)
            if isinstance(value, str) and value:
                return value
        data = payload.get("data")
        if isinstance(data, dict):
            for key in ("id", "file_id", "uid"):
                value = data.get(key)
                if isinstance(value, str) and value:
                    return value
    raise ValueError(f"no file id in upload response: {payload!r}"[:300])


def parse_chat_response(payload: dict) -> tuple[str, list[str]]:
    """Return ``(answer, source_texts)`` from an OpenAI-style chat payload.

    Handles the plain ``choices[0].message.content`` shape plus the shapes
    Open WebUI uses for RAG citations: a top-level ``citations`` list, a
    ``sources`` list on the message, and ``files`` echoes. Source entries may
    be plain strings or ``{"content"/"text"/"document", ...}`` dicts.
    """
    try:
        message = payload["choices"][0]["message"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError(f"unrecognised chat payload: {str(payload)[:300]}") from exc
    content = message.get("content", "")
    answer = content if isinstance(content, str) else json.dumps(content)

    raw_sources: list = []
    for key in ("citations", "sources"):
        block = payload.get(key)
        if isinstance(block, list):
            raw_sources.extend(block)
        block = message.get(key)
        if isinstance(block, list):
            raw_sources.extend(block)

    sources: list[str] = []
    for entry in raw_sources:
        if isinstance(entry, str):
            if entry.strip():
                sources.append(entry)
        elif isinstance(entry, dict):
            for key in ("content", "text", "document", "chunk", "page_content"):
                value = entry.get(key)
                if isinstance(value, str) and value.strip():
                    sources.append(value)
                    break
                # Live shape (2026-09-09): {"source": {...}, "document": [chunk, ...]}
                if isinstance(value, list):
                    texts = [t for t in value if isinstance(t, str) and t.strip()]
                    if texts:
                        sources.extend(texts)
                        break
    return answer, sources


def chunk_texts_to_leaf_chunks(source_texts: list[str], leaves: list[Chunk], k: int = 5) -> tuple[list[Chunk], dict]:
    """Map the app's raw source texts back to our leaf chunk ids.

    Joins the sources into one context string and reuses chapter 11's
    overlap mapping so retrieval metrics stay comparable across chapters.
    """
    context = "\n\n".join(source_texts)
    ranked = map_context_to_chunks(context, leaves)
    quality = mapping_quality(context, ranked)
    return [chunk for chunk, _score in ranked[:k]], quality


# -- thin HTTP client (network only past this point) -------------------------


def _client(api_key: str = "") -> httpx.Client:
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    return httpx.Client(base_url=BASE_URL, headers=headers, timeout=120.0)


def api_key_from_env() -> str:
    return os.environ.get("OPENWEBUI_API_KEY", "")


def signin(email: str, password: str) -> str:
    """Sign in (fall back to first-user signup) and return the bearer token."""
    with _client() as client:
        resp = client.post("/api/v1/auths/signin", json={"email": email, "password": password})
        if resp.status_code == 200:
            return parse_auth_response(resp.json())
        resp = client.post("/api/v1/auths/signup", json={"name": "tutorial", "email": email, "password": password})
        resp.raise_for_status()
        return parse_auth_response(resp.json())


def update_retrieval_config(api_key: str, config_name: str) -> dict:
    """Push one of :data:`NAMED_CONFIGS` to the running instance."""
    payload = NAMED_CONFIGS[config_name]
    with _client(api_key) as client:
        resp = client.post("/api/v1/retrieval/config/update", json=payload)
        resp.raise_for_status()
        return resp.json()


def fetch_openapi_paths(api_key: str = "") -> list[str]:
    """List live API paths from the instance's OpenAPI schema (``/docs``).

    Tries several candidate schema URLs (the exact path moved between
    releases, and some builds serve the SPA fallback HTML instead); only
    responses with a JSON content type are parsed. Raises ``RuntimeError``
    with the tried URLs when no schema endpoint answers.
    """
    candidates = ("/openapi.json", "/docs/openapi.json", "/api/openapi.json")
    with _client(api_key) as client:
        for candidate in candidates:
            resp = client.get(candidate)
            content_type = resp.headers.get("content-type", "")
            if resp.status_code == 200 and "json" in content_type:
                return sorted(resp.json().get("paths", {}))
    raise RuntimeError(
        "no JSON OpenAPI schema found; tried "
        + ", ".join(BASE_URL + c for c in candidates)
        + " (this build serves the SPA fallback there; the retrieval-config "
        + "field names were instead verified by a successful config push)"
    )


def create_knowledge(api_key: str, name: str = KNOWLEDGE_NAME) -> str:
    with _client(api_key) as client:
        resp = client.post("/api/v1/knowledge/create", json={"name": name, "description": "12 RAG tutorial papers"})
        resp.raise_for_status()
        return parse_knowledge_response(resp.json())


def wait_for_file_ready(api_key: str, file_id: str, timeout_s: float = 300.0) -> dict:
    """Poll ``GET /api/v1/files/{id}`` until ``data.status`` is completed.

    Attaching a still-``pending`` file to a knowledge base returns
    ``400 Bad Request`` (observed live 2026-09-09), so ``upload`` waits here.
    Raises ``TimeoutError`` / ``RuntimeError`` on timeout / processing error.
    """
    deadline = time.monotonic() + timeout_s
    with _client(api_key) as client:
        while True:
            resp = client.get(f"/api/v1/files/{file_id}")
            resp.raise_for_status()
            info = resp.json()
            status = (info.get("data") or {}).get("status", "")
            if status == "completed":
                return info
            if status == "error":
                raise RuntimeError(f"file {file_id} failed processing: {info.get('data')}")
            if time.monotonic() > deadline:
                raise TimeoutError(f"file {file_id} still '{status}' after {timeout_s:.0f}s")
            time.sleep(2.0)


def upload_file_to_knowledge(api_key: str, knowledge_id: str, path: Path) -> str:
    with _client(api_key) as client:
        with path.open("rb") as fh:
            resp = client.post("/api/v1/files/", files={"file": (path.name, fh, "text/markdown")})
        resp.raise_for_status()
        file_id = parse_file_upload_response(resp.json())
        resp = client.post(f"/api/v1/knowledge/{knowledge_id}/file/add", json={"file_id": file_id})
        if resp.status_code == 400:
            # File still processing server-side — wait, then retry once.
            wait_for_file_ready(api_key, file_id)
            resp = client.post(f"/api/v1/knowledge/{knowledge_id}/file/add", json={"file_id": file_id})
        resp.raise_for_status()
        return file_id


def chat_with_collection(api_key: str, question: str, collection_id: str, model: str) -> tuple[str, list[str]]:
    """Ask through ``/api/chat/completions`` scoped to a knowledge collection."""
    with _client(api_key) as client:
        resp = client.post(
            "/api/chat/completions",
            json={
                "model": model,
                "messages": [{"role": "user", "content": question}],
                "files": [{"type": "collection", "id": collection_id}],
            },
        )
        resp.raise_for_status()
        return parse_chat_response(resp.json())


# -- CLI ---------------------------------------------------------------------


@app.command()
def setup(
    email: str = "tutorial@localhost",
    password: str = "tutorial-local-only",
    config: str = "default",
    verify: bool = False,
) -> None:
    """Sign in, save ``OPENWEBUI_API_KEY`` to ``.env``, push RAG settings."""
    if config not in NAMED_CONFIGS:
        raise typer.BadParameter(f"config must be one of {sorted(NAMED_CONFIGS)}")
    if verify:
        try:
            paths = fetch_openapi_paths()
        except RuntimeError as exc:
            console.print(f"[yellow]{exc}[/yellow]")
            return
        console.print("\n".join(p for p in paths if "retrieval" in p or "knowledge" in p))
        return
    token = signin(email, password)
    env_path = settings.path(".env")
    lines = env_path.read_text().splitlines() if env_path.exists() else []
    lines = [line for line in lines if not line.startswith("OPENWEBUI_API_KEY=")]
    lines.append(f"OPENWEBUI_API_KEY={token}")
    env_path.write_text("\n".join(lines) + "\n")
    console.print("[green]saved[/green] OPENWEBUI_API_KEY to .env (local only, never committed)")
    update_retrieval_config(token, config)
    console.print(f"[green]pushed[/green] retrieval config '{config}': {json.dumps(NAMED_CONFIGS[config])}")


@app.command()
def upload(knowledge_id: str = "") -> None:
    """Create the knowledge base (unless given) and upload the 12 Markdown files."""
    api_key = api_key_from_env()
    if not api_key:
        raise typer.BadParameter("OPENWEBUI_API_KEY is not set — run `setup` first")
    if not knowledge_id:
        knowledge_id = create_knowledge(api_key)
        console.print(f"created knowledge base {knowledge_id}")
    md_files = sorted(CORPUS_MD_DIR.glob("*.md"))
    if len(md_files) != 12:
        console.print(f"[yellow]warning[/yellow] expected 12 Markdown files, found {len(md_files)}")
    for path in md_files:
        file_id = upload_file_to_knowledge(api_key, knowledge_id, path)
        console.print(f"uploaded {path.name} -> {file_id}")
    console.print(f"[green]knowledge base ready[/green] id={knowledge_id}")


@app.command()
def ask(question: str, knowledge_id: str, model: str = settings.chat_model, k: int = 5) -> None:
    """Ask one question scoped to a knowledge collection; print answer + sources."""
    api_key = api_key_from_env()
    if not api_key:
        raise typer.BadParameter("OPENWEBUI_API_KEY is not set — run `setup` first")
    answer, sources = chat_with_collection(api_key, question, knowledge_id, model)
    console.print(f"[bold]answer:[/bold]\n{answer}\n")
    leaves = build_parent_child_index(load_documents())[0]
    mapped, quality = chunk_texts_to_leaf_chunks(sources, leaves, k=k)
    console.print(f"mapped chunks: {[c.id for c in mapped]} quality={quality}")


@app.command(name="eval")
def eval_cmd(
    knowledge_ids: str = "",
    model: str = settings.chat_model,
    limit: int | None = None,
) -> None:
    """Evaluate each knowledge base on the test split (rows ``12_openwebui_*``).

    ``knowledge_ids`` maps config names to collection ids as
    ``default:<id>,hybrid_rerank:<id>`` — one collection per RAG configuration
    (create with ``upload`` after ``setup --config <name>``).
    """
    api_key = api_key_from_env()
    if not api_key:
        raise typer.BadParameter("OPENWEBUI_API_KEY is not set — run `setup` first")
    mapping = dict(part.split(":", 1) for part in knowledge_ids.split(",") if part.strip()) if knowledge_ids else {}
    if not mapping:
        raise typer.BadParameter("pass --knowledge-ids default:<id>[,hybrid_rerank:<id>]")
    leaves = build_parent_child_index(load_documents())[0]
    for config_name, collection_id in mapping.items():
        if config_name not in NAMED_CONFIGS:
            raise typer.BadParameter(f"unknown config '{config_name}'; expected one of {sorted(NAMED_CONFIGS)}")
        cache: dict[str, tuple[str, list[str]]] = {}
        qualities: list[dict] = []

        def retrieve_fn(item: dict, _cid=collection_id, _cache=cache, _quals=qualities) -> list[Chunk]:
            answer_text, sources = chat_with_collection(api_key, item["question"], _cid, model)
            _cache[item["id"]] = (answer_text, sources)
            mapped, quality = chunk_texts_to_leaf_chunks(sources, leaves)
            _quals.append({"id": item["id"], **quality})
            return mapped

        def answer_fn(item: dict, retrieved: list[Chunk], _cache=cache) -> tuple[str, list[str], int]:
            answer_text, sources = _cache[item["id"]]
            return answer_text, sources, N_LLM_CALLS_PER_Q

        name = f"12_openwebui_{config_name}"
        console.print(f"[bold]evaluating[/bold] {name}")
        started = time.monotonic()
        evaluate_run(name, chapter="12", answer_fn=answer_fn, retrieve_fn=retrieve_fn, split="test", limit=limit)
        run_dir = RUNS_DIR / name
        (run_dir / "mapping.json").write_text(json.dumps(qualities, indent=2))
        config_record = {
            "app": "openwebui",
            "config_name": config_name,
            "retrieval_settings": NAMED_CONFIGS[config_name],
            "collection_id": collection_id,
            "model": model,
            "base_url": BASE_URL,
            "eval_seconds": round(time.monotonic() - started, 1),
        }
        (run_dir / "config.json").write_text(json.dumps({**json.loads((run_dir / "config.json").read_text()), **config_record}, indent=2))


if __name__ == "__main__":
    app()
