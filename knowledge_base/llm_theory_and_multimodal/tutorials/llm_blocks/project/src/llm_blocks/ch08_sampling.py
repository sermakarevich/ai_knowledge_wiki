"""Chapter 08 — from logits to text: decoding strategies, perplexity, thinking tokens.

`uv run python -m llm_blocks.ch08_sampling plots` draws the six CPU figures (no
downloads); `plots-real` draws the two figures that read the real SmolLM2-135M model;
`demo` prints the numbers quoted in the chapter; `demo-real` prints three real
completions under three decoding settings plus the perplexity of one sentence.

Every decoding function below takes and returns **logits** (raw, unbounded scores),
never probabilities, and follows `transformers.generation.logits_process`'s exact
convention: removed tokens are set to `-inf` rather than deleted, so the vector stays
the same shape and a plain `softmax` afterwards gives them probability 0. Functions
work on the last dimension, so a `(vocab,)` vector or a `(batch, vocab)` batch both
work, which is what lets the tests compare directly against the batched
`transformers` warpers.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn.functional as F
import typer
from torch import Tensor

from llm_blocks.plotting import save, style

app = typer.Typer(add_completion=False, no_args_is_help=False)

NEG_INF = float("-inf")


# ---------------------------------------------------------------------------
# 1. The warpers: pure functions on a logits vector
# ---------------------------------------------------------------------------


def greedy(logits: Tensor) -> Tensor:
    """Always pick the single highest-scoring token: `argmax(logits)`.

    Cheapest and most deterministic strategy, and the one most likely to fall into
    repetition loops, because it never explores anything but the current best guess.
    """
    return logits.argmax(dim=-1)


def temperature(logits: Tensor, temp: float) -> Tensor:
    """`logits / temp`. `temp < 1` sharpens the distribution (more confident, more
    greedy-like); `temp > 1` flattens it (more varied, more random). `temp = 1` is a
    no-op. Matches `TemperatureLogitsWarper`."""
    return logits / temp


def top_k(logits: Tensor, k: int, filter_value: float = NEG_INF) -> Tensor:
    """Keep only the `k` highest-scoring tokens; set every other logit to `filter_value`.

    Matches `TopKLogitsWarper`: find the score of the `k`-th best token and mask
    everything strictly below it.
    """
    k = min(k, logits.shape[-1])
    threshold = torch.topk(logits, k, dim=-1).values[..., -1, None]
    return logits.masked_fill(logits < threshold, filter_value)


def top_p(logits: Tensor, p: float, filter_value: float = NEG_INF) -> Tensor:
    """Nucleus sampling: keep the smallest set of highest-probability tokens whose
    probabilities sum to at least `p`; mask the rest.

    Matches `TopPLogitsWarper`: sort ascending, cut everything whose cumulative mass
    (from the low end) is still below `1 - p` — equivalently, everything *not* needed
    to reach `p` from the high end — always keeping at least one token.
    """
    sorted_logits, sorted_idx = torch.sort(logits, dim=-1, descending=False)
    cumulative_probs = sorted_logits.softmax(dim=-1).cumsum(dim=-1)
    sorted_remove = cumulative_probs <= (1 - p)
    sorted_remove[..., -1] = False  # always keep the single best token
    remove = sorted_remove.scatter(-1, sorted_idx, sorted_remove)
    return logits.masked_fill(remove, filter_value)


def min_p(logits: Tensor, p: float, filter_value: float = NEG_INF) -> Tensor:
    """Keep every token whose probability is at least `p` times the top token's
    probability; mask the rest. Matches `MinPLogitsWarper`.

    Unlike top-k/top-p, the cutoff *adapts* to how confident the model is: when one
    token dominates, the threshold is high and few tokens survive; when the
    distribution is flat, the threshold is low and many survive.
    """
    probs = logits.softmax(dim=-1)
    top_probs = probs.amax(dim=-1, keepdim=True)
    threshold = p * top_probs
    remove = probs < threshold
    top1 = probs.argmax(dim=-1, keepdim=True)
    remove.scatter_(-1, top1, False)  # always keep the single best token
    return logits.masked_fill(remove, filter_value)


def repetition_penalty(logits: Tensor, prev_ids: Sequence[int], penalty: float) -> Tensor:
    """Discourage tokens already seen in `prev_ids`: divide their logit by `penalty`
    if positive, multiply by `penalty` if negative (so the penalty always pushes the
    score *down*, whichever side of zero it starts on). `penalty = 1.0` is a no-op;
    typical values are 1.1-1.3. Matches `RepetitionPenaltyLogitsProcessor` for one
    sequence (`logits` is `(vocab,)`, `prev_ids` are the tokens generated so far).
    """
    logits = logits.clone()
    if not prev_ids:
        return logits
    idx = torch.as_tensor(sorted(set(prev_ids)), dtype=torch.long)
    vals = logits[idx]
    vals = torch.where(vals < 0, vals * penalty, vals / penalty)
    logits[idx] = vals
    return logits


def presence_penalty(logits: Tensor, prev_ids: Sequence[int], penalty: float) -> Tensor:
    """Subtract a flat `penalty` from every token that has appeared at least once in
    `prev_ids` (OpenAI-style: a fixed cost for *presence*, regardless of how many
    times). `penalty = 0` is a no-op."""
    logits = logits.clone()
    if not prev_ids:
        return logits
    idx = torch.as_tensor(sorted(set(prev_ids)), dtype=torch.long)
    logits[idx] = logits[idx] - penalty
    return logits


def frequency_penalty(logits: Tensor, prev_ids: Sequence[int], penalty: float) -> Tensor:
    """Subtract `penalty * count` from every token, where `count` is how many times it
    appears in `prev_ids` (OpenAI-style: the more a token repeats, the harder it is
    pushed down)."""
    logits = logits.clone()
    if not prev_ids:
        return logits
    counts = torch.bincount(torch.as_tensor(prev_ids, dtype=torch.long), minlength=logits.shape[-1])
    return logits - penalty * counts.to(logits.dtype)


# ---------------------------------------------------------------------------
# 2. Perplexity
# ---------------------------------------------------------------------------


def perplexity(logits: Tensor, targets: Tensor) -> float:
    """`exp(mean negative log-likelihood)` of the `targets` under `logits`.

    `logits` is `(n, vocab)`, `targets` is `(n,)`. A model that always assigns
    probability 1 to the correct token has perplexity 1 (zero surprise); a model that
    guesses uniformly over `vocab_size` tokens has perplexity `vocab_size` — see
    `distribution_perplexity` below for the same idea applied to a single distribution
    instead of a scored sequence.
    """
    log_probs = F.log_softmax(logits, dim=-1)
    nll = -log_probs.gather(-1, targets.unsqueeze(-1)).squeeze(-1)
    return torch.exp(nll.mean()).item()


def entropy(logits: Tensor) -> Tensor:
    """Shannon entropy of `softmax(logits)`, in nats: `-sum(p * log(p))`. Zero when the
    model is completely certain (one token has probability 1); largest when the
    distribution is uniform."""
    probs = logits.softmax(dim=-1)
    log_probs = F.log_softmax(logits, dim=-1)
    return -(probs * log_probs).sum(dim=-1)


def distribution_perplexity(logits: Tensor) -> Tensor:
    """`exp(entropy(logits))` — the "effective number of choices" a distribution
    offers, treating it as its own target rather than scoring it against one true
    next token (that is what `perplexity` above does). A distribution that puts all
    its mass on one token has an effective choice count of 1; a uniform distribution
    over `n` tokens has an effective choice count of exactly `n`."""
    return torch.exp(entropy(logits))


# ---------------------------------------------------------------------------
# 3. generate(): a tiny decoding loop
# ---------------------------------------------------------------------------

ModelFn = Callable[[list[int]], Tensor]
Strategy = Callable[[Tensor, list[int]], int]


def greedy_strategy(logits: Tensor, prev_ids: list[int]) -> int:
    """A `Strategy` that always calls `greedy`; ignores `prev_ids`."""
    del prev_ids
    return int(greedy(logits))


def sampling_strategy(
    temp: float = 1.0,
    k: int | None = None,
    p: float | None = None,
    mp: float | None = None,
    rep_penalty: float | None = None,
    generator: torch.Generator | None = None,
) -> Strategy:
    """Build a `Strategy` that applies, in order, repetition penalty, temperature,
    top-k, top-p, min-p, then samples from what is left.

    The order matters: `temperature` has to run before `top_p`/`min_p` because both
    read *probabilities*, and temperature changes what those probabilities are (this
    is also why Ollama and most servers apply temperature first). Each filter is
    optional (`None` skips it), so this one function covers greedy-adjacent sampling,
    plain temperature sampling, and every combination the chapter discusses.
    """

    def strategy(logits: Tensor, prev_ids: list[int]) -> int:
        out = logits
        if rep_penalty is not None:
            out = repetition_penalty(out, prev_ids, rep_penalty)
        out = temperature(out, temp)
        if k is not None:
            out = top_k(out, k)
        if p is not None:
            out = top_p(out, p)
        if mp is not None:
            out = min_p(out, mp)
        probs = F.softmax(out, dim=-1)
        return int(torch.multinomial(probs, 1, generator=generator))

    return strategy


def toy_bigram_table(vocab_size: int = 12, seed: int = 0) -> Tensor:
    """A fixed `(vocab_size, vocab_size)` table of logits: row `i` is "what comes after
    token `i`". Standing in for a real model's next-token distribution, but fixed and
    tiny so `generate` is fully deterministic and needs no download."""
    generator = torch.Generator().manual_seed(seed)
    return torch.randn(vocab_size, vocab_size, generator=generator) * 2.0


def make_bigram_model(table: Tensor) -> ModelFn:
    """Wrap a transition table as a `ModelFn`: the next-token logits depend only on the
    most recent token, exactly like a (order-1) bigram language model."""

    def model_fn(ids: list[int]) -> Tensor:
        return table[ids[-1]]

    return model_fn


def generate(model_fn: ModelFn, prompt_ids: list[int], strategy: Strategy, max_new: int) -> list[int]:
    """Repeatedly: ask `model_fn` for the next-token logits given the tokens so far,
    pick one with `strategy`, append it, stop after `max_new` new tokens.

    This is the entire decoding loop a real generation library runs — the only
    difference between calling it with `make_bigram_model` here and calling it with a
    real transformer (`plots_real`, `demo_real`) is what `model_fn` does internally.
    """
    ids = list(prompt_ids)
    for _ in range(max_new):
        logits = model_fn(ids)
        ids.append(strategy(logits, ids))
    return ids


# ---------------------------------------------------------------------------
# 4. A "realistic" 50-token distribution used by several figures
# ---------------------------------------------------------------------------


def zipfian_logits(n: int = 50, seed: int = 0) -> Tensor:
    """A synthetic but realistic-looking next-token distribution: scores fall off
    roughly like `-log(rank)` (a handful of tokens dominate, a long tail barely
    registers — the shape real language-model output usually has), plus a little
    noise so it is not perfectly smooth."""
    generator = torch.Generator().manual_seed(seed)
    ranks = torch.arange(1, n + 1, dtype=torch.float32)
    base = -torch.log(ranks) * 3.0
    noise = torch.randn(n, generator=generator) * 0.3
    return base + noise


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------


def _fig_pipeline() -> str:
    style()
    fig, ax = plt.subplots(figsize=(12, 3.2))
    stages = [
        "hidden state h\n(hidden_size,)",
        "LM head\nh @ E^T",
        "logits\n(vocab_size,)",
        "warpers\ntemp, top-k,\ntop-p, min-p,\nrep. penalty",
        "probabilities\nsoftmax",
        "sample\n(or argmax)",
    ]
    colors = ["#9467bd", "#1f77b4", "#1f77b4", "#d62728", "#2ca02c", "#ff7f0e"]
    n = len(stages)
    box_w, gap = 1.9, 0.55
    for i, (text, color) in enumerate(zip(stages, colors)):
        x0 = i * (box_w + gap)
        ax.add_patch(plt.Rectangle((x0, 0), box_w, 1.4, facecolor=color, edgecolor="k", alpha=0.75))
        ax.text(x0 + box_w / 2, 0.7, text, ha="center", va="center", fontsize=8.3, color="white", weight="bold")
        if i < n - 1:
            ax.annotate("", xy=(x0 + box_w + gap - 0.05, 0.7), xytext=(x0 + box_w + 0.05, 0.7),
                        arrowprops={"arrowstyle": "->", "lw": 1.4})
    ax.set_xlim(-0.3, n * (box_w + gap))
    ax.set_ylim(-0.3, 1.9)
    ax.axis("off")
    ax.set_title(
        "The last step of a decoder: one hidden vector becomes one sampled token\n"
        "warpers only ever move logits toward -inf or rescale them; softmax always runs last"
    )
    return str(save(fig, "08_pipeline"))


def _fig_temperature() -> str:
    style()
    base = zipfian_logits()
    temps = [0.2, 0.7, 1.0, 1.5]
    fig, axes = plt.subplots(1, len(temps), figsize=(14, 3.6), sharey=True)
    x = np.arange(len(base))
    for ax, t in zip(axes, temps):
        probs = temperature(base, t).softmax(dim=-1).numpy()
        ax.bar(x, probs, color="#1f77b4", width=0.9)
        top1 = probs.max()
        ax.set_title(f"T = {t}\ntop token gets {top1:.0%}", fontsize=9.5)
        ax.set_xlabel("token, sorted by base rank")
    axes[0].set_ylabel("probability")
    fig.suptitle("The same 50-token distribution at four temperatures — lower T sharpens, higher T flattens")
    fig.tight_layout()
    return str(save(fig, "08_temperature"))


def _fig_topk_topp_minp() -> str:
    style()
    base = zipfian_logits()
    x = np.arange(len(base))
    probs = base.softmax(dim=-1).numpy()
    settings = [
        ("top-k = 10", top_k(base, 10)),
        ("top-p = 0.9", top_p(base, 0.9)),
        ("min-p = 0.1", min_p(base, 0.1)),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(14, 3.8), sharey=True)
    for ax, (title, filtered) in zip(axes, settings):
        kept = ~torch.isinf(filtered)
        n_kept = int(kept.sum())
        kept_mass = probs[kept.numpy()].sum()
        colors = np.where(kept.numpy(), "#2ca02c", "#cccccc")
        ax.bar(x, probs, color=colors, width=0.9)
        ax.set_title(f"{title}\nkeeps {n_kept} tokens, {kept_mass:.0%} of the mass", fontsize=9.5)
        ax.set_xlabel("token, sorted by base rank")
    axes[0].set_ylabel("probability (unfiltered)")
    fig.suptitle("Three ways to truncate the same distribution — green = kept, grey = set to -inf")
    fig.tight_layout()
    return str(save(fig, "08_topk_topp_minp"))


def _fig_repetition_penalty() -> str:
    style()
    base = zipfian_logits(n=20, seed=1)
    prev_ids = [0, 1, 2, 5]
    penalties = [1.0, 1.2, 1.5]
    x = np.arange(len(base))
    fig, ax = plt.subplots(figsize=(10, 4.5))
    width = 0.25
    for i, pen in enumerate(penalties):
        penalized = repetition_penalty(base, prev_ids, pen)
        ax.bar(x + (i - 1) * width, penalized.numpy(), width=width, label=f"penalty = {pen}")
    for i in prev_ids:
        ax.axvspan(i - 0.5, i + 0.5, color="#d62728", alpha=0.08)
    ax.text(0.02, 0.96, "shaded columns = tokens already generated", transform=ax.transAxes,
            fontsize=8.5, va="top", bbox={"boxstyle": "round", "facecolor": "white", "edgecolor": "gray"})
    ax.set_xlabel("token id")
    ax.set_ylabel("logit")
    ax.set_title("Repetition penalty only touches logits of tokens already seen\n"
                 "(positive logits shrink toward zero, negative logits grow more negative)")
    ax.legend(fontsize=9)
    return str(save(fig, "08_repetition_penalty"))


def _fig_perplexity_intuition() -> str:
    style()
    vocab = 8
    dists = {
        "certain\n(one token ~1.0)": torch.tensor([8.0] + [0.0] * (vocab - 1)),
        "confident\n(top token ~0.6)": torch.tensor([2.0, 1.0, 0.5, 0.2, 0.0, 0.0, -0.3, -0.5]),
        "unsure\n(fairly flat)": torch.tensor([0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0, -0.1]),
        "uniform\n(no idea)": torch.zeros(vocab),
    }
    fig, axes = plt.subplots(1, len(dists), figsize=(13, 3.6), sharey=True)
    for ax, (title, logits) in zip(axes, dists.items()):
        probs = logits.softmax(dim=-1).numpy()
        ppl = distribution_perplexity(logits).item()
        ax.bar(np.arange(vocab), probs, color="#9467bd")
        ax.set_title(f"{title}\nperplexity = {ppl:.2f}", fontsize=9.5)
        ax.set_xlabel("token")
    axes[0].set_ylabel("probability")
    fig.suptitle("Perplexity as the \"effective number of choices\": exp(entropy) of the distribution")
    fig.tight_layout()
    return str(save(fig, "08_perplexity_intuition"))


def _fig_greedy_vs_sampling_tree() -> str:
    style()
    fig, ax = plt.subplots(figsize=(10, 6.0))

    def edge(parent: tuple[float, float], child: tuple[float, float], p: float, color: str, lw: float) -> None:
        ax.plot([parent[0], child[0]], [parent[1], child[1]], color=color, lw=lw)
        mid = ((parent[0] + child[0]) / 2, (parent[1] + child[1]) / 2)
        offset = (0.35, 0.05) if child[0] >= parent[0] else (-0.35, 0.05)
        ax.text(mid[0] + offset[0], mid[1] + offset[1], f"P={p}", fontsize=8.5, ha="center", color=color)

    root = (5.0, 5.0)
    ax.text(*root, "start", ha="center", va="center", fontsize=10, zorder=3,
            bbox={"boxstyle": "circle", "facecolor": "#eeeeee"})

    step1 = [(2.0, 3.0, "A", 0.6, "#d62728"), (8.0, 3.0, "B", 0.4, "#1f77b4")]
    for x, y, label, p, color in step1:
        edge(root, (x, y), p, color, 2.0)
        ax.text(x, y, label, ha="center", va="center", fontsize=10, zorder=3,
                bbox={"boxstyle": "circle", "facecolor": color, "alpha": 0.7})

    # Chosen so greedy's step-1 choice (A, 0.6 > 0.4) does NOT lead to the best
    # sequence: A's best continuation (A2) gives a lower joint probability than
    # B's best continuation (B1), which greedy never explores.
    step2 = [
        (0.5, 0.8, "A1", 0.1, "#d62728", (2.0, 3.0)),
        (3.2, 0.8, "A2", 0.5, "#d62728", (2.0, 3.0)),
        (6.8, 0.8, "B1", 0.9, "#1f77b4", (8.0, 3.0)),
        (9.5, 0.8, "B2", 0.1, "#1f77b4", (8.0, 3.0)),
    ]
    for x, y, label, p, color, parent in step2:
        edge(parent, (x, y), p, color, 1.4)
        ax.text(x, y, label, ha="center", va="center", fontsize=9, zorder=3,
                bbox={"boxstyle": "circle", "facecolor": color, "alpha": 0.5})

    joint = {"A1": 0.6 * 0.1, "A2": 0.6 * 0.5, "B1": 0.4 * 0.9, "B2": 0.4 * 0.1}
    best = max(joint, key=joint.get)
    for x, y, label, *_rest in step2:
        ax.text(x, y - 0.55, f"joint={joint[label]:.2f}" + ("  <- best sequence" if label == best else ""),
                ha="center", fontsize=8.5, weight="bold" if label == best else "normal")

    ax.text(5.0, -0.3,
            f"Greedy picks A at step 1 (0.6 > 0.4), then A2 (0.5 > 0.1): sequence A-A2, joint = {joint['A2']:.2f}.\n"
            f"But B-B1 has joint = {joint['B1']:.2f} — the single most likely *sequence* — "
            "greedy never sees it because it never revisits step 1.",
            ha="center", fontsize=9.5,
            bbox={"boxstyle": "round", "facecolor": "#fff6e5", "edgecolor": "#ff7f0e"})

    ax.set_xlim(-1, 11)
    ax.set_ylim(-1.4, 6.4)
    ax.axis("off")
    ax.set_title("Greedy decoding maximises each step, not the whole sequence")
    return str(save(fig, "08_greedy_vs_sampling_tree"))


# ---------------------------------------------------------------------------
# Figures that read the real SmolLM2-135M model
# ---------------------------------------------------------------------------


def real_model_fn(tokenizer, model) -> ModelFn:
    """Wrap a loaded causal-LM as a `ModelFn`: feed the whole prefix, read the logits
    for the last position. Simple and correct, not fast (no KV cache) — fine for the
    short prompts used here."""

    def model_fn(ids: list[int]) -> Tensor:
        with torch.no_grad():
            out = model(torch.tensor([ids]))
        return out.logits[0, -1]

    return model_fn


def _top15(tokenizer, model, prompt: str) -> tuple[list[str], np.ndarray]:
    ids = tokenizer.encode(prompt, add_special_tokens=False)
    logits = real_model_fn(tokenizer, model)(ids)
    probs = logits.softmax(dim=-1)
    top = torch.topk(probs, 15)
    labels = [tokenizer.decode([i]).replace(" ", "␣") or "∅" for i in top.indices.tolist()]
    return labels, top.values.numpy()


def _fig_real_next_token() -> str:
    from llm_blocks.reference import load_smollm

    style()
    tokenizer, model = load_smollm()
    prompts = ["The capital of France is", "I think that"]
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.0))
    for ax, prompt in zip(axes, prompts):
        labels, values = _top15(tokenizer, model, prompt)
        y = np.arange(len(labels))[::-1]
        ax.barh(y, values, color="#1f77b4")
        ax.set_yticks(y, labels, fontsize=8.5)
        ax.set_xlabel("probability")
        ax.set_title(f"after: \"{prompt}\"", fontsize=10)
    fig.suptitle("SmolLM2-135M's top-15 next-token probabilities: a sharp answer vs a genuinely open continuation")
    fig.tight_layout()
    return str(save(fig, "08_real_next_token"))


_ENTROPY_SENTENCE = (
    "The quick brown fox jumps over the lazy dog while the sun slowly sets behind "
    "the distant mountains and birds fly home."
)


def _fig_real_entropy_over_text() -> str:
    from llm_blocks.reference import load_smollm

    style()
    tokenizer, model = load_smollm()
    ids = tokenizer.encode(_ENTROPY_SENTENCE, add_special_tokens=False)[:40]
    with torch.no_grad():
        logits = model(torch.tensor([ids])).logits[0]
    ent = entropy(logits).numpy()
    pieces = [tokenizer.decode([i]).replace(" ", "␣") for i in ids]

    fig, ax = plt.subplots(figsize=(13, 4.5))
    ax.plot(ent, "o-", color="#1f77b4", ms=4)
    ax.set_xticks(range(len(pieces)), pieces, rotation=60, ha="right", fontsize=7.5)
    ax.set_ylabel("entropy of the NEXT-token distribution, nats")
    ax.set_title(
        "Per-token entropy while reading a sentence: low points are tokens the model saw coming, "
        "high points are genuine forks in the road"
    )
    return str(save(fig, "08_real_entropy_over_text"))


def demo_real() -> None:
    """Print 3 real completions under greedy / T=0.7 top-p=0.9 / T=1.5, plus the
    perplexity of one sentence, on SmolLM2-135M."""
    from llm_blocks.reference import load_smollm

    tokenizer, model = load_smollm()
    fn = real_model_fn(tokenizer, model)
    prompt = "The best way to learn a new skill is"
    prompt_ids = tokenizer.encode(prompt, add_special_tokens=False)

    strategies = {
        "greedy": greedy_strategy,
        "T=0.7, top-p=0.9": sampling_strategy(temp=0.7, p=0.9, generator=torch.Generator().manual_seed(0)),
        "T=1.5": sampling_strategy(temp=1.5, generator=torch.Generator().manual_seed(0)),
    }
    print(f"prompt: {prompt!r}\n")
    for name, strategy in strategies.items():
        ids = generate(fn, list(prompt_ids), strategy, max_new=20)
        text = tokenizer.decode(ids[len(prompt_ids):])
        print(f"[{name}]\n  {text!r}\n")

    sentence = "Paris is the capital of France."
    ids = tokenizer.encode(sentence, add_special_tokens=False)
    with torch.no_grad():
        logits = model(torch.tensor([ids])).logits[0]
    ppl = perplexity(logits[:-1], torch.tensor(ids[1:]))
    print(f"perplexity of {sentence!r}: {ppl:.2f}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


@app.command()
def plots() -> None:
    """Regenerate the six CPU figures for this chapter (no downloads)."""
    print(f"wrote: {_fig_pipeline()}")
    print(f"wrote: {_fig_temperature()}")
    print(f"wrote: {_fig_topk_topp_minp()}")
    print(f"wrote: {_fig_repetition_penalty()}")
    print(f"wrote: {_fig_perplexity_intuition()}")
    print(f"wrote: {_fig_greedy_vs_sampling_tree()}")


@app.command(name="plots-real")
def plots_real() -> None:
    """Regenerate the two figures that need the real SmolLM2-135M model."""
    print(f"wrote: {_fig_real_next_token()}")
    print(f"wrote: {_fig_real_entropy_over_text()}")


@app.command(name="demo-real")
def demo_real_command() -> None:
    """Print 3 real completions plus one sentence's perplexity on SmolLM2-135M."""
    demo_real()


@app.command()
def demo() -> None:
    """Print the numbers quoted in the chapter."""
    base = zipfian_logits()
    print("Same 50-token distribution, kept tokens/mass under each filter:")
    for name, filtered in [("top-k=10", top_k(base, 10)), ("top-p=0.9", top_p(base, 0.9)), ("min-p=0.1", min_p(base, 0.1))]:
        kept = ~torch.isinf(filtered)
        mass = base.softmax(dim=-1)[kept].sum().item()
        print(f"  {name:10s}: keeps {int(kept.sum()):2d} tokens, {mass:.1%} of the probability mass")

    print("\nTemperature sharpens/flattens the top token's share:")
    for t in [0.2, 0.7, 1.0, 1.5]:
        top1 = temperature(base, t).softmax(dim=-1).max().item()
        print(f"  T={t}: top token gets {top1:.1%}")

    print("\nPerplexity as effective choices, toy distributions:")
    vocab = 8
    for name, logits in [
        ("certain", torch.tensor([8.0] + [0.0] * (vocab - 1))),
        ("confident", torch.tensor([2.0, 1.0, 0.5, 0.2, 0.0, 0.0, -0.3, -0.5])),
        ("uniform", torch.zeros(vocab)),
    ]:
        print(f"  {name:10s}: perplexity = {distribution_perplexity(logits).item():.2f}  (vocab size {vocab})")

    print("\nToy bigram generate() with different strategies:")
    table = toy_bigram_table()
    model_fn = make_bigram_model(table)
    prompt = [0]
    greedy_out = generate(model_fn, prompt, greedy_strategy, max_new=10)
    sample_out = generate(
        model_fn, prompt, sampling_strategy(temp=0.7, p=0.9, generator=torch.Generator().manual_seed(0)), max_new=10
    )
    print(f"  greedy        : {greedy_out}")
    print(f"  T=0.7, p=0.9  : {sample_out}")

    print("\nPerplexity of a toy sequence scored by the bigram table:")
    seq = greedy_out
    logits = torch.stack([table[i] for i in seq[:-1]])
    targets = torch.tensor(seq[1:])
    print(f"  perplexity = {perplexity(logits, targets):.2f}  (vocab size {table.shape[0]})")


if __name__ == "__main__":
    app()
