"""Chapter 04 — the training loop: LR schedule, param groups, and a tiny end-to-end run.

CPU only, no network: a small synthetic shard directory (reusing chapter 02's `write_shards`)
and the same tiny in-memory tokenizer chapter 03's tests use stand in for real data/tokenizer.
"""

import json

import numpy as np
import pytest
import torch
import yaml

from llm_tutorial.data import write_shards
from llm_tutorial.model import build_model
from llm_tutorial.pretrain import TrainConfig, build_param_groups, lr_at, train

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


# --------------------------------------------------------------------------- lr_at


def test_lr_at_warmup_is_linear_to_peak():
    lr, warmup_steps, total_steps = 1.0, 100, 1000
    assert lr_at(0, lr, warmup_steps, total_steps) == pytest.approx(0.01)
    assert lr_at(24, lr, warmup_steps, total_steps) == pytest.approx(0.25)
    assert lr_at(49, lr, warmup_steps, total_steps) == pytest.approx(0.50)
    assert lr_at(99, lr, warmup_steps, total_steps) == pytest.approx(1.0)


def test_lr_at_cosine_decays_to_min_lr():
    lr, min_lr_ratio, total_steps = 1.0, 0.1, 100
    kwargs = dict(lr=lr, warmup_steps=0, total_steps=total_steps, min_lr_ratio=min_lr_ratio, schedule="cosine")
    assert lr_at(0, **kwargs) == pytest.approx(1.0)
    assert lr_at(50, **kwargs) == pytest.approx(0.55, abs=1e-6)
    assert lr_at(100, **kwargs) == pytest.approx(0.1)
    assert lr_at(150, **kwargs) == pytest.approx(0.1)  # clamped at the floor past total_steps


def test_lr_at_wsd_is_flat_then_decays():
    lr, min_lr_ratio, total_steps = 1.0, 0.1, 100
    kwargs = dict(
        lr=lr, warmup_steps=0, total_steps=total_steps, min_lr_ratio=min_lr_ratio,
        schedule="wsd", decay_fraction=0.2,
    )
    assert lr_at(0, **kwargs) == pytest.approx(1.0)
    assert lr_at(79, **kwargs) == pytest.approx(1.0)  # still on the stable plateau
    assert lr_at(90, **kwargs) == pytest.approx(0.55, abs=1e-6)  # halfway through the decay
    assert lr_at(100, **kwargs) == pytest.approx(0.1)


# ------------------------------------------------------------------ param group split


def test_build_param_groups_excludes_norms_and_embeddings_from_decay():
    model, _ = build_model(HYBRID_SECTION, device="cpu")
    decay_group, no_decay_group = build_param_groups(model, weight_decay=0.1)
    assert decay_group["weight_decay"] == 0.1
    assert no_decay_group["weight_decay"] == 0.0
    assert all(p.dim() >= 2 for p in decay_group["params"])
    assert any(p.dim() < 2 for p in no_decay_group["params"])  # norms/biases live here
    n_total = sum(p.numel() for p in model.parameters() if p.requires_grad)
    n_grouped = sum(p.numel() for p in decay_group["params"]) + sum(p.numel() for p in no_decay_group["params"])
    assert n_total == n_grouped


# ---------------------------------------------------------------- end-to-end tiny run


@pytest.fixture(scope="module")
def tiny_tokenizer_dir(tmp_path_factory):
    from tokenizers import Tokenizer, models, pre_tokenizers
    from transformers import PreTrainedTokenizerFast

    specials = ["<|endoftext|>", "<|pad|>"]
    vocab = {tok: i for i, tok in enumerate(specials)}
    for i in range(VOCAB_SIZE - len(specials)):
        vocab[f"tok{i}"] = len(vocab)

    tokenizer = Tokenizer(models.WordLevel(vocab=vocab, unk_token="<|endoftext|>"))
    tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()
    fast = PreTrainedTokenizerFast(
        tokenizer_object=tokenizer, eos_token="<|endoftext|>", pad_token="<|pad|>"
    )
    out = tmp_path_factory.mktemp("tiny_tokenizer")
    fast.save_pretrained(out)
    return out


@pytest.fixture
def synthetic_data_dir(tmp_path):
    rng = np.random.default_rng(0)
    train_stream = (rng.integers(0, VOCAB_SIZE, size=500, dtype=np.uint16) for _ in range(20))
    data_dir = tmp_path / "data"
    write_shards(train_stream, data_dir, shard_tokens=2000, prefix="train")
    rng.integers(0, VOCAB_SIZE, size=4000, dtype=np.uint16).tofile(data_dir / "val.bin")
    return data_dir


@pytest.fixture
def model_config_path(tmp_path):
    path = tmp_path / "model.yaml"
    path.write_text(yaml.safe_dump({"model": HYBRID_SECTION}))
    return path


def _test_config(tmp_path, model_config_path, synthetic_data_dir, tiny_tokenizer_dir, run_name, train_tokens) -> TrainConfig:
    return TrainConfig(
        run_name=run_name,
        model_config=str(model_config_path),
        tokenizer_dir=str(tiny_tokenizer_dir),
        data_dir=str(synthetic_data_dir),
        block_size=32,
        micro_batch=2,
        grad_accum=1,
        train_tokens=train_tokens,
        lr=1e-3,
        warmup_steps=5,
        schedule="cosine",
        dtype="fp32",
        compile=False,
        eval_every=10,
        eval_tokens=256,
        sample_every=0,
        ckpt_every=10,
        keep_last=2,
        seed=0,
        prompts=["tok1 tok2"],
        log_every=1,
    )


def test_train_runs_30_steps_and_writes_artifacts(tmp_path, monkeypatch, model_config_path, synthetic_data_dir, tiny_tokenizer_dir):
    monkeypatch.chdir(tmp_path)
    config = _test_config(tmp_path, model_config_path, synthetic_data_dir, tiny_tokenizer_dir, "test_run", train_tokens=64 * 30)
    metrics = train(config)

    run_dir = tmp_path / "runs" / "test_run"
    assert (run_dir / "metrics.json").exists()
    log_lines = [json.loads(line) for line in (run_dir / "log.jsonl").read_text().splitlines()]
    train_losses = [line["loss"] for line in log_lines if "loss" in line]
    assert len(train_losses) >= 25
    assert train_losses[-1] < train_losses[0]
    assert metrics["total_steps"] == 30
    assert (run_dir / "checkpoints" / "final").exists()
    assert any((run_dir / "checkpoints").glob("step_*"))


def test_train_resume_continues_from_the_right_step(tmp_path, monkeypatch, model_config_path, synthetic_data_dir, tiny_tokenizer_dir):
    monkeypatch.chdir(tmp_path)
    short_config = _test_config(tmp_path, model_config_path, synthetic_data_dir, tiny_tokenizer_dir, "resume_run", train_tokens=64 * 12)
    train(short_config)

    run_dir = tmp_path / "runs" / "resume_run"
    log_lines = [json.loads(line) for line in (run_dir / "log.jsonl").read_text().splitlines()]
    steps_before = {line["step"] for line in log_lines if "loss" in line}
    assert max(steps_before) == 11

    longer_config = _test_config(tmp_path, model_config_path, synthetic_data_dir, tiny_tokenizer_dir, "resume_run", train_tokens=64 * 24)
    train(longer_config, resume=True)

    log_lines_after = [json.loads(line) for line in (run_dir / "log.jsonl").read_text().splitlines()]
    steps_after = {line["step"] for line in log_lines_after if "loss" in line}
    assert min(s for s in steps_after if s not in steps_before) == 12
    assert max(steps_after) == 23
