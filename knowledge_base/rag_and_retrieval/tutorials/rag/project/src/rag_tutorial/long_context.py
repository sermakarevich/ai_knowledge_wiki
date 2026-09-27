"""Long-context vs RAG mini-experiment (`13_long_context`).

Question: for questions answerable from a single paper, does giving the LLM
the WHOLE paper (long context, no retrieval) beat the best RAG run? The
golden `evidence.paper` tells us which paper each `single_hop` question is
about, so routing is an oracle here (noted as a limitation — a real system
would have to route first, and routing errors would lower the score).

Method: for each sampled `single_hop` test question, prompt `qwen3.8:27b`
with the full paper Markdown (`num_ctx` 32k; papers that do not fit are
truncated and flagged with `truncated: true`) and judge the answer with the
same `judge_correctness` as every other run, so the numbers are comparable.
Results go to `runs/13_long_context/{metrics, predictions}.json` and are
summarised against the best RAG run in the findings note.
"""

from __future__ import annotations

import json
import random
import time

import typer
from rich.console import Console

from rag_tutorial.config import settings
from rag_tutorial.corpus import MD_DIR

app = typer.Typer(add_completion=False)
console = Console()

RUNS_DIR = settings.path("runs")
EXPERIMENT = "13_long_context"

LONG_CTX = 32768
# Character budget for the paper text: ~4 chars/token -> ~24k tokens of paper
# inside a 32k window, leaving room for prompt + answer.
MAX_PAPER_CHARS = 95000


def load_paper_text(paper: str) -> str:
    """Read the parsed Markdown for one paper id (filename stem)."""
    path = MD_DIR / f"{paper}.md"
    return path.read_text()


def build_long_context_prompt(question: str, paper_text: str) -> tuple[str, bool]:
    """Wrap a full paper + question into a prompt; truncate + flag if needed."""
    truncated = len(paper_text) > MAX_PAPER_CHARS
    if truncated:
        paper_text = paper_text[:MAX_PAPER_CHARS]
    prompt = (
        "Answer the question using only the paper below. Quote the paper id in brackets.\n\n"
        f"Paper:\n{paper_text}\n\nQuestion: {question}"
    )
    return prompt, truncated


def answer_long_context(question: str, paper: str, client=None) -> tuple[str, bool, float]:
    """Ask the chat model with the whole paper as context. Returns (answer, truncated, seconds)."""
    from rag_tutorial.llm import ollama  # noqa: PLC0415

    client = client or ollama
    prompt, truncated = build_long_context_prompt(question, load_paper_text(paper))
    start = time.monotonic()
    answer = client.chat(
        [
            {"role": "system", "content": "Answer briefly using only the given paper. If it is not enough, say so."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=384,
        num_ctx=LONG_CTX,
    )
    return answer, truncated, time.monotonic() - start


def sample_single_hop(n: int = 8, seed: int = 13) -> list[dict]:
    """Sample `n` single_hop test questions with single-paper evidence."""
    from rag_tutorial.golden import QA_PATH, load_qa  # noqa: PLC0415

    items = [i for i in load_qa(QA_PATH) if i["split"] == "test" and i["type"] == "single_hop" and i["evidence"]]
    rng = random.Random(seed)
    rng.shuffle(items)
    return items[:n]


def compare_against_rag(longctx: dict, rag_run: str = "07_best_combo") -> dict:
    """Compare long-context results vs a RAG run's predictions on the same ids."""
    preds = {}
    with (RUNS_DIR / rag_run / "predictions.jsonl").open() as f:
        for line in f:
            if line.strip():
                row = json.loads(line)
                preds[row["id"]] = row
    rows = []
    for item in longctx["items"]:
        rag = preds.get(item["id"], {})
        rows.append(
            {
                "id": item["id"],
                "longctx_correctness": item.get("correctness"),
                "rag_correctness": (rag.get("correctness") or {}).get("score"),
                "longctx_seconds": item.get("seconds"),
                "rag_seconds": rag.get("seconds"),
            }
        )
    lc = [r["longctx_correctness"] for r in rows if r["longctx_correctness"] is not None]
    rc = [r["rag_correctness"] for r in rows if r["rag_correctness"] is not None]
    return {
        "rag_run": rag_run,
        "n": len(rows),
        "longctx_mean_correctness": round(sum(lc) / len(lc), 3) if lc else None,
        "rag_mean_correctness": round(sum(rc) / len(rc), 3) if rc else None,
        "longctx_mean_seconds": round(sum(r["longctx_seconds"] for r in rows if r["longctx_seconds"]) / len(rows), 1) if rows else None,
        "rows": rows,
    }


@app.command(name="run")
def run_experiment(n: int = 8, seed: int = 13, rag_run: str = "07_best_combo") -> None:
    """Run the long-context experiment on `n` single_hop questions."""
    from rag_tutorial.evaluate import judge_correctness  # noqa: PLC0415

    items = sample_single_hop(n=n, seed=seed)
    out_items = []
    for item in items:
        paper = item["evidence"][0]["paper"]
        answer, truncated, seconds = answer_long_context(item["question"], paper)
        verdict = judge_correctness(item["question"], item["answer"], answer)
        out_items.append(
            {
                "id": item["id"],
                "paper": paper,
                "question": item["question"],
                "answer": answer,
                "truncated": truncated,
                "correctness": verdict["score"],
                "seconds": round(seconds, 1),
            }
        )
        console.print(f"{item['id']}: correctness={verdict['score']} s={seconds:.0f}s truncated={truncated}")
    run_dir = RUNS_DIR / EXPERIMENT
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "predictions.json").write_text(json.dumps(out_items, indent=2, ensure_ascii=False))
    comparison = compare_against_rag({"items": out_items}, rag_run=rag_run)
    (run_dir / "metrics.json").write_text(json.dumps(comparison, indent=2))
    console.print(f"[green]wrote[/green] {run_dir}/metrics.json")
    console.print(json.dumps({k: v for k, v in comparison.items() if k != "rows"}, indent=2))


if __name__ == "__main__":
    app()
