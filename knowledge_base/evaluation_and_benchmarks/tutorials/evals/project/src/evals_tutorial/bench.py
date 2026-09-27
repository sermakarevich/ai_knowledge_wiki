"""Chapter 11: model benchmarks with lm-evaluation-harness against Ollama.

Two public benchmarks — GSM8K (grade-school math word problems, exact match on
the extracted final answer) and IFEval (instruction following, scored by
deterministic checkers) — run on three very different local models through the
harness's `local-chat-completions` backend, which talks OpenAI-chat to our
Ollama server.

The point of the chapter is that a benchmark *score* is not a stable property
of a model: sample size, prompt template, few-shot count and even the
extraction regex all move it. So alongside the three-way model comparison we
run a prompt-sensitivity study on the same 50 questions (0-shot vs 5-shot vs
the CoT template vs our own plain single-shot prompt) and report paired
differences with confidence intervals instead of bare deltas.

Subcommands:
- `run`         run the harness for one (model, task) pair via subprocess
- `collect`     parse the harness output into our metrics.json (bootstrap CI)
- `sensitivity` the four gsm8k prompt variants on one model, paired bootstrap
- `all`         the full chapter pipeline

The harness invocation is the only LLM work here; everything else is parsing
and statistics (NumPy only, via `evals_tutorial.stats`).
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import time
from pathlib import Path

import typer
from rich import print as rprint
from rich.console import Console

from evals_tutorial import stats
from evals_tutorial.config import settings
from evals_tutorial.results import write_metrics

app = typer.Typer(help=__doc__, add_completion=False)
console = Console()

MODELS = ["qwen3.8:27b", "gemma4:latest", "tiny-qwen35-110m-sft:latest"]
TASKS = ["gsm8k", "ifeval"]
QWEN = "qwen3.8:27b"

# (metric, filter) pair that is the "main" number for each task in the
# harness results JSON.
# IFEval's `inst_level_strict_acc` is a LIST of per-instruction scores in each
# sample (not a single 0/1), so keep the primary on the scalar
# `prompt_level_strict_acc` (all-or-nothing per prompt, matches the spec).
PRIMARY_METRIC = {
    "gsm8k": ("exact_match", "flexible-extract"),
    "gsm8k_cot": ("exact_match", "flexible-extract"),
    "ifeval": ("prompt_level_strict_acc", "none"),
}

# Sensitivity variants: label -> harness task / fewshot / output sub-dir.
# `out_subdir` is relative to runs/11_lmeval; the harness then appends its own
# sanitized-model dir underneath. The 5-shot variant deliberately reuses the
# main `gsm8k` run (same 5 few-shots + seed) so its number matches the main
# table exactly and we don't burn 50 extra calls.
# `plain` is handled separately (our own prompt through the cached llm client).
SENSITIVITY = [
    {"label": "0shot", "run_as": "gsm8k", "num_fewshot": 0, "task_key": "gsm8k", "out_subdir": "gsm8k_0shot"},
    {"label": "5shot", "run_as": "gsm8k", "num_fewshot": 5, "task_key": "gsm8k", "out_subdir": "gsm8k"},
    {"label": "cot", "run_as": "gsm8k_cot", "num_fewshot": None, "task_key": "gsm8k_cot", "out_subdir": "gsm8k_cot"},
    {"label": "plain", "run_as": None, "num_fewshot": None, "task_key": None, "out_subdir": None},
]

# Last plausible number anywhere in the reply: handles "#### 42", "$1,234",
# negatives, decimals, "The answer is 7."
PLAIN_ANSWER_RE = re.compile(r"""[-$£€]?\s?\d[\d,]*(?:\.\d+)?""")


def sanitize_model(name: str) -> str:
    """`name:tag` is not a valid directory name — the harness writes `name__tag`."""
    return name.replace(":", "__")


def gsm8k_extract(response: str) -> str | None:
    """Lenient extractor: the last plausible number in the reply, normalized.

    Returns the number as a plain decimal string ("42", "1234", "-7.5") or
    None when the reply contains nothing that looks like a number.
    """
    if not response:
        return None
    matches = PLAIN_ANSWER_RE.findall(response)
    if not matches:
        return None
    raw = matches[-1]
    raw = re.sub(r"[^\d.\-]", "", raw)
    try:
        value = float(raw)
    except ValueError:
        return None
    return str(int(value)) if value == int(value) else str(value)


def build_model_args(model: str, base_url: str | None = None) -> str:
    """The `--model_args` string for our Ollama OpenAI-compatible endpoint."""
    base_url = base_url or f"{settings.ollama_url.rstrip('/')}/v1/chat/completions"
    return (
        f"model={model},"
        f"base_url={base_url},"
        "num_concurrent=1,max_retries=3,tokenized_requests=False"
    )


def harness_run(
    model: str,
    task: str,
    limit: int = 50,
    out_dir: Path | None = None,
    base_url: str | None = None,
    num_fewshot: int | None = None,
    project_root: Path | None = None,
    dry_run: bool = False,
) -> int:
    """Run `lm_eval` for one (model, task) pair; return the exit code.

    With `dry_run=True` only prints the command (tests / planning).
    """
    root = project_root or settings.project_root
    out_dir = out_dir or root / "runs" / "11_lmeval" / task
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        "uv", "run", "lm_eval",
        "--model", "local-chat-completions",
        "--model_args", build_model_args(model, base_url),
        "--tasks", task,
        "--limit", str(limit),
        "--seed", "0",
        "--apply_chat_template",
        "--gen_kwargs", "temperature=0",
        "--output_path", str(out_dir),
        "--log_samples",
    ]
    if num_fewshot is not None:
        cmd += ["--num_fewshot", str(num_fewshot)]
    if dry_run:
        print(" ".join(cmd))
        return 0
    env = dict(os.environ)
    env["OPENAI_API_KEY"] = "ollama"
    env.setdefault("HF_HOME", str(root / "data" / "hf_home"))
    start = time.monotonic()
    proc = subprocess.run(cmd, cwd=str(root), env=env)
    rprint(
        f"[dim]lm_eval exit={proc.returncode} "
        f"({round(time.monotonic() - start)}s) model={model} task={task}[/dim]"
    )
    return proc.returncode


def find_harness_output(out_dir: Path) -> tuple[Path, Path]:
    """Locate the newest (results.json, samples.jsonl) at or under `out_dir`.

    `out_dir` is usually already the harness's model-scoped directory (the
    harness appends its own sanitized-model subdirectory to any `output_path`
    it is given), so prefer a direct glob and only fall back to recursive.
    """
    if not out_dir.exists():
        raise FileNotFoundError(f"no harness output in {out_dir} — run `bench run` first")
    globber = lambda prefix: (
        sorted(out_dir.glob(prefix)) or sorted(out_dir.rglob(prefix))
    )
    results = globber("results*.json")
    samples = globber("samples_*.jsonl")
    if not results or not samples:
        raise FileNotFoundError(f"missing results/samples under {out_dir}")
    return results[-1], samples[-1]


def _sample_correct(row: dict, metric: str) -> float | None:
    """Per-sample 0/1 for a scalar metric; None when the row has no scalar.

    The harness occasionally stores list-valued metrics (e.g. IFEval's
    instruction-level scores) — those are not 0/1 samples so we skip them."""
    if metric not in row:
        return None
    val = row[metric]
    if isinstance(val, (list, tuple)):
        return None
    if val is None:
        return None
    return float(val)


def _resp_text(row: dict) -> str:
    resp = row.get("resps")
    if isinstance(resp, list) and resp:
        first = resp[0]
        if isinstance(first, list) and first:
            return first[0]
        return first
    return "" if resp is None else str(resp)


def _items_gsm8k(rows: list[dict]) -> list[dict]:
    items = []
    for row in rows:
        resp = _resp_text(row)
        target = row.get("target") or ""
        gold = target.split("####")[-1].strip()
        correct = _sample_correct(row, "exact_match")
        items.append({
            "doc_id": row.get("doc_id"),
            "question": (row.get("doc") or {}).get("question", ""),
            "gold": gold,
            "output": resp[:2000],
            "extracted": gsm8k_extract(resp),
            "correct": correct,
        })
    return items


def _items_ifeval(rows: list[dict]) -> list[dict]:
    items = []
    for row in rows:
        resp = _resp_text(row)
        doc = row.get("doc") or {}
        instructions = doc.get("instruction_id_list") or []
        items.append({
            "doc_id": row.get("doc_id"),
            "prompt": (doc.get("instruction_string_response") or "")[:500],
            "n_instructions": len(instructions),
            "output": resp[:2000],
            "prompt_level_strict_acc": row.get("prompt_level_strict_acc"),
            "inst_level_strict_acc": row.get("inst_level_strict_acc"),
            "prompt_level_loose_acc": row.get("prompt_level_loose_acc"),
            "inst_level_loose_acc": row.get("inst_level_loose_acc"),
            "correct": _sample_correct(row, "prompt_level_strict_acc"),
        })
    return items


def collect_experiment(
    task: str,
    model: str,
    limit: int = 50,
    project_root: Path | None = None,
) -> Path:
    """Parse one harness (model, task) output into our metrics.json contract.

    Experiment name: `11_<task>_<model>` (e.g. `11_gsm8k_qwen3.8:27b`).
    """
    root = project_root or settings.project_root
    # All models share one task-level output dir; the harness nests each model
    # in its own sanitized subdirectory, so scope the read to this model's.
    out_dir = root / "runs" / "11_lmeval" / task / sanitize_model(model)
    results_path, samples_path = find_harness_output(out_dir)
    results = json.loads(results_path.read_text())
    task_block = results["results"][task]
    metric, filter_ = PRIMARY_METRIC[task]
    metric_key = f"{metric},{filter_}"
    stderr_key = f"{metric}_stderr,{filter_}"

    rows = [json.loads(line) for line in samples_path.read_text().splitlines() if line.strip()]
    # gsm8k logs ONE row per question PER filter (strict-match +
    # flexible-extract); score exactly the rows of our primary filter.
    if filter_:
        scoped = [r for r in rows if r.get("filter") == filter_]
        if scoped:
            rows = scoped
    per_sample = [v for v in (_sample_correct(r, metric) for r in rows) if v is not None]
    if not per_sample:
        raise ValueError(f"no per-sample `{metric}` values in {samples_path}")

    items = _items_gsm8k(rows) if task.startswith("gsm8k") else _items_ifeval(rows)

    score = float(task_block[metric_key]) if metric_key in task_block else float(sum(per_sample) / len(per_sample))
    lo, hi = stats.bootstrap_ci(per_sample, seed=0)
    harness_stderr = task_block.get(stderr_key)
    try:
        harness_stderr = float(harness_stderr)
    except (TypeError, ValueError):
        harness_stderr = None

    try:
        seconds = float(results.get("total_evaluation_time_seconds") or 0.0)
    except (TypeError, ValueError):
        seconds = 0.0

    experiment = f"11_{task}_{model}"
    out_path = write_metrics(
        experiment=experiment,
        chapter=11,
        n=len(rows),
        metrics={metric: round(score, 6)},
        ci={metric: [round(lo, 4), round(hi, 4)]},
        llm_calls=len(rows),
        seconds=seconds,
        details={
            "model": model,
            "task": task,
            "primary_metric": metric,
            "n_scored": len(per_sample),
            "n_total": len(rows),
            "harness_stderr": harness_stderr,
            "our_bootstrap_ci": [round(lo, 4), round(hi, 4)],
            "comparison": (
                f"harness stderr={harness_stderr} (1 SE, normal approx) vs our "
                f"bootstrap 95% CI [{lo:.4f}, {hi:.4f}] on n={len(per_sample)} items"
            ),
            "notes": f"{task} on {model} via lm-evaluation-harness {results.get('lm_eval_version', '?')}",
        },
        predictions=items,
        config={
            "model_backend": "local-chat-completions",
            "model": model,
            "base_url": (results.get("config", {}).get("model_args") or {}).get("base_url"),
            "task": task,
            "limit": limit,
            "seed": 0,
            "num_fewshot": (results.get("n-shot") or {}).get(task),
            "gen_kwargs": (results.get("config") or {}).get("gen_kwargs"),
            "results_file": str(results_path),
            "samples_file": str(samples_path),
            "lm_eval_version": results.get("lm_eval_version"),
        },
        project_root=root,
    )
    console.print(
        f"[green]{experiment}[/green]: {metric}={score:.4f} "
        f"CI=[{lo:.4f},{hi:.4f}] n={len(rows)}"
    )
    return out_path


def _gold_lookup(per_variant_items: list[dict]) -> dict[str, str]:
    return {it["question"]: it["gold"] for it in per_variant_items if it.get("question")}


def sensitivity(
    model: str = QWEN,
    limit: int = 50,
    project_root: Path | None = None,
    use_llm: bool = True,
) -> Path:
    """Four gsm8k prompt variants on the same `limit` questions; paired bootstrap.

    Variants (each `limit` items, seed 0, temperature 0):
    - 0shot   gsm8k template, 0 fewshots
    - 5shot   gsm8k template, default 5 fewshots
    - cot     the harness `gsm8k_cot` task (different "Q:/A:" template + CoT
      fewshots baked into the yaml)
    - plain   our own `prompts/gsm8k_plain_v1.txt` single-shot prompt through
      `evals_tutorial.llm` (cached), same questions, lenient extractor

    Writes per-variant rows `11_gsm8k_<variant>_<model>` and the summary row
    `11_gsm8k_prompt_sensitivity` (primary metric `score_range`).
    """
    root = project_root or settings.project_root
    base = root / "runs" / "11_lmeval"

    variant_data: dict[str, dict] = {}
    reference_questions: list[str] = []

    for spec in SENSITIVITY:
        label = spec["label"]
        if label == "plain":
            continue  # computed below, needs 5shot items for gold
        # `run_dir` is the task-level output_path (harness appends its own
        # sanitized-model subdir beneath it). Only one model ever runs the
        # on-demand variants, so scoping `read_dir` to that model's subdir is
        # unambiguous — and for 5shot it points straight at the model's main
        # `gsm8k` run (reused, so it never needs regeneration).
        run_dir = base / spec["out_subdir"]
        read_dir = run_dir / sanitize_model(model)
        has_output = bool(list(read_dir.glob("results*.json")))
        if not has_output and spec["label"] != "5shot" and use_llm:
            code = harness_run(
                model,
                spec["run_as"],
                limit=limit,
                out_dir=run_dir,
                num_fewshot=spec["num_fewshot"],
                project_root=root,
            )
            if code != 0:
                raise RuntimeError(f"harness run failed for {model} {spec['label']} (exit {code})")
            has_output = bool(list(read_dir.glob("results*.json")))
        if not has_output:
            console.print(f"[yellow]skipping {label}: no harness output (missing main gsm8k run?)[/yellow]")
            continue
        results_path, samples_path = find_harness_output(read_dir)
        results = json.loads(results_path.read_text())
        rows = [json.loads(line) for line in samples_path.read_text().splitlines() if line.strip()]
        filter_ = PRIMARY_METRIC[spec["task_key"]][1]
        if filter_:
            scoped = [r for r in rows if r.get("filter") == filter_]
            if scoped:
                rows = scoped
        items = _items_gsm8k(rows)
        valid = [it["correct"] for it in items if it["correct"] is not None]
        lo, hi = stats.bootstrap_ci(valid, seed=0)
        score = sum(valid) / len(valid)
        if not reference_questions:
            reference_questions = [it["question"] for it in items]
        harness_block = results["results"].get(spec["task_key"], {})
        variant_data[label] = {
            "score": score,
            "ci": [round(lo, 4), round(hi, 4)],
            "n": len(rows),
            "items": items,
            "harness_score": harness_block.get("exact_match,flexible-extract"),
            "harness_stderr": harness_block.get("exact_match_stderr,flexible-extract"),
            "scored_by": "harness flexible-extract",
            "notes": f"gsm8k {spec['num_fewshot'] if spec['num_fewshot'] is not None else 'cot'}-shot via lm-eval",
        }

    # -- plain variant: our own prompt, through the cached Ollama client --
    if use_llm:
        from evals_tutorial.llm import Ollama

        prompt_text = (root / "src" / "evals_tutorial" / "prompts" / "gsm8k_plain_v1.txt").read_text()
        client = Ollama()
        golds = _gold_lookup(variant_data.get("5shot", {}).get("items", []))
        plain_items: list[dict] = []
        t_total = 0.0
        for i, question in enumerate(reference_questions):
            t0 = time.monotonic()
            try:
                reply = client.chat(
                    [{"role": "user", "content": prompt_text.format(question=question)}],
                    model=model,
                )
            except Exception as exc:  # record and keep going
                reply = ""
                rprint(f"[yellow]plain call failed (item {i}): {exc}[/yellow]")
            t_total += time.monotonic() - t0
            extracted = gsm8k_extract(reply)
            gold = golds.get(question)
            if extracted is None or gold is None:
                correct = None
            else:
                correct = 1.0 if extracted == gold.strip() else 0.0
            plain_items.append({
                "question": question,
                "gold": gold,
                "output": (reply or "")[:2000],
                "extracted": extracted,
                "correct": correct,
            })
        valid = [it["correct"] for it in plain_items if it["correct"] is not None]
        if not valid:
            raise ValueError("plain variant produced no scored items")
        lo, hi = stats.bootstrap_ci(valid, seed=0)
        variant_data["plain"] = {
            "score": sum(valid) / len(valid),
            "ci": [round(lo, 4), round(hi, 4)],
            "n": len(plain_items),
            "items": plain_items,
            "scored_by": "our gsm8k_plain_v1 + lenient regex",
            "notes": "single-shot custom prompt via evals_tutorial.llm (cached)",
        }

    labels = list(variant_data.keys())
    if len(labels) < 2:
        raise ValueError("need at least 2 variants for the sensitivity study")

    # Align on the questions common to every variant.
    qsets = {
        v: {it["question"]: it for it in info["items"] if it.get("question")}
        for v, info in variant_data.items()
    }
    common = set.intersection(*[set(d) for d in qsets.values()])
    order = [q for q in reference_questions if q in common] or sorted(common)
    aligned = {v: {q: qsets[v][q]["correct"] for q in order} for v in labels}

    # Write per-variant experiment rows (they show up in results.md too).
    for v in labels:
        info = variant_data[v]
        write_metrics(
            experiment=f"11_gsm8k_{v}_{model}",
            chapter=11,
            n=int(info["n"]),
            metrics={"exact_match": round(info["score"], 6)},
            ci={"exact_match": list(info["ci"])},
            llm_calls=int(info["n"]),
            seconds=0.0,
            details={
                "variant": v,
                "sensitivity_member": True,
                "scored_by": info.get("scored_by", ""),
                "harness_score": info.get("harness_score"),
                "notes": info.get("notes", ""),
            },
            predictions=[
                {"question": it.get("question"),
                 "gold": it.get("gold"),
                 "output": it.get("output"),
                 "extracted": it.get("extracted"),
                 "correct": it.get("correct")}
                for it in info["items"]
            ],
            config={"variant": v, "model": model, "limit": limit, "seed": 0},
            project_root=root,
        )

    # Paired differences and flip counts between every pair of variants.
    pair_results: dict[str, dict] = {}
    flip_counts: dict[str, int] = {}
    for i, a in enumerate(labels):
        for b in labels[i + 1:]:
            xs = [aligned[a][q] for q in order]
            ys = [aligned[b][q] for q in order]
            mask = [x is not None and y is not None for x, y in zip(xs, ys)]
            if sum(mask) < 5:
                continue
            pair_results[f"{a}_vs_{b}"] = stats.paired_bootstrap(
                [x for x, m in zip(xs, mask) if m],
                [y for y, m in zip(ys, mask) if m],
                seed=0,
            )
            flip_counts[f"{a}_vs_{b}"] = sum(
                1 for x, y, m in zip(xs, ys, mask) if m and round(float(x), 3) != round(float(y), 3)
            )

    any_flip = [
        q for q in order
        if len({round(float(aligned[v][q]), 3) for v in labels
                if aligned[v][q] is not None}) > 1
    ]
    example_flip = None
    if any_flip:
        ex_q = any_flip[0]
        example_flip = {
            "question": ex_q,
            "per_variant": {
                v: {
                    "correct": aligned[v][ex_q],
                    "extracted": qsets[v][ex_q].get("extracted"),
                }
                for v in labels
            },
        }

    scores = [variant_data[v]["score"] for v in labels]
    metrics: dict[str, float] = {"score_range": round(max(scores) - min(scores), 6)}
    ci: dict[str, list[float]] = {}
    for v in labels:
        metrics[f"score_{v}"] = round(variant_data[v]["score"], 6)
        ci[f"score_{v}"] = list(variant_data[v]["ci"])

    details = {
        "model": model,
        "n_common_questions": len(order),
        "variants": {
            v: {
                "score": variant_data[v]["score"],
                "ci": list(variant_data[v]["ci"]),
                "scored_by": variant_data[v].get("scored_by", ""),
                "harness_score": variant_data[v].get("harness_score"),
                "harness_stderr": variant_data[v].get("harness_stderr"),
            }
            for v in labels
        },
        "paired": pair_results,
        "flip_counts": flip_counts,
        "n_flips_any_variant": len(any_flip),
        "example_flip": example_flip,
        "notes": "prompt sensitivity: 0-shot / 5-shot / CoT / plain on the same questions",
    }

    all_predictions: list[dict] = []
    for v in labels:
        for it in variant_data[v]["items"]:
            all_predictions.append({
                "variant": v,
                "question": it.get("question"),
                "gold": it.get("gold"),
                "output": (it.get("output") or "")[:1000],
                "extracted": it.get("extracted"),
                "correct": it.get("correct"),
            })

    exp_name = "11_gsm8k_prompt_sensitivity" if model == QWEN else f"11_gsm8k_prompt_sensitivity_{model}"
    out = write_metrics(
        experiment=exp_name,
        chapter=11,
        n=len(order),
        metrics=metrics,
        ci=ci,
        llm_calls=sum(len(variant_data[v]["items"]) for v in labels),
        seconds=0.0,
        details=details,
        predictions=all_predictions,
        config={
            "model": model,
            "limit": limit,
            "seed": 0,
            "variants": labels,
            "plain_prompt": "prompts/gsm8k_plain_v1.txt",
        },
        project_root=root,
    )
    console.print(
        f"[green]sensitivity[/green]: range={metrics['score_range']:.4f} "
        f"flips={len(any_flip)}/{len(order)} on {model}"
    )
    return out


def run_all(
    limit: int = 50,
    project_root: Path | None = None,
    models: list[str] | None = None,
    sensitivity_model: str | None = None,
) -> None:
    """Full chapter pipeline: (models x tasks) harness runs + collect + sensitivity.

    `sensitivity` runs the missing 0/5-shot harness variants itself (and the
    plain variant via the cached llm client), so this stays ~30 harness runs
    + 50 cached-able chat calls.
    """
    models = models or MODELS
    sens_model = sensitivity_model or QWEN

    for model in models:
        for task in TASKS:
            harness_run(model, task, limit=limit, project_root=project_root)

    for model in models:
        for task in TASKS:
            collect_experiment(task, model, limit=limit, project_root=project_root)

    sensitivity(
        sens_model,
        limit=limit,
        project_root=project_root,
    )


# ---------------------------------------------------------------------------
# Typer CLI
# ---------------------------------------------------------------------------
@app.command("run")
def run_cmd(
    model: str = typer.Option(QWEN, help="Ollama model name (e.g. qwen3.8:27b)"),
    task: str = typer.Option("gsm8k", help="harness task name: gsm8k, ifeval, gsm8k_cot, gsm8k_zeroshot"),
    limit: int = typer.Option(50, help="max items"),
    out_dir: Path | None = typer.Option(None, help="override output dir"),
    num_fewshot: int | None = typer.Option(None, help="override fewshot count"),
    dry_run: bool = typer.Option(False, "--dry-run", help="print the command only"),
) -> None:
    """Run the harness for one (model, task) pair."""
    code = harness_run(model, task, limit=limit, out_dir=out_dir, num_fewshot=num_fewshot, dry_run=dry_run)
    if code != 0 and not dry_run:
        raise typer.Exit(code)


@app.command("collect")
def collect_cmd(
    model: str = typer.Option(QWEN),
    task: str = typer.Option("gsm8k"),
    limit: int = typer.Option(50),
) -> None:
    """Parse harness output for one (model, task) into runs/<experiment>."""
    collect_experiment(task, model, limit=limit)


@app.command("sensitivity")
def sensitivity_cmd(
    model: str = typer.Option(QWEN),
    limit: int = typer.Option(50),
    no_llm: bool = typer.Option(False, "--no-llm", help="skip the plain (llm) variant"),
) -> None:
    """Run the 4-variant gsm8k prompt-sensitivity study on one model."""
    sensitivity(model, limit=limit, use_llm=not no_llm)


@app.command("all")
def all_cmd(
    limit: int = typer.Option(50),
) -> None:
    """The whole chapter: 6 harness runs + collect + sensitivity (qwen)."""
    run_all(limit=limit)


if __name__ == "__main__":
    app()
