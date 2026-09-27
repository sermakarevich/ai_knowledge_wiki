"""Second-opinion evaluation with RAGAS (chapter 13).

RAGAS (Retrieval-Augmented Generation Assessment, an open-source library of
LLM-judged metrics for RAG pipelines) re-scores a sample of our runs with its
own judges, so we can check how much to trust our single in-house judge.

Metrics used (modern `ragas.metrics.collections` names in installed RAGAS
0.4.3; the spec's classic names map as ResponseRelevancy -> AnswerRelevancy,
LLMContextPrecisionWithReference -> ContextPrecisionWithReference,
LLMContextRecall -> ContextRecall — the legacy aliases belong to an older
class hierarchy that `evaluate()` refuses to mix with the new one):
- Faithfulness: are the answer's claims supported by the retrieved context?
- AnswerRelevancy: does the answer actually address the question?
- ContextPrecisionWithReference: of the retrieved chunks, how many are relevant?
- ContextRecall: of the gold evidence, how much did retrieval cover?
- FactualCorrectness: does the answer match the reference answer?

The RAGAS judges run on our local chat model (`qwen3.8:27b`, a 27-billion-
parameter language model served by Ollama on the `rtx` GPU box). The spec
suggested `langchain-ollama` wrappers, but installed RAGAS 0.4.3 rejects
both `LangchainLLMWrapper` and `LangchainEmbeddingsWrapper` for these
metrics ("collections metrics only support modern ..."), so both judges go
through the modern factories with OpenAI-compatible clients pointed at
Ollama's `/v1` endpoint (the approach the research note documents):
`llm_factory(chat_model, client=...)` and
`OpenAIEmbeddings(client=..., model="nomic-embed-text")`.

Two environment workarounds, both documented here rather than hidden:
1. RAGAS 0.4.3 does `from langchain_community.chat_models.vertexai import
   ChatVertexAI` at import time, but the installed `langchain-community`
   0.4.x removed that module. We insert a tiny stub into `sys.modules`
   before importing RAGAS; it is only ever used if someone asks for the
   VertexAI provider, which this tutorial never does.
2. `predictions.jsonl` stores retrieved *chunk ids*, not chunk texts. RAGAS
   needs the texts, so `build_id_to_text` resolves ids from (a) the on-disk
   Chroma index, (b) deterministically rebuilt fixed-512 and parent-800
   chunks (chunk ids hash paper+offsets, so rebuilds reproduce them
   exactly), and (c) the persisted LlamaIndex docstores (same id scheme).
   Ids that still do not resolve run answer-only metrics and are counted
   in `n_unresolved_contexts`.

RAGAS is known to struggle with small/local judges (its prompts demand
strict JSON, which `qwen3.8:27b` does not always obey). Every item records
per-metric success/failure; the output JSON reports the failure rate and
the `RunConfig` (`max_retries`, timeouts) used to mitigate it.
"""

from __future__ import annotations

import json
import random
import sys
import types
from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer(add_completion=False)
console = Console()

# -- workaround 1: stub the removed vertexai module before RAGAS imports it --
if "langchain_community.chat_models.vertexai" not in sys.modules:
    try:
        import langchain_community.chat_models.vertexai  # noqa: F401
    except ImportError:
        _stub = types.ModuleType("langchain_community.chat_models.vertexai")

        class _ChatVertexAI:  # pragma: no cover - never instantiated here
            def __init__(self, *args, **kwargs):
                raise ImportError("ChatVertexAI is not available in this tutorial environment.")

        _stub.ChatVertexAI = _ChatVertexAI
        sys.modules["langchain_community.chat_models.vertexai"] = _stub


def _import_metric(name: str):
    """Import a RAGAS metric by name from the modern `collections` location."""
    collections = __import__("ragas.metrics.collections", fromlist=[name])
    return getattr(collections, name)


# Installed RAGAS 0.4.3 renamed the classic metrics; the old aliases
# (ResponseRelevancy, LLMContextPrecisionWithReference, LLMContextRecall)
# still import from `ragas.metrics` but belong to the legacy class
# hierarchy, and `evaluate()` refuses a mix of old + new metric objects —
# so we use the modern names exclusively. Mapping to the spec's names:
# ResponseRelevancy -> AnswerRelevancy,
# LLMContextPrecisionWithReference -> ContextPrecisionWithReference,
# LLMContextRecall -> ContextRecall.
METRIC_NAMES = [
    "Faithfulness",
    "AnswerRelevancy",
    "ContextPrecisionWithReference",
    "ContextRecall",
    "FactualCorrectness",
]

REP_RUNS = [
    "03_naive_fixed_512_k5",
    "07_best_combo",
    "08_lg_crag",
    "09_li_fusion_rerank",
    "11_lightrag_hybrid",
]


def build_id_to_text() -> dict[str, str]:
    """Map chunk id -> text for resolving `predictions.jsonl` chunk ids.

    Two sources, no LLM calls:
    1. The on-disk Chroma index (`data/indexes/chroma`, gitignored but
       present on this machine): every indexed collection's documents.
       This covers parent-swapped runs (ch05/ch07) whose ids are not
       plain fixed-512 chunks.
    2. Fallback: deterministically rebuild fixed-512 chunks (chapter 03
       settings — chunk ids hash paper+offsets, so the rebuild reproduces
       them exactly).
    Ids from runs with foreign chunking (LlamaIndex nodes, LightRAG) still
    do not resolve; those items run answer-only metrics and are counted.
    """
    mapping: dict[str, str] = {}
    try:
        import chromadb

        from rag_tutorial.config import settings as _settings

        client = chromadb.PersistentClient(path=str(_settings.path("data/indexes/chroma")))
        for coll in client.list_collections():
            data = coll.get(include=["documents"])
            for cid, doc in zip(data["ids"], data["documents"] or [], strict=False):
                if doc:
                    mapping.setdefault(cid, doc)
    except Exception:
        pass
    try:
        from rag_tutorial.chunkers import fixed_token_chunks, parent_chunks
        from rag_tutorial.golden import load_documents

        for doc in load_documents().values():
            for chunk in fixed_token_chunks(doc, size=512, overlap=64):
                mapping.setdefault(chunk.id, chunk.text)
            # chapter 05/07 swap child hits for these larger parents (800/100)
            for chunk in parent_chunks(doc, size=800, overlap=100):
                mapping.setdefault(chunk.id, chunk.text)
    except Exception:
        pass
    try:
        # LlamaIndex runs keep deterministic `chunk_id(paper, start, end)`
        # ids; the node texts live in the persisted docstores (gitignored
        # but present on this machine).
        import glob as _glob

        from rag_tutorial.config import settings as _settings2
        from rag_tutorial.schema import chunk_id

        for docstore_path in _glob.glob(str(_settings2.path("data/indexes/li_*/docstore.json"))):
            try:
                store = json.loads(Path(docstore_path).read_text())
            except (OSError, ValueError):
                continue
            for node in store.get("docstore/data", {}).values():
                inner = node.get("__data__", node)
                meta = inner.get("metadata") or {}
                paper = meta.get("paper") or ""
                start, end = inner.get("start_char_idx"), inner.get("end_char_idx")
                text = inner.get("text") or ""
                if paper and start is not None and end is not None and text:
                    try:
                        mapping.setdefault(chunk_id(paper, int(start), int(end)), text)
                    except (TypeError, ValueError):
                        pass
    except Exception:
        pass
    return mapping


def load_items(run: str, limit: int | None = None, seed: int = 13) -> list[dict]:
    """Join one run's predictions with golden references for RAGAS input.

    Items are deterministically shuffled (`seed`) before `limit` truncates,
    so a slice covers all question types instead of just the first N.
    """
    from rag_tutorial.config import settings
    from rag_tutorial.golden import QA_PATH, load_qa

    runs_dir = settings.path("runs")
    preds = [json.loads(line) for line in (runs_dir / run / "predictions.jsonl").read_text().splitlines() if line.strip()]
    rng = random.Random(seed)
    rng.shuffle(preds)
    gold = {item["id"]: item for item in load_qa(QA_PATH)}
    id_to_text = build_id_to_text()
    items = []
    for pred in preds:
        item = gold.get(pred["id"])
        if item is None:
            continue
        contexts, unresolved = [], 0
        for cid in pred.get("retrieved_chunk_ids", []):
            text = id_to_text.get(cid)
            if text is None:
                unresolved += 1
            else:
                contexts.append(f"[{cid[:8]}] {text}")
        items.append(
            {
                "id": pred["id"],
                "question": pred["question"],
                "answer": pred.get("answer", ""),
                "reference": item.get("answer", ""),
                "reference_contexts": [ev["quote"] for ev in item.get("evidence", [])],
                "retrieved_contexts": contexts,
                "n_unresolved": unresolved,
                "ours_correctness": (pred.get("correctness") or {}).get("score"),
                "ours_faithfulness": (pred.get("faithfulness") or {}).get("score"),
            }
        )
        if limit is not None and len(items) >= limit:
            break
    return items


def make_judges(timeout: int = 180, max_retries: int = 3, max_workers: int = 2):
    """Build the RAGAS LLM + embeddings judges on the local Ollama models.

    Installed RAGAS (0.4.3) "collections" metrics reject
    `LangchainLLMWrapper` ("only support modern InstructorLLM"), so the LLM
    goes through `llm_factory` with an OpenAI-compatible client pointed at
    Ollama's `/v1` endpoint (the approach the research note documents).
    Embeddings likewise go through RAGAS's modern `OpenAIEmbeddings` with
    model `nomic-embed-text` on the same endpoint (`LangchainEmbeddingsWrapper`
    is rejected the same way).
    """
    from rag_tutorial.config import settings

    try:
        from ragas.run_config import RunConfig
    except ImportError:  # older RAGAS layout
        from ragas.utils import RunConfig  # type: ignore[no-redef]
    from ragas.embeddings import OpenAIEmbeddings
    from ragas.llms import llm_factory

    import openai

    # Async client: collections metrics score via `agenerate()` and refuse a
    # synchronous client outright.
    client = openai.AsyncOpenAI(base_url=f"{settings.ollama_url}/v1", api_key="ollama")
    llm = llm_factory(settings.chat_model, client=client)
    run_config = RunConfig(timeout=timeout, max_retries=max_retries, max_workers=max_workers)
    embeddings = OpenAIEmbeddings(client=client, model=settings.embed_model)
    return llm, embeddings, {"timeout": timeout, "max_retries": max_retries, "max_workers": max_workers}


def _metric_kwargs(name: str, item: dict) -> dict | None:
    """Kwargs for one metric's `ascore()`; None when inputs are missing.

    Context metrics need resolved retrieved contexts; without them the item
    keeps answer-only metrics (counted as a skip, not a failure).
    """
    q, a, ref, ctx = item["question"], item["answer"], item["reference"], item["retrieved_contexts"]
    if name == "Faithfulness":
        return {"user_input": q, "response": a, "retrieved_contexts": ctx} if ctx and a else None
    if name == "AnswerRelevancy":
        return {"user_input": q, "response": a} if a else None
    if name == "ContextPrecisionWithReference":
        return {"user_input": q, "reference": ref, "retrieved_contexts": ctx} if ctx and ref else None
    if name == "ContextRecall":
        return {"user_input": q, "retrieved_contexts": ctx, "reference": ref} if ctx and ref else None
    if name == "FactualCorrectness":
        return {"response": a, "reference": ref} if a and ref else None
    raise KeyError(name)


async def _score_one(metric, kwargs: dict, timeout: int):
    """Score one (metric, item); return None on any failure (parse/timeout/LLM)."""
    import asyncio

    try:
        result = await asyncio.wait_for(metric.ascore(**kwargs), timeout=timeout)
        value = result.value if hasattr(result, "value") else result
        score = float(value.get("value", value) if isinstance(value, dict) else value)
        return score if score == score and 0.0 <= score <= 1.5 else None
    except Exception:
        return None


async def _score_items(metrics: list, items: list[dict], timeout: int) -> list[dict]:
    """Score every item sequentially (one LLM call at a time — shared GPU)."""
    scored = []
    for item in items:
        entry = {"id": item["id"], "n_unresolved": item["n_unresolved"]}
        for metric, name in zip(metrics, METRIC_NAMES, strict=True):
            kwargs = _metric_kwargs(name, item)
            if kwargs is None:
                entry[name] = None
                entry[f"{name}_skipped"] = True
                continue
            entry[name] = await _score_one(metric, kwargs, timeout)
        entry["ours_correctness"] = item["ours_correctness"]
        entry["ours_faithfulness"] = item["ours_faithfulness"]
        scored.append(entry)
    return scored


def run_ragas(
    runs: list[str] | None = None,
    limit: int | None = None,
    output: str | Path | None = None,
    timeout: int = 300,
    max_retries: int = 3,
) -> dict:
    """Score `limit` questions of each run with the five RAGAS metrics.

    Scoring goes metric-by-metric via each metric's `ascore()` (installed
    RAGAS 0.4.3 removed `evaluate()` support for these metrics). Returns the
    result dict and writes it to `runs/13_ragas.json` (default). Items whose
    chunk ids did not resolve get answer-only metrics; context metrics are
    null there (`*_skipped`). Per-metric failures (usually the local judge's
    malformed JSON) are null and counted in `failure_rate`.
    """
    import asyncio

    from rag_tutorial.config import settings

    runs = runs or list(REP_RUNS)
    llm, embeddings, judge_cfg = make_judges(timeout=timeout, max_retries=max_retries)
    metrics = []
    for name in METRIC_NAMES:
        cls = _import_metric(name)
        try:
            metrics.append(cls(llm=llm, embeddings=embeddings))
        except TypeError:
            metrics.append(cls(llm=llm))

    result: dict = {"runs": {}, "judge": judge_cfg, "metric_names": METRIC_NAMES}
    for run in runs:
        items = load_items(run, limit=limit)
        try:
            scored = asyncio.run(_score_items(metrics, items, timeout))
        except Exception as exc:  # whole-run failure (e.g. judge unreachable)
            result["runs"][run] = {"error": f"{type(exc).__name__}: {exc}", "items": []}
            continue
        n_ok = sum(1 for e in scored for name in METRIC_NAMES if e.get(name) is not None)
        n_applicable = sum(
            1 for e in scored for name in METRIC_NAMES if not e.get(f"{name}_skipped", False)
        )
        result["runs"][run] = {
            "n_items": len(scored),
            "n_unresolved_contexts": sum(e["n_unresolved"] for e in scored),
            "failure_rate": 1 - n_ok / n_applicable if n_applicable else None,
            "items": scored,
        }
        console.print(f"[green]scored[/green] {run}: {len(scored)} items")

    out = Path(output) if output else settings.path("runs") / "13_ragas.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2))
    console.print(f"[green]wrote[/green] {out}")
    return result


@app.command(name="run-all")
def run_all(
    run_name: list[str] = typer.Option(None, "--run", help="Run(s) to score; default: the five representative runs."),
    limit: int | None = typer.Option(None, "--limit", help="Max questions per run (omit for all)."),
    output: str | None = typer.Option(None, "--output", help="Output JSON path."),
    timeout: int = typer.Option(300, "--timeout"),
    max_retries: int = typer.Option(3, "--max-retries"),
) -> None:
    """Score representative runs with RAGAS -> runs/13_ragas.json."""
    run_ragas(runs=run_name or None, limit=limit, output=output, timeout=timeout, max_retries=max_retries)


if __name__ == "__main__":
    app()
