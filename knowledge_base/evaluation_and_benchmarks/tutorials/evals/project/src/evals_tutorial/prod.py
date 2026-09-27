"""Chapter 13a — production: Langfuse self-hosted (tracing, datasets,
experiment runs, human scores).

Zero LLM calls: everything is replayed from committed traces, tickets and
prediction files; `answer`'s LLM calls are served from `data/cache`.

    just langfuse-up                          start the stack (profile `langfuse`)
    just prod-trace answer_v1                 replay the 80 traces as Langfuse traces
    just prod-dataset                         create helpdesk-test (60) + helpdesk-dev (20)
    just prod-experiment v1                   cached run of helpdesk-test + ch-05/ch-04 scores
    just prod-scores answer_v1                ch-03 human labels as scores on those traces
    prod ci                                   CI regression gate (chapter 13b)
    prod monitor --sample 0.2                 online sampling monitor (chapter 13b)

The client is created lazily and only talks when LANGFUSE_HOST +
LANGFUSE_PUBLIC_KEY + LANGFUSE_SECRET_KEY are set (`require_live()`).
"""

from __future__ import annotations

import json

import typer
from langfuse import Langfuse
from langfuse.types import TraceContext

from evals_tutorial import halluc
from evals_tutorial import helpdesk
from evals_tutorial import stats
from evals_tutorial import tracing
from evals_tutorial.config import settings
from evals_tutorial.results import write_metrics

app = typer.Typer(add_completion=False)


# -- client -------------------------------------------------------------------


def require_live() -> Langfuse:
    if not tracing.is_live() or not tracing.settings.langfuse_secret_key:
        raise typer.Exit(
            "Langfuse is not configured. Set LANGFUSE_HOST, LANGFUSE_PUBLIC_KEY "
            "and LANGFUSE_SECRET_KEY in project/.env (see .env.template) and "
            "start the stack with `just langfuse-up`."
        )
    return tracing.client()


def _json(path) -> list[dict]:
    return [json.loads(line) for line in settings.path(path).read_text().splitlines() if line.strip()]


def _tickets() -> dict[str, dict]:
    return {t["id"]: t for t in helpdesk.load_tickets()}  # noqa: F841


# -- trace: replay committed traces into Langfuse -------------------------------


def replay_traces(run: str) -> list[dict]:
    """Push one run's committed traces as Langfuse observations.

    `create_trace_id()` mints a client-side id and `TraceContext` binds it,
    so the same id can later be used for `create_score(..., trace_id=...)`
    (the `scores` command).
    """
    lf = require_live()
    tickets = _tickets()
    rows: list[dict] = []
    for trace in helpdesk.load_traces(run):
        tid = trace["ticket_id"]
        ticket = tickets.get(tid, {})
        trace_id = lf.create_trace_id()
        usage = trace.get("usage") or {}
        with lf.start_as_current_observation(
            trace_context=TraceContext(trace_id=trace_id),
            name=f"helpdesk answer {run}",
            as_type="span",
            input=trace.get("input"),
            output=trace.get("output"),
            metadata={
                "version": trace.get("version"),
                "model": trace.get("model"),
                "latency_s": trace.get("latency_s"),
                "retrieved": trace.get("retrieved", []),
                "persona": ticket.get("persona"),
                "topic": ticket.get("topic"),
                "scenario": ticket.get("scenario"),
                "split": ticket.get("split"),
                "gold": ticket.get("gold"),
            },
        ) as span:
            span.update(
                usage_details={
                    "input": usage.get("prompt_eval_count") or 0,
                    "output": usage.get("eval_count") or 0,
                },
                model=trace.get("model"),
            )
        rows.append(
            {
                "ticket_id": tid,
                "trace_id": trace_id,
                "url": lf.get_trace_url(trace_id=trace_id) or "",
            }
        )
    lf.flush()
    return rows


@app.command()
def trace(
    run: str = typer.Option("answer_v1", help="committed run, e.g. answer_v1 or answer_v2"),
) -> None:
    """Replay the run's committed 80 traces into Langfuse (zero LLM calls)."""
    rows = replay_traces(run)
    mapped = settings.path("data/langfuse") / run
    mapped.parent.mkdir(parents=True, exist_ok=True)
    mapped.write_text(json.dumps(rows, indent=2))
    print(f"pushed {len(rows)} traces of run {run!r} (ticket_id->trace_id map: {mapped})")


# -- dataset ---------------------------------------------------------------------


def upsert_datasets() -> list[dict]:
    lf = require_live()
    tickets = _tickets()
    out: list[dict] = []
    for name, split in (("helpdesk-test", "test"), ("helpdesk-dev", "dev")):
        lf.create_dataset(
            name=name,
            description=f"chapter 03 {split} split of the 80 helpdesk tickets",
        )
        count = 0
        for ticket in tickets.values():
            if ticket.get("split") != split:
                continue
            lf.create_dataset_item(
                id=ticket["id"],
                dataset_name=name,
                input=ticket["text"],
                expected_output=ticket.get("gold"),
                metadata={
                    "ticket_id": ticket["id"],
                    "persona": ticket.get("persona"),
                    "topic": ticket.get("topic"),
                    "scenario": ticket.get("scenario"),
                },
            )
            count += 1
        out.append({"dataset": name, "items": count})
    lf.flush()
    return out


@app.command()
def dataset() -> None:
    """Create helpdesk-test (60) and helpdesk-dev (20) from tickets+gold labels."""
    for row in upsert_datasets():
        print(f"dataset {row['dataset']!r}: {row['items']} items")


# -- experiment: cached dataset run + committed verdicts ---------------------------


def _verdicts(version: str) -> dict[str, dict]:
    """chapter-05 overall judge verdicts, per ticket id."""
    return {
        r["ticket_id"]: r
        for r in _json("runs/05_judge_overall/predictions.jsonl")
        if r.get("split") == "test"
    }


def _checks(version: str) -> dict[str, dict]:
    """chapter-04 code-check results, per ticket id."""
    return {
        r["ticket_id"]: r
        for r in _json(f"runs/04_checks_answer_{version}/predictions.jsonl")
        if r.get("split") == "test"
    }


def _evaluators_for(version: str) -> list:
    verdicts = _verdicts(version)
    checks = _checks(version)

    def evaluate(*, input, output, expected_output, metadata, **_):  # noqa: ARG001
        tid = (metadata or {}).get("ticket_id")
        v = verdicts.get(tid)
        c = checks.get(tid)
        results = []
        if v is not None:
            results.append(
                {
                    "name": "judge_overall_pass",
                    "value": 1.0 if v.get("pred_pass") else 0.0,
                    "comment": f"chapter-05 overall judge verdict (committed {version}; agreement={v.get('agreement')})",
                }
            )
        if c is not None:
            failed = [name for name, ok in c.get("checks", {}).items() if not ok]
            results.append(
                {
                    "name": "all_checks_pass",
                    "value": 1.0 if c.get("pass") else 0.0,
                    "comment": f"chapter-04 checks: failed={failed or []} (committed {version})",
                }
            )
        return results

    return [evaluate]


def run_experiment(version: str) -> dict:
    """Run helpdesk-test through the cached answer, attach committed verdicts.

    The task goes through `helpdesk.answer` (wrapped by `@observe`), so the
    experiment run item's observation also carries the live trace; the
    evaluator rows land on observations of the run item.
    """
    lf = require_live()
    ds = lf.get_dataset("helpdesk-test")

    def task_fn(*, item, **_):
        text = item["input"] if isinstance(item, dict) else item.input
        return helpdesk.answer(text, version=version).text

    result = lf.run_experiment(
        name="helpdesk",
        run_name=f"answer_{version}",
        data=[
            {
                "input": i.input,
                "expected_output": i.expected_output,
                "metadata": i.metadata,
            }
            for i in ds.items
        ],
        task=task_fn,
        evaluators=_evaluators_for(version),
        max_concurrency=1,
        metadata={"chapter": "13", "version": version, "source": "cache"},
    )
    lf.flush()
    item_results = getattr(result, "item_results", []) or []
    traced = sum(1 for i in item_results if getattr(i, "trace_id", None))
    scored = sum(
        1
        for i in item_results
        if any(e.name in ("judge_overall_pass", "all_checks_pass") for e in (getattr(i, "evaluations", None) or []))
    )
    return {
        "version": version,
        "run_name": f"answer_{version}",
        "items": len(item_results),
        "items_traced": traced,
        "items_scored": scored,
        "dataset_run_id": getattr(result, "dataset_run_id", None),
    }


@app.command()
def experiment(
    version: str = typer.Option("v1", help="prompt version: v1 or v2"),
) -> None:
    """Run helpdesk-test through the cached answer; attach ch-05/ch-04 scores."""
    if version not in ("v1", "v2"):
        raise typer.Exit("version must be v1 or v2")
    row = run_experiment(version)
    print(
        f"experiment {row['run_name']}: {row['items']} items, "
        f"{row['items_traced']} traced, {row['items_scored']} scored"
    )
    if row["dataset_run_id"]:
        print(f"dataset_run_id: {row['dataset_run_id']}")


# -- scores: chapter-03 human labels ------------------------------------------------


def push_human_scores(run: str) -> dict:
    """Push ch-03 human labels as scores on the traces replayed by `trace`."""
    lf = require_live()
    mapped_path = settings.path("data/langfuse") / run
    if not mapped_path.exists():
        rows = replay_traces(run)
        mapped_path.parent.mkdir(parents=True, exist_ok=True)
        mapped_path.write_text(json.dumps(rows, indent=2))
    else:
        rows = json.loads(mapped_path.read_text())
    trace_id_for = {r["ticket_id"]: r["trace_id"] for r in rows}

    version = run.removeprefix("answer_")
    labels = _json(f"data/labels/answer_{version}.jsonl") if (
        settings.path(f"data/labels/answer_{version}.jsonl").exists()
    ) else _json("data/labels/answer_v1.jsonl")

    pushed = skipped = 0
    for lab in labels:
        tid = lab.get("ticket_id")
        trace_id = trace_id_for.get(tid)
        if not trace_id:
            skipped += 1
            continue
        lf.create_score(
            name="human_pass",
            value=1.0 if lab.get("pass") else 0.0,
            trace_id=trace_id,
            comment="; ".join(lab.get("failure_modes") or []) or "pass",
        )
        pushed += 1
    lf.flush()
    return {"run": run, "pushed": pushed, "skipped": skipped, "traces": len(trace_id_for)}


@app.command()
def scores(
    run: str = typer.Option("answer_v1", help="committed run the labels belong to"),
) -> None:
    """Attach ch-03 human labels (`data/labels/answer_v1.jsonl`) as scores."""
    row = push_human_scores(run)
    print(f"pushed {row['pushed']} human_pass scores on {row['traces']} traces ({row['skipped']} without trace)")


# -- chapter 13b: CI regression gate -------------------------------------------------
#
# Gate rule (specs/13b_ci_gate_monitor.md):
#   FAIL if the 95% CI upper bound of the pass-rate delta is < -0.05
#        (i.e. we are sure the new version regressed on the judge),
#   or if `all_checks_pass` dropped by more than 0.10.
# Otherwise PASS. Deterministic, zero LLM calls: reads the committed
# ch-05 overall verdicts and ch-04 code checks for both versions.

GATE_MIN_DELTA = 0.05       # fail if delta_ci_upper < -GATE_MIN_DELTA
GATE_MAX_CHECKS_DROP = 0.10  # fail if all_checks_drop > GATE_MAX_CHECKS_DROP


def gate_decision(
    pass_a: list[bool],
    pass_b: list[bool],
    checks_drop: float,
    min_delta: float = GATE_MIN_DELTA,
    max_checks_drop: float = GATE_MAX_CHECKS_DROP,
    n_boot: int = 2000,
    seed: int = 0,
) -> dict:
    """Apply the gate rule to paired verdict lists (same order, same tickets).

    `pass_a`/`pass_b` are paired per-ticket pass flags for the candidate
    (`a`, e.g. v2) and baseline (`b`, e.g. v1); `checks_drop` is
    all_checks_pass(baseline) - all_checks_pass(candidate).
    """
    if len(pass_a) != len(pass_b):
        raise ValueError("paired lists must have equal length")
    n = len(pass_a)
    a = [1.0 if x else 0.0 for x in pass_a]
    b = [1.0 if x else 0.0 for x in pass_b]
    pa = sum(a) / n if n else 0.0
    pb = sum(b) / n if n else 0.0
    delta = pa - pb
    if n >= 2 and any(x != y for x, y in zip(a, b)):
        pr = stats.paired_bootstrap(a, b, n_boot=n_boot, seed=seed)
        delta_ci = list(pr["ci"])
        p = pr["p_value"]
    else:
        delta_ci = [delta, delta]
        p = 1.0
    reasons = []
    if delta_ci[1] < -min_delta:
        reasons.append(
            f"pass-rate delta CI upper {delta_ci[1]:+.3f} < -{min_delta} "
            f"(delta={delta:+.3f})"
        )
    if checks_drop > max_checks_drop:
        reasons.append(f"all_checks_pass dropped by {checks_drop:+.3f} > {max_checks_drop}")
    return {
        "pass": not reasons,
        "reasons": reasons,
        "pass_rate_a": pa,
        "pass_rate_b": pb,
        "delta": delta,
        "delta_ci": delta_ci,
        "p_value": p,
        "checks_drop": checks_drop,
        "min_delta": min_delta,
        "max_checks_drop": max_checks_drop,
    }


def _ci_gate_report(version: str = "v2", baseline: str = "v1") -> dict:
    """Paired ch-05 verdicts + ch-04 checks for shared test tickets."""
    v_new = _verdicts(version)
    v_base = _verdicts(baseline)
    common = sorted(set(v_new) & set(v_base))
    if not common:
        raise RuntimeError(f"no shared test tickets between {version} and {baseline}")
    a = [bool(v_new[t].get("pred_pass")) for t in common]
    b = [bool(v_base[t].get("pred_pass")) for t in common]
    c_new = _checks(version)
    c_base = _checks(baseline)
    common_c = sorted(set(c_new) & set(c_base))
    checks_new = sum(1.0 if c_new[t].get("pass") else 0.0 for t in common_c) / len(common_c)
    checks_base = sum(1.0 if c_base[t].get("pass") else 0.0 for t in common_c) / len(common_c)
    checks_drop = checks_base - checks_new
    dec = gate_decision(a, b, checks_drop)
    summary = [
        f"# CI regression gate — {version} vs {baseline}",
        "",
        f"- n tickets: {len(common)}",
        f"- pass rate: {dec['pass_rate_b']:.3f} ({baseline}) → {dec['pass_rate_a']:.3f} ({version})  Δ = **{dec['delta']:+.3f}**",
        f"- pass-rate delta CI [95%]: [{dec['delta_ci'][0]:+.3f}, {dec['delta_ci'][1]:+.3f}]",
        f"- p-value (paired bootstrap): {dec['p_value']:.3f}",
        f"- all_checks_pass: {checks_base:.3f} → {checks_new:.3f}  (drop {checks_drop:+.3f})",
        "",
        f"**Decision: {'FAIL ❌' if not dec['pass'] else 'PASS ✅'}**",
        "",
    ]
    for r in dec["reasons"]:
        summary.append(f"- failed rule: {r}")
    return {
        "version": version,
        "baseline": baseline,
        "n": len(common),
        "tickets": common,
        "pass_rate_base": dec["pass_rate_b"],
        "pass_rate_new": dec["pass_rate_a"],
        "checks_drop": checks_drop,
        "dec": dec,
        "summary": "\n".join(summary),
    }


def run_gate(version: str = "v2", baseline: str = "v1", project_root=None) -> dict:
    """Compute the gate, write runs/13_ci_gate/, return report (for tests too)."""
    rep = _ci_gate_report(version, baseline)
    dec = rep["dec"]
    out = write_metrics(
        f"13_ci_gate_{version}_vs_{baseline}",
        13,
        rep["n"],
        {
            "pass_rate_delta": dec["delta"],
            "pass_rate_baseline": rep["pass_rate_base"],
            "pass_rate_version": rep["pass_rate_new"],
            "all_checks_drop": rep["checks_drop"],
            "gate_pass": 1.0 if dec["pass"] else 0.0,
        },
        ci={"pass_rate_delta": dec["delta_ci"]},
        llm_calls=0,
        details={
            "version": version,
            "baseline": baseline,
            "gate": dec,
            "summary_md": rep["summary"],
        },
        predictions=[
            {
                "ticket_id": t,
                f"pass_{baseline}": bool(_verdicts(baseline)[t]["pred_pass"]),
                f"pass_{version}": bool(_verdicts(version)[t]["pred_pass"]),
            }
            for t in rep["tickets"]
        ],
        config={"min_delta": GATE_MIN_DELTA, "max_checks_drop": GATE_MAX_CHECKS_DROP, "n_boot": 2000, "seed": 0},
        project_root=project_root,
        dir_name="13_ci_gate",
    )
    rep["out"] = str(out)
    return rep


@app.command()
def ci(
    version: str = typer.Option("v2", help="candidate prompt version"),
    baseline: str = typer.Option("v1", help="baseline prompt version"),
) -> None:
    """CI regression gate: fail (exit 1) if the verdict delta CI upper < -0.05 or checks drop > 0.10."""
    rep = run_gate(version, baseline)
    print(rep["summary"])
    if not rep["dec"]["pass"]:
        raise typer.Exit(1)


# -- chapter 13b: online monitoring on a sample -------------------------------------


def plan_days(
    traces: list[dict],
    sample: float = 0.2,
    days: int = 7,
    seed: int = 0,
) -> list[list[dict]]:
    """Simulate `days` of daily sampling at `sample` fraction of the pool per day.

    The pool is shuffled (seeded) and cut into disjoint chunks of size
    ``k = max(1, round(len * sample))``; the last (possibly shorter) chunk is
    the remainder so the chunks partition the whole pool.  Day ``i`` scores
    chunk ``i % n_chunks`` (a rotation).  As a result, every day scores
    exactly ``k`` traces for the first ``n_chunks`` days (the requested
    ``sample`` fraction of the pool); when ``days >= n_chunks`` the union
    over the window covers the whole pool so no trace is wasted.
    Deterministic: same inputs → same plan.
    """
    import math
    import random

    if not traces:
        return [[] for _ in range(days)]
    rng = random.Random(seed)
    ordered = list(traces)
    rng.shuffle(ordered)
    n = len(ordered)
    k = max(1, int(round(n * sample)))
    n_chunks = max(1, math.ceil(n / k))
    # Partition the pool into n_chunks contiguous pieces; the last may be shorter
    # (by construction n - (n_chunks-1)*k >= 0, so the tail never disappears).
    base, extra = divmod(n, n_chunks)
    sizes = [base + (1 if i < extra else 0) for i in range(n_chunks)]
    chunks: list[list[dict]] = []
    pos = 0
    for size in sizes:
        chunks.append(ordered[pos : pos + size])
        pos += size
    return [chunks[i % n_chunks] for i in range(days)]


def _hhem_score(model, tok, source: str, response: str) -> float:
    """1 - consistency (chapter 09 math): higher = more hallucinationy."""
    import torch  # local import: keep prod importable without torch

    cons = 0.0
    if source.strip() and response.strip():
        out = tok(
            halluc.HHEM_PROMPT.format(text1=source, text2=response),
            truncation=True,
            max_length=512,
            return_tensors="pt",
        )
        with torch.no_grad():
            logits = model(input_ids=out["input_ids"], attention_mask=out["attention_mask"]).logits
        head = logits[:, 0, :] if logits.dim() == 3 else logits
        cons = float(torch.softmax(head, dim=-1)[0, halluc.HHEM_CONSISTENT].item())
    return 1.0 - cons


def _trace_pass(trace: dict, hhem_score: float, threshold: float = 0.3) -> bool:
    """Cheap online pass rule: word cap (<=150) AND HHEM score below threshold."""
    words = len((trace.get("output") or "").split())
    return words <= 150 and hhem_score < threshold


def score_sample(rows: list[dict], model, tok, threshold: float = 0.3) -> list[dict]:
    """Score sampled traces: HHEM (ch-09, CPU) + one cheap code check (word cap)."""
    out = []
    for row in rows:
        source = halluc.handbook_text_for(row)
        h = _hhem_score(model, tok, source, row.get("output") or "")
        words = len((row.get("output") or "").split())
        out.append(
            {
                "ticket_id": row["ticket_id"],
                "hhem_score": round(h, 6),
                "words": words,
                "words_ok": words <= 150,
                "pass": _trace_pass(row, h, threshold),
            }
        )
    return out


def build_monitor_table(plan: list[list[dict]], threshold: float = 0.3) -> tuple[list[dict], dict]:
    """Per-day sampled pass rate + pooled CI + alert flags.

    Pass rule (chapter 04 family): word cap (<= 150 words) AND HHEM score
    below threshold. Alert rule: a day whose sampled pass rate falls below
    the *pooled* (all-days) 95% CI lower bound is flagged — demonstrating
    how a thresholded monitor fires on a bad day while normal days do not.
    """
    import math

    model, tok = halluc.load_hhem()
    rows = []
    for i, day in enumerate(plan, start=1):
        scored = score_sample(day, model, tok, threshold=threshold)
        n = len(scored)
        passed = sum(1 for s in scored if s["pass"])
        rate = passed / n if n else 0.0
        se = math.sqrt(rate * (1 - rate) / n) if n and 0 < rate < 1 else 0.0
        rows.append(
            {
                "day": i,
                "n_sampled": n,
                "passed": passed,
                "rate": rate,
                "ci_lower": max(0.0, rate - 1.96 * se),
                "ci_upper": min(1.0, rate + 1.96 * se),
                "hhem_mean": round(sum(s["hhem_score"] for s in scored) / n, 4) if n else 0.0,
                "scored": scored,
            }
        )
    tot = sum(r["n_sampled"] for r in rows)
    ps = sum(r["passed"] for r in rows)
    overall = ps / tot if tot else 0.0
    se = math.sqrt(overall * (1 - overall) / tot) if tot and 0 < overall < 1 else 0.0
    lo = max(0.0, overall - 1.96 * se)
    hi = min(1.0, overall + 1.96 * se)
    any_alert = False
    for r in rows:
        r["overall"] = overall
        r["overall_ci_lower"] = lo
        r["overall_ci_upper"] = hi
        r["alert"] = bool(r["rate"] < lo)
        any_alert = any_alert or r["alert"]
    return rows, {"overall": overall, "lo": lo, "hi": hi, "alert": any_alert}


def _monitor_png(rows: list[dict], overall: float, lo: float, out: object) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 4))
    x = [r["day"] for r in rows]
    y = [r["rate"] for r in rows]
    yerr_lo = [r["rate"] - r["ci_lower"] for r in rows]
    yerr_hi = [r["ci_upper"] - r["rate"] for r in rows]
    ax.axhline(overall, color="k", ls="--", lw=1, label=f"overall pass rate {overall:.3f}")
    ax.axhline(lo, color="grey", ls=":", lw=1, label=f"overall 95% CI lower {lo:.3f} (alert line)")
    ax.errorbar(x, y, yerr=[yerr_lo, yerr_hi], fmt="o", color="#1f77b4", capsize=3, label="day rate ± 95% CI")
    for r in rows:
        if r["alert"]:
            ax.annotate("alert", (r["day"], r["rate"]), textcoords="offset points", xytext=(0, 8), ha="center", color="#d62728")
    ax.set_xlabel("day")
    ax.set_ylabel("pass rate")
    ax.set_title("chapter 13b — online monitor (20% sample/day, 7 seeded days)")
    ax.legend(loc="lower right")
    ax.set_xticks(x)
    ax.set_ylim(0, max(1.0, overall + 0.05))
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)


@app.command()
def monitor(
    sample: float = typer.Option(0.2, help="daily sample fraction of the trace pool"),
    days: int = typer.Option(7, help="number of seeded 'days'"),
    seed: int = typer.Option(0, help="seed for day partitioning + sampling"),
    threshold: float = typer.Option(0.3, help="HHEM score threshold (score >= threshold => fail)"),
    run: str = typer.Option("answer_v1", help="committed trace run to monitor"),
) -> None:
    """Simulate online monitoring on a 20% daily sample, 7 seeded days, HHEM + a cheap check."""
    traces = helpdesk.load_traces(run)
    plan = plan_days(traces, sample=sample, days=days, seed=seed)
    covered = sorted({t["ticket_id"] for d in plan for t in d})
    rows, agg = build_monitor_table(plan, threshold=threshold)
    out_dir = settings.path("runs") / "13_monitor"
    out_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Online monitor — chapter 13b",
        "",
        f"run `{run}`: {len(traces)} traces pooled over {days} seeded days, "
        f"sample={sample:.0%}/day, HHEM threshold={threshold} + one cheap check (max 150 words).",
        f"Pooled sampled pass: **{agg['overall']:.3f}** (95% CI [{agg['lo']:.3f}, {agg['hi']:.3f}]).",
        "Alert rule: day pass rate below the pooled 95% CI lower bound → flagged.",
        "",
        "| day | n | pass | rate ±CI | alert |",
        "|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['day']} | {r['n_sampled']} | {r['passed']} | {r['rate']:.3f} "
            f"[{r['ci_lower']:.3f},{r['ci_upper']:.3f}] | {'❗' if r['alert'] else ''} |"
        )
    (out_dir / "rolling.md").write_text("\n".join(lines) + "\n")
    _monitor_png(rows, agg["overall"], agg["lo"], out_dir / "rolling.png")
    flat = [
        {"day": r["day"], **{k: v for k, v in s.items()}}
        for r in rows
        for s in r["scored"]
    ]
    (out_dir / "scores.jsonl").write_text(
        "".join(json.dumps(x) + "\n" for x in flat)
    )
    write_metrics(
        f"13_monitor_{run}",
        13,
        sum(r["n_sampled"] for r in rows),
        {
            "sampled_pass": agg["overall"],
            "overall_ci_lower": agg["lo"],
            "overall_ci_upper": agg["hi"],
            "days": float(days),
            "sample_rate": sample,
            "threshold": threshold,
            "alerts": float(sum(1 for r in rows if r["alert"])),
        },
        ci={"sampled_pass": [agg["lo"], agg["hi"]]},
        llm_calls=0,
        details={
            "run": run,
            "n_traces": len(traces),
            "covered": covered,
            "days_rows": [
                {k: v for k, v in r.items() if k != "scored"}
                for r in rows
            ],
            "rules": "pass = words<=150 AND hhem_score<threshold; alert = day rate < pooled CI lower",
        },
        config={"sample": sample, "days": days, "seed": seed, "threshold": threshold},
        dir_name="13_monitor",
    )
    print(
        f"wrote {out_dir / 'rolling.md'} and {out_dir / 'rolling.png'}; "
        f"pooled sampled pass {agg['overall']:.3f} "
        f"(CI [{agg['lo']:.3f}, {agg['hi']:.3f}]), "
        f"{len(covered)}/{len(traces)} traces covered over {days} days, "
        f"alerts on {sum(1 for r in rows if r['alert'])} day(s)"
    )


if __name__ == "__main__":
    app()
