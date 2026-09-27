"""Chapter 10 — forgetting mitigations, merging, reporting. CPU only, no network, no downloads.

Everything the chapter *claims* about weight editing is arithmetic, and arithmetic is testable
without a GPU. The three claims under test:

* scaling a LoRA adapter by `lam` scales its effective update `dW = (alpha/r)*B*A` by exactly
  `lam` — not `lam**2`, which is what you get if you scale both factors;
* TIES trims, elects a sign by total magnitude, and averages only the deltas that agree — so a
  lone dissenter is dropped rather than allowed to cancel the majority out;
* `report()` turns per-variant `metrics.json` files into rows whose deltas are in percentage
  points against the baseline.
"""

import json

import pytest
import torch

from llm_tutorial.finetune import FTConfig, build_distill_prompt, build_train_examples
from llm_tutorial.forget import (
    lora_deltas,
    report,
    scale_adapter,
    scale_lora_state_dict,
    summarise_rows,
    ties_merge,
    trim_to_density,
)

ITEMS = [
    {
        "question": "Which protocol operates at layer 3?",
        "answers": {"A": "HTTP", "B": "IP", "C": "TCP", "D": "SMTP"},
        "solution": "B",
    },
    {
        "question": "What does CIA stand for in security?",
        "answers": {"A": "Confidentiality, Integrity, Availability", "B": "Central Intelligence Agency",
                    "C": "Cipher, Integrity, Audit", "D": "Control, Isolation, Access"},
        "solution": "A",
    },
]


# ------------------------------------------------------------------ adapter scaling (lambda)


def _tiny_lora_state() -> dict[str, torch.Tensor]:
    """One LoRA layer's worth of tensors, shaped like peft writes them: A is r x in, B is out x r."""
    torch.manual_seed(0)
    return {
        "base_model.model.model.layers.0.mlp.up_proj.lora_A.weight": torch.randn(2, 3),
        "base_model.model.model.layers.0.mlp.up_proj.lora_B.weight": torch.randn(4, 2),
    }


def test_scale_lora_state_dict_halves_the_delta():
    state = _tiny_lora_state()
    a = state["base_model.model.model.layers.0.mlp.up_proj.lora_A.weight"]
    b = state["base_model.model.model.layers.0.mlp.up_proj.lora_B.weight"]
    delta = b @ a

    scaled = scale_lora_state_dict(state, 0.5)
    scaled_delta = scaled["base_model.model.model.layers.0.mlp.up_proj.lora_B.weight"] @ scaled[
        "base_model.model.model.layers.0.mlp.up_proj.lora_A.weight"
    ]

    torch.testing.assert_close(scaled_delta, 0.5 * delta)
    # A must be untouched — scaling both factors would give 0.25*delta, the classic mistake.
    torch.testing.assert_close(scaled["base_model.model.model.layers.0.mlp.up_proj.lora_A.weight"], a)


def test_scale_lora_state_dict_endpoints():
    state = _tiny_lora_state()
    b_key = "base_model.model.model.layers.0.mlp.up_proj.lora_B.weight"
    assert torch.count_nonzero(scale_lora_state_dict(state, 0.0)[b_key]) == 0
    torch.testing.assert_close(scale_lora_state_dict(state, 1.0)[b_key], state[b_key])


def test_scale_adapter_roundtrip(tmp_path):
    safetensors = pytest.importorskip("safetensors.torch")
    adapter = tmp_path / "adapter"
    adapter.mkdir()
    state = _tiny_lora_state()
    safetensors.save_file(state, str(adapter / "adapter_model.safetensors"))
    (adapter / "adapter_config.json").write_text(json.dumps({"r": 2, "lora_alpha": 4}))

    out = scale_adapter(adapter, 0.25, tmp_path / "scaled")

    assert (out / "adapter_config.json").exists(), "the config must travel with the weights"
    written = safetensors.load_file(str(out / "adapter_model.safetensors"))
    b_key = "base_model.model.model.layers.0.mlp.up_proj.lora_B.weight"
    torch.testing.assert_close(written[b_key], 0.25 * state[b_key])


def test_lora_deltas_applies_alpha_over_r(tmp_path):
    safetensors = pytest.importorskip("safetensors.torch")
    adapter = tmp_path / "adapter"
    adapter.mkdir()
    state = _tiny_lora_state()
    safetensors.save_file(state, str(adapter / "adapter_model.safetensors"))
    (adapter / "adapter_config.json").write_text(json.dumps({"r": 2, "lora_alpha": 4}))

    deltas = lora_deltas(adapter)

    assert list(deltas) == ["model.layers.0.mlp.up_proj.weight"], "peft's key prefix must be stripped"
    a = state["base_model.model.model.layers.0.mlp.up_proj.lora_A.weight"]
    b = state["base_model.model.model.layers.0.mlp.up_proj.lora_B.weight"]
    torch.testing.assert_close(deltas["model.layers.0.mlp.up_proj.weight"], (4 / 2) * (b @ a))


# ------------------------------------------------------------------ TIES


def test_trim_to_density_keeps_the_largest():
    tensor = torch.tensor([[0.1, -0.9, 0.2, 0.05]])
    trimmed = trim_to_density(tensor, 0.5)  # keep 2 of 4
    assert torch.count_nonzero(trimmed) == 2
    torch.testing.assert_close(trimmed, torch.tensor([[0.0, -0.9, 0.2, 0.0]]))


def test_trim_to_density_one_is_a_noop():
    tensor = torch.tensor([[0.1, -0.9, 0.2, 0.05]])
    torch.testing.assert_close(trim_to_density(tensor, 1.0), tensor)


def test_ties_merge_elects_the_majority_sign_and_averages_only_the_agreeing():
    # Entry 0: +0.8 and +0.6 agree -> mean 0.7.
    # Entry 1: +0.9 vs -0.1: the positive side carries more magnitude, so +0.9 wins alone
    #          (a plain sum would have given 0.8, a plain mean 0.4).
    a = torch.tensor([0.8, 0.9])
    b = torch.tensor([0.6, -0.1])

    merged = ties_merge([a, b], density=1.0)

    torch.testing.assert_close(merged, torch.tensor([0.7, 0.9]))


def test_ties_merge_drops_trimmed_entries():
    # density 0.5 on a 4-entry vector keeps the 2 biggest of each delta.
    a = torch.tensor([1.0, 0.9, 0.01, 0.02])
    b = torch.tensor([0.01, 0.02, 1.0, 0.9])

    merged = ties_merge([a, b], density=0.5)

    # Every entry survives in exactly one delta, so each keeps its own value, not a half-mean.
    torch.testing.assert_close(merged, torch.tensor([1.0, 0.9, 1.0, 0.9]))


def test_ties_merge_weights_shift_the_election():
    a = torch.tensor([0.4])
    b = torch.tensor([-0.5])
    # Unweighted, b's larger magnitude wins the sign.
    torch.testing.assert_close(ties_merge([a, b], density=1.0), torch.tensor([-0.5]))
    # Weighting a by 2 flips the election: 2*0.4 = 0.8 > 0.5.
    torch.testing.assert_close(ties_merge([a, b], density=1.0, weights=[2.0, 1.0]), torch.tensor([0.4]))


def test_ties_merge_single_delta_is_a_trim():
    a = torch.tensor([0.5, -0.3])
    torch.testing.assert_close(ties_merge([a], density=1.0), a)


def test_ties_merge_rejects_empty():
    with pytest.raises(ValueError):
        ties_merge([])


# ------------------------------------------------------------------ self-distillation data


def test_build_train_examples_self_distill_uses_the_models_own_wording():
    items = [{**ITEMS[0], "self_answer": "B) IP. The Internet Protocol routes packets, which is layer 3."}]
    (example,) = build_train_examples(items, style="mcq_self_distill")
    assistant = example["messages"][-1]["content"]
    assert assistant.startswith("B)"), "the evaluator parses the first letter — it must come first"
    assert "routes packets" in assistant


def test_build_train_examples_self_distill_repairs_a_missing_letter():
    items = [{**ITEMS[0], "self_answer": "The Internet Protocol routes packets."}]
    (example,) = build_train_examples(items, style="mcq_self_distill")
    assistant = example["messages"][-1]["content"]
    assert assistant.startswith("B) IP"), "a reply without the letter must be prefixed with it"
    assert "routes packets" in assistant


def test_build_train_examples_self_distill_falls_back_to_the_canned_answer():
    (example,) = build_train_examples([ITEMS[0]], style="mcq_self_distill")
    assert example["messages"][-1]["content"] == "B) IP"


def test_build_distill_prompt_tells_the_model_the_answer():
    prompt = build_distill_prompt(ITEMS[0])
    assert "The correct answer is B) IP." in prompt
    assert ITEMS[0]["question"] in prompt


def test_self_distill_is_a_valid_config_format():
    cfg = FTConfig.model_validate({
        "run_name": "forget/selfdistill",
        "base": "Qwen/Qwen3.5-4B",
        "data": {"train_file": "runs/data/cybermetric/train_selfdistill.json",
                 "format": "mcq_self_distill"},
    })
    assert cfg.data.format == "mcq_self_distill"
    # A slash in run_name must still give a sane run dir — chapter 10 relies on it.
    assert cfg.run_dir.as_posix() == "runs/forget/selfdistill"
    assert cfg.adapter_dir.as_posix() == "runs/forget/selfdistill/adapter"


# ------------------------------------------------------------------ report()


def _general(mmlu: float, gsm8k: float) -> dict:
    return {
        "mmlu": {"metric": "acc", "value": mmlu, "stderr": 0.01},
        "gsm8k": {"metric": "exact_match", "value": gsm8k, "stderr": 0.02},
    }


def _write(run_dir, payload):
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "metrics.json").write_text(json.dumps(payload))


@pytest.fixture()
def forget_runs(tmp_path, monkeypatch):
    """Three fake variants plus a baseline, laid out exactly as `run_all` would leave them."""
    monkeypatch.chdir(tmp_path)
    out_dir = tmp_path / "runs" / "forget"
    _write(out_dir / "base", {
        "name": "base", "model": "Qwen/Qwen3.5-4B",
        "domain": {"accuracy": 0.50, "ci95": [0.45, 0.55]},
        "general": _general(0.60, 0.40), "general_mean": 0.50,
        "perplexity": {"domain": {"nll": 1.0}, "general": {"nll": 2.0}},
    })
    _write(out_dir / "naive", {
        "name": "naive", "kind": "reuse",
        "domain": {"accuracy": 0.70, "ci95": [0.65, 0.75]},
        "general": _general(0.50, 0.30), "general_mean": 0.40,
        "train_minutes": 10.0,
    })
    _write(out_dir / "good", {
        "name": "good", "kind": "train",
        "domain": {"accuracy": 0.72, "ci95": [0.67, 0.77]},
        "general": _general(0.62, 0.42), "general_mean": 0.52,
        "train_minutes": 12.5,
        "perplexity": {"domain": {"nll": 0.8}, "general": {"nll": 2.1}},
    })
    _write(out_dir / "lost_the_domain", {
        "name": "lost_the_domain", "kind": "scale",
        "domain": {"accuracy": 0.40, "ci95": [0.35, 0.45]},
        "general": _general(0.70, 0.50), "general_mean": 0.60,
    })
    config = tmp_path / "forget_variants.yaml"
    config.write_text(
        "out_dir: runs/forget\n"
        "base_model: Qwen/Qwen3.5-4B\n"
        "baseline: {name: base, from_metrics: unused.json}\n"
        "per_task_plot: {naive: naive}\n"
        "variants:\n"
        "  - {name: naive, kind: reuse}\n"
        "  - {name: good, kind: train}\n"
        "  - {name: lost_the_domain, kind: scale}\n"
    )
    return config, out_dir


def test_report_builds_rows_with_the_right_deltas(forget_runs):
    config, out_dir = forget_runs

    summary = report(str(config))

    assert (out_dir / "summary.json").exists()
    rows = {r["name"]: r for r in summary["rows"]}
    assert len(rows) == 3

    naive = rows["naive"]
    assert naive["domain_delta_pts"] == pytest.approx(20.0)   # 0.70 - 0.50
    assert naive["general_delta_pts"] == pytest.approx(-10.0)  # 0.40 - 0.50
    assert naive["per_task_delta_pts"] == {"mmlu": pytest.approx(-10.0), "gsm8k": pytest.approx(-10.0)}
    assert naive["train_minutes"] == 10.0

    good = rows["good"]
    assert good["domain_delta_pts"] == pytest.approx(22.0)
    assert good["general_delta_pts"] == pytest.approx(2.0)
    assert good["domain_nll"] == 0.8 and good["general_nll"] == 2.1


def test_report_picks_the_best_variant_that_kept_the_domain(forget_runs):
    config, _ = forget_runs

    summary = report(str(config))

    # `lost_the_domain` has the highest general_mean (0.60) but is *below* the base model on the
    # domain, so it is not eligible — a model that forgot nothing because it learned nothing.
    assert summary["best"]["name"] == "good"
    assert summary["best"]["general_delta_pts"] == pytest.approx(2.0)


def test_report_writes_both_plots(forget_runs):
    config, out_dir = forget_runs

    report(str(config))

    assert (out_dir / "tradeoff.png").exists()
    assert (out_dir / "per_task.png").exists()


def test_summarise_rows_tolerates_a_variant_without_a_general_suite():
    baseline = {"domain": {"accuracy": 0.5}, "general": _general(0.6, 0.4), "general_mean": 0.5}
    (row,) = summarise_rows(baseline, [{"name": "domain_only", "domain": {"accuracy": 0.7}}])
    assert row["domain_delta_pts"] == pytest.approx(20.0)
    assert row["general_mean"] is None
    assert row["general_delta_pts"] is None
    assert row["per_task_delta_pts"] == {}


def test_report_needs_a_baseline(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    config = tmp_path / "c.yaml"
    config.write_text("out_dir: runs/forget\nbase_model: x\nbaseline: {name: base}\nvariants: []\n")
    with pytest.raises(FileNotFoundError):
        report(str(config))
