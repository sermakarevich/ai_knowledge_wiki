"""Retrievers introduced in chapter 04, extended in later chapters.

Every retriever exposes `.retrieve(question) -> list[Chunk]` — the chunks
handed to the generation prompt — and `.retrieved_ids()` returning the ids of
the chunks from the *last* `.retrieve()` call, for debugging/printing. Note
that for `ParentChildRetriever`/`SentenceWindowRetriever` the chunks handed to
the prompt (parents / windows) are not the same objects the dense index
matched against — the evidence-containment rule from chapter 02 is checked
against whatever is handed to the prompt, per chapter 04's spec.

Chapter 05 fixes the chunking strategy to `04_parent_child` (chapter 04's best
performer, and free of extra LLM calls) and adds retrieval-only techniques on
top of that same child index: `BM25Retriever` (keyword search), `HybridRetriever`
(dense+BM25 fusion), `mmr_select`/`MMRRetriever` (diversity re-ranking) and
`route_paper` (a query router for metadata filtering). All of them operate on
the child-chunk index and swap hits to their parent chunk via `_swap_to_parent`,
the same de-duplication rule `ParentChildRetriever` introduced in chapter 04.
"""

from __future__ import annotations

import json

import bm25s

from rag_tutorial.chunkers import sentence_spans
from rag_tutorial.config import settings
from rag_tutorial.llm import ollama
from rag_tutorial.schema import Chunk, Document
from rag_tutorial.stores import ChromaStore, QdrantStore

try:
    import Stemmer  # PyStemmer

    _STEMMER = Stemmer.Stemmer("english").stemWords
except ImportError:  # pragma: no cover - PyStemmer ships in pyproject, always installed
    _STEMMER = None

BM25_INDEX_DIR = "data/indexes/bm25"


class DenseRetriever:
    """Plain top-k dense (cosine) retrieval — the chapter 03 baseline, reusable
    for any chunking strategy whose chunks are indexed as-is (no small-to-big
    swap)."""

    def __init__(self, store: ChromaStore, embedder=None, k: int = 5):
        self.store = store
        self.embedder = embedder or ollama
        self.k = k
        self._last_ids: list[str] = []

    def retrieve(self, question: str, where: dict | None = None) -> list[Chunk]:
        query_embedding = self.embedder.embed_query(question)
        chunks = [chunk for chunk, _score in self.store.query(query_embedding, k=self.k, where=where)]
        self._last_ids = [c.id for c in chunks]
        return chunks

    def retrieve_scored(self, question: str, k: int, where: dict | None = None) -> list[tuple[Chunk, float]]:
        """Like `.retrieve` but with an explicit `k` and cosine scores attached —
        used by `HybridRetriever` (fusion needs scores) and `MMRRetriever`
        (over-fetches candidates before diversity re-selection)."""
        query_embedding = self.embedder.embed_query(question)
        return self.store.query(query_embedding, k=k, where=where)

    def retrieve_candidates(self, question: str, k: int, where: dict | None = None) -> list[Chunk]:
        return [chunk for chunk, _score in self.retrieve_scored(question, k, where=where)]

    def retrieved_ids(self) -> list[str]:
        return self._last_ids


def _swap_to_parent(
    ranked_children: list[Chunk],
    child_to_parent: dict[str, str] | None,
    parents: dict[str, Chunk] | None,
    k: int,
) -> list[Chunk]:
    """Walk `ranked_children` (already sorted best-first), swap each one for its
    parent chunk (chapter 04's small-to-big idea) and de-duplicate parents so
    two children of the same parent do not hand the LLM the same context
    twice, keeping the first (best-ranked) `k` distinct parents.

    If `child_to_parent`/`parents` is `None` (no parent-child mapping — plain
    child-level retrieval), this is a no-op de-duplication over the children
    themselves, truncated to `k`.
    """
    result: list[Chunk] = []
    seen: set[str] = set()
    for child in ranked_children:
        parent_id = (child_to_parent or {}).get(child.id, child.id)
        if parent_id in seen:
            continue
        seen.add(parent_id)
        result.append((parents or {}).get(parent_id, child))
        if len(result) >= k:
            break
    return result


class ParentChildRetriever:
    """Dense-search the small child chunks, swap each hit for its larger parent,
    and de-duplicate parents (two children of the same parent should not hand
    the LLM the same context twice). Over-fetches children (`k * fetch_multiplier`)
    so that de-duplication still leaves up to `k` distinct parents.
    """

    def __init__(
        self,
        store: ChromaStore,
        child_to_parent: dict[str, str],
        parents: dict[str, Chunk],
        embedder=None,
        k: int = 5,
        fetch_multiplier: int = 4,
    ):
        self.store = store
        self.child_to_parent = child_to_parent
        self.parents = parents
        self.embedder = embedder or ollama
        self.k = k
        self.fetch_multiplier = fetch_multiplier
        self._last_ids: list[str] = []

    def retrieve(self, question: str, where: dict | None = None) -> list[Chunk]:
        query_embedding = self.embedder.embed_query(question)
        scored = self.store.query(query_embedding, k=self.k * self.fetch_multiplier, where=where)
        children = [child for child, _score in scored]
        result = _swap_to_parent(children, self.child_to_parent, self.parents, self.k)
        self._last_ids = [c.id for c in result]
        return result

    def retrieved_ids(self) -> list[str]:
        return self._last_ids


class SentenceWindowRetriever:
    """Dense-search single indexed sentences, then expand each hit to `window`
    sentences on either side (recomputed from the paper's full text) before
    handing it to the LLM."""

    def __init__(self, store: ChromaStore, docs: dict[str, Document], embedder=None, k: int = 5, window: int = 3):
        self.store = store
        self.docs = docs
        self.embedder = embedder or ollama
        self.k = k
        self.window = window
        self._last_ids: list[str] = []

    def retrieve(self, question: str) -> list[Chunk]:
        query_embedding = self.embedder.embed_query(question)
        scored = self.store.query(query_embedding, k=self.k)
        result = [self._expand(chunk) for chunk, _score in scored]
        self._last_ids = [chunk.id for chunk, _score in scored]
        return result

    def _expand(self, chunk: Chunk) -> Chunk:
        doc = self.docs.get(chunk.paper)
        if doc is None:
            return chunk
        spans = sentence_spans(doc.text)
        idx = next((i for i, (s, e) in enumerate(spans) if s == chunk.start and e == chunk.end), None)
        if idx is None:
            return chunk
        lo, hi = max(idx - self.window, 0), min(idx + self.window, len(spans) - 1)
        start_char, end_char = spans[lo][0], spans[hi][1]
        return Chunk(
            id=chunk.id,
            paper=chunk.paper,
            section=chunk.section,
            text=doc.text[start_char:end_char],
            start=start_char,
            end=end_char,
            meta={"strategy": "sentence_window", "window": self.window},
        )

    def retrieved_ids(self) -> list[str]:
        return self._last_ids


# -- chapter 05: BM25 -----------------------------------------------------------------------


class BM25Retriever:
    """Keyword (BM25) search over the same child-chunk index the dense retriever
    uses, via `bm25s`. Tokenisation is lowercase + English stopwords + an
    optional Snowball stemmer (`PyStemmer`, falls back to no stemming if it is
    not importable) — so "retrieval"/"retrieves"/"retrieved" all match the same
    stem. The index (postings + the chunk corpus) is persisted under
    `data/indexes/bm25/<name>/` so re-running an experiment does not re-tokenise
    the corpus.
    """

    def __init__(
        self,
        name: str,
        k: int = 5,
        child_to_parent: dict[str, str] | None = None,
        parents: dict[str, Chunk] | None = None,
        fetch_multiplier: int = 4,
    ):
        self.name = name
        self.k = k
        self.child_to_parent = child_to_parent
        self.parents = parents
        self.fetch_multiplier = fetch_multiplier
        self.persist_dir = settings.path(BM25_INDEX_DIR) / name
        self._bm25: bm25s.BM25 | None = None
        self._chunks: list[Chunk] = []
        self._last_ids: list[str] = []

    @staticmethod
    def _tokenize(texts: list[str]):
        return bm25s.tokenize(texts, lower=True, stopwords="en", stemmer=_STEMMER, show_progress=False)

    def build(self, chunks: list[Chunk]) -> "BM25Retriever":
        self._chunks = chunks
        tokens = self._tokenize([c.text for c in chunks])
        self._bm25 = bm25s.BM25()
        self._bm25.index(tokens, show_progress=False)
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        self._bm25.save(str(self.persist_dir), corpus=[c.model_dump() for c in chunks], show_progress=False)
        return self

    def load(self) -> "BM25Retriever":
        self._bm25 = bm25s.BM25.load(str(self.persist_dir), load_corpus=True, show_progress=False)
        self._chunks = [Chunk(**row) for row in self._bm25.corpus]
        # `bm25s.BM25.retrieve` defaults to `self._bm25.corpus` (set by
        # `load_corpus=True` above) when its own `corpus=` argument is not
        # given, returning corpus rows instead of plain integer doc ids —
        # `retrieve_scored` indexes `self._chunks` by id, so that default
        # must be cleared (a freshly-`.build()`-ed index never sets it,
        # which is why this only bites after a reload).
        self._bm25.corpus = None
        return self

    @classmethod
    def from_chunks(
        cls,
        name: str,
        chunks: list[Chunk],
        k: int = 5,
        child_to_parent: dict[str, str] | None = None,
        parents: dict[str, Chunk] | None = None,
        rebuild: bool = False,
    ) -> "BM25Retriever":
        """Build a fresh index, or load a persisted one from `data/indexes/bm25/<name>`
        if it already exists and `rebuild` is False."""
        retriever = cls(name, k=k, child_to_parent=child_to_parent, parents=parents)
        if not rebuild and (retriever.persist_dir / "params.index.json").exists():
            retriever.load()
        else:
            retriever.build(chunks)
        return retriever

    def retrieve_scored(self, question: str, k: int, where: dict | None = None) -> list[tuple[Chunk, float]]:
        """Top-`k` chunks by BM25 score, most relevant first. `where` (e.g.
        `{"paper": ...}`) filters *after* scoring — a wider `n` is scored first
        (bm25s only ranks within the corpus it indexed, so post-filtering is the
        only option) so a filtered query still returns up to `k` results."""
        n = len(self._chunks) if where else min(k, len(self._chunks))
        n = max(n, 1)
        query_tokens = self._tokenize([question])
        results, scores = self._bm25.retrieve(query_tokens, k=n, show_progress=False)
        candidates = [(self._chunks[i], float(s)) for i, s in zip(results[0], scores[0])]
        if where:
            candidates = [(c, s) for c, s in candidates if all(getattr(c, key, None) == val for key, val in where.items())]
        return candidates[:k]

    def retrieve_candidates(self, question: str, k: int, where: dict | None = None) -> list[Chunk]:
        return [chunk for chunk, _score in self.retrieve_scored(question, k, where=where)]

    def retrieve(self, question: str, where: dict | None = None) -> list[Chunk]:
        fetch_k = self.k * self.fetch_multiplier if self.child_to_parent else self.k
        candidates = self.retrieve_candidates(question, fetch_k, where=where)
        result = _swap_to_parent(candidates, self.child_to_parent, self.parents, self.k)
        self._last_ids = [c.id for c in result]
        return result

    def retrieved_ids(self) -> list[str]:
        return self._last_ids

    def clone(
        self, k: int | None = None, child_to_parent: dict[str, str] | None = None, parents: dict[str, Chunk] | None = None
    ) -> "BM25Retriever":
        """A new `BM25Retriever` sharing this one's already-built index (no
        re-tokenising/re-indexing), with a different `k`/parent mapping —
        `retrieval_eval.py` builds the BM25 index once and reuses it across
        every chapter-05 experiment via this method."""
        other = BM25Retriever(
            self.name,
            k=k if k is not None else self.k,
            child_to_parent=child_to_parent,
            parents=parents,
            fetch_multiplier=self.fetch_multiplier,
        )
        other._bm25 = self._bm25
        other._chunks = self._chunks
        return other


# -- chapter 05: fusion ---------------------------------------------------------------------


def rrf_fuse(rankings: list[list[str]], rrf_k: int = 60, top_k: int | None = None) -> list[str]:
    """Reciprocal Rank Fusion (Cormack, Clarke & Buettcher, 2009): combine several
    *ranked* id lists into one, without needing their scores to be on the same
    scale (a cosine similarity and a BM25 score are not comparable numbers, but
    "rank 1" means the same thing in both).

        RRF(d) = sum over rankings r that contain d of  1 / (rrf_k + rank_r(d))

    where `rank_r(d)` is `d`'s 1-indexed position in ranking `r` (documents not
    present in a ranking simply do not contribute a term for it). `rrf_k`
    (60, the value used in the original paper and in Qdrant's own fusion)
    flattens the curve so that a document ranked #1 by one retriever does not
    automatically outrank a document ranked #2-#3 by *every* retriever.
    Returns ids sorted by fused score, best first.
    """
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, doc_id in enumerate(ranking, start=1):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (rrf_k + rank)
    ordered = sorted(scores, key=lambda d: scores[d], reverse=True)
    return ordered[:top_k] if top_k else ordered


def _min_max_normalize(scores: dict[str, float]) -> dict[str, float]:
    if not scores:
        return {}
    values = list(scores.values())
    lo, hi = min(values), max(values)
    if hi == lo:
        return {doc_id: 1.0 for doc_id in scores}
    return {doc_id: (v - lo) / (hi - lo) for doc_id, v in scores.items()}


def weighted_fuse(
    dense_scores: dict[str, float], sparse_scores: dict[str, float], alpha: float = 0.5, top_k: int | None = None
) -> list[str]:
    """Weighted-sum fusion: min-max normalise each retriever's scores to `[0, 1]`
    *independently* first (cosine similarity lives in roughly `[-1, 1]`, BM25
    scores are unbounded and corpus-dependent — comparing them raw would let
    whichever retriever happens to produce bigger numbers dominate), then
    combine as `alpha * dense_norm + (1 - alpha) * sparse_norm`. A document
    missing from one side (retrieved by only one of the two retrievers) counts
    as 0 on that side rather than being dropped. Returns ids sorted by fused
    score, best first.
    """
    dense_norm = _min_max_normalize(dense_scores)
    sparse_norm = _min_max_normalize(sparse_scores)
    ids = set(dense_norm) | set(sparse_norm)
    fused = {doc_id: alpha * dense_norm.get(doc_id, 0.0) + (1 - alpha) * sparse_norm.get(doc_id, 0.0) for doc_id in ids}
    ordered = sorted(fused, key=lambda d: fused[d], reverse=True)
    return ordered[:top_k] if top_k else ordered


class HybridRetriever:
    """Fuse a dense retriever and a `BM25Retriever` over the same child-chunk
    index. Each side is asked for its top `k_each` candidates; the fused
    ranking is computed by `fusion` ("rrf" or "weighted"), then the top `k`
    fused ids are swapped to their parent chunk and de-duplicated exactly like
    `ParentChildRetriever` (pass `child_to_parent`/`parents` for that; leave
    them `None` to fuse at the child level directly).

    A tiny LLM query router can be turned on with `router=True` (see
    `route_paper`): before fusing, it asks the LLM which paper (if any) the
    question names, and if one is found, both sides are queried with
    `where={"paper": ...}`.
    """

    def __init__(
        self,
        dense: DenseRetriever,
        sparse: BM25Retriever,
        fusion: str = "rrf",
        k: int = 5,
        k_each: int = 20,
        rrf_k: int = 60,
        alpha: float = 0.5,
        child_to_parent: dict[str, str] | None = None,
        parents: dict[str, Chunk] | None = None,
        router: bool = False,
        llm_client=None,
        papers: list[dict] | None = None,
    ):
        if fusion not in {"rrf", "weighted"}:
            raise ValueError(f"unknown fusion {fusion!r}, choose 'rrf' or 'weighted'")
        self.dense = dense
        self.sparse = sparse
        self.fusion = fusion
        self.k = k
        self.k_each = k_each
        self.rrf_k = rrf_k
        self.alpha = alpha
        self.child_to_parent = child_to_parent
        self.parents = parents
        self.router = router
        self.llm_client = llm_client or ollama
        self.papers = papers or []
        self._last_ids: list[str] = []
        self._last_where: dict | None = None
        self.router_fired = 0
        self.router_calls = 0

    def _where_for(self, question: str) -> dict | None:
        if not self.router:
            return None
        self.router_calls += 1
        paper_id = route_paper(question, self.papers, llm_client=self.llm_client)
        if paper_id is None:
            return None
        self.router_fired += 1
        return {"paper": paper_id}

    def retrieve(self, question: str) -> list[Chunk]:
        where = self._where_for(question)
        self._last_where = where
        dense_scored = self.dense.retrieve_scored(question, self.k_each, where=where)
        sparse_scored = self.sparse.retrieve_scored(question, self.k_each, where=where)
        by_id: dict[str, Chunk] = {c.id: c for c, _s in dense_scored} | {c.id: c for c, _s in sparse_scored}

        if self.fusion == "rrf":
            dense_ranking = [c.id for c, _s in dense_scored]
            sparse_ranking = [c.id for c, _s in sparse_scored]
            fused_ids = rrf_fuse([dense_ranking, sparse_ranking], rrf_k=self.rrf_k)
        else:
            dense_scores = {c.id: s for c, s in dense_scored}
            sparse_scores = {c.id: s for c, s in sparse_scored}
            fused_ids = weighted_fuse(dense_scores, sparse_scores, alpha=self.alpha)

        ranked_children = [by_id[doc_id] for doc_id in fused_ids]
        fetch_k = self.k * 4 if self.child_to_parent else self.k
        result = _swap_to_parent(ranked_children[:fetch_k], self.child_to_parent, self.parents, self.k)
        self._last_ids = [c.id for c in result]
        return result

    def retrieved_ids(self) -> list[str]:
        return self._last_ids


# -- chapter 05: MMR --------------------------------------------------------------------------


def _cosine(a: list[float], b: list[float]) -> float:
    import numpy as np

    va, vb = np.asarray(a, dtype=np.float64), np.asarray(b, dtype=np.float64)
    denom = np.linalg.norm(va) * np.linalg.norm(vb)
    return float(np.dot(va, vb) / denom) if denom else 0.0


def mmr_select(
    query_embedding: list[float],
    candidates: list[Chunk],
    candidate_embeddings: list[list[float]],
    k: int = 5,
    lambda_mult: float = 0.7,
) -> list[Chunk]:
    """Maximal Marginal Relevance: greedily pick `k` chunks out of `candidates`
    that are each relevant to the query *and* different from what has already
    been picked, trading the two off with `lambda_mult` (1.0 = pure relevance,
    same as plain top-k; 0.0 = pure diversity, ignores the query after the
    first pick):

        MMR = argmax_{d in candidates \\ selected} [
            lambda_mult * sim(d, query) - (1 - lambda_mult) * max_{s in selected} sim(d, s)
        ]

    `candidate_embeddings` must be the same length/order as `candidates` (chapter
    05 gets them for free from the embedding cache — the candidates were already
    embedded once at indexing time, so re-requesting them via
    `ollama.embed_documents` is a 100% cache hit, not a new LLM/embedding call).
    """
    if not candidates:
        return []
    relevance = [_cosine(query_embedding, emb) for emb in candidate_embeddings]
    selected: list[int] = []
    remaining = set(range(len(candidates)))

    while remaining and len(selected) < k:
        if not selected:
            best = max(remaining, key=lambda i: relevance[i])
        else:
            def _mmr_score(i: int) -> float:
                redundancy = max(_cosine(candidate_embeddings[i], candidate_embeddings[j]) for j in selected)
                return lambda_mult * relevance[i] - (1 - lambda_mult) * redundancy

            best = max(remaining, key=_mmr_score)
        selected.append(best)
        remaining.discard(best)

    return [candidates[i] for i in selected]


class MMRRetriever:
    """Dense-search the top `fetch_k` candidates, then re-select `k` of them with
    `mmr_select` for diversity. Candidate embeddings come from the embedder's
    on-disk cache (see `mmr_select`'s docstring) — no extra embedding calls
    beyond the one query embedding.
    """

    def __init__(
        self,
        dense: DenseRetriever,
        embedder=None,
        k: int = 5,
        fetch_k: int = 20,
        lambda_mult: float = 0.7,
        child_to_parent: dict[str, str] | None = None,
        parents: dict[str, Chunk] | None = None,
    ):
        self.dense = dense
        self.embedder = embedder or ollama
        self.k = k
        self.fetch_k = fetch_k
        self.lambda_mult = lambda_mult
        self.child_to_parent = child_to_parent
        self.parents = parents
        self._last_ids: list[str] = []

    def retrieve(self, question: str) -> list[Chunk]:
        candidates = self.dense.retrieve_candidates(question, self.fetch_k)
        query_embedding = self.embedder.embed_query(question)
        candidate_embeddings = self.embedder.embed_documents([c.text for c in candidates])
        fetch_k = self.k * 4 if self.child_to_parent else self.k
        selected = mmr_select(query_embedding, candidates, candidate_embeddings, k=fetch_k, lambda_mult=self.lambda_mult)
        result = _swap_to_parent(selected, self.child_to_parent, self.parents, self.k)
        self._last_ids = [c.id for c in result]
        return result

    def retrieved_ids(self) -> list[str]:
        return self._last_ids


# -- chapter 05: query router (metadata filtering) --------------------------------------------

_ROUTER_SCHEMA = {
    "type": "object",
    "properties": {
        "paper": {"type": ["string", "null"], "description": "the arXiv id of the one paper the question names, or null"},
    },
    "required": ["paper"],
}

_ROUTER_SYSTEM = (
    "You route questions for a RAG system to a single paper filter. Reply with JSON only, "
    "matching the schema. Only name a paper if the question is clearly and specifically about "
    "that one paper (e.g. names its method, title, or arXiv id); if the question could be about "
    "several papers, the whole corpus, or you are not sure, reply with paper: null."
)


def route_paper(question: str, papers: list[dict], llm_client=None) -> str | None:
    """Ask the LLM which paper (by arXiv id) `question` is about, if any.

    `papers` is a list of `{"id": ..., "title": ...}` dicts (the corpus listing
    from `rag_tutorial.corpus.load_papers`). Returns the arXiv id if the model
    named one of `papers`' ids, else `None` — used to build a `where={"paper":
    ...}` metadata filter, so a wrong or hallucinated id never over-filters
    silently (it is checked against the known id list here).
    """
    client = llm_client or ollama
    listing = "\n".join(f"- {p['id']}: {p['title']}" for p in papers)
    reply = client.chat(
        [
            {"role": "system", "content": _ROUTER_SYSTEM},
            {"role": "user", "content": f"Papers:\n{listing}\n\nQuestion: {question}"},
        ],
        json_schema=_ROUTER_SCHEMA,
        temperature=0,
        max_tokens=100,
    )
    data = json.loads(reply)
    paper_id = data.get("paper")
    valid_ids = {p["id"] for p in papers}
    return paper_id if paper_id in valid_ids else None


# -- chapter 05: Qdrant native hybrid ----------------------------------------------------------


class QdrantHybridRetriever:
    """Thin adapter around `stores.QdrantStore.query_hybrid` — Qdrant does the
    dense+sparse fusion server-side in one `query_points` call, instead of
    `HybridRetriever`'s two separate Python-side queries + client-side fusion.
    Needs a running Qdrant (`just up qdrant`); not used in the offline test
    suite (see `tests/test_05_retrieval.py`, `@pytest.mark.slow`).
    """

    def __init__(
        self,
        store: QdrantStore,
        embedder=None,
        k: int = 5,
        k_each: int = 20,
        child_to_parent: dict[str, str] | None = None,
        parents: dict[str, Chunk] | None = None,
    ):
        self.store = store
        self.embedder = embedder or ollama
        self.k = k
        self.k_each = k_each
        self.child_to_parent = child_to_parent
        self.parents = parents
        self._last_ids: list[str] = []
        self.last_seconds = 0.0

    def retrieve(self, question: str, where: dict | None = None) -> list[Chunk]:
        query_embedding = self.embedder.embed_query(question)
        fetch_k = self.k * 4 if self.child_to_parent else self.k
        scored, seconds = self.store.query_hybrid(question, query_embedding, k=fetch_k, k_each=self.k_each, where=where)
        self.last_seconds = seconds
        children = [chunk for chunk, _score in scored]
        result = _swap_to_parent(children, self.child_to_parent, self.parents, self.k)
        self._last_ids = [c.id for c in result]
        return result

    def retrieved_ids(self) -> list[str]:
        return self._last_ids
