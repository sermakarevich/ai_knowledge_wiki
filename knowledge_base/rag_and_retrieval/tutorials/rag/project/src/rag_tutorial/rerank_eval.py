"""Chapter 07: rerankers + query transforms on the fixed chapter-05 setup
(parent_child 800/160, hybrid RRF pool, k=5 final, baseline prompt).

Every named experiment writes `runs/<name>/{metrics.json,predictions.jsonl,config.json}`.
  - `07_hybrid_k20_*_k5`: rerank the hybrid pool (k_each=20) with cross-encoder
    bge/MiniLM, FlashRank, ColBERT (pylate), LLM listwise (pointwise is
    unit-tested in `tests/test_07_rerank.py` and not run as a named experiment)
  - `07_multi_query`, `07_hyde`, `07_step_back`, `07_decompose`: extra queries
    -> per-query hybrid child rankings -> RRF fusion -> parent swap
  - `07_litm_reorder` (k=10), `07_compress`: retrieval unchanged, context reshuffled/pruned
  - `07_best_combo`: multi-query + cross-encoder bge + lost-in-the-middle reorder

`sweep` is retrieval-only (fast rerankers bge/minilm/flashrank × k_each
{20, 50} × k {1, 3, 5, 10, 20}, no generation) and writes
`runs/07_rerank_sweep.json`; `per-type` writes `runs/07_per_type.md`.
"""

from __future__ import annotations

import json
import statistics
import time

import typer
from rich.console import Console

from rag_tutorial.baseline import _short_names
from rag_tutorial.config import settings
from rag_tutorial.evaluate import evaluate_run, retrieval_metrics
from rag_tutorial.golden import QA_PATH, load_qa
from rag_tutorial.llm import ollama
from rag_tutorial.prompts import build_messages
from rag_tutorial.query_transforms import (
    compress,
    decompose,
    hyde,
    lost_in_the_middle_reorder,
    multi_query,
    step_back,
)
from rag_tutorial.rerankers import (
    ColBERTUnavailable,
    ColBERTReranker,
    CrossEncoderReranker,
    FlashRankReranker,
    LLMReranker,
)
from rag_tutorial.retrieval_eval import _Indexes
from rag_tutorial.retrievers import _swap_to_parent, rrf_fuse
from rag_tutorial.schema import Chunk

app = typer.Typer(add_completion=False)
console = Console()

RUNS_DIR = settings.path("runs")
RERANK_POOL = 20  # chapter-05 fixed setup: k_each=20
CTX_K = 5  # chapter-05 fixed setup: final k=5
LITM_K = 10  # spec: `07_litm_reorder` (k=10)


# -- the one answer path shared by every named runner ---------------------------------


def _triples(chunks: list[Chunk]) -> list[tuple[str, str, str]]:
    short_names = _short_names()
    return [(short_names.get(c.paper, c.paper), c.section, c.text) for c in chunks]


def _ask(question: str, contexts: list[Chunk]) -> tuple[str, list[str]]:
    triples = _triples(contexts)
    messages = build_messages(question, triples)
    reply = ollama.chat(messages, max_tokens=384)
    return reply, [f"[{s}] {text}" for s, _section, text in triples]


def _answer_fn(chunks_fn) -> tuple:
    """answer_fn factory: `chunks_fn(retrieved)` maps the ranked result to the
    context order actually handed to the generator."""

    def answer_fn(item: dict, retrieved: list[Chunk]) -> tuple[str, list[str], int]:
        context = chunks_fn(retrieved)
        reply, contexts = _ask(item["question"], context)
        return reply, contexts, 1

    return answer_fn


# -- hybrid child-level ranking (no parent swap) ----------------------------------------


def _hybrid_children(idx: _Indexes, question: str, k_each: int = RERANK_POOL) -> list[Chunk]:
    """One hybrid RRF pass at the child level — the candidate pool every
    reranker experiment starts from."""
    dense = idx.dense_raw(k=k_each)
    sparse = idx.bm25(k=k_each, with_parent_swap=False)
    dense_ids = [c.id for c, _s in dense.retrieve_scored(question, k_each)]
    sparse_ids = [c.id for c, _s in sparse.retrieve_scored(question, k_each)]
    fused = rrf_fuse([dense_ids, sparse_ids])
    by_id = {c.id: c for c in idx.children}
    return [by_id[cid] for cid in fused if cid in by_id]


def _to_parents(ranked_children: list[Chunk], idx: _Indexes, n: int = CTX_K) -> list[Chunk]:
    return _swap_to_parent(ranked_children, idx.child_to_parent, idx.parents, n)


def _hybrid_parents(idx: _Indexes, question: str, k: int) -> list[Chunk]:
    return _to_parents(_hybrid_children(idx, question, k_each=max(k, RERANK_POOL)), idx, n=k)


def _variants_children(idx: _Indexes, item: dict, extra_queries: list[str], k_each: int = RERANK_POOL) -> list[Chunk]:
    """Per-query hybrid child rankings (original + variants) -> RRF fusion."""
    dense = idx.dense_raw(k=k_each)
    sparse = idx.bm25(k=k_each, with_parent_swap=False)
    by_id = {c.id: c for c in idx.children}
    low = item["question"].lower()
    rankings = []
    for q in [item["question"]] + [v for v in extra_queries if v and v.lower() != low]:
        dense_ids = [c.id for c, _s in dense.retrieve_scored(q, k_each)]
        sparse_ids = [c.id for c, _s in sparse.retrieve_scored(q, k_each)]
        rankings.append(rrf_fuse([dense_ids, sparse_ids]))
    fused = rrf_fuse(rankings)
    return [by_id[cid] for cid in fused if cid in by_id][: 2 * k_each]


# -- shared reranker instances (one model load each) -------------------------------------


class _Rerankers:
    def __init__(self):
        self._bge: CrossEncoderReranker | None = None
        self._minilm: CrossEncoderReranker | None = None
        self._flashrank: FlashRankReranker | None = None
        self._colbert: ColBERTReranker | None = None
        self._llm_list: LLMReranker | None = None
        self._llm_point: LLMReranker | None = None
        self.colbert_error: str | None = None

    def bge(self) -> CrossEncoderReranker:
        if self._bge is None:
            self._bge = CrossEncoderReranker("BAAI/bge-reranker-v2-m3")
        return self._bge

    def minilm(self) -> CrossEncoderReranker:
        if self._minilm is None:
            self._minilm = CrossEncoderReranker("cross-encoder/ms-marco-MiniLM-L-6-v2")
        return self._minilm

    def flashrank(self) -> FlashRankReranker:
        if self._flashrank is None:
            self._flashrank = FlashRankReranker("ms-marco-TinyBERT-L-2-v2")
        return self._flashrank

    def colbert(self) -> ColBERTReranker:
        if self._colbert is None:
            try:
                self._colbert = ColBERTReranker("answerdotai/answerai-colbert-small-v1")
                self._colbert._ensure()  # force the model load; record a clean error
            except ColBERTUnavailable as exc:
                self.colbert_error = str(exc)
                raise
        return self._colbert

    def llm_listwise(self) -> LLMReranker:
        if self._llm_list is None:
            self._llm_list = LLMReranker(mode="listwise")
        return self._llm_list

    def llm_pointwise(self) -> LLMReranker:
        if self._llm_point is None:
            self._llm_point = LLMReranker(mode="pointwise")
        return self._llm_point


_RR = _Rerankers()


# -- named runners ------------------------------------------------------------------------


def run_rerank(name: str, idx: _Indexes, reranker, pool: int) -> dict:
    def retrieve_fn(item: dict) -> list[Chunk]:
        children = _hybrid_children(idx, item["question"], k_each=pool)
        reranked = reranker.rerank(item["question"], children, k=CTX_K)
        return _to_parents(reranked, idx)

    metrics = evaluate_run(name, chapter="07", answer_fn=_answer_fn(lambda c: c), retrieve_fn=retrieve_fn)
    # Attribute the reranker itself: how many scoring passes it actually did
    # across the whole test split (0 on a fully disk-cached re-run). Every
    # Reranker subclass carries the class attribute; this is 0 on a cache hit.
    metrics["details"]["reranker_n_calls"] = reranker.n_calls
    (RUNS_DIR / name / "metrics.json").write_text(json.dumps(metrics, indent=2))
    return metrics


def run_transform(name: str, idx: _Indexes, make_variants) -> dict:
    def retrieve_fn(item: dict) -> list[Chunk]:
        tr = make_variants(item["question"])
        return _to_parents(_variants_children(idx, item, tr.variants), idx)

    return evaluate_run(name, chapter="07", answer_fn=_answer_fn(lambda c: c), retrieve_fn=retrieve_fn)


def run_litm(idx: _Indexes) -> dict:
    """Retrieval = baseline hybrid at k=10; only the generator's context order
    changes (2nd-ranked chunk moved to the end — `lost_in_the_middle_reorder`)."""

    def retrieve_fn(item: dict) -> list[Chunk]:
        return _hybrid_parents(idx, item["question"], k=LITM_K)

    return evaluate_run(
        "07_litm_reorder",
        chapter="07",
        answer_fn=_answer_fn(lambda chunks: lost_in_the_middle_reorder(chunks, k=LITM_K)),
        retrieve_fn=retrieve_fn,
    )


def run_compress(idx: _Indexes) -> dict:
    """Retrieval = baseline hybrid at k=5; the generator gets only the LLM-pruned
    question-relevant sentences. One extra LLM pass per question (counted in
    `llm_calls_per_q`)."""

    def retrieve_fn(item: dict) -> list[Chunk]:
        return _hybrid_parents(idx, item["question"], k=CTX_K)

    def answer_fn(item: dict, retrieved: list[Chunk]) -> tuple[str, list[str], int]:
        result = compress(retrieved, item["question"], ollama)
        short_names = _short_names()
        compressed_chunks = []
        for chunk, text in result.compressed:
            if text and text.strip():
                compressed_chunks.append((chunk.paper, chunk.section, text))
        if compressed_chunks:
            fake = [Chunk(id=f"compressed:{i}", paper=p, section=s, text=t, start=0, end=0) for i, (p, s, t) in enumerate(compressed_chunks)]
            reply, contexts = _ask(item["question"], fake)
        else:
            reply, contexts = _ask(item["question"], [])  # nothing relevant -> model abstains
        return reply, contexts, 1 + result.n_llm_calls

    return evaluate_run("07_compress", chapter="07", answer_fn=answer_fn, retrieve_fn=retrieve_fn)


def run_best_combo(idx: _Indexes) -> dict:
    """Multi-query (3 variants) + per-query hybrid child rankings -> RRF ->
    cross-encoder bge on the fused pool -> lost-in-the-middle reorder of the
    final 5 contexts."""

    def retrieve_fn(item: dict) -> list[Chunk]:
        tr = multi_query(item["question"], ollama, n=3)
        children = _variants_children(idx, item, tr.variants)
        reranked = _RR.bge().rerank(item["question"], children, k=CTX_K)
        return _to_parents(reranked, idx)

    return evaluate_run(
        "07_best_combo",
        chapter="07",
        answer_fn=_answer_fn(lambda chunks: lost_in_the_middle_reorder(chunks, k=CTX_K)),
        retrieve_fn=retrieve_fn,
    )


# -- retrieval-only k_each sweep (reranked pools, no generation) ----------------------------


@app.command()
def sweep(rebuild: bool = False) -> None:
    """For each reranker and k_each in {20, 50}: retrieval-only metrics of
    'rerank the pool -> top-k' (k in 1/3/5/10/20). Writes
    `runs/07_rerank_sweep.json`."""
    idx = _Indexes(rebuild=rebuild)
    items = [i for i in load_qa(QA_PATH) if i["split"] == "test" and i["evidence"]]
    ks = (1, 3, 5, 10, 20)

    def fetch(rr, k_each: int, item: dict, k: int) -> list[Chunk]:
        children = _hybrid_children(idx, item["question"], k_each=k_each)
        reranked = rr.rerank(item["question"], children, k=max(k, 5))
        return _to_parents(reranked, idx, n=k)

    # Fast rankers only — the sweep has no generation, but ColBERT still costs
    # one passage encoding per (question, passage) and LLM reranking needs
    # 27x50 chat calls on a shared GPU. The two cross-encoders + FlashRank
    # are the ones that fit within the chapter's "politeness" budget.
    rerankers: list[tuple[str, object]] = [
        ("cross-encoder-bge", _RR.bge()),
        ("cross-encoder-minilm", _RR.minilm()),
        ("flashrank", _RR.flashrank()),
    ]

    rows = []
    for k_each in (20, 50):
        for label, rr in rerankers:
            rows.append(_retrieval_only(f"{label}_keach_{k_each}", lambda item, k, _rr=rr, _ke=k_each: fetch(_rr, _ke, item, k), items, ks))

    out = RUNS_DIR / "07_rerank_sweep.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rows, indent=2))
    console.print(f"[green]wrote[/green] {out}")


def _retrieval_only(name: str, retrieve_fn, items: list[dict], ks: tuple[int, ...]) -> dict:
    rows, seconds = [], []
    for item in items:
        start = time.monotonic()
        retrieved = retrieve_fn(item, max(ks))
        seconds.append(time.monotonic() - start)
        rows.append(retrieval_metrics(retrieved, item["evidence"], ks=ks, ndcg_ks=ks))

    def _mean(key: str) -> float:
        return statistics.fmean(r[key] for r in rows) if rows else 0.0

    result = {"name": name, "n_questions": len(rows), "mean_seconds": round(statistics.fmean(seconds), 4) if seconds else 0.0}
    for k in ks:
        result[f"hit@{k}"] = round(_mean(f"hit@{k}"), 4)
        result[f"recall@{k}"] = round(_mean(f"recall@{k}"), 4)
        result[f"ndcg@{k}"] = round(_mean(f"ndcg@{k}"), 4)
    result["mrr"] = round(_mean("mrr"), 4)
    return result


# -- per-question-type table ------------------------------------------------------------------


@app.command()
def per_type() -> None:
    """Per-question-type table, `07_best_combo` vs the `05_hybrid_rrf_k5`
    baseline. Writes `runs/07_per_type.md`."""
    TYPES = ("single_hop", "multi_hop", "comparative", "global", "unanswerable")

    def rows_of(run_name: str) -> list[dict]:
        out = []
        with (RUNS_DIR / run_name / "predictions.jsonl").open() as f:
            for line in f:
                rec = json.loads(line)
                out.append(
                    {
                        "type": rec["type"],
                        "correct": rec["correctness"]["score"] if rec.get("correctness") else None,
                        "faithful": rec["faithfulness"]["score"] if rec.get("faithfulness") else None,
                        "abstain": rec["abstain"]["abstain"] if rec.get("abstain") else None,
                    }
                )
        return out

    def _mean(rows: list[dict], key: str) -> float | None:
        vals = [r[key] for r in rows if r.get(key) is not None]
        return statistics.fmean(vals) if vals else None

    base, combo = rows_of("05_hybrid_rrf_k5"), rows_of("07_best_combo")

    def _fmt(v: float | None) -> str:
        return f"{v:.4f}" if v is not None else "-"

    def _delta(a: float | None, b: float | None) -> str:
        return f"{(b - a):+.4f}" if a is not None and b is not None else "-"

    lines = ["| type | n |", "|---|---|"]
    for t in TYPES:
        lines.append(f"| {t} | {sum(1 for r in combo if r['type'] == t)} |")

    for metric, key in (("correct", "correct"), ("faithful", "faithful"), ("abstain", "abstain")):
        lines += ["", f"| {metric} | " + " | ".join(TYPES) + " |", "|---|" + "---|" * len(TYPES)]
        for label, rows in (("05_hybrid_rrf_k5 (baseline)", base), ("07_best_combo", combo)):
            lines.append(f"| {label} | " + " | ".join(_fmt(_mean([r for r in rows if r['type'] == t], key)) for t in TYPES) + " |")
        lines.append("| delta | " + " | ".join(_delta(_mean([r for r in base if r['type'] == t], key), _mean([r for r in combo if r['type'] == t], key)) for t in TYPES) + " |")

    out = RUNS_DIR / "07_per_type.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n")
    console.print(f"[green]wrote[/green] {out}")


# -- run-all ---------------------------------------------------------------------------------


EXPERIMENTS = {
    "07_hybrid_k20_ce_bge_k5": lambda idx: run_rerank("07_hybrid_k20_ce_bge_k5", idx, _RR.bge(), RERANK_POOL),
    "07_hybrid_k20_ce_minilm_k5": lambda idx: run_rerank("07_hybrid_k20_ce_minilm_k5", idx, _RR.minilm(), RERANK_POOL),
    "07_hybrid_k20_flashrank_k5": lambda idx: run_rerank("07_hybrid_k20_flashrank_k5", idx, _RR.flashrank(), RERANK_POOL),
    "07_hybrid_k20_llm_listwise_k5": lambda idx: run_rerank("07_hybrid_k20_llm_listwise_k5", idx, _RR.llm_listwise(), RERANK_POOL),
    "07_hybrid_k20_colbert_k5": lambda idx: run_rerank("07_hybrid_k20_colbert_k5", idx, _RR.colbert(), RERANK_POOL),
    "07_multi_query": lambda idx: run_transform("07_multi_query", idx, lambda q: multi_query(q, ollama, n=3)),
    "07_hyde": lambda idx: run_transform("07_hyde", idx, lambda q: hyde(q, ollama)),
    "07_step_back": lambda idx: run_transform("07_step_back", idx, lambda q: step_back(q, ollama)),
    "07_decompose": lambda idx: run_transform("07_decompose", idx, lambda q: decompose(q, ollama)),
    "07_litm_reorder": lambda idx: run_litm(idx),
    "07_compress": lambda idx: run_compress(idx),
    "07_best_combo": lambda idx: run_best_combo(idx),
}


@app.command(name="run-all")
def run_all(only: list[str] = typer.Option(None, "--only", help="run only these experiment names (default: all)"), rebuild: bool = False) -> None:
    idx = _Indexes(rebuild=rebuild)
    names = only or list(EXPERIMENTS)
    for name in names:
        if name not in EXPERIMENTS:
            raise typer.BadParameter(f"unknown experiment {name!r}, choose from {list(EXPERIMENTS)}")
        console.print(f"[bold]running[/bold] {name}")
        try:
            EXPERIMENTS[name](idx)
        except ColBERTUnavailable as exc:
            (RUNS_DIR / name).mkdir(parents=True, exist_ok=True)
            (RUNS_DIR / name / "metrics.json").write_text(
                json.dumps({"experiment": name, "chapter": "07", "skipped": "colbert", "reason": str(exc)}, indent=2)
            )
            console.print(f"[yellow]skipped[/yellow] {name}: {exc}")
        else:
            console.print(f"[green]done[/green] {name}")


if __name__ == "__main__":
    app()
