"""Chapter 06 — DPO (`DPOTrainer`) preference pairs and GRPO (`GRPOTrainer`) verifiable reward.

CPU only, no network, no downloads: a tiny 2-layer test model (the chapter 03/04/05 pattern)
stands in for the real one, and a handful of synthetic rows stand in for UltraFeedback/GSM8K.
"""

import pytest
from datasets import Dataset
from tokenizers import Tokenizer, models, pre_tokenizers
from transformers import PreTrainedTokenizerFast

from llm_tutorial.chat import attach_chat_template
from llm_tutorial.dpo import DPORunConfig, to_pairs
from llm_tutorial.grpo import GRPORunConfig, correctness_reward, extract_answer, format_reward
from llm_tutorial.model import build_model

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
    specials = ["<|endoftext|>", "<|pad|>", "<|im_start|>", "<|im_end|>"]
    words = [
        "hello", "world", "how", "are", "you", "fine", "thanks", "what", "is",
        "the", "capital", "of", "france", "paris", "2", "plus", "4", "sky",
        "color", "blue", "green", "answer", "natalia", "sold", "clips",
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
    out = tmp_path_factory.mktemp("chat_tokenizer_06")
    fast.save_pretrained(out)
    attach_chat_template(fast)
    return fast


@pytest.fixture()
def tiny_model_dir(chat_tokenizer, tmp_path):
    tok_dir = tmp_path / "tok"
    chat_tokenizer.save_pretrained(tok_dir)
    model, _ = build_model(HYBRID_SECTION, device="cpu", tokenizer_dir=tok_dir)
    out = tmp_path / "tiny_model"
    model.save_pretrained(out)
    chat_tokenizer.save_pretrained(out)
    return out


# ------------------------------------------------------------------------------- to_pairs


def test_to_pairs_splits_shared_prompt_from_completions():
    row = {
        "chosen": [
            {"role": "user", "content": "what color is the sky"},
            {"role": "assistant", "content": "blue"},
        ],
        "rejected": [
            {"role": "user", "content": "what color is the sky"},
            {"role": "assistant", "content": "green"},
        ],
    }
    pairs = to_pairs(row)
    assert pairs["prompt"] == [{"role": "user", "content": "what color is the sky"}]
    assert pairs["chosen"] == [{"role": "assistant", "content": "blue"}]
    assert pairs["rejected"] == [{"role": "assistant", "content": "green"}]


def test_to_pairs_is_pure():
    row = {
        "chosen": [{"role": "user", "content": "hi"}, {"role": "assistant", "content": "a"}],
        "rejected": [{"role": "user", "content": "hi"}, {"role": "assistant", "content": "b"}],
    }
    before = {k: list(v) for k, v in row.items()}
    to_pairs(row)
    assert row == before


# --------------------------------------------------------------------------- extract_answer


@pytest.mark.parametrize(
    "text,expected",
    [
        ("Reasoning...\nAnswer: 42", "42"),
        ("Natalia sold 48/2=24 clips.\n#### 24", "24"),
        ("The total cost is $1,234 today.\nAnswer: $1,234", "1234"),
        ("Some rambling text with the number 7 in the middle, then more text.", "7"),
        ("I have no idea what to say here.", None),
        ("Step 1...\nStep 2...\nAnswer: 100\nP.S. thanks!", "100"),
    ],
)
def test_extract_answer_formats(text, expected):
    assert extract_answer(text) == expected


# ------------------------------------------------------------------------------ reward funcs


def test_correctness_reward_exact_match():
    completions = [
        [{"role": "assistant", "content": "Answer: 42"}],
        [{"role": "assistant", "content": "Answer: 41"}],
        [{"role": "assistant", "content": "#### 7"}],
    ]
    answers = ["42", "42", "7"]
    rewards = correctness_reward(completions, answers)
    assert rewards == [1.0, 0.0, 1.0]


def test_correctness_reward_strips_commas_and_dollar():
    completions = [[{"role": "assistant", "content": "Answer: $1,234"}]]
    rewards = correctness_reward(completions, ["1234"])
    assert rewards == [1.0]


def test_format_reward_checks_answer_line_presence():
    completions = [
        [{"role": "assistant", "content": "Some reasoning.\nAnswer: 5"}],
        [{"role": "assistant", "content": "No answer line here."}],
    ]
    rewards = format_reward(completions)
    assert rewards == [0.2, 0.0]


# ------------------------------------------------------------------------------------- DPO


def test_dpo_trainer_runs_three_steps(tiny_model_dir, chat_tokenizer):
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from trl import DPOConfig, DPOTrainer

    tokenizer = AutoTokenizer.from_pretrained(tiny_model_dir)
    attach_chat_template(tokenizer)
    model = AutoModelForCausalLM.from_pretrained(tiny_model_dir)

    rows = [
        {
            "prompt": [{"role": "user", "content": "hello world"}],
            "chosen": [{"role": "assistant", "content": "fine thanks"}],
            "rejected": [{"role": "assistant", "content": "world hello"}],
        }
        for _ in range(4)
    ]
    dataset = Dataset.from_list(rows)

    args = DPOConfig(
        output_dir="/tmp/dpo_test_out",
        max_steps=3,
        per_device_train_batch_size=2,
        max_length=64,
        beta=0.1,
        loss_type="sigmoid",
        logging_steps=1,
        save_strategy="no",
        report_to="none",
    )
    trainer = DPOTrainer(
        model=model,
        ref_model=None,
        args=args,
        train_dataset=dataset,
        processing_class=tokenizer,
    )
    trainer.train()
    assert len(trainer.state.log_history) > 0
    assert any("loss" in r for r in trainer.state.log_history)


# ------------------------------------------------------------------------------------ GRPO


def test_grpo_trainer_runs_two_steps(tiny_model_dir, chat_tokenizer):
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from trl import GRPOConfig, GRPOTrainer

    tokenizer = AutoTokenizer.from_pretrained(tiny_model_dir)
    attach_chat_template(tokenizer)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(tiny_model_dir)

    rows = [
        {
            "prompt": [
                {"role": "system", "content": "Answer with a number."},
                {"role": "user", "content": "what is 2 plus 4"},
            ],
            "answer": "6",
        }
        for _ in range(4)
    ]
    dataset = Dataset.from_list(rows)

    args = GRPOConfig(
        output_dir="/tmp/grpo_test_out",
        max_steps=2,
        per_device_train_batch_size=4,
        num_generations=2,
        max_completion_length=8,
        beta=0.0,
        logging_steps=1,
        save_strategy="no",
        report_to="none",
    )
    trainer = GRPOTrainer(
        model=model,
        reward_funcs=[correctness_reward, format_reward],
        args=args,
        train_dataset=dataset,
        processing_class=tokenizer,
    )
    trainer.train()
    assert len(trainer.state.log_history) > 0


def test_run_configs_load_from_yaml(tmp_path):
    dpo_yaml = tmp_path / "dpo.yaml"
    dpo_yaml.write_text(
        "run_name: t\nbase: b\ndataset: d\nn_train: 10\nn_eval: 2\n"
    )
    cfg = DPORunConfig.from_yaml(dpo_yaml)
    assert cfg.run_name == "t"
    assert cfg.n_train == 10

    grpo_yaml = tmp_path / "grpo.yaml"
    grpo_yaml.write_text("run_name: g\nbase: b\nsteps: 5\n")
    gcfg = GRPORunConfig.from_yaml(grpo_yaml)
    assert gcfg.run_name == "g"
    assert gcfg.steps == 5
