"""Chapter 02: the 80-ticket set with gold labels by construction.

Grid: 6 personas x 12 topics (handbook section ids) x 4 scenarios. 80
combinations are picked with a seeded RNG such that every topic appears at
least 5 times and every scenario at least 15 times. The labels are decided
*before* the LLM writes the ticket text, so they are gold by construction:

- category  = topic
- priority  = f(scenario)
- needs_escalation = out_of_policy_request, or urgent_blocker on sensitive topics
- sections  = [topic] (+ one related section for 20 % of the tickets)
- answer_points = the 1-2 key facts the ticket must be about

The LLM only writes the customer's message (60-160 words, persona voice) for
each (persona, topic, scenario, facts) tuple.
"""

from __future__ import annotations

import json
import random
from pathlib import Path

import typer
from pydantic import BaseModel, Field
from rich.console import Console
from rich.table import Table

from evals_tutorial.config import settings
from evals_tutorial.handbook import SECTION_IDS, key_facts
from evals_tutorial.llm import ollama

TICKETS_PATH = Path("data") / "tickets" / "tickets.jsonl"

SEED = 42
N_TICKETS = 80
# Dev budget per topic so the split is exactly 20 dev / 60 test and every
# topic appears in BOTH splits (8 topics take 2 dev tickets, 4 take 1).
DEV_PER_TOPIC: dict[str, int] = {sid: (2 if i < 8 else 1) for i, sid in enumerate(SECTION_IDS)}

PERSONAS: list[str] = [
    "hurried commuter",
    "polite retiree",
    "angry first-time buyer",
    "small-business buyer",
    "non-native English speaker",
    "teenager",
]

SCENARIOS: list[str] = ["simple_question", "problem_report", "urgent_blocker", "out_of_policy_request"]

PRIORITY_BY_SCENARIO: dict[str, str] = {
    "simple_question": "low",
    "problem_report": "normal",
    "urgent_blocker": "urgent",
    "out_of_policy_request": "normal",
}

# Topics where an urgent blocker also needs escalation (money, personal data, safety).
ESCALATING_TOPICS = {"payments", "privacy", "damaged_items"}

# Fixed related-section map: for the 20 % of tickets that need a second section.
RELATED_SECTION: dict[str, str] = {
    "returns": "shipping",
    "shipping": "returns",
    "warranty": "damaged_items",
    "damaged_items": "warranty",
    "discounts": "gift_cards",
    "gift_cards": "discounts",
    "payments": "order_changes",
    "order_changes": "payments",
    "international": "shipping",
    "loyalty": "discounts",
    "privacy": "accounts",
    "accounts": "privacy",
}

SCENARIO_PROMPT: dict[str, str] = {
    "simple_question": "You have a simple question about the policy. There is no problem yet, you just want to know the rules before doing anything.",
    "problem_report": "Something went wrong and you are reporting a problem about the policy.",
    "urgent_blocker": "You are blocked RIGHT NOW and it is urgent: the issue is stopping you from doing what you came to the shop for.",
    "out_of_policy_request": "You are asking for something the shop's policy probably does not allow (an exception, a special case, a refund that is normally denied). You are not threatening, just asking.",
}


class TicketText(BaseModel):
    text: str = Field(description="The customer's message, 60-160 words")


def _ticket_text(client, prompt: str) -> str:
    """Ask the LLM for the customer's message, via `chat_json` (schema {text: str})
    on the real cached client, or plain `chat` on offline stand-ins like FakeLLM."""
    from evals_tutorial.llm import Ollama

    messages = [{"role": "user", "content": prompt}]
    if isinstance(client, Ollama):
        return client.chat_json(messages, TicketText, temperature=0.0).text
    return client.chat(messages, temperature=0.0)


def pick_grid(rng: random.Random) -> list[tuple[str, str, str]]:
    """Pick N_TICKETS persona/topic/scenario triples: every topic >= 5, every scenario >= 15.

    Construction: 12 topics start at 5 each (60), the remaining 20 are added
    round-robin. Scenarios come from a bag of 15 of each (60) plus 20 random
    extras, all shuffled, dealt one per ticket, so the coverage floors hold.
    """
    per_topic = {sid: 5 for sid in SECTION_IDS}
    for i in range(N_TICKETS - sum(per_topic.values())):
        per_topic[SECTION_IDS[i % len(SECTION_IDS)]] += 1

    bag = [s for s in SCENARIOS for _ in range(15)]
    bag += [rng.choice(SCENARIOS) for _ in range(N_TICKETS - len(bag))]
    rng.shuffle(bag)

    combos: list[tuple[str, str, str]] = []
    idx = 0
    for sid in SECTION_IDS:
        offset = (SECTION_IDS.index(sid) * 2) % len(PERSONAS)
        for j in range(per_topic[sid]):
            scenario = bag[idx]
            persona = PERSONAS[(j + offset) % len(PERSONAS)]
            combos.append((persona, sid, scenario))
            idx += 1
    return combos


def gold_labels(topic: str, scenario: str, facts: list[str], related: bool) -> dict:
    sections = [topic]
    if related and topic in RELATED_SECTION:
        related_sid = RELATED_SECTION[topic]
        if related_sid not in sections:
            sections.append(related_sid)
    needs_escalation = scenario == "out_of_policy_request" or (
        scenario == "urgent_blocker" and topic in ESCALATING_TOPICS
    )
    return {
        "category": topic,
        "priority": PRIORITY_BY_SCENARIO[scenario],
        "needs_escalation": needs_escalation,
        "sections": sections,
        "answer_points": list(facts),
    }


def _ticket_user_prompt(persona: str, topic: str, scenario: str, facts: list[str]) -> str:
    return (
        f"Write the message a customer with this profile sends to Northwind Outdoor support "
        f"(a shop selling bikes and camping gear).\n\n"
        f"Customer profile: {persona}.\n"
        f"Situation: {SCENARIO_PROMPT[scenario]}\n"
        f"The message must be about these policy facts:\n" + "\n".join(f"- {f}" for f in facts) + "\n\n"
        "Rules:\n"
        "- 60 to 160 words, first person, in the voice of the customer profile above.\n"
        "- Do NOT name the policy section or use headings; write it like a real support ticket.\n"
        "- The message must reference the concrete numbers from the facts above.\n\n"
        "Reply with only the customer's message."
    )


def generate(client=None) -> list[dict]:
    """Build the 80 tickets (labels first, then LLM text) and return them as dicts."""
    client = client or ollama
    rng = random.Random(SEED)
    handbook = {sid: key_facts(sid) for sid in SECTION_IDS}
    combos = pick_grid(rng)
    assert len(combos) == N_TICKETS

    rows: list[dict] = []
    for i, (persona, topic, scenario) in enumerate(combos, start=1):
        topic_facts = handbook[topic]
        n_facts = rng.choice([1, 2]) if len(topic_facts) > 1 else 1
        facts = rng.sample(topic_facts, n_facts)
        related = (i % 5) == 0  # 16 of 80 = 20 %
        gold = gold_labels(topic, scenario, facts, related)
        prompt = _ticket_user_prompt(persona, topic, scenario, facts)
        ticket_text = _ticket_text(client, prompt)

        rows.append(
            {
                "id": f"tkt-{i:03d}",
                "persona": persona,
                "topic": topic,
                "scenario": scenario,
                "text": ticket_text,
                "gold": gold,
            }
        )
    return rows


def split(rows: list[dict]) -> list[dict]:
    """Assign split exactly 20 dev / 60 test, stratified by topic (>= 1 dev per topic)."""
    seen: dict[str, int] = {}
    out = []
    for row in rows:
        n = seen.get(row["topic"], 0) + 1
        seen[row["topic"]] = n
        row = dict(row)
        row["split"] = "dev" if n <= DEV_PER_TOPIC.get(row["topic"], 1) else "test"
        out.append(row)
    dev = sum(1 for r in out if r["split"] == "dev")
    assert dev == 20, f"expected 20 dev, got {dev}"
    return out


def write(rows: list[dict], path: Path | None = None) -> Path:
    path = path or settings.path(TICKETS_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["id", "split", "persona", "topic", "scenario", "text", "gold"]
    with path.open("w") as fh:
        for row in rows:
            fh.write(json.dumps({k: row[k] for k in fields}, ensure_ascii=False) + "\n")
    return path


def load_tickets(path: Path | None = None) -> list[dict]:
    path = path or settings.path(TICKETS_PATH)
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def stats() -> dict[str, dict[str, int]]:
    rows = load_tickets()
    out: dict[str, dict[str, int]] = {}
    for key in ("topic", "scenario", "split"):
        counts: dict[str, int] = {}
        for r in rows:
            counts[r[key]] = counts.get(r[key], 0) + 1
        out[key] = counts
    priority_counts: dict[str, int] = {}
    for r in rows:
        priority_counts[r["gold"]["priority"]] = priority_counts.get(r["gold"]["priority"], 0) + 1
    out["priority"] = priority_counts
    return out


app = typer.Typer(add_completion=False)


@app.command(name="generate")
def generate_cmd() -> None:
    """Generate the 80 tickets (labels by construction + LLM text) and write tickets.jsonl."""
    rows = split(generate())
    path = write(rows)
    print(f"Wrote {len(rows)} tickets to {path}")


@app.command(name="stats")
def stats_cmd() -> None:
    """Counts per topic / scenario / priority / split."""
    console = Console()
    for name, counts in stats().items():
        table = Table(title=f"tickets by {name}")
        table.add_column(name)
        table.add_column("count", justify="right")
        for k in sorted(counts):
            table.add_row(k, str(counts[k]))
        console.print(table)


if __name__ == "__main__":
    app()
