"""A small evaluation harness: LLM-as-judge over `data/questions.json` (chapter 10).

Chapters 08/09 showed individual answers looked good by eye. This module
automates that eye-check across every question in the shared evaluation set,
in both `vector` (plain RAG baseline) and `graph` (this tutorial's pipeline)
modes, and asks the LLM (Large Language Model) itself to judge each answer
against the passages it was allowed to use -- "LLM-as-judge". With only 8
questions this is a smoke test, not a statistically meaningful benchmark; see
"limits of this harness" in chapter 10 for why.

Run with: python -m graph_rag.evaluate run
"""

import json
import time
from datetime import datetime, timezone
from pathlib import Path

import typer
from pydantic import BaseModel, Field
from rich.console import Console
from rich.table import Table

from graph_rag import retrieval
from graph_rag.llm import chat_json

app = typer.Typer(add_completion=False)
console = Console()

_QUESTIONS_PATH = Path("data/questions.json")
_OUT_DIR = Path("data/extracted")
_MAX_CHUNK_CHARS_FOR_JUDGE = 6000


class Judgement(BaseModel):
    faithful: bool = Field(description="True only if every claim in the answer is directly supported by the source chunks")
    complete_0_5: int = Field(ge=0, le=5, description="How completely the answer addresses the question, 0 (not at all) to 5 (fully)")
    reason: str = Field(description="One sentence explaining the judgement")


_JUDGE_SYSTEM = """You are grading one answer from a RAG (Retrieval-Augmented Generation) system \
against the exact source passages it was allowed to use. Judge two things:
1. faithful: true only if every claim in the answer is directly supported by the source passages \
below -- no invented facts, no claims the passages don't actually say. An honest "not in the \
documents" answer is faithful if the passages genuinely do not contain the answer.
2. complete_0_5: how completely the answer addresses the question, 0 (not at all) to 5 (fully). An \
honest "not in the documents" answer should score high completeness if the passages genuinely lack \
the information -- that is the correct, complete response to give, not a failure.
Output ONLY JSON matching the given schema."""


def _judge(question: str, answer_text: str, chunks: list[dict]) -> Judgement:
    chunks_text = "\n".join(f"[{c['id']}] {c['text']}" for c in chunks)[:_MAX_CHUNK_CHARS_FOR_JUDGE]
    user = f"Question: {question}\n\nAnswer:\n{answer_text}\n\nSource passages:\n{chunks_text}"
    messages = [{"role": "system", "content": _JUDGE_SYSTEM}, {"role": "user", "content": user}]
    return chat_json(messages, Judgement)


def _run_one(question: dict, mode: str) -> dict:
    """Answer `question` in `mode`, time it, then judge it against the same
    context `build_context` would hand the LLM (a second, cheap retrieval
    call with no extra LLM chat -- only `retrieval.answer`'s own internal
    context build makes an LLM call).
    """
    start = time.monotonic()
    ans = retrieval.answer(question["question"], mode=mode)
    elapsed = time.monotonic() - start

    ctx = retrieval.build_context(question["question"], mode)
    judgement = _judge(question["question"], ans.text, ctx.chunks)

    return {
        "id": question["id"],
        "type": question["type"],
        "question": question["question"],
        "mode": mode,
        "answer": ans.text,
        "citations": ans.citations,
        "latency_s": round(elapsed, 2),
        "context_tokens": ans.context_stats["budget_used"],
        "faithful": judgement.faithful,
        "complete_0_5": judgement.complete_0_5,
        "reason": judgement.reason,
    }


def run_evaluation(questions_path: Path = _QUESTIONS_PATH, modes: tuple[str, ...] = ("vector", "graph")) -> dict:
    questions = json.loads(questions_path.read_text())
    records: list[dict] = []
    for q in questions:
        for mode in modes:
            records.append(_run_one(q, mode))

    summary = _summarize(records, modes)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "n_questions": len(questions),
        "modes": list(modes),
        "records": records,
        "summary": summary,
    }


def _summarize(records: list[dict], modes: tuple[str, ...]) -> list[dict]:
    summary = []
    for mode in modes:
        rows = [r for r in records if r["mode"] == mode]
        if not rows:
            continue
        n = len(rows)
        summary.append(
            {
                "mode": mode,
                "n_questions": n,
                "faithful_pct": round(100 * sum(r["faithful"] for r in rows) / n, 1),
                "avg_completeness_0_5": round(sum(r["complete_0_5"] for r in rows) / n, 2),
                "avg_latency_s": round(sum(r["latency_s"] for r in rows) / n, 2),
                # one `answer` chat call + one `_judge` chat call per question;
                # graph mode's `answer` also spends embedding calls inside
                # `retrieve_context`, not counted here since those are cheap
                # embedding calls, not chat completions.
                "llm_calls": 2 * n,
                "avg_context_tokens": round(sum(r["context_tokens"] for r in rows) / n, 1),
            }
        )
    return summary


def _print_summary(summary: list[dict]) -> Table:
    table = Table(title="Evaluation summary")
    for col in ["mode", "n_questions", "faithful_pct", "avg_completeness_0_5", "avg_latency_s", "llm_calls", "avg_context_tokens"]:
        table.add_column(col)
    for row in summary:
        table.add_row(*[str(row[c]) for c in ["mode", "n_questions", "faithful_pct", "avg_completeness_0_5", "avg_latency_s", "llm_calls", "avg_context_tokens"]])
    return table


@app.command()
def run(
    questions: Path = typer.Option(_QUESTIONS_PATH, "--questions"),
    out_dir: Path = typer.Option(_OUT_DIR, "--out-dir"),
) -> None:
    """Run the evaluation harness and save `data/extracted/eval_<timestamp>.json`."""
    result = run_evaluation(questions)
    out_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_path = out_dir / f"eval_{timestamp}.json"
    out_path.write_text(json.dumps(result, indent=2) + "\n")
    console.print(_print_summary(result["summary"]))
    console.print(f"[green]saved {out_path}[/green]")


if __name__ == "__main__":
    app()
