"""Chapter 02 — tokens, embeddings, softmax, tied LM head.

`uv run python -m llm_blocks.ch02_tokens_embeddings plots` draws the four figures that
need no downloads; `plots-real` draws the three figures/files that use the small
SmolLM2-135M model (downloaded once, cached); `demo` prints the numbers quoted in the
chapter.
"""

from __future__ import annotations

import math

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn.functional as F
import typer
from sklearn.decomposition import PCA
from torch import Tensor, nn

from llm_blocks import plotting
from llm_blocks.plotting import annotate_arrow, save, style
from llm_blocks.reference import load_smollm

app = typer.Typer(add_completion=False, no_args_is_help=False)


# ---------------------------------------------------------------------------
# From-scratch building blocks
# ---------------------------------------------------------------------------


class Embedding(nn.Module):
    """Token id -> vector: a lookup into a `(vocab_size, dim)` matrix `E`.

    Row `i` of `E` *is* the learned vector for token id `i` — "looking up" a token
    is nothing more than reading one row out of a matrix.
    """

    def __init__(self, vocab_size: int, dim: int) -> None:
        super().__init__()
        self.weight = nn.Parameter(torch.randn(vocab_size, dim) * 0.02)

    def forward(self, ids: Tensor) -> Tensor:
        return self.weight[ids]

    def one_hot_lookup(self, ids: Tensor) -> Tensor:
        """Same result as `forward`, computed as `one_hot(ids) @ E` — the lookup *is* a matmul."""
        one_hot = F.one_hot(ids, num_classes=self.weight.shape[0]).to(self.weight.dtype)
        return one_hot @ self.weight


def softmax(x: Tensor, temperature: float = 1.0) -> Tensor:
    """`softmax(x / temperature)` along the last dim, with the max-subtraction trick.

    Subtracting the row max before `exp` does not change the result (it cancels in the
    ratio) but keeps the largest exponent at `exp(0) = 1` instead of risking `exp(large)`
    overflowing to `inf`.
    """
    z = x / temperature
    z = z - z.max(dim=-1, keepdim=True).values
    exp_z = torch.exp(z)
    return exp_z / exp_z.sum(dim=-1, keepdim=True)


def cross_entropy(logits: Tensor, targets: Tensor) -> Tensor:
    """Mean `-log p(target)` over the batch, computed via log-softmax for stability.

    Working in log-space avoids ever computing `softmax` itself (which could underflow
    to exactly 0.0 for a very wrong prediction, turning `log(0)` into `-inf`).
    """
    z = logits - logits.max(dim=-1, keepdim=True).values
    log_probs = z - torch.log(torch.exp(z).sum(dim=-1, keepdim=True))
    picked = log_probs.gather(-1, targets.unsqueeze(-1)).squeeze(-1)
    return -picked.mean()


class TiedLMHead(nn.Module):
    """The reverse lookup: `logits = h @ E.T`, reusing the embedding matrix `E`.

    No new parameters are introduced — the same table that turns token ids into
    vectors is reused, transposed, to turn a hidden vector back into one score per
    vocabulary entry.
    """

    def __init__(self, embedding: Embedding) -> None:
        super().__init__()
        self.embedding = embedding

    def forward(self, h: Tensor) -> Tensor:
        return h @ self.embedding.weight.T


# ---------------------------------------------------------------------------
# Numbers quoted in the chapter
# ---------------------------------------------------------------------------

VOCAB_HIDDEN_PAIRS = [
    (32_000, 768),
    (151_936, 768),
    (248_320, 768),
    (32_000, 5120),
    (151_936, 5120),
    (248_320, 5120),
]


# ---------------------------------------------------------------------------
# Figures (no downloads)
# ---------------------------------------------------------------------------


def _fig_one_hot_lookup():
    style()
    vocab_size, dim, token_id = 4, 3, 2
    torch.manual_seed(0)
    emb = Embedding(vocab_size, dim)

    fig, (ax_pic, ax_text) = plt.subplots(1, 2, figsize=(11, 4.5), gridspec_kw={"width_ratios": [1.3, 1]})

    cell = 0.8
    # one-hot row vector for token_id (one cell per vocabulary entry)
    for i in range(vocab_size):
        is_hot = i == token_id
        rect = plt.Rectangle(
            (i * cell, 2 * cell), cell, cell, facecolor="#d62728" if is_hot else "#cccccc", alpha=0.6, edgecolor="k"
        )
        ax_pic.add_patch(rect)
        ax_pic.text(i * cell + cell / 2, 2 * cell + cell / 2, "1" if is_hot else "0", ha="center", va="center")
    ax_pic.text(-0.6, 2 * cell + cell / 2, f"one-hot(id={token_id})", ha="right", va="center")

    # embedding matrix E (vocab_size rows x dim columns), row token_id highlighted
    e = emb.weight.detach().numpy()
    for r in range(vocab_size):
        for c in range(dim):
            is_hot_row = r == token_id
            rect = plt.Rectangle(
                (c * cell, (0.7 - r) * cell),
                cell,
                cell,
                facecolor="#1f77b4" if is_hot_row else "#e8e8e8",
                alpha=0.7 if is_hot_row else 0.4,
                edgecolor="k",
            )
            ax_pic.add_patch(rect)
            ax_pic.text(c * cell + cell / 2, (0.7 - r) * cell + cell / 2, f"{e[r, c]:.2f}", ha="center", va="center", fontsize=8)
    ax_pic.text(-0.6, (0.7 - (vocab_size - 1) / 2) * cell, f"E ({vocab_size}x{dim})", ha="right", va="center")

    row = e[token_id]
    for c in range(dim):
        rect = plt.Rectangle((c * cell, -3.3 * cell), cell, cell, facecolor="#d62728", alpha=0.6, edgecolor="k")
        ax_pic.add_patch(rect)
        ax_pic.text(c * cell + cell / 2, -3.3 * cell + cell / 2, f"{row[c]:.2f}", ha="center", va="center", fontsize=8)
    ax_pic.text(-0.6, -3.3 * cell + cell / 2, "row picked out", ha="right", va="center")

    ax_pic.set_xlim(-2.2, 3.2)
    ax_pic.set_ylim(-3.6, 3.2)
    ax_pic.axis("off")
    ax_pic.set_title("one_hot(id) @ E == E[id]")

    ours = emb(torch.tensor(token_id))
    via_one_hot = emb.one_hot_lookup(torch.tensor(token_id))
    ax_text.axis("off")
    ax_text.text(
        0.0,
        0.6,
        "E[id]            = "
        + np.array2string(ours.detach().numpy(), precision=3)
        + "\none_hot(id) @ E  = "
        + np.array2string(via_one_hot.detach().numpy(), precision=3),
        fontsize=9,
        family="monospace",
        va="center",
    )
    ax_text.text(
        0.0,
        0.2,
        "Indexing a matrix and multiplying by a one-hot vector give the\n"
        "exact same row: `Embedding` is a matmul in disguise, just done\n"
        "by direct indexing because it is much faster than a real matmul\n"
        "against a mostly-zero vector.",
        fontsize=10,
        va="center",
    )
    return save(fig, "02_one_hot_lookup")


def _fig_softmax_temperature():
    style()
    logits = torch.tensor([2.0, 1.0, 0.1, -1.0, 0.5])
    temperatures = [0.3, 1.0, 3.0]
    labels = [f"token {i}" for i in range(len(logits))]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    width = 0.25
    x = np.arange(len(logits))
    for i, temp in enumerate(temperatures):
        probs = softmax(logits, temperature=temp).numpy()
        ax.bar(x + (i - 1) * width, probs, width=width, label=f"T={temp}")

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("probability")
    ax.set_title("02 — same logits, softmax at three temperatures")
    ax.legend()
    annotate_arrow(
        ax,
        "low T: sharper, more confident",
        xy=(0 - width, softmax(logits, temperature=0.3)[0].item()),
        xytext=(0.6, 0.85),
    )
    annotate_arrow(
        ax,
        "high T: flatter, closer to uniform",
        xy=(0 + width, softmax(logits, temperature=3.0)[0].item()),
        xytext=(2.2, 0.55),
    )
    return save(fig, "02_softmax_temperature")


def _fig_cross_entropy():
    style()
    p = np.logspace(-4, 0, 300, endpoint=False)
    loss = -np.log(p)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(p, loss, color="#1f77b4")
    ax.set_xscale("log")
    ax.set_xlabel("predicted probability of the correct token (log scale)")
    ax.set_ylabel("cross-entropy loss = -log(p)")
    ax.set_title("02 — cross-entropy: confident and wrong is punished hardest")

    for vocab, color in [(32_000, "#2ca02c"), (248_320, "#d62728")]:
        uniform_loss = math.log(vocab)
        ax.axhline(uniform_loss, color=color, linestyle="--", linewidth=1)
        ax.text(
            1.5e-4,
            uniform_loss + 0.3,
            f"ln({vocab:,}) = {uniform_loss:.2f} (uniform random guess)",
            color=color,
            fontsize=8,
        )

    annotate_arrow(
        ax,
        "p -> 1: loss -> 0, the model was confident and right",
        xy=(0.9, -np.log(0.9)),
        xytext=(0.08, 6.5),
    )
    annotate_arrow(
        ax,
        "p -> 0: loss explodes, confident and wrong",
        xy=(2e-4, -np.log(2e-4)),
        xytext=(3e-3, 3.5),
    )
    return save(fig, "02_cross_entropy")


def _fig_embedding_size():
    style()
    vocab = np.logspace(np.log10(1_000), np.log10(300_000), 200)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    for hidden, color in [(768, "#1f77b4"), (5120, "#d62728")]:
        params = vocab * hidden
        ax.plot(vocab, params / 1e6, color=color, label=f"hidden={hidden}")

    for v in (32_000, 151_936, 248_320):
        for hidden, color in [(768, "#1f77b4"), (5120, "#d62728")]:
            params = v * hidden
            ax.plot(v, params / 1e6, "o", color=color, markersize=5)
        ax.axvline(v, color="grey", linestyle=":", linewidth=0.8)

    ax.set_xscale("log")
    ax.set_xlabel("vocabulary size (log scale)")
    ax.set_ylabel("embedding parameters (millions)")
    ax.set_title("02 — embedding-table size = vocab_size x hidden_size")
    ymin, ymax = ax.get_ylim()
    for v in (32_000, 151_936, 248_320):
        ax.text(v, ymin + 0.02 * (ymax - ymin), f"{v:,}", rotation=90, fontsize=7, ha="right", va="bottom")
    ax.legend()
    return save(fig, "02_embedding_size")


# ---------------------------------------------------------------------------
# Figures that need the small real model (downloads once)
# ---------------------------------------------------------------------------

_TOKEN_EXAMPLE_SENTENCE = "The antidisestablishmentarianism conference costs $1234.56 in 2024."

_PCA_GROUPS: dict[str, list[str]] = {
    "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    "months": [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ],
    "numbers": ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"],
    "countries": [
        "France",
        "Germany",
        "Japan",
        "Canada",
        "Brazil",
        "Egypt",
        "India",
        "Italy",
        "Spain",
        "China",
    ],
    "punctuation": [".", ",", "!", "?", ";", ":", "-", "'", '"', "(", ")"],
}

_NEIGHBOUR_WORDS = ["king", "Paris", "eight", "January", "happy"]


def _first_token_id(tokenizer, word: str) -> int:
    """The id of the first sub-token of ` {word}` (a leading space matches how the
    word normally appears mid-sentence in byte-level BPE tokenizers like SmolLM2's)."""
    ids = tokenizer.encode(" " + word, add_special_tokens=False)
    return ids[0]


def _fig_tokens_example():
    style()
    tokenizer, _ = load_smollm()
    ids = tokenizer.encode(_TOKEN_EXAMPLE_SENTENCE, add_special_tokens=False)
    pieces = [tokenizer.decode([i]) for i in ids]

    fig, ax = plt.subplots(figsize=(12, 2.6))
    colors = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd", "#ff7f0e", "#17becf"]
    x = 0.0
    for i, piece in enumerate(pieces):
        width = max(0.5, 0.22 * len(piece) + 0.3)
        rect = plt.Rectangle((x, 0), width, 1, facecolor=colors[i % len(colors)], alpha=0.55, edgecolor="k")
        ax.add_patch(rect)
        ax.text(x + width / 2, 0.5, piece.replace(" ", "␣"), ha="center", va="center", fontsize=8)
        x += width

    ax.set_xlim(0, x)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title(f"02 — SmolLM2 tokenizer splits one sentence into {len(pieces)} tokens ({'␣'} = a space)")
    return save(fig, "02_tokens_example")


def _fig_embeddings_pca():
    style()
    tokenizer, model = load_smollm()
    embed_weight = model.get_input_embeddings().weight.detach().numpy()

    vectors, group_names, labels = [], [], []
    for group, words in _PCA_GROUPS.items():
        for word in words:
            token_id = _first_token_id(tokenizer, word)
            vectors.append(embed_weight[token_id])
            group_names.append(group)
            labels.append(word)

    coords = PCA(n_components=2).fit_transform(np.stack(vectors))

    fig, ax = plt.subplots(figsize=(9, 7))
    colors = {"days": "#1f77b4", "months": "#d62728", "numbers": "#2ca02c", "countries": "#9467bd", "punctuation": "#ff7f0e"}
    for group in _PCA_GROUPS:
        mask = [g == group for g in group_names]
        ax.scatter(coords[mask, 0], coords[mask, 1], color=colors[group], label=group, s=30)

    for (x, y), label in zip(coords, labels):
        ax.annotate(label, (x, y), fontsize=6, alpha=0.8, xytext=(2, 2), textcoords="offset points")

    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    ax.set_title("02 — PCA of SmolLM2 input embeddings for ~60 hand-picked tokens")
    ax.legend()
    return save(fig, "02_embeddings_pca")


def _nearest_neighbours_report() -> str:
    tokenizer, model = load_smollm()
    embed_weight = model.get_input_embeddings().weight.detach()
    normed = F.normalize(embed_weight, dim=-1)

    lines = []
    for word in _NEIGHBOUR_WORDS:
        token_id = _first_token_id(tokenizer, word)
        sims = normed @ normed[token_id]
        top = torch.topk(sims, k=6)
        neighbours = [
            (tokenizer.decode([i]), sims[i].item()) for i in top.indices.tolist() if i != token_id
        ][:5]
        lines.append(f"'{word}' (id={token_id}) nearest neighbours:")
        for piece, sim in neighbours:
            lines.append(f"    {piece!r:15s} cos={sim:.3f}")
    return "\n".join(lines)


def _write_nearest_neighbours() -> str:
    report = _nearest_neighbours_report()
    plotting.ASSETS.mkdir(parents=True, exist_ok=True)
    path = plotting.ASSETS / "02_nearest_neighbours.txt"
    path.write_text(report + "\n")
    return str(path)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


@app.command()
def plots() -> None:
    """Regenerate every figure for this chapter that needs no download."""
    print(f"wrote: {_fig_one_hot_lookup()}")
    print(f"wrote: {_fig_softmax_temperature()}")
    print(f"wrote: {_fig_cross_entropy()}")
    print(f"wrote: {_fig_embedding_size()}")


@app.command(name="plots-real")
def plots_real() -> None:
    """Regenerate the figures/files that need the small real model (downloads once)."""
    print(f"wrote: {_fig_tokens_example()}")
    print(f"wrote: {_fig_embeddings_pca()}")
    print(f"wrote: {_write_nearest_neighbours()}")


@app.command()
def demo() -> None:
    """Print the numbers used in the chapter."""
    print("embedding-table parameters (vocab_size x hidden_size):")
    for vocab, hidden in VOCAB_HIDDEN_PAIRS:
        params = vocab * hidden
        print(f"  vocab={vocab:>7,}  hidden={hidden:>5}  -> {params:>15,} params  ({params / 1e6:.1f}M, {params / 1e9:.3f}B)")

    print(f"ln(32,000) = {math.log(32_000):.4f}  (starting cross-entropy loss, uniform 32k-vocab guess)")
    print(f"ln(248,320) = {math.log(248_320):.4f}  (starting cross-entropy loss, uniform 248,320-vocab guess)")


if __name__ == "__main__":
    app()
