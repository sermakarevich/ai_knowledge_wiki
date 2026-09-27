"""Chapter 04 — the pre-training loop: real code, no Trainer abstraction.

    train config.yaml [--resume]   - run (or continue) a pre-training job
    plot run_name                  - loss.png from a run's log.jsonl + metrics.json

Everything chapters 02 (`PackedDataset`) and 03 (`build_model`, `generate_samples`,
`save_checkpoint`) built is reused unchanged; this module only adds the optimizer, the
learning-rate schedule, the accumulation/clipping/logging loop, and checkpoint/resume.
"""

import json
import math
import signal
import time
from dataclasses import dataclass, field, fields
from pathlib import Path

import torch
import typer
from rich.console import Console
from transformers import AutoTokenizer

from .config import load_yaml
from .data import PackedDataset
from .model import build_model, count_params, generate_samples, load_checkpoint, save_checkpoint
from .sanity import compute_loss

app = typer.Typer(add_completion=False, help=__doc__)
console = Console()

GPU_PEAK_FLOPS = 165e12  # measured bf16 sustained throughput on the 4090 (chapter 03 bench)

_STOP = False


def _request_stop(signum, frame) -> None:
    global _STOP
    _STOP = True


signal.signal(signal.SIGTERM, _request_stop)


# ------------------------------------------------------------------------------- config


@dataclass
class TrainConfig:
    run_name: str
    model_config: str
    tokenizer_dir: str
    data_dir: str
    block_size: int = 2048
    micro_batch: int = 16
    grad_accum: int = 4
    train_tokens: float = 1.5e9
    lr: float = 6e-4
    min_lr_ratio: float = 0.1
    warmup_steps: int = 300
    schedule: str = "cosine"
    decay_fraction: float = 0.2
    weight_decay: float = 0.1
    betas: tuple[float, float] = (0.9, 0.95)
    grad_clip: float = 1.0
    dtype: str = "bf16"
    compile: bool = True
    eval_every: int = 500
    eval_tokens: float = 2e6
    sample_every: int = 2000
    ckpt_every: int = 2000
    keep_last: int = 2
    seed: int = 1337
    prompts: list[str] = field(default_factory=lambda: ["Once upon a time"])
    log_every: int = 10

    @property
    def tokens_per_step(self) -> int:
        return self.micro_batch * self.grad_accum * self.block_size

    @property
    def total_steps(self) -> int:
        return max(int(self.train_tokens) // self.tokens_per_step, 1)

    @classmethod
    def from_yaml(cls, path: str | Path) -> "TrainConfig":
        raw = load_yaml(path)
        known = {f.name for f in fields(cls)}
        kwargs = {k: v for k, v in raw.items() if k in known}
        if "betas" in kwargs:
            kwargs["betas"] = tuple(kwargs["betas"])
        for numeric_key in ("train_tokens", "eval_tokens"):
            if numeric_key in kwargs:
                kwargs[numeric_key] = float(kwargs[numeric_key])  # YAML may misparse "5e7" as a string
        return cls(**kwargs)


# --------------------------------------------------------------------------- LR schedule


def lr_at(
    step: int,
    lr: float,
    warmup_steps: int,
    total_steps: int,
    min_lr_ratio: float = 0.1,
    schedule: str = "cosine",
    decay_fraction: float = 0.2,
) -> float:
    """The learning rate for one step: linear warmup, then `cosine` decay to `min_lr` over
    the rest of training, or `wsd` (warmup-stable-decay: hold at `lr`, then linearly decay
    to `min_lr` over the last `decay_fraction` of `total_steps`)."""
    min_lr = lr * min_lr_ratio
    if warmup_steps > 0 and step < warmup_steps:
        return lr * (step + 1) / warmup_steps

    if schedule == "cosine":
        span = max(total_steps - warmup_steps, 1)
        progress = min((step - warmup_steps) / span, 1.0)
        return min_lr + 0.5 * (lr - min_lr) * (1 + math.cos(math.pi * progress))

    if schedule == "wsd":
        decay_steps = max(int(total_steps * decay_fraction), 1)
        decay_start = max(total_steps - decay_steps, warmup_steps)
        if step < decay_start:
            return lr
        progress = min((step - decay_start) / decay_steps, 1.0)
        return lr - (lr - min_lr) * progress

    raise ValueError(f"unknown schedule {schedule!r}; use 'cosine' or 'wsd'")


# ------------------------------------------------------------------------- optimizer setup


def build_param_groups(model: torch.nn.Module, weight_decay: float) -> list[dict]:
    """Two AdamW param groups: matrices get `weight_decay`, everything 1-D (norms, biases)
    plus the (tied) embedding table get none — decaying an embedding row or a norm's gain
    toward zero has no regularising benefit and just fights the optimizer."""
    decay, no_decay = [], []
    for name, param in model.named_parameters():
        if not param.requires_grad:
            continue
        if param.dim() < 2 or "norm" in name.lower() or "embed_tokens" in name:
            no_decay.append(param)
        else:
            decay.append(param)
    return [
        {"params": decay, "weight_decay": weight_decay},
        {"params": no_decay, "weight_decay": 0.0},
    ]


def _device_and_dtype(dtype_str: str) -> tuple[str, torch.dtype]:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if dtype_str == "bf16":
        return device, torch.bfloat16
    return device, torch.float32


# ------------------------------------------------------------------------------- checkpoints


def _latest_checkpoint(checkpoints_dir: Path) -> Path | None:
    candidates = [p for p in checkpoints_dir.glob("step_*") if p.is_dir()]
    if not candidates:
        return None
    return max(candidates, key=lambda p: int(p.name.removeprefix("step_")))


def _prune_checkpoints(checkpoints_dir: Path, keep_last: int) -> None:
    candidates = sorted(
        (p for p in checkpoints_dir.glob("step_*") if p.is_dir()),
        key=lambda p: int(p.name.removeprefix("step_")),
    )
    for stale in candidates[:-keep_last] if keep_last > 0 else candidates:
        for f in stale.rglob("*"):
            if f.is_file():
                f.unlink()
        for d in sorted(stale.rglob("*"), reverse=True):
            if d.is_dir():
                d.rmdir()
        stale.rmdir()


def _save_final(model: torch.nn.Module, tokenizer, run_dir: Path, step: int) -> Path:
    final_dir = run_dir / "checkpoints" / "final"
    final_dir.mkdir(parents=True, exist_ok=True)
    unwrapped = getattr(model, "_orig_mod", model)
    unwrapped.save_pretrained(final_dir, safe_serialization=True)
    tokenizer.save_pretrained(final_dir)
    (final_dir / "step.json").write_text(json.dumps({"step": step}))
    return final_dir


# ------------------------------------------------------------------------------------ train


def train(config: TrainConfig, resume: bool = False) -> dict:
    torch.manual_seed(config.seed)
    device, dtype = _device_and_dtype(config.dtype)
    device_type = "cuda" if device == "cuda" else "cpu"

    run_dir = Path("runs") / config.run_name
    checkpoints_dir = run_dir / "checkpoints"
    checkpoints_dir.mkdir(parents=True, exist_ok=True)
    log_path = run_dir / "log.jsonl"

    model_section = load_yaml(config.model_config)["model"]
    tokenizer = AutoTokenizer.from_pretrained(config.tokenizer_dir)

    start_step = 0
    latest = _latest_checkpoint(checkpoints_dir) if resume else None
    if latest is not None:
        model, _ = load_checkpoint(latest, device=device, dtype=dtype)
        model_cfg = model.config
        start_step = json.loads((latest / "step.json").read_text())["step"] + 1
        console.print(f"resuming from {latest} at step {start_step}")
    else:
        model, model_cfg = build_model(
            model_section, device=device, dtype=dtype, tokenizer_dir=config.tokenizer_dir
        )

    optimizer = torch.optim.AdamW(
        build_param_groups(model, config.weight_decay),
        lr=config.lr,
        betas=tuple(config.betas),
        fused=(device == "cuda"),
    )
    if latest is not None and (latest / "optim.pt").exists():
        optimizer.load_state_dict(torch.load(latest / "optim.pt", map_location=device)["optimizer"])

    if config.compile:
        model = torch.compile(model)

    train_ds = PackedDataset(config.data_dir, split="train", block_size=config.block_size)
    val_ds = PackedDataset(config.data_dir, split="val", block_size=config.block_size)
    train_iter = train_ds.iter_batches(config.micro_batch, device=device)
    val_iter = val_ds.iter_batches(config.micro_batch, device=device)

    total_steps = config.total_steps
    tokens_per_step = config.tokens_per_step
    autocast_enabled = device == "cuda"

    def run_forward_backward(x: torch.Tensor, y: torch.Tensor) -> float:
        with torch.autocast(device_type=device_type, dtype=torch.bfloat16, enabled=autocast_enabled):
            loss = compute_loss(model, x, y) / config.grad_accum
        loss.backward()
        return loss.item() * config.grad_accum

    @torch.no_grad()
    def evaluate() -> tuple[float, float]:
        model.eval()
        n_batches = max(int(config.eval_tokens) // (config.micro_batch * config.block_size), 1)
        total = 0.0
        for _ in range(n_batches):
            x, y = next(val_iter)
            with torch.autocast(device_type=device_type, dtype=torch.bfloat16, enabled=autocast_enabled):
                total += compute_loss(model, x, y).item()
        model.train()
        mean_loss = total / n_batches
        return mean_loss, math.exp(min(mean_loss, 20.0))

    model.train()
    log_file = open(log_path, "a")
    tokens_seen = start_step * tokens_per_step
    tokens_per_s_history: list[float] = []
    peak_mem_gb = 0.0
    final_train_loss = float("nan")
    final_val_loss = float("nan")
    final_val_ppl = float("nan")
    train_start = time.perf_counter()

    def checkpoint_now(step: int) -> None:
        unwrapped = getattr(model, "_orig_mod", model)
        ckpt_dir = save_checkpoint(unwrapped, tokenizer, run_dir, step)
        torch.save({"optimizer": optimizer.state_dict()}, ckpt_dir / "optim.pt")
        _prune_checkpoints(checkpoints_dir, config.keep_last)

    interrupted = False
    try:
        for step in range(start_step, total_steps):
            if _STOP:
                console.print("SIGTERM received, saving checkpoint and stopping")
                interrupted = True
                break
            step_start = time.perf_counter()
            lr = lr_at(
                step, config.lr, config.warmup_steps, total_steps, config.min_lr_ratio,
                config.schedule, config.decay_fraction,
            )
            for group in optimizer.param_groups:
                group["lr"] = lr

            optimizer.zero_grad(set_to_none=True)
            step_loss = 0.0
            for _ in range(config.grad_accum):
                x, y = next(train_iter)
                step_loss += run_forward_backward(x, y) / config.grad_accum
            grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), config.grad_clip)
            optimizer.step()

            if device == "cuda":
                torch.cuda.synchronize()
            tokens_seen += tokens_per_step
            step_elapsed = time.perf_counter() - step_start
            tokens_per_s = tokens_per_step / step_elapsed
            tokens_per_s_history.append(tokens_per_s)
            if device == "cuda":
                peak_mem_gb = max(peak_mem_gb, torch.cuda.max_memory_allocated() / 1024**3)
            final_train_loss = step_loss

            if step % config.log_every == 0 or step == total_steps - 1:
                remaining_steps = total_steps - step - 1
                eta_s = remaining_steps * step_elapsed
                record = {
                    "step": step,
                    "tokens": tokens_seen,
                    "loss": step_loss,
                    "lr": lr,
                    "grad_norm": float(grad_norm),
                    "tokens_per_s": tokens_per_s,
                    "peak_mem_gb": peak_mem_gb,
                    "eta_s": eta_s,
                }
                log_file.write(json.dumps(record) + "\n")
                log_file.flush()
                console.print(
                    f"step {step:6d}/{total_steps}  loss {step_loss:.4f}  lr {lr:.2e}  "
                    f"grad_norm {float(grad_norm):.2f}  {tokens_per_s:,.0f} tok/s  "
                    f"peak {peak_mem_gb:.2f} GB  eta {eta_s / 60:.1f} min"
                )

            if config.eval_every and step % config.eval_every == 0:
                final_val_loss, final_val_ppl = evaluate()
                log_file.write(json.dumps({
                    "step": step, "tokens": tokens_seen, "val_loss": final_val_loss, "val_ppl": final_val_ppl,
                }) + "\n")
                log_file.flush()
                console.print(f"  eval step {step}: val_loss {final_val_loss:.4f}  ppl {final_val_ppl:.2f}")

            if config.sample_every and step % config.sample_every == 0:
                samples = generate_samples(model, tokenizer, config.prompts)
                with open(run_dir / "samples.md", "a") as f:
                    f.write(f"\n## step {step}\n\n")
                    for prompt, sample in zip(config.prompts, samples):
                        f.write(f"- prompt: `{prompt!r}`\n  output: `{sample!r}`\n")

            if config.ckpt_every and step % config.ckpt_every == 0 and step > start_step:
                checkpoint_now(step)
        else:
            step = total_steps - 1
    except KeyboardInterrupt:
        console.print("KeyboardInterrupt, saving checkpoint before exit")
        checkpoint_now(step)
        log_file.close()
        raise

    if interrupted:
        checkpoint_now(step)
        log_file.close()
        console.print(f"stopped at step {step}; checkpoint saved, run again with --resume")
        return {"interrupted_at_step": step}

    final_val_loss, final_val_ppl = evaluate()
    checkpoint_now(step)
    _save_final(model, tokenizer, run_dir, step)
    log_file.close()

    wall_time_s = time.perf_counter() - train_start
    n_params = count_params(getattr(model, "_orig_mod", model), model_cfg)["total"]
    mfu = (
        6 * n_params * (tokens_seen - start_step * tokens_per_step) / (wall_time_s * GPU_PEAK_FLOPS)
        if wall_time_s > 0
        else 0.0
    )
    metrics = {
        "run_name": config.run_name,
        "config": config.__dict__,
        "total_steps": step + 1,
        "tokens_seen": tokens_seen,
        "wall_time_s": wall_time_s,
        "tokens_per_s_mean": sum(tokens_per_s_history) / len(tokens_per_s_history) if tokens_per_s_history else 0.0,
        "peak_mem_gb": peak_mem_gb,
        "final_train_loss": final_train_loss,
        "final_val_loss": final_val_loss,
        "final_val_perplexity": final_val_ppl,
        "mfu": mfu,
    }
    (run_dir / "metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True, default=str))
    console.print(f"wrote {run_dir / 'metrics.json'}")
    return metrics


@app.command("train")
def train_cmd(
    config: str = typer.Argument(..., help="YAML config, e.g. configs/pretrain_fineweb.yaml"),
    resume: bool = typer.Option(False, "--resume", help="continue from the latest checkpoint"),
) -> None:
    cfg = TrainConfig.from_yaml(config)
    train(cfg, resume=resume)


# -------------------------------------------------------------------------------------- plot


@app.command()
def plot(run_name: str = typer.Argument(..., help="e.g. runs/pretrain_110m_fineweb or just the name")) -> None:
    """Read `log.jsonl` and write `loss.png`: train + val loss vs tokens seen."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    run_dir = Path(run_name) if "/" in run_name else Path("runs") / run_name
    lines = [json.loads(line) for line in (run_dir / "log.jsonl").read_text().splitlines() if line.strip()]

    train_points = [(r["tokens"], r["loss"]) for r in lines if "loss" in r]
    val_points = [(r["tokens"], r["val_loss"]) for r in lines if "val_loss" in r]

    fig, ax = plt.subplots(figsize=(8, 5))
    if train_points:
        xs, ys = zip(*train_points)
        ax.plot(xs, ys, label="train loss", alpha=0.7)
    if val_points:
        xs, ys = zip(*val_points)
        ax.plot(xs, ys, label="val loss", marker="o")
    ax.set_xlabel("tokens seen")
    ax.set_ylabel("cross-entropy loss")
    ax.set_title(f"pre-training loss: {run_dir.name}")
    ax.legend()
    fig.tight_layout()
    out_path = run_dir / "loss.png"
    fig.savefig(out_path, dpi=120)
    console.print(f"wrote {out_path}")


if __name__ == "__main__":
    app()
