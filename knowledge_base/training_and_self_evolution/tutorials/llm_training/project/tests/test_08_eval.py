"""Chapter 08 — evaluation harness. CPU only, no network, no subprocess: everything under test
here is a pure string/JSON/statistics transform; `run_hf`/`run_ollama`/`evaluate_hf`/
`evaluate_ollama`/`judge` themselves need the GPU, the network, or a running Ollama server and
are exercised on `rtx`, not here."""

import json
from pathlib import Path

import pytest

from llm_tutorial.config import RunMetrics
from llm_tutorial.eval_domain import ci95, dedup_train, format_mcq, parse_letter
from llm_tutorial.eval_general import parse_results_json, summarize
from llm_tutorial.judge import build_judge_messages, parse_verdict

FIXTURES = Path(__file__).parent / "fixtures"


# --------------------------------------------------------------------------------- parse_letter


@pytest.mark.parametrize(
    "text,expected",
    [
        ("B", "B"),
        ("A.", "A"),
        ("Answer: B", "B"),
        ("(C)", "C"),
        ("The answer is D", "D"),
        ("answer: (A)", "A"),
        ("I think it's C.", "C"),
        ("no idea", None),
    ],
)
def test_parse_letter(text, expected):
    assert parse_letter(text) == expected


# --------------------------------------------------------------------------------- format_mcq


def test_format_mcq_contains_all_options():
    item = {
        "question": "Which protocol operates at layer 3?",
        "answers": {"A": "HTTP", "B": "IP", "C": "TCP", "D": "SMTP"},
        "solution": "B",
    }
    prompt = format_mcq(item)
    assert "A) HTTP" in prompt
    assert "B) IP" in prompt
    assert "C) TCP" in prompt
    assert "D) SMTP" in prompt
    assert item["question"] in prompt
    assert "letter only" in prompt.lower()


# --------------------------------------------------------------------------------- dedup_train


def test_dedup_train_removes_exact_and_variant_duplicates():
    eval_items = [{"question": "What is AES?"}, {"question": "Define least privilege."}]
    train_items = [
        {"question": "What is AES?"},  # exact duplicate
        {"question": "  what IS aes?  "},  # whitespace/case variant
        {"question": "Define Least Privilege."},  # case variant
        {"question": "What is a firewall?"},  # unique
    ]
    result = dedup_train(train_items, eval_items)
    assert result == [{"question": "What is a firewall?"}]


def test_dedup_train_no_overlap_keeps_everything():
    eval_items = [{"question": "unrelated question"}]
    train_items = [{"question": "a"}, {"question": "b"}]
    assert dedup_train(train_items, eval_items) == train_items


# --------------------------------------------------------------------------------- ci95


def test_ci95_all_correct_is_a_point_near_one():
    lo, hi = ci95([True] * 100, n_boot=500)
    assert 0.9 <= lo <= hi <= 1.0


def test_ci95_all_wrong_is_a_point_near_zero():
    lo, hi = ci95([False] * 100, n_boot=500)
    assert 0.0 <= lo <= hi <= 0.1


def test_ci95_half_correct_brackets_half():
    correct = [True] * 50 + [False] * 50
    lo, hi = ci95(correct, n_boot=1000)
    assert lo < 0.5 < hi


def test_ci95_empty_list():
    assert ci95([]) == (0.0, 0.0)


# --------------------------------------------------------------------------------- RunMetrics


def test_run_metrics_minimal():
    m = RunMetrics(run_name="tiny-qwen35-110m-base", model="tiny-qwen35-110m", stage="base")
    assert m.general == {}
    assert m.domain is None


def test_run_metrics_full_round_trip():
    payload = {
        "run_name": "qwen35-4b-baseline",
        "model": "Qwen/Qwen3.5-4B",
        "base": "Qwen/Qwen3.5-4B",
        "stage": "baseline",
        "general": {"mmlu": {"metric": "acc", "value": 0.55, "stderr": 0.03}},
        "general_mean": 0.55,
        "domain": {
            "dataset": "CyberMetric", "split": "2000", "n": 2000,
            "accuracy": 0.62, "ci95": [0.60, 0.64], "per_category": {},
        },
        "judge": {"n": 20, "mean_score": 3.8},
        "cost": {"wall_seconds": 1800.0, "peak_gb": 9.5},
    }
    m = RunMetrics.model_validate(payload)
    assert m.domain.accuracy == 0.62
    assert m.judge.mean_score == 3.8
    assert m.general["mmlu"].value == 0.55


def test_run_metrics_rejects_bad_stage_type():
    with pytest.raises(Exception):
        RunMetrics(run_name="x", model="x", stage=123)


# --------------------------------------------------------------------------------- lm_eval results parsing


def test_parse_results_json_picks_primary_metric_and_stderr():
    results = json.loads((FIXTURES / "eval_general_results.json").read_text())
    parsed = parse_results_json(results, tasks=["mmlu", "arc_challenge", "gsm8k"])
    assert parsed["mmlu"] == {"metric": "acc", "value": 0.24, "stderr": 0.031}
    assert parsed["arc_challenge"]["metric"] == "acc_norm"
    assert parsed["arc_challenge"]["value"] == pytest.approx(0.312)
    assert parsed["gsm8k"]["value"] == pytest.approx(0.055)


def test_summarize_computes_general_mean():
    results = json.loads((FIXTURES / "eval_general_results.json").read_text())
    summary = summarize(results, tasks=["mmlu", "arc_challenge", "gsm8k"])
    expected_mean = (0.24 + 0.312 + 0.055) / 3
    assert summary["general_mean"] == pytest.approx(expected_mean)
    assert set(summary["general"].keys()) == {"mmlu", "arc_challenge", "gsm8k"}


# --------------------------------------------------------------------------------- judge


def test_build_judge_messages_includes_question_reference_candidate():
    messages = build_judge_messages("What is AES?", "A symmetric block cipher.", "It's a hash function.")
    assert messages[0]["role"] == "system"
    user = messages[1]["content"]
    assert "What is AES?" in user
    assert "A symmetric block cipher." in user
    assert "It's a hash function." in user


def test_parse_verdict_canned_response():
    canned = json.dumps({"score": 4, "verdict": "correct", "reason": "Matches the reference closely."})
    verdict = parse_verdict(canned)
    assert verdict.score == 4
    assert verdict.verdict == "correct"


def test_parse_verdict_rejects_out_of_range_score():
    canned = json.dumps({"score": 9, "verdict": "correct", "reason": "bad score"})
    with pytest.raises(Exception):
        parse_verdict(canned)
