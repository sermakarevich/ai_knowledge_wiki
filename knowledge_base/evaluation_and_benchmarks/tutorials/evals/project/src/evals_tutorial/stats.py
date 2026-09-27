"""Chapter 07a: the shared statistics module.

Every number in ``runs/results.md`` is a point estimate on a small sample (60
tickets, 100-150 pairs). This module adds error bars and tests:

- ``bootstrap_ci`` / ``wilson_ci`` / ``clustered_bootstrap_ci`` -- 95 % CIs
- ``paired_bootstrap`` / ``mcnemar`` / ``permutation_test`` -- paired tests
- ``power_binary`` / ``power_paired`` -- sample-size planning
- ``bonferroni`` / ``benjamini_hochberg`` -- multiple-comparisons corrections
- ``retrofit`` -- bootstrap a 95 % CI onto every existing experiment by
  re-reading its ``predictions.jsonl``, resampling its rows, and writing the
  CI into ``metrics.json``; then rebuilds ``runs/results.md``.

Pure functions, NumPy only, every stochastic entry point takes a ``seed``.
Typer commands: ``ci``, ``paired``, ``power``, ``retrofit``. No network.
"""

from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path
from typing import Callable, Sequence

import numpy as np
import typer


# ---------------------------------------------------------------------------
# normal quantile (no scipy)
# ---------------------------------------------------------------------------


def z_alpha(alpha: float) -> float:
    """Two-sided critical value z with P(|Z| > z) = alpha (bisection on erf)."""
    target = 1 - alpha / 2

    def cdf(z: float) -> float:
        return 0.5 * (1 + math.erf(z / math.sqrt(2)))

    lo, hi = -8.0, 8.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if cdf(mid) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


# ---------------------------------------------------------------------------
# confidence intervals
# ---------------------------------------------------------------------------


def bootstrap_ci(
    values: Sequence[float],
    stat: Callable[[np.ndarray], float] = np.mean,
    n_boot: int = 2000,
    alpha: float = 0.05,
    seed: int = 0,
) -> tuple[float, float]:
    """Percentile bootstrap CI of ``stat`` over ``values``.

    Rows resampled with replacement ``n_boot`` times; the CI is the
    ``(alpha/2, 1 - alpha/2)`` percentiles of the bootstrap statistic.
    """
    x = np.asarray(values, dtype=float)
    n = x.size
    if n == 0:
        raise ValueError("bootstrap_ci: empty values")
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, n, size=(n_boot, n))
    dist = np.array([stat(x[i]) for i in idx])
    lo = float(np.percentile(dist, 100 * alpha / 2))
    hi = float(np.percentile(dist, 100 * (1 - alpha / 2)))
    return (lo, hi)


def wilson_ci(k: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    """Wilson score interval for a proportion ``k/n`` (no scipy needed)."""
    if n <= 0:
        raise ValueError("wilson_ci: n must be positive")
    if not 0 <= k <= n:
        raise ValueError("wilson_ci: k must be in [0, n]")
    p = k / n
    z = z_alpha(alpha)
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    lo = max(0.0, center - half)
    hi = min(1.0, center + half)
    return (float(lo), float(hi))


def clustered_bootstrap_ci(
    values: Sequence[float],
    clusters: Sequence[str | int] | None = None,
    stat: Callable[[np.ndarray], float] = np.mean,
    n_boot: int = 2000,
    alpha: float = 0.05,
    seed: int = 0,
) -> tuple[float, float]:
    """Bootstrap CI that resamples whole clusters (not rows).

    Tickets in the same cluster (e.g. the same ``topic``) are correlated, so
    plain row bootstrap understates uncertainty. Here each replicate keeps
    all rows of a randomly drawn cluster (drawn with replacement until we
    have as many clusters as the observed sample).

    ``clusters=None`` falls back to a plain row bootstrap.
    """
    x = np.asarray(values, dtype=float)
    n = x.size
    if n == 0:
        raise ValueError("clustered_bootstrap_ci: empty values")
    if clusters is None:
        return bootstrap_ci(x, stat=stat, n_boot=n_boot, alpha=alpha, seed=seed)
    cl = list(clusters)
    if n != len(cl):
        raise ValueError("clustered_bootstrap_ci: values/clusters length mismatch")
    pos: dict[str | int, list[int]] = {}
    for i, c in enumerate(cl):
        pos.setdefault(c, []).append(i)
    keys = list(pos)
    if len(keys) <= 1:
        v = round(float(stat(x)), 12)
        return (v, v)
    rng = np.random.default_rng(seed)
    dist: list[float] = []
    for _ in range(n_boot):
        pick = rng.integers(0, len(keys), size=len(keys))
        idx = np.concatenate([np.asarray(pos[keys[q]], dtype=int) for q in pick])
        dist.append(float(stat(x[idx])))
    lo = float(np.percentile(dist, 100 * alpha / 2))
    hi = float(np.percentile(dist, 100 * (1 - alpha / 2)))
    return (lo, hi)


# ---------------------------------------------------------------------------
# paired comparisons
# ---------------------------------------------------------------------------


def paired_bootstrap(
    a: Sequence[float],
    b: Sequence[float],
    n_boot: int = 2000,
    alpha: float = 0.05,
    seed: int = 0,
) -> dict:
    """Paired bootstrap difference ``mean(a) - mean(b)`` with CI and p-value.

    Pairs are resampled together (keeping the per-row alignment), so the CI
    is on the *paired* difference. Two-sided p is the share of bootstrap
    replicates as extreme as the observed one relative to 0.
    """
    ra = np.asarray(a, dtype=float)
    rb = np.asarray(b, dtype=float)
    if ra.size != rb.size or ra.size == 0:
        raise ValueError("paired_bootstrap: a and b must be equal-length, non-empty")
    diff0 = float(ra.mean() - rb.mean())
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, ra.size, size=(n_boot, ra.size))
    dist = np.array([float(ra[i].mean() - rb[i].mean()) for i in idx])
    lo = float(np.percentile(dist, 100 * alpha / 2))
    hi = float(np.percentile(dist, 100 * (1 - alpha / 2)))
    # two-sided p: fraction of bootstrap replicates on the other side of 0
    # (if the CI excludes zero, this is ~0/0 = min side ~ 1.0; we want it ~0)
    if diff0 == 0:
        p = 1.0
    else:
        p = float(2 * min(np.mean(dist <= 0), np.mean(dist >= 0)))
        p = min(1.0, max(p, 2.0 / n_boot))
    return {
        "mean_a": float(ra.mean()),
        "mean_b": float(rb.mean()),
        "diff": diff0,
        "ci": [lo, hi],
        "p_value": p,
    }


def mcnemar(a: Sequence[bool], b: Sequence[bool]) -> dict:
    """McNemar test on paired binary outcomes (exact, two-sided binomial)."""
    ra = np.asarray(a, dtype=bool)
    rb = np.asarray(b, dtype=bool)
    if ra.size != rb.size or ra.size == 0:
        raise ValueError("mcnemar: a and b must be equal-length, non-empty")
    b10 = int(np.sum(ra & ~rb))
    b01 = int(np.sum(~ra & rb))
    n = b10 + b01
    if n == 0:
        return {"b10": 0, "b01": 0, "p_value": 1.0, "statistic": None}
    # exact two-sided: sum PMF over counts i whose binom(n, 0.5) mass
    # is <= the observed mass, then multiply by 2. For i <= n/2 that equals
    # 2 * P(X <= min(b10, b01)); for i > n/2 it's 2 * P(X >= max(b10, b01)).
    from math import comb

    k = min(b10, b01)
    obs_mass = comb(n, k) * 0.5**n
    total = sum(comb(n, i) * 0.5**n for i in range(n + 1) if comb(n, i) * 0.5**n <= obs_mass)
    p = float(min(1.0, total))
    z = math.sqrt(n) if n else 0.0
    stat = (b10 - b01) / z if z else None
    return {"b10": b10, "b01": b01, "p_value": p, "statistic": stat}


def permutation_test(
    a: Sequence[float],
    b: Sequence[float],
    stat: Callable[[np.ndarray], float] = np.mean,
    n_perm: int = 10000,
    seed: int = 0,
) -> dict:
    """Randomization test of ``stat(a) - stat(b) == 0`` under label shuffling."""
    ra = np.asarray(a, dtype=float)
    rb = np.asarray(b, dtype=float)
    if ra.size == 0 or rb.size == 0:
        raise ValueError("permutation_test: a and b must be non-empty")
    pooled = np.concatenate([ra, rb])
    observed = float(stat(ra) - stat(rb))
    rng = np.random.default_rng(seed)
    na = ra.size
    counts = 0
    for _ in range(n_perm):
        rng.shuffle(pooled)
        d = float(stat(pooled[:na]) - stat(pooled[na:]))
        if abs(d) >= abs(observed) - 1e-12:
            counts += 1
    p = (counts + 1) / (n_perm + 1)
    return {"observed": observed, "p_value": float(p)}


# ---------------------------------------------------------------------------
# power
# ---------------------------------------------------------------------------


def power_binary(p0: float, delta: float, alpha: float = 0.05, power: float = 0.8) -> int:
    """Sample size per arm for a two-proportion unpaired test (normal approx)."""
    if not 0 <= p0 <= 1:
        raise ValueError("power_binary: p0 must be in [0, 1]")
    p1 = p0 + delta
    if not 0 <= p1 <= 1:
        raise ValueError("power_binary: p0 + delta must be in [0, 1]")
    if delta <= 0:
        raise ValueError("power_binary: delta must be > 0")
    za = z_alpha(alpha)
    zb = z_alpha(2 * (1 - power))
    pbar = (p0 + p1) / 2
    num = (za * math.sqrt(2 * pbar * (1 - pbar)) + zb * math.sqrt(p0 * (1 - p0) + p1 * (1 - p1))) ** 2
    den = delta * delta
    return int(math.ceil(num / den))


def power_paired(
    delta: float,
    q: float = 0.30,
    alpha: float = 0.05,
    power: float = 0.8,
    *,
    p_discordant: float | None = None,
) -> int:
    """Sample size (pairs) for a paired (McNemar) test, normal approximation.

    Standard formula (dropping the ``-delta^2`` correction term):

        n ~= (z_alpha + z_beta)^2 * q / delta^2

    where ``q`` (or ``p_discordant``) is the expected proportion of *discordant*
    pairs under the alternative and ``delta`` is the target pass-rate difference
    ``|mean(a) - mean(b)| = p10 - p01``. The discordant count carries the signal
    but its variance grows with ``q``, so *more* discordance needs *more* pairs
    (delta fixed, larger delta needs far fewer).

    Kept backwards-compatible: first positional arg is ``delta``; the old
    keyword-first signature ``power_paired(p_discordant, delta)`` still works
    via the ``p_discordant`` keyword.
    """
    if q is not None and p_discordant is not None:
        q = p_discordant  # explicit keyword wins
    if p_discordant is not None and q is None:
        q = p_discordant
    if not (0 < q <= 1):
        q = 0.30
    if not 0 < delta < 1:
        raise ValueError("power_paired: delta must be in (0, 1)")
    za = z_alpha(alpha)
    zb = z_alpha(2 * (1 - power))
    num = (za + zb) ** 2 * q
    den = delta * delta
    return int(math.ceil(num / den))


def _z_power(power: float) -> float:
    """z with P(Z < z) = power (power must be in (0.5, 1))."""
    if not 0.5 < power < 1.0:
        raise ValueError("_z_power: power must be in (0.5, 1)")
    return z_alpha(2 * (1 - power))


# ---------------------------------------------------------------------------
# multiple comparisons
# ---------------------------------------------------------------------------


def bonferroni(pvals: Sequence[float], m: int | None = None, alpha: float = 0.05) -> list[bool]:
    """Bonferroni: reject where m * p < alpha (equivalently p < alpha/m)."""
    ps = [float(p) for p in pvals]
    m = m if m is not None else len(ps)
    thresh = alpha / m
    return [p < thresh for p in ps]


def benjamini_hochberg(pvals: Sequence[float], alpha: float = 0.05) -> list[int]:
    """BH: indices rejected at FDR ``alpha`` (largest p meeting p <= rank*alpha/m,
    reject that and all stronger)."""
    ps = [float(p) for p in pvals]
    m = len(ps)
    if m == 0:
        return []
    order = np.argsort(ps)
    cut = max(
        (int(idx) for idx, rank in zip(order, range(1, m + 1)) if ps[idx] <= rank * alpha / m),
        key=lambda _i: ps[_i],
        default=None,
    )
    if cut is None:
        return []
    return sorted(i for i, p in enumerate(ps) if p <= ps[cut])


# ---------------------------------------------------------------------------
# retrofit: per-experiment primary recomputed from resampled rows
# ---------------------------------------------------------------------------


def _f1(prec: float, rec: float) -> float:
    return 0.0 if (prec + rec) == 0 else 2 * prec * rec / (prec + rec)


def _f1_macro(rows: list[dict]) -> float:
    cats = sorted({r["gold"]["category"] for r in rows} | {r["prediction"]["category"] for r in rows if r.get("prediction", {}).get("category")})
    f1s = []
    for lab in cats:
        tp = sum(1 for r in rows if r["gold"]["category"] == lab and r["prediction"]["category"] == lab)
        fp = sum(1 for r in rows if r["gold"]["category"] != lab and r["prediction"]["category"] == lab)
        fn = sum(1 for r in rows if r["gold"]["category"] == lab and r["prediction"]["category"] != lab)
        f1s.append(_f1(tp / (tp + fp) if tp + fp else 0.0, tp / (tp + fn) if tp + fn else 0.0))
    return sum(f1s) / len(f1s) if f1s else 0.0


def _kappa(rows: list[dict], t: str = "true_fail", p: str = "pred_fail") -> float:
    y = [bool(r[t]) for r in rows]
    x = [bool(r[p]) for r in rows]
    n = len(y)
    if n == 0:
        return 0.0
    obs = sum(1 for i in range(n) if y[i] == x[i]) / n
    pt = sum(y) / n
    px = sum(x) / n
    exp = pt * px + (1 - pt) * (1 - px)
    if exp >= 1.0 - 1e-12:
        return 1.0 if obs >= 1.0 - 1e-12 else 0.0
    return (obs - exp) / (1 - exp)


def _auroc(rows: list[dict], score: str = "score", label: str = "true_fail") -> float:
    pos = [r[score] for r in rows if r[label]]
    neg = [r[score] for r in rows if not r[label]]
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


def _agreement(rows: list[dict]) -> float:
    if not rows:
        return 0.0
    return sum(1 for r in rows if r["score"] >= 0.5) / len(rows)


def _flip_rate(rows: list[dict]) -> float:
    if not rows:
        return 0.0
    return 1.0 - _agreement(rows)


def _bt_spearman(rows: list[dict]) -> float:
    models = [r["id"] for r in rows]
    human = {r["id"]: r["output"]["human"] for r in rows}
    qwen = {r["id"]: r["output"]["qwen"] for r in rows}
    if len(models) < 2:
        return 0.0

    def ranks(tbl: dict[str, float]) -> list[float]:
        pairs = sorted(((tbl[m], m) for m in models), key=lambda t: t[0])
        rk: dict[str, float] = {}
        i = 0
        while i < len(pairs):
            j = i
            while j + 1 < len(pairs) and pairs[j + 1][0] == pairs[i][0]:
                j += 1
            avg = (i + j) / 2 + 1
            for kk in range(i, j + 1):
                rk[pairs[kk][1]] = avg
            i = j + 1
        return [rk[m] for m in models]

    x = ranks(human)
    y = ranks(qwen)
    n = len(models)
    mx = sum(x) / n
    my = sum(y) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(x, y))
    vx = (sum((a - mx) ** 2 for a in x)) ** 0.5
    vy = (sum((b - my) ** 2 for b in y)) ** 0.5
    if vx == 0 or vy == 0:
        return 0.0
    return cov / (vx * vy)


# experiment -> how to recompute its *primary* metric from resampled rows,
# and (for ticket-based runs) which field to join to a ticket ``topic`` for
# the clustered CI; `None` means no clustered variant for that run.
RETROFIT_MAP: dict[str, dict] = {
    "04_triage_v1": {
        "stat": _f1_macro,
        "primary": "f1_macro",
        "cluster_field": "ticket_id",
    },
    "04_checks_answer_v1": {
        "stat": lambda rows: sum(1 for r in rows if r["pass"]) / len(rows) if rows else 0.0,
        "primary": "all_checks_pass",
        "cluster_field": "ticket_id",
    },
    "04_similarity_answer_v1": {
        "stat": lambda rows: _auroc(rows, "embed_cosine", "pass"),
        "primary": "auroc_embed_vs_label",
        "cluster_field": "ticket_id",
    },
    "05_judge_did_not_answer": {"stat": lambda rows: _kappa(rows), "primary": "kappa", "cluster_field": "ticket_id"},
    "05_judge_missing_required_fact": {"stat": lambda rows: _kappa(rows), "primary": "kappa", "cluster_field": "ticket_id"},
    "05_judge_missing_required_fact_nocontext": {"stat": lambda rows: _kappa(rows), "primary": "kappa", "cluster_field": "ticket_id"},
    "05_judge_overall": {"stat": lambda rows: _kappa(rows, "true_pass", "pred_pass"), "primary": "kappa", "cluster_field": "ticket_id"},
    "05_judge_unsupported_claim": {"stat": lambda rows: _kappa(rows), "primary": "kappa", "cluster_field": "ticket_id"},
    "05_judge_wrong_section_retrieved": {"stat": lambda rows: _kappa(rows), "primary": "kappa", "cluster_field": "ticket_id"},
    "05_likert_overall": {"stat": lambda rows: _auroc(rows, "score", "true_fail"), "primary": "auroc", "cluster_field": "ticket_id"},
    "06_agreement_atla_selene-mini": {"stat": _agreement, "primary": "agreement_with_humans", "cluster_field": None},
    "06_agreement_gemma4_latest": {"stat": _agreement, "primary": "agreement_with_humans", "cluster_field": None},
    "06_agreement_qwen3.8_27b": {"stat": _agreement, "primary": "agreement_with_humans", "cluster_field": None},
    "06_bias_atla_selene-mini": {"stat": _flip_rate, "primary": "position_flip_rate", "cluster_field": None},
    "06_bias_gemma4_latest": {"stat": _flip_rate, "primary": "position_flip_rate", "cluster_field": None},
    "06_bias_qwen3.8_27b": {"stat": _flip_rate, "primary": "position_flip_rate", "cluster_field": None},
    "06_bradley_terry": {"stat": _bt_spearman, "primary": "spearman_rho", "cluster_field": None},
    "06_panel": {"stat": _agreement, "primary": "panel_agreement", "cluster_field": None},
}


def retrofit(
    project_root: Path | None = None,
    n_boot: int = 2000,
    seed: int = 0,
    rebuild: bool = True,
) -> list[Path]:
    """Add a 95 % CI (plus a clustered CI when possible) to every experiment.

    Reads each experiment's ``predictions.jsonl``, resamples its rows,
    recomputes the primary metric on each resample, and writes the CI into
    its ``metrics.json`` under ``ci[<primary>]``. For ticket-based runs it
    also computes a CI that resamples whole topic clusters. Returns the list
    of ``metrics.json`` paths touched; then rebuilds ``runs/results.md``.
    """
    from evals_tutorial import results as R

    runs = R._runs_dir(project_root)
    # ticket-id -> topic map (lazy; only if we have ticket rows to cluster on)
    ticket_topic: dict[str, str] = {}
    try:
        from evals_tutorial.tickets import load_tickets

        for t in load_tickets():
            ticket_topic[t["id"]] = t.get("topic", "")
    except Exception:
        pass

    written: list[Path] = []
    for exp, spec in RETROFIT_MAP.items():
        exp_dir = runs / exp
        metrics_path = exp_dir / "metrics.json"
        preds_path = exp_dir / "predictions.jsonl"
        if not metrics_path.exists() or not preds_path.exists():
            continue
        rows = [json.loads(line) for line in preds_path.read_text().splitlines() if line.strip()]
        if not rows:
            continue
        stat: Callable[[list[dict]], float] = spec["stat"]
        n = len(rows)
        rng = np.random.default_rng(seed)
        idx_boot = rng.integers(0, n, size=(n_boot, n))
        dist = np.array([stat([rows[i] for i in idx]) for idx in idx_boot])
        lo = float(np.percentile(dist, 2.5))
        hi = float(np.percentile(dist, 97.5))
        record = json.loads(metrics_path.read_text())
        record.setdefault("ci", {})[spec["primary"]] = [round(lo, 6), round(hi, 6)]
        # clustered CI: resample whole topics (ticket-based runs only)
        cf = spec.get("cluster_field")
        if cf and cf in rows[0] and all(r.get(cf) in ticket_topic for r in rows):
            clusters = [ticket_topic[r[cf]] for r in rows]
            pos: dict[str, list[int]] = {}
            for i, c in enumerate(clusters):
                pos.setdefault(c, []).append(i)
            keys = list(pos)
            if len(keys) >= 2:
                rng2 = np.random.default_rng(seed + 1)
                cdist: list[float] = []
                for _ in range(n_boot):
                    pick = rng2.integers(0, len(keys), size=len(keys))
                    cidx = np.concatenate([np.asarray(pos[keys[q]], dtype=int) for q in pick])
                    cdist.append(float(stat([rows[i] for i in cidx])))
                cl_lo = float(np.percentile(cdist, 2.5))
                cl_hi = float(np.percentile(cdist, 97.5))
                record.setdefault("details", {}).setdefault("clustered_ci", {})[spec["primary"]] = [round(cl_lo, 6), round(cl_hi, 6)]
                record["details"]["clustered_ci"]["method"] = f"bootstrap-by-cluster ({cf} -> ticket topic)"
        metrics_path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")
        written.append(metrics_path)
    if rebuild:
        R.build(project_root)
    return written


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

app = typer.Typer(add_completion=False, help="Evals statistics (CIs, paired tests, power, multiple comparisons).")


@app.command(name="ci")
def ci(
    experiment: str = typer.Option("05_likert_overall", help="experiment dir name"),
    n_boot: int = typer.Option(2000, help="bootstrap replicates"),
    seed: int = typer.Option(0, help="seed (reproducible)"),
    alpha: float = typer.Option(0.05, help="two-sided alpha"),
) -> None:
    """Print the bootstrap CI for one experiment's primary metric (from predictions.jsonl)."""
    from evals_tutorial import results as R

    spec = RETROFIT_MAP[experiment]
    rows_path = R._runs_dir(None) / experiment / "predictions.jsonl"
    rows = [json.loads(l) for l in rows_path.read_text().splitlines() if l.strip()]
    stat = spec["stat"]
    n = len(rows)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, n, size=(n_boot, n))
    dist = np.array([stat([rows[i] for i in ix]) for ix in idx])
    lo = float(np.percentile(dist, 100 * alpha / 2))
    hi = float(np.percentile(dist, 100 * (1 - alpha / 2)))
    print(f"{experiment}: {spec['primary']}: n={n}, CI[{alpha/2*100:g}%,{100 - alpha/2*100:g}%] = [{lo:.4f}, {hi:.4f}]")


# ---------------------------------------------------------------------------
# A/B: answer_v1 vs answer_v2 (chapter 07)
# ---------------------------------------------------------------------------


def _load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"A/B source not found: {path}")
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def _load_ticket_topics(project_root: Path | None = None) -> dict[str, str]:
    try:
        from evals_tutorial.tickets import load_tickets

        return {t["id"]: t.get("topic", "") for t in load_tickets()}
    except Exception:
        return {}


def ab_answer_v2_vs_v1(
    project_root: Path | None = None,
    n_boot: int = 2000,
    seed: int = 0,
    alpha: float = 0.05,
) -> list[Path]:
    """Paired A/B comparison of `answer_v1` vs `answer_v2` on the test split.

    Primary (judge-vs-judge): `05_judge_overall` vs `07_answer_v2_judged_overall`
    Same frozen judge, same 60 test tickets; only the SUT prompt changes.

    Secondary: per-check pass rates (`04_checks_answer_v1` vs `04_checks_answer_v2`)
    with multiple-comparisons corrections (Bonferroni + BH).

    Writes two experiments:
    - `07_ab_answer_v2_vs_v1`  (primary `pass_rate_delta`)
    - `07_answer_v2_pass_rate` (primary `pass_rate`)

    Returns the list of metrics.json paths written.
    """
    from evals_tutorial import results as R

    runs = R._runs_dir(project_root)
    ticket_topic = _load_ticket_topics(project_root)

    # --- load all sources ---------------------------------------------------
    v1_overall_rows = _load_jsonl(runs / "05_judge_overall" / "predictions.jsonl")
    v2_overall_rows = _load_jsonl(runs / "07_answer_v2_judged_overall" / "predictions.jsonl")

    v1_map = {r["ticket_id"]: r["pred_pass"] for r in v1_overall_rows if r["split"] == "test"}
    v2_map = {r["ticket_id"]: r["pred_pass"] for r in v2_overall_rows if r["split"] == "test"}

    # keep only tickets present in both, aligned by ticket_id (test split)
    common_ids = sorted(set(v1_map) & set(v2_map))
    if len(common_ids) < 2:
        raise ValueError(f"A/B: need at least 2 test tickets in both runs, got {len(common_ids)}")

    y1 = [1.0 if v1_map[tid] else 0.0 for tid in common_ids]
    y2 = [1.0 if v2_map[tid] else 0.0 for tid in common_ids]
    n = len(common_ids)
    clusters = [ticket_topic.get(tid, "") for tid in common_ids]

    # --- primary: judge-vs-judge pass-rate delta ------------------------------
    pb = paired_bootstrap(y1, y2, n_boot=n_boot, seed=seed, alpha=alpha)
    mn_overall = mcnemar([v > 0.5 for v in y1], [v > 0.5 for v in y2])

    # --- plain & clustered bootstrap CIs on pass_rate_v2 -----------------------
    plain_ci_v2 = bootstrap_ci(y2, n_boot=n_boot, alpha=alpha, seed=seed)
    clustered_ci_v2 = clustered_bootstrap_ci(
        y2, clusters=list(clusters), n_boot=n_boot, alpha=alpha, seed=seed + 1
    )

    # --- per-check comparison (secondary) -------------------------------------
    v1_checks_path = runs / "04_checks_answer_v1" / "predictions.jsonl"
    v2_checks_path = runs / "04_checks_answer_v2" / "predictions.jsonl"

    per_check: dict[str, dict] = {}
    if v1_checks_path.exists() and v2_checks_path.exists():
        v1_checks = _load_jsonl(v1_checks_path)
        v2_checks = _load_jsonl(v2_checks_path)
        v1c_map = {r["ticket_id"]: r.get("checks", {}) for r in v1_checks if r["split"] == "test"}
        v2c_map = {r["ticket_id"]: r.get("checks", {}) for r in v2_checks if r["split"] == "test"}
        check_ids = sorted({c for checks in v1c_map.values() for c in checks} |
                           {c for checks in v2c_map.values() for c in checks})
        raw_pvals: list[float] = []
        for check in check_ids:
            c1 = [1.0 if v1c_map.get(tid, {}).get(check) else 0.0 for tid in common_ids if tid in v1c_map]
            c2 = [1.0 if v2c_map.get(tid, {}).get(check) else 0.0 for tid in common_ids if tid in v2c_map]
            if len(c1) < 2 or len(c2) < 2:
                continue
            pb_c = paired_bootstrap(c1, c2, n_boot=n_boot, seed=seed, alpha=alpha)
            mn_c = mcnemar([v > 0.5 for v in c1], [v > 0.5 for v in c2])
            raw_pvals.append(mn_c["p_value"])
            per_check[check] = {
                "pass_rate_v1": round(pc1 := sum(c1) / len(c1), 6),
                "pass_rate_v2": round(pc2 := sum(c2) / len(c2), 6),
                "delta": round(pc2 - pc1, 6),
                "mcnemar_p": round(mn_c["p_value"], 6),
                "bootstrap_p": round(pb_c["p_value"], 6),
            }
        bonf_rej = bonferroni(raw_pvals, alpha=alpha) if raw_pvals else []
        bh_rej = benjamini_hochberg(raw_pvals, alpha=alpha) if raw_pvals else []
        if raw_pvals:
            for i, (check, p) in enumerate(zip(per_check.keys(), raw_pvals)):
                per_check[check]["bonferroni_rejected"] = bonf_rej[i]
                per_check[check]["bh_rejected"] = i in bh_rej
    else:
        raw_pvals = []
        bonf_rej = []
        bh_rej = []

    # --- per-topic table -------------------------------------------------------
    topic_stats: dict[str, dict] = {}
    for tid, topic in zip(common_ids, clusters):
        t = topic or "(untagged)"
        topic_stats.setdefault(t, {"n": 0, "v1_pass": 0, "v2_pass": 0})
        topic_stats[t]["n"] += 1
        topic_stats[t]["v1_pass"] += 1 if v1_map[tid] else 0
        topic_stats[t]["v2_pass"] += 1 if v2_map[tid] else 0

    # --- write: 07_ab_answer_v2_vs_v1 ------------------------------------------
    details = {
        "primary": "pass_rate_delta",
        "n_pairs": n,
        "pass_rate_v1": round(pb["mean_a"], 6),
        "pass_rate_v2": round(pb["mean_b"], 6),
        "ci_v2_plain": [round(x, 6) for x in plain_ci_v2],
        "ci_v2_clustered": [round(x, 6) for x in clustered_ci_v2],
        "mcnemar": mn_overall,
        "bootstrap": pb,
        "per_check": per_check,
        "multiple_comparisons": {
            "n_checks": len(per_check),
            "bonferroni_rejected": list(bonf_rej),
            "bh_rejected_indices": bh_rej,
        },
        "per_topic": topic_stats,
        "notes": "v2 (new prompt) vs v1 (baseline), test split, same frozen judge",
    }
    ab_preds = [
        {
            "ticket_id": tid,
            "pass_v1": v1_map[tid],
            "pass_v2": v2_map[tid],
            "agreement": v1_map[tid] == v2_map[tid],
        }
        for tid in common_ids
    ]
    p1 = R.write_metrics(
        experiment="07_ab_answer_v2_vs_v1",
        chapter="07",
        n=n,
        metrics={
            "pass_rate_delta": round(pb["diff"], 6),
            "pass_rate_v1": round(pb["mean_a"], 6),
            "pass_rate_v2": round(pb["mean_b"], 6),
            "mcnemar_p": round(mn_overall["p_value"], 6),
            "bootstrap_p": round(pb["p_value"], 6),
        },
        ci={"pass_rate_delta": [round(pb["ci"][0], 6), round(pb["ci"][1], 6)]},
        details=details,
        predictions=ab_preds,
        config={"a_run": "answer_v1", "b_run": "answer_v2", "n_boot": n_boot, "seed": seed, "alpha": alpha},
        project_root=project_root,
    )

    # --- write: 07_answer_v2_pass_rate -----------------------------------------
    v2_pr = pb["mean_b"]
    v2_preds = [{"ticket_id": tid, "pass": v2_map[tid]} for tid in common_ids]
    p2 = R.write_metrics(
        experiment="07_answer_v2_pass_rate",
        chapter="07",
        n=n,
        metrics={"pass_rate": round(v2_pr, 6), "ci_plain": [round(plain_ci_v2[0], 6), round(plain_ci_v2[1], 6)],
                 "ci_clustered": [round(clustered_ci_v2[0], 6), round(clustered_ci_v2[1], 6)]},
        details={
            "primary": "pass_rate",
            "run": "answer_v2",
            "split": "test",
        },
        predictions=v2_preds,
        config={"run": "answer_v2", "seed": seed, "n_boot": n_boot},
        project_root=project_root,
    )

    R.build(project_root)
    return [p1, p2]


@app.command(name="paired")
def paired(
    a: str = typer.Option(..., help="array of floats OR run name (e.g. answer_v1)"),
    b: str = typer.Option(..., help="array of floats OR run name (e.g. answer_v2)"),
    n_boot: int = typer.Option(2000, help="bootstrap replicates"),
    seed: int = typer.Option(0, help="seed (reproducible)"),
) -> None:
    """Paired bootstrap + McNemar: inline float arrays OR run-name A/B (07b).

    If `a` and `b` look like run names (contain `_v1`/`_v2` or match
    `answer_v1`/`answer_v2`), the A/B experiment is written under
    `07_ab_answer_v2_vs_v1` and `07_answer_v2_pass_rate`.
    Otherwise they are parsed as whitespace/comma-separated float arrays.
    """
    RUN_NAMES = {"answer_v1", "answer_v2"}

    def is_run_name(s: str) -> bool:
        s = s.strip().lower()
        return s in RUN_NAMES or ("_v" in s and " " not in s and "," not in s and s not in ("",))

    if is_run_name(a) and is_run_name(b):
        paths = ab_answer_v2_vs_v1(n_boot=n_boot, seed=seed)
        for p in paths:
            print(f"wrote {p}")
        print("07_ab_answer_v2_vs_v1 + 07_answer_v2_pass_rate written; results.md rebuilt")
        return

    def parse(s: str) -> list[float]:
        return [float(x) for x in s.replace(",", " ").split() if x.strip() != ""]

    ra, rb = parse(a), parse(b)
    res = paired_bootstrap(ra, rb, n_boot=n_boot, seed=seed)
    print(f"mean a = {res['mean_a']:.4f}, mean b = {res['mean_b']:.4f}")
    print(f"diff (a - b) = {res['diff']:.4f}  CI = [{res['ci'][0]:.4f}, {res['ci'][1]:.4f}]  p(2-sided bootstrap) = {res['p_value']:.4f}")
    m = mcnemar([v > 0.5 for v in ra], [v > 0.5 for v in rb])
    print(f"mcnemar: b10={m['b10']}, b01={m['b01']}, exact p = {m['p_value']:.4f}")


@app.command(name="power")
def power(
    p0: float = typer.Option(0.5, help="baseline proportion (0..1)"),
    deltas: str = typer.Option("0.05,0.10,0.20", help="comma-separated absolute differences"),
    alphas: str = typer.Option("0.05,0.01", help="comma-separated FWER per comparison"),
    powers: str = typer.Option("0.80,0.90", help="comma-separated power values"),
) -> None:
    """Print a small power table for a two-proportion unpaired test."""
    al = [float(x) for x in alphas.split(",") if x.strip()]
    pw = [float(x) for x in powers.split(",") if x.strip()]
    ds = [float(x) for x in deltas.split(",") if x.strip()]
    header = ["delta"] + [f"alpha={a},power={p}" for a in al for p in pw]
    widths = [7] + [22] * len(al) * len(pw)
    line = " | ".join(f"{h:<{w}}" for h, w in zip(header, widths))
    print(line)
    print("-" * len(line))
    for d in ds:
        cells = [f"{d:g}"]
        for a in al:
            for p in pw:
                try:
                    cells.append(str(power_binary(p0, d, alpha=a, power=p)))
                except ValueError:
                    cells.append("n/a")
        print(" | ".join(f"{c:<{w}}" for c, w in zip(cells, widths)))
    print()
    print(f"paired (McNemar) size at p_discordant=0.30, delta: " + ", ".join(
        f"{d:g}->{power_paired(d, 0.30)}" for d in ds
    ))


@app.command(name="retrofit")
def retrofit_cmd(
    n_boot: int = typer.Option(2000, help="bootstrap replicates"),
    seed: int = typer.Option(0, help="seed (reproducible)"),
) -> None:
    """Bootstrap a 95 % CI onto every existing runs/*/metrics.json, then rebuild runs/results.md."""
    paths = retrofit(n_boot=n_boot, seed=seed)
    print(f"retrofitted {len(paths)} experiments -> metrics.json; runs/results.md rebuilt")


if __name__ == "__main__":
    app()
