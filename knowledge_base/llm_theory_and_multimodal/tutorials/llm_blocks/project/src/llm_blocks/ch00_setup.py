"""Chapter 00 — setup: prove the environment and the plotting pipeline work.

`uv run python -m llm_blocks.ch00_setup check` prints library versions and draws
the smoke-test figure; `plots` draws the same figure (the one this chapter embeds).
"""

from __future__ import annotations

import numpy as np
import torch
import transformers
import typer

from llm_blocks import plotting
from llm_blocks.plotting import annotate_arrow, save, style

app = typer.Typer(add_completion=False, no_args_is_help=False)


def _smoke_figure():
    """A sine wave with an annotated arrow: if this PNG exists, `save()` works end to end."""
    style()
    import matplotlib.pyplot as plt

    x = np.linspace(0, 4 * np.pi, 400)
    y = np.sin(x)

    fig, ax = plt.subplots()
    ax.plot(x, y, label="sin(x)")
    peak = np.pi / 2
    annotate_arrow(
        ax,
        "first peak: proves plotting + annotation work",
        xy=(peak, 1.0),
        xytext=(peak + 3, 1.2),
    )
    ax.set_xlabel("x")
    ax.set_ylabel("sin(x)")
    ax.set_title("00 — smoke test: if you can see this, the pipeline works")
    ax.legend()
    return save(fig, "00_smoke")


@app.command()
def check() -> None:
    """Print versions/environment info and draw the smoke figure."""
    print(f"torch: {torch.__version__}")
    print(f"transformers: {transformers.__version__}")
    print(f"cpu threads: {torch.get_num_threads()}")
    print(f"torch.cuda.is_available(): {torch.cuda.is_available()}")

    plotting.ASSETS.mkdir(parents=True, exist_ok=True)
    print(f"assets dir: {plotting.ASSETS} (exists: {plotting.ASSETS.is_dir()})")

    path = _smoke_figure()
    print(f"wrote: {path}")


@app.command()
def plots() -> None:
    """Regenerate every figure for this chapter (just the smoke figure)."""
    path = _smoke_figure()
    print(f"wrote: {path}")


if __name__ == "__main__":
    app()
