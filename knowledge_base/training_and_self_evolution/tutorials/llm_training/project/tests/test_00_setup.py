"""Tests for the chapter 00 skeleton: gpu parsing, config metrics merge, and check --cpu."""

import json

from typer.testing import CliRunner

from llm_tutorial import gpu
from llm_tutorial.check import app
from llm_tutorial.config import write_metrics

runner = CliRunner()

NVIDIA_SMI_HEADER = """index, name, memory.used [MiB], memory.total [MiB], utilization.gpu [%]
0, NVIDIA GeForce RTX 4090, 1024 MiB, 24564 MiB, 5 %
1, NVIDIA GeForce GTX 1080 Ti, 200 MiB, 11264 MiB, 0 %
"""

NVIDIA_SMI_NOHEADER = "5, 1024\n"

OLLAMA_PS_LOADED = """NAME            ID              SIZE      PROCESSOR    UNTIL
qwen3.8:27b     abcd1234ef56    17 GB     100% GPU     4 minutes from now
"""

OLLAMA_PS_EMPTY = "NAME    ID    SIZE    PROCESSOR    UNTIL\n"


def test_parse_nvidia_smi_with_header():
    rows = gpu.parse_nvidia_smi(NVIDIA_SMI_HEADER)
    assert len(rows) == 2
    assert rows[0]["index"] == "0"
    assert rows[0]["utilization.gpu [%]"] == "5 %"


def test_parse_nvidia_smi_noheader():
    rows = gpu.parse_nvidia_smi(NVIDIA_SMI_NOHEADER, fields=["utilization.gpu", "memory.used"])
    assert rows == [{"utilization.gpu": "5", "memory.used": "1024"}]


def test_parse_nvidia_smi_empty():
    assert gpu.parse_nvidia_smi("") == []


def test_parse_ollama_ps_loaded():
    assert gpu.parse_ollama_ps(OLLAMA_PS_LOADED) == ["qwen3.8:27b"]


def test_parse_ollama_ps_empty():
    assert gpu.parse_ollama_ps(OLLAMA_PS_EMPTY) == []


def test_write_metrics_merges(tmp_path):
    run_dir = tmp_path / "demo_run"
    write_metrics(run_dir, {"a": 1})
    path = write_metrics(run_dir, {"b": 2})

    data = json.loads(path.read_text())
    assert data == {"a": 1, "b": 2}


def test_write_metrics_overwrites_existing_key(tmp_path):
    run_dir = tmp_path / "demo_run"
    write_metrics(run_dir, {"a": 1})
    path = write_metrics(run_dir, {"a": 2})

    assert json.loads(path.read_text()) == {"a": 2}


def test_check_cpu_mode():
    result = runner.invoke(app, ["--cpu"])
    assert result.exit_code == 0
    assert "torch" in result.stdout
