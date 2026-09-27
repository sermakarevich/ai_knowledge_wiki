"""Tests for chapter 01: Linear/MLP2/activations vs torch reference, train_toy, plots."""

import matplotlib

matplotlib.use("Agg")
import torch
import torch.nn.functional as F
from typer.testing import CliRunner

from llm_blocks import plotting
from llm_blocks.ch01_neural_networks import (
    MLP2,
    Linear,
    TrainConfig,
    app,
    gelu_exact,
    gelu_tanh,
    relu,
    silu,
    swiglu,
    train_toy,
)

runner = CliRunner()


def test_linear_matches_torch():
    torch.manual_seed(0)
    x = torch.randn(8, 5)

    ours = Linear(5, 3)
    reference = torch.nn.Linear(5, 3)
    reference.weight.data.copy_(ours.weight.data)
    reference.bias.data.copy_(ours.bias.data)

    torch.testing.assert_close(ours(x), reference(x), rtol=1e-4, atol=1e-5)


def test_mlp2_matches_sequential():
    torch.manual_seed(0)
    x = torch.randn(8, 4)

    ours = MLP2(4, 6, 2, activation=relu)
    reference = torch.nn.Sequential(
        torch.nn.Linear(4, 6),
        torch.nn.ReLU(),
        torch.nn.Linear(6, 2),
    )
    reference[0].weight.data.copy_(ours.fc1.weight.data)
    reference[0].bias.data.copy_(ours.fc1.bias.data)
    reference[2].weight.data.copy_(ours.fc2.weight.data)
    reference[2].bias.data.copy_(ours.fc2.bias.data)

    torch.testing.assert_close(ours(x), reference(x), rtol=1e-4, atol=1e-5)


def test_relu_matches_torch():
    x = torch.randn(100)
    torch.testing.assert_close(relu(x), F.relu(x))


def test_gelu_tanh_matches_torch():
    x = torch.randn(100)
    torch.testing.assert_close(gelu_tanh(x), F.gelu(x, approximate="tanh"), rtol=1e-4, atol=1e-5)


def test_gelu_exact_matches_torch():
    x = torch.randn(100)
    torch.testing.assert_close(gelu_exact(x), F.gelu(x, approximate="none"), rtol=1e-4, atol=1e-5)


def test_silu_matches_torch():
    x = torch.randn(100)
    torch.testing.assert_close(silu(x), F.silu(x))


def test_swiglu_shape_and_gating():
    torch.manual_seed(0)
    x = torch.randn(4, 8)
    w_gate = torch.randn(8, 16)
    w_up = torch.randn(8, 16)

    out = swiglu(x, w_gate, w_up)
    assert out.shape == (4, 16)
    torch.testing.assert_close(out, silu(x @ w_gate) * (x @ w_up))


def test_train_toy_reduces_loss_and_fits_moons():
    cfg = TrainConfig(steps=300, hidden=16, lr=0.5, seed=0, snapshot_steps=(0, 50, 300))
    result = train_toy(cfg)

    assert len(result["losses"]) == 300
    assert result["losses"][-1] < result["losses"][0]
    assert result["accuracy"] > 0.9
    assert set(result["snapshots"].keys()) == {0, 50, 300}
    assert result["snapshots"][0].shape == result["xx"].shape


def test_ch01_plots_runs(tmp_path, monkeypatch):
    monkeypatch.setattr(plotting, "ASSETS", tmp_path)

    result = runner.invoke(app, ["plots"])

    assert result.exit_code == 0
    for name in [
        "01_activations",
        "01_loss_surface",
        "01_moons_training",
        "01_loss_curve",
        "01_matmul_picture",
    ]:
        assert (tmp_path / f"{name}.png").is_file()


def test_ch01_demo_runs():
    result = runner.invoke(app, ["demo"])

    assert result.exit_code == 0
    assert "parameters" in result.stdout
    assert "accuracy" in result.stdout
