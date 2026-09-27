"""Offline stand-ins for `evals_tutorial.llm.Ollama`, used by every test in this tutorial.

Both classes expose the same method names as `Ollama` (`chat`, `chat_json`,
`embed`, `embed_documents`, `embed_query`) so any code written against the real
client can be tested on the Mac, on CPU, with no network and no Docker.
"""

from __future__ import annotations

import hashlib

import numpy as np
from pydantic import BaseModel


class FakeLLM:
    """Returns a canned answer if the last user message contains a known substring,
    otherwise echoes the last user message back (prefixed), so tests can assert on
    predictable output without a real model.

    `chat_json` returns a canned *dict* (registered the same way, keyed by a
    substring of the request) converted into the requested Pydantic model; if no
    canned answer matches it raises `ValueError` to simulate a bad reply.
    """

    def __init__(
        self,
        canned: dict[str, str] | None = None,
        json_answers: dict[str, dict] | None = None,
        embed_dim: int = 32,
    ):
        self.canned = canned or {}
        self.json_answers = json_answers or {}
        self.calls: list[list[dict]] = []
        self._embed = FakeEmbedder(dim=embed_dim)  # full client protocol: chat + embed

    def _last_user(self, messages: list[dict]) -> str:
        return next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")

    # -- embedding (delegated to FakeEmbedder) ---------------------------------

    def embed(self, texts: list[str], **_kwargs) -> list[list[float]]:
        return self._embed.embed(texts)

    def embed_documents(self, texts: list[str], **_kwargs) -> list[list[float]]:
        return self._embed.embed_documents(texts)

    def embed_query(self, text: str, **_kwargs) -> list[float]:
        return self._embed.embed_query(text)

    def chat(self, messages: list[dict], **_kwargs) -> str:
        self.calls.append(messages)
        last_user = self._last_user(messages)
        for substring, answer in self.canned.items():
            if substring in last_user:
                return answer
        return f"echo: {last_user}"

    def chat_json(self, messages: list[dict], schema: type[BaseModel], **_kwargs) -> BaseModel:
        self.calls.append(messages)
        last_user = self._last_user(messages)
        for substring, value in self.json_answers.items():
            if substring in last_user:
                return schema.model_validate(value)
        raise ValueError(f"no canned json answer for: {last_user!r}")


class FakeEmbedder:
    """Deterministic, hashed bag-of-words embeddings, unit-normalised.

    Same text always maps to the same vector (no network, no model); different
    texts are very likely to map to different vectors, which is enough for
    testing retrieval logic without a real embedding model.
    """

    def __init__(self, dim: int = 32):
        self.dim = dim
        self.calls: list[str] = []

    def _vector(self, text: str) -> list[float]:
        vec = np.zeros(self.dim, dtype=np.float64)
        for word in text.lower().split():
            h = int(hashlib.sha256(word.encode("utf-8")).hexdigest(), 16)
            vec[h % self.dim] += 1.0
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec.tolist()

    def embed(self, texts: list[str], **_kwargs) -> list[list[float]]:
        self.calls.extend(texts)
        return [self._vector(t) for t in texts]

    def embed_documents(self, texts: list[str], **_kwargs) -> list[list[float]]:
        return self.embed(texts)

    def embed_query(self, text: str, **_kwargs) -> list[float]:
        return self.embed([text])[0]
