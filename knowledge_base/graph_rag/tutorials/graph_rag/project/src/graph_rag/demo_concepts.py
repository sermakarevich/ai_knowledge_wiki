"""Tiny runnable demo for chapter 01: embeddings and cosine similarity.

Run with: python -m graph_rag.demo_concepts
"""

import math

from graph_rag.llm import embed

SENTENCES = [
    "GraphRAG partitions the knowledge graph into a hierarchy of communities "
    "and summarizes them bottom-up.",
    "Community detection groups closely related entities into hierarchical "
    "clusters that are summarized from the bottom level up.",
    "HippoRAG runs Personalized PageRank over a knowledge graph seeded by "
    "query entities to perform multi-hop retrieval in a single step.",
    "What does GraphRAG partitions and how does it summarize them?"
]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Cosine of the angle between two vectors: 1.0 = identical direction, 0.0 = unrelated, -1.0 = opposite."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    return dot / (norm_a * norm_b)


def main() -> None:
    vectors = embed(SENTENCES)
    print(f"embedded {len(vectors)} sentences, {len(vectors[0])} dimensions each\n")
    for i in range(len(SENTENCES)):
        for j in range(i + 1, len(SENTENCES)):
            sim = cosine_similarity(vectors[i], vectors[j])
            print(f"sim(sentence {i}, sentence {j}) = {sim:.4f}")
            print(f"  [{i}] {SENTENCES[i]}")
            print(f"  [{j}] {SENTENCES[j]}")


if __name__ == "__main__":
    main()
