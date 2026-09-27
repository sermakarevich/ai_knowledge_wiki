"""Loaders for the two small real models used for "real" plots and sanity checks.

Both models are downloaded from the Hugging Face Hub the first time they are used
(cached under `~/.cache/huggingface`) and loaded in fp32 on CPU, in eval mode. Both
loaders are `functools.lru_cache`d so a chapter that calls them from several plot
functions only pays the load cost once per process.
"""

from __future__ import annotations

from functools import lru_cache

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    PreTrainedModel,
    PreTrainedTokenizerBase,
)

SMOLLM_ID = "HuggingFaceTB/SmolLM2-135M"
QWEN35_ID = "Qwen/Qwen3.5-0.8B"


@lru_cache(maxsize=1)
def load_smollm() -> tuple[PreTrainedTokenizerBase, PreTrainedModel]:
    """Load SmolLM2-135M: a plain Llama-style decoder, the simplest real transformer.

    `attn_implementation="eager"` forces the attention module to compute and keep
    the attention-weight tensor (softmax(QK^T/sqrt(d))) instead of using a fused
    kernel (sdpa/flash) that never materialises it — needed for the attention
    heat-map figures in chapter 03.
    """
    tokenizer = AutoTokenizer.from_pretrained(SMOLLM_ID)
    model = AutoModelForCausalLM.from_pretrained(
        SMOLLM_ID,
        dtype=torch.float32,
        attn_implementation="eager",
    )
    model.eval()
    return tokenizer, model


@lru_cache(maxsize=1)
def load_qwen35_08b() -> tuple[PreTrainedTokenizerBase, PreTrainedModel]:
    """Load the Qwen3.5-0.8B text model: same block types (attention + Gated DeltaNet,
    SwiGLU MLP, RMSNorm, partial RoPE) as the 27B model, just fewer/smaller layers.

    The `Qwen/Qwen3.5-0.8B` checkpoint uses the `qwen3_5` model type, which
    `transformers` registers as a vision-language model (`Qwen3_5ForConditionalGeneration`)
    so the *same* config class also serves plain text checkpoints. `AutoModelForCausalLM`
    maps `qwen3_5` to `Qwen3_5ForCausalLM` (see `transformers.models.qwen3_5.modeling_qwen3_5`),
    which wraps only the text tower (`Qwen3_5TextModel` + `lm_head`) and lists
    `^model.visual.*` in `_keys_to_ignore_on_load_unexpected` — so loading a text-only
    checkpoint with `AutoModelForCausalLM.from_pretrained` just works, no vision
    weights are expected or loaded.
    """
    tokenizer = AutoTokenizer.from_pretrained(QWEN35_ID)
    model = AutoModelForCausalLM.from_pretrained(QWEN35_ID, dtype=torch.float32)
    model.eval()
    return tokenizer, model
