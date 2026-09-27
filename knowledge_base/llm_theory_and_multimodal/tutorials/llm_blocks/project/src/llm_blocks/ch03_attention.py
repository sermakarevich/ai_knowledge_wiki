"""Chapter 03 — attention: Q/K/V, causal mask, multi-head, GQA, QK-norm, gate, KV cache.

`uv run python -m llm_blocks.ch03_attention plots` draws the six figures that need no
downloads; `plots-real` draws the two figures that use SmolLM2-135M (downloaded once,
cached); `demo` prints the FLOP and cache-size numbers quoted in the chapter.

Shape convention everywhere in this module: `(B, H, T, D)` — batch, heads, time
(tokens), head dimension. The only exception is the *input* to a whole attention
module, which is `(B, T, d_model)`, the shape a transformer's residual stream has.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import torch
import typer
from matplotlib.patches import FancyArrowPatch, Rectangle
from torch import Tensor, nn

from llm_blocks.plotting import save, style
from llm_blocks.reference import load_smollm

app = typer.Typer(add_completion=False, no_args_is_help=False)


# ---------------------------------------------------------------------------
# From-scratch building blocks
# ---------------------------------------------------------------------------


def scaled_dot_product_attention(
    q: Tensor, k: Tensor, v: Tensor, causal: bool = True
) -> tuple[Tensor, Tensor]:
    """Attention for one set of heads. Returns `(output, weights)`.

    `q, k, v` are `(B, H, T, D)` (queries may be shorter than keys when decoding with a
    cache: `(B, H, Tq, D)` with `Tk >= Tq`). The maths is three lines:

        scores  = q @ k^T / sqrt(D)          "how well does each question match each label"
        weights = softmax(masked scores)     "turn the matches into fractions summing to 1"
        out     = weights @ v                "a weighted average of the drawers' contents"

    With `causal=True` every position may only look at itself and the past: the future
    entries are set to `-inf` *before* the softmax, so `exp(-inf) = 0` gives them exactly
    zero weight.
    """
    t_q, t_k = q.shape[-2], k.shape[-2]
    scores = q @ k.transpose(-2, -1) / math.sqrt(q.shape[-1])
    if causal:
        scores = scores + causal_mask(t_q, t_k, dtype=scores.dtype, device=scores.device)
    weights = torch.softmax(scores, dim=-1)
    return weights @ v, weights


def causal_mask(t_q: int, t_k: int, dtype: torch.dtype = torch.float32, device=None) -> Tensor:
    """Additive `(1, 1, t_q, t_k)` mask: `0` where a token may look, `-inf` where it may not.

    Query `i` sits at absolute position `t_k - t_q + i` (the offset matters only when the
    queries are the *new* tokens appended to a KV cache), so it may attend to every key
    up to and including that position.
    """
    offset = t_k - t_q
    rows = torch.arange(t_q, device=device).unsqueeze(1) + offset
    cols = torch.arange(t_k, device=device).unsqueeze(0)
    blocked = cols > rows
    mask = torch.zeros(t_q, t_k, dtype=dtype, device=device)
    mask = mask.masked_fill(blocked, float("-inf"))
    return mask.view(1, 1, t_q, t_k)


class MultiHeadAttention(nn.Module):
    """Classic multi-head attention (Vaswani et al., 2017), written out in full.

    One linear layer each for queries, keys and values maps the residual stream
    `(B, T, d_model)` into `n_heads` independent sub-spaces of size `d_model // n_heads`.
    Each head runs its own attention; the results are concatenated back into one vector
    per token and passed through an output projection.
    """

    def __init__(self, d_model: int, n_heads: int, bias: bool = True) -> None:
        super().__init__()
        if d_model % n_heads != 0:
            raise ValueError(f"d_model={d_model} must be divisible by n_heads={n_heads}")
        self.d_model = d_model
        self.n_heads = n_heads
        self.head_dim = d_model // n_heads
        self.q_proj = nn.Linear(d_model, d_model, bias=bias)
        self.k_proj = nn.Linear(d_model, d_model, bias=bias)
        self.v_proj = nn.Linear(d_model, d_model, bias=bias)
        self.o_proj = nn.Linear(d_model, d_model, bias=bias)

    def _split_heads(self, x: Tensor) -> Tensor:
        """`(B, T, d_model)` -> `(B, H, T, D)`."""
        b, t, _ = x.shape
        return x.view(b, t, self.n_heads, self.head_dim).transpose(1, 2)

    def forward(self, x: Tensor, causal: bool = True) -> tuple[Tensor, Tensor]:
        b, t, _ = x.shape
        q = self._split_heads(self.q_proj(x))
        k = self._split_heads(self.k_proj(x))
        v = self._split_heads(self.v_proj(x))
        out, weights = scaled_dot_product_attention(q, k, v, causal=causal)
        out = out.transpose(1, 2).reshape(b, t, self.d_model)  # merge heads back
        return self.o_proj(out), weights


class RMSNorm(nn.Module):
    """Root-mean-square normalisation over the last dimension, with a learned gain.

    `x / sqrt(mean(x^2) + eps) * weight`: it rescales a vector to a fixed length but,
    unlike LayerNorm, does not subtract the mean. Chapter 05 goes into why.
    """

    def __init__(self, dim: int, eps: float = 1e-6) -> None:
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(dim))

    def forward(self, x: Tensor) -> Tensor:
        variance = x.float().pow(2).mean(dim=-1, keepdim=True)
        normed = x.float() * torch.rsqrt(variance + self.eps)
        return (self.weight.float() * normed).to(x.dtype)


class GroupedQueryAttention(nn.Module):
    """Grouped-query attention (GQA), the layout modern LLMs actually use.

    Queries keep `n_heads` heads, but keys and values only have `n_kv_heads` heads, each
    shared by a group of `n_heads // n_kv_heads` query heads (`repeat_interleave` copies
    each KV head across its group). Only the K/V tensors are stored in the KV cache, so
    the cache shrinks by exactly that group factor.

    Two Qwen3-family options:
      * `qk_norm=True` — RMSNorm applied to every query and key head *before* the dot
        product, so head norms cannot drift upwards during training (Qwen3 onwards).
      * `gated=True` — a parallel `gate_proj` whose sigmoid multiplies the attention
        output elementwise before `o_proj`; the "gated attention" of Qwen3.5 / Qwen3-Next.
    """

    def __init__(
        self,
        d_model: int,
        n_heads: int,
        n_kv_heads: int,
        head_dim: int,
        qk_norm: bool = True,
        gated: bool = False,
        eps: float = 1e-6,
        bias: bool = False,
    ) -> None:
        super().__init__()
        if n_heads % n_kv_heads != 0:
            raise ValueError(f"n_heads={n_heads} must be divisible by n_kv_heads={n_kv_heads}")
        self.n_heads = n_heads
        self.n_kv_heads = n_kv_heads
        self.n_groups = n_heads // n_kv_heads
        self.head_dim = head_dim
        self.scaling = head_dim**-0.5
        self.gated = gated

        self.q_proj = nn.Linear(d_model, n_heads * head_dim, bias=bias)
        self.k_proj = nn.Linear(d_model, n_kv_heads * head_dim, bias=bias)
        self.v_proj = nn.Linear(d_model, n_kv_heads * head_dim, bias=bias)
        self.o_proj = nn.Linear(n_heads * head_dim, d_model, bias=bias)
        self.q_norm = RMSNorm(head_dim, eps=eps) if qk_norm else None
        self.k_norm = RMSNorm(head_dim, eps=eps) if qk_norm else None
        self.gate_proj = nn.Linear(d_model, n_heads * head_dim, bias=bias) if gated else None

    def forward(
        self,
        x: Tensor,
        causal: bool = True,
        cache: KVCache | None = None,
        rope: Callable[[Tensor], Tensor] | None = None,
    ) -> tuple[Tensor, Tensor]:
        b, t, _ = x.shape
        q = self.q_proj(x).view(b, t, self.n_heads, self.head_dim)
        k = self.k_proj(x).view(b, t, self.n_kv_heads, self.head_dim)
        v = self.v_proj(x).view(b, t, self.n_kv_heads, self.head_dim)
        if self.q_norm is not None:
            q, k = self.q_norm(q), self.k_norm(k)
        q, k, v = q.transpose(1, 2), k.transpose(1, 2), v.transpose(1, 2)  # -> (B, H, T, D)

        # Positions enter here and nowhere else: `rope` (chapter 04) rotates every query and
        # key head by its position's angle, *before* the keys go into the cache — exactly
        # where `transformers` calls `apply_rotary_pos_emb`. Left as an injected callable
        # because chapter 04 is built on top of this file, so this file cannot import it.
        if rope is not None:
            q, k = rope(q), rope(k)

        if cache is not None:
            k, v = cache.append(k, v)

        # Share each KV head across its group of query heads.
        k_rep = k.repeat_interleave(self.n_groups, dim=1)
        v_rep = v.repeat_interleave(self.n_groups, dim=1)

        out, weights = scaled_dot_product_attention(q, k_rep, v_rep, causal=causal)
        out = out.transpose(1, 2).reshape(b, t, self.n_heads * self.head_dim)
        if self.gate_proj is not None:
            out = out * torch.sigmoid(self.gate_proj(x))
        return self.o_proj(out), weights


# ---------------------------------------------------------------------------
# KV cache
# ---------------------------------------------------------------------------


class KVCache:
    """The simplest possible KV cache: keep the keys/values of every past token.

    Each call to `append` concatenates the new step's `(B, H_kv, 1, D)` keys and values
    onto what is already stored and returns the full history, so the new token can attend
    to everything before it without the model recomputing those projections.
    """

    def __init__(self) -> None:
        self.k: Tensor | None = None
        self.v: Tensor | None = None

    def append(self, k: Tensor, v: Tensor) -> tuple[Tensor, Tensor]:
        self.k = k if self.k is None else torch.cat([self.k, k], dim=-2)
        self.v = v if self.v is None else torch.cat([self.v, v], dim=-2)
        return self.k, self.v

    def __len__(self) -> int:
        return 0 if self.k is None else self.k.shape[-2]


def kv_cache_bytes(
    n_layers: int, n_kv_heads: int, head_dim: int, seq: int, dtype_bytes: int = 2
) -> int:
    """Bytes of KV cache for one sequence:

        bytes = 2 (K and V) * n_layers * n_kv_heads * head_dim * seq * dtype_bytes

    Nothing else is in there: no batch dimension (one sequence), no query heads — with
    grouped-query attention the query heads share these keys and values.
    """
    return 2 * n_layers * n_kv_heads * head_dim * seq * dtype_bytes


# ---------------------------------------------------------------------------
# A toy model, only to show that the KV cache changes cost but not output
# ---------------------------------------------------------------------------


@dataclass
class ToyConfig:
    """A tiny decoder-only stack: attention + one linear, repeated `n_layers` times."""

    vocab_size: int = 64
    d_model: int = 32
    n_heads: int = 4
    n_kv_heads: int = 2
    head_dim: int = 8
    n_layers: int = 4


class ToyLM(nn.Module):
    """Embedding -> [GQA + linear] x n_layers -> LM head. No norms, no MLP: not a good
    model, just enough machinery to run a greedy-decoding loop two different ways."""

    def __init__(self, cfg: ToyConfig) -> None:
        super().__init__()
        self.cfg = cfg
        self.embed = nn.Embedding(cfg.vocab_size, cfg.d_model)
        self.layers = nn.ModuleList(
            GroupedQueryAttention(cfg.d_model, cfg.n_heads, cfg.n_kv_heads, cfg.head_dim)
            for _ in range(cfg.n_layers)
        )
        self.mixers = nn.ModuleList(nn.Linear(cfg.d_model, cfg.d_model) for _ in range(cfg.n_layers))
        self.lm_head = nn.Linear(cfg.d_model, cfg.vocab_size, bias=False)

    def forward(self, ids: Tensor, caches: list[KVCache] | None = None) -> Tensor:
        h = self.embed(ids)
        for i, (attn, mixer) in enumerate(zip(self.layers, self.mixers)):
            cache = None if caches is None else caches[i]
            h = h + attn(h, causal=True, cache=cache)[0]
            h = h + torch.tanh(mixer(h))
        return self.lm_head(h)


def attention_matmul_flops(cfg: ToyConfig, t_q: int, t_k: int) -> int:
    """Multiply-add FLOPs of the matrix multiplies in one attention layer, counting
    `2 * m * n * k` for an `(m, k) @ (k, n)` product: the four projections plus the two
    attention matmuls (scores and the weighted sum of values)."""
    d, h, kv, hd = cfg.d_model, cfg.n_heads, cfg.n_kv_heads, cfg.head_dim
    proj = 2 * t_q * d * (h * hd)  # q_proj
    proj += 2 * 2 * t_q * d * (kv * hd)  # k_proj + v_proj
    proj += 2 * t_q * (h * hd) * d  # o_proj
    scores = 2 * h * t_q * t_k * hd  # q @ k^T
    values = 2 * h * t_q * t_k * hd  # weights @ v
    return proj + scores + values


def greedy_decode(
    model: ToyLM, prompt: Tensor, n_new: int, use_cache: bool
) -> tuple[Tensor, int]:
    """Generate `n_new` tokens greedily; return `(ids, attention matmul FLOPs)`.

    Without a cache every step re-runs the whole prefix through the model. With a cache
    each step feeds in one token and reads the stored keys/values of the prefix, so the
    per-step cost stops growing with the prompt (except for the attention matmuls, which
    still touch every past key).
    """
    ids = prompt.clone()
    flops = 0
    caches = [KVCache() for _ in range(model.cfg.n_layers)] if use_cache else None
    with torch.no_grad():
        for step in range(n_new):
            if use_cache:
                chunk = ids if step == 0 else ids[:, -1:]
                t_q = chunk.shape[1]
                t_k = len(caches[0]) + t_q
                logits = model(chunk, caches=caches)
            else:
                t_q = t_k = ids.shape[1]
                logits = model(ids)
            flops += model.cfg.n_layers * attention_matmul_flops(model.cfg, t_q, t_k)
            next_id = logits[:, -1].argmax(dim=-1, keepdim=True)
            ids = torch.cat([ids, next_id], dim=1)
    return ids, flops


# ---------------------------------------------------------------------------
# Real model configuration (see specs/COMMON.md; verified with transformers)
# ---------------------------------------------------------------------------

QWEN38_27B = {
    "n_layers": 64,
    "n_attention_layers": 16,  # 3:1 hybrid: 3 linear-attention layers per full-attention one
    "n_kv_heads": 4,
    "n_heads": 24,
    "head_dim": 256,
}


# ---------------------------------------------------------------------------
# Figures (no downloads)
# ---------------------------------------------------------------------------

TOY_TOKENS = ["The", "cat", "sat", "because", "it", "was"]


def _toy_qk() -> tuple[Tensor, Tensor, Tensor]:
    """Hand-built q/k/v for a 6-token sentence so the heat-map tells a story.

    Every token gets a 5-dimensional "topic" code (animal, action, cause, filler,
    pronoun). Keys advertise a token's own topic; queries say which topic that token is
    looking for — "it" looks for an animal, so it should find "cat".
    """
    #                animal action cause filler pronoun
    keys = torch.tensor(
        [
            [0.0, 0.0, 0.0, 1.0, 0.0],  # The     — filler
            [1.0, 0.0, 0.0, 0.0, 0.0],  # cat     — animal
            [0.0, 1.0, 0.0, 0.0, 0.0],  # sat     — action
            [0.0, 0.0, 1.0, 0.0, 0.0],  # because — cause
            [0.0, 0.0, 0.0, 0.0, 1.0],  # it      — pronoun, stands for something else
            [0.0, 1.0, 0.0, 0.0, 0.0],  # was     — action
        ]
    )
    queries = torch.tensor(
        [
            [0.0, 0.0, 0.0, 1.0, 0.0],  # The     — nothing to look for yet
            [0.0, 0.0, 0.0, 1.0, 0.0],  # cat     — nothing to look for yet
            [1.0, 0.0, 0.0, 0.0, 0.0],  # sat     — who sat? an animal
            [0.0, 1.0, 0.0, 0.0, 0.0],  # because — because of which action?
            [1.0, 0.0, 0.0, 0.0, 0.0],  # it      — "it" = which animal?
            [1.0, 0.0, 0.0, 0.0, 0.0],  # was     — the subject again
        ]
    )
    values = torch.eye(6)
    scale = 6.0  # sharpen the softmax so the picture is readable
    return (queries * scale).view(1, 1, 6, 5), keys.view(1, 1, 6, 5), values.view(1, 1, 6, 6)


def _fig_attention_weights_toy() -> str:
    style()
    q, k, v = _toy_qk()
    _, weights = scaled_dot_product_attention(q, k, v, causal=True)
    w = weights[0, 0].numpy()

    fig, ax = plt.subplots(figsize=(6.4, 5.2))
    im = ax.imshow(w, cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks(range(6), TOY_TOKENS, rotation=30, ha="right")
    ax.set_yticks(range(6), TOY_TOKENS)
    ax.set_xlabel("key — the token being looked at")
    ax.set_ylabel("query — the token doing the looking")
    ax.set_title('Causal attention weights (hand-built Q/K)\neach row sums to 1; "it" finds "cat"')
    for i in range(6):
        for j in range(6):
            if w[i, j] > 0.005:
                ax.text(j, i, f"{w[i, j]:.2f}", ha="center", va="center",
                        color="white" if w[i, j] > 0.5 else "black", fontsize=8)
    ax.grid(False)
    ax.add_patch(Rectangle((0.5, 3.5), 1, 1, fill=False, edgecolor="#d62728", lw=2.5))
    fig.colorbar(im, ax=ax, shrink=0.8, label="attention weight")
    return str(save(fig, "03_attention_weights_toy"))


def _fig_causal_mask() -> str:
    style()
    t = 8
    mask = causal_mask(t, t)[0, 0]
    allowed = (mask == 0).float().numpy()

    fig, ax = plt.subplots(figsize=(5.6, 5.0))
    ax.imshow(allowed, cmap="Greens", vmin=0, vmax=1.4)
    ax.set_xticks(range(t), [f"k{j}" for j in range(t)])
    ax.set_yticks(range(t), [f"q{i}" for i in range(t)])
    ax.set_xlabel("key position")
    ax.set_ylabel("query position")
    ax.set_title("Causal mask: green = allowed (0 added), white = blocked (−inf added)")
    for i in range(t):
        for j in range(t):
            ax.text(j, i, "0" if allowed[i, j] else "−∞", ha="center", va="center", fontsize=8,
                    color="black")
    ax.grid(False)
    return str(save(fig, "03_causal_mask"))


def _fig_multihead_schematic() -> str:
    style()
    fig, ax = plt.subplots(figsize=(9.5, 4.6))
    ax.set_xlim(0, 10.6)
    ax.set_ylim(-0.3, 5)
    ax.axis("off")
    ax.set_title("Multi-head attention: split → attend per head → concat → project")

    def box(x, y, w, h, text, color, fontsize=9):
        ax.add_patch(Rectangle((x, y), w, h, facecolor=color, edgecolor="black", lw=1.0, alpha=0.85))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize)

    def arrow(x1, y1, x2, y2):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="->", mutation_scale=13, lw=1.1))

    box(0.2, 2.0, 1.3, 1.0, "x\n(B,T,d)", "#cfe3f5")
    box(1.9, 2.0, 1.3, 1.0, "Q/K/V\nprojections", "#cfe3f5")
    arrow(1.5, 2.5, 1.9, 2.5)

    ys = [4.1, 3.2, 2.3, 1.4]
    for i, y in enumerate(ys):
        label = f"head {i + 1}\nattention" if i < 3 else "head H\nattention"
        box(3.7, y - 0.32, 1.9, 0.64, label, "#dcefdc", fontsize=8)
        arrow(3.2, 2.5, 3.7, y)
        arrow(5.6, y, 6.2, 2.5)
    ax.text(4.65, 0.75, "each head has its own d/H-dim sub-space", ha="center", fontsize=8,
            style="italic")

    box(6.2, 2.0, 1.3, 1.0, "concat\n(B,T,d)", "#f5ddcf")
    box(7.9, 2.0, 1.3, 1.0, "o_proj", "#f5ddcf")
    arrow(7.5, 2.5, 7.9, 2.5)
    arrow(9.2, 2.5, 9.6, 2.5)
    box(9.6, 2.2, 0.9, 0.6, "out", "#cfe3f5", fontsize=8)
    return str(save(fig, "03_multihead_schematic"))


def _fig_gqa_schematic() -> str:
    style()
    n_q, n_kv = QWEN38_27B["n_heads"], QWEN38_27B["n_kv_heads"]
    group = n_q // n_kv
    colors = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd"]

    fig, ax = plt.subplots(figsize=(10.0, 4.4))
    ax.set_xlim(-0.6, n_q + 0.4)
    ax.set_ylim(-0.4, 3.6)
    ax.axis("off")
    ax.set_title(
        f"Grouped-query attention in Qwen3.5/3.8: {n_q} query heads share {n_kv} key/value heads"
        f"\n(head dim {QWEN38_27B['head_dim']}; each KV head serves {group} query heads)"
    )

    for i in range(n_q):
        c = colors[i // group]
        ax.add_patch(Rectangle((i + 0.08, 2.4), 0.84, 0.9, facecolor=c, alpha=0.75,
                               edgecolor="black", lw=0.5))
        ax.text(i + 0.5, 2.85, f"{i}", ha="center", va="center", fontsize=7, color="white")
    ax.text(-0.5, 2.85, "Q heads", ha="right", va="center", fontsize=10)

    for j in range(n_kv):
        x = j * group
        ax.add_patch(Rectangle((x + 0.08, 0.5), group - 0.16, 0.9, facecolor=colors[j], alpha=0.75,
                               edgecolor="black", lw=0.8))
        ax.text(x + group / 2, 0.95, f"K/V head {j}", ha="center", va="center", fontsize=9,
                color="white")
        for i in range(x, x + group):
            ax.add_patch(FancyArrowPatch((i + 0.5, 2.4), (x + group / 2, 1.4), arrowstyle="->",
                                         mutation_scale=8, lw=0.7, color=colors[j], alpha=0.7))
    ax.text(-0.5, 0.95, "KV heads\n(cached)", ha="right", va="center", fontsize=10)
    ax.text(n_q / 2, 0.0, f"KV cache is {n_q // n_kv}x smaller than with one KV head per query head",
            ha="center", fontsize=9, style="italic")
    return str(save(fig, "03_gqa_schematic"))


def _fig_kv_cache_growth() -> str:
    style()
    seqs = np.array([1024, 4096, 16384, 32768, 65536, 131072, 262144])
    gb = 1024**3
    hybrid = np.array([
        kv_cache_bytes(QWEN38_27B["n_attention_layers"], QWEN38_27B["n_kv_heads"],
                       QWEN38_27B["head_dim"], int(s)) / gb
        for s in seqs
    ])
    dense = np.array([
        kv_cache_bytes(QWEN38_27B["n_layers"], QWEN38_27B["n_kv_heads"],
                       QWEN38_27B["head_dim"], int(s)) / gb
        for s in seqs
    ])

    fig, ax = plt.subplots(figsize=(8.4, 5.0))
    ax.plot(seqs, hybrid, "o-", label=f"3:1 hybrid — {QWEN38_27B['n_attention_layers']} attention layers")
    ax.plot(seqs, dense, "s-", label=f"all-attention — {QWEN38_27B['n_layers']} layers")
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xlabel("context length (tokens)")
    ax.set_ylabel("KV cache for one sequence (GB, bf16)")
    ax.set_title("KV cache growth, Qwen3.8-27B geometry\n"
                 "bytes = 2 · layers · kv_heads · head_dim · seq · 2")
    ax.set_xticks(seqs, [f"{s // 1024}k" for s in seqs])

    seq70k = 70_000
    gb70k = kv_cache_bytes(QWEN38_27B["n_attention_layers"], QWEN38_27B["n_kv_heads"],
                           QWEN38_27B["head_dim"], seq70k) / gb
    ax.axvline(seq70k, color="gray", ls="--", lw=1)
    ax.annotate(
        f"70k tokens ≈ {gb70k:.1f} GB\n(fits beside the weights on a 24 GB card)",
        xy=(seq70k, gb70k), xytext=(6000, gb70k * 3.0),
        arrowprops={"arrowstyle": "->", "color": "black", "lw": 1.2}, fontsize=9,
    )
    ax.legend(loc="upper left")
    return str(save(fig, "03_kv_cache_growth"))


def _fig_qk_norm_effect() -> str:
    style()
    torch.manual_seed(0)
    b, h, t, d = 1, 4, 128, 64
    # "Large-norm" q/k: what heads drift towards late in a long training run.
    q = torch.randn(b, h, t, d) * 3.0
    k = torch.randn(b, h, t, d) * 3.0
    norm = RMSNorm(d)

    with torch.no_grad():
        raw = (q @ k.transpose(-2, -1) / math.sqrt(d)).flatten().numpy()
        normed = (norm(q) @ norm(k).transpose(-2, -1) / math.sqrt(d)).flatten().numpy()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.0, 4.2))
    ax1.hist(raw, bins=80, color="#d62728", alpha=0.85)
    ax1.set_title(f"no QK-norm: logits span ±{np.abs(raw).max():.0f}")
    ax2.hist(normed, bins=80, color="#2ca02c", alpha=0.85)
    ax2.set_title(f"QK-norm: logits span ±{np.abs(normed).max():.0f}")
    for ax in (ax1, ax2):
        ax.set_xlabel("attention logit  q·k/√d")
        ax.set_ylabel("count")
    fig.suptitle("QK-norm keeps attention logits in a small range, so softmax cannot saturate")
    fig.tight_layout()

    top_raw = torch.softmax(torch.tensor(raw[:t]), dim=-1).max().item()
    top_norm = torch.softmax(torch.tensor(normed[:t]), dim=-1).max().item()
    for ax, top in ((ax1, top_raw), (ax2, top_norm)):
        ax.set_ylim(0, ax.get_ylim()[1] * 1.2)
        ax.text(0.02, 0.96, f"largest softmax weight in one row: {top:.3f}",
                transform=ax.transAxes, fontsize=8, va="top",
                bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.85})
    return str(save(fig, "03_qk_norm_effect"))


# ---------------------------------------------------------------------------
# Figures that need the real model
# ---------------------------------------------------------------------------

REAL_SENTENCE = "The cat sat on the mat, and then it slept for hours."

# (layer, head, label) — picked by inspecting the SmolLM2-135M attention maps; see
# `_describe_real_heads()`, which re-derives the choice from the data.
REAL_HEADS = [
    (0, 2, "layer 0"),
    (1, 1, "layer 1"),
    (3, 0, "layer 3"),
    (5, 0, "layer 5"),
    (10, 3, "layer 10"),
    (20, 0, "layer 20"),
]


def _real_attentions() -> tuple[list[str], tuple[Tensor, ...]]:
    tokenizer, model = load_smollm()
    enc = tokenizer(REAL_SENTENCE, return_tensors="pt")
    with torch.no_grad():
        out = model(**enc, output_attentions=True)
    tokens = [t.replace("Ġ", "_") for t in tokenizer.convert_ids_to_tokens(enc["input_ids"][0])]
    return tokens, out.attentions


def _classify_head(w: np.ndarray) -> str:
    """Label an attention map by the simplest pattern it matches.

    `previous token`: most of the mass sits one step back on the diagonal.
    `first-token sink`: most of the mass sits on column 0 (the "attention sink").
    otherwise `content`: the head spreads its attention over earlier words.
    """
    t = w.shape[0]
    prev = np.mean([w[i, i - 1] for i in range(1, t)])
    sink = w[1:, 0].mean()
    diag = np.mean([w[i, i] for i in range(t)])
    if prev > 0.4:
        return "previous-token head"
    if sink > 0.5:
        return "first-token sink"
    if diag > 0.4:
        return "self / current-token head"
    return "content head"


def _fig_real_attention_heads() -> str:
    style()
    tokens, attentions = _real_attentions()
    n = min(12, len(tokens))
    fig, axes = plt.subplots(2, 3, figsize=(12.5, 8.4))
    for ax, (layer, head, name) in zip(axes.ravel(), REAL_HEADS):
        w = attentions[layer][0, head, :n, :n].numpy()
        ax.imshow(w, cmap="Blues", vmin=0, vmax=1)
        ax.set_xticks(range(n), tokens[:n], rotation=90, fontsize=7)
        ax.set_yticks(range(n), tokens[:n], fontsize=7)
        ax.set_title(f"{name}, head {head}\n{_classify_head(w)}", fontsize=10)
        ax.grid(False)
    fig.suptitle(f"SmolLM2-135M attention weights — “{REAL_SENTENCE}”", fontsize=12)
    fig.tight_layout()
    return str(save(fig, "03_real_attention_heads"))


def _fig_real_attention_entropy() -> str:
    style()
    _, attentions = _real_attentions()
    means, spreads = [], []
    for w in attentions:
        p = w[0].clamp_min(1e-12)  # (H, T, T)
        ent = -(p * p.log()).sum(dim=-1)  # entropy of each row, in nats
        rows = ent[:, 1:]  # row 0 has one key only: entropy is always 0
        means.append(rows.mean().item())
        spreads.append(rows.std().item())

    layers = np.arange(len(means))
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(layers, means, "o-", label="mean over heads and positions")
    ax.fill_between(layers, np.array(means) - np.array(spreads), np.array(means) + np.array(spreads),
                    alpha=0.2, label="± 1 std over heads/positions")
    ax.set_xlabel("layer")
    ax.set_ylabel("attention entropy (nats)")
    ax.set_title("SmolLM2-135M: how spread-out attention is, per layer\n"
                 "low = a head looks at one token; high = it averages over many")
    ax.legend()
    return str(save(fig, "03_real_attention_entropy"))


def _describe_real_heads() -> None:
    """Print the pattern label for every (layer, head) so the six in `REAL_HEADS` can be
    re-picked if the checkpoint or the sentence ever changes."""
    tokens, attentions = _real_attentions()
    n = min(12, len(tokens))
    for layer, w_layer in enumerate(attentions):
        labels = [_classify_head(w_layer[0, h, :n, :n].numpy()) for h in range(w_layer.shape[1])]
        interesting = [f"h{h}:{lab}" for h, lab in enumerate(labels) if lab != "content head"]
        print(f"layer {layer:2d}: {', '.join(interesting) if interesting else 'all content heads'}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


@app.command()
def plots() -> None:
    """Regenerate every figure for this chapter that needs no download."""
    print(f"wrote: {_fig_attention_weights_toy()}")
    print(f"wrote: {_fig_causal_mask()}")
    print(f"wrote: {_fig_multihead_schematic()}")
    print(f"wrote: {_fig_gqa_schematic()}")
    print(f"wrote: {_fig_kv_cache_growth()}")
    print(f"wrote: {_fig_qk_norm_effect()}")


@app.command(name="plots-real")
def plots_real() -> None:
    """Regenerate the figures that need SmolLM2-135M (downloads once, cached)."""
    print(f"wrote: {_fig_real_attention_heads()}")
    print(f"wrote: {_fig_real_attention_entropy()}")


@app.command(name="head-patterns")
def head_patterns() -> None:
    """Print the pattern label of every SmolLM2 head (how `REAL_HEADS` was chosen)."""
    _describe_real_heads()


@app.command()
def demo() -> None:
    """Print the FLOP and cache-size numbers quoted in the chapter."""
    torch.manual_seed(0)
    cfg = ToyConfig()
    model = ToyLM(cfg).eval()
    prompt = torch.randint(0, cfg.vocab_size, (1, 8))
    n_new = 256

    with_cache, flops_cache = greedy_decode(model, prompt, n_new, use_cache=True)
    without_cache, flops_plain = greedy_decode(model, prompt, n_new, use_cache=False)
    same = torch.equal(with_cache, without_cache)

    print(f"toy model: {cfg.n_layers} layers, d_model={cfg.d_model}, "
          f"{cfg.n_heads} Q heads / {cfg.n_kv_heads} KV heads, head dim {cfg.head_dim}")
    print(f"greedy decode of {n_new} tokens from an {prompt.shape[1]}-token prompt")
    print(f"  identical output tokens: {same}")
    print(f"  attention matmul FLOPs without cache: {flops_plain / 1e9:9.3f} G")
    print(f"  attention matmul FLOPs with    cache: {flops_cache / 1e9:9.3f} G")
    print(f"  speed-up factor: {flops_plain / flops_cache:.1f}x")

    print("\nKV cache, one sequence, bf16 (2 bytes):")
    print("  bytes = 2 * layers * kv_heads * head_dim * seq * 2")
    gb = 1024**3
    for seq in (4096, 32768, 70_000, 131072, 262144):
        hybrid = kv_cache_bytes(QWEN38_27B["n_attention_layers"], QWEN38_27B["n_kv_heads"],
                                QWEN38_27B["head_dim"], seq) / gb
        dense = kv_cache_bytes(QWEN38_27B["n_layers"], QWEN38_27B["n_kv_heads"],
                               QWEN38_27B["head_dim"], seq) / gb
        mha = kv_cache_bytes(QWEN38_27B["n_layers"], QWEN38_27B["n_heads"],
                             QWEN38_27B["head_dim"], seq) / gb
        print(f"  seq={seq:>7,}:  3:1 hybrid (16 attn layers) {hybrid:7.2f} GB   "
              f"all-attention (64 layers) {dense:7.2f} GB   "
              f"no GQA (64 layers, 24 KV heads) {mha:8.2f} GB")


if __name__ == "__main__":
    app()
