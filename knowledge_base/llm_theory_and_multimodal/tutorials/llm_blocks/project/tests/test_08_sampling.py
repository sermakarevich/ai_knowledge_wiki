"""Tests for chapter 08: decoding strategies, perplexity, the toy generate() loop.

The warper tests compare our from-scratch functions to
`transformers.generation.logits_process` (`TemperatureLogitsWarper`,
`TopKLogitsWarper`, `TopPLogitsWarper`, `MinPLogitsWarper`,
`RepetitionPenaltyLogitsProcessor`), batch size 1, which is what our functions
operate on for a single sequence.
"""

import math
from itertools import pairwise

import matplotlib
import pytest
import torch

matplotlib.use("Agg")
from typer.testing import CliRunner

from llm_blocks.ch08_sampling import (
    app,
    distribution_perplexity,
    entropy,
    frequency_penalty,
    generate,
    greedy,
    greedy_strategy,
    make_bigram_model,
    min_p,
    perplexity,
    presence_penalty,
    repetition_penalty,
    sampling_strategy,
    temperature,
    top_k,
    top_p,
    toy_bigram_table,
    zipfian_logits,
)

runner = CliRunner()


def _random_logits(seed=0, n=30):
    torch.manual_seed(seed)
    return torch.randn(n) * 3.0


# ---------------------------------------------------------------------------
# Warpers vs transformers
# ---------------------------------------------------------------------------


def test_greedy_matches_argmax():
    logits = _random_logits(0)
    assert int(greedy(logits)) == int(logits.argmax())


def test_temperature_matches_transformers():
    from transformers.generation.logits_process import TemperatureLogitsWarper

    logits = _random_logits(1)
    ref = TemperatureLogitsWarper(0.6)(None, logits.unsqueeze(0))[0]
    ours = temperature(logits, 0.6)
    torch.testing.assert_close(ours, ref)


@pytest.mark.parametrize("k", [1, 5, 10, 100])
def test_top_k_matches_transformers(k):
    from transformers.generation.logits_process import TopKLogitsWarper

    logits = _random_logits(2)
    ref = TopKLogitsWarper(k)(None, logits.unsqueeze(0))[0]
    ours = top_k(logits, k)
    torch.testing.assert_close(ours, ref)


@pytest.mark.parametrize("p", [0.1, 0.5, 0.9, 0.99])
def test_top_p_matches_transformers(p):
    from transformers.generation.logits_process import TopPLogitsWarper

    logits = _random_logits(3)
    ref = TopPLogitsWarper(p)(None, logits.unsqueeze(0))[0]
    ours = top_p(logits, p)
    torch.testing.assert_close(ours, ref)


@pytest.mark.parametrize("p", [0.05, 0.1, 0.5])
def test_min_p_matches_transformers(p):
    from transformers.generation.logits_process import MinPLogitsWarper

    logits = _random_logits(4)
    ref = MinPLogitsWarper(p)(None, logits.unsqueeze(0))[0]
    ours = min_p(logits, p)
    torch.testing.assert_close(ours, ref)


@pytest.mark.parametrize("penalty", [1.0, 1.2, 1.8])
def test_repetition_penalty_matches_transformers(penalty):
    from transformers.generation.logits_process import RepetitionPenaltyLogitsProcessor

    logits = _random_logits(5)
    prev_ids = [2, 5, 5, 9, 20]
    ref = RepetitionPenaltyLogitsProcessor(penalty)(
        torch.tensor([prev_ids]), logits.unsqueeze(0).clone()
    )[0]
    ours = repetition_penalty(logits, prev_ids, penalty)
    torch.testing.assert_close(ours, ref)


def test_repetition_penalty_noop_with_no_history():
    logits = _random_logits(6)
    torch.testing.assert_close(repetition_penalty(logits, [], 1.5), logits)


def test_top_k_and_top_p_keep_at_least_one_token():
    logits = _random_logits(7)
    assert (~torch.isinf(top_k(logits, 1))).sum() == 1
    assert (~torch.isinf(top_p(logits, 1e-9))).sum() >= 1
    assert (~torch.isinf(min_p(logits, 0.999))).sum() >= 1


# ---------------------------------------------------------------------------
# presence / frequency penalty (not in transformers, simple additive checks)
# ---------------------------------------------------------------------------


def test_presence_penalty_only_touches_seen_tokens():
    logits = torch.zeros(5)
    out = presence_penalty(logits, [1, 1, 1, 3], penalty=0.5)
    expected = torch.tensor([0.0, -0.5, 0.0, -0.5, 0.0])
    torch.testing.assert_close(out, expected)


def test_frequency_penalty_scales_with_count():
    logits = torch.zeros(5)
    out = frequency_penalty(logits, [1, 1, 1, 3], penalty=0.5)
    expected = torch.tensor([0.0, -1.5, 0.0, -0.5, 0.0])
    torch.testing.assert_close(out, expected)


# ---------------------------------------------------------------------------
# Perplexity and entropy
# ---------------------------------------------------------------------------


def test_perplexity_is_one_when_model_is_always_right():
    logits = torch.full((4, 3), -100.0)
    targets = torch.tensor([0, 1, 2, 0])
    for i, t in enumerate(targets):
        logits[i, t] = 100.0
    assert perplexity(logits, targets) == pytest.approx(1.0, abs=1e-3)


def test_perplexity_is_vocab_size_when_uniform():
    vocab = 16
    logits = torch.zeros(5, vocab)
    targets = torch.randint(0, vocab, (5,))
    assert perplexity(logits, targets) == pytest.approx(vocab, rel=1e-4)


def test_perplexity_matches_manual_cross_entropy():
    torch.manual_seed(8)
    logits = torch.randn(10, 7)
    targets = torch.randint(0, 7, (10,))
    manual = math.exp(torch.nn.functional.cross_entropy(logits, targets).item())
    assert perplexity(logits, targets) == pytest.approx(manual, rel=1e-5)


def test_entropy_zero_for_certain_distribution():
    logits = torch.tensor([100.0, -100.0, -100.0])
    assert entropy(logits).item() == pytest.approx(0.0, abs=1e-4)


def test_entropy_max_for_uniform_distribution():
    n = 6
    logits = torch.zeros(n)
    assert entropy(logits).item() == pytest.approx(math.log(n), rel=1e-5)


def test_distribution_perplexity_matches_vocab_for_uniform():
    n = 9
    assert distribution_perplexity(torch.zeros(n)).item() == pytest.approx(n, rel=1e-4)


def test_distribution_perplexity_is_one_for_certain():
    logits = torch.tensor([100.0, -100.0, -100.0, -100.0])
    assert distribution_perplexity(logits).item() == pytest.approx(1.0, abs=1e-3)


# ---------------------------------------------------------------------------
# generate() with the toy bigram model
# ---------------------------------------------------------------------------


def test_toy_bigram_table_is_deterministic():
    torch.testing.assert_close(toy_bigram_table(seed=0), toy_bigram_table(seed=0))
    assert not torch.allclose(toy_bigram_table(seed=0), toy_bigram_table(seed=1))


def test_generate_greedy_is_deterministic_and_correct_length():
    table = toy_bigram_table(seed=0)
    model_fn = make_bigram_model(table)
    out1 = generate(model_fn, [0], greedy_strategy, max_new=8)
    out2 = generate(model_fn, [0], greedy_strategy, max_new=8)
    assert out1 == out2
    assert len(out1) == 9
    # greedy must always pick argmax of the row for the previous token
    for prev, nxt in pairwise(out1):
        assert nxt == int(table[prev].argmax())


def test_generate_sampling_is_reproducible_with_same_generator_seed():
    table = toy_bigram_table(seed=0)
    model_fn = make_bigram_model(table)
    strat_a = sampling_strategy(temp=0.8, k=5, generator=torch.Generator().manual_seed(42))
    strat_b = sampling_strategy(temp=0.8, k=5, generator=torch.Generator().manual_seed(42))
    out_a = generate(model_fn, [0], strat_a, max_new=10)
    out_b = generate(model_fn, [0], strat_b, max_new=10)
    assert out_a == out_b


def test_generate_sampling_respects_top_k_support():
    table = toy_bigram_table(seed=0)
    model_fn = make_bigram_model(table)
    strat = sampling_strategy(temp=1.0, k=1, generator=torch.Generator().manual_seed(0))
    out = generate(model_fn, [0], strat, max_new=8)
    for prev, nxt in pairwise(out):
        assert nxt == int(table[prev].argmax())  # k=1 collapses sampling to greedy


def test_generate_respects_repetition_penalty_in_strategy():
    table = toy_bigram_table(seed=2)
    model_fn = make_bigram_model(table)
    strat = sampling_strategy(temp=1e-6, rep_penalty=1000.0, generator=torch.Generator().manual_seed(0))
    out = generate(model_fn, [0], strat, max_new=1)
    # near-zero temperature + huge penalty on repeats should still just pick the
    # (unpenalized, since prev_ids only has the prompt token) argmax of row 0
    assert out[1] == int(table[0].argmax())


# ---------------------------------------------------------------------------
# Figure helpers / CLI
# ---------------------------------------------------------------------------


def test_zipfian_logits_is_deterministic_and_decreasing_on_average():
    a = zipfian_logits(seed=0)
    b = zipfian_logits(seed=0)
    torch.testing.assert_close(a, b)
    probs = a.softmax(dim=-1)
    assert probs[:5].mean() > probs[-5:].mean()


def test_plots_runs():
    result = runner.invoke(app, ["plots"])
    assert result.exit_code == 0, result.output


def test_demo_runs():
    result = runner.invoke(app, ["demo"])
    assert result.exit_code == 0, result.output
    assert "Perplexity" in result.output
