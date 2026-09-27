"""Chapter 09 — training dynamics: optimizers, schedules, clipping, batch size, precision.

`uv run python -m llm_blocks.ch09_training_dynamics plots` draws the nine figures for this
chapter (no downloads, CPU only, ~2 min); `demo` prints the final losses and wall times
quoted in the chapter.

The toy language model reuses three blocks from earlier chapters unchanged:
`GroupedQueryAttention` (chapter 03), `RMSNorm` (chapter 05), `SwiGLUMLP` (chapter 06).
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn.functional as F
import typer
from torch import Tensor, nn

from llm_blocks.ch03_attention import GroupedQueryAttention
from llm_blocks.ch05_norm_residual import RMSNorm
from llm_blocks.ch06_mlp_moe import SwiGLUMLP
from llm_blocks.plotting import save, style

app = typer.Typer(add_completion=False, no_args_is_help=False)


# ---------------------------------------------------------------------------
# 1. Optimizers from scratch, operating on a plain list of tensors
# ---------------------------------------------------------------------------


class SGD:
    """Plain gradient descent: `p -= lr * grad`. Matches `torch.optim.SGD(momentum=0)`."""

    def __init__(self, params: list[Tensor], lr: float) -> None:
        self.params = list(params)
        self.lr = lr

    @torch.no_grad()
    def step(self) -> None:
        for p in self.params:
            if p.grad is not None:
                p.add_(p.grad, alpha=-self.lr)

    def zero_grad(self) -> None:
        for p in self.params:
            p.grad = None


class SGDMomentum:
    """SGD with a momentum buffer (a "ball with memory"):

        v = momentum * v + grad
        p = p - lr * v

    Matches `torch.optim.SGD(momentum=momentum, dampening=0, nesterov=False)`: the buffer
    keeps a running, exponentially-weighted sum of past gradients, so the step keeps moving
    in a direction that was consistently downhill even after the gradient there shrinks —
    the effect the "paths on a quadratic bowl" figure below shows directly.
    """

    def __init__(self, params: list[Tensor], lr: float, momentum: float = 0.9) -> None:
        self.params = list(params)
        self.lr = lr
        self.momentum = momentum
        self.velocity = [torch.zeros_like(p) for p in self.params]

    @torch.no_grad()
    def step(self) -> None:
        for p, v in zip(self.params, self.velocity):
            if p.grad is None:
                continue
            v.mul_(self.momentum).add_(p.grad)
            p.add_(v, alpha=-self.lr)

    def zero_grad(self) -> None:
        for p in self.params:
            p.grad = None


class Adam:
    """Adam (Kingma & Ba, 2015): a running mean (`m`) and a running mean-square (`v`) of the
    gradient, each bias-corrected, give every parameter its *own* step size — a parameter
    with a small, noisy gradient still gets a normal-sized step, because `v` divides it back
    up. Matches `torch.optim.Adam(betas=(beta1, beta2), eps=eps)`.
    """

    def __init__(
        self,
        params: list[Tensor],
        lr: float = 1e-3,
        betas: tuple[float, float] = (0.9, 0.999),
        eps: float = 1e-8,
    ) -> None:
        self.params = list(params)
        self.lr = lr
        self.beta1, self.beta2 = betas
        self.eps = eps
        self.m = [torch.zeros_like(p) for p in self.params]
        self.v = [torch.zeros_like(p) for p in self.params]
        self.t = 0

    @torch.no_grad()
    def step(self) -> None:
        self.t += 1
        bias1 = 1 - self.beta1**self.t
        bias2 = 1 - self.beta2**self.t
        for p, m, v in zip(self.params, self.m, self.v):
            if p.grad is None:
                continue
            g = p.grad
            m.mul_(self.beta1).add_(g, alpha=1 - self.beta1)
            v.mul_(self.beta2).addcmul_(g, g, value=1 - self.beta2)
            m_hat = m / bias1
            v_hat = v / bias2
            p.add_(m_hat / (v_hat.sqrt() + self.eps), alpha=-self.lr)

    def zero_grad(self) -> None:
        for p in self.params:
            p.grad = None


class AdamW:
    """Adam with *decoupled* weight decay (Loshchilov & Hutter, 2019): instead of adding
    `wd * p` into the gradient before it feeds `m`/`v` (plain Adam + L2 regularisation, which
    lets the adaptive step size warp the decay too), the decay is applied straight to the
    parameter, at the plain learning rate, in the same line as the Adam step:

        p = p - lr * wd * p - lr * m_hat / (sqrt(v_hat) + eps)

    Matches `torch.optim.AdamW(betas=(beta1, beta2), eps=eps, weight_decay=wd)`.
    """

    def __init__(
        self,
        params: list[Tensor],
        lr: float = 1e-3,
        betas: tuple[float, float] = (0.9, 0.999),
        eps: float = 1e-8,
        weight_decay: float = 0.01,
    ) -> None:
        self.params = list(params)
        self.lr = lr
        self.beta1, self.beta2 = betas
        self.eps = eps
        self.weight_decay = weight_decay
        self.m = [torch.zeros_like(p) for p in self.params]
        self.v = [torch.zeros_like(p) for p in self.params]
        self.t = 0

    @torch.no_grad()
    def step(self) -> None:
        self.t += 1
        bias1 = 1 - self.beta1**self.t
        bias2 = 1 - self.beta2**self.t
        for p, m, v in zip(self.params, self.m, self.v):
            if p.grad is None:
                continue
            g = p.grad
            if self.weight_decay != 0:
                p.add_(p, alpha=-self.lr * self.weight_decay)
            m.mul_(self.beta1).add_(g, alpha=1 - self.beta1)
            v.mul_(self.beta2).addcmul_(g, g, value=1 - self.beta2)
            m_hat = m / bias1
            v_hat = v / bias2
            p.add_(m_hat / (v_hat.sqrt() + self.eps), alpha=-self.lr)

    def zero_grad(self) -> None:
        for p in self.params:
            p.grad = None


# ---------------------------------------------------------------------------
# 2. Learning-rate schedules: pure functions of the step
# ---------------------------------------------------------------------------


def warmup_cosine(step: int, total: int, warmup: int, lr_max: float, lr_min: float = 0.0) -> float:
    """Linear warmup from 0 to `lr_max` over `warmup` steps, then cosine decay from
    `lr_max` down to `lr_min` over the rest of `total` steps. The standard LLM default."""
    if warmup > 0 and step < warmup:
        return lr_max * (step + 1) / warmup
    span = max(total - warmup, 1)
    progress = min((step - warmup) / span, 1.0)
    cosine = 0.5 * (1 + np.cos(np.pi * progress))
    return lr_min + (lr_max - lr_min) * cosine


def wsd(step: int, total: int, warmup: int, decay_frac: float, lr_max: float) -> float:
    """Warmup-stable-decay: linear warmup, hold flat at `lr_max`, then linear decay to 0
    over the last `decay_frac` of `total` steps. Popular when the total token budget is not
    fixed in advance (MiniCPM, Llama-3.1, DeepSeek-V2): training can stop at any "stable"
    checkpoint and only the short decay phase needs to be re-run to finish cleanly.
    """
    if warmup > 0 and step < warmup:
        return lr_max * (step + 1) / warmup
    decay_steps = int(total * decay_frac)
    decay_start = max(total - decay_steps, warmup)
    if step < decay_start:
        return lr_max
    progress = min((step - decay_start) / max(total - decay_start, 1), 1.0)
    return lr_max * (1 - progress)


def linear_decay_to_zero(step: int, total: int, warmup: int, lr_max: float) -> float:
    """Linear warmup, then a straight line down to exactly 0 at `step == total`."""
    if warmup > 0 and step < warmup:
        return lr_max * (step + 1) / warmup
    span = max(total - warmup, 1)
    progress = min((step - warmup) / span, 1.0)
    return lr_max * (1 - progress)


# ---------------------------------------------------------------------------
# 3. Gradient clipping
# ---------------------------------------------------------------------------


def clip_grad_norm_(params: list[Tensor], max_norm: float, eps: float = 1e-6) -> float:
    """Rescale every gradient in `params` so their combined L2 norm is at most `max_norm`;
    returns the *pre-clip* total norm. Matches `torch.nn.utils.clip_grad_norm_` (default
    `norm_type=2.0`): one global scale factor, so the *direction* of the combined gradient
    is unchanged, only its length is capped.
    """
    grads = [p.grad for p in params if p.grad is not None]
    if not grads:
        return 0.0
    total_norm = torch.sqrt(sum(g.pow(2).sum() for g in grads))
    clip_coef = max_norm / (total_norm + eps)
    if clip_coef < 1:
        for g in grads:
            g.mul_(clip_coef)
    return total_norm.item()


# ---------------------------------------------------------------------------
# 4. A quadratic toy problem for the optimizer-paths figure
# ---------------------------------------------------------------------------


def ill_conditioned_quadratic(xy: Tensor, a: float = 1.0, b: float = 20.0) -> Tensor:
    """`f(x, y) = a*x^2 + b*y^2`: a bowl that is much steeper along `y` than `x` (curvature
    ratio `b/a`) — the classic picture for why plain gradient descent zig-zags and momentum
    (or Adam's per-parameter scaling) does not.
    """
    return a * xy[0] ** 2 + b * xy[1] ** 2


def optimizer_path(make_opt, steps: int = 40, start: tuple[float, float] = (-4.0, 1.5)) -> np.ndarray:
    """Run `steps` steps of an optimizer built by `make_opt([xy])` on the quadratic above;
    return the `(steps + 1, 2)` array of visited points."""
    xy = torch.tensor(start, requires_grad=True)
    opt = make_opt([xy])
    path = [xy.detach().clone().numpy()]
    for _ in range(steps):
        opt.zero_grad()
        loss = ill_conditioned_quadratic(xy)
        loss.backward()
        opt.step()
        path.append(xy.detach().clone().numpy())
    return np.array(path)


# ---------------------------------------------------------------------------
# 5. Synthetic bigram-grammar token stream and the toy transformer LM
# ---------------------------------------------------------------------------

VOCAB_SIZE = 256
N_ACTIVE = 200  # "words" with real bigram structure; the rest of the vocab is rare noise


def make_bigram_grammar(
    vocab_size: int = VOCAB_SIZE, n_active: int = N_ACTIVE, n_successors: int = 3, seed: int = 0
) -> Tensor:
    """A `(vocab_size, vocab_size)` transition-probability table with real structure: each
    "active" token (id `0..n_active-1`) has `n_successors` preferred next tokens that carry
    most of the probability mass; the remaining `vocab_size - n_active` tokens are rare
    filler with a near-uniform, low-probability row. A model that learns this table can
    predict the next token far better than chance — the source of the falling loss curve.
    """
    generator = torch.Generator().manual_seed(seed)
    probs = torch.full((vocab_size, vocab_size), 0.02 / vocab_size)
    for i in range(n_active):
        successors = torch.randperm(vocab_size, generator=generator)[:n_successors]
        weights = torch.rand(n_successors, generator=generator) * 3 + 1
        weights = weights / weights.sum() * 0.98
        probs[i, successors] += weights
    probs = probs / probs.sum(dim=-1, keepdim=True)
    return probs


def sample_token_stream(probs: Tensor, n_tokens: int, seed: int = 0) -> Tensor:
    """Sample a length-`n_tokens` sequence of ids from the order-1 Markov chain `probs`,
    starting from token 0."""
    generator = torch.Generator().manual_seed(seed)
    ids = torch.zeros(n_tokens, dtype=torch.long)
    for i in range(1, n_tokens):
        ids[i] = torch.multinomial(probs[ids[i - 1]], 1, generator=generator)
    return ids


def make_batches(stream: Tensor, batch_size: int, seq_len: int, n_batches: int, seed: int = 0) -> list[Tensor]:
    """Cut `n_batches` random `(batch_size, seq_len + 1)` windows out of `stream` (the extra
    token gives every window its own next-token targets)."""
    generator = torch.Generator().manual_seed(seed)
    max_start = len(stream) - seq_len - 1
    batches = []
    for _ in range(n_batches):
        starts = torch.randint(0, max_start, (batch_size,), generator=generator)
        batches.append(torch.stack([stream[s : s + seq_len + 1] for s in starts]))
    return batches


@dataclass
class ToyLMConfig:
    """A tiny decoder-only transformer built from chapters 03/05/06's blocks."""

    vocab_size: int = VOCAB_SIZE
    d_model: int = 64
    n_heads: int = 4
    n_kv_heads: int = 2
    head_dim: int = 16
    d_ff: int = 128
    n_layers: int = 2
    max_seq: int = 128


class ToyTransformerLM(nn.Module):
    """Embedding + learned position embedding -> [pre-norm GQA + pre-norm SwiGLU] x n_layers
    -> final RMSNorm -> LM head. The same pre-norm residual-stream recipe as chapter 05,
    the same GQA as chapter 03, the same SwiGLU MLP as chapter 06 — no new machinery, just
    those three blocks stacked into a model small enough to train on CPU in seconds.
    """

    def __init__(self, cfg: ToyLMConfig) -> None:
        super().__init__()
        self.cfg = cfg
        self.embed = nn.Embedding(cfg.vocab_size, cfg.d_model)
        self.pos_embed = nn.Embedding(cfg.max_seq, cfg.d_model)
        self.attn_norms = nn.ModuleList(RMSNorm(cfg.d_model) for _ in range(cfg.n_layers))
        self.attns = nn.ModuleList(
            GroupedQueryAttention(cfg.d_model, cfg.n_heads, cfg.n_kv_heads, cfg.head_dim)
            for _ in range(cfg.n_layers)
        )
        self.mlp_norms = nn.ModuleList(RMSNorm(cfg.d_model) for _ in range(cfg.n_layers))
        self.mlps = nn.ModuleList(SwiGLUMLP(cfg.d_model, cfg.d_ff) for _ in range(cfg.n_layers))
        self.final_norm = RMSNorm(cfg.d_model)
        self.lm_head = nn.Linear(cfg.d_model, cfg.vocab_size, bias=False)

    def forward(self, ids: Tensor) -> Tensor:
        _, t = ids.shape
        positions = torch.arange(t, device=ids.device)
        h = self.embed(ids) + self.pos_embed(positions)
        for attn_norm, attn, mlp_norm, mlp in zip(self.attn_norms, self.attns, self.mlp_norms, self.mlps):
            h = h + attn(attn_norm(h), causal=True)[0]
            h = h + mlp(mlp_norm(h))
        h = self.final_norm(h)
        return self.lm_head(h)

    def num_params(self) -> int:
        return sum(p.numel() for p in self.parameters())


def lm_loss(model: ToyTransformerLM, batch: Tensor) -> Tensor:
    """Next-token cross-entropy on one `(batch, seq_len + 1)` window."""
    inputs, targets = batch[:, :-1], batch[:, 1:]
    logits = model(inputs)
    return F.cross_entropy(logits.reshape(-1, logits.shape[-1]), targets.reshape(-1))


@dataclass
class TrainResult:
    losses: list[float] = field(default_factory=list)
    grad_norms: list[float] = field(default_factory=list)
    lrs: list[float] = field(default_factory=list)
    tokens_seen: list[int] = field(default_factory=list)
    wall_time: float = 0.0
    diverged: bool = False


def train_toy_lm(
    cfg: ToyLMConfig,
    batches: list[Tensor],
    make_opt,
    lr_fn=None,
    clip_norm: float | None = None,
    seed: int = 0,
) -> TrainResult:
    """Train `ToyTransformerLM` for `len(batches)` steps; `make_opt(params, lr)` builds an
    optimizer (any of the four above), `lr_fn(step) -> float` overrides the learning rate
    every step if given (a schedule), `clip_norm` clips gradients before the optimizer step.
    Stops early and marks `diverged=True` if the loss becomes non-finite.
    """
    torch.manual_seed(seed)
    model = ToyTransformerLM(cfg)
    params = list(model.parameters())
    opt = make_opt(params)
    result = TrainResult()
    start = time.perf_counter()
    tokens_per_step = batches[0].shape[0] * (batches[0].shape[1] - 1)
    for step, batch in enumerate(batches):
        if lr_fn is not None:
            lr = lr_fn(step)
            opt.lr = lr
            result.lrs.append(lr)
        loss = lm_loss(model, batch)
        opt.zero_grad()
        loss.backward()
        grad_norm = clip_grad_norm_(params, clip_norm) if clip_norm is not None else _grad_norm(params)
        result.grad_norms.append(grad_norm)
        opt.step()
        loss_val = loss.item()
        result.losses.append(loss_val)
        result.tokens_seen.append((step + 1) * tokens_per_step)
        if not np.isfinite(loss_val):
            result.diverged = True
            break
    result.wall_time = time.perf_counter() - start
    return result


def _grad_norm(params: list[Tensor]) -> float:
    grads = [p.grad for p in params if p.grad is not None]
    if not grads:
        return 0.0
    return torch.sqrt(sum(g.pow(2).sum() for g in grads)).item()


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------


def _fig_optimizers_path() -> str:
    style()
    paths = {
        "SGD, lr=0.045": optimizer_path(lambda p: SGD(p, lr=0.045)),
        "SGD + momentum, lr=0.02": optimizer_path(lambda p: SGDMomentum(p, lr=0.02, momentum=0.9)),
        "Adam, lr=0.3": optimizer_path(lambda p: Adam(p, lr=0.3)),
    }
    x = np.linspace(-4.5, 4.5, 200)
    y = np.linspace(-2, 2, 200)
    xx, yy = np.meshgrid(x, y)
    zz = 1.0 * xx**2 + 20.0 * yy**2

    fig, ax = plt.subplots(figsize=(8, 5.2))
    ax.contour(xx, yy, zz, levels=25, colors="#cccccc", linewidths=0.7)
    for (name, path), color in zip(paths.items(), ["#d62728", "#ff7f0e", "#1f77b4"]):
        ax.plot(path[:, 0], path[:, 1], "o-", ms=3, lw=1.3, color=color, label=name)
    ax.plot(0, 0, "k*", ms=14, label="minimum")
    ax.set_xlabel("x  (shallow direction)")
    ax.set_ylabel("y  (steep direction, curvature 20x)")
    ax.set_title("Same start, same bowl: SGD zig-zags along the steep axis and barely\n"
                 "moves along the shallow one; momentum overshoots once then settles, much\n"
                 "faster along x; Adam rescales each axis by its own gradient scale")
    ax.legend(fontsize=9)
    return str(save(fig, "09_optimizers_path"))


def _fig_lr_schedules() -> str:
    style()
    total, warmup = 10_000, 500
    steps = np.arange(total)
    schedules = {
        "warmup + cosine": [warmup_cosine(s, total, warmup, lr_max=1.0) for s in steps],
        "WSD (decay last 20%)": [wsd(s, total, warmup, decay_frac=0.2, lr_max=1.0) for s in steps],
        "linear decay to 0": [linear_decay_to_zero(s, total, warmup, lr_max=1.0) for s in steps],
    }
    fig, ax = plt.subplots(figsize=(9, 4.8))
    for name, values in schedules.items():
        ax.plot(steps, values, label=name, lw=1.6)
    ax.axvline(warmup, color="#999999", ls="--", lw=1, label=f"warmup ends ({warmup} steps)")
    ax.set_xlabel("step")
    ax.set_ylabel("learning rate / lr_max")
    ax.set_title("Three LR schedules over 10k steps, same warmup and peak\n"
                 "WSD stays flat until the last 20% then drops fast; cosine decays the whole way")
    ax.legend(fontsize=9)
    return str(save(fig, "09_lr_schedules"))


def _default_batches(batch_size: int = 32, seq_len: int = 32, n_batches: int = 400, seed: int = 0) -> list[Tensor]:
    probs = make_bigram_grammar(seed=seed)
    stream = sample_token_stream(probs, n_tokens=20_000, seed=seed)
    return make_batches(stream, batch_size=batch_size, seq_len=seq_len, n_batches=n_batches, seed=seed)


def _looks_diverged(losses: list[float]) -> bool:
    """Heuristic for the sweep label: the loss shot up to several times its starting
    value at some point during training, even if it partially recovered."""
    if not np.all(np.isfinite(losses)):
        return True
    return max(losses) > 3 * np.mean(losses[:5])


def _fig_toy_lm_lr_sweep() -> tuple[str, dict[float, TrainResult]]:
    style()
    cfg = ToyLMConfig()
    batches = _default_batches(n_batches=400)
    lrs = [1e-4, 1e-3, 1e-2, 1.0]
    results = {lr: train_toy_lm(cfg, batches, lambda p, lr=lr: AdamW(p, lr=lr)) for lr in lrs}

    fig, ax = plt.subplots(figsize=(9, 4.8))
    for lr, res in results.items():
        label = f"lr={lr:g}" + ("  (diverges)" if _looks_diverged(res.losses) else "")
        ax.plot(res.losses, label=label, lw=1.4)
    ax.axhline(np.log(cfg.vocab_size), color="#999999", ls="--", lw=1, label="ln(vocab) = random guessing")
    ax.set_xlabel("step")
    ax.set_ylabel("cross-entropy loss")
    ax.set_ylim(0, 15)
    ax.set_title("Toy LM, four learning rates, AdamW, same 400 steps\n"
                 "too low barely moves, too high spikes wildly — the single most important knob")
    ax.legend(fontsize=9)
    return str(save(fig, "09_toy_lm_lr_sweep")), results


def _fig_toy_lm_schedule(best_lr: float = 1e-2) -> tuple[str, dict[str, TrainResult]]:
    style()
    cfg = ToyLMConfig()
    batches = _default_batches(n_batches=400, seed=1)
    total, warmup = len(batches), 40
    schedules = {
        "constant": lambda s: best_lr,
        "warmup + cosine": lambda s: warmup_cosine(s, total, warmup, lr_max=best_lr),
        "WSD": lambda s: wsd(s, total, warmup, decay_frac=0.2, lr_max=best_lr),
    }
    results = {
        name: train_toy_lm(cfg, batches, lambda p: AdamW(p, lr=best_lr), lr_fn=fn)
        for name, fn in schedules.items()
    }
    fig, ax = plt.subplots(figsize=(9, 4.8))
    for name, res in results.items():
        ax.plot(res.losses, label=name, lw=1.4)
    ax.set_xlabel("step")
    ax.set_ylabel("cross-entropy loss")
    ax.set_title(f"Toy LM, three schedules, same peak lr={best_lr:g}, same 400 steps, AdamW\n"
                 "warmup avoids the early spike a constant lr risks; cosine/WSD keep improving longer")
    ax.legend(fontsize=9)
    return str(save(fig, "09_toy_lm_schedule")), results


def _fig_grad_clipping(high_lr: float = 8e-2) -> tuple[str, dict[str, TrainResult]]:
    style()
    cfg = ToyLMConfig()
    batches = _default_batches(n_batches=200, seed=2)
    results = {
        "no clipping": train_toy_lm(cfg, batches, lambda p: AdamW(p, lr=high_lr), clip_norm=None),
        "clip at 1.0": train_toy_lm(cfg, batches, lambda p: AdamW(p, lr=high_lr), clip_norm=1.0),
    }
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8))
    ax1.plot(results["no clipping"].grad_norms, color="#d62728", lw=1.2, label="grad norm, no clipping")
    ax1.axhline(1.0, color="#333333", ls="--", lw=1, label="clip threshold = 1.0")
    ax1.set_xlabel("step")
    ax1.set_ylabel("gradient L2 norm (pre-clip)")
    ax1.set_yscale("log")
    ax1.set_title("Gradient norm spikes at a high lr")
    ax1.legend(fontsize=8.5)
    for name, res in results.items():
        ax2.plot(res.losses, label=name, lw=1.3)
    ax2.set_xlabel("step")
    ax2.set_ylabel("cross-entropy loss")
    ax2.set_title(f"Loss at a high lr ({high_lr:g}), with vs without clipping")
    ax2.legend(fontsize=8.5)
    fig.tight_layout()
    return str(save(fig, "09_grad_clipping")), results


def _fig_batch_size(target_tokens: int = 32 * 32 * 400) -> tuple[str, dict[int, TrainResult]]:
    style()
    cfg = ToyLMConfig()
    seq_len = 32
    batch_sizes = [8, 32, 128]
    results = {}
    for bs in batch_sizes:
        n_batches = target_tokens // (bs * seq_len)
        batches = _default_batches(batch_size=bs, seq_len=seq_len, n_batches=n_batches, seed=3)
        results[bs] = train_toy_lm(cfg, batches, lambda p: AdamW(p, lr=3e-3))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8))
    for bs, res in results.items():
        ax1.plot(res.tokens_seen, res.losses, label=f"batch {bs}", lw=1.2, alpha=0.85)
    ax1.set_xlabel("tokens seen")
    ax1.set_ylabel("cross-entropy loss")
    ax1.set_title("Same tokens seen, three batch sizes\nsmall batch = noisier gradient, same eventual loss")
    ax1.legend(fontsize=9)

    _fig_grad_accum_schematic(ax2)
    fig.tight_layout()
    return str(save(fig, "09_batch_size")), results


def _fig_grad_accum_schematic(ax: plt.Axes) -> None:
    """Draw, on a given axis, micro-batches accumulating into one optimizer step."""
    micro = 4
    for i in range(micro):
        x0 = i * 1.6
        ax.add_patch(plt.Rectangle((x0, 1.6), 1.3, 1.0, facecolor="#1f77b4", alpha=0.75, edgecolor="k"))
        ax.text(x0 + 0.65, 2.1, f"micro-batch {i+1}\nforward+backward", ha="center", va="center",
                fontsize=7.5, color="white")
        ax.annotate("", xy=(x0 + 0.65, 1.5), xytext=(x0 + 0.65, 0.95),
                    arrowprops={"arrowstyle": "->", "lw": 1.2})
    ax.add_patch(plt.Rectangle((0, 0.0), micro * 1.6 - 0.3, 0.9, facecolor="#2ca02c", alpha=0.75, edgecolor="k"))
    ax.text((micro * 1.6 - 0.3) / 2, 0.45, "grads summed -> one optimizer.step()", ha="center", va="center",
            fontsize=8.5, color="white", weight="bold")
    ax.set_xlim(-0.3, micro * 1.6 + 0.3)
    ax.set_ylim(-0.3, 3.0)
    ax.axis("off")
    ax.set_title("Gradient accumulation: several small forward/backward passes\n"
                 "before one weight update = one large effective batch, less memory")


def _fig_precision() -> str:
    style()
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))

    ax = axes[0]
    magnitudes = np.array([1e-4, 1e-2, 1.0, 1e2, 1e4, 1e8, 1e30])
    dtypes = {"fp32": torch.float32, "bf16": torch.bfloat16, "fp16": torch.float16}
    x = np.arange(len(magnitudes))
    width = 0.25
    for i, (name, dtype) in enumerate(dtypes.items()):
        spacing = []
        for m in magnitudes:
            t = torch.tensor(m, dtype=dtype)
            nxt = torch.nextafter(t, torch.tensor(float("inf"), dtype=dtype))
            gap = (nxt - t).float().item()
            spacing.append(gap if np.isfinite(gap) and gap > 0 else np.nan)
        ax.bar(x + (i - 1) * width, spacing, width=width, label=name)
    ax.set_yscale("log")
    ax.set_xticks(x, [f"{m:.0e}" for m in magnitudes], rotation=30)
    ax.set_xlabel("magnitude")
    ax.set_ylabel("gap to the next representable value")
    ax.set_title("Representable spacing by magnitude\nbf16 stays finite far out (fp32's exponent range); "
                 "fp16 overflows to inf past ~65504", fontsize=9.5)
    ax.legend(fontsize=8.5)

    ax2 = axes[1]
    sums = {}
    for name, dtype in dtypes.items():
        acc = torch.zeros((), dtype=dtype)
        step = torch.tensor(1e-3, dtype=dtype)
        for _ in range(1000):
            acc = acc + step
        sums[name] = acc.float().item()
    names = list(sums.keys())
    values = [sums[n] for n in names]
    bars = ax2.bar(names, values, color=["#1f77b4", "#2ca02c", "#d62728"])
    ax2.axhline(1.0, color="#333333", ls="--", lw=1, label="exact answer = 1.0")
    for bar, v in zip(bars, values):
        ax2.text(bar.get_x() + bar.get_width() / 2, v, f"{v:.4f}", ha="center", va="bottom", fontsize=9)
    ax2.set_ylabel("sum of 1e-3 added 1000 times")
    ax2.set_title("Low-precision accumulation error\nfp16/bf16 round each addition; fp32 stays close to exact",
                  fontsize=9.5)
    ax2.legend(fontsize=8.5)
    fig.tight_layout()
    return str(save(fig, "09_precision"))


def _fig_scaling_law(target_tokens: int = 32 * 32 * 300) -> tuple[str, dict[int, TrainResult]]:
    style()
    seq_len = 32
    sizes = {
        "small (d=32)": ToyLMConfig(d_model=32, n_heads=2, n_kv_heads=1, head_dim=16, d_ff=64),
        "medium (d=64)": ToyLMConfig(d_model=64, n_heads=4, n_kv_heads=2, head_dim=16, d_ff=128),
        "large (d=128)": ToyLMConfig(d_model=128, n_heads=4, n_kv_heads=2, head_dim=32, d_ff=256),
    }
    results = {}
    param_counts = {}
    for name, cfg in sizes.items():
        n_batches = target_tokens // (32 * seq_len)
        batches = _default_batches(batch_size=32, seq_len=seq_len, n_batches=n_batches, seed=4)
        res = train_toy_lm(cfg, batches, lambda p: AdamW(p, lr=3e-3))
        results[name] = res
        param_counts[name] = ToyTransformerLM(cfg).num_params()

    fig, ax = plt.subplots(figsize=(9, 5.0))
    ns = [param_counts[name] for name in sizes]
    final_losses = [np.mean(results[name].losses[-20:]) for name in sizes]
    ax.plot(ns, final_losses, "o-", ms=9, color="#1f77b4", label="our toy LMs (real losses, equal tokens)")
    for name, n, loss in zip(sizes, ns, final_losses):
        ax.annotate(name, (n, loss), textcoords="offset points", xytext=(8, 6), fontsize=8.5)

    n_schematic = np.logspace(np.log10(min(ns) * 0.7), np.log10(max(ns) * 4), 50)
    schematic = final_losses[0] * (min(ns) / n_schematic) ** 0.10 * 0.6 + 1.0
    ax.plot(n_schematic, schematic, "--", color="#d62728", label="published L(N) shape (schematic, not fitted)")

    ax.set_xscale("log")
    ax.set_xlabel("parameters (log scale)")
    ax.set_ylabel("loss (final, averaged over last 20 steps)")
    ax.set_title("Loss vs model size at equal tokens seen\n"
                 "our 3 toy sizes are real runs; the dashed curve only illustrates the published power-law shape")
    ax.legend(fontsize=8.5)
    return str(save(fig, "09_scaling_law")), results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

_CACHE: dict = {}


@app.command()
def plots() -> None:
    """Regenerate the nine figures for this chapter."""
    print(f"wrote: {_fig_optimizers_path()}")
    print(f"wrote: {_fig_lr_schedules()}")
    path, _CACHE["lr_sweep"] = _fig_toy_lm_lr_sweep()
    print(f"wrote: {path}")
    path, _CACHE["schedule"] = _fig_toy_lm_schedule()
    print(f"wrote: {path}")
    path, _CACHE["clipping"] = _fig_grad_clipping()
    print(f"wrote: {path}")
    path, _CACHE["batch_size"] = _fig_batch_size()
    print(f"wrote: {path}")
    print(f"wrote: {_fig_precision()}")
    path, _CACHE["scaling"] = _fig_scaling_law()
    print(f"wrote: {path}")


@app.command()
def demo() -> None:
    """Print the final losses and wall times quoted in the chapter."""
    t0 = time.perf_counter()
    print("LR sweep (AdamW, 400 steps, toy LM):")
    _, lr_results = _fig_toy_lm_lr_sweep()
    for lr, res in lr_results.items():
        tag = "DIVERGED" if res.diverged else f"final loss {res.losses[-1]:.3f}"
        print(f"  lr={lr:g}: {tag}  ({res.wall_time:.2f}s)")

    print("\nSchedule comparison (AdamW, lr=1e-2 peak, 400 steps):")
    _, sched_results = _fig_toy_lm_schedule()
    for name, res in sched_results.items():
        print(f"  {name:16s}: final loss {res.losses[-1]:.3f}  ({res.wall_time:.2f}s)")

    print("\nGradient clipping (AdamW, lr=8e-2, 200 steps):")
    _, clip_results = _fig_grad_clipping()
    for name, res in clip_results.items():
        tag = "DIVERGED" if res.diverged else f"final loss {res.losses[-1]:.3f}"
        print(f"  {name:12s}: {tag}  ({res.wall_time:.2f}s)")

    print("\nBatch size (equal tokens seen):")
    _, batch_results = _fig_batch_size()
    for bs, res in batch_results.items():
        print(f"  batch={bs:4d}: final loss {res.losses[-1]:.3f}, {len(res.losses)} steps  ({res.wall_time:.2f}s)")

    print("\nScaling law (equal tokens, 3 toy sizes):")
    _, scale_results = _fig_scaling_law()
    for name, res in scale_results.items():
        print(f"  {name:14s}: final loss {np.mean(res.losses[-20:]):.3f}  ({res.wall_time:.2f}s)")

    print(f"\ntotal demo wall time: {time.perf_counter() - t0:.1f}s")


if __name__ == "__main__":
    app()
