"""Offline tests for chapter 02: chunk ids, section detection, retrieval metrics,

the LLM judges (with FakeLLM) and the scoreboard renderer. No network calls.
"""

from __future__ import annotations

import json
import math

from rag_tutorial.evaluate import (
    chunk_covers_quote,
    judge_abstain,
    judge_correctness,
    judge_faithfulness,
    retrieval_metrics,
)
from rag_tutorial.schema import Chunk, chunk_id, detect_sections
from rag_tutorial.scoreboard import render_scoreboard
from rag_tutorial.testing import FakeLLM

# -- schema ---------------------------------------------------------------------------


def test_chunk_id_is_deterministic():
    a = chunk_id("2005.11401", 100, 200)
    b = chunk_id("2005.11401", 100, 200)
    assert a == b
    assert len(a) == 16
    assert all(c in "0123456789abcdef" for c in a)


def test_chunk_id_differs_on_any_argument():
    base = chunk_id("paper_a", 0, 10)
    assert chunk_id("paper_b", 0, 10) != base
    assert chunk_id("paper_a", 1, 10) != base
    assert chunk_id("paper_a", 0, 11) != base


def test_detect_sections_heading_path():
    text = (
        "intro text before any heading\n"
        "# 1 Introduction\n"
        "intro body\n"
        "## 1.1 Motivation\n"
        "motivation body\n"
        "# 2 Method\n"
        "method body\n"
        "## 2.1 Retrieval\n"
        "retrieval body\n"
    )
    sections = detect_sections(text)
    paths = [s.path for s in sections]
    assert paths == [
        "",
        "1 Introduction",
        "1 Introduction > 1.1 Motivation",
        "2 Method",
        "2 Method > 2.1 Retrieval",
    ]

    # sections are ordered and non-overlapping (a small gap between sections is
    # the heading line itself, which belongs to no section's body text)
    assert sections[0].start == 0
    for prev, nxt in zip(sections, sections[1:]):
        assert prev.end <= nxt.start
    assert sections[-1].end == len(text)

    # "1.1 Motivation" is nested under "1 Introduction" but "2 Method" resets the stack
    assert sections[2].path == "1 Introduction > 1.1 Motivation"
    assert sections[3].path == "2 Method"


def test_detect_sections_no_headings_returns_one_section():
    text = "just a plain paragraph with no markdown headings at all"
    sections = detect_sections(text)
    assert len(sections) == 1
    assert sections[0].path == ""
    assert sections[0].start == 0
    assert sections[0].end == len(text)


# -- retrieval metrics ------------------------------------------------------------------


def _chunk(paper: str, text: str) -> Chunk:
    return Chunk(id=chunk_id(paper, 0, len(text)), paper=paper, section="", text=text, start=0, end=len(text))


def test_retrieval_metrics_hand_built_case():
    evidence = [{"paper": "p1", "quote": "the cat sat on the mat"}]
    retrieved = [
        _chunk("p1", "an unrelated sentence about something else entirely"),
        _chunk("p1", "the cat sat on the mat and then slept all afternoon"),
    ]

    result = retrieval_metrics(retrieved, evidence, ks=(5, 10))

    assert result["hit@5"] == 1.0
    assert result["recall@5"] == 1.0
    assert result["mrr"] == 0.5  # first relevant chunk is at rank 2

    dcg = 1.0 / math.log2(2 + 1)  # relevant chunk at rank 2 (1-indexed)
    idcg = 1.0 / math.log2(1 + 1)  # ideal: the one relevant chunk at rank 1
    assert result["ndcg@10"] == dcg / idcg


def test_retrieval_metrics_no_relevant_chunk_is_all_zero():
    evidence = [{"paper": "p1", "quote": "a very specific fact"}]
    retrieved = [_chunk("p1", "nothing to do with the evidence at all")]

    result = retrieval_metrics(retrieved, evidence)

    assert result["hit@5"] == 0.0
    assert result["recall@5"] == 0.0
    assert result["mrr"] == 0.0
    assert result["ndcg@10"] == 0.0


def test_retrieval_metrics_empty_evidence_is_zero_not_error():
    result = retrieval_metrics([_chunk("p1", "some text")], evidence=[])
    assert result["hit@5"] == 0.0
    assert result["mrr"] == 0.0


def test_chunk_covers_quote_requires_same_paper():
    evidence = {"paper": "p1", "quote": "the exact phrase"}
    chunk = _chunk("p2", "this chunk contains the exact phrase verbatim")
    assert not chunk_covers_quote(chunk, evidence)


def test_chunk_covers_quote_partial_token_overlap():
    evidence = {"paper": "p1", "quote": "alpha beta gamma delta epsilon"}
    # 4 of 5 tokens present (80%) — meets the 0.8 overlap threshold
    chunk = _chunk("p1", "alpha beta gamma delta zeta")
    assert chunk_covers_quote(chunk, evidence)


# -- judges (FakeLLM, no network) ---------------------------------------------------


def test_judge_correctness_uses_canned_score():
    fake = FakeLLM(canned={"Reference answer: Paris": json.dumps({"score": 1, "reason": "matches reference"})})
    result = judge_correctness("What is the capital of France?", "Paris", "The capital is Paris.", client=fake)
    assert result["score"] == 1.0
    assert result["reason"] == "matches reference"


def test_judge_faithfulness_computes_score_from_support_results():
    claims_json = json.dumps({"claims": ["The sky is blue.", "The grass is purple."]})
    support_json = json.dumps(
        {
            "results": [
                {"claim": "The sky is blue.", "supported": True},
                {"claim": "The grass is purple.", "supported": False},
            ]
        }
    )
    fake = FakeLLM(canned={"The sky is blue. The grass is purple.": claims_json, "Claims:": support_json})
    result = judge_faithfulness("The sky is blue. The grass is purple.", ["The sky is blue. Grass is green."], client=fake)
    assert result["total"] == 2
    assert result["supported"] == 1
    assert result["score"] == 0.5
    assert result["unsupported_claims"] == ["The grass is purple."]


def test_judge_faithfulness_no_contexts_still_returns_score_one_for_empty_claims():
    fake = FakeLLM(canned={"empty answer": json.dumps({"claims": []})})
    result = judge_faithfulness("empty answer", [], client=fake)
    assert result["total"] == 0
    assert result["score"] == 1.0


def test_judge_abstain_true_when_model_declines():
    fake = FakeLLM(canned={"Model's answer: I cannot answer this from the documents.": json.dumps({"abstain": True, "reason": "declined"})})
    result = judge_abstain("some unanswerable question", "I cannot answer this from the documents.", client=fake)
    assert result["abstain"] == 1.0


def test_judge_abstain_false_when_model_guesses():
    fake = FakeLLM(canned={"Model's answer: The answer is 42.": json.dumps({"abstain": False, "reason": "guessed"})})
    result = judge_abstain("some unanswerable question", "The answer is 42.", client=fake)
    assert result["abstain"] == 0.0


# -- scoreboard -------------------------------------------------------------------------


def test_scoreboard_renders_two_rows_with_anchor_bolded():
    rows = [
        {
            "experiment": "02_no_retrieval",
            "chapter": "02",
            "hit@5": 0.1,
            "recall@5": 0.1,
            "mrr": 0.2,
            "ndcg@10": 0.15,
            "correctness": 0.4,
            "faithfulness": 0.9,
            "unanswerable_abstain": 0.5,
            "llm_calls_per_q": 1,
            "seconds_per_q": 3.2,
        },
        {
            "experiment": "03_naive_fixed_512_k5",
            "chapter": "03",
            "hit@5": 0.6,
            "recall@5": 0.55,
            "mrr": 0.5,
            "ndcg@10": 0.52,
            "correctness": 0.7,
            "faithfulness": 0.8,
            "unanswerable_abstain": 0.6,
            "llm_calls_per_q": 1,
            "seconds_per_q": 4.1,
        },
    ]
    markdown = render_scoreboard(rows)

    assert "| experiment | chapter | hit@5 | recall@5 | MRR | nDCG@10 | correctness | faithfulness | unanswerable-abstain | LLM calls/q | s/q |" in markdown
    lines = markdown.strip().splitlines()
    assert len(lines) == 4  # header + separator + 2 rows
    # chapter 02 anchor sorts before chapter 03 and is bolded
    assert "**02_no_retrieval**" in lines[2]
    assert "**03_naive_fixed_512_k5**" in lines[3]


def test_scoreboard_handles_missing_values():
    rows = [{"experiment": "x", "chapter": "02"}]
    markdown = render_scoreboard(rows)
    assert "| x | 02 | - | - | - | - | - | - | - | - | - |" in markdown
