"""Offline tests for chapter 12: RAG-app response parsers, settings builders,
and the source-text -> leaf-chunk mapping. No network; fixtures live under
``tests/fixtures/`` and mirror the shapes each app's API returns.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from rag_tutorial import app_kotaemon, app_openwebui, app_ragflow
from rag_tutorial.schema import Chunk

FIXTURES = Path(__file__).parent / "fixtures"


def _load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text())


def _leaves() -> list[Chunk]:
    return [
        Chunk(
            id="leaf-a",
            paper="p1",
            section="s",
            text="Retrieval-Augmented Generation grounds language models in retrieved passages for factual answers.",
            start=0,
            end=10,
        ),
        Chunk(
            id="leaf-b",
            paper="p1",
            section="s",
            text="Completely unrelated paragraph about ocean tides and lunar cycles overhead.",
            start=10,
            end=20,
        ),
    ]


# -- Open WebUI ---------------------------------------------------------------


def test_openwebui_settings_builder_defaults():
    payload = app_openwebui.build_retrieval_settings()
    assert payload == {
        "RAG_EMBEDDING_ENGINE": "ollama",
        "RAG_EMBEDDING_MODEL": "nomic-embed-text",
        "CHUNK_SIZE": 1000,
        "CHUNK_OVERLAP": 100,
        "TOP_K": 5,
        "ENABLE_RAG_HYBRID_SEARCH": False,
        "RAG_RERANKING_MODEL": "",
    }


def test_openwebui_settings_builder_hybrid_rerank():
    payload = app_openwebui.build_retrieval_settings(hybrid=True, reranker_model="cross-encoder/ms-marco-MiniLM-L-6-v2")
    assert payload["ENABLE_RAG_HYBRID_SEARCH"] is True
    assert payload["RAG_RERANKING_MODEL"] == "cross-encoder/ms-marco-MiniLM-L-6-v2"
    assert payload["RAG_EMBEDDING_ENGINE"] == "ollama"


def test_openwebui_named_configs_cover_scoreboard_rows():
    assert set(app_openwebui.NAMED_CONFIGS) == {"default", "hybrid_rerank"}
    assert app_openwebui.NAMED_CONFIGS["default"]["ENABLE_RAG_HYBRID_SEARCH"] is False
    assert app_openwebui.NAMED_CONFIGS["hybrid_rerank"]["ENABLE_RAG_HYBRID_SEARCH"] is True


def test_openwebui_parse_chat_with_citations():
    answer, sources = app_openwebui.parse_chat_response(_load("openwebui_chat_citations.json"))
    assert "Retrieval-Augmented Generation" in answer
    assert len(sources) == 2
    assert sources[0].startswith("Retrieval-Augmented Generation grounds")


def test_openwebui_parse_chat_with_message_sources():
    answer, sources = app_openwebui.parse_chat_response(_load("openwebui_chat_sources.json"))
    assert "Hybrid search" in answer
    assert len(sources) == 2
    assert any("Reciprocal rank fusion" in s for s in sources)


def test_openwebui_parse_chat_rejects_garbage():
    with pytest.raises(ValueError):
        app_openwebui.parse_chat_response({"unexpected": "shape"})


def test_openwebui_parse_live_sources_shape():
    # Shape captured from the live instance (2026-09-09): top-level
    # ``sources`` entries are {"source": {...}, "document": [chunk, ...]}.
    answer, sources = app_openwebui.parse_chat_response(_load("openwebui_chat_live.json"))
    assert answer
    assert len(sources) >= 2
    assert all(isinstance(s, str) and s.strip() for s in sources)


def test_openwebui_parse_auth_and_knowledge_ids():
    assert app_openwebui.parse_auth_response({"token": "abc"}) == "abc"
    assert app_openwebui.parse_auth_response({"access_token": "xyz"}) == "xyz"
    assert app_openwebui.parse_knowledge_response({"id": "kb-1"}) == "kb-1"
    assert app_openwebui.parse_file_upload_response({"id": "file-9"}) == "file-9"
    assert app_openwebui.parse_file_upload_response({"data": {"id": "file-10"}}) == "file-10"
    # Live shape (2026-09-09): top-level id wins over nested data.status dict.
    assert (
        app_openwebui.parse_file_upload_response(
            {"id": "da19f9a7", "filename": "2004.04906.md", "data": {"status": "pending"}, "meta": {}}
        )
        == "da19f9a7"
    )
    with pytest.raises(ValueError):
        app_openwebui.parse_auth_response({"nope": 1})


def test_openwebui_sources_map_to_correct_leaf():
    answer, sources = app_openwebui.parse_chat_response(_load("openwebui_chat_citations.json"))
    assert answer
    mapped, quality = app_openwebui.chunk_texts_to_leaf_chunks(sources, _leaves(), k=2)
    assert mapped[0].id == "leaf-a"
    assert quality["n_strong_in_top10"] >= 1


# -- kotaemon ------------------------------------------------------------------


def test_kotaemon_parse_dict_response():
    answer, cited = app_kotaemon.parse_kotaemon_response(_load("kotaemon_chat.json"))
    assert "cross-encoder" in answer
    assert len(cited) == 2
    assert cited[0].startswith("A cross-encoder reranker")


def test_kotaemon_parse_plain_string():
    answer, cited = app_kotaemon.parse_kotaemon_response("just an answer")
    assert answer == "just an answer"
    assert cited == []


def test_kotaemon_parse_unknown_shape_degrades():
    answer, cited = app_kotaemon.parse_kotaemon_response({"weird": ["shape"]})
    assert isinstance(answer, str) and answer
    assert cited == []


def test_kotaemon_resolve_endpoint_prefers_chat():
    api_map = {"/upload": True, "/chat": True}
    assert app_kotaemon.resolve_endpoint(api_map, ["chat", "ask"]) == "/chat"
    with pytest.raises(KeyError):
        app_kotaemon.resolve_endpoint(api_map, ["predict"])


def test_kotaemon_resolve_live_endpoint_names():
    # Real names from the live main-lite instance (2026-09-09): the message
    # enters via /submit_msg, generation via /chat_fn (session-state bound).
    api_map = {"/submit_msg": True, "/chat_fn": True, "/new_conv": True}
    assert app_kotaemon.resolve_endpoint(api_map, app_kotaemon.CHAT_ENDPOINT_CANDIDATES) == "/submit_msg"


def test_kotaemon_cited_chunks_map_to_correct_leaf():
    _answer, cited = app_kotaemon.parse_kotaemon_response(
        {"output": "x", "references": [{"content": _leaves()[0].text}, "filler words about cooking"]}
    )
    mapped, _quality = app_kotaemon.chunk_texts_to_leaf_chunks(cited, _leaves(), k=2)
    assert mapped[0].id == "leaf-a"


# -- RAGFlow --------------------------------------------------------------------


def test_ragflow_kb_settings_defaults():
    payload = app_ragflow.build_kb_settings()
    assert payload["chunk_len"] == 512
    assert payload["parser_id"] == "naive"
    assert payload["embd_id"] == "nomic-embed-text"
    assert "rerank_id" not in payload


def test_ragflow_named_configs_cover_scoreboard_rows():
    assert set(app_ragflow.NAMED_CONFIGS) == {"default", "tuned"}
    assert app_ragflow.NAMED_CONFIGS["tuned"]["chunk_len"] == 1024
    assert "rerank_id" in app_ragflow.NAMED_CONFIGS["tuned"]


def test_ragflow_parse_completion():
    answer, chunks = app_ragflow.parse_completion_response(_load("ragflow_completion.json"))
    assert "Chunk size 512" in answer
    assert len(chunks) == 2
    assert chunks[0].startswith("A chunk size of 512")


def test_ragflow_parse_completion_unknown_shape_degrades():
    answer, chunks = app_ragflow.parse_completion_response({"surprise": 1})
    assert isinstance(answer, str)
    assert chunks == []


def test_ragflow_parse_dataset_id():
    assert app_ragflow.parse_dataset_response({"data": {"id": "ds-1"}}) == "ds-1"
    assert app_ragflow.parse_dataset_response({"id": "ds-2"}) == "ds-2"
    with pytest.raises(ValueError):
        app_ragflow.parse_dataset_response({"data": {}})


def test_ragflow_chunks_map_to_correct_leaf():
    leaves = [
        Chunk(id="leaf-a", paper="p1", section="s", text="A chunk size of 512 tokens balances context coverage.", start=0, end=10),
        Chunk(id="leaf-b", paper="p1", section="s", text="Baking sourdough requires patience and a hot oven.", start=10, end=20),
    ]
    _answer, chunks = app_ragflow.parse_completion_response(_load("ragflow_completion.json"))
    mapped, _quality = app_ragflow.chunk_texts_to_leaf_chunks(chunks, leaves, k=2)
    assert mapped[0].id == "leaf-a"


# -- CLI smoke (no network: --help only) -----------------------------------------


@pytest.mark.parametrize("module", [app_openwebui, app_kotaemon, app_ragflow])
def test_app_cli_help_lists_commands(module):
    result = CliRunner().invoke(module.app, ["--help"])
    assert result.exit_code == 0
    assert "upload" in result.output
    assert "ask" in result.output
    assert "eval" in result.output
