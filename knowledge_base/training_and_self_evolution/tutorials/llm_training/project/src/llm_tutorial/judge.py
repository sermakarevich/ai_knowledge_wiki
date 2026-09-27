"""Chapter 08 — LLM-as-judge: score one open-ended answer against a reference, 1-5, using the
local `qwen3.8:27b` through Ollama's `/api/chat` with a JSON-schema-constrained reply (same
pattern as the `graph_rag` tutorial's `chat_json`): `think: false`, `temperature: 0`.

Position-bias note: this judge only ever sees ONE candidate answer at a time (question +
reference + candidate), never a pair of candidates to rank against each other. That sidesteps
position bias (favouring whichever answer is shown first/second) entirely, at the cost of not
being able to directly compare two models' phrasing — only their scores against the same
reference. Verbosity bias (rewarding longer answers) and self-preference bias (a model favouring
its own style of answer) are NOT eliminated by this design; the chapter names them as open
caveats, not solved problems.
"""

import json
from pathlib import Path

import httpx
import typer
import yaml
from pydantic import BaseModel, Field
from rich.console import Console
from rich.table import Table

app = typer.Typer(add_completion=False, help=__doc__)
console = Console()

DEFAULT_OLLAMA_URL = "http://127.0.0.1:11434"
DEFAULT_JUDGE_MODEL = "qwen3.8:27b"

JUDGE_SYSTEM = """You are grading one candidate answer to a cybersecurity question against a \
known-correct reference answer. Score the candidate 1-5:
1 = wrong or contradicts the reference
2 = mostly wrong, touches the right topic
3 = partially correct, missing key points or containing a real error
4 = correct and complete, minor phrasing issues only
5 = fully correct and matches the reference's meaning
Output ONLY JSON matching the given schema. `verdict` is "correct" if score >= 4, else "incorrect"."""


class Verdict(BaseModel):
    score: int = Field(ge=1, le=5)
    verdict: str = Field(description='"correct" or "incorrect"')
    reason: str = Field(description="one sentence explaining the score")


def build_judge_messages(question: str, reference: str, candidate: str) -> list[dict]:
    """The `{"role", "content"}` messages sent to the judge model (pure, unit-tested)."""
    user = (
        f"Question: {question}\n\n"
        f"Reference answer: {reference}\n\n"
        f"Candidate answer: {candidate}"
    )
    return [{"role": "system", "content": JUDGE_SYSTEM}, {"role": "user", "content": user}]


def parse_verdict(content: str) -> Verdict:
    """Parse the judge model's raw JSON reply into a `Verdict` (pure, unit-tested with canned
    strings — no network)."""
    return Verdict.model_validate_json(content)


def judge(
    question: str,
    reference: str,
    candidate: str,
    model: str = DEFAULT_JUDGE_MODEL,
    url: str = DEFAULT_OLLAMA_URL,
    timeout: float = 120.0,
) -> dict:
    """Call the judge model over `POST {url}/api/chat` and return `{score, verdict, reason}`."""
    messages = build_judge_messages(question, reference, candidate)
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "think": False,
        "format": Verdict.model_json_schema(),
        "options": {"temperature": 0},
    }
    resp = httpx.post(f"{url}/api/chat", json=payload, timeout=timeout)
    resp.raise_for_status()
    content = resp.json()["message"]["content"]
    verdict = parse_verdict(content)
    return verdict.model_dump()


def judge_pairs(items: list[dict], model: str = DEFAULT_JUDGE_MODEL, url: str = DEFAULT_OLLAMA_URL) -> dict:
    """Judge a list of `{"question", "reference", "candidate"}` dicts and summarise
    `{n, mean_score, records}`."""
    records = []
    for item in items:
        verdict = judge(item["question"], item["reference"], item["candidate"], model=model, url=url)
        records.append({**item, **verdict})
    mean_score = sum(r["score"] for r in records) / len(records) if records else 0.0
    return {"n": len(records), "mean_score": mean_score, "records": records}


@app.command(name="answer-hf")
def answer_hf_cmd(
    model_dir: str = typer.Argument(..., help="a saved model dir or HF repo id"),
    judge_set: str = typer.Argument("configs/judge_set.yaml"),
    out_path: str = typer.Option(..., help="where to write the answers.json `judge run` needs"),
    max_new_tokens: int = typer.Option(256),
) -> None:
    """Generate one candidate answer per `judge_set` question from an HF checkpoint (greedy,
    temperature=0) and write `[{id, candidate}, ...]` to `out_path` — the file `judge run`'s
    `--answers` expects."""
    from transformers import AutoModelForCausalLM, AutoTokenizer

    from .chat import attach_chat_template, chat

    with open(judge_set) as f:
        questions = yaml.safe_load(f)["questions"]

    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    if tokenizer.chat_template is None:
        attach_chat_template(tokenizer)
    model = AutoModelForCausalLM.from_pretrained(model_dir).to("cuda").eval()

    answers = []
    for q in questions:
        reply = chat(
            model, tokenizer, [{"role": "user", "content": q["question"]}],
            max_new_tokens=max_new_tokens, temperature=0.0,
        )
        answers.append({"id": q["id"], "candidate": reply})

    with open(out_path, "w") as f:
        json.dump(answers, f, indent=2)
    console.print(f"wrote {len(answers)} answers to {out_path}")


@app.command()
def run(
    judge_set: str = typer.Argument("configs/judge_set.yaml"),
    answers: str = typer.Option(..., help="JSON file: list of {id, candidate}"),
    model: str = typer.Option(DEFAULT_JUDGE_MODEL),
    url: str = typer.Option(DEFAULT_OLLAMA_URL),
    run_dir: str = typer.Option(None, help="write {n, mean_score} into <run_dir>/metrics.json (default: answers' own directory)"),
) -> None:
    """Judge a set of candidate answers against `configs/judge_set.yaml`'s reference answers."""
    from .config import write_metrics

    with open(judge_set) as f:
        questions = yaml.safe_load(f)["questions"]
    with open(answers) as f:
        candidates_by_id = {row["id"]: row["candidate"] for row in json.load(f)}

    items = [
        {"question": q["question"], "reference": q["reference"], "candidate": candidates_by_id[q["id"]]}
        for q in questions
        if q["id"] in candidates_by_id
    ]
    result = judge_pairs(items, model=model, url=url)

    table = Table(title=f"judge ({model}) mean_score={result['mean_score']:.2f} n={result['n']}")
    table.add_column("score")
    table.add_column("verdict")
    table.add_column("reason")
    for record in result["records"]:
        table.add_row(str(record["score"]), record["verdict"], record["reason"])
    console.print(table)

    target_dir = run_dir or str(Path(answers).parent)
    write_metrics(target_dir, {"judge": {"n": result["n"], "mean_score": result["mean_score"]}})


if __name__ == "__main__":
    app()
