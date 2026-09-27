"""Chapter 12: Inspect-AI task runners and results collector.

Two commands run the Inspect tasks (both against the cached Ollama client, so
a re-run costs zero fresh LLM calls), and a third reads those logs back,
reconciles them against the chapter-05/11 baselines and writes the shared
results entries:

    uv run python -m evals_tutorial.inspect_run helpdesk   # 60 test tickets
    uv run python -m evals_tutorial.inspect_run gsm8k      # 50 questions
    uv run python -m evals_tutorial.inspect_run collect    # metrics + reconcile

Both runs land under ``runs/12_inspect/logs/`` (Inspect ``.eval`` logs), and
``collect`` writes:

* ``runs/12_inspect_helpdesk_v1/metrics.json`` (+ ``predictions.jsonl``, ``config.json``)
* ``runs/12_inspect_gsm8k_qwen3.8:27b/metrics.json`` (+ the same two)
* ``runs/12_reconcile.md`` -- per-item compare vs chapters 05 & 11
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import typer
from inspect_ai import eval
from inspect_ai.log import read_eval_log
from inspect_ai.log._log import EvalLog

from . import judge
from .config import settings
from .inspect_tasks import (
    cached_model,
    gsm8k_task,
    helpdesk_task,
)
from .labels import load_labels
from .llm import usage_log
from .results import write_metrics
from .stats import bootstrap_ci

app = typer.Typer(help=__doc__, add_completion=False)

LOGS_DIR = settings.path("runs") / "12_inspect" / "logs"

HEXPERIMENT_HELPDESK = "12_inspect_helpdesk_v1"
HEXPERIMENT_GSM8K = f"12_inspect_gsm8k_{settings.chat_model}"


# ---------------------------------------------------------------------------
# runners (0 fresh LLM calls: every call is a cache hit)
# ---------------------------------------------------------------------------


def _eval_log(task_fragment: str) -> EvalLog:
    """Locate the most recent Inspect ``.eval`` log for a task name fragment."""
    import re

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    pattern = re.compile(re.escape(task_fragment).replace(re.escape("_"), "[-_]"))
    candidates = [p for p in LOGS_DIR.glob("*.eval") if pattern.search(p.name)]
    if not candidates:
        raise SystemExit(
            f"No Inspect log matching '{task_fragment}' in {LOGS_DIR}; "
            f"run `just inspect-helpdesk` / `just inspect-gsm8k` first."
        )
    latest = max(candidates, key=lambda p: p.stat().st_mtime)
    data = read_eval_log(str(latest))
    return data[0] if isinstance(data, list) else data


@app.command("helpdesk")
def helpdesk_cmd() -> None:
    """Run chapter 05's flow (60 test tickets) as an Inspect-AI Task."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    before = dict(usage_log)
    started = time.monotonic()
    d = eval(
        helpdesk_task(),
        model=cached_model(),
        log_dir=str(LOGS_DIR),
        log_level="error",
    )
    seconds = time.monotonic() - started
    calls = usage_log["misses"] - before["misses"]
    hits = usage_log["hits"] - before["hits"]
    path = d.log_file if hasattr(d, "log_file") else ""
    print(
        f"helpdesk: {seconds:.1f}s (fresh LLM calls: {calls}, cache hits: {hits}) -> {LOGS_DIR}"
    )


@app.command("gsm8k")
def gsm8k_cmd(
    limit: int = typer.Option(50, help="max items (ch-11 used 50)"),
) -> None:
    """Run chapter 11's GSM8K plain-prompt run (50 questions) as an Inspect Task."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    before = dict(usage_log)
    started = time.monotonic()
    d = eval(
        gsm8k_task(limit=limit),
        model=cached_model(),
        log_dir=str(LOGS_DIR),
        log_level="error",
    )
    seconds = time.monotonic() - started
    calls = usage_log["misses"] - before["misses"]
    hits = usage_log["hits"] - before["hits"]
    print(
        f"gsm8k: {seconds:.1f}s (fresh LLM calls: {calls}, cache hits: {hits}) -> {LOGS_DIR}"
    )


# ---------------------------------------------------------------------------
# collect: read the logs, reconcile vs chapter 05/11, write metrics + report
# ---------------------------------------------------------------------------


def _read_old05() -> tuple[dict[str, dict], dict]:
    """Chapter 05's frozen per-ticket rows and metrics.json."""
    exp = settings.path("runs") / "05_judge_overall"
    rows = [json.loads(l) for l in (exp / "predictions.jsonl").read_text().splitlines() if l.strip()]
    by_id = {r["ticket_id"]: r for r in rows}
    meta = json.loads((exp / "metrics.json").read_text())
    return by_id, meta


def _read_old11() -> tuple[dict[str, dict], dict]:
    """Chapter 11's frozen per-question rows and metrics.json.

    The Inspect gsm8k task re-runs chapter 11's **plain-prompt** variant, so the
    comparison baseline is `11_gsm8k_plain_<model>` (not the 5-shot harness run).
    That folder's rows have no `doc_id`, only `question`, so we recover the id by
    matching each plain question to the `doc_id`-carrying harness rows.
    """
    model = settings.chat_model
    plain_dir = settings.path("runs") / f"11_gsm8k_plain_{model}"
    plain_rows = [
        json.loads(l) for l in (plain_dir / "predictions.jsonl").read_text().splitlines() if l.strip()
    ]
    meta = json.loads((plain_dir / "metrics.json").read_text())

    harness_dir = settings.path("runs") / f"11_gsm8k_{model}"
    q2id: dict[str, str] = {}
    if (harness_dir / "predictions.jsonl").exists():
        for r in (
            json.loads(l)
            for l in (harness_dir / "predictions.jsonl").read_text().splitlines()
            if l.strip()
        ):
            q2id[r["question"]] = str(r["doc_id"])

    by_id: dict[str, dict] = {}
    for i, r in enumerate(plain_rows):
        key = q2id.get(r["question"], str(i))
        by_id[key] = r
    return by_id, meta


def _is_yes(v: object) -> bool:
    return v in (True, 1, 1.0)


def _collect_helpdesk(log: EvalLog) -> dict:
    old_rows, old_meta = _read_old05()
    labels = {r["ticket_id"]: r for r in load_labels("answer_v1")}
    pred_rows: list[dict] = []
    judge_vals: list[float] = []
    code_vals: list[float] = []
    inc_vals: list[float] = []
    for s in sorted(log.samples, key=lambda x: x.id):
        scores = s.scores or {}
        jg = scores.get("judge_grade")
        cc = scores.get("code_checks")
        inc = scores.get("includes")
        if jg is None:
            continue
        failed_meta = list((jg.metadata or {}).get("failed", []))
        pred_pass = len(failed_meta) == 0
        true_pass = bool(labels.get(s.id, {}).get("pass", True))
        judge_vals.append(1.0 if pred_pass else 0.0)
        code_vals.append(float(cc.value) if cc is not None and cc.value is not None else 0.0)
        inc_vals.append(1.0 if (inc is not None and inc.value == "C") else 0.0)
        pred_rows.append(
            {
                "ticket_id": s.id,
                "true_pass": true_pass,
                "pred_pass": pred_pass,
                "failed_modes": failed_meta,
                "code_checks_pass_rate": (round(float(cc.value), 4) if cc is not None and cc.value is not None else None),
                "includes_hit": (inc is not None and inc.value == "C"),
                "agreement": (true_pass == pred_pass),
                "reply": (jg.answer or "")[:400],
                "gold": (s.metadata or {}).get("gold", {}),
            }
        )

    n = len(pred_rows)

    def _kappa(rows: list[dict]) -> float:
        """Cohen's kappa, positive class = fail (chapter 05's exactly)."""
        if not rows:
            return 0.0
        y_true = [not r["true_pass"] for r in rows]
        y_pred = [not r["pred_pass"] for r in rows]
        return judge.cohen_kappa(y_true, y_pred)

    agree_vals = [1.0 if r["agreement"] else 0.0 for r in pred_rows]
    ci_acc = list(bootstrap_ci(agree_vals)) if n else [0.0, 0.0]
    ci_pr = list(bootstrap_ci(judge_vals)) if n else [0.0, 0.0]
    ci_code = list(bootstrap_ci(code_vals)) if n else [0.0, 0.0]
    ci_inc = list(bootstrap_ci(inc_vals)) if n else [0.0, 0.0]
    # kappa is a paired statistic (true_pass, pred_pass): resample rows, not scalars.
    def _row_kappa(idx) -> float:
        return _kappa([pred_rows[int(i)] for i in idx])

    import numpy as _np

    if n:
        rng = _np.random.default_rng(0)
        kappa_boot = sorted(
            _row_kappa(rng.integers(0, n, size=n)) for _ in range(2000)
        )

        lo = kappa_boot[max(int(0.025 * len(kappa_boot)), 0)]
        hi = kappa_boot[min(int(0.975 * len(kappa_boot)), len(kappa_boot) - 1)]
    else:
        lo = hi = 0.0

    # `pass_rate` (primary, spec) = mean(pred_pass): the model-graded scorer's score rate.
    # `accuracy` matches chapter-05's definition: mean(true_pass == pred_pass).
    acc = sum(1 for r in pred_rows if r["agreement"]) / n if n else 0.0
    pass_rate = sum(judge_vals) / n if n else 0.0

    metrics = {
        "pass_rate": pass_rate,
        "accuracy": acc,
        "kappa": _kappa(pred_rows),
        "code_checks_mean": sum(code_vals) / n if n else 0.0,
        "includes_hit_rate": sum(inc_vals) / n if n else 0.0,
    }
    ci = {
        "pass_rate": ci_pr,
        "accuracy": ci_acc,
        "kappa": [round(lo, 4), round(hi, 4)],
        "code_checks_mean": ci_code,
        "includes_hit_rate": ci_inc,
    }

    write_metrics(
        experiment=HEXPERIMENT_HELPDESK,
        chapter="12",
        n=n,
        metrics=metrics,
        ci=ci,
        details={
            "primary": "pass_rate",
            "harness": "inspect_ai",
            "model": settings.chat_model,
            "task": "helpdesk_answer[test:v1]",
            "note": "Inspect-AI re-run of chapter 05 (frozen answer_v1); primary = pass_rate (mean of the judge_grade scorer pass verdicts); kappa (positive=fail) + accuracy match ch-05's definitions",
        },
        predictions=pred_rows,
        config={
            "harness": "inspect_ai",
            "inspect_ai_version": getattr(getattr(log, "eval", None), "packages", {}).get("inspect_ai", ""),
            "model": settings.chat_model,
            "modes": judge.tracked_modes(),
            "judge_versions": {m: judge.chosen_version(m) for m in judge.tracked_modes()},
        },
    )
    return {
        "log": log,
        "meta": metrics,
        "ci": ci,
        "rows": pred_rows,
        "old_rows": old_rows,
    }


def _collect_gsm8k(log: EvalLog) -> dict:
    old_rows, old_meta = _read_old11()
    rows: list[dict] = []
    vals: list[float] = []
    for s in sorted(log.samples, key=lambda x: x.id):
        scores = s.scores or {}
        if not scores:
            continue
        sc = next(iter(scores.values()))
        ok = sc.value == "C"
        vals.append(1.0 if ok else 0.0)
        gold = (s.metadata or {}).get("gold")
        out_text = (sc.answer or "")[:300]
        old = old_rows.get(str(s.id))
        ch11_correct = _is_yes(old.get("correct")) if old else None
        rows.append(
            {
                "doc_id": s.id,
                "gold": gold,
                "correct": int(ok),
                "ch11_correct": int(ch11_correct) if ch11_correct is not None else None,
                "agreement": (ok == ch11_correct) if ch11_correct is not None else None,
                "output": out_text,
            }
        )
    n = len(rows)
    acc = sum(vals) / n if n else 0.0
    n_disagree = sum(1 for r in rows if r["agreement"] is False)
    ci_acc = list(bootstrap_ci(vals)) if n else [0.0, 0.0]
    metrics = {
        "accuracy": acc,
        "agreement_with_ch11": (n - n_disagree) / n if n else 0.0,
    }
    write_metrics(
        experiment=HEXPERIMENT_GSM8K,
        chapter="12",
        n=n,
        metrics=metrics,
        ci={"accuracy": ci_acc, "agreement_with_ch11": [0.0, 1.0] if n else [0.0, 0.0]},
        details={
            "primary": "accuracy",
            "harness": "inspect_ai",
            "model": settings.chat_model,
            "task": f"gsm8k[{len(rows)}]",
            "note": "Inspect-AI re-run of chapter 11 (plain prompt); scorer = match(location='end', numeric=True); target = gold number",
        },
        predictions=rows,
        config={
            "harness": "inspect_ai",
            "inspect_ai_version": getattr(getattr(log, "eval", None), "packages", {}).get("inspect_ai", ""),
            "model": settings.chat_model,
        },
    )
    return {
        "log": log,
        "meta": metrics,
        "ci": {"accuracy": ci_acc},
        "rows": rows,
        "old_rows": old_rows,
    }


def _fmt(v: float | None, nd: int = 4) -> str:
    if v is None:
        return "—"
    if isinstance(v, bool):
        return "yes" if v else "no"
    return f"{v:.{nd}f}"


def _write_reconcile(h: dict, g: dict) -> Path:
    out_path = settings.path("runs") / "12_reconcile.md"
    h_old, g_old = h["old_rows"], g["old_rows"]
    h_meta, g_meta = h["meta"], g["meta"]
    _, old05_meta = _read_old05()
    _, old11_meta = _read_old11()

    lines = [
        "# Chapter 12 — Inspect-AI re-run of chapters 05 and 11",
        "",
        "Both run in Inspect-AI on the **cached Ollama client** (0 fresh LLM calls),",
        "with the **same** prompt files, labels and scorer composition as the chapter",
        "baselines — so the only variable is the harness around the model.",
        "",
        "## 1) helpdesk (chapter 05)",
        "",
        "| metric | chapter 05 | Inspect | agree? |",
        "|---|---|---|---|",
        f"| pass_rate (primary) | — | **{_fmt(h_meta['pass_rate'])}** | — |",
        f"| accuracy | {_fmt(old05_meta['metrics'].get('accuracy'))} | **{_fmt(h_meta['accuracy'])}** | {'yes' if abs(h_meta['accuracy'] - old05_meta['metrics'].get('accuracy', 0)) < 1e-6 else '**NO**'} |",
        f"| kappa (positive=fail) | **{_fmt(old05_meta['metrics'].get('kappa'))}** | **{_fmt(h_meta['kappa'])}** | {'yes' if abs(h_meta['kappa'] - old05_meta['metrics'].get('kappa', 0)) < 1e-6 else '**NO**'} |",
        f"| code_checks mean | — | {_fmt(h_meta['code_checks_mean'])} | — |",
        f"| includes hit rate | — | {_fmt(h_meta['includes_hit_rate'])} | — |",
        "",
        "Per-item (chapter 05 `pred_pass` vs Inspect `judge_grade` verdict):",
        "",
        "| ticket | ch-05 pred | Inspect pred | agree? | ch-05 failed | Inspect failed |",
        "|---|---|---|---|---|---|",
    ]
    for r in sorted(h["rows"], key=lambda r: r["ticket_id"]):
        old = h_old.get(r["ticket_id"], {})
        h_failed = ", ".join(r["failed_modes"]) or "—"
        o_failed = ", ".join(sorted((old.get("mode_fails") or {}).keys())) or "—"
        agree = _is_yes(old.get("pred_pass")) == _is_yes(r["pred_pass"])
        lines.append(
            f"| {r['ticket_id']} | {'yes' if old.get('pred_pass') else 'no'} | {'yes' if r['pred_pass'] else 'no'} | "
            f"{'yes' if agree else '**NO**'} | {o_failed} | {h_failed} |"
        )

    h_dis = sum(
        1
        for r in h["rows"]
        if r["ticket_id"] in h_old
        and _is_yes(h_old[r["ticket_id"]].get("pred_pass")) != _is_yes(r["pred_pass"])
    )
    lines += [
        "",
        f"Disagreements: **{h_dis}** / {len(h['rows'])}.",
        "",
        "### 1.1) Interpretation",
        "",
        f"- Inspect's primary `pass_rate` = `{_fmt(h_meta['pass_rate'])}` (mean of per-ticket judge pass verdicts; ch-05 recorded accuracy/kappa instead).",
        f"- Inspect's `judge_grade` accuracy = `{_fmt(h_meta['accuracy'])}` vs ch-05 accuracy = `{_fmt(old05_meta['metrics'].get('accuracy'))}`.",
        f"- Inspect kappa (positive=fail) = `{_fmt(h_meta['kappa'])}` vs ch-05 kappa = `{_fmt(old05_meta['metrics'].get('kappa'))}`.",
        "- `code_checks_mean` = mean of ch-10's 6 deterministic checks (auxiliary).",
        "- `includes_hit_rate` = fraction where any ch-05 gold answer point appears (expected to be low: replies paraphrase).",
        "",
        "## 2) gsm8k (chapter 11)",
        "",
        "| metric | chapter 11 | Inspect | agree? |",
        "|---|---|---|---|",
        f"| accuracy | {_fmt(old11_meta['metrics'].get('exact_match'))} | **{_fmt(g_meta['accuracy'])}** | {'yes' if abs(g_meta['accuracy'] - old11_meta['metrics'].get('exact_match', 0)) < 1e-6 else '**NO**'} |",
        "",
        "Per-item (chapter 11 `correct` vs Inspect `match(location='end')`):",
        "",
        "| doc_id | ch-11 | gold | Inspect | agree? |",
        "|---|---|---|---|---|",
    ]
    for r in g["rows"]:
        old = g_old.get(str(r["doc_id"]), {})
        ch11 = _is_yes(old.get("correct")) if old else None
        ins = "yes" if r["correct"] else "no"
        if ch11 is None:
            ch11_s, agree_s = "—", "—"
        else:
            ch11_s = "yes" if ch11 else "no"
            agree_s = "yes" if ch11 == bool(r["correct"]) else "**NO**"
        lines.append(f"| {r['doc_id']} | {ch11_s} | {r['gold']} | {ins} | {agree_s} |")
    g_dis = sum(1 for r in g["rows"] if r["agreement"] is False)
    lines += [
        "",
        f"Disagreements: **{g_dis}** / {len(g['rows'])}.",
        "",
        "### 2.1) Interpretation",
        "",
        "- Both use the **same plain-prompt file** and the **same 50 questions**.",
        "- Scorer difference: ch-11's harness extracts the last `#### N` line; Inspect's `match(location='end', numeric=True)` pulls the last parseable number.",
    ]
    out_path.write_text("\n".join(lines) + "\n")
    return out_path


@app.command("collect")
def collect_cmd() -> None:
    """Read the Inspect logs, reconcile vs ch-05/11, and write the results table's entries."""
    helpdesk_results = _collect_helpdesk(_eval_log("helpdesk_answer"))
    gsm8k_results = _collect_gsm8k(_eval_log("gsm8k"))
    rep = _write_reconcile(helpdesk_results, gsm8k_results)
    from .results import build

    build()
    print(f"inspect-collect OK: {HEXPERIMENT_HELPDESK}, {HEXPERIMENT_GSM8K} -> {rep.name}; results.md rebuilt")


if __name__ == "__main__":
    app()
