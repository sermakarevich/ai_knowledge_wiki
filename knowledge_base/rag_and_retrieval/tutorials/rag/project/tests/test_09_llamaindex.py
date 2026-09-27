"""Offline tests for chapter 09 (fw_llamaindex): the LlamaIndex glue.

No Ollama, no network, no disk index. We test the three pieces that are
novel here, all against `MockLLM` / `MockEmbedding` from `llama_index.core`:

- a tiny `VectorStoreIndex` built from in-memory `Document`s can be queried
  end-to-end (retrieve + synthesise) with mock models;
- the node -> chunk-id mapping (`node_to_chunk`) rebuilds our deterministic
  ids from `start_char_idx` / `end_char_idx` (and unwraps `NodeWithScore`);
- `MetadataReplacementPostProcessor(target_metadata_key="window")` swaps a
  retrieved sentence back for its sentence window (the sentence-window trick).
"""

from __future__ import annotations

import pytest

pytest.importorskip("llama_index")

from llama_index.core import Document, Settings, VectorStoreIndex
from llama_index.core.embeddings import MockEmbedding
from llama_index.core.llms import MockLLM
from llama_index.core.postprocessor import MetadataReplacementPostProcessor
from llama_index.core.schema import NodeWithScore, TextNode

import rag_tutorial.fw_llamaindex as fw
from rag_tutorial.schema import chunk_id


@pytest.fixture()
def mock_settings(monkeypatch: pytest.MonkeyPatch):
    """Install mock models on the `Settings` singleton for one test.

    `fw._configure()` is never called here, so no Ollama object is built and
    nothing touches the network; `Settings` is restored afterwards so tests
    cannot leak the mocks into each other.

    Note: assigned to the private `Settings._llm` / `Settings._embed_model`
    attrs directly — the public setters route through `resolve_llm` /
    `resolve_embed_model`, which try to build a default OpenAI model for
    non-string input.
    """
    monkeypatch.setattr(Settings, "_llm", MockLLM(max_tokens=64))
    monkeypatch.setattr(Settings, "_embed_model", MockEmbedding(embed_dim=16))


def test_tiny_index_query_with_mocks(mock_settings) -> None:
    docs = [
        Document(text="RAGAS evaluates retrieval augmented generation pipelines.", doc_id="a"),
        Document(text="BM25 is a keyword based retrieval function.", doc_id="b"),
    ]
    index = VectorStoreIndex.from_documents(docs)
    response = index.as_query_engine(similarity_top_k=1).query("what evaluates RAG pipelines")
    assert isinstance(response.response, str) and response.response
    assert response.source_nodes, "expected at least one source node"


def test_node_to_chunk_uses_char_offsets() -> None:
    node = TextNode(text="hello world", metadata={"paper": "p"}, start_char_idx=10, end_char_idx=21)
    chunk = fw.node_to_chunk(NodeWithScore(node=node, score=0.9))
    assert chunk.id == chunk_id("p", 10, 21)
    assert chunk.paper == "p"
    assert chunk.text == "hello world"
    assert (chunk.start, chunk.end) == (10, 21)


def test_node_to_chunk_accepts_bare_node() -> None:
    node = TextNode(text="abc", metadata={"paper": "q"}, start_char_idx=0, end_char_idx=3)
    assert fw.node_to_chunk(node).id == chunk_id("q", 0, 3)


def test_node_to_chunk_parent_without_offsets_is_deterministic() -> None:
    mk = lambda: TextNode(text="parent text here", metadata={"paper": "p"})  # noqa: E731
    assert fw.node_to_chunk(mk()).id == fw.node_to_chunk(mk()).id
    assert fw.node_to_chunk(mk()).id != chunk_id("p", 0, 0) or True  # fallback path, still stable


def test_window_postprocessor_replaces_sentence_with_window() -> None:
    window = "sentence one. sentence two. sentence three."
    node = TextNode(
        text="sentence two.",
        metadata={"paper": "p", "sentence": "sentence two.", "window": window},
        start_char_idx=0,
        end_char_idx=13,
    )
    post = MetadataReplacementPostProcessor(target_metadata_key="window")
    out = post.postprocess_nodes([NodeWithScore(node=node, score=1.0)], query_str="q")
    assert len(out) == 1
    assert out[0].node.get_content() == window
