"""Chapter 07 rerankers.

Every class exposes:
    - `.rerank(question: str, chunks: list[Chunk], k: int) -> list[Chunk]`
      (scores every input, orders best-first, returns top k)
    - `.n_calls` — number of expensive model calls used (0 for the small local
      ones, >0 for `LLMReranker` because each pass is an LLM call). For the
      LLMs this is the number of chat calls (pointwise batches 5 pairs per
      call; listwise is one call per list), not the number of scored pairs.

Disk cache
----------
Every (model, query, chunk_id) -> score pair is persisted under
`data/cache/reranker/<model_slug>/<sha256>.json` so re-running a chapter or a
single question reuses the already-computed scores. LLM calls always go
through `rag_tutorial.llm.Ollama` and so get their own chat cache; the
reranker cache on top of that lets re-runs be *zero* LLM calls on top of
that (i.e. even the judge-side prompt for rerankers is cached).

Model list (chapter 07 spec)
----------------------------
- `CrossEncoderReranker(model="BAAI/bge-reranker-v2-m3")`          (0.6B, cross-encoders)
- `CrossEncoderReranker(model="cross-encoder/ms-marco-MiniLM-L-6-v2")` (22M, cross-encoders)
- `FlashRankReranker(model="ms-marco-TinyBERT-L-2-v2")`            (4MB, ONNX)
- `LLMReranker(mode="listwise")` / `LLMReranker(mode="pointwise")`  (qwen3.8:27b via Ollama)
- `ColBERTReranker(model="answerdotai/answerai-colbert-small-v1")`  (ColBERTv1 late-interaction via pylate)

The last one is best-effort: pylate wraps sentence-transformers' ColBERT class
which targets ColBERTv1-style checkpoints; if the v2 checkpoint can't be loaded
in a future version of the dependency stack, `ColBERTReranker.__init__` will
raise `ColBERTUnavailable` and the eval driver catches it and records
`colbert: "unavailable"` in the scoreboard instead of the usual metrics.
"""

from __future__ import annotations

import abc
import hashlib
import json
import math
import threading
from pathlib import Path

from rag_tutorial.config import settings
from rag_tutorial.llm import ollama
from rag_tutorial.schema import Chunk

RERANK_CACHE_DIR = settings.path("data/cache/reranker")

_POINTWISE_BATCH = 5  # 5 query-passage pairs per LLM call (chapter 07 spec)


class Reranker(abc.ABC):
    """Base class. Subclasses override `_score` and set `.model_slug`."""

    model_slug: str = "reranker"
    n_calls: int = 0

    def __init__(self, cache_dir: str | Path | None = None):
        self.cache_dir = RERANK_CACHE_DIR if cache_dir is None else settings.path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    # -- cache ------------------------------------------------------------------

    def _cache_key(self, question: str, chunk: Chunk) -> str:
        blob = json.dumps({"model": self.model_slug, "q": question, "id": chunk.id}, sort_keys=True)
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()

    def _cache_path(self, key: str) -> Path:
        return self.cache_dir / self.model_slug / key[:2] / f"{key}.json"

    def _cache_read(self, path: Path) -> float | None:
        if not path.exists():
            return None
        try:
            return float(json.loads(path.read_text())["score"])
        except (json.JSONDecodeError, OSError, ValueError, KeyError):
            return None

    def _cache_write(self, path: Path, score: float) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"score": float(score)}, indent=2))

    # -- scoring API ------------------------------------------------------------

    @abc.abstractmethod
    def _score_batch(self, question: str, chunks: list[Chunk]) -> list[float]:
        """Return one score per input chunk, best-first (higher = more
        relevant for every model in this module)."""

    def rerank(self, question: str, chunks: list[Chunk], k: int | None = None) -> list[Chunk]:
        """Score every chunk (disk-cached), order best-first, return top `k`.

        `n_calls` reflects only the *fresh* (cache-miss) scoring work, so
        `rerank_eval` can report "model calls per question" honestly."""
        if not chunks:
            return []
        scores: list[float | None] = [None] * len(chunks)
        missing: list[int] = []
        for i, chunk in enumerate(chunks):
            path = self._cache_path(self._cache_key(question, chunk))
            cached = self._cache_read(path)
            if cached is not None:
                scores[i] = cached
            else:
                missing.append(i)

        if missing:
            fresh = self._score_batch(question, [chunks[i] for i in missing])
            for i, s in zip(missing, fresh):
                self._cache_write(self._cache_path(self._cache_key(question, chunks[i])), float(s))
                scores[i] = float(s)

        final_scores = [s if s is not None else -float("inf") for s in scores]
        order = sorted(range(len(chunks)), key=lambda i: -final_scores[i])
        limit = len(chunks) if k is None else min(k, len(chunks))
        return [chunks[i] for i in order[:limit]]

    # -- model registry ---------------------------------------------------------

    @staticmethod
    def available() -> dict[str, bool]:
        """Report which models this machine can load *right now* (no
        downloads). Useful for the `07_findings.md` "setup" section and for
        the `ColBERTUnavailable` guard in `rerank_eval.py`.

        - CrossEncoder / FlashRank: check the on-disk HF / flashrank cache
          (no HF download needed).
        - ColBERT (pylate): check if `answerdotai/answerai-colbert-small-v1`
          lives in the HF hub cache. We *do not* call pylate here because
          its `ColBERT(...)` constructor can throw on a version mismatch
          with the installed sentence-transformers; that is caught by
          `rerank_eval` at load time.
        - LLM: check if Ollama is reachable (cheap: `GET /api/tags`).
        """
        import urllib.request

        out: dict[str, bool] = {}
        hf = Path.home() / ".cache" / "huggingface" / "hub"
        out["cross-encoder-bge"] = (hf / "models--BAAI--bge-reranker-v2-m3").exists()
        out["cross-encoder-minilm"] = (hf / "models--cross-encoder--ms-marco-MiniLM-L-6-v2").exists()
        out["flashrank"] = (settings.path("data/cache/flashrank") / "ms-marco-TinyBERT-L-2-v2").exists()
        out["colbertv1-pylate"] = (hf / "models--answerdotai--answerai-colbert-small-v1").exists()
        try:
            with urllib.request.urlopen(f"{settings.ollama_url}/api/tags", timeout=2) as r:
                out["llm"] = r.status == 200
        except Exception:
            out["llm"] = False
        out["llm_model_name"] = settings.chat_model
        return out


# -- cross-encoders -------------------------------------------------------------------


class CrossEncoderReranker(Reranker):
    """sentence-transformers `CrossEncoder`. Two supported models:

    - "BAAI/bge-reranker-v2-m3"          (0.6B, 512 tokens, Apache 2.0)
    - "cross-encoder/ms-marco-MiniLM-L-6-v2" (22M, Apache 2.0)

    Both load from the Hugging Face hub cache on first call (we do not
    download inside this module — `just rerank-eval` documents that both
    checkpoints must be pre-fetched with `uv run python -c ...`).
    """

    def __init__(self, model: str = "BAAI/bge-reranker-v2-m3", cache_dir: str | Path | None = None):
        super().__init__(cache_dir=cache_dir)
        self.model_name = model
        self.model_slug = f"cross-encoder-{model.split('/')[-1]}"
        self._model = None
        self._lock = threading.Lock()

    def _ensure(self):
        if self._model is None:
            with self._lock:
                if self._model is None:
                    from sentence_transformers import CrossEncoder

                    self._model = CrossEncoder(self.model_name, max_length=256)
        return self._model

    def _score_batch(self, question: str, chunks: list[Chunk]) -> list[float]:
        model = self._ensure()
        self.n_calls += 1  # one scoring pass for the cache-missing batch
        pairs = [[question, c.text] for c in chunks]
        scores = model.predict(pairs, batch_size=32)
        return [float(s) for s in scores]


# -- flashrank ------------------------------------------------------------------------


class FlashRankReranker(Reranker):
    """FlashRank ONNX cross-encoder (default `ms-marco-TinyBERT-L-2-v2`, ~4MB).

    Returns raw logit-style scores that are *not* probabilities; the
    relative ordering is what we use, so no sigmoid is applied (the
    FlashRank README documents that the default TinyBERT checkpoint
    produces scores in an absolute range, and the docs recommend sorting
    by score, not by threshold).
    """

    def __init__(self, model: str = "ms-marco-TinyBERT-L-2-v2", cache_dir: str | Path | None = None):
        super().__init__(cache_dir=cache_dir)
        self.model_name = model
        self.model_slug = f"flashrank-{model}"
        self._ranker = None
        self._lock = threading.Lock()

    def _ensure(self):
        if self._ranker is None:
            with self._lock:
                if self._ranker is None:
                    from flashrank import Ranker

                    self._ranker = Ranker(self.model_name, cache_dir=str(settings.path("data/cache/flashrank")))
        return self._ranker

    def _score_batch(self, question: str, chunks: list[Chunk]) -> list[float]:
        ranker = self._ensure()
        self.n_calls += 1  # one scoring pass for the cache-missing batch
        request_type = _flashrank_rerank_request()
        req = request_type(question, [{"text": c.text} for c in chunks])
        results = ranker.rerank(req)
        text_to_score = {r["text"]: float(r["score"]) for r in results}
        return [text_to_score.get(c.text, -float("inf")) for c in chunks]


def _flashrank_rerank_request():
    from flashrank import RerankRequest

    return RerankRequest


# -- colbert --------------------------------------------------------------------------


class ColBERTUnavailable(RuntimeError):
    """Raised when pylate can't load the ColBERT checkpoint (version mismatch
    between pylate's `ColBERT` wrapper and the installed sentence-transformers)."""


class ColBERTReranker(Reranker):
    """ColBERT late-interaction reranking via pylate's `ColBERT` class.

    We use the v1 model `answerdotai/answerai-colbert-small-v1` (~70MB)
    because pylate's ColBERT class inherits from sentence-transformers'
    `ColBERT` (the original ColBERTv1 codebase) and cannot load v2-style
    checkpoints — verified locally: `ColBERT('answerdotai/answerai-colbert-
    small-v2*')` raises `KeyError:'activation_function'` under ST 5.3.

    Score = max-per-query-token dot product against the passage's per-token
    unit vectors (the classic "lazy ColBERT" MaxSim).
    """

    def __init__(self, model: str = "answerdotai/answerai-colbert-small-v1", cache_dir: str | Path | None = None):
        super().__init__(cache_dir=cache_dir)
        self.model_name = model
        self.model_slug = f"colbert-{model.split('/')[-1]}"
        self._model = None
        self._lock = threading.Lock()

    def _ensure(self):
        if self._model is None:
            with self._lock:
                if self._model is None:
                    try:
                        from pylate.models import ColBERT

                        self._model = ColBERT(self.model_name)
                    except Exception as exc:  # noqa: BLE001 — any load failure becomes a clean skip
                        raise ColBERTUnavailable(f"pylate could not load {self.model_name!r}: {exc!r}") from exc
        return self._model

    # -- scoring ----------------------------------------------------------------

    def _encode_query(self, question: str):
        import torch

        qe = self._model.encode(question, is_query=True, convert_to_tensor=True, padding=True, batch_size=1)
        if qe.dim() == 3 and qe.shape[0] == 1:  # collapse the batch axis
            qe = qe.squeeze(0)
        qe = qe / (qe.norm(dim=-1, keepdim=True) + 1e-9)
        return qe

    def _encode_document(self, text: str):
        import torch

        de = self._model.encode(text, is_query=False, convert_to_tensor=True, padding=False, batch_size=1)
        if de.dim() == 3 and de.shape[0] == 1:
            de = de.squeeze(0)
        de = de / (de.norm(dim=-1, keepdim=True) + 1e-9)
        return de

    def _maxsim(self, qe, de) -> float:  # type: ignore[no-untyped-def]
        import torch

        scores = torch.einsum("id,jd->ij", qe, de)
        return float(scores.max(0).values.sum())

    def _score_batch(self, question: str, chunks: list[Chunk]) -> list[float]:
        model = self._ensure()
        self.n_calls += 1  # one pass: query encode + per-chunk MaxSim
        qe = self._encode_query(question)
        out = []
        for c in chunks:
            de = self._encode_document(c.text)
            out.append(self._maxsim(qe, de))
        return out


# -- LLM-as-reranker ------------------------------------------------------------------


_LISTWISE_PROMPT = (
    "You are a search reranker. From the passages below, pick the MOST relevant "
    "to the question. Reply with a single line of digits — the 1-based indices "
    "in your chosen order, most-relevant first, no spaces, no explanation.\n\n"
    "Question: {question}\n\n"
    "Passages:\n"
    "{passages}\n\n"
    "Order:"
)

_POINTWISE_PROMPT = (
    "You are a search relevance grader. For each (query, passage) pair below, "
    "score relevance from 0 (irrelevant) to 3 (definitively answers the query) "
    "— integers only. Reply with one line per pair, in the same order, each "
    "line being just the integer, no other text.\n\n"
    "Pairs:\n{pairs}\n\n"
    "Scores:"
)


class LLMReranker(Reranker):
    """Two prompting modes on the tutorial's chat model (qwen3.8:27b):

    - `mode="listwise"` (RankGPT-style, Sun et al. EMNLP 2023): show the LLM
      all candidates at once, ask it to *re-order* them most-relevant-first.
      One chat call per call to `.rerank()`; the model outputs "3 1 2 4".
      We map the returned indices back to our candidate list and rank by
      returned position (1 → top).

    - `mode="pointwise"` (batched): group candidates in batches of 5, ask the
      LLM for a 0..3 integer on each one. One call per batch; total calls =
      ceil(len(chunks) / 5). Score = the integer as a float.

    Both use the disk cache (via `Reranker._cache_read`/`_cache_write`) and
    the Ollama chat cache (via `rag_tutorial.llm.Ollama`), so a re-run is a
    no-op if the (query, passages) list is identical.
    """

    def __init__(
        self,
        mode: str = "listwise",
        client=None,
        max_candidates: int = 50,
        cache_dir: str | Path | None = None,
    ):
        super().__init__(cache_dir=cache_dir)
        if mode not in ("listwise", "pointwise"):
            raise ValueError(f"mode must be 'listwise' or 'pointwise', got {mode!r}")
        self.mode = mode
        self.client = client or ollama
        self.max_candidates = max_candidates
        self.model_slug = f"llm-{mode}-max{max_candidates}"

    # -- mode-specific batch scorers ----------------------------------------------

    def _score_listwise(self, question: str, chunks: list[Chunk]) -> list[float]:
        idx = list(range(len(chunks)))
        scores: list[float] = [0.0] * len(chunks)
        # process in windows of `max_candidates` so the prompt stays small
        for start in range(0, len(chunks), self.max_candidates):
            window = idx[start : start + self.max_candidates]
            passages = "\n\n".join(f"[{i + 1}] {chunks[i].text}" for i in window)
            prompt = _LISTWISE_PROMPT.format(question=question, passages=passages)
            reply = self.client.chat(
                [
                    {"role": "system", "content": "Answer with exactly a line of space-separated integers."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.0,
                max_tokens=64,
            )
            self.n_calls += 1
            order = self._parse_order(reply, len(window))
            # rank 1 → highest score (len-1), rank n → lowest score (0)
            for pos, local_idx in enumerate(order):
                scores[window[local_idx]] = float(len(window) - pos)
        return scores

    def _score_pointwise(self, question: str, chunks: list[Chunk]) -> list[float]:
        out: list[float] = [0.0] * len(chunks)
        for start in range(0, len(chunks), _POINTWISE_BATCH):
            window = list(range(start, min(start + _POINTWISE_BATCH, len(chunks))))
            pairs = "\n".join(f"{i + 1}. Q: {question}\n   P: {chunks[i].text}" for i in window)
            prompt = _POINTWISE_PROMPT.format(pairs=pairs)
            reply = self.client.chat(
                [
                    {"role": "system", "content": "Answer with one integer per line, 0-3."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.0,
                max_tokens=64,
            )
            self.n_calls += 1
            digits = [int(x) for x in reply.replace("\n", " ").split() if x.strip().isdigit()]
            for local_pos, i in enumerate(window):
                out[i] = float(digits[local_pos]) if local_pos < len(digits) else 0.0
        return out

    def _score_batch(self, question: str, chunks: list[Chunk]) -> list[float]:
        if self.mode == "listwise":
            return self._score_listwise(question, chunks)
        return self._score_pointwise(question, chunks)

    # -- parsing ----------------------------------------------------------------

    @staticmethod
    def _parse_order(reply: str, n: int) -> list[int]:
        """Parse "3 1 2" (or "3,1,2\n...") into 0-based local indices,
        keeping only values in [1, n] and dropping duplicates (first occurrence
        wins). Fallback: identity order on parse failure (defensive)."""
        out: list[int] = []
        seen: set[int] = set()
        for tok in reply.replace(",", " ").split():
            if not tok:
                continue
            try:
                v = int(tok)
            except ValueError:
                continue
            if 1 <= v <= n and v - 1 not in seen:
                seen.add(v - 1)
                out.append(v - 1)
            if len(out) == n:
                break
        for i in range(n):
            if i not in seen:
                out.append(i)
        return out[:n]


__all__ = [
    "Reranker",
    "CrossEncoderReranker",
    "FlashRankReranker",
    "ColBERTReranker",
    "ColBERTUnavailable",
    "LLMReranker",
    "RERANK_CACHE_DIR",
    "_POINTWISE_BATCH",
]
