"""Build a Hugging Face model from the `model:` section of one of our YAML configs.

Two architectures are supported:

* `arch: qwen3_5` — the hybrid Qwen3.5/Qwen3.8 text architecture (`Qwen3_5TextConfig`):
  three Gated DeltaNet linear-attention layers for every one Gated full-attention layer.
* `arch: qwen3`   — the plain dense-attention Qwen3 architecture (`Qwen3Config`), used as a
  fallback when the hybrid linear-attention kernels are not available on a machine.

Chapter 01 used `build_model` on the `meta` device just to count parameters. Chapter 03 adds
everything needed to actually train the model: real (non-meta) initialisation tied to a real
tokenizer, a report of what that initialisation looks like, sample generation, and checkpointing.
"""

import json
import math
from pathlib import Path
from typing import Any

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    PreTrainedModel,
    PreTrainedTokenizerBase,
    Qwen3_5TextConfig,
    Qwen3Config,
)
from transformers.configuration_utils import PreTrainedConfig

ARCHITECTURES: dict[str, type[PreTrainedConfig]] = {
    "qwen3_5": Qwen3_5TextConfig,
    "qwen3": Qwen3Config,
}


def build_config(model_section: dict[str, Any]) -> PreTrainedConfig:
    """`{"arch": "qwen3_5", "hidden_size": 768, ...}` -> a `PreTrainedConfig`.

    Every key except `arch` is passed straight to the config class, so the YAML file uses
    exactly the names Hugging Face uses and there is nothing to translate in your head.
    """
    section = dict(model_section)
    arch = section.pop("arch", "qwen3_5")
    if arch not in ARCHITECTURES:
        raise ValueError(f"unknown arch {arch!r}; known: {sorted(ARCHITECTURES)}")
    return ARCHITECTURES[arch](**section)


def round_up_to_multiple(n: int, multiple: int) -> int:
    """32000 tokens is already a multiple of 64; a hand-picked vocab_size might not be.

    GPU matmuls (and the embedding/LM-head weight tensors) are fastest when their last
    dimension is a multiple of 64 (tensor-core tile size), so we pad the *unused* tail of the
    vocabulary rather than train with an odd-sized embedding table.
    """
    return ((n + multiple - 1) // multiple) * multiple


def build_model(
    model_section: dict[str, Any],
    device: str = "cpu",
    dtype: torch.dtype = torch.float32,
    tokenizer_dir: str | Path | None = None,
) -> tuple[PreTrainedModel, PreTrainedConfig]:
    """Instantiate a causal-LM from the `model:` section.

    `device="meta"` builds the module tree *without allocating any memory* (chapter 01's use).
    `device="cpu"`/`"cuda"` allocates real, randomly-initialised weights (`initializer_range`,
    0.02 by default) — that is what every chapter from 03 onward needs.

    If `tokenizer_dir` is given, the config's `vocab_size` must already equal the tokenizer's
    size rounded up to a multiple of 64 (see `round_up_to_multiple`); this catches a stale
    vocab_size in a YAML config before you waste a training run on it. `pad_token_id`,
    `eos_token_id` and `bos_token_id` are copied from the tokenizer onto the config and the
    model's `generation_config` so `generate_samples` and later training code never has to look
    the tokenizer up again.
    """
    section = dict(model_section)
    tokenizer: PreTrainedTokenizerBase | None = None
    if tokenizer_dir is not None:
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_dir)
        expected_vocab = round_up_to_multiple(len(tokenizer), 64)
        config_vocab = section.get("vocab_size")
        if config_vocab != expected_vocab:
            raise ValueError(
                f"model vocab_size={config_vocab} does not match tokenizer {tokenizer_dir!r} "
                f"({len(tokenizer)} tokens, padded to {expected_vocab}); fix the YAML config"
            )

    config = build_config(section)
    with torch.device(device):
        model = AutoModelForCausalLM.from_config(config, dtype=dtype)

    if tokenizer is not None:
        config.pad_token_id = tokenizer.pad_token_id
        config.eos_token_id = tokenizer.eos_token_id
        config.bos_token_id = tokenizer.bos_token_id
        model.generation_config.pad_token_id = tokenizer.pad_token_id
        model.generation_config.eos_token_id = tokenizer.eos_token_id
        model.generation_config.bos_token_id = tokenizer.bos_token_id

    return model, config


# ------------------------------------------------------------------------ init inspection


def init_weights_report(model: PreTrainedModel) -> dict[str, dict[str, float]]:
    """Mean/std of the embedding table and a few linear layers, at random initialisation.

    Qwen3(.5) initialises every weight from `N(0, initializer_range^2)` with
    `initializer_range = 0.02`, so every row of this table should show a mean near 0 and a
    std near 0.02 — this is the concrete evidence for what "random initialisation" means.
    """
    report: dict[str, dict[str, float]] = {}
    for name, param in model.named_parameters():
        if param.dim() < 2:
            continue
        is_embedding = "embed_tokens" in name
        is_sample_linear = any(key in name for key in ("q_proj", "gate_proj", "lm_head")) and (
            ".0." in name or ".layers.0" in name or "lm_head" in name
        )
        if is_embedding or is_sample_linear:
            data = param.detach().float()
            report[name] = {
                "mean": data.mean().item(),
                "std": data.std().item(),
                "shape": list(param.shape),
            }
    return report


def count_params(model: PreTrainedModel, config: PreTrainedConfig | None = None) -> dict[str, int]:
    """Total / embedding / non-embedding parameter counts (see chapter 01 for why the split
    matters: the embedding table grows with the vocabulary, not with depth or width)."""
    total = sum(p.numel() for p in model.parameters())
    if config is None:
        config = model.config
    embed = config.vocab_size * config.hidden_size
    untied_head = 0 if getattr(config, "tie_word_embeddings", False) else embed
    return {
        "total": total,
        "embedding": embed + untied_head,
        "non_embedding": total - embed - untied_head,
    }


def expected_init_loss(vocab_size: int) -> float:
    """ln(vocab_size): the cross-entropy loss of a model that outputs a uniform distribution
    over the vocabulary — what an untrained model's loss should be close to."""
    return math.log(vocab_size)


# ------------------------------------------------------------------------------ generation


@torch.no_grad()
def generate_samples(
    model: PreTrainedModel,
    tokenizer: PreTrainedTokenizerBase,
    prompts: list[str],
    max_new_tokens: int = 40,
    temperature: float = 0.8,
    top_p: float = 0.95,
) -> list[str]:
    """Generate a continuation for each prompt with `model.generate`.

    This works unchanged for both architectures: the hybrid model's Gated DeltaNet layers keep
    a fixed-size recurrent state (updated one token at a time) instead of a growing key/value
    cache, but `generate` hides that difference behind the same `past_key_values`-style API.
    """
    model.eval()
    device = next(model.parameters()).device
    outputs = []
    for prompt in prompts:
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        generated = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=temperature > 0,
            temperature=temperature if temperature > 0 else None,
            top_p=top_p if temperature > 0 else None,
            pad_token_id=tokenizer.pad_token_id,
        )
        outputs.append(tokenizer.decode(generated[0], skip_special_tokens=True))
    return outputs


# ------------------------------------------------------------------------------ checkpoints


def save_checkpoint(
    model: PreTrainedModel,
    tokenizer: PreTrainedTokenizerBase,
    run_dir: str | Path,
    step: int,
) -> Path:
    """Save weights (safetensors) + config + tokenizer to `<run_dir>/checkpoints/step_<n>/`."""
    ckpt_dir = Path(run_dir) / "checkpoints" / f"step_{step}"
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(ckpt_dir, safe_serialization=True)
    tokenizer.save_pretrained(ckpt_dir)
    (ckpt_dir / "step.json").write_text(json.dumps({"step": step}))
    return ckpt_dir


def load_checkpoint(
    path: str | Path, device: str = "cpu", dtype: torch.dtype = torch.float32
) -> tuple[PreTrainedModel, PreTrainedTokenizerBase]:
    """Load a model + tokenizer previously written by `save_checkpoint`."""
    path = Path(path)
    with torch.device(device):
        model = AutoModelForCausalLM.from_pretrained(path, dtype=dtype)
    tokenizer = AutoTokenizer.from_pretrained(path)
    return model, tokenizer
