"""Offline tests for chapter 03: fixed-size token chunking, the Chroma store

round trip, and the prompt builder. No network calls; Chroma runs in-process
against a tmp_path directory and embeddings come from `testing.FakeEmbedder`.
"""

from __future__ import annotations

from rag_tutorial.chunkers import CHUNKERS, fixed_token_chunks
from rag_tutorial.llm import count_tokens
from rag_tutorial.prompts import SYSTEM_PROMPT, build_messages, format_context
from rag_tutorial.schema import Document
from rag_tutorial.stores import ChromaStore
from rag_tutorial.testing import FakeEmbedder

_SAMPLE_TEXT = (
    "# 1 Introduction\n"
    + ("Retrieval augmented generation combines a retriever with a generator. " * 60)
    + "\n## 1.1 Motivation\n"
    + ("Long documents do not fit in a single prompt window so we must chunk them. " * 60)
)


def _doc(paper: str = "2005.11401", text: str = _SAMPLE_TEXT) -> Document:
    return Document.from_markdown(paper, "Sample Paper", text)


# -- fixed_token_chunks -----------------------------------------------------------------


def test_fixed_token_chunks_respects_size_and_overlap():
    doc = _doc()
    chunks = fixed_token_chunks(doc, size=64, overlap=16)
    assert len(chunks) > 1
    for chunk in chunks[:-1]:
        assert count_tokens(chunk.text) == 64
    assert count_tokens(chunks[-1].text) <= 64


def test_fixed_token_chunks_overlap_shares_text():
    doc = _doc()
    chunks = fixed_token_chunks(doc, size=64, overlap=16)
    # consecutive chunks must overlap: the second chunk starts before the first ends
    assert chunks[1].start < chunks[0].end


def test_fixed_token_chunks_covers_whole_text():
    doc = _doc()
    chunks = fixed_token_chunks(doc, size=64, overlap=16)
    assert chunks[0].start == 0
    assert chunks[-1].end == len(doc.text)
    # no gaps: each next chunk starts at or before the previous chunk's end
    for prev, nxt in zip(chunks, chunks[1:]):
        assert nxt.start <= prev.end


def test_fixed_token_chunks_ids_are_deterministic():
    doc = _doc()
    first = fixed_token_chunks(doc, size=64, overlap=16)
    second = fixed_token_chunks(doc, size=64, overlap=16)
    assert [c.id for c in first] == [c.id for c in second]
    assert len(first[0].id) == 16


def test_fixed_token_chunks_rejects_overlap_ge_size():
    doc = _doc()
    try:
        fixed_token_chunks(doc, size=32, overlap=32)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for overlap >= size")


def test_fixed_token_chunks_carries_section():
    doc = _doc()
    chunks = fixed_token_chunks(doc, size=64, overlap=16)
    sections = {c.section for c in chunks}
    assert "1 Introduction" in sections
    assert any("1.1 Motivation" in s for s in sections)


def test_chunkers_registry_has_fixed():
    assert CHUNKERS["fixed"] is fixed_token_chunks


# -- ChromaStore ------------------------------------------------------------------------


def test_chroma_store_round_trip(tmp_path):
    embedder = FakeEmbedder(dim=32)
    doc = _doc()
    chunks = fixed_token_chunks(doc, size=64, overlap=16)

    store = ChromaStore("test_collection", persist_dir=tmp_path / "chroma")
    embeddings = embedder.embed_documents([c.text for c in chunks])
    store.add(chunks, embeddings)

    assert store.count() == len(chunks)

    query_embedding = embedder.embed_query(chunks[0].text)
    results = store.query(query_embedding, k=3)
    assert len(results) == 3
    top_chunk, top_score = results[0]
    assert top_chunk.id == chunks[0].id
    assert top_score > 0.99  # querying with a chunk's own embedding should match itself


def test_chroma_store_reset_clears_collection(tmp_path):
    embedder = FakeEmbedder(dim=32)
    doc = _doc()
    chunks = fixed_token_chunks(doc, size=64, overlap=16)

    store = ChromaStore("test_collection_reset", persist_dir=tmp_path / "chroma")
    store.add(chunks, embedder.embed_documents([c.text for c in chunks]))
    assert store.count() == len(chunks)

    store.reset()
    assert store.count() == 0


# -- prompts ------------------------------------------------------------------------------


def test_format_context_cites_paper_short_names():
    triples = [("raptor", "3 Method", "RAPTOR builds a tree of summaries.")]
    rendered = format_context(triples)
    assert "[raptor §3 Method]" in rendered
    assert "RAPTOR builds a tree of summaries." in rendered


def test_build_messages_includes_system_prompt_and_question():
    messages = build_messages("What does RAPTOR do?", [("raptor", "3 Method", "It clusters chunks recursively.")])
    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == SYSTEM_PROMPT
    assert "What does RAPTOR do?" in messages[1]["content"]
    assert "[raptor §3 Method]" in messages[1]["content"]


def test_build_messages_with_no_chunks_still_asks_the_question():
    messages = build_messages("Unanswerable question?", [])
    assert "Unanswerable question?" in messages[1]["content"]
