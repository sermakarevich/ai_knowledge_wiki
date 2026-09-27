"""Tests for chapter 03: our attention blocks vs torch / transformers references."""


import matplotlib
import pytest

matplotlib.use("Agg")
import torch
import torch.nn.functional as F
from typer.testing import CliRunner

from llm_blocks import plotting
from llm_blocks.ch03_attention import (
    GroupedQueryAttention,
    KVCache,
    MultiHeadAttention,
    RMSNorm,
    ToyConfig,
    ToyLM,
    app,
    causal_mask,
    greedy_decode,
    kv_cache_bytes,
    scaled_dot_product_attention,
)

runner = CliRunner()


# ---------------------------------------------------------------------------
# scaled dot-product attention
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("causal", [True, False])
def test_sdpa_matches_torch(causal):
    torch.manual_seed(0)
    q, k, v = (torch.randn(2, 3, 7, 8) for _ in range(3))

    ours, weights = scaled_dot_product_attention(q, k, v, causal=causal)
    reference = F.scaled_dot_product_attention(q, k, v, is_causal=causal)

    torch.testing.assert_close(ours, reference, rtol=1e-4, atol=1e-5)
    torch.testing.assert_close(weights.sum(dim=-1), torch.ones(2, 3, 7), rtol=1e-4, atol=1e-5)


def test_sdpa_weights_are_zero_in_the_future():
    torch.manual_seed(0)
    q, k, v = (torch.randn(1, 1, 5, 4) for _ in range(3))
    _, weights = scaled_dot_product_attention(q, k, v, causal=True)
    upper = torch.triu(weights[0, 0], diagonal=1)
    assert torch.count_nonzero(upper) == 0


def test_causal_mask_offset_for_a_single_new_query():
    """One query appended to a 4-token cache may look at all 5 keys."""
    mask = causal_mask(t_q=1, t_k=5)
    assert torch.isfinite(mask).all()
    assert mask.shape == (1, 1, 1, 5)


# ---------------------------------------------------------------------------
# multi-head attention
# ---------------------------------------------------------------------------


def test_multihead_matches_torch_multiheadattention():
    torch.manual_seed(0)
    d_model, n_heads, t = 16, 4, 6
    ours = MultiHeadAttention(d_model, n_heads)
    reference = torch.nn.MultiheadAttention(d_model, n_heads, batch_first=True)

    # torch packs q/k/v into a single (3*d, d) matrix; ours keeps them separate.
    with torch.no_grad():
        w = torch.cat([ours.q_proj.weight, ours.k_proj.weight, ours.v_proj.weight], dim=0)
        b = torch.cat([ours.q_proj.bias, ours.k_proj.bias, ours.v_proj.bias], dim=0)
        reference.in_proj_weight.copy_(w)
        reference.in_proj_bias.copy_(b)
        reference.out_proj.weight.copy_(ours.o_proj.weight)
        reference.out_proj.bias.copy_(ours.o_proj.bias)

    x = torch.randn(2, t, d_model)
    mask = torch.triu(torch.full((t, t), float("-inf")), diagonal=1)
    with torch.no_grad():
        ours_out, _ = ours(x, causal=True)
        ref_out, _ = reference(x, x, x, attn_mask=mask, need_weights=False)

    torch.testing.assert_close(ours_out, ref_out, rtol=1e-4, atol=1e-5)


def test_multihead_rejects_indivisible_dims():
    with pytest.raises(ValueError):
        MultiHeadAttention(d_model=10, n_heads=3)


# ---------------------------------------------------------------------------
# grouped-query attention vs transformers Qwen3Attention
# ---------------------------------------------------------------------------


def _identity_rope(batch: int, seq: int, head_dim: int):
    """cos = 1, sin = 0 turns `apply_rotary_pos_emb` into the identity, so the test
    compares attention alone (RoPE is chapter 04)."""
    cos = torch.ones(batch, seq, head_dim)
    sin = torch.zeros(batch, seq, head_dim)
    return cos, sin


def test_gqa_matches_transformers_qwen3_attention():
    """Equivalence with `transformers` 5.16 `Qwen3Attention`.

    Call signature in 5.16:
        Qwen3Attention(config, layer_idx)(hidden_states,
                                          position_embeddings=(cos, sin),
                                          attention_mask=additive_float_mask)
    and it returns `(attn_output, attn_weights)`. `config._attn_implementation = "eager"`
    is what makes it return real weights instead of `None`.

    Qwen3 always applies QK-norm, so the `qk_norm=False` variant of our module has no
    counterpart here; it is checked against our own maths in
    `test_gqa_without_qk_norm_matches_manual_maths`.
    """
    from transformers.models.qwen3.configuration_qwen3 import Qwen3Config
    from transformers.models.qwen3.modeling_qwen3 import Qwen3Attention

    torch.manual_seed(0)
    d_model, n_heads, n_kv_heads, head_dim, t = 32, 4, 2, 8, 6
    config = Qwen3Config(
        hidden_size=d_model,
        num_attention_heads=n_heads,
        num_key_value_heads=n_kv_heads,
        head_dim=head_dim,
        num_hidden_layers=1,
        intermediate_size=64,
        vocab_size=100,
        attention_bias=False,
        rms_norm_eps=1e-6,
    )
    config._attn_implementation = "eager"
    reference = Qwen3Attention(config, layer_idx=0).eval()

    ours = GroupedQueryAttention(d_model, n_heads, n_kv_heads, head_dim, qk_norm=True, gated=False)
    with torch.no_grad():
        ours.q_proj.weight.copy_(reference.q_proj.weight)
        ours.k_proj.weight.copy_(reference.k_proj.weight)
        ours.v_proj.weight.copy_(reference.v_proj.weight)
        ours.o_proj.weight.copy_(reference.o_proj.weight)
        ours.q_norm.weight.copy_(reference.q_norm.weight)
        ours.k_norm.weight.copy_(reference.k_norm.weight)

    x = torch.randn(2, t, d_model)
    mask = causal_mask(t, t)  # (1, 1, T, T) additive float mask, -inf above the diagonal
    with torch.no_grad():
        ours_out, ours_w = ours(x, causal=True)
        ref_out, ref_w = reference(
            x, position_embeddings=_identity_rope(2, t, head_dim), attention_mask=mask
        )

    torch.testing.assert_close(ours_out, ref_out, rtol=1e-4, atol=1e-5)
    torch.testing.assert_close(ours_w, ref_w, rtol=1e-4, atol=1e-5)


def test_gqa_without_qk_norm_matches_manual_maths():
    torch.manual_seed(0)
    d_model, n_heads, n_kv_heads, head_dim, t = 24, 6, 3, 4, 5
    ours = GroupedQueryAttention(d_model, n_heads, n_kv_heads, head_dim, qk_norm=False)
    x = torch.randn(1, t, d_model)

    with torch.no_grad():
        out, _ = ours(x)
        q = ours.q_proj(x).view(1, t, n_heads, head_dim).transpose(1, 2)
        k = ours.k_proj(x).view(1, t, n_kv_heads, head_dim).transpose(1, 2)
        v = ours.v_proj(x).view(1, t, n_kv_heads, head_dim).transpose(1, 2)
        k = k.repeat_interleave(n_heads // n_kv_heads, dim=1)
        v = v.repeat_interleave(n_heads // n_kv_heads, dim=1)
        expected = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        expected = ours.o_proj(expected.transpose(1, 2).reshape(1, t, n_heads * head_dim))

    torch.testing.assert_close(out, expected, rtol=1e-4, atol=1e-5)


def test_gqa_gate_multiplies_the_attention_output():
    torch.manual_seed(0)
    d_model, n_heads, n_kv_heads, head_dim, t = 16, 4, 2, 4, 5
    gated = GroupedQueryAttention(d_model, n_heads, n_kv_heads, head_dim, gated=True)
    plain = GroupedQueryAttention(d_model, n_heads, n_kv_heads, head_dim, gated=False)
    with torch.no_grad():
        for name in ("q_proj", "k_proj", "v_proj", "o_proj"):
            getattr(plain, name).weight.copy_(getattr(gated, name).weight)
        plain.q_norm.weight.copy_(gated.q_norm.weight)
        plain.k_norm.weight.copy_(gated.k_norm.weight)
        # A gate driven to +inf is the identity: sigmoid(large) = 1.
        gated.gate_proj.weight.fill_(0.0)
        gated.gate_proj.bias = torch.nn.Parameter(torch.full((n_heads * head_dim,), 30.0))

        x = torch.randn(1, t, d_model)
        torch.testing.assert_close(gated(x)[0], plain(x)[0], rtol=1e-4, atol=1e-5)

        # A gate driven to -inf zeroes the block out entirely.
        gated.gate_proj.bias.fill_(-30.0)
        torch.testing.assert_close(gated(x)[0], torch.zeros_like(x), rtol=1e-4, atol=1e-5)


def test_gqa_rejects_indivisible_head_counts():
    with pytest.raises(ValueError):
        GroupedQueryAttention(d_model=16, n_heads=5, n_kv_heads=2, head_dim=4)


def test_rmsnorm_matches_torch():
    torch.manual_seed(0)
    x = torch.randn(3, 7, 16)
    ours = RMSNorm(16)
    reference = torch.nn.RMSNorm(16, eps=1e-6)
    with torch.no_grad():
        reference.weight.copy_(ours.weight)
    torch.testing.assert_close(ours(x), reference(x), rtol=1e-4, atol=1e-5)


# ---------------------------------------------------------------------------
# KV cache
# ---------------------------------------------------------------------------


def test_kv_cache_bytes_formula():
    # 16 attention layers, 4 KV heads, head dim 256, 70k tokens, bf16.
    assert kv_cache_bytes(16, 4, 256, 70_000) == 2 * 16 * 4 * 256 * 70_000 * 2
    assert kv_cache_bytes(16, 4, 256, 2048) == 2 * kv_cache_bytes(16, 4, 256, 1024)
    # Halving the KV heads halves the cache: that is the whole point of GQA.
    assert kv_cache_bytes(16, 2, 256, 1024) * 2 == kv_cache_bytes(16, 4, 256, 1024)


def test_kv_cache_stacks_along_time():
    cache = KVCache()
    assert len(cache) == 0
    for step in range(3):
        k = torch.randn(1, 2, 1, 4)
        cache.append(k, k)
        assert len(cache) == step + 1


def test_gqa_step_by_step_with_cache_equals_full_forward():
    torch.manual_seed(0)
    d_model, n_heads, n_kv_heads, head_dim, t = 16, 4, 2, 4, 6
    attn = GroupedQueryAttention(d_model, n_heads, n_kv_heads, head_dim).eval()
    x = torch.randn(1, t, d_model)

    with torch.no_grad():
        full, _ = attn(x, causal=True)
        cache = KVCache()
        steps = [attn(x[:, i : i + 1], causal=True, cache=cache)[0] for i in range(t)]
    torch.testing.assert_close(torch.cat(steps, dim=1), full, rtol=1e-4, atol=1e-5)


def test_greedy_decode_same_tokens_but_fewer_flops_with_cache():
    torch.manual_seed(0)
    cfg = ToyConfig(n_layers=2)
    model = ToyLM(cfg).eval()
    prompt = torch.randint(0, cfg.vocab_size, (1, 5))

    cached, flops_cached = greedy_decode(model, prompt, n_new=12, use_cache=True)
    plain, flops_plain = greedy_decode(model, prompt, n_new=12, use_cache=False)

    assert torch.equal(cached, plain)
    assert flops_cached < flops_plain


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def test_plots_command_writes_every_figure(tmp_path, monkeypatch):
    monkeypatch.setattr(plotting, "ASSETS", tmp_path)
    result = runner.invoke(app, ["plots"])
    assert result.exit_code == 0, result.output
    expected = {
        "03_attention_weights_toy.png",
        "03_causal_mask.png",
        "03_multihead_schematic.png",
        "03_gqa_schematic.png",
        "03_kv_cache_growth.png",
        "03_qk_norm_effect.png",
    }
    assert expected <= {p.name for p in tmp_path.iterdir()}


def test_demo_command_runs():
    result = runner.invoke(app, ["demo"])
    assert result.exit_code == 0, result.output
    assert "identical output tokens: True" in result.output
