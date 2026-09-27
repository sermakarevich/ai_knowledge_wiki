"""Chapter 12 offline tests — the Inspect-AI rebuild of chapters 05 & 11.

Hermetic: no Ollama, no network. The dataset builders read the committed
tickets / harness dump (disk, not network); the scorers are exercised against
a fake `TaskState` with `_mode_scores` / `code_evals.CHECKS` / RAG monkeypatched;
`_collect_helpdesk` runs on a tiny hand-written log-shaped dict with all disk
reads and `write_metrics` monkeypatched. The one test marked `slow` performs
the real log read of `runs/12_inspect/logs`.

Run with: cd project && uv run pytest tests/ -q -m "not slow"
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

import pytest

pytest.importorskip("inspect_ai")
from inspect_ai.scorer import CORRECT, INCORRECT  # noqa: E402

from evals_tutorial import code_evals, inspect_run as R, inspect_tasks as T  # noqa: E402

TICKET_ID = "tkt-001"
REPLY = "Your return window is 30 days."


class _FakeState:
    """Duck-type of the bits the scorer reads off a TaskState — no real TaskState needed."""

    def __init__(self) -> None:
        self.input = TICKET_ID
        self.sample_id = TICKET_ID
        self.metadata = {"ticket_id": TICKET_ID, "gold": {}}
        self.output = type("O", (), {"completion": REPLY, "error": None})()


def _state() -> _FakeState:
    return _FakeState()


async def _call_score(score_fn, state: TaskState) -> object:
    return await score_fn(state, None)


# ---------------------------------------------------------------------------
# dataset builders
# ---------------------------------------------------------------------------


def test_helpdesk_dataset_shape():
    ds = T._helpdesk_dataset(split="test")
    assert len(ds.samples) == 60
    assert ds.name == "helpdesk-test"
    for s in ds.samples[:5]:
        assert s.id and isinstance(s.input, str) and s.input
        assert isinstance(s.target, list)
        assert set(s.metadata) >= {"ticket_id", "scenario", "persona", "gold"}
        assert s.metadata["ticket_id"] == s.id


def test_gsm8k_dataset_shape(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    # Point the harness-dump reader at a tiny synthetic jsonl.
    dump = tmp_path / "runs" / "11_lmeval" / "gsm8k" / "qwen3.8__27b"
    dump.mkdir(parents=True)
    rows = [
        {"doc_id": i, "doc": {"question": f"Q{i}?", "answer": f"CoT... #### {i * 3}"}}
        for i in range(3)
    ]
    (dump / "samples.jsonl").write_text("\n".join(json.dumps(r) for r in rows))
    monkeypatch.setattr(T, "_SAMPLES_DIR", dump)
    monkeypatch.setattr(T, "_SAMPLES_FALLBACK", tmp_path / "runs" / "11_lmeval" / "gsm8k")

    ds = T._gsm8k_dataset(limit=3)
    assert len(ds.samples) == 3
    by_id = {s.id: s for s in ds.samples}
    # gold number = the number after the last `####` in the synthetic answers
    assert by_id["2"].target == "6"
    for s in ds.samples:
        assert "doc_id" in s.metadata
        assert s.metadata["gold"] in {"0", "3", "6"}


# ---------------------------------------------------------------------------
# scorers (fake TaskState, monkeypatched LLM/RAG)
# ---------------------------------------------------------------------------


def test_judge_grade_all_modes_pass_is_correct(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        T, "_mode_scores", lambda ticket, reply: {"m_a": {"version": "v2", "verdict": "pass", "critique": "ok"}}
    )
    score_coro = T._judge_grade(version="v1")  # the `@scorer` factory returns the async score fn
    score = asyncio.run(_call_score(score_coro, _state()))
    assert score.value == CORRECT
    assert score.metadata["failed"] == []
    assert score.answer == REPLY


def test_judge_grade_any_mode_fail_is_incorrect(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        T,
        "_mode_scores",
        lambda ticket, reply: {
            "m_a": {"version": "v2", "verdict": "pass", "critique": "ok"},
            "m_b": {"version": "v1", "verdict": "fail", "critique": "missing fact"},
        },
    )
    score_coro = T._judge_grade(version="v1")
    score = asyncio.run(_call_score(score_coro, _state()))
    assert score.value == INCORRECT
    assert score.metadata["failed"] == ["m_b"]
    assert "m_b" in score.explanation and "fail" in score.explanation


def test_code_checks_scores_pass_rate(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(T.helpdesk, "retrieved_context", lambda text: ([], [{"section": "returns"}]))
    monkeypatch.setitem(code_evals.CHECKS, "no_forbidden_promises", lambda ticket, tr: True)
    monkeypatch.setitem(code_evals.CHECKS, "nonempty", lambda ticket, tr: False)
    n_checks = len(code_evals.CHECKS)

    score_coro = T._code_checks()
    score = asyncio.run(_call_score(score_coro, _state()))
    assert score.metadata["total"] == n_checks
    assert score.metadata["passed"] == sum(1 for v in score.metadata["results"].values() if v)
    assert score.value == pytest.approx(score.metadata["passed"] / n_checks)
    assert score.metadata["results"]["nonempty"] is False
    assert score.metadata["results"]["no_forbidden_promises"] is True


# ---------------------------------------------------------------------------
# collect: the log→metrics pipeline, fully monkeypatched
# ---------------------------------------------------------------------------


class _TinyLog:
    """Minimal stand-in for `inspect_ai.log.EvalLog` (`.samples` + `.eval.packages`)."""

    def __init__(self, samples: list) -> None:
        self.samples = samples
        self.eval = type("E", (), {"packages": {"inspect_ai": "0.3.999"}})()


def _tiny_helpdesk_log(n: int = 6) -> _TinyLog:
    class S:
        def __init__(self, i, judge_pass, code_val, inc_hit):
            self.id = f"t{str(i).zfill(3)}"
            self.metadata = {"gold": {}}
            self.scores = {
                "judge_grade": type("JG", (), {"value": 1 if judge_pass else 0, "answer": "reply",
                                               "metadata": {"failed": [] if judge_pass else ["m"]}})(),
                "code_checks": type("CC", (), {"value": code_val})(),
                "includes": type("IN", (), {"value": "C" if inc_hit else "I"})(),
            }

    half = n // 2
    samples = [
        S(i, judge_pass=(i < half), code_val=1.0 if i % 2 == 0 else 0.0, inc_hit=(i % 3 == 0)) for i in range(n)
    ]
    return _TinyLog(samples)


def _tiny_gsm8k_log(n: int = 4) -> _TinyLog:
    class S:
        def __init__(self, i, ok):
            self.id = str(i)
            self.metadata = {"gold": str(i * 2), "doc_id": i}
            self.scores = {"match": type("M", (), {"value": "C" if ok else "I", "answer": f"{i * 2}"})()}

    return _TinyLog([S(i, ok=(i < n - 1)) for i in range(n)])


def test_collect_helpdesk_schema(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    written = {}

    def fake_write(**kw):
        written.update(kw)

    monkeypatch.setattr(R, "_read_old05", lambda: ({}, {"metrics": {}}))
    monkeypatch.setattr(R, "load_labels", lambda run: [
        {"ticket_id": f"t{str(i).zfill(3)}", "pass": True} for i in range(6)
    ])
    monkeypatch.setattr(R, "bootstrap_ci", lambda vals: [0.0, 1.0])
    monkeypatch.setattr(R, "write_metrics", fake_write)
    class _JudgeStub:
        def cohen_kappa(self, y_true, y_pred):
            return 1.0

        @staticmethod
        def tracked_modes():
            return ["m"]

        @staticmethod
        def chosen_version(mode):
            return "v1"

    monkeypatch.setattr(R, "judge", _JudgeStub())

    out = R._collect_helpdesk(_tiny_helpdesk_log(6))

    assert set(written) >= {"experiment", "chapter", "n", "metrics", "ci", "details", "predictions", "config"}
    assert written["experiment"] == R.HEXPERIMENT_HELPDESK
    assert written["n"] == 6

    metrics = written["metrics"]
    for key in ("pass_rate", "accuracy", "kappa", "code_checks_mean", "includes_hit_rate"):
        assert key in metrics
    ci = written["ci"]
    for key in ("pass_rate", "accuracy", "kappa", "code_checks_mean", "includes_hit_rate"):
        assert key in ci and len(ci[key]) == 2

    # 6 samples, first 3 judge-pass → pass_rate == 0.5; true_pass all True → accuracy == 0.5
    assert metrics["pass_rate"] == pytest.approx(0.5)
    assert metrics["accuracy"] == pytest.approx(0.5)
    assert written["details"]["primary"] == "pass_rate"
    assert out["rows"] and len(out["rows"]) == 6


def test_collect_gsm8k_schema(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    written = {}

    def fake_write(**kw):
        written.update(kw)

    monkeypatch.setattr(R, "_read_old11", lambda: ({}, {"metrics": {}}))
    monkeypatch.setattr(R, "bootstrap_ci", lambda vals: [0.0, 1.0])
    monkeypatch.setattr(R, "write_metrics", fake_write)

    R._collect_gsm8k(_tiny_gsm8k_log(4))

    assert set(written) >= {"experiment", "chapter", "n", "metrics", "ci", "details", "predictions", "config"}
    metrics = written["metrics"]
    for key in ("accuracy", "agreement_with_ch11"):
        assert key in metrics
    # 4 samples, first 3 ok → accuracy == 0.75
    assert metrics["accuracy"] == pytest.approx(0.75)
    assert written["details"]["primary"] == "accuracy"


@pytest.mark.slow
def test_collect_reads_real_log():
    """Performs the full log read of `runs/12_inspect/logs` — skipped in the fast suite."""
    log = R._eval_log("helpdesk_answer")
    assert log is not None
