"""A disk-cached client for the Ollama server: chat and embeddings.

Every request Ollama runs on the `rtx` GPU box is expensive in *wall time* (10-60s
over an SSH tunnel, more if the model has to load) even though it costs nothing in
money. So every call in this tutorial goes through this module, which hashes the
exact request into a cache key and writes the response to disk before returning
it. Re-running a chapter, a test, or the whole evaluation a second time costs
zero LLM calls as long as the inputs are unchanged — that is what makes this
tutorial reproducible and free to re-run.

Cache key = sha256 of a canonical JSON encoding of
`(endpoint, model, options, input)` — for chat, `input` is the message list (plus
the JSON schema, if any); for embeddings, `input` is a *single* text, so that
re-chunking a document only re-embeds the chunks that actually changed.

Cache layout:
    data/cache/chat/<key[:2]>/<key>.json
    data/cache/embed/<model>/<key[:2]>/<key>.json

Each cache entry stores the request, the response, and Ollama's `usage` numbers
(`prompt_eval_count`, `eval_count`, `total_duration`) so `cache_stats()` can
report tokens and time saved by the cache.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from pathlib import Path

import httpx
import tiktoken
import typer
from rich.console import Console
from rich.table import Table

from rag_tutorial.config import settings

_EMBED_BATCH_SIZE = 32

# Transient network failures we retry: the Ollama server sits behind an SSH
# tunnel, and a long batch will occasionally see one dropped connection.
_TRANSIENT = (httpx.ConnectError, httpx.ReadTimeout, httpx.ReadError, httpx.RemoteProtocolError)

# Embedding models expect different task-instruction prefixes (or none) on the
# raw text before embedding. The table is keyed by (model, side):
# - "document" is applied when indexing passages, "query" when embedding a
#   search question, and a missing side means "no prefix" for that side.
# Sources: each model's Ollama library page / Hugging Face card (see
# specs/research/models_eval_papers.md Part 1).
_EMBED_PREFIXES: dict[str, dict[str, str]] = {
    "nomic-embed-text": {"document": "search_document: ", "query": "search_query: "},
    # HF card: query prompt "Represent this sentence for searching relevant
    # passages: {sentence}"; documents have no prefix.
    "mxbai-embed-large": {"document": "", "query": "Represent this sentence for searching relevant passages: "},
    # HF card: query "task: search result | query: {content}", document
    # "title: {title} | text: {content}" (use "none" when there is no title).
    "embeddinggemma": {"document": "title: none | text: ", "query": "task: search result | query: "},
    # bge-m3, snowflake-arctic-embed2, qwen3-embedding, all-minilm: no
    # instruction prefix documented — entries omitted (= no prefix).
}

_encoding = tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str) -> int:
    """Approximate token count using tiktoken's `cl100k_base` encoding.

    This is *not* the real tokenizer for any Ollama model (they use their own
    SentencePiece/BPE vocabularies) — it is a fast, dependency-light stand-in
    good enough for chunk-size budgeting and reporting.
    """
    return len(_encoding.encode(text))


def _canonical_json(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _cache_key(endpoint: str, model: str, options: dict, payload_input) -> str:
    blob = _canonical_json({"endpoint": endpoint, "model": model, "options": options, "input": payload_input})
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


@dataclass
class Stats:
    hits: int = 0
    misses: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    seconds: float = 0.0

    def as_dict(self) -> dict:
        return {
            "hits": self.hits,
            "misses": self.misses,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "seconds": round(self.seconds, 2),
        }


class OllamaError(RuntimeError):
    pass


class Ollama:
    """Cached client for chat and embeddings against a running Ollama server."""

    def __init__(self, base_url: str | None = None, cache_dir: str | Path | None = None):
        self.base_url = base_url or settings.ollama_url
        self.cache_dir = settings.path(cache_dir or settings.cache_dir)
        self.stats = Stats()

    # -- HTTP -----------------------------------------------------------------

    def _post(self, path: str, payload: dict, attempts: int = 3) -> dict:
        last_exc: Exception | None = None
        for attempt in range(1, attempts + 1):
            try:
                response = httpx.post(f"{self.base_url}{path}", json=payload, timeout=180)
                if response.status_code >= 500:
                    raise OllamaError(f"{path} returned HTTP {response.status_code}: {response.text[:200]}")
                response.raise_for_status()
                return response.json()
            except (*_TRANSIENT, OllamaError) as exc:
                last_exc = exc
                if attempt == attempts:
                    break
                time.sleep(2**attempt)
        raise OllamaError(
            f"Could not reach Ollama at {self.base_url}{path} after {attempts} attempts ({last_exc}). "
            "Is the SSH tunnel to rtx up? Try `just tunnel`."
        ) from last_exc

    # -- cache -----------------------------------------------------------------

    def _cache_path(self, kind: str, key: str, model: str | None = None) -> Path:
        if kind == "embed":
            return self.cache_dir / "embed" / model / key[:2] / f"{key}.json"
        return self.cache_dir / kind / key[:2] / f"{key}.json"

    def _read_cache(self, path: Path) -> dict | None:
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text())
        except (json.JSONDecodeError, OSError):
            return None

    def _write_cache(self, path: Path, entry: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(entry, indent=2, sort_keys=True))

    # -- chat -----------------------------------------------------------------

    def chat(
        self,
        messages: list[dict],
        *,
        model: str | None = None,
        temperature: float = 0.0,
        seed: int = 42,
        num_ctx: int = 16384,
        max_tokens: int = 1024,
        json_schema: dict | None = None,
    ) -> str:
        """Send a chat request and return the assistant's reply text, via the disk cache."""
        model = model or settings.chat_model
        options = {"temperature": temperature, "seed": seed, "num_ctx": num_ctx, "num_predict": max_tokens}
        cache_input = {"messages": messages, "schema": json_schema, "think": False}
        key = _cache_key("/api/chat", model, options, cache_input)
        path = self._cache_path("chat", key)

        cached = self._read_cache(path)
        if cached is not None:
            self.stats.hits += 1
            return cached["response"]

        # qwen3.8:27b is a "thinking" model: without think=False its reasoning
        # tokens are drawn from the same num_predict budget as the answer, so a
        # small max_tokens can produce an empty content field.
        payload = {"model": model, "messages": messages, "stream": False, "think": False, "options": options}
        if json_schema is not None:
            payload["format"] = json_schema

        start = time.monotonic()
        data = self._post("/api/chat", payload)
        elapsed = time.monotonic() - start

        reply = data["message"]["content"]
        usage = {
            "prompt_eval_count": data.get("prompt_eval_count"),
            "eval_count": data.get("eval_count"),
            "total_duration": data.get("total_duration"),
        }
        self.stats.misses += 1
        self.stats.prompt_tokens += usage["prompt_eval_count"] or 0
        self.stats.completion_tokens += usage["eval_count"] or 0
        self.stats.seconds += elapsed

        self._write_cache(path, {"request": {"model": model, "options": options, "input": cache_input}, "response": reply, "usage": usage})
        return reply

    # -- embeddings -------------------------------------------------------------

    def _prefix_for(self, model: str, kind: str) -> str:
        return _EMBED_PREFIXES.get(model, {}).get(kind, "")

    def embed(self, texts: list[str], *, model: str | None = None, prefix: str = "") -> list[list[float]]:
        """Embed a list of texts, caching one entry per (model, prefixed text).

        Caching per text (not per batch) means re-chunking a document only pays
        for the chunks whose text actually changed.
        """
        model = model or settings.embed_model
        options = {"truncate": True}

        prefixed = [f"{prefix}{t}" for t in texts]
        keys = [_cache_key("/api/embed", model, options, t) for t in prefixed]
        paths = [self._cache_path("embed", k, model=model) for k in keys]

        results: list[list[float] | None] = [None] * len(texts)
        to_fetch: list[int] = []
        for i, path in enumerate(paths):
            cached = self._read_cache(path)
            if cached is not None:
                self.stats.hits += 1
                results[i] = cached["response"]
            else:
                to_fetch.append(i)
                self.stats.misses += 1

        for start_idx in range(0, len(to_fetch), _EMBED_BATCH_SIZE):
            batch_indices = to_fetch[start_idx : start_idx + _EMBED_BATCH_SIZE]
            batch_texts = [prefixed[i] for i in batch_indices]
            payload = {"model": model, "input": batch_texts, "truncate": True}

            start = time.monotonic()
            data = self._post("/api/embed", payload)
            elapsed = time.monotonic() - start
            self.stats.seconds += elapsed

            vectors = data["embeddings"]
            usage = {"prompt_eval_count": data.get("prompt_eval_count"), "total_duration": data.get("total_duration")}
            per_text_duration = (usage["total_duration"] or 0) // max(len(batch_texts), 1)
            for i, vector in zip(batch_indices, vectors):
                results[i] = vector
                entry = {
                    "request": {"model": model, "options": options, "input": prefixed[i]},
                    "response": vector,
                    "usage": {**usage, "total_duration": per_text_duration},
                }
                self._write_cache(paths[i], entry)

        return results  # type: ignore[return-value]

    def embed_documents(self, texts: list[str], *, model: str | None = None) -> list[list[float]]:
        """Embed passages meant to be *searched* (the document side of retrieval)."""
        model = model or settings.embed_model
        return self.embed(texts, model=model, prefix=self._prefix_for(model, "document"))

    def embed_query(self, text: str, *, model: str | None = None) -> list[float]:
        """Embed a search query, adding the model's query-side prefix if it needs one."""
        model = model or settings.embed_model
        return self.embed([text], model=model, prefix=self._prefix_for(model, "query"))[0]


ollama = Ollama()


def cache_stats() -> dict:
    """Summarize the on-disk cache: number of entries and total size per kind."""
    stats = {}
    for kind_dir in ["chat", "embed"]:
        base = settings.path(settings.cache_dir) / kind_dir
        if not base.exists():
            stats[kind_dir] = {"entries": 0, "bytes": 0}
            continue
        files = list(base.rglob("*.json"))
        stats[kind_dir] = {"entries": len(files), "bytes": sum(f.stat().st_size for f in files)}
    return stats


app = typer.Typer(add_completion=False)


@app.command(name="cache-stats")
def cache_stats_cmd() -> None:
    """Print the on-disk cache size (entries, bytes) per kind."""
    console = Console()
    table = Table(title="rag_tutorial cache")
    table.add_column("kind")
    table.add_column("entries", justify="right")
    table.add_column("bytes", justify="right")
    for kind, info in cache_stats().items():
        table.add_row(kind, str(info["entries"]), str(info["bytes"]))
    console.print(table)


if __name__ == "__main__":
    app()
