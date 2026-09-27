"""Offline tests for chapter 11: RAPTOR tree building + collapsed retrieval and
the LightRAG chunk-mapping helper. No network; LLM/embeddings come from
`testing.FakeEmbedder`/`FakeLLM`, Chroma runs in-process on `tmp_path`.
"""

from __future__ import annotations

import pytest

from rag_tutorial.raptor import (
    _node_to_chunk,
    build_tree,
    cluster_embeddings,
    summarize_cluster,
    tree_shape,
)
from rag_tutorial.schema import Chunk, chunk_id
from rag_tutorial.stores import ChromaStore
from rag_tutorial.sys_lightrag import extract_lightrag_chunks, map_context_to_chunks
from rag_tutorial.testing import FakeEmbedder, FakeLLM


def _leaves(n: int = 30) -> list[Chunk]:
    topics = ["retrieval", "reranking", "chunking", "evaluation", "embeddings", "graphs"]
    out = []
    for i in range(n):
        topic = topics[i % len(topics)]
        text = f"Paper section about {topic} with distinctive terms alpha{i} beta{i} gamma{i}. " * 4
        out.append(
            Chunk(
                id=chunk_id(f"paper{i % 3}", i * 100, i * 100 + 50),
                paper=f"paper{i % 3}",
                section=f"section {i}",
                text=text,
                start=i * 100,
                end=i * 100 + 50,
            )
        )
    return out


# -- clustering ----------------------------------------------------------------------


def test_cluster_embeddings_target_size():
    vecs = FakeEmbedder(dim=16).embed([c.text for c in _leaves()])
    labels = cluster_embeddings(vecs, target_size=10)
    assert len(labels) == 30
    assert len(set(labels)) == 3  # 30 nodes / target 10 -> 3 clusters


def test_cluster_embeddings_edge_cases():
    assert cluster_embeddings([]) == []
    assert cluster_embeddings([[1.0, 0.0]]) == [0]
    assert cluster_embeddings([[1.0, 0.0]] * 4, target_size=10) == [0] * 4


# -- tree building -------------------------------------------------------------------


def test_build_tree_terminates_with_levels():
    leaves = _leaves()
    embedder = FakeEmbedder(dim=16)
    nodes, summary_calls = build_tree(leaves, embed_fn=embedder.embed_documents, llm=FakeLLM(), target_size=10)
    shape = tree_shape(nodes)
    assert shape["levels"]["0"] == 30
    assert shape["depth"] >= 1
    assert summary_calls > 0
    assert shape["n_summaries"] == summary_calls
    top = max(n["level"] for n in nodes)
    assert shape["levels"][str(top)] <= 5  # recursion stops at <= 5 top nodes


def test_summaries_reference_children():
    leaves = _leaves()
    nodes, _ = build_tree(leaves, embed_fn=FakeEmbedder(dim=16).embed_documents, llm=FakeLLM(), target_size=10)
    leaf_ids = {c.id for c in leaves}
    summaries = [n for n in nodes if n["level"] > 0]
    assert summaries
    for summary in summaries:
        assert summary["children"], "every summary must reference its cluster members"
        for child_id in summary["children"]:
            assert child_id in leaf_ids | {n["id"] for n in nodes if n["level"] == summary["level"] - 1}


def test_summarize_cluster_uses_llm():
    llm = FakeLLM()
    summary = summarize_cluster(["first excerpt", "second excerpt"], llm=llm)
    assert isinstance(summary, str) and summary
    assert len(llm.calls) == 1


# -- collapsed retrieval --------------------------------------------------------------


def test_collapsed_retrieval_returns_leaves_and_summaries(tmp_path):
    leaves = _leaves()
    embedder = FakeEmbedder(dim=16)
    nodes, _ = build_tree(leaves, embed_fn=embedder.embed_documents, llm=FakeLLM(), target_size=10)
    by_id = {c.id: c for c in leaves}
    store_chunks = [by_id[n["id"]] if n["level"] == 0 else _node_to_chunk(n) for n in nodes]

    store = ChromaStore("test_11_raptor", persist_dir=tmp_path)
    store.add(store_chunks, embedder.embed([c.text for c in store_chunks]))

    summary_text = next(n["text"] for n in nodes if n["level"] > 0)
    scored = store.query(embedder.embed_query(summary_text), k=5)
    assert len(scored) == 5
    sections = [c.section for c, _s in scored]
    assert any(s.startswith("summary/") for s in sections), "summaries must be retrievable"
    assert any(not s.startswith("summary/") for s in sections), "leaves must stay retrievable"


# -- LightRAG chunk mapping ------------------------------------------------------------


def test_map_context_to_chunks_small_example():
    chunks = [
        Chunk(id="a", paper="p1", section="s", text="knowledge graphs link entities with typed relations", start=0, end=10),
        Chunk(id="b", paper="p1", section="s", text="unrelated paragraph about ocean tides and the moon", start=10, end=20),
    ]
    context = "Retrieved evidence: knowledge graphs link entities with typed relations. They help multi-hop QA."
    ranked = map_context_to_chunks(context, chunks)
    assert ranked[0][0].id == "a"
    assert ranked[0][1] >= 0.5
    assert ranked[1][0].id == "b"
    assert ranked[1][1] < ranked[0][1]


def test_lightrag_query_modes_exist():
    lightrag = pytest.importorskip("lightrag")
    for mode in ("naive", "local", "global", "hybrid", "mix"):
        param = lightrag.QueryParam(mode=mode, only_need_context=True)
        assert param.mode == mode


def test_extract_lightrag_chunks_ordered():
    context = (
        "Reference Document List:\n```json\n"
        '{"reference_id": "", "content": "second chunk text here"}\n'
        '{"reference_id": "", "content": "first chunk text here"}\n'
        "```\nEntities:\n```json\n"
        '{"entity": "RAG", "type": "method", "description": "retrieval"}\n'
        "```"
    )
    chunks = extract_lightrag_chunks(context)
    assert chunks == ["second chunk text here", "first chunk text here"]


def test_map_context_prefers_earlier_lightrag_chunk():
    # Both leaves appear verbatim in the context, but LightRAG ranked the
    # chunk containing "b" first — "b" must win despite overlap ties.
    leaf_a = "alpha leaf about evaluation metrics for question answering systems"
    leaf_b = "beta leaf about ocean tides and lunar cycles in detail here"
    filler = "filler words " * 60
    context = (
        "Reference Document List:\n```json\n"
        '{"reference_id": "", "content": "' + filler + leaf_b + '"}\n'
        '{"reference_id": "", "content": "' + filler + leaf_a + '"}\n'
        "```"
    )
    chunks = [
        Chunk(id="a", paper="p1", section="s", text=leaf_a, start=0, end=10),
        Chunk(id="b", paper="p1", section="s", text=leaf_b, start=10, end=20),
    ]
    ranked = map_context_to_chunks(context, chunks)
    assert ranked[0][0].id == "b"
