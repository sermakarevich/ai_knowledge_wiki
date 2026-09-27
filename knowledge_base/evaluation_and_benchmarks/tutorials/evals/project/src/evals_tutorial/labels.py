"""Chapter 03: the label set — reference-aware grading, open coding, axial coding.

- `grade --run answer_v1`: for every trace, one `chat_json` call with the
  reference-aware rubric (`prompts/reference_grader_v1.txt`). The grader sees
  the gold answer points and the gold handbook sections — information the app
  itself never sees — which stands in for a human domain expert. Writes
  `data/labels/<run>.jsonl` with the contract from `index.md`:
  `ticket_id, pass, failure_modes, note` (+ the raw grader fields under
  `raw`). 80 calls, all cached.
- `grade --run triage_v1`: pure code — compare `category`/`priority`/
  `needs_escalation` against gold; no LLM.
- `code --run <run>`: prints the open-coding corpus — one note per failing
  trace — for the axial-coding step (cluster the notes into a failure
  taxonomy; the worker does the clustering BY HAND, never by LLM).
- `stats --run <run>`: pass rate, counts per failure mode, per topic and per
  scenario — Markdown tables.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import typer
from pydantic import BaseModel, Field
from rich.console import Console
from rich.table import Table

from evals_tutorial.config import settings
from evals_tutorial.handbook import handbook_dir
from evals_tutorial.helpdesk import PROMPTS_DIR, load_traces
from evals_tutorial.tickets import load_tickets

LABELS_DIR = Path("data") / "labels"
TRIAGE_FAILURE_MODES = ("wrong_category", "wrong_priority", "wrong_escalation")


class ReferenceGrade(BaseModel):
    """The reference-aware grader's verdict for one answer trace."""

    # `pass` is a Python keyword, so the attribute is `pass_` with JSON alias "pass".
    pass_: bool = Field(alias="pass", description="true only if every key fact is stated, every claim is supported, nothing is over-promised and the question is answered")
    missing_points: list[str] = Field(default_factory=list, description="key facts from the reference standard that are omitted or stated inaccurately")
    unsupported_claims: list[str] = Field(default_factory=list, description="claims in the reply the handbook sections do not support")
    wrong_tone_or_promise: bool = Field(description="true if the reply promises/implies something the handbook does not allow")
    did_not_answer: bool = Field(description="true if the reply does not answer the customer's actual question")
    note: str = Field(description="ONE short sentence describing the single most important problem (the open-coding note)")


def labels_path(run: str) -> Path:
    return settings.path(LABELS_DIR / f"{run}.jsonl")


def write_labels(rows: list[dict], run: str, path: Path | None = None) -> Path:
    if not rows:
        raise ValueError("no labels to write")
    path = path or labels_path(run)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return path


def load_labels(run: str) -> list[dict]:
    path = labels_path(run)
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _ticket_by_id() -> dict[str, dict]:
    return {t["id"]: t for t in load_tickets()}


def _handbook_text(section_id: str) -> str:
    path = handbook_dir() / f"{section_id}.md"
    return path.read_text().strip() if path.exists() else f"(no handbook text for {section_id})"


# -- answer grading (reference-aware, LLM) ------------------------------------


def grade_messages(trace: dict, ticket: dict) -> list[dict]:
    """System = the rubric prompt; user = ticket + reference standard + handbook + reply."""
    gold = ticket["gold"]
    points = "\n".join(f"- {p}" for p in gold["answer_points"])
    sections = "\n\n".join(f"### {sid}\n{_handbook_text(sid)}" for sid in gold["sections"])
    user = (
        f"Customer ticket:\n{trace['input']}\n\n"
        f"Reference standard — key facts a correct reply must convey:\n{points}\n\n"
        f"Handbook sections that cover this answer:\n{sections}\n\n"
        f"Assistant reply to grade:\n{trace['output']}\n"
    )
    system = (PROMPTS_DIR / "reference_grader_v1.txt").read_text()
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def grade_answer(run: str = "answer_v1", client=None) -> list[dict]:
    """Grade every `answer` trace with the reference-aware rubric and write the labels file."""
    if client is None:
        from evals_tutorial.llm import ollama

        client = ollama
    tickets = _ticket_by_id()
    rows: list[dict] = []
    for trace in load_traces(run):
        ticket = tickets[trace["ticket_id"]]
        g = client.chat_json(grade_messages(trace, ticket), ReferenceGrade, temperature=0.0)
        rows.append(
            {
                "ticket_id": trace["ticket_id"],
                "pass": bool(g.pass_),
                "failure_modes": [],  # filled in by the axial-coding step
                "note": g.note,
                "raw": {
                    "missing_points": g.missing_points,
                    "unsupported_claims": g.unsupported_claims,
                    "wrong_tone_or_promise": g.wrong_tone_or_promise,
                    "did_not_answer": g.did_not_answer,
                },
            }
        )
    write_labels(rows, run)
    n_fail = sum(1 for r in rows if not r["pass"])
    print(f"graded {len(rows)} traces for {run!r}: {len(rows) - n_fail} pass / {n_fail} fail -> {labels_path(run)}")
    return rows


# -- triage grading (pure code) -------------------------------------------------


def grade_triage(trace: dict, ticket: dict) -> dict:
    """Compare the triage prediction with gold: one mode per wrong field."""
    gold = ticket["gold"]
    out = trace["output"]
    problems: list[str] = []
    if out.get("category") != gold["category"]:
        problems.append(f"category: predicted {out.get('category')!r}, gold {gold['category']!r}")
    if out.get("priority") != gold["priority"]:
        problems.append(f"priority: predicted {out.get('priority')!r}, gold {gold['priority']!r}")
    if bool(out.get("needs_escalation")) != bool(gold["needs_escalation"]):
        problems.append(f"escalation: predicted {out.get('needs_escalation')!r}, gold {gold['needs_escalation']!r}")
    modes = [
        "wrong_category" if out.get("category") != gold["category"] else "",
        "wrong_priority" if out.get("priority") != gold["priority"] else "",
        "wrong_escalation" if bool(out.get("needs_escalation")) != bool(gold["needs_escalation"]) else "",
    ]
    note = "; ".join(problems) if problems else "category, priority and escalation all match gold"
    return {
        "ticket_id": trace["ticket_id"],
        "pass": not problems,
        "failure_modes": [m for m in modes if m],
        "note": note,
        "raw": {
            "predicted": {k: out.get(k) for k in ("category", "priority", "needs_escalation")},
            "gold": {k: gold[k] for k in ("category", "priority", "needs_escalation")},
            "reason": out.get("reason"),
        },
    }


def grade_triage_run(run: str = "triage_v1") -> list[dict]:
    """Grade every triage trace against gold — no LLM calls — and write the labels file."""
    tickets = _ticket_by_id()
    rows = [grade_triage(trace, tickets[trace["ticket_id"]]) for trace in load_traces(run)]
    write_labels(rows, run)
    n_fail = sum(1 for r in rows if not r["pass"])
    print(f"graded {len(rows)} traces for {run!r}: {len(rows) - n_fail} pass / {n_fail} fail -> {labels_path(run)}")
    return rows


# -- axial coding: show the open-coding corpus ----------------------------------


def failing_corpus(run: str = "answer_v1") -> list[dict]:
    """(ticket_id, note, raw) for every failing label, sorted by ticket_id."""
    return [
        {"ticket_id": r["ticket_id"], "note": r["note"], "raw": r.get("raw") or {}}
        for r in sorted(load_labels(run), key=lambda r: r["ticket_id"])
        if not r["pass"]
    ]


def apply_failure_modes(run: str, mapping: dict[str, list[str]], path: Path | None = None) -> list[dict]:
    """Set `failure_modes` on the labels file from a hand-built `ticket_id -> [mode ids]` map."""
    rows = load_labels(run)
    for row in rows:
        row["failure_modes"] = list(mapping.get(row["ticket_id"], []))
    write_labels(rows, run, path)
    return rows


# -- stats ----------------------------------------------------------------------


def _md_table(headers: list[str], rows: list[list[Any]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    out += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return "\n".join(out)


def stats(run: str = "answer_v1") -> dict[str, Any]:
    """Pass rate, per failure mode, per topic, per scenario — dict + printed Markdown."""
    tickets = _ticket_by_id()
    rows = load_labels(run)
    n = len(rows)
    n_pass = sum(1 for r in rows if r["pass"])

    by_mode: dict[str, int] = {}
    for r in rows:
        for m in r.get("failure_modes") or []:
            by_mode[m] = by_mode.get(m, 0) + 1

    groups: dict[str, dict[str, int]] = {}
    for key in ("topic", "scenario"):
        per: dict[str, dict[str, int]] = {}
        for r in rows:
            t = tickets[r["ticket_id"]]
            bucket = per.setdefault(t[key], {"pass": 0, "fail": 0})
            bucket["pass" if r["pass"] else "fail"] += 1
        groups[key] = {k: v for k, v in sorted(per.items())}

    doc = [
        f"# labels stats: {run}",
        f"n={n}  pass={n_pass}  fail={n - n_pass}  pass rate={n_pass / n:.1%}" if n else f"# labels stats: {run} (no labels)",
        "",
    ]
    if by_mode:
        doc += ["## per failure mode", _md_table(["failure_mode", "count"], [[m, by_mode[m]] for m in sorted(by_mode, key=by_mode.get, reverse=True)]), ""]
    for key in ("topic", "scenario"):
        if groups.get(key):
            doc += [f"## per {key}", _md_table([key, "pass", "fail", "pass rate"], [[k, v["pass"], v["fail"], f"{v['pass'] / (v['pass'] + v['fail']):.0%}"] for k, v in groups[key].items()]), ""]
    print("\n".join(doc))
    return {"n": n, "pass": n_pass, "fail": n - n_pass, "by_mode": by_mode, "groups": groups}


# -- CLI ------------------------------------------------------------------------


def grade_run(run: str, client=None) -> list[dict]:
    if run.startswith("triage"):
        return grade_triage_run(run)
    if run.startswith("answer"):
        return grade_answer(run, client=client)
    raise ValueError(f"unknown run {run!r} (expected an 'answer_v1' or 'triage_v1' run)")


app = typer.Typer(add_completion=False)


@app.command()
def grade(run: str = typer.Option("answer_v1")) -> None:
    """Grade all traces of a run (answer: reference-aware LLM; triage: pure code)."""
    grade_run(run)


@app.command()
def code(run: str = typer.Option("answer_v1")) -> None:
    """Print the open-coding corpus: one note per failing trace (read all of them, then cluster)."""
    corpus = failing_corpus(run)
    console = Console()
    table = Table(title=f"open coding — {len(corpus)} failing traces of {run}")
    table.add_column("ticket")
    table.add_column("note", overflow="fold")
    table.add_column("raw signals")
    for row in corpus:
        raw = row["raw"]
        signals = " ".join(
            part
            for part in [
                f"missing={raw['missing_points']}" if raw.get("missing_points") else "",
                f"unsupported={raw['unsupported_claims']}" if raw.get("unsupported_claims") else "",
                f"over-promise" if raw.get("wrong_tone_or_promise") else "",
                "did-not-answer" if raw.get("did_not_answer") else "",
                "; ".join(f"{k}={raw[k]}" for k in ("category", "priority", "escalation") if isinstance(raw.get(k), str) and "gold" in raw),
            ]
            if part
        ) or ("all match gold" if raw.get("predicted") else "-")
        table.add_row(row["ticket_id"], row["note"], signals)
    console.print(table)
    console.print("Cluster these notes into 4-7 failure modes and write data/labels/taxonomy.yaml (by hand).")


@app.command(name="stats")
def stats_cmd(run: str = typer.Option("answer_v1")) -> None:
    """Pass rate + counts per failure mode / topic / scenario (Markdown)."""
    stats(run)


if __name__ == "__main__":
    app()
