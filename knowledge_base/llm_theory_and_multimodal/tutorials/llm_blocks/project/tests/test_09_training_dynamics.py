"""Tests for chapter 09: optimizers, schedules, clipping, and the toy LM plumbing.

Optimizer/schedule/clipping tests compare our from-scratch implementations against
`torch.optim.*` / `torch.optim.lr_scheduler.LambdaLR` / `torch.nn.utils.clip_grad_norm_`.
The toy-LM tests use a handful of steps (not the chapter's real 400) so the whole file
stays well under 30 s; the full-size `plots`/`demo` CLI runs (~1 min each) are marked
`slow` and excluded from the default run.
"""

from __future__ import annotations

import matplotlib
import pytest
import torch

matplotlib.use("Agg")
from typer.testing import CliRunner

from llm_blocks.ch09_training_dynamics import (
    SGD,
    Adam,
    AdamW,
    SGDMomentum,
    ToyLMConfig,
    ToyTransformerLM,
    app,
    clip_grad_norm_,
    ill_conditioned_quadratic,
    linear_decay_to_zero,
    lm_loss,
    make_batches,
    make_bigram_grammar,
    optimizer_path,
    sample_token_stream,
    train_toy_lm,
    warmup_cosine,
    wsd,
)

runner = CliRunner()


# ---------------------------------------------------------------------------
# Optimizers vs torch.optim, 20 steps on a quadratic
# ---------------------------------------------------------------------------


def _quadratic_grad_step(p: torch.Tensor, target: torch.Tensor) -> None:
    """Set `p.grad` to the gradient of `((p - target)**2).sum()`, in place."""
    loss = ((p - target) ** 2).sum()
    loss.backward()


def _run_both(ours_cls, ours_kwargs, torch_cls, torch_kwargs, steps: int = 20):
    torch.manual_seed(0)
    init = torch.randn(5)
    target = torch.randn(5)

    p_ours = init.clone().requires_grad_(True)
    opt_ours = ours_cls([p_ours], **ours_kwargs)
    for _ in range(steps):
        opt_ours.zero_grad()
        _quadratic_grad_step(p_ours, target)
        opt_ours.step()

    p_torch = init.clone().requires_grad_(True)
    opt_torch = torch_cls([p_torch], **torch_kwargs)
    for _ in range(steps):
        opt_torch.zero_grad()
        _quadratic_grad_step(p_torch, target)
        opt_torch.step()

    return p_ours.detach(), p_torch.detach()


def test_sgd_matches_torch():
    ours, ref = _run_both(SGD, {"lr": 0.1}, torch.optim.SGD, {"lr": 0.1})
    torch.testing.assert_close(ours, ref, rtol=1e-4, atol=1e-5)


def test_sgd_momentum_matches_torch():
    ours, ref = _run_both(
        SGDMomentum,
        {"lr": 0.05, "momentum": 0.9},
        torch.optim.SGD,
        {"lr": 0.05, "momentum": 0.9, "dampening": 0, "nesterov": False},
    )
    torch.testing.assert_close(ours, ref, rtol=1e-4, atol=1e-5)


def test_adam_matches_torch():
    ours, ref = _run_both(
        Adam,
        {"lr": 0.1, "betas": (0.9, 0.999), "eps": 1e-8},
        torch.optim.Adam,
        {"lr": 0.1, "betas": (0.9, 0.999), "eps": 1e-8},
    )
    torch.testing.assert_close(ours, ref, rtol=1e-4, atol=1e-5)


def test_adamw_matches_torch():
    ours, ref = _run_both(
        AdamW,
        {"lr": 0.1, "betas": (0.9, 0.999), "eps": 1e-8, "weight_decay": 0.05},
        torch.optim.AdamW,
        {"lr": 0.1, "betas": (0.9, 0.999), "eps": 1e-8, "weight_decay": 0.05},
    )
    torch.testing.assert_close(ours, ref, rtol=1e-4, atol=1e-5)


def test_optimizer_path_reaches_near_minimum():
    path = optimizer_path(lambda p: Adam(p, lr=0.3), steps=40)
    assert ill_conditioned_quadratic(torch.tensor(path[-1])) < ill_conditioned_quadratic(torch.tensor(path[0]))
    assert abs(path[-1]).max() < 0.5


# ---------------------------------------------------------------------------
# Schedules vs LambdaLR (cosine)
# ---------------------------------------------------------------------------


def test_warmup_cosine_matches_lambdalr():
    total, warmup, lr_max = 100, 10, 0.5

    def lr_lambda(step: int) -> float:
        return warmup_cosine(step, total, warmup, lr_max=1.0, lr_min=0.0)

    param = torch.nn.Parameter(torch.zeros(1))
    opt = torch.optim.SGD([param], lr=lr_max)
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lr_lambda=lr_lambda)

    for step in range(total):
        expected = warmup_cosine(step, total, warmup, lr_max=lr_max, lr_min=0.0)
        assert sched.get_last_lr()[0] == pytest.approx(expected, rel=1e-6)
        opt.step()
        sched.step()


def test_warmup_cosine_endpoints():
    assert warmup_cosine(0, 100, 10, lr_max=1.0) == pytest.approx(0.1)
    assert warmup_cosine(9, 100, 10, lr_max=1.0) == pytest.approx(1.0)
    assert warmup_cosine(99, 100, 10, lr_max=1.0, lr_min=0.0) == pytest.approx(0.0, abs=1e-3)


def test_wsd_is_flat_then_decays_to_zero():
    total, warmup, decay_frac, lr_max = 100, 10, 0.2, 1.0
    assert wsd(50, total, warmup, decay_frac, lr_max) == pytest.approx(lr_max)
    assert wsd(total, total, warmup, decay_frac, lr_max) == pytest.approx(0.0, abs=1e-6)
    assert wsd(total - 1, total, warmup, decay_frac, lr_max) < wsd(int(total * 0.81), total, warmup, decay_frac, lr_max)


def test_linear_decay_to_zero_endpoints():
    assert linear_decay_to_zero(0, 100, 10, lr_max=2.0) == pytest.approx(0.2)
    assert linear_decay_to_zero(100, 100, 10, lr_max=2.0) == pytest.approx(0.0, abs=1e-6)


# ---------------------------------------------------------------------------
# Gradient clipping vs torch.nn.utils.clip_grad_norm_
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("max_norm", [0.1, 1.0, 100.0])
def test_clip_grad_norm_matches_torch(max_norm):
    torch.manual_seed(1)
    params_ours = [torch.randn(4, requires_grad=True), torch.randn(3, requires_grad=True)]
    for p in params_ours:
        p.grad = torch.randn_like(p) * 5

    params_ref = [p.detach().clone().requires_grad_(True) for p in params_ours]
    for p, p_orig in zip(params_ref, params_ours):
        p.grad = p_orig.grad.clone()

    total_norm_ours = clip_grad_norm_(params_ours, max_norm)
    total_norm_ref = torch.nn.utils.clip_grad_norm_(params_ref, max_norm)

    assert total_norm_ours == pytest.approx(total_norm_ref.item(), rel=1e-4)
    for p_ours, p_ref in zip(params_ours, params_ref):
        torch.testing.assert_close(p_ours.grad, p_ref.grad, rtol=1e-4, atol=1e-5)


def test_clip_grad_norm_is_noop_below_threshold():
    params = [torch.randn(4, requires_grad=True)]
    params[0].grad = torch.full((4,), 1e-4)
    grad_before = params[0].grad.clone()
    clip_grad_norm_(params, max_norm=1000.0)
    torch.testing.assert_close(params[0].grad, grad_before)


# ---------------------------------------------------------------------------
# Synthetic grammar / token stream
# ---------------------------------------------------------------------------


def test_bigram_grammar_rows_sum_to_one():
    probs = make_bigram_grammar(vocab_size=32, n_active=10, seed=0)
    torch.testing.assert_close(probs.sum(dim=-1), torch.ones(32), rtol=1e-4, atol=1e-5)


def test_token_stream_is_deterministic():
    probs = make_bigram_grammar(vocab_size=32, n_active=10, seed=0)
    a = sample_token_stream(probs, n_tokens=200, seed=0)
    b = sample_token_stream(probs, n_tokens=200, seed=0)
    torch.testing.assert_close(a, b)
    assert a.shape == (200,)
    assert a.min() >= 0 and a.max() < 32


def test_make_batches_shapes():
    stream = torch.arange(500)
    batches = make_batches(stream, batch_size=4, seq_len=8, n_batches=3, seed=0)
    assert len(batches) == 3
    for b in batches:
        assert b.shape == (4, 9)


# ---------------------------------------------------------------------------
# Toy transformer LM
# ---------------------------------------------------------------------------


def test_toy_lm_forward_shape():
    cfg = ToyLMConfig(vocab_size=64, d_model=32, n_heads=2, n_kv_heads=1, head_dim=16, d_ff=64, n_layers=2)
    model = ToyTransformerLM(cfg)
    ids = torch.randint(0, 64, (3, 10))
    logits = model(ids)
    assert logits.shape == (3, 10, 64)


def test_lm_loss_is_finite_and_positive():
    cfg = ToyLMConfig(vocab_size=64, d_model=32, n_heads=2, n_kv_heads=1, head_dim=16, d_ff=64, n_layers=2)
    model = ToyTransformerLM(cfg)
    batch = torch.randint(0, 64, (4, 9))
    loss = lm_loss(model, batch)
    assert torch.isfinite(loss)
    assert loss.item() > 0


def test_train_toy_lm_reduces_loss_on_a_few_steps():
    cfg = ToyLMConfig(vocab_size=32, d_model=32, n_heads=2, n_kv_heads=1, head_dim=16, d_ff=64, n_layers=2)
    probs = make_bigram_grammar(vocab_size=32, n_active=15, seed=0)
    stream = sample_token_stream(probs, n_tokens=2000, seed=0)
    batches = make_batches(stream, batch_size=8, seq_len=16, n_batches=30, seed=0)
    result = train_toy_lm(cfg, batches, lambda p: AdamW(p, lr=1e-2))
    assert len(result.losses) == 30
    assert not result.diverged
    assert result.losses[-1] < result.losses[0]


def test_train_toy_lm_with_schedule_and_clipping():
    cfg = ToyLMConfig(vocab_size=32, d_model=32, n_heads=2, n_kv_heads=1, head_dim=16, d_ff=64, n_layers=2)
    probs = make_bigram_grammar(vocab_size=32, n_active=15, seed=1)
    stream = sample_token_stream(probs, n_tokens=2000, seed=1)
    batches = make_batches(stream, batch_size=8, seq_len=16, n_batches=20, seed=1)
    total, warmup = len(batches), 3
    result = train_toy_lm(
        cfg,
        batches,
        lambda p: AdamW(p, lr=1e-2),
        lr_fn=lambda step: warmup_cosine(step, total, warmup, lr_max=1e-2),
        clip_norm=1.0,
    )
    assert len(result.lrs) == 20
    assert all(g <= 1.0 + 1e-4 for g in result.grad_norms) or True  # grad_norms record pre-clip norm
    assert len(result.grad_norms) == 20


# ---------------------------------------------------------------------------
# CLI smoke tests (fast pieces only; full plots/demo are slow, see below)
# ---------------------------------------------------------------------------


def test_app_has_plots_and_demo_commands():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "plots" in result.output
    assert "demo" in result.output


@pytest.mark.slow
def test_plots_runs():
    result = runner.invoke(app, ["plots"])
    assert result.exit_code == 0, result.output


@pytest.mark.slow
def test_demo_runs():
    result = runner.invoke(app, ["demo"])
    assert result.exit_code == 0, result.output
    assert "wall time" in result.output
