"""Chapter 06 (part 2) — GRPO (Group Relative Policy Optimization) with TRL's `GRPOTrainer`.

    train config.yaml        - GRPO-tune a model on GSM8K with a verifiable numeric-answer reward
    evaluate model_dir        - greedy GSM8K accuracy (used before and after training)
    plot run_name             - reward mean/std and eval accuracy vs step

DPO needs a *pair* of answers labelled by a human. GRPO needs neither a human label nor a
reward model: for each prompt it samples a *group* of `num_generations` completions from the
current policy, scores each with a programmatic reward function (here: is the final number
correct?), and pushes probability mass toward the above-group-average completions and away from
the below-average ones — "group relative" because the reward is normalised within its own group,
not against a global baseline.
"""

import json
import re
from dataclasses import dataclass, fields
from pathlib import Path

import torch
import typer
from rich.console import Console

from .config import load_yaml

app = typer.Typer(add_completion=False, help=__doc__)
console = Console()

SYSTEM_PROMPT = (
    "You are a careful math tutor. Solve the problem step by step, showing your reasoning, "
    "then finish with one line of the exact form:\nAnswer: <number>"
)


# ------------------------------------------------------------------------------- config


@dataclass
class GRPORunConfig:
    run_name: str
    base: str
    dataset: str = "openai/gsm8k"
    dataset_config: str = "main"
    n_eval: int = 300
    system_prompt: str = SYSTEM_PROMPT
    max_prompt_len: int = 512
    max_completion_len: int = 256
    num_generations: int = 8
    per_device_batch: int = 8
    grad_accum: int = 2
    lr: float = 1e-6
    beta: float = 0.0
    steps: int = 300
    temperature: float = 1.0
    bf16: bool = True
    logging_steps: int = 5
    seed: int = 1337
    use_lora: bool = False
    lora_r: int = 32
    lora_alpha: int = 64
    num_proc: int | None = None

    @classmethod
    def from_yaml(cls, path: str | Path) -> "GRPORunConfig":
        raw = load_yaml(path)
        known = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in raw.items() if k in known})


def _device_and_dtype(bf16: bool) -> tuple[str, torch.dtype]:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.bfloat16 if (bf16 and device == "cuda") else torch.float32
    return device, dtype


# ------------------------------------------------------------------------- reward functions


_ANSWER_LINE_RE = re.compile(r"answer\s*:\s*(.+)", re.IGNORECASE)
_NUMBER_RE = re.compile(r"-?\$?\d[\d,]*\.?\d*")


def _clean_number(text: str) -> str | None:
    text = text.strip().rstrip(".")
    text = text.replace(",", "").replace("$", "")
    if not text:
        return None
    try:
        value = float(text)
    except ValueError:
        return None
    return str(int(value)) if value == int(value) else str(value)


def extract_answer(text: str) -> str | None:
    """Pull the final numeric answer out of a completion.

    Tries, in order: the last `Answer: <...>` line (our prompted format), the last `#### <...>`
    line (GSM8K's own ground-truth format), then the last number anywhere in the text. Returns
    `None` if no number is found at all.
    """
    for line in reversed(text.strip().splitlines()):
        match = _ANSWER_LINE_RE.search(line)
        if match:
            numbers = _NUMBER_RE.findall(match.group(1))
            if numbers:
                return _clean_number(numbers[-1])
    for line in reversed(text.strip().splitlines()):
        if line.strip().startswith("####"):
            numbers = _NUMBER_RE.findall(line)
            if numbers:
                return _clean_number(numbers[-1])
    numbers = _NUMBER_RE.findall(text)
    if numbers:
        return _clean_number(numbers[-1])
    return None


def correctness_reward(completions: list, answer: list[str], **kwargs) -> list[float]:
    """1.0 if the completion's final numeric answer exactly matches the ground truth, else 0.0."""
    rewards = []
    for completion, gold in zip(completions, answer):
        text = completion[-1]["content"] if isinstance(completion, list) else completion
        predicted = extract_answer(text)
        gold_clean = _clean_number(str(gold))
        rewards.append(1.0 if predicted is not None and predicted == gold_clean else 0.0)
    return rewards


def format_reward(completions: list, **kwargs) -> list[float]:
    """0.2 bonus if the completion contains a well-formed `Answer: <number>` line."""
    rewards = []
    for completion in completions:
        text = completion[-1]["content"] if isinstance(completion, list) else completion
        has_line = any(_ANSWER_LINE_RE.search(line) for line in text.splitlines())
        rewards.append(0.2 if has_line else 0.0)
    return rewards


# --------------------------------------------------------------------------- dataset


def _ground_truth(answer_field: str) -> str:
    return answer_field.split("####")[-1].strip()


def prepare_dataset(config: GRPORunConfig, split: str = "train", n: int | None = None):
    """Load GSM8K, wrap each question in the system prompt as a conversation, and keep the
    ground-truth final number as the `answer` column (consumed by `correctness_reward`)."""
    from datasets import load_dataset

    ds = load_dataset(config.dataset, config.dataset_config, split=split)

    def _to_prompt(row: dict) -> dict:
        return {
            "prompt": [
                {"role": "system", "content": config.system_prompt},
                {"role": "user", "content": row["question"]},
            ],
            "answer": _ground_truth(row["answer"]),
        }

    ds = ds.map(_to_prompt, remove_columns=ds.column_names, num_proc=config.num_proc)
    if n is not None:
        ds = ds.select(range(min(n, len(ds))))
    return ds


# ------------------------------------------------------------------------------------- eval


def evaluate(model, tokenizer, n: int = 300, max_new_tokens: int = 256, system_prompt: str = SYSTEM_PROMPT) -> dict:
    """Greedy GSM8K test accuracy: exact match on `extract_answer` vs the ground-truth number.
    Used before and after GRPO training (and again in chapter 08)."""
    from datasets import load_dataset

    ds = load_dataset("openai/gsm8k", "main", split="test")
    n = min(n, len(ds))
    ds = ds.select(range(n))

    device = next(model.parameters()).device
    correct = 0
    for row in ds:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": row["question"]},
        ]
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=False).to(device)
        with torch.no_grad():
            generated = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                pad_token_id=tokenizer.pad_token_id or tokenizer.eos_token_id,
            )
        new_tokens = generated[0, inputs["input_ids"].shape[1] :]
        text = tokenizer.decode(new_tokens, skip_special_tokens=True)
        predicted = extract_answer(text)
        gold = _ground_truth(row["answer"])
        if predicted is not None and predicted == gold:
            correct += 1
    return {"n": n, "correct": correct, "accuracy": correct / n if n else 0.0}


@app.command("evaluate")
def evaluate_cmd(
    model_dir: str = typer.Argument(...),
    n: int = typer.Option(300),
) -> None:
    from transformers import AutoModelForCausalLM, AutoTokenizer

    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForCausalLM.from_pretrained(model_dir).to(device)
    result = evaluate(model, tokenizer, n=n)
    console.print(result)


# ------------------------------------------------------------------------------------ train


def _load_base_model(base: str, dtype: torch.dtype):
    """Load the policy model. `Qwen/Qwen3.5-0.8B`'s checkpoint is the multimodal
    `Qwen3_5ForConditionalGeneration` (it ships with a vision tower even for the text-only
    size); `AutoModelForCausalLM` resolves it to that class and returns the whole
    conditional-generation wrapper, not a bare text model. We keep the wrapper (TRL only calls
    `.generate()` and computes logprobs through the LM head, both of which the wrapper forwards
    to its inner language model) rather than trying to unwrap `.model.language_model`, which
    would need every generation-config/tied-embedding attribute copied over."""
    from transformers import AutoModelForCausalLM

    return AutoModelForCausalLM.from_pretrained(base, dtype=dtype)


def _peft_config(config: GRPORunConfig):
    if not config.use_lora:
        return None
    from peft import LoraConfig

    return LoraConfig(
        r=config.lora_r,
        lora_alpha=config.lora_alpha,
        target_modules="all-linear",
        task_type="CAUSAL_LM",
    )


def train(config: GRPORunConfig) -> dict:
    from transformers import AutoTokenizer
    from trl import GRPOConfig, GRPOTrainer

    torch.manual_seed(config.seed)
    device, dtype = _device_and_dtype(config.bf16)

    tokenizer = AutoTokenizer.from_pretrained(config.base)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = _load_base_model(config.base, dtype).to(device)

    run_dir = Path("runs") / config.run_name
    run_dir.mkdir(parents=True, exist_ok=True)

    console.print("evaluating base model on GSM8K before GRPO...")
    accuracy_before = evaluate(model, tokenizer, n=config.n_eval, system_prompt=config.system_prompt)
    console.print(f"before: {accuracy_before}")

    train_dataset = prepare_dataset(config, split="train")

    args = GRPOConfig(
        output_dir=str(run_dir / "checkpoints"),
        max_steps=config.steps,
        learning_rate=config.lr,
        beta=config.beta,
        num_generations=config.num_generations,
        max_completion_length=config.max_completion_len,
        per_device_train_batch_size=config.per_device_batch,
        gradient_accumulation_steps=config.grad_accum,
        temperature=config.temperature,
        bf16=(device == "cuda" and config.bf16),
        logging_steps=config.logging_steps,
        save_strategy="no",
        seed=config.seed,
        report_to="none",
    )

    trainer = GRPOTrainer(
        model=model,
        reward_funcs=[correctness_reward, format_reward],
        args=args,
        train_dataset=train_dataset,
        processing_class=tokenizer,
        peft_config=_peft_config(config),
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

    console.print("evaluating trained model on GSM8K after GRPO...")
    accuracy_after = evaluate(trainer.model, tokenizer, n=config.n_eval, system_prompt=config.system_prompt)
    console.print(f"after: {accuracy_after}")

    log_history = trainer.state.log_history
    metrics = _metrics_from_log_history(log_history)
    metrics.update(
        {
            "run_name": config.run_name,
            "config": config.__dict__,
            "n_train": len(train_dataset),
            "wall_time_s": wall_time_s,
            "peak_mem_gb": peak_mem_gb,
            "accuracy_before": accuracy_before,
            "accuracy_after": accuracy_after,
            "log_history": log_history,
        }
    )
    (run_dir / "metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True, default=str))
    console.print(f"wrote {run_dir / 'metrics.json'}")
    _plot_from_log_history(log_history, run_dir)
    return metrics


def _metrics_from_log_history(log_history: list[dict]) -> dict:
    reward_points = [r["reward"] for r in log_history if "reward" in r]
    std_points = [r.get("reward_std", float("nan")) for r in log_history if "reward" in r]
    return {
        "final_reward_mean": reward_points[-1] if reward_points else float("nan"),
        "final_reward_std": std_points[-1] if std_points else float("nan"),
        "frac_reward_zero_std": (
            sum(1 for s in std_points if s == 0) / len(std_points) if std_points else float("nan")
        ),
    }


def _plot_from_log_history(log_history: list[dict], run_dir: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    def _series(key: str):
        pts = [(r["step"], r[key]) for r in log_history if key in r and "step" in r]
        return zip(*pts) if pts else ((), ())

    fig, ax = plt.subplots(figsize=(8, 5))
    xs, ys = _series("reward")
    if xs:
        ax.plot(xs, ys, label="reward mean", color="tab:blue")
    xs, ys = _series("reward_std")
    if xs:
        ax.plot(xs, ys, label="reward std", color="tab:orange", alpha=0.7)
    ax.set_xlabel("step")
    ax.set_ylabel("reward")
    ax.set_title(f"GRPO reward: {run_dir.name}")
    ax.legend()
    fig.tight_layout()
    out_path = run_dir / "reward.png"
    fig.savefig(out_path, dpi=120)
    console.print(f"wrote {out_path}")


def write_samples(config: GRPORunConfig, n: int = 3) -> Path:
    """Generate `n` GSM8K test questions with the pre-GRPO base model and the trained model
    side by side (greedy), with the extracted answer and correctness, for the chapter."""
    from datasets import load_dataset
    from transformers import AutoTokenizer

    run_dir = Path("runs") / config.run_name
    device, dtype = _device_and_dtype(config.bf16)

    tokenizer = AutoTokenizer.from_pretrained(config.base)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    ds = load_dataset("openai/gsm8k", "main", split="test").select(range(n))

    base_model = _load_base_model(config.base, dtype).to(device)
    # `transformers` transparently detects `adapter_config.json` in the checkpoint dir and
    # returns the base model with the LoRA adapter already merged in — no separate `peft`
    # loading step needed (and doubling up here would silently re-wrap the wrong base weights).
    trained_model = _load_base_model(str(run_dir / "final"), dtype).to(device)

    lines = [f"# GRPO samples: {config.run_name}", ""]
    for i, row in enumerate(ds):
        messages = [
            {"role": "system", "content": config.system_prompt},
            {"role": "user", "content": row["question"]},
        ]
        gold = _ground_truth(row["answer"])
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=False).to(device)

        def _greedy(m):
            with torch.no_grad():
                generated = m.generate(
                    **inputs,
                    max_new_tokens=config.max_completion_len,
                    do_sample=False,
                    pad_token_id=tokenizer.pad_token_id or tokenizer.eos_token_id,
                )
            return tokenizer.decode(generated[0, inputs["input_ids"].shape[1] :], skip_special_tokens=True)

        before, after = _greedy(base_model), _greedy(trained_model)
        lines += [
            f"## Problem {i + 1} (gold answer: {gold})",
            "",
            f"> {row['question']}",
            "",
            f"**Before:** (extracted: {extract_answer(before)})", "", before, "",
            f"**After:** (extracted: {extract_answer(after)})", "", after, "",
        ]
    out_path = run_dir / "samples.md"
    out_path.write_text("\n".join(lines))
    console.print(f"wrote {out_path}")
    return out_path


@app.command("train")
def train_cmd(config: str = typer.Argument(..., help="YAML config, e.g. configs/grpo_gsm8k_110m.yaml")) -> None:
    cfg = GRPORunConfig.from_yaml(config)
    train(cfg)
    write_samples(cfg)


@app.command("samples")
def samples_cmd(config: str = typer.Argument(..., help="YAML config used for the run")) -> None:
    cfg = GRPORunConfig.from_yaml(config)
    write_samples(cfg)


@app.command()
def plot(run_name: str = typer.Argument(..., help="e.g. grpo_110m_gsm8k or runs/grpo_110m_gsm8k")) -> None:
    run_dir = Path(run_name) if "/" in run_name else Path("runs") / run_name
    metrics = json.loads((run_dir / "metrics.json").read_text())
    _plot_from_log_history(metrics["log_history"], run_dir)


if __name__ == "__main__":
    app()
