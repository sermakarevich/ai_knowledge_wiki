"""Tests for chapter 04: sinusoidal PE, RoPE, and partial RoPE vs `transformers`."""

import math

import matplotlib
import pytest

matplotlib.use("Agg")
import torch
from typer.testing import CliRunner

from llm_blocks import plotting
from llm_blocks.ch04_positional_encoding import (
    _attention_no_position,
    _attention_with_rope,
    app,
    apply_rope,
    partial_rope,
    permutation_test,
    rope_cos_sin,
    sinusoidal_pe,
)

runner = CliRunner()


# ---------------------------------------------------------------------------
# sinusoidal PE
# ---------------------------------------------------------------------------


def test_sinusoidal_shape_and_bounds():
    pe = sinusoidal_pe(seq=32, d=16)
    assert pe.shape == (32, 16)
    assert pe.abs().max() <= 1.0 + 1e-6


def test_sinusoidal_position_zero_is_sin0_cos0():
    pe = sinusoidal_pe(seq=4, d=8)
    # sin(0) = 0 for every even dim, cos(0) = 1 for every odd dim.
    torch.testing.assert_close(pe[0, 0::2], torch.zeros(4), atol=1e-6, rtol=0)
    torch.testing.assert_close(pe[0, 1::2], torch.ones(4), atol=1e-6, rtol=0)


def test_sinusoidal_rows_are_unique():
    pe = sinusoidal_pe(seq=50, d=32)
    for i in range(49):
        assert not torch.allclose(pe[i], pe[i + 1])


# ---------------------------------------------------------------------------
# RoPE vs transformers.models.qwen3.modeling_qwen3
# ---------------------------------------------------------------------------


def test_rope_cos_sin_matches_qwen3_rotary_embedding():
    from transformers.models.qwen3.configuration_qwen3 import Qwen3Config
    from transformers.models.qwen3.modeling_qwen3 import Qwen3RotaryEmbedding

    head_dim, seq, theta = 32, 16, 10000.0
    cfg = Qwen3Config(head_dim=head_dim, rope_parameters={"rope_theta": theta, "rope_type": "default"})
    rot = Qwen3RotaryEmbedding(cfg)
    position_ids = torch.arange(seq).unsqueeze(0)
    ref_cos, ref_sin = rot(torch.zeros(1, seq, head_dim), position_ids)

    cos, sin = rope_cos_sin(seq, head_dim, theta=theta)

    torch.testing.assert_close(cos, ref_cos[0], rtol=1e-4, atol=1e-5)
    torch.testing.assert_close(sin, ref_sin[0], rtol=1e-4, atol=1e-5)


def test_apply_rope_matches_qwen3_apply_rotary_pos_emb():
    from transformers.models.qwen3.modeling_qwen3 import apply_rotary_pos_emb

    torch.manual_seed(0)
    b, h, seq, head_dim = 2, 3, 12, 32
    q = torch.randn(b, h, seq, head_dim)
    k = torch.randn(b, h, seq, head_dim)
    cos, sin = rope_cos_sin(seq, head_dim)

    ours_q, ours_k = apply_rope(q, cos, sin), apply_rope(k, cos, sin)
    ref_q, ref_k = apply_rotary_pos_emb(q, k, cos.unsqueeze(0), sin.unsqueeze(0))

    torch.testing.assert_close(ours_q, ref_q, rtol=1e-4, atol=1e-5)
    torch.testing.assert_close(ours_k, ref_k, rtol=1e-4, atol=1e-5)


def test_rope_preserves_vector_norm():
    """A rotation changes direction, not length: ||apply_rope(x)|| == ||x||."""
    torch.manual_seed(0)
    seq, head_dim = 10, 16
    x = torch.randn(1, 1, seq, head_dim)
    cos, sin = rope_cos_sin(seq, head_dim)
    rotated = apply_rope(x, cos, sin)

    torch.testing.assert_close(rotated.norm(dim=-1), x.norm(dim=-1), rtol=1e-4, atol=1e-5)


def test_rope_dot_product_depends_only_on_relative_distance():
    """q at position p, k at position p+dist: the dot product must not depend on p."""
    torch.manual_seed(0)
    head_dim = 32
    cos, sin = rope_cos_sin(seq=300, head_dim=head_dim)
    q0, k0 = torch.randn(head_dim), torch.randn(head_dim)

    dist = 50
    dots = []
    for p in (0, 100, 200):
        q = apply_rope(q0.unsqueeze(0), cos[p].unsqueeze(0), sin[p].unsqueeze(0))
        k = apply_rope(k0.unsqueeze(0), cos[p + dist].unsqueeze(0), sin[p + dist].unsqueeze(0))
        dots.append((q * k).sum().item())

    assert math.isclose(dots[0], dots[1], rel_tol=1e-4)
    assert math.isclose(dots[0], dots[2], rel_tol=1e-4)


# ---------------------------------------------------------------------------
# partial RoPE vs transformers.models.qwen3_5.modeling_qwen3_5
# ---------------------------------------------------------------------------


def test_partial_rope_matches_qwen3_5_apply_rotary_pos_emb():
    from transformers.models.qwen3_5.modeling_qwen3_5 import (
        apply_rotary_pos_emb as ref_apply,
    )

    torch.manual_seed(0)
    b, h, seq, head_dim = 2, 2, 10, 16
    rotary_frac = 0.25
    rotary_dim = int(head_dim * rotary_frac)

    q = torch.randn(b, h, seq, head_dim)
    k = torch.randn(b, h, seq, head_dim)
    cos, sin = rope_cos_sin(seq, rotary_dim)

    ours_q = partial_rope(q, cos, sin, rotary_frac=rotary_frac)
    ours_k = partial_rope(k, cos, sin, rotary_frac=rotary_frac)
    ref_q, ref_k = ref_apply(q, k, cos.unsqueeze(0), sin.unsqueeze(0))

    torch.testing.assert_close(ours_q, ref_q, rtol=1e-4, atol=1e-5)
    torch.testing.assert_close(ours_k, ref_k, rtol=1e-4, atol=1e-5)


def test_partial_rope_leaves_the_tail_untouched():
    torch.manual_seed(0)
    head_dim, rotary_frac = 16, 0.25
    rotary_dim = int(head_dim * rotary_frac)
    x = torch.randn(1, 1, 5, head_dim)
    cos, sin = rope_cos_sin(5, rotary_dim)

    out = partial_rope(x, cos, sin, rotary_frac=rotary_frac)

    torch.testing.assert_close(out[..., rotary_dim:], x[..., rotary_dim:], rtol=0, atol=0)


def test_partial_rope_rejects_mismatched_rotary_frac():
    x = torch.randn(1, 1, 4, 16)
    cos, sin = rope_cos_sin(4, 8)  # rotary_dim=8, but rotary_frac=0.25 of 16 expects 4
    with pytest.raises(ValueError):
        partial_rope(x, cos, sin, rotary_frac=0.25)


# ---------------------------------------------------------------------------
# permutation test
# ---------------------------------------------------------------------------


def test_permutation_test_true_without_positions():
    assert permutation_test(_attention_no_position) is True


def test_permutation_test_false_with_rope():
    assert permutation_test(_attention_with_rope) is False


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def test_plots_command_runs(tmp_path, monkeypatch):
    monkeypatch.setattr(plotting, "ASSETS", tmp_path)
    result = runner.invoke(app, ["plots"])
    assert result.exit_code == 0, result.output
    for name in (
        "04_sinusoidal", "04_rope_rotation", "04_rope_relative",
        "04_frequencies", "04_partial_rope", "04_context_extension",
    ):
        assert (tmp_path / f"{name}.png").is_file()


def test_demo_command_runs():
    result = runner.invoke(app, ["demo"])
    assert result.exit_code == 0, result.output
    assert "permutation-equivariant = True" in result.output
    assert "permutation-equivariant = False" in result.output
