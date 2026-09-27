"""Vector-store benchmark (Chapter 06).

Builds the *same* chunk set (child chunks of the parent_child index, embedded
with nomic-embed-text) and the *same* 27 golden queries into five stores —
Chroma, FAISS, LanceDB, PgVector and Qdrant — then measures, per store:

- **build time** (ingest of ~2k 768-dim vectors + payload),
- **search latency** P50 / P95 and QPS over the golden queries (dense, K=5),
- **recall@5** so retrieval quality is provably identical across stores, and
- **on-disk size**.

The point of the chapter is that quality is a property of the *embedding
model and the index math*, not of the storage backend — the same vectors must
return the same neighbours everywhere, and only latency/size/ops differ.

Qdrant is driven through its client's pure-dense `search` path (not the hybrid
path that mixes in BM25), so every store is compared on the same dense top-k
query. All five stores are local on this machine — no cloud, no external
service — and Chroma, FAISS and LanceDB need no server at all.

Run: `uv run python -m rag_tutorial.store_bench` → `runs/06_store_bench.json`.
"""

from __future__ import annotations

import json
import statistics
import time
from pathlib import Path

import numpy as np
import typer
from rich.console import Console
from rich.table import Table

from rag_tutorial.config import settings
from rag_tutorial.evaluate import retrieval_metrics
from rag_tutorial.golden import load_qa
from rag_tutorial.llm import Ollama
from rag_tutorial.retrieval_eval import build_parent_child_index
from rag_tutorial.golden import load_documents
from rag_tutorial.schema import Chunk
from rag_tutorial.stores import ChromaStore, FaissStore, LanceDBStore, PgVectorStore

app = typer.Typer(add_completion=False)
console = Console()

RUNS_DIR = settings.path("runs")
OUT_PATH = RUNS_DIR / "06_store_bench.json"
EMBED_MODEL = "nomic-embed-text"
K = 5
STORE_ROOT = settings.path("data/stores/06_bench")


def _unit_normalize(v: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(v, axis=-1, keepdims=True)
    return v / np.where(n == 0, 1.0, n)


def _chunks_and_vectors() -> tuple[list[Chunk], list[str], np.ndarray]:
    documents = load_documents()
    children, _, _ = build_parent_child_index(documents)
    client = Ollama()
    vectors = np.asarray(client.embed_documents([c.text for c in children], model=EMBED_MODEL), dtype=float)
    # Unit-normalise so that cosine (Chroma/Qdrant/PgVector), inner-product
    # (FAISS-IP) and L2 (LanceDB) all give IDENTICAL top-k orderings — this is
    # the whole point of the bench: quality is identical across stores, only
    # latency/size/ops differ.
    vectors = _unit_normalize(vectors)
    return children, [c.id for c in children], vectors


def _embed_queries(questions: list[str]) -> np.ndarray:
    client = Ollama()
    mat = np.asarray([client.embed_query(q, model=EMBED_MODEL) for q in questions], dtype=float)
    return _unit_normalize(mat)


def _on_disk_bytes(store) -> int | None:
    for attr in ("on_disk_bytes", "_dir_bytes"):
        fn = getattr(store, attr, None)
        if callable(fn):
            return int(fn())
    return None


def _percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    values = sorted(values)
    if pct == 100:
        return values[-1]
    if pct == 0:
        return values[0]
    rank = (len(values) - 1) * (pct / 100.0)
    lower = int(rank)
    upper = min(lower + 1, len(values) - 1)
    frac = rank - lower
    return values[lower] + (values[upper] - values[lower]) * frac


def _recall_over(q_vecs, search_fn, questions, evidence, k: int) -> float:
    per_q = []
    for q, ev in zip(questions, evidence):
        v = q_vecs[len(per_q)]
        ranked = search_fn(v, k)
        m = retrieval_metrics(ranked, ev, ks=(k,))
        per_q.append(m["recall@" + str(k)])
    return round(statistics.fmean(per_q), 4)


class _LocalStore:
    """Wraps one of Chroma / FAISS / LanceDB / PgVector behind a uniform API."""

    def __init__(self, name: str, store) -> None:
        self.name = name
        self.store = store

    def add(self, chunks, ids, vectors: np.ndarray) -> float:
        if hasattr(self.store, "reset"):
            self.store.reset()  # clean slate so we measure a from-scratch build
        t0 = time.perf_counter()
        self.store.add(chunks, [v.tolist() for v in vectors])
        if hasattr(self.store, "save"):
            self.store.save()  # FAISS keeps rows in memory; persist before measuring disk
        return time.perf_counter() - t0

    def search(self, vec: np.ndarray, k: int) -> list[Chunk]:
        # .query() returns list[(Chunk, score)] — unwrap to a plain Chunk list
        # (the shape retrieval_metrics expects).
        return [chunk for chunk, _score in self.store.query([float(x) for x in vec], k)]

    def on_disk_bytes(self) -> int | None:
        return _on_disk_bytes(self.store)

    def close(self) -> None:
        for attr in ("close", "close_database", "close"):
            fn = getattr(self.store, attr, None)
            if callable(fn):
                try:
                    fn()
                except Exception:
                    pass
                return


class _QdrantStore:
    """Dense top-k search via the Qdrant client (the hybrid/BM25 path is
    deliberately avoided so every store is compared on the same dense query)."""

    COLLECTION = "ch06_store_bench"

    def __init__(self, name: str) -> None:
        from qdrant_client import QdrantClient

        self.name = name
        self.client = QdrantClient(url=settings.qdrant_url, timeout=30)
        if self.client.collection_exists(self.COLLECTION):
            self.client.delete_collection(self.COLLECTION)

    def add(self, chunks, ids, vectors: np.ndarray) -> float:
        from qdrant_client.models import Distance, PointStruct, VectorParams

        self.client.create_collection(
            collection_name=self.COLLECTION,
            vectors_config=VectorParams(size=vectors.shape[1], distance=Distance.COSINE),
        )
        points = [
            PointStruct(id=i, vector=[float(x) for x in vectors[i]],
                        payload={"chunk_id": chunks[i].id, "paper": chunks[i].paper,
                                "section": chunks[i].section, "chunk_text": chunks[i].text})
            for i in range(len(ids))
        ]
        t0 = time.perf_counter()
        for i in range(0, len(points), 64):
            self.client.upsert(self.COLLECTION, points=points[i:i + 64], wait=True)
        return time.perf_counter() - t0

    def search(self, vec: np.ndarray, k: int) -> list[Chunk]:
        res = self.client.query_points(
            collection_name=self.COLLECTION,
            query=[float(x) for x in vec],
            limit=k,
            with_payload=True,
        )
        return [
            Chunk(id=p.payload["chunk_id"], paper=p.payload["paper"], section=p.payload["section"],
                  text=p.payload["chunk_text"], start=0, end=0)
            for p in res.points
        ]

    def on_disk_bytes(self) -> None:
        # Qdrant writes to its own volume; not cheaply measurable here.
        return None

    def close(self) -> None:
        try:
            if self.client.collection_exists(self.COLLECTION):
                self.client.delete_collection(self.COLLECTION)
        except Exception:
            pass


def _make_adapter(name: str):
    # NOTE: every store takes `collection_name` first; `persist_dir`/`kind`/`dim`
    # /`dsn` are keyword args. (Faiss's 2nd positional arg is `kind`, not a path.)
    if name == "chroma":
        return _LocalStore(name, ChromaStore("ch06_bench", persist_dir=STORE_ROOT / "chroma"))
    if name == "faiss":
        return _LocalStore(name, FaissStore("ch06_bench", kind="flat", persist_dir=STORE_ROOT / "faiss"))
    if name == "lancedb":
        return _LocalStore(name, LanceDBStore("ch06_bench", persist_dir=STORE_ROOT / "lancedb"))
    if name == "pgvector":
        return _LocalStore(name, PgVectorStore("ch06_bench", dim=768,
                                               dsn="postgres://postgres:postgres@localhost:5434/rag"))
    if name == "qdrant":
        return _QdrantStore(name)
    raise ValueError(f"unknown store: {name}")


@app.command()
def run(
    stores: str = typer.Option("chroma,faiss,lancedb,pgvector,qdrant", help="comma list"),
    k: int = typer.Option(K, min=1, max=50),
    rounds: int = typer.Option(3, help="search rounds for latency (excludes build)"),
) -> None:
    names = [s.strip() for s in stores.split(",") if s.strip()]
    questions, evidence = _load_golden()
    chunks, ids, vectors = _chunks_and_vectors()
    q_vecs = _embed_queries(questions)
    console.print(f"{len(chunks)} chunks x {vectors.shape[1]}d, {len(questions)} queries, K={k}")

    results = {"k": k, "n_chunks": len(chunks), "n_queries": len(questions), "stores": {}}
    for name in names:
        t_total = time.perf_counter()
        store = _make_adapter(name)
        try:
            build_s = store.add(chunks, ids, vectors)
            # warmup
            store.search(q_vecs[0], k)
            latencies = []
            for _ in range(rounds):
                for v in q_vecs:
                    t0 = time.perf_counter()
                    store.search(v, k)
                    latencies.append(time.perf_counter() - t0)
            recall = _recall_over(q_vecs, store.search, questions, evidence, k)
            lat_s = sorted(latencies)
            p50 = _percentile(lat_s, 50) * 1000
            p95 = _percentile(lat_s, 95) * 1000
            qps = round(len(q_vecs) * rounds / max(sum(latencies), 1e-9), 1)
            row = {
                "build_seconds": round(build_s, 3),
                "p50_ms": round(p50, 2),
                "p95_ms": round(p95, 2),
                "qps": qps,
                "recall@5": recall,
                "on_disk_bytes": store.on_disk_bytes(),
            }
            results["stores"][name] = row
            console.print(f"[green]{name}[/green]: build={build_s:.2f}s p50={p50:.1f}ms p95={p95:.1f}ms qps={qps} recall5={recall}")
        except Exception as e:
            results["stores"][name] = {"error": f"{type(e).__name__}: {e}"}
            console.print(f"[red]{name}[/red] ERROR: {e!r}")
        finally:
            store.close()

    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(results, indent=2) + "\n")
    console.print(f"\nwrote [bold]{OUT_PATH}[/bold]")
    _print_table(results)


def _load_golden() -> tuple[list[str], list[list[dict]]]:
    items = [q for q in load_qa() if q["split"] == "test" and q["evidence"]]
    return [q["question"] for q in items], [q["evidence"] for q in items]


def _print_table(results: dict) -> None:
    table = Table(title="Vector store benchmark (dense K=5, same vectors)")
    for col in ("store", "build_s", "p50_ms", "p95_ms", "qps", "recall@5", "on_disk"):
        table.add_column(col)
    for name, row in results["stores"].items():
        if "error" in row:
            table.add_row(name, "—", "—", "—", "—", "—", f"ERROR {row['error'][:30]}")
            continue
        on_disk = row.get("on_disk_bytes")
        table.add_row(
            name, f"{row['build_seconds']:.2f}", f"{row['p50_ms']:.1f}", f"{row['p95_ms']:.1f}",
            str(row["qps"]), f"{row['recall@5']:.3f}",
            f"{on_disk/1024/1024:.2f} MB" if on_disk else "n/a",
        )
    console.print(table)


if __name__ == "__main__":
    app()
