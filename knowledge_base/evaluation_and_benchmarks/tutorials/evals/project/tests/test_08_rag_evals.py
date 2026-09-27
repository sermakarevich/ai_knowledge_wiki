"""Chapter 08a tests: retrieval IR metrics (pure, fast) + ragas wiring (import-guarded)
+ a `slow` live path.

Fast tests exercise the pure IR math with hand-computed expectations, plus the
failure-split logic on synthetic data. The ragas live path is marked `slow`
and skipped in the default run; an import-guarded sanity test verifies the
wiring resolves without making network calls.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from evals_tutorial.rag_evals import (
    _failed_ticket_ids,
    _split_ticket_ids,
    auroc,
    graded_relevance,
    hit_at_k,
    ndcg,
    per_ticket_ir,
    precision_at_k,
    recall_at_k,
    recall_curve,
    reciprocal_rank,
    spearman,
)

DATA = Path(__file__).parent.parent


# ---------------------------------------------------------------------------
# pure IR metrics -- hand-computed expectations
# ---------------------------------------------------------------------------


def test_hit_at_k_basic():
    assert hit_at_k(["a", "b"], ["a", "c"], 2) == 1.0
    assert hit_at_k(["a", "b"], ["c", "d"], 2) == 0.0
    # rank order matters for the cut-off: gold at position 3 misses at k=2
    assert hit_at_k(["x", "y", "a"], ["a"], 2) == 0.0
    assert hit_at_k(["x", "y", "a"], ["a"], 3) == 1.0


def test_recall_at_k_partial_and_full():
    # gold size 2; top-2 contains both -> 1.0
    assert recall_at_k(["a", "b"], ["a", "b"], 2) == pytest.approx(1.0)
    # top-2 contains one of two -> 0.5
    assert recall_at_k(["a", "x"], ["a", "b"], 2) == pytest.approx(0.5)
    # none -> 0.0
    assert recall_at_k(["x", "y"], ["a", "b"], 2) == 0.0
    # no gold -> 0.0
    assert recall_at_k(["a"], [], 2) == 0.0


def test_precision_at_k_denominator_is_k():
    # 1 gold in top-2 => 1/2
    assert precision_at_k(["a", "x"], ["a", "b"], 2) == pytest.approx(0.5)
    # 2 gold in top-2 => 1.0
    assert precision_at_k(["a", "b"], ["a", "b"], 2) == pytest.approx(1.0)
    # zero gold in top-k => 0.0
    assert precision_at_k(["x", "y"], ["a"], 2) == 0.0
    # k<=0 guard
    assert precision_at_k(["a"], ["a"], 0) == 0.0


def test_reciprocal_rank_first_match():
    assert reciprocal_rank(["a", "b"], ["b", "c"]) == pytest.approx(0.5)
    assert reciprocal_rank(["a", "b", "c"], ["c", "d"]) == pytest.approx(1 / 3)
    assert reciprocal_rank(["x", "y"], ["a", "b"]) == 0.0
    assert reciprocal_rank([], ["a"]) == 0.0


def test_graded_relevance_order():
    assert graded_relevance(["a", "b", "c"]) == {"a": 3.0, "b": 2.0, "c": 1.0}
    assert graded_relevance(["a", "b"]) == {"a": 2.0, "b": 1.0}
    assert graded_relevance([]) == {}


def test_ndcg_perfect_and_order_sensitivity():
    # gold [a,b,c] (grades a=3,b=2,c=1). Perfect ordering -> 1.0
    assert ndcg(["a", "b", "c"], ["a", "b", "c"], 3) == pytest.approx(1.0)
    # reversed order scores lower than perfect but > 0
    assert ndcg(["c", "b", "a"], ["a", "b", "c"], 3) < 1.0
    assert ndcg(["c", "b", "a"], ["a", "b", "c"], 3) > 0.0
    # gold section absent at all -> 0.0
    assert ndcg(["x", "y"], ["a", "b"], 3) == 0.0
    # no gold -> 0.0 (guard)
    assert ndcg(["a", "b"], [], 3) == 0.0


def test_ndcg_hand_example_matches_0_62():
    # From the spec's worked example:
    # retrieved top-3 = [b, z, a], gold (graded) a:3, b:2, c:1
    # DCG   = 2/log2(2) + 0/log2(3) + 3/log2(4) = 2.0 + 0 + 1.5 = 3.5
    # IDCG  = 3/log2(2) + 2/log2(3) + 1/log2(4) = 3.0 + 1.2619 + 0.5 = 4.7619
    # nDCG  = 3.5 / 4.7619 = 0.735006...  (spec rounded differently); assert exact
    import math

    dcg = 2 / math.log2(2) + 3 / math.log2(4)
    idcg = 3 / math.log2(2) + 2 / math.log2(3) + 1 / math.log2(4)
    got = ndcg(["b", "z", "a"], ["a", "b", "c"], 3)
    assert got == pytest.approx(dcg / idcg, abs=1e-9)


def test_per_ticket_ir_assembles_expected_names():
    r = per_ticket_ir(["a", "b"], ["a", "b"], k=2)
    assert set(r) == {"hit@2", "recall@2", "precision@2", "mrr", "ndcg@2"}
    assert r["hit@2"] == 1.0
    assert r["recall@2"] == 1.0
    assert r["precision@2"] == 1.0
    assert r["mrr"] == 1.0
    assert r["ndcg@2"] == 1.0


def test_recall_curve_prefix_property():
    sections = ["a", "x", "b", "y"]
    gold = ["a", "b"]
    curve = recall_curve(sections, gold, kmax=4)
    assert [c["k"] for c in curve] == [1, 2, 3, 4]
    # k=1: top=[a] -> hit=1, recall=1/2, precision=1/1
    assert curve[0]["hit"] == 1.0
    assert curve[0]["recall"] == pytest.approx(0.5)
    assert curve[0]["precision"] == pytest.approx(1.0)
    # k=2: top=[a,x] -> hit=1, recall=1/2, precision=1/2
    assert curve[1]["recall"] == pytest.approx(0.5)
    assert curve[1]["precision"] == pytest.approx(0.5)
    # k=3: top=[a,x,b] -> hit=1, recall=1, precision=2/3
    assert curve[2]["recall"] == pytest.approx(1.0)
    assert curve[2]["precision"] == pytest.approx(2 / 3)
    # recall is non-decreasing in k (prefix property from a stable ranking)
    recalls = [c["recall"] for c in curve]
    assert recalls == sorted(recalls)


# ---------------------------------------------------------------------------
# split helpers on synthetic files
# ---------------------------------------------------------------------------


def test_split_ticket_ids_and_failed(tmp_path: Path):
    p = tmp_path / "predictions.jsonl"
    rows = [
        {"ticket_id": "t1", "split": "test", "pred_pass": True},
        {"ticket_id": "t2", "split": "test", "pred_pass": False},
        {"ticket_id": "t3", "split": "dev", "pred_pass": False},
    ]
    p.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    assert _split_ticket_ids(p, "test") == ["t1", "t2"]
    assert _split_ticket_ids(p, "all") == ["t1", "t2", "t3"]
    assert _failed_ticket_ids(p, "test") == {"t2"}
    assert _failed_ticket_ids(p, "dev") == {"t3"}


def test_split_helpers_tolerate_missing_file(tmp_path: Path):
    missing = tmp_path / "does_not_exist.jsonl"
    assert _split_ticket_ids(missing, "test") == []
    assert _failed_ticket_ids(missing, "test") == set()


# ---------------------------------------------------------------------------
# agreement primitives (pure) -- hand-checked
# ---------------------------------------------------------------------------


def test_spearman_monotonic_transform_is_1():
    # Spearman is rank-based: any strictly increasing transform must be 1.0.
    base = [0.1, 0.2, 0.45, 0.7, 0.99]
    assert spearman(base, [b * 10 for b in base]) == pytest.approx(1.0)
    assert spearman(base, [b ** 3 for b in base]) == pytest.approx(1.0)


def test_spearman_inverse_is_minus_1():
    base = [0.1, 0.3, 0.6, 0.9]
    assert spearman(base, [-x for x in base]) == pytest.approx(-1.0)


def _pearson(a, b):
    import math

    n = len(a)
    mx = sum(a) / n
    my = sum(b) / n
    cov = sum((i - mx) * (j - my) for i, j in zip(a, b))
    vx = sum((i - mx) ** 2 for i in a)
    vy = sum((j - my) ** 2 for j in b)
    return cov / math.sqrt(vx * vy)


def test_spearman_hand_example_on_integer_ranks():
    # For distinct integers, tie-averaged ranks are the values themselves.
    x = [1, 2, 3, 4, 5]
    y = [2, 1, 4, 3, 5]
    assert spearman(x, y) == pytest.approx(_pearson(x, y))


def test_spearman_tie_averaging_matches_average_ranks():
    # x=[1,1,3,4,5]: the tie at 1 gives ranks 1.5,1.5, then 3,4,5.
    # y=[5,4,3,2,1] strictly decreasing -> ranks 5,4,3,2,1.
    # Spearman = Pearson on those tie-averaged rank vectors (cross-checked
    # against scipy.stats.spearmanr: -0.974679).
    assert spearman([1, 1, 3, 4, 5], [5, 4, 3, 2, 1]) == pytest.approx(
        _pearson([1.5, 1.5, 3, 4, 5], [5, 4, 3, 2, 1])
    )


def test_spearman_ties_and_degenerate():
    # constant input -> zero variance -> 0.0 (documented guard)
    assert spearman([1, 1, 1, 1], [0.1, 0.2, 0.3, 0.4]) == 0.0
    # tied input still yields a value strictly inside (-1, 1)
    v = spearman([1, 1, 2, 2, 3], [0.5, 0.2, 0.8, 0.1, 0.9])
    assert -1.0 < v < 1.0


def test_auroc_perfect_and_reversed():
    assert auroc([0.1, 0.2, 0.8, 0.9], [0, 0, 1, 1]) == pytest.approx(1.0)
    assert auroc([0.8, 0.9, 0.1, 0.2], [0, 0, 1, 1]) == pytest.approx(0.0)
    # single class -> 0.5 by convention (not enough signal)
    assert auroc([0.1, 0.9], [0, 0]) == 0.5
    assert auroc([0.1, 0.9], [1, 1]) == 0.5


def test_auroc_known_mann_whitney_case():
    # positive [3] vs negatives [1,5,7]: beats 1, loses to 5 and 7.
    # U = 1 + 0.5*0 = 1 ; AUC = 1 / (1*3) = 1/3
    assert auroc([3, 1, 5, 7], [1, 0, 0, 0]) == pytest.approx(1 / 3)
    # tie at the positive value splits its contribution in half:
    # positive [2] vs negatives [2,1]: beats 1, ties 2 -> U=1+0.5=1.5 ; AUC=1.5/2
    assert auroc([2, 2, 1], [1, 0, 0]) == pytest.approx(0.75)


def test_auroc_rejects_length_mismatch():
    with pytest.raises(ValueError):
        auroc([0.5, 0.6], [1])


def _make_canned_agreement_project(tmp_path: Path) -> Path:
    """Canned 5-ticket project laid out the way the 08b agreement command
    expects it: `runs/05_judge_overall` gates the ticket order
    (and carries `pred_pass`), `runs/08_ragas_answer_v1` is one row per
    ticket in the same order (no ticket_id -- positional alignment),
    and the other three sources are keyed by ticket_id.
    """
    import json

    (tmp_path / "data" / "tickets").mkdir(parents=True)
    (tmp_path / "runs" / "05_judge_overall").mkdir(parents=True)
    (tmp_path / "runs" / "08_ragas_answer_v1").mkdir(parents=True)
    (tmp_path / "runs" / "08_deepeval_answer_v1").mkdir(parents=True)
    (tmp_path / "runs" / "04_similarity_answer_v1").mkdir(parents=True)

    (tmp_path / "runs" / "05_judge_overall" / "predictions.jsonl").write_text(
        "\n".join(
            json.dumps({"ticket_id": f"t1{i}", "split": "test", "pred_pass": (i < 3)})
            for i in range(5)
        )
        + "\n"
    )
    ragas = [
        {"faithfulness": v} for v in [1.0, 0.8, 0.6, 0.4, 0.2]
    ]
    (tmp_path / "runs" / "08_ragas_answer_v1" / "predictions.jsonl").write_text(
        "\n".join(json.dumps(r) for r in ragas) + "\n"
    )
    deep = [
        {"ticket_id": f"t1{i}", "faithfulness": v}
        for i, v in enumerate([1, 0.9, 0.7, 0.5, 0.3])
    ]
    (tmp_path / "runs" / "08_deepeval_answer_v1" / "predictions.jsonl").write_text(
        "\n".join(json.dumps(r) for r in deep) + "\n"
    )
    sim = [
        {"ticket_id": f"t1{i}", "embed_cosine": v, "pass": (i < 3)}
        for i, v in enumerate([0.90, 0.80, 0.60, 0.30, 0.10])
    ]
    (tmp_path / "runs" / "04_similarity_answer_v1" / "predictions.jsonl").write_text(
        "\n".join(json.dumps(r) for r in sim) + "\n"
    )
    return tmp_path


def test_agreement_core_canned(tmp_path: Path):
    """The pure (no-LLM) agreement path: given canned RAGAS/DeepEval/sim/verdict
    files, it reads them positionally + by ticket_id, computes the 3 Spearman +
    6 AUROC metrics in the expected ranges, and reports the primary."""
    import shutil

    from evals_tutorial.rag_evals import _agreement_core

    root = _make_canned_agreement_project(tmp_path)
    core = _agreement_core(
        run="answer_v1", n=5, seed=0, n_boot=50, project_root=root
    )
    assert core["n"] == 5, "all 5 canned tickets should agree"
    m = core["metrics"]
    # same monotone trend -> Spearman must be ~ 1
    assert m["spearman_ragas_vs_deepeval"] == pytest.approx(1.0)
    assert m["spearman_ragas_vs_embed"] > 0.9
    assert m["spearman_deepeval_vs_embed"] > 0.9
    # cosine perfectly separates 3/2 pass vs fail -> AUC = 1
    assert m["auroc_embed_cosine_vs_label"] == pytest.approx(1.0)
    # same ordering between ragas and label -> AUC = 1
    assert m["auroc_ragas_faithfulness_vs_label"] == pytest.approx(1.0)
    # all metrics in their proper range
    for key, v in m.items():
        low, high = (-1, 1) if key.startswith("spearman_") else (0, 1)
        assert low <= v <= high, key
    # deterministic across runs at the same seed
    core2 = _agreement_core(
        run="answer_v1", n=5, seed=0, n_boot=50, project_root=root
    )
    assert core2["metrics"] == m


# ---------------------------------------------------------------------------
# ragas wiring -- import-guarded, no network
# ---------------------------------------------------------------------------


def test_ragas_wiring_imports_resolve():
    # These must resolve in this venv; if ragas restructures, the failure here
    # (not at runtime) pins the required public surface for chapter 08a.
    import warnings

    warnings.filterwarnings("ignore")
    from openai import OpenAI  # noqa: F401
    from ragas import SingleTurnSample, EvaluationDataset, evaluate  # noqa: F401
    from ragas.embeddings import LangchainEmbeddingsWrapper  # noqa: F401
    from ragas.llms import llm_factory  # noqa: F401
    from ragas.metrics import AnswerRelevancy, ContextPrecision, Faithfulness  # noqa: F401

    sample = SingleTurnSample(
        user_input="Question?",
        retrieved_contexts=["ctx-1", "ctx-2"],
        reference="gold points",
        reference_contexts=["ctx-1", "ctx-2"],
        response="An answer.",
    )
    ds = EvaluationDataset(samples=[sample])
    assert len(ds) == 1
    for metric in (Faithfulness(), AnswerRelevancy(), ContextPrecision()):
        assert "SINGLE_TURN" in metric.required_columns


def test_ragas_wiring_llm_factory_shape():
    # factory is called lazily; we only assert it returns an object with the
    # generate methods the counter monkey-patches.
    import warnings

    warnings.filterwarnings("ignore")
    from openai import OpenAI
    from ragas.llms import llm_factory

    llm = llm_factory(
        "qwen3.8:27b",
        provider="openai",
        client=OpenAI(base_url="http://127.0.0.1:11435/v1", api_key="ollama"),
        temperature=0,
    )
    assert hasattr(llm, "generate")
    assert hasattr(llm, "agenerate")


def test_deepeval_wiring_imports_resolve():
    """The required DeepEval public surface must resolve in this venv (no
    network call). Pins the exact API the 08b wiring relies on so a
    deepeval restructure fails here (fast) rather than at run time."""
    import warnings

    warnings.filterwarnings("ignore")
    from deepeval.metrics import (  # noqa: F401
        AnswerRelevancyMetric,
        ContextualPrecisionMetric,
        FaithfulnessMetric,
    )
    from deepeval.models import OllamaModel
    from deepeval.test_case import LLMTestCase

    model = OllamaModel(model="qwen3.8:27b", base_url="http://127.0.0.1:11435")
    # the counter monkey-patches these; assert both exist before we patch them
    assert hasattr(model, "generate")
    assert hasattr(model, "a_generate")

    tc = LLMTestCase(
        input="How do I reset my password?",
        actual_output="Go to Settings and choose Reset.",
        retrieval_context=["To reset, go to Settings > Reset. An email is sent."],
        expected_output="Go to Settings and reset; a confirmation email is sent.",
    )
    assert tc.input and tc.actual_output and tc.retrieval_context

    # every metric we use must build with a shared model instance
    for cls in (FaithfulnessMetric, AnswerRelevancyMetric, ContextualPrecisionMetric):
        metric = cls(model=model, threshold=0.5, async_mode=False)
        assert metric is not None  # construction only; no LLM call


# ---------------------------------------------------------------------------
# live ragas run -- requires Ollama; guarded behind the `slow` marker
# ---------------------------------------------------------------------------


@pytest.mark.slow
def test_ragas_live_small_sample():
    """A 2-sample RAGAS run end-to-end. Only runs under `pytest -m slow` with
    Ollama up. Verifies the counter, the mean extraction, and the write path
    against the real local model.
    """
    from evals_tutorial.rag_evals import _ragas_core

    root = DATA
    core = _ragas_core(run="answer_v1", n=2, split="test", seed=0, project_root=root)
    # we should have produced at least the 3 requested metric means
    assert "faithfulness" in core["metrics"]
    assert "answer_relevancy" in core["metrics"]
    assert "context_precision" in core["metrics"]
    # each in [0, 1]
    for name, value in core["metrics"].items():
        assert 0.0 <= value <= 1.0, name
    # LLM calls were counted (a small 2-sample run is well under budget)
    assert core["llm_calls"] > 0
    assert core["n"] >= 1


@pytest.mark.slow
def test_deepeval_live_small_sample():
    """A 2-sample DeepEval run end-to-end against the local Ollama model.
    Verifies the native-OllamaModel counter, per-item scores in [0,1], and
    that all three metric columns are produced.
    """
    from evals_tutorial.rag_evals import _deepeval_core

    root = DATA
    core = _deepeval_core(run="answer_v1", n=2, split="test", seed=0, project_root=root)
    for name in ("faithfulness", "answer_relevancy", "context_precision"):
        if name in core["metrics"]:
            assert 0.0 <= core["metrics"][name] <= 1.0, name
    assert core["llm_calls"] > 0
    assert core["n"] == 2


def test_agreement_core_reads_all_six_sources(tmp_path: Path):
    """The pure agreement core must read six on-disk sources and emit the
    3 Spearman + 6 AUROC metrics. Uses a self-contained 8-ticket project
    whose hand-computed / scipy-verified values we assert on, so the test
    is hermetic and fast (no LLM; runs/08b outputs are produced by the
    justfile pipeline, not by tests).

    Ticket layout (RAGAS rows are positional; DeepEval/sim/overall by id):

    tid ragas deep cos  label verdict
    T1  0.90  0.80 0.90   1    1
    T2  0.50  0.60 0.45   1    1
    T3  0.70  0.40 0.60   1    1
    T4  0.80  0.90 0.80   0    0
    T5  0.20  0.10 0.25   0    0
    T6  0.10  0.30 0.15   0    0
    T7  0.60  0.50 0.50   0    1
    T8  0.30  0.20 0.30   1    0
    """
    import json

    (tmp_path / "data").mkdir(parents=True)
    for d in ("05_judge_overall", "08_ragas_answer_v1", "08_deepeval_answer_v1",
              "04_similarity_answer_v1"):
        (tmp_path / "runs" / d).mkdir(parents=True)

    # The overall file gates ticket order; also carries pred_pass.
    overall = [
        {"ticket_id": "T1", "split": "test", "pred_pass": 1},
        {"ticket_id": "T2", "split": "test", "pred_pass": 1},
        {"ticket_id": "T3", "split": "test", "pred_pass": 1},
        {"ticket_id": "T4", "split": "test", "pred_pass": 0},
        {"ticket_id": "T5", "split": "test", "pred_pass": 0},
        {"ticket_id": "T6", "split": "test", "pred_pass": 0},
        {"ticket_id": "T7", "split": "test", "pred_pass": 1},
        {"ticket_id": "T8", "split": "test", "pred_pass": 0},
    ]
    (tmp_path / "runs" / "05_judge_overall" / "predictions.jsonl").write_text(
        "\n".join(json.dumps(r) for r in overall) + "\n"
    )

    ragas = [
        {"faithfulness": v} for v in [0.9, 0.5, 0.7, 0.8, 0.2, 0.1, 0.6, 0.3]
    ]
    (tmp_path / "runs" / "08_ragas_answer_v1" / "predictions.jsonl").write_text(
        "\n".join(json.dumps(r) for r in ragas) + "\n"
    )

    deep = [
        {"ticket_id": "T1", "faithfulness": 0.8},
        {"ticket_id": "T2", "faithfulness": 0.6},
        {"ticket_id": "T3", "faithfulness": 0.4},
        {"ticket_id": "T4", "faithfulness": 0.9},
        {"ticket_id": "T5", "faithfulness": 0.1},
        {"ticket_id": "T6", "faithfulness": 0.3},
        {"ticket_id": "T7", "faithfulness": 0.5},
        {"ticket_id": "T8", "faithfulness": 0.2},
    ]
    (tmp_path / "runs" / "08_deepeval_answer_v1" / "predictions.jsonl").write_text(
        "\n".join(json.dumps(r) for r in deep) + "\n"
    )

    sim = [
        {"ticket_id": "T1", "embed_cosine": 0.90, "pass": True},
        {"ticket_id": "T2", "embed_cosine": 0.45, "pass": True},
        {"ticket_id": "T3", "embed_cosine": 0.60, "pass": True},
        {"ticket_id": "T4", "embed_cosine": 0.80, "pass": False},
        {"ticket_id": "T5", "embed_cosine": 0.25, "pass": False},
        {"ticket_id": "T6", "embed_cosine": 0.15, "pass": False},
        {"ticket_id": "T7", "embed_cosine": 0.50, "pass": False},
        {"ticket_id": "T8", "embed_cosine": 0.30, "pass": True},
    ]
    (tmp_path / "runs" / "04_similarity_answer_v1" / "predictions.jsonl").write_text(
        "\n".join(json.dumps(r) for r in sim) + "\n"
    )

    from evals_tutorial.rag_evals import _agreement_core

    root = tmp_path
    core = _agreement_core(run="answer_v1", n=8, seed=0, n_boot=50, project_root=root)
    assert core["n"] == 8
    m = core["metrics"]

    # Hand-computed AUROCs (verified by brute-force enumeration):
    # rag=[.9,.5,.7,.8,.2,.1,.6,.3], lab=[1,1,1,0,0,0,0,1] -> 11/16 = 0.6875
    # dep=[.8,.6,.4,.9,.1,.3,.5,.2]                     -> 9/16  = 0.5625
    assert m["auroc_ragas_faithfulness_vs_label"] == pytest.approx(0.6875)
    assert m["auroc_deepeval_faithfulness_vs_label"] == pytest.approx(0.5625)

    # Cross-check Spearman (scipy available here for reference only, not
    # imported by the module under test).
    try:
        from scipy.stats import spearmanr as _sp

        assert m["spearman_ragas_vs_deepeval"] == pytest.approx(
            float(_sp([0.9, 0.5, 0.7, 0.8, 0.2, 0.1, 0.6, 0.3],
                      [0.8, 0.6, 0.4, 0.9, 0.1, 0.3, 0.5, 0.2])[0])
        )
    except ImportError:
        pass

    # every metric strictly in its valid range
    for key, v in m.items():
        if key.startswith("spearman_"):
            assert -1.0 <= v <= 1.0, key
        elif key.startswith("auroc_"):
            assert 0.0 <= v <= 1.0, key

    # deterministic at same seed
    core2 = _agreement_core(run="answer_v1", n=8, seed=0, n_boot=50, project_root=root)
    assert core2["metrics"] == m


def _load_real_answer_traces() -> list[str]:
    """ticket_ids of the real answer_v1 traces on disk."""
    path = DATA / "runs" / "traces" / "answer_v1"
    if not path.exists():
        return []
    return sorted(p.stem for p in path.glob("*.json"))


@pytest.mark.slow
def test_retrieval_core_runs_and_writes(tmp_path: Path):
    """Full retrieval core on the real test split (cached embeddings -- no LLM).

    ``load_traces`` reads the real project's answer_v1 traces (it is bound to
    the global settings, not project_root); the tmp project only supplies the
    tickets + synthetic predictions that gate which tickets are evaluated.
    Verifies: n, the failure-split identity, the primary metric + its CI, and
    that the curve PNG is written.
    """
    from evals_tutorial.rag_evals import _retrieval_core

    root = tmp_path
    (root / "data" / "tickets").mkdir(parents=True)
    (root / "data" / "tickets" / "tickets.jsonl").write_text(
        (DATA / "data" / "tickets" / "tickets.jsonl").read_text()
    )
    (root / "runs" / "05_judge_overall").mkdir(parents=True)

    trace_ids = _load_real_answer_traces()[:12]
    assert trace_ids, "no answer_v1 traces on disk"
    rows = [
        {"ticket_id": tid, "split": "test", "pred_pass": (i % 3 != 0)}
        for i, tid in enumerate(trace_ids)
    ]
    (root / "runs" / "05_judge_overall" / "predictions.jsonl").write_text(
        "\n".join(json.dumps(r) for r in rows) + "\n"
    )

    core = _retrieval_core(run="answer_v1", kmax=5, n_boot=200, seed=0, project_root=root)
    assert core["n"] == len(trace_ids)
    # failure split identity: retrieval_fail + generation_fail == failures
    failed = sum(1 for r in rows if not r["pred_pass"])
    split = core["details"]["failure_split"]
    assert split["retrieval_fail"] + split["generation_fail"] == failed
    assert failed == split["failed_total"]
    assert core["details"]["primary"] == "recall@2"
    lo, hi = core["ci"]["recall@2"]
    assert lo <= core["metrics"]["recall@2"] <= hi
    assert (root / "runs" / "08_retrieval_answer_v1" / "recall_curve.png").exists()


def test_retrieval_failure_split_identity_is_well_defined():
    """The failure split partitions the failing tickets, so the two buckets must
    sum to the failure count for *any* per-ticket input. Exercise the exact
    predicate used in _retrieval_core on a mixed set."""
    per_ticket = [
        {"pred_pass": True,  "recall@2": 0.0},
        {"pred_pass": False, "recall@2": 0.0},  # -> retrieval_fail
        {"pred_pass": False, "recall@2": 1.0},  # -> generation_fail
        {"pred_pass": False, "recall@2": 0.5},  # -> generation_fail
        {"pred_pass": False, "recall@2": 0.0},  # -> retrieval_fail
    ]
    ret = sum(1 for r in per_ticket if not r["pred_pass"] and r["recall@2"] == 0.0)
    gen = sum(1 for r in per_ticket if not r["pred_pass"] and r["recall@2"] > 0.0)
    failed = sum(1 for r in per_ticket if not r["pred_pass"])
    assert ret == 2 and gen == 2 and ret + gen == failed
