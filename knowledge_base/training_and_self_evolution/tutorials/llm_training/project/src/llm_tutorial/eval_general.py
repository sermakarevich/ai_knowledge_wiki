"""Chapter 08 — the general-capability suite: EleutherAI's `lm-evaluation-harness` (`lm_eval`
0.4.12), run against an HF checkpoint (`--model hf`) or an Ollama model through its
OpenAI-compatible endpoint (`--model local-chat-completions` / `local-completions`).

    run-hf model_dir out_dir              - lm_eval CLI against a saved HF folder (needs GPU)
    run-ollama model_name out_dir         - lm_eval CLI against an Ollama model over HTTP
    summarize out_dir                    - parse out_dir/results.json into {task: {metric, ...}}

Loglikelihood vs generative tasks: `mmlu`/`arc_challenge`/`hellaswag`/`winogrande`/
`truthfulqa_mc2` are *loglikelihood* tasks — lm_eval scores each answer choice by feeding
"<question><choice>" through the model and comparing the SUM of the model's own token
log-probabilities for each choice, then picks the highest-scoring one. It never asks the model
to "generate an answer letter". `gsm8k`/`ifeval` are *generative* tasks: the model actually
generates free text, which is then checked (exact numeric match / instruction-following rules).

This distinction is why Ollama can only run half the suite: Ollama's OpenAI-compatible
`/v1/completions` endpoint does not return per-token logprobs for arbitrary continuations (it
truncates/omits `logprobs` for anything beyond very small requests, and `/v1/chat/completions`
never returns them at all), so lm_eval's `local-completions`/`local-chat-completions` models can
only run generative tasks against it. Loglikelihood tasks (mmlu, arc_challenge, hellaswag,
winogrande, truthfulqa_mc2) need the HF path, where lm_eval reads real logits.
"""

import json
import subprocess
import time
from pathlib import Path

import typer
from rich.console import Console

from .config import load_yaml, write_metrics

app = typer.Typer(add_completion=False, help=__doc__)
console = Console()

DEFAULT_CONFIG = "configs/eval_general.yaml"
DEFAULT_OLLAMA_BASE_URL = "http://127.0.0.1:11434/v1"

# lm_eval reports several metrics per task (e.g. "acc,none" and "acc_norm,none"); this is the one
# each benchmark is conventionally reported by. Any task not listed falls back to the first
# non-stderr metric found for it.
PRIMARY_METRIC = {
    "mmlu": "acc,none",
    "arc_challenge": "acc_norm,none",
    "hellaswag": "acc_norm,none",
    "winogrande": "acc,none",
    "truthfulqa_mc2": "acc,none",
    "gsm8k": "exact_match,flexible-extract",
    "ifeval": "prompt_level_strict_acc,none",
}

# Only these are loglikelihood tasks; the rest of the suite is generative (see module docstring).
LOGLIKELIHOOD_TASKS = {"mmlu", "arc_challenge", "hellaswag", "winogrande", "truthfulqa_mc2"}
GENERATIVE_TASKS = {"gsm8k", "ifeval"}


# --------------------------------------------------------------------------------- results.json parsing


def parse_results_json(results: dict, tasks: list[str] | None = None) -> dict[str, dict]:
    """Parse an lm_eval `results.json` `{"results": {task: {"metric,filter": value, ...}}}` dict
    into `{task: {"metric": str, "value": float, "stderr": float | None}}`, picking each task's
    conventional primary metric (falling back to the first non-stderr metric found)."""
    task_results = results.get("results", {})
    tasks = tasks if tasks is not None else list(task_results.keys())
    parsed: dict[str, dict] = {}
    for task in tasks:
        entry = task_results.get(task)
        if entry is None:
            continue
        metric_key = PRIMARY_METRIC.get(task)
        if metric_key is None or metric_key not in entry:
            metric_key = next(
                (k for k in entry if not k.endswith("_stderr,none") and k != "alias" and isinstance(entry[k], (int, float))),
                None,
            )
        if metric_key is None:
            continue
        metric_name = metric_key.split(",")[0]
        stderr_key = f"{metric_name}_stderr,{metric_key.split(',', 1)[1]}" if "," in metric_key else None
        parsed[task] = {
            "metric": metric_name,
            "value": float(entry[metric_key]),
            "stderr": float(entry[stderr_key]) if stderr_key and stderr_key in entry else None,
        }
    return parsed


def summarize(results: dict, tasks: list[str] | None = None) -> dict:
    """`parse_results_json` plus `general_mean` (the mean of the tasks' primary metric values)."""
    parsed = parse_results_json(results, tasks)
    values = [v["value"] for v in parsed.values()]
    general_mean = sum(values) / len(values) if values else 0.0
    return {"general": parsed, "general_mean": general_mean}


# --------------------------------------------------------------------------------- running lm_eval


def _limit_and_fewshot(task: str, cfg: dict) -> tuple[int | None, int]:
    limit = cfg.get("limit", {}).get(task)
    num_fewshot = cfg.get("num_fewshot", {}).get(task, 0)
    return limit, num_fewshot


def run_hf(
    model_dir: str,
    out_dir: str,
    tasks: list[str] | None = None,
    config_path: str = DEFAULT_CONFIG,
    adapter: str | None = None,
    limit_scale: float = 1.0,
) -> dict:
    """Run `lm_eval --model hf` once per task (each task can have its own `--num_fewshot`/
    `--limit`), merge every task's `results.json` into one dict, and write `metrics.json`.

    The `lm_eval` CLI (not its Python API) is used deliberately: it is the interface documented
    and version-pinned by EleutherAI, it prints its own progress bars for a 45-minute suite, and
    it writes one `results.json` + `--log_samples` per invocation that this function only parses.
    """
    cfg = load_yaml(config_path)
    tasks = tasks or cfg["tasks"]
    out_dir_path = Path(out_dir)
    out_dir_path.mkdir(parents=True, exist_ok=True)

    model_args = f"pretrained={model_dir},dtype=bfloat16,trust_remote_code=False"
    if adapter:
        model_args += f",peft={adapter}"

    merged_results: dict = {"results": {}}
    start = time.monotonic()
    for task in tasks:
        limit, num_fewshot = _limit_and_fewshot(task, cfg)
        scaled_limit = max(1, int(limit * limit_scale)) if limit else None
        task_out = out_dir_path / task
        cmd = [
            "lm_eval", "--model", "hf", "--model_args", model_args,
            "--tasks", task, "--num_fewshot", str(num_fewshot),
            "--batch_size", str(cfg.get("batch_size", "auto")),
            "--seed", str(cfg.get("seed", 1234)),
            "--output_path", str(task_out), "--log_samples",
        ]
        if scaled_limit:
            cmd += ["--limit", str(scaled_limit)]
        console.print(f"[bold]$ {' '.join(cmd)}[/bold]")
        subprocess.run(cmd, check=True)
        merged_results["results"].update(_load_task_results(task_out))
    wall_seconds = time.monotonic() - start

    summary = summarize(merged_results, tasks)
    summary["cost"] = {"wall_seconds": wall_seconds}
    write_metrics(out_dir, summary)
    return summary


def _load_task_results(task_out: Path) -> dict:
    """`lm_eval --output_path <dir>` writes `<dir>/<hashed-run-dir>/results_*.json`; find and
    load the one `results` dict it contains."""
    candidates = list(task_out.rglob("results_*.json"))
    if not candidates:
        raise FileNotFoundError(f"no results_*.json found under {task_out}")
    data = json.loads(candidates[0].read_text())
    return data.get("results", {})


def run_ollama(
    model_name: str,
    out_dir: str,
    tasks: list[str] | None = None,
    config_path: str = DEFAULT_CONFIG,
    base_url: str = DEFAULT_OLLAMA_BASE_URL,
) -> dict:
    """Run only the GENERATIVE tasks (gsm8k, ifeval) against an Ollama model through lm_eval's
    `local-chat-completions` model type, which speaks Ollama's OpenAI-compatible `/v1/chat/
    completions`. Loglikelihood tasks are skipped with a clear message (see module docstring)."""
    cfg = load_yaml(config_path)
    requested = tasks or cfg["tasks"]
    skipped = [t for t in requested if t in LOGLIKELIHOOD_TASKS]
    runnable = [t for t in requested if t in GENERATIVE_TASKS]
    if skipped:
        console.print(
            f"[yellow]skipping loglikelihood tasks over Ollama (no logprobs endpoint): {skipped}. "
            "Run these against the HF checkpoint instead (`run_hf`).[/yellow]"
        )

    out_dir_path = Path(out_dir)
    out_dir_path.mkdir(parents=True, exist_ok=True)
    model_args = f"model={model_name},base_url={base_url}/chat/completions,num_concurrent=1,max_retries=3"

    merged_results: dict = {"results": {}}
    start = time.monotonic()
    for task in runnable:
        _, num_fewshot = _limit_and_fewshot(task, cfg)
        limit = cfg.get("limit", {}).get(task)
        task_out = out_dir_path / task
        cmd = [
            "lm_eval", "--model", "local-chat-completions", "--model_args", model_args,
            "--tasks", task, "--num_fewshot", str(num_fewshot),
            "--apply_chat_template",
            "--output_path", str(task_out), "--log_samples",
        ]
        if limit:
            cmd += ["--limit", str(limit)]
        console.print(f"[bold]$ {' '.join(cmd)}[/bold]")
        subprocess.run(cmd, check=True)
        merged_results["results"].update(_load_task_results(task_out))
    wall_seconds = time.monotonic() - start

    summary = summarize(merged_results, runnable)
    summary["cost"] = {"wall_seconds": wall_seconds}
    summary["skipped_loglikelihood_tasks"] = skipped
    write_metrics(out_dir, summary)
    return summary


# --------------------------------------------------------------------------------- CLI


@app.command(name="run-hf")
def run_hf_cmd(
    model_dir: str = typer.Argument(...),
    out_dir: str = typer.Argument(...),
    tasks: str = typer.Option(None, help="comma-separated subset of configs/eval_general.yaml tasks"),
    config_path: str = typer.Option(DEFAULT_CONFIG, help="alternate eval_general.yaml, e.g. a batch_size variant"),
    adapter: str = typer.Option(None),
    limit_scale: float = typer.Option(1.0),
) -> None:
    task_list = tasks.split(",") if tasks else None
    summary = run_hf(model_dir, out_dir, tasks=task_list, config_path=config_path, adapter=adapter, limit_scale=limit_scale)
    console.print(summary)


@app.command(name="run-ollama")
def run_ollama_cmd(
    model_name: str = typer.Argument(...),
    out_dir: str = typer.Argument(...),
    tasks: str = typer.Option(None),
) -> None:
    task_list = tasks.split(",") if tasks else None
    summary = run_ollama(model_name, out_dir, tasks=task_list)
    console.print(summary)


if __name__ == "__main__":
    app()
