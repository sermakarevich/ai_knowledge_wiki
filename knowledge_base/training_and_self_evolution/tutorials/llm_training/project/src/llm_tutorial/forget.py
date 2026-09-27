"""Chapter 10 — catastrophic forgetting: measure it, then reduce it.

    run-all   configs/forget_variants.yaml  - train/merge + evaluate every mitigation variant
    report                                  - runs/forget/summary.json + tradeoff.png + per_task.png
    scale-adapter  adapter lam out          - W = W_base + lam*dW  ("adapter scaling")
    ties-merge-adapters  base a1 a2 out     - TIES-merge two LoRA deltas into a bf16 checkpoint
    perplexity-all configs/forget_variants.yaml - domain/general NLL for every variant

Catastrophic forgetting is what happens when training on a narrow task overwrites weights that
other tasks were using. Nothing in the loss says "keep being good at arithmetic"; gradient descent
just walks downhill on the cybersecurity questions in front of it, and whatever else those weights
were doing is collateral damage.

Every mitigation in this module is one of three ideas:
  * **move less** - a smaller learning rate, fewer epochs, a lower LoRA rank, or a target
    distribution the model already agrees with (self-distillation) all shrink the step size.
  * **keep practising** - replay mixes general chat data back into the training set, so "stay
    good at ordinary conversation" is literally part of the loss again.
  * **edit after the fact** - the LoRA delta is just a tensor. Scale it down, or combine two
    deltas with TIES, and you get a new model without training anything.
"""

import json
import math
import time
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from .config import load_yaml, write_metrics

app = typer.Typer(add_completion=False, help=__doc__)
console = Console()

DEFAULT_CONFIG = "configs/forget_variants.yaml"
DEFAULT_OUT_DIR = Path("runs/forget")

# The seven chapter-08 tasks, in the order the chapter's tables and plots use.
GENERAL_TASKS = ("mmlu", "arc_challenge", "hellaswag", "winogrande", "truthfulqa_mc2", "gsm8k", "ifeval")


# =============================================================================== tensor maths
#
# Everything in this section is pure tensor arithmetic on state dicts. No model is loaded, no GPU
# is needed, and the unit tests exercise all of it on 2x3 tensors made by hand.


def scale_lora_state_dict(state: dict, lam: float) -> dict:
    """Multiply a LoRA adapter's effective update by `lam`.

    A LoRA layer computes `y = W*x + (alpha/r) * B*(A*x)`, so the update it adds to the frozen
    weight is `dW = (alpha/r) * B*A`. That expression is *linear in B*: scale every `lora_B`
    tensor by `lam` and the whole update scales by `lam`, with `A` untouched. (Scaling `A`
    instead would work equally well; scaling both would give `lam**2`, which is the classic
    off-by-a-square in this trick.)

    `lam = 1.0` is the fine-tuned model, `lam = 0.0` is the base model, and values in between walk
    the straight line between them - a one-dimensional dial between "specialised" and "original"
    that costs no training at all.
    """
    out = {}
    for key, tensor in state.items():
        if ".lora_B." in key or key.endswith("lora_embedding_B"):
            out[key] = tensor * lam
        else:
            out[key] = tensor.clone() if hasattr(tensor, "clone") else tensor
    return out


def scale_adapter(adapter_dir: str | Path, lam: float, out_dir: str | Path) -> Path:
    """Write a copy of a saved LoRA adapter whose update is `lam` times as strong."""
    from safetensors.torch import load_file, save_file

    adapter_dir, out_dir = Path(adapter_dir), Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    state = load_file(adapter_dir / "adapter_model.safetensors")
    save_file(scale_lora_state_dict(state, lam), str(out_dir / "adapter_model.safetensors"))
    for name in ("adapter_config.json", "tokenizer.json", "tokenizer_config.json",
                 "special_tokens_map.json", "vocab.json", "merges.txt", "chat_template.jinja"):
        src = adapter_dir / name
        if src.exists():
            (out_dir / name).write_bytes(src.read_bytes())
    console.print(f"wrote lambda={lam} adapter to {out_dir}")
    return out_dir


def trim_to_density(tensor, density: float):
    """Keep the `density` fraction of entries with the largest magnitude, zero the rest.

    This is step 1 of TIES ("TRIM, ELECT SIGN & MERGE", Yadav et al. 2023). The observation behind
    it is that most of a fine-tuning delta is noise: a small fraction of the entries carry almost
    all of the change, and the rest only get in the way when two deltas are added together.
    """
    import torch

    if density >= 1.0:
        return tensor.clone()
    flat = tensor.flatten()
    k = max(int(round(density * flat.numel())), 1)
    threshold = flat.abs().kthvalue(flat.numel() - k + 1).values
    return torch.where(tensor.abs() >= threshold, tensor, torch.zeros_like(tensor))


def ties_merge(deltas: list, density: float = 0.2, weights: list[float] | None = None):
    """Merge several fine-tuning deltas of the same shape with TIES.

    Adding two deltas straight up is a bad idea: where one says "+0.3" and the other says "-0.28"
    the sum is a meaningless "+0.02", and both fine-tunes lose. That is *parameter interference*.
    TIES fixes it in three steps:

    1. **Trim** each delta to its largest-magnitude entries (`trim_to_density`).
    2. **Elect a sign** per entry: whichever direction carries more total magnitude wins.
    3. **Disjoint mean**: average only the deltas that agree with the elected sign; the ones
       pulling the other way are dropped rather than allowed to cancel the winner out.

    `weights` lets one delta count for more than another (e.g. `[1.0, 0.5]` to keep the domain
    adapter dominant).
    """
    import torch

    if not deltas:
        raise ValueError("ties_merge needs at least one delta")
    stacked = torch.stack([trim_to_density(d, density) for d in deltas]).float()
    w = torch.tensor(weights if weights is not None else [1.0] * len(deltas), dtype=torch.float32)
    w = w.view(-1, *([1] * (stacked.dim() - 1)))

    elected = torch.sign((stacked * w).sum(dim=0))
    elected = torch.where(elected == 0, torch.ones_like(elected), elected)

    agrees = (torch.sign(stacked) == elected) & (stacked != 0)
    numerator = (stacked * w * agrees).sum(dim=0)
    denominator = (w * agrees).sum(dim=0)
    merged = torch.where(denominator > 0, numerator / denominator, torch.zeros_like(numerator))
    return merged.to(deltas[0].dtype)


def lora_deltas(adapter_dir: str | Path) -> dict:
    """`{base weight name -> dW}` for a saved adapter, with the `alpha/r` scaling already applied.

    peft stores the pieces under keys like
    `base_model.model.model.layers.0.mlp.up_proj.lora_A.weight`; we recombine them into the one
    matrix that actually gets added to `model.layers.0.mlp.up_proj.weight`.
    """
    from safetensors.torch import load_file

    adapter_dir = Path(adapter_dir)
    cfg = json.loads((adapter_dir / "adapter_config.json").read_text())
    scaling = cfg["lora_alpha"] / cfg["r"]
    if cfg.get("use_rslora"):
        scaling = cfg["lora_alpha"] / math.sqrt(cfg["r"])
    state = load_file(adapter_dir / "adapter_model.safetensors")

    a_parts = {k.split(".lora_A.")[0]: v for k, v in state.items() if ".lora_A." in k}
    b_parts = {k.split(".lora_B.")[0]: v for k, v in state.items() if ".lora_B." in k}
    deltas = {}
    for prefix, a in a_parts.items():
        b = b_parts.get(prefix)
        if b is None:
            continue
        # "base_model.model.<real name>.weight" -> "<real name>.weight"
        name = prefix.replace("base_model.model.", "", 1) + ".weight"
        deltas[name] = (b.float() @ a.float()) * scaling
    return deltas


def ties_merge_adapters(
    base: str,
    adapter_dirs: list[str],
    out_dir: str | Path,
    density: float = 0.2,
    weights: list[float] | None = None,
) -> Path:
    """TIES-merge the *deltas* of several LoRA adapters into one plain bf16 checkpoint.

    We merge `dW` matrices rather than the `A`/`B` factors. peft's `add_weighted_adapter(
    combination_type="ties")` does the sign election on `A` and `B` separately, which is not the
    same operation - the sign of a factor is not the sign of the product, and two adapters can
    disagree on `B` while agreeing perfectly on `B*A`. Reconstructing `dW` costs one small matmul
    per layer and makes the maths exactly the TIES paper's.
    """
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    out_dir = Path(out_dir)
    all_deltas = [lora_deltas(d) for d in adapter_dirs]
    names = sorted(set().union(*[set(d) for d in all_deltas]))
    console.print(f"TIES: {len(adapter_dirs)} adapters, {len(names)} weight matrices, density {density}")

    model = AutoModelForCausalLM.from_pretrained(base, dtype=torch.bfloat16, device_map="cpu")
    params = dict(model.named_parameters())
    applied, missing = 0, []
    for name in names:
        present = [d[name] for d in all_deltas if name in d]
        param = params.get(name)
        if param is None:
            missing.append(name)
            continue
        merged = ties_merge(present, density=density,
                            weights=weights[: len(present)] if weights else None)
        with torch.no_grad():
            param.add_(merged.to(param.dtype).to(param.device))
        applied += 1
    if missing:
        console.print(f"[yellow]{len(missing)} delta names had no matching parameter, e.g. {missing[:3]}[/yellow]")

    out_dir.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(str(out_dir))
    AutoTokenizer.from_pretrained(adapter_dirs[0]).save_pretrained(str(out_dir))
    console.print(f"wrote TIES-merged checkpoint ({applied} matrices updated) to {out_dir}")
    return out_dir


# =============================================================================== evaluation


def evaluate_model(
    name: str,
    model_path: str,
    adapter: str | None = None,
    out_dir: str | Path = DEFAULT_OUT_DIR,
    domain_split: str = "500",
    general: bool = True,
    general_config: str = "configs/eval_general_4b.yaml",
    extra: dict | None = None,
) -> dict:
    """Domain accuracy + the chapter-08 general suite for any model, adapter or not.

    `finetune.evaluate()` always evaluates `base + adapter` from a run's own config; chapter 10
    also needs to score merged and rescaled checkpoints that have no config and no adapter, so it
    gets its own entry point. The measurement itself is identical - same functions, same limits,
    same seeds - which is the only reason the numbers are comparable at all.
    """
    from . import eval_domain, eval_general
    from .finetune import free_gpu

    run_dir = Path(out_dir) / name
    run_dir.mkdir(parents=True, exist_ok=True)
    start = time.perf_counter()
    write_metrics(run_dir, {"name": name, "model": model_path, "adapter": adapter, **(extra or {})})

    result = eval_domain.evaluate_hf(model_path, split=domain_split, adapter=adapter)
    console.print(f"[bold]{name}[/bold] CyberMetric-{domain_split}: {result['accuracy']:.3f} ci95 {result['ci95']}")
    out = {"domain": result}
    write_metrics(run_dir, {"domain": result})

    if general:
        free_gpu()
        summary = eval_general.run_hf(model_path, str(run_dir / "general"),
                                      config_path=general_config, adapter=adapter)
        out["general"] = summary["general"]
        out["general_mean"] = summary["general_mean"]
        write_metrics(run_dir, {"general": summary["general"], "general_mean": summary["general_mean"]})
        console.print(f"[bold]{name}[/bold] general_mean: {summary['general_mean']:.4f}")
    write_metrics(run_dir, {"eval_wall_seconds": time.perf_counter() - start})
    return out


def general_eval_texts(dataset: str, subset: str, n: int, tokenizer, seed: int = 1234) -> list[str]:
    """`n` held-out SmolTalk conversations rendered with the chat template, for perplexity."""
    from datasets import load_dataset

    from .chat import render

    try:
        data = load_dataset(dataset, subset, split="test")
    except (ValueError, KeyError):
        data = load_dataset(dataset, subset, split="train").select(range(n * 4))
    data = data.shuffle(seed=seed).select(range(min(n, len(data))))
    return [render(row["messages"], tokenizer, add_generation_prompt=False, enable_thinking=False)
            for row in data]


def perplexity_all(config_path: str = DEFAULT_CONFIG) -> dict:
    """Domain and general perplexity for every variant, merged into its `metrics.json`.

    Cheap next to the general suite (a forward pass over a few hundred short texts) and it sees
    drift that a 500-question accuracy rounds away.
    """
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    from . import eval_domain
    from .finetune import free_gpu

    raw = load_yaml(config_path)
    out_dir = Path(raw.get("out_dir", DEFAULT_OUT_DIR))
    ppl_cfg = raw.get("perplexity", {})
    domain_items = eval_domain.load_split(raw.get("domain_split", "500"))[: ppl_cfg.get("domain_n", 200)]
    domain_texts = eval_domain.domain_perplexity_texts(domain_items)

    results = {}
    for entry in [raw["baseline"]] + raw["variants"]:
        name = entry["name"]
        run_dir = out_dir / name
        if not (run_dir / "metrics.json").exists():
            console.print(f"[yellow]skip {name}: no metrics.json yet[/yellow]")
            continue
        metrics = json.loads((run_dir / "metrics.json").read_text())
        if "perplexity" in metrics:
            console.print(f"[yellow]skip {name}: perplexity already recorded[/yellow]")
            results[name] = metrics["perplexity"]
            continue
        model_path, adapter = metrics.get("model"), metrics.get("adapter")
        if not model_path:
            continue
        console.rule(f"perplexity: {name}")
        tokenizer = AutoTokenizer.from_pretrained(adapter or model_path)
        model = AutoModelForCausalLM.from_pretrained(
            model_path, dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32
        )
        if adapter:
            from peft import PeftModel

            model = PeftModel.from_pretrained(model, adapter)
        model = model.to("cuda" if torch.cuda.is_available() else "cpu").eval()
        general_texts = general_eval_texts(
            ppl_cfg.get("dataset", "HuggingFaceTB/smoltalk"),
            ppl_cfg.get("subset", "smol-magpie-ultra"), ppl_cfg.get("general_n", 200), tokenizer,
        )
        entry_result = {
            "domain": eval_domain.perplexity(model, tokenizer, domain_texts),
            "general": eval_domain.perplexity(model, tokenizer, general_texts),
        }
        console.print(f"{name}: domain nll {entry_result['domain']['nll']:.4f} "
                      f"general nll {entry_result['general']['nll']:.4f}")
        write_metrics(run_dir, {"perplexity": entry_result})
        results[name] = entry_result
        del model
        free_gpu()
    return results


# =============================================================================== the driver


def _reuse(entry: dict, run_dir: Path, domain_key: str) -> dict:
    """Copy an already-measured run (chapter 08 baseline or a chapter-09 ablation variant) into
    `runs/forget/<name>/metrics.json` so every row of the table has the same shape.

    Nothing is recomputed. Re-running the general suite on `abl_ref` would burn 80 GPU-minutes to
    reproduce a number we already paid for, and the whole point of chapter 08's fixed limits and
    seeds is that we do not have to.
    """
    source = Path(entry["from_metrics"])
    metrics = json.loads(source.read_text())
    domain = metrics.get(domain_key) or metrics.get("domain")
    out = {
        "name": entry["name"],
        "model": entry.get("model"),
        "adapter": entry.get("adapter"),
        "reused_from": str(source),
        "domain": domain,
        "note": entry.get("note"),
    }
    if metrics.get("general_mean") is not None:
        out["general"] = metrics["general"]
        out["general_mean"] = metrics["general_mean"]
    if metrics.get("train"):
        out["train_minutes"] = metrics["cost"]["wall_seconds"] / 60
        out["config"] = metrics.get("config")
    run_dir.mkdir(parents=True, exist_ok=True)
    write_metrics(run_dir, out)
    console.print(f"[green]reused {source} -> {run_dir / 'metrics.json'}[/green]")
    return out


def run_all(config_path: str = DEFAULT_CONFIG, only: str | None = None) -> dict:
    """Run every variant in `configs/forget_variants.yaml`, skipping the finished ones.

    A finished variant is one whose `runs/forget/<name>/metrics.json` already has both a `domain`
    and a `general_mean` key (or `general: false`). That is what makes this safe to re-run after
    an out-of-memory kill or a dropped SSH session: it picks up where it stopped instead of
    redoing nine hours of evaluation.
    """
    from .finetune import FTConfig, _deep_merge, free_gpu, train

    raw = load_yaml(config_path)
    out_dir = Path(raw.get("out_dir", DEFAULT_OUT_DIR))
    out_dir.mkdir(parents=True, exist_ok=True)
    base_model = raw["base_model"]
    general_config = raw.get("general_config", "configs/eval_general_4b.yaml")
    domain_split = str(raw.get("domain_split", "500"))
    base_train = raw.get("base_train_config", {})

    _reuse(raw["baseline"], out_dir / raw["baseline"]["name"], raw.get("baseline_domain_key", "domain_500"))

    for entry in raw["variants"]:
        name = entry["name"]
        if only and name != only:
            continue
        run_dir = out_dir / name
        metrics_path = run_dir / "metrics.json"
        wants_general = entry.get("general", True)
        if metrics_path.exists():
            done = json.loads(metrics_path.read_text())
            if done.get("domain") and (done.get("general_mean") is not None or not wants_general):
                console.print(f"[yellow]skip {name} (already measured)[/yellow]")
                continue
        console.rule(f"[bold]forget variant: {name} ({entry['kind']})")
        try:
            _run_variant(entry, raw, run_dir, base_model, base_train, general_config, domain_split,
                         FTConfig, _deep_merge, train, free_gpu)
        except Exception as exc:  # noqa: BLE001 — one bad variant must not lose the rest
            console.print(f"[red]variant {name} failed: {type(exc).__name__}: {exc}[/red]")
            free_gpu()
            continue

    return report(config_path)


def _run_variant(entry, raw, run_dir, base_model, base_train, general_config, domain_split,
                 FTConfig, _deep_merge, train, free_gpu) -> None:
    kind = entry["kind"]
    name = entry["name"]
    model_path, adapter, extra = base_model, None, {"kind": kind, "note": entry.get("note")}

    if kind == "reuse":
        _reuse(entry, run_dir, raw.get("baseline_domain_key", "domain_500"))
        return

    if kind == "train":
        merged = _deep_merge(json.loads(json.dumps(base_train)), entry.get("config", {}))
        merged["run_name"] = f"{run_dir.parent.name}/{name}"
        cfg = FTConfig.model_validate(merged)
        # Resume-safety: a variant whose adapter is already on disk was killed *after* training,
        # during the 80-minute general suite. Retraining it would throw away 25 GPU-minutes to
        # reproduce a file we already have.
        if (cfg.adapter_dir / "adapter_model.safetensors").exists():
            console.print(f"[yellow]{name}: adapter already trained, going straight to evaluation[/yellow]")
        else:
            train(cfg)
            free_gpu()
        adapter = str(cfg.adapter_dir)
        trained = json.loads((cfg.run_dir / "metrics.json").read_text())
        stats = trained["train"]
        extra |= {
            "config": trained["config"],
            "train_minutes": trained["cost"]["wall_seconds"] / 60,
            "train_rows": stats["n_rows"],
            "n_domain": stats.get("n_domain"),
            "n_replay": stats.get("n_replay", 0),
            "final_train_loss": stats["final_train_loss"],
            "trainable_params": stats.get("trainable_params"),
        }
    elif kind == "eval_only":
        adapter = entry["adapter"]
        if entry.get("from_metrics"):
            source = json.loads(Path(entry["from_metrics"]).read_text())
            extra |= {"config": source.get("config"),
                      "train_minutes": source["cost"]["wall_seconds"] / 60}
    elif kind == "scale":
        adapter = str(scale_adapter(entry["adapter"], entry["lam"],
                                    entry.get("out", f"runs/models/{name}-adapter")))
        extra |= {"lam": entry["lam"], "scaled_from": entry["adapter"]}
    elif kind == "ties":
        out_path = Path(entry.get("out", f"runs/models/{name}-merged"))
        if (out_path / "config.json").exists():
            console.print(f"[yellow]{name}: merged checkpoint already exists, reusing it[/yellow]")
        else:
            ties_merge_adapters(
                base_model, entry["adapters"], out_path,
                density=entry.get("density", 0.2), weights=entry.get("weights"),
            )
        model_path = str(out_path)
        free_gpu()
        extra |= {"density": entry.get("density", 0.2), "adapters": entry["adapters"],
                  "weights": entry.get("weights")}
    else:
        raise ValueError(f"unknown variant kind: {kind!r}")

    evaluate_model(name, model_path, adapter=adapter, out_dir=run_dir.parent,
                   domain_split=str(entry.get("domain_split", domain_split)),
                   general=entry.get("general", True), general_config=general_config, extra=extra)


# =============================================================================== report


def summarise_rows(baseline: dict, variants: list[dict]) -> list[dict]:
    """One row per variant with its deltas against the base model, in percentage points.

    Percentage *points*, not percent: "MMLU fell 3.7 points" means 76.1 -> 72.4, which is what
    everyone means and what nobody writes down.
    """
    base_domain = (baseline.get("domain") or {}).get("accuracy")
    base_general = baseline.get("general_mean")
    base_tasks = {t: v["value"] for t, v in (baseline.get("general") or {}).items()}

    rows = []
    for metrics in variants:
        domain = (metrics.get("domain") or {}).get("accuracy")
        general_mean = metrics.get("general_mean")
        tasks = {t: v["value"] for t, v in (metrics.get("general") or {}).items()}
        row = {
            "name": metrics.get("name"),
            "kind": metrics.get("kind", "reuse"),
            "note": metrics.get("note"),
            "domain_accuracy": domain,
            "domain_ci95": (metrics.get("domain") or {}).get("ci95"),
            "domain_delta_pts": None if domain is None or base_domain is None
            else round(100 * (domain - base_domain), 2),
            "general_mean": general_mean,
            "general_delta_pts": None if general_mean is None or base_general is None
            else round(100 * (general_mean - base_general), 2),
            "general": metrics.get("general"),
            "per_task_delta_pts": {
                task: round(100 * (value - base_tasks[task]), 2)
                for task, value in tasks.items() if task in base_tasks
            },
            "train_minutes": metrics.get("train_minutes"),
            "domain_nll": (metrics.get("perplexity") or {}).get("domain", {}).get("nll"),
            "general_nll": (metrics.get("perplexity") or {}).get("general", {}).get("nll"),
        }
        rows.append(row)
    return rows


def report(config_path: str = DEFAULT_CONFIG) -> dict:
    """Build `runs/forget/summary.json`, `tradeoff.png` and `per_task.png` from what exists."""
    raw = load_yaml(config_path)
    out_dir = Path(raw.get("out_dir", DEFAULT_OUT_DIR))
    baseline_name = raw["baseline"]["name"]

    def _load(name: str) -> dict | None:
        path = out_dir / name / "metrics.json"
        return json.loads(path.read_text()) if path.exists() else None

    baseline = _load(baseline_name)
    if baseline is None:
        raise FileNotFoundError(f"no baseline metrics at {out_dir / baseline_name / 'metrics.json'}")
    variants = [m for m in (_load(v["name"]) for v in raw["variants"]) if m]
    rows = summarise_rows(baseline, variants)

    summary = {
        "baseline": {
            "name": baseline_name,
            "domain_accuracy": (baseline.get("domain") or {}).get("accuracy"),
            "general_mean": baseline.get("general_mean"),
            "general": baseline.get("general"),
            "domain_nll": (baseline.get("perplexity") or {}).get("domain", {}).get("nll"),
            "general_nll": (baseline.get("perplexity") or {}).get("general", {}).get("nll"),
        },
        "rows": rows,
        "best": _pick_best(rows),
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    console.print(f"wrote {out_dir / 'summary.json'} ({len(rows)} rows)")

    _plot_tradeoff(summary, out_dir)
    _plot_per_task(summary, out_dir, raw.get("per_task_plot", {}))
    _print_table(summary)
    return summary


def _pick_best(rows: list[dict]) -> dict | None:
    """The variant that keeps the most general ability without giving up the domain.

    The rule, stated before looking at the numbers so it cannot be tuned to them: among variants
    whose domain accuracy is at least as good as the base model's, take the highest
    `general_mean`; break ties on domain accuracy. Recipes that lost the domain are not on the
    table - a model that forgot nothing because it learned nothing is not a result.
    """
    eligible = [r for r in rows
                if r.get("general_mean") is not None and (r.get("domain_delta_pts") or 0) >= 0]
    if not eligible:
        return None
    best = max(eligible, key=lambda r: (r["general_mean"], r["domain_accuracy"]))
    return {"name": best["name"], "general_mean": best["general_mean"],
            "domain_accuracy": best["domain_accuracy"],
            "general_delta_pts": best["general_delta_pts"],
            "domain_delta_pts": best["domain_delta_pts"]}


def _plot_tradeoff(summary: dict, out_dir: Path) -> None:
    """x = change in general_mean, y = change in domain accuracy, one labelled dot per variant.

    The origin is the base model. Up-and-to-the-right is a free lunch; down-and-to-the-right is
    the trade the chapter is about; the vertical line at x=0 separates "kept its general ability"
    from "forgot".
    """
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    points = [r for r in summary["rows"]
              if r.get("general_delta_pts") is not None and r.get("domain_delta_pts") is not None]
    if not points:
        console.print("[yellow]tradeoff.png skipped: no variant has both deltas yet[/yellow]")
        return
    fig, ax = plt.subplots(figsize=(9, 6))
    best_name = (summary.get("best") or {}).get("name")
    for row in points:
        colour = "#e45756" if (row["general_delta_pts"] < 0) else "#4c78a8"
        marker = "D" if row["name"] == best_name else "o"
        ax.scatter(row["general_delta_pts"], row["domain_delta_pts"], s=90, color=colour,
                   marker=marker, zorder=3, edgecolors="black", linewidths=0.6)
        ax.annotate(row["name"], (row["general_delta_pts"], row["domain_delta_pts"]),
                    textcoords="offset points", xytext=(7, 5), fontsize=8)
    ax.scatter(0, 0, s=160, marker="*", color="black", zorder=4, label="base model (chapter 08)")
    ax.axhline(0, color="grey", lw=0.8)
    ax.axvline(0, color="grey", lw=0.8)
    ax.set_xlabel("change in general_mean vs base model (percentage points)")
    ax.set_ylabel("change in CyberMetric accuracy vs base model (percentage points)")
    ax.set_title("Specialise vs forget: every chapter-10 variant against the untouched Qwen3.5-4B")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8, loc="lower left")
    fig.tight_layout()
    fig.savefig(out_dir / "tradeoff.png", dpi=120)
    console.print(f"wrote {out_dir / 'tradeoff.png'}")


def _plot_per_task(summary: dict, out_dir: Path, plot_cfg: dict) -> None:
    """Grouped bars per general task for base / the forgetting baseline / the best variant.

    `general_mean` is an average over seven very different tasks, and an average can hide a
    disaster: a model can lose 15 points of GSM8K and gain 5 on four multiple-choice tasks and
    come out even. This is the plot that stops the mean from lying.
    """
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    naive_name = plot_cfg.get("naive")
    best_name = (summary.get("best") or {}).get("name")
    by_name = {r["name"]: r for r in summary["rows"]}
    series = [("base model", summary["baseline"].get("general") or {})]
    for label, name in (("forgetting baseline: " + str(naive_name), naive_name),
                        ("best mitigation: " + str(best_name), best_name)):
        row = by_name.get(name)
        if row and row.get("general"):
            series.append((label, row["general"]))
    if len(series) < 2:
        console.print("[yellow]per_task.png skipped: need at least two measured series[/yellow]")
        return

    tasks = [t for t in GENERAL_TASKS if t in series[0][1]]
    x = np.arange(len(tasks))
    width = 0.8 / len(series)
    fig, ax = plt.subplots(figsize=(11, 5.5))
    for i, (label, general) in enumerate(series):
        values = [100 * general.get(t, {}).get("value", 0.0) for t in tasks]
        errors = [100 * general.get(t, {}).get("stderr", 0.0) for t in tasks]
        ax.bar(x + i * width - 0.4 + width / 2, values, width, yerr=errors, capsize=3, label=label)
    ax.set_xticks(x, [f"{t}\n({series[0][1][t]['metric']})" for t in tasks], fontsize=8)
    ax.set_ylabel("score (%)")
    ax.set_title("Per-task general capability (chapter-08 suite, same limits and seed)")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(out_dir / "per_task.png", dpi=120)
    console.print(f"wrote {out_dir / 'per_task.png'}")


def _print_table(summary: dict) -> None:
    table = Table(title="chapter 10 — forgetting mitigations (Qwen3.5-4B)")
    for column in ("variant", "domain acc", "Δ domain", "general_mean", "Δ general", "domain NLL",
                   "general NLL", "train min"):
        table.add_column(column)
    base = summary["baseline"]
    table.add_row("base (chapter 08)", f"{base['domain_accuracy']:.3f}", "-",
                  f"{base['general_mean']:.4f}", "-",
                  f"{base['domain_nll']:.3f}" if base.get("domain_nll") else "-",
                  f"{base['general_nll']:.3f}" if base.get("general_nll") else "-", "-")
    for row in summary["rows"]:
        fmt = lambda v, spec="{:.3f}": "-" if v is None else spec.format(v)  # noqa: E731
        table.add_row(row["name"], fmt(row["domain_accuracy"]), fmt(row["domain_delta_pts"], "{:+.1f}"),
                      fmt(row["general_mean"], "{:.4f}"), fmt(row["general_delta_pts"], "{:+.1f}"),
                      fmt(row["domain_nll"]), fmt(row["general_nll"]), fmt(row["train_minutes"], "{:.1f}"))
    console.print(table)


# =============================================================================== CLI


@app.command("run-all")
def run_all_cmd(
    config: str = typer.Argument(DEFAULT_CONFIG),
    only: str = typer.Option(None, help="run just this one variant"),
) -> None:
    """Train/merge and evaluate every mitigation variant (skips the finished ones)."""
    run_all(config, only=only)


@app.command("report")
def report_cmd(config: str = typer.Argument(DEFAULT_CONFIG)) -> None:
    """Rebuild runs/forget/summary.json and both plots from whatever has been measured."""
    report(config)


@app.command("perplexity-all")
def perplexity_all_cmd(config: str = typer.Argument(DEFAULT_CONFIG)) -> None:
    """Domain + general perplexity for every variant that already has a metrics.json."""
    perplexity_all(config)


@app.command("scale-adapter")
def scale_adapter_cmd(
    adapter_dir: str = typer.Argument(...),
    lam: float = typer.Argument(..., help="0.0 = base model, 1.0 = the fine-tune"),
    out_dir: str = typer.Argument(...),
) -> None:
    """Write a copy of a LoRA adapter whose update is `lam` times as strong."""
    scale_adapter(adapter_dir, lam, out_dir)


@app.command("ties-merge-adapters")
def ties_merge_adapters_cmd(
    base: str = typer.Argument(...),
    adapters: list[str] = typer.Argument(...),
    out_dir: str = typer.Option(...),
    density: float = typer.Option(0.2),
) -> None:
    """TIES-merge several LoRA deltas into one plain bf16 checkpoint."""
    ties_merge_adapters(base, list(adapters), out_dir, density=density)


if __name__ == "__main__":
    app()
