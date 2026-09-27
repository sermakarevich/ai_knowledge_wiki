"""Chapter 10 (part 2) — RAG as a DSPy *program* with optimised prompts.

DSPy (Stanford NLP) is the programming-instead-of-prompting framework: you
write compositional Python (`dspy.Module` + `dspy.Signature`) and an
*optimizer* (teleprompter) rewrites the instructions and few-shot demos to
maximise a metric. Retrieval itself is "just Python you plug in" (per DSPy's
own RAG tutorial) — so our chapter-07 best retriever (hybrid RRF child
pool, k_each=20 + bge-reranker-v2-m3 cross-encoder rerank + parent swap,
k=5) runs as a plain function inside `forward()`.

What this module adds:
- `RAG(dspy.Module)` with `dspy.ChainOfThought("context, question -> answer")`.
- Row `10_dspy_zero_shot`: the program with no optimisation.
- Metric: cheap token-F1 between prediction and reference (NOT our LLM
  judge) inside the optimiser — the judge needs ~3 LLM calls per example,
  which would blow the <=400-call optimiser budget; final test-set scoring
  still uses `evaluate_run` with our real judges. Said explicitly, as specced.
- Optimisers on the dev split (9 questions — small on purpose, overfitting
  risk noted): `dspy.BootstrapFewShot` (cheap) -> row
  `10_dspy_bootstrap`; `dspy.MIPROv2(auto="light")` -> row
  `10_dspy_mipro`. Optimised programs saved as JSON (`program.save(...)`);
  LLM calls used by optimisation counted via `len(lm.history)`.
- Optional `dspy.Refine`/citation assertions: SKIPPED (budget) — the shared
  prompt already demands `[short_name]` citations; noted in findings.

DSPy LM: `dspy.LM("ollama_chat/qwen3.8:27b", api_base=<ollama_url>,
temperature=0, max_tokens=384, cache=True)` (LiteLLM `ollama_chat/`
convention). `data/cache/dspy/` holds the saved programs (and is the
documented DSPy cache dir for this tutorial; DSPy's own `cache=True`
response cache is in-process).

Overfitting warning: dev has only ~9 questions, so both optimisers can
memorise few-shot demos; test-set numbers are the honest ones.

Run:
    uv run --group dspy python -m rag_tutorial.fw_dspy baseline
    uv run --group dspy python -m rag_tutorial.fw_dspy optimize
    uv run --group dspy python -m rag_tutorial.fw_dspy eval
"""

from __future__ import annotations

import json
import os
import re
import time
from functools import lru_cache

import typer
from rich.console import Console

from rag_tutorial.baseline import _short_names
from rag_tutorial.config import settings
from rag_tutorial.evaluate import RUNS_DIR, evaluate_run
from rag_tutorial.golden import QA_PATH, load_qa
from rag_tutorial.schema import Chunk

app = typer.Typer(add_completion=False)
console = Console()

DSPY_CACHE_DIR = settings.path("data/cache/dspy")
K = 5

import dspy  # noqa: E402  (the `dspy` uv group; keep AFTER the rag_tutorial
# imports above: `import dspy` first breaks numpy for later chromadb imports
# (TypeError: data type 'bool' not understood). `python -m` entry points are
# safe; `python -c "import dspy; from rag_tutorial import fw_dspy"` is not.)


# ---------------------------------------------------------------------------
# LM singleton
# ---------------------------------------------------------------------------


def get_lm() -> dspy.LM:
    """Ollama chat LM for DSPy (LiteLLM `ollama_chat/` convention)."""
    DSPY_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return dspy.LM(
        f"ollama_chat/{settings.chat_model}",
        api_base=settings.ollama_url,
        api_key="",
        temperature=0,
        # 4096: ChainOfThought emits long `reasoning` BEFORE `answer` from
        # the same budget; 384 and 1024 both cut off the answer
        # (AdapterParseError: only [reasoning] parsed).
        max_tokens=4096,
        # 5 parent chunks + CoT instructions exceed Ollama's default 4k
        # window; our cached client uses 16384 everywhere, so match it.
        num_ctx=16384,
        cache=True,
        # qwen3.8:27b is a thinking model: without think=False its native
        # reasoning fills `reasoning_content` and leaves `text` empty, so
        # DSPy parses an empty response (same reason rag_tutorial.llm sends
        # think=False). Verified litellm forwards `think` to Ollama.
        think=False,
    )


def configure() -> dspy.LM:
    lm = get_lm()
    dspy.configure(lm=lm)
    return lm


# ---------------------------------------------------------------------------
# Chapter-07 best retriever as plain Python (hybrid RRF + bge rerank, k=5)
# ---------------------------------------------------------------------------


@lru_cache(maxsize=1)
def _indexes():
    from rag_tutorial.retrieval_eval import _Indexes

    return _Indexes()


@lru_cache(maxsize=1)
def _bge_reranker():
    from rag_tutorial.rerankers import CrossEncoderReranker

    return CrossEncoderReranker(model="BAAI/bge-reranker-v2-m3")


def retrieve_chunks(question: str, k: int = K) -> list[Chunk]:
    """Ch07 best: hybrid RRF child pool (k_each=20) -> bge rerank -> parents."""
    from rag_tutorial.rerank_eval import _hybrid_children, _to_parents

    idx = _indexes()
    children = _hybrid_children(idx, question)
    ranked_children = _bge_reranker().rerank(question, children, k=len(children))
    return _to_parents(ranked_children, idx, n=k)


def retrieve_texts(question: str, k: int = K) -> list[str]:
    short_names = _short_names()
    return [
        f"[{short_names.get(c.paper, c.paper)}] {c.text}"
        for c in retrieve_chunks(question, k)
    ]


# ---------------------------------------------------------------------------
# DSPy program
# ---------------------------------------------------------------------------


class RAG(dspy.Module):
    """One retriever (plain Python) + one ChainOfThought generation step."""

    def __init__(self, k: int = K):
        super().__init__()
        self.k = k
        self.respond = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question: str):
        context = retrieve_texts(question, self.k)
        return self.respond(context="\n\n".join(context), question=question)


def _program_answer(program: RAG, question: str) -> tuple[str, list[str]]:
    pred = program(question=question)
    answer = str(getattr(pred, "answer", pred))
    chunks = retrieve_chunks(question)
    short_names = _short_names()
    contexts = [f"[{short_names.get(c.paper, c.paper)}] {c.text}" for c in chunks]
    return answer, contexts


def _harness(program: RAG):
    def retrieve_fn(item: dict) -> list[Chunk]:
        return retrieve_chunks(item["question"])

    def answer_fn(item: dict, retrieved: list[Chunk]) -> tuple[str, list[str], int]:
        pred = program(question=item["question"])
        answer = str(getattr(pred, "answer", pred))
        short_names = _short_names()
        contexts = [f"[{short_names.get(c.paper, c.paper)}] {c.text}" for c in retrieved]
        return answer, contexts, 1

    return retrieve_fn, answer_fn


# ---------------------------------------------------------------------------
# Metric (cheap token-F1 inside the optimiser — NOT the LLM judge)
# ---------------------------------------------------------------------------

_WORD_RE = re.compile(r"\w+")


def _tokens(text: str) -> list[str]:
    return _WORD_RE.findall(text.lower())


def token_f1(pred: str, ref: str) -> float:
    pt, rt = _tokens(pred), _tokens(ref)
    if not pt or not rt:
        return 0.0
    from collections import Counter

    pc, rc = Counter(pt), Counter(rt)
    overlap = sum((pc & rc).values())
    if not overlap:
        return 0.0
    prec = overlap / len(pt)
    rec = overlap / len(rt)
    return 2 * prec * rec / (prec + rec)


def dspy_metric(example: dspy.Example, pred: dspy.Prediction, trace=None) -> float:
    """Cheap optimiser metric: token-F1 vs the reference answer."""
    try:
        return token_f1(str(pred.answer), str(example.answer))
    except Exception:  # noqa: BLE001 — optimiser must never crash on a bad pred
        return 0.0


# ---------------------------------------------------------------------------
# Dev/test splits as dspy.Example
# ---------------------------------------------------------------------------


def load_dspy_split(split: str) -> list[dspy.Example]:
    return [
        dspy.Example(question=item["question"], answer=item["answer"]).with_inputs("question")
        for item in load_qa(QA_PATH)
        if item["split"] == split
    ]


def _program_path(name: str):
    path = DSPY_CACHE_DIR / f"{name}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _count_lm_calls(lm) -> int:
    try:
        return len(lm.history)
    except Exception:  # noqa: BLE001
        return -1


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


@app.command()
def baseline() -> None:
    """Evaluate the zero-shot program on the test split (-> 10_dspy_zero_shot)."""
    lm = configure()
    program = RAG()
    retrieve_fn, answer_fn = _harness(program)
    t0 = time.monotonic()
    metrics = evaluate_run("10_dspy_zero_shot", chapter="10", answer_fn=answer_fn, retrieve_fn=retrieve_fn, split="test")
    metrics["details"]["dspy"] = {"optimizer": "none", "lm_calls": _count_lm_calls(lm), "seconds": round(time.monotonic() - t0, 1)}
    (RUNS_DIR / "10_dspy_zero_shot" / "metrics.json").write_text(json.dumps(metrics, indent=2))
    program.save(str(_program_path("10_dspy_zero_shot")))
    console.print(f"[green]wrote[/green] runs/10_dspy_zero_shot/metrics.json")


@app.command()
def optimize() -> None:
    """Run BootstrapFewShot + MIPROv2(light) on the dev split; save programs.

    Budgets kept small (<=400 LLM calls per optimiser by construction:
    dev=9 examples, max_bootstrapped_demos<=4, MIPROv2 auto=light).
    """
    lm = configure()
    devset = load_dspy_split("dev")
    console.print(f"[green]devset[/green] {len(devset)} examples (overfitting risk noted)")
    summary: dict = {"dev_n": len(devset), "metric": "token_f1 (cheap; judge only in final eval)"}

    # -- BootstrapFewShot (cheap) --
    t0 = time.monotonic()
    before = _count_lm_calls(lm)
    tele = dspy.BootstrapFewShot(
        metric=dspy_metric, max_bootstrapped_demos=4, max_labeled_demos=4
    )
    bootstrap = tele.compile(RAG(), trainset=devset)
    b_calls = _count_lm_calls(lm) - before
    bootstrap.save(str(_program_path("10_dspy_bootstrap")))
    summary["bootstrap"] = {"lm_calls": b_calls, "seconds": round(time.monotonic() - t0, 1)}
    console.print(f"[green]bootstrap[/green] {b_calls} LM calls; saved data/cache/dspy/10_dspy_bootstrap.json")

    # -- MIPROv2 light (needs `optuna`: uv add --group dspy optuna) --
    t0 = time.monotonic()
    before = _count_lm_calls(lm)
    try:
        mipro = dspy.MIPROv2(metric=dspy_metric, auto="light", num_threads=1)
        mipro_prog = mipro.compile(RAG(), trainset=devset, max_bootstrapped_demos=2, max_labeled_demos=2)
        mipro_prog.save(str(_program_path("10_dspy_mipro")))
        summary["mipro"] = {"lm_calls": _count_lm_calls(lm) - before, "seconds": round(time.monotonic() - t0, 1)}
        console.print(f"[green]mipro[/green] {summary['mipro']['lm_calls']} LM calls; saved data/cache/dspy/10_dspy_mipro.json")
    except Exception as exc:  # noqa: BLE001 — keep the bootstrap result + summary
        summary["mipro"] = {"error": f"{type(exc).__name__}: {exc}"}
        console.print(f"[yellow]mipro failed ({exc}); bootstrap program kept[/yellow]")

    summary_path = settings.path("runs/10_dspy_optimize_summary.json")
    summary_path.write_text(json.dumps(summary, indent=2))
    # Also mirror into a runs/ dir so the scoreboard tool ignores it safely.
    console.print(f"[green]wrote[/green] {summary_path} {json.dumps(summary)}")


@app.command()
def eval() -> None:
    """Evaluate zero-shot / bootstrap / mipro programs on test (-> 3 rows)."""
    configure()
    programs: dict[str, RAG] = {}
    for name in ("10_dspy_zero_shot", "10_dspy_bootstrap", "10_dspy_mipro"):
        path = _program_path(name)
        prog = RAG()
        if path.exists():
            try:
                prog.load(str(path))
                console.print(f"[green]loaded[/green] {path}")
            except Exception as exc:  # noqa: BLE001 — fall back to zero-shot
                console.print(f"[yellow]could not load {path} ({exc}); using zero-shot[/yellow]")
        else:
            console.print(f"[yellow]missing {path}; using zero-shot[/yellow]")
        programs[name] = prog

    for name, prog in programs.items():
        if (RUNS_DIR / name / "metrics.json").exists():
            console.print(f"[yellow]skipping[/yellow] {name} (metrics.json exists)")
            continue
        retrieve_fn, answer_fn = _harness(prog)
        console.print(f"[bold]evaluating[/bold] {name} ...")
        t0 = time.monotonic()
        evaluate_run(name, chapter="10", answer_fn=answer_fn, retrieve_fn=retrieve_fn, split="test")
        console.print(f"[green]wrote[/green] runs/{name}/metrics.json ({time.monotonic() - t0:.1f}s)")


@app.command(name="eval-all")
def eval_all() -> None:
    """Alias for `eval` (all three DSPy rows)."""
    eval()


if __name__ == "__main__":
    os.makedirs(DSPY_CACHE_DIR, exist_ok=True)
    app()
