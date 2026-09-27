"""Chapter 07 — linear attention, the delta rule, Gated DeltaNet and the 3:1 hybrid stack.

`uv run python -m llm_blocks.ch07_linear_attention plots` draws the six CPU figures
(no downloads); `plots-real` draws the two figures that read the real Qwen3.5-0.8B /
Qwen3.8-27B configs (config download only, no weights); `demo` prints the cost and
memory numbers quoted in the chapter.

Tensor layout convention in this module: `(B, T, H, D)` — batch, time, head, head dim —
because that is the layout `transformers`' Gated DeltaNet kernels take, so our functions
and the reference ones can be compared without any reshaping gymnastics.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn.functional as F
import typer
from torch import Tensor, nn

from llm_blocks.ch03_attention import kv_cache_bytes
from llm_blocks.plotting import save, style

app = typer.Typer(add_completion=False, no_args_is_help=False)

QWEN35_08B_ID = "Qwen/Qwen3.5-0.8B"
QWEN38_27B_ID = "Qwen/Qwen3.8-27B"


# ---------------------------------------------------------------------------
# 1. What one layer costs: FLOP counters
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class LayerGeometry:
    """The shapes of one transformer layer, verified against the real configs.

    Defaults are Qwen3.8-27B; `QWEN35_08B` below is the small sibling. `n_heads` /
    `n_kv_heads` / `head_dim` describe a full-attention layer, the `linear_*` fields a
    Gated DeltaNet layer.
    """

    hidden_size: int = 5120
    n_heads: int = 24
    n_kv_heads: int = 4
    head_dim: int = 256
    linear_num_v_heads: int = 48
    linear_num_k_heads: int = 16
    linear_head_dim: int = 128
    conv_kernel: int = 4
    n_layers: int = 64
    n_attention_layers: int = 16  # 3:1 hybrid -> every 4th layer


QWEN38_27B = LayerGeometry()
QWEN35_08B = LayerGeometry(
    hidden_size=1024,
    n_heads=8,
    n_kv_heads=2,
    head_dim=256,
    linear_num_v_heads=16,
    linear_num_k_heads=16,
    linear_head_dim=128,
    n_layers=24,
    n_attention_layers=6,
)


def softmax_attention_cost(seq: int, geom: LayerGeometry = QWEN38_27B) -> int:
    """Multiply-add FLOPs of one full-attention layer on a `seq`-token prompt.

    Counting `2*m*n*k` for an `(m, k) @ (k, n)` product: the four projections (linear in
    `seq`) plus the two attention matmuls `q @ k^T` and `weights @ v` (quadratic in `seq`).
    The causal mask means only half the score matrix is really needed; we count the full
    matrix because that is what a dense implementation computes — the shape of the curve
    is the same either way.
    """
    d, h, kv, hd = geom.hidden_size, geom.n_heads, geom.n_kv_heads, geom.head_dim
    proj = 2 * seq * d * (h * hd)  # q_proj
    proj += 2 * 2 * seq * d * (kv * hd)  # k_proj + v_proj
    proj += 2 * seq * (h * hd) * d  # o_proj
    quadratic = 2 * (2 * h * seq * seq * hd)  # scores + weighted sum of values
    return proj + quadratic


def linear_attention_cost(seq: int, geom: LayerGeometry = QWEN38_27B) -> int:
    """Multiply-add FLOPs of one Gated DeltaNet layer on a `seq`-token prompt.

    Every term is linear in `seq`: the projections, the short depthwise convolution, and
    the recurrent rule itself, which touches the fixed `head_k_dim x head_v_dim` state a
    constant number of times per token (decay, read, write, output ~ 6 passes over it).
    """
    d, hv, hk, hd = geom.hidden_size, geom.linear_num_v_heads, geom.linear_num_k_heads, geom.linear_head_dim
    key_dim, value_dim = hk * hd, hv * hd
    conv_dim = 2 * key_dim + value_dim
    proj = 2 * seq * d * conv_dim  # in_proj_qkv
    proj += 2 * seq * d * value_dim  # in_proj_z (the output gate)
    proj += 2 * 2 * seq * d * hv  # in_proj_a + in_proj_b (alpha, beta)
    proj += 2 * seq * value_dim * d  # out_proj
    conv = 2 * seq * conv_dim * geom.conv_kernel
    rule = 6 * seq * hv * hd * hd  # decay, read, write, output on a (hd x hd) state
    return proj + conv + rule


def recurrent_state_bytes(geom: LayerGeometry = QWEN38_27B, dtype_bytes: int = 2) -> int:
    """Bytes of "cache" one Gated DeltaNet layer keeps: the `d_k x d_v` state per value
    head plus the short convolution's `kernel-1` token window. It does **not** depend on
    the sequence length — that is the whole point of the mechanism.
    """
    hd = geom.linear_head_dim
    state = geom.linear_num_v_heads * hd * hd
    conv_dim = 2 * geom.linear_num_k_heads * hd + geom.linear_num_v_heads * hd
    conv = conv_dim * (geom.conv_kernel - 1)
    return (state + conv) * dtype_bytes


# ---------------------------------------------------------------------------
# 2. Linear attention: the same thing written two ways
# ---------------------------------------------------------------------------


def elu_feature_map(x: Tensor) -> Tensor:
    """`phi(x) = elu(x) + 1`, the standard positive feature map of Katharopoulos et al.
    (2020). Softmax attention needs non-negative weights; dropping the softmax loses that,
    so a feature map that is always > 0 is applied to q and k instead."""
    return F.elu(x) + 1.0


def linear_attention_parallel(q: Tensor, k: Tensor, v: Tensor) -> Tensor:
    """Parallel form: `out = ((phi(q) phi(k)^T) * causal_mask) @ v`.

    Same shape of computation as softmax attention (a `T x T` matrix) but *without* the
    softmax, which is exactly what makes the recurrent form below possible. Inputs are
    `(B, T, H, D)`; the output is `(B, T, H, D_v)`.
    """
    qh, kh, vh = (x.transpose(1, 2) for x in (q, k, v))  # -> (B, H, T, D)
    scores = elu_feature_map(qh) @ elu_feature_map(kh).transpose(-1, -2)  # (B, H, T, T)
    t = q.shape[1]
    mask = torch.ones(t, t, dtype=torch.bool, device=q.device).tril()
    out = (scores * mask) @ vh
    return out.transpose(1, 2)


def linear_attention_recurrent(q: Tensor, k: Tensor, v: Tensor) -> tuple[Tensor, Tensor]:
    """Recurrent form: `S_t = S_{t-1} + k_t v_t^T`, `o_t = S_t^T q_t`.

    One loop over time carrying a fixed `(D_k, D_v)` matrix `S` — a recurrent neural
    network (RNN) whose hidden state happens to be a matrix. Returns `(out, final_state)`.
    Mathematically identical to `linear_attention_parallel`, but the memory it needs does
    not grow with `T`.
    """
    qh, kh, vh = (elu_feature_map(q.transpose(1, 2)), elu_feature_map(k.transpose(1, 2)), v.transpose(1, 2))
    b, h, t, d_k = kh.shape
    d_v = vh.shape[-1]
    state = torch.zeros(b, h, d_k, d_v, dtype=vh.dtype, device=vh.device)
    out = torch.zeros(b, h, t, d_v, dtype=vh.dtype, device=vh.device)
    for i in range(t):
        state = state + kh[:, :, i].unsqueeze(-1) * vh[:, :, i].unsqueeze(-2)
        out[:, :, i] = (state * qh[:, :, i].unsqueeze(-1)).sum(dim=-2)
    return out.transpose(1, 2), state


def linear_attention(q: Tensor, k: Tensor, v: Tensor, form: str = "parallel") -> Tensor:
    """Dispatch to `linear_attention_parallel` (training-style) or
    `linear_attention_recurrent` (generation-style). Both return the same numbers."""
    if form == "parallel":
        return linear_attention_parallel(q, k, v)
    if form == "recurrent":
        return linear_attention_recurrent(q, k, v)[0]
    raise ValueError(f"form must be 'parallel' or 'recurrent', got {form!r}")


# ---------------------------------------------------------------------------
# 3. The delta rule and the gate
# ---------------------------------------------------------------------------


def gated_delta_rule_recurrent(
    q: Tensor, k: Tensor, v: Tensor, beta: Tensor, alpha: Tensor
) -> tuple[Tensor, Tensor]:
    """Gated DeltaNet's recurrence (Yang et al., ICLR 2025):

        S_t = S_{t-1} * alpha_t * (I - beta_t k_t k_t^T) + beta_t k_t v_t^T
        o_t = S_t^T q_t

    written in the equivalent "read, subtract, write" form the kernels use:
    fade the state by `alpha_t`, read what is currently stored under `k_t`, and write only
    the *difference* between the new value and the old one, scaled by the write strength
    `beta_t`.

    Shapes: `q`, `k` are `(B, T, H, D_k)`, `v` is `(B, T, H, D_v)`, `beta` and `alpha` are
    `(B, T, H)`. Returns `(out, final_state)` with `out` `(B, T, H, D_v)`.
    No scaling and no normalisation happen here — the caller decides (Qwen3.5 L2-normalises
    q and k and scales q by `1/sqrt(D_k)`; see `GatedDeltaNetBlock`).
    """
    qh, kh, vh = (x.transpose(1, 2) for x in (q, k, v))  # -> (B, H, T, D)
    beta_h, alpha_h = beta.transpose(1, 2), alpha.transpose(1, 2)  # -> (B, H, T)
    b, h, t, d_k = kh.shape
    d_v = vh.shape[-1]
    state = torch.zeros(b, h, d_k, d_v, dtype=vh.dtype, device=vh.device)
    out = torch.zeros(b, h, t, d_v, dtype=vh.dtype, device=vh.device)
    for i in range(t):
        k_t, v_t, q_t = kh[:, :, i], vh[:, :, i], qh[:, :, i]
        state = state * alpha_h[:, :, i, None, None]  # let old memories fade
        stored = (state * k_t.unsqueeze(-1)).sum(dim=-2)  # S^T k_t: what is there now
        delta = (v_t - stored) * beta_h[:, :, i, None]  # the correction to write
        state = state + k_t.unsqueeze(-1) * delta.unsqueeze(-2)
        out[:, :, i] = (state * q_t.unsqueeze(-1)).sum(dim=-2)
    return out.transpose(1, 2), state


def delta_rule_recurrent(q: Tensor, k: Tensor, v: Tensor, beta: Tensor) -> tuple[Tensor, Tensor]:
    """Plain DeltaNet (Schlag et al., 2021): the gated rule with `alpha_t = 1` — nothing
    ever fades, but every write first erases whatever that key held:

        S_t = S_{t-1} (I - beta_t k_t k_t^T) + beta_t k_t v_t^T
    """
    return gated_delta_rule_recurrent(q, k, v, beta, torch.ones_like(beta))


def l2norm(x: Tensor, eps: float = 1e-6) -> Tensor:
    """`x / sqrt(sum(x^2) + eps)` — the exact form `transformers`/`fla` use, so our block
    and the reference agree bit-for-bit on short sequences."""
    return x * torch.rsqrt((x * x).sum(dim=-1, keepdim=True) + eps)


# ---------------------------------------------------------------------------
# 4. The full block, mirroring transformers' Qwen3_5GatedDeltaNet
# ---------------------------------------------------------------------------


class RMSNormGated(nn.Module):
    """RMSNorm followed by a SiLU output gate: `w * rms_norm(x) * silu(z)`.

    Same module as `Qwen3_5RMSNormGated`: the norm is applied first, the gate second.
    """

    def __init__(self, dim: int, eps: float = 1e-6) -> None:
        super().__init__()
        self.weight = nn.Parameter(torch.ones(dim))
        self.eps = eps

    def forward(self, x: Tensor, gate: Tensor) -> Tensor:
        normed = x * torch.rsqrt(x.pow(2).mean(dim=-1, keepdim=True) + self.eps)
        return self.weight * normed * F.silu(gate)


class GatedDeltaNetBlock(nn.Module):
    """A from-scratch Gated DeltaNet layer with the same parameters and maths as
    `transformers.models.qwen3_5.modeling_qwen3_5.Qwen3_5GatedDeltaNet` (prefill path,
    no cache).

    Pipeline: one projection produces q, k and v together; a short depthwise causal
    convolution (kernel 4) mixes each channel with its 3 predecessors; two more
    projections produce the per-head write strength `beta = sigmoid(b)` and decay
    `alpha = exp(-exp(A_log) * softplus(a + dt_bias))`; the gated delta rule runs the
    recurrence; a gated RMSNorm and `out_proj` produce the layer output.
    """

    def __init__(
        self,
        hidden_size: int,
        num_k_heads: int,
        num_v_heads: int,
        head_k_dim: int,
        head_v_dim: int,
        conv_kernel_size: int = 4,
        eps: float = 1e-6,
    ) -> None:
        super().__init__()
        self.num_k_heads, self.num_v_heads = num_k_heads, num_v_heads
        self.head_k_dim, self.head_v_dim = head_k_dim, head_v_dim
        self.key_dim, self.value_dim = num_k_heads * head_k_dim, num_v_heads * head_v_dim
        self.conv_kernel_size = conv_kernel_size
        self.conv_dim = 2 * self.key_dim + self.value_dim

        self.in_proj_qkv = nn.Linear(hidden_size, self.conv_dim, bias=False)
        self.in_proj_z = nn.Linear(hidden_size, self.value_dim, bias=False)
        self.in_proj_b = nn.Linear(hidden_size, num_v_heads, bias=False)
        self.in_proj_a = nn.Linear(hidden_size, num_v_heads, bias=False)
        self.conv1d = nn.Conv1d(
            self.conv_dim,
            self.conv_dim,
            kernel_size=conv_kernel_size,
            groups=self.conv_dim,
            padding=conv_kernel_size - 1,
            bias=False,
        )
        self.dt_bias = nn.Parameter(torch.ones(num_v_heads))
        self.A_log = nn.Parameter(torch.log(torch.empty(num_v_heads).uniform_(0.01, 16)))
        self.norm = RMSNormGated(head_v_dim, eps=eps)
        self.out_proj = nn.Linear(self.value_dim, hidden_size, bias=False)

    def forward(self, x: Tensor) -> Tensor:
        """`x` is `(B, T, hidden_size)`; the output has the same shape."""
        b, t, _ = x.shape

        mixed = self.in_proj_qkv(x).transpose(1, 2)  # (B, conv_dim, T)
        mixed = F.silu(self.conv1d(mixed)[:, :, :t]).transpose(1, 2)  # causal: drop the tail
        q, k, v = torch.split(mixed, [self.key_dim, self.key_dim, self.value_dim], dim=-1)
        q = q.reshape(b, t, self.num_k_heads, self.head_k_dim)
        k = k.reshape(b, t, self.num_k_heads, self.head_k_dim)
        v = v.reshape(b, t, self.num_v_heads, self.head_v_dim)

        beta = self.in_proj_b(x).sigmoid()
        alpha = torch.exp(-self.A_log.exp() * F.softplus(self.in_proj_a(x) + self.dt_bias))

        if self.num_v_heads > self.num_k_heads:  # several value heads share one key head
            repeat = self.num_v_heads // self.num_k_heads
            q = q.repeat_interleave(repeat, dim=2)
            k = k.repeat_interleave(repeat, dim=2)

        q = l2norm(q) / math.sqrt(self.head_k_dim)  # the kernels normalise, then scale q
        k = l2norm(k)
        core, _ = gated_delta_rule_recurrent(q, k, v, beta, alpha)

        z = self.in_proj_z(x).reshape(b, t, self.num_v_heads, self.head_v_dim)
        core = self.norm(core, z).reshape(b, t, self.value_dim)
        return self.out_proj(core)


# ---------------------------------------------------------------------------
# 5. Toy associative memory: why plain linear attention needs the delta rule
# ---------------------------------------------------------------------------


def _write_and_read(keys: Tensor, values: Tensor, probes: Tensor, targets: Tensor, use_delta: bool) -> np.ndarray:
    """Write the `(key, value)` stream into one `dim x dim` state, then read each probe key
    back and return the relative error `||retrieved - target|| / ||target||`.

    `use_delta=False` is plain linear attention (`S += k v^T` — values pile up on top of
    each other); `use_delta=True` is the delta rule with `beta = 1`
    (`S += k (v - S^T k)^T` — each write first erases what that key held).
    """
    dim = keys.shape[-1]
    state = torch.zeros(dim, values.shape[-1])
    for k_t, v_t in zip(keys, values):
        target = v_t - (state.T @ k_t) if use_delta else v_t
        state = state + torch.outer(k_t, target)
    retrieved = probes @ state  # row i = S^T probe_i
    return ((retrieved - targets).norm(dim=-1) / targets.norm(dim=-1)).numpy()


def associative_memory_errors(n_pairs: int = 6, dim: int = 16, seed: int = 0) -> dict[str, np.ndarray]:
    """Scenario 1 — `n_pairs` *different* keys written once each, then all read back.

    Both writers suffer here: a `dim x dim` state is a finite memory and non-orthogonal
    keys always leak into each other. The delta rule leaks less, and because keys are unit
    vectors its `I - k k^T` is an exact projection, so the *last* key written comes back
    perfectly.
    """
    torch.manual_seed(seed)
    keys = F.normalize(torch.randn(n_pairs, dim), dim=-1)
    values = torch.randn(n_pairs, dim)
    return {
        "linear attention": _write_and_read(keys, values, keys, values, use_delta=False),
        "delta rule": _write_and_read(keys, values, keys, values, use_delta=True),
    }


def overwrite_errors(n_keys: int = 3, dim: int = 16, seed: int = 0) -> dict[str, np.ndarray]:
    """Scenario 2 — the same `n_keys` keys are written *twice*, with a new value the second
    time; we then ask for the new value. This is the case the delta rule exists for: plain
    linear attention has no way to remove the old value, so it returns roughly
    `old + new`, while the delta rule erases before it writes.
    """
    torch.manual_seed(seed)
    keys = F.normalize(torch.randn(n_keys, dim), dim=-1)
    old_values, new_values = torch.randn(n_keys, dim), torch.randn(n_keys, dim)
    stream_k = torch.cat([keys, keys])
    stream_v = torch.cat([old_values, new_values])
    return {
        "linear attention": _write_and_read(stream_k, stream_v, keys, new_values, use_delta=False),
        "delta rule": _write_and_read(stream_k, stream_v, keys, new_values, use_delta=True),
    }


def state_norm_trace(steps: int = 400, dim: int = 16, alpha: float = 0.98, seed: int = 0) -> dict[str, np.ndarray]:
    """Write a fresh random key -> value pair at every step and record the size of the
    state `||S||_F` for three writers.

    Plain linear attention just adds, so the state grows without bound (like a random walk,
    roughly `sqrt(t)`). The delta rule subtracts before it writes, which already keeps the
    state bounded. The decay gate then sets *where* that bound sits.
    """
    torch.manual_seed(seed)
    keys = F.normalize(torch.randn(steps, dim), dim=-1)
    values = torch.randn(steps, dim) * 0.5

    traces = {}
    for name, a, use_delta in [
        ("plain linear attention (no delta, no gate)", 1.0, False),
        ("delta rule, no gate (alpha = 1)", 1.0, True),
        (f"delta rule + decay gate (alpha = {alpha})", alpha, True),
    ]:
        state = torch.zeros(dim, dim)
        norms = []
        for k_t, v_t in zip(keys, values):
            state = state * a
            target = v_t - state.T @ k_t if use_delta else v_t
            state = state + torch.outer(k_t, target)
            norms.append(state.norm().item())
        traces[name] = np.array(norms)
    return traces


def memory_persistence(
    steps: int = 300,
    dim: int = 16,
    alphas: tuple[float, ...] = (1.0, 0.99, 0.95),
    noise_beta: float = 0.1,
    seed: int = 0,
) -> dict[float, np.ndarray]:
    """How long one memory survives. Write a single key -> value pair at `t = 0`, then keep
    writing unrelated pairs, and at every step read the original key back and record the
    relative error.

    With `alpha = 1` the memory only degrades from interference — here the later writes
    use a small write strength (`noise_beta = 0.1`) so that interference is slow and the
    effect of the gate is visible on its own. With `alpha < 1` the memory is also
    multiplied by `alpha` every step, so it fades on a timescale of about
    `1 / (1 - alpha)` tokens — that is the knob the gate gives the model.
    """
    torch.manual_seed(seed)
    key0 = F.normalize(torch.randn(dim), dim=-1)
    value0 = torch.randn(dim)
    keys = F.normalize(torch.randn(steps, dim), dim=-1)
    values = torch.randn(steps, dim) * 0.5

    out: dict[float, np.ndarray] = {}
    for a in alphas:
        state = torch.outer(key0, value0)
        errors = []
        for k_t, v_t in zip(keys, values):
            state = state * a
            state = state + noise_beta * torch.outer(k_t, v_t - state.T @ k_t)
            errors.append(((state.T @ key0 - value0).norm() / value0.norm()).item())
        out[a] = np.array(errors)
    return out


# ---------------------------------------------------------------------------
# 6. CPU benchmark: our recurrent DeltaNet vs our softmax attention
# ---------------------------------------------------------------------------


BENCH_LENGTHS = (256, 512, 1024, 2048, 4096, 8192)


def _softmax_attention(q: Tensor, k: Tensor, v: Tensor) -> Tensor:
    """`(B, T, H, D)` softmax attention with a causal mask, for the timing comparison."""
    qh, kh, vh = (x.transpose(1, 2) for x in (q, k, v))
    scores = (qh @ kh.transpose(-1, -2)) / math.sqrt(q.shape[-1])
    t = q.shape[1]
    mask = torch.ones(t, t, dtype=torch.bool, device=q.device).tril()
    scores = scores.masked_fill(~mask, float("-inf"))
    return (scores.softmax(dim=-1) @ vh).transpose(1, 2)


def _time_call(fn, min_seconds: float = 0.05, max_reps: int = 50) -> float:
    """Seconds per call: warm up once, then repeat enough times to measure at least
    `min_seconds` in total so short calls are not swamped by timer noise."""
    fn()
    t0 = time.perf_counter()
    fn()
    single = time.perf_counter() - t0
    reps = min(max_reps, max(1, int(min_seconds / max(single, 1e-9))))
    if reps == 1:
        return single
    t0 = time.perf_counter()
    for _ in range(reps):
        fn()
    return (time.perf_counter() - t0) / reps


def bench_cpu(lengths: tuple[int, ...] = BENCH_LENGTHS, dim: int = 64) -> dict[str, list[float]]:
    """Wall time of one layer's mixing step for each sequence length, single head, `d=64`,
    on this CPU. Both implementations are the plain PyTorch ones in this module — no fused
    kernels on either side, so the comparison is about the *shape* of the cost, not
    about which library is faster."""
    times: dict[str, list[float]] = {"softmax attention": [], "gated delta rule": []}
    for t in lengths:
        torch.manual_seed(0)
        q, k, v = (torch.randn(1, t, 1, dim) for _ in range(3))
        beta = torch.rand(1, t, 1)
        alpha = torch.rand(1, t, 1) * 0.02 + 0.98
        qn, kn = l2norm(q), l2norm(k)
        with torch.no_grad():
            times["softmax attention"].append(
                _time_call(lambda q=q, k=k, v=v: _softmax_attention(q, k, v))
            )
            times["gated delta rule"].append(
                _time_call(
                    lambda qn=qn, kn=kn, v=v, beta=beta, alpha=alpha:
                    gated_delta_rule_recurrent(qn, kn, v, beta, alpha)
                )
            )
    return times


FIT_FROM = 1024  # below this the fixed per-call overheads dominate and hide the real slope


def fit_slope(lengths: np.ndarray, seconds: np.ndarray, fit_from: int = FIT_FROM) -> tuple[float, float]:
    """Least-squares fit of `seconds = c * lengths**p` in log-log space; returns `(p, c)`.
    `p` near 2 means quadratic, near 1 means linear.

    Only lengths `>= fit_from` are used: at a few hundred tokens the Python and BLAS
    call overheads are a large share of the measurement and flatten the curve, which
    would make attention look sub-quadratic when it is not."""
    mask = lengths >= fit_from
    p, log_c = np.polyfit(np.log(lengths[mask]), np.log(seconds[mask]), 1)
    return float(p), float(np.exp(log_c))


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------


COST_LENGTHS = np.array([1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144])


def _fig_cost_vs_length() -> str:
    style()
    soft = np.array([softmax_attention_cost(int(n)) for n in COST_LENGTHS], dtype=float)
    lin = np.array([linear_attention_cost(int(n)) for n in COST_LENGTHS], dtype=float)

    fig, ax = plt.subplots(figsize=(9, 5.2))
    ax.loglog(COST_LENGTHS, soft, "o-", color="#d62728", label="full attention (one layer)")
    ax.loglog(COST_LENGTHS, lin, "o-", color="#1f77b4", label="Gated DeltaNet (one layer)")

    s70 = softmax_attention_cost(70_000)
    l70 = linear_attention_cost(70_000)
    ax.axvline(70_000, color="k", ls="--", lw=0.8)
    ax.annotate(
        f"70,000 tokens\nattention {s70 / 1e12:.1f} TFLOP\nDeltaNet {l70 / 1e12:.2f} TFLOP\n"
        f"= {s70 / l70:.0f}x cheaper",
        xy=(70_000, s70),
        xytext=(4000, s70 * 1.4),
        arrowprops={"arrowstyle": "->", "color": "black", "lw": 1.2},
        fontsize=9,
    )
    ax.set_xlabel("prompt length (tokens, log scale)")
    ax.set_ylabel("FLOPs in one layer (log scale)")
    ax.set_title("Cost of one layer vs prompt length, Qwen3.8-27B shapes\n"
                 "attention bends upwards (slope 2); Gated DeltaNet stays a straight slope-1 line")
    ax.legend()
    return str(save(fig, "07_cost_vs_length"))


def _fig_linear_attention_state() -> str:
    style()
    fig, ax = plt.subplots(figsize=(11, 5.0))

    ax.text(3.0, 5.5, "Full attention: a KV cache that grows", ha="center", fontsize=11, weight="bold")
    for i, t in enumerate([1, 2, 3, 4, 5]):
        for j in range(t):
            ax.add_patch(plt.Rectangle((0.4 + i * 1.15, 3.2 + j * 0.32), 0.9, 0.28,
                                       facecolor="#d62728", edgecolor="k", lw=0.4, alpha=0.85))
        ax.text(0.85 + i * 1.15, 2.95, f"t={t}", ha="center", fontsize=8)
    ax.text(3.0, 2.35, "one K and V row per token, per layer\n-> memory and compute both grow with length",
            ha="center", fontsize=9)

    ax.text(9.3, 5.5, "Linear attention: one fixed state matrix", ha="center", fontsize=11, weight="bold")
    for i, t in enumerate([1, 2, 3, 4, 5]):
        x0 = 7.4 + i * 0.78
        ax.add_patch(plt.Rectangle((x0, 3.5), 0.62, 0.62,
                                   facecolor="#1f77b4", edgecolor="k", lw=0.4, alpha=0.85))
        ax.text(x0 + 0.31, 2.95, f"t={t}", ha="center", fontsize=8)
    ax.text(9.3, 2.35, "S (d_k x d_v) is overwritten in place\n-> same size at token 5 and at token 262,144",
            ha="center", fontsize=9)

    ax.text(6.15, 1.2,
            "Qwen3.8-27B: 64 KiB of KV cache per token (16 attention layers)   vs   "
            f"{recurrent_state_bytes() * 48 / 2**20:.1f} MiB of DeltaNet state in total, for any length",
            ha="center", fontsize=9.5,
            bbox={"boxstyle": "round", "facecolor": "#eeeeee", "edgecolor": "gray"})

    ax.set_xlim(0, 12.3)
    ax.set_ylim(0.6, 6.2)
    ax.axis("off")
    ax.set_title("What each mechanism has to remember about the past")
    return str(save(fig, "07_linear_attention_state"))


def _fig_delta_rule() -> str:
    style()
    panels = [
        (associative_memory_errors(), "6 different keys, written once each",
         [f"key {i + 1}" for i in range(6)],
         "a finite memory always leaks: both are imperfect,\nthe delta rule leaks less"),
        (overwrite_errors(), "3 keys, each written twice (value updated)",
         [f"key {i + 1}" for i in range(3)],
         "asking for the NEW value: linear attention still has\nthe old one added in; the delta rule erased it"),
    ]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5.2))
    width = 0.38
    for ax, (errors, title, ticks, note) in zip(axes, panels):
        labels = list(errors)
        x = np.arange(len(ticks))
        ax.bar(x - width / 2, errors[labels[0]], width, color="#d62728", label=labels[0])
        ax.bar(x + width / 2, errors[labels[1]], width, color="#1f77b4", label=labels[1])
        # The LAST key written comes back exactly under the delta rule, so its bar has zero
        # height; say so, otherwise it reads as a missing measurement.
        for xi, err in zip(x, errors[labels[1]]):
            if err < 0.02:
                ax.text(xi + width / 2, 0.03, "0.00\n(exact)", ha="center", va="bottom",
                        fontsize=8, color="#1f77b4")
        ax.set_xticks(x, ticks, fontsize=9)
        ax.set_xlabel("which key we read back")
        ax.set_ylim(0, 1.55)
        means = "   ".join(f"{lb}: {errors[lb].mean():.2f}" for lb in labels)
        ax.set_title(f"{title}\nmean error — {means}", fontsize=10)
        ax.text(0.02, 0.97, note, transform=ax.transAxes, va="top", fontsize=8.5,
                bbox={"boxstyle": "round", "facecolor": "white", "edgecolor": "gray"})
        ax.legend(fontsize=8.5, loc="upper right")
    axes[0].set_ylabel("relative retrieval error  ||retrieved - v|| / ||v||")

    fig.suptitle("One 16x16 state used as an associative memory: write key -> value pairs, then read them back")
    fig.tight_layout()
    return str(save(fig, "07_delta_rule"))


def _fig_gating() -> str:
    style()
    traces = state_norm_trace()
    persistence = memory_persistence()

    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.0))
    for (name, trace), color in zip(traces.items(), ["#9467bd", "#d62728", "#1f77b4"]):
        axes[0].plot(trace, color=color, lw=1.2, label=name)
    axes[0].set_xlabel("token index t")
    axes[0].set_ylabel("size of the state,  ||S||_F")
    axes[0].set_title("How big the memory gets\n(one fresh key -> value pair written per step)")
    axes[0].legend(fontsize=8)
    axes[0].text(0.03, 0.03,
                 "plain accumulation never stops growing;\n"
                 "the delta rule bounds it, the gate lowers the bound",
                 transform=axes[0].transAxes, fontsize=8.5, va="bottom",
                 bbox={"boxstyle": "round", "facecolor": "white", "edgecolor": "gray"})

    for (a, errors), color in zip(persistence.items(), ["#1f77b4", "#2ca02c", "#d62728"]):
        label = f"alpha = {a}" + ("  (no decay)" if a == 1.0 else f"  (~{1 / (1 - a):.0f}-token horizon)")
        axes[1].plot(errors, color=color, lw=1.2, label=label)
        if a < 1.0:
            axes[1].axvline(1 / (1 - a), color=color, ls=":", lw=0.9)
    axes[1].axhline(1.0, color="k", ls="--", lw=0.8)
    axes[1].text(5, 1.02, "error = 1.0 means the memory is gone", fontsize=8)
    axes[1].set_xlabel("tokens written since the memory was stored")
    axes[1].set_ylabel("relative error when reading that memory back")
    axes[1].set_title("How long one memory survives\n(dotted line = the 1/(1-alpha) horizon)")
    axes[1].legend(fontsize=8, loc="lower right")

    fig.suptitle("The decay gate alpha is a forgetting knob: how much of the past the state keeps")
    fig.tight_layout()
    return str(save(fig, "07_gating"))


def _fig_hybrid_stack() -> str:
    style()
    fig, ax = plt.subplots(figsize=(11, 6.0))
    n_groups, per_group = 16, 4
    for g in range(n_groups):
        for j in range(per_group):
            layer = g * per_group + j
            is_attn = (layer + 1) % 4 == 0
            color = "#d62728" if is_attn else "#1f77b4"
            ax.add_patch(plt.Rectangle((j * 1.15, n_groups - 1 - g), 1.0, 0.82,
                                       facecolor=color, edgecolor="k", lw=0.4, alpha=0.85))
            ax.text(j * 1.15 + 0.5, n_groups - 1 - g + 0.41, str(layer),
                    ha="center", va="center", fontsize=7, color="white")
        ax.text(-0.35, n_groups - 1 - g + 0.41, f"group {g}", ha="right", va="center", fontsize=7.5)

    ax.text(5.4, 12.5, "Qwen3.8-27B: 64 layers = 16 x [D D D A]", fontsize=12, weight="bold")
    ax.text(5.4, 10.6,
            "D = Gated DeltaNet (linear attention)\n"
            "   stores: one fixed 128x128 state per value head\n"
            f"   {recurrent_state_bytes() / 2**10:.0f} KiB per layer, whatever the context length\n"
            "   cost per token: constant\n\n"
            "A = full attention (GQA, 24 Q heads / 4 KV heads, head dim 256)\n"
            "   stores: a KV cache, 4 KiB per token per layer\n"
            "   cost per token: grows with everything seen so far\n"
            "   job: precise recall of a specific earlier token",
            fontsize=9.5, va="top",
            bbox={"boxstyle": "round", "facecolor": "#f4f4f4", "edgecolor": "gray"})
    ax.text(5.4, 1.6,
            "At 70,000 tokens: 4.3 GB of KV cache (16 attention layers)\n"
            f"+ {48 * recurrent_state_bytes() / 2**20:.0f} MB of DeltaNet state (48 layers).\n"
            "All-attention would be 17.1 GB.",
            fontsize=9.5, va="top",
            bbox={"boxstyle": "round", "facecolor": "#fff6e5", "edgecolor": "#ff7f0e"})

    ax.set_xlim(-1.6, 13.0)
    ax.set_ylim(-0.4, 16.6)
    ax.axis("off")
    ax.set_title("The 3:1 hybrid stack: three cheap linear layers, then one real attention layer")
    return str(save(fig, "07_hybrid_stack"))


def _fig_cpu_bench() -> str:
    style()
    times = bench_cpu()
    lengths = np.array(BENCH_LENGTHS, dtype=float)
    extrap = np.array([8192, 16384, 32768, 65536, 131072], dtype=float)

    fig, ax = plt.subplots(figsize=(9.5, 5.4))
    fits = {}
    for (name, ts), color in zip(times.items(), ["#d62728", "#1f77b4"]):
        seconds = np.array(ts, dtype=float)
        p, c = fit_slope(lengths, seconds)
        fits[name] = (p, c)
        ax.loglog(lengths, seconds, "o-", color=color,
                  label=f"{name} (measured; fitted slope {p:.2f} above {FIT_FROM} tokens)")
        ax.loglog(extrap, c * extrap**p, ":", color=color, lw=1.1, alpha=0.8)

    # Where the two fitted power laws meet: c_a * n^p_a = c_d * n^p_d
    (p_a, c_a), (p_d, c_d) = fits["softmax attention"], fits["gated delta rule"]
    crossover = float(np.exp((np.log(c_d) - np.log(c_a)) / (p_a - p_d)))
    if lengths[-1] < crossover < extrap[-1]:
        ax.axvline(crossover, color="k", ls="--", lw=0.8)
        ax.annotate(f"extrapolated crossover\n~{crossover / 1000:.0f}k tokens",
                    xy=(crossover, c_a * crossover**p_a), xytext=(0.58, 0.42),
                    textcoords="axes fraction", fontsize=9,
                    arrowprops={"arrowstyle": "->", "color": "black", "lw": 1.0})

    ax.set_xlabel("sequence length (tokens, log scale)")
    ax.set_ylabel("wall time for one layer's mixing step, seconds (log scale)")
    ax.set_title("Measured on this Mac CPU: batch 1, one head, d=64, plain PyTorch on both sides\n"
                 "dotted = the fitted power law extrapolated; slopes are what matter, not constants")
    ax.legend(fontsize=8.5, loc="upper left")
    ax.text(0.02, 0.02,
            f"at 8192 tokens attention is still faster ({times['softmax attention'][-1] * 1e3:.0f} ms vs "
            f"{times['gated delta rule'][-1] * 1e3:.0f} ms):\n"
            "our delta rule is a Python for-loop over tokens, attention is one BLAS matmul.\n"
            "On a GPU the fla chunked kernel removes that constant; the slopes stay 2 and 1.",
            transform=ax.transAxes, fontsize=8.5, va="bottom",
            bbox={"boxstyle": "round", "facecolor": "white", "edgecolor": "gray"})
    return str(save(fig, "07_cpu_bench"))


# ---------------------------------------------------------------------------
# Figures that read the real configs
# ---------------------------------------------------------------------------


def load_text_config(model_id: str):
    """`AutoConfig.from_pretrained(model_id)` reduced to the text config — config download
    only, no weights. Falls back to the 0.8B if the network is unavailable."""
    from transformers import AutoConfig

    try:
        config = AutoConfig.from_pretrained(model_id)
    except OSError:
        config = AutoConfig.from_pretrained(QWEN35_08B_ID)
    return config.get_text_config() if hasattr(config, "get_text_config") else config


def geometry_from_config(config) -> LayerGeometry:
    """Turn a `Qwen3_5TextConfig` into the `LayerGeometry` used by the cost counters."""
    return LayerGeometry(
        hidden_size=config.hidden_size,
        n_heads=config.num_attention_heads,
        n_kv_heads=config.num_key_value_heads,
        head_dim=config.head_dim,
        linear_num_v_heads=config.linear_num_value_heads,
        linear_num_k_heads=config.linear_num_key_heads,
        linear_head_dim=config.linear_key_head_dim,
        conv_kernel=config.linear_conv_kernel_dim,
        n_layers=config.num_hidden_layers,
        n_attention_layers=sum(t == "full_attention" for t in config.layer_types),
    )


def _fig_real_layer_types() -> str:
    style()
    config = load_text_config(QWEN35_08B_ID)
    layer_types = list(config.layer_types)

    fig, ax = plt.subplots(figsize=(12, 2.8))
    for i, kind in enumerate(layer_types):
        is_attn = kind == "full_attention"
        ax.add_patch(plt.Rectangle((i, 0), 0.9, 1.0,
                                   facecolor="#d62728" if is_attn else "#1f77b4",
                                   edgecolor="k", lw=0.4, alpha=0.88))
        ax.text(i + 0.45, 0.5, "A" if is_attn else "D", ha="center", va="center",
                color="white", fontsize=9, weight="bold")
        ax.text(i + 0.45, -0.22, str(i), ha="center", va="center", fontsize=6.5)

    n_attn = sum(t == "full_attention" for t in layer_types)
    ax.set_xlim(-0.4, len(layer_types) + 0.2)
    ax.set_ylim(-0.6, 1.5)
    ax.axis("off")
    ax.set_title(
        f"Qwen3.5-0.8B `layer_types`, read straight from the config: {len(layer_types)} layers, "
        f"{n_attn} full attention (A, red), {len(layer_types) - n_attn} Gated DeltaNet (D, blue)\n"
        "the pattern is [D D D A] repeated — every 4th layer is real attention"
    )
    return str(save(fig, "07_real_layer_types"))


def _fig_real_state_vs_kvcache() -> str:
    style()
    seq = np.array([1024, 4096, 16384, 65536, 262144], dtype=float)
    models = [("Qwen3.5-0.8B", QWEN35_08B_ID), ("Qwen3.8-27B", QWEN38_27B_ID)]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5.0))
    for ax, (title, model_id) in zip(axes, models):
        geom = geometry_from_config(load_text_config(model_id))
        n_linear = geom.n_layers - geom.n_attention_layers
        kv = np.array([
            kv_cache_bytes(geom.n_attention_layers, geom.n_kv_heads, geom.head_dim, int(n)) for n in seq
        ], dtype=float)
        state = np.full_like(seq, recurrent_state_bytes(geom) * n_linear)

        ax.loglog(seq, kv / 2**20, "o-", color="#d62728",
                  label=f"KV cache, {geom.n_attention_layers} attention layers")
        ax.loglog(seq, state / 2**20, "o-", color="#1f77b4",
                  label=f"DeltaNet state, {n_linear} linear layers")
        per_token = kv[0] / seq[0]
        ax.set_title(f"{title}\n{per_token / 1024:.0f} KiB of KV cache per token vs "
                     f"{state[0] / 2**20:.1f} MiB of fixed state")
        ax.set_xlabel("context length (tokens, log scale)")
        ax.set_ylabel("bf16 memory, MiB (log scale)")
        ax.legend(fontsize=8.5)
        ax.axvline(70_000, color="k", ls="--", lw=0.8)
        ax.text(70_000, ax.get_ylim()[0] * 1.6, " 70k", fontsize=8)

    fig.suptitle("What the two layer types cost to remember: the KV cache is a slope-1 line, "
                 "the recurrent state is flat")
    fig.tight_layout()
    return str(save(fig, "07_real_state_vs_kvcache"))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


@app.command()
def plots() -> None:
    """Regenerate the six CPU figures for this chapter (no downloads)."""
    print(f"wrote: {_fig_cost_vs_length()}")
    print(f"wrote: {_fig_linear_attention_state()}")
    print(f"wrote: {_fig_delta_rule()}")
    print(f"wrote: {_fig_gating()}")
    print(f"wrote: {_fig_hybrid_stack()}")
    print(f"wrote: {_fig_cpu_bench()}")


@app.command()
def plots_real() -> None:
    """Regenerate the two figures that read the real Qwen3.5/3.8 configs."""
    print(f"wrote: {_fig_real_layer_types()}")
    print(f"wrote: {_fig_real_state_vs_kvcache()}")


@app.command()
def demo() -> None:
    """Print the cost and memory numbers quoted in the chapter."""
    seq = 70_000
    geom = QWEN38_27B
    soft, lin = softmax_attention_cost(seq, geom), linear_attention_cost(seq, geom)
    print(f"Qwen3.8-27B shapes, prompt of {seq:,} tokens, cost of ONE layer:")
    print(f"  full attention   : {soft / 1e12:8.2f} TFLOP")
    print(f"  Gated DeltaNet   : {lin / 1e12:8.2f} TFLOP   ({soft / lin:.0f}x cheaper)")
    n_linear = geom.n_layers - geom.n_attention_layers
    whole_hybrid = geom.n_attention_layers * soft + n_linear * lin
    whole_dense = geom.n_layers * soft
    print(f"  whole stack, 3:1 hybrid ({geom.n_attention_layers} A + {n_linear} D):"
          f" {whole_hybrid / 1e12:8.2f} TFLOP")
    print(f"  whole stack, all attention (64 A)          : {whole_dense / 1e12:8.2f} TFLOP"
          f"   ({whole_dense / whole_hybrid:.1f}x more)")

    print("\nMemory to carry the past, bf16, one sequence:")
    for title, g in [("Qwen3.8-27B", QWEN38_27B), ("Qwen3.5-0.8B", QWEN35_08B)]:
        n_lin = g.n_layers - g.n_attention_layers
        per_token = kv_cache_bytes(g.n_attention_layers, g.n_kv_heads, g.head_dim, 1)
        state = recurrent_state_bytes(g) * n_lin
        kv70 = kv_cache_bytes(g.n_attention_layers, g.n_kv_heads, g.head_dim, seq)
        all_attn = kv_cache_bytes(g.n_layers, g.n_kv_heads, g.head_dim, seq)
        print(f"  {title}: KV cache {per_token / 1024:.0f} KiB/token -> {kv70 / 2**30:.2f} GB at {seq:,}; "
              f"DeltaNet state {state / 2**20:.0f} MiB (fixed); "
              f"all-attention would be {all_attn / 2**30:.2f} GB")

    print("\nOne layer's mixing step on this CPU (batch 1, one head, d=64):")
    times = bench_cpu()
    print(f"  {'seq':>6}  {'attention':>12}  {'delta rule':>12}")
    for i, t in enumerate(BENCH_LENGTHS):
        print(f"  {t:>6}  {times['softmax attention'][i] * 1e3:>10.2f} ms  "
              f"{times['gated delta rule'][i] * 1e3:>10.2f} ms")
    lengths = np.array(BENCH_LENGTHS, dtype=float)
    for name in times:
        p, _ = fit_slope(lengths, np.array(times[name], dtype=float))
        print(f"  fitted slope, {name}: {p:.2f}")


if __name__ == "__main__":
    app()
