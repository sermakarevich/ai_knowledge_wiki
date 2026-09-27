"""Chapter 03 — sanity checks every training run needs before you trust it.

    init-loss config tokenizer_dir   - one forward pass on real tokens, loss vs ln(vocab_size)
    overfit config tokenizer_dir     - can the model learn at all? memorise one fixed batch
    bench config                     - bf16 training speed, memory, and fla kernel usage
    decide                           - compare bench variants and pick hybrid vs dense

Every command writes its numbers to `runs/<run_name>/metrics.json` so the chapter never quotes
an invented number.
"""

import json
import time
from pathlib import Path

import torch
import torch.nn.functional as F
import typer
from rich.console import Console

from .config import load_yaml, write_metrics
from .data import PackedDataset
from .model import build_model, expected_init_loss, generate_samples

app = typer.Typer(add_completion=False, help=__doc__)
console = Console()


def _fixed_batch(data_dir: str, split: str, block: int, batch: int, seed: int = 0):
    """`batch` random `block`-token windows from a prepared shard directory (chapter 02)."""
    ds = PackedDataset(data_dir, split=split, block_size=block)
    generator = torch.Generator().manual_seed(seed)
    idxs = torch.randint(0, len(ds), (batch,), generator=generator)
    xs, ys = zip(*(ds[int(i)] for i in idxs))
    return torch.stack(xs), torch.stack(ys)


def compute_loss(model, x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
    """`x`/`y` are already shifted by one token (see `PackedDataset`), so the loss is a plain
    cross-entropy between every predicted position and its real next token — no extra shift."""
    logits = model(input_ids=x).logits
    return F.cross_entropy(logits.reshape(-1, logits.size(-1)), y.reshape(-1))


# --------------------------------------------------------------------------- init-loss


@app.command("init-loss")
def init_loss(
    config: str = typer.Argument(..., help="YAML config with a `model:` section"),
    tokenizer_dir: str = typer.Argument(..., help="tokenizer dir the model's vocab must match"),
    data_dir: str = typer.Option("runs/data/tinystories", help="dir with a val.bin shard"),
    batch: int = typer.Option(8),
    block: int = typer.Option(256),
    run_name: str = typer.Option("sanity_init_loss"),
) -> None:
    """A randomly-initialised model should output roughly a uniform distribution over the
    vocabulary, so its loss on real text should sit close to ln(vocab_size)."""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    section = load_yaml(config)["model"]
    model, cfg = build_model(section, device=device, tokenizer_dir=tokenizer_dir)
    model.eval()
    x, y = _fixed_batch(data_dir, "val", block, batch)
    x, y = x.to(device), y.to(device)
    with torch.no_grad():
        loss = compute_loss(model, x, y)

    expected = expected_init_loss(cfg.vocab_size)
    console.print(f"measured init loss : {loss.item():.4f}")
    console.print(f"ln(vocab_size={cfg.vocab_size}) : {expected:.4f}")
    console.print(f"delta              : {loss.item() - expected:+.4f}")

    path = write_metrics(
        f"runs/{run_name}",
        {
            "config": str(config),
            "vocab_size": cfg.vocab_size,
            "measured_loss": loss.item(),
            "expected_loss_ln_vocab": expected,
            "batch": batch,
            "block": block,
        },
    )
    console.print(f"wrote {path}")


# ----------------------------------------------------------------------------- overfit


@app.command()
def overfit(
    config: str = typer.Argument(..., help="YAML config with a `model:` section"),
    tokenizer_dir: str = typer.Argument(..., help="tokenizer dir the model's vocab must match"),
    data_dir: str = typer.Option("runs/data/tinystories", help="dir with train_*.bin shards"),
    steps: int = typer.Option(200),
    batch: int = typer.Option(4),
    block: int = typer.Option(256),
    lr: float = typer.Option(1e-3),
    loss_threshold: float = typer.Option(0.1),
    run_name: str = typer.Option("sanity_overfit"),
) -> None:
    """Train on ONE fixed batch with AdamW until the loss collapses near zero.

    This is the classic "can the model learn at all" test: with a fixed batch there is nothing
    to generalise to, so if the loss does not go near zero the bug is in the model or the
    optimiser, not in the data.
    """
    from transformers import AutoTokenizer

    device = "cuda" if torch.cuda.is_available() else "cpu"
    section = load_yaml(config)["model"]
    model, cfg = build_model(section, device=device, tokenizer_dir=tokenizer_dir)
    tok = AutoTokenizer.from_pretrained(tokenizer_dir)
    x, y = _fixed_batch(data_dir, "train", block, batch)
    x, y = x.to(device), y.to(device)

    optim = torch.optim.AdamW(model.parameters(), lr=lr)
    history = []
    model.train()
    loss_value = float("inf")
    final_step = steps
    for step in range(1, steps + 1):
        optim.zero_grad()
        loss = compute_loss(model, x, y)
        loss.backward()
        optim.step()
        loss_value = loss.item()
        if step == 1 or step % 20 == 0:
            console.print(f"step {step:4d}  loss {loss_value:.4f}")
            history.append({"step": step, "loss": loss_value})
        if loss_value < loss_threshold:
            console.print(f"reached loss < {loss_threshold} at step {step}")
            final_step = step
            break

    prompt = tok.decode(x[0, :20].tolist(), skip_special_tokens=True)
    target = tok.decode(x[0, 20:60].tolist(), skip_special_tokens=True)
    [generated] = generate_samples(model, tok, [prompt], max_new_tokens=40, temperature=0.0)

    path = write_metrics(
        f"runs/{run_name}",
        {
            "config": str(config),
            "steps_run": final_step,
            "final_loss": loss_value,
            "history": history,
            "prompt": prompt,
            "target_continuation": target,
            "generated_continuation": generated,
        },
    )
    console.print(f"prompt   : {prompt!r}")
    console.print(f"target   : {target!r}")
    console.print(f"generated: {generated!r}")
    console.print(f"wrote {path}")


# -------------------------------------------------------------------------------- bench


@app.command()
def bench(
    config: str = typer.Argument(..., help="YAML config with a `model:` section"),
    batch: int = typer.Option(16),
    block: int = typer.Option(2048),
    steps: int = typer.Option(8),
    compile: bool = typer.Option(False, "--compile", help="wrap the model in torch.compile"),
    label: str = typer.Option(None, help="variant name in metrics.json; default from arch+compile"),
    run_name: str = typer.Option("bench_110m"),
) -> None:
    """bf16 training steps on random tokens: tokens/s, peak memory, and whether `fla`
    (flash-linear-attention) kernels are importable — the hybrid architecture's Gated DeltaNet
    layers fall back to a slow pure-PyTorch path without them."""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    section = load_yaml(config)["model"]
    dtype = torch.bfloat16 if device == "cuda" else torch.float32
    model, cfg = build_model(section, device=device, dtype=dtype)
    model.train()

    try:
        import fla  # noqa: F401

        fla_available = True
    except ImportError:
        fla_available = False

    if compile:
        model = torch.compile(model)

    optim = torch.optim.AdamW(model.parameters(), lr=1e-3)
    x = torch.randint(0, cfg.vocab_size, (batch, block), device=device)
    y = torch.randint(0, cfg.vocab_size, (batch, block), device=device)

    def step_once() -> float:
        optim.zero_grad()
        with torch.autocast(device_type=device, dtype=torch.bfloat16, enabled=device == "cuda"):
            loss = compute_loss(model, x, y)
        loss.backward()
        optim.step()
        return loss.item()

    for _ in range(2):  # warmup: first CUDA kernels / torch.compile's first trace
        step_once()

    if device == "cuda":
        torch.cuda.reset_peak_memory_stats()
        torch.cuda.synchronize()
    start = time.perf_counter()
    final_loss = 0.0
    for _ in range(steps):
        final_loss = step_once()
    if device == "cuda":
        torch.cuda.synchronize()
    elapsed = time.perf_counter() - start

    tokens_per_sec = batch * block * steps / elapsed
    peak_mem_gb = torch.cuda.max_memory_allocated() / 1024**3 if device == "cuda" else None

    arch_label = "hybrid" if section.get("arch", "qwen3_5") == "qwen3_5" else "dense"
    variant = label or f"{arch_label}_{'compiled' if compile else 'eager'}"
    result = {
        "device": device,
        "arch": arch_label,
        "config": str(config),
        "compiled": compile,
        "fla_available": fla_available,
        "batch": batch,
        "block": block,
        "steps": steps,
        "elapsed_s": elapsed,
        "tokens_per_s": tokens_per_sec,
        "peak_mem_gb": peak_mem_gb,
        "final_loss": final_loss,
    }
    path = write_metrics(f"runs/{run_name}", {variant: result})
    mem_str = f"{peak_mem_gb:.2f} GB" if peak_mem_gb is not None else "n/a (cpu)"
    console.print(
        f"{variant}: {tokens_per_sec:,.0f} tok/s, peak mem {mem_str}, fla_available={fla_available}"
    )
    console.print(f"wrote {path}")


# ------------------------------------------------------------------------------- decide


@app.command()
def decide(run_name: str = typer.Option("bench_110m")) -> None:
    """Compare `hybrid_eager` vs `dense_eager` from a prior `bench` run and pick the
    architecture chapter 04 trains: dense if `fla` is unavailable or hybrid is > 3x slower."""
    path = Path("runs") / run_name / "metrics.json"
    metrics = json.loads(path.read_text())
    hybrid = metrics.get("hybrid_eager")
    dense = metrics.get("dense_eager")
    if not hybrid or not dense:
        raise typer.BadParameter(f"{path} needs both hybrid_eager and dense_eager entries")

    ratio = dense["tokens_per_s"] / hybrid["tokens_per_s"] if hybrid["tokens_per_s"] else float("inf")
    fla_available = hybrid["fla_available"]
    use_dense = (not fla_available) or ratio > 3.0
    if not fla_available:
        reason = "fla (flash-linear-attention) is not importable on this machine"
    elif use_dense:
        reason = f"hybrid eager is {ratio:.2f}x slower than dense (> 3x threshold)"
    else:
        reason = f"hybrid eager is only {ratio:.2f}x slower than dense (<= 3x threshold)"

    decision = {
        "hybrid_vs_dense_speed_ratio": ratio,
        "fla_available": fla_available,
        "chosen_arch": "dense" if use_dense else "hybrid",
        "reason": reason,
    }
    metrics["decision"] = decision
    path.write_text(json.dumps(metrics, indent=2, sort_keys=True))
    console.print(decision)


if __name__ == "__main__":
    app()
