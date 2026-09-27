"""Chapter 05 offline tests — LLM-as-judge module (binary per-mode judges).

Hermetic: `settings.path` is redirected to `tmp_path`, a synthetic 10-ticket
split with synthetic labels and traces stands in for the real data, and
`FakeLLM` returns canned `{critique, verdict}` JSONs. No network, no LLM.

Run with: cd project && uv run pytest tests/ -q -m "not slow"
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import evals_tutorial.config as cfg
from evals_tutorial import judge as J
from evals_tutorial.testing import FakeLLM

# 10 synthetic dev tickets: 4 truly fail the mode, 6 pass.
# Canned predictions: 3 of the 4 fails caught (TP=3, FN=1),
# 1 of the 6 passes falsely flagged (FP=1, TN=5).
FAIL_TICKETS = ["tkt-a01", "tkt-a02", "tkt-a03", "tkt-a04"]  # true_fail
PASS_TICKETS = ["tkt-b01", "tkt-b02", "tkt-b03", "tkt-b04", "tkt-b05", "tkt-b06"]
PRED_FAIL = ["tkt-a01", "tkt-a02", "tkt-a03", "tkt-b02"]  # judge says fail

MODE = "missing_required_fact"


def _input_for(tid: str) -> str:
    return f"ticket for {tid}"  # unique substring the FakeLLM keys on


@pytest.fixture()
def root(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    """Redirect `settings.path(...)` to tmp_path and build the synthetic dataset."""
    monkeypatch.setattr(cfg.Settings, "path", lambda self, rel: tmp_path / rel)

    all_tids = FAIL_TICKETS + PASS_TICKETS
    tickets = [
        {"id": tid, "split": "dev", "persona": "p", "topic": "t", "scenario": "s", "text": _input_for(tid)}
        for tid in all_tids
    ]
    (tmp_path / "data" / "tickets").mkdir(parents=True)
    with (tmp_path / "data" / "tickets" / "tickets.jsonl").open("w") as f:
        for t in tickets:
            f.write(json.dumps(t) + "\n")

    labels = [
        {
            "ticket_id": tid,
            "pass": tid not in FAIL_TICKETS,
            "failure_modes": [MODE] if tid in FAIL_TICKETS else [],
            "note": "synthetic",
        }
        for tid in all_tids
    ]
    (tmp_path / "data" / "labels").mkdir(parents=True)
    with (tmp_path / "data" / "labels" / "answer_v1.jsonl").open("w") as f:
        for r in labels:
            f.write(json.dumps(r) + "\n")

    (tmp_path / "runs" / "traces" / "answer_v1").mkdir(parents=True)
    for tid in all_tids:
        trace = {
            "run": "answer_v1",
            "version": "v1",
            "ticket_id": tid,
            "input": _input_for(tid),
            "retrieved": [{"section": "returns", "score": 0.9}],
            "prompt": "p",
            "output": "a reply",
            "latency_s": 1.0,
            "model": "qwen3.8:27b",
            "usage": {},
        }
        (tmp_path / "runs" / "traces" / "answer_v1" / f"{tid}.json").write_text(json.dumps(trace))

    # stub prompt files for every tracked mode, v1 and v2, with placeholders
    monkeypatch.setattr(J, "PROMPTS_DIR", tmp_path / "prompts")
    pdir = tmp_path / "prompts"
    pdir.mkdir()
    for m in (MODE, "unsupported_claim", "wrong_section_retrieved", "did_not_answer"):
        for v in ("v1", "v2"):
            text = f"{v} judge for {m}\n" + "--- TICKET ---\n{ticket}\n--- CONTEXT ---\n{context}\n--- REPLY ---\n{reply}\n"
            if v == "v2":
                text = "# examples: tkt-043(fail) tkt-051(fail) tkt-002(pass) tkt-037(pass)\n" + text
            (pdir / f"judge_{m}_{v}.txt").write_text(text)
    return tmp_path


@pytest.fixture()
def fake() -> FakeLLM:
    answers = {
        _input_for(tid): {"critique": f"canned for {tid}", "verdict": "fail" if tid in PRED_FAIL else "pass"}
        for tid in FAIL_TICKETS + PASS_TICKETS
    }
    return FakeLLM(json_answers=answers)


# -- 1. predictions + alignment metrics on the 10-row synthetic set ------------


def test_grade_split_predictions_and_metrics(root: Path, fake: FakeLLM):
    res = J.grade_split(MODE, "v1", "dev", fake)
    assert res["n"] == 10
    preds = {r["ticket_id"]: r["pred_fail"] for r in res["rows"]}
    assert preds == {tid: (tid in PRED_FAIL) for tid in FAIL_TICKETS + PASS_TICKETS}
    truths = {r["ticket_id"]: r["true_fail"] for r in res["rows"]}
    assert truths == {tid: (tid in FAIL_TICKETS) for tid in FAIL_TICKETS + PASS_TICKETS}

    # hand-computed: TP=3, FN=1, FP=1, TN=5
    assert res["confusion"] == {"tp": 3, "fp": 1, "tn": 5, "fn": 1}
    assert res["tpr"] == pytest.approx(3 / 4)
    assert res["tnr"] == pytest.approx(5 / 6)
    assert res["accuracy"] == pytest.approx(0.8)
    # obs=0.8, exp=0.4*0.4+0.6*0.6=0.52 -> kappa = 0.28/0.48
    assert res["kappa"] == pytest.approx(0.28 / 0.48)


# -- 2. metrics functions on known inputs ---------------------------------------


def test_cohen_kappa_known_inputs():
    assert J.cohen_kappa([True, True, False, False], [True, True, False, False]) == pytest.approx(1.0)
    assert J.cohen_kappa([True, False], [False, True]) == pytest.approx(-1.0)
    # obs 0.5 vs chance 0.5 -> kappa 0
    assert J.cohen_kappa([True, False], [True, True]) == pytest.approx(0.0)
    assert J.cohen_kappa([], []) == 0.0


def test_auroc_known_inputs():
    assert J.auroc([4, 3, 2, 1], [1, 1, 0, 0]) == pytest.approx(1.0)
    assert J.auroc([1, 2, 3, 4], [1, 1, 0, 0]) == pytest.approx(0.0)
    # ties count half
    assert J.auroc([2, 2, 1], [1, 0, 1]) == pytest.approx(0.25)
    assert J.auroc([1, 2], [1, 0]) == pytest.approx(0.0)
    assert J.auroc([1, 1], [1, 0]) == pytest.approx(0.5)
    # degenerate (only one class present) -> neutral 0.5
    assert J.auroc([3, 3], [1, 1]) == pytest.approx(0.5)


# -- 3. prompt files load and carry their placeholders ---------------------------


def test_tracked_modes_match_taxonomy_counts(root: Path):
    assert J.tracked_modes() == [MODE]  # only the synthetic label set has >= 4 fails


def test_prompts_load_with_placeholders(root: Path):
    for mode in J.tracked_modes():
        for version in ("v1", "v2"):
            text = (J.PROMPTS_DIR / f"judge_{mode}_{version}.txt").read_text()
            assert "{ticket}" in text
            assert "{context}" in text
            assert "{reply}" in text


# -- 4. v2 few-shot ids are dev tickets (against the REAL committed data) --------


def test_v2_example_ids_are_dev_tickets():
    real_root = cfg.PROJECT_ROOT
    ids_by_split = {}
    for line in (real_root / "data" / "tickets" / "tickets.jsonl").read_text().splitlines():
        if line.strip():
            row = json.loads(line)
            ids_by_split[row["id"]] = row["split"]
    modes = [MODE, "unsupported_claim", "wrong_section_retrieved", "did_not_answer"]
    pdir = real_root / "src" / "evals_tutorial" / "prompts"
    for mode in modes:
        first = (pdir / f"judge_{mode}_v2.txt").read_text().splitlines()[0]
        assert first.startswith("# examples:"), mode
        for token in first.split()[2:]:
            tid = token.split("(")[0]
            assert tid in ids_by_split, f"{mode}: unknown ticket {tid}"
            assert ids_by_split[tid] == "dev", f"{mode}: {tid} is not a dev ticket"


# -- 5. align picks the higher-kappa version on dev ------------------------------


def test_align_mode_picks_best_on_dev(root: Path, monkeypatch: pytest.MonkeyPatch):
    def fake_grade(mode, version, split, client, *, nocontext=False):
        return {
            "n": 1,
            "rows": [],
            "confusion": {"tp": 0, "fp": 0, "tn": 1, "fn": 0},
            "tpr": 0.0,
            "tnr": 1.0,
            "accuracy": 1.0,
            "kappa": 0.9 if version == "v1" else 0.3,
        }

    monkeypatch.setattr(J, "grade_split", fake_grade)
    res = J.align_mode(MODE, FakeLLM())
    assert res["best"] == "v1"
    assert res["best_kappa"] == pytest.approx(0.9)
    assert res["versions"]["v2"]["kappa"] == pytest.approx(0.3)
