"""Chapter 05 — chat template, assistant-only loss masking, dataset length filtering.

CPU only, no network, no downloads: a tiny in-memory tokenizer (the chapter 03/04 pattern, with
`<|im_start|>`/`<|im_end|>` added) and a 2-layer test model stand in for the real ones.
"""

import pytest
from datasets import Dataset
from tokenizers import Tokenizer, models, pre_tokenizers
from transformers import PreTrainedTokenizerFast

from llm_tutorial.chat import attach_chat_template, chat, render
from llm_tutorial.model import build_model
from llm_tutorial.sft import filter_by_length

VOCAB_SIZE = 512

HYBRID_SECTION = {
    "arch": "qwen3_5",
    "vocab_size": VOCAB_SIZE,
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
    """A tiny word-level tokenizer with `<|im_start|>`/`<|im_end|>` already special, then given
    the chat template — the same shape `attach_chat_template` expects from the real tokenizer
    chapter 02 trains."""
    specials = ["<|endoftext|>", "<|pad|>", "<|im_start|>", "<|im_end|>"]
    words = [
        "hello", "world", "how", "are", "you", "fine", "thanks", "what", "is",
        "the", "capital", "of", "france", "paris", "2", "plus", "4",
    ]
    vocab = {tok: i for i, tok in enumerate(specials + words)}
    for i in range(VOCAB_SIZE - len(vocab)):
        vocab[f"tok{i}"] = len(vocab)
    assert len(vocab) == VOCAB_SIZE

    tokenizer = Tokenizer(models.WordLevel(vocab=vocab, unk_token="<|endoftext|>"))
    tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()
    fast = PreTrainedTokenizerFast(
        tokenizer_object=tokenizer,
        eos_token="<|endoftext|>",
        pad_token="<|pad|>",
        additional_special_tokens=["<|im_start|>", "<|im_end|>"],
    )
    out = tmp_path_factory.mktemp("chat_tokenizer")
    fast.save_pretrained(out)
    attach_chat_template(fast)
    return fast


# ------------------------------------------------------------------------ chat template


def test_attach_chat_template_sets_eos_to_im_end(chat_tokenizer):
    assert chat_tokenizer.eos_token == "<|im_end|>"
    assert chat_tokenizer.chat_template is not None


def test_render_produces_expected_chatml_string(chat_tokenizer):
    messages = [
        {"role": "user", "content": "hello world"},
        {"role": "assistant", "content": "how are you"},
    ]
    rendered = render(messages, chat_tokenizer, add_generation_prompt=False)
    assert rendered == (
        "<|im_start|>system\nYou are a helpful assistant.<|im_end|>\n"
        "<|im_start|>user\nhello world<|im_end|>\n"
        "<|im_start|>assistant\nhow are you<|im_end|>\n"
    )


def test_render_add_generation_prompt_appends_assistant_header(chat_tokenizer):
    messages = [{"role": "user", "content": "hello world"}]
    rendered = render(messages, chat_tokenizer, add_generation_prompt=True)
    assert rendered.endswith("<|im_start|>assistant\n")


def test_apply_chat_template_masks_only_assistant_tokens(chat_tokenizer):
    """TRL's `assistant_only_loss` relies on exactly this mask: everything up to and including
    the user's turn is 0 (masked out of the loss), only the assistant's turn (content + its
    closing `<|im_end|>`) is 1."""
    messages = [
        {"role": "user", "content": "hello world"},
        {"role": "assistant", "content": "how are you"},
    ]
    encoded = chat_tokenizer.apply_chat_template(
        messages, tokenize=True, return_dict=True, return_assistant_tokens_mask=True
    )
    tokens = chat_tokenizer.convert_ids_to_tokens(encoded["input_ids"])
    mask = encoded["assistant_masks"]
    assert any(mask), "at least one token must be marked as assistant"
    assistant_tokens = [t for t, m in zip(tokens, mask) if m]
    assert assistant_tokens == ["how", "are", "you", "<|im_end|>"]
    non_assistant_tokens = [t for t, m in zip(tokens, mask) if not m]
    assert "<|im_start|>" in non_assistant_tokens
    assert not any(t == "how" for t in non_assistant_tokens)


# --------------------------------------------------------------------------- filter_by_length


def test_filter_by_length_drops_the_long_conversation(chat_tokenizer):
    short_a = [{"role": "user", "content": "hello world"}, {"role": "assistant", "content": "fine thanks"}]
    short_b = [{"role": "user", "content": "what is the capital"}, {"role": "assistant", "content": "paris"}]
    long_conv = [
        {"role": "user", "content": " ".join(["hello"] * 200)},
        {"role": "assistant", "content": " ".join(["world"] * 200)},
    ]
    ds = Dataset.from_dict({"messages": [short_a, long_conv, short_b]})

    filtered = filter_by_length(ds, chat_tokenizer, max_len=64)

    assert len(filtered) == 2
    kept_first_turns = [row["messages"][0]["content"] for row in filtered]
    assert "hello world" in kept_first_turns
    assert "what is the capital" in kept_first_turns
    assert not any("hello hello" in c for c in kept_first_turns)


# ------------------------------------------------------------------------------------- chat()


def test_chat_returns_a_string_and_terminates(chat_tokenizer, tmp_path):
    from transformers import AutoTokenizer

    tok_dir = tmp_path / "tok"
    chat_tokenizer.save_pretrained(tok_dir)
    tokenizer = AutoTokenizer.from_pretrained(tok_dir)
    attach_chat_template(tokenizer)
    model, _ = build_model(HYBRID_SECTION, device="cpu", tokenizer_dir=tok_dir)

    out = chat(model, tokenizer, [{"role": "user", "content": "hello world"}], max_new_tokens=8)
    assert isinstance(out, str)
