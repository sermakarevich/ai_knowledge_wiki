"""Tests for chapter 03: the frozen graph schema. No LLM call — this only
loads and validates data/extracted/schema.json, which was produced once by
`just schema-propose` and is committed so re-runs are instant.
"""

from pathlib import Path

from graph_rag.schema_discovery import GraphSchema, validate_schema

_SCHEMA_PATH = Path(__file__).resolve().parents[1] / "data" / "extracted" / "schema.json"

_REQUIRED_ENTITY_TYPES = {"Method", "Dataset", "Organization", "Metric", "Paper"}
_REQUIRED_RELATIONSHIP_PREFIXES = ("PROPOSED_BY", "EVALUATED_ON", "IMPROVES", "USES")


def _load_schema() -> GraphSchema:
    return GraphSchema.model_validate_json(_SCHEMA_PATH.read_text())


def test_schema_file_parses_into_model():
    schema = _load_schema()
    assert schema.entity_types
    assert schema.relationship_types


def test_schema_has_no_validation_issues():
    schema = _load_schema()
    assert validate_schema(schema) == []


def test_schema_contains_required_entity_types():
    schema = _load_schema()
    names = {e.name for e in schema.entity_types}
    assert _REQUIRED_ENTITY_TYPES <= names


def test_schema_contains_required_relationship_families():
    schema = _load_schema()
    names = {r.name for r in schema.relationship_types}
    for prefix in _REQUIRED_RELATIONSHIP_PREFIXES:
        assert any(name.startswith(prefix) or prefix in name for name in names), (
            f"no relationship type covering '{prefix}' in {sorted(names)}"
        )


def test_entity_type_names_are_pascal_case():
    schema = _load_schema()
    for entity in schema.entity_types:
        assert entity.name[0].isupper()
        assert "_" not in entity.name


def test_relationship_type_names_are_upper_snake_case():
    schema = _load_schema()
    for rel in schema.relationship_types:
        assert rel.name == rel.name.upper()
