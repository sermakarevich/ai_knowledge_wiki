"""Offline tests for chapter 07: rerankers + query transforms.

No network, no HF model load, no Ollama. Reranker scoring is exercised through
a concrete `_score_batch` stand-in (or `FakeLLM` for the LLM reranker) and the
disk cache is pointed at `tmp_path`. Query transforms are driven by `FakeLLM`.
The heavy model classes (CrossEncoder / FlashRank / ColBERT) are *not*
constructed here — those need the cached checkpoints and are covered by
`just rerank-eval` smoke runs, not unit tests.
"""

from __future__ import annotations

import pytest

from rag_tutorial.query_transforms import (
    compress,
    decompose,
    hyde,
    lost_in_the_middle_reorder,
    multi_query,
    step_back,
)
from rag_tutorial.rerankers import LLMReranker, Reranker
from rag_tutorial.schema import Chunk, chunk_id
from rag_tutorial.testing import FakeLLM


def _chunk(text: str, paper: str = "p") -> Chunk:
    return Chunk(id=chunk_id(paper, 0, len(text)), paper=paper, section="s", text=text, start=0, end=len(text))


# -- concrete Reranker stand-in (scores by text length, no model) --------------


class _LengthReranker(Reranker):
    """Scores each chunk by `len(text)` (longer = higher), so the best-first
    order + cache-hit behaviour can be asserted without a real model. Mirrors
    the real backends by incrementing `n_calls` once per cache-miss batch."""

    model_slug = "length-reranker"

    def _score_batch(self, question: str, chunks: list[Chunk]) -> list[float]:
        self.n_calls += 1
        return [float(len(c.text)) for c in chunks]


def test_rerank_orders_best_first_and_truncates(tmp_path):
    rr = _LengthReranker(cache_dir=tmp_path)
    short, mid, long = _chunk("a"), _chunk("dd"), _chunk("bbb")
    # input deliberately unsorted: [short, mid, long]
    assert [c.text for c in rr.rerank("q", [short, mid, long], k=None)] == ["bbb", "dd", "a"]
    assert [c.text for c in rr.rerank("q", [short, mid, long], k=2)] == ["bbb", "dd"]


def test_rerank_clamps_k_to_pool_size(tmp_path):
    rr = _LengthReranker(cache_dir=tmp_path)
    a, b = _chunk("a"), _chunk("bbbb")
    assert len(rr.rerank("q", [a, b], k=10)) == 2


def test_rerank_empty_pool_is_empty(tmp_path):
    assert _LengthReranker(cache_dir=tmp_path).rerank("q", [], k=5) == []


def test_rerank_cache_hit_skips_scoring(tmp_path):
    rr = _LengthReranker(cache_dir=tmp_path)
    pool = [_chunk("a"), _chunk("dd"), _chunk("bbb")]
    rr.rerank("same-question", pool)
    n_after_first = rr.n_calls
    assert n_after_first == 1  # one fresh batch on the first pass
    # identical (question, chunks): everything served from the disk cache
    rr.rerank("same-question", pool)
    assert rr.n_calls == n_after_first  # no second scoring pass
    # a different question is a cache miss for the same chunks
    rr.rerank("different-question", pool)
    assert rr.n_calls == n_after_first + 1


# -- LLMReranker.parse_order (static / pure) -----------------------------------


def test_parse_order_simple_space_separated():
    assert LLMReranker._parse_order("3 1 2", 3) == [2, 0, 1]


def test_parse_order_commas_and_noise():
    assert LLMReranker._parse_order("3, 1, 2\n", 3) == [2, 0, 1]
    assert LLMReranker._parse_order("ok: 2, 3, 1.", 3) == [1, 2, 0]


def test_parse_order_drops_out_of_range_then_fills():
    # "5" is invalid for a 3-item pool -> dropped; "1" kept; rest filled in order
    assert LLMReranker._parse_order("5 1", 3) == [0, 1, 2]


def test_parse_order_keeps_first_dup_drop():
    assert LLMReranker._parse_order("1 1 2", 3) == [0, 1, 2]


def test_parse_order_garbage_falls_back_to_identity():
    assert LLMReranker._parse_order("no numbers here", 3) == [0, 1, 2]


def test_llm_listwise_reorders_via_fake(tmp_path):
    # "3 1 2" over 3 passages -> local order [2,0,1] -> chunk[2] best, then [0], then [1]
    client = FakeLLM({"Order:": "3 1 2"})
    rr = LLMReranker(mode="listwise", client=client, cache_dir=tmp_path)
    first, second, third = _chunk("first"), _chunk("second"), _chunk("third")
    out = rr.rerank("q", [first, second, third], k=3)
    assert [c.text for c in out] == ["third", "first", "second"]
    assert rr.n_calls == 1  # one chat call per listwise pass


def test_llmreranker_rejects_bad_mode():
    with pytest.raises(ValueError):
        LLMReranker(mode="sideways")


# -- query transforms (driven by FakeLLM) ---------------------------------------


def test_multi_query_strips_numbering_and_counts_calls():
    client = FakeLLM({"Queries:": "1. attention mechanism\n2. softmax weighting\n3. token mixing"})
    res = multi_query("what is attention", client, n=3)
    assert res.variants == ["attention mechanism", "softmax weighting", "token mixing"]
    assert res.n_llm_calls == 1


def test_multi_query_drops_verbatim_repeat_of_question():
    client = FakeLLM({"Queries:": "1. what is attention\n2. attention mechanism\n3. softmax weighting"})
    res = multi_query("what is attention", client, n=3)
    assert res.variants == ["attention mechanism", "softmax weighting"]  # the repeat is dropped


def test_multi_query_rejects_bad_n():
    with pytest.raises(ValueError):
        multi_query("q", FakeLLM(), n=0)


def test_hyde_returns_single_passage():
    client = FakeLLM({"Synthetic answer:": "The block uses scaled dot-product attention."})
    res = hyde("how does a transformer block work", client)
    assert res.variants == ["The block uses scaled dot-product attention."]
    assert res.n_llm_calls == 1


def test_step_back_single_variant():
    client = FakeLLM({"Step-back question:": "How do attention layers improve sequence modelling"})
    res = step_back("what does the softmax in attention compute", client)
    assert res.variants == ["How do attention layers improve sequence modelling"]
    assert res.n_llm_calls == 1


def test_decompose_two_subquestions():
    client = FakeLLM({"Sub-questions:": "1. what is a transformer\n2. how is it trained"})
    res = decompose("how are transformers trained", client)
    assert res.variants == ["what is a transformer", "how is it trained"]
    assert res.n_llm_calls == 1


def test_decompose_single_line_is_noop():
    # one line came back -> the transform reports empty so the driver falls back
    client = FakeLLM({"Sub-questions:": "1. what is a transformer"})
    res = decompose("how are transformers trained", client)
    assert res.variants == []
    assert res.n_llm_calls == 1


def test_compress_drops_not_relevant_chunks():
    c_alpha = _chunk("alpha beta gamma", paper="pa")
    c_delta = _chunk("delta epsilon", paper="pd")
    client = FakeLLM(
        {
            "alpha beta gamma": "not relevant",  # keyed on the embedded passage text
            "delta epsilon": "the kept detail 42",
        }
    )
    res = compress([c_alpha, c_delta], "what is the answer", client)
    assert len(res.compressed) == 1
    assert res.compressed[0][0].text == "delta epsilon"
    assert res.compressed[0][1] == "the kept detail 42"
    assert res.n_llm_calls == 2  # one chat call per chunk (not batched)


def test_compress_empty_pool_is_noop():
    res = compress([], "q", FakeLLM())
    assert res.compressed == []
    assert res.n_llm_calls == 0


def test_lost_in_the_middle_moves_second_to_end():
    chunks = [_chunk("a%02d" % i) for i in range(5)]
    out = lost_in_the_middle_reorder(chunks, k=5)  # [a,b,c,d,e] -> [a,c,d,e,b]
    assert [id(c) for c in out] == [id(chunks[0])] + [id(c) for c in chunks[2:]] + [id(chunks[1])]
    # k=3 -> top [a,b,c] -> [a,c,b]
    assert [id(c) for c in lost_in_the_middle_reorder(chunks, k=3)] == [id(chunks[0]), id(chunks[2]), id(chunks[1])]
    # fewer than 2 chunks: nothing to move
    assert lost_in_the_middle_reorder(chunks, k=1) == [chunks[0]]
