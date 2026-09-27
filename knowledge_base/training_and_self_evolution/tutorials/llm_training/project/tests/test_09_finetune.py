"""Chapter 09 — LoRA/QLoRA fine-tuning. CPU only, no network, no downloads.

The GPU-only parts (`load_base` against a real checkpoint, `train`, `merge` on 27B, the eval
commands) run on `rtx`. What is tested here is everything that can go wrong *without* a GPU:
the training-example construction, the config schema, the target-module resolution and regex,
and the one numerical claim LoRA makes — that merging `B·A` into `W` does not change the output.
"""

import json

import pytest
import torch
from pydantic import ValidationError

from llm_tutorial.finetune import (
    LANGUAGE_MODEL_LINEAR_RE,
    FTConfig,
    build_train_examples,
    match_module_names,
    resolve_target_modules,
    to_prompt_completion,
)
from llm_tutorial.model import build_model

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
    {
        "question": "Which hash is considered broken for collision resistance?",
        "answers": {"A": "SHA-256", "B": "SHA-3", "C": "MD5", "D": "BLAKE2"},
        "solution": "C",
    },
]

TINY_MODEL = {
    "arch": "qwen3_5",
    "vocab_size": 512,
    "hidden_size": 64,
    "intermediate_size": 128,
    "num_hidden_layers": 2,
    "num_attention_heads": 4,
    "num_key_value_heads": 2,
    "head_dim": 16,
    "linear_num_value_heads": 4,
    "linear_num_key_heads": 2,
    "linear_key_head_dim": 16,
    "linear_value_head_dim": 16,
    "full_attention_interval": 2,
    "tie_word_embeddings": True,
    "max_position_embeddings": 128,
}


@pytest.fixture(scope="module")
def chat_tokenizer(tmp_path_factory):
    """A tiny word-level tokenizer carrying chapter 05's ChatML template (no downloads)."""
    from tokenizers import Tokenizer, models, pre_tokenizers
    from transformers import PreTrainedTokenizerFast

    from llm_tutorial.chat import attach_chat_template

    specials = ["<|endoftext|>", "<|pad|>", "<|im_start|>", "<|im_end|>"]
    vocab = {tok: i for i, tok in enumerate(specials)}
    for i in range(512 - len(vocab)):
        vocab[f"tok{i}"] = len(vocab)
    tokenizer = Tokenizer(models.WordLevel(vocab=vocab, unk_token="<|endoftext|>"))
    tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()
    fast = PreTrainedTokenizerFast(
        tokenizer_object=tokenizer,
        eos_token="<|endoftext|>",
        pad_token="<|pad|>",
        additional_special_tokens=["<|im_start|>", "<|im_end|>"],
    )
    fast.save_pretrained(tmp_path_factory.mktemp("chat_tokenizer"))
    return attach_chat_template(fast)

# ----------------------------------------------------------------------- build_train_examples


def test_build_train_examples_letter_first():
    examples = build_train_examples(ITEMS)
    assert len(examples) == 3
    for example, item in zip(examples, ITEMS):
        user, assistant = example["messages"]
        assert user["role"] == "user"
        assert assistant["role"] == "assistant"
        # the user turn is exactly what the chapter-08 evaluator sends
        assert item["question"] in user["content"]
        assert "Answer with the letter only." in user["content"]
        # the assistant turn starts with the letter, then the option text
        letter = item["solution"]
        assert assistant["content"].startswith(f"{letter}) ")
        assert assistant["content"] == f"{letter}) {item['answers'][letter]}"


def test_build_train_examples_answer_parses_back_to_the_solution():
    """The whole point of the letter-first format: chapter 08's parser must recover the label."""
    from llm_tutorial.eval_domain import parse_letter

    for example, item in zip(build_train_examples(ITEMS), ITEMS):
        assert parse_letter(example["messages"][-1]["content"]) == item["solution"]


def test_build_train_examples_rejects_unknown_style():
    with pytest.raises(ValueError, match="unknown train example style"):
        build_train_examples(ITEMS, style="plain_text")


def test_to_prompt_completion_splits_prompt_and_answer(chat_tokenizer):
    rows = to_prompt_completion(build_train_examples(ITEMS), chat_tokenizer)
    assert len(rows) == 3
    for row, item in zip(rows, ITEMS):
        # the prompt ends at the generation prompt; the answer is not in it
        assert row["prompt"].endswith("<|im_start|>assistant\n")
        assert row["completion"].startswith(f"{item['solution']}) ")
        # exactly one assistant header, opened by the generation prompt and never closed:
        # everything after it is what the model must learn to produce
        assert row["prompt"].count("<|im_start|>assistant") == 1
        assert "<|im_end|>" not in row["prompt"].split("<|im_start|>assistant")[1]


# ----------------------------------------------------------------------- config validation


def _minimal_config(**overrides) -> dict:
    return {"run_name": "t", "base": "tiny", **overrides}


def test_config_defaults():
    cfg = FTConfig.model_validate(_minimal_config())
    assert cfg.quant == "none"
    assert cfg.lora.r == 16 and cfg.lora.alpha == 32
    assert cfg.lora.target_modules == "all-linear"
    assert cfg.data.replay.n == 0
    assert cfg.max_len == 1024


def test_config_rejects_unknown_quant():
    with pytest.raises(ValidationError, match="quant"):
        FTConfig.model_validate(_minimal_config(quant="int8"))


def test_config_rejects_unknown_key():
    """`extra="forbid"`: a typo in the YAML must fail loudly, not be silently dropped."""
    with pytest.raises(ValidationError):
        FTConfig.model_validate(_minimal_config(lr_rate=1e-4))


def test_config_roundtrips_through_json():
    cfg = FTConfig.model_validate(_minimal_config(quant="nf4", lora={"r": 8, "alpha": 16}))
    assert FTConfig.model_validate(json.loads(cfg.model_dump_json())) == cfg


# ----------------------------------------------------------------------- target modules


def test_resolve_target_module_presets():
    assert resolve_target_modules("all-linear") == "all-linear"
    assert resolve_target_modules("attention") == ["q_proj", "k_proj", "v_proj", "o_proj"]
    assert resolve_target_modules("mlp") == ["gate_proj", "up_proj", "down_proj"]
    # an explicit list passes straight through, and so does an unknown string (peft reads it
    # as a regex)
    assert resolve_target_modules(["q_proj"]) == ["q_proj"]
    assert resolve_target_modules(r".*\.q_proj") == r".*\.q_proj"


def test_language_model_regex_skips_the_vision_tower():
    """The real module names of a multimodal Qwen3.5 checkpoint: the regex must adapt the text
    model's attention/MLP projections and nothing in `visual.`"""
    names = [
        "model.language_model.layers.0.self_attn.q_proj",
        "model.language_model.layers.0.self_attn.k_proj",
        "model.language_model.layers.0.self_attn.v_proj",
        "model.language_model.layers.0.self_attn.o_proj",
        "model.language_model.layers.0.mlp.gate_proj",
        "model.language_model.layers.0.mlp.up_proj",
        "model.language_model.layers.0.mlp.down_proj",
        "model.language_model.layers.1.linear_attn.in_proj_qkv",
        "model.language_model.layers.1.linear_attn.out_proj",
        "model.visual.blocks.0.attn.q_proj",
        "model.visual.blocks.0.mlp.down_proj",
        "model.visual.merger.mlp.0",
        "lm_head",
    ]
    matched = match_module_names(LANGUAGE_MODEL_LINEAR_RE, names)
    assert matched == [
        "model.language_model.layers.0.self_attn.q_proj",
        "model.language_model.layers.0.self_attn.k_proj",
        "model.language_model.layers.0.self_attn.v_proj",
        "model.language_model.layers.0.self_attn.o_proj",
        "model.language_model.layers.0.mlp.gate_proj",
        "model.language_model.layers.0.mlp.up_proj",
        "model.language_model.layers.0.mlp.down_proj",
    ]
    assert not [n for n in matched if "visual" in n]
    # the Gated DeltaNet projections are deliberately NOT in this list
    assert not [n for n in matched if "in_proj" in n or "out_proj" in n]


# ----------------------------------------------------------------------- LoRA train + merge


@pytest.fixture(scope="module")
def tiny_lora_model():
    """A 2-layer hybrid test model wrapped in LoRA on `q_proj`/`v_proj`, trained 3 steps on CPU."""
    from peft import LoraConfig, get_peft_model

    torch.manual_seed(0)
    model, _ = build_model(TINY_MODEL, device="cpu", dtype=torch.float32)
    peft_model = get_peft_model(
        model,
        LoraConfig(r=4, lora_alpha=8, lora_dropout=0.0, target_modules=["q_proj", "v_proj"],
                   bias="none", task_type="CAUSAL_LM"),
    )
    return peft_model


def test_lora_trainable_fraction_is_tiny(tiny_lora_model):
    trainable = sum(p.numel() for p in tiny_lora_model.parameters() if p.requires_grad)
    total = sum(p.numel() for p in tiny_lora_model.parameters())
    assert trainable > 0
    assert trainable / total < 0.05, "LoRA should train well under 5% of the parameters"
    # only the lora_A/lora_B matrices carry gradients
    assert all("lora_" in name for name, p in tiny_lora_model.named_parameters() if p.requires_grad)


def test_lora_merge_and_unload_preserves_logits(tiny_lora_model):
    """The LoRA identity: `y = W·x + (alpha/r)·B·A·x` is exactly `y = (W + (alpha/r)·B·A)·x`.

    `merge_and_unload()` folds the adapter into the base weights, so a merged checkpoint must
    produce the same logits as the adapted model. Train 3 steps first so `B` is no longer the
    zero matrix LoRA initialises it to — otherwise the test would pass trivially.
    """
    torch.manual_seed(0)
    input_ids = torch.randint(0, TINY_MODEL["vocab_size"], (2, 16))
    optimizer = torch.optim.AdamW([p for p in tiny_lora_model.parameters() if p.requires_grad], lr=1e-2)
    tiny_lora_model.train()
    for _ in range(3):
        loss = tiny_lora_model(input_ids=input_ids, labels=input_ids).loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

    lora_b = [p for name, p in tiny_lora_model.named_parameters() if "lora_B" in name]
    assert any(p.abs().sum().item() > 0 for p in lora_b), "3 steps should move lora_B off zero"

    tiny_lora_model.eval()
    with torch.no_grad():
        adapted = tiny_lora_model(input_ids=input_ids).logits.clone()
        merged_model = tiny_lora_model.merge_and_unload()
        merged = merged_model(input_ids=input_ids).logits

    assert torch.allclose(adapted, merged, atol=1e-4), \
        f"max abs diff {(adapted - merged).abs().max().item()}"
