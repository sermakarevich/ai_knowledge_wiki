"""Inspect-AI task definitions for chapter 12.

Chapters 05-11 hand-rolled ``client -> prompt -> JSON`` and scored the output
with a home-grown loop.  Here the same two workloads are rebuilt as proper
``inspect_ai`` ``Task`` objects: a dataset of :class:`~inspect_ai.dataset.Sample`
records, a solver that produces the answer, and built-in or custom scorers.

* :func:`helpdesk_task` -- chapter 05's support-reply flow.  The solver writes
  the reply through the cached client (identical retriever, prompt and
  temperature to chapter 05), so every call is a cache hit.  Three scorers
  grade each reply:

    - ``judge_grade`` -- the four tracked failure-mode judges (exact ch-05
      prompts and mode versions), AND-composed into one pass/fail.  PRIMARY.
    - ``code_checks`` -- ch-10's six deterministic checks, scored as pass-rate.
    - ``includes`` -- built-in substring scorer: pass if any of the ticket's
      gold answer points appears verbatim in the reply.

* :func:`gsm8k_task` -- chapter 11's GSM8K plain-prompt run (same 50
  questions, same prompt file).  The scorer is the built-in
  ``match(location="end", numeric=True)``: it extracts the last number in the
  output and compares it to the target, which is the gold number.

* :class:`CachedModelAPI` -- an Inspect ``ModelAPI`` that routes
  ``generate()`` through :data:`evals_tutorial.llm.ollama`, the same cached
  client every chapter uses, so a full re-run costs zero fresh LLM calls and
  the log records a real model name.
"""

from __future__ import annotations

import json
import re
from typing import Any

from inspect_ai import Task
from inspect_ai.dataset import MemoryDataset, Sample
from inspect_ai.model import GenerateConfig, Model, ModelAPI, ModelOutput, modelapi
from inspect_ai.scorer import CORRECT, INCORRECT, Score, Target, accuracy, includes, match, scorer
from inspect_ai.solver import Generate, TaskState, solver

from . import code_evals, helpdesk, judge
from .tickets import load_tickets as _load_tickets_uncached
from .config import settings
from .llm import ollama

_TICKET_CACHE: dict[str, dict[str, Any]] | None = None


def _tickets_by_id() -> dict[str, dict[str, Any]]:
    """Load all tickets once and index by id."""
    global _TICKET_CACHE
    if _TICKET_CACHE is None:
        _TICKET_CACHE = {str(t["id"]): t for t in _load_tickets_uncached()}
    return _TICKET_CACHE


def load_tickets(split: str | None = None) -> list[dict[str, Any]]:
    """Load tickets, filtered by ``split`` if given."""
    by_id = _tickets_by_id()
    if split is None:
        return list(by_id.values())
    return [t for t in by_id.values() if t.get("split") == split]


# ---------------------------------------------------------------------------
# Model API: route Inspect's calls through the cached ollama client
# ---------------------------------------------------------------------------


@modelapi("cached_ollama")
class CachedModelAPI(ModelAPI):
    """``ModelAPI`` that delegates to :data:`evals_tutorial.llm.ollama`.

    Keeps chapter 12's runs on the exact same cached client (and cache) as
    chapters 05-11, so re-running is free and numbers reconcile 1:1.
    """

    def __init__(
        self,
        model_name: str = settings.chat_model,
        base_url: str | None = None,
        api_key: str | None = None,
        api_key_vars: list[str] | None = None,
        config: GenerateConfig | None = None,
    ) -> None:
        super().__init__(
            model_name=model_name,
            base_url=base_url or settings.ollama_url,
            api_key=api_key,
            api_key_vars=api_key_vars or [],
            config=config or GenerateConfig(),
        )

    async def generate(
        self,
        input: list[Any],
        tools: list[Any] | None = None,
        tool_choice: Any = None,
        config: GenerateConfig | None = None,
    ) -> ModelOutput:
        user_text = ""
        for msg in reversed(list(input or [])):
            role = getattr(msg, "role", "")
            content = getattr(msg, "content", "")
            if role == "user" and isinstance(content, str):
                user_text = content
                break
        text = await self._run_sync(self._generate_text, user_text)
        return ModelOutput.from_content(settings.chat_model, text)

    def _generate_text(self, user_text: str) -> str:
        if not user_text:
            return ""
        return ollama.chat([{"role": "user", "content": user_text}])

    @staticmethod
    async def _run_sync(fn: Any, *args: Any) -> Any:
        import asyncio

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: fn(*args))


def cached_model() -> Any:
    """A ready-to-``eval()`` Inspect ``Model`` backed by the cached client."""
    return Model(CachedModelAPI(), GenerateConfig())


# ---------------------------------------------------------------------------
# helpdesk (chapter 05) -- solver + three scorers
# ---------------------------------------------------------------------------


@solver(name="helpdesk_solve")
def helpdesk_solve(version: str = "v1") -> Any:
    """Write the support reply for the ticket in ``state.input``."""

    async def solve(state: TaskState, generate: Generate) -> TaskState:
        reply = helpdesk.answer(state.input, version=version)
        # Inspect requires a ModelOutput on state.output; the reply itself came
        # from the cached client (same messages, same temperature), so this is
        # only the carrier object the scorers read.
        state.output = ModelOutput.from_content(settings.chat_model, reply.text)
        return state

    return solve


def _mode_scores(ticket: dict, reply: str) -> dict[str, Any]:
    """Run every tracked judge mode for one ticket and return per-mode rows.

    Mirrors :func:`evals_tutorial.judge.judge_ticket` exactly (same prompt,
    same model, same trace shape) so the verdict matches chapter 05's
    per-ticket record.
    """
    # ch-05 traces store retrieved section *ids* (judge._context_for looks the
    # text up itself); use the `retrieved` rows (index [1]), not full-text blocks.
    _blocks, retrieved = helpdesk.retrieved_context(ticket["text"])
    trace = {
        "ticket_id": ticket["id"],
        "input": ticket["text"],
        "output": reply,
        "retrieved": retrieved,
    }
    scored: dict[str, Any] = {}
    for mode in judge.tracked_modes():
        ver = judge.chosen_version(mode)
        try:
            verdict = judge.judge_ticket(mode, ver, trace, ollama)
            critique = verdict.critique
            verdict_str = verdict.verdict
        except Exception as exc:  # noqa: BLE001 - keep the run alive, count as fail
            critique = f"judge error: {exc}"
            verdict_str = "fail"
        scored[mode] = {"version": ver, "verdict": verdict_str, "critique": critique}
    return scored


@scorer(metrics=[accuracy()], name="judge_grade")
def _judge_grade(version: str = "v1") -> Any:
    """AND-compose the four tracked failure-mode verdicts into one score.

    A ticket passes iff no mode fails (exactly chapter 05's rule).  Built-in
    style scorer so ``inspect view`` renders it alongside ``includes``/``match``.
    """

    async def score(state: TaskState, target: Target) -> Score:
        ticket_id = str((state.metadata or {}).get("ticket_id", state.sample_id))
        reply_text = (state.output.completion or "") if state.output else ""
        ticket = _tickets_by_id().get(ticket_id) or {
            "id": ticket_id, "text": state.input, "gold": {},
        }
        mode_rows = _mode_scores(ticket, reply_text)
        fails = [m for m, r in mode_rows.items() if r["verdict"] != "pass"]
        value: Any = 1 if not fails else 0
        explanation = "; ".join(
            f"{m}[{r['version'][1:]}]={r['verdict']}" for m, r in mode_rows.items()
        )
        return Score(
            value=CORRECT if not fails else INCORRECT,
            answer=reply_text,
            explanation=explanation,
            metadata={"modes": mode_rows, "failed": fails},
        )

    return score


@scorer(metrics=[accuracy()], name="code_checks")
def _code_checks() -> Any:
    """Run the six deterministic checks (chapter 10) and score as pass-rate."""

    async def score(state: TaskState, target: Target) -> Score:
        ticket_id = str((state.metadata or {}).get("ticket_id", state.sample_id))
        reply_text = (state.output.completion or "") if state.output else ""
        ticket = _tickets_by_id().get(ticket_id) or {
            "id": ticket_id, "text": state.input, "gold": {},
        }
        _blocks, retrieved = helpdesk.retrieved_context(ticket["text"])
        trace = {
            "ticket_id": ticket_id,
            "input": ticket["text"],
            "output": reply_text,
            "retrieved": retrieved,
        }
        results = {name: bool(fn(ticket, trace)) for name, fn in code_evals.CHECKS.items()}
        passed = sum(1 for v in results.values() if v)
        n = len(results)
        value = passed / n if n else 0.0
        explanation = ", ".join(f"{name}={'ok' if v else 'FAIL'}" for name, v in results.items())
        return Score(
            value=value,
            answer=reply_text,
            explanation=explanation,
            metadata={"results": results, "passed": passed, "total": n},
        )

    return score


def _helpdesk_dataset(split: str = "test") -> MemoryDataset:
    """Chapter 05's ``test``/``dev`` split as an Inspect dataset.

    ``target`` carries the gold ``answer_points`` (what ``includes`` checks);
    ``metadata`` carries the full gold record for reconciliation.
    """
    tickets = load_tickets(split=split)
    samples = [
        Sample(
            input=t["text"],
            target=list((t.get("gold") or {}).get("answer_points") or []),
            id=t["id"],
            metadata={
                "ticket_id": t["id"],
                "scenario": t.get("scenario") or "",
                "persona": t.get("persona") or "",
                "gold": t.get("gold") or {},
            },
        )
        for t in tickets
    ]
    return MemoryDataset(samples, name=f"helpdesk-{split}")


def helpdesk_task(split: str = "test", version: str = "v1") -> Task:
    """Chapter 05's helpdesk reply flow, rebuilt as an Inspect-AI Task."""
    return Task(
        dataset=_helpdesk_dataset(split=split),
        solver=helpdesk_solve(version=version),
        scorer=[
            _judge_grade(version=version),
            _code_checks(),
            includes(),
        ],
        name="helpdesk_answer",
        config=GenerateConfig(),
        display_name=f"helpdesk_answer[{split}:{version}]",
    )


# ---------------------------------------------------------------------------
# gsm8k (chapter 11) -- solver + scorer
# ---------------------------------------------------------------------------

# Same prompt file the ch-11 plain variant used (byte-for-byte: the cached
# client keys its cache on prompt text).
_GSM8K_PROMPT = (
    helpdesk.PROMPTS_DIR / "gsm8k_plain_v1.txt"
).read_text()

_SAMPLES_DIR = settings.path("runs") / "11_lmeval" / "gsm8k" / "qwen3.8__27b"
_SAMPLES_FALLBACK = settings.path("runs") / "11_lmeval" / "gsm8k"


def _gold_number(answer_with_cot: str) -> str | None:
    """Extract the reference number from a GSM8K answer (which may be CoT).

    The reference may be ``42``, ``$42`` or ``42 meters`` - the number in the
    segment after the last ``####`` marker (or the whole string) is gold.
    """
    if "####" in answer_with_cot:
        answer_with_cot = answer_with_cot.split("####")[-1]
    m = re.search(r"-?\d+(?:\.\d+)?", answer_with_cot)
    return m.group(0) if m else None


def _gsm8k_samples(limit: int) -> list[dict[str, Any]]:
    """Pull ``limit`` unique GSM8K records from chapter 11's harness dump."""
    records: list[dict[str, Any]] = []
    seen: set[Any] = set()
    for directory in (_SAMPLES_DIR, _SAMPLES_FALLBACK):
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*.jsonl")):
            with path.open() as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        rec = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    question = (rec.get("doc") or {}).get("question") or rec.get("question")
                    answer = (rec.get("doc") or {}).get("answer") or rec.get("answer")
                    doc_id = rec.get("doc_id", rec.get("id"))
                    if not question or not answer or doc_id in seen:
                        continue
                    seen.add(doc_id)
                    records.append(
                        {"question": question, "answer": answer, "doc_id": doc_id}
                    )
            if len(records) >= limit:
                break
        if len(records) >= limit:
            break
    return records[:limit]


@solver(name="gsm8k_solve")
def gsm8k_solve() -> Any:
    """Call the cached client with chapter 11's exact GSM8K plain prompt."""

    async def solve(state: TaskState, generate: Generate) -> TaskState:
        prompt = _GSM8K_PROMPT.format(question=state.input)
        text = ollama.chat([{"role": "user", "content": prompt}])
        state.output = ModelOutput.from_content(settings.chat_model, text)
        return state

    return solve


def _gsm8k_dataset(limit: int) -> MemoryDataset:
    records = _gsm8k_samples(limit)
    samples = [
        Sample(
            id=str(rec["doc_id"] or i),
            input=rec["question"],
            target=_gold_number(rec["answer"]) or rec["answer"],
            metadata={"doc_id": rec["doc_id"], "gold": _gold_number(rec["answer"])},
        )
        for i, rec in enumerate(records)
    ]
    return MemoryDataset(samples, name=f"gsm8k-{limit}")


def gsm8k_task(limit: int = 50) -> Task:
    """Chapter 11's GSM8K run, rebuilt as an Inspect-AI Task (first ``limit``).

    Scorer: built-in ``match(location="end", numeric=True)`` -- extracts the
    last number in the output and compares it to the gold number (the target).
    """
    return Task(
        dataset=_gsm8k_dataset(limit=limit),
        solver=gsm8k_solve(),
        scorer=match(location="end", numeric=True),
        name="gsm8k",
        config=GenerateConfig(),
        display_name=f"gsm8k[{limit}]",
    )
