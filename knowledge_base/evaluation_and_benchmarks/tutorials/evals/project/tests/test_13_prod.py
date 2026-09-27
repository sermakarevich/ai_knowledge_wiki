"""Chapter 13a offline tests — the Langfuse self-host wiring.

Hermetic: no Langfuse server, no Ollama. The compose file / .env.template /
justfile are checked as text; `tracing.observe` is exercised in its no-op
(no keys) and live (keys + no server) modes; the prod data adapters
(`_verdicts`, `_checks`, the evaluator) are checked against the committed
ch-04/ch-05 prediction files. `require_live` must refuse to run without the
keys. The one `slow` test runs the whole flow against a live stack.

Run with: cd project && uv run pytest tests/ -q -m "not slow"
"""

from __future__ import annotations

import importlib
import json
from pathlib import Path

import pytest
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
COMPOSE = PROJECT_ROOT / "docker-compose.yml"

from evals_tutorial import tracing  # noqa: E402
from evals_tutorial import prod  # noqa: E402
from evals_tutorial import helpdesk  # noqa: E402
from evals_tutorial.tracing import observe  # noqa: E402
import evals_tutorial.config as cfg  # noqa: E402

LANGFUSE_RECIPE = {"langfuse-up", "langfuse-down", "langfuse-logs"}
PROD_RECIPE = {"prod-trace", "prod-dataset", "prod-experiment", "prod-scores"}


# -- compose file ---------------------------------------------------------------


def _compose() -> dict:
    return yaml.safe_load(COMPOSE.read_text())


def test_compose_service_names_prefixed_evals() -> None:
    c = _compose()
    assert c["services"], "compose must define services"
    for name in c["services"]:
        assert name.startswith("evals-"), f"service {name!r} must start with 'evals-'"
    assert {"evals-langfuse-web", "evals-postgres", "evals-clickhouse", "evals-redis", "evals-minio"} <= set(
        c["services"]
    )


def test_compose_only_ui_port_published_is_3030_to_3000() -> None:
    c = _compose()
    published: list[str] = []
    for name, svc in c["services"].items():
        for port in (svc or {}).get("ports", []) or []:
            left = str(port).split(":")[0]
            published.append(f"{name}:{left}")
    assert published == ["evals-langfuse-web:3030"], (
        f"only the UI on host 3030 may be published, got {published}"
    )
    web = c["services"]["evals-langfuse-web"]
    assert "3030:3000" in [p if ":" in str(p) else "3030:3000" for p in web["ports"]]


def test_compose_profile_langfuse_on_every_service() -> None:
    c = _compose()
    for name, svc in c["services"].items():
        profiles = (svc or {}).get("profiles") or []
        assert "langfuse" in profiles, f"service {name!r} must sit behind profile 'langfuse'"


def test_compose_volumes_prefixed_evals_langfuse() -> None:
    c = _compose()
    for name in c.get("volumes", {}):
        assert name.startswith("evals-langfuse-"), f"volume {name!r} must start with 'evals-langfuse-'"
    assert set(c["volumes"]) >= {
        "evals-langfuse-postgres-data",
        "evals-langfuse-clickhouse-data",
        "evals-langfuse-minio-data",
        "evals-langfuse-redis-data",
    }


def test_compose_langfuse_init_keys_wired() -> None:
    web = _compose()["services"]["evals-langfuse-web"]["environment"]
    for key in (
        "LANGFUSE_INIT_ORG_ID",
        "LANGFUSE_INIT_PROJECT_ID",
        "LANGFUSE_INIT_PROJECT_NAME",
        "LANGFUSE_INIT_PROJECT_PUBLIC_KEY",
        "LANGFUSE_INIT_PROJECT_SECRET_KEY",
        "LANGFUSE_INIT_USER_EMAIL",
    ):
        assert key in web, f"evals-langfuse-web must consume {key}"


# -- .env.template / justfile ------------------------------------------------------


def test_env_template_has_langfuse_keys() -> None:
    text = (PROJECT_ROOT / ".env.template").read_text()
    for key in ("LANGFUSE_HOST", "LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY"):
        assert key in text, f".env.template must document {key}"
    assert "http://localhost:3030" in text


def test_justfile_has_langfuse_and_prod_recipes() -> None:
    text = (PROJECT_ROOT / "justfile").read_text()
    for recipe in LANGFUSE_RECIPE | PROD_RECIPE:
        assert f"\n{recipe}" in "\n" + text or text.startswith(f"{recipe}:"), f"justfile must define '{recipe}'"
    assert "docker compose --profile langfuse up -d" in text
    assert "docker compose --profile langfuse down" in text


# -- tracing wrapper -------------------------------------------------------------


def _fresh(name: str) -> object:
    importlib.reload(name)
    return name


@pytest.fixture()
def no_keys(monkeypatch) -> None:
    monkeypatch.setattr(tracing, "settings", type("S", (), {"langfuse_host": "", "langfuse_public_key": ""}))
    monkeypatch.setattr(tracing, "_LIVE", False)


def test_observe_is_identity_without_keys(no_keys) -> None:
    def fn(x: int) -> int:
        return x * 2

    assert tracing.observe(fn) is fn


def test_observe_wraps_when_keys_present(monkeypatch) -> None:
    monkeypatch.setattr(
        tracing, "settings", type("S", (), {"langfuse_host": "http://localhost:1", "langfuse_public_key": "pk", "langfuse_secret_key": "sk"})
    )
    monkeypatch.setattr(tracing, "_LIVE", True)

    def fn(x: int) -> int:
        return x * 3

    wrapped = tracing.observe(fn)
    assert wrapped is not fn
    assert wrapped(4) == 12


def test_helpdesk_stays_plain_function_without_keys(no_keys) -> None:
    # identity wrapper keeps the callable and its signature usable
    import inspect

    sig = inspect.signature(helpdesk.answer)
    assert "ticket_text" in sig.parameters
    from evals_tutorial.testing import FakeLLM

    reply = helpdesk.answer("I need to return my bike", version="v1", client=FakeLLM())
    assert isinstance(reply.text, str) and reply.text


# -- prod: guards and data adapters ------------------------------------------------


def test_require_live_refuses_without_keys(no_keys) -> None:
    import typer

    with pytest.raises(typer.Exit):
        prod.require_live()


def test_verdicts_and_checks_cover_60_test_tickets() -> None:
    v = prod._verdicts("v1")
    c = prod._checks("v1")
    assert len(v) == 60 and len(c) == 60
    assert set(v) == set(c)
    assert "tkt-003" in v
    assert isinstance(v["tkt-003"]["pred_pass"], bool)
    assert isinstance(c["tkt-003"]["pass"], bool)
    assert set(c["tkt-003"]["checks"]) == {
        "nonempty",
        "max_words_150",
        "mentions_section_name",
        "no_phone_or_email_invented",
        "no_forbidden_promises",
        "mentions_all_answer_point_keywords",
    }


def test_evaluator_emits_two_rows_for_a_known_ticket() -> None:
    evaluators = prod._evaluators_for("v1")
    assert len(evaluators) == 1
    rows = evaluators[0](
        input="ticket text",
        output="answer text",
        expected_output=None,
        metadata={"ticket_id": "tkt-003"},
    )
    by_name = {r["name"]: r for r in rows}
    assert set(by_name) == {"judge_overall_pass", "all_checks_pass"}
    assert by_name["judge_overall_pass"]["value"] == (1.0 if prod._verdicts("v1")["tkt-003"]["pred_pass"] else 0.0)
    assert by_name["all_checks_pass"]["value"] == (1.0 if prod._checks("v1")["tkt-003"]["pass"] else 0.0)


def test_evaluator_without_ticket_id_returns_no_rows() -> None:
    evaluators = prod._evaluators_for("v1")
    assert evaluators[0](input="x", output="y", expected_output=None, metadata={}) == []


def test_push_human_scores_refuses_without_keys(no_keys) -> None:
    import typer

    with pytest.raises(typer.Exit):
        prod.push_human_scores("answer_v1")


def test_prod_cli_declares_the_chapter13a_commands() -> None:
    import typer.main

    names = set(typer.main.get_command(prod.app).commands)
    assert {"trace", "dataset", "experiment", "scores", "ci", "monitor"} <= names


# -- slow: live end-to-end ---------------------------------------------------------


@pytest.mark.slow
def test_live_flow_trace_dataset_experiment_scores() -> None:
    """Run against a live Langfuse: needs `just langfuse-up` + keys in .env."""
    import urllib.request

    import typer

    if not tracing.is_live():
        pytest.skip("LANGFUSE_HOST/LANGFUSE_PUBLIC_KEY not set")
    try:
        urllib.request.urlopen("http://localhost:3030/api/public/health", timeout=3)
    except Exception:
        pytest.skip("Langfuse stack not running (run `just langfuse-up`)")

    try:
        lf = prod.require_live()
        lf.auth_check()
    except typer.Exit:
        pytest.skip("Langfuse not configured")

    rows = prod.replay_traces("answer_v1")
    assert len(rows) == 80 and all(r["trace_id"] for r in rows)

    datasets = prod.upsert_datasets()
    assert {d["dataset"]: d["items"] for d in datasets} == {"helpdesk-test": 60, "helpdesk-dev": 20}

    for version in ("v1", "v2"):
        row = prod.run_experiment(version)
        assert row["items"] == 60 and row["items_traced"] >= 1 and row["items_scored"] == 60

    score_row = prod.push_human_scores("answer_v1")
    assert score_row["pushed"] == 80 and score_row["skipped"] == 0


# -- chapter 13b: CI gate decision ----------------------------------------------


def test_gate_pass_when_delta_neutral_and_checks_improve() -> None:
    # v1 vs v1: delta=0, no regression, checks_drop=0 → pass
    a = [True, False, True, True, False, True] * 10
    b = [True, False, True, True, False, True] * 10
    dec = prod.gate_decision(a, b, checks_drop=-0.05)
    assert dec["pass"] is True, dec["reasons"]
    assert dec["delta"] == 0.0
    assert dec["delta_ci"] == [0.0, 0.0]  # identical pairs → no spread


def test_gate_pass_when_delta_improves() -> None:
    a = [True] * 20
    b = [True] * 18 + [False, False]
    dec = prod.gate_decision(a, b, checks_drop=0.0)
    assert dec["pass"] is True, dec["reasons"]
    assert dec["delta"] > 0
    assert dec["delta_ci"][1] > 0  # CI upper bound positive
    assert dec["delta_ci"][0] >= 0  # CI lower bound never negative


def test_gate_fails_when_ci_excludes_improvement() -> None:
    # a is worse on every ticket → delta_ci_upper < 0 → fail
    a = [False] * 20
    b = [True] * 20
    dec = prod.gate_decision(a, b, checks_drop=0.0)
    assert dec["pass"] is False
    assert dec["delta"] == -1.0
    assert any("pass-rate delta CI upper" in r for r in dec["reasons"])


def test_gate_fails_when_checks_drop_too_large() -> None:
    a = [True] * 20
    b = [True] * 20  # identical, so CI is [0,0] and no delta rule fires
    dec = prod.gate_decision(a, b, checks_drop=0.15)
    assert dec["pass"] is False
    assert any("all_checks_pass" in r for r in dec["reasons"])


def test_gate_rejects_mismatched_lengths() -> None:
    with pytest.raises(ValueError):
        prod.gate_decision([True, False], [True, False, True], checks_drop=0.0)


# -- chapter 13b: day plan (determinism, coverage, size) -------------------------


def _fake_traces(n: int) -> list[dict]:
    return [{"ticket_id": f"tkt-{i:03d}", "output": "x " * 200, "retrieved": []} for i in range(n)]


def test_plan_days_is_deterministic() -> None:
    traces = _fake_traces(80)
    p1 = prod.plan_days(traces, sample=0.2, days=7, seed=42)
    p2 = prod.plan_days(traces, sample=0.2, days=7, seed=42)
    p3 = prod.plan_days(traces, sample=0.2, days=7, seed=43)
    assert [t["ticket_id"] for d in p1 for t in d] == [t["ticket_id"] for d in p2 for t in d]
    assert [t["ticket_id"] for d in p1 for t in d] != [t["ticket_id"] for d in p3 for t in d]


def test_plan_days_samples_at_requested_fraction() -> None:
    traces = _fake_traces(80)
    plan = prod.plan_days(traces, sample=0.2, days=7)
    k_expected = max(1, int(round(80 * 0.2)))  # 16
    for day in plan:
        assert len(day) == k_expected


def test_plan_days_covers_every_trace_over_7_days() -> None:
    traces = _fake_traces(80)
    plan = prod.plan_days(traces, sample=0.2, days=7)
    covered = {t["ticket_id"] for d in plan for t in d}
    assert covered == {t["ticket_id"] for t in traces}


def test_plan_days_works_for_any_pool_size() -> None:
    for n in (10, 20, 50, 100):
        traces = _fake_traces(n)
        plan = prod.plan_days(traces, sample=0.2, days=7)
        assert len(plan) == 7
        # each day scores max(1, round(n*0.2)) items
        k_expected = max(1, int(round(n * 0.2)))
        for day in plan:
            assert len(day) == k_expected


# -- chapter 13b: trace-level pass rule (word cap) -------------------------------


def test_trace_pass_rule_word_cap() -> None:
    # short output passes when hhem score is low
    assert prod._trace_pass({"output": "hi"}, hhem_score=0.1, threshold=0.3) is True
    # long output fails regardless of hhem score
    assert prod._trace_pass({"output": "x " * 500}, hhem_score=0.0, threshold=0.3) is False
    # hhem score above threshold fails
    assert prod._trace_pass({"output": "hi"}, hhem_score=0.9, threshold=0.3) is False
