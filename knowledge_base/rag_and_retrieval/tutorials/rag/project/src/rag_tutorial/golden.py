"""Build and inspect the golden question set (`data/golden/qa.jsonl`).

Five question types probe different retrieval behaviour:
- `single_hop`: answerable from one passage of one paper.
- `multi_hop`: needs a passage from *each* of two different papers.
- `comparative`: "how does X in paper A differ from Y in paper B".
- `global`: about the corpus as a whole (themes, which papers address X).
- `unanswerable`: plausible-sounding but not answerable from the corpus —
  the model should say so, not hallucinate.

`generate` asks `qwen3.8:27b` for structured JSON candidates (one call per
item) and keeps only the ones whose evidence quotes are verbatim substrings
of the source text (whitespace-normalised) — this catches the model
paraphrasing instead of quoting, which would make the evidence useless for
retrieval metrics. `review` prints every kept item for a human pass; `stats`
summarises the final file.
"""

from __future__ import annotations

import json
import random
import re
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from rag_tutorial.config import settings
from rag_tutorial.corpus import MD_DIR, load_papers
from rag_tutorial.llm import Ollama, count_tokens
from rag_tutorial.schema import Document

app = typer.Typer(add_completion=False)
console = Console()

QA_PATH = settings.path("data/golden/qa.jsonl")

PASSAGE_TOKENS = 800
SEED = 42

N_SINGLE_HOP = 12
N_MULTI_HOP = 10
N_COMPARATIVE = 6
N_GLOBAL = 6
N_UNANSWERABLE = 6

_WHITESPACE_RE = re.compile(r"\s+")


def _normalize(text: str) -> str:
    return _WHITESPACE_RE.sub(" ", text).strip()


def quote_in_source(quote: str, source: str) -> bool:
    """Verbatim-substring check after collapsing all whitespace runs to one space.

    We require an *exact* normalised substring match (not fuzzy) for golden
    evidence, because these quotes are the ground truth `retrieval_metrics`
    is scored against — a paraphrase here would silently make every later
    chapter's recall numbers wrong.
    """
    return _normalize(quote) in _normalize(source)


# -- corpus access -----------------------------------------------------------------


def load_documents() -> dict[str, Document]:
    docs = {}
    for paper in load_papers():
        md_path = MD_DIR / f"{paper['id']}.md"
        if not md_path.exists():
            continue
        docs[paper["id"]] = Document.from_markdown(paper["id"], paper["title"], md_path.read_text())
    return docs


def _first_abstract(text: str) -> str:
    """Best-effort abstract extraction: the paragraph after an 'Abstract' heading,
    or the first ~600 characters of body text if no such heading is found."""
    match = re.search(r"abstract\W*\n+(.+?)(?:\n\s*\n|\n#|\n\d+\s+introduction)", text, re.IGNORECASE | re.DOTALL)
    if match:
        return _normalize(match.group(1))[:1200]
    body = text.split("<!-- page 1 -->", 1)[-1]
    return _normalize(body)[:1200]


def sample_passage(doc: Document, rng: random.Random, n_tokens: int = PASSAGE_TOKENS) -> tuple[str, int, int]:
    """Pick a random ~n_tokens-token window of the paper's body text.

    Character offsets are approximated by scaling from `count_tokens`, then
    the window is grown/shrunk by a few characters at a time until its token
    count is close to the target — good enough for a passage sampler that
    only feeds question generation, not for anything scored.
    """
    text = doc.text
    approx_chars_per_token = max(len(text) / max(count_tokens(text), 1), 1)
    window_chars = int(n_tokens * approx_chars_per_token)
    window_chars = min(window_chars, len(text))
    max_start = max(len(text) - window_chars, 0)
    start = rng.randint(0, max_start) if max_start > 0 else 0
    end = min(start + window_chars, len(text))
    return text[start:end], start, end


# -- JSON schemas for structured generation -----------------------------------------

_SINGLE_HOP_SCHEMA = {
    "type": "object",
    "properties": {
        "question": {"type": "string"},
        "answer": {"type": "string"},
        "quote": {"type": "string", "description": "verbatim span (<=300 chars) from the passage that answers the question"},
    },
    "required": ["question", "answer", "quote"],
}

_TWO_QUOTE_SCHEMA = {
    "type": "object",
    "properties": {
        "question": {"type": "string"},
        "answer": {"type": "string"},
        "quote_a": {"type": "string", "description": "verbatim span (<=300 chars) from passage A"},
        "quote_b": {"type": "string", "description": "verbatim span (<=300 chars) from passage B"},
    },
    "required": ["question", "answer", "quote_a", "quote_b"],
}

_GLOBAL_SCHEMA = {
    "type": "object",
    "properties": {
        "question": {"type": "string"},
        "answer": {"type": "string"},
        "papers": {"type": "array", "items": {"type": "string"}, "description": "arXiv ids of the papers the answer relies on"},
    },
    "required": ["question", "answer", "papers"],
}

_UNANSWERABLE_SCHEMA = {
    "type": "object",
    "properties": {
        "question": {"type": "string", "description": "plausible-sounding but NOT answerable from a 2020-2024 RAG-research corpus"},
        "answer": {"type": "string", "description": "why this cannot be answered from the provided papers"},
    },
    "required": ["question", "answer"],
}


def _ask(client: Ollama, prompt: str, schema: dict) -> dict:
    reply = client.chat(
        [
            {
                "role": "system",
                "content": "You write evaluation questions for a RAG benchmark. Reply with JSON only, matching the schema.",
            },
            {"role": "user", "content": prompt},
        ],
        json_schema=schema,
        max_tokens=512,
    )
    return json.loads(reply)


# -- per-type generation -------------------------------------------------------------


def generate_single_hop(client: Ollama, docs: dict[str, Document], rng: random.Random, n: int) -> list[dict]:
    items = []
    paper_ids = list(docs)
    rng.shuffle(paper_ids)
    # oversample: cycle through papers twice so a failed verification on one
    # paper's passage doesn't cost that paper its question
    candidates = (paper_ids * 2)[: n * 2]
    for paper_id in candidates:
        if len(items) >= n:
            break
        passage, _start, _end = sample_passage(docs[paper_id], rng)
        prompt = (
            f"Passage from the paper '{docs[paper_id].title}' (arXiv {paper_id}):\n\n{passage}\n\n"
            "Write ONE factoid question that is answerable using ONLY this passage, and that is "
            "specific to this paper (not a generic question about RAG in general). Give a short "
            "reference answer, and quote the exact sentence or phrase (<=300 characters, verbatim, "
            "no paraphrasing) from the passage above that supports the answer."
        )
        try:
            data = _ask(client, prompt, _SINGLE_HOP_SCHEMA)
        except (json.JSONDecodeError, KeyError):
            continue
        if not quote_in_source(data["quote"], passage):
            continue
        items.append(
            {
                "type": "single_hop",
                "question": data["question"],
                "answer": data["answer"],
                "evidence": [{"paper": paper_id, "quote": data["quote"].strip()}],
            }
        )
    return items


def generate_multi_hop(client: Ollama, docs: dict[str, Document], rng: random.Random, n: int) -> list[dict]:
    items = []
    paper_ids = list(docs)
    for _ in range(n * 2):  # oversample; some candidates will fail verification
        if len(items) >= n:
            break
        a, b = rng.sample(paper_ids, 2)
        passage_a, _, _ = sample_passage(docs[a], rng)
        passage_b, _, _ = sample_passage(docs[b], rng)
        prompt = (
            f"Passage A, from '{docs[a].title}' (arXiv {a}):\n{passage_a}\n\n"
            f"Passage B, from '{docs[b].title}' (arXiv {b}):\n{passage_b}\n\n"
            "Write ONE question that can only be answered by combining information from BOTH "
            "passages (a reader who only saw one of them could not fully answer it). Give a short "
            "reference answer, and quote a verbatim supporting span (<=300 characters) from each "
            "passage."
        )
        try:
            data = _ask(client, prompt, _TWO_QUOTE_SCHEMA)
        except (json.JSONDecodeError, KeyError):
            continue
        if not (quote_in_source(data["quote_a"], passage_a) and quote_in_source(data["quote_b"], passage_b)):
            continue
        items.append(
            {
                "type": "multi_hop",
                "question": data["question"],
                "answer": data["answer"],
                "evidence": [
                    {"paper": a, "quote": data["quote_a"].strip()},
                    {"paper": b, "quote": data["quote_b"].strip()},
                ],
            }
        )
    return items


def generate_comparative(client: Ollama, docs: dict[str, Document], rng: random.Random, n: int) -> list[dict]:
    items = []
    paper_ids = list(docs)
    for _ in range(n * 2):
        if len(items) >= n:
            break
        a, b = rng.sample(paper_ids, 2)
        passage_a, _, _ = sample_passage(docs[a], rng)
        passage_b, _, _ = sample_passage(docs[b], rng)
        prompt = (
            f"Passage A, from '{docs[a].title}' (arXiv {a}):\n{passage_a}\n\n"
            f"Passage B, from '{docs[b].title}' (arXiv {b}):\n{passage_b}\n\n"
            "Write ONE comparative question of the form 'how does <aspect> in paper A differ from "
            "<aspect> in paper B', where the aspect is something both passages actually describe "
            "(e.g. a method, a metric, a design choice). Give a short reference answer contrasting "
            "the two, and quote a verbatim supporting span (<=300 characters) from each passage."
        )
        try:
            data = _ask(client, prompt, _TWO_QUOTE_SCHEMA)
        except (json.JSONDecodeError, KeyError):
            continue
        if not (quote_in_source(data["quote_a"], passage_a) and quote_in_source(data["quote_b"], passage_b)):
            continue
        items.append(
            {
                "type": "comparative",
                "question": data["question"],
                "answer": data["answer"],
                "evidence": [
                    {"paper": a, "quote": data["quote_a"].strip()},
                    {"paper": b, "quote": data["quote_b"].strip()},
                ],
            }
        )
    return items


# Distinct angles for `global` questions. Without something like this every
# candidate call has the *same* prompt (same paper listing, temperature 0) and
# therefore the same cache key — the first attempt at this generator produced
# six byte-identical questions before this list was added.
_GLOBAL_FOCUS_AREAS = [
    "which papers propose ways to improve the retrieval step itself (not generation)",
    "which papers are primarily about evaluating or benchmarking RAG systems, and how",
    "which papers address multi-hop or multi-document reasoning",
    "what failure modes or limitations of RAG are discussed across multiple papers",
    "which papers propose alternatives to flat top-k chunk retrieval (e.g. trees, graphs, iteration)",
    "how do the papers differ in the kind of external knowledge source they retrieve from",
]


def generate_global(client: Ollama, docs: dict[str, Document], rng: random.Random, n: int) -> list[dict]:
    abstracts = {paper_id: _first_abstract(doc.text) for paper_id, doc in docs.items()}
    listing = "\n".join(f"- {pid} ({docs[pid].title}): {abstracts[pid][:400]}" for pid in docs)
    items = []
    focus_areas = _GLOBAL_FOCUS_AREAS[:n]
    for focus in focus_areas:
        prompt = (
            f"Here is a list of papers with their abstracts:\n{listing}\n\n"
            f"Write ONE 'global' question about the corpus as a whole, focused on: {focus}. "
            "Give a short reference answer, and list the arXiv ids of the papers the answer relies on."
        )
        try:
            data = _ask(client, prompt, _GLOBAL_SCHEMA)
        except (json.JSONDecodeError, KeyError):
            continue
        cited = [pid for pid in data.get("papers", []) if pid in docs]
        if not cited:
            continue
        items.append(
            {
                "type": "global",
                "question": data["question"],
                "answer": data["answer"],
                "evidence": [{"paper": pid, "quote": abstracts[pid][:300]} for pid in cited],
            }
        )
    return items


# Distinct "shapes" of unanswerable question, one per candidate — same reason
# as `_GLOBAL_FOCUS_AREAS`: an identical prompt at temperature 0 is a cache hit
# on the *same* response every time, so plain "make one up" instructions
# without a per-candidate hook produced six identical questions.
_UNANSWERABLE_HOOKS = [
    "a specific numeric result (e.g. an F1 or accuracy score) from a paper published in 2027",
    "a question about an unrelated field, e.g. protein folding or astrophysics",
    "a question about a named model or benchmark that sounds real but does not appear in any of these papers",
    "a question asking to compare this corpus's results against a 2026 industry leaderboard",
    "a question about the private implementation details of a commercial product (not a research paper)",
    "a question about a section or appendix number that does not exist in any of these papers",
]


def generate_unanswerable(client: Ollama, docs: dict[str, Document], rng: random.Random, n: int) -> list[dict]:
    titles = "\n".join(f"- {pid}: {doc.title}" for pid, doc in docs.items())
    items = []
    for hook in _UNANSWERABLE_HOOKS[:n]:
        prompt = (
            f"This corpus contains only these 2020-2024 papers about retrieval-augmented generation:\n{titles}\n\n"
            f"Write ONE question that sounds like it could plausibly be about this corpus, built "
            f"around this hook: {hook}. Then write an answer explaining that this cannot be "
            "answered from the provided papers."
        )
        try:
            data = _ask(client, prompt, _UNANSWERABLE_SCHEMA)
        except (json.JSONDecodeError, KeyError):
            continue
        items.append(
            {
                "type": "unanswerable",
                "question": data["question"],
                "answer": data["answer"],
                "evidence": [],
            }
        )
    return items


GENERATORS = {
    "single_hop": (generate_single_hop, N_SINGLE_HOP),
    "multi_hop": (generate_multi_hop, N_MULTI_HOP),
    "comparative": (generate_comparative, N_COMPARATIVE),
    "global": (generate_global, N_GLOBAL),
    "unanswerable": (generate_unanswerable, N_UNANSWERABLE),
}


@app.command()
def generate(seed: int = SEED) -> None:
    """Generate candidate questions of all five types and write them to qa.jsonl.

    Every 4th item (by final index) is assigned split="dev"; the rest are
    "test". Run `just golden-review` afterwards for the human pass.
    """
    client = Ollama()
    docs = load_documents()
    rng = random.Random(seed)

    all_items: list[dict] = []
    for type_name, (fn, n) in GENERATORS.items():
        items = fn(client, docs, rng, n)
        console.print(f"{type_name}: kept {len(items)}/{n} requested")
        all_items.extend(items)

    for i, item in enumerate(all_items):
        item["id"] = f"{item['type']}_{i:03d}"
        item["split"] = "dev" if (i + 1) % 4 == 0 else "test"

    QA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with QA_PATH.open("w") as f:
        for item in all_items:
            ordered = {k: item[k] for k in ["id", "type", "split", "question", "answer", "evidence"]}
            f.write(json.dumps(ordered, ensure_ascii=False) + "\n")
    console.print(f"[green]wrote {len(all_items)} items[/green] to {QA_PATH}")


def load_qa(path: Path | None = None) -> list[dict]:
    path = path or QA_PATH
    with path.open() as f:
        return [json.loads(line) for line in f if line.strip()]


@app.command()
def review() -> None:
    """Print every item in qa.jsonl with its evidence, for a human read-through."""
    items = load_qa()
    for item in items:
        console.print(f"\n[bold]{item['id']}[/bold] ({item['type']}, {item['split']})")
        console.print(f"  Q: {item['question']}")
        console.print(f"  A: {item['answer']}")
        for ev in item["evidence"]:
            console.print(f"  evidence [{ev['paper']}]: {ev['quote']!r}")


@app.command()
def stats() -> None:
    """Print counts per type/split, mean question length, and paper coverage."""
    items = load_qa()
    table = Table(title="golden set stats")
    table.add_column("type")
    table.add_column("dev", justify="right")
    table.add_column("test", justify="right")
    table.add_column("total", justify="right")
    by_type: dict[str, dict[str, int]] = {}
    for item in items:
        by_type.setdefault(item["type"], {"dev": 0, "test": 0})
        by_type[item["type"]][item["split"]] += 1
    for type_name, counts in by_type.items():
        total = counts["dev"] + counts["test"]
        table.add_row(type_name, str(counts["dev"]), str(counts["test"]), str(total))
    total_dev = sum(c["dev"] for c in by_type.values())
    total_test = sum(c["test"] for c in by_type.values())
    table.add_row("[bold]total[/bold]", f"[bold]{total_dev}[/bold]", f"[bold]{total_test}[/bold]", f"[bold]{len(items)}[/bold]")
    console.print(table)

    mean_len = sum(count_tokens(item["question"]) for item in items) / max(len(items), 1)
    console.print(f"mean question length: {mean_len:.1f} tokens")

    papers_covered = {ev["paper"] for item in items for ev in item["evidence"]}
    console.print(f"papers covered by evidence: {len(papers_covered)} — {sorted(papers_covered)}")


if __name__ == "__main__":
    app()
