"""Chapter 05: LLM-as-judge alignment — binary pass/fail per failure mode.

- `align`: for each tracked mode (the 4 with >= 4 fails in the committed
  labels: `missing_required_fact`, `unsupported_claim`,
  `wrong_section_retrieved`, `did_not_answer`), grade every *dev*-split
  ticket with variant v1 (zero-shot) and variant v2 (few-shot, 2 pass +
  2 fail worked examples drawn from the dev split) and pick the winner by
  Cohen's kappa against the ground-truth mode labels. The winner is
  recorded under `runs/05_judge_align/<mode>.json` so `run` can resolve
  `version=best` deterministically on the test split.
- `run`: grade the *test* split with the chosen version (or an explicit
  v1/v2) and write `runs/05_judge_<mode>/` via the shared `results`
  plumbing (primary metric = `kappa`; auxiliary: `tpr`, `tnr`,
  `accuracy`, `kappa_dev`).
- `overall`: compose the 4 mode judges into one ticket-level
  `05_judge_overall` experiment (a ticket passes overall only if it
  passes every tracked mode) graded against the reference-aware `pass`
  label.
- `likert`: a Likert 1-5 quality judge as a coarse-grained control —
  primary metric `auroc` of the ordinal score against binary labels on
  the test split.
- `scorecard`: a single Markdown table over `runs/*/metrics.json` (one
  row per chapter-05 experiment, kappa first so it is easy to read).
- `nocontext`: an ablation on the `missing_required_fact` mode — run the
  nocontext prompt (handbook text withheld) against the test split and
  compare its kappa with the context-full variant for the same mode.

Design choices (see `research/SOURCES_practitioner.md`, LLM-as-judge):
- Binary pass/fail per failure mode beats a global "quality" score: each
  mode has an unambiguous definition in `taxonomy.yaml`, so the judge has
  a single, checkable question. This follows the "binary pass/fail"
  recommendation over Likert (Hamel & Shankar, AI Evals FAQ).
- Align the judge against the human labels BEFORE trusting it: treat the
  binary judge as a classifier and report TPR/TNR plus Cohen's kappa
  against a human-labeled dev split. Kappa, unlike raw accuracy, is the
  right statistic under class imbalance and near-perfect agreement
  (Shankar et al., "Who Validates the Validators?").
- `critique` comes before `verdict` in the JSON schema: forcing the
  critique first keeps the judge's verdict tied to the evidence instead
  of leading with a label.

Every LLM call goes through `evals_tutorial.llm`, so re-runs are cached.
"""

from __future__ import annotations

import json
import math
import time
from pathlib import Path
from typing import Any

import typer
import yaml
from pydantic import BaseModel, Field

from evals_tutorial.config import settings
from evals_tutorial.handbook import handbook_dir
from evals_tutorial.helpdesk import PROMPTS_DIR, load_traces
from evals_tutorial.labels import load_labels
from evals_tutorial.llm import Ollama, usage_log
from evals_tutorial.results import write_metrics
from evals_tutorial.tickets import load_tickets

# -- modes / taxonomy -----------------------------------------------------------


def load_taxonomy() -> list[dict]:
    """Load the failure-mode taxonomy (id, name, definition, example ids)."""
    path = settings.path("data") / "labels" / "taxonomy.yaml"
    return yaml.safe_load(path.read_text()) or []


def tracked_modes() -> list[str]:
    """Failure modes with >= 4 fails in the committed answer_v1 labels.

    These are the modes we build a judge for (enough failing examples to
    align against); the rest (`wrong_value` 2, `over_promise` 1) are
    skipped per the chapter scope.
    """
    labels = load_labels("answer_v1")
    counts: dict[str, int] = {}
    for row in labels:
        if not row["pass"]:
            for m in row.get("failure_modes") or []:
                counts[m] = counts.get(m, 0) + 1
    return [m for m in sorted(counts) if counts[m] >= 4]


# -- prompt building ------------------------------------------------------------


def _handbook_text(section_id: str) -> str:
    path = handbook_dir() / f"{section_id}.md"
    return path.read_text().strip() if path.exists() else f"(no handbook text for {section_id})"


def _context_for(trace: dict) -> str:
    """Rebuild the recalled handbook context from the trace's `retrieved` ids.

    The SUT's RAG prompt already embeds the section texts, but the judge
    rebuilds them from the stable `retrieved` section ids so the judge is
    independent of the answer prompt's wording.
    """
    sections = [r["section"] for r in trace.get("retrieved") or []]
    if not sections:
        return "(no handbook sections were recalled)"
    return "\n\n".join(f"### {sid}\n{_handbook_text(sid)}" for sid in sections)


def _mode_template(mode: str, version: str) -> str:
    name = "nocontext" if mode.endswith("_nocontext") else mode
    return (PROMPTS_DIR / f"judge_{name}_{version}.txt").read_text()


def judge_messages(mode: str, version: str, trace: dict, *, nocontext: bool = False) -> list[dict]:
    """System = the mode prompt; user = ticket + context + reply.

    The prompt files carry literal `{ticket}` / `{context}` / `{reply}`
    markers AND a trailing `{"critique": ...}` JSON example, so we fill the
    markers with `.replace` (not `str.format`, which would choke on the
    unescaped JSON braces in the example line).
    """
    template = (PROMPTS_DIR / f"judge_{mode}{'_nocontext' if nocontext else ''}_{version}.txt").read_text()
    reply = trace["output"]
    context = "(withheld: nocontext ablation)" if nocontext else _context_for(trace)
    user = template.replace("{ticket}", trace["input"]).replace("{context}", context).replace("{reply}", reply)
    return [{"role": "system", "content": "You are a careful, fair evaluator."}, {"role": "user", "content": user}]


# -- judge schemas ---------------------------------------------------------------


class JudgeVerdict(BaseModel):
    """Binary judge output for one failure mode: critique first, then verdict."""

    critique: str = Field(description="ONE short sentence citing the evidence that drives the verdict")
    verdict: str = Field(description='"pass" or "fail"')


class LikertVerdict(BaseModel):
    """Likert 1-5 quality judge output: critique first, then the integer score."""

    critique: str = Field(description="ONE short sentence citing the evidence that drives the score")
    score: int = Field(ge=1, le=5, description="integer 1-5 quality score")


def judge_ticket(mode: str, version: str, trace: dict, client: Ollama, *, nocontext: bool = False) -> JudgeVerdict:
    """Grade one test/dev ticket for one mode: returns the JSON-schema verdict."""
    msgs = judge_messages(mode, version, trace, nocontext=nocontext)
    reply = client.chat_json(msgs, JudgeVerdict, model=settings.judge_model, temperature=0.0)
    verdict = reply.verdict.strip().lower()
    if verdict not in ("pass", "fail"):
        raise ValueError(f"judge returned non-binary verdict {verdict!r} for {trace['ticket_id']} ({mode})")
    return reply


def likert_ticket(trace: dict, client: Ollama) -> LikertVerdict:
    """Grade one ticket for overall quality with the 1-5 Likert judge."""
    template = (PROMPTS_DIR / "judge_likert_v1.txt").read_text()
    user = template.replace("{ticket}", trace["input"]).replace("{context}", _context_for(trace)).replace("{reply}", trace["output"])
    msgs = [{"role": "system", "content": "You are a careful, fair evaluator."}, {"role": "user", "content": user}]
    return client.chat_json(msgs, LikertVerdict, model=settings.judge_model, temperature=0.0)


# -- metrics ---------------------------------------------------------------------


def _confusion(y_true: list[bool], y_pred: list[bool]) -> dict[str, int]:
    """y==1 is the fail class (we judge the mode); count TP/FP/TN/FN."""
    tp = fp = tn = fn = 0
    for t, p in zip(y_true, y_pred):
        if t and p:
            tp += 1
        elif t and not p:
            fn += 1
        elif not t and p:
            fp += 1
        else:
            tn += 1
    return {"tp": tp, "fp": fp, "tn": tn, "fn": fn}


def tpr_tnr(conf: dict[str, int]) -> tuple[float, float]:
    """True-positive / true-negative rate (treat "fail" as the positive class)."""
    pos = conf["tp"] + conf["fn"] or 1
    neg = conf["tn"] + conf["fp"] or 1
    return conf["tp"] / pos, conf["tn"] / neg


def cohen_kappa(y_true: list[bool], y_pred: list[bool]) -> float:
    """Cohen's kappa for binary labels. 0.0 when there is no agreement to measure."""
    n = len(y_true)
    if n == 0:
        return 0.0
    obs = sum(1 for t, p in zip(y_true, y_pred) if t == p) / n
    p_true = sum(y_true) / n
    p_pred = sum(y_pred) / n
    exp = p_true * p_pred + (1 - p_true) * (1 - p_pred)
    if exp >= 1.0 - 1e-12:
        return 1.0 if obs >= 1.0 - 1e-12 else 0.0
    return (obs - exp) / (1 - exp)


def auroc(scores: list[float], labels: list[int]) -> float:
    """Rank-based AUC (Mann-Whitney) of ordinal scores vs. binary labels."""
    pos = [s for s, lab in zip(scores, labels) if lab == 1]
    neg = [s for s, lab in zip(scores, labels) if lab == 0]
    if not pos or not neg:
        return 0.5
    wins = 0.0
    for s in pos:
        for r in neg:
            if s > r:
                wins += 1.0
            elif s == r:
                wins += 0.5
    return wins / (len(pos) * len(neg))


def _ground_truth_mode(ticket_id: str, mode: str) -> bool:
    """True label: does this ticket carry `mode` in its ground-truth failure_modes?"""
    labels = {r["ticket_id"]: r for r in load_labels("answer_v1")}
    row = labels.get(ticket_id)
    if row is None:
        raise KeyError(f"no label for {ticket_id}")
    return mode in (row.get("failure_modes") or [])


def grade_split(mode: str, version: str, split: str, client: Ollama, *, nocontext: bool = False, limit: int | None = None, run: str = "answer_v1") -> dict[str, Any]:
    """Grade every ticket in `split` for one mode; return per-ticket verdicts + metrics.

    `limit` grades only the first `limit` tickets in split order (default: all).
    `run` selects which recorded traces to grade (default `answer_v1`).
    """
    tickets = [t for t in load_tickets() if t["split"] == split]
    if limit is not None:
        tickets = tickets[:limit]
    traces = {t["ticket_id"]: t for t in load_traces(run)}
    rows: list[dict] = []
    y_true: list[bool] = []
    y_pred: list[bool] = []
    for tk in tickets:
        trace = traces.get(tk["id"])
        if trace is None:
            continue
        v = judge_ticket(mode, version, trace, client, nocontext=nocontext)
        predicted_fail = v.verdict.strip().lower() == "fail"
        true_fail = _ground_truth_mode(tk["id"], mode)
        y_true.append(true_fail)
        y_pred.append(predicted_fail)
        rows.append(
            {
                "ticket_id": tk["id"],
                "split": split,
                "mode": mode,
                "version": version,
                "nocontext": nocontext,
                "true_fail": true_fail,
                "pred_fail": predicted_fail,
                "agreement": true_fail == predicted_fail,
                "critique": v.critique,
            }
        )
    conf = _confusion(y_true, y_pred)
    tpr, tnr = tpr_tnr(conf)
    acc = sum(1 for a, b in zip(y_true, y_pred) if a == b) / len(y_true) if y_true else 0.0
    return {
        "n": len(rows),
        "rows": rows,
        "confusion": conf,
        "tpr": tpr,
        "tnr": tnr,
        "accuracy": acc,
        "kappa": cohen_kappa(y_true, y_pred),
    }


# -- align (dev) -----------------------------------------------------------------


def align_mode(mode: str, client: Ollama, split: str = "dev") -> dict[str, Any]:
    """Align v1 vs v2 on the dev split for one mode; return metrics for each + the winner."""
    v1 = grade_split(mode, "v1", split, client, nocontext=False)
    v2 = grade_split(mode, "v2", split, client, nocontext=False)
    best = "v2" if v2["kappa"] >= v1["kappa"] else "v1"
    return {
        "mode": mode,
        "split": split,
        "versions": {"v1": v1, "v2": v2},
        "best": best,
        "best_kappa": v1["kappa"] if best == "v1" else v2["kappa"],
    }


def align_all(client: Ollama | None = None, split: str = "dev") -> dict[str, Any]:
    """Align all tracked modes on the dev split; write per-mode alignment records."""
    client = client or settings._default_client()
    out_dir = settings.path("runs") / "05_judge_align"
    out_dir.mkdir(parents=True, exist_ok=True)
    summary: dict[str, Any] = {}
    for mode in tracked_modes():
        res = align_mode(mode, client, split=split)
        (out_dir / f"{mode}.json").write_text(json.dumps(res, indent=2, ensure_ascii=False) + "\n")
        summary[mode] = {"best": res["best"], "best_kappa": res["best_kappa"], "v1_kappa": res["versions"]["v1"]["kappa"], "v2_kappa": res["versions"]["v2"]["kappa"]}
    return summary


def chosen_version(mode: str) -> str:
    """The dev-alignment winner recorded for `mode` (falls back to v1 if none)."""
    path = settings.path("runs") / "05_judge_align" / f"{mode}.json"
    if path.exists():
        rec = json.loads(path.read_text())
        return rec.get("best", "v1")
    return "v1"


# -- runs (test) -----------------------------------------------------------------


def _llm_calls_used(before: dict) -> int:
    return (usage_log["hits"] + usage_log["misses"]) - (before["hits"] + before["misses"])


def run_mode(mode: str, version: str = "best", client: Ollama | None = None, split: str = "test", run: str = "answer_v1") -> Path:
    """Grade the split for one mode and write the per-mode judge experiment.

    `run` selects which recorded traces to grade (default `answer_v1`). When
    `run != answer_v1` (the chapter-07 A/B) the experiment is written under the
    A/B name `07_answer_v2_judged_<mode>` (chapter 07) so it never clobbers the
    frozen chapter-05 baseline `05_judge_<mode>`.
    """
    client = client or settings._default_client()
    if version == "best":
        version = "v1" if chosen_version(mode) not in ("v1", "v2") else chosen_version(mode)
    before = dict(usage_log)
    started = time.monotonic()
    res = grade_split(mode, version, split, client, nocontext=False, run=run)
    seconds = time.monotonic() - started
    calls = _llm_calls_used(before)

    # dev kappa for this mode+version (align already computed it; re-read the record).
    align_path = settings.path("runs") / "05_judge_align" / f"{mode}.json"
    kappa_dev = None
    if align_path.exists():
        rec = json.loads(align_path.read_text())
        kappa_dev = rec["versions"].get(version, {}).get("kappa")

    is_ab = run != "answer_v1"
    experiment = f"07_answer_v2_judged_{mode}" if is_ab else f"05_judge_{mode}"
    return write_metrics(
        experiment=experiment,
        chapter="07" if is_ab else "05",
        n=res["n"],
        metrics={
            "kappa": res["kappa"],
            "tpr": res["tpr"],
            "tnr": res["tnr"],
            "accuracy": res["accuracy"],
            "kappa_dev": round(kappa_dev, 4) if kappa_dev is not None else -1.0,
        },
        llm_calls=calls,
        seconds=seconds,
        details={
            "primary": "kappa",
            "mode": mode,
            "version": version,
            "split": split,
            "run": run,
            "confusion": res["confusion"],
            "judge_model": settings.judge_model,
            "notes": f"{mode} {version} (best={chosen_version(mode)}) on {run}",
        },
        predictions=res["rows"],
        config={
            "mode": mode,
            "version": version,
            "split": split,
            "run": run,
            "judge_model": settings.judge_model,
            "judge_prompt": f"judge_{mode}_{version}.txt",
        },
    )


def run_all_modes(client: Ollama | None = None, version: str = "best", split: str = "test", run: str = "answer_v1") -> list[Path]:
    """Grade the split for every tracked mode (parallel where possible).

    Uses a small thread pool: each ticket's LLM call is independent, so we
    can grade all modes concurrently to cut wall time on the shared GPU box.
    `run` selects which recorded traces to grade (default `answer_v1`).
    """
    import concurrent.futures as cf

    client = client or settings._default_client()
    paths: list[Path] = []
    with cf.ThreadPoolExecutor(max_workers=min(4, len(tracked_modes()) or 1)) as pool:
        futures = {pool.submit(run_mode, mode, version, client, split, run): mode for mode in tracked_modes()}
        for fut in cf.as_completed(futures):
            paths.append(fut.result())  # raise any exception
    return sorted(paths)


# -- overall (ticket-level pass) -------------------------------------------------


def overall(client: Ollama | None = None, split: str = "test", run: str = "answer_v1") -> Path:
    """Compose the 4 mode verdicts into a ticket-level judged-overall experiment.

    A ticket passes overall only if NO tracked mode judges it as a fail.
    Ground truth: the reference-aware `pass` label in the answer_v1 labels.
    `run` selects which recorded traces to grade (default `answer_v1`). When
    grading the chapter-07 prompt (`answer_v2`) the result is written under
    `07_answer_v2_judged_overall` (chapter 07) so the frozen `05_judge_overall`
    baseline is preserved for the A/B comparison.

    The four per-mode verdicts are *composed* from the per-mode experiment
    already written by `judge run --mode all --run <run>` (no re-LLM here), so
    this call adds 0 extra LLM budget. If a per-mode file is missing it falls
    back to grading that one mode inline.
    """
    client = client or settings._default_client()
    is_ab = run != "answer_v1"
    modes = tracked_modes()
    runs_dir = settings.path("runs")
    modes_by_ticket: dict[str, dict[str, bool]] = {}
    for mode in modes:
        exp_name = f"07_answer_v2_judged_{mode}" if is_ab else f"05_judge_{mode}"
        pred_path = runs_dir / exp_name / "predictions.jsonl"
        if pred_path.exists():
            for line in pred_path.read_text().splitlines():
                if not line.strip():
                    continue
                row = json.loads(line)
                if row.get("split") != split:
                    continue
                modes_by_ticket.setdefault(row["ticket_id"], {})[mode] = bool(row["pred_fail"])
            continue
        # fallback: grade this mode inline (counts against budget)
        version = chosen_version(mode)
        res = grade_split(mode, version, split, client, nocontext=False, run=run)
        for row in res["rows"]:
            modes_by_ticket.setdefault(row["ticket_id"], {})[mode] = row["pred_fail"]

    labels = {r["ticket_id"]: r for r in load_labels("answer_v1")}
    y_true: list[bool] = []
    y_pred: list[bool] = []
    rows: list[dict] = []
    for tid, mfail in modes_by_ticket.items():
        true_pass = bool(labels[tid]["pass"])
        pred_pass = not any(mfail.values())  # passes overall if no mode fails
        y_true.append(not true_pass)  # positive class = fail
        y_pred.append(not pred_pass)
        rows.append(
            {
                "ticket_id": tid,
                "split": split,
                "true_pass": true_pass,
                "pred_pass": pred_pass,
                "mode_fails": {m: v for m, v in mfail.items() if v},
                "agreement": true_pass == pred_pass,
            }
        )
    conf = _confusion(y_true, y_pred)
    tpr, tnr = tpr_tnr(conf)
    acc = sum(1 for a, b in zip(y_true, y_pred) if a == b) / len(y_true) if y_true else 0.0
    pass_rate = sum(1 for r in rows if r["pred_pass"]) / len(rows) if rows else 0.0
    return write_metrics(
        experiment="07_answer_v2_judged_overall" if is_ab else "05_judge_overall",
        chapter="07" if is_ab else "05",
        n=len(rows),
        metrics={"kappa": cohen_kappa(y_true, y_pred), "pass_rate": pass_rate, "tpr": tpr, "tnr": tnr, "accuracy": acc},
        details={"primary": "kappa", "modes": modes, "run": run, "note": "ticket passes overall iff no tracked mode fails"},
        predictions=rows,
        config={"modes": modes, "run": run, "judge_model": settings.judge_model},
    )


# -- likert (control) -------------------------------------------------------------


def likert(client: Ollama | None = None, split: str = "test", limit: int | None = None) -> Path:
    """Grade the test split with the 1-5 Likert judge; primary metric = AUC.

    `limit` grades the first `limit` tickets in split order (default: all).
    """
    client = client or settings._default_client()
    tickets = [t for t in load_tickets() if t["split"] == split]
    if limit is not None:
        tickets = tickets[:limit]
    traces = {t["ticket_id"]: t for t in load_traces("answer_v1")}
    labels = {r["ticket_id"]: r for r in load_labels("answer_v1")}
    scores: list[float] = []
    labs: list[int] = []
    rows: list[dict] = []
    before = dict(usage_log)
    started = time.monotonic()
    for tk in tickets:
        trace = traces.get(tk["id"])
        if trace is None or tk["id"] not in labels:
            continue
        v = likert_ticket(trace, client)
        is_fail = not labels[tk["id"]]["pass"]
        scores.append(float(v.score))
        labs.append(1 if is_fail else 0)
        rows.append(
            {
                "ticket_id": tk["id"],
                "split": split,
                "score": v.score,
                "true_fail": is_fail,
                "critique": v.critique,
            }
        )
    seconds = time.monotonic() - started
    calls = _llm_calls_used(before)
    auc = auroc(scores, labs)
    import collections as _c

    histogram = {str(s): _c.Counter(scores).get(s, 0) for s in range(1, 6)}
    notes = "Likert 1-5 control judge (higher AUC = scores separate pass/fail better)"
    if limit is not None:
        notes = f"Likert 1-5 control on first {limit} {split} tickets — " + notes
    return write_metrics(
        experiment="05_likert_overall",
        chapter="05",
        n=len(rows),
        metrics={"auroc": auc, "mean_score": sum(scores) / len(scores) if scores else 0.0},
        llm_calls=calls,
        seconds=seconds,
        details={"primary": "auroc", "note": notes, "score_histogram": histogram, "limit": limit},
        predictions=rows,
        config={"judge_model": settings.judge_model, "prompt": "judge_likert_v1.txt", "limit": limit},
    )


# -- nocontext ablation -----------------------------------------------------------


def _with_context_kappa_same_tickets(mode: str, split: str, limit: int | None) -> float | None:
    """With-context kappa on exactly the first `limit` tickets of `split`.

    Reuses the already-written step-1 `05_judge_<mode>` test predictions
    (the chosen version on the full split) so this costs zero LLM calls while
    measuring the same ticket set as the nocontext ablation — a fair compare.
    """
    tids = [t["id"] for t in load_tickets() if t["split"] == split]
    if limit is not None:
        tids = tids[:limit]
    pred_path = settings.path("runs") / f"05_judge_{mode}" / "predictions.jsonl"
    if not pred_path.exists():
        return None
    by_id = {}
    for line in pred_path.read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        by_id.setdefault(row.get("ticket_id"), row)
    y_true = [by_id[tid]["true_fail"] for tid in tids if tid in by_id]
    y_pred = [by_id[tid]["pred_fail"] for tid in tids if tid in by_id]
    if not y_true:
        return None
    return cohen_kappa(y_true, y_pred)


def nocontext(mode: str = "missing_required_fact", client: Ollama | None = None, split: str = "test", limit: int | None = None) -> Path:
    """Ablation: grade `mode` with handbook text withheld on the test split.

    `limit` grades the first `limit` tickets in split order (default: all).
    """
    client = client or settings._default_client()
    before = dict(usage_log)
    started = time.monotonic()
    res = grade_split(mode, "v1", split, client, nocontext=True, limit=limit)
    seconds = time.monotonic() - started
    calls = _llm_calls_used(before)
    # with-context kappa on the SAME ticket set (zero new calls; from step-1 cache).
    kappa_ctx = _with_context_kappa_same_tickets(mode, split, limit)
    note = "nocontext ablation (handbook text withheld)"
    if limit is not None:
        note = f"nocontext ablation on first {limit} {split} tickets — " + note
    return write_metrics(
        experiment=f"05_judge_{mode}_nocontext",
        chapter="05",
        n=res["n"],
        metrics={"kappa": res["kappa"], "tpr": res["tpr"], "tnr": res["tnr"], "accuracy": res["accuracy"], "kappa_with_context": round(kappa_ctx, 4) if kappa_ctx is not None else -1.0},
        llm_calls=calls,
        seconds=seconds,
        details={"primary": "kappa", "mode": mode, "note": note, "limit": limit, "with_context_source": f"05_judge_{mode} (chosen version, same {limit if limit is not None else 'all'} tickets)"},
        predictions=res["rows"],
        config={"mode": mode, "nocontext": True, "judge_model": settings.judge_model, "limit": limit},
    )


# -- scorecard --------------------------------------------------------------------


DEV_SCORECARD_COLUMNS = ["mode", "version", "tpr", "tnr", "accuracy", "kappa", "chosen"]
SCORECARD_COLUMNS = ["experiment", "mode", "n", "kappa", "tpr", "tnr", "llm_calls", "notes"]


def _fmt(x: Any) -> str:
    if x is None:
        return "—"
    if isinstance(x, float):
        return f"{x:.3f}"
    return str(x)


def _dev_scorecard_rows() -> list[dict]:
    """modes x {v1, v2} on dev (from 05a align records), with the winner marked."""
    rows: list[dict] = []
    for mode in tracked_modes():
        path = settings.path("runs") / "05_judge_align" / f"{mode}.json"
        if not path.exists():
            continue
        rec = json.loads(path.read_text())
        best = rec.get("best")
        for v in ("v1", "v2"):
            d = (rec.get("versions") or {}).get(v) or {}
            rows.append(
                {
                    "mode": mode,
                    "version": v,
                    "tpr": _fmt(d.get("tpr")),
                    "tnr": _fmt(d.get("tnr")),
                    "accuracy": _fmt(d.get("accuracy")),
                    "kappa": _fmt(d.get("kappa")),
                    "chosen": "<-" if v == best else "",
                }
            )
    return rows


def build_scorecard() -> tuple[Path, str]:
    """Markdown scorecard: dev alignment (v1 vs v2) + chosen-version test runs + ablations."""
    from evals_tutorial.results import iter_metrics

    dev_rows = _dev_scorecard_rows()
    lines = ["# Chapter 05 — judge scorecard", ""]
    if dev_rows:
        lines += [
            "## Dev alignment (v1 vs v2, chosen = higher kappa) — from 05a",
            "| " + " | ".join(DEV_SCORECARD_COLUMNS) + " |",
            "|" + "|".join("---" for _ in DEV_SCORECARD_COLUMNS) + "|",
        ]
        for r in dev_rows:
            lines.append("| " + " | ".join(str(r[c]) for c in DEV_SCORECARD_COLUMNS) + " |")
        lines.append("")
    lines += ["## Test (chosen version + ablations)", "| " + " | ".join(SCORECARD_COLUMNS) + " |", "|" + "|".join("---" for _ in SCORECARD_COLUMNS) + "|"]
    rows = []
    for rec in iter_metrics():
        if str(rec.get("chapter")) != "5" and str(rec.get("chapter")) != "05":
            continue
        metrics = rec.get("metrics", {})
        mode = rec.get("details", {}).get("mode", "overall" if "overall" in rec.get("experiment", "") else "")
        kappa = metrics.get("kappa", metrics.get("auroc"))
        rows.append(
            {
                "experiment": rec.get("experiment", ""),
                "mode": mode,
                "n": rec.get("n", ""),
                "kappa": kappa,
                "tpr": metrics.get("tpr", "—"),
                "tnr": metrics.get("tnr", "—"),
                "llm_calls": rec.get("llm_calls", 0),
                "notes": rec.get("details", {}).get("notes", ""),
            }
        )
    # sort: per-mode kappa judges first (by kappa desc), then overall, likert, nocontext
    def order(r: dict) -> tuple:
        exp = r["experiment"]
        if "nocontext" in exp:
            return (3, 0)
        if "overall" in exp:
            return (2, 0)
        if "likert" in exp:
            return (1, 0)
        return (0, -(r["kappa"] if isinstance(r["kappa"], float) else 0.0))

    for r in sorted(rows, key=order):
        cells = [
            r["experiment"],
            r["mode"],
            r["n"],
            _fmt(r["kappa"]),
            _fmt(r["tpr"]),
            _fmt(r["tnr"]),
            r["llm_calls"],
            r["notes"],
        ]
        lines.append("| " + " | ".join(str(c) for c in cells) + " | ")
    doc = "\n".join(lines) + "\n"

    out = settings.path("runs") / "05_judge_scorecard.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc)
    return out, doc


# -- CLI ----------------------------------------------------------------------------


def _default_client_factory() -> Ollama:
    from evals_tutorial.llm import ollama

    return ollama


settings._default_client = lambda: _default_client_factory()

app = typer.Typer(add_completion=False)


@app.command()
def align(client: str = typer.Option("", help="ignored: uses Ollama (or the test-injected one)"), split: str = typer.Option("dev")) -> None:
    """Align v1 vs v2 on the dev split for every tracked mode (writes 05_judge_align/<mode>.json)."""
    summary = align_all(client=settings._default_client(), split=split)
    for mode, row in summary.items():
        print(f"{mode}: best={row['best']} (v1={row['v1_kappa']:.3f}, v2={row['v2_kappa']:.3f}) -> {row['best_kappa']:.3f}")
    print(f"wrote {settings.path('runs') / '05_judge_align'}")


@app.command(name="run")
def run_cmd(
    mode: str = typer.Option("all", help="a tracked mode, or 'all'"),
    version: str = typer.Option("best", help="v1/v2 or 'best'"),
    split: str = typer.Option("test"),
    run: str = typer.Option("answer_v1", help="which recorded traces to grade (answer_v1/answer_v2); answer_v2 -> 07_answer_v2_judged_<mode>"),
) -> None:
    """Grade the split for one mode (or all) and write the per-mode judge metrics.

    With `run=answer_v2` the result lands under `07_answer_v2_judged_<mode>`
    (chapter 07) leaving the frozen `05_judge_<mode>` baseline untouched.
    """
    client = settings._default_client()
    if mode == "all":
        paths = run_all_modes(client=client, version=version, split=split, run=run)
    else:
        paths = [run_mode(mode, version=version, client=client, split=split, run=run)]
    for p in paths:
        print(f"wrote {p}")


@app.command(name="overall")
def overall_cmd(
    split: str = typer.Option("test"),
    run: str = typer.Option("answer_v1", help="which recorded traces to grade; answer_v2 -> 07_answer_v2_judged_overall"),
) -> None:
    """Compose the 4 mode judges into the ticket-level judged-overall experiment."""
    print(f"wrote {overall(client=settings._default_client(), split=split, run=run)}")


@app.command(name="likert")
def likert_cmd(split: str = typer.Option("test"), limit: int | None = typer.Option(None, help="grade only the first N tickets in split order")) -> None:
    """Grade the test split with the 1-5 Likert judge (control); primary metric = AUC."""
    print(f"wrote {likert(client=settings._default_client(), split=split, limit=limit)}")


@app.command(name="nocontext")
def nocontext_cmd(mode: str = typer.Option("missing_required_fact"), split: str = typer.Option("test"), limit: int | None = typer.Option(None, help="grade only the first N tickets in split order")) -> None:
    """Ablation: run the nocontext prompt (text withheld) on the test split for a mode."""
    print(f"wrote {nocontext(mode=mode, client=settings._default_client(), split=split, limit=limit)}")


@app.command()
def scorecard() -> None:
    """Write runs/05_judge_scorecard.md — kappa-first Markdown table over ch.05 metrics."""
    out, _ = build_scorecard()
    print(f"wrote {out}")


@app.command(name="all")
def all_cmd(split: str = typer.Option("test")) -> None:
    """Full chapter-05 pipeline: align -> run -> overall -> likert -> nocontext -> scorecard."""
    client = settings._default_client()
    print("== align (dev) ==")
    align_all(client=client, split="dev")
    print("== run all modes (test) ==")
    for p in run_all_modes(client=client, version="best", split=split):
        print(f"  {p}")
    print("== overall (test) ==")
    print(f"  {overall(client=client, split=split)}")
    print("== likert (test) ==")
    print(f"  {likert(client=client, split=split)}")
    print("== nocontext ablation (test) ==")
    print(f"  {nocontext(mode='missing_required_fact', client=client, split=split)}")
    print("== scorecard ==")
    out, _ = build_scorecard()
    print(f"  {out}")


if __name__ == "__main__":
    app()
