"""Chapter 02: the Northwind Outdoor handbook.

Generates one policy document per handbook section (12 sections) through the
cached LLM client, and provides `load()` / `key_facts()` for the ticket
generator and later chapters.

The 12 section ids are fixed by the data contracts in `index.md`.
"""

from __future__ import annotations

import re
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from evals_tutorial.config import settings
from evals_tutorial.llm import ollama

SECTION_IDS: list[str] = [
    "returns",
    "shipping",
    "warranty",
    "payments",
    "accounts",
    "discounts",
    "gift_cards",
    "order_changes",
    "damaged_items",
    "international",
    "loyalty",
    "privacy",
]

SECTION_TITLES: dict[str, str] = {
    "returns": "Returns",
    "shipping": "Shipping",
    "warranty": "Warranty",
    "payments": "Payments",
    "accounts": "Accounts",
    "discounts": "Discounts",
    "gift_cards": "Gift Cards",
    "order_changes": "Order Changes",
    "damaged_items": "Damaged Items",
    "international": "International Orders",
    "loyalty": "Loyalty Program",
    "privacy": "Privacy",
}

HANDBOOK_DIR = Path("data") / "handbook"

SYSTEM_PROMPT = (
    "You write the customer-facing policy documents of the fictional online shop "
    "Northwind Outdoor, which sells bikes and camping gear. Write only about Northwind "
    "Outdoor. Use Markdown. Be concrete: every rule must contain real numbers (days, "
    "percentages, amounts, thresholds)."
)

_USER_PROMPT_TEMPLATE = (
    "Write the *{title}* policy document for Northwind Outdoor.\n"
    "\n"
    "Requirements:\n"
    "- Start with the heading `# {title}`.\n"
    "- Then 4 to 6 numbered rules (a numbered list). Each rule must contain at least one "
    "concrete number: a number of days, a percentage, a price amount, or a threshold.\n"
    "- The whole document must be between 200 and 400 words.\n"
    "- End the document with a section `## Key facts` containing 3 to 5 bullet points "
    "(`- fact`). Each bullet is one self-contained fact with a concrete number, "
    "covering the most common customer questions for this policy.\n"
    "\n"
    "Reply with the Markdown document only, no commentary."
)


def handbook_dir() -> Path:
    return settings.path(HANDBOOK_DIR)


def _word_count(text: str) -> int:
    return len(re.findall(r"\S+", text))


def load() -> dict[str, str]:
    """Return {section_id: full markdown text} for every handbook section on disk."""
    out: dict[str, str] = {}
    for sid in SECTION_IDS:
        path = handbook_dir() / f"{sid}.md"
        if path.exists():
            out[sid] = path.read_text()
    return out


def key_facts(section_id: str) -> list[str]:
    """Parse the `## Key facts` bullet list of one handbook section."""
    text = (handbook_dir() / f"{section_id}.md").read_text()
    m = re.search(r"## Key facts\s*\n(.*?)(?:\n\n|\Z)", text, re.DOTALL)
    if m is None:
        return []
    bullets = [line[2:].strip() for line in m.group(1).splitlines() if line.lstrip().startswith("- ")]
    return bullets


def generate(section_ids: list[str] | None = None, client=None) -> list[str]:
    """Ask the LLM for one policy document per section and write it to disk.

    Returns the list of section ids generated.
    """
    client = client or ollama
    handbook_dir().mkdir(parents=True, exist_ok=True)
    for sid in section_ids or SECTION_IDS:
        title = SECTION_TITLES[sid]
        reply = client.chat(
            [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": _USER_PROMPT_TEMPLATE.format(title=title)},
            ],
            temperature=0.0,
        )
        (handbook_dir() / f"{sid}.md").write_text(reply.strip() + "\n")
    return section_ids or SECTION_IDS


def stats() -> list[dict]:
    rows = []
    for sid in SECTION_IDS:
        path = handbook_dir() / f"{sid}.md"
        if not path.exists():
            rows.append({"section": sid, "words": 0, "facts": 0})
            continue
        rows.append({"section": sid, "words": _word_count(path.read_text()), "facts": len(key_facts(sid))})
    return rows


app = typer.Typer(add_completion=False)


@app.command(name="generate")
def generate_cmd() -> None:
    """Generate the 12 handbook sections with the (cached) LLM."""
    generate()
    print(f"Wrote {len(SECTION_IDS)} handbook sections to {handbook_dir()}")


@app.command(name="stats")
def stats_cmd() -> None:
    """Table: section | words | facts."""
    console = Console()
    table = Table(title="Handbook stats")
    table.add_column("section")
    table.add_column("words", justify="right")
    table.add_column("facts", justify="right")
    for row in stats():
        table.add_row(row["section"], str(row["words"]), str(row["facts"]))
    console.print(table)


if __name__ == "__main__":
    app()
