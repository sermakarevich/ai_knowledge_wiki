"""Tests for the chapter 00 skeleton: save(), style(), and the smoke figure."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from typer.testing import CliRunner

from llm_blocks import plotting
from llm_blocks.ch00_setup import app

runner = CliRunner()


def test_save_writes_png(tmp_path, monkeypatch):
    monkeypatch.setattr(plotting, "ASSETS", tmp_path)

    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    path = plotting.save(fig, "unit_test")

    assert path == tmp_path / "unit_test.png"
    assert path.is_file()
    assert path.stat().st_size > 0


def test_style_is_idempotent():
    plotting.style()
    first = dict(plt.rcParams)
    plotting.style()
    second = dict(plt.rcParams)

    assert first["figure.figsize"] == second["figure.figsize"]
    assert first["figure.dpi"] == second["figure.dpi"]
    assert first["grid.alpha"] == second["grid.alpha"]


def test_ch00_plots_runs(tmp_path, monkeypatch):
    monkeypatch.setattr(plotting, "ASSETS", tmp_path)

    result = runner.invoke(app, ["plots"])

    assert result.exit_code == 0
    assert (tmp_path / "00_smoke.png").is_file()


def test_ch00_check_runs(tmp_path, monkeypatch):
    monkeypatch.setattr(plotting, "ASSETS", tmp_path)

    result = runner.invoke(app, ["check"])

    assert result.exit_code == 0
    assert "torch" in result.stdout
    assert (tmp_path / "00_smoke.png").is_file()
