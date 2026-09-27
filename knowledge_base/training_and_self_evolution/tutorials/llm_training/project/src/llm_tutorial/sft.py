"""Chapter 05 — SFT (Supervised Fine-Tuning) with TRL's `SFTTrainer`.

    train config.yaml           - fine-tune the chapter-04 base model on SmolTalk
    compare base sft            - generate 8 fixed prompts with both models, write samples.md
    plot run_name                - loss.png from a run's metrics.json

Unlike chapter 04's pre-training loop (written out by hand), this chapter uses TRL's
`SFTTrainer`: the loop, the batching, the optimizer, and — crucially — the assistant-only loss
mask are all handled by the trainer, because the mask depends on the `{% generation %}` tags in
`chat.CHAT_TEMPLATE`, not on anything this module has to implement itself.
"""

import json
import time
from dataclasses import dataclass, fields
from pathlib import Path

import torch
import typer
from rich.console import Console

from .chat import attach_chat_template, chat
from .config import load_yaml

app = typer.Typer(add_completion=False, help=__doc__)
console = Console()


# ------------------------------------------------------------------------------- config


@dataclass
class SFTRunConfig:
    run_name: str
    base: str
    dataset: str
    subsets: list[str]
    n_train: int = 50_000
    n_eval: int = 1_000
    max_len: int = 2048
    packing: bool = False
    assistant_only_loss: bool = True
    epochs: float = 2.0
    lr: float = 1e-4
    warmup_ratio: float = 0.03
    schedule: str = "cosine"
    per_device_batch: int = 16
    grad_accum: int = 2
    bf16: bool = True
    eval_steps: int = 200
    logging_steps: int = 10
    seed: int = 1337
    num_proc: int | None = None

    @classmethod
    def from_yaml(cls, path: str | Path) -> "SFTRunConfig":
        raw = load_yaml(path)
        known = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in raw.items() if k in known})


def _device_and_dtype(bf16: bool) -> tuple[str, torch.dtype]:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.bfloat16 if (bf16 and device == "cuda") else torch.float32
    return device, dtype


# --------------------------------------------------------------------------- dataset


def filter_by_length(ds, tokenizer, max_len: int, num_proc: int | None = None):
    """Keep only conversations whose ChatML rendering tokenizes to `<= max_len` tokens.

    A conversation that gets truncated mid-turn would either cut off the assistant's answer
    (teaching the model to stop speaking mid-sentence) or, worse, cut off the loss mask's view
    of where the assistant turn started — dropping it instead of truncating it is the simplest
    thing that cannot go wrong.
    """

    def _fits(example: dict) -> bool:
        # Ask the tokenizer for the exact same assistant mask TRL's SFTTrainer will compute
        # (rather than a heuristic on the raw message text) and require at least one `1` in
        # it — `assistant_only_loss=True` raises on any example whose mask is all zero. This
        # also catches cases a text-only heuristic would miss: e.g. our chapter-02 tokenizer
        # silently drops a lone `{` immediately after a newline, which happens on some
        # SmolTalk JSON-formatted answers and otherwise zeroes out the *whole* mask (the
        # `char_to_token` lookup for the assistant span's start character fails, and
        # transformers gives up on the entire span rather than skipping just that character).
        encoded = tokenizer.apply_chat_template(
            example["messages"],
            tokenize=True,
            add_generation_prompt=False,
            return_dict=True,
            return_assistant_tokens_mask=True,
        )
        if 1 not in encoded["assistant_masks"]:
            return False
        return len(encoded["input_ids"]) <= max_len

    return ds.filter(_fits, num_proc=num_proc)


def prepare_dataset(config: SFTRunConfig, num_proc: int | None = None):
    """Load `config.subsets` of `config.dataset`, keep the `messages` column, drop
    conversations longer than `config.max_len` tokens, shuffle, and split into
    `config.n_train` / `config.n_eval` non-overlapping rows."""
    from datasets import DatasetDict, concatenate_datasets, load_dataset
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(config.base)
    attach_chat_template(tokenizer)

    parts = []
    for subset in config.subsets:
        subset_ds = load_dataset(config.dataset, subset, split="train")
        parts.append(subset_ds.select_columns(["messages"]))
    full = concatenate_datasets(parts) if len(parts) > 1 else parts[0]

    filtered = filter_by_length(full, tokenizer, config.max_len, num_proc=num_proc or config.num_proc)
    filtered = filtered.shuffle(seed=config.seed)

    n_total = min(config.n_train + config.n_eval, len(filtered))
    filtered = filtered.select(range(n_total))
    n_train = min(config.n_train, n_total)
    return DatasetDict(
        {
            "train": filtered.select(range(n_train)),
            "eval": filtered.select(range(n_train, n_total)),
        }
    )


def _count_tokens(ds, tokenizer) -> int:
    total = 0
    for row in ds:
        rendered = tokenizer.apply_chat_template(row["messages"], tokenize=False, add_generation_prompt=False)
        total += len(tokenizer(rendered, add_special_tokens=False)["input_ids"])
    return total


# ------------------------------------------------------------------------------------ train


def train(config: SFTRunConfig) -> dict:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from trl import SFTConfig, SFTTrainer

    torch.manual_seed(config.seed)
    device, dtype = _device_and_dtype(config.bf16)

    tokenizer = AutoTokenizer.from_pretrained(config.base)
    attach_chat_template(tokenizer)
    model = AutoModelForCausalLM.from_pretrained(config.base, dtype=dtype).to(device)

    dataset = prepare_dataset(config)

    run_dir = Path("runs") / config.run_name
    run_dir.mkdir(parents=True, exist_ok=True)

    # This installed transformers (5.16) only takes `warmup_steps`, not `warmup_ratio` — TRL's
    # `SFTConfig` inherits `TrainingArguments` as-is, so we convert the ratio ourselves.
    steps_per_epoch = max(len(dataset["train"]) // (config.per_device_batch * config.grad_accum), 1)
    total_steps = steps_per_epoch * config.epochs
    warmup_steps = round(config.warmup_ratio * total_steps)

    args = SFTConfig(
        output_dir=str(run_dir / "checkpoints"),
        num_train_epochs=config.epochs,
        learning_rate=config.lr,
        lr_scheduler_type=config.schedule,
        warmup_steps=warmup_steps,
        per_device_train_batch_size=config.per_device_batch,
        per_device_eval_batch_size=config.per_device_batch,
        gradient_accumulation_steps=config.grad_accum,
        bf16=(device == "cuda" and config.bf16),
        eval_strategy="steps",
        eval_steps=config.eval_steps,
        logging_steps=config.logging_steps,
        save_strategy="no",
        max_length=config.max_len,
        packing=config.packing,
        assistant_only_loss=config.assistant_only_loss,
        seed=config.seed,
        report_to="none",
    )

    trainer = SFTTrainer(
        model=model,
        args=args,
        train_dataset=dataset["train"],
        eval_dataset=dataset["eval"],
        processing_class=tokenizer,
    )

    if device == "cuda":
        torch.cuda.reset_peak_memory_stats()
    train_start = time.perf_counter()
    trainer.train()
    wall_time_s = time.perf_counter() - train_start
    peak_mem_gb = torch.cuda.max_memory_allocated() / 1024**3 if device == "cuda" else 0.0

    final_dir = run_dir / "final"
    trainer.save_model(str(final_dir))
    tokenizer.save_pretrained(final_dir)
    models_dir = Path("runs/models/tiny-qwen35-110m-sft")
    trainer.save_model(str(models_dir))
    tokenizer.save_pretrained(models_dir)

    n_tokens = _count_tokens(dataset["train"], tokenizer) * config.epochs
    log_history = trainer.state.log_history
    eval_losses = [r["eval_loss"] for r in log_history if "eval_loss" in r]

    metrics = {
        "run_name": config.run_name,
        "config": config.__dict__,
        "n_train": len(dataset["train"]),
        "n_eval": len(dataset["eval"]),
        "tokens_trained": n_tokens,
        "wall_time_s": wall_time_s,
        "peak_mem_gb": peak_mem_gb,
        "log_history": log_history,
        "final_train_loss": next(
            (r["loss"] for r in reversed(log_history) if "loss" in r), float("nan")
        ),
        "final_eval_loss": eval_losses[-1] if eval_losses else float("nan"),
    }
    (run_dir / "metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True, default=str))
    console.print(f"wrote {run_dir / 'metrics.json'}")
    _plot_from_log_history(log_history, run_dir)
    return metrics


def _plot_from_log_history(log_history: list[dict], run_dir: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    train_points = [(r["step"], r["loss"]) for r in log_history if "loss" in r and "step" in r]
    eval_points = [(r["step"], r["eval_loss"]) for r in log_history if "eval_loss" in r and "step" in r]

    fig, ax = plt.subplots(figsize=(8, 5))
    if train_points:
        xs, ys = zip(*train_points)
        ax.plot(xs, ys, label="train loss", alpha=0.7)
    if eval_points:
        xs, ys = zip(*eval_points)
        ax.plot(xs, ys, label="eval loss", marker="o")
    ax.set_xlabel("step")
    ax.set_ylabel("cross-entropy loss")
    ax.set_title(f"SFT loss: {run_dir.name}")
    ax.legend()
    fig.tight_layout()
    out_path = run_dir / "loss.png"
    fig.savefig(out_path, dpi=120)
    console.print(f"wrote {out_path}")


@app.command("train")
def train_cmd(config: str = typer.Argument(..., help="YAML config, e.g. configs/sft_smoltalk.yaml")) -> None:
    cfg = SFTRunConfig.from_yaml(config)
    train(cfg)


@app.command()
def plot(run_name: str = typer.Argument(..., help="e.g. runs/sft_110m_smoltalk or just the name")) -> None:
    run_dir = Path(run_name) if "/" in run_name else Path("runs") / run_name
    metrics = json.loads((run_dir / "metrics.json").read_text())
    _plot_from_log_history(metrics["log_history"], run_dir)


# ---------------------------------------------------------------------------------- compare


def compare(
    base: str,
    sft: str,
    prompts_file: str = "configs/eval_prompts.yaml",
    run_name: str = "sft_110m_smoltalk",
    max_new_tokens: int = 128,
) -> Path:
    """Generate all fixed prompts with both `base` and `sft` models and write a two-column
    Markdown comparison to `runs/<run_name>/samples.md`."""
    from transformers import AutoModelForCausalLM, AutoTokenizer

    prompts = load_yaml(prompts_file)["prompts"]
    device, dtype = _device_and_dtype(True)

    base_tokenizer = AutoTokenizer.from_pretrained(base)
    attach_chat_template(base_tokenizer)
    base_model = AutoModelForCausalLM.from_pretrained(base, dtype=dtype).to(device)

    sft_tokenizer = AutoTokenizer.from_pretrained(sft)
    attach_chat_template(sft_tokenizer)
    sft_model = AutoModelForCausalLM.from_pretrained(sft, dtype=dtype).to(device)

    lines = [
        f"# SFT before/after — `{base}` vs `{sft}`",
        "",
        "| prompt | base (pre-SFT) | SFT |",
        "|---|---|---|",
    ]
    for prompt in prompts:
        messages = prompt["messages"]
        user_text = " → ".join(m["content"] for m in messages if m["role"] == "user")
        base_out = chat(base_model, base_tokenizer, messages, max_new_tokens=max_new_tokens)
        sft_out = chat(sft_model, sft_tokenizer, messages, max_new_tokens=max_new_tokens)
        lines.append(
            f"| **{prompt['id']}**: {user_text} "
            f"| {base_out.replace(chr(10), ' ')} "
            f"| {sft_out.replace(chr(10), ' ')} |"
        )

    out_path = Path("runs") / run_name / "samples.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n")
    console.print(f"wrote {out_path}")
    return out_path


@app.command("compare")
def compare_cmd(
    base: str = typer.Argument(..., help="base (pre-SFT) model dir"),
    sft: str = typer.Argument(..., help="SFT model dir"),
    prompts_file: str = typer.Option("configs/eval_prompts.yaml"),
    run_name: str = typer.Option("sft_110m_smoltalk"),
) -> None:
    compare(base, sft, prompts_file, run_name)


if __name__ == "__main__":
    app()
