"""Offline tests for chapter 04's chunking strategies and retrievers. No network:
embeddings come from `testing.FakeEmbedder`, the contextual chunker's LLM calls
come from `testing.FakeLLM`.
"""

from __future__ import annotations

import re

from rag_tutorial.chunkers import (
    CHUNKERS,
    contextual_chunks,
    fixed_token_chunks,
    markdown_chunks,
    parent_child_chunks,
    parent_chunks,
    recursive_chunks,
    semantic_chunks,
    sentence_chunks,
    sentence_window_chunks,
)
from rag_tutorial.retrievers import DenseRetriever, ParentChildRetriever, SentenceWindowRetriever
from rag_tutorial.schema import Document
from rag_tutorial.stores import ChromaStore
from rag_tutorial.testing import FakeEmbedder, FakeLLM

_WHITESPACE_RE = re.compile(r"\s+")

_SAMPLE_TEXT = (
    "# 1 Introduction\n"
    + ("Retrieval augmented generation combines a retriever with a generator. " * 40)
    + "\n## 1.1 Motivation\n"
    + ("Long documents do not fit in a single prompt window so we must chunk them. " * 40)
    + "\n# 2 Method\n"
    + ("The method embeds sentences and clusters them by similarity. " * 40)
)


def _doc(paper: str = "2005.11401", text: str = _SAMPLE_TEXT) -> Document:
    return Document.from_markdown(paper, "Sample Paper", text)


def _normalize(text: str) -> str:
    return _WHITESPACE_RE.sub(" ", text).strip()


def _covers_original(chunks, doc, strip_headers: bool = False) -> None:
    """Concatenated chunk texts must contain the whole document text (modulo
    whitespace, and modulo any contextual header lines when `strip_headers`)."""
    if strip_headers:
        bodies = []
        for c in chunks:
            body = c.text.split("\n", 1)[1] if "\n" in c.text else c.text
            bodies.append(body)
        covered = _normalize(" ".join(bodies))
    else:
        covered = _normalize(" ".join(c.text for c in chunks))
    for original_piece in _normalize(doc.text).split():
        assert original_piece in covered


# -- registry --------------------------------------------------------------------------


def test_registry_has_all_strategies():
    for name in ["fixed", "recursive", "sentence", "markdown", "semantic", "parent_child", "sentence_window", "contextual"]:
        assert name in CHUNKERS


# -- recursive ---------------------------------------------------------------------------


def test_recursive_chunks_respect_size_budget():
    doc = _doc()
    chunks = recursive_chunks(doc, size=128, overlap=16)
    assert len(chunks) > 1
    for chunk in chunks:
        assert chunk.meta["strategy"] == "recursive"


def test_recursive_chunks_cover_whole_text():
    doc = _doc()
    chunks = recursive_chunks(doc, size=128, overlap=16)
    _covers_original(chunks, doc)


def test_recursive_chunks_ids_deterministic():
    doc = _doc()
    a = recursive_chunks(doc, size=128, overlap=16)
    b = recursive_chunks(doc, size=128, overlap=16)
    assert [c.id for c in a] == [c.id for c in b]


# -- sentence -----------------------------------------------------------------------------


def test_sentence_chunks_group_size_and_overlap():
    doc = _doc()
    chunks = sentence_chunks(doc, n_sentences=5, overlap=1)
    assert len(chunks) > 1
    for chunk in chunks[:-1]:
        assert chunk.meta["n_sentences"] == 5


def test_sentence_chunks_cover_whole_text():
    doc = _doc()
    chunks = sentence_chunks(doc, n_sentences=5, overlap=1)
    _covers_original(chunks, doc)


# -- markdown -------------------------------------------------------------------------------


def test_markdown_chunks_start_with_header_line():
    doc = _doc()
    chunks = markdown_chunks(doc, size=128, overlap=16)
    assert chunks
    for chunk in chunks:
        first_line = chunk.text.split("\n", 1)[0]
        assert first_line == chunk.meta["header"]
        assert doc.title in first_line


def test_markdown_chunks_cover_whole_text():
    # markdown_chunks only covers section *bodies* (text after the heading line,
    # per doc.sections) — the heading markers themselves ("#", "##") are not part
    # of any section body, so compare against the sections' own text.
    doc = _doc()
    chunks = markdown_chunks(doc, size=128, overlap=16)
    bodies = [c.text.split("\n", 1)[1] if "\n" in c.text else "" for c in chunks]
    covered = _normalize(" ".join(bodies))
    expected = _normalize("".join(doc.text[s.start : s.end] for s in doc.sections))
    for word in expected.split():
        assert word in covered


def test_markdown_chunks_split_long_sections_by_size():
    doc = _doc()
    chunks = markdown_chunks(doc, size=64, overlap=8)
    by_section: dict[str, int] = {}
    for chunk in chunks:
        by_section[chunk.section] = by_section.get(chunk.section, 0) + 1
    assert any(count > 1 for count in by_section.values())


# -- semantic -------------------------------------------------------------------------------


def test_semantic_chunks_splits_two_topic_text():
    text = ("Cats are small furry mammals that like to sleep. " * 6) + ("Rockets launch payloads into orbit using fuel. " * 6)
    doc = _doc(text=text)
    chunks = semantic_chunks(doc, FakeEmbedder(dim=64), percentile=20)
    assert len(chunks) >= 2


def test_semantic_chunks_cover_whole_text():
    text = ("Cats are small furry mammals that like to sleep. " * 6) + ("Rockets launch payloads into orbit using fuel. " * 6)
    doc = _doc(text=text)
    chunks = semantic_chunks(doc, FakeEmbedder(dim=64), percentile=20)
    _covers_original(chunks, doc)


def test_semantic_chunks_single_sentence_document():
    doc = _doc(text="Just one sentence here.")
    chunks = semantic_chunks(doc, FakeEmbedder(dim=32))
    assert len(chunks) == 1


# -- parent/child ---------------------------------------------------------------------------


def test_parent_child_children_point_to_existing_parents():
    doc = _doc()
    parents = {p.id: p for p in parent_chunks(doc, size=200, overlap=32)}
    children = parent_child_chunks(doc, parent_size=200, parent_overlap=32, child_size=48, child_overlap=8)
    assert children
    for child in children:
        assert child.meta["parent_id"] in parents


def test_parent_child_children_are_smaller_than_parents():
    doc = _doc()
    children = parent_child_chunks(doc, parent_size=200, parent_overlap=32, child_size=48, child_overlap=8)
    for child in children:
        assert len(child.text) < 200 * 6  # generous char/token upper bound


# -- sentence window ------------------------------------------------------------------------


def test_sentence_window_chunks_are_single_sentences():
    doc = _doc()
    chunks = sentence_window_chunks(doc, window=3)
    assert len(chunks) > 1
    for chunk in chunks:
        assert chunk.meta["window"] == 3


def test_sentence_window_retriever_expands_window():
    doc = _doc()
    chunks = sentence_window_chunks(doc, window=2)
    embedder = FakeEmbedder(dim=32)

    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        store = ChromaStore("test_sentence_window", persist_dir=tmp)
        store.add(chunks, embedder.embed_documents([c.text for c in chunks]))
        retriever = SentenceWindowRetriever(store, {doc.paper: doc}, embedder=embedder, k=1, window=2)
        target = chunks[5]
        result = retriever.retrieve(target.text)
        assert len(result) == 1
        assert len(result[0].text) >= len(target.text)
        assert target.text in result[0].text


# -- contextual -----------------------------------------------------------------------------


def test_contextual_chunks_prepend_llm_context():
    doc = _doc()
    llm = FakeLLM()
    chunks = contextual_chunks(doc, llm, abstract="A short paper about RAG.", size=128, overlap=16)
    assert chunks
    for chunk in chunks:
        assert chunk.text.startswith("echo:") or len(chunk.text) > 0
    assert len(llm.calls) == len(chunks)


def test_contextual_chunks_keep_same_ids_as_markdown():
    doc = _doc()
    md_chunks = markdown_chunks(doc, size=128, overlap=16)
    ctx_chunks = contextual_chunks(doc, FakeLLM(), abstract="abstract", size=128, overlap=16)
    assert [c.id for c in md_chunks] == [c.id for c in ctx_chunks]


# -- ParentChildRetriever ---------------------------------------------------------------------


def test_parent_child_retriever_swaps_and_dedupes():
    doc = _doc()
    parents = {p.id: p for p in parent_chunks(doc, size=200, overlap=32)}
    children = parent_child_chunks(doc, parent_size=200, parent_overlap=32, child_size=48, child_overlap=8)
    child_to_parent = {c.id: c.meta["parent_id"] for c in children}

    embedder = FakeEmbedder(dim=32)
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        store = ChromaStore("test_parent_child", persist_dir=tmp)
        store.add(children, embedder.embed_documents([c.text for c in children]))
        retriever = ParentChildRetriever(store, child_to_parent, parents, embedder=embedder, k=2)
        result = retriever.retrieve(children[0].text)
        assert 1 <= len(result) <= 2
        for chunk in result:
            assert chunk.id in parents


# -- DenseRetriever -----------------------------------------------------------------------------


def test_dense_retriever_returns_k_chunks_and_ids():
    doc = _doc()
    chunks = fixed_token_chunks(doc, size=64, overlap=16)
    embedder = FakeEmbedder(dim=32)
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        store = ChromaStore("test_dense", persist_dir=tmp)
        store.add(chunks, embedder.embed_documents([c.text for c in chunks]))
        retriever = DenseRetriever(store, embedder=embedder, k=3)
        result = retriever.retrieve(chunks[0].text)
        assert len(result) == 3
        assert retriever.retrieved_ids() == [c.id for c in result]
