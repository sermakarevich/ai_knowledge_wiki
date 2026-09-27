"""Offline tests for chapter 00: cache round-trip, embedding cache granularity,
FakeEmbedder determinism, token counting, and PDF parsing. No network calls."""

from __future__ import annotations

import io

import httpx
import pytest

from rag_tutorial.llm import Ollama, count_tokens
from rag_tutorial.testing import FakeEmbedder, FakeLLM


def _mock_transport(responses: list[dict]):
    """An httpx MockTransport that pops one canned JSON response per request."""
    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        response = responses[calls["n"]]
        calls["n"] += 1
        return httpx.Response(200, json=response)

    return httpx.MockTransport(handler), calls


def test_chat_cache_round_trip(tmp_path, monkeypatch):
    ollama = Ollama(base_url="http://fake", cache_dir=tmp_path)

    call_count = {"n": 0}

    def fake_post(self, path, payload, attempts=3):
        call_count["n"] += 1
        return {"message": {"content": "OK"}, "prompt_eval_count": 5, "eval_count": 1, "total_duration": 100}

    monkeypatch.setattr(Ollama, "_post", fake_post)

    messages = [{"role": "user", "content": "hello"}]
    first = ollama.chat(messages)
    second = ollama.chat(messages)

    assert first == second == "OK"
    assert call_count["n"] == 1  # second call hit the cache, no HTTP
    assert ollama.stats.hits == 1
    assert ollama.stats.misses == 1


def test_embed_cache_is_per_text(tmp_path, monkeypatch):
    ollama = Ollama(base_url="http://fake", cache_dir=tmp_path)

    seen_batches: list[list[str]] = []

    def fake_post(self, path, payload, attempts=3):
        seen_batches.append(payload["input"])
        return {"embeddings": [[float(len(t))] for t in payload["input"]]}

    monkeypatch.setattr(Ollama, "_post", fake_post)

    first = ollama.embed(["alpha", "beta"])
    assert len(seen_batches) == 1 and seen_batches[0] == ["alpha", "beta"]

    # "alpha" is cached; only "gamma" should trigger a new HTTP call.
    second = ollama.embed(["alpha", "gamma"])
    assert len(seen_batches) == 2 and seen_batches[1] == ["gamma"]
    assert first[0] == second[0]


def test_fake_embedder_deterministic_and_unit_norm():
    embedder = FakeEmbedder(dim=32)
    v1 = embedder.embed(["retrieval augmented generation"])[0]
    v2 = embedder.embed(["retrieval augmented generation"])[0]
    assert v1 == v2

    import math

    norm = math.sqrt(sum(x * x for x in v1))
    assert abs(norm - 1.0) < 1e-9


def test_fake_llm_canned_and_echo():
    llm = FakeLLM(canned={"capital of France": "Paris"})
    assert llm.chat([{"role": "user", "content": "What is the capital of France?"}]) == "Paris"
    assert llm.chat([{"role": "user", "content": "anything else"}]) == "echo: anything else"


def test_count_tokens_positive():
    assert count_tokens("retrieval augmented generation") > 0


def test_corpus_parse_on_tiny_pdf(tmp_path, monkeypatch):
    """pypdf can write a minimal PDF; check parse()'s page-marker + dehyphenation logic."""
    pypdf = pytest.importorskip("pypdf")
    from pypdf import PdfWriter

    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    pdf_path = tmp_path / "tiny.pdf"
    with open(pdf_path, "wb") as f:
        writer.write(f)

    reader = pypdf.PdfReader(pdf_path)
    assert len(reader.pages) == 1

    from rag_tutorial.corpus import _dehyphenate

    assert _dehyphenate("infor-\nmation") == "information"
