"""Chapter 01 — neural networks in one page: neurons, matmul, activations, loss, GD.

`uv run python -m llm_blocks.ch01_neural_networks plots` draws every figure this
chapter embeds; `demo` prints the parameter counts and final accuracy quoted in the
chapter text.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import matplotlib.pyplot as plt
import numpy as np
import torch
import typer
from sklearn.datasets import make_moons
from torch import Tensor, nn

from llm_blocks.plotting import annotate_arrow, save, style

app = typer.Typer(add_completion=False, no_args_is_help=False)


# ---------------------------------------------------------------------------
# From-scratch building blocks
# ---------------------------------------------------------------------------


class Linear(nn.Module):
    """From-scratch `y = x W^T + b`, laid out like `torch.nn.Linear` (weight is (out, in))."""

    def __init__(self, in_features: int, out_features: int) -> None:
        super().__init__()
        bound = 1 / math.sqrt(in_features)
        self.weight = nn.Parameter(torch.empty(out_features, in_features).uniform_(-bound, bound))
        self.bias = nn.Parameter(torch.empty(out_features).uniform_(-bound, bound))

    def forward(self, x: Tensor) -> Tensor:
        return x @ self.weight.T + self.bias


class MLP2(nn.Module):
    """Linear -> activation -> Linear: the smallest network that is not just one matmul."""

    def __init__(self, in_features: int, hidden: int, out_features: int, activation=None) -> None:
        super().__init__()
        self.fc1 = Linear(in_features, hidden)
        self.fc2 = Linear(hidden, out_features)
        self.activation = activation if activation is not None else relu

    def forward(self, x: Tensor) -> Tensor:
        return self.fc2(self.activation(self.fc1(x)))


def relu(x: Tensor) -> Tensor:
    """max(0, x): a hinge, the simplest non-linearity."""
    return torch.clamp(x, min=0.0)


def gelu_tanh(x: Tensor) -> Tensor:
    """GELU, tanh approximation (what most LLM code actually runs)."""
    return 0.5 * x * (1.0 + torch.tanh(math.sqrt(2.0 / math.pi) * (x + 0.044715 * x.pow(3))))


def gelu_exact(x: Tensor) -> Tensor:
    """GELU, exact form using the Gaussian error function `erf`."""
    return x * 0.5 * (1.0 + torch.erf(x / math.sqrt(2.0)))


def silu(x: Tensor) -> Tensor:
    """SiLU / swish: `x * sigmoid(x)`, smoother than ReLU and used as the SwiGLU activation."""
    return x * torch.sigmoid(x)


def swiglu(x: Tensor, w_gate: Tensor, w_up: Tensor) -> Tensor:
    """SwiGLU gating: `silu(x @ W_gate) * (x @ W_up)` — a learned "volume knob" times a value."""
    gate = silu(x @ w_gate)
    value = x @ w_up
    return gate * value


# ---------------------------------------------------------------------------
# The two-moons demo
# ---------------------------------------------------------------------------


@dataclass
class TrainConfig:
    hidden: int = 16
    lr: float = 0.5
    steps: int = 300
    seed: int = 0
    n_samples: int = 500
    noise: float = 0.2
    snapshot_steps: tuple[int, ...] = field(default_factory=lambda: (0, 50, 300))


def train_toy(cfg: TrainConfig) -> dict:
    """Fit `MLP2` on two-moons with hand-written SGD (`p -= lr * p.grad`), no optimizer object."""
    torch.manual_seed(cfg.seed)
    x_np, y_np = make_moons(n_samples=cfg.n_samples, noise=cfg.noise, random_state=cfg.seed)
    x = torch.tensor(x_np, dtype=torch.float32)
    y = torch.tensor(y_np, dtype=torch.float32).unsqueeze(1)

    model = MLP2(in_features=2, hidden=cfg.hidden, out_features=1, activation=relu)

    pad = 0.5
    xx, yy = np.meshgrid(
        np.linspace(x_np[:, 0].min() - pad, x_np[:, 0].max() + pad, 200),
        np.linspace(x_np[:, 1].min() - pad, x_np[:, 1].max() + pad, 200),
    )
    grid = torch.tensor(np.c_[xx.ravel(), yy.ravel()], dtype=torch.float32)

    def boundary_probs() -> np.ndarray:
        with torch.no_grad():
            logits = model(grid)
            return torch.sigmoid(logits).reshape(xx.shape).numpy()

    losses: list[float] = []
    snapshots: dict[int, np.ndarray] = {}
    if 0 in cfg.snapshot_steps:
        snapshots[0] = boundary_probs()

    for step in range(1, cfg.steps + 1):
        logits = model(x)
        loss = nn.functional.binary_cross_entropy_with_logits(logits, y)

        for p in model.parameters():
            p.grad = None
        loss.backward()
        with torch.no_grad():
            for p in model.parameters():
                p -= cfg.lr * p.grad

        losses.append(loss.item())
        if step in cfg.snapshot_steps:
            snapshots[step] = boundary_probs()

    with torch.no_grad():
        preds = (torch.sigmoid(model(x)) > 0.5).float()
        accuracy = (preds == y).float().mean().item()

    return {
        "model": model,
        "losses": losses,
        "snapshots": snapshots,
        "xx": xx,
        "yy": yy,
        "x": x_np,
        "y": y_np,
        "accuracy": accuracy,
    }


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------


def _fig_activations():
    style()
    x = torch.linspace(-4, 4, 400, requires_grad=True)

    fig, (ax_f, ax_d) = plt.subplots(1, 2, figsize=(11, 4.5))
    for name, fn in [("ReLU", relu), ("GELU", gelu_tanh), ("SiLU", silu)]:
        y = fn(x)
        ax_f.plot(x.detach().numpy(), y.detach().numpy(), label=name)

        grad = torch.autograd.grad(y.sum(), x, retain_graph=True)[0]
        ax_d.plot(x.detach().numpy(), grad.numpy(), label=f"{name}'")

    ax_f.set_title("activation functions")
    ax_f.set_xlabel("x")
    ax_f.set_ylabel("f(x)")
    ax_f.legend()

    ax_d.set_title("their derivatives")
    ax_d.set_xlabel("x")
    ax_d.set_ylabel("f'(x)")
    ax_d.legend()

    fig.suptitle("01 — ReLU, GELU, SiLU and their gradients")
    return save(fig, "01_activations")


def _fig_loss_surface():
    style()
    torch.manual_seed(0)
    n = 40
    x = torch.linspace(-3, 3, n)
    w_true, b_true = 2.0, -1.0
    y = w_true * x + b_true + 0.3 * torch.randn(n)

    def loss_fn(w: float, b: float) -> float:
        pred = w * x + b
        return ((pred - y) ** 2).mean().item()

    w_grid = np.linspace(-1, 5, 120)
    b_grid = np.linspace(-4, 2, 120)
    ww, bb = np.meshgrid(w_grid, b_grid)
    zz = np.vectorize(loss_fn)(ww, bb)

    fig, ax = plt.subplots(figsize=(7, 6))
    contour = ax.contour(ww, bb, zz, levels=12, cmap="viridis")
    ax.clabel(contour, inline=True, fontsize=6)

    bound = 20.0  # stop a diverging path once it leaves the region worth plotting
    for lr, color in [(0.02, "#1f77b4"), (0.1, "#2ca02c"), (0.5, "#d62728")]:
        w, b = torch.tensor(0.0, requires_grad=True), torch.tensor(0.0, requires_grad=True)
        path_w, path_b = [w.item()], [b.item()]
        diverged = False
        for _ in range(40):
            pred = w * x + b
            loss = ((pred - y) ** 2).mean()
            w.grad = None
            b.grad = None
            loss.backward()
            with torch.no_grad():
                w -= lr * w.grad
                b -= lr * b.grad
            path_w.append(w.item())
            path_b.append(b.item())
            if abs(path_w[-1]) > bound or abs(path_b[-1]) > bound:
                diverged = True
                break
        label = f"lr={lr}" + (" (diverges)" if diverged else "")
        ax.plot(path_w, path_b, "-o", color=color, markersize=2, linewidth=1, label=label)

    ax.plot(w_true, b_true, "k*", markersize=14, label="true (w, b)")
    ax.set_xlim(w_grid.min(), w_grid.max())
    ax.set_ylim(b_grid.min(), b_grid.max())
    ax.set_xlabel("w")
    ax.set_ylabel("b")
    ax.set_title("01 — MSE loss surface and gradient-descent paths")
    ax.legend(fontsize=8)
    return save(fig, "01_loss_surface")


def _fig_moons_training(result: dict):
    style()
    steps = sorted(result["snapshots"].keys())
    fig, axes = plt.subplots(1, len(steps), figsize=(4 * len(steps), 4.2))
    x_np, y_np = result["x"], result["y"]
    xx, yy = result["xx"], result["yy"]

    for ax, step in zip(axes, steps):
        probs = result["snapshots"][step]
        ax.contourf(xx, yy, probs, levels=20, cmap="RdBu_r", alpha=0.6, vmin=0, vmax=1)
        ax.scatter(x_np[:, 0], x_np[:, 1], c=y_np, cmap="RdBu_r", edgecolor="k", s=12)
        ax.set_title(f"step {step}")
        ax.set_xlabel("x1")
        ax.set_ylabel("x2")

    fig.suptitle("01 — decision boundary learning the two-moons dataset")
    return save(fig, "01_moons_training")


def _fig_loss_curve(result: dict):
    style()
    losses = result["losses"]
    fig, ax = plt.subplots()
    ax.plot(range(1, len(losses) + 1), losses, color="#1f77b4")
    ax.set_yscale("log")
    ax.set_xlabel("step")
    ax.set_ylabel("loss (log scale)")
    ax.set_title("01 — training loss vs step")

    plateau_step = max(5, len(losses) // 15)
    steep_step = len(losses) // 3
    annotate_arrow(
        ax,
        "plateau: gradients ~0 at the start",
        xy=(plateau_step, losses[plateau_step - 1]),
        xytext=(plateau_step + len(losses) * 0.2, losses[plateau_step - 1] * 1.5),
    )
    annotate_arrow(
        ax,
        "steep phase: loss drops fast",
        xy=(steep_step, losses[steep_step - 1]),
        xytext=(steep_step + len(losses) * 0.15, losses[steep_step - 1] * 2.5),
    )
    return save(fig, "01_loss_curve")


def _fig_matmul_picture():
    style()
    fig, (ax_pic, ax_text) = plt.subplots(1, 2, figsize=(11, 4.5), gridspec_kw={"width_ratios": [1.2, 1]})

    x_vals = [0.5, -1.0, 2.0, 0.0]
    w_vals = [[0.1, 0.2, -0.3], [0.4, -0.1, 0.5], [-0.2, 0.3, 0.1], [0.0, 0.5, -0.4]]

    cell = 0.8
    for i, v in enumerate(x_vals):
        rect = plt.Rectangle((i * cell, 2 * cell), cell, cell, facecolor="#1f77b4", alpha=0.5, edgecolor="k")
        ax_pic.add_patch(rect)
        ax_pic.text(i * cell + cell / 2, 2 * cell + cell / 2, f"{v}", ha="center", va="center")
    ax_pic.text(-0.6, 2 * cell + cell / 2, "x (1x4)", ha="right", va="center")

    for r in range(4):
        for c in range(3):
            rect = plt.Rectangle((c * cell, (0.7 - r) * cell), cell, cell, facecolor="#2ca02c", alpha=0.4, edgecolor="k")
            ax_pic.add_patch(rect)
            ax_pic.text(c * cell + cell / 2, (0.7 - r) * cell + cell / 2, f"{w_vals[r][c]}", ha="center", va="center", fontsize=8)
    ax_pic.text(-0.6, (0.7 - 1.5) * cell, "W (4x3)", ha="right", va="center")

    out_col0 = sum(x_vals[r] * w_vals[r][0] for r in range(4))
    rect = plt.Rectangle((0, -3.3 * cell), cell, cell, facecolor="#d62728", alpha=0.5, edgecolor="k")
    ax_pic.add_patch(rect)
    ax_pic.text(cell / 2, -3.3 * cell + cell / 2, f"{out_col0:.2f}", ha="center", va="center")
    ax_pic.text(-0.6, -3.3 * cell + cell / 2, "x@W (1x3)", ha="right", va="center")

    ax_pic.set_xlim(-2.2, 3.2)
    ax_pic.set_ylim(-3.6, 3.2)
    ax_pic.axis("off")
    ax_pic.set_title("x (1x4) . W (4x3) -> one row of output")

    terms = " + ".join(f"{x_vals[r]}*{w_vals[r][0]}" for r in range(4))
    ax_text.axis("off")
    ax_text.text(
        0.0,
        0.6,
        f"output[0,0] = {terms}\n            = {out_col0:.3f}",
        fontsize=11,
        family="monospace",
        va="center",
    )
    ax_text.text(
        0.0,
        0.2,
        "Every output cell is one dot product between a row of x\nand a column of W: a layer is just many dot products\ndone at once.",
        fontsize=10,
        va="center",
    )
    return save(fig, "01_matmul_picture")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


@app.command()
def plots() -> None:
    """Regenerate every figure for this chapter."""
    print(f"wrote: {_fig_activations()}")
    print(f"wrote: {_fig_loss_surface()}")

    cfg = TrainConfig()
    result = train_toy(cfg)
    print(f"wrote: {_fig_moons_training(result)}")
    print(f"wrote: {_fig_loss_curve(result)}")
    print(f"wrote: {_fig_matmul_picture()}")


@app.command()
def demo() -> None:
    """Print the parameter counts and final accuracy quoted in the chapter."""
    model = MLP2(in_features=2, hidden=16, out_features=1)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"MLP2(2 -> 16 -> 1) parameters: {n_params}")
    print(f"  fc1 (Linear 2->16): {sum(p.numel() for p in model.fc1.parameters())}")
    print(f"  fc2 (Linear 16->1): {sum(p.numel() for p in model.fc2.parameters())}")

    result = train_toy(TrainConfig())
    print(f"two-moons final train accuracy after 300 steps: {result['accuracy']:.3f}")
    print(f"final loss: {result['losses'][-1]:.4f}")


if __name__ == "__main__":
    app()
