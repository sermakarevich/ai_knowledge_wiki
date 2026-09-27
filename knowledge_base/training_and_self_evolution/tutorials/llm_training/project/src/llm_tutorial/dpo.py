"""Chapter 06 (part 1) — DPO (Direct Preference Optimization) with TRL's `DPOTrainer`.

    train config.yaml   - DPO-tune the chapter-05 SFT model on UltraFeedback preference pairs
    plot run_name       - rewards/margins/accuracy vs step from a run's metrics.json

SFT teaches the model to imitate one "correct" answer per prompt. DPO instead shows it a
*pair* of answers for the same prompt — one preferred ("chosen"), one not ("rejected") — and
nudges the model's probabilities so it prefers the chosen one, without ever needing a separate
reward model: the "reward" is implicit in how much more likely the policy makes the chosen
answer relative to a frozen copy of itself (the reference model), scaled by `beta`.
"""

import json
from dataclasses import dataclass, fields
from pathlib import Path

import torch
import typer
from rich.console import Console

from .chat import attach_chat_template
from .config import load_yaml

app = typer.Typer(add_completion=False, help=__doc__)
console = Console()


# ------------------------------------------------------------------------------- config


@dataclass
class DPORunConfig:
    run_name: str
    base: str
    dataset: str
    train_split: str = "train_prefs"
    eval_split: str = "test_prefs"
    n_train: int = 10_000
    n_eval: int = 500
    max_len: int = 1024
    max_prompt_len: int = 512
    beta: float = 0.1
    loss_type: str = "sigmoid"
    lr: float = 5e-6
    epochs: float = 1.0
    per_device_batch: int = 8
    grad_accum: int = 4
    bf16: bool = True
    eval_steps: int = 100
    logging_steps: int = 10
    seed: int = 1337
    num_proc: int | None = None

    @classmethod
    def from_yaml(cls, path: str | Path) -> "DPORunConfig":
        raw = load_yaml(path)
        known = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in raw.items() if k in known})


def _device_and_dtype(bf16: bool) -> tuple[str, torch.dtype]:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.bfloat16 if (bf16 and device == "cuda") else torch.float32
    return device, dtype


# --------------------------------------------------------------------------- dataset


def to_pairs(row: dict) -> dict:
    """UltraFeedback's `chosen`/`rejected` columns each already contain the full conversation
    (user turn + assistant turn), duplicated in both. TRL's `DPOTrainer` wants the shared prefix
    split out once as `prompt`, leaving only the differing assistant turn in `chosen`/`rejected`.

    Both `row["chosen"]` and `row["rejected"]` start with the same user message here (single-turn
    UltraFeedback), so the prompt is just that first message.
    """
    return {
        "prompt": row["chosen"][:-1],
        "chosen": row["chosen"][-1:],
        "rejected": row["rejected"][-1:],
    }


def _fits(row: dict, tokenizer, max_prompt_len: int, max_len: int) -> bool:
    prompt_text = tokenizer.apply_chat_template(row["prompt"], tokenize=False, add_generation_prompt=True)
    prompt_len = len(tokenizer(prompt_text, add_special_tokens=False)["input_ids"])
    if prompt_len > max_prompt_len:
        return False
    chosen_text = tokenizer.apply_chat_template(row["prompt"] + row["chosen"], tokenize=False)
    rejected_text = tokenizer.apply_chat_template(row["prompt"] + row["rejected"], tokenize=False)
    full_len = max(
        len(tokenizer(chosen_text, add_special_tokens=False)["input_ids"]),
        len(tokenizer(rejected_text, add_special_tokens=False)["input_ids"]),
    )
    return full_len <= max_len


def prepare_pairs(config: DPORunConfig, tokenizer=None, num_proc: int | None = None):
    """Load `config.train_split`/`config.eval_split` of `config.dataset`, convert every row with
    `to_pairs`, drop pairs whose prompt or full sequence overflows `max_prompt_len`/`max_len`,
    and cap each split at `config.n_train`/`config.n_eval` rows."""
    from datasets import DatasetDict, load_dataset

    if tokenizer is None:
        from transformers import AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained(config.base)
        attach_chat_template(tokenizer)

    def _prepare_split(split: str, n: int):
        ds = load_dataset(config.dataset, split=split)
        ds = ds.map(to_pairs, remove_columns=ds.column_names, num_proc=num_proc or config.num_proc)
        ds = ds.filter(
            lambda row: _fits(row, tokenizer, config.max_prompt_len, config.max_len),
            num_proc=num_proc or config.num_proc,
        )
        n = min(n, len(ds))
        return ds.shuffle(seed=config.seed).select(range(n))

    return DatasetDict(
        {
            "train": _prepare_split(config.train_split, config.n_train),
            "eval": _prepare_split(config.eval_split, config.n_eval),
        }
    )


# ------------------------------------------------------------------------------------ train


def train(config: DPORunConfig) -> dict:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from trl import DPOConfig, DPOTrainer

    torch.manual_seed(config.seed)
    device, dtype = _device_and_dtype(config.bf16)

    tokenizer = AutoTokenizer.from_pretrained(config.base)
    attach_chat_template(tokenizer)
    model = AutoModelForCausalLM.from_pretrained(config.base, dtype=dtype).to(device)

    dataset = prepare_pairs(config, tokenizer=tokenizer)

    run_dir = Path("runs") / config.run_name
    run_dir.mkdir(parents=True, exist_ok=True)

    args = DPOConfig(
        output_dir=str(run_dir / "checkpoints"),
        num_train_epochs=config.epochs,
        learning_rate=config.lr,
        beta=config.beta,
        loss_type=config.loss_type,
        max_length=config.max_len,
        per_device_train_batch_size=config.per_device_batch,
        per_device_eval_batch_size=config.per_device_batch,
        gradient_accumulation_steps=config.grad_accum,
        bf16=(device == "cuda" and config.bf16),
        eval_strategy="steps",
        eval_steps=config.eval_steps,
        logging_steps=config.logging_steps,
        save_strategy="no",
        seed=config.seed,
        report_to="none",
    )

    trainer = DPOTrainer(
        model=model,
        ref_model=None,  # TRL makes a frozen copy of `model` for us
        args=args,
        train_dataset=dataset["train"],
        eval_dataset=dataset["eval"],
        processing_class=tokenizer,
    )

    if device == "cuda":
        torch.cuda.reset_peak_memory_stats()
    import time

    train_start = time.perf_counter()
    trainer.train()
    wall_time_s = time.perf_counter() - train_start
    peak_mem_gb = torch.cuda.max_memory_allocated() / 1024**3 if device == "cuda" else 0.0

    final_dir = run_dir / "final"
    trainer.save_model(str(final_dir))
    tokenizer.save_pretrained(final_dir)
    models_dir = Path("runs/models/tiny-qwen35-110m-dpo")
    trainer.save_model(str(models_dir))
    tokenizer.save_pretrained(models_dir)

    log_history = trainer.state.log_history
    metrics = _metrics_from_log_history(log_history)
    metrics.update(
        {
            "run_name": config.run_name,
            "config": config.__dict__,
            "n_train": len(dataset["train"]),
            "n_eval": len(dataset["eval"]),
            "wall_time_s": wall_time_s,
            "peak_mem_gb": peak_mem_gb,
            "log_history": log_history,
        }
    )
    (run_dir / "metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True, default=str))
    console.print(f"wrote {run_dir / 'metrics.json'}")
    _plot_from_log_history(log_history, run_dir)
    return metrics


def _metrics_from_log_history(log_history: list[dict]) -> dict:
    def _last(key: str):
        for row in reversed(log_history):
            if key in row:
                return row[key]
        return float("nan")

    return {
        "final_rewards_chosen": _last("rewards/chosen"),
        "final_rewards_rejected": _last("rewards/rejected"),
        "final_rewards_margins": _last("rewards/margins"),
        "final_rewards_accuracies": _last("rewards/accuracies"),
        "final_eval_loss": _last("eval_loss"),
    }


def _plot_from_log_history(log_history: list[dict], run_dir: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    def _series(key: str):
        pts = [(r["step"], r[key]) for r in log_history if key in r and "step" in r]
        return zip(*pts) if pts else ((), ())

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

    xs, ys = _series("rewards/margins")
    ax1.plot(xs, ys, label="rewards/margins", color="tab:blue")
    xs, ys = _series("rewards/chosen")
    ax1.plot(xs, ys, label="rewards/chosen", alpha=0.6)
    xs, ys = _series("rewards/rejected")
    ax1.plot(xs, ys, label="rewards/rejected", alpha=0.6)
    ax1.axhline(0.0, color="grey", lw=0.5)
    ax1.set_xlabel("step")
    ax1.set_ylabel("implicit reward")
    ax1.set_title("DPO rewards")
    ax1.legend()

    xs, ys = _series("rewards/accuracies")
    ax2.plot(xs, ys, color="tab:green")
    ax2.axhline(0.5, color="grey", lw=0.5, ls="--")
    ax2.set_xlabel("step")
    ax2.set_ylabel("accuracy")
    ax2.set_title("rewards/accuracies (chosen > rejected)")
    ax2.set_ylim(0, 1)

    fig.suptitle(f"DPO: {run_dir.name}")
    fig.tight_layout()
    out_path = run_dir / "dpo.png"
    fig.savefig(out_path, dpi=120)
    console.print(f"wrote {out_path}")


def _generate(model, tokenizer, prompt_messages: list[dict], device, max_new_tokens: int = 200) -> str:
    prompt = tokenizer.apply_chat_template(prompt_messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=False).to(device)
    with torch.no_grad():
        generated = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=tokenizer.pad_token_id or tokenizer.eos_token_id,
        )
    new_tokens = generated[0, inputs["input_ids"].shape[1] :]
    return tokenizer.decode(new_tokens, skip_special_tokens=True)


def write_samples(config: DPORunConfig, n: int = 3) -> Path:
    """Generate `n` prompts from the eval split with the pre-DPO base model and the trained
    model side by side, so the chapter can show a concrete before/after difference."""
    from transformers import AutoModelForCausalLM, AutoTokenizer

    run_dir = Path("runs") / config.run_name
    device, dtype = _device_and_dtype(config.bf16)

    tokenizer = AutoTokenizer.from_pretrained(config.base)
    attach_chat_template(tokenizer)
    dataset = prepare_pairs(config, tokenizer=tokenizer)
    prompts = [dataset["eval"][i]["prompt"] for i in range(min(n, len(dataset["eval"])))]

    base_model = AutoModelForCausalLM.from_pretrained(config.base, dtype=dtype).to(device)
    dpo_model = AutoModelForCausalLM.from_pretrained(run_dir / "final", dtype=dtype).to(device)

    lines = [f"# DPO samples: {config.run_name}", ""]
    for i, prompt_messages in enumerate(prompts):
        user_text = prompt_messages[-1]["content"]
        before = _generate(base_model, tokenizer, prompt_messages, device)
        after = _generate(dpo_model, tokenizer, prompt_messages, device)
        lines += [
            f"## Prompt {i + 1}",
            "",
            f"> {user_text}",
            "",
            "**Before (SFT base):**", "", before, "",
            "**After (DPO):**", "", after, "",
        ]
    out_path = run_dir / "samples.md"
    out_path.write_text("\n".join(lines))
    console.print(f"wrote {out_path}")
    return out_path


@app.command("train")
def train_cmd(config: str = typer.Argument(..., help="YAML config, e.g. configs/dpo_ultrafeedback.yaml")) -> None:
    cfg = DPORunConfig.from_yaml(config)
    train(cfg)
    write_samples(cfg)


@app.command("samples")
def samples_cmd(config: str = typer.Argument(..., help="YAML config used for the run")) -> None:
    cfg = DPORunConfig.from_yaml(config)
    write_samples(cfg)


@app.command()
def plot(run_name: str = typer.Argument(..., help="e.g. dpo_110m_uf or runs/dpo_110m_uf")) -> None:
    run_dir = Path(run_name) if "/" in run_name else Path("runs") / run_name
    metrics = json.loads((run_dir / "metrics.json").read_text())
    _plot_from_log_history(metrics["log_history"], run_dir)


if __name__ == "__main__":
    app()
