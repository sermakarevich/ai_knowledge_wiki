"""Tests for chapter 10: our assembled decoder must *be* Qwen3, not resemble it.

The two tests that matter are `test_tiny_logits_match_transformers` (same logits) and
`test_tiny_greedy_decode_matches` (same tokens). Everything downloadable is marked slow.
"""

import matplotlib
import pytest
import torch

matplotlib.use("Agg")
from typer.testing import CliRunner

from llm_blocks.ch10_transformer import (
    TINY_HF_KWARGS,
    WEIGHT_MAP,
    Decoder,
    DecoderLayer,
    app,
    bytes_per_weight_table,
    count_params_and_flops,
    decoder_config_from_hf,
    greedy_decode,
    load_qwen3_weights,
    tiny_pair,
)

runner = CliRunner()
VOCAB = TINY_HF_KWARGS["vocab_size"]


def _tiny_config(**overrides):
    from transformers.models.qwen3 import Qwen3Config

    return Qwen3Config(**{**TINY_HF_KWARGS, **overrides})


# ---------------------------------------------------------------------------
# Equivalence with transformers' Qwen3ForCausalLM
# ---------------------------------------------------------------------------


def test_tiny_logits_match_transformers():
    pytest.importorskip("transformers")
    _, hf_model, ours = tiny_pair(seed=0)
    torch.manual_seed(1)
    ids = torch.randint(0, VOCAB, (3, 16))
    with torch.no_grad():
        ref = hf_model(ids).logits
        got = ours(ids)
    assert got.shape == ref.shape
    torch.testing.assert_close(got, ref, rtol=1e-4, atol=1e-5)


def test_tiny_greedy_decode_matches():
    pytest.importorskip("transformers")
    _, hf_model, ours = tiny_pair(seed=2)
    torch.manual_seed(3)
    prompt = torch.randint(0, VOCAB, (1, 5))
    assert greedy_decode(ours, prompt, 10) == greedy_decode(hf_model, prompt, 10)


def test_tied_embeddings_variant_matches():
    """`tie_word_embeddings=True`: the LM head is the embedding matrix, nothing to copy."""
    pytest.importorskip("transformers")
    from transformers.models.qwen3.modeling_qwen3 import Qwen3ForCausalLM

    torch.manual_seed(4)
    config = _tiny_config(tie_word_embeddings=True)
    hf_model = Qwen3ForCausalLM(config).eval()
    ours = Decoder(decoder_config_from_hf(config)).eval()
    load_qwen3_weights(ours, hf_model)
    ids = torch.randint(0, VOCAB, (2, 9))
    with torch.no_grad():
        torch.testing.assert_close(ours(ids), hf_model(ids).logits, rtol=1e-4, atol=1e-5)
    assert sum(p.numel() for p in ours.parameters()) < sum(
        p.numel() for p in Decoder(decoder_config_from_hf(_tiny_config())).parameters()
    )


def test_parameter_counts_agree():
    pytest.importorskip("transformers")
    _, hf_model, ours = tiny_pair(seed=5)
    assert sum(p.numel() for p in ours.parameters()) == sum(
        p.numel() for p in hf_model.parameters()
    )


def test_weight_map_covers_every_checkpoint_tensor():
    """`load_qwen3_weights` raises if any checkpoint tensor is left unclaimed."""
    pytest.importorskip("transformers")
    _, hf_model, ours = tiny_pair(seed=6)
    n_expected = len([k for k in WEIGHT_MAP if "{i}" in k]) * ours.cfg.n_layers + len(
        [k for k in WEIGHT_MAP if "{i}" not in k]
    )
    assert len(hf_model.state_dict()) == n_expected


def test_load_rejects_a_mismatched_config():
    """A shape mismatch must fail loudly rather than silently produce a different model."""
    pytest.importorskip("transformers")
    from transformers.models.qwen3.modeling_qwen3 import Qwen3ForCausalLM

    hf_model = Qwen3ForCausalLM(_tiny_config()).eval()
    wrong = decoder_config_from_hf(_tiny_config())
    wrong.d_ff = 256  # the checkpoint's MLP is 128 wide
    with pytest.raises(ValueError, match="shape mismatch"):
        load_qwen3_weights(Decoder(wrong), hf_model)


# ---------------------------------------------------------------------------
# The decoder on its own: caching, shapes, RoPE actually being applied
# ---------------------------------------------------------------------------


def test_kv_cache_decoding_matches_full_recompute():
    pytest.importorskip("transformers")
    _, _, ours = tiny_pair(seed=7)
    torch.manual_seed(8)
    ids = torch.randint(0, VOCAB, (1, 7))
    with torch.no_grad():
        full = ours(ids)
        caches = ours.new_caches()
        step = torch.cat([ours(ids[:, i : i + 1], caches=caches) for i in range(ids.shape[1])], 1)
    torch.testing.assert_close(step, full, rtol=1e-4, atol=1e-5)


def test_rope_makes_the_decoder_order_sensitive():
    """Without positions a decoder's first token would see the same thing in any order."""
    pytest.importorskip("transformers")
    _, _, ours = tiny_pair(seed=9)
    ids = torch.tensor([[3, 17, 42, 8]])
    with torch.no_grad():
        a = ours(ids)[0, -1]
        b = ours(ids[:, [1, 0, 2, 3]])[0, -1]
    assert not torch.allclose(a, b, atol=1e-3)


def test_decoder_layer_is_residual():
    """A layer only ever *adds* to the stream, so zeroing its two output projections
    must make it the identity — the property that lets 64 of them stack."""
    pytest.importorskip("transformers")
    cfg = decoder_config_from_hf(_tiny_config())
    layer = DecoderLayer(cfg).eval()
    with torch.no_grad():
        layer.self_attn.o_proj.weight.zero_()
        layer.mlp.down_proj.weight.zero_()
        x = torch.randn(2, 6, cfg.d_model)
        cos, sin = torch.ones(6, cfg.head_dim), torch.zeros(6, cfg.head_dim)
        torch.testing.assert_close(layer(x, cos, sin), x)


# ---------------------------------------------------------------------------
# Counting
# ---------------------------------------------------------------------------


def test_count_params_and_flops_on_a_tiny_config():
    pytest.importorskip("transformers")
    config = _tiny_config()
    counts = count_params_and_flops(config, seq=64)
    _, hf_model, _ = tiny_pair(seed=10)
    assert counts["total_params"] == sum(p.numel() for p in hf_model.parameters())
    assert counts["flops"]["embeddings"] == 0  # a lookup is not arithmetic
    assert counts["n_attention_layers"] == config.num_hidden_layers
    # Attention's score/value term is the only one that grows with the context.
    longer = count_params_and_flops(config, seq=256)
    assert longer["flops"]["attention scores"] == 4 * counts["flops"]["attention scores"]
    assert longer["flops"]["mlp"] == counts["flops"]["mlp"]


def test_bytes_per_weight_table():
    gb = bytes_per_weight_table(27e9)
    assert gb["bf16 (2 bytes)"] == pytest.approx(54.0)
    assert 14 < gb["4-bit (0.5 byte + scales)"] < 17


# ---------------------------------------------------------------------------
# CLI smoke tests
# ---------------------------------------------------------------------------


def test_cli_help_runs():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0


@pytest.mark.slow
def test_cli_plots_runs():
    """`plots` downloads three config files (no weights)."""
    assert runner.invoke(app, ["plots"]).exit_code == 0


@pytest.mark.slow
def test_cli_demo_runs():
    result = runner.invoke(app, ["demo"])
    assert result.exit_code == 0
    assert "identical                  True" in result.stdout
