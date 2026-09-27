"""Chapter 08: retrieval metrics + RAGAS + DeepEval + agreement.

Deliverables:

1. ``retrieval``  -- classic information-retrieval metrics (hit@k, recall@k,
   precision@k, MRR, nDCG@k) for the answer pipeline, plus a recall@k curve
   (PNG) and a retrieval-vs-generation failure split. Pure embeddings
   (cached), zero new LLM generation calls.

2. ``ragas``      -- RAGAS classic metrics (faithfulness, answer_relevancy,
   context_precision) over the test split, using the local Ollama model.

3. ``deepeval``   -- the *same three* metrics from DeepEval (Faithfulness,
   AnswerRelevancy, ContextualPrecision) on the same test split, using
   DeepEval's native :class:`deepeval.models.OllamaModel` as the judge.

4. ``agreement``  -- Spearman correlation between the RAGAS and DeepEval
   faithfulness scores and the ch-04 embedding cosine similarity, plus AUROC
   of each of those three against the ch-03 gold pass label and the ch-05
   overall verdict. Pure, no LLM calls.

``all`` chains all four and rebuilds `runs/results.md`.
"""

from __future__ import annotations

import json
import math
import time
from pathlib import Path
from typing import Callable

import numpy as np
import typer

from evals_tutorial.config import settings
from evals_tutorial.helpdesk import TOP_SECTIONS, load_traces, retrieve
from evals_tutorial.results import write_metrics
from evals_tutorial.stats import bootstrap_ci
from evals_tutorial.tickets import load_tickets

app = typer.Typer(add_completion=False)

_RUN_TO_PRED_DIR = {
    "answer_v1": "05_judge_overall",
    "answer_v2": "07_answer_v2_judged_overall",
}


# ---------------------------------------------------------------------------
# pure IR metrics (deterministic, no I/O) -- these are the unit-tested core
# ---------------------------------------------------------------------------


def _ordered_unique(sections: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for s in sections:
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out


def _topk(retrieved_sections: list[str], k: int) -> list[str]:
    return _ordered_unique(retrieved_sections)[:k]


def hit_at_k(retrieved_sections: list[str], gold_sections: list[str], k: int) -> float:
    """1.0 if any gold section is in the top-k, else 0.0."""
    gold = set(gold_sections)
    return 1.0 if gold & set(_topk(retrieved_sections, k)) else 0.0


def recall_at_k(retrieved_sections: list[str], gold_sections: list[str], k: int) -> float:
    """|gold ∩ top-k| / |gold|; 0.0 if there is no gold section."""
    gold = set(gold_sections)
    if not gold:
        return 0.0
    return len(gold & set(_topk(retrieved_sections, k))) / len(gold)


def precision_at_k(retrieved_sections: list[str], gold_sections: list[str], k: int) -> float:
    """|gold ∩ top-k| / k; 0.0 when k <= 0 or top-k is empty."""
    if k <= 0:
        return 0.0
    topk = _topk(retrieved_sections, k)
    if not topk:
        return 0.0
    return len(set(gold_sections) & set(topk)) / k


def reciprocal_rank(retrieved_sections: list[str], gold_sections: list[str]) -> float:
    """1 / (1-based rank of first gold section); 0.0 if no gold section is present."""
    gold = set(gold_sections)
    for i, section in enumerate(_ordered_unique(retrieved_sections), start=1):
        if section in gold:
            return 1.0 / i
    return 0.0


def graded_relevance(gold_sections: list[str]) -> dict[str, float]:
    """Grade each gold section by importance order (earlier = higher).

    ``gold = [a, b, c]`` -> ``{a: 3, b: 2, c: 1}``. Non-gold sections absent.
    """
    gold = list(dict.fromkeys(gold_sections))
    n = len(gold)
    return {section: float(n - idx) for idx, section in enumerate(gold)}


def ndcg(retrieved_sections: list[str], gold_sections: list[str], k: int) -> float:
    """nDCG@k with graded relevance (see :func:`graded_relevance`)."""
    if not gold_sections or k <= 0:
        return 0.0
    grades = graded_relevance(gold_sections)

    def dcg(ordered: list[str]) -> float:
        total = 0.0
        for i, section in enumerate(ordered, start=1):
            total += grades.get(section, 0.0) / math.log2(i + 1)
        return total

    ideal = dcg(list(grades.keys()))
    if ideal <= 0:
        return 0.0
    return dcg(_topk(retrieved_sections, k)) / ideal


def per_ticket_ir(retrieved_sections: list[str], gold_sections: list[str], k: int) -> dict[str, float]:
    """All single-ticket IR metrics at once, at cut-off ``k``.

    At k == TOP_SECTIONS (the SUT's cut-off), precision@k == recall@k == hit@k
    when all gold sections are present -- the small-k distinctions are still
    visible in the curve, and MRR / nDCG add rank and order sensitivity.
    """
    return {
        f"hit@{k}": hit_at_k(retrieved_sections, gold_sections, k),
        f"recall@{k}": recall_at_k(retrieved_sections, gold_sections, k),
        f"precision@{k}": precision_at_k(retrieved_sections, gold_sections, k),
        "mrr": reciprocal_rank(retrieved_sections, gold_sections),
        f"ndcg@{k}": ndcg(retrieved_sections, gold_sections, k),
    }


def recall_curve(
    retrieved_sections: list[str], gold_sections: list[str], kmax: int
) -> list[dict[str, float]]:
    """hit / recall / precision at each k in 1..kmax from one ranked list.

    Uses the prefix property of ranked lists, so a single ``retrieve(k=kmax)``
    per ticket is enough to produce the whole curve -- no need to retrieve
    separately for each k.
    """
    gold = set(gold_sections)
    uniq = _ordered_unique(retrieved_sections)
    return [
        {
            "k": k,
            "hit": 1.0 if (gold & set(uniq[:k])) else 0.0,
            "recall": (len(gold & set(uniq[:k])) / len(gold)) if gold else 0.0,
            "precision": (len(gold & set(uniq[:k])) / k) if uniq[:k] else 0.0,
        }
        for k in range(1, kmax + 1)
    ]


def _plot_curves(points: list[dict[str, float]], path: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ks = [p["k"] for p in points]
    fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=140)
    ax.plot(ks, [p["recall"] for p in points], marker="o", label="recall@k")
    ax.plot(ks, [p["precision"] for p in points], marker="s", label="precision@k")
    ax.plot(ks, [p["hit"] for p in points], marker="^", linestyle="--", label="hit@k")
    ax.set_xlabel("k")
    ax.set_ylabel("score")
    ax.set_title("Retrieval curves (test split)")
    ax.set_xticks(ks)
    ax.set_ylim(0.0, 1.05)
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    plt.close(fig)


# ---------------------------------------------------------------------------
# agreement primitives (deterministic, pure, unit-tested separately so the live
# path is validated without a GPU)
# ---------------------------------------------------------------------------


def _tie_averaged_rank(values: list[float]) -> list[float]:
    """1-based tie-averaged ranks (mean rank for ties). Mirrors the rank the
    Mann-Whitney / Spearman formulas use; deterministic and dependency-free."""
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    n = len(values)
    while i < n:
        j = i
        while j + 1 < n and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + 1 + j + 1) / 2.0  # mean of 1..(i+1) .. 1..(j+1)
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def _pearson(x: list[float], y: list[float]) -> float:
    """Pearson correlation; 0.0 for a degenerate (zero-variance) input."""
    n = len(x)
    if n != len(y) or n < 2:
        return 0.0
    mx = sum(x) / n
    my = sum(y) / n
    cov = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    vx = sum((xi - mx) ** 2 for xi in x)
    vy = sum((yi - my) ** 2 for yi in y)
    if vx <= 0.0 or vy <= 0.0:
        return 0.0
    return cov / math.sqrt(vx * vy)


def spearman(x: list[float], y: list[float]) -> float:
    """Spearman rank correlation = Pearson on tie-averaged ranks."""
    return _pearson(_tie_averaged_rank(list(x)), _tie_averaged_rank(list(y)))


def auroc(scores: list[float], labels: list[int]) -> float:
    """Binary AUC via Mann-Whitney (0.5 if only one class present)."""
    labels = [int(bool(L)) for L in labels]
    if len(scores) != len(labels):
        raise ValueError("scores/labels length mismatch")
    n1 = sum(labels)
    n0 = len(labels) - n1
    if n1 == 0 or n0 == 0:
        return 0.5
    ranks = _tie_averaged_rank(list(scores))
    rank_sum_pos = sum(r for r, L in zip(ranks, labels) if L)
    return (rank_sum_pos - n1 * (n1 + 1) / 2.0) / (n1 * n0)


# ---------------------------------------------------------------------------
# data helpers
# ---------------------------------------------------------------------------


def _load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _split_ticket_ids(predictions_path: Path, split: str) -> list[str]:
    """ticket_ids where split matches (or "all"), in file order."""
    rows = _load_jsonl(predictions_path) if predictions_path.exists() else []
    return [
        r["ticket_id"]
        for r in rows
        if (split in ("all", "", None) or r.get("split") == split)
    ]


def _failed_ticket_ids(predictions_path: Path, split: str) -> set[str]:
    """ticket_ids where split matches and ``pred_pass`` is False."""
    rows = _load_jsonl(predictions_path) if predictions_path.exists() else []
    return {
        r["ticket_id"]
        for r in rows
        if r.get("split") == split and not r.get("pred_pass", True)
    }


def _tickets_by_id(project_root: Path) -> dict[str, dict]:
    tickets = load_tickets(project_root / "data" / "tickets" / "tickets.jsonl")
    return {t["id"]: t for t in tickets}


def _runs_dir(project_root: Path) -> Path:
    return Path(project_root) / "runs"


def _predictions_path_for(run: str, project_root: Path) -> Path:
    return _runs_dir(project_root) / _RUN_TO_PRED_DIR[run] / "predictions.jsonl"


def _experiment_name(run: str) -> str:
    return f"08_retrieval_{run}"


# ---------------------------------------------------------------------------
# retrieval command
# ---------------------------------------------------------------------------


def _retrieval_core(
    run: str,
    kmax: int,
    n_boot: int,
    seed: int,
    project_root: Path,
) -> dict:
    project_root = Path(project_root)
    predictions_path = _predictions_path_for(run, project_root)
    test_ids = _split_ticket_ids(predictions_path, split="test")
    failed_ids = _failed_ticket_ids(predictions_path, split="test")
    tickets = _tickets_by_id(project_root)
    traces_by_id = {t["ticket_id"]: t for t in load_traces(run)}
    client = None  # use module-level ollama; embeddings will hit the local cache

    per_ticket: list[dict] = []
    for tid in test_ids:
        ticket = tickets.get(tid)
        trace = traces_by_id.get(tid)
        if ticket is None or trace is None:
            continue
        retrieved = [r["section"] for r in trace.get("retrieved", [])]
        gold = list(ticket.get("gold", {}).get("sections", []))
        row = per_ticket_ir(retrieved, gold, k=TOP_SECTIONS)
        row.update(
            {
                "ticket_id": tid,
                "split": "test",
                "retrieved": retrieved,
                "gold": gold,
                "pred_pass": tid not in failed_ids,
            }
        )
        per_ticket.append(row)

    def _mean(name: str) -> float:
        vals = [r[name] for r in per_ticket]
        return float(np.mean(vals)) if vals else 0.0

    metrics = {
        "recall@2": _mean("recall@2"),
        "hit@2": _mean("hit@2"),
        "precision@2": _mean("precision@2"),
        "mrr": _mean("mrr"),
        "ndcg@2": _mean("ndcg@2"),
    }
    recall2 = [r["recall@2"] for r in per_ticket]
    ci: dict[str, list[float]] = {}
    if recall2:
        lo, hi = bootstrap_ci(recall2, n_boot=n_boot, seed=seed)
        ci["recall@2"] = [float(lo), float(hi)]

    # --- recall@k curve: one fresh retrieve(k=kmax) per ticket (cached embed) --
    exp_name = _experiment_name(run)
    curves_dir = _runs_dir(project_root) / exp_name
    curves_dir.mkdir(parents=True, exist_ok=True)

    per_ticket_curves: list[list[dict[str, float]]] = []
    for tid in test_ids:
        ticket = tickets.get(tid)
        if ticket is None:
            continue
        sections = [r["section"] for r in retrieve(ticket["text"], k=kmax, client=client)]
        gold = list(ticket.get("gold", {}).get("sections", []))
        per_ticket_curves.append(recall_curve(sections, gold, kmax))
    curve_points = [
        {
            "k": k,
            "recall": float(np.mean([c[k - 1]["recall"] for c in per_ticket_curves])),
            "precision": float(np.mean([c[k - 1]["precision"] for c in per_ticket_curves])),
            "hit": float(np.mean([c[k - 1]["hit"] for c in per_ticket_curves])),
        }
        for k in range(1, kmax + 1)
    ]
    _plot_curves(curve_points, curves_dir / "recall_curve.png")

    # --- retrieval-vs-generation failure split -------------------------------
    ret_fail = sum(1 for r in per_ticket if not r["pred_pass"] and r["recall@2"] == 0.0)
    gen_fail = sum(1 for r in per_ticket if not r["pred_pass"] and r["recall@2"] > 0.0)

    config = {
        "run": run,
        "kmax": kmax,
        "top_sections": TOP_SECTIONS,
        "n_boot": n_boot,
        "seed": seed,
        "n_test": len(per_ticket),
        "curve_png": str(curves_dir / "recall_curve.png"),
        "retrieval": "cosine top-k over handbook chunks, collapsed to sections",
    }
    details = {
        "primary": "recall@2",
        "notes": (
            "Per-ticket classical IR metrics on the test split. recall@2 is primary; "
            "CIs are bootstrap over tickets. The recall@k curve uses one fresh "
            "retrieve(k=kmax) per ticket (embeddings are cached). Failure split: "
            "failed tickets whose gold section was not in top-2 are retrieval "
            "failures; the rest are generation failures."
        ),
        "recall_curve": curve_points,
        "failure_split": {
            "failed_total": ret_fail + gen_fail,
            "retrieval_fail": ret_fail,
            "generation_fail": gen_fail,
        },
        "kmax": kmax,
    }
    prediction_rows = [
        {
            "ticket_id": r["ticket_id"],
            "split": r["split"],
            "retrieved": r["retrieved"],
            "gold": r["gold"],
            "pred_pass": r["pred_pass"],
            "hit@2": r["hit@2"],
            "recall@2": r["recall@2"],
            "precision@2": r["precision@2"],
            "mrr": r["mrr"],
            "ndcg@2": r["ndcg@2"],
        }
        for r in per_ticket
    ]
    return {
        "experiment": exp_name,
        "chapter": 8,
        "n": len(per_ticket),
        "metrics": metrics,
        "ci": ci,
        "llm_calls": 0,
        "seconds": 0.0,
        "details": details,
        "predictions": prediction_rows,
        "config": config,
        "project_root": project_root,
    }


@app.command()
def retrieval(  # noqa: PLR0913
    run: str = typer.Option("answer_v1", help="answer_v1 | answer_v2"),
    kmax: int = typer.Option(8, help="curve computed up to this k"),
    n_boot: int = typer.Option(2000),
    seed: int = typer.Option(0),
    project_root: Path = typer.Option(Path("."), show_default=False),
) -> None:
    core = _retrieval_core(run=run, kmax=kmax, n_boot=n_boot, seed=seed, project_root=project_root)
    path = write_metrics(**core)
    typer.echo(f"wrote {path}")


# ---------------------------------------------------------------------------
# ragas command
# ---------------------------------------------------------------------------


def _ragas_core(
    run: str,
    n: int,
    split: str,
    seed: int,
    project_root: Path,
) -> dict:
    import os

    os.environ["RAGAS_DO_NOT_TRACK"] = "true"

    from langchain_ollama import OllamaEmbeddings
    from openai import OpenAI
    from ragas import SingleTurnSample, EvaluationDataset, evaluate
    from ragas.embeddings import LangchainEmbeddingsWrapper
    from ragas.llms import llm_factory
    from ragas.metrics import AnswerRelevancy, ContextPrecision, Faithfulness

    from evals_tutorial.helpdesk import retrieved_context

    project_root = Path(project_root)
    runs = _runs_dir(project_root)
    predictions_path = _predictions_path_for(run, project_root)
    split_ids = _split_ticket_ids(predictions_path, split=split)
    tickets = _tickets_by_id(project_root)
    traces_by_id = {t["ticket_id"]: t for t in load_traces(run)}

    samples: list[SingleTurnSample] = []
    for tid in split_ids[:n]:
        ticket = tickets.get(tid)
        trace = traces_by_id.get(tid)
        if ticket is None or trace is None or not trace.get("output"):
            continue
        blocks, _rows = retrieved_context(ticket["text"])
        reference = "\n".join(ticket.get("gold", {}).get("answer_points", []))
        samples.append(
            SingleTurnSample(
                user_input=ticket["text"],
                retrieved_contexts=list(blocks),
                reference=reference,
                reference_contexts=list(blocks),
                response=trace["output"],
            )
        )

    client = OpenAI(base_url=settings.ollama_url + "/v1", api_key="ollama")
    llm = llm_factory(
        settings.chat_model,
        provider="openai",
        client=client,
        temperature=0,
        max_tokens=4096,
    )
    embeddings = LangchainEmbeddingsWrapper(
        OllamaEmbeddings(base_url=settings.ollama_url, model=settings.embed_model)
    )

    counter = {"gen": 0}

    def _count(fn: Callable) -> Callable:
        def _wrap(*a, **kw):
            counter["gen"] += 1
            return fn(*a, **kw)

        return _wrap

    for name in ("generate", "agenerate"):
        if hasattr(llm, name):
            setattr(llm, name, _count(getattr(llm, name)))

    t0 = time.time()
    result = evaluate(
        EvaluationDataset(samples=samples),
        metrics=[Faithfulness(), AnswerRelevancy(), ContextPrecision()],
        llm=llm,
        embeddings=embeddings,
        show_progress=False,
    )
    dt = time.time() - t0

    # result[name] is the per-item score list; _repr_dict[name] is its NaN-mean.
    # RAGAS can emit NaN for a sample whose sub-generation was truncated by the
    # token cap (local qwen) -- so we mean/CI over valid (finite) scores and
    # report how many were dropped per metric.
    import math

    metric_names = ["faithfulness", "answer_relevancy", "context_precision"]
    ci: dict[str, list[float]] = {}
    per_item_cols: dict[str, list[float]] = {}
    dropped: dict[str, int] = {}
    for name in metric_names:
        if name not in result._scores_dict:
            continue
        col = [float(v) for v in result[name]]
        valid = [v for v in col if not math.isnan(v)]
        per_item_cols[name] = valid
        dropped[name] = len(col) - len(valid)
        if len(valid) > 1:
            lo, hi = bootstrap_ci(valid, n_boot=2000, seed=seed)
            ci[name] = [float(lo), float(hi)]
    means = {}
    for name, valid in per_item_cols.items():
        means[name] = float(np.mean(valid)) if valid else float("nan")

    per_item_rows = [
        {name: rec.get(name) for name in metric_names}
        for rec in result.scores
    ]
    return {
        "experiment": f"08_ragas_{run}",
        "chapter": 8,
        "n": len(samples),
        "metrics": means,
        "ci": ci,
        "llm_calls": counter["gen"],
        "seconds": round(dt, 3),
        "details": {
            "primary": "faithfulness",
            "notes": (
                "RAGAS classic metrics (faithfulness, answer_relevancy, "
                "context_precision) on the test split. response = cached SUT "
                "answer from the trace. LLM calls counted on the RAGAS wrapper."
            ),
        },
        "predictions": per_item_rows,
        "config": {
            "run": run,
            "n": len(samples),
            "split": split,
            "seed": seed,
            "model": settings.chat_model,
            "embed_model": settings.embed_model,
            "max_tokens": 4096,
            "metrics": list(means.keys()),
            "dropped_nan": dropped,
        },
        "project_root": project_root,
    }


@app.command()
def ragas(  # noqa: PLR0913
    run: str = typer.Option("answer_v1"),
    n: int = typer.Option(30),
    split: str = typer.Option("test", help="test | all"),
    seed: int = typer.Option(0),
    project_root: Path = typer.Option(Path("."), show_default=False),
) -> None:
    core = _ragas_core(run=run, n=n, split=split, seed=seed, project_root=project_root)
    path = write_metrics(**core)
    typer.echo(f"wrote {path}")


# ---------------------------------------------------------------------------
# DeepEval (chapter 08b) -- native OllamaModel judge; LLM calls counted at the
# native-provider level (a_generate / generate) rather than through a wrapper.
# ---------------------------------------------------------------------------


def _deepeval_core(
    run: str,
    n: int,
    split: str,
    seed: int,
    project_root: Path,
) -> dict:
    """Run DeepEval (Faithfulness/AnswerRelevancy/ContextualPrecision) over the
    first ``n`` tickets on ``split`` (matching the same selection logic as the
    RAGAS run), using DeepEval's native :class:`deepeval.models.OllamaModel` as
    the judge so ``is_native_model`` is True and the cost-accruing path is used.
    LLM calls are counted by wrapping the model's ``a_generate`` / ``generate``
    instance methods -- DeepEval routes every metric's LLM call through these.
    """
    import os

    os.environ.setdefault("DEEPEVAL_TELEMETRY_OPT_OUT", "1")

    from deepeval.metrics import (
        AnswerRelevancyMetric,
        ContextualPrecisionMetric,
        FaithfulnessMetric,
    )
    from deepeval.models import OllamaModel
    from deepeval.test_case import LLMTestCase

    from evals_tutorial.helpdesk import retrieved_context

    project_root = Path(project_root)
    predictions_path = _predictions_path_for(run, project_root)
    split_ids = _split_ticket_ids(predictions_path, split=split)
    tickets = _tickets_by_id(project_root)
    traces_by_id = {t["ticket_id"]: t for t in load_traces(run)}

    test_cases: list[tuple[str, LLMTestCase]] = []
    for tid in split_ids[:n]:
        ticket = tickets.get(tid)
        trace = traces_by_id.get(tid)
        if ticket is None or trace is None or not trace.get("output"):
            continue
        blocks, _rows = retrieved_context(ticket["text"])
        reference = "\n".join(ticket.get("gold", {}).get("answer_points", []))
        test_cases.append(
            (
                tid,
                LLMTestCase(
                    input=ticket["text"],
                    actual_output=trace["output"],
                    retrieval_context=list(blocks),
                    expected_output=reference,
                ),
            )
        )

    model = OllamaModel(
        model=settings.chat_model, base_url=settings.ollama_url, temperature=0
    )
    counter = {"gen": 0}
    orig_sync = model.generate
    orig_async = model.a_generate

    def _count_sync(*args, **kwargs):
        counter["gen"] += 1
        return orig_sync(*args, **kwargs)

    async def _count_async(*args, **kwargs):
        counter["gen"] += 1
        return await orig_async(*args, **kwargs)

    model.generate = _count_sync  # type: ignore[method-assign]
    model.a_generate = _count_async  # type: ignore[method-assign]

    t0 = time.time()
    per_ticket: list[dict] = []
    for tid, tc in test_cases:
        row: dict = {"ticket_id": tid, "split": split}
        for name, cls in (
            ("faithfulness", FaithfulnessMetric),
            ("answer_relevancy", AnswerRelevancyMetric),
            ("context_precision", ContextualPrecisionMetric),
        ):
            try:
                metric = cls(model=model, threshold=0.5, async_mode=False)
                metric.measure(tc)
                row[name] = float(metric.score) if metric.score is not None else float("nan")
            except Exception as exc:  # noqa: BLE001  (one bad metric per row shouldn't kill the run)
                row[name] = float("nan")
                row.setdefault("errors", []).append(f"{name}: {exc}")
        per_ticket.append(row)
    dt = time.time() - t0

    def _finite(name: str) -> list[float]:
        return [
            r[name]
            for r in per_ticket
            if r.get(name) is not None and not (isinstance(r.get(name), float) and math.isnan(r.get(name)))
        ]

    metric_names = ["faithfulness", "answer_relevancy", "context_precision"]
    means: dict[str, float] = {}
    ci: dict[str, list[float]] = {}
    dropped: dict[str, int] = {}
    for name in metric_names:
        finite = _finite(name)
        dropped[name] = len(per_ticket) - len(finite)
        if finite:
            means[name] = float(np.mean(finite))
        if len(finite) > 1:
            lo, hi = bootstrap_ci(finite, n_boot=2000, seed=seed)
            ci[name] = [float(lo), float(hi)]

    return {
        "experiment": f"08_deepeval_{run}",
        "chapter": 8,
        "n": len(per_ticket),
        "metrics": means,
        "ci": ci,
        "llm_calls": counter["gen"],
        "seconds": round(dt, 3),
        "details": {
            "primary": "faithfulness",
            "notes": (
                "DeepEval native Ollama judge (Faithfulness/AnswerRelevancy/"
                "ContextualPrecision) on the same test split as RAGAS. "
                "LLM calls counted on the native OllamaModel.generate/a_generate."
            ),
            "dropped_nan": dropped,
        },
        "predictions": per_ticket,
        "config": {
            "run": run,
            "n": n,
            "split": split,
            "seed": seed,
            "model": settings.chat_model,
            "judge": "deepeval.models.OllamaModel (native)",
            "deepeval_version": _deepeval_version(),
        },
        "project_root": project_root,
    }


def _deepeval_version() -> str:
    try:
        import deepeval

        return getattr(deepeval, "__version__", "unknown")
    except Exception:  # noqa: BLE001
        return "unknown"


@app.command()
def deepeval(  # noqa: PLR0913
    run: str = typer.Option("answer_v1"),
    n: int = typer.Option(30),
    split: str = typer.Option("test", help="test | all"),
    seed: int = typer.Option(0),
    project_root: Path = typer.Option(Path("."), show_default=False),
) -> None:
    core = _deepeval_core(run=run, n=n, split=split, seed=seed, project_root=project_root)
    path = write_metrics(**core)
    typer.echo(f"wrote {path}")


# ---------------------------------------------------------------------------
# evaluator agreement (chapter 08b; pure -- no LLM calls)
# ---------------------------------------------------------------------------


def _agreement_core(
    run: str,
    n: int,
    seed: int,
    n_boot: int,
    project_root: Path,
) -> dict:
    """Agreement of RAGAS faithfulness, DeepEval faithfulness and ch-04
    embedding cosine similarity vs the ch-03 gold pass label and vs the
    ch-05 overall verdict, on the ``n`` common test-split tickets.

    Data sources (all already produced in earlier chapters):
    - RAGAS per-item  : ``runs/08_ragas_<run>/predictions.jsonl`` (no ticket_id;
      aligned positionally to the first-``n`` test ids in
      ``runs/05_judge_overall`` -- same order the RAGAS command used).
    - DeepEval per-item: ``runs/08_deepeval_<run>/predictions.jsonl`` (has ticket_id).
    - ch-04 cosine + ch-03 label: ``runs/04_similarity_<run>/predictions.jsonl``.
    - ch-05 overall verdict: ``runs/05_judge_overall/predictions.jsonl`` (test split).
    """
    project_root = Path(project_root)
    runs = _runs_dir(project_root)
    ragas_rows = _load_jsonl(runs / f"08_ragas_{run}" / "predictions.jsonl")
    deepeval_rows = _load_jsonl(runs / f"08_deepeval_{run}" / "predictions.jsonl")
    sim_rows = _load_jsonl(runs / f"04_similarity_{run}" / "predictions.jsonl")
    overall_rows = _load_jsonl(runs / f"05_judge_overall" / "predictions.jsonl")

    first_n_test = _split_ticket_ids(
        _predictions_path_for(run, project_root), split="test"
    )[:n]
    ragas_map = {r.get("ticket_id"): r for r in ragas_rows}
    deepeval_map = {r["ticket_id"]: r for r in deepeval_rows if r.get("ticket_id")}
    sim_map = {r["ticket_id"]: r for r in sim_rows if r.get("ticket_id")}
    overall_map = {r["ticket_id"]: r for r in overall_rows if r.get("ticket_id")}

    # RAGAS rows carry no ticket_id; align positionally with first_n_test.
    # _ragas_core skipped tickets missing ticket/trace, so positional alignment
    # is exact when all tickets exist in both files (which is the case here).
    aligned_ragas = ragas_rows[: len(first_n_test)]

    rows: list[dict] = []
    for i, tid in enumerate(first_n_test):
        if i >= len(aligned_ragas):
            continue
        r_ragas = aligned_ragas[i].get("faithfulness")
        r_deepeval = deepeval_map.get(tid, {}).get("faithfulness")
        emb = sim_map.get(tid, {}).get("embed_cosine")
        label = sim_map.get(tid, {}).get("pass")
        verdict = overall_map.get(tid, {}).get("pred_pass")
        if None in (r_ragas, r_deepeval, emb, label, verdict):
            continue
        if isinstance(r_ragas, float) and math.isnan(r_ragas):
            continue
        if isinstance(r_deepeval, float) and math.isnan(r_deepeval):
            continue
        rows.append(
            {
                "ticket_id": tid,
                "ragas_faithfulness": float(r_ragas),
                "deepeval_faithfulness": float(r_deepeval),
                "embed_cosine": float(emb),
                "pass_label": int(bool(label)),
                "pred_pass": int(bool(verdict)),
            }
        )

    n_tickets = len(rows)
    if n_tickets < 3:
        return {
            "experiment": "08_agreement_metrics",
            "chapter": 8,
            "n": 0,
            "metrics": {},
            "ci": {},
            "llm_calls": 0,
            "seconds": 0.0,
            "details": {
                "primary": "auroc_ragas_faithfulness_vs_label",
                "notes": f"only {n_tickets} common tickets (need >=3); cannot compute",
            },
            "predictions": rows,
            "config": {"run": run, "n": n, "seed": seed},
            "project_root": project_root,
        }

    rag = [r["ragas_faithfulness"] for r in rows]
    dep = [r["deepeval_faithfulness"] for r in rows]
    emd = [r["embed_cosine"] for r in rows]
    lab = [r["pass_label"] for r in rows]
    pred = [r["pred_pass"] for r in rows]

    metrics = {
        "spearman_ragas_vs_deepeval": spearman(rag, dep),
        "spearman_ragas_vs_embed": spearman(rag, emd),
        "spearman_deepeval_vs_embed": spearman(dep, emd),
        "auroc_ragas_faithfulness_vs_label": auroc(rag, lab),
        "auroc_deepeval_faithfulness_vs_label": auroc(dep, lab),
        "auroc_embed_cosine_vs_label": auroc(emd, lab),
        "auroc_ragas_faithfulness_vs_verdict": auroc(rag, pred),
        "auroc_deepeval_faithfulness_vs_verdict": auroc(dep, pred),
        "auroc_embed_cosine_vs_verdict": auroc(emd, pred),
    }

    def _bootstrap(metric_key: str) -> list[float]:
        vals: list[float] = []
        rng = np.random.default_rng(seed)
        idxs = np.arange(n_tickets)
        for _ in range(n_boot):
            samp = rng.choice(n_tickets, size=n_tickets, replace=True)
            if len(set(int(x) for x in samp)) < 2:
                continue
            s1 = [rag[i] for i in samp]
            s2 = [dep[i] for i in samp]
            s3 = [emd[i] for i in samp]
            l1 = [lab[i] for i in samp]
            p1 = [pred[i] for i in samp]
            if metric_key == "spearman_ragas_vs_deepeval":
                vals.append(spearman(s1, s2))
            elif metric_key == "spearman_ragas_vs_embed":
                vals.append(spearman(s1, s3))
            elif metric_key == "spearman_deepeval_vs_embed":
                vals.append(spearman(s2, s3))
            elif metric_key == "auroc_ragas_faithfulness_vs_label":
                vals.append(auroc(s1, l1))
            elif metric_key == "auroc_deepeval_faithfulness_vs_label":
                vals.append(auroc(s2, l1))
            elif metric_key == "auroc_embed_cosine_vs_label":
                vals.append(auroc(s3, l1))
            elif metric_key == "auroc_ragas_faithfulness_vs_verdict":
                vals.append(auroc(s1, p1))
            elif metric_key == "auroc_deepeval_faithfulness_vs_verdict":
                vals.append(auroc(s2, p1))
            elif metric_key == "auroc_embed_cosine_vs_verdict":
                vals.append(auroc(s3, p1))
        if len(vals) < 2:
            return [metrics[metric_key], metrics[metric_key]]
        lo = float(np.percentile(vals, 2.5))
        hi = float(np.percentile(vals, 97.5))
        return [lo, hi]

    ci: dict[str, list[float]] = {k: _bootstrap(k) for k in metrics}

    return {
        "experiment": "08_agreement_metrics",
        "chapter": 8,
        "n": n_tickets,
        "metrics": metrics,
        "ci": ci,
        "llm_calls": 0,
        "seconds": 0.0,
        "details": {
            "primary": "auroc_ragas_faithfulness_vs_label",
            "notes": (
                "Evaluator agreement: Spearman between RAGAS/DeepEval faithfulness "
                "and ch-04 embedding cosine, plus AUROC of each against the ch-03 "
                "gold pass label and the ch-05 overall verdict. Pure, no LLM calls."
            ),
        },
        "predictions": rows,
        "config": {
            "run": run,
            "n": n,
            "seed": seed,
            "n_boot": n_boot,
            "ragas_experiment": f"08_ragas_{run}",
            "deepeval_experiment": f"08_deepeval_{run}",
            "label_source": "runs/04_similarity_answer_v1 (ch-03 label)",
            "verdict_source": "runs/05_judge_overall (ch-05 overall)",
        },
        "project_root": project_root,
    }


@app.command()
def agreement(  # noqa: PLR0913
    run: str = typer.Option("answer_v1"),
    n: int = typer.Option(30),
    seed: int = typer.Option(0),
    n_boot: int = typer.Option(500),
    project_root: Path = typer.Option(Path("."), show_default=False),
) -> None:
    core = _agreement_core(run=run, n=n, seed=seed, n_boot=n_boot, project_root=project_root)
    path = write_metrics(**core)
    typer.echo(f"wrote {path}")


@app.command()
def all(run: str = typer.Option("answer_v1"), n: int = typer.Option(30)) -> None:
    core = _retrieval_core(run=run, kmax=5, n_boot=200, seed=0, project_root=Path("."))
    write_metrics(**core)
    core = _ragas_core(run=run, n=n, split="test", seed=0, project_root=Path("."))
    write_metrics(**core)
    core = _deepeval_core(run=run, n=n, split="test", seed=0, project_root=Path("."))
    write_metrics(**core)
    core = _agreement_core(run=run, n=n, seed=0, n_boot=500, project_root=Path("."))
    write_metrics(**core)
    typer.echo("done: 08_retrieval_* + 08_ragas_* + 08_deepeval_* + 08_agreement_metrics")


if __name__ == "__main__":
    app()
