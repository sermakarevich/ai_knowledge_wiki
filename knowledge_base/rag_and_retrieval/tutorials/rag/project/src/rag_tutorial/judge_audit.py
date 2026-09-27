"""Judge reliability audit (chapter 13): correlation, human spot-check, stability, leak check.

Our whole scoreboard trusts one LLM judge (`evaluate.judge_correctness` /
`judge_faithfulness`) on one question set. This module checks that trust four
ways (LLM = large language model; judge = an LLM asked to grade an answer):

1. `correlate`: Spearman rank correlation (a number in [-1, 1] saying whether
   two scores rise and fall together) between our judges and the RAGAS second
   opinion (`runs/13_ragas.json`): correctness vs FactualCorrectness,
   faithfulness vs Faithfulness, per run and pooled.
2. `sample`: draw 25 (question, answer, judge verdict) items across runs into
   `runs/13_human_audit.jsonl` with empty `human_score`/`note` fields for a
   human (here: a solo automated pass by the tutorial author, not an
   independent reviewer) to fill in; `agreement` then compares.
3. `stability`: re-run our correctness judge with `seed` 1..3 on 20 items
   (temperature 0 should be nearly deterministic — measure it).
4. `leak`: for 10 golden questions, cosine similarity (embedding dot-product:
   high means similar wording) between the question and its evidence quote vs
   the question and a random chunk — synthetic questions often "leak" answer
   wording, which flatters dense retrieval.
"""

from __future__ import annotations

import json
import random
from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer(add_completion=False)
console = Console()


# -- pure helpers (unit-tested, no network) ------------------------------------


def _ranks(xs: list[float]) -> list[float]:
    """Average-tie ranks, 1-based."""
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    ranks = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def spearman(xs: list[float], ys: list[float]) -> float | None:
    """Spearman rank correlation, or None when undefined (<2 points or constant)."""
    pairs = [(x, y) for x, y in zip(xs, ys, strict=True) if x is not None and y is not None]
    if len(pairs) < 2:
        return None
    rx, ry = _ranks([p[0] for p in pairs]), _ranks([p[1] for p in pairs])
    n = len(pairs)
    mx, my = sum(rx) / n, sum(ry) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(rx, ry, strict=True))
    vx = sum((a - mx) ** 2 for a in rx)
    vy = sum((b - my) ** 2 for b in ry)
    if vx == 0 or vy == 0:
        return None
    return cov / (vx * vy) ** 0.5


def cosine(a: list[float], b: list[float]) -> float:
    """Cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    return dot / (na * nb) if na and nb else 0.0


def pareto_frontier(points: list[dict], x_key: str, y_key: str, x_lower_is_better: bool = True) -> list[str]:
    """Names of the non-dominated points (higher y, and lower-or-equal x, wins).

    A point is on the Pareto frontier (the set of runs no other run beats on
    *both* axes) if no other point is at least as good on both axes and
    strictly better on one.
    """
    front = []
    for i, cand in enumerate(points):
        dominated = False
        for j, other in enumerate(points):
            if i == j:
                continue
            x_better = other[x_key] <= cand[x_key] if x_lower_is_better else other[x_key] >= cand[x_key]
            y_better = other[y_key] >= cand[y_key]
            strictly = (other[x_key] != cand[x_key]) or (other[y_key] != cand[y_key])
            if x_better and y_better and strictly:
                dominated = True
                break
        if not dominated:
            front.append(cand["name"])
    return front


def agreement(human: list[float], machine: list[float], tol: float = 0.0) -> dict:
    """Agreement stats between two score lists: exact/tolerant match rate + MAE."""
    pairs = [(h, m) for h, m in zip(human, machine, strict=True) if h is not None and m is not None]
    if not pairs:
        return {"n": 0, "match_rate": None, "mae": None}
    match = sum(1 for h, m in pairs if abs(h - m) <= tol)
    mae = sum(abs(h - m) for h, m in pairs) / len(pairs)
    return {"n": len(pairs), "match_rate": match / len(pairs), "mae": mae}


def sample_audit_items(run_predictions: dict[str, list[dict]], n: int = 25, seed: int = 13) -> list[dict]:
    """Round-robin sample of n items across runs for the human spot-check."""
    rng = random.Random(seed)
    runs = sorted(run_predictions)
    pools = {r: [p for p in run_predictions[r] if p.get("correctness")] for r in runs}
    for pool in pools.values():
        rng.shuffle(pool)
    items, i = [], 0
    while len(items) < n and any(pools[r] for r in runs):
        run = runs[i % len(runs)]
        if pools[run]:
            pred = pools[run].pop()
            items.append(
                {
                    "run": run,
                    "id": pred["id"],
                    "type": pred.get("type"),
                    "question": pred["question"],
                    "answer": pred.get("answer", ""),
                    "judge_correctness": (pred.get("correctness") or {}).get("score"),
                    "judge_reason": (pred.get("correctness") or {}).get("reason", ""),
                    "human_score": None,
                    "note": "",
                }
            )
        i += 1
    return items


# -- live pieces (need Ollama / RAGAS output) ----------------------------------


def correlate(ragas_path=None) -> dict:
    """Spearman(ours vs RAGAS) per run + pooled; prints a Markdown table."""
    from rag_tutorial.config import settings

    path = ragas_path or settings.path("runs") / "13_ragas.json"
    data = json.loads(Path(path).read_text()) if isinstance(path, (str, Path)) else path
    table = []
    pool_c, pool_f, pool_rc, pool_rf = [], [], [], []
    for run, payload in data["runs"].items():
        c = [(e.get("ours_correctness"), e.get("FactualCorrectness")) for e in payload.get("items", [])]
        f = [(e.get("ours_faithfulness"), e.get("Faithfulness")) for e in payload.get("items", [])]
        pool_c += c
        pool_f += f
        table.append(
            {
                "run": run,
                "n": len(payload.get("items", [])),
                "spearman_correctness_vs_factual": spearman([a for a, _ in c], [b for _, b in c]),
                "spearman_faithfulness_vs_ragas": spearman([a for a, _ in f], [b for _, b in f]),
            }
        )
    pooled = {
        "run": "POOLED",
        "n": len(pool_c),
        "spearman_correctness_vs_factual": spearman([a for a, _ in pool_c], [b for _, b in pool_c]),
        "spearman_faithfulness_vs_ragas": spearman([a for a, _ in pool_f], [b for _, b in pool_f]),
    }
    return {"per_run": table, "pooled": pooled}


def stability(n_items: int = 20, seeds: tuple[int, ...] = (1, 2, 3)) -> dict:
    """Re-run `judge_correctness` with several seeds; count verdict flips.

    Each (question, seed) is a fresh LLM call (the cache key includes the
    seed), so this measures real temperature-0 determinism of `qwen3.8:27b`.
    """
    from rag_tutorial.config import settings
    from rag_tutorial.evaluate import judge_correctness
    from rag_tutorial.golden import QA_PATH, load_qa

    test_items = [i for i in load_qa(QA_PATH) if i["split"] == "test" and i["type"] != "unanswerable"][:n_items]
    run = settings.path("runs") / "07_best_combo" / "predictions.jsonl"
    answers = {json.loads(line)["id"]: json.loads(line)["answer"] for line in run.read_text().splitlines() if line.strip()}
    rows = []
    for item in test_items:
        scores = {}
        for seed in seeds:
            verdict = judge_correctness(item["question"], item["answer"], answers.get(item["id"], ""), seed=seed)
            scores[seed] = verdict["score"]
        rows.append({"id": item["id"], "scores": scores, "flipped": len(set(scores.values())) > 1})
    flips = sum(1 for r in rows if r["flipped"])
    return {"n_items": len(rows), "seeds": list(seeds), "n_flipped": flips, "flip_rate": flips / len(rows) if rows else None, "rows": rows}


def leak_check(n_questions: int = 10, seed: int = 13) -> dict:
    """Question↔evidence vs question↔random-chunk similarity (answers 'leak'?)."""
    import numpy as np

    from rag_tutorial.chunkers import fixed_token_chunks
    from rag_tutorial.golden import QA_PATH, load_documents, load_qa
    from rag_tutorial.llm import ollama

    rng = random.Random(seed)
    test_items = [i for i in load_qa(QA_PATH) if i["split"] == "test" and i["evidence"]]
    chosen = rng.sample(test_items, min(n_questions, len(test_items)))
    docs = load_documents()
    all_chunks = [c.text for doc in docs.values() for c in fixed_token_chunks(doc, size=512, overlap=64)]
    rows = []
    for item in chosen:
        quote = item["evidence"][0]["quote"]
        rand_chunk = rng.choice(all_chunks)
        vecs = ollama.embed([item["question"], quote, rand_chunk])
        rows.append(
            {
                "id": item["id"],
                "sim_question_evidence": round(cosine(vecs[0], vecs[1]), 3),
                "sim_question_random": round(cosine(vecs[0], vecs[2]), 3),
            }
        )
    for row in rows:
        row["leak_gap"] = round(row["sim_question_evidence"] - row["sim_question_random"], 3)
    arr_ev = np.mean([r["sim_question_evidence"] for r in rows])
    arr_rd = np.mean([r["sim_question_random"] for r in rows])
    return {"rows": rows, "mean_evidence": round(float(arr_ev), 3), "mean_random": round(float(arr_rd), 3)}


@app.command(name="correlate")
def correlate_cmd() -> None:
    """Print the ours-vs-RAGAS Spearman table."""
    out = correlate()
    for row in out["per_run"] + [out["pooled"]]:
        console.print(row)


@app.command()
def sample(n: int = 25, seed: int = 13) -> None:
    """Write runs/13_human_audit.jsonl (human_score/note left blank to fill)."""
    from rag_tutorial.config import settings
    from rag_tutorial.ragas_eval import REP_RUNS

    runs_dir = settings.path("runs")
    preds = {}
    for run in REP_RUNS:
        path = runs_dir / run / "predictions.jsonl"
        preds[run] = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    items = sample_audit_items(preds, n=n, seed=seed)
    out = runs_dir / "13_human_audit.jsonl"
    out.write_text("\n".join(json.dumps(i, ensure_ascii=False) for i in items) + "\n")
    console.print(f"[green]wrote[/green] {out} ({len(items)} items)")


@app.command(name="stability")
def stability_cmd(n_items: int = 20) -> None:
    """Re-run the judge with seeds 1..3 and report flips."""
    console.print(json.dumps(stability(n_items=n_items), indent=2))


@app.command()
def leak(n_questions: int = 10) -> None:
    """Report question↔evidence vs question↔random-chunk similarity."""
    console.print(json.dumps(leak_check(n_questions=n_questions), indent=2))


if __name__ == "__main__":
    app()
