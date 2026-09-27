"""Chapter 06 — the MLP block (SwiGLU) and Mixture of Experts (MoE).

`uv run python -m llm_blocks.ch06_mlp_moe plots` draws the six figures for this chapter
(config download only for the parameter-breakdown and cost figures, no model weights);
`demo` prints the parameter table quoted in the chapter.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn.functional as F
import typer
from torch import Tensor, nn

from llm_blocks.plotting import save, style

app = typer.Typer(add_completion=False, no_args_is_help=False)


# ---------------------------------------------------------------------------
# 1. SwiGLU MLP
# ---------------------------------------------------------------------------


class SwiGLUMLP(nn.Module):
    """The feed-forward block used by Qwen3 / Qwen3.5 / Qwen3.8: `down(silu(gate(x)) * up(x))`.

    Three matrices instead of the classic two (`down(act(fc1(x)))`): `gate` and `up` both
    read the full input, `silu(gate(x))` acts as a per-element "volume knob" on `up(x)`
    (0 = mute that feature, 1 = pass it through unchanged), and `down` projects back to
    `d_model`. No biases, matching `transformers.models.qwen3.modeling_qwen3.Qwen3MLP`.
    """

    def __init__(self, d_model: int, d_ff: int) -> None:
        super().__init__()
        self.gate_proj = nn.Linear(d_model, d_ff, bias=False)
        self.up_proj = nn.Linear(d_model, d_ff, bias=False)
        self.down_proj = nn.Linear(d_ff, d_model, bias=False)

    def forward(self, x: Tensor) -> Tensor:
        return self.down_proj(F.silu(self.gate_proj(x)) * self.up_proj(x))


# ---------------------------------------------------------------------------
# 2. Key-value memory demo
# ---------------------------------------------------------------------------


@dataclass
class KeyValueMemoryDemo:
    """A tiny lookup task: 50 "keys" (random vectors) each map to their own "value" (random
    vector). Fitting a 1-hidden-layer MLP on this task is a minimal illustration of Geva et
    al. (2021)'s "key-value memory" reading of a feed-forward layer: the first matrix's rows
    act as pattern detectors ("keys") that fire for specific inputs, and the second matrix's
    columns act as the "values" retrieved once a key fires.
    """

    n_keys: int = 50
    d_model: int = 16
    d_hidden: int = 64
    seed: int = 0

    keys: Tensor = field(init=False, repr=False)
    values: Tensor = field(init=False, repr=False)
    model: nn.Sequential = field(init=False, repr=False)

    def __post_init__(self) -> None:
        torch.manual_seed(self.seed)
        self.keys = F.normalize(torch.randn(self.n_keys, self.d_model), dim=-1)
        self.values = torch.randn(self.n_keys, self.d_model)
        self.model = nn.Sequential(
            nn.Linear(self.d_model, self.d_hidden),
            nn.ReLU(),
            nn.Linear(self.d_hidden, self.d_model),
        )

    def train(self, steps: int = 800, lr: float = 0.05) -> list[float]:
        """Fit the MLP to map every key to its value with plain Adam + MSE loss."""
        opt = torch.optim.Adam(self.model.parameters(), lr=lr)
        losses = []
        for _ in range(steps):
            pred = self.model(self.keys)
            loss = F.mse_loss(pred, self.values)
            opt.zero_grad()
            loss.backward()
            opt.step()
            losses.append(loss.item())
        return losses

    def firing_matrix(self) -> Tensor:
        """Post-ReLU hidden activations for every key: shape `(n_keys, d_hidden)`.

        Each row is one key's "which neurons fired" pattern; each column is one hidden
        neuron's "which keys make it fire" pattern — the key-detector reading of the block.
        """
        with torch.no_grad():
            hidden = self.model[1](self.model[0](self.keys))
        return hidden


# ---------------------------------------------------------------------------
# 3. Mixture of Experts: router, layer, load-balancing loss
# ---------------------------------------------------------------------------


class TopKRouter(nn.Module):
    """Score every expert for every token, then keep only the top `k`.

    `softmax` turns the raw scores into a probability distribution over experts (so they
    are comparable and sum to 1); `topk` keeps only the `k` largest, and the kept weights
    are renormalised to sum to 1 again so the expert outputs are combined as a proper
    weighted average (matches `norm_topk_prob=True` in
    `transformers.models.qwen3_moe.modeling_qwen3_moe.Qwen3MoeTopKRouter`).
    """

    def __init__(self, d_model: int, n_experts: int, k: int) -> None:
        super().__init__()
        self.n_experts = n_experts
        self.k = k
        self.weight = nn.Linear(d_model, n_experts, bias=False)

    def forward(self, x: Tensor) -> tuple[Tensor, Tensor, Tensor]:
        """`x`: `(n_tokens, d_model)`. Returns `(router_probs, topk_weights, topk_indices)`,
        all `(n_tokens, ...)` — `router_probs` keeps every expert's probability (needed by
        `load_balancing_loss`); `topk_weights`/`topk_indices` are `(n_tokens, k)`."""
        router_logits = self.weight(x)
        router_probs = F.softmax(router_logits, dim=-1)
        topk_weights, topk_indices = torch.topk(router_probs, self.k, dim=-1)
        topk_weights = topk_weights / topk_weights.sum(dim=-1, keepdim=True)
        return router_probs, topk_weights, topk_indices


class MoELayer(nn.Module):
    """`n_experts` independent `SwiGLUMLP`s, a `TopKRouter` picking `k` of them per token, and
    an optional always-on "shared expert" that every token also goes through (as in
    Qwen3-MoE / Qwen3.8-MoE) so some general-purpose computation does not have to compete
    for router slots.
    """

    def __init__(self, d_model: int, d_ff: int, n_experts: int, k: int, shared_expert: bool = True) -> None:
        super().__init__()
        self.n_experts = n_experts
        self.k = k
        self.router = TopKRouter(d_model, n_experts, k)
        self.experts = nn.ModuleList([SwiGLUMLP(d_model, d_ff) for _ in range(n_experts)])
        self.shared_expert = SwiGLUMLP(d_model, d_ff) if shared_expert else None

    def forward(self, x: Tensor) -> tuple[Tensor, Tensor, Tensor]:
        """`x`: `(..., d_model)`. Returns `(output, router_probs, topk_indices)` — the latter
        two flattened to `(n_tokens, ...)` so the caller can feed them to
        `load_balancing_loss`."""
        shape = x.shape
        x_flat = x.reshape(-1, shape[-1])
        router_probs, topk_weights, topk_indices = self.router(x_flat)

        out = torch.zeros_like(x_flat)
        for expert_idx, expert in enumerate(self.experts):
            slot_mask = topk_indices == expert_idx  # (n_tokens, k)
            token_mask = slot_mask.any(dim=-1)
            if not token_mask.any():
                continue
            weight = (topk_weights * slot_mask).sum(dim=-1, keepdim=True)[token_mask]
            out[token_mask] += weight * expert(x_flat[token_mask])

        if self.shared_expert is not None:
            out = out + self.shared_expert(x_flat)

        return out.reshape(shape), router_probs, topk_indices


def load_balancing_loss(router_probs: Tensor, expert_indices: Tensor, n_experts: int) -> Tensor:
    """Switch-Transformer-style auxiliary loss: `n_experts * sum_e f_e * P_e`.

    `f_e` = fraction of (token, top-k slot) pairs assigned to expert `e`; `P_e` = that
    expert's average router probability over all tokens. Both are minimised together only
    when every expert gets both an equal *share of tokens* and an equal *average score* —
    at the uniform optimum `f_e = P_e = 1/n_experts` for every `e`, the loss reaches its
    minimum value of 1. `f_e` is computed from a hard `one_hot` (not differentiable through
    the routing *choice*), so this loss only pushes gradients through the router's
    *scores*, not through which experts get picked.
    """
    n_tokens, k = expert_indices.shape
    avg_prob = router_probs.mean(dim=0)
    one_hot = F.one_hot(expert_indices, num_classes=n_experts).float()
    assignment_frac = one_hot.sum(dim=(0, 1)) / (n_tokens * k)
    return n_experts * (assignment_frac * avg_prob).sum()


# ---------------------------------------------------------------------------
# 4. Toy MoE training: expert collapse vs balanced usage
# ---------------------------------------------------------------------------


@dataclass
class MoeToyTrainConfig:
    d_model: int = 16
    d_ff: int = 32
    n_experts: int = 8
    k: int = 2
    n_tokens: int = 4096
    steps: int = 600
    lr: float = 0.02
    balance_weight: float = 0.05
    seed: int = 0


def train_toy_moe(cfg: MoeToyTrainConfig, use_balancing_loss: bool) -> Tensor:
    """Train a small `MoELayer` (no shared expert, so every token depends entirely on which
    experts the router picks) on a fixed random regression task, with or without
    `load_balancing_loss` added to the training loss. Returns the expert-usage histogram
    (length `n_experts`, counts summed over all `(token, slot)` assignments) measured on a
    fresh evaluation batch after training.
    """
    torch.manual_seed(cfg.seed)
    target_map = torch.randn(cfg.d_model, cfg.d_model) / cfg.d_model**0.5

    layer = MoELayer(cfg.d_model, cfg.d_ff, cfg.n_experts, cfg.k, shared_expert=False)
    opt = torch.optim.Adam(layer.parameters(), lr=cfg.lr)

    for _ in range(cfg.steps):
        x = torch.randn(cfg.n_tokens, cfg.d_model)
        y = x @ target_map.T
        out, router_probs, topk_indices = layer(x)
        loss = F.mse_loss(out, y)
        if use_balancing_loss:
            loss = loss + cfg.balance_weight * load_balancing_loss(router_probs, topk_indices, cfg.n_experts)
        opt.zero_grad()
        loss.backward()
        opt.step()

    torch.manual_seed(cfg.seed + 1)
    x_eval = torch.randn(cfg.n_tokens, cfg.d_model)
    with torch.no_grad():
        _, _, topk_indices = layer(x_eval)
    usage = torch.bincount(topk_indices.reshape(-1), minlength=cfg.n_experts)
    return usage


# ---------------------------------------------------------------------------
# 5. Parameter breakdown for a real text config
# ---------------------------------------------------------------------------

QWEN38_27B_ID = "Qwen/Qwen3.8-27B"
QWEN35_08B_ID = "Qwen/Qwen3.5-0.8B"

_BUCKET_PATTERNS = [
    ("embeddings", re.compile(r"embed_tokens")),
    ("lm_head", re.compile(r"^lm_head")),
    ("norms", re.compile(r"norm")),  # checked after linear_attn/self_attn/mlp below
    ("deltanet", re.compile(r"linear_attn")),
    ("attention", re.compile(r"self_attn")),
    ("mlp", re.compile(r"\.mlp\.")),
]


def param_breakdown(config) -> dict[str, int]:
    """Parameter count per block type for a text config, without allocating any real
    memory: `AutoModelForCausalLM.from_config` on the `"meta"` device builds the module
    tree (every `nn.Parameter` has a shape but no storage) so `numel()` is exact and instant
    even for a 27B-parameter config.
    """
    from transformers import AutoModelForCausalLM

    with torch.device("meta"):
        model = AutoModelForCausalLM.from_config(config)

    buckets = {"embeddings": 0, "attention": 0, "deltanet": 0, "mlp": 0, "norms": 0, "lm_head": 0, "other": 0}
    for name, p in model.named_parameters():
        n = p.numel()
        if "embed_tokens" in name:
            buckets["embeddings"] += n
        elif name.startswith("lm_head"):
            buckets["lm_head"] += n
        elif "linear_attn" in name:
            buckets["norms" if "norm" in name else "deltanet"] += n
        elif "self_attn" in name:
            buckets["norms" if "norm" in name else "attention"] += n
        elif ".mlp." in name:
            buckets["mlp"] += n
        elif "norm" in name:
            buckets["norms"] += n
        else:
            buckets["other"] += n
    return buckets


def load_text_config(model_id: str):
    """`AutoConfig.from_pretrained(model_id).get_text_config()` — config download only, no
    weights. Falls back to `Qwen/Qwen3.5-0.8B` if the network is unavailable.
    """
    from transformers import AutoConfig

    try:
        config = AutoConfig.from_pretrained(model_id)
    except OSError:
        config = AutoConfig.from_pretrained(QWEN35_08B_ID)
    return config.get_text_config() if hasattr(config, "get_text_config") else config


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------


def _fig_swiglu_schematic() -> str:
    style()
    fig, ax = plt.subplots(figsize=(11, 4.6))

    def box(x, y, w, h, label, color):
        ax.add_patch(plt.Rectangle((x, y), w, h, facecolor=color, edgecolor="k", alpha=0.85))
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=9)

    box(0.0, 1.0, 1.4, 0.9, "x\n(5120)", "#cccccc")
    box(2.2, 1.9, 1.6, 0.9, "gate_proj\n5120 -> 17408", "#1f77b4")
    box(2.2, 0.1, 1.6, 0.9, "up_proj\n5120 -> 17408", "#ff7f0e")
    box(4.4, 1.9, 1.4, 0.9, "SiLU\n(17408)", "#1f77b4")
    box(6.3, 1.0, 1.6, 0.9, "elementwise *\n(17408)", "#9467bd")
    box(8.4, 1.0, 1.8, 0.9, "down_proj\n17408 -> 5120", "#2ca02c")
    box(10.7, 1.0, 1.4, 0.9, "out\n(5120)", "#cccccc")

    for (x0, y0), (x1, y1) in [
        ((1.4, 1.45), (2.2, 2.35)),
        ((1.4, 1.45), (2.2, 0.55)),
        ((3.8, 2.35), (4.4, 2.35)),
        ((5.8, 2.35), (6.3, 1.65)),
        ((3.8, 0.55), (6.3, 1.25)),
        ((7.9, 1.45), (8.4, 1.45)),
        ((10.2, 1.45), (10.7, 1.45)),
    ]:
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops={"arrowstyle": "-|>", "color": "gray", "lw": 1.4})

    ax.set_xlim(-0.3, 12.3)
    ax.set_ylim(-0.2, 3.2)
    ax.axis("off")
    ax.set_title("SwiGLU MLP, Qwen3.8-27B shapes: down(silu(gate(x)) * up(x))\n"
                 "hidden 5120 -> intermediate 17408 (~3.4x) -> hidden 5120, three matrices, no bias")
    return str(save(fig, "06_swiglu_schematic"))


def _fig_gate_behaviour() -> str:
    style()
    x = torch.linspace(-4, 4, 400)
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.4))

    for gate_val, color in [(-3.0, "#d62728"), (0.0, "#7f7f7f"), (3.0, "#1f77b4")]:
        gate = torch.full_like(x, gate_val)
        knob = F.silu(gate)
        axes[0].plot(x.numpy(), (knob * x).numpy(), color=color, label=f"gate={gate_val:g}  (silu={knob[0]:.2f})")
    axes[0].plot(x.numpy(), x.numpy(), "k--", lw=0.8, label="up(x) itself")
    axes[0].set_xlabel("up(x)")
    axes[0].set_ylabel("silu(gate(x)) * up(x)")
    axes[0].set_title("The gate as a volume knob:\nsame up(x), three fixed gate values")
    axes[0].legend(fontsize=8)

    gate_grid, up_grid = torch.meshgrid(torch.linspace(-4, 4, 120), torch.linspace(-4, 4, 120), indexing="xy")
    surface = (F.silu(gate_grid) * up_grid).numpy()
    im = axes[1].imshow(surface, extent=(-4, 4, -4, 4), origin="lower", cmap="RdBu_r", vmin=-4, vmax=4)
    axes[1].set_xlabel("gate(x)")
    axes[1].set_ylabel("up(x)")
    axes[1].set_title("silu(gate) * up over both inputs\n(blue/red = output sign, white = muted)")
    fig.colorbar(im, ax=axes[1], shrink=0.85)

    fig.suptitle("SiLU-gated linear unit: the gate scales up(x) from ~0 (muted) to ~up(x) (passed through)")
    fig.tight_layout()
    return str(save(fig, "06_gate_behaviour"))


def _fig_kv_memory() -> str:
    style()
    demo = KeyValueMemoryDemo()
    demo.train()
    firing = demo.firing_matrix().numpy()

    fig, ax = plt.subplots(figsize=(10, 6))
    im = ax.imshow(firing, aspect="auto", cmap="viridis")
    ax.set_xlabel("hidden neuron (64)")
    ax.set_ylabel("input key (50)")
    ax.set_title("Key-value memory: which hidden neurons fire for which key\n"
                 "(post-ReLU activation; sparse, selective firing per key)")
    fig.colorbar(im, ax=ax, label="activation", shrink=0.85)
    return str(save(fig, "06_kv_memory"))


def _fig_param_pie() -> str:
    style()
    configs = [("Qwen3.8-27B (dense)", QWEN38_27B_ID), ("Qwen3.5-0.8B", QWEN35_08B_ID)]
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.4))

    for ax, (title, model_id) in zip(axes, configs):
        breakdown = param_breakdown(load_text_config(model_id))
        labels = [k for k, v in breakdown.items() if v > 0]
        sizes = [v for v in breakdown.values() if v > 0]
        total = sum(sizes)
        ax.pie(sizes, labels=[f"{lb}\n{sz / total:.0%}" for lb, sz in zip(labels, sizes)], startangle=90)
        ax.set_title(f"{title}\ntotal = {total:,} params")

    fig.suptitle("Where the parameters live: MLP dominates a dense model,\n"
                 "attention/DeltaNet and embeddings are the rest")
    fig.tight_layout()
    return str(save(fig, "06_param_pie"))


def _fig_moe_schematic() -> str:
    style()
    fig, ax = plt.subplots(figsize=(11, 5.4))

    ax.add_patch(plt.Rectangle((0.2, 4.2), 1.6, 0.9, facecolor="#cccccc", edgecolor="k"))
    ax.text(1.0, 4.65, "token x", ha="center", va="center", fontsize=9)
    ax.add_patch(plt.Rectangle((3.0, 4.2), 1.8, 0.9, facecolor="#9467bd", edgecolor="k"))
    ax.text(3.9, 4.65, "router\n(top-2 of 8)", ha="center", va="center", fontsize=9)
    ax.annotate("", xy=(3.0, 4.65), xytext=(1.8, 4.65), arrowprops={"arrowstyle": "-|>", "color": "gray", "lw": 1.4})

    n_experts = 8
    chosen = {2, 5}
    xs = np.linspace(0.6, 10.6, n_experts)
    for i, x in enumerate(xs):
        color = "#1f77b4" if i in chosen else "#dddddd"
        ax.add_patch(plt.Rectangle((x - 0.5, 2.0), 1.0, 0.9, facecolor=color, edgecolor="k"))
        ax.text(x, 2.45, f"expert {i}", ha="center", va="center", fontsize=7.5)
        style_arrow = {"arrowstyle": "-|>", "color": "#1f77b4" if i in chosen else "#dddddd", "lw": 1.6 if i in chosen else 0.8}
        ax.annotate("", xy=(x, 2.9), xytext=(3.9, 4.2), arrowprops=style_arrow)

    ax.add_patch(plt.Rectangle((9.6, 4.2), 2.0, 0.9, facecolor="#ff7f0e", edgecolor="k"))
    ax.text(10.6, 4.65, "shared expert\n(always on)", ha="center", va="center", fontsize=8)
    ax.annotate("", xy=(10.6, 4.2), xytext=(10.6, 2.9), arrowprops={"arrowstyle": "-", "color": "#ff7f0e", "lw": 1.6})

    ax.add_patch(plt.Rectangle((4.8, 0.2), 1.8, 0.9, facecolor="#2ca02c", edgecolor="k"))
    ax.text(5.7, 0.65, "weighted sum\n+ shared expert", ha="center", va="center", fontsize=8)
    for x in [xs[i] for i in chosen] + [10.6]:
        color = "#1f77b4" if x != 10.6 else "#ff7f0e"
        ax.annotate("", xy=(5.7, 1.1), xytext=(x, 2.0), arrowprops={"arrowstyle": "-|>", "color": color, "lw": 1.4})

    ax.set_xlim(-0.3, 12.0)
    ax.set_ylim(-0.3, 5.5)
    ax.axis("off")
    ax.set_title("Mixture of Experts: a router picks top-2 of 8 experts per token,\n"
                 "plus an always-on shared expert (Qwen3-MoE / Qwen3.8-MoE style)")
    return str(save(fig, "06_moe_schematic"))


def _fig_expert_usage() -> str:
    style()
    cfg = MoeToyTrainConfig()
    usage_collapsed = train_toy_moe(cfg, use_balancing_loss=False)
    usage_balanced = train_toy_moe(cfg, use_balancing_loss=True)

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6), sharey=True)
    experts = np.arange(cfg.n_experts)
    axes[0].bar(experts, usage_collapsed.numpy(), color="#d62728")
    axes[0].set_title("Without load-balancing loss:\nusage collapses onto a few experts")
    axes[1].bar(experts, usage_balanced.numpy(), color="#1f77b4")
    axes[1].set_title("With load-balancing loss:\nusage spreads across all experts")
    for ax in axes:
        ax.set_xlabel("expert index")
        ax.axhline(cfg.n_tokens * cfg.k / cfg.n_experts, color="k", ls="--", lw=0.8, label="perfectly balanced")
        ax.legend(fontsize=8)
    axes[0].set_ylabel(f"tokens routed to this expert (of {cfg.n_tokens} tokens, top-{cfg.k})")
    fig.suptitle(f"Expert usage after {cfg.steps} toy training steps, {cfg.n_experts} experts, top-{cfg.k}")
    fig.tight_layout()
    return str(save(fig, "06_expert_usage"))


def _fig_moe_cost() -> str:
    style()
    dense_total = sum(param_breakdown(load_text_config(QWEN38_27B_ID)).values())
    # Qwen3.8-2.4T-A95B, as reported on the model card: 2.4T total, 95B active.
    moe_total, moe_active = 2.4e12, 95e9

    fig, ax = plt.subplots(figsize=(8.6, 5.0))
    labels = ["Qwen3.8-27B\n(dense)", "Qwen3.8-2.4T-A95B\n(MoE, reported)"]
    totals = [dense_total, moe_total]
    actives = [dense_total, moe_active]
    x = np.arange(2)
    width = 0.35
    ax.bar(x - width / 2, totals, width, label="total params (stored)", color="#9467bd")
    ax.bar(x + width / 2, actives, width, label="active params (compute per token)", color="#1f77b4")
    ax.set_yscale("log")
    ax.set_xticks(x, labels)
    ax.set_ylabel("parameters (log scale)")
    ax.set_title("MoE is cheap to run (active params) but expensive to store (total params)\n"
                 "single-GPU: the 27B dense model fits, the MoE's total size does not")
    ax.legend()
    return str(save(fig, "06_moe_cost"))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


@app.command()
def plots() -> None:
    """Regenerate every figure for this chapter (config download only, no MoE weights)."""
    print(f"wrote: {_fig_swiglu_schematic()}")
    print(f"wrote: {_fig_gate_behaviour()}")
    print(f"wrote: {_fig_kv_memory()}")
    print(f"wrote: {_fig_param_pie()}")
    print(f"wrote: {_fig_moe_schematic()}")
    print(f"wrote: {_fig_expert_usage()}")
    print(f"wrote: {_fig_moe_cost()}")


@app.command()
def demo() -> None:
    """Print the parameter breakdown table quoted in the chapter."""
    for title, model_id in [("Qwen3.8-27B (dense)", QWEN38_27B_ID), ("Qwen3.5-0.8B", QWEN35_08B_ID)]:
        breakdown = param_breakdown(load_text_config(model_id))
        total = sum(breakdown.values())
        print(f"\n{title}: total = {total:,} params")
        for k, v in breakdown.items():
            if v > 0:
                print(f"  {k:>12}: {v:>15,}  ({v / total:.1%})")


if __name__ == "__main__":
    app()
