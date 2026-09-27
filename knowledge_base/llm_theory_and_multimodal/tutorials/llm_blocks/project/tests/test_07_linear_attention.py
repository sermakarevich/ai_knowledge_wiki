"""Tests for chapter 07: linear attention, the delta rule, Gated DeltaNet, the 3:1 hybrid.

The delta-rule tests compare our from-scratch functions to the pure-torch fallbacks in
`transformers.models.qwen3_5.modeling_qwen3_5` (`torch_recurrent_gated_delta_rule` and
`torch_chunk_gated_delta_rule`), which is what actually runs on this Mac because the
`fla` Triton kernel package is not installed.
"""

import math

import matplotlib
import pytest
import torch

matplotlib.use("Agg")
from typer.testing import CliRunner

from llm_blocks.ch07_linear_attention import (
    QWEN35_08B,
    QWEN38_27B,
    GatedDeltaNetBlock,
    app,
    associative_memory_errors,
    delta_rule_recurrent,
    gated_delta_rule_recurrent,
    l2norm,
    linear_attention,
    linear_attention_cost,
    linear_attention_parallel,
    linear_attention_recurrent,
    memory_persistence,
    overwrite_errors,
    recurrent_state_bytes,
    softmax_attention_cost,
    state_norm_trace,
)

runner = CliRunner()


# ---------------------------------------------------------------------------
# Cost counters
# ---------------------------------------------------------------------------


def test_softmax_cost_is_quadratic_and_linear_cost_is_linear():
    """Doubling the length roughly quadruples attention and exactly doubles the linear
    layer (attention is not exactly 4x because the projections are linear terms)."""
    a1, a2 = softmax_attention_cost(65536), softmax_attention_cost(131072)
    l1, l2 = linear_attention_cost(65536), linear_attention_cost(131072)
    assert 3.8 < a2 / a1 <= 4.0
    assert l2 / l1 == pytest.approx(2.0, rel=1e-9)


def test_linear_attention_is_cheaper_at_long_context():
    """At 70k tokens one DeltaNet layer is ~8x cheaper than one attention layer, and the
    gap keeps widening because only the attention side has a quadratic term."""
    ratio_70k = softmax_attention_cost(70_000) / linear_attention_cost(70_000)
    ratio_262k = softmax_attention_cost(262_144) / linear_attention_cost(262_144)
    assert ratio_70k > 5
    assert ratio_262k > 2.5 * ratio_70k


def test_recurrent_state_does_not_depend_on_length():
    """The whole point: the DeltaNet "cache" has no sequence dimension at all."""
    assert recurrent_state_bytes(QWEN38_27B) > recurrent_state_bytes(QWEN35_08B)
    # 48 value heads x 128 x 128 state + conv window, 2 bytes each
    expected_state = 48 * 128 * 128 * 2
    assert recurrent_state_bytes(QWEN38_27B) > expected_state


# ---------------------------------------------------------------------------
# Linear attention: parallel form == recurrent form
# ---------------------------------------------------------------------------


def test_linear_attention_parallel_equals_recurrent():
    torch.manual_seed(0)
    q, k, v = (torch.randn(2, 9, 3, 5) for _ in range(3))
    par = linear_attention_parallel(q, k, v)
    rec, state = linear_attention_recurrent(q, k, v)
    torch.testing.assert_close(par, rec, rtol=1e-4, atol=1e-5)
    assert state.shape == (2, 3, 5, 5)


def test_linear_attention_dispatcher():
    torch.manual_seed(1)
    q, k, v = (torch.randn(1, 6, 2, 4) for _ in range(3))
    torch.testing.assert_close(
        linear_attention(q, k, v, form="parallel"),
        linear_attention(q, k, v, form="recurrent"),
        rtol=1e-4,
        atol=1e-5,
    )
    with pytest.raises(ValueError):
        linear_attention(q, k, v, form="nonsense")


def test_linear_attention_is_causal():
    """Changing a *later* token's value must not change an earlier output."""
    torch.manual_seed(2)
    q, k, v = (torch.randn(1, 7, 1, 4) for _ in range(3))
    out_a = linear_attention_parallel(q, k, v)
    v2 = v.clone()
    v2[:, 5:] += 10.0
    out_b = linear_attention_parallel(q, k, v2)
    torch.testing.assert_close(out_a[:, :5], out_b[:, :5], rtol=1e-4, atol=1e-5)


# ---------------------------------------------------------------------------
# Delta rule vs the transformers torch fallbacks
# ---------------------------------------------------------------------------


def _reference_inputs(b=2, t=13, h=3, d_k=8, d_v=8, seed=0):
    torch.manual_seed(seed)
    q = torch.randn(b, t, h, d_k)
    k = torch.randn(b, t, h, d_k)
    v = torch.randn(b, t, h, d_v)
    beta = torch.rand(b, t, h)
    g = -torch.rand(b, t, h) * 0.5  # g = log(alpha), so alpha = exp(g) in (0, 1)
    return q, k, v, beta, g


def _normalised(q, k, d_k):
    """Replicate what the kernels do internally with `use_qk_l2norm_in_kernel=True`:
    L2-normalise q and k, then scale q by 1/sqrt(d_k)."""
    return l2norm(q) / math.sqrt(d_k), l2norm(k)


def test_gated_delta_rule_matches_transformers_recurrent():
    from transformers.models.qwen3_5.modeling_qwen3_5 import (
        torch_recurrent_gated_delta_rule,
    )

    q, k, v, beta, g = _reference_inputs()
    ref_out, ref_state = torch_recurrent_gated_delta_rule(
        q, k, v, g=g, beta=beta, initial_state=None, output_final_state=True,
        use_qk_l2norm_in_kernel=True,
    )
    qn, kn = _normalised(q, k, q.shape[-1])
    ours, state = gated_delta_rule_recurrent(qn, kn, v, beta, g.exp())
    torch.testing.assert_close(ours, ref_out, rtol=1e-4, atol=1e-5)
    torch.testing.assert_close(state, ref_state, rtol=1e-4, atol=1e-5)


def test_gated_delta_rule_matches_transformers_chunked():
    """The chunked kernel is the one that runs for a prefill; it must give the same
    numbers as the token-by-token loop."""
    from transformers.models.qwen3_5.modeling_qwen3_5 import (
        torch_chunk_gated_delta_rule,
    )

    q, k, v, beta, g = _reference_inputs(t=70, seed=3)  # > one 64-token chunk
    ref_out, _ = torch_chunk_gated_delta_rule(
        q, k, v, g=g, beta=beta, initial_state=None, output_final_state=False,
        use_qk_l2norm_in_kernel=True,
    )
    qn, kn = _normalised(q, k, q.shape[-1])
    ours, _ = gated_delta_rule_recurrent(qn, kn, v, beta, g.exp())
    torch.testing.assert_close(ours, ref_out, rtol=1e-4, atol=1e-5)


def test_delta_rule_is_gated_rule_with_alpha_one():
    from transformers.models.qwen3_5.modeling_qwen3_5 import (
        torch_recurrent_gated_delta_rule,
    )

    q, k, v, beta, _ = _reference_inputs(seed=7)
    g = torch.zeros_like(beta)  # alpha = exp(0) = 1: no decay
    ref_out, _ = torch_recurrent_gated_delta_rule(
        q, k, v, g=g, beta=beta, initial_state=None, output_final_state=False,
        use_qk_l2norm_in_kernel=True,
    )
    qn, kn = _normalised(q, k, q.shape[-1])
    ours, _ = delta_rule_recurrent(qn, kn, v, beta)
    torch.testing.assert_close(ours, ref_out, rtol=1e-4, atol=1e-5)


def test_delta_rule_with_beta_zero_writes_nothing():
    """beta = 0 means "do not write": the state stays empty and the output is zero."""
    torch.manual_seed(4)
    q, k, v = torch.randn(1, 6, 1, 4), torch.randn(1, 6, 1, 4), torch.randn(1, 6, 1, 4)
    out, state = delta_rule_recurrent(q, k, v, torch.zeros(1, 6, 1))
    torch.testing.assert_close(out, torch.zeros_like(out), atol=1e-6, rtol=0)
    torch.testing.assert_close(state, torch.zeros_like(state), atol=1e-6, rtol=0)


def test_delta_rule_with_beta_one_stores_the_last_key_exactly():
    """With unit-norm keys and beta = 1, `I - k k^T` is an exact projection, so reading
    back the most recently written key returns its value with no interference."""
    torch.manual_seed(5)
    t, d = 6, 8
    k = torch.nn.functional.normalize(torch.randn(1, t, 1, d), dim=-1)
    v = torch.randn(1, t, 1, d)
    q = k.clone()  # query each position with its own key
    out, _ = delta_rule_recurrent(q, k, v, torch.ones(1, t, 1))
    torch.testing.assert_close(out[:, -1], v[:, -1], rtol=1e-4, atol=1e-5)


def test_gate_shrinks_the_state():
    """alpha < 1 has to produce a smaller state than alpha = 1 on the same inputs."""
    torch.manual_seed(6)
    q, k, v = torch.randn(1, 20, 1, 6), torch.randn(1, 20, 1, 6), torch.randn(1, 20, 1, 6)
    beta = torch.full((1, 20, 1), 0.5)
    _, gated = gated_delta_rule_recurrent(q, k, v, beta, torch.full((1, 20, 1), 0.8))
    _, plain = delta_rule_recurrent(q, k, v, beta)
    assert gated.norm() < plain.norm()


# ---------------------------------------------------------------------------
# The whole block vs transformers' Qwen3_5GatedDeltaNet
# ---------------------------------------------------------------------------


def _tiny_config(hidden=32, num_k_heads=2, num_v_heads=4, head_dim=8):
    from transformers.models.qwen3_5 import Qwen3_5TextConfig

    return Qwen3_5TextConfig(
        hidden_size=hidden,
        intermediate_size=2 * hidden,
        num_hidden_layers=4,
        num_attention_heads=2,
        num_key_value_heads=1,
        head_dim=hidden // 2,
        linear_num_key_heads=num_k_heads,
        linear_num_value_heads=num_v_heads,
        linear_key_head_dim=head_dim,
        linear_value_head_dim=head_dim,
        linear_conv_kernel_dim=4,
        vocab_size=64,
    )


@pytest.mark.parametrize("num_v_heads", [2, 4])
def test_block_matches_qwen3_5_gated_deltanet(num_v_heads):
    """Copy every weight across and compare a single no-cache forward pass.

    `num_v_heads = 2` is the "one value head per key head" case (as in the real 0.8B);
    `num_v_heads = 4` exercises the `repeat_interleave` path (as in the real 27B, which
    has 48 value heads sharing 16 key heads).
    """
    from transformers.models.qwen3_5.modeling_qwen3_5 import Qwen3_5GatedDeltaNet

    torch.manual_seed(0)
    hidden, num_k_heads, head_dim = 32, 2, 8
    config = _tiny_config(hidden, num_k_heads, num_v_heads, head_dim)
    ref = Qwen3_5GatedDeltaNet(config, layer_idx=0).eval()
    ours = GatedDeltaNetBlock(
        hidden_size=hidden,
        num_k_heads=num_k_heads,
        num_v_heads=num_v_heads,
        head_k_dim=head_dim,
        head_v_dim=head_dim,
        conv_kernel_size=config.linear_conv_kernel_dim,
        eps=config.rms_norm_eps,
    ).eval()

    with torch.no_grad():
        for name in ["in_proj_qkv", "in_proj_z", "in_proj_a", "in_proj_b", "out_proj"]:
            getattr(ours, name).weight.copy_(getattr(ref, name).weight)
        ours.conv1d.weight.copy_(ref.conv1d.weight)
        ours.dt_bias.copy_(ref.dt_bias)
        ours.A_log.copy_(ref.A_log)
        ours.norm.weight.copy_(ref.norm.weight)

    x = torch.randn(2, 11, hidden)
    with torch.no_grad():
        torch.testing.assert_close(ours(x), ref(x), rtol=1e-4, atol=1e-5)


def test_block_output_shape_and_causality():
    torch.manual_seed(1)
    block = GatedDeltaNetBlock(16, num_k_heads=2, num_v_heads=2, head_k_dim=8, head_v_dim=8).eval()
    x = torch.randn(1, 12, 16)
    with torch.no_grad():
        out_a = block(x)
        x2 = x.clone()
        x2[:, 8:] += 3.0
        out_b = block(x2)
    assert out_a.shape == (1, 12, 16)
    torch.testing.assert_close(out_a[:, :8], out_b[:, :8], rtol=1e-4, atol=1e-5)


# ---------------------------------------------------------------------------
# The two teaching demos
# ---------------------------------------------------------------------------


def test_delta_rule_retrieves_better_than_linear_attention():
    errors = associative_memory_errors()
    assert errors["delta rule"].mean() < errors["linear attention"].mean()
    # the last-written pair is exact under the delta rule (unit keys, beta = 1)
    assert errors["delta rule"][-1] < 1e-5


def test_delta_rule_overwrites_a_reused_key():
    """The case the rule exists for: linear attention returns roughly old + new (error
    around 1), the delta rule returns the new value."""
    errors = overwrite_errors()
    assert errors["linear attention"].mean() > 0.8
    assert errors["delta rule"].mean() < 0.4
    assert errors["delta rule"][-1] < 1e-5


def test_state_norm_bounds():
    """Plain accumulation grows without bound; the delta rule bounds it; the gate lowers
    that bound further."""
    traces = state_norm_trace()
    plain = traces["plain linear attention (no delta, no gate)"]
    delta = traces["delta rule, no gate (alpha = 1)"]
    gated = next(v for k, v in traces.items() if k.startswith("delta rule + decay"))
    assert plain[-1] > 2 * delta[-1]  # plain accumulation ends far above the delta rule
    assert gated[-1] < delta[-1]
    assert delta[-1] / delta[len(delta) // 2] < 1.5  # settled, not still climbing


def test_gate_sets_a_forgetting_horizon():
    """A smaller alpha must forget the stored memory sooner."""
    persistence = memory_persistence()
    at_50 = {a: errors[50] for a, errors in persistence.items()}
    assert at_50[0.95] > at_50[0.99] > at_50[1.0]


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def test_demo_runs():
    result = runner.invoke(app, ["demo"])
    assert result.exit_code == 0, result.output
    assert "Gated DeltaNet" in result.output
