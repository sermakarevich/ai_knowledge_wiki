"""Chapter 11 tests: parser, extractor, model-args, sensitivity plumbing.

Everything here is offline (no Ollama, no network). The one test that would
need a live harness + GPU is `@pytest.mark.slow`.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from evals_tutorial import bench


# ---------------------------------------------------------------------------
# extractor + model args
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "text, expected",
    [
        ("the work is 16 - 3 - 4 = 9, 9 * 2 = 18\n#### 18", "18"),
        ("Janet makes $1,234 per day. The answer is 7.", "7"),
        ("$1,234", "1234"),
        ("Answer: -7.5", "-7.5"),
        ("no number here", None),
        ("twelve 12 apples", "12"),
        ("", None),
    ],
)
def test_gsm8k_extract_tricky(text, expected):
    assert bench.gsm8k_extract(text) == expected


def test_build_model_args_shape():
    s = bench.build_model_args("qwen3.8:27b")
    assert s.startswith("model=qwen3.8:27b,base_url=http://127.0.0.1:11435/v1/chat/completions")
    assert "num_concurrent=1" in s and "max_retries=3" in s and "tokenized_requests=False" in s


def test_sanitize_model():
    assert bench.sanitize_model("gemma4:latest") == "gemma4__latest"
    assert bench.sanitize_model("qwen3.8:27b") == "qwen3.8__27b"


def test_harness_run_dry_run(capsys):
    code = bench.harness_run("qwen3.8:27b", "gsm8k", limit=50, dry_run=True)
    assert code == 0
    printed = capsys.readouterr().out
    assert "lm_eval" in printed and "--tasks gsm8k" in printed
    assert "--limit 50" in printed and "local-chat-completions" in printed


# ---------------------------------------------------------------------------
# collector parsing a miniature harness output
# ---------------------------------------------------------------------------
def _write_harness_out(base: Path, model: str, task: str, n: int, correct: list[int]) -> None:
    """Write a miniature lm_eval output the way the harness does: it appends its own
    sanitized-model subdirectory to whatever `output_path` it is given, then writes
    results*.json + samples_*.jsonl into that nested dir. We pass
    `runs/11_lmeval/<task>` as output_path, so files land under
    `runs/11_lmeval/<task>/<sanitized_model>/` — and the reader rglobs under
    `runs/11_lmeval/<task>` to find them (model-agnostic)."""
    metric = bench.PRIMARY_METRIC[task][0]
    subdir = base / "runs" / "11_lmeval" / task / bench.sanitize_model(model)
    filter_ = bench.PRIMARY_METRIC[task][1]
    score = sum(correct) / n
    results = {
        "results": {
            task: {
                "name": task,
                "sample_len": n,
                f"{metric},{filter_}": score,
                f"{metric}_stderr,{filter_}": 0.1 if n > 1 else "N/A",
            }
        },
        "n-shot": {task: 5 if task.startswith("gsm8k") else 0},
        "config": {
            "model_args": {"base_url": "http://127.0.0.1:11435/v1/chat/completions", "model": model},
            "gen_kwargs": {"temperature": 0},
        },
        "lm_eval_version": "0.4.13",
        "total_evaluation_time_seconds": "12.5",
    }
    out_dir = base / "runs" / "11_lmeval" / bench.sanitize_model(model) / task
    subdir.mkdir(parents=True, exist_ok=True)
    (subdir / "results_2026-09-05T12-00-00.json").write_text(json.dumps(results))
    lines = []
    for i in range(n):
        if task == "gsm8k":
            row = {
                "doc_id": i,
                "doc": {"question": f"q{i}", "answer": f"work{i}\n#### {i + 1}"},
                "target": f"work{i}\n#### {i + 1}",
                "resps": [[f"worked it out\n#### {i + 1}"]] if correct[i] else [["worked it out\n#### 99"]],
                "filtered_resps": [str(i + 1) if correct[i] else "99"],
                "filter": "flexible-extract",
                "metrics": ["exact_match"],
                "exact_match": float(correct[i]),
            }
        else:
            row = {
                "doc_id": i,
                "doc": {},
                "target": "",
                "resps": [[f"reply{i}"]],
                "filtered_resps": [f"reply{i}"],
                "filter": "none",
                "metrics": [metric],
                metric: float(correct[i]),
            }
        lines.append(json.dumps(row))
    (subdir / "samples_x_2026-09-05T12-00-00.jsonl").write_text("\n".join(lines) + "\n")


def test_collect_gsm8k_fixture(tmp_path):
    _write_harness_out(tmp_path, "gemma4:latest", "gsm8k", n=5, correct=[1, 0, 1, 1, 0])
    out = bench.collect_experiment("gsm8k", "gemma4:latest", project_root=tmp_path)
    rec = json.loads((out.parent / "metrics.json").read_text())
    assert rec["experiment"] == "11_gsm8k_gemma4:latest"
    assert rec["n"] == 5
    assert rec["metrics"] == {"exact_match": pytest.approx(0.6)}
    lo, hi = rec["ci"]["exact_match"]
    assert lo <= 0.6 <= hi
    assert rec["details"]["harness_stderr"] == pytest.approx(0.1)
    cfg = json.loads((out.parent / "config.json").read_text())
    assert cfg["model"] == "gemma4:latest"
    preds = (out.parent / "predictions.jsonl").read_text().splitlines()
    assert len(preds) == 5
    first = json.loads(preds[0])
    assert first["gold"] == "1" and first["extracted"] == "1" and first["correct"] == 1.0


def test_collect_ifeval_fixture(tmp_path):
    _write_harness_out(tmp_path, "tiny-qwen35-110m-sft:latest", "ifeval", n=4, correct=[1, 1, 0, 1])
    out = bench.collect_experiment("ifeval", "tiny-qwen35-110m-sft:latest", project_root=tmp_path)
    rec = json.loads((out.parent / "metrics.json").read_text())
    assert rec["metrics"] == {"prompt_level_strict_acc": pytest.approx(0.75)}
    assert rec["llm_calls"] == 4


def test_find_harness_output_missing_is_clear(tmp_path):
    with pytest.raises(FileNotFoundError, match="run `bench run` first"):
        bench.find_harness_output(tmp_path / "does" / "not" / "exist")
