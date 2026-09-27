"""YAML config loading and the per-run output layout every chapter writes to."""

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import yaml
from pydantic import BaseModel, Field

RUNS_DIR = Path(__file__).resolve().parents[2] / "runs"


def load_yaml(path: str | Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


@dataclass(frozen=True)
class RunPaths:
    """Where one run's outputs live: runs/<run_name>/{metrics.json,samples.md,loss.png,checkpoints/}."""

    run_name: str
    root: Path = RUNS_DIR

    @property
    def run_dir(self) -> Path:
        return self.root / self.run_name

    @property
    def metrics_json(self) -> Path:
        return self.run_dir / "metrics.json"

    @property
    def samples_md(self) -> Path:
        return self.run_dir / "samples.md"

    @property
    def loss_png(self) -> Path:
        return self.run_dir / "loss.png"

    @property
    def checkpoints_dir(self) -> Path:
        return self.run_dir / "checkpoints"

    def ensure(self) -> "RunPaths":
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.checkpoints_dir.mkdir(parents=True, exist_ok=True)
        return self


# ---------------------------------------------------------------------------- chapter 08 schema


class GeneralTaskResult(BaseModel):
    metric: str
    value: float
    stderr: float | None = None


class DomainResult(BaseModel):
    dataset: str
    split: str
    n: int
    accuracy: float
    ci95: tuple[float, float]
    per_category: dict[str, float] = Field(default_factory=dict)


class JudgeResult(BaseModel):
    n: int
    mean_score: float


class CostResult(BaseModel):
    wall_seconds: float
    peak_gb: float | None = None


class RunMetrics(BaseModel):
    """The fixed schema every chapter-08+ run writes into `runs/<run>/metrics.json`.

    Every section (`train`/`general`/`domain`/`judge`/`cost`) is optional on its own — a
    domain-only run does not need a `general` suite and vice versa — but any section that is
    present must match this shape, so chapter 09/10 can load and compare runs mechanically.
    """

    run_name: str
    model: str
    base: str | None = None
    stage: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    train: dict = Field(default_factory=dict)
    general: dict[str, GeneralTaskResult] = Field(default_factory=dict)
    general_mean: float | None = None
    domain: DomainResult | None = None
    judge: JudgeResult | None = None
    cost: CostResult | None = None


def write_metrics(run_dir: str | Path, metrics: dict) -> Path:
    """Merge `metrics` into `<run_dir>/metrics.json`, creating it if needed."""
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = run_dir / "metrics.json"
    existing = {}
    if metrics_path.exists():
        existing = json.loads(metrics_path.read_text())
    existing.update(metrics)
    metrics_path.write_text(json.dumps(existing, indent=2, sort_keys=True))
    return metrics_path
