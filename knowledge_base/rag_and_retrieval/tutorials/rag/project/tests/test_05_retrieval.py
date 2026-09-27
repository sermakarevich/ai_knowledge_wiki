"""Offline tests for chapter 05: BM25, RRF/weighted fusion, MMR, query routing.

No network, no Qdrant (Qdrant-backed tests are `@pytest.mark.slow`, since they
need a running `just up qdrant`). Embeddings/LLM calls come from
`testing.FakeEmbedder`/`FakeLLM`.
"""

from __future__ import annotations

import json
import uuid

import pytest

from rag_tutorial.retrievers import (
    BM25Retriever,
    HybridRetriever,
    MMRRetriever,
    mmr_select,
    route_paper,
    rrf_fuse,
    weighted_fuse,
)
from rag_tutorial.schema import Chunk, chunk_id
from rag_tutorial.testing import FakeEmbedder, FakeLLM


def _chunk(paper: str, section: str, text: str, start: int = 0, end: int = 1) -> Chunk:
    return Chunk(id=chunk_id(paper, start, end), paper=paper, section=section, text=text, start=start, end=end)


class _FakeDense:
    """A dense retriever stand-in with a fixed, hand-set ranking (no store)."""

    def __init__(self, scored: list[tuple[Chunk, float]]):
        self._scored = scored

    def retrieve_scored(self, question: str, k: int, where=None):
        return self._scored[:k]

    def retrieve_candidates(self, question: str, k: int, where=None):
        return [c for c, _s in self._scored[:k]]


# -- RRF ------------------------------------------------------------------------------


def test_rrf_fuse_expected_order():
    # "a" and "d" each appear in *both* rankings (rank 1 and rank 3), so their
    # RRF scores are a sum of two terms; "b" and "c" each appear in only one
    # ranking (rank 2), a single term. 1/61 + 1/61 > 1/63 + 1/63 > 1/62, so the
    # expected order is a, d, then b/c tied.
    ranking_1 = ["a", "b", "d"]
    ranking_2 = ["a", "c", "d"]
    fused = rrf_fuse([ranking_1, ranking_2], rrf_k=60)
    assert fused[0] == "a"
    assert fused[1] == "d"
    assert set(fused[2:4]) == {"b", "c"}


def test_rrf_fuse_top_k_truncates():
    fused = rrf_fuse([["a", "b", "c"], ["c", "b", "a"]], rrf_k=60, top_k=2)
    assert len(fused) == 2


def test_rrf_fuse_document_only_in_one_ranking_still_scored():
    fused = rrf_fuse([["a", "b"], ["c"]], rrf_k=60)
    assert set(fused) == {"a", "b", "c"}


# -- weighted fusion --------------------------------------------------------------------


def test_weighted_fuse_normalises_each_side_independently():
    # Dense scores live in [-1, 1], sparse (BM25) scores are unbounded -- without
    # independent min-max normalisation the BM25 score of 50 would swamp every
    # dense score. After normalisation, "b" (best on both sides) must win.
    dense_scores = {"a": 0.9, "b": 0.95, "c": 0.1}
    sparse_scores = {"a": 5.0, "b": 50.0, "c": 1.0}
    fused = weighted_fuse(dense_scores, sparse_scores, alpha=0.5)
    assert fused[0] == "b"


def test_weighted_fuse_missing_side_counts_as_zero():
    # "only_dense" is absent from sparse_scores; it must not be dropped, just
    # scored as 0 on the sparse side.
    dense_scores = {"only_dense": 1.0}
    sparse_scores = {"only_sparse": 1.0}
    fused = weighted_fuse(dense_scores, sparse_scores, alpha=0.5)
    assert set(fused) == {"only_dense", "only_sparse"}


def test_weighted_fuse_alpha_favours_dense_when_high():
    dense_scores = {"a": 1.0, "b": 0.0}
    sparse_scores = {"a": 0.0, "b": 1.0}
    fused = weighted_fuse(dense_scores, sparse_scores, alpha=0.9)
    assert fused[0] == "a"


# -- MMR --------------------------------------------------------------------------------


_MMR_QUERY = [1.0, 0.1, 0.0]
_MMR_CANDIDATES_TEXT = ["near-dup-1", "near-dup-2", "diverse"]
_MMR_EMBEDDINGS = [
    [0.95, 0.05, 0.0],  # near-dup-1: highest relevance to the query, picked first
    [1.0, 0.0, 0.0],  # near-dup-2: close behind on relevance, but nearly identical to near-dup-1
    [0.3, 1.0, 0.0],  # diverse: lower relevance, but far from near-dup-1
]


def test_mmr_prefers_diverse_candidate():
    # Pure top-k would take the two near-duplicates; a real diversity weight
    # (lambda=0.5) should swap the second one out for the diverse candidate,
    # since it is redundant with the first pick.
    candidates = [_chunk("p", "s", text) for text in _MMR_CANDIDATES_TEXT]
    selected = mmr_select(_MMR_QUERY, candidates, _MMR_EMBEDDINGS, k=2, lambda_mult=0.5)
    assert [c.text for c in selected] == ["near-dup-1", "diverse"]


def test_mmr_pure_relevance_when_lambda_is_one():
    candidates = [_chunk("p", "s", text) for text in _MMR_CANDIDATES_TEXT]
    selected = mmr_select(_MMR_QUERY, candidates, _MMR_EMBEDDINGS, k=2, lambda_mult=1.0)
    assert [c.text for c in selected] == ["near-dup-1", "near-dup-2"]


def test_mmr_retriever_uses_embedder_cache_not_extra_query_embeddings():
    dense = _FakeDense(
        [
            (_chunk("p", "s", "alpha", 0, 1), 0.9),
            (_chunk("p", "s", "beta", 1, 2), 0.8),
        ]
    )
    embedder = FakeEmbedder(dim=16)
    retriever = MMRRetriever(dense, embedder=embedder, k=2, fetch_k=2, lambda_mult=0.7)
    result = retriever.retrieve("alpha beta")
    assert {c.text for c in result} == {"alpha", "beta"}
    # one query embedding + one embed_documents call over the 2 candidates
    assert embedder.calls.count("alpha beta") == 1


# -- BM25 -----------------------------------------------------------------------------


def test_bm25_retrieves_chunk_with_rare_term(tmp_path, monkeypatch):
    import rag_tutorial.retrievers as retrievers_module

    monkeypatch.setattr(type(retrievers_module.settings), "path", lambda self, p: tmp_path / p)
    chunks = [
        _chunk("p", "s", "the transformer architecture uses self attention", 0, 1),
        _chunk("p", "s", "gradient descent optimises the loss function", 1, 2),
        _chunk("p", "s", "quokkas are marsupials found on rottnest island", 2, 3),
    ]
    retriever = BM25Retriever.from_chunks("test_rare_term", chunks, k=1)
    result = retriever.retrieve("what is a quokka")
    assert result[0].text == chunks[2].text


def test_bm25_where_filters_after_scoring(tmp_path, monkeypatch):
    import rag_tutorial.retrievers as retrievers_module

    monkeypatch.setattr(type(retrievers_module.settings), "path", lambda self, p: tmp_path / p)
    chunks = [
        _chunk("paper_a", "s", "retrieval augmented generation for question answering", 0, 1),
        _chunk("paper_b", "s", "retrieval augmented generation for summarisation", 1, 2),
    ]
    retriever = BM25Retriever.from_chunks("test_where", chunks, k=5)
    result = retriever.retrieve("retrieval augmented generation", where={"paper": "paper_b"})
    assert len(result) == 1
    assert result[0].paper == "paper_b"


def test_bm25_retrieve_after_reload_from_disk(tmp_path, monkeypatch):
    # Regression test: `bm25s.BM25.retrieve()` defaults to its own `.corpus`
    # attribute (set by `load_corpus=True`) when no `corpus=` is passed,
    # returning corpus rows instead of plain integer doc ids -- which broke
    # `retrieve_scored`'s `self._chunks[i]` lookup, but only on a *reloaded*
    # index (a freshly `.build()`-ed one never sets `.corpus`).
    import rag_tutorial.retrievers as retrievers_module

    monkeypatch.setattr(type(retrievers_module.settings), "path", lambda self, p: tmp_path / p)
    chunks = [
        _chunk("p", "s", "self attention transformer architecture", 0, 1),
        _chunk("p", "s", "quokkas are marsupials found on rottnest island", 1, 2),
    ]
    BM25Retriever.from_chunks("test_reload", chunks, k=1)
    reloaded = BM25Retriever.from_chunks("test_reload", chunks, k=1, rebuild=False)
    result = reloaded.retrieve("what is a quokka")
    assert result[0].text == chunks[1].text


def test_bm25_clone_shares_index_without_rebuilding(tmp_path, monkeypatch):
    import rag_tutorial.retrievers as retrievers_module

    monkeypatch.setattr(type(retrievers_module.settings), "path", lambda self, p: tmp_path / p)
    chunks = [_chunk("p", "s", "self attention mechanism", 0, 1)]
    built = BM25Retriever.from_chunks("test_clone", chunks, k=5)
    cloned = built.clone(k=1)
    assert cloned._bm25 is built._bm25
    assert cloned.retrieve("self attention")[0].text == chunks[0].text


# -- hybrid retriever wiring -------------------------------------------------------------


def test_hybrid_retriever_rrf_end_to_end(tmp_path, monkeypatch):
    import rag_tutorial.retrievers as retrievers_module

    monkeypatch.setattr(type(retrievers_module.settings), "path", lambda self, p: tmp_path / p)
    shared_kwargs = dict(paper="p", section="s")
    c1 = _chunk(text="alpha beta gamma", start=0, end=1, **shared_kwargs)
    c2 = _chunk(text="delta epsilon zeta", start=1, end=2, **shared_kwargs)
    dense = _FakeDense([(c1, 0.9), (c2, 0.5)])
    sparse = BM25Retriever.from_chunks("test_hybrid", [c1, c2], k=5)
    retriever = HybridRetriever(dense, sparse, fusion="rrf", k=2, k_each=2)
    result = retriever.retrieve("alpha")
    assert {c.text for c in result} == {"alpha beta gamma", "delta epsilon zeta"}


# -- query router -----------------------------------------------------------------------

_PAPERS = [{"id": "2005.11401", "title": "Retrieval-Augmented Generation"}, {"id": "2401.05856", "title": "Other Paper"}]


def test_route_paper_returns_named_paper():
    llm = FakeLLM(canned={"RAG": json.dumps({"paper": "2005.11401"})})
    result = route_paper("What does the RAG paper propose?", _PAPERS, llm_client=llm)
    assert result == "2005.11401"


def test_route_paper_returns_none_when_llm_says_null():
    llm = FakeLLM(canned={"compare": json.dumps({"paper": None})})
    result = route_paper("How do these papers compare?", _PAPERS, llm_client=llm)
    assert result is None


def test_route_paper_rejects_hallucinated_id():
    llm = FakeLLM(canned={"foo": json.dumps({"paper": "9999.99999"})})
    result = route_paper("foo question", _PAPERS, llm_client=llm)
    assert result is None


# -- Qdrant native hybrid (needs `just up qdrant`) ----------------------------------------


@pytest.mark.slow
def test_qdrant_native_hybrid_retrieves_by_dense_and_sparse():
    from rag_tutorial.schema import chunk_id as _chunk_id
    from rag_tutorial.stores import QdrantStore

    store = QdrantStore(f"test_ch05_{uuid.uuid4().hex[:8]}", dim=16)
    try:
        store.reset()
        chunks = [
            _chunk("p", "s", "self attention transformer architecture", 0, 1),
            _chunk("p", "s", "gradient descent optimises the loss function", 1, 2),
        ]
        chunks = [
            Chunk(id=_chunk_id("p", i, i + 1), paper="p", section="s", text=c.text, start=i, end=i + 1)
            for i, c in enumerate(chunks)
        ]
        embeddings = [[1.0] + [0.0] * 15, [0.0] * 15 + [1.0]]
        store.add(chunks, embeddings)
        results, seconds = store.query_hybrid("self attention transformer", embeddings[0], k=1, k_each=5)
        assert results[0][0].text == chunks[0].text
        assert seconds >= 0.0
    finally:
        store.client.delete_collection(store.collection_name)
