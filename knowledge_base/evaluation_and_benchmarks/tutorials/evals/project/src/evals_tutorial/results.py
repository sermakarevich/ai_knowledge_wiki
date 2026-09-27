"""Chapter 04: shared results plumbing every later chapter reuses.

- `write_metrics(...)` writes one experiment's numbers to
  `project/runs/<experiment>/{metrics.json, predictions.jsonl, config.json}`
  exactly per the `index.md` data contract.
- `build()` scans every `project/runs/*/metrics.json`, sorts by chapter then
  experiment, and rewrites `project/runs/results.md` as one Markdown table with
  the shared columns (`experiment | chapter | n | primary metric | 95 % CI |
   LLM calls | s/item | notes`). Idempotent and deterministic (no clock), so
   rebuilding from unchanged data leaves the file byte-identical.

No LLM calls, no new dependencies. The table's primary metric is the first
metric recorded for an experiment (its `details['primary']`), so each
experiment chooses what "the" number is (e.g. `f1_macro`, `all_checks_pass`,
`auroc_embed_vs_label`).
"""

from __future__ import annotations

import json
from pathlib import Path

import typer


def _runs_dir(project_root: Path | None = None) -> Path:
    from evals_tutorial.config import settings

    return (project_root or settings.project_root) / "runs"


def write_metrics(
    experiment: str,
    chapter: int | str,
    n: int,
    metrics: dict[str, float],
    ci: dict[str, list[float]] | None = None,
    llm_calls: int = 0,
    seconds: float = 0.0,
    details: dict | None = None,
    predictions: list[dict] | None = None,
    config: dict | None = None,
    project_root: Path | None = None,
    dir_name: str | None = None,
) -> Path:
    """Write `metrics.json`, `predictions.jsonl`, `config.json` for one experiment.

    `primary` (the first metric name) and `notes` (a short string) are recorded
    inside `details` so `build` can render the shared results table without
    re-deriving anything. `dir_name`, when given, overrides the folder name
    (which defaults to `experiment`). Returns the `metrics.json` path.
    """
    details = dict(details or {})
    primary = list(metrics.keys())[0] if metrics else ""
    details.setdefault("primary", primary)
    details.setdefault("notes", "")

    out_dir = _runs_dir(project_root) / (dir_name or experiment)
    out_dir.mkdir(parents=True, exist_ok=True)

    record = {
        "experiment": experiment,
        "chapter": chapter,
        "n": n,
        "metrics": metrics,
        "ci": ci or {},
        "llm_calls": llm_calls,
        "seconds": round(seconds, 3),
        "details": details,
    }
    (out_dir / "metrics.json").write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")

    pred_dir = out_dir
    with (pred_dir / "predictions.jsonl").open("w") as fh:
        for row in predictions or []:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    (out_dir / "config.json").write_text(json.dumps(config or {}, indent=2, ensure_ascii=False) + "\n")
    return out_dir / "metrics.json"


def load_record(path: Path) -> dict:
    return json.loads(path.read_text())


def iter_metrics(project_root: Path | None = None) -> list[dict]:
    """All `runs/*/metrics.json` records, sorted by chapter then experiment."""
    runs = _runs_dir(project_root)
    if not runs.exists():
        return []
    records = [load_record(p) for p in runs.glob("*/metrics.json")]
    records.sort(key=lambda r: (str(r.get("chapter", "")), r.get("experiment", "")))
    return records


def _format_ci(ci: dict | None, primary: str) -> str:
    if ci and primary in ci:
        lo, hi = ci[primary]
        return f"[{lo}, {hi}]"
    return "—"


def render_rows(records: list[dict]) -> tuple[str, list[str]]:
    """Return (header_line, data_lines) for the shared results table."""
    header = "experiment | chapter | n | primary metric | 95 % CI | LLM calls | s/item | notes"
    lines: list[str] = []
    for record in records:
        primary = record.get("details", {}).get("primary", "")
        primary_value = record.get("metrics", {}).get(primary, "")
        n = record.get("n", 0)
        seconds = record.get("seconds", 0.0)
        per_item = round(seconds / n, 3) if n else 0.0
        notes = record.get("details", {}).get("notes", "")
        lines.append(
            " | ".join(
                [
                    str(record.get("experiment", "")),
                    str(record.get("chapter", "")),
                    str(n),
                    str(primary_value),
                    _format_ci(record.get("ci"), primary),
                    str(record.get("llm_calls", 0)),
                    str(per_item),
                    notes,
                ]
            )
        )
    return header, lines


def build(project_root: Path | None = None) -> Path:
    """Scan `runs/*/metrics.json` and rewrite `runs/results.md`. Idempotent."""
    runs = _runs_dir(project_root)
    runs.mkdir(parents=True, exist_ok=True)
    records = iter_metrics(project_root)
    header, lines = render_rows(records)

    block = [
        "# Results",
        "",
        f"{len(records)} experiment(s)",
        "",
        header,
        "|---|---|---|---|---|---|---|---|",
        *lines,
        "",
    ]
    out = runs / "results.md"
    out.write_text("\n".join(block))
    return out


app = typer.Typer(add_completion=False)


@app.command(name="write")
def write_cmd(
    experiment: str = typer.Option(..., help="experiment id, e.g. 04_triage_v1"),
    chapter: str = typer.Option("04", help="chapter number"),
    n: int = typer.Option(0, help="rows evaluated (test split)"),
    metrics: str = typer.Option("{}", help="JSON object {name: value}; first key is primary"),
    ci: str = typer.Option("{}", help="JSON object {name: [lo, hi]}"),
    llm_calls: int = typer.Option(0),
    seconds: float = typer.Option(0.0),
    details: str = typer.Option("{}", help="JSON object; add 'notes' for the table"),
    predictions: str = typer.Option("[]", help="JSON list of rows for predictions.jsonl"),
    config: str = typer.Option("{}", help="JSON object for config.json"),
) -> None:
    """Write one experiment's metrics.json / predictions.jsonl / config.json."""
    path = write_metrics(
        experiment=experiment,
        chapter=chapter,
        n=n,
        metrics=json.loads(metrics),
        ci=json.loads(ci),
        llm_calls=llm_calls,
        seconds=seconds,
        details=json.loads(details),
        predictions=json.loads(predictions),
        config=json.loads(config),
    )
    print(f"wrote {path}")


@app.command(name="build")
def build_cmd() -> None:
    """Rewrite `runs/results.md` from every `runs/*/metrics.json`."""
    print(f"wrote {build()}")


if __name__ == "__main__":
    app()
