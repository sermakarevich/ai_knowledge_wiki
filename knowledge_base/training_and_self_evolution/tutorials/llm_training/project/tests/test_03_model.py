"""Chapter 03 — the real (non-meta) model: init, forward/backward, generation, checkpoints.

CPU only, no network: a tiny in-memory tokenizer stands in for the real 32k BPE tokenizer.
"""

import math
from pathlib import Path

import pytest
import torch

from llm_tutorial.model import (
    build_model,
    count_params,
    expected_init_loss,
    generate_samples,
    init_weights_report,
    load_checkpoint,
    round_up_to_multiple,
    save_checkpoint,
)

VOCAB_SIZE = 512

HYBRID_SECTION = {
    "arch": "qwen3_5",
    "vocab_size": VOCAB_SIZE,
    "hidden_size": 64,
    "intermediate_size": 128,
    "num_hidden_layers": 2,
    "num_attention_heads": 4,
    "num_key_value_heads": 2,
    "head_dim": 16,
    "linear_num_value_heads": 4,
    "linear_num_key_heads": 2,
    "linear_key_head_dim": 16,
    "linear_value_head_dim": 16,
    "full_attention_interval": 2,
    "tie_word_embeddings": True,
    "max_position_embeddings": 128,
}

DENSE_SECTION = {
    "arch": "qwen3",
    "vocab_size": VOCAB_SIZE,
    "hidden_size": 64,
    "intermediate_size": 128,
    "num_hidden_layers": 2,
    "num_attention_heads": 4,
    "num_key_value_heads": 2,
    "head_dim": 16,
    "tie_word_embeddings": True,
    "max_position_embeddings": 128,
}

SECTIONS = pytest.mark.parametrize("section", [HYBRID_SECTION, DENSE_SECTION], ids=["hybrid", "dense"])


@pytest.fixture(scope="module")
def tiny_tokenizer_dir(tmp_path_factory) -> Path:
    """A tiny `PreTrainedTokenizerFast` with an exact vocab of `VOCAB_SIZE` word-level tokens."""
    from tokenizers import Tokenizer, models, pre_tokenizers
    from transformers import PreTrainedTokenizerFast

    specials = ["<|endoftext|>", "<|pad|>"]
    vocab = {tok: i for i, tok in enumerate(specials)}
    for i in range(VOCAB_SIZE - len(specials)):
        vocab[f"tok{i}"] = len(vocab)
    assert len(vocab) == VOCAB_SIZE

    tokenizer = Tokenizer(models.WordLevel(vocab=vocab, unk_token="<|endoftext|>"))
    tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()
    fast = PreTrainedTokenizerFast(
        tokenizer_object=tokenizer, eos_token="<|endoftext|>", pad_token="<|pad|>"
    )
    out = tmp_path_factory.mktemp("tiny_tokenizer")
    fast.save_pretrained(out)
    return out


def test_round_up_to_multiple():
    assert round_up_to_multiple(512, 64) == 512
    assert round_up_to_multiple(500, 64) == 512
    assert round_up_to_multiple(1, 64) == 64


@SECTIONS
def test_build_model_matches_tokenizer_vocab(section, tiny_tokenizer_dir):
    model, config = build_model(section, device="cpu", tokenizer_dir=tiny_tokenizer_dir)
    assert config.vocab_size == VOCAB_SIZE
    assert config.pad_token_id == 1
    assert config.eos_token_id == 0


@SECTIONS
def test_build_model_rejects_vocab_mismatch(section, tiny_tokenizer_dir):
    bad_section = dict(section, vocab_size=VOCAB_SIZE + 64)
    with pytest.raises(ValueError, match="vocab_size"):
        build_model(bad_section, device="cpu", tokenizer_dir=tiny_tokenizer_dir)


@SECTIONS
def test_forward_loss_near_ln_vocab(section):
    model, config = build_model(section, device="cpu")
    model.eval()
    x = torch.randint(0, VOCAB_SIZE, (2, 32))
    with torch.no_grad():
        out = model(input_ids=x, labels=x)
    assert torch.isfinite(out.loss)
    assert abs(out.loss.item() - math.log(VOCAB_SIZE)) < 0.5


@SECTIONS
def test_one_adamw_step_decreases_loss(section):
    model, config = build_model(section, device="cpu")
    model.train()
    x = torch.randint(0, VOCAB_SIZE, (2, 32))
    optim = torch.optim.AdamW(model.parameters(), lr=1e-3)

    loss_before = model(input_ids=x, labels=x).loss
    optim.zero_grad()
    loss_before.backward()
    optim.step()

    with torch.no_grad():
        loss_after = model(input_ids=x, labels=x).loss

    assert loss_after.item() < loss_before.item()


@SECTIONS
def test_generate_samples_returns_one_string_per_prompt(section, tiny_tokenizer_dir):
    from transformers import AutoTokenizer

    model, config = build_model(section, device="cpu", tokenizer_dir=tiny_tokenizer_dir)
    tokenizer = AutoTokenizer.from_pretrained(tiny_tokenizer_dir)
    prompts = ["tok1 tok2 tok3", "tok4 tok5"]
    outputs = generate_samples(model, tokenizer, prompts, max_new_tokens=5)
    assert len(outputs) == len(prompts)
    assert all(isinstance(o, str) for o in outputs)


@SECTIONS
def test_checkpoint_round_trip_has_identical_logits(section, tiny_tokenizer_dir, tmp_path):
    from transformers import AutoTokenizer

    model, config = build_model(section, device="cpu", tokenizer_dir=tiny_tokenizer_dir)
    tokenizer = AutoTokenizer.from_pretrained(tiny_tokenizer_dir)
    model.eval()

    ckpt_dir = save_checkpoint(model, tokenizer, tmp_path, step=3)
    assert ckpt_dir == tmp_path / "checkpoints" / "step_3"
    loaded_model, loaded_tokenizer = load_checkpoint(ckpt_dir)
    loaded_model.eval()

    x = torch.randint(0, VOCAB_SIZE, (1, 16))
    with torch.no_grad():
        original = model(input_ids=x).logits
        restored = loaded_model(input_ids=x).logits
    assert torch.allclose(original, restored)
    assert loaded_tokenizer.vocab_size == VOCAB_SIZE


@SECTIONS
def test_count_params_keys(section):
    model, config = build_model(section, device="cpu")
    summary = count_params(model, config)
    assert set(summary) == {"total", "embedding", "non_embedding"}
    assert summary["total"] == summary["embedding"] + summary["non_embedding"]
    assert summary["embedding"] == VOCAB_SIZE * 64


@SECTIONS
def test_init_weights_report_std_near_initializer_range(section):
    model, config = build_model(section, device="cpu")
    report = init_weights_report(model)
    assert report
    for stats in report.values():
        assert abs(stats["mean"]) < 0.05
        assert 0.01 < stats["std"] < 0.03


def test_expected_init_loss():
    assert expected_init_loss(32000) == pytest.approx(math.log(32000))
