"""Chapter 13 evaluation tests — all offline (no Ollama, no network).

Covers the pure helpers: Spearman correlation, Pareto frontier, the
scoreboard-analysis renderer on synthetic runs, the human-audit sampler,
agreement stats, and the prompt-injection file builder (in a tmp dir).
"""

from __future__ import annotations

import json

from rag_tutorial import judge_audit, scoreboard
from rag_tutorial.injection_demo import (
    INJECTION_FILENAME,
    INJECTION_INSTRUCTION,
    build_injection_file,
    remove_injection_file,
)


def _row(name, correctness, s_q=1.0, calls=1.0, chapter="13", recall=0.5):
    return {
        "experiment": name,
        "chapter": chapter,
        "correctness": correctness,
        "seconds_per_q": s_q,
        "llm_calls_per_q": calls,
        "recall@5": recall,
    }


def test_spearman_perfect_and_inverse():
    assert judge_audit.spearman([1, 2, 3, 4], [10, 20, 30, 40]) == 1.0
    assert judge_audit.spearman([1, 2, 3, 4], [40, 30, 20, 10]) == -1.0


def test_spearman_undefined_cases():
    assert judge_audit.spearman([1.0], [2.0]) is None  # single point
    assert judge_audit.spearman([1, 1, 1], [1, 2, 3]) is None  # constant x
    assert judge_audit.spearman([1, 2, 3], [5, 5, 5]) is None  # constant y


def test_spearman_ignores_none_pairs():
    assert judge_audit.spearman([1, 2, None, 4], [1, 2, 99, 4]) == 1.0


def test_pareto_frontier_synthetic():
    rows = [
        _row("fast_bad", 0.3, s_q=1.0),
        _row("slow_good", 0.7, s_q=10.0),
        _row("dominated", 0.5, s_q=10.0),  # worse quality, same cost as slow_good
        _row("mid", 0.5, s_q=2.0),
    ]
    front = scoreboard.pareto_frontier(rows)
    names = [r["experiment"] for r in front]
    assert "dominated" not in names
    assert set(names) == {"fast_bad", "slow_good", "mid"}


def test_render_analysis_from_two_synthetic_runs():
    rows = [_row("03_naive_fixed_512_k5", 0.435), _row("07_best_combo", 0.587, s_q=4.95)]
    md = scoreboard.render_analysis(rows)
    assert md.startswith("# Scoreboard analysis")
    assert "07_best_combo" in md and "03_naive_fixed_512_k5" in md
    assert "Pareto frontier" in md and "What helped most" in md
    assert "+0.152" in md  # best-combo delta vs naive baseline


def test_family_of_mapping():
    assert scoreboard.family_of("04_parent_child") == "chunking"
    assert scoreboard.family_of("07_hybrid_k20_ce_bge_k5") == "rerank"
    assert scoreboard.family_of("11_lightrag_hybrid") == "graph-lightrag"


def test_sample_audit_items_round_robin():
    preds = {
        "run_a": [{"id": f"a{i}", "question": "q", "answer": "a", "correctness": {"score": 1.0, "reason": "r"}} for i in range(10)],
        "run_b": [{"id": f"b{i}", "question": "q", "answer": "a", "correctness": {"score": 0.0, "reason": "r"}} for i in range(10)],
    }
    items = judge_audit.sample_audit_items(preds, n=6, seed=13)
    assert len(items) == 6
    assert {i["run"] for i in items} == {"run_a", "run_b"}
    assert all(i["human_score"] is None and i["note"] == "" for i in items)


def test_agreement_stats():
    out = judge_audit.agreement([1.0, 0.5, 0.0], [1.0, 0.0, 0.0])
    assert out["n"] == 3
    assert out["match_rate"] == 2 / 3
    assert out["mae"] == (0.0 + 0.5 + 0.0) / 3


def test_injection_file_builder_roundtrip(tmp_path):
    path = build_injection_file(tmp_path)
    assert path.name == INJECTION_FILENAME
    text = path.read_text()
    assert INJECTION_INSTRUCTION in text
    assert remove_injection_file(tmp_path) is True
    assert remove_injection_file(tmp_path) is False


def test_audit_items_serialise_to_jsonl():
    preds = {
        "run_a": [{"id": "q1", "type": "single_hop", "question": "q?", "answer": "a", "correctness": {"score": 0.5, "reason": "ok"}}],
    }
    items = judge_audit.sample_audit_items(preds, n=1)
    line = json.dumps(items[0], ensure_ascii=False)
    assert json.loads(line)["judge_correctness"] == 0.5
