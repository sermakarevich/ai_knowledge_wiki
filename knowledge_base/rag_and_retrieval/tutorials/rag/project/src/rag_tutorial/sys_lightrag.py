"""Chapter 11 (part 2): LightRAG — graph + vector hybrid retrieval as a system.

LightRAG (Guo et al., arXiv:2410.05779, `lightrag-hku` on PyPI) builds a
knowledge graph (entities + relations extracted by the LLM) over the corpus
at indexing time, then answers in one of five query modes: `naive` (plain
chunk retrieval), `local` (entity-centric), `global` (community summaries for
thematic questions), `hybrid` (local+global) and `mix` (local+global+naive).

Wiring: `LightRAG(working_dir=data/indexes/lightrag,
llm_model_func=ollama_model_complete, llm_model_name="qwen3.8:27b",
llm_model_kwargs={"host": ..., "options": {"num_ctx": 32768,
"temperature": 0}}, embedding_func=EmbeddingFunc(embedding_dim=768,
max_token_size=8192, func=ollama_embed))`. Both callbacks route through
`rag_tutorial.llm` so every LightRAG call is disk-cached and counted.

`lightrag` is imported lazily inside `get_rag()` so this module's pure
helpers (chunk mapping) stay importable without the optional dependency.
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path

import typer
from rich.console import Console

from rag_tutorial.config import settings
from rag_tutorial.corpus import load_papers
from rag_tutorial.evaluate import evaluate_run
from rag_tutorial.golden import load_documents
from rag_tutorial.llm import ollama
from rag_tutorial.prompts import build_messages
from rag_tutorial.retrieval_eval import build_parent_child_index
from rag_tutorial.schema import Chunk

app = typer.Typer(add_completion=False)
console = Console()

RUNS_DIR = settings.path("runs")
LIGHTRAG_RUN_DIR = RUNS_DIR / "11_lightrag"
WORKING_DIR = str(settings.path("data/indexes/lightrag"))
MODES = ("naive", "local", "global", "hybrid", "mix")

CALLS = {"llm": 0, "embed_texts": 0}

_WORD_RE = re.compile(r"\w+")


def _tokens(text: str) -> set[str]:
    return set(_WORD_RE.findall(text.lower()))


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


# -- LightRAG callbacks ------------------------------------------------------------


async def ollama_model_complete(prompt: str, system_prompt: str | None = None, history_messages=None, **kwargs) -> str:
    """LLM callback for LightRAG: fixed model, temperature 0, disk-cached."""
    CALLS["llm"] += 1
    messages: list[dict] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.extend(history_messages or [])
    messages.append({"role": "user", "content": prompt})
    return ollama.chat(messages, model=settings.chat_model, temperature=0.0, num_ctx=32768, max_tokens=1024)


async def ollama_embed(texts: list[str]):
    """Embedding callback for LightRAG: nomic-embed-text, 768 dims, cached."""
    import numpy as np

    CALLS["embed_texts"] += len(texts)
    vectors = ollama.embed(texts, model=settings.embed_model)
    return np.asarray(vectors, dtype=np.float32)


def get_rag():
    """Build the LightRAG instance (lazy `lightrag` import)."""
    import asyncio

    from lightrag import LightRAG
    from lightrag.utils import EmbeddingFunc

    rag = LightRAG(
        working_dir=WORKING_DIR,
        llm_model_func=ollama_model_complete,
        llm_model_name=settings.chat_model,
        llm_model_kwargs={"host": settings.ollama_url, "options": {"num_ctx": 32768, "temperature": 0}},
        embedding_func=EmbeddingFunc(embedding_dim=settings.embed_dim, max_token_size=8192, func=ollama_embed),
    )
    asyncio.run(rag.initialize_storages())
    return rag


# -- chunk mapping -----------------------------------------------------------------


def extract_lightrag_chunks(context: str) -> list[str]:
    """Ordered LightRAG text-chunk contents from the context string.

    With `only_need_context=True` LightRAG returns its retrieved chunks as
    one-JSON-object-per-line inside ```json fences (entries with a `content`
    key; entity/relationship/report blocks have different keys and are
    skipped). Order = LightRAG's own retrieval ranking, which the id mapping
    below preserves. Returns [] when no chunk block parses (plain-text
    context) so callers can fall back to overlap ranking.
    """
    out: list[str] = []
    decoder = json.JSONDecoder()
    for block in re.findall(r"```json(.*?)```", context, re.S):
        i, n = 0, len(block)
        while i < n:
            while i < n and block[i] not in "{[":
                i += 1
            if i >= n:
                break
            try:
                obj, j = decoder.raw_decode(block, i)
            except json.JSONDecodeError:
                i += 1
                continue
            i = j
            items = obj if isinstance(obj, list) else [obj]
            for item in items:
                if isinstance(item, dict) and isinstance(item.get("content"), str):
                    out.append(item["content"])
    return out


def map_context_to_chunks(context: str, chunks: list[Chunk]) -> list[tuple[Chunk, float]]:
    """Map a LightRAG context string back to our leaf chunk ids.

    Score = |chunk words ∩ context words| / |chunk words| (+0.5 bonus when the
    chunk's first 200 normalised chars appear verbatim — the common case when
    LightRAG returns its own chunks, which overlap ours). Ranking is
    order-aware: a leaf contained verbatim in LightRAG's Nth returned chunk
    sorts before one from a later chunk (LightRAG's ranking is the relevance
    signal); leaves contained in no returned chunk backfill by score. Without
    any parseable chunk block this degrades to pure score order. Returns
    (chunk, score) sorted best-first.
    """
    context_text = _normalize(context)
    context_words = _tokens(context)
    lr_chunks = [_normalize(c) for c in extract_lightrag_chunks(context)]
    scored: list[tuple[int, float, Chunk]] = []
    for chunk in chunks:
        words = _tokens(chunk.text)
        if not words:
            continue
        score = len(words & context_words) / len(words)
        probe = _normalize(chunk.text)[:200]
        verbatim = bool(probe) and probe in context_text
        if verbatim:
            score += 0.5
        rank = len(lr_chunks)
        if verbatim:
            for idx, lrc in enumerate(lr_chunks):
                if probe in lrc:
                    rank = idx
                    break
        scored.append((rank, score, chunk))
    scored.sort(key=lambda triple: (triple[0], -triple[1]))
    return [(chunk, score) for _rank, score, chunk in scored]


def mapping_quality(context: str, ranked: list[tuple[Chunk, float]]) -> dict:
    """How well did the mapping work (for the findings note)."""
    top1 = ranked[0][1] if ranked else 0.0
    n_strong = sum(1 for _c, s in ranked[:10] if s >= 0.5)
    return {
        "context_chars": len(context),
        "n_lr_chunks": len(extract_lightrag_chunks(context)),
        "top1_score": round(top1, 4),
        "n_strong_in_top10": n_strong,
    }


# -- shared retrieval ---------------------------------------------------------------


def _short_names() -> dict[str, str]:
    return {paper["id"]: paper["short_name"] for paper in load_papers()}


class LightRAGRetriever:
    """One LightRAG instance + our leaf chunks; retrieval = only_need_context + mapping."""

    def __init__(self, mode: str):
        if mode not in MODES:
            raise ValueError(f"mode must be one of {MODES}")
        from lightrag import QueryParam

        self.mode = mode
        self.rag = get_rag()
        self.QueryParam = QueryParam
        docs = load_documents()
        children, _parents, _c2p = build_parent_child_index(docs)
        self.leaves = children
        self.last_delta = 0
        self.last_quality: dict = {}

    def retrieve(self, question: str, k: int) -> list[Chunk]:
        before = CALLS["llm"]
        param = self.QueryParam(mode=self.mode, only_need_context=True)
        context = self.rag.query(question, param=param)
        self.last_delta = CALLS["llm"] - before
        ranked = map_context_to_chunks(str(context), self.leaves)
        self.last_quality = mapping_quality(str(context), ranked)
        return [chunk for chunk, _score in ranked[:k]]

    def native_answer(self, question: str) -> str:
        param = self.QueryParam(mode=self.mode)
        return str(self.rag.query(question, param=param))


def answer(question: str, retrieved: list[Chunk]) -> tuple[str, list[str]]:
    """Same fixed prompt as every other chapter — scoreboard deltas are the retriever."""
    short_names = _short_names()
    triples = [(short_names.get(c.paper, c.paper), c.section, c.text) for c in retrieved]
    messages = build_messages(question, triples)
    reply = ollama.chat(messages, max_tokens=384)
    contexts = [f"[{short_name}] {text}" for short_name, _section, text in triples]
    return reply, contexts


# -- CLI ----------------------------------------------------------------------------


@app.command()
def index() -> None:
    """Insert the 12 parsed papers; record wall time, LLM calls, graph size."""
    started = time.monotonic()
    CALLS["llm"] = 0
    CALLS["embed_texts"] = 0
    rag = get_rag()
    docs = load_documents()
    papers = load_papers()
    texts = [docs[p["id"]].text for p in papers if p["id"] in docs]
    console.print(f"inserting {len(texts)} papers into {WORKING_DIR} ...")
    rag.insert(texts)
    wall_minutes = (time.monotonic() - started) / 60

    stats = {
        "n_docs": len(texts),
        "doc_chars": sum(len(t) for t in texts),
        "wall_minutes": round(wall_minutes, 2),
        "llm_calls": CALLS["llm"],
        "embed_texts": CALLS["embed_texts"],
        "graph": describe_working_dir(),
    }
    LIGHTRAG_RUN_DIR.mkdir(parents=True, exist_ok=True)
    (LIGHTRAG_RUN_DIR / "index_stats.json").write_text(json.dumps(stats, indent=2))
    console.print(f"[green]indexed[/green] {json.dumps(stats['graph'], indent=2)} in {wall_minutes:.1f} min")


def describe_working_dir() -> dict:
    """Count entities/relations/communities from LightRAG's working dir."""
    info: dict = {}
    base = Path(WORKING_DIR)
    if base.exists():
        info["files"] = {p.name: p.stat().st_size for p in sorted(base.iterdir()) if p.is_file()}
    graphml = base / "graph_chunk_entity_relation.graphml"
    if graphml.exists():
        try:
            import networkx as nx

            graph = nx.read_graphml(graphml)
            info["entities"] = graph.number_of_nodes()
            info["relations"] = graph.number_of_edges()
        except Exception as exc:  # noqa: BLE001 — best effort introspection
            info["graph_error"] = str(exc)[:200]
    for name in ("community_reports.json", "kv_store_community_reports.json"):
        reports = base / name
        if reports.exists():
            try:
                data = json.loads(reports.read_text())
                info["communities"] = len(data) if isinstance(data, (dict, list)) else "present"
                info["communities_file"] = name
            except (json.JSONDecodeError, OSError):
                pass
    return info


@app.command()
def ask(question: str, mode: str = "mix", k: int = 5) -> None:
    """Ask one question: native LightRAG answer + mapped chunk ids."""
    retriever = LightRAGRetriever(mode)
    native = retriever.native_answer(question)
    console.print(f"[bold]LightRAG ({mode}) answer:[/bold]\n{native}\n")
    mapped = retriever.retrieve(question, k)
    console.print(f"mapped chunks: {[c.id for c in mapped]} quality={retriever.last_quality}")


@app.command(name="eval")
def eval_cmd() -> None:
    """Evaluate every query mode on the test split (rows `11_lightrag_<mode>`)."""
    for mode in MODES:
        retriever = LightRAGRetriever(mode)
        qualities: list[dict] = []

        def retrieve_fn(item: dict, _retriever=retriever, _qualities=qualities, k: int = 5) -> list[Chunk]:
            chunks = _retriever.retrieve(item["question"], k)
            _qualities.append({"id": item["id"], **_retriever.last_quality})
            return chunks

        def answer_fn(item: dict, retrieved: list[Chunk], _retriever=retriever) -> tuple[str, list[str], int]:
            reply, contexts = answer(item["question"], retrieved)
            return reply, contexts, 1 + _retriever.last_delta

        console.print(f"[bold]evaluating[/bold] 11_lightrag_{mode}")
        evaluate_run(f"11_lightrag_{mode}", chapter="11", answer_fn=answer_fn, retrieve_fn=retrieve_fn, split="test")
        out = RUNS_DIR / f"11_lightrag_{mode}" / "mapping.json"
        out.write_text(json.dumps(qualities, indent=2))


if __name__ == "__main__":
    app()
