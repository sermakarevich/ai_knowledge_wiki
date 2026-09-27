"""Tests for chapter 05: LayerNorm/RMSNorm vs torch/transformers, blocks, depth stats."""

import matplotlib
import torch

matplotlib.use("Agg")
from typer.testing import CliRunner

from llm_blocks.ch05_norm_residual import (
    Block,
    DeepStack,
    LayerNorm,
    NoNormTrainConfig,
    RMSNorm,
    app,
    stack_stats,
    train_deep_stack,
)

runner = CliRunner()


# ---------------------------------------------------------------------------
# LayerNorm vs torch.nn.LayerNorm
# ---------------------------------------------------------------------------


def test_layernorm_matches_torch():
    torch.manual_seed(0)
    dim = 32
    x = torch.randn(4, 7, dim) * 3.0 + 1.0

    ours = LayerNorm(dim, eps=1e-5)
    ref = torch.nn.LayerNorm(dim, eps=1e-5)
    with torch.no_grad():
        ref.weight.copy_(torch.randn(dim))
        ref.bias.copy_(torch.randn(dim))
        ours.weight.copy_(ref.weight)
        ours.bias.copy_(ref.bias)

    torch.testing.assert_close(ours(x), ref(x), rtol=1e-4, atol=1e-5)


def test_layernorm_recenters_and_rescales():
    x = torch.randn(64) * 5.0 + 3.0
    y = LayerNorm(64)(x)
    assert y.mean().abs() < 1e-5
    # LayerNorm divides by the *biased* std (ddof=0); compare against that, not tensor.std()'s default ddof=1.
    assert abs(y.std(unbiased=False).item() - 1.0) < 1e-3


# ---------------------------------------------------------------------------
# RMSNorm vs torch.nn.RMSNorm and transformers Qwen3RMSNorm / Qwen3_5RMSNorm
# ---------------------------------------------------------------------------


def test_rmsnorm_matches_torch():
    torch.manual_seed(0)
    dim = 32
    x = torch.randn(4, 7, dim) * 3.0 + 1.0

    ours = RMSNorm(dim, eps=1e-6, qwen_variant=False)
    ref = torch.nn.RMSNorm(dim, eps=1e-6)
    with torch.no_grad():
        ref.weight.copy_(torch.randn(dim))
        ours.weight.copy_(ref.weight)

    torch.testing.assert_close(ours(x), ref(x), rtol=1e-4, atol=1e-5)


def test_rmsnorm_does_not_recenter():
    x = torch.randn(64) * 5.0 + 3.0
    y = RMSNorm(64)(x)
    # RMSNorm only rescales: sign of every element must be preserved.
    assert torch.all(torch.sign(y) == torch.sign(x))


def test_rmsnorm_matches_qwen3rmsnorm():
    __import__("pytest").importorskip("transformers")
    from transformers.models.qwen3.modeling_qwen3 import Qwen3RMSNorm

    torch.manual_seed(0)
    dim = 16
    x = torch.randn(3, 5, dim)

    ours = RMSNorm(dim, eps=1e-6, qwen_variant=False)
    ref = Qwen3RMSNorm(dim, eps=1e-6)
    with torch.no_grad():
        ref.weight.copy_(torch.randn(dim))
        ours.weight.copy_(ref.weight)

    torch.testing.assert_close(ours(x), ref(x), rtol=1e-4, atol=1e-5)


def test_rmsnorm_matches_qwen3_5rmsnorm():
    __import__("pytest").importorskip("transformers")
    from transformers.models.qwen3_5.modeling_qwen3_5 import Qwen3_5RMSNorm

    torch.manual_seed(0)
    dim = 16
    x = torch.randn(3, 5, dim)

    ours = RMSNorm(dim, eps=1e-6, qwen_variant=True)
    ref = Qwen3_5RMSNorm(dim, eps=1e-6)
    with torch.no_grad():
        ref.weight.copy_(torch.randn(dim))
        ours.weight.copy_(ref.weight)

    torch.testing.assert_close(ours(x), ref(x), rtol=1e-4, atol=1e-5)


def test_qwen3_5_variant_identity_at_zero_weight():
    """Qwen3.5's weight starts at zero, so an untrained norm is exactly x / rms(x)."""
    x = torch.randn(4, 16)
    norm = RMSNorm(16, qwen_variant=True)
    assert torch.allclose(norm.weight, torch.zeros(16))
    expected = x / torch.sqrt(x.pow(2).mean(dim=-1, keepdim=True) + norm.eps)
    torch.testing.assert_close(norm(x), expected, rtol=1e-4, atol=1e-5)


# ---------------------------------------------------------------------------
# Block: pre-norm vs post-norm
# ---------------------------------------------------------------------------


def test_block_pre_norm_formula():
    torch.manual_seed(0)
    dim = 8
    block = Block(dim, pre_norm=True, norm=RMSNorm(dim))
    x = torch.randn(2, dim)
    expected = x + block.f(block.norm(x))
    torch.testing.assert_close(block(x), expected)


def test_block_post_norm_formula():
    torch.manual_seed(0)
    dim = 8
    block = Block(dim, pre_norm=False, norm=RMSNorm(dim))
    x = torch.randn(2, dim)
    expected = block.norm(x + block.f(x))
    torch.testing.assert_close(block(x), expected)


def test_block_no_norm_is_identity_pass_through():
    dim = 8
    block = Block(dim, pre_norm=True, norm=None)
    assert isinstance(block.norm, torch.nn.Identity)


# ---------------------------------------------------------------------------
# stack_stats
# ---------------------------------------------------------------------------


def test_stack_stats_shapes():
    stats = stack_stats(depth=6, pre_norm=True, use_norm=True, dim=16)
    assert len(stats["activation_std"]) == 6
    assert len(stats["residual_norm"]) == 6
    assert len(stats["gradient_norm"]) == 6
    assert all(v > 0 for v in stats["residual_norm"])


def test_stack_stats_post_norm_keeps_residual_norm_flat():
    """post-norm applies a norm at the very end of every block, so ||x|| stays ~constant
    across depth by construction -- unlike pre-norm/no-norm, where the residual stream
    keeps accumulating each layer's addition."""
    post = stack_stats(depth=32, pre_norm=False, use_norm=True, dim=32)
    post_growth = post["residual_norm"][-1] / post["residual_norm"][0]
    assert abs(post_growth - 1.0) < 0.05


def test_stack_stats_no_norm_grows_faster_than_pre_norm():
    """Without any normalization the residual stream grows faster across depth than with
    a pre-norm RMSNorm in every block."""
    pre = stack_stats(depth=32, pre_norm=True, use_norm=True, dim=32)
    no_norm = stack_stats(depth=32, pre_norm=True, use_norm=False, dim=32)
    pre_growth = pre["residual_norm"][-1] / pre["residual_norm"][0]
    no_norm_growth = no_norm["residual_norm"][-1] / no_norm["residual_norm"][0]
    assert pre_growth < no_norm_growth


# ---------------------------------------------------------------------------
# No-norm training demo
# ---------------------------------------------------------------------------


def test_train_deep_stack_runs_and_returns_losses():
    cfg = NoNormTrainConfig(steps=5)
    losses = train_deep_stack(cfg, use_norm=True)
    assert len(losses) == 5
    assert all(torch.isfinite(torch.tensor(losses)))


def test_deep_stack_forward_shape():
    model = DeepStack(in_features=2, dim=16, depth=4, use_norm=True)
    x = torch.randn(5, 2)
    assert model(x).shape == (5, 1)


# ---------------------------------------------------------------------------
# CLI smoke tests
# ---------------------------------------------------------------------------


def test_cli_demo_runs():
    result = runner.invoke(app, ["demo"])
    assert result.exit_code == 0
    assert "residual norm" in result.stdout
