"""Shared plotting helpers so every chapter produces figures that look the same.

Uses the non-interactive "Agg" backend: on macOS the default backend can try to open
a GUI window, which fails or hangs when a script is run from a terminal / CI. Agg
renders straight to a PNG file with no window, which is all `save()` needs.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

from pathlib import Path

import matplotlib.pyplot as plt

ASSETS = Path(__file__).resolve().parents[3] / "assets"

_COLORS = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd", "#ff7f0e", "#17becf"]


def style() -> None:
    """Set the rcParams every chapter figure should share. Safe to call more than once."""
    plt.rcParams.update(
        {
            "figure.figsize": (8, 4.5),
            "figure.dpi": 130,
            "axes.grid": True,
            "grid.alpha": 0.3,
            "axes.prop_cycle": plt.cycler(color=_COLORS),
        }
    )


def save(fig: plt.Figure, name: str) -> Path:
    """Write `fig` to `ASSETS/{name}.png` (tight bbox, 130 dpi) and close it."""
    ASSETS.mkdir(parents=True, exist_ok=True)
    path = ASSETS / f"{name}.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def annotate_arrow(ax: plt.Axes, text: str, xy: tuple[float, float], xytext: tuple[float, float]) -> None:
    """Draw an annotated arrow from `xytext` to `xy` with `text` at the tail."""
    ax.annotate(
        text,
        xy=xy,
        xytext=xytext,
        arrowprops={"arrowstyle": "->", "color": "black", "lw": 1.2},
        fontsize=10,
    )
