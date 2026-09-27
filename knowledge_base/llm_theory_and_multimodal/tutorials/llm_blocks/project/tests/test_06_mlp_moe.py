"""Tests for chapter 06: SwiGLU MLP, key-value memory demo, MoE layer and routing."""

import matplotlib
import pytest
import torch
import torch.nn.functional as F

matplotlib.use("Agg")
from typer.testing import CliRunner

from llm_blocks.ch06_mlp_moe import (
    KeyValueMemoryDemo,
    MoELayer,
    MoeToyTrainConfig,
    SwiGLUMLP,
    TopKRouter,
    app,
    load_balancing_loss,
    train_toy_moe,
)

runner = CliRunner()


# ---------------------------------------------------------------------------
# SwiGLUMLP vs transformers Qwen3MLP
# ---------------------------------------------------------------------------


def test_swiglu_matches_qwen3mlp():
    __import__("pytest").importorskip("transformers")
    from transformers.models.qwen3 import Qwen3Config
    from transformers.models.qwen3.modeling_qwen3 import Qwen3MLP

    torch.manual_seed(0)
    hidden, inter = 16, 40
    config = Qwen3Config(hidden_size=hidden, intermediate_size=inter, num_hidden_layers=1,
                          num_attention_heads=2, num_key_value_heads=2)
    ref = Qwen3MLP(config)
    ours = SwiGLUMLP(hidden, inter)
    with torch.no_grad():
        ours.gate_proj.weight.copy_(ref.gate_proj.weight)
        ours.up_proj.weight.copy_(ref.up_proj.weight)
        ours.down_proj.weight.copy_(ref.down_proj.weight)

    x = torch.randn(3, 5, hidden)
    torch.testing.assert_close(ours(x), ref(x), rtol=1e-4, atol=1e-5)


def test_swiglu_gate_mutes_output():
    """A gate input driven very negative makes silu(gate) ~ 0, muting up(x) entirely."""
    torch.manual_seed(0)
    mlp = SwiGLUMLP(4, 8)
    with torch.no_grad():
        mlp.gate_proj.weight.fill_(0.0)
    x = torch.randn(2, 4)
    # gate_proj(x) == 0 everywhere (weight is zero, no bias) -> silu(0) == 0 -> output is down_proj(0) == 0.
    out = mlp(x)
    torch.testing.assert_close(out, torch.zeros_like(out), atol=1e-6, rtol=0)


# ---------------------------------------------------------------------------
# KeyValueMemoryDemo
# ---------------------------------------------------------------------------


def test_kv_memory_trains_and_fires_selectively():
    demo = KeyValueMemoryDemo(n_keys=20, d_model=8, d_hidden=32, seed=0)
    losses = demo.train(steps=300)
    assert losses[-1] < losses[0]
    firing = demo.firing_matrix()
    assert firing.shape == (20, 32)
    # ReLU firing is sparse: not every neuron fires for every key.
    assert (firing == 0).float().mean() > 0.05


# ---------------------------------------------------------------------------
# TopKRouter
# ---------------------------------------------------------------------------


def test_router_topk_weights_sum_to_one():
    torch.manual_seed(0)
    router = TopKRouter(d_model=8, n_experts=6, k=3)
    x = torch.randn(10, 8)
    router_probs, topk_weights, topk_indices = router(x)
    assert router_probs.shape == (10, 6)
    assert topk_weights.shape == (10, 3)
    assert topk_indices.shape == (10, 3)
    torch.testing.assert_close(topk_weights.sum(dim=-1), torch.ones(10), rtol=1e-5, atol=1e-5)
    torch.testing.assert_close(router_probs.sum(dim=-1), torch.ones(10), rtol=1e-5, atol=1e-5)


# ---------------------------------------------------------------------------
# MoELayer
# ---------------------------------------------------------------------------


def test_moe_equals_dense_swiglu_when_one_expert():
    torch.manual_seed(0)
    d_model, d_ff = 8, 16
    mlp = SwiGLUMLP(d_model, d_ff)
    moe = MoELayer(d_model, d_ff, n_experts=1, k=1, shared_expert=False)
    with torch.no_grad():
        moe.experts[0].gate_proj.weight.copy_(mlp.gate_proj.weight)
        moe.experts[0].up_proj.weight.copy_(mlp.up_proj.weight)
        moe.experts[0].down_proj.weight.copy_(mlp.down_proj.weight)

    x = torch.randn(3, 4, d_model)
    out_moe, _, _ = moe(x)
    torch.testing.assert_close(out_moe, mlp(x), rtol=1e-4, atol=1e-5)


def test_moe_matches_qwen3moe_sparse_block():
    __import__("pytest").importorskip("transformers")
    from transformers.models.qwen3_moe import Qwen3MoeConfig
    from transformers.models.qwen3_moe.modeling_qwen3_moe import Qwen3MoeSparseMoeBlock

    torch.manual_seed(0)
    hidden, inter, n_experts, k = 16, 8, 4, 2
    config = Qwen3MoeConfig(hidden_size=hidden, moe_intermediate_size=inter,
                             num_experts=n_experts, num_experts_per_tok=k, norm_topk_prob=True)
    ref = Qwen3MoeSparseMoeBlock(config)
    with torch.no_grad():
        ref.gate.weight.copy_(torch.randn_like(ref.gate.weight))
        ref.experts.gate_up_proj.copy_(torch.randn_like(ref.experts.gate_up_proj) * 0.1)
        ref.experts.down_proj.copy_(torch.randn_like(ref.experts.down_proj) * 0.1)

    ours = MoELayer(hidden, inter, n_experts, k, shared_expert=False)
    with torch.no_grad():
        ours.router.weight.weight.copy_(ref.gate.weight)
        for e in range(n_experts):
            gate_w, up_w = ref.experts.gate_up_proj[e].chunk(2, dim=0)
            ours.experts[e].gate_proj.weight.copy_(gate_w)
            ours.experts[e].up_proj.weight.copy_(up_w)
            ours.experts[e].down_proj.weight.copy_(ref.experts.down_proj[e])

    x = torch.randn(2, 3, hidden)
    out_ours, _, _ = ours(x)
    out_ref = ref(x)
    torch.testing.assert_close(out_ours, out_ref, rtol=1e-4, atol=1e-5)


def test_moe_shared_expert_always_contributes():
    torch.manual_seed(0)
    moe = MoELayer(d_model=8, d_ff=16, n_experts=4, k=2, shared_expert=True)
    x = torch.randn(2, 8)
    out_with, _, _ = moe(x)
    moe.shared_expert = None
    out_without, _, _ = moe(x)
    assert not torch.allclose(out_with, out_without)


# ---------------------------------------------------------------------------
# load_balancing_loss
# ---------------------------------------------------------------------------


def test_load_balancing_loss_minimal_when_perfectly_balanced():
    n_experts, n_tokens = 4, 8
    router_probs = torch.full((n_tokens, n_experts), 1.0 / n_experts)
    expert_indices = torch.arange(n_tokens).remainder(n_experts).unsqueeze(-1)
    loss = load_balancing_loss(router_probs, expert_indices, n_experts)
    torch.testing.assert_close(loss, torch.tensor(1.0), rtol=1e-5, atol=1e-5)


def test_load_balancing_loss_higher_when_collapsed():
    n_experts, n_tokens = 4, 8
    balanced_probs = torch.full((n_tokens, n_experts), 1.0 / n_experts)
    balanced_indices = torch.arange(n_tokens).remainder(n_experts).unsqueeze(-1)

    collapsed_probs = F.one_hot(torch.zeros(n_tokens, dtype=torch.long), n_experts).float()
    collapsed_indices = torch.zeros(n_tokens, 1, dtype=torch.long)

    balanced_loss = load_balancing_loss(balanced_probs, balanced_indices, n_experts)
    collapsed_loss = load_balancing_loss(collapsed_probs, collapsed_indices, n_experts)
    assert collapsed_loss > balanced_loss


def test_load_balancing_gradient_flows_only_through_router_scores():
    torch.manual_seed(0)
    moe = MoELayer(d_model=8, d_ff=16, n_experts=4, k=2, shared_expert=False)
    x = torch.randn(16, 8)
    _, router_probs, topk_indices = moe(x)
    loss = load_balancing_loss(router_probs, topk_indices, moe.n_experts)
    loss.backward()
    assert moe.router.weight.weight.grad is not None
    assert torch.any(moe.router.weight.weight.grad != 0)
    for expert in moe.experts:
        assert expert.gate_proj.weight.grad is None


# ---------------------------------------------------------------------------
# Toy MoE training: collapse vs balance
# ---------------------------------------------------------------------------


def test_train_toy_moe_usage_more_balanced_with_loss():
    cfg = MoeToyTrainConfig(n_tokens=1024, steps=400)
    usage_collapsed = train_toy_moe(cfg, use_balancing_loss=False)
    usage_balanced = train_toy_moe(cfg, use_balancing_loss=True)
    assert usage_collapsed.sum() == usage_balanced.sum() == cfg.n_tokens * cfg.k
    # std/mean (coefficient of variation) should shrink once the balancing loss is added.
    cv_collapsed = usage_collapsed.float().std() / usage_collapsed.float().mean()
    cv_balanced = usage_balanced.float().std() / usage_balanced.float().mean()
    assert cv_balanced <= cv_collapsed + 1e-6


# ---------------------------------------------------------------------------
# CLI smoke test
# ---------------------------------------------------------------------------


@pytest.mark.slow
def test_cli_demo_runs():
    """`demo` downloads two real configs (`AutoConfig.from_pretrained`), no weights."""
    result = runner.invoke(app, ["demo"])
    assert result.exit_code == 0
    assert "total" in result.stdout
