"""Chapter 02: the Northwind Outdoor helpdesk — `triage` and `answer`.

- `triage(ticket_text, version)` classifies a ticket (12 categories, 4
  priorities, escalation flag) with the versioned system prompt
  `prompts/triage_v1.txt` and the cached JSON-schema chat call.
- `answer(ticket_text, version)` embeds the 12 handbook sections (chunked to
  <= 120 words) + the ticket, retrieves the top-k chunks by cosine, collapses
  them to sections, and writes a reply from the top-2 sections' full text
  (citations as `[section_id]`).
- `run --task triage|answer --version v1 --split all` records one trace file
  per ticket at `project/runs/traces/<task>_<version>/<ticket_id>.json`
  (the trace contract in `index.md`).

Every LLM call goes through `evals_tutorial.llm`, so re-runs are cached.
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path

import typer
from typing import Literal
from pydantic import BaseModel, Field

from evals_tutorial.config import settings
from evals_tutorial.handbook import SECTION_IDS, handbook_dir
from evals_tutorial.llm import ollama
from evals_tutorial.tickets import load_tickets
from evals_tutorial.tracing import observe  # chapter 13: env guard, no-op without keys

PROMPTS_DIR = Path(__file__).parent / "prompts"
RUNS_DIR = Path("runs") / "traces"

TOP_K_CHUNKS = 4
TOP_SECTIONS = 2
CHUNK_MAX_WORDS = 120

Category = Literal[
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
Priority = Literal["low", "normal", "high", "urgent"]


class Triage(BaseModel):
    category: Category
    priority: Priority
    needs_escalation: bool
    reason: str


class Reply(BaseModel):
    text: str
    citations: list[str] = Field(default_factory=list, description="section ids cited as [section_id]")


# -- prompt loading -----------------------------------------------------------


def prompt_text(name: str, version: str) -> str:
    return (PROMPTS_DIR / f"{name}_{version}.txt").read_text()


# -- retrieval ----------------------------------------------------------------


def chunk_text(text: str, max_words: int = CHUNK_MAX_WORDS) -> list[str]:
    """Split text into chunks of at most `max_words` words along sentence boundaries."""
    words = text.split()
    if len(words) <= max_words:
        return [text] if text.strip() else []

    sentences = re.split(r"(?<=[.!?])\s+|\n+", text.strip())
    chunks: list[str] = []
    cur: list[str] = []
    cur_words = 0
    for sentence in sentences:
        s_words = len(sentence.split())
        if cur and cur_words + s_words > max_words:
            chunks.append(" ".join(cur))
            cur, cur_words = [], 0
        if s_words > max_words and cur:
            chunks.append(" ".join(cur))
            cur, cur_words = [], 0
        # even a single huge sentence is pushed as its own chunk (handbook rules are short)
        cur.append(sentence)
        cur_words += s_words
    if cur:
        chunks.append(" ".join(cur))
    return [c.strip() for c in chunks if c.strip()]


def _handbook_chunks() -> list[dict]:
    """{section, text} for every handbook chunk (<= CHUNK_MAX_WORDS words)."""
    out: list[dict] = []
    for sid in SECTION_IDS:
        path = handbook_dir() / f"{sid}.md"
        if not path.exists():
            continue
        for chunk in chunk_text(path.read_text()):
            out.append({"section": sid, "text": chunk})
    return out


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def retrieve(ticket_text: str, k: int = TOP_K_CHUNKS, client=None) -> list[dict]:
    """Embed handbook chunks + ticket, cosine top-k chunks, collapse to sections in score order.

    Returns `[{section, score}]` — one row per section, that section's best
    chunk score, sections sorted by best score descending.
    """
    client = client or ollama
    chunks = _handbook_chunks()
    vectors = client.embed_documents([c["text"] for c in chunks])
    query = client.embed_query(ticket_text)
    scored = sorted(
        ((c["section"], _cosine(query, vector)) for c, vector in zip(chunks, vectors)),
        key=lambda pair: pair[1],
        reverse=True,
    )[:k]
    best: dict[str, float] = {}
    for section, score in scored:
        best[section] = max(best.get(section, score), score)
    return [{"section": section, "score": round(score, 6)} for section, score in sorted(best.items(), key=lambda kv: -kv[1])]


def retrieved_context(ticket_text: str, top_n: int = TOP_SECTIONS, client=None) -> tuple[list[str], list[dict]]:
    """Top-n retrieved sections as full-text blocks, plus the `retrieved` rows."""
    retrieved = retrieve(ticket_text, client=client)
    sections = [row["section"] for row in retrieved[:top_n]]
    blocks = []
    for sid in sections:
        blocks.append((handbook_dir() / f"{sid}.md").read_text().strip())
    return blocks, retrieved


# -- triage -------------------------------------------------------------------


def triage_messages(ticket_text: str, version: str = "v1") -> list[dict]:
    return [
        {"role": "system", "content": prompt_text("triage", version)},
        {"role": "user", "content": ticket_text},
    ]


def triage(ticket_text: str, version: str = "v1", client=None) -> Triage:
    """Classify a ticket via the versioned prompt + JSON-schema chat call."""
    client = client or ollama
    return client.chat_json(triage_messages(ticket_text, version), Triage, temperature=0.0)


# -- answer -------------------------------------------------------------------

_CITATION_RE = re.compile(r"\[([a-z_]+)\]")


def answer_messages(ticket_text: str, version: str = "v1", client=None) -> list[dict]:
    """Assemble the system prompt + user message (excerpts and the ticket)."""
    client = client or ollama
    blocks, _ = retrieved_context(ticket_text, client=client)
    user = "Handbook excerpts:\n" + "\n\n".join(blocks) + "\n\nCustomer question:\n" + ticket_text
    return [
        {"role": "system", "content": prompt_text("answer", version)},
        {"role": "user", "content": user},
    ]


@observe
def answer(ticket_text: str, version: str = "v1", client=None) -> Reply:
    """Retrieve, then write the reply from the top-2 sections' text.

    Chapter 13: when `LANGFUSE_HOST` + `LANGFUSE_PUBLIC_KEY` are set in
    `.env`, calls are traced into the local Langfuse (`evals_tutorial.tracing`
    turns the wrapper into `langfuse.observe`); otherwise this is a plain
    function and nothing is sent anywhere.
    """
    client = client or ollama
    reply_text = client.chat(answer_messages(ticket_text, version=version, client=client), temperature=0.0)
    citations = list(dict.fromkeys(c for c in _CITATION_RE.findall(reply_text) if c in SECTION_IDS))
    return Reply(text=reply_text, citations=citations)


# -- traces -------------------------------------------------------------------


def _trace_dir(task: str, version: str) -> Path:
    return settings.path(RUNS_DIR / f"{task}_{version}")


def _latest_chat_entry(max_age_s: float = 120.0) -> dict | None:
    """Newest entry under `data/cache/chat` (written by the call we just made).

    Traces report `usage` and `latency_s` from `llm.py`: every chat call
    stores the Ollama `usage` numbers and its own wall time (`elapsed_s`) in
    its cache entry, so reading the newest entry gives the per-ticket numbers.
    """
    import time

    base = settings.path(settings.cache_dir) / "chat"
    if not base.exists():
        return None
    now = time.time()
    best: tuple[float, Path] | None = None
    for path in base.rglob("*.json"):
        mtime = path.stat().st_mtime
        if now - mtime > max_age_s:
            continue
        if best is None or mtime > best[0]:
            best = (mtime, path)
    if best is None:
        return None
    try:
        return json.loads(best[1].read_text())
    except (json.JSONDecodeError, OSError):
        return None


def _call_info(entry: dict | None) -> tuple[float | None, dict | None]:
    """(latency_s, usage) from a cache entry; (None, None) when unavailable."""
    if entry is None:
        return None, None
    return entry.get("elapsed_s"), entry.get("usage")


def write_trace(task: str, version: str, ticket: dict, prompt: str, output, retrieved: list[dict]) -> Path:
    if task == "triage":
        output_field = output.model_dump() if isinstance(output, Triage) else output
    else:
        output_field = output.text if isinstance(output, Reply) else output
    latency_s, usage = _call_info(_latest_chat_entry())
    trace = {
        "run": f"{task}_{version}",
        "version": version,
        "ticket_id": ticket["id"],
        "input": ticket["text"],
        "retrieved": retrieved,
        "prompt": prompt,
        "output": output_field,
        "latency_s": latency_s,
        "model": settings.chat_model,
        "usage": usage,
    }
    out_dir = _trace_dir(task, version)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{ticket['id']}.json"
    path.write_text(json.dumps(trace, indent=2, ensure_ascii=False))
    return path


def load_traces(run: str) -> list[dict]:
    """All traces of one run (e.g. 'answer_v1'), sorted by ticket_id."""
    d = settings.path(RUNS_DIR / run)
    return [json.loads(p.read_text()) for p in sorted(d.glob("*.json"))]


def run_batch(task: str, version: str = "v1", split: str = "all", client=None) -> list[Path]:
    client = client or ollama
    tickets = load_tickets()
    if split != "all":
        tickets = [t for t in tickets if t["split"] == split]
    paths = []
    for ticket in tickets:
        if task == "triage":
            result = triage(ticket["text"], version=version, client=client)
            retrieved: list[dict] = []
            prompt = prompt_text("triage", version)
        elif task == "answer":
            result = answer(ticket["text"], version=version, client=client)
            retrieved = retrieve(ticket["text"], client=client)
            prompt = prompt_text("answer", version)
        else:
            raise ValueError(f"unknown task {task!r} (use 'triage' or 'answer')")
        paths.append(write_trace(task, version, ticket, prompt, result, retrieved))
    return paths


app = typer.Typer(add_completion=False)


@app.command(name="triage")
def triage_cmd(ticket: str) -> None:
    """Triage a ticket (v1 prompt) and print the JSON result."""
    print(json.dumps(triage(ticket).model_dump(), indent=2))


@app.command(name="answer")
def answer_cmd(ticket: str) -> None:
    """Answer a ticket (v1 prompt, RAG) and print text + citations."""
    result = answer(ticket)
    print(result.text)
    print(f"citations: {result.citations}")


@app.command(name="run")
def run_task(
    task: str = typer.Option("triage", help="triage or answer"),
    version: str = typer.Option("v1"),
    split: str = typer.Option("all", help="all, dev or test"),
) -> None:
    """Run one task over every ticket and write one trace file per ticket."""
    paths = run_batch(task, version=version, split=split)
    print(f"{len(paths)} traces written to {_trace_dir(task, version)}")


if __name__ == "__main__":
    app()
