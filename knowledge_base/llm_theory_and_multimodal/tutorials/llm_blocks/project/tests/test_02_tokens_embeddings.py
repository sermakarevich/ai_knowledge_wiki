"""Tests for chapter 02: Embedding/softmax/cross_entropy/TiedLMHead vs torch reference, plots."""

import matplotlib
import pytest

matplotlib.use("Agg")
import torch
import torch.nn.functional as F
from typer.testing import CliRunner

from llm_blocks import plotting
from llm_blocks.ch02_tokens_embeddings import (
    Embedding,
    TiedLMHead,
    app,
    cross_entropy,
    softmax,
)

runner = CliRunner()


def test_embedding_matches_torch():
    torch.manual_seed(0)
    ids = torch.tensor([3, 0, 7, 7, 2])

    ours = Embedding(vocab_size=10, dim=4)
    reference = torch.nn.Embedding(10, 4)
    reference.weight.data.copy_(ours.weight.data)

    torch.testing.assert_close(ours(ids), reference(ids))


def test_embedding_lookup_equals_one_hot_matmul():
    torch.manual_seed(0)
    emb = Embedding(vocab_size=6, dim=5)
    ids = torch.tensor([0, 3, 5, 1])

    torch.testing.assert_close(emb(ids), emb.one_hot_lookup(ids))


def test_softmax_matches_torch():
    torch.manual_seed(0)
    x = torch.randn(4, 9)
    torch.testing.assert_close(softmax(x, temperature=1.0), torch.softmax(x, dim=-1), rtol=1e-5, atol=1e-6)


@pytest.mark.parametrize("temperature", [0.3, 1.0, 3.0])
def test_softmax_matches_torch_at_temperature(temperature):
    torch.manual_seed(0)
    x = torch.randn(4, 9)
    ours = softmax(x, temperature=temperature)
    reference = torch.softmax(x / temperature, dim=-1)
    torch.testing.assert_close(ours, reference, rtol=1e-5, atol=1e-6)
    torch.testing.assert_close(ours.sum(dim=-1), torch.ones(4))


def test_softmax_max_subtraction_is_stable_for_large_logits():
    x = torch.tensor([[1000.0, 1001.0, 999.0]])
    probs = softmax(x)
    assert torch.isfinite(probs).all()
    torch.testing.assert_close(probs.sum(dim=-1), torch.ones(1))


def test_cross_entropy_matches_torch():
    torch.manual_seed(0)
    logits = torch.randn(8, 12)
    targets = torch.randint(0, 12, (8,))
    torch.testing.assert_close(cross_entropy(logits, targets), F.cross_entropy(logits, targets), rtol=1e-4, atol=1e-5)


def test_tied_lm_head_matches_linear():
    torch.manual_seed(0)
    emb = Embedding(vocab_size=10, dim=6)
    h = torch.randn(3, 6)

    head = TiedLMHead(emb)
    reference = torch.nn.Linear(6, 10, bias=False)
    reference.weight.data.copy_(emb.weight.data)

    torch.testing.assert_close(head(h), reference(h), rtol=1e-4, atol=1e-5)


def test_ch02_plots_runs(tmp_path, monkeypatch):
    monkeypatch.setattr(plotting, "ASSETS", tmp_path)

    result = runner.invoke(app, ["plots"])

    assert result.exit_code == 0
    for name in [
        "02_one_hot_lookup",
        "02_softmax_temperature",
        "02_cross_entropy",
        "02_embedding_size",
    ]:
        assert (tmp_path / f"{name}.png").is_file()


def test_ch02_demo_runs():
    result = runner.invoke(app, ["demo"])

    assert result.exit_code == 0
    assert "ln(32,000)" in result.stdout
    assert "ln(248,320)" in result.stdout


@pytest.mark.slow
def test_ch02_plots_real_runs(tmp_path, monkeypatch):
    monkeypatch.setattr(plotting, "ASSETS", tmp_path)

    result = runner.invoke(app, ["plots-real"])

    assert result.exit_code == 0
    assert (tmp_path / "02_tokens_example.png").is_file()
    assert (tmp_path / "02_embeddings_pca.png").is_file()
    assert (tmp_path / "02_nearest_neighbours.txt").is_file()
