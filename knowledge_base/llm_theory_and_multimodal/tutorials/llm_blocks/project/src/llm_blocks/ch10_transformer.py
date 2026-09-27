"""Chapter 10 — assembling the blocks into a decoder that *is* Qwen3.

Nothing new is implemented here. `DecoderLayer` and `Decoder` are pure wiring around the
classes written in chapters 02–06:

    ch02  Embedding, TiedLMHead          token ids -> vectors, vectors -> logits
    ch03  GroupedQueryAttention          the mixer (with QK-norm and a KV cache)
    ch04  rope_cos_sin, apply_rope       where each token sits in the sequence
    ch05  RMSNorm                        the scale control in front of every sub-block
    ch06  SwiGLUMLP                      the per-token feed-forward memory

`load_qwen3_weights` copies a `transformers` `Qwen3ForCausalLM` state dict into that stack,
after which the two models produce the same logits to floating-point noise (~1e-4 in fp32)
and therefore the same greedy tokens.

Commands:
  `plots`       four figures, no downloads beyond the small config files
  `plots-real`  the Qwen3-0.6B logit-match figure (downloads 1.2 GB once)
  `demo`        tiny-model equivalence + the 27B parameter/FLOP table
  `demo-real`   the identical 20-token continuation, written to ../assets/10_real_generation.txt
"""

from __future__ import annotations

from dataclasses import dataclass

import matplotlib.pyplot as plt
import torch
import typer
from matplotlib.patches import FancyArrowPatch, Rectangle
from torch import Tensor, nn

from llm_blocks.ch02_tokens_embeddings import Embedding, TiedLMHead
from llm_blocks.ch03_attention import GroupedQueryAttention, KVCache
from llm_blocks.ch04_positional_encoding import apply_rope, rope_cos_sin
from llm_blocks.ch05_norm_residual import RMSNorm
from llm_blocks.ch06_mlp_moe import SwiGLUMLP, load_text_config, param_breakdown
from llm_blocks.plotting import ASSETS, save, style

app = typer.Typer(add_completion=False, no_args_is_help=False)

QWEN3_06B_ID = "Qwen/Qwen3-0.6B"
QWEN35_08B_ID = "Qwen/Qwen3.5-0.8B"
QWEN38_27B_ID = "Qwen/Qwen3.8-27B"


# ---------------------------------------------------------------------------
# 1. The decoder, assembled from the blocks of chapters 02–06
# ---------------------------------------------------------------------------


@dataclass
class DecoderConfig:
    """Everything that has to be decided before a single weight exists.

    These are exactly the fields a Hugging Face `Qwen3Config` carries under different
    names; `decoder_config_from_hf` does the translation.
    """

    vocab_size: int
    d_model: int
    n_layers: int
    n_heads: int
    n_kv_heads: int
    head_dim: int
    d_ff: int
    rms_norm_eps: float = 1e-6
    rope_theta: float = 1_000_000.0
    tie_word_embeddings: bool = False


class DecoderLayer(nn.Module):
    """One pre-norm transformer layer: `x -> x + attn(norm(x)) -> h + mlp(norm(h))`.

    "Pre-norm" means the normalisation sits *inside* each branch, in front of the
    sub-block, and never on the residual stream itself (chapter 05): whatever the layer
    adds, the highway carrying `x` from the embedding to the LM head stays untouched.
    """

    def __init__(self, cfg: DecoderConfig) -> None:
        super().__init__()
        self.input_layernorm = RMSNorm(cfg.d_model, eps=cfg.rms_norm_eps)
        self.self_attn = GroupedQueryAttention(
            d_model=cfg.d_model,
            n_heads=cfg.n_heads,
            n_kv_heads=cfg.n_kv_heads,
            head_dim=cfg.head_dim,
            qk_norm=True,
            gated=False,
            eps=cfg.rms_norm_eps,
            bias=False,
        )
        self.post_attention_layernorm = RMSNorm(cfg.d_model, eps=cfg.rms_norm_eps)
        self.mlp = SwiGLUMLP(cfg.d_model, cfg.d_ff)

    def forward(self, x: Tensor, cos: Tensor, sin: Tensor, cache: KVCache | None = None) -> Tensor:
        attn_out, _ = self.self_attn(
            self.input_layernorm(x), causal=True, cache=cache, rope=lambda t: apply_rope(t, cos, sin)
        )
        h = x + attn_out
        return h + self.mlp(self.post_attention_layernorm(h))


class Decoder(nn.Module):
    """Embedding -> N `DecoderLayer`s -> final RMSNorm -> LM head. That is a whole LLM.

    `tie_word_embeddings` reuses the embedding matrix, transposed, as the output layer
    (chapter 02): small models do this because the two matrices would otherwise be the
    single largest cost (for Qwen3-0.6B: 151936 x 1024 = 156M weights, more than a quarter
    of the model), large ones untie them because they can afford it.
    """

    def __init__(self, cfg: DecoderConfig) -> None:
        super().__init__()
        self.cfg = cfg
        self.embed_tokens = Embedding(cfg.vocab_size, cfg.d_model)
        self.layers = nn.ModuleList(DecoderLayer(cfg) for _ in range(cfg.n_layers))
        self.norm = RMSNorm(cfg.d_model, eps=cfg.rms_norm_eps)
        self.lm_head: nn.Module = (
            TiedLMHead(self.embed_tokens)
            if cfg.tie_word_embeddings
            else nn.Linear(cfg.d_model, cfg.vocab_size, bias=False)
        )

    def forward(self, ids: Tensor, caches: list[KVCache] | None = None) -> Tensor:
        """`(B, T)` token ids -> `(B, T, vocab)` logits."""
        h = self.embed_tokens(ids)
        past = 0 if caches is None else len(caches[0])
        cos, sin = rope_cos_sin(past + ids.shape[1], self.cfg.head_dim, theta=self.cfg.rope_theta)
        cos, sin = cos[past:].to(h.dtype), sin[past:].to(h.dtype)
        for i, layer in enumerate(self.layers):
            h = layer(h, cos, sin, cache=None if caches is None else caches[i])
        return self.lm_head(self.norm(h))

    def new_caches(self) -> list[KVCache]:
        """One KV cache per layer, for step-by-step decoding."""
        return [KVCache() for _ in range(self.cfg.n_layers)]


# ---------------------------------------------------------------------------
# 2. Loading real Qwen3 weights into our stack
# ---------------------------------------------------------------------------


def decoder_config_from_hf(hf_config) -> DecoderConfig:
    """Translate a `transformers` `Qwen3Config` into our `DecoderConfig`.

    The only non-obvious field is the RoPE base: transformers 5.16 keeps it in the
    `rope_parameters` dict (`config.rope_parameters["rope_theta"]`) rather than as a
    top-level `rope_theta` attribute.
    """
    head_dim = getattr(hf_config, "head_dim", None) or (
        hf_config.hidden_size // hf_config.num_attention_heads
    )
    rope = getattr(hf_config, "rope_parameters", None) or {}
    theta = rope.get("rope_theta", getattr(hf_config, "rope_theta", 10000.0))
    return DecoderConfig(
        vocab_size=hf_config.vocab_size,
        d_model=hf_config.hidden_size,
        n_layers=hf_config.num_hidden_layers,
        n_heads=hf_config.num_attention_heads,
        n_kv_heads=hf_config.num_key_value_heads,
        head_dim=head_dim,
        d_ff=hf_config.intermediate_size,
        rms_norm_eps=hf_config.rms_norm_eps,
        rope_theta=float(theta),
        tie_word_embeddings=bool(hf_config.tie_word_embeddings),
    )


#: Our parameter name  <-  Hugging Face parameter name, `{i}` = layer index.
WEIGHT_MAP: dict[str, str] = {
    "embed_tokens.weight": "model.embed_tokens.weight",
    "layers.{i}.input_layernorm.weight": "model.layers.{i}.input_layernorm.weight",
    "layers.{i}.self_attn.q_proj.weight": "model.layers.{i}.self_attn.q_proj.weight",
    "layers.{i}.self_attn.k_proj.weight": "model.layers.{i}.self_attn.k_proj.weight",
    "layers.{i}.self_attn.v_proj.weight": "model.layers.{i}.self_attn.v_proj.weight",
    "layers.{i}.self_attn.o_proj.weight": "model.layers.{i}.self_attn.o_proj.weight",
    "layers.{i}.self_attn.q_norm.weight": "model.layers.{i}.self_attn.q_norm.weight",
    "layers.{i}.self_attn.k_norm.weight": "model.layers.{i}.self_attn.k_norm.weight",
    "layers.{i}.post_attention_layernorm.weight": "model.layers.{i}.post_attention_layernorm.weight",
    "layers.{i}.mlp.gate_proj.weight": "model.layers.{i}.mlp.gate_proj.weight",
    "layers.{i}.mlp.up_proj.weight": "model.layers.{i}.mlp.up_proj.weight",
    "layers.{i}.mlp.down_proj.weight": "model.layers.{i}.mlp.down_proj.weight",
    "norm.weight": "model.norm.weight",
    "lm_head.weight": "lm_head.weight",
}


def load_qwen3_weights(decoder: Decoder, hf_model) -> Decoder:
    """Copy every weight of a `Qwen3ForCausalLM` into our `Decoder`, in place.

    This is the whole "porting a model" job: it is a rename table, not a conversion.
    Every tensor is copied bit-for-bit with no transpose and no reshape, because our
    blocks were written with the same shape conventions as `transformers`
    (`nn.Linear` stores `(out_features, in_features)`, RMSNorm has one gain per channel,
    the embedding matrix is `(vocab, d_model)`).
    """
    src = dict(hf_model.state_dict())
    n_layers = decoder.cfg.n_layers
    pairs: list[tuple[str, str]] = []
    for ours, theirs in WEIGHT_MAP.items():
        if ours == "lm_head.weight" and decoder.cfg.tie_word_embeddings:
            continue  # tied: the LM head *is* the embedding matrix, nothing to copy
        if "{i}" in ours:
            pairs += [(ours.format(i=i), theirs.format(i=i)) for i in range(n_layers)]
        else:
            pairs.append((ours, theirs))

    dst = dict(decoder.named_parameters())
    with torch.no_grad():
        for ours, theirs in pairs:
            if theirs not in src:
                raise KeyError(f"{theirs} missing from the checkpoint (have {len(src)} tensors)")
            if ours not in dst:
                raise KeyError(f"{ours} missing from our decoder")
            if dst[ours].shape != src[theirs].shape:
                raise ValueError(f"shape mismatch {ours} {tuple(dst[ours].shape)} "
                                 f"vs {theirs} {tuple(src[theirs].shape)}")
            dst[ours].copy_(src[theirs].to(dst[ours].dtype))

    copied = {p for _, p in pairs}
    ignored = {"rotary_emb.inv_freq"}  # a buffer, recomputed by rope_cos_sin
    leftover = [k for k in src if k not in copied and not any(k.endswith(s) for s in ignored)]
    if decoder.cfg.tie_word_embeddings:
        leftover = [k for k in leftover if k != "lm_head.weight"]
    if leftover:
        raise KeyError(f"checkpoint tensors nobody claimed: {leftover[:5]}")
    return decoder


def decoder_from_pretrained(model_id: str = QWEN3_06B_ID):
    """`(tokenizer, hf_model, our_decoder)` for a real dense Qwen3 checkpoint (downloads once)."""
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    hf_model = AutoModelForCausalLM.from_pretrained(model_id, dtype=torch.float32)
    hf_model.eval()
    ours = Decoder(decoder_config_from_hf(hf_model.config))
    load_qwen3_weights(ours, hf_model)
    ours.eval()
    return tokenizer, hf_model, ours


@torch.no_grad()
def greedy_decode(model, prompt_ids: Tensor, n_new: int) -> list[int]:
    """`n_new` greedy tokens from our `Decoder` or from a `transformers` model.

    Deliberately the dumbest possible loop (re-run the whole prefix every step, no cache):
    the point of this chapter is that the two models agree, and a cache would add a second
    thing that could disagree. Chapter 03 has the cached version.
    """
    ids = prompt_ids.clone()
    out: list[int] = []
    for _ in range(n_new):
        logits = model(ids)
        logits = logits.logits if hasattr(logits, "logits") else logits
        next_id = int(logits[0, -1].argmax())
        out.append(next_id)
        ids = torch.cat([ids, torch.tensor([[next_id]], dtype=ids.dtype)], dim=1)
    return out


# ---------------------------------------------------------------------------
# 3. Counting: parameters and FLOPs per block type
# ---------------------------------------------------------------------------


def count_params_and_flops(config, seq: int = 1024) -> dict:
    """Parameters and forward FLOPs *per generated token* per block type.

    Parameters come from chapter 06's `param_breakdown` (a meta-device model tree, so a
    27B config costs no memory). FLOPs use the one rule that matters: a weight matrix is
    used once per token, in one multiply and one add, so **a matmul costs 2 FLOPs per
    weight per token** — the "forward ≈ 2·N" rule of thumb. The only term that is *not*
    proportional to a weight count is the attention score/value pair, which touches every
    key in the context and therefore grows with `seq`:

        4 * n_heads * head_dim * seq   FLOPs per token per full-attention layer

    (2 for `q @ k^T`, 2 for `weights @ v`.) That single term is why a long context makes
    attention's share of the compute grow while everything else stays flat.
    """
    params = param_breakdown(config)
    head_dim = getattr(config, "head_dim", None) or (
        config.hidden_size // config.num_attention_heads
    )
    layer_types = getattr(config, "layer_types", None) or ["full_attention"] * config.num_hidden_layers
    n_attn_layers = sum(1 for t in layer_types if "attention" in t and "linear" not in t)

    flops = {k: 2 * v for k, v in params.items()}
    flops["embeddings"] = 0  # reading a row of a table is a lookup, not arithmetic
    flops["attention scores"] = 4 * n_attn_layers * config.num_attention_heads * head_dim * seq
    return {
        "params": params,
        "flops": flops,
        "seq": seq,
        "n_layers": config.num_hidden_layers,
        "n_attention_layers": n_attn_layers,
        "total_params": sum(params.values()),
        "total_flops": sum(flops.values()),
    }


def bytes_per_weight_table(total_params: int) -> dict[str, float]:
    """Gigabytes of weights at the precisions a model card quotes."""
    return {"fp32 (4 bytes)": total_params * 4 / 1e9,
            "bf16 (2 bytes)": total_params * 2 / 1e9,
            "int8 (1 byte)": total_params * 1 / 1e9,
            "4-bit (0.5 byte + scales)": total_params * 0.55 / 1e9}


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------

_C_NORM = "#cfd8dc"
_C_MIX = "#90caf9"
_C_MLP = "#a5d6a7"
_C_ADD = "#ffe082"


def _box(ax, x, y, w, h, label, color, fontsize=8):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=color, edgecolor="black", lw=1.0))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fontsize)


def _arrow(ax, x1, y1, x2, y2, style_="-|>", color="black"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style_, mutation_scale=11,
                                 color=color, lw=1.1, shrinkA=0, shrinkB=0))


def _draw_layer(ax, cfg: dict, kind: str) -> None:
    """Draw one Qwen3.5/3.8 layer: `kind` is 'attention' or 'deltanet'."""
    d, ff = cfg["hidden"], cfg["ff"]
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 10)
    ax.axis("off")

    # The residual stream: one vertical line the whole layer hangs off.
    ax.plot([0.9, 0.9], [0.3, 9.7], color="#546e7a", lw=2.5, zorder=0)
    ax.text(0.9, 0.05, f"residual stream (B, T, {d})", ha="center", fontsize=8, color="#546e7a")

    if kind == "attention":
        title = f"Gated Attention   ({cfg['n_attn']} of {cfg['n_layers']} layers)"
        rows = [
            (f"q/k/v_proj: {d} -> {cfg['heads']}x{cfg['head_dim']} (Q) and "
             f"{cfg['kv_heads']}x{cfg['head_dim']} (K, V)  — GQA"),
            f"QK-norm: RMSNorm over each {cfg['head_dim']}-dim head",
            (f"partial RoPE on the first {int(cfg['head_dim'] * cfg['rotary'])} of "
             f"{cfg['head_dim']} dims ({cfg['rotary']:.2f})"),
            f"softmax(QK^T / sqrt({cfg['head_dim']})) @ V  — grows with context length",
            f"sigmoid(gate_proj(x)) * out, then o_proj: {cfg['heads']}x{cfg['head_dim']} -> {d}",
        ]
        color = _C_MIX
    else:
        title = f"Gated DeltaNet   ({cfg['n_layers'] - cfg['n_attn']} of {cfg['n_layers']} layers)"
        rows = [
            (f"q/k/v + beta + alpha proj: {d} -> "
             f"{cfg['lin_qk_heads']}x{cfg['lin_head_dim']} (Q, K), "
             f"{cfg['lin_v_heads']}x{cfg['lin_head_dim']} (V)"),
            f"short causal conv (kernel {cfg['conv']}), then L2-normalise q and k",
            (f"gated delta rule on a fixed state S: {cfg['lin_v_heads']} x "
             f"{cfg['lin_head_dim']}x{cfg['lin_head_dim']} numbers"),
            "no positions and no KV cache — the state size never grows",
            (f"RMSNormGated(out, gate), then o_proj: "
             f"{cfg['lin_v_heads']}x{cfg['lin_head_dim']} -> {d}"),
        ]
        color = "#ce93d8"

    mlp_rows = [
        f"gate_proj, up_proj: {d} -> {ff}   (two matrices, read the same input)",
        "silu(gate(x)) * up(x)  — a per-feature volume knob",
        f"down_proj: {ff} -> {d}",
        f"{3 * d * ff / 1e6:.0f}M weights: the biggest block in the layer",
    ]

    branches = [(title, rows, color, 9.25, 8.7, 2.9, 4.9),
                ("SwiGLU MLP", mlp_rows, _C_MLP, 4.35, 3.8, 2.4, 0.5)]
    for name, body, col, y_in, y_norm, mix_h, y_add in branches:
        y_mix = y_norm - 0.45 - mix_h
        _arrow(ax, 0.9, y_in, 2.5, y_in)
        ax.text(1.7, y_in + 0.12, "x", fontsize=8, ha="center", color="#546e7a")
        _box(ax, 2.5, y_norm, 7.7, 0.55, f"RMSNorm ({d}), eps 1e-6", _C_NORM)
        _arrow(ax, 6.35, y_norm, 6.35, y_norm - 0.45)
        ax.add_patch(Rectangle((2.5, y_mix), 7.7, mix_h, facecolor=col, edgecolor="black", lw=1.0))
        ax.text(6.35, y_mix + mix_h - 0.28, name, ha="center", fontsize=9, weight="bold")
        for j, row in enumerate(body):
            ax.text(2.75, y_mix + mix_h - 0.72 - 0.4 * j, "- " + row, fontsize=7, va="center")
        _arrow(ax, 6.35, y_mix, 6.35, y_add)
        _arrow(ax, 6.35, y_add, 1.25, y_add)
        ax.add_patch(plt.Circle((0.9, y_add), 0.16, facecolor=_C_ADD, edgecolor="black", zorder=3))
        ax.text(0.9, y_add, "+", ha="center", va="center", fontsize=9, zorder=4)
    ax.set_title(title.split("   (")[0] + " layer", fontsize=11)


def _qwen35_shapes() -> dict:
    config = load_text_config(QWEN38_27B_ID)
    layer_types = list(getattr(config, "layer_types", []))
    return {
        "hidden": config.hidden_size,
        "ff": config.intermediate_size,
        "heads": config.num_attention_heads,
        "kv_heads": config.num_key_value_heads,
        "head_dim": config.head_dim,
        "rotary": getattr(config, "partial_rotary_factor", 0.25),
        "n_layers": config.num_hidden_layers,
        "n_attn": sum(1 for t in layer_types if t == "full_attention"),
        "lin_qk_heads": getattr(config, "linear_num_key_heads", 16),
        "lin_v_heads": getattr(config, "linear_num_value_heads", 48),
        "lin_head_dim": getattr(config, "linear_key_head_dim", 128),
        "conv": getattr(config, "linear_conv_kernel_dim", 4),
    }


def _fig_layer_diagram() -> str:
    style()
    cfg = _qwen35_shapes()
    fig, axes = plt.subplots(1, 2, figsize=(15, 6.5))
    _draw_layer(axes[0], cfg, "deltanet")
    _draw_layer(axes[1], cfg, "attention")
    fig.suptitle(
        f"One Qwen3.8-27B layer, both variants (shapes for hidden={cfg['hidden']}, "
        f"{cfg['n_layers']} layers, 3 DeltaNet : 1 attention)",
        fontsize=11,
    )
    return str(save(fig, "10_layer_diagram"))


_BUCKET_ORDER = ["embeddings", "attention", "deltanet", "mlp", "norms", "lm_head", "other"]
_BUCKET_COLORS = {"embeddings": "#90a4ae", "attention": "#1f77b4", "deltanet": "#9467bd",
                  "mlp": "#2ca02c", "norms": "#ffbb78", "lm_head": "#d62728", "other": "#8c564b"}


def _fig_param_breakdown() -> str:
    style()
    models = [("Qwen3-0.6B\n(dense, tied)", QWEN3_06B_ID),
              ("Qwen3.5-0.8B\n(hybrid, tied)", QWEN35_08B_ID),
              ("Qwen3.8-27B\n(hybrid, untied)", QWEN38_27B_ID)]
    fig, ax = plt.subplots(figsize=(10, 5))
    labels, totals = [], []
    for x, (label, model_id) in enumerate(models):
        buckets = param_breakdown(load_text_config(model_id))
        total = sum(buckets.values())
        labels.append(label)
        totals.append(total)
        bottom = 0.0
        for name in _BUCKET_ORDER:
            share = buckets.get(name, 0) / total * 100
            if share <= 0:
                continue
            ax.bar(x, share, bottom=bottom, color=_BUCKET_COLORS[name], width=0.55,
                   label=name if x == 0 or name not in ax.get_legend_handles_labels()[1] else None)
            if share > 4:
                ax.text(x, bottom + share / 2, f"{name}\n{share:.0f}%", ha="center", va="center",
                        fontsize=8)
            bottom += share
        ax.text(x, 102, f"{total / 1e9:.2f}B params", ha="center", fontsize=9)
    ax.set_xticks(range(len(models)))
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 110)
    ax.set_ylabel("share of all parameters (%)")
    ax.set_title("Where the weights live. The MLP is the model; attention is the cheap part.")
    ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=8)
    ax.grid(axis="x", visible=False)
    return str(save(fig, "10_param_breakdown"))


def _fig_flops_breakdown() -> str:
    style()
    config = load_text_config(QWEN38_27B_ID)
    contexts = [1024, 70000]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
    for ax, seq in zip(axes, contexts):
        counts = count_params_and_flops(config, seq=seq)
        flops = counts["flops"]
        items = [(k, v) for k, v in flops.items() if v > 0]
        items.sort(key=lambda kv: -kv[1])
        total = sum(v for _, v in items)
        names = [k for k, _ in items]
        vals = [v / total * 100 for _, v in items]
        colors = [_BUCKET_COLORS.get(n, "#ff7f0e") for n in names]
        ax.barh(names[::-1], vals[::-1], color=colors[::-1])
        for y, v in enumerate(vals[::-1]):
            ax.text(v + 1, y, f"{v:.1f}%", va="center", fontsize=8)
        ax.set_xlim(0, 100)
        ax.set_xlabel("share of forward FLOPs per token (%)")
        ax.set_title(f"context {seq:,} tokens\ntotal {total / 1e9:.1f} GFLOP/token".replace(",", " "),
                     fontsize=10)
    fig.suptitle("Qwen3.8-27B: what the GPU actually multiplies, per generated token",
                 fontsize=11, y=1.06)
    return str(save(fig, "10_flops_breakdown"))


_MAP_ROWS = [
    ("tokens, embeddings, softmax", "02", "02 tokenizer & data, 03 model from scratch"),
    ("attention, GQA, KV cache", "03", "01 concepts, 04 pre-training (memory)"),
    ("RoPE, partial RoPE", "04", "01 concepts, 07 export (num_ctx)"),
    ("RMSNorm, residuals", "05", "03 model from scratch, 04 pre-training (stability)"),
    ("SwiGLU MLP, MoE", "06", "01 concepts, 09 domain fine-tuning (LoRA targets)"),
    ("Gated DeltaNet, hybrid stack", "07", "03 model from scratch, 04 pre-training"),
    ("sampling, perplexity", "08", "05 SFT, 07 export to Ollama, 08 evaluation"),
    ("optimisers, schedules, bf16", "09", "04 pre-training, 06 DPO/GRPO"),
    ("the assembled decoder", "10", "03–10: this is the object every stage trains"),
]


def _fig_tutorial_map() -> str:
    style()
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, len(_MAP_ROWS) + 1.6)
    ax.axis("off")
    ax.text(1.6, len(_MAP_ROWS) + 1.0, "block", fontsize=10, weight="bold", ha="center")
    ax.text(4.4, len(_MAP_ROWS) + 1.0, "llm_blocks\nchapter", fontsize=10, weight="bold", ha="center")
    ax.text(8.6, len(_MAP_ROWS) + 1.0, "used in ../llm_training/", fontsize=10, weight="bold",
            ha="center")
    for j, (block, chapter, usage) in enumerate(_MAP_ROWS):
        y = len(_MAP_ROWS) - j - 0.3
        _box(ax, 0.1, y, 3.0, 0.62, block, _C_MLP if j < 8 else _C_ADD, fontsize=8)
        _box(ax, 3.9, y, 1.0, 0.62, chapter, _C_NORM, fontsize=9)
        _box(ax, 5.7, y, 5.9, 0.62, usage, _C_MIX, fontsize=8)
        _arrow(ax, 3.1, y + 0.31, 3.9, y + 0.31)
        _arrow(ax, 4.9, y + 0.31, 5.7, y + 0.31)
    ax.set_title("Every block you built here, and the chapter of ../llm_training/ that uses it",
                 fontsize=11)
    return str(save(fig, "10_tutorial_map"))


# ---------------------------------------------------------------------------
# Real-model figures and text (downloads)
# ---------------------------------------------------------------------------

REAL_PROMPT = (
    "The capital of France is Paris, and the capital of Italy is Rome. "
    "Large language models predict the next token of a sequence, one token at a time."
)


def _fig_real_match() -> str:
    style()
    tokenizer, hf_model, ours = decoder_from_pretrained(QWEN3_06B_ID)
    ids = tokenizer(REAL_PROMPT, return_tensors="pt").input_ids[:, :30]
    with torch.no_grad():
        ref = hf_model(ids).logits
        got = ours(ids)
    delta = (ref - got).abs().amax(dim=-1)[0].numpy()
    scale = ref.abs().amax().item()

    fig, ax = plt.subplots(figsize=(9, 4.2))
    ax.plot(delta, marker="o", ms=3.5)
    ax.set_yscale("log")
    ax.set_xlabel("position in the 30-token prompt")
    ax.set_ylabel("max |our logit - transformers logit|")
    ax.set_title(
        f"Qwen3-0.6B: our blocks vs transformers, fp32\n"
        f"largest difference {delta.max():.2e} on logits up to {scale:.1f} "
        f"(relative {delta.max() / scale:.1e}) — floating-point noise, not a bug"
    )
    ax.axhline(1e-4, color="#d62728", ls="--", lw=1, label="1e-4 (the test tolerance)")
    ax.legend(fontsize=8)
    return str(save(fig, "10_real_match"))


def _real_generation_report() -> str:
    tokenizer, hf_model, ours = decoder_from_pretrained(QWEN3_06B_ID)
    prompt = "The capital of France is"
    ids = tokenizer(prompt, return_tensors="pt").input_ids
    theirs_ids = greedy_decode(hf_model, ids, 20)
    ours_ids = greedy_decode(ours, ids, 20)
    lines = [
        f"model:  {QWEN3_06B_ID} (fp32, CPU), 20 greedy tokens",
        f"prompt: {prompt!r}",
        "",
        f"transformers ids: {theirs_ids}",
        f"our decoder  ids: {ours_ids}",
        f"identical:        {theirs_ids == ours_ids}",
        "",
        f"transformers text: {(prompt + tokenizer.decode(theirs_ids))!r}",
        f"our decoder text : {(prompt + tokenizer.decode(ours_ids))!r}",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


TINY_HF_KWARGS = {
    "vocab_size": 128,
    "hidden_size": 64,
    "intermediate_size": 128,
    "num_hidden_layers": 2,
    "num_attention_heads": 4,
    "num_key_value_heads": 2,
    "head_dim": 16,
    "tie_word_embeddings": False,
}


def tiny_pair(seed: int = 0):
    """A random tiny `Qwen3ForCausalLM` and our `Decoder` holding the same weights."""
    from transformers.models.qwen3 import Qwen3Config
    from transformers.models.qwen3.modeling_qwen3 import Qwen3ForCausalLM

    torch.manual_seed(seed)
    config = Qwen3Config(**TINY_HF_KWARGS)
    hf_model = Qwen3ForCausalLM(config).eval()
    ours = Decoder(decoder_config_from_hf(config))
    load_qwen3_weights(ours, hf_model)
    ours.eval()
    return config, hf_model, ours


@app.command()
def plots() -> None:
    """Draw every figure of chapter 10 (config downloads only, no weights)."""
    for path in (_fig_layer_diagram(), _fig_param_breakdown(), _fig_flops_breakdown(),
                 _fig_tutorial_map()):
        print("wrote", path)


@app.command(name="plots-real")
def plots_real() -> None:
    """Draw the Qwen3-0.6B logit-match figure (downloads 1.2 GB once)."""
    print("wrote", _fig_real_match())


@app.command(name="demo-real")
def demo_real() -> None:
    """Greedy-decode the same prompt with both models and save the transcript."""
    report = _real_generation_report()
    print(report)
    path = ASSETS / "10_real_generation.txt"
    path.write_text(report + "\n")
    print("\nwrote", path)


@app.command()
def demo() -> None:
    """Tiny-model equivalence, then the parameter/FLOP arithmetic quoted in the chapter."""
    _, hf_model, ours = tiny_pair()
    torch.manual_seed(1)
    ids = torch.randint(0, TINY_HF_KWARGS["vocab_size"], (2, 12))
    with torch.no_grad():
        ref = hf_model(ids).logits
        got = ours(ids)
    print("tiny random Qwen3 (2 layers, hidden 64, 4 heads / 2 KV heads, head dim 16, vocab 128)")
    print(f"  max |delta logit|          {(ref - got).abs().max().item():.3e}")
    print(f"  logit scale                {ref.abs().max().item():.3f}")
    theirs = greedy_decode(hf_model, ids[:1, :4], 10)
    mine = greedy_decode(ours, ids[:1, :4], 10)
    print(f"  10 greedy tokens, theirs   {theirs}")
    print(f"  10 greedy tokens, ours     {mine}")
    print(f"  identical                  {theirs == mine}")
    print(f"  our parameters             {sum(p.numel() for p in ours.parameters()):,}")
    print(f"  their parameters           {sum(p.numel() for p in hf_model.parameters()):,}")

    print("\nQwen3.8-27B, per generated token:")
    config = load_text_config(QWEN38_27B_ID)
    for seq in (1024, 70000):
        counts = count_params_and_flops(config, seq=seq)
        n = counts["total_params"]
        attn = counts["flops"]["attention scores"] / counts["total_flops"] * 100
        print(f"  context {seq:>6}: {counts['total_flops'] / 1e9:7.1f} GFLOP/token "
              f"(2N = {2 * n / 1e9:.1f}), attention scores {attn:5.1f}% of it")
    counts = count_params_and_flops(config, seq=1024)
    n = counts["total_params"]
    print(f"  parameters                 {n:,} ({n / 1e9:.2f}B)")
    for name, gb in bytes_per_weight_table(n).items():
        print(f"    {name:<26} {gb:6.1f} GB")
    print(f"  training on D tokens       6*N*D FLOPs; D = 36e12 -> {6 * n * 36e12:.2e} FLOPs")


if __name__ == "__main__":
    app()
