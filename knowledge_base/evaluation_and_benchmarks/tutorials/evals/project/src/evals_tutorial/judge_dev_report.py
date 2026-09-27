"""Chapter 05a (dev half): read the dev-alignment records and emit

- `runs/05_align_dev.md`   — scorecard: mode | version | TPR | TNR | acc | kappa | chosen
- `runs/05_dev/<mode>_<version>.jsonl` — per-ticket predictions (one JSON row per line)

No LLM calls: everything is already in `runs/05_judge_align/<mode>.json`.
"""

from __future__ import annotations

import json
from pathlib import Path

from evals_tutorial.config import settings
from evals_tutorial.judge import tracked_modes


def main() -> None:
    align_dir = settings.path("runs") / "05_judge_align"
    dev_dir = settings.path("runs") / "05_dev"
    dev_dir.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Chapter 05a — dev-split judge alignment scorecard",
        "",
        "Aligned the v1 (zero-shot) and v2 (few-shot) binary judge of each tracked mode against the",
        "chapter-03 human labels on the `dev` split (20 tickets). Chosen version per mode = higher",
        "Cohen's kappa on dev. Predictions: `runs/05_dev/<mode>_<version>.jsonl`.",
        "",
        "| mode | version | TPR | TNR | acc | kappa | chosen |",
        "|---|---|---|---|---|---|---|",
    ]

    for mode in tracked_modes():
        rec = json.loads((align_dir / f"{mode}.json").read_text())
        chosen = rec["best"]
        for version in ("v1", "v2"):
            v = rec["versions"][version]
            star = " <-" if version == chosen else ""
            lines.append(
                f"| {mode} | {version}{star} | {v['tpr']:.3f} | {v['tnr']:.3f} | {v['accuracy']:.3f} | {v['kappa']:.3f} | {chosen if version == chosen else ''} |"
            )
        with (dev_dir / f"{mode}_v1.jsonl").open("w") as f:
            for row in rec["versions"]["v1"]["rows"]:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
        with (dev_dir / f"{mode}_v2.jsonl").open("w") as f:
            for row in rec["versions"]["v2"]["rows"]:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")

    (settings.path("runs") / "05_align_dev.md").write_text("\n".join(lines) + "\n")
    print(f"wrote {settings.path('runs') / '05_align_dev.md'} and {dev_dir}/*.jsonl")


if __name__ == "__main__":
    main()
