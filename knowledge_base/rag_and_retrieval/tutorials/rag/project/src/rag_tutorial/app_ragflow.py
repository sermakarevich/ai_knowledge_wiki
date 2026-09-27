"""Chapter 12 (part 3): RAGFlow — optional, time-boxed to ~2 hours.

RAGFlow (Infiniflow, Apache-2.0) is the most feature-rich open-source RAG
engine in our survey (deep document parsing, template chunking, hybrid
multi-recall + fused re-ranking, agent workflows), but it is the heaviest:
documented minimum **16 GB RAM** (Elasticsearch-backed) and **x86-only**
Docker images — under Docker Desktop emulation on this Apple Silicon Mac it
may not run at all. Rules for this module:

- ``just ragflow-up`` / ``just ragflow-down`` manage the stack (cloned at a
  pinned tag into ``data/ragflow/``, gitignored; UI on 8085, API on 9385).
  No ``-slim`` image exists for recent tags (verified 2026-09-09: slim tags
  stop at v0.21.1), so only the full ~9 GB x86-only image is available.
- If it cannot run (RAM, missing arm64 image, …), document precisely what
  failed in the findings note, keep the survey entry, and stop — do not
  exceed ~2 hours.
- If it runs: point it at Ollama (chat + embeddings), create a knowledge
  base (KB) with default chunking, upload the PDFs, and evaluate through its
  HTTP API — rows ``12_ragflow_default`` and ``12_ragflow_tuned``.

RAGFlow's HTTP API surface below follows the ``/api/v1`` conventions
(``/api/v1/datasets``, ``/api/v1/chats/.../completions`` with
``Authorization: Bearer <key>``); exact paths are re-verified against the
pinned tag's API docs/SDK at run time, and any drift is recorded in the
findings note.
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
BASE_URL = os.environ.get("RAGFLOW_URL", "http://localhost:9385")
CORPUS_PDF_DIR = settings.path("data/corpus/pdf")

N_LLM_CALLS_PER_Q = 1


# -- pure helpers (no network): settings builder + response parsers ---------


def build_kb_settings(
    chunk_size: int = 512,
    chunk_overlap: int = 0,
    parser: str = "naive",
    embedding_model: str = "nomic-embed-text",
    rerank_model: str = "",
) -> dict:
    """Knowledge-base creation payload for ``POST /api/v1/datasets``.

    ``parser`` is RAGFlow's chunk-method selector (``"naive"`` = default
    general chunking); ``rerank_model`` empty means the KB's default
    (no extra reranker). Field names re-verified against the pinned tag at
    run time — see the findings note.
    """
    payload: dict = {
        "name": "rag-tutorial-12-papers",
        "chunk_len": chunk_size,
        "chunk_overlap": chunk_overlap,
        "parser_id": parser,
        "embd_id": embedding_model,
    }
    if rerank_model:
        payload["rerank_id"] = rerank_model
    return payload


NAMED_CONFIGS: dict[str, dict] = {
    "default": build_kb_settings(),
    "tuned": build_kb_settings(chunk_size=1024, chunk_overlap=128, rerank_model="cross-encoder/ms-marco-MiniLM-L-6-v2"),
}


def parse_dataset_response(payload: dict) -> str:
    """Extract the dataset id from a ``POST /api/v1/datasets`` response."""
    data = payload.get("data", payload) if isinstance(payload, dict) else payload
    if isinstance(data, dict):
        for key in ("id", "dataset_id", "kb_id"):
            value = data.get(key)
            if isinstance(value, str) and value:
                return value
    raise ValueError(f"no dataset id in response: {str(payload)[:300]}")


def parse_completion_response(payload: dict) -> tuple[str, list[str]]:
    """Return ``(answer, chunk_texts)`` from a chat-completion response.

    Handles RAGFlow's ``{"data": {"answer": ..., "reference": {"chunks":
    [{"content": ...}]}}}`` shape plus bare ``{"answer": ...}`` and
    OpenAI-style ``choices`` payloads. Unknown shapes degrade to
    ``(str(payload), [])``.
    """
    if not isinstance(payload, dict):
        return str(payload), []
    data = payload.get("data", payload)
    if not isinstance(data, dict):
        return str(data), []
    answer = data.get("answer", "")
    if not isinstance(answer, str):
        choices = payload.get("choices", [])
        if choices and isinstance(choices[0], dict):
            answer = str(choices[0].get("message", {}).get("content", ""))
        else:
            answer = json.dumps(data)[:2000]
    chunks: list[str] = []
    reference = data.get("reference", {})
    if isinstance(reference, dict):
        for entry in reference.get("chunks", []) or []:
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


def chunk_texts_to_leaf_chunks(source_texts: list[str], leaves: list[Chunk], k: int = 5) -> tuple[list[Chunk], dict]:
    """Map RAGFlow's reference chunks back to our leaf chunk ids (ch11 mapping)."""
    context = "\n\n".join(source_texts)
    ranked = map_context_to_chunks(context, leaves)
    quality = mapping_quality(context, ranked)
    return [chunk for chunk, _score in ranked[:k]], quality


# -- thin HTTP client (network only past this point) -------------------------


def _client(api_key: str) -> httpx.Client:
    return httpx.Client(base_url=BASE_URL, headers={"Authorization": f"Bearer {api_key}"}, timeout=180.0)


def create_dataset(api_key: str, config_name: str) -> str:
    with _client(api_key) as client:
        resp = client.post("/api/v1/datasets", json=NAMED_CONFIGS[config_name])
        resp.raise_for_status()
        return parse_dataset_response(resp.json())


def upload_document(api_key: str, dataset_id: str, path: Path) -> dict:
    with _client(api_key) as client:
        with path.open("rb") as fh:
            resp = client.post(f"/api/v1/datasets/{dataset_id}/documents", files={"file": (path.name, fh)})
        resp.raise_for_status()
        return resp.json()


def create_chat(api_key: str, dataset_ids: list[str], name: str = "rag-tutorial") -> str:
    with _client(api_key) as client:
        resp = client.post("/api/v1/chats", json={"dataset_ids": dataset_ids, "name": name})
        resp.raise_for_status()
        data = resp.json().get("data", resp.json())
        chat_id = data.get("id", "") if isinstance(data, dict) else ""
        if not chat_id:
            raise ValueError(f"no chat id in response: {str(resp.json())[:300]}")
        return chat_id


def chat_completion(api_key: str, chat_id: str, question: str) -> tuple[str, list[str]]:
    with _client(api_key) as client:
        resp = client.post(f"/api/v1/chats/{chat_id}/completions", json={"question": question, "stream": False})
        resp.raise_for_status()
        return parse_completion_response(resp.json())


# -- CLI ---------------------------------------------------------------------


@app.command()
def upload(config: str = "default") -> None:
    """Create the dataset (KB) and upload the corpus PDFs."""
    api_key = os.environ.get("RAGFLOW_API_KEY", "")
    if not api_key:
        raise typer.BadParameter("RAGFLOW_API_KEY is not set — create it in the RAGFlow UI first")
    if config not in NAMED_CONFIGS:
        raise typer.BadParameter(f"config must be one of {sorted(NAMED_CONFIGS)}")
    dataset_id = create_dataset(api_key, config)
    console.print(f"created dataset {dataset_id}")
    pdfs = sorted(CORPUS_PDF_DIR.glob("*.pdf"))
    for path in pdfs:
        upload_document(api_key, dataset_id, path)
        console.print(f"uploaded {path.name}")
    console.print(f"[green]dataset ready[/green] id={dataset_id}")


@app.command()
def ask(question: str, chat_id: str, k: int = 5) -> None:
    """Ask one question through a RAGFlow chat session; print answer + mapping."""
    api_key = os.environ.get("RAGFLOW_API_KEY", "")
    if not api_key:
        raise typer.BadParameter("RAGFLOW_API_KEY is not set")
    answer, chunks = chat_completion(api_key, chat_id, question)
    console.print(f"[bold]answer:[/bold]\n{answer}\n")
    leaves = build_parent_child_index(load_documents())[0]
    mapped, quality = chunk_texts_to_leaf_chunks(chunks, leaves, k=k)
    console.print(f"mapped chunks: {[c.id for c in mapped]} quality={quality}")


@app.command(name="eval")
def eval_cmd(
    chats: str = "",
    limit: int | None = None,
) -> None:
    """Evaluate RAGFlow chats on the test split (rows ``12_ragflow_*``).

    ``chats`` maps config names to chat-session ids as
    ``default:<chat_id>,tuned:<chat_id>``.
    """
    api_key = os.environ.get("RAGFLOW_API_KEY", "")
    if not api_key:
        raise typer.BadParameter("RAGFLOW_API_KEY is not set")
    mapping = dict(part.split(":", 1) for part in chats.split(",") if part.strip()) if chats else {}
    if not mapping:
        raise typer.BadParameter("pass --chats default:<chat_id>[,tuned:<chat_id>]")
    leaves = build_parent_child_index(load_documents())[0]
    for config_name, chat_id in mapping.items():
        if config_name not in NAMED_CONFIGS:
            raise typer.BadParameter(f"unknown config '{config_name}'; expected one of {sorted(NAMED_CONFIGS)}")
        cache: dict[str, tuple[str, list[str]]] = {}
        qualities: list[dict] = []

        def retrieve_fn(item: dict, _cid=chat_id, _cache=cache, _quals=qualities) -> list[Chunk]:
            answer_text, chunks = chat_completion(api_key, _cid, item["question"])
            _cache[item["id"]] = (answer_text, chunks)
            mapped, quality = chunk_texts_to_leaf_chunks(chunks, leaves)
            _quals.append({"id": item["id"], **quality})
            return mapped

        def answer_fn(item: dict, retrieved: list[Chunk], _cache=cache) -> tuple[str, list[str], int]:
            answer_text, chunks = _cache[item["id"]]
            return answer_text, chunks, N_LLM_CALLS_PER_Q

        name = f"12_ragflow_{config_name}"
        console.print(f"[bold]evaluating[/bold] {name}")
        started = time.monotonic()
        evaluate_run(name, chapter="12", answer_fn=answer_fn, retrieve_fn=retrieve_fn, split="test", limit=limit)
        run_dir = RUNS_DIR / name
        (run_dir / "mapping.json").write_text(json.dumps(qualities, indent=2))
        config_record = {
            "app": "ragflow",
            "config_name": config_name,
            "kb_settings": NAMED_CONFIGS[config_name],
            "chat_id": chat_id,
            "base_url": BASE_URL,
            "eval_seconds": round(time.monotonic() - started, 1),
        }
        (run_dir / "config.json").write_text(json.dumps({**json.loads((run_dir / "config.json").read_text()), **config_record}, indent=2))


if __name__ == "__main__":
    app()
