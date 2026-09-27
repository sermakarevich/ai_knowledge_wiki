"""Chapter 03 offline tests — labels (grading + taxonomy) and the trace viewer.

No network: `evals_tutorial.testing.FakeLLM` stands in for the Ollama grader,
and `settings.path` is redirected to `tmp_path` so no test writes into the real
project tree. Tests 2 and 4 read the real, committed data files (taxonomy,
answer_v1 labels, one trace, tickets) read-only.

Run with: cd project && uv run pytest -m "not slow" -q
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

import evals_tutorial.config as cfg
from evals_tutorial import labels as LB
from evals_tutorial import viewer as VW
from evals_tutorial.testing import FakeLLM

PROJECT_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture()
def root(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    """Redirect every `settings.path(...)` to tmp_path so nothing touches the real tree."""
    monkeypatch.setattr(cfg.Settings, "path", lambda self, rel: tmp_path / rel)
    return tmp_path


def _label_row_factory() -> dict:
    return {
        "pass": True,
        "missing_points": [],
        "unsupported_claims": ["the reply claims a 30-day window the handbook does not state"],
        "wrong_tone_or_promise": False,
        "did_not_answer": False,
        "note": "the reply fabricates a deadline that is not in the handbook sections",
    }


def _fake_trace() -> dict:
    return {"run": "answer_v1", "version": "v1", "ticket_id": "tkt-001", "input": "tkt-001", "output": "You have 30 days.", "retrieved": []}


def _fake_ticket() -> dict:
    return {
        "id": "tkt-001",
        "text": "tkt-001",
        "gold": {
            "category": "returns",
            "priority": "normal",
            "needs_escalation": False,
            "sections": ["returns"],
            "answer_points": ["Refunds are processed within 5 business days of receiving the package."],
        },
    }


# -- 1. grade_answer writes contract rows to the labels JSONL -------------------


def test_grade_answer_writes_contract_rows(monkeypatch: pytest.MonkeyPatch, root: Path):
    # The grader call is faked; `grade_messages`'s user message contains "tkt-001",
    # which FakeLLM json_answers match by substring of the last user message.
    llm = FakeLLM(json_answers={"tkt-001": _label_row_factory()})
    monkeypatch.setattr(LB, "load_traces", lambda run: [_fake_trace()])
    monkeypatch.setattr(LB, "_ticket_by_id", lambda: {"tkt-001": _fake_ticket()})
    labels_path = root / "data" / "labels" / "answer_v1.jsonl"
    monkeypatch.setattr(LB, "labels_path", lambda run: labels_path)

    returned = LB.grade_answer("answer_v1", client=llm)

    # returned in-memory rows
    assert len(returned) == 1
    row = returned[0]
    assert row["ticket_id"] == "tkt-001"
    assert row["pass"] is True
    assert row["failure_modes"] == []
    assert row["note"] == _label_row_factory()["note"]
    assert row["raw"]["unsupported_claims"] == _label_row_factory()["unsupported_claims"]

    # and the same row is on disk, one JSON line, loadable via the module loader
    assert labels_path.exists()
    on_disk = LB.load_labels("answer_v1")
    assert len(on_disk) == 1
    disk = on_disk[0]
    assert set(disk) == {"ticket_id", "pass", "failure_modes", "note", "raw"}
    assert set(disk["raw"]) == {"missing_points", "unsupported_claims", "wrong_tone_or_promise", "did_not_answer"}
    assert disk == row


# -- 2. taxonomy ids cover every failure_mode used in the committed failing labels


def test_taxonomy_ids_cover_committed_failure_modes():
    tax_path = PROJECT_ROOT / "data" / "labels" / "taxonomy.yaml"
    labels_path = PROJECT_ROOT / "data" / "labels" / "answer_v1.jsonl"
    assert tax_path.exists(), "taxonomy.yaml is missing"
    assert labels_path.exists(), "answer_v1.jsonl is missing"

    taxonomy = yaml.safe_load(tax_path.read_text())
    assert isinstance(taxonomy, list) and taxonomy, "taxonomy.yaml must be a non-empty list"

    taxonomy_ids = {m["id"] for m in taxonomy}
    assert taxonomy_ids, "no taxonomy ids loaded"

    # every committed mode id in the failing rows is defined in the taxonomy
    rows = [json.loads(line) for line in labels_path.read_text().splitlines() if line.strip()]
    failing = [r for r in rows if not r["pass"]]
    assert failing, "expected some failing rows in answer_v1"
    committed_modes = {m for r in failing for m in r.get("failure_modes") or []}
    assert committed_modes, "expected at least one failure_mode across failing rows"
    missing = committed_modes - taxonomy_ids
    assert not missing, f"failure modes used in labels but absent from the taxonomy: {missing}"

    # sanity: each taxonomy entry is well-formed and its examples are all failing tickets
    failing_ids = {r["ticket_id"] for r in failing}
    for entry in taxonomy:
        assert set(entry) >= {"id", "name", "definition"}, f"malformed taxonomy entry: {entry!r}"
        for ex in entry.get("example_ticket_ids") or []:
            assert ex in failing_ids, f"{entry['id']}: example {ex!r} is not a failing ticket"


# -- 3. table-driven triage grading (pure code, no LLM) -------------------------


@pytest.mark.parametrize(
    "predicted, gold, expected_modes",
    [
        (
            # fully correct -> pass, no modes
            {"category": "returns", "priority": "normal", "needs_escalation": False},
            {"category": "returns", "priority": "normal", "needs_escalation": False},
            [],
        ),
        (
            # wrong category only
            {"category": "privacy", "priority": "normal", "needs_escalation": False},
            {"category": "returns", "priority": "normal", "needs_escalation": False},
            ["wrong_category"],
        ),
        (
            # wrong priority only
            {"category": "returns", "priority": "urgent", "needs_escalation": False},
            {"category": "returns", "priority": "normal", "needs_escalation": False},
            ["wrong_priority"],
        ),
        (
            # wrong escalation only
            {"category": "returns", "priority": "normal", "needs_escalation": True},
            {"category": "returns", "priority": "normal", "needs_escalation": False},
            ["wrong_escalation"],
        ),
        (
            # all three wrong -> all three modes, in a stable order
            {"category": "privacy", "priority": "urgent", "needs_escalation": True},
            {"category": "returns", "priority": "normal", "needs_escalation": False},
            ["wrong_category", "wrong_priority", "wrong_escalation"],
        ),
    ],
)
def test_grade_triage_table_driven(predicted: dict, gold: dict, expected_modes: list[str]):
    trace = {"run": "triage_v1", "ticket_id": "tkt-x", "output": dict(predicted, reason="predicted reason")}
    ticket = {"id": "tkt-x", "gold": dict(gold)}

    out = LB.grade_triage(trace, ticket)

    assert set(out) == {"ticket_id", "pass", "failure_modes", "note", "raw"}
    assert out["ticket_id"] == "tkt-x"
    assert out["failure_modes"] == expected_modes
    assert (not out["failure_modes"]) == out["pass"], "pass must be the inverse of failure_modes"
    if expected_modes:
        assert "gold" in out["note"], "a failing row must describe the mismatch against gold"
    # raw carries both sides for audit
    assert out["raw"]["predicted"]["category"] == predicted["category"]
    assert out["raw"]["gold"] == {k: gold[k] for k in ("category", "priority", "needs_escalation")}


# -- 4. viewer.build_page renders a standalone, self-contained HTML page --------


def test_build_page_standalone(monkeypatch: pytest.MonkeyPatch, root: Path):
    trace = {"run": "answer_v1", "version": "v1", "ticket_id": "tkt-001", "input": "ticket text here", "output": "30 days, you said", "retrieved": [{"section": "returns", "score": 0.9}], "model": "qwen3.8:27b", "latency_s": 1.2}
    ticket = {
        "id": "tkt-001",
        "topic": "returns",
        "scenario": "simple_question",
        "gold": {"category": "returns", "priority": "normal", "needs_escalation": False, "sections": ["returns"], "answer_points": ["5 business days refund window"]},
    }
    label = {"ticket_id": "tkt-001", "pass": False, "failure_modes": ["missing_required_fact"], "note": "omits the 5-day refund window"}

    # build_page reads through these three module-level loaders — patch them so no
    # real files are needed and the test is hermetic.
    monkeypatch.setattr(VW, "load_traces", lambda run: [trace])
    monkeypatch.setattr(VW, "load_labels", lambda run: {label["ticket_id"]: label})
    monkeypatch.setattr(VW, "tickets_by_id", lambda: {ticket["id"]: ticket})

    page = VW.build_page("answer_v1")

    assert page.startswith("<!doctype html>")
    assert page.endswith("</html>")
    assert "tkt-001" in page
    assert "returns" in page
    assert "missing_required_fact" in page  # failure-mode badge
    assert "omits the 5-day refund window" in page  # grader note surfaced
    assert "Filter by failure mode" in page  # <details> panel doubles as a filter
    assert "1 traces" in page and "0 pass / 1 fail" in page

    # self-contained: no scripts, stylesheets or font links pulled from outside
    for external in ['<script src=', "<link rel=\"stylesheet\" href=", '<link rel="stylesheet" href=', "url(http", "@import url"]:
        assert external not in page, f"page should not reference an external resource: {external}"
