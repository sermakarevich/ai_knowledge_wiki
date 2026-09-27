"""Chapter 01 — look inside a model without training it, and price the training run.

Two commands, both CPU-only and both fast:

    uv run python -m llm_tutorial.anatomy describe configs/tiny_qwen35_110m.yaml
    uv run python -m llm_tutorial.anatomy describe --from-hub Qwen/Qwen3.8-27B
    uv run python -m llm_tutorial.anatomy budget

`describe` builds the model on PyTorch's `meta` device — the module tree and every parameter
shape exist, but no memory is allocated and no weight is initialised — so you can inspect a 27B
model on a laptop. `--from-hub` downloads only `config.json` (a few kilobytes), never weights.

`budget` turns a parameter count and a token count into training FLOPs (6·N·D) and into hours
on one RTX 4090.
"""

import re
from dataclasses import dataclass

import typer
from rich.console import Console
from rich.table import Table

from .config import load_yaml
from .model import build_config, build_model

app = typer.Typer(add_completion=False, help=__doc__)
console = Console()

# One RTX 4090: ~165 TFLOP/s dense bf16 peak with FP32 accumulate.
RTX4090_TFLOPS = 165.0
# Model FLOPs Utilisation: the fraction of that peak a real training loop actually reaches.
DEFAULT_MFU = 0.4

# (label, parameters, training tokens) — the "why not 27B from scratch" table of chapter 01.
DEFAULT_BUDGET_ROWS: list[tuple[str, float, float]] = [
    ("Qwen3.8-27B, full pre-training", 27e9, 36e12),
    ("Qwen3.8-27B, 1T tokens", 27e9, 1e12),
    ("Qwen3.5-4B, 1T tokens", 4e9, 1e12),
    ("our tiny-qwen35-110m, 1.5B tokens", 108.6e6, 1.5e9),
]


def human(n: float) -> str:
    """3.4e9 -> '3.40B'."""
    for limit, suffix in ((1e12, "T"), (1e9, "B"), (1e6, "M"), (1e3, "K")):
        if abs(n) >= limit:
            return f"{n / limit:.2f}{suffix}"
    return f"{n:.0f}"


# --------------------------------------------------------------------------- describe


def compress_layer_types(layer_types: list[str]) -> str:
    """['linear_attention','linear_attention','linear_attention','full_attention', ...]
    -> 'LLLF LLLF ...' with a legend, so a 64-layer pattern fits on one line."""
    short = {"linear_attention": "L", "full_attention": "F", "sliding_attention": "S"}
    letters = "".join(short.get(t, "?") for t in layer_types)
    return " ".join(letters[i : i + 4] for i in range(0, len(letters), 4))


def _generalise(name: str, layer_types: list[str] | None) -> str:
    """`model.layers.3.self_attn.q_proj.weight` -> `model.layers.{full}.self_attn.q_proj.weight`
    so that all layers of the same kind collapse into one table row."""
    match = re.search(r"\.layers\.(\d+)\.", name)
    if not match:
        return name
    idx = int(match.group(1))
    kind = "all"
    if layer_types and idx < len(layer_types):
        kind = layer_types[idx].replace("_attention", "")
    return name.replace(f".layers.{idx}.", ".layers.{" + kind + "}.", 1)


@dataclass
class ParamGroup:
    name: str
    shape: tuple[int, ...]
    per_module: int
    count: int

    @property
    def total(self) -> int:
        return self.per_module * self.count


def group_parameters(model, layer_types: list[str] | None) -> list[ParamGroup]:
    """Collapse the parameter list into one row per (generalised name, shape)."""
    groups: dict[tuple[str, tuple[int, ...]], ParamGroup] = {}
    for name, param in model.named_parameters():
        key = (_generalise(name, layer_types), tuple(param.shape))
        if key in groups:
            groups[key].count += 1
        else:
            groups[key] = ParamGroup(key[0], key[1], param.numel(), 1)
    return list(groups.values())


def parameter_summary(model, config) -> dict[str, int]:
    """Total, embedding and non-embedding parameter counts.

    "Non-embedding" is the number people compare across models: the embedding table grows with
    the vocabulary, not with the depth or width that does the actual thinking.
    """
    total = sum(p.numel() for p in model.parameters())
    embed = config.vocab_size * config.hidden_size
    untied_head = 0 if getattr(config, "tie_word_embeddings", False) else embed
    return {
        "total": total,
        "embedding": embed + untied_head,
        "non_embedding": total - embed - untied_head,
    }


def text_config(config):
    """Qwen3.8 ships a multimodal wrapper (`Qwen3_5Config`); the language model is `.text_config`."""
    return getattr(config, "text_config", config)


def print_description(model, config, title: str) -> dict[str, int]:
    layer_types = getattr(config, "layer_types", None)

    table = Table(title=title, header_style="bold")
    table.add_column("module")
    table.add_column("shape", justify="right")
    table.add_column("×", justify="right")
    table.add_column("parameters", justify="right")
    for group in group_parameters(model, layer_types):
        table.add_row(
            group.name,
            "×".join(str(d) for d in group.shape),
            str(group.count),
            f"{group.total:,}",
        )
    console.print(table)

    summary = parameter_summary(model, config)
    console.print(f"total parameters      : {summary['total']:,}  ({human(summary['total'])})")
    console.print(f"embedding parameters  : {summary['embedding']:,}")
    console.print(f"non-embedding         : {summary['non_embedding']:,}")
    console.print(f"tie_word_embeddings   : {getattr(config, 'tie_word_embeddings', None)}")
    if layer_types:
        console.print(f"layer_types ({len(layer_types)}) : {compress_layer_types(layer_types)}")
        console.print("  L = linear_attention (Gated DeltaNet), F = full_attention")
    return summary


@app.command()
def describe(
    config_path: str = typer.Argument(None, help="YAML config with a `model:` section"),
    from_hub: str = typer.Option(
        None, "--from-hub", help="Hugging Face repo id; downloads config.json only, no weights"
    ),
) -> None:
    """Print every parameter tensor of a model, grouped by layer kind, plus the totals."""
    if from_hub:
        from transformers import AutoConfig

        config = text_config(AutoConfig.from_pretrained(from_hub))
        import torch
        from transformers import AutoModelForCausalLM

        with torch.device("meta"):
            model = AutoModelForCausalLM.from_config(config)
        print_description(model, config, f"{from_hub} (config only, meta device)")
        return

    if not config_path:
        raise typer.BadParameter("give a config path or --from-hub")
    section = load_yaml(config_path)["model"]
    model, config = build_model(section, device="meta")
    print_description(model, config, f"{config_path} ({config.__class__.__name__}, meta device)")


# ----------------------------------------------------------------------------- budget


def training_flops(params: float, tokens: float) -> float:
    """The standard estimate: 6 floating-point operations per parameter per token.

    Two of the six are the forward pass (a multiply and an add per weight), four are the
    backward pass (gradients with respect to the inputs and to the weights).
    """
    return 6.0 * params * tokens


def budget_row(
    label: str,
    params: float,
    tokens: float,
    tflops: float = RTX4090_TFLOPS,
    mfu: float = DEFAULT_MFU,
) -> dict[str, float | str]:
    """One row of the compute table: FLOPs, GPU-seconds, hours and years on one 4090."""
    flops = training_flops(params, tokens)
    seconds = flops / (tflops * 1e12 * mfu)
    return {
        "label": label,
        "params": params,
        "tokens": tokens,
        "flops": flops,
        "gpu_hours": seconds / 3600.0,
        "gpu_years": seconds / (3600.0 * 24 * 365.25),
    }


@app.command()
def budget(
    params: float = typer.Option(None, help="parameter count of one model, e.g. 27e9"),
    tokens: float = typer.Option(None, help="training tokens for that model, e.g. 36e12"),
    tflops: float = typer.Option(RTX4090_TFLOPS, help="peak bf16 TFLOP/s of the GPU"),
    mfu: float = typer.Option(DEFAULT_MFU, help="Model FLOPs Utilisation, 0..1"),
) -> None:
    """How long would training this cost on one RTX 4090? (6·N·D / (peak × MFU))"""
    if params and tokens:
        rows = [budget_row("custom", params, tokens, tflops, mfu)]
    else:
        rows = [budget_row(*row, tflops=tflops, mfu=mfu) for row in DEFAULT_BUDGET_ROWS]

    table = Table(
        title=f"training compute at {tflops:.0f} TFLOP/s peak × {mfu:.0%} MFU", header_style="bold"
    )
    table.add_column("model / token budget")
    table.add_column("N params", justify="right")
    table.add_column("D tokens", justify="right")
    table.add_column("6·N·D FLOPs", justify="right")
    table.add_column("4090-hours", justify="right")
    table.add_column("4090-years", justify="right")
    for r in rows:
        table.add_row(
            str(r["label"]),
            human(r["params"]),
            human(r["tokens"]),
            f"{r['flops']:.2e}",
            f"{r['gpu_hours']:,.1f}",
            f"{r['gpu_years']:,.2f}",
        )
    console.print(table)


if __name__ == "__main__":
    app()
