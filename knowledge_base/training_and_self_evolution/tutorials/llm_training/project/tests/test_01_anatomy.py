"""Chapter 01 — the model we describe must really have the shape the chapter claims.

CPU only, no network: both configs are local YAML and the models are built from scratch.
"""

from pathlib import Path

import pytest
from transformers import Qwen3ForCausalLM

from llm_tutorial.anatomy import budget_row, compress_layer_types, parameter_summary, training_flops
from llm_tutorial.config import load_yaml
from llm_tutorial.model import build_model

CONFIGS = Path(__file__).resolve().parents[1] / "configs"


@pytest.fixture(scope="module")
def tiny_hybrid():
    section = load_yaml(CONFIGS / "tiny_qwen35_110m.yaml")["model"]
    return build_model(section, device="cpu")


def test_tiny_model_is_about_110m(tiny_hybrid):
    model, config = tiny_hybrid
    summary = parameter_summary(model, config)
    assert 108.0e6 < summary["total"] < 109.2e6
    # embeddings are tied, so the table is counted once and the LM head adds nothing
    assert summary["embedding"] == 32000 * 768
    assert summary["non_embedding"] == summary["total"] - 32000 * 768


def test_layer_pattern_is_three_linear_then_one_full(tiny_hybrid):
    _, config = tiny_hybrid
    assert len(config.layer_types) == 12
    full = [i for i, t in enumerate(config.layer_types) if t == "full_attention"]
    assert full == [3, 7, 11]
    assert all(t == "linear_attention" for i, t in enumerate(config.layer_types) if i not in full)
    assert compress_layer_types(config.layer_types) == "LLLF LLLF LLLF"


def test_dense_fallback_is_a_plain_qwen3(tmp_path):
    section = load_yaml(CONFIGS / "tiny_qwen3_110m_dense.yaml")["model"]
    model, config = build_model(section, device="meta")
    assert isinstance(model, Qwen3ForCausalLM)
    assert set(config.layer_types) == {"full_attention"}


def test_budget_maths():
    # 1B parameters x 1T tokens = 6e21 FLOPs; at 100 TFLOP/s x 50 % MFU = 5e13 FLOP/s
    # that is 1.2e8 seconds = 33,333.3 hours.
    assert training_flops(1e9, 1e12) == pytest.approx(6e21)
    row = budget_row("demo", 1e9, 1e12, tflops=100.0, mfu=0.5)
    assert row["flops"] == pytest.approx(6e21)
    assert row["gpu_hours"] == pytest.approx(1.2e8 / 3600)
    assert row["gpu_years"] == pytest.approx(1.2e8 / (3600 * 24 * 365.25))
