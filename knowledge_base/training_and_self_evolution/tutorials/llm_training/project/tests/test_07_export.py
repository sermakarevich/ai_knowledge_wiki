"""Chapter 07 — GGUF/Ollama export helpers. CPU only, no network, no subprocess calls: every
function under test here is a pure string/JSON transform; `to_gguf`/`quantize`/`create`/`perplexity`
themselves shell out to `llama.cpp`/`ollama` binaries and are exercised on `rtx`, not here."""

import json

from llm_tutorial.export import (
    build_ollama_chat_payload,
    ensure_chat_template,
    modelfile,
    parse_perplexity_output,
)


# ------------------------------------------------------------------------------------ modelfile


def test_modelfile_contains_required_lines(tmp_path):
    gguf = tmp_path / "tiny-qwen35-110m-dpo-Q8_0.gguf"
    gguf.touch()
    out_path = tmp_path / "Modelfile"

    modelfile(gguf, out_path, num_ctx=4096)
    text = out_path.read_text()

    assert "FROM ./tiny-qwen35-110m-dpo-Q8_0.gguf" in text
    assert "TEMPLATE" in text
    assert "PARAMETER stop <|im_end|>" in text
    assert "PARAMETER stop <|endoftext|>" in text
    assert "PARAMETER num_ctx 4096" in text


def test_modelfile_default_stop_tokens(tmp_path):
    gguf = tmp_path / "m.gguf"
    gguf.touch()
    out_path = tmp_path / "Modelfile"

    modelfile(gguf, out_path)
    text = out_path.read_text()

    assert text.count("PARAMETER stop") == 2


def test_modelfile_optional_system(tmp_path):
    gguf = tmp_path / "m.gguf"
    gguf.touch()
    out_path = tmp_path / "Modelfile"

    modelfile(gguf, out_path, system="You are a pirate.")
    text = out_path.read_text()

    assert 'SYSTEM """You are a pirate."""' in text


def test_modelfile_from_line_absolute_when_different_dir(tmp_path):
    gguf_dir = tmp_path / "ggufs"
    gguf_dir.mkdir()
    gguf = gguf_dir / "m.gguf"
    gguf.touch()
    out_dir = tmp_path / "modelfiles"
    out_dir.mkdir()
    out_path = out_dir / "Modelfile"

    modelfile(gguf, out_path)
    text = out_path.read_text()

    assert f"FROM {gguf}" in text


# ----------------------------------------------------------------------------- ensure_chat_template


def test_ensure_chat_template_detects_jinja_file(tmp_path):
    (tmp_path / "chat_template.jinja").write_text("{{ messages }}")
    assert ensure_chat_template(tmp_path) is True


def test_ensure_chat_template_detects_tokenizer_config_key(tmp_path):
    (tmp_path / "tokenizer_config.json").write_text(json.dumps({"chat_template": "{{ messages }}"}))
    assert ensure_chat_template(tmp_path) is True


def test_ensure_chat_template_absent(tmp_path):
    (tmp_path / "tokenizer_config.json").write_text(json.dumps({"eos_token": "<|endoftext|>"}))
    assert ensure_chat_template(tmp_path) is False


def test_ensure_chat_template_no_files_at_all(tmp_path):
    assert ensure_chat_template(tmp_path) is False


# ------------------------------------------------------------------------- parse_perplexity_output


CANNED_LOG = """\
build: 1234 (9723942a) with cc (Ubuntu 13.3.0) for x86_64-linux-gnu
llama_model_loader: loaded meta data with 30 key-value pairs and 147 tensors
perplexity: tokenizing the input ..
perplexity: tokenization took 12.34 ms
perplexity: calculating perplexity over 195 chunks, n_ctx=1024, batch_size=2048, n_seq=1
perplexity: 1.23 seconds per pass - ETA 4.02 minutes
[1]4.5975,[2]5.1234,[3]6.0102,[4]5.8877,
Final estimate: PPL = 20.1234 +/- 0.2345

llama_perf_context_print:        load time =    120.45 ms
"""


def test_parse_perplexity_output_extracts_final_estimate():
    assert parse_perplexity_output(CANNED_LOG) == 20.1234


def test_parse_perplexity_output_raises_when_missing():
    import pytest

    with pytest.raises(ValueError):
        parse_perplexity_output("no ppl line here")


# --------------------------------------------------------------------- build_ollama_chat_payload


def test_build_ollama_chat_payload_shape():
    messages = [{"role": "user", "content": "Reply with exactly the word PONG."}]
    payload = build_ollama_chat_payload(messages, "tiny-qwen35-110m-dpo")

    assert payload == {
        "model": "tiny-qwen35-110m-dpo",
        "messages": messages,
        "stream": False,
    }


def test_build_ollama_chat_payload_with_options():
    messages = [{"role": "user", "content": "hi"}]
    payload = build_ollama_chat_payload(messages, "m", options={"temperature": 0, "seed": 0})

    assert payload["options"] == {"temperature": 0, "seed": 0}
    assert payload["stream"] is False
