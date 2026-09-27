"""Chapter 07 — export a Hugging Face safetensors checkpoint to GGUF (llama.cpp's single-file
format: weights + tokenizer + chat-template metadata in one file) and chat with it in **Ollama**.

Pipeline: `to_gguf` (llama.cpp's `convert_hf_to_gguf.py`, bf16) -> `quantize` (`llama-quantize`,
Q8_0/Q5_K_M/Q4_K_M) -> `modelfile` (an explicit Go-template `TEMPLATE` + `stop` tokens + `num_ctx`)
-> `create` (`ollama create`) -> `chat`/`check_template` (Ollama's HTTP API, for reproducible
checks) -> `perplexity` (quantisation cost, `llama-perplexity` vs an HF forward pass on the same
text). Everything here runs on `rtx`: it needs the GGUF binaries, the Ollama service, and the GPU.
"""

import json
import re
import subprocess
from pathlib import Path

import httpx
import typer
from rich.console import Console

app = typer.Typer(add_completion=False, help=__doc__)
console = Console()

DEFAULT_LLAMACPP_DIR = Path.home() / "projects" / "llama.cpp"
DEFAULT_OLLAMA_BASE_URL = "http://127.0.0.1:11434"
DEFAULT_STOP = ["<|im_end|>", "<|endoftext|>"]


# ------------------------------------------------------------------------------- chat template


def ensure_chat_template(model_dir: str | Path) -> bool:
    """Return whether `model_dir` carries a chat template (a `chat_template.jinja` file, or a
    `chat_template` key in `tokenizer_config.json` — the two places `transformers` writes it to).

    Our base model (chapter 04, pre-SFT) has neither: it is exported without a template, and
    `convert_hf_to_gguf.py` simply embeds no `tokenizer.chat_template` metadata key for it. The
    SFT/DPO tokenizers (chapter 05's `attach_chat_template`) always have one.
    """
    model_dir = Path(model_dir)
    if (model_dir / "chat_template.jinja").exists():
        return True
    tok_cfg = model_dir / "tokenizer_config.json"
    if tok_cfg.exists():
        cfg = json.loads(tok_cfg.read_text())
        if cfg.get("chat_template"):
            return True
    return False


# ------------------------------------------------------------------------------------ to_gguf


def to_gguf(
    model_dir: str | Path,
    out_dir: str | Path,
    dtype: str = "bf16",
    llamacpp_dir: str | Path = DEFAULT_LLAMACPP_DIR,
) -> Path:
    """Convert `model_dir` (HF safetensors) to a single GGUF file with
    `convert_hf_to_gguf.py --outtype <dtype>`. Logs whether a chat template will be embedded."""
    model_dir = Path(model_dir)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    has_template = ensure_chat_template(model_dir)
    console.print(f"{model_dir.name}: chat template {'found' if has_template else 'NOT found (base model)'}")

    out_file = out_dir / f"{model_dir.name}-{dtype}.gguf"
    cmd = [
        "python",
        str(Path(llamacpp_dir) / "convert_hf_to_gguf.py"),
        str(model_dir),
        "--outfile",
        str(out_file),
        "--outtype",
        dtype,
        "--no-mtp",  # our checkpoints never have a multi-token-prediction head (see chapter text)
    ]
    console.print(" ".join(cmd))
    subprocess.run(cmd, check=True)
    return out_file


# ------------------------------------------------------------------------------------ quantize


def quantize(
    gguf_in: str | Path,
    quant_type: str = "Q8_0",
    out_path: str | Path | None = None,
    llamacpp_dir: str | Path = DEFAULT_LLAMACPP_DIR,
) -> Path:
    """Run `llama-quantize` on `gguf_in`, producing a smaller GGUF at `out_path`
    (default: same directory, `<stem>-<quant_type>.gguf` with the dtype suffix replaced)."""
    gguf_in = Path(gguf_in)
    if out_path is None:
        stem = re.sub(r"-(bf16|f16|f32)$", "", gguf_in.stem)
        out_path = gguf_in.with_name(f"{stem}-{quant_type}.gguf")
    out_path = Path(out_path)

    binary = Path(llamacpp_dir) / "build" / "bin" / "llama-quantize"
    cmd = [str(binary), str(gguf_in), str(out_path), quant_type]
    console.print(" ".join(cmd))
    subprocess.run(cmd, check=True)
    return out_path


# ---------------------------------------------------------------------------------- modelfile


def modelfile(
    gguf: str | Path,
    out_path: str | Path,
    system: str | None = "You are a helpful assistant.",
    num_ctx: int = 2048,
    stop: list[str] | None = None,
    temperature: float = 0.7,
) -> Path:
    """Write an Ollama `Modelfile` pointing `FROM` a local GGUF path (relative to the Modelfile's
    own directory, matching how `ollama create` resolves it), with an explicit ChatML `TEMPLATE`
    in Go-template syntax mirroring chapter 05's Jinja `CHAT_TEMPLATE`, one `PARAMETER stop` line
    per stop string, and `num_ctx`/`temperature`.

    Ollama can instead read the chat template `convert_hf_to_gguf.py` embeds in the GGUF's
    `tokenizer.chat_template` metadata key (drop the `TEMPLATE` block and it falls back to that).
    Both work; writing `TEMPLATE` here makes the prompt contract visible in one file instead of
    hidden inside the GGUF's metadata — see `07_export_to_ollama.md` for both routes side by side.

    `system` defaults to `chat.DEFAULT_SYSTEM` — the same string chapter 05's `render()` injects
    whenever the first message is not a system turn. Leaving `SYSTEM` unset in the Modelfile while
    the HF template always injects a default system turn is exactly the mismatch `check_template`
    is built to catch (see `07_export_to_ollama.md` §"a real template-agreement bug").
    """
    if stop is None:
        stop = list(DEFAULT_STOP)
    gguf = Path(gguf)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    from_line = f"FROM ./{gguf.name}" if gguf.parent == out_path.parent else f"FROM {gguf}"

    lines = [from_line, ""]
    if system:
        lines += [f'SYSTEM """{system}"""', ""]
    lines += [
        'TEMPLATE """{{ if .System }}<|im_start|>system',
        "{{ .System }}<|im_end|>",
        '{{ end }}{{ range .Messages }}<|im_start|>{{ .Role }}',
        "{{ .Content }}<|im_end|>",
        '{{ end }}<|im_start|>assistant',
        '"""',
        "",
    ]
    for s in stop:
        lines.append(f"PARAMETER stop {s}")
    lines.append(f"PARAMETER num_ctx {num_ctx}")
    lines.append(f"PARAMETER temperature {temperature}")

    out_path.write_text("\n".join(lines) + "\n")
    console.print(f"wrote {out_path}")
    return out_path


# ------------------------------------------------------------------------------ ollama create


def create(name: str, modelfile_path: str | Path) -> None:
    """`ollama create <name> -f <modelfile_path>`. Never touches `~/.ollama` directly."""
    cmd = ["ollama", "create", name, "-f", str(modelfile_path)]
    console.print(" ".join(cmd))
    subprocess.run(cmd, check=True)


# ---------------------------------------------------------------------------------------- chat


def build_ollama_chat_payload(
    messages: list[dict[str, str]],
    model: str,
    stream: bool = False,
    options: dict | None = None,
) -> dict:
    """The JSON body for Ollama's `POST /api/chat` (pure, unit-tested)."""
    payload: dict = {"model": model, "messages": messages, "stream": stream}
    if options:
        payload["options"] = options
    return payload


def chat(
    name: str,
    messages: list[dict[str, str]],
    base_url: str = DEFAULT_OLLAMA_BASE_URL,
    options: dict | None = None,
    timeout: float = 120.0,
) -> str:
    """Send `messages` to `POST {base_url}/api/chat` with `stream: false` and return the
    assistant's reply text — the reproducible check this chapter uses instead of `ollama run`."""
    payload = build_ollama_chat_payload(messages, name, stream=False, options=options)
    resp = httpx.post(f"{base_url}/api/chat", json=payload, timeout=timeout)
    resp.raise_for_status()
    return resp.json()["message"]["content"]


def generate_raw(
    name: str,
    raw_prompt: str,
    base_url: str = DEFAULT_OLLAMA_BASE_URL,
    options: dict | None = None,
    timeout: float = 120.0,
) -> str:
    """`POST {base_url}/api/generate` with `raw: true`: send `raw_prompt` exactly as-is, bypassing
    Ollama's own `TEMPLATE` entirely. Used to prove our HF chat template and the Modelfile's
    `TEMPLATE` agree — if they render the same string, generating from that string directly here
    should behave the same as `chat()` templating the same messages through Ollama's own route."""
    payload: dict = {"model": name, "prompt": raw_prompt, "raw": True, "stream": False}
    if options:
        payload["options"] = options
    resp = httpx.post(f"{base_url}/api/generate", json=payload, timeout=timeout)
    resp.raise_for_status()
    return resp.json()["response"]


# -------------------------------------------------------------------------------- check_template

LEAK_MARKERS = ("<|im_start|>", "<|im_end|>", "<|endoftext|>")


def check_template(
    name: str,
    model_dir: str | Path,
    base_url: str = DEFAULT_OLLAMA_BASE_URL,
    prompt_text: str = "Reply with exactly the word PONG.",
) -> dict:
    """Send one fixed prompt two ways and compare:

    1. `chat()` — Ollama's own `/api/chat`, templated with the Modelfile's `TEMPLATE`.
    2. `generate_raw()` — the *same* conversation rendered ourselves with the HF tokenizer's
       `chat_template` (chapter 05's `render()`), sent through `/api/generate` with `raw: true`.

    If the two templates genuinely agree, both routes feed the model the same prompt string, so
    at `temperature: 0` (deterministic) they should produce the same completion. Also checks that
    neither reply leaks a ChatML control token, and that both stopped (did not run to `num_ctx`).
    """
    from .chat import attach_chat_template, render
    from transformers import AutoTokenizer

    messages = [{"role": "user", "content": prompt_text}]
    options = {"temperature": 0, "seed": 0}

    chat_reply = chat(name, messages, base_url=base_url, options=options)

    tokenizer = AutoTokenizer.from_pretrained(str(model_dir))
    if tokenizer.chat_template is None:
        attach_chat_template(tokenizer)
    rendered_prompt = render(messages, tokenizer, add_generation_prompt=True)
    raw_reply = generate_raw(name, rendered_prompt, base_url=base_url, options=options)

    leaked = any(m in chat_reply for m in LEAK_MARKERS) or any(m in raw_reply for m in LEAK_MARKERS)
    result = {
        "prompt": prompt_text,
        "rendered_prompt": rendered_prompt,
        "chat_reply": chat_reply,
        "raw_reply": raw_reply,
        "templates_agree": chat_reply.strip() == raw_reply.strip(),
        "leaked_special_tokens": leaked,
    }
    console.print(json.dumps(result, indent=2))
    return result


# --------------------------------------------------------------------------------- perplexity


def parse_perplexity_output(text: str) -> float:
    """Extract the final PPL number from `llama-perplexity`'s log, e.g. a line
    `Final estimate: PPL = 32.1234 +/- 0.5678` -> `32.1234`."""
    match = re.search(r"Final estimate:\s*PPL\s*=\s*([\d.]+)", text)
    if not match:
        raise ValueError(f"could not find 'Final estimate: PPL = ...' in:\n{text}")
    return float(match.group(1))


def perplexity(
    gguf: str | Path,
    text_file: str | Path,
    ctx: int = 1024,
    llamacpp_dir: str | Path = DEFAULT_LLAMACPP_DIR,
) -> float:
    """Run `llama-perplexity -m <gguf> -f <text_file> -c <ctx>` and parse its final PPL."""
    binary = Path(llamacpp_dir) / "build" / "bin" / "llama-perplexity"
    cmd = [str(binary), "-m", str(gguf), "-f", str(text_file), "-c", str(ctx)]
    console.print(" ".join(cmd))
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return parse_perplexity_output(result.stdout + result.stderr)


def hf_perplexity(model_dir: str | Path, text_file: str | Path, max_len: int = 1024) -> float:
    """HF bf16 reference perplexity on the same text file, for the quantisation-cost table:
    non-overlapping `max_len`-token windows, `exp(total cross-entropy / total tokens)`."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.bfloat16 if device == "cuda" else torch.float32
    tokenizer = AutoTokenizer.from_pretrained(str(model_dir))
    model = AutoModelForCausalLM.from_pretrained(str(model_dir), dtype=dtype).to(device).eval()

    text = Path(text_file).read_text()
    ids = tokenizer(text, add_special_tokens=False)["input_ids"]

    total_nll = 0.0
    total_tokens = 0
    with torch.no_grad():
        for start in range(0, len(ids) - 1, max_len):
            window = ids[start : start + max_len]
            if len(window) < 2:
                continue
            input_ids = torch.tensor([window], device=device)
            out = model(input_ids=input_ids, labels=input_ids)
            n = len(window) - 1  # `labels` internally shifts by one; that many tokens are scored
            total_nll += out.loss.item() * n
            total_tokens += n
    return float(torch.exp(torch.tensor(total_nll / total_tokens)))


# ------------------------------------------------------------------------------------- Typer CLI


@app.command("to-gguf")
def to_gguf_cmd(
    model_dir: str = typer.Argument(..., help="HF safetensors dir, e.g. runs/models/tiny-qwen35-110m-dpo"),
    out_dir: str = typer.Option("runs/export", help="directory for the .gguf file"),
    dtype: str = typer.Option("bf16"),
    llamacpp_dir: str = typer.Option(str(DEFAULT_LLAMACPP_DIR)),
) -> None:
    to_gguf(model_dir, out_dir, dtype=dtype, llamacpp_dir=llamacpp_dir)


@app.command("quantize")
def quantize_cmd(
    gguf_in: str = typer.Argument(...),
    quant_type: str = typer.Option("Q8_0"),
    out_path: str = typer.Option(None),
    llamacpp_dir: str = typer.Option(str(DEFAULT_LLAMACPP_DIR)),
) -> None:
    quantize(gguf_in, quant_type=quant_type, out_path=out_path, llamacpp_dir=llamacpp_dir)


@app.command("modelfile")
def modelfile_cmd(
    gguf: str = typer.Argument(...),
    out_path: str = typer.Argument(...),
    system: str = typer.Option("You are a helpful assistant."),
    num_ctx: int = typer.Option(2048),
    temperature: float = typer.Option(0.7),
) -> None:
    modelfile(gguf, out_path, system=system, num_ctx=num_ctx, stop=list(DEFAULT_STOP), temperature=temperature)


@app.command("create")
def create_cmd(name: str = typer.Argument(...), modelfile_path: str = typer.Argument(...)) -> None:
    create(name, modelfile_path)


@app.command("chat")
def chat_cmd(
    name: str = typer.Argument(...),
    prompt: str = typer.Option(..., "--prompt"),
    base_url: str = typer.Option(DEFAULT_OLLAMA_BASE_URL),
) -> None:
    reply = chat(name, [{"role": "user", "content": prompt}], base_url=base_url)
    console.print(reply)


@app.command("check-template")
def check_template_cmd(
    name: str = typer.Argument(...),
    model_dir: str = typer.Argument(...),
    base_url: str = typer.Option(DEFAULT_OLLAMA_BASE_URL),
) -> None:
    check_template(name, model_dir, base_url=base_url)


@app.command("perplexity")
def perplexity_cmd(
    gguf: str = typer.Argument(...),
    text_file: str = typer.Argument(...),
    ctx: int = typer.Option(1024),
    llamacpp_dir: str = typer.Option(str(DEFAULT_LLAMACPP_DIR)),
) -> None:
    ppl = perplexity(gguf, text_file, ctx=ctx, llamacpp_dir=llamacpp_dir)
    console.print(f"PPL({gguf}) = {ppl:.4f}")


@app.command("hf-perplexity")
def hf_perplexity_cmd(
    model_dir: str = typer.Argument(...),
    text_file: str = typer.Argument(...),
    max_len: int = typer.Option(1024),
) -> None:
    ppl = hf_perplexity(model_dir, text_file, max_len=max_len)
    console.print(f"PPL({model_dir}) = {ppl:.4f}")


if __name__ == "__main__":
    app()
