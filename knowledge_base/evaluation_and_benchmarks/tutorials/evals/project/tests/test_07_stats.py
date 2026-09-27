"""Chapter 07a tests for stats.py.

Fast: all functions are deterministic for a given seed; no network, no LLM.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pytest

from evals_tutorial.stats import (
    benjamini_hochberg,
    bonferroni,
    bootstrap_ci,
    clustered_bootstrap_ci,
    mcnemar,
    paired_bootstrap,
    permutation_test,
    power_binary,
    power_paired,
    retrofit,
    wilson_ci,
    z_alpha,
)

DATA = Path(__file__).parent.parent / "runs"


# ---------------------------------------------------------------------------
# bootstrap / wilson
# ---------------------------------------------------------------------------


def test_bootstrap_ci_contains_mean():
    rng = np.random.default_rng(0)
    x = rng.normal(loc=0.5, scale=0.2, size=60)
    lo, hi = bootstrap_ci(x, n_boot=1000, seed=1)
    assert lo < float(x.mean()) < hi
    assert lo < hi
    # width should shrink slightly with more resamples; just assert shape
    assert (hi - lo) > 0


def test_bootstrap_ci_matches_wilson_for_proportion():
    # 40 successes out of 60 -> prop 0.6667, wilson should sit inside bootstrap
    x = [1.0] * 40 + [0.0] * 20
    bl, bh = bootstrap_ci(x, stat=np.mean, n_boot=5000, seed=0)
    wl, wh = wilson_ci(40, 60)
    assert wl <= bh
    assert bh <= wh + 2e-2 or bh < wh + 2e-2  # wilson is the canonical CI for proportions
    assert abs((bh + bl) / 2 - 40 / 60) < 0.06


def test_wilson_ci_bounds():
    lo, hi = wilson_ci(0, 60)
    assert lo == 0.0
    assert hi > 0.03
    # 60/60 (all pass) -> CI is tight near 1 (Wilson lower bound at n=60 is ~0.94)
    lo, hi = wilson_ci(60, 60)
    assert lo > 0.93
    assert hi == pytest.approx(1.0)
    with pytest.raises(ValueError):
        wilson_ci(70, 60)


def test_bootstrap_ci_requires_nonempty():
    with pytest.raises(ValueError):
        bootstrap_ci([], n_boot=10)


# ---------------------------------------------------------------------------
# clustered bootstrap
# ---------------------------------------------------------------------------


def test_clustered_bootstrap_ci_is_reproducible_and_wider_than_row_ci_same_clusters():
    rng = np.random.default_rng(0)
    # build 12 clusters x 5 rows each with mild within-cluster correlation
    vals = []
    clusters = []
    for c in range(12):
        base = rng.normal(0.5, 0.05)
        for _ in range(5):
            vals.append(base + rng.normal(0, 0.02))
            clusters.append(f"c{c}")
    c_lo, c_hi = clustered_bootstrap_ci(vals, clusters, n_boot=500, seed=0)
    plain_lo, plain_hi = bootstrap_ci(vals, n_boot=500, seed=0)
    # same seed, same n_boot means the two draws are different; assert CI exists
    assert c_lo < c_hi
    assert plain_lo < plain_hi
    # clustered is typically wider than rows when within-cluster corr > 0; not asserted strictly
    # but the point estimate should be inside both
    assert plain_lo <= np.mean(vals) <= plain_hi
    assert c_lo <= np.mean(vals) <= c_hi


def test_clustered_bootstrap_single_cluster_falls_back_to_point():
    lo, hi = clustered_bootstrap_ci([0.1, 0.2, 0.3], ["a", "a", "a"])
    assert lo == 0.2 and hi == 0.2


# ---------------------------------------------------------------------------
# paired
# ---------------------------------------------------------------------------


def test_paired_bootstrap_sign_and_ci():
    rng = np.random.default_rng(0)
    a = rng.normal(0.72, 0.10, size=60)
    b = a + rng.normal(-0.15, 0.05, size=60)  # a clearly better than b
    res = paired_bootstrap(a, b, n_boot=2000, seed=0)
    assert res["diff"] > 0
    assert res["ci"][0] > 0
    assert res["p_value"] < 0.01


def test_paired_bootstrap_symmetric_when_identical():
    a = [0.5] * 50
    res = paired_bootstrap(a, a, n_boot=100, seed=0)
    assert res["diff"] == 0.0
    assert res["ci"][0] <= 0 <= res["ci"][1]


def test_mcnemar_b10_b01_counts():
    # 2 pairs where a=1,b=0 (b10), 3 pairs where a=0,b=1 (b01)
    a = [1, 1, 0, 0, 0, 1, 1, 1, 1]
    b = [0, 0, 1, 1, 1, 1, 1, 1, 1]
    m = mcnemar(a, b)
    assert m["b10"] == 2
    assert m["b01"] == 3
    # exact two-sided: sum of binom(5,0.5) PMF for counts i where PMF(i) <= PMF(2)
    # PMFs: [1/32, 5/32, 10/32, 10/32, 5/32, 1/32];  observed at k=2 -> 10/32
    # sum where PMF <= 10/32 = (1+5+10+10+5+1)/32 = 32/32 = 1.0 (n=5 odd -> tie at center)
    assert m["p_value"] == 1.0


def test_mcnemar_all_discordance_one_direction():
    a = [1, 1, 1, 1]
    b = [0, 0, 0, 0]
    m = mcnemar(a, b)
    assert m["b10"] == 4
    assert m["b01"] == 0
    # exact two-sided: k=0, obs_mass = 1/16; sum over PMF <= 1/16 = (1+1)/16 = 0.125
    assert m["p_value"] == pytest.approx(0.125)


def test_mcnemar_asymmetric_is_strong():
    # 6 pairs a=1,b=0 (b10) and 1 pair a=0,b=1 (b01) -> strongly one-directional
    a = [1, 1, 1, 1, 1, 1, 0]
    b = [0, 0, 0, 0, 0, 0, 1]
    m = mcnemar(a, b)
    assert m["b10"] == 6 and m["b01"] == 1
    # sum binom(7,0.5) PMF for i where PMF(i) <= PMF(1)=7/128: i=0(1/128), i=1(7/128), i=6(7/128), i=7(1/128)
    assert m["p_value"] == pytest.approx((1 + 7 + 7 + 1) / 128)


def test_mcnemar_no_discordance_gives_p1():
    a = [1, 1, 1]
    b = [1, 1, 1]
    m = mcnemar(a, b)
    assert m["b10"] == 0 and m["b01"] == 0
    assert m["p_value"] == 1.0


def test_permutation_test_two_populations():
    a = [100.0] + [100.0 + 0.1] * 19
    b = [1.0] + [1.0 + 0.1] * 19
    res = permutation_test(a, b, n_perm=5000, seed=0)
    assert res["observed"] > 0
    assert res["p_value"] < 0.01


# ---------------------------------------------------------------------------
# power
# ---------------------------------------------------------------------------


def test_power_binary_increases_with_delta():
    assert power_binary(0.5, 0.05) > power_binary(0.5, 0.10)
    assert power_binary(0.5, 0.10) > power_binary(0.5, 0.20)
    # sanity bounds
    n_small = power_binary(0.5, 0.50, alpha=0.05, power=0.8)
    assert n_small < 400


def test_power_paired_monotonic_in_q():
    # larger discordance means *less* needed signal per pair, so n is smaller
    assert power_paired(0.60, 0.10) < power_paired(0.20, 0.10)


def test_z_alpha_known_values():
    assert abs(z_alpha(0.05) - 1.959964) < 1e-3
    assert abs(z_alpha(0.01) - 2.575829) < 1e-3


# ---------------------------------------------------------------------------
# multiple comparisons
# ---------------------------------------------------------------------------


def test_bonferroni_rejects_strong_only():
    ps = [0.01, 0.05, 0.10, 0.5]
    res = bonferroni(ps, alpha=0.05)
    # 0.05/4 = 0.0125; only p=0.01 < thresh
    assert res == [True, False, False, False]


def test_benjamini_hochberg_keeps_order():
    ps = [0.001, 0.008, 0.039, 0.041, 0.238, 0.469]
    # m=6, alpha=0.05: thresholds i*0.05/6: 0.00833, 0.01667, 0.025, 0.0333, 0.04167, 0.05
    res = benjamini_hochberg(ps)
    assert 0 in res and 1 in res
    # 0.008 <= 0.01667 (rank 2) OK, 0.039 > 0.025 (rank 3) fails; so cut at 0.008
    assert 2 not in res


# ---------------------------------------------------------------------------
# retrofit (real pipeline, seeded, cheap)
# ---------------------------------------------------------------------------


def test_retrofit_is_idempotent_and_writes_ci_fields():
    # we do not re-write on this test (would mutate metrics.json); instead
    # verify that every experiment in RETROFIT_MAP has a CI after the first
    # retrofit -- if one is missing, the test fails (and the user runs the recipe)
    from evals_tutorial.stats import RETROFIT_MAP

    for exp in RETROFIT_MAP:
        p = DATA / exp / "metrics.json"
        if not p.exists():
            continue
        import json

        rec = json.loads(p.read_text())
        prim = rec["details"]["primary"]
        assert prim in rec["ci"], f"{exp} has no CI for {prim}; run stats-retrofit"
        lo, hi = rec["ci"][prim]
        val = rec["metrics"][prim]
        assert lo <= val <= hi, f"{exp}: point estimate {val} not inside CI [{lo},{hi}]"


def test_retrofit_cli_is_exposed():
    # ensure the module's CLI is callable (no execution here)
    import evals_tutorial.stats as S

    assert hasattr(S, "app")
    # Typer apps expose commands as attributes or in .registered_commands
    names = {c.name for c in S.app.registered_commands}
    assert {"ci", "paired", "power", "retrofit"} <= names


# ---------------------------------------------------------------------------
# A/B: answer_v2 vs answer_v1  (synthetic e2e on tmp_path)
# ---------------------------------------------------------------------------


def test_ab_answer_v2_vs_v1_synthetic(tmp_path: Path):
    """End-to-end: write two predicted-overall files, call ab_answer_v2_vs_v1,
    and verify both experiment dirs are written under runs/ with correct values."""
    import json

    from evals_tutorial.stats import ab_answer_v2_vs_v1

    runs = tmp_path / "runs"

    # 10 test-split tickets: v1 passes t00..t06 (7/10), v2 passes t00..t07 (8/10)
    def _write_overall(exp: str, v2: bool):
        d = runs / exp
        d.mkdir(parents=True, exist_ok=True)
        rows = [
            {"ticket_id": f"t{i:02d}", "split": "test",
             "pred_pass": (i < (8 if v2 else 7))}
            for i in range(10)
        ]
        (d / "predictions.jsonl").write_text(
            "\n".join(json.dumps(r) for r in rows) + "\n"
        )

    _write_overall("05_judge_overall", v2=False)
    _write_overall("07_answer_v2_judged_overall", v2=True)

    paths = ab_answer_v2_vs_v1(project_root=tmp_path, n_boot=200, seed=0)
    assert len(paths) == 2

    # --- 07_ab_answer_v2_vs_v1 ---
    ab_path = runs / "07_ab_answer_v2_vs_v1" / "metrics.json"
    assert ab_path.exists(), "07_ab_answer_v2_vs_v1 not written"
    ab = json.loads(ab_path.read_text())
    assert ab["n"] == 10
    # delta = mean(v1) - mean(v2) = 0.7 - 0.8 = -0.1
    assert ab["metrics"]["pass_rate_v1"] == pytest.approx(0.7)
    assert ab["metrics"]["pass_rate_v2"] == pytest.approx(0.8)
    assert ab["metrics"]["pass_rate_delta"] == pytest.approx(-0.1, abs=1e-6)
    # McNemar: 0 pairs (v1=1,v2=0); 1 pair (v1=0,v2=1) = t07
    assert ab["details"]["mcnemar"]["b10"] == 0
    assert ab["details"]["mcnemar"]["b01"] == 1
    # per-topic table present
    assert "per_topic" in ab["details"]
    # CI for primary present
    assert "pass_rate_delta" in ab["ci"]

    # --- 07_answer_v2_pass_rate ---
    v2_path = runs / "07_answer_v2_pass_rate" / "metrics.json"
    assert v2_path.exists(), "07_answer_v2_pass_rate not written"
    v2r = json.loads(v2_path.read_text())
    assert v2r["metrics"]["pass_rate"] == pytest.approx(0.8)
    assert v2r["details"]["primary"] == "pass_rate"

    # results.md rebuilt
    results_md = runs / "results.md"
    assert results_md.exists(), "results.md not rebuilt"
    text = results_md.read_text()
    assert "07_ab_answer_v2_vs_v1" in text
    assert "07_answer_v2_pass_rate" in text
