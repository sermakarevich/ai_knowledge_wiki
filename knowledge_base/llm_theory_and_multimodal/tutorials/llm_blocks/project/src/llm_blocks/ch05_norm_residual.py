"""Chapter 05 — normalization and the residual stream.

`uv run python -m llm_blocks.ch05_norm_residual plots` draws the five figures for this
chapter (no downloads); `demo` prints the depth-stats numbers and the no-norm training
comparison quoted in the chapter.
"""

from __future__ import annotations

from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import torch
import typer
from sklearn.datasets import make_moons
from torch import Tensor, nn

from llm_blocks.plotting import save, style

app = typer.Typer(add_completion=False, no_args_is_help=False)


# ---------------------------------------------------------------------------
# 1. LayerNorm and RMSNorm from scratch
# ---------------------------------------------------------------------------


class LayerNorm(nn.Module):
    """Re-centre (subtract the mean) and re-scale (divide by the std), per token.

    Matches `torch.nn.LayerNorm(dim, eps=eps)`: statistics are computed over the last
    dimension only, in the input's own dtype (no forced fp32 upcast, unlike RMSNorm below).
    """

    def __init__(self, dim: int, eps: float = 1e-5) -> None:
        super().__init__()
        self.weight = nn.Parameter(torch.ones(dim))
        self.bias = nn.Parameter(torch.zeros(dim))
        self.eps = eps

    def forward(self, x: Tensor) -> Tensor:
        mean = x.mean(dim=-1, keepdim=True)
        var = x.var(dim=-1, keepdim=True, unbiased=False)
        x_norm = (x - mean) / torch.sqrt(var + self.eps)
        return x_norm * self.weight + self.bias


class RMSNorm(nn.Module):
    """Root-mean-square norm: re-scale only, no re-centring, no bias.

        RMSNorm(x) = x / sqrt(mean(x^2) + eps) * weight            (Qwen3 / Llama)
        RMSNorm(x) = x / sqrt(mean(x^2) + eps) * (1 + weight)      (Qwen3.5)

    Both variants compute the mean-square and the rsqrt in float32 even if `x` is bf16
    (`transformers.models.qwen3.modeling_qwen3.Qwen3RMSNorm` and
    `transformers.models.qwen3_5.modeling_qwen3_5.Qwen3_5RMSNorm`, transformers 5.16), then
    cast back to `x`'s dtype — the squared values in `mean(x^2)` lose too much precision in
    bf16 otherwise. The two differ only in how the learnable scale is parameterised: Qwen3
    (dense) initialises `weight` to ones and multiplies directly (`weight * x_norm`); Qwen3.5
    initialises `weight` to *zeros* and multiplies by `1 + weight`, so an untrained scale
    starts as the identity (`1 + 0 = 1`) and gradients see a scale centred at 0 — a
    parameterisation trick, not a mathematical difference in what a *trained* norm computes.
    """

    def __init__(self, dim: int, eps: float = 1e-6, qwen_variant: bool = False) -> None:
        super().__init__()
        self.eps = eps
        self.qwen_variant = qwen_variant
        self.weight = nn.Parameter(torch.zeros(dim) if qwen_variant else torch.ones(dim))

    def forward(self, x: Tensor) -> Tensor:
        input_dtype = x.dtype
        x = x.to(torch.float32)
        variance = x.pow(2).mean(dim=-1, keepdim=True)
        x_norm = x * torch.rsqrt(variance + self.eps)
        scale = (1.0 + self.weight.float()) if self.qwen_variant else self.weight.float()
        return (x_norm * scale).to(input_dtype)


# ---------------------------------------------------------------------------
# 2. Pre-norm vs post-norm block, and depth statistics
# ---------------------------------------------------------------------------


class TinyMLP(nn.Module):
    """A stand-in for "attention or MLP": one hidden layer, GELU, back to `dim`."""

    def __init__(self, dim: int, hidden_mult: int = 4) -> None:
        super().__init__()
        self.fc1 = nn.Linear(dim, dim * hidden_mult)
        self.fc2 = nn.Linear(dim * hidden_mult, dim)

    def forward(self, x: Tensor) -> Tensor:
        return self.fc2(nn.functional.gelu(self.fc1(x)))


class Block(nn.Module):
    """One residual block, in either convention.

        pre_norm=True:  x + f(norm(x))    (Qwen3/Qwen3.5, GPT-2 onward)
        pre_norm=False: norm(x + f(x))    (original transformer, "post-norm")

    `f` is a `TinyMLP`; `norm` is `RMSNorm`, `LayerNorm`, or `None` (identity — the "no norm"
    baseline used by `stack_stats`).
    """

    def __init__(self, dim: int, pre_norm: bool = True, norm: nn.Module | None = None) -> None:
        super().__init__()
        self.pre_norm = pre_norm
        self.f = TinyMLP(dim)
        self.norm = norm if norm is not None else nn.Identity()

    def forward(self, x: Tensor) -> Tensor:
        if self.pre_norm:
            return x + self.f(self.norm(x))
        return self.norm(x + self.f(x))


def _make_norm(dim: int, use_norm: bool) -> nn.Module | None:
    return RMSNorm(dim) if use_norm else None


def stack_stats(depth: int = 32, pre_norm: bool = True, use_norm: bool = True, dim: int = 64, seed: int = 0) -> dict:
    """Run one random input through `depth` stacked `Block`s and record, per layer:

    - activation std: `std(f(norm(x)))` or `std(f(x))` — the size of what this layer adds.
    - residual norm: `||x||` of the residual stream itself, right after this layer's add.
    - gradient norm at the input: backprop a dummy scalar loss (`x_out.sum()`) and record
      `||d loss / d x_input||` when the loss is defined using only the first `layer_idx + 1`
      blocks — i.e. how large a gradient signal would reach the *input* if the network were
      only that deep. This isolates each layer's individual contribution to vanishing or
      exploding gradients rather than mixing them into one end-to-end backward pass.
    """
    torch.manual_seed(seed)
    blocks = [Block(dim, pre_norm=pre_norm, norm=_make_norm(dim, use_norm)) for _ in range(depth)]

    x0 = torch.randn(8, dim)
    activation_std, residual_norm, gradient_norm = [], [], []

    x = x0
    for block in blocks:
        if block.pre_norm:
            f_out = block.f(block.norm(x))
        else:
            f_out = block.f(x)
        x = block(x)
        activation_std.append(f_out.std().item())
        residual_norm.append(x.norm(dim=-1).mean().item())

    for layer_idx in range(depth):
        x_in = x0.clone().requires_grad_(True)
        x = x_in
        for block in blocks[: layer_idx + 1]:
            x = block(x)
        loss = x.sum()
        (grad,) = torch.autograd.grad(loss, x_in)
        gradient_norm.append(grad.norm(dim=-1).mean().item())

    return {
        "activation_std": activation_std,
        "residual_norm": residual_norm,
        "gradient_norm": gradient_norm,
    }


# ---------------------------------------------------------------------------
# 3. No-norm training demo: 12-layer toy MLP stack on two-moons
# ---------------------------------------------------------------------------


@dataclass
class NoNormTrainConfig:
    dim: int = 16
    depth: int = 12
    lr: float = 0.18
    steps: int = 200
    seed: int = 0
    n_samples: int = 500
    noise: float = 0.2


class DeepStack(nn.Module):
    """`depth` pre-norm `Block`s (optionally normless) feeding a linear classifier head."""

    def __init__(self, in_features: int, dim: int, depth: int, use_norm: bool) -> None:
        super().__init__()
        self.embed = nn.Linear(in_features, dim)
        self.blocks = nn.ModuleList([Block(dim, pre_norm=True, norm=_make_norm(dim, use_norm)) for _ in range(depth)])
        self.head = nn.Linear(dim, 1)

    def forward(self, x: Tensor) -> Tensor:
        x = self.embed(x)
        for block in self.blocks:
            x = block(x)
        return self.head(x)


def train_deep_stack(cfg: NoNormTrainConfig, use_norm: bool) -> list[float]:
    """Train `DeepStack` on two-moons with plain SGD; return the loss at every step."""
    torch.manual_seed(cfg.seed)
    x_np, y_np = make_moons(n_samples=cfg.n_samples, noise=cfg.noise, random_state=cfg.seed)
    x = torch.tensor(x_np, dtype=torch.float32)
    y = torch.tensor(y_np, dtype=torch.float32).unsqueeze(1)

    model = DeepStack(in_features=2, dim=cfg.dim, depth=cfg.depth, use_norm=use_norm)
    losses = []
    for _ in range(cfg.steps):
        logits = model(x)
        loss = nn.functional.binary_cross_entropy_with_logits(logits, y)
        for p in model.parameters():
            p.grad = None
        loss.backward()
        with torch.no_grad():
            for p in model.parameters():
                if p.grad is not None and torch.isfinite(p.grad).all():
                    p -= cfg.lr * p.grad
        losses.append(loss.item())
    return losses


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------


def _fig_layernorm_vs_rmsnorm() -> str:
    style()
    torch.manual_seed(0)
    dim = 16
    x = torch.randn(dim) * 3.0 + 2.0  # off-centre, wide-spread to make both effects visible

    ln = LayerNorm(dim)
    rn = RMSNorm(dim)
    with torch.no_grad():
        y_ln = ln(x)
        y_rn = rn(x)

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6), sharey=False)
    idx = np.arange(dim)
    width = 0.35
    axes[0].bar(idx - width / 2, x.numpy(), width, label="before", color="#cccccc")
    axes[0].bar(idx + width / 2, y_ln.numpy(), width, label="after LayerNorm", color="#1f77b4")
    axes[0].axhline(0, color="k", lw=0.6)
    axes[0].set_title(f"LayerNorm: mean {x.mean():.2f} -> {y_ln.mean():.2f}, std {x.std():.2f} -> {y_ln.std():.2f}")
    axes[0].set_xlabel("dimension")
    axes[0].legend(fontsize=8)

    axes[1].bar(idx - width / 2, x.numpy(), width, label="before", color="#cccccc")
    axes[1].bar(idx + width / 2, y_rn.numpy(), width, label="after RMSNorm", color="#d62728")
    axes[1].axhline(0, color="k", lw=0.6)
    axes[1].set_title(f"RMSNorm: mean {x.mean():.2f} -> {y_rn.mean():.2f} (unchanged sign), "
                       f"rms {x.pow(2).mean().sqrt():.2f} -> {y_rn.pow(2).mean().sqrt():.2f}")
    axes[1].set_xlabel("dimension")
    axes[1].legend(fontsize=8)

    fig.suptitle("16-dim vector before/after LayerNorm vs RMSNorm\n"
                 "LayerNorm re-centres AND re-scales; RMSNorm only re-scales (no mean subtraction)")
    fig.tight_layout()
    return str(save(fig, "05_layernorm_vs_rmsnorm"))


def _fig_residual_highway() -> str:
    style()
    fig, ax = plt.subplots(figsize=(11, 4.0))

    y_stream = 0.0
    x_positions = [0, 2, 4, 6, 8, 10]
    ax.annotate("", xy=(x_positions[-1] + 0.6, y_stream), xytext=(x_positions[0] - 0.6, y_stream),
                arrowprops={"arrowstyle": "-|>", "color": "#1f77b4", "lw": 3})
    ax.text((x_positions[0] + x_positions[-1]) / 2, y_stream + 0.35, "residual stream (the highway)",
            ha="center", color="#1f77b4", fontsize=11, fontweight="bold")

    blocks = [("attention\n(layer 1)", x_positions[1]), ("MLP\n(layer 1)", x_positions[2]),
              ("attention\n(layer 2)", x_positions[3]), ("MLP\n(layer 2)", x_positions[4])]
    for label, xpos in blocks:
        box = plt.Rectangle((xpos - 0.55, y_stream + 0.6), 1.1, 0.9, facecolor="#ff7f0e", alpha=0.85, edgecolor="k")
        ax.add_patch(box)
        ax.text(xpos, y_stream + 1.05, label, ha="center", va="center", fontsize=8)
        ax.annotate("", xy=(xpos, y_stream + 0.6), xytext=(xpos, y_stream + 0.05),
                    arrowprops={"arrowstyle": "-|>", "color": "gray", "lw": 1.2})
        ax.annotate("", xy=(xpos + 0.15, y_stream + 0.02), xytext=(xpos + 0.15, y_stream + 0.6),
                    arrowprops={"arrowstyle": "-|>", "color": "#2ca02c", "lw": 1.6})

    ax.text(x_positions[-1] + 0.6, y_stream - 0.5, "on-ramp reads the highway,\ncomputes something, "
            "adds back on\n(green = written contribution)", fontsize=8, ha="right", color="#2ca02c")
    ax.set_xlim(x_positions[0] - 1.2, x_positions[-1] + 1.6)
    ax.set_ylim(-1.0, 2.0)
    ax.axis("off")
    ax.set_title("The residual stream as a highway: every block reads from it (gray) "
                 "and writes back onto it (green)")
    return str(save(fig, "05_residual_highway"))


def _fig_depth_stats() -> str:
    style()
    configs = [
        ("pre-norm", True, True, "#1f77b4"),
        ("post-norm", False, True, "#d62728"),
        ("no-norm", True, False, "#2ca02c"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(14.5, 4.6))
    titles = ["activation std |f(...)|", "residual-stream norm ||x||", "gradient norm at input"]
    keys = ["activation_std", "residual_norm", "gradient_norm"]

    for label, pre_norm, use_norm, color in configs:
        stats = stack_stats(depth=32, pre_norm=pre_norm, use_norm=use_norm)
        for ax, key in zip(axes, keys):
            ax.plot(range(1, len(stats[key]) + 1), stats[key], "-o", ms=3, color=color, label=label)

    for ax, title in zip(axes, titles):
        ax.set_yscale("log")
        ax.set_xlabel("layer index")
        ax.set_title(title)
        ax.legend(fontsize=8)
    fig.suptitle("32-layer stack, random input: no-norm grows fastest, pre-norm grows more slowly,\n"
                 "post-norm is pinned flat by its own final normalization at every layer (log-y)")
    fig.tight_layout()
    return str(save(fig, "05_depth_stats"))


def _fig_no_norm_training() -> str:
    style()
    cfg = NoNormTrainConfig()
    losses_norm = train_deep_stack(cfg, use_norm=True)
    losses_nonorm = train_deep_stack(cfg, use_norm=False)

    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    ax.plot(losses_norm, label="with RMSNorm", color="#1f77b4")
    ax.plot(losses_nonorm, label="no norm", color="#d62728")
    ax.set_yscale("log")
    ax.set_xlabel("step")
    ax.set_ylabel("BCE loss (log scale)")
    ax.set_title(f"{cfg.depth}-layer toy MLP stack on two-moons, lr={cfg.lr}: "
                 "without normalization the loss stalls or blows up")
    ax.legend()
    return str(save(fig, "05_no_norm_training"))


def _fig_residual_contributions() -> str:
    style()
    stats = stack_stats(depth=32, pre_norm=True, use_norm=True)
    contributions = np.array(stats["activation_std"])

    fig, ax = plt.subplots(figsize=(10, 4.6))
    ax.bar(range(1, len(contributions) + 1), contributions, color="#9467bd")
    ax.set_xlabel("layer index")
    ax.set_ylabel("std of this layer's contribution, std(f(norm(x)))")
    ax.set_title("Pre-norm stack: how much each layer adds to the residual stream\n"
                 "(every layer adds a similarly sized nudge — none dominates or vanishes)")
    return str(save(fig, "05_residual_contributions"))


# ---------------------------------------------------------------------------
# Real model configuration (see specs/COMMON.md)
# ---------------------------------------------------------------------------

QWEN35_NORM = {
    "rms_norm_eps": 1e-6,
    "hidden_size": 5120,
    "num_hidden_layers": 64,
}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


@app.command()
def plots() -> None:
    """Regenerate every figure for this chapter."""
    print(f"wrote: {_fig_layernorm_vs_rmsnorm()}")
    print(f"wrote: {_fig_residual_highway()}")
    print(f"wrote: {_fig_depth_stats()}")
    print(f"wrote: {_fig_no_norm_training()}")
    print(f"wrote: {_fig_residual_contributions()}")


@app.command()
def demo() -> None:
    """Print the depth-stats numbers and the no-norm training result quoted in the chapter."""
    for label, pre_norm, use_norm in [("pre-norm", True, True), ("post-norm", False, True), ("no-norm", True, False)]:
        stats = stack_stats(depth=32, pre_norm=pre_norm, use_norm=use_norm)
        print(f"{label:>10}: residual norm layer 1 = {stats['residual_norm'][0]:.3g}, "
              f"layer 32 = {stats['residual_norm'][-1]:.3g}, "
              f"gradient norm layer 1 = {stats['gradient_norm'][0]:.3g}, "
              f"layer 32 = {stats['gradient_norm'][-1]:.3g}")

    cfg = NoNormTrainConfig()
    losses_norm = train_deep_stack(cfg, use_norm=True)
    losses_nonorm = train_deep_stack(cfg, use_norm=False)
    print(f"\n{cfg.depth}-layer toy stack on two-moons, lr={cfg.lr}, {cfg.steps} steps:")
    print(f"  with RMSNorm: final loss = {losses_norm[-1]:.4f}")
    print(f"  no norm:      final loss = {losses_nonorm[-1]:.4f}")

    print("\nQwen3.5 normalization config values:")
    for k, v in QWEN35_NORM.items():
        print(f"  {k}: {v:,}")


if __name__ == "__main__":
    app()
