"""The shared evaluator: retrieval metrics, LLM judges, and `evaluate_run`.

Every later chapter calls `evaluate_run` the same way, so every experiment's
`runs/<name>/metrics.json` has the same columns and can go on one scoreboard
(`project/runs/scoreboard.md`, built by `scoreboard.py`). Nothing in this
module may change its metric *definitions* after chapter 02 — a bug fix is
allowed, but it must be called out (and the anchors re-run) in whatever
chapter makes the fix.

Call contract used by `evaluate_run` (fixed here for every later chapter):
- `retrieve_fn(item: dict) -> list[Chunk]` — `item` is one golden-set row
  (`question`, `evidence`, `type`, ...); most retrievers only look at
  `item["question"]`, but the oracle anchor below needs `item["evidence"]`.
- `answer_fn(item: dict, retrieved: list[Chunk]) -> (answer: str, contexts: list[str], n_llm_calls: int)`
  — `contexts` are the exact strings the generator put in the prompt (used by
  `judge_faithfulness`); `n_llm_calls` lets the scoreboard report cost.
"""

from __future__ import annotations

import json
import re
import time

import typer
from rich.console import Console

from rag_tutorial.config import settings
from rag_tutorial.golden import QA_PATH, load_qa
from rag_tutorial.llm import ollama
from rag_tutorial.schema import Chunk

app = typer.Typer(add_completion=False)
console = Console()

RUNS_DIR = settings.path("runs")

_WORD_RE = re.compile(r"\w+")
_WHITESPACE_RE = re.compile(r"\s+")

# A chunk counts as covering an evidence quote if it contains at least this
# fraction of the quote's (lowercased) word tokens.
RELEVANCE_TOKEN_OVERLAP = 0.8


def _normalize(text: str) -> str:
    return _WHITESPACE_RE.sub(" ", text).strip().lower()


def _tokens(text: str) -> set[str]:
    return set(_WORD_RE.findall(text.lower()))


def chunk_covers_quote(chunk: Chunk, evidence: dict) -> bool:
    """A chunk is "relevant" to one evidence item if it is from the same paper and

    either (a) the quote is an exact normalised substring of the chunk text, or
    (b) at least `RELEVANCE_TOKEN_OVERLAP` of the quote's word tokens are
    present in the chunk's token set.

    We use both checks rather than just (b) because token-set overlap alone
    would call a chunk "relevant" even if the quote's words are scattered
    across unrelated sentences in a long chunk; the substring check catches
    the common case (the quote is literally inside the chunk) cheaply and
    exactly, and the token-overlap check catches the case where a chunk
    boundary lands in the middle of the quote (e.g. one extra trailing word
    cut off) so a strict substring match would be too harsh.
    """
    if chunk.paper != evidence["paper"]:
        return False
    if _normalize(evidence["quote"]) in _normalize(chunk.text):
        return True
    quote_tokens = _tokens(evidence["quote"])
    if not quote_tokens:
        return False
    overlap = len(quote_tokens & _tokens(chunk.text)) / len(quote_tokens)
    return overlap >= RELEVANCE_TOKEN_OVERLAP


def retrieval_metrics(
    retrieved_chunks: list[Chunk], evidence: list[dict], ks: tuple[int, ...] = (5, 10), ndcg_ks: tuple[int, ...] | None = None
) -> dict:
    """hit@k, recall@k, MRR and nDCG@k of `retrieved_chunks` against `evidence`.

    - hit@k: 1 if at least one evidence quote is covered by a chunk in the
      top k, else 0 (0 if there is no evidence, e.g. unanswerable questions —
      caller should exclude those from averages).
    - recall@k: fraction of evidence quotes covered by *some* chunk in the top k.
    - MRR: 1 / rank of the first chunk (over the whole ranked list) that
      covers any evidence quote; 0 if none does.
    - nDCG@k: chunks are graded 1 if they cover >=1 evidence quote else 0;
      normalised by the ideal ordering (all relevant chunks first). Computed
      for every `k` in `ndcg_ks` (defaults to `ks`, so `ndcg@10` is always
      present when 10 is in `ks`, unchanged from chapters 02-04); chapter 05's
      retrieval-only k-sweep passes `ks=ndcg_ks=(1, 3, 5, 10, 20)`.
    """
    ndcg_ks = ndcg_ks if ndcg_ks is not None else ks
    if not evidence:
        return (
            {f"hit@{k}": 0.0 for k in ks}
            | {f"recall@{k}": 0.0 for k in ks}
            | {"mrr": 0.0}
            | {f"ndcg@{k}": 0.0 for k in ndcg_ks}
        )

    relevance = [any(chunk_covers_quote(chunk, ev) for ev in evidence) for chunk in retrieved_chunks]

    result: dict = {}
    for k in ks:
        top_k = relevance[:k]
        result[f"hit@{k}"] = 1.0 if any(top_k) else 0.0
        covered = {
            i
            for i, ev in enumerate(evidence)
            for chunk in retrieved_chunks[:k]
            if chunk_covers_quote(chunk, ev)
        }
        result[f"recall@{k}"] = len(covered) / len(evidence)

    rr = 0.0
    for rank, is_relevant in enumerate(relevance, start=1):
        if is_relevant:
            rr = 1.0 / rank
            break
    result["mrr"] = rr

    for k in ndcg_ks:
        top_k = relevance[:k]
        dcg = sum(rel / _log2(i + 1) for i, rel in enumerate(top_k, start=1) if rel)
        n_relevant = min(sum(relevance), k)
        idcg = sum(1.0 / _log2(i + 1) for i in range(1, n_relevant + 1))
        result[f"ndcg@{k}"] = (dcg / idcg) if idcg > 0 else 0.0

    return result


def _log2(x: float) -> float:
    import math

    return math.log2(x)


# -- LLM judges ----------------------------------------------------------------------

_CORRECTNESS_SCHEMA = {
    "type": "object",
    "properties": {
        "score": {"type": "number", "enum": [0, 0.5, 1]},
        "reason": {"type": "string"},
    },
    "required": ["score", "reason"],
}

_CLAIMS_SCHEMA = {
    "type": "object",
    "properties": {"claims": {"type": "array", "items": {"type": "string"}}},
    "required": ["claims"],
}

_SUPPORT_SCHEMA = {
    "type": "object",
    "properties": {
        "results": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"claim": {"type": "string"}, "supported": {"type": "boolean"}},
                "required": ["claim", "supported"],
            },
        }
    },
    "required": ["results"],
}

_ABSTAIN_SCHEMA = {
    "type": "object",
    "properties": {"abstain": {"type": "boolean"}, "reason": {"type": "string"}},
    "required": ["abstain", "reason"],
}


def judge_correctness(question: str, reference: str, answer: str, client=None, seed: int = 42) -> dict:
    """Score `answer` against `reference` on a 0 / 0.5 / 1 scale via the chat model.

    0 = wrong or missing the key fact, 0.5 = partially correct, 1 = correct.
    `seed` is exposed for the chapter-13 stability audit; the default (42)
    reproduces the exact cache keys of all earlier runs.
    """
    client = client or ollama
    prompt = (
        f"Question: {question}\nReference answer: {reference}\nModel's answer: {answer}\n\n"
        "Score the model's answer against the reference on this scale: 1 = correct and "
        "complete, 0.5 = partially correct or missing some of the reference, 0 = wrong or "
        "does not answer the question. Give a one-sentence reason."
    )
    reply = client.chat(
        [{"role": "system", "content": "You are a strict grader for a RAG benchmark. Reply with JSON only."}, {"role": "user", "content": prompt}],
        json_schema=_CORRECTNESS_SCHEMA,
        temperature=0,
        seed=seed,
        max_tokens=256,
    )
    data = json.loads(reply)
    return {"score": float(data["score"]), "reason": data["reason"]}


def judge_faithfulness(answer: str, contexts: list[str], client=None) -> dict:
    """RAGAS-style faithfulness: split `answer` into atomic claims, then check each

    against `contexts`. Returns `{supported, total, score, unsupported_claims}`.
    An answer with no claims (e.g. an empty or refusal answer) gets score 1.0
    and `total=0` — there is nothing unsupported to penalise.

    Chapter 03 bug fix: `max_tokens` for the two internal chat calls was 512/1024,
    too small once retrieval widens (e.g. k=10 on a `global` question) and the
    generator writes a long, multi-paper answer — the claims list got cut off
    mid-JSON-string and `json.loads` raised. Raised to 1536/2048 (implementation
    detail, not a metric-definition change); the 02 anchors were re-run after
    this fix since it changes `ollama.chat`'s cache key (`num_predict`).
    """
    client = client or ollama
    claims_reply = client.chat(
        [
            {"role": "system", "content": "Split the answer into a list of short, atomic factual claims. Reply with JSON only."},
            {"role": "user", "content": f"Answer:\n{answer}"},
        ],
        json_schema=_CLAIMS_SCHEMA,
        temperature=0,
        max_tokens=3072,
    )
    claims = json.loads(claims_reply)["claims"]
    if not claims:
        return {"supported": 0, "total": 0, "score": 1.0, "unsupported_claims": []}

    context_block = "\n\n".join(f"[{i}] {c}" for i, c in enumerate(contexts))
    claims_block = "\n".join(f"- {c}" for c in claims)
    support_reply = client.chat(
        [
            {
                "role": "system",
                "content": "For each claim, decide if it is directly supported by the contexts. Reply with JSON only.",
            },
            {"role": "user", "content": f"Contexts:\n{context_block}\n\nClaims:\n{claims_block}"},
        ],
        json_schema=_SUPPORT_SCHEMA,
        temperature=0,
        max_tokens=4096,
    )
    results = json.loads(support_reply)["results"]
    supported = sum(1 for r in results if r["supported"])
    total = len(results)
    unsupported = [r["claim"] for r in results if not r["supported"]]
    return {"supported": supported, "total": total, "score": supported / total if total else 1.0, "unsupported_claims": unsupported}


def judge_abstain(question: str, answer: str, client=None) -> dict:
    """For `unanswerable` questions: 1 if `answer` correctly declines to answer."""
    client = client or ollama
    prompt = (
        f"Question: {question}\nModel's answer: {answer}\n\n"
        "This question is not answerable from the documents. Does the model's answer correctly "
        "recognise that it cannot be answered (abstain), rather than guessing or hallucinating "
        "a specific answer?"
    )
    reply = client.chat(
        [{"role": "system", "content": "Reply with JSON only."}, {"role": "user", "content": prompt}],
        json_schema=_ABSTAIN_SCHEMA,
        temperature=0,
        max_tokens=200,
    )
    data = json.loads(reply)
    return {"abstain": 1.0 if data["abstain"] else 0.0, "reason": data["reason"]}


# -- the shared run loop --------------------------------------------------------------


def evaluate_run(
    name: str,
    chapter: str,
    answer_fn,
    retrieve_fn,
    split: str = "test",
    limit: int | None = None,
    judge_client=None,
) -> dict:
    """Run every golden-set question of `split` through `retrieve_fn`/`answer_fn`,

    judge the answers, and write `runs/<name>/{metrics.json,predictions.jsonl,config.json}`.
    Returns the metrics dict. `limit` truncates the question list for smoke runs.
    """
    items = [item for item in load_qa(QA_PATH) if item["split"] == split]
    if limit is not None:
        items = items[:limit]

    run_dir = RUNS_DIR / name
    run_dir.mkdir(parents=True, exist_ok=True)

    predictions = []
    retrieval_rows = []
    correctness_scores = []
    faithfulness_scores = []
    abstain_scores = []
    llm_calls = []
    seconds = []

    for item in items:
        start = time.monotonic()
        retrieved = retrieve_fn(item)
        answer, contexts, n_llm_calls = answer_fn(item, retrieved)
        elapsed = time.monotonic() - start

        r_metrics = retrieval_metrics(retrieved, item["evidence"])
        if item["evidence"]:
            retrieval_rows.append(r_metrics)

        faithfulness = judge_faithfulness(answer, contexts, client=judge_client) if contexts else {"score": 1.0, "supported": 0, "total": 0, "unsupported_claims": []}
        faithfulness_scores.append(faithfulness["score"])

        if item["type"] == "unanswerable":
            abstain = judge_abstain(item["question"], answer, client=judge_client)
            abstain_scores.append(abstain["abstain"])
            correctness = None
        else:
            correctness = judge_correctness(item["question"], item["answer"], answer, client=judge_client)
            correctness_scores.append(correctness["score"])
            abstain = None

        llm_calls.append(n_llm_calls)
        seconds.append(elapsed)

        predictions.append(
            {
                "id": item["id"],
                "type": item["type"],
                "question": item["question"],
                "answer": answer,
                "retrieved_chunk_ids": [c.id for c in retrieved],
                "retrieval_metrics": r_metrics,
                "correctness": correctness,
                "faithfulness": faithfulness,
                "abstain": abstain,
                "n_llm_calls": n_llm_calls,
                "seconds": round(elapsed, 3),
            }
        )

    def _mean(xs: list[float]) -> float | None:
        return sum(xs) / len(xs) if xs else None

    metrics = {
        "experiment": name,
        "chapter": chapter,
        "split": split,
        "n_questions": len(items),
        "hit@5": _mean([r["hit@5"] for r in retrieval_rows]),
        "recall@5": _mean([r["recall@5"] for r in retrieval_rows]),
        "hit@10": _mean([r["hit@10"] for r in retrieval_rows]),
        "recall@10": _mean([r["recall@10"] for r in retrieval_rows]),
        "mrr": _mean([r["mrr"] for r in retrieval_rows]),
        "ndcg@10": _mean([r["ndcg@10"] for r in retrieval_rows]),
        "correctness": _mean(correctness_scores),
        "faithfulness": _mean(faithfulness_scores),
        "unanswerable_abstain": _mean(abstain_scores),
        "llm_calls_per_q": _mean(llm_calls),
        "seconds_per_q": _mean(seconds),
        "details": {"cache_stats": ollama.stats.as_dict() if judge_client is None else {}},
    }

    (run_dir / "metrics.json").write_text(json.dumps(metrics, indent=2))
    with (run_dir / "predictions.jsonl").open("w") as f:
        for row in predictions:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    (run_dir / "config.json").write_text(
        json.dumps({"name": name, "chapter": chapter, "split": split, "limit": limit, "chat_model": settings.chat_model, "embed_model": settings.embed_model}, indent=2)
    )

    console.print(f"[green]wrote[/green] {run_dir}/metrics.json ({len(items)} questions)")
    return metrics


# -- the two chapter-02 anchors --------------------------------------------------------


def _no_retrieval_answer(item: dict, _retrieved: list[Chunk]) -> tuple[str, list[str], int]:
    answer = ollama.chat(
        [
            {
                "role": "system",
                "content": "Answer the question briefly from your own knowledge. If you do not know or are not sure, say so plainly.",
            },
            {"role": "user", "content": item["question"]},
        ],
        max_tokens=256,
    )
    return answer, [], 1


def _no_retrieve(_item: dict) -> list[Chunk]:
    return []


def _oracle_retrieve(item: dict) -> list[Chunk]:
    """"Retrieve" the gold evidence quotes themselves — the upper bound on

    generation quality, since retrieval cannot fail if it is skipped entirely.
    """
    return [
        Chunk(id=f"oracle-{item['id']}-{i}", paper=ev["paper"], section="", text=ev["quote"], start=0, end=len(ev["quote"]))
        for i, ev in enumerate(item["evidence"])
    ]


def _oracle_answer(item: dict, retrieved: list[Chunk]) -> tuple[str, list[str], int]:
    if not retrieved:
        answer = ollama.chat(
            [
                {
                    "role": "system",
                    "content": "Answer briefly. If you do not know or are not sure, say so plainly.",
                },
                {"role": "user", "content": item["question"]},
            ],
            max_tokens=256,
        )
        return answer, [], 1
    contexts = [f"[{c.paper}] {c.text}" for c in retrieved]
    context_block = "\n\n".join(contexts)
    answer = ollama.chat(
        [
            {
                "role": "system",
                "content": "Answer the question using only the given excerpts from papers, citing the paper id. If the excerpts are not enough, say so.",
            },
            {"role": "user", "content": f"Excerpts:\n{context_block}\n\nQuestion: {item['question']}"},
        ],
        max_tokens=384,
    )
    return answer, contexts, 1


@app.command(name="no-retrieval")
def anchor_no_retrieval(limit: int | None = None) -> None:
    """Anchor `02_no_retrieval`: the LLM answers from memory alone, no retrieval."""
    evaluate_run("02_no_retrieval", chapter="02", answer_fn=_no_retrieval_answer, retrieve_fn=_no_retrieve, split="test", limit=limit)


@app.command(name="oracle")
def anchor_oracle(limit: int | None = None) -> None:
    """Anchor `02_oracle`: the LLM gets the gold evidence quotes as context (upper bound)."""
    evaluate_run("02_oracle", chapter="02", answer_fn=_oracle_answer, retrieve_fn=_oracle_retrieve, split="test", limit=limit)


if __name__ == "__main__":
    app()
