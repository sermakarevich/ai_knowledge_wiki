"""Chapter 11 (part 1): RAPTOR — recursive abstractive tree-organized retrieval.

RAPTOR (Sarthi et al., arXiv:2401.18059) builds a tree over the corpus:
leaves = original chunks, higher levels = LLM summaries of embedding-space
clusters of the level below. Retrieval is "collapsed tree": embed the query
and take the top-k nodes over *all* levels from one store.

Leaves here are chapter 05's fixed setup (parent_child children, 160/32
tokens), so a scoreboard difference vs `05_*` is the tree, not the chunking.

Clustering: the paper uses UMAP + GMM. We use agglomerative clustering with
cosine distance (`scikit-learn`) instead — one fewer heavy dependency
(`umap-learn` pulls `numba`/`pynndescent`), deterministic output, and direct
control of the cluster count (`n_clusters = ceil(N / target_size)`), which is
what decides the tree shape and the summary-call budget.

All LLM/embedding calls go through `rag_tutorial.llm` (disk-cached).
"""

from __future__ import annotations

import json
import time
from collections import Counter
from pathlib import Path

import numpy as np
import typer
from rich.console import Console
from sklearn.cluster import AgglomerativeClustering

from rag_tutorial.config import settings
from rag_tutorial.corpus import load_papers
from rag_tutorial.evaluate import evaluate_run
from rag_tutorial.golden import load_documents
from rag_tutorial.llm import ollama
from rag_tutorial.prompts import build_messages
from rag_tutorial.retrieval_eval import build_parent_child_index
from rag_tutorial.schema import Chunk
from rag_tutorial.stores import ChromaStore

app = typer.Typer(add_completion=False)
console = Console()

RUNS_DIR = settings.path("runs")
RAPTOR_DIR = RUNS_DIR / "11_raptor"
TREE_PATH = RAPTOR_DIR / "tree.json"
BUILD_STATS_PATH = RAPTOR_DIR / "build_stats.json"
COLLECTION_NAME = "raptor_11_all"

TARGET_CLUSTER_SIZE = 10
TOP_LEVEL_MAX_NODES = 5
SUMMARY_MAX_TOKENS = 512


def _short_names() -> dict[str, str]:
    return {paper["id"]: paper["short_name"] for paper in load_papers()}


def cluster_embeddings(embeddings: list[list[float]], target_size: int = TARGET_CLUSTER_SIZE) -> list[int]:
    """Partition `embeddings` into clusters of roughly `target_size` nodes.

    Agglomerative clustering on cosine distance (embeddings need not be
    normalised — cosine handles that). Returns one integer label per row.
    A single node forms its own cluster; an empty input returns [].
    """
    n = len(embeddings)
    if n == 0:
        return []
    if n == 1:
        return [0]
    n_clusters = max(1, round(n / target_size))
    n_clusters = min(n_clusters, n)
    if n_clusters == 1:
        return [0] * n
    model = AgglomerativeClustering(n_clusters=n_clusters, metric="cosine", linkage="average")
    return [int(x) for x in model.fit_predict(np.asarray(embeddings, dtype=np.float64))]


def summarize_cluster(texts: list[str], llm=None) -> str:
    """One LLM summary of a cluster's member texts. Returns the summary text."""
    client = llm or ollama
    excerpts = "\n\n".join(f"[excerpt {i + 1}]\n{t[:1200]}" for i, t in enumerate(texts))
    reply = client.chat(
        [
            {
                "role": "system",
                "content": "Summarize the excerpts below into one concise paragraph that preserves the key facts, "
                "numbers and named entities. Reply with the summary only.",
            },
            {"role": "user", "content": excerpts},
        ],
        max_tokens=SUMMARY_MAX_TOKENS,
    )
    return reply.strip()


def build_tree(
    leaves: list[Chunk],
    embed_fn=None,
    llm=None,
    target_size: int = TARGET_CLUSTER_SIZE,
) -> tuple[list[dict], int]:
    """Build the RAPTOR tree over `leaves`. Returns (nodes, summary_calls).

    `nodes` are dicts {id, level, paper, section, text, children}; level 0 =
    leaves. One recursion step clusters the current level, writes one summary
    node per cluster, embeds the summaries and repeats — until the newest
    level has <= `TOP_LEVEL_MAX_NODES` nodes (it becomes the top, no single
    root is forced) or a level has a single node.
    """
    embed = embed_fn or ollama.embed_documents
    nodes: list[dict] = [
        {"id": c.id, "level": 0, "paper": c.paper, "section": c.section, "text": c.text, "children": []}
        for c in leaves
    ]
    summary_calls = 0
    current = nodes
    level = 0
    while len(current) > 1:
        level += 1
        vectors = embed([n["text"] for n in current])
        labels = cluster_embeddings(vectors, target_size=target_size)
        by_label: dict[int, list[int]] = {}
        for idx, label in enumerate(labels):
            by_label.setdefault(label, []).append(idx)
        if len(by_label) <= 1 and len(current) <= TOP_LEVEL_MAX_NODES:
            break
        new_level: list[dict] = []
        for label in sorted(by_label):
            members = [current[i] for i in by_label[label]]
            if len(members) == 1 and len(by_label) == 1:
                break  # clustering cannot split further; top level reached
            papers = Counter(m["paper"] for m in members)
            summary = summarize_cluster([m["text"] for m in members], llm=llm)
            summary_calls += 1
            new_level.append(
                {
                    "id": f"raptor-L{level}-{len(new_level):04d}",
                    "level": level,
                    "paper": papers.most_common(1)[0][0],
                    "section": f"summary/L{level}",
                    "text": summary,
                    "children": [m["id"] for m in members],
                }
            )
        else:
            current = new_level
            nodes.extend(new_level)
            if len(new_level) <= TOP_LEVEL_MAX_NODES:
                break
            continue
        break
    return nodes, summary_calls


def tree_shape(nodes: list[dict]) -> dict:
    """{levels: {level: count}, total_nodes, n_summaries, depth} for reporting."""
    per_level = Counter(n["level"] for n in nodes)
    return {
        "levels": {str(k): per_level[k] for k in sorted(per_level)},
        "total_nodes": len(nodes),
        "n_summaries": sum(1 for n in nodes if n["level"] > 0),
        "depth": max(per_level) if per_level else 0,
    }


def save_tree(nodes: list[dict]) -> None:
    RAPTOR_DIR.mkdir(parents=True, exist_ok=True)
    TREE_PATH.write_text(json.dumps(nodes, indent=2, ensure_ascii=False))


def load_tree() -> list[dict]:
    return json.loads(TREE_PATH.read_text())


def _node_to_chunk(node: dict) -> Chunk:
    return Chunk(
        id=node["id"],
        paper=node["paper"],
        section=node["section"],
        text=node["text"],
        start=0,
        end=len(node["text"]),
        meta={"level": node["level"], "children": node.get("children", [])},
    )


def retrieve_collapsed(question: str, k: int, store: ChromaStore | None = None) -> list[Chunk]:
    """Collapsed-tree retrieval: top-k over leaves + summaries in one collection."""
    store = store or ChromaStore(COLLECTION_NAME)
    query_embedding = ollama.embed_query(question)
    return [chunk for chunk, _score in store.query(query_embedding, k=k)]


def answer(question: str, retrieved: list[Chunk]) -> tuple[str, list[str]]:
    """Same fixed prompt as chapters 03/05 — scoreboard differences are the retriever."""
    short_names = _short_names()
    triples = [(short_names.get(c.paper, c.paper), c.section, c.text) for c in retrieved]
    messages = build_messages(question, triples)
    reply = ollama.chat(messages, max_tokens=384)
    contexts = [f"[{short_name}] {text}" for short_name, _section, text in triples]
    return reply, contexts


def _answer_fn(item: dict, retrieved: list[Chunk]) -> tuple[str, list[str], int]:
    reply, contexts = answer(item["question"], retrieved)
    return reply, contexts, 1


@app.command()
def build() -> None:
    """Build the RAPTOR tree (embed leaves -> cluster -> summarize -> repeat),
    store every node in one Chroma collection, write tree.json + build_stats.json."""
    started = time.monotonic()
    docs = load_documents()
    children, _parents, _c2p = build_parent_child_index(docs)
    console.print(f"leaves (ch05 children): {len(children)}")

    nodes, summary_calls = build_tree(children)
    shape = tree_shape(nodes)
    console.print(f"tree shape: {shape} ({summary_calls} summary calls)")

    save_tree(nodes)
    store = ChromaStore(COLLECTION_NAME)
    store.reset()
    chunks = _nodes_to_store_chunks(nodes, children)
    embeddings = ollama.embed_documents([c.text for c in chunks])
    store.add(chunks, embeddings)

    stats = {
        "n_leaves": len(children),
        "summary_calls": summary_calls,
        "tree_shape": shape,
        "collection": COLLECTION_NAME,
        "stored_nodes": store.count(),
        "wall_minutes": round((time.monotonic() - started) / 60, 2),
        "index_bytes": store.on_disk_bytes(),
    }
    RAPTOR_DIR.mkdir(parents=True, exist_ok=True)
    BUILD_STATS_PATH.write_text(json.dumps(stats, indent=2))
    (RAPTOR_DIR / "config.json").write_text(
        json.dumps(
            {
                "leaves": "ch05 parent_child children (160/32)",
                "clustering": f"agglomerative cosine, target_size={TARGET_CLUSTER_SIZE}",
                "top_level_max_nodes": TOP_LEVEL_MAX_NODES,
                "chat_model": settings.chat_model,
                "embed_model": settings.embed_model,
            },
            indent=2,
        )
    )
    console.print(f"[green]built[/green] {store.count()} nodes in {stats['wall_minutes']} min")


def _nodes_to_store_chunks(nodes: list[dict], leaves: list[Chunk]) -> list[Chunk]:
    """Leaves keep their original chunk identity (id/offsets); summaries are new chunks."""
    by_id = {c.id: c for c in leaves}
    out: list[Chunk] = []
    for node in nodes:
        if node["level"] == 0 and node["id"] in by_id:
            out.append(by_id[node["id"]])
        else:
            out.append(_node_to_chunk(node))
    return out


@app.command()
def ask(question: str, k: int = 5) -> None:
    """Collapsed retrieval + fixed prompt for one question."""
    retrieved = retrieve_collapsed(question, k)
    for rank, chunk in enumerate(retrieved, start=1):
        level = chunk.meta.get("level", 0) if chunk.meta else 0
        console.print(f"[{rank}] L{level} {chunk.id} {chunk.paper} §{chunk.section[:50]}")
    reply, _contexts = answer(question, retrieved)
    console.print(f"\n[bold]Answer:[/bold]\n{reply}")


def _make_retrieve_fn(k: int):
    store = ChromaStore(COLLECTION_NAME)

    def retrieve_fn(item: dict) -> list[Chunk]:
        return retrieve_collapsed(item["question"], k, store)

    return retrieve_fn


@app.command(name="eval")
def eval_cmd() -> None:
    """Evaluate collapsed-tree retrieval at k=5 and k=10 (test split)."""
    evaluate_run(
        "11_raptor_collapsed_k5", chapter="11", answer_fn=_answer_fn, retrieve_fn=_make_retrieve_fn(5), split="test"
    )
    evaluate_run(
        "11_raptor_collapsed_k10", chapter="11", answer_fn=_answer_fn, retrieve_fn=_make_retrieve_fn(10), split="test"
    )


def collection_bytes() -> int:
    return ChromaStore(COLLECTION_NAME).on_disk_bytes()


PER_TYPE_ROWS = [
    "05_hybrid_rrf_k5",
    "07_best_combo",
    "08_lg_crag",
    "09_li_router",
    "11_raptor_collapsed_k5",
    "11_raptor_collapsed_k10",
    "11_lightrag_naive",
    "11_lightrag_local",
    "11_lightrag_global",
    "11_lightrag_hybrid",
    "11_lightrag_mix",
]

QUESTION_TYPES = ("single_hop", "multi_hop", "comparative", "global", "unanswerable")


def _correctness_score(raw) -> float | None:
    """Extract the 0/0.5/1 judge score; judge output is sometimes a str(dict)."""
    import ast

    if raw is None:
        return None
    if isinstance(raw, str):
        try:
            raw = ast.literal_eval(raw)
        except (ValueError, SyntaxError):
            return None
    if isinstance(raw, dict) and isinstance(raw.get("score"), (int, float)):
        return float(raw["score"])
    return None


def _abstain_score(raw) -> float | None:
    import ast

    if raw is None:
        return None
    if isinstance(raw, str):
        try:
            raw = ast.literal_eval(raw)
        except (ValueError, SyntaxError):
            return None
    if isinstance(raw, dict) and isinstance(raw.get("abstain"), (int, float)):
        return float(raw["abstain"])
    return None


def per_type_table(experiments: list[str] = PER_TYPE_ROWS) -> dict:
    """Mean correctness per question type (abstain rate for unanswerable).

    Reads each experiment's predictions.jsonl; missing experiments are skipped
    and recorded under "skipped".
    """
    table: dict[str, dict[str, float | None]] = {}
    skipped: list[str] = []
    for exp in experiments:
        path = RUNS_DIR / exp / "predictions.jsonl"
        if not path.exists():
            skipped.append(exp)
            continue
        by_type: dict[str, list[float]] = {t: [] for t in QUESTION_TYPES}
        for line in path.read_text().splitlines():
            if not line.strip():
                continue
            item = json.loads(line)
            qtype = item.get("type", "?")
            if qtype not in by_type:
                by_type[qtype] = []
            if qtype == "unanswerable":
                score = _abstain_score(item.get("abstain"))
            else:
                score = _correctness_score(item.get("correctness"))
            if score is not None:
                by_type[qtype].append(score)
        table[exp] = {
            t: (round(sum(v) / len(v), 4) if v else None) for t, v in by_type.items() if t in QUESTION_TYPES
        }
    return {"table": table, "skipped": skipped}


def indexing_cost_table() -> dict:
    """LLM calls / minutes / disk for baseline, contextual(04), RAPTOR, LightRAG."""
    costs: dict[str, dict] = {}
    stats_04 = {}
    chunk_stats = RUNS_DIR / "04_chunk_stats.json"
    if chunk_stats.exists():
        for row in json.loads(chunk_stats.read_text()):
            stats_04[row["experiment"]] = row
    fixed = stats_04.get("04_fixed_512_ov128", {})
    costs["baseline (03 naive, 512/128)"] = {
        "llm_calls": 0,
        "index_minutes": round(fixed.get("index_seconds", 0) / 60, 2) if fixed else None,
        "n_chunks": fixed.get("n_chunks"),
        "note": "embed-only; no LLM at index time",
    }
    contextual = stats_04.get("04_contextual_512", {})
    ctx_metrics = RUNS_DIR / "04_contextual_512" / "metrics.json"
    ctx_calls = None
    if ctx_metrics.exists():
        ctx_calls = json.loads(ctx_metrics.read_text()).get("details", {}).get("index_llm_calls")
    costs["contextual retrieval (04)"] = {
        "llm_calls": ctx_calls if ctx_calls is not None else contextual.get("n_chunks"),
        "index_minutes": round(contextual.get("index_seconds", 0) / 60, 2) if contextual else None,
        "n_chunks": contextual.get("n_chunks"),
        "note": "one LLM call per chunk (cached); calls counted" if ctx_calls else "one LLM call per chunk (estimate)",
    }
    raptor_stats = RAPTOR_DIR / "build_stats.json"
    if raptor_stats.exists():
        stats = json.loads(raptor_stats.read_text())
        costs["RAPTOR (11)"] = {
            "llm_calls": stats.get("summary_calls"),
            "index_minutes": stats.get("wall_minutes"),
            "n_nodes": stats.get("stored_nodes"),
            "tree_shape": stats.get("tree_shape"),
            "index_bytes": stats.get("index_bytes"),
        }
    else:
        costs["RAPTOR (11)"] = {"note": "build not finished yet"}
    lightrag_stats = RUNS_DIR / "11_lightrag" / "index_stats.json"
    if lightrag_stats.exists():
        stats = json.loads(lightrag_stats.read_text())
        costs["LightRAG (11)"] = {
            "llm_calls": stats.get("llm_calls"),
            "embed_texts": stats.get("embed_texts"),
            "index_minutes": stats.get("wall_minutes"),
            "graph": stats.get("graph"),
        }
    else:
        costs["LightRAG (11)"] = {"note": "index not finished yet"}
    return costs


@app.command(name="per-type")
def per_type_cmd() -> None:
    """Per-type correctness table for ch05/07/08/09 best + all ch11 rows.

    Writes runs/11_per_type.json and runs/11_per_type.png (indexing costs
    included in the JSON).
    """
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    per_type = per_type_table()
    costs = indexing_cost_table()
    out = {"per_type_correctness": per_type["table"], "skipped": per_type["skipped"], "indexing_cost": costs}
    (RUNS_DIR / "11_per_type.json").write_text(json.dumps(out, indent=2))

    rows = list(per_type["table"])
    plot_types = [t for t in QUESTION_TYPES if t != "unanswerable"]
    x = range(len(plot_types))
    width = 0.8 / max(1, len(rows))
    fig, ax = plt.subplots(figsize=(12, 5))
    for i, exp in enumerate(rows):
        vals = [per_type["table"][exp].get(t) or 0.0 for t in plot_types]
        ax.bar([p + i * width for p in x], vals, width=width, label=exp)
    ax.set_xticks([p + width * (len(rows) - 1) / 2 for p in x])
    ax.set_xticklabels(plot_types, rotation=15)
    ax.set_ylabel("mean correctness")
    ax.set_title("Correctness per question type (test split)")
    ax.legend(fontsize=7, loc="lower right")
    fig.tight_layout()
    fig.savefig(RUNS_DIR / "11_per_type.png", dpi=120)
    console.print(f"[green]wrote[/green] runs/11_per_type.json + runs/11_per_type.png ({len(rows)} rows)")
    if per_type["skipped"]:
        console.print(f"[yellow]skipped (no predictions.jsonl):[/yellow] {per_type['skipped']}")


if __name__ == "__main__":
    app()
