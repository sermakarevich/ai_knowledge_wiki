"""Chapter 00 offline tests. No network — the httpx transport is mocked, or we
use the FakeLLM/FakeEmbedder stand-ins.

Run with: cd project && uv run pytest tests/ -q -m "not slow"
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import httpx
import pytest
from pydantic import BaseModel

from evals_tutorial import llm
from evals_tutorial.llm import Ollama, cache_stats, count_tokens
from evals_tutorial.testing import FakeEmbedder, FakeLLM

DATA_PUBLIC = Path(__file__).resolve().parent.parent / "data" / "public"


class Reply(BaseModel):
    word: str
    ok: bool


def test_chat_cache_round_trip(tmp_path: Path):
    """First chat call hits the (mocked) server and writes the cache; the second
    identical call must be served from disk, so the mocked server is only ever
    called once."""

    posted: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        posted.append(body)
        if request.url.path == "/api/chat":
            return httpx.Response(200, json={"message": {"content": "OK"}})
        raise AssertionError(f"unexpected path {request.url.path}")

    client = Ollama(base_url="http://test.local", cache_dir=tmp_path, transport=httpx.MockTransport(handler))
    messages = [{"role": "user", "content": "hi"}]

    hits_before, misses_before = llm.usage_log["hits"], llm.usage_log["misses"]
    first = client.chat(messages, max_tokens=4)
    second = client.chat(messages, max_tokens=4)

    assert first == second == "OK"
    assert len(posted) == 1  # second call was a cache hit, no network
    assert llm.usage_log["hits"] - hits_before == 1
    assert llm.usage_log["misses"] - misses_before == 1

    chat_files = list((tmp_path / "chat").rglob("*.json"))
    assert len(chat_files) == 1
    entry = json.loads(chat_files[0].read_text())
    assert entry["response"] == "OK"
    assert entry["request"]["input"]["messages"] == messages


def test_embed_cache_is_per_text(tmp_path: Path):
    """Embedding cache is per (model, text): re-embedding ["alpha", "gamma"] only
    re-fetches "gamma" — "alpha" came from the cache."""

    posted: list[list[str]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        assert request.url.path == "/api/embed"
        posted.append(list(body["input"]))
        vectors = [[1.0, 0.5, 0.5] for _ in body["input"]]
        return httpx.Response(200, json={"embeddings": vectors})

    client = Ollama(base_url="http://test.local", cache_dir=tmp_path, transport=httpx.MockTransport(handler))

    first = client.embed(["alpha", "beta"])
    assert len(first) == 2

    second = client.embed(["alpha", "gamma"])
    assert second[0] == first[0]  # "alpha" came back from the cache unchanged
    posted_texts = [t for batch in posted for t in batch]
    assert "alpha" in posted_texts  # fetched once, during the first call
    assert "gamma" in posted_texts  # fetched once, during the second call
    n_alpha = posted_texts.count("alpha")
    assert n_alpha == 1, "alpha was re-fetched — cache is per (model, text) and must have served it"
    # one cache file per text, under embed/<model>/<key[:2]>/
    files = list((tmp_path / "embed" / "nomic-embed-text").rglob("*.json"))
    assert len(files) == 3  # alpha, beta, gamma


def test_chat_json_validation_retry_with_fakellm(tmp_path: Path, monkeypatch):
    """chat_json retries once with the validation error appended when the first
    reply fails pydantic validation (FakeLLM drives the underlying chat)."""
    fake = FakeLLM(
        canned={
            "hello": 'not json at all',
            "retry": '{"word": "OK", "ok": true}',
        }
    )
    client = Ollama(base_url="http://test.local", cache_dir=tmp_path)
    monkeypatch.setattr(Ollama, "chat", lambda self, messages, **kw: fake.chat(messages))

    result = client.chat_json([{"role": "user", "content": "hello"}], Reply)
    assert result == Reply(word="OK", ok=True)
    assert len(fake.calls) == 2  # initial bad reply + one retry
    retry_messages = fake.calls[1]
    last_user = next(m["content"] for m in reversed(retry_messages) if m["role"] == "user")
    assert "retry" in last_user  # the validation error told the model to retry
    assert any(m.get("role") == "assistant" and "not json at all" in m.get("content", "") for m in retry_messages)


def test_fake_embedder_deterministic_and_unit_norm():
    fe = FakeEmbedder(dim=32)
    a1 = fe.embed_query("hello world")
    a2 = fe.embed_query("hello world")
    b = fe.embed_query("different text")
    assert a1 == a2  # deterministic
    assert b != a1
    norm = math.sqrt(sum(x * x for x in a1))
    assert norm == pytest.approx(1.0, abs=1e-9)  # unit-normalised
    assert len(a1) == 32


def test_count_tokens_positive():
    assert count_tokens("Hello, world! This is a tokenization test.") > 0
    assert count_tokens("") == 0
    assert count_tokens("a longer sentence with more words than two") > count_tokens("two")


def test_public_data_files_present_and_row_counts():
    """data/public/*.jsonl parse, and their row counts match
    `data/public/README.md`."""
    expected = {
        "mt_bench_answers.jsonl": 480,
        "mt_bench_human_votes.jsonl": 3355,
        "mt_bench_gpt4_votes.jsonl": 2400,
        "ragtruth_test_subset.jsonl": 480,
    }
    for name, rows_n in expected.items():
        path = DATA_PUBLIC / name
        assert path.exists(), f"missing {path}"
        lines = [line for line in path.read_text().splitlines() if line.strip()]
        assert len(lines) == rows_n, f"{name}: expected {rows_n} rows, got {len(lines)}"
        assert isinstance(json.loads(lines[0]), dict)  # first line parses as JSONL


def test_cache_stats_shape(tmp_path: Path, monkeypatch):
    """cache_stats returns a stable shape (kind → entries/bytes) even when empty."""
    monkeypatch.setattr("evals_tutorial.config.settings.cache_dir", str(tmp_path))
    stats = cache_stats()
    assert set(stats) == {"chat", "embed"}
    for v in stats.values():
        assert v["entries"] == 0 and v["bytes"] == 0
