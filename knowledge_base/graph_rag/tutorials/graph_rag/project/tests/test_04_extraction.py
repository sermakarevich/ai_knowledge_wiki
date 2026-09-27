"""Tests for chapter 04: cached extraction results. No LLM call -- this only
loads and validates data/extracted/chunks/*.json, which was produced once by
`just extract` and is committed so re-runs are instant.
"""

from pathlib import Path

from graph_rag.extraction import ChunkExtraction

_CHUNKS_DIR = Path(__file__).resolve().parents[1] / "data" / "extracted" / "chunks"


def _load_all() -> list[ChunkExtraction]:
    paths = sorted(_CHUNKS_DIR.glob("*.json"))
    assert paths, f"no cached extractions found in {_CHUNKS_DIR}"
    return [ChunkExtraction.model_validate_json(p.read_text()) for p in paths]


def test_at_least_20_chunks_are_cached():
    paths = list(_CHUNKS_DIR.glob("*.json"))
    assert len(paths) >= 20


def test_every_cache_file_parses_into_model():
    extractions = _load_all()
    assert all(isinstance(e, ChunkExtraction) for e in extractions)


def test_average_at_least_one_entity_per_chunk():
    extractions = _load_all()
    total_entities = sum(len(e.entities) for e in extractions)
    assert total_entities / len(extractions) >= 1


def test_every_relationship_endpoint_exists_in_same_chunk_entities():
    for extraction in _load_all():
        normalized_names = {entity.normalized_name for entity in extraction.entities}
        for rel in extraction.relationships:
            assert rel.source in normalized_names, (
                f"chunk {extraction.chunk_id}: relationship source {rel.source!r} "
                f"not in {sorted(normalized_names)}"
            )
            assert rel.target in normalized_names, (
                f"chunk {extraction.chunk_id}: relationship target {rel.target!r} "
                f"not in {sorted(normalized_names)}"
            )


def test_prompt_version_is_recorded():
    for extraction in _load_all():
        assert extraction.prompt_version


def test_relationship_weight_is_in_unit_range():
    for extraction in _load_all():
        for rel in extraction.relationships:
            assert 0 <= rel.weight <= 1
