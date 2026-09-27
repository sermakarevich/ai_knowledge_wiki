"""Smoke tests for the chapter 00 skeleton: Neo4j+APOC and the Ollama embed call."""

import pytest

from graph_rag.db import get_driver
from graph_rag.llm import chat, embed


def test_apoc_version():
    with get_driver() as driver:
        version = driver.execute_query(
            "RETURN apoc.version() AS v", database_="neo4j"
        ).records[0]["v"]
    assert isinstance(version, str)
    assert version


def test_embed_dimensions():
    vectors = embed(["hi"])
    assert len(vectors[0]) == 768


@pytest.mark.slow
def test_chat_replies():
    reply = chat([{"role": "user", "content": "Reply with one word: ok"}])
    assert isinstance(reply, str)
    assert reply.strip()
