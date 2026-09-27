"""Chapter 04 offline tests — code-graded evals and the shared results plumbing.

All tests are hermetic: `settings.path` is redirected to `tmp_path` so nothing
touches the real project tree, the `FakeLLM`/`FakeEmbedder` stand in for the
Ollama client, no network, and matplotlib renders to `Agg` (no window).

Run with: cd project && uv run pytest tests/ -q -m "not slow"
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

import evals_tutorial.config as cfg
from evals_tutorial import code_evals as CE
from evals_tutorial import results as R
from evals_tutorial.testing import FakeLLM


@pytest.fixture()
def root(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    """Redirect every `settings.path(...)` to tmp_path so nothing touches the real tree."""
    monkeypatch.setattr(cfg.Settings, "path", lambda self, rel: tmp_path / rel)
    # keep the chapter-03 usage counter clean so run_* LLM-call accounting is
    # the fake client's own contribution only.
    monkeypatch.setitem(CE._llm.usage_log, "hits", 0)
    monkeypatch.setitem(CE._llm.usage_log, "misses", 0)
    return tmp_path


# -- 1. results.write_metrics + build round-trip -------------------------------


def test_results_roundtrip_and_table_header(root: Path):
    # two experiments: one with a CI on its primary, one without
    R.write_metrics(
        experiment="zz_with_ci",
        chapter=9,
        n=10,
        metrics={"primary_a": 0.5, "aux": 0.4},
        ci={"primary_a": [0.40, 0.60]},
        llm_calls=12,
        seconds=3.0,
        details={"primary": "primary_a", "notes": "has a CI"},
        predictions=[{"ticket_id": "t1", "pass": True}],
        config={"client": "FakeLLM"},
        project_root=root,
    )
    R.write_metrics(
        experiment="zz_no_ci",
        chapter=9,
        n=5,
        metrics={"only_metric": 0.9},
        ci={},
        llm_calls=0,
        seconds=0.0,
        details={"notes": "no CI at all"},
        predictions=[],
        config={},
        project_root=root,
    )
    out = R.build(root)
    text = out.read_text()

    # exact column header from index.md
    assert "experiment | chapter | n | primary metric | 95 % CI | LLM calls | s/item | notes" in text
    # CI rendered as [lo, hi]
    assert "[0.4, 0.6]" in text
    # the CI-less experiment shows the em-dash sentinel
    zz_no = [line for line in text.splitlines() if line.startswith("zz_no_ci")][0]
    assert "—" in zz_no
    # both experiments present, count reflected in the generated header
    assert "2 experiment(s)" in text
    # per-item second: 3.0s / 10 = 0.3 for the CI experiment
    zz_with = [line for line in text.splitlines() if line.startswith("zz_with_ci")][0]
    assert "0.3" in zz_with

    # the contract files landed exactly where index.md says
    m = json.loads((root / "runs" / "zz_with_ci" / "metrics.json").read_text())
    assert m["experiment"] == "zz_with_ci"
    assert m["n"] == 10
    assert m["details"]["primary"] == "primary_a"
    assert (root / "runs" / "zz_with_ci" / "predictions.jsonl").read_text().count("t1") == 1
    assert (root / "runs" / "zz_with_ci" / "config.json").exists()


# -- 2. triage metrics on a 6-row synthetic set (known confusion matrix) --------


def _gold(cat: str) -> dict:
    return {"category": cat, "priority": "normal", "needs_escalation": False}


def test_triage_metrics_known_confusion(root: Path, monkeypatch: pytest.MonkeyPatch):
    # gold/pred categories (rows=gold, cols=pred):
    #   A A   -> both pred A
    #   B     -> pred B
    #   B     -> pred C   (B->C confusion)
    #   C C   -> both pred C
    cases = [
        ("t1", "A", "A"),
        ("t2", "A", "A"),
        ("t3", "B", "B"),
        ("t4", "B", "C"),
        ("t5", "C", "C"),
        ("t6", "C", "C"),
    ]

    def load_labels(run):
        return [
            {"ticket_id": tid, "pass": g == p, "failure_modes": [], "note": "",
             "raw": {"gold": _gold(g)}}
            for tid, g, p in cases
        ]

    def load_tickets():
        return [
            {"id": tid, "split": "test", "scenario": "s", "persona": "p", "gold": _gold(g)}
            for tid, g, _ in cases
        ]  # includes the `id` key run_similarity / run_triage index by

    def load_traces(run):
        return [
            {"ticket_id": tid, "output": dict(_gold(p), reason="r")}
            for tid, _, p in cases
        ]

    monkeypatch.setattr(CE, "load_labels", load_labels)
    monkeypatch.setattr(CE, "load_tickets", load_tickets)
    monkeypatch.setattr(CE, "load_traces", load_traces)

    path = CE.run_triage("triage_v1", split="test", project_root=root)
    m = json.loads(path.read_text())
    assert m["n"] == 6

    metrics = m["metrics"]
    pytest.approx
    # category accuracy: 5 of 6
    assert metrics["category_accuracy"] == pytest.approx(5 / 6)
    # macro F1 over {A,B,C}: A=1.0, B=2/3, C=0.8  -> mean 0.8222
    assert metrics["f1_macro"] == pytest.approx((1 + 2 / 3 + 0.8) / 3)
    # micro F1: tp=5, fp=1, fn=1 -> P=R=5/6
    assert metrics["f1_micro"] == pytest.approx(5 / 6)
    # every priority/escalation is correct
    assert metrics["priority_accuracy"] == 1.0
    assert metrics["needs_escalation_accuracy"] == 1.0
    # full-tuple accuracy == category accuracy here (rest are all right)
    assert metrics["category_priority_escalation_accuracy"] == pytest.approx(5 / 6)
    assert metrics["json_valid_rate"] == 1.0, "every trace output parsed into the schema"
    # per-category supports recorded for the three synthetic classes
    per = m["details"]["per_category"]
    assert per["B"]["support"] == 2 and per["C"]["support"] == 2
    assert per["A"]["f1"] == pytest.approx(1.0)
    assert per["C"]["precision"] == pytest.approx(2 / 3)  # one B predicted as C
    # the confusion PNG was written with Agg (no window) and is non-empty
    assert (root / "runs" / "04_triage_v1" / "confusion.png").stat().st_size > 0


# -- 3. the six deterministic checks on hand-made pass/fail replies --------------


def test_each_check_on_handmade_replies(root: Path, monkeypatch: pytest.MonkeyPatch):
    # write the forbidden-phrases YAML into the redirected data dir
    (root / "data" / "checks").mkdir(parents=True, exist_ok=True)
    (root / "data" / "checks" / "forbidden_phrases.yaml").write_text(
        yaml.safe_dump({"phrases": ["guarantee", "full refund immediately"]}),
        encoding="utf-8",
    )

    ticket = {
        "id": "t1",
        "scenario": "s",
        "gold": {
            "sections": ["returns"],
            "answer_points": ["Refund within five business days"],
        },
    }  # noqa: E501
    good = "About returns: your refund within five business days."
    bad = "We guarantee a full refund immediately — call us at 044 555 1234."

    # nonempty / words: good is short & non-empty, a 151-word reply is the fail
    assert CE.CHECKS["nonempty"](ticket, {"output": good}) is True
    assert CE.CHECKS["nonempty"](ticket, {"output": ""}) is False
    assert CE.CHECKS["max_words_150"](ticket, {"output": good}) is True
    assert CE.CHECKS["max_words_150"](ticket, {"output": "word " * 151}) is False

    # section name: good mentions "returns" (section title), bad does not
    assert CE.CHECKS["mentions_section_name"](ticket, {"output": good}) is True
    assert CE.CHECKS["mentions_section_name"](ticket, {"output": "call 044 555 1234"}) is False

    # phone/email: good is clean, bad invents a phone number
    assert CE.CHECKS["no_phone_or_email_invented"](ticket, {"output": good}) is True
    assert CE.CHECKS["no_phone_or_email_invented"](ticket, {"output": bad}) is False

    # forbidden promises: good is clean, bad contains "guarantee"
    assert CE.CHECKS["no_forbidden_promises"](ticket, {"output": good}) is True
    assert CE.CHECKS["no_forbidden_promises"](ticket, {"output": bad}) is False

    # answer-point keywords (refund / business): good has them, bad has neither
    assert CE.CHECKS["mentions_all_answer_point_keywords"](ticket, {"output": good}) is True
    assert CE.CHECKS["mentions_all_answer_point_keywords"](ticket, {"output": "call 044 555 1234"}) is False


# -- 4. ROUGE-L on short strings with hand-computed values ----------------------


def test_rouge_l_handcomputed():
    # ref: the cat sat on the mat  (6 tokens, "the" twice)
    # hyp: the cat sat on mat       (5 tokens)
    # LCS = the cat sat on mat (5) -> P=1.0, R=5/6, F=2pr/(p+r)=20/22
    r = CE.rouge_l("the cat sat on the mat", "the cat sat on mat")
    assert r["precision"] == pytest.approx(1.0)
    assert r["recall"] == pytest.approx(5 / 6)
    assert r["f"] == pytest.approx(20 / 22)

    # identical -> everything 1.0
    r = CE.rouge_l("a b c d", "a b c d")
    assert r == {"precision": 1.0, "recall": 1.0, "f": 1.0}

    # partial overlap: ref [the quick brown fox] hyp [the fox] -> LCS=2
    # P=2/2=1.0, R=2/4=0.5, F=2*(1*0.5)/(1.5)=0.6667
    r = CE.rouge_l("the quick brown fox", "the fox")
    assert r["precision"] == pytest.approx(1.0)
    assert r["recall"] == pytest.approx(0.5)
    assert r["f"] == pytest.approx(2 / 3)

    # disjoint -> all 0.0
    r = CE.rouge_l("alpha beta", "gamma delta")
    assert r == {"precision": 0.0, "recall": 0.0, "f": 0.0}


# -- 5. similarity with FakeEmbedder -------------------------------------------


def test_similarity_fake_embedder(root: Path, monkeypatch: pytest.MonkeyPatch):
    # 4 tickets, 2 pass / 2 fail. Pass replies overlap the gold answer point,
    # fail replies do not, so both ROUGE-L and embedding cosine separate labels.
    gold_point = "Refund within five business days"
    tickets = [
        {"id": tid, "split": "test", "scenario": "s", "persona": "p",
         "gold": {"answer_points": [gold_point]}}
        for tid in ("t1", "t2", "t3", "t4")
    ]
    replies = {
        "t1": "your refund within five business days",
        "t2": "refund within five business days",
        "t3": "please contact support for details",
        "t4": "call the office for assistance",
    }
    passes = {"t1": True, "t2": True, "t3": False, "t4": False}

    monkeypatch.setattr(CE, "load_tickets", lambda: tickets)
    monkeypatch.setattr(CE, "load_labels", lambda run: [
        {"ticket_id": tid, "pass": passes[tid], "failure_modes": [], "note": "", "raw": {}}
        for tid in passes
    ])
    monkeypatch.setattr(CE, "load_traces", lambda run: [
        {"ticket_id": tid, "output": replies[tid]} for tid in replies
    ])

    client = FakeLLM()  # embed_documents via FakeEmbedder, no network
    path = CE.run_similarity("answer_v1", split="test", client=client, project_root=root)
    m = json.loads(path.read_text())

    assert m["n"] == 4
    mm = m["metrics"]
    # both similarity scores should perfectly separate pass from fail -> AUC 1.0
    assert mm["auroc_embed_vs_label"] == pytest.approx(1.0)
    assert mm["auroc_rouge_vs_label"] == pytest.approx(1.0)
    # pass replies have higher cosine than fail replies
    preds = {r["ticket_id"]: r for r in (json.loads(l) for l in (path.parent / "predictions.jsonl").read_text().splitlines())}
    assert preds["t1"]["embed_cosine"] > preds["t3"]["embed_cosine"]
    assert preds["t1"]["rouge_f"] > preds["t3"]["rouge_f"]
    # fake client made no real LLM calls
    assert CE._llm.usage_log["hits"] + CE._llm.usage_log["misses"] == 0
    assert m["llm_calls"] == 0
