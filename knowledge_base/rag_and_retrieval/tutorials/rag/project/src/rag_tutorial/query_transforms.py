"""Chapter 07 query transforms.

Each transform takes a question and (via the chat model) produces *extra*
search inputs. The eval driver uses them to expand the set of queries fed to
the retriever, then merges the per-query candidate pools by
union-of-RRF (the same `rrf_fuse` function chapter 05 used for dense + BM25).

Three families:

* "rewrite" transforms return extra **queries** — multi-query, step-back,
  decomposition — each a small list (2-5 items) that we can embed directly.
* "synthetic passage" transforms return one pseudo-passage meant to be
  embedded and matched — HyDE (generate a plausible answer as if we had it).
* "reorder"/"compress" transforms act on **retrieved candidates** and on the
  **final context window** handed to the generator, not on the query itself;
  `lost_in_the_middle_reorder` and `compress_context` are implemented here,
  with the call-count bookkeeping the eval driver needs.

All functions take either an `Ollama` instance (via rag_tutorial.llm) or a
`FakeLLM` (`rag_tutorial.testing.FakeLLM`), so unit tests can monkeypatch the
prompt with canned replies and verify the parsing logic without touching the
network.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from rag_tutorial.llm import Ollama, count_tokens

_LINE_RE = re.compile(r"^\s*(?:\d+|[a-e])[\.\)]\s*")
_BULLET_RE = re.compile(r"^[\*\-\u2022]\s+")


# ---------------------------------------------------------------------------
# prompts (kept inline here, not in prompts.py — these are ch07-specific and
# do not belong in the shared SYSTEM_PROMPT / build_messages contract)
# ---------------------------------------------------------------------------

MULTI_QUERY_SYSTEM = "You are a search query rewriter. Output only the requested lines, one per item."
MULTI_QUERY_PROMPT = (
    "Rewrite the question below into {n} different search queries that a corpus of "
    "research papers would be indexed by — change the vocabulary, use synonyms, "
    "shift from definition to application and vice-versa. Reply with exactly {n} "
    "numbered lines, each line being one complete query (no other text).\n\n"
    "Question: {question}\n\n"
    "Queries:"
)

HYDE_SYSTEM = "Write a plausible, concrete answer to the question as if you already knew it. Two to four sentences, no citations, no hedging."
HYDE_PROMPT = (
    "You are preparing a synthetic answer for a dense search engine. Using ONLY the "
    "information implied by the question, write the two-to-four-sentence passage a "
    "real answer would look like, in plain prose. Do not cite, do not hedge, do not "
    "say 'I cannot answer'.\n\n"
    "Question: {question}\n\n"
    "Synthetic answer:"
)

STEP_BACK_SYSTEM = "You are a search query strategist. Identify the higher-level question this specific one answers, and rephrase."
STEP_BACK_PROMPT = (
    "Given a detailed, specific question, state the ONE higher-level question that "
    "containing a good answer to it would also require answering. Reply with exactly "
    "one line — the rephrased question (no other text).\n\n"
    "Specific question: {question}\n\n"
    "Step-back question:"
)

DECOMPOSE_SYSTEM = "Split the question into 2-4 short sub-questions, each retrievable on its own. One per line, numbered, no other text."
DECOMPOSE_PROMPT = (
    "Break the question below into 2-4 sub-questions, each of which could be "
    "answered from a single passage of an academic corpus. Reply with numbered "
    "lines only (e.g. '1. ...\\n2. ...'). No other text.\n\n"
    "Question: {question}\n\n"
    "Sub-questions:"
)


# ---------------------------------------------------------------------------
# parsing helpers (shared across all transforms; defensive on LLM format noise)
# ---------------------------------------------------------------------------


def _clean_line(line: str) -> str:
    line = _BULLET_RE.sub("", line.strip())
    line = _LINE_RE.sub("", line).strip()
    # strip leading/trailing quotes the LLM sometimes adds for "quoted" answers
    if len(line) >= 2 and line[0] == line[-1] and line[0] in {'"', "'", "\u201c", "\u201d"}:
        line = line[1:-1].strip()
    return line


def _split_lines(text: str, min_lines: int = 1, max_lines: int | None = None) -> list[str]:
    raw = [line for line in (ln.strip() for ln in text.splitlines()) if line.strip()]
    cleaned = [_clean_line(ln) for ln in raw if _clean_line(ln)]
    if max_lines is not None:
        cleaned = cleaned[:max_lines]
    return cleaned[: max_lines] if min_lines == 1 else cleaned[-min_lines:]


# ---------------------------------------------------------------------------
# the transform dataclass — every function below returns one of these
# ---------------------------------------------------------------------------


@dataclass
class TransformResult:
    """Uniform return shape so the eval driver has one code path for every
    transform name."""

    name: str
    variants: list[str]
    n_llm_calls: int

    def as_dict(self) -> dict:
        return {"name": self.name, "variants": self.variants, "n_llm_calls": self.n_llm_calls}


@dataclass
class CompressResult:
    """`compress_context` — different shape from `variants`: it returns a list
    of (chunk, compressed_text) preserving input order, for downstream
    generation. `n_tokens_before/after` use `count_tokens` (tiktoken
    cl100k_base, same as the tutorial's chunk-size budgeting)."""

    name: str
    compressed: list[tuple[object, str]]
    n_llm_calls: int
    n_tokens_before: int
    n_tokens_after: int

    def as_dict(self) -> dict:
        return {
            "name": self.name,
            "n_llm_calls": self.n_llm_calls,
            "n_tokens_before": self.n_tokens_before,
            "n_tokens_after": self.n_tokens_after,
        }


__all__ = [
    "multi_query",
    "hyde",
    "step_back",
    "decompose",
    "compress",
    "lost_in_the_middle_reorder",
    "TransformResult",
    "CompressResult",
]


# ---------------------------------------------------------------------------
# transforms
# ---------------------------------------------------------------------------


def multi_query(question: str, client: Ollama, n: int = 3) -> TransformResult:
    """Produce `n` alternative phrasings of `question` to widen the retrieval pool."""
    if n < 1:
        raise ValueError(f"n must be >= 1, got {n}")
    reply = client.chat(
        [
            {"role": "system", "content": MULTI_QUERY_SYSTEM},
            {"role": "user", "content": MULTI_QUERY_PROMPT.format(n=n, question=question)},
        ],
        temperature=0.3,  # small temperature for variety (chapter 07 research: Sun et al.)
        max_tokens=220,
    )
    variants = _split_lines(reply, min_lines=1, max_lines=n)
    # Drop the original question if the LLM repeated it verbatim and keep the
    # first `n` distinct alternatives.
    seen = {question.strip().lower()}
    out = []
    for v in variants:
        key = v.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(v)
        if len(out) == n:
            break
    return TransformResult(name="multi_query", variants=out, n_llm_calls=1)


def hyde(question: str, client: Ollama) -> TransformResult:
    """Generate a plausible answer (1-3 sentences) to `question`; the driver
    embeds that text and adds the result to the candidate pool before RRF fusion."""
    reply = client.chat(
        [
            {"role": "system", "content": HYDE_SYSTEM},
            {"role": "user", "content": HYDE_PROMPT.format(question=question)},
        ],
        temperature=0.5,  # slightly higher so we don't always generate the same generic passage
        max_tokens=200,
    )
    passage = reply.strip()
    return TransformResult(name="hyde", variants=[passage] if passage else [], n_llm_calls=1)


def step_back(question: str, client: Ollama) -> TransformResult:
    """Identify the broader question that answering the concrete one requires
    (e.g. 'what is the effect of X on Y in Z' → 'how does X affect Y generally').
    One extra variant."""
    reply = client.chat(
        [
            {"role": "system", "content": STEP_BACK_SYSTEM},
            {"role": "user", "content": STEP_BACK_PROMPT.format(question=question)},
        ],
        temperature=0.2,
        max_tokens=160,
    )
    line = _split_lines(reply, min_lines=1, max_lines=1)
    out = line[0] if line and line[0] != question.strip().lower() else None
    return TransformResult(name="step_back", variants=[out] if out else [], n_llm_calls=1)


def decompose(question: str, client: Ollama) -> TransformResult:
    """Split into 2-4 sub-questions; each becomes a separate search query."""
    reply = client.chat(
        [
            {"role": "system", "content": DECOMPOSE_SYSTEM},
            {"role": "user", "content": DECOMPOSE_PROMPT.format(question=question)},
        ],
        temperature=0.3,
        max_tokens=240,
    )
    variants = _split_lines(reply, min_lines=2, max_lines=4)
    if len(variants) < 2 and len(variants) == 1:
        # one line came back: treat as a no-op (driver will fall back to the
        # original question) so the call count still reflects one attempt
        variants = []
    return TransformResult(name="decompose", variants=variants, n_llm_calls=1)


# ---------------------------------------------------------------------------
# "post-retrieval" transforms
# ---------------------------------------------------------------------------


def lost_in_the_middle_reorder(chunks: list[object], k: int = 5) -> list[object]:
    """Move the 2nd-ranked chunk to the end (and the rest forward).

    Chapter 07's `lost_in_the_middle` effect: with a k-sized context window and
    an LLM that attends most to the first/last positions, the 2nd-ranked
    (usually the strongest candidate after the top-1) is the one least likely
    to actually be read. Moving it to the end puts it in a position the LLM
    weights more heavily without changing *which* chunks are present.

    Pure reorder — no LLM call, no retrieval call, just a list rotation of the
    top-k. `k` here is the size of the *final context window*, not the
    retrieval pool.
    """
    top = list(chunks[:k])
    if len(top) < 2:
        return top
    return [top[0]] + top[2:] + [top[1]]


_COMPRESS_SYSTEM = (
    "You are a context compressor. Keep only the sentences of the passage that are "
    "directly relevant to the question. Preserve every factual detail of the kept "
    "sentences (numbers, names, units). Drop everything else. Do NOT add "
    "information, do NOT cite. If no sentence is relevant, output 'not relevant'."
)
_COMPRESS_PROMPT = "Question: {question}\n\nPassage:\n{passage}\n\nKept sentences:"


def compress(chunks: list[object], question: str, client: Ollama) -> CompressResult:
    """Extract the question-relevant sentences from every chunk in `chunks`
    (chapter 07 spec: `compress(chunks, q)`). The retrieval step is unchanged
    (retrieval metrics still measure the original, uncompressed chunks), but
    the *generation* context is smaller and question-focused, which should
    (a) reduce the chance the LLM loses track of the actual claim, and (b)
    reduce prompt tokens.

    Returns a `CompressResult` with `(chunk, compressed_text)` pairs and the
    token counts before/after (`count_tokens` = tiktoken cl100k_base, the
    tutorial's standard budgeting estimator).

    Each chunk is compressed in one LLM call — intentional (not batched) so a
    per-chunk failure is isolated and the Ollama disk cache can serve re-runs
    of a single chunk for free.

    A chunk that compresses to 'not relevant' (or empty) is *dropped* from
    the context; `CompressResult.compressed` then lists the survivors.
    """
    if not chunks:
        return CompressResult(name="compress", compressed=[], n_llm_calls=0, n_tokens_before=0, n_tokens_after=0)

    n_before = sum(count_tokens(c.text) for c in chunks)
    compressed: list[tuple[object, str]] = []
    n_calls = 0
    for chunk in chunks:
        reply = client.chat(
            [
                {"role": "system", "content": _COMPRESS_SYSTEM},
                {"role": "user", "content": _COMPRESS_PROMPT.format(question=question, passage=chunk.text)},
            ],
            temperature=0.0,
            max_tokens=220,
        )
        n_calls += 1
        text = reply.strip()
        if not text or text.lower().startswith("not relevant"):
            continue  # chapter 07 spec: drop chunks with nothing relevant to the question
        compressed.append((chunk, text))

    n_after = sum(count_tokens(tx) for _c, tx in compressed)
    return CompressResult(
        name="compress",
        compressed=compressed,
        n_llm_calls=n_calls,
        n_tokens_before=n_before,
        n_tokens_after=n_after,
    )
