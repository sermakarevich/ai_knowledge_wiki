"""Chapter 02 offline tests. No network — `evals_tutorial.testing.FakeLLM`
(plus its delegated `FakeEmbedder`) stands in for the real Ollama client, and
`settings.path` is redirected to `tmp_path` so no test touches the project tree.

Run with: cd project && uv run pytest tests/ -q -m "not slow"
"""

from __future__ import annotations

import json
import random
from collections import Counter
from pathlib import Path

import pytest
from pydantic import ValidationError

import evals_tutorial.config as cfg
from evals_tutorial import helpdesk as HD
from evals_tutorial import handbook as HB
from evals_tutorial import tickets as TK
from evals_tutorial.handbook import SECTION_IDS
from evals_tutorial.testing import FakeLLM

SECTION_IDS = set(HB.SECTION_IDS)
VALID_PRIORITIES = {"low", "normal", "high", "urgent"}
TRACE_REQUIRED = {"run", "version", "ticket_id", "input", "retrieved", "prompt", "output", "latency_s", "model", "usage"}


@pytest.fixture()
def root(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    """Redirect every `settings.path(...)` to tmp_path so the SUT is fully isolated."""
    monkeypatch.setattr(cfg.Settings, "path", lambda self, rel: tmp_path / rel)
    HB.handbook_dir = lambda: tmp_path / "data" / "handbook"
    HD.handbook_dir = lambda: tmp_path / "data" / "handbook"
    return tmp_path


@pytest.fixture()
def handbook(root: Path) -> list[Path]:
    """Write 12 plausible handbook sections to the isolated root."""
    d = root / "data" / "handbook"
    d.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for sid in SECTION_IDS:
        p = d / f"{sid}.md"
        p.write_text(
            f"# {tid_to_title(sid)}\n"
            f"{sid.replace('_', ' ')} policy: you can act within 30 days. "
            "The fee is 20 percent. The cap is 500 euros. You get 3 chances.\n"
            "\n## Key facts\n"
            "- 30 days to act\n"
            "- 20 percent fee\n"
            "- 500 euro cap\n"
            "- 3 chances allowed\n"
        )
        written.append(p)
    return written


def tid_to_title(sid: str) -> str:
    return HB.SECTION_TITLES[sid]


@pytest.fixture()
def tickets_rows(handbook: list[Path]) -> list[dict]:
    """Generate+split the 80 rows (labels first, canned LLM text)."""
    return TK.split(TK.generate(client=FakeLLM(canned={"customer": "customer message: I have 30 days left and need a 500 euro refund."})))


# -- grid coverage ------------------------------------------------------------


def test_grid_coverage_floors_hold():
    combos = TK.pick_grid(random.Random(TK.SEED))
    assert len(combos) == TK.N_TICKETS == 80

    topics = Counter(sid for _, sid, _ in combos)
    scenarios = Counter(sc for _, _, sc in combos)

    assert set(topics) == SECTION_IDS, f"missing topics: {SECTION_IDS - set(topics)}"
    assert min(topics.values()) >= 5, "each topic must appear >= 5 times"
    assert set(scenarios) == set(TK.SCENARIOS)
    assert min(scenarios.values()) >= 15, "each scenario must appear >= 15 times"


# -- gold labels by construction ----------------------------------------------


def test_gold_category_is_the_topic():
    assert TK.gold_labels("warranty", "simple_question", [], False)["category"] == "warranty"
    assert TK.gold_labels("privacy", "urgent_blocker", [], False)["category"] == "privacy"


def test_gold_priority_matches_scenario_table():
    for scenario, prio in TK.PRIORITY_BY_SCENARIO.items():
        got = TK.gold_labels("returns", scenario, [], False)["priority"]
        assert prio == got, scenario


def test_gold_escalation_rule():
    # out_of_policy_request always escalates, regardless of topic
    assert TK.gold_labels("returns", "out_of_policy_request", [], False)["needs_escalation"] is True
    assert TK.gold_labels("shipping", "out_of_policy_request", [], False)["needs_escalation"] is True
    # urgent_blocker only escalates on the sensitive topics
    assert TK.gold_labels("payments", "urgent_blocker", [], False)["needs_escalation"] is True
    assert TK.gold_labels("privacy", "urgent_blocker", [], False)["needs_escalation"] is True
    assert TK.gold_labels("damaged_items", "urgent_blocker", [], False)["needs_escalation"] is True
    assert TK.gold_labels("returns", "urgent_blocker", [], False)["needs_escalation"] is False
    # simple_question / problem_report never escalate
    assert TK.gold_labels("payments", "simple_question", [], False)["needs_escalation"] is False
    assert TK.gold_labels("payments", "problem_report", [], False)["needs_escalation"] is False


def test_gold_sections_includes_related_when_flagged():
    related = TK.RELATED_SECTION["returns"]
    without = TK.gold_labels("returns", "simple_question", ["a"], False)
    with_ = TK.gold_labels("returns", "simple_question", ["a"], True)
    assert without["sections"] == ["returns"]
    assert set(with_["sections"]) == {"returns", related}


def test_gold_answer_points_are_the_chosen_facts():
    got = TK.gold_labels("shipping", "problem_report", ["30 days to act", "20 percent fee"], False)
    assert got["answer_points"] == ["30 days to act", "20 percent fee"]


# -- ticket file: shape + splits ----------------------------------------------


def test_ticket_counts_and_split(tickets_rows: list[dict]):
    splits = Counter(r["split"] for r in tickets_rows)
    assert splits == {"dev": 20, "test": 60}

    topics_in_dev = {r["topic"] for r in tickets_rows if r["split"] == "dev"}
    topics_in_test = {r["topic"] for r in tickets_rows if r["split"] == "test"}
    assert topics_in_dev == SECTION_IDS, "every topic should appear in dev"
    assert topics_in_test == SECTION_IDS, "every topic should appear in test"


def test_ticket_row_shape_and_gold_schema(tickets_rows: list[dict]):
    for r in tickets_rows:
        assert set(r.keys()) == {"id", "split", "persona", "topic", "scenario", "text", "gold"}
        assert r["topic"] in SECTION_IDS
        assert r["scenario"] in TK.SCENARIOS
        g = r["gold"]
        assert set(g) == {"category", "priority", "needs_escalation", "sections", "answer_points"}
        assert g["category"] == r["topic"]
        assert g["category"] in SECTION_IDS
        assert g["priority"] in VALID_PRIORITIES
        assert isinstance(g["needs_escalation"], bool)
        assert isinstance(g["sections"], list)
        assert g["category"] in g["sections"]
        assert r["scenario"] not in g  # sanity: gold is not a raw copy
        assert all(isinstance(f, str) and f for f in g["answer_points"])


def test_tickets_write_and_load_roundtrip(root: Path, tickets_rows: list[dict]):
    path = TK.write(tickets_rows)
    rows = TK.load_tickets(path)
    assert rows == tickets_rows


# -- triage schema ------------------------------------------------------------


def test_triage_schema_accepts_valid_json():
    t = HD.Triage.model_validate(
        {"category": "returns", "priority": "normal", "needs_escalation": False, "reason": "asking about the 30-day rule"}
    )
    assert t.category == "returns" and t.priority == "normal" and t.needs_escalation is False


@pytest.mark.parametrize(
    "bad",
    [
        {"category": "not_a_section", "priority": "low", "needs_escalation": False, "reason": "r"},
        {"category": "returns", "priority": "whenever", "needs_escalation": False, "reason": "r"},
        {"category": "returns", "priority": "low", "needs_escalation": False},  # missing `reason`
        {"priority": "low", "needs_escalation": False, "reason": "r"},  # missing `category`
    ],
)
def test_triage_schema_rejects_invalid(bad: dict):
    with pytest.raises(ValidationError):
        HD.Triage.model_validate(bad)


def test_triage_via_fakellm(root: Path):
    llm = FakeLLM(json_answers={"ticket-t": {"category": "returns", "priority": "normal", "needs_escalation": False, "reason": "asked about 30 days"}})
    out = HD.triage("ticket-t", client=llm)
    assert isinstance(out, HD.Triage)
    assert out.category == "returns"


def test_triage_messages_shape(root: Path):
    msgs = HD.triage_messages("I want to return my bike")
    assert msgs[0]["role"] == "system" and "category" in msgs[0]["content"]
    assert msgs[1]["role"] == "user" and msgs[1]["content"] == "I want to return my bike"


# -- retrieval ----------------------------------------------------------------


def test_retrieve_returns_ranked_known_sections(root: Path, handbook: list[Path]):
    retrieved = HD.retrieve("I want to return my bike within the 30 days and my refund of 500 euros", client=FakeLLM())
    assert retrieved, "retrieve returned nothing"
    assert all(row["section"] in SECTION_IDS for row in retrieved)
    scores = [row["score"] for row in retrieved]
    assert scores == sorted(scores, reverse=True), "scores must be non-increasing"
    assert len({row["section"] for row in retrieved}) == len(retrieved), "no duplicate sections"


def test_retrieve_empty_if_no_handbook(root: Path):
    # The `handbook` fixture does NOT run here, so the isolated root has no handbook.
    assert HD.retrieve("anything at all", client=FakeLLM()) == []


def test_retrieved_context_limits_blocks_to_top_n(root: Path, handbook: list[Path]):
    llm = FakeLLM()
    blocks, rows = HD.retrieved_context("I want to return my bike within the 30 days", client=llm)
    assert 0 < len(blocks) <= HD.TOP_SECTIONS
    assert len(blocks) == len(rows[:HD.TOP_SECTIONS])
    assert all(b.strip() for b in blocks)


# -- trace contract -----------------------------------------------------------


def _fakellm_for_traces() -> FakeLLM:
    return FakeLLM(
        canned={"ticket-t": "Sure, per [returns] you have 30 days and a 20 percent fee. See [shipping] for details."},
        json_answers={"ticket-t": {"category": "returns", "priority": "low", "needs_escalation": False, "reason": "30-day window"}},
    )


def test_triage_trace_contract(root: Path, handbook: list[Path]):
    path = HD.write_trace(
        task="triage",
        version="v1",
        ticket={"id": "tkt-100", "text": "ticket-t"},
        prompt=HD.prompt_text("triage", "v1"),
        output=HD.triage("ticket-t", client=_fakellm_for_traces()),
        retrieved=[],
    )
    trace = json.loads(path.read_text())
    assert TRACE_REQUIRED <= set(trace), f"missing keys: {TRACE_REQUIRED - set(trace)}"
    assert trace["run"] == "triage_v1"
    assert trace["version"] == "v1"
    assert trace["ticket_id"] == "tkt-100"
    assert trace["input"] == "ticket-t"
    assert trace["retrieved"] == []
    assert trace["output"]["category"] == "returns"
    assert trace["prompt"] == HD.prompt_text("triage", "v1")
    assert path.parent.name == "triage_v1" and path.name == "tkt-100.json"


def test_answer_trace_contract(root: Path, handbook: list[Path]):
    llm = _fakellm_for_traces()
    ticket = {"id": "tkt-200", "text": "ticket-t"}
    retrieved = HD.retrieve(ticket["text"], client=llm)
    path = HD.write_trace(
        task="answer",
        version="v1",
        ticket=ticket,
        prompt=HD.prompt_text("answer", "v1"),
        output=HD.answer(ticket["text"], client=llm),
        retrieved=retrieved,
    )
    trace = json.loads(path.read_text())
    assert TRACE_REQUIRED <= set(trace)
    assert trace["run"] == "answer_v1"
    assert trace["output"] == "Sure, per [returns] you have 30 days and a 20 percent fee. See [shipping] for details."
    assert trace["retrieved"] and all(set(r) == {"section", "score"} for r in trace["retrieved"])


def test_load_traces_sorted(root: Path, handbook: list[Path]):
    llm = _fakellm_for_traces()
    for tid in ["tkt-003", "tkt-001", "tkt-002"]:
        HD.write_trace(
            task="triage",
            version="v1",
            ticket={"id": tid, "text": "ticket-t"},
            prompt=HD.prompt_text("triage", "v1"),
            output=HD.triage("ticket-t", client=llm),
            retrieved=[],
        )
    loaded = HD.load_traces("triage_v1")
    assert [t["ticket_id"] for t in loaded] == ["tkt-001", "tkt-002", "tkt-003"]


# -- prompt version files exist (frozen once traces are recorded) --------------


def test_v1_prompt_files_exist():
    triage_prompt = HD.prompt_text("triage", "v1")
    answer_prompt = HD.prompt_text("answer", "v1")
    assert triage_prompt.strip() and answer_prompt.strip()
    # v1 prompts are system-only templates — no ticket/context placeholders.
    assert "{ticket}" not in triage_prompt and "{ticket}" not in answer_prompt
    assert "{context}" not in answer_prompt
