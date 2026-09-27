"""Chapter 09a — offline tests for the CPU hallucination detectors.

Fast tests cover the pure helpers (threshold pick, metrics, sentence
splitting, word chunking, span-level P/R) and the RAGTruth file contract.
Model-loading paths are tagged `@pytest.mark.slow` and skipped by the
default `pytest -m "not slow"` run (they need the HF download + GPU-free
CPU inference).

Run with: cd project && uv run pytest tests/ -q -m "not slow"
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from evals_tutorial import halluc as H


# ---------------------------------------------------------------------------
# helper tests (no model)
# ---------------------------------------------------------------------------


def test_pick_threshold_picks_max_f1():
    # Negatives are all below 0.5, positives all >= 0.8. The first
    # (lowest) threshold that captures every positive with zero false
    # positives is 0.8 (F1 = 1.0). Anything above 0.8 also gives F1 = 1.0
    # but misses some positives (e.g. 1.0 drops the 0.8 and 0.9 rows),
    # and anything <= 0.3 grabs a false positive.
    scores = [0.1, 0.2, 0.3, 0.8, 0.9, 1.0]
    labels = [False, False, False, True, True, True]
    thr = H.pick_threshold(scores, labels)
    assert thr == 0.8
    # verify the threshold is one of the unique score values (so callers
    # can reproduce the decision rule exactly)
    assert thr in set(scores)


def test_pick_threshold_degenerate_all_positive():
    # when every label is positive, any threshold above min score is fine;
    # assert the threshold is one of the unique scores so callers can
    # reconstruct the decision rule.
    s = [0.2, 0.7, 0.9]
    l = [True, True, True]
    thr = H.pick_threshold(s, l)
    assert thr in {0.2, 0.7, 0.9}


def test_precision_recall_f1_basic():
    p, r, f1 = H.precision_recall_f1(tp=10, fp=5, fn=5)
    assert p == pytest.approx(10 / 15)
    assert r == pytest.approx(10 / 15)
    assert f1 == pytest.approx(2 * p * r / (p + r))


def test_precision_recall_f1_handles_zero_denom():
    assert H.precision_recall_f1(0, 0, 0) == (0.0, 0.0, 0.0)
    assert H.precision_recall_f1(0, 5, 0) == (0.0, 0.0, 0.0)
    assert H.precision_recall_f1(0, 0, 5) == (0.0, 0.0, 0.0)


def test_auroc_perfect_separation():
    assert H.auroc([0.1, 0.9], [False, True]) == pytest.approx(1.0)
    assert H.auroc([0.9, 0.1], [True, False]) == pytest.approx(1.0)
    assert H.auroc([0.1, 0.9], [True, False]) == pytest.approx(0.0)


def test_auroc_with_ties():
    assert H.auroc([0.5, 0.5], [False, True]) == pytest.approx(0.5)


def test_split_sentences_basic():
    sents = H.split_sentences("The model is fast. It runs on CPU! Really? Yes.")
    assert len(sents) == 4
    assert sents[0] == "The model is fast."
    assert sents[1].endswith("CPU!")


def test_split_sentences_empty():
    assert H.split_sentences("") == []
    assert H.split_sentences("   ") == []


def test_split_sentences_single():
    assert H.split_sentences("One sentence only.") == ["One sentence only."]


def test_chunk_words():
    text = " ".join(f"w{i}" for i in range(700))
    chunks = H.chunk_words(text, k=300)
    assert len(chunks) == 3
    assert chunks[0].count(" ") == 299
    assert chunks[-1].count(" ") == 99
    joined = " ".join(chunks)
    assert len(joined.split()) == 700


def test_chunk_words_empty():
    assert H.chunk_words("") == [""]
    assert H.chunk_words(None) == [""]  # type: ignore[arg-type]


def test_span_token_pr_full_match():
    answer = "The cat sat on the mat."
    gold = [{"start": 0, "end": 4, "text": "The", "label_type": "hallucinated"}]
    pred = [{"start": 0, "end": 4, "text": "The", "confidence": 0.9}]
    out = H.span_token_pr(pred, gold, answer)
    assert out["precision"] == pytest.approx(1.0)
    assert out["recall"] == pytest.approx(1.0)
    assert out["f1"] == pytest.approx(1.0)


def test_span_token_pr_partial_overlap():
    answer = "The quick brown fox"
    gold = [{"start": 4, "end": 9, "text": "quick", "label_type": "hallucinated"}]
    # prediction overlaps half the gold span
    pred = [{"start": 6, "end": 14, "text": "brown ", "confidence": 0.8}]
    out = H.span_token_pr(pred, gold, answer)
    inter = 3  # chars [6,7,8]
    assert out["precision"] == pytest.approx(inter / 8)
    assert out["recall"] == pytest.approx(inter / 5)


def test_span_token_pr_ignores_non_hallucinated_gold():
    answer = "abc"
    gold = [{"start": 0, "end": 1, "text": "a", "label_type": "factuality"}]
    pred = [{"start": 0, "end": 1, "text": "a", "confidence": 0.9}]
    out = H.span_token_pr(pred, gold, answer)
    assert out["recall"] == 0.0  # no hallucinated gold to count
    assert out["precision"] in (0.0, 1.0, pytest.approx(0.0))


def test_ragtruth_contract():
    path = H.ragtruth_path()
    assert path.exists(), f"expected {path}"
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    assert len(rows) == 480, f"expected 480 rows, got {len(rows)}"
    required = {
        "id", "source_id", "task_type", "source", "prompt", "source_info",
        "model", "response", "labels", "quality", "hallucinated",
    }
    for r in rows:
        missing = required - r.keys()
        assert not missing, f"row {r.get('id')} missing {missing}"
        assert isinstance(r["hallucinated"], bool)
        assert isinstance(r["labels"], list)
    assert sum(1 for r in rows if r["hallucinated"]) > 0
    assert sum(1 for r in rows if not r["hallucinated"]) > 0


def test_evidence_for_summary_and_qa():
    # Summary: source_info is a raw text string
    row_s = {
        "task_type": "Summary",
        "prompt": "Summarize the following news within 200 words:\n<text>",
        "source_info": "RAW NEWS DOCUMENT TEXT",
    }
    assert H.evidence_for(row_s) == "RAW NEWS DOCUMENT TEXT"

    # QA: source_info is a dict with passages
    row_q = {
        "task_type": "QA",
        "prompt": "Given the following passages, answer: ?\nQ: ...",
        "source_info": {"question": "q?", "passages": "PASSAGE TEXT"},
    }
    assert H.evidence_for(row_q) == "PASSAGE TEXT"

    # Fall back to prompt if neither special-cases
    row_x = {"task_type": "Other", "prompt": "FALLBACK"}
    assert H.evidence_for(row_x) == "FALLBACK"


def test_question_for_qa_only():
    assert H.question_for({"source_info": {"question": "q?"}}) == "q?"
    assert H.question_for({"source_info": {"text": "not-a-dict"}}) is None
    assert H.question_for({}) is None


def test_dev_test_split():
    rows = [{"i": i} for i in range(480)]
    dev, test = H.dev_test_split(rows, dev_n=80)
    assert len(dev) == 80 and len(test) == 400
    assert [r["i"] for r in dev] == list(range(80))
    assert [r["i"] for r in test] == list(range(80, 480))


def test_dev_test_split_requires_more_rows():
    with pytest.raises(ValueError):
        H.dev_test_split([{"i": 0} for _ in range(10)], dev_n=80)


def test_label_index():
    # HF configs use integer keys; some carry string keys — both work.
    id2label = {0: "contradiction", 1: "neutral", 2: "entailment"}
    assert H._label_index(id2label, "entailment") == 2
    assert H._label_index(id2label, "ENTAILMENT") == 2
    assert H._label_index(id2label, "neutral") == 1
    id2label_str = {"0": "contradiction", "1": "neutral", "2": "entailment"}
    assert H._label_index(id2label_str, "entailment") == 2
    # missing name -> 0
    assert H._label_index(id2label, "nope") == 0


def test_parse_selfcheck_score():
    # mean consistency 0.8 -> score 0.2
    assert H.selfcheck_score([0.9, 0.8, 0.7]) == pytest.approx(0.2)


def test_parse_selfcheck_score_clamps():
    assert H.selfcheck_score([0.0, 0.0]) == pytest.approx(1.0)
    assert H.selfcheck_score([1.0, 1.0]) == pytest.approx(0.0)


def test_pairwise_agreement():
    assert H.pairwise_agreement([True, True, False, False], [True, False, True, False]) == pytest.approx(0.5)
    assert H.pairwise_agreement([True, True], [True, False]) == pytest.approx(0.5)
    assert H.pairwise_agreement([], []) == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# slow tests — real model load + predict on 1 row each
# ---------------------------------------------------------------------------


@pytest.mark.slow
def test_hhem_load_and_predict():
    model, tok = H.load_hhem()
    out = model(**tok("premise: cat\nhypothesis: dog", return_tensors="pt", max_length=32))
    assert out.logits.shape[-1] == 2


@pytest.mark.slow
def test_lettuce_load_and_predict():
    d = H.load_lettuce()
    spans = d.predict_prompt(
        "What is the capital of France? Paris is the capital.",
        "The capital is London.",
        output_format="spans",
    )
    assert isinstance(spans, list)


@pytest.mark.slow
def test_nli_load_and_predict():
    m, t = H.load_nli()
    o = t(["The cat is black."], ["Cats are black."], return_tensors="pt")
    logits = m(**o).logits
    assert logits.shape[-1] == 3
