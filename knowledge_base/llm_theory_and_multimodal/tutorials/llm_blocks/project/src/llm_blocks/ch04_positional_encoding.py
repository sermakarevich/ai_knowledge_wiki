"""Chapter 04 — positional encoding: sinusoidal, RoPE, partial RoPE, context extension.

`uv run python -m llm_blocks.ch04_positional_encoding plots` draws the six figures for
this chapter (no downloads); `demo` prints the permutation-test result and the real config
values quoted in the chapter.

Shape convention: a single (query/key) tensor is `(..., T, D)` — any leading batch/head
dims, then time (tokens), then head dimension. `cos`/`sin` are `(T, D)` (or `(T, rotary_dim)`
for the partial variant) and broadcast against the trailing two dims of `x`.
"""

from __future__ import annotations

import math

import matplotlib.pyplot as plt
import numpy as np
import torch
import typer
from torch import Tensor

from llm_blocks.ch03_attention import scaled_dot_product_attention
from llm_blocks.plotting import save, style

app = typer.Typer(add_completion=False, no_args_is_help=False)


# ---------------------------------------------------------------------------
# 1. Sinusoidal positional encoding (Vaswani et al., 2017)
# ---------------------------------------------------------------------------


def sinusoidal_pe(seq: int, d: int) -> Tensor:
    """The original transformer's absolute position table, `(seq, d)`.

        PE(pos, 2i)   = sin(pos / 10000^(2i/d))
        PE(pos, 2i+1) = cos(pos / 10000^(2i/d))

    Even dimensions get a sine, odd dimensions the matching cosine, at `d/2` different
    frequencies. This table is added to the token embedding before the first layer.
    """
    position = torch.arange(seq).unsqueeze(1).float()  # (seq, 1)
    div_term = torch.exp(torch.arange(0, d, 2).float() * (-math.log(10000.0) / d))  # (d/2,)
    pe = torch.zeros(seq, d)
    pe[:, 0::2] = torch.sin(position * div_term)
    pe[:, 1::2] = torch.cos(position * div_term)
    return pe


# ---------------------------------------------------------------------------
# 2. RoPE (rotary position embedding) — rotate-half convention
# ---------------------------------------------------------------------------


def rope_cos_sin(seq: int, head_dim: int, theta: float = 10000.0) -> tuple[Tensor, Tensor]:
    """`(cos, sin)`, each `(seq, head_dim)`, for absolute positions `0..seq-1`.

    Matches `transformers.models.qwen3.modeling_qwen3.Qwen3RotaryEmbedding`: `head_dim/2`
    frequencies `1/theta^(2i/head_dim)`, each position's angle `pos * freq`, duplicated
    into the second half of the last dimension (`cat(freqs, freqs)`) so `cos`/`sin` are the
    same width as the vector they will rotate.
    """
    inv_freq = 1.0 / (theta ** (torch.arange(0, head_dim, 2).float() / head_dim))  # (head_dim/2,)
    positions = torch.arange(seq).float()
    freqs = torch.outer(positions, inv_freq)  # (seq, head_dim/2)
    emb = torch.cat([freqs, freqs], dim=-1)  # (seq, head_dim)
    return emb.cos(), emb.sin()


def rotate_half(x: Tensor) -> Tensor:
    """Split the last dim in half and swap-and-negate: `(x1, x2) -> (-x2, x1)`."""
    x1, x2 = x[..., : x.shape[-1] // 2], x[..., x.shape[-1] // 2 :]
    return torch.cat((-x2, x1), dim=-1)


def apply_rope(x: Tensor, cos: Tensor, sin: Tensor) -> Tensor:
    """Rotate `x` (`..., T, D`) by the angles in `cos`/`sin` (`T, D`).

    Exactly `transformers`' `apply_rotary_pos_emb` for one tensor: `x*cos + rotate_half(x)*sin`.
    Treating adjacent-and-opposite `(x_i, x_{i+d/2})` pairs as the real/imaginary parts of a
    complex number, this is multiplication by `e^{i * pos * freq}` — a rotation that leaves
    the pair's length unchanged and only turns its angle.
    """
    return x * cos + rotate_half(x) * sin


def partial_rope(x: Tensor, cos: Tensor, sin: Tensor, rotary_frac: float = 0.25) -> Tensor:
    """Rotate only the first `rotary_frac` of the head dimension; pass the rest through.

    `cos`/`sin` are already sized to the rotary slice (`rotary_dim = cos.shape[-1]`), the
    same convention `transformers.models.qwen3_5.modeling_qwen3_5.apply_rotary_pos_emb`
    uses: `rotary_dim` is baked into the rotary embedding module as
    `int(head_dim * partial_rotary_factor)`, not recomputed here. `rotary_frac` is kept as
    an argument only to assert the caller's `cos`/`sin` were built with the same fraction.
    """
    rotary_dim = cos.shape[-1]
    expected = int(x.shape[-1] * rotary_frac)
    if rotary_dim != expected:
        raise ValueError(f"cos/sin last dim {rotary_dim} does not match rotary_frac={rotary_frac} "
                          f"of head_dim={x.shape[-1]} (expected {expected})")
    x_rot, x_pass = x[..., :rotary_dim], x[..., rotary_dim:]
    x_rot = apply_rope(x_rot, cos, sin)
    return torch.cat([x_rot, x_pass], dim=-1)


# ---------------------------------------------------------------------------
# 3. Permutation test: attention alone is a set function; RoPE breaks that
# ---------------------------------------------------------------------------


def permutation_test(model_fn, seq: int = 8, d: int = 16, seed: int = 0) -> bool:
    """`True` if `model_fn` is permutation-equivariant: shuffling the input tokens
    shuffles the output the same way (`model_fn(x)[perm] == model_fn(x[perm])`).

    `model_fn` takes `(1, seq, d)` and returns `(1, seq, d)`. Plain (non-causal) attention
    with no positional information is permutation-equivariant — it only ever compares
    tokens to each other, never to a fixed "slot". RoPE ties each query/key to its absolute
    position *before* the dot product, so moving a token's content to a different position
    changes what it does, and the equivariance breaks.
    """
    torch.manual_seed(seed)
    x = torch.randn(1, seq, d)
    perm = torch.randperm(seq)

    out = model_fn(x)
    out_perm_input = model_fn(x[:, perm])
    out_then_perm = out[:, perm]

    return torch.allclose(out_perm_input, out_then_perm, atol=1e-5)


def _attention_no_position(x: Tensor, n_heads: int = 2) -> Tensor:
    """Plain non-causal attention, `x` used directly as q/k/v (no learned projections, no
    positions): the simplest possible thing that is permutation-equivariant."""
    b, t, d = x.shape
    hd = d // n_heads
    qkv = x.view(b, t, n_heads, hd).transpose(1, 2)  # (B, H, T, D)
    out, _ = scaled_dot_product_attention(qkv, qkv, qkv, causal=False)
    return out.transpose(1, 2).reshape(b, t, d)


def _attention_with_rope(x: Tensor, n_heads: int = 2, theta: float = 10000.0) -> Tensor:
    """Same attention, but q/k are rotated by RoPE at their *absolute* position first."""
    b, t, d = x.shape
    hd = d // n_heads
    cos, sin = rope_cos_sin(t, hd, theta=theta)
    qkv = x.view(b, t, n_heads, hd).transpose(1, 2)  # (B, H, T, D)
    q = apply_rope(qkv, cos, sin)
    k = apply_rope(qkv, cos, sin)
    out, _ = scaled_dot_product_attention(q, k, qkv, causal=False)
    return out.transpose(1, 2).reshape(b, t, d)


# ---------------------------------------------------------------------------
# Real model configuration (see specs/COMMON.md; verified with transformers AutoConfig)
# ---------------------------------------------------------------------------

QWEN35_08B = {
    "head_dim": 256,
    "num_attention_heads": 8,
    "num_key_value_heads": 2,
    "num_hidden_layers": 24,
    "partial_rotary_factor": 0.25,
    "rope_theta": 10_000_000.0,
    "max_position_embeddings": 262_144,
}


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------


def _fig_sinusoidal() -> str:
    style()
    seq, d = 64, 64
    pe = sinusoidal_pe(seq, d).numpy()

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6), gridspec_kw={"width_ratios": [1.3, 1]})
    im = axes[0].imshow(pe.T, cmap="RdBu", vmin=-1, vmax=1, aspect="auto", origin="lower")
    axes[0].set_xlabel("position")
    axes[0].set_ylabel("dimension")
    axes[0].set_title(f"Sinusoidal table, {seq} positions x {d} dims")
    fig.colorbar(im, ax=axes[0], shrink=0.85)

    positions = np.arange(seq)
    for dim, color, label in [(0, "#1f77b4", "dim 0 (fast)"), (32, "#d62728", "dim 32 (slow)")]:
        axes[1].plot(positions, pe[:, dim], color=color, label=label)
    axes[1].set_xlabel("position")
    axes[1].set_ylabel("PE value")
    axes[1].set_title("Two dimensions: low dims oscillate\nfast, high dims slowly")
    axes[1].legend()
    fig.suptitle("Sinusoidal positional encoding (Vaswani et al., 2017)")
    fig.tight_layout()
    return str(save(fig, "04_sinusoidal"))


def _fig_rope_rotation() -> str:
    style()
    n_pos = 8
    head_dim = 6  # 3 pairs -> 3 frequencies
    theta = 10000.0
    cos, sin = rope_cos_sin(n_pos, head_dim, theta=theta)
    v = torch.tensor([1.0, 0.0])  # the same 2-D vector at every position, per pair

    fig, axes = plt.subplots(1, 3, figsize=(12.0, 4.2))
    cmap = plt.get_cmap("viridis")
    for pair, ax in enumerate(axes):
        angle = torch.atan2(sin[:, pair], cos[:, pair])
        circle = plt.Circle((0, 0), 1.0, fill=False, color="gray", lw=0.8)
        ax.add_patch(circle)
        for p in range(n_pos):
            a = angle[p].item()
            x, y = math.cos(a) * v[0].item() - math.sin(a) * v[1].item(), \
                   math.sin(a) * v[0].item() + math.cos(a) * v[1].item()
            ax.annotate("", xy=(x, y), xytext=(0, 0),
                        arrowprops={"arrowstyle": "->", "color": cmap(p / (n_pos - 1)), "lw": 1.6})
        ax.set_xlim(-1.3, 1.3)
        ax.set_ylim(-1.3, 1.3)
        ax.set_aspect("equal")
        ax.set_title(f"pair {pair} (freq index {pair})\nangle/step = {angle[1].item():.3f} rad")
        ax.grid(alpha=0.2)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, n_pos - 1))
    fig.colorbar(sm, ax=axes, shrink=0.75, label="position (0..7)", pad=0.02)
    fig.suptitle("RoPE: the same 2-D pair, rotated further at each position\n"
                 "(low frequency index -> big steps; high index -> tiny steps)")
    return str(save(fig, "04_rope_rotation"))


def _fig_rope_relative() -> str:
    """RoPE's "long-term decay": for a fixed vector `v` rotated at two positions, a pair's
    contribution to the dot product is `|v_pair|^2 * cos(distance * freq_pair)`. Summed
    over 32 pairs with geometrically spaced frequencies, the cosines fall out of phase with
    each other as distance grows, so the total decays in envelope even though `q` and `k`
    are the *same* vector (only their position differs) — averaging over many random `v`
    makes that envelope visible.
    """
    style()
    torch.manual_seed(0)
    head_dim = 64
    theta = 10000.0
    max_dist = 512
    offset = 200
    n_samples = 256

    cos, sin = rope_cos_sin(offset + max_dist + 1, head_dim, theta=theta)
    q0 = torch.randn(n_samples, head_dim)
    k0 = q0  # same content vector, rotated by two different positions

    def dot_at(q_pos: int, k_positions: np.ndarray) -> np.ndarray:
        q_rot = apply_rope(q0, cos[q_pos].unsqueeze(0), sin[q_pos].unsqueeze(0))
        out = np.empty(len(k_positions))
        for i, kp in enumerate(k_positions):
            k_rot = apply_rope(k0, cos[kp].unsqueeze(0), sin[kp].unsqueeze(0))
            out[i] = (q_rot * k_rot).sum(dim=-1).mean().item()
        return out

    distances = np.arange(0, max_dist + 1, 8)
    dots_from_0 = dot_at(0, distances)
    dots_from_offset = dot_at(offset, offset + distances)

    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    ax.plot(distances, dots_from_0, label="q at position 0, k at 0..512")
    ax.plot(distances, dots_from_offset, "--", label=f"q at position {offset}, k at {offset}..{offset + 512}")
    ax.set_xlabel("relative distance |q position - k position|")
    ax.set_ylabel("mean q . k (averaged over random vectors)")
    ax.set_title("RoPE dot product depends only on the distance,\nnot the absolute positions")
    ax.legend()
    return str(save(fig, "04_rope_relative"))


def _fig_frequencies() -> str:
    style()
    head_dim = 64
    thetas = {"theta = 10,000 (Vaswani/Llama default)": 10_000.0,
              f"theta = {QWEN35_08B['rope_theta']:,.0f} (Qwen3.5-0.8B rope_theta)": QWEN35_08B["rope_theta"]}

    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    dim_pairs = np.arange(head_dim // 2)
    for label, theta in thetas.items():
        inv_freq = 1.0 / (theta ** (2 * dim_pairs / head_dim))
        wavelength = 2 * math.pi / inv_freq  # positions for one full rotation
        ax.plot(dim_pairs, wavelength, "o-", ms=3, label=label)
    ax.set_yscale("log")
    ax.set_xlabel("dimension pair index (0 = fastest)")
    ax.set_ylabel("wavelength (positions per full rotation)")
    ax.set_title(f"RoPE wavelength per dimension pair, head_dim={head_dim}\n"
                 "low dims: short wavelength (local); high dims: long wavelength (global)")
    ax.legend()
    return str(save(fig, "04_frequencies"))


def _fig_partial_rope() -> str:
    style()
    head_dim = 256
    frac = QWEN35_08B["partial_rotary_factor"]
    rotary_dim = int(head_dim * frac)

    fig, ax = plt.subplots(figsize=(9.5, 2.4))
    colors = ["#2ca02c" if i < rotary_dim else "#cccccc" for i in range(head_dim)]
    ax.bar(range(head_dim), np.ones(head_dim), width=1.0, color=colors, edgecolor="none")
    ax.set_xlim(0, head_dim)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xlabel("channel within one head")
    ax.set_title(f"Partial RoPE, head_dim={head_dim}, rotary_frac={frac}: "
                 f"first {rotary_dim} channels rotated (green), {head_dim - rotary_dim} pass through (gray)")
    return str(save(fig, "04_partial_rope"))


def _fig_context_extension() -> str:
    """Toy illustration of why long context needs a RoPE frequency rescale.

    During training a model only ever sees the *slowest* dimension pair sweep through
    angles `0 .. trained_len * inv_freq[-1]` (it wraps many times for the fast pairs, but
    the slowest pair barely turns at all). Evaluate it at 4x the length with the same
    `theta` and that pair's angle runs 4x past anything seen in training — the "unseen
    angle" problem. A toy NTK-style fix multiplies `theta` so the slowest pair's angle at
    the *new* length lands back where the *old* length used to end.
    """
    style()
    head_dim = 64
    theta = 10000.0
    trained_len = 4096
    eval_len = 16384
    scale = eval_len / trained_len
    positions = np.arange(0, eval_len + 1)

    def slowest_angle(theta_eff: float) -> np.ndarray:
        inv_freq_slowest = 1.0 / (theta_eff ** ((head_dim - 2) / head_dim))
        return positions * inv_freq_slowest

    angle_no_rescale = slowest_angle(theta)
    ntk_theta = theta * scale ** (head_dim / (head_dim - 2))  # toy NTK-style bump
    angle_ntk = slowest_angle(ntk_theta)
    trained_max_angle = trained_len * (1.0 / (theta ** ((head_dim - 2) / head_dim)))

    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    ax.plot(positions, angle_no_rescale, label="no rescale: angle keeps growing past training range")
    ax.plot(positions, angle_ntk, label="toy NTK-style theta rescale: angle stays in range")
    ax.axvline(trained_len, color="gray", ls="--", lw=1)
    ax.axhline(trained_max_angle, color="gray", ls=":", lw=1)
    ax.axhspan(0, trained_max_angle, color="green", alpha=0.08, label="angle range seen in training")
    ax.text(trained_len * 1.02, trained_max_angle * 1.05, "trained length (4,096)", fontsize=8)
    ax.set_xlabel("position (tokens)")
    ax.set_ylabel("rotation angle of the slowest dimension pair (radians)")
    ax.set_title("Context extension — ILLUSTRATION ONLY (toy theta rescale, not real YaRN)\n"
                 "a model trained to 4k sees only the shaded angle range; without a rescale,\n"
                 "16k tokens push the slowest RoPE dimension into angles it never saw in training")
    ax.legend(fontsize=8, loc="upper left")
    return str(save(fig, "04_context_extension"))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


@app.command()
def plots() -> None:
    """Regenerate every figure for this chapter."""
    print(f"wrote: {_fig_sinusoidal()}")
    print(f"wrote: {_fig_rope_rotation()}")
    print(f"wrote: {_fig_rope_relative()}")
    print(f"wrote: {_fig_frequencies()}")
    print(f"wrote: {_fig_partial_rope()}")
    print(f"wrote: {_fig_context_extension()}")


@app.command()
def demo() -> None:
    """Print the permutation-test result and the config values quoted in the chapter."""
    equivariant_no_pos = permutation_test(_attention_no_position)
    equivariant_rope = permutation_test(_attention_with_rope)
    print("permutation test (shuffle tokens, compare to shuffling the output):")
    print(f"  plain attention, no positions: permutation-equivariant = {equivariant_no_pos}")
    print(f"  attention + RoPE:              permutation-equivariant = {equivariant_rope}")

    print("\nQwen3.5-0.8B config values (verified with transformers.AutoConfig):")
    for k, v in QWEN35_08B.items():
        print(f"  {k}: {v:,}" if isinstance(v, (int, float)) else f"  {k}: {v}")


if __name__ == "__main__":
    app()
