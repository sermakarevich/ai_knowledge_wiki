"""Offline tests for chapter 01: the cosine-similarity matrix helper. No network calls."""

from __future__ import annotations

from rag_tutorial.demo_concepts import cosine_matrix
from rag_tutorial.testing import FakeEmbedder


def test_cosine_matrix_symmetric_with_unit_diagonal():
    embedder = FakeEmbedder(dim=32)
    sentences = [
        "retrieval augmented generation combines search and language models",
        "RAG systems retrieve documents before generating an answer",
        "sourdough bread needs a long slow fermentation",
    ]
    vectors = embedder.embed(sentences)
    matrix = cosine_matrix(vectors)

    n = len(sentences)
    for i in range(n):
        assert abs(matrix[i][i] - 1.0) < 1e-9
        for j in range(n):
            assert abs(matrix[i][j] - matrix[j][i]) < 1e-9
