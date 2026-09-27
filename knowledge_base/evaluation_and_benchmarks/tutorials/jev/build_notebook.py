"""Generate jev_tutorial.ipynb. Run `just build` (or `uv run python build_notebook.py`)."""

from __future__ import annotations

import nbformat as nbf

cells: list = []


def md(text: str) -> None:
    cells.append(nbf.v4.new_markdown_cell(text.strip("\n")))


def code(text: str) -> None:
    cells.append(nbf.v4.new_code_cell(text.strip("\n")))


# --------------------------------------------------------------------------- 0
md(r"""
# Jev (TypeSafe) from Python — basics, patterns, and a real code review of `fleet`

**Jev** is the model behind [TypeSafe](https://docs.typesafe.ai/introduction). It is a *System One* model: it does **not** write text.
You send it some **state** (the material to judge: a message, a JSON object, a source file) plus one or more **typed questions**,
and it returns **numbers your code can use directly**:

| Question type | You ask | You get back |
|---|---|---|
| `Choice` | "Pick one of these options" | `choice`, `probabilities` (per option), `confidence` |
| `Score` | "Rate this on my ordered rubric" | `score` (can land between levels), `probabilities`, `confidence` |
| `Noul` | "Is this statement true?" | `noul` — a number from 0 (no) to 1 (yes) |

Because there is no text generation, calls are fast, cheap (fractions of a cent per million input tokens), and all questions
in one request are evaluated **in parallel** against the same state.

Abbreviations used below: **API** = Application Programming Interface (the HTTP service); **SDK** = Software Development Kit
(the `typesafe_sdk` Python package); **JSON** = JavaScript Object Notation (plain data format); **ADR** = Architecture
Decision Record (a short document explaining a design decision).

Notebook map:
1. Setup
2. Basic examples (straight from the docs)
3. Patterns: confidence routing, composite scoring, speculative fan-out
4. **Advanced:** ask Jev "how should I improve `~/git/fleet`?" — architecture scorecard, ranked improvement backlog, per-file code-smell scan
5. Cost and takeaways
""")

# --------------------------------------------------------------------------- 1
md(r"""
## 1. Setup

The SDK reads `TYPESAFE_API_KEY` from the environment and calls the `jev-latest` model by default.
Other environment variables: `TYPESAFE_BASE_URL`, `TYPESAFE_DEFAULT_MODEL`, `TYPESAFE_LOG_LEVEL`.
""")
code(r"""
import asyncio
import json
import os
from pathlib import Path

import pandas as pd
from typesafe_sdk import (
    AsyncTypeSafeClient,
    Choice,
    Noul,
    RetryPolicy,
    Score,
    TypeSafeAPIError,
    TypeSafeClient,
)

assert os.environ.get("TYPESAFE_API_KEY"), "Set TYPESAFE_API_KEY in your shell before starting Jupyter"

pd.set_option("display.max_colwidth", 80)
pd.set_option("display.width", 160)

# One shared usage counter so we can see what the whole notebook cost at the end.
USAGE = {"input_tokens": 0, "output_tokens": 0, "requests": 0}


def track(response):
    USAGE["input_tokens"] += response.usage.input_tokens
    USAGE["output_tokens"] += response.usage.output_tokens
    USAGE["requests"] += 1
    return response


client = TypeSafeClient(retry=RetryPolicy(max_retries=4, backoff_max=2.0, timeout=60.0))

for m in client.models.list().models:
    print(f"{m.name:12s} {m.release_date[:10]}  {m.description}")
""")

# --------------------------------------------------------------------------- 2
md(r"""
## 2. Basic examples

### 2.1 The quick-start example: one support ticket, three questions

This is the example from the [Quick start](https://docs.typesafe.ai/introduction/quickstart) page. One call, three different question types.
""")
code(r"""
ticket = (
    "Hi, I've been trying to connect my Stripe account for 3 days and it keeps failing. "
    "I'm losing sales. Please help ASAP."
)

response = track(
    client.system_one(
        state=ticket,
        questions={
            "department": Choice(
                instructions="Which team should handle this",
                criteria={
                    "billing": "Payment or subscription issues",
                    "technical": "Bugs or integration problems",
                    "sales": "Pricing or account questions",
                },
            ),
            "frustration": Score(
                instructions="How frustrated the customer appears",
                criteria=[
                    "Calm, just stating facts",
                    "Frustrated but civil",
                    "Very angry, strong language",
                ],
            ),
            "is_urgent": Noul(
                instructions="The message conveys urgency or time-sensitivity",
            ),
        },
    )
)

print(response.answers["department"].choice)  # e.g. "technical"
print(response.answers["frustration"].score)  # e.g. 1.03  -> between "frustrated" (1) and "angry" (2)
print(response.answers["is_urgent"].noul)  # e.g. 0.99
""")

md(r"""
### 2.2 What is inside an answer

Every `Choice` and `Score` answer carries the full **probability distribution** and a single **confidence** number (0–1) computed from
the shape of that distribution: concentrated = confident, spread out = unsure. `Noul` answers are just the 0–1 number.
`response.choices`, `response.scores`, `response.nouls` are typed views of `response.answers`.
""")
code(r"""
dept = response.choices["department"]
frus = response.scores["frustration"]

print("choice:      ", dept.choice)
print("probabilities", {k: round(v, 3) for k, v in dept.probabilities.items()})
print("confidence:  ", round(dept.confidence, 3))
print()
print("score:       ", round(frus.score, 3))
print("legend:      ", frus.legend)  # which level means what
print("probabilities", {k: round(v, 3) for k, v in frus.probabilities.items()})
print("confidence:  ", round(frus.confidence, 3))
print()
print("model:       ", response.model)
print("request_id:  ", response.request_id)
print("usage:       ", response.usage)
""")

md(r"""
### 2.3 State does not have to be a string

State can be a **dict** (JSON object) or a **list**. The docs recommend a dict for most real requests so every part has a name.
This example (from the [State](https://docs.typesafe.ai/concepts/state) page) puts a conversation, an order and a policy into one state and asks
questions that need to *compare* those parts.
""")
code(r"""
state = {
    "ticket": {
        "subject": "Duplicate charge",
        "messages": [
            {"from": "customer", "text": "I was charged twice for order A-104. Please refund the duplicate."},
            {"from": "support", "text": "We are checking the charges."},
        ],
    },
    "order": {
        "id": "A-104",
        "charges": [
            {"amount_usd": 49, "status": "captured"},
            {"amount_usd": 49, "status": "captured"},
        ],
    },
    "refund_policy": "Duplicate charges are eligible for a refund.",
}

r = track(
    client.system_one(
        state,
        {
            "refund_requested": Noul(instructions="Did the customer ask for a refund?"),
            "duplicate_confirmed": Noul(
                instructions="Do the order records show the same amount captured more than once?"
            ),
            "policy_allows_refund": Noul(instructions="Does the refund policy cover this situation?"),
            "next_step": Choice(
                instructions="What should support do next?",
                criteria={
                    "refund": "Issue the refund now",
                    "investigate": "Look deeper before deciding",
                    "decline": "Explain that no refund is due",
                },
            ),
        },
    )
)
for name, ans in r.nouls.items():
    print(f"{name:22s} {ans.noul:.3f}")
print("next_step:", r.choices["next_step"].choice, {k: round(v, 3) for k, v in r.choices["next_step"].probabilities.items()})
""")

md(r"""
### 2.4 Structured instructions and criteria

Instructions and option descriptions can be JSON objects too, not just strings. This is useful to spell out boundaries:
*what* an option covers, what it is *not for*, and *examples*. (From [Advanced: structure](https://docs.typesafe.ai/primitives/advanced).)
""")
code(r"""
r = track(
    client.system_one(
        "I ordered the standing desk two weeks ago and tracking still says label created. Was I even charged?",
        {
            "department": Choice(
                instructions={
                    "question": "Which team should handle this message?",
                    "focus": "Classify the customer's primary request, not every topic mentioned.",
                },
                criteria={
                    "billing": {
                        "what": "Charges, invoices, refunds, or subscriptions",
                        "not_for": "Order tracking or account access",
                        "examples": ["I was charged twice", "Where is my refund?"],
                    },
                    "shipping": {
                        "what": "Where an order is and when it arrives",
                        "not_for": "Payment questions",
                        "examples": ["Tracking has not updated", "Package is late"],
                    },
                    "account": {
                        "what": "Login, password, profile changes",
                        "examples": ["I cannot log in"],
                    },
                },
            )
        },
    )
)
print(r.choices["department"].choice, {k: round(v, 3) for k, v in r.choices["department"].probabilities.items()})
""")

md(r"""
### 2.5 Raw dictionaries, `extra_body`, retries, errors, logging

- A question can be a plain dict with a `"type"` key — handy for fields the SDK does not model yet.
- `extra_body` sends extra request fields.
- `RetryPolicy` can be set per client or per call. `TypeSafeAPIError` carries `status` and `request_id`.
- The SDK logs to the `typesafe_sdk` logger (`TYPESAFE_LOG_LEVEL=info` gives one line per request).
""")
code(r"""
import logging

logging.getLogger("typesafe_sdk").setLevel(logging.WARNING)

r = track(
    client.system_one(
        "I was charged twice.",
        {"billing": {"type": "noul", "instructions": "About billing?"}},  # raw dict question
        retry=RetryPolicy(max_retries=2, backoff_max=0.5, timeout=30.0),  # per-call override
    )
)
print("billing noul:", r.nouls["billing"].noul)

# Error handling: an obviously wrong model name triggers an API error.
try:
    client.system_one("hello", {"x": Noul(instructions="Is this a greeting?")}, model="does-not-exist")
except TypeSafeAPIError as error:
    print("API error ->", type(error).__name__, error.status, error.request_id)
""")

md(r"""
### 2.6 The async client

`AsyncTypeSafeClient` has the same interface with `await`. Jupyter lets you `await` at the top level of a cell.
We will use this later to scan many files concurrently.
""")
code(r"""
async with AsyncTypeSafeClient(retry=RetryPolicy(max_retries=4, backoff_max=2.0, timeout=60.0)) as aclient:
    messages = [
        "Where is my order?",
        "Cancel my subscription immediately, this is a scam.",
        "Thanks, the fix worked!",
    ]
    tasks = [
        aclient.system_one(
            m,
            {
                "tone": Choice(instructions="What is the tone?", criteria={"calm": None, "frustrated": None, "angry": None}),
                "churn_risk": Noul(instructions="Is the customer likely to leave?"),
            },
        )
        for m in messages
    ]
    results = [track(r) for r in await asyncio.gather(*tasks)]

for m, r in zip(messages, results):
    print(f"{r.choices['tone'].choice:10s} churn={r.nouls['churn_risk'].noul:.2f}  | {m}")
""")

# --------------------------------------------------------------------------- 3
md(r"""
## 3. Patterns

### 3.1 Confidence-gated routing

Confidence lets the model say "I am not sure". The standard pattern: **below a floor → send to a human**; above it, the threshold for
acting automatically **scales with the stakes** of the action. (From [Confidence](https://docs.typesafe.ai/confidence).)
""")
code(r"""
def route(user_message: str) -> str:
    r = track(
        client.system_one(
            user_message,
            {
                "action": Choice(
                    instructions="What is the user trying to do?",
                    criteria={
                        "check_balance": "View account balance",
                        "approve_transfer": "Approve the pending withdrawal request",
                        "support": "Get help with an issue",
                    },
                )
            },
        )
    )
    action = r.choices["action"]
    c = action.confidence
    if c < 0.5:
        decision = "ROUTE TO HUMAN (model unsure)"
    elif action.choice == "check_balance":
        decision = "show balance (low stakes, act)"  # wrong screen is recoverable
    elif action.choice == "approve_transfer":
        decision = "execute transfer" if c > 0.9 else "ASK USER TO CONFIRM transfer"  # high stakes
    else:
        decision = "open support flow"
    return f"{action.choice:17s} conf={c:.2f} -> {decision}"


for msg in [
    "How much money do I have?",
    "Yes go ahead and approve the pending withdrawal.",
    "approve... actually wait, what is my balance first?",
    "The app crashed twice today.",
]:
    print(route(msg), "|", msg)
""")

md(r"""
### 3.2 Composite scoring

A judgment that depends on several things is best split into **one Score per thing**, then combined **in your code with weights you control**.
Changing priorities means changing numbers, not rewriting a prompt. (From [Composite scoring](https://docs.typesafe.ai/patterns/composite-scoring).)
""")
code(r"""
candidates = {
    "A": "8 years Python, built and ran a 6-person platform team, designed the event pipeline that handles 2B events/day.",
    "B": "3 years Python and Go, strong individual contributor, deep in distributed systems, no management experience.",
    "C": "12 years across Java/Python/JS, managed 20 engineers, mostly hands-off for the last 5 years.",
}
levels = ["none", "basic", "solid", "strong", "expert"]  # 0..4

rows = []
for name, cv in candidates.items():
    r = track(
        client.system_one(
            {"cv": cv},
            {
                "python_depth": Score(instructions="Depth of hands-on Python skill", criteria=levels),
                "team_leadership": Score(instructions="Experience leading people", criteria=levels),
                "system_design": Score(instructions="Experience designing large systems", criteria=levels),
                "generalist": Score(instructions="Breadth across languages and domains", criteria=levels),
            },
        )
    )
    s = {k: v.score / 4 for k, v in r.scores.items()}  # normalise to 0..1
    rows.append(
        {
            "candidate": name,
            **{k: round(v, 2) for k, v in s.items()},
            "senior_ic": round(0.40 * s["python_depth"] + 0.10 * s["team_leadership"] + 0.40 * s["system_design"] + 0.10 * s["generalist"], 2),
            "eng_manager": round(0.15 * s["python_depth"] + 0.40 * s["team_leadership"] + 0.20 * s["system_design"] + 0.25 * s["generalist"], 2),
        }
    )
pd.DataFrame(rows).set_index("candidate")
""")

md(r"""
### 3.3 Speculative fan-out

Extra questions in the same request are almost free (they run in parallel, and the state is only sent once).
So ask **every question you might need** up front, then let your code pick which answers matter.
(From [Speculative fan-out](https://docs.typesafe.ai/patterns/fan-out).)
""")
code(r"""
def triage(ticket_text: str) -> str:
    r = track(
        client.system_one(
            ticket_text,
            {
                "category": Choice(
                    instructions="What kind of ticket is this?",
                    criteria={"bug_report": None, "billing": None, "feature_request": None},
                ),
                # Speculative: only used if category == bug_report
                "bug_severity": Score(instructions="How severe is the bug?", criteria=["cosmetic", "annoying", "blocking", "data loss"]),
                "has_reproducible_steps": Noul(instructions="Does the ticket give steps to reproduce?"),
                # Speculative: only used if category == billing
                "refund_requested": Noul(instructions="Is a refund requested?"),
                # Always useful
                "frustration": Score(instructions="How frustrated is the writer?", criteria=["calm", "frustrated", "angry"]),
            },
        )
    )
    a = r.answers
    cat = a["category"].choice
    if cat == "bug_report":
        out = "escalate to engineering" if (a["bug_severity"].score > 1.5 and a["has_reproducible_steps"].noul > 0.6) else "bug backlog"
    elif cat == "billing":
        out = "billing team, refund likely" if a["refund_requested"].noul > 0.7 else "billing team"
    else:
        out = "log feature request"
    if a["frustration"].score > 1.5:
        out += " + PRIORITY RESPONSE"
    return f"{cat:16s} -> {out}"


for t in [
    "Every time I click export the app crashes. Steps: open report, click Export, choose CSV. Lost a day of work!!!",
    "You billed me for the Pro plan but I downgraded last month. I want my money back.",
    "Would be nice to have dark mode.",
]:
    print(triage(t), "|", t[:60])
""")

# --------------------------------------------------------------------------- 4
md(r"""
## 4. Advanced: "Jev, how should I improve `fleet`?"

`~/git/fleet` is a Python supervisor that runs coding agents in parallel from a shared **beads** task queue.

**Important framing.** Jev cannot *write* advice — it only judges. So the question "how should I improve fleet?" has to be
turned into typed questions where Jev is the **judge** and you (or a text-generating LLM) supply the **candidates**:

1. **Scorecard** — feed the project docs as state, ask Scores on quality dimensions and Nouls on specific risks.
2. **Which area first?** — a `Choice` over improvement areas; the probabilities *are* the ranked answer.
3. **Ranked backlog** — you list concrete improvement ideas; Jev scores each on impact / effort / risk / fit; your code combines them.
4. **Per-file smell scan** — send every source file, ask about the project's *own* ADR rules (e.g. "no function over ~40 lines"), rank files.

The request budget is about **32,000 tokens (~150,000 characters)** shared by state and questions, so we trim inputs to fit.
Results are cached in `fleet_cache/` so re-running the notebook does not re-call the API.
""")
code(r"""
FLEET = Path("~/git/fleet").expanduser()
assert FLEET.exists(), f"fleet repo not found at {FLEET}"
CACHE = Path("fleet_cache")
CACHE.mkdir(exist_ok=True)
MAX_STATE_CHARS = 120_000  # stay under the ~150k-character request budget with room for questions


def fit(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[:limit] + "\n...[truncated]..."


def read(rel: str) -> str:
    return (FLEET / rel).read_text(errors="replace")


def answers_to_dict(response) -> dict:
    out = {}
    for name, ans in response.answers.items():
        if hasattr(ans, "choice"):
            out[name] = {"type": "choice", "choice": ans.choice, "confidence": ans.confidence, "probabilities": dict(ans.probabilities)}
        elif hasattr(ans, "score"):
            out[name] = {"type": "score", "score": ans.score, "confidence": ans.confidence, "probabilities": dict(ans.probabilities)}
        else:
            out[name] = {"type": "noul", "noul": ans.noul}
    return out


def cached(key: str, call):
    # call() must return a SystemOneResponse; we store a plain-JSON version of its answers.
    path = CACHE / f"{key}.json"
    if path.exists():
        return json.loads(path.read_text())
    result = answers_to_dict(track(call()))
    path.write_text(json.dumps(result, indent=1))
    return result


# The "project brief": what the project says about itself. ADRs explain *why* it is built this way.
docs_state = {
    "readme": read("README.md"),
    "overview": read("docs/OVERVIEW.md"),
    "architecture": fit(read("docs/ARCHITECTURE.md"), 40_000),
    "adr_index": read("docs/adr/README.md"),
    "adr_titles": [p.name for p in sorted((FLEET / "docs/adr").glob("0*.md"))],
    "package_sizes_loc": {
        d.name: sum(len(f.read_text(errors="replace").splitlines()) for f in d.rglob("*.py"))
        for d in sorted((FLEET / "src/fleet").iterdir())
        if d.is_dir() and d.name != "__pycache__"
    },
}
print("state size:", len(json.dumps(docs_state)), "characters")
""")

md(r"""
### 4.1 Architecture scorecard

Scores are 0–4 on the same rubric for every dimension, so they are comparable. The `confidence` column tells you where Jev found the
docs ambiguous — a low confidence is itself a finding ("the docs do not make this clear").
""")
code(r"""
rubric = [
    "absent or broken",
    "weak, obvious gaps",
    "adequate for a single developer",
    "good, would satisfy a small team",
    "excellent, production grade",
]
dimensions = {
    "docs_clarity": "How clear and complete is the documentation for a newcomer?",
    "modularity": "How well separated are concerns (layers, one owner per file, registries)?",
    "failure_handling": "How well does the system handle stale/killed/blocked work and restarts?",
    "observability": "How easy is it to see what the system is doing (logs, events, UI, metrics)?",
    "testability": "How easy would it be to test the core logic in isolation?",
    "extensibility": "How easy is it to add a new coder, worker kind, or event source?",
    "security_posture": "How well are secrets, remote access and the web UI protected?",
    "scalability": "How well would it scale beyond one machine and a handful of concurrent agents?",
    "cost_control": "How well does it track and cap spending on model/API usage?",
}
risks = {
    "single_machine_limit": "The design is limited to a single supervisor on a single machine.",
    "hard_bd_dependency": "The system depends on an external command-line tool (bd/beads) for its core queue.",
    "no_ui_auth": "The web UI has no authentication described.",
    "big_files_present": "Some modules are much larger than the project's own clean-code rules allow.",
    "docs_match_code": "The documentation claims to be generated from and checked against the real code.",
}

scorecard = cached(
    "scorecard",
    lambda: client.system_one(
        docs_state,
        {
            **{k: Score(instructions=v, criteria=rubric) for k, v in dimensions.items()},
            **{k: Noul(instructions=v) for k, v in risks.items()},
        },
    ),
)

scores = pd.DataFrame(
    [{"dimension": k, "score_0_4": round(v["score"], 2), "confidence": round(v["confidence"], 2)} for k, v in scorecard.items() if v["type"] == "score"]
).sort_values("score_0_4").set_index("dimension")
nouls = pd.DataFrame(
    [{"statement": k, "p_true": round(v["noul"], 2)} for k, v in scorecard.items() if v["type"] == "noul"]
).set_index("statement")
display(scores)
display(nouls)
""")

md(r"""
### 4.2 "Which area should I improve first?" — one Choice

The probabilities are the ranking. Low confidence means several areas are close — look at the distribution, not just the top pick.
""")
code(r"""
areas = {
    "multi_machine": "Let several supervisors on different machines share one queue safely.",
    "cost_tracking": "Track tokens and money per task/attempt, with budget caps and reports.",
    "quality_gates": "Make automated validation (tests, lint, review) a mandatory step before a task closes.",
    "smarter_retries": "Better triage of blocked/stalled tasks, including automatic low-risk fixes.",
    "model_routing": "Choose coder and model per task automatically based on predicted difficulty and cost.",
    "codebase_hygiene": "Split oversized modules and enforce the project's own clean-code rules.",
    "ui_security": "Authentication and safe remote access for the web UI and ask-human inbox.",
    "shared_memory": "Persistent project notes shared across tasks so agents stop re-discovering the codebase.",
    "evaluation": "Replay past tasks against new prompts/coders and compare outcomes (an eval harness).",
}
first = cached(
    "first_area",
    lambda: client.system_one(
        docs_state,
        {
            "first": Choice(
                instructions={
                    "question": "Given the current state of this project, which single improvement area would deliver the most value next?",
                    "focus": "Judge from what the docs say exists today and what they admit is missing or fragile.",
                },
                criteria=areas,
            )
        },
    ),
)["first"]
print("top pick:", first["choice"], " confidence:", round(first["confidence"], 2))
pd.Series(first["probabilities"]).sort_values(ascending=False).round(3).to_frame("probability")
""")

md(r"""
### 4.3 Ranked improvement backlog

Here **you** write the candidates (or ask a text LLM such as Claude to brainstorm them). Jev scores each one on four independent
axes against the project brief; the priority formula is plain code with weights you can tune:

`priority = 0.45·impact + 0.25·(1 − effort) + 0.15·(1 − risk) + 0.15·fits_philosophy`

Each candidate is its own request (the state = brief + candidate), run concurrently with the async client.
""")
code(r"""
ideas = [
    "Run several supervisors on different machines against one shared beads queue, using leases so two machines never claim the same task.",
    "Record tokens and estimated cost per attempt in attempts.jsonl and show per-task/per-day spend in the web UI, with a hard daily budget cap.",
    "Make the post-merge validation step mandatory by default: run the project's tests and linter before an isolated task's branch is merged and the bead closed.",
    "Extend the blocked-task investigator so that for low-risk root causes (e.g. missing dependency, flaky test) it opens a fix task automatically instead of only writing a report.",
    "Add a model-routing step that predicts task difficulty from the bead title/description and picks a cheap local model for easy tasks and a frontier model for hard ones.",
    "Split serve/api/models.py (~1000 lines) and cli/render.py (~800 lines) into per-concept modules to satisfy the project's own ~40-line-function rule.",
    "Add authentication (token or OAuth) to the web UI and the ask_human inbox so the dashboard can be exposed beyond localhost.",
    "Keep a per-repository NOTES.md that every worker reads at start and appends to at the end, so agents stop rediscovering the codebase on each attempt.",
    "Build an evaluation harness that replays a set of historical tasks with a new prompt template or coder and reports success rate, cost and duration side by side.",
    "Replace the bd command-line subprocess calls with a direct store adapter (SQLite/Dolt) so the queue works even when the bd binary is missing or its output format changes.",
    "Add a Slack integration mirroring the Telegram one (notifications, inbound tasks, answering blocked questions from chat).",
    "Publish fleet to PyPI with a versioned changelog and a plugin API for third-party coders.",
]
brief = {"readme": docs_state["readme"], "overview": fit(docs_state["overview"], 12_000)}
four = ["none", "small", "moderate", "large", "very large"]


async def judge_ideas():
    async with AsyncTypeSafeClient(retry=RetryPolicy(max_retries=5, backoff_max=4.0, timeout=90.0)) as ac:

        async def one(i, idea):
            key = f"idea_{i:02d}"
            path = CACHE / f"{key}.json"
            if path.exists():
                return json.loads(path.read_text())
            r = track(
                await ac.system_one(
                    {"project": brief, "proposed_improvement": idea},
                    {
                        "impact": Score(instructions="How much would this improve the project for its users?", criteria=four),
                        "effort": Score(instructions="How much engineering work would it take?", criteria=four),
                        "risk": Score(instructions="How likely is it to destabilise existing behaviour?", criteria=four),
                        "fits_philosophy": Noul(instructions="Is this consistent with the project's stated design rules and goals?"),
                        "already_exists": Noul(instructions="Do the docs say this capability already exists in some form?"),
                    },
                )
            )
            d = answers_to_dict(r)
            path.write_text(json.dumps(d, indent=1))
            return d

        return await asyncio.gather(*(one(i, idea) for i, idea in enumerate(ideas)))


judged = await judge_ideas()

rows = []
for idea, j in zip(ideas, judged):
    impact, effort, risk = (j[k]["score"] / 4 for k in ("impact", "effort", "risk"))
    fits, exists = j["fits_philosophy"]["noul"], j["already_exists"]["noul"]
    rows.append(
        {
            "idea": idea[:90] + ("..." if len(idea) > 90 else ""),
            "impact": round(impact, 2),
            "effort": round(effort, 2),
            "risk": round(risk, 2),
            "fits": round(fits, 2),
            "exists": round(exists, 2),
            "priority": round(0.45 * impact + 0.25 * (1 - effort) + 0.15 * (1 - risk) + 0.15 * fits, 3),
        }
    )
backlog = pd.DataFrame(rows).sort_values("priority", ascending=False).reset_index(drop=True)
backlog
""")

md(r"""
### 4.4 Per-file code-smell scan against fleet's own rules

ADR 0006 in fleet says: *no function over ~40 lines, dispatch over kinds as a table not an if-chain, one owner per file*.
We send **every** `.py` file under `src/fleet` as state and ask Jev about those rules plus general readability.
~200 files → ~200 small requests, run with a concurrency limit; the whole scan costs a few cents.
""")
code(r"""
py_files = sorted(p for p in (FLEET / "src/fleet").rglob("*.py") if not ({"__pycache__", "node_modules"} & set(p.parts)) and p.stat().st_size > 0)
print(len(py_files), "files")

file_questions = {
    "refactor_need": Score(
        instructions="How much does this file need refactoring to be clean and easy to maintain?",
        criteria=["none, clean as is", "minor tidy-up", "noticeable refactor needed", "major rewrite needed"],
    ),
    "readability": Score(instructions="How easy is this code to read for a newcomer?", criteria=["hard", "okay", "easy", "exemplary"]),
    "long_function": Noul(instructions="Does the file contain at least one function or method longer than about 40 lines (excluding literal tables)?"),
    "if_chain_dispatch": Noul(instructions="Does the file dispatch over kinds/types with a long if/elif chain instead of a table or registry?"),
    "mixed_abstraction": Noul(instructions="Do functions mix high-level orchestration with low-level details in the same body?"),
    "missing_tests_signal": Noul(instructions="Does the logic look hard to unit-test (heavy I/O, globals, subprocess calls mixed with logic)?"),
    "biggest_issue": Choice(
        instructions="What is the single biggest quality issue in this file?",
        criteria={
            "none": "The file is fine",
            "too_long": "Functions or the module are too long",
            "duplication": "Repeated logic that should be shared",
            "naming": "Unclear or inconsistent names",
            "docs": "Missing or misleading docstrings/comments",
            "error_handling": "Errors swallowed, unclear, or inconsistent",
            "coupling": "Knows too much about other modules",
        },
    ),
}


async def scan_files(concurrency: int = 8):
    sem = asyncio.Semaphore(concurrency)
    async with AsyncTypeSafeClient(retry=RetryPolicy(max_retries=6, backoff_max=5.0, timeout=90.0)) as ac:

        async def one(path: Path):
            rel = str(path.relative_to(FLEET))
            key = "file_" + rel.replace("/", "__")
            cache_path = CACHE / f"{key}.json"
            if cache_path.exists():
                return rel, json.loads(cache_path.read_text())
            code_text = path.read_text(errors="replace")
            async with sem:
                r = track(await ac.system_one({"path": rel, "code": fit(code_text, MAX_STATE_CHARS)}, file_questions))
            d = answers_to_dict(r)
            d["_lines"] = len(code_text.splitlines())
            cache_path.write_text(json.dumps(d, indent=1))
            return rel, d

        return dict(await asyncio.gather(*(one(p) for p in py_files)))


scan = await scan_files()

files_df = pd.DataFrame(
    [
        {
            "file": rel,
            "lines": d["_lines"],
            "refactor_need": round(d["refactor_need"]["score"], 2),
            "readability": round(d["readability"]["score"], 2),
            "p_long_fn": round(d["long_function"]["noul"], 2),
            "p_if_chain": round(d["if_chain_dispatch"]["noul"], 2),
            "p_mixed": round(d["mixed_abstraction"]["noul"], 2),
            "p_hard_to_test": round(d["missing_tests_signal"]["noul"], 2),
            "biggest_issue": d["biggest_issue"]["choice"],
        }
        for rel, d in scan.items()
    ]
).sort_values(["refactor_need", "lines"], ascending=False)

print("Top 15 files by refactor need:")
display(files_df.head(15).reset_index(drop=True))
print("\nBiggest-issue distribution across all files:")
display(files_df["biggest_issue"].value_counts().to_frame("files"))
print("\nAverage refactor need per package:")
display(
    files_df.assign(package=files_df["file"].str.split("/").str[2])
    .groupby("package")[["refactor_need", "readability", "p_long_fn"]]
    .mean()
    .round(2)
    .sort_values("refactor_need", ascending=False)
)
""")

md(r"""
### 4.5 Turning judgments into work

Jev gave you **ranked, numeric** answers; the next step needs a text-generating agent. Two natural hand-offs:

- Feed the top files to Claude Code: `claude -p "Refactor these files to satisfy ADR 0006: ..."`.
- Or make it a fleet task itself, so the whole loop (Jev ranks → coder fixes → tests validate) runs unattended:
""")
code(r"""
top = files_df.head(5)
title = "Refactor the 5 files Jev ranked highest for refactor need"
desc = "Apply ADR 0006 (functions <= ~40 lines, table-driven dispatch). Files and Jev's findings:\n" + "\n".join(
    f"- {r.file} (need={r.refactor_need}, issue={r.biggest_issue}, p_long_fn={r.p_long_fn})" for r in top.itertuples()
)
print(f"cd {FLEET} && fleet bd create --title {title!r} --description {json.dumps(desc)}")
""")

# --------------------------------------------------------------------------- 5
md(r"""
## 5. Cost and takeaways
""")
code(r"""
price_per_m_input = 0.042  # USD per 1M input tokens for jev (from the TypeSafe cookbook, 2026-09) — check the current price page
print(USAGE)
print(f"approx cost of everything this notebook actually sent: ${USAGE['input_tokens'] / 1e6 * price_per_m_input:.4f}")
print("(cached results from fleet_cache/ were not re-sent)")
""")
md(r"""
**Takeaways**

- Jev is a **judge, not a writer**. Ask it to choose, rate, or confirm — never to explain.
- Put everything the judgment needs into a **named dict state**; keep the *questions* separate from the *content*.
- Ask **many questions per request** (fan-out) — they run in parallel and cost almost nothing extra.
- Split complex judgments into **several Scores** and combine them **in code** with explicit weights.
- Use **confidence** to decide when to act automatically and when to ask a human.
- For "how do I improve X?" questions: **you** (or a text LLM) supply candidates and rubrics; Jev ranks them consistently and cheaply,
  and re-running is deterministic enough to track progress over time.
""")

nb = nbf.v4.new_notebook()
nb["cells"] = cells
nb["metadata"] = {
    "kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"},
    "language_info": {"name": "python"},
}
nbf.write(nb, "jev_tutorial.ipynb")
print(f"wrote jev_tutorial.ipynb with {len(cells)} cells")
