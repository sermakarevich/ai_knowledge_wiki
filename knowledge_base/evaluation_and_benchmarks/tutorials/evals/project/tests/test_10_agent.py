"""Chapter 10a offline tests — no network, no Ollama."""

from __future__ import annotations

import json
import copy

import pytest

from evals_tutorial import agent
from evals_tutorial.agent import (
    Order,
    ShopDB,
    check_assertions,
    check_forbidden,
    check_required,
    check_reply,
    check_steps,
    cancel_order,
    call_tool,
    escalate,
    fresh_db,
    list_orders,
    grade_episode,
    issue_refund,
    load_tasks,
    lookup_order,
    pass_at_k,
    pass_pow_k,
    reply,
    run_episode,
    start_return,
    update_address,
)


class StubLLM:
    """A small stand-in for `Ollama` that emits a scripted sequence of
    assistant messages (tool calls and/or plain text), one per
    `chat_with_tools` call. Used by `run_episode` tests in place of the real
    model — no network."""

    def __init__(self, scripts: list[dict]):
        self.scripts = list(scripts)
        self.calls: list[dict] = []

    def chat_with_tools(self, messages, tools=None, temperature=0.0, seed=None):
        self.calls.append({"messages": messages, "tools": tools,
                           "temperature": temperature, "seed": seed})
        if not self.scripts:
            return {"role": "assistant", "content": "stub says stop"}
        return self.scripts.pop(0)


# ---------------------------------------------------------------------------
# DB construction and reset
# ---------------------------------------------------------------------------


def test_fresh_db_is_deterministic():
    a, b = fresh_db(), fresh_db()
    assert a.snapshot() == b.snapshot()
    assert len(a.customers) >= 12
    assert len(a.orders) == 15
    statuses = {o.status for o in a.orders}
    # spec asks for the core five statuses in the DB
    assert {"placed", "shipped", "delivered", "returned", "cancelled"} <= statuses


def test_unknown_order_raises():
    db = fresh_db()
    with pytest.raises(KeyError):
        db.order("NOPE")


def test_by_email_filters():
    db = fresh_db()
    maya = db.by_email("maya.chen@example.com")
    assert [o.order_id for o in maya] == ["O120", "O121"]


# ---------------------------------------------------------------------------
# tools — happy paths
# ---------------------------------------------------------------------------


def test_cancel_placed_order_refunds_full():
    db = fresh_db()
    r = cancel_order(db, "O101")
    assert r["ok"] is True
    o = db.order("O101")
    assert o.status == "cancelled"
    assert o.fee == 0.0
    assert o.refund_total == 120.0


def test_cancel_processing_order_applies_fee():
    db = fresh_db()
    cancel_order(db, "O106")
    o = db.order("O106")
    assert o.status == "cancelled"
    assert o.fee == 5.0
    assert o.refund_total == 215.0


def test_update_address_within_window():
    db = fresh_db()
    r = update_address(db, "O102", {"street": "5 Harbor Ct", "city": "Rivertown", "zip": "04102"})
    assert r["ok"] is True
    assert db.order("O102").address == {"street": "5 Harbor Ct", "city": "Rivertown", "zip": "04102"}


def test_start_return_in_window_records():
    db = fresh_db()
    r = start_return(db, "O104", "I1", "scratched")
    assert r["ok"] is True
    o = db.order("O104")
    assert o.return_status == "started"
    assert o.return_item == "I1"
    assert o.refund_total == 0.0  # start_return does not move money


def test_issue_refund_after_started_return_ok():
    db = fresh_db()
    start_return(db, "O104", "I1")
    r = issue_refund(db, "O104", 180.0)
    assert r["ok"] is True
    assert db.order("O104").refund_total == 180.0


def test_escalate_records_reason():
    db = fresh_db()
    r = escalate(db, "refund >= 200 without return")
    assert r["ok"] is True and r["escalation_id"].startswith("E")
    assert db.escalations and db.escalations[-1]["reason"] == "refund >= 200 without return"


def test_reply_is_terminal():
    db = fresh_db()
    assert reply(db, "All set.") == {"ok": True, "ended": True, "text": "All set."}


# ---------------------------------------------------------------------------
# tools — policy refusals
# ---------------------------------------------------------------------------


def test_cancel_shipped_order_refused():
    db = fresh_db()
    before = db.snapshot()
    r = cancel_order(db, "O103")
    assert r["ok"] is False
    assert "shipped" in r["error"]
    assert db.snapshot() == before


def test_cancel_delivered_order_refused():
    db = fresh_db()
    before = db.snapshot()
    r = cancel_order(db, "O104")
    assert r["ok"] is False and "shipped" in r["error"]
    assert db.snapshot() == before


def test_update_address_locked_after_ship():
    db = fresh_db()
    before = db.snapshot()
    addr = {"street": "99 Elm", "city": "Rivertown", "zip": "04103"}
    r = update_address(db, "O103", addr)
    assert r["ok"] is False
    assert db.snapshot() == before


def test_start_return_refused_out_window():
    db = fresh_db()
    before = db.snapshot()
    r = start_return(db, "O108", "I1", "broke")
    assert r["ok"] is False
    assert "window" in r["error"]
    assert db.snapshot() == before


def test_start_return_refused_custom_item():
    # O111 is delivered but its (only) item is custom-configured
    db = fresh_db()
    before = db.snapshot()
    r = start_return(db, "O111", "I1", "not what I wanted")
    assert r["ok"] is False
    assert "custom" in r["error"] or "personalized" in r["error"]
    assert db.snapshot() == before


def test_issue_refund_above_threshold_needs_escalate():
    db = fresh_db()
    r = issue_refund(db, "O110", 240.0)
    assert r["ok"] is False
    assert "escalate" in r["error"]
    # escalate, then it works
    assert escalate(db, "refund 240")["ok"] is True
    r2 = issue_refund(db, "O110", 240.0)
    assert r2["ok"] is True
    assert db.order("O110").refund_total == 240.0


def test_issue_refund_capped_at_total_and_cumulative():
    db = fresh_db()
    assert issue_refund(db, "O101", 50.0)["ok"] is True
    assert issue_refund(db, "O101", 50.0)["ok"] is True
    assert issue_refund(db, "O101", 75.0)["ok"] is False  # would exceed total 120
    assert db.order("O101").refund_total == 100.0


def test_unknown_order_errors_not_crashes():
    db = fresh_db()
    for name, args in [
        ("lookup_order", {"order_id": "NO"}),
        ("list_orders", {"email": "nobody@example.com"}),
        ("cancel_order", {"order_id": "NO"}),
        ("update_address", {"order_id": "NO", "address": {"x": 1}}),
        ("start_return", {"order_id": "NO", "item_id": "I1"}),
        ("issue_refund", {"order_id": "NO", "amount": 5.0}),
    ]:
        result, errored = call_tool(db, name, args)
        assert name not in ("lookup_order",) or result.get("ok") is False
        if name != "list_orders":
            assert result.get("ok") is False and "unknown order" in result["error"]
        assert errored is True
    # list_orders returns ok: False when nobody matches
    result, errored = call_tool(db, "list_orders", {"email": "nobody@example.com"})
    assert result["ok"] is False


def test_unknown_tool_is_error():
    db = fresh_db()
    result, errored = call_tool(db, "no_such_tool", {})
    assert result["ok"] is False and "unknown tool" in result["error"]
    assert errored is True


def test_bad_arguments_do_not_crash():
    db = fresh_db()
    result, errored = call_tool(db, "issue_refund", {"order_id": "O101", "amount": "lots"})
    assert result["ok"] is False
    assert errored is True


# ---------------------------------------------------------------------------
# grading functions
# ---------------------------------------------------------------------------


def _snapshot_with(order_id: str = "O101", status: str = "cancelled", fee: float = 0.0) -> dict:
    return {"orders": {order_id: {"status": status, "fee": fee, "refund_total": 0.0}}, "escalations": []}


def test_check_assertions_pass_and_fail():
    snap = _snapshot_with()
    ok = check_assertions(snap, {"orders.O101.status": "cancelled", "orders.O101.fee": 0.0})
    assert all(c["pass"] for c in ok)
    bad = check_assertions(snap, {"orders.O101.status": "delivered"})
    assert bad[0]["pass"] is False
    missing = check_assertions(snap, {"orders.NOPE.status": "x"})
    assert missing[0]["pass"] is False


def test_check_required_and_forbidden():
    used = ["lookup_order", "cancel_order", "reply"]
    assert all(c["pass"] for c in check_required(used, ["cancel_order", "lookup_order"]))
    assert not all(c["pass"] for c in check_required(used, ["start_return"]))
    assert check_forbidden(used, []) is True
    assert check_forbidden(used, ["issue_refund"]) is True
    assert check_forbidden(used, ["cancel_order"]) is False


def test_check_steps_and_reply():
    assert check_steps(3, 8) and not check_steps(9, 8)
    assert check_reply("All set, cancelled.", ["cancelled"])
    assert not check_reply("All set.", ["cancelled"])
    assert not check_reply(None, ["x"])
    assert check_reply("anything", [])


def test_grade_episode_passes():
    task = {
        "id": "t01",
        "expected_state": {"orders.O101.status": "cancelled", "orders.O101.fee": 0.0},
        "required_actions": ["cancel_order"],
        "forbidden_actions": ["issue_refund"],
        "max_steps": 8,
        "expected_reply_keywords": ["cancelled"],
    }
    traj = {
        "state_after": {"orders": {"O101": {"status": "cancelled", "fee": 0.0, "refund_total": 120.0}}, "escalations": []},
        "used_tools": ["lookup_order", "cancel_order", "reply"],
        "final_reply": "Cancelled your order O101, refund of 120 on the way.",
        "steps_detail": [1, 2, 3],
    }
    g = grade_episode(task, traj)
    assert g["pass"] is True
    assert g["failed"] == []


def test_grade_episode_fails_for_forbidden_tool():
    task = {"expected_state": {"orders.O101.status": "cancelled"}, "forbidden_actions": ["cancel_order"]}
    traj = {"state_after": {"orders": {"O101": {"status": "cancelled"}}, "escalations": []},
            "used_tools": ["cancel_order"], "final_reply": "ok", "steps_detail": [1]}
    g = grade_episode(task, traj)
    assert g["pass"] is False and "no_forbidden_tools" in g["failed"]


def test_grade_episode_fails_for_over_budget_and_bad_reply():
    task = {"expected_state": {}, "max_steps": 1, "expected_reply_keywords": ["yes"]}
    traj = {"state_after": {"orders": {}}, "used_tools": [], "final_reply": "no", "steps_detail": [1, 2]}
    g = grade_episode(task, traj)
    assert "within_step_budget" in g["failed"] and "final_reply" in g["failed"]


# ---------------------------------------------------------------------------
# pass@k / pass^k
# ---------------------------------------------------------------------------


def _trajs(*rows):
    return [
        {"task_id": tid, "pass": flag, "trial": i}
        for tid, flags in rows for i, flag in enumerate(flags)
    ]


def test_pass_at_k_and_pow_k_semantics():
    trajs = _trajs(("A", [True, False, True]), ("B", [True, True, True]), ("C", [False, False, False]))
    pak = {r["task_id"]: r["pass_at_k"] for r in pass_at_k(trajs)}
    ppk = {r["task_id"]: r["pass_pow_k"] for r in pass_pow_k(trajs)}
    assert pak == {"A": True, "B": True, "C": False}
    assert ppk == {"A": False, "B": True, "C": False}


def test_pass_at_k_all_false_is_zero_pow():
    trajs = _trajs(("X", [False, False, False]))
    assert pass_at_k(trajs)[0]["pass_at_k"] is False
    assert pass_pow_k(trajs)[0]["pass_pow_k"] is False


# ---------------------------------------------------------------------------
# agent loop integration (offline, via StubLLM)
# ---------------------------------------------------------------------------


def test_run_episode_cancel_flow(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    scripts = [
        {"role": "assistant", "tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "O101"}}]},
        {"role": "assistant", "tool_calls": [{"name": "cancel_order", "arguments": {"order_id": "O101"}}]},
        {"role": "assistant", "tool_calls": [{"name": "reply", "arguments": {"text": "cancelled O101 for you."}}]},
    ]
    task = load_tasks()[0]  # t01
    traj = run_episode(task, StubLLM(scripts), project_root=_real_project_root())
    assert traj["ended_with_reply"] is True
    assert traj["grade"]["pass"] is True
    o = traj["state_after"]["orders"]["O101"]
    assert o["status"] == "cancelled" and o["refund_total"] == 120.0
    assert traj["used_tools"] == ["lookup_order", "cancel_order", "reply"]


def _real_project_root():
    # `run_episode` resolves prompts/ + data/handbook relative to project_root;
    # point at this repo so tests run from anywhere.
    from pathlib import Path

    return Path(__file__).resolve().parent.parent.parent


def test_run_episode_bad_tool_is_recorded_not_fatal(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    scripts = [
        {"role": "assistant", "tool_calls": [{"name": "no_such_tool", "arguments": {}}]},
        {"role": "assistant", "tool_calls": [{"name": "reply", "arguments": {"text": "done."}}]},
    ]
    task = {"id": "tX", "customer_email": "x@example.com", "user_message": "m",
            "expected_state": {}, "required_actions": [], "forbidden_actions": [],
            "max_steps": 8, "expected_reply_keywords": ["done"]}
    traj = run_episode(task, StubLLM(scripts), project_root=_real_project_root())
    steps = traj["steps_detail"]
    assert steps[0]["tool"] == "no_such_tool" and steps[0]["error"] is True
    assert traj["steps"] == 2
    assert traj["grade"]["no_forbidden"] is True


# ---------------------------------------------------------------------------
# smoke: CLI helpers
# ---------------------------------------------------------------------------


def test_load_tasks_shape():
    tasks = load_tasks()
    assert len(tasks) == 20
    cats = {t["category"] for t in tasks}
    assert cats == {"straightforward", "policy", "escalation"}
    ids = {t["id"] for t in tasks}
    assert {"t01", "t05", "t10", "t17"} <= ids
    # DEMO_TASK_IDS are present and all tasks have required keys
    for t in tasks:
        for key in ("id", "customer_email", "user_message", "expected_state",
                    "required_actions", "forbidden_actions", "max_steps",
                    "expected_reply_keywords"):
            assert key in t, (t["id"], key)


def test_tool_schemas_cover_tools():
    names = {s["function"]["name"] for s in agent.TOOL_SCHEMAS}
    assert names == set(agent.TOOLS.keys())
    for s in agent.TOOL_SCHEMAS:
        fn = s["function"]
        params = fn["parameters"]
        assert params["type"] == "object"
        assert params["required"], fn["name"]
        assert set(params["required"]) <= set(params["properties"].keys()) or fn["name"] in ("list_orders", "reply")


# ---------------------------------------------------------------------------
# chapter 10b — kappa, stats, transcript judge, multi-turn simulate
# ---------------------------------------------------------------------------


def test_cohen_kappa_extremes_and_partial():
    k = agent._cohen_kappa
    assert k([1, 0, 1, 0], [1, 0, 1, 0]) == 1.0  # identical
    assert k([1, 1, 0, 0], [0, 0, 1, 1]) == -1.0  # fully opposite
    # partial: po=0.5, p1a=0.5, p0a=0.5, p1b=0.5, p0b=0.5 -> pe=0.5 -> kappa=0
    assert k([1, 0, 1, 0], [0, 1, 0, 1]) == -1.0
    assert 0.0 < k([1, 1, 0, 0], [1, 1, 1, 0]) < 1.0
    with pytest.raises(ValueError, match="same length"):
        k([1, 0], [1, 0, 1])


def test_pass_k_stats_has_ci_and_per_task_and_type():
    trajs = [
        {"task_id": "A", "pass": True, "trial": 0, "task": {"category": "straightforward"}},
        {"task_id": "A", "pass": True, "trial": 1, "task": {"category": "straightforward"}},
        {"task_id": "A", "pass": False, "trial": 2, "task": {"category": "straightforward"}},
        {"task_id": "B", "pass": False, "trial": 0, "task": {"category": "policy"}},
        {"task_id": "B", "pass": False, "trial": 1, "task": {"category": "policy"}},
        {"task_id": "B", "pass": False, "trial": 2, "task": {"category": "policy"}},
    ]
    s = agent.pass_k_stats(trajs)
    assert s["n_tasks"] == 2
    assert s["n_trials"] == 6
    assert s["k"] == 3
    # 1 of 2 tasks has >=1 pass
    assert s["pass_at_k"] == 0.5
    # 0 of 2 tasks has all pass
    assert s["pass_pow_k"] == 0.0
    assert s["pass_at_k_ci"]["pass_at_k"]
    assert [0.0, 1.0] == s["pass_at_k_ci"]["pass_at_k"]  # degenerate bootstrap with 2 tasks
    assert s["per_task"][0]["task_id"] == "A" and s["per_task"][1]["task_id"] == "B"


def test_per_task_type_stats_buckets_by_category():
    trajs = [
        {"task_id": "A", "pass": True, "trial": 0, "task": {"category": "straightforward"}},
        {"task_id": "A", "pass": True, "trial": 1, "task": {"category": "straightforward"}},
        {"task_id": "B", "pass": False, "trial": 0, "task": {"category": "policy"}},
    ]
    out = agent.per_task_type_stats(trajs)
    assert set(out) == {"straightforward", "policy"}
    assert out["straightforward"]["pass_at_k"] == 1.0
    assert out["policy"]["pass_at_k"] == 0.0


def test_trajectory_stats_counts_tools_and_errors():
    trajs = [
        {"steps_detail": [{"tool": "x", "error": True}, {"tool": "y", "error": False}],
         "used_tools": ["x", "y"], "pass": True,
         "grade": {"checks": [{"name": "no_forbidden_tools", "pass": True}]}},
        {"steps_detail": [{"tool": "x", "error": False}],
         "used_tools": ["x"], "pass": False,
         "grade": {"checks": [{"name": "no_forbidden_tools", "pass": False}]}},
    ]
    s = agent.trajectory_stats(trajs)
    assert s["n_episodes"] == 2
    assert s["mean_steps"] == 1.5
    assert s["tool_call_rate"] == 1.5
    assert s["tool_error_rate"] == round(1 / 3, 4)
    assert s["policy_violation_rate"] == 0.5
    assert s["pass_rate"] == 0.5


class StubJSON:
    """A stub for `llm.chat_json` used by the judge and sim user: returns a
    fixed pydantic-validated shape per call index."""

    def __init__(self, outputs):
        self.outputs = list(outputs)
        self.calls = 0

    def chat_json(self, messages, schema, **kwargs):
        out = self.outputs[min(self.calls, len(self.outputs) - 1)]
        self.calls += 1
        return schema.model_validate(out) if not isinstance(out, dict) else out


def test_judge_transcript_parses_pass_and_fail():
    llm_ok = StubJSON([{"verdict": "PASS", "note": "good"}])
    r = agent.judge_transcript(
        {"task_id": "A", "task": {"id": "A", "customer_email": "e@x.com", "user_message": "cancel"},
         "steps_detail": [{"tool": "cancel_order", "args": {"order_id": "O101"},
                           "result_digest": {"ok": True}}],
         "final_reply": "cancelled"},
        llm_ok,
    )
    assert r == {"pass": True, "critique": "good"}
    assert llm_ok.calls == 1

    llm_bad = StubJSON([{"verdict": "FAIL", "note": "missing escalate"}])
    r2 = agent.judge_transcript({"task_id": "A", "task": {"id": "A", "user_message": "x"},
                                 "steps_detail": [], "final_reply": "no"}, llm_bad)
    assert r2 == {"pass": False, "critique": "missing escalate"}


def test_judge_transcript_handles_non_json_verdict():
    """A judge that returns the schema but with a non-boolean verdict should
    still produce a pass flag (False when the string does not start with PASS)."""
    llm = StubJSON([{"verdict": "nope", "note": "ambiguous"}])
    r = agent.judge_transcript({"task_id": "A", "task": {}, "steps_detail": [], "final_reply": "no"}, llm)
    assert r["pass"] is False


def test_simulate_episode_replies_then_returns_grading():
    """Simulate an agent that immediately replies and a sim user that
    declares done. The episode should end, be graded, and expose
    `mode == "simulate"` and `user_turns_used == 0` because the agent
    replied on the first turn."""
    scripts = [
        # One episode step that ends in reply:
        {"role": "assistant", "tool_calls": [
            {"name": "lookup_order", "arguments": {"order_id": "O101"}},
            {"name": "cancel_order", "arguments": {"order_id": "O101"}},
            {"name": "reply", "arguments": {"text": "Cancelled O101, refund on the way."}},
        ]},
    ]
    sim = StubJSON([{"done": True, "message": ""}])  # not used: episode ends on reply

    class MultiLLM:
        def __init__(self):
            self._tools = StubLLM(scripts)
            self.json = sim

        def chat_with_tools(self, *a, **kw):
            return self._tools.chat_with_tools(*a, **kw)

        def chat_json(self, *a, **kw):
            return self.json.chat_json(*a, **kw)

    task = load_tasks()[0]  # t01
    traj = agent.simulate_episode(task, MultiLLM(), project_root=_real_project_root())
    assert traj["mode"] == "simulate"
    assert traj["ended_with_reply"] is True
    assert traj["finished_reason"] == "reply"
    assert traj["user_turns_used"] == 0
    assert traj["grade"]["pass"] is True
    o = traj["state_after"]["orders"]["O101"]
    assert o["status"] == "cancelled" and o["refund_total"] == 120.0


def test_simulate_episode_multi_turn_question_then_answer():
    """Agent asks a question (no reply on turn 1), sim user provides the
    missing id (turn 2 question answered), agent completes (turn 3)."""
    scripts = [
        # turn 1: agent asks for the order id
        {"role": "assistant", "content": "What is the order id?"},
        # turn 2: agent acts using the id the customer provided
        {"role": "assistant", "tool_calls": [
            {"name": "cancel_order", "arguments": {"order_id": "O101"}},
            {"name": "reply", "arguments": {"text": "cancelled O101 for you."}},
        ]},
    ]

    from pydantic import BaseModel, Field

    class MultiLLM:
        def __init__(self):
            self._tools = StubLLM(scripts)
            self.json = StubJSON([{"done": False, "message": "it was O101"},
                                  {"done": True, "message": ""}])

        def chat_with_tools(self, *a, **kw):
            return self._tools.chat_with_tools(*a, **kw)

        def chat_json(self, *a, **kw):
            return self.json.chat_json(*a, **kw)

    task = load_tasks()[0]
    traj = agent.simulate_episode(task, MultiLLM(), project_root=_real_project_root())
    assert traj["mode"] == "simulate"
    assert traj["ended_with_reply"] is True
    assert traj["finished_reason"] == "reply"
    assert traj["user_turns_used"] == 1
    g = traj["grade"]["pass"]
    assert g is True