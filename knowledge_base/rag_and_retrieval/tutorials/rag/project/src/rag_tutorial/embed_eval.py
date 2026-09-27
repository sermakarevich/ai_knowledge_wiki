"""Chapter 06: embedding model comparison, Matryoshka truncation, Qdrant
quantization, and an HNSW parameter sweep — all on the *same* chunks as
chapter 05 (parent_child, child 160/32 tokens), so any scoreboard difference
is attributable to the embedding model / index parameter alone.

Four sub-commands:

  models       Retrieval-only comparison of six embedding models (7 models
               total including the nomic baseline): dim, size, prefixes,
               throughput (chunks/s through Ollama), and hit@5/recall@5/MRR/
               nDCG@10 over the test split. Writes `runs/06_embedding_models.json`
               and a bar chart `runs/06_embedding_models.png`.

  matryoshka   For nomic-embed-text (768 dim, Matryoshka-capable): truncate the
               cached vectors to 512/256/128 dims, re-normalise, and measure
               the same retrieval metrics per dim. → `runs/06_matryoshka.json`.

  quant        In Qdrant: scalar int8, product (PQ x64), and binary
               quantization — retrieval-only recall vs the float baseline,
               collection RAM from Qdrant's collection info.
               → `runs/06_quant.json`.

  hnsw         HNSW parameter sweep: m ∈ {8,16,32}, ef_construct ∈ {100,200},
               search ef ∈ {16,64,256}; report recall@10 vs exact brute-force
               (numpy) and query latency. → `runs/06_hnsw.json`.

  all          Run all four.

No chat model calls in any command; embeddings are disk-cached by `Ollama` so
a re-run costs zero GPU time.
"""

from __future__ import annotations

import json
import statistics
import time
from functools import lru_cache
from pathlib import Path

import httpx
import numpy as np
import typer
from rich.console import Console
from rich.table import Table

from rag_tutorial.config import settings
from rag_tutorial.evaluate import retrieval_metrics
from rag_tutorial.golden import load_qa
from rag_tutorial.llm import _EMBED_PREFIXES, ollama
from rag_tutorial.retrieval_eval import build_parent_child_index
from rag_tutorial.golden import load_documents
from rag_tutorial.schema import Chunk

app = typer.Typer(add_completion=False)
console = Console()

RUNS_DIR = settings.path("runs")

# ---------------------------------------------------------------------------
# Embedding model list
# ---------------------------------------------------------------------------
# Bare names: they key both the `_EMBED_PREFIXES` table in llm.py (which is
# documented as the bare names) and the embed-disk-cache from chapter 05,
# which cached nomic under `"nomic-embed-text"`. Ollama itself is called with
# the *tagged* name resolved by `_resolve_model` — see its docstring.
EMBED_MODELS = [
    "nomic-embed-text",
    "mxbai-embed-large",
    "embeddinggemma",
    "bge-m3",
    "snowflake-arctic-embed2",
    "qwen3-embedding",
    "all-minilm",
]

K = 5
MATRYOSHKA_DIMS = (512, 256, 128)
HNSW_M = (8, 16, 32)
HNSW_EF_CONSTRUCT = (100, 200)
HNSW_EF_SEARCH = (16, 64, 256)

# ---------------------------------------------------------------------------
# Shared: build chunks and cached embeddings
# ---------------------------------------------------------------------------


def _build_chunks() -> list[Chunk]:
    documents = load_documents()
    children, _, _ = build_parent_child_index(documents)
    return children


def _embed_chunks(children: list[Chunk], model: str) -> tuple[np.ndarray, float]:
    """Return (embedding matrix, elapsed seconds) — hits the Ollama disk cache
    if previously computed, so `elapsed` is meaningful only for the first run."""
    start = time.monotonic()
    raw = ollama.embed_documents([c.text for c in children], model=model)
    elapsed = time.monotonic() - start
    return np.asarray(raw, dtype=float), elapsed


def _embed_queries(questions: list[str], model: str) -> np.ndarray:
    return np.asarray([ollama.embed_query(q, model=model) for q in questions], dtype=float)


def _unit_normalize(v: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(v, axis=-1, keepdims=True)
    return v / np.where(n == 0, 1.0, n)


def _test_items() -> list[dict]:
    return [item for item in load_qa() if item["split"] == "test" and item.get("evidence")]


# ---------------------------------------------------------------------------
# models
# ---------------------------------------------------------------------------


@lru_cache(maxsize=1)
def _ollama_models() -> dict[str, dict]:
    try:
        data = httpx.get(f"{settings.ollama_url}/api/tags", timeout=10).json()
        return {m["name"]: m for m in data.get("models", [])}
    except Exception:
        return {}


def _resolve_model(bare: str) -> str:
    """Map a bare model name to the exact name Ollama's `/api/embed` accepts.

    Ollama 0.32.12's `/api/embed` rejects bare names for models stored under a
    version tag (`mxbai-embed-large` → 404, `mxbai-embed-large:335m` → 200).
    `nomic-embed-text` is stored as `:latest` yet still accepts the bare
    name — and the chapter-05 embed cache for it is keyed bare — so when a
    `data/cache/embed/<bare>/` directory with entries already exists we keep
    the bare name (reusing that cache), otherwise we prefer the tagged name
    from `/api/tags`.
    """
    cache_dir = Path(settings.cache_dir) / "embed" / bare
    if cache_dir.is_dir() and any(cache_dir.iterdir()):
        return bare
    models = _ollama_models()
    if bare in models:
        return bare
    for name in models:
        if name.startswith(bare + ":"):
            return name
    return bare


def _model_info(bare: str) -> dict:
    """Pull model size from Ollama's /api/tags endpoint (via bare name)."""
    m = _resolve_model(bare)
    info = _ollama_models().get(m)
    if info is None:
        return {"size_bytes": None, "size_mb": None, "params": None}
    size_bytes = info.get("size", 0)
    params = info.get("details", {}).get("parameter_size", "")
    return {"size_bytes": size_bytes, "size_mb": round(size_bytes / (1024 * 1024), 0), "params": params}


def _retrieval_only(
    children: list[Chunk],
    child_vecs: np.ndarray,
    query_vecs: np.ndarray,
    items: list[dict],
) -> dict:
    """Brute-force top-5 nearest (numpy dot product) → retrieval_metrics."""
    child_mat = _unit_normalize(child_vecs)
    q_mat = _unit_normalize(query_vecs)

    per_item = []
    for qi, item in enumerate(items):
        sims = q_mat[qi] @ child_mat.T
        top5_idx = np.argpartition(sims, -K)[-K:]
        top5_idx = top5_idx[np.argsort(sims[top5_idx])[::-1]]
        retrieved = [children[i] for i in top5_idx]
        per_item.append(retrieval_metrics(retrieved, item["evidence"], ks=(5, 10), ndcg_ks=(5, 10)))

    def _mean(key: str) -> float:
        return statistics.fmean(r[key] for r in per_item) if per_item else 0.0

    return {
        "n_questions": len(per_item),
        "hit@5": round(_mean("hit@5"), 4),
        "recall@5": round(_mean("recall@5"), 4),
        "mrr": round(_mean("mrr"), 4),
        "ndcg@5": round(_mean("ndcg@5"), 4),
        "ndcg@10": round(_mean("ndcg@10"), 4),
    }


def cmd_models() -> None:
    items = _test_items()
    children = _build_chunks()
    print(f"[bold]{len(children)}[/bold] chunks, [bold]{len(items)}[/bold] test questions")

    results: list[dict] = []
    for bare in EMBED_MODELS:
        model = _resolve_model(bare)
        console.print(f"  [dim]embedding[/dim] {model} ...")
        child_vecs, embed_secs = _embed_chunks(children, model)
        dim = child_vecs.shape[1]
        q_vecs = _embed_queries([it["question"] for it in items], model)
        metrics = _retrieval_only(children, child_vecs, q_vecs, items)
        info = _model_info(bare)
        prefix_doc = _EMBED_PREFIXES.get(bare, {}).get("document", "")
        prefix_query = _EMBED_PREFIXES.get(bare, {}).get("query", "")
        row = {
            "model": model,
            "dim": dim,
            "size_mb": info["size_mb"],
            "params": info["params"],
            "prefix_doc": prefix_doc or None,
            "prefix_query": prefix_query or None,
            "embed_seconds": round(embed_secs, 2),
            "chunks_per_sec": round(len(children) / embed_secs, 1) if embed_secs > 0 else None,
            **{k: v for k, v in metrics.items() if k != "n_questions"},
            "n_questions": metrics["n_questions"],
        }
        results.append(row)
        console.print(f"    dim={dim}  recall@5={row['recall@5']}  mrr={row['mrr']}")

    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RUNS_DIR / "06_embedding_models.json"
    out_path.write_text(json.dumps(results, indent=2))
    console.print(f"[green]wrote[/green] {out_path}")
    _plot_models(results)


def _plot_models(rows: list[dict]) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    labels = [r["model"].replace("-", "\n", 1) for r in rows]
    recalls = [r["recall@5"] for r in rows]
    mrrs = [r["mrr"] for r in rows]

    fig, ax = plt.subplots(figsize=(8, 4))
    x = range(len(rows))
    bars1 = ax.bar([xi - 0.18 for xi in x], recalls, width=0.36, label="recall@5", color="#4472C4")
    bars2 = ax.bar([xi + 0.18 for xi in x], mrrs, width=0.36, label="mrr", color="#ED7D31")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, fontsize=8, rotation=20)
    ax.set_ylabel("score")
    ax.set_title("Chapter 06: embedding model retrieval quality")
    ax.legend()
    fig.tight_layout()
    out = RUNS_DIR / "06_embedding_models.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    console.print(f"[green]wrote[/green] {out}")


# ---------------------------------------------------------------------------
# matryoshka
# ---------------------------------------------------------------------------


def cmd_matryoshka() -> None:
    """Truncate nomic-embed-text vectors to 512/256/128 dims, re-normalise,
    and measure recall@5 / MRR / nDCG@10 per dim."""
    model = "nomic-embed-text"
    items = _test_items()
    children = _build_chunks()
    full_vecs = np.asarray(ollama.embed_documents([c.text for c in children], model=model), dtype=float)
    full_q_vecs = np.asarray([ollama.embed_query(it["question"], model=model) for it in items], dtype=float)

    dims_to_test = (full_vecs.shape[1],) + MATRYOSHKA_DIMS
    console.print(f"[bold]full dim[/bold] = {full_vecs.shape[1]}, testing {list(dims_to_test)}")

    results = []
    for dim in dims_to_test:
        cv = full_vecs[:, :dim].copy()
        qv = full_q_vecs[:, :dim].copy()
        cv = _unit_normalize(cv)
        qv = _unit_normalize(qv)
        metrics = _retrieval_only(children, cv, qv, items)
        row = {"dim": dim, **metrics}
        results.append(row)
        console.print(f"  dim={dim:<5} recall@5={row['recall@5']}  mrr={row['mrr']}  ndcg@10={row['ndcg@10']}")

    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RUNS_DIR / "06_matryoshka.json"
    out_path.write_text(json.dumps({"model": model, "results": results}, indent=2))
    console.print(f"[green]wrote[/green] {out_path}")


# ---------------------------------------------------------------------------
# quant
# ---------------------------------------------------------------------------


def _qdrant_client():
    from qdrant_client import QdrantClient

    return QdrantClient(url=settings.qdrant_url)


def _ram_mb(n_points: int, dim: int, scheme: str) -> float:
    """Analytic estimated RAM for the vector store (no per-collection API in Qdrant 1.19).

    Memory is dominated by the vector payload itself (HNSW links add a small
    overhead on top); this is what `quant` exists to reduce.
    """
    n = n_points
    if scheme == "float":
        nbytes = n * dim * 4  # float32
    elif scheme == "int8":
        nbytes = n * dim * 1  # one byte per dim + (dim//2) scale offsets, negligible
    elif scheme == "pq_x64":
        # one 8-bit sub-quant code per 64 dims
        nbytes = n * (dim + 63) // 64
    elif scheme == "binary":
        nbytes = (n * dim + 7) // 8
    else:
        raise ValueError(f"unknown scheme {scheme!r}")
    return round(nbytes / (1024 * 1024), 3)


def _recall_in_qdrant(client, collection: str, q_vecs: np.ndarray, children: list[Chunk], items: list[dict], k: int = 5) -> float:
    from qdrant_client import models as m

    per_q = []
    for qi, item in enumerate(items):
        res = client.query_points(collection, query=q_vecs[qi].tolist(), limit=k, with_payload=True, using="dense")
        retrieved = []
        for pt in res.points:
            p = pt.payload
            retrieved.append(
                Chunk(id=p["chunk_id"], paper=p["paper"], section=p["section"], text=p["text"], start=p["start"], end=p["end"])
            )
        per_q.append(retrieval_metrics(retrieved, item["evidence"], ks=(k,))["recall@" + str(k)])
    return round(statistics.fmean(per_q), 4)


def cmd_quant() -> None:
    from qdrant_client import models as m

    items = _test_items()
    children = _build_chunks()
    model = "nomic-embed-text"
    raw_vecs = np.asarray(ollama.embed_documents([c.text for c in children], model=model), dtype=float)
    q_vecs = np.asarray([ollama.embed_query(it["question"], model=model) for it in items], dtype=float)
    dim = raw_vecs.shape[1]
    client = _qdrant_client()

    COL = "ch06_quant_bench"
    if client.collection_exists(COL):
        client.delete_collection(COL)

    # --- float baseline ------------------------------------------------------
    client.create_collection(
        COL, vectors_config={"dense": m.VectorParams(size=dim, distance=m.Distance.COSINE)}
    )
    points = [
        m.PointStruct(
            id=int(c.id, 16),
            vector={"dense": raw_vecs[i].tolist()},
            payload={"chunk_id": c.id, "paper": c.paper, "section": c.section, "text": c.text, "start": c.start, "end": c.end},
        )
        for i, c in enumerate(children)
    ]
    client.upsert(COL, points=points, wait=True)
    time.sleep(0.3)
    float_recall = _recall_in_qdrant(client, COL, q_vecs, children, items)
    console.print(f"  float:   recall@5={float_recall}  ram≈{_ram_mb(len(children), dim, 'float')}MB (analytic)")

    # --- scalar quant (int8) -------------------------------------------------
    client.delete_collection(COL)
    client.create_collection(
        COL,
        vectors_config={"dense": m.VectorParams(size=dim, distance=m.Distance.COSINE)},
        quantization_config=m.ScalarQuantization(scalar=m.ScalarQuantizationConfig(type="int8", quantile=0.99, always_ram=True)),
    )
    client.upsert(COL, points=points, wait=True)
    time.sleep(0.5)
    scalar_recall = _recall_in_qdrant(client, COL, q_vecs, children, items)
    console.print(f"  scalar:  recall@5={scalar_recall}  ram≈{_ram_mb(len(children), dim, 'int8')}MB (analytic)")

    # --- product quant (PQ x64) -----------------------------------------------
    client.delete_collection(COL)
    client.create_collection(
        COL,
        vectors_config={"dense": m.VectorParams(size=dim, distance=m.Distance.COSINE)},
        quantization_config=m.ProductQuantization(product=m.ProductQuantizationConfig(compression="x64", always_ram=True)),
    )
    client.upsert(COL, points=points, wait=True)
    time.sleep(0.5)
    pq_recall = _recall_in_qdrant(client, COL, q_vecs, children, items)
    console.print(f"  pq:      recall@5={pq_recall}  ram≈{_ram_mb(len(children), dim, 'pq_x64')}MB (analytic)")

    # --- binary quant ---------------------------------------------------------
    client.delete_collection(COL)
    client.create_collection(
        COL,
        vectors_config={"dense": m.VectorParams(size=dim, distance=m.Distance.COSINE)},
        quantization_config=m.BinaryQuantization(binary=m.BinaryQuantizationConfig(always_ram=False)),
    )
    client.upsert(COL, points=points, wait=True)
    time.sleep(0.5)
    bq_recall = _recall_in_qdrant(client, COL, q_vecs, children, items)
    console.print(f"  binary:  recall@5={bq_recall}  ram≈{_ram_mb(len(children), dim, 'binary')}MB (analytic)")

    n = len(children)
    results = {
        "float": {"recall@5": float_recall, "ram_mb": _ram_mb(n, dim, "float"), "note": "analytic estimate (Qdrant 1.19 has no per-collection RAM API)"},
        "scalar_int8": {"recall@5": scalar_recall, "ram_mb": _ram_mb(n, dim, "int8")},
        "product_x64": {"recall@5": pq_recall, "ram_mb": _ram_mb(n, dim, "pq_x64")},
        "binary": {"recall@5": bq_recall, "ram_mb": _ram_mb(n, dim, "binary")},
    }
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RUNS_DIR / "06_quant.json"
    out_path.write_text(json.dumps(results, indent=2))
    console.print(f"[green]wrote[/green] {out_path}")

    # clean up
    client.delete_collection(COL)


# ---------------------------------------------------------------------------
# hnsw
# ---------------------------------------------------------------------------


def cmd_hnsw() -> None:
    import time as _time
    from qdrant_client import models as m

    items = _test_items()
    children = _build_chunks()
    model = "nomic-embed-text"
    raw_vecs = np.asarray(ollama.embed_documents([c.text for c in children], model=model), dtype=float)
    q_vecs = np.asarray([ollama.embed_query(it["question"], model=model) for it in items], dtype=float)
    dim = raw_vecs.shape[1]
    client = _qdrant_client()

    COL = "ch06_hnsw_bench"
    if client.collection_exists(COL):
        client.delete_collection(COL)

    points = [
        m.PointStruct(
            id=int(c.id, 16),
            vector={"dense": raw_vecs[i].tolist()},
            payload={"chunk_id": c.id, "paper": c.paper, "section": c.section, "text": c.text, "start": c.start, "end": c.end},
        )
        for i, c in enumerate(children)
    ]

    results = []
    for m_ in HNSW_M:
        for ef_c in HNSW_EF_CONSTRUCT:
            for ef_s in HNSW_EF_SEARCH:
                if client.collection_exists(COL):
                    client.delete_collection(COL)
                client.create_collection(
                    COL,
                    vectors_config={"dense": m.VectorParams(size=dim, distance=m.Distance.COSINE)},
                    hnsw_config=m.HnswConfigDiff(m=m_, ef_construct=ef_c),
                )
                client.upsert(COL, points=points, wait=True)
                _time.sleep(0.3)

                # Exact baseline (numpy)
                cv = _unit_normalize(raw_vecs)
                qv = _unit_normalize(q_vecs)
                id_by_pos = [int(c.id, 16) for c in children]  # positional -> point id
                exact_latencies = []
                exact_top10_sets = []
                for q in qv:
                    t0 = _time.monotonic()
                    sims = q @ cv.T
                    idx = np.argpartition(sims, -10)[-10:]
                    exact_top10_sets.append(frozenset(id_by_pos[i] for i in idx))
                    exact_latencies.append(_time.monotonic() - t0)
                exact_mean_ms = round(statistics.fmean(exact_latencies) * 1000, 3)

                # Qdrant (HNSW)
                qdrant_latencies = []
                qdrant_top10_sets = []
                for q in qv:
                    t0 = _time.monotonic()
                    res = client.query_points(COL, query=q.tolist(), limit=10, with_payload=True, using="dense", search_params=m.SearchParams(hnsw_ef=ef_s))
                    qdrant_latencies.append(_time.monotonic() - t0)
                    qdrant_top10_sets.append(frozenset(int(p.id) for p in res.points))
                qdrant_mean_ms = round(statistics.fmean(qdrant_latencies) * 1000, 3)

                # Recall@10 = |ANN ∩ exact| / |exact|
                recalls = [len(a & e) / len(e) if e else 0.0 for a, e in zip(qdrant_top10_sets, exact_top10_sets)]
                recall_vs_exact = round(statistics.fmean(recalls), 4)

                row = {
                    "m": m_,
                    "ef_construct": ef_c,
                    "ef_search": ef_s,
                    "qdrant_ms": qdrant_mean_ms,
                    "exact_ms": exact_mean_ms,
                    "recall_vs_exact": recall_vs_exact,
                }
                results.append(row)
                console.print(
                    f"  m={m_:<4} ef_c={ef_c:<5} ef_s={ef_s:<5} "
                    f"recall={recall_vs_exact}  qdrant={qdrant_mean_ms}ms  exact={exact_mean_ms}ms"
                )

    if client.collection_exists(COL):
        client.delete_collection(COL)

    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RUNS_DIR / "06_hnsw.json"
    out_path.write_text(json.dumps(results, indent=2))
    console.print(f"[green]wrote[/green] {out_path}")


# ---------------------------------------------------------------------------
# all
# ---------------------------------------------------------------------------


def cmd_all() -> None:
    console.print("[bold cyan]=== models ===[/bold cyan]")
    cmd_models()
    console.print("\n[bold cyan]=== matryoshka ===[/bold cyan]")
    cmd_matryoshka()
    console.print("\n[bold cyan]=== quant ===[/bold cyan]")
    cmd_quant()
    console.print("\n[bold cyan]=== hnsw ===[/bold cyan]")
    cmd_hnsw()


# ---------------------------------------------------------------------------
# Typer wiring
# ---------------------------------------------------------------------------


@app.command("models")
def models_cmd() -> None:
    """Retrieval-only comparison of all embedding models."""
    cmd_models()


@app.command("matryoshka")
def matryoshka_cmd() -> None:
    """Matryoshka truncation eval for nomic-embed-text."""
    cmd_matryoshka()


@app.command("quant")
def quant_cmd() -> None:
    """Qdrant scalar/product/binary quantization eval."""
    cmd_quant()


@app.command("hnsw")
def hnsw_cmd() -> None:
    """HNSW parameter sweep (m, ef_construct, ef_search)."""
    cmd_hnsw()


@app.command("all")
def all_cmd() -> None:
    """Run all four evals."""
    cmd_all()


if __name__ == "__main__":
    app()
