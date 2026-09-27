"""Chapter 06a offline tests — MT-Bench judge module (sample / judge / agreement / bias).

Hermetic: `settings.path` is redirected to `tmp_path`, the data dir is a
synthetic 30-row vote file plus tiny answer/gpt4 files, and verdicts are
canned. No network, no LLM.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import evals_tutorial.config as cfg
import evals_tutorial.mtbench as M
from evals_tutorial.testing import FakeLLM


def _vote(qid: int, ma: str, mb: str, winner: str, turn: int = 1, judge: str = "author") -> dict:
    return {"question_id": qid, "model_a": ma, "model_b": mb, "winner": winner, "judge": judge, "turn": turn}


def _answer(qid: int, model: str, a1: str, q: str = "Q") -> dict:
    return {"question_id": qid, "model": model, "questions": [q, "Q2"], "answers": [a1, "A2"]}


@pytest.fixture
def root(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    """Redirect settings + module data dir into tmp_path and plant synthetic data."""
    monkeypatch.setattr(cfg.Settings, "path", lambda self, rel: tmp_path / rel)
    data = tmp_path / "data" / "public"
    data.mkdir(parents=True)
    monkeypatch.setattr(M, "DATA_DIR", data)

    votes = [
        # q1: pair (x, y): 3 annotators model_a + 1 model_b (no ties)
        _vote(1, "m-x", "m-y", "model_a", judge="a1"),
        _vote(1, "m-x", "m-y", "model_a", judge="a2"),
        _vote(1, "m-x", "m-y", "model_a", judge="a3"),
        _vote(1, "m-x", "m-y", "model_b", judge="a4"),
        # q1: pair (x, y) voted a tie
        _vote(1, "m-x", "m-y", "tie", judge="a5"),
        # q2: pair (x, y): two votes disagree incl. tie
        _vote(2, "m-x", "m-y", "model_a", judge="a1"),
        _vote(2, "m-x", "m-y", "tie (bothbad)", judge="a2"),
        # q2: pair (y, x) (reversed order): two votes for model_a (= m-y)
        _vote(2, "m-y", "m-x", "model_a", judge="a1"),
        _vote(2, "m-y", "m-x", "model_a", judge="a3"),
        # q3: turn-2 votes only (must be excluded from turn-1 sampling)
        _vote(3, "m-x", "m-y", "model_a", turn=2),
        _vote(3, "m-x", "m-y", "model_b", turn=2),
        # q3: tie-only turn-1 group (excluded by the non-tie rule)
        _vote(3, "m-x", "m-y", "tie", judge="a1"),
        _vote(3, "m-x", "m-y", "tie", judge="a3"),
        # q4: many models, several ordered pairs, for sampling
    ]
    for i in range(3):
        votes.append(_vote(4, f"m-a{i}", f"m-a{i + 1}", "model_a" if i % 2 == 0 else "model_b", judge=f"j{i}"))
    with (data / "mt_bench_human_votes.jsonl").open("w") as fh:
        for v in votes:
            fh.write(json.dumps(v) + "\n")

    answers = [
        _answer(1, "m-x", "AX", "Q1"),
        _answer(1, "m-y", "AY", "Q1"),
        _answer(2, "m-x", "BX-long", "Q2"),
        _answer(2, "m-y", "BY", "Q2"),
        _answer(2, "m-y", "BX-long", "Q2"),  # same (q, model) key overwritten later on purpose
        _answer(4, "m-a0", "A0", "Q4"),
        _answer(4, "m-a1", "A1", "Q4"),
        _answer(4, "m-a2", "A2", "Q4"),
        _answer(4, "m-a3", "A3", "Q4"),
        _answer(4, "m-a4", "A4", "Q4"),
        _answer(4, "m-a5", "A5", "Q4"),
    ]
    with (data / "mt_bench_answers.jsonl").open("w") as fh:
        for a in answers:
            fh.write(json.dumps(a) + "\n")

    g4 = [
        _vote(1, "m-x", "m-y", "model_a", judge="gpt4_pair"),
        _vote(2, "m-y", "m-x", "model_a", judge="gpt4_pair"),  # reversed order row
    ]
    with (data / "mt_bench_gpt4_votes.jsonl").open("w") as fh:
        for v in g4:
            fh.write(json.dumps(v) + "\n")
    return tmp_path


# ---------------------------------------------------------------------------
# sample
# ---------------------------------------------------------------------------


def test_sample_deterministic_and_tie_free(root: Path):
    votes = M.load_jsonl(M.DATA_DIR / "mt_bench_human_votes.jsonl")
    answers = M.load_answers()
    first = M.sample_votes(votes, answers=answers)
    second = M.sample_votes(votes, answers=answers)
    assert first == second  # deterministic

    # tie votes and turn-2 rows excluded exactly once per ordered pair
    keys = [(p["question_id"], p["model_a"], p["model_b"]) for p in first]
    assert len(keys) == len(set(keys))
    for p in first:
        assert p["turn"] == 1
        assert not p["winner"].startswith("tie")
        assert p["winner"] in ("model_a", "model_b")
        assert p["human_winner"] == p["winner"]

    # expected pick order: sorted keys, first 6 available non-tie turn-1 ordered pairs
    expected_keys = [
        (1, "m-x", "m-y"),
        (2, "m-x", "m-y"),
        (2, "m-y", "m-x"),
        (4, "m-a0", "m-a1"),
        (4, "m-a1", "m-a2"),
        (4, "m-a2", "m-a3"),
    ]
    assert keys == expected_keys
    assert [p["pair_index"] for p in first] == list(range(6))
    # answers attached from the answer file
    p0 = first[0]
    assert p0["question"] == "Q1" and p0["answer_a"] == "AX" and p0["answer_b"] == "AY"


def test_sample_n_caps_and_seed_recorded():
    votes = [_vote(1, "a", "b", "model_a"), _vote(2, "a", "b", "model_b")]
    got = M.sample_votes(votes, n=1)
    assert len(got) == 1 and got[0]["question_id"] == 1


# ---------------------------------------------------------------------------
# human–human agreement
# ---------------------------------------------------------------------------


def test_human_human_agreement_handmade(root: Path):
    votes = M.load_jsonl(M.DATA_DIR / "mt_bench_human_votes.jsonl")
    no_ties = M.human_human_agreement(votes, include_ties=False)
    with_ties = M.human_human_agreement(votes, include_ties=True)

    # turn-1 vote groups: (q1 x,y) 3a+1b+tie; (q2 x,y) a+tie; (q2 y,x) 2a;
    # (q3 x,y) 2 ties
    # no ties: q1 -> C(4,2)=6 combos/3 agreeing; q2(x,y) 1 vote -> skip;
    # q2(y,x) -> 1/1; q3 has 0 non-tie votes -> skip
    assert no_ties["groups"] == 2
    assert no_ties["agreeing"] == 3 + 1
    assert no_ties["total"] == 6 + 1
    assert no_ties["rate"] == pytest.approx(4 / 7)

    # with ties: q1 -> C(5,2)=10/3; q2(x,y) -> 1/0; q2(y,x) -> 1/1;
    # q3 tie+tie -> 1 combo/1 agreeing
    assert with_ties["groups"] == 4
    assert with_ties["total"] == 10 + 1 + 1 + 1
    assert with_ties["agreeing"] == 3 + 0 + 1 + 1
    assert with_ties["rate"] == pytest.approx(5 / 13)


# ---------------------------------------------------------------------------
# verdict parsing
# ---------------------------------------------------------------------------


def test_parse_verdict():
    assert M.parse_verdict("Answer A is more complete and correct.\n\nJudge: A") == "A"
    assert M.parse_verdict("B has fewer errors.\njudge: b") == "B"
    assert M.parse_verdict("Both answers are equally good.\n\nJudge: tie") == "tie"


# ---------------------------------------------------------------------------
# agreement + bias on canned verdicts
# ---------------------------------------------------------------------------

PAIRS = [
    # 0: A in ab (=model_a), B in ba (=model_a) -> consistent model_a; human model_a -> AGREE
    {"pair_index": 0, "question_id": 10, "model_a": "ma", "model_b": "mb",
     "human_winner": "model_a", "answer_a": "aaa-long", "answer_b": "b", "question": "q"},
    # 1: A in ab (=model_a), A in ba (=model_b) -> FLIP, no consistent winner; human model_b
    {"pair_index": 1, "question_id": 11, "model_a": "ma", "model_b": "mb",
     "human_winner": "model_b", "answer_a": "short", "answer_b": "bbbb-long", "question": "q"},
    # 2: B in ab (=model_b), A in ba (=model_b) -> consistent model_b; human model_b -> AGREE
    {"pair_index": 2, "question_id": 12, "model_a": "ma", "model_b": "mb",
     "human_winner": "model_b", "answer_a": "b1", "answer_b": "bb-long", "question": "q"},
    # 3: B in ab (=model_b), B in ba (=model_a) -> FLIP; human model_a
    {"pair_index": 3, "question_id": 13, "model_a": "ma", "model_b": "mb",
     "human_winner": "model_a", "answer_a": "llong", "answer_b": "x", "question": "q"},
    # 4: A in ab (=model_a), tie in ba -> no consistent winner; human model_a
    {"pair_index": 4, "question_id": 14, "model_a": "ma", "model_b": "mb",
     "human_winner": "model_a", "answer_a": "xx-long", "answer_b": "y", "question": "q"},
    # 5: tie in ab, B in ba (=model_a) -> no consistent winner; human model_a
    {"pair_index": 5, "question_id": 15, "model_a": "ma", "model_b": "mb",
     "human_winner": "model_a", "answer_a": "z", "answer_b": "yyy-long", "question": "q"},
]


def _write_verdicts(root: Path, model: str):
    verdicts = {
        (0, "ab"): "A", (0, "ba"): "B",
        (1, "ab"): "A", (1, "ba"): "A",
        (2, "ab"): "B", (2, "ba"): "A",
        (3, "ab"): "B", (3, "ba"): "B",
        (4, "ab"): "A", (4, "ba"): "tie",
        (5, "ab"): "tie", (5, "ba"): "B",
    }
    for order in ("ab", "ba"):
        rows = []
        for i in range(6):
            p = PAIRS[i]
            rows.append(
                {
                    "pair_index": i,
                    "question_id": p["question_id"],
                    "model_a": "ma",
                    "model_b": "mb",
                    "order": order,
                    "model": model,
                    "raw": f"why\nJudge: {verdicts[(i, order)]}",
                    "verdict": verdicts[(i, order)],
                }
            )
        M._save_jsonl(M._verdict_path(model, order), rows)


def test_agreement_on_canned_verdicts(root: Path):
    _write_verdicts(root, "m")
    res = M.agreement_metrics("m", PAIRS)
    # consistent winner: p0 model_a (agree), p1 flip -> None, p2 model_b (agree),
    # p3 flip -> None, p4 tie mix -> None, p5 tie mix -> None
    assert res["n"] == 6
    assert res["agreeing"] == 2
    assert res["agreement"] == pytest.approx(2 / 6)
    assert res["tie_majorities"] == 4  # pairs 1, 3, 4, 5 have no consistent winner


def test_bias_on_canned_verdicts(root: Path):
    _write_verdicts(root, "m")
    res = M.bias_metrics("m", PAIRS)
    # flips: p1 (model_a vs model_b), p3 (model_b vs model_a) -> 2
    assert res["flips"] == 2
    assert res["position_flip_rate"] == pytest.approx(2 / 6)
    # first position wins: ab A = p0, p1, p4 (3) + ba A = p1, p2 (2) = 5 of 12
    assert res["first_position_wins"] == 5
    assert res["call_observations"] == 12
    # judge picks longer, per call (winner == longer model, ties don't count):
    # p0 model_a==longer(a) both orders -> 2; p1 flip -> 0; p2 model_b==longer(b)
    # both orders -> 2; p3 flip (model_b vs model_a), longer=a -> 0;
    # p4 model_a==longer(a) in ab, tie in ba -> 1; p5 tie then model_a, longer=b -> 0
    assert res["judge_picks_longer"] == 5
    # humans pick longer: p0..p4 yes, p5 human=model_a but b is longer -> no => 5
    assert res["human_picks_longer"] == 5
    # agreement conditioned on longer-wins: all pairs except p5 (5), agreeing p0, p2 => 2
    assert res["agree_longer_wins"]["n"] == 5
    assert res["agree_longer_wins"]["agreeing"] == 2
    assert res["agree_shorter_wins"]["n"] == 1
    assert res["agree_shorter_wins"]["rate"] == 0.0


def test_position_mapping():
    assert M._model_winner("A", "ab") == "model_a"
    assert M._model_winner("B", "ab") == "model_b"
    assert M._model_winner("A", "ba") == "model_b"
    assert M._model_winner("B", "ba") == "model_a"
    assert M._majority("A", "B") == "model_a"  # A-in-ab & B-in-ba = model_a, same model -> no flip
    assert M._majority("B", "A") == "model_b"  # B-in-ab & A-in-ba = model_b -> no flip
    assert M._majority("A", "A") is None  # A-in-ab=model_a vs A-in-ba=model_b -> position flip
    assert M._majority("B", "B") is None  # flip too
    assert M._majority("A", "tie") is None
    assert M._majority("tie", "A") is None


def test_judge_all_uses_fake_and_is_idempotent(root: Path):
    pairs = [
        {"pair_index": 0, "question_id": 9, "model_a": "ma", "model_b": "mb",
         "question": "hello q one", "answer_a": "AAA", "answer_b": "BBB"},
        {"pair_index": 1, "question_id": 9, "model_a": "ma", "model_b": "mb",
         "question": "hello q two", "answer_a": "CCC", "answer_b": "DDD"},
    ]
    fake = FakeLLM(canned={
        "hello q one": "A is clearly better.\n\nJudge: A",
        "hello q two": "Both fine.\n\nJudge: tie",
    })
    stats1 = M.judge_all(pairs, "m", "ab", client=fake)
    assert stats1 == {"calls": 2, "cached": 0, "seconds": stats1["seconds"]}
    rows = M._load_verdicts("m", "ab")
    assert [r["verdict"] for r in sorted(rows.values(), key=lambda r: r["pair_index"])] == ["A", "tie"]
    # re-run: everything cached -> zero calls, client untouched
    fake2 = FakeLLM({})
    stats2 = M.judge_all(pairs, "m", "ab", client=fake2)
    assert stats2["calls"] == 0 and stats2["cached"] == 2
    assert fake2.calls == []
    # verdicts unchanged (no duplicates appended)
    assert len(M._load_verdicts("m", "ab")) == 2


# ---------------------------------------------------------------------------
# PoLL panel (majority over judges)
# ---------------------------------------------------------------------------


def _write_verdicts_for(root: Path, model: str, ab: dict[int, str], ba: dict[int, str]):
    """Write ab/ba verdict rows for `model` on the given pair_index -> verdict maps."""
    for order, mapping in (("ab", ab), ("ba", ba)):
        rows = [
            {
                "pair_index": i,
                "question_id": 100 + i,
                "model_a": "ma",
                "model_b": "mb",
                "order": order,
                "model": model,
                "raw": f"why\nJudge: {v}",
                "verdict": v,
            }
            for i, v in mapping.items()
        ]
        M._save_jsonl(M._verdict_path(model, order), rows)


def test_panel_majority_of_two_judges(root: Path):
    # judge p1: pair0 consistent model_a (A in ab + B in ba); pair1 model_b
    #   (B in ab + A in ba); pair2 a flip (A in ab + A in ba -> None)
    _write_verdicts_for(root, "p1",
                        ab={0: "A", 1: "B", 2: "A"},
                        ba={0: "B", 1: "A", 2: "A"})
    # judge p2: pair0 model_b; pair1 model_b; pair2 model_a (A in ab + B in ba)
    _write_verdicts_for(root, "p2",
                        ab={0: "B", 1: "B", 2: "A"},
                        ba={0: "A", 1: "A", 2: "B"})

    pairs = [
        {"pair_index": 0, "question_id": 100, "model_a": "ma", "model_b": "mb", "human_winner": "model_a"},
        {"pair_index": 1, "question_id": 101, "model_a": "ma", "model_b": "mb", "human_winner": "model_b"},
        {"pair_index": 2, "question_id": 102, "model_a": "ma", "model_b": "mb", "human_winner": "model_a"},
    ]
    res = M.panel_verdicts(pairs, judges=("p1", "p2"))
    assert res["n"] == 3
    # pair0: p1 model_a vs p2 model_b -> bare split -> tie (human model_a -> miss)
    assert res["rows"][0]["panel"] == "tie" and res["rows"][0]["judge_votes"] == ["model_a", "model_b"]
    # pair1: both model_b -> panel model_b (human model_b -> agree)
    assert res["rows"][1]["panel"] == "model_b" and res["rows"][1]["agrees"]
    # pair2: p1 None (flip) vs p2 model_a -> 1 available -> model_a (human model_a -> agree)
    assert res["rows"][2]["panel"] == "model_a" and res["rows"][2]["judge_votes"] == [None, "model_a"]
    assert res["agreement"] == pytest.approx(2 / 3)
    assert res["tie_majorities"] == 1
    assert res["pairs_with_at_least_2_judges"] == 2  # pair0, pair1 (pair2 has 1)


def test_panel_three_judges_two_to_one(root: Path):
    _write_verdicts_for(root, "j1", ab={0: "A"}, ba={0: "B"})  # -> model_a
    _write_verdicts_for(root, "j2", ab={0: "A"}, ba={0: "B"})  # -> model_a
    _write_verdicts_for(root, "j3", ab={0: "B"}, ba={0: "A"})  # -> model_b
    pairs = [
        {"pair_index": 0, "question_id": 200, "model_a": "ma", "model_b": "mb", "human_winner": "model_a"},
    ]
    res = M.panel_verdicts(pairs, judges=("j1", "j2", "j3"))
    # 2 model_a + 1 model_b -> strict majority of 3 is model_a
    assert res["rows"][0]["panel"] == "model_a"
    assert res["rows"][0]["judge_votes"] == ["model_a", "model_a", "model_b"]
    assert res["rows"][0]["agrees"]


def test_panel_all_uninformative_is_tie(root: Path):
    _write_verdicts_for(root, "k1", ab={0: "A"}, ba={0: "A"})  # flip -> None
    _write_verdicts_for(root, "k2", ab={0: "tie"}, ba={0: "tie"})  # tie -> None
    pairs = [
        {"pair_index": 0, "question_id": 300, "model_a": "ma", "model_b": "mb", "human_winner": "model_a"},
    ]
    res = M.panel_verdicts(pairs, judges=("k1", "k2"))
    assert res["rows"][0]["panel"] == "tie"
    assert res["rows"][0]["judge_votes"] == [None, None]
    assert res["tie_majorities"] == 1 and res["agreement"] == 0.0
    assert res["pairs_with_at_least_2_judges"] == 0  # zero *available* picks


# ---------------------------------------------------------------------------
# Bradley–Terry + Spearman
# ---------------------------------------------------------------------------


def test_fit_bt_orders_three_models():
    xs = ["A", "A", "A", "B", "B", "B", "A", "A", "A"]
    ys = ["B", "B", "B", "C", "C", "C", "C", "C", "C"]
    winners = ["A"] * 9
    scores = M._fit_bt(xs, ys, winners, ["A", "B", "C"])
    # A beats everyone most -> top; C never wins -> bottom; max normalised to 1.0
    assert scores["A"] == pytest.approx(1.0)
    assert scores["A"] > scores["B"] > scores["C"]


def test_fit_bt_ties_split_half():
    # A vs B: 1 tie (0.5 each) -> symmetric, equal scores
    xs = ["A"]
    ys = ["B"]
    winners = ["tie"]
    scores = M._fit_bt(xs, ys, winners, ["A", "B"])
    assert scores["A"] == pytest.approx(scores["B"])


def test_spearman_same_and_inverted():
    same = {"A": 1, "B": 2, "C": 3}
    assert M._spearman(same, same) == pytest.approx(1.0)
    inverted = {"A": 3, "B": 2, "C": 1}
    assert M._spearman(same, inverted) == pytest.approx(-1.0)
