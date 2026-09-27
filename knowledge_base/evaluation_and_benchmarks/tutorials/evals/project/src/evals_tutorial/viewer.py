"""Chapter 03: a trace viewer built for *our* trace schema.

Two commands:
- `html --run answer_v1 [--out runs/viewer/answer_v1.html]` writes one static
  HTML page (no server, no JS framework, inline CSS) that lists every trace —
  ticket text, gold labels, retrieved sections with scores, the reply, latency
  and (when `data/labels/<run>.jsonl` exists) the label, failure modes and
  open-coding note. Traces are also grouped under a `<details>` panel per
  failure mode, which doubles as a keyboard-free filter.
- `show <ticket_id> --run answer_v1` renders one trace in the terminal with
  `rich` — the same fields, the same order.

Everything reads the files produced in chapter 02 (`runs/traces/` and
`data/tickets/tickets.jsonl`); nothing is re-run and no LLM is called here.
"""

from __future__ import annotations

import html as _html
import json
from pathlib import Path
from typing import Any

import typer
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from evals_tutorial.config import settings
from evals_tutorial.helpdesk import load_traces
from evals_tutorial.tickets import load_tickets

LABELS_DIR = Path("data") / "labels"

_CSS = """
body{font-family:ui-monospace,Menlo,Consolas,monospace;margin:24px;background:#fafafa;color:#1c1c1e}
h1{font-size:20px}h2{font-size:16px;margin:20px 0 8px}
.card{border:1px solid #d1d1d6;border-radius:8px;background:#fff;margin:12px 0;padding:12px 16px}
.card.pass{border-left:6px solid #30a14e}.card.fail{border-left:6px solid #e5484d}
.meta{color:#6e6e73;font-size:12px;margin-bottom:8px}
.label{display:inline-block;padding:1px 8px;border-radius:10px;font-size:12px;margin-right:6px}
.pass-l{background:#dcf5e3;color:#1a7f37}.fail-l{background:#ffe5e7;color:#a40e14}
.fmode{display:inline-block;background:#fff3d6;color:#8a5b00;padding:1px 8px;border-radius:10px;font-size:12px;margin:0 6px 4px 0}
.ticket,.reply{white-space:pre-wrap;background:#f4f4f5;border-radius:6px;padding:8px;margin:6px 0;font-size:13px}
.retrieved{font-size:12px;color:#444}table.gold{border-collapse:collapse;font-size:13px}table.gold td{padding:1px 12px 1px 0}
.note{color:#57606a;font-size:13px;font-style:italic}
details{margin:8px 0}summary{cursor:pointer;font-weight:600}
summary .count{color:#6e6e73;font-weight:400}
"""


def esc(text: Any) -> str:
    return _html.escape(str(text))


def load_labels(run: str) -> dict[str, dict]:
    """`ticket_id -> label row` from `data/labels/<run>.jsonl` (empty when missing)."""
    path = settings.path(LABELS_DIR / f"{run}.jsonl")
    if not path.exists():
        return {}
    return {row["ticket_id"]: row for row in (json.loads(line) for line in path.read_text().splitlines() if line.strip())}


def tickets_by_id() -> dict[str, dict]:
    return {t["id"]: t for t in load_tickets()}


def _triage_output(output: Any) -> str:
    """Render triage's dict output as `field=value` lines."""
    return "\n".join(f"{k}: {v}" for k, v in output.items())


def _card(trace: dict, ticket: dict | None, label: dict | None) -> str:
    out = trace["output"]
    body = (
        f'<div class="meta">run={esc(trace["run"])}  model={esc(trace.get("model"))}  '
        f'latency={trace.get("latency_s")}s</div>\n'
        f'<div class="ticket">{esc(trace["input"])}</div>\n'
    )
    gold = (ticket or {}).get("gold", {})
    if gold:
        body += "<table class=\"gold\"><tr><td>gold category</td><td>{}</td></tr><tr><td>gold priority</td><td>{}</td></tr>" "<tr><td>escalation</td><td>{}</td></tr><tr><td>sections</td><td>{}</td></tr>" "<tr><td>answer points</td><td>{}</td></tr></table>\n".format(
            esc(gold.get("category")),
            esc(gold.get("priority")),
            esc(gold.get("needs_escalation")),
            esc(", ".join(gold.get("sections", []))),
            esc("; ".join(gold.get("answer_points", []))),
        )
    retrieved = trace.get("retrieved") or []
    if retrieved:
        rows = "  ".join(f'{r["section"]} ({r["score"]:.3f})' for r in retrieved)
        body += f'<div class="retrieved">retrieved: {esc(rows)}</div>\n'
    body += f'<div class="reply">{esc(out if isinstance(out, str) else _triage_output(out))}</div>\n'
    if label is not None:
        cls = "pass" if label.get("pass") else "fail"
        modes = "".join(f'<span class="fmode">{esc(m)}</span>' for m in label.get("failure_modes", []))
        body += f'<p><span class="label {cls}-l">{cls}</span>{modes}</p>\n'
        if label.get("note"):
            body += f'<p class="note">{esc(label["note"])}</p>\n'
    return body, ("pass" if label and label.get("pass") else "fail") if label is not None else ""


def build_page(run: str) -> str:
    traces = load_traces(run)
    labels = load_labels(run)
    tickets = tickets_by_id()

    cards: list[str] = []
    by_mode: dict[str, list[str]] = {}
    n_pass = n_fail = 0
    for trace in traces:
        ticket = tickets.get(trace["ticket_id"])
        label = labels.get(trace["ticket_id"])
        body, state = _card(trace, ticket, label)
        if state == "pass":
            n_pass += 1
        elif state == "fail":
            n_fail += 1
        cards.append(f'<div class="card card-{state}" id="{esc(trace["ticket_id"])}"><h2>{esc(trace["ticket_id"])}</h2>{body}</div>')
        if label is not None:
            for mode in label.get("failure_modes") or ["_unclassified_fail"]:
                by_mode.setdefault(mode, []).append(f'<div><a href="#{esc(trace["ticket_id"])}">{esc(trace["ticket_id"])}</a></div>')

    if by_mode:
        groups = []
        for mode in sorted(by_mode):
            ids = by_mode[mode]
            groups.append(
                f'<details><summary>{esc(mode)} <span class="count">({len(ids)})</span></summary>'
                + "\n".join(ids)
                + "</details>"
            )
        filter_block = f"<h2>Filter by failure mode</h2>" + "\n".join(groups)
    else:
        filter_block = ""

    summary = f'<p>{len(traces)} traces; ' if not labels else f'<p>{len(traces)} traces — {n_pass} pass / {n_fail} fail; '
    summary += f'labels from <code>{esc(LABELS_DIR / (run + ".jsonl"))}</code></p>' if labels else "no labels file yet</p>"
    return (
        "<!doctype html><html><head><meta charset=\"utf-8\"><title>evals_tutorial traces — "
        f"{esc(run)}</title><style>{_CSS}</style></head><body>"
        f"<h1>traces: {esc(run)} {summary}</h1>{filter_block}<h2>All traces</h2>{'<div>' + chr(10).join(cards) + '</div>'}"
        "</body></html>"
    )


def _rich_trace(trace: dict, ticket: dict | None, label: dict | None) -> None:
    console = Console()
    head = Text()
    head.append(trace["ticket_id"], style="bold")
    gold = (ticket or {}).get("gold") or {}
    if gold:
        head.append(f"  topic={gold['category']}  scenario={ticket and ticket.get('scenario')}", style="dim")
    console.print(Panel(head, box=box.SIMPLE))
    table = Table(box=box.SIMPLE_HEAVY, show_header=False)
    table.add_column(style="bold", width=14)
    table.add_column()
    table.add_row("ticket", trace["input"])
    if gold:
        table.add_row("gold", f"category={gold['category']} priority={gold['priority']} esc={gold['needs_escalation']}\nsections={gold['sections']}\npoints={gold['answer_points']}")
    if trace.get("retrieved"):
        table.add_row("retrieved", "; ".join(f"{r['section']} ({r['score']:.3f})" for r in trace["retrieved"]))
    out = trace["output"]
    table.add_row("reply", out if isinstance(out, str) else json.dumps(out, indent=2))
    table.add_row("meta", f"model={trace.get('model')} latency={trace.get('latency_s')}s")
    console.print(table)
    if label is not None:
        style = "green" if label.get("pass") else "red"
        console.print(f"[{style}]{'PASS' if label.get('pass') else 'FAIL'}[/] modes={label.get('failure_modes')}")
        if label.get("note"):
            console.print(f"[italic]note: {label['note']}[/]")


app = typer.Typer(add_completion=False)


@app.command(name="html")
def html_cmd(
    run: str = typer.Option("answer_v1", help="trace run, e.g. answer_v1 or triage_v1"),
    out: Path | None = typer.Option(None, help="output .html path (default runs/viewer/<run>.html under the project)"),
) -> None:
    """Render every trace of a run to one static, self-contained HTML page."""
    out_path = out if out is not None else Path("runs") / "viewer" / f"{run}.html"
    if not out_path.is_absolute():
        out_path = settings.path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(build_page(run))
    print(f"{out_path.resolve()}")


@app.command(name="show")
def show_cmd(
    ticket_id: str,
    run: str = typer.Option("answer_v1", help="trace run, e.g. answer_v1 or triage_v1"),
) -> None:
    """Show one trace (ticket, gold, retrieved, reply, label) with rich."""
    traces = load_traces(run)
    match = next((t for t in traces if t["ticket_id"] == ticket_id), None)
    if match is None:
        raise typer.Exit(f"no trace {ticket_id!r} in run {run!r}")
    labels = load_labels(run)
    _rich_trace(match, tickets_by_id().get(ticket_id), labels.get(ticket_id))


if __name__ == "__main__":
    app()
