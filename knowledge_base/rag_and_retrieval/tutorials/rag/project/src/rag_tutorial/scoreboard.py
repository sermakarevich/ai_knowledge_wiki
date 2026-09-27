"""Collect every `runs/*/metrics.json` into one Markdown table, `runs/scoreboard.md`.

Columns match `index.md`'s "Scoreboard columns" row exactly, so every chapter's
experiments are directly comparable. The three anchor rows (`0N_no_retrieval`,
`03_naive_rag`, `0N_oracle`) are bolded so they stand out as reference points.
"""

from __future__ import annotations

import json

import typer
from rich.console import Console

from rag_tutorial.config import settings

app = typer.Typer(add_completion=False)
console = Console()

RUNS_DIR = settings.path("runs")
SCOREBOARD_PATH = RUNS_DIR / "scoreboard.md"

_COLUMNS = [
    ("experiment", "experiment"),
    ("chapter", "chapter"),
    ("hit@5", "hit@5"),
    ("recall@5", "recall@5"),
    ("mrr", "MRR"),
    ("ndcg@10", "nDCG@10"),
    ("correctness", "correctness"),
    ("faithfulness", "faithfulness"),
    ("unanswerable_abstain", "unanswerable-abstain"),
    ("llm_calls_per_q", "LLM calls/q"),
    ("seconds_per_q", "s/q"),
]

# Experiment names that are anchors and get bolded on the scoreboard.
ANCHOR_NAMES = {"02_no_retrieval", "02_oracle", "03_naive_fixed_512_k5"}

NAIVE_BASELINE = "03_naive_fixed_512_k5"

# Technique family per experiment, for the "what helped most" ranking.
# Matched by longest-prefix first; anything unmatched is "other".
FAMILY_PREFIXES: list[tuple[str, str]] = [
    ("02_no_retrieval", "anchor"),
    ("02_oracle", "anchor"),
    ("03_naive", "anchor"),
    ("04_", "chunking"),
    ("05_bm25", "sparse"),
    ("05_dense_mmr", "diversity"),
    ("05_dense", "dense"),
    ("05_hybrid", "hybrid"),
    ("05_qdrant", "hybrid"),
    ("07_best_combo", "best-combo"),
    ("07_compress", "compression"),
    ("07_decompose", "query-transform"),
    ("07_hybrid_k20", "rerank"),
    ("07_hyde", "query-transform"),
    ("07_litm", "rerank"),
    ("07_multi_query", "query-transform"),
    ("07_step_back", "query-transform"),
    ("08_lc", "framework-langchain"),
    ("08_lg", "agentic"),
    ("09_li", "framework-llamaindex"),
    ("10_dspy", "dspy"),
    ("10_hs", "framework-haystack"),
    ("11_lightrag", "graph-lightrag"),
    ("11_raptor", "graph-raptor"),
    ("12_openwebui", "app"),
]

ANALYSIS_PATH = RUNS_DIR / "scoreboard_analysis.md"
QUALITY_LATENCY_PLOT = RUNS_DIR / "13_quality_vs_latency.png"
CALLS_PLOT = RUNS_DIR / "13_correctness_vs_calls.png"
RECALL_PLOT = RUNS_DIR / "13_recall_vs_correctness.png"
PERTYPE_PLOT = RUNS_DIR / "13_per_type_heatmap.png"


def family_of(experiment: str) -> str:
    """Map an experiment name to its technique family (longest-prefix match)."""
    best, best_len = "other", -1
    for prefix, family in FAMILY_PREFIXES:
        if experiment.startswith(prefix) and len(prefix) > best_len:
            best, best_len = family, len(prefix)
    return best


def pareto_frontier(rows: list[dict], quality: str = "correctness", cost: str = "seconds_per_q") -> list[dict]:
    """Runs no other run beats on BOTH quality (higher) and cost (lower).

    A row with missing quality/cost is skipped. Returned in descending
    quality order.
    """
    valid = [r for r in rows if r.get(quality) is not None and r.get(cost) is not None]
    frontier = []
    for cand in valid:
        dominated = any(
            other is not cand
            and (other[quality] or 0) >= (cand[quality] or 0)
            and (other[cost] or 0) <= (cand[cost] or 0)
            and ((other[quality] or 0) > (cand[quality] or 0) or (other[cost] or 0) < (cand[cost] or 0))
            for other in valid
        )
        if not dominated:
            frontier.append(cand)
    return sorted(frontier, key=lambda r: r[quality], reverse=True)


def family_deltas(rows: list[dict], baseline: str = NAIVE_BASELINE) -> list[dict]:
    """Per-family best correctness, its delta vs the naive baseline, and cost.

    One row per family: the family's max-correctness run, the delta
    (family best minus baseline correctness), and that run's seconds/question
    and LLM calls/question. Sorted by delta descending — the "what helped
    most per cost" ranking.
    """
    by_name = {r.get("experiment"): r for r in rows}
    base = by_name.get(baseline, {})
    base_c = base.get("correctness") or 0.0
    families: dict[str, list[dict]] = {}
    for row in rows:
        families.setdefault(family_of(row.get("experiment", "")), []).append(row)
    ranking = []
    for family, members in sorted(families.items()):
        scored = [m for m in members if m.get("correctness") is not None]
        if not scored:
            continue
        best = max(scored, key=lambda m: m["correctness"])
        ranking.append(
            {
                "family": family,
                "best_run": best.get("experiment"),
                "correctness": best.get("correctness"),
                "delta_vs_naive": round((best.get("correctness") or 0.0) - base_c, 3),
                "seconds_per_q": best.get("seconds_per_q"),
                "llm_calls_per_q": best.get("llm_calls_per_q"),
                "n_runs": len(members),
            }
        )
    return sorted(ranking, key=lambda r: r["delta_vs_naive"], reverse=True)


def per_type_table(top_runs: list[str] | None = None) -> dict[str, dict[str, float | None]]:
    """Mean correctness per question type for a few runs (heatmap input).

    Reads `predictions.jsonl` (which carries the judge verdict per question)
    and averages `correctness.score` by `type`. Unanswerable questions have no
    correctness score and are skipped.
    """
    import json as _json

    if top_runs is None:
        top_runs = [
            "03_naive_fixed_512_k5",
            "07_hybrid_k20_ce_bge_k5",
            "09_li_fusion_rerank",
            "10_dspy_zero_shot",
            "08_lg_crag",
            "11_lightrag_hybrid",
        ]
    table: dict[str, dict[str, float | None]] = {}
    for name in top_runs:
        path = RUNS_DIR / name / "predictions.jsonl"
        if not path.exists():
            continue
        by_type: dict[str, list[float]] = {}
        with path.open() as f:
            for line in f:
                if not line.strip():
                    continue
                pred = _json.loads(line)
                if not pred.get("correctness"):
                    continue
                by_type.setdefault(pred.get("type", "?"), []).append(float(pred["correctness"]["score"]))
        table[name] = {t: round(sum(v) / len(v), 3) for t, v in sorted(by_type.items())}
    return table


def render_analysis(rows: list[dict]) -> str:
    """Render `runs/scoreboard_analysis.md` from scoreboard rows (pure)."""
    ranking = family_deltas(rows)
    frontier = pareto_frontier(rows)
    per_type = per_type_table()
    lines = [
        "# Scoreboard analysis (all runs)",
        "",
        f"_{len(rows)} runs. Baseline for deltas: `{NAIVE_BASELINE}`._",
        "",
        "## What helped most (best run per technique family, ranked by gain)",
        "",
        "| family | best run | correctness | delta vs naive | s/q | LLM calls/q | n runs |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in ranking:
        lines.append(
            f"| {r['family']} | {r['best_run']} | {_fmt(r['correctness'])} | "
            f"{r['delta_vs_naive']:+.3f} | {_fmt(r['seconds_per_q'])} | "
            f"{_fmt(r['llm_calls_per_q'])} | {r['n_runs']} |"
        )
    lines += [
        "",
        "## Pareto frontier (no other run is better on both quality and latency)",
        "",
        "| run | correctness | s/q |",
        "|---|---|---|",
    ]
    for r in frontier:
        lines.append(f"| {r.get('experiment')} | {_fmt(r.get('correctness'))} | {_fmt(r.get('seconds_per_q'))} |")
    lines += [
        "",
        "## Correctness by question type (selected runs)",
        "",
        "| run | " + " | ".join(sorted({t for per in per_type.values() for t in per})) + " |",
        "|" + "|".join(["---"] * (len({t for per in per_type.values() for t in per}) + 1)) + "|",
    ]
    for name, per in per_type.items():
        types = sorted({t for p in per_type.values() for t in p})
        lines.append("| " + name + " | " + " | ".join(_fmt(per.get(t)) for t in types) + " |")
    lines += [
        "",
        "## Plots",
        "",
        f"- Correctness vs seconds/question: `{QUALITY_LATENCY_PLOT.name}`",
        f"- Correctness vs LLM calls/question: `{CALLS_PLOT.name}`",
        f"- Recall@5 vs correctness: `{RECALL_PLOT.name}`",
        f"- Per-type heatmap: `{PERTYPE_PLOT.name}`",
        "",
    ]
    return "\n".join(lines)


def write_plots(rows: list[dict]) -> list[str]:
    """Write the four analysis plots (matplotlib, Agg backend). Returns paths."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plotted = [r for r in rows if r.get("correctness") is not None]
    written: list[str] = []

    def _scatter(xs_key: str, path, xlabel: str, logx: bool = False) -> None:
        fig, ax = plt.subplots(figsize=(10, 6))
        xs = [(r.get(xs_key) or 0) for r in plotted]
        ys = [r["correctness"] for r in plotted]
        ax.scatter(xs, ys, alpha=0.6)
        for r, x, y in zip(plotted, xs, ys):
            ax.annotate(str(r.get("experiment", "")).replace("_", " ")[:24], (x, y), fontsize=6, alpha=0.8)
        ax.set_xlabel(xlabel)
        ax.set_ylabel("correctness")
        if logx:
            ax.set_xscale("symlog", linthresh=0.01)
        fig.tight_layout()
        fig.savefig(path, dpi=100)
        plt.close(fig)
        written.append(str(path))

    _scatter("seconds_per_q", QUALITY_LATENCY_PLOT, "seconds / question", logx=True)
    _scatter("llm_calls_per_q", CALLS_PLOT, "LLM calls / question", logx=True)

    fig, ax = plt.subplots(figsize=(8, 6))
    rx = [r.get("recall@5") or 0 for r in plotted]
    ry = [r["correctness"] for r in plotted]
    ax.scatter(rx, ry, alpha=0.6)
    for r, x, y in zip(plotted, rx, ry):
        ax.annotate(str(r.get("experiment", ""))[:22], (x, y), fontsize=6, alpha=0.8)
    ax.set_xlabel("recall@5")
    ax.set_ylabel("correctness")
    fig.tight_layout()
    fig.savefig(RECALL_PLOT, dpi=100)
    plt.close(fig)
    written.append(str(RECALL_PLOT))

    per_type = per_type_table()
    if per_type:
        types = sorted({t for per in per_type.values() for t in per})
        names = list(per_type)
        data = [[per_type[n].get(t, float("nan")) for t in types] for n in names]
        fig, ax = plt.subplots(figsize=(9, max(3, len(names) * 0.55)))
        im = ax.imshow(data, vmin=0, vmax=1, aspect="auto")
        ax.set_xticks(range(len(types)), types, rotation=20, ha="right", fontsize=8)
        ax.set_yticks(range(len(names)), [n[:28] for n in names], fontsize=7)
        for i in range(len(names)):
            for j in range(len(types)):
                ax.text(j, i, f"{data[i][j]:.2f}", ha="center", va="center", fontsize=7)
        fig.colorbar(im, ax=ax, label="correctness")
        fig.tight_layout()
        fig.savefig(PERTYPE_PLOT, dpi=100)
        plt.close(fig)
        written.append(str(PERTYPE_PLOT))
    return written


@app.command()
def build() -> None:
    """Rebuild runs/scoreboard.md from every runs/*/metrics.json."""
    rows = load_all_metrics()
    markdown = render_scoreboard(rows)
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    SCOREBOARD_PATH.write_text(markdown)
    console.print(f"[green]wrote[/green] {SCOREBOARD_PATH} ({len(rows)} rows)")
    analysis = render_analysis(rows)
    ANALYSIS_PATH.write_text(analysis)
    console.print(f"[green]wrote[/green] {ANALYSIS_PATH}")
    for path in write_plots(rows):
        console.print(f"[green]wrote[/green] {path}")


def _fmt(value) -> str:
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)


def load_all_metrics() -> list[dict]:
    metrics = []
    if not RUNS_DIR.exists():
        return metrics
    for path in sorted(RUNS_DIR.glob("*/metrics.json")):
        row = json.loads(path.read_text())
        # Chapter-13 summaries (e.g. `13_long_context/metrics.json`) are not
        # scoreboard rows — only files with an `experiment` key count.
        if "experiment" not in row:
            continue
        metrics.append(row)
    return metrics


def render_scoreboard(rows: list[dict]) -> str:
    rows = sorted(rows, key=lambda r: (r.get("chapter", ""), r.get("experiment", "")))
    header = "| " + " | ".join(label for _key, label in _COLUMNS) + " |"
    sep = "|" + "|".join("---" for _ in _COLUMNS) + "|"
    lines = [header, sep]
    for row in rows:
        is_anchor = row.get("experiment") in ANCHOR_NAMES
        cells = []
        for key, _label in _COLUMNS:
            cell = _fmt(row.get(key))
            cells.append(f"**{cell}**" if is_anchor else cell)
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    app()
