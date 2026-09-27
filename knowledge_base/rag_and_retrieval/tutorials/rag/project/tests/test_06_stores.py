"""Offline + integration tests for chapter 06 (embedding models, Matryoshka,
Qdrant quantization, HNSW sweep).

Offline tests run without Ollama, Qdrant or the GPU: they exercise the pure
numpy retrieval path and the model-name resolution. The Qdrant-backed evals
(quant / hnsw) are `@pytest.mark.slow`, since they need a running
`just up qdrant` and the nomic embeddings cache.
"""

from __future__ import annotations

import json

import numpy as np
import pytest

import rag_tutorial.embed_eval as embed_eval
from rag_tutorial.schema import Chunk, chunk_id


def _chunk(paper: str, section: str, text: str, start: int = 0, end: int = 1) -> Chunk:
    return Chunk(id=chunk_id(paper, start, end), paper=paper, section=section, text=text, start=start, end=end)


# -- name resolution (Ollama 0.32 tags) --------------------------------------------------


class _FakeTags:
    def __init__(self, models):
        self._models = models

    def json(self):
        return {"models": self._models}


def _tag(name: str, size: int = 10_000_000) -> dict:
    return {"name": name, "size": size, "details": {"parameter_size": "22M"}}


def test_resolve_model_maps_bare_name_to_tagged(monkeypatch, tmp_path):
    """Ollama rejects bare names for tagged models (`mxbai-embed-large` → 404,
    `mxbai-embed-large:335m` → 200): the resolver must return the tagged name
    when no local cache dir exists to pin the bare one."""
    monkeypatch.setattr(embed_eval.settings, "cache_dir", str(tmp_path / "no-such-cache"))
    embed_eval._ollama_models.cache_clear()
    monkeypatch.setattr(
        embed_eval.httpx,
        "get",
        lambda *a, **k: _FakeTags([_tag("mxbai-embed-large:335m"), _tag("nomic-embed-text:latest")]),
    )
    assert embed_eval._resolve_model("mxbai-embed-large") == "mxbai-embed-large:335m"


def test_resolve_model_keeps_bare_name_when_cache_exists(monkeypatch, tmp_path):
    """A bare name with an existing, non-empty cache dir (nomic's ch.05
    entries, ~262 MB) must not be renamed — or the disk cache silently
    misses and every re-embedding is paid again."""
    (tmp_path / "embed" / "nomic-embed-text").mkdir(parents=True)
    (tmp_path / "embed" / "nomic-embed-text" / "a.json").write_text("{}")
    monkeypatch.setattr(embed_eval.settings, "cache_dir", str(tmp_path))
    embed_eval._ollama_models.cache_clear()
    monkeypatch.setattr(embed_eval.httpx, "get", lambda *a, **k: _FakeTags([_tag("nomic-embed-text:latest")]))
    assert embed_eval._resolve_model("nomic-embed-text") == "nomic-embed-text"


def test_resolve_model_unknown_name_passes_through(monkeypatch, tmp_path):
    monkeypatch.setattr(embed_eval.settings, "cache_dir", str(tmp_path))
    embed_eval._ollama_models.cache_clear()
    monkeypatch.setattr(embed_eval.httpx, "get", lambda *a, **k: _FakeTags([_tag("unrelated:999m")]))
    assert embed_eval._resolve_model("whatever") == "whatever"


def test_ollama_tags_failure_is_nonfatal(monkeypatch, tmp_path):
    monkeypatch.setattr(embed_eval.settings, "cache_dir", str(tmp_path))
    embed_eval._ollama_models.cache_clear()

    def _boom(*a, **k):
        raise RuntimeError("no ollama")

    monkeypatch.setattr(embed_eval.httpx, "get", _boom)
    assert embed_eval._resolve_model("any-name") == "any-name"
    assert embed_eval._model_info("any-name") == {"size_bytes": None, "size_mb": None, "params": None}


def test_model_list_starts_with_baseline_and_has_seven_entries():
    assert len(embed_eval.EMBED_MODELS) == 7
    assert embed_eval.EMBED_MODELS[0] == "nomic-embed-text"  # reuses ch.05 cache
    assert all(":" not in m for m in embed_eval.EMBED_MODELS)  # bare keys match _EMBED_PREFIXES


# -- numpy top-k retrieval helper ---------------------------------------------------------


def test_retrieval_only_finds_planted_relevant_chunk():
    """Plant one chunk vector aligned with the question vector: it must land
    in the top 5, and `hit@5` must be 1.0 (evidence quote = chunk text, same
    paper — the shape `chunk_covers_quote` checks)."""
    rng = np.random.default_rng(7)
    dim = 32
    children = [_chunk("paper", "section", f"chunk number {i} unique words") for i in range(20)]
    child_vecs = rng.normal(0, 1, (20, dim))
    query_vecs = np.zeros((1, dim))
    query_vecs[0][:] = child_vecs[3] / np.linalg.norm(child_vecs[3])

    item = {"evidence": [{"paper": "paper", "quote": "chunk number 3 unique words"}]}
    metrics = embed_eval._retrieval_only(children, child_vecs, query_vecs, [item])
    assert metrics["n_questions"] == 1
    assert metrics["hit@5"] == 1.0
    assert metrics["recall@5"] == 1.0
    assert 0.0 < metrics["mrr"] <= 1.0
    assert 0.0 < metrics["ndcg@10"] <= 1.0


def test_retrieval_only_is_deterministic():
    rng = np.random.default_rng(0)
    dim = 16
    n = 12
    children = [_chunk("p", "s", f"content {i}") for i in range(n)]
    child_vecs = rng.normal(0, 1, (n, dim))
    query_vecs = rng.normal(0, 1, (2, dim))
    items = [
        {"evidence": [{"paper": "p", "quote": "content 0"}]},
        {"evidence": [{"paper": "p", "quote": "content 1"}]},
    ]
    a = embed_eval._retrieval_only(children, child_vecs, query_vecs, items)
    b = embed_eval._retrieval_only(children, child_vecs, query_vecs, items)
    assert a == b


# -- Matryoshka / normalisation -----------------------------------------------------------


def test_unit_normalize_unit_norm_and_direction_preserved():
    v = np.array([[1.0, 0.0, 0.0], [2.0, 0.0, 0.0], [0.0, 3.0, 0.0]])
    out = embed_eval._unit_normalize(v)
    np.testing.assert_allclose(np.linalg.norm(out, axis=1), np.ones(3), rtol=1e-12)
    np.testing.assert_allclose(out[1], out[0])  # 2x the same direction → same unit vector
    np.testing.assert_allclose(out[2], np.array([0.0, 1.0, 0.0]))


def test_unit_normalize_zero_row_stays_finite():
    out = embed_eval._unit_normalize(np.array([[0.0, 0.0], [3.0, 4.0]]))
    assert not np.isnan(out).any()
    np.testing.assert_allclose(out[1], np.array([0.6, 0.8]))


def test_matryoshka_dim_grid_is_sub_dimensions_of_full():
    """Every truncation dim must be a valid prefix of the 768-dim nomic output
    and strictly decrease; the grid is what `cmd_matryoshka` sweeps."""
    assert all(0 < d < 768 for d in embed_eval.MATRYOSHKA_DIMS)
    assert embed_eval.MATRYOSHKA_DIMS == tuple(sorted(embed_eval.MATRYOSHKA_DIMS, reverse=True))


# -- Qdrant-backed evals (need `just up qdrant` + nomic cache) ----------------------------


@pytest.mark.slow
def test_quant_eval_writes_all_modes_and_cleans_up():
    embed_eval.cmd_quant()
    out = embed_eval.RUNS_DIR / "06_quant.json"
    assert out.exists()
    data = json.loads(out.read_text())
    for key in ("float", "scalar_int8", "product_x64", "binary"):
        assert key in data, f"missing mode {key}"
        assert data[key]["recall@5"] >= 0.0
        assert data[key]["ram_mb"] >= 0.0
    client = embed_eval._qdrant_client()
    assert not client.collection_exists("ch06_quant_bench")


@pytest.mark.slow
def test_hnsw_eval_covers_full_grid_and_cleans_up():
    embed_eval.cmd_hnsw()
    out = embed_eval.RUNS_DIR / "06_hnsw.json"
    assert out.exists()
    rows = json.loads(out.read_text())
    expected = {(m_, ef_c, ef_s) for m_ in embed_eval.HNSW_M for ef_c in embed_eval.HNSW_EF_CONSTRUCT for ef_s in embed_eval.HNSW_EF_SEARCH}
    got = {(r["m"], r["ef_construct"], r["ef_search"]) for r in rows}
    assert got == expected
    for r in rows:
        assert 0.0 <= r["recall_vs_exact"] <= 1.0
        assert r["qdrant_ms"] > 0
        assert r["exact_ms"] > 0
    client = embed_eval._qdrant_client()
    assert not client.collection_exists("ch06_hnsw_bench")
